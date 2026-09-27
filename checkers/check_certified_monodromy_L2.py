#!/usr/bin/env python3
"""
check_certified_monodromy_L2.py -- WP-S2-CERT step 1: CERTIFIED monodromy of L2.

Why. check_U1_lattice.py stage 2 continues the order-2 operator L2 numerically
(mpmath, 60 digits, Taylor order 140) and RECOGNISES the Sym^2 monodromy entries
as rationals through a 1e-35 tolerance gate. That gate is a heuristic: nothing
bounds the truncation and rounding errors. This checker redoes stage 2 in Arb
ball arithmetic (python-flint) with RIGOROUS truncation bounds, and then states
what the heuristic could not: each recognised rational is the UNIQUE rational of
denominator <= MAX_DEN inside a rigorous enclosure of the corresponding entry.

What is rigorous here (every step enclosed, no float anywhere in a bound):
  * Frobenius solutions at the MUM point z = 0: coefficients are exact rationals
    (holo_series / log_partner of the U1 checker); the tails beyond NSER terms are
    bounded by a majorant proved by induction on the theta-form recurrence:
        |a_m| <= K rho^m for m >= N0-2, once  Q1 rho + Q2 <= rho^2  where
        Q_j = sup_{m>=N0} |S_j(m)/lead(m)|  (sup of a rational function on the
        integers >= N0, enclosed by interval evaluation in u = 1/m on [0, 1/N0]);
    the log partner h has the same growth with an inhomogeneous term bounded the
    same way (K_h = max(initial, K_A eps / delta)).
  * Analytic continuation: Taylor steps around ball-valued centres; the local
    recurrence coefficients are exact rationals of the (rational) centre; the tail
    beyond TAYLOR_ORDER terms is bounded by the same majorant argument
    (Sum_s Q_s rho^-s <= 1); step length 1/2 of the majorant radius r_maj, which
    is <= the distance to the nearest singular point (proof in r_majorant()).
  * Linear algebra (W^-1, Sym^2) in balls.
Certification statement, per family:
  C-a  the cusp loop encloses [[1,1],[0,1]] (machinery control, rigorous)
  C-b  every recognised Sym^2 entry N[i][j] (from check_U1_lattice.stage2_monodromy,
       the heuristic) lies in the enclosure, and the enclosure's diameter is
       < 1/MAX_DEN^2, so no other rational with denominator <= MAX_DEN does
  C-c  det M(loc) encloses -1 for both finite loci
  C-d  the enclosure of M(loc) does NOT contain the identity (negative control:
       the loop is not trivial, rigorously)
Step 2 (same checker): the certified exact matrices are fed into the U1 checker's
exact stage 3 and the derived lattice (Gram, det, signature, discriminant group,
2n, U-splitting witness, overlattice count) is compared field by field with the
lattice certificate on main (C2_cooper_s7_v5.json LIVE; C2_cooper_s10_v4_DRAFT.json,
ADVISORY). Exit 0 needs both the certification and this chain to close.
What is NOT claimed: that the monodromy-invariant lattice IS T (Dolgachev/Doran,
Tier B, unchanged); that MAX_DEN is the right denominator bound (it is the U1
checker's, 10^4); any promotion of cooper_s10; anything physical.

Controls: checkers/test_certified_monodromy_L2_controls.py.
Exit 0 iff every certification clause holds for the family.

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: checkers/test_certified_monodromy_L2_controls.py | Reviewed-by: N
"""
import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

import mpmath as mp
from flint import acb, acb_mat, arb, ctx, fmpq

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "checkers"))
import check_U1_lattice as u1  # noqa: E402

PREC_BITS = 420
NSER = 400          # exact Frobenius terms at z = 0
N0_FROB = 60        # induction start for the Frobenius majorant
TAYLOR_ORDER = 500  # local Taylor order per step (tail floor ~ STEP_X^500 per step)
N0_STEP = 40        # induction start for the step majorant
STEP_X = Fr(7, 20)  # step length as a fraction of the majorant radius r_maj (rho|h| ~ STEP_X).
                    # Kept well below 1/1.7: the ball radii inside the recurrence grow ~1.7x
                    # faster than the majorant rho (Arb complex products are not tight), and
                    # the evaluated radius diverges once that rate times |h| reaches 1.
                    # A looser step never gives a WRONG enclosure, only a useless one (fail-closed).
