import Mathlib.Data.Rat.Defs
import Mathlib.Tactic

namespace BlackHole

/-- A concrete 2x2 matrix over rational numbers ℚ representing a quantum density operator. -/
structure DensityMatrix2 where
  a : ℚ  -- rho_11
  b : ℚ  -- rho_12
  c : ℚ  -- rho_21
  d : ℚ  -- rho_22
  deriving DecidableEq, Repr

namespace DensityMatrix2

/-- Matrix addition. -/
def add (A B : DensityMatrix2) : DensityMatrix2 :=
  ⟨A.a + B.a, A.b + B.b, A.c + B.c, A.d + B.d⟩

/-- Matrix multiplication. -/
def mul (A B : DensityMatrix2) : DensityMatrix2 :=
  ⟨A.a * B.a + A.b * B.c, A.a * B.b + A.b * B.d,
   A.c * B.a + A.d * B.c, A.c * B.b + A.d * B.d⟩

/-- The trace of a 2x2 matrix is the sum of its diagonal elements. -/
def trace (A : DensityMatrix2) : ℚ :=
  A.a + A.d

/-- A density matrix is normalized if its trace equals 1 (trace conservation). -/
def is_normalized (A : DensityMatrix2) : Prop :=
  trace A = 1

/-- A matrix is a projection operator if A^2 = A. -/
def is_projection (A : DensityMatrix2) : Prop :=
  mul A A = A

/-- The purity of a state is the trace of its square: Tr(rho^2). -/
def purity (A : DensityMatrix2) : ℚ :=
  trace (mul A A)

/-- Positive semi-definiteness algebraic condition for a symmetric 2x2 rational matrix:
    both diagonal elements are non-negative, and the determinant is non-negative. -/
def is_psd (A : DensityMatrix2) : Prop :=
  A.a ≥ 0 ∧ A.d ≥ 0 ∧ A.a * A.d - A.b * A.c ≥ 0

/-- Theorem: Any projection operator (mul A A = A) that is normalized (trace = 1)
    has a purity of exactly 1.
    This formalizes the pure state criterion for information conservation. -/
theorem purity_of_normalized_projection (A : DensityMatrix2) (hn : is_normalized A) (hp : is_projection A) :
    purity A = 1 := by
  unfold purity
  unfold is_projection at hp
  rw [hp]
  exact hn

/-- Theorem: For any rational matrix A_gen = [[x, y], [z, w]], the unnormalized
    operator rho_un = A_gen * A_gen^T is positive semi-definite (is_psd). -/
theorem uuT_is_psd (x y z w : ℚ) :
    let rho_un := DensityMatrix2.mk (x^2 + y^2) (x*z + y*w) (x*z + y*w) (z^2 + w^2)
    is_psd rho_un := by
  intro rho_un
  unfold is_psd
  refine ⟨?_, ?_, ?_⟩
  · dsimp [rho_un]
    have h1 : x^2 ≥ 0 := sq_nonneg x
    have h2 : y^2 ≥ 0 := sq_nonneg y
    linarith
  · dsimp [rho_un]
    have h1 : z^2 ≥ 0 := sq_nonneg z
    have h2 : w^2 ≥ 0 := sq_nonneg w
    linarith
  · dsimp [rho_un]
    -- Determinant check: (x^2 + y^2)(z^2 + w^2) - (xz + yw)^2 = (xw - yz)^2 >= 0
    have h_det : (x^2 + y^2) * (z^2 + w^2) - (x*z + y*w) * (x*z + y*w) = (x*w - y*z)^2 := by ring
    rw [h_det]
    exact sq_nonneg (x*w - y*z)

/-- Theorem: For any rational matrix A_gen, if the trace of the unnormalized density operator
    rho_un is non-zero, then normalizing by the trace yields a valid state with trace = 1. -/
theorem trace_of_normalized_is_one (x y z w : ℚ) (ht_nz : (x^2 + y^2) + (z^2 + w^2) ≠ 0) :
    let rho_un := DensityMatrix2.mk (x^2 + y^2) (x*z + y*w) (x*z + y*w) (z^2 + w^2)
    let tr := trace rho_un
    let rho_norm := DensityMatrix2.mk (rho_un.a / tr) (rho_un.b / tr) (rho_un.c / tr) (rho_un.d / tr)
    is_normalized rho_norm := by
  intro rho_un tr rho_norm
  unfold is_normalized trace
  dsimp [rho_norm, rho_un, tr, trace]
  have h_tr : tr = (x^2 + y^2) + (z^2 + w^2) := by rfl
  have h_tr_nz : tr ≠ 0 := by
    rw [h_tr]
    exact ht_nz
  field_simp [h_tr_nz]
  try ring

end DensityMatrix2
end BlackHole
