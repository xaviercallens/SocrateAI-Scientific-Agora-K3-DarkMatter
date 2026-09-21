/-
  Stream2Lean/CMPoints.lean — kernel-checked INSTANCES behind Stream 2's 2026-09-21 certificates
  (`CM_POINTS_RHO20.json`, `A2_MEMBERSHIP.json`, `ATKIN_LEHNER_DISC_FORM.json`).

  Built on LeanMaster's lattice API (`Gram`, `latticeNorm`, `reflection`, `reflection_isometry`,
  `reflection_involution`) and Mathlib. See `lakefile.lean` for the status of that dependency:
  it is a TRIAL rebuild of LeanMaster v3.45.0 at lean/mathlib v4.34.0.

  SCOPE. These are statements about explicit integer vectors and matrices, and about squares in
  `ZMod`. They are the finite arithmetic the Python checkers compute, nothing more. NOT here, and
  staying Tier B: that `U ⊕ ⟨2n⟩` is the transcendental lattice of the cooper_s7 / cooper_s10
  families; that `v·ω = 0` makes the member ρ = 20 with `T_X = v^⊥` (Dolgachev 1996 §7, read, not
  proved); every z-value (numeric recognition through a relation certified PASS(40)); and the
  general criterion "D occurs iff D is a square mod 4n", of which only the two instances that
  matter are checked below. cooper_s10 is ADVISORY (lattice certificate DRAFT). No selection, no
  physical reading (VISION §1.3; Tier C blocked, F5b). Stream 1 owns the general theorems; these
  instances are offered to them as targets, not as a parallel development.
-/
import DualScaleStream2.Lattice.Hyperbolic
import DualScaleStream2.Lattice.Reflection
import Mathlib.Tactic

namespace Stream2Lean.CMPoints

open Matrix DualScaleStream2.Lattice

/-- `U ⊕ ⟨2N⟩` in the basis `(e, f, w)`; same convention as Stream 1's `MnLattice.TN`. -/
def TN (N : ℤ) : Gram 3 := !![0, 1, 0; 1, 0, 0; 0, 0, 2 * N]

theorem TN_symm (N : ℤ) : (TN N)ᵀ = TN N := by
  ext i j; fin_cases i <;> fin_cases j <;> rfl

/-- Norm form `2xy + 2N z²`. -/
theorem TN_norm (N x y z : ℤ) : latticeNorm (TN N) ![x, y, z] = 2 * x * y + 2 * N * z ^ 2 := by
  simp [latticeNorm, TN, dotProduct, mulVec, Fin.sum_univ_succ]; ring

-- ── the singular-locus vectors of `CM_POINTS_RHO20.json` ─────────────────────────────

/-- s7, z = 1/27 (Fricke point): `(1,−1,0)` is a `(−2)`-vector, for every level. -/
theorem fricke_vector_norm (N : ℤ) : latticeNorm (TN N) ![1, -1, 0] = -2 := by
  rw [TN_norm]; ring

/-- s7, z = −1: `(2,−4,1)` is a `(−2)`-vector of `U ⊕ ⟨14⟩`. -/
theorem s7_second_wall_norm : latticeNorm (TN 7) ![2, -4, 1] = -2 := by
  rw [TN_norm]; norm_num

/-- s7, z = ∞: `(14,−14,5)` has norm `−42` — NOT a `(−2)`-vector (no wall). -/
theorem s7_A2_vector_norm : latticeNorm (TN 7) ![14, -14, 5] = -42 := by
  rw [TN_norm]; norm_num

/-- s10 (advisory): the three locus vectors have norms `−2, −4, −20`. -/
theorem s10_locus_norms :
    latticeNorm (TN 10) ![1, -1, 0] = -2 ∧ latticeNorm (TN 10) ![2, -6, 1] = -4 ∧
      latticeNorm (TN 10) ![10, -10, -3] = -20 := by
  refine ⟨?_, ?_, ?_⟩ <;> rw [TN_norm] <;> norm_num

/-- The two `(−2)`-vectors of s7 give honest lattice reflections: LeanMaster's general
    theorems apply (isometry and involution), with no computation repeated here. -/
theorem s7_walls_are_reflections :
    ((reflection (TN 7) ![2, -4, 1])ᵀ * TN 7 * reflection (TN 7) ![2, -4, 1] = TN 7 ∧
        reflection (TN 7) ![2, -4, 1] * reflection (TN 7) ![2, -4, 1] = 1) ∧
      ((reflection (TN 7) ![1, -1, 0])ᵀ * TN 7 * reflection (TN 7) ![1, -1, 0] = TN 7 ∧
        reflection (TN 7) ![1, -1, 0] * reflection (TN 7) ![1, -1, 0] = 1) :=
  ⟨⟨reflection_isometry _ (TN_symm 7) _ s7_second_wall_norm,
      reflection_involution _ _ s7_second_wall_norm⟩,
    ⟨reflection_isometry _ (TN_symm 7) _ (fricke_vector_norm 7),
      reflection_involution _ _ (fricke_vector_norm 7)⟩⟩

-- ── `A2_MEMBERSHIP.json`: the two congruences that decide it ─────────────────────────

/-- `−3` IS a square modulo `4·7 = 28` (witness `5`): the necessary condition holds for s7. -/
theorem neg_three_is_square_mod_28 : ∃ x : ZMod 28, x ^ 2 = -3 := ⟨5, by decide⟩

/-- `−3` is NOT a square modulo `4·10 = 40`: no vector of `U ⊕ ⟨20⟩` has `v^⊥` of
    discriminant `−3`, whatever its size. This is the all-vectors half of the s10 negative;
    the reduction of "`v^⊥ ≅ A₂`" to this congruence is the Python checker's leg (A), Tier B. -/
theorem neg_three_not_square_mod_40 : ¬ ∃ x : ZMod 40, x ^ 2 = -3 := by decide

/-- NEGATIVE CONTROL: the s10 statement is not vacuous — `−4` IS a square mod 40
    (the discriminant found at s10's z = ∞). -/
theorem neg_four_is_square_mod_40 : ∃ x : ZMod 40, x ^ 2 = -4 := ⟨6, by decide⟩

-- ── `ATKIN_LEHNER_DISC_FORM.json`: O(q) of the discriminant group ℤ/20 ───────────────

/-- The automorphisms of the discriminant form of `U ⊕ ⟨20⟩` are the multipliers `m` with
    `m² ≡ 1 mod 40`, read in `ℤ/20`: exactly `{1, 9, 11, 19}`. -/
theorem disc_form_automorphisms_level_10 :
    (Finset.univ.filter fun m : Fin 20 => (m.val ^ 2) % 40 = 1) = {1, 9, 11, 19} := by decide

/-- The Atkin–Lehner multiplier rule at `n = 10`: `w₂ ↦ 11`, `w₅ ↦ 9`, `w₁₀ ↦ 19` are
    `≡ −1 mod 2Q` and `≡ +1 mod 2n/Q`. -/
theorem atkin_lehner_multipliers_level_10 :
    (11 % 4 = 3 ∧ 11 % 10 = 1) ∧ (9 % 10 = 9 ∧ 9 % 4 = 1) ∧ (19 % 20 = 19) := by decide

end Stream2Lean.CMPoints
