# T0 Decision Request — does a published flux bound on attractive K3 pairs have any authorised use here?

**Date:** 2026-09-21
**From:** Stream 2 (task B4 of the thought-experiments batch)
**To:** T0 (Xavier Callens)
**Status:** DECISION REQUESTED — two questions (Q1, Q2). **Nothing was executed.** WP S3-00b
(flux / tadpole) is BLOCKED (F5b, CLAUDE.md ledger item 4) and stays BLOCKED after this brief.
**What this file is:** a literature reading, a statement of what five sources say verbatim, a
tension with LeanMaster Stream 9, and options. It carries no checker, no certificate, no number
about any candidate, and no physical claim. The `unblock-tier-c` skill was followed: its Step 3
(tadpole retry) has three preconditions. Q1 below concerns the **second** (is a threefold base
specified?); the third — a written T0 re-opening of S3-00 §2(b) — arises only under Option C of
§7. Neither is assumed, and the first (U1 PASS with a v4 lattice certificate) is not met either.
**Revision 2 (same day):** amended after independent review; the changes are listed in §8.

---

## 0. The two questions

**Q1.** Ledger item 4 says the tadpole condition "is not posable until a threefold base B₃ is
specified". In the K3 × K3 setting of the sources below the base is P¹ × K3 and χ/24 = 24 is
printed. Does that count as "a specified base" **for this program**, or only for the K3 × K3
model itself?

**Q2.** Independently of Q1: is an exact-arithmetic, pre-registered, MATH-ONLY labelling exercise
authorised — "which of the binary forms in the published finite list occur as T_X = v^⊥ inside
T_n = U ⊕ ⟨2n⟩ (criterion: D a square mod 4n, plus an explicit vector)" — as a record, not a
gate, with no scoring?

The facts (§1–§4) are kept apart from the recommendation (§7).

## 1. Provenance of the idea and of the sources

The idea was the orchestrator's, written **from model memory, unfetched**. Step 0 of the skill
(verify artifacts first) was applied to it: all five sources were fetched from arxiv.org on
2026-09-21, hash-pinned in `docs/literature/MANIFEST.md` (addendum of this date; the PDFs are
git-ignored by `docs/literature/.gitignore`, the `.txt` extractions are not), and the relevant
sections READ. The MANIFEST records which parts were read and which were not. Line numbers below
are lines of the `pdftotext -layout` extraction (`docs/literature/<name>.txt`); the PDF is
authoritative. A–K p.7 eq. (25) and p.8 Table 1 were also read as page images, because the text
layer scrambles them.

| tag | source | read |
|---|---|---|
| A–K | Aspinwall–Kallosh, arXiv:hep-th/0506014v1 | §1–§3.2 (all of the mathematics of the list) |
| BKW | Braun–Kimura–Watari, arXiv:1401.5908v1 | in part: §1, §2.1–2.2, one passage of §4.1.1, §5.1–5.2. Table 2 (p.10): **text layer only, not cross-checked against the page image, not transcribed**. Most of §3–§4 not read |
| BHLV | Braun–Hebecker–Lüdeling–Valandro, arXiv:0811.2416v2 | in part: abstract, §1, eqs. (2.5)–(2.6), (4.1), (4.17)–(4.19) |
| DRS | Dasgupta–Rajesh–Sethi, arXiv:hep-th/9908088v3 | in part: eq. (1.2), eqs. (2.6)–(2.10), §3.1 through eq. (3.9) (rev. 2: the T⁴/ℤ₄ example, p.12–13, was missed in rev. 1), §3.3 T⁶/Γ paragraph |
| Moore | Moore, arXiv:hep-th/9807087v3 | in part: §4.2, Thm 4.3.2 |

`checkers/check_literature_provenance.py` was run after the MANIFEST addendum: VERDICT PASS. It
reads `refs/literature_provenance.txt`, not the MANIFEST, so **the five new PDFs are outside its
scope**; its PASS says only that nothing previously pinned was disturbed.

Side effect to know about: **two** certificates record the sha256 of `MANIFEST.md` among their
inputs — `data/certificates/CM_POINTS_RHO20.json` and `data/certificates/A2_MEMBERSHIP.json` (the
second because `check_A2_membership.input_hashes()` starts from `CM.input_hashes()`; rev. 1 of
this brief named only the first, the reviewer found the second by `grep -rl 701ad5dd`). The
addendum changes `MANIFEST.md`, so the value both record (`701ad5dd…c667a6`, written into the
addendum itself) is now the pre-addendum hash, and the rev. 2 edit of the addendum moves the
current hash once more. No checker or control compares these recorded values (grep of
`checkers/`, `scripts/`), so nothing turns red; the next re-emission of either certificate will
record the then-current value. **The owners of both certificates should be told**; this task
may not touch either file.

