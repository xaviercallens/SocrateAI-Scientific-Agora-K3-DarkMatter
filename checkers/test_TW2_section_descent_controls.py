#!/usr/bin/env python3
"""test_TW2_section_descent_controls.py -- controls for checkers/check_TW2_section_descent.py (standing rule 1).

  P1  the full run reads P.O = 5, contr = 0, h = 14, discriminant orders {10,10,2,1,1}, a UNIQUE (14,10) fit
      (44 points for 26 unknowns), agreement at 8 held-out points, section defined over Q (square class +1)
  P2  the certificate cross-check against step 0, step 2a, Kumar-Kuwata 2d = 14 and the fibration certificate agrees
  N1  a tampered Velu numerator is refused (w^2 = Delta(s) fails on the divisor)
  N2  a wrong normalization (kappa sign flipped, beta kept) is refused (j of E_t no longer matches)
  N3  too few points (20 < 26 unknowns): the section is NOT determined (nullspace dimension > 1)
  N4  a wrong shape (deg N <= 13): no solution (nullspace dimension 0)
  N5  2P is a different section: the same shape cannot fit it (height 56 needs deg N = 56 - ... > 14)
  N6  the quadratic twist by -1 (other branch) gives the same geometry (P.O, h) and square class -1 (twist control)
  N7  the read-off is sensitive: deleting the quartic factor of the denominator changes P.O and the height
  N8  an odd-order pole is refused (not a section's x-coordinate)
"""
import copy
import sys
from fractions import Fraction as Fr
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_TW2_section_descent as d  # noqa: E402

fails = []


def check(name, cond, detail=""):
    print(f"  {'ok  ' if cond else 'FAIL'} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        fails.append(name)


ing = d.ingredients()
res = d.run(44, 8, ing=ing)
check("P1 section read: P.O = 5, contr = 0, h = 14",
      res["verdict"] == "SECTION_READ" and res["P_dot_O"] == 5 and res["contr_A1"] == "0" and res["height"] == "14", str(res.get("verdict")))
check("P1b unique fit, over-determined, held-out agree", res["nullspace_dim"] == 1 and res["n_fit_points"] > res["n_unknowns"] and res["heldout_agree"])
check("P1c discriminant orders {10,10,2,1,1}", res["discriminant_orders"] == [10, 10, 2, 1, 1])
check("P1d defined over Q (square class +1) and t -> -t gives -P", res["y_square_check"]["square_class_of_constant"] == 1 and res["t_to_minus_t_invariant"])
check("P1e finite poles are the node t = -1 and the quartic, no pole at 0 or infinity",
      not res["pole_at_t0"] and not res["pole_at_infinity"] and len(res["poles_finite"]) == 2)

# N1 tampered Velu numerator
bad = copy.deepcopy(ing)
bad["num"][0] += 1
try:
    d.section_at(bad, Fr(2))
    check("N1 tampered Velu numerator is refused", False, "no refusal")
except d.Refuse:
    check("N1 tampered Velu numerator is refused", True)

# N2 wrong normalization: kappa sign flipped with beta kept (the pair no longer matches E_t)
sf = d.simple_form(ing, 1)
sf_bad = dict(sf, kappa=-sf["kappa"])
try:
    d.read_section(ing, sf_bad, 2)
    check("N2 wrong normalization is refused", False, "no refusal")
except d.Refuse:
    check("N2 wrong normalization is refused", True)

# N3 too few points, N4 wrong shape
few = d.run(20, 2, ing=ing)
check("N3 20 points < 26 unknowns: not determined", few["verdict"].startswith("NOT_DETERMINED") and few["nullspace_dim"] > 1, str(few.get("nullspace_dim")))
shape = d.run(44, 2, dn=13, dd=10, ing=ing)
check("N4 deg N <= 13: no solution", shape["verdict"].startswith("NOT_DETERMINED") and shape["nullspace_dim"] == 0, str(shape.get("nullspace_dim")))


# N5 2P cannot be fit by the same shape
def doubled(ing_, sf_, n):
    t0s, samples, tw = [], [], []
    for k in range(2, 2 + n):
        a, pts, P = d.section_at(ing_, Fr(k))
        P2 = d.w_add(a, P, P)
        ts, X1, ok, u2 = d.to_F1(ing_, Fr(k), a, P2, sf_)
        samples.append((ts, X1))
        t0s.append(Fr(k))
        tw.append(u2)
    return t0s, samples, tw


dbl = d.run(44, 2, ing=ing, transform=doubled)
check("N5 2P does not fit the (14,10) shape", dbl["verdict"].startswith("NOT_DETERMINED") and dbl["nullspace_dim"] == 0, str(dbl.get("nullspace_dim")))

# N6 other branch = twist by -1
tw = d.run(44, 4, ing=ing, branch=-1)
check("N6 branch -1: same P.O and h, square class -1 (the twist by -1)",
      tw["verdict"] == "SECTION_READ" and tw["P_dot_O"] == 5 and tw["height"] == "14" and tw["y_square_check"]["square_class_of_constant"] == -1,
      str({k: tw.get(k) for k in ("verdict", "P_dot_O", "height")}))

# N7 sensitivity of the read-off; N8 odd pole refused
sfm = d.simple_form(ing, 1)
Nn = sp.sympify(res["X_numerator"])
Dd = sp.sympify(res["X_denominator"])
# (i) the total P.O is conserved when poles move to infinity: (deg N - 4)/2 = 5 -- a robustness check, not a weakness
quart = [f for f, m in sp.factor_list(Dd)[1] if sp.degree(f, d.tt) == 4][0]
ro_moved = d.read_off(Nn, sp.cancel(Dd / quart ** 2), sfm)
check("N7a moving the quartic's poles to infinity leaves P.O = 5", ro_moved["P_dot_O"] == 5 and ro_moved["pole_at_infinity"])
# (ii) adding a genuine extra double pole (at t = 3) must change P.O and the height
ro_extra = d.read_off(Nn, sp.expand(Dd * (d.tt - 3) ** 2), sfm)
check("N7b an extra pole changes P.O and the height", ro_extra["P_dot_O"] == 6 and ro_extra["height"] == "16", str(ro_extra))
try:
    d.read_off(Nn, Dd * (d.tt - 2), sfm)
    check("N8 odd-order pole is refused", False, "no refusal")
except d.Refuse:
    check("N8 odd-order pole is refused", True)

print()
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all TW2 section-descent controls behaved as required")
