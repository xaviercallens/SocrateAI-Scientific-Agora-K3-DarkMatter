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
