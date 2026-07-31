# Deep Think (T0s) Alignment Brief — TW2-A Q1: the codim-2 (4,6) Reading Question

**Date:** 2026-07-31 · **Referring authority:** T0 (Xavier Callens), formal referral in
`T0_RECOMMENDATIONS_TW2A_2026_07_31.md` · **Prepared by:** Fable 5 (T1 coordinator)
**Requested review mode:** adversarial, independent re-derivation where feasible.
**Contamination note:** this brief deliberately presents both readings symmetrically and
omits any in-house lean. Nothing here should be read as a preferred answer.

---

## 1. The setting (self-contained)

Work over ℂ. Base threefold **B₃ = P(O ⊕ O) over P²** (the n=0 trivial P¹-bundle, i.e.
P¹×P²), with disjoint sections C₀ = {s=0}, C∞ = {t=0} ([s:t] the fiber coordinate,
[x:y:z] on P²). Generic Weierstrass model y² = x³ + f x + g with f ∈ H⁰(−4K_{B₃}),
g ∈ H⁰(−6K_{B₃}); −4K has bidegree (8,12) and −6K bidegree (12,18) in (fiber, base)
degrees. The model is required to carry **Kodaira II\* (E₈) fibers along both C₀ and C∞**
(vanishing orders (4,5) of (f,g) on each, order 10 of Δ), targeting a K3 fiber with
Néron–Severi lattice M₁₉ = U ⊕ E₈(−1)² ⊕ ⟨−14⟩.

An explicit such (f, g) has been exhibited and machine-verified (exact sympy arithmetic,
negative controls; repo: `checkers/check_TW2A_n0_construction.py`, certificate
`data/certificates/TW2A_n0_construction.json`):

  f = −3 τ w² s⁴ t⁴,  g = s⁵ t⁵ w³ (a s² + b s t + c t²),

with explicit rational τ, a, b, c and w = x⁶ + y⁶ − 2z⁶ (so a, c ∈ H⁰(P², O(18)) after
absorbing w³; in the general two-E₈ ansatz a, c are arbitrary degree-18 forms).

## 2. The proven obstruction (Finding 4 — exact, unconditional)

For **every** n=0 two-E₈ model (not only the exhibited one): the C∞-side coefficient
forms a, c ∈ H⁰(P², O(18)) are nonconstant, hence {a=0} and {c=0} are nonempty curves in
P². Along the codimension-2 locus **{t=0} ∩ {a=0}**, every monomial of g has (t,a)-adic
order ≥ 6 while ord(f) ≥ 4 — verified as an unconditional algebraic statement, no
genericity used. Symmetrically {s=0} ∩ {c=0} inside C₀. Additionally verified: the
(1,0)+(1,0) section pair is the **only** disjoint two-divisor configuration supporting
two E₈'s at n=0, so the phenomenon is exhaustive over the ansatz, not an artifact of one
model. (In the exhibited model the locus is even deeper, (6,8), and contains the rational
point (1:1:1) ∈ {w=0}.)

So: **every n=0 two-E₈ model carries nonempty codimension-2 curves where (ord f, ord g) ≥
(4, 6), sitting inside the E₈ divisors themselves** (the E₈×E₈ collision curves).

## 3. The question referred (Q1) — verbatim task from T0

> Determine if a base blow-up (Reading 2) of this specific P¹-bundle over P² will
> mathematically preserve the c₁ = 0 Calabi-Yau condition globally, or if the SCFT
> collision is terminal (Reading 1).

The two readings, stated symmetrically:

- **Reading 1 (terminal):** a codim-2 locus with (4,6) means no smooth minimal
  Calabi-Yau Weierstrass model exists **over the given base**; since the requirement was
  scoped to this base family, the n=0 (and, if the structural remark below generalizes,
  every-n) fourfold route is a documented dead end.
- **Reading 2 (curable):** codim-2 (4,6) loci are cured by blowing up B₃ along the
  collision curve (tensor-branch transition; exceptional divisor enters the base). The
  cure changes K_{B₃} and hence leaves the P(O⊕O(n))/P² family as scoped; the prior
  feasibility table (WP-TW1) would need re-derivation on blown-up bases.

## 4. What a decisive answer looks like

1. **The precise mathematical criterion** separating curable from terminal codim-2 (4,6)
   loci (e.g., conditions under which the blown-up base B̂₃ admits f̂ ∈ H⁰(−4K_{B̂₃}),
   ĝ ∈ H⁰(−6K_{B̂₃}) with a crepant-resolvable discriminant — orders after proper
   transform, multiplicity of the center, normal-crossing status of the collision curve
   {t=0}∩{a=0} for generic degree-18 a).
2. **Applied to this specific case**: for the collision curve of an n=0 two-E₈ model
   (a smooth plane curve of degree 18 inside C∞ ≅ P², generically), does one blow-up
   (or a finite sequence) reduce the orders below (4,6) while preserving c₁ = 0 of the
   **total space** after crepant resolution — yes or no, with the derivation.
3. **Citations to primary literature** (paper + theorem/section granularity) sufficient
   for this project to hash-pin the criterion into `refs/` — the repo currently holds no
   F-theory/Tate-algorithm references, which is why this is referred rather than settled
   in-house.
4. **Scope statement**: whether the answer is specific to n=0 or extends to all n ≥ 0
   (the unchecked structural remark: the C∞-side coefficient has degree 18+n for every
   n ≥ 0, suggesting nonempty vanishing loci always exist — this remark is UNVERIFIED and
   is included only as a question, not a claim).

## 5. Independent re-derivation targets (adversarial checklist)

Deep Think is invited to attack any of the load-bearing exact claims rather than accept
them: (i) the unconditional (t,a)-adic order ≥ 6 of g on {t=0}∩{a=0}; (ii) the
exhaustiveness of the (1,0)+(1,0) disjoint configuration at n=0; (iii) the monodromy
computation around {w=0} (fiberwise inversion; P̄ ↦ −P̄; invariant rank 18) — already
T0-accepted for abandoning the isotrivial ansatz, but a second derivation strengthens or
falsifies it; (iv) the fiber-level Shioda–Tate arithmetic (h(P) = 14, P·O = 5, P̄² = −14)
— note this layer is **out of scope for Q1** (it is settled at Tier B and was
independently hand-re-derived by the coordinator), listed only for completeness.

## 6. What is NOT asked

No physics interpretation beyond what the mathematical answer forces; no opinion on
whether the program should continue either way (that is T0's call); no evaluation of
cooper_s10/U⊕⟨20⟩ (out of scope, uncertified); nothing about Stream 3/empirical work.

## 7. Repo pointers (for the record; the brief above is self-contained)

- Result brief: `briefs/WP_TW2A_N0_CONSTRUCTION_2026_07_31.md` (S2 `8305247`)
- Checker + controls: `checkers/check_TW2A_n0_construction.py`,
  `checkers/test_TW2A_n0_construction_controls.py` (7/7)
- Pinned literature inputs: `refs/x0_7_inose_cm.json` (SHA-256 `17732a41…ce9aa0`)
- Referral: `briefs/T0_RECOMMENDATIONS_TW2A_2026_07_31.md`

---
*Intake protocol reminder for the eventual debrief: Deep Think's response will be audited
before any of its content is cited (per the standing rule: cite only audit verdicts, not
the debrief directly — precedent `DEEPTHINK_DEBRIEF_AUDIT_2026_07_28.md`).*
