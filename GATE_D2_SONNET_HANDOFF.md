# 🎯 GATE D-2: Sonnet Tier Handoff

**Status:** READY (GATE R-0 ✅ closed, commit c3a1b37)  
**Date:** 2026-07-14  
**For:** Claude Sonnet (derivations, theory, non-decide Lean proofs)

---

## What Haiku completed (R-0)

✅ Lean file repaired (broken file → drafts/, math-only replacement deployed)  
✅ False doc claims corrected (audit notices added)  
✅ Provenance tagging live (data_provenance field, synthetic discoveries blocked)  
✅ Bounded observable deployed (period_bounded ∈ [0,1], dynamic range < 2)  
✅ Mock test passes with bounded observable

**Commit:** c3a1b37 `fix(R-0): rigor repair — Lean file quarantine, provenance tagging, bounded observable`

---

## What Sonnet must do (D-2)

**D-2.1: Resolve m_eff(Δ) contradiction**

Currently two inconsistent laws exist in the codebase:
1. `m_eff(Δ) = m₀ · exp(kΔ)` with k ≈ 0.048 (Part VI manuscript / memory)
2. `m_eff(Δ) ≈ m₀(1 + κΔ)^{1/4}` (AGORA_K3_T2_BRIDGE_PLAN.md)

**Task:**
- Derive the correct small-Δ law from the chameleon potential V(φ) + conformal coupling A(φ)ρ_b
- Standard chameleon scaling is m_eff ∝ ρ^{(n+2)/(2n+2)} — identify the correct n
- Verify which (exp vs. quartic) is the correct small-Δ limit
- Create `docs/derivations/meff_delta_law.md` with assumption ledger and Taylor-series agreement test

**Output:** one unified m_eff law; both older formulas explicitly deprecated in manuscripts

---

**D-2.2: Derive or parameterize ρ_b → z**

Current implementation: ad-hoc sigmoid (acknowledged in comments as un-parameterized).

**Task:**
- Either: derive from the D-2.1 coupling (ρ_b modulates z via A(φ)ρ_b term)
- Or: declare a 2-parameter ansatz family z(ρ; a, b) and **marginalize over (a,b) in all downstream statistics**
- Create API: `density_to_modulus(rho, params={'a': ?, 'b': ?})`
- Perform sensitivity grid: does the D-1.3 kernel-swap verdict survive across the (a,b) parameter space?

**Output:** derivation doc + updated Python API + sensitivity table

---

**D-2.3: T² sector formalization (the "×T²" half)**

The K3×T² hypothesis currently has no T² formalization in code.

**Task (Python):**
- `lss_tensor_analytics/t2_modulus.py` — KK tower masses m²_{n,m}(τ) as a function of the Kähler modulus τ = τ₁ + iτ₂
- Compute KK contributions to m_eff
- Implement see-saw evolution ansatz τ(z_eq) for "freeze-out" interpretation
- Document the Chameleon-induced τ feedback (how does ρ_b affect τ?)

**Task (Lean):**
- `Structures/T2Lattice.lean` — *math-only, no physics theorem names per Rule 4*
  - Gaussian-integer-like lattice Λ in ℂ
  - Positive-definite quadratic form |n + mτ|² / Im(τ)
  - `decide`-provable spectrum facts for concrete rational τ on ℚ[i]
  - Do NOT state "supersymmetry", "T-duality", or "moduli stabilization" in theorem names

**Output:** Python module + Lean math file (both compiling, zero sorry)

---

**D-2.4: s₇ vs s₁₀ discriminant (activated if D-1.3 declares degeneracy)**

If the mock calibration in GATE D-1 shows that the observable cannot distinguish cooper_s7 from cooper_s10, this task activates.

**Task:**
- Compute exact singular-point loci of the Picard–Fuchs operators for both sequences
- They differ in modular level (7 vs 10) ⇒ different singularities ⇒ different critical densities ρ_crit
- Predict the ρ_crit ratio and the corresponding (z, Δ) signatures
- Create `data/k3t2/d2_4_singular_loci.json` (exact loci in ℚ or algebraic-number form)
- Register the prediction BEFORE any new empirical runs (preregistration)

**Activation condition:** D-1.3 verdict shows r(s7, s10) > 0.95  
**If not activated:** document "spectral degeneracy confirmed" as publishable result

**Output:** singular-locus JSON + discrimination strategy doc

---

**D-2.5: Clean up the Lean K3 topology layer**

The quarantined file had "rigidity," "mirror symmetry," "monodromy" as physics theorem names. Replace with math-only content.

**Task:**
- Enhance `Structures/CooperS7_Topology.lean` only if needed
- OR create a separate `Structures/K3TopologyMath.lean` with *only* Betti vectors, χ = 24, leading-coeff positivity — all provable by `decide` or `ring`
- NO physics claims in theorem names
- Ensure all compiles (lake build → exit 0, zero sorry)

**Output:** math-only Lean module, validated

---

## Preregistration & Decision Rules

**Before running D-1 empirical work, commit:**
- [ ] `docs/derivations/meff_delta_law.md` (one law, others deprecated)
- [ ] `lss_tensor_analytics/t2_modulus.py` (functional, documented)
- [ ] `Structures/T2Lattice.lean` (compiling, zero sorry)
- [ ] `data/k3t2/d2_4_singular_loci.json` (exact loci, s7 & s10 both)
- [ ] Sensitivity grid results (ρ→z parameterization robustness)

These are *not* empirical results; they are theory inputs and discriminants. Commit them first.

---

## What comes after D-2 (Haiku's D-1 + D-3)

Once Sonnet closes D-2:
1. **Haiku:** GATE D-1 (mock ensembles, kernel-swap battery, calibrated p-values)
2. **Haiku:** GATE D-3 (calibrated empirical reruns: sweep, tomography, TDA, lensing)
3. **HUMAN:** GATE-E (publication/outreach decision)

---

**Next step:** Sonnet begins D-2.1 (m_eff law derivation). Ping when ready to commit.

Good luck! 🚀
