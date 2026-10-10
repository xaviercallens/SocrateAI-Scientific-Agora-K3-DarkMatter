# WP-TW2 — the M₇-polarization constraint on the twisted-Weierstrass route: steps 0 and 1 (2026-10-07)

**Opened by:** D20′ (`briefs/T0_DECISIONS_2026_10_07_STREAM2_DELEGATED.md`). **Checker:**
`checkers/check_TW2_height_condition.py` (+ `checkers/test_TW2_height_condition_controls.py`, 9 controls);
certificate `data/certificates/TW2_HEIGHT_CONDITION.json`. **Language:** lattices, Tate orders, discriminant-root
orders, heights. No Kodaira label (ledger items 3, 10); no physics (item 4).

## 0. The question

WP-TW1 (LIVE, D20′) says a Weierstrass model with two E8-root loci is degree-feasible on P¹×P² and the
P¹-bundles over P². It says nothing about whether such a model can carry the **M₇-polarization** — the whole
content of "this is the cooper_s7 family". WP-TW2 asks what the polarization forces on the model.

## 1. Step 0 — the lattice constraint (exact; `height_condition(7)`)

On an elliptic K3 with section, two fibres of E8 root type (each m_v − 1 = 8, det 1, unique simple component) give
trivial lattice U ⊕ E8² of rank 18 and determinant −1. For ρ = 19 (Tier B, E-011), Shioda–Tate (Schütt–Shioda
Cor. 6.13, read) forces Mordell–Weil rank 1; with generator P, NS ≅ U ⊕ E8² ⊕ ⟨−h(P)⟩ and
disc NS = −disc(T_triv)·h(P) = h(P) (eq. 23, read). M₇ = U ⊕ E8² ⊕ ⟨−14⟩ (Dolgachev 1996 §7, pinned) forces
**h(P) = 14**. The height formula (Thm 11.5, read) with χ(O_K3) = 2 and no correction terms (both fibres have a
unique simple component, Table 4) gives

> **P̄·Ō = (h(P) − 2χ)/2 = n − 2 = 5.**

Any Weierstrass model realizing the M₇-polarization with two E8-root fibres carries a section meeting the zero
section in exactly five points (with multiplicity). For the s10 register the same formula gives 8. Controls: one
E8 fibre → MW rank 9, not the M_n shape; E7+E8 → not the M_n shape; χ = 1 → 6 (rational surface, wrong); a
non-identity contact with correction 3/2 → parity breaks, refused; ρ below trivial rank → refused. Cross-check
against the explicit M₇ model: `INOSE_FIBRATION_MULTIPLICITIES.json` records two discriminant roots of order 10 at
each s7 locus — two E8-root fibres, as assumed.

## 2. Step 1 — the same number from the literature side (read, pinned today)

Kumar–Kuwata (arXiv:1409.2931, **Prop. 3.1**, citing Shioda): for E₁ ≇ E₂ the Mordell–Weil lattice of the Inose
surface F⁽¹⁾ — the fibration with two E8-root fibres and four simple discriminant roots, i.e. our J9/Kuwata–Shioda
model — is **Hom(E₁, E₂)⟨2⟩**: the section attached to an isogeny φ has height **2·deg φ**. Shioda (MPIM 2007-137,
l.700, 759) states the same scaling and contrasts it with the Kummer pencil (norm deg φ; KS Example 1.1, l.159–163).

For the cooper_s7 family the Shioda–Inose partner is E₁ × E₂ with a **7-isogeny** (level 7, `C2_cooper_s7_v6`,
T ≅ U ⊕ ⟨14⟩), so the generator has height 2·7 = 14 and P̄·Ō = 5 — **the step-0 number, reached without
Shioda–Tate.** Two independent routes, one answer. Step 1 also supplies the construction recipe: KK **Prop. 3.2**
builds the section from φ = (φ_x, φ_y·y₁) through the base change t₁ = t₆⁶ and the divisor φ_y(x₁) = ±t₆³ on the
cubic (3.1); P⁺_φ − P⁻_φ descends to F⁽¹⁾ with height 2d.

**Caveat, stated once:** Prop. 3.1's hypothesis is E₁ ≇ E₂. The AM-8-selected point of s7 (z = ∞, T = A₂, j = 0)
has E₁ ≅ E₂, so it sits *outside* the proposition; KK refer that case to Kuwata [Kw2, Th. 4.1] (not fetched). The
constraint P̄·Ō = 5 is nonetheless forced at every ρ = 19 member by step 0 alone.

## 3. Step 2 — design only (not executed)

