#!/usr/bin/env python3
"""
check_lean_attestations_rankjump.py -- lift the LATTICE HALF of named CM_POINTS_RHO20 rows
to Tier A on the strength of kernel-checked statements, but only after (i) the attested
statement is shown, by exact recomputation here, to be about THAT row, and (ii) Stream 2's
own gate readings (producer != verifier) are on record in the attestation.

Inputs
  refs/lean_attestations_rankjump_2026_09_27.json   the attestations (data, with provenance)
  data/certificates/CM_POINTS_RHO20.json             the rows

What is checked per attestation (exact integer arithmetic, norm 2xy + 2Nz^2):
  A1  the row exists: (candidate, v) is a row of the certificate, and the row's N is the
      attestation's N
  A2  v^2 recomputed here equals both the row's -minus_v2 and the attested v_norm
  A3  every attested basis vector is orthogonal to v (pairing xq + yp + 2Nzr = 0)
  A4  the attested 2x2 Gram of that basis, recomputed here, equals the attested gram, and
      is SL(2,Z)-equivalent to the row's reduced form: Gauss-reduce the attested Gram's
      form and compare with the row's T_X_reduced_form_abc
  A5  frame determinant det(v | w1 | w2) recomputed equals the attested frame_det, and
      the orthogonal-determinant identity det(gram) * v^2 = -2N * det(frame)^2 holds
  A6  the gate record: G1 exit 0, G2 exit 0, G4 exit 0, print_axioms exit 0 with exactly
      {propext, Classical.choice, Quot.sound}, none of the audited failures in the
      attested file, producer_neq_verifier true. (G3's exit is 1 in a repository with
      registered axioms; what matters is that the attested declarations are not among
      the failures -- recorded as read.)
  A7  optional --verify-source-files: the attested file exists at the given worktree
      path and its sha256 matches (refuses on mismatch; skipped if the path is absent).
A row gets lattice_tier "A" only if A1-A6 all hold; otherwise it stays "B" with the
failing clause named. The output certificate is an OVERLAY on CM_POINTS_RHO20.json:
nothing in that certificate is modified. The z-recognition of each row and the
identification v^perp = T_X stay Tier B / Tier L, as the attestations themselves say.

Controls: checkers/test_lean_attestations_rankjump_controls.py.

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: checkers/test_lean_attestations_rankjump_controls.py | Reviewed-by: N
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AUDIT_DATE = "2026-09-27"
STD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
def _repos_root():
    """The directory holding the sibling repositories: walk up from this file (which may live
    in a git worktree under .claude/worktrees/) until the LeanProposal repo is a sibling."""
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


def check_attestation(att, cm, verify_files=False):
    fam = cm["families"].get(att["candidate"])
    out = {"id": att["id"], "candidate": att["candidate"], "v": att["v"], "clauses": {}}
    if fam is None:
        out["clauses"]["A1_row_exists"] = False
        out["lattice_tier"] = "B"
        out["reason"] = "candidate not in certificate"
        return out
    N = int(fam["n"])
    row = next((r for r in fam["rows"] if r["v"] == att["v"]), None)
    c = out["clauses"]
    c["A1_row_exists"] = row is not None and N == int(att["N"])
    if row is None:
        out["lattice_tier"] = "B"
        out["reason"] = "no such row"
        return out
    v = att["v"]
    c["A2_norm"] = (norm(N, v) == -int(row["minus_v2"]) == int(att["claims"]["v_norm"]))
    w1, w2 = att["claims"]["perp_basis"]
    c["A3_basis_orthogonal"] = pair(N, v, w1) == 0 and pair(N, v, w2) == 0
    gram = [[pair(N, w1, w1), pair(N, w1, w2)], [pair(N, w2, w1), pair(N, w2, w2)]]
    c["A4_gram_matches_attested"] = gram == att["claims"]["gram"]
    a, b, cc = gram[0][0] // 2, gram[0][1], gram[1][1] // 2
    reduced = reduce_form(a, b, cc)
    c["A4_reduced_form_is_row_T"] = list(reduced) == list(row["T_X_reduced_form_abc"]) == list(att["claims"]["reduced_form"])
    fd = det3(v, w1, w2)
    gdet = gram[0][0] * gram[1][1] - gram[0][1] * gram[1][0]
    c["A5_frame_det"] = fd == int(att["claims"]["frame_det"]) and gdet * norm(N, v) == -2 * N * fd * fd
    vb = att["verified_by_stream2"]
    c["A6_gates"] = (vb.get("G1_lake_build_Agora", {}).get("exit") == 0 and vb.get("G2_sorry_grep", {}).get("exit") == 0
                     and vb.get("G4_statement_lock", {}).get("exit") == 0
                     and vb.get("print_axioms", {}).get("exit") == 0
                     and set(vb.get("print_axioms", {}).get("axioms", [])) == STD_AXIOMS
                     and any(t in vb.get("print_axioms", {}).get("on", []) for t in att["source"]["theorems"])
                     and vb.get("G3_axiom_audit", {}).get("none_in_MnLattice_sec3b", False) is True
                     and vb.get("producer_neq_verifier") is True)
    if verify_files:
        root = SOURCE_ROOTS.get(att["source"]["repo"])
        f = root / att["source"]["file"] if root else None
        if f is not None and f.exists():
            c["A7_source_sha256"] = hashlib.sha256(f.read_bytes()).hexdigest() == att["source"]["file_sha256"]
        else:
            c["A7_source_sha256"] = None
    ok = all(v_ is True for k, v_ in c.items() if k != "A7_source_sha256") and c.get("A7_source_sha256") in (None, True)
    out["lattice_tier"] = "A" if ok else "B"
    out["row_z"] = row.get("z_value_if_rational")
    out["row_D"] = row.get("D")
    out["what_is_tier_A"] = "v^2, the exact orthogonal complement as a set, its Gram matrix and the index" if ok else None
    out["what_stays_tier_B"] = "z-recognition (numeric); v algebraic at tau (Lefschetz)"
    out["what_stays_tier_L"] = "v^perp = T_X (Dolgachev 1996 sec. 7 / Doran 1998 Thm 5.13)"
    out["cited"] = {k: att["source"][k] for k in ("repo", "file", "commit", "file_sha256", "theorems")}
    if not ok:
        out["reason"] = [k for k, v_ in c.items() if v_ is False]
    return out


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--attestations", default=REPO / "refs" / "lean_attestations_rankjump_2026_09_27.json", type=Path)
    ap.add_argument("--cm", default=REPO / "data" / "certificates" / "CM_POINTS_RHO20.json", type=Path)
    ap.add_argument("--verify-source-files", action="store_true")
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    atts = json.loads(a.attestations.read_text())
    cm = json.loads(a.cm.read_text())
    results = [check_attestation(att, cm, a.verify_source_files) for att in atts["attestations"]]
    for r in results:
        print(f"  {r['id']:16s} {r['candidate']} v={r['v']} z={r.get('row_z')} D={r.get('row_D')} -> lattice_tier {r['lattice_tier']}"
              + (f"  ({r.get('reason')})" if r["lattice_tier"] != "A" else ""))
    n_a = sum(r["lattice_tier"] == "A" for r in results)
    print(f"rows lifted to Tier A (lattice half): {n_a} / {len(results)}; pending: {[p['id'] for p in atts.get('pending', [])]}")
    if a.emit:
        cert = {
            "certificate": "CM_POINTS_RHO20_LATTICE_TIER", "checker": "checkers/check_lean_attestations_rankjump.py",
            "checker_version": "1.0.0", "date": AUDIT_DATE,
            "status": "OVERLAY on CM_POINTS_RHO20.json (unchanged): per-row lattice_tier granted from kernel-checked "
                      "statements after exact recomputation that each statement is about that row and after Stream 2's "
                      "own gate readings. The rho = 20 cut stays read narrowly (D7'); nothing ranks; cooper_s10 rows, "
                      "if any, stay ADVISORY (D6').",
            "rows": results, "pending": atts.get("pending", []),
            "inputs": {"sha256": {"refs/lean_attestations_rankjump_2026_09_27.json": sha(a.attestations),
                                  "data/certificates/CM_POINTS_RHO20.json": sha(a.cm)}},
            "not_claimed": ["anything about z beyond the CM certificate's numeric recognition",
                            "that v^perp is T_X (Tier L)", "any promotion of cooper_s10", "any physical reading"],
            "controls": "checkers/test_lean_attestations_rankjump_controls.py",
            "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: gates re-run by Stream 2 in the producer's "
                          "worktree (exit codes in the attestation file) + checkers/test_lean_attestations_rankjump_controls.py | Reviewed-by: N",
        }
        out = REPO / "data" / "certificates" / "CM_POINTS_RHO20_LATTICE_TIER.json"
        out.write_text(json.dumps(cert, indent=2) + "\n")
        print("wrote", out)
    return 0 if n_a == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