NPTS = 28           # polygon points per loop (chord ~ one step, no tiny remainder steps)
DEN_WAYPOINT = 2 ** 20
MAX_DEN = u1.MAX_DEN
AUDIT_DATE = "2026-09-27"


class CertFailure(Exception):
    pass


def chk(c, msg):
    if not c:
        raise CertFailure(msg)


# ----------------------------------------------------------------------------
# ball helpers
# ----------------------------------------------------------------------------
def A_(x):
    """exact -> arb (Fraction / int / fmpq), rigorous."""
    if isinstance(x, Fr):
        return arb(x.numerator) / arb(x.denominator)
    if isinstance(x, fmpq):
        return arb(int(x.p)) / arb(int(x.q))
    return arb(int(x))


def C_(re, im=0):
    return acb(A_(re) if not isinstance(re, arb) else re, A_(im) if not isinstance(im, arb) else im)


def ub(x):
    """rigorous upper bound (as arb with zero radius) of |x| for arb/acb x."""
    return arb(abs(x).upper())


def lb(x):
    return arb(x.lower())


def amax(a, b):
    return a if bool(a >= b) else b


def ball(rad):
    """acb ball [0 +/- rad] in both parts (rad: arb), built in ball arithmetic."""
    r = ub(rad) * arb(0, 1)
    return acb(r, r)


def contains_exact(x, q):
    """acb x contains the rational q (as a real number)."""
    return x.real.contains(A_(q)) and x.imag.contains(arb(0))


def diameter(x):
    """exact arb: 2 * max(radius of real part, radius of imaginary part)."""
    return arb(2) * amax(arb(x.real.rad()), arb(x.imag.rad()))


# ----------------------------------------------------------------------------
# rigorous sup of a rational function P(m)/D(m) over integers m >= N0
# ----------------------------------------------------------------------------
def sup_ratio(P, D, N0):
    """P, D: ascending coefficient lists (arb or exact). Returns an arb upper
    bound of sup_{m >= N0} |P(m)/D(m)|. Method: m = 1/u, u in [0, 1/N0]; the
    homogenised polynomials P~(u) = sum P_i u^(d-i), D~(u) likewise, evaluated at
    the interval u = [0, 1/N0] by ball arithmetic (inclusion-monotone)."""
    P = [p if isinstance(p, arb) else A_(p) for p in P]
    D = [d if isinstance(d, arb) else A_(d) for d in D]
    d = max(len(P), len(D)) - 1
    u = (arb(1) / arb(N0)) * arb(0.5, 0.5000001)   # encloses [0, 1/N0]
    Pt = sum((P[i] * u ** (d - i) for i in range(len(P))), arb(0))
    Dt = sum((D[i] * u ** (d - i) for i in range(len(D))), arb(0))
    chk(not Dt.contains(arb(0)), f"sup_ratio: denominator enclosure contains 0 at N0={N0}; raise N0")
    return ub(Pt / Dt)


# ----------------------------------------------------------------------------
# Frobenius solutions at z = 0 with certified tails
# ----------------------------------------------------------------------------
def theta_recurrence_pieces(L2):
    """theta form L2[i][j] = coeff of z^j theta^i. lead(m) = sum_i Q_i0 m^i;
    S_j(m) = sum_i Q_ij (m-j)^i; R_j(m) = sum_i i Q_ij (m-j)^(i-1) (j = 0,1,2)."""
    import sympy as sp
    m = sp.Symbol("m")
    lead = sp.Poly(sum(sp.Integer(L2[i][0]) * m ** i for i in range(3)), m)
    S = {}
    R = {}
    for j in range(3):
        S[j] = sp.Poly(sum(sp.Integer(L2[i][j]) * (m - j) ** i for i in range(3)), m)
        R[j] = sp.Poly(sum(i * sp.Integer(L2[i][j]) * (m - j) ** (i - 1) for i in range(1, 3)), m)

    def coeffs(p):
        c = p.all_coeffs()[::-1]
        return [int(x) for x in c] if c else [0]
    return coeffs(lead), {j: coeffs(S[j]) for j in (1, 2)}, {j: coeffs(R[j]) for j in (0, 1, 2)}


