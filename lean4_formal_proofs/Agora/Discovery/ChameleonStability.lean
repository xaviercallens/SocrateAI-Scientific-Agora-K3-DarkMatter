import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

open Real

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
