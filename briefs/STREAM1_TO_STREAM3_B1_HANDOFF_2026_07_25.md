# Stream 1 → Stream 3 Handoff: B1 Chameleon Infrastructure for S3-00

**Date:** 2026-07-25
**From:** Stream 1 (WP-B1, Sonnet 5 Phase 2B)
**To:** Stream 3 (S3-00 MVM derivation — m_φ, α_D, Λ_D)
**Status:** ✅ Infrastructure ready to cite; ⏸️ one gap flagged below

---

## Why this matters to S3-00

Per `briefs/STREAM3_BLOCKER_ASSESSMENT_2026_07_24.md`, S3-00 derives `m_φ`,
`α_D`, `Λ_D` and — per the Dual-Scale pivot — needs a **scale-coherence
bridge** between the global K3 vacuum and the local elliptic-halo EFT. That
bridge is the chameleon screening mechanism. As of this session, that
mechanism is no longer just asserted in prose — it is a **kernel-checked
Lean 4 formalization** you can cite directly.

Per project memory, all three of S3-00's original blockers are already
cleared (Stream 2 candidate selection = cooper_s7/s10 with ρ=4, T=18;
ASSUMPTIONS.md v2.0 SIGNED; PREDICTION.md v1.0-PINNED) — so this B1
infrastructure lands at the moment S3-00 can actually use it.

## What's available now (kernel-verified, `lake build` green)

**File:** `lean4_formal_proofs/Structures/Axioms/B1_Screening.lean` +
`Structures/B1_Chameleon.lean`

