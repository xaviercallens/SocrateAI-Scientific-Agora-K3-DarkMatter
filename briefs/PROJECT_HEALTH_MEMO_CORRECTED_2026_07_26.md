# Project Health, Theory Completion Status, and Roadmap — CORRECTED

**To:** Xavier Callens (T0 Owner)
**From:** Stream 2
**Date:** 2026-07-26 (evening)
**Supersedes:** the "Overall Project Health, Theory Completion Status, and Roadmap to Finish"
memo circulated earlier today. That draft contained two governance-level errors and four stale
claims — itemized in `ESCALATIONS.md` **E-015**. Do not circulate the earlier version.

---

## The honest headline

**Yes, the project is in good shape — but the reason is narrower than the original memo claimed.**

The guardrails worked: the Two-Model Rule, adversarial review, and in-band retraction discipline
caught a false geometry (E-007), two fabricating pipelines (E-010, E-012), and an astrophysical
category error (3D void statistics from photometric data). That part of the earlier memo was
right, and it is worth saying plainly.

What the earlier memo got wrong is the *direction of travel*. It described a project **days from
a complete framework**, with an M2 derivation and an unblinded test as the remaining steps. The
actual position is that **the physics branch has already landed — on a pre-registered negative
(F5b)** — and the mathematics is what survives. That is a real, publishable outcome. It is not a
setback. But it is not "three steps from a testable topological universe model" either, and
planning against that picture would put Stream 2 back onto work T0 has explicitly gated off.

---

## 🟢 Stream 1 — Pure Mathematics (Lean 4): parked clean

**Effectively complete.** This is the strongest part of the project and the earlier memo
under-reported it in one respect and over-reported it in another.

- `L₃ = Sym²(L₂)` — kernel-proven in Lean 4 for both s7 and s10, zero `sorry`, axiom-clean.
- **Dyadic baseline** — kernel-proved (`sqrtSeq_dyadic`): the formal square root of *any* integer
  series carries only 2-power denominators. s10 and s18 partners are provably **non-integral**
  (explicit witnesses `17/2`, `45/2` at n=2), and that is the *generic* behaviour. **s7 avoiding
  it is a genuine arithmetic anomaly** — correct as stated.
- **One** open goal remains, not two: `open_goal_partner_eq_sqrt_s7`, classified
  **blocked-on-mathlib** (needs operator→solution-sequence transport machinery the pinned Mathlib
  doesn't provide). The second goal, `open_goal_partner_integral_s7`, was **reopened and closed**
  (WP S1-13).
- **One caveat the earlier memo dropped:** that closure rests on a *literature axiom* — O'Brien
  2016 **Theorem 6.2, p.47**, registered in `AXIOMS.md` (2 axioms total, both registered). It is
  a theorem in-kernel, not a `PASS(N)` verification, but it is not derived from first principles
  either. Stream 2 converged on the same result independently via the normalized-uniformizer
  mechanism (`X₇ = q − 9q² + …` is monic; reverting a monic integral series never introduces a
  denominator) — that route is Tier B computational, and the axiom is what makes the conclusion
  Tier A.

`lake build` green (3118 jobs), 0 `sorry` outside `OpenGoals/`. **Stream 1 is parked. Nothing
blocks it and it blocks nothing.**

---

## 🟡 Stream 2 — Theory: mathematics complete, physics branch closed

The earlier memo described a "massive breakthrough" and put Stream 2 at ~70% with M2 as the next
step. Both halves need correcting.

### What is genuinely settled — and it is a real result

**ρ = 19, T = 3, derived exactly** (E-011, tier B) — not `ρ ≤ 19`. The chain: L₃ irreducible ⇒
minimal-order annihilator ⇒ rank V = 3; the K3s are projective (Almkvist–van Straten explicit
models — six hyperplane sections of G(2,6); four (1,1) sections in ℙ³×ℙ³); T(X)⊗ℚ irreducible
(Zarhin 1983 Thm 1.6(a), Huybrechts 3.2.7/3.3.1, both fetched and read in primary form); a
nonzero sub-Hodge-structure of an irreducible one forces V = T, hence ρ = 22 − 3 = 19.
Independently reproduced by Stream 1.

The earlier memo's *physical reading* of this is right and worth keeping: T = 3 means the three
periods of the s7 ODE control all the complex-structure moduli, so the old T = 18 picture's 15
uncontrolled flat directions — which violated fifth-force bounds — are gone.

### Where the memo went wrong

**There are no Type II fibres to build within.** E-007 did not revise the Kodaira classification;
it retracted it. L₂ is a *twisted* Picard–Fuchs operator (monodromy determinant −1, outside
SL₂(ℤ)), so no Kodaira type is derivable from it at all, and E-009 established that the finite
singular loci are **order-2 elliptic points of a Fuchsian group** — finite-order monodromy by
construction, not fibre degenerations. The old "2× Type II" traced to a hardcoded `components=2`.
Note also the polarity: while it was live, Type II was a **veto** (no weakly-coupled gauge algebra
from cuspal fibres — Wall 1 of M1), not permissive headroom.

**M2 is not the next step; it is not authorized.** Per T0 decision **D2**, Phase M is **dormant**
and M2 opens only when *both* (i) Route γ yields derived C1v3/C2v3 lattice data, and (ii) T0
re-opens Phase M by explicit decision. Neither condition is met — Route γ's actual outcome was
E-009, which found the fibration reading category-mismatched, i.e. the opposite of delivering
fibre data.

**The branch has already closed.** WP S3-00 ran and reached an honest obstruction: **F5b, no
prediction extractable**, adopted into `PREDICTION.md` **v1.1-PINNED §6**. Two independent
obstructions, not one: (1) no explicit compactification exists — no flux quanta, no genuine
moduli stabilization, so m_φ has no numerator; (2) `EXECUTION_PLAN.md` §S3-00 step 2(b) derives
α_D, Λ_D **from Kodaira fibre data**, which is retracted *and* category-mismatched. Obstruction 2
is structural, not a missing computation.

**F5b is not a refutation.** The hypothesis was not tested and found false — it is
*under-constructed* at the level an empirical test requires. It is pre-authorized by `VISION.md`
§4/§5 as a reportable result, and it is **reversible**: exhibit a flux stabilization plus a
non-fibration route to the dark gauge sector, and S3-00 reopens.

---

## 🟡 Stream 3 — Empirical: WP-E5 executing, correctly scoped as engineering

The earlier memo's account of the pivot is right: legacy Δ-spikes, 3D photometric illusions, and
weak-lensing κ-peaks were all abandoned, the last for lack of public shear data. Two corrections.

**The statistic is β₁, not β₂.** In the transverse projection Stream 3 adopted, H₂ is trivial for
a 2D complex, so **β₂ ≡ 0 identically**. β₁ (loops) is the correct 2D analogue of voids. The
switch was forced and right — but it reverses Stream 3's own directive E2.10 (which banned β₁ as
a sensitivity floor, citing baseline-artifact sensitivity), so E2.10 needs amending **in writing**,
and σ(0) for β₁ must be reported numerically rather than merely asserted under a threshold.

