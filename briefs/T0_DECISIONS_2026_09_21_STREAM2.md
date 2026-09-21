# T0 decisions — 2026-09-21 (Stream 2 record)

**Ruled by:** T0 (Xavier Callens), in the Stream 2 session of 2026-09-21. **Recorded by:** Claude
(Fable 5.1). Numbering continues `briefs/T0_DECISIONS_2026_09_16_STREAM2.md` (D6′).

## D7′ — the ρ = 20 cut is ADOPTED in this repository too

**Context.** Stream 3 reported (`briefs/STREAM3_TO_STREAMS1_2_T0_RULING_RHO20_ADOPTED_2026_09_21.md`,
filed here as received) that T0 had adopted decision D-1 of its
`T0_DECISION_REQUEST_K3_SELECTION_2026_09_21.md`, recorded there as ruling R1 with the T0 text
*"adopt decision 1 and implement what you could at this stage waiting for others streams"*.
A ruling given to another session is not applied here on report alone (lesson of 2026-09-16, D6′:
a menu choice is not a ruling), so T0 was asked directly in this session whether the adoption holds
for this repository with Stream 3's narrow reading.

**T0 text (verbatim, this session):** *"oui je confirme la coupure aussi sur ce repo."*

**What is adopted.** The program adopts **ρ = 20** as a selection criterion: a K3 candidate is a
member of a register family whose transcendental lattice has rank 2 and is positive definite, so
classification runs by positive-definite binary quadratic forms, finite at each discriminant.
Inside the two register families this is the CM-point locus computed in `CM_POINTS_RHO20.json` and
`A2_MEMBERSHIP.json` (Tier B).

**What is NOT adopted — the ruling does not say it, and each item needs its own T0 text:**

- **No ranking of cooper_s7 over cooper_s10 and no minimum-|D| rule.** "A₂ is in the s7 family and
  not in the s10 family" stays a lattice fact. Note the register's GE-14: two known principles point
  at *different* members (the (−2)-walls at D = −28, −7; the minimal discriminant at D = −3), and
  the ruling chooses between them no more than it chooses a candidate.
- **No corroboration claim.** Elliptic point ⇒ CM is forced (`ELLIPTIC_POINTS_ARE_CM.json`); the
  binary-form side and the modular side agree by Shioda–Inose.
- **cooper_s10 stays ADVISORY.** D6′ is untouched; the adoption promotes no s10 row and does not
  make `C2_cooper_s10_v4_DRAFT.json` LIVE.
- **No physical reading.** No (m, f) prior, m_φ, α_D or Λ_D follows from any CM point; that map is
  Tier C, BLOCKED under F5b, and the tadpole is unposable without B₃ (ledger item 4). The flux
  literature read on 2026-09-21 supplies no bound on |D| for a one-parameter family
  (`briefs/T0_DECISION_REQUEST_FLUX_BOUND_ON_D_2026_09_21.md`).
- **`K3_CRITERIA.md` is not frozen or edited by this ruling.** How the cut enters the criteria
  (a new criterion? wording? which coordinate for C3 — Stream 3's D-2; the two-entry register —
  their D-3) is still open and goes through the §6 amendment protocol.
- **Gate T3 is not adopted** by this ruling (decision 2 of the K3×T² proposal, still open).

**Known limits the adoption inherits (unchanged by it).** The CM table is complete on the
discriminants it lists and silent elsewhere (window −v² ≤ 44); z-values are numeric recognitions
through a relation certified PASS(40); "v·ω = 0 ⇒ ρ = 20, T_X = v^⊥" is the cited Dolgachev 1996 §7
framework, not proved here; CM points are dense on the modular curve, so the cut yields a finite
list only per discriminant.

**Actions taken under D7′ (same PR).**
1. `CLAUDE.md` ledger: item 8 added (dated).
2. `TODO.md`: the "ρ = 20 fork" item closed with this record; the remaining open T0 items kept.
3. Six checkers and one renderer: "not adopted" wording replaced by the narrow adoption; all
   certificates re-emitted and briefs re-rendered. **No computed value changes** — verified by
   diffing the certificates before and after with the status / not-claimed / hash / version fields
   set aside.
4. Stream 3 told: their mirror drift detector will fail closed on the new certificate hashes, by
   design; they re-read, re-run the controls and re-mirror.

---
*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: T0 text quoted verbatim from this
session; Stream 3's record read at its source (`briefs/T0_RULINGS_2026_09_21.md`, their repository) |
Reviewed-by: T0 Y for the ruling itself; the narrow reading is recorded as Stream 3 proposed it and
as T0 was asked to confirm it, and is countermandable*
