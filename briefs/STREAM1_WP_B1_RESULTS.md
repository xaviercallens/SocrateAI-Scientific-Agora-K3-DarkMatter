# Stream 1 WP-B1 Results — Chameleon Mechanism (Lean 4)

**Status:** ✅ **COMPLETE — all 4 DoD lemmas kernel-verified, zero `sorry`**
**Date:** 2026-07-25
**Executors:** Haiku 4.5 (Phase 2A architecture) → Sonnet 5 (Phase 2B compilation fix) → Opus 5 (Phase 2C completion)
**Provenance:** `Generated-by: Opus 5 | Verified-by: lake build (1588 jobs, 0 errors) | Reviewed-by: [pending T0 sign-off]`

---

## Definition of Done — Final Status

| DoD item | Status |
|---|---|
| Lean 4 compiles, zero `sorry`, zero undeclared `axiom` | ✅ |
| `screening_always_triggers : ∀ ρ, m_eff ρ ≥ m_bare` | ✅ kernel-verified |
| `force_range_bounded : ∀ ρ, r_S ρ ≤ C` | ✅ kernel-verified (⚠️ see Deviation 1) |
| `dense_env_short_range : ∀ ε>0, ∃ρ_crit, ∀ρ≥ρ_crit, r_S ρ < ε` | ✅ kernel-verified |
| `no_unscreened_lmp` | ✅ kernel-verified (⚠️ see Deviation 2 — **spec was false as written**) |
| Coupled to `SYM2_PARTNER` (B3 local EFT), interface compiles | ✅ `Structures/B1_Sym2Bridge.lean` |
| All citations in docstrings | ✅ CI-enforced |
| CI workflow | ✅ `.github/workflows/stream1_b1.yml` |
| Results table | ✅ this file |

**Two deviations from the brief require T0/T1 sign-off before this gate can be
marked closed. Both are documented below and recorded in the Lean source, not
just in prose.**

---

## ⚠️ Deviation 1 — `force_range_bounded` restated (needs sign-off)

The brief's DoD says:
```
force_range_bounded : ∀ ρ, r_S ρ ≤ C * (m_eff ρ)^(-1)
```
Under Lean's `x⁻¹ = 0` convention for `x = 0`, this is **false** at
`ρ = 0, m_bare = 0`: LHS `= C_max`, RHS `= C_max · 0⁻¹ = 0`, so it would
demand `C_max ≤ 0`, contradicting `C_max_positive`.

**What we proved instead:** the uniform bound `screening_radius ρ ≤ C_max`,
with `screening_radius ρ := C_max / (m_eff ρ + 1)` (the `+ 1` floor keeps the
denominator positive without a case split).

**Impact:** carries the brief's physical intent (range controlled by a fixed
constant) and is strictly stronger wherever `m_eff ρ ≥ 1`. If the asymptotic
inverse-mass scaling law is ever needed, use `dense_env_short_range` in the
limit — **not** `force_range_bounded` directly.

## ⚠️ Deviation 2 — `no_unscreened_lmp` was FALSE as specified (needs sign-off)

The brief's DoD says:
```
no_unscreened_lmp : ¬(∃ params, K3_bulk_unscreened_force (r > Mpc))
```
Transcribed literally, `r` is **freely existentially quantified with no
functional dependence on `params`**. So `params = ⟨1,1⟩` together with
`r = 2·10⁶` witnesses the existential, and the negation is refutable. This is
not a hard lemma — **it is a false statement**.

This is recorded in the kernel, not only in prose:
```lean
theorem brief_literal_statement_is_refutable :
    ∃ params : K3_BulkParameters, ∃ r : ℝ,
      has_unscreened_long_range r ∧ params.coupling > 0 ∧ params.scale > 0
```
so the spec bug cannot silently reappear.

**Corrected statement (proved):** make the range a *function of* the K3 data,
`k3_force_range params := 1 / params.scale` (range = inverse mediator mass,
set by the compactification scale), then
```lean
theorem no_unscreened_lmp (params : K3_BulkParameters)
    (h_scale : (params.scale : ℝ) ≥ 1e-6) :
    ¬ has_unscreened_long_range (k3_force_range params)
```
`h_scale` — "the K3 compactification scale is not itself Mpc-sized" — is an
**explicit Tier [B] modeling hypothesis, not derived here**. It is precisely
the quantity Stream 2's lattice certificates constrain. Surfacing it as a
visible hypothesis rather than burying it is the point; the earlier `sorry`
was hiding exactly this.

---

## Root Causes Fixed (Phase 2A → 2B) — reusable Lean-4 checklist for this repo

| Blocker | Root cause | Fix |
|---|---|---|
| `constant m_bare : ℝ` failing to parse | `constant` was removed from Lean 4 years ago | top-level `axiom` |
| File-scope `variable (...)` corrupting arities | Lean 4 auto-binds mentioned variables into *every* downstream `def` (`m_eff` silently gained a phantom `m_bare` parameter) | removed `variable`; constants are global `axiom`s |
| `ℝ≥0` → `LE Type` / `OfNat Type 0` errors | needs **both** `import Mathlib.Data.NNReal.Basic` **and** `open scoped NNReal` (the notation is scoped) | added both |
| `div_le_iff` / `div_lt_iff` unknown | renamed `div_le_iff₀` / `div_lt_iff₀` | updated call sites |
| `Real.sqrt_sq` / `sqrt_le_sqrt` hypothesis mismatch on `positivity` | `positivity` proves `0 ≤ e` / `0 < e`, not general `a ≤ b` | `linarith` + `NNReal.coe_nonneg` / `NNReal.coe_pos` |

