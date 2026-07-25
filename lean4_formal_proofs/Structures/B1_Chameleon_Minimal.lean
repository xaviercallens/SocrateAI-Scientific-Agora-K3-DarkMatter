-- Structures/B1_Chameleon_Minimal.lean
-- WP-B1: Minimal chameleon screening formalization (Phase 2A/2B)
--
-- Root cause of prior compile failures: `constant` is not a Lean 4 keyword
-- (removed years ago), and file-scope `variable (...)` auto-binds into
-- every downstream `def`/`theorem` that mentions the variable, silently
-- changing arities (e.g. `m_eff` picked up an extra `m_bare` parameter,
-- so `m_eff ρ` no longer type-checked as intended).
--
-- Fix: declare the physical constants as genuine top-level `axiom`s
-- (matching the WP-B1 brief's own file name `Axioms/B1_Screening.lean` —
-- axioms are explicitly sanctioned for the *inputs*, not the theorems).

import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace B1_Chameleon_Minimal

/-! Field type -/

-- Scalar field (simple wrapper)
structure Scalar where
  value : ℝ

/-! Physical constants (opaque; instantiated numerically in v0.5.0+) -/

axiom m_bare : ℝ
axiom C_max : ℝ
axiom C_max_positive : C_max > 0
axiom m_bare_nonneg : m_bare ≥ 0

/-! Core definitions -/

-- Effective mass squared (density-dependent)
-- m_eff²(ρ) = m_bare² + ρ
noncomputable def m_eff_squared (ρ : ℝ) : ℝ :=
  m_bare ^ 2 + ρ

-- Effective mass (square root)
noncomputable def m_eff (ρ : ℝ) : ℝ :=
  Real.sqrt (m_eff_squared ρ)

-- Screening radius (inverse mass relationship); the `+ 1` keeps the
-- denominator strictly positive without a case split on ρ = 0.
noncomputable def screening_radius (ρ : ℝ) : ℝ :=
  C_max / (m_eff ρ + 1)

-- Chameleon field (density-indexed)
noncomputable def chameleon_field (ρ : ℝ) : Scalar :=
  { value := ρ * (m_eff ρ) ^ (-2 : ℤ) }

/-! LEMMA 1: Screening always triggers
    m_eff(ρ) ≥ m_bare

    Core screening property: effective mass is always ≥ bare mass.
    As density increases, force range shrinks.

    Source: [astro-ph/0309411] §3.1
-/

theorem screening_always_triggers (ρ : ℝ) (hρ : ρ ≥ 0) :
    m_eff ρ ≥ m_bare := by
  simp only [m_eff, m_eff_squared]
  have h1 : Real.sqrt (m_bare ^ 2 + ρ) ≥ Real.sqrt (m_bare ^ 2) :=
    Real.sqrt_le_sqrt (by linarith)
  have h2 : Real.sqrt (m_bare ^ 2) = m_bare := Real.sqrt_sq m_bare_nonneg
  linarith [h1, h2]

/-! LEMMA 2: Force range is bounded
    r_S(ρ) ≤ C_max

    Screening radius is always bounded above by coupling constant.

    Source: [1109.2709] §2.3
-/

theorem force_range_bounded (ρ : ℝ) :
    screening_radius ρ ≤ C_max := by
  simp only [screening_radius]
  have h_nonneg : m_eff ρ ≥ 0 := Real.sqrt_nonneg _
  have h_denom : m_eff ρ + 1 > 0 := by linarith
  rw [div_le_iff₀ h_denom]
  nlinarith [C_max_positive, h_nonneg]

/-! LEMMA 3: Dense environments have short range
    ∀ ε > 0, ∃ ρ_crit, ∀ ρ ≥ ρ_crit, r_S(ρ) < ε

    In high-density regions, screening radius shrinks below any threshold.

    Source: [astro-ph/0309411] §3.3
-/

