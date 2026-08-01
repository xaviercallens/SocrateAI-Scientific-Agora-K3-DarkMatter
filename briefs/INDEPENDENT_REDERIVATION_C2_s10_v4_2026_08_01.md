# Independent re-derivation of T(cooper_s10) ≅ U ⊕ ⟨20⟩ — verdict for T0 acceptance

**Requested by:** T0 (Xavier), 2026-08-01 — producer≠verifier gate on
`C2_cooper_s10_v4_DRAFT.json` before promotion to LIVE.
**Verdict:** **AGREEMENT on everything the lattice claim asserts** — with one scope
boundary stated explicitly below rather than glossed. Recommendation: **acceptable to
promote**, with the residual item recorded in-cert.

Reproduce: `python3 checkers/independent_rederivation_C2_s10_v4.py` (23 checks) and
`python3 checkers/independent_rederivation_C2_s10_v4_controls.py` (10 controls). Both
exit 0.

## Independence discipline actually applied

- Does **not** import, call, or copy `check_U1_lattice.py` or
  `check_U1_witness_serialization.py`. Every routine (Smith normal form, discriminant
  form, U-splitting, overlattice enumeration) is written from the lattice-theory
  definitions.
- The only inputs taken from the existing work are the **claims under test** (the Gram
  matrix `G` and the asserted witness `P`), transcribed by hand — reading them through
  the repo's own loader would couple this check to the code it must be independent of.
- **The obvious cross-check was rejected as circular and NOT used.** The natural move is
  to derive T from G0's NS result via the Nikulin complement. `G0_NS_genus_cooper_s10.json`
  labels its own Gram input `"T_input"` — G0 *consumed* T ≅ U⊕⟨20⟩ and computed NS = T^⊥
  from it. Deriving T back from NS would therefore be circular, and is not treated as
  evidence anywhere below.

## What was independently re-derived (AGREES)

| Claim | Independent result |
|---|---|
| det = −20 | −20 ✓ |
| signature (2,1) | (2,1) ✓, nondegenerate |
| even lattice | ✓ (all Gram diagonal entries even) |
| discriminant group Z/20 | elementary divisors [1,1,20] via own SNF ✓ |
| discriminant form q ≡ 1/20 mod 2Z | ✓ — compared **orbit-wise** ({1/20, 9/20}), since q depends on the choice of generator; the claimed value lies in the orbit |
| **T ≅ U ⊕ ⟨20⟩** | ✓ **re-derived from scratch** (below) |
| witness det P = 1 | 1 ✓ |
| PᵀGP = U ⊕ ⟨20⟩ | ✓ exact |
| 0 proper even invariant overlattices | 0 ✓ (enumerated all 5 nontrivial subgroups of Z/20; none isotropic) |

**The strongest single result:** the U-splitting was re-derived by my own algorithm
(find primitive isotropic `e` with (e,L)=Z → build hyperbolic partner `f = w − (w²/2)e`
→ solve for the rank-1 complement exactly). It started from a *different* isotropic
vector (`e = [−5,−1,−2]`, vs the certificate's implicit `(1,0,0)`) and produced a
*different* witness:

```
P_mine = [[-5, 18, 60],      (vs the cert's  P = [[1, -360, 120],
          [-1,  3, 11],                          [0,   -6,   1],
          [-2,  5, 20]]                          [0,   -1,   0]])
```

Both satisfy PᵀGP = U ⊕ ⟨20⟩. **d = 20 is therefore not an artifact of the particular
splitting the original pipeline happened to choose** — an arbitrary different starting
point lands on the same invariant, which is what independence is supposed to test.

## Controls (a verifier that never fails on purpose is untested)

1. Same algorithm aimed at the **LIVE s7 lattice** returns **d = 14**, not 20 — proves it
   reads `d` out of the lattice rather than being hardwired.
2. Tampered Grams ⟨18⟩, ⟨22⟩, ⟨60⟩ each return their own value; **none masquerades as 20**.
3. The s10 witness applied to the **s7** lattice produces
   `[[0,1,0],[1,−216,36],[0,36,14]]` — visibly non-split, so the witness is
   s10-specific, not generic.
4. A non-unimodular "witness" (2·P, det 8) is correctly rejected.
5. The opposite convention `P G Pᵀ` yields `[[2591760,43199,7200],…]` — garbage. The
   convention check is therefore discriminating, not one that would pass either way.

## Internal coherence with G0 (consistency, explicitly NOT independent corroboration)

Computed independently (E8(−1) Cartan matrix built from scratch: even, det +1):

- rank NS + rank T = 19 + 3 = **22** ✓
- signature (1,18) + (2,1) = **(3,19)** ✓ (K3 lattice)
- q_T = +1/20, q_NS = −1/20 → **q_T = −q_NS** ✓ (Nikulin)

This is a real coherence constraint that would catch a later edit to one certificate but
not the other. It is **not** evidence for d = 20, because G0 took T as input.

## Scope boundary — what is NOT independently re-derived

Everything above is downstream of the Gram matrix `G`. **That `G` is the
monodromy-invariant orbit lattice of the cooper_s10 family — and specifically the value
20 itself — was not independently re-derived here**, and cannot be without redoing the
60-dps analytic continuation, cusp-loop machinery, and rational recognition that produced
it. Both the certificate and this check share that single upstream chain.

I looked for an outside handle on 20 and did not find a usable one:

- The hash-pinned Gorodetsky/Cooper table (`refs/cooper_sequences.md`, S1) gives Cooper's
  parameters `(a,b,c,d)`; for s10 that `d` is **4**, a recurrence coefficient — **not** the
  lattice determinant. Easy to conflate; it is a different quantity and gives no
  corroboration.
- **Flagged as a pattern, explicitly NOT as evidence:** s7 → 14 and s10 → 20 are both
  2·(the index in Cooper's `s_n` label). No pinned source in any of the three repos
  establishes that Cooper's index determines the lattice determinant, and treating a
  suggestive numerical coincidence as confirmation is precisely the failure mode this
  program has repeatedly caught. It is offered only as a *hypothesis a future
  independent check could test*, and must not be cited as support for d = 20.

**If T0 wants that last item closed**, the honest route is an independent monodromy
computation of the cusp unipotent by a different method or precision regime — a separate,
well-scoped WP, not something this re-derivation can substitute for.

## Recommendation

The lattice-theoretic content of `C2_cooper_s10_v4_DRAFT` is **independently confirmed
and discriminating-control-tested**. I recommend promotion to LIVE, with the certificate's
`tier_reason` retaining (as it already correctly does) the statement that monodromy
entries enter via numerical recognition — that remains the single-lineage element, now
explicitly documented rather than implicit.

---
*Generated-by: Opus 5 (independent verifier, deliberately not the C2-v4 producer's code
path) | Verified-by: `checkers/independent_rederivation_C2_s10_v4.py` 23/23 +
`..._controls.py` 10/10, both exit 0, re-run from the repo | Reviewed-by: pending T0*
