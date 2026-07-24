# 🔬 Phase 10: Shioda–Inose Selection & Core Prioritization

> Numbered Phase **10** to avoid collision with the existing Phase 8 (AutoEvolve Gate Battery,
> complete) and Phase 9 (Observable Redesign, in progress) in `PROJECT_STATUS_TRACKER.md`.
> This is the discriminator/selection workstream that follows the C3b partner-identification blocker.

**Status:** active · **Owner:** Stream 2 (Theory & K3 Selection) · **Handoff from:** Stream 1 (math kernel)

> Epistemic note: claims below are tagged **[A]** established/certified math, **[B]** checkable
> but unproven (carries a verification route), **[C]** physical interpretation (conjecture marker
> required in-sentence). See the tier rules in `.claude/skills/epistemic-guardrails`.

## 1. Relieving the Stream 1 Burden

**[A]** Stream 1 established that the vanishing of the Almkvist–van Straten invariant
(W ≡ 0) holds structurally for the entire Cooper ansatz. **[B]** Consequently, checking
W ≡ 0 is evidence of K3-type geometry but is **non-discriminating** between s₇ (A183204)
and s₁₀: it takes the same value on both, so it cannot select between them. Stream 1's role
in candidate *selection* is therefore complete; the burden of active candidate discrimination
shifts to Stream 2.

## 2. Active Discriminators (computational tasks)

To break the geometric degeneracy, the Python/SymPy pipeline computes non-structural criteria.
These are **[B]** — checkable but unproven — and must be reported with their verification order:

1. **C3b (Shioda–Inose moduli map):** find the explicit second-order partner operator L₂ such
   that L₃ = Sym²(L₂). Report as `PASS(N)` at the order N to which the mirror map / relation is
   verified — never bare `PASS`. **[C]** *We conjecture* that an established Sym² relation would
   correspond to a Shioda–Inose structure on the associated K3; the geometric relation on its own
   implies **no** bulk↔brane physical coupling absent a worked EFT matching (see §4).
2. **C1/C2 (Kodaira fiber classification):** extract the intersection matrix of the K3
   transcendental lattice. **[B]** This constrains admissible D-brane gauge-group embeddings.
   Any statement that a particular embedding *is* realized is **[C]** and must carry a conjecture
   marker in the same sentence.

## 3. Computational Priority Target: Cooper s₇

**Priority ranking — mathematical/operational grounds (load-bearing):** s₇ (A183204) is the
Cooper sequence that has been *executed and validated* end-to-end in the checker framework
(recurrence reproduces its own terms; mirror map computed to order 24+). Because it is the
partner-mapping candidate with a validated certificate in hand, Stream 2 prioritizes computing
the L₂ partner of **s₇** over s₁₀. This ordering is a resourcing decision and does not by itself
assert that s₇ is physically preferred.

**Empirical context (NOT load-bearing here):** s₇ was flagged as a leading candidate in the
V4C/SDSS-DR17 exploratory analysis, but that pipeline inherits defect A4 (the discovery logger
cannot distinguish real from synthetic SDSS inputs) and defect A7 (non-reproducible headline
numbers). **No empirical dominance claim is used to justify the priority above**, and none should
be cited as fact until re-sourced under a Stream-3 quorum re-run (DM-3).

**[C]** *We conjecture* — as a physical hypothesis to be tested by the gate battery, not a result —
that if a Shioda–Inose partner for s₇ exists and a worked EFT matching is constructed, the
resulting background *could* support a realistic GUT-scale gauge sector (e.g. SU(5) or SO(10)).
No such embedding is constructed or verified; this is a Tier-C target, not a finding. Any promotion
requires the EFT matching of §4 plus a T0 tier ruling in `TIER_LEDGER.md`.

## 4. Binding constraint: geometry ≠ physics

The Sym² / Shioda–Inose relation is a statement about differential operators and lattices. It does
**not** "link", "lock", "couple", or "govern" the bulk-to-brane EFT. Any physical coupling claim
requires a separately worked EFT matching and must be written with an explicit conjecture marker.
This paragraph is binding on all downstream prose derived from this brief.

## 5. Interface pointers

- Honest cross-stream number interface: `data/interfaces/pipeline_bound_v1.json` (+ `.sha256`),
  imported by Stream 1 as `hypothesis_pipeline_upper_bound` — a **hypothesis**, `must_not_be_imported_as: axiom`
  (S1-1; A7 provenance). Promotion gated on DM-3.
- Checker certificates are the sole source of candidate numbers (see `criteria-checkers` skill).

---
Generated-by: Opus 4.8 (Tier B/C prose) | Verified-by: pending checker certificates for C3b `PASS(N)` | Reviewed-by: pending T0
