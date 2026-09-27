#!/usr/bin/env python3
"""
test_certified_monodromy_L2_controls.py -- controls for checkers/check_certified_monodromy_L2.py

Standing rule 1: a test that cannot fail is not a test. The certified checker's
value is its rigour, so the controls exercise (i) that the pipeline certifies the
real family, (ii) that it REFUSES a different operator, and (iii) that each
rigorous helper is a genuine bound on cases where the truth is known exactly.

  P0  cooper_s7 certifies (all clauses); ~20 s
  N1  scrambled operator (L2[1][1] += 1): the true family's recognised Sym^2
      matrices are NOT enclosed (C-b fails), while the cusp control still passes
      (the scramble keeps the MUM structure) -- a different operator has different
      monodromy, rigorously
  N2  r_majorant is a lower bound of the distance to the nearest root, on
      a2(z) = z(1-26z-27z^2) shifted to several centres (roots 0, -1, 1/27 exact)
  N3  sup_ratio is an upper bound of the sup of (2m+1)/(m+1) over m >= 10 (exact
      sup = 21/11 at m=10), and not absurdly loose (< 2.5)
  N4  the geometric tail identities: T0(N) = sum_{m>N} x^m and T1(N) = sum_{m>N} m x^(m-1)
      dominate direct partial sums to a large cutoff (exact rationals)
  N5  a class of the recurrence: frobenius_certified's majorant bound |a_m| <= K rho^m
      actually holds for the exact partner coefficients at m = N0 .. N0+200 (s7)
  N6  uniqueness logic: a ball of diameter >= 1/MAX_DEN^2 must NOT be declared unique
      (two rationals of denominator <= MAX_DEN fit inside)
  N7  contains_exact rejects a rational outside the ball and accepts one inside
"""
import sys
from fractions import Fraction as Fr
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "checkers"))

from flint import acb, arb, ctx  # noqa: E402
import check_certified_monodromy_L2 as cm  # noqa: E402
import check_U1_lattice as u1  # noqa: E402

ctx.prec = cm.PREC_BITS
failures = []