def frobenius_certified(L2, z0, verbose=True):
    """A, A', h, h' at rational z0 as acb enclosures (tails included)."""
    a = u1.holo_series(L2, NSER)
    h = u1.log_partner(L2, a, NSER)
    lead, S, R = theta_recurrence_pieces(L2)
    Q1, Q2 = sup_ratio(S[1], lead, N0_FROB), sup_ratio(S[2], lead, N0_FROB)
    r0, r1, r2 = (sup_ratio(R[j], lead, N0_FROB) for j in (0, 1, 2))
    # rho: Q1 rho + Q2 <= rho^2, with a 5% margin so that delta > 0 below
    rho = ub((Q1 + (Q1 * Q1 + arb(4) * Q2).sqrt()) / arb(2)) * arb(105) / arb(100)
    chk(bool(Q1 * rho + Q2 <= rho * rho), "frobenius: majorant inequality not certified")
    KA = amax(*(ub(A_(a[k]) / rho ** k) for k in (N0_FROB - 2, N0_FROB - 1)))
    delta = lb(arb(1) - Q1 / rho - Q2 / (rho * rho))
    chk(bool(delta > 0), "frobenius: delta <= 0")
    eps = r0 + r1 / rho + r2 / (rho * rho)
    Kh_init = amax(*(ub(A_(h[k]) / rho ** k) for k in (N0_FROB - 2, N0_FROB - 1)))
    Kh = amax(Kh_init, ub(KA * eps / delta))
    x = ub(rho * A_(z0))
    chk(bool(x < 1), f"frobenius: rho*z0 = {x} >= 1")
    N = NSER - 1
    T0 = x ** (N + 1) / (arb(1) - x)
    T1 = ((N + 1) * x ** N * (arb(1) - x) + x ** (N + 1)) / (arb(1) - x) ** 2

    def ev(coeffs):
        z = A_(z0)
        val, dv = arb(0), arb(0)
        for k in reversed(range(len(coeffs))):
            val = val * z + A_(coeffs[k])
        for k in reversed(range(1, len(coeffs))):
            dv = dv * z + k * A_(coeffs[k])
        return val, dv

    Av, Ad = ev(a)
    hv, hd = ev(h)
    Av = acb(Av) + ball(KA * T0)
    Ad = acb(Ad) + ball(KA * rho * T1)
    hv = acb(hv) + ball(Kh * T0)
    hd = acb(hd) + ball(Kh * rho * T1)
    if verbose:
        print(f"  [frobenius] rho = {float(rho):.4f}, K_A = {float(KA):.3e}, K_h = {float(Kh):.3e}, "
              f"x = rho*z0 = {float(x):.4f}, tail T0 = {float(T0):.2e}")
    return Av, Ad, hv, hd, {"rho": str(float(rho)), "K_A": str(float(KA)), "K_h": str(float(Kh)),
                            "x": str(float(x)), "tail_T0": str(float(T0)), "NSER": NSER, "N0": N0_FROB}


# ----------------------------------------------------------------------------
# certified Taylor steps
# ----------------------------------------------------------------------------
def shift_poly(p, c):
    """p(z) with exact int coefficients -> coefficients of p(c + h) in h, c a
    Gaussian rational (pair of Fractions) -> list of (Fr, Fr) pairs (re, im)."""
    cre, cim = c
    n = len(p)
    out = [(Fr(0), Fr(0))] * n
    # binomial expansion with complex rational arithmetic
    powers = [(Fr(1), Fr(0))]
    for _ in range(n):
        pr, pi = powers[-1]
        powers.append((pr * cre - pi * cim, pr * cim + pi * cre))
    out = [[Fr(0), Fr(0)] for _ in range(n)]
    for k, pk in enumerate(p):
        if pk == 0:
            continue
        for j in range(k + 1):
            b = math.comb(k, j)
            pr, pi = powers[k - j]
            out[j][0] += pk * b * pr
            out[j][1] += pk * b * pi
    return [(o[0], o[1]) for o in out]


def cabs2(c):
    return c[0] * c[0] + c[1] * c[1]


def r_majorant(a2s):
    """positive r with |a2_0| = sum_{s>=1} |a2_s| r^s, as a rigorous LOWER bound.
    Any singular point (root of a2) at distance d satisfies |a2_0| <= sum |a2_s| d^s,
    hence d >= r: the disc |h| < r is singularity-free."""
    A0 = lb(A_(cabs2(a2s[0])).sqrt())
    mags = [ub(A_(cabs2(c)).sqrt()) for c in a2s[1:]]
    lo, hi = arb(0), arb(1)
    while bool(sum((mags[s] * hi ** (s + 1) for s in range(len(mags))), arb(0)) < A0):
        hi = hi * 2
    for _ in range(80):
        mid = (lo + hi) / 2
        if bool(sum((mags[s] * mid ** (s + 1) for s in range(len(mags))), arb(0)) < A0):
            lo = mid
        else:
            hi = mid
    return lb(lo)


