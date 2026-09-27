#!/usr/bin/env python3
"""
check_inose_fibration_multiplicities.py -- WP-GE10 step 2 (the part that needs no
Kodaira reading): discriminant-root multiplicities of the Inose elliptic fibration
on the M-polarized K3 X = Inose(E1 x E2), from a SOURCED Weierstrass equation, and
what happens when J(E1) = J(E2) -- in particular at the two singular loci of L3.

Source (fetched, hash-pinned, read -- docs/literature/MANIFEST.md 2026-09-27):
Kuwata-Shioda, arXiv:math/0609473 sec. 5.3: the type-J9 elliptic pencil on the
Kummer surface Km(E1 x E2), E_i : y^2 = x(x-1)(x-lambda_i), has Weierstrass form
    Y^2 = X^3 + (l1 l2 - 2 l1 - 2 l2 + 1) u (u-1)^2 X^2
              - (l1 + l2 - 1)(l1 l2 - l1 - l2) u^2 (u-1)^4 X
              - l1 l2 (l1 - 1)(l2 - 1) u^3 (u-1)^5                       (KS (5.x), l.1413-1415)
with discriminant u^6 (u-1)^10 d(u), deg d = 2, and
    disc(d) = 16 l1^2 l2^2 (l1-1)^2 (l2-1)^2 (l1^2-l1+1)^3 (l2^2-l2+1)^3    (KS l.1418).
KS Example 1.3: the degree-2 base change of this pencil is the elliptic K3 surface
with two II* fibres, i.e. the Inose surface X (Shioda-Inose partner of the Kummer).

What this checker does (all exact, sympy over Q(l1, l2)):
  T1  TRANSCRIPTION CHECK: recompute Delta from the transcribed equation and verify
      KS's two printed facts (the u^6 (u-1)^10 factorisation with deg d = 2, and the
      printed disc(d)). A transcription error fails here.
  T2  Base change u = s^2 and the twist X -> s^2 X, Y -> s^3 Y that makes the model
      minimal at s = 0 and s = infinity: coefficient degrees (4, 8, 12) in s, so the
      total space is a K3 (Weierstrass degrees), Delta_X(s) = (s^2-1)^10 d(s^2) of
      degree 24. Multiplicities of the roots of Delta_X are reported as ORDERS ONLY;
      no Kodaira label is attached (ledger item 3 reading is T0's, brief sec. 5).
  T3  Generic (l1, l2 independent): orders {10, 10, 1, 1, 1, 1} -- the four simple
      roots come from d(s^2), simple iff disc(d) != 0, d(0) != 0, d(1) != 0.
  T4  J1 = J2 (isomorphic curves, take l2 = l1 = l). FINDING (computed, not
      expected beforehand): d(0) = 0 IDENTICALLY, so d(u) = u e(u) with e linear,
      and after u = s^2 the two roots at +-sqrt(.) collapse onto the branch point
      s = 0: exactly ONE order-2 fibre appears there. Orders {10, 10, 2, 1, 1}
      (0 at infinity) for every l outside the finite exceptional set
      {lead(e) = 0, e(0) = 0, e(1) = 0}, computed explicitly.
  T5  The two singular loci of the s7 family (z = -1, D = -7; z = 1/27, D = -28)
      have J1 = J2 = J with J read from INOSE_MODEL_M7.json (sigma/2 at the locus):
      the degree-6 lambda-polynomial of that J shares no root with the exceptional
      set, so BOTH loci have orders {10, 10, 2, 1, 1}: one new order-2 fibre at
      each, no difference between the div-2 point z = -1 and the div-1 point
      z = 1/27 at the fibre level. GE-10's "A1 points merging at the div-2 locus"
      is NOT what this fibration shows; the second extra class of the rank-20
      surface (rank 19 -> 20) is not a fibre and must be a Mordell-Weil section.
  T6  The two special values: J = 0 (l^2 - l + 1 = 0; z = infinity of the s7
      family, E_omega x E_omega): orders {10, 10, 4}; J = 1 (l = -1; E_i x E_i):
      orders {10, 10, 2, 2} (one at infinity). Both computed exactly over the
      relevant field. (Read with Kodaira labels these are the external review's
      tables for X3 and X4 -- labels withheld here.)
  j(l) is COMPUTED from the Legendre cubic's Weierstrass invariants (c4^3 / Delta),
  never typed.

Not claimed: any Kodaira label; anything about cooper_s10; any physical reading.
Controls: checkers/test_inose_fibration_multiplicities_controls.py.

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: checkers/test_inose_fibration_multiplicities_controls.py | Reviewed-by: N
"""
import argparse
import hashlib
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parent.parent
AUDIT_DATE = "2026-09-27"

