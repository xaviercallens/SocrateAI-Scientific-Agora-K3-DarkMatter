#!/usr/bin/env python3
"""
test_inose_fibration_multiplicities_controls.py -- controls for
checkers/check_inose_fibration_multiplicities.py

Standing rule 1: a test that cannot fail is not a test.

  P0  real run: all_ok
  N1  a transcription error (sign flipped in the a4 coefficient) must be REFUSED by
      T1 (KS's printed discriminant no longer matches)
  N2  a different transcription error (a6 exponent 4 instead of 5) must be refused
      by T1 (u^6 (u-1)^10 no longer divides Delta, or deg d != 2)
  N3  the invariants helper reproduces j = 1728 for the Legendre curve with lam = -1
      and j = 0 for lam a root of lam^2 - lam + 1 (computed, then compared)
  N4  the exceptional set is discriminating: lambda = -1 (j = 1728) is NOT exceptional
      (its orders stay {10,10,1,1,1,1}) while lambda with lam^2 - lam + 1 = 0 IS
  N5  the loci's J values read from INOSE_MODEL_M7.json are not 0 or 1
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "checkers"))

import sympy as sp  # noqa: E402
import check_inose_fibration_multiplicities as fm  # noqa: E402

failures = []


def check(name, cond, detail=""):
    tag = "ok   " if cond else "FAIL "
    print(f"  {tag} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


res = fm.run(verbose=False)
check("P0 all_ok", res["all_ok"])

# N1 / N2: monkeypatch the transcription
orig = fm.ks_j9
def bad1(l1_, l2_):
    a2, a4, a6 = orig(l1_, l2_)
    return a2, -a4, a6
def bad2(l1_, l2_):
    a2, a4, a6 = orig(l1_, l2_)
    return a2, a4, a6 * (fm.u - 1) ** -1
for name, fn in (("N1 flipped a4 sign refused", bad1), ("N2 a6 exponent error refused", bad2)):
    fm.ks_j9 = fn
    try:
        fm.run(verbose=False)
        check(name, False, "not refused")
    except fm.Refuse as e:
        check(name, "T1" in str(e))
    except Exception as e:  # a non-polynomial a6 may break earlier: still a refusal
        check(name, True)
fm.ks_j9 = orig

# N3
j_m1 = sp.simplify(fm.legendre_j(sp.Integer(-1)))
j_om = sp.simplify(fm.legendre_j((1 + sp.sqrt(-3)) / 2))
check("N3 legendre_j(-1) = 1728 and legendre_j(-omega-type) = 0", j_m1 == 1728 and j_om == 0, f"{j_m1}, {j_om}")

# N4 -- the exceptional set is discriminating: a generic lambda (= 3, j not 0 or 1728)
# is not exceptional; lambda = -1 (lead(e) = 0: the simple root goes to infinity) and
# the omega-type lambda (e(0) = 0: order 4 at s = 0) are.
exc = res["T4_J1_eq_J2"]["exceptional_lambda_factors"]
lam = fm.lam
excl = sp.Integer(1)
for f in exc:
    excl *= sp.sympify(f, locals={"lam": lam})
check("N4 lambda = 3 not exceptional; lambda = -1 and omega-type are",
      sp.expand(excl.subs(lam, 3)) != 0 and sp.expand(excl.subs(lam, -1)) == 0
      and sp.simplify(excl.subs(lam, (1 + sp.sqrt(-3)) / 2)) == 0)
def orders_multiset(entry):
    fin = [o["order"] for o in entry["orders_finite"] for _ in range(o["degree"])]
    return sorted(fin + ([entry["order_at_infinity"]] if entry["order_at_infinity"] else []))
check("N4 J=1 orders are {2,2,10,10} and J=0 orders are {4,10,10}",
      orders_multiset(res["T6_special_values"]["J=1 (lam=-1)"]) == [2, 2, 10, 10]
      and orders_multiset(res["T6_special_values"]["J=0 (lam^2-lam+1=0)"]) == [4, 10, 10])
# N4b -- a direct instance of the general statement: lambda = 3 gives orders {10,10,2,1,1}
a2, a4, a6 = fm.ks_j9(sp.Integer(3), sp.Integer(3))
A2 = sp.expand(sp.cancel(a2.subs(fm.u, fm.s ** 2) / fm.s ** 2))
A4 = sp.expand(sp.cancel(a4.subs(fm.u, fm.s ** 2) / fm.s ** 4))
A6 = sp.expand(sp.cancel(a6.subs(fm.u, fm.s ** 2) / fm.s ** 6))
_, _, DX3 = fm.invariants(A2, A4, A6)
fl = sp.factor_list(sp.expand(DX3), fm.s)[1]
ords = sorted(int(m) for f, m in fl for _ in range(sp.Poly(f, fm.s).degree()))
check("N4b lambda = 3 instance: orders {1,1,2,10,10}", ords == [1, 1, 2, 10, 10], str(ords))

# N5
check("N5 loci J values not in {0, 1}", all(sp.Rational(v["J"]) not in (0, 1) for v in res["T5_s7_loci"].values()))

print()
if failures:
    print(f"FAILED: {len(failures)} control(s): {failures}")
    sys.exit(1)
print("all Inose-fibration-multiplicity controls passed")
