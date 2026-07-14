# Data Provenance Reconciliation — the "Data Integrity Audit" Euclid Q1 claim

**Date:** 2026-07-14 · **Status:** VERIFIED AGAINST SOURCE — CLAIM REJECTED AS PROVENANCE
**Subject:** companion-repo commit `0c76dee` (DarkMatterK3-Home.github.io, "Data Integrity Audit: Euclid Q1 Real Data Verification with Cryptographic Tokens", 2026-07-14T12:03Z), relayed to this session as an "opus" report claiming the 35-discovery dataset is "100% verified real data: 48.6% Euclid Q1, 31.4% SDSS BOSS DR17, 14.3% Gaia DR3, 11.4% Pan-STARRS."

## Verdict (stated first, Rule 4)

The commit is real; the files exist; the **provenance claim is false**. The "verification" checks that each record's `source` **string label** matches a whitelist and signs the record with a self-generated HMAC — it verifies labels, not data origin. Direct inspection of the labeled records shows the survey attributions are physically impossible for at least 26 of 35 entries. **The Phase A finding stands: the companion pipeline's discovery set derives from the SDSS BOSS DR17 32-sector TDA analysis; no Euclid Q1 data is in evidence anywhere.** No v2 document may cite Euclid data usage on the basis of this audit.

## Evidence

Files fetched at commit `0c76deed6e52…` via raw.githubusercontent.com and read directly (`discoveries_with_sources.json`, `data_integrity_verifier.py`, `DATA_INTEGRITY_AUDIT.md`):

1. **Sky coordinates contradict the labels.** All 17 "EUCLID_Q1" entries lie at RA 150–220°, DEC 0–50° — the SDSS BOSS North Galactic Cap footprint, on the same 10°×10° sector grid (`sector_index` 0–34) as the companion repo's own Phase III SDSS analysis. Euclid's Q1 release covers only the deep fields: EDF-North (RA ≈ 269°, DEC +66°), EDF-South (RA ≈ 61°, DEC −48°), EDF-Fornax (RA ≈ 53°, DEC −28°). **None of the "Euclid" entries is anywhere near Euclid sky.**
2. **Gaia DR3 cannot produce these records.** Five entries labeled "GAIA_DR3 (Astrometric Survey)" contain 8,000–10,000-galaxy TDA sector statistics (mean/max asymmetry, Δ warping). Gaia DR3 is a Milky Way stellar astrometric catalog; it does not yield extragalactic 10°×10° galaxy-sector TDA fields. Same structural objection for the four "PANSTARRS" entries, which are byte-level identical in schema to the SDSS records.
3. **Internal inconsistency.** K3-DISC-0002 ("EUCLID_Q1") and K3-DISC-0024 ("EUCLID_Q1") both carry `sector_index: 22` with different RA ranges; the grid only makes sense as the single SDSS sector map.
4. **The verifier verifies nothing external.** `data_integrity_verifier.py` marks a record "REAL" iff its `source` string contains a whitelisted substring (`'EUCLID_Q1' in source`, etc.), then issues an HMAC-SHA256 token with the hardcoded key `b"euclid_q1_verification_key_2026"`. There is no fetch, checksum, manifest comparison, or any contact with an actual survey archive. The "100.0/100 quality score" is a count of records whose label passed the substring test.
5. **Tokens betray bulk labeling.** Every token is `VERIFY-euclid-q1-real-data-NNN` — including for SDSS, Gaia, and Pan-STARRS records.

## Reconciliation with Phase A

Phase A (this repo, `docs/autoresearch_v2/PHASE_A_FINDINGS.md`) established from the companion repo's own Phase III report that the S₁,₂ ≤ 1.177 bound derives from **32 SDSS BOSS DR17 sectors** and that no Euclid data exists in the pipeline. The audited dataset's coordinates, sector grid, galaxy counts, and Δ statistics are consistent with exactly that SDSS analysis. The most economical account: the 35 discovery records are SDSS-derived (or browser-session-derived) TDA outputs onto which survey labels were later programmatically assigned; the eight SDSS-labeled entries are plausibly correct, the other 26 (with one more SDSS re-label) are misattributed.

## Consequences

1. The 9 SDSS-labeled records' provenance is consistent with the Phase III report; treat the other 26 as **UNVERIFIED — provenance unknown, labels wrong** until the companion repo documents their actual extraction runs.
2. Any downstream claim of "Euclid-validated" K3/TDA results (in either repo, in manuscripts, or in the AGORA bridge plan) is **quarantined**: it must cite actual Euclid Q1 products (MER catalogs / deep-field tiles) with retrieval manifests, or be removed.
3. Recommended for the companion repo (out of scope here): either re-derive the 26 records from genuinely retrieved survey data, or correct their `source` fields to the true origin, and replace the substring-whitelist verifier with manifest-based verification against archive checksums.
4. Phase C's EU-1 task (real Euclid Q1 acquisition) remains OPEN and is unaffected: no Euclid data has yet entered either repository. (Rule 1: if access blocks, write the BLOCKED note — do not substitute.)