l1, l2, u, s, X, lam = sp.symbols("l1 l2 u s X lam")


class Refuse(Exception):
    pass


def chk(c, msg):
    if not c:
        raise Refuse(msg)


# ----------------------------------------------------------------------------
# Weierstrass invariants of y^2 = x^3 + a2 x^2 + a4 x + a6 (Silverman's b, c, Delta)
# ----------------------------------------------------------------------------
def invariants(a2, a4, a6):
    b2 = 4 * a2
    b4 = 2 * a4
    b6 = 4 * a6
    b8 = 4 * a2 * a6 - a4 ** 2          # b2 a6 - ... for a1 = a3 = 0: b8 = 4 a2 a6 - a4^2
    c4 = b2 ** 2 - 24 * b4
    c6 = -b2 ** 3 + 36 * b2 * b4 - 216 * b6
    delta = -b2 ** 2 * b8 - 8 * b4 ** 3 - 27 * b6 ** 2 + 9 * b2 * b4 * b6
    return sp.expand(c4), sp.expand(c6), sp.expand(delta)


def ks_j9(l1_, l2_):
    """KS (5.x) coefficients as polynomials in u (transcribed from lines 1413-1415)."""
    a2 = (l1_ * l2_ - 2 * l1_ - 2 * l2_ + 1) * u * (u - 1) ** 2
    a4 = -(l1_ + l2_ - 1) * (l1_ * l2_ - l1_ - l2_) * u ** 2 * (u - 1) ** 4
    a6 = -l1_ * l2_ * (l1_ - 1) * (l2_ - 1) * u ** 3 * (u - 1) ** 5
    return a2, a4, a6


def legendre_j(l_):
    """j of y^2 = x(x-1)(x-l) = x^3 - (1+l) x^2 + l x, computed from invariants."""
    c4, c6, delta = invariants(-(1 + l_), l_, 0)
    return sp.cancel(c4 ** 3 / delta)


def orders_of_roots(poly_in_s, var):
    """[(factor, multiplicity, degree)] over Q, plus the order at infinity given a
    target total degree."""
    P = sp.Poly(sp.expand(poly_in_s), var)
    out = []
    for fac, mult in sp.factor_list(P)[1]:
        fp = sp.Poly(fac, var)
        if fp.degree() > 0:
            out.append((str(fac), int(mult), fp.degree()))
    return out, P.degree()


