import Mathlib.Algebra.Polynomial.Derivative
import Mathlib.Tactic.Ring

/-!
# L₃ = Sym²(L₂): the bulk order-3 operator is the symmetric square of the order-2 partner

This file gives a **kernel-checked, `sorry`-free, axiom-free** proof that the
Cooper s₇ and s₁₀ bulk Picard–Fuchs operators `L₃` equal the classical symmetric
square `Sym²(L₂)` of their extracted order-2 elliptic partners `L₂`, verified
**coefficient by coefficient in the θ = z·d/dz basis** as exact identities in `ℚ[z]`.

## Provenance of the coefficients (Stream 2, Tier A CAS)

Both operators are built in the θ-basis `L = θ^order − z·A(θ) − z²·B(θ+1)` from
their integer recurrences (`refs/recurrences_v1.json`). The order-2 partner `L₂`
was extracted as the exact power-series symmetric-square root of `L₃` by
`checkers/check_C3b_symsqrt.py`; certificates:

* `data/certificates/C3b_symsqrt_cooper_s7.json`  — partner OEIS A279619, integral
* `data/certificates/C3b_symsqrt_cooper_s10.json` — partner rational (non-integral)

The checker verified `Sym²(L₂) − L₃ = 0` as monic d/dz coefficients (`D2=D1=D0=0`).
This Lean file re-proves the equivalent, cleaner **θ-basis coefficient identities**
that were derived symbolically (`scripts/derive_sym2_identities.py`, this session)
and that hold *unconditionally* as polynomial identities:

| θ-power | `L₃` coefficient | Sym² combination of `L₂` coefficients |
|---------|------------------|----------------------------------------|
| θ³      | `Q₃`             | `P₂`                                   |
| θ²      | `Q₂`             | `3·P₁`                                 |
| θ¹      | `Q₁`             | `θ(P₁) + 4·P₀`                         |
| θ⁰      | `Q₀`             | `2·θ(P₀)`                             |

together with the **collapse identity** `θ(P₂) = 2·P₁` (Deep Think T0s), which is
the structural fact that makes the generic Sym² formula collapse to these clean
θ-basis relations (it eliminates the fractional 2·a₁²+a₁′ terms in monic form).

Here `θ(p) = X · derivative p` uses Mathlib's purely-algebraic `Polynomial.derivative`
(no analysis), so every theorem below is discharged by `simp`-normalising the
derivative and closing with `ring` — a genuine kernel check, NO `sorry`, NO `axiom`,
NO `native_decide`. This is plain **Tier A**.

## Epistemic scope (VISION §2)

This proves a **mathematical** operator identity only. It says nothing, and must not
be read to say anything, about a bulk↔brane *physical* coupling — that interpretation
remains a Tier C conjecture (see `ROADMAP.md`, VISION §1.3: geometry ≠ physics).
-/

open Polynomial

-- Derivative-normalising `simp only` sets below intentionally list a uniform lemma
-- bundle across all six proofs; some entries are redundant in individual goals.
set_option linter.unusedSimpArgs false

namespace CooperSym2

/-- θ = z·d/dz acting on `ℚ[z]`, built from Mathlib's algebraic `derivative`. -/
noncomputable def θ (p : ℚ[X]) : ℚ[X] := X * derivative p

/-! ## Cooper s₇  (level-7 sporadic, bulk A183204; partner A279619) -/

namespace S7

/-- Order-2 partner `L₂` θ-coefficients (from `C3b_symsqrt_cooper_s7.json`). -/
noncomputable def P2 : ℚ[X] := -27 * X ^ 2 - 26 * X + 1
noncomputable def P1 : ℚ[X] := -27 * X ^ 2 - 13 * X
noncomputable def P0 : ℚ[X] := -6 * X ^ 2 - 2 * X

/-- Bulk `L₃` θ-coefficients (Cooper s₇ recurrence, `L₃ = θ³ − z·A₃(θ) − z²·B₃(θ+1)`). -/
noncomputable def Q3 : ℚ[X] := -27 * X ^ 2 - 26 * X + 1
noncomputable def Q2 : ℚ[X] := -81 * X ^ 2 - 39 * X
noncomputable def Q1 : ℚ[X] := -78 * X ^ 2 - 21 * X
noncomputable def Q0 : ℚ[X] := -24 * X ^ 2 - 4 * X

/-- Collapse identity (Deep Think): `θ(P₂) = 2·P₁`. -/
theorem collapse : θ P2 = 2 * P1 := by
  unfold θ P2 P1
  simp only [derivative_add, derivative_sub, derivative_mul, derivative_pow,
    derivative_X, derivative_C, derivative_one, derivative_ofNat, derivative_neg, map_natCast, Nat.cast_ofNat, map_ofNat]
  ring

