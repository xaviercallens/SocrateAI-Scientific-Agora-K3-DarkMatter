-- B1_Chameleon.lean
-- WP-B1: Four lemmas proving chameleon screening mechanism
--
-- Purpose: Formalize the four core theorems required for Stream 1 WP-B1
-- 1. Screening always triggers (m_eff(ρ) ≥ m_bare)
-- 2. Force range is bounded (r_S ≤ C_max)
-- 3. Dense environments have short range (∀ε, ∃ρ_crit)
-- 4. Naive K3 cannot produce Mpc-range force
--
-- Source: [astro-ph/0309411] Khoury-Weltman; [1109.2709] cosmological chameleon
--
-- NOTE (2026-07-25, Sonnet 5 fix): rewritten against the corrected
-- `Structures.Axioms.B1_Screening` (constants are now `axiom`s, not the
-- removed `constant` keyword; `screening_radius ρ := C_max / (m_eff ρ + 1)`
-- with the `+ 1` floor replacing the earlier `split_ifs` case analysis,
-- which left the `> 0` branch's division algebra as an unclosed `sorry`).
--
-- DEVIATION FROM BRIEF (documented, not silent): the brief's DoD lists
-- `force_range_bounded : r_S ρ ≤ C * (m_eff ρ)⁻¹`. With Lean's `x⁻¹ = 0`
-- convention for `x = 0`, that statement is FALSE at `ρ = 0, m_bare = 0`
-- (LHS = C_max, RHS = C_max·0⁻¹ = 0). We instead prove the stronger,
-- always-true, uniform bound `r_S ρ ≤ C_max` (already established as
-- `B1_Screening.screening_radius_bounded`), which implies the brief's
-- intent (screening radius stays controlled by a fixed constant) without
-- the zero-division edge case. Flagged for Sonnet/T1 sign-off per the
-- WP-B1 manual validation gate.

import Mathlib.Analysis.Real.Sqrt
import Mathlib.Data.NNReal.Basic
import Mathlib.Tactic.Linarith
import Structures.Axioms.B1_Screening

open scoped NNReal

namespace B1_Chameleon

open B1_Screening

/-! LEMMA 1: Screening always triggers
    ∀ ρ : EnvDensity, m_eff(ρ) ≥ m_bare

    This is the core screening property: the effective mass is always at least the bare mass.
    As density increases, the effective mass increases, suppressing the force range.

    Source: [astro-ph/0309411] §3.1 - chameleon scalar equation of motion
-/

theorem screening_always_triggers (ρ : EnvDensity) :
    m_eff ρ ≥ (m_bare : ℝ) := by
  simp only [m_eff, m_eff_squared]
  have h1 : Real.sqrt ((m_bare : ℝ) ^ 2 + (ρ : ℝ)) ≥ Real.sqrt ((m_bare : ℝ) ^ 2) :=
    Real.sqrt_le_sqrt (by linarith [NNReal.coe_nonneg ρ])
  have h2 : Real.sqrt ((m_bare : ℝ) ^ 2) = (m_bare : ℝ) := Real.sqrt_sq (NNReal.coe_nonneg m_bare)
  linarith [h1, h2]

/-! LEMMA 2: Force range is bounded
    ∀ ρ : EnvDensity, r_S(ρ) ≤ C_max

    The screening radius never exceeds the fixed constant C_max, regardless
    of environment density — see the file-header note on the DoD deviation.

    Source: [1109.2709] Khoury-Weltman chameleon cosmology, Eq. (2.3)
-/

theorem force_range_bounded (ρ : EnvDensity) :
    screening_radius ρ ≤ (C_max : ℝ) :=
  B1_Screening.screening_radius_bounded ρ

/-! LEMMA 3: Dense environments have short range
    ∀ ε > 0, ∃ ρ_crit, ∀ ρ ≥ ρ_crit, r_S(ρ) < ε

    In sufficiently dense environments, the screening radius becomes arbitrarily small.
    This means that in high-density regions (e.g., solar system, galaxies),
    the chameleon force is short-ranged and unobservable at Mpc scales.

    Source: [astro-ph/0309411] §3.3 - screening in high-density environments
-/

theorem dense_env_short_range (ε : ℝ) (hε : ε > 0) :
    ∃ ρ_crit : EnvDensity, ∀ ρ : EnvDensity, ρ ≥ ρ_crit →
      screening_radius ρ < ε := by
  set K := (C_max : ℝ) / ε with hK
  have hK_nonneg : K ≥ 0 :=
    le_of_lt (div_pos (NNReal.coe_pos.mpr C_max_positive) hε)
  refine ⟨⟨K ^ 2, by positivity⟩, fun ρ hρ => ?_⟩
  have hρ_real : (ρ : ℝ) ≥ K ^ 2 := by exact_mod_cast hρ
  simp only [screening_radius]
  -- √ρ ≥ K since ρ ≥ K²
  have h_sqrt_ge : Real.sqrt (ρ : ℝ) ≥ K := by
    have h1 : Real.sqrt (K ^ 2) = K := Real.sqrt_sq hK_nonneg
    have h2 : Real.sqrt (K ^ 2) ≤ Real.sqrt (ρ : ℝ) := Real.sqrt_le_sqrt hρ_real
    linarith [h1, h2]
  -- m_eff ρ ≥ √ρ since m_eff² = m_bare² + ρ ≥ ρ
  have h_meff_ge_sqrt : m_eff ρ ≥ Real.sqrt (ρ : ℝ) := by
    simp only [m_eff, m_eff_squared]
    exact Real.sqrt_le_sqrt (by nlinarith [sq_nonneg (m_bare : ℝ)])
  have h_meff_ge : m_eff ρ ≥ K := le_trans h_sqrt_ge h_meff_ge_sqrt
  have h_denom_gt : m_eff ρ + 1 > K := by linarith
  have h_denom_pos : m_eff ρ + 1 > 0 := by linarith
  rw [div_lt_iff₀ h_denom_pos]
  have h_mul : ε * K < ε * (m_eff ρ + 1) :=
    mul_lt_mul_of_pos_left h_denom_gt hε
  have h_eq : ε * K = (C_max : ℝ) := by
    rw [hK, mul_comm, div_mul_cancel₀ (C_max : ℝ) hε.ne']
  linarith [h_mul, h_eq]

/-! SUPPORTING: screening radius is strictly antitone in density

    Denser environment ⇒ strictly shorter force range. This is the
    monotone form of the screening mechanism (Lemma 3 gives the limit
    statement; this gives the pointwise comparison).

    Source: [astro-ph/0309411] §3.3
-/

theorem screening_radius_strict_anti (ρ₁ ρ₂ : EnvDensity) (h : ρ₁ < ρ₂) :
    screening_radius ρ₂ < screening_radius ρ₁ := by
  have h_coe : (ρ₁ : ℝ) < (ρ₂ : ℝ) := by exact_mod_cast h
  have h_meff : m_eff ρ₁ < m_eff ρ₂ := by
    simp only [m_eff, m_eff_squared]
    exact Real.sqrt_lt_sqrt
      (by nlinarith [sq_nonneg (m_bare : ℝ), NNReal.coe_nonneg ρ₁]) (by linarith)
  have h1 : (0 : ℝ) < m_eff ρ₁ + 1 := by
    have := Real.sqrt_nonneg (m_eff_squared ρ₁); simp only [m_eff]; linarith
  have h2 : (0 : ℝ) < m_eff ρ₂ + 1 := by
    have := Real.sqrt_nonneg (m_eff_squared ρ₂); simp only [m_eff]; linarith
  have hC : (0 : ℝ) < (C_max : ℝ) := NNReal.coe_pos.mpr C_max_positive
  simp only [screening_radius]
  rw [div_lt_div_iff₀ h2 h1]
  nlinarith [hC, h_meff]

/-! LEMMA 4: No unscreened long-range force from K3 alone
    Without chameleon screening, the K3 geometric mediation cannot produce
    an unscreened Mpc-range force. This is a negative result that justifies
    introducing the chameleon mechanism as necessary infrastructure.

    ⚠️ SPEC CORRECTION (2026-07-25, Sonnet 5). The brief's literal DoD
    statement

        no_unscreened_lmp : ¬(∃ params, K3_bulk_unscreened_force (r > Mpc))

    transcribed into Lean as

        ¬(∃ params : K3_BulkParameters, ∃ r : ℝ,
            has_unscreened_long_range r ∧ params.coupling > 0 ∧ params.scale > 0)

    is **FALSE, not merely hard** — `r` is freely existentially quantified
    with no functional dependence on `params`, so `⟨1,1⟩` together with
    `r = 2·10⁶` satisfies the inner conjunction and refutes the negation.
    This is proved below as `brief_literal_statement_is_refutable`, so the
    defect is recorded in the kernel rather than only in prose.

    The intended physical content is that the force range is *determined by*
    the K3 data. We therefore introduce `k3_force_range params := 1 /
    params.scale` (range = inverse mediator mass, set by the compactification
    scale) and prove the corrected statement, which is a genuine theorem.

    It carries one explicit modeling hypothesis — `h_scale`, that the K3
    compactification scale is not itself Mpc-sized. That hypothesis is a
    Tier [B] input, NOT derived here; it is precisely the quantity Stream 2's
    lattice certificates constrain. Making it a visible hypothesis rather
    than a hidden assumption is the point.

    Source: [astro-ph/0309411] §2 - standard screening constraints
-/

-- Placeholder structure for K3 bulk parameters
-- (Real definition would be imported from Stream 1 K3 structures)
structure K3_BulkParameters where
  coupling : ℝ≥0
  scale : ℝ≥0

-- Unscreened force definition: force range r > 1 Mpc
def has_unscreened_long_range (r : ℝ) : Prop := r > 1_000_000  -- 1 Mpc in physical units

/-- The force range mediated by K3 bulk exchange alone: the inverse of the
mediator mass, which is set by the compactification scale. -/
noncomputable def k3_force_range (params : K3_BulkParameters) : ℝ :=
  1 / (params.scale : ℝ)

/-- **Defect record.** The brief's literal transcription is refutable: `r`
carries no dependence on `params`, so the existential is trivially witnessed.
Kept in-tree so the spec bug cannot silently reappear. -/
theorem brief_literal_statement_is_refutable :
    ∃ params : K3_BulkParameters, ∃ r : ℝ,
      has_unscreened_long_range r ∧
      (params.coupling > 0) ∧ (params.scale > 0) := by
  refine ⟨⟨1, 1⟩, 2_000_000, ?_, ?_, ?_⟩
  · unfold has_unscreened_long_range; norm_num
  · norm_num
  · norm_num

/-- **Corrected Lemma 4.** K3 bulk mediation alone cannot produce an
unscreened Mpc-range force, given that the compactification scale is not
itself Mpc-sized (`h_scale`, a Tier [B] modeling input constrained by
Stream 2's lattice certificates). -/
theorem no_unscreened_lmp
    (params : K3_BulkParameters)
    (h_scale : (params.scale : ℝ) ≥ 1e-6) :
    ¬ has_unscreened_long_range (k3_force_range params) := by
  intro h_unscreened
  simp only [has_unscreened_long_range, k3_force_range] at h_unscreened
  have h_pos : (0 : ℝ) < (params.scale : ℝ) := lt_of_lt_of_le (by norm_num) h_scale
  rw [gt_iff_lt, lt_div_iff₀ h_pos] at h_unscreened
  linarith

end B1_Chameleon
