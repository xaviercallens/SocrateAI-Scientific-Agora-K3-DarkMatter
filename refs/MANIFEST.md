# refs/ MANIFEST

Literature-derived inputs to the checkers. Per `K3_CRITERIA.md` §3 (checker contract) and
`CLAUDE.md` rule 2, checkers may read candidate data **only** from files listed here.
Each entry: file, SHA256, provenance, transcriber.

| File | SHA256 | Provenance | Transcribed by |
|---|---|---|---|
| `recurrences_v1.json` | `da7ef8207ad1709fe67b472979d40849cb7693a733936e8fb4022bf8c2fe5e34` | Cooper (2012), Ramanujan J. 29, 163–183, Eq. (16); Zagier (2009), "Integral solutions of Apéry-like differential equations", Table 1 | Xavier Callens (manual transcription, 2026-07-17) |

**Integrity rule:** any edit to a FROZEN ref file requires a new version file (`_v2`, …) and a
new manifest row — never an in-place edit. Checkers embed the SHA256 of the ref they read in
every certificate they emit, so a silent edit invalidates all downstream certificates.

**Transcription verification status:** the recurrences in `recurrences_v1.json` are
machine-checked for internal consistency by `checkers/check_C3b_moduli_map.py` (integrality
of all generated terms — a mistranscribed Apéry-like recurrence generically fails integrality
within a few terms because the (k+1)^d denominator stops clearing). This checks *consistency*,
not *provenance*: it cannot detect transcription of the wrong (but still integral) sequence.
Provenance remains human-attested per the table above.
