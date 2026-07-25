# Stream 2 → Stream 3: E-009 Resolved — the K3 Exists (informational; Gate E criterion 1 scoring UNCHANGED)

**Date:** 2026-07-26 · **Authority:** Stream 2 finding, informational update to `briefs/STREAM2_TO_STREAM3_GATE_E_CRITERION1_2026_07_26.md`
**Action required by Stream 3 before the 2026-07-27 EOD verdict: none new.** This brief exists so the
resolution doesn't surface as a surprise mid-verdict and to say plainly what it does and does not change.

## What changed

**E-009 is RESOLVED.** The category worry raised on 2026-07-26 — "maybe there is no K3 at all and the
fibration reading is a mirage" — is answered: **there is a K3, explicitly constructed in the literature.**

Fetched **Almkvist & van Straten, arXiv:2103.08651v1**. Its section "the three sporadic third order
operators" *is* our s7/s10/s18 (their own words: "also found by S. Cooper, where they are called s10, s7
and s18"). They give explicit constructions:

- **s7** → K3 = intersection of six hyperplane sections of the Grassmannian G(2,6) (Plücker embedding)
- **s10** → K3 = intersection of four (1,1)-type hyperplane sections in P³×P³

Their *printed* Riemann symbols and operator coefficients match this repo's independently-computed values
exactly, at all four singular points, for both operators — external validation of the whole computation
chain, not just the existence claim. Full detail: `ESCALATIONS.md` E-009.

**Bonus:** s18 (blocked/corrupt in `refs/recurrences_v1.json` since 2026-07-20) is recovered from the same
source. This is a Stream 2 housekeeping item (folding the corrected operator into the refs register); it
does not touch anything Stream 3 is running.

## What this does NOT change

**Gate E criterion 1 is still scored UNRESOLVED for the 2026-07-27 EOD verdict, per T0 decision D1.**
Nothing here reverses that. Reason: A–vS state **no Picard number**. The K3 existing tells you the
geometry is real; it does not hand you ρ or T. `picard_rank` and `transcendental_rank` remain `null` in
every certificate. The standing rule (`ESCALATIONS.md`) is explicit: **emit no ρ and no T until one is
derived.**

Concretely, the residual moved from **[C]** (conditional on an unproven existence claim) to **[B]**
(a standard identification — order-3 sub-VHS = full transcendental lattice — awaiting a citation that
hasn't been fetched yet: Stienstra & Beukers, *Math. Ann.* 271 (1985) 269–304). That is real progress, but
it is not a derived number, so it does not change what you score tomorrow.

**Keep following `briefs/STREAM2_TO_STREAM3_GATE_E_CRITERION1_2026_07_26.md` exactly as written:**
score criterion 1 UNRESOLVED, score the other five criteria on their own evidence, retain the
criterion-1 outputs (`lattice_chi2`, `picard_estimate`, `transcendental_estimate`) as re-scorable data —
do not compare them against ρ=4/T=18 (permanently retracted, E-007) or against ρ=19/T=3 (not yet derived).

## Forward-looking note (no action needed now)

If Stienstra–Beukers 1985 is fetched and confirms the identification, ρ=19/T=3 becomes derived and Stream 2
will emit C1/C2 v3 and notify Stream 3 directly (per `TODO.md` Phase 2/3). At that point your already-retained
D-3 criterion-1 outputs can be re-scored against the derived prior **without re-running the batch** — that
is exactly why D1 said to retain rather than discard them. Until that notification arrives, there is nothing
to do differently.

**Generated-by:** Sonnet 5 (Stream 2, informational follow-up to T0 decision D1) | **Verified-by:** `ESCALATIONS.md` E-009, `TODO.md` Phase 1 | **Reviewed-by:** Xavier (T0) — pending
