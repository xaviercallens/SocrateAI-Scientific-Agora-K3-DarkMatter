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


def theta_coeffs(A_poly, B_poly):
    """Theta-form coefficients P2,P1,P0 of L2 = theta^2 - z A(theta) - z^2 B(theta+1)."""
    k, z, th = sp.symbols("k z theta")
    A = A_poly.subs(k, th)
    B = B_poly.subs(k, th)
    L2 = sp.expand(th**2 - z * A - z**2 * B.subs(th, th + 1))
    P = {j: sp.Integer(0) for j in range(3)}
    for (j,), c in sp.Poly(L2, th).terms():
        P[j] = sp.expand(c)
    return P[2], P[1], P[0]


def singular_loci(A_poly, B_poly):
    """Roots of P2(z)=1 - a2 z - b2 z^2, a2,b2 = leading coeffs of A(k),B(k)."""
    k, z = sp.symbols("k z")
    a2 = sp.Poly(A_poly, k).LC()
    b2 = sp.Poly(B_poly, k).LC()
    P2 = sp.expand(1 - a2 * z - b2 * z**2)
    roots = sp.solve(sp.Eq(P2, 0), z)
    return P2, sorted(roots, key=lambda r: sp.re(r.evalf())), a2, b2


def local_exponents(A_poly, B_poly):
    """Exact indicial exponents at every regular singular point of the order-2 ODE
        P2 z^2 y'' + z(P2+P1) y' + P0 y = 0,  (theta = z d/dz form),
    at z=0, the finite loci (roots of P2), and z=inf. Returns list of (point, [r1,r2])
    plus the Fuchs-relation check (sum of all exponents == #sing_pts - 2 for order 2)."""
    z, r, w = sp.symbols("z r w")
    P2z, P1z, P0z = theta_coeffs(A_poly, B_poly)
    # y'' + p y' + q y = 0
    a = sp.expand(P2z * z**2)
    b = sp.expand(z * (P2z + P1z))
    p = sp.cancel(b / a)
    q = sp.cancel(P0z / a)

    def roots_with_mult(poly_in_r):
        """Exact roots of a quadratic-in-r indicial poly, WITH multiplicity (list length 2)."""
        rr = sp.roots(sp.Poly(sp.expand(poly_in_r), r))  # {root: multiplicity}
        out = []
        for root, mult in rr.items():
            out.extend([sp.nsimplify(root)] * mult)
        return out  # length 2 for a genuine 2nd-order indicial equation

    def indicial_at(zc):
        p0 = sp.limit((z - zc) * p, z, zc)
        q0 = sp.limit((z - zc)**2 * q, z, zc)
        return roots_with_mult(r * (r - 1) + p0 * r + q0)

    pts = []
    finite_sing = [sp.Integer(0)] + list(sp.solve(P2z, z))
    for zc in finite_sing:
        pts.append((str(zc), indicial_at(zc)))
    # at infinity: z=1/w, exponents from the transformed equation's indicial at w=0
    p_w = sp.cancel((2 / w - p.subs(z, 1 / w) / w**2))   # p_tilde(w) for y in w
    q_w = sp.cancel(q.subs(z, 1 / w) / w**4)
    p0i = sp.limit(w * p_w, w, 0)
    q0i = sp.limit(w**2 * q_w, w, 0)
    pts.append(("oo", roots_with_mult(r * (r - 1) + p0i * r + q0i)))

    total = sum(sum(e for e in exps) for _, exps in pts)
    n_sing = len(pts)
    fuchs_ok = sp.simplify(total - (n_sing - 2)) == 0
    return pts, bool(fuchs_ok), sp.nsimplify(total), n_sing


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
    result["finite_singular_loci_z"] = [str(sp.nsimplify(r)) for r in roots]
    result["mum_point"] = "z=0"

    exps, fuchs_ok, total, n_sing = local_exponents(A.as_expr(), B.as_expr())
    result["local_exponents"] = {pt: [str(x) for x in ex] for pt, ex in exps}
    result["exponent_differences"] = {pt: str(sp.Abs(ex[0] - ex[1])) for pt, ex in exps if len(ex) == 2}
    result["fuchs_relation_check"] = {"sum_all_exponents": str(total),
                                      "expected_n_sing_minus_2": n_sing - 2,
                                      "PASS": fuchs_ok}
    result["kodaira_types"] = ("DEFERRED (open ticket): exponent differences computed exactly, but "
                               "PF-exponent -> Kodaira-type requires resolving the rank-1 twist "
                               "(fibre monodromy in SL2(Z), det +1) vs raw PF monodromy. NOT emitting "
                               "a type or a rho/T until that is done rigorously — see F6 lesson.")
    result["verdict"] = (f"C1_LOCI_AND_EXPONENTS_CORRECTED(n_finite_loci={len(roots)}, "
                         f"fuchs_ok={fuchs_ok})")
    if not fuchs_ok:
        result["verdict"] = "ERROR_FUCHS_RELATION_FAILED"
        return result, 2
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
