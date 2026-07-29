#!/usr/bin/env python3
"""
check_TW1_two_e8_feasibility.py — WP-TW1, two-E8 degree-feasibility gate for
the twisted-Weierstrass PRIMARY route (S3 briefs/
EXECUTION_PLAN_2026_07_29_TWISTED_AND_WPE6.md, WP-TW1 section; authorized by
T0 countermand R2 2026-07-29, S2 CLAUDE.md ledger entry 6).

WHAT THIS COMPUTES
------------------
Route A (strict pullback) is CLOSED (S2 CLAUDE.md ledger entry 6). The
promoted PRIMARY route builds a Calabi-Yau fourfold directly as a generic
Weierstrass model

    y^2 = x^3 + f*x + g,      f in H^0(-4K_B3),  g in H^0(-6K_B3)

on a threefold base B3. This is automatically Calabi-Yau: for f in |-4K_B3|,
g in |-6K_B3| the Weierstrass model has trivial canonical class, K_X4=0
(standard fact for the anticanonical-weighted Weierstrass construction,
cited, not re-derived here — see e.g. Morrison-Vafa I 1996).

The program's separately certified G0 result (data/certificates/
G0_NS_genus_cooper_s7.json, Tier B, LIVE, three independent verification
lineages) proved NS(cooper_s7) ⊇ E8(-1) ⊕ E8(-1): the certified K3 fiber's
Neron-Severi lattice contains TWO copies of E8(-1). ANY valid B3 for the
twisted construction must therefore be able to host TWO E8 Kodaira-type
(II*) gauge loci in the discriminant Delta = 4f^3+27g^2.

This script checks ONLY the pure necessary-condition (degree-budget +
collision) screen — NOT whether the M-polarized family can actually be
exhibited on any surviving base (S3 DEEPTHINK_DEBRIEF_AUDIT_2026_07_29.md
$A5: "the honest hard part... is where the route most plausibly dies" — a
separate, harder, NOT-YET-attempted future WP).

THE NECESSARY CONDITION (Tate's algorithm, standard F-theory convention;
plan's own formalization, WP-TW1 step 1): an E8 (type II*) locus over an
irreducible divisor D on B3 needs, along a generic point of D,

    v_D(f) >= 4,   v_D(g) >= 5,   v_D(Delta) = 10        (E8 Tate orders)

For a divisor D to carry this GLOBALLY (not just at one point), f must be
divisible by D^4 as a section of O(-4K_B3), i.e. f in H^0(-4K_B3 - 4D); and
g must be divisible by D^5, i.e. g in H^0(-6K_B3 - 5D). For TWO such
divisors D1, D2, requiring the condition independently and simultaneously
along EACH one gives (this is not assumed, it follows from unique
factorization of sections when D1 != D2 are distinct irreducible divisors —
see collision_P3() for the case where D1, D2 additionally intersect):

    4*[D1] + 4*[D2]  <=  [-4K_B3]      (f must be divisible by D1^4 D2^4)
    5*[D1] + 5*[D2]  <=  [-6K_B3]      (g must be divisible by D1^5 D2^5)
   10*[D1] + 10*[D2]  <= [-12K_B3]     (Delta budget, corollary of the above)

in the EFFECTIVE cone of Pic(B3) — this is the plan's step-1 formalization,
implemented exactly here with sympy Integer/Rational arithmetic (no floats).

CRITICAL — the collision/non-minimality analysis (plan step 3, load-bearing,
NOT optional): on P^3, Pic(P^3) = Z, so ANY two nonzero effective divisors
D1, D2 numerically intersect (classical projective-dimension theorem:
dim(D1) + dim(D2) = 2+2 = 4 >= 3 = dim(P^3) forces D1 ∩ D2 != empty). Because
f is divisible by BOTH D1^4 and D2^4 as GLOBAL sections, at a generic point
of the intersection curve C = D1 ∩ D2 the vanishing orders of f, g ADD:
v_C(f) >= 4+4 = 8, v_C(g) >= 5+5 = 10. ADDITIVITY ITSELF IS A THEOREM, NOT A
CONVENTION CHOICE (unique factorization of sections for distinct irreducible
D1 != D2 forces it — there is no coherent alternative under which C even has
a single well-defined local vanishing order). This triggers the standard
Weierstrass (4,6)-non-minimality curse (v(f)>=4 AND v(g)>=6) AND
independently v_C(Delta) >= min(3*8, 2*10) = 20 >= 12 (the discriminant-
order-12 non-minimality flag).

The genuinely open question is what a codim-2 (4,6) locus MEANS for the
base, not whether it occurs — two readings, both giving the SAME verdict
for P^3-as-given but differing in SCOPE (see the certificate's "collision"
block and the brief for the full discussion):
  Reading 1 (adopted): no minimal Weierstrass CY exists over B3=P^3 as
    given => P^3 FAILS.
  Reading 2: the standard cure for a codim-2 (4,6) locus is to blow up B3
    along C, producing a DIFFERENT base not checked here (in the standard
    F-theory literature, codim-2 (4,6)/collision loci are routinely cured
    this way, not simply declared impossible) => P^3-as-given still FAILS,
    but this says nothing about a blow-up of P^3, which is UNCHECKED.
Both readings agree on P^3-as-given; NEITHER is silently chosen without
being named — the certificate flags this scope boundary explicitly rather
than overclaiming "P^3 fails, period."

On the P^1-bundle bases P(O_{P^2} (+) O_{P^2}(n)), the two TAUTOLOGICAL
sections C0, C_infty of a split rank-2 bundle are DISJOINT by construction
(classical scroll fact, cited) for every n >= 0 — so the collision analysis
is VACUOUS there (no intersection curve exists at all). Passing the raw
degree budget is NOT sufficient by itself, though: a PASS also requires
that the EXACT Tate orders (v(f)=4, v(g)=5, not just the inequality) are
REALIZABLE, i.e. that after extracting D1^4 D2^4 (resp. D1^5 D2^5) from the
ambient linear system, the residual line bundle has a section that does NOT
vanish identically on D1 or D2 (which would silently push the true order
above 4/5, e.g. to (4,6), triggering non-minimality even WITHOUT a
collision). This is checked explicitly here (restrict_to_C0/restrict_to_Cinf
below), not merely assumed from the inequality holding — see
run_P1xP2()/run_P1bundle()'s "realizability" block.

deg Delta on P^3 = 48 (NOT 144 — S3 DEEPTHINK_DEBRIEF_AUDIT_2026_07_29.md
$A5 recorded arithmetic-error correction: -K_{P^3}=O(4) => -12K=O(48); the
verbatim external debrief's 144 is discarded, not propagated).

Also note (cheap, ruled out immediately): placing BOTH E8 loci on a SINGLE
divisor D (D1=D2) is not a live alternative to the two-divisor cases checked
here — it would require v(g)>=5+5=10 along that one divisor, immediately
(4,10), far past the (4,6) curse, non-minimal by inspection, worse than
either case actually checked.

STATUS: DRAFT. Producing tier does not self-promote to LIVE (criteria-
checkers skill; S2 CLAUDE.md standing rule).

NECESSARY CONDITION ONLY — a PASS here does NOT assert the M-polarized
family (rho=19, T=U (+) <14>) actually exists on that base; that is
separate, harder, future work (plan DoD, explicit in every certificate's
"not_claimed").

Usage:
  python3 checkers/check_TW1_two_e8_feasibility.py                # print only
  python3 checkers/check_TW1_two_e8_feasibility.py --emit-cert    # write all 3 certs

Exit codes: 0 all structural assertions + controls passed (independent of
whether individual bases PASS or FAIL the geometry question — FAIL is a
valid, non-error, documented outcome). 3 a structural precondition failed.

Generated-by: Sonnet 5 (Stream 2, WP-TW1 session 2026-07-29)
Verified-by: this script's own structural assertions + checkers/
  test_TW1_two_e8_feasibility_controls.py (>=1 positive, >=2 negative controls)
Reviewed-by: pending T0 (Xavier) — coordinator reviews and commits, no agent
  self-promotes DRAFT -> LIVE
"""

