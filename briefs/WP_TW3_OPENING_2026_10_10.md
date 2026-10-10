# WP-TW3 opening — twist data on B₃ = P¹×P² and the first gate (2026-10-10)

Status: opened by D32′ (`T0_DECISIONS_2026_10_07_STREAM2_DELEGATED.md`). Tier B (exact arithmetic over the certificate's Tier B
inputs). Checker `checkers/check_TW3_twist_data_degrees.py`, certificate `data/certificates/TW3_TWIST_DATA_DEGREES.json`,
controls `checkers/test_TW3_twist_data_degrees_controls.py`.

## 1. Twist data (all from the certificate)

| Item | Value |
|---|---|
| Base B₃ | P¹×P², K = O(−2,−3), −K = O(2,3) |
| E8 divisors | D₁ = {0}×P², D₂ = {∞}×P², class (1,0) each; disjoint set-theoretically (product structure) |
| f ∈ H⁰(−4K) | bound O(8,12); need 4·(1,0)+4·(1,0) = (8,0); residual f′ ∈ O(0,12), h⁰ = 91 |
| g ∈ H⁰(−6K) | bound O(12,18); need (10,0); residual g′ ∈ O(2,18), h⁰ = 570 |
| Δ | bound O(24,36); need (20,0); margin (4,36) |

The margins equal those of the TW1 certificate `TW1_two_e8_P1xP2.json` (read, not retyped). The residual f′ restricts to O(12) on
each divisor, so the exact Tate order is realized by a generic section.

The fibre over y ∈ P² is the pencil Y² = X³ + f′(y) t⁴ X + t⁵ (c(y) t² + b(y) t + a(y)) with f′ ∈ O(12) and a, b, c ∈ O(18) on P².
Its invariants are α³ = −f′³/(27 a c) and β² = b²/(4 a c) (scaling t → μt, X → ν²X; the derivation is re-verified on six
exact rational instances).

## 2. Gate TW3-G2 (necessary condition, then exact constructions)

M₇-polarized fibres require (α³, β²) = (π(z), π(z) − σ(z) + 1) at z = z(y) = u/v, with u, v forms of degree e on P². From
`INOSE_MODEL_M7.json`:

- π = (1/2985984) (448z² + 224z + 1)³ / z⁸
- π − σ + 1 = (1/2985984) (1728z⁴ + 5120z³ + 9024z² + 528z − 1)² / z⁸

Minimal vanishing order x = ord(a) + ord(c) forced along each special component, with ord f′, ord b ≥ 0 and the cube/square
conditions: **x = 8 along {u = 0}, x = 4 along {v = 0}**, and 0 elsewhere. Summing over the degree-e curves gives
12 e ≤ deg(ac) = 36, so **e ≤ 3**. The cases e = 1, 2, 3 are each built explicitly (an auxiliary form of degree 4, 2, 0) with
deg f′ = deg a = deg b = deg c exactly as above, and both identities α³ = π∘z and β² = (π−σ+1)∘z hold **as exact polynomial
identities** in y₀, y₁, y₂; each is cross-checked at three rational points. e = 4 is refused.

## 3. What this does not do

- It does not show the Weierstrass fibration is smooth or minimal (gate G3 is the next one: the discriminant's behaviour where
  a, c, ω vanish simultaneously, and the codimension-2 fibres).
- No Calabi–Yau fourfold statement, no Euler characteristic, no tadpole (ledger item 4: F5b stays).
- No fibre type is attached (ledger items 3 and 10); only vanishing orders and degree counts are used.
- The condition e ≤ 3 is necessary for this divisibility structure, not a classification of all rational maps z.
- Nothing physical, nothing about dark-sector observables.

## 4. Controls (19, all behave as required)

Divisor class (0,1) and (2,0), a non-disjoint pair (1,0),(0,1), Tate orders (5,5) and (4,7), the wrong canonical class, e = 4,
a tampered a, a tampered b, a doubled π in the pull-back check, a tampered π structure; plus positive anchors for the real data.
One control (G5) was first mis-specified, perturbing a constant the pull-back check never reads; it was rewritten to perturb π
itself. The checker's first run also failed on a real bug (h₁² was counted as a non-zero class in the disjointness test); fixed.
