# M1 — Mechanism Memo (Phase M, Astrophysical Model Construction)

**Date:** 2026-07-26 · **Owner:** Stream 2 (T1 drafting, per directive §6) · **Stop-point:** ✅ **CLEARED — T0 ACCEPTED 2026-07-26** (decision D2, `briefs/T0_DECISIONS_2026_07_26.md`). Phase M is dormant, gated on Route γ; M2 remains unauthorized.
**Directive:** Stream 2 Directive — Astrophysical Model Construction (Phase M), Fable 5 (T0), 2026-07-25
**Length discipline:** ≤2 pages per directive §6.

---

## §0. Premise reconciliation — the directive's geometric anchor no longer exists

The directive (2026-07-25) states its Tier A/B input as: *"Sym² identity, ρ=4/T=18
Shioda–Tate, 2× Type II Kodaira fibres."* As of 2026-07-26:

| Directive premise | Current status |
|---|---|
| Sym² identity (L₃ = Sym²(L₂)) | ✅ **Stands.** Tier A, kernel-verified — E-007 *confirms* it |
| ρ = 4 / T = 18 | ❌ **Permanently retracted** (E-007). ρ=4 traced to a hardcoded `components=2` in a faulty lookup, not to geometry |
| 2× Type II Kodaira fibres | ❌ **Permanently retracted** (E-007). L₂ is a *twisted* PF operator (weight-1 modular DE for X₀(7), CM by ℚ(√−7)); exponents {0,½}, det(monodromy)=−1 ∉ SL₂(ℤ) ⇒ **no Kodaira type is derivable from L₂ by any labelling** |
| Fallback "use L₃ instead" | ❌ **Refuted** (E-008). L₃ exponents are {0,½,1} — the Sym² cross term keeps ½; gauge transforms cannot clear it (exponent differences are gauge-invariant). Only Route γ (ramified Hauptmodul pullback) survives, **untested** |

Consequence: two of the three walls in directive §3 are posed in terms of quantities
that have been withdrawn. This memo restates them honestly before answering.

## §1. Envelope statement (directive §4) — provenance-pending in this repo

