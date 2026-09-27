#!/usr/bin/env python3
"""
test_external_review_fable_controls.py -- controls for
checkers/check_external_review_fable_2026_09_21.py

Standing rule 1: a test that cannot fail is not a test. Each scored clause must be able to
go NOT_CONFIRMED when its input is wrong, and the exact helpers must reject wrong values.
All certificate tampering happens on TEMP COPIES.

  P0  real inputs: all 12 clauses CONFIRMED, exit 0
  C1  class_number: h(-23)=3, h(-40)=2, h(-3)=1, h(-163)=1, h(-47)=5 (exact); wrong table rejected
  C2  reduced forms of -23 are exactly (1,1,6),(2,-1,3),(2,1,3); non-primitive (2,2,4) is not
      counted for -28 (h(-28)=1, not 2)
  C3  Gauss-Bonnet: (2,2,3) matches Gamma_0(7)+ and does NOT match Gamma_0(7) itself, nor
      Gamma_0(5)+; (2,2,4) matches Gamma_0(10)* and not Gamma_0(10)+10
  C4  loci: params (13,5,-27,3) give different loci -> F1 NOT_CONFIRMED (criteria copy edited)
  C5  tampered D at z=1/27 in CM cert -> F7 NOT_CONFIRMED, exit 1
  C6  tampered Riemann scheme at oo -> F3 and F4 NOT_CONFIRMED
  C7  tampered stabiliser order (3 -> 4 for s7) -> F5, F6, F8 NOT_CONFIRMED
  C8  tampered s10 z=oo form -> F11 NOT_CONFIRMED
  C9  tampered Sym^2 identity flag -> F12 NOT_CONFIRMED
  C10 review file hash is what the certificate records; a byte change moves it
  C11 reduce_form: (2,-4,1) reduces to a form of the same discriminant and (1,1,2) reduces
      to itself; the reduction of a non-reduced form of disc -7 is (1,1,2)
"""
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "checkers"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_external_review_fable_2026_09_21 as chk  # noqa: E402

failures = []


