# SocrateAI Skills Index — Scientific Rigor Framework

This directory contains a comprehensive set of skills designed to enforce scientific honesty, prevent hallucinations, and ensure rigorous alternatives in the K3-Dark-Matter research project.

## Overview

These skills implement the **8 Core Rules** from `AGENTS.md` and provide concrete, actionable workflows for ensuring:
- ✓ No simulation without execution data (Rule 1)
- ✓ No math claim without kernel verification (Rule 2)
- ✓ No LLM as final arbiter of truth (Rule 3)
- ✓ Extreme skepticism of all outputs (Rule 4)
- ✓ Only real data in sequences (Rule 5)
- ✓ Caveats propagated everywhere (Rule 6)
- ✓ Honest about fits vs. derivations (Rule 7)
- ✓ Cross-consistency across all sources (Rule 8)

---

## The Skills

### 1. **strict-math-verification** (Existing)
**When to use:** Before approving any Lean 4 proof or benchmark claim

Enforces:
- No `sorry` in proofs
- `lake build` verification required
- Physically relevant derivatives
- Execution-backed benchmarks only

**Key workflow:**
```bash
1. Search for `sorry` in modified files
2. Run `lake build` from project root
3. Inspect JSON benchmark outputs
4. Verify initial conditions are physically motivated
```

---

### 2. **claim-classification-audit**
**When to use:** Before submitting any manuscript or documentation; when writing discussion sections

Enforces the three-tier classification:
- **[VERIFIED]** — Kernel-checked or exact-rational
- **[FITTED]** — Phenomenological, calibrated to data
- **[PREDICTED]** — Falsifiable future consequence

**Key workflow:**
```
1. Identify every scientific claim
2. Classify it: VERIFIED? FITTED? PREDICTED?
3. Add justification linking to source (proof module, fit procedure, prediction paper)
4. Search entire manuscript for same claim; all instances use same label
5. Ensure labels never creep upward (don't call FITTED "expected" or PREDICTED "likely")
```

**Example:**
```
✗ WRONG:  "The model explains JWST galaxies"
✓ RIGHT:  "A mass-varying axion with ε=0.0251 [FITTED to JWST] reduces early-universe 
           growth barriers by ΔV/V≈19% [VERIFIED calculation], which is falsifiable by 
           future stellar-mass-function precision [PREDICTED]"
```

---

### 3. **falsifiability-audit**
**When to use:** When writing `PREDICTIONS.md` or proposing any [PREDICTED] claim

Enforces:
- Every [PREDICTED] claim includes a falsification gate
- Precision thresholds are realistic (5-year timeline preferred)
- Measurement method is specified
- Vague hedging ("might," "could") is banned

**Key workflow:**
```
For each prediction:
  1. Observable quantity identified ✓
  2. Theoretical value predicted ✓
  3. Precision threshold given ✓
  4. Timeline attached ✓
  5. Falsification criterion (if measure X, we're ruled out) ✓
```

**Example:**
```
✓ GOOD PREDICTION:
  "S₈(z) exhibits temporal gradient [PREDICTED]; 
   Euclid precision σ<0.01 falsifies if S₈(z) is flat"

✗ VAGUE PREDICTION:
  "The model might predict early galaxies form faster"
```

---

### 4. **axiom-gap-disclosure**
**When to use:** Whenever adding an `axiom` to Lean; before each release

Enforces:
- Every unproven assumption is labeled as `axiom` in Lean
- Every axiom is justified in Lean comments
- Every axiom appears in CAVEATS.md with detailed discussion
- Every axiom appears in OPEN_PROBLEMS.md with discharge path
- Every manuscript depending on an axiom includes a caveat

**Four-ledger system:**
```
1. Lean code (axiom + comment)
2. CAVEATS.md (detailed physics implications)
3. OPEN_PROBLEMS.md (status, effort, collaboration path)
4. Manuscripts (caveat with reference to OPEN_PROBLEMS item)
```

**Example:**
```lean
axiom s20_recurrence (n : ℕ) : 
  P0(n)*S20(n) + P1(n)*S20(n+1) + ... = 0
-- Justification: Exact-verified n∈[0,60] via scripts/verify_s20_recurrence.py
-- Pending: WZ certificate compilation (OPEN_PROBLEMS.md, item 3)
```

Manuscript caveat:
```latex
\textbf{Caveat A.1:} The stiffness bound assumes the S₂₀ Picard-Fuchs recurrence 
for general n. This is exact-verified for n∈[0,60] but awaits kernel proof compilation 
(OPEN_PROBLEMS.md, item 3, Phase 4 timeline).
```

