#!/usr/bin/env python3
"""
check_U1_lattice.py — U1 execution (docs/U1_ROUTE_DESIGN_2026_07_26.md):
derive the discriminant data of the transcendental-lattice candidate T of a
Cooper-family K3 from the family itself, via elliptic monodromies of the
order-2 partner operator L2.

WHAT THIS SCRIPT DOES (in the route design's order)
---------------------------------------------------
STAGE 0  Symbolic re-derivation of the Dolgachev section-7 framework facts this
         run relies on (period shape, Yukawa constant, cusp n-blindness, the
         quadric bilinear form). sympy-exact, symbolic n. The route design
         instructs re-derivation before use; this stage IS that re-derivation.

STAGE 1  (U1a-3) Exact q-series: operators are DERIVED at runtime from the
         recurrence coefficients in refs/recurrences_v1.json (numbers are
         computed, never typed), holomorphic + log Frobenius solutions, mirror
         map, and the mirror-normalized two-point Yukawa as an exact q-series.
         Asserts constancy to full computed order. HONESTY NOTE (printed at
         runtime, discussed in the brief): in any Wronskian/quadric-compatible
         normalization the constancy is mathematically forced once the operator
         is a symmetric square (Tier A for these families), so stage 1 is a
         PIPELINE-CONSISTENCY control; the VALUE of the constant is a
         normalization convention and is NOT independently extractable here.
         The value acquires meaning only from the integral lattice of stage 3.

STAGE 2  (U1a-2) Numerical analytic continuation of L2 around BOTH finite
         singular loci (loci computed at runtime as the roots of the leading
         theta-coefficient), in the Frobenius basis (A, Bhat) at the MUM point,
         Bhat = (A log z + g)/(2 pi i). The loop around z = 0 is continued
         numerically as a machinery control and must reproduce the analytically
         known [[1,1],[0,1]]. Sym^2 of the 2x2 matrices gives the L3 (lattice)
         monodromies; entries are recognized as rationals with a LOUD tolerance
         gate and then verified exactly (involutivity, order-3 product).

STAGE 3  Exact lattice pipeline (sympy rationals, no floats): joint invariant
         symmetric bilinear form (must be unique up to scale), orbit lattice of
         the cusp-invariant vector f under the monodromy group, closure check,
         Gram matrix restricted to the lattice, primitive even rescale, det,
         signature, discriminant group/form, the derived 2n (divisibility of
         (T_cusp - 1)^2 on the lattice), an EXPLICIT U-splitting when div(f)=1
         (which proves the isometry type of the computed lattice by exhibiting
         an integral base change - no genus theory needed), and the count of
         proper even monodromy-invariant overlattices.

NO EXPECTED VALUE APPEARS IN THIS PIPELINE. The script prints what it derives.
Expectations (det = -14 etc.) live only in the route design, the controls
(checkers/test_U1_controls.py, which compare two DIFFERENT families against
each other), and the findings brief.

Usage:
  python3 checkers/check_U1_lattice.py                       # cooper_s7
  python3 checkers/check_U1_lattice.py --family cooper_s10   # control family
  python3 checkers/check_U1_lattice.py --controls            # all controls
  python3 checkers/check_U1_lattice.py --emit-cert           # s7 + controls + DRAFT cert

Exit codes: 0 all stages pass . 3 a structural assertion failed . 2 usage/data.

Generated-by: Fable 5 (Stream 2, U1 execution session 2026-07-27)
Verified-by: this script's own structural assertions + checkers/test_U1_controls.py
Reviewed-by: pending T0 (Xavier)
"""

import argparse
import hashlib
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

import mpmath as mp
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_form

REPO = Path(__file__).resolve().parent.parent
REFS = REPO / "refs" / "recurrences_v1.json"

DPS = 60                 # working precision (decimal digits)
NSER = 400               # exact Frobenius series terms for base-point evaluation
NQ = 36                  # exact q-series order for stage 1
TAYLOR_ORDER = 140       # local Taylor order for continuation
STEP_RATIO = mp.mpf("0.35")   # step size as fraction of distance to nearest sing.
TOL_NUM = mp.mpf(10) ** -40   # numeric structural tolerance (M0 control, M^2=I)
TOL_REC = mp.mpf(10) ** -35   # recognition tolerance (rational entries)
MAX_DEN = 10 ** 4             # recognition denominator bound

FAMILIES = {
    "cooper_s7": {"bulk": "cooper_s7", "partner": "cooper_s7_partner",
                  "hauptmodul_bfile": "oeis_A279618_bfile.txt"},
    "cooper_s10": {"bulk": "cooper_s10", "partner": "cooper_s10_partner",
                   "hauptmodul_bfile": None},
}


class ControlFailure(Exception):
    """Raised when a structural condition fails (this is the loud path)."""


def chk(cond, msg):
    if not cond:
        raise ControlFailure(msg)


# ----------------------------------------------------------------------------
# STAGE 0 — symbolic framework re-derivation (Dolgachev 1996 section 7, READ;
# docs/literature/dolgachev_1996_mirror_lattice_polarized_k3.pdf, hash-pinned)
# ----------------------------------------------------------------------------

def stage0_framework():
    n = sp.Symbol("n", positive=True)
    tau = sp.Symbol("tau")
    x, y = sp.symbols("x y", real=True)

    G = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 2 * n]])  # U + <2n>, basis (f,g,e)
    mu = sp.Matrix([-n * tau**2, 1, tau])                 # Dolgachev p.20: mu = -nt^2 f + g + te
    dmu = mu.diff(tau)

    chk(sp.simplify((mu.T * G * mu)[0, 0]) == 0, "stage0: mu not isotropic")
    chk(sp.simplify((mu.T * G * dmu)[0, 0]) == 0, "stage0: Q(mu, dmu) != 0")
    yuk = sp.simplify((dmu.T * G * dmu)[0, 0])
    chk(yuk == 2 * n, f"stage0: Q(dmu,dmu) = {yuk} != 2n")

    mu_c = mu.subs(tau, x + sp.I * y)
    pos = sp.simplify(sp.expand((mu_c.T * G * sp.conjugate(mu_c))[0, 0]))
    chk(pos == 4 * n * y**2, f"stage0: (mu, mubar) = {pos} != 4 n y^2")
    # -> the e-direction has POSITIVE square 2n; fixes the sign of the invariant
    #    form in stage 3 (signature (2,1), middle/flag coefficient positive).

    T = sp.Matrix([[1, -n, -2 * n], [0, 1, 0], [0, 1, 1]])  # T(f)=f, T(g)=g-nf+e, T(e)=e-2nf
    chk(sp.simplify(T.T * G * T - G) == sp.zeros(3, 3), "stage0: T not in O(G)")
    chk(sp.simplify(T * mu - mu.subs(tau, tau + 1)) == sp.zeros(3, 1),
        "stage0: T mu(tau) != mu(tau+1)")

    F0 = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])       # swap f <-> g
    chk(sp.simplify(F0 * mu - (-n * tau**2) * mu.subs(tau, -1 / (n * tau))) == sp.zeros(3, 1),
        "stage0: F0 does not realize tau -> -1/(n tau)")

    # Frobenius flag coordinates: mu = P * (1, tau, tau^2)
    P = sp.Matrix([[0, 0, -n], [1, 0, 0], [0, 1, 0]])
    chk(sp.simplify(P * sp.Matrix([1, tau, tau**2]) - mu) == sp.zeros(3, 1), "stage0: P wrong")
    Tflag = sp.simplify(P.inv() * T * P)
    chk(n not in Tflag.free_symbols, "stage0: cusp matrix in flag coords depends on n")
    chk(Tflag == sp.Matrix([[1, 0, 0], [1, 1, 0], [1, 2, 1]]), "stage0: unexpected flag cusp matrix")
    Gflag = sp.simplify(P.T * G * P)
    chk(Gflag == sp.Matrix([[0, 0, -n], [0, 2 * n, 0], [-n, 0, 0]]),
        "stage0: flag Gram is not -2n * polarization of y0 y2 - y1^2")

    # Sym^2 representation SL2 -> SO(1,2), derived from scratch on binary forms
    a, b, c, d, u = sp.symbols("a b c d u")
    al, be, ga = sp.symbols("alpha beta gamma")
    sqn = sp.sqrt(n)
    phi = al * x**2 + 2 * be * sqn * x * y + ga * y**2
    sub = phi.subs([(x, d * x - b * y), (y, -c * x + a * y)], simultaneous=True).expand()
    alp = sub.coeff(x, 2).coeff(y, 0)
    bep = sub.coeff(x, 1).coeff(y, 1) / (2 * sqn)
    gap = sub.coeff(y, 2).coeff(x, 0)
    M = sp.Matrix([[sp.diff(r, v) for v in (ga, be, al)] for r in (gap, bep, alp)])
    GE = sp.Matrix([[0, 0, -1], [0, 2 * n, 0], [-1, 0, 0]])
    chk(sp.simplify((M.T * GE * M - GE).subs(d, (1 + b * c) / a)) == sp.zeros(3, 3),
        "stage0: derived Sym^2 rep does not preserve the form")
    v = sp.Matrix([n * u**2, u, 1])
    w = (M * v).subs(d, (1 + b * c) / a)
    w = sp.simplify(w / w[2, 0])
    chk(sp.simplify(w[0, 0] - n * w[1, 0] ** 2) == 0,
        "stage0: Sym^2 rep not equivariant on isotropic vectors")
    return {
        "yukawa_constant_symbolic": "Q(d_tau mu, d_tau mu) = 2n  [re-derived]",
        "cusp_flag_matrix_n_free": True,
        "flag_gram": "-2n * polarization(y0 y2 - y1^2)  [re-derived]",
        "note": ("The printed Dolgachev A(g) matrix (OCR) differs from the from-scratch "
                 "derivation in the middle-row denominators (1/n vs 1/sqrt(n)); the "
                 "from-scratch matrix passes Gram-preservation + equivariance and is "
                 "the one relied on (which is: none - stage 2/3 use only computed "
                 "matrices)."),
    }


