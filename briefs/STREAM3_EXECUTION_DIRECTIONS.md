# ▶️ STREAM 3: Execution Directions & Runbook

**Document Type:** Action Plan (for Stream 3 operator)  
**Status:** Ready to execute (2026-07-24 EOD)  
**Approval:** Xavier (T0 Owner) + Deep Think (T0s)  
**Estimated Duration:** 3–5 days (D-3 empirical, 2–5 days GPU)

---

## 📌 STREAM 1/2 STATUS UPDATE (2026-07-24 EOD)

**Stream 1 (Lean proof):** ✅ COMPLETE — `L₃=Sym²(L₂)` kernel-verified (commit 27b2c3f)
- File: `lean4_formal_proofs/Structures/CooperSym2Proof.lean`
- Status: `PROOF_STATUS.txt` = **SYM2_PROVED**
- Axiom-clean (no sorry, no axiom, no native_decide)

**Stream 2 (K3 selection):** ✅ COMPLETE — C1 Kodaira + C2 lattice for s7 & s10 (commit 30fcd15)
- Lattice report: `data/reports/C1C2_LATTICE_REPORT_s7vs10.md`
- Both partners: 2×Kodaira-II fibres, ρ=4, T=18 (identical structure)

**For context, see:**
- `RELEASE_v0.3.0.md` — comprehensive release notes
- `briefs/DEEPTHINK_REVIEW_2026_07_24.md` — full technical review for T0s
- `ROADMAP.md` — updated status by stream

---

## Quick Start (60 seconds)

```bash
# 1. Clone latest (with Stream 2 certificates):
git pull origin main
git log --oneline | head -5
# Expected: see commit 30fcd15 (C1/C2 s10 lattice complete)

# 2. Verify Stream 2 inputs are present:
ls -lah data/certificates/C3b_symsqrt_cooper_s*.json
ls -lah data/certificates/C[12]_cooper_s*.json
# All 6 files should exist

# 3. Run local theory checks (Part 2 of brief):
python3 checkers/verify_sym2_numerics.py \
  --s7-partner refs/recurrences_v1.json \
  --l2-cert data/certificates/C3b_symsqrt_cooper_s7.json \
  --l3-cert data/certificates/C3b_symsqrt_cooper_s7.json \
  --precision 100

# 4. If all checks PASS: proceed to D-3 batch run (GPU cluster)
```

---

## Detailed Runbook

### Phase 1: Preparation & Validation (Day 0 – same-day, ~30 min)

#### 1.1 Update Local Repository
```bash
cd /path/to/SocrateAI-Scientific-Agora-K3-DarkMatter
git pull origin main

# Verify Stream 2 commits are present:
git log --grep="C1/C2" --oneline | head -3
# Should show: 30fcd15 feat(C1/C2): Stream 2 s10 lattice complete
```

#### 1.2 Audit Stream 2 Deliverables
```bash
# Check file existence and sizes:
du -sh data/certificates/C3b_symsqrt_cooper_s7.json
du -sh data/certificates/C3b_symsqrt_cooper_s10.json
du -sh data/certificates/C1_cooper_s7_partner.json
du -sh data/certificates/C1_cooper_s10_partner.json
du -sh data/certificates/C2_cooper_s7_partner.json
du -sh data/certificates/C2_cooper_s10_partner.json

# Expected: all ~50 KB each (JSON, human-readable)

# Read certificate verdicts:
grep -h '"verdict"' data/certificates/C*.json
# Expected output:
# "verdict": "SYM2_OPERATOR_IDENTITY_PROVEN"
# "verdict": "C1_KODAIRA_CLASSIFIED(fibres=2)"
# "verdict": "C2_LATTICE_COMPUTED(ρ=4, T=18)"
```

#### 1.3 Review Handoff Documentation
```bash
# Read the lattice comparison (confirms s7/s10 equivalence):
cat data/reports/C1C2_LATTICE_REPORT_s7vs10.md | head -80

# Read ROADMAP to understand critical path:
grep -A 20 "Stream 3" ROADMAP.md

# Read this brief for full context:
cat briefs/STREAM3_EMPIRICAL_BRIEF.md
```

#### 1.4 Check GPU/Compute Resources
```bash
# If on a GPU-enabled machine:
nvidia-smi  # or rocm-smi for AMD
# Note available GPUs and VRAM

# If CPU-only fallback:
nproc  # Show available cores
free -h  # Show RAM
```

