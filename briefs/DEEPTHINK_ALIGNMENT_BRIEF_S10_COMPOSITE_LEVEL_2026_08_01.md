# Deep Think (T0s) Alignment Brief — cooper_s10: does Dolgachev's M_n correspondence survive composite n?

**Date:** 2026-08-01 · **Referring authority:** T0 (Xavier Callens) · **Prepared by:**
Opus 5 (T1 coordinator)
**Requested review mode:** adversarial; independent re-derivation where feasible.
**Contamination note:** the in-house computation is presented in full, including a
self-correction, so it can be attacked. We state below exactly where our own reasoning is
weakest and would most like to be wrong.

---

## 0. The single question

> **Q.** Dolgachev (1996) §7 identifies the moduli of the mirror family for M_n-polarized
> K3 surfaces with `X₀(n)+ = H/Γ₀(n)+`, the **Fricke** double extension, and gives
> `(M_n)^⊥ = U ⊕ ⟨2n⟩`. We find, by exact q-series computation, that the cooper_s10
> mirror-map coordinate is a Hauptmodul for **Γ₀(10)\***, the *full* Atkin–Lehner quotient
> (index 4), not Γ₀(10)+ (index 2). For prime n these coincide; for n=10 they do not.
>
> **Does the M_n ⟹ T = U⊕⟨2n⟩ correspondence still apply when the family's moduli map
> factors through Γ₀(n)\* ⊋ Γ₀(n)+? If not, what is the correct transcendental lattice?**

The practical stake: `C2_cooper_s10_v4` (now LIVE) asserts `T(s10) ≅ U ⊕ ⟨20⟩`. It is
independently verified downstream of its Gram matrix, but the value **20** rests on a
single lineage (60-dps monodromy numerics). This modular route was our attempt at a second,
disjoint lineage. It got as far as "level 10" and then hit the group mismatch above.

## 1. What is established (exact, reproducible, machine-checked)

All arithmetic is exact `Fraction`; no floating point. Scripts:
`checkers/spike_s10_mirror_map_level.py`, `checkers/spike_s10_modular_structure.py`.

**1.1 Machinery validated against the known case before use.** Exact Frobenius
(dual-number ε-derivative) applied to the hash-pinned Cooper recurrence
`(n+1)³u_{n+1} = (2n+1)(an²+an+b)u_n − n(cn²+d)u_{n−1}` reproduces:
- s7 periods = A183204 (1, 4, 48, 760, 13840, 273504), params (13,4,−27,3)
- s10 periods = A005260 (1, 2, 18, 164, 1810, 21252), params (6,2,−64,4)
- **s7's inverse mirror map z(q) = A279618 exactly on all 11 available b-file terms**
  (1, −9, 30, −15, −240, 978, −1463, −2361, 18201, −42800, 15624)

That last identity independently recovers the coordinate underlying the existing
`HAUPTMODUL_S7_GAMMA07PLUS` certificate, and is our evidence that the construction is the
intended one rather than a lookalike.

**1.2 The s10 analogue.** `z(q) = 1, −4, −6, 56, −45, −360, 894, 960, …`, integral to
order 44.

**1.3 Level 10, with cross-level negative controls.** Searching eta quotients
`t = q·∏_{d|N} E(q^d)^{r_d}` under weight 0 (`Σ r_d = 0`) and leading power q¹
(`Σ d·r_d = 24`) — a constraint pair that *forces* the level-7 coordinate
`q(E(q⁷)/E(q))⁴`, which is how the search itself was validated — and testing whether z(q)
is degree-2 rational in t:

| tested against | s10 z(q) | s7 z(q) |
|---|---|---|
| level 10 | **3 hits** | 0 hits |
| level 7 | 0 hits | **1 hit** |
| levels 2,3,4,5,6,8,9,11,12,13,14,15 | **0 each** | — |

s7's level-14 hit is a pure containment artifact (exponents `(−4,0,4,0)`; Γ₀(14) ⊂ Γ₀(7)).

**1.4 The fitted relations are Fricke-invariant.** Each fit has numerator `a = (0,1,0)`:

| family | relation | κ |
|---|---|---|
| s7 | `1/z − 13 = 49t + 1/t` | 1/49 |
| s10 | `1/z − 8 = 16t + 1/t` | 1/16 |
| s10 | `1/z − 6 = 25t + 1/t` | 1/25 |
| s10 | `1/z + 2 = t + 1/t` | 1 |

κ is **derived**, not fitted-and-hoped: for `t = (η(2τ)η(10τ)/(η(τ)η(5τ)))⁴`, w₁₀ sends
η(τ)→√(−10iτ)η(10τ), η(2τ)→√(−5iτ)η(5τ), η(5τ)→√(−2iτ)η(2τ), η(10τ)→√(−iτ)η(τ); the
radical factor is √5/√20 = 1/2, so `t∘w₁₀ = (1/16)·t⁻¹`. The independently measured κ from
the fit is 1/16. The same derivation gives 1/49 for s7, matching the existing certificate's
`fricke_kappa: 49` in reciprocal convention.

**In form, s10 is identical to certified s7.** That is what makes the next section the
whole content of the question.

**1.5 The group, from Ligozat cusp divisors + Atkin–Lehner action.**

- s7's `t₇`: degree 1 (pole at cusp 1, zero at cusp 7) — a **genuine Hauptmodul** for Γ₀(7).
- all three s10 coordinates: **degree 2** (2 zeros, 2 poles) — *not* Hauptmoduls. (Genuine
  degree-1 level-10 eta quotients do exist — 12 found by search — but the mirror map does
  not fit against them at degree 2.)