# ----------------------------------------------------------------------------
# refs -> operators. Recurrences are read from refs/recurrences_v1.json and the
# theta-operators DERIVED from them (no typed operator coefficients).
# Bulk convention:    P0(k) a(k) + P1(k) a(k+1) + P2(k) a(k+2) = 0
#   -> L3 = P2(th-2) + z P1(th-1) + z^2 P0(th)
# Partner convention: C(k) a(k+1) = A(k) a(k) + B(k) a(k-1)
#   -> L2 = C(th-1) - z A(th) - z^2 B(th+1)
# ----------------------------------------------------------------------------

def _polyshift(coeffs, shift):
    """coeffs of p(k) ascending -> coeffs of p(k + shift) ascending (exact)."""
    th = sp.Symbol("th")
    p = sum(sp.Integer(c) * (th + shift) ** i for i, c in enumerate(coeffs))
    p = sp.Poly(sp.expand(p), th)
    out = [int(x) for x in reversed(p.all_coeffs())]
    return out


def load_operators(family):
    data = json.loads(REFS.read_text())["sequences"]
    fam = FAMILIES[family]
    bulk = data[fam["bulk"]]["recurrence_coefficients"]
    part = data[fam["partner"]]["recurrence_coefficients"]

    P0, P1, P2 = bulk["P0"], bulk["P1"], bulk["P2"]
    A, B, C = part["A"], part["B"], part["C"]

    # L3 theta coefficients: Q_i(z) = Q[i] = [z^0, z^1, z^2] entries
    t0 = _polyshift(P2, -2)   # z^0 polynomial in theta
    t1 = _polyshift(P1, -1)   # z^1
    t2 = _polyshift(P0, 0)    # z^2
    deg = 4
    L3 = [[0] * 3 for _ in range(deg)]
    for i in range(deg):
        L3[i][0] = t0[i] if i < len(t0) else 0
        L3[i][1] = t1[i] if i < len(t1) else 0
        L3[i][2] = t2[i] if i < len(t2) else 0
    # L2 theta coefficients
    s0 = _polyshift(C, -1)
    s1 = [-x for x in _polyshift(A, 0)]
    s2 = [-x for x in _polyshift(B, 1)]
    L2 = [[0] * 3 for _ in range(3)]
    for i in range(3):
        L2[i][0] = s0[i] if i < len(s0) else 0
        L2[i][1] = s1[i] if i < len(s1) else 0
        L2[i][2] = s2[i] if i < len(s2) else 0
    # MUM sanity: indicial polys th^3 / th^2
    chk(L3[0][0] == 0 and L3[1][0] == 0 and L3[2][0] == 0 and L3[3][0] == 1,
        f"{family}: L3 not MUM-normalized (th^3 indicial)")
    chk(L2[0][0] == 0 and L2[1][0] == 0 and L2[2][0] == 1,
        f"{family}: L2 not MUM-normalized (th^2 indicial)")
    return L2, L3


def cross_check_lean_provenance(family, L3):
    """Assert the refs-derived L3 equals the Lean-provenance table in
    scripts/compute_L3_monodromy.py (independent transcription route)."""
    sys.path.insert(0, str(REPO / "scripts"))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "l3mono", REPO / "scripts" / "compute_L3_monodromy.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    z = mod.z
    ops = mod.L3_OPERATORS[family]
    for i, key in enumerate(["Q0", "Q1", "Q2", "Q3"]):
        got = sp.Poly(ops[key], z).all_coeffs()[::-1]
        got = [int(x) for x in got] + [0] * (3 - len(got))
        chk(got[:3] == L3[i], f"{family}: refs-derived L3 {key} {L3[i]} != Lean table {got[:3]}")


# ----------------------------------------------------------------------------
# exact power-series helpers (Fraction lists)
# ----------------------------------------------------------------------------

def smul(a, b, n=NQ):
    r = [Fr(0)] * n
    for i, ai in enumerate(a[:n]):
        if ai:
            for j, bj in enumerate(b[: n - i]):
                if bj:
                    r[i + j] += ai * bj
    return r


def sadd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else Fr(0)) + (b[i] if i < len(b) else Fr(0)) for i in range(n)]


def sinv(a, n=NQ):
    chk(a[0] != 0, "sinv: zero constant term")
    r = [Fr(0)] * n
    r[0] = Fr(1) / a[0]
    for k in range(1, n):
        s = Fr(0)
        for j in range(1, k + 1):
            if j < len(a) and a[j]:
                s += a[j] * r[k - j]
        r[k] = -s / a[0]
    return r


def sexp(a, n=NQ):
    chk(a[0] == 0, "sexp: nonzero constant term")
    e = [Fr(0)] * n
    e[0] = Fr(1)
    for k in range(1, n):
        s = Fr(0)
        for j in range(1, k + 1):
            aj = a[j] if j < len(a) else Fr(0)
            if aj:
                s += j * aj * e[k - j]
        e[k] = s / k
    return e


def scompose(a, b, n=NQ):
    chk(b[0] == 0, "scompose: b(0) != 0")
    r = [Fr(0)] * n
    pw = [Fr(0)] * n
    pw[0] = Fr(1)
    for k in range(n):
        ak = a[k] if k < len(a) else Fr(0)
        if ak:
            r = sadd(r, [ak * x for x in pw])[:n]
        pw = smul(pw, b, n)
    return r[:n]


def srevert(a, n=NQ):
    chk(a[0] == 0 and a[1] != 0, "srevert: need a = a1 z + ...")
    g = [Fr(0), Fr(1) / a[1]] + [Fr(0)] * (n - 2)
    for _ in range(16):
        comp = scompose(a, g, n)
        err = [(Fr(1) if i == 1 else Fr(0)) - comp[i] for i in range(n)]
        if all(x == 0 for x in err):
            break
        da = [i * a[i] for i in range(1, len(a))]
        dag = scompose(da, g, n)
        g = sadd(g, smul(err, sinv(dag, n), n))[:n]
    comp = scompose(a, g, n)
    chk(comp[1] == 1 and all(comp[i] == 0 for i in range(n) if i != 1), "srevert: no convergence")
    return g


def holo_series(L, n):
    """Holomorphic Frobenius solution at MUM z=0, a0 = 1 (theta form)."""
    a = [Fr(0)] * n
    a[0] = Fr(1)
    for m in range(1, n):
        s, lead = Fr(0), Fr(0)
        for i, Qi in enumerate(L):
            for j, qij in enumerate(Qi):
                if qij and j <= m:
                    if j == 0:
                        lead += qij * Fr(m) ** i
                    else:
                        s += qij * Fr(m - j) ** i * a[m - j]
        chk(lead != 0, f"holo_series: indicial degeneracy at m={m}")
        a[m] = -s / lead
    return a


def log_partner(L, a, n):
    """h with y1 = y0 log z + h a solution, h(0) = 0 (theta form).
    L(h) = -(sum_i i Q_i theta^(i-1)) y0."""
    h = [Fr(0)] * n
    for m in range(1, n):
        s, lead = Fr(0), Fr(0)
        for i, Qi in enumerate(L):
            for j, qij in enumerate(Qi):
                if qij and j <= m:
                    if j == 0:
                        lead += qij * Fr(m) ** i
                    else:
                        s += qij * Fr(m - j) ** i * h[m - j]
        r = Fr(0)
        for i, Qi in enumerate(L):
            if i == 0:
                continue
            for j, qij in enumerate(Qi):
                if qij and j <= m:
                    r += i * qij * Fr(m - j) ** (i - 1) * a[m - j]
        h[m] = (-r - s) / lead
    return h


