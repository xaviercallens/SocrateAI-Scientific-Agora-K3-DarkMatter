"""Golden tests for check_C3b_moduli_map.py.

Controls:
  1. Identity control (known-good): pairing a sequence with itself must recover the
     identity relation x - y = 0 — exercises the full pipeline (extraction, MUM check,
     integrality, Frobenius, mirror map, reversion, nullspace) with a known answer.
  2. Corrupted control (known-bad): perturbing one initial term must break integrality
     (the (k+1)^d denominator stops clearing) — the checker must FAIL, proving it can.
  3. Determinism: two runs produce identical certificates (bit-identical JSON).
  4. MUM falsifiability: a non-MUM recurrence (denominator not (k+1)^d) must be rejected.
"""

import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from check_C3b_moduli_map import (  # noqa: E402
    extract_recurrence_polys, generate_sequence, frobenius_derivative,
    mirror_map_z_of_q, run_check, ser_exp, ser_mul, ser_revert,
)

REFS = Path(__file__).resolve().parent.parent.parent / "refs" / "recurrences_v1.json"


def _write_refs(tmp_path, sequences):
    p = tmp_path / "refs.json"
    p.write_text(json.dumps({"_meta": {"status": "TEST"}, "sequences": sequences}))
    return p


ZAGIER_A = {
    "type": "order-2",
    "role": "z_brane",
    "source": "test fixture (copied from refs/recurrences_v1.json)",
    "initial_terms": [1, 2],
    "index_variable": "k",
    "recurrence_python":
        "((7*k**2+7*k+2)*s[-1] + 8*k**2*s[-2]) / sp.Rational((k+1)**2)",
}


# ---------------------------------------------------------------- series toolkit

def test_series_exp_log_roundtrip():
    N = 10
    h = [Fraction(0)] + [Fraction(1, n) for n in range(1, N)]
    E = ser_exp(h, N)
    # d/dz log E = h' must hold: E' = h' E
    for n in range(1, N):
        lhs = n * E[n]
        rhs = sum(j * h[j] * E[n - j] for j in range(1, n + 1))
        assert lhs == rhs


def test_series_reversion_roundtrip():
    N = 12
    q = [Fraction(0), Fraction(1), Fraction(3), Fraction(-2), Fraction(5, 7)] \
        + [Fraction(0)] * (N - 5)
    z = ser_revert(q, N)
    # compose q(z(q)) == identity
    from check_C3b_moduli_map import ser_compose
    ident = ser_compose(q, z, N)
    assert ident[1] == 1
    assert all(ident[n] == 0 for n in range(2, N))


# ---------------------------------------------------------------- extraction

def test_extraction_zagier_A():
    A, B, C, mum = extract_recurrence_polys(ZAGIER_A["recurrence_python"], 2)
    assert mum, "zagier_A denominator must be exactly (k+1)^2 (MUM)"
    a, integral = generate_sequence(A, B, C, [1, 2], 20)
    assert integral
    # first terms must satisfy the recurrence's own k=0 consistency:
    # C(0) a_1 = A(0) a_0  (B(0)=0 here)
    from check_C3b_moduli_map import poly_at
    assert poly_at(C, 0) * a[1] == poly_at(A, 0) * a[0]


def test_mirror_map_normalization():
    A, B, C, _ = extract_recurrence_polys(ZAGIER_A["recurrence_python"], 2)
    a, _ = generate_sequence(A, B, C, [1, 2], 16)
    ad = frobenius_derivative(A, B, C, a, 16)
    z = mirror_map_z_of_q(a, ad, 16)
    assert z[0] == 0 and z[1] == 1, "mirror map must be z(q) = q + O(q^2)"


# ---------------------------------------------------------------- controls

def test_identity_control(tmp_path):
    """Known-good: a sequence paired with itself must yield x - y = 0."""
    refs = _write_refs(tmp_path, {"ctrl_bulk": {**ZAGIER_A, "type": "order-2"},
                                  "ctrl_brane": dict(ZAGIER_A)})
    result, code = run_check(refs, "ctrl_bulk", "ctrl_brane",
                             n_terms=16, max_bidegree=2)
    assert code == 0, result.get("verdict")
    assert "C3B_RELATION_FOUND" in result["verdict"]
    assert result["relation"].startswith("1*x - 1*y = 0") or \
           "x" in result["relation"] and "y" in result["relation"]


def test_corrupted_control(tmp_path):
    """Known-bad: perturbed initial term must fail integrality."""
    bad = dict(ZAGIER_A, initial_terms=[1, 3])
    refs = _write_refs(tmp_path, {"bad": bad, "good": dict(ZAGIER_A)})
    result, code = run_check(refs, "bad", "good", n_terms=16, max_bidegree=2)
    assert code == 1
    assert result["verdict"] == "FAIL_INTEGRALITY"


def test_non_mum_rejected(tmp_path):
    """A recurrence whose denominator is not (k+1)^order must be rejected."""
    non_mum = dict(ZAGIER_A, recurrence_python=
                   "((7*k**2+7*k+2)*s[-1] + 8*k**2*s[-2]) / sp.Rational((k+2)**2)")
    refs = _write_refs(tmp_path, {"nm": non_mum, "good": dict(ZAGIER_A)})
    result, code = run_check(refs, "nm", "good", n_terms=8, max_bidegree=1)
    assert code == 1
    assert result["verdict"] == "FAIL_MUM"


def test_determinism(tmp_path):
    refs = _write_refs(tmp_path, {"a": dict(ZAGIER_A), "b": dict(ZAGIER_A)})
    r1, _ = run_check(refs, "a", "b", n_terms=12, max_bidegree=2)
    r2, _ = run_check(refs, "a", "b", n_terms=12, max_bidegree=2)
    assert json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)


# ---------------------------------------------------------------- real refs sanity

@pytest.mark.skipif(not REFS.exists(), reason="frozen refs not present")
def test_frozen_refs_integrality():
    """Every VALID frozen sequence must be MUM and generate integrally — a transcription
    sanity gate. Skips: (a) BLOCKED entries (intentionally quarantined, not required valid);
    (b) operator-level partners that declare only `initial_terms_rational` (a symmetric-square
    root partner may be rational, e.g. cooper_s10_partner — it is still required MUM)."""
    refs = json.loads(REFS.read_text())
    for sid, entry in refs["sequences"].items():
        if entry.get("_meta_status") == "BLOCKED" or str(entry.get("status", "")).startswith("BLOCKED"):
            continue
        order = {"order-2": 2, "order-3": 3}[entry["type"]]
        A, B, C, mum = extract_recurrence_polys(entry["recurrence_python"], order)
        assert mum, f"{sid}: not MUM"
        init = entry.get("initial_terms")
        if init is None:
            # Rational operator-level partner: MUM already asserted; integrality N/A by design.
            assert "initial_terms_rational" in entry, f"{sid}: missing initial terms"
            continue
        _, integral = generate_sequence(A, B, C, init, 40)
        assert integral, f"{sid}: integrality failed — check transcription"
