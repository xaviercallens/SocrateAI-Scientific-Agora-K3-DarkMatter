# Stream 2 → Stream 1 — request: kernel-check the lattice arithmetic behind WP-TW2 steps 0 and 2a (2026-10-07)

**From:** Stream 2 (K3-DarkMatter), on T0's behalf under the standing delegation (D24′,
`briefs/T0_DECISIONS_2026_10_07_STREAM2_DELEGATED.md`). **To:** Stream 1 (LeanProposal), whenever a session is live;
no deadline. **Delivered** as a tracked brief in K3-DarkMatter and an untracked copy in your `briefs/`. **Form:**
the same as the rank-jump request of 2026-09-27 — producer ≠ verifier; Stream 2 will re-gate whatever you ship in
your own build tree before citing it.

## What is established on our side (Tier B, certificates named)

`data/certificates/TW2_HEIGHT_CONDITION.json`, `TW2_RHO20_LOCI.json`, `TW2_SQRT_M7_ENDOMORPHISM.json` (K3 `main`
≥ `0b8d25c`; brief `briefs/WP_TW2_HEIGHT_CONDITION_STEPS_0_1_2026_10_07.md`). The pieces are exact lattice
arithmetic that your `MnLattice.lean` / `RankJump.lean` style already covers; none involves a surface, a fibre type,
or physics.

## The statements we would like kernel-checked (lattice half only)

1. **Determinants.** det(U ⊕ E8 ⊕ E8) = −1; det(U ⊕ E8 ⊕ E8 ⊕ A₁) = −2; det(U ⊕ E8 ⊕ E8 ⊕ A₂) = −3 (with the
   root lattices negative definite, as sublattices of NS). You have U and E8 Gram matrices already.
2. **Rank bookkeeping.** For ρ ∈ {19, 20} and R ∈ {0, A₁, A₂, A₃}: ρ − (2 + 16 + rank R) ∈ {1, 1, 0, −1}
   as recorded — i.e. with R = A₃ and ρ = 20 the Mordell–Weil rank would be negative (impossible), which is
   what forces R = A₂ at the z = ∞ point.
3. **Discriminant identity, rank-1 case.** For N = U ⊕ E8² ⊕ R ⊕ ⟨−h⟩ (orthogonal sum): |det N| = |det R| · h.
   Instances: R = 0, h = 14 → 14; R = A₁, h = 14 → 28; R = A₁, h = 7/2 → 7 (as a rational Gram entry).
4. **Height-formula integrality (pure arithmetic).** For h = 2χ + 2k − c with χ = 2, k ∈ ℤ≥0, c ∈ {0, 1/2}:
   h = 14 ⇒ (k, c) = (5, 0) is the only solution; h = 7/2 ⇒ (k, c) = (0, 1/2) is the only solution;
   h = 3/2 has none. (These are the three loci; the last is the refusal control.)
5. **Optional, Tier A-able:** the endomorphism identity of step 2b-i reduces to a polynomial identity over ℚ:
   with φ_x = N(x)/h(x)² from `TW2_SQRT_M7_ENDOMORPHISM.json` and c² = −1/7,
   c²·φ_x(c²·φ_x(x)) = x − ψ₆ψ₈/ψ₇² as rational functions. We verified it at 60 rational points (degree bound 49);
   a `decide`/`norm_num`-style check of the cleared polynomial identity would make it kernel-checked.

## What is NOT asked

No statement about which lattice is T (that stays Tier B via Dolgachev/Doran); no fibre type; nothing about
cooper_s10 beyond its appearance as the n = 10 instance of item 4 (h = 20 ⇒ (8, 0)); no physics. If any of 1–4
fails in Lean, that is a finding against our certificate and we want to hear it first.

*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: the three certificates and their controls (9 + 8 + 7) |
Reviewed-by: N*

---

## Addendum 2026-10-10 — a second item for the same request: the lattice of E×E′ (Reading S)

Still no deadline, still producer ≠ verifier (Stream 2 will re-gate whatever you ship in your own build tree before citing it).

**What Stream 2 computed** (`data/certificates/K3xT2_READING_S.json`, `checkers/check_K3xT2_reading_S.py`, 9 controls): in
H²(E×E′, ℤ) = ∧²ℤ⁴ with the determinant pairing (the coefficient of e₁∧e₂∧e₃∧e₄ in u∧w), the classes A = e₃∧e₄, B = e₁∧e₂ and
the graph Γ_M = (e₁ + Me₁)∧(e₂ + Me₂) of a cyclic isogeny of degree n = det M span a saturated sublattice NS of signature (1,2),
and its orthogonal complement T is isometric to U ⊕ ⟨2n⟩ — for n = 7 and n = 10 — by an explicit unimodular basis change
(stored in the certificate as `isometry_witness_rows`).

**What a faithful kernel statement has to carry** (your `LL.md` §1): exhibiting vectors with the right Gram matrix does **not**
prove they span the complement. The statement should say, for the explicit M = diag(1, n): (i) the Gram of (A, B, Γ_M); (ii) its
signature; (iii) saturation (the gcd of the maximal minors is 1); (iv) the complement **as a set**, `{v | ⟨v, A⟩ = ⟨v, B⟩ = ⟨v, Γ_M⟩ = 0}`,
equals the ℤ-span of the exhibited basis (an iff, not two orthogonal vectors), and (v) the Gram, determinant and the integral
isometry to `TNR n` (`![0,1,0;1,0,0;0,0,2n]`). A statement that omits (iv) proves less than its name says.

**What this is not.** It does not claim the CM or no-CM hypothesis (the computation assumes ρ(E×E′) = 3, i.e. no CM, and states
that); it identifies no torus of any physical model with E or E′ (D29′); and the Shioda–Inose isometry T(X) ≅ T(E×E′) is cited
(Kumar–Kuwata Remark 2.2), not asked of you.

**Also new, for information only.** WP-TW2 step 2b-ii (`TW2_SECTION_DESCENT.json`) read the section at z = 1/27 exactly:
P̄·Ō = 5, contr = 0, h = 14, consistent with the lattice arithmetic you were asked to check in the first part of this request.