---

### 5. **empirical-data-validation**
**When to use:** Before any empirical result; before submitting papers with fits

Enforces:
- No synthetic data labeled as real
- Data lineage fully documented
- Reproducibility ensured via scripts
- Error bars from data papers propagated
- Fit quality metrics reported (χ²/dof, covariance, residuals)

**Data metadata template:**
```python
# DATASET: DESI DR1 BAO Measurements
# Origin:   Adame et al. 2024, https://zenodo.org/...
# Fetch:    bash scripts/fetch_desi_bao.sh
# Cuts:     z ∈ [0.1, 4.0], systematic errors per DR1 spec
# Last verified: 2024-07-10
# Reproduces: Adame et al. Fig 3 within stated errors ✓
```

**Forbidden:**
```python
# WRONG: Synthetic data
synthetic_desi = solve_ode(params) + noise
fit = fit_to(synthetic_desi)
```

**Required:**
```python
# CORRECT: Real data
real_desi = load_dataset('desi_dr1_bao.csv')  # with metadata comment
fit, chi2 = fit_to(real_desi)
print(f"χ²/dof = {chi2/dof}")  # Always report goodness-of-fit
```

---

### 6. **honest-alternatives-generator**
**When to use:** When a [PREDICTED] is falsified, a [FITTED] produces tension, or an [AXIOM] cannot be discharged

Enforces:
- Three tiers of alternatives: Conservative, Moderate, Radical
- Each alternative is internally consistent (equations provided)
- Each alternative has a falsification gate
- References to prior work included
- Cost-benefit analysis explicit

**Three tiers:**
```
Tier 1 (Conservative): Change parameters only (same structure)
  Example: Adjust field initial condition to hilltop instead of tracking attractor
  
Tier 2 (Moderate): Change one structural assumption
  Example: Add multi-field coupling (V(ϕ,χ) = exp(λϕ) + β·χ·exp(λϕ/2))
  
Tier 3 (Radical): Replace foundational picture
  Example: Dark energy is transient + early radiation-dominated
```

**Example:**
```
TENSION: λ_fit = 1.67 > √2, so single-exponential can't sustain dark energy

TIER 1: Hilltop initial condition
  Mechanism: V(ϕ) = Λ₄(1-cos(ϕ/f))^n, start at ϕ₀ ≈ π
  Prediction: w₀ ≈ -0.99
  Falsify: CMB spectral index running inconsistent with hilltop
  
TIER 2: Multi-field coupling
  Mechanism: V(ϕ,χ) = exp(λϕ) + β·χ·exp(λϕ/2)
  Prediction: w₀ ≈ -0.98, w_a ≈ 0.1
  Falsify: DESI single-field fit has χ² < multi-field by > 5 units
  
TIER 3: Transient dark energy
  Mechanism: Field very light for z > 10, rolls only recently as H → 0
  Prediction: w(a) = const early, decays late; no early-time acceleration
  Falsify: Planck CMB deviations from standard physics, or PTA lines at z > 10
```

---

### 7. **cross-consistency-gate** (Rule 8)
**When to use:** Before every release tag; after major parameter refits

Enforces:
- Every numerical constant (λ, w₀, H₀, m_a, etc.) is identical across:
  - Python code
  - LaTeX manuscripts
  - JSON configs
  - Lean proofs (where applicable)
  - README/documentation

**Master Parameter Ledger** (maintained and committed):
```yaml
lambda_fit:
  value: 1.6724
  uncertainty: ± 0.0521
  references:
    python: "simulations/cosmology_solver.py:47"
    latex: "Part_II_Vafa_DarkEnergy.tex:342"
    json: "k3_gitn_results.json:lambda_fit"
    lean: "SwamplandK3T2.lean:lambda_fit_value"
  status: ✓ CONSISTENT
```

**Pre-release checklist:**
```bash
1. Run scripts/cross_consistency_check.sh → exit code must be 0
2. Inspect PARAMETER_LEDGER.yaml for any ⚠ or ✗ flags
3. Verify uncertainty bars match (code + paper)
4. Search manuscripts for parameter values not in ledger
5. Re-run Jupyter notebooks; verify outputs unchanged
6. Lake build Lean; zero errors
7. Tag and commit ledger
```

---

## Integration Workflow

### When Writing a Paper Section

