# S2-1: Singular-Locus-Proximity Observable Design (Preregistration)

**Date:** 2026-07-18 · **Tier:** B (checkable, unproven) · **Status:** PREREGISTRATION DRAFT  
**Authority:** Preregistered by Haiku (design), approved by HUMAN before kernel-swap battery runs.

---

## 1. Motivation: Reframing H3 via F-theory Geometry

### Background: Old Observable Failure

**GATE D-1.3 verdict (2026-07-14, binding):** The FFT-contrast observable
```
Δ(FFT) = |FFT(K3_volume(ρ_b)) − FFT(ρ_b)|
```
is **kernel-blind**. Formally: r(cooper_s7, random_control) = 1.0000. 

**Why it fails (Tier A fact):** FFT contrast measures *nonlinearity* between K3_volume and density. Any smooth monotone transformation produces nonzero contrast (Δ guaranteed nonzero), independent of which kernel (s₇ or s₁₀) generates the mapping. The metric re-detects the density maximum, not K3-specific structure.

### Reframing: Exact Singular Loci as the Observable

**H3 (reframed):** In F-theory, matter is localized where the modulus hits the discriminant locus — the point where the elliptic fiber degenerates. For a given K3 kernel, the exact singular locus is known exactly (from D-2.4):
- **s₇ (Cooper level-7):** z ∈ {−1, 1/27}  
- **s₁₀ (Cooper level-10):** z ∈ {−1/4, 1/16}

These are **kernel-specific**. An observable based on proximity to kernel-specific loci cannot be kernel-blind by construction.

---

## 2. Observable Definition (Tier B: Hypothesis)

**Name:** Singular-Locus-Proximity Observable for kernel K

**Input:** 
- Density field ρ_b (3D grid, 128³ voxels)
- Kernel K ∈ {s₇, s₁₀} (determines singular locus z_crit(K))
- Mapping ρ_b → z via the chameleon ansatz (existing sigmoid, range [0, 1])

**Output:** Proximity metric L_K(ρ_b) defined as:

```
L_K(ρ_b) := ∑_i dist(z_i, z_crit(K)) / N_voxels

where:
  z_i = chameleon_map(ρ_b[i])  [Tier A: existing]
  z_crit(K) = {−1, 1/27} for K=s₇; {−1/4, 1/16} for K=s₁₀  [Tier A: D-2.4]
  dist(z, z_crit) = min |z − z_c| over z_c ∈ z_crit(K)  [Tier A: geometry]
  N_voxels = 128³  [Tier A: grid definition]
```

**Interpretation (Tier B hypothesis):** L_K(ρ_b) quantifies how close the local modulus field gets to the kernel-specific discriminant locus. *Hypothesis*: 
- If ρ_b is structured according to K3 physics (our conjecture), the modulus field will be confined near the singular locus, yielding low L_K.
- If ρ_b is random (noise), the modulus field will be diffuse, yielding high L_K.

**Note on Tier C language:** We are *not* claiming this observable "probes dark matter" or "establishes K3 geometry." That is a Tier C interpretation deferred to theoretical validation post-GATE-D-1v2. Here we state only the mathematical design and hypothesis.

---

## 3. Preregistered Decision Rule (GATE D-1v2 Battery)

Before any data run, we fix the kernel-swap battery and acceptance criterion.

### Kernel-Swap Battery v2

**Purpose:** Determine if L_K(ρ_b) is kernel-specific (cannot distinguish from random data using a random kernel).

**Three-part test:**

#### Test 1: Same-Kernel Signal (s₇ kernel on s₇-model data)
```
L_s7(ρ_b_s7) := apply L_s7 observable to density field sampled from K3 model with kernel s₇
Expected: low (modulus confined near z_crit(s7))
Null: same as random
```

#### Test 2: Same-Kernel Control (s₇ kernel on random-growth-matched data)
```
L_s7(ρ_b_random_s7_matched) := apply L_s7 observable to Poisson/Gaussian random field with same density profile as s₇ run
Expected under H0 (no K3): same distribution as Test 1
Expected under H1 (K3 true): significantly lower than Test 1
```

