# WP-GE10 step 1 — an explicit M₇-polarized model over the cooper_s7 coordinate (Inose / CDLW normal form)

**Date:** 2026-09-27 · **From:** Stream 2 · **To:** T0 (one reading to rule, §5); Stream 1 (a Lean
target, §6) · **Status:** RECORD, Tier B; nothing scored, ranked or promoted (D7′ narrow).

## 1. Why

The open thread GE-10 (`briefs/THOUGHT_EXPERIMENTS_K3_SELECTION_2026_09_21.md`; TODO "hypothesis,
zero independent tests") could not be tested because no explicit M₇-polarized K3 model existed in this
repository; the Almkvist–van Straten models are projective K3s without the M₇ structure made visible.
Standing rule 4: fetch and read before code. Three sources were fetched, hash-pinned and read
(`docs/literature/MANIFEST.md`, addendum 2026-09-27):

- **Clingher–Doran 2007** (arXiv:math/0602146), Thm 1.2 / Cor 1.3: the Inose quartic X(a,b) is the
  M = U⊕E₈⊕E₈-polarized K3 whose two elliptic curves have J-invariants (J(i) = 1 normalisation) equal
  to the roots of x² − (a³ − b² + 1)x + a³; so π := J₁J₂ = a³ and σ := J₁ + J₂ = a³ − b² + 1.
- **CDLW** (arXiv:0712.1880) §3.2: X(a,b) is M_n-polarized iff (E₁, E₂) are n-isogenous; the M_n locus
  is Y₀(n)+n ≅ X₀(n)+n, parametrised by the Γ₀(n)+ Hauptmodul when that curve has genus 0. Thm 3.4:
  the Picard–Fuchs operator drops to third order exactly on that locus.
- **DHNT** (arXiv:1312.6434) Remark 5.3: restricting the CDLW normal form to the M_n locus gives an
  M_n-polarized family for any n; they make n ≤ 4 explicit.

For n = 7 the Hauptmodul is our s7 coordinate z (T1 certificate `HAUPTMODUL_S7_GAMMA07PLUS.json`), so
the model is X(a(z), b(z)) with a³ = π(z) and b² = π(z) − σ(z) + 1, where π and σ are functions on
X₀(7)+. That curve has **one** cusp (z = 0), so π and σ are Laurent polynomials in z.

## 2. What was computed (`checkers/check_inose_model_M7.py` → `INOSE_MODEL_M7.json`; all exact unless stated)

- **z(q)** to order 130 from the certified relation 1/z = 49t + 13 + 1/t, t = η(7τ)⁴/η(τ)⁴ (constants
  and exponents read from `CM_POINTS_RHO20.json`), cross-checked term by term against the pinned
  b-file (29 terms) and the mirror map recomputed from `refs/` (36 terms).
- **J(q)** = E₄³/(E₄³ − E₆²) exactly; σ = J(τ) + J(7τ), π = J(τ)J(7τ).
- **The model.** Verified on every order to q¹²⁸ (`PASS(128)`):

  σ(z) = −(160/27) z⁻¹ + (98/9) z⁻² + (245/18) z⁻³ − (1813/288) z⁻⁴ + (7/9) z⁻⁵ − (7/192) z⁻⁶ + (1/1728) z⁻⁷

  π(z) = (21952/729) z⁻² + (10976/243) z⁻³ + (5537/243) z⁻⁴ + (2891/729) z⁻⁵ + (791/15552) z⁻⁶ + (7/31104) z⁻⁷ + (1/2985984) z⁻⁸

  and the family is the CDLW normal-form point [a, b, 1] ∈ WP(2,3,6) with W₁ = a³ = π(z),
  W₂ = b² = π(z) − σ(z) + 1. This is the explicit M₇-polarized model GE-10 was missing.
- **Where the 7-isogenous pair is isomorphic** (J₁ = J₂ ⇔ σ² = 4π). Exactly:

  σ² − 4π = −(z+1)(27z−1) · (2z−1)²(8z−1)²(24z−1)²(8z²+16z−1)² / (2985984 z¹⁴).

  The two **simple** zeros are the two finite singular loci of L₃, z = −1 and z = 1/27 — the W₇ fixed
  points, D = −7 and D = −28 (J₁ − J₂ behaves like a square root there, as it must at a point fixed
  by the involution that swaps J₁ and J₂). The **double** zeros are the other CM points whose curve
  has an endomorphism of norm 7 (D f² = t² − 28): z = 1/2 (D = −12), z = 1/8 (D = −19), z = 1/24
  (D = −27), and the two roots of 8z² + 16z − 1 (D = −24, class number 2). Each discriminant is hit
  exactly h(D) times (1+1+1+2 = 5 double zeros). Discriminants were assigned by matching σ(z)/2 to
  Klein's J at a representative τ of each reduced form (numeric control, 1e−20). Where
  `CM_POINTS_RHO20.json` has the row (z = −1, 1/27, 1/2) its D agrees; the rows for −19, −27, −24 are
  outside that table's vector window (−v² ≤ 44; they need −v² = 266, 378, 84), which the checker
  computes and records — a **finding about the table's window**, consistent with its own "not
  complete beyond the listed discriminants" clause.
- **z = ∞** (the order-3 point): σ = π = 0, i.e. both curves have J = 0 — E_ω × E_ω, T = A₂, the
  surface the external review names X₃ (consistent with `A2_MEMBERSHIP.json`, by a third route).
- **Numeric control at the loci:** at the certificate's τ for z = −1 and z = 1/27, `mpmath.kleinj(τ)`
  and `kleinj(7τ)` both equal σ(z)/2 to 1e−36. Controls: `checkers/test_inose_model_M7_controls.py`
  (scrambled z refused; level-5 pair does not fit; wrong pole order fails; class-number count needs
  D = −24; the J control rejects a 1e−10 shift; σ² − 4π ≠ 0 at a generic point).

## 3. What this says, read against the ledger

1. **Three disjoint routes now meet at the same two points.** The operator route (Riemann scheme),
   the lattice route (CM points of U⊕⟨14⟩) and the **Inose route** (self-7-isogenous pairs) all
   single out z = −1 and z = 1/27. The Inose route is exact once z is the Γ₀(7)+ Hauptmodul (Tier B);
   it uses no monodromy and no lattice. It is not corroboration of the lattice route in the D7′ sense
   (elliptic point ⇒ CM is still forced); it is a different **construction** of the same surfaces.
2. **ρ = 20 points that are not singular points of L₃.** z = 1/2, 1/8, 1/24 and the D = −24 pair have
   ρ = 20 (J₁ = J₂ gives the extra class, the graph of the identity) while L₃ is regular there. This is
   the "CM points are dense; the cut lists members, never a point" clause of D7′ made concrete at
   rational z. No preference among any of them follows (AM-6).
3. **GE-10 itself is not yet tested.** The hypothesis (A₁ points merging at the div-2 locus z = −1) is
   about the geometry of the surface at the two simple zeros. The model now exists to test it; the
   test needs the next step.

## 4a. Step 2, executed the same day up to the Kodaira boundary (`checkers/check_inose_fibration_multiplicities.py` → `INOSE_FIBRATION_MULTIPLICITIES.json`)

**Source, not memory.** The Weierstrass equation was taken from Kuwata–Shioda (arXiv:math/0609473,
located through the arXiv API by author — a remembered id was wrong and discarded unread), §5.3:
the type-J₉ pencil on Km(E₁×E₂) with Legendre parameters λ₁, λ₂, discriminant u⁶(u−1)¹⁰d(u),
deg d = 2, and their printed disc(d). The transcription is **verified** against that printed
discriminant (up to the recorded convention factor 16² between Silverman's Δ and theirs); a
sign flip or an exponent error is refused (controls N1, N2). KS state (Example 1.3) that the
degree-2 base change of this pencil is the elliptic K3 with two II* fibres, i.e. the Inose
surface; the base change u = s² and the minimalising twist are done here and give a K3
Weierstrass model (degrees 4, 8, 12) with Δ_X = (s²−1)¹⁰ d(s²) of degree 24.

**Result, exact, orders of vanishing only (no Kodaira label attached, §5):**

| situation | orders of the roots of Δ_X |
|---|---|
| generic (E₁, E₂ independent) | {10, 10, 1, 1, 1, 1} |
| **J(E₁) = J(E₂)**, J ∉ {0, 1} — in particular **both loci z = −1 (D = −7) and z = 1/27 (D = −28)** | **{10, 10, 2, 1, 1}** |
| J = 0 (z = ∞, E_ω × E_ω) | {10, 10, 4} |
| J = 1 (E_i × E_i) | {10, 10, 2, 2} (one at s = ∞) |

The mechanism was not expected beforehand and is the finding: with λ₁ = λ₂, **d(0) vanishes
identically**, so d(u) = u·e(u) and after the base change the two simple roots at ±√(·) collapse
onto the branch point s = 0 — exactly **one order-2 fibre** appears, for every isomorphic pair
outside the explicit exceptional set {λ ∈ {0, 1, −1, 2, ½}, λ² − λ + 1 = 0} = {J ∈ {1, 0}} and the
degenerate curves. The degree-6 λ-polynomials of the two loci' J-values (J = −125/64 and
614125/64, read from the model; they are j = −3375 and 255³, the class-number-one values for
D = −7 and −28 — computed, not typed) share no root with that set.

**GE-10, answered at the fibre level for this fibration:** the div-2 point z = −1 and the div-1
point z = 1/27 are **indistinguishable** — each shows one new order-2 fibre, no "merging of A₁'s".
The second extra class of the rank-20 surface (rank 19 → 20 at these loci) is therefore **not a
fibre**; it must be a Mordell–Weil section. (Read with the D7′ lattice data this would put the
section's height at disc(NS)/2, i.e. 7/2 at z = −1 and 14 at z = 1/27 — an implication, not
computed, Tier B.) The two special rows reproduce, from the sourced equation, the orders that
the external review's X₃ and X₄ tables carry under their Kodaira labels (II*, II*, IV and
II*, II*, I₂, I₂) — which lets those two review rows be scored CONFIRMED at the level of orders.

