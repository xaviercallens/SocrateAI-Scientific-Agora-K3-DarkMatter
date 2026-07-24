#!/usr/bin/env python3
"""
check_C3b_symsqrt.py — C3b criterion checker, *constructive* variant.

The moduli-map checker (check_C3b_moduli_map.py) searches for an algebraic relation
between a bulk (order-3) mirror map and a *catalogued* brane (order-2) mirror map. That
test presumes the order-2 partner is already known and pre-normalised. For the Cooper
sporadic sequences it never was — every catalogued order-2 candidate failed, because the
partner is not in any catalogue: it is the symmetric-square root of the bulk operator
itself, in the bulk's own z-coordinate.

This checker EXTRACTS that partner directly and certifies the symmetric-square relation:

  1. Load the bulk order-3 holonomic recurrence from refs/ (literature transcription only).
  2. Generate g_n = Σ a_n z^n exactly (Fraction), reusing the order-3 MUM checker.
  3. Take the exact power-series square root f = √g  (g_0 = 1 ⇒ f_0 = 1). If the bulk is a
     symmetric square Sym²(L2), the unique holomorphic solution of L3 at the MUM point is
     the square of the holomorphic solution of L2, so g = f² and f solves L2.
  4. DETECT whether f is order-2 holonomic: fit polynomials C(n) f_{n+1} = A(n) f_n + B(n) f_{n-1}
     (deg ≤ D) by an EXACT nullspace over ℚ on the first `n_fit` terms, then RE-VALIDATE the
     fitted recurrence on terms up to `n_val` (falsifiability of the fit — a spurious fit dies
     here). If no order-2 recurrence exists, the bulk is NOT a symmetric square → verdict
     NOT_SYMMETRIC_SQUARE (this is the intended failure mode; apery_zeta2 as "bulk" hits it).
  5. Validate the extracted L2 is MUM (C(n) = (n+1)²) and integral-or-rational, and confirm
     z(L2)(q) == z(L3)(q) exactly to `mirror_order` (Sym² preserves the mirror map; this is the
     moduli map, and it is the identity — the tightest possible Shioda–Inose relation).
  6. Emit a certificate embedding the ref SHA256, the extracted partner recurrence, the partner
     terms, and all validation orders.

Epistemic tier: the extracted recurrence and all equalities are exact-arithmetic, machine-
checked to finite order N — report as PASS(N). A proof that f satisfies the recurrence for ALL
n (operator-level L3 = Sym²(L2)) is a Stream-1 symbolic-ODE task, tracked separately.

Checker contract (K3_CRITERIA.md §3): exact arithmetic, no network, no LLM calls, deterministic.
"""

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp

# Reuse the audited order-3 machinery (recurrence extraction, generation, Frobenius, mirror map).
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_C3b_moduli_map as base  # noqa: E402

CHECKER_VERSION = "1.0.0"
REPO_ROOT = Path(__file__).resolve().parent.parent


def series_sqrt(g, N):
    """Exact power-series square root of g (list[Fraction]) with g[0] == 1."""
    assert g[0] == 1, "series_sqrt requires g[0] == 1 (MUM normalisation)"
    f = [Fraction(0)] * N
    f[0] = Fraction(1)
    for n in range(1, N):
        s = sum(f[j] * f[n - j] for j in range(1, n))
        f[n] = (g[n] - s) / 2
    return f


