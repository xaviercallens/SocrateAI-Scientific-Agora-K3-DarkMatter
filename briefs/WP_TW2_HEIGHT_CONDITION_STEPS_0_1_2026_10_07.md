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