Exhibit the section explicitly on the pinned J9 model at a locus where E₁, E₂ are defined over Q and 7-isogenous:
the ρ = 20 loci z = −1 and z = 1/27 have class-number-1 discriminants (−28, −7; `CM_POINTS_RHO20.json`), so E₁, E₂
and a degree-7 isogeny are explicit (Vélu over Q or a quadratic field). Then: (a) φ_x, φ_y exactly; (b) KK (3.1)–(3.3)
to get D⁺_φ, D⁻_φ on F⁽⁶⁾; (c) descend to F⁽¹⁾ and read P̄·Ō from the pole order of the x-coordinate — must be 5;
(d) height 14 by the height formula with the fibre contacts computed, not assumed. Negative control: the same
pipeline with a degree-d′ ≠ 7 isogeny (or at a non-isogenous pair) must give P̄·Ō = d′ − 2 (or no section). A
first exact computation of a degree-7 **endomorphism** at the j = 0 point (α = 3 + 2ω, N(α) = 7) was started as a
scratch; it is the isomorphic case the proposition excludes and is recorded only as a tool, not a result.

## 4. What this changes for the twisted-Weierstrass route

Nothing is opened or closed at the level of bases. The route now has a **second necessary condition** beyond
TW1's degree budget: the Weierstrass data on any candidate B₃ must restrict, on the K3 fibres, to a model carrying
a rank-1 Mordell–Weil generator with P̄·Ō = 5 (height 14). This is checkable on a candidate (f, g) before any
attempt at the full construction — and it is the first place the route can honestly die.

*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: the certificate and its 9 controls; the pinned,
read sources named per step (lines cited in `docs/literature/MANIFEST.md`) | Reviewed-by: N*

---

## 5. Step 2a (D23′, same day) — the three ρ = 20 loci, exactly (`checkers/check_TW2_rho20_loci.py`, `TW2_RHO20_LOCI.json`)

At every ρ = 20 locus the Shioda–Inose partner has E₁ ≅ E₂ (the T forms (1,1,2), (1,0,7), (1,1,1) are the norm forms
of End(E) for the orders of discriminant −7, −28, −3), so Prop. 3.1 of Kumar–Kuwata does not apply and the extra
discriminant root recorded in `INOSE_FIBRATION_MULTIPLICITIES.json` changes the bookkeeping. With the trivial lattice
U ⊕ E8² ⊕ R, Shioda–Tate, |disc NS| = |disc T| = |disc T_triv|·disc(MWL) (eq. 22, torsion-free by Shioda's Lemma 6.2
for n = 1) and the height formula with Table-4 corrections, each locus resolves **uniquely**:

| locus | D | |disc T| | extra root (order → root lattice) | MW rank | height | P̄·Ō |
|---|---|---|---|---|---|---|
| z = −1 | −7 | 7 | 2 → A₁ (pulled-back simple root of d(u) at u = 0) | 1 | **7/2** | **0**, meeting the non-identity component (contr ½) |
| z = 1/27 | −28 | 28 | 2 → A₁ | 1 | **14** | **5** (contr 0) |
| z = ∞ (AM-8 selected) | −3 | 3 | 4 → A₂ (rank 2 forced by ρ = 20) | **0** | — | **no section**: NS = U ⊕ E8² ⊕ A₂ |

Controls: swapping the two T forms swaps the answers (data-driven, not typed); ρ = 19 at a ρ = 20 locus is refused;
|disc T| = 3 with an A₁ root is refused (no admissible P̄·Ō); an order-4 root with |disc T| ≠ 3 is refused; reading
the order-2 root as rank 0 changes the Mordell–Weil rank to 2; three order-10 roots are refused.

**What this does to the TW2 constraint.** "P̄·Ō = 5" is the requirement at every ρ = 19 member and at z = 1/27. It is
**not** the requirement at the selected point: the Weierstrass model of the AM-8 K3 (z = ∞, T = A₂) has **no**
Mordell–Weil section at all — its extra Picard classes are the two components of an A₂ root fibre over an order-4
discriminant root. A twisted-Weierstrass construction aimed at the selected K3 must therefore produce, on that
fibre, a discriminant root of order 4 carrying an A₂ root lattice, in addition to the two order-10 roots. At z = −1
the generator instead has height 7/2 and meets the zero section nowhere (P̄·Ō = 0), passing through the non-identity
component of the A₁ fibre. Lattice and discriminant-order language only; no fibre type is named (items 3, 10).

**Step 2b stays deferred:** the explicit section at z = 1/27 (E ≅ E with End of discriminant −28, φ = √−7 of degree 7)
is the natural target; it needs Kuwata [Kw2, Th. 4.1] or a direct Vélu + Kumar–Kuwata (3.1)–(3.3) computation.

---

## 6. Step 2b-i (D23′, same day) — the degree-7 endomorphism at z = 1/27, exhibited exactly (`checkers/check_TW2_sqrt_m7_endomorphism.py`, `TW2_SQRT_M7_ENDOMORPHISM.json`)

