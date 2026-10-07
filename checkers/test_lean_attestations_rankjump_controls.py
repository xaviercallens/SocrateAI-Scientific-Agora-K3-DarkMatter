#!/usr/bin/env python3
"""
test_lean_attestations_rankjump_controls.py -- controls for checkers/check_lean_attestations_rankjump.py

Standing rule 1: a test that cannot fail is not a test. Every clause that grants Tier A
must be shown to withhold it on a tampered input (deep copies only).

  P0  real attestations: all six rows Tier A; the two s7 (-2)-rows have 2 independent files;
      --verify-source-files agrees where the producer worktrees are present (skipped, said so, if absent)
  N1  attested Gram tampered                       -> A4 false, that attestation fails
  N2  attested basis vector not orthogonal to v     -> A3 false
  N3  attested vector is not a certificate row      -> A1 false
  N4  gate record: print_axioms lists an extra axiom -> A6 false
  N5  gate record: producer_neq_verifier false      -> A6 false
  N6  attested frame determinant tampered           -> A5 false; an attestation WITHOUT frame_det still
      passes A5 through the determinant identity
  N7  file sha256 tampered with --verify-source-files -> A7 false (when the worktree is present)
  N8  a row whose only attestation fails            -> lattice_tier B (single-source rows are not
      rescued by the other file)
  N9  Q1: certificate kernel basis tampered to a non-unimodular relative -> tier B with the Q1 reason
  N10 Q2: certificate det_T_X tampered              -> tier B with the Q2 reason
"""
import copy
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "checkers"))
import check_lean_attestations_rankjump as la  # noqa: E402

failures = []


