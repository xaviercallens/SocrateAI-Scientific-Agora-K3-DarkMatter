#!/usr/bin/env python3
"""
check_CM_points_rho20.py -- the CM-point (rho = 20) map of the cooper_s7 and cooper_s10
families, as lattice / modular arithmetic.  Tier B at best.  No physical reading.

WHAT IS COMPUTED
  The rank-3 lattice T_n = U + <2n>, basis (e, f, w), norm v^2 = 2xy + 2n z^2, is RE-DERIVED
  from the family's C2 lattice certificate through check_T3_level_consistency.lattice_leg
  (n is never typed here).  The period vector is omega(tau) = (1, -n tau^2, tau)
  [Stream 1 MnLattice.period, read as source].  For an integer vector v = (x, y, z):

      B(v, omega) = y - n x tau^2 + 2 n z tau,

  a quadratic in tau of discriminant 2n * v^2.  So B(v, omega) = 0 has a root in the upper
  half plane iff v^2 < 0, and then tau = z/x + i * sqrt(-v^2 / (2n)) / |x|.
  (Stage 0 re-derives all of this symbolically with sympy; nothing above is trusted.)

  For each primitive v in a LOGGED window (see WINDOW below) the checker computes
    - tau, as an exact quadratic irrational (Re tau and (Im tau)^2 are Fractions);
    - T_X := v^perp in T_n: an exact integer kernel, checked orthogonal, rank 2 and
      saturated (gcd of 2x2 minors = 1), Gram even and positive definite; Gauss-reduced
      to (a, b, c) with Gram [[2a, b], [b, 2c]]; D = b^2 - 4ac < 0; det = -D; and the
      exact identity det = (-v^2) * 2n / div(v)^2 is asserted row by row;
    - the round trip: from the NUMERICAL tau alone, the integer vectors annihilating
      omega(tau) are searched for and must come back as +-v (this is the function the
      non-CM control exercises);
    - w = 1/z = alpha t + beta + gamma / t, with t the level-n eta quotient evaluated by
      mpmath and (alpha, beta, gamma) RE-FITTED exactly to q^ORDER by
      check_T3_level_consistency.modular_leg;
    - recognition of w (hence z) as an algebraic number by LLL on (Re, Im) at DPS_FIT
      digits, accepted only if the polynomial still vanishes at w recomputed at
      DPS_VERIFY digits.  This is NUMERIC RECOGNITION (Tier B), never a proof that z is
      that algebraic number.
  Rows are deduplicated by the value of z (numeric clustering, tolerance logged) and
  sorted by |D|.

FAMILY-LEVEL CONSISTENCY CHECKS (each gates the exit code; each has a control that makes
it fire -- controls R2, S8):
    - fricke_consistency: for every enumerated v, z(tau_v) = z(tau_{-swap v}), where
      swap e<->f is Fricke tau -> -1/(n tau) (stage 0).  Couples the lattice's n to the
      modular side's level: with the n of the OTHER family it fails.
    - same z => same T_X up to the sign of b, and same z => same (-v^2, div v).

WINDOW (logged, never silent).  v primitive, x > 0 (v ~ -v), 0 < -v^2 <= BOUND,
  -1/2 < Re tau <= 1/2 (tau -> tau + 1 is in Gamma_0(n)), |tau|^2 >= 1/n (Fricke),
  Im tau >= Y_MIN.  This is NOT claimed to be a fundamental domain, and the table is NOT
  claimed complete at any D; the per-row field `conjugates_in_table` (how many roots of
  the recognised minimal polynomial occur as z-values in the table) is a diagnostic of
  that, not a gate.

TIERS OF THE LINKS
  exact (integer / Fraction / sympy): T_n, v^2, tau, T_X, reduction, D, det identity,
      the relation 1/z = alpha t + beta + gamma/t to q^ORDER (PASS(ORDER), a finite order).
  numeric recognition (Tier B): every value of t, w, z and every minimal polynomial.
  framework, cited not proved (Tier B, source read and hash-pinned in
      docs/literature/MANIFEST.md): Dolgachev 1996 sec 7 -- the period domain of
      M_n-polarized K3 surfaces is H / Gamma_0(n)+ with T = U + <2n>; an integral class
      orthogonal to the period is of type (1,1), hence algebraic by the Lefschetz (1,1)
      theorem (standard; NOT one of the statements the MANIFEST pins from Dolgachev), so
      at such tau the Picard number is 20 and the transcendental lattice is v^perp.  THIS
      is the link that turns "v.omega = 0" into "rho = 20"; the checker computes the
      lattice side only.  Dolgachev Thm 7.3 (pinned) removes the (-2)-walls from the
      ample locus: at a (-2)-vector point (the rows -v^2 = 2, which include C1 singular
      loci) the statement refers at best to a pseudo-ample / resolved surface; see
      NOT_CLAIMED.
  Tier L elsewhere (LeanMaster docs/STREAM8_WHICH_K3.md sec G10 and
      DualScaleDyons/FrickeRepair.lean, read as source at commit 4109a51 -- the commit
      that introduces both; no Lean build run): rho = 20 <=> rank-2 positive definite
      T(X), classified by reduced binary forms; Shioda-Inose identifies the rho = 20
      locus with the CM locus (Huybrechts, quoted there, not proved there or here).
      Both cross-repo citations are RE-VERIFIED at run time by verify_citation() (the
      path must exist at the cited commit and contain the cited name); an earlier draft
      of this file cited a commit at which neither LeanMaster file existed, and that
      hash is now control R5's real known-bad.
  Stream 1 (SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal, commit 3a96018,
      read as source, no Lean build run): MnLattice.TN_norm, period, period_isotropic,
      swap_is_fricke, swap_fixes_selfdual; SelfDual.root = (1,-1,0), root_norm = -2,
      root_orthogonal_iff_selfdual, s7_singular_points_are_selfdual (the two s7 loci are
      zOf(1/7), zOf(-1/7)); ModularAction.root2 = (-2,4,1) with root2_norm = -2 and
      W7conj_eq_neg_reflection; g3_fixes (14,-14,5), norm -42.  Those vectors are
      re-found here by enumeration, not imported.

NOT CLAIMED: see NOT_CLAIMED below; it is copied into the certificate.

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: test_CM_points_rho20_controls.py
Reviewed-by: N
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time
from fractions import Fraction as F
from math import gcd, isqrt
from pathlib import Path

import mpmath as mp
import sympy as sp
from sympy.polys.matrices import DomainMatrix
from sympy import ZZ

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_T3_level_consistency as T3  # noqa: E402

H10 = T3.H10
REPO = T3.REPO
CERTS = T3.CERTS
OUT = CERTS / "CM_POINTS_RHO20.json"

BOUND = 44                 # 0 < -v^2 <= BOUND
Y_MIN = F(1, 20)           # Im tau >= Y_MIN
DPS_FIT = 120              # digits used to FIT a minimal polynomial
DPS_VERIFY = 200           # digits used to RE-CHECK it (must be > DPS_FIT)
DEGREES = (1, 2, 3, 4, 6, 8)
# second tier, tried only on rows the first tier leaves unrecognised (taller polynomials)
TIER2 = {"dps_fit": 320, "dps_verify": 420, "degrees": (6, 8, 12)}
CLUSTER_DPS = 40           # pass-1 precision for grouping by z
CLUSTER_TOL_EXP = 28       # two w-values are the same if |dw| <= 10^-28 (1 + |w|)
ORDER = T3.ORDER
LOCI_CERT = {"cooper_s7": "C1_L3_cooper_s7.json", "cooper_s10": "C1_L3_cooper_s10.json"}

# Cross-repo citations.  The commit is the one the source was READ at; verify_citation()
# re-checks at run time that each path exists at that commit and contains the cited name
# (standing rule 4: verify a directive's artifacts).  No Lean build is run.
EXTERNAL_CITATIONS = {
    "leanmaster": {
        "repo_dir_name": "SocrateAI-Scientific-Agora-LeanMaster", "commit": "4109a51",
        "paths": {"docs/STREAM8_WHICH_K3.md": "G10",
                  "DualScaleDyons/FrickeRepair.lean": "repair_selects"}},
    "stream1": {
        "repo_dir_name": "SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal",
        "commit": "3a96018",
        "paths": {"Agora/Geometry/MnLattice.lean": "swap_is_fricke",
                  "Agora/Geometry/SelfDual.lean": "root_orthogonal_iff_selfdual",
                  "Agora/Geometry/ModularAction.lean": "root2_norm"}},
}

NOT_CLAIMED = [
    "that this table scores or ranks a candidate: the rho = 20 cut was ADOPTED by T0 on 2026-09-21 "
    "(D7', briefs/T0_DECISIONS_2026_09_21_STREAM2.md) and is read narrowly - no ranking of "
    "candidates, no minimum-|D| rule",
    "that any member of either family is singled out or preferred: this is a table of "
    "lattice/modular arithmetic",
    "that the table is complete at any discriminant: the enumeration window is logged and "
    "is not shown to be a fundamental domain",
    "that any z-value IS the algebraic number recorded: every minimal polynomial is a numeric "
    "recognition, fitted at DPS_FIT digits and re-checked at DPS_VERIFY digits (Tier B)",
    "that the step from 'v.omega = 0' to 'rho = 20, T_X = v^perp' is proved here: it is the cited "
    "framework (Dolgachev 1996 sec 7 period domain, read and pinned, plus the Lefschetz (1,1) "
    "theorem, standard and not among the pinned statements; Tier B). The checker computes the "
    "lattice side only",
    "that a smooth M_n-polarized member with rho = 20 sits at the (-2)-vector rows: Dolgachev "
    "Thm 7.3 (pinned) removes the (-2)-walls from the ample locus, and those rows include C1 "
    "singular loci of the operator; 'T_X = v^perp' there refers at best to a pseudo-ample / "
    "resolved surface and is recorded as lattice arithmetic only",
    "anything certified about T(cooper_s10): C2_cooper_s10_v4_DRAFT.json is DRAFT by T0 ruling; "
    "every s10 row carries LATTICE_CERT_DRAFT and is advisory",
    "any Kodaira fibre type at any locus (CLAUDE.md ledger item 3): the loci are elliptic "
    "points of the modular curve and are treated only as such",
    "any physical reading whatsoever (VISION sec 1.3; Tier C blocked, F5b)",
]


class Refused(Exception):
    """Refuse to emit a number rather than emit a wrong one.  `.clause` names what fired."""

    def __init__(self, clause, msg=""):
        super().__init__(f"{clause}: {msg}" if msg else clause)
        self.clause = clause


def log(*a):
    print(*a, flush=True)


# ------------------------------------------------------------- stage 0 (sympy) ----
def stage0_selftest():
    """Re-derive the mathematics symbolically.  Returns a dict of booleans, all must hold."""
    n, x, y, z, tau, s, m = sp.symbols("n x y z tau s m")
    G = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 2 * n]])
    v = sp.Matrix([x, y, z])
    om = sp.Matrix([1, -n * tau ** 2, tau])
    pairing = sp.expand((v.T * G * om)[0])
    quad = sp.Poly(-pairing, tau)                 # n x tau^2 - 2 n z tau - y
    a2, a1, a0 = quad.all_coeffs()
    v2 = sp.expand((v.T * G * v)[0])
    out = {
        "omega_isotropic": sp.expand((om.T * G * om)[0]) == 0,
        "pairing_is_y_minus_nx_tau2_plus_2nz_tau":
            sp.expand(pairing - (y - n * x * tau ** 2 + 2 * n * z * tau)) == 0,
        "norm_is_2xy_plus_2n_z2": sp.expand(v2 - (2 * x * y + 2 * n * z ** 2)) == 0,
        "quadratic_discriminant_is_2n_v2": sp.expand(a1 ** 2 - 4 * a2 * a0 - 2 * n * v2) == 0,
    }
    # tau = z/x + i s / x with s^2 = m/(2n), m = -v^2, i.e. y = -(m + 2 n z^2)/(2x):
    tau0 = z / x + sp.I * s / x
    y0 = -(m + 2 * n * z ** 2) / (2 * x)
    res = sp.expand(pairing.subs({tau: tau0, y: y0}))
    res = sp.simplify(res.subs(s ** 2, m / (2 * n)))
    out["root_is_z_over_x_plus_i_sqrt_m_over_2n_over_x"] = res == 0
    # Fricke fixed locus: v = (1,-1,0) pairs to -(n tau^2 + 1)  [Stream 1 root_pairing_period]
    out["root_1_m1_0_pairs_to_minus_n_tau2_minus_1"] = sp.expand(
        pairing.subs({x: 1, y: -1, z: 0}) + n * tau ** 2 + 1) == 0
    # swap e<->f is Fricke: swap(omega(tau)) = (-n tau^2) omega(-1/(n tau))
    sw = sp.Matrix([om[1], om[0], om[2]])
    om_f = om.subs(tau, -1 / (n * tau))
    out["swap_is_fricke"] = sp.simplify(sw - (-n * tau ** 2) * om_f) == sp.zeros(3, 1)
    if not all(out.values()):
        raise Refused("stage0_selftest", str(out))
    return {k: bool(b) for k, b in out.items()}


# --------------------------------------------------------------- lattice side ----
def gram_T(n):
    return [[0, 1, 0], [1, 0, 0], [0, 0, 2 * n]]


def norm(n, v):
    x, y, z = v
    return 2 * x * y + 2 * n * z * z


def pair_row(n, v):
    """The integer linear form u -> B(v, u), as a row."""
    x, y, z = v
    return (y, x, 2 * n * z)


def ext_gcd(a, b):
    if b == 0:
        return (abs(a), (1 if a >= 0 else -1), 0)
    g, s, t = ext_gcd(b, a % b)
    return g, t, s - (a // b) * t


def integer_kernel(row):
    """A Z-basis (two vectors) of {u in Z^3 : row . u = 0}; row != 0."""
    g = gcd(gcd(row[0], row[1]), row[2])
    r0, r1, r2 = (c // g for c in row)
    if r0 == 0 and r1 == 0:
        return [(1, 0, 0), (0, 1, 0)]
    g01, a, b = ext_gcd(r0, r1)
    assert a * r0 + b * r1 == g01
    u1 = (r1 // g01, -r0 // g01, 0)
    h = gcd(g01, r2)
    u2 = (-a * r2 // h, -b * r2 // h, g01 // h)
    return [u1, u2]


def verify_TX(n, v, basis):
    """Check that `basis` is a Z-basis of v^perp in T_n and return its Gram matrix.
    Refuses with a clause code otherwise."""
    v = tuple(int(c) for c in v)
    if v == (0, 0, 0) or gcd(gcd(v[0], v[1]), v[2]) != 1:
        raise Refused("v_not_primitive", f"v = {v}")
    if norm(n, v) >= 0:
        raise Refused("no_upper_half_plane_root",
                      f"v^2 = {norm(n, v)} >= 0: discriminant 2n v^2 is not negative")
    row = pair_row(n, v)
    if len(basis) != 2:
        raise Refused("kernel_wrong_rank", f"{len(basis)} vectors")
    for u in basis:
        if sum(r * c for r, c in zip(row, u)) != 0:
            raise Refused("kernel_not_orthogonal", f"B(v, {tuple(u)}) != 0")
    (a0, a1, a2), (b0, b1, b2) = basis
    minors = (a1 * b2 - a2 * b1, a2 * b0 - a0 * b2, a0 * b1 - a1 * b0)
    gm = gcd(gcd(minors[0], minors[1]), minors[2])
    if gm == 0:
        raise Refused("kernel_wrong_rank", "basis vectors are dependent")
    if gm != 1:
        raise Refused("kernel_not_saturated",
                      f"gcd of 2x2 minors = {gm}: an index-{gm} sublattice of v^perp")
    G = gram_T(n)
    B = [[sum(basis[i][k] * G[k][l] * basis[j][l] for k in range(3) for l in range(3))
          for j in range(2)] for i in range(2)]
    if B[0][0] % 2 or B[1][1] % 2:
        raise Refused("TX_not_even", str(B))
    det = B[0][0] * B[1][1] - B[0][1] ** 2
    if not (B[0][0] > 0 and det > 0):
        raise Refused("TX_not_positive_definite", str(B))
    div = gcd(gcd(row[0], row[1]), row[2])
    if det * div * div != -norm(n, v) * 2 * n:
        raise Refused("det_identity_fails",
                      f"det {det} * div^2 {div * div} != -v^2 * 2n = {-norm(n, v) * 2 * n}")
    return B, div


def gauss_reduce(a, b, c):
    """Reduce the positive definite form a x^2 + b x y + c y^2 (proper equivalence)."""
    if not (a > 0 and b * b - 4 * a * c < 0):
        raise Refused("TX_not_positive_definite", f"({a},{b},{c})")
    D = b * b - 4 * a * c
    while True:
        if c < a:
            a, b, c = c, -b, a
        if -a < b <= a:
            if a == c and b < 0:
                b = -b
            break
        k = (b + a) // (2 * a) if b > a else -((a - b) // (2 * a))
        # b -> b - 2 a k, c -> c - b k + a k^2
        a, b, c = a, b - 2 * a * k, c - b * k + a * k * k
    assert b * b - 4 * a * c == D and -a < b <= a <= c
    return a, b, c


def transcendental_lattice(n, v, basis=None):
    basis = integer_kernel(pair_row(n, v)) if basis is None else basis
    B, div = verify_TX(n, v, basis)
    a, b, c = gauss_reduce(B[0][0] // 2, B[0][1], B[1][1] // 2)
    return {"kernel_basis": [list(u) for u in basis], "gram": B, "div_v": div,
            "reduced_form": [a, b, c], "D": b * b - 4 * a * c, "det": 4 * a * c - b * b,
            "content": gcd(gcd(a, b), c)}


def tau_exact(n, v):
    """(Re tau, (Im tau)^2) as Fractions; refuses unless v^2 < 0."""
    x, y, z = v
    m = -norm(n, v)
    if m <= 0 or x == 0:
        raise Refused("no_upper_half_plane_root", f"v^2 = {-m}")
    return F(z, x), F(m, 2 * n * x * x)


def tau_num(n, v):
    re, im2 = tau_exact(n, v)
    return mp.mpc(mp.mpf(re.numerator) / re.denominator,
                  mp.sqrt(mp.mpf(im2.numerator) / im2.denominator))


def enumerate_vectors(n, bound=BOUND, y_min=Y_MIN):
    """Primitive v = (x, y, z), x > 0, 0 < m = -v^2 <= bound, tau in the logged window."""
    out = []
    for m in range(2, bound + 1, 2):
        # Im tau = sqrt(m/(2n))/x >= y_min  <=>  x^2 <= m / (2 n y_min^2)
        x_max = isqrt(int(F(m, 2 * n) / (y_min * y_min)))
        for x in range(1, x_max + 1):
            for z in range(-((x - 1) // 2), x // 2 + 1):
                num = -(m + 2 * n * z * z)
                if num % (2 * x):
                    continue
                y = num // (2 * x)
                if gcd(gcd(x, y), z) != 1:
                    continue
                if -y < x:            # |tau|^2 = -y/(n x) >= 1/n
                    continue
                out.append((x, y, z))
    return out


def vectors_annihilating(n, tau, x_max, tol=None):
    """From a NUMERICAL tau alone: primitive integer v = (x>0, y, z) with B(v, omega(tau)) = 0.
    B = 0 forces z = x Re(tau) and y = -n x |tau|^2, so both must be integers."""
    tol = tol or mp.mpf(10) ** (-(mp.mp.dps // 2))
    re, nn = mp.re(tau), n * (mp.re(tau) ** 2 + mp.im(tau) ** 2)
    found = []
    for x in range(1, x_max + 1):
        zf, yf = x * re, -x * nn
        z, y = int(mp.nint(zf)), int(mp.nint(yf))
        if abs(zf - z) < tol and abs(yf - y) < tol and gcd(gcd(x, y), z) == 1:
            found.append((x, y, z))
    return found


# --------------------------------------------------------------- modular side ----
def relation_for(key, level):
    M = T3.modular_leg(key, level, ORDER)
    if not (M["uniformizes_at_level"] and M["relation"]):
        raise Refused("relation_not_certified", f"{key} at level {level}: {M['failing_clauses']}")
    return {k: F(val) for k, val in M["relation"].items()}, T3.LEVEL_COORD[level]


def w_of_tau(rel, r, tau):
    """w = 1/z = alpha t + beta + gamma/t at the current mp.dps (guard digits added inside)."""
    dps = mp.mp.dps
    mp.mp.dps = dps + 25
    try:
        t = H10.eta_quotient_num(r, tau)
        w = (mp.mpf(rel["alpha"].numerator) / rel["alpha"].denominator * t
             + mp.mpf(rel["beta"].numerator) / rel["beta"].denominator
             + mp.mpf(rel["gamma"].numerator) / rel["gamma"].denominator / t)
    finally:
        mp.mp.dps = dps
    return +t, +w


def _lll_candidate(val, d, P):
    S = 10 ** P
    pw, rows = mp.mpc(1), []
    for i in range(d + 1):
        rows.append([1 if j == i else 0 for j in range(d + 1)]
                    + [int(mp.nint(mp.re(pw) * S)), int(mp.nint(mp.im(pw) * S))])
        pw *= val
    red = DomainMatrix([[ZZ(c) for c in row] for row in rows], (d + 1, d + 3), ZZ).lll()
    best = min((list(map(int, r)) for r in red.to_list()),
               key=lambda r: sum(c * c for c in r))
    return best[:d + 1]


def recognize_algebraic(val_fit, val_verify, dps_fit, dps_verify, degrees=DEGREES):
    """Minimal polynomial of `val` (ascending integer coefficients) or None.
    Fitted from val_fit (dps_fit digits) by LLL; ACCEPTED only if it also vanishes at
    val_verify (dps_verify digits) to within 10^-(dps_verify - 20) relative size."""
    if dps_verify <= dps_fit:
        raise Refused("precision_control", "verify precision must exceed fit precision")
    P = dps_fit - 15
    old = mp.mp.dps
    mp.mp.dps = dps_verify + 10
    try:
        if abs(val_verify) < mp.mpf(10) ** (-(dps_fit - 20)):
            return {"degree": 1, "coeffs": [0, 1], "is_zero": True}
        if abs(val_verify) > 1:
            # |val|^d * 10^P would need more digits than val_fit carries (the integer
            # entries of the LLL matrix would be noise in their last d*log10|val| digits):
            # recognise 1/val, of modulus < 1, and reverse the coefficients.
            rec = recognize_algebraic(1 / val_fit, 1 / val_verify, dps_fit, dps_verify, degrees)
            if rec is None:
                return None
            c = rec["coeffs"][::-1]
            if c[-1] < 0:
                c = [-k for k in c]
            return {"degree": rec["degree"], "coeffs": c, "is_zero": False}
        for d in degrees:
            c = _lll_candidate(val_fit, d, P)
            if not any(c[1:]):
                continue
            hmax = max(abs(k) for k in c)
            if (d + 1) * mp.log10(hmax + 1) > 0.7 * P:
                continue                               # too tall to distinguish from noise
            scale = sum(abs(k) * abs(val_verify) ** i for i, k in enumerate(c))
            resid = abs(sum(k * val_verify ** i for i, k in enumerate(c)))
            if resid > scale * mp.mpf(10) ** (-(dps_verify - 20)):
                continue
            X = sp.symbols("X")
            poly = sp.Poly(sum(k * X ** i for i, k in enumerate(c)), X)
            for fac, _ in poly.factor_list()[1]:
                fc = [int(k) for k in fac.all_coeffs()[::-1]]
                sc = sum(abs(k) * abs(val_verify) ** i for i, k in enumerate(fc))
                if abs(sum(k * val_verify ** i for i, k in enumerate(fc))) \
                        <= sc * mp.mpf(10) ** (-(dps_verify - 20)):
                    if fc[-1] < 0:
                        fc = [-k for k in fc]
                    return {"degree": len(fc) - 1, "coeffs": fc, "is_zero": False}
        return None
    finally:
        mp.mp.dps = old


def z_minpoly_from_w(rec):
    """w = 1/z: reverse the coefficients.  w = 0 <-> z = infinity."""
    if rec is None:
        return None
    if rec["is_zero"]:
        return {"degree": 1, "z": "infinity", "coeffs": None}
    c = rec["coeffs"][::-1]
    if c[-1] < 0:
        c = [-k for k in c]
    out = {"degree": rec["degree"], "coeffs": c, "z": None}
    if rec["degree"] == 1:
        out["z"] = str(F(-c[0], c[1]))
    return out


def poly_str(c):
    if c is None:
        return None
    X = sp.symbols("z")
    return str(sp.Poly(sum(k * X ** i for i, k in enumerate(c)), X).as_expr())


# ---------------------------------------------------------------- per family ----
def point_record(n, v, rel, r, dps_fit=DPS_FIT, dps_verify=DPS_VERIFY, degrees=DEGREES,
                 tier2=True):
    """Everything about one vector.  Refuses on any lattice-side violation."""
    TX = transcendental_lattice(n, v)
    re, im2 = tau_exact(n, v)
    mp.mp.dps = dps_fit
    tau = tau_num(n, v)
    back = vectors_annihilating(n, tau, x_max=abs(v[0]))
    if tuple(v) not in back:
        raise Refused("round_trip_fails", f"tau of {v} is annihilated by {back}")
    tiers = [(dps_fit, dps_verify, degrees)]
    if tier2:
        tiers.append((TIER2["dps_fit"], TIER2["dps_verify"], TIER2["degrees"]))
    for dps_fit, dps_verify, degs in tiers:
        mp.mp.dps = dps_fit
        t_fit, w_fit = w_of_tau(rel, r, tau_num(n, v))
        mp.mp.dps = dps_verify
        t_ver, w_ver = w_of_tau(rel, r, tau_num(n, v))
        rec_w = recognize_algebraic(w_fit, w_ver, dps_fit, dps_verify, degs)
        if rec_w is not None:
            break
    degrees = tuple(sorted(set(d for tr in tiers for d in tr[2])))
    rec_t = recognize_algebraic(t_fit, t_ver, dps_fit, dps_verify, (1, 2))
    zmp = z_minpoly_from_w(rec_w)
    mp.mp.dps = 30
    znum = None if (rec_w and rec_w["is_zero"]) else mp.chop(1 / w_ver, tol=mp.mpf(10) ** -100)
    t_ver = mp.chop(t_ver, tol=mp.mpf(10) ** -100)
    rowd = {
        "v": list(v), "minus_v2": -norm(n, v), "div_v": TX["div_v"],
        # exact: the reflection in v is integral on T_n iff v^2 divides 2 div(v)
        "v_is_reflective": (2 * TX["div_v"]) % (-norm(n, v)) == 0,
        "tau": {"re": str(re), "im_squared": str(im2)},
        "T_X_reduced_form_abc": TX["reduced_form"], "D": TX["D"], "det_T_X": TX["det"],
        "T_X_form_content": TX["content"], "T_X_kernel_basis": TX["kernel_basis"],
        "t_numeric": mp.nstr(t_ver, 25),
        "t_minpoly": poly_str(rec_t["coeffs"]).replace("z", "t") if rec_t else None,
        "z_numeric": "infinity" if znum is None else mp.nstr(znum, 25),
        "z_recognised": zmp is not None,
        "z_degree": zmp["degree"] if zmp else None,
        "z_value_if_rational": zmp["z"] if zmp else None,
        "z_minpoly": poly_str(zmp["coeffs"]) if zmp else None,
        "z_minpoly_coeffs_ascending": zmp["coeffs"] if zmp else None,
        "recognition": (f"Tier B numeric recognition: LLL at {dps_fit} digits, "
                        f"re-checked at {dps_verify} digits" if zmp else
                        f"UNRECOGNISED at degree <= {max(degrees)} (not a statement that z is "
                        "transcendental; the degree/height cap is the limit)"),
    }
    mp.mp.dps = DPS_FIT
    return rowd, (w_ver if znum is not None else None)


def group_by_z(n, rel, r, vs):
    """Pass 1 (cheap): cluster the vectors by the value of w = 1/z, identifying w with its
    complex conjugate (tau -> -conj(tau) sends z to conj(z) and preserves T_X up to the
    sign of b).  Numeric clustering with a logged tolerance, not string keys.
    Returns a list of lists of vectors."""
    mp.mp.dps = CLUSTER_DPS
    tol = mp.mpf(10) ** -CLUSTER_TOL_EXP
    reps, groups = [], []
    for v in vs:
        _, w = w_of_tau(rel, r, tau_num(n, v))
        for i, w0 in enumerate(reps):
            if min(abs(w - w0), abs(mp.conj(w) - w0)) <= tol * (1 + abs(w0)):
                groups[i].append(v)
                break
        else:
            reps.append(w)
            groups.append([v])
    return groups


def same_z_checks(n, groups):
    """Same z => same T_X (up to the sign of b), and same z => same (-v^2, div v): all the
    vectors of a group lie in one orbit of the isometries that fix z.  Returns the two
    violation lists (empty = consistent).  Control S8 feeds it a merged group."""
    form_viol, normdiv_viol = [], []
    for grp in groups:
        TXs = [transcendental_lattice(n, v) for v in grp]
        forms = {(T["reduced_form"][0], abs(T["reduced_form"][1]), T["reduced_form"][2])
                 for T in TXs}
        nd = {(-norm(n, v), T["div_v"]) for v, T in zip(grp, TXs)}
        if len(forms) != 1:
            form_viol.append({"vectors": [list(v) for v in grp],
                              "forms_up_to_sign_b": sorted(forms)})
        if len(nd) != 1:
            normdiv_viol.append({"vectors": [list(v) for v in grp],
                                 "minus_v2_and_div": sorted(nd)})
    return form_viol, normdiv_viol


def fricke_image(v):
    """-swap(v): swap e<->f is Fricke tau -> -1/(n tau) (stage 0); the sign puts x > 0.
    Exact check that it is what it says: same norm, and tau' * tau = -1/n."""
    x, y, z = v
    return (-y, -x, -z)