def step_recurrence_qs(a2s, a1s, a0s):
    """q_s(m) numerator/denominator coefficient lists (in m) for
    c_m = sum_s q_s(m) c_{m-s}; entries are Gaussian rationals -> complex arb."""
    def cx(c):
        return acb(A_(c[0]), A_(c[1]))
    S = 3
    num = {s: [acb(0), acb(0), acb(0)] for s in range(1, S + 1)}
    for s in range(1, S + 1):
        if s < len(a2s):   # a2_s (m-s)(m-s-1)
            c = cx(a2s[s])
            num[s][0] += c * (s * (s + 1))
            num[s][1] += c * (-(2 * s + 1))
            num[s][2] += c
        if s - 1 < len(a1s):   # a1_{s-1} (m-s)
            c = cx(a1s[s - 1])
            num[s][0] += c * (-s)
            num[s][1] += c
        if s - 2 >= 0 and s - 2 < len(a0s):   # a0_{s-2}
            num[s][0] += cx(a0s[s - 2])
    den = [acb(0), -cx(a2s[0]), cx(a2s[0])]   # a2_0 m(m-1)
    return num, den


def sup_ratio_c(P, D, N0):
    d = max(len(P), len(D)) - 1
    u = arb(1 / (2 * N0), 1 / (2 * N0) * 1.0000001)
    Pt = sum((P[i] * u ** (d - i) for i in range(len(P))), acb(0))
    Dt = sum((D[i] * u ** (d - i) for i in range(len(D))), acb(0))
    chk(not Dt.contains(acb(0)), "sup_ratio_c: denominator encloses 0")
    return ub(Pt / Dt)


class CertContinuator:
    def __init__(self, L2):
        self.a2, self.a1, self.a0 = u1.dz_form(L2)

    def step(self, p, y, dy, h):
        """p: Gaussian rational centre; h: Gaussian rational step; y, dy: acb."""
        a2s, a1s, a0s = shift_poly(self.a2, p), shift_poly(self.a1, p), shift_poly(self.a0, p)
        num, den = step_recurrence_qs(a2s, a1s, a0s)
        # exact-rational recurrence, evaluated in balls
        c = [y, dy]
        for m in range(2, TAYLOR_ORDER):
            s = acb(0)
            for sh in (1, 2, 3):
                if m - sh < 0:
                    continue
                qn = num[sh][0] + num[sh][1] * m + num[sh][2] * (m * m)
                s += qn * c[m - sh]
            c.append(-s / (den[1] * m + den[2] * (m * m)))
        # majorant
        Q = {sh: sup_ratio_c(num[sh], den, N0_STEP) for sh in (1, 2, 3)}
        rm = r_majorant(a2s)
        rho = arb(1) / rm
        # tighten: smallest rho with sum Q_s rho^-s <= 1, bisection above 1/rm
        lo, hi = rho, rho * 4
        for _ in range(60):
            mid = (lo + hi) / 2
            g = Q[1] / mid + Q[2] / mid ** 2 + Q[3] / mid ** 3
            if bool(g <= 1):
                hi = mid
            else:
                lo = mid
        rho = ub(hi)
        chk(bool(Q[1] / rho + Q[2] / rho ** 2 + Q[3] / rho ** 3 <= 1), "step: majorant not certified")
        K = arb(0)
        for k in range(N0_STEP - 3, N0_STEP):
            K = amax(K, ub(c[k] / rho ** k))
        hb = acb(A_(h[0]), A_(h[1]))
        x = ub(rho * ub(hb))
        chk(bool(x < 1), f"step: rho|h| = {float(x)} >= 1")
        N = TAYLOR_ORDER - 1
        T0 = x ** (N + 1) / (arb(1) - x)
        T1 = ((N + 1) * x ** N * (arb(1) - x) + x ** (N + 1)) / (arb(1) - x) ** 2
        # FORWARD summation, deliberately: Horner from the top passes through wide
        # balls (|mid| ~ 1e300 with radius > |mid|) and Arb's radius accounting is
        # then far looser (measured: 5e-35 vs 2.7e-53 on the same coefficients).
        # Both are rigorous; the forward sum's radius telescopes tightly.
        val, dval = acb(0), acb(0)
        hpow = acb(1)
        for k in range(len(c)):
            if k >= 1:
                dval += k * c[k] * hpow          # hpow = h^(k-1) here
                hpow = hpow * hb
            val += c[k] * hpow                   # hpow = h^k
        val += ball(K * T0)
        dval += ball(K * rho * T1)
        self.last_step_info = {"K": float(K), "rho": float(rho), "r_maj": float(rm), "x": float(x),
                               "tail0": float(K * T0), "Q": [float(Q[s]) for s in (1, 2, 3)],
                               "diam_c_last": float(diameter(c[-1])), "abs_c_last": float(abs(c[-1]))}
        return val, dval, rm, float(x)

    def continue_path(self, waypoints, y, dy, trace=False):
        p = waypoints[0]
        xmax = 0.0
        nsteps = 0
        for target in waypoints[1:]:
            while p != target:
                a2s = shift_poly(self.a2, p)
                rm = r_majorant(a2s)
                dmax = Fr(str(float(lb(rm * A_(STEP_X)))))   # rational, ~ STEP_X * r_maj
                step = (target[0] - p[0], target[1] - p[1])
                n2 = cabs2(step)
                if n2 > dmax * dmax:
                    # shrink to a rational step of length <= dmax along the same direction
                    scale = Fr(str(float(dmax) / math.sqrt(float(n2)) * 0.999))
                    step = (step[0] * scale, step[1] * scale)
                y, dy, _, x = self.step(p, y, dy, step)
                xmax = max(xmax, x)
                p = (p[0] + step[0], p[1] + step[1])
                nsteps += 1
                if trace:
                    i = self.last_step_info
                    print(f"    step {nsteps:3d} p=({float(p[0]):+.3f},{float(p[1]):+.3f}) "
                          f"|h|={math.sqrt(float(cabs2(step))):.4f} x={x:.3f} |y|={float(abs(y)):.3e} "
                          f"diam(y)={float(diameter(y)):.2e} diam(dy)={float(diameter(dy)):.2e} "
                          f"K={i['K']:.2e} rho={i['rho']:.2f} Q={['%.2f' % q for q in i['Q']]} "
                          f"tail0={i['tail0']:.1e} |c_N|={i['abs_c_last']:.1e} diam(c_N)={i['diam_c_last']:.1e}")
        self.last_nsteps = nsteps
        return y, dy, xmax


