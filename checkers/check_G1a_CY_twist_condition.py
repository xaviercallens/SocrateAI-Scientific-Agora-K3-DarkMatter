#!/usr/bin/env python3
"""
check_G1a_CY_twist_condition.py — WP S2-G Phase G1-a (CY/twist condition)
(briefs/WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md sec.1 & sec.5, G1-a bullet;
phase opened by T0 2026-07-28, briefs/T0_DECISIONS_2026_07_28_STREAM2.md item 2).

WHAT THIS COMPUTES
------------------
Route A pulls the certified cooper_s7 K3 family back over a base surface B2
via a moduli map phi: B2 -> (z-line), producing X4 = B2 x_{zline} Y (Y = the
family's total space, compactified over its own modular curve). Since
dim(B2)=2 > dim(zline)=1, any non-constant phi is necessarily a fibration
with 1-dimensional generic fiber (dimension count).

Because the generic fiber (a K3 surface) has trivial canonical bundle,
K_{Y/zline} descends to a line bundle L on zline of some fixed integer
degree ell (the family's Hodge/discriminant-degree invariant — NOT computed
here, see "WHAT THIS DOES NOT COMPUTE" below). Flat base change along phi
gives, exactly:

    K_{X4/B2} = pi^*( phi^*L ),    pi: X4 -> B2

so
    K_{X4} = pi^*( K_{B2} (+) phi^*L )         [additive/tensor notation
                                                 mixed for readability; see
                                                 module derivation below for
                                                 the precise Pic-additive form]

and the CY condition c1(X4)=0 (K_{X4} trivial) is EQUIVALENT, on the base,
to:

    K_{B2} = -ell * F        (*)

where F = phi^*(point) is the fiber class of phi (F^2 = 0 always, since
fibers of a fibration are pairwise disjoint). This is the K3-fibration
analogue of the elliptic-surface Weierstrass twist condition the plan's
G1-a bullet names.

THE RESULT (obstruction, ell-independent): for every B2 in the plan's own
proposed ladder (P^2; every Hirzebruch surface F_n, n>=0, which includes
P^1xP^1 as F_0), condition (*) has NO SOLUTION for any integer ell and any
choice of phi — proven exactly, via linear algebra over the Picard lattice,
without ever needing to know ell. Two independent failure modes:

  - P^2: Pic(P^2) = Z*H is rank 1 and POSITIVE DEFINITE (H^2=1>0). A rank-1
    positive-definite lattice contains NO nonzero isotropic vector (n^2*k=0,
    k>0 => n=0 over Q). Since any candidate fiber class F must be isotropic
    (F^2=0) and any nonzero divisor class must be a multiple of H, NO
    algebraic fibration phi: P^2 -> (curve) exists AT ALL — condition (*)
    is not merely unsolved, it has no candidate F to even test. (Also
    reproduces the classical Bezout fact: two curves of degree e>=1 in P^2
    meet in e^2>0 points, so no base-point-free pencil exists for e>=1.)

  - F_n (all n>=0, incl. P^1xP^1=F_0): Pic(F_n) = Z*s (+) Z*f (section,
    fiber), with the STANDARD ruling phi = the P^1-bundle projection, fiber
    class F=f (f^2=0, verified). K_{F_n} is DERIVED here (not assumed) via
    the adjunction/genus-degree formula 2g(C)-2 = C^2 + K.C applied to the
    two rational curves s (g=0, s^2=-n) and f (g=0, f^2=0), giving the
    linear system that pins K_{F_n} = -2s - (n+2)f exactly, for every n.
    Matching K_{F_n} against -ell*f requires the s-coefficient to vanish:
    -2 = 0 — FALSE for every n, every ell. UNSOLVABLE, ell-independent,
    n-independent. (Corollary cross-check: K_{F_n}^2 = 8 != 0 for all n,
    computed via the Gram pairing — the ell-independent K^2=0 necessary
    condition from squaring (*) is a second, coarser proof of the same
    failure, kept as an independent arithmetic cross-check.)

The CONSTANT-phi case (X4 = B2 x K3, requiring K_{B2}=0) is also checked
and also fails for both B2's: K_{P^2}=-3H != 0 (coefficient -3 != 0);
K_{F_n}=-2s-(n+2)f != 0 (coefficient of s is -2 != 0 for every n).

POSITIVE CONTROL (proves this checker is not a stub that always returns
OBSTRUCTED): a degree-9 del Pezzo surface dP9 (= P^2 blown up at 9 points,
Pic = Z*H (+) Z*E_1 (+) ... (+) Z*E_9, Gram diag(1,-1,...,-1)) with its
classical anticanonical elliptic fibration (fiber class F=-K, a textbook
fact [B: cited, not re-derived — Cossec-Dolgachev / any rational-elliptic-
surface reference], verified here to satisfy F^2=0 exactly) DOES satisfy
(*), with ell SOLVED (not assumed) to be exactly 1.

WHAT THIS DOES NOT COMPUTE
---------------------------
- ell itself (the Hodge-bundle degree of the cooper_s7 family over its
  modular curve X0(7)+/z-line) — no orbifold Riemann-Hurwitz/Roch on
  X0(7)+ is attempted here. The obstruction result above holds for EVERY
  possible value of ell, so ell's actual value is immaterial to it — this
  is a strength (the result is robust to a quantity this repo has not yet
  derived), stated explicitly rather than silently assumed away.
- G1-b (degenerate-fiber crepant resolution) or G1-c (elliptic/F-theory
  posability) — moot for these B2's since G1-a already fails for them.
- Whether K3-fibered CY fourfolds over P^2 or F_n exist AT ALL by some
  OTHER construction. The obstruction here is specific to the NAIVE
  fiber-product pullback of a FIXED 1-parameter family along a FIXED
  moduli map phi (exactly what the plan's G1-a bullet asks about). The
  plan's own "-4K/-6K Weierstrass twisting" analogy may refer to a more
  general construction — choosing the total space directly via twisted
  sections on B2 rather than factoring through a fixed map to a fixed
  1-dimensional modulus — which this checker does NOT test and which
  would need an explicit Weierstrass-like presentation of the M-polarized
  family on B2 directly (out of scope for this deliverable; flagged as
  the natural next question if Route A is pursued further on this ladder).
  See not_claimed in the emitted certificates.

TIER: every step in this file is exact classical algebraic geometry
(canonical-class-via-adjunction, Picard-lattice linear algebra, Bezout/
isotropy) computed with sympy Integer/Rational only — no floats, no
numerical tolerance, and (unlike G0) no dependence on the family's
monodromy-derived transcendental lattice T at all, since ell cancels out
of the argument entirely. Tier E (exact) for the arithmetic; see each
certificate's "tier"/"tier_reason" for the DRAFT/no-self-promotion caveat.

Usage:
  python3 checkers/check_G1a_CY_twist_condition.py                # print only
  python3 checkers/check_G1a_CY_twist_condition.py --emit-cert    # write both certs

Exit codes: 0 all structural assertions (preconditions, cross-checks)
passed — NOTE this is independent of whether the CY condition itself was
found ADMISSIBLE or OBSTRUCTED; OBSTRUCTED is a valid, non-error outcome
recorded in the certificate. 3 a structural PRECONDITION failed (malformed
input, e.g. a non-isotropic candidate fiber class) — this is the checker
refusing to answer an ill-posed question, not a geometry result.

Generated-by: Sonnet 5 (Stream 2, WP S2-G Phase G1-a session 2026-07-28)
Verified-by: this script's own structural assertions + checkers/test_G1a_CY_condition_controls.py
Reviewed-by: pending T0 (Xavier) — coordinator reviews and commits, no agent commits
"""