def fricke_consistency(n, rel, r, vs):
    """For every v: w(tau_v) must equal w(tau_{fricke_image v}), because z is a function on
    H / Gamma_0(n)+ and the Fricke involution of THAT n is in the group.  This is the check
    that ties the lattice's n to the level of the modular side: evaluated with the n of
    another family it fails (control R2).  Returns the list of violations."""
    mp.mp.dps = CLUSTER_DPS
    tol = mp.mpf(10) ** -CLUSTER_TOL_EXP
    viol = []
    for v in vs:
        vf = fricke_image(v)
        if norm(n, vf) != norm(n, v):
            raise Refused("fricke_image_not_isometric", f"{v} -> {vf}")
        re, im2 = tau_exact(n, v)
        ref, im2f = tau_exact(n, vf)
        # exact: tau * tau' = -1/n  <=>  re*ref - im*imf = -1/n and re*imf + ref*im = 0
        if not (im2 * im2f == (re * ref + F(1, n)) ** 2 and re * re * im2f == ref * ref * im2
                and re * ref <= 0 and re * ref + F(1, n) > 0):
            raise Refused("fricke_image_not_fricke", f"{v} -> {vf}")
        _, w = w_of_tau(rel, r, tau_num(n, v))
        _, wf = w_of_tau(rel, r, tau_num(n, vf))
        if abs(w - wf) > tol * (1 + abs(w)):
            viol.append({"v": list(v), "fricke_image": list(vf),
                         "abs_dw_over_1_plus_abs_w": mp.nstr(abs(w - wf) / (1 + abs(w)), 5)})
    return viol


