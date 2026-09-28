#!/usr/bin/env python3
"""
test_C6_selector_adopted_controls.py -- controls for checkers/check_C6_selector_adopted.py

Standing rule 1: a test that cannot fail is not a test.

  P0  real K3_CRITERIA.md + real certificates: verified True for both families
  N1  K3_CRITERIA.md missing the AM-8/SEL-D text -> refused before any computation runs
  N2  CM_POINTS_RHO20.json's z=infinity row tampered to a different D -> refused
      (z_matches / matches_claim fails)
  N3  CM_COMPLETENESS.json's points_on_X0n_star for the claimed D tampered to 2 ->
      refused (unique_on_curve fails, even though the window still realizes the min)
  N4  the CLAIMED dict (what the criteria text asserts) edited to a wrong T -> refused
      (matches_claim fails) -- this exercises the comparison against prose, not just
      against the certificates, since a real drift is a prose bug, not a data bug
"""
import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "checkers"))
import check_C6_selector_adopted as ca  # noqa: E402

failures = []


def check(name, cond, detail=""):
    tag = "ok   " if cond else "FAIL "
    print(f"  {tag} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


class Sandbox:
    def __init__(self):
        self.root = Path(tempfile.mkdtemp(prefix="c6adopt_ctl_"))
        self.certs = self.root / "certs"
        self.certs.mkdir()
        for n in ("CM_POINTS_RHO20.json", "CM_COMPLETENESS.json", "C6_SELECTOR_COMPARISON.json"):
            shutil.copy(REPO_ROOT / "data" / "certificates" / n, self.certs / n)
        self.criteria = self.root / "K3_CRITERIA.md"
        shutil.copy(REPO_ROOT / "K3_CRITERIA.md", self.criteria)

    def edit_cert(self, name, fn):
        f = self.certs / name
        d = json.loads(f.read_text())
        fn(d)
        f.write_text(json.dumps(d))


# P0
sb = Sandbox()
res = ca.verify(sb.criteria, sb.certs)
check("P0 both families verified", all(r["ok"] for r in res.values()))

# N1
sb = Sandbox()
sb.criteria.write_text(sb.criteria.read_text().replace("AM-8", "AM-X").replace("SEL-D", "SEL-Z"))
try:
    ca.verify(sb.criteria, sb.certs)
    check("N1 missing AM-8 text refused", False, "not refused")
except ca.Refuse as e:
    check("N1 missing AM-8 text refused", "AM-8" in str(e))

# N2
sb = Sandbox()
def tamper_locus(d):
    d["families"]["cooper_s7"]["locus_hits"]["infinity"][0]["D"] = -99
sb.edit_cert("CM_POINTS_RHO20.json", tamper_locus)
try:
    ca.verify(sb.criteria, sb.certs)
    check("N2 tampered locus D refused", False, "not refused")
except ca.Refuse as e:
    check("N2 tampered locus D refused", "cooper_s7" in str(e))

# N3
sb = Sandbox()
def tamper_curve_count(d):
    for row in d["families"]["cooper_s7"]["per_D"]:
        if row["D"] == -3:
            row["points_on_X0n_star"] = 2
sb.edit_cert("CM_COMPLETENESS.json", tamper_curve_count)
try:
    ca.verify(sb.criteria, sb.certs)
    check("N3 tampered curve-point count refused", False, "not refused")
except ca.Refuse as e:
    check("N3 tampered curve-point count refused", "unique_on_curve=False" in str(e) or "cooper_s7" in str(e))

# N4
orig = dict(ca.CLAIMED)
ca.CLAIMED = copy.deepcopy(orig)
ca.CLAIMED["cooper_s7"]["T"] = [9, 9, 9]
sb = Sandbox()
try:
    ca.verify(sb.criteria, sb.certs)
    check("N4 wrong CLAIMED value refused", False, "not refused")
except ca.Refuse as e:
    check("N4 wrong CLAIMED value refused", "matches_claim=False" in str(e) or "cooper_s7" in str(e))
finally:
    ca.CLAIMED = orig

print()
if failures:
    print(f"FAILED: {len(failures)} control(s): {failures}")
    sys.exit(1)
print("all C6-selector-adopted controls passed")