The envelope numbers (0.22–0.27 Mpc transverse; β₁/β₂ at nbins=8; Coma 93.8% empty;
no public shear) are cited from `docs/WP_R6_SURVEY_SCALES.md` / `WP_R7_BETA_VARIANCE_SCAN.md`,
which **do not exist in this repository** (14 of 16 directive-referenced artifacts are
absent here; they presumably live in Stream 3's workspace). Per the directive's own
instruction ("do not re-derive from memory"), this memo **treats the envelope as an
externally supplied constraint of unverified local provenance** and requests those two
docs (or their hashes) be mirrored into this repo before M2. No observable is proposed
below, so nothing yet depends on them.

> **Provenance update (2026-07-26, post-D3):** the mirror landed — see
> `stream3_mirror/` (25 files, hash-pinned, source commit `3d18add`). The envelope
> claims were independently re-verified at mirror time (36/50 Coma duplicates exact;
> β₀ 14/30 exact; β₂ 30/30 exact; β₁ alone 29/30 — see
> `stream3_mirror/README.md` precision note). §1's provenance objection is closed.

## §2. Wall-by-wall answer (directive §3 — mandatory, silence = return)

**Wall 1 — Type II veto (a₁ / Λ_D).**
*Restated post-E-007:* the wall is now **stronger than the directive states**. There is
no certified fibre content of any type — Type II was retracted, and no replacement
exists at the L₂ or L₃ level (E-008). A fibre-derived gauge sector is therefore not
vetoed but **unconstructible**: there is no object to read a gauge algebra from.
*Route proposed:* **none from fibres.** The directive permits "a different gauge-sector
origin, stated explicitly as conjecture." The only non-fibre mechanism structure in
this repo is the WP-B1 chameleon-screened scalar sector (Tier A *structure*:
kernel-verified screening lemmas; Tier C *physics*). It is a scalar, not a gauge,
sector — and it fails M1's own standard today, see Wall 2 / §3.

**Wall 2 — Flat-direction wall (a₂ / m_φ).**
*Restated post-E-007:* "T=18 leaves 15 moduli unstabilized" can no longer be asserted —
**T is unknown**. The wall cannot be cleared *or even posed*: a stabilization story
requires knowing what there is to stabilize. Any "decoupling argument" written today
would be checkable against nothing, i.e. Tier C assumption-stacking (Rule 7).
*Route proposed:* **none nameable now.** Unblocking condition, named: Route γ delivers
an integral-exponent operator → C1v3/C2v3 emit *derived* ρ/T → this wall becomes
posable again.

**Wall 3 — Topology void (a₃ / vacuum energy).**
*Unaffected by E-007/E-008.* B₃ remains unspecified; the tadpole condition remains
unposable. *Route proposed:* adopt the directive's own second option — **any future
model under this program makes no dark-energy claim.** This is the one wall we can
route past today, by renunciation rather than construction.

## §3. The one candidate examined, and why it is not proposed

The WP-B1 chameleon sector (`Structures/B1_Chameleon.lean`) is the only mechanism chain
in this repo with Tier A structural backing (screening triggers; force range uniformly
bounded; dense environments provably short-range — suggesting, at Tier C, a
void-vs-cluster environment-dependent signature). It does not route through [A-DD]
(no Dark-Dimension scale-setting; constants are opaque axioms), so directive §2 does
not kill it. **What kills it today is Rule 7:** its three constants (m_bare, α_ch,
C_max) are uninstantiated axioms, and with ρ/T retracted there is **no certified
geometric input from which to derive them**. Choosing them so the signature lands in
the §4 envelope would be a fit dressed as a derivation — the exact failure the
directive names. *Re-entry condition, named:* if Route γ-derived lattice data can fix
or bound (m_bare, α_ch, C_max) independently of the target catalogs, this candidate
becomes nameable and would then be run through P4 siblings and the two-model rule.

## §4. Sibling list (P4, for whenever a candidate becomes nameable)

From `refs/recurrences_v1.json`: cooper_s7 (A183204) / cooper_s10 (A005260) [primary
pair]; Domb A002895; A002893; A006077; A112019; apéry ζ(2), ζ(3); s18 (Gorodetsky —
**still BLOCKED**, corrupt transcription). Note: `pipeline/siblings.py` does not exist
in this repo; the harness lives (if anywhere) in Stream 3's workspace and must be
identified before M2.

## §5. Kill condition (restated verbatim in effect)

If after the two-model pass no relation survives (𝒱, g_s)-elimination — or no mechanism
clears §3's walls without importing an unconstructed scenario — Stream 2 files the
negative under this directive and stops.

## §6. M1 verdict

**No mechanism route can currently be named past Walls 1 and 2** — not because the
walls held against attempts, but because the geometric quantities they are posed in
were retracted (E-007) and the first fallback refuted (E-008) after the directive was
signed. Per directive §7, this memo *is* the honest output. It is a **conditional
negative**, distinct from a clean kill: the single, specific unblocking condition is
**Route γ (ramified Hauptmodul pullback) yielding an integral-exponent operator and
derived C1v3/C2v3 lattice data**. If Route γ fails too, the geometric leg of this
program has no path to an astrophysical model from the s7/s10 pair, and *that* filing
would be the clean third negative.

**Requested T0 decisions:** (1) accept this conditional-negative M1 and gate Phase M on
Route γ; (2) have Stream 3 mirror WP-R6/R7 (+ hashes) into this repo; (3) confirm the
Wall 3 renunciation (no dark-energy claims) as standing policy for any future M1′.

---
*Tier discipline: no forbidden verbs applied to unconstructed physics; every mechanism
sentence above carries [Tier C] explicitly or by the §0 table. `check_tier_language.py`
does not exist in this repo — self-audited; script requested alongside WP-R6/R7.*

**Generated-by:** Fable 5 (T1 drafting under directive §6) | **Verified-by:** premise table traced to ESCALATIONS.md E-007/E-008, `checkers/check_C1_kodaira_consistency.py`, `scripts/compute_L3_monodromy.py` | **Reviewed-by:** Xavier (T0) — ACCEPTED 2026-07-26 (decision D2)