## 2. What the sources say, verbatim

### 2.1 The tadpole condition

- A–K eq. (2), p.2 (l.110–112): "A consistent theory must contain M2-branes and/or nonzero G-flux
  in this background satisfying [21]  n_M2 + ½G² = 24."
- BKW eq. (17), p.7 (l.375–383): "The M2/D3-brane tadpole cancellation is equivalent to
  ½∫_Y (G ∧ G) + N_M2/D3 = χ(Y)/24 = 24, where N_M2/D3 is the number of M2/D3-branes minus
  anti-M2/D3-branes".
- BHLV p.7 (l.279–288; rev. 1 wrongly said p.9): "where χ is the Euler number of the compact manifold. For K3 × K3, it is
  χ = 24² = 576." and eq. (2.6): "In the absence of spacetime-filling M2 branes … requires
  (1/2ℓ_M⁶) ∫ G₄ ∧ G₄ = χ/24."
- DRS eq. (1.2) (l.72–77): "χ/24 = (1/8π²) ∫ G ∧ G + n"; §3.1 (l.496–501): "The anomaly
  χ/24 = 24 which must be cancelled by a combination of branes and G-flux."

### 2.2 The assumptions under which a finite list is obtained (A–K)

- Flux type (p.2, l.113–115): "The supergravity analysis of [4] showed that G must be primitive
  and of type (2,2) in order that any supersymmetry be preserved."
- Branes and smoothness (p.3, l.144–145): "By assuming, from now on, that n_M2 = 0 and that our
  K3 surfaces are smooth, we will restrict attention to only the first kind of modulus".
- Ansatz (p.4, l.185): "For now, let us assume that G is purely of type G₁, i.e., G₀ = 0",
  with G₁ = Re(γ Ω₁ ∧ Ω₂) (eq. (4)) and G₁ ≠ 0 (p.4, l.181–182).
- Theorem 2 (p.5): "The K3 surfaces S₁ and S₂ whose complex structures are fixed by G are forced
  to both be attractive." Definition, same page: "The surface S_j is said to be attractive if
  ρ(S_j) = 20, the maximal value."
- Theorem 3 (p.6): "A pair of attractive K3 surfaces S₁ and S₂ will correspond to a choice of
  integral G-flux if and only if det(Q₁Q₂) is a perfect square."

### 2.3 What exactly is bounded

Not |D| as such, and not by the tadpole equation read as an equation between integers. A–K
eq. (25), p.7 (page image): **½G² = |γ|² det(Q₁Q₂) / (q₁² q₂²) = 24**, where Q_j is the Gram
matrix (2a b; b 2c) of the transcendental lattice, q_j one of its basis vectors, and γ a complex
number constrained by integrality of eq. (22). The finiteness argument (eqs. (26)–(31)) is: take
reduced representatives |b| ≤ |c| ≤ |a| (their Theorem 4), so det Q₁ ≥ 3ac and det Q₂ ≥ 3df;
then ½G² ≥ (9/4)|γ|² ad when Re γ ≠ 0 (|γ|² ≥ 1 there), and ½G² ≥ 3dc in the purely imaginary
case. Conclusion, p.7: "there are only a finite number of possibilities for a, b, c, d, e, f, and
thus only a finite number of attractive K3 surfaces whenever G² is bounded."

So the bounded objects are the **six entries of the two reduced forms jointly**, through a
quantity that also contains γ and q_j². A bound on each determinant follows (bounded reduced
entries), but no inequality of the shape "|D₁| ≤ c" or "|D₁D₂| ≤ c" is printed in the parts read.

### 2.4 Is the list given? Yes, for one case

A–K p.7–8: "For ½G² = 24, i.e., G₀ = 0, there are 13 possibilities up to SL(2, ℤ) equivalence
which we list in table 1." Table 1 (p.8), read from the page image, in the paper's matrix
notation (2a b; b 2c), with its "O?" column (✓ = an orientifold reading exists, §2.3 of A–K):

