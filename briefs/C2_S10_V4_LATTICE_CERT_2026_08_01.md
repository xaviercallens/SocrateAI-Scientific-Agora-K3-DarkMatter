# C2_cooper_s10_v4_DRAFT — first titled lattice certificate for cooper_s10

**Status:** DRAFT — pending T0 (Xavier) acceptance. Until then T(s₁₀) ≅ U⊕⟨20⟩ remains
formally uncertified and `G0_NS_genus_cooper_s10.json`'s input-provenance gap statement
stands unchanged.
**Certificate:** `data/certificates/C2_cooper_s10_v4_DRAFT.json` (checker_version 1.2.0)
**Authority:** closes the gap explicitly flagged in the 2026-08-01 G0-s10 certificate
(`input_provenance.T_certificate_status`) and offered to T0 in
`briefs/T0_PIVOT_RESPONSE_2026_08_01.md` §1.1; T0's "continue and improve" (2026-08-01)
taken as the GO. Emission is coordinator work; promotion to LIVE is T0's alone.

## What it certifies (claim, Tier B)

The joint monodromy-invariant lattice of the cooper_s10 family is isometric to **U ⊕ ⟨20⟩**
by an explicit integral base change (serialized witness). Identification with the family's
transcendental lattice T is Tier B via the same read framework sources as s7's LIVE v5
(Dolgachev Thm 7.1/§7, Doran Thm 5.13) — the pipeline is family-generic; no s10-specific
step was added or skipped.

## Bar and numbering

Emitted directly at the **s7-v5 bar** (serialized `u_splitting.basis_change_matrix`
witness included from the start, per the 2026-07-27 T0 witness-serialization ruling).
Numbered v4 because the only existing s10 certificate is `C2_cooper_s10_v3.json` (rank
ρ=19/T=3, LIVE, untouched — it stays the runtime rank source); there is no witness-less
intermediate stage for this family.

## Verification performed (coordinator, 2026-08-01)

1. **Full pipeline run from clean shell** (`--emit-cert-s10`): both families, all
   mandatory controls — cross-family discrimination (s7 det −14 vs s10 det −20),
   scrambled-matrix (entry + conjugate), yukawa-scramble — all PASS; stage3 found the
   explicit U-splitting (det-1 base change).
2. **Witness independently validated** by the separate
   `check_U1_witness_serialization.py --cert <this file>`: P = [[1,−360,120],[0,−6,1],
   [0,−1,0]], det(P)=1 ∈ GL₃(ℤ), PᵀGP = U⊕⟨20⟩ matches the certificate's own
   `gram_after`. **VERDICT: PASS.**
3. **Known-bad control**: a tampered copy (one witness entry −360→−361) FAILS loudly
   (exit 3, recomputed PᵀGP ≠ gram_after) — the validator can actually detect a wrong
   witness on this family's numbers.
4. **Regression**: `test_U1_controls.py` ALL CONTROLS PASS after the checker change.

## Consistency with existing artifacts

- Mirror-image control structure: s7's LIVE v5 carries s10 as its discriminating control
  (det −20, 2n=20); this certificate carries s7 (det −14, 2n=14) as its own. The two pin
  each other.
- `G0_NS_genus_cooper_s10.json` (2026-08-01) consumed exactly this pipeline's T as input;
  on acceptance of this v4, that G0 certificate's tier_reason inherits the upgrade
  without rework (its own stated design).
- DL-3 firewall: the AlphaEvolve/Vertex report of the same lattice is not in this
  derivation chain; recorded under `not_claimed`.

## What T0 acceptance would change

T(s₁₀) ≅ U⊕⟨20⟩ moves from "unreviewed pipeline output" to reviewed Tier-B certificate —
the same standing s7's lattice identification has held since v5 acceptance. Nothing else:
rank certs, G0 certs, and every not_claimed item are unaffected.

---
*Generated-by: Fable 5 (T1 coordinator) | Verified-by: check_U1_lattice.py structural
assertions + check_U1_witness_serialization.py (PASS on real, FAIL on tampered) +
test_U1_controls.py (all pass) | Reviewed-by: pending T0*
