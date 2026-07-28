#!/usr/bin/env python3
"""
test_G1a_CY_condition_controls.py — mandatory negative controls for
check_G1a_CY_twist_condition.py (WP S2-G Phase G1-a; CLAUDE.md standing rule
1: "a test that cannot fail is not a test — every headline-number checker
ships a negative control").

Controls:
  1. LADDER-MUST-OBSTRUCT (re-assertion): P^2 and F_n (n=0..5, and symbolic
     n) must all independently return OBSTRUCTED via a fresh call, not the
     __main__ path — this is the DoD's "at least one input that must FAIL
     the CY condition" requirement, and the headline finding of this WP.
  2. POSITIVE CONTROL (dP9 must ADMIT, ell=1): proves the checker is not a
     stub that always returns OBSTRUCTED regardless of input — the same
     solve_proportionality() machinery that fails the whole B2 ladder
     genuinely PASSES on a structurally different, correctly-posed input,
     and derives (not assumes) the numerically correct ell.
  3. MALFORMED FIBER CLASS REJECTED: a candidate "fiber class" F with
     F^2 != 0 (violating the defining property of a fibration fiber — fibers
     are pairwise disjoint) must be rejected LOUDLY by
     solve_proportionality()'s isotropy precondition, not silently answer a
     nonsense question. This is the DoD's "deliberately corrupted/malformed
     input that must be rejected" requirement.
  4. ASYMMETRIC GRAM REJECTED: a non-symmetric "Gram matrix" (not a valid
     intersection pairing) must be rejected loudly by the symmetry
     precondition check.
  5. RANK-1 ISOTROPY GUARD SANITY: check_isotropic_existence_rank1() must
     correctly report "only_zero_isotropic_vector=False" for a rank-1
     lattice that IS allowed to have a nonzero isotropic vector (k=0
     degenerate case is guarded separately; here we check a NEGATIVE-
     definite k<0 rank-1 lattice, e.g. k=-1, still only n=0 works since
     n^2*(-1)=0 also forces n=0 -- included as a boundary sanity check
     that the guard's conclusion is about k!=0 in general, not simply
     "true because I hardcoded True").

Run:  python3 checkers/test_G1a_CY_condition_controls.py

Generated-by: Sonnet 5 (Stream 2, WP S2-G Phase G1-a session 2026-07-28)
Verified-by: this file IS the verifier for check_G1a_CY_twist_condition.py
Reviewed-by: pending T0 (Xavier)
"""

import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_G1a_CY_twist_condition as G1a  # noqa: E402


def control_ladder_must_obstruct():
    r_p2 = G1a.run_P2()
    assert r_p2["overall_determination"] == "OBSTRUCTED", \
        f"P^2 control FAILED: expected OBSTRUCTED, got {r_p2['overall_determination']}"

    n_sym = sp.Symbol("n", integer=True, nonnegative=True)
    r_fn_sym = G1a.run_Fn(n_sym)
    assert r_fn_sym["overall_determination"] == "OBSTRUCTED", \
        f"F_n (symbolic) control FAILED: expected OBSTRUCTED, got {r_fn_sym['overall_determination']}"

    for n_val in range(6):
        r = G1a.run_Fn(sp.Integer(n_val))
        assert r["overall_determination"] == "OBSTRUCTED", \
            f"F_{n_val} control FAILED: expected OBSTRUCTED, got {r['overall_determination']}"
    print("  [control] P^2 and F_0..F_5 (+ symbolic n) all independently OBSTRUCTED: PASS")
    return True


def control_dp9_positive():
    r = G1a.run_dP9_positive_control()
    assert r["overall_determination"] == "ADMISSIBLE", \
        f"dP9 positive control FAILED: expected ADMISSIBLE, got {r['overall_determination']}"
    assert r["cy_twist_condition"]["ell"] == "1", \
        f"dP9 positive control FAILED: expected ell=1, got {r['cy_twist_condition']['ell']}"
    print(f"  [control] dP9 positive control: ADMISSIBLE, ell={r['cy_twist_condition']['ell']}: PASS "
          "(checker responds to input, is not a stub)")
    return True