def series_from_refs(family, which, n):
    """Regenerate the sequence from its refs recurrence (independent of the
    operator route); returns list of Fractions."""
    data = json.loads(REFS.read_text())["sequences"]
    key = FAMILIES[family][which]
    entry = data[key]["recurrence_coefficients"]
    if which == "bulk":
        P0, P1, P2 = entry["P0"], entry["P1"], entry["P2"]
        init = data[key]["initial_terms"][:2]
        a = [Fr(x) for x in init]
        for k in range(0, n - 2):
            p0 = sum(Fr(c) * k**i for i, c in enumerate(P0))
            p1 = sum(Fr(c) * k**i for i, c in enumerate(P1))
            p2 = sum(Fr(c) * k**i for i, c in enumerate(P2))
            a.append((-p0 * a[k] - p1 * a[k + 1]) / p2)
        return a[:n]
    A, B, C = entry["A"], entry["B"], entry["C"]
    if "initial_terms" in data[key]:
        init = data[key]["initial_terms"][:2]
        a = [Fr(x) for x in init]
    else:
        init = data[key]["initial_terms_rational"][:2]
        a = [Fr(x) for x in init]
    for k in range(1, n - 1):
        Ak = sum(Fr(c) * k**i for i, c in enumerate(A))
        Bk = sum(Fr(c) * k**i for i, c in enumerate(B))
        Ck = sum(Fr(c) * k**i for i, c in enumerate(C))
        a.append((Ak * a[k] + Bk * a[k - 1]) / Ck)
    return a[:n]


# ----------------------------------------------------------------------------
# STAGE 1 — exact q-series Yukawa (U1a-3)
# ----------------------------------------------------------------------------

def stage1_yukawa(family, L2, L3, scramble_mirror=False, verbose=True):
    n = NQ
    A = holo_series(L2, n)
    y0 = holo_series(L3, n)
    chk(A == series_from_refs(family, "partner", n),
        f"{family}: L2 holomorphic solution != refs partner recurrence series")
    chk(y0 == series_from_refs(family, "bulk", n),
        f"{family}: L3 holomorphic solution != refs bulk recurrence series")

    h2 = log_partner(L2, A, n)
    h3 = log_partner(L3, y0, n)
    zser = [Fr(0), Fr(1)] + [Fr(0)] * (n - 2)
    q2 = smul(zser, sexp(smul(h2, sinv(A, n), n), n), n)
    q3 = smul(zser, sexp(smul(h3, sinv(y0, n), n), n), n)
    chk(q2 == q3, f"{family}: mirror map from L2 != mirror map from L3")

    zq = srevert(q3, n)
    if scramble_mirror:
        zq = list(zq)
        zq[5] += Fr(1)  # deliberate corruption (negative control only)

    # external validation against the pinned Hauptmodul b-file, when available
    hb = FAMILIES[family]["hauptmodul_bfile"]
    haupt_match = None
    if hb:
        bf = REPO / "refs" / hb
        chk(bf.exists(), f"missing b-file {bf}")
        d = {}
        for line in bf.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                p = line.split()
                d[int(p[0])] = int(p[1])
        upto = min(n, max(d) + 1)
        haupt_match = all(zq[m] == d.get(m) for m in range(1, upto))
        if not scramble_mirror:
            chk(haupt_match, f"{family}: mirror map z(q) != pinned Hauptmodul b-file {hb}")

    # Y_zz = C exp(-(2/3) int a2/a3), a3 = Q3 z^3, a2 = (3 Q3 + Q2) z^2 (d/dz form).
    # exponents from exact residues of (3Q3+Q2)/(z Q3):
    z = sp.Symbol("z")
    Q3p = sum(sp.Integer(L3[3][j]) * z**j for j in range(3))
    Q2p = sum(sp.Integer(L3[2][j]) * z**j for j in range(3))
    R = sp.cancel((3 * Q3p + Q2p) / (z * Q3p))
    roots = sp.solve(sp.Eq(Q3p, 0), z)
    chk(all(r.is_real for r in roots), f"{family}: non-real singular locus {roots}")
    pts = [sp.Integer(0)] + sorted(roots, key=lambda r: sp.Rational(r))
    exps = {}
    for r in pts:
        rho = sp.residue(R, z, r)
        e = sp.Rational(-2, 3) * rho
        chk(e.is_integer, f"{family}: non-integer Yukawa exponent {e} at z={r}")
        exps[r] = int(e)
    chk(exps[sp.Integer(0)] == -2, f"{family}: exponent at 0 is {exps[sp.Integer(0)]}, not -2")

    # Y_tt(q) = z(q)^-2 * prod (1 - z/r)^{e_r} * (q dz/dq)^2 / y0(z(q))^2, C = 1
    qdz = [i * zq[i] for i in range(n)]
    num = smul(qdz, qdz, n)
    den = smul(zq, zq, n)
    for r in pts:
        if r == 0:
            continue
        rq = Fr(int(sp.Rational(r).p), int(sp.Rational(r).q))
        fac = sadd([Fr(1)], [-x / rq for x in zq])[:n]
        e = exps[r]
        chk(e < 0, f"{family}: unexpected positive exponent {e}")
        for _ in range(-e):
            den = smul(den, fac, n)
    y0q = scompose(y0, zq, n)
    den = smul(den, smul(y0q, y0q, n), n)
    chk(num[0] == num[1] == 0 and den[0] == den[1] == 0, "stage1: leading orders wrong")
    num_s = num[2:]
    den_s = den[2:]
    m = len(num_s)
    Ytt = smul(num_s, sinv(den_s, m), m)
    valid = m - 2  # the two top orders are truncation-contaminated by the shift
    constant = Ytt[0]
    tail_ok = all(Ytt[i] == 0 for i in range(1, valid))
    if verbose:
        print(f"  [stage1] {family}: mirror maps L2==L3 agree exactly to q^{n-1}")
        if haupt_match is not None:
            print(f"  [stage1] z(q) == pinned Hauptmodul b-file: {haupt_match}")
        print(f"  [stage1] Yukawa exponents (derived): {[(str(r), exps[r]) for r in pts]}")
        print(f"  [stage1] Y_tt(q) constant to q^{valid - 1}: {tail_ok}; "
              f"constant = {constant} (in the C=1 normalization)")
        print("  [stage1] FINDING: the constancy is the checkable content; the VALUE is a "
              "normalization convention here and is fixed only by the stage-3 integral "
              "lattice (see brief).")
    chk(tail_ok, f"{family}: Yukawa q-series NOT constant - pipeline bug (or scrambled control)")
    return {"yukawa_constant_C1_norm": str(constant), "constant_to_order": valid - 1,
            "hauptmodul_match": haupt_match,
            "value_independent": False,
            "value_note": "value is convention until fixed by the integral lattice (stage 3)"}


# ----------------------------------------------------------------------------
# STAGE 2 — numerical monodromy of L2 (mpmath, precision-tracked)
# ----------------------------------------------------------------------------

def dz_form(L2):
    """theta form [Q0,Q1,Q2] (z-coeff lists) -> d/dz form a2 y'' + a1 y' + a0 y,
    divided by one z:  a2 = z Q2, a1 = Q2 + Q1, a0 = Q0/z (exact int lists)."""
    Q0, Q1, Q2 = L2[0], L2[1], L2[2]
    chk(Q0[0] == 0, "dz_form: Q0 not divisible by z")
    a2 = [0] + list(Q2)
    a1 = [Q2[i] + Q1[i] for i in range(3)]
    a0 = [Q0[i + 1] for i in range(len(Q0) - 1)]
    return a2, a1, a0


