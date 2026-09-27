#!/usr/bin/env python3
"""
test_inose_model_M7_controls.py -- controls for checkers/check_inose_model_M7.py

Standing rule 1: a test that cannot fail is not a test.

  P0  real run: all_ok (S1..S7)
  N1  scrambled z(q) (z[5] += 1): refused at S1 (disagrees with the b-file and the
      mirror map) -- the Hauptmodul identification is load-bearing and is checked
  N2  wrong level: J(q) J(q^5) is NOT a Laurent polynomial of the fitted degree in
      the level-7 coordinate -- the S3 verification fails on held-out orders
  N3  fit_laurent on a series that is not a Laurent polynomial of the stated pole
      order (pi with pole order 7 instead of 8) fails held-out verification
  N4  the class-number expectation is discriminating: with the allowed set of
      discriminants altered (drop -24), the count 5 cannot be reproduced
  N5  the kleinj control is discriminating: sigma/2 shifted by 1e-10 no longer
      matches kleinj at the certificate's tau
  N6  the exact evaluations at the loci: sigma^2 - 4 pi is 0 at z = -1 and z = 1/27
      and NON-zero at a generic rational point (z = 1/100)
"""
import sys
from fractions import Fraction as Fr
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "checkers"))

import mpmath as mp  # noqa: E402
import check_inose_model_M7 as im  # noqa: E402
from check_external_review_fable_2026_09_21 import reduced_primitive_forms  # noqa: E402

failures = []


def check(name, cond, detail=""):
    tag = "ok   " if cond else "FAIL "
    print(f"  {tag} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


N = 90   # shorter than the production order; enough for every clause below

# P0
res = im.run(n=N, verbose=False)
check("P0 all_ok on real inputs", res["all_ok"], str({k: v for k, v in res.items() if k.startswith("S")})[:300])

# N1
try:
    im.run(n=N, scramble="z", verbose=False)
    check("N1 scrambled z refused", False, "not refused")
except im.Refuse as e:
    check("N1 scrambled z refused", "b-file" in str(e) or "mirror" in str(e))

# N2
bad = im.run(n=N, level=5, verbose=False)
check("N2 level-5 pair is not a Laurent polynomial in the level-7 coordinate",
      not (bad["S3"]["sigma_all_orders"] and bad["S3"]["pi_all_orders"]))

# N3
alpha, beta, gamma, eta, loci, bfile, cm = im.load_inputs()
z = im.hauptmodul_series(alpha, beta, gamma, eta, N)
Jq = im.klein_J_times_q(N)
Jq7 = im.substitute_q7(im.klein_J_times_q(N // 7 + 1), N)
pi_shift = im.smul(Jq, Jq7, N)
_, ver_ok_order, ok8 = im.fit_laurent(pi_shift, z, 8, N)
# wrong pole order: treat q^8 pi as if it were q^7 pi (i.e. pi with pole order 7)
_, _, ok7 = im.fit_laurent(pi_shift, z, 7, N)
check("N3 correct pole order verifies; wrong pole order fails", ok8 and not ok7)

# N4
allowed = {-28, -27, -24, -19, -12, -7, -3}
double_D = [D for D in allowed if D not in (-3, -28, -7)]
full = sum(len(reduced_primitive_forms(D)) for D in double_D)
without_24 = sum(len(reduced_primitive_forms(D)) for D in double_D if D != -24)
check("N4 class-number count 5 needs D = -24 (h = 2)", full == 5 and without_24 == 3
      and res["S5"]["actual_double_zero_count"] == 5)

# N5
mp.mp.dps = 40
loc = "1/27"
h = loci[loc]
re, im2 = Fr(h["tau"]["re"]), Fr(h["tau"]["im_squared"])
tau = mp.mpc(mp.mpf(re.numerator) / re.denominator, mp.sqrt(mp.mpf(im2.numerator) / im2.denominator))
sv = Fr(res["S4_model"]["at_loci"][loc]["sigma"])
target = mp.mpf(sv.numerator) / sv.denominator / 2
check("N5 kleinj control matches sigma/2 and rejects a 1e-10 shift",
      abs(mp.kleinj(tau) - target) < mp.mpf(10) ** -25 and abs(mp.kleinj(tau) - (target + mp.mpf(10) ** -10)) > mp.mpf(10) ** -25)

# N6
s = [Fr(x) for x in res["S3"]["sigma_laurent"].replace("*z^-", " ").replace("(", "").replace(")", "").split(" + ")
     if x.strip()] if False else None  # (string parsing avoided; re-run the fit instead)
sig_shift = [Fr(0)] * N
for i in range(N - 6):
    sig_shift[i + 6] += Jq[i]
for i in range(N):
    sig_shift[i] += Jq7[i]
s_coeffs, _, _ = im.fit_laurent(sig_shift, z, 7, N)
p_coeffs, _, _ = im.fit_laurent(pi_shift, z, 8, N)
def Dz(zv):
    sv = im.laurent_eval(s_coeffs, zv)
    pv = im.laurent_eval(p_coeffs, zv)
    return sv * sv - 4 * pv
check("N6 sigma^2 - 4pi vanishes at the loci and not at z = 1/100",
      Dz(Fr(-1)) == 0 and Dz(Fr(1, 27)) == 0 and Dz(Fr(1, 100)) != 0)

print()
if failures:
    print(f"FAILED: {len(failures)} control(s): {failures}")
    sys.exit(1)
print("all Inose-model controls passed")
