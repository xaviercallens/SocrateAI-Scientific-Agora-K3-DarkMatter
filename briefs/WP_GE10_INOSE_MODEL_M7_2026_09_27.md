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

## 4. Next step (not executed — needs one T0 reading, §5)

Reduce X(a(z), b(z)) to its Inose elliptic fibration (Weierstrass form, source to fetch: Inose 1978
or Shioda 2006 "Kummer sandwich", not from memory) and compute, as exact functions of z, the orders
of vanishing of (a₄, a₆, Δ) at the roots of Δ(t). At the two simple zeros the extra algebraic class
should appear as a coincidence of discriminant roots; whether the div-1 point (z = 1/27) and the
div-2 point (z = −1) differ **in the fibre configuration** or only in the value of J is exactly
GE-10's question, and it is decidable by this computation. The external review's own tables for
X₃/X₄ (II*, II*, IV; II*, II*, I₂, I₂) are the z = ∞ cases of the s7 and s10 families, respectively.

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
