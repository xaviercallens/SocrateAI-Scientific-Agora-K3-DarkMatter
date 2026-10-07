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
