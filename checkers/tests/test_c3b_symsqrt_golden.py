"""Golden tests for check_C3b_symsqrt.py.

Contract (criteria-checkers skill): one known-good control that must PASS, one known-bad
control that must FAIL by design. Here the known-bad is an order-2 sequence fed as the bulk:
its series square root is NOT order-2 holonomic, so the checker must refuse to invent a partner.
"""
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "checkers"))
import check_C3b_symsqrt as chk  # noqa: E402

REFS = str(REPO / "refs" / "recurrences_v1.json")


def test_known_good_s7_extracts_partner():
    """cooper_s7 IS a symmetric square; partner = A279619 (1,2,22,336,6006,...)."""
    result, code = chk.run_check(REFS, "cooper_s7", n_fit=26, n_val=60)
    assert code == 0
    assert result["verdict"].startswith("SYM2_PARTNER_EXTRACTED")
    assert result["validation"]["partner_MUM"] is True
    assert result["validation"]["mirror_map_z_L2_eq_z_L3"] is True
    # Partner sequence is the exact integer sequence (falsifiable literal).
    assert result["partner_L2"]["first_terms"][:6] == ["1", "2", "22", "336", "6006", "117348"]
    assert result["partner_L2"]["partner_is_integral"] is True


def test_known_good_s10_extracts_partner():
    result, code = chk.run_check(REFS, "cooper_s10", n_fit=26, n_val=60)
    assert code == 0
    assert result["verdict"].startswith("SYM2_PARTNER_EXTRACTED")
    assert result["validation"]["mirror_map_z_L2_eq_z_L3"] is True


def test_known_bad_order2_bulk_is_rejected():
    """apery_zeta2 is order-3-typed? No — it is order-2. Feeding an order-2 sequence's data as a
    bulk must be refused up front; and even the underlying sqrt-holonomic test must not fire.
    We assert the checker does not fabricate a partner."""
    # apery_zeta2 is registered order-2, so the bulk-type guard must reject it.
    result, code = chk.run_check(REFS, "apery_zeta2", n_fit=26, n_val=60)
    assert code != 0
    assert result["verdict"] == "ERROR_BULK_NOT_ORDER3"


def test_known_bad_generic_order3_not_symsquare(tmp_path):
    """PRIMARY known-bad control: a generic order-3 MUM sequence (s7 with its first term
    perturbed 4→5, i.e. the a1 recurrence coefficient 90→91) is NOT a symmetric square —
    its series square root is not order-2 holonomic at any tested degree. Must return
    NOT_SYMMETRIC_SQUARE. This proves the order-2-holonomic property is non-trivial (the
    checker is not vacuously certifying every MUM sequence)."""
    import json
    refs = json.loads(Path(REFS).read_text())
    refs["sequences"]["_test_generic_pert"] = {
        "type": "order-3",
        "status": "OK",
        "source": "TEST-ONLY perturbation of cooper_s7 (a1 coeff 90->91); generic non-Sym^2 control.",
        "initial_terms": [1, 4],
        "recurrence_python": ("((91+177*(k-1)+117*(k-1)**2+26*(k-1)**3)*s[-1] + "
                              "(24+78*(k-1)+81*(k-1)**2+27*(k-1)**3)*s[-2])/"
                              "((8+12*(k-1)+6*(k-1)**2+(k-1)**3))"),
    }
    p = tmp_path / "refs_test.json"
    p.write_text(json.dumps(refs))
    result, code = chk.run_check(str(p), "_test_generic_pert", n_fit=30, n_val=60)
    assert code != 0
    assert result["verdict"] == "NOT_SYMMETRIC_SQUARE"


def test_known_bad_non_mum_symsquare_rejected(tmp_path):
    """SECONDARY control (MUM gate): Apéry ζ(3) (A005259). Its series square root IS order-2
    holonomic, but with C(n) = -4(n+1)^2 (constant 4 ≠ 1) — a symmetric square of a NON-MUM
    order-2 operator. It has no matching elliptic mirror map, so the checker must refuse to
    certify it as an elliptic partner: verdict FAIL_PARTNER_VALIDATION (partner_MUM False)."""
    import json
    refs = json.loads(Path(REFS).read_text())
    refs["sequences"]["_test_apery_zeta3"] = {
        "type": "order-3",
        "status": "OK",
        "source": "TEST-ONLY A005259 Apéry ζ(3); Sym^2 of a non-MUM operator (control).",
        "initial_terms": [1, 5],
        "recurrence_python": ("((34*k**3+51*k**2+27*k+5)*s[-1] - (k)**3*s[-2])/((k+1)**3)"),
    }
    p = tmp_path / "refs_test.json"
    p.write_text(json.dumps(refs))
    result, code = chk.run_check(str(p), "_test_apery_zeta3", n_fit=30, n_val=60)
    assert code != 0
    assert result["verdict"] == "FAIL_PARTNER_VALIDATION"
    assert result["validation"]["partner_MUM"] is False


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