def conjugates_diagnostic(rows):
    """Per row of degree > 1: how many roots of the recognised minimal polynomial occur
    among the z-values (and their complex conjugates) of `rows`.  A coverage diagnostic,
    not a gate.  Control S9 removes rows and the count must drop."""
    mp.mp.dps = 30
    zvals = []
    for R in rows:
        if R["z_numeric"] != "infinity":
            zv = mp.mpmathify(R["z_numeric"].replace(" ", ""))
            zvals += [zv, mp.conj(zv)]
    out = []
    for R in rows:
        c = R["z_minpoly_coeffs_ascending"]
        if c and R["z_degree"] > 1:
            roots = mp.polyroots([mp.mpf(k) for k in c[::-1]], maxsteps=200, extraprec=200)
            hit = sum(1 for rt in roots if any(abs(rt - zv) < mp.mpf(10) ** -15 * (1 + abs(rt))
                                               for zv in zvals))
            out.append(f"{hit}/{R['z_degree']}")
        else:
            out.append(None)
    return out


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def input_hashes():
    """sha256 of every repo file a number in the certificate is derived from."""
    files = [CERTS / spec["lattice_cert"] for spec in T3.CANDIDATES.values()]
    files += [CERTS / f for f in LOCI_CERT.values()]
    files += [T3.C1.REFS, REPO / "docs" / "literature" / "MANIFEST.md"]
    return {str(Path(f).relative_to(REPO)): sha256_file(f) for f in files}


