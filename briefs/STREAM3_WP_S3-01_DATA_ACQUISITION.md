# 🗂️ WP S3-01: Data Acquisition & Manifest (Non-Blocking Prep)

**Work Package:** S3-01 (EXECUTION_PLAN.md §4)  
**Scope:** Fetch, hash-pin, and manifest all public datasets used by candidate observables  
**Blocker dependency:** None (candidate-agnostic; runs in parallel)  
**Duration:** 1–2 days  
**Output:** data/MANIFEST.md + scripts/fetch_stream3_data.sh  
**CI check:** Checksum verification on every run

---

## 1. Datasets to Acquire (Table from STREAM_1_DIRECTIVE.md §2.1)

| Dataset | Observable | Source | Approx. size | Status |
|---|---|---|---|---|
| NANOGrav 15-yr posteriors | P1 (PTA) | Agazie et al. 2023, public release | 100 MB | — |
| EPTA Data Release 2 | P1 (PTA) | Liu et al. 2023, public release | 50 MB | — |
| SDSS stacked lensing profiles | P2 (halo) | Mandelbaum et al. 2013/2020 | 200 MB | — |
| DES Y3 lensing profiles | P2 (halo) | Leauthaud et al. 2024 | 150 MB | — |
| Euclid ERO (if available) | P2 (halo) | ESA/Euclid public archive | 500 MB–2 GB | Check availability |
| SDSS DR12 Lyman-α power spectrum | Lyman-α null | Palanque-Delabrouille et al. 2015 | 50 MB | — |
| DESI Early Data Release | Lyman-α null | DESI public archive | 200 MB | — |

**Total expected:** ~1.2–2.5 GB (manageable)

---

## 2. Execution Steps

### Step 2.1: Create Fetch Script Structure

```bash
#!/bin/bash
# scripts/fetch_stream3_data.sh
# Idempotent fetch + hash verification for all Stream 3 observational datasets

set -eu

DATADIR="data/stream3_observational"
MANIFEST="data/MANIFEST_STREAM3.md"

mkdir -p "$DATADIR"

# Helper: fetch if not present or verify if exists
fetch_and_verify() {
    local name="$1"
    local url="$2"
    local expected_sha256="$3"
    local filepath="$DATADIR/$name"
    
    if [ -f "$filepath" ]; then
        actual_sha=$(sha256sum "$filepath" | awk '{print $1}')
        if [ "$actual_sha" = "$expected_sha256" ]; then
            echo "✓ $name present and verified"
            return 0
        else
            echo "✗ $name exists but hash mismatch (expected $expected_sha256, got $actual_sha)"
            return 1
        fi
    fi
    
    echo "Fetching $name from $url..."
    curl -L -o "$filepath" "$url"
    
    actual_sha=$(sha256sum "$filepath" | awk '{print $1}')
    if [ "$actual_sha" = "$expected_sha256" ]; then
        echo "✓ $name fetched and verified"
        return 0
    else
        echo "✗ $name hash mismatch (expected $expected_sha256, got $actual_sha)"
        rm "$filepath"
        return 1
    fi
}

# Dataset 1: NANOGrav 15-yr posteriors
fetch_and_verify \
    "nanograv_15yr_posteriors.tar.gz" \
    "https://data.nanograv.org/11yr-dataset/real_data/raw/residuals/NANOGrav_11yr_Posterior.tar" \
    "PLACEHOLDER_SHA256_1"

# Dataset 2: EPTA DR2
fetch_and_verify \
    "epta_dr2.tar.gz" \
    "https://epta.inaf.it/releases/dr2/EPTA_DR2_public.tar" \
    "PLACEHOLDER_SHA256_2"

# [... repeat for all datasets ...]

echo "All datasets verified. Update $MANIFEST with results."
```

### Step 2.2: Populate MANIFEST.md

Create `data/MANIFEST_STREAM3.md`:

```markdown
# Stream 3 Observational Datasets Manifest

**Last updated:** 2026-07-24  
**Verification script:** scripts/fetch_stream3_data.sh (idempotent, safe to re-run)  
**CI check:** checksum verification on every run

## Datasets

| Name | Observable | Source | Size | SHA256 | Fetch date | Status |
|------|-----------|--------|------|--------|-----------|--------|
| NANOGrav 15-yr posteriors | P1 (PTA) | Agazie et al. 2023, https://data.nanograv.org/11yr-dataset | 100 MB | [COMPUTE] | [AUTO] | — |
| EPTA DR2 | P1 (PTA) | Liu et al. 2023, https://epta.inaf.it/releases/dr2 | 50 MB | [COMPUTE] | [AUTO] | — |
| SDSS stacked lensing | P2 (halo) | Mandelbaum et al. 2013/2020, https://data.sdss.org | 200 MB | [COMPUTE] | [AUTO] | — |
| DES Y3 lensing | P2 (halo) | Leauthaud et al. 2024, https://des.ncsa.illinois.edu | 150 MB | [COMPUTE] | [AUTO] | — |
| Euclid ERO | P2 (halo) | ESA Euclid public archive, https://www.esa.int/euclid | TBD | [TBD] | [TBD] | Check availability |
| SDSS DR12 Lyman-α | Lyman-α null | Palanque-Delabrouille et al. 2015, https://data.sdss.org/sas/dr12 | 50 MB | [COMPUTE] | [AUTO] | — |
| DESI EDR | Lyman-α null | DESI public, https://data.desi.lbl.gov | 200 MB | [COMPUTE] | [AUTO] | — |

## Anti-Hallucination Rule
Every URL and version tag in this table is **fetched and verified**, never transcribed from memory. 
If a source becomes unavailable or URL changes, this manifest is updated with a new fetch, not the old URL kept as "known good."

## CI Contract
- Fetch script runs on every commit (optional `--skip-fetch` flag for re-use in CI)
- SHA256 mismatch → CI failure (explicit; no silent fallback to old SHA)
- All datasets present and verified before any downstream pipeline runs

Generated-by: scripts/fetch_stream3_data.sh (automated) | Verified-by: sha256sum | Reviewed-by: pending T0
```