import argparse
import json
import sys
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parent.parent


class ControlFailure(Exception):
    """A structural PRECONDITION failed — the loud path. NOT the same as an
    OBSTRUCTED geometry verdict, which is a normal, valid return value."""


def chk(cond, msg):
    if not cond:
        raise ControlFailure(msg)


# ----------------------------------------------------------------------------
# generic exact primitives
# ----------------------------------------------------------------------------

def pairing(Gram, u, v):
    """Exact bilinear pairing u.v w.r.t. Gram, u,v as plain lists/tuples."""
    uv = sp.Matrix(u)
    vv = sp.Matrix(v)
    return (uv.T * Gram * vv)[0, 0]


def adjunction_canonical_class(Gram, curves, label):
    """DERIVE (not assume) the canonical class K = sum(a_i * basis_i) of a
    smooth projective surface with Picard lattice (basis, Gram), given a
    list of smooth rational curves C_i (each with known self-intersection,
    read off Gram) spanning the lattice, via the genus-degree/adjunction
    formula  2*g(C) - 2 = C^2 + K.C  with g(C)=0 for each (all curves used
    here are rational: lines in P^2, or the ruling's section/fiber in F_n).

    curves: list of coordinate vectors (in the same basis as Gram) of the
    spanning rational curves, one per basis vector (so the resulting linear
    system in the unknown coefficients a_i is square and, for the bases used
    here, uniquely solvable).

    Returns the exact coefficient vector [a_i] as sympy Rationals (Integers
    in all cases actually used in this file).
    """
    n = Gram.shape[0]
    chk(len(curves) == n, f"{label}: need exactly {n} spanning curves, got {len(curves)}")
    a = sp.symbols(f"a0:{n}")
    # Build K = sum_i a_i * curves[i] as a vector, then impose adjunction on
    # each spanning curve C_j: K.C_j = 2*g(C_j) - 2 - C_j.C_j = -2 - C_j^2
    # (g=0 for every curve used in this file).
    K_sym = sp.zeros(n, 1)
    for i in range(n):
        K_sym += a[i] * sp.Matrix(curves[i])
    eqs = []
    for j in range(n):
        Cj = sp.Matrix(curves[j])
        Cj_sq = (Cj.T * Gram * Cj)[0, 0]
        KdotCj = (K_sym.T * Gram * Cj)[0, 0]
        rhs = -2 - Cj_sq  # genus-degree formula, g(C_j)=0
        eqs.append(sp.Eq(KdotCj, rhs))
    sol = sp.solve(eqs, list(a), dict=True)
    chk(len(sol) == 1, f"{label}: adjunction linear system did not have a unique solution: {sol}")
    sol = sol[0]
    coeffs = [sp.nsimplify(sol[ai]) for ai in a]
    chk(all(c == sp.Integer(c) for c in coeffs), f"{label}: derived K coefficients not integral: {coeffs}")
    return [int(c) for c in coeffs]


