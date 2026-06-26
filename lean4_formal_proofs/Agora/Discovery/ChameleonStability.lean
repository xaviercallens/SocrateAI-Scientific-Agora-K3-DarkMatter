import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Pow.Deriv
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul

open Real

namespace Agora.Discovery.ChameleonStability

noncomputable def m_eff (m0 ρ_crit γ ρ_b : ℝ) : ℝ :=
  m0 * (1 + ρ_b / ρ_crit) ^ γ

theorem m_eff_vacuum (m0 ρ_crit γ : ℝ) : m_eff m0 ρ_crit γ 0 = m0 := by
  unfold m_eff
  rw [zero_div, add_zero, Real.one_rpow, mul_one]

theorem m_eff_pos (m0 ρ_crit γ ρ_b : ℝ) (hm0 : 0 < m0) (hρ_crit : 0 < ρ_crit) (hρ_b : 0 ≤ ρ_b) :
    0 < m_eff m0 ρ_crit γ ρ_b := by
  unfold m_eff
  apply mul_pos hm0
  apply Real.rpow_pos_of_pos
  have h1 : 0 ≤ ρ_b / ρ_crit := div_nonneg hρ_b (le_of_lt hρ_crit)
  linarith

theorem m_eff_mono (m0 ρ_crit γ ρ_b1 ρ_b2 : ℝ) 
    (hm0 : 0 < m0) (hρ_crit : 0 < ρ_crit) (hγ : 0 < γ)
    (h1 : 0 ≤ ρ_b1) (h2 : ρ_b1 < ρ_b2) :
    m_eff m0 ρ_crit γ ρ_b1 < m_eff m0 ρ_crit γ ρ_b2 := by
  unfold m_eff
  apply mul_lt_mul_of_pos_left _ hm0
  apply Real.rpow_lt_rpow
  · have h3 : 0 ≤ ρ_b1 / ρ_crit := div_nonneg h1 (le_of_lt hρ_crit)
    linarith
  · have h4 : ρ_b1 / ρ_crit < ρ_b2 / ρ_crit := div_lt_div_of_pos_right h2 hρ_crit
    linarith
  · exact hγ

/-- The formal derivative of the effective mass with respect to ρ_b. -/
noncomputable def m_eff_deriv (m0 ρ_crit γ ρ_b : ℝ) : ℝ :=
  m0 * γ * (1 + ρ_b / ρ_crit) ^ (γ - 1) * (1 / ρ_crit)

/--
Theorem: The formal derivative of the Chameleon effective mass matches the analytical derivative.
Verifies the exact coupling derivative required for stability and monotonicity.
-/
theorem m_eff_has_deriv_at (m0 ρ_crit γ ρ_b : ℝ) (hρ_crit : 0 < ρ_crit) (hρ_b : 0 ≤ ρ_b) :
    HasDerivAt (fun ρ => m_eff m0 ρ_crit γ ρ) (m_eff_deriv m0 ρ_crit γ ρ_b) ρ_b := by
  dsimp [m_eff, m_eff_deriv]
  have h_inner : HasDerivAt (fun ρ => 1 + ρ / ρ_crit) (1 / ρ_crit) ρ_b := by
    have h_one : HasDerivAt (fun _ => (1 : ℝ)) 0 ρ_b := hasDerivAt_const ρ_b 1
    have h_div : HasDerivAt (fun ρ => ρ / ρ_crit) (1 / ρ_crit) ρ_b := by
      have h_eq : (fun ρ => ρ / ρ_crit) = (fun ρ => (1 / ρ_crit) * ρ) := by
        ext x
        ring
      rw [h_eq]
      have h_id := hasDerivAt_id ρ_b
      have h_mul := HasDerivAt.const_mul (1 / ρ_crit) h_id
      have h_ring : (1 / ρ_crit) * 1 = 1 / ρ_crit := by ring
      have h_res := h_ring ▸ h_mul
      exact h_res
    have h_add := HasDerivAt.add h_one h_div
    have h_ring : 0 + 1 / ρ_crit = 1 / ρ_crit := by ring
    exact h_ring ▸ h_add

  have h_base_pos : 1 + ρ_b / ρ_crit ≠ 0 := by
    have h1 : 0 ≤ ρ_b / ρ_crit := div_nonneg hρ_b (le_of_lt hρ_crit)
    linarith
  have h_rpow := hasDerivAt_rpow_const (Or.inl h_base_pos) (p := γ)
  have h_comp := HasDerivAt.comp ρ_b h_rpow h_inner
  have h_tot := HasDerivAt.const_mul m0 h_comp
  have h_eq_deriv : m0 * (γ * (1 + ρ_b / ρ_crit) ^ (γ - 1) * (1 / ρ_crit)) =
                    m0 * γ * (1 + ρ_b / ρ_crit) ^ (γ - 1) * (1 / ρ_crit) := by ring
  exact h_eq_deriv ▸ h_tot

end Agora.Discovery.ChameleonStability
