# Extended Monodromy Framework — Design for v0.5.0 (2026-07-25)

**Task:** Priority 4 (Optional) — Design full Frobenius exponent computation (research phase, no implementation)  
**Date:** 2026-07-25 (during D-3 wait)  
**Scope:** Plan infrastructure for v0.5.0 release (Tier A Kodaira-type resolution)  
**Timeline:** 2–3 hours (research + planning only)

---

## Overview

Stream 2's v2 certificates (commit 1dd17cd) use **exponent-based Kodaira classification** (Tier B: exact but heuristic). Full Tier A requires **complete monodromy-orbit analysis**:

1. **Local monodromy matrices** at each singular fibre (SL₂(ℤ) action)
2. **Rank-1 twist resolution** (fibre discriminant → component structure)
3. **Gram matrix of transcendental lattice** (intersection form)
4. **Modular-forms identification** (for elliptic partners, e.g., A279619)

This document outlines the infrastructure for v0.5.0.

---

## 1. Current State (v2 Certificates, Tier B)

### What We Have

**C1-v2 certificates** contain:
- ✅ Singular loci z-coordinates (exact, from P₂(z) roots)
- ✅ Local Picard-Fuchs exponents (exact, via indicial equation)
- ✅ Fuchs relation verification (independent constraint)
- ✅ Kodaira type (heuristic from exponent difference)
- ✅ Picard rank ρ (from Shioda-Tate formula)

**Limitations (Tier B→A gap):**
- ⚠️ Kodaira types marked "tentative" (need full monodromy-orbit classification)
- ⚠️ No transcendental lattice Gram matrix (requires Hodge-theory integration)
- ⚠️ No Weierstrass model at singular fibres (component multiplicities heuristic)
- ⚠️ No modular-forms identification of elliptic partners (A279619 origin unclear)

### Why Tier A Matters

- **v0.4.0 release:** Tier B sufficient (operator identity validated empirically by Stream 3)
- **v0.5.0 planning:** Tier A required for:
  - Extending to new K3 candidates (s18, s22, etc.)
  - Claiming isomorphism between partners rigorously
  - Building dual K3 isogenies (if geometry allows)
  - Publishing results in peer-reviewed venues

---

## 2. Full Monodromy Computation (Tier A)

### 2.1 Local Monodromy Matrices

At each singular point $z_c$, the local solution space is 2-dimensional (order-2 operator). The monodromy action is a linear transformation:

$$\gamma_c: \text{solutions} \to \text{solutions}$$

represented as a 2×2 matrix in SL₂(ℤ).

**Computational approach:**
```
For each singular point z_c:
  1. Compute local solution basis (analytic continuation around z_c)
  2. Trace path returning to z_c (close the loop)
  3. Extract monodromy matrix M_c ∈ SL₂(ℤ)
  4. Classify M_c (elliptic, parabolic, hyperbolic, unipotent)
```

**Tools:**
- SymPy `logseries` + analytic continuation for local expansions
- SageMath `matrix_group` for SL₂(ℤ) orbit analysis
- Numerical integration (mpmath) for path-tracing

**Expected output:**
```
cooper_s7_partner:
  z = -1: M₁ = [[a, b], [c, d]] (specific 2×2 matrix)
  z = 1/27: M₂ = [[a', b'], [c', d']]
  → Trace each M, eigenvalues, jordan form
  → Map to Kodaira type via standard tables (Morrison, Persson)
```

### 2.2 Rank-1 Twist (Fibre-Picard Lattice)

The **elliptic fibre** at each singular point has a geometric realization as an algebraic curve. The Picard number of the fibre (number of irreducible components + rational curves) is determined by the **rank-1 twist** of the local monodromy.

**Concept:** SL₂(ℤ) action on ℂ* lifts to Pic(fibre) action. The rank of the fixed-point sublattice tells us the component structure.

**Computational approach:**
```
For each singular point z_c with monodromy M_c:
  1. Compute Jordan normal form of M_c
  2. Extract eigenvalues λ, multiplicities
  3. Map to Kodaira classification:
     - (λ=1, mult=2, unipotent) → Type II or I_n (n determined by higher-order terms)
     - (λ=-1, mult=2) → Type III or I_n^*
     - (λ≠±1) → Type IV or I_n with n = 1/(1 - λ)
  4. Count irreducible components (from Kodaira table)
```

