# GATE-C-SELECT: Final Decision — Top 3 for Phase 8.D

**Date:** 2026-07-14 · **Decision:** Novel-heavy · **Authority:** HUMAN (user)

## Selected finalists

1. **t103** (OEIS A276536) — in-session sieve discovery, Phase 8.A/8.B
2. **cooper_s7** (OEIS A183204) — Cooper 2012 level-7 sporadic
3. **cooper_s10** (OEIS A005260) — Cooper 2012 level-10 sporadic

Rationale (user directive, "Novel-heavy"): prioritize the strongest in-session
discovery alongside two independently literature-anchored Cooper sporadics,
rather than defaulting to the most heavily pre-anchored set. All three passed
every Phase 8.B gate (G1-1 through G2-4) with no BLOCKED entries.

## Correction carried into Phase 8.D (Rule 4, honest reporting)

Phase 8.B's G1-4 monodromy output used the field name `det_err = |det(M) - 1|`
and an inline comment calling it a "symplecticity" check. For all three
finalists, several singular points have **det(M) = -1** (det_err ≈ 2.0), not
det(M) = +1. This is **not a defect or a failed check** — by Abel's/Liouville's
formula, det(M) at a regular singular point equals exp(2πi × residue of
−Q_{m-1}/Q_m there), and a residue with half-integer part legitimately gives
det(M) = -1. It only means the local monodromy flips orientation, a normal
feature of order-3 Fuchsian operators. The mislabeling ("symplecticity") has
been corrected in `scripts/k3_monodromy_verification.py` (2026-07-14); no
Phase 8.B verdict changes as a result — `monodromy_computable` only required
the singular point to be regular and the integration to converge, which held.

## Phase 8.D deliverables (this session)

- **D-1 Lean kernel verification** — `lean4_formal_proofs/Structures/{CooperS7Recurrence,CooperS10Recurrence,T103Recurrence}.lean`. Each: exact-integer shift recurrence (order 2 for both Cooper sequences, order 4 for t103 — t103's minimal SHIFT recurrence needed a wider search window ρ≤4/δ≤8 than its Phase 8.B ODE-based K3 classification used), `decide`-proved for n ∈ [0,20] with **zero `sorry`**, general law as an explicit `axiom` (matching the established `S20Recurrence.lean` pattern). All three verified independently to n≈200 by direct Python computation before Lean formalization. `lake build` succeeds for all three; `#print axioms` confirms the `_checked` theorems rest only on Lean's standard foundational axioms (`propext`, `Classical.choice`, `Quot.sound`) — no hidden dependency on the general-law axiom.  
  **Extended in this session:** `CooperS7Recurrence.lean` and `CooperS10Recurrence.lean` now also contain `cooper_s7_pos`/`cooper_s10_pos` (all `Fin 20` values strictly positive) and `cooper_s7_monotone`/`cooper_s10_monotone` (strict monotonicity over `Fin 19`), both kernel-verified by `native_decide`.
- **D-2 CI integration** — `scripts/cross_consistency_check.sh` extended with a "Phase 8.D: GATE-C Finalist Lean Kernel Verification" section that actually runs `lake build` on all three files (not just greps for a filename) plus a pool-freeze check. Full suite: 28/28 PASS.
- **D-5 gate verification dossier (Cooper)** — `docs/autoresearch_v2/COOPER_K3_GATE_VERIFICATION.md` created, summarizing G1-1/G1-2/G1-3/G1-4 and G2-1/G2-2/G2-3/G2-4 results for `cooper_s7` and `cooper_s10` with data sources and honest interpretation.
- Structural observation (not a physics claim): all three finalists' shift recurrences have a clean cubic leading coefficient — (n+2)³ for both Cooper sequences, (n+4)³ for t103.

## Open for next session (D-3, D-5 remainder, D-4)

- **D-3** Part VII manuscript — skeleton started (`manuscripts_and_proofs/Part_VII_Hypothesis_Foundry_DRAFT.md`), full LaTeX writeup pending.
- **D-5** Observatory targeting dossier — pending; needs the PTA/superradiance numbers from `g2_3_superradiance_bands.json`/`g2_4_obs_screens.json` reformatted per-finalist.
- **D-4** External verification invitations — **NOT executed**: this is an outward-facing action (opening GitHub issues on external community repos) that commits the project's name/reputation externally. Flagging for explicit user sign-off before any such posting, per the "actions visible to others" guidance — not something to do autonomously even under a general "proceed" instruction.
