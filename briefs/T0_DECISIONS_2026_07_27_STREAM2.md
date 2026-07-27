# T0 Decision Record — 2026-07-27 (Stream 2: post-U1 decisions)

**Authority:** Xavier Callens (T0), verbal in-session 2026-07-27, responding to the
decision list in `briefs/STREAM2_TO_STREAMS1_3_U1_CLOSED_2026_07_27.md` §"T0 decisions"
and the M1′ options (`briefs/STREAM2_M1PRIME_MECHANISM_MEMO_2026_07_27.md` §4). Recorded
by T1 coordinator. Scope: exactly these four decisions.

## D1′ — C2 v4 ACCEPTED

`C2_cooper_s7_v4.json` is live (promoted from the DRAFT, which is retained unchanged for
audit): T ≅ U⊕⟨14⟩ [Tier B], det −14, explicit integral splitting, with the two residual
Tier-B links as stated in the U1 brief §4. Operational consequences, stated to prevent
the value-vs-gate-scoring conflation recurring:
- **H-M7 upgrade is PARTIAL:** the T-half (T = U⊕⟨14⟩) is now [B]; the NS-half
  (NS = U⊕E₈²⊕⟨−14⟩) **stays [C]** — it requires the Nikulin-type primitive-embedding
  step that has not been executed (M1′ route R1). No document may cite H-M7 as
  wholesale-[B].
- v3 remains the runtime source for the ranks (ρ = 19, T = 3 — identical in v4); no
  checker rewiring is implied by this acceptance.
- **Gate E scoring is unchanged** (T0 D1 of 2026-07-26 stands): a derived lattice is
  still not a measurement; criterion 1 remains UNRESOLVED absent a valid empirical run.

## D2′ — S3-00 §2(b): RE-SCOPED onto the derived geometry

The Kodaira-based derivation clause is replaced by amendment **A1** in
`EXECUTION_PLAN.md` (Amendment log): α_D, Λ_D derivation is re-posed on the certified
M₇-polarized lattice data, and is **posable only given an exhibited fourfold X₄ with base
B₃** (M1′ routes R1/R2 — the same missing object as the Phase M re-gate). No Kodaira
reading may be reintroduced under any normalization. Until an X₄ is exhibited, the step
is dormant-by-construction and F5b stands.

## D3′ — Phase M: OPTION B (dormant, re-gated); M1′ accepted as the standing memo

T0's phrasing contained both "reopen against M1′" and "consider option B keep dormant and
re-gate"; **T1 records the final clause — Option B — as the decision** (it was also both
recommendations), reading "against M1′" as acceptance of M1′ as the standing mechanism
memo superseding M1. T0 may correct this reading; a correction would be recorded as a new
decision, not an edit here. Effect: Phase M stays dormant; D2-of-2026-07-26's Route-γ
condition (discharged) is REPLACED by: **Phase M reopens only upon (i) an exhibited
X₄/B₃, making A.1.4/A.3.4 posable, plus (ii) a flux vector for A.2.5, plus (iii) for
route R1 additionally the NS promotion step and a fibration selection principle** — per
M1′ §revisit conditions. M2 remains unauthorized.

## D4′ — v0.4.0 still means "Gate E PASS"

The reservation is retained with its original meaning. Plainly stated consequence: under
D1 (criterion 1 UNRESOLVED) and E-012 (no valid D-3 run possible), v0.4.0 is not
reachable on current evidence and stays parked until a valid empirical route exists
(candidates: the re-gated S3-00 §2(b) given an X₄; a T0-ratified WP-E5 successor; a
pinned WP-E6 program). The TODO item closes as ANSWERED, not as achieved.

## D5′ — C2 v5 (P-witness serialization) ACCEPTED, promoted to LIVE

`C2_cooper_s7_v5.json` is now the LIVE lattice certificate for cooper_s7, superseding
`C2_cooper_s7_v4.json` in that role (v4 and `v4_DRAFT.json` retained unchanged for audit,
same treatment as v3 when v4 was promoted). v5 adds exactly one field vs v4 —
`derived.u_splitting.basis_change_matrix`, the explicit GL₃(ℤ) witness P that
`stage3_lattice()` computed in memory but previously discarded — motivated directly by
Stream 1's independent-verification finding
(`briefs/STREAM1_U1_INDEPENDENT_VERIFICATION_2026_07_27.md`, Stream 1 repo: the v4
certificate recorded det(P) and PᵀGP but not P itself, forcing third parties to
re-derive their own witness). No other derived/how/controls/tier field values changed.
`C2_cooper_s7_v3.json` remains the unaffected runtime source for ranks (ρ=19, T=3); no
checker rewiring implied. Verification: `checkers/check_U1_witness_serialization.py
--all` and its 6 controls (`test_U1_witness_serialization_controls.py`), plus the full
13-command regression, all green pre- and post-promotion.

Authority: Xavier Callens (T0), verbal via T1 coordinator, 2026-07-27 (same session as
D1′–D4′, decided in parallel with WP-E6b's option-A ruling in the Dark Home repo).

---
Generated-by: Fable 5 (T1 coordinator) | Verified-by: n/a (decision record); certificate
promotions in `data/certificates/C2_cooper_s7_v4.json` and `C2_cooper_s7_v5.json` carry
the acceptance fields | Reviewed-by: Xavier (T0) — records his own in-session decisions;
the D3′ Option-B reading is explicitly flagged for his confirmation
