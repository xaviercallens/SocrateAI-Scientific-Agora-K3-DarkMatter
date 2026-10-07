#!/usr/bin/env python3
"""Controls for checkers/check_TW0_hodge_degree_orbifold.py (standing rule 1)."""
import sys
from pathlib import Path

import pytest
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from checkers import check_TW0_hodge_degree_orbifold as tw0  # noqa: E402

z = tw0.z


def test_P1_s7_four_singular_points_and_fuchs():
    scheme, n, total = tw0.riemann_scheme(tw0.OPERATORS["cooper_s7"]["P"])
    assert n == 4 and "0" in scheme          # the 07-29 brief listed three; z = 0 (MUM) is singular
    assert total == 2 and scheme["0"] == [0, 0]


def test_P2_signatures_agree_for_s7_at_level_7():
    res = tw0.analyse("cooper_s7", tw0.OPERATORS["cooper_s7"])
    assert res["signatures_agree"]
    assert res["signature_from_exponents"] == {"genus": 0, "elliptic_orders": [2, 2, 3], "cusps": 1}


def test_P3_degrees_never_two_at_family_level():
    res = tw0.analyse("cooper_s7", tw0.OPERATORS["cooper_s7"])
    d = res["degrees"]
    family_values = {sp.Rational(d["deg_omega_Q"]), sp.Rational(d["deg_omega2_Q"]),
                     sp.Rational(d["deg_ext_omega2_residues_[0,1)"]), sp.Rational(d["deg_ext_omega2_residues_(-1,0]"])}
    assert 2 not in family_values
    assert tw0.surface_reading()["ell_surface"] == 2


def test_N1_wrong_level_disagrees():
    res = tw0.analyse("cooper_s7", tw0.OPERATORS["cooper_s7"], level=5)
    assert not res["signatures_agree"]


def test_N2_wrong_operator_disagrees():
    res = tw0.analyse("cooper_s10", tw0.OPERATORS["cooper_s10"], level=7)
    assert not res["signatures_agree"]


def test_N3_irregular_singular_point_refused():
    """A coefficient perturbation that keeps the operator Fuchsian cannot break the Fuchs relation
    (it is an identity), so the honest negative control is an irregular point: raise deg P0."""
    P2, P1, P0 = tw0.OPERATORS["cooper_s7"]["P"]
    with pytest.raises(tw0.Refuse):
        tw0.riemann_scheme((P2, P1, P0 + z**3))
    scheme, _, total = tw0.riemann_scheme((P2, P1 + 3 * z, P0))   # still Fuchsian: relation holds by identity
    assert total == len(scheme) - 2


def test_N4_formula_0729_is_non_discriminating():
    s7, _, _ = tw0.riemann_scheme(tw0.OPERATORS["cooper_s7"]["P"])
    s10, _, _ = tw0.riemann_scheme(tw0.OPERATORS["cooper_s10"]["P"])
    assert tw0.formula_0729(s7) == tw0.formula_0729(s10) == 1   # Fuchs forces it for every 4-point order-2 operator


def test_N5_noether_discriminates_rational_surface():
    assert tw0.surface_reading(h01=0, h02=0)["ell_surface"] == 1   # rational elliptic surface, not K3


def test_class_numbers_counted_not_typed():
    assert tw0.class_number(-28) == 1 and tw0.class_number(-7) == 1 and tw0.class_number(-20) == 2 and tw0.class_number(-23) == 3


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