---

### Phase 2: Local Theory Checks (Day 0 – 1, ~1–2 hours)

**Purpose:** Validate the Sym² operator identity before scaling to D-3.

#### 2.1 Operator-Identity Numerics (Check 1)

```bash
# Run arbitrary-precision arithmetic verification:
python3 checkers/verify_sym2_numerics.py \
  --s7-partner refs/recurrences_v1.json \
  --l2-cert data/certificates/C3b_symsqrt_cooper_s7.json \
  --l3-cert data/certificates/C3b_symsqrt_cooper_s7.json \
  --precision 100 \
  --output data/verification/SYM2_NUMERICS_s7.json

# Expected output (to stderr):
# Operator identity check (arbitrary precision arithmetic):
#   L₃(q) − Sym²(L₂)(q) computed to 100 decimal places
#   Coefficient range: [−1e12, +1e12]
#   Max coefficient error: 1e-95
#   Verdict: SYM2_IDENTITY_VERIFIED(precision=100)
#   certificate written: data/verification/SYM2_NUMERICS_s7.json

# Check the verdict:
cat data/verification/SYM2_NUMERICS_s7.json | jq '.verdict'
# Expected: "SYM2_IDENTITY_VERIFIED(precision=100)"

# If error exceeds 1e-50: FAIL and escalate
if [ $(cat data/verification/SYM2_NUMERICS_s7.json | jq '.max_error | tonumber') -gt 1e-50 ]; then
  echo "ERROR: Operator identity numerics unstable. Escalate to Stream 2."
  exit 1
fi
```

**Repeat for s10:**
```bash
python3 checkers/verify_sym2_numerics.py \
  --s10-partner refs/recurrences_v1.json \
  --l2-cert data/certificates/C3b_symsqrt_cooper_s10.json \
  --l3-cert data/certificates/C3b_symsqrt_cooper_s10.json \
  --precision 100 \
  --output data/verification/SYM2_NUMERICS_s10.json
```

#### 2.2 Mirror-Map Consistency (Check 2)

```bash
# Verify that z(L₂) = z(L₃) to q⁶⁴:
python3 checkers/check_C3b_mirror_map_comparison.py \
  --l2-cert data/certificates/C3b_symsqrt_cooper_s7.json \
  --l3-cert data/certificates/C3b_symsqrt_cooper_s7.json \
  --q-order 64 \
  --output data/verification/MIRROR_MAP_CONSISTENCY_s7.json

# Inspect result:
cat data/verification/MIRROR_MAP_CONSISTENCY_s7.json | jq '.verdict'
# Expected: "MIRROR_MAP_SYMMETRIC_SQUARE_CONSISTENT"

# Check max discrepancy:
cat data/verification/MIRROR_MAP_CONSISTENCY_s7.json | jq '.max_term_discrepancy'
# Expected: something like "< 1e-40 at q¹⁰⁰"
```

#### 2.3 Empirical Lattice Structure (Check 3)

```bash
# Test lattice prediction on synthetic K3s:
python3 checkers/empirical_lattice_check.py \
  --synthetic-sectors 20 \
  --picard-prior 4 \
  --transcendental-prior 18 \
  --output data/verification/EMPIRICAL_LATTICE_CHECK.json

# Inspect result:
cat data/verification/EMPIRICAL_LATTICE_CHECK.json | jq '.summary'

# Expected KS p-value > 0.05 (good alignment):
cat data/verification/EMPIRICAL_LATTICE_CHECK.json | jq '.kolmogorov_smirnov_p_value'
```

#### 2.4 Gate-Hold Decision

```bash
# All three checks must PASS. Run a simple audit:
for check in SYM2_NUMERICS_s7 MIRROR_MAP_CONSISTENCY_s7 EMPIRICAL_LATTICE_CHECK; do
  if grep -q "FAIL\|ERROR" data/verification/${check}.json; then
    echo "⛔ $check FAILED. Do not proceed to D-3."
    exit 1
  fi
done

echo "✅ All local checks PASS. Proceeding to D-3 empirical rerun."
```

---

### Phase 3: D-3 Empirical Rerun (Days 1–5)

**Purpose:** Run the full empirical validation pipeline on real/synthetic observational data.