def run(verbose=True):
    # ---- T1 transcription check
    a2, a4, a6 = ks_j9(l1, l2)
    c4, c6, delta = invariants(a2, a4, a6)
    D = sp.Poly(delta, u)
    q, r = sp.div(D, sp.Poly(u ** 6 * (u - 1) ** 10, u))
    chk(r.is_zero, "T1: u^6 (u-1)^10 does not divide Delta -- transcription error")
    d = q
    chk(d.degree() == 2, f"T1: deg d = {d.degree()} != 2 -- transcription error")
    # Convention: Silverman's Delta (used here) is 16 x the discriminant of the cubic
    # that KS use, so our d = 16 x their d and disc(d) = 256 x theirs. KS's printed
    # disc(d) is compared with disc(d/16); the factor is recorded, not hidden.
    dpoly = sp.expand(d.as_expr() / 16)
    disc_d = sp.discriminant(dpoly, u)
    printed = 16 * l1 ** 2 * l2 ** 2 * (l1 - 1) ** 2 * (l2 - 1) ** 2 * (l1 ** 2 - l1 + 1) ** 3 * (l2 ** 2 - l2 + 1) ** 3
    t1_disc_ok = sp.expand(disc_d - printed) == 0
    chk(t1_disc_ok, "T1: disc(d/16) differs from KS line 1418 -- transcription error")
    d0 = sp.factor(dpoly.subs(u, 0))
    d1 = sp.factor(dpoly.subs(u, 1))
    # ---- T2 base change and twist
    A2 = sp.expand(sp.cancel(a2.subs(u, s ** 2) / s ** 2))
    A4 = sp.expand(sp.cancel(a4.subs(u, s ** 2) / s ** 4))
    A6 = sp.expand(sp.cancel(a6.subs(u, s ** 2) / s ** 6))
    for nm, P_, dmax in (("a2", A2, 4), ("a4", A4, 8), ("a6", A6, 12)):
        chk(sp.Poly(P_, s).degree() <= dmax and sp.denom(sp.together(P_)) == 1, f"T2: {nm} not a polynomial of degree <= {dmax}")
    C4, C6, DX = invariants(A2, A4, A6)
    DXp = sp.Poly(DX, s)
    chk(DXp.degree() == 24, f"T2: deg Delta_X = {DXp.degree()} != 24")
    chk(sp.expand(DX - (s ** 2 - 1) ** 10 * 16 * dpoly.subs(u, s ** 2)) == 0, "T2: Delta_X != (s^2-1)^10 (16 d)(s^2)")
    # ---- T3 generic orders
    generic = {"orders_at_s_plus_minus_1": 10, "roots_of_d_of_s2": "4 simple iff disc(d) != 0, d(0) != 0",
               "order_at_infinity": 24 - 20 - 4}
    # ---- T4: l1 = l2 = lam.  FINDING: d(0) vanishes identically, so d(u) = u e(u) with
    # e linear; after u = s^2 the two simple roots at +-sqrt(root) collapse onto the
    # branch point s = 0: ONE fibre of order 2 appears there. The orders are
    # {10, 10, 2, 1, 1} (order 0 at infinity) unless lead(e) = 0 (the simple root goes
    # to infinity: order 2 there), e(0) = 0 (order 4 at s = 0) or e(1) = 0 (collision
    # with the order-10 fibres).
    disc_eq = sp.factor(disc_d.subs({l1: lam, l2: lam}))
    d0_eq = sp.factor(d0.subs({l1: lam, l2: lam}))
    d1_eq = sp.factor(d1.subs({l1: lam, l2: lam}))
    chk(d0_eq == 0, "T4: d(0) at l1 = l2 is not identically zero -- the analysis below assumes it")
    d_eq = sp.Poly(sp.expand(dpoly.subs({l1: lam, l2: lam})), u)
    e_eq, rem = sp.div(d_eq, sp.Poly(u, u))
    chk(rem.is_zero and e_eq.degree() == 1, "T4: d(u)/u at l1 = l2 is not linear")
    e_lead = sp.factor(e_eq.LC())
    e0 = sp.factor(e_eq.as_expr().subs(u, 0))
    e1 = sp.factor(e_eq.as_expr().subs(u, 1))
    jlam = legendre_j(lam)
    exc_prod = sp.expand(sp.numer(sp.together(e_lead * e0 * e1)))
    exceptional = sorted({str(fct) for fct, _ in sp.factor_list(exc_prod, lam)[1]})
    # ---- T5: our loci
    inose = json.loads((REPO / "data" / "certificates" / "INOSE_MODEL_M7.json").read_text())
    loci = {}
    for loc, v in inose["result"]["S4_model"]["at_loci"].items():
        Jval = sp.Rational(Fr(v["J_common_if_zero"]).numerator, Fr(v["J_common_if_zero"]).denominator)
        chk(Fr(v["sigma^2-4pi"]) == 0, f"T5: sigma^2 - 4 pi != 0 at z = {loc}")
        jv = 1728 * Jval
        # lambda polynomial for this j: numer(j(lam)) - jv * denom(j(lam))
        jn, jd = sp.fraction(sp.together(jlam))
        lampoly = sp.Poly(sp.expand(jn - jv * jd), lam)
        # does the lambda-polynomial share a root with the exceptional set?
        gcd = sp.gcd(lampoly.as_expr(), exc_prod)
        shares = sp.Poly(gcd, lam).degree() > 0
        loci[loc] = {"J": str(Jval), "j": str(jv), "lambda_polynomial_degree": lampoly.degree(),
                     "shares_root_with_exceptional_set": bool(shares),
                     "orders": None if shares else {"s=+1": 10, "s=-1": 10, "s=0": 2, "roots_of_e(s^2)": [1, 1], "s=infinity": 0}}
    t5_ok = all(not v["shares_root_with_exceptional_set"] for v in loci.values())
    # ---- T6: J = 0 and J = 1 (exact, over the needed field)
    special = {}
    for label, lval, field in (("J=0 (lam^2-lam+1=0)", None, "QQ<omega>"), ("J=1 (lam=-1)", sp.Integer(-1), "QQ")):
        if lval is None:
            om = sp.Symbol("om")
            # lam = -omega: lam^2 - lam + 1 = 0 ; work modulo that relation via extension
            K = sp.QQ.algebraic_field(sp.sqrt(-3))
            lam_val = (1 + sp.sqrt(-3)) / 2          # a root of lam^2 - lam + 1
        else:
            lam_val = lval
        Dspec = sp.expand(DX.subs({l1: lam_val, l2: lam_val}))
        Ps = sp.Poly(Dspec, s, extension=sp.sqrt(-3)) if lval is None else sp.Poly(Dspec, s)
        facs = sp.factor_list(Ps.as_expr(), s, extension=sp.sqrt(-3)) if lval is None else sp.factor_list(Ps.as_expr(), s)
        orders = []
        for fac, mult in facs[1]:
            fp = sp.Poly(fac, s, extension=sp.sqrt(-3)) if lval is None else sp.Poly(fac, s)
            if fp.degree() > 0:
                orders.append({"factor": str(fac), "order": int(mult), "degree": fp.degree()})
        deg = Ps.degree()
        special[label] = {"lambda": str(lam_val), "j": str(sp.simplify(legendre_j(lam_val))),
                          "orders_finite": orders, "order_at_infinity": 24 - deg}
    res = {
        "T1_transcription": {"delta_divisible_by_u6_um1_10": True, "deg_d": 2, "disc_d_matches_KS_line_1418": t1_disc_ok,
                             "convention": "Silverman Delta = 16 x KS cubic discriminant; d here = KS d (after /16)",
                             "d(u)": str(sp.factor(dpoly)), "d(0)": str(d0), "d(1)": str(d1)},
        "T2_K3_model": {"a2": str(A2), "a4": str(A4), "a6": str(A6), "Delta_X": "(s^2-1)^10 * d(s^2)", "deg_Delta_X": 24},
        "T3_generic_orders": generic,
        "T4_J1_eq_J2": {"disc_d_at_l1_eq_l2": str(disc_eq), "d0_at_l1_eq_l2": str(d0_eq), "d1_at_l1_eq_l2": str(d1_eq),
                        "e(u)=d(u)/u": str(e_eq.as_expr()), "lead_e": str(e_lead), "e(0)": str(e0), "e(1)": str(e1),
                        "exceptional_lambda_factors": exceptional,
                        "statement": "d(0) = 0 identically at l1 = l2: for lambda outside the exceptional factors the "
                                     "orders are {10, 10, 2, 1, 1} (order 0 at infinity) -- exactly ONE order-2 fibre "
                                     "appears, at the branch point s = 0; the extra algebraic class at J1 = J2 is "
                                     "that fibre"},
        "T5_s7_loci": loci, "T5_all_loci_generic_orders": t5_ok,
        "T6_special_values": special,
        "all_ok": bool(t1_disc_ok and t5_ok),
    }
    if verbose:
        print("  T1 transcription: Delta = u^6 (u-1)^10 d(u), deg d = 2, disc(d) = KS line 1418:", t1_disc_ok)
        print("     d(u) =", sp.factor(dpoly))
        print("  T2 K3 model degrees ok; Delta_X = (s^2-1)^10 d(s^2), degree 24")
        print("  T4 l1 = l2 = lam: d(0) = 0 identically; e(u) = d/u =", e_eq.as_expr())
        print("     lead(e) =", e_lead, "; e(0) =", e0, "; e(1) =", e1, "; exceptional lambda factors:", exceptional)
        for loc, v in loci.items():
            print(f"  T5 z={loc}: J = {v['J']}, lambda-poly degree {v['lambda_polynomial_degree']}, shares exceptional root: "
                  f"{v['shares_root_with_exceptional_set']} -> orders {v['orders']}")
        for k, v in special.items():
            print(f"  T6 {k}: orders {v['orders_finite']} ; order at infinity {v['order_at_infinity']}")
        print("  all_ok:", res["all_ok"])
    return res


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    try:
        res = run()
    except Refuse as e:
        print("REFUSED:", e)
        return 2
    if a.emit:
        cert = {
            "certificate": "INOSE_FIBRATION_MULTIPLICITIES", "checker": "checkers/check_inose_fibration_multiplicities.py",
            "checker_version": "1.0.0", "date": AUDIT_DATE, "tier": "B",
            "status": "RECORD, NOT A GATE. Discriminant-root ORDERS of the Inose elliptic fibration on X = Inose(E1 x E2), "
                      "from the Kuwata-Shioda J9 equation (transcription verified against their printed discriminant), "
                      "after the degree-2 base change they name. No Kodaira label is attached anywhere in this "
                      "certificate: whether such labels may be read off an explicit Weierstrass model is T0's reading "
                      "(briefs/WP_GE10_INOSE_MODEL_M7_2026_09_27.md sec. 5). The rho = 20 cut stays read narrowly (D7').",
            "claim": "At every point with J(E1) = J(E2) outside a finite explicit exceptional set -- in particular at "
                     "both singular loci of the s7 family, z = -1 (D = -7) and z = 1/27 (D = -28) -- the orders of the "
                     "discriminant roots are {10, 10, 2, 1, 1}: exactly one order-2 fibre appears (at the base-change "
                     "branch point), because d(0) vanishes identically when the two curves are isomorphic. The div-2 "
                     "and div-1 points are indistinguishable at the fibre level; the second extra class of the rank-20 "
                     "surface is not a fibre (GE-10, fibre-level question, answered for this fibration). Special values: "
                     "J = 0 -> {10, 10, 4}; J = 1 -> {10, 10, 2, 2}.",
            "tier_reason": "exact polynomial algebra on a sourced equation (Tier L, pinned); the link to the s7 loci is "
                           "through INOSE_MODEL_M7.json (Tier B: Hauptmodul identification).",
            "result": res,
            "inputs": {"sha256": {"docs/literature/arxiv_math_0609473.pdf": sha(REPO / "docs" / "literature" / "arxiv_math_0609473.pdf"),
                                  "data/certificates/INOSE_MODEL_M7.json": sha(REPO / "data" / "certificates" / "INOSE_MODEL_M7.json")}},
            "not_claimed": ["any Kodaira label", "the Mordell-Weil structure at the loci (not computed)",
                            "anything about cooper_s10", "any physical reading"],
            "controls": "checkers/test_inose_fibration_multiplicities_controls.py",
            "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: checkers/test_inose_fibration_multiplicities_controls.py | Reviewed-by: N",
        }
        out = REPO / "data" / "certificates" / "INOSE_FIBRATION_MULTIPLICITIES.json"
        out.write_text(json.dumps(cert, indent=2) + "\n")
        print("wrote", out)
    return 0 if res["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
