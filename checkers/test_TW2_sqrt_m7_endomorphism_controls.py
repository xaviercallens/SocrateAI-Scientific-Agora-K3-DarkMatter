#!/usr/bin/env python3
"""Controls for checkers/check_TW2_sqrt_m7_endomorphism.py (standing rule 1)."""
import random
import sys
from pathlib import Path

import pytest
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from checkers import check_TW2_sqrt_m7_endomorphism as e  # noqa: E402

x = e.x


@pytest.fixture(scope="module")
def setup():
    j = e.read_j()
    A, B = e.model_from_j(j)
    psi = e.division_polys(8, A, B)
    h = e.kernel_cubic(psi[7])
    phi_x, (A2, B2) = e.velu(A, B, h)
    return j, A, B, psi, h, phi_x, A2, B2


def _compose_check(phi_x, c2, psi, A, B, mult, n=30):
    num, den = sp.fraction(phi_x)
    pm = sp.expand(sp.expand(psi[mult - 1] * psi[mult + 1]).subs(e.y ** 2, x ** 3 + A * x + B))
    rng = random.Random(3); ok = tried = 0
    for _ in range(n):
        x0 = sp.Rational(rng.randint(-10 ** 5, 10 ** 5), rng.randint(1, 100))
        try:
            v1 = c2 * num.subs(x, x0) / den.subs(x, x0); v2 = c2 * num.subs(x, v1) / den.subs(x, v1)
            rhs = x0 - pm.subs(x, x0) / psi[mult].subs(x, x0) ** 2
            tried += 1; ok += int(sp.simplify(v2 - rhs) == 0)
        except ZeroDivisionError:
            pass
    return ok, tried


def test_P1_full_run_passes(setup):
    r = e.run(n_points=55)
    assert r["composition_phi_phi_equals_minus7"]["is_identity"] and r["phi_x"]["degrees"] == [7, 6]


def test_P2_j_is_read_not_typed(setup):
    j = setup[0]
    assert j == sp.Integer(16581375) and str(j) == str(e.read_j())


def test_N1_wrong_sign_of_isomorphism_constant_fails(setup):
    j, A, B, psi, h, phi_x, A2, B2 = setup
    c2 = e.iso_constant(A, B, A2, B2)
    ok, tried = _compose_check(phi_x, -c2, psi, A, B, 7, n=12)
    assert tried and ok == 0


def test_N2_wrong_multiplier_fails(setup):
    j, A, B, psi, h, phi_x, A2, B2 = setup
    c2 = e.iso_constant(A, B, A2, B2)
    psi5 = e.division_polys(6, A, B)
    ok, tried = _compose_check(phi_x, c2, psi5, A, B, 5, n=12)
    assert tried and ok == 0


def test_N3_random_cubic_is_not_a_kernel(setup):
    j, A, B, psi, h, phi_x, A2, B2 = setup
    hbad = sp.Poly(x ** 3 + 3 * x + 11, x)
    phi_bad, (A3, B3) = e.velu(A, B, hbad)
    j3 = sp.Rational(1728 * 4 * A3 ** 3, 4 * A3 ** 3 + 27 * B3 ** 2)
    assert j3 != j                                    # codomain not even isomorphic to E


def test_N4_non_CM_curve_has_no_rational_7_kernel():
    # y^2 = x^3 - x + 1 has j = 1728 * 4 * (-1)^3 / (4*(-1)^3 + 27) = -6912/23: no CM, no rational 7-isogeny
    A, B = sp.Integer(-1), sp.Integer(1)
    psi = e.division_polys(8, A, B)
    with pytest.raises(e.Refuse):
        e.kernel_cubic(psi[7])


def test_N5_j_0_or_1728_refused():
    with pytest.raises(e.Refuse):
        e.model_from_j(sp.Integer(0))


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