def check_isotropic_existence_rank1(Gram1x1, label):
    """For a rank-1 lattice generated by v with v^2=k (k an integer, given
    nonzero), prove EXACTLY (symbolic solve, not just 'obviously') that the
    only integer n with (n*v)^2=0 is n=0 whenever k>0 — i.e. a positive-
    definite rank-1 lattice has no nonzero isotropic vector, hence supports
    no algebraic fibration (which would require a nonzero isotropic/fiber
    class)."""
    chk(Gram1x1.shape == (1, 1), f"{label}: expected 1x1 Gram, got {Gram1x1.shape}")
    k = Gram1x1[0, 0]
    chk(k != 0, f"{label}: rank-1 Gram is degenerate (k=0)")
    n = sp.Symbol("n", integer=True)
    sols = sp.solve(sp.Eq(n**2 * k, 0), n)
    only_zero = (sols == [0])
    return {
        "k": int(k),
        "positive_definite": bool(k > 0),
        "solutions_of_n^2*k=0": [str(s) for s in sols],
        "only_zero_isotropic_vector": bool(only_zero),
    }


def solve_proportionality(Gram, K_vec, F_vec, label):
    """Test K_vec = -ell * F_vec for the CY twist condition (*). First
    verifies F is isotropic (a genuine precondition for F to be a fibration
    fiber class: fails LOUDLY / raises if not — this is what the malformed-
    input control exercises). Then solves the proportionality component-
    wise, exactly over Q: returns a result dict with determination
    ADMISSIBLE (unique ell found) or OBSTRUCTED (no ell solves it) — this
    branch does NOT raise; OBSTRUCTED is a normal, valid finding."""
    n = Gram.shape[0]
    chk(Gram == Gram.T, f"{label}: Gram matrix not symmetric")
    chk(len(K_vec) == n and len(F_vec) == n, f"{label}: vector/Gram size mismatch")
    F_sq = pairing(Gram, F_vec, F_vec)
    chk(F_sq == 0, f"{label}: candidate fiber class F is not isotropic (F^2={F_sq}) "
        "-- F must satisfy F^2=0 to be the fiber class of an algebraic fibration "
        "over a curve (distinct fibers are disjoint, hence self-intersection 0); "
        "this input is malformed / does not describe a genuine fibration")

    ell_candidates = {}
    consistent = True
    reason = None
    for i, (k, f) in enumerate(zip(K_vec, F_vec)):
        if f == 0:
            if k != 0:
                consistent = False
                reason = (f"component {i}: K has nonzero coefficient {k} where F's "
                          f"coefficient is 0 -- no scalar ell can satisfy K=-ell*F")
                break
        else:
            ell_candidates[i] = sp.Rational(-k, f)
    if consistent and len(set(ell_candidates.values())) > 1:
        consistent = False
        reason = f"inconsistent per-component ratios {ell_candidates} -- K is not proportional to F"

    K_sq = pairing(Gram, K_vec, K_vec)  # ell-independent corollary cross-check: if K=-ell*F
    # and F^2=0 then K^2 = ell^2*F^2 = 0 identically -- so K^2 != 0 is an
    # independent (coarser, ell-blind) proof of the same obstruction.
    corollary_k_sq_zero = (K_sq == 0)

    if consistent:
        ell = ell_candidates.popitem()[1] if ell_candidates else sp.Integer(0)
        # verify every component agrees with this ell (guards a subtle bug:
        # a component with f=0,k=0 gives no info and must not silently pass)
        for k, f in zip(K_vec, F_vec):
            chk(k == -ell * f, f"{label}: internal inconsistency solving ell")
        return {
            "determination": "ADMISSIBLE",
            "ell": str(ell),
            "K_sq": int(K_sq),
            "corollary_K_sq_is_zero": bool(corollary_k_sq_zero),
            "reasoning": f"K = -ell*F solved exactly with ell={ell}; verified component-wise.",
        }
    return {
        "determination": "OBSTRUCTED",
        "ell": None,
        "K_sq": int(K_sq),
        "corollary_K_sq_is_zero": bool(corollary_k_sq_zero),
        "reasoning": (f"No ell in Q solves K=-ell*F for this (Gram,K,F): {reason}. "
                      f"Corollary cross-check: K^2={K_sq} "
                      f"{'== 0, so the ell-blind K^2 corollary is UNINFORMATIVE here (it cannot by itself rule out K=-ell*F); the per-component test above is the decisive one' if corollary_k_sq_zero else '!= 0, independently confirming no ell can work since K=-ell*F would force K^2=ell^2*F^2=0'}."),
    }