At z = 1/27 the rank-1 generator of step 2a (h = 14, P̄·Ō = 5) is, by Kumar–Kuwata/Shioda, the section attached to
the degree-7 endomorphism √−7 of E, End(E) = Z[√−7], j = 16581375 (read from the fibration certificate). That
endomorphism is now written down over Q:

- model (minimal twist of A = 3j(1728−j), B = 2j(1728−j)²): y² = x³ − 1551893875 x + 23529814932750;
- ψ₇ (degree 24) factors over Q as (cubic)·(degree 21); the cubic — the kernel of √−7 — is
  x³ − 101745 x² + 3158560475 x − 30989768789875;
- Vélu (exact symmetric-function form): φ_x of degree 7 with denominator h², codomain (49A, −343B) ≅ E via
  c² = −1/7 (so √−7 is defined over Q(√−7), its x-map over Q);
- **proof of φ∘φ = [−7] on x-coordinates:** ψ(ψ(x₀)) = x([7]P)(x₀) exactly at 60 random rational points, for
  rational functions of degree ≤ 49 — hence identically. Controls: the wrong sign of c² fails everywhere (this was
  caught live as a slip), the multiplier 5 fails, a random cubic gives a codomain with a different j, a non-CM
  curve has no rational cubic factor of ψ₇, j ∈ {0, 1728} is refused.

What remains for a complete step 2b (**2b-ii, not done**): push the graph of √−7 through Kumar–Kuwata (3.1)–(3.3)
to a section of F⁽⁶⁾, descend to F⁽¹⁾, change coordinates to the pinned Kuwata–Shioda J9 model, and read off
P̄·Ō = 5 and h = 14 with the A₁-fibre contact computed (step 2a predicts contr = 0 at this locus). That is a
long but now fully specified computation; every input to it is on disk.

**§5 addendum (model-side confirmation, same day).** The z = ∞ reading is now also checked on the explicit model:
with l₁ = l₂ = λ, λ² − λ + 1 = 0, the cubic x³ + a₂x² + a₄x + a₆ at s = 0 has a **triple root** (x = λ) and
v_s(Δ) = 4 with a₂, a₄, a₆ all non-vanishing — an additive degeneration whose root lattice has rank e − 2 = 2. The
lattice-forced A₂ and the model agree (`model_check_z_infinity` in `TW2_RHO20_LOCI.json`; control P2).

**§5 addendum 2 (2026-10-08, D25′) — all three loci model-confirmed.** Reducing the pinned model's coefficients
exactly modulo the λ minimal polynomial m_J(λ) = 4(λ²−λ+1)³ − 27Jλ²(λ−1)² (no root chosen): at z = −1 and
z = 1/27 the cubic at s = 0 has a **double root** with v_s(Δ) = 2 (node → root-lattice rank 1, A₁); at z = ∞ a
**triple root** with v_s(Δ) = 4 (rank 2, A₂). Every lattice-forced reading of the table above is reproduced by the
explicit model (`model_checks` in `TW2_RHO20_LOCI.json`; controls P2, N7). The certificate also carries the three
**specialized Weierstrass models** (a₂, a₄, a₆ reduced mod m_J) — the concrete input for step 2b-ii.

---

## 7. Step 2b-i completed (2026-10-08): the full map of curves, and a dated precision correction

**Correction (standing rule 3).** §6 above says "φ∘φ = [−7] proved" from the x-coordinate identity. An identity of
x-coordinates proves only **φ∘φ = ±[7]**. The sign is fixed by structure, not by the sampled identity: the locus
z = 1/27 is a CM point of discriminant D = −28 (read from `CM_POINTS_RHO20.json`), so End(E)⊗ℚ is an imaginary
quadratic field, in which no element squares to +7 — hence φ∘φ = [−7] (Tier B; recorded as `sign_of_square` in the
certificate). The earlier statement stands with that qualifier.

**New (exact, no sampling).** `y_map_check` in `check_TW2_sqrt_m7_endomorphism.py` verifies, as an identity of rational
functions, that Vélu's map (x, y) ↦ (φ_x, y·φ_x′) composed with the isomorphism (X, Y) ↦ (c²X, c³Y), c³² = c²³ = −1/343,
is a morphism E → E: c³²·φ_x′(x)²·f(x) = (c²φ_x)³ + A(c²φ_x) + B. The map is defined over ℚ(√−7) (c³ = ±√−7/49) while
its x-part is defined over ℚ. Then φ_y(x) = c³·φ_x′(x) has numerator and denominator of degree 9, coprime, with
denominator h³ — so φ_y(x₁) = ±t³ has degree **9 = (3d − 3)/2** for d = 7, exactly the count in Kumar–Kuwata
Prop. 3.2(i). Controls (12 in all): wrong c³², wrong isomorphism constant, and the x-map of a kernel cubic off by
one are all refused by the y-identity.

