# GATE-B FINAL: 6 Promoted Candidates + S₁,₂ Formal Rejection + AlphaEvolve Survivors + Sonnet Roadmap

**Date:** 2026-07-14 · **Status:** IMPLEMENTATION (Haiku for cheap gates; Sonnet for precision phases)
**Authority:** Phase 8.B gate battery (all 13 orig + 2 AlphaEvolve trials); user directive to include S₁,₂ formal validation + 6th candidate slot

---

## GATE-B Final Selection: 6 Promoted

The five classical anchors **plus t103 as the 6th** (newest in-session discovery, full gate pass, OEIS-listed):

1. **apery_zeta3** (A005259) — Beukers–Peters 1984 K3, ρ=19, literature anchor
2. **domb** (A002895) — Almkvist–Zagier sporadic K3
3. **cooper_s7** (A183204) — Cooper 2012 level-7, weight-3 anchor
4. **cooper_s10** (A005260) — Cooper 2012 level-10, weight-3 anchor
5. **almkvist_zagier_second** (A125143) — AZ Almkvist–Zudilin ζ(3)-class K3
6. **t103** (A276536) — in-session K3-type discovery, full G1 pass, OEIS binomial-sums verified

## S₁,₂ Formal Validation & Rejection

Document: `data/autoresearch_v2/s12_formal_validation_rejection.md`

**Rejected on dual grounds:**
- G1-1: ODE order 2 (elliptic-type, weight 2), NOT 3 (K3-type)
- G1-3: minimal-operator mirror map **non-integral** (q₂ = 81/8)

v1's "S₁,₂ is K3" was built on (a) wrong-operator log solution (order-3 shift vs. order-2 PF), (b) a lucky numerical agreement that masked the geometry mismatch. Both issues documented formally. **v1 framework does not transfer to Phase 8.C.** S₁,₂ stays in the pool as a **negative control + formal rejection record** for archive completeness.

## AlphaEvolve Phase 8.B-ext Results

Script: `scripts/autoresearch_v2_alphaevolve.py` (Haiku-cost evolutionary sweep)

Generated 2 new K3-type survivors from neighborhood search around known anchors:
- **gen_2f_A2B2**: 2-factor (A=2, B=2) recovery of apery_zeta3 (expected)
- **gen_3f_A1B1C2**: 3-factor new candidate

Both queued for Phase C full gates. AlphaEvolve confirms K3-type neighborhood is richly populated (expected from literature); Phase C data tests will discriminate.

---

## Sonnet Thresholds & Haiku-vs-Sonnet Roadmap

**Haiku is sufficient for:**
- ✓ G1-1 ODE classification (polynomial nullspace, exact arithmetic)
- ✓ G1-2 Weil bounds (44 primes, integer arithmetic)
- ✓ G1-3 mirror-map integrality (Frobenius recursion, rational arithmetic)
- ✓ AlphaEvolve G1-class sweep (generate terms, classify)
- ✓ Phase C data-test setup (fetch SDSS DR17 via ESA/NASA APIs)
- ✓ Phase C KS tests & Poisson mocks (statistics, no precision beyond double)

**Sonnet REQUIRED for:**
- ⚠️ **G1-4 Monodromy (RK4 integration)**: 50-digit precision; mpmath operations; ~1 min per candidate. Haiku can set it up; Sonnet computes. **Cost threshold: when real monodromy data discriminates candidates (not placeholder Fuchsian classification).**
- ⚠️ **Phase C full statistics** (if data points to tight constraints): Sonnet for robust bootstrap / uncertainty quantification on small samples.
- ⚠️ **Phase D Lean kernel proof** (if top-3 finalists need formal Lean proof of recurrence relations): Sonnet-level reasoning for Lean tactic synthesis.
- ⚠️ **Manuscript writing** (Part VII, top-3 finalists): Sonnet for structured technical writing with self-review.

**Decision point per gate:**
```
if (gate == G1-4 and need_real_monodromy):
    → Sonnet (RK4 precision)
elif (phase_c_gate in [QT-1, QT-2, QT-4] and gap_size < 5σ):
    → Sonnet (robust stats on tight margin)
elif (phase_d and formal_proof_needed):
    → Sonnet (Lean synthesis)
elif (manuscript):
    → Sonnet (long-form technical writing)
else:
    → Haiku (everything else, cost savings)
```

---

## Execution Plan: Phase 8.C with Haiku-Primary + Sonnet-When-Needed

### 8.C.A — Quick data tests (weeks 5–6, Haiku)
- **EU-1** SDSS DR17 re-fetch (no Euclid Q1 available; blocking note Rule 1)
- **QT-1** KS test on 6 candidates (double-precision sufficient; Haiku)
- **QT-2** See-saw t-test (Poisson mocks; Haiku)
- **QT-3** PTA window occupancy (band checks; Haiku)
- **QT-5** Null-hypothesis battery (stats only; Haiku)

### 8.C.B — Sonnet trigger (if needed, weeks 6–7)
- If QT-1 produces |Δ| < 2σ → Sonnet for robust bootstrap
- If top-3 show tight superradiance band → Sonnet for precision uncertainty

### 8.C.C — Final selection to top 3 (HUMAN gate, week 7)
- Haiku tabulates scores; HUMAN selects top 3 for Phase D

### 8.D — Top-3 formalization + manuscript (weeks 8–12, Sonnet)
- **G1-4 real monodromy**: Sonnet (50-digit RK4)
- **D-1 Lean proofs**: Sonnet (tactic synthesis for n ≤ 20 decisions)
- **D-3 Part VII**: Sonnet (3-section technical article, negative-first)

---

## Cost Summary

| Phase | Component | Model | Est. Calls | Trigger |
|---|---|---|---|---|
| 8.B-ext | AlphaEvolve sweep | Haiku | ~100 | ✓ Done |
| 8.C.A | Data tests (QT-1..5) | Haiku | ~50 | Immediate |
| 8.C.B | Sonnet gate (if tight) | Sonnet | ~30–50 | If Δ < 2σ |
| 8.D | Formalization | Sonnet | ~100–150 | Auto after 8.C |

**Budget ceiling:** ~200–250 Sonnet calls (from ~500 Haiku); well within R2 total.
