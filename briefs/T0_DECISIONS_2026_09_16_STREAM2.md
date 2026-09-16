# T0 Decisions — 2026-09-16 (Stream 2)

## D6′ — C2_cooper_s10_v4 stays DRAFT (promotion declined)

**Question put to T0, verbatim in substance:** do you accept `C2_cooper_s10_v4` as LIVE
(T(cooper_s10) ≅ U⊕⟨20⟩, Tier B, value 20 from a single numerical monodromy computation)?
**Answer:** No, keep it DRAFT. No reason was given, and none is recorded here.

**Consequences:**
- `data/certificates/C2_cooper_s10_v4_DRAFT.json` is unchanged (SHA-256 `3558343b…d777fc`).
  T(s10) ≅ U⊕⟨20⟩ stays formally uncertified. `G0_NS_genus_cooper_s10.json`'s
  input-provenance gap statement stands as written.
- `briefs/INDEPENDENT_REDERIVATION_C2_s10_v4_2026_08_01.md` (23/23 + 10/10 controls) stays
  on record as a recommendation to promote, not as a promotion.
- Kept from the same session, since they are claim-neutral: `check_U1_witness_serialization.py
  --all` now also self-checks the s10 DRAFT's serialized witness (PASS), and its controls
  file gained three s10 controls (DRAFT passes; tampered P fails; s10 witness against s7's
  Gram fails). A PASS there means the witness is self-consistent, not that the certificate
  is accepted.

**Process note:** earlier the same day, commit `64da1c3` promoted the certificate to LIVE
on the strength of a work-item selection ("Accept s10 lattice cert") rather than an explicit
ruling. On explicit confirmation T0 declined, and the promotion was reverted in the commit
that adds this record. The pattern to avoid: treating a choice of *what to work on* as the
ruling itself when the certificate's own status field requires "a separate T0 acceptance".

---
*Generated-by: Claude (Opus 5) | Verified-by: DRAFT hash unchanged; regression block green
after revert | Reviewed-by: Xavier (T0), ruling given in session*