| Q₁ | Q₂ | γ | O? |   | Q₁ | Q₂ | γ | O? |
|---|---|---|---|---|---|---|---|---|
| (4 0; 0 2) | (4 0; 0 2) | 1 + i/√2 | ✗ |   | (4 2; 2 4) | (2 1; 1 2) | 2 + 2i/√3 | ✓ |
| (4 2; 2 4) | (6 0; 0 2) | 1 + i/√3 | ✓ |   | (6 0; 0 4) | (6 0; 0 4) | 2i/√6 | ✗ |
| (6 0; 0 6) | (2 0; 0 2) | 1 + i | ✗ |   | (6 0; 0 6) | (4 0; 0 4) | 1 | ✓ |
| (8 4; 4 8) | (4 2; 2 4) | 1 + i/√3 | ✓ |   | (12 0; 0 2) | (12 0; 0 2) | i/√6 | ✗ |
| (12 0; 0 4) | (2 1; 1 2) | 1 + i/√3 | ✓ |   | (12 0; 0 4) | (6 0; 0 2) | i/√3 | ✓ |
| (12 0; 0 6) | (4 0; 0 2) | i/√2 | ✗ |   | (12 0; 0 12) | (2 0; 0 2) | 1 | ✓ |
| (16 8; 8 16) | (2 1; 1 2) | 1 + i/√3 | ✓ |   |   |   |   |   |

Transcription control (trivial arithmetic, appendix A; a scratch script, **not** a checker, no
certificate): the 13 pairs above agree as a multiset with BKW's independent reproduction of the
table in [a b c] notation (BKW Table 1, text layer); Theorem 3 holds on all 13 rows; the ✓ column
has 8 entries and coincides with BKW's rule (l.619) "all of a, b and c … are even" for one of the
two forms; a deliberately corrupted entry makes the cross-check fail. The determinants that occur
are 3, 4, 8, 12, 16, 24, 36, 48, 72, 144, 192 (copied from the script output).

A–K add (p.8): "In principle, a given pair of attractive K3 surfaces might admit many, but
finitely many, inequivalent choices of G. In our case, where the numbers are quite small, this
never happens." and "One may, of course, obtain other possibilities by considering a nonzero G₀.
In this case, we solve the same problem for ½G² < 24."

### 2.4a One ρ = 20 example in DRS (missed in rev. 1)

DRS do not use the word "attractive", but §3.1, p.12–13 (l.553–589) builds one such surface and
puts a flux on it:

- l.559–566: "Under this ℤ₄ quotient action, there are no untwisted (1,1) forms. The resulting K3
  has Picard number 20 [21]. … The intersection matrix for these transcendental integral classes
  is given by [21] (2 0; 0 2)." Their ref. [21] is Shioda–Inose.
- eq. (3.8), l.572–576: "Let us take both K3₁ and K3₂ to be T⁴/ℤ₄ orbifolds. Then the (2,2) form
  {γ₁ ∧ γ̄₂ + γ̄₁ ∧ γ₂} defined on K3₁ × K3₂ is primitive and integral." This is a flux of the
  shape A–K call G₁.
- eq. (3.9), l.584–589: "We can then cancel the anomaly completely with the following G-flux:
  G/2π = λ₁ ∧ λ₂ + γ₁ ∧ γ̄₂ + γ̄₁ ∧ γ₂. Note that this choice of G-flux does not preserve the full
  N=4 supersymmetry. … Therefore, only N=2 supersymmetry survives." Here λ is "a primitive (1,1)
  class with self-intersection −4", so the λ₁ ∧ λ₂ term is of the shape A–K call G₀.

What the page shows, without any computation: the form (2 0; 0 2) occurs in A–K Table 1 as Q₂ of
two rows (partners (6 0; 0 6) and (12 0; 0 12)), but the DRS **pair** (2 0; 0 2) × (2 0; 0 2) is
not among the 13. That is consistent with A–K's own remark quoted above — the DRS solution has a
nonzero G₀-type term, outside the G₀ = 0 case the table covers — and is an early instance of the
§2.5 point. DRS give one example, no list, and no finiteness statement.

### 2.5 How the list changes when the assumptions are relaxed (BKW)

The three numbers below (13, 66, 313) are answers to **three differently posed problems**, not
successive relaxations of one; the assumptions of each are listed with it.

