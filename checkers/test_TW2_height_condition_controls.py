#!/usr/bin/env python3
"""Controls for checkers/check_TW2_height_condition.py (standing rule 1)."""
import sys
from fractions import Fraction as Fr
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from checkers import check_TW2_height_condition as tw2  # noqa: E402


def test_P1_e8_data_computed_from_cartan_matrix():
    assert tw2.FIBRE_TYPES["E8"]["root_rank"] == 8 and tw2.FIBRE_TYPES["E8"]["root_det"] == 1


def test_P2_n7_forces_P_dot_O_5_and_n10_forces_8():
    assert tw2.height_condition(7)["P_dot_O"] == 5 and tw2.height_condition(7)["height_h_P"] == 14
    assert tw2.height_condition(10)["P_dot_O"] == 8 and tw2.height_condition(10)["height_h_P"] == 20


def test_P3_shioda_tate_rank_bookkeeping():
    r = tw2.height_condition(7)
    assert r["trivial_lattice_rank"] == 18 and r["mordell_weil_rank"] == 1 and r["disc_trivial_lattice"] == -1


def test_N1_one_e8_fibre_is_not_M_n_shape():
    r = tw2.height_condition(7, fibres=("E8",))
    assert r["mordell_weil_rank"] == 9 and r["ns_is_M_n_shape"] is False


def test_N2_wrong_chi_changes_the_answer():
    assert tw2.height_condition(7, chi=1)["P_dot_O"] == 6   # rational elliptic surface value, not the K3 one


def test_N3_e7_plus_e8_is_not_M_n_shape():
    r = tw2.height_condition(7, fibres=("E7", "E8"), rho=18)
    assert r["ns_is_M_n_shape"] is False


def test_N4_nonzero_correction_term_refused_when_parity_breaks():
    # a hypothetical non-identity contact with correction 3/2 makes 2 P.O non-integral: must refuse, not round
    tw2.FIBRE_TYPES["E7test"] = {"root_rank": 7, "root_det": 2, "simple_components": 2, "nonidentity_contr": Fr(3, 2)}
    try:
        with pytest.raises(tw2.Refuse):
            tw2.height_condition(7, meets_nonidentity=("E7test",))
    finally:
        del tw2.FIBRE_TYPES["E7test"]


def test_N5_rho_below_trivial_rank_refused():
    with pytest.raises(tw2.Refuse):
        tw2.height_condition(7, rho=17)


def test_P4_explicit_M7_model_has_two_order_10_roots_at_each_locus():
    counts = tw2.e8_fibre_count_from_inose_certificate()
    if counts is None:
        pytest.skip("INOSE_FIBRATION_MULTIPLICITIES.json absent")
    assert set(counts.values()) == {2}


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