# ----------------------------------------------------------------------------
# B2 = P^2
# ----------------------------------------------------------------------------

def run_P2():
    Gram = sp.Matrix([[1]])  # Pic(P^2) = Z*H, H^2 = 1
    label = "P^2"

    iso = check_isotropic_existence_rank1(Gram, label)
    chk(iso["only_zero_isotropic_vector"], f"{label}: internal check failed unexpectedly")

    # DERIVE K_{P^2} via adjunction on a line L=H (g=0, L^2=1): 2*0-2=1+K.L
    K_coeffs = adjunction_canonical_class(Gram, curves=[[1]], label=label)
    chk(K_coeffs == [-3], f"{label}: derived K coefficients {K_coeffs} != expected [-3] "
        "(K_{P^2} = -3H is a standard fact; mismatch would indicate a bug in the "
        "adjunction solver, not a new geometry finding)")

    constant_phi_ok = (K_coeffs == [0] * len(K_coeffs))

    return {
        "B2": "P^2",
        "picard_basis": ["H"],
        "picard_gram": [[1]],
        "isotropic_class_existence": iso,
        "phi_existence_determination": "IMPOSSIBLE" if iso["only_zero_isotropic_vector"] else "UNRESOLVED",
        "phi_existence_reasoning": (
            "LOAD-BEARING ARGUMENT (Picard-lattice): Pic(P^2)=Z*H is rank-1 "
            "positive-definite (H^2=1>0); any nonzero class is n*H with "
            "(n*H)^2=n^2>0 for n!=0, so NO nonzero isotropic class exists. An "
            "algebraic fibration phi:P^2->(any curve C) requires a fiber class "
            "F with F^2=0 (distinct fibers are numerically disjoint) -- "
            "impossible here. This argument NEVER references the target curve "
            "C (only Pic(P^2) itself), hence it holds for a target of ANY "
            "genus, uniformly -- not because P^2 is simply connected (the "
            "usual genus>=1 argument), but because no candidate fiber class "
            "exists at all, which is a strictly stronger and genus-independent "
            "statement. INDEPENDENT CORROBORATION (Bezout, a second, distinct "
            "argument, not a restatement of the first): two curves of degree "
            "e in P^2 meet in e^2>0 points for e>=1, so no base-point-free "
            "pencil |O(e)| exists for e>=1; e=0 is the constant map. "
            "CONCLUSION: NO non-constant phi: P^2 -> (z-line) exists, for any "
            "target curve, of any genus -- the fiber-product construction of "
            "Route A's G1-a is inapplicable to B2=P^2 UNCONDITIONALLY, "
            "independent of the CY/twist condition, independent of ell, "
            "independent of the choice of z-line model."
        ),
        "K_B2": {"coeffs": K_coeffs, "expr": "-3H", "derivation": "adjunction on a line L=H, g(L)=0"},
        "cy_twist_condition_determination": "OBSTRUCTED (VACUOUS: no valid fiber class F exists to test K=-ell*F against)",
        "constant_phi_case": {
            "requires_K_B2_zero": True,
            "K_B2_is_zero": bool(constant_phi_ok),
            "determination": "ADMISSIBLE" if constant_phi_ok else "OBSTRUCTED",
            "reasoning": f"K_{{P^2}}=-3H has nonzero coefficient -3 -- constant phi also fails.",
        },
        "overall_determination": "OBSTRUCTED",
    }