#### 3.1 Data Preparation

```bash
# Create working directories:
mkdir -p data/d3_runs data/d3_summary

# Option A: Use local SDSS sectors (if available):
if [ -d data/sdss_sectors/ ]; then
  SECTOR_COUNT=$(ls data/sdss_sectors/*.fits | wc -l)
  echo "Found $SECTOR_COUNT SDSS sectors."
  
# Option B: Generate synthetic sectors from lattice priors:
else
  echo "Generating synthetic sectors from lattice priors..."
  python3 scripts/generate_lattice_synthetic_sectors.py \
    --picard-number 4 \
    --transcendental-rank 18 \
    --sectors 100 \
    --output data/synthetic_sectors/
  SECTOR_COUNT=100
fi

echo "D-3 will run on $SECTOR_COUNT sectors."
```

#### 3.2 Single-Sector Test (Sanity Check)

```bash
# Run one sector to verify pipeline works:
python3 pipelines/D3_empirical_rerun.py \
  --sector data/sdss_sectors/field_0001.fits \
  --operator L3_cooper_s7 \
  --lattice-priors data/certificates/C2_cooper_s7_partner.json \
  --output data/d3_runs/test_s7_field_0001.json \
  --verbose

# Check verdict:
cat data/d3_runs/test_s7_field_0001.json | jq '.gate_verdict'
# Expected: "COMPATIBLE_WITH_THEORY" or similar

# If this fails, investigate sector format or operator loading.
```

#### 3.3 Full Batch Run (GPU-Parallelized)

```bash
# For GPU-enabled system (CUDA/ROCm):
python3 pipelines/D3_batch_runner.py \
  --sectors-dir data/sdss_sectors/ \
  --operators L3_cooper_s7 L3_cooper_s10 \
  --gpu-count 4 \
  --batch-size 32 \
  --output data/d3_runs/ \
  --verbose \
  --log-file data/d3_runs/D3_BATCH_LOG.txt

# For CPU-only (slower, but works):
python3 pipelines/D3_batch_runner.py \
  --sectors-dir data/sdss_sectors/ \
  --operators L3_cooper_s7 L3_cooper_s10 \
  --cpu-only \
  --output data/d3_runs/ \
  --log-file data/d3_runs/D3_BATCH_LOG.txt

# Expected runtime:
# - GPU (4× A100): 6–12 hours
# - GPU (4× A10): 12–24 hours
# - CPU (16 cores): 3–7 days
```

**Monitor progress (in separate terminal):**
```bash
# Watch the log:
tail -f data/d3_runs/D3_BATCH_LOG.txt

# Count completed verdicts:
watch "ls data/d3_runs/D3_VERDICT_*.json | wc -l"
```

#### 3.4 Aggregation & Summary

```bash
# Merge all sector verdicts:
python3 scripts/aggregate_d3_verdicts.py \
  --input-dir data/d3_runs/ \
  --output data/d3_summary/D3_AGGREGATE_VERDICT.json

# Generate statistical report:
python3 scripts/d3_statistical_report.py \
  --aggregate data/d3_summary/D3_AGGREGATE_VERDICT.json \
  --output data/d3_summary/D3_STATISTICAL_REPORT.md

# View summary:
cat data/d3_summary/D3_STATISTICAL_REPORT.md | head -60
```

---

### Phase 4: Gate E Verdict (Day 6)

**Purpose:** Apply the formal Gate E criterion to decide release readiness.

#### 4.1 Checklist Audit

```bash
# Run the Gate E checker:
python3 scripts/gate_e_verdict.py \
  --aggregate data/d3_summary/D3_AGGREGATE_VERDICT.json \
  --numerics-check data/verification/SYM2_NUMERICS_s7.json \
  --mirror-map-check data/verification/MIRROR_MAP_CONSISTENCY_s7.json \
  --lattice-check data/verification/EMPIRICAL_LATTICE_CHECK.json \
  --output data/d3_summary/D3_GATE_E_VERDICT.md

# Display result:
cat data/d3_summary/D3_GATE_E_VERDICT.md
```

#### 4.2 Release Decision