def verify_citation(cit, commit=None, home=None):
    """Does each cited path exist at the cited commit of the sibling repo, and contain the
    cited name?  Returns {"status": VERIFIED | PHANTOM | REPO_UNAVAILABLE, ...}.  Read-only
    (git cat-file / git show).  REPO_UNAVAILABLE (e.g. CI without the sibling checkouts) is
    logged and does not fail the run; PHANTOM does."""
    commit = commit or cit["commit"]
    repo = Path(home or Path.home()) / cit["repo_dir_name"]
    out = {"repo": cit["repo_dir_name"], "commit": commit, "paths": {}}
    if not (repo / ".git").exists():
        out["status"] = "REPO_UNAVAILABLE"
        return out
    ok = True
    for path, needle in cit["paths"].items():
        pr = subprocess.run(["git", "-C", str(repo), "show", f"{commit}:{path}"],
                            capture_output=True, text=True)
        if pr.returncode != 0:
            out["paths"][path] = "absent_at_commit"
            ok = False
        elif needle not in pr.stdout:
            out["paths"][path] = f"present_but_name_{needle}_not_found"
            ok = False
        else:
            out["paths"][path] = f"present_contains_{needle}"
    out["status"] = "VERIFIED" if ok else "PHANTOM"
    return out


def family(key, bound=BOUND, y_min=Y_MIN):
    spec = T3.CANDIDATES[key]
    L = T3.lattice_leg(CERTS / spec["lattice_cert"])
    n = L["n_lattice"]
    rel, r = relation_for(key, n)
    flags = [] if spec["lattice_cert_status"] == "LIVE" else ["LATTICE_CERT_DRAFT"]
    loci = json.loads((CERTS / LOCI_CERT[key]).read_text())["finite_singular_loci"]
    vs = enumerate_vectors(n, bound, y_min)
    log(f"[{key}] n = {n} (re-derived from {spec['lattice_cert']}, {spec['lattice_cert_status']}); "
        f"relation 1/z = {rel['alpha']} t + {rel['beta']} + {rel['gamma']}/t (PASS({ORDER})); "
        f"window: 0 < -v^2 <= {bound}, Im tau >= {y_min}, -1/2 < Re tau <= 1/2, "
        f"|tau|^2 >= 1/{n}; {len(vs)} primitive vectors")

    # pass 1 (cheap): group the vectors by z-value; family-level consistency checks
    groups = group_by_z(n, rel, r, vs)
    same_z_violations, same_z_normdiv_violations = same_z_checks(n, groups)
    fricke_violations = fricke_consistency(n, rel, r, vs)

    rows = []
    for grp in groups:
        grp.sort(key=lambda v: (-norm(n, v), v[0], abs(v[2]), v))
        rowd, _ = point_record(n, grp[0], rel, r)
        rowd["vectors_in_window_with_this_z_up_to_conj"] = len(grp)
        rowd["flags"] = list(flags)
        rowd["advisory"] = bool(flags)
        rowd["singular_locus_match"] = (rowd["z_value_if_rational"]
                                        if rowd["z_value_if_rational"] in loci + ["infinity"]
                                        else None)
        rows.append(rowd)
    rows.sort(key=lambda R: (-R["D"], R["minus_v2"], R["v"]))

    # diagnostic: how many roots of each minimal polynomial appear in the table
    for R, c in zip(rows, conjugates_diagnostic(rows)):
        R["conjugates_in_table"] = c
    return {"candidate": key, "n": n, "lattice_cert": spec["lattice_cert"],
            "lattice_cert_status": spec["lattice_cert_status"], "flags": flags,
            "advisory": bool(flags), "lattice_leg": L,
            "relation_1_over_z": {k: str(val) for k, val in rel.items()},
            "relation_order_checked": ORDER,
            "eta_exponents_t": {str(k): e for k, e in r.items()},
            "singular_loci_from_C1_cert": loci,
            "vectors_enumerated": len(vs), "distinct_z_up_to_conj": len(rows),
            "unrecognised_rows": sum(1 for R in rows if not R["z_recognised"]),
            "same_z_different_form_violations": same_z_violations,
            "same_z_different_norm_or_div_violations": same_z_normdiv_violations,
            "fricke_consistency_violations": fricke_violations,
            "fricke_consistency_vectors_checked": len(vs),
            "rows": rows}


