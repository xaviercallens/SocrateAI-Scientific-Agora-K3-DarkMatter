# Stream 2 — T3 (two-leg agreement on n) is now a runnable test, with real known-bads

**Date:** 2026-09-21 · **Branch:** `stream2/T3-level-consistency-2026-09-21` ·
**Tier:** B · **For:** T0 (decision 2 of the K3×T² proposal), Stream 1 (citation audit)

**T3 is NOT adopted by this work.** Adoption is T0 decision 2 of
`briefs/STREAM2_K3xT2_SELECTION_CRITERIA_PROPOSAL_2026_09_16.md` §6 and stays open.
`K3_CRITERIA.md` is unchanged, nothing is scored, no certificate was promoted.

## 1. What was built

`checkers/check_T3_level_consistency.py` (+ `checkers/test_T3_level_consistency_controls.py`,
25 controls, and `data/certificates/T3_LEVEL_CONSISTENCY.json`).

| leg | what it reads | what it recomputes |
|---|---|---|
| **L — lattice** | the candidate's C2 certificate | the Gram determinant from `derived.gram_primitive_even` (not the stored `det` field); evenness of the diagonal; `Pᵀ G P = U⊕⟨d⟩` from the serialized witness `P`, with `det P = ±1`; `d = |det|`, `d = 2n`; and Sylvester's diagonal `diag(2, d, −2)` → signature (2,1). `n_L = d/2`. |
| **M — modular** | the refs *recurrence* | `z(q)`, the inverse mirror map (via `check_C1_mirror_integrality`, round trip enforced), then a Möbius fit that must FAIL and a degree-2 fit that must solve on orders ≤ 12 and **verify on held-out orders 13–40**, against the level-`n_L` eta-quotient coordinate. |

The level tested in leg M is the one leg L names. That is what makes this a gate and not a
lookup: a wrong `n_L` sends leg M to a failing fit (control S7 + R2).

## 2. Result

| candidate | `n_L` | leg M at that level | verdict | open flags |
|---|---|---|---|---|
| `cooper_s7` | 7 (det −14, `Pᵀ G P = U⊕⟨14⟩`, det P = 1) | PASS; `1/z = 49·t + 13 + 1/t` | **T3_AGREE(n=7)**, CONSISTENT | — |
| `cooper_s10` | 10 (det −20, `Pᵀ G P = U⊕⟨20⟩`, det P = 1) | PASS; `1/z = 16·t + 8 + 1/t` | **T3_AGREE(n=10)**, CONSISTENT_WITH_OPEN_ITEMS | `LATTICE_CERT_DRAFT`, `ATKIN_LEHNER_ACTION_UNVERIFIED` |

**The two s10 items are reported separately and are not the same item.**
`LATTICE_CERT_DRAFT` is process: `C2_cooper_s10_v4_DRAFT.json` is DRAFT by T0's 2026-09-16
ruling (D6′), so the s10 row is advisory. `ATKIN_LEHNER_ACTION_UNVERIFIED` is open
mathematics: the group is Γ₀(10)\*, not Γ₀(10)+, and `spike_disc_form_vs_atkin_lehner.py`
matched only the **counts** (|Aut(disc form of U⊕⟨20⟩)| = |AL(Γ₀(10))| = 4). That the
*actions* agree is unshown and referred to Deep Think, still unanswered. Collapsing the
second into the first would hide open mathematics behind a process gate.

## 3. Correction to the proposal's wording — the two legs are not independent

The proposal (§Layer 2, T3) says the two sides "name the same isogeny degree by
**independent computations**". Traced to source, that is too strong, and the checker's
docstring and certificate say so instead:

- leg L's `derived_2n_from_cusp_unipotent` comes from the monodromy representation of
  L₂/L₃ (`check_U1_lattice.py` `stage3_lattice`, a `(T_cusp − 1)²` divisibility);
- leg M comes from the q-series of the **same family's recurrence**;
- the operator and the recurrence are the same data.

So the two legs are **two disjoint computational routes from one object**, not independent
measurements. The certificate's `not_claimed` list carries this verbatim. Recommended
wording wherever T3 is described: *"internal consistency between two disjoint computations
on the same operator"*.

## 4. Discriminating power — stated honestly

**Real known-bads (real refs candidates, untampered):** the four other order-3 entries —
`apery_zeta3`, `domb`, `almkvist_zagier_second`, `avs_sporadic3_s18`, all with integral
mirror maps (C1 PASS(60)) — each **fail** the degree-2 fit at level 7 *and* at level 10.
So a passing leg M is candidate-specific, not a property of any order-3 mirror map. Real
cross-family bads fail too: `cooper_s7`'s z at level 10, `cooper_s10`'s z at level 7.

