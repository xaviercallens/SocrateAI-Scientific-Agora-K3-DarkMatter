#!/usr/bin/env python3
"""check_TW2_section_descent.py -- WP-TW2 step 2b-ii: the section of the M_7-polarized K3 attached to the degree-7
isogeny phi (z = 1/27), built by Kumar-Kuwata Prop. 3.2 ((3.1)-(3.3)), descended to F^(1), and READ:
P.O, the A_1 contact, and the height h = 2 chi + 2 P.O - contr -- all computed here, none asserted.

Inputs (rule 4: each verified to exist before this script was written)
  * the curve E1 : y^2 = x^3 + A x + B (j read from INOSE_FIBRATION_MULTIPLICITIES.json, locus 1/27),
    kernel cubic h and Velu isogeny phi: E1 -> E2 = (A2, B2) from check_TW2_sqrt_m7_endomorphism.py (step 2b-i);
  * Kumar-Kuwata arXiv:1409.2931 (pinned: docs/literature/kumar_kuwata_1409.2931.txt) sec. 3.1 l.460-548
    ((3.1) cubic C_t, (3.2)-(3.3) divisors D+-, Prop. 3.2) and (2.8) l.427-447 for the Weierstrass form of F^(n).

Method (exact; Fractions throughout, no floats)
  1. C_t : x2^3 + c x2 + d = t^6 (x1^3 + a x1 + b), (a,b) = E1, (c,d) = E2, origin O = (1 : t^2 : 0).
     With s = x2 - t^2 x1 it is a quadratic in x1; its discriminant gives a quartic w^2 = Delta(s) with the
     rational point O = (s,w) = (0, q), q = a t^6 - c t^2; Mordell's quartic -> Weierstrass map gives E_t.
     The map is VERIFIED by identity on the actual divisor points (an exact check in the residue field).
  2. D+- : the 9 points (x1, phi_x(x1)) with phi_y(x1) = +- t^3 (roots of Pn - (+-t^3) h^3, degree 9 = (3d-3)/2).
     Q+- is found by Riemann-Roch: the unique g in L(10 O_W) vanishing on D+- has one more zero R, Q = -R.
  3. P(t) = Q+ - Q- on E_t, mapped to the short Weierstrass form of F^(6)_t (invariants compared: j must agree),
     then t1 = t^6 gives F^(1); X(t1) is reconstructed as a rational function from many exact specializations and
     checked on held-out points.
  4. Read: pole structure of X (=> P.O), the A_1 fibre at t1 = 1 (=> contr), h.

NOT CLAIMED: any Kodaira label (ledger items 3, 10): the A_1 root fibre is the root lattice of step 2a, here only its
contact with the section is computed; nothing physical (the K3 is a model surface, ledger item 4).

Usage: python3 checkers/check_TW2_section_descent.py [--points N] [--emit]
Controls: checkers/test_TW2_section_descent_controls.py
Generated-by: Claude (Fable 5.1), Stream 2, 2026-10-10 | Verified-by: controls; identity checks inline | Reviewed-by: N
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_TW2_sqrt_m7_endomorphism as endo  # noqa: E402

REPO = HERE.parent
CERTS = REPO / "data" / "certificates"
OUT = CERTS / "TW2_SECTION_DESCENT.json"
x_ = sp.Symbol("x")


class Refuse(RuntimeError):
    pass


# ------------------------------------------------------------------ polynomials over Q (lists, low -> high)
def ptrim(p):
    while p and p[-1] == 0:
        p = p[:-1]
    return p


def padd(a, b):
    n = max(len(a), len(b))
    return ptrim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def pneg(a):
    return [-c for c in a]


def pmul(a, b):
    if not a or not b:
        return []
    r = [Fr(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] += ai * bj
    return ptrim(r)


def pdivmod(a, b):
    a, q = list(a), []
    if not b:
        raise ZeroDivisionError
    q = [Fr(0)] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b) and a:
        c = a[-1] / b[-1]
        k = len(a) - len(b)
        q[k] = c
        a = ptrim([a[i] - (c * b[i - k] if 0 <= i - k < len(b) else 0) for i in range(len(a))])
    return ptrim(q), a


def peval(p, v):
    r = Fr(0)
    for c in reversed(p):
        r = r * v + c
    return r


def pscale(p, s):
    return ptrim([c * s for c in p])


# ------------------------------------------------------------------ residue field K = Q[theta]/H
class Field:
    def __init__(self, H):
        self.H = [Fr(c) for c in H]
        self.H = pscale(self.H, 1 / self.H[-1])
        self.n = len(self.H) - 1

    def red(self, a):
        return pdivmod(a, self.H)[1]

    def const(self, c):
        return ptrim([Fr(c)])

    def mul(self, a, b):
        return self.red(pmul(a, b))

    def inv(self, a):
        # extended Euclid on (a, H)
        r0, r1 = list(self.H), self.red(a)
        s0, s1 = [], [Fr(1)]
        while r1:
            q, r = pdivmod(r0, r1)
            r0, r1 = r1, r
            s0, s1 = s1, padd(s0, pneg(pmul(q, s1)))
        if len(r0) != 1:
            raise Refuse("element not invertible in the residue field (H not squarefree or zero divisor)")
        return self.red(pscale(s0, 1 / r0[0]))

    def pw(self, a, k):
        r = self.const(1)
        for _ in range(k):
            r = self.mul(r, a)
        return r

    def horner(self, p, a):
        r = []
        for c in reversed(p):
            r = self.red(padd(pmul(r, a), [Fr(c)])) if r else self.red([Fr(c)])
        return r

    def is_zero(self, a):
        return not self.red(a)


# ------------------------------------------------------------------ Weierstrass (generalized) over Q
def w_invariants(a1, a2, a3, a4, a6):
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    c4 = b2 * b2 - 24 * b4
    c6 = -b2 ** 3 + 36 * b2 * b4 - 216 * b6
    return b2, c4, c6


def on_curve(a, P):
    a1, a2, a3, a4, a6 = a
    X, Y = P
    return Y * Y + a1 * X * Y + a3 * Y == X ** 3 + a2 * X * X + a4 * X + a6


def w_neg(a, P):
    if P is None:
        return None
    a1, _, a3, _, _ = a
    return (P[0], -P[1] - a1 * P[0] - a3)


def w_add(a, P, Q):
    a1, a2, a3, a4, a6 = a
    if P is None:
        return Q
    if Q is None:
        return P
    if P[0] == Q[0]:
        if P[1] + Q[1] + a1 * Q[0] + a3 == 0:
            return None
        lam = (3 * P[0] ** 2 + 2 * a2 * P[0] + a4 - a1 * P[1]) / (2 * P[1] + a1 * P[0] + a3)
    else:
        lam = (Q[1] - P[1]) / (Q[0] - P[0])
    nu = P[1] - lam * P[0]
    x3 = lam * lam + a1 * lam - a2 - P[0] - Q[0]
    y3 = -(lam + a1) * x3 - nu - a3
    return (x3, y3)


# ------------------------------------------------------------------ the construction
def ingredients(j=None):
    j = endo.read_j() if j is None else j
    A, B = endo.model_from_j(j)
    psi = endo.division_polys(7, A, B)
    h = endo.kernel_cubic(psi[7])
    phi_x, (A2, B2) = endo.velu(A, B, h)
    num, den = sp.fraction(phi_x)
    dphi = sp.cancel(sp.diff(phi_x, x_))
    Pn, Pd = sp.fraction(dphi)
    f1 = x_ ** 3 + A * x_ + B
    if sp.cancel(dphi ** 2 * f1 - (phi_x ** 3 + A2 * phi_x + B2)) != 0:
        raise Refuse("Velu normalization: phi_x'^2 f1 != phi_x^3 + A2 phi_x + B2 (the y-map is not phi_x')")
    cvt = lambda e: [Fr(int(sp.Rational(c).p), int(sp.Rational(c).q)) for c in sp.Poly(e, x_).all_coeffs()[::-1]]
    return {"j": j, "A": int(A), "B": int(B), "A2": int(A2), "B2": int(B2), "h": cvt(h.as_expr()),
            "num": cvt(num), "den": cvt(den), "Pn": cvt(Pn), "Pd": cvt(Pd)}


def quartic(t, a, b, c, d):
    """w^2 = Delta(s) = -3 t^4 s^4 + 0 s^3 + c2 s^2 + c1 s + (c t^2 - a t^6)^2   (derived in the module docstring)."""
    r = c * t ** 2 - a * t ** 6
    return {"a4": -3 * t ** 4, "a3": Fr(0), "a2": 6 * t ** 2 * r - 12 * t ** 4 * c, "a1": -12 * t ** 4 * (d - t ** 6 * b),
            "a0": r * r, "q": -r}


def mordell(qd):
    q = qd["q"]
    if q == 0:
        raise Refuse("q = 0: choose another t")
    c2, c1, a4, a3 = qd["a2"], qd["a1"], qd["a4"], qd["a3"]
    return (c1 / q, c2 - c1 * c1 / (4 * q * q), 2 * q * a3, -4 * q * q * a4,
            (c2 - c1 * c1 / (4 * q * q)) * (-4 * q * q * a4))


def divisor_points(ing, t0, sign, F):
    """the 9 points of D^sign as elements of K = Q[theta]/H, in Weierstrass coordinates of E_t."""
    a, b, c, d = ing["A"], ing["B"], ing["A2"], ing["B2"]
    t = Fr(t0)
    qd = quartic(t, Fr(a), Fr(b), Fr(c), Fr(d))
    wa = mordell(qd)
    th = [Fr(0), Fr(1)]
    xn = F.horner(ing["num"], th)
    xd = F.horner(ing["den"], th)
    x2 = F.mul(xn, F.inv(xd))
    s = F.red(padd(x2, pneg(pscale(th, t ** 2))))
    r = c * t ** 2 - a * t ** 6
    w = F.red(padd(pscale(F.mul(s, th), 6 * t ** 4), padd(pscale(F.mul(s, s), 3 * t ** 2), [Fr(r)])))
    # quartic identity in K: w^2 == Delta(s)   (this validates (3.1) and the derivation of Delta)
    s2 = F.mul(s, s)
    Delta = F.red(padd(padd(pscale(F.mul(s2, s2), qd["a4"]), pscale(s2, qd["a2"])), padd(pscale(s, qd["a1"]), [qd["a0"]])))
    if not F.is_zero(padd(F.mul(w, w), pneg(Delta))):
        raise Refuse("w^2 != Delta(s) on the divisor: the cubic (3.1) reduction is wrong")
    # Mordell: x = (2q(v+q) + c1 u)/u^2 ; y = (4q^2(v+q) + 2q(c1 u + c2 u^2) - (c1^2/(2q)) u^2)/u^3
    q, c1, c2 = qd["q"], qd["a1"], qd["a2"]
    si = F.inv(s)
    si2 = F.mul(si, si)
    vq = F.red(padd(w, [Fr(q)]))
    X = F.mul(padd(pscale(vq, 2 * q), pscale(s, c1)) if True else None, si2)
    Y = F.mul(F.red(padd(padd(pscale(vq, 4 * q * q), pscale(padd(pscale(s, c1), pscale(s2, c2)), 2 * q)),
                         pscale(s2, -(c1 * c1) / (2 * q)))), F.mul(si2, si))
    return wa, X, Y


def check_on_curve_K(F, wa, X, Y):
    a1, a2, a3, a4, a6 = [Fr(v) for v in wa]
    lhs = F.red(padd(F.mul(Y, Y), padd(pscale(F.mul(X, Y), a1), pscale(Y, a3))))
    X2 = F.mul(X, X)
    rhs = F.red(padd(F.mul(X2, X), padd(pscale(X2, a2), padd(pscale(X, a4), [a6]))))
    return F.is_zero(padd(lhs, pneg(rhs)))


def residual_point(F, wa, X, Y):
    """Riemann-Roch: g in L(10 O) vanishing on the 9 conjugate points; its 10th zero R; returns R as a rational point."""
    a1, a2, a3, a4, a6 = [Fr(v) for v in wa]
    cols = []
    xp = F.const(1)
    xs = []
    for i in range(6):
        xs.append(xp)
        xp = F.mul(xp, X)
    funcs = [("x", i, xs[i]) for i in range(6)] + [("y", j, F.mul(xs[j], Y)) for j in range(4)]
    n = F.n
    M = sp.zeros(n, len(funcs))
    for c, (_, _, vec) in enumerate(funcs):
        vec = vec + [Fr(0)] * (n - len(vec))
        for r in range(n):
            M[r, c] = sp.Rational(vec[r].numerator, vec[r].denominator)
    ns = M.nullspace()
    if len(ns) != 1:
        raise Refuse(f"L(10 O) vanishing space has dimension {len(ns)}, expected 1")
    coef = ns[0]
    den = sp.ilcm(*[sp.fraction(sp.nsimplify(c))[1] for c in coef])
    cf = [Fr(int(c * den)) for c in coef]
    u = ptrim([cf[i] for i in range(6)])
    v = ptrim([cf[6 + j] for j in range(4)])
    f = [Fr(a6), Fr(a4), Fr(a2), Fr(1)]
    ax = [Fr(a3), Fr(a1)]
    Nx = padd(padd(pmul(u, u), pneg(pmul(pmul(ax, u), v))), pneg(pmul(pmul(v, v), f)))      # u^2 - (a1x+a3)uv - f v^2
    # minimal polynomial of X over Q: char poly of multiplication by X on K
    cols_ = []
    for k in range(n):
        e = [Fr(0)] * k + [Fr(1)]
        cols_.append(F.mul(X, e) + [Fr(0)] * n)
    Mx = sp.Matrix(n, n, lambda r, c: sp.Rational(cols_[c][r].numerator, cols_[c][r].denominator))
    cp = sp.Poly(Mx.charpoly(x_).as_expr(), x_).all_coeffs()[::-1]
    Nm = [Fr(int(sp.Rational(c).p), int(sp.Rational(c).q)) for c in cp]
    qd_, rem = pdivmod(Nx, Nm)
    if rem or len(qd_) != 2:
        raise Refuse(f"norm identity failed: quotient degree {len(qd_) - 1}, remainder degree {len(rem) - 1}")
    XR = -qd_[0] / qd_[1]
    vR = peval(v, XR)
    if vR == 0:
        raise Refuse("v(X_R) = 0: residual point is 2-torsion or degenerate")
    YR = -peval(u, XR) / vR
    if not on_curve((a1, a2, a3, a4, a6), (XR, YR)):
        raise Refuse("the residual point is not on E_t")
    return (XR, YR)


def section_at(ing, t0):
    t0 = Fr(t0)
    pts = {}
    wa = None
    for sign in (+1, -1):
        H = padd(ing["Pn"], pneg(pscale(pmul(pmul(ing["h"], ing["h"]), ing["h"]), sign * t0 ** 3)))
        if len(H) - 1 != 9:
            raise Refuse(f"degree of H is {len(H) - 1}, expected 9")
        F = Field(H)
        wa, Xk, Yk = divisor_points(ing, t0, sign, F)
        if not check_on_curve_K(F, wa, Xk, Yk):
            raise Refuse("Mordell transform: divisor point not on the Weierstrass cubic (formula wrong)")
        R = residual_point(F, wa, Xk, Yk)
        pts[sign] = w_neg(tuple(Fr(v) for v in wa), R)         # Q = -R
    a = tuple(Fr(v) for v in wa)
    P = w_add(a, pts[+1], w_neg(a, pts[-1]))
    return a, pts, P


def simple_form(ing, branch=1):
    """KK sec. 2 (l.296-303) simple normal form  Y^2 = X^3 - 3 alpha X + t_s + 1/t_s - 2 beta  with
    alpha = (J1 J2)^(1/3), beta = 1 - J (the branch that puts the A_1 node at t_s = 1), J = j/1728.
    The relation t_s = kappa * t^6 (t = KK's t_6) is computed, not typed: kappa = -sqrt(Delta_E1 / Delta_E2) (perfect square),
    and the exact j-match of E_t with this form is ASSERTED at every specialization (to_F1)."""
    J = Fr(ing["j"], 1728)
    n, d = J.numerator ** 2, J.denominator ** 2
    cube = lambda v: round(abs(v) ** (1 / 3))
    an, ad = cube(n), cube(d)
    if an ** 3 != n or ad ** 3 != d:
        raise Refuse("(J1 J2)^(1/3) is not rational at this locus")
    alpha = Fr(an, ad)
    D1 = -16 * (4 * ing["A"] ** 3 + 27 * ing["B"] ** 2)
    D2 = -16 * (4 * ing["A2"] ** 3 + 27 * ing["B2"] ** 2)
    r = Fr(D1, D2)
    sn, sd = sp.integer_nthroot(r.numerator, 2), sp.integer_nthroot(r.denominator, 2)
    if not (sn[1] and sd[1]):
        raise Refuse("Delta_E1 / Delta_E2 is not a rational square")
    if branch not in (1, -1):
        raise Refuse("branch must be +1 or -1")
    # the two branches (beta = J-1, kappa > 0) and (beta = 1-J, kappa < 0) both match j(E_t) exactly (j is twist-blind); they
    # differ by the quadratic twist by -1. Branch +1 is the default: on it the section is defined over Q (square class +1).
    kappa = branch * Fr(int(sn[0]), int(sd[0]))
    return {"J": J, "alpha": alpha, "beta": branch * (J - 1), "kappa": kappa, "branch": branch}


def to_F1(ing, t0, a, P, sf):
    """map P on E_t0 (Mordell model) to the integral model Y'^2 = X'^3 - 3 alpha t^4 X' + t^5 (t^2 - 2 beta t + 1) of F^(1)
    at t = t_s = kappa t0^6; returns (t_s, X', matched) with matched = exact j-match AND u^4 = alpha'/alpha (twist constant)."""
    b2, c4, c6 = w_invariants(*a)
    alpha_, beta_ = -c4 / 48, -c6 / 864
    Xs = P[0] + b2 / 12
    ts = sf["kappa"] * Fr(t0) ** 6
    al2, be2 = -3 * sf["alpha"], ts + 1 / ts - 2 * sf["beta"]
    if alpha_ == 0 or beta_ == 0 or al2 == 0 or be2 == 0:
        raise Refuse("degenerate short model (j = 0 or 1728 at this t)")
    jm = (alpha_ ** 3 * (4 * al2 ** 3 + 27 * be2 ** 2) == al2 ** 3 * (4 * alpha_ ** 3 + 27 * beta_ ** 2))
    u2 = (be2 / beta_) / (al2 / alpha_)
    ok4 = (u2 * u2 == al2 / alpha_)
    return ts, (ts ** 2) * u2 * Xs, bool(jm and ok4), u2


def reconstruct(samples, dn, dd):
    """X(t1) = N/D with deg N <= dn, deg D <= dd from exact samples [(t1, X)] by nullspace; None if not unique."""
    rows = []
    for t1, X in samples:
        rows.append([sp.Rational(t1.numerator, t1.denominator) ** i for i in range(dn + 1)] +
                    [-sp.Rational(X.numerator, X.denominator) * sp.Rational(t1.numerator, t1.denominator) ** i for i in range(dd + 1)])
    M = sp.Matrix(rows)
    ns = M.nullspace()
    return ns


def read_section(ing, sf, npts):
    """specialize at npts rational t, reconstruct X'(t_s) = N / D^2, read P.O and the contact at the node t_s = 1."""
    samples, twists = [], []
    t0s = [Fr(k, 1) for k in range(2, 2 + npts)]
    for t0 in t0s:
        a, pts, P = section_at(ing, t0)
        ts, X1, ok, u2 = to_F1(ing, t0, a, P, sf)
        if not ok:
            raise Refuse(f"t0 = {t0}: E_t0 is not isomorphic to the simple form up to a constant twist (j or u^4 mismatch)")
        samples.append((ts, X1))
        twists.append(u2)
    return t0s, samples, twists


def fit(samples, dn, dd):
    rows = [[sp.Rational(t.numerator, t.denominator) ** i for i in range(dn + 1)] +
            [-sp.Rational(X.numerator, X.denominator) * sp.Rational(t.numerator, t.denominator) ** i for i in range(dd + 1)]
            for t, X in samples]
    return sp.Matrix(rows).nullspace()


tt = sp.Symbol("t")


def rational_from_null(v, dn, dd):
    N = sum(v[i] * tt ** i for i in range(dn + 1))
    Dp = sum(v[dn + 1 + i] * tt ** i for i in range(dd + 1))
    g = sp.gcd(sp.Poly(N, tt), sp.Poly(Dp, tt)).as_expr()
    return sp.cancel(N / g), sp.cancel(Dp / g)


def _rat(fr):
    return sp.Rational(fr.numerator, fr.denominator)


def read_off(N, Dp, sf, chi=2):
    """P.O, the A_1 contact and the height from the reconstructed X'(t) = N/Dp on
    Y^2 = X^3 - 3 alpha t^4 X + t^5 (t^2 - 2 beta t + 1)  (weight 4/6: X_inf = s^4 X', s = 1/t)."""
    alpha, beta = _rat(sf["alpha"]), _rat(sf["beta"])
    Nn, Dn = sp.Poly(N, tt), sp.Poly(Dp, tt)
    fl = sp.factor_list(Dp)[1]
    if any(m % 2 for _, m in fl):
        raise Refuse("denominator of X' is not a square: odd-order pole, so X' is not a section's x-coordinate")
    PO_fin = sum(sp.degree(f, tt) * (m // 2) for f, m in fl)             # a pole of order 2m at a finite t contributes m
    pole0 = Dn.eval(0) == 0
    excess = Nn.degree() - Dn.degree() - 4                                # pole at infinity iff > 0
    pole_inf = excess > 0
    PO = PO_fin + (excess // 2 if pole_inf else 0)
    # the A_1 node: the unique multiplicity-2 linear factor of the discriminant (computed, not typed)
    a4_, a6_ = -3 * alpha * tt ** 4, tt ** 5 * (tt ** 2 - 2 * beta * tt + 1)
    nodes = [f for f, m in sp.factor_list(sp.expand(-16 * (4 * a4_ ** 3 + 27 * a6_ ** 2)))[1] if m == 2 and sp.degree(f, tt) == 1]
    if len(nodes) != 1:
        raise Refuse(f"expected exactly one double linear factor of the discriminant, found {len(nodes)}")
    r = sp.solve(nodes[0], tt)[0]
    Dat1 = Dn.eval(r)
    if Dat1 == 0:
        contr, contact = sp.Integer(0), f"P meets O inside the A_1 fibre (pole of X' at t = {r}), hence the identity component"
    else:
        X1 = sp.Rational(Nn.eval(r)) / sp.Rational(Dat1)
        cub = X1 ** 3 - 3 * alpha * X1 + (r + 1 / r - 2 * beta)           # the fibre cubic at the node
        dcub = 3 * X1 ** 2 - 3 * alpha
        if cub == 0 and dcub == 0:
            contr, contact = sp.Rational(1, 2), "P passes through the node: non-identity component"
        else:
            contr, contact = sp.Integer(0), "P meets the identity component away from the node"
    h = 2 * chi + 2 * PO - contr
    return {"P_dot_O": int(PO), "contr_A1": str(contr), "contact_reading": contact, "height": str(h),
            "pole_at_t0": bool(pole0), "pole_at_infinity": bool(pole_inf),
            "poles_finite": [str(f) + "^" + str(m) for f, m in fl]}


def disc_orders(sf):
    alpha, beta = _rat(sf["alpha"]), _rat(sf["beta"])
    a4, a6 = -3 * alpha * tt ** 4, tt ** 5 * (tt ** 2 - 2 * beta * tt + 1)
    Dl = sp.expand(-16 * (4 * a4 ** 3 + 27 * a6 ** 2))
    fl = sp.factor_list(Dl)[1]
    orders = []
    for f, m in fl:
        orders += [int(m)] * int(sp.degree(f, tt))
    inf = 24 - sum(orders)
    return sorted(orders + ([inf] if inf else []), reverse=True)


def y_square_check(N, Dp, sf):
    """Y'^2 = X'^3 - 3 alpha t^4 X' + t^5 (...) is (constant) * (square) in Q(t): every multiplicity of the numerator is even."""
    alpha, beta = _rat(sf["alpha"]), _rat(sf["beta"])
    num = sp.expand(N ** 3 - 3 * alpha * tt ** 4 * N * Dp ** 2 + tt ** 5 * (tt ** 2 - 2 * beta * tt + 1) * Dp ** 3)
    c, fl = sp.factor_list(num)
    c = sp.Rational(c)
    n = abs(c.p * c.q)                                                    # square class of c = sign * (p q) mod squares
    sqf = 1
    for pr, e in sp.factorint(n).items():
        sqf *= pr ** (e % 2)
    sqf = int(sqf) * (1 if c > 0 else -1)
    return {"all_multiplicities_even": all(m % 2 == 0 for _, m in fl), "constant": str(c),
            "square_class_of_constant": sqf,
            "reading": "Y' lies in Q(sqrt(square_class)) * Q(t); a square class of 1 means the section is defined over Q"}


def run(npts=44, held=8, dn=14, dd=10, ing=None, transform=None, branch=1):
    ing = ing or ingredients()
    sf = simple_form(ing, branch)
    t0s, samples, twists = read_section(ing, sf, npts + held) if transform is None else transform(ing, sf, npts + held)
    fit_s, held_s = samples[:npts], samples[npts:]
    ns = fit(fit_s, dn, dd)
    out = {"j": str(ing["j"]), "E1": [ing["A"], ing["B"]], "E2": [ing["A2"], ing["B2"]],
           "alpha": str(sf["alpha"]), "beta": str(sf["beta"]), "kappa": str(sf["kappa"]), "branch": sf["branch"],
           "n_fit_points": npts, "n_unknowns": dn + dd + 2, "nullspace_dim": len(ns), "n_heldout": len(held_s)}
    if len(ns) != 1:
        out["verdict"] = f"NOT_DETERMINED (nullspace dimension {len(ns)})"
        return out
    N, Dp = rational_from_null(ns[0], dn, dd)
    ok_held = all(_rat(X) * Dp.subs(tt, _rat(t)) == N.subs(tt, _rat(t)) for t, X in held_s)
    a, _, P = section_at(ing, Fr(3))
    a2, _, P2 = section_at(ing, Fr(-3))
    # t -> -t swaps D+ and D- (the sign of t^3 flips), so P(-t) = -P(t): same X, opposite Y on the same Weierstrass curve
    sym = bool(P2[0] == P[0] and P2 in (P, w_neg(a, P)))
    ro = read_off(N, Dp, sf)
    out.update({"X_numerator": str(sp.expand(N)), "X_denominator": str(sp.expand(Dp)), "deg_N": int(sp.degree(N, tt)),
                "deg_D2": int(sp.degree(Dp, tt)), "heldout_agree": bool(ok_held), "t_to_minus_t_invariant": bool(sym),
                "y_square_check": y_square_check(N, Dp, sf), "discriminant_orders": disc_orders(sf), **ro})
    out["verdict"] = "SECTION_READ"
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--points", type=int, default=44)
    ap.add_argument("--heldout", type=int, default=8)
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    res = run(a.points, a.heldout)
    for k, v in res.items():
        print(f"  {k}: {v}")
    ok = res.get("verdict") == "SECTION_READ" and res.get("heldout_agree") and res.get("t_to_minus_t_invariant")
    if a.emit and ok:
        h0 = json.loads((CERTS / "TW2_HEIGHT_CONDITION.json").read_text())["result"]["cooper_s7_n7"]
        l0 = json.loads((CERTS / "TW2_RHO20_LOCI.json").read_text())["result"]["loci"]["1/27"]["resolution"]
        fib = json.loads((CERTS / "INOSE_FIBRATION_MULTIPLICITIES.json").read_text())["result"]["T5_s7_loci"]["1/27"]["orders"]
        fib_orders = sorted([fib["s=+1"], fib["s=-1"], fib["s=0"]] + list(fib["roots_of_e(s^2)"]), reverse=True)
        cross = {"step0_P_dot_O": h0["P_dot_O"], "step0_height": h0["height_h_P"],
                 "step2a_P_dot_O": l0["P_dot_O_solutions"][0]["P_dot_O"], "step2a_contr": l0["P_dot_O_solutions"][0]["contr"],
                 "fibration_certificate_orders": fib_orders, "kumar_kuwata_height_2d": 2 * 7}
        cross["agree"] = bool(res["P_dot_O"] == cross["step0_P_dot_O"] == cross["step2a_P_dot_O"]
                              and res["height"] == str(cross["step0_height"]) == str(cross["kumar_kuwata_height_2d"])
                              and res["contr_A1"] == str(cross["step2a_contr"])
                              and res["discriminant_orders"] == fib_orders)
        cert = {"certificate": "TW2_SECTION_DESCENT", "work_package": "WP-TW2 step 2b-ii (2026-10-10)",
                "checker": "checkers/check_TW2_section_descent.py",
                "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "tier": "B (exact rational arithmetic; the construction is Kumar-Kuwata Prop. 3.2, Tier L, pinned text; the section "
                        "is reconstructed from exact specializations, over-determined, and verified at held-out points)",
                "result": res, "cross_check_against_earlier_steps": cross,
                "not_claimed": ["any Kodaira label (ledger items 3, 10): the A_1 is the root lattice of step 2a; only the section's contact with it is read",
                                "that this section generates the full Mordell-Weil group beyond height 14 = 2*7 (KK Prop. 3.2(ii) and the lattice "
                                "side both give 14; no index computation is made here)",
                                "anything physical; the K3 is a model surface (ledger item 4)",
                                "z = -1 and z = infinity: this is the z = 1/27 locus only"],
                "generated_by": "Claude (Fable 5.1), Stream 2, 2026-10-10",
                "verified_by": "checkers/test_TW2_section_descent_controls.py", "reviewed_by": "N"}
        OUT.write_text(json.dumps(cert, indent=2, default=str) + "\n")
        print("wrote", OUT)
        if not cross["agree"]:
            print("CROSS-CHECK DISAGREES", cross)
            return 1
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refuse as e:
        print("REFUSED:", e)
        sys.exit(2)
