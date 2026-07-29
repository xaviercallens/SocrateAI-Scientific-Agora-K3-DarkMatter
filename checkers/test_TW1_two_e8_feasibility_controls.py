#!/usr/bin/env python3
"""
test_TW1_two_e8_feasibility_controls.py — mandatory controls for
check_TW1_two_e8_feasibility.py (WP-TW1; S2 CLAUDE.md standing rule 1:
"a test that cannot fail is not a test — every headline-number checker
ships a negative control").

Controls (plan step 4: >=1 positive, >=2 negative):
  1. POSITIVE: the disjoint-section P^1xP^2 configuration (a special case
     n=0 of the P^1-bundle-over-P^2 ladder) must PASS -- the classically
     expected heterotic/F-theory E8xE8-dual geometry. Proves the checker
     is not a stub that always returns FAIL.
  2. NEGATIVE (shrunk bound): artificially shrinking -4K_{P1xP2}'s
     h1-component from 8 to 7 must FLIP the same disjoint two-E8
     configuration from PASS to FAIL.
  3. NEGATIVE (three E8): three mutually-disjoint E8 divisors on P^1xP^2
     (same construction as the two-E8 PASS, one more point-fiber) must
     FAIL on the f-budget (need 12 > bound 8) -- proves the checker
     correctly tightens as E8-count increases, per plan step 4's
     "three E8's where two barely fit" requirement.
  4. P^3 MUST FAIL (re-assertion, headline finding): re-run independently
     of __main__ and confirm the collision-forced non-minimality verdict.
  5. MALFORMED INPUT REJECTED: budget_chain() with mismatched
     need/bound/labels lengths must be rejected loudly, not silently
     produce a wrong-length result.

Run:  python3 checkers/test_TW1_two_e8_feasibility_controls.py

Generated-by: Sonnet 5 (Stream 2, WP-TW1 session 2026-07-29)
Verified-by: this file IS the verifier for check_TW1_two_e8_feasibility.py
Reviewed-by: pending T0 (Xavier)
"""

import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_TW1_two_e8_feasibility as TW1  # noqa: E402


def control_positive_disjoint_p1xp2():
    r = TW1.control_positive_disjoint_pass()
    assert r["overall_verdict"] == "PASS", \
        f"positive control FAILED: expected PASS, got {r['overall_verdict']}"
    print("  [control] disjoint P^1xP^2 (two E8): PASS (checker responds to "
          "input, is not a stub)")
    return True


def control_negative_shrunk_bound():
    result = TW1.control_negative_shrunk_bound()
    assert not result["all_components_pass"], \
        f"negative control (shrunk bound) FAILED TO FAIL: {result}"
    print("  [control] shrunk -4K bound flips PASS->FAIL: PASS "
          f"({result['chain']})")
    return True


def control_negative_three_e8():
    result = TW1.control_negative_three_e8()
    assert not result["all_components_pass"], \
        f"negative control (three E8) FAILED TO FAIL: {result}"
    print("  [control] three-E8 on P^1xP^2 correctly exceeds f-budget: PASS "
          f"({result['chain']})")
    return True


def control_p3_must_fail():
    r = TW1.run_P3()
    assert r["overall_verdict"] == "FAIL", \
        f"P^3 headline control FAILED: expected FAIL, got {r['overall_verdict']}"
    assert r["collision_analysis"]["collision_unavoidable_for_every_d1_d2"] is True
    assert r["collision_analysis"]["non_minimality_test_4_6_curse"] is True
    assert r["collision_analysis"]["non_minimality_test_discriminant_order_ge_12"] is True
    print("  [control] P^3 collision-forced non-minimality re-confirmed: PASS")
    return True


def control_malformed_input_rejected():
    try:
        TW1.budget_chain((1, 2), (1,), ("a", "b"))  # length mismatch
    except TW1.ControlFailure as e:
        print(f"  [control] malformed budget_chain input rejected loudly: PASS\n            ({e})")
        return True
    raise TW1.ControlFailure("malformed-input control FAILED: budget_chain() "
                              "accepted mismatched need/bound/labels without complaint")


def main():
    print("=" * 78)
    print("test_TW1_two_e8_feasibility_controls.py")
    print("=" * 78)
    controls = [
        ("positive: disjoint P^1xP^2 two-E8 PASSes", control_positive_disjoint_p1xp2),
        ("negative: shrunk bound flips PASS->FAIL", control_negative_shrunk_bound),
        ("negative: three E8 exceeds f-budget", control_negative_three_e8),
        ("P^3 headline result: collision-forced FAIL", control_p3_must_fail),
        ("malformed budget_chain input rejected", control_malformed_input_rejected),
    ]
    worst = 0
    for name, fn in controls:
        print(f"\n--- {name} ---")
        try:
            fn()
        except (TW1.ControlFailure, AssertionError) as e:
            print(f"FAIL: {name}: {e}", file=sys.stderr)
            worst = 3
    print()
    if worst == 0:
        print("ALL CONTROLS PASSED")
    return worst


if __name__ == "__main__":
    sys.exit(main())