# ---------------------------------------------------------------- prediction ----
def locus_hits(fam):
    hits = {}
    for R in fam["rows"]:
        if R["singular_locus_match"]:
            hits.setdefault(R["singular_locus_match"], []).append(
                {"v": R["v"], "minus_v2": R["minus_v2"], "div_v": R["div_v"],
                 "v_is_reflective": R["v_is_reflective"], "D": R["D"], "T_X_reduced_form_abc": R["T_X_reduced_form_abc"],
                 "t_minpoly": R["t_minpoly"], "tau": R["tau"]})
    return hits


def evaluate_prediction(fams):
    """The orchestrator's pre-registered hand estimate, scored clause by clause."""
    out = {"statement": (
        "PRE-REGISTERED (orchestrator hand estimate, unverified before this run): the Fricke "
        "fixed point n tau^2 = -1 is v = (1,-1,0), v^2 = -2, T_X = <2> + <2n>; for s7 it maps "
        "to one of {-1, 1/27} and the OTHER locus is another (-2)-vector CM point with "
        "t = -1/7. For s10: which of {-1/4, 1/16, infinity} come from (-2)- or other "
        "small-norm vectors (no value predicted).")}
    clauses, kinds = {}, {}
    for key, fam in fams.items():
        n = fam["n"]
        root = (1, -1, 0)
        TX = transcendental_lattice(n, root)
        name = (f"{key}: v=(1,-1,0) has v^2=-2 and T_X = <2>+<{2*n}>"
                + (" [ADVISORY: n from a DRAFT lattice certificate]" if fam["advisory"] else ""))
        clauses[name] = norm(n, root) == -2 and TX["reduced_form"] == [1, 0, n]
        kinds[name] = ("arithmetic_identity: holds for every n once n is fixed; carries no "
                       "content beyond the lattice certificate's n")
        fam["locus_hits"] = locus_hits(fam)
    s7 = fams["cooper_s7"]
    h = s7["locus_hits"]
    fr = [loc for loc, L in h.items() if any(x["v"] == [1, -1, 0] for x in L)]
    clauses["cooper_s7: Fricke fixed point maps to one of the C1 loci"] = (
        len(fr) == 1 and fr[0] in s7["singular_loci_from_C1_cert"])
    others = [l for l in s7["singular_loci_from_C1_cert"] if l not in fr]
    ok_other = (len(others) == 1 and others[0] in h
                and any(x["minus_v2"] == 2 for x in h[others[0]]))
    clauses["cooper_s7: the OTHER locus is a (-2)-vector CM point"] = bool(ok_other)
    clauses["cooper_s7: ... at t = -1/7"] = bool(
        ok_other and any(x["t_minpoly"] == "7*t + 1" for x in h[others[0]]))
    for name in clauses:
        kinds.setdefault(name, "non_trivial: depends on the numeric evaluation of z(tau) and "
                               "could have failed")
    out["clauses"] = clauses
    out["clause_kinds"] = kinds
    out["non_trivial_clauses_confirmed"] = (
        f"{sum(1 for k in clauses if clauses[k] and kinds[k].startswith('non_trivial'))}/"
        f"{sum(1 for k in clauses if kinds[k].startswith('non_trivial'))}")
    out["s7_fricke_locus"] = fr[0] if len(fr) == 1 else None
    out["s10_observed"] = {loc: [{"v": x["v"], "minus_v2": x["minus_v2"], "div_v": x["div_v"],
                                  "D": x["D"], "t_minpoly": x["t_minpoly"],
                                  "v_is_reflective": x["v_is_reflective"]} for x in L]
                           for loc, L in fams["cooper_s10"]["locus_hits"].items()}
    out["s10_loci_not_hit_in_window"] = [
        l for l in fams["cooper_s10"]["singular_loci_from_C1_cert"] + ["infinity"]
        if l not in fams["cooper_s10"]["locus_hits"]]
    out["outcome"] = "CONFIRMED" if all(clauses.values()) else "REFUTED_IN_PART"
    return out


