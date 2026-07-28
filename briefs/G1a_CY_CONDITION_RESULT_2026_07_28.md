# WP S2-G Phase G1-a result: CY/twist condition — B2 ladder OBSTRUCTED

**Date:** 2026-07-28. **Status:** DRAFT — pending T0 (Xavier) / independent verification-pass
review before any promotion to LIVE. Producing tier does not self-promote (standing rule:
verification is never done by the producing tier).
**Phase:** WP S2-G Phase G1-a (briefs/WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md §1 & §5, G1-a
bullet), opened by T0 2026-07-28 (briefs/T0_DECISIONS_2026_07_28_STREAM2.md item 2, "Phase G1
GATE OPENED (Route A)").

## Result

**For every base surface in the plan's own proposed B2 ladder — P², and every Hirzebruch
surface F_n (n≥0, which includes P¹×P¹ as F₀) — the naive fiber-product pullback of the
certified cooper_s7 K3 family along a moduli map φ: B2 → (z-line) CANNOT be Calabi-Yau
(c1(X4)≠0), for every choice of non-constant φ and for EVERY value of the family's
(uncomputed) Hodge-bundle degree ℓ.** This is a structural, ℓ-independent obstruction, proven
by exact linear algebra over each surface's Picard lattice — not a numerical near-miss.

Two independent failure modes, one per rung:

- **B2 = P²: no φ exists at all, unconditionally.** Load-bearing argument (Picard-lattice):
  Pic(P²) = ℤ·H is rank-1 and positive-definite (H²=1). A rank-1 positive-definite lattice has
  no nonzero isotropic vector (n²·k=0 with k>0 forces n=0 over ℚ — solved exactly, not
  asserted). Since any algebraic fibration φ: B2→(curve) requires a fiber class F with F²=0
  (distinct fibers are numerically disjoint), and every nonzero class on P² is a multiple of H
  with (nH)²=n²>0 for n≠0, **no non-constant φ: P² → (z-line) exists.** This argument never
  references the target curve — only Pic(P²) itself — so it holds uniformly for a target of
  any genus; that is a genuinely stronger, and different, statement than the usual "P² is
  simply connected" genus-≥1 argument, since it also rules out genus-0 targets. As an
  **independent corroboration** (a second, distinct argument, not a restatement): classical
  Bezout — two curves of degree e≥1 in P² meet in e²>0 points, so no base-point-free pencil
  |O(e)| exists for e≥1. The CY/twist condition is therefore not merely failed but **vacuous**
  for P² — there is no candidate fiber class to test it against. The constant-φ case (X4 = P²
  × K3) also fails: K_{P²} = −3H ≠ 0.

- **B2 = F_n (all n≥0, incl. P¹×P¹): φ exists (the standard ruling), but K_{B2} is never
  proportional to the fiber class.** K_{F_n} was **derived here via the adjunction/genus-
  degree formula** (2g(C)−2 = C² + K·C, applied to the section s and fiber f, both rational),
  not assumed from memory — giving exactly K_{F_n} = −2s − (n+2)f, for every n. Matching this
  against −ℓ·f requires the s-coefficient to vanish: −2 = 0, which is false for every n and
  every ℓ. **Unsolvable, uniformly in n and ℓ.** Corollary (ℓ-blind) cross-check: K_{F_n}² = 8
  ≠ 0 for every n (Noether's formula K² = 12·χ(O) − e, e(F_n) = 4, χ(O) = 1). The constant-φ
  case also fails for every n (same nonzero s-coefficient).

**Positive control (proves the checker is not a stub):** a degree-9 del Pezzo surface dP9 (=
P² blown up at 9 points), with its classical anticanonical elliptic fibration (fiber class F =
−K, verified F²=0 exactly), **does** satisfy the twist condition, with ℓ **solved** (not
assumed) to be exactly 1 — matching the classical fact that a generic rational elliptic
surface has Hodge-bundle degree χ_top/12 = 12/12 = 1. The same machinery that obstructs the
whole B2 ladder genuinely admits a structurally different, correctly-posed input.

## What this does NOT claim

- **Does not compute ℓ** (the cooper_s7 family's Hodge-bundle degree over X₀(7)+/z-line) — not
  needed for this result, and no orbifold Riemann–Hurwitz/Roch computation on X₀(7)+ was
  attempted. The obstruction holds for every possible value of ℓ, which is a strength: the
  result is robust to a quantity this repo has not yet derived, stated explicitly rather than
  silently assumed away.
- **Does not address G1-b (crepant resolution) or G1-c (F-theory posability)** — moot for a
  B2 that already fails G1-a.
- **Does NOT claim K3-fibered Calabi-Yau fourfolds fail to exist over P² or F_n by ANY
  construction.** The obstruction here is specific to the NAIVE fiber-product pullback of a
  FIXED 1-parameter family along a FIXED moduli map φ — exactly what the plan's G1-a bullet
  asks about. The plan's own "−4K/−6K Weierstrass twisting" analogy may point at a more
  general construction (choosing the total space directly via twisted sections on B2, rather
  than factoring through a map to a fixed 1-dimensional modulus) — that alternative is **not**
  tested here and would require an explicit Weierstrass-like presentation of the M-polarized
  family directly on B2. Flagged as the natural next question if Route A on this ladder is
  pursued further.
- No observable of any kind (m_φ, α_D, Λ_D) — F5b stands. No physical coupling of any kind
  (VISION §1.3).

## Method

Exact classical algebraic geometry throughout — canonical class derived via adjunction (not
assumed), Picard-lattice linear algebra, Bezout/isotropy — sympy Integer/Rational only, no
floats, no numerical tolerance anywhere. **Unlike G0, this derivation does not touch the
family's monodromy-derived transcendental lattice T at all** (ℓ cancels out of the argument
entirely), so this result does not inherit G0's Tier-B ceiling from T; see the certificates'
own `tier`/`tier_reason` for the Tier E justification and DRAFT-status caveat.

Checker: `checkers/check_G1a_CY_twist_condition.py`. Companion negative controls (5, all
passing): `checkers/test_G1a_CY_condition_controls.py` — (1) the full ladder re-asserted
OBSTRUCTED standalone, (2) dP9 positive control re-asserted ADMISSIBLE with ℓ=1, (3) a
non-isotropic candidate fiber class rejected loudly, (4) an asymmetric "Gram matrix" rejected
loudly, (5) a rank-1 negative-definite boundary case sanity check on the isotropy guard.

Certificates:
- `data/certificates/G1a_CY_condition_P2.json`
- `data/certificates/G1a_CY_condition_Fn_ladder.json` (covers F_n for n=0..5 concretely, plus
  the fully general symbolic-n derivation)

## Status and next step

**DRAFT.** This is producer-tier work (Sonnet, this session); per this project's standing
"verification is never done by the producing tier" rule, it does not self-promote to LIVE. The
recommended next action for T0 is the same two-part framing the advisor review of this WP
surfaced: (i) accept the untwisted-pullback obstruction as a documented, ℓ-independent
structural negative for the plan's proposed ladder (a legitimate G1-a outcome per the plan's
own "a documented dead end beats an undocumented detour" house style); and (ii) decide whether
Route A is worth continuing on a **revised** B2 ladder restricted to surfaces satisfying the
necessary condition K_{B2}² = 0 exhibited here (e.g. rational elliptic surfaces / blow-ups of
P² at ≥9 points in general position, K3 surfaces, abelian or bielliptic surfaces) — or whether
the "twisted" (non-pullback) construction gestured at by the plan's own Weierstrass analogy is
the more promising direction, which would need G1-a's scope to be revisited with an explicit
Weierstrass-type presentation of the M-polarized family, a genuinely different and larger
undertaking not attempted here.

**One question to name for T0, not answered here:** if a revised, K_{B2}²=0 ladder is pursued,
does G1-b/G1-c's design still apply unchanged, or does G0's U-summand argument (certified only
for the fiberwise, abstract-lattice statement — see that certificate's own "FIBERWISE, NOT YET
RELATIVE" caveat) need to be re-derived for a non-rational candidate base (e.g. a K3 or abelian
surface base is not simply-connected, unlike every surface in the original ladder)? This is a
scoping question for whoever opens the next rung, not a finding of this deliverable.

Provenance: Generated-by: Sonnet 5 (Stream 2, WP S2-G Phase G1-a session 2026-07-28) |
Verified-by: checkers/check_G1a_CY_twist_condition.py structural assertions +
checkers/test_G1a_CY_condition_controls.py | Reviewed-by: pending T0 (Xavier)