**Tools:**
- SymPy eigenvalue computation
- Kodaira classification tables (Morrison 1984, Persson 1977)
- Custom lookup (fibre → component count)

**Expected output:**
```
cooper_s7_partner:
  z = -1: Monodromy trace = 2 (unipotent) → Type II → 2 irreducible components
  z = 1/27: Monodromy trace = 2 (unipotent) → Type II → 2 irreducible components
  ρ = 2 + (2-1) + (2-1) = 4 ✓ (matches v2 certificate)
```

### 2.3 Transcendental Lattice Gram Matrix

Once ρ is known, the transcendental lattice T has rank 22 - ρ = T (K3 constraint). The **Gram matrix** encodes the intersection form:

$$\text{Gram}_{ij} = \langle e_i, e_j \rangle$$

where basis vectors $e_i$ span T and ⟨·,·⟩ is the Hodge intersection pairing.

**Computational approach:**
```
Difficult! Requires:
  1. Integrate Picard-Fuchs periods along closed paths (all homotopy group elements)
  2. Compute period matrix (transcendental part)
  3. Extract intersection form from period matrix
  4. Verify Hodge Riemann bilinear relations (validation check)
```

**Tools:**
- Sage/PARI numerical integration (arbitrary precision)
- mpmath for high-precision arithmetic (100–1000 digits)
- Lattice-reduction algorithms (LLL) to find small Gram matrix

**Expected deliverable:**
```
cooper_s7_partner transcendental_lattice:
  T = 18 (rank)
  Gram matrix (18×18, integer entries after scaling)
  Signature: (1, 17) (one positive, rest negative — K3 constraint)
```

---

## 3. Modular-Forms Identification (Elliptic Partners)

**Problem:** Given an order-2 elliptic operator, identify its corresponding modular form.

**Example:** cooper_s7_partner (OEIS A279619) is derived from the symmetric square of cooper_s7 (K3-type). But what modular form encodes A279619?

**Approach (Existing Methods):**

1. **Newform lookup** (L-functions and Modular Forms Database, LMFDB):
   - Search LMFDB for modular forms matching the period structure
   - Cross-check Hecke eigenvalues against OEIS coefficients

2. **Modularity theorem** (Taniyama–Shimura):
   - If A279619 is a modular form sequence, it corresponds to an elliptic curve over ℚ
   - Identify conductor, level, weight

3. **Symmetric-square lifting** (Theory):
   - If L_K is order-3 (K3), then Sym²(L_K) is order-2 (elliptic)
   - The modular form of Sym²(L_K) is Sym²(f) where f is the modular form of L_K

**Implementation:**

```python
# Pseudocode for v0.5.0

from lmfdb import ModularForms

def identify_elliptic_partner(sequence_name, oeis_id, coefficients):
    """
    Query LMFDB for modular form matching the sequence.
    """
    # Step 1: Compute L-function coefficients (Euler product)
    l_coeffs = compute_l_coefficients(coefficients)
    
    # Step 2: Search LMFDB by level, weight, character
    results = ModularForms.search(
        conductor=oeis_id.conductor,  # estimate from growth rate
        weight=2,  # elliptic = weight 2 (universal)
        character=1  # assume trivial character (no quadratic twist)
    )
    
    # Step 3: Cross-check eigenvalues
    for mf in results:
        if match_hecke_eigenvalues(l_coeffs, mf.eigenvalues):
            return mf
    
    # Step 4: If no match, try higher weights or twists
    results = ModularForms.search(
        conductor=...,
        weight=3,  # try order-3 (symmetric square weight)
        character=1
    )
    # ... iterate until match found or exhausted
    
    return None  # Not identified
```

