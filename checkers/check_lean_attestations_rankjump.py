#!/usr/bin/env python3
"""
check_lean_attestations_rankjump.py -- lift the LATTICE HALF of named CM_POINTS_RHO20 rows
to Tier A on the strength of kernel-checked statements, but only after (i) the attested
statement is shown, by exact recomputation here, to be about THAT row, and (ii) Stream 2's
own gate readings (producer != verifier) are on record for the attesting file.

Inputs
  refs/lean_attestations_rankjump_2026_09_27.json   attestations + per-file gate records (data)
  data/certificates/CM_POINTS_RHO20.json             the rows (never modified)

Per attestation (exact integer arithmetic, norm 2xy + 2Nz^2):
  A1  the row exists: (candidate, v) is a row of the certificate, with the attestation's N
  A2  v^2 recomputed here equals both the row's -minus_v2 and the attested v_norm
  A3  every attested basis vector is orthogonal to v
  A4  the 2x2 Gram of the attested basis, recomputed here, equals the attested gram, and
      Gauss-reduces to the row's T_X_reduced_form_abc (= the attested reduced_form)
  A5  det(v | w1 | w2) recomputed equals the attested frame_det when one is attested (else
      it is recorded), and the identity det(gram) * v^2 = -2N * det(frame)^2 holds
  A6  the file's gate record: G1 exit 0, G2 exit 0, G4 exit 0, print_axioms exit 0 with
      exactly {propext, Classical.choice, Quot.sound} covering at least one attested theorem,
      G3 with none_in_attested_file true (G3's exit may be 1 in a repository that registers
      disclosed axioms; what matters is that no attested declaration is among the failures),
      producer_neq_verifier true
  A7  --verify-source-files: the attested file exists at the producer's worktree path and its
      sha256 matches (refuses on mismatch; skipped, and said so, if the path is absent)
Per row (LeanMaster's two audit questions, 2026-09-27):
  Q1  the certificate's T_X_kernel_basis (unreduced) and the attested basis span the same
      sublattice: the integer change of basis M (kernel_basis * M = attested basis, solved
      exactly) is recorded together with the kernel basis's Gram; refuse if M is not
      unimodular
  Q2  det_T_X is sourced to the KERNEL-CHECKED Gram (4ac - b^2 of the attested reduced form)
      and compared with the certificate's det_T_X (which came from the -v^2 * 2N / div^2
      formula, Tier B); both are recorded and the certified one is named.
A row gets lattice_tier "A" iff at least one attestation passes A1-A7; the number of
independent attesting files is recorded. The output is an OVERLAY on CM_POINTS_RHO20.json.
cooper_s10 rows carry advisory_family: true (T0 D6'): Tier A lattice arithmetic promotes
nothing. z-recognition stays Tier B; v^perp = T_X stays Tier L; the index step is unproved.

Controls: checkers/test_lean_attestations_rankjump_controls.py.

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: checkers/test_lean_attestations_rankjump_controls.py | Reviewed-by: N
"""
import argparse
import hashlib
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AUDIT_DATE = "2026-09-27"
STD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def _repos_root():
    p = REPO
    for _ in range(6):
        if (p.parent / "SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal").exists():
            return p.parent
        p = p.parent
    return REPO.parent


SOURCE_ROOTS = {
    "SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal":
        _repos_root() / "SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal" / ".claude" / "worktrees" / "k3-criteria-stream2-directions-2026-09-27",
    "SocrateAI-Scientific-Agora-LeanMaster":
        _repos_root() / "SocrateAI-Scientific-Agora-LeanMaster" / ".claude" / "worktrees" / "rank-jump-lemma",
}


def norm(N, v):
    x, y, z = v
    return 2 * x * y + 2 * N * z * z


def pair(N, v, w):
    x, y, z = v
    p, q, r = w
    return x * q + y * p + 2 * N * z * r


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]))


def reduce_form(a, b, c):
    while True:
        if c < a:
            a, b, c = c, -b, a
            continue
        if not (-a < b <= a):
            k = (a - b) // (2 * a)
            b2 = b + 2 * a * k
            c = a * k * k + b * k + c
            b = b2
            continue
        if a == c and b < 0:
            b = -b
            continue
        return (a, b, c)


def change_of_basis(kernel_basis, target_basis):
    """Integer M (2x2) with target_j = sum_i M[i][j] kernel_i, solved exactly; None if not
    expressible; returns (M, det)."""
    k1, k2 = kernel_basis
    M = [[None, None], [None, None]]
    for j, t in enumerate(target_basis):
        # solve a*k1 + b*k2 = t over Q using two independent coordinates, verify on the third
        sol = None
        for (i1, i2) in ((0, 1), (0, 2), (1, 2)):
            det = k1[i1] * k2[i2] - k1[i2] * k2[i1]
            if det == 0:
                continue
            a = Fr(t[i1] * k2[i2] - t[i2] * k2[i1], det)
            b = Fr(k1[i1] * t[i2] - k1[i2] * t[i1], det)
            if all(a * k1[i] + b * k2[i] == t[i] for i in range(3)):
                sol = (a, b)
            break
        if sol is None or sol[0].denominator != 1 or sol[1].denominator != 1:
            return None, None
        M[0][j], M[1][j] = int(sol[0]), int(sol[1])
    return M, M[0][0] * M[1][1] - M[0][1] * M[1][0]


