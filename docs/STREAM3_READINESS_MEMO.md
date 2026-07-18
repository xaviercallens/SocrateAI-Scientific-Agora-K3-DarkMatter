# Stream 3 (Experimentation) Readiness Memo

**Date:** 2026-07-18  
**Status:** READY TO PROCEED (with known contingency)  
**Authority:** Stream 2 completion of D-1v2; Stream 1 axiom review in parallel

---

## Executive Summary

**✅ YES, provide ASSUMPTIONS.md to Stream 3 NOW**

D-3 (empirical validation) is unblocked and can proceed independently of C3b finalization. Stream 3 has sufficient certified inputs to begin real-data pipeline work.

---

## What Stream 3 Receives (Certified)

### ✅ Observable: Locked and Ready
- **L_K (singular-locus-proximity metric)** — kernel-specific, validated via kernel-swap battery
- **Separation:** s7=389.58σ, s10=389.36σ (far exceeds 2σ threshold)
- **Decision:** GATE D-1v2 PASS (2026-07-18, commit e9144a7)
- **Status:** Observable is production-ready for D-3 empirical rerun

### ✅ Candidate Pool: Qualified
- **cooper_s7** (OEIS A183204, Lean-verified) — Primary K3 candidate
- **cooper_s10** (OEIS A005260, Lean-verified) — Secondary K3 candidate
- **gorodetsky_s18** (arXiv:2102.11839) — Tertiary candidate (pending)
- **All three:** Passed mock calibration + kernel-swap battery validation

### ✅ Analysis Framework: Preregistered
- `GATE_D1v2_ANALYSIS_FRAMEWORK.md` — Outcome interpretation
- `GATE_D1v2_DECISION_GUIDE.md` — Decision procedures (HUMAN review)
- All cross-validation rules locked and documented

---

## What Stream 3 Does NOT Yet Have (Pending C3b)

### ⏳ Geometric Validation
- **C3b (Shioda-Inose moduli maps)** — Determines if K3↔elliptic algebraic locking closes
- **Status:** Framework functional, correct partner pairings under identification
- **Timeline:** ~1-2 weeks (mathematical, not computational)
- **Impact on D-3:** None (independent path)

### ⏳ Final Verdict
- **Branch outcome:** If C3b PASS → geometric mechanism confirmed
- **Branch outcome:** If C3b FAIL → geometry broken (Branch F5), model falsified
- **Stream 3 contingency:** Proceed with D-3 now; hold publication until C3b resolves

---

## D-3 Scope (What Stream 3 Does Next)

**Task:** Run L_K observable on real SDSS/Euclid sectors (100s of sectors)

**Inputs ready:**
- Observable L_K (validated, kernel-specific)
- Candidates s7, s10 (qualified, mock-tested)
- Analysis framework (preregistered, interpretation locked)
- Success criteria (≥80% alignment with predictions)

**Execution:**
```
For each (survey_sector, candidate) in {SDSS, Euclid} × {s7, s10}:
  1. Compute L_K(sector_density_map, candidate_kernel)
  2. Extract asymmetry Δ and lensing correlation
  3. Compare against mock ensemble (calibration from D-1v2)
  4. Flag anomalies or candidates that fail threshold
```

**Expected outcome:** Discriminate s7 vs. s10 on real data (confirmation or falsification)

---

## Contingency Path

**If C3b finds NO low-degree algebraic relations (Branch F5):**
- D-3 results become null (geometry is broken)
- Model is falsified at the geometric level
- Stream 3 work is not wasted: identifies empirical limits of observable L_K
- Publishing: Hold until C3b resolves; prepare post-mortem if F5

**Probability estimate:** Unknown (depends on correct partner identification)

---

## Assumptions Stream 3 Should Review

**From ASSUMPTIONS.md (Section 2.3 Experimentation):**
- V5 pipeline can classify hypotheses as K3 or Elliptic EFT ✓ (ready)
- Weak Lensing validation can achieve >80% alignment ? (untested)
- PTA validation can compare scalar monopole ? (untested)
- Cross-validation between streams will confirm results ✓ (framework in place)

**Action for Stream 3:** Review Section 2.3 and flag any assumptions that need tuning for SDSS/Euclid specifics.

---

## Decision

**✅ APPROVED:** Provide ASSUMPTIONS.md to Stream 3 now

Stream 3 can begin D-3 pipeline setup immediately. Observable is locked. Candidates are qualified. Framework is preregistered.

**Caveat:** Explain that C3b (Streams 1+2 responsibility) will determine final geometric verdict ~1-2 weeks. Stream 3 should plan for:
1. Parallel execution of D-3 (no delay)
2. Provisional publication (hold final endorsement until C3b resolves)
3. Contingency communication with collaborators if Branch F5 occurs

---

**Sign-off:** Stream 2 (S2-1d PASS), Stream 1 (R-0 complete, peer review approved)

**Next:** Provide ASSUMPTIONS.md to Stream 3 with this memo attached as context.

---

**Document:** ASSUMPTIONS.md (v1.0, 2026-07-18)  
**Validity:** Until C3b results available (expected ~2026-07-24)  
**Review cycle:** Weekly sync with all three streams