- N_M2 ≥ 0 instead of = 0, still G₀ = 0 (§2.2, eq. (28), "½[G₁]·[G₁] ≤ 24"): "Out of the 66
  entries in Table 2, some pairs of K3 surfaces appear more than once." (l.497). Same assumptions
  as A–K otherwise. Table 2 (p.10, l.530–561) was looked at in the text layer only, which is
  visibly scrambled in its γ column; it was **not** transcribed or cross-checked against the page
  image. What the text layer shows (reviewer's observation, confirmed by reading the lines): it
  contains forms absent from the 13-pair list, among them [2 1 1] × [2 1 1] at flux 7 (and, with the
  representative [2 −1 1] in the be < 0 part of the table, again at flux 7 and at flux 14), [4 2 2] at flux 14 and [6 3 3] × [2 1 1] at flux 21. In the paper's convention
  (2a b; b 2c) these have determinants 7, 28 and 63 (appendix B, trivial arithmetic). No
  intersection with any family of this repo was performed or scored; the point is only that the
  choice between the 13-pair and the 66-entry list changes which small determinants appear at
  all — see §6, "Forking paths".
- G₀ ≠ 0 (§5.1.2, l.2186–2193): "each one of them does not have to be integral by itself; only
  the total flux … needs to be integral … the condition (24) is too restrictive. … This means that
  the search for pairs of attractive K3 surface in Sections 2.1 and 2.2 needs to be carried out
  once again for cases with G₀ ≠ 0."
- Their scan (§5.2, p.45, titled "A Landscape of Vacua with a Rank-16 7-brane Gauge Group").
  Its assumptions, all from l.2425–2449 and l.2488–2492 (rev. 1 listed only the last one):
  (a) case (i) only — l.2434–2435: "we restrict our attention only to the cases i)", i.e. G₁ ≠ 0,
  D = 2; (b) a fixed Kähler form — l.2438–2440: "We provide the following presentation for a
  fixed choice of J_S (rather than scanning over all possible J_S)", eq. (122); (c) a fixed
  frame — l.2448–2449: "Assuming that W_unbroken = E₈ ⊕ E₈ (or D₁₆; ℤ₂⟨sp⟩), we scan all possible
  pairs of attractive K3 surfaces of the form X[a 0 c] × X[a′ 0 c′]"; (d) the tadpole is an
  inequality filled by branes — l.2492: "the remaining D3-brane charge is supplied by placing an
  appropriate number of D3-branes"; (e) diagonal forms [a 0 c] only, 0 < c ≤ a ≤ 50 (l.2488:
  "an artefact of cutting the scan at a, a′ ≤ 50"). Result (l.2493–2497): "we found
  that there are 313 different choices of X × S admitting the flux satisfying all the three
  conditions above. … If both G₁ and G₀ were required to be integral, there would only be 28
  different choices, and the largest possible value of a would be 6." The scan is bounded by
  construction; no finiteness statement for G₀ ≠ 0 was found in the parts read.
- An infinite series (§5.2, l.2576–2580): "for a series of infinite pairs of attractive K3
  surfaces X × S = X[k 0 k] × X[k 0 k] (where k = 1, 2 ···, ∞). Under this choice of the flux, a
  one parameter (k) deformation of the complex structure … remains a flat direction, and all the
  ρ_X = ρ_S = 20 points X[k 0 k] × X[k 0 k] just sit in this flat direction." BKW remove these
  from their ensemble because a modulus is left unfixed, not because the tadpole excludes them.

### 2.6 The base

- A–K §2.3, p.8–9 (l.434–437): "Assume that S₂ is an elliptic K3 surface with a section. Let
  π : S₂ → B denote this elliptic fibration of S₂. By shrinking the area of the elliptic fibre,
  one moves to an F-theory fibration corresponding to a type IIB compactification on S₁ × B."
  and p.10 (l.492–493): "any attractive K3 surface is elliptic with a section [23] so our condition for an
  F-theory limit is automatically satisfied."
- BKW §4.1.1 (l.1149–1150): "In the case of π_Y : Y = K3 × K3 → P¹ × K3, the rank is
  44 − 23 − 1 = 20."
- BKW §1, p.3 (l.165–168): "This compactification cannot be considered realistic enough for an
  immediate use in particle physics (e.g. there are no matter curves), but a sufficient complexity
  is involved in this toy model of landscape".

### 2.7 Density, and the classification of attractive K3 surfaces

- Moore §4.2 (l.1410–1411): "Attractive K3 surfaces are 'maximally algebraic' and form a dense set
  in the moduli space of algebraic K3's."
- Moore Thm 4.3.2 (l.1510–1511), attributed to his ref. [70]: "There is a 1-1 correspondence
  between attractive K3 surfaces and PSL(2, ℤ) equivalence classes of positive even binary
  quadratic forms." A–K p.6 cite the same classification from their ref. [23].
- Moore's paper contains no occurrence of the word "tadpole" (grep of the text layer). It is a
  source for the classification and for density, not for any flux bound.

### 2.8 One-parameter lattice-polarized families

