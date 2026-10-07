#!/usr/bin/env python3
"""Controls for checkers/check_TW2_rho20_loci.py (standing rule 1)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from checkers import check_TW2_rho20_loci as t  # noqa: E402

ORD2 = {"s=+1": 10, "s=-1": 10, "s=0": 2, "roots_of_e(s^2)": [1, 1], "s=infinity": 0}
ORD4 = {"s": 4, "s - 1": 10, "s + 1": 10, "s=infinity": 0}
GEN = {"s=+1": 10, "s=-1": 10, "roots": [1, 1, 1, 1], "s=infinity": 0}


def test_P1_data_driven_results_from_certificates():
    loci, d0 = t.load_inputs()
    r1 = t.analyse_locus("-1", loci["-1"]["abc"], loci["-1"]["orders"])
    r2 = t.analyse_locus("1/27", loci["1/27"]["abc"], loci["1/27"]["orders"])
    r3 = t.analyse_locus("infinity", loci["infinity"]["abc"], loci["infinity"]["orders"])
    assert r1["abs_disc_T"] == 7 and r1["resolution"]["mordell_weil_rank"] == 1
    assert r1["resolution"]["height"] == "7/2" and r1["resolution"]["P_dot_O_solutions"] == [{"contr": "1/2", "P_dot_O": 0}]
    assert r2["abs_disc_T"] == 28 and r2["resolution"]["height"] == "14" and r2["resolution"]["P_dot_O_solutions"] == [{"contr": "0", "P_dot_O": 5}]
    assert r3["abs_disc_T"] == 3 and r3["resolution"]["mordell_weil_rank"] == 0 and r3["resolution"]["root_lattice"] == "A2"


def test_N1_swapping_T_forms_swaps_the_answers():
    r = t.analyse_locus("x", (1, 0, 7), ORD2)          # disc 28 with an A1 root
    assert r["resolution"]["P_dot_O_solutions"][0]["P_dot_O"] == 5
    r = t.analyse_locus("x", (1, 1, 2), ORD2)          # disc 7 with an A1 root
    assert r["resolution"]["P_dot_O_solutions"][0]["P_dot_O"] == 0


def test_N2_rho19_at_a_rho20_locus_refused():
    with pytest.raises(t.Refuse):
        t.analyse_locus("x", (1, 0, 7), ORD2, rho=19)     # rank-2 T is incompatible with rho = 19 bookkeeping here


def test_N3_disc_too_small_for_an_A1_fibre_refused():
    with pytest.raises(t.Refuse):
        t.analyse_locus("x", (1, 1, 1), ORD2)          # |disc T| = 3 with an A1 root: h = 3/2 < 2chi - 1/2, no P.O >= 0
    # and a disc that DOES admit a non-identity contact is accepted with the half-integral height (not a tautology)
    r = t.analyse_locus("x", (1, 1, 3), ORD2)          # |disc T| = 11: h = 11/2, contr 1/2, P.O = 1
    assert r["resolution"]["P_dot_O_solutions"] == [{"contr": "1/2", "P_dot_O": 1}]


def test_N4_order4_root_with_disc_not_3_refused():
    with pytest.raises(t.Refuse):
        t.analyse_locus("x", (1, 0, 1), ORD4)          # |disc T| = 4 vs A2 (det 3): inconsistent, and A3 gives rank MW < 0


def test_N5_additive_reading_of_the_order2_root_changes_everything():
    r = t.analyse_locus("x", (1, 0, 7), ORD2, d0_is_simple_root=False)   # rank-0 root: MW rank 2
    assert r["resolution"]["mordell_weil_rank"] == 2


def test_N6_three_order10_roots_refused():
    with pytest.raises(t.Refuse):
        t.extra_root_orders({"a": 10, "b": 10, "c": 10})


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
