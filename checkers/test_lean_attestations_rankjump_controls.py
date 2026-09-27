#!/usr/bin/env python3
"""
test_lean_attestations_rankjump_controls.py -- controls for checkers/check_lean_attestations_rankjump.py

Standing rule 1: a test that cannot fail is not a test. Every clause that grants Tier A
must be shown to withhold it on a tampered attestation (temp copies only).

  P0  real attestations: both rows Tier A; --verify-source-files agrees when the
      producer's worktree is present (skipped, not failed, if absent)
  N1  attested Gram tampered ([[2,1],[1,4]] -> [[2,1],[1,5]])  -> A4 false, tier B
  N2  attested basis vector not orthogonal to v                -> A3 false, tier B
  N3  attested vector is not a certificate row                 -> A1 false, tier B
  N4  gate record: print_axioms lists an extra axiom           -> A6 false, tier B
  N5  gate record: producer_neq_verifier false                 -> A6 false, tier B
  N6  frame determinant tampered                               -> A5 false, tier B
  N7  file sha256 tampered with --verify-source-files          -> A7 false, tier B
      (only when the producer's worktree is present)
"""
import copy
import json
import sys
import tempfile
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


def run(att, verify=False):
    return la.check_attestation(att, cm, verify)


base = [run(a) for a in atts["attestations"]]
check("P0 both rows Tier A", all(r["lattice_tier"] == "A" for r in base) and len(base) == 2)
root = la.SOURCE_ROOTS[atts["attestations"][0]["source"]["repo"]]
present = (root / atts["attestations"][0]["source"]["file"]).exists()
if present:
    v = [run(a, True) for a in atts["attestations"]]
    check("P0 source sha256 verified", all(r["clauses"].get("A7_source_sha256") is True for r in v))
else:
    check("P0 source file absent -> A7 skipped, not failed", all(run(a, True)["lattice_tier"] == "A" for a in atts["attestations"]))

second = atts["attestations"][1]

t = copy.deepcopy(second); t["claims"]["gram"] = [[2, 1], [1, 5]]
r = run(t); check("N1 tampered Gram -> B", r["lattice_tier"] == "B" and r["clauses"]["A4_gram_matches_attested"] is False)

t = copy.deepcopy(second); t["claims"]["perp_basis"] = [[2, -3, 1], [1, 3, 0]]
r = run(t); check("N2 non-orthogonal basis -> B", r["lattice_tier"] == "B" and r["clauses"]["A3_basis_orthogonal"] is False)

t = copy.deepcopy(second); t["v"] = [3, -4, 1]
r = run(t); check("N3 vector not a row -> B", r["lattice_tier"] == "B" and r["clauses"]["A1_row_exists"] is False)

t = copy.deepcopy(second); t["verified_by_stream2"]["print_axioms"]["axioms"] = ["propext", "Classical.choice", "Quot.sound", "sorryAx"]
r = run(t); check("N4 extra axiom -> B", r["lattice_tier"] == "B" and r["clauses"]["A6_gates"] is False)

t = copy.deepcopy(second); t["verified_by_stream2"]["producer_neq_verifier"] = False
r = run(t); check("N5 producer = verifier -> B", r["lattice_tier"] == "B" and r["clauses"]["A6_gates"] is False)

t = copy.deepcopy(second); t["claims"]["frame_det"] = 1
r = run(t); check("N6 tampered frame det -> B", r["lattice_tier"] == "B" and r["clauses"]["A5_frame_det"] is False)

if present:
    t = copy.deepcopy(second); t["source"]["file_sha256"] = "0" * 64
    r = run(t, True); check("N7 tampered file sha -> B", r["lattice_tier"] == "B" and r["clauses"]["A7_source_sha256"] is False)
else:
    check("N7 skipped (producer worktree absent)", True)

print()
if failures:
    print(f"FAILED: {len(failures)} control(s): {failures}")
    sys.exit(1)
print("all lean-attestation controls passed")
