#!/usr/bin/env python3
"""
check_U1_witness_serialization.py — verifies the explicit base-change witness
matrix P now serialized at derived.u_splitting.basis_change_matrix (added
2026-07-27 per T0 ruling, motivated by Stream 1's independent-verification
finding: briefs/STREAM1_U1_INDEPENDENT_VERIFICATION_2026_07_27.md, Stream 1
repo — check_U1_lattice.py's stage3_lattice() computed the base-change matrix
P in memory but serialized only det(P) and P^T G P, forcing third parties to
re-derive their own witness).

WHAT THIS CHECKS (exact integer arithmetic throughout, no floats)
  - If derived.u_splitting.basis_change_matrix is ABSENT (e.g. v3.json, which
    has no "derived" block at all, or v4.json, which predates this field):
    report WITNESS_ABSENT. This is NOT a failure — v3/v4 are expected to lack
    it and must not break the regression.
  - If present: verify P is a 3x3 integer matrix, det(P) is +-1 and matches
    the certificate's own basis_change_det, and P^T G P (G =
    derived.gram_primitive_even, taken as certificate input) equals the
    certificate's own derived.u_splitting.gram_after exactly.
  All hold -> PASS. Any violation -> FAIL.

This is a self-consistency check of what the certificate claims about its own
serialized witness (it does not re-derive P from G independently — Stream 1's
check_U1_splitting_independent.py, in the Stream 1 repo, already does that).

Usage:
  python3 checkers/check_U1_witness_serialization.py                # v5 draft
  python3 checkers/check_U1_witness_serialization.py --cert <path>
  python3 checkers/check_U1_witness_serialization.py --all           # v3,v4,v5

Exit codes: 0 PASS or WITNESS_ABSENT (both legitimate non-failure outcomes),
3 FAIL (structural inconsistency), 2 usage/data (missing file).

Generated-by: Sonnet 5 (Stream 2) | Verified-by: this file's own structural
assertions + test_U1_witness_serialization_controls.py | Reviewed-by: pending
T0 (Xavier) acceptance of C2_cooper_s7_v5_DRAFT.json
"""

import argparse
import json
import sys
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parent.parent
DEFAULT_CERT = REPO / "data" / "certificates" / "C2_cooper_s7_v5_DRAFT.json"


class ControlFailure(Exception):
    """Structural inconsistency: a real FAIL."""


class WitnessAbsent(Exception):
    """The certificate predates witness serialization — not a failure."""


def chk(cond, msg):
    if not cond:
        raise ControlFailure(msg)


def load_cert(path):
    return json.loads(Path(path).read_text())


def verify_certificate(cert, verbose=True, scramble_P=None, scramble_gram_after=None):
    """Returns a result dict on PASS. Raises WitnessAbsent if the certificate
    has no serialized witness, ControlFailure if it has one but it's wrong.
    `scramble_P` / `scramble_gram_after` are hooks used only by the negative
    controls, never by the plain PASS run."""
    derived = cert.get("derived")
    if derived is None:
        raise WitnessAbsent("certificate has no 'derived' block "
                             "(not a U1 lattice certificate, e.g. v3.json)")
    u = derived.get("u_splitting")
    if not u or "basis_change_matrix" not in u:
        raise WitnessAbsent("certificate has no derived.u_splitting.basis_change_matrix "
                             "(predates the T0-ruled witness serialization, e.g. v4.json)")

    G_raw = derived.get("gram_primitive_even")
    chk(G_raw is not None, "certificate has basis_change_matrix but no "
        "gram_primitive_even — not self-contained")
    chk(len(G_raw) == 3 and all(len(row) == 3 for row in G_raw), "G is not 3x3")
    G = sp.Matrix(G_raw)

    P_raw = u["basis_change_matrix"]
    if scramble_P is not None:
        P_raw = scramble_P([list(row) for row in P_raw])
    chk(len(P_raw) == 3 and all(len(row) == 3 for row in P_raw), "P is not 3x3")
    chk(all(isinstance(x, int) for row in P_raw for x in row), "P has non-integer entries")
    P = sp.Matrix(P_raw)

    detP = int(P.det())
    chk(detP in (1, -1), f"det(P) = {detP}, not +-1 (P not in GL_3(Z))")
    cert_detP = u.get("basis_change_det")
    if cert_detP is not None and scramble_P is None:
        chk(detP == cert_detP, f"independently computed det(P) = {detP} != "
            f"certificate's own basis_change_det = {cert_detP}")

    gram_after_raw = u["gram_after"]
    if scramble_gram_after is not None:
        gram_after_raw = scramble_gram_after([list(row) for row in gram_after_raw])
    gram_after = sp.Matrix(gram_after_raw)

    PtGP = P.T * G * P
    chk(PtGP == gram_after, f"P^T G P = {PtGP.tolist()} != certificate's own "
        f"gram_after = {gram_after.tolist()}")

    if verbose:
        print(f"  G  (gram_primitive_even, from certificate) = {G.tolist()}")
        print(f"  P  (basis_change_matrix, from certificate)  = {P.tolist()}")
        print(f"  det(P) = {detP}  (in GL_3(Z): {detP in (1, -1)})")
        print(f"  P^T G P = {PtGP.tolist()}")
        print(f"  matches certificate's gram_after: {PtGP == gram_after}")

    return {"detP": detP, "PtGP": PtGP.tolist(), "gram_after": gram_after.tolist()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cert", default=str(DEFAULT_CERT))
    ap.add_argument("--all", action="store_true",
                     help="check v3, v4, and v5-draft certificates in one run")
    args = ap.parse_args()

    paths = [Path(args.cert)]
    if args.all:
        paths = [REPO / "data" / "certificates" / f
                  for f in ("C2_cooper_s7_v3.json", "C2_cooper_s7_v4.json",
                             "C2_cooper_s7_v5_DRAFT.json")]

    worst = 0
    for path in paths:
        print("=" * 78)
        print(f"check_U1_witness_serialization.py — {path.name}")
        print("=" * 78)
        if not path.exists():
            print(f"FAIL: certificate not found at {path}", file=sys.stderr)
            worst = max(worst, 2)
            continue
        cert = load_cert(path)
        try:
            verify_certificate(cert, verbose=True)
            print("VERDICT: PASS (witness self-consistent)")
        except WitnessAbsent as e:
            print(f"VERDICT: WITNESS_ABSENT ({e})")
        except ControlFailure as e:
            print(f"VERDICT: FAIL ({e})", file=sys.stderr)
            worst = max(worst, 3)
        print()
    return worst


if __name__ == "__main__":
    sys.exit(main())
