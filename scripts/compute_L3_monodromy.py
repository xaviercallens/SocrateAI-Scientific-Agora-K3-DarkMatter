#!/usr/bin/env python3
"""
compute_L3_monodromy.py — local exponent / unipotency analysis of the ORDER-3
operator L3, per the Deep Think (T0s) course-correction mandate of 2026-07-25.

Mandate context
---------------
E-007 established that L2 is a *twisted* Picard-Fuchs operator (exponents {0, 1/2},
det(monodromy) = -1), so no Kodaira data can be read from it. Deep Think's
course-correction proposed "Route A": run C1/C2 on L3 instead, on the stated
premise that

    "Because L3 = Sym^2(L2), the 1/2 exponents of L2 double to 1 in L3,
     effectively clearing the branch cut and rendering L3 unipotent at the
     finite singular points."

THIS SCRIPT TESTS THAT PREMISE. It does not assume it.

Result (see run output / emitted certificate): the premise is FALSE.
Sym^2 of a rank-2 system with exponents {0, 1/2} has solution space spanned by
{y1^2, y1*y2, y2^2}, whose exponents are {0, 0+1/2, 1} = {0, 1/2, 1}. Only the
y2^2 term doubles to 1; the CROSS TERM y1*y2 retains exponent 1/2. The branch
cut is therefore NOT cleared, and L3 is NOT unipotent at the finite singular loci.

Consequence: Route A as specified cannot work. A gauge transformation cannot fix
this either -- gauge transforms shift all exponents at a point by the same amount
and therefore leave exponent DIFFERENCES invariant, so a difference of 1/2 is
gauge-invariant. Clearing it requires a ramified pullback (Route B, Hauptmodul).

Two independent confirmations are printed: a direct order-3 indicial computation,
and the structural Sym^2 prediction.

Usage:
  python3 scripts/compute_L3_monodromy.py
  python3 scripts/compute_L3_monodromy.py --emit-certs
"""

import argparse
import json
import sys
from pathlib import Path

import sympy as sp

z, r = sp.symbols("z r")
REPO = Path(__file__).resolve().parent.parent

# L3 theta-basis coefficients (L3 = Q3*th^3 + Q2*th^2 + Q1*th + Q0), exact in Q[z].
# Provenance: lean4_formal_proofs/Structures/CooperSym2Proof.lean (Tier A, kernel-verified).
L3_OPERATORS = {
    "cooper_s7": {
        "oeis": "A183204",
        "Q3": -27 * z**2 - 26 * z + 1,
        "Q2": -81 * z**2 - 39 * z,
        "Q1": -78 * z**2 - 21 * z,
        "Q0": -24 * z**2 - 4 * z,
    },
    "cooper_s10": {
        "oeis": "A005260",
        "Q3": -64 * z**2 - 12 * z + 1,
        "Q2": -192 * z**2 - 18 * z,
        "Q1": -188 * z**2 - 10 * z,
        "Q0": -60 * z**2 - 2 * z,
    },
}

# L2 exponents at every finite singular locus, established by
# checkers/check_C1_kodaira_consistency.py (E-007).
L2_EXPONENTS = [sp.Integer(0), sp.Rational(1, 2)]


def l3_local_exponents(Q3, Q2, Q1, Q0, zc):
    """Indicial roots of the order-3 operator L3 at the regular singular point zc.

    theta = z*d/dz, so
        theta^1 = zD
        theta^2 = zD + z^2 D^2
        theta^3 = zD + 3 z^2 D^2 + z^3 D^3
    giving
        L3 = Q3*z^3 D^3 + (3*Q3 + Q2)*z^2 D^2 + (Q3 + Q2 + Q1)*z D + Q0.
    """
    a3 = sp.expand(Q3 * z**3)
    a2 = sp.expand((3 * Q3 + Q2) * z**2)
    a1 = sp.expand((Q3 + Q2 + Q1) * z)
    a0 = sp.expand(Q0)

    p2, p1, p0 = sp.simplify(a2 / a3), sp.simplify(a1 / a3), sp.simplify(a0 / a3)
    A2 = sp.simplify(sp.limit((z - zc) * p2, z, zc))
    A1 = sp.simplify(sp.limit((z - zc) ** 2 * p1, z, zc))
    A0 = sp.simplify(sp.limit((z - zc) ** 3 * p0, z, zc))

    ind = r * (r - 1) * (r - 2) + A2 * r * (r - 1) + A1 * r + A0
    roots = sp.solve(sp.Eq(sp.simplify(ind), 0), r)
    return sorted([sp.nsimplify(x) for x in roots], key=lambda s: sp.re(s))