# ----------------------------------------------------------------------------
# B2 = F_n (Hirzebruch surfaces, n>=0; n=0 is P^1xP^1)
# ----------------------------------------------------------------------------

def run_Fn(n):
    """n: sympy Symbol (nonneg, symbolic — general case) or a concrete
    nonnegative sympy Integer / python int."""
    label = f"F_{n}"
    Gram = sp.Matrix([[-n, 1], [1, 0]])  # Pic(F_n)=Z*s (+) Z*f, s^2=-n, f^2=0, s.f=1

    # fiber class F = f = (0,1) -- the standard ruling's fiber, verified isotropic
    F_vec = [0, 1]
    F_sq = pairing(Gram, F_vec, F_vec)
    chk(sp.simplify(F_sq) == 0, f"{label}: standard ruling fiber f is not isotropic (bug)")

    # DERIVE K_{F_n} via adjunction on the two spanning rational curves s,f.
    # Solved once symbolically (n_sym free) so the SAME derivation covers
    # both the fully-general case and every concrete instantiation below.
    n_sym = sp.Symbol("n")
    Gram_sym = sp.Matrix([[-n_sym, 1], [1, 0]])
    a0, a1 = sp.symbols("a0 a1")
    K_sym_vec = a0 * sp.Matrix([1, 0]) + a1 * sp.Matrix([0, 1])
    eqs = []
    for Cj, gj in ([[1, 0], 0], [[0, 1], 0]):
        Cj_m = sp.Matrix(Cj)
        Cj_sq = (Cj_m.T * Gram_sym * Cj_m)[0, 0]
        KdotCj = (K_sym_vec.T * Gram_sym * Cj_m)[0, 0]
        eqs.append(sp.Eq(KdotCj, -2 - Cj_sq))
    sol = sp.solve(eqs, [a0, a1], dict=True)
    chk(len(sol) == 1, f"{label}: adjunction system (symbolic n) not uniquely solvable: {sol}")
    a0_val = sp.simplify(sol[0][a0])
    a1_val = sp.simplify(sol[0][a1])
    chk(a0_val == -2, f"{label}: derived K s-coefficient {a0_val} != expected -2 (bug)")
    chk(sp.simplify(a1_val - (-(n_sym + 2))) == 0,
        f"{label}: derived K f-coefficient {a1_val} != expected -(n+2) (bug)")

    # instantiate at the requested n (symbolic-n path substitutes n_sym->n
    # which is a no-op when n IS n_sym itself; concrete-n path substitutes
    # a genuine integer)
    a0_n = a0_val
    a1_n = sp.simplify(a1_val.subs(n_sym, n))
    K_coeffs_n = [a0_n, a1_n]

    prop = solve_proportionality(Gram, K_coeffs_n, F_vec, label)

    K_sq_general = sp.simplify(((-2) * sp.Matrix([1, 0]) + (-(n + 2)) * sp.Matrix([0, 1])).T
                                * Gram * ((-2) * sp.Matrix([1, 0]) + (-(n + 2)) * sp.Matrix([0, 1])))[0, 0]
    K_sq_general = sp.simplify(K_sq_general)

    constant_phi_ok = (sp.simplify(a0_n) == 0 and sp.simplify(a1_n) == 0)

    return {
        "B2": f"F_{n}" + (" (= P^1 x P^1)" if str(n) == "0" else ""),
        "n": str(n),
        "picard_basis": ["s (section, s^2=-n)", "f (fiber, f^2=0)"],
        "picard_gram": [[str(-n), 1], [1, 0]],
        "fiber_class_F": {"coeffs": F_vec, "F_sq": int(F_sq) if F_sq == 0 else str(F_sq),
                           "source": "standard P^1-bundle ruling phi:F_n->P^1 -- the natural fibration "
                                     "the plan itself proposes for F_n; no claim of exhaustiveness "
                                     "over all possible fibrations is made (see not_claimed)"},
        "K_B2": {"coeffs": [str(a0_n), str(a1_n)], "expr": f"-2*s + ({a1_n})*f",
                 "derivation": "adjunction on the two spanning rational curves s (g=0,s^2=-n) and f (g=0,f^2=0); "
                               "linear system solved exactly, not assumed"},
        "K_sq": str(sp.simplify(K_sq_general)),
        "cy_twist_condition": prop,
        "cy_twist_condition_determination": prop["determination"],
        "constant_phi_case": {
            "requires_K_B2_zero": True,
            "K_B2_is_zero": bool(constant_phi_ok),
            "determination": "ADMISSIBLE" if constant_phi_ok else "OBSTRUCTED",
            "reasoning": f"K_{{F_{n}}} s-coefficient is -2 != 0 for every n -- constant phi also fails.",
        },
        "overall_determination": prop["determination"],
    }


