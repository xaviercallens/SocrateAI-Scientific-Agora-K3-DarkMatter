# WP-TW1 result: two-E8 degree-feasibility gate for the twisted-Weierstrass route

**Date:** 2026-07-29. **Status:** DRAFT — pending T0 (Xavier) / independent verification-pass
review before any promotion to LIVE. Producing tier does not self-promote (standing rule).
**WP:** WP-TW1 (S3 `briefs/EXECUTION_PLAN_2026_07_29_TWISTED_AND_WPE6.md`, WP-TW1 section),
authorized by T0 countermand R2 2026-07-29 (S2 `briefs/T0_COUNTERMAND_R2_2026_07_29.md`;
S2 `CLAUDE.md` ledger entry 6: Route A CLOSED, twisted-Weierstrass PRIMARY).

## Question asked

Route A (strict pullback) is closed. The promoted primary route builds a Calabi–Yau fourfold
directly as a generic Weierstrass model `y² = x³ + fx + g`, `f ∈ H⁰(−4K_B3)`,
`g ∈ H⁰(−6K_B3)`, on a threefold base B3. The certified G0 result (Tier B, LIVE, three
independent lineages) proved `NS(cooper_s7) ⊇ E8(-1) ⊕ E8(-1)`: any valid B3 must be able to
host **two** E8 (Kodaira II\*) gauge loci in the discriminant `Δ = 4f³+27g²`. **Before anyone
attempts to build the family**, WP-TW1 asks only: is this arithmetically and geometrically
*possible at all*, as a pure necessary-condition (degree-budget + collision) screen, on any
standard 3-fold base?

