# WP-TW2-A: explicit twisted-Weierstrass (f, g) construction at n = 0 — mixed result

**Date:** 2026-07-31. **Status:** DRAFT — pending T0 (Xavier) / coordinator verification
pass. Producing tier does not self-promote (standing rule).
**WP:** WP-TW2-A, executing standing T0 order D5 via delegated ruling R4
(S3 `briefs/T1_DELEGATED_RULINGS_2026_07_31.md`). Predecessor: `WP_TW2_M19_EXHIBITION_2026_07_31.md`
(verified-honest-negative: stopped before the construction attempt). Feasibility input:
`TW1_TWO_E8_FEASIBILITY_RESULT_2026_07_29.md`.
**Checker:** `checkers/check_TW2A_n0_construction.py` (exit 0; controls in
`checkers/test_TW2A_n0_construction_controls.py`, 7/7 green; certificate
`data/certificates/TW2A_n0_construction.json`). Exact sympy Integer/Rational arithmetic and
exact radicals end-to-end; no floats.

## Headline (four findings)

1. **f, g EXHIBITED at n = 0** (explicit rational coefficients, exact II* along both C₀ and
   C∞) — the construction D5 ordered exists and is now on disk, checker-verified.
2. **The ⟨−14⟩ class is IDENTIFIED and its source is FORCED** (on the K3 fiber, where M₁₉
   lives per the predecessor's T0-endorsed rescoping): it is the orthogonal projection
   **P̄ = P − O − 7F of a Mordell–Weil section P of height 14 with P·O = 5**, and every
   alternative source (extra reducible-fiber components, multisections, base-curve
   pullbacks — the task's candidate list) is *excluded by exact arithmetic*. Fiber-level
   M₁₉ realization holds **conditional on cited Shioda–Inose theory (Tier B, hedged
   below)**.
3. **Fourfold-level ⟨−14⟩ realization is OBSTRUCTED for the entire isotrivial ansatz**, by
   two independent exact computations (monodromy; square-twist non-minimality) — this is
   an obstruction result of the same epistemic shape as TW1's P³ collision verdict.
4. **NEW STRUCTURAL FINDING (sharpest):** *every* n = 0 two-E8 model — not just ours —
   carries **unavoidable codim-2 (4,6) curves inside both E8 divisors**, which TW1's
   necessary-condition screen (generic points of divisors only) structurally could not
   see. Under TW1's adopted Reading 1 this makes every n = 0 model non-minimal as given;
   under Reading 2 the standard cure (base blow-up) leaves n = 0 scope. **The two readings
   diverge materially for the first time → genuine T0 ruling required** (this is the
   "sharp impasse survives an actual n = 0 construction attempt" branch that R4 said
   returns to T0 with the evidence).

No physical coupling of any kind is claimed (VISION §1.3). No observable — F5b stands.
cooper_s10 / U⊕⟨20⟩ not used. No AlphaEvolve/Stream-4 input (sandbox).

## 1. Setup (n = 0)

B₃ = P(O⊕O)/P² = P¹×P², coords (s:t)×(x:y:z). −K = O(2,3), so f ∈ H⁰(O(8,12)),
g ∈ H⁰(O(12,18)). II* along a divisor D needs exactly (v(f), v(g), v(Δ)) = (≥4, 5, 10)
(same Tate convention as TW1's checker). Imposing II* along C₀ = {s=0} and C∞ = {t=0}
forces
```
f = s⁴t⁴·φ(x,y,z),           φ  of degree 12,
g = s⁵t⁵·(a s² + b st + c t²),   a, b, c of degree 18,
```
with exact orders ⟺ φ, a, c ≢ 0 on the respective divisors. The checker verifies
(exhaustive enumeration inside TW1's budget box, exact intersection products) that
**(1,0)+(1,0) — i.e. two P¹-fibers — is the ONLY disjoint irreducible two-divisor
configuration at n = 0**, so everything below covers every two-E8 model at n = 0.

## 2. The explicit model (finding 1)

The certified G0/U1 anchor is T(cooper_s7) ≅ U⊕⟨14⟩, NS ≅ M₁₉ = U⊕E₈(−1)²⊕⟨−14⟩
(G0 certificate, LIVE). An elliptic K3 with two II* fibers and NS = M₁₉ is, by cited
Shioda–Inose theory, the Inose K3 of a pair of elliptic curves related by a **cyclic
7-isogeny** (T ≅ U⊕⟨2n⟩ for an n-isogenous non-CM pair; 2n = 14 ⟹ n = 7). This dictated
the working point: h = 1 on X₀(7), giving the non-CM pair

- j₁ = 63·2647³ = 1168429123449, j₂ = 21609 (exact, from the X₀(7) hauptmodul
  parametrization in `refs/x0_7_inose_cm.json`; J_i = j_i/1728),

and the **all-rational** twisted model (the τ-parametrization clears both the cube root
and the square root of the normalized Inose form):
```
τ = J₁J₂(1−J₁)(1−J₂),  a = 1,  c = τ³/(J₁J₂),  b = −2J₁J₂(1−J₁)²(1−J₂)²,
w = x⁶ + y⁶ − 2z⁶      (degree-6 twist form),
f = −3τ·w²·s⁴t⁴,       g = s⁵t⁵·w³·(a s² + b st + c t²).
```
Checker-verified, all exact: bidegrees (8,12)/(12,18) ✓; orders (4,5,10) along both C₀,
C∞ ⟹ II*+II* ✓; residual discriminant quartic separable ⟹ 4×I₁ ✓; fiber Euler number
10+10+4 = 24, χ = 2 ✓; along the twist wall {w=0}: orders (2,3,6) = I₀*, **CY-minimal in
codimension 1** ✓. The scaling to the normalized Inose model X_{α,β} (α³ = J₁J₂,
β² = (1−J₁)(1−J₂)) is *exhibited* as explicit radicals and verified symbolically: every
fiber over {w ≠ 0} is Q̄-isomorphic to the single Inose K3 (isotrivial family).

**Transcription safety:** the literature data entered via `refs/x0_7_inose_cm.json` +
MANIFEST (SHA256-pinned) and is consumed only after in-checker gates pass: the Fricke
involution identity j₁(49/h) = j₂(h) (symbolic); every CM j equals its factored cube form;
and the *joint fingerprint* — at the Fricke fixed points h = ±7 the parametrization must
reproduce the textbook CM values 255³ (disc −28) and −15³ (disc −7) **and** the residual
quartic discriminant must vanish *exactly* (it does; and it is nonzero at h = 1). A wrong
constant in either the hauptmodul or the Inose normalization breaks this fingerprint.

## 3. K3-fiber Picard classes and the ⟨−14⟩ generator (finding 2)

Assembled and verified exactly (checker blocks C–D):

- **U** from (F, O+F): Gram [[0,1],[1,0]] ✓. **E₈(−1)²** from the two II* fibers:
  Cartan det = 1 ✓, negative definite ✓; trivial lattice rank 18, det −1, signature
  (1,17) ✓. E₈ component groups trivial ⟹ **contr_v = 0 for every section** (all
  sections pass through identity components) ✓.
- **Shioda–Tate forcing** — *conditional on the cited SI facts (Tier B): ρ = 19 and
  T ≅ U⊕⟨14⟩ for the Inose K3 of a non-CM 7-isogenous pair* — exact arithmetic then
  forces: MW rank = 19−18 = 1; MW torsion-free (component groups trivial); generator
  height h(P) = |disc NS|/|det triv| = 14; height formula 14 = 2·2 + 2(P·O) − 0 ⟹
  **P·O = 5** (integral ✓).
- **P̄ = P − O − 7F**: P̄² = −14, P̄·F = P̄·O = P̄·(all 16 E₈ classes) = 0 ✓; the full
  19×19 Gram in basis (F, O+F, e₁..e₈, e₁′..e₈′, P̄) is **exactly** the block matrix
  U⊕E₈(−1)²⊕⟨−14⟩, det 14, signature (1,18), disc group Z/14 — same genus data as the
  G0 certificate's exhibited NS(cooper_s7) ✓.
- **Uniqueness of the source** (what else was searched, exhaustively by structure):
  ADE fiber enhancement excluded (only rank-1 ADE is A₁, det 2 ≠ 14; gluing arithmetic
  14m² = 2 has no solution); base-curve pullbacks restrict to multiples of F (inside U);
  multisection classes lie in span(trivial lattice, MW projections) by Shioda–Tate. **The
  MW section is the only possible source of ⟨−14⟩.** Also: 14 is squarefree ⟹ no proper
  same-rank overlattice (index m needs m² | 14) ⟹ NS is *exactly* M₁₉ given ρ = 19.

Corroboration (cited, not load-bearing): Shioda's MWL(Inose pencil) ≅ Hom(E₁,E₂) with
height 2·deg gives 2·7 = 14 for the 7-isogeny generator — consistent with the independent
Shioda–Tate derivation above.

**Epistemic status of finding 2:** everything numeric is exact and checker-verified; the
*existence* inputs (ρ = 19, T ≅ U⊕⟨14⟩) are cited literature (Inose 1978; Morrison 1984
Thm 6.3; Shioda 2006), Tier B — verified-in-repo they are not. The explicit polynomial
coordinates of P are NOT exhibited (§5).

## 4. Fourfold-level obstructions (findings 3–4)

**(E) Square twist is CY-fatal.** The unique way (inside this ansatz) to make the
fiberwise section rational over the family is w = v² (v a cubic): the lift
(x, y) → (v²x_P, v³y_P) is verified as a symbolic identity. But then ord_{v=0}(f, g, Δ) =
(4, 6, 12) — a **codimension-1 (4,6) divisor**, non-minimal under BOTH readings (the
unambiguous case). Geometrically the square twist trivializes the family (birationally
K3×P², not CY) — the checker's order computation is the certificate of that.

**(F) Monodromy kills ⟨−14⟩ for non-square w.** The wall monodromy around {w=0} is the
fiberwise elliptic inversion (verified symbolically: w = σ² trivializes the twist; the
deck map σ ↦ −σ sends Y ↦ −Y). Inversion fixes F, O and every E₈ class (E₈ Dynkin graph
has trivial automorphism group — brute-forced — and component groups are trivial), and
sends P̄ ↦ −P̄. The monodromy-invariant sublattice of M₁₉ has rank 18; divisor classes on
X₄ restrict into the invariants ⟹ **no divisor on the isotrivial X₄ restricts to the
⟨−14⟩ generator**. Rank-18 (U⊕E₈²) *is* realized by fourfold divisors (zero-section,
fibers, resolved II* components — fiberwise).

**(G) Universal codim-2 (4,6) at n = 0.** For *every* n = 0 model (not just ours):
a, c ∈ H⁰(P², O(18)) are nonconstant, so {a=0}, {c=0} are nonempty curves; along
{t=0}∩{a=0} every term of g = s⁵t⁵(as²+bst+ct²) has (t,a)-adic order ≥ 6 —
**unconditionally, no genericity needed** — while v(f) ≥ 4. The (4,6) curse fires on a
nonempty codim-2 curve inside C∞ (symmetrically {s=0}∩{c=0} inside C₀), for every model.
This is invisible to TW1's screen, which (correctly, per its own scope) checked exact
orders at *generic* points of the divisors only. In our explicit model the locus is even
deeper ((6,8), since a,b,c all carry w³) and contains the exhibited rational point
(1:1:1) ∈ {w=0}.

**The Reading question now has teeth.** TW1 recorded two readings of a codim-2 (4,6)
locus and adopted Reading 1 (no minimal Weierstrass CY over B₃ as given) — harmless
there, because both readings agreed on P³. Here they **diverge**:
- *Reading 1* ⟹ every n = 0 two-E8 model is non-minimal as given ⟹ the n = 0
  fourfold-level exhibition is CLOSED as a documented dead end (and TW1's PASS verdicts
  describe a screen no actual model can survive at the next stage).
- *Reading 2* (standard F-theory practice: such loci are routinely cured by base
  blow-ups — the classic E₈×E₈ "point-like instanton" story) ⟹ the cure exists but the
  base is no longer P(O⊕O)/P² ⟹ leaves n = 0 (indeed the whole current ladder rung's)
  scope, and TW1's verdict table would need re-examination on blown-up bases.

This is a genuinely T0-owned epistemic call (possibly with the T0s referral R4
anticipated). **Flagged, not resolved here.** Structural remark, **UNCHECKED** and
explicitly not claimed: the C∞-side coefficient has positive degree 18+n for every n ≥ 0,
suggesting the phenomenon is not special to n = 0 — verification is future work.

## 5. The three construction attempts (per the WP's stop rule)

1. **Isotrivial, square twist (w = v²)** — the only variant with a manifestly rational
   ⟨−14⟩ divisor (lift identity verified). **Dead:** codim-1 (4,6,12) along {v=0},
   non-minimal under both readings (checker block E).
2. **Isotrivial, generic twist (w square-free)** — CY-minimal in codim 1 (I₀* wall ✓),
   fiber-level M₁₉ realized (Tier B). **Dead at the fourfold level:** inversion monodromy
   (block F) — and additionally caught by (G) at codim 2 under Reading 1.
3. **General coefficients (any φ, a, b, c)** — instead of a third ad-hoc model, the
   general analysis: fiberwise M₁₉ forces the Inose invariants (φ³/ac, b²/ac) to trace
   the X₀(7) modular curve over P², and (G) proves every such model carries the codim-2
   (4,6) curves. The non-isotrivial "modular pencil" route (X₀(7) has genus 0, so
   pencils P² ⇢ X₀(7) exist; a factorization ansatz φ = q̃₁q̃₂q̃₃m, ac ∝ λ₁⁸λ₂⁸q̃₁m³
   makes the cube/square constraints structurally satisfiable) is **mapped but not
   executed** — it is pointless to execute before T0 rules on the Reading question, since
   (G) gates it equally.

Also not exhibited: explicit polynomial coordinates (A, B, C) of the MW section P
(x_P = A/B², y_P = C/B³, deg B = 5 ⟸ P·O = 5). Identified follow-up paths: (i) Kummer
sandwich transfer of the graph of the 7-isogeny (fully explicit in principle, long);
(ii) literature transcription (Shioda/Kuwata explicit-section computations); (iii) direct
ansatz solve (≈46 unknowns, ≈40 nonlinear conditions — infeasible for the repo's sympy
toolchain as a blind Gröbner problem). Not started; gated on the same T0 ruling.

## 6. What is and is not claimed

**Claimed (exact, checker-verified):** the explicit f, g and all order/bidegree/
separability/Euler facts; the trivial-lattice and M₁₉ Gram assembly and its match to G0's
genus; the P̄ intersection arithmetic; the exclusion lemmas; the three obstruction
computations (E), (F), (G); the disjoint-pair exhaustiveness at n = 0; all control
behavior.

**Claimed conditional on cited literature (Tier B, hedged):** ρ = 19 and T ≅ U⊕⟨14⟩ for
the h = 1 Inose fiber (Shioda–Inose theory + non-CM + cyclic 7-isogeny via X₀(7)); hence
"NS(generic fiber) = M₁₉ exactly" and "h(P) = 14, P·O = 5".

**Not claimed:** anything at n > 0; a proof of the SI facts; crepant resolution of the
fourfold; explicit section coordinates; any resolution of the Reading question; any
physical statement (VISION §1.3); any observable (F5b). cooper_s10 / U⊕⟨20⟩ untouched.

## 7. Escalation to T0 (decision request)

**Q1 (the Reading question — blocking):** does a codim-2 (4,6) locus mean "no minimal
Weierstrass CY over B₃ as given" (Reading 1, TW1-adopted ⟹ n = 0 fourfold route CLOSED
as documented dead end) or "cure by base blow-up" (Reading 2 ⟹ base leaves the current
ladder; TW1 table needs re-examination on blown-up bases)? The repo has no F-theory/Tate
literature in `refs/` to settle it; this WP supplies the first case where the answer
changes the verdict. R4 pre-authorized returning the T0s (Deep Think) referral question to
T0 exactly here.

**Q2 (scope):** given the monodromy obstruction, should "M₁₉ exhibition" be formally
re-scoped to the K3 fiber (predecessor's reading, completed here at Tier B), with the
fourfold-divisor version tracked as a separate open problem?

**Q3 (only if Reading 2):** authorize WP-TW2-B (non-isotrivial modular-pencil families +
blow-up bookkeeping + explicit MW section), in that order.

## Decision log

- 2026-07-31, producing session: all checker assertions + 7/7 pytest controls green;
  TW0/TW1 regression re-run clean (TW1 exit 0; 4/4 controls). Files:
  `checkers/check_TW2A_n0_construction.py`, `checkers/test_TW2A_n0_construction_controls.py`,
  `refs/x0_7_inose_cm.json` (+ MANIFEST entry, SHA256-pinned),
  `data/certificates/TW2A_n0_construction.json`, this brief.

Provenance: Generated-by: Fable 5 (Stream 2, WP-TW2-A session 2026-07-31) | Verified-by:
`checkers/check_TW2A_n0_construction.py` (exit 0) + `checkers/test_TW2A_n0_construction_controls.py`
(7/7) | Reviewed-by: pending T0 (Xavier) — coordinator verification pass owed
(producer ≠ verifier).
