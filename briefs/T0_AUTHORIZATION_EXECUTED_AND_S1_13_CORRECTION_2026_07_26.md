# T0 Authorization Executed — and One Correction (WP S1-13)

**Date:** 2026-07-26 · **From:** Stream 1 · **To:** T0 (Xavier), Stream 2, Deep Think
**Responds to:** "🏛️ T0 AUTHORIZATION: Stream 1 Parking & Unblock Queue Cleared" +
Deep Think's adversarial review of S1-10/11/12, both received this session.
**Commits:** `1969e1b`/`49a1e6d` (this repo).

---

## 1. Deep Think's review — accepted

A1–A4 all PASS, independently re-derived (not just re-read), including the same golden
values computed from raw parameters rather than copied from our output. This clears the
two-model bar for `PartnerOperators.lean`/`PartnerIntegrality.lean`/`FormalSqrt.lean`, same
standard as D2/WZ. Thank you — the four attack points were chosen because they were the
places a subtle error would hide, and none did.

## 2. T0 rulings — executed, with one correction

| Ruling | Status |
|---|---|
| WP-B1 sign-off: **APPROVED** | Recorded — `briefs/STREAM1_WP_B1_RESULTS.md`, `TODO.md` (Agora repo) |
| `open_goal_partner_eq_sqrt_s7`: **blocked-on-mathlib** | Concur, unchanged |
| `open_goal_partner_integral_s7`: **blocked-on-mathlib** | **Reopened and closed instead — see §3** |
| Deep Think review: **APPROVED** | Recorded above |
| Literature upgrade (s7 integrality → sourced): **applied, mechanism corrected** | See §3 |
| Literature downgrade (Q6 modular mechanism → [C]): **applied** | Unchanged from S1-12 |

## 3. The correction: `open_goal_partner_integral_s7` is CLOSED, not parked

Before accepting "blocked-on-mathlib" for both goals, I rechecked the premise — the standing
practice this project keeps re-earning the hard way (E-007, E-010). It holds for the bridge
goal. It does not hold for this one.

**The check:** does `partnerSeq s7_params` actually satisfy O'Brien's own recurrence for his
sequence `c₇`? CAS-confirmed exact match — same coefficients, same initial data. Then I read
the actual thesis text (already fetched, hash-pinned by Stream 2) rather than trust Deep
Think's paraphrase of it.

**What was wrong in the citation:** Deep Think named Theorem 6.1, which only proves the
recurrence↔generating-function correspondence — not integrality — and gave the mechanism
as "η-quotients have integer Fourier coefficients, therefore corollary". That argument
doesn't hold in general: `c₇(n)` arises from a **series reversion** of the Hauptmodul `X₇`,
and reversion does not automatically preserve integrality even when both series do. That is
exactly why O'Brien needed an explicit induction rather than a one-line corollary — his own
words: *"it is not obvious… the proof is short but there was a lot of background involved."*
The correct citation is **Theorem 6.2, p.47**.

**What this buys:** Theorem 6.2's *conclusion* can be cited without rebuilding the
modular-forms machinery needed to *derive* it — that machinery establishes O'Brien's
q-expansions, not the use of his already-published theorem. New
`Agora/Axioms/OBrien2016.lean` states his theorem as a literature-sourced axiom (registered
`AXIOMS.md`, same footing as `pipeline_upper_bound`), connected to our object via
`partnerSeq_s7_recurrence` (the mechanical match above, kernel-checked). **The goal is now
closed — a theorem, not `PASS(N)`.**

**Independent convergence, found mid-session:** Stream 2 reached the same correction in
parallel, via a sharper route: `checkers/check_s7_partner_integrality_modular.py`
reconstructs the actual modular parametrization and identifies the real mechanism —
`X₇ = q − 9q² + …` is a *normalized integral uniformizer* (leading coefficient exactly 1),
and reverting a monic integral series never introduces a denominator. That's the general
fact Deep Think's "corollary" was reaching for and missed. Their result is Tier B
(computational); this axiom is what makes the conclusion Tier A in the kernel. Cross-
referenced in the axiom's docstring both ways.

**Also caught and fixed:** `scripts/export_open_goals.py`'s status regex required literal
`:= by`, so this goal's first (term-mode) closure attempt vanished from `open_goals.json`
silently — worse than misreporting, absent entirely. Fixed to match any `:=`.

## 4. Stream 1 status, corrected

**One** open goal remains, not two: `open_goal_partner_eq_sqrt_s7`, genuinely
blocked-on-mathlib (needs operator→solution-sequence transport machinery the pinned Mathlib
doesn't have — this route doesn't touch it, since it's about `partnerSeq` directly, not the
`sqrtSeq` bridge). `lake build` green (3118 jobs), 0 `sorry` outside `OpenGoals/`, 2 axioms
total, both registered. **Stream 1 remains parked**, on a smaller and more accurate open-item
count than the authorization stated.

---

**Generated-by:** Sonnet 5 (Stream 1) | **Verified-by:** Lean kernel (`lake build Agora Tests
OpenGoals`, 3118 jobs); CAS recurrence match; direct read of
`docs/literature/obrien_2016_massey_thesis.txt` lines 2560–2697 (Agora repo) |
**Reviewed-by:** Xavier (T0) — pending; this brief reports a deviation from a just-issued
ruling and should be read as such, not as a unilateral override
