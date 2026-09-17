# Stream 2 proposal — K3 selection criteria for the K3×T² dual-scale hypothesis

**Date:** 2026-09-16 · **From:** Claude (Opus 5), Stream 2 · **To:** T0 (Xavier), for review
**Status:** PROPOSAL. Not a criteria freeze, not an amendment. `K3_CRITERIA.md` (S1, register
frozen 2026-07-20, thresholds not frozen) is unchanged. If T0 adopts any part, it goes in
through that file's §6 amendment protocol.

> **Update 2026-09-17: gate K3 now has a checker.** `checkers/check_C1_mirror_integrality.py`
> emitted `data/certificates/C1_mirror_integrality_<key>.json` for all six order-3 register
> entries. Every one is **PASS(60)** in the register's own normalization, the three
> non-candidates included, so K3 filters without ranking (as §0 expected). Its 7 controls
> include a real known-bad case: A112019's minimal operator (pinned b-file) fails
> integrality at q² = 81/8. N₁ is still TBD-AT-FREEZE. §3 has been updated in place.

---

## 0. Why write new criteria at all

The skeleton in `K3_CRITERIA.md` §2 was written before E-007 … E-016. Four of its six
criteria no longer do what they claim:

| Skeleton criterion | What happened | Consequence |
|---|---|---|
| C1 mirror-map integrality | Was never certified (the old `C1_*` files are retracted Kodaira certificates); since 2026-09-17 every order-3 register entry is PASS(60) | Needed as a gate; does not rank |
| C2 Kodaira fibre content | A category error for this family (E-007/E-008/E-009; ledger 3) | Must be **replaced**, not scored |
| C3 Sym² (`W = 0`) | Holds identically for the whole Cooper ansatz (C3's own 2026-07-18 note) | Structural consistency check only |
| C4 lattice data | Thresholds "must be derived from the EFT-matching draft"; S3-00b is BLOCKED (F5b) | Cannot be given thresholds now without fitting them to the candidates |

The M24/Moonshine proposal (Sep 16, B2 HOLD; register rejected B3) fails for a fifth reason:
the K3 elliptic genus is the same for every K3 surface, so it cannot separate any two
candidates. **Design rule for everything below: a criterion earns a place only if some
admissible candidate or control can fail it.** Each one lists the case that fails it.

## 1. What "K3×T²" means in these criteria (needs a T0 ruling)

Two readings are possible, and they lead to different criteria:

- **Reading P (literal product):** the compactification space is the product K3×T². Its
  holonomy is SU(2), a proper subgroup of SU(3), so it keeps more supersymmetry than a
  generic Calabi–Yau threefold, and the T² factor is a fixed torus unrelated to the K3's
  moduli. *(Standard fact from model knowledge, not pinned in `docs/literature/`.)* Under
  this reading nothing ties the T² to the candidate K3, so no criterion can use the Sym²
  structure: every K3 works equally well.
- **Reading S (Shioda–Inose pairing), which this proposal adopts:** "T²" is the elliptic
  side of the pairing the program has actually certified: L₃ = Sym²(L₂) (Tier A, Lean),
  the order-2 partner L₂, its modular curve, and the transcendental lattice T. For a K3
  with Picard rank 19, a Shioda–Inose structure relates it to an abelian surface E×E′ with
  T(X) ≅ T(E×E′). When E and E′ are related by a cyclic isogeny of degree n (and have no
  complex multiplication), T(E×E′) ≅ U⊕⟨2n⟩. *(Model knowledge, not pinned. Candidate
  sources to fetch: Morrison 1984, "On K3 surfaces with large Picard number", Invent.
  Math. 75, and Dolgachev 1996 §7, which is already pinned.)* Under this reading each
  candidate comes with a definite pair of elliptic curves, and "which K3" becomes "which
  isogeny degree n", which is checkable.

Reading S is the only one of the two under which a *selection* is meaningful, and it
matches TW2A Finding 2 as T0 recorded it on 2026-07-31 (`⟨−14⟩ = P̄`, "Shioda-Inose
7-isogeny"). **The physical dual-scale interpretation of either reading stays Tier C**
(VISION §1.3). None of the criteria below scores physics.

## 2. Proposed criteria

Four layers. Layers 1–3 are **gates**: a candidate either passes or leaves the selection.
Layer 4 **records** how far a construction has got and never ranks. `PASS(N)` orders are
TBD-AT-FREEZE unless a certificate already fixes them.

### Layer 0 — Admissibility (exists today)
- **K0. Citable, self-regenerating definition.** Recurrence from a fetched source, in
  `refs/` with SHA-256, and it reproduces its own stored terms.
  *Checker:* `test_refs_self_regenerate.py`. *Fails:* the corrupt s18 and zagier_A
  entries of 2026-07-20. *Open:* t103's register status (S1 flag, unanswered).

### Layer 1 — Is it a K3 family? (hard gates)
- **K1. Minimal Picard–Fuchs order is exactly 3, and L₃ is irreducible.**
  *Checkers:* `check_L3_irreducible_minimal.py`, MINODE certificates.
  *Fails:* A002893 (`MINODE_zagier_sporadic_A_A002893.json`: order 2); A112019 (order 2).
- **K2. Sym² with an integral order-2 partner.** Replaces C3 as the gate. `W = 0` alone is
  automatic for this family shape. What can fail is extracting an L₂ whose solution
  sequence validates.
  *Certificates:* `C3b_symsqrt_*`. *Fails:* `C3b_symsqrt_apery_zeta3.json` and
  `C3b_symsqrt_almkvist_zagier_second.json` (both `FAIL_PARTNER_VALIDATION`).
- **K3. MUM point plus mirror-map integrality, `PASS(N)`.** Kept from C1, with N frozen.
  *Fails:* any candidate with a non-integral mirror-map coefficient (the pre-ledger
  S₁,₂ record, q₂ = 81/8, `archive/pre-ledger/CAVEATS.md`, is the historical example; it
  would need a re-run to count as a control).
- **K4. An explicit projective K3 model exists in a fetched source.** The E-009 lesson:
  existence was a literature question. *Satisfied:* s7 and s10 by Almkvist–van Straten
  arXiv:2103.08651. *Fails:* any candidate with no such source (currently s18: "no K3
  established", ESCALATIONS E-009 follow-up).

### Layer 2 — The T² side: which elliptic pair? (hard gates; the part that can actually discriminate)
- **T1. L₂'s coordinate is a Hauptmodul for an explicit genus-0 group Γ_n, by an exact
  q-series identity `PASS(N)`, with cross-level negative controls.**
  *s7:* `HAUPTMODUL_S7_GAMMA07PLUS.json` (Γ₀(7)+). *s10:* Hauptmodul for Γ₀(10)\* found by
  the spike, no certificate yet. *Fails:* a candidate tested against the wrong level (the
  spike's s7-at-level-10 and s10-at-level-7 rows).
- **T2. Transcendental lattice T ≅ U⊕⟨2n⟩, certified with a serialized witness and an
  independent re-derivation (producer ≠ verifier), then accepted by T0.**
  *s7:* `C2_cooper_s7_v5.json` LIVE, n = 7. *s10:* `C2_cooper_s10_v4_DRAFT.json` has passed
  independent re-derivation but **T0 kept it DRAFT on 2026-09-16 (D6′)**, so T2 is not
  met for s10. *Fails:* scrambled-matrix and different-level controls in
  `test_U1_controls.py`.
- **T3 (new). Two-lineage agreement on n.** The n read from the lattice in T2 must equal the
  level of the modular group in T1, and the extra Atkin–Lehner involutions in Γ_n must be
  accounted for by isometries of T's discriminant form. This is the criterion that turns
  "K3×T²" into a checkable statement: the K3 side (monodromy lattice) and the T² side
  (modular curve) must name the same isogeny degree by independent computations.
  *s7:* lattice n = 7, modular level 7 with Fricke extension. Agrees.
  *s10:* lattice n = 10, but the modular group is Γ₀(10)\*, not Γ₀(10)+. **Open**, and
  referred to Deep Think. One exact input for that review is new today:
  `checkers/spike_disc_form_vs_atkin_lehner.py` computes, for T = U⊕⟨2n⟩, the number of
  automorphisms of the discriminant form and the size of the Atkin–Lehner group of
  Γ₀(n). They agree for every n in 1–60, including n = 7 (both 2) and n = 10 (both 4); a
  scrambled form disagrees at 15 of 60 n. **This only matches counts.** It suggests
  Γ₀(10)\* may be the expected group for T = U⊕⟨20⟩ rather than a contradiction, but it
  does not show the actions agree. That is the question for Deep Think (SPIKE, Tier B at
  best once reviewed).
  *Fails:* a lattice n that differs from the modular level (e.g. a candidate with
  det −14 whose L₂ uniformizes at level 10).

### Layer 3 — Lattice consistency (gates, weak on purpose)
- **L1. ρ and rank T derived at runtime, never typed** (`check_C2_transcendental_rank.py`;
  ρ = 19, rank T = 3 for s7 and s10 per `C2_cooper_s7_v3.json` / `C2_cooper_s10_v3.json`,
  Tier B).
- **L2. NS = T^⊥ contains U** (elliptic fibration with section). *Certificates:*
  `G0_NS_genus_cooper_s7.json`, `..._s10.json` (both DRAFT). Their own caveat applies: weak
  discriminating power. Kept as a consistency gate and never scored.
- **L3. NS contains E8(−1)², the lattice condition for a Shioda–Inose structure.** Same
  G0 certificates. Consistency with Reading S; not a ranking input.

### Layer 4 — Construction progress (recorded, never scored)
- **F1. Degree-budget screen** for two E8 loci on a threefold base (TW1, necessary
  condition only). s7: PASS on P¹×P² and on P(O⊕O(n))/P² for n = 0..3 (DRAFT); FAIL on P³.
  s10: PASS on the three P¹-bundle cases (trap-check brief, 2026-07-31).
- **F2. Explicit Weierstrass model with no unresolved codim-2 (4,6) locus.** s7: the
  locus exists (TW2A); whether it is fatal is TW2A Q1, with Deep Think. s10: not attempted,
  deliberately (it has the same open question).
- **F3. Hodge-bundle degree ℓ.** s7: computed 2 (`TW0_hodge_degree_cooper_s7.json`),
  matching the Tier B-external value in the ledger.
- **F4. Tadpole posable.** BLOCKED (F5b) until a base B₃ is exhibited. Allowed status:
  `BLOCKED`. Never scored.

## 3. Scoring: none yet

Lexicographic gates only. **No weights, no soft scores** while C4/C5-type requirements have
no EFT source. Proposed output per candidate: the deepest layer fully passed, plus the list
of open items. If two candidates reach the same layer, the report says **tie** and does not
break it. On current certificates:

| Candidate | Where it stands | Blocking items |
|---|---|---|
| cooper_s7 | Layer 1 (K0–K4) met, K3 at PASS(60); T1, T2, T3 met; L2/L3 on DRAFT certificates | L2/L3 review, F2 (TW2A Q1) |
| cooper_s10 | Layer 1 (K0–K4) met, K3 at PASS(60) | T1 (spike only, no certificate), T2 (kept DRAFT, D6′), T3 (Γ₀(10)\* question) |
| cooper_s18 | K3 at PASS(60); fails K4 | K4 (no K3 established), register quarantine |
| t103 | Not assessable | Register status (S1 flag) |

K3 (mirror-map integrality) was added 2026-09-17 via `C1_mirror_integrality_<key>.json`.
N₁ is not frozen, so "met" means PASS(60), not a frozen threshold.

This is a snapshot built from pointers to the certificates named above, not the
auto-generated live table (`K3_CRITERIA.md` §5). It says s7 is further along on Layer 2. **It does not
say s7 is the better vacuum.** Nothing here can decide that until the Tier C matching
exists.

## 4. Explicitly excluded, with the reason

| Excluded | Reason |
|---|---|
| M24 / Mathieu Moonshine / elliptic-genus criteria | Same for every K3, so they cannot discriminate (see §0). The Sep 16 text also had factual errors: the group it names has order 8160, not 960; M₂₃ does not act on a K3. *(Model knowledge, unpinned.)* |
| Mukai-type symplectic group order as a score | Returned by T0 (B2). If revived, the condition belongs on the coinvariant lattice inside NS, and T0 notes it does not separate the two ρ = 19 candidates |
| Kodaira fibre types from L₂/L₃ exponents | Category error for this family (ledger 3) |
| `W = 0` as a ranking input | Automatic for the Cooper ansatz |
| Swampland bounds named without written inequalities; observables m_φ, α_D, Λ_D | Tier C, blocked (ledger 4); C5 has a Tier B ceiling |
| "n = 2 × Cooper index" pattern | Untested, no source (s10 re-derivation brief) |
| AutoEvolve R2 Foundry / Chameleon / DarkMatterK3@Home outputs | Sandbox (ledger 7) |
| Reading P (literal product) as a selection basis | Gives the same answer for every K3 (§1) |

## 5. Housekeeping found while writing this

`C1_cooper_s7_partner.json`, `C1_cooper_s10_partner.json`, `C2_cooper_s7_partner.json` and
`C2_cooper_s10_partner.json` (the v1 files) still carried the retracted Kodaira "II" labels
and ρ = 4, T = 18 as live verdicts, with no retraction marker. Only their v2 successors and
the zagier_sporadic_A files had one, so a script reading the v1 files would have picked up
retracted values (standing rule 3). Fixed in the same commit as this brief: each file now
has verdict `RETRACTED (E-007, F6)` and a `RETRACTED` block that preserves the old verdict.
No other field changed.

## 6. Decisions requested from T0

1. **Reading S or Reading P** for "K3×T²" (§1). Everything in Layer 2 assumes S.
2. Adopt T3 (two-lineage agreement on n) as a hard gate? It is the only criterion here that
   ties the K3 side to the T² side, and it is currently open for s10.
3. Replace C2 (Kodaira) with T2 in `K3_CRITERIA.md`, via the §6 amendment protocol.
4. Confirm "no scoring, report deepest layer and ties" until an EFT source exists.
5. Literature to fetch before any freeze: Morrison 1984 (Shioda–Inose, T ≅ U⊕⟨2n⟩ for
   isogenous pairs). The §1 and §4 statements marked "model knowledge" stay unciteable
   until it is fetched.

---
*Generated-by: Claude (Opus 5), Stream 2 | Verified-by: certificate verdict strings read
from `data/certificates/` this session; `spike_disc_form_vs_atkin_lehner.py` run with its
negative control; statements marked "model knowledge" are not verified | Reviewed-by:
pending T0 (Xavier)*
