# K3_CRITERIA.md — amendment proposal under §6, for T0 (2026-09-21)

**Status: PROPOSAL. Nothing in `K3_CRITERIA.md` is edited by this brief.** It gives T0, for each
open point, the exact text to approve or refuse. Base text: Stream 1's copy
(`SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal/K3_CRITERIA.md`, last changed at their
commit 6c09d2d, 2026-07-24), which is the more recent of the two copies (see AM-5).
§6 requires for each amendment: motivation, exact diff, impact statement.

**Impact statement common to all five.** Criteria v1.0 has never been frozen (§7 pre-freeze
checklist still blocks it; the 2026-07-18 register amendment says so). No ranking run on record was
produced under frozen criteria, and no scoring has been run since the 2026-09-16 K3×T² proposal
("no scoring, report deepest layer and ties"). §6 rule 2 therefore demotes no existing output.
All five amendments add or re-word **gates and records**; none introduces a score.

---

## AM-1 — the adopted ρ = 20 cut enters as a new criterion C6 (ruled: D7′)

*Motivation.* T0 adopted the cut on 2026-09-21 (D7′; Stream 3 R1) and read it narrowly. The
criteria document must say exactly that much and no more.

*Exact text to add after C5:*

> ### C6 — Definiteness cut (ρ = 20) (T0 D7′, 2026-09-21)
> - **Definition:** within a register family, the *candidate surfaces* are the members whose
>   transcendental lattice has rank 2 and is positive definite (ρ = 20): the CM points of the
>   family's modular curve. A member is named by `(family, D, z)` with `T_X` its reduced form.
> - **Checking procedure:** `checkers/check_CM_points_rho20.py` (table),
>   `checkers/check_A2_membership.py` (occurrence criterion: *D occurs at level n iff D is a square
>   mod 4n*), `checkers/check_CM_completeness_classnumber.py` (completeness per listed D).
> - **Threshold:** membership is exact lattice arithmetic; z-values are numeric recognitions and
>   are reported as such, through a Hauptmodul relation quoted `PASS(N)`.
> - **Failure:** a proposed surface that is not a CM point of a register family is outside C6.
> - **What C6 is not:** not a ranking — no ordering by |D|, no preference between families;
>   not corroboration — elliptic point ⇒ CM is forced, and the binary-form and modular sides agree
>   by Shioda–Inose; not complete beyond the discriminants a certificate lists (CM points are dense
>   on the curve); not physical — no member maps to an observable (F5b).
> - **Tier:** B. **Scoring:** none.

## AM-2 — C3: "integral in which coordinate?" (Stream 3's D-2) — OPEN, two readings

*Motivation.* C3's definition reads: *"L₃ equals Sym²(L₂) for an explicitly exhibited order-2
operator L₂"*. **The text contains no integrality requirement.** On the literal text s7 and s10
both pass (operator identity proven for all n: `C3b_symsqrt_cooper_s7/s10.json`; Stream 1
`partner_res0..3`, `partner_eq_sqrt_s10`). Integrality of the partner *sequence* is a separate
attribute, and it is coordinate-dependent: s10's and s18's partners are integral in **2z**, s7's in
z (`PARTNER_GLOBAL_BOUNDEDNESS.json`, PASS(160); bound e(n) ≤ n−1 for all n modulo two Stream 1
theorems).

*Reading L (literal; Stream 2's recommendation).* Add one sentence to C3:

> - **Integrality is not part of C3.** The partner's *global boundedness constant* — the least c
>   with the partner series integral in the coordinate cz — is **reported** as an attribute
>   (`checkers/check_partner_global_boundedness.py`), never used as a gate or a score.

*Reading I (integral in the given coordinate z).* Add instead:

> - **The partner series must be integral in the family's own coordinate z.**

Impact of I: s10 **fails** C3 (c = 2), s7 passes; by C3's own failure clause that is *F1 removal
of s10 for the dual-scale role*. That is a large consequence to hang on a choice of coordinate, and
Stream 1's note already calls C3 "STRUCTURAL, not a discriminating filter" — which is why we
recommend L. It is T0's call.

## AM-3 — C2 (Kodaira fibre content) is a category error for this register — replace by the lattice gate

*Motivation.* Ledger item 3: the singular loci are elliptic points of X₀(n)⁺, not Kodaira
degenerations; every exponent→Kodaira lookup has been deleted; the C1/C2 Kodaira certificates are
retracted (E-007). C2 as written cannot be run on any register primary and its checker
(`check_C2_kodaira.py`) must not be. Already proposed on 2026-09-16
(`STREAM2_K3xT2_SELECTION_CRITERIA_PROPOSAL_2026_09_16.md`, decision 3), still unanswered.

*Exact change:* retitle C2 "Transcendental lattice (T2)", body:

> - **Definition:** T ≅ U⊕⟨2n⟩, certified with a serialized base-change witness and an independent
>   re-derivation (producer ≠ verifier), then accepted by T0.
> - **Checker:** `checkers/check_U1_lattice.py`, `check_U1_witness_serialization.py`,
>   `independent_rederivation_C2_s10_v4.py`. **Status:** s7 LIVE (`C2_cooper_s7_v5.json`); s10 DRAFT.
> - The former Kodaira text is kept below, struck, with its retraction reference (E-007, F6).

## AM-4 — T1 and T3 as consistency gates, never scored (decision 2 of the K3×T² proposal)

*Motivation.* T3 now runs (`check_T3_level_consistency.py`, 25 controls) and the Atkin–Lehner
side is an explicit isomorphism W(n) → O(q_A), PASS(30) (`ATKIN_LEHNER_DISC_FORM.json`).

> ### T1 — modular coordinate. L₂'s coordinate is a Hauptmodul of an explicit genus-0 group,
>   by an exact q-series identity quoted PASS(N), with cross-level negative controls.
> ### T3 — level consistency. The n re-derived from the lattice certificate equals the level at
>   which the mirror map uniformizes. **Two disjoint computations on the same operator — not
>   independent measurements.** Consistency gate; never a score.

*With it:* in `check_T3_level_consistency.py`, replace the flag `ATKIN_LEHNER_ACTION_UNVERIFIED`
by the narrower `ATKIN_LEHNER_ACTION_VERIFIED_LATTICE_LEVEL__S10_LATTICE_CERT_DRAFT`: the action is
no longer the open item; the DRAFT status of the s10 lattice certificate is. Stated limits stay:
no real candidate with both legs disagrees; the teeth are directional.

## AM-5 — one canonical copy

*Motivation.* Stream 1's copy (188 lines) and Stream 3's (143 lines) differ in 6 hunks — Stream 3's
is the older skeleton (still `SYM2_UNVERIFIED` for s7/s10, older t103 handling). This repository,
which owns selection, has **no root copy**. Proposal: the canonical file lives **here** (Stream 2
owns ranking per Stream 1's README), seeded from Stream 1's copy plus whichever of AM-1…AM-4 T0
approves; the other two repositories keep a mirrored, hash-pinned copy that fails closed on drift
(the mechanism Stream 3 already uses for our certificates).

---
*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: C3 and §6 text read in Stream 1's
`K3_CRITERIA.md` at 6c09d2d; every certificate named exists on `main` at v0.3.10 | Reviewed-by: N*
