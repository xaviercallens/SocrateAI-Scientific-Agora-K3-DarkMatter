#!/usr/bin/env python3
"""
check_nodality_explicit_models.py -- singular members of explicit Laurent-polynomial models
of the cooper_s7 / cooper_s10 pencils, computed WITHOUT the lattice and WITHOUT the monodromy,
and compared with the lattice-side statement of data/certificates/CM_POINTS_RHO20.json.

STATUS: record, not a gate.  Tier B.  No physical reading of any kind.  The rho = 20 cut and
T3 are NOT adopted.  cooper_s10 output is ADVISORY (its lattice certificate is DRAFT).
No Kodaira reading is made anywhere (CLAUDE.md ledger item 3): the objects examined are
SURFACES -- the members {P = lambda} of a pencil, z = 1/lambda -- and the word "node" below
always means an isolated A1 singular point of such a surface (nondegenerate Hessian).

WHAT IS COMPUTED (all exact: integers, Fractions, sympy over Q or Q(i); zero tests are
structural or by minimal polynomial -- no numeric recognition, no nsimplify; values are
compared as exact numbers, never as strings)
  leg CT   constant-term identity CT(P^n) = s(n), n <= CT_ORDER, s(n) from the binomial
           closed form, cross-checked against refs/recurrences_v1.json.  PASS(CT_ORDER): a
           finite order.  A P failing it is REFUSED (clause `ct_mismatch`) before any geometry.
  leg T    critical points of P on the torus (C*)^3 with P != 0, via a Groebner basis with a
           Rabinowitsch variable w (w*x*y*z*N = 1).  The ideal must be zero-dimensional
           (clause `critical_locus_not_zero_dimensional` otherwise); then the list is
           COMPLETE for the torus with P != 0.  At each point: critical value, Hessian rank.
           rank 3 = nondegenerate = Morse = the member {P = value} has an A1 point there
           and the total space of the pencil is smooth there.  rank < 3: clause
           `hessian_degenerate` (NOT Morse).
  leg Z    critical points with P = 0 (that is z = infinity): only whether that locus is
           positive-dimensional.  If it is, NOTHING is said about z = infinity.
  leg K    for a model whose numerator has degree <= 2 in each variable and denominator xyz:
           the closure of {P = lambda} in P^1 x P^1 x P^1 is a (2,2,2) surface.  For each
           lambda in a logged list: all singular points (8 charts, partitioned by which
           coordinates are infinite), Hessian rank at each.  The "signature" of a member is
           (number of singular points, sorted Hessian ranks).  lambda is MODEL-SPECIAL when
           its signature differs from the generic one (probes must agree among themselves).
  leg S    OPTIONAL second CAS (Singular, if installed): total Tjurina number of each
           member, number of singular points (cross-check of leg K), Milnor and Tjurina
           numbers at the rational singular points of the special members.  Not installed
           -> clause `singular_leg_not_run`; nothing in legs CT/T/Z/K depends on it.

  leg C    OPTIONAL, second CAS: primary decomposition of the relative singular scheme over
           Q[lambda]; the vertical associated primes give EXACTLY the members whose total
           Tjurina number differs from the generic one (clause
           `complete_special_set_differs_from_scan` if that set is not leg K's special set).

LIMITS (repeated in the certificate under `not_claimed`)
  * {P = lambda} is ONE birational model.  Neither model here is the M_n-polarized model of
    Dolgachev 1996: the (2,2,2) closure is polarized by a single class.  "A1 point on this
    model" is what is observed; nothing is proved about the minimal resolution.
  * Torus critical points do not see the toric boundary; leg K sees the boundary of ONE
    compactification only.
  * A change of signature is NOT evidence of a singular point of the operator: control R4
    is a real member (s7, model b, lambda = 2) where the signature changes and L3 is regular.
  * z = infinity (lambda = 0) is not examined: the member P = 0 has non-isolated singularities.

Usage:  python3 checkers/check_nodality_explicit_models.py [--emit] [--quick] | --brief
Exit 0 iff the integrity gates hold (see `gates` in the certificate).  The hand estimate is
SCORED, never gated: a refuted clause is a finding.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parent.parent
CERTS = REPO / "data" / "certificates"
REFS = REPO / "refs" / "recurrences_v1.json"
CM_CERT = CERTS / "CM_POINTS_RHO20.json"
LOCI_CERT = {"cooper_s7": "C1_L3_cooper_s7.json", "cooper_s10": "C1_L3_cooper_s10.json"}
OUT = CERTS / "NODALITY_EXPLICIT_MODELS.json"

CT_ORDER = 10
PROBES = [3, 5, -7, 11]            # members used to define the generic signature
INT_SCAN = range(-12, 41)          # logged integer window of lambda for leg K

x, y, z, w = sp.symbols("x y z w")
VARS = (x, y, z)

# --------------------------------------------------------------------------------------
# sequences (closed forms; cross-checked against refs)
# --------------------------------------------------------------------------------------
CLOSED_FORM = {
    "cooper_s7": lambda n: sum(comb(n, j) ** 2 * comb(2 * j, n) * comb(j + n, j)
                               for j in range(n + 1)),
    "cooper_s10": lambda n: sum(comb(n, k) ** 4 for k in range(n + 1)),
}


def sequence(key, nmax):
    return [CLOSED_FORM[key](n) for n in range(nmax + 1)]


def refs_crosscheck(key, ref=None):
    """Closed form against the terms held in refs (n <= refs_terms - 1 only; the CT leg goes
    to CT_ORDER on the closed form).  `ref` may be supplied by a control (S9)."""
    if ref is None:
        ref = json.loads(REFS.read_text())["sequences"][key]["initial_terms"]
    mine = sequence(key, len(ref) - 1)
    bad = [n for n, (a, b) in enumerate(zip(ref, mine)) if int(a) != b]
    return {"refs_terms": len(ref), "covers_n_up_to": len(ref) - 1, "agree": not bad,
            "clause": "refs_mismatch" if bad else None,
            "first_mismatch_index": bad[0] if bad else None}


# --------------------------------------------------------------------------------------
# models.  P = N / D, D a monomial.  Provenance of each P is stated; none is trusted
# before leg CT passes.
# --------------------------------------------------------------------------------------
MODELS = {
    "s10_a": {
        "family": "cooper_s10",
        "N": (1 + x) * (1 + y) * (1 + z) * (1 + x * y * z), "D": x * y * z,
        "provenance": "derived here: C(n,k)^4 = [x^k y^k z^k (xyz)^-k] of "
                      "((1+x)(1+y)(1+z)(1+1/(xyz)))^n",
    },
    "s7_a": {
        "family": "cooper_s7",
        "N": sp.expand((x + y + z + 1) ** 2 * y * z
                       + (x + y + z + 1) * (y + z + 1) * (z + 1) ** 2), "D": x * y * z,
        "provenance": "written from recollection of the literature on Landau-Ginzburg "
                      "models of the Fano threefold of degree 14 (NOT fetched, NOT pinned in "
                      "docs/literature/MANIFEST.md); admitted ONLY because leg CT passes",
    },
    "s7_b": {
        "family": "cooper_s7",
        "N": (1 + x * (1 + y) * (1 + z) ** 2) * (1 + x) * (1 + y), "D": x * y * z,
        "provenance": "derived here from the closed form: C(n,j)^2 from "
                      "(1 + x(1+y)(1+z)^2)^n (1+1/x)^n at x^j x^-j, then "
                      "[y^n](1+y)^(n+j) = C(n+j,n), [z^n](1+z)^(2j) = C(2j,n)",
    },
}

# REAL known-bads for leg CT (kept in the certificate; both are honest candidates that fail)
KNOWN_BAD_MODELS = {
    "s7_missing_square": {
        "family": "cooper_s7",
        "N": (1 + x * (1 + y) * (1 + z)) * (1 + x) * (1 + y), "D": x * y * z,
        "provenance": "the s7_b derivation with the square on (1+z) forgotten: gives "
                      "sum C(n,j)^2 C(n+j,n) C(j,n), a different sequence",
    },
    "s7_a_misremembered": {
        "family": "cooper_s7",
        "N": sp.expand((x + y + z + 1) ** 2 * y * z
                       + (x + y + z + 1) * (y + z + 1) * (z + 1)), "D": x * y * z,
        "provenance": "s7_a with the square on (z+1) dropped: the kind of slip a formula "
                      "written from recollection invites; this is why s7_a is admitted on "
                      "leg CT alone",
    },
    "franel_polynomial_for_s10": {
        "family": "cooper_s10",
        "N": (1 + x) * (1 + y) * (1 + x * y) * z, "D": x * y * z,
        "provenance": "exponent confusion: ((1+x)(1+y)(1+1/(xy)))^n has constant term "
                      "sum C(n,k)^3, not sum C(n,k)^4; the two sequences share n = 0 and n = 1, "
                      "so a CT check of order 1 would ACCEPT this P",
    },
    "s10_polynomial_for_s7": {
        "family": "cooper_s7",
        "N": MODELS["s10_a"]["N"], "D": x * y * z,
        "provenance": "cross-family: the s10 polynomial offered for the s7 sequence",
    },
}


# --------------------------------------------------------------------------------------
# leg CT
# --------------------------------------------------------------------------------------
def _poly_dict(expr):
    return {m: int(c) for m, c in sp.Poly(sp.expand(expr), *VARS).terms()}


def _mul(a, b):
    out = {}
    for (i1, j1, k1), c1 in a.items():
        for (i2, j2, k2), c2 in b.items():
            key = (i1 + i2, j1 + j2, k1 + k2)
            out[key] = out.get(key, 0) + c1 * c2
    return out


def constant_terms(N, D, nmax):
    """CT((N/D)^n), n = 0..nmax, integer arithmetic."""
    nd = _poly_dict(N)
    (dm, dc), = _poly_dict(D).items()
    if dc != 1:
        raise ValueError("denominator must be a monic monomial")
    out, power = [], {(0, 0, 0): 1}
    for n in range(nmax + 1):
        out.append(power.get(tuple(n * e for e in dm), 0))
        if n < nmax:
            power = _mul(power, nd)
    return out


def check_ct(model, order=CT_ORDER):
    got = constant_terms(model["N"], model["D"], order)
    want = sequence(model["family"], order)
    bad = [n for n in range(order + 1) if got[n] != want[n]]
    res = {"order_checked": order, "constant_terms": got, "sequence": want}
    if bad:
        res.update(verdict="REFUSED", clause="ct_mismatch", first_mismatch_index=bad[0])
    else:
        res.update(verdict=f"PASS({order})", clause=None)
    return res


# --------------------------------------------------------------------------------------
# leg T / leg Z
# --------------------------------------------------------------------------------------
def _crit_equations(N, D):
    return [sp.expand(sp.diff(N, v) * D - N * sp.diff(D, v)) for v in VARS]


def _zero_dimensional(G, gens):
    """Standard criterion: for every variable some leading monomial is a pure power of it."""
    lms = [sp.Poly(g, *gens).monoms(order=G.order)[0] for g in G.exprs]
    return all(any(m[i] > 0 and sum(m) == m[i] for m in lms) for i in range(len(gens)))


def _simp(e):
    """Exact normal form of an algebraic number.  NO numeric recognition: sp.nsimplify is
    deliberately not used (it maps 27 + 10^-20 to 27; control S8)."""
    return sp.radsimp(sp.simplify(sp.sympify(e)))


def _is_zero(e):
    """Exact zero test: structural after simplification, else by minimal polynomial over Q.
    An expression that is not an algebraic number raises (nothing is decided numerically)."""
    e = _simp(e)
    if e == 0:
        return True
    if e.is_Rational:
        return False
    t = sp.Dummy("t")
    return sp.minimal_polynomial(e, t, polys=True) == sp.Poly(t, t)


def _num(s):
    """Exact sympy number from a certificate string ('1/27', '-I', ...); floats refused."""
    v = sp.sympify(s)
    if v.atoms(sp.Float):
        raise ValueError(f"float in an exact comparison: {s!r}")
    return v


def same_number(a, b):
    return _is_zero(_num(a) - _num(b))


def lookup_number(d, val):
    """Entry of dict d whose KEY is the same exact number as val (keys such as 'infinity'
    are skipped).  None when absent."""
    for k, v in d.items():
        if k != "infinity" and same_number(k, val):
            return v
    return None


def _rank(M):
    return M.applyfunc(lambda e: sp.simplify(e)).rank(simplify=True)


def torus_critical_points(N, D):
    """Complete list of critical points of P = N/D on the torus with P != 0."""
    gens = (w,) + VARS
    eqs = _crit_equations(N, D) + [sp.expand(w * D * N - 1)]
    G = sp.groebner(eqs, *gens, order="grevlex")
    if list(G.exprs) == [1]:
        return {"verdict": "OK", "clause": None, "points": []}
    if not _zero_dimensional(G, gens):
        return {"verdict": "REFUSED", "clause": "critical_locus_not_zero_dimensional",
                "points": None}
    Glex = sp.groebner(list(G.exprs), *gens, order="lex")
    sols = sp.solve_poly_system(list(Glex.exprs), *gens)
    P = N / D
    H = sp.hessian(P, VARS)
    pts = []
    for s in sols:
        s = tuple(_simp(t) for t in s)
        sub = dict(zip(gens, s))
        if not all(_is_zero(e.subs(sub)) for e in eqs):
            return {"verdict": "REFUSED", "clause": "solution_does_not_satisfy_equations",
                    "points": None}
        val = _simp(P.subs(sub))
        rk = _rank(H.subs(sub))
        pts.append({"point": [str(t) for t in s[1:]], "critical_value": str(val),
                    "z": str(_simp(1 / val)), "hessian_rank": int(rk),
                    "hessian_det": str(_simp(H.subs(sub).det())),
                    "morse": rk == 3,
                    "clause": None if rk == 3 else "hessian_degenerate",
                    "rational": all(t.is_rational for t in s[1:])})
    pts.sort(key=lambda p: (p["critical_value"], p["point"]))
    return {"verdict": "OK", "clause": None, "points": pts}


def value_zero_locus(N, D):
    """Is the set of torus critical points with P = 0 positive-dimensional?"""
    gens = (w,) + VARS
    eqs = _crit_equations(N, D) + [sp.expand(N), sp.expand(w * D - 1)]
    G = sp.groebner(eqs, *gens, order="grevlex")
    if list(G.exprs) == [1]:
        return {"empty": True, "positive_dimensional": False}
    return {"empty": False, "positive_dimensional": not _zero_dimensional(G, gens)}


def compare_with_loci(points, loci):
    """loci: list of strings (finite singular points z of the operator, from the C1 cert).
    Values are compared as exact numbers (same_number), never as strings."""
    zs = Counter(p["z"] for p in points)
    extra = sorted(zv for zv in zs if not any(same_number(zv, l) for l in loci))
    missing = sorted(l for l in loci if not any(same_number(zv, l) for zv in zs))
    clauses = []
    if extra:
        clauses.append("critical_value_not_a_certified_locus")
    if missing:
        clauses.append("certified_locus_without_torus_critical_point")
    return {"critical_points_per_z": dict(zs), "extra": extra, "missing": missing,
            "clauses": clauses}


# --------------------------------------------------------------------------------------
# leg K: closure in P^1 x P^1 x P^1
# --------------------------------------------------------------------------------------
def is_222(N, D):
    p = sp.Poly(sp.expand(N), *VARS)
    return sp.expand(D - x * y * z) == 0 and all(p.degree(v) <= 2 for v in VARS)


def chart_equation(N, lam, c):
    F = sp.expand(N - lam * x * y * z)
    for i, v in enumerate(VARS):
        if (c >> i) & 1:
            F = sp.expand(sp.cancel(F.subs(v, 1 / v) * v ** 2))
    return F


def singular_points_222(N, lam):
    """All singular points of the closure of {N = lam xyz}; chart c lists the points whose
    coordinates i with bit i of c set are infinite (so the 8 lists partition the surface)."""
    out = []
    for c in range(8):
        F = chart_equation(N, lam, c)
        eqs = [F] + [sp.diff(F, v) for v in VARS] + [v for i, v in enumerate(VARS) if (c >> i) & 1]
        G = sp.groebner(eqs, *VARS, order="grevlex")
        if list(G.exprs) == [1]:
            continue
        if not _zero_dimensional(G, VARS):
            return {"verdict": "REFUSED", "clause": "singular_locus_not_isolated", "points": None}
        Glex = sp.groebner(list(G.exprs), *VARS, order="lex")
        H = sp.hessian(F, VARS)
        for s in sp.solve_poly_system(list(Glex.exprs), *VARS):
            s = tuple(_simp(t) for t in s)
            sub = dict(zip(VARS, s))
            if not all(_is_zero(e.subs(sub)) for e in eqs):
                return {"verdict": "REFUSED", "clause": "solution_does_not_satisfy_equations",
                        "points": None}
            on_torus = c == 0 and not any(_is_zero(t) for t in s)
            out.append({"chart": c, "point_in_chart": [str(t) for t in s],
                        "hessian_rank": int(_rank(H.subs(sub))), "on_torus": on_torus,
                        "rational": all(t.is_rational for t in s)})
    return {"verdict": "OK", "clause": None, "points": out}


def signature(points):
    return [len(points), sorted(p["hessian_rank"] for p in points)]


def scan_222(N, lams, loci):
    members, refused = {}, {}
    for lam in lams:
        r = singular_points_222(N, lam)
        if r["verdict"] != "OK":
            refused[str(lam)] = r["clause"]
            continue
        members[str(lam)] = r["points"]
    probe_sigs = {str(l): signature(members[str(l)]) for l in PROBES if str(l) in members}
    distinct = {json.dumps(s) for s in probe_sigs.values()}
    if len(distinct) != 1 or len(probe_sigs) != len(PROBES):
        return {"verdict": "REFUSED", "clause": "probes_disagree_on_generic_signature",
                "probe_signatures": probe_sigs}
    generic = json.loads(distinct.pop())
    special = {}
    for k, pts in members.items():
        sig = signature(pts)
        if sig == generic:
            continue
        zstr = str(1 / sp.Rational(k))
        is_locus = any(same_number(zstr, l) for l in loci)
        kinds = []
        torus = [p for p in pts if p["on_torus"]]
        if torus:
            kinds.append("new_torus_singular_point" + ("s" if len(torus) > 1 else ""))
        nb = len(pts) - len(torus)
        if nb < generic[0]:
            kinds.append("boundary_points_merge")
        if Counter(p["hessian_rank"] for p in pts if not p["on_torus"]) != Counter(generic[1]) \
                and nb == generic[0]:
            kinds.append("boundary_point_hessian_rank_drops")
        special[k] = {"z": zstr, "signature": sig, "kinds": kinds,
                      "z_is_certified_locus": is_locus,
                      "clause": None if is_locus else "model_special_but_operator_regular",
                      "points": pts}
    return {"verdict": "OK", "clause": None, "generic_signature": generic,
            "generic_member_points_at_probe": members[str(PROBES[0])],
            "probe_signatures": probe_sigs, "lambdas_scanned": [str(l) for l in lams],
            "refused_lambdas": refused, "special": special}


# --------------------------------------------------------------------------------------
# leg S: Singular (optional)
# --------------------------------------------------------------------------------------
_SING_PRE = r'''
LIB "primdec.lib"; LIB "sing.lib";
proc inv2(poly F, poly v) { matrix C=coef(F,v); poly G=0; int i;
  for(i=1;i<=ncols(C);i++){ G=G+C[2,i]*v^(2-deg(C[1,i])); } return(G); }
proc inreg(ideal R, int c){ int ok=1; ideal S=std(R);
 if((c mod 2)==1){ if(reduce(x,S)!=0){ok=0;} }
 if(((c div 2) mod 2)==1){ if(reduce(y,S)!=0){ok=0;} }
 if(((c div 4) mod 2)==1){ if(reduce(z,S)!=0){ok=0;} }
 return(ok);}
'''


def _sing_str(e):
    """Integer-coefficient string for Singular (a nonzero constant factor changes neither
    the singular points nor Milnor / Tjurina numbers; 'z^2/16' would be misparsed)."""
    _, q = sp.Poly(sp.expand(e), *VARS).clear_denoms(convert=True)
    return str(q.as_expr()).replace("**", "^")


def _sing_str_in(e, gens):
    _, q = sp.Poly(sp.expand(e), *gens).clear_denoms(convert=True)
    return str(q.as_expr()).replace("**", "^")


def singular_leg(N, lams, local_points):
    """local_points: list of (lam, chart, (px,py,pz)) rational points for Milnor/Tjurina."""
    exe = shutil.which("Singular")
    if not exe:
        return {"verdict": "NOT_RUN", "clause": "singular_leg_not_run"}
    s = ["ring r=0,(x,y,z),dp;", _SING_PRE]
    for lam in lams:
        s.append(f'"LAMBDA {lam}"; poly F0={_sing_str(N - lam * x * y * z)}; int tot=0; int np=0;')
        for c in range(8):
            s.append("poly F=F0;")
            s += [f"F=inv2(F,{v});" for i, v in enumerate("xyz") if (c >> i) & 1]
            s.append('ideal I=std(ideal(F,diff(F,x),diff(F,y),diff(F,z)));'
                     'if(dim(I)>0){"NONISOLATED";} else { if(vdim(I)>0){ list L=primdecGTZ(I);'
                     f'int i; for(i=1;i<=size(L);i++){{ if(inreg(L[i][2],{c}))'
                     '{ tot=tot+vdim(std(L[i][1])); np=np+vdim(std(L[i][2])); } } kill L; kill i; } }'
                     'kill F; kill I;')
        s.append('"TOTAL",tot,np; kill tot; kill np; kill F0;')
    s.append("ring rl=0,(x,y,z),ds;")
    for n, (lam, c, pt) in enumerate(local_points):
        F = chart_equation(N, sp.Rational(lam), c).subs(
            {v: v + sp.Rational(p) for v, p in zip(VARS, pt)}, simultaneous=True)
        s.append(f'poly G{n}={_sing_str(F)}; "LOCAL {n}",milnor(G{n}),tjurina(G{n});')
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write("\n".join(s) + "\nquit;\n")
    run = subprocess.run([exe, "-q", fh.name], capture_output=True, text=True, timeout=1800)
    lines = [l for l in run.stdout.splitlines() if "redefining" not in l]
    if any("NONISOLATED" in l for l in lines):
        return {"verdict": "REFUSED", "clause": "singular_locus_not_isolated"}
    totals, local, cur = {}, {}, None
    for l in lines:
        t = l.split()
        if t[:1] == ["LAMBDA"]:
            cur = t[1]
        elif t[:1] == ["TOTAL"]:
            totals[cur] = {"total_tjurina": int(t[1]), "singular_points": int(t[2])}
        elif t[:1] == ["LOCAL"]:
            local[int(t[1])] = {"milnor": int(t[2]), "tjurina": int(t[3])}
    if len(totals) != len(lams) or len(local) != len(local_points):
        return {"verdict": "REFUSED", "clause": "singular_output_unparsed",
                "stderr": run.stderr[-500:]}
    ver = subprocess.run([exe, "-v", "-q", "--execute=quit;"], capture_output=True, text=True)
    return {"verdict": "OK", "clause": None, "totals": totals,
            "singular_version": (ver.stdout.strip().splitlines() or ["?"])[0],
            "local": [dict(lam=str(lp[0]), chart=lp[1], point_in_chart=[str(p) for p in lp[2]],
                           **local[n]) for n, lp in enumerate(local_points)]}


def completeness_leg(N, shift=0):
    """leg C (second CAS only): the relative singular scheme of the (2,2,2) closure over the
    lambda-line, F = N - (l - shift) xyz, in each of the 8 affine charts of (P^1)^3.
    primdecGTZ lists ALL associated primes (embedded ones included); those whose elimination
    ideal in Q[l] is nonzero are the vertical ones.  Away from the members with non-isolated
    singular points the scheme is finite over Q[l], a finite module over a PID is free plus
    torsion, and the torsion is supported exactly on the vertical associated primes; so the
    members whose TOTAL TJURINA NUMBER differs from the generic one are exactly the roots of
    the eliminants (standard commutative algebra, used as an argument, not machine-checked).
    Also: number of singular points and total Tjurina number of the generic member over Q(l).
    `shift` exists for control R10 (special members moved outside the scanned window)."""
    exe = shutil.which("Singular")
    if not exe:
        return {"verdict": "NOT_RUN", "clause": "singular_leg_not_run"}
    l = sp.Symbol("l")
    F0 = _sing_str_in(N - (l - shift) * x * y * z, VARS + (l,))
    s = ['LIB "primdec.lib";', "ring r=0,(x,y,z,l),dp;",
         "proc inv2(poly F, poly v) { matrix C=coef(F,v); poly G=0; int i;"
         " for(i=1;i<=ncols(C);i++){ G=G+C[2,i]*v^(2-deg(C[1,i])); } return(G); }",
         f"poly F0={F0}; int c; int i;",
         "for(c=0;c<8;c++){ poly F=F0;"
         " if((c mod 2)==1){F=inv2(F,x);} if(((c div 2) mod 2)==1){F=inv2(F,y);}"
         " if(((c div 4) mod 2)==1){F=inv2(F,z);}"
         " ideal I=F,diff(F,x),diff(F,y),diff(F,z); list L=primdecGTZ(I);"
         " for(i=1;i<=size(L);i++){ ideal E=eliminate(L[i][2],x*y*z);"
         ' if(size(E)>0){ "VERT",c,dim(std(L[i][2])),":",E[1]; } kill E; }'
         " kill F; kill I; kill L; }",
         "ring rg=(0,l),(x,y,z),dp;", _SING_PRE.split("\n", 2)[2],
         f"poly F0={F0}; int tot=0; int np=0; int c; int i;"]
    for c in range(8):
        s.append("poly F=F0;")
        s += [f"F=inv2(F,{v});" for i, v in enumerate("xyz") if (c >> i) & 1]
        s.append('ideal I=std(ideal(F,diff(F,x),diff(F,y),diff(F,z)));'
                 'if(dim(I)>0){"NONISOLATED";} else { if(vdim(I)>0){ list L=primdecGTZ(I);'
                 f'for(i=1;i<=size(L);i++){{ if(inreg(L[i][2],{c}))'
                 '{ tot=tot+vdim(std(L[i][1])); np=np+vdim(std(L[i][2])); } } kill L; } }'
                 'kill F; kill I;')
    s.append('"GENERIC",tot,np;')
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write("\n".join(s) + "\nquit;\n")
    run = subprocess.run([exe, "-q", fh.name], capture_output=True, text=True, timeout=1800)
    vertical, generic = {}, None
    for ln in run.stdout.splitlines():
        t = ln.split()
        if t[:1] == ["VERT"]:
            poly = sp.Poly(sp.sympify(ln.split(":", 1)[1].replace("^", "**")), l)
            for fac, _ in poly.factor_list()[1]:
                key = (str(-fac.nth(0) / fac.nth(1)) if fac.degree() == 1
                       else "roots of " + str(fac.as_expr()))
                vertical[key] = max(vertical.get(key, 0), int(t[2]))
        elif t[:1] == ["GENERIC"]:
            generic = {"total_tjurina": int(t[1]), "singular_points": int(t[2])}
    if generic is None or "NONISOLATED" in run.stdout or not vertical:
        return {"verdict": "REFUSED", "clause": "singular_output_unparsed",
                "stderr": run.stderr[-500:]}
    return {"verdict": "OK", "clause": None, "shift": str(shift),
            "generic_over_Q_of_lambda": generic,
            "lambda_with_non_isolated_singular_points": sorted(
                (k for k, d in vertical.items() if d > 0), key=_lam_key),
            "lambda_where_total_tjurina_differs_from_generic": sorted(
                (k for k, d in vertical.items() if d == 0), key=_lam_key),
            "statement": "exactly these members (lambda outside the non-isolated list) have a total "
                         "Tjurina number different from the generic one on this closure"}


def _lam_key(k):
    return (1, 0, k) if k.startswith("roots") else (0, sp.Rational(k), k)


def compare_complete_with_scan(closure, sleg, cleg):
    """Clause `complete_special_set_differs_from_scan` unless leg C's set equals leg K's special
    set, its generic counts equal leg K / leg S, and every special member was in the scanned list."""
    if cleg.get("verdict") != "OK":
        return {"agree": None, "clause": cleg.get("clause")}
    comp = cleg["lambda_where_total_tjurina_differs_from_generic"]
    rational = [k for k in comp if not k.startswith("roots")]
    scan = list(closure["special"])
    only_c = [k for k in comp if k not in rational or not any(same_number(k, q) for q in scan)]
    only_k = [q for q in scan if not any(same_number(k, q) for k in rational)]
    g = cleg["generic_over_Q_of_lambda"]
    counts_ok = (g["singular_points"] == closure["generic_signature"][0]
                 and (sleg.get("verdict") != "OK" or g["total_tjurina"] == sleg["generic_total_tjurina"]))
    ok = not only_c and not only_k and counts_ok
    return {"agree": ok, "clause": None if ok else "complete_special_set_differs_from_scan",
            "in_complete_set_not_in_scan_special": only_c,
            "in_scan_special_not_in_complete_set": only_k, "generic_counts_agree": counts_ok}


def arnold_label(corank, mu):
    """(corank of the Hessian, Milnor number) -> name in Arnold's list of simple
    singularities (standard classification, cited not proved; only the cases met)."""
    if corank == 0 and mu == 1:
        return "A1"
    if corank == 1 and mu >= 2:
        return f"A{mu}"
    if corank == 2 and mu in (4, 5):
        return f"D{mu}"
    return "unlabelled"


# --------------------------------------------------------------------------------------
# lattice arithmetic behind the remark of the brief (exact; an INTERPRETATION aid only)
# --------------------------------------------------------------------------------------
def root_system_remark():
    D4 = sp.Matrix([[-2, 1, 1, 1], [1, -2, 0, 0], [1, 0, -2, 0], [1, 0, 0, -2]])  # C0;C1,C2,C3
    A2 = sp.Matrix([[-2, 1], [1, -2]])

    def roots(G, box=2):
        n = G.shape[0]
        import itertools
        return [sp.Matrix(v) for v in itertools.product(range(-box, box + 1), repeat=n)
                if (sp.Matrix([v]) * G * sp.Matrix(v))[0] == -2]

    e = [sp.Matrix([1, 1, 0, 0]), sp.Matrix([1, 0, 1, 0]), sp.Matrix([1, 0, 0, 1])]
    pair = lambda G, a, b: int((a.T * G * b)[0])
    d4_roots = roots(D4)
    orth = [r for r in d4_roots if all(pair(D4, r, ei) == 0 for ei in e)]
    sub = sp.Matrix.hstack(*e, orth[0]) if orth else None
    a2_roots = roots(A2)
    a2_orth = [r for r in a2_roots if pair(A2, r, sp.Matrix([1, 0])) == 0]
    two = e[0] + e[1]                       # two orthogonal roots (Gram entry checked below)
    return {
        "D4_number_of_roots": len(d4_roots),
        "three_orthogonal_roots_e_i": [[int(t) for t in v] for v in e],
        "e_i_gram": [[pair(D4, a, b) for b in e] for a in e],
        "roots_of_D4_orthogonal_to_all_e_i": [[int(t) for t in r] for r in orth],
        "index_of_A1^3_plus_that_root_in_D4": (abs(int(sub.det())) if orth else None),
        "A2_number_of_roots": len(a2_roots),
        "roots_of_A2_orthogonal_to_a_root": [[int(t) for t in r] for r in a2_orth],
        "two_orthogonal_roots_used": [[int(t) for t in e[0]], [int(t) for t in e[1]]],
        "their_pairing": pair(D4, e[0], e[1]),
        "sum_of_two_orthogonal_roots_has_norm": pair(D4, two, two),
    }


# --------------------------------------------------------------------------------------
# inputs
# --------------------------------------------------------------------------------------
def count_controls():
    t = (Path(__file__).resolve().parent / "test_nodality_explicit_models_controls.py").read_text()
    return sum(1 for ln in t.splitlines() if ln.startswith("def test_"))


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_loci(family):
    return json.loads((CERTS / LOCI_CERT[family]).read_text())["finite_singular_loci"]


def load_lattice_side(family):
    fam = json.loads(CM_CERT.read_text())["families"][family]
    hits = {}
    for r in fam["rows"]:
        zv = r.get("z_value_if_rational")
        if zv and zv not in hits:
            hits[zv] = {"minus_v2": r["minus_v2"], "div_v": r["div_v"],
                        "reflective": r["v_is_reflective"], "D": r["D"], "v": r["v"]}
    return {"advisory": fam["advisory"], "flags": fam["flags"], "rational_z": hits,
            "lattice_cert": fam["lattice_cert"], "lattice_cert_status": fam["lattice_cert_status"]}


def lambda_list(family, quick=False):
    lat = load_lattice_side(family)
    lams = set(sp.Integer(p) for p in PROBES)
    for zv in lat["rational_z"]:
        if zv != "infinity":
            lams.add(1 / sp.Rational(zv))
    if not quick:
        lams |= {sp.Integer(k) for k in INT_SCAN if k != 0}
    return sorted(lams)


# --------------------------------------------------------------------------------------
# scoring of the orchestrator's hand estimate (UNVERIFIED when issued)
# --------------------------------------------------------------------------------------
def tjurina_change(res, lam):
    """(generic, member, change) of the total Tjurina number on the (2,2,2) closure, from the
    optional second CAS; None when that leg did not run for this model."""
    s = res.get("singular_leg") or {}
    if s.get("verdict") != "OK":
        return None
    member = lookup_number(s["members_with_other_total_tjurina"], lam)
    member = s["generic_total_tjurina"] if member is None else member
    return {"generic": s["generic_total_tjurina"], "member": member,
            "change": member - s["generic_total_tjurina"]}


def score(results, lattice):
    out = []

    def add(clause, outcome, basis, advisory=False):
        out.append({"clause": clause, "outcome": outcome, "basis": basis, "advisory": advisory})

    for fam, models in (("cooper_s7", ["s7_a", "s7_b"]), ("cooper_s10", ["s10_a"])):
        adv = lattice[fam]["advisory"]
        loci = results[models[0]]["loci"]
        # (a) torus critical values = certified loci
        for m in models:
            cmpr = results[m]["compare"]
            add(f"{m}: set of torus critical values (as z) equals the certified finite loci {loci}",
                "confirmed" if not cmpr["clauses"] else "REFUTED",
                f"extra={cmpr['extra']} missing={cmpr['missing']}", adv)
        for zv in loci:
            lat = lookup_number(lattice[fam]["rational_z"], zv)
            predicted = bool(lat and lat["minus_v2"] == 2)
            for m in models:
                pts = [p for p in results[m]["torus"]["points"] if same_number(p["z"], zv)]
                one_morse = len(pts) == 1 and pts[0]["morse"]
                k = results[m].get("closure")
                kinfo = (lookup_number(k["special"], 1 / sp.Rational(zv))
                         if k and k["verdict"] == "OK" else None)
                tau = tjurina_change(results[m], 1 / sp.Rational(zv))
                basis = (f"torus critical points over z: {len(pts)}, Morse: "
                         f"{[p['morse'] for p in pts]}"
                         + (f"; closure signature {kinfo['signature']} vs generic "
                            f"{k['generic_signature']}, kinds {kinfo['kinds']}" if kinfo else ""))
                if predicted:
                    closure_ok = k is not None and k["verdict"] == "OK"
                    if closure_ok:
                        g = k["generic_signature"]
                        one_new_a1 = bool(kinfo) and kinfo["signature"] == [g[0] + 1, sorted(g[1] + [3])]
                        outcome = ("confirmed ON THIS MODEL (torus and (2,2,2) closure); model-level, "
                                   "nothing about the M_n-polarized model"
                                   if one_morse and one_new_a1 else
                                   "literal clause FAILS ON THIS MODEL (no single new A1 point); "
                                   "NOT a refutation of the lattice side: "
                                   + (f"total Tjurina number {tau['generic']} -> {tau['member']} "
                                      f"(change {tau['change']:+d})" if tau else
                                      "total Tjurina number not available (second CAS not run)")
                                   + "; M_n-polarized model open")
                        if tau:
                            basis += (f"; total Tjurina number generic {tau['generic']}, this member "
                                      f"{tau['member']} (change {tau['change']:+d})")
                    else:
                        outcome = ("confirmed on the torus (boundary of this model not examined)"
                                   if one_morse else
                                   "NOT OBSERVED on the torus (boundary of this model not examined)")
                    add(f"{m}: z = {zv} comes from a (-2)-vector (div {lat['div_v']}), so exactly "
                        f"one A1 point appears on the model", outcome, basis, adv)
                else:
                    add(f"{m}: z = {zv} (-v^2 = {lat['minus_v2'] if lat else '?'}, div "
                        f"{lat['div_v'] if lat else '?'}): no prediction was made",
                        "observed", basis, adv)
        add(f"{fam}: behaviour at z = infinity", "NOT EXAMINED",
            "value-0 critical locus positive-dimensional in every model: "
            + str({m: results[m]["value_zero"]["positive_dimensional"] for m in models}), adv)
    return out


# --------------------------------------------------------------------------------------
NOT_CLAIMED = [
    "anything about the minimal resolution of any member: an A1 point is observed on a "
    "birational model; nothing is proved about the smooth K3 surface",
    "that either model is the M_n-polarized model of Dolgachev 1996: the (2,2,2) closure "
    "carries one polarization class, and its singular points are not the (-2)-walls of M_n",
    "anything at the toric boundary of models that are not (2,2,2) (s7_a): not examined",
    "anything at z = infinity: the member P = 0 has non-isolated singular points in every "
    "model here; the order-3 statement of the lattice side is neither supported nor contradicted",
    "that a change of signature detects a singular point of the operator: s7_b at lambda = 2 "
    "is a real counterexample (control R4)",
    "completeness of leg K by itself: leg K examines a logged finite list of members.  Leg C "
    "(second CAS only) states which members have a total Tjurina number different from the "
    "generic one, by an argument that is standard but not machine-checked; a change of "
    "signature at constant total Tjurina number is not excluded by leg C",
    "the names A_k, D_4 beyond (Hessian corank, Milnor number) matched against Arnold's list "
    "(standard, cited not proved); Milnor and Tjurina numbers come from the optional Singular leg",
    "the reading of the s7 z = -1 and s10 z = -1/4 observations through root systems "
    "(brief section 5): the integer arithmetic is exact, the identification of those roots "
    "with classes on the surface is a hypothesis and is not checked here",
    "anything certified about cooper_s10: its lattice certificate is DRAFT; all s10 output is ADVISORY",
    "any Kodaira reading at any locus (CLAUDE.md ledger item 3): only singular points of "
    "surfaces are discussed",
    "that rho = 20 or T3 is a criterion of the program: neither is adopted; nothing is scored or ranked",
    "any physical reading whatsoever (VISION sec 1.3; Tier C blocked, F5b)",
]


def analyse_model(name, model, loci, quick=False, with_singular=True):
    res = {"family": model["family"], "provenance": model["provenance"],
           "N": str(sp.expand(model["N"])), "D": str(model["D"]), "loci": loci}
    res["ct"] = check_ct(model)
    if res["ct"]["clause"]:
        res["verdict"] = "REFUSED"
        res["clause"] = res["ct"]["clause"]
        return res
    res["torus"] = torus_critical_points(model["N"], model["D"])
    if res["torus"]["clause"]:
        res["verdict"], res["clause"] = "REFUSED", res["torus"]["clause"]
        return res
    res["compare"] = compare_with_loci(res["torus"]["points"], loci)
    res["value_zero"] = value_zero_locus(model["N"], model["D"])
    if is_222(model["N"], model["D"]):
        lams = lambda_list(model["family"], quick)
        res["closure"] = scan_222(model["N"], lams, loci)
        if res["closure"]["verdict"] == "OK" and with_singular:
            sp_l = list(res["closure"]["special"])
            local = [(l, p["chart"], tuple(p["point_in_chart"]))
                     for l in sp_l + [str(PROBES[0])]
                     for p in (res["closure"]["special"][l]["points"] if l in sp_l
                               else res["closure"]["generic_member_points_at_probe"])
                     if p["rational"]]
            sl = singular_leg(model["N"], [sp.Rational(l) for l in res["closure"]["lambdas_scanned"]],
                              local)
            if sl["verdict"] == "OK":
                gen = res["closure"]["generic_signature"][0]
                mism = [l for l, t in sl["totals"].items()
                        if t["singular_points"] != (len(res["closure"]["special"][l]["points"])
                                                    if l in res["closure"]["special"] else gen)]
                sl["point_count_disagreements_with_sympy"] = mism
                taus = Counter(t["total_tjurina"] for t in sl["totals"].values())
                sl["generic_total_tjurina"] = taus.most_common(1)[0][0]
                sl["members_with_other_total_tjurina"] = {
                    l: t["total_tjurina"] for l, t in sl["totals"].items()
                    if t["total_tjurina"] != sl["generic_total_tjurina"]}
                for lp in sl["local"]:
                    pts = (res["closure"]["special"][lp["lam"]]["points"]
                           if lp["lam"] in res["closure"]["special"]
                           else res["closure"]["generic_member_points_at_probe"])
                    rk = [p["hessian_rank"] for p in pts if p["chart"] == lp["chart"]
                          and p["point_in_chart"] == lp["point_in_chart"]][0]
                    lp["hessian_corank_sympy"] = 3 - rk
                    lp["label"] = arnold_label(3 - rk, lp["milnor"])
                sl.pop("totals")
            res["singular_leg"] = sl
            res["completeness_leg"] = completeness_leg(model["N"])
            res["completeness_vs_scan"] = compare_complete_with_scan(
                res["closure"], sl, res["completeness_leg"])
    else:
        res["closure"] = {"verdict": "NOT_RUN", "clause": "not_a_222_surface"}
    res["verdict"], res["clause"] = "OK", None
    return res


def run(quick=False, with_singular=True, log=print):
    lattice = {f: load_lattice_side(f) for f in LOCI_CERT}
    results = {}
    for name, model in MODELS.items():
        log(f"== {name} ({model['family']})")
        r = analyse_model(name, model, load_loci(model["family"]), quick, with_singular)
        results[name] = r
        log(f"   CT: {r['ct']['verdict']}")
        for p in r["torus"]["points"]:
            log(f"   torus critical point {p['point']}: value {p['critical_value']} (z = {p['z']}), "
                f"Hessian rank {p['hessian_rank']}")
        log(f"   compare with loci {r['loci']}: {r['compare']['clauses'] or 'equal'}")
        log(f"   value-0 critical locus positive-dimensional: {r['value_zero']['positive_dimensional']}")
        k = r["closure"]
        if k["verdict"] == "OK":
            log(f"   closure: generic signature {k['generic_signature']}; special: "
                + str({l: (v['signature'], v['kinds'], v['clause']) for l, v in k['special'].items()}))
            s = r.get("singular_leg", {})
            if s.get("verdict") == "OK":
                log(f"   Singular: generic total Tjurina {s['generic_total_tjurina']}, others "
                    f"{s['members_with_other_total_tjurina']}, count disagreements "
                    f"{s['point_count_disagreements_with_sympy']}")
                for lp in s["local"]:
                    log(f"      lambda {lp['lam']} chart {lp['chart']} {lp['point_in_chart']}: "
                        f"mu {lp['milnor']} tau {lp['tjurina']} corank {lp['hessian_corank_sympy']} "
                        f"-> {lp['label']}")
            else:
                log(f"   Singular leg: {s.get('clause')}")
            cl = r.get("completeness_leg", {})
            if cl.get("verdict") == "OK":
                log(f"   leg C: total Tjurina differs from generic exactly at lambda in "
                    f"{cl['lambda_where_total_tjurina_differs_from_generic']}; non-isolated at "
                    f"{cl['lambda_with_non_isolated_singular_points']}; generic over Q(lambda) "
                    f"{cl['generic_over_Q_of_lambda']}; vs scan: {r['completeness_vs_scan']}")
            elif cl:
                log(f"   leg C: {cl.get('clause')}")
        else:
            log(f"   closure: {k['clause']}")
    known_bad = {}
    for name, model in KNOWN_BAD_MODELS.items():
        c = check_ct(model)
        known_bad[name] = {"provenance": model["provenance"], "verdict": c["verdict"],
                           "clause": c["clause"],
                           "first_mismatch_index": c.get("first_mismatch_index"),
                           "constant_terms": c["constant_terms"][:6], "sequence": c["sequence"][:6]}
        log(f"== known-bad {name}: {c['verdict']} ({c['clause']} at n = {c.get('first_mismatch_index')})")
    refs = {f: refs_crosscheck(f) for f in LOCI_CERT}
    log(f"refs cross-check: {refs}")
    gates = {
        "refs_crosscheck": all(v["agree"] for v in refs.values()),
        "complete_special_set_equals_scan_or_second_CAS_absent": all(
            r.get("completeness_vs_scan", {}).get("agree") is not False
            and r.get("completeness_leg", {}).get("verdict") != "REFUSED"
            for r in results.values()),
        "all_models_pass_ct": all(r["ct"]["clause"] is None for r in results.values()),
        "known_bad_models_refused": all(k["clause"] == "ct_mismatch" for k in known_bad.values()),
        "torus_lists_complete_zero_dimensional": all(r["verdict"] == "OK" for r in results.values()),
        "no_torus_critical_value_outside_certified_loci":
            all(not r["compare"]["extra"] for r in results.values()),
        "closure_probes_agree": all(r["closure"]["verdict"] in ("OK", "NOT_RUN")
                                    for r in results.values()),
        "two_CAS_agree_on_point_counts_or_second_CAS_absent": all(
            not r.get("singular_leg", {}).get("point_count_disagreements_with_sympy")
            and r.get("singular_leg", {}).get("verdict") != "REFUSED" for r in results.values()),
    }
    scored = score(results, lattice)
    for s in scored:
        log(f"   [{s['outcome']}]{' ADVISORY' if s['advisory'] else ''} {s['clause']} -- {s['basis']}")
    log(f"gates: {gates}")
    return results, known_bad, gates, scored, lattice, refs


# --------------------------------------------------------------------------------------
# brief (rendered from the certificate; no number is typed)
# --------------------------------------------------------------------------------------
BRIEF = REPO / "briefs" / "STREAM2_NODALITY_EXPLICIT_MODELS_2026_09_21.md"


class BriefStale(Exception):
    """The certificate no longer supports a sentence of the brief (E-015 guard)."""


def _require(cond, what):
    if not cond:
        raise BriefStale(f"brief_prose_not_supported_by_certificate: {what}")


def _closure_facts(m):
    """Everything sections 4-5 say about one (2,2,2) model, READ from the certificate."""
    K, Sg = m["closure"], m.get("singular_leg", {})
    _require(K["verdict"] == "OK", "closure leg ran")
    g = K["generic_signature"]
    out = {"generic_points": g[0], "generic_ranks": g[1], "members": {}}
    has_s = Sg.get("verdict") == "OK"
    non_a1 = lambda lam: Counter(l_["label"] for l_ in Sg["local"]
                                 if l_["lam"] == lam and l_["label"] != "A1")
    generic_non_a1 = non_a1(str(PROBES[0])) if has_s else None
    for lam, v in K["special"].items():
        pts = v["points"]
        torus = [p for p in pts if p["on_torus"]]
        rest = [p for p in pts if not p["on_torus"]]
        tt = (lookup_number(Sg["members_with_other_total_tjurina"], lam)
              if Sg.get("verdict") == "OK" else None)
        out["members"][lam] = {
            "z": v["z"], "locus": v["z_is_certified_locus"], "points": len(pts),
            "new_torus": len(torus), "new_torus_ranks": sorted(p["hessian_rank"] for p in torus),
            "new_torus_rational": [p["rational"] for p in torus],
            "others": len(rest), "others_ranks": sorted(p["hessian_rank"] for p in rest),
            "others_unchanged": sorted(p["hessian_rank"] for p in rest) == g[1],
            "min_rank": min(p["hessian_rank"] for p in pts),
            "tjurina_change": (None if tt is None else tt - Sg["generic_total_tjurina"]),
            # non-A1 labels of this member that the generic member (probe) does not have
            "labels": (sorted((non_a1(lam) - generic_non_a1).elements()) if has_s else None)}
    out["generic_non_A1_labels"] = sorted(generic_non_a1.elements()) if has_s else None
    return out


def _plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")


def brief_text(c):
    M, L = c["models"], c["lattice_side_read_from"]["rational_z"]
    o = []
    a = o.append
    a("# Stream 2 brief: singular members of explicit models of the cooper_s7 / cooper_s10 "
      "pencils, against the lattice side (2026-09-21)")
    a("")
    a("**Status: RECORD, NOT A GATE.** Tier **B**. Nothing is scored or ranked; `K3_CRITERIA.md` is "
      "unchanged; the rho = 20 cut and T3 are not adopted. All cooper_s10 output is **ADVISORY** "
      f"(flags {c['flags']['cooper_s10']}: its lattice certificate is DRAFT). This is algebraic geometry of "
      "explicit surfaces; it carries no physical reading. No Kodaira reading is made (ledger item 3): "
      "the singular objects below are points of **surfaces** (members of a pencil), named each time.")
    a("")
    a(f"Rendered from `data/certificates/NODALITY_EXPLICIT_MODELS.json` by "
      f"`python3 checkers/check_nodality_explicit_models.py --brief`; code identity `{c['checker_version']}`; "
      f"certificate verdict **{c['verdict']}** (integrity gates only: {sum(c['gates'].values())}/{len(c['gates'])} hold). "
      "The hand estimate is scored in section 6 and is not part of that verdict.")
    a("")
    a("## 1. Question")
    a("")
    a("The lattice side (`CM_POINTS_RHO20.json`, Tier B) places the finite singular points of L3 at these vectors of T_n:")
    a("")
    a("| family | z | -v^2 | div v | reflective | D |")
    a("|---|---|---|---|---|---|")
    for fam in ("cooper_s7", "cooper_s10"):
        for zv in M["s7_a" if fam == "cooper_s7" else "s10_a"]["loci"] + ["infinity"]:
            r = L[fam][zv]
            a(f"| {fam}{' (ADVISORY)' if fam in c['advisory_families'] else ''} | {zv} | {r['minus_v2']} | {r['div_v']} | {r['reflective']} | {r['D']} |")
    a("")
    a("The orchestrator's hand estimate (UNVERIFIED when issued): at a (-2)-vector the polarized model acquires one "
      "ordinary double point (an A1 point of the surface); at the other points no such statement is made. The test asked "
      "for: an explicit model, no lattice, no monodromy.")
    a("")
    a("## 2. Models, and the constant-term gate")
    a("")
    a("A Laurent polynomial P with CT(P^n) = s(n) gives the pencil {P = lambda}, z = 1/lambda. No P is used before the "
      "identity is checked exactly. Almkvist-van Straten (arXiv:2103.08651, pinned; read) describe the surfaces as six "
      "hyperplane sections of G(2,6) and four (1,1) sections of P^3 x P^3 and refer to Gorodetsky for Laurent "
      "polynomials; they print no equations, so their models are **not explicit enough to use** and are not used.")
    a("")
    a("| model | family | P = N / (xyz), N = | provenance | CT identity |")
    a("|---|---|---|---|---|")
    for k, m in M.items():
        a(f"| {k} | {m['family']} | `{m['N']}` | {m['provenance']} | {m['ct']['verdict']} |")
    a("")
    a("Real known-bads (refused before any geometry, clause named):")
    a("")
    for k, m in c["known_bad_models"].items():
        a(f"- `{k}`: {m['verdict']}, clause `{m['clause']}`, first mismatch at n = {m['first_mismatch_index']} "
          f"(CT {m['constant_terms'][:4]} against {m['sequence'][:4]}) - {m['provenance']}")
    a("")
    late = {k: m["first_mismatch_index"] for k, m in c["known_bad_models"].items() if m["first_mismatch_index"] > 1}
    a(f"PASS({c['order_checked']}) is a finite order: what the machine checked is n <= {c['order_checked']}, which is evidence and "
      "not a proof. For the models whose provenance reads 'derived here' the provenance column is a hand derivation "
      "valid for every n (a hand argument, not machine-checked); the model 'written from recollection' rests on the "
      f"finite order alone. Known-bads that survive n = 1 and are refused later: {late or 'none'}; control S2 shows a wrong P "
      "that passes at order 3 and is refused at order 4. The closed forms are cross-checked against "
      f"`refs/recurrences_v1.json` for n <= { {f: v['covers_n_up_to'] for f, v in c['refs_crosscheck'].items()} } only "
      "(that is all the register holds); beyond that the sequence is the closed form itself. Control S9 tampers a refs term "
      "(`refs_mismatch`).")
    a("")
    a("## 3. Torus critical points (exact; complete for the torus with P != 0)")
    a("")
    a("Groebner basis with a Rabinowitsch variable; the ideal is zero-dimensional in every model, so the list is complete "
      "for (C*)^3 with P != 0. Hessian rank 3 means a nondegenerate critical point: the member {P = value} has an A1 point "
      "there and the total space of the pencil is smooth there.")
    a("")
    a("| model | critical point | value | z | Hessian rank | Morse | coordinates rational |")
    a("|---|---|---|---|---|---|---|")
    for k, m in M.items():
        for p in m["torus"]["points"]:
            a(f"| {k} | ({', '.join(p['point'])}) | {p['critical_value']} | {p['z']} | {p['hessian_rank']} | {p['morse']} | {p['rational']} |")
    a("")
    for k, m in M.items():
        cm = m["compare"]
        a(f"- {k}: torus critical points per z = {cm['critical_points_per_z']}; certified loci {m['loci']}; "
          f"loci with no torus critical point: {cm['missing'] or 'none'}; critical values outside the loci: {cm['extra'] or 'none'}; "
          f"clauses: {cm['clauses'] or 'none'}.")
    a("")
    a("**z = infinity.** In every model the torus critical points with P = 0 form a positive-dimensional set "
      f"({ {k: m['value_zero']['positive_dimensional'] for k, m in M.items()} }), and the member lambda = 0 has non-isolated "
      "singular points (control R8). Nothing is said here about z = infinity: the order-3 statement of the lattice side is "
      "neither supported nor contradicted.")
    a("")
    a("## 4. The (2,2,2) closure in P^1 x P^1 x P^1 (s7_b and s10_a)")
    a("")
    a("Where N has degree at most 2 in each variable, the closure of {P = lambda} is a (2,2,2) surface. For each lambda "
      "of a logged finite list (1/z for every rational z of the lattice certificate, the probes, and an integer window) "
      "all singular points of that surface are computed in eight charts, with the Hessian rank of the local equation. "
      "Signature = [number of singular points, sorted Hessian ranks]. The optional second CAS (Singular) adds total "
      "Tjurina numbers, and Milnor / Tjurina numbers at the rational singular points.")
    a("")
    for k, m in M.items():
        K = m["closure"]
        if K["verdict"] != "OK":
            a(f"- **{k}**: leg not run, clause `{K['clause']}`: the boundary of this model is not examined.")
            continue
        S = m.get("singular_leg", {})
        a(f"- **{k}**: {len(K['lambdas_scanned'])} members scanned (lambda from {K['lambdas_scanned'][0]} to {K['lambdas_scanned'][-1]}); "
          f"generic signature {K['generic_signature']}"
          + (f"; generic total Tjurina number {S['generic_total_tjurina']}; point counts of the two CAS disagree on "
             f"{len(S['point_count_disagreements_with_sympy'])} members" if S.get("verdict") == "OK" else f"; second CAS: `{S.get('clause')}`") + ".")
        for lam, v in K["special"].items():
            loc = [l for l in S.get("local", []) if l["lam"] == lam] if S.get("verdict") == "OK" else []
            labels = sorted(l["label"] for l in loc)
            tt = S["members_with_other_total_tjurina"].get(lam) if S.get("verdict") == "OK" else None
            a(f"  - lambda = {lam} (z = {v['z']}): signature {v['signature']}, kinds {v['kinds']}, "
              f"z is a certified locus: {v['z_is_certified_locus']}"
              + (f", clause `{v['clause']}`" if v["clause"] else "")
              + (f"; total Tjurina {tt}; rational singular points by (corank, Milnor number): {labels}" if loc else "")
              + ("; non-rational points are not sent to the second CAS" if any(not p["rational"] for p in v["points"]) else "") + ".")
    a("")
    a("**Leg C (second CAS; complete, not a scan).** Primary decomposition of the relative singular scheme over Q[lambda], "
      "chart by chart: the members whose total Tjurina number differs from the generic one are exactly the roots of the "
      "eliminants of the vertical associated primes (finite module over a PID = free + torsion; standard, used as an "
      "argument, not machine-checked).")
    a("")
    for k, m in M.items():
        cl = m.get("completeness_leg")
        if not cl:
            continue
        if cl["verdict"] != "OK":
            a(f"- {k}: leg C not run, clause `{cl['clause']}`; the special set of leg K is then a finite scan only.")
            continue
        cv = m["completeness_vs_scan"]
        a(f"- {k}: total Tjurina number differs from generic exactly at lambda in {cl['lambda_where_total_tjurina_differs_from_generic']}; "
          f"non-isolated singular points exactly at lambda in {cl['lambda_with_non_isolated_singular_points']}; generic member over "
          f"Q(lambda): {cl['generic_over_Q_of_lambda']['singular_points']} singular points, total Tjurina number "
          f"{cl['generic_over_Q_of_lambda']['total_tjurina']}. Against leg K: agree = {cv['agree']}"
          + (f", clause `{cv['clause']}`" if cv["clause"] else "") + ". So no other scanned member (the other rational CM "
          "values of the lattice certificate included) is special on this model in this sense.")
    a("")
    a("Plain reading of what is observed on s7_b, the model where the boundary is examined:")
    a("")
    f7, f10 = _closure_facts(M["s7_b"]), _closure_facts(M["s10_a"])
    m27, mm1, m2 = (lookup_number(f7["members"], q) for q in (27, -1, 2))
    _require(m27 and mm1 and m2, "s7_b special members at lambda = 27, -1, 2")
    _require(len(f7["members"]) == 3, "s7_b has exactly three special members")
    t7a = [p for p in M["s7_a"]["torus"]["points"]]
    _require(m27["new_torus"] == 1 and m27["new_torus_ranks"] == [3] and m27["others_unchanged"] and m27["locus"],
             "s7_b z = 1/27: one new A1 point on the torus, nothing else changes")
    _require(len(t7a) == 1 and t7a[0]["morse"] and same_number(t7a[0]["z"], "1/27"), "s7_a: one Morse point over 1/27")
    a(f"- z = {m27['z']}: {_plural(m27['new_torus'], 'new A1 point')} (Hessian rank {m27['new_torus_ranks']}), on the torus; "
      f"the other {m27['others']} singular points keep the generic Hessian ranks. s7_a (torus only): "
      f"{_plural(len(t7a), 'Morse critical point')} over z = {t7a[0]['z']}."
      + (f" Total Tjurina number change {m27['tjurina_change']:+d}." if m27["tjurina_change"] is not None else ""))
    _require(mm1["new_torus"] == 0 and mm1["points"] < f7["generic_points"] and mm1["locus"],
             "s7_b z = -1: no new singular point, points merge")
    a(f"- z = {mm1['z']}: **no new singular point.** The number of singular points goes {f7['generic_points']} -> {mm1['points']}: "
      f"singular points of the generic member merge, and the lowest Hessian rank on the member is {mm1['min_rank']}"
      + (f" (second CAS: non-A1 labels of this member that the generic member does not have: {mm1['labels']}; the generic "
         f"member already has {f7['generic_non_A1_labels']})" if mm1["labels"] is not None else "")
      + (f". Total Tjurina number change {mm1['tjurina_change']:+d}, against {m27['tjurina_change']:+d} at z = {m27['z']}"
         if mm1["tjurina_change"] is not None else "") + ".")
    _require(m2["new_torus"] == 0 and m2["points"] == f7["generic_points"] and not m2["locus"]
             and not m2["others_unchanged"], "s7_b z = 1/2: a Hessian rank drops, L3 regular")
    a(f"- z = {m2['z']}: same number of singular points ({m2['points']}), Hessian ranks {f7['generic_ranks']} -> {m2['others_ranks']}"
      + (f", total Tjurina number change {m2['tjurina_change']:+d}" if m2["tjurina_change"] is not None else "")
      + (f", non-A1 labels the generic member does not have: {m2['labels']}" if m2["labels"] is not None else "")
      + ", and **L3 is regular there**. A change of signature is therefore NOT a detector of singular points of the operator "
      "(control R4). On the lattice side z = 1/2 is a CM point of a non-reflective vector "
      f"(-v^2 = {L['cooper_s7']['1/2']['minus_v2']}, div {L['cooper_s7']['1/2']['div_v']}, D = {L['cooper_s7']['1/2']['D']}).")
    a("")
    n16, nm4 = lookup_number(f10["members"], 16), lookup_number(f10["members"], -4)
    _require(n16 and nm4 and len(f10["members"]) == 2, "s10_a special members are lambda = 16 and -4")
    _require(all(q["others_unchanged"] and set(q["new_torus_ranks"]) == {3} for q in (n16, nm4)),
             "s10_a: new points are A1 on the torus, generic points unchanged")
    a(f"and on s10_a (ADVISORY): z = {n16['z']}: {_plural(n16['new_torus'], 'new A1 point')} on the torus (rational: "
      f"{n16['new_torus_rational']}); z = {nm4['z']}: **{_plural(nm4['new_torus'], 'new A1 point')}** on the torus (rational: "
      f"{nm4['new_torus_rational']}; coordinates in Q(i), exchanged by conjugation: see the table of section 3); the "
      f"{f10['generic_points']} singular points of the generic member keep their Hessian ranks at both values"
      + (f"; total Tjurina number changes {n16['tjurina_change']:+d} and {nm4['tjurina_change']:+d}"
         if n16["tjurina_change"] is not None else "") + ".")
    a("")
    a("## 5. A reading through root systems - HYPOTHESIS, not checked")
    a("")
    R = c["root_system_arithmetic_for_remark"]
    a("Exact integer arithmetic (in the certificate, control S7): in the D4 root lattice take three mutually orthogonal "
      f"roots e_i; the roots orthogonal to all three are {R['roots_of_D4_orthogonal_to_all_e_i']} (one root up to sign), and "
      f"A1^3 plus that root has index {R['index_of_A1^3_plus_that_root_in_D4']} in D4. In A2 the roots orthogonal to a given root: "
      f"{R['roots_of_A2_orthogonal_to_a_root'] or 'none'}. The sum of two orthogonal roots has norm {R['sum_of_two_orthogonal_roots_has_norm']}.")
    a("")
    merged = f7["generic_points"] - mm1["points"] + 1
    _require(R["their_pairing"] == 0, "the two roots summed are orthogonal")
    lat = {q: lookup_number(L["cooper_s7"], q) for q in ("-1", "1/27")}
    lat10 = {q: lookup_number(L["cooper_s10"], q) for q in ("-1/4", "1/16")}
    a("If - and this is the unverified step - the singular points of a member correspond to roots among the algebraic "
      f"classes orthogonal to the model's polarization, the observations would read: s7 z = {mm1['z']}, {merged} singular points "
      f"merging into one (new label {mm1['labels']}), as one new root glued to the old ones with index "
      f"{R['index_of_A1^3_plus_that_root_in_D4']}, where the lattice vector has div {lat['-1']['div_v']}; s7 z = {m27['z']} and s10 z = "
      f"{n16['z']}, an isolated new A1, where the lattice vectors have div {lat['1/27']['div_v']} and {lat10['1/16']['div_v']}; s10 z = "
      f"{nm4['z']}, {_plural(nm4['new_torus'], 'A1 point')} exchanged by conjugation, as a vector delta_1 + delta_2 of norm "
      f"{R['sum_of_two_orthogonal_roots_has_norm']}, where the lattice vector has -v^2 = {lat10['-1/4']['minus_v2']}, div "
      f"{lat10['-1/4']['div_v']}; s7 z = {m2['z']}, new label {m2['labels']}, no new root orthogonal to the old one "
      f"({R['roots_of_A2_orthogonal_to_a_root'] or 'none'} in A2), and the operator is regular there.")
    a("")
    a("**This reading is post hoc.** It was written in this document AFTER the observations of section 4 and was built "
      "from them; the observations it accommodates are therefore fits, not tests, and are not counted as agreement. "
      "**Independent tests passed so far: 0.** A first real test would be a second compactification of the same pencil, "
      "or a boundary analysis of s7_a, with the expected local types written down BEFORE the computation. The "
      "identification of roots with classes on the surface is not computed here.")
    a("")
    a("Thought experiment, kept as an aid to discussion only. Picture the pencil as a drum whose skin is re-tensioned as "
      "lambda moves. A (-2)-wall says: somewhere one cycle is pinched to a point. The lattice tells you THAT a cycle is "
      "pinched; it does not tell you WHERE on a given drawing of the drum the pinch shows. On one drawing (the torus chart) "
      "the pinch at z = 1/27 is in full view; the pinch at z = -1 happens at the rim, where old dents already sit, "
      f"and what one sees is {merged} dents running together. The drawing is not the drum: that is the content of the "
      "word 'birational' in section 8.")
    a("")
    a("## 6. Hand estimate, scored")
    a("")
    a("| clause | outcome | basis |")
    a("|---|---|---|")
    for s_ in c["hand_estimate_scored"]:
        a(f"| {s_['clause']}{' **[ADVISORY]**' if s_['advisory'] else ''} | **{s_['outcome']}** | {s_['basis']} |")
    a("")
    pred = [s_ for s_ in c["hand_estimate_scored"] if "comes from a (-2)-vector" in s_["clause"]]
    held = [s_["clause"].split(",")[0] for s_ in pred if s_["outcome"].startswith("confirmed")]
    failed = [s_["clause"].split(",")[0] for s_ in pred if s_["outcome"].startswith("literal clause FAILS")]
    unseen = [s_["clause"].split(",")[0] for s_ in pred if s_["outcome"].startswith("NOT OBSERVED")]
    _require(len(held) + len(failed) + len(unseen) == len(pred), "every (-2)-vector clause is classified")
    _require(mm1["tjurina_change"] is not None and mm1["tjurina_change"] == m27["tjurina_change"],
             "total Tjurina change at s7_b z = -1 equals the change at z = 1/27")
    a(f"Summary (model-level in every line; s10 ADVISORY). The clause '(-2)-vector => exactly one new A1 point' holds on: "
      f"{held or 'none'}. Its literal form fails on: {failed or 'none'}. It is not observed on the torus, boundary not "
      f"examined, on: {unseen or 'none'}. Where it fails, the outcome column records the change of the total Tjurina number, "
      f"which is {mm1['tjurina_change']:+d}, the same as at the locus where the clause holds: the model shows a different local picture with the same "
      "total, and that is NOT a refutation of the lattice side. Whether the M_7-polarized model has an A1 point at z = -1 "
      "stays open, since neither model is the M_7-polarized one.")
    a("")
    a("## 7. Controls")
    a("")
    cf = c["controls_file"]
    tests = (REPO / cf["path"]).read_text()
    ids = ["R%d" % i for i in range(1, 11)] + ["S%d" % i for i in range(1, 11)]
    _require(all(f"def test_{i}_" in tests for i in ids) and cf["number_of_controls"] == len(ids),
             "the controls named in section 7 exist in the controls file")
    a(f"`{cf['path']}`, {cf['number_of_controls']} controls, each naming the clause that fired. Real: R1 {len(c['known_bad_models'])} "
      f"wrong polynomials (`ct_mismatch`, no geometry computed; surviving n = 1: {sorted(late) or 'none'}); R2 cross-family both ways "
      "(`critical_value_not_a_certified_locus`); R3 (x-1)^3-type toy (`hessian_degenerate`, NOT Morse); R4 s7_b at "
      "lambda = 2 (`model_special_but_operator_regular`); R5 Morse toy with 4 critical points (non-vacuity); R6 non-isolated "
      "critical points (`critical_locus_not_zero_dimensional`); R7 `not_a_222_surface`; R8 the member at z = infinity "
      "(`singular_locus_not_isolated`); R9 the headline observations; R10 a scan list that omits special members "
      "(`complete_special_set_differs_from_scan`), and leg C on a shifted pencil finds members outside the scanned window. "
      "Tamper: S1, S2 (low-order CT accepts a wrong P), S3 tampered loci, S4 `probes_disagree_on_generic_signature`, "
      "S5 `singular_leg_not_run`, S6 `unlabelled`, S7 root arithmetic, S8 a critical value 10^-20 away from a certified "
      "locus is NOT matched (exact comparison), S9 tampered refs term (`refs_mismatch`), S10 this brief refuses to render "
      "from a certificate that no longer supports its sentences (`brief_prose_not_supported_by_certificate`).")
    a("")
    a("Clauses with no control, stated: `solution_does_not_satisfy_equations` and `singular_output_unparsed` are exercised "
      "only on their passing side; a disagreement between the two CAS on point counts has not been provoked.")
    a("")
    a("## 8. Not claimed")
    a("")
    for n in c["not_claimed"]:
        a(f"- {n}")
    a("")
    a("Tier statement: leg CT, leg T, leg Z, leg K are exact (integers, sympy over Q and Q(i); zero tests are structural or "
      "by minimal polynomial, no numeric recognition anywhere); they are Tier B because "
      "CT is a finite order, leg K is a finite list (leg C's completeness rests on an argument that is not "
      "machine-checked), and the link from a model's singular points to the "
      "lattice side is the cited framework, not a computation. Singular-point names rest on the optional second CAS plus "
      "Arnold's list (standard, cited not proved).")
    a("")
    a(c["provenance"])
    return "\n".join(o) + "\n"


def render_brief():
    BRIEF.write_text(brief_text(json.loads(OUT.read_text())))
    print(f"wrote {BRIEF.relative_to(REPO)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--quick", action="store_true", help="skip the integer window of leg K")
    ap.add_argument("--brief", action="store_true", help="render the brief from the certificate")
    args = ap.parse_args()
    if args.brief:
        render_brief()
        return 0
    results, known_bad, gates, scored, lattice, refs = run(quick=args.quick)
    ok = all(gates.values())
    if args.emit:
        try:
            ver = subprocess.run(["git", "describe", "--always", "--dirty"], cwd=REPO,
                                 capture_output=True, text=True).stdout.strip()
        except Exception:
            ver = "unknown"
        files = [REFS, CM_CERT] + [CERTS / f for f in LOCI_CERT.values()] + [Path(__file__)]
        cert = {
            "certificate": "NODALITY_EXPLICIT_MODELS",
            "checker": "checkers/check_nodality_explicit_models.py",
            "checker_version": ver, "date": "2026-09-21",
            "status": "RECORD_NOT_A_GATE", "tier": "B",
            "verdict": (f"PASS({CT_ORDER})" if ok else "FAIL"),
            "order_checked": CT_ORDER,
            "verdict_scope": "integrity gates only; the hand estimate is scored separately and "
                             "is NOT part of the verdict",
            "advisory_families": [f for f in lattice if lattice[f]["advisory"]],
            "flags": {f: lattice[f]["flags"] for f in lattice},
            "quick_mode": args.quick,
            "gates": gates,
            "refs_crosscheck": refs,
            "controls_file": {"path": "checkers/test_nodality_explicit_models_controls.py",
                              "number_of_controls": count_controls()},
            "hand_estimate_scored": scored,
            "lattice_side_read_from": {"file": str(CM_CERT.relative_to(REPO)),
                                       "rational_z": {f: lattice[f]["rational_z"] for f in lattice}},
            "models": results, "known_bad_models": known_bad,
            "root_system_arithmetic_for_remark": root_system_remark(),
            "not_claimed": NOT_CLAIMED,
            "inputs": {"sha256": {str(p.relative_to(REPO)): sha256_file(p) for p in files}},
            "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: "
                          "checkers/test_nodality_explicit_models_controls.py; optional second "
                          "CAS (Singular) | Reviewed-by: N",
        }
        OUT.write_text(json.dumps(cert, indent=1, sort_keys=True, default=str) + "\n")
        print(f"wrote {OUT.relative_to(REPO)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