def check(name, cond, detail=""):
    tag = "ok   " if cond else "FAIL "
    print(f"  {tag} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


# P0
res = cm.certify_family("cooper_s7", verbose=False)
check("P0 cooper_s7 certified", res["certified"], str({k: v for k, v in res["clauses"].items()})[:300])

# N1
try:
    bad = cm.certify_family("cooper_s7", verbose=False, scramble="operator")
    cb = [v for k, v in bad["clauses"].items() if k.startswith("C-b")]
    check("N1 scrambled operator: reference matrices NOT enclosed", not bad["certified"]
          and any(not v["all_entries_enclosed"] for v in cb))
    check("N1 scrambled operator: cusp control still passes (structure kept)",
          bad["clauses"]["C-a_cusp_loop_encloses_unipotent"]["holds"])
except cm.CertFailure as e:
    check("N1 scrambled operator refused", True)

# N2
L2, _ = u1.load_operators("cooper_s7")
cont = cm.CertContinuator(L2)
roots = [Fr(0), Fr(-1), Fr(1, 27)]
ok2 = True
for centre in [(Fr(1, 108), Fr(0)), (Fr(-1, 2), Fr(1, 2)), (Fr(-3, 2), Fr(0)), (Fr(1, 20), Fr(1, 50)), (Fr(-1, 4), Fr(-1, 4))]:
    rm = cm.r_majorant(cm.shift_poly(cont.a2, centre))
    dist2 = min((centre[0] - r) ** 2 + centre[1] ** 2 for r in roots)
    ok2 &= bool(rm * rm <= cm.A_(dist2)) and bool(rm > 0)
check("N2 r_majorant <= distance to nearest singular point, > 0", ok2)

# N3
s = cm.sup_ratio([1, 2], [1, 1], 10)
check("N3 sup_ratio bounds sup (2m+1)/(m+1), m>=10 (=21/11)", bool(s >= cm.A_(Fr(21, 11))) and bool(s < 2.5), str(s))

# N4
x = Fr(3, 5)
for N in (5, 40):
    T0 = cm.arb(x.numerator) / cm.arb(x.denominator)
    xa = T0
    T0v = xa ** (N + 1) / (arb(1) - xa)
    T1v = ((N + 1) * xa ** N * (arb(1) - xa) + xa ** (N + 1)) / (arb(1) - xa) ** 2
    s0 = sum(x ** m for m in range(N + 1, N + 400))
    s1 = sum(m * x ** (m - 1) for m in range(N + 1, N + 400))
    check(f"N4 tail identities dominate partial sums (N={N})",
          bool(T0v >= cm.A_(s0)) and bool(T1v >= cm.A_(s1)))

# N5
a = u1.holo_series(L2, cm.N0_FROB + 201)
lead, S, R = cm.theta_recurrence_pieces(L2)
Q1, Q2 = cm.sup_ratio(S[1], lead, cm.N0_FROB), cm.sup_ratio(S[2], lead, cm.N0_FROB)
rho = cm.ub((Q1 + (Q1 * Q1 + arb(4) * Q2).sqrt()) / arb(2)) * arb(105) / arb(100)
KA = cm.amax(*(cm.ub(cm.A_(a[k]) / rho ** k) for k in (cm.N0_FROB - 2, cm.N0_FROB - 1)))
ok5 = all(bool(cm.A_(abs(a[m])) <= KA * rho ** m) for m in range(cm.N0_FROB, cm.N0_FROB + 200))
check("N5 Frobenius majorant holds on 200 exact coefficients past N0", ok5)
# and it is a real bound: a smaller rho (the raw growth 27) with the same K must FAIL somewhere
rho_bad = arb(27) * arb(95) / arb(100)
ok5b = any(not bool(cm.A_(abs(a[m])) <= KA * rho_bad ** m) for m in range(cm.N0_FROB, cm.N0_FROB + 200))
check("N5 an under-estimated rho is caught by the exact coefficients", ok5b)

# N6 -- the closest pair of distinct rationals with denominators <= D is 1/D and
# 1/(D-1), at distance 1/(D(D-1)) > 1/D^2; a ball of diameter >= 1/D^2 may hold both,
# a ball of diameter < 1/D^2 cannot hold two.
D = cm.MAX_DEN
bound = Fr(1, D * D)
q1, q2 = Fr(1, D), Fr(1, D - 1)
mid = (q1 + q2) / 2
wide = acb(cm.A_(mid) + cm.A_(Fr(6, 10) * (q2 - q1)) * arb(0, 1), arb(0))   # diameter 1.2 * gap > 1/D^2
narrow = acb(cm.A_(mid) + cm.A_(Fr(2, 10) * bound) * arb(0, 1), arb(0))     # diameter 0.4/D^2
check("N6 wide ball is not unique; narrow ball is", not bool(cm.diameter(wide) < cm.A_(bound))
      and bool(cm.diameter(narrow) < cm.A_(bound)))
check("N6 wide ball indeed holds two admissible rationals (1/D and 1/(D-1))",
      cm.contains_exact(wide, q1) and cm.contains_exact(wide, q2)
      and q1.denominator <= D and q2.denominator <= D)
check("N6 narrow ball cannot hold both", not (cm.contains_exact(narrow, q1) and cm.contains_exact(narrow, q2)))

# N7
b = acb(arb(1, 1e-30), arb(0, 1e-30))
check("N7 contains_exact", cm.contains_exact(b, Fr(1)) and not cm.contains_exact(b, Fr(1, 1) + Fr(1, 10 ** 20)))

print()
if failures:
    print(f"FAILED: {len(failures)} control(s): {failures}")
    sys.exit(1)
print("all certified-monodromy controls passed")
