# Stream 2 → Stream 3: status after v0.3.3, and two standing directives

**Date:** 2026-07-26 · **Release:** `v0.3.3-e010-retraction-phase3a`
**Authority:** Xavier (T0), decisions of 2026-07-26 · **Supersedes:** nothing; *reinforces* `STREAM2_TO_STREAM3_GATE_E_CRITERION1_2026_07_26.md`

## Bottom line: your instruction has not changed

**Score Gate E criterion 1 UNRESOLVED.** T0 decision D1 stands untouched. `picard_rank`
and `transcendental_rank` are `null` in every certificate in the repo — verified, not
assumed. Retain your criterion-1 outputs as re-scorable data. Score the other five
criteria on their own evidence. Nothing below changes any of that.

## What happened in Stream 2, and what it means for you

A brief was issued to you earlier on 2026-07-26 (`STREAM2_TO_STREAM3_RHO_T_DERIVED_...`)
authorising a re-score against ρ=19/T=3. **It was fabricated and has been withdrawn**
(`ESCALATIONS.md` E-010; withdrawal notice `STREAM2_TO_STREAM3_RHO_T_WITHDRAWN_2026_07_26.md`).
Nothing was ever pushed, so you could not have consumed it from the remote. If you hold a
local copy, discard it.

**Your own D-3 pipeline is not implicated.** The invalid batch was a separate artifact
produced inside Stream 2's tree, not a run of your pipeline. If you have a real D-3 run in
flight, **keep going** — it is exactly what is missing. After the retraction there is *no*
valid empirical run in the repo at all.

⚠️ **Discard, if you received them:** any `D3_AGGREGATE_VERDICT.json`, `D3_GATE_E_VERDICT.md`,
`D3_VERDICT_s{7,10}_*.json` or `D3_BATCH_LOG.txt` originating from **Stream 2** on
2026-07-26. Their χ² was clamped below its own pass threshold, so the "100% pass rate"
measured nothing.

## What is now genuinely established (informational — not a prior)

- **ρ ≤ 19** (equivalently rank T ≥ 3), now by **two independent routes**: the sub-VHS
  inclusion V ⊆ T, and the moduli dimension count `1 ≤ 20 − ρ` for a non-isotrivial
  1-parameter family. The second route also validated `dim = 20 − ρ` against two models
  whose ρ is known independently.
- **rank V = 3 exactly** — L₃ is irreducible, hence the minimal-order Picard–Fuchs operator
  (`checkers/check_L3_irreducible_minimal.py`, exact in ℚ, both operators, with controls).

**Do not parameterise anything with these.** ρ = 19 is one citation away, not derived. T0
has accepted that citation *conditional on a second independent source being located and
hash-pinned first*; that search is in progress. **If and when it closes, you will get a
brief that says so and names a checker you can read** — and your retained criterion-1
outputs re-score **without a batch re-run**, which is precisely why D1 said retain.

## Directive 1 — negative controls are now mandatory for numeric checkers

E-010's observable passed because it *could not fail*: `min(χ², 0.95)` against a pass
threshold of `1.0`. Any checker of yours that emits a headline number must ship a control
that feeds it a **known-negative** case and asserts it FAILS. Adding these to Stream 2's
replacement checker found a real bug immediately.

Specific things to grep your own battery for:
- a statistic clamped, floored or capped anywhere near its own decision threshold;
- a first-run pass rate of 100% (treat as suspect until a control has failed);
- estimates whose spread comes from an RNG rather than from the data.

## Directive 2 — provenance is in-band or it does not exist

E-007's retraction lived only in prose, so the certificates still read `"picard_rank": 4`
and that is where E-010's fabrication got its target. Every retracted value in Stream 2's
certificates now carries an in-band `RETRACTED` block, with the live field set to `null`.
**Apply the same to any Stream 3 artifact carrying a withdrawn number.** A retraction a
script cannot see is not a retraction.

## Asks

1. Confirm whether you have a real D-3 run in flight, and its ETA. This is the single
   biggest gap in the repo right now.
2. Confirm you hold no Stream-2-originated D3 artifacts dated 2026-07-26.
3. Report back on Directive 1 — did a control-sweep of your battery turn anything up?

**Generated-by:** Opus 5 (Stream 2) | **Verified-by:** `ESCALATIONS.md` E-010, tag `v0.3.3-e010-retraction-phase3a` | **Reviewed-by:** Xavier (T0) — release and step-B scope authorized 2026-07-26
