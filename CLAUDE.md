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
6. **Route A (strict pullback) is CLOSED — T0 countermand 2026-07-29** (`briefs/
   T0_COUNTERMAND_R2_2026_07_29.md`). Tier B structural negative: no strict-pullback
   Calabi-Yau realization of the cooper_s7 family exists over K²≠0 bases (G1-a, in-house
   exact, LIVE) nor via any even-ramification escape on K²=0 bases (O2/O3, hand-verified —
   S3 `DEEPTHINK_DEBRIEF_AUDIT_2026_07_29.md`). The Hodge-bundle degree ℓ = 2 is ratified
   **Tier B-external** (T0s derivation via the Tier-A Sym² theorem; in-house verification
   WP-TW0 pending — if it lands ≠ 2, F6 disclosure + T0 escalation). Do not spend compute on
   G1-b or any strict-pullback geometry. Twisted-Weierstrass is the PRIMARY route; its gate
   is the two-E8 degree-feasibility check (WP-TW1; use deg Δ = 48 on P³, not 144).
7. **"AutoEvolve R2 Hypothesis Foundry" / K3-T2-Chameleon / DarkMatterK3@Home track is an
   EXPLORATORY SANDBOX** (T0 ruling, 2026-08-01, same standing as rule 4's Route-A-adjacent
   discipline and mirroring the identical S3 CLAUDE.md rule 7). Covers
   `AUTORESEARCH_IMPLEMENTATION_GUIDE.md` — the pre-ledger 2026-07-14 sieve
   (`k3_sieve_analysis.py`) + G1/G2/QT physics-viability gate funnel
   (`candidate_pool.yaml`, 13→5→3 selection) — and its S3 counterpart (`api/discoveries.json`
   35 `K3-DISC-*` entries, `ui_loom/`, `core_wasm/`, `public/wasm/`, `AGORA_K3_T2_BRIDGE_PLAN.md`,
   `PHASE5_IMPLEMENTATION_PLAN.md`). **No claim from this material — including any candidate's
   "K3/T2" geometry-class assignment, achievable-mass contour, or the Chameleon coupling
   formula — may be cited as evidence for cooper_s7/s10 or into this repo's Tier A/B/C
   certificates.** **Naming collision, explicit — three similarly-named, UNRELATED systems in
   this program:** (a) **"AutoEvolve"** (this repo, `autoevolve-harness` skill, top of this
   file) is the CURRENT, sanctioned, checker-certificate-ONLY scoring harness over cooper_s7/s10
   — legitimate, part of Streams 1–3, unaffected by this rule. (b) **"AutoEvolve R2 Hypothesis
   Foundry"** (this rule) is the pre-ledger sieve+physics-gate funnel over binomial-sum
   sequences — sandboxed by this rule, despite sharing the word "AutoEvolve" with (a). (c)
   **"AlphaEvolve"** (Stream-4, Vertex AI, S3 CLAUDE.md rule 5) is a third, unrelated codebase.
   Do not conflate any of the three. Resumed work on (b)/DarkMatterK3@Home stays on its own
   branch(es), not `main`, labeled `sandbox/`, until a future T0 ruling reconciles or retires it.

## Escalation
Anything touching a pinned document, a frozen criterion, or this ledger is T0-owned
(Xavier): write a brief in `briefs/` and flag it instead of improvising.