# ----------------------------------------------------------------------------
# positive control: dP9 (degree-9 del Pezzo = P^2 blown up at 9 points)
# ----------------------------------------------------------------------------

def run_dP9_positive_control():
    label = "dP9"
    # Pic(dP9) = Z*H (+) Z*E1 (+) ... (+) Z*E9, Gram = diag(1,-1,...,-1)
    Gram = sp.diag(1, *([-1] * 9))
    K_vec = [-3] + [1] * 9  # K = -3H + E1+...+E9, standard blow-up formula [B: cited]
    K_sq = pairing(Gram, K_vec, K_vec)
    chk(K_sq == 0, f"{label}: sanity K^2 != 0 for dP9 (bug or wrong formula)")

    F_vec = [3] + [-1] * 9  # F = -K = 3H - E1-...-E9, classical anticanonical elliptic fibration [B]
    F_sq = pairing(Gram, F_vec, F_vec)
    chk(F_sq == 0, f"{label}: candidate fiber class F=-K is not isotropic -- classical fact "
        "would be contradicted; checker or Gram is wrong")

    prop = solve_proportionality(Gram, K_vec, F_vec, label)
    chk(prop["determination"] == "ADMISSIBLE",
        f"{label}: POSITIVE CONTROL FAILED -- expected ADMISSIBLE (classical rational elliptic "
        f"surface fact), got {prop}")
    chk(prop["ell"] == "1", f"{label}: expected ell=1 (rational elliptic surface, "
        f"chi_top=12 => Hodge-bundle degree 1), got ell={prop['ell']}")
    return {
        "B2": "dP9 (positive control, NOT part of the plan's B2 ladder)",
        "picard_basis": ["H", "E1..E9"],
        "picard_gram": "diag(1,-1,-1,-1,-1,-1,-1,-1,-1,-1)",
        "K_B2": {"coeffs": K_vec, "expr": "-3H+E1+...+E9",
                 "derivation": "[B: cited classical blow-up canonical-bundle formula K_Bl=pi*K+sum(Ei), "
                               "not re-derived by adjunction here -- this is the sanity input, not the "
                               "load-bearing new result]"},
        "fiber_class_F": {"coeffs": F_vec, "F_sq": int(F_sq),
                           "source": "[B: cited classical fact -- the anticanonical pencil |-K| gives "
                                     "the elliptic fibration on a (generic) rational elliptic surface]"},
        "cy_twist_condition": prop,
        "overall_determination": prop["determination"],
        "note": ("PROVES THIS CHECKER IS NOT A STUB: on a genuinely different input where the "
                 "classical answer is admissible, solve_proportionality() returns ADMISSIBLE and "
                 "SOLVES (does not assume) ell=1, matching the classical chi_top(dP9)/12=1 fact "
                 "for a generic rational elliptic surface."),
    }


# ----------------------------------------------------------------------------
# driver
# ----------------------------------------------------------------------------

def _certificate_common_footer():
    return {
        "checker": "check_G1a_CY_twist_condition.py",
        "checker_version": "1.0.0",
        "date": "2026-07-28",
        "tier": "E",
        "tier_reason": (
            "Every step is exact classical algebraic geometry (adjunction/genus-degree "
            "formula to derive K_B2, exact Picard-lattice linear algebra, Bezout/isotropy) "
            "computed with sympy Integer/Rational only -- no floats, no numerical tolerance. "
            "Unlike G0 (data/certificates/G0_NS_genus_cooper_s7.json), this derivation does "
            "NOT use the family's monodromy-derived transcendental lattice T or any Tier-B "
            "input -- the unknown Hodge-bundle degree ell of the cooper_s7 family over its "
            "modular curve cancels out of the argument entirely (the obstruction holds for "
            "every value of ell). This certificate is therefore Tier E in its own right, not "
            "inheriting a lower tier from an upstream Tier-B quantity."
        ),
        "not_claimed": [
            "does not compute ell (the cooper_s7 family's Hodge-bundle degree over X0(7)+/"
            "z-line) -- not needed for this result, and no orbifold Riemann-Hurwitz/Roch "
            "computation on X0(7)+ is attempted here",
            "does not address G1-b (degenerate-fiber crepant resolution) or G1-c "
            "(elliptic/F-theory posability) -- moot for a B2 that already fails G1-a",
            "does NOT claim K3-fibered Calabi-Yau fourfolds fail to exist over P^2 or F_n by "
            "ANY construction -- only the NAIVE fiber-product pullback of the FIXED cooper_s7 "
            "family along a FIXED moduli map phi:B2->(z-line) is shown obstructed; a more "
            "general Weierstrass-like twisted construction (the plan's own '-4K/-6K "
            "twisting' analogy, read as a free choice of twisted sections rather than a "
            "pullback of a fixed family) is NOT tested here and would need an explicit "
            "Weierstrass-type presentation of the M-polarized family directly on B2",
            "does not claim to have found the unique or exhaustive fibration structure on "
            "F_n for n>0 (only the standard/unique ruling is used, which is the natural "
            "candidate and the one the plan itself proposes)",
            "no observable of any kind (m_phi, alpha_D, Lambda_D) -- F5b stands",
            "no physical coupling of any kind (VISION sec 1.3)",
        ],
        "how": {
            "adjunction": "genus-degree formula 2g(C)-2=C^2+K.C, g=0 for all spanning curves "
                          "used (lines in P^2; section+fiber in F_n), solved as an exact "
                          "linear system in the unknown K-coefficients, sympy sp.solve",
            "proportionality_test": "K_B2=-ell*F solved component-wise exactly over Q "
                                    "(solve_proportionality()); K^2=0 kept as an independent "
                                    "ell-blind corollary cross-check",
            "isotropy_precondition": "F^2=0 checked exactly via the Gram pairing before any "
                                     "proportionality test is attempted -- a non-isotropic "
                                     "candidate F is rejected as a malformed input, not "
                                     "silently tested",
        },
    }