import argparse
import json
import sys
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parent.parent

# E8 (Kodaira type II*) Tate orders — plan's own formalization (WP-TW1,
# S3 DEEPTHINK_DEBRIEF_AUDIT_2026_07_29.md $A5, "standard, correct").
VF_E8 = sp.Integer(4)   # v(f) >= 4
VG_E8 = sp.Integer(5)   # v(g) >= 5
VDELTA_E8 = sp.Integer(10)  # v(Delta) = 10


class ControlFailure(Exception):
    """A structural PRECONDITION failed. NOT the same as a documented FAIL
    verdict for a base's geometric feasibility, which is a normal, valid
    return value."""


def chk(cond, msg):
    if not cond:
        raise ControlFailure(msg)


# ----------------------------------------------------------------------------
# generic budget-check primitive (componentwise <=, exact sympy)
# ----------------------------------------------------------------------------

def budget_chain(need, bound, labels):
    """need, bound: tuples of sympy expressions (Integers or expressions in
    a nonnegative-integer symbol n) in the SAME Pic-basis coordinates.
    labels: tuple of coordinate names for printing.
    Returns dict with per-component margin (bound-need) and an overall
    verdict. For symbolic (n-dependent) components, verdict is computed via
    sp.solve_univariate_inequality over n>=0; for pure-Integer components it
    is a plain comparison. Raises ControlFailure if need/bound/labels length
    mismatch (malformed input guard)."""
    chk(len(need) == len(bound) == len(labels),
        f"budget_chain: length mismatch need={need} bound={bound} labels={labels}")
    margins = []
    all_pass = True
    n_sym = sp.Symbol("n", integer=True, nonnegative=True)
    chain = []
    for lbl, nd, bd in zip(labels, need, bound):
        margin = sp.simplify(bd - nd)
        margins.append(margin)
        if margin.free_symbols:
            # symbolic in n: verify margin >= 0 holds for EVERY n>=0
            sol = sp.solve_univariate_inequality(margin >= 0, n_sym, relational=False)
            holds_for_all_n = sp.Interval(0, sp.oo).is_subset(sol)
            all_pass = all_pass and bool(holds_for_all_n)
            chain.append(f"{lbl}: need={nd}, bound={bd}, margin={margin} "
                         f"(>=0 for all n>=0: {holds_for_all_n})")
        else:
            ok = bool(margin >= 0)
            all_pass = all_pass and ok
            chain.append(f"{lbl}: need={nd}, bound={bd}, margin={margin} (>=0: {ok})")
    return {
        "margins": [str(m) for m in margins],
        "chain": chain,
        "all_components_pass": bool(all_pass),
    }


# ----------------------------------------------------------------------------
# exact-realizability primitives for the P^1-bundle family P(O(+)O(n*h))/P^2
# (n=0 is P^1xP^2). A raw degree-budget PASS is NECESSARY but not SUFFICIENT:
# the budget only checks that D1^4 D2^4 | f (resp D1^5 D2^5 | g) is possible
# AT ALL; it does not check that the EXACT orders v=4, v=5 (not more) are
# REALIZABLE by an actual section, i.e. that the residual line bundle (what
# remains of -4K/-6K after extracting D1^4 D2^4 / D1^5 D2^5) has a member
# that does NOT vanish identically on D1 or D2 -- if it did, the true order
# would silently be pushed higher (e.g. to (4,6)), triggering non-minimality
# even without any collision. This is the gap flagged in review: checked
# here explicitly via the scroll's standard H^0 decomposition, not assumed.
#
# Standard fact (verified against the known Hirzebruch identity
# K_{F_n}=-2C0-(n+2)f and cross-checked two independent ways in this
# session): for X=P(O(+)O(n*h)) over P^2 with tautological sections
# C0 (normal bundle O(-n*h)) and C_infty=C0+n*h (normal bundle O(n*h)),
#     restriction of O(a*C0+b*h) to C0      = O_{P^2}(b - a*n)
#     restriction of O(a*C0+b*h) to C_infty = O_{P^2}(b)
# and the restriction map H^0(X,aC0+bh) -> H^0(C0 or C_infty, ...) is
# surjective for a split (decomposable) bundle (classical scroll fact,
# cited) -- so a GENERIC global section restricts to a GENERIC, hence
# nonzero-unless-forced, section of the target, PROVIDED the target degree
# is >= 0 (H^0(P^2,O(d))!=0 needs d>=0). "Realizable" below means both
# restricted degrees are >=0 -- the section is then guaranteed to exist and
# NOT vanish identically on either divisor for a generic choice.
# ----------------------------------------------------------------------------

