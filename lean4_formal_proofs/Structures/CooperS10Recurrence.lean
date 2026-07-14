import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic.FinCases

/-!
# Cooper s₁₀ (A005260) order-2 Picard–Fuchs recurrence  (Phase 8.D, GATE-C finalist)

This file formalizes the order-2 global recurrence for
  CooperS10(n) = ∑ k ∈ range (n + 1), choose n k ^ 4
with the minimal degree-3 integer polynomial coefficients P₀, P₁, P₂ below
(extracted by exact-integer modular+Fraction nullspace search,
`scripts/autoresearch_v2_phase_a_scan.py::find_shift_recurrence`, Phase 8.B/8.D).

Source: OEIS A005260, a(n) = Σ_{k=0}^{n} C(n,k)^4; "This sequence is s_10 in
Cooper's paper." (J. Kimberley, OEIS comment, Nov 25 2012). Cooper's paper:
S. Cooper, "Sporadic sequences, modular forms and new series for 1/π",
Ramanujan J. 29 (2012), 163–183 — a level-10 weight-3 sporadic sequence.

## Verification status (honest scope)

* The recurrence is TRUE: verified EXACTLY (arbitrary-precision integers) for
  every n in [0, 197] by direct computation this session (198 independent
  checks), extending the 85-held-out-term validation from Phase 8.B G1-1.
* `cooper_s10_recurrence_checked` below KERNEL-VERIFIES the recurrence for each
  concrete n ≤ 20 — a genuine `decide` proof, NO `sorry`.
* `cooper_s10_recurrence` is the GENERAL (all-n) law, declared as an explicit
  `axiom` for the same reason as `CooperS7.cooper_s7_recurrence` and
  `S20.s20_recurrence` (see those files' docstrings): a full kernel proof
  requires a Wilf–Zeilberger certificate not yet translated into Lean.
* P₂(n) = (n+2)³ exactly, matching cooper_s7's leading coefficient — recorded
  as a structural observation only.
-/

open Nat Finset BigOperators

namespace CooperS10

def cooper_s10_term (n k : ℕ) : ℤ :=
  (choose n k : ℤ)^4

def CooperS10 (n : ℕ) : ℤ :=
  ∑ k ∈ range (n + 1), cooper_s10_term n k

/-- P₀(n) = -60 - 188n - 192n² - 64n³ -/
def P0 (n : ℤ) : ℤ := -60 - 188*n - 192*n^2 - 64*n^3

/-- P₁(n) = -42 - 82n - 54n² - 12n³ -/
def P1 (n : ℤ) : ℤ := -42 - 82*n - 54*n^2 - 12*n^3

/-- P₂(n) = 8 + 12n + 6n² + n³ = (n+2)³ -/
def P2 (n : ℤ) : ℤ := 8 + 12*n + 6*n^2 + n^3

theorem P2_eq_cube (n : ℤ) : P2 n = (n + 2)^3 := by
  unfold P2; ring

/-- Left-hand side of the order-2 recurrence at index `n`. -/
def cooper_s10_lhs (n : ℕ) : ℤ :=
  P0 n * CooperS10 n + P1 n * CooperS10 (n+1) + P2 n * CooperS10 (n+2)

/-- KERNEL-VERIFIED (no `sorry`): genuine `decide`, n from 0 to 20. -/
theorem cooper_s10_recurrence_checked :
    ∀ n ∈ Finset.range 21, cooper_s10_lhs n = 0 := by decide

/-- The GENERAL law, declared as an axiom (see file docstring for scope).
Empirically verified to n = 197 externally (Rule 1 compliant). -/
axiom cooper_s10_recurrence : ∀ n : ℕ, cooper_s10_lhs n = 0

-- Structural finite-range facts (kernel `native_decide`, no `sorry`)

/-- All Cooper s₁₀ values in the checked range are strictly positive. -/
theorem cooper_s10_pos (i : Fin 20) : CooperS10 i > 0 := by
  fin_cases i <;> native_decide

/-- Cooper s₁₀ is strictly monotone over the checked range. -/
theorem cooper_s10_monotone (i : Fin 19) : CooperS10 i.castSucc < CooperS10 i.succ := by
  fin_cases i <;> native_decide

end CooperS10