**This is a necessary-condition screen only.** A PASS below does **not** assert the
M-polarized cooper_s7 family (ρ=19, T ≅ U⊕⟨14⟩) actually exists on that base — exhibiting the
specific f, g sections realizing that M-polarization is separate, harder, not-yet-attempted
future work (S3 `DEEPTHINK_DEBRIEF_AUDIT_2026_07_29.md` §A5: "the honest hard part... is where
the route most plausibly dies," referring to the M-polarization, not the E8 degree count).

## Necessary condition (formalized here, plan step 1)

E8 (type II\*) locus over a divisor D needs Tate orders `v(f)≥4, v(g)≥5, v(Δ)=10` along D
(plan's own formalization, adopted by S3 audit §A5 as "standard, correct"). For it to hold
globally along D, f must be divisible by D⁴ and g by D⁵ as global sections. For two divisors
D1, D2 required independently: `4[D1]+4[D2] ≤ [−4K_B3]`, `5[D1]+5[D2] ≤ [−6K_B3]`,
`10[D1]+10[D2] ≤ [−12K_B3]` in the effective cone — plus the **collision analysis** (plan step
3, mandatory): if D1 ∩ D2 ≠ ∅, the vanishing orders of f, g **add** at the intersection
(distinct irreducible divisors, unique-factorization argument), which can trigger the standard
Weierstrass non-minimality flags independently of whether the raw per-divisor budget passes.

Uses the audit-corrected `deg Δ = 48` on P³ (`−K_{P³}=O(4) ⇒ −12K=O(48)`, **not 144** — the
verbatim external debrief's number was an arithmetic error, discarded, not propagated).

## Result: verdict table

| Base B3 | Raw degree budget (per-divisor) | Collision? | Exact-order realizability | **Verdict** |
|---|---|---|---|---|
| P³ (Pic rank 1) | PASSES (e.g. D1=D2=2H: f 16≤16, g 20≤24, Δ 40≤48) | **Unavoidable** (Pic(P³)=ℤ ⇒ any two nonzero effective divisors intersect, classical projective dimension theorem) | moot — collision already fails the base | **FAIL** |
| P¹×P² (Pic rank 2) | PASSES (D1=D2=(1,0) at distinct P¹-points: f 8≤8 tight, g 10≤12, Δ 20≤24) | **None** — D1={p1}×P², D2={p2}×P², p1≠p2 ⇒ disjoint by set-theoretic construction | VERIFIED (f-, g-residuals restrict to O(12), O(18) on both divisors — both ≥0) | **PASS** |
| P(O⊕O(n)) over P², n=0,1,2,3 | PASSES for every n (f-margin 0 on the tight component, independent of n; g-, Δ-margins grow with n) | **None** — C0, C∞ (tautological sections of the split bundle) are disjoint by construction for every n | VERIFIED for n=0,1,2,3, for the configuration D1=C0, D2=C∞ (g-residual restricts to O(18−n) on C0, O(n+18) on C∞ — both ≥0 for n≤18) | **PASS** (n=0..3) |
| P(O⊕O(n)) over P², symbolic n≥0 | PASSES uniformly in n (tight-component margin is n-independent) | **None**, uniformly in n | For the SAME (D1,D2)=(C0,C∞) configuration: VERIFIED for n≤18 (g-residual's C0-restriction is O(18−n), negative past n=18 *for this configuration*). Other divisor-class choices at n>18 are **unchecked**, not shown to fail (the budget has slack there) | **PASS for budget (all n≥0); PASS for realizability of the checked configuration on n≤18** |

**Headline, revised after a second-pass review caught a gap in the first draft: the raw
per-divisor degree arithmetic PASSING is NECESSARY but NOT SUFFICIENT.** A budget PASS only
shows `D1⁴D2⁴ | f` etc. is arithmetically *possible*; it does not show the *exact* Tate orders
(`v(f)=4`, not silently pushed to a higher value) are *achievable* by an actual section — if
every member of the residual linear system happened to vanish identically on one of the two
divisors, the true order would be forced higher (e.g. to `v(g)≥6`), triggering non-minimality
even with **no** collision. This was checked explicitly (not assumed) via the scroll's standard
`H⁰` decomposition, for the specific configuration D1=C0, D2=C∞ used throughout: the residual
bundle after extracting `D1⁴D2⁴` (resp. `D1⁵D2⁵`) restricts to `O(18−n)` on C0 and `O(n+18)` on
C∞ for the g-condition — both non-negative, hence realizable by a generic choice, **for this
configuration, when n≤18**. **The result survives this sharper check for every base and every
concrete n checked (0..3).** For the general symbolic-n family, a second review pass caught a
further imprecision in an intermediate draft: the `n≤18` bound is a property of the *checked
configuration* `(D1,D2)=(C0,C∞)`, not a limit of the scroll itself — the g-budget has slack in
other components that a different divisor-class choice could exploit past `n=18`, which this WP
does not check. The corrected claim: budget alone holds for all n≥0; exact-order realizability
of the *specific* `(C0,C∞)` configuration is verified for n≤18; other configurations at n>18 are
**unchecked**, not shown to fail.

P³ fails because Pic-rank-1 forces the two E8 loci to collide; both disjoint-section bases
(P¹×P² and the P¹-bundles over P² checked) avoid the collision entirely by construction and
pass with comfortable margins on both the budget and the sharper realizability check.

## P³ collision analysis, in detail (plan step 3, load-bearing)

Pic(P³) = ℤ·H. Any two nonzero effective divisors D1=d1·H, D2=d2·H (d1,d2≥1) satisfy
dim(D1)+dim(D2) = 2+2 = 4 ≥ 3 = dim(P³), forcing D1∩D2 ≠ ∅ (classical projective dimension
theorem) — confirmed numerically via the intersection number D1·D2 = d1·d2·(H³) = d1·d2 > 0 for
every d1,d2 ≥ 1. At a generic point of the intersection curve C = D1∩D2, because f is divisible
by **both** D1⁴ and D2⁴ as global sections (distinct irreducible divisors ⇒ unique
factorization forces the combined divisibility D1⁴D2⁴|f), the vanishing orders **add**:
v_C(f) ≥ 4+4 = 8, v_C(g) ≥ 5+5 = 10. Two independent standard non-minimality tests both fire:
the (4,6)-curse (v(f)≥4 ∧ v(g)≥6 ⇒ worse-than-canonical singularity, blow-up required) and the
discriminant-order flag (v(Δ) ≥ min(3·8, 2·10) = 20 ≥ 12). **This holds for every d1,d2 ≥ 1** —
the collision is not a corner case, it is forced by Pic(P³) having rank 1, so no choice of
divisor degrees rescues P³.

### Non-minimality convention — where the real ambiguity is (corrected on review)

An earlier draft of this analysis mis-scoped the ambiguity as "does v(f), v(g) add at the
collision curve C?" — **that is not a convention choice, it is a theorem.** Unique
factorization of sections forces `D1⁴D2⁴ | f` (resp. `D1⁵D2⁵ | g`) once both divisibility
conditions are imposed on the distinct irreducible divisors D1≠D2 simultaneously; there is no
coherent alternative reading under which C even has a single well-defined local vanishing order
to assign a different value to.

The **genuinely open question**, correctly placed on review, is what a codim-2 (4,6) locus
*means* for the base — not whether it occurs. This repo's `refs/` has no F-theory/Tate-algorithm
literature entries to settle it, so both readings are stated explicitly rather than one being
silently assumed:

- **Reading 1 (adopted here):** a codim-2 (4,6) locus means no minimal Weierstrass CY exists
  over B3 *as given* — P³ FAILS.
- **Reading 2:** in the standard F-theory literature, a codim-2 (4,6) locus is routinely *cured*
  by blowing up the base along the offending curve, producing a strictly different base
  `Bl_C(P³)` — under this reading P³-as-given still fails (the model over P³ itself is
  non-minimal), but this says **nothing** about whether the blow-up would pass a re-run of this
  same check. That base is **not checked by this WP**.

**Both readings agree on the verdict for P³-as-given** (additivity, which is forced regardless,
already decides that), so the table above is not affected by which reading is taken — but they
differ in *scope*, and that scope boundary is recorded explicitly in `not_claimed` rather than
resolved by omission: **this brief does not claim blow-ups of P³ along the collision curve
fail.** No escalation trigger is hit (the verdict itself is convention-independent), but the
scope question is a live one for whoever next considers P³-family bases.

## Positive and negative controls (plan step 4)

- **Positive:** the disjoint-section P¹×P² configuration (§ above) PASSES — the classically
  expected geometry (two disjoint stacks of 7-branes / E8 loci is exactly the heterotic/F-theory
  E8×E8 dual construction in the standard literature). Confirms the checker is not a stub.
- **Negative 1 (shrunk bound):** artificially shrinking `−4K_{P1×P2}`'s tight component from 8
  to 7 flips the same two-E8 configuration from PASS to FAIL (margin −1). Confirms sensitivity
  to the actual bound.
- **Negative 2 (three E8):** three mutually-disjoint E8 divisors on P¹×P² (same construction,
  one more point-fiber) exceed the f-budget (need 12 > bound 8) even though no collision occurs
  — confirms the check correctly tightens as the E8 count increases from two to three.

All controls implemented in `checkers/test_TW1_two_e8_feasibility_controls.py`, all passing.

## What this does NOT claim

- Does not construct any explicit f, g polynomial on any base.
- Does not assert the M-polarized cooper_s7 family exists on P¹×P² or any P¹-bundle — only that
  the two-E8 degree/collision/realizability necessary condition does not by itself rule those
  bases out. Forcing the actual M-polarization (ρ=19, T≅U⊕⟨14⟩) is separately flagged by the S3
  audit as "the honest hard part" and is not attempted here.
- Does not address crepant resolvability of any residual singularities beyond the two E8 loci.
- P³'s FAIL verdict is for P³ **as given** only — does not claim a blow-up of P³ along the
  collision curve also fails (see the two-readings discussion above); that base is unchecked.
- Does not re-check D1=D2 (both E8 loci on one divisor) as a separate numeric case — ruled out
  by inspection (would need v(g)≥10 on a single divisor, immediately past the (4,6) curse).
- For the P¹-bundle family, exact-order realizability is verified only for the SPECIFIC
  configuration `(D1,D2)=(C0,C∞)` checked throughout, and only for n≤18 (where g's residual
  restricted to C0 stays effective). This is **not** a claim that the scroll itself fails
  realizability for n>18 — the budget has slack in other components that a different
  divisor-class choice could exploit; that possibility is unchecked, not shown to fail.
- No observable of any kind (m_φ, α_D, Λ_D) — F5b stands. No physical coupling of any kind
  (VISION §1.3).

## Method

Exact sympy Integer/Rational arithmetic throughout (no floats). Canonical classes for P³,
P¹×P², and the scroll P(O⊕O(n)) over P² are standard classical formulas (cited, not
re-derived from scratch here — the scroll formula was cross-checked to reduce to the known
Hirzebruch `K_{Fn} = −2C0−(n+2)f` formula when the base is P¹ instead of P², confirming the
generalization to a P² base). The realizability check uses the scroll's standard `H⁰`
decomposition (`H⁰(aC0+π*L) = ⊕_{i=0}^a H⁰(P²,L−i·n·h)`, cited classical fact), independently
cross-checked two ways: against the Hirzebruch restriction-to-C0 identity and by symmetry under
C0↔C∞. Checker: `checkers/check_TW1_two_e8_feasibility.py`. Controls:
`checkers/test_TW1_two_e8_feasibility_controls.py` (5 controls, all passing: 1 positive, 2
negative per plan step 4, plus the P³ headline re-assertion and a malformed-input guard — the
positive/negative controls exercise the realizability logic too, since they call the same
`run_P1xP2()`/`run_P1bundle()` functions that now gate PASS on it).

Certificates:
- `data/certificates/TW1_two_e8_P3.json`
- `data/certificates/TW1_two_e8_P1xP2.json`
- `data/certificates/TW1_two_e8_P1bundle_P2.json` (covers n=0..3 concretely, plus the fully
  general symbolic-n derivation, plus the three controls)

## Status and next step

**DRAFT.** All bases checked did NOT uniformly fail — this is a mixed (not a No-Go) result:
P³ fails (collision-forced, as given), disjoint-section bases (P¹×P², P¹-bundles over P² for
n=0..3 concretely, budget uniformly for all n≥0, realizability verified for 0≤n≤18) pass the
necessary-condition screen. Per the plan's escalation trigger, an "ALL bases FAIL" scenario
would require a T0 ruling on publication framing as a documented No-Go — that trigger is
**not** hit here. The recommended next action for T0 is to authorize (or not) the harder
follow-on WP: attempting to exhibit the actual M-polarized f, g sections on the surviving
P¹-bundle-over-P² family (the audit's identified "honest hard part"), which this WP explicitly
does not attempt.

## Decision log

- **2026-07-29, coordinator (separate session, producer≠verifier):** re-ran
  `checkers/check_TW1_two_e8_feasibility.py` and `checkers/test_TW1_two_e8_feasibility_controls.py`
  fresh from a clean shell — checker's summary table and all 5 controls reproduce exactly as
  claimed above. Independently hand-derived (not just re-read) the load-bearing numbers rather
  than trusting the checker's own arithmetic: (1) P³ collision — `-K_{P³}=O(4)` (standard
  `K_{P^n}=O(-n-1)`), `deg(-12K)=48`, combined orders at the forced intersection `v_f=4+4=8`,
  `v_g=5+5=10`, `v_Δ=min(3·8,2·10)=20` — (4,6)-curse and `v_Δ≥12` both fire, matches. (2) P¹×P²
  budget — `-K=O(2,3)`, `s=(2,0)`, `need_f=(8,0)` vs `bound_f=(8,12)` (tight on h1 as claimed),
  residual_f=(0,12), residual_g=(2,18), both restrict non-negatively — matches. (3) Scroll
  family symbolic-n — re-derived `K_X=-2C0-(n+3)h` independently as the general-base
  specialization of the scroll canonical-bundle formula (coefficient = n + deg(-K_base): 2 for
  P¹→Hirzebruch's `n+2`, 3 for P²→`n+3`, self-consistent with the module's claimed Hirzebruch
  reduction); re-derived the g-residual's C0-restriction as `18−n` from scratch (residual_g =
  `(2, n+18)`, `restrict_to_C0 = (n+18) − 2n = 18−n`) — matches the brief's `n≤18` threshold
  exactly, including that this is scoped to the specific `(C0,C∞)` configuration only. No
  discrepancy found between this independent re-derivation and the producing session's claims.
  **Status stays DRAFT** — coordinator verification does not self-promote to LIVE; that is a
  T0-only call. Recommend T0 review the mixed result (P³ FAIL / disjoint-section bases PASS)
  and rule on the next-step question already posed above (authorize the harder M-polarization
  exhibition attempt on the surviving P¹-bundle family, or not).

Provenance: Generated-by: Sonnet 5 (Stream 2, WP-TW1 session 2026-07-29) | Verified-by:
`checkers/check_TW1_two_e8_feasibility.py` structural assertions +
`checkers/test_TW1_two_e8_feasibility_controls.py` + coordinator independent hand-derivation
(2026-07-29, separate session) | Reviewed-by: pending T0 (Xavier)