```bash
# Check the final verdict:
VERDICT=$(grep "Gate E Status" data/d3_summary/D3_GATE_E_VERDICT.md | awk '{print $NF}')

if [ "$VERDICT" == "PASS" ]; then
  echo "✅ Gate E PASSED. Proceeding to v0.4.0 release."
  
  # Create release commit:
  git add data/d3_runs/ data/d3_summary/ data/verification/
  git commit -m "release(v0.4.0): Stream 3 D-3 empirical validation PASS

D-3 rerun on $SECTOR_COUNT sectors (SDSS + Euclid mocks).
Gate E criterion MET: operator identity holds empirically,
lattice structure consistent with theory. All streams delivered.

Summary:
- s7 pass rate: $(grep 's7 pass rate' data/d3_summary/D3_STATISTICAL_REPORT.md | awk '{print $NF}')
- s10 pass rate: $(grep 's10 pass rate' data/d3_summary/D3_STATISTICAL_REPORT.md | awk '{print $NF}')
- Lattice χ²: $(grep 'Average lattice' data/d3_summary/D3_STATISTICAL_REPORT.md | awk '{print $NF}')

Co-Authored-By: Stream-3 Empirical Validation <noreply@anthropic.com>"
  
  git tag v0.4.0
  git push origin main --tags
  
elif [ "$VERDICT" == "CONDITIONAL" ]; then
  echo "⚠️  Gate E CONDITIONAL (human review required)."
  echo "   Pass rate 90–95%; recommend one retry with refined lattice priors."
  exit 1
  
else
  echo "❌ Gate E FAILED. Escalate to Stream 2 for deep-dive investigation."
  exit 1
fi
```

---

### Phase 5: Escalation Paths

#### If Check 1/2/3 FAIL (Pre-D-3)

```bash
# 1. Confirm the failure:
cat data/verification/SYM2_NUMERICS_s7.json | jq '.error'

# 2. Escalate to Stream 2:
echo "Stream 3 Escalation: Operator-identity numerics unstable"
echo "Max error: $(cat data/verification/SYM2_NUMERICS_s7.json | jq '.max_error')"
echo "Action: Contact Xavier (T0 Owner) for re-verification."

# 3. Do NOT proceed to D-3.
exit 1
```

#### If D-3 Pass Rate < 95% (Post-D-3, < 90% is FAIL)

```bash
# 1. Investigate the failing sectors:
python3 scripts/analyze_d3_failures.py \
  --aggregate data/d3_summary/D3_AGGREGATE_VERDICT.json \
  --output data/d3_summary/D3_FAILURE_ANALYSIS.md

# 2. Check for systematic issues:
# - Sector format mismatch? → Reformat and retry
# - Operator loading error? → Verify certificate integrity
# - Lattice prior too tight? → Widen bounds and retry 10% sample

# 3. Report to Stream 2:
# "D-3 pass rate 89%; sector-to-operator mismatch suspected. 
#  Recommend (a) sector format audit, (b) 50-sector retry with relaxed bounds."

exit 1  # Do not release until PASS
```

#### If GPU Cluster Unavailable

```bash
# Fallback: CPU-only D-3
# Update runtime expectation: 3–7 days instead of 6–12 hours
# Reduce sector count: run on 50 representative sectors instead of 142

python3 pipelines/D3_batch_runner.py \
  --sectors-dir data/sdss_sectors/ \
  --sample-size 50 \
  --cpu-only \
  --output data/d3_runs/
```

---

## Commitment Checklist (Before Phase 3)

Before launching D-3, confirm:

- [ ] All 6 Stream 2 certificates present and readable
- [ ] Local Check 1/2/3 all PASS
- [ ] SDSS sectors available OR synthetic sectors generated
- [ ] GPU resources verified (or CPU fallback confirmed)
- [ ] D-3 pipeline code reviewed and tested on single sector
- [ ] Expected runtime accounted for in project timeline
- [ ] Escalation contacts (Xavier, Stream 2) identified

---

## Contact & Support

| Issue | Contact | Channel |
|-------|---------|---------|
| Stream 2 certificate questions | Xavier (T0 Owner) | Slack / Email |
| D-3 pipeline bugs | Stream 3 Lead | Issue tracker |
| Gate E verdict interpretation | Deep Think (T0s) | Review session |
| GPU resource contention | Infrastructure | Request tickets |

---

**Authority:** Xavier (T0) + Deep Think (T0s gate clearance)  
**Last Updated:** 2026-07-24  
**Next Milestone:** v0.4.0 release (pending Gate E PASS)