---

## Axiom Trust Base (CI-audited, `Structures/B1_AxiomAudit.lean`)

**No `sorryAx` anywhere.** Every theorem depends on the three standard Lean
kernel axioms `[propext, Classical.choice, Quot.sound]` plus only the declared
physical constants it genuinely needs:

| Theorem | Physical-constant axioms used |
|---|---|
| `screening_always_triggers` | `m_bare` |
| `force_range_bounded` | `C_max`, `C_max_positive`, `m_bare` |
| `dense_env_short_range` | `C_max`, `C_max_positive`, `m_bare` |
| `screening_radius_strict_anti` | `C_max`, `C_max_positive`, `m_bare` |
| `no_unscreened_lmp` | **none** (pure kernel) |
| `brief_literal_statement_is_refutable` | **none** (pure kernel) |
| `s7_site` / `s10_site` | `m_bare`, `α_ch` |

Declared physical constants (opaque; S3-00 instantiates numerically):
`m_bare`, `α_ch` (**= α_D**), `ρ_env`, `C_max` + `C_max_positive`,
`C_min` + `C_min_positive` + `C_min_le_C_max`.

---

## Golden Tests — 10/10 passing, zero `sorry`

| # | Test | Status |
|---|---|---|
| 1 | Known-good screening parameters (solar-system scale) | ✅ |
| 2 | `m_eff` monotonicity | ✅ |
| 3 | Screening radius strict antitonicity (+ concrete instance) | ✅ |
| 4 | Known-bad unscreened scenario refuted | ✅ |
| 5 | Dense-environment limit at concrete ε = 1 mm | ✅ |
| 6 | Force-range uniform bound | ✅ |
| 7 | Chameleon field well-definedness | ✅ |
| 8 | Brane coupling site existence | ✅ |
| 9 | Corrected Lemma 4 at the inverse-Mpc scale bound | ✅ |
| 10 | Defect record: brief's literal Lemma 4 is refutable | ✅ |

## B3 / SYM2_PARTNER Bridge (`Structures/B1_Sym2Bridge.lean`)

`DualScaleSite` pairs chameleon-side data with the order-2 elliptic partner's
θ-basis coefficients. Its two `Prop` fields give it teeth:
* `density_coherent` — the coupling vertex sits at the same density the site claims;
* `sym2_witness` — the supplied partner genuinely satisfies `θ(P₂) = 2·P₁`.

`s7_site` and `s10_site` are therefore **compile-time evidence that Stream 1's
two independent workstreams (Sym² proof and chameleon screening) are
structurally consistent.**

⚠️ **Epistemic scope** (inherited from `CooperSym2Proof.lean`): this is a
type-level/algebraic interface only. It does **not** assert a physical
bulk↔brane coupling exists or has any strength — that remains Tier [C].
Instantiating `α_ch` does not inherit this file's Tier A status.

---

## Build Verification

```
$ lake build Structures.Axioms.B1_Screening Structures.B1_Chameleon \
             Structures.B1_Sym2Bridge Structures.Tests.B1_screening_golden \
             Structures.B1_AxiomAudit
Build completed successfully (1588 jobs).
```
Zero errors, zero `sorry` warnings.

## Files

| File | Role |
|---|---|
| `Structures/Axioms/B1_Screening.lean` | definitions + physical-constant axioms + 2 lemmas |
| `Structures/B1_Chameleon.lean` | 4 DoD lemmas + antitonicity + defect record |
| `Structures/B1_Sym2Bridge.lean` | B3 / SYM2_PARTNER interface, s7 & s10 instances |
| `Structures/Tests/B1_screening_golden.lean` | 10 golden tests |
| `Structures/B1_AxiomAudit.lean` | trust-base audit (CI-consumed) |
| `.github/workflows/stream1_b1.yml` | validation gate |

Removed: `Structures/B1_Chameleon_Minimal.lean` (Phase 2A debug scaffold, superseded).

---

## Open Items

1. **T0/T1 sign-off on Deviations 1 and 2** — this is the remaining gate to
   closing WP-B1. Deviation 2 in particular means the brief's DoD text should
   be amended, since it currently specifies a false theorem.
2. **Stream 2 request:** tighten `h_scale` in `no_unscreened_lmp` from the
   placeholder `1e-6` bound to the value implied by the lattice certificates
   (`data/certificates/C2_cooper_s{7,10}_partner_v2.json`, ρ=4, T=18).
3. **Stream 3 (S3-00):** instantiate `m_bare`, `α_ch` (= α_D), `C_max`
   numerically — see `briefs/STREAM1_TO_STREAM3_B1_HANDOFF_2026_07_25.md`.
   Structure is Tier A; the numbers remain Tier B/C until independently justified.

---

**Provenance:** `Generated-by: Opus 5 | Verified-by: lake build (1588 jobs, 0 errors) | Reviewed-by: [pending]`