def check_attestation(att, gate_records, cm, verify_files=False):
    fam = cm["families"].get(att["candidate"])
    out = {"id": att["id"], "clauses": {}}
    if fam is None:
        out["clauses"]["A1_row_exists"] = False
        out["ok"] = False
        return out
    N = int(fam["n"])
    row = next((r for r in fam["rows"] if r["v"] == att["v"]), None)
    c = out["clauses"]
    c["A1_row_exists"] = row is not None and N == int(att["N"])
    if row is None:
        out["ok"] = False
        return out
    v = att["v"]
    cl = att["claims"]
    c["A2_norm"] = (norm(N, v) == -int(row["minus_v2"]) == int(cl["v_norm"]))
    w1, w2 = cl["perp_basis"]
    c["A3_basis_orthogonal"] = pair(N, v, w1) == 0 and pair(N, v, w2) == 0
    gram = [[pair(N, w1, w1), pair(N, w1, w2)], [pair(N, w2, w1), pair(N, w2, w2)]]
    c["A4_gram_matches_attested"] = gram == cl["gram"]
    a, b, cc = gram[0][0] // 2, gram[0][1], gram[1][1] // 2
    reduced = reduce_form(a, b, cc)
    c["A4_reduced_form_is_row_T"] = list(reduced) == list(row["T_X_reduced_form_abc"]) == list(cl["reduced_form"])
    fd = det3(v, w1, w2)
    gdet = gram[0][0] * gram[1][1] - gram[0][1] * gram[1][0]
    out["frame_det_recomputed"] = fd
    c["A5_frame_det"] = (("frame_det" not in cl) or fd == int(cl["frame_det"])) and gdet * norm(N, v) == -2 * N * fd * fd
    gr = gate_records.get(att["gate_record"], {})
    vb = gr.get("verified_by_stream2", {})
    pa = vb.get("print_axioms", {})
    c["A6_gates"] = (vb.get("G1", {}).get("exit") == 0 and vb.get("G2", {}).get("exit") == 0
                     and vb.get("G4", {}).get("exit") == 0 and pa.get("exit") == 0
                     and set(pa.get("axioms", [])) == STD_AXIOMS
                     and any(t in pa.get("on", []) for t in att["theorems"])
                     and vb.get("G3", {}).get("none_in_attested_file") is True
                     and vb.get("producer_neq_verifier") is True)
    if verify_files:
        root = SOURCE_ROOTS.get(gr.get("repo"))
        f = root / gr["file"] if (root and gr.get("file")) else None
        c["A7_source_sha256"] = (hashlib.sha256(f.read_bytes()).hexdigest() == gr.get("file_sha256")) if (f and f.exists()) else None
    out["ok"] = all(x is True for k, x in c.items() if k != "A7_source_sha256") and c.get("A7_source_sha256") in (None, True)
    out["source"] = {k: gr.get(k) for k in ("repo", "file", "namespace", "commit", "file_sha256")}
    out["theorems"] = att["theorems"]
    out["failed_clauses"] = [k for k, x in c.items() if x is False]
    return out


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def build_rows(atts, cm, verify_files):
    rows = {}
    for att in atts["attestations"]:
        res = check_attestation(att, atts["gate_records"], cm, verify_files)
        key = (att["candidate"], tuple(att["v"]))
        rows.setdefault(key, {"candidate": att["candidate"], "v": att["v"], "attestations": [], "advisory_family": bool(att.get("advisory_family"))})
        rows[key]["attestations"].append(res)
    out = []
    for (cand, v), r in rows.items():
        fam = cm["families"][cand]
        N = int(fam["n"])
        row = next((x for x in fam["rows"] if x["v"] == list(v)), None)
        passing = [a for a in r["attestations"] if a["ok"]]
        r["independent_files_passing"] = len({a["source"]["file"] for a in passing})
        r["lattice_tier"] = "A" if passing else "B"
        if row is not None:
            r["row_z"] = row.get("z_value_if_rational")
            r["row_D"] = row.get("D")
            # Q1: change of basis from the certificate's kernel basis to a passing attested basis
            kb = row.get("T_X_kernel_basis")
            if passing and kb:
                att0 = next(a for a in atts["attestations"] if a["candidate"] == cand and a["v"] == list(v) and check_attestation(a, atts["gate_records"], cm)["ok"])
                M, dM = change_of_basis(kb, att0["claims"]["perp_basis"])
                kgram = [[pair(N, kb[0], kb[0]), pair(N, kb[0], kb[1])], [pair(N, kb[1], kb[0]), pair(N, kb[1], kb[1])]]
                r["Q1_kernel_basis"] = {"T_X_kernel_basis": kb, "its_gram": kgram, "attested_basis": att0["claims"]["perp_basis"],
                                        "change_of_basis_M": M, "det_M": dM, "unimodular": dM in (1, -1)}
                if dM not in (1, -1):
                    r["lattice_tier"] = "B"
                    r["reason"] = "Q1: kernel basis and attested basis are not related by a unimodular change"
            # Q2: det source
            if passing:
                a_, b_, c_ = att0["claims"]["reduced_form"]
                r["Q2_det_T_X"] = {"certified_here": 4 * a_ * c_ - b_ * b_, "source_certified": "4ac - b^2 of the kernel-checked reduced Gram",
                                   "certificate_det_T_X": row.get("det_T_X"), "certificate_source": "-v^2 * 2N / div(v)^2 (Tier B formula)",
                                   "agree": (4 * a_ * c_ - b_ * b_) == row.get("det_T_X")}
                if not r["Q2_det_T_X"]["agree"]:
                    r["lattice_tier"] = "B"
                    r["reason"] = "Q2: kernel Gram determinant disagrees with the certificate's det_T_X"
        r["what_is_tier_A"] = ("v^2, a saturated Z-basis of v^perp (as a set), its Gram matrix and reduced form" if r["lattice_tier"] == "A" else None)
        r["what_stays_tier_B"] = "z-recognition (numeric); v algebraic at tau (Lefschetz); the index step |det frame| = |v^2|/div (observed per row only)"
        r["what_stays_tier_L"] = "v^perp = T_X (Dolgachev 1996 sec. 7 / Doran 1998 Thm 5.13)"
        out.append(r)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--attestations", default=REPO / "refs" / "lean_attestations_rankjump_2026_09_27.json", type=Path)
    ap.add_argument("--cm", default=REPO / "data" / "certificates" / "CM_POINTS_RHO20.json", type=Path)
    ap.add_argument("--verify-source-files", action="store_true")
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    atts = json.loads(a.attestations.read_text())
    cm = json.loads(a.cm.read_text())
    rows = build_rows(atts, cm, a.verify_source_files)
    for r in rows:
        print(f"  {r['candidate']:10s} v={r['v']} z={r.get('row_z')} D={r.get('row_D')} -> lattice_tier {r['lattice_tier']} "
              f"({r['independent_files_passing']} file(s){', ADVISORY family' if r['advisory_family'] else ''})"
              + (f"  [{r.get('reason')}]" if r["lattice_tier"] != "A" else ""))
    n_a = sum(r["lattice_tier"] == "A" for r in rows)
    print(f"rows at Tier A (lattice half): {n_a} / {len(rows)}")
    if a.emit:
        cert = {
            "certificate": "CM_POINTS_RHO20_LATTICE_TIER", "checker": "checkers/check_lean_attestations_rankjump.py",
            "checker_version": "1.1.0", "date": AUDIT_DATE,
            "status": "OVERLAY on CM_POINTS_RHO20.json (unchanged): per-row lattice_tier granted from kernel-checked "
                      "statements after exact recomputation that each statement is about that row and after Stream 2's "
                      "own gate readings in each producer's worktree. The rho = 20 cut stays read narrowly (D7'); nothing "
                      "ranks; cooper_s10 rows stay ADVISORY (D6') whatever their lattice tier.",
            "rows": rows, "gate_records": atts["gate_records"], "not_proved_in_either_file": atts.get("not_proved_in_either_file", []),
            "inputs": {"sha256": {"refs/lean_attestations_rankjump_2026_09_27.json": sha(a.attestations),
                                  "data/certificates/CM_POINTS_RHO20.json": sha(a.cm)}},
            "not_claimed": ["anything about z beyond the CM certificate's numeric recognition",
                            "that v^perp is T_X (Tier L)", "the general index step (unproved in both files)",
                            "any promotion of cooper_s10", "any ranking", "any physical reading"],
            "controls": "checkers/test_lean_attestations_rankjump_controls.py",
            "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: gates re-run by Stream 2 in both producers' "
                          "worktrees (exit codes in the attestation file) + checkers/test_lean_attestations_rankjump_controls.py | Reviewed-by: N",
        }
        out = REPO / "data" / "certificates" / "CM_POINTS_RHO20_LATTICE_TIER.json"
        out.write_text(json.dumps(cert, indent=2) + "\n")
        print("wrote", out)
    return 0 if n_a == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