def emit_certificate_P2(result_p2, dp9_control, out_path):
    cert = {
        "certificate": "G1a_CY_condition_P2",
        "status": "DRAFT - pending T0 (Xavier) / verification-pass review. WP S2-G Phase G1-a "
                  "(briefs/WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md sec.1 & sec.5; phase opened "
                  "by T0 2026-07-28, briefs/T0_DECISIONS_2026_07_28_STREAM2.md item 2). "
                  "Producing tier does not self-promote to LIVE.",
        "operator": "cooper_s7 (Route A, B2=P^2 rung of the B2 ladder)",
        "claim": (
            "For B2=P^2, the naive fiber-product pullback X4=B2 x_{zline} Y of the certified "
            "cooper_s7 K3 family along any moduli map phi:P^2->(z-line) CANNOT be Calabi-Yau "
            "(c1(X4)!=0), for every choice of non-constant phi and every value of the family's "
            "(uncomputed) Hodge-bundle degree ell -- because Pic(P^2)=Z*H is rank-1 positive-"
            "definite and contains no nonzero isotropic class, so NO non-constant algebraic "
            "fibration phi:P^2->(curve) exists at all (the CY/twist condition is not merely "
            "failed, it is vacuous: there is no candidate fiber class to test it against). "
            "The constant-phi case (X4=B2 x K3) also fails, since K_{P^2}=-3H != 0."
        ),
        "cy_twist_condition": MATCH_CRITERION_TEXT,
        "match_determination": result_p2["overall_determination"],
        "derived": result_p2,
        "positive_control_dP9": dp9_control,
        **_certificate_common_footer(),
        "provenance": "Generated-by: Sonnet 5 (Stream 2, WP S2-G Phase G1-a session 2026-07-28) "
                      "| Verified-by: check_G1a_CY_twist_condition.py structural assertions + "
                      "checkers/test_G1a_CY_condition_controls.py | Reviewed-by: pending T0 "
                      "(Xavier) -- coordinator reviews and commits, no agent commits",
    }
    out_path.write_text(json.dumps(cert, indent=2, default=str))
    print(f"\nWrote {out_path.relative_to(REPO)}")


