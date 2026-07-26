#!/usr/bin/env python3
"""
AE-7 — Tests for Stream 2 AutoEvolve anchor fingerprints and gate battery.

Answer-key controls:
  * A005259 (S22 / apery_zeta3) — order-3 ODE, q2 = 12, integral mirror map
  * A005258 (S21 / apery_zeta2_s21) — order-2 ODE, q2 = 5, integral, elliptic
  * A112019 (S12) — order-2 ODE, q2 = 81/8, NON-integral (negative control)
  * cooper_s7 — order-3, q2 = 9, integral, C3b PASS, partner = A279619
  * cooper_s10 — order-3, q2 = 4, integral, C3b PASS, rational partner
"""

import json
import sys
from fractions import Fraction
from pathlib import Path

try:
    import pytest
except ModuleNotFoundError:
    pytest = None

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT))

from ae_anchor_fingerprints import fingerprint


def _skip(msg):
    if pytest:
        pytest.skip(msg)
    print(f"SKIP: {msg}")


def load_fingerprints():
    path = REPO_ROOT / "data" / "autoresearch_v2" / "ae_anchor_fingerprints.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


def _ode_order(rec):
    return rec.get("ode", {}).get("ode_order")


def _q2(rec):
    q = rec.get("mirror", {}).get("q2")
    return Fraction(str(q)) if q else None


def _integral(rec):
    return rec.get("mirror", {}).get("integral")


def _c3b_verdict(rec):
    return rec.get("c3b", {}).get("verdict", "")


def test_apery_zeta3_is_k3_control():
    rec = fingerprint("apery_zeta3")
    assert _ode_order(rec) == 3
    assert _q2(rec) == Fraction(12)
    assert _integral(rec) is True


def test_apery_zeta2_s21_is_elliptic_control():
    rec = fingerprint("apery_zeta2_s21")
    assert _ode_order(rec) == 2
    assert _q2(rec) == Fraction(5)
    assert _integral(rec) is True


def test_s12_is_order2_non_integral():
    rec = fingerprint("s12_v1_primary")
    assert _ode_order(rec) == 2
    assert _q2(rec) == Fraction(81, 8)
    assert _integral(rec) is False


def test_cooper_s7_q2_and_c3b():
    rec = fingerprint("cooper_s7")
    assert _ode_order(rec) == 3
    assert _q2(rec) == Fraction(9)
    assert _integral(rec) is True
    assert "SYM2" in _c3b_verdict(rec)
    # Partner first terms match A279619: 1, 2, 22, 336, 6006, ...
    partner_terms = rec["c3b"]["partner_first_terms"]
    assert [int(Fraction(t)) for t in partner_terms[:5]] == [1, 2, 22, 336, 6006]


def test_cooper_s10_q2_and_c3b():
    rec = fingerprint("cooper_s10")
    assert _ode_order(rec) == 3
    assert _q2(rec) == Fraction(4)
    assert _integral(rec) is True
    assert "SYM2" in _c3b_verdict(rec)


def test_cooper_s7_singular_loci():
    rec = fingerprint("cooper_s7")
    roots = rec["singular_loci"]["rational_roots"]
    assert "-1" in roots
    assert "1/27" in roots


def test_cooper_s10_singular_loci():
    rec = fingerprint("cooper_s10")
    roots = rec["singular_loci"]["rational_roots"]
    assert "-1/4" in roots
    assert "1/16" in roots


def test_fingerprint_json_has_no_float_literals():
    """Gate numbers must be exact rationals (strings), not floats."""
    data = load_fingerprints()
    if data is None:
        return _skip("ae_anchor_fingerprints.json not generated yet")
    text = json.dumps(data, default=str)
    import re
    floats = re.findall(r"\b\d+\.\d+\b", text)
    assert not floats, f"Found bare float literals in fingerprint JSON: {floats[:20]}"


def test_fingerprint_json_reproduces_answer_keys():
    data = load_fingerprints()
    if data is None:
        return _skip("ae_anchor_fingerprints.json not generated yet")
    fps = data["fingerprints"]
    assert Fraction(str(fps["apery_zeta3"]["mirror"]["q2"])) == Fraction(12)
    assert fps["apery_zeta3"]["ode"]["ode_order"] == 3
    assert Fraction(str(fps["s12_v1_primary"]["mirror"]["q2"])) == Fraction(81, 8)
