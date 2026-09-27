# External review — "K3 Selection Review" (Fable 5.1), dated 2026-09-21

**Record, verbatim.** Text extracted 2026-09-27 from the Claude Docs document
`https://claude.ai/artifact/SFDSuPbfKD8SB4mVQhAErg` (doc id `cc708cbe-058d-4c7e-9903-02b9af1e1d5d`, rev 21)
by flattening its block XML to Markdown: headings, list items and table cells preserved in
order, table rows flattened to one cell per line, inline formatting dropped. Nothing was
added, reworded or removed. Author of the reviewed text: Fable 5.1 (per the session that
produced it); the "specification" it reviews is NOT this repository's material.

**Status in this repository:** an EXTERNAL REVIEW, not a ruling and not a certificate.
Its Stream-2-relevant clauses are scored against certificates by
`checkers/check_external_review_fable_2026_09_21.py`
(`data/certificates/EXTERNAL_REVIEW_FABLE_2026_09_21_AUDIT.json`); the audit and the
directions drawn from it are in `briefs/EXTERNAL_REVIEW_FABLE51_AUDIT_AND_DIRECTIONS_2026_09_27.md`.
Nothing in this file may be cited as evidence for a candidate; only the audit certificate may.
The review's own caveat applies: its literature identifiers are "from memory and should be
pinned before citation".

---

# 

