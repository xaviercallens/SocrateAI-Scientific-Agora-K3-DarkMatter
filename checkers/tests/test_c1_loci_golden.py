"""Golden tests for check_C1_singular_loci.py (the F6-corrected C1 locus/exponent checker).

Known-good: cooper_s7_partner — loci must be the CORRECT z-space {-1, 1/27} (NOT the old
buggy index-space {1/3, 2/3}), and the Fuchs relation (sum of all exponents = #sing - 2)
must hold exactly. Regression guard: a checker whose loci ever revert to {1/3,2/3} is the bug.
"""
import sys
from pathlib import Path

import sympy as sp
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "checkers"))
import check_C1_singular_loci as chk  # noqa: E402

REFS = str(REPO / "refs" / "recurrences_v1.json")


def test_s7_partner_corrected_loci_and_fuchs():
    result, code = chk.run_check(REFS, "cooper_s7_partner")
    assert code == 0
    loci = set(sp.nsimplify(x) for x in result["finite_singular_loci_z"])
    assert loci == {sp.Integer(-1), sp.Rational(1, 27)}, result["finite_singular_loci_z"]
    # the OLD F6 bug reported index-space {1/3, 2/3}: guard against regression
    assert sp.Rational(1, 3) not in loci and sp.Rational(2, 3) not in loci
    assert result["fuchs_relation_check"]["PASS"] is True


def test_fuchs_holds_for_all_order2_partners():
    for pid in ("cooper_s7_partner", "cooper_s10_partner", "zagier_sporadic_A"):
        result, code = chk.run_check(REFS, pid)
        assert code == 0, pid
        assert result["fuchs_relation_check"]["PASS"] is True, pid


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