## 4. Next step (the part that still needs the T0 reading, §5)

Done in §4a up to the point where a Kodaira **label** would be attached to an order. What remains
gated: (i) naming the order-2 fibre (I₂ vs II is decided by ord a₄ at s = 0 — computable, but the
label is the reading T0 owns); (ii) the Mordell–Weil section at the loci (its explicit form; only
its existence is forced by the rank count). Neither changes the fibre-level conclusion.

## 5. Ask (T0)

**Ledger item 3 says: no Kodaira fibre from L₂/L₃ exponents at any locus.** The next step reads
Kodaira types of an **explicit Weierstrass model over the t-line of a fixed surface**, not from
Picard–Fuchs exponents and not of the z-family. I read that as outside the prohibition (the audit
brief of the Fable review said the same), but the ledger is T0-owned: **confirm that reading, or
decline the step.** Nothing in §2 depends on it.

## 6. Stream 1

The Laurent polynomials σ(z), π(z) are exact rational data; "σ² − 4π factors as stated" and "the
simple factors are z + 1 and 27z − 1" are finite computations a kernel could check (polynomial
identity over ℚ). Optional target, after the rank-jump lemma.

*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: `checkers/check_inose_model_M7.py` (all
clauses), `checkers/test_inose_model_M7_controls.py`; sources read as listed in
`docs/literature/MANIFEST.md` (addendum 2026-09-27) | Reviewed-by: N*