#### Test 3: Cross-Kernel Rejection (s₇ kernel on s₁₀-model data)
```
L_s7(ρ_b_s10) := apply L_s7 observable to density field from K3 model with kernel s₁₀
Expected: high (modulus confined near z_crit(s10) ≠ z_crit(s7))
Validates that observable is kernel-specific, not just K3-generic
```

### Decision Threshold (Preregistered)

**Acceptance criterion for GATE D-1v2 PASS:**

The observable L_K passes if **all three conditions hold**:

1. **Kernel specificity:** L_s7(ρ_b_s7) < L_s7(ρ_b_random_s7) by ≥2σ (where σ is the mock ensemble std)
2. **Same for s₁₀:** L_s₁₀(ρ_b_s10) < L_s₁₀(ρ_b_random_s10) by ≥2σ
3. **Cross-kernel rejection:** L_s7(ρ_b_s10) > L_s7(ρ_b_s7) by ≥2σ (observable correctly rejects wrong kernel)

**Threshold determination:** 
- Generate 1000 mock Poisson density fields at reference (ρ_b=0.28)
- Compute L_K for each mock
- Derive empirical σ_mock
- Set threshold as mean_mock ± 2·σ_mock

**Note on Tier B:** This is a *conjectured* design. Whether L_K actually achieves 2σ separation is an empirical question to be answered by the kernel-swap battery. A failure to pass does not invalidate the logic — it simply means this particular proximity metric is not sensitive enough (a design iteration would follow).

---

## 4. Implementation Roadmap

### Phase A: Preregistration Lock (this document)
- [x] Observable definition fixed (no changes post-preregistration)
- [x] Decision rule committed (no post-hoc threshold selection)
- [x] This file will be committed to repo before running any battery

### Phase B: Mock Calibration (Haiku tier)
- [ ] Generate 1000 Poisson mocks at reference density
- [ ] Compute L_K for each mock
- [ ] Derive empirical null distribution + σ_mock
- [ ] Output: `data/k3t2/s2_1_mock_calibration.json` (mean, std, quantiles)

### Phase C: Kernel-Swap Battery v2 (Haiku tier)
- [ ] Run L_s7 on 100 s₇-model samples (ρ_b from K3 s₇ physics)
- [ ] Run L_s7 on 100 random-matched samples
- [ ] Run L_s₁₀ on 100 s₁₀-model samples
- [ ] Run L_s₁₀ on 100 random-matched samples
- [ ] Cross-kernel tests: L_s7(s₁₀_model), L_s₁₀(s₇_model)
- [ ] Output: `data/k3t2/d1_3b_kernel_swap_v2.json` (all results + z-scores vs mock)

### Phase D: GATE D-1v2 Adjudication (HUMAN)
- [ ] HUMAN reviews kernel-swap results
- [ ] HUMAN decision: PASS (proceed to D-3) or FAIL (iterate design)
- [ ] Decision recorded in `data/k3t2/GATE_D1v2_DECISION.md`

---

## 5. Epistemic Compliance Checklist

- [x] Observable design stated as Tier B (hypothesis, checkable)
- [x] Mathematical components traced to Tier A (D-2.4 loci, chameleon map)
- [x] Preregistration locked before execution
- [x] Decision threshold objective (2σ, computed from mocks, not post-hoc)
- [x] No Tier C language ("predicts", "establishes") without conjecture marker
- [x] Kernel-specific by construction (loci differ for s₇ vs s₁₀)
- [x] Failure path defined (allows design iteration if GATE D-1v2 fails)
- [x] Provenance footer present (below)

---

**Generated-by:** Haiku 4.5 (S2-1 design phase) | **Verified-by:** epistemic-guardrails skill | **Reviewed-by:** HUMAN approval pending

*This preregistration is binding. No changes to observable definition, decision rule, or threshold after commit.*
