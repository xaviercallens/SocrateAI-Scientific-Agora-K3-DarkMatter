# Spike — independent handle on d=20 for cooper_s10 via the mirror map's modular level

**REVISION 2 (2026-08-01, same day). Revision 1's central conclusion was WRONG and is
corrected here.** R1 reported "the Fricke step does not close, κ is never 100." Both halves
were errors of mine: (a) κ is normalisation-dependent, and 100 was a bad analogy, not a
derived expectation; (b) the fits *are* Fricke-invariant — R1's test misread `a2 = 0` as a
failure when `a0 = a2 = 0` satisfies the invariance condition trivially. Corrected below.

**Verdict after correction: the dual lineage still does NOT close — but for a completely
different, sharper, and more interesting reason than R1 gave.** The obstruction is a
group mismatch (Γ₀(10)\* vs Dolgachev's Γ₀(10)+), not a failed invariance.

Reproduce: `checkers/spike_s10_mirror_map_level.py` (mirror map, level search, cross-level
controls) and `checkers/spike_s10_modular_structure.py` (Ligozat cusp divisors,
Atkin–Lehner action). Exact `Fraction` arithmetic throughout.

## Established, and solid

**1. Machinery validated before use.** Exact Frobenius (dual-number ε-derivative) on the
pinned Cooper recurrence reproduces A183204 (s7 periods), A005260 (s10 periods), and
**s7's z(q) = A279618 exactly on all 11 b-file terms** — identifying A279618 as the s7
inverse mirror map and recovering the certified s7 coordinate independently.

**2. s10 mirror map**: `z(q) = 1, −4, −6, 56, −45, −360, 894, 960, …`, integral to order 44.

**3. Level 10, with discriminating controls.** With weight 0 (Σr_d=0) and leading power q¹
(Σ d·r_d=24) — a constraint pair that *forces* the level-7 coordinate `q(E(q⁷)/E(q))⁴`,
which is how it was validated:

| tested against | s10 z(q) | s7 z(q) |
|---|---|---|
| level 10 | **3 hits** | 0 hits |
| level 7 | 0 hits | **1 hit** |
| levels 2,3,4,5,6,8,9,11,12,13,14,15 | **0 each** | — |

s7's apparent level-14 hit is a pure containment artifact (exponents `(-4,0,4,0)`, i.e. the
level-7 quotient with zeros on the 2 and 14 slots; Γ₀(14) ⊂ Γ₀(7)).

**4. The fitted relations, and their Fricke invariance (this is the R1 correction).**
Every fit has the form `z = t/(b₀ + b₁t + b₂t²)`, i.e. numerator coefficients `a=(0,1,0)`:

| family | relation | κ |
|---|---|---|
| s7 | `1/z − 13 = 49t + 1/t` | 1/49 |
| s10 | `1/z − 8 = 16t + 1/t` | 1/16 |
| s10 | `1/z − 6 = 25t + 1/t` | 1/25 |
| s10 | `1/z + 2 = t + 1/t` | 1 |

All four are Fricke-invariant (`a₀ = κa₂` holds trivially at `a₀=a₂=0`; `b₀/b₂ = κ`). The
κ values are *derived*, not assumed: for `t=(η(2τ)η(10τ)/(η(τ)η(5τ)))⁴`, w₁₀ sends
η(τ)→√(−10iτ)η(10τ), η(2τ)→√(−5iτ)η(5τ), η(5τ)→√(−2iτ)η(2τ), η(10τ)→√(−iτ)η(τ), giving
radical factor √5/√20 = 1/2 and hence `t∘w₁₀ = (1/16)t⁻¹`. Measured κ = 1/16. ✓ The same
computation gives 1/49 for s7, matching `HAUPTMODUL_S7_GAMMA07PLUS`'s `fricke_kappa: 49`
in reciprocal convention. **s10's structure is identical in form to certified s7.**

## Where it actually breaks: a group mismatch

Ligozat cusp divisors settle which modular group each coordinate lives on:

- **s7's t₇: degree 1** (pole at cusp 1, zero at cusp 7) — a **genuine Hauptmodul** for Γ₀(7).
- **All three s10 coordinates: degree 2** (2 zeros, 2 poles) — **not** Hauptmoduls, though
  genuine level-10 Hauptmodul eta quotients do exist (12 found by search).

The Atkin–Lehner action explains why. For N=10 the AL group is {1, w₂, w₅, w₁₀}, and each
coordinate is invariant under exactly one involution and anti-invariant under the other two:

| coordinate | κ | invariant | anti-invariant |
|---|---|---|---|
| (−4,4,−4,4) | 1/16 | w₅ | w₂, w₁₀ |
| (−2,−2,2,2) | 1/25 | w₂ | w₅, w₁₀ |
| (6,−6,−6,6) | 1 | w₁₀ | w₂, w₅ |

So `u = 16t + 1/t` is invariant under w₅ (inherited from t) *and* w₁₀ (by construction),
hence under the entire AL group. It has 4 poles on X₀(10), and X₀(10)→X₀(10)\* is degree 4,
so u has degree 1 on X₀(10)\*. Since `z = 1/(u+8)` is Möbius in u:

> **z_s10 is a Hauptmodul for Γ₀(10)\*, the FULL Atkin–Lehner quotient — not for Γ₀(10)+.**

Dolgachev §7 (line 103, pinned text) states the moduli as `X₀(n)+ = H/Γ₀(n)+`, explicitly
the **Fricke double extension** (index 2). For n=10, Γ₀(10)\* is a strictly further
quotient (index 4). For prime n=7 the two coincide — `Γ₀(7)+ = Γ₀(7)*` — which is exactly
why the s7 case closes cleanly and s10 does not.

## Verdict

**Licensed:** the s10 mirror map is modular of level 10 — established by exact q-series
identity with cross-level negative controls, on a lineage entirely disjoint from the
monodromy numerics. The level is 10 and not anything else tested.

**NOT licensed:** concluding `T ≅ U⊕⟨20⟩` from Dolgachev §7. The theorem is stated for
Γ₀(n)+; what is established here is Γ₀(10)\*. Whether the s10 family is the generic
M₁₀-polarized family, or its moduli map factors through the further AL quotient (which
would mean it is *not* generic in Dolgachev's sense), is now the open question — and it is
a substantive geometric question, not a computational gap.

**Consequence for C2-v4: unchanged.** Accept with the single-lineage caveat retained in
`tier_reason`. This spike raises structural confidence that the relevant level is 10; it
does not supply the second lineage for d=20.

**Per T0's stated fallback ("if the math fights back, fail fast, document the negative
result"): invoked.** No further compute spent. The remaining question is now precisely
posed rather than vague: does Dolgachev's M_n correspondence extend to composite n where
Γ₀(n)\* ⊋ Γ₀(n)+, and if so with which lattice? That is a literature/theory question for
T0s (Deep Think) or a targeted read of Dolgachev §7's composite-n hypotheses — not more
q-series computation.

---
*Generated-by: Opus 5 (T1) | Verified-by: `spike_s10_mirror_map_level.py` +
`spike_s10_modular_structure.py`, exact Fraction arithmetic, machinery validated against
A183204 / A005260 / A279618 before use; κ values derived from the eta transformation and
independently matched by the fits; cross-level controls run | Reviewed-by: pending T0 |
**Supersedes Revision 1 of this file, whose Fricke conclusion was erroneous.***