def git_head():
    try:
        return subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    log("=" * 78)
    log("CM points (rho = 20) of the cooper_s7 / cooper_s10 families -- lattice arithmetic")
    log("=" * 78)
    s0 = stage0_selftest()
    log("stage 0 symbolic self-test:", "all hold" if all(s0.values()) else s0)
    log(f"BOUND = {BOUND} (0 < -v^2 <= BOUND), Y_MIN = {Y_MIN}, DPS_FIT = {DPS_FIT}, "
        f"DPS_VERIFY = {DPS_VERIFY}, degrees tried {DEGREES}; second tier for unrecognised rows: {TIER2}")
    fams = {k: family(k) for k in ("cooper_s7", "cooper_s10")}
    pred = evaluate_prediction(fams)

    for key, fam in fams.items():
        log(f"\n[{key}] {fam['distinct_z_up_to_conj']} distinct z (up to conjugation) from "
            f"{fam['vectors_enumerated']} vectors; unrecognised: {fam['unrecognised_rows']}; "
            f"flags: {fam['flags'] or 'none'}" + ("  ** ADVISORY **" if fam["advisory"] else ""))
        log(f"  {'|D|':>5} {'-v^2':>4} {'div':>3} {'v':<16} {'(a,b,c)':<14} deg  z")
        for R in fam["rows"][:25]:
            zs = R["z_value_if_rational"] or R["z_minpoly"] or "UNRECOGNISED"
            log(f"  {-R['D']:>5} {R['minus_v2']:>4} {R['div_v']:>3} {str(tuple(R['v'])):<16} "
                f"{str(tuple(R['T_X_reduced_form_abc'])):<14} {str(R['z_degree']):<4} {zs}"
                + ("   <-- singular locus" if R["singular_locus_match"] else ""))
        log(f"  consistency: Fricke z(tau_v) = z(tau_-swap(v)) on {fam['fricke_consistency_vectors_checked']} "
            f"vectors: {len(fam['fricke_consistency_violations'])} violations; same z => same T_X: "
            f"{len(fam['same_z_different_form_violations'])}; same z => same (-v^2, div): "
            f"{len(fam['same_z_different_norm_or_div_violations'])}")
        for kk in ("fricke_consistency_violations", "same_z_different_form_violations",
                   "same_z_different_norm_or_div_violations"):
            if fam[kk]:
                log(f"  !! {kk}:", fam[kk][:5])
    log("\nPRE-REGISTERED PREDICTION:", pred["outcome"])
    for c, ok in pred["clauses"].items():
        log(f"  {'confirmed' if ok else 'REFUTED  '}  {c}  [{pred['clause_kinds'][c].split(':')[0]}]")
    log("  non-trivial clauses confirmed:", pred["non_trivial_clauses_confirmed"])
    log("  s10 observed:", json.dumps(pred["s10_observed"]))
    log("  s10 loci not hit in window:", pred["s10_loci_not_hit_in_window"])

    violations = sum(len(f["same_z_different_form_violations"]) for f in fams.values())
    nd_violations = sum(len(f["same_z_different_norm_or_div_violations"]) for f in fams.values())
    fr_violations = sum(len(f["fricke_consistency_violations"]) for f in fams.values())
    citations = {k: verify_citation(c) for k, c in EXTERNAL_CITATIONS.items()}
    for k, c in citations.items():
        log(f"citation {k} @ {c['commit']}: {c['status']} {c['paths']}")
    citations_ok = all(c["status"] != "PHANTOM" for c in citations.values())
    loci_ok = all(l in f["locus_hits"] for f in fams.values()
                  for l in f["singular_loci_from_C1_cert"])
    cert = {
        "certificate": "CM_POINTS_RHO20",
        "checker": "checkers/check_CM_points_rho20.py",
        "checker_version": git_head(),
        "date": "2026-09-21",
        "status": ("RECORD, NOT A GATE. The rho = 20 cut was ADOPTED by T0 on 2026-09-21 (D7', briefs/T0_DECISIONS_2026_09_21_STREAM2.md), read narrowly: no ranking of candidates, no minimum-|D| rule, no physical reading. "
                   "K3_CRITERIA.md unchanged. No scoring. cooper_s10 rows advisory."),
        "claim": ("For each primitive v of negative norm in a logged window of T_n = U+<2n>: the "
                  "exact tau with B(v, omega(tau)) = 0, the exact rank-2 lattice v^perp with its "
                  "reduced form and discriminant, and a numeric recognition of z(tau)."),
        "tier": "B",
        "tier_links": {
            "exact": ["T_n re-derived from the C2 certificate", "v^2, tau, v^perp, Gauss reduction, D",
                      "det(v^perp) = -v^2 * 2n / div(v)^2, asserted per row",
                      f"1/z = alpha t + beta + gamma/t, PASS({ORDER})", "stage-0 sympy identities"],
            "numeric_recognition_tier_B": [
                f"every t, z value and minimal polynomial: LLL at {DPS_FIT} digits, re-checked "
                f"at {DPS_VERIFY} digits (second tier {TIER2['dps_fit']}/{TIER2['dps_verify']}); "
                "each row records the precision actually used"],
            "framework_cited_tier_B": [
                "Dolgachev 1996 sec 7 (docs/literature/MANIFEST.md, read, hash-pinned): period "
                "domain H/Gamma_0(n)+, T = U+<2n>",
                "Lefschetz (1,1) theorem (standard; not among the statements pinned in the "
                "MANIFEST): v.omega = 0 => v algebraic => rho = 20, T_X = v^perp",
                "caveat: Dolgachev Thm 7.3 (pinned) removes the (-2)-walls from the ample locus; "
                "at rows with -v^2 = 2 the statement refers at best to a pseudo-ample / resolved "
                "surface"],
            "tier_L_external": [
                "LeanMaster docs/STREAM8_WHICH_K3.md sec G10 + DualScaleDyons/FrickeRepair.lean, "
                f"commit {EXTERNAL_CITATIONS['leanmaster']['commit']}, read as source, no Lean "
                "build run: rho=20 <=> rank-2 positive "
                "definite T(X); Shioda-Inose / CM locus (Huybrechts, quoted there)"],
            "stream1_read_as_source": [
                "SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal commit "
                f"{EXTERNAL_CITATIONS['stream1']['commit']}, "
                "Agora/Geometry/{MnLattice,SelfDual,ModularAction}.lean, no Lean build run"],
        },
        "external_citations_verified_at_run_time": citations,
        "inputs": {"sha256": input_hashes()},
        "not_claimed": NOT_CLAIMED,
        "window": {"BOUND_minus_v2": BOUND, "Y_MIN_im_tau": str(Y_MIN),
                   "re_tau": "(-1/2, 1/2]", "abs_tau_squared_min": "1/n", "x_positive": True,
                   "dedup": ("by z up to complex conjugation (tau -> -conj(tau)); numeric "
                             f"clustering at {CLUSTER_DPS} digits, tolerance 10^-{CLUSTER_TOL_EXP} "
                             "relative to 1 + |1/z|"),
                   "complete": "NOT CLAIMED"},
        "precision": {"DPS_FIT": DPS_FIT, "DPS_VERIFY": DPS_VERIFY, "degrees_tried": list(DEGREES),
                      "tier2_for_rows_unrecognised_by_tier1": {k: (list(x) if isinstance(x, tuple)
                                                                   else x) for k, x in TIER2.items()}},
        "stage0_selftest": s0,
        "prediction": pred,
        "checks": {"same_z_different_form_violations": violations,
                   "same_z_different_norm_or_div_violations": nd_violations,
                   "fricke_consistency_violations": fr_violations,
                   "external_citations_not_phantom": citations_ok,
                   "all_C1_singular_loci_reproduced": loci_ok},
        "controls": "checkers/test_CM_points_rho20_controls.py",
        "families": fams,
        "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: "
                      "test_CM_points_rho20_controls.py | Reviewed-by: N",
    }
    log(f"\nall C1 singular loci reproduced as CM points: {loci_ok}; "
        f"same-z/different-form violations: {violations}; same-z/different-(norm,div): "
        f"{nd_violations}; Fricke-consistency violations: {fr_violations}; citations not "
        f"phantom: {citations_ok}; elapsed {time.time() - t0:.0f}s")
    if args.emit:
        OUT.write_text(json.dumps(cert, indent=1) + "\n")
        log(f"wrote {OUT.relative_to(REPO)}")
    return 0 if (loci_ok and citations_ok
                 and violations == nd_violations == fr_violations == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