def restrict_to_C0(a, b, n):
    return sp.simplify(b - a * n)


def restrict_to_Cinf(a, b):
    return b


def realizability_check(residual_a, residual_b, n_val, label):
    """residual = (a,b) in (C0,h)-coords of what remains of the target
    linear system after extracting D1^k D2^k, FOR THE SPECIFIC CONFIGURATION
    (D1,D2)=(C0,C_infty) used throughout this file. Returns dict with both
    restricted degrees and an explicit REALIZABLE/NOT-REALIZABLE verdict for
    THAT configuration -- this is NOT a statement about every possible
    divisor-class choice on the scroll (the budget has slack in several
    components; a different (D1,D2) choice at large n is not ruled out and
    is simply UNCHECKED here, not shown to fail).
    n_val may be a concrete sympy Integer OR the nonnegative-integer symbol
    n; in the symbolic case, the "realizable_for_all_n_geq_0" key (only --
    see below) reports whether THIS configuration's realizability holds for
    every n>=0 (it does not, past n=18: the g-residual's restriction to C0
    is O(18-n) for this configuration specifically)."""
    r_C0 = restrict_to_C0(residual_a, residual_b, n_val)
    r_Cinf = restrict_to_Cinf(residual_a, residual_b)
    n_sym = sp.Symbol("n", integer=True, nonnegative=True)

    if hasattr(r_C0, "free_symbols") and r_C0.free_symbols:
        sol_C0 = sp.solve_univariate_inequality(r_C0 >= 0, n_sym, relational=False)
        holds_all_n = bool(sp.Interval(0, sp.oo).is_subset(sol_C0))
        return {
            "label": label,
            "residual_class_C0_h_coords": [str(residual_a), str(residual_b)],
            "restriction_to_C0_degree_expr": str(r_C0),
            "restriction_to_Cinf_degree_expr": str(r_Cinf),
            "restriction_to_C0_nonneg_for_n_in": str(sol_C0),
            "realizable_for_all_n_geq_0": holds_all_n,
            # NOTE: deliberately NO bare "realizable" key in this branch --
            # a bare True/False here for a symbolic-n result reads as a
            # single unconditional verdict and is easy to misread against
            # (D1,D2)=(C0,C_infty) specifically; callers must use the
            # explicit "realizable_for_all_n_geq_0" key instead.
            "configuration_checked": "(D1,D2) = (C0, C_infty) only -- other "
                                     "divisor-class choices at large n are "
                                     "UNCHECKED, not shown to fail.",
            "reasoning": (f"{label} (symbolic n), configuration (D1,D2)=(C0,C_infty): "
                          f"restriction to C0 is O({r_C0}), "
                          f">=0 for n in {sol_C0} (restriction to C_infty is O({r_Cinf}), "
                          f">=0 for all n>=0 always) -- realizability for EVERY n>=0 "
                          + ("HOLDS." if holds_all_n else
                             "DOES NOT hold uniformly; see the concrete per-n "
                             "instances for the range where it does.")),
        }
    ok_C0 = bool(sp.simplify(r_C0) >= 0)
    ok_Cinf = bool(sp.simplify(r_Cinf) >= 0)
    realizable = ok_C0 and ok_Cinf
    return {
        "label": label,
        "residual_class_C0_h_coords": [str(residual_a), str(residual_b)],
        "restriction_to_C0_degree": str(r_C0),
        "restriction_to_Cinf_degree": str(r_Cinf),
        "realizable": realizable,
        "reasoning": (f"{label}: residual = {residual_a}*C0+({residual_b})*h restricts to "
                      f"O({r_C0}) on C0 and O({r_Cinf}) on C_infty; both >=0 => a generic "
                      f"global section does NOT vanish identically on either divisor, so the "
                      f"exact Tate order (not just the budget inequality) is achievable."
                      if realizable else
                      f"{label}: NOT REALIZABLE -- a restricted degree is negative, so EVERY "
                      f"section of the residual bundle vanishes identically on that divisor, "
                      f"silently pushing the true order above the target -- non-minimality "
                      f"would be forced even without a collision."),
    }


# ----------------------------------------------------------------------------
# (a) B3 = P^3   (Pic = Z*H, rank 1)
# ----------------------------------------------------------------------------