None of the parts read mentions a lattice-polarized family, a modular curve X₀(n)+, or a
restriction of the search to a subfamily. The setting throughout is the full moduli space of each
factor: A–K eq. (5) (the Grassmannian of 4-planes in Γ₄,ₙ ⊗ ℝ); BKW p.5 (l.276–278): "The loci
satisfying these conditions have complex codimension 40 in the moduli space M_cpx(S₁) × M_cpx(S₂),
and hence are isolated points." Any statement about the cooper_s7 / cooper_s10 families would be
**ours**, obtained by intersecting a published list of isolated forms with the forms v^⊥ ⊂ T_n;
no source makes it. Three further points from the text bear on that intersection:

1. The list is a list of **pairs**. Theorem 3 ties the two factors (same imaginary quadratic
   field); a family of this repo could supply at most one factor, and nothing in the program
   specifies the other.
2. A–K assume smooth K3 surfaces. `briefs/STREAM2_CM_POINTS_RHO20_2026_09_21.md` §4 records that
   the (−2)-vector rows and the point z = ∞ of cooper_s7 are singular points of the operator where
   the explicit projective model has not been examined; what is singular there is the differential
   operator L₃ (and, at the (−2)-vector rows, possibly the polarized surface, which acquires at
   worst a node only on the pseudo-ample reading — not examined). No fibre classification of any
   kind is made or implied (ledger item 3).
3. The criterion "D is a square mod 4n" of `briefs/STREAM2_A2_MEMBERSHIP_2026_09_21.md` decides
   which **discriminants** occur; the published list is a list of **form classes**. The A2 brief
   states that its per-D class lists are not claimed complete. An honest intersection needs an
   explicit vector per class, as the A2 checker does for one class.

## 3. The orchestrator's hand estimate, scored against the text

| # | clause (from memory, unverified when issued) | outcome |
|---|---|---|
| 1a | the ρ = 20 condition alone selects nothing, because such points are dense | **confirmed** as a statement about the moduli space of algebraic K3 surfaces (Moore §4.2). For the two families it is the CM-points brief's observation, not the source's |
| 1b | "what selects is a bound on \|D\|" | **imprecise**: the printed bound is on ½G² as in eq. (25) and yields bounds on the six reduced entries; bounded determinants follow, but no bound on \|D\| is printed (§2.3) |
| 2a | A–K: the flux solutions are pairs of attractive K3 surfaces | **confirmed** (Thm 2), for G₁ ≠ 0 |
| 2b | the tadpole χ/24 = 24 "bounds the data, giving a finite list" | **confirmed only under stated assumptions**: G primitive of type (2,2), G₀ = 0, n_M2 = 0, smooth surfaces → 13 pairs, listed. The tadpole does not do this alone: the argument uses the positive expression (24)–(25), see §4. With N_M2 ≥ 0: 66 entries (BKW). With G₀ ≠ 0: 313 in a scan that is bounded by construction and carries further assumptions of its own (rank-16 frame, fixed J_S, case (i), diagonal forms; §2.5), and an infinite series with a flat direction (BKW §5.2). These are three different problems, not one problem relaxed twice |
| 2c | DRS, BHLV/BKW, Moore are "related" sources for this | **mixed**: BKW and BHLV refer to the A–K list directly (BHLV reproduces one pair, (4.19), and says its own results "are more general since we do not restrict ourselves to attractive K3 surfaces"); DRS gives the tadpole and G = ∗G, and **one** ρ = 20 example (T⁴/ℤ₄, transcendental form (2 0; 0 2)) with a flux whose (2,0)×(0,2) part is of G₁ shape and whose anomaly-cancelling completion (3.9) has a G₀-type term (§2.4a) — one example, no list, no finiteness statement (rev. 1 said "no attractive surfaces"; that was wrong for the paper as a whole); Moore gives classification and density and has no tadpole |
| 3a | F-theory on K3 × K3 has base K3 × P¹ | **confirmed** (A–K §2.3; BKW l.1149–1150) |
| 3b | "so the tadpole would be posable there, unlike the program's current situation" | the first half is **confirmed** (χ = 576 printed by BHLV); whether that changes the program's situation is Q1 and is not something a source can settle. See §5 |

## 4. The tension with LeanMaster Stream 9, and how far it reconciles

Read as source, no Lean build run: `SocrateAI-Scientific-Agora-LeanMaster/docs/STREAM9_ORIENTIFOLD.md`
at commit `b8f8a27` (last commit touching the file).

- S9.5, l.120–134: "for every value of the flux contribution there are **infinitely many** flux
  vectors realising it: the tadpole bounds the integer ½N_flux, never the quanta. A finiteness
  statement about flux vacua therefore has to come from the supersymmetry/imaginary-self-duality
  conditions and from quotienting by the duality group — never from the budget alone. Any count
  citing only a tadpole is counting the wrong set."
