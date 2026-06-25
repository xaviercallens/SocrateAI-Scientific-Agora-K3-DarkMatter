import Mathlib

open Matrix

noncomputable def L : ℂ := 2 * Real.pi * Complex.I

noncomputable def mum_matrix : Matrix (Fin 3) (Fin 3) ℂ
  | 0, 0 => 1
  | 0, 1 => L
  | 0, 2 => L^2 / 2
  | 1, 0 => 0
  | 1, 1 => 1
  | 1, 2 => L
  | 2, 0 => 0
  | 2, 1 => 0
  | 2, 2 => 1

def I3 : Matrix (Fin 3) (Fin 3) ℂ := 1

noncomputable def N : Matrix (Fin 3) (Fin 3) ℂ := mum_matrix - I3

theorem unipotent_index_three : N ^ 3 = 0 := by
  simp only [pow_succ, pow_zero]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [N, mum_matrix, I3, Matrix.mul_apply, Matrix.sub_apply, Matrix.one_apply, Fin.sum_univ_succ]

theorem symplectic_det_one : mum_matrix.det = 1 := by
  simp [mum_matrix, Matrix.det_fin_three]
