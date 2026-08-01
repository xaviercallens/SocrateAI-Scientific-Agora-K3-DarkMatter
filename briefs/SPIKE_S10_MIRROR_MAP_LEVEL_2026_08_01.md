# Spike — independent handle on d=20 for cooper_s10 via the mirror map's modular level

**Status: PARTIAL SUCCESS. A genuine second lineage for "10" that does not touch the
monodromy numerics — but it does NOT on its own certify T ≅ U⊕⟨20⟩, because the Fricke
"+" step Dolgachev's theorem actually requires is not closed.** Reported as-is rather
than rounded up.

Reproduce: `python3 checkers/spike_s10_mirror_map_level.py` (~2 min, exact `Fraction`
arithmetic throughout, no floating point).

Context: the independent re-derivation
(`briefs/INDEPENDENT_REDERIVATION_C2_s10_v4_2026_08_01.md`) confirmed everything
downstream of the Gram matrix `G`, but flagged that the value **20** itself rests on a
single upstream lineage (60-dps monodromy numerics). This spike asked whether a second,
disjoint lineage exists. T0 authorised a bounded feasibility spike, not the full WP.

## The route

Dolgachev 1996 §7, verified by direct read of the hash-pinned text
(`docs/literature/dolgachev_1996_mirror_lattice_polarized_k3.txt`):

- line 995: `M_N = U ⊥ E8 ⊥ E8 ⊥ <−2N>` — matches G0's NS(s10) at N=10
- line 1005: `(M_n)^⊥ = U ⊥ <2n>` — matches C2-v4's T at n=10
- line 103: the moduli is `X_0(n)+ = H/Γ_0(n)+`, the **Fricke** double extension

So if the s10 family's mirror-map coordinate is a Hauptmodul for Γ₀(10)**+**, then n=10
and 2n=20 follow from classical modular theory, with no monodromy numerics involved.

## What was established (solid)

**1. Machinery validated against the known case.** An exact Frobenius construction
(dual-number ε-derivative, `u_n(ε)` from the pinned Cooper recurrence) gives the
holomorphic period and the log-solution, hence the mirror map `q(z)` and its inverse
`z(q)`. It reproduces:

- s7 periods = A183204 (1, 4, 48, 760, 13840, 273504) ✓
- s10 periods = A005260 (1, 2, 18, 164, 1810, 21252) ✓
- **s7's `z(q)` = A279618 exactly, on all 11 available b-file terms** ✓
  (1, −9, 30, −15, −240, 978, −1463, −2361, 18201, −42800, 15624)

That last one identifies the recipe: **A279618 *is* the inverse mirror map of the s7
family.** The s7 Hauptmodul certificate's coordinate is recovered independently.

**2. The s10 analog, computed exactly and integral:**
`z(q) = 1, −4, −6, 56, −45, −360, 894, 960, …` (integral to order 44).

**3. Level 10, with discriminating controls.** Imposing weight 0 (Σr_d = 0) and leading
power q¹ (Σ d·r_d = 24) on eta quotients `q·∏_{d|N} E(q^d)^{r_d}` — a constraint pair
that *forces* the level-7 coordinate `q(E(q⁷)/E(q))⁴`, which is how it was validated —
and testing whether `z(q)` is degree-2 rational in the coordinate:

| tested against | s10 z(q) | s7 z(q) |
|---|---|---|
| level 10 | **3 hits** | 0 hits |
| level 7 | 0 hits | **1 hit** |
| levels 2,3,4,5,6,8,9,11,12,13,14,15 | **0 hits each** | — |

**s10 hits level 10 and nothing else; s7 hits level 7 and misses level 10.** The test
discriminates level, and the two families are cleanly separated. (s7's apparent level-14
hit is a pure containment artifact — exponents `(-4,0,4,0)`, i.e. literally the level-7
quotient with zeros on the 2 and 14 slots, as expected since Γ₀(14) ⊂ Γ₀(7).)

## What did NOT close, and why it matters

Dolgachev's statement is about **Γ₀(n)+**, the Fricke extension — not Γ₀(n). Testing
invariance under `t → κ/t` (which forces κ = a₀/a₂ = b₀/b₂ in the fitted degree-2
relation):

- **s7: κ = 1/49** — i.e. 7², matching the existing `HAUPTMODUL_S7_GAMMA07PLUS` cert's
  `fricke_kappa: 49` modulo an inverted convention in my normalisation. The method works.
- **s10: κ = 1, 1/16, 1/25** for the three coordinates — i.e. 1, 4², 5². **None is
  10² = 100.**

This is substantive, not a bug. Level 7 is prime, so its normaliser contributes a single
Fricke involution w₇. Level 10 is composite (2·5), so Γ₀(10) has Atkin–Lehner involutions
w₂, w₅, w₁₀; the κ values 4² and 5² are consistent with my three coordinates being
eigen-coordinates for **w₂ and w₅ rather than the Fricke w₁₀**. Additionally, the
Γ₀(10)+ Hauptmodul is expected to be a *combination* (`t + 100/t`), which a search over
single eta quotients cannot find by construction.

## Verdict and what this does / does not license

**Does license:** stating that the s10 mirror map is modular of level 10, established by
exact q-series identity with cross-level negative controls, on a lineage entirely
disjoint from the monodromy numerics. That is real, independent corroboration that the
relevant level is **10** and not something else.

**Does NOT license:** treating T ≅ U⊕⟨20⟩ as independently certified by this route.
Invoking Dolgachev §7 needs Γ₀(10)**+**, and the Fricke step is exactly what is open.
Anyone citing this spike must not skip that gap.

**The C2-v4 recommendation is therefore unchanged** from the re-derivation brief: accept,
with the single-lineage caveat retained in `tier_reason`. This spike strengthens
confidence in n=10; it does not remove the caveat.

## Well-defined remaining step (if T0 wants the full WP)

Construct the Γ₀(10) Hauptmodul proper, form the Fricke combination `t + 100/t`, and test
whether `z(q)` is degree-2 rational in *that*, with the same negative controls plus a
wrong-κ control. If it verifies, Dolgachev §7 applies and d=20 gains a fully independent
certificate. Tractable and now well-scoped — the periods, mirror map, and level-10
coordinates all exist and are committed.

---
*Generated-by: Opus 5 (T1) | Verified-by: `checkers/spike_s10_mirror_map_level.py`,
exact Fraction arithmetic, machinery validated against A183204 / A005260 / A279618 before
use; cross-level controls run | Reviewed-by: pending T0*