- S9.6b, l.199–223: "it comes from positivity", with the explicit disclaimer (l.225) that the
  positive form there is not shown to be the physical flux norm.

Stream 9's setting is T⁶/Γ with 3-form flux; the sources here are K3 × K3 with 4-form flux. They
are different models, and nothing below transfers a theorem from one to the other. With that
said, **the K3 × K3 sources do not contradict S9.5; they are an instance of it.** In each of them
finiteness (or restrictiveness) is obtained from the tadpole **together with** a positivity
statement that comes from the supersymmetry condition, and up to a duality quotient:

- DRS eqs. (2.8), (2.10) (l.205–214): "the conditions (2.3) imply that, G = ∗G" and "the
  self-dual G-field is primitive: J ∧ G = 0." For a self-dual form ∫ G ∧ G = ∫ G ∧ ∗G, a norm.
- A–K eq. (24), p.6: "G² = ½|γ|² ∫Ω₁ ∧ Ω̄₁ ∫Ω₂ ∧ Ω̄₂" — a product of positive quantities — and the
  finiteness proof then uses det Q ≥ 3ac, i.e. positive definiteness of the transcendental
  lattices. The flux G₁ lives in T_{S₁} ⊗ T_{S₂}, a positive definite lattice of rank 4.
- BKW §5.1.1 (l.2142–2144): the G₀ flux "always gives rise to a positive contribution —
  1/2[G₀]·[G₀] — to the D3-tadpole, since both W_frame and [J_S^⊥ ⊂ S_S ⊗ ℝ] are negative definite."
- BHLV §4 (l.906–909): "tr G^a G = 48. Of course, we also require that the flux gives Minkowski
  minima, i.e. G^a G needs to have only non-negative eigenvalues. These conditions turn out to be
  rather restrictive".
- Duality quotient: A–K count "up to SL(2, ℤ) equivalence"; BKW devote §3 to when two elliptic
  fibrations count as the same.

**Our remark, not from a source and not checked by any script here:** on the full lattice
H²(S₁, ℤ) ⊗ H²(S₂, ℤ), whose form is indefinite, the equation ½G² = 24 alone would bound nothing
(the solution set of such an equation on an indefinite lattice is in general infinite), which is the same phenomenon S9.5 describes in its own setting. **Residual tension, stated:** (i) the orchestrator's
phrase "the tadpole bounds the data" is the wording S9.5 warns against and is corrected by row 2b
above; (ii) BKW's infinite series X[k 0 k] × X[k 0 k] shows that even with the supersymmetry
conditions imposed, finiteness of the set of *surfaces* is lost once G₀ ≠ 0 is allowed and
flat directions are not excluded — so "the published finite list" means "the list under
G₀ = 0", not a model-independent fact; (iii) this reconciliation is a reading of prose in five
papers and one doc file, at Tier L; none of it is machine-checked here or in LeanMaster.

## 5. One structural observation relevant to Q1 (a reading, flagged as ours)

In A–K §2.3 the elliptic fibration is that of the single surface S₂ over B ≅ P¹, and S₁ is a
product factor. The parameter z of a cooper family does not appear as a coordinate on the base:
K3 × K3 uses **one member** of a family (an isolated attractive point), it does not realise the
family as a fibration over a threefold. Ledger item 6 names Twisted-Weierstrass, with its gate on
P³, as the PRIMARY route; K3 × P¹ is not a base of that construction. So a "yes" to Q1 would not
supply the missing B₃ of the existing route — it would adopt a second, different compactification,
the one BKW themselves call a "toy model". LeanMaster's Stream 9 doc makes the parallel remark
about its own move (§2, "a change of compactification, not a continuation").

## 6. What an authorised labelling exercise would and would not give

Would give (if Q2 = yes): a table, exact integer arithmetic, of which form classes from a
pre-registered published list occur as v^⊥ ⊂ U ⊕ ⟨2n⟩ for n = 7 and (ADVISORY, lattice certificate
DRAFT) n = 10, each with an explicit primitive vector, and with the clause that fired for each
absence. Tier B at best; a record, not a gate.

Would **not** give: any observable; any value of m_φ, α_D, Λ_D or of a₁, a₂, a₃ (ledger item 4);
any dark-energy or vacuum-energy statement (T0 decision D4 / A-DE stays untouched); any coupling
between the geometry and a physical sector (VISION §1.3: a lattice coincidence is not a physical
mechanism); any adoption of the ρ = 20 cut or of T3; any ranking of a candidate or of a member of
a family; any statement that a flux solution exists on a surface of this program — the list is
one of pairs, and the partner surface is unspecified.

