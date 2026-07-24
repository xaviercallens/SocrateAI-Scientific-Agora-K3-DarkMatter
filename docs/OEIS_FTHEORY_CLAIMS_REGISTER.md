# OEIS ↔ F-Theory Mapping — Claims Register (guardrail-compliant form)

**Date:** 2026-07-24 | **Purpose:** The externally supplied "AI-swarm deep-research output"
(comparative matrix + shortlist) cannot enter this repo as written: it states Tier C physics
with forbidden verbs as fact and contains numbers with no checker provenance. This register
records each claim with its verification status. **A claim graduates out of this register only
via a checker certificate or a refs-pinned citation.**

**House rules applied (epistemic-guardrails):** no numbers from memory; PASS always carries
its order; Tier C requires an in-sentence conjecture marker; the Sym²/Shioda–Inose relation
implies no physics by itself (VISION §1.3).

## Mathematical claims (checkable)

| # | Claim (as supplied) | Status | Evidence / required action |
|---|---|---|---|
| M1 | A183204 (Cooper s₇) min ODE order 3, K3-type | ✅ **VERIFIED** Tier B | Golden control in `check_min_ode_order.py` (order-2 refused, order 3 found); consistent with C3b-SYM bulk role |
| M2 | A112019 min ODE order **2** despite order-3 shift recurrence | ✅ **VERIFIED** Tier B, `PASS(58)` | `data/certificates/MINODE_A112019.json` (deg-5 ODE, orders<2 excluded to deg 8, min recurrence order 3) |
| M3 | A005258 (Apéry ζ(2)) order-2 / elliptic | ✅ **VERIFIED** Tier B | refs-frozen recurrence + golden test (min ODE order 2) |
| M4 | A005259 (Apéry ζ(3)) order-3 K3 (Beukers–Peters) | ⏳ **NOT IN REFS** | Literature-solid but unusable here until fetch+hash into `refs/` + checker run |
| M5 | A002893 order-3 K3-type | ❌ **REFUTED** Tier B, `PASS(43)` | `data/certificates/MINODE_zagier_sporadic_A_A002893.json`: min ODE order **2** (deg 3; orders<2 excluded to deg 8) — elliptic-type, corroborating refs typing; the supplied "K3 Base / order-3" row is wrong |
| M6 | A112019 mirror map q₂ = 81/8 (fractional) | ❌ **UNVERIFIED** | No checker computes A112019's mirror map yet; extend mirror-map machinery to its order-2 ODE operator |
| M7 | A005258 mirror map q₂ = 27/4 (fractional) | ❌ **UNVERIFIED** | Same machinery; runnable from refs recurrence — queued |
| M8 | A002893 Picard rank ρ ≥ 19 | ❌ **UNVERIFIED, from memory** | No certificate; forbidden to cite until computed |

## Physics claims (Tier C — conjecture markers mandatory; none may use *certifies/provides/drives/successfully explains*)

| # | Claim (as supplied) | Compliant restatement |
|---|---|---|
| P1 | s₇ "provides the rigid background necessary to drive cosmic expansion via the Atiyah–Singer trace anomaly" | **[C] We conjecture** a dark-energy role for the s₇ K3 background **if** an EFT matching (nonexistent today) is constructed; no checker or derivation supports "drives" |
| P2 | A112019 "is the perfect EFT for localized DM subhalos… Chameleon mechanism successfully explaining dwarf cores" | **[C] We conjecture** an elliptic-fiber subhalo role; "successfully explaining" is unsupported — no comparison to data has been run (that is Stream 3 S3-03/04's job, post-PREDICTION-pin) |
| P3 | Fractional mirror map = orbifold/orientifold quotient signature | **[C] Hypothesis**, checkable in principle (monodromy computation) — currently unverified (M6/M7 prerequisite) |
| P4 | "Synthesis of A183204 + A112019 provides a mathematically complete, observationally verifiable vacuum" | **Refused as stated** — "complete/verifiable" presupposes the S3-00 MVM derivation and Gate-E empirics that have not happened |

## Shortlist status

No shortlist can be issued from this register yet: the supplied "winners" rest on M6/M8 (unverified)
and P1–P4 (Tier C). The candidate decision lives in `K3_SELECTION_REPORT.md` §3 (T0-PENDING),
which uses only checker-verified rows.

Generated-by: Stream 2 (Fable 5) | Verified-by: certificates cited inline | Reviewed-by: T0 pending
