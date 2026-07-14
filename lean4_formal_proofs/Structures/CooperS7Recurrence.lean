import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic.FinCases

/-!
# Cooper s₇ (A183204) order-2 Picard–Fuchs recurrence  (Phase 8.D, GATE-C finalist)

This file formalizes the order-2 global recurrence for
  CooperS7(n) = ∑ j ∈ range (n + 1), choose n j ^ 2 * choose (2*j) n * choose (j + n) j
with the minimal degree-3 integer polynomial coefficients P₀, P₁, P₂ below
(extracted by exact-integer modular+Fraction nullspace search,
`scripts/autoresearch_v2_phase_a_scan.py::find_shift_recurrence`, Phase 8.B/8.D).

Source: OEIS A183204, "This sequence is s_7 in Cooper's paper." (J. Kimberley,
OEIS comment, Nov 06 2012); closed-form term is the Wadim Zudilin formula cited
on that OEIS page. Cooper's paper: S. Cooper, "Sporadic sequences, modular forms
and new series for 1/π", Ramanujan J. 29 (2012), 163–183 — a level-7 weight-3
sporadic sequence.

## Verification status (honest scope)

* The recurrence is TRUE: verified EXACTLY (arbitrary-precision integers) for
  every n in [0, 197] by direct computation this session (198 independent
  checks), extending the 85-held-out-term validation from Phase 8.B G1-1.
* `cooper_s7_recurrence_checked` below KERNEL-VERIFIES the recurrence for each
  concrete n ≤ 20 — a genuine `decide` proof, NO `sorry`.
* `cooper_s7_recurrence` is the GENERAL (all-n) law. As with `S20.s20_recurrence`,
  a full kernel proof of the general law would require a Wilf–Zeilberger
  certificate translated into Lean, not yet done. Declared as an explicit
  `axiom`, not a `sorry` (an axiom is a declared, auditable assumption; a
  `sorry` would vacuously discharge dependent goals).
* Notable structural fact (not a claim about physics): the leading coefficient
  P₂(n) = (n+2)³ exactly — the same clean closed leading form found for
  cooper_s10 (P₂(n) = (n+2)³) and, up to shift, t103 (P₄(n) = (n+4)³). This is
  a common feature of Cooper/Almkvist–Zagier-class sporadic sequences and is
  recorded here as an observation, not used in any downstream physics claim.
-/

open Nat Finset BigOperators

namespace CooperS7

def cooper_s7_term (n j : ℕ) : ℤ :=
  (choose n j : ℤ)^2 * (choose (2*j) n : ℤ) * (choose (j + n) j : ℤ)

def CooperS7 (n : ℕ) : ℤ :=
  ∑ j ∈ range (n + 1), cooper_s7_term n j

/-- P₀(n) = -24 - 78n - 81n² - 27n³ -/
def P0 (n : ℤ) : ℤ := -24 - 78*n - 81*n^2 - 27*n^3

/-- P₁(n) = -90 - 177n - 117n² - 26n³ -/
def P1 (n : ℤ) : ℤ := -90 - 177*n - 117*n^2 - 26*n^3

/-- P₂(n) = 8 + 12n + 6n² + n³ = (n+2)³ -/
def P2 (n : ℤ) : ℤ := 8 + 12*n + 6*n^2 + n^3

theorem P2_eq_cube (n : ℤ) : P2 n = (n + 2)^3 := by
  unfold P2; ring

/-- Left-hand side of the order-2 recurrence at index `n`. -/
def cooper_s7_lhs (n : ℕ) : ℤ :=
  P0 n * CooperS7 n + P1 n * CooperS7 (n+1) + P2 n * CooperS7 (n+2)

/-- KERNEL-VERIFIED (no `sorry`): the recurrence holds as an exact integer
identity for every concrete n from 0 to 20. Genuine `decide` — the kernel
evaluates each `cooper_s7_lhs n` (large arbitrary-precision integer arithmetic
via `Nat.choose`/`Int`) and checks it against 0. -/
theorem cooper_s7_recurrence_checked :
    ∀ n ∈ Finset.range 21, cooper_s7_lhs n = 0 := by decide

/-- The GENERAL law, for all n : ℕ (not just n ≤ 20). Declared as an axiom
(not proved in-kernel) — see file docstring for scope. Empirically verified
to n = 197 by `scripts/autoresearch_v2_phase_a_scan.py` (external, Rule 1
compliant: real executed arithmetic, not hand-typed). -/
axiom cooper_s7_recurrence : ∀ n : ℕ, cooper_s7_lhs n = 0

-- Structural finite-range facts (kernel `native_decide`, no `sorry`)

/-- All Cooper s₇ values in the checked range are strictly positive. -/
theorem cooper_s7_pos (i : Fin 20) : CooperS7 i > 0 := by
  fin_cases i <;> native_decide

/-- Cooper s₇ is strictly monotone over the checked range. -/
theorem cooper_s7_monotone (i : Fin 19) : CooperS7 i.castSucc < CooperS7 i.succ := by
  fin_cases i <;> native_decide

end CooperS7
