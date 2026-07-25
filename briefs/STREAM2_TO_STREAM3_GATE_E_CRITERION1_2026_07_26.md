# Stream 2 → Stream 3: Gate E Criterion 1 — Scored UNRESOLVED (T0 decision D1)

**Date:** 2026-07-26 · **Authority:** Xavier (T0), decision D1 in `briefs/T0_DECISIONS_2026_07_26.md`
**Action required by Stream 3 before the 2026-07-27 EOD verdict.**

## What changed

The lattice prior your D-3 batch was parameterized with — **ρ = 4, T = 18** from
`data/certificates/C2_cooper_s7_partner.json` — is **permanently withdrawn** (E-007:
the value traces to a hardcoded `components = 2` in a retracted lookup, not to
geometry; E-008: no replacement derivation exists yet). Full detail: `ESCALATIONS.md`.

## What to do at aggregation / verdict time

1. **Do not score criterion 1 as PASS or FAIL.** Score it **UNRESOLVED** in
   `D3_AGGREGATE_VERDICT.json` / `D3_GATE_E_VERDICT.md`, citing E-007 and T0 decision D1.
2. **Score the other five criteria normally** on their own evidence
   (operator numerics, mirror-map, s7/s10 pass rates against their own nulls,
   physics-washing audit). The batch is not discarded.
3. **Retain, do not delete, the criterion-1 outputs** (`lattice_chi2`,
   `picard_estimate`, `transcendental_estimate` per sector). They are data. If Route γ
   later yields a *derived* prior, they can be re-scored against it without re-running
   the batch. Until then they must not be compared to ρ=4/T=18 as if it were a
   certified target.
4. **Verdict framing:** under the pinned logic, the best achievable outcome on
   2026-07-27 is **CONDITIONAL** (≤5/6 scoreable). State this in the verdict header
   rather than letting it surface as a surprise.

## One more request (T0 decision D3)

Mirror into this repo, hash-pinned: `docs/WP_R6_SURVEY_SCALES.md`,
`docs/WP_R7_BETA_VARIANCE_SCAN.md`, `NO_PREDICTION_BRANCH.md`,
`check_tier_language.py`, `pipeline/siblings.py`. Phase M's M2 cannot open without
them (and without Route γ).

**Generated-by:** Fable 5 (T1, executing T0 decision D1/D3) | **Verified-by:** ESCALATIONS.md E-007/E-008 | **Reviewed-by:** Xavier (T0) authorization 2026-07-26