def emit_certificate_Fn(results_fn, result_fn_symbolic, dp9_control, out_path):
    cert = {
        "certificate": "G1a_CY_condition_Fn_ladder",
        "status": "DRAFT - pending T0 (Xavier) / verification-pass review. WP S2-G Phase G1-a "
                  "(briefs/WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md sec.1 & sec.5; phase opened "
                  "by T0 2026-07-28, briefs/T0_DECISIONS_2026_07_28_STREAM2.md item 2). "
                  "Producing tier does not self-promote to LIVE.",
        "operator": "cooper_s7 (Route A, F_n rung of the B2 ladder, n>=0; n=0 is P^1xP^1)",
        "claim": (
            "For EVERY Hirzebruch surface B2=F_n (n>=0, including P^1xP^1=F_0) with its "
            "standard ruling phi:F_n->P^1 (fiber class f), the naive fiber-product pullback "
            "X4=B2 x_{zline} Y of the certified cooper_s7 K3 family CANNOT be Calabi-Yau, for "
            "every value of the family's (uncomputed) Hodge-bundle degree ell -- because "
            "K_{F_n} = -2s - (n+2)f (derived here via adjunction, not assumed) has a nonzero "
            "s-coefficient (-2) for every n, so K_{F_n} is never proportional to the fiber "
            "class f: no ell solves K_{F_n} = -ell*f. Corollary (ell-blind) cross-check: "
            "K_{F_n}^2 = 8 != 0 for every n (Noether's formula K^2=12-e, e(F_n)=4). The "
            "constant-phi case also fails for every n (same nonzero s-coefficient)."
        ),
        "cy_twist_condition": MATCH_CRITERION_TEXT,
        "match_determination": "OBSTRUCTED (uniform in n, uniform in ell)",
        "derived": {
            "symbolic_n": result_fn_symbolic,
            "concrete_instances_n_0_to_5": results_fn,
        },
        "positive_control_dP9": dp9_control,
        **_certificate_common_footer(),
        "provenance": "Generated-by: Sonnet 5 (Stream 2, WP S2-G Phase G1-a session 2026-07-28) "
                      "| Verified-by: check_G1a_CY_twist_condition.py structural assertions + "
                      "checkers/test_G1a_CY_condition_controls.py | Reviewed-by: pending T0 "
                      "(Xavier) -- coordinator reviews and commits, no agent commits",
    }
    out_path.write_text(json.dumps(cert, indent=2, default=str))
    print(f"\nWrote {out_path.relative_to(REPO)}")


MATCH_CRITERION_TEXT = (
    "c1(X4)=0 for the naive fiber-product pullback X4=B2 x_{zline} Y is equivalent, on the "
    "base, to K_B2 = -ell*F where F is the fiber class of phi:B2->(z-line) and ell is the "
    "(fixed, family-determined) degree of the Hodge/relative-dualizing line bundle of Y over "
    "its modular curve; F must be isotropic (F^2=0) to be a genuine fibration fiber class."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-cert", action="store_true")
    ap.add_argument("--out-p2", default=str(REPO / "data" / "certificates" / "G1a_CY_condition_P2.json"))
    ap.add_argument("--out-fn", default=str(REPO / "data" / "certificates" / "G1a_CY_condition_Fn_ladder.json"))
    args = ap.parse_args()

    try:
        print("=== G1-a: CY/twist condition, B2 ladder ===\n")

        result_p2 = run_P2()
        print(f"[P^2] phi existence: {result_p2['phi_existence_determination']}")
        print(f"[P^2] overall determination: {result_p2['overall_determination']}\n")

        n_sym = sp.Symbol("n", integer=True, nonnegative=True)
        result_fn_symbolic = run_Fn(n_sym)
        print(f"[F_n, symbolic n] K_B2 = {result_fn_symbolic['K_B2']['expr']}")
        print(f"[F_n, symbolic n] K^2 = {result_fn_symbolic['K_sq']}")
        print(f"[F_n, symbolic n] overall determination: {result_fn_symbolic['overall_determination']}\n")

        results_fn = []
        for n_val in range(6):
            r = run_Fn(sp.Integer(n_val))
            results_fn.append(r)
            print(f"[F_{n_val}] K_B2 = {r['K_B2']['expr']}, K^2={r['K_sq']}, "
                  f"determination={r['overall_determination']}")
            chk(r["overall_determination"] == "OBSTRUCTED",
                f"F_{n_val}: expected OBSTRUCTED, got {r['overall_determination']}")

        print()
        dp9_control = run_dP9_positive_control()
        print(f"[dP9 positive control] determination: {dp9_control['overall_determination']}, "
              f"ell={dp9_control['cy_twist_condition']['ell']}")

        chk(result_p2["overall_determination"] == "OBSTRUCTED", "P^2 unexpectedly not OBSTRUCTED")
        chk(result_fn_symbolic["overall_determination"] == "OBSTRUCTED", "F_n (symbolic) unexpectedly not OBSTRUCTED")
        chk(dp9_control["overall_determination"] == "ADMISSIBLE", "dP9 positive control unexpectedly not ADMISSIBLE")

        if args.emit_cert:
            emit_certificate_P2(result_p2, dp9_control, Path(args.out_p2))
            emit_certificate_Fn(results_fn, result_fn_symbolic, dp9_control, Path(args.out_fn))

        print("\n=== SUMMARY ===")
        print("B2 = P^2:            OBSTRUCTED (no non-constant phi exists at all)")
        print("B2 = F_n (all n>=0): OBSTRUCTED (K_B2 never proportional to fiber class)")
        print("Positive control dP9: ADMISSIBLE, ell=1 (checker is not a stub)")
        print("\ncheck_G1a_CY_twist_condition.py: all structural assertions passed")
        return 0
    except ControlFailure as e:
        print(f"\nFAIL / PRECONDITION VIOLATION: {e}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
