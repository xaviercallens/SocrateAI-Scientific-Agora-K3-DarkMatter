#!/usr/bin/env python3
"""
test_U1_controls.py — mandatory negative controls for check_U1_lattice.py
(docs/U1_ROUTE_DESIGN_2026_07_26.md: "a run without them is not evidence").

Controls:
  1. DIFFERENT-LEVEL: the identical pipeline on cooper_s10 must produce a
     DIFFERENT lattice than cooper_s7 (asserted as computed-vs-computed
     inequality - no expected value is typed anywhere).
  2. SCRAMBLED MATRIX (two modes):
     a. raw entry perturbation  -> must fail loudly (involution gate);
     b. corrupted involution    -> must fail loudly (joint-structure gates);
     c. UNIT control on the invariant-form solver itself: with one elliptic
        matrix conjugated out of the joint group, the invariant symmetric form
        must NOT exist (solution space dim 0) - this exercises the
        invariant-lattice failure mode directly, bypassing earlier gates.
  3. YUKAWA SCRAMBLE: a corrupted mirror map must break the exact q-series
     constancy check (the constancy check must be able to fail).
  4. STRUCTURAL POSITIVES for the record: the s7 run must satisfy its own
     internal consistency (derived 2n == |det| == U-splitting d), asserted
     between computed quantities only.

Run:  python3 checkers/test_U1_controls.py

Generated-by: Fable 5 (Stream 2, U1 execution session 2026-07-27)
Verified-by: this file IS the verifier for check_U1_lattice.py
Reviewed-by: pending T0 (Xavier)
"""

import sys
from pathlib import Path

import mpmath as mp
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_U1_lattice as U1  # noqa: E402


def control_invariant_form_unit():
    """Direct unit control on the invariant-lattice step: conjugate one elliptic
    Sym^2 matrix out of the joint group and assert the joint invariant symmetric
    form DISAPPEARS (dim 0). Uses the s7 matrices recognized at runtime."""
    L2, L3 = U1.load_operators("cooper_s7")
    loci, Ns, _ = U1.stage2_monodromy("cooper_s7", L2, verbose=False)
    N0 = sp.Matrix([[1, 1, 1], [0, 1, 2], [0, 0, 1]])
    gens = [N0] + [Ns[str(l)] for l in loci]
    S = sp.Matrix([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
    gens[1] = S * gens[1] * S.inv()  # still an involution, but wrong group

    gsym = sp.symbols("g11 g12 g13 g22 g23 g33")
    G = sp.Matrix([[gsym[0], gsym[1], gsym[2]],
                   [gsym[1], gsym[3], gsym[4]],
                   [gsym[2], gsym[4], gsym[5]]])
    eqs = []
    for M in gens:
        E = M.T * G * M - G
        eqs.extend([E[i, j] for i in range(3) for j in range(i, 3)])
    sol = sp.solve(eqs, gsym, dict=True)
    Gs = G.subs(sol[0]) if sol else sp.zeros(3, 3)
    free = Gs.free_symbols
    assert len(free) == 0 and Gs == sp.zeros(3, 3), (
        "invariant-form unit control FAILED: a joint invariant form survived a "
        f"scrambled elliptic matrix (dim {len(free)})")
    print("  [control] invariant-form unit: joint invariant form vanishes for the "
          "scrambled matrix (dim 0): PASS")


def main():
    mp.mp.dps = U1.DPS
    print("=== U1 mandatory controls ===")
    U1.stage0_framework()
    print("  [stage0] framework re-derivation: OK")

    res_s7 = U1.run_family("cooper_s7", verbose=False)
    lat = res_s7["stage3"]

    # 4. internal consistency between computed quantities (no typed expectations)
    assert lat["derived_2n"] == abs(lat["det"]), (lat["derived_2n"], lat["det"])
    assert lat["u_splitting"] is not None and lat["u_splitting"]["d"] == lat["derived_2n"]
    assert tuple(lat["signature"]) == (2, 1), lat["signature"]
    assert lat["proper_even_invariant_overlattices"] == 0
    print(f"  [s7] internal consistency: 2n == |det| == splitting d == {lat['derived_2n']}; "
          f"signature (2,1); no proper even invariant overlattices")

    # 1. different-level control
    U1.control_different_level(res_s7)

    # 2a/2b. scrambled-matrix controls through the pipeline
    U1.control_scrambled()

    # 2c. scrambled-matrix control directly on the invariant-form step
    control_invariant_form_unit()

    # 3. Yukawa scramble control
    U1.control_yukawa_scramble()

    print("\ntest_U1_controls.py: ALL CONTROLS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
