# T0 Decision Request: G1 B₂ Ladder, Post-Convergence (2026-07-28)

**Status:** DECISION-REQUEST. Two fully independent derivations now agree the plan's original
B₂ ladder is obstructed for the naive-pullback construction. This document lays out what's
settled, what's still open, and the concrete options — no option is executed until you rule.

## What's settled (two independent routes converge)

1. **Deep Think (T0s), external, zero-shot** (`briefs/DEEPTHINK_DEBRIEF_AUDIT_2026_07_28.md`
   §C2, S3, audited/hand-verified by the coordinator): strict pullback needs K²(B₂)=0;
   P²(9), P¹×P¹(8), F_n(8) all fail.
2. **In-house G1-a agent, exact symbolic checker, deliberately not shown Deep Think's finding**
   (`briefs/G1a_CY_CONDITION_RESULT_2026_07_28.md`, this repo, commit `d6146c4`): the same
   conclusion, proven exactly and unconditionally in ℓ (the family's own Hodge-bundle degree,
   left uncomputed), plus an additional, stronger result — no map φ: P² → any curve exists at
   all (Picard-lattice isotropy argument, corroborated by Bezout), so P² is not merely
   K²-obstructed but categorically inadmissible.

Both routes independently land on **dP9 (degree-9 del Pezzo)** as the natural next candidate
— Deep Think proposed it as a fix; the in-house checker's own positive control (built to prove
the checker isn't a stub) landed on it independently and solved its Hodge-bundle degree
exactly (ℓ=1, matching the classical rational-elliptic-surface fact).

**Coordinator assessment: this convergence is strong evidence the naive-pullback construction
on the original ladder is genuinely dead**, not an artifact of either derivation.

## What's still open (neither route resolved these)

- **O1 — the actual Hodge-bundle degree ℓ for the cooper_s7 family's own map to X₀(7)+ is
  uncomputed.** The in-house dP9 control found ℓ=1 for dP9's *own* generic fibration (a
  sanity-check input), not for cooper_s7 specifically — this does not transfer.
- **O2 — Deep Think's proposed dP9 fix conflicts with its own even-ramification proposal**
  (audit §C3): a dP9 admitting a section has no multiple fibers, leaving no room for the
  ramification-index trick Deep Think separately proposed for G1-b. Unresolved.
- **O3 — Halphen (index-2, multiple-fiber) variant**, floated as a possible reconciliation of
  O2, has a parity concern (audit §C3), sketch-level only.
- **The "twisted Weierstrass" escape hatch is untested by both routes.** The plan's own G1-a
  bullet gestures at this as an alternative to naive pullback (constructing X₄ directly via
  twisted sections on B₂, rather than factoring through a fixed map to the z-line) — neither
  Deep Think nor the in-house checker attempted it; it would need an explicit Weierstrass-type
  presentation of the M-polarized family directly on B₂, a larger undertaking.
- **G0's U-summand argument is certified fiberwise only** (its own stated caveat) — if the
  ladder moves to a non-simply-connected base (K3, abelian, bielliptic — all K²=0 candidates),
  that argument may need re-deriving; untouched by anything done today.

## Options

**Option 1 — Revise the ladder to K²=0 surfaces, continue naive pullback.** Candidates: dP9
(rational elliptic surface, both routes' preferred first try), other rational elliptic
surfaces, K3, abelian, bielliptic. Next step would be resolving O1 (compute ℓ for cooper_s7)
before re-running the G1-a checker on the new candidate — if ℓ≠1, dP9 itself may fail too, so
O1 is now load-bearing for this option and should be computed first, cheaply, before any further
ladder rung is attempted.

**Option 2 — Pursue the twisted (non-pullback) construction instead.** Larger undertaking,
untested by anyone yet; would need its own scoping pass before a T1 agent could attempt it.

**Option 3 — Both, in parallel, on separate rungs** (the plan's own "ladder" framing already
anticipates parallel rungs with independent stop conditions).

**Option 4 — Treat today's convergence as a sufficient structural-negative result and pause
Route A**, filing it as a documented dead end per house style ("a documented dead end beats an
undocumented detour") pending a strategic review rather than immediately continuing.

**Coordinator has no recommendation to force here** — Option 1 is the cheapest next step and
both independent reviewers gravitated toward dP9, but O1's uncomputed status means even that
"obvious" choice isn't guaranteed to clear on the first try, and Option 2 may be the more
durable path if the plan's own twisted-Weierstrass framing was always the intended mechanism.
This is a strategic call, not a mechanical one.

## Sources

- `briefs/G0_NS_GENUS_RESULT_2026_07_28.md`, `briefs/G1a_CY_CONDITION_RESULT_2026_07_28.md`
- `briefs/DEEPTHINK_DEBRIEF_AUDIT_2026_07_28.md` (S3, canonical audit; do not cite the inbound
  verbatim archive directly)
- `briefs/WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md` §8 decision log (updated this session)

---
Generated-by: Fable 5 (coordinator) | Verified-by: G1-a's F_n canonical-class formula
independently re-derived from scratch by the coordinator (adjunction, not read from the
checker) — matches; all 5 controls independently re-run — PASS | Reviewed-by: T0 N (this
document is the review request)
