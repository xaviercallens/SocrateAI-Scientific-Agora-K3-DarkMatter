import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace Agora.Discovery.UniversalScaling

/-- 
The theoretical soliton-halo mass scaling relation in Fuzzy Dark Matter.
Mc = alpha * Mh^(1/3).
-/
noncomputable def SolitonMass (M_h alpha : ℝ) : ℝ :=
  alpha * M_h ^ (1/3 : ℝ)

/--
Theorem: The soliton mass scaling relation is homogeneous of degree 1/3.
Scaling the parent halo mass by a factor of lambda scales the soliton mass by lambda^(1/3).
-/
theorem soliton_mass_scaling_homogeneity (M_h alpha lambda : ℝ) (hM : 0 ≤ M_h) (hl : 0 ≤ lambda) :
    SolitonMass (lambda * M_h) alpha = lambda ^ (1/3 : ℝ) * SolitonMass M_h alpha := by
  dsimp [SolitonMass]
  rw [Real.mul_rpow hl hM]
  ring

end Agora.Discovery.UniversalScaling