class Continuator:
    def __init__(self, L2, loci):
        self.a2, self.a1, self.a0 = dz_form(L2)
        self.sing = [mp.mpf(0)] + [mp.mpf(x.p) / mp.mpf(x.q) for x in loci]

    def _shift(self, p, z0):
        out = [mp.mpc(0)] * len(p)
        for k, pk in enumerate(p):
            if pk == 0:
                continue
            for j in range(k + 1):
                out[j] += pk * mp.binomial(k, j) * z0 ** (k - j)
        return out

    def step(self, p, y, dy, h):
        a2 = self._shift(self.a2, p)
        a1 = self._shift(self.a1, p)
        a0 = self._shift(self.a0, p)
        c = [y, dy]
        for k in range(TAYLOR_ORDER - 2):
            s = mp.mpc(0)
            for j in range(1, min(len(a2) - 1, k) + 1):
                s += a2[j] * (k - j + 2) * (k - j + 1) * c[k - j + 2]
            for j in range(0, min(len(a1) - 1, k) + 1):
                s += a1[j] * (k - j + 1) * c[k - j + 1]
            for j in range(0, min(len(a0) - 1, k) + 1):
                s += a0[j] * c[k - j]
            c.append(-s / (a2[0] * (k + 2) * (k + 1)))
        val = mp.mpc(0)
        dval = mp.mpc(0)
        for k in reversed(range(len(c))):
            val = val * h + c[k]
        for k in reversed(range(1, len(c))):
            dval = dval * h + k * c[k]
        tail = abs(c[-1]) * abs(h) ** (len(c) - 1) + abs(c[-2]) * abs(h) ** (len(c) - 2)
        return val, dval, tail

    def continue_path(self, waypoints, y, dy):
        p = waypoints[0]
        maxtail = mp.mpf(0)
        for target in waypoints[1:]:
            while abs(target - p) > 0:
                dmax = STEP_RATIO * min(abs(p - s) for s in self.sing)
                step = target - p
                if abs(step) > dmax:
                    step = step / abs(step) * dmax
                y, dy, tail = self.step(p, y, dy, step)
                maxtail = max(maxtail, tail)
                p += step
        return y, dy, maxtail


def circle(center, radius, start_angle, npts=24):
    return [center + radius * mp.exp(1j * (start_angle + 2 * mp.pi * k / npts))
            for k in range(npts + 1)]


def build_loops(loci, z0):
    """Counterclockwise loops from base z0 around each finite locus, avoiding
    all other singular points. Loci are real; positive loci are approached
    along the real axis, negative loci over the upper half plane."""
    loops = {}
    allpts = [mp.mpf(0)] + [mp.mpf(x.p) / mp.mpf(x.q) for x in loci]
    for loc in loci:
        zc = mp.mpf(loc.p) / mp.mpf(loc.q)
        others = [s for s in allpts if abs(s - zc) > mp.mpf(10) ** -12]
        gap = min(abs(zc - s) for s in others)
        R = min(gap / 2, abs(zc) / 2)
        if zc > 0:
            entry = zc - R
            loops[str(loc)] = [z0, entry] + circle(zc, R, mp.pi) + [entry, z0]
        else:
            h = mp.mpc(0, R)
            loops[str(loc)] = ([z0, z0 + h, zc + h] + circle(zc, R, mp.pi / 2)
                               + [zc + h, z0 + h, z0])
    return loops


def stage2_monodromy(family, L2, verbose=True):
    z = sp.Symbol("z")
    Q2p = sum(sp.Integer(L2[2][j]) * z**j for j in range(3))
    loci = sorted([sp.Rational(r) for r in sp.solve(sp.Eq(Q2p, 0), z)])
    chk(len(loci) == 2, f"{family}: expected 2 finite loci, got {loci}")
    if verbose:
        print(f"  [stage2] finite singular loci (roots of Q2, computed): {loci}")

    n = NSER
    A = [Fr(x) for x in series_from_refs(family, "partner", n)]
    # log partner for L2 at full length
    h = log_partner(L2, A, n)

    rho = min(abs(mp.mpf(x.p) / mp.mpf(x.q)) for x in loci)
    z0 = rho / 4
    tail_series = abs(mp.mpf(A[-1].numerator) / mp.mpf(A[-1].denominator)) * z0 ** (n - 1)
    chk(tail_series < mp.mpf(10) ** -45, f"{family}: base-point series tail too large: {tail_series}")

    def ev(coeffs, zz, deriv=False):
        val = mp.mpf(0)
        for k in reversed(range(len(coeffs))):
            val = val * zz + mp.mpf(coeffs[k].numerator) / mp.mpf(coeffs[k].denominator)
        if not deriv:
            return val
        dv = mp.mpf(0)
        for k in reversed(range(1, len(coeffs))):
            dv = dv * zz + k * (mp.mpf(coeffs[k].numerator) / mp.mpf(coeffs[k].denominator))
        return val, dv

    Aval, Ader = ev(A, z0, deriv=True)
    gval, gder = ev(h, z0, deriv=True)
    twopii = 2j * mp.pi
    Bval = (Aval * mp.log(z0) + gval) / twopii
    Bder = (Ader * mp.log(z0) + Aval / z0 + gder) / twopii

    cont = Continuator(L2, loci)
    W = mp.matrix([[Aval, Bval], [Ader, Bder]])

    def monodromy(waypoints):
        Ay, Ad, t1 = cont.continue_path(waypoints, Aval, Ader)
        By, Bd, t2 = cont.continue_path(waypoints, Bval, Bder)
        col1 = mp.lu_solve(W, mp.matrix([Ay, Ad]))
        col2 = mp.lu_solve(W, mp.matrix([By, Bd]))
        return mp.matrix([[col1[0], col2[0]], [col1[1], col2[1]]]), max(t1, t2)

    # machinery control: numeric loop around 0 must give [[1,1],[0,1]]
    M0n, tail0 = monodromy(circle(mp.mpf(0), z0, 0))
    ref = mp.matrix([[1, 1], [0, 1]])
    err0 = max(abs(M0n[i, j] - ref[i, j]) for i in range(2) for j in range(2))
    chk(err0 < TOL_NUM, f"{family}: cusp-loop machinery control failed, err={err0}")
    if verbose:
        print(f"  [stage2] cusp-loop machinery control: |M0_num - [[1,1],[0,1]]| = "
              f"{mp.nstr(err0, 3)}  (tail {mp.nstr(tail0, 3)})")

    loops = build_loops(loci, z0)
    Ms = {}
    for loc in loci:
        M, tail = monodromy(loops[str(loc)])
        chk(tail < mp.mpf(10) ** -45, f"{family}: continuation tail too large at {loc}: {tail}")
        det = M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]
        sq = M * M
        errI = max(abs(sq[i, j] - (1 if i == j else 0)) for i in range(2) for j in range(2))
        chk(abs(det + 1) < TOL_NUM, f"{family}: det M({loc}) = {det}, expected -1 (exponents 0,1/2)")
        chk(errI < TOL_NUM, f"{family}: M({loc})^2 != I numerically, err={errI}")
        if verbose:
            print(f"  [stage2] M({loc}): det = -1, M^2 = I to {mp.nstr(errI, 3)}")
            print("           " + mp.nstr(M, 17).replace("\n", "\n           "))
        Ms[str(loc)] = M

    # Sym^2 in the flag basis (A^2, A*Bhat, Bhat^2); convention new = old * M
    def sym2(M):
        m00, m01, m10, m11 = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
        return mp.matrix([
            [m00**2, m00 * m01, m01**2],
            [2 * m00 * m10, m00 * m11 + m01 * m10, 2 * m01 * m11],
            [m10**2, m10 * m11, m11**2],
        ])

    Ns_num = {k: sym2(M) for k, M in Ms.items()}

    # rational recognition with loud tolerance gates
    def recognize(Mn, label):
        out = sp.zeros(3, 3)
        for i in range(3):
            for j in range(3):
                x = Mn[i, j]
                chk(abs(mp.im(x)) < TOL_REC, f"{family}: {label}[{i}{j}] has imaginary part "
                    f"{mp.nstr(mp.im(x), 3)} - not real-rational")
                fr = Fr(str(mp.re(x))).limit_denominator(MAX_DEN)
                err = abs(mp.re(x) - mp.mpf(fr.numerator) / mp.mpf(fr.denominator))
                chk(err < TOL_REC, f"{family}: {label}[{i}{j}] = {mp.nstr(x, 30)} not rational "
                    f"within tolerance (best {fr}, err {mp.nstr(err, 3)})")
                out[i, j] = sp.Rational(fr.numerator, fr.denominator)
        return out

    Ns = {k: recognize(v, f"Sym2 M({k})") for k, v in Ns_num.items()}
    dens = sorted({x.q for Nk in Ns.values() for x in Nk})
    if verbose:
        for k, Nk in Ns.items():
            print(f"  [stage2] Sym^2 monodromy at z={k} recognized exactly:")
            for row in Nk.tolist():
                print(f"             {row}")
        print(f"  [stage2] denominators appearing: {dens}")
    return loci, Ns, {"cusp_control_err": float(err0), "recognition_denominators": [int(x) for x in dens]}


# ----------------------------------------------------------------------------
# STAGE 3 — exact lattice pipeline
# ----------------------------------------------------------------------------