Known before running anything, and part of why the exercise is weak evidence at best:

- **Base rate.** Both sets are concentrated at small |D|. A reader of §2.4 and of the A2 brief
  can see without computing that the class (2 1; 1 2) of determinant 3 is in Table 1 and is on
  record for n = 7. That is not scored here and is not a finding; it illustrates that overlaps
  are expected a priori. A run without a **real** negative control — the same intersection at
  several other levels n′, reporting how often a "hit" occurs — would be a test that cannot fail
  (standing rule 1).
- **Forking paths.** The 13-pair list, the 66-entry list and the G₀ ≠ 0 scan give different
  answers, and they answer differently posed problems (§2.5). The fork is not harmless for the
  levels of this repo: the text layer of BKW Table 2 shows determinant-7 forms that the 13-pair
  list lacks (§2.5), so the list choice alone decides whether small determinants tied to n = 7
  beyond the determinant-3 class appear at all. The base-rate illustration above is therefore
  one-sided: it shows the one overlap visible in Table 1 and says nothing about Table 2. The list, the role (S₁ or S₂), the treatment of the ✓/✗ column and of the singular
  rows must be fixed in writing before the run (PREDICTION-protocol discipline, ledger item 5),
  or the outcome is a FIT.
- **Transcription.** BKW Table 2 would have to be read as page images and cross-checked, as was
  done here for Table 1.

## 7. Options for T0, then a recommendation

| option | what it means | consequences |
|---|---|---|
| **A. Park** | Q1 = no, Q2 = no. This brief stays as the record of what the sources say | Zero risk to the ledger. The corrected statement of the idea (§3, §4) is preserved. No new table |
| **B. Math-only labelling, ledger unchanged** | Q1 = "specified for the K3 × K3 model only; ledger item 4 unchanged, F5b stands". Q2 = yes, under a pre-registration note fixing list, role, controls; output labelled record / lattice coincidence; s10 ADVISORY | One more exact table with controls. Main risk is narrative drift: a coincidence table sitting next to the word "flux". Mitigation: the not-claimed block of §6 copied into the certificate; base-rate control mandatory; no mention in any status table |
| **C. Treat K3 × P¹ as the program's B₃** | Q1 = yes; re-open S3-00 §2(b) on K3 × K3 | Changes the compactification (§5), sits beside the PRIMARY Twisted-Weierstrass route, and would need preconditions 1 and 3 of `unblock-tier-c` Step 3 ruled on as well. Even then every output would remain Tier C conjecture until a worked matching exists. Not something Stream 2 can assess alone |
| **D. Refer to T0s first** | ask Deep Think whether K3 × K3 is relevant to the dual-scale proposal at all, before any labelling | Costs a round trip; two earlier Deep Think briefs are still unanswered |

**Recommendation (opinion, separate from the facts above).** Q1: **no** — K3 × P¹ is a specified
base of a different model, and saying otherwise would quietly replace the construction the ledger
is about. Q2: **A by default; B only if T0 wants the table**, and then only with the pre-registered
list choice and the other-levels base-rate control. The reason for leaning to A is §2.5: the
"finite list" is finite because of G₀ = 0; differently posed versions of the problem return 13,
66 and 313 (the last under its own frame, Kähler-form and scan-range assumptions, so the three
are not like-for-like); DRS already exhibit a solution outside the 13; and BKW exhibit an
infinite series with a flat direction. Membership in any one of these lists therefore carries
little information even as pure mathematics, and which list is used changes the answer at the
small determinants that matter for n = 7. Option C is not recommended. The useful output of this task
is already in hand: the idea as issued is corrected in two places (what is bounded; what does the
bounding), and the apparent conflict with Stream 9 is an agreement.

---

## Appendix A — transcription cross-check (scratch; trivial arithmetic; not a checker)

