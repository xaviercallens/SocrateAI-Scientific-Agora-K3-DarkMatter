#!/usr/bin/env python3
"""
check_C1_singular_loci.py — CORRECTED singular-locus extraction for order-2 partners.

Supersedes the singular-locus step of check_C1.py, which had an F6 defect: it solved for
roots of the recurrence coefficient B(k) in the discrete INDEX k and mislabeled them as
z-space singular points (and hardcoded exponents 0,1/2 -> "type II"). Those are dimensionally
wrong: k is the recurrence index, z is the moduli coordinate.

Correct method (exact algebra): for a MUM order-2 operator built as
    L2 = theta^2 - z*A(theta) - z^2*B(theta+1),  theta = z d/dz,
the leading d/dz coefficient is  z^2 * (1 - a2*z - b2*z^2)  where a2,b2 are the leading
coefficients of A,B. The finite singular loci (excluding the MUM point z=0) are the roots of
    P2(z) = 1 - a2*z - b2*z^2 = 0.
Local exponents (indicial equation) require the full Frobenius analysis at each z-root and are
reported as TODO (NOT hardcoded) so no false Kodaira type is emitted.

Input: an order-2 entry in refs/recurrences_v1.json. Output: corrected-loci certificate.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "checkers"))
import check_C3b_moduli_map as base  # noqa: E402

CHECKER_VERSION = "1.0.0"


def singular_loci(A_poly, B_poly):
    """Roots of P2(z)=1 - a2 z - b2 z^2, a2,b2 = leading coeffs of A(k),B(k)."""
    k, z = sp.symbols("k z")
    a2 = sp.Poly(A_poly, k).LC()
    b2 = sp.Poly(B_poly, k).LC()
    P2 = sp.expand(1 - a2 * z - b2 * z**2)
    roots = sp.solve(sp.Eq(P2, 0), z)
    return P2, sorted(roots, key=lambda r: sp.re(r.evalf())), a2, b2


def run_check(refs_path, partner_id):
    raw = Path(refs_path).read_bytes()
    refs = json.loads(raw)
    result = {
        "checker": "check_C1_singular_loci.py",
        "checker_version": CHECKER_VERSION,
        "criterion": "C1-loci (CORRECTED z-space singular locus of order-2 partner)",
        "supersedes": "check_C1.py singular-locus step (F6 defect: index-space roots of B(k))",
        "refs_sha256": hashlib.sha256(raw).hexdigest(),
        "partner": partner_id,
    }
    e = refs["sequences"].get(partner_id)
    if e is None or e["type"] != "order-2":
        result["verdict"] = "ERROR_PARTNER_NOT_ORDER2"
        return result, 2
    A, B, C, _ = base.extract_recurrence_polys(e["recurrence_python"], 2)
    P2, roots, a2, b2 = singular_loci(A.as_expr(), B.as_expr())
    result["leading_dz_factor_P2_of_z"] = str(sp.factor(P2))
    result["singular_loci_z"] = [str(sp.nsimplify(r)) for r in roots]
    result["mum_point"] = "z=0"
    result["kodaira_types"] = "TODO — requires local Frobenius exponents; NOT hardcoded (see F6 note)"
    result["verdict"] = f"C1_SINGULAR_LOCI_CORRECTED(n_finite_loci={len(roots)})"
    result["provenance"] = ("Generated-by: checkers/check_C1_singular_loci.py v1.0.0 (Tier B) | "
                            "Verified-by: exact algebra (leading d/dz coefficient) | Reviewed-by: pending T0")
    return result, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refs", default=str(REPO / "refs" / "recurrences_v1.json"))
    ap.add_argument("--partner", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    result, code = run_check(args.refs, args.partner)
    payload = json.dumps(result, indent=2, sort_keys=True)
    out = args.out or str(REPO / "data" / "certificates" / f"C1loci_{args.partner}.json")
    Path(out).write_text(payload + "\n")
    print(payload)
    sys.exit(code)


if __name__ == "__main__":
    main()
