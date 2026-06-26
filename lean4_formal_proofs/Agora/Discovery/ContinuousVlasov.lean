import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring

namespace Agora.Discovery.ContinuousVlasov

/-- The continuous Taylor series sequences representing the 3 moments of the linearized
    Vlasov-Poisson equation (waterbag closure).
    y0 is density, y1 is momentum, y2 is pressure. -/
def is_continuous_vlasov_sequence (K : ℚ) (y0 y1 y2 : ℕ → ℚ) : Prop :=
  ∀ n : ℕ,
    (n + 1 : ℚ) * y0 (n + 1) = y1 n ∧
    (n + 1 : ℚ) * y1 (n + 1) = y2 n - y0 n ∧
    (n + 1 : ℚ) * y2 (n + 1) = K * y1 n

/-- The exact continuous-time recurrence relation for the density Taylor coefficients. -/
theorem vlasov_continuous_recurrence_exact (K : ℚ) (y0 y1 y2 : ℕ → ℚ)
    (h : is_continuous_vlasov_sequence K y0 y1 y2) :
    ∀ n : ℕ, ((n + 3 : ℚ) * (n + 2 : ℚ)) * y0 (n + 3) = (K - 1) * y0 (n + 1) := by
  intro n
  
  have eq1 : (n + 3 : ℚ) * y0 (n + 3) = y1 (n + 2) := by
    have h1 := (h (n + 2)).1
    have s1 : ((n + 2 : ℕ) + 1 : ℚ) = (n + 3 : ℚ) := by push_cast; ring
    rw [← s1]
    exact h1
    
  have eq2 : (n + 2 : ℚ) * y1 (n + 2) = y2 (n + 1) - y0 (n + 1) := by
    have h2 := (h (n + 1)).2.1
    have s1 : ((n + 1 : ℕ) + 1 : ℚ) = (n + 2 : ℚ) := by push_cast; ring
    rw [← s1]
    exact h2

  have eq3 : (n + 1 : ℚ) * y2 (n + 1) = K * y1 n := by
    exact (h n).2.2
    
  have eq4 : (n + 1 : ℚ) * y0 (n + 1) = y1 n := by
    exact (h n).1
    
  have left_step : ((n + 3 : ℚ) * (n + 2 : ℚ)) * y0 (n + 3) = (n + 2 : ℚ) * y1 (n + 2) := by
    calc ((n + 3 : ℚ) * (n + 2 : ℚ)) * y0 (n + 3)
      _ = (n + 2 : ℚ) * ((n + 3 : ℚ) * y0 (n + 3)) := by ring
      _ = (n + 2 : ℚ) * y1 (n + 2) := by rw [eq1]
      
  have main_eq : ((n + 3 : ℚ) * (n + 2 : ℚ)) * y0 (n + 3) = y2 (n + 1) - y0 (n + 1) := by
    rw [left_step, eq2]

  have eq_y2 : (n + 1 : ℚ) * y2 (n + 1) = (n + 1 : ℚ) * (K * y0 (n + 1)) := by
    calc (n + 1 : ℚ) * y2 (n + 1)
      _ = K * y1 n := eq3
      _ = K * ((n + 1 : ℚ) * y0 (n + 1)) := by rw [← eq4]
      _ = (n + 1 : ℚ) * (K * y0 (n + 1)) := by ring

  have n_plus_1_ne_zero : (n + 1 : ℚ) ≠ 0 := by
    intro hc
    have h_nat : (n + 1 : ℚ) = (↑(n + 1) : ℚ) := by simp
    rw [h_nat] at hc
    norm_cast at hc

  have eq_y2_simple : y2 (n + 1) = K * y0 (n + 1) := by
    exact mul_left_cancel₀ n_plus_1_ne_zero eq_y2
    
  calc ((n + 3 : ℚ) * (n + 2 : ℚ)) * y0 (n + 3)
    _ = y2 (n + 1) - y0 (n + 1) := main_eq
    _ = K * y0 (n + 1) - y0 (n + 1) := by rw [eq_y2_simple]
    _ = (K - 1) * y0 (n + 1) := by ring

end Agora.Discovery.ContinuousVlasov
