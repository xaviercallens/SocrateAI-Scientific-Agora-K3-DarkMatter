"""
GAP-2 / Task T2.1: regression test recomputing the topological stiffness
integers V''(0)=1014 (S12) and V''(0)=336 (S21) from scratch, using EXACT
rational arithmetic end-to-end (no floats).

Full pipeline trace: docs/derivations/stiffness_pipeline.md. In short:
  1. mirror_map_coefficients(A,B,N) (scripts/mirror_map_integrality.py,
     already independently audited under GAP-1 task T1.3) computes the
     exact-rational mirror-map coefficients q(z)/z = sum_n coeffs[n] z^n,
     i.e. coeffs[d-1] = q_d.
  2. V''(0) := sum_{d=1}^{3} q_d * d^2  (scripts/k3_sieve_analysis.py:191,
     there computed in floating point; this test redoes it exactly).

This test asserts three things Rule 1 requires be checked, not assumed:
  (a) q_1, q_2, q_3 are genuine integers (denominator == 1) for both S12, S21
      -- a precondition for V''(0) to even be an integer;
  (b) the resulting V''(0) values match the ledger's 1014 / 336 EXACTLY;
  (c) k3_sieve_analysis.py's floating-point q_d (rounded) agree with the
      exact-rational q_d -- i.e. the float pipeline used for the sieve table
      is not silently diverging from the audited exact pipeline.
"""
import os
import sys
from fractions import Fraction as F

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

from mirror_map_integrality import mirror_map_coefficients  # noqa: E402


EXPECTED_STIFFNESS = {
    "S12": {"A": 1, "B": 2, "V_pp_0": 1014, "q123": (1, 8, 109)},
    "S21": {"A": 2, "B": 1, "V_pp_0": 336, "q123": (1, 5, 35)},
}


def exact_V_pp_0(A: int, B: int, d_max: int = 3) -> tuple[int, list[F]]:
    """Exact-rational V''(0) = sum_{d=1}^{d_max} q_d * d^2, plus the q_d used."""
    res = mirror_map_coefficients(A, B, N=d_max)
    coeffs = [F(x) for x in res["q_over_z_coefficients"]]  # coeffs[d-1] = q_d
    q = [coeffs[d - 1] for d in range(1, d_max + 1)]
    for d, qd in enumerate(q, start=1):
        assert qd.denominator == 1, (
            f"q_{d}(A={A},B={B}) = {qd} is NOT an integer -- "
            f"V''(0) is not well-defined as claimed"
        )
    V_pp_0 = sum(qd * F(d**2) for d, qd in enumerate(q, start=1))
    assert V_pp_0.denominator == 1
    return int(V_pp_0), q


class TestStiffnessExactRecomputation:
    @pytest.mark.parametrize("name", ["S12", "S21"])
    def test_q_coefficients_are_integers(self, name):
        exp = EXPECTED_STIFFNESS[name]
        _, q = exact_V_pp_0(exp["A"], exp["B"])
        assert tuple(int(x) for x in q) == exp["q123"]

    @pytest.mark.parametrize("name", ["S12", "S21"])
    def test_V_pp_0_matches_ledger(self, name):
        exp = EXPECTED_STIFFNESS[name]
        V_pp_0, _ = exact_V_pp_0(exp["A"], exp["B"])
        assert V_pp_0 == exp["V_pp_0"], (
            f"{name}: exact recomputation gives V''(0)={V_pp_0}, "
            f"but PARAMETER_LEDGER.yaml / GaugeCoupling.lean claim {exp['V_pp_0']}"
        )

    def test_stiffness_ratio_matches_kernel_verified_bounds(self):
        """Cross-check against GaugeCoupling.lean's kernel-verified bounds:
        1.73 < sqrt(1014/336) < 1.75."""
        v12, _ = exact_V_pp_0(1, 2)
        v21, _ = exact_V_pp_0(2, 1)
        ratio = F(v12, v21)
        assert F(173, 100) ** 2 < ratio < F(175, 100) ** 2

    def test_float_pipeline_agrees_with_exact_pipeline(self):
        """scripts/k3_sieve_analysis.py computes q_d in floating point and
        rounds; verify that rounding actually recovers the exact integers
        (i.e. the float pipeline is not silently wrong)."""
        sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
        from k3_sieve_analysis import get_u_v, get_mirror_map

        for name, exp in EXPECTED_STIFFNESS.items():
            u, v = get_u_v(exp["A"], exp["B"], n_max=22)
            q_float = get_mirror_map(u, v, d_max=5)
            q_int_float = tuple(int(round(x)) for x in q_float[1:4])
            assert q_int_float == exp["q123"], (
                f"{name}: float pipeline rounds to {q_int_float}, "
                f"exact pipeline gives {exp['q123']}"
            )
