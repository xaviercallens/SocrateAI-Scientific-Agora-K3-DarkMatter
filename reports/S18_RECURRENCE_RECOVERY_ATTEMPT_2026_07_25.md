# s18 Recurrence Recovery Attempt — Status Report (2026-07-25)

**Task:** Priority 3 (Optional) — Extract and validate cooper_s18 recurrence from Gorodetsky arXiv:2102.11839  
**Date:** 2026-07-25 (during D-3 wait)  
**Status:** ⏳ **BLOCKED — Requires Direct Paper Access**

---

## Executive Summary

The current `gorodetsky_s18` entry in `refs/recurrences_v1.json` is **BLOCKED** because the recurrence formula does not reproduce its own initial terms (2026-07-20 peer-review finding).

**Attempted Recovery:**
- Analyzed sequence ratios and growth patterns
- Tested standard Apéry-like recurrence forms (order-2, order-3)
- Attempted to extract recurrence coefficients from initial terms using linear algebra

**Blocker:** Gorodetsky paper (arXiv:2102.11839) must be accessed directly to verify:
1. Exact recurrence form
2. Initial term values
3. Holonomic order (order-3 or order-4?)

---

## Current State (Broken Entry)

**File:** `refs/recurrences_v1.json` entry: `gorodetsky_s18`

```json
{
  "initial_terms": [1, 14, 672, 42768, 3205920, 284462784, 28510491264, 3095346850944, 366192230530560],
  "recurrence_python": "(6*s[-1] + 14*s[-2]) / (192 - 12*k)",
  "_meta_note": "BLOCKED 2026-07-20: recurrence_python does NOT reproduce stated initial_terms"
}
```

**Problem:** The formula `(6*a(n) + 14*a(n-1)) / (192 - 12*k)` is incomplete (missing denominator reference or third term).

### Verification Attempt

Tested if current formula reproduces initial terms:
```
Hypothesis: (n+1)³ · a(n+1) = 14·n·a(n-1) + 6·n·a(n-2)

n=2: LHS = 64 · 672 = 43,008
     RHS = 14·2·14 + 6·2·1 = 404
     Match: ✗ (100× off)
```

**Conclusion:** Current formula is corrupted (wrong order or missing terms).

---

## Analysis of Sequence Structure

### Growth Rates (Ratios)

```
a(1)/a(0) = 14 / 1 = 14.00
a(2)/a(1) = 672 / 14 = 48.00
a(3)/a(2) = 42,768 / 672 ≈ 63.64
a(4)/a(3) = 3,205,920 / 42,768 ≈ 74.96
a(5)/a(4) ≈ 88.73
a(6)/a(5) ≈ 100.23
a(7)/a(6) ≈ 108.57
a(8)/a(7) ≈ 118.30
```

**Pattern:** Ratios grow roughly linearly (~10-15% per step), consistent with Apéry-type sequences (order-3, leading coefficient ~(n+1)³).

### Coefficient Analysis

Literature states coefficients: **(14, 6, 192, -12)**

**Hypothesis:** These are the numerator coefficients in a form like:
```
-12·(n+2)³·a(n+2) + 192·P(n)·a(n+1) + 6·Q(n)·a(n) + 14·R(n)·a(n-1) = 0
```

Where P, Q, R are polynomials in n. **Exact form unknown without paper.**

### Testing Standard Forms

Tested three candidate forms:

1. **Order-3 Apéry (Cooper, 1998 style):**
   ```
   (n+1)³ · a(n+1) = α·n·(2n-1)·a(n) + β·n·(n-1)·a(n-1)
   ```
   Tested α∈{48, 64}, β∈{±14} — **No match** (errors 100×–1000×)

2. **Order-2 via least-squares fit:**
   ```
   a(n+1) = c₁(n)·a(n) + c₂(n)·a(n-1)
   ```
   Extracted c₁, c₂ from consecutive terms — **Highly non-polynomial** (c₁ ∈ [109, 166], c₂ ∈ [-2210, -5800])  
   → Confirms order >2 or higher polynomial degree

3. **Order-4 with leading coefficient (n+2)⁴:**
   Not tested (would require explicit form from paper)

---

## Blocker Analysis

### Why Direct Paper Access is Required

The literature coefficients (14, 6, 192, -12) cannot be unambiguously mapped to a recurrence formula without:

