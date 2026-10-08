#!/usr/bin/env python3
"""test_K3xT2_reading_S_controls.py -- controls for checkers/check_K3xT2_reading_S.py (standing rule 1: each must be able to fail).

  P1  both families: T(E x E') for the cyclic n-isogeny is isometric to the certified Gram (the positive result)
  N1  wrong level: n = 5 against the cooper_s7 Gram (U + <14>) finds no isometry
  N2  non-cyclic isogeny M = 2*I (degree 4, kernel (Z/2)^2): NS = <A, B, Gamma> is NOT saturated, caught before any comparison
  N3  orientation: det M = -n gives NS signature (2,1), not (1,2) -- caught by the exact signature check
  N4  tampered certified Gram (2n -> 2n + 2): no isometry
  N5  wrong CM order at z = 1/27 (D = -7 instead of the computed -28): T(E x E) differs from the certified row
  N6  the j -> D identification is not vacuous: a j that is not a class-number-one j-invariant matches no order
  N7  the class-number-one enumeration (computed) is exactly the 13 Heegner-Stark discriminants -- a fixed point the code must hit
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_K3xT2_reading_S as k  # noqa: E402

fails = []


def check(name, cond, detail=""):
    print(f"  {'ok  ' if cond else 'FAIL'} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        fails.append(name)


U14 = [[0, 0, -1], [0, 14, 0], [-1, 0, 0]]
res = k.run()
check("P1 both families isometric to certified T", res["all_generic_isometric"], str({f: v["verdict"] for f, v in res["generic"].items()}))
check("P1b s7 rho=20 points agree (forced consistency)", res["all_rho20_agree"])

r = k.generic_check(5, U14, [2, 1])
check("N1 n = 5 against U+<14>: no isometry", r["verdict"] == "FAIL_NO_ISOMETRY_TO_CERTIFIED_GRAM", r["verdict"])

r = k.generic_check(4, [[0, 0, -1], [0, 8, 0], [-1, 0, 0]], [2, 1], M=[[2, 0], [0, 2]])
check("N2 non-cyclic M = 2I: NS not saturated", r["verdict"].startswith("FAIL_NS_NOT_SATURATED"), r["verdict"])

r = k.generic_check(7, U14, [2, 1], M=[[1, 0], [0, -7]])
check("N3 det M = -7: NS signature wrong", r["verdict"] == "FAIL_NS_SIGNATURE", r["verdict"])

r = k.generic_check(7, [[0, 0, -1], [0, 16, 0], [-1, 0, 0]], [2, 1])
check("N4 tampered Gram 14 -> 16: no isometry", r["verdict"] == "FAIL_NO_ISOMETRY_TO_CERTIFIED_GRAM", r["verdict"])

t = k.T_of_ExE(-7)
check("N5 wrong order D=-7 at z=1/27 disagrees with certified [1,0,7]", t["T_reduced_abc"] != [1, 0, 7], str(t["T_reduced_abc"]))

check("N6 j = 1000 (not a class-number-one j) matches no order", k.order_for_j(1000) == [])

check("N7 class-number-one list is the 13 Heegner-Stark discriminants",
      k.class_number_one(200) == [-3, -4, -7, -8, -11, -12, -16, -19, -27, -28, -43, -67, -163])

print()
if fails:
    print(f"FAILED: {fails}")
    sys.exit(1)
print("all K3xT2 reading-S controls behaved as required")
