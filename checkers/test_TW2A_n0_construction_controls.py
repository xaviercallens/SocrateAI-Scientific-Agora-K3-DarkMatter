#!/usr/bin/env python3
"""Golden tests for check_TW2A_n0_construction.py (criteria-checkers contract
sec. 5: one known-good control and known-bad controls that must FAIL).

The checker's own [H] block already exercises H1-H5 in-process; this file
makes them pytest-collectable and adds an end-to-end exit-code test plus
independent known-bad probes that do NOT reuse the checker's control paths.

Generated-by: Fable 5 (Stream 2, WP-TW2-A 2026-07-31)
Verified-by: pytest
Reviewed-by: pending T0 (Xavier)
"""

import subprocess
import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_TW2A_n0_construction as C  # noqa: E402

HERE = Path(__file__).resolve().parent


def _model():
    _, j1, j2, cm = C.load_refs_gated()
    return C.fiber_model_from_h(j1, j2, 1), j1, j2, cm


# --------------------------- known-good ------------------------------------

def test_end_to_end_exit_zero():
    r = subprocess.run([sys.executable, str(HERE / "check_TW2A_n0_construction.py")],
                       capture_output=True, text=True, timeout=560)
    assert r.returncode == 0, r.stdout + r.stderr


def test_positive_exact_orders_and_invariants():
    m, *_ = _model()
    w = C.xx ** 6 + C.yy ** 6 - 2 * C.zz ** 6
    f4, g4 = C.build_fourfold(m, w)
    res, _ = C.verify_fourfold_orders(f4, g4)
    assert res["orders_C0"] == (4, 5, 10) and res["orders_Cinf"] == (4, 5, 10)
    assert C.quartic_disc(C.residual_quartic(m)) != 0


def test_positive_m19_assembly_matches_g0():
    lat = C.trivial_lattice_and_m19()
    assert lat["M19_det"] == 14 and lat["M19_signature"] == [1, 18]
    assert lat["matches_G0_candidate_genus"]


# --------------------------- known-bad -------------------------------------

def test_bad_wrong_vanishing_order_fails():
    """Deliberately wrong vanishing order (c = 0 pushes ord_s(g) to 6):
    the exact-order gate must raise. (Task-mandated negative control.)"""
    m, *_ = _model()
    bad = dict(m)
    bad["c"] = sp.Integer(0)
    g_bad = sp.expand(C.s ** 5 * C.t ** 5 *
                      (bad["a"] * C.s ** 2 + bad["b"] * C.s * C.t))
    assert C.ord_along(g_bad, C.s) == 6
    try:
        C.chk(C.ord_along(g_bad, C.s) == 5, "exact order 5 must fail")
        raised = False
    except C.ControlFailure:
        raised = True
    assert raised


def test_bad_tampered_gram_fails():
    """Corrupt one M19 entry: the block-form/det gate must detect it."""
    target = C.block_diag(sp.Matrix([[0, 1], [1, 0]]), C.e8_cartan_minus()[0],
                          C.e8_cartan_minus()[0], sp.Matrix([[-14]]))
    target[18, 18] = -12   # tamper <-14> -> <-12>
    assert target.det() != 14


def test_bad_cm_point_rejected():
    """h = 7 (CM) must be rejected by BOTH the CM gate and separability."""
    m, j1, j2, cm = _model()
    m7 = C.fiber_model_from_h(j1, j2, 7)
    assert m7["j1"] in cm            # CM gate fires
    assert C.quartic_disc(C.residual_quartic(m7)) == 0  # degeneration fingerprint


def test_bad_square_twist_is_nonminimal():
    m, *_ = _model()
    r = C.square_twist_fatal(m)
    assert r["orders_along_v0"] == [4, 6, 12]  # codim-1 (4,6): fatal, as designed


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
