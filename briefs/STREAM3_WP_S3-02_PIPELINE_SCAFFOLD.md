# 🔧 WP S3-02: Pipeline Architecture & Golden Tests (Non-Blocking Prep)

**Work Package:** S3-02 (EXECUTION_PLAN.md §4)  
**Scope:** Build the V5 pipeline's shape — candidate-agnostic, parameter-free, ready for frozen PREDICTION.md to be plugged in  
**Blocker dependency:** None (generic scaffold; runs in parallel)  
**Duration:** 3–5 days  
**Output:** V5 pipeline code + closure & null golden tests (green in CI)  
**Binding constraint:** Zero hard-coded candidate-specific numbers; every observable a thin adapter config

---

## 1. Design Constraints (Binding — Do Not Relax)

Per EXECUTION_PLAN.md §4 WP S3-02 + VISION.md:

### 1.1 No Free Knobs
The pipeline **reads** frozen PREDICTION.md parameters and the Free-Parameter Ledger (WP P0-B).  
It does **NOT** define, guess, or vary parameters. If a number is not in PREDICTION.md or the ledger, it has no business being in the pipeline.

**Consequence:** m_φ, α_D, Λ_D are inputs; pipeline does not derive them.

### 1.2 TEST vs FIT Labeling (Not Cosmetic)
- **TEST:** A quantity compared against data it was never fitted to (shape prediction, spectral feature)
- **FIT:** A quantity tuned using the same data it's then compared against (normalization, amplitude)

**Binding rule:** Every output labeled TEST or FIT at the point of generation. Mislabeling either direction is how a falsification program becomes secretly unfalsifiable.

