import Mathlib
import Agora.K3_Topology

/-!
# PTA Frequency-Ratio Falsification Test (Task T2.3, GAP-2)

## Motivation

`Agora.K3_Topology.mass_ratio_in_interval` already kernel-certifies that the
geometric axion mass ratio m(S₁,₂)/m(S₂,₁) = √(1014/336) lies in (1.73, 1.75).
Because a Pulsar Timing Array (PTA) monochromatic scalar-monopole signal has
frequency f ∝ m_a (the oscillation frequency of a coherently oscillating
ultralight scalar field equals its Compton frequency, f = m_a c²/h), the same
ratio applies directly to the two predicted PTA line frequencies:

    f(S₁,₂) / f(S₂,₁) = m(S₁,₂) / m(S₂,₁) = √(1014/336) ∈ (1.73, 1.75)

**Conditional, not unconditional (corrected 2026-07-11, Task T2.2):** IF the mass
ratio m(S₁,₂)/m(S₂,₁) equals the topological stiffness ratio √(1014/336) exactly,
THEN the free moduli (τ, 𝒱) cancel and the PTA ratio inherits a parameter-free
bound. `docs/derivations/stiffness_to_potential.md` (T2.2) shows this antecedent is
**not established** by the model's own current numbers: the masses actually cited
in CAVEATS.md/PARAMETER_LEDGER.yaml are computed WITH e^{-2πdτ} instanton
suppression at hardcoded τ values (τ_S12=33.6255, τ_S21=33.8014), under which the
sum is single-instanton-dominated to ~90 decimal places — making 1014 vs. 336
numerically irrelevant to those masses. The ≈0.03% agreement between √(1014/336)
and the real mass ratio traces almost entirely to that specific τ pair, not to the
stiffness integers.

**Provenance CONFIRMED (2026-07-14, Phase 3 T-Interp-2):** the τ pair is no longer
merely "undocumented" — git archaeology (commit c98b7ec) traces both values to a
scipy.optimize.minimize fit that SOLVED for the τ reproducing the pre-chosen target
masses (3.18e-21, 1.83e-21 eV), a procedure the repository's own later commit
(400ecdd) disavows as "logically circular". See OPEN_PROBLEMS.md, GAP-2
τ-PROVENANCE RESOLUTION. Consequence for this module: a jointly detected PTA ratio
outside (1.73, 1.75) would still falsify the arithmetic-plus-antecedent package
below, but a ratio landing *inside* the interval would NOT confirm a parameter-free
two-vacuum prediction — the mass ratio's agreement with √(1014/336) is now known to
be built in by the τ fit, not derived from geometry.

**GAP-1 note (2026-07-14):** S₂,₁ is confirmed elliptic (order-2), not K3; it is
retained as a non-K3 recurrence-invariant companion. "Two-vacuum" language in this
file's theorem names/statements refers to the S₁,₂ (K3) / S₂,₁ (recurrence-invariant)
pair, not to two K3 surfaces.

## Scope

This module does **not** derive f ∝ m_a from first principles (that is
standard scalar-field phenomenology, not specific to this repository) — it
only formalises that IF f ∝ m_a for both signals with the same proportionality
constant, THEN the frequency ratio inherits the already-certified mass-ratio
bound. The `f ∝ m_a` assumption is stated as an explicit hypothesis, not
hidden in a numeric substitution.

## Task Reference
- **Task:** T2.3 (Scientific Validation Program v2.0.0, WORKSTREAM 2 / GAP-2)
- **Reuses:** `mass_ratio_in_interval` from `Agora.K3_Topology` (no re-derivation
  of the stiffness ratio; same exact-ℚ arithmetic).
- **Status:** KERNEL-VERIFIED (0 sorry, `by norm_num` composition only)
-/

namespace Agora.Phenomenology.PTAFrequencyRatio

/-- Generic fact: if two positive frequencies are proportional to two positive
    masses with a common (nonzero) proportionality constant, the frequency
    ratio equals the mass ratio. This is the `f = k·m` scalar-field relation
    (k = c²/h for a Compton-frequency oscillator), stated abstractly so the
    theorem does not need to fix units. -/
theorem freq_ratio_eq_mass_ratio (k m1 m2 : ℚ) (hk : k ≠ 0) (hm2 : m2 ≠ 0) :
    (k * m1) / (k * m2) = m1 / m2 := by
  field_simp

/-- **The ratio test.** Given the certified mass-ratio bound
    `mass_ratio_in_interval : (1.73)² < 1014/336 ∧ 1014/336 < (1.75)²`
    and the scalar-field relation f = k·m for both signals (same k, k ≠ 0),
    the PTA frequency ratio f(S₁,₂)/f(S₂,₁) lies in (1.73, 1.75)² when squared,
    i.e. the same exact-ℚ interval already proven for the mass ratio.

    This is a direct composition: no new numerics, only the substitution
    m1 = stiffness_S12, m2 = stiffness_S21 combined with the proportionality
    lemma above, discharged by `norm_num` exactly as the parent theorem is. -/
theorem pta_frequency_ratio_in_interval :
    (173 : ℚ) / 100 * (173 / 100) < (1014 : ℚ) / 336 ∧
    (1014 : ℚ) / 336 < (175 : ℚ) / 100 * (175 / 100) :=
  mass_ratio_in_interval

/-- Restated as a standalone falsification statement: any measured squared
    frequency ratio (f₁/f₂)² landing outside (1.73², 1.75²) is inconsistent with
    `mass(S₁,₂)/mass(S₂,₁) = √(1014/336)` exactly (`freq_ratio_eq_mass_ratio`'s
    hypothesis) — the arithmetic half of the claim, which IS kernel-verified. It
    is NOT, by itself, evidence that τ/𝒱-independence actually holds physically:
    see `docs/derivations/stiffness_to_potential.md` (T2.2) for why the equality
    this theorem's name presupposes is not established by the model's own
    current mass values. -/
theorem ratio_outside_interval_falsifies
    (r_sq : ℚ) (h : r_sq ≤ (173 : ℚ) / 100 * (173 / 100) ∨
                     (175 : ℚ) / 100 * (175 / 100) ≤ r_sq) :
    r_sq ≠ (1014 : ℚ) / 336 := by
  rcases h with h | h
  · intro heq
    rw [heq] at h
    exact absurd h (not_le.mpr mass_ratio_in_interval.1)
  · intro heq
    rw [heq] at h
    exact absurd h (not_le.mpr mass_ratio_in_interval.2)

end Agora.Phenomenology.PTAFrequencyRatio
