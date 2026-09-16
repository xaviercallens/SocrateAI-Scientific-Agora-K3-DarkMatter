# LR-3 Extended Sieve Results — 2026-09-16

**EXPLORATORY SANDBOX artifact** — Track B (AutoEvolve R2 Hypothesis Foundry / K3-T2 track,
`CLAUDE.md` rule 7). Not citable into Streams 1–3 or any Tier A/B/C claim. Session continues
Phase A of `AUTORESEARCH_IMPLEMENTATION_GUIDE.md` on branch `sandbox/autoevolve-r2-phase-a-2026-08-01`.

## What ran

`scripts/autoresearch_v2_phase_a_scan.py` (pre-existing, unmodified) in `scan2` and `scan3`
modes — exact-arithmetic ODE/shift-recurrence classifier, held-out validated to n_max=110 with
two independent 62-bit-prime modular pre-screens before an exact `Fraction` solve. Per §LR-3
acceptance criterion, no relation is reported without an exact held-out pass; no non-zero
residual occurred in this run.

- **2-factor**, (A,B) ∈ [1,8]²: `data/autoresearch_v2/phase_a_scan2.json`
- **3-factor**, (A,B,C) ∈ [0,3]×[0,3]×[1,3]: `data/autoresearch_v2/phase_a_scan3.json`
- Consolidated: `data/autoresearch_v2/sieve_scan_extended.json` (LR-3's specified output path)

## Findings

**2-factor grid:** no new order-3/K3-type survivor. Only S(2,2) = A005259 (the known literature
anchor) reaches ODE order 3; every other of the 64 combinations is order ≤2 (elliptic/rational)
or has no ODE in the search window (ρ≤4, δ≤8).

**3-factor grid:** 4 order-3/K3-type survivors, one already known:

| (A,B,C) | ODE (order,deg) | Identity | Status |
|---|---|---|---|
| (1,0,3) | (3,6) | A276536 = **T103** | Known GATE-C finalist — sieve independently re-derives its existing classification (cross-check PASS, not a new find) |
| (0,0,3) | (3,4) | **A079727**, Σ C(2k,k)³ | **New** to this program's pool |
| (0,1,1) | (3,6) | **not in OEIS** (search returned no results) | **New**, genuinely unlisted integer sequence |
| (1,1,2) | (3,8) | **A274789**, diagonal of 1/(1−(wxyz+wxy+wxz+wy+wz+xy+xz+y+z)) | **New** to this program's pool |

**Follow-up G1-2 (Weil bound) run** on the 3 new survivors (`scripts/lr3_g12_weil_screen_new_survivors.py`,
new script this session, weight-3 Ramanujan–Petersson bound |a_p| ≤ 2p, reusing the
Stienstra–Beukers unit-root recipe already documented in `modularity_screen.py`, not
re-derived): **all 3 pass, 0 failures across 44 primes each** (`data/autoresearch_v2/g1_2_weil_new_survivors.json`).

## What this is NOT

ODE order 3 + Weil-bound pass is necessary, not sufficient, for K3-type geometry — see
`S12_S21_DEFINITION_ALIGNMENT.md` for the companion case (S₁,₂) where this same classifier's
order-2 result correctly excludes K3, establishing the classifier discriminates in at least one
direction. None of the 3 new survivors have run G1-3 (mirror-map integrality), G1-4 (monodromy),
or G2-* (physics viability). **Not promoted to `candidate_pool.yaml`; no HUMAN gate has seen
these.** Per rule 4 (verify before executing further), the honest next step if continued is
G1-3 on these 3, not a pool promotion.

## Also produced this session

`docs/autoresearch_v2/s12_s21_oeis_match.md` (LR-1 output) — independent from-scratch
re-derivation (direct binomial-sum computation, not by reading the prior doc first) confirming
the existing 2026-07-14 finding (`S12_S21_DEFINITION_ALIGNMENT.md`): S₁,₂ = A112019 and
S₂,₁ = A005258 are both elliptic (order-2), not K3 — corrects the guide's own anticipated
"key finding," which is superseded by this repo's later, more careful classification.

---
*Generated-by: Claude Sonnet 5 (T1 executor, sandboxed) | Verified-by: exact integer arithmetic,
held-out validated; OEIS matches confirmed via direct oeis.org search, not typed from memory |
Reviewed-by: pending T0*

## T0 Ruling — 2026-09-16

**A079727 — HOLD on G1-3 (mirror integrality) and G1-4 (monodromy).** No further gate runs on
A079727 until it is analytically checked for being a partial sum / twist of a known
hypergeometric family (it is Σₖ₌₀ⁿ C(2k,k)³) rather than new geometry. The other two new
survivors (the OEIS-unlisted (0,1,1) sequence and A274789) were not ruled on; nothing is
promoted to `candidate_pool.yaml`. Ruled by T0 (Xavier Callens) in session; recorded by Claude
(Opus 5). Mirror: S3 `briefs/T0_RULINGS_2026_09_16.md` §B1.

Generated-by: Claude (Opus 5) | Verified-by: n/a (ruling record) | Reviewed-by: T0 Y
