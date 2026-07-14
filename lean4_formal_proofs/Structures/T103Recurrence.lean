import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-!
# T103 (A276536) order-4 shift recurrence  (Phase 8.D, GATE-C finalist)

This file formalizes the order-4 global recurrence for
  T103(n) = ∑ k ∈ range (n + 1), choose n k * choose (2*k) k ^ 3
with the minimal degree-3 integer polynomial coefficients P₀..P₄ below
(extracted by exact-integer modular+Fraction nullspace search,
`scripts/autoresearch_v2_phase_a_scan.py::find_shift_recurrence`, widened
search bounds ρ≤4/δ≤8 in Phase 8.D — the default Phase 8.B/G1-1 window
(ρ≤3/δ≤4) did not contain this sequence's minimal SHIFT recurrence, though
its minimal generating-function ODE (order 3, degree 6) was found there and
is the basis of its Phase 8.B K3-type classification).

Source: OEIS A276536, "Binomial sums of the cubes of the central binomial
coefficients" — an in-session sieve discovery (Phase 8.A LR-3), OEIS identity
resolved in Phase 8.B (LR-2 closure). No Cooper/Almkvist–Zagier literature
attribution is claimed; T103 is a novel candidate promoted on the strength of
its own gate results (GATE-B, 2026-07-14), not external anchoring.

## Verification status (honest scope)

* The SHIFT recurrence (order 4, degree 3) is TRUE: verified EXACTLY
  (arbitrary-precision integers) for every n in [0, 195] by direct computation
  this session (196 independent checks). This is a DIFFERENT (larger, ρ=4)
  operator than the order-3 generating-function ODE used for T103's K3-type
  classification in Phase 8.B (`g1_1_order_classification.json`); both are
  valid annihilating relations for the same sequence — the shift recurrence is
  what Lean formalizes here because it has a `decide`-friendly finite check,
  matching the pattern of `S20Recurrence.lean` / `CooperS7Recurrence.lean`.
* `t103_recurrence_checked` below KERNEL-VERIFIES the recurrence for each
  concrete n ≤ 20 — a genuine `decide` proof, NO `sorry`.
* `t103_recurrence` is the GENERAL (all-n) law, declared as an explicit
  `axiom` for the same reason as the other Phase 8.D finalists (full kernel
  proof requires a Wilf–Zeilberger certificate not yet translated into Lean).
* P₄(n) = (n+4)³ exactly — the third consecutive GATE-C finalist with a clean
  cubic leading coefficient (cooper_s7, cooper_s10: (n+2)³); recorded as a
  structural observation, not used in any physics claim.
-/

open Nat Finset BigOperators

namespace T103

def t103_term (n k : ℕ) : ℤ :=
  (choose n k : ℤ) * (choose (2*k) k : ℤ)^3

def T103 (n : ℕ) : ℤ :=
  ∑ k ∈ range (n + 1), t103_term n k

/-- P₀(n) = 390 + 715n + 390n² + 65n³ -/
def P0 (n : ℤ) : ℤ := 390 + 715*n + 390*n^2 + 65*n^3

/-- P₁(n) = -2940 - 3626n - 1470n² - 196n³ -/
def P1 (n : ℤ) : ℤ := -2940 - 3626*n - 1470*n^2 - 196*n^3

/-- P₂(n) = 5397 + 5363n + 1782n² + 198n³ -/
def P2 (n : ℤ) : ℤ := 5397 + 5363*n + 1782*n^2 + 198*n^3

/-- P₃(n) = -2919 - 2500n - 714n² - 68n³ -/
def P3 (n : ℤ) : ℤ := -2919 - 2500*n - 714*n^2 - 68*n^3

/-- P₄(n) = 64 + 48n + 12n² + n³ = (n+4)³ -/
def P4 (n : ℤ) : ℤ := 64 + 48*n + 12*n^2 + n^3

theorem P4_eq_cube (n : ℤ) : P4 n = (n + 4)^3 := by
  unfold P4; ring

/-- Left-hand side of the order-4 recurrence at index `n`. -/
def t103_lhs (n : ℕ) : ℤ :=
  P0 n * T103 n + P1 n * T103 (n+1) + P2 n * T103 (n+2)
    + P3 n * T103 (n+3) + P4 n * T103 (n+4)

/-- KERNEL-VERIFIED (no `sorry`): genuine `decide`, n from 0 to 20. -/
theorem t103_recurrence_checked :
    ∀ n ∈ Finset.range 21, t103_lhs n = 0 := by decide

/-- The GENERAL law, declared as an axiom (see file docstring for scope).
Empirically verified to n = 195 externally (Rule 1 compliant). -/
axiom t103_recurrence : ∀ n : ℕ, t103_lhs n = 0

end T103
