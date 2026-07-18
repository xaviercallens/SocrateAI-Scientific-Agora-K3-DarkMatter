# C3b Extraction Status Report

**Date:** 2026-07-18  
**Overall Status:** Framework established; implementation blocked on recurrence transformation  
**Blocker Type:** Specialized mathematical transformation (shift-recurrence → ODE)

---

## What Has Been Accomplished

### ✅ Framework Infrastructure
1. **refs/recurrences_v1.json** — Reference database with:
   - cooper_s7, cooper_s10 (Lean-verified shift-recurrences)
   - apery_zeta2 (OEIS A005258, recurrence verified)
   - Initial terms verified against OEIS b-files

2. **C3B_EXTRACTION_FRAMEWORK.md** — Complete algorithm documentation

3. **checkers/check_C3b_moduli_map.py** — Pre-existing deterministic exact-arithmetic tool (v1.0.0)

### ✅ Sequence Validation
- cooper_s7 (A183204): Initial terms [1, 4, 48, 760, 13840, 273504, ...] ✓ verified
- cooper_s10 (A005260): Initial terms [1, 2, 18, 164, 1810, 21252, ...] ✓ verified
- apery_zeta2 (A005258): Recurrence verified: (n+1)² · a(n+1) = (11n² + 11n + 3) · a(n) + n² · a(n-1)

---

## Critical Blocker: Recurrence Form Mismatch

### The Problem

**Lean files provide:** Order-2 shift-recurrences (generating-function coefficient form)
- cooper_s7: P₀(n)·a(n) + P₁(n)·a(n+1) + P₂(n)·a(n+2) = 0
- P₂(n) = (n+2)³

**C3b checker expects:** Order-3 Picard-Fuchs ODEs (differential equation form)
- Requires C(k) = (k+1)³ exactly for MUM (maximally unipotent monodromy) validation
- Extraction test shows C(k) = (k+2)³ ≠ required form

### Why The Difference Exists

The Lean files record the **shift-recurrence** (polynomial identity in sequence indices), which is order-2 because three consecutive terms appear. The **generating-function ODE** (differential equation in the variable z) is order-3 because the ODE coefficients have degree-3.

These are related by the transformation **θ = z·d/dz** (Euler operator), documented in `scripts/k3t2_singular_loci.py`.

### The Required Transformation

To convert shift-recurrence → ODE:
1. Take P₀(n), P₁(n), P₂(n) from shift-recurrence
2. Apply shift and substitution P_k(n) → P_k(θ) where θ = z·d/dz
3. Expand θ-powers in terms of z^j·d^j/dz^j (standard identities, e.g., θ³ = z·d/dz + 3z²·d²/dz² + z³·d³/dz³)
4. Collect by derivative order to extract ODE form
5. Extract Q₀(z), Q₁(z), Q₂(z), Q₃(z) (coefficients of F, F', F'', F''')

This is **exactly what** `k3t2_singular_loci.py` does (lines 58–153), but for singular-locus extraction, not C3b.

---

## Path Forward

### Option A: Automate the Transformation
**Task:** Create a script that applies theta transformation to refs/recurrences_v1.json entries:
```python
def shift_recurrence_to_ode(P0, P1, P2):
    """Transform shift-recurrence (order-2) to ODE (order-3)."""
    # Use k3t2_singular_loci.py logic:
    # 1. Extract theta-power coefficients
    # 2. Apply shifts for P0(theta), P1(theta-1), P2(theta-2)
    # 3. Combine with z-powers: L = z^2·P0(theta) + z·P1(theta-1) + P2(theta-2)
    # 4. Return ODE coefficients Q0, Q1, Q2, Q3
    pass
```

**Blockers:** Requires careful symbolic algebra; test cases needed to verify against k3t2_singular_loci.py output.

### Option B: Use Existing ODE Data
**Alternative:** Extract ODE coefficients from `data/k3t2/d2_4_singular_loci.json` (output of k3t2_singular_loci.py for s7/s10) and use those directly in refs file.

**Blockers:** Gorodetsky s18 may not have ODE data on hand; requires rerunning singular-loci script.

### Option C: Direct Mirror-Map Computation
**Alternative:** Skip ODE extraction; compute mirror maps directly from shift-recurrence terms.

**Blockers:** C3b checker is hard-coded for ODE form; would require checker modification.

---

## Why This Matters

The C3b gate determines whether the K3 moduli can close an algebraic relation with an associated elliptic curve. If the answer is yes (low-degree F(z) found), the EFT mechanism works and D-3 (empirical validation) proceeds. If no, the geometry is broken (Branch F5).

The checker is designed with the right algorithm (exact arithmetic, falsifiable relations), but it's optimized for ODE form. The shift-recurrence form technically has the same mathematical content, but needs transformation to meet the checker's MUM validation criteria.

---

## Recommendation

**Immediate next step (minimal effort, high confidence):**

1. Use Option B: Extract confirmed ODE coefficients for cooper_s7 and cooper_s10 from running k3t2_singular_loci.py with the new correct shift-recurrence data.
2. Embed those ODE coefficients into refs/recurrences_v1.json as a separate field or parallel entry.
3. Run C3b checker with corrected ODE form.

**Long-term robustness (Option A):**

Write a `shift_to_ode_transformer.py` utility that codifies the theta transformation and validates against singular-loci reference outputs. This makes future C3b runs automated and reproducible.

---

## Current State of Deliverables

- ✅ Framework established & documented
- ✅ Sequence data verified
- ⏸️ Checker execution blocked (awaiting ODE form recurrences)
- ⏳ Awaiting manual confirmation of next path

**Authority:** Peer review (2026-07-18) cleared R-0 and elevated C3b extraction. Block is mechanical (recurrence form conversion), not conceptual.

---

Generated-by: Claude Code | Reviewed-by: pending | Validated-by: OEIS cross-checks
