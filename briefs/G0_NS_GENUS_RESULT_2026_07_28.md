# WP S2-G Phase G0 result: NS genus certified, PROCEED (not HALT)

**Date:** 2026-07-28. **Status:** DRAFT certificate, pending T0 review before G1 is considered.
**Phase:** WP S2-G Phase G0 (briefs/WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md §5), opened by T0
2026-07-28 (decision log in that file, commit 1dd660a).

## Result

The Néron-Severi lattice of the generic K3 fiber in the certified cooper_s7 family, computed
as the Nikulin orthogonal complement of the certified transcendental lattice T ≅ U⊕⟨14⟩
inside the K3 lattice Λ = U³⊕E8(-1)², is:

**NS ≅ U ⊕ E8(-1) ⊕ E8(-1) ⊕ ⟨-14⟩** — rank 19, signature (1,18), cyclic discriminant group
of order 14.

**Match criterion (does NS contain U as an orthogonal direct summand?): YES.** This is the G0
row's stop condition; a NO would have halted the plan here. It did not — Route A may proceed
to G1 pending a separate T0 gate (not opened by this result; see decision log below).

An unforced cross-check: NS's rank (19) matches ρ=19 (E-011, Zarhin 1983 Thm 1.6(a)) via a
completely independent derivation route (Nikulin complement of the monodromy-derived T, vs.
Zarhin's direct rank computation).

## Method

Two independent derivations, checked to agree on the literal Gram matrix (not just
isomorphism-in-principle):
1. **Constructive witness** (primary): T's certified splitting embeds explicitly into Λ via
   f→e_U1, e→f_U1, w→e_U2+7f_U2 (checked primitive); NS is read off directly from Λ's block
   structure.
2. **Genus-uniqueness argument** (independent cross-check): existence+uniqueness of the
   primitive embedding (Huybrechts Thm 1.12), additivity of signature, discriminant-form
   duality (Prop 0.2(i)), uniqueness in genus (Thm 1.5) — all bounds checked exactly, not
   assumed.

Exact sympy integer/rational arithmetic throughout (Smith normal form, exact charpoly
real-root signature, Sylvester-criterion positive-definiteness); no floats, no numerical
tolerance anywhere in the lattice arithmetic itself.

## Coordinator independent verification (2026-07-28, this session)

Reproduced independently of the generating agent's self-report:
- Re-ran `checkers/check_NS_genus_G0.py` fresh: identical output (MATCH: YES, same Gram data).
- Ran `checkers/test_NS_genus_G0_controls.py` (5 negative/regression controls): ALL PASSED —
  scrambled-candidate-twist (2 variants), non-cyclic disc-group guard, oversized disc-group
  guard, cross-family discrimination (s7 d=14 vs s10 d=20), E8-matrix sanity.
- Hand-checked the core invariants independently of the code: Hodge-index signature
  (1,18)=(1,ρ-1) for ρ=19 ✓; discriminant-order duality |disc(T)|=|disc(NS)|=14 (mutual
  orthogonal complements in a unimodular lattice) ✓; rank arithmetic (22-3=19) ✓.

This is reproduction + hand-verification of invariants, not yet a fully independent
from-scratch re-derivation in separate code (the standard this repo set for U1 — see
STREAM2_U1_EXECUTION_2026_07_27.md). **Recommended before promoting this certificate out of
DRAFT status**: a from-scratch re-derivation by a fresh session that does not read
`check_NS_genus_G0.py` first, matching the U1 precedent.

## Independent from-scratch re-derivation (2026-07-28, second agent, blind to the checker)

Completed. **Verdict: AGREE.** A fresh agent, instructed not to read `check_NS_genus_G0.py` or
`test_NS_genus_G0_controls.py` until after producing its own result, independently: verified
T's certified basis-change witness by exact matrix multiplication; built its own E8 Cartan
matrix from a *different* Dynkin-diagram node labeling than the checker's and independently
verified it symmetric/even/positive-definite/unimodular; constructed Λ = U³⊕E8(-1)² and
verified its defining properties; embedded T and computed NS = T^⊥ explicitly (not by genus
argument alone); re-derived the discriminant-form value **27/14 mod 2Z independently**, matching
the checker exactly; confirmed NS contains U as a literal orthogonal direct summand by explicit
construction. Also checked the Huybrechts theorem citations (1.12, 0.2, 1.5, 1.11) against the
repo's own hash-pinned `docs/literature/huybrechts_K3Global.txt` — real, correctly numbered,
used in matching contexts, not fabricated.

**Two honest limits on how independent this was, both worth keeping attached to any future
citation of "independently verified":**
1. The task prompt handed to the second agent stated the specific embedding construction
   verbatim (`f→e_U1, e→f_U1, w→e_U2+7f_U2`) rather than leaving the agent to discover it —
   this is the canonically forced construction (a norm-2n vector in a hyperbolic plane is
   e+nf; there is no other natural choice), not a free design decision, but the re-derivation
   was not blind to *that specific step*. The genuinely independent pieces are the E8 basis
   (a different matrix reaching the same conclusion), the signature/discriminant-group
   computation routines, the primitivity checks (Smith normal form), and the 27/14 value.
2. Uniqueness-of-embedding (the Nikulin/Eichler bound: rank(Λ)−rank(T)=19 ≥ ℓ(A_T)+2=3) is
   load-bearing for the argument, not optional — the second agent confirmed this explicitly
   rather than treating the explicit witness as sufficient on its own.

**Status update: the U1-precedent independent-verification standard is now met**, with the
above two caveats recorded rather than smoothed over. Certificate remains formally DRAFT
pending T0's own review and explicit promotion — this session does not self-promote it.

## Caveats (carried verbatim from the certificate — do not drop these in any summary)

1. **Weak discriminating power.** Both cooper_s7 (d=14) and cooper_s10 (d=20) pass with a U
   summand. For this family's NS shape (rank 19, cyclic disc group), the genus-representative
   construction essentially always places a U in front regardless of n. Clearing G0 rules out
   one specific failure mode; it is not strong evidence G1 will succeed, and does not touch the
   plan's flagged main risk (G1-b, crepant resolvability).
2. **Fiberwise, not yet relative.** This certifies the abstract generic K3 fiber admits an
   elliptic fibration with section. G1-c needs the *relative* structure — the isotropic NS
   class monodromy-invariant along the whole family — which this G0 certificate does not check
   (monodromy generators are available from `check_U1_lattice.py` stage2/stage3 but unused
   here).

## Tier and scope

Tier B (inherited from T's own tier — the lattice arithmetic in this certificate is exact and
would be Tier E/A in isolation, but a claim cannot be more certain than its input). Does not
claim: Kodaira fibre types, physical coupling, CY condition/resolution/elliptic-fibration
construction for X₄, any observable (F5b stands), or realization beyond the abstract-lattice
statement.

## Decision log

- **2026-07-28, coordinator (this session):** independently reproduced and verified per above.
  Certificate committed as DRAFT. **G1 is NOT opened by this result** — per the 2026-07-28 T0
  decision (WP_S2G_X4_EXHIBITION_PLAN §8), G1 remains a separate, later T0 gate, to be
  requested once this DRAFT is reviewed (and ideally independently re-derived per the
  recommendation above).

## Files

- `checkers/check_NS_genus_G0.py` — the checker (exact arithmetic, both derivation methods)
- `checkers/test_NS_genus_G0_controls.py` — 5 negative/regression controls (standalone script,
  not pytest-collected — run via `python3 checkers/test_NS_genus_G0_controls.py`)
- `data/certificates/G0_NS_genus_cooper_s7.json` — the certificate (DRAFT)

Generated-by: Sonnet 5 (Stream 2, WP S2-G Phase G0 agent, 2026-07-28) | Reviewed-by: Sonnet 5
(coordinator, this session, independent reproduction) | T0 review: pending