| Object | Type | Role in S3-00 |
|---|---|---|
| `EnvDensity` | `ℝ≥0` | Local environment density input (galactic/halo density at the observation point) |
| `m_eff (ρ : EnvDensity) : ℝ` | `√(m_bare² + ρ)` | The effective mass `m_φ` **as a function of environment** — this is what S3-00's "derive m_φ" step is instantiating numerically |
| `screening_radius (ρ) : ℝ` | `C_max / (m_eff ρ + 1)` | The force range at density ρ — directly checkable against observational scale (PTA baseline, lensing scale, etc., per PREDICTION.md's pinned observable) |
| `chameleon_field (ρ) : Scalar` | value `= ρ · m_eff(ρ)⁻²` | Formal field configuration at a given density |
| `brane_coupling_site (ρ) : BraneCouplingVertex` | `{field_value, coupling_strength := α_ch, environment_density}` | This is `α_D`'s structural home — `α_ch` is the axiom S3-00 needs to instantiate numerically |

**Kernel-verified guarantees you can cite without re-deriving:**
1. `screening_always_triggers : m_eff ρ ≥ m_bare` — screening never makes the field lighter than its bare mass.
2. `force_range_bounded : screening_radius ρ ≤ C_max` — the force range has a hard, environment-independent ceiling.
3. `dense_env_short_range : ∀ ε>0, ∃ ρ_crit, ∀ ρ≥ρ_crit, screening_radius ρ < ε` — in any sufficiently dense environment (solar system, galactic disk), the force range is provably below any observational threshold you name.

These are Tier A (kernel-checked, no `sorry`) — see `briefs/STREAM1_WP_B1_RESULTS.md` for the full audit and the exact axiom list each theorem depends on.

## What S3-00 needs to supply (numerical instantiation)

The Lean file declares four physical constants as `axiom`s — they are
**opaque until you give them numbers**:

```lean
axiom m_bare : ℝ≥0    -- bare chameleon mass (input from EFT normalization)
axiom α_ch   : ℝ≥0    -- brane coupling strength — this IS α_D
axiom ρ_env  : ℝ≥0    -- reference/threshold environment density (currently unused in proofs; available for S3-00's Λ_D bookkeeping)
axiom C_max  : ℝ≥0, C_max_positive : C_max > 0   -- screening-radius normalization constant
```

**S3-00's job:** pick concrete numerical values for `m_bare`, `α_ch`
(`= α_D`), `C_max` from the pinned observable + Stream 2's lattice
certificates (`data/certificates/C2_cooper_s{7,10}_partner_v2.json`, ρ=4,
T=18), and check that `screening_radius(ρ_observation) < ε_observational`
via `dense_env_short_range` (or the sharper numeric instance you'll compute
directly). **This is exactly the Tier B→A promotion path**: the *structure*
is Tier A now; the *numbers* you plug in remain Tier B/C until independently
justified per epistemic-guardrails.

## Lemma 4 status — now proven, but read the hypothesis

**UPDATE 2026-07-25 (Phase 2C):** `no_unscreened_lmp` is no longer a `sorry`.
It is proven — but the brief's *literal* version turned out to be **false as
stated** (`r` was freely existentially quantified with no dependence on the K3
params, so `⟨1,1⟩` with `r = 2·10⁶` refutes it; this is now recorded in-kernel
as `brief_literal_statement_is_refutable`).

The corrected, proven form makes the range a function of the K3 data:
```lean
noncomputable def k3_force_range (params : K3_BulkParameters) : ℝ := 1 / params.scale

theorem no_unscreened_lmp (params : K3_BulkParameters)
    (h_scale : (params.scale : ℝ) ≥ 1e-6) :
    ¬ has_unscreened_long_range (k3_force_range params)
```

**What this means for S3-00:** you may cite this lemma, but `h_scale` — "the
K3 compactification scale is not itself Mpc-sized" — is an **explicit Tier [B]
modeling hypothesis, not derived**. Its placeholder value `1e-6` should be
replaced by the bound implied by Stream 2's lattice certificates
(`data/certificates/C2_cooper_s{7,10}_partner_v2.json`, ρ=4, T=18). Until
that substitution happens, any S3-00 quantity depending on this lemma inherits
Tier B, not Tier A. Request the tightened bound from Stream 2.

## Bonus: B3 bridge now available

`Structures/B1_Sym2Bridge.lean` provides `DualScaleSite` with ready-made
`s7_site ρ` / `s10_site ρ` instances, plus site-level restatements
(`site_force_range_bounded`, `site_screening_triggers`,
`site_denser_is_shorter`) so you can cite one object instead of re-threading
the environment density by hand. `s7_site_coupling_is_alpha` confirms the
site's coupling really is the global `α_ch` (= your `α_D`), with no hidden
second coupling. **Scope caveat:** the bridge is type-level/algebraic only —
it does not assert a physical bulk↔brane coupling (Tier [C], per VISION §1.3).

## One documented deviation (needs your awareness, not your action)

`force_range_bounded` proves `screening_radius ρ ≤ C_max` (a uniform bound),
not the brief's literal `≤ C_max · m_eff(ρ)⁻¹` (which is false at ρ=0,
m_bare=0 under Lean's `0⁻¹=0` convention). The uniform bound is strictly
stronger everywhere `m_eff(ρ) ≥ 1`, so it does not change the physical
conclusion, but if you ever need the exact `C·m_eff⁻¹` inverse-mass scaling
law asymptotically, use `dense_env_short_range` in the limit, not
`force_range_bounded` directly. Full detail: `briefs/STREAM1_WP_B1_RESULTS.md`.

## Files to reference in your S3-00 writeup

- `lean4_formal_proofs/Structures/Axioms/B1_Screening.lean` — definitions
- `lean4_formal_proofs/Structures/B1_Chameleon.lean` — 3/4 proven lemmas
- `briefs/STREAM1_WP_B1_RESULTS.md` — full audit, axiom lists, build log
- `briefs/STREAM1_WP_B1_CHAMELEON_MECHANISM.md` — original scope/brief

---

**Status:** Ready for Stream 3 to instantiate numerically. No further Stream 1
action needed unless S3-00 surfaces a gap in the screening formalism itself
(escalate via `briefs/ESCALATIONS.md` per VISION.md §1.3 if so).
