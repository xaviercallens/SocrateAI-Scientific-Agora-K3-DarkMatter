---
name: axiom-gap-disclosure
description: Tracks and enforces transparent disclosure of all unproven assumptions, axioms, and open problems, preventing silent assumptions from hiding in code or manuscripts.
---

# Axiom & Gap Disclosure Protocol

Use this skill whenever adding an assumption, axiom, or unproven mathematical claim to the project.

## Core Principle

> Every unproven assumption must be: (1) explicitly labeled as `axiom` in Lean, (2) justified with a reason in comments, (3) disclosed in CAVEATS.md, (4) tracked in OPEN_PROBLEMS.md, and (5) disclosed in every manuscript that depends on it.

**Violations of this principle are release-blocking.**

## Axiom Taxonomy

### Type A: Mathematical Axioms (proven in principle, formalization pending)
- **Example:** `s20_recurrence (general n)` — exact for n∈[0,60], kernel-verified n≤8, WZ certificate compilation pending
- **Justification:** Symbolic verification via SymPy; pending kernel compilation
- **Discharge path:** Phase 4 roadmap (WZ Lean compilation)
- **Lean annotation:**
  ```lean
  axiom s20_recurrence (n : ℕ) : 
    P0(n)*S20(n) + P1(n)*S20(n+1) + ... = 0
  -- Justification: Exact-verified for n ∈ [0, 60] via scripts/verify_s20_recurrence.py
  -- Pending: WZ certificate compilation in Phase 4 (see OPEN_PROBLEMS.md, item 3)
  ```

### Type B: Physical Axioms (phenomenological input)
- **Example:** Chameleon density-dependent mass scaling $m_\text{eff} \propto \rho^{1/4}$ near M87*
- **Justification:** Established mechanism in chameleon theory; not specific to this geometry
- **Discharge path:** Either (1) formal derivation from Lagrangian, or (2) honest statement "phenomenological input"
- **Lean annotation:**
  ```lean
  axiom chameleon_rho_scaling (ρ : ℝ) (m0 : ℝ) :
    m_eff ρ = m0 * (ρ / ρ_ref).pow (1/4)
  -- Justification: Standard chameleon screening mechanism (Khoury–Weltman 2004).
  -- This particular power-law form is observationally motivated, not derived here.
  -- See CAVEATS.md, item C.2 for discussion of alternatives.
  ```

### Type C: Compactification Axioms (string-theory input required)
- **Example:** "K3 fiber is in the S₁,₂ algebraic family" within a Type IIA orientifold
- **Justification:** Identified via exact algebraic sieve; compactification geometry not constructed
- **Discharge path:** Collaboration with string phenomenologists
- **Lean annotation:**
  ```lean
  axiom k3_fiber_in_s12_family :
    ∃ (K3 : ComplexSurface), (Picard K3 = 1) ∧ (PicardFuchsOrder K3 = 3) ∧ 
    (SectionCoefficients K3 = S12Coefficients)
  -- Justification: K3 surfaces with this Hodge signature are rare; S₁,₂ identified 
  -- via exact rational sieve in DISCOVERY_REPORT.md.
  -- Missing: Full orientifold construction (Type IIA/IIB) with flux quantization.
  -- Seeking collaborators: String phenomenologists for item 1 in OPEN_PROBLEMS.md
  ```

### Type D: Empirical Fitting (parameters with known uncertainty range)
- **Example:** λ = 1.6724 ± 0.0521 from DESI BAO
- **Justification:** Maximum-likelihood fit; dataset specified
- **Discharge path:** Not an axiom; state as [FITTED] with explicit error bar in code
- **Code annotation:**
  ```python
  # [FITTED] λ = 1.6724 ± 0.0521 (68% CL) from DESI 2024 BAO fit
  # Loss: -2ln(L) over (w0, wa) grid with H0 = 71.92 (fixed to Cepheid prior)
  # Data: DESI DR1 BAO measurements (Adame et al. 2024), z ∈ [0.1, 4.0]
  # Alternative constraints: Pantheon+ + Planck (λ = 1.58 ± 0.09) — consistent
  lambda_fit = 1.6724
  lambda_fit_err = 0.0521
  ```

## Disclosure Checklist

**Before any axiom or gap is added to the codebase:**

- [ ] **Create Lean axiom** with justification comment (Type A, B, C, or D)
- [ ] **Update OPEN_PROBLEMS.md** with one-line entry
- [ ] **Update CAVEATS.md** with detailed discussion (if Type A, B, or C)
- [ ] **Update VISION.md** publication checklist if blocking (e.g., "Goal II: Compactification [pending]")
- [ ] **Search manuscripts** for any claim depending on this axiom; add caveat to each (see template below)
- [ ] **Add to MEMORY.md** if it's a recurring pattern or collaboration need