**Example:**
- P2 halo-profile **shape** (r_c vs M_halo power law) = TEST ✓ (predicted shape; not fitted to the same data)
- P2 halo-profile **normalization** (σ(v) amplitude) = FIT ✓ (tuned against the same stacked-profile data it's compared to)
- P1 PTA **spectrum** (frequency vs amplitude curve) = TEST ✓ (predicted; compared to published posteriors which were never fitted to this model)

### 1.3 Assumption-Tag Pass-Through
Every output the pipeline produces carries the assumption-ID list inherited from PREDICTION.md:
- [A-SEQ] sequence
- [A-VOL] volume
- [A-ONT] ontology
- [A-REL] relations

Do **NOT** strip these tags in transit. Every result carries: `output | TEST | [A-SEQ, A-VOL] | sensitivity ±X%`

### 1.4 Candidate Agnosticism
No hard-coded s7, s10, or candidate-specific numbers anywhere in the code.  
**PREDICTION.md** supplies: m_φ, α_D, Λ_D, observable choice.  
**Pipeline** is a thin wrapper: load PREDICTION.md → plug values → run → output TEST/FIT results.

---

## 2. Pipeline Architecture (High-Level Sketch)

```
PREDICTION.md (frozen, hash-pinned)
    ├─ m_φ(𝒱, g_s) relation [A-SEQ, A-VOL]
    ├─ α_D, Λ_D(𝒱, g_s) relation [A-ONT, A-REL]
    └─ Observable choice: P1 | P2 | Lyman-α
            ↓
  V5_Pipeline
    ├─ [adapter: P1] → NANOGrav/EPTA posteriors, predict nHz spectrum, TEST against published results
    ├─ [adapter: P2] → SDSS/DES profiles, predict r_c(M_halo) shape (TEST) + σ(v) amplitude (FIT)
    └─ [adapter: Lyman-α] → DESI/SDSS Ly-α power spectrum, compare against expected null
            ↓
  OBSERVATIONAL_REPORT.md (machine-generated tables + T0 interpretation)
    ├─ Result tables (pass/fail, likelihood, exclusion, TEST/FIT labels, assumption tags)
    ├─ Kill-condition evaluation (pre-committed branches: F3/F4/F5)
    └─ T0 interpretation (Tier C claims with in-sentence [C] markers)
```

### 2.1 Pipeline Input Spec

```python
# pipelines/v5_config.yaml (or .py)
observable: "P1"  # "P1" | "P2" | "Lyman-α"
prediction_hash: "abc123def456..."  # git hash of frozen PREDICTION.md

# The pipeline does NOT contain these; it reads them from PREDICTION.md:
# m_phi: null  (ERROR: must be in PREDICTION.md)
# alpha_D: null  (ERROR: must be in PREDICTION.md)
```

### 2.2 Pipeline Output Spec

```python
# pipelines/output_schema.json
{
  "observable": "P1",
  "prediction_hash": "abc123def456...",
  "test_vs_fit": {
    "quantity_1": "TEST",
    "quantity_2": "FIT"
  },
  "assumptions": ["A-SEQ", "A-VOL"],
  "results": {
    "pass": true,
    "likelihood": 0.87,
    "exclusion_sigma": 2.3,
    "p_value": 0.023
  },
  "kill_condition": {
    "triggered": false,
    "reason": null
  }
}
```

---

## 3. Golden Tests (Must Be Green Before Real Data)

### 3.1 Closure Test (Positive Control)

**Purpose:** Verify the pipeline correctly recovers injected signal.

**Method:**
1. Generate synthetic "data" matching the model's predicted shape/spectrum
2. Inject known signal (m_φ, α_D, Λ_D) at known amplitude
3. Run pipeline on synthetic data
4. Verify: pipeline recovers the injected parameters within stated tolerance

**Example (P1/PTA):**
```python
def test_closure_pta():
    # Inject synthetic nHz spectrum matching predicted m_phi = 1e-22 eV
    synthetic_spectrum = generate_synthetic_pta_spectrum(
        m_phi=1e-22, 
        alpha_D=0.5, 
        lambda_D=1e6,
        noise_level=0.05,
        seed=42
    )
    
    result = pipeline.run(
        observable="P1",
        data=synthetic_spectrum,
        freeze_predictions=PREDICTION_HASH
    )
    
    # Assert: m_phi recovered within 10% of injected
    assert abs(result['m_phi'] - 1e-22) / 1e-22 < 0.1
    assert result['pass'] == True
    assert result['test_vs_fit']['spectrum'] == 'TEST'
```

**Acceptance:** Recovered parameter within 5–10% of injected (tolerance pre-committed in test; not tuned after seeing result).

### 3.2 Null Test (Negative Control)

**Purpose:** Verify pipeline does NOT find signal when there is none.

**Method:**
1. Generate synthetic data with NO injected signal (null)
2. Run pipeline on null data
3. Verify: pipeline reports null / no detection at stated significance level (α = 0.05)
4. False-positive rate must be < α

**Example (P1/PTA):**
```python
def test_null_pta():
    # No signal, just noise
    null_spectrum = generate_null_pta_spectrum(
        noise_level=0.05,
        n_trials=100,
        seed=42
    )
    
    # Run pipeline 100 times on null realizations
    false_positive_count = 0
    for i in range(100):
        result = pipeline.run(
            observable="P1",
            data=null_spectrum[i],
            freeze_predictions=PREDICTION_HASH
        )
        if result['pass']:  # pipeline claims detection
            false_positive_count += 1
    
    # Assert: false-positive rate < 5%
    fpr = false_positive_count / 100
    assert fpr < 0.05, f"False positive rate {fpr:.3f} exceeds α=0.05"
```

**Acceptance:** False-positive rate ≤ 5% across 100 null realizations (no tuning after seeing results).

---

## 4. Pipeline Skeleton Code

Create `pipelines/v5_pipeline.py`:

```python
#!/usr/bin/env python3
"""
V5 Observational Test Pipeline
Generic, candidate-agnostic, parameter-free.
Reads frozen PREDICTION.md; outputs TEST/FIT-labeled results.
"""

import json
from pathlib import Path
from typing import Dict, List

class V5Pipeline:
    def __init__(self, observable: str, prediction_hash: str):
        """
        Args:
            observable: "P1" | "P2" | "Lyman-α"
            prediction_hash: git SHA of frozen PREDICTION.md
        """
        self.observable = observable
        self.prediction_hash = prediction_hash
        self.predictions = self._load_frozen_predictions()
        self.assumptions = self.predictions.get('assumptions', [])
    
    def _load_frozen_predictions(self) -> Dict:
        """Load frozen PREDICTION.md from git object store (not mutable filesystem copy)."""
        # Pseudocode; real implementation uses git show
        # git show <prediction_hash>:PREDICTION.md | parse YAML
        # Returns: {'observable': 'P1', 'm_phi': ..., 'assumptions': [...]}
        raise NotImplementedError
    
    def run(self, data: Dict) -> Dict:
        """
        Execute the test.
        
        Args:
            data: dataset dict with observable and measurements
        
        Returns:
            {
              'observable': str,
              'prediction_hash': str,
              'results': {...},
              'test_vs_fit': {...},
              'assumptions': [...],
              'kill_condition': {...}
            }
        """
        if self.observable == "P1":
            return self._run_p1(data)
        elif self.observable == "P2":
            return self._run_p2(data)
        elif self.observable == "Lyman-α":
            return self._run_lyman_alpha(data)
        else:
            raise ValueError(f"Unknown observable: {self.observable}")
    
    def _run_p1(self, data: Dict) -> Dict:
        """P1: PTA nHz spectrum comparison."""
        m_phi = self.predictions['m_phi']  # from PREDICTION.md
        predicted_freq = m_phi / 3.14159  # nHz
        predicted_spectrum = self._model_spectrum(predicted_freq)
        
        result = {
            'observable': 'P1',
            'prediction_hash': self.prediction_hash,
            'test_vs_fit': {'spectrum': 'TEST'},
            'assumptions': self.assumptions,
            'results': {
                'pass': self._test_pta(predicted_spectrum, data),
                'likelihood': self._likelihood(predicted_spectrum, data),
                'p_value': self._p_value(predicted_spectrum, data),
            },
            'kill_condition': self._check_kill_condition()
        }
        return result
    
    def _run_p2(self, data: Dict) -> Dict:
        """P2: Lensing halo-profile shape (TEST) + normalization (FIT)."""
        # Similar structure; split TEST/FIT labels
        result = {
            'observable': 'P2',
            'prediction_hash': self.prediction_hash,
            'test_vs_fit': {
                'profile_shape': 'TEST',
                'profile_normalization': 'FIT'
            },
            'assumptions': self.assumptions,
            'results': {...},
            'kill_condition': {...}
        }
        return result
    
    def _run_lyman_alpha(self, data: Dict) -> Dict:
        """Lyman-α null test."""
        # Test: expected null in Ly-α power spectrum
        result = {
            'observable': 'Lyman-α',
            'prediction_hash': self.prediction_hash,
            'test_vs_fit': {'spectrum': 'TEST'},
            'assumptions': self.assumptions,
            'results': {'pass': True, 'significance': 'null @ >3σ'},
            'kill_condition': {...}
        }
        return result
    
    def _check_kill_condition(self) -> Dict:
        """Evaluate pre-committed kill condition (from PREDICTION.md)."""
        # If no observable-relation survives the (V, g_s) elimination → trigger F5
        # Returns: {'triggered': bool, 'reason': str | None}
        return {'triggered': False, 'reason': None}
    
    # ... helper methods (test, likelihood, p_value, etc.) ...

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python v5_pipeline.py <prediction_hash>")
        sys.exit(1)
    
    prediction_hash = sys.argv[1]
    
    # Load frozen PREDICTION.md to determine observable
    pipeline = V5Pipeline(
        observable="P1",  # or read from PREDICTION.md
        prediction_hash=prediction_hash
    )
    
    # Load real data (from MANIFEST_STREAM3.md)
    data = load_observational_data("P1")
    
    # Run test
    result = pipeline.run(data)
    
    # Write output with provenance
    output = {
        **result,
        'provenance': 'Generated-by: pipelines/v5_pipeline.py (Tier B) | Verified-by: golden tests (closure, null) | Reviewed-by: pending T0'
    }
    
    with open('data/s3_observational_report_draft.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(json.dumps(output, indent=2))
```

---

## 5. Test File Structure

Create `tests/test_v5_pipeline.py`:

```python
import pytest
from pathlib import Path
from pipelines.v5_pipeline import V5Pipeline

PREDICTION_HASH = "frozen_v1.0"  # Use actual git commit SHA

def test_closure_pta():
    """Golden test 1: Pipeline recovers injected signal in synthetic PTA data."""
    # See § 3.1 above
    pass

def test_null_pta():
    """Golden test 2: Pipeline does not false-positive on null PTA data."""
    # See § 3.2 above
    pass

def test_closure_lensing():
    """Golden test 1: Pipeline recovers injected signal in synthetic lensing profiles."""
    pass

def test_null_lensing():
    """Golden test 2: Pipeline does not false-positive on null lensing data."""
    pass

def test_assumption_tags_preserved():
    """Assert: assumption tags from PREDICTION.md flow through to output unchanged."""
    pipeline = V5Pipeline(observable="P1", prediction_hash=PREDICTION_HASH)
    result = pipeline.run(data={...})
    
    assert 'assumptions' in result
    assert result['assumptions'] == pipeline.assumptions
    # Every sub-result also carries tags
    for key, val in result['results'].items():
        if isinstance(val, dict):
            assert 'assumptions' in val
```

Run tests:
```bash
pytest tests/test_v5_pipeline.py -v
# Expected: all green before touching real data
```

---

## 6. Acceptance Criteria (Definition of Done)

- [ ] **Pipeline architecture documented** (input/output spec, three adapters for P1/P2/Lyman-α)
- [ ] **Closure golden test GREEN** in CI (for at least one observable; others follow)
- [ ] **Null golden test GREEN** in CI (false-positive rate < α)
- [ ] **Zero hard-coded candidate numbers** in pipeline code (grep for "s7\|s10\|1e-22" → should find nothing)
- [ ] **TEST/FIT labels** present in all output (no unlabeled quantities)
- [ ] **Assumption tags preserved** end-to-end from PREDICTION.md to output
- [ ] **Provenance footer** on all pipeline outputs: Generated-by / Verified-by / Reviewed-by
- [ ] **Commit message includes:** "WP S3-02: Pipeline scaffold complete; closure and null golden tests green"

---

## 7. What NOT to Do (Binding)

❌ **Do NOT** hard-code m_φ = 1e-22 eV, α_D = 0.5, etc. in pipeline code  
❌ **Do NOT** select "P1 is the observable" in source; make it a config input  
❌ **Do NOT** strip assumption tags from intermediate results  
❌ **Do NOT** test the pipeline on real public data until golden tests pass  
❌ **Do NOT** change the TEST/FIT labels after seeing results  

---

## 8. Timeline

| Task | Duration | Parallel? |
|------|----------|-----------|
| Design pipeline architecture | 2–4 hours | Yes (parallel with S3-01) |
| Implement V5_Pipeline skeleton | 4–8 hours | Yes |
| Write closure test | 2–4 hours | Yes |
| Write null test | 2–4 hours | Yes |
| Add CI check | 1–2 hours | Yes |
| Debug test failures | 4–8 hours | Yes (iterate) |
| Final verification | 1–2 hours | Yes |
| **Total** | **3–5 days** | **Full parallelization with S3-01** |

---

## 9. Deliverables

**Files to commit:**
- `pipelines/v5_pipeline.py` (main pipeline, candidate-agnostic)
- `pipelines/v5_config.yaml` (config schema; no actual observable/numbers hardcoded)
- `tests/test_v5_pipeline.py` (closure + null golden tests)
- `.github/workflows/stream3_pipeline_test.yml` (CI: golden tests green before release)

**Commit message:**
```
feat(stream3): WP S3-02 pipeline scaffold complete

Build V5 pipeline shape (candidate-agnostic, parameter-free). Reads frozen
PREDICTION.md; outputs TEST/FIT-labeled results with assumption tags.

Three adapters (P1 PTA, P2 lensing, Lyman-α null) ready for config input.

Golden tests:
  - Closure: pipeline recovers injected signal in synthetic data ✓
  - Null: false-positive rate < 5% on null data ✓

Zero hard-coded candidate-specific numbers. Pipeline is thin wrapper around
PREDICTION.md values; ready to plug numbers once PREDICTION.md freezes.

Co-Authored-By: Stream 3 (Pipeline Architecture) <noreply@anthropic.com>
```

---

## 10. Next Steps After Completion

Once S3-01 and S3-02 are done:
1. ✅ Datasets fetched, hashed, manifested (S3-01)
2. ✅ Pipeline scaffold ready, golden tests green (S3-02)
3. ⏳ Wait for blockers to clear: K3_SELECTION_REPORT.md, ASSUMPTIONS.md sign-off, PREDICTION.md pinned
4. 🔄 Proceed to §4 Step 1 (S3-00 MVM Matching) once all blockers cleared

**Status:** Ready to execute now (no blocker dependencies)  
**Next:** Begin immediately in parallel with WP S3-01 (data acquisition)  
**Unblock:** S3-00 (Step 1 of full sequence) proceeds once all three blockers clear

