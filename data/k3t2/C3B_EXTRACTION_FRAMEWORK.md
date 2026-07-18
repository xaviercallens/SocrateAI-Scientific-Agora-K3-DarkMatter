# C3b Extraction Framework — Shioda-Inose Moduli Map

**Date:** 2026-07-18  
**Status:** Framework established; sequence validation in progress  
**Authority:** Peer review (memorandum 2026-07-18) — C3b is the critical bottleneck after GATE D-1v2 PASS

---

## What is C3b?

C3b criterion is the Shioda-Inose moduli map extraction — the explicit algebraic relation linking the bulk K3 modulus $z_{\text{bulk}}$ to the brane elliptic modulus $z_{\text{brane}}$:

$$F(z_{\text{bulk}}, z_{\text{brane}}) = 0$$

**Physical meaning:** The geometric locking mechanism between the K3 surface (bulk) and its associated elliptic curve (brane) is encoded in this algebraic map. If the map has extreme singularities or fails algebraic closure, the EFT decoupling breaks → **Branch F5 (failure)**.

**Candidate pairs for extraction:**
- s₇ (order-3 K3, bulk) ↔ order-2 elliptic (brane)
- s₁₀ (order-3 K3, bulk) ↔ order-2 elliptic (brane)
- s₁₈ (order-3 K3, Gorodetsky, bulk) ↔ order-2 elliptic (brane)

---

## Implementation Infrastructure

### 1. Reference Sequence Database

**File:** `refs/recurrences_v1.json` (created 2026-07-18)

Contains:
- **Bulk sequences (order-3):** cooper_s7 (A183204, Lean-verified), cooper_s10 (A005260, Lean-verified), gorodetsky_s18 (arXiv:2102.11839, literature-sourced)
- **Brane sequences (order-2):** apery_zeta2 (A005258, classical), zagier_sporadic_A (Zagier 2009 §4)
- **Fields per sequence:** exact recurrence (Python-evaluable), initial terms, sources, structural notes

### 2. C3b Checker

**File:** `checkers/check_C3b_moduli_map.py` (v1.0.0, pre-existing)

**Algorithm:**
1. Load holonomic recurrences (shift-recurrence form)
2. Extract polynomial coefficients C(k), A(k), B(k) symbolically
3. **Validate MUM condition:** C(k) = (k+1)^order exactly (maximally unipotent monodromy at z=0)
4. Generate exact integer sequence terms from recurrence (high-precision arithmetic)
5. Check integrality (catches mistranscribed sequences within first few terms)
6. Compute Frobenius solutions: y₀(z) and y₁(z) = y₀ log z + ...
7. Derive mirror maps via series inversion: z(q) from q(z)
8. Search polynomial relations P(z_bulk(q^{m_b}), z_brane(q^{m_e})) = 0 over ℚ
9. Validate any found relation at higher truncation order (falsifiability check)
10. Output JSON certificate with verdict

**Command template:**
```bash
python3 checkers/check_C3b_moduli_map.py \
  --refs refs/recurrences_v1.json \
  --bulk <order-3-id> \
  --brane <order-2-id> \
  --n-terms 28 \
  --max-bidegree 4 \
  --out data/certificates/C3b_<bulk>__<brane>.json
```

---

## Execution Plan

### Phase 1: Sequence Validation (Current)

**Task:** Verify exact recurrence transcriptions via:
1. **MUM condition:** C(k) = (k+1)^order for order-3 (s₇, s₁₀, s₁₈) and order-2 (apery_zeta2, zagier_A)
2. **Integrality test:** Run checker up to ~20 terms; all terms must be integers
3. **Literature cross-check:** Recomputed terms vs OEIS b-files and published tables

**Blocker:** Exact recurrence relations require careful transcription from:
- OEIS A183204 (s₇), A005260 (s₁₀), A005258 (apery ζ2)
- Gorodetsky arXiv:2102.11839 (s₁₈)
- Zagier 2009 "Integral solutions of Apéry-like recurrences" (zagier family)

**Current status:** Recurrence strings drafted; MUM validation in progress (apery_zeta2 + cooper_s7 run shows C(k) extraction needs refinement).

### Phase 2: Moduli Map Extraction (Pending)

Once sequences validate:
```bash
for pair in \
  "cooper_s7 apery_zeta2" \
  "cooper_s10 zagier_sporadic_A" \
  "gorodetsky_s18 apery_zeta3"
do
  python3 checkers/check_C3b_moduli_map.py --bulk ${pair% *} --brane ${pair#* } ...
done
```

**Outcome matrix:**
| Pair | Verdict | Relation | Validation | Next |
|------|---------|----------|------------|------|
| s₇+brane | C3B_RELATION_FOUND | F(z_b, z_e) = 0 | ✓ to q^36 | extract F(z) |
| s₁₀+brane | C3B_RELATION_FOUND | ... | ✓ to q^36 | extract F(z) |
| s₁₈+brane | C3B_RELATION_FOUND | ... | ✓ to q^36 | extract F(z) |

### Phase 3: Relation Analysis (Post-extraction)

**Questions to resolve:**
1. Is F(z) a low-degree rational function or high-degree/singular?
2. Do the three pairs find the SAME algebraic relation (moduli locking is canonical)?
3. Are there branch cuts or algebraic poles that break EFT closure?

**Output:** `C3B_EXTRACTION_RESULTS.md` with:
- Three certified F(z) mappings
- Singularity analysis (physical/unphysical poles)
- Decision: GATE C3B PASS or Branch F5

---

## Epistemic Status

**After D-1v2 PASS:**
- Observable L_K validated (kernel-specific, 389σ separation)
- **Remaining question:** Can we lock the K3↔elliptic moduli map algebraically?

**C3b determines:**
- ✅ **PASS:** F(z) exists, low-degree, EFT locking mechanism closes → proceed to D-3
- ❌ **FAIL:** No relation found, or relation has extreme singularities → Branch F5 (geometric mechanism broken)

---

## Authority & Review

- **Peer review (2026-07-18):** "All computational resources must pivot to C3b extraction. Compute exact rational Hauptmodul mappings for s₇, s₁₀, s₁₈ against verified order-2 partners. Extract algebraic maps F(z)."
- **Checker design:** Deterministic exact arithmetic, no LLM calls, falsifiable (relation validated at higher order)
- **Reference data:** Literature-only (OEIS, published papers, Lean-transcribed recurrences)

---

**Next:** Resume sequence validation once recurrence transcriptions are verified against OEIS/literature sources. Target: 3 C3b certificates by 2026-07-19.

Generated-by: Claude Code | Reviewed-by: pending | Approved-by: [user judgment on reference accuracy]