/-- θ³ coefficient: `Q₃ = P₂`. -/
theorem sym2_theta3 : Q3 = P2 := by unfold Q3 P2; ring

/-- θ² coefficient: `Q₂ = 3·P₁`. -/
theorem sym2_theta2 : Q2 = 3 * P1 := by unfold Q2 P1; ring

/-- θ¹ coefficient: `Q₁ = θ(P₁) + 4·P₀`. -/
theorem sym2_theta1 : Q1 = θ P1 + 4 * P0 := by
  unfold θ Q1 P1 P0
  simp only [derivative_add, derivative_sub, derivative_mul, derivative_pow,
    derivative_X, derivative_C, derivative_ofNat, derivative_neg, map_natCast, Nat.cast_ofNat, map_ofNat]
  ring

/-- θ⁰ coefficient: `Q₀ = 2·θ(P₀)`. -/
theorem sym2_theta0 : Q0 = 2 * θ P0 := by
  unfold θ Q0 P0
  simp only [derivative_add, derivative_sub, derivative_mul, derivative_pow,
    derivative_X, derivative_C, derivative_ofNat, derivative_neg, map_natCast, Nat.cast_ofNat, map_ofNat]
  ring

/-- **L₃ = Sym²(L₂), Cooper s₇** — all four θ-basis coefficient identities at once. -/
theorem L3_eq_Sym2_L2 :
    Q3 = P2 ∧ Q2 = 3 * P1 ∧ Q1 = θ P1 + 4 * P0 ∧ Q0 = 2 * θ P0 :=
  ⟨sym2_theta3, sym2_theta2, sym2_theta1, sym2_theta0⟩

end S7

/-! ## Cooper s₁₀  (level-10 sporadic, bulk A005260; partner rational) -/

namespace S10

/-- Order-2 partner `L₂` θ-coefficients (from `C3b_symsqrt_cooper_s10.json`). -/
noncomputable def P2 : ℚ[X] := -64 * X ^ 2 - 12 * X + 1
noncomputable def P1 : ℚ[X] := -64 * X ^ 2 - 6 * X
noncomputable def P0 : ℚ[X] := -15 * X ^ 2 - X

/-- Bulk `L₃` θ-coefficients (Cooper s₁₀ recurrence). -/
noncomputable def Q3 : ℚ[X] := -64 * X ^ 2 - 12 * X + 1
noncomputable def Q2 : ℚ[X] := -192 * X ^ 2 - 18 * X
noncomputable def Q1 : ℚ[X] := -188 * X ^ 2 - 10 * X
noncomputable def Q0 : ℚ[X] := -60 * X ^ 2 - 2 * X

/-- Collapse identity (Deep Think): `θ(P₂) = 2·P₁`. -/
theorem collapse : θ P2 = 2 * P1 := by
  unfold θ P2 P1
  simp only [derivative_add, derivative_sub, derivative_mul, derivative_pow,
    derivative_X, derivative_C, derivative_one, derivative_ofNat, derivative_neg, map_natCast, Nat.cast_ofNat, map_ofNat]
  ring

/-- θ³ coefficient: `Q₃ = P₂`. -/
theorem sym2_theta3 : Q3 = P2 := by unfold Q3 P2; ring

/-- θ² coefficient: `Q₂ = 3·P₁`. -/
theorem sym2_theta2 : Q2 = 3 * P1 := by unfold Q2 P1; ring

/-- θ¹ coefficient: `Q₁ = θ(P₁) + 4·P₀`. -/
theorem sym2_theta1 : Q1 = θ P1 + 4 * P0 := by
  unfold θ Q1 P1 P0
  simp only [derivative_add, derivative_sub, derivative_mul, derivative_pow,
    derivative_X, derivative_C, derivative_ofNat, derivative_neg, map_natCast, Nat.cast_ofNat, map_ofNat]
  ring

/-- θ⁰ coefficient: `Q₀ = 2·θ(P₀)`. -/
theorem sym2_theta0 : Q0 = 2 * θ P0 := by
  unfold θ Q0 P0
  simp only [derivative_add, derivative_sub, derivative_mul, derivative_pow,
    derivative_X, derivative_C, derivative_ofNat, derivative_neg, map_natCast, Nat.cast_ofNat, map_ofNat]
  ring

/-- **L₃ = Sym²(L₂), Cooper s₁₀** — all four θ-basis coefficient identities at once. -/
theorem L3_eq_Sym2_L2 :
    Q3 = P2 ∧ Q2 = 3 * P1 ∧ Q1 = θ P1 + 4 * P0 ∧ Q0 = 2 * θ P0 :=
  ⟨sym2_theta3, sym2_theta2, sym2_theta1, sym2_theta0⟩

end S10

end CooperSym2
