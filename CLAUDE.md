# CLAUDE.md — Stream 2: Selection & Geometry

Selection/geometry repo for the Dual-Scale program. Governing docs: `VISION.md`,
`EXECUTION_PLAN.md`, `TODO.md` (the restart document — read it first in every session),
`.agents/AGENTS.md` (workspace rules). Read the **epistemic-guardrails** skill before writing
any prose, **criteria-checkers** before touching `checkers/` or `refs/`, and
**autoevolve-harness** before any ranking run.

## Commands
- Regression suite: the command block in `TODO.md` §Regression — all must stay green
- Tier language: `python3 scripts/check_tier_language.py` (scans root + briefs)

## Standing rules (earned via E-007, E-010, E-012 — full text in TODO.md)
1. A test that cannot fail is not a test — every headline-number checker ships a negative control.
2. Read the source, not the certificate.
3. Retractions must be in-band (machine-visible), not prose-only.
4. Verify a directive's artifacts before executing it (six phantom-artifact occurrences to date).
5. Numbers are computed, never typed.

## 🛑 Epistemic boundaries — post-F5b/F6 ledger (added 2026-07-27)

This ledger supersedes any older number in briefs, reports, or certificates. When a document
contradicts it, the document carries (or needs) a dated correction note.

1. **Tier A (established):** `L₃ = Sym²(L₂)` is kernel-proven in Lean 4 (Stream 1) and may be
   stated as fact. The Sym² relation supplies no physical coupling by itself (VISION §1.3).
2. **Tier B (derived, not measured):** ρ = 19, T = 3 for the cooper_s7 family — derived
   (E-011, Zarhin 1983 Thm 1.6(a) + Huybrechts, fetched and read), independently verified by
   Stream 1. A derived prior is not a measurement: Gate E criterion 1 stays UNRESOLVED
   (T0 decision D1). The old ρ = 4, T = 18 and the "2× Type II" Kodaira labels are
   **RETRACTED (E-007)** — never use, cite, or "confirm" them.
3. **Kodaira readings are a category error for this family.** The finite singular loci are
   confirmed — cooper_s7: {−1, 1/27}; cooper_s10: {−1/4, 1/16} — but they are order-2
   elliptic points of the X₀(n)+ modular curve, not Kodaira degenerations (E-008/E-009;
   Dolgachev 1996 / Doran 1998, fetched, read, hash-pinned in `docs/literature/MANIFEST.md`).
   Do NOT classify Kodaira fibres from L₂ or L₃ exponents at any locus, under any
   normalization; every exponent→Kodaira lookup in this repo has been deleted or disabled.
   The one open geometric item is U1 (is T ≅ U⊕⟨14⟩?): `docs/U1_ROUTE_DESIGN_2026_07_26.md` —
   execute with its negative controls or not at all.
4. **Tier C (blocked physics):** WP S3-00b (F-theory flux/tadpole) is BLOCKED (F5b). Do not
   assume, generate, or backfill exact observables (m_φ, α_D, Λ_D) or coefficients
   (a₁, a₂, a₃). The tadpole condition is not posable until a threefold base B₃ is
   specified; until then no dark-energy / vacuum-energy claim (T0 decision D4, A-DE).
5. **Empirical pivot is T0-gated.** Parameter sweeps / exclusion-bound pipelines enter only
   via a pre-registered PREDICTION v2 amendment under the pin protocol; outputs are labeled
   exclusion/FIT — never TEST — until pinned. The WP-E5 2D transverse route stays CLOSED by
   its data floors (~1.6 Mpc, ~10⁴ objects per slice); a sweep does not reopen it.

## Escalation
Anything touching a pinned document, a frozen criterion, or this ledger is T0-owned
(Xavier): write a brief in `briefs/` and flag it instead of improvising.