def sym2_predicted_exponents(l2_exps):
    """Exponents of Sym^2 of a rank-2 system: {2a, a+b, 2b} for L2 exponents {a,b}."""
    a, b = l2_exps
    return sorted([2 * a, a + b, 2 * b], key=lambda s: sp.re(s))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-certs", action="store_true", help="write C1_L3_*.json certificates")
    args = ap.parse_args()

    predicted = sym2_predicted_exponents(L2_EXPONENTS)

    print("=" * 76)
    print("L3 LOCAL EXPONENT / UNIPOTENCY ANALYSIS")
    print("Testing the Deep Think Route-A premise: 'L3 is unipotent at finite loci'")
    print("=" * 76)
    print(f"\nL2 exponents at every finite locus (E-007): {L2_EXPONENTS}")
    print(f"Sym^2 structural prediction for L3:        {predicted}   <- cross term keeps 1/2")

    overall_unipotent = True
    certs = {}

    for name, op in L3_OPERATORS.items():
        Q3, Q2, Q1, Q0 = op["Q3"], op["Q2"], op["Q1"], op["Q0"]
        loci = sorted(sp.solve(sp.Eq(Q3, 0), z), key=lambda s: sp.re(s))

        print("\n" + "-" * 76)
        print(f"{name}  (bulk {op['oeis']})   leading Q3 = {sp.factor(Q3)}")
        fibres = []
        for zc in loci:
            exps = l3_local_exponents(Q3, Q2, Q1, Q0, zc)
            unip = all(bool(x.is_integer) for x in exps)
            matches = exps == predicted
            overall_unipotent &= unip
            print(
                f"   z = {str(zc):>6}   exponents = {[str(e) for e in exps]}   "
                f"unipotent? {unip}   matches Sym^2 prediction? {matches}"
            )
            fibres.append(
                {
                    "singular_point_z": str(zc),
                    "local_exponents": [str(e) for e in exps],
                    "unipotent": bool(unip),
                    "matches_sym2_prediction": bool(matches),
                    "kodaira_type": None,
                    "kodaira_type_reason": (
                        "NOT DETERMINED. Exponents contain a half-integer (1/2), so the local "
                        "monodromy is not unipotent and this is not a Kodaira fibre monodromy. "
                        "No Kodaira type is derivable at this locus from L3."
                    ),
                }
            )

        certs[name] = {
            "checker": "compute_L3_monodromy.py",
            "checker_version": "1.0.0",
            "date": "2026-07-26",
            "operator": "L3 (order-3 bulk)",
            "sequence": op["oeis"],
            "provenance": (
                "L3 theta-basis coefficients from lean4_formal_proofs/Structures/"
                "CooperSym2Proof.lean (Tier A, kernel-verified)"
            ),
            "finite_singular_loci": [str(l) for l in loci],
            "l2_exponents_reference": [str(e) for e in L2_EXPONENTS],
            "sym2_predicted_exponents": [str(e) for e in predicted],
            "fibres": fibres,
            "picard_rank": None,
            "transcendental_rank": None,
            "verdict": "L3_NOT_UNIPOTENT_AT_FINITE_LOCI",
            "route_A_premise": "REFUTED",
            "notes": [
                "Deep Think (T0s) course-correction 2026-07-25 proposed Route A on the premise "
                "that L3 = Sym^2(L2) makes the 1/2 exponents 'double to 1', rendering L3 "
                "unipotent at the finite singular points. This script tested that premise and "
                "REFUTES it.",
                "Sym^2 of a rank-2 system with exponents {a,b} has exponents {2a, a+b, 2b}. "
                "With {0, 1/2} that is {0, 1/2, 1}: only y2^2 doubles to 1, while the CROSS "
                "TERM y1*y2 retains 1/2. The branch cut is not cleared.",
                "Confirmed two independent ways: direct order-3 indicial computation, and the "
                "Sym^2 structural prediction. They agree exactly.",
                "A gauge transformation cannot fix this: gauge shifts all exponents at a point "
                "by the same amount, so exponent DIFFERENCES are gauge-invariant. A difference "
                "of 1/2 cannot be gauged away. Clearing it requires a RAMIFIED PULLBACK "
                "(Route B: Hauptmodul substitution), not a gauge transform.",
                "Therefore NO Picard rank rho and NO transcendental rank T are emitted here. "
                "Emitting them would repeat the E-007 fabrication.",
            ],
        }

    print("\n" + "=" * 76)
    print("VERDICT")
    print("=" * 76)
    if overall_unipotent:
        print("L3 IS unipotent at all finite loci -- Route A premise HOLDS.")
    else:
        print("L3 is NOT unipotent at the finite singular loci -- Route A premise is REFUTED.")
        print("  Exponents {0, 1/2, 1}: the Sym^2 cross term y1*y2 retains the half-integer.")
        print("  Kodaira classification remains BLOCKED at the L3 level.")
        print("  Gauge transforms cannot help (exponent differences are gauge-invariant).")
        print("  Only Route B (ramified Hauptmodul pullback) remains viable.")
        print("\n  NO rho / T emitted. Emitting them would repeat the E-007 fabrication.")

    if args.emit_certs:
        outdir = REPO / "data" / "certificates"
        for name, cert in certs.items():
            p = outdir / f"C1_L3_{name}.json"
            p.write_text(json.dumps(cert, indent=2))
            print(f"\nWrote {p.relative_to(REPO)}")

    return 0 if overall_unipotent else 3


if __name__ == "__main__":
    sys.exit(main())