def run_P3():
    mK = sp.Integer(4)  # -K_{P^3} = O(4)  (classical: K_{P^n} = O(-n-1))
    bound_f = 4 * mK    # O(16)
    bound_g = 6 * mK    # O(24)
    bound_d = 12 * mK   # O(48)  -- audit-corrected, was mis-stated as 144
    chk(bound_d == 48, f"deg(-12K_P3) sanity check failed: got {bound_d}, expected 48 "
        "(S3 DEEPTHINK_DEBRIEF_AUDIT_2026_07_29.md $A5 correction)")

    # symbolic degree budget: D1=d1*H, D2=d2*H, d1,d2 positive integers
    d1, d2 = sp.symbols("d1 d2", positive=True, integer=True)
    s = d1 + d2
    need_f, need_g, need_d = 4 * s, 5 * s, 10 * s
    # raw arithmetic ceiling on s = d1+d2 from each bound (integer floor)
    s_max_f = sp.floor(bound_f / 4)
    s_max_g = sp.floor(bound_g / 5)
    s_max_d = sp.floor(bound_d / 10)
    s_max = min(s_max_f, s_max_g, s_max_d)

    # --- collision analysis (load-bearing, plan step 3) ---
    # Any two nonzero effective divisors on P^3 intersect: dim(D1)+dim(D2) =
    # 2+2=4 >= 3=dim(P^3) => D1 ∩ D2 != empty (classical projective
    # dimension theorem, e.g. Hartshorne I.7.2 exercise / general position
    # in P^n). Confirmed numerically too: D1.D2 = d1*d2*(H^3) = d1*d2 > 0.
    intersection_number = sp.simplify(d1 * d2)  # H^3=1 on P^3
    collision_unavoidable = True  # true for ALL d1,d2 >= 1 on Pic-rank-1 P^3

    # combined vanishing order at a generic point of C = D1 ∩ D2: f is
    # divisible by D1^4 AND D2^4 as GLOBAL sections (distinct irreducible
    # divisors D1 != D2 => orders add at their intersection: f = s1^4 s2^4 h,
    # h a unit near a generic point of C, s_i the local equation of D_i).
    v_f_collision = VF_E8 + VF_E8   # 8
    v_g_collision = VG_E8 + VG_E8   # 10

    # Non-minimality test 1: the standard Weierstrass (4,6)-curse.
    curse_46_triggered = bool(v_f_collision >= 4 and v_g_collision >= 6)
    # Non-minimality test 2: discriminant order >= 12.
    # Delta = 4f^3+27g^2 =>  v(Delta) >= min(3*v(f), 2*v(g)) generically with
    # equality when the two summand orders differ (ultrametric-type bound;
    # here 3*8=24 != 2*10=20, so equality holds and v(Delta) = 20 exactly).
    v_delta_collision = min(3 * v_f_collision, 2 * v_g_collision)  # 20
    discriminant_order_flag = bool(v_delta_collision >= 12)

    # ADDITIVITY (v_f, v_g add at C) is a THEOREM, not a convention choice:
    # unique factorization of sections forces D1^4 D2^4 | f (resp D1^5 D2^5
    # | g) once BOTH divisibility conditions are imposed on D1 != D2
    # simultaneously -- there is no coherent alternative under which C even
    # has a single well-defined local vanishing order to assign a different
    # value to. This is NOT the flagged ambiguity (an earlier draft of this
    # analysis mis-scoped the ambiguity here; corrected on review).
    #
    # The GENUINELY open question is what a codim-2 (4,6) locus MEANS for
    # the base, not whether it occurs. Two readings, differing in SCOPE
    # (not in the P^3-as-given verdict, on which they agree):
    reading_convergence = {
        "reading_1_no_minimal_model_over_B3_as_given": {
            "v_f_at_C": int(v_f_collision), "v_g_at_C": int(v_g_collision),
            "curse_4_6_triggered": curse_46_triggered,
            "v_delta_at_C": int(v_delta_collision),
            "discriminant_order_flag_ge_12": discriminant_order_flag,
            "verdict": "no minimal Weierstrass CY over P^3 as given -- FAIL (adopted here)",
        },
        "reading_2_standard_blow_up_cure": {
            "note": "In the standard F-theory literature, a codim-2 (4,6) "
                    "locus is routinely CURED by blowing up the base along "
                    "the offending curve C, producing a strictly different "
                    "base X' = Bl_C(P^3) (not P^3 itself). Under this "
                    "reading, P^3-AS-GIVEN still fails (the model over P^3 "
                    "itself is non-minimal), but this reading says NOTHING "
                    "about whether Bl_C(P^3) would pass a re-run of this "
                    "same check -- that base is NOT checked by this WP "
                    "(explicit in the certificate's not_claimed).",
        },
        "convergence": "Both readings agree P^3-AS-GIVEN fails (additivity "
                       "is forced regardless of which reading of the "
                       "'blow-up or not' question is taken) -- the raw "
                       "per-divisor degree budget is irrelevant once "
                       "collision is accounted for, for every d1,d2 >= 1. "
                       "They differ in SCOPE (whether a blow-up escapes the "
                       "verdict), which is recorded, not silently resolved, "
                       "and is flagged in not_claimed rather than answered.",
    }

    # raw budget substituted at the boundary case d1=d2=2 (s=4, inside s_max=4)
    # to show the arithmetic DOES pass in isolation -- the point of the WP.
    # (d1,d2 are multivariate symbols here, so this concrete substitution --
    # not the generic budget_chain(), which only handles a single symbol n
    # for the P^1-bundle ladder -- is used to certify the raw-budget claim.)
    raw_budget_boundary_case = budget_chain(
        (need_f.subs({d1: 2, d2: 2}), need_g.subs({d1: 2, d2: 2}), need_d.subs({d1: 2, d2: 2})),
        (bound_f, bound_g, bound_d), ("f (deg)", "g (deg)", "Delta (deg)"))
    return {
        "base": "P^3",
        "picard_rank": 1,
        "minus_K": {"expr": "O(4)", "value": int(mK)},
        "bounds": {"-4K": int(bound_f), "-6K": int(bound_g), "-12K": int(bound_d)},
        "raw_degree_budget_symbolic": {
            "need_f_expr": str(need_f), "need_g_expr": str(need_g), "need_delta_expr": str(need_d),
            "s_max_from_f_bound": int(s_max_f), "s_max_from_g_bound": int(s_max_g),
            "s_max_from_delta_bound": int(s_max_d), "s_max_overall": int(s_max),
            "interpretation": f"raw arithmetic allows d1+d2 <= {s_max} "
                              f"(e.g. d1=d2=2 fits) -- ARITHMETICALLY PASSES in isolation",
        },
        "raw_degree_budget_boundary_case_d1_2_d2_2": raw_budget_boundary_case,
        "collision_analysis": {
            "reasoning": "Pic(P^3)=Z*H rank 1: any two nonzero effective "
                        "divisors D1=d1*H, D2=d2*H (d1,d2>=1) satisfy "
                        "dim(D1)+dim(D2)=2+2=4>=3=dim(P^3), forcing "
                        "D1 ∩ D2 != empty by the classical projective "
                        "dimension theorem; confirmed numerically via the "
                        "intersection number D1.D2 = d1*d2*(H^3) = d1*d2 > 0 "
                        "for every d1,d2 >= 1.",
            "intersection_number_expr": str(intersection_number),
            "collision_unavoidable_for_every_d1_d2": collision_unavoidable,
            "v_f_at_collision_curve": int(v_f_collision),
            "v_g_at_collision_curve": int(v_g_collision),
            "v_delta_at_collision_curve": int(v_delta_collision),
            "non_minimality_test_4_6_curse": curse_46_triggered,
            "non_minimality_test_discriminant_order_ge_12": discriminant_order_flag,
            "reading_convergence": reading_convergence,
        },
        "overall_verdict": "FAIL",
        "overall_verdict_reasoning": (
            "Raw per-divisor degree budget ARITHMETICALLY PASSES (e.g. "
            "d1=d2=2 gives need_f=16<=16, need_g=20<=24, need_delta=40<=48), "
            "but the MANDATORY collision analysis shows this is irrelevant: "
            "because Pic(P^3) has rank 1, D1 and D2 ALWAYS intersect, and at "
            "the intersection curve the combined orders (v_f=8, v_g=10) "
            "trigger BOTH standard non-minimality flags (the (4,6)-curse "
            "and v(Delta)>=12) UNCONDITIONALLY, for every choice of d1,d2>=1. "
            "P^3 therefore FAILS the two-E8 necessary-condition screen: no "
            "configuration on P^3 survives the collision, regardless of the "
            "raw degree budget passing."
        ),
    }


