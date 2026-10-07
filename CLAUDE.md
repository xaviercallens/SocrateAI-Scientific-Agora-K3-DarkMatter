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
6. CI green is a release gate (D16′, 2026-09-29): no `vX.Y.Z` tag until the Agora CI Gate's
   post-merge run on `main` reports Gates A–D green; a red run is recorded in the release brief
   with its run id, never described as "should be fixed".

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
   S3 `DEEPTHINK_DEBRIEF_AUDIT_2026_07_29.md`). **ℓ, amended D19′ (2026-10-07, on T0's behalf
   under explicit delegation; `briefs/T0_DECISIONS_2026_10_07_STREAM2_DELEGATED.md`):** ℓ := χ(O_K3) = 2
   is the fundamental-line-bundle degree of the Weierstrass model (Tier A, Noether, deg Δ = 24);
   the family-level Hodge-bundle degree over X₀(7)+ is 2/3 (Tier B, `TW0_HODGE_DEGREE_ORBIFOLD.json`),
   so "ℓ = 2 via the Sym² theorem" was a conflation of two readings — WP-TW0 CLOSED (F6 brief
   `WP_TW0_HODGE_DEGREE_REEXAMINATION_2026_10_07.md`). Do not spend compute on G1-b or any
   strict-pullback geometry. Twisted-Weierstrass is the PRIMARY route; its gate, the two-E8
   degree-feasibility screen (WP-TW1, deg Δ = 48 on P³), is **LIVE (D20′)**: P³ as given FAILS
   (forced collision), P¹×P² and P(O⊕O(n))/P² PASS as a necessary condition only; next is WP-TW2
   (M₇-polarization: a section with P̄·Ō = 5, `check_TW2_height_condition.py`).
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

8. **The ρ = 20 cut is ADOPTED — and read narrowly (T0 decision D7′, 2026-09-21,**
   `briefs/T0_DECISIONS_2026_09_21_STREAM2.md`; Stream 3 ruling R1 of the same day). The program
   adopts ρ = 20 as a selection criterion: inside a register family, the candidates are the members
   whose transcendental lattice is rank 2 and positive definite — the CM points of the modular
   curve (`CM_POINTS_RHO20.json`, `A2_MEMBERSHIP.json`, Tier B). **The ruling adopts nothing else.**
   No ranking of cooper_s7 over cooper_s10 and **no minimum-|D| rule** ("A₂ ∈ s7 family, A₂ ∉ s10
   family" is a lattice fact, not a preference); cooper_s10 stays ADVISORY (D6′ untouched); the
   agreement between the binary-form side and the modular side is **forced** (elliptic ⇒ CM,
   Shioda–Inose) and is never to be presented as corroboration; CM points are dense on the curve,
   so the cut gives a finite list only per discriminant; no CM point maps to any observable (rule 4
   stands); `K3_CRITERIA.md` is not edited by this ruling (§6 amendment protocol), and gate T3 is
   still not adopted. Widening any of these needs its own T0 text.

9. **A C6 selector is ADOPTED, narrowly (AM-8, 2026-09-28; `K3_CRITERIA.md` C6, `briefs/
   STREAM2_AM8_SELECTOR_COMPARISON_2026_09_28.md`).** T0 chose "SEL-D: minimal `|disc T|`" from two
   computed alternatives, via `AskUserQuestion`. This narrows item 8's "no minimum-|D| rule": that
   phrase now reads as barring only a **cross-family** ranking by `|D|` (the sentence right after it —
   "A₂ ∈ s7, A₂ ∉ s10, is a lattice fact, not a preference" — is unchanged and still governs comparing
   families). It does not bar a **within-family** discriminant-floor selection, which AM-8 adopts:
   per family, the candidate of minimal `|disc T|`, verified unique on the modular curve (not by class
   number alone) — `T = A₂` (`D = −3`) for cooper_s7, `T = ⟨2⟩⊕⟨2⟩` (`D = −4`) for cooper_s10
   (ADVISORY, D6′ untouched). Nothing else in item 8 changes: no cross-family ranking, no physical
   reading, no promotion of s10's DRAFT lattice certificate, gate T3 still not adopted. Reversible by
   one T0 sentence.

10. **No Kodaira label for the explicit Weierstrass model either (D14′, 2026-09-29, taken on T0's
    behalf under explicit delegation and confirmed by T0 the same day;
    `briefs/T0_DECISIONS_2026_09_29_STREAM2_DELEGATED.md`).** Item 3's
    prohibition is read to cover the explicit M₇-polarized Inose/CDLW model and its Kuwata–Shioda
    fibration (`INOSE_MODEL_M7.json`, `INOSE_FIBRATION_MULTIPLICITIES.json`): discriminant-root
    **orders** may be reported; fibre **types** (I_n, I_n*, II, III, IV, …) may not be attached to any
    cooper_s7/s10 locus, at any normalization, in any document. GE-10 is closed at the level of orders
    (both s7 loci {10,10,2,1,1}; the extra Picard class is a Mordell–Weil section, not a fibre).
    Reversible by one T0 sentence; a reversal must name the fibre-type derivation it accepts.
11. **`C2_cooper_s10_v5.json` is LIVE (D15′, 2026-09-29, taken on T0's behalf under explicit
    delegation and confirmed by T0 the same day; same brief).** Value-identical promotion of `C2_cooper_s10_v4_DRAFT.json` after re-running the
    independent re-derivation (23/23) and the witness check; D6′'s "stays DRAFT" is superseded. What
    lifts: the ADVISORY label that rested only on the DRAFT status. What does not change: no ranking
    of cooper_s7 over cooper_s10 (items 8/9); `C2_cooper_s10_v3.json` stays the runtime ρ/T source;
    the identification with T is still Tier B (Dolgachev/Doran); certificates emitted before
    2026-09-29 keep their `LATTICE_CERT_DRAFT` flags until re-emitted (value-identical,
    provenance-stale). Reversible by one T0 sentence (v4_DRAFT retained unchanged).

## Escalation
Anything touching a pinned document, a frozen criterion, or this ledger is T0-owned
(Xavier): write a brief in `briefs/` and flag it instead of improvising.