For N=10 the AL group is {1, w₂, w₅, w₁₀}, acting on cusps c|10 by w₂: 1↔2, 5↔10;
w₅: 1↔5, 2↔10; w₁₀: 1↔10, 2↔5. Each fitted coordinate is invariant under exactly one:

| coordinate | κ | invariant | anti-invariant (t → const/t) |
|---|---|---|---|
| (−4,4,−4,4) | 1/16 | w₅ | w₂, w₁₀ |
| (−2,−2,2,2) | 1/25 | w₂ | w₅, w₁₀ |
| (6,−6,−6,6) | 1 | w₁₀ | w₂, w₅ |

Hence `u = 16t + 1/t` is invariant under w₅ (inherited from t) **and** w₁₀ (by
construction), therefore under the whole AL group. u has 4 poles on X₀(10);
X₀(10) → X₀(10)\* is degree 4; so u has degree 1 on X₀(10)\*. Since `z = 1/(u+8)` is
Möbius in u:

> **z_s10 is a Hauptmodul for Γ₀(10)\*, not Γ₀(10)+.**

## 2. Where our reasoning is weakest (please attack these first)

1. **The step 1.5 → "the family's moduli is X₀(10)\*".** We have shown the *mirror-map
   coordinate* is a Hauptmodul for Γ₀(10)\*. Inferring that the family's moduli *is*
   X₀(10)\* assumes the mirror map is the uniformizing coordinate of the moduli, not a
   coordinate on a quotient reached for an unrelated reason. We think this is the most
   likely place we are wrong.
2. **Whether Dolgachev §7's hypotheses actually exclude composite n.** We read the pinned
   text (`docs/literature/dolgachev_1996_mirror_lattice_polarized_k3.txt`, lines 981–1005,
   1083–1085) and found the Fricke statement, but we did **not** find an explicit
   primality hypothesis. It is possible the correspondence is stated for all n and our
   Γ₀(10)\* finding indicates the s10 family is a *non-generic* member (e.g. an extra
   identification from a symmetry of this particular family) rather than a counterexample.
3. **Degree-2-only search.** We tested degree-2 rationality in a single eta quotient. If
   the correct relation for composite level is degree 3+, or involves two coordinates, our
   "0 hits at genuine Hauptmoduls" is an artifact of the ansatz, not a fact about s10.
4. **Whether κ, being normalisation-dependent, carries the weight we give it.** We already
   made one error here (an earlier revision of our own brief wrongly expected κ = n² = 100
   and reported the Fricke step as failed). The correction is recorded in
   `briefs/SPIKE_S10_MIRROR_MAP_LEVEL_2026_08_01.md` Revision 2. We flag this because it is
   the kind of mistake that can recur in the opposite direction.

## 3. What we are NOT asking, and what must not be assumed

- We are **not** asking whether `T(s10) ≅ U⊕⟨20⟩` is true. It is LIVE, independently
  verified downstream of its Gram matrix (`briefs/INDEPENDENT_REDERIVATION_C2_s10_v4_2026_08_01.md`,
  23/23 checks + 10/10 discriminating controls). We are asking whether *this modular route*
  can supply a second, independent lineage for the number **20**.
- Please do **not** import the Nikulin complement from `G0_NS_genus_cooper_s10.json` as
  evidence: that certificate consumed T as `"T_input"` and computed NS = T^⊥ from it.
  Using it to confirm T is circular. We rejected it for that reason.
- The claim "the s7→14 / s10→20 pattern is 2·(index in Cooper's s_n label)" is an
  **untested numerical observation with no pinned source**, offered only as something a
  reviewer might test or dismiss. It must not be treated as support.

## 4. Concrete asks

**A1.** Rule on Q (§0). If the correspondence does extend to composite n, state the
transcendental lattice it gives for the s10 family and whether it is `U⊕⟨20⟩`.

**A2.** Independently re-derive, by any method you prefer, the modular group of the
cooper_s10 mirror map. If you get Γ₀(10)+ rather than Γ₀(10)\*, say where our §1.5
Atkin–Lehner argument fails.

**A3.** Adjudicate weakness §2.1 specifically: does "mirror-map coordinate is a Hauptmodul
for G" license "moduli is H/G"?

**A4.** If the route is salvageable, state the minimal additional computation that would
close it. If it is not, say so plainly — T0 has authorised a fail-fast fallback to the
documented single-lineage caveat, and a clean negative is a fully acceptable outcome.

## 5. Reproduction

```
git clone <S2>; cd SocrateAI-Scientific-Agora-K3-DarkMatter; git checkout v0.3.5-s10-independent-rederivation
python3 checkers/independent_rederivation_C2_s10_v4.py          # 23/23, exit 0
python3 checkers/independent_rederivation_C2_s10_v4_controls.py # 10/10, exit 0
python3 checkers/spike_s10_mirror_map_level.py                  # mirror map + level search
python3 checkers/spike_s10_modular_structure.py                 # Ligozat + Atkin-Lehner
```

---
*Generated-by: Opus 5 (T1 coordinator) | Verified-by: all numbers in §1 emitted by the two
committed scripts, exact Fraction arithmetic, machinery validated against A183204 /
A005260 / A279618 before use | Reviewed-by: pending T0s (Deep Think) — audit this brief
before citing any verdict from it, per standing practice*