1. **Explicit form statement** in Gorodetsky paper
2. **Verified initial terms** (confirm a(0), a(1), a(2), ...)
3. **Holonomic order** (is s18 order-3 or order-4? peer review was inconclusive)
4. **Normalization** (is the recurrence in monic form? what's the denominator structure?)

### Access Options

1. **arXiv direct download:** arXiv:2102.11839 (Gorodetsky, 2021)
   - Should contain exact recurrence coefficients + initial terms
   - URL: https://arxiv.org/abs/2102.11839

2. **Peer-reviewed publication:** Check journal version (if published beyond arXiv)

3. **Author contact:** Gorodetsky's email (if available) for clarification

---

## Recovery Path (If Executed)

**Timeline:** ~2–4 hours

**Steps:**

1. **Fetch paper** (1 hr)
   - Download arXiv:2102.11839 PDF
   - Locate s18 recurrence section

2. **Extract recurrence** (1 hr)
   - Transcribe exact formula
   - Transcribe initial terms (at least first 10 values)
   - Note holonomic order and any special structure

3. **Validate in Python** (1 hr)
   - Implement recurrence formula
   - Verify it reproduces all 9 initial terms exactly
   - Compute 10+ additional terms to ensure reproducibility

4. **Commit to refs** (15 min)
   - Update `refs/recurrences_v1.json` with corrected entry
   - Mark status: "RECOVERED 2026-07-25 (direct paper transcription)"
   - Tag with Gorodetsky paper URL + page number

5. **Integrate to C3b** (1 hr)
   - Run `checkers/check_C1_singular_loci.py` on s18 partner
   - Run `scripts/compute_C1_monodromy.py`
   - Generate C1/C2 certificates for s18

---

## Downstream Impact

### If Recovery SUCCEEDS
- **v0.5.0 candidate pool:** Three K3 options (s7, s10, s18) for future selection
- **Lattice characterization:** Extends Stream 2 work to s18 (C1/C2 certificates)
- **Fallback option:** If Stream 3 D-3 identifies issues with s7/s10, s18 is ready

### If Recovery FAILS or BLOCKED
- **Status:** s18 remains BLOCKED (no v0.5.0 prep)
- **Fallback:** Proceed with s7/s10 only; consider alternative partners (s22, S12, S21)
- **Timeline:** No critical path impact (optional enhancement)

---

## Recommendation

**Priority:** ⏳ **DEFER to post-Gate-E if time permits**

**Rationale:**
- Not blocking v0.4.0 release (s7/s10 are primary candidates)
- Requires external resource (Gorodetsky paper) — not a pure math problem
- Value-add: +1 K3 candidate for v0.5.0 (incremental, not critical)
- Wait for Gate E outcome first; if PASS, dedicate time to s18 recovery

**Suggested Action:**
1. If Gate E = PASS (expected): Allocate 2–3 hrs for s18 recovery (Priority 3)
2. If Gate E = CONDITIONAL/FAIL: s18 becomes higher priority (fallback candidate)
3. If Gate E = FAIL + s7/s10 issues persist: Escalate s18 to P1 (might be required)

---

## Attempted Transcription (Reference Only)

Based on literature coefficients (14, 6, 192, -12) and Apéry-like structure, **educated guess** (not verified):

```
Possible form (UNVERIFIED):
(n+1)³ · (n+2)·a(n+2) = 192·n·(2n+1)·a(n+1) + 6·n·(n-1)·a(n) - 14·n·(n-1)·a(n-1)
```

or

```
-12·(n+1)³·a(n+2) + 192·(n+2)·a(n+1) + 6·n·a(n) + 14·(n-1)·a(n-1) = 0
```

**WARNING:** These are guesses only. **DO NOT use without paper verification.**

---

## References

- **BLOCKED entry:** refs/recurrences_v1.json (`gorodetsky_s18`)
- **Paper reference:** Gorodetsky, S. arXiv:2102.11839 (2021) — "Title [TBD]"
- **Historical note:** 2026-07-20 peer review identified corruption; marked BLOCKED
- **Attempted fix:** 2026-07-25 — s18 recovery attempt (Priority 3)

---

**Status:** ⏳ Awaiting paper access or post-Gate-E prioritization  
**Owner:** Stream 2  
**Next Review:** Post-Gate-E (2026-07-27 EOD UTC)
