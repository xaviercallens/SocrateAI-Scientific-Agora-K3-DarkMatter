# Stream 3 Mirror — WP-R Series Artifacts (T0 Decision D3)

**Mirrored:** 2026-07-26, per T0 decision **D3** (`briefs/T0_DECISIONS_2026_07_26.md`)
**Source repo:** `/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home` @ commit **`3d18add`**
("T0 sign-off WP-R5/R6/R7 (series closed) + Stream 2 Phase M directive"), clean tree
**Source data volume:** `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata`
**Integrity:** every file hashed in `MANIFEST.sha256` (25 files, ~824 KB)

Directive path mapping: where a directive references `docs/WP_R6_SURVEY_SCALES.md` etc.,
the mirrored copy lives at `stream3_mirror/<same relative path>`. Files are **read-only
references** here — the source of truth remains Stream 3's repo; re-mirror on change.

## Contents

| Group | Files |
|---|---|
| WP-R reports | `docs/WP_R5_3D_FIELD.md`, `docs/WP_R6_SURVEY_SCALES.md`, `docs/WP_R7_BETA_VARIANCE_SCAN.md` |
| Findings & sign-offs | `docs/FINDING_R_NULLDEGENERATE_2026_07_25.md`, `docs/WP_R5_R6_SONNET_REVIEW_SIGNOFF_2026_07_25.md`, `docs/T0_SIGNOFF_WP_R5_R6_R7_2026_07_25.md` |
| Terminus doc | `NO_PREDICTION_BRANCH.md` (Off-Ramp 3 / §8.5 — the branch Phase M must not re-walk) |
| Pipeline modules | `pipeline/{cosmology, realfield3d, siblings, gate, stream3_comparison}.py` |
| Scripts | `scripts/wp_r7_beta_variance_scan.py`, `scripts/check_tier_language.py` |
| Directive original | `briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md` (Phase M — executed as M1) |
| **Data outcomes** | `data/wp_r5_3d_field/*.json`, `data/wp_r7_beta_variance/*.json`, `data/survey_characterization/*.json` (results + their SHA manifests) |
| **Raw inputs** | `data/euclid_z/euclid_z_edf_{north,fornax,south}.csv`, `data/sdss_z/sdss_z_coma_cluster.csv` |

## Independent verification performed at mirror time (2026-07-26)

Per repo discipline, load-bearing claims were recomputed from the raw files **before**
adopting the mirror — independent of every report:

| Claim (T0 sign-off §1) | Recomputed here | Verdict |
|---|---|---|
| 36/50 Coma spectro rows share (RA, Dec) | `Counter` on raw CSV → 50 rows, 36 in duplicated (RA, Dec) groups | ✅ **REPRODUCED exactly** |
| Results JSON integrity | sha256(`wp_r7_results_2026_07_25.json`) = `b700f1f3…` = manifest value | ✅ **MATCH** |
| β₀ nonzero-variance 14/30 (Euclid) | direct recount from checksummed JSON | ✅ **14/30 exactly** |
| β₂ nonzero-variance 30/30 | direct recount | ✅ **30/30 exactly** |
| "β₁/β₂ 30/30" | recount: **β₁ alone = 29/30**; the "β₁ **or** β₂" union = 30/30 | ⚠️ see precision note |

### ⚠️ Precision note on WP-R7 §3 wording (recorded, not escalated)

WP-R7 §5's table is headed *"Nonzero-variance combos (β₁ **or** β₂)"* — under that union
definition, 30/30 **reproduces exactly**. But §3's prose says *"β₁ **and** β₂ show nonzero
null variance at every single (threshold, scheme) combination"* — strictly false: **β₁
alone is 29/30**. The single degenerate cell is
`euclid_z_edf_fornax · threshold 50% · scheme angular_csr · β₁ variance = 0.0`.

**Downstream consequence (why this is worth one line):** a future statistic choice of
β₁ *alone* at the 50% threshold under `angular_csr` on a fornax-like field would sit in a
zero-variance cell. Choose β₂, or the β₁/β₂ pair, or a higher threshold — which is
exactly the Phase M directive's own "and/or" phrasing, so no directive change is needed.
The T0 sign-off's "✅ Reproduced" is accurate under the §5 union definition it recounted.

## Epistemic status

Everything here is **ENGINEERING / Tier B** input material (per the WP-R docs' own
banners): survey accessibility envelope, statistic power map, null infrastructure. None
of it is a physics claim. It becomes usable in a pre-registered comparison only through
the Phase M process (M1 accepted as conditional negative; M2 gated on Route γ — see
`briefs/T0_DECISIONS_2026_07_26.md` D2).

**Generated-by:** Fable 5 (T1, executing T0 decision D3) | **Verified-by:** independent recomputation at mirror time (table above) | **Reviewed-by:** Xavier (T0) authorization 2026-07-26 (D3)
