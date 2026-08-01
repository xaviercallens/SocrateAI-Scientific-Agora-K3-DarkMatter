# G0 NS-genus result — cooper_s10 (T0 pivot directive §1.1, 2026-08-01)

**Status:** DRAFT — pending T0 (Xavier) review.
**Certificate:** `data/certificates/G0_NS_genus_cooper_s10.json` (checker_version 1.1.0)
**Authority:** T0 strategic-pivot directive 2026-07-31/08-01, §1 task 1 ("derive the
Néron-Severi lattice via the Nikulin orthogonal complement of T ≅ U⊕⟨20⟩; verify NS
contains U as an orthogonal direct summand").

---

## Result

**U-summand determination: YES.**

NS(s₁₀) = T⊥ inside Λ = U³ ⊕ E8(−1)² is isometric to

```
U ⊕ E8(−1) ⊕ E8(−1) ⊕ ⟨−20⟩      (rank 19, signature (1,18), det −20,
                                   cyclic discriminant group Z/20, q ≡ −1/20 mod 2Z)
```

U is an orthogonal direct summand (manifest in the exhibited block form), so the generic
K3 fiber of the cooper_s10 family admits an elliptic fibration **with section** over P¹
(Huybrechts Ch.14 Ex 0.3) — the direct analog of the s7 result, with d = 20 in place of 14.

The full 19×19 Gram matrix is serialized in the certificate
(`derived.candidate.gram` == `derived.constructive_witness.NS_gram_exhibited`, checked
equal as exact integer matrices, not isomorphic-in-principle).

## How (two independent routes, checked to agree on the identical Gram)

1. **Exhibited (primary):** T's U-splitting (fresh from
   `check_U1_lattice.py:run_family('cooper_s10')` at DPS precision) embeds into Λ via
   f→e_U1, e→f_U1, w→e_U2+10·f_U2 (checked primitive: gcd of maximal 3×3 minors = 1);
   NS read off from Λ's block structure as Z·(e_U2−10·f_U2) ⊕ U₃ ⊕ E8(−1)², orthogonality
   to embedded T checked exactly.
2. **Genus-uniqueness (secondary):** Huybrechts Thm 1.12 (embedding exists, unique),
   Prop 0.2(i) (complement disc form −q_T), Thm 1.5 (unique in genus; ℓ+2=3 ≤ 19).

Pipeline is byte-identical to the s7 G0 code path (coordinator-verified 2026-07-28,
cross-verified against an independent Deep Think lineage for s7); only the input family
differs.

## Integrity gates (both PASS, checked at runtime)

- Fresh s10 T matches the s10 control block pinned inside the reviewed LIVE
  `C2_cooper_s7_v5.json` (det = −20, 2n = 20).
- NS rank 19 equals `C2_cooper_s10_v3.json` picard_rank = 19, derived by the entirely
  independent Zarhin-1983 route (E-011 style) — an unforced cross-check.

## Controls

`checkers/test_NS_genus_G0_controls.py`: 7/7 PASS, including two new s10-specific
controls added with this change (s10 scrambled-twist must-fail on both the evenness and
disc-form gates; certificate round-trip + tampered-det anchor gate must-fail).

## Tier and honest limits

**Tier B** — the lattice arithmetic is exact end-to-end, but the claim inherits the tier
of its input, and s10's input is **weaker than s7's**: T(s₁₀) ≅ U⊕⟨20⟩ is re-derived
in-house by the same monodromy pipeline as s7's, but — unlike s7 — has **no titled,
T0-reviewed C2-v5-style lattice certificate** of its own. That promotion (serialized
witness, monodromy provenance, negative controls, review) is a separate deliverable.
The AlphaEvolve/Vertex report of the same lattice is Stream-4 exploratory-sandbox
provenance (DL-3) and was **not** an input; the agreement is recorded as coincidence,
not evidence.

Same standing caveats as the s7 G0 certificate: weak discriminating power (any member of
this T ≅ U⊕⟨2n⟩ family clears G0 by the same construction); fiberwise only — no
monodromy-invariance, no fourfold-level statement, no Kodaira types, no observables.

---
*Generated-by: Fable 5 (T1 coordinator) | Verified-by: check_NS_genus_G0.py structural
assertions + verify_s10_against_in_repo_anchors() + test_NS_genus_G0_controls.py (7/7) |
Reviewed-by: pending T0*