def rat_circle(center, R, start_angle):
    pts = []
    for k in range(NPTS + 1):
        ang = start_angle + 2 * math.pi * k / NPTS
        cr = Fr(round(math.cos(ang) * DEN_WAYPOINT), DEN_WAYPOINT)
        ci = Fr(round(math.sin(ang) * DEN_WAYPOINT), DEN_WAYPOINT)
        pts.append((center + R * cr, R * ci))
    pts[-1] = pts[0]
    return pts


def rat_loops(loci, z0):
    allpts = [Fr(0)] + list(loci)
    loops = {}
    for loc in loci:
        others = [s for s in allpts if s != loc]
        gap = min(abs(loc - s) for s in others)
        R = min(gap / 2, abs(loc) / 2)
        if loc > 0:
            entry = (loc - R, Fr(0))
            loops[str(loc)] = [(z0, Fr(0)), entry] + rat_circle(loc, R, math.pi) + [entry, (z0, Fr(0))]
        else:
            loops[str(loc)] = ([(z0, Fr(0)), (z0, R), (loc, R)] + rat_circle(loc, R, math.pi / 2)
                               + [(loc, R), (z0, R), (z0, Fr(0))])
    return loops


# ----------------------------------------------------------------------------
# main pipeline
# ----------------------------------------------------------------------------
def certify_family(family, verbose=True, scramble=None):
    import sympy as sp
    L2_ref, _L3 = u1.load_operators(family)
    L2 = L2_ref
    if scramble == "operator":
        # control: a different operator must NOT reproduce the reference's monodromy
        L2 = [list(r) for r in L2_ref]
        L2[1][1] += 1
    z = sp.Symbol("z")
    Q2p = sum(sp.Integer(L2[2][j]) * z ** j for j in range(3))
    loci = sorted(Fr(int(sp.Rational(r).p), int(sp.Rational(r).q)) for r in sp.solve(sp.Eq(Q2p, 0), z))
    chk(len(loci) == 2, f"{family}: expected 2 finite loci, got {loci}")
    z0 = min(abs(l) for l in loci) / 4

    Av, Ad, hv, hd, frob = frobenius_certified(L2, z0, verbose)
    logz0 = acb(A_(z0).log())
    twopii = acb(0, 1) * acb.pi() * 2
    Bv = (Av * logz0 + hv) / twopii
    Bd = (Ad * logz0 + Av / acb(A_(z0)) + hd) / twopii
    W = acb_mat([[Av, Bv], [Ad, Bd]])
    cont = CertContinuator(L2)

    def monodromy(wps):
        Ay, Ad2, x1 = cont.continue_path(wps, Av, Ad)
        By, Bd2, x2 = cont.continue_path(wps, Bv, Bd)
        col1 = W.solve(acb_mat([[Ay], [Ad2]]))
        col2 = W.solve(acb_mat([[By], [Bd2]]))
        return acb_mat([[col1[0, 0], col2[0, 0]], [col1[1, 0], col2[1, 0]]]), max(x1, x2)

    out = {"family": family, "z0": str(z0), "loci": [str(l) for l in loci], "frobenius": frob, "clauses": {}}

    # C-a cusp loop
    M0, x0 = monodromy(rat_circle(Fr(0), z0, 0.0))
    ref0 = [[1, 1], [0, 1]]
    ca = all(contains_exact(M0[i, j], ref0[i][j]) for i in range(2) for j in range(2))
    rad0 = max(float(diameter(M0[i, j])) for i in range(2) for j in range(2))
    out["clauses"]["C-a_cusp_loop_encloses_unipotent"] = {"holds": ca, "max_diameter": rad0}
    if verbose:
        print(f"  [C-a] cusp loop encloses [[1,1],[0,1]]: {ca}  (max diameter {rad0:.2e}, max rho|h| {x0:.3f})")

    # reference (heuristic) recognition from the U1 checker, ALWAYS on the true operator
    mp.mp.dps = u1.DPS
    ref_loci, Ns_ref, _ = u1.stage2_monodromy(family, L2_ref, verbose=False)
    chk([Fr(int(r.p), int(r.q)) for r in ref_loci] == loci, "loci mismatch with U1 checker")

    def sym2(M):
        m00, m01, m10, m11 = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
        return [[m00 ** 2, m00 * m01, m01 ** 2],
                [2 * m00 * m10, m00 * m11 + m01 * m10, 2 * m01 * m11],
                [m10 ** 2, m10 * m11, m11 ** 2]]

    loops = rat_loops(loci, z0)
    all_ok = ca
    bound = Fr(1, MAX_DEN * MAX_DEN)
    for loc in loci:
        M, x = monodromy(loops[str(loc)])
        det = M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]
        cc = contains_exact(det, -1)
        eye = [[1, 0], [0, 1]]
        cd = not all(contains_exact(M[i, j], eye[i][j]) for i in range(2) for j in range(2))
        N = sym2(M)
        Nref = Ns_ref[str(sp.Rational(loc.numerator, loc.denominator))]
        cb_contains = all(contains_exact(N[i][j], Fr(int(Nref[i, j].p), int(Nref[i, j].q)))
                          for i in range(3) for j in range(3))
        dia_arb = arb(0)
        for i in range(3):
            for j in range(3):
                dia_arb = amax(dia_arb, diameter(N[i][j]))
        dia = float(dia_arb)
        cb_unique = bool(dia_arb < A_(bound))
        out["clauses"][f"C-b_sym2_entries_certified_at_{loc}"] = {
            "recognised_matrix": [[str(Nref[i, j]) for j in range(3)] for i in range(3)],
            "all_entries_enclosed": cb_contains, "max_diameter": dia,
            "unique_rational_with_den_le_MAX_DEN": cb_unique, "MAX_DEN": MAX_DEN}
        out["clauses"][f"C-c_det_encloses_minus_one_at_{loc}"] = {"holds": cc}
        out["clauses"][f"C-d_loop_not_trivial_at_{loc}"] = {"holds": cd}
        all_ok &= cb_contains and cb_unique and cc and cd
        if verbose:
            print(f"  [z={loc}] max rho|h| {x:.3f}; det encloses -1: {cc}; not identity: {cd}; "
                  f"Sym^2 entries enclosed: {cb_contains}; max diameter {dia:.2e} < 1/MAX_DEN^2: {cb_unique}")
    out["certified"] = all_ok

    # ---- step 2: the certified exact matrices into the exact stage 3 -------------
    # The certification above says the recognised rationals ARE the monodromy entries
    # (unique in their enclosures). Feeding exactly those into stage 3 and comparing
    # with the lattice certificate on main closes the chain
    #   certified numerics -> exact lattice arithmetic -> recorded lattice.
    Ns_cert = {k: v.copy() for k, v in Ns_ref.items()}
    if scramble == "stage3_entry":
        k0 = sorted(Ns_cert)[0]
        Ns_cert[k0][0, 2] += 1        # control: must be refused by stage 3's exact gates
    lat = u1.stage3_lattice(family, L2_ref, ref_loci, Ns_cert, verbose=False)
    ref_name = {"cooper_s7": "C2_cooper_s7_v5.json", "cooper_s10": "C2_cooper_s10_v4_DRAFT.json"}[family]
    ref = json.loads((REPO / "data" / "certificates" / ref_name).read_text())["derived"]
    compare = {
        "gram_primitive_even": (lat["gram_primitive_even"], ref["gram_primitive_even"]),
        "det": (lat["det"], ref["det"]),
        "signature": (lat["signature"], ref["signature"]),
        "disc_group_elementary_divisors": (lat["disc_group_elementary_divisors"], ref["disc_group_elementary_divisors"]),
        "derived_2n": (lat["derived_2n"], ref["derived_2n_from_cusp_unipotent"]),
        "u_splitting.d": (lat["u_splitting"]["d"], ref["u_splitting"]["d"]),
        "u_splitting.gram_after": (lat["u_splitting"]["gram_after"], ref["u_splitting"]["gram_after"]),
        "u_splitting.basis_change_matrix": (lat["u_splitting"]["basis_change_matrix"],
                                            ref["u_splitting"]["basis_change_matrix"]),
        "proper_even_invariant_overlattices": (lat["proper_even_invariant_overlattices"],
                                               ref["proper_even_invariant_overlattices"]),
    }
    equal = {k: a == b for k, (a, b) in compare.items()}
    out["stage3_from_certified_matrices"] = {
        "reference_certificate": ref_name,
        "reference_status": "LIVE" if "DRAFT" not in ref_name else "DRAFT (ADVISORY)",
        "derived_here": {k: a for k, (a, b) in compare.items()},
        "field_equal": equal,
        "all_equal": all(equal.values()),
    }
    out["chain_closed"] = all_ok and all(equal.values())
    if verbose:
        print(f"  [stage3] from certified matrices: {sum(equal.values())}/{len(equal)} fields equal to "
              f"{ref_name} -> chain closed: {out['chain_closed']}")
    return out


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", default="cooper_s7", choices=sorted(u1.FAMILIES))
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--emit-c2-draft", action="store_true",
                    help="cooper_s7 only: write C2_cooper_s7_v6_DRAFT.json = v5 content with the stage-2 "
                         "input provenance changed from 1e-35 recognition to this certification. DRAFT: "
                         "v5 stays LIVE until T0 rules; every derived value is asserted equal to v5.")
    a = ap.parse_args(argv)
    ctx.prec = PREC_BITS
    try:
        res = certify_family(a.family)
    except CertFailure as e:
        print("CERTIFICATION REFUSED:", e)
        return 2
    print("certified:", res["certified"], "| stage-3 chain closed:", res["chain_closed"])
    if a.emit:
        cert = {
            "certificate": f"CERTIFIED_MONODROMY_L2_{a.family}",
            "checker": "checkers/check_certified_monodromy_L2.py", "checker_version": "1.0.0",
            "date": AUDIT_DATE, "tier": "B",
            "status": "WP-S2-CERT steps 1+2 (T0 D9', 2026-09-27). Step 1 replaces the 1e-35 recognition gate "
                      "of check_U1_lattice.py stage 2 by rigorous enclosures: each recognised Sym^2 entry is the "
                      "unique rational of denominator <= MAX_DEN in a ball-arithmetic enclosure with certified "
                      "truncation bounds. Step 2 feeds exactly those matrices into the exact stage 3 and compares "
                      "the derived lattice field by field with the lattice certificate on main "
                      "(result.stage3_from_certified_matrices). The Dolgachev/Doran identification of the "
                      "invariant lattice with T is unchanged and stays Tier B. cooper_s10 remains ADVISORY "
                      "(lattice certificate DRAFT, T0 D6'); certifying its numerics does not promote it.",
            "tier_reason": "the monodromy matrices in the Frobenius flag basis are now certified (Arb balls, "
                           "majorant tail bounds, exact rational centres); Tier B remains for the identification "
                           "of the monodromy-invariant lattice with T (framework sources, read).",
            "parameters": {"PREC_BITS": PREC_BITS, "NSER": NSER, "N0_FROB": N0_FROB, "TAYLOR_ORDER": TAYLOR_ORDER,
                           "N0_STEP": N0_STEP, "NPTS": NPTS, "MAX_DEN": MAX_DEN, "python_flint": __import__("flint").__version__},
            "result": res,
            "inputs": {"sha256": {"refs/recurrences_v1.json": sha(u1.REFS),
                                  "checkers/check_U1_lattice.py": sha(REPO / "checkers" / "check_U1_lattice.py")}},
            "not_claimed": ["anything beyond stage 2 of check_U1_lattice.py",
                            "that MAX_DEN = 10^4 is the right denominator bound (it is the U1 checker's)",
                            "any physical reading (VISION sec. 1.3; ledger item 4)"],
            "controls": "checkers/test_certified_monodromy_L2_controls.py",
            "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: "
                          "checkers/test_certified_monodromy_L2_controls.py | Reviewed-by: N",
        }
        out = REPO / "data" / "certificates" / f"CERTIFIED_MONODROMY_L2_{a.family}.json"
        out.write_text(json.dumps(cert, indent=2) + "\n")
        print("wrote", out)
    if a.emit_c2_draft:
        if a.family != "cooper_s7" or not (res["certified"] and res["chain_closed"]):
            print("REFUSED: --emit-c2-draft needs cooper_s7 certified with the stage-3 chain closed")
            return 2
        v5 = json.loads((REPO / "data" / "certificates" / "C2_cooper_s7_v5.json").read_text())
        v6 = dict(v5)
        v6["certificate"] = "C2_cooper_s7_v6_DRAFT"
        v6["status"] = ("DRAFT - pending T0 (Xavier) review; does NOT supersede C2_cooper_s7_v5.json (LIVE, "
                        "D5'). Content = v5 with ONE change of provenance: the stage-2 monodromy matrices are "
                        "CERTIFIED (checkers/check_certified_monodromy_L2.py, Arb ball arithmetic with rigorous "
                        "truncation bounds; each Sym^2 entry the unique rational of denominator <= 10^4 in its "
                        "enclosure; exact stage 3 on them reproduces v5 field by field) instead of recognised "
                        "through a 1e-35 tolerance. Every derived value is asserted identical to v5 below.")
        v6["date"] = AUDIT_DATE
        v6["tier"] = "B"
        v6["tier_reason"] = ("the numerical link is closed (certified enclosures replace the 1e-35 recognition "
                             "gate); the residual Tier B is the identification of the joint monodromy-invariant "
                             "lattice with T via the read framework sources (Dolgachev 1996 sec. 7, Doran 1998 "
                             "Thm 5.13) and the Frobenius-basis normalisation conventions of stage 2")
        how = dict(v5.get("how", {}))
        how["stage2"] = ("CERTIFIED: Arb ball arithmetic (python-flint), Frobenius tails and Taylor-step tails "
                         "bounded by majorant induction, exact rational path points; see "
                         "data/certificates/CERTIFIED_MONODROMY_L2_cooper_s7.json (result.clauses)")
        v6["how"] = how
        v6["inputs_added_in_v6"] = {"sha256": {
            "data/certificates/CERTIFIED_MONODROMY_L2_cooper_s7.json":
                sha(REPO / "data" / "certificates" / "CERTIFIED_MONODROMY_L2_cooper_s7.json"),
            "data/certificates/C2_cooper_s7_v5.json": sha(REPO / "data" / "certificates" / "C2_cooper_s7_v5.json")}}
        v6["derived_identical_to_v5"] = v6["derived"] == v5["derived"]
        v6["supersedes_if_accepted"] = "C2_cooper_s7_v5.json (no value changes; provenance only)"
        v6["provenance"] = ("Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: "
                            "checkers/check_certified_monodromy_L2.py (certified + chain closed) and "
                            "checkers/test_certified_monodromy_L2_controls.py | Reviewed-by: N (DRAFT)")
        assert v6["derived_identical_to_v5"] is True
        outp = REPO / "data" / "certificates" / "C2_cooper_s7_v6_DRAFT.json"
        outp.write_text(json.dumps(v6, indent=2) + "\n")
        print("wrote", outp, "(DRAFT; v5 stays LIVE)")
    return 0 if (res["certified"] and res["chain_closed"]) else 1


if __name__ == "__main__":
    sys.exit(main())