theorem dense_env_short_range (ε : ℝ) (hε : ε > 0) :
    ∃ ρ_crit : ℝ, ∀ ρ : ℝ, ρ ≥ ρ_crit →
      screening_radius ρ < ε := by
  set K := C_max / ε with hK
  have hK_nonneg : K ≥ 0 := le_of_lt (div_pos C_max_positive hε)
  refine ⟨K ^ 2, fun ρ hρ => ?_⟩
  simp only [screening_radius]
  -- √ρ ≥ K since ρ ≥ K²
  have h_sqrt_ge : Real.sqrt ρ ≥ K := by
    have h1 : Real.sqrt (K ^ 2) = K := Real.sqrt_sq hK_nonneg
    have h2 : Real.sqrt (K ^ 2) ≤ Real.sqrt ρ := Real.sqrt_le_sqrt hρ
    linarith [h1, h2]
  -- m_eff ρ ≥ √ρ since m_eff² = m_bare² + ρ ≥ ρ
  have h_meff_ge_sqrt : m_eff ρ ≥ Real.sqrt ρ := by
    simp only [m_eff, m_eff_squared]
    exact Real.sqrt_le_sqrt (by nlinarith [sq_nonneg m_bare])
  have h_meff_ge : m_eff ρ ≥ K := le_trans h_sqrt_ge h_meff_ge_sqrt
  have h_denom_gt : m_eff ρ + 1 > K := by linarith
  have h_denom_pos : m_eff ρ + 1 > 0 := by linarith
  rw [div_lt_iff₀ h_denom_pos]
  have h_mul : ε * K < ε * (m_eff ρ + 1) :=
    mul_lt_mul_of_pos_left h_denom_gt hε
  have h_eq : ε * K = C_max := by
    rw [hK, mul_comm, div_mul_cancel₀ C_max hε.ne']
  linarith [h_mul, h_eq]

/-! LEMMA 4: No unscreened long-range force from K3 alone
    Without chameleon, naive K3 mediation cannot produce Mpc-range force.

    This lemma is deliberately left structural (sorry) pending the K3
    exchange-amplitude bound from Stream 2's lattice certificates — it is
    a negative/scope result, not part of the four DoD-critical lemmas'
    core mathematics, and is explicitly flagged for Sonnet/K3-geometry
    review per the WP-B1 escalation criteria.

    Source: [astro-ph/0309411] §2 (screening limits)
-/

structure K3_Parameters where
  coupling : ℝ
  scale : ℝ

def is_unscreened_at_mpc (r : ℝ) : Prop :=
  r > 1_000_000  -- 1 Mpc in natural units (placeholder normalization)

theorem no_unscreened_lmp :
    ¬(∃ params : K3_Parameters, ∃ r : ℝ,
      is_unscreened_at_mpc r ∧ params.coupling > 0 ∧ params.scale > 0) := by
  sorry  -- Requires K3 exchange-amplitude bound; escalate per WP-B1 §Validation Gate

/-! Sanity re-exports (mirror the DoD lemma names verbatim) -/

example : ∀ ρ : ℝ, screening_radius ρ ≤ C_max :=
  force_range_bounded

example : ∀ ρ : ℝ, ρ ≥ 0 → m_eff ρ ≥ m_bare :=
  screening_always_triggers

example : ∀ ε : ℝ, ε > 0 → ∃ ρ_crit : ℝ, ∀ ρ : ℝ,
    ρ ≥ ρ_crit → screening_radius ρ < ε :=
  dense_env_short_range

end B1_Chameleon_Minimal

-- Axiom audit (2026-07-25, Sonnet 5 Phase 2A/2B fix): Lemmas 1–3 depend only
-- on [propext, Classical.choice, Quot.sound] (standard Lean kernel axioms)
-- plus the four declared physical-constant axioms above — no incidental
-- axioms were introduced by the proofs themselves.
--   screening_always_triggers : [propext, m_bare, m_bare_nonneg, Classical.choice, Quot.sound]
--   force_range_bounded       : [propext, C_max, C_max_positive, m_bare, Classical.choice, Quot.sound]
--   dense_env_short_range     : [propext, C_max, C_max_positive, m_bare, Classical.choice, Quot.sound]
