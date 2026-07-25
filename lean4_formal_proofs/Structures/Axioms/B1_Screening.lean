-- Axioms/B1_Screening.lean
-- Chameleon screening mechanism formalization (WP-B1)
--
-- Defines the chameleon scalar field Φ as dependent on environment density ρ,
-- with screening potential V_eff(Φ, ρ) and environment-dependent effective mass m_eff(ρ).
--
-- Source: [astro-ph/0309411] Khoury-Weltman screening; [1109.2709] cosmological chameleon
--
-- NOTE (2026-07-25, Sonnet 5 fix): the previous revision of this file used
-- `noncomputable constant ...` (not a Lean 4 keyword — `constant` was removed
-- from the language) and relied on file-scope `variable` auto-binding, which
-- silently changed the arity of downstream `def`s. Physical constants are
-- now genuine top-level `axiom`s, matching this file's own name/purpose.

import Mathlib.Analysis.Real.Sqrt
import Mathlib.Data.NNReal.Basic

open scoped NNReal

namespace B1_Screening

/-! Chameleon scalar field definition and screening properties -/

-- Environment density type (non-negative reals)
abbrev EnvDensity : Type := ℝ≥0

-- Scalar field type (real-valued)
structure Scalar where
  value : ℝ

/-! Field constants and axioms -/

-- Bare mass (constant, not density-dependent)
axiom m_bare : ℝ≥0

-- Background coupling strength (dimensionless)
axiom α_ch : ℝ≥0

-- Critical density threshold (dimensionless)
axiom ρ_env : ℝ≥0

-- Maximum screening constant (dimensionless, order unity)
axiom C_max : ℝ≥0
axiom C_max_positive : C_max > 0

-- Minimum screening constant (dimensionless, order unity)
axiom C_min : ℝ≥0
axiom C_min_positive : C_min > 0
axiom C_min_le_C_max : C_min ≤ C_max

/-! Chameleon effective mass (density-dependent) -/

-- V_eff(Φ, ρ) = V_bare(Φ) + ρ * Φ
-- The second term (ρ*Φ) induces environment-dependent mass
-- In the quadratic case: m_eff²(ρ) = m_bare² + ρ

noncomputable def m_eff_squared (ρ : EnvDensity) : ℝ :=
  (m_bare : ℝ) ^ 2 + (ρ : ℝ)

noncomputable def m_eff (ρ : EnvDensity) : ℝ :=
  Real.sqrt (m_eff_squared ρ)

/-! Screening radius (inverse mass scale) -/

-- r_S(ρ, m_eff) ∝ 1/m_eff(ρ). The `+ 1` keeps the denominator strictly
-- positive without a case split on ρ = 0 ∧ m_bare = 0.
-- In screened regime: r_S ~ 1 mm to 1 meter
-- Unscreened regime (false): r_S ~ Mpc scale

noncomputable def screening_radius (ρ : EnvDensity) : ℝ :=
  (C_max : ℝ) / (m_eff ρ + 1)

/-! Chameleon field type (environment-indexed) -/

-- The chameleon field Φ is indexed by environment density ρ
-- For each density, we have a corresponding field configuration
noncomputable def chameleon_field (ρ : EnvDensity) : Scalar :=
  { value := (ρ : ℝ) * (m_eff ρ) ^ (-2 : ℤ) }

/-! Coupling to brane system (B3 local EFT) -/

-- The coupling site where chameleon couples to elliptic brane
-- Structure: field value × coupling strength × density dependence
structure BraneCouplingVertex where
  field_value : ℝ
  coupling_strength : ℝ≥0
  environment_density : EnvDensity

noncomputable def brane_coupling_site (ρ : EnvDensity) : BraneCouplingVertex :=
  {
    field_value := (chameleon_field ρ).value
    coupling_strength := α_ch
    environment_density := ρ
  }

/-! Screening condition verification -/

-- The central claim: effective mass always increases with density
theorem m_eff_monotone (ρ₁ ρ₂ : EnvDensity) (h : ρ₁ ≤ ρ₂) :
    m_eff ρ₁ ≤ m_eff ρ₂ := by
  simp only [m_eff, m_eff_squared]
  have h_coe : (ρ₁ : ℝ) ≤ (ρ₂ : ℝ) := by exact_mod_cast h
  exact Real.sqrt_le_sqrt (by linarith)

-- Screening radius is bounded above by C_max (using the `+ 1` denominator floor)
theorem screening_radius_bounded (ρ : EnvDensity) :
    screening_radius ρ ≤ (C_max : ℝ) := by
  simp only [screening_radius]
  have h_nonneg : m_eff ρ ≥ 0 := Real.sqrt_nonneg _
  have h_denom : m_eff ρ + 1 > 0 := by linarith
  have hC : (C_max : ℝ) > 0 := NNReal.coe_pos.mpr C_max_positive
  rw [div_le_iff₀ h_denom]
  nlinarith [hC, h_nonneg]

end B1_Screening