**Which clause actually fires.** `uniformizes_at_level` is a conjunction of four clauses
(Newman, deg-2 solves, deg-2 verifies held-out, Möbius fails), and the checker now reports
*which* one failed. That exposed a gap worth recording: all ten R1/R2 known-bads fail on
**`deg2_fit_solves`**, so those controls alone establish only that leg M tests degree-2
solvability at the level. The Möbius clause — the one separating a Hauptmodul for Γ₀(n)⁺/\*
from one for Γ₀(n) — needed its own known-bad, and now has one (**R4**): the level-7
coordinate fed to itself *is* a Γ₀(7) Hauptmodul; it passes Newman, deg-2 solve **and**
held-out verification, and is rejected **solely** by the Möbius clause. The clause is live.

**Stated limitations, in the certificate:**
- *No real candidate exists that has both legs and disagrees* — only s7 and s10 have a
  lattice certificate at all, and both agree. T3's power against a real disagreeing
  candidate is **UNESTABLISHED**; leg L is covered by synthetic tampering only.
- *The teeth are **directional***. Leg M is only ever run at `n_L`, so a wrong `n_L` is sent
  to a failing fit (R2, S7), but nothing here tests a correct lattice paired with a modular
  certification at some *other* level.

T0 should weigh decision 2 with both in front of them.

**Synthetic controls on leg L (each must refuse):** tampered witness `P`, tampered Gram
entry, `det P = 2`, odd U-complement, missing witness, and the two conflation rows in §5.
**25/25** behave as required.

## 5. What was leveraged from Stream 1 (Tier A-external)

Repo `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal`, commit `e801d6e`,
`Agora/Geometry/MnLattice.lean` and `Agora/Geometry/SymSquareForms.lean`, 0 sorry.
**Read as source text; no Lean build was run from this repo.**

- `TN_det` — `det(U⊕⟨2N⟩) = −2N`. With the invariance of the Gram determinant under
  unimodular base change this makes `n_L` an isometry invariant, which is why leg L is
  allowed to read `n` off a Gram matrix at all.
- `TN_diagonalises` — `diagBasisᵀ (U⊕⟨2N⟩) diagBasis = diag(2, 2N, −2)`. Re-run inside
  leg L, so the signature (2,1) is recomputed rather than copied from the certificate.
- `no_isometry_G0N_TN` — the Gauss discriminant lattice of Γ₀(N)-forms (`b² − 4Nac`,
  Gram det `−4N²`) is **not** isometric to `U⊕⟨2N⟩` (Gram det `−2N`) for any `N ≥ 1`.
  Stream 1 records that a directive had merged the two lattices into one claim; two
  controls make that block machine-visible on this side, and they are **deliberately kept
  apart** because they exercise different parts of the theorem:
  - **S1a (parity, not the determinant).** The Gauss Gram has a `1` on the diagonal, so leg
    L refuses on evenness and the determinant is never reached. Honest label: this row
    would fire identically for any odd-diagonal matrix. It is *not* the determinant leg.
  - **S1b (the determinant leg).** An *even* lattice carrying the Gauss determinant `−4N²`
    splits as `U⊕⟨4N²⟩`, so leg L reads `n = 2N²` — 98 instead of 7, 200 instead of 10 —
    and leg M has no coordinate at that level. Substituting one lattice for the other
    moves the very number T3 compares. That is the consequence of the two not being
    isometric, and it is what the citation is for.

**Derived here, not by Stream 1:** `U⊕⟨14⟩` and `U⊕⟨20⟩` are not isometric. One line from
`TN_det` plus determinant invariance (−14 ≠ −20). Stream 1 proved `G0N ≇ TN`; it did not
prove this, and it is not attributed to them.

## 6. Regression

All 18 previously-green commands plus the two new ones are green on this branch (19 checker
commands + the tier-language wrapper, 0 violations). `TODO.md` §Regression updated with the
two new lines.

## 7. Asks

1. **T0 — decision 2 of the K3×T² proposal** (adopt T3 as a hard gate?) can now be taken
   against a running test rather than a description. §4's stated limitation is the material
   input: the gate has real discriminating power on leg M and none demonstrated on leg L
   against a real candidate.
2. **T0 — wording.** Approve replacing "independent computations" with "two disjoint
   computations on the same operator" in the proposal §Layer 2 T3 (a dated correction note,
   not a silent edit), per §3.
3. **Deep Think referral, still unanswered.** The Γ₀(10)\* Atkin–Lehner action question
   (`briefs/DEEPTHINK_ALIGNMENT_BRIEF_S10_COMPOSITE_LEVEL_2026_08_01.md` §2.1) is now the
   single mathematical item standing between s10 and a clean T3, separate from the DRAFT
   status. It is worth re-transmitting.
4. **Stream 1 — citation audit.** §5 is the full list of what was imported and how it is
   attributed. Please flag anything overstated, and in particular confirm `e801d6e` is the
   right commit to pin.

---
*Generated-by: Claude (Opus 5), Stream 2 | Verified-by: `check_T3_level_consistency.py`,
`test_T3_level_consistency_controls.py` (25/25), full regression re-run | Reviewed-by: N*
