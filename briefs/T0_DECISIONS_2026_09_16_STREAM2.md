# T0 Decisions — 2026-09-16 (Stream 2)

## D6′ — C2_cooper_s10_v4 ACCEPTED, promoted to LIVE

`data/certificates/C2_cooper_s10_v4.json` is now the LIVE lattice certificate for
cooper_s10: the monodromy-invariant lattice of the family is isometric to U ⊕ ⟨20⟩ by the
serialized integral base change, identified with T at **Tier B** (same framework citations
and same numerical-recognition caveat as `C2_cooper_s7_v5.json`). It is the first lattice
certificate for this family, so there is nothing to supersede. `C2_cooper_s10_v4_DRAFT.json`
is retained byte-identical for audit (SHA-256 `3558343b…d777fc` before and after).
`C2_cooper_s10_v3.json` remains the runtime source for ranks (ρ = 19, T = 3).

**What changed in the LIVE file relative to the DRAFT:** `certificate`, `status`,
`provenance`, `controls.witness_serialization` (path), the last `not_claimed` entry (the
"DRAFT is not live" line), one added `not_claimed` entry (no second lineage for the value
20), and an added `t0_acceptance` block. The `derived` block is identical (checked by
serialized comparison at promotion time).

**Basis for acceptance:**
- Independent re-derivation by a different code path (producer ≠ verifier):
  `briefs/INDEPENDENT_REDERIVATION_C2_s10_v4_2026_08_01.md`, 23/23 checks plus 10/10
  discriminating controls, recommending promotion. Re-run 2026-09-16 at `aaf828b`: both
  exit 0.
- Witness self-check: `checkers/check_U1_witness_serialization.py --all` now covers s10
  v4 and v4_DRAFT (both PASS). Its controls file gained three s10 controls: the LIVE
  certificate passes; a tampered P fails; s10's P against s7's Gram fails. 10/10 green.

**Unchanged by this decision:**
- The value 20 still comes from one line of computation (60-dps monodromy numerics). The
  modular second-lineage attempt stopped at Γ₀(10)\* vs Γ₀(10)+ and is referred to Deep
  Think (`briefs/DEEPTHINK_ALIGNMENT_BRIEF_S10_COMPOSITE_LEVEL_2026_08_01.md`, not yet
  transmitted as far as the repos record).
- `G0_NS_genus_cooper_s10.json` stays DRAFT. It gained an in-band `correction_notes` entry
  saying its "no T0-reviewed lattice certificate" gap statement is superseded. No value in
  it changes, because it re-derives T itself instead of reading this certificate.
- Every fourfold-level question for cooper_s10 still sits behind the TW2A Reading-1/2
  referral. No Kodaira types, no physical coupling (E-007/E-008/E-009, VISION §1.3).

Authority: Xavier Callens (T0), in session 2026-09-16, by selecting "Accept s10 lattice
cert" when asked which Stream-2 decision to take next.

---
*Generated-by: Claude (Opus 5) | Verified-by: regression block + s10 re-derivation and
controls, green before and after promotion; DRAFT hash unchanged | Reviewed-by: Xavier (T0)
records his own in-session decision*
