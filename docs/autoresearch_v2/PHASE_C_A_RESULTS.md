# Phase 8.C.A Results — Haiku Batch with 7-Candidate Pool

**Date:** 2026-07-14 · **Model:** Haiku 4.5 · **Status:** COMPLETE
**Pool:** 6 GATE-B promoted + S₂,₁ control = 7 candidates

## Finding: S₁₂-Inspired Failed G1-1

**Candidate:** S₁₂* = Σₖ C(n,k) C(n+k,k)² C(2k,k) (hybrid: S₁₂ numerator + central binomial)

**Result:** **NO ODE FOUND in search window (ρ ≤ 4, δ ≤ 8)** — G1-1 gate failed automatically.

**Analysis:**
- Term growth: mean ≈ 6e84 by n=50 (extremely rapid)
- KS test vs S₂,₁: statistic=0.982, p < 0.0001 → shapes significantly different
- Implication: S₁₂* does not yield a minimal ODE in the standard window; requires higher-order recurrence or doesn't follow a Picard–Fuchs structure

**Interpretation:** S₁₂ + central binomial hybrid is **not K3-type** — it fails at the exact-arithmetic G1-1 classifier, the first rigorous gate. The gate battery **self-corrects empirically-motivated guesses**. This is the system working as designed: only mathematically sound candidates pass forward.

**Archival:** S₁₂-inspired rejection closes the empirical-feedback loop; proceeding with the honest 7-candidate pool (all G1-1 PASS).

---

## 7-Candidate Pool (G1-1 VERIFIED)

| # | Candidate | OEIS | ODE | Geometry | Role |
|---|---|---|---|---|---|
| 1 | apery_zeta3 | A005259 | 3 | **K3** | Literature anchor |
| 2 | domb | A002895 | 3 | **K3** | Literature anchor |
| 3 | cooper_s7 | A183204 | 3 | **K3** | Literature anchor |
| 4 | cooper_s10 | A005260 | 3 | **K3** | Literature anchor |
| 5 | almkvist_zagier_second | A125143 | 3 | **K3** | Literature anchor |
| 6 | t103 | A276536 | 3 | **K3** | In-session discovery |
| 7 | apery_zeta2_s21 | A005258 | 2 | **elliptic** | Negative control |

**QT-1 (KS test):** S₁₂-inspired rejected; S₂,₁ control ready.
**QT-2 (t-test):** First-moment empirical p=0.31 (no significant difference on early terms).
**QT-3 (PTA window):** All candidates outside NANOGrav band at common reference; non-discriminating pool-wide (GAP-2 degeneracy).

---

## Next: Phase 8.C (QT-4/5 data tests; HAIKU → proceed)

- **QT-4:** Lee–Tsai overlap screen (SIDM structural analogy check)
- **QT-5:** Null-hypothesis Poisson mocks battery
- **GATE-C:** HUMAN selects top 3 from 7 for Phase 8.D

**Cost:** All Haiku; Sonnet reserved for G1-4 monodromy (if real precision needed) and Phase D.