def stage3_lattice(family, L2, loci, Ns, scramble=False, verbose=True):
    N0 = sp.Matrix([[1, 1, 1], [0, 1, 2], [0, 0, 1]])  # Sym^2 of [[1,1],[0,1]] (cusp)
    gens = [N0] + [Ns[str(l)] for l in loci]
    if scramble == "entry":
        gens[1] = gens[1].copy()
        gens[1][0, 2] += 1  # breaks involutivity -> caught at the first exact gate
    elif scramble == "conjugate":
        # an involution NOT in the joint group: conjugate one elliptic matrix by a
        # unipotent that does not commute with the structure. Involutivity survives;
        # the joint invariant form / lattice steps must then fail.
        S = sp.Matrix([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
        gens[1] = S * gens[1] * S.inv()

    for i, Nk in enumerate(gens[1:], 1):
        chk(Nk**2 == sp.eye(3), f"{family}: elliptic Sym^2 matrix #{i} is not an involution")

    # product relation with the loop at infinity, derived from the L2 indicial
    # equation at z = infinity (computed, not typed): exponents rho1, rho2 give
    # Sym^2 infinity-eigenvalues e^{2 pi i e}, e in {2 rho1, rho1+rho2, 2 rho2}.
    rho = sp.Symbol("rho")
    ind_inf = sum(sp.Integer(L2[i][2]) * (-rho) ** i for i in range(3))
    rinf = sp.solve(sp.Eq(ind_inf, 0), rho)
    chk(len(rinf) == 2, f"{family}: infinity indicial equation not order 2: {rinf}")
    r1, r2 = sorted(sp.Rational(x) for x in rinf)
    e_list = [2 * r1, r1 + r2, 2 * r2]
    exp_re = sp.simplify(sum(sp.cos(2 * sp.pi * e) for e in e_list))
    exp_im = sp.simplify(sum(sp.sin(2 * sp.pi * e) for e in e_list))
    chk(exp_im == 0 and exp_re.is_integer,
        f"{family}: expected infinity trace {exp_re}+{exp_im}i not an integer")
    exp_trace = sp.Integer(exp_re)
    m_ord = int(sp.lcm([sp.Rational(e).q for e in e_list]))
    import itertools
    infty_orders = []
    for perm in itertools.permutations(range(3)):
        P = gens[perm[0]] * gens[perm[1]] * gens[perm[2]]
        if P.trace() == exp_trace and P**m_ord == sp.eye(3):
            infty_orders.append(perm)
    chk(infty_orders, f"{family}: no ordering of the three loops matches the "
        f"infinity monodromy (expected trace {exp_trace}, order dividing {m_ord})")
    if verbose:
        print(f"  [stage3] exact: elliptic Sym^2 involutions OK; infinity product "
              f"(exponents {r1},{r2} -> trace {exp_trace}, order | {m_ord}) for "
              f"orderings {infty_orders}")

    # joint invariant symmetric bilinear form
    gsym = sp.symbols("g11 g12 g13 g22 g23 g33")
    G = sp.Matrix([[gsym[0], gsym[1], gsym[2]],
                   [gsym[1], gsym[3], gsym[4]],
                   [gsym[2], gsym[4], gsym[5]]])
    eqs = []
    for M in gens:
        E = M.T * G * M - G
        eqs.extend([E[i, j] for i in range(3) for j in range(i, 3)])
    sol = sp.solve(eqs, gsym, dict=True)
    chk(len(sol) == 1, f"{family}: invariant-form solve returned {len(sol)} branches")
    Gs = G.subs(sol[0])
    free = sorted(Gs.free_symbols, key=str)
    chk(len(free) == 1, f"{family}: invariant form space has dim {len(free)}, not 1 "
        "(scrambled matrices land here)")
    # sign fixed by stage 0: (mu, mubar) = 4 n y^2 > 0 => flag middle entry positive
    Gs = Gs.subs(free[0], 1)
    if Gs[1, 1] < 0:
        Gs = -Gs
    chk(Gs[1, 1] > 0, f"{family}: cannot orient invariant form (G22 = {Gs[1, 1]})")

    # orbit lattice of the cusp-invariant vector f
    ker = (N0 - sp.eye(3)).nullspace()
    chk(len(ker) == 1, f"{family}: cusp fixed space has dim {len(ker)}")
    f = ker[0]
    vecs = [f]
    stable = False
    for _ in range(10):
        allv = list(vecs)
        for M in gens + [g.inv() for g in gens]:
            for v in vecs:
                allv.append(M * v)
        B = sp.Matrix.hstack(*allv)
        den = sp.lcm([x.q for x in B])
        H = hermite_normal_form((B * den).applyfunc(sp.Integer)) / sp.Integer(den)
        newvecs = [H[:, j] for j in range(H.shape[1])]
        if len(newvecs) == 3 and len(vecs) == 3 and sp.Matrix.hstack(*newvecs) == sp.Matrix.hstack(*vecs):
            stable = True
            break
        vecs = newvecs
    chk(stable, f"{family}: orbit lattice did not stabilize (scrambled matrices land here)")
    B = sp.Matrix.hstack(*vecs)
    for M in gens:
        X = B.inv() * M * B
        chk(all(x.q == 1 for x in X), f"{family}: lattice not closed under a generator")
    if verbose:
        print(f"  [stage3] orbit lattice of f stabilized; basis (flag coords) = {B.tolist()}")

    # Gram, primitive even rescale
    Gram_raw = B.T * Gs * B
    den = sp.lcm([x.q for x in Gram_raw])
    Gi = (Gram_raw * den).applyfunc(sp.Integer)
    gg = sp.gcd(list(Gi))
    Gi = (Gi / gg).applyfunc(sp.Integer)
    even = all(Gi[i, i] % 2 == 0 for i in range(3))
    chk(even, f"{family}: primitive integral Gram is not even: {Gi.tolist()}")
    det = Gi.det()

    # signature (exact real roots of the characteristic polynomial)
    lam = sp.Symbol("lam")
    cp = sp.Poly(Gi.charpoly(lam).as_expr(), lam)
    rts = cp.real_roots()
    chk(len(rts) == 3 and all(r != 0 for r in rts), f"{family}: degenerate Gram")
    sig = (sum(1 for r in rts if r > 0), sum(1 for r in rts if r < 0))

    # discriminant group and discriminant form
    S = smith_normal_form(Gi)
    elem = [int(S[i, i]) for i in range(3) if S[i, i] not in (1, -1)]
    Ginv = Gi.inv()
    # generators of the discriminant group in lattice coords: columns of Gi^{-1} * U-part;
    # for a report-level disc form we use the dual basis vectors with nontrivial order.
    disc_form = []
    for i in range(3):
        v = Ginv[:, i]
        order = sp.lcm([x.q for x in v])
        if order == 1:
            continue
        qval = sp.nsimplify((v.T * Gi * v)[0, 0])
        disc_form.append({"dual_basis_vector": i, "order": int(order),
                          "q_value_mod_2Z": str(sp.Rational(qval) % 2)})

    # derived 2n: divisibility of (N0 - 1)^2 Lambda inside Z f
    N0L = B.inv() * N0 * B
    Nsq = (N0L - sp.eye(3)) ** 2
    fL = B.solve(f)
    mults = []
    for j in range(3):
        v = Nsq[:, j]
        if v == sp.zeros(3, 1):
            continue
        k = None
        for i in range(3):
            if fL[i] != 0:
                k = v[i] / fL[i]
                break
        chk(v == k * fL, f"{family}: (N0-1)^2 image not along f")
        mults.append(k)
    chk(mults, f"{family}: (N0-1)^2 = 0 on the lattice")
    two_n = abs(sp.gcd(mults))
    chk(all(x.q == 1 for x in [sp.Rational(m) for m in mults]), f"{family}: non-integral multiples")

    # explicit U-splitting (constructive isometry: no genus theory needed)
    bil = lambda u, v: (u.T * Gi * v)[0, 0]
    pair = [bil(fL, sp.eye(3)[:, j]) for j in range(3)]
    divf = sp.gcd(pair)
    splitting = None
    if divf == 1:
        # v with <f, v> = 1, then e = v - (Q(v)/2) f isotropic, <f,e> = 1
        found = None
        rng = range(-6, 7)
        for c0 in rng:
            for c1 in rng:
                for c2 in rng:
                    if c0 * pair[0] + c1 * pair[1] + c2 * pair[2] == 1:
                        found = sp.Matrix([c0, c1, c2])
                        break
                if found is not None:
                    break
            if found is not None:
                break
        chk(found is not None, f"{family}: no small vector with <f,v>=1 found")
        v = found
        Qv = bil(v, v)
        chk(Qv % 2 == 0, f"{family}: Q(v) odd on an even lattice - contradiction")
        e = v - (Qv / 2) * fL
        chk(bil(e, e) == 0 and bil(fL, e) == 1, f"{family}: U-completion failed")
        # complement: primitive generator of the kernel of pairing with (f, e).
        # Since U = <f,e> is unimodular, Lambda = U + (U-perp cap Lambda) splits.
        Kmat = sp.Matrix.vstack((Gi * fL).T, (Gi * e).T)
        kern = Kmat.nullspace()
        chk(len(kern) == 1, f"{family}: U-perp not rank 1")
        w = kern[0]
        w = w * sp.lcm([x.q for x in w])
        w = (w / sp.gcd([sp.Integer(x) for x in w])).applyfunc(sp.Integer)
        T = sp.Matrix.hstack(fL, e, w)
        chk(abs(T.det()) == 1, f"{family}: splitting base change not unimodular "
            f"(det {T.det()})")
        Gsplit = T.T * Gi * T
        d = Gsplit[2, 2]
        target = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, d]])
        chk(Gsplit == target, f"{family}: splitting Gram is {Gsplit.tolist()}, not U + <d>")
        chk(abs(det) == abs(d), f"{family}: internal inconsistency det vs splitting")
        # explicit witness matrix P = T = [f | e | w] (columns), so that
        # P^T Gi P = Gsplit = gram_after. Serialized alongside basis_change_det
        # so third parties don't have to re-derive P themselves (T0 ruling
        # 2026-07-27, motivated by Stream 1's independent-verification finding
        # that only det(P) and P^T G P were being recorded, not P itself; see
        # briefs/STREAM2_P_WITNESS_SERIALIZATION_2026_07_27.md).
        splitting = {"basis_change_det": int(T.det()), "d": int(d),
                     "basis_change_matrix": [[int(x) for x in row] for row in T.tolist()],
                     "gram_after": [[int(x) for x in row] for row in Gsplit.tolist()]}
    chk(int(two_n) == int(abs(det)), f"{family}: derived 2n {two_n} != |det| {abs(det)} "
        "(internal consistency)")

    # proper even invariant overlattices (isotropic invariant subgroups of disc group)
    # disc group here: enumerate x in L^dual / L via SNF; keep it simple for |det| small.
    overlattices = 0
    adet = int(abs(det))
    if adet <= 400 and len(elem) == 1:
        m = elem[0]
        # dual generator with order m:
        gen = None
        for i in range(3):
            v = Ginv[:, i]
            if sp.lcm([x.q for x in v]) == m:
                gen = v
                break
        chk(gen is not None, f"{family}: no cyclic disc generator found")
        for a in range(1, m):
            x = a * gen
            qx = sp.Rational((x.T * Gi * x)[0, 0])
            ordx = m // sp.gcd(a, m)
            if ordx == 1:
                continue
            if qx % 2 == 0:  # isotropic element -> candidate even overlattice
                overlattices += 1
    if verbose:
        print(f"  [stage3] primitive even Gram (lattice basis): {Gi.tolist()}")
        print(f"  [stage3] det = {det}   signature = {sig}   disc group elementary divisors = {elem}")
        print(f"  [stage3] disc form on dual generators (q mod 2Z): {disc_form}")
        print(f"  [stage3] derived 2n from (T_cusp - 1)^2 divisibility: {two_n}")
        if splitting:
            print(f"  [stage3] EXPLICIT U-splitting found: Gram -> U + <{splitting['d']}> "
                  f"via integral base change (det {splitting['basis_change_det']})")
        print(f"  [stage3] proper even invariant overlattices: {overlattices}")
    return {
        "gram_primitive_even": [[int(x) for x in row] for row in Gi.tolist()],
        "det": int(det),
        "signature": [int(sig[0]), int(sig[1])],
        "disc_group_elementary_divisors": elem,
        "disc_form": disc_form,
        "derived_2n": int(two_n),
        "u_splitting": splitting,
        "proper_even_invariant_overlattices": int(overlattices),
    }


