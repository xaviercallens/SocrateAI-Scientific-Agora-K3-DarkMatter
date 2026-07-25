-- Structures/B1_Sym2Bridge.lean
-- WP-B1 deliverable: interface coupling the chameleon screening mechanism (B1)
-- to the SYM2_PARTNER order-2 elliptic operator (B3 local EFT side).
--
-- DoD item: "Coupled to `SYM2_PARTNER` (B3 local EFT) — interface compiles
-- without error."
--
-- ⚠️ EPISTEMIC SCOPE (VISION §1.3, and inherited verbatim from
-- CooperSym2Proof.lean's own scope note). This file establishes a **type-level
-- and algebraic** interface only: it checks that the chameleon-side data
-- (`BraneCouplingVertex`, indexed by environment density) and the Sym²-side
-- data (the order-2 partner's θ-basis coefficients, carrying their proven
-- collapse identity) can be assembled into a single coherent record.
--
-- It does NOT assert, and must not be read as asserting, that a physical
-- bulk↔brane coupling exists or has any particular strength. That remains a
-- Tier [C] conjecture. The coupling constant `α_ch` is an opaque axiom here;
-- giving it a value is S3-00's job (Stream 3), and doing so does not inherit
-- this file's Tier A status.
--
-- What IS Tier A here: the record below cannot be constructed unless the
-- Sym² collapse identity actually holds for the partner you supply. So the
-- s7/s10 instances at the bottom are compile-time evidence that Stream 1's
-- two independent workstreams (Sym² proof, chameleon screening) are
-- structurally consistent — no more, no less.

import Mathlib.Algebra.Polynomial.Derivative
import Structures.B1_Chameleon
import Structures.CooperSym2Proof

open Polynomial
open scoped NNReal

namespace B1_Sym2Bridge

open B1_Screening B1_Chameleon

/-- A dual-scale site: local environment data (chameleon side) paired with the
order-2 elliptic partner operator's θ-basis coefficients (Sym² side).

The two `Prop` fields are what give the structure its content:
* `density_coherent` — the brane coupling vertex is evaluated at the *same*
  environment density the site claims to sit at (rules out silently mixing
  densities between the two halves);
* `sym2_witness` — the supplied partner genuinely satisfies the collapse
  identity `θ(P₂) = 2·P₁`, i.e. it really is a Sym² root in the sense
  Stream 1 proved, not an arbitrary pair of polynomials. -/
structure DualScaleSite where
  env_density : EnvDensity
  partner_P2 : ℚ[X]
  partner_P1 : ℚ[X]
  partner_P0 : ℚ[X]
  coupling : BraneCouplingVertex
  density_coherent : coupling.environment_density = env_density
  sym2_witness : CooperSym2.θ partner_P2 = 2 * partner_P1

/-- Cooper s₇ dual-scale site at environment density `ρ`.

Constructing this is a kernel check that the s₇ Sym² partner (Stream 1,
`CooperSym2.S7.collapse`) and the chameleon coupling vertex (this WP) fit
the `DualScaleSite` interface simultaneously. -/
noncomputable def s7_site (ρ : EnvDensity) : DualScaleSite where
  env_density := ρ
  partner_P2 := CooperSym2.S7.P2
  partner_P1 := CooperSym2.S7.P1
  partner_P0 := CooperSym2.S7.P0
  coupling := brane_coupling_site ρ
  density_coherent := rfl
  sym2_witness := CooperSym2.S7.collapse

/-- Cooper s₁₀ dual-scale site at environment density `ρ`. -/
noncomputable def s10_site (ρ : EnvDensity) : DualScaleSite where
  env_density := ρ
  partner_P2 := CooperSym2.S10.P2
  partner_P1 := CooperSym2.S10.P1
  partner_P0 := CooperSym2.S10.P0
  coupling := brane_coupling_site ρ
  density_coherent := rfl
  sym2_witness := CooperSym2.S10.collapse

/-! ## Screening guarantees transported to dual-scale sites

These restate the B1 lemmas at the site level, so Stream 3 can cite a single
object rather than re-threading `env_density` through by hand. -/

/-- At any dual-scale site, the screening radius respects the uniform bound. -/
theorem site_force_range_bounded (S : DualScaleSite) :
    screening_radius S.env_density ≤ (C_max : ℝ) :=
  force_range_bounded S.env_density

/-- At any dual-scale site, the effective mass is at least the bare mass. -/
theorem site_screening_triggers (S : DualScaleSite) :
    m_eff S.env_density ≥ (m_bare : ℝ) :=
  screening_always_triggers S.env_density

/-- Denser sites have strictly shorter force range. -/
theorem site_denser_is_shorter (S T : DualScaleSite)
    (h : S.env_density < T.env_density) :
    screening_radius T.env_density < screening_radius S.env_density :=
  screening_radius_strict_anti _ _ h

/-- The coupling strength recorded at any site is the global `α_ch` axiom —
i.e. the interface does not secretly introduce a second, site-dependent
coupling. (Stream 3: this is the quantity to instantiate as `α_D`.) -/
theorem s7_site_coupling_is_alpha (ρ : EnvDensity) :
    (s7_site ρ).coupling.coupling_strength = α_ch := rfl

theorem s10_site_coupling_is_alpha (ρ : EnvDensity) :
    (s10_site ρ).coupling.coupling_strength = α_ch := rfl

end B1_Sym2Bridge
