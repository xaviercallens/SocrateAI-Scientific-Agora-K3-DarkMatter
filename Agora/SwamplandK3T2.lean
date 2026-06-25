import Mathlib.Data.Real.Basic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.SpecialFunctions.ExpDeriv

noncomputable def V (V_0 c r : ℝ) : ℝ :=
  V_0 * Real.exp (-c * r)

noncomputable def grad_V (V_0 c r : ℝ) : ℝ :=
  -c * V_0 * Real.exp (-c * r)

theorem V_has_deriv_at (V_0 c r : ℝ) :
  HasDerivAt (fun x => V V_0 c x) (grad_V V_0 c r) r := by
  dsimp [V, grad_V]
  have h1 : HasDerivAt (fun x => -c * x) (-c) r := by
    simpa using HasDerivAt.const_mul (-c) (hasDerivAt_id r)
  have h2 : HasDerivAt (fun x => Real.exp (-c * x)) (Real.exp (-c * r) * -c) r := by
    exact HasDerivAt.comp r (Real.hasDerivAt_exp (-c * r)) h1
  have h3 : HasDerivAt (fun x => V_0 * Real.exp (-c * x)) (V_0 * (Real.exp (-c * r) * -c)) r := by
    exact HasDerivAt.const_mul V_0 h2
  have h_eq : V_0 * (Real.exp (-c * r) * -c) = -c * V_0 * Real.exp (-c * r) := by ring
  exact h_eq ▸ h3

theorem swampland_bound (V_0 c r : ℝ) (hV0 : V_0 > 0) (hc : c > 0) :
  |grad_V V_0 c r| = c * (V V_0 c r) := by
  rw [grad_V, V]
  have h_prod : c * V_0 * Real.exp (-c * r) > 0 := by
    positivity
  calc |-c * V_0 * Real.exp (-c * r)|
    _ = |-(c * V_0 * Real.exp (-c * r))| := by ring_nf
    _ = |c * V_0 * Real.exp (-c * r)| := by rw [abs_neg]
    _ = c * V_0 * Real.exp (-c * r) := abs_of_pos h_prod
    _ = c * (V_0 * Real.exp (-c * r)) := by ring