# ----------------------------------------------------------------------------
# pipeline driver
# ----------------------------------------------------------------------------

def run_family(family, scramble=None, scramble_mirror=False, verbose=True):
    chk(family in FAMILIES, f"unknown family {family}")
    if verbose:
        print(f"=== U1 pipeline: {family} ===")
    L2, L3 = load_operators(family)
    cross_check_lean_provenance(family, L3)
    if verbose:
        print(f"  [ops] L2/L3 derived from refs recurrences; L3 cross-checked against "
              f"the Lean-provenance table in scripts/compute_L3_monodromy.py")
    y = stage1_yukawa(family, L2, L3, scramble_mirror=scramble_mirror, verbose=verbose)
    loci, Ns, s2info = stage2_monodromy(family, L2, verbose=verbose)
    lat = stage3_lattice(family, L2, loci, Ns, scramble=scramble, verbose=verbose)
    return {"family": family, "loci": [str(l) for l in loci], "stage1": y,
            "stage2": s2info, "stage3": lat}


# ----------------------------------------------------------------------------
# controls (also runnable via checkers/test_U1_controls.py)
# ----------------------------------------------------------------------------

def control_different_level(res_s7=None, verbose=True):
    """Identical pipeline on cooper_s10 must produce a DIFFERENT lattice."""
    if res_s7 is None:
        res_s7 = run_family("cooper_s7", verbose=False)
    res_s10 = run_family("cooper_s10", verbose=verbose)
    d7, d10 = res_s7["stage3"]["det"], res_s10["stage3"]["det"]
    n7, n10 = res_s7["stage3"]["derived_2n"], res_s10["stage3"]["derived_2n"]
    chk(d10 != d7, f"different-level control FAILED: s10 det {d10} == s7 det {d7}")
    chk(n10 != n7, f"different-level control FAILED: s10 2n {n10} == s7 2n {n7}")
    if verbose:
        print(f"  [control] different-level: s7 det={d7}, 2n={n7}; s10 det={d10}, 2n={n10} "
              f"- pipeline discriminates: PASS")
    return res_s10


def control_scrambled(verbose=True):
    """Perturbing one elliptic Sym^2 matrix must break the pipeline - both for a
    raw entry perturbation (caught at the involution gate) and for a corrupted
    involution (caught at the joint invariant-form / lattice step)."""
    for mode in ("entry", "conjugate"):
        try:
            run_family("cooper_s7", scramble=mode, verbose=False)
        except ControlFailure as e:
            if verbose:
                print(f"  [control] scrambled-matrix ({mode}): pipeline failed loudly "
                      f"as required: PASS")
                print(f"            ({e})")
            continue
        raise ControlFailure(f"scrambled-matrix control ({mode}) FAILED: pipeline "
                             "accepted a corrupted matrix")
    return True


def control_yukawa_scramble(verbose=True):
    """Perturbing the mirror map must break Yukawa constancy (the constancy
    check must be able to fail)."""
    L2, L3 = load_operators("cooper_s7")
    try:
        stage1_yukawa("cooper_s7", L2, L3, scramble_mirror=True, verbose=False)
    except ControlFailure as e:
        if verbose:
            print(f"  [control] yukawa-scramble: constancy check failed loudly as required: PASS")
        return True
    raise ControlFailure("yukawa-scramble control FAILED: constancy check accepted a corrupted map")