**Checklist:**
1. ✓ Use `/claim-classification-audit` — Label all claims [VERIFIED/FITTED/PREDICTED]
2. ✓ Use `/falsifiability-audit` — Every [PREDICTED] has falsification gate
3. ✓ Use `/axiom-gap-disclosure` — Every axiom dependency gets a caveat
4. ✓ Use `/empirical-data-validation` — Every fit cites data source, reports χ²/dof
5. ✓ Use `/honest-alternatives-generator` — When tensions arise, propose Tier 1–3 alternatives

### When Finishing a Feature

**Checklist:**
1. ✓ Use `/strict-math-verification` — Lean proofs compile; no `sorry`
2. ✓ Use `/cross-consistency-gate` — Update PARAMETER_LEDGER.yaml; all values match
3. ✓ Use `/empirical-data-validation` — Benchmark with real data only
4. ✓ Use `/axiom-gap-disclosure` — Any new assumptions go in CAVEATS.md

### Before Release

**Checklist (blocking):**
1. ✓ `/cross-consistency-gate` — `scripts/cross_consistency_check.sh` returns 0
2. ✓ `/axiom-gap-disclosure` — All unproven items in OPEN_PROBLEMS.md; all axioms disclosed in manuscripts
3. ✓ `/empirical-data-validation` — All data sources with DOI/retrieval script
4. ✓ `/falsifiability-audit` — All [PREDICTED] claims have precision thresholds + timelines
5. ✓ `/claim-classification-audit` — Audit report generated; no label creep

---

## Example: Applying Skills to a New Result

**Scenario:** You fit quintessence parameters (λ, w₀, w_a) to new DESI data.

**Steps:**

1. **Data validation** `/empirical-data-validation`
   - Add metadata comment to Python code
   - Verify against published DESI DR1 figures
   - Report χ²/dof (you get 2.1; slightly high)

2. **Claim classification** `/claim-classification-audit`
   - λ = 1.6724 is [FITTED to DESI 2024 BAO]
   - Fit prefers thawing trajectory [FITTED observation]
   - Trajectory differs from ΛCDM by X sigma [PREDICTED falsification by Euclid]

3. **Consistency check** `/cross-consistency-gate`
   - Update simulations/cosmology_solver.py with new λ
   - Update Part_II_Vafa_DarkEnergy.tex with new λ in all instances
   - Update k3_gitn_results.json
   - Update PARAMETER_LEDGER.yaml with new uncertainty
   - Run `scripts/cross_consistency_check.sh` ✓

4. **Axiom review** `/axiom-gap-disclosure`
   - The fit assumes chameleon screening (axiom: chameleon_rho_scaling)
   - Caveat already in manuscripts? ✓
   - Should we update OPEN_PROBLEMS.md entry? No change needed.

5. **Alternatives** `/honest-alternatives-generator`
   - New fit still has λ > √2 tension with single-exponential attractor
   - Propose Tier 1 (hilltop), Tier 2 (multi-field), Tier 3 (transient) alternatives
   - Add to Discussion section with falsification gates

6. **Falsifiability** `/falsifiability-audit`
   - New prediction: S₈(z) gradient at Euclid precision falsifies if flat
   - Precision: Euclid σ_{S₈} < 0.01 per bin (design spec) ✓
   - Timeline: Euclid DR1 2026–2028 ✓

7. **Final audit** `/claim-classification-audit`
   - Audit all new claims in manuscript; all labels consistent
   - Ready for submission ✓

---

## When to Invoke Each Skill

| Scenario | Skill | Priority |
|----------|-------|----------|
| Writing manuscript section | claim-classification-audit | HIGH |
| Proposing prediction | falsifiability-audit | HIGH |
| Adding unproven assumption | axiom-gap-disclosure | HIGH |
| Reporting empirical result | empirical-data-validation | HIGH |
| Drafting tension discussion | honest-alternatives-generator | HIGH |
| Before release tag | cross-consistency-gate | BLOCKING |
| Approving Lean proof | strict-math-verification | HIGH |
| Code review | All of the above | HIGH |

---

## Maintenance

These skills are living documents. Update them when:
- New rules are added to AGENTS.md
- Lessons learned from review/refutation
- New tools available (e.g., new Lean libraries, automated checking scripts)

Tag updates in git commits:
```bash
git commit -m "skills: enhance claim-classification-audit with example for Swampland tension"
```

---

## References

- **AGENTS.md** — The 8 core rules (Rules 1–8)
- **VISION.md** — Goals I–III and publication checklist
- **OPEN_PROBLEMS.md** — Outstanding gaps and collaboration needs
- **CAVEATS.md** — Detailed disclosure of all limitations
- **PREDICTIONS.md** — Curated falsifiable predictions manifest