```python
from math import isqrt
AK = [((4,0,2),(4,0,2),0),((4,2,4),(6,0,2),1),((6,0,6),(2,0,2),0),((8,4,8),(4,2,4),1),
 ((12,0,4),(2,1,2),1),((12,0,6),(4,0,2),0),((16,8,16),(2,1,2),1),((4,2,4),(2,1,2),1),
 ((6,0,4),(6,0,4),0),((6,0,6),(4,0,4),1),((12,0,2),(12,0,2),0),((12,0,4),(6,0,2),1),
 ((12,0,12),(2,0,2),1)]                      # A-K Table 1, page image: (2a, b, 2c), O? column
BKW = [((8,8,8),(1,1,1)),((6,0,6),(1,0,1)),((6,0,3),(2,0,1)),((6,0,2),(3,0,1)),((6,0,2),(1,1,1)),
 ((6,0,1),(6,0,1)),((4,4,4),(2,2,2)),((3,0,3),(2,0,2)),((3,0,3),(1,0,1)),((3,0,2),(3,0,2)),
 ((3,0,1),(2,2,2)),((2,2,2),(1,1,1)),((2,0,1),(2,0,1))]      # BKW Table 1, text layer: [a b c]
abc = lambda m: (max(m[0],m[2])//2, m[1], min(m[0],m[2])//2)
det = lambda m: m[0]*m[2]-m[1]**2
key = lambda rows: sorted(tuple(sorted(p, reverse=True)) for p in rows)
print(key([(abc(p),abc(q)) for p,q,_ in AK]) == key(BKW))                       # True
print(all(isqrt(det(p)*det(q))**2 == det(p)*det(q) for p,q,_ in AK))            # True
print([any(all(x%2==0 for x in abc(m)) for m in (p,q)) for p,q,_ in AK] == [bool(o) for *_,o in AK])  # True
print(sorted({det(m) for p,q,_ in AK for m in (p,q)}))
AK[0] = ((4,0,4),(4,0,2),0); print(key([(abc(p),abc(q)) for p,q,_ in AK]) == key(BKW))  # False (control)
```

Output of the run on 2026-09-21: `True`, `True`, `True`,
`[3, 4, 8, 12, 16, 24, 36, 48, 72, 144, 192]`, `False`.

## Appendix B — determinants of the BKW Table 2 forms named in §2.5 (scratch; trivial arithmetic)

```python
for a, b, c in [(2,1,1), (4,2,2), (6,3,3)]:      # BKW [a b c]  <->  matrix (2a b; b 2c)
    print((a, b, c), 4*a*c - b*b)
```

Output of the run on 2026-09-21: `(2, 1, 1) 7`, `(4, 2, 2) 28`, `(6, 3, 3) 63`.

On appendix A: its only negative control is a tamper. That is accepted here because the appendix
is a transcription cross-check that emits no certificate and no headline; it is not a checker and
must not be reused as one. The reviewer additionally checked A–K eq. (25) in exact fractions on
all 13 rows with the transcribed γ (reported as holding, each with one choice of q²); that script
is the reviewer's and was not re-run here.

## 8. Changes in revision 2 (after independent review, 2026-09-21)

| # | reviewer finding | action |
|---|---|---|
| 1 | DRS §3.1 contains a Picard-number-20 K3 with form (2 0; 0 2) and a flux; rev. 1 said "no attractive surfaces" | **accepted**, checked at DRS l.553–589 / p.12–13; new §2.4a, row 2c rescored, read-scope rows corrected |
| 2 | assumptions of the 313 scan under-reported; "13 → 66 → 313" not like-for-like | **accepted**, checked at BKW l.2425–2449, l.2488–2497; §2.5, row 2b and §7 reworded |
| 3 | BHLV χ = 576 and eq. (2.6) are on p.7, not p.9 | **accepted**, checked by per-page extraction |
| 4 | `A2_MEMBERSHIP.json` also records the pre-addendum MANIFEST hash | **accepted**, checked by grep; §1 rewritten; owners to be told |
| 5 | header named precondition 3 where Q1 is precondition 2 | fixed |
| 6 | BKW Table 2 text layer shows determinant-7 forms absent from the 13 | **accepted** as a text-layer observation only; §2.5, §6; no intersection performed |
| 7 | unsourced remark in §4 | now labelled as ours |
| 8 | appendix A control is tamper-only | kept, with the limitation stated in appendix B |
| 9 | the five PDFs are outside `refs/literature_provenance.txt` | unchanged (that file is not this task's to edit); stated in §1. **For the owner of `refs/`.** |

No conclusion of rev. 1 is reversed. Nothing was executed in either revision.

---

Generated-by: Claude (Fable 5.1), Stream 2, task B4 | Verified-by: sources fetched and read this session (sha256 in docs/literature/MANIFEST.md addendum 2026-09-21); Table 1 cross-checked between two independent transcriptions with a failing control; independent reviewer pass (verdict CONFIRMED_WITH_FIXES_NEEDED, all four should-fix items addressed in rev. 2, §8); scripts/check_tier_language.py | Reviewed-by: N