## Manuscript Caveat Template

Whenever a result depends on an unproven axiom, add a caveat of this form:

```latex
\textbf{Caveat [AXIOM-ID]:} This result assumes [axiom name]. 
[One sentence: what would happen if assumption were false?] 
See OPEN_PROBLEMS.md (item X) for status and collaboration invitation.
```

**Example for S₂₀ recurrence:**
```latex
\textbf{Caveat A.1:} The stiffness bound depends on the general-n S₂₀ Picard-Fuchs 
recurrence being correct. This has been exact-verified for n ∈ [0, 60] 
(scripts/verify_s20_recurrence.py) but the general proof awaits Wilf-Zeilberger 
certificate compilation (Phase 4, OPEN_PROBLEMS.md item 3).
```

**Example for chameleon scaling:**
```latex
\textbf{Caveat B.1:} The chameleon mass-screening mechanism assumes density-dependent 
scaling m_eff ∝ ρ^{1/4}. If the true screening law differs, superradiance bounds 
shift by 𝒪(1) factors. See CAVEATS.md (C.2) for alternative parametrizations.
```

## The Four-Ledger System

Maintain four linked documents that **must stay synchronized**:

1. **Lean code (`lean4_formal_proofs/Agora/`):** Axioms in source, clearly labeled
2. **CAVEATS.md:** Detailed physics and math implications
3. **OPEN_PROBLEMS.md:** Status, effort estimate, collaboration path
4. **Manuscripts:** Every dependent claim includes caveat reference

**Release-blocking check:** Before tagging a version, grep for unmatched axioms:
```bash
# Find all axioms in Lean
grep -r "^axiom " lean4_formal_proofs/ | awk '{print $2}' > /tmp/lean_axioms.txt

# Find all axiom references in CAVEATS.md
grep -o "\[AXIOM-[A-Z0-9]\+\]" CAVEATS.md | sort -u > /tmp/caveat_axioms.txt

# Check for gaps
comm -23 /tmp/lean_axioms.txt /tmp/caveat_axioms.txt  # Undisclosed axioms
comm -13 /tmp/lean_axioms.txt /tmp/caveat_axioms.txt  # Stale caveat references
```

## Axiom Lifetime Management

| Phase | Status | Action |
|-------|--------|--------|
| **Created** | Pending discharge | Add to OPEN_PROBLEMS.md with timeline estimate |
| **Working** | In progress (e.g., WZ certificate generation) | Update VISION.md roadmap; note in release notes |
| **Ready to discharge** | Formal proof available | Prepare Lean compilation; update all manuscripts |
| **Discharged** | Kernel-verified theorem | Remove `axiom` keyword; update CAVEATS.md to note closure |

Example log entry in VISION.md:
```
[x] **Goal I (partial):** s20_recurrence discharged for n≤8 via `decide`; 
    general law now an explicit `axiom`. 
    ⏱ Pending Phase 4: WZ certificate compilation (2–4 weeks effort).
```

## Handling Axioms from External Libraries

If an axiom comes from a Mathlib import (e.g., `SLT.CoveringNumber`), you still must:

1. **Document the assumption** if it could affect physical claims:
   ```lean
   -- Note: This theorem depends on Mathlib.Topology.CoveringNumber, 
   -- which assumes the ambient space is a metric space. For finite-dimensional 
   -- network weight spaces, this assumption is always satisfied.
   ```

2. **Verify the assumption holds in context** (not just globally true)

3. **Cite in manuscripts** if it impacts rigor claims

## Output: Axiom Audit Report

When reviewing a branch or release, generate a report:

```
AXIOM AUDIT REPORT — Commit [hash]

Type A (Math formalization pending):
  ✓ s20_recurrence (general n) → OPEN_PROBLEMS.md item 3 → Phase 4 discharge path clear
  ⚠ fano_supercongruence_13 → needs numerical verification extension

Type B (Physical axioms):
  ✓ chameleon_rho_scaling → CAVEATS.md B.1 → cited in Part I §2.3 and Part II §3.1
  ⚠ D_brane_geometry_coupling → CAVEATS.md item (missing) → BLOCKING

Type C (Compactification axioms):
  ✗ k3_fiber_in_type_iia_orientifold → OPEN_PROBLEMS.md item 1 → NO MANUSCRIPT CAVEAT → BLOCKING

Type D (Empirical fits):
  ✓ lambda_fit = 1.6724 → empirical_crucible/Agora_Empirical_Validation.ipynb → error bars provided
  ✓ w0, wa → Part II §2.1 → error bars from DESI covariance matrix

BLOCKING ISSUES: 1
  - D-brane coupling axiom not disclosed in any caveat section

RELEASE STATUS: BLOCKED until all Type C axioms appear in manuscripts
```