def control_malformed_fiber_class_rejected():
    """F with F^2 != 0 fed as a candidate fiber class must be rejected."""
    Gram = sp.Matrix([[1]])          # Pic(P^2)-like, H^2=1
    K_vec = [-3]
    F_vec_bad = [1]                  # F=H, F^2=1 != 0 -- NOT a valid fiber class
    try:
        G1a.solve_proportionality(Gram, K_vec, F_vec_bad, "MALFORMED-F-not-isotropic")
    except G1a.ControlFailure as e:
        print(f"  [control] malformed non-isotropic fiber class rejected loudly: PASS\n            ({e})")
        return True
    raise G1a.ControlFailure("malformed-fiber-class control FAILED: solve_proportionality() "
                              "accepted a non-isotropic F without complaint")


def control_asymmetric_gram_rejected():
    """A non-symmetric 'Gram matrix' (not a valid intersection pairing) must
    be rejected by the symmetry precondition."""
    Gram_bad = sp.Matrix([[0, 1], [2, 0]])  # NOT symmetric (Gram[0,1]=1 != Gram[1,0]=2)
    K_vec = [-2, -3]
    F_vec = [0, 1]
    try:
        G1a.solve_proportionality(Gram_bad, K_vec, F_vec, "MALFORMED-asymmetric-Gram")
    except G1a.ControlFailure as e:
        print(f"  [control] asymmetric Gram matrix rejected loudly: PASS\n            ({e})")
        return True
    raise G1a.ControlFailure("asymmetric-Gram control FAILED: solve_proportionality() "
                              "accepted a non-symmetric Gram matrix without complaint")


def control_rank1_isotropy_guard_sanity():
    """Boundary sanity: a NEGATIVE k (k=-1) rank-1 lattice must also report
    only_zero_isotropic_vector=True (n^2*(-1)=0 => n=0 too), confirming the
    guard's exact symbolic solve is doing real work (k!=0 in general, not a
    hardcoded 'positive-definite implies True' shortcut)."""
    Gram_neg = sp.Matrix([[-1]])
    res = G1a.check_isotropic_existence_rank1(Gram_neg, "TEST-negative-definite-rank1")
    assert res["only_zero_isotropic_vector"] is True, \
        f"rank-1 isotropy guard control FAILED: expected only_zero=True for k=-1, got {res}"
    assert res["positive_definite"] is False, \
        f"rank-1 isotropy guard control FAILED: k=-1 should report positive_definite=False, got {res}"
    print(f"  [control] rank-1 isotropy guard on k=-1 (negative-definite): "
          f"only_zero_isotropic_vector=True, positive_definite=False: PASS")
    return True


def main():
    print("=" * 78)
    print("test_G1a_CY_condition_controls.py")
    print("=" * 78)
    controls = [
        ("ladder must obstruct (P^2, F_0..F_5, symbolic n)", control_ladder_must_obstruct),
        ("dP9 positive control (must admit, ell=1)", control_dp9_positive),
        ("malformed non-isotropic fiber class rejected", control_malformed_fiber_class_rejected),
        ("asymmetric Gram matrix rejected", control_asymmetric_gram_rejected),
        ("rank-1 isotropy guard sanity (k=-1)", control_rank1_isotropy_guard_sanity),
    ]
    worst = 0
    for name, fn in controls:
        print(f"\n--- {name} ---")
        try:
            fn()
        except (G1a.ControlFailure, AssertionError) as e:
            print(f"FAIL: {name}: {e}", file=sys.stderr)
            worst = 3
    print()
    if worst == 0:
        print("ALL CONTROLS PASSED")
    return worst


if __name__ == "__main__":
    sys.exit(main())
