# What "validate the K3×T² dual-scale T-duality theory" can and cannot mean (Stream 2, 2026-10-10)

**Answer first.** The physical theory cannot be validated today. It is Tier C: no worked EFT matching exists, `PREDICTION.md` §6 holds
no derived quantity, and the flux/tadpole route is blocked (F5b). What can be, and has been, validated is the mathematics the
phrase rests on. This brief maps the phrase to its components and says which are established, which are blocked, and what comes next.

Requested by T0 on 2026-10-10: *"continue on the K3 numeric calculation to identify and validate the K3*T2 dual scale t duality theory"*.

## The components, and their tiers

| Component | Status | Where |
|---|---|---|
| L₃ = Sym²(L₂) (the K3 family is a symmetric square of an elliptic family) | **Tier A**, Lean kernel | Stream 1; ledger item 1 |
| Γ₀(N)⁺ = O⁺(U⊕⟨2N⟩), the Fricke involution swapping e↔f acting on the period | **Tier A**, Lean kernel | Stream 1 (`ModularAction`, `SelfDual`) |
| The dual-scale bound 𝒟(G) = tr G + tr G⁻¹ ≥ 2d, equality iff G = 1, invariant under G ↦ G⁻¹ | **Tier A**, Lean kernel; a statement about torus metrics only | LeanMaster `DualScaleStream2.DualScale.dualScale_ge`, `dualScale_eq_iff`, `dualScale_inv` |
| "K3×T²" = Shioda–Inose pairing X ↔ E×E′, T(X) ≅ U⊕⟨2n⟩ for n = 7, 10 | **Tier B** (computed exactly; the pairing itself Tier L) | `K3xT2_READING_S.json`, D29′ |
| Level consistency, lattice n = modular n | **Tier B**, hard gate since AM-9 | `T3_LEVEL_CONSISTENCY.json` |
| The M₇-polarizing section at z = 1/27: P̄·Ō = 5, contr = 0, h = 14, explicitly | **Tier B** (exact; construction Tier L) | `TW2_SECTION_DESCENT.json`, step 2b-ii |
| Identification of the T² of any physical compactification with E or E′ | **Tier C, not made** | D29′, ledger item 12 |
| Any dark-sector mass, coupling, exclusion or dark-energy statement | **Tier C, blocked** | ledger item 4; F5b |

## Computations considered and not run

- **tr G + tr G⁻¹ on the CM tori.** Not run, for four reasons. It would put the torus of the elliptic curve in the role of a physical
  T², which D29′ declines. tr G is not GL(2,ℤ)-invariant, so a number needs an orbit minimum. The Kähler modulus has no value, so any
  number needs one typed in (rule 5). And placing the X₃ and X₄ values side by side is a cross-family ordering, barred by ledger
  items 8/9 and D31′. The Lean theorem is already stated for all positive-definite G; evaluating it at special points adds no
  information that is not forced by the definitions.
- **A ranking or score of s7 against s10.** D31′: considered, not adopted.
- **A "K3 numeric selection" on survey data.** Home has no such pipeline. The only real-data comparison pre-registered is the WP-E6
  (m, f) fuzzy-dark-matter sweep, whose real-data mode is mechanically blocked until T0 pins the C1–C5 ruling and the eligibility rule.
  Nothing about the K3 selection feeds an observable.

## What would make the physical theory testable (the chain, from VISION §3–4)

worked EFT matching from the geometric data → a quantitative prediction that differs from ΛCDM → pre-registration and pin → survival
against public data. None of the first link exists. The mathematics above is necessary groundwork for it and says nothing about whether
the chain can be completed.

## Next mathematical computations, in order

1. **WP-TW2 at z = −1** (the case P̄·Ō = 0, h = 7/2): the same descent, now with the A₁ contact at a non-trivial component possible.
   The method and controls of step 2b-ii carry over; the isogeny degree is 2 here, so the kernel is the 2-torsion, which needs its own
   Vélu step. (At z = ∞ there is no section: rank 0.)
2. **Kernel check of the Reading S lattice** in Stream 1's own build tree (the request is addended): the claim must be carried by the
   statement, per Stream 1's `LL.md` §1.
3. **WP-TW3** (twist data over a threefold base): needs T0 text; unopened.

*Generated-by: Claude (Opus 5.5 / Fable 5.1), Stream 2, 2026-10-10 | Verified-by: the certificates and Lean statements named above | Reviewed-by: N*
