#!/usr/bin/env python3
"""
test_U1_witness_serialization_controls.py — mandatory negative controls for
check_U1_witness_serialization.py. "A test that cannot fail is not a test"
(TODO.md standing rule 1).

Controls:
  1. TAMPERED P: corrupt one entry of the real v5 (LIVE) basis_change_matrix.
     P^T G P no longer equals gram_after -> must FAIL.
  2. NON-UNIMODULAR P: scale a column of the real P by 2. det(P) becomes even
     -> must FAIL at the GL_3(Z) gate.
  3. TAMPERED gram_after: corrupt one entry of the certificate's own claimed
     gram_after. The real P no longer matches it -> must FAIL.
  4. WITNESS ABSENT (v4.json): the (now-superseded, still audit-retained) v4
     certificate predates this field entirely -> must report WITNESS_ABSENT,
     NOT FAIL (so the regression stays green on v4).
  5. WITNESS ABSENT (v3.json): a differently-shaped certificate with no
     "derived" block at all -> must also report WITNESS_ABSENT, not crash.
  6. POSITIVE sanity: the unmodified v5.json (LIVE) certificate PASSes.
  7. POSITIVE sanity: the retained v5_DRAFT.json certificate PASSes too
     (identical witness content to v5.json, only metadata differs).

Run:
  python3 checkers/test_U1_witness_serialization_controls.py
  pytest checkers/test_U1_witness_serialization_controls.py

Generated-by: Sonnet 5 (Stream 2) | Verified-by: this file IS the verifier for
check_U1_witness_serialization.py | Reviewed-by: pending T0 (Xavier)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_U1_witness_serialization as W  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
CERTS = REPO / "data" / "certificates"


def _v5():
    return W.load_cert(CERTS / "C2_cooper_s7_v5.json")


def _v5_draft():
    return W.load_cert(CERTS / "C2_cooper_s7_v5_DRAFT.json")


def _v4():
    return W.load_cert(CERTS / "C2_cooper_s7_v4.json")


def _v3():
    return W.load_cert(CERTS / "C2_cooper_s7_v3.json")


# ---------------------------------------------------------------------------
# 1. tampered P
# ---------------------------------------------------------------------------

def test_tampered_P_fails():
    cert = _v5()

    def scramble(P):
        P[0][1] += 1
        return P

    try:
        W.verify_certificate(cert, verbose=False, scramble_P=scramble)
    except W.ControlFailure as e:
        return str(e)
    raise AssertionError("tampered-P control FAILED: checker accepted a corrupted witness")


# ---------------------------------------------------------------------------
# 2. non-unimodular P
# ---------------------------------------------------------------------------

def test_non_unimodular_P_fails():
    cert = _v5()

    def scramble(P):
        for i in range(3):
            P[i][0] *= 2
        return P

    try:
        W.verify_certificate(cert, verbose=False, scramble_P=scramble)
    except W.ControlFailure as e:
        assert "GL_3(Z)" in str(e), f"expected a GL_3(Z) rejection, got: {e}"
        return str(e)
    raise AssertionError("non-unimodular-P control FAILED: checker accepted det(P) != +-1")


# ---------------------------------------------------------------------------
# 3. tampered gram_after
# ---------------------------------------------------------------------------

def test_tampered_gram_after_fails():
    cert = _v5()

    def scramble(gram_after):
        gram_after[2][2] += 1
        return gram_after

    try:
        W.verify_certificate(cert, verbose=False, scramble_gram_after=scramble)
    except W.ControlFailure as e:
        return str(e)
    raise AssertionError("tampered-gram_after control FAILED: checker accepted a "
                          "mismatched gram_after")


# ---------------------------------------------------------------------------
# 4/5. witness absent — must NOT fail
# ---------------------------------------------------------------------------

def test_v4_witness_absent():
    cert = _v4()
    try:
        W.verify_certificate(cert, verbose=False)
    except W.WitnessAbsent as e:
        return str(e)
    except W.ControlFailure as e:
        raise AssertionError(f"v4 (predates serialization) raised ControlFailure "
                              f"instead of WitnessAbsent: {e}")
    raise AssertionError("v4 unexpectedly PASSED (it has no basis_change_matrix field)")


def test_v3_witness_absent():
    cert = _v3()
    try:
        W.verify_certificate(cert, verbose=False)
    except W.WitnessAbsent as e:
        return str(e)
    except W.ControlFailure as e:
        raise AssertionError(f"v3 (different schema entirely) raised ControlFailure "
                              f"instead of WitnessAbsent: {e}")
    raise AssertionError("v3 unexpectedly PASSED (it has no 'derived' block)")


# ---------------------------------------------------------------------------
# 6. positive sanity
# ---------------------------------------------------------------------------

def test_v5_live_passes():
    cert = _v5()
    result = W.verify_certificate(cert, verbose=False)
    assert result["detP"] in (1, -1)
    assert result["PtGP"] == result["gram_after"]
    return "v5 (LIVE) witness verified PASS as expected"


def test_v5_draft_passes():
    cert = _v5_draft()
    result = W.verify_certificate(cert, verbose=False)
    assert result["detP"] in (1, -1)
    assert result["PtGP"] == result["gram_after"]
    return "v5_DRAFT witness verified PASS as expected"


# ---------------------------------------------------------------------------
# runner (plain python3, no pytest dependency required)
# ---------------------------------------------------------------------------

CONTROLS = [
    ("tampered-P (must FAIL)", test_tampered_P_fails),
    ("non-unimodular-P (must FAIL)", test_non_unimodular_P_fails),
    ("tampered-gram_after (must FAIL)", test_tampered_gram_after_fails),
    ("v4 witness absent (must NOT fail)", test_v4_witness_absent),
    ("v3 witness absent (must NOT fail)", test_v3_witness_absent),
    ("v5 LIVE unmodified (must PASS)", test_v5_live_passes),
    ("v5 draft unmodified (must PASS)", test_v5_draft_passes),
]


def main():
    print("=" * 78)
    print("test_U1_witness_serialization_controls.py")
    print("=" * 78)
    all_ok = True
    for name, fn in CONTROLS:
        try:
            detail = fn()
            ok = True
        except AssertionError as e:
            ok, detail = False, str(e)
        all_ok &= ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        print(f"        {detail}")
    print("=" * 78)
    print(f"VERDICT: {'ALL CONTROLS PASS' if all_ok else 'CONTROL SUITE FAILED'}")
    print("=" * 78)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