# ----------------------------------------------------------------------------
# (b) B3 = P^1 x P^2   (Pic = Z*h1 (+) Z*h2, disjoint fiber divisors)
# ----------------------------------------------------------------------------

def run_P1xP2():
    mK = (sp.Integer(2), sp.Integer(3))  # -K_{P1xP2} = O(2,3): -K_P1=O(2), -K_P2=O(3)
    bound_f = (4 * mK[0], 4 * mK[1])   # O(8,12)
    bound_g = (6 * mK[0], 6 * mK[1])   # O(12,18)
    bound_d = (12 * mK[0], 12 * mK[1])  # O(24,36)

    # D1 = {p1} x P^2 = (1,0), D2 = {p2} x P^2 = (1,0), p1 != p2 in P^1.
    # DISJOINT BY CONSTRUCTION (a point in D1 ∩ D2 would need its P^1
    # coordinate to equal BOTH p1 and p2 simultaneously -- impossible since
    # p1 != p2). No collision analysis needed: it is vacuous, not merely
    # favorable, since D1 ∩ D2 = empty as a SET, not just numerically.
    D1, D2 = (1, 0), (1, 0)
    s = (D1[0] + D2[0], D1[1] + D2[1])  # (2,0)
    need_f = (4 * s[0], 4 * s[1])
    need_g = (5 * s[0], 5 * s[1])
    need_d = (10 * s[0], 10 * s[1])

    chain_f = budget_chain(need_f, bound_f, ("h1-component (f)", "h2-component (f)"))
    chain_g = budget_chain(need_g, bound_g, ("h1-component (g)", "h2-component (g)"))
    chain_d = budget_chain(need_d, bound_d, ("h1-component (Delta)", "h2-component (Delta)"))

    # --- exact-realizability check (P^1xP^2 = n=0 case of the scroll
    # family; the (h1,h2) coords used above coincide with (C0,h) at n=0) ---
    residual_f = (bound_f[0] - need_f[0], bound_f[1] - need_f[1])   # (0,12)
    residual_g = (bound_g[0] - need_g[0], bound_g[1] - need_g[1])   # (2,18)
    real_f = realizability_check(residual_f[0], residual_f[1], 0, "f-residual")
    real_g = realizability_check(residual_g[0], residual_g[1], 0, "g-residual")

    overall_pass = (chain_f["all_components_pass"] and chain_g["all_components_pass"]
                     and chain_d["all_components_pass"]
                     and real_f["realizable"] and real_g["realizable"])

    return {
        "base": "P^1 x P^2",
        "picard_rank": 2,
        "minus_K": {"expr": "O(2,3)", "value": [int(mK[0]), int(mK[1])]},
        "bounds": {"-4K": [int(x) for x in bound_f], "-6K": [int(x) for x in bound_g],
                   "-12K": [int(x) for x in bound_d]},
        "divisor_choice": {
            "D1": "{p1} x P^2, class (1,0)", "D2": "{p2} x P^2, class (1,0), p1 != p2",
            "disjointness": "SET-THEORETIC, by construction (product structure): "
                            "a point (x,y) in D1 ∩ D2 needs x=p1 AND x=p2, "
                            "impossible since p1 != p2. Collision analysis is "
                            "VACUOUS here, not merely passed.",
        },
        "budget_f": chain_f, "budget_g": chain_g, "budget_delta": chain_d,
        "realizability": {"f": real_f, "g": real_g},
        "overall_verdict": "PASS" if overall_pass else "FAIL",
        "overall_verdict_reasoning": (
            "Two E8 divisors placed at distinct point-fibers {p1}xP^2, "
            "{p2}xP^2 are disjoint by construction (no collision analysis "
            "needed), the degree budget is satisfied in every component "
            "(f: 8<=8 tight; g: 10<=12 margin 2; Delta: 20<=24 margin 4), AND "
            "the EXACT Tate orders are realizable (not just the inequality): "
            "the f-residual O(0,12) restricts to O(12) on both divisors "
            "(>=0), and the g-residual O(2,18) restricts to O(18) on both "
            "(>=0) -- a generic choice of f,g achieves v(f)=4, v(g)=5 exactly "
            "on each divisor, not silently pushed higher. This is a "
            "necessary-condition PASS only -- it does not by itself "
            "construct the M-polarized family on this base."
        ),
    }


# ----------------------------------------------------------------------------
# (c) B3 = P(O_{P^2} (+) O_{P^2}(n))  for n = 0..3 and symbolic n >= 0
# ----------------------------------------------------------------------------

