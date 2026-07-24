"""Golden tests for check_min_ode_order.py (criteria-checkers contract).

Known-good: apery_zeta2 (Apery zeta(2), refs-frozen order-2 elliptic operator)
  -> minimal ODE order MUST be 2 (order 1 excluded inside the box).
Known-bad control: cooper_s7 (order-3 K3 bulk)
  -> checker MUST NOT certify order <= 2; minimal ODE order MUST be 3.
A checker that has never refused order-2 for a genuine K3 is untested.
"""
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "checkers"))
import check_min_ode_order as chk  # noqa: E402

REFS = str(REPO / "refs" / "recurrences_v1.json")


def test_known_good_apery_zeta2_is_order2():
    result, code = chk.run_check("refs", REFS, "apery_zeta2", n_terms=45)
    assert code == 0
    assert result["min_ode"]["order"] == 2, result["verdict"]


def test_known_bad_cooper_s7_not_order2():
    result, code = chk.run_check("refs", REFS, "cooper_s7", n_terms=45)
    assert code == 0
    # The control: a genuine K3 bulk must NOT admit an order<=2 annihilator.
    assert result["min_ode"]["order"] == 3, result["verdict"]


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
