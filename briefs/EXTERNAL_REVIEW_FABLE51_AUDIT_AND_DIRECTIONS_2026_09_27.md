# External review "K3 Selection Review" (Fable 5.1, 2026-09-21) — recorded, audited, directions

**Date:** 2026-09-27 · **From:** Stream 2 · **To:** T0 (Xavier); Stream 1, Stream 3, LeanMaster (each
gets a delivery note citing this brief) · **Authority:** T0 asked in session (2026-09-27) to read the
review, record it, review it, and authorised Stream 2 to "take directions to unblock Stream 1, Stream 2
and Stream 3". What was executed, what is proposed, and what was declined are separated below.

## 1. What the review is, and what it reviews

- Recorded verbatim: `docs/literature/external_reviews/FABLE51_K3_SELECTION_REVIEW_2026_09_21.md`,
  sha256 `6ab674536a5bb1e50bdc9df3b6f3445e7ba0e34e3d78df141503ce18030233a9`, row added to
  `docs/literature/MANIFEST.md` (addendum 2026-09-27). Read in full.
- **The "specification" it reviews is `~/K3spec.md`** (untracked, home directory; title "Physical
  Justification and Geometric Specification of the K3×T² Manifold under Mathieu Moonshine M₂₄"). That
  document was **already REJECTED by T0 on 2026-09-16** as a K3-selection input
  (`docs/K3xT2_M24_MOONSHINE_CLAIMS_REGISTER_2026_09_16.md` §7, commit `aaf828b`: fabricated OEIS
  citations, 16-not-24 Kummer nodes, impossible M₂₄→A₄ quotient). The review reaches the same verdict
  by a longer route and adds the Λ arithmetic (98 orders), the A₄ branching, the non-homogeneous quartic
  and the Papers 10–12 conflicts. Its §"Edits required in the spec" therefore applies to a document this
  program has no plans to use; it is kept as record only.
- The review's own caveat: "literature identifiers below are from memory and should be pinned before
  citation". None of them is pinned here by this brief.

## 2. Audit — clause by clause, against certificates

`checkers/check_external_review_fable_2026_09_21.py` → `data/certificates/EXTERNAL_REVIEW_FABLE_2026_09_21_AUDIT.json`;
controls `checkers/test_external_review_fable_controls.py` (22, each clause shown able to go
NOT_CONFIRMED; exact helpers reject wrong class numbers and wrong groups). **All 12 scored clauses
CONFIRMED**:

| # | review clause (Stream-2 scope) | source of confirmation |
|---|---|---|
| F1–F2 | s7 loci {0, 1/27, −1, ∞}; s10 loci {0, −1/4, 1/16, ∞} | leading symbol `1 − 2az + cz²` from register params, exact |
| F3–F4 | L₃ Riemann schemes; L₂ exponents at ∞ {⅓,⅔} / {⅜,⅝} via {2α, α+β, 2β} | `L3_RIEMANN_SCHEME.json` + exact |
| F5–F6 | stabiliser orders (2,2,3)/(2,2,4); Gauss–Bonnet matches Γ₀(7)+ (index 8, halved) and Γ₀(10)* (index 18, quartered), and **not** Γ₀(10)+10 | `ELLIPTIC_POINTS_ARE_CM.json` + exact Fractions |
| F7–F8 | W₇ has two fixed points: τ=i/√7 → v=(1,−1,0), T=⟨2⟩⊕⟨14⟩, D=−28; the other → v=±(−2,4,1), T=[[2,1],[1,4]], D=−7; count = h(−28)+h(−7) = 2 | `CM_POINTS_RHO20.json` (z=1/27 and z=−1) + exact class numbers |
| F9 | W₁₀ Fricke point → ⟨2⟩⊕⟨20⟩, D=−40, h=2 | `CM_POINTS_RHO20.json` z=1/16 (s10 ADVISORY) |
| F10 | h(−3)=h(−4)=h(−7)=h(−8)=h(−28)=1, h(−40)=2, h(−23)=3 with forms (1,1,6),(2,±1,3) | exact enumeration |
| F11 | the review's **X₃ lattice A₂ (D=−3) is the z=∞ member of cooper_s7**; its **X₄ lattice ⟨2⟩⊕⟨2⟩ (D=−4) is the z=∞ member of cooper_s10** | `CM_POINTS_RHO20.json` locus_hits (lattice statement only; the naming of the surfaces is Shioda–Inose, Tier L, unpinned here) |
| F12 | L₃ = Sym²(L₂), L₂ exhibited, no condition on (a,b,c,d) | `C3b_symsqrt_*.json` |

The review's "prediction that upgrades a Tier B item" (two W₇ fixed points with those lattices) was
thus already on `main` as a computed certificate dated the same day; the review did not have it.

**Findings in band (not failures of the review):**
- **N1** — it repeats the rejected spec's labels "1/27 (conifold), −1 (Fricke)". Per the certificate the
  W₇ fixed point τ=i/√7 sits at **z = 1/27**, and the D=−7 point at z=−1. "Conifold" is a Kodaira-type
  reading, forbidden for this family by ledger item 3 (both are order-2 elliptic points, E-008/E-009).
- **N2** — its "h(−4N)+h(−N) fixed points" rule is scored at N=7 only; at N=10 the review itself names
  the full Atkin–Lehner group, where W₁₀ is one of three involutions.
- **N3** — its central methodological point ("a selector must be named before either ordering means
  anything") is the content of **D7′ read narrowly**: C6 lists members; no quantity to extremise among
  them has been adopted. See §4 for the proposed amendment.

**Not scored** (no artifact in this repo; listed in the certificate): Λ, M₂₄/A₄/GHV statements, Kummer,
quartic, r/n_s/δ_CP/21-cm/TDA rows, Papers 10–12 conflicts, the X₃/X₄ Weierstrass fibre tables, the
Hurwitz-order observation, experiments E1–E4, TDA proposals. The LeanMaster theorems the review cites
exist by name and location (`smallest_black_hole` AttractorCharges.lean:145, `tau_minimal` :174,
`discriminant_gap` :133, `smallest_black_hole_index` :201, `immortal_m1` Immortal.lean:86,
`ratio_fails_at_every_class` CharactersAll.lean:215, `literal_lock_fails_at_2A` ForgerTest.lean:72);
`dualLength_bogoliubov` lives in the external QuantumFluids repo. Their statements were read via the
LeanMaster index, not re-proved.

## 3. What the review changes for K3 selection, read against the ledger

1. **Convergence, Tier B, narrow.** Paper 12's attractor floor (T_S = A₂, `smallest_black_hole`) and the
   review's "second-smallest" X₄ (⟨2⟩⊕⟨2⟩) are both members of our register families — at z=∞ of s7 and
   of s10 respectively. The review derived them at N=1; our certificates place them at N=7 and N=10. Both
   can hold (a rank-20 surface lies in many one-parameter families). **No preference follows**: D7′ adopts
   no ranking, and "A₂ ∈ s7, A₂ ∉ s10" stays a lattice fact (`A2_MEMBERSHIP.json`).
2. **The selector gap is real and already ours.** The review lists three selectors that disagree
   (discriminant floor → A₂; lattice height → ⟨2⟩⊕⟨2⟩; Fricke point → two surfaces at N=7). That is why
   D7′ adopted a cut and not a choice. The improvement the review offers is to make the requirement
   explicit in `K3_CRITERIA.md` — proposal in §4.
3. **"Tier B item closed without Stream 2" — partly.** Matching the (2,2,3)/(2,2,4) signatures to Γ₀(7)+ /
   Γ₀(10)* by Gauss–Bonnet was recorded here on 2026-07-26 (`L3_RIEMANN_SCHEME.json`, lead1_bonus, [B])
   and the coordinate is pinned by the T1 Hauptmodul certificates. What stays Tier B is the identification
   of the monodromy-invariant lattice with T (Dolgachev §7 / Doran 5.13, read) and the numeric recognition
   of monodromy entries in `check_U1_lattice.py`. The review's own recommendation for that link —
   **certified ball-arithmetic continuation** — is the right tool: see WP-S2-CERT in §5.
4. **Arm V / Arm P / Arm 0 (the control design) is not posable here today.** It needs an observable
   evaluated at a CM point; ledger item 4 / F5b: no observable exists, and no member of C6 maps to one.
   The design is recorded as the pre-registration template for whenever one does (pin protocol, rule 5).
   The purely lattice version is vacuous — the rank jump is by construction.
5. **Kodaira, two different things.** The review's Inose–Weierstrass fibre tables (II*, II*, IV; II*, II*,
   I₂, I₂) are read from orders of vanishing of an explicit model — not from L₂/L₃ exponents — so they are
   not the E-007 category error. Nothing in this repo checks them; they are Lean targets for Stream 1 (§5).
6. **Nothing physical.** The review's "mirror-symmetry reading of W_N" (Dolgachev–Nikulin) is Tier L
   mathematics we already cite; its QHE / SIT / Aubry–André material is Tier C in its own words and outside
   this repo.

## 4. Proposed amendment AM-6 (§6 protocol) — **ADOPTED later the same day, T0 D9′** (`briefs/T0_DECISIONS_2026_09_27_STREAM2.md`; text below applied verbatim)

*Motivation.* The review's N3; D7′'s "widening needs its own T0 text"; three known selectors disagree.
*Exact diff* — add to **C6** after "**What C6 is NOT**":

> - **Selector clause (AM-6, proposed 2026-09-27).** C6 lists the candidate members of a family. Naming
>   one of them "the" K3 of the program requires a **named extremised quantity** — e.g. minimal |disc T|,
>   minimal lattice height of the algebraic class, the fixed point of a named involution — adopted by its
>   own T0 text, with the outputs of the other known selectors listed beside it. Known selectors disagree
>   on the register families (`EXTERNAL_REVIEW_FABLE_2026_09_21_AUDIT.json`, F7–F11): until one is
>   adopted, no member is preferred and nothing downstream may assume one.

and to **§7 Pre-Freeze Checklist**: "- [ ] Selector named (AM-6) or explicitly declined for v1.0."
*Impact statement:* no ranking run exists, so none is invalidated; no certificate value changes; the
Stream 1 / Stream 3 mirrors re-pin (they must anyway, PR #55).

## 5. Directions per stream

**Stream 2 (this repo) — executed:** record + manifest row; audit checker + controls; regression block
lines in `TODO.md`. **Proposed at first, then executed under T0 D9′ the same day**
(`briefs/T0_DECISIONS_2026_09_27_STREAM2.md`): AM-6 (§4) adopted; **WP-S2-CERT step 1 landed** —
`checkers/check_certified_monodromy_L2.py` redoes `check_U1_lattice.py` stage 2 (the order-2 operator
L₂, Frobenius basis at the MUM point, Sym²) in Arb ball arithmetic (`python-flint 0.9.0`, installed
under D9′-4) with rigorous truncation bounds: majorant induction on the θ-form recurrence for the
Frobenius tails, majorant induction on the local Taylor recurrence for each continuation step (step ≤
0.35 × the majorant radius, which is proved ≤ the distance to the nearest singular point), exact rational
centres. Result, both families: every Sym² entry the heuristic recognised is the **unique rational of
denominator ≤ 10⁴** inside its enclosure (s7 diameters 1.5e−96 and 1.0e−115; s10 4.2e−102 and
2.2e−115); det M = −1 enclosed; loops rigorously non-trivial; cusp loop encloses [[1,1],[0,1]] to
1e−116. Two engineering facts are recorded in the checker: Horner evaluation from the top passes through
wide balls and loses ~20 digits of radius accounting (forward summation is used), and the ball radii
inside the recurrence grow ~1.7× faster than the majorant ρ, so the step fraction is kept at 0.35 (a
looser step can only fail closed). What this does **not** do: the identification of the
monodromy-invariant lattice with T stays Tier B (framework sources), and s10 stays ADVISORY (lattice
certificate DRAFT, D6′). Certificates `CERTIFIED_MONODROMY_L2_cooper_s7.json` / `_s10.json`; controls
`checkers/test_certified_monodromy_L2_controls.py`. **Declined:** running Arm V/P/0 (no observable), any
ranking, any Kodaira label on the register loci.

**Stream 1 (LeanProposal) — delivery note `briefs/STREAM2_TO_STREAM1_FABLE_REVIEW_DIRECTIONS_2026_09_27.md`
in their repo:** (a) pin Doran 1998 Thm 5.13 as Tier L in their docs — our fetched copy is hash-pinned
(`docs/literature/MANIFEST.md`, `2a3ce065…`); (b) the rank-jump lemma the review calls "a nullspace, a
saturation and a binary-form reduction": in U⊕⟨2N⟩, v=(1,−1,0) has v²=−2 and v^⊥ ≅ ⟨2⟩⊕⟨2N⟩ — integer
linear algebra next to `TN_diagonalises` (MnLattice.lean:179), which would put F7/F9's lattices in the
kernel; (c) optional: Inose–Weierstrass invariants of X₃ and X₄ (orders of vanishing → fibre types →
Euler sum 24 → NS rank 20 → disc NS = −disc T) as finite computations, and the D₄/Hurwitz-order rank-2
free-module statement; (d) their README's "s₇ lattice Tier B pending Stream 2 numerical monodromy" can
cite `C2_cooper_s7_v5.json` (LIVE, T0 D5′) and `CM_POINTS_RHO20.json` — still Tier B; (e) the t103 flag
(E-014) is still unanswered — unchanged by this brief.

**Stream 3 (Home) — delivery note `briefs/STREAM2_TO_STREAM3_FABLE_REVIEW_DIRECTIONS_2026_09_27.md` in their
repo:** (a) the review's "observational element: none" agrees with WP-E5 CLOSED and A-DE; (b) its
laboratory programme (Aubry–André calibration arm; SIT noise duality; self-dual JJ/QPS circuit; Γ₀(2)
flow) is outside Stream 3's astrophysical scope and outside this repo's Tier A/B; if T0 wants it, it
enters only via a pre-registered PREDICTION v2 amendment under the pin protocol, with Arm V/P/0 and a
kill rule frozen by tag before any data; the Aubry–André self-duality check is an exactly solvable
script that can be built with negative controls without touching any K3 claim; (c) re-pin their
`K3_CRITERIA.md` mirror after PR #55; (d) the K3spec rows (Λ, 462/360, δ_CP, 4.038 GHz, TDA peak) stay
REJECTED (2026-09-16) — nothing to do.

**LeanMaster:** no action; the review's citations of Papers 10–12 resolve to existing declarations
(§2). Its "QHE critical point = N=2 Fricke point" is Tier C in the review's own words.

## 6. Asks for T0

1. Adopt, amend, or decline **AM-6** (§4).
2. Allow the `python-flint` install for **WP-S2-CERT**, or decline it.
3. Confirm that the review's spec-edit list needs no action (spec REJECTED 2026-09-16).
4. Whether the review's laboratory programme should be offered to Stream 3 under the pin protocol at all.

---
*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: `checkers/check_external_review_fable_2026_09_21.py`
(12/12 CONFIRMED), `checkers/test_external_review_fable_controls.py` (22/22), LeanMaster `search_theorems`
for the cited declarations, repo search for the reviewed spec (untracked `~/K3spec.md`, rejected
2026-09-16) | Reviewed-by: N*
