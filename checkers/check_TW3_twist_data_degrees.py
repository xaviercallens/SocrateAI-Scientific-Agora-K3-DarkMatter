#!/usr/bin/env python3
"""check_TW3_twist_data_degrees.py -- WP-TW3 (opened by D32', 2026-10-10): the twist data of a twisted-Weierstrass model over
B3 = P^1 x P^2 with two E8 root fibres, as exact degree/divisibility arithmetic, plus the first gate (G2) it exposes.

WHAT IS SPECIFIED (decision D32', briefs/T0_DECISIONS_2026_10_07_STREAM2_DELEGATED.md)
  B3 = P^1 x P^2; D1 = {0} x P^2, D2 = {inf} x P^2 (class (1,0), disjoint); Weierstrass sections f in H^0(-4K), g in H^0(-6K)
  with vanishing orders (4,5) along D1 and D2:  f = s^4 t^4 f',  g = s^5 t^5 g',  f' in O(0,12), g' in O(2,18).
  In the t-line affine coordinate the fibre over y in P^2 is the pencil  Y^2 = X^3 + f'(y) t^4 X + t^5 (c(y) t^2 + b(y) t + a(y)),
  with f' in O(12), a, b, c in O(18) on P^2 (g' is a binary quadratic form in the P^1 coordinates with O(18) coefficients).

WHAT IS COMPUTED (all exact; no floats)
  1. K, the budgets and the residual classes, from the Chow ring of P^1 x P^2; compared with the TW1 certificate's margins.
  2. dim H^0 of the residual line bundles.
  3. The invariants of the pencil: alpha^3 = -f'^3/(27 a c), beta^2 = b^2/(4 a c) (derived by the scaling t -> mu t, X -> nu^2 X
     and VERIFIED here on exact rational instances).
  4. GATE G2 (necessary condition, then a construction): the K3 fibres are M_7-polarized iff (alpha^3, beta^2) =
     (pi(z), pi(z) - sigma(z) + 1) for a rational function z = u/v of P^2 (u, v forms of degree e), with sigma, pi read from
     INOSE_MODEL_M7.json. pi = c q^3 / (D0 z^8) and pi - sigma + 1 = c' R^2 / (D0 z^8) are factored from the certificate. The
     orders along the curves {u = 0}, {v = 0} and the fibres force ord(a c) >= 8 e on {u = 0} and >= 4 e on {v = 0}, so
     12 e <= deg(a c) = 36, i.e. e <= 3. For each e in 1..e_max an explicit (f', a, b, c) is built and the two invariant identities
     are verified EXACTLY as polynomial identities in y.

NOT CLAIMED: that the resulting Weierstrass threefold-fibration is smooth or minimal (gate G3); anything about a Calabi-Yau
fourfold, tadpole or Euler characteristic (ledger item 4, F5b stays); any Kodaira type (ledger items 3, 10: only vanishing orders
are used); anything physical.

Usage: python3 checkers/check_TW3_twist_data_degrees.py [--emit]
Controls: checkers/test_TW3_twist_data_degrees_controls.py
Generated-by: Claude (Sonnet 5.5, fork of Fable 5.1 session), Stream 2, 2026-10-10 | Verified-by: controls | Reviewed-by: N
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parent.parent
CERTS = REPO / "data" / "certificates"
OUT = CERTS / "TW3_TWIST_DATA_DEGREES.json"
z = sp.Symbol("z")
y0, y1, y2 = sp.symbols("y0 y1 y2")


class Refuse(RuntimeError):
    pass


# ---------------------------------------------------------------- Chow ring of P^1 x P^2 (classes (a, b) = a h1 + b h2)
DIMS = (1, 2)


def canonical(dims=DIMS):
    return tuple(-(n + 1) for n in dims)


def effective(cls):
    """effective = nef cone of a product of projective spaces: every coordinate >= 0."""
    return all(c >= 0 for c in cls)


def intersect_h(cls1, cls2):
    """product of two divisor classes in A^2(P^1 x P^2), as coefficients of (h1 h2, h2^2) (h1^2 = 0, h2^3 = 0)."""
    (a1, b1), (a2, b2) = cls1, cls2
    # h1^2 = 0 in A^*(P^1): that monomial is not a class of A^2 and carries no coefficient
    return {"h1h2": a1 * b2 + a2 * b1, "h2^2": b1 * b2}


def disjoint_necessary(cls1, cls2):
    """a necessary condition for D1 ∩ D2 = ∅: the product class vanishes in A^2."""
    p = intersect_h(cls1, cls2)
    return p["h1h2"] == 0 and p["h2^2"] == 0


def h0(cls):
    a, b = cls
    if a < 0 or b < 0:
        return 0
    return (a + 1) * ((b + 1) * (b + 2) // 2)


def budgets(d1, d2, orders=(4, 5, 10), dims=DIMS):
    K = canonical(dims)
    mK = tuple(-k for k in K)
    tot = (d1[0] + d2[0], d1[1] + d2[1])
    out = {}
    for name, mult, o in (("f", 4, orders[0]), ("g", 6, orders[1]), ("Delta", 12, orders[2])):
        bound = tuple(mult * k for k in mK)
        resid = tuple(bound[i] - o * tot[i] for i in range(2))
        out[name] = {"bound": bound, "need": tuple(o * tot[i] for i in range(2)), "residual": resid, "ok": effective(resid)}
    return out


# ---------------------------------------------------------------- the pencil invariants (derived, then verified)
def pencil_invariants(a, b, c, fp):
    """alpha^3 and beta^2 of  Y^2 = X^3 + fp t^4 X + t^5 (c t^2 + b t + a)  (the normal form is Y^2 = X^3 - 3 alpha t^4 X + t^5 (t^2 - 2 beta t + 1))."""
    return -fp ** 3 / (27 * a * c), b ** 2 / (4 * a * c)


def verify_invariant_derivation(trials=6):
    """exact: pick rational a, c with a/c a rational square (mu), solve nu^6 = a mu^5 over a rational perfect sixth power by
    construction, scale, and compare with the closed forms. Returns the number of exact agreements."""
    ok = 0
    for k in range(1, trials + 1):
        mu = Fr(k + 1, 3)
        nu = Fr(k + 2, 5)
        a = nu ** 6 / mu ** 5                    # makes  a mu^5 / nu^6 = 1
        c = a / mu ** 2                          # makes  c mu^7 / nu^6 = 1
        b = Fr(7 * k + 1, 11)
        fp = Fr(3 * k + 2, 7)
        # scaled pencil: Y^2 = X^3 + fp mu^4 nu^-4 t^4 X + t^5 (t^2 + (b mu^6/nu^6) t + 1)
        alpha_scaled = -(fp * mu ** 4 / nu ** 4) / 3
        beta_scaled = -(b * mu ** 6 / nu ** 6) / 2
        al3, be2 = pencil_invariants(a, b, c, fp)
        ok += int(alpha_scaled ** 3 == al3 and beta_scaled ** 2 == be2)
    return ok, trials


# ---------------------------------------------------------------- the M_7 side: orders of pi and pi - sigma + 1
def load_model():
    s3 = json.loads((CERTS / "INOSE_MODEL_M7.json").read_text())["result"]["S3"]
    sig = sp.sympify(s3["sigma_laurent"].replace("^", "**"))
    pi = sp.sympify(s3["pi_laurent"].replace("^", "**"))
    return sig, pi


def structure(F):
    """F(z) = c * N(z)^m ... / (D0 z^p): returns dict with the constant, the factor list of the numerator over Q, the pole
    order at 0 and the order at infinity."""
    n, d = sp.fraction(sp.together(F))
    n, d = sp.Poly(n, z), sp.Poly(d, z)
    if d.as_expr().subs(z, 0) != 0 or len(d.terms()) != 1:
        raise Refuse("denominator is not a monomial in z")
    const, facs = sp.factor_list(n.as_expr())
    p = d.degree()
    D0 = d.LC()
    return {"const": sp.Rational(const) / D0, "factors": [(sp.Poly(f, z), int(m)) for f, m in facs],
            "pole_order_at_0": int(p), "den_degree": int(p), "num_degree": int(n.degree()),
            "ord_at_infinity": int(p - n.degree())}


def order_conditions(pi_struct, w_struct):
    """Return (X, detail): the minimal sum of (ord_a + ord_c) over the special components, per unit of fibre degree e.
    For a component C where  alpha^3 = pi∘z  has order o_pi  and  beta^2 = W∘z  has order o_w:
        o_pi = 3 ord_f' - (ord_a + ord_c),  o_w = 2 ord_b - (ord_a + ord_c),  ord_f', ord_b >= 0, ord_a + ord_c >= 0.
    The minimal x = ord_a + ord_c solves x >= max(0, -o_pi, -o_w), x ≡ -o_pi (mod 3), x ≡ -o_w (mod 2)."""
    def minimal(o_pi, o_w):
        lo = max(0, -o_pi, -o_w)
        for x in range(lo, lo + 7):
            if (x + o_pi) % 3 == 0 and (x + o_w) % 2 == 0:
                return x
        raise Refuse("no x")
    detail = []
    X = 0
    # component z = 0:   pi and W both have a pole of order p
    x0 = minimal(-pi_struct["den_degree"] + 0, -w_struct["den_degree"] + 0)
    detail.append({"component": "z = 0", "o_pi": -pi_struct["den_degree"], "o_W": -w_struct["den_degree"], "x_min": x0})
    X += x0
    xi = minimal(pi_struct["ord_at_infinity"], w_struct["ord_at_infinity"])
    detail.append({"component": "z = infinity", "o_pi": pi_struct["ord_at_infinity"], "o_W": w_struct["ord_at_infinity"], "x_min": xi})
    X += xi
    # finite zeros of the numerators other than 0: each distinct complex root is its own component; the two functions can
    # share a root only if the factor lists share it (checked by gcd)
    gpi = sp.Poly(sp.prod([f.as_expr() for f, _ in pi_struct["factors"]]), z)
    gw = sp.Poly(sp.prod([f.as_expr() for f, _ in w_struct["factors"]]), z)
    if sp.gcd(gpi, gw).degree() > 0:
        raise Refuse("pi and W share a zero; the shared-root case is not handled")
    for struct, other, name in ((pi_struct, w_struct, "pi"), (w_struct, pi_struct, "W")):
        for f, m in struct["factors"]:
            if f.degree() == 0:
                continue
            x = minimal(m if name == "pi" else 0, m if name == "W" else 0)
            detail.append({"component": f"roots of a degree-{f.degree()} factor of the numerator of {name}",
                           "multiplicity": m, "n_roots": int(f.degree()), "x_min_per_root": x})
            X += x * f.degree()
    return X, detail


# ---------------------------------------------------------------- explicit construction for a given e
def form(deg, vars_=(y0, y1, y2), coeffs=None):
    """a fixed generic form of degree deg (deterministic coefficients) in 3 variables; deg 0 -> 1."""
    if deg == 0:
        return sp.Integer(1)
    mons = [y0 ** i * y1 ** j * y2 ** (deg - i - j) for i in range(deg + 1) for j in range(deg + 1 - i)]
    cs = coeffs or [1 + ((7 * k + 3 * deg) % 5) for k in range(len(mons))]
    return sp.Add(*[c * m for c, m in zip(cs, mons)])


def homog(poly_z, deg, u, v):
    """v^deg * poly(u / v) as a form."""
    p = sp.Poly(poly_z, z)
    return sp.expand(sum(c * u ** i * v ** (deg - i) for (i,), c in p.terms()))


def construct(e, pi_s, w_s, delta_budget=36):
    """explicit (f', a, b, c) of the divisibility structure for fibre degree e; raises Refuse if a degree is negative."""
    delta = (delta_budget - 12 * e) // 6 if (delta_budget - 12 * e) % 6 == 0 else None
    if delta is None or delta < 0:
        raise Refuse(f"e = {e}: deg(omega) = ({delta_budget} - 12 e)/6 is not a non-negative integer")
    if len(pi_s["factors"]) != 1 or pi_s["factors"][0][1] != 3 or pi_s["factors"][0][0].degree() != 2:
        raise Refuse("pi is not c q^3 / z^p with q quadratic")
    if len(w_s["factors"]) != 1 or w_s["factors"][0][1] != 2 or w_s["factors"][0][0].degree() != 4:
        raise Refuse("pi - sigma + 1 is not c' R^2 / z^p with R quartic")
    q, R = pi_s["factors"][0][0], w_s["factors"][0][0]
    u = form(e, coeffs=None)
    v = form(e, coeffs=[2 + ((5 * k + 1) % 4) for k in range(sp.binomial(e + 2, 2))])
    omega = form(delta, coeffs=None) if delta else sp.Integer(1)
    Q = homog(q.as_expr(), 2, u, v)
    Rt = homog(R.as_expr(), 4, u, v)
    c_pi = pi_s["const"]            # pi = c_pi q^3 / z^8 (absorbing 1/D0)
    c_w = w_s["const"]
    k0 = -1 / (27 * c_pi)           # ac = k0 u^8 v^4 omega^6 makes f' = Q v^2 omega^2 rational
    p_exp, v_exp = pi_s["den_degree"], 4
    if p_exp != 8:
        raise Refuse("pole order of pi at 0 is not 8; the closed form below is specific to the certificate's structure")
    ac_pol = k0 * u ** 8 * v ** v_exp * omega ** 6
    fp = Q * v ** 2 * omega ** 2
    b_sq_const = sp.Rational(-4) * c_w / (27 * c_pi)
    bb = v ** 2 * omega ** 3 * Rt            # b = sqrt(b_sq_const) * bb
    # split ac into a, c of degree 18 each: a = k0 u^p v^q omega^r , c = u^(8-p) v^(4-q) omega^(6-r)
    split = None
    for p, qv, r in itertools.product(range(0, 9), range(0, 5), range(0, 7)):
        if e * (p + qv) + delta * r == 18 and e * ((8 - p) + (4 - qv)) + delta * (6 - r) == 18:
            split = (p, qv, r)
            break
    if split is None:
        raise Refuse(f"e = {e}: no split of a c into two degree-18 forms of this shape")
    p, qv, r = split
    a = k0 * u ** p * v ** qv * omega ** r
    c = u ** (8 - p) * v ** (4 - qv) * omega ** (6 - r)
    return {"e": e, "delta": delta, "u": u, "v": v, "omega": omega, "Q": Q, "R": Rt, "f": fp, "a": a, "c": c, "bb": bb,
            "b_sq_const": b_sq_const, "split": split, "c_pi": c_pi, "c_w": c_w,
            "degrees": {"f'": 12, "a": e * (p + qv) + delta * r, "c": e * ((8 - p) + (4 - qv)) + delta * (6 - r),
                        "b": 2 * e + 3 * delta + 4 * e}}


def verify_construction(S):
    """alpha^3 = pi(z) and beta^2 = W(z) at z = u/v, as exact polynomial identities (cross-multiplied)."""
    u, v, Q, Rt, fp, a, c, bb = S["u"], S["v"], S["Q"], S["R"], S["f"], S["a"], S["c"], S["bb"]
    c_pi, c_w = S["c_pi"], S["c_w"]
    # alpha^3 = -f'^3 / (27 a c) ;  pi(z) = c_pi Q^3 v^2 / u^8   =>   -f'^3 u^8 == 27 a c * c_pi Q^3 v^2
    lhs1 = sp.expand(-fp ** 3 * u ** 8)
    rhs1 = sp.expand(27 * a * c * c_pi * Q ** 3 * v ** 2)
    # beta^2 = b^2 / (4 a c) with b^2 = b_sq_const * bb^2 ;  W(z) = c_w R^2 / u^8   =>   b_sq_const bb^2 u^8 == 4 a c c_w R^2
    lhs2 = sp.expand(S["b_sq_const"] * bb ** 2 * u ** 8)
    rhs2 = sp.expand(4 * a * c * c_w * Rt ** 2)
    return {"alpha3_identity": sp.expand(lhs1 - rhs1) == 0, "beta2_identity": sp.expand(lhs2 - rhs2) == 0}


def pull_back_check(S, pi, W, n_points=3):
    """independent numeric-exact cross-check: at rational points y, alpha^3 from the sections equals pi(z(y)); same for W."""
    ok = True
    for pt in [(1, 2, 3), (2, 5, 1), (3, 1, 7)][:n_points]:
        sub = {y0: pt[0], y1: pt[1], y2: pt[2]}
        uu, vv = S["u"].subs(sub), S["v"].subs(sub)
        zz = sp.Rational(uu, vv)
        al3 = -(S["f"].subs(sub)) ** 3 / (27 * S["a"].subs(sub) * S["c"].subs(sub))
        be2 = S["b_sq_const"] * S["bb"].subs(sub) ** 2 / (4 * S["a"].subs(sub) * S["c"].subs(sub))
        ok &= sp.simplify(al3 - pi.subs(z, zz)) == 0 and sp.simplify(be2 - W.subs(z, zz)) == 0
    return bool(ok)


def run(emit=False):
    tw1 = json.loads((CERTS / "TW1_two_e8_P1xP2.json").read_text())["result"]
    d1, d2 = (1, 0), (1, 0)
    K = canonical()
    if tuple(-k for k in K) != tuple(tw1["minus_K"]["value"]):
        raise Refuse("canonical class disagrees with the TW1 certificate")
    B = budgets(d1, d2)
    marg = {n: tuple(int(m) for m in tw1[f"budget_{n.lower() if n != 'Delta' else 'delta'}"]["margins"]) for n in ("f", "g", "Delta")}
    tw1_agree = all(B[n]["residual"] == marg[n] or (n == "Delta" and False) for n in ("f", "g")) and \
        B["Delta"]["residual"] == marg["Delta"]
    dims = {"f'": h0(B["f"]["residual"]), "g'": h0(B["g"]["residual"])}
    inv_ok, inv_n = verify_invariant_derivation()
    sig, pi = load_model()
    W = sp.together(pi - sig + 1)
    pi_s, w_s = structure(pi), structure(W)
    X, detail = order_conditions(pi_s, w_s)
    deg_ac = 2 * B["g"]["residual"][1]
    e_max = deg_ac // X
    builds = {}
    for e in range(1, e_max + 1):
        S = construct(e, pi_s, w_s)
        ver = verify_construction(S)
        builds[e] = {"delta_deg_omega": S["delta"], "split_a_c": S["split"], "section_degrees": S["degrees"],
                     "alpha3_identity_exact": ver["alpha3_identity"], "beta2_identity_exact": ver["beta2_identity"],
                     "pullback_points_agree": pull_back_check(S, pi, W)}
    e_fail = e_max + 1
    try:
        construct(e_fail, pi_s, w_s)
        fail_refused = False
    except Refuse:
        fail_refused = True
    res = {"base": "P^1 x P^2", "K": list(K), "D1": list(d1), "D2": list(d2),
           "disjoint_necessary_condition": disjoint_necessary(d1, d2),
           "budgets": {n: {"bound": list(v["bound"]), "need": list(v["need"]), "residual": list(v["residual"]), "ok": v["ok"]}
                       for n, v in B.items()},
           "tw1_margins_agree": bool(tw1_agree), "h0_residuals": dims,
           "invariant_derivation_exact_agreements": [inv_ok, inv_n],
           "pi": {"constant": str(pi_s["const"]), "numerator_factors": [[str(f.as_expr()), m] for f, m in pi_s["factors"]],
                  "pole_order_at_0": pi_s["den_degree"], "order_at_infinity": pi_s["ord_at_infinity"]},
           "W": {"constant": str(w_s["const"]), "numerator_factors": [[str(f.as_expr()), m] for f, m in w_s["factors"]],
                 "pole_order_at_0": w_s["den_degree"], "order_at_infinity": w_s["ord_at_infinity"]},
           "G2": {"sum_x_per_unit_e": X, "components": detail, "deg_ac": deg_ac, "e_max": e_max,
                  "condition": "e * sum_x <= deg(a c)", "constructions": {str(k): v for k, v in builds.items()},
                  "e_max_plus_1_refused": fail_refused}}
    ok = (res["disjoint_necessary_condition"] and all(v["ok"] for v in res["budgets"].values()) and tw1_agree and
          inv_ok == inv_n and all(b["alpha3_identity_exact"] and b["beta2_identity_exact"] and b["pullback_points_agree"]
                                  for b in builds.values()) and fail_refused and e_max >= 1)
    res["verdict"] = "TWIST_DATA_DEGREES_CONSISTENT; G2 NECESSARY CONDITION MET (constructions exact)" if ok else "FAIL"
    if emit and ok:
        cert = {"certificate": "TW3_TWIST_DATA_DEGREES", "work_package": "WP-TW3 (opened by D32', 2026-10-10)",
                "checker": "checkers/check_TW3_twist_data_degrees.py",
                "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "tier": "B (exact integer/rational arithmetic; pencil invariants derived and verified on exact instances; the "
                        "sigma, pi laurent series are INOSE_MODEL_M7.json's, Tier B)",
                "result": res,
                "not_claimed": ["that the Weierstrass fibration these sections define is smooth or minimal (gate G3)",
                                "anything about a Calabi-Yau fourfold, its Euler characteristic or a tadpole (ledger item 4; F5b stays)",
                                "any Kodaira type: only vanishing orders and root lattices are used (ledger items 3, 10)",
                                "that e in 1..e_max are the only maps z: P^2 -> P^1; only that these are the ones the degree budget allows "
                                "for this divisibility structure",
                                "anything physical"],
                "generated_by": "Claude (Sonnet 5.5, fork of Fable 5.1 session), Stream 2, 2026-10-10",
                "verified_by": "checkers/test_TW3_twist_data_degrees_controls.py", "reviewed_by": "N"}
        OUT.write_text(json.dumps(cert, indent=2, default=str) + "\n")
        print("wrote", OUT)
    return res, ok


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    res, ok = run(a.emit)
    print("K =", res["K"], "| residual f', g' classes:", res["budgets"]["f"]["residual"], res["budgets"]["g"]["residual"],
          "| h0:", res["h0_residuals"])
    print("G2: sum x per unit e =", res["G2"]["sum_x_per_unit_e"], "| deg(ac) =", res["G2"]["deg_ac"], "| e_max =", res["G2"]["e_max"])
    for e, b in res["G2"]["constructions"].items():
        print(f"  e = {e}: deg omega {b['delta_deg_omega']}, section degrees {b['section_degrees']}, "
              f"alpha^3 identity {b['alpha3_identity_exact']}, beta^2 identity {b['beta2_identity_exact']}, points {b['pullback_points_agree']}")
    print("verdict:", res["verdict"])
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refuse as ex:
        print("REFUSED:", ex)
        sys.exit(2)
