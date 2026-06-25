import Mathlib

/-- 
  The string compactification mass calibration.
  Derived from Svrcek & Witten (2006) for instanton action in Calabi-Yau/K3 compactifications.
-/

noncomputable def string_scale (M_pl V : ℝ) : ℝ :=
  M_pl / Real.sqrt V

noncomputable def instanton_action (tau : ℝ) : ℝ :=
  2 * Real.pi * tau

noncomputable def axion_mass_sq (M_s f_a d_sum : ℝ) : ℝ :=
  (M_s^4 / f_a^2) * d_sum

noncomputable def axion_mass (M_pl V tau : ℝ) (q : ℕ → ℝ) (d_max : ℕ) : ℝ :=
  let d_sum := ∑' (d : ℕ), if d ≤ d_max then (d : ℝ)^2 * q d * Real.exp (-2 * Real.pi * d * tau) else 0
  (M_pl / Real.sqrt V) * Real.sqrt d_sum

theorem instanton_positivity {tau d : ℝ} (htau : tau > 0) (hd : d > 0) :
  Real.exp (-2 * Real.pi * d * tau) > 0 :=
by
  exact Real.exp_pos _

/-- 
  If the volume modulus is positive and the instanton sum is positive, 
  the axion mass is strictly positive.
-/
theorem axion_mass_pos {M_pl V inst_sum : ℝ} 
  (hM : M_pl > 0) (hV : V > 0) (h_inst : inst_sum > 0) :
  (M_pl / Real.sqrt V) * Real.sqrt inst_sum > 0 :=
by
  have h1 : M_pl / Real.sqrt V > 0 := div_pos hM (Real.sqrt_pos.mpr hV)
  have h2 : Real.sqrt inst_sum > 0 := Real.sqrt_pos.mpr h_inst
  exact mul_pos h1 h2