# ----------------------------------------------------------------------------
# certificate
# ----------------------------------------------------------------------------

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def emit_cert(res_s7, res_s10):
    lat = res_s7["stage3"]
    cert = {
        "certificate": "C2_cooper_s7_v4_DRAFT",
        "status": "DRAFT - pending T0 (Xavier) review; does NOT supersede C2_cooper_s7_v3.json",
        "checker": "check_U1_lattice.py",
        "checker_version": "1.0.0",
        "date": "2026-07-27",
        "operator": "cooper_s7",
        "claim": (
            "The joint monodromy-invariant lattice of the cooper_s7 family "
            "(orbit lattice of the cusp-invariant isotropic vector under the "
            "computed monodromy group, primitive even scaling) is isometric to "
            "U + <14> by an explicit integral base change. Identification of this "
            "lattice with the transcendental lattice T of the family is Tier B via "
            "the read framework sources (Dolgachev Thm 7.1/sec 7 p.20, Doran Thm 5.13)."
        ),
        "derived": {
            "gram_primitive_even": lat["gram_primitive_even"],
            "det": lat["det"],
            "signature": lat["signature"],
            "disc_group_elementary_divisors": lat["disc_group_elementary_divisors"],
            "disc_form": lat["disc_form"],
            "derived_2n_from_cusp_unipotent": lat["derived_2n"],
            "u_splitting": lat["u_splitting"],
            "proper_even_invariant_overlattices": lat["proper_even_invariant_overlattices"],
            "yukawa": res_s7["stage1"],
        },
        "how": {
            "stage0": "Dolgachev sec-7 framework re-derived symbolically (sympy) before use",
            "stage1": "exact q-series Yukawa; constancy asserted; VALUE is normalization-"
                      "dependent and NOT claimed as independent evidence (see brief)",
            "stage2": f"numerical analytic continuation at {DPS} dps, Taylor order "
                      f"{TAYLOR_ORDER}; cusp-loop machinery control err "
                      f"{res_s7['stage2']['cusp_control_err']:.2e}; rational recognition "
                      f"tolerance 1e-35, denominators {res_s7['stage2']['recognition_denominators']}",
            "stage3": "exact sympy rational lattice pipeline; all structural conditions asserted",
        },
        "controls": {
            "different_level_cooper_s10": {
                "det": res_s10["stage3"]["det"],
                "derived_2n": res_s10["stage3"]["derived_2n"],
                "discriminates": True,
            },
            "scrambled_matrix": "pipeline fails loudly (test_U1_controls.py)",
            "yukawa_scramble": "constancy check fails loudly (test_U1_controls.py)",
        },
        "tier": "B",
        "tier_reason": (
            "monodromy entries enter via numerical recognition (60-digit numerics, "
            "1e-35 gate, exact structural post-verification); lattice-to-T "
            "identification cites read framework theorems; not kernel-proven"
        ),
        "u1b_status": (
            "NOT NEEDED in the Eichler/genus form: an explicit integral base change "
            "realizing U + <14> was found and verified exactly, which is stronger than "
            "a one-class-genus argument for this lattice. Cassels Ch. 11 therefore not "
            "fetched; no 2-adic spinor-norm claim is made anywhere."
        ),
        "not_claimed": [
            "no Kodaira fibre types (E-007/E-008/E-009 stand)",
            "no physical coupling of any kind (VISION sec 1.3)",
            "rho/T ranks unchanged (ρ=19, T=3 per C2_cooper_s7_v3.json, E-011)",
            "no claim about which lattice T is beyond the stated Tier-B identification",
        ],
        "refs_sha256": {
            "recurrences_v1.json": sha256(REFS),
            "oeis_A279618_bfile.txt": sha256(REPO / "refs" / "oeis_A279618_bfile.txt"),
        },
        "provenance": "Generated-by: Fable 5 (Stream 2) | Verified-by: check_U1_lattice.py "
                      "structural assertions + test_U1_controls.py | Reviewed-by: pending T0 (Xavier)",
    }
    out = REPO / "data" / "certificates" / "C2_cooper_s7_v4_DRAFT.json"
    out.write_text(json.dumps(cert, indent=2))
    print(f"\nWrote {out.relative_to(REPO)} (DRAFT, pending T0)")


def emit_cert_v5(res_s7, res_s10):
    """v5 DRAFT: same derived/how/controls/tier content as C2_cooper_s7_v4.json
    (LIVE), plus ONE new field: derived.u_splitting.basis_change_matrix (the
    explicit integral base-change witness P, P^T G P = gram_after) — now
    serialized so third parties don't have to re-derive it. T0 RULING (Xavier,
    2026-07-27, verbal via coordinator): APPROVED, motivated by Stream 1's
    independent-verification finding (briefs/STREAM1_U1_INDEPENDENT_
    VERIFICATION_2026_07_27.md, Stream 1 repo) that the certificate recorded
    only det(P) and P^T G P, not P itself. Does NOT touch C2_cooper_s7_v4.json
    (LIVE) or C2_cooper_s7_v3.json (runtime rank source). Goes live only by a
    future, separate T0 acceptance."""
    lat = res_s7["stage3"]
    cert = {
        "certificate": "C2_cooper_s7_v5_DRAFT",
        "status": (
            "DRAFT - pending T0 (Xavier) review; does NOT supersede "
            "C2_cooper_s7_v4.json (LIVE) or C2_cooper_s7_v3.json. Adds ONE field "
            "vs v4 LIVE: derived.u_splitting.basis_change_matrix, the explicit "
            "base-change witness P (previously computed in stage3_lattice() but "
            "not serialized). All other derived/how/controls/tier field VALUES "
            "are unchanged from C2_cooper_s7_v4.json. Motivated by Stream 1's "
            "independent-verification finding "
            "(briefs/STREAM1_U1_INDEPENDENT_VERIFICATION_2026_07_27.md, Stream 1 "
            "repo). T0 RULING (Xavier, 2026-07-27, verbal via coordinator): "
            "APPROVED - serialize P in future certificate versions. Goes LIVE "
            "only by a future, separate T0 acceptance."
        ),
        "checker": "check_U1_lattice.py",
        "checker_version": "1.1.0",
        "date": "2026-07-27",
        "operator": "cooper_s7",
        "claim": (
            "The joint monodromy-invariant lattice of the cooper_s7 family "
            "(orbit lattice of the cusp-invariant isotropic vector under the "
            "computed monodromy group, primitive even scaling) is isometric to "
            "U + <14> by an explicit integral base change. Identification of this "
            "lattice with the transcendental lattice T of the family is Tier B via "
            "the read framework sources (Dolgachev Thm 7.1/sec 7 p.20, Doran Thm 5.13)."
        ),
        "derived": {
            "gram_primitive_even": lat["gram_primitive_even"],
            "det": lat["det"],
            "signature": lat["signature"],
            "disc_group_elementary_divisors": lat["disc_group_elementary_divisors"],
            "disc_form": lat["disc_form"],
            "derived_2n_from_cusp_unipotent": lat["derived_2n"],
            "u_splitting": lat["u_splitting"],
            "proper_even_invariant_overlattices": lat["proper_even_invariant_overlattices"],
            "yukawa": res_s7["stage1"],
        },
        "how": {
            "stage0": "Dolgachev sec-7 framework re-derived symbolically (sympy) before use",
            "stage1": "exact q-series Yukawa; constancy asserted; VALUE is normalization-"
                      "dependent and NOT claimed as independent evidence (see brief)",
            "stage2": f"numerical analytic continuation at {DPS} dps, Taylor order "
                      f"{TAYLOR_ORDER}; cusp-loop machinery control err "
                      f"{res_s7['stage2']['cusp_control_err']:.2e}; rational recognition "
                      f"tolerance 1e-35, denominators {res_s7['stage2']['recognition_denominators']}",
            "stage3": "exact sympy rational lattice pipeline; all structural conditions "
                      "asserted; basis_change_matrix is the in-memory witness T=[f|e|w] "
                      "(columns), now serialized rather than discarded",
        },
        "controls": {
            "different_level_cooper_s10": {
                "det": res_s10["stage3"]["det"],
                "derived_2n": res_s10["stage3"]["derived_2n"],
                "discriminates": True,
            },
            "scrambled_matrix": "pipeline fails loudly (test_U1_controls.py)",
            "yukawa_scramble": "constancy check fails loudly (test_U1_controls.py)",
            "witness_serialization": "checkers/check_U1_witness_serialization.py + "
                                     "checkers/test_U1_witness_serialization_controls.py "
                                     "(tampered P / tampered gram_after FAIL; missing "
                                     "witness on v3/v4 reported WITNESS_ABSENT, not FAIL)",
        },
        "tier": "B",
        "tier_reason": (
            "monodromy entries enter via numerical recognition (60-digit numerics, "
            "1e-35 gate, exact structural post-verification); lattice-to-T "
            "identification cites read framework theorems; not kernel-proven"
        ),
        "u1b_status": (
            "NOT NEEDED in the Eichler/genus form: an explicit integral base change "
            "realizing U + <14> was found and verified exactly, which is stronger than "
            "a one-class-genus argument for this lattice. Cassels Ch. 11 therefore not "
            "fetched; no 2-adic spinor-norm claim is made anywhere."
        ),
        "not_claimed": [
            "no Kodaira fibre types (E-007/E-008/E-009 stand)",
            "no physical coupling of any kind (VISION sec 1.3)",
            "rho/T ranks unchanged (ρ=19, T=3 per C2_cooper_s7_v3.json, E-011)",
            "no claim about which lattice T is beyond the stated Tier-B identification",
            "this v5 DRAFT is not live; C2_cooper_s7_v4.json remains the LIVE lattice "
            "certificate until a future, separate T0 acceptance of v5",
        ],
        "refs_sha256": {
            "recurrences_v1.json": sha256(REFS),
            "oeis_A279618_bfile.txt": sha256(REPO / "refs" / "oeis_A279618_bfile.txt"),
        },
        "provenance": "Generated-by: Sonnet 5 (Stream 2) | Verified-by: check_U1_lattice.py "
                      "structural assertions + test_U1_controls.py + "
                      "check_U1_witness_serialization.py + "
                      "test_U1_witness_serialization_controls.py | "
                      "Reviewed-by: pending T0 (Xavier) acceptance of v5",
    }
    out = REPO / "data" / "certificates" / "C2_cooper_s7_v5_DRAFT.json"
    out.write_text(json.dumps(cert, indent=2))
    print(f"\nWrote {out.relative_to(REPO)} (DRAFT, pending T0)")