### Step 2.3: Verify Fetch Script

```bash
# Test the fetch script
cd /path/to/repo

# First run: fetches everything
bash scripts/fetch_stream3_data.sh

# Second run: should no-op (all present and verified)
bash scripts/fetch_stream3_data.sh

# Expected output:
# ✓ nanograv_15yr_posteriors.tar.gz present and verified
# ✓ epta_dr2.tar.gz present and verified
# [... etc ...]
```

### Step 2.4: Add CI Check

Create `.github/workflows/stream3_data_verify.yml` (or equivalent in your CI system):

```yaml
name: Stream 3 Data Manifest Verification

on: [push, pull_request]

jobs:
  verify-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Verify data manifest and checksums
        run: |
          bash scripts/fetch_stream3_data.sh --verify-only
          # If any SHA mismatch, script exits with error (CI fails)
```

---

## 3. Acceptance Criteria (Definition of Done)

- [ ] All 7 datasets in the table above **fetched and SHA256-verified**
- [ ] `data/MANIFEST_STREAM3.md` **populated with URLs, versions, SHA256 hashes, and fetch dates**
- [ ] `scripts/fetch_stream3_data.sh` **is idempotent** (second run no-ops if all present and verified)
- [ ] **No dataset referenced in repo without a MANIFEST.md entry** (search for filenames; grep source paths)
- [ ] **CI check green** (data verification on every commit)
- [ ] **Commit message includes:** "WP S3-01: Data acquisition — all observational datasets fetched, hash-pinned, manifest complete"

---

## 4. Anti-Hallucination Enforcement

This section is critical. The Stream 1/2 rule applies identically here:

> **Rule: Fetch and hash; never transcribe a number from memory.**

For each dataset:
1. **Find the official source** (published paper, official public archive, DOI registry)
2. **Extract the direct download URL** from that source (not a mirror; not a cached version)
3. **Download the artifact** to `data/stream3_observational/`
4. **Compute SHA256** of the downloaded file: `sha256sum filename`
5. **Record in MANIFEST.md**: URL, version/release tag (from source), SHA256, fetch timestamp
6. **Never** copy a SHA256 from a paper or assume "if I remember this URL, it's correct"

---

## 5. Fallback: Data Unavailable

If a dataset becomes unavailable (URL dead, archive deprecated):
1. **Do NOT** update the URL in the manifest to a mirror or a guess
2. **Instead:** Report the unavailability in MANIFEST.md with timestamp and archive-link (Archive.org, etc.)
3. **Escalate:** Comment in the repo that this observable's dataset is unavailable; flag for decision on Lyman-α fallback vs retry
4. **Update PREDICTION.md** (once pinned) to reflect which observable is actually testable

---

## 6. Timeline

| Task | Duration | Parallel? |
|------|----------|-----------|
| Write fetch script | 1–2 hours | Yes (parallel with WP S3-02) |
| Test all 7 dataset URLs | 2–4 hours | Yes |
| Compute SHA256 hashes | 1–2 hours | Yes |
| Populate MANIFEST.md | 1 hour | Yes |
| Add CI check | 1 hour | Yes |
| Final verification run | 30 min | Yes |
| **Total** | **1–2 days** | **Full parallelization** |

---

## 7. Deliverables

**Files to commit:**
- `data/MANIFEST_STREAM3.md` (manifest table with all URLs, SHA256s, fetch dates)
- `scripts/fetch_stream3_data.sh` (idempotent fetch script)
- `.github/workflows/stream3_data_verify.yml` (or CI equivalent)
- `.gitignore` update: ignore `data/stream3_observational/` locally (optional; artifact dirs often not committed)

**Commit message:**
```
feat(stream3): WP S3-01 data acquisition complete

Fetch, hash-pin, and manifest all observational datasets for P1 (PTA),
P2 (lensing), and Lyman-α null tests. All seven datasets verified.

- data/MANIFEST_STREAM3.md: URLs, versions, SHA256 hashes, fetch dates
- scripts/fetch_stream3_data.sh: idempotent fetch + verify script
- CI: automated checksum verification on every run

Anti-hallucination enforced: all URLs fetched and verified, not transcribed.

Co-Authored-By: Stream 3 (Data Acquisition) <noreply@anthropic.com>
```

---

## 8. What NOT to Do

❌ **Do NOT** start downloading datasets to your personal machine and uploading to GitHub LFS  
❌ **Do NOT** hard-code specific observable names in the fetch script (it's candidate-agnostic)  
❌ **Do NOT** assume "this is the same dataset as paper X used" without verifying the exact URL  
❌ **Do NOT** silently fall back to a different URL if one is unavailable (escalate instead)

---

**Status:** Ready to execute now (no blocker dependencies)  
**Next:** Begin immediately in parallel with WP S3-02 (pipeline scaffold)  
**Unblock:** S3-00 (Step 1 of full sequence) proceeds once all three blockers clear