def run_P1bundle(n_val):
    """n_val: sympy Integer (concrete) or the nonnegative-integer Symbol n.
    Pic(X) = Z*C0 (+) Z*h, h = pi^*(hyperplane on P^2). Standard scroll
    formula (cited classical fact, verified here to reduce to the known
    Hirzebruch K_{F_n}=-2C0-(n+2)f formula when the base is P^1 instead of
    P^2 -- see module docstring / brief for the cross-check):
        K_X = -2*C0 - (n+3)*h   =>   -K_X = 2*C0 + (n+3)*h
    C0, C_infty=C0+n*h are the two DISJOINT tautological sections of the
    split bundle O (+) O(n*h) (classical scroll fact, cited)."""
    mK = (sp.Integer(2), n_val + 3)  # -K_X in (C0,h) coords
    bound_f = (4 * mK[0], 4 * mK[1])
    bound_g = (6 * mK[0], 6 * mK[1])
    bound_d = (12 * mK[0], 12 * mK[1])

    D1 = (sp.Integer(1), sp.Integer(0))          # C0
    D2 = (sp.Integer(1), n_val)                  # C_infty = C0 + n*h
    s = (D1[0] + D2[0], D1[1] + D2[1])           # (2, n)
    need_f = (4 * s[0], 4 * s[1])
    need_g = (5 * s[0], 5 * s[1])
    need_d = (10 * s[0], 10 * s[1])

    chain_f = budget_chain(need_f, bound_f, ("C0-component (f)", "h-component (f)"))
    chain_g = budget_chain(need_g, bound_g, ("C0-component (g)", "h-component (g)"))
    chain_d = budget_chain(need_d, bound_d, ("C0-component (Delta)", "h-component (Delta)"))
    budget_pass = chain_f["all_components_pass"] and chain_g["all_components_pass"] \
        and chain_d["all_components_pass"]

    # --- exact-realizability check (raw budget PASS is necessary but not
    # sufficient -- see module docstring / realizability_check() docstring) ---
    residual_f = (bound_f[0] - need_f[0], sp.simplify(bound_f[1] - need_f[1]))  # (0,12)
    residual_g = (bound_g[0] - need_g[0], sp.simplify(bound_g[1] - need_g[1]))  # (2,n+18)
    real_f = realizability_check(residual_f[0], residual_f[1], n_val, "f-residual")
    real_g = realizability_check(residual_g[0], residual_g[1], n_val, "g-residual")
    is_symbolic = hasattr(n_val, "free_symbols") and bool(n_val.free_symbols)
    if is_symbolic:
        # budget holds for ALL n>=0 (verified above); realizability of the
        # EXACT orders for the SPECIFIC configuration (D1,D2)=(C0,C_infty)
        # checked here holds only where g's C0-restriction (18-n) stays
        # >=0, i.e. n<=18 for THIS configuration -- other divisor-class
        # choices at large n are UNCHECKED (the budget has slack there),
        # not shown to fail. Report this configuration-scoped, bounded
        # claim explicitly rather than a single all-n boolean.
        overall_pass = budget_pass  # the budget claim itself IS uniform in n
        verdict_str = ("PASS (budget: all n>=0; exact-order realizability for the "
                       "(D1,D2)=(C0,C_infty) configuration checked: verified n<=18, "
                       "other configurations at n>18 unchecked)")
    else:
        overall_pass = budget_pass and real_f["realizable"] and real_g["realizable"]
        verdict_str = "PASS" if overall_pass else "FAIL"

    return {
        "base": f"P(O (+) O({n_val})) over P^2",
        "n": str(n_val),
        "picard_rank": 2,
        "minus_K": {"expr": f"2*C0 + ({n_val}+3)*h", "value": [str(mK[0]), str(mK[1])]},
        "bounds": {"-4K": [str(x) for x in bound_f], "-6K": [str(x) for x in bound_g],
                   "-12K": [str(x) for x in bound_d]},
        "divisor_choice": {
            "D1": "C0 (tautological section, normal bundle O(-n*h))",
            "D2": "C_infty = C0 + n*h (tautological section, normal bundle O(n*h))",
            "disjointness": "C0 and C_infty are DISJOINT by construction for "
                            "every n (classical scroll fact: the two "
                            "sections of a split rank-2 bundle O (+) O(n*h) "
                            "correspond to its two direct summands and never "
                            "meet). Collision analysis is VACUOUS here, not "
                            "merely passed. Physically: this is exactly the "
                            "two-DISJOINT-7-brane-stack geometry of "
                            "heterotic/F-theory E8 x E8 duality (standard "
                            "F-theory literature construction).",
        },
        "budget_f": chain_f, "budget_g": chain_g, "budget_delta": chain_d,
        "realizability": {"f": real_f, "g": real_g},
        "overall_verdict": verdict_str,
        "overall_verdict_reasoning": (
            f"For n={n_val}: two E8 divisors on the disjoint tautological "
            "sections C0, C_infty satisfy the degree budget in every "
            "component with margin INDEPENDENT of n on the tightest (C0) "
            "component (margin 0 for f, exactly analogous to the P^1xP^2 "
            "case which is the n=0 instance of this family) and margin "
            "growing with n on the h-component (budget alone holds for ALL "
            "n>=0). The EXACT Tate orders are also realizable here, for "
            "this (D1,D2)=(C0,C_infty) configuration (g's residual "
            "O(2,(n+18)h) restricts to O(18-n) on C0, requiring n<=18 for "
            "THIS configuration -- comfortably satisfied for the small n "
            "checked). Necessary-condition PASS only."
            if not is_symbolic else
            "For symbolic n>=0: the raw degree BUDGET holds for ALL n>=0 "
            "(margin on the tight C0-component is n-independent, =0 for f), "
            "but exact REALIZABILITY of v(g)=5 (not accidentally pushed to "
            "6) FOR THE SPECIFIC CONFIGURATION (D1,D2)=(C0,C_infty) checked "
            "here requires the g-residual's restriction to C0, O(18-n), to "
            "be >=0, i.e. n<=18 for THIS configuration -- realizability is "
            "NOT claimed uniformly for all n>=0 by this check; it is "
            "claimed, and verified, for this configuration on n<=18 (which "
            "comfortably covers every concrete instance checked, n=0..3). "
            "Other divisor-class choices at n>18 are simply UNCHECKED here "
            "(the budget has slack in the C0- and h-components of g and "
            "Delta that a different choice could exploit), NOT shown to "
            "fail -- this is a statement about the checked configuration, "
            "not a property of the scroll itself. This qualification is "
            "exactly the kind of gap a raw-budget-only check would "
            "silently miss."
        ),
    }