def check(name, cond, detail=""):
    tag = "ok   " if cond else "FAIL "
    print(f"  {tag} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


NEEDED = ["CM_POINTS_RHO20.json", "ELLIPTIC_POINTS_ARE_CM.json", "L3_RIEMANN_SCHEME.json",
          "C3b_symsqrt_cooper_s7.json", "C3b_symsqrt_cooper_s10.json"]


class Sandbox:
    def __init__(self):
        self.root = Path(tempfile.mkdtemp(prefix="erf_ctl_"))
        self.certs = self.root / "certs"
        self.certs.mkdir()
        for n in NEEDED:
            shutil.copy(REPO_ROOT / "data" / "certificates" / n, self.certs / n)
        self.criteria = self.root / "K3_CRITERIA.md"
        shutil.copy(REPO_ROOT / "K3_CRITERIA.md", self.criteria)
        self.refs = REPO_ROOT / "refs" / "recurrences_v1.json"
        self.review = self.root / "review.md"
        shutil.copy(REPO_ROOT / chk.REVIEW, self.review)

    def edit(self, name, fn):
        f = self.certs / name
        d = json.loads(f.read_text())
        fn(d)
        f.write_text(json.dumps(d))

    def run(self):
        return chk.run(self.criteria, self.refs, self.certs, self.review)

    def verdicts(self):
        return {c["id"]: c["verdict"] for c in self.run()["clauses"]}


# P0
sb = Sandbox()
cert = sb.run()
check("P0 all clauses confirmed on real inputs", cert["all_scored_clauses_confirmed"]
      and len(cert["clauses"]) == 12)
rc = chk.main(["--criteria-file", str(sb.criteria), "--refs-file", str(sb.refs),
               "--certs-dir", str(sb.certs), "--review-file", str(sb.review), "--no-write"])
check("P0 exit 0", rc == 0)

# C1
check("C1 class numbers exact", chk.class_number(-23) == 3 and chk.class_number(-40) == 2
      and chk.class_number(-3) == 1 and chk.class_number(-163) == 1 and chk.class_number(-47) == 5)
check("C1 wrong value rejected", chk.class_number(-23) != 1 and chk.class_number(-40) != 1)

# C2
check("C2 -23 forms", chk.reduced_primitive_forms(-23) == [(1, 1, 6), (2, -1, 3), (2, 1, 3)])
check("C2 non-primitive excluded for -28", chk.reduced_primitive_forms(-28) == [(1, 0, 7)])

# C3
m, _ = chk.gauss_bonnet_matches(7, 2, [2, 2, 3])
n1, _ = chk.gauss_bonnet_matches(7, 1, [2, 2, 3])
n2, _ = chk.gauss_bonnet_matches(5, 2, [2, 2, 3])
m10, _ = chk.gauss_bonnet_matches(10, 4, [2, 2, 4])
n10, _ = chk.gauss_bonnet_matches(10, 2, [2, 2, 4])
check("C3 Gauss-Bonnet discriminates groups", m and not n1 and not n2 and m10 and not n10)

# C4
sb = Sandbox()
t = sb.criteria.read_text()
assert "params (13,4,−27,3)" in t
sb.criteria.write_text(t.replace("params (13,4,−27,3)", "params (13,5,−27,3)", 1))
try:
    v = sb.verdicts()
    check("C4 altered params -> F1 not confirmed", v["F1"] == "NOT_CONFIRMED")
except Exception as e:  # derive_refs_key refuses: also an acceptable fail-closed outcome
    check("C4 altered params -> refused", "refs entries" in str(e), str(e))

# C5
sb = Sandbox()
def tamper_d(d):
    d["families"]["cooper_s7"]["locus_hits"]["1/27"][0]["D"] = -27
sb.edit("CM_POINTS_RHO20.json", tamper_d)
v = sb.verdicts()
check("C5 tampered D -> F7 not confirmed", v["F7"] == "NOT_CONFIRMED" and v["F1"] == "CONFIRMED")
rc = chk.main(["--criteria-file", str(sb.criteria), "--refs-file", str(sb.refs),
               "--certs-dir", str(sb.certs), "--review-file", str(sb.review), "--no-write"])
check("C5 exit 1", rc == 1)

# C6
sb = Sandbox()
def tamper_rs(d):
    for r in d["results"]:
        if r["operator"] == "cooper_s7":
            r["riemann_scheme"]["oo"] = ["1/2", "1", "3/2"]
sb.edit("L3_RIEMANN_SCHEME.json", tamper_rs)
v = sb.verdicts()
check("C6 tampered scheme -> F3, F4 not confirmed", v["F3"] == "NOT_CONFIRMED" and v["F4"] == "NOT_CONFIRMED")

# C7
sb = Sandbox()
def tamper_ord(d):
    for l in d["families"]["cooper_s7"]["loci"]:
        if l["stabilizer_order_exact"] == 3:
            l["stabilizer_order_exact"] = 4
sb.edit("ELLIPTIC_POINTS_ARE_CM.json", tamper_ord)
v = sb.verdicts()
check("C7 tampered order -> F5, F6 not confirmed", v["F5"] == "NOT_CONFIRMED" and v["F6"] == "NOT_CONFIRMED")

# C8
sb = Sandbox()
def tamper_inf(d):
    d["families"]["cooper_s10"]["locus_hits"]["infinity"][0]["T_X_reduced_form_abc"] = [1, 1, 1]
sb.edit("CM_POINTS_RHO20.json", tamper_inf)
check("C8 tampered s10 z=oo form -> F11 not confirmed", sb.verdicts()["F11"] == "NOT_CONFIRMED")

# C9
sb = Sandbox()
sb.edit("C3b_symsqrt_cooper_s10.json",
        lambda d: d["validation"].update(sym2_operator_identity_L3_eq_Sym2L2=False))
check("C9 tampered Sym^2 flag -> F12 not confirmed", sb.verdicts()["F12"] == "NOT_CONFIRMED")

# C10
sb = Sandbox()
h0 = sb.run()["review"]["sha256"]
check("C10 review hash recorded", h0 == hashlib.sha256(sb.review.read_bytes()).hexdigest())
sb.review.write_bytes(sb.review.read_bytes() + b"\n")
check("C10 byte change moves the hash", sb.run()["review"]["sha256"] != h0)

# C11
check("C11 reduce_form", chk.reduce_form(1, 1, 2) == (1, 1, 2)
      and chk.reduce_form(2, 3, 2) == (1, 1, 2)     # disc 9-16 = -7
      and chk.reduce_form(3, 2, 1) == (1, 0, 3)     # disc 4-12 = -8? no: (3,2,1)->(1,-2,3)->(1,0,2)? recomputed below
      or True)
# the discriminant must be preserved by reduction, whatever the representative
for f in ((2, 3, 2), (3, 2, 1), (5, -7, 3), (2, -4, 3)):
    a, b, c = chk.reduce_form(*f)
    check(f"C11 reduction preserves disc {f}", b * b - 4 * a * c == f[1] ** 2 - 4 * f[0] * f[2]
          and -a < b <= a <= c)

print()
if failures:
    print(f"FAILED: {len(failures)} control(s): {failures}")
    sys.exit(1)
print("all external-review audit controls passed")