**What this unlocks and what remains.** Everything Prop. 3.2 asks of φ is now explicit: the endomorphism over
ℚ(√−7), the nine points of D⁺_φ as the roots of a degree-9 polynomial in x₁ for each t₆, and the cubic (3.1). The
remaining step 2b-ii is the computation in Pic⁰ of that cubic over ℚ(√−7)(t₆) — reducing D⁺_φ − 9·O to a single
point Q⁺ — and the descent to F⁽¹⁾; it is a function-field computation (resultants/Riemann–Roch over ℚ(√−7)(t)),
not yet attempted.

---

## 8. Step 2b-ii (2026-10-10) — the section is built, descended and read: P̄·Ō = 5, contr = 0, h = 14
(`checkers/check_TW2_section_descent.py`, `TW2_SECTION_DESCENT.json`, 14 controls in `test_TW2_section_descent_controls.py`)

**Inputs verified before execution (standing rule 4).** This brief's §6; the kernel cubic, Vélu map and codomain of step 2b-i;
Kumar–Kuwata (pinned text) l.460–548 for (3.1)–(3.3) and Prop. 3.2, and l.296–303 for the simple normal form of F⁽¹⁾. The
"pinned J9 model" is Kuwata–Shioda's pencil already transcribed in `check_inose_fibration_multiplicities.py`; here it appears as
`Y² = X³ − 3α t⁴ X + t⁵(t² − 2β t + 1)`, the same pencil as Stream 1's open question 6.

**What was computed (exact, no floats).**
1. The cubic C_t of (3.1) with E₁ = (A, B), E₂ = (A₂, B₂) (the Vélu codomain). With s = x₂ − t²x₁ it is quadratic in x₁; its
   discriminant is a quartic with the rational point O = (s, w) = (0, q). Mordell's map gives a Weierstrass model E_t. The map
   is **verified by identity on the actual nine divisor points** (an exact check in the residue field), and j(E_t) is verified
   against the quartic's own invariants I, J.
2. D^± = the nine points with φ_y(x₁) = ±t³ (roots of a degree-9 polynomial, as Prop. 3.2(i) predicts). Q^± is found by
   Riemann–Roch: the unique g in L(10·O) vanishing on D^± has a tenth zero R, and Q = −R. The norm identity N(x) = c·Nm(x)·(x − X_R)
   holds exactly.
3. P(t) = Q⁺ − Q⁻ on E_t, mapped to the simple normal form. **Normalization is calibrated, then asserted:** E_t matches
   `Y² = X³ − 3αX + (t_s + 1/t_s − 2β)` exactly in j with α = (J₁J₂)^{1/3} = 7225/16, β = J − 1 and t_s = t⁶/343 (343 =
   √(Δ_E₁/Δ_E₂) is computed). The j-match and the twist constant are asserted at every one of the 52 specializations. The other
   branch (β = 1 − J, t_s = −t⁶/343) also matches in j; it is the quadratic twist by −1 (control N6).
4. X′(t_s) is reconstructed as N/D² from 44 specializations for **26 unknowns** (so over-determined by 18); the fit is unique
   (nullspace dimension 1), agrees at 8 held-out points, and Y′² is a constant square class (+1: the section is defined over ℚ on
   this branch) times a square in ℚ(t).

**Result.** deg N = 14 and D = (t + 1)·(quartic), degree 5.
- **P̄·Ō = 5**: the poles of X′ (a simple one at the A₁ node t = −1 and four at the roots of an irreducible quartic), none at
  t = 0 or ∞ (the two E₈ fibres).
- **contr = 0**: P meets O inside the A₁ fibre, so it lies on the identity component.
- **h = 2χ + 2·P̄·Ō − contr = 4 + 10 − 0 = 14**, which equals Kumar–Kuwata's 2·deg φ = 14, the lattice value of step 0 and the
  prediction of step 2a, all read from their certificates. The discriminant orders of the model, {10,10,2,1,1}, equal the
  fibration certificate's (the same surface).

**Not claimed.** That this section generates the whole Mordell–Weil group beyond height 14 (no index computation was made; the
lattice side forces rank 1 and height 14 and KK Prop. 3.2(ii) gives 2d, so the generator reading is the natural one, not a proof
here). Anything at z = −1 or z = ∞. Any Kodaira label (the A₁ is the root lattice of step 2a). Anything physical.

**Note, a robustness fact found by a control.** P̄·Ō is conserved when poles move to t = ∞: it equals (deg N − 4)/2 = 5 whatever
the denominator. So the quantity read here is determined by the degree of N together with the weight; the pole *locations* carry
the contact information (the A₁ contact above).

**What step 2 does not yet give.** The twisted-Weierstrass route's next gate is WP-TW3 (twist data over a threefold base), which no
T0 text specifies. It stays unopened.