# K3 Selection Review
2026-09-21 · @Xavier
The K3 selection in the specification cannot be confirmed as written: seven load-bearing claims fail direct computation, and its three headline choices (Kummer surface, τ = i, R_NL = 462/360) contradict the programme's own kernel-checked Papers 10 and 12. A defensible replacement already exists inside the programme: the attractor K3 of Paper 12, X₃ with transcendental lattice A₂, which has an explicit Weierstrass model whose invariants are checkable in Lean.
## Verdict
Not confirmable. The failures fall in three classes, and the third is the one a referee will find first.
- 
Arithmetic and algebra that does not hold. The cosmological-constant evaluation is off by 98 orders of magnitude; the A₄ branching 24 = 3⊕3⊕3⊕1¹⁵ is impossible for any A₄ inside M₂₄; the "Kummer quartic" is not homogeneous; a K3 cannot carry 24 nodes; the Picard–Fuchs operator's singular points are not where the spec says, and a rank-20 K3 has no complex-structure modulus for such an operator to govern.
- 
Claims with no derivation. The error bar on r, the value of δ_CP, the 21-cm depth, the 4.038 GHz peak, the TDA Euler peak and the "b₂ = 22 in galaxy clustering" line have no computation behind them in the spec or in Papers 10–12.
- 
Contradiction with the programme's own kernel-checked results. Paper 12 selects T_S = A₂, D = −3, τ = ω (not Kummer, not τ = i). Paper 10 shows 462/360 fails twining at every non-identity class. Paper 11 records that K3 × T² is N = 4 and non-chiral, so no generation count follows from it.
What survives, and can stay: χ = 24, b₂ = 22, signature (3,19), Γ³·¹⁹ ≅ E₈(−1)² ⊕ U³, Mukai's theorem, the EOT decomposition 90 = 45⊕45̅ etc., the Borcherds-lift weight formula (with its label corrected), and the eight η-quotient coefficients a(n), which I reproduced exactly.
The honest framing is the one Paper 12 already uses: "which K3" has an answer only once one says which physics is doing the selecting. The spec never says, and borrows from three different selectors at once.
## Claim-by-claim verification
Every line below was recomputed in this session (Python/SymPy; M₂₄ built from its standard four generators on P¹(F₂₃) and its order checked as 244 823 040). Nothing is taken from the spec's own tables.
Spec claim (section)
What computation gives
Status
ρ_Λ = M_Pl⁴ e^{−2π√23}/V⁸ ≈ 2.28×10⁻⁴⁷ GeV⁴ ≈ 10⁻¹²² M_Pl⁴ (§2.1)
e^{−30.133}/(30.133)⁸ = 1.2×10⁻²⁵, so ρ = 2.7×10⁵¹ GeV⁴: 98 orders too large. The spec's own intermediate numbers (8.19×10⁻¹⁴, 6.79×10¹¹) are right; the final line does not follow from them. Reaching 10⁻¹²² needs Δ ≈ 1425 (with the V⁸ prefactor) or ≈ 1999 (without), not 23
fails
24 restricted to A₄ = 3₁ ⊕ 3₂ ⊕ 3₃ ⊕ 1^{15} (§2.3)
Multiplicity of the triplet is (24 − f₂)/4 with f₂ the fixed points of an involution of M₂₄, and f₂ ∈ {0, 8} (classes 2B, 2A). So the multiplicity is 6 or 4, never 3. An explicit A₄ ⊂ M₂₂ ⊂ M₂₄ gives 24 = 8·1 ⊕ 2·1′ ⊕ 2·1″ ⊕ 4·3
fails
Kummer T⁴/Z₂ with 24 conical A₁ nodes (§3.3 A)
A Kummer surface has exactly 16 nodes. Nikulin (1975): a K3 carries at most 16 disjoint (−2)-curves, and 16 forces Kummer. 24 nodes is impossible on any K3
fails
Quartic (Σxᵢ²)² − y₀² x₀²x₁²x₂²x₃² Σ 1/xᵢ² = 0 (§3.3 B)
First term has degree 4, second degree 8 − 2 = 6. Not homogeneous, so not a hypersurface in P³ at all
fails
Picard–Fuchs "Almkvist–Zudilin #1", singular fibres at z = 1/27 and z = −1, ρ = 20 (§3.3 C)
Leading symbol of the operator as written is 1 − 27z − 9z², singular at z = 0.0366 and z = −3.04. AESZ #1 is the fourth-order quintic operator θ⁴ − 5⁵z(θ+1/5)⋯(θ+4/5), not this. A one-parameter family has generic ρ ≤ 19; ρ = 20 is rigid and has no modulus z
fails
Δ(Q,P) = 4(Q²/2)(P²/2) − (Q·P)² = 2n, Mₙ = √(2n) M_Pl (§3.2)
Q² = P² = 2, Q·P = 1 gives Δ = 3. Paper 12 Prop. 2.2 uses exactly this odd value as its floor
fails
k_g = χ(g)/2 − 2 with χ(2A) = 16, χ(3A) = 12, χ(4B) = 10 (§3.5)
Correct if χ(g) means the number of cycles of the frame shape (1⁸2⁸ has 16 cycles). The character of the 24 on 2A is 8. Formula right, symbol wrong
relabel
η-quotient: leading power q^{+1700/24}, weight −91.5, a(n) = 1, −24, 229, … (§3.6)
Σ d·e_d = −1700, so the leading power is q^{−1700/24}. Weight −91.5 correct. All eight a(n) reproduced. a(1) = −e₁ = −24 by construction, not a consistency check against χ(K3). Σ d·e_d ≡ 4 mod 24, so this is not a form on Γ₀(12) in the Newman–Ligozat sense; "level 12" is just the largest index
sign error; over-read
H³(M₂₄, U(1)) ≅ Z₁₂ × Z₂ (§3.3 A)
Literature value H⁴(M₂₄, Z) ≅ Z₁₂ (Dutour Sikirić–Ellis 2009, used by Gaberdiel–Persson–Ronellenfitsch–Volpato)
pin source
r = 12/N_e² = 0.00396 ± 0.00015, n_s = 1 − 2/N − 3/(2N²) = 0.9636 (§2.2)
12/55² = 0.00397. The displayed n_s formula gives 0.9631; 0.9636 is 1 − 2/N. N_e ∈ [50, 60] gives r ∈ [0.0033, 0.0048], so ±0.00015 is not derived from anything. 12/N² is the α = 1 attractor (K = −3 log), but the T² modulus τ has K = −log(τ + τ̄), i.e. α = 1/3 and r = 4/N² = 0.0013; the √(2/3) in §1.3 belongs to a volume modulus, not τ
error bar undeclared; α ambiguity
δ_CP = 282.4° ± 4° from τ* = i (§2.3)
τ = i lies on the CP-conserving locus of modular flavour models with generalised CP (Novichkov–Penedo–Petcov–Titov 2019): δ_CP ∈ {0, π} there. A non-trivial phase needs complex free couplings, so the "zero-parameter" claim fails on its own terms
fails
Σ_N χ(Λ_N) ≡ 0 over the 24 Niemeier lattices; Δ = 23 is the leading polar discriminant of 1/Φ₁₀ (§2.1)
No such identity exists. Polar terms of 1/Φ₁₀ have 4nm − ℓ² < 0, the most polar being −1. 23 is the largest element order of M₂₄, not a polar index
unsupported
χ(K3 × T²) = 0 is the prerequisite for 4D gravitational anomaly cancellation (§3.1)
Pure gravitational anomalies exist only in 4k + 2 dimensions. Nothing in 4D is cancelled by χ = 0
wrong
58 moduli = 20 Kähler + 38 complex structure (§3.4)
58 = dim O(3,19)/(O(3)×O(19)) + volume = 57 + 1. The 20/38 split is not a decomposition of that space
wrong
χ = 24, b₂ = 22, σ = −16, Γ³·¹⁹ ≅ E₈(−1)² ⊕ U³; Mukai: Aut_s ↪ M₂₃; EOT: 90 = 45 ⊕ 45̅, 462 = 231 ⊕ 231̅, 1540 = 770 ⊕ 770̅
Correct
holds
## Conflicts with Papers 10–12
Six statements in the spec are contradicted by results the programme has already kernel-checked or frozen. A referee who has the papers will read the spec as retracting them.
Spec
Programme result
Where
Fricke fixed point τ* = i; Kummer orbifold T⁴/Z₂
Attractor floor is D = −3, T_S = A₂, τ = ω (`smallest_black_hole`, `tau_minimal`); the paper says this "breaks an earlier i/ω tie". τ = i is the D = −4 charge (1, 0, 1), the second-smallest, and the surface is Inose-type, not Kummer
Paper 12, Thm 2.3, Remark 2.1
R_NL = 462/360 = 1.28333 listed as a CMB-S4 prediction
The ratio fails twining at all 25 non-identity classes (`ratio_fails_at_every_class`); classified numerology, Tier C
Paper 10, Thm 4.1
Three fermion families from M₂₄ ⊃ M₂₂ ⊃ L₂(11) ⊃ A₄
Type IIA on K3 × T² is N = 4, non-chiral, admits no chiral matter; a chiral geometry is "new research, not a patch"
Paper 11, §4 and §12.2
"Zero free parameters", "machine-certified Lean 4 proofs" of the physics
"The identification of a Lean object with a physical quantity is never Tier A"; "any statement about our universe" is listed under Is not proved
Paper 10, §2 and §11
Δ = 23 sets the dark-energy density
The only place 23 enters the programme's lattice arithmetic is as a discriminant D = −23, where h(−23) = H(23) = 3 counts U-duality orbits. No Λ appears; Paper 11 excluded the Hubble-scale dark-energy reading (C-A)
Paper 12 §2; Paper 11 §6
Δ(Q, P) is even; Mₙ = √(2n) M_Pl
4ac − b² = 3 is attained and is the floor (`discriminant_gap`)
Paper 12, Prop. 2.2
The TDA line in the spec's parameter table ("Cosmic Euler peak χ = 24.2 ± 0.8, 4.82σ") has no counterpart anywhere in the four papers. The only TDA datum the programme reports is the superfluid vortex floor F = 0.943ξ, which Paper 12 §5 shows sits at a lattice distance √2Δx to fourteen digits. If the CMB number exists, it needs a source file and a freeze tag; if it does not, the row must go.
## What selecting a K3 can mean
M₂₄ does not select a K3 surface, and no argument built on Mathieu moonshine can. The elliptic genus is a deformation invariant: it is the same function for every K3, so everything M₂₄ says is said about the whole 80-dimensional moduli space at once. Gaberdiel–Hohenegger–Volpato (2011) classified the symmetry groups of K3 sigma models: they are subgroups of Co₀ fixing a 4-plane, and M₂₄ is not among them at any point. The largest known is Z₂⁸:M₂₀ at the Z₂-orbifold of the D₄ torus (Gaberdiel–Taormina–Volpato–Wendland 2013); its order 245 760 does not even divide |M₂₄|, so it is not a subgroup of M₂₄. "The K3 of Mathieu moonshine" is a category error, and the spec's §1.2 rests on it.
A selection therefore needs a selector, which is the point Paper 12 makes. There are three that are Tier L, and they give different surfaces.
Selector
Input
Output
Literature
Attractor
A primitive positive-definite charge form (a, b, c) on K3 × T²
The singular K3 with T = [2a b; b 2c] (ρ = 20) and the T² at τ = (b + √D)/2a; unique per SL(2, Z)-class of the form
Moore 1998; Shioda–Inose 1977
Symmetry
The sigma-model point of maximal symmetry
The D₄-torus orbifold with Z₂⁸:M₂₀, realised through the hexacode and a quantum error-correcting code
GHV 2011; GTVW 2013; Harvey–Moore 2020
Arithmetic
Field of definition
A singular K3 of discriminant d is defined over Q only if the class group of discriminant d is 2-elementary; that gives a finite list of d
Schütt 2007, 2010
The spec borrows the output of each (ρ = 20 from the first, Kummer and Golay-code language from the second, "defined by a quartic" from the third) without running any of them, and the borrowed pieces are mutually inconsistent: a Kummer surface never has T = A₂ or T = ⟨2⟩ ⊕ ⟨2⟩ (Kummer doubles the form), and neither attractor surface has 16 nodes.
## Proposed selection
Take the attractor selector, because it is the only one of the three the programme has already formalised, and let it pick. It picks X₃, Vinberg's "most algebraic" K3 surface, and X₃ has a Weierstrass model whose every invariant is a finite computation.
### Primary: X₃ = Inose(Eω × Eω), the D = −3 attractor of Paper 12`
This is Inose's form y² = x³ − 3αt⁴x + t⁵(t² − 2βt + 1) with α³ = J₁J₂ = 0 and β² = (1 − J₁)(1 − J₂) = 1, i.e. both elliptic curves equal to Eω (j = 0). Checked in this session:
Datum
Value
How checked
Discriminant Δ(t)
27 t¹⁰ (t − 1)⁴, degree 14, so order 10 at t = ∞
SymPy factorisation
Singular fibres
II* at t = 0, II* at t = ∞, IV at t = 1
Kodaira table from ord(a₆) = 5, 5, 2 with a₄ = 0
Euler numbers
10 + 10 + 4 = 24 = χ(K3)
sum
Néron–Severi lattice
U ⊕ E₈(−1)² ⊕ A₂(−1), rank 20, Mordell–Weil rank 0
2 + 8 + 8 + 2 = 20
Transcendental lattice
T = A₂ = [2 1; 1 2], det 3; the unique even positive-definite binary lattice of discriminant 3, since h(−3) = 1
reduced forms of discriminant −3: only (1, 1, 1)
Field of definition
Q (class group trivial)
Schütt's criterion
Charges
(p²/2, p·q, q²/2) = (1, 1, 1), D = −3, τ = ω = e^{2πi/3}
Paper 12 `smallest_black_hole`, `tau_minimal`
Single-centred index
25 353
Paper 12 `smallest_black_hole_index`
Kummer partner
Km(Eω × Eω), T = A₂(2) = [4 2; 2 4], via the Shioda–Inose structure (Kummer sandwich)
Shioda 2006
What this replaces in the spec. "Kummer orbifold" becomes "Shioda–Inose partner of a Kummer surface": the Kummer is the degree-2 relative, not the surface. "Fricke fixed point τ = i" becomes "τ = ω, the order-6 elliptic point of SL(2, Z)". "Picard–Fuchs operator" is dropped: a singular K3 has no complex-structure modulus. If a family is wanted, the one-parameter Inose family with E₁ = Eω fixed and J₂ free has generic ρ = 19 and its Picard–Fuchs operator is second order in J₂ (the period is ω₁ · ω₂ with ω₁ constant); X₃ is its J₂ = 0 fibre.
What it buys: every line of the spec's "ρ = 20 attractor" column becomes a theorem about an explicit surface, provable in Lean by orders of vanishing and a 20 × 20 Gram determinant. What it does not buy: any 4D observable. The compactification is N = 4 and the selection is of one black hole's near-horizon geometry, exactly as Paper 12 states.
### Alternative A: X₄ = Inose(Eᵢ × Eᵢ), the D = −4 attractor — and the Fricke selection (see below)`
Δ(t) = 27 t¹⁰ (t − 1)² (t + 1)², degree 14: fibres II* at 0 and ∞ plus I₂ at t = 1 and at t = −1 (ord Δ = 2 with a₄ ≠ 0 there, so multiplicative), Euler 10 + 10 + 2 + 2 = 24; NS = U ⊕ E₈(−1)² ⊕ A₁(−1)², rank 20, Mordell–Weil rank 0, discriminant 4; T = ⟨2⟩ ⊕ ⟨2⟩, D = −4, charges (1, 0, 1), τ = i, index −50 064 matching Sen's printed 50 064 (Paper 12). It is the Shioda–Inose partner of Km(Eᵢ × Eᵢ), T = [4 0; 0 4]. This is the only legitimate reading of the spec's "Fricke fixed point" on the attractor side, and it is the second-smallest black hole, not the smallest. It is also, independently, what the Fricke involution selects on the K3 period modulus of the N = 1 Sym² family — see The Sym² selection chain below, which supersedes the framing of this subsection. Preferring it over the D = −3 floor now has a candidate reason (it is the W_N fixed point, and it is first in a height filtration) rather than none.
### Alternative B, if the number 23 must be kept: the D = −23 Galois orbit
Reduced forms of discriminant −23 are (1, 1, 6), (2, 1, 3), (2, −1, 3): h(−23) = H(23) = 3. The attractor selector returns three singular K3 surfaces, with T = [2 1; 1 12], [4 1; 1 6], [4 −1; −1 6], at τ = (1 + i√23)/2 and (±1 + i√23)/4. Their class group is cyclic of order 3, not 2-elementary, so by Schütt none is defined over Q; they are conjugate over the Hilbert class field of Q(√−23). This is the only rigorous place in the programme where 23 and 3 meet: three U-duality orbits of dyons at D = −23, counted by the same H that Paper 12's `immortal_m1` uses. It is a count of surfaces, not of fermion generations, and it says nothing about Λ.
### An observation to check, not a claim
The D₄ lattice is the Hurwitz order up to scale, and both i and ω = (−1 + i + j + k)/2 are units in it. Since Z[i] and Z[ω] are principal ideal domains and the order is torsion-free of rank 2 over each, C²/Λ_{D₄} is isomorphic as a complex torus to Eᵢ × Eᵢ under left multiplication by i and to Eω × Eω under left multiplication by ω. So the symmetry selector (GTVW's D₄-torus orbifold) and both attractor selectors (via their Kummer partners) sit on one real 4-torus, separated only by the choice of complex structure. If that holds up, it is the honest version of the spec's wish to have Kummer, τ = i and Z₂⁸:M₂₀ in one place; it would also be a small, self-contained Lean target (a rank-2 free-module statement).
## The Sym² selection chain
The operator theorem in SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal selects a K3 surface once one step is added. A rank-19 family is not a surface; the Fricke involution says which member to take, and the answer is computable by integer linear algebra.
### What was verified here
Building L₃ = θ³ − z(2θ+1)(aθ²+aθ+b) + z²(θ+1)(c(θ+1)²+d) and applying the Almkvist–van Straten residual gives zero identically, with no conditions on (a, b, c, d). This reproduces `partner_res0..3`, `partner_magic` and `P_cleared_eq_zero` independently of the Lean development.
The same criterion applied to the operator printed in §3.3C of the specification gives residual 3(54z⁴ − 162z³ + 39z² + 9z + 1) ≠ 0. It is not a symmetric square, so it is not a rank-19 K3 Picard–Fuchs operator.
But the specification's singular points are right. The s₇ operator (a,b,c,d) = (13, 4, −27, 3) has leading symbol −z³(z+1)(27z − 1), with singularities at z = 0, 1/27, −1 and ∞ — exactly the "0 (LCS), 1/27 (conifold), −1 (Fricke)" of §3.3C. The specification meant the repository's own s₇ operator and a different operator was transcribed in its place. (s₁₀ = (6, 2, −64, 4) gives −z³(4z+1)(16z − 1): 0, −1/4, 1/16, ∞.) Neither s₇ nor s₁₀ is the symmetric square of a Zagier-sporadic operator — solving for (A, B, C) projectively returns nothing — which is what makes Cooper's sequences new.
### The chain
The repository keeps operator, lattice and L-function as separate domains, which is correct tier hygiene. The implications between them are nonetheless theorems, and they are what turns the operator result into a selection principle:
L₃ = Sym² L₂  ⟺  T has rank 3 and signature (2,1)  ⟺  a one-parameter family of K3 surfaces with generic ρ = 19.
The middle term is already in `Geometry/MnLattice.lean` as T = U ⊕ ⟨2N⟩ with `TN_diagonalises`, and the right-hand equivalence is Doran's Picard–Fuchs uniformization: SO(2,1)° ≅ PSL(2,R), so a rank-3 variation of Hodge structure of that signature is the symmetric square of a rank-2 one. The automorphy factor (Ncτ+d)² recorded in `Geometry/ModularAction.lean` is the same Sym² at the monodromy level. Pin Doran as Tier L; the rest is already Tier A.
### The Fricke fixed point selects the surface
With period vector ω(τ) = e − Nτ²f + τg in U ⊕ ⟨2N⟩, a class v = (p, q, r) is algebraic exactly when Npτ² − 2Nrτ − q = 0. The Fricke involution W_N : τ ↦ −1/(Nτ) has fixed point τ = i/√N, and that is the solution for v = e − f, which has v² = −2. The Picard rank jumps to 20 and the new transcendental lattice is the orthogonal complement, computed here:
N
Fricke point
new class v
v²
T (reduced)
det T
CM disc
h
1
τ = i
(1, −1, 0)
−2
⟨2⟩ ⊕ ⟨2⟩
4
−4
1
2
τ = i/√2
(1, −1, 0)
−2
⟨2⟩ ⊕ ⟨4⟩
8
−8
1
7 (s₇)
τ = i/√7
(1, −1, 0)
−2
⟨2⟩ ⊕ ⟨14⟩
28
−28
1
10 (s₁₀)
τ = i/√10
(1, −1, 0)
−2
⟨2⟩ ⊕ ⟨20⟩
40
−40
2
So τ* = i/√N in §1.3 of the specification was the right formula attached to the wrong modulus. On the K3 period modulus, where W_N is the actual extra symmetry of the monodromy group Γ₀(N)+N and the moduli space carries an orbifold point, it selects a surface. On the T² Kähler modulus, where the specification put it, it selects nothing.
### τ = i and τ = ω are the two elliptic points of one family
At N = 1 the family has two elliptic points, and both complements were computed:
- 
order 2 (Fricke, τ = i), v = (1, −1, 0), v² = −2 → T = ⟨2⟩ ⊕ ⟨2⟩, det 4. This is X₄ = Inose(Eᵢ × Eᵢ), the specification's surface.
- 
order 3 (τ = ω), v = (−2, 2, 1), v² = −6 → T = (2, 2, 2) = A₂, det 3. This is X₃, Paper 12's attractor floor.
Neither paper is wrong. They apply different selectors to the same Sym² family, and the selectors disagree because they optimise different things: Paper 12 minimises the charge-form discriminant under the supergravity positivity condition, giving A₂; a lattice-height filtration gives ⟨2⟩⊕⟨2⟩ first. Which is physical depends on which quantity the programme claims is minimised, and that has never been stated.
### A prediction that upgrades a Tier B item
The README records the s₇ transcendental lattice as Tier B, pending Stream 2 numerical monodromy. The rank-jump computation needs no monodromy: it is a nullspace, a saturation and a binary-form reduction on a 3 × 3 integer Gram matrix. Predicted: W₇ has two fixed points, giving T = ⟨2⟩ ⊕ ⟨14⟩ (det 28, CM disc −28) and T = [[2,1],[1,4]] (det 7, CM disc −7), both from (−2)-classes, both h = 1 and defined over Q by Schütt's criterion. If Stream 2 returns something else, one of the two is wrong and the disagreement is cheap to find. The multiplicity matters: W_N has h(−4N) + h(−N) fixed points, so "the Fricke fixed point" is a selector only for N = 1. At N = 7 it names two surfaces, and the one with the smaller determinant is not the one at τ = i/√7.
In §3.3C of the specification this means: substitute the s₇ operator, keep the singular points, and drop the claim that the family has ρ = 20 — ρ = 19 generically, with 20 at the Fricke point, which is the surface being selected.
## Duality in other physics domains
The question is where the same modular duality is real physics rather than an analogy. One domain in the programme is already closed, and it is worth stating why before opening others.
Quantum fluids are closed as physics, open as an identity. Paper 12 §5 records the outcome: the independent superfluid group's Bogoliubov dual-length identity survives (`dualLength_bogoliubov`), but helium-4 misses the bound by a factor of 21 to 51 across pressures, the roton sits 4.6 times below the envelope, and the authors withdrew the string-theoretic framing. The R + α′/R shape in a dispersion relation is a genuine algebraic identity; it is not evidence of a compactification. Reopening this needs a different fluid and a pre-registered freeze, not a re-reading of the same data.
Three domains where the duality is exact and the fixed points are physical:
Domain
Group
Duality
Fixed point
Status
Quantum Hall plateau transitions
Γ₀(2) on σ = σ_xy + iσ_xx
σ ↦ σ/(2σ+1), σ ↦ σ+1
σ* = (1+i)/2, the measured critical point
Lutken–Ross, Burgess–Dolan; semicircle law is data
Seiberg–Witten N = 2 SU(2)
Γ(2) on the u-plane
S-duality τ ↦ −1/τ
monopole and dyon points
exact; periods satisfy an order-2 operator
2D XY model / BKT
vortex–spin-wave duality
R ↦ α′/R
the self-dual radius, the BKT transition
measured in films and cold atoms
K3 mirror symmetry
Γ₀(N)+N on the K3 period
W_N, the Dolgachev–Nikulin mirror involution
τ = i/√N
Dolgachev 1996; this is the programme's own family
The last row matters most: the Fricke involution the programme has been invoking already has a physical meaning, and it is mirror symmetry of the K3 family, not T-duality of a T². That reading is a theorem, and it keeps the duality while dropping the identification α′ = ℓ_P c/H₀ that Paper 11 excluded.
### One convergence worth checking
The unique elliptic point of Γ₀(2) is σ* = (1+i)/2, fixed by [[1,−1],[2,−1]] (verified: residual 0, determinant 1, trace 0), satisfying 2σ² − 2σ + 1 = 0, CM discriminant −4. Read as a point of the N = 2 K3 family, it gives the algebraic class v = (2, −2, 1) with v² = −4 and complement T = ⟨2⟩ ⊕ ⟨2⟩, det 4 — the same surface the N = 1 Fricke point selects.
Two unrelated selectors, one from a condensed-matter critical point that has been measured and one from the mirror involution of the K3 family, land on X₄ = Inose(Eᵢ × Eᵢ). This is stated as an observation to check, not a result: the identification of σ with a K3 period modulus is a reading (Tier C), and nothing here derives it. What makes it worth a stream is that it is falsifiable in one computation — if the Γ₀(2) point and the N = 2 family are genuinely the same moduli space, then the QHE critical exponents should be computable from the K3 period, and they are measured.
## What TDA can and cannot add
All K3 surfaces are diffeomorphic, so no persistence computation on the surface, or on a cosmological point cloud, can select one. What changed is that selection is now point selection on a modular curve, and a countable set of distinguished points in a surface is the natural setting for persistence.
Target
Filtration
Null model
What it returns
Rank-20 locus of the family
height max(|p|,|q|,|r|) of the algebraic class
none needed — exact
Ranks candidate surfaces by arithmetic complexity; computed below
CM points with |D| ≤ D_max in Γ₀(N)+N \ H
hyperbolic distance
Duke equidistribution
Whether the Fricke point is an outlier or typical
Cooper parameter space (a,b,c,d)
distance to integrality of the sequence
random (a,b,c,d)
Whether the sporadic solutions are isolated or lie on a variety
Monodromy of L₃ around {0, 1/27, −1, ∞}
—
—
Determines N from the operator alone, without Cooper's label
Rank jumps along a path in τ
zigzag persistence
—
The natural formalism for a lattice that appears and disappears
The first is already computable. Enumerating primitive (p, q, r) with |p|,|q|,|r| ≤ 6 for N = 1 and recording the first height at which each transcendental lattice appears:
T (reduced)
det
h(−det)
first height
witness v
⟨2⟩ ⊕ ⟨2⟩
4
1
1
(−1, 1, 0)
A₂ = (2,2,2)
3
1
2
(−2, 2, −1)
⟨2⟩ ⊕ ⟨4⟩
8
1
2
(−2, 1, 0)
⟨4⟩ ⊕ ⟨4⟩
16
1
2
(−1, 2, −1)
⟨4⟩ ⊕ ⟨8⟩
32
2
2
(−1, 2, 0)
So in a height filtration ⟨2⟩⊕⟨2⟩ is born first and A₂ second, while in a discriminant ordering A₂ (det 3) comes first. The two orderings disagree on exactly the two surfaces the programme has been arguing about. That disagreement is the honest content: a selector must be named before either ordering means anything.
### The technique that would actually unblock Stream 2
Not TDA. The blocker on the Tier B items is certified monodromy, and the tool for that is rigorous numerics — ball or interval arithmetic (Arb, or Mathlib's interval machinery) for analytic continuation of the Picard–Fuchs solutions along generators of π₁(P¹ − {0, 1/27, −1, ∞}). That produces enclosures of the monodromy matrices tight enough to certify the integer matrices exactly, which identifies Γ₀(N)+N from the operator and closes the loop on the table above without assuming Cooper's level labels.
## Reusing the topological-charge protocol
The astrophysical U(1) paper (28 Lean theorems, September 2026) contains no statement about K3 surfaces, and its own Section 1 rules out the move that would connect it to one. What it does supply is a certification protocol for reading a discrete invariant out of sampled data — which is exactly the blocker on the K3 selection.
### Transfers, does not transfer
Transfers. The five principles, read as a protocol for certifying integer monodromy matrices obtained by numerical analytic continuation of the Picard–Fuchs solutions; and the Arm V / Arm P / Arm 0 design, read as the control for any claim that a special point in moduli is a difference-maker.
Does not transfer. π₁(U(1)) = ℤ is a statement about a rank-1 charge on a loop. K3 selection is about a rank-2 transcendental lattice at a CM point. The shared word "topological" is not an identification, and the paper was written to say so. In particular this paper does not revive the specification's dead row (24 nodes → CMB defects); what it supplies there is the correct way to measure net string charge in a region — Principle 4, boundary-only — which is what that row's measurement side should have said in the first place.
### The five principles as a monodromy protocol
Principle
Statement for a U(1) phase
Statement for monodromy of L₃
1 integrality
w ∈ ℤ for any closed loop; a non-integer output is a bug in the reader
in an integral basis the monodromy lies in GL(3, ℤ); a non-integer entry is a continuation bug, never a property of the family
2 conservation by continuity
w constant while no sampled step reaches π; a change certifies a slip
the matrix is constant while no step leaves the disc of convergence; a change certifies the path crossed a singular point
3 barrier
changing w costs at least 2J − 2π²J/n
the step size is bounded by the separation of singular points; for s₇ the minimum separation is 1/27
4 scale additivity
oriented boundary sum = 2π × net charge inside; a neutral set is invisible
monodromy of a region = ordered product of the enclosed local monodromies; a set whose product is the identity is invisible — which is what an apparent singularity is
5 continuum limit
refinement is the test; a change under refinement disqualifies the loop
halve the step and recompute; a change in the integer matrix means the path was unresolved
Principle 4's contrapositive is the useful one here: a root of the leading symbol contributes nothing to the monodromy if its local monodromy is trivial, so the count of singular points is not the count of generators. That is checkable from the local exponents before any numerics are run.
### The monodromy group is readable without numerics at all
Computing the indicial equation of the s₇ and s₁₀ operators at every root of the leading symbol and at infinity:
Operator
z = 0
interior points
z = ∞
reading
s₇ = (13, 4, −27, 3)
0, 0, 0
z = −1: {0, ½, 1}; z = 1/27: {0, ½, 1}
{⅔, 1, ⁴⁄₃}
1 cusp, 2 elliptic points of order 2, 1 of order 3
s₁₀ = (6, 2, −64, 4)
0, 0, 0
z = −¼: {0, ½, 1}; z = 1/16: {0, ½, 1}
{¾, 1, ⁵⁄₄}
1 cusp, 2 elliptic points of order 2, 1 of order 4
None is apparent. Reading the exponents at infinity through the Sym² structure {2α, α+β, 2β} gives L₂ exponents {⅓, ⅔} for s₇ (difference ⅓) and {⅜, ⅝} for s₁₀ (difference ¼), which is where the orders 3 and 4 come from.
These signatures are matched by Gauss–Bonnet against exactly one group each:
- 
Γ₀(7)+7. Index 8, area 8π/3, halved to 4π/3. Then 2π[−2 + (½ + ½ + ⅔) + 1] = 4π/3. Matches. N = 7 is confirmed from the operator alone.
- 
Γ₀(10)+ — the full Atkin–Lehner group of order 4, not Γ₀(10)+10. Index 18, area 6π, quartered to 3π/2. Then 2π[−2 + (½ + ½ + ¾) + 1] = 3π/2. Matches, while Γ₀(10)+10 (area 3π) does not. So s₁₀ has three Atkin–Lehner involutions, and W₁₀ is only one of them.
This is the Tier B item closed without Stream 2: the monodromy group follows from indicial equations, which are polynomial root computations, not numerics. Certified numerical continuation remains worth building, but it is now a cross-check rather than the critical path.
### The correction this forces
The two order-2 points of Γ₀(7)+7 are the two fixed points of W₇, and they select different surfaces:
W₇ fixed point
algebraic class v
v²
T
det
CM disc
h
τ = i/√7
(1, −1, 0)
−2
⟨2⟩ ⊕ ⟨14⟩
28
−28
1
τ with 7τ² + 7τ + 2 = 0
(−2, 4, 1)
−2
[[2,1],[1,4]]
7
−7
1
Both are (−2)-classes, both have class number 1 and are defined over Q, and the second has the smaller determinant. So "the Fricke fixed point" is a selector only when W_N has one fixed point, which happens for N = 1 and fails whenever N ≡ 3 mod 4. This is the third time the same gap has appeared — after height versus discriminant at N = 1, and order 2 versus order 3 at N = 1 — and it is the same gap each time: no quantity has been named as the one being extremised.
### The control design, applied
The paper's pre-registration template is the instrument for closing that gap, and it ports directly:
- 
Arm V. Impose the arithmetic label: evaluate the observable at the rank-20 CM point. Correctness checked as in Principle 1 — the reader returns the lattice that was imposed.
- 
Arm P. Impose the same surplus non-topologically: a nearby non-CM point matched by bisection to machine precision on every continuous quantity the model has (period, metric, volume), with no rank jump.
- 
Arm 0. The generic point, untouched.
- 
Effect size. Effect per unit of surplus. A large effect in V and a small one in P for the same surplus is the signature that the rank jump, not the location in moduli, is doing the work.
- 
Kill rule. If V and P cannot be matched, no claim.
That design answers the question the programme has been unable to answer by inspection: whether an attractor point is special because of its arithmetic or merely because of where it sits. It is also the honest reason the earlier selectors disagree — none of them has been run against a matched control.
## Proposed experiments: the Brownian-motion criterion
Einstein's 1905 move was not a new instrument. He noticed that a humble, existing phenomenon already carried the signature of the hypothesis — in its fluctuations, not its mean flow — and supplied a formula with no free parameter that turned the observation into a measurement of a constant. Perrin then measured Avogadro's number with pollen. The local dual-scale hypothesis admits a test of exactly that shape in three laboratory systems, and in none of the sky.
### Why the cosmological version could never have had a Perrin experiment
The Brownian formula ⟨x²⟩ = 2Dt, D = k_BT/6πηa closes because the pollen grain and the water molecules are in equilibrium with each other: fluctuation–dissipation ties the macroscopic observable to the microscopic constant. The cosmological dual-scale identification α′ = ℓ_P c/H₀ had no such closure. Nothing relates the Planck length to the Hubble radius except the hypothesis itself, so every observable derived from it was a free assertion, and Paper 11 records that all four were excluded or unreachable. "Local" means the opposite situation: a system in which the duality ℓ ↦ s²/ℓ is a theorem of the model, so the self-dual scale s and every ratio at it are fixed numbers before any measurement.
### The template is Kramers–Wannier, not string theory
Kramers and Wannier (1941) fixed the Ising critical temperature exactly, T_c = 2J/ln(1+√2), from duality alone: if the model is self-dual under K ↔ K* and has one transition, the transition sits at the self-dual point. That is the whole logical content of a local dual-scale hypothesis, stated once and for all:
In a system with UV scale a and IR scale L that is exactly self-dual under ℓ ↦ aL/ℓ, any unique transition occurs at ℓ = √(aL), and every observable is a symmetric function of log(ℓ/ℓ).**
The first clause is what the programme has been calling the geometric-mean self-dual length. The second is the falsifiable part, and it has two levels.
### The universal prediction, in two moments
First moment (means). An observable measured on the two sides of the self-dual point at equal |log(ℓ/ℓ*)| takes dual values. This has been seen: at the superconductor–insulator transition in InOₓ films, the current–voltage curve on one side is the voltage–current curve on the other (Breznay, Steiner, Kivelson, Kapitulnik, PNAS 2016), the exchange being I ↔ V/R_Q with R_Q = h/(2e)² = 6453.20 Ω.
Second moment (fluctuations — the Brownian level). If the duality is a symmetry of the theory and not an accident of a scaling function, it maps the full distribution of the dual pair (X, X̃), hence every correlation function. The second moments (S_XX, S_XX̃, S_X̃X̃) then transform in the symmetric square of the duality's rank-2 action — the same Sym² that the programme has proved at the operator level — and at the self-dual point:`
No free parameter enters. A system whose means reflect but whose noise does not is not self-dual; it merely has a symmetric scaling function. That distinction is the experiment.
### An exact anchor, computed here
The Aubry–André model — hopping J on a lattice with an incommensurate potential of strength λ — is exactly self-dual under λ ↦ 4J²/λ, which exchanges the position and momentum lattices. Verified numerically on 987 sites: the two couplings multiply to (2J)²; the dual spectrum satisfies E′ = (2J/λ)E to 10⁻¹²; and at the self-dual point λ = 2J every eigenstate has position IPR equal to momentum IPR to 10⁻⁹. This is a second-moment duality in an exactly solvable model, it has been realised in cold atoms (Roati et al., Nature 2008) and photonic lattices, and the self-dual point λ/J = 2 is a pure number. It is the calibration arm.
### Three experiments, ranked by what they would settle
#
System
Exact duality
Self-dual point
Parameter-free prediction
Status
Arm P (matched control)
E1
Cold atoms or photonic waveguides in a bichromatic lattice
Aubry–André, position ↔ momentum
λ = 2J
IPR_x = IPR_k for every state; localisation lengths obey ξ(λ) = ξ̃(4J²/λ)
transition observed 2008; second-moment test not isolated
same λ, random (non-quasiperiodic) potential of matched strength: Anderson, no duality
E2
2D superconductor–insulator transition (InOₓ, TiN, gated oxide interfaces, tunable Josephson arrays)
charge ↔ vortex, 2e ↔ h/2e
R□ = h/(2e)² = 6453 Ω, i.e. σ = i
current shot noise at g equals voltage (phase-slip) noise at the dual g′ divided by R_Q²; Fano factors map with 2e ↔ h/2e
means reflect (2016); noise reflection untested
a pair of non-dual points with matched resistance: same dissipation, no duality
E3
Self-dual superconducting circuit: Josephson junction with a quantum-phase-slip junction at E_J = E_S
Mooij–Nazarov flux ↔ charge
E_J = E_S
charge dispersion in units of E_S equals flux dispersion in units of E_J; Shapiro voltage over dual-Shapiro current equals R_Q exactly (metrological closure of h and e in one device)
dual Shapiro steps I = 2ef observed (Nature 2022); self-dual circuit not built
JJ and QPSJ with E_J ≠ E_S but matched total energy
E4
Longitudinal and Hall conductivity flow at the SIT in a field, and at quantum Hall plateau transitions
modular Γ₀(2) on σ = σ_xy + iσ_xx
σ = i (SIT), σ = (1+i)/2 (QHE, 19.37 μS each)
flow lines are semicircles; the fixed points are these two CM points and no others
QHE semicircle law observed (1999); SIT flow diagram less complete
same materials, flow lines away from the critical semicircle
E2 is the Brownian experiment. The mean-level duality is established; the noise-level duality is the sharper claim, it is where the Sym² lives, and its failure would be as informative as its success — it would show the dirty-boson critical point is not self-dual, which is an open question in its own right. E3 is the closure test: the ratio of the Josephson voltage step to the dual current step is a fundamental constant, and self-duality is the statement that one device produces both.
### The protocol, frozen before any run
Each experiment carries the Arm V / Arm P / Arm 0 design of the U(1) paper. Arm V is the dual pair or the self-dual point; Arm P is a pair matched on every continuous quantity (resistance, dissipation, total energy) but not related by the duality; Arm 0 is the untouched generic point. Effect size is the reflection residual per unit of matched quantity. Kill rule: if Arm P reproduces the reflection as well as Arm V, the duality claim is dead and the reflection is a property of the scaling function, not of a symmetry. Decision rules, thresholds and the disclosed prior knowledge (the 2016 and 2022 results are known) go under a git tag before the first measurement.
### The observational element, stated plainly
There is none. No astrophysical system is known to be exactly self-dual. The three settings of the U(1) paper — cosmic and axion strings, neutron-star superfluids, condensate haloes — carry a topological charge but no duality, and Paper 11 has already closed the cosmological identification. A local dual-scale hypothesis is laboratory physics. Saying so is the difference between this proposal and the specification.
### What this does and does not do for the K3 selection
The self-dual points these experiments would locate — σ = i at the SIT, σ = (1+i)/2 at the plateau transition — are CM points of discriminant −4. Through the Sym² chain they attach to the surface with T = ⟨2⟩ ⊕ ⟨2⟩, X₄ = Inose(Eᵢ × Eᵢ). The experiments test the duality; the K3 is its mathematical shadow, and no measurement here touches the surface itself. That is the correct relation between the two, and it is the one the specification inverted.
## Proposed K3 criteria
A K3 selection is admissible in this programme when it passes all eight conditions below. The current spec passes none of C1–C4 and C6–C8; it passes C5 only for χ, b₂ and the signature.
- 
Name the selector. State which physics picks the surface (attractor charges, sigma-model symmetry, field of definition) and derive the surface from that input alone. "M₂₄" is not a selector, because the elliptic genus is the same for every K3 (GHV 2011).
- 
State the lattice pair (NS, T). T must be even, positive-definite, of rank 22 − ρ; for ρ = 20 give the binary form and check disc(NS) = −disc(T). Respect Nikulin's bound of 16 disjoint (−2)-curves. A rank-20 surface has no complex-structure modulus, so no Picard–Fuchs operator is attached to it; if a family is meant, say which fibre is selected.
- 
Give a model whose invariants are finite computations. A Weierstrass form with deg a₄ ≤ 8, deg a₆ ≤ 12; fibre types from the orders of a₄, a₆, Δ; Euler numbers summing to 24; ρ = 2 + Σ(m_v − 1) + rank MW. Each is a Tier A target in the existing toolchain.
- 
Twine every integer before reading it as physics. Paper 10's forger's test is the standard: 24 passes, 462/360 fails. No integer that fails may appear in a predictions table.
- 
Derive error bars, do not type them. An observable that depends on an unfixed quantity (N_e, the α of the Kähler potential, a loop order) is reported as a range over that quantity with the dependence shown. "±0.00015" on r with N_e ∈ [50, 60] is an example of what this forbids.
- 
Freeze by tag before comparison. Every observable derived from the surface follows the Paper 11 protocol: statement, inputs, decision rule and disclosure of prior knowledge committed under a git tag, verdict computed in Lean against pinned data. A predictions table without tags is not a predictions table.
- 
Chirality gate. No fermion-generation, Yukawa, PMNS or δ_CP claim from K3 × T² until a chiral construction (K3-fibred Calabi–Yau threefold, or orientifold plus flux) is written down and its N = 1 spectrum computed. Modular-flavour numbers evaluated at τ = i or τ = ω additionally face the CP-conservation result of Novichkov–Penedo–Petcov–Titov at those points.
- 
Tier label on every line. Tier A (kernel), Tier L (literature, pinned by file and line range), Tier C (reading). A specification that carries no labels is not admissible in the programme's own terms, whatever its content.
Two further rules follow from what went wrong here rather than from the papers. A number that appears in a headline (10⁻¹²², three generations, 23) must be recomputed from its formula by someone other than its author before it is typeset; the Λ line would have failed in thirty seconds. And a claim about a group ("the 24 branches as …") is checked by constructing the group, which SymPy does for M₂₄ from four permutations in under a minute.
## Edits required in the spec
In order of how quickly a referee would find each.
- 
§2.1: remove the Λ derivation. No exponent built from M₂₄ data gives 10⁻¹²², and Paper 11 has already excluded the Hubble-scale dark-energy reading. If a Λ section stays, it says so.
- 
§2.3: replace the branching with the true one (24 = 8·1 ⊕ 2·1′ ⊕ 2·1″ ⊕ 4·3 for A₄ ⊂ M₂₂; 6·1 ⊕ 6·3 or 4·1 ⊕ 4·1′ ⊕ 4·1″ ⊕ 4·3 for the other embeddings) or remove the generation claim; remove δ_CP and Σm_ν (0.059 eV is the normal-ordering floor, not a prediction).
- 
§3.3 A–C: replace with the Inose model of X₃ (or X₄, with a reason), its fibre table, NS and T. Delete the 24-node Kummer and the non-homogeneous quartic. For the Picard–Fuchs row, substitute the repository's own s₇ operator (a,b,c,d) = (13, 4, −27, 3), which is a verified symmetric square and has exactly the claimed singular points 0, 1/27, −1, ∞; the operator currently printed fails the Sym² criterion. State ρ = 19 generically, 20 at the Fricke point.
- 
§3.4: replace τ* = i by τ = ω, or justify D = −4 over the D = −3 floor; replace "20 Kähler + 38 complex structure" by 57 + 1.
- 
§3.5: relabel χ(g) as the cycle count ℓ(g) of the frame shape.
- 
§3.6: correct the leading power to q^{−1700/24}; drop the a(1) = −χ(K3) reading and c_eff = −1698; state that the quotient is not a Γ₀(12) form.
- 
§4 table: delete R_NL = 462/360 (Paper 10 Thm 4.1). For every remaining row give a source file and a freeze tag or move the row to a Tier C list: the TDA Euler peak, b₂ = 22 in clustering, 4.038 GHz, ARCADE/EDGES, the Golay-code line (the correct home for the last is Harvey–Moore's hexacode construction at the GTVW point, which is not M₂₄).
- 
§2.2 and §5: state α; give r as a range over N_e (0.0033–0.0048 for α = 1, 0.0011–0.0016 for α = 1/3) and note that LiteBIRD's σ(r) ≈ 0.001 separates the two; check n_s against ACT DR6, whose P-ACT-LB value 0.9743 ± 0.0034 puts the Starobinsky-class 0.964 at roughly 3σ; remove the ±0.00015.
- 
§1.3 and §3.4: remove MICROSCOPE, GW170817 and α̇/α as consequences; a modulus of mass 10¹³ GeV decouples trivially and the exponent e^{−m/H₀} is not a physical quantity.
- 
§3.1: remove the anomaly sentence.
- 
§3.2: replace "Δ = 2n" by the correct statement (any integer of the form 4ac − b²; floor 3) and drop Mₙ = √(2n) M_Pl.
- 
Throughout: add tier labels, and reconcile every sentence with Papers 10–12 before circulation.
## Sources
Computations in this review are mine (SymPy, this session); the programme's results are quoted from the four attached papers. Literature identifiers below are from memory and should be pinned in papers/foundations/ before citation, per the programme's own rule; the two ACT items were opened in this session.
- 
Papers 10, 11, 12 and the T-duality manuscript (attached, September 2026).
- 
G. Moore, Arithmetic and Attractors, hep-th/9807087.
- 
E. Vinberg, The two most algebraic K3 surfaces, Math. Ann. 265 (1983) 1–21.
- 
T. Shioda, H. Inose, On singular K3 surfaces (1977); H. Inose, Defining equations of singular K3 surfaces and a notion of isogeny (1978); T. Shioda, Kummer sandwich theorem of certain elliptic K3 surfaces, Proc. Japan Acad. 82 (2006).
- 
V. Nikulin, Kummer surfaces, Izv. Akad. Nauk SSSR 39 (1975).
- 
S. Mukai, Finite groups of automorphisms of K3 surfaces and the Mathieu group, Invent. Math. 94 (1988).
- 
M. Schütt, Fields of definition of singular K3 surfaces, math/0612396; K3 surfaces with Picard rank 20 over Q, 0804.1558.
- 
M. Gaberdiel, S. Hohenegger, R. Volpato, Symmetries of K3 sigma models, 1106.4315.
- 
M. Gaberdiel, A. Taormina, R. Volpato, K. Wendland, A K3 sigma model with Z₂⁸:M₂₀ symmetry, 1309.4127.
- 
J. Harvey, G. Moore, Moonshine, superconformal symmetry, and quantum error correction, 2003.13700.
- 
M. Gaberdiel, D. Persson, H. Ronellenfitsch, R. Volpato, Generalised Mathieu moonshine, 1211.7025; M. Dutour Sikirić, G. Ellis, Wythoff polytopes and low-dimensional homology of Mathieu groups, J. Algebra 322 (2009).
- 
P. Novichkov, J. Penedo, S. Petcov, A. Titov, Generalised CP symmetry in modular-invariant models of flavour, 1905.11970.
- 
G. Almkvist, C. van Enckevort, D. van Straten, W. Zudilin, Tables of Calabi–Yau equations, math/0507430.
- 
ACT Collaboration, DR6 ΛCDM and extended-model constraints, act.princeton.edu; Refined predictions for Starobinsky inflation in light of ACT, 2504.20757.