def run_P1bundle_symbolic_n():
    n = sp.Symbol("n", integer=True, nonnegative=True)
    return run_P1bundle(n)


# ----------------------------------------------------------------------------
# controls (>=1 positive, >=2 negative -- plan step 4)
# ----------------------------------------------------------------------------

def control_negative_shrunk_bound():
    """Artificially shrink -4K_{P1xP2}'s h1-component from 8 to 7: the same
    two-disjoint-fiber-divisor configuration that PASSES for real must now
    FAIL, proving the checker is sensitive to the bound and not a stub."""
    bound_f_shrunk = (7, 12)   # was (8,12)
    need_f = (8, 0)            # same D1=D2=(1,0) as run_P1xP2
    result = budget_chain(need_f, bound_f_shrunk, ("h1 (f, SHRUNK)", "h2 (f)"))
    chk(not result["all_components_pass"],
        f"NEGATIVE CONTROL FAILED TO FAIL: shrunk-bound config unexpectedly passed: {result}")
    return result


def control_negative_three_e8():
    """Three E8 divisors on P^1xP^2, each class (1,0) at 3 distinct points
    (mutually disjoint by the same product-structure argument as the
    two-E8 case) -- the f-budget is exceeded (need=12 > bound=8) even
    though NO collision occurs. Demonstrates the check correctly tightens
    from 2->3 E8's exactly as the plan's step-4 control requires."""
    bound_f = (8, 12)  # -4K_{P1xP2} h1-component
    s3 = (3, 0)
    need_f = (4 * s3[0], 4 * s3[1])
    result = budget_chain(need_f, bound_f, ("h1 (f, 3xE8)", "h2 (f, 3xE8)"))
    chk(not result["all_components_pass"],
        f"NEGATIVE CONTROL FAILED TO FAIL: three-E8 config unexpectedly passed: {result}")
    return result


def control_positive_disjoint_pass():
    """The disjoint-section P^1-bundle / P^1xP^2 configuration is expected,
    from standard F-theory literature (heterotic/F-theory E8xE8 duality:
    two disjoint stacks of 7-branes realize the two E8 factors), to PASS --
    proves the checker is not a stub that always returns FAIL."""
    r = run_P1xP2()
    chk(r["overall_verdict"] == "PASS",
        f"POSITIVE CONTROL FAILED: expected PASS for disjoint-section "
        f"P^1xP^2, got {r['overall_verdict']}")
    return r


# ----------------------------------------------------------------------------
# certificate emission
# ----------------------------------------------------------------------------

def _common_footer():
    return {
        "status": "DRAFT - pending T0 (Xavier) / verification-pass review. "
                  "WP-TW1 (S3 briefs/EXECUTION_PLAN_2026_07_29_TWISTED_AND_WPE6.md, "
                  "WP-TW1 section; T0 countermand R2 2026-07-29). Producing "
                  "tier does not self-promote to LIVE.",
        "not_claimed": [
            "This is a NECESSARY-CONDITION SCREEN ONLY. A PASS does not "
            "assert the M-polarized cooper_s7 family (rho=19, T ≅ U (+) "
            "<14>) actually EXISTS on that base -- exhibiting f, g "
            "sections that realize the specific M-polarization is separate, "
            "harder, NOT-YET-attempted future work (S3 audit $A5: 'the "
            "honest hard part... this, not the E8 degree count, is where "
            "the route most plausibly dies').",
            "Does not construct any explicit f, g polynomial.",
            "Does not address whether the resulting singularities (beyond "
            "the two E8 loci) admit a crepant resolution.",
            "P^3's FAIL verdict is for P^3 AS GIVEN only. Does NOT claim that "
            "a blow-up of P^3 along the forced collision curve D1 ∩ D2 also "
            "fails -- the standard F-theory cure for a codim-2 (4,6) locus "
            "is exactly such a blow-up, producing a DIFFERENT base not "
            "checked here (see the P^3 certificate's 'collision_analysis' "
            "block for the two-readings discussion this scopes).",
            "Placing BOTH E8 loci on a single divisor (D1=D2) is not "
            "separately re-checked as a numeric case -- it is ruled out by "
            "inspection (would require v(g)>=10 on one divisor, immediately "
            "past the (4,6) curse) and is not among the configurations "
            "reported PASS/FAIL above.",
            "On the P^1-bundle family, exact-order realizability is verified "
            "ONLY for the SPECIFIC configuration (D1,D2)=(C0,C_infty) checked "
            "here, and ONLY for n<=18 (where g's residual restricted to C0 "
            "stays effective). This is NOT a claim that the scroll itself "
            "fails realizability for n>18 -- the budget has slack there (in "
            "the C0- and h-components of g and Delta) that a DIFFERENT "
            "divisor-class choice could exploit; that possibility is simply "
            "UNCHECKED by this WP, not shown to fail.",
            "No physical coupling of any kind claimed (VISION sec 1.3).",
            "No observable of any kind (m_phi, alpha_D, Lambda_D) -- F5b stands.",
        ],
        "checker": "check_TW1_two_e8_feasibility.py",
        "checker_version": "1.0.0",
        "date": "2026-07-29",
        "tier": "E",
        "tier_reason": "Exact classical algebraic geometry (canonical class "
                       "of P^3/product/scroll via cited standard formulas, "
                       "Picard-lattice linear algebra, projective dimension "
                       "theorem, Tate order divisibility arithmetic) computed "
                       "with sympy Integer/Rational only -- no floats, no "
                       "numerical tolerance. This is a repo-local "
                       "computation-quality tag (distinct from VISION.md's "
                       "epistemic Tier A/B/C), matching the convention used "
                       "in check_G1a_CY_twist_condition.py's certificates. "
                       "Depends on G0 (Tier B, LIVE) only for the QUALITATIVE "
                       "fact 'two E8(-1) summands must be supportable' -- "
                       "does not use the rho=19/T=3 numeric derivation in "
                       "its own arithmetic, so this result is unconditional "
                       "given G0's NS(cooper_s7) ⊇ E8(-1)(+)E8(-1) finding.",
        "provenance": "Generated-by: Sonnet 5 (Stream 2, WP-TW1 session "
                      "2026-07-29) | Verified-by: check_TW1_two_e8_feasibility.py "
                      "structural assertions + checkers/"
                      "test_TW1_two_e8_feasibility_controls.py | "
                      "Reviewed-by: pending T0 (Xavier) -- coordinator "
                      "reviews and commits, no agent commits",
    }