**"Unblinded test with Gate G1-L open" is not a near-term step.** G1-L requires both a valid pin
*and* a populated `PREDICTION.md` §6. Because F5b fired, §6 will not be populated on the
cooper_s7 branch, so **G1-L will not open on this branch** — by design, per
`NO_PREDICTION_BRANCH.md`. The WP-E work is therefore correctly labelled
**`[SYNTHETIC-BOUNDING]` / ENGINEERING-only**: it characterizes what the data *could* resolve. It
is not, and must not be reported as, a test of any hypothesis.

**What WP-E5 can deliver:** a bounding box on where a chameleon-like signal would be detectable
against cosmic variance. That is genuinely valuable — it constrains the space any future
mechanism must live in, and it is publishable as methodology. **What it cannot deliver:** a
confirmation, because there is no pinned prediction to confirm.

---

## Roadmap — what is actually left

**1. Finish WP-E5 (Stream 3, active).** Output: `WP_E_EMPIRICAL_BOUNDS.md`, labelled
ENGINEERING/`[SYNTHETIC-BOUNDING]`. Five review items are still open and are listed in the
companion brief — one of them (a shell guard that skips instead of halting) is a real bug.

**2. Two T0 decisions (yours, blocking nothing but pointing at nothing).**
   - Does `v0.4.0` still mean "Gate E PASS"? That event may now be unreachable — redefine or retire.
   - Amend or formally strike `EXECUTION_PLAN.md` §S3-00 step 2(b). F5b stands without it either way.

**3. Publication of the Tier A mathematics — the realistic near-term output.** This does not
depend on the physics resolving: `L₃ = Sym²(L₂)` (kernel-proven); L₃ irreducible ⇒ minimal-order
Picard–Fuchs operator (exact in ℚ, with negative controls); **ρ = 19, T = 3**; the s7-partner
integrality mechanism; exact Riemann schemes, Fuchs Σ = 6, MUM at 0, W(L₃) = W(L₂)³; the A–vS
identification with explicit projective K3 models. Venue: a mathematics or math-physics journal,
not PRL/Nature Astronomy — there is no empirical claim attached.

**Not on the roadmap:** M2 (gated, D2), the unblinded test (G1-L closed by F5b), and any
dark-energy claim (renounced as standing policy, D4 / `ASSUMPTIONS.md` A-DE).

---

## What would change this picture

The physics branch reopens if either obstruction lifts: an explicit flux stabilization fixing
(𝒱, g_s), **or** a derivation of α_D and Λ_D from ρ/T plus the modular data (level 7, disc −7,
Γ₀(7)+) instead of from fibre content. The second is a well-posed question for Deep Think and is
the specific ask in the debrief sent this evening. Neither is scheduled, and neither should be
assumed.

---

**Generated-by:** Stream 2 (Sonnet 5) | **Verified-by:** every claim traced to a primary document —
`ESCALATIONS.md` E-007/E-009/E-011/E-012/E-013/E-015, `PREDICTION.md` v1.1 §6,
`briefs/T0_DECISIONS_2026_07_26.md` (D2, D4),
`briefs/T0_AUTHORIZATION_EXECUTED_AND_S1_13_CORRECTION_2026_07_26.md` (§3, §4),
`briefs/STREAM2_TO_STREAM3_WPE_SEQUENCE_REVIEW_2026_07_26.md` (A–E),
`stream3_mirror/NO_PREDICTION_BRANCH.md` (G1-L) | **Reviewed-by:** Xavier (T0) — pending