def emit_cert_s10_v4(res_s10, res_s7):
    """s10 lattice certificate DRAFT, emitted directly at the s7-v5 bar
    (lattice claim + serialized basis_change_matrix witness). Numbering: the
    only existing s10 certificate is C2_cooper_s10_v3.json (rank ρ=19/T=3,
    LIVE) — there is no s10 lattice certificate at any version, so this v4
    DRAFT is the FIRST titled lattice claim for the family; no
    witness-less intermediate (s7's v4 stage) is emitted, per the T0 ruling
    (2026-07-27) that a splitting witness must be serialized, not implicit.
    Motivated by the gap stated in G0_NS_genus_cooper_s10.json's
    input_provenance.T_certificate_status (2026-08-01): the U+<20>
    identification existed only as a regression control and an unreviewed
    pipeline run. Roles are the mirror image of emit_cert_v5: cooper_s7 (LIVE
    v5, det -14) is the cross-family discriminating control here."""
    lat = res_s10["stage3"]
    cert = {
        "certificate": "C2_cooper_s10_v4_DRAFT",
        "status": (
            "DRAFT - pending T0 (Xavier) review; does NOT supersede "
            "C2_cooper_s10_v3.json (LIVE rank certificate, which stays the "
            "runtime rho/T source). FIRST titled lattice certificate for "
            "cooper_s10: emitted directly at the s7-v5 bar (serialized "
            "u_splitting.basis_change_matrix witness included from the start, "
            "per the 2026-07-27 T0 witness-serialization ruling; no "
            "witness-less v4-stage intermediate exists for this family). "
            "Until accepted, T(s10) ~= U+<20> remains formally UNCERTIFIED "
            "and downstream users (e.g. G0_NS_genus_cooper_s10.json) must "
            "keep saying so. Goes LIVE only by a separate T0 acceptance."
        ),
        "checker": "check_U1_lattice.py",
        "checker_version": "1.2.0",
        "date": "2026-08-01",
        "operator": "cooper_s10",
        "claim": (
            "The joint monodromy-invariant lattice of the cooper_s10 family "
            "(orbit lattice of the cusp-invariant isotropic vector under the "
            "computed monodromy group, primitive even scaling) is isometric to "
            "U + <20> by an explicit integral base change. Identification of this "
            "lattice with the transcendental lattice T of the family is Tier B via "
            "the read framework sources (Dolgachev Thm 7.1/sec 7 p.20, Doran Thm 5.13), "
            "exactly as for cooper_s7's C2_cooper_s7_v5.json — the pipeline is "
            "family-generic and no s10-specific framework step was added or skipped."
        ),
        "derived": {
            "gram_primitive_even": lat["gram_primitive_even"],
            "det": lat["det"],
            "signature": lat["signature"],
            "disc_group_elementary_divisors": lat["disc_group_elementary_divisors"],
            "disc_form": lat["disc_form"],
            "derived_2n_from_cusp_unipotent": lat["derived_2n"],
            "u_splitting": lat["u_splitting"],
            "proper_even_invariant_overlattices": lat["proper_even_invariant_overlattices"],
            "yukawa": res_s10["stage1"],
        },
        "how": {
            "stage0": "Dolgachev sec-7 framework re-derived symbolically (sympy) before use",
            "stage1": "exact q-series Yukawa; constancy asserted; VALUE is normalization-"
                      "dependent and NOT claimed as independent evidence (see s7 brief)",
            "stage2": f"numerical analytic continuation at {DPS} dps, Taylor order "
                      f"{TAYLOR_ORDER}; cusp-loop machinery control err "
                      f"{res_s10['stage2']['cusp_control_err']:.2e}; rational recognition "
                      f"tolerance 1e-35, denominators {res_s10['stage2']['recognition_denominators']}",
            "stage3": "exact sympy rational lattice pipeline; all structural conditions "
                      "asserted; basis_change_matrix is the in-memory witness T=[f|e|w] "
                      "(columns), serialized",
        },
        "controls": {
            "different_level_cooper_s7": {
                "det": res_s7["stage3"]["det"],
                "derived_2n": res_s7["stage3"]["derived_2n"],
                "discriminates": res_s7["stage3"]["det"] != lat["det"],
                "note": "mirror image of C2_cooper_s7_v5.json's own s10 control: "
                        "the LIVE s7 result (det -14) is the discriminating "
                        "cross-family control for this s10 certificate",
            },
            "scrambled_matrix": "pipeline fails loudly (test_U1_controls.py)",
            "yukawa_scramble": "constancy check fails loudly (test_U1_controls.py)",
            "witness_serialization": "checkers/check_U1_witness_serialization.py --cert "
                                     "data/certificates/C2_cooper_s10_v4_DRAFT.json "
                                     "(tampered P / tampered gram_after FAIL)",
        },
        "tier": "B",
        "tier_reason": (
            "monodromy entries enter via numerical recognition (60-digit numerics, "
            "1e-35 gate, exact structural post-verification); lattice-to-T "
            "identification cites read framework theorems; not kernel-proven. "
            "Same tier and same reasons as C2_cooper_s7_v5.json — nothing about "
            "the s10 run is weaker EXCEPT review status, which this DRAFT "
            "requests rather than claims."
        ),
        "u1b_status": (
            "NOT NEEDED in the Eichler/genus form: an explicit integral base change "
            "realizing U + <20> was found and verified exactly, which is stronger than "
            "a one-class-genus argument for this lattice. No 2-adic spinor-norm claim "
            "is made anywhere."
        ),
        "not_claimed": [
            "no Kodaira fibre types (E-007/E-008/E-009 stand)",
            "no physical coupling of any kind (VISION sec 1.3)",
            "rho/T ranks unchanged (rho=19, T=3 per C2_cooper_s10_v3.json)",
            "no claim about which lattice T is beyond the stated Tier-B identification",
            "no claim originating from the AlphaEvolve/Vertex report of the same "
            "lattice (Stream-4 exploratory sandbox, DL-3 firewall) — this "
            "certificate's derivation chain does not touch it",
            "this v4 DRAFT is not live; until T0 acceptance the s10 lattice "
            "identification remains uncertified and G0_NS_genus_cooper_s10.json's "
            "input-provenance gap statement stands",
        ],
        "refs_sha256": {
            "recurrences_v1.json": sha256(REFS),
        },
        "provenance": "Generated-by: Fable 5 (T1 coordinator, Stream 2, 2026-08-01) | "
                      "Verified-by: check_U1_lattice.py structural assertions + "
                      "test_U1_controls.py + check_U1_witness_serialization.py --cert "
                      "<this file> | Reviewed-by: pending T0 (Xavier) acceptance",
    }
    out = REPO / "data" / "certificates" / "C2_cooper_s10_v4_DRAFT.json"
    out.write_text(json.dumps(cert, indent=2))
    print(f"\nWrote {out.relative_to(REPO)} (DRAFT, pending T0)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", default="cooper_s7", choices=sorted(FAMILIES))
    ap.add_argument("--controls", action="store_true", help="run all negative controls")
    ap.add_argument("--emit-cert", action="store_true",
                    help="run s7 pipeline + ALL controls, then write the DRAFT v4 certificate")
    ap.add_argument("--emit-cert-v5", action="store_true",
                    help="run s7 pipeline + ALL controls, then write the DRAFT v5 certificate "
                         "(v4 content + serialized basis_change_matrix witness P; v4 untouched)")
    ap.add_argument("--emit-cert-s10", action="store_true",
                    help="run BOTH family pipelines + ALL controls, then write the s10 "
                         "DRAFT v4 lattice certificate (first titled lattice claim for "
                         "cooper_s10, at the s7-v5 witness bar; s7 is the cross-family control)")
    args = ap.parse_args()

    mp.mp.dps = DPS
    try:
        stage0_framework()
        print("[stage0] Dolgachev sec-7 framework re-derived symbolically: OK")
        if args.controls or args.emit_cert or args.emit_cert_v5 or args.emit_cert_s10:
            res_s7 = run_family("cooper_s7")
            print("\n=== controls (mandatory: a run without them is not evidence) ===")
            res_s10 = control_different_level(res_s7)
            control_scrambled()
            control_yukawa_scramble()
            if args.emit_cert:
                emit_cert(res_s7, res_s10)
            if args.emit_cert_v5:
                emit_cert_v5(res_s7, res_s10)
            if args.emit_cert_s10:
                emit_cert_s10_v4(res_s10, res_s7)
        else:
            run_family(args.family)
        print("\ncheck_U1_lattice.py: all structural assertions passed")
        return 0
    except ControlFailure as e:
        print(f"\nFAIL: {e}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