def fit_order2_recurrence(f, n_fit, deg):
    """Exact nullspace fit of C(n) f_{n+1} + A(n) f_n + B(n) f_{n-1} = 0, deg(poly) ≤ deg,
    over n = 1..n_fit-2. Returns (C_poly, A_poly, B_poly) as sympy Polys in n with integer
    coefficients (content removed), or None if no nonzero relation exists."""
    n = sp.Symbol("n")
    rows = []
    for m in range(1, n_fit - 1):
        row = []
        for fv in (f[m + 1], f[m], f[m - 1]):
            for d in range(deg + 1):
                val = Fraction(m) ** d * fv
                row.append(sp.Rational(val.numerator, val.denominator))
        rows.append(row)
    ns = sp.Matrix(rows).nullspace()
    if not ns:
        return None
    v = ns[0]
    dens = [sp.denom(x) for x in v]
    lcm = sp.ilcm(*[int(d) for d in dens]) if len(dens) > 1 else int(dens[0])
    iv = [int(x * lcm) for x in v]
    g0 = 0
    for x in iv:
        g0 = sp.igcd(g0, x)
    if g0 > 1:
        iv = [x // g0 for x in iv]

    def poly(off):
        return sp.Poly(sum(iv[off + d] * n ** d for d in range(deg + 1)), n)

    Cpoly, Apoly, Bpoly = poly(0), poly(deg + 1), poly(2 * (deg + 1))
    # Normalise sign so the f_{n+1} leading coefficient is negative of a square (C = -(n+1)^2·k):
    if Cpoly.LC() > 0:
        Cpoly, Apoly, Bpoly = -Cpoly, -Apoly, -Bpoly
    return Cpoly, Apoly, Bpoly


def validate_recurrence(f, Cpoly, Apoly, Bpoly, n_val):
    """Check C(m) f_{m+1} + A(m) f_m + B(m) f_{m-1} == 0 for m = 1..n_val-2. Return first
    failing m or None."""
    n = sp.Symbol("n")
    for m in range(1, n_val - 1):
        val = (Cpoly.eval(m) * f[m + 1] + Apoly.eval(m) * f[m]
               + Bpoly.eval(m) * f[m - 1])
        if sp.nsimplify(val) != 0:
            return m
    return None


def sym2_operator_identity(bulk_A, bulk_B, partner_A_expr, partner_B_expr):
    """Symbolically verify L3 = Sym^2(L2) as differential operators over Q(z) — an ALL-n proof,
    not a finite-order check. Both operators are built in the theta = z d/dz basis from their
    recurrence polynomials: L = theta^order - z*A(theta) - z^2*B(theta+1). We convert L2 to monic
    d/dz form (a1, a0), form Sym^2 via the classical formula
        Sym^2(D^2 + a1 D + a0) = D^3 + 3a1 D^2 + (2a1^2 + a1' + 4a0) D + (4a0 a1 + 2a0'),
    convert L3 to monic d/dz form, and check all three coefficients are equal as rational
    functions of z. Returns (bool, collapse_identity_holds, detail)."""
    th = sp.Symbol("theta")
    z = sp.Symbol("z")

    def Pz(Lexpr, order):
        poly = sp.Poly(sp.expand(Lexpr), th)
        P = {j: sp.Integer(0) for j in range(order + 1)}
        for (j,), c in poly.terms():
            P[j] = sp.expand(c)
        return P

    # L2 = theta^2 - z A2(theta) - z^2 B2(theta+1)
    A2 = sp.sympify(str(partner_A_expr).replace("n", "theta"))
    B2 = sp.sympify(str(partner_B_expr).replace("n", "theta"))
    L2 = sp.expand(th**2 - z * A2 - z**2 * B2.subs(th, th + 1))
    P = Pz(L2, 2)
    collapse = sp.expand(z * sp.diff(P[2], z) - 2 * P[1]) == 0  # theta(P2) = 2 P1 (Deep Think)
    c2 = sp.expand(P[2] * z**2); c1 = sp.expand((P[2] + P[1]) * z); c0 = sp.expand(P[0])
    a1 = sp.cancel(c1 / c2); a0 = sp.cancel(c0 / c2)
    s_b2 = sp.cancel(3 * a1)
    s_b1 = sp.cancel(2 * a1**2 + sp.diff(a1, z) + 4 * a0)
    s_b0 = sp.cancel(4 * a0 * a1 + 2 * sp.diff(a0, z))

    # L3 = theta^3 - z A3(theta) - z^2 B3(theta+1), monic in d/dz
    A3 = sp.Poly(bulk_A.as_expr().subs(sp.Symbol("k"), th), th).as_expr()
    B3 = sp.Poly(bulk_B.as_expr().subs(sp.Symbol("k"), th), th).as_expr()
    L3 = sp.expand(th**3 - z * A3 - z**2 * B3.subs(th, th + 1))
    Q = Pz(L3, 3)
    d3 = sp.expand(Q[3] * z**3)
    d2 = sp.expand(3 * Q[3] * z**2 + Q[2] * z**2)
    d1 = sp.expand((Q[3] + Q[2] + Q[1]) * z)
    d0 = sp.expand(Q[0])
    l_b2 = sp.cancel(d2 / d3); l_b1 = sp.cancel(d1 / d3); l_b0 = sp.cancel(d0 / d3)

    eq2 = sp.simplify(s_b2 - l_b2) == 0
    eq1 = sp.simplify(s_b1 - l_b1) == 0
    eq0 = sp.simplify(s_b0 - l_b0) == 0
    detail = {"partner_operator_theta": {"P2": str(P[2]), "P1": str(P[1]), "P0": str(P[0])},
              "collapse_theta_P2_eq_2P1": bool(collapse),
              "sym2_minus_L3_monic": {"D2": str(sp.simplify(s_b2 - l_b2)),
                                      "D1": str(sp.simplify(s_b1 - l_b1)),
                                      "D0": str(sp.simplify(s_b0 - l_b0))}}
    return (eq2 and eq1 and eq0), bool(collapse), detail


def run_check(refs_path, bulk_id, n_fit=26, n_val=60, deg=2, mirror_order=14):
    refs_raw = Path(refs_path).read_bytes()
    refs_sha = hashlib.sha256(refs_raw).hexdigest()
    refs = json.loads(refs_raw)

    result = {
        "checker": "check_C3b_symsqrt.py",
        "checker_version": CHECKER_VERSION,
        "criterion": "C3b-symsqrt (constructive: L3 = Sym^2(L2); extract the order-2 partner)",
        "refs_file": str(refs_path),
        "refs_sha256": refs_sha,
        "bulk": bulk_id,
        "parameters": {"n_fit": n_fit, "n_val": n_val, "fit_degree": deg,
                       "mirror_order": mirror_order},
    }

    entry = refs["sequences"].get(bulk_id)
    if entry is None:
        result["verdict"] = "ERROR_UNKNOWN_SEQUENCE"
        return result, 2
    if entry.get("_meta_status") == "BLOCKED":
        result["verdict"] = "REFUSED_NO_DATA"
        result["error"] = "bulk entry is BLOCKED — transcribe from fetched sources first"
        return result, 2
    if entry["type"] != "order-3":
        result["verdict"] = "ERROR_BULK_NOT_ORDER3"
        return result, 2

    A3, B3, C3, mum3 = base.extract_recurrence_polys(entry["recurrence_python"], 3)
    g, integral3 = base.generate_sequence(A3, B3, C3, entry["initial_terms"], n_val)
    result["bulk_source"] = entry["source"]
    if not mum3:
        result["verdict"] = "FAIL_BULK_MUM"
        return result, 1

    # Extract the order-2 partner via series square root + holonomic fit.
    f = series_sqrt(g, n_val)
    fit = fit_order2_recurrence(f, n_fit, deg)
    if fit is None:
        result["verdict"] = "NOT_SYMMETRIC_SQUARE"
        result["evidence"] = {"sqrt_first_terms": [str(x) for x in f[:8]],
                              "reason": f"sqrt(g) has no order-2 recurrence of degree ≤ {deg} "
                                        f"(fit over n≤{n_fit})"}
        return result, 1
    Cpoly, Apoly, Bpoly = fit
    bad = validate_recurrence(f, Cpoly, Apoly, Bpoly, n_val)
    if bad is not None:
        result["verdict"] = "FIT_FAILED_VALIDATION"
        result["evidence"] = {"failing_n": bad, "validated_up_to": n_val}
        return result, 1

    n = sp.Symbol("n")
    mum2 = sp.expand(Cpoly.as_expr() + (n + 1) ** 2) == 0  # C(n) == -(n+1)^2
    partner_integral = all(x.denominator == 1 for x in f)

    # Build the partner recurrence string in the checker's a_{k+1} convention and confirm the
    # mirror map equals the bulk's (Sym² preserves it — the moduli map is the identity).
    # After sign-normalisation C(n) = -(n+1)^2, the relation -(n+1)^2 f_{n+1} + A f_n + B f_{n-1} = 0
    # gives a_{k+1} = (A·a_k + B·a_{k-1}) / (k+1)^2 with A, B taken directly.
    Aexpr = sp.expand(Apoly.as_expr())
    Bexpr = sp.expand(Bpoly.as_expr())
    k = sp.Symbol("k")
    rec_str = (f"(({str(Aexpr).replace('n','k')})*s[-1] + "
               f"({str(Bexpr).replace('n','k')})*s[-2])/((k+1)**2)")
    A2, B2, C2, _ = base.extract_recurrence_polys(rec_str, 2)
    f_init = [f[0], f[1]]
    a2, _ = base.generate_sequence(A2, B2, C2, f_init, mirror_order)
    ad2 = base.frobenius_derivative(A2, B2, C2, a2, mirror_order)
    z_l2 = base.mirror_map_z_of_q(a2, ad2, mirror_order)
    ad3 = base.frobenius_derivative(A3, B3, C3, g, mirror_order)
    z_l3 = base.mirror_map_z_of_q(g, ad3, mirror_order)
    mirror_match = z_l2 == z_l3

    result["partner_L2"] = {
        "recurrence": f"(n+1)^2 f(n+1) = ({Aexpr}) f(n) + ({Bexpr}) f(n-1)",
        "recurrence_python": rec_str,
        "initial_terms": [str(x) for x in f_init],
        "first_terms": [str(x) for x in f[:10]],
        "partner_is_integral": partner_integral,
        "B_coefficient_factored": str(sp.factor(Bexpr)),
    }
    # ALL-n operator-level proof: verify L3 = Sym^2(L2) symbolically over Q(z).
    op_identity, collapse_ok, op_detail = sym2_operator_identity(A3, B3, Aexpr, Bexpr)

    result["validation"] = {
        "sqrt_is_order2_holonomic": True,
        "recurrence_validated_to_n": n_val - 2,
        "partner_MUM": bool(mum2),
        "mirror_map_z_L2_eq_z_L3": bool(mirror_match),
        "mirror_map_order": mirror_order,
        "bulk_z_of_q": [str(x) for x in z_l3[:8]],
        "sym2_operator_identity_L3_eq_Sym2L2": bool(op_identity),
        "sym2_operator_detail": op_detail,
    }
    if mum2 and mirror_match and op_identity:
        result["verdict"] = ("SYM2_OPERATOR_IDENTITY_PROVEN(all-n symbolic; "
                             f"partner revalidated to n={n_val - 2}, mirror q^{mirror_order})")
        code = 0
    elif mum2 and mirror_match:
        # Partner is right to finite order but the symbolic operator identity did not close —
        # do not claim all-n; report the weaker finite-order verdict.
        result["verdict"] = f"SYM2_PARTNER_EXTRACTED(validated to n={n_val - 2}, mirror q^{mirror_order})"
        code = 0
    else:
        result["verdict"] = "FAIL_PARTNER_VALIDATION"
        code = 1
    return result, code


def main():
    ap = argparse.ArgumentParser(description="C3b constructive symmetric-square-root checker")
    ap.add_argument("--refs", default=str(REPO_ROOT / "refs" / "recurrences_v1.json"))
    ap.add_argument("--bulk", default="cooper_s7")
    ap.add_argument("--n-fit", type=int, default=26)
    ap.add_argument("--n-val", type=int, default=60)
    ap.add_argument("--deg", type=int, default=2)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    result, code = run_check(args.refs, args.bulk, n_fit=args.n_fit,
                             n_val=args.n_val, deg=args.deg)
    result["provenance"] = ("Generated-by: checkers/check_C3b_symsqrt.py "
                            f"v{CHECKER_VERSION} (Tier A computation, finite-order PASS) | "
                            "Verified-by: exact power-series sqrt + nullspace fit + "
                            "high-order revalidation + mirror-map equality | Reviewed-by: pending T0")
    payload = json.dumps(result, indent=2, sort_keys=True)
    out = args.out or str(REPO_ROOT / "data" / "certificates" / f"C3b_symsqrt_{args.bulk}.json")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(payload + "\n")
    print(payload)
    print(f"\ncertificate written: {out}", file=sys.stderr)
    sys.exit(code)


if __name__ == "__main__":
    main()