def check(name, cond, detail=""):
    tag = "ok   " if cond else "FAIL "
    print(f"  {tag} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


atts = json.loads((REPO_ROOT / "refs" / "lean_attestations_rankjump_2026_09_27.json").read_text())
cm = json.loads((REPO_ROOT / "data" / "certificates" / "CM_POINTS_RHO20.json").read_text())
GR = atts["gate_records"]


def one(att, gr=GR, cmx=cm, verify=False):
    return la.check_attestation(att, gr, cmx, verify)


rows = la.build_rows(atts, cm, False)
check("P0 six rows, all Tier A", len(rows) == 6 and all(r["lattice_tier"] == "A" for r in rows))
two = [r for r in rows if r["candidate"] == "cooper_s7" and r["v"] in ([1, -1, 0], [2, -4, 1])]
check("P0 the two s7 (-2)-rows have 2 independent files", all(r["independent_files_passing"] == 2 for r in two))
# advisory_family must mirror the CM certificate's family flag (LIVE since D15' => False), never a hardcode
check("P0 advisory_family mirrors CM_POINTS_RHO20.json per row",
      all(r["advisory_family"] == bool(cm["families"][r["candidate"]]["advisory"]) for r in rows))
_cm_adv = copy.deepcopy(cm); _cm_adv["families"]["cooper_s10"]["advisory"] = True
check("N0 a CM certificate flagging s10 advisory flips advisory_family on every s10 row",
      all(r["advisory_family"] for r in la.build_rows(atts, _cm_adv, False) if r["candidate"] == "cooper_s10"))
present = {k: (la.SOURCE_ROOTS[g["repo"]] / g["file"]).exists() for k, g in GR.items()}
if all(present.values()):
    rv = la.build_rows(atts, cm, True)
    check("P0 source sha256 verified for every attestation", all(a["clauses"].get("A7_source_sha256") is True for r in rv for a in r["attestations"]))
else:
    check(f"P0 some producer worktree absent ({present}) -> A7 skipped, not failed", all(r["lattice_tier"] == "A" for r in la.build_rows(atts, cm, True)))

lm_s7 = next(a for a in atts["attestations"] if a["id"] == "LM-s7-z-1")
s1_s7 = next(a for a in atts["attestations"] if a["id"] == "S1-s7-z-1")
lm_inf = next(a for a in atts["attestations"] if a["id"] == "LM-s7-zinf")

t = copy.deepcopy(lm_s7); t["claims"]["gram"] = [[2, 1], [1, 5]]
check("N1 tampered Gram fails A4", one(t)["clauses"]["A4_gram_matches_attested"] is False and not one(t)["ok"])
t = copy.deepcopy(lm_s7); t["claims"]["perp_basis"] = [[2, -3, 1], [1, 3, 0]]
check("N2 non-orthogonal basis fails A3", one(t)["clauses"]["A3_basis_orthogonal"] is False)
t = copy.deepcopy(lm_s7); t["v"] = [3, -4, 1]
check("N3 vector not a row fails A1", one(t)["clauses"]["A1_row_exists"] is False)
g = copy.deepcopy(GR); g["LM-RankJump-73f6fb1"]["verified_by_stream2"]["print_axioms"]["axioms"].append("sorryAx")
check("N4 extra axiom fails A6", one(lm_s7, g)["clauses"]["A6_gates"] is False)
g = copy.deepcopy(GR); g["LM-RankJump-73f6fb1"]["verified_by_stream2"]["producer_neq_verifier"] = False
check("N5 producer = verifier fails A6", one(lm_s7, g)["clauses"]["A6_gates"] is False)
t = copy.deepcopy(s1_s7); t["claims"]["frame_det"] = 1
check("N6 tampered frame det fails A5; no frame_det still passes via identity",
      one(t)["clauses"]["A5_frame_det"] is False and one(lm_s7)["clauses"]["A5_frame_det"] is True)
if present.get("LM-RankJump-73f6fb1"):
    g = copy.deepcopy(GR); g["LM-RankJump-73f6fb1"]["file_sha256"] = "0" * 64
    check("N7 tampered file sha fails A7", one(lm_s7, g, cm, True)["clauses"]["A7_source_sha256"] is False)
else:
    check("N7 skipped (LeanMaster worktree absent)", True)

# N8: break the only attestation of a genuinely single-source row -> that row B, others unaffected.
# (LM-s7-zinf is NOT single-source once S1-s7-zinf covers the same row too -- verified separately
# below, since double-sourcing a previously single-source row is itself worth asserting.)
rows_now = la.build_rows(atts, cm, False)
single_source_rows = [r for r in rows_now if r["independent_files_passing"] == 1]
check("N8 setup: at least one genuinely single-source row exists to tamper", len(single_source_rows) >= 1)
target_cand, target_v = single_source_rows[0]["candidate"], single_source_rows[0]["v"]
target_id = next(a["id"] for a in atts["attestations"] if a["v"] == target_v and a["candidate"] == target_cand)
a2 = copy.deepcopy(atts)
for a in a2["attestations"]:
    if a["id"] == target_id:
        a["claims"]["gram"] = [[9, 9], [9, 9]]
rows8 = la.build_rows(a2, cm, False)
r_target = next(r for r in rows8 if r["v"] == target_v and r["candidate"] == target_cand)
check(f"N8 single-source row ({target_id}) goes B when its attestation fails; others stay A",
      r_target["lattice_tier"] == "B" and sum(r["lattice_tier"] == "A" for r in rows8) == len(rows_now) - 1)

# N8b: LM-s7-zinf alone (the old N8 target) is no longer single-source, now that S1-s7-zinf also
# covers cooper_s7/(14,-14,-5) -- confirms the double-sourcing this session's work added, and that
# it is a real property of the DATA, not an artifact of this control.
zinf_row = next(r for r in rows_now if r["v"] == [14, -14, -5] and r["candidate"] == "cooper_s7")
check("N8b s7 z=infinity is double-sourced (Stream 1 sec. 3c + LeanMaster)",
      zinf_row["independent_files_passing"] == 2)

# N9: tamper the certificate's kernel basis to a non-unimodular relative (scale one vector by 2)
cm9 = copy.deepcopy(cm)
row9 = next(r for r in cm9["families"]["cooper_s7"]["rows"] if r["v"] == [2, -4, 1])
row9["T_X_kernel_basis"] = [[2, 4, 0], [0, -7, 1]]
r9 = next(r for r in la.build_rows(atts, cm9, False) if r["v"] == [2, -4, 1])
check("N9 non-unimodular kernel basis -> B with Q1 reason", r9["lattice_tier"] == "B" and "Q1" in r9.get("reason", ""))

# N10: tamper the certificate's det_T_X
cm10 = copy.deepcopy(cm)
row10 = next(r for r in cm10["families"]["cooper_s7"]["rows"] if r["v"] == [2, -4, 1])
row10["det_T_X"] = 8
r10 = next(r for r in la.build_rows(atts, cm10, False) if r["v"] == [2, -4, 1])
check("N10 disagreeing det_T_X -> B with Q2 reason", r10["lattice_tier"] == "B" and "Q2" in r10.get("reason", ""))

print()
if failures:
    print(f"FAILED: {len(failures)} control(s): {failures}")
    sys.exit(1)
print("all lean-attestation controls passed")