**Tools:**
- LMFDB API (https://www.lmfdb.org/api/)
- SageMath `modular_forms` module
- High-precision L-function computation

**Expected output for v0.5.0:**
```
cooper_s7_partner (A279619):
  Identified as: Modular form of level L, weight 2, character χ
  Conductor: [specific integer]
  Hecke eigenvalues: a₂, a₃, a₅, ... (first 100)
  Symmetry: Symmetric square of cooper_s7_modform
  Status: VERIFIED MODULAR ✓
```

---

## 4. Weierstrass Model at Singular Fibres

For a complete understanding, extract the **Weierstrass model** at each singular fibre:

$$y^2 = x^3 + A(z) x + B(z)$$

where $A(z), B(z)$ are the Picard-Fuchs potentials at the fibre.

**Purpose:** Determine exact component structure and multiplicities.

**Computational approach:**
```
1. From Picard-Fuchs operator, extract discriminant Δ(z) = 4A³ + 27B²
2. Factor Δ(z) at each singular point z_c
3. Multiplicity of (z - z_c) in Δ determines fibre type
4. Solve singularities at (z_c, y_c) to find nodes/cusps
5. Count irreducible components of the curve
```

**Tools:**
- SymPy factorization
- Singular (computer algebra for singularity analysis)
- Custom curve-resolution code

**Expected output:**
```
cooper_s7_partner fibre at z = -1:
  Weierstrass form: y² = x³ + A₋₁ x + B₋₁ (at z = -1)
  Discriminant order: ord_{z=-1} Δ(z) = 2
  Singularities: [[x₁, y₁], [x₂, y₂]] (node locations)
  Reducible components: 2 rational curves intersecting transversely
  Kodaira type: II ✓ (matches monodromy result)
```

---

## 5. Implementation Roadmap (v0.5.0)

### Phase 1: Monodromy Matrix Computation (4–6 hrs)

**Goal:** scripts/compute_monodromy_matrices.py

```
Input: Picard-Fuchs operator (from recurrence)
Process:
  1. Compute local series solutions around each singular point
  2. Analytically continue along closed paths (homotopy generators)
  3. Extract SL₂(ℤ) matrices at each fibre
  4. Verify consistency (product of all monodromies = identity + symplectic constraint)
Output: Monodromy matrices + classification (elliptic/parabolic/hyperbolic)
```

**Estimate:** 4–6 hours (including testing + error handling)

### Phase 2: Kodaira-Type Resolution (2–3 hrs)

**Goal:** scripts/resolve_kodaira_types.py

```
Input: Monodromy matrices (from Phase 1)
Process:
  1. Extract traces, eigenvalues, jordan forms
  2. Look up Kodaira classification (Morrison tables)
  3. Count irreducible components per fibre
  4. Verify Shioda-Tate constraint (ρ = 2 + Σ(m_i - 1))
Output: Exact Kodaira types + component counts
```

**Estimate:** 2–3 hours

### Phase 3: Transcendental Lattice Gram Matrix (8–12 hrs)

**Goal:** scripts/compute_transcendental_lattice.py

```
Input: Periods (from Picard-Fuchs integration)
Process:
  1. Integrate periods along all homotopy loops
  2. Build period matrix (transcendental part)
  3. Compute intersection form (from period matrix)
  4. Reduce Gram matrix to minimal form (LLL)
  5. Verify Hodge Riemann constraints
Output: Gram matrix (T × T integers, signature (1, T-1))
```

**Estimate:** 8–12 hours (numerical integration is finicky)

### Phase 4: Modular-Forms Identification (3–5 hrs)

**Goal:** scripts/identify_modular_forms.py

```
Input: Elliptic operator + OEIS sequence
Process:
  1. Query LMFDB API for matching modular forms
  2. Cross-check Hecke eigenvalues
  3. Verify L-function match
  4. Document symmetry (symmetric square? twist?)
Output: Modular form parameters + verification
```

**Estimate:** 3–5 hours (depends on LMFDB availability)

### Phase 5: Weierstrass Model & Singularities (2–4 hrs)

**Goal:** scripts/analyze_weierstrass_model.py

```
Input: Picard-Fuchs potentials A(z), B(z)
Process:
  1. Compute discriminant Δ(z)
  2. Factor at singular points
  3. Resolve singularities
  4. Verify component count vs. Kodaira type
Output: Weierstrass forms + singularity reports
```

**Estimate:** 2–4 hours

### Total Estimate (All Phases)

**19–34 hours** for full Tier A monodromy framework.

**Breakdown:**
- Phases 1–2 (core monodromy): 6–9 hrs
- Phase 3 (lattice): 8–12 hrs (most demanding)
- Phases 4–5 (modular forms + Weierstrass): 5–9 hrs

---

## 6. Resource Requirements

### Software Tools

| Tool | Purpose | Status |
|------|---------|--------|
| SymPy | Polynomial algebra, eigenvalues, factorization | ✅ Installed |
| SageMath | Modular forms, lattice reduction (LLL) | ⚠️ Optional (not required) |
| mpmath | High-precision arithmetic (100–1000 digits) | ✅ Available |
| LMFDB API | Modular form database queries | ✅ Open web API |
| Singular | Singularity analysis (optional) | ⚠️ Specialized (install if needed) |
| PARI/GP | Lattice algorithms, period computation | ⚠️ Specialized (install if needed) |

**Recommendation:** Start with SymPy + mpmath (already available); add Sage/Singular only if needed.

### Computation Time

- **Monodromy matrix:** ~10–30 sec per operator (analytic continuation can be slow)
- **Lattice Gram matrix:** ~1–5 min per operator (numerical integration at many points)
- **Full run (both s7 & s10 partners):** ~5–10 min total

**Hardware:** CPU-only (no GPU needed; ~4 GB RAM for high-precision arithmetic)

---

## 7. Integration with Stream Workflows

### Stream 1 (Lean Formalization)
- **No impact:** v0.5.0 monodromy is independent of Lean proof
- **Optional:** Could formalize monodromy-orbit constraints as additional lemmas (advanced)

### Stream 2 (K3 Selection & Lattice)
- **Upgrade path:** v2 → v2.1 certificates with Tier A Kodaira types + Gram matrices
- **Validation:** v0.5.0 artifacts should verify v0.4.0 results (self-consistency check)

### Stream 3 (D-3 Empirical Validation)
- **Post-hoc verification:** v0.5.0 monodromy should match empirical D-3 structure (if Gate E PASS)
- **Fallback analysis:** If Gate E CONDITIONAL/FAIL, monodromy can help diagnose lattice issues

---

## 8. Success Criteria (v0.5.0 Release)

✅ **All candidates characterized (Tier A):**
- [ ] Exact Kodaira types (resolved from monodromy)
- [ ] Picard rank ρ (verified via Shioda-Tate + monodromy)
- [ ] Transcendental lattice Gram matrix (with signature validation)
- [ ] Modular form identification (for elliptic partners)

✅ **Self-consistency checks pass:**
- [ ] Monodromy symplectic constraint: det(M_i) = ±1 for all i
- [ ] Hodge Riemann bilinear relations: signature (1, T-1)
- [ ] Fujita's formula: discriminant matches expected genus-genus formula

✅ **Documentation complete:**
- [ ] v2.1 certificates (exact Kodaira types)
- [ ] Lattice Gram matrices (committted JSON)
- [ ] Modular form cross-references (LMFDB links)

✅ **Backward compatibility:**
- [ ] v0.5.0 results should agree with v0.4.0 (where Tier B was used)
- [ ] Any discrepancies resolved via deeper analysis (not errors)

---

## 9. References & Further Reading

**Kodaira Classification:**
- Kodaira, K. (1963). "On compact analytic surfaces: II"
- Morrison, D. (1984). "On K3 surfaces with large Picard number"
- Persson, U. (1977). "Configuration of Kodaira fibers on elliptic K3 surfaces"

**Picard-Fuchs & Modular Forms:**
- Deligne, P. (1974). "Variétés abéliennes ordinaires..." (Bourbaki seminar)
- Nagel, J. (2014). "Introduction to Hodge structures" (Lecture notes)

**Symmetric Squares & Monodromy:**
- Gelbart, S.; Shahidi, F. (1988). "Analytic properties of automorphic L-functions"
- Gross, B. (1990). "A tameness criterion for Galois representations"

**LMFDB:**
- https://www.lmfdb.org/ (The L-functions and Modular Forms Database)
- API: https://www.lmfdb.org/api/

---

## 10. Recommendation

### For v0.4.0 (Current Release)
✅ **Tier B sufficient** — exponent-based Kodaira types + Shioda-Tate ρ

### For v0.5.0 (Future Release)
📌 **Prioritize Phases 1–2** (monodromy + Kodaira resolution) — **6–9 hrs**  
⏳ **Phase 3** (lattice Gram matrix) — defer if time-constrained  
⏳ **Phases 4–5** (modular forms + Weierstrass) — optional enhancements

### Effort vs. Value
- **High ROI:** Phases 1–2 (6–9 hrs → complete Kodaira classification)
- **Medium ROI:** Phase 3 (8–12 hrs → full lattice structure)
- **Low ROI:** Phases 4–5 (5–9 hrs → publication enhancement)

**Suggested v0.5.0 scope:** Phases 1–3 (17–25 hrs over 2–3 days)

---

**Generated:** 2026-07-25 (design phase, no implementation)  
**Status:** 📋 **READY FOR v0.5.0 PLANNING**  
**Next Step:** After Gate E decision (2026-07-27), authorize v0.5.0 sprint if resources available
