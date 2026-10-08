# Which K3 is the selected point? — identification (2026-10-08)

**Asked by T0:** "continue now and identify the K3." **Checker:** `checkers/check_selected_k3_identification.py`
(+10 controls); certificate `data/certificates/SELECTED_K3_IDENTIFICATION.json`. Lattice and discriminant language only; no
Kodaira label; no physics; no ranking.

## The answer

A singular K3 surface (Picard number 20) is determined up to isomorphism by its transcendental lattice up to SL₂(ℤ)
(Shioda–Inose; Thm 8.1 of Kumar–Kuwata and l.912 of Shioda 2007, both pinned and read). So the surface is named by the class
of T:

| point | T (Gram) | det | classes of that det | the K3 surface |
|---|---|---|---|---|
| **cooper_s7, z = ∞ — the AM-8 pick** | [[2,1],[1,2]] | 3 | 1 | **X₃, Vinberg's "most algebraic" K3** (table No. 1) |
| **cooper_s10, z = ∞ — the AM-8 pick** | [[2,0],[0,2]] | 4 | 1 | **X₄, Vinberg's second most algebraic K3** (table No. 2) |
| cooper_s7, z = −1 | [[2,1],[1,4]] | 7 | 1 | X₇ (table No. 3, Ujikawa) |
| cooper_s7, z = 1/27 | [[2,0],[0,14]] | 28 | **2** | the singular K3 with T = ⟨2⟩⊕⟨14⟩; the other class at determinant 28 is 2·[[2,1],[1,4]] (non-primitive) — the determinant alone does **not** name it |

Sources (all read; table and statements **parsed from the pinned text**, not typed): T. Takatsu, arXiv:1903.03054 — the table of
transcendental lattices with its attributions (No. 1 [2,1,2] and No. 2 [2,0,2] to Vinberg, No. 3 [2,1,4] to Ujikawa), the
sentence "the singular K3 surfaces with discriminant d is unique up to isomorphisms for d = 3, 4, 7, so we denoted by X_d", and
§5.1: X₃ is the minimal resolution of (E_ω × E_ω)/σ with σ(x,y) = (ωx, ω²y), E_ω = ℂ/ℤ+ℤω, and X₄ the same with E_i. The class
counts in the table above are **computed** (reduced forms enumerated, non-primitive included), not quoted.

## What it connects to

- **Consistency with the explicit model, not corroboration.** At z = ∞ the pinned Inose/Kuwata–Shioda model has σ = π = 0, i.e.
  Shioda–Inose partner E_ω × E_ω (`INOSE_MODEL_M7.json` S6) — exactly the partner Takatsu uses for X₃. This agreement is forced
  by the Shioda–Inose structure (ledger item 8); it is stated as consistency only.
- **Why the picks look like this (computed).** The determinants attained by any positive-definite even rank-2 lattice start
  3, 4, 7, 8, 11. The AM-8 s7 pick sits at the absolute minimum 3 and the s10 pick at the next value 4; s10 cannot reach 3
  because A₂ is absent from its family (`A2_MEMBERSHIP.json`). This is a lattice fact forced by arithmetic — not a preference,
  not corroboration, and **no cross-family ranking** follows (items 8/9).
- **Fibration language (step 2a, unchanged).** X₃ carries an elliptic fibration with NS = U ⊕ E8² ⊕ A₂ and Mordell–Weil rank 0.
  Schütt–Shioda (l.3295, citing Nishiyama) state that X₃ has exactly six elliptic fibrations; **whether ours is one of the six
  is not verified** (Nishiyama's paper not fetched).

## Not identified / not claimed

- That the family member at that parameter value is a smooth fibre of a specific projective model: `A2_MEMBERSHIP.json` records
  that what is established is a point of the period domain. The identification is of the *surface with that period*.
- Anything from Vinberg 1983 beyond what Takatsu's table and Schütt–Shioda l.3293 state (not fetched).
- A correction to an earlier moment of this session: a search snippet had attributed the Takatsu paper to "Shimada–Veniani";
  the paper's own header names Taiki Takatsu (it only cites Shimada). The pin and file names use the header.
- Tiers: T = v⊥ is Tier B (Dolgachev §7); bijection and table are Tier L; the statement "X₃ is the cooper_s7 K3 at z = ∞" is
  therefore **Tier B**, with the lattice half of the chosen vector Tier A (two independent kernel sources).

*Generated-by: Claude (Sonnet 5.5), Stream 2 | Verified-by: the certificate and its 10 controls; pinned sources with line numbers in `docs/literature/MANIFEST.md` | Reviewed-by: N*
