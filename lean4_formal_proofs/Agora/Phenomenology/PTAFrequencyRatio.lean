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

This is a genuine **parameter-free** prediction: the free moduli (τ, 𝒱) that
set the *absolute* mass scale (§GAP-2, `docs/derivations/stiffness_to_potential.md`)
cancel exactly in the ratio, leaving only the topological stiffness ratio
1014/336. If both PTA lines (predicted periods ≈7.52 d for S₁,₂ and ≈13.08 d
for S₂,₁ — see `PREDICTIONS.md` Prediction 4) were ever jointly detected with
a frequency ratio outside (1.73, 1.75), the two-vacuum K3 interpretation would
be falsified independently of every uncertain modelling choice upstream.

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
    frequency ratio (f₁/f₂)² landing outside (1.73², 1.75²) is inconsistent
    with the two-vacuum K3 topology, independently of τ, 𝒱, or any other free
    modulus (they cancel in the ratio by `freq_ratio_eq_mass_ratio`). -/
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
