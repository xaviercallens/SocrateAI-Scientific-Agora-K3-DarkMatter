# Stream 2 → Stream 1: E-009 Status — No New Required Work

**Date:** 2026-07-26 · **Authority:** Stream 2 finding, informational
**Action required by Stream 1: none.** Written because E-009's resolution touches the s18 item that was
sitting in your optional-work list, and it's worth being explicit about why it still isn't actionable.

## What changed

E-009 is RESOLVED — the K3 exists, explicitly constructed for s7 and s10 (Almkvist–van Straten
arXiv:2103.08651v1; see `ESCALATIONS.md` E-009 and `briefs/STREAM2_TO_STREAM3_E009_RESOLVED_2026_07_26.md`
for the full finding). As a byproduct, s18 — corrupt in `refs/recurrences_v1.json` since 2026-07-20 — is
recovered: A-vS's "Sporadic 3" gives the correct operator directly and it regenerates the published
sequence (1, 6, 54, 564, 6390, 76356, 948276) exactly.

## Why this does not open new Lean work

`TODO.md` currently lists "optional: s18 recurrence recovery — unblocked by the Phase 1 Gorodetsky fetch"
under your maintenance items. That line is now **superseded, not activated**:

1. **The recovery came from a different source than expected** (Almkvist–van Straten, not the Gorodetsky
   re-transcription Stream 2 attempted on 2026-07-25 and left blocked). Folding the corrected operator into
   `refs/recurrences_v1.json` is a refs-register edit — Stream 2 housekeeping, not a proof task.
2. **Your L₃=Sym²(L₂) proofs for s7/s10 were only possible because an order-2 companion operator was
   identified** — A279619 (disc −7 weight-1 form) for s7, verified as the exact square root of A183204's
   generating function. **No order-2 companion for s18 has been identified in anything fetched so far.**
   A-vS's sporadic-operators section documents s18 as order-3 only; it does not name a weight-1 partner.
   Without that companion there is nothing to state as a Sym² claim, let alone encode in Lean.

So the honest status is: s18 has a recovered order-3 operator (Stream 2's to fold in), but not yet the
order-2 counterpart your Lean pattern (`B1_Sym2Bridge.lean` et al.) depends on. If Stream 2 later finds or
rules out such a companion, that would be the trigger for a Stream 1 task — flagged here for awareness
only, not authorized.

## Unchanged

- Your one open T0 item remains **WP-B1 sign-off** (`briefs/STREAM1_WP_B1_RESULTS.md`) — unrelated to
  E-009, still pending per `TODO.md`.
- The other maintenance item ("tighten `h_scale` in `no_unscreened_lmp` once C1 v3 lands") is still not
  actionable — C1/C2 v3 has not landed; per the Stream 3 brief above, ρ/T are still `null` pending the
  Stienstra–Beukers 1985 citation.

**Generated-by:** Sonnet 5 (Stream 2, informational follow-up) | **Verified-by:** `ESCALATIONS.md` E-007/E-009, `refs/literature_provenance.txt` | **Reviewed-by:** Xavier (T0) — pending