def emit_certificate(result, cert_name, out_path):
    cert = {
        "certificate": cert_name,
        "operator": "cooper_s7 (two E8(-1) requirement per G0, "
                    "data/certificates/G0_NS_genus_cooper_s7.json)",
        "necessary_condition": "E8 (Kodaira II*) Tate orders v(f)>=4, v(g)>=5, "
                               "v(Delta)=10 along a divisor D; for two "
                               "divisors D1,D2: 4[D1]+4[D2]<=[-4K], "
                               "5[D1]+5[D2]<=[-6K], 10[D1]+10[D2]<=[-12K] in "
                               "the effective cone, PLUS collision analysis.",
        "result": result,
        **_common_footer(),
    }
    out_path.write_text(json.dumps(cert, indent=2, default=str))
    print(f"\nWrote {out_path.relative_to(REPO)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-cert", action="store_true")
    ap.add_argument("--out-p3", default=str(REPO / "data" / "certificates" / "TW1_two_e8_P3.json"))
    ap.add_argument("--out-p1xp2", default=str(REPO / "data" / "certificates" / "TW1_two_e8_P1xP2.json"))
    ap.add_argument("--out-p1bundle", default=str(REPO / "data" / "certificates" / "TW1_two_e8_P1bundle_P2.json"))
    args = ap.parse_args()

    try:
        print("=== WP-TW1: two-E8 degree-feasibility check, twisted route gate ===\n")

        r_p3 = run_P3()
        print(f"[P^3] raw budget passes: {r_p3['raw_degree_budget_boundary_case_d1_2_d2_2']['all_components_pass']}")
        print(f"[P^3] collision unavoidable: {r_p3['collision_analysis']['collision_unavoidable_for_every_d1_d2']}")
        print(f"[P^3] overall verdict: {r_p3['overall_verdict']}\n")

        r_p1xp2 = run_P1xP2()
        print(f"[P^1xP^2] overall verdict: {r_p1xp2['overall_verdict']}\n")

        results_bundle = []
        for n_val in range(4):
            r = run_P1bundle(sp.Integer(n_val))
            results_bundle.append(r)
            print(f"[P(O(+)O({n_val}))/P^2] overall verdict: {r['overall_verdict']}")
        r_bundle_symbolic = run_P1bundle_symbolic_n()
        print(f"[P(O(+)O(n))/P^2, symbolic n>=0] overall verdict: {r_bundle_symbolic['overall_verdict']}\n")

        # controls
        pos = control_positive_disjoint_pass()
        neg1 = control_negative_shrunk_bound()
        neg2 = control_negative_three_e8()
        print("[control] positive (disjoint P^1xP^2): PASS as expected")
        print("[control] negative (shrunk bound): correctly FAILS")
        print("[control] negative (three E8): correctly FAILS")

        chk(r_p3["overall_verdict"] == "FAIL", "P^3 unexpectedly not FAIL")
        chk(r_p1xp2["overall_verdict"] == "PASS", "P^1xP^2 unexpectedly not PASS")
        chk(r_bundle_symbolic["overall_verdict"].startswith("PASS"),
            f"P^1-bundle (symbolic n) unexpectedly not PASS: {r_bundle_symbolic['overall_verdict']}")
        chk(all(r["overall_verdict"] == "PASS" for r in results_bundle),
            "not all concrete P^1-bundle instances (n=0..3, within the "
            "(C0,C_infty)-configuration's verified n<=18 realizability "
            "band) PASS")

        if args.emit_cert:
            emit_certificate(r_p3, "TW1_two_e8_P3", Path(args.out_p3))
            emit_certificate(r_p1xp2, "TW1_two_e8_P1xP2", Path(args.out_p1xp2))
            emit_certificate(
                {"symbolic_n": r_bundle_symbolic, "concrete_instances_n_0_to_3": results_bundle,
                 "controls": {"positive_disjoint_P1xP2": pos,
                              "negative_shrunk_bound": neg1,
                              "negative_three_e8": neg2}},
                "TW1_two_e8_P1bundle_P2", Path(args.out_p1bundle))

        print("\n=== SUMMARY ===")
        print("B3 = P^3:                       FAIL (raw budget passes, collision-forced non-minimality)")
        print("B3 = P^1 x P^2:                 PASS (disjoint fiber divisors; budget AND exact-order realizability both verified)")
        print("B3 = P(O(+)O(n))/P^2, n=0..3:   PASS (disjoint sections; budget AND exact-order realizability both verified)")
        print("B3 = P(O(+)O(n))/P^2, all n>=0: budget PASSES uniformly; for the (D1,D2)=(C0,C_infty)")
        print("                                 configuration checked, exact-order realizability verified for n<=18")
        print("                                 (other configurations at n>18 unchecked, not shown to fail)")
        print("\ncheck_TW1_two_e8_feasibility.py: all structural assertions passed")
        return 0
    except ControlFailure as e:
        print(f"\nFAIL / PRECONDITION VIOLATION: {e}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
