---
name: empirical-data-validation
description: Enforces that all empirical claims use real observational data, not synthetic or simulated substitutes; tracks data lineage and validates reproducibility.
---

# Empirical Data Validation & Lineage Tracking

Use this skill before reporting any result that depends on observational data: cosmological fits, astrophysical bounds, or empirical validation claims.

## Core Rule: Real Data Only

**Synthetic or toy data is only acceptable if:**
1. Explicitly labeled as "toy" or "forecast"
2. Used to debug code logic, not to report scientific results
3. Never mixed with real data without clear separation
4. Always accompanied by a planned validation with real data

## Data Lineage Checklist

Before committing any data-dependent result:

- [ ] **Origin documented:** Where did the data come from? (e.g., "DESI DR1 BAO measurements, Adame et al. 2024, https://zenodo.org/...")
- [ ] **Retrieval method recorded:** How to obtain it again? (e.g., "bash scripts/fetch_desi_bao.sh")
- [ ] **Processing logged:** What cuts/transforms applied? (e.g., "z < 4.0 only, systematic errors added in quadrature per data release notes")
- [ ] **Version control:** Is the dataset committed (if small) or archived with DOI (if large)?
- [ ] **Reproducibility:** Can the exact same analysis be run on the exact same data 6 months from now?
- [ ] **Uncertainty propagation:** Are error bars from the data paper carried through? Not replaced by assumptions?

## For Each Dataset Used

Create a metadata comment in the code:

```python
# ============================================================================
# DATASET: DESI DR1 BAO Measurements
# ============================================================================
# Origin:     Adame et al. 2024, DESI Collaboration
# Archive:    https://data.desi.lbl.gov/desi/public/releases/edr/everest/
#             Public data release, no restrictions
# Citation:   DESI Collaboration (2024), arXiv:2404.03002
# DOI:        10.5281/zenodo.[ID]
# 
# Data fetch: scripts/fetch_desi_bao.sh
# Input file: data/observational/desi_dr1_bao.csv (cached)
# 
# Cuts applied:
#   - z ∈ [0.1, 4.0] (fiducial analysis range)
#   - Systematic errors added in quadrature (DR1 spec, table 2)
#   - No masking applied (full sample used)
# 
# Processing:
#   - D_M(z) and D_H(z) computed from Eq. 5, DR1 paper
#   - r_d = 147.09 ± 0.26 Mpc (Planck 2018 prior, fixed)
# 
# Validation:
#   - Reproduces Adame et al. Fig 3 within stated errors ✓
#   - No additional selection bias introduced ✓
# 
# Last verified: 2024-07-10
# Last updated: 2024-07-10
# ============================================================================

desi_data = pd.read_csv('data/observational/desi_dr1_bao.csv')
```

## Forbidden Practices

### ❌ Generating "Data" from Simulations
```python
# WRONG: Simulating data instead of using real observations
theoretical_values = solve_ode(params)
synthetic_desi = theoretical_values + np.random.normal(0, error_scale, size=len(z))
fit_params = minimize_loss(synthetic_desi, theoretical_values)
print(f"Best fit: {fit_params}")  # Report as science result!
```

✅ **Correct:** Use real data; compare to theory
```python
# Load real DESI data
real_data = pd.read_csv('data/observational/desi_dr1_bao.csv')
real_chi2 = compute_chi2(params, real_data)

# Generate forecast (clearly labeled)
forecast_precision = 0.02  # Euclid forecast sensitivity
theoretical_values = solve_ode(params)
print(f"Best fit χ²: {real_chi2} (real DESI DR1 data)")
print(f"Forecast (Euclid, σ < {forecast_precision}): would test...[separate section]")
```

### ❌ Citing "Preliminary Results"
```python
# WRONG: Using unpublished numbers you created
hargrove_2024_private_comm_value = 0.776
s8_best_fit = hargrove_2024_private_comm_value
```

✅ **Correct:** Use published results
```python
# From DES Y3 publication (Hamaus et al. 2024, PRL)
des_y3_s8_best = 0.776  # ± 0.017 (68% CL)
des_y3_s8_err = 0.017
```

### ❌ Hiding Dataset Choices
```python
# WRONG: No source, no traceability
chi2 = compute_fit(params, dataset)
```

✅ **Correct:** Explicit source
```python
# Load DES Y3 weak lensing, KiDS-1000 comparison (Hamaus et al. 2024)
chi2_des_y3 = compute_fit(params, load_dataset('des_y3_shear_2024'))
chi2_kids = compute_fit(params, load_dataset('kids_1000_shear_2020'))
```

## Fit Quality & Honest Reporting

### ✓ Always report:
- **Goodness-of-fit metric:** χ²/dof, reduced χ², or Bayesian Information Criterion
- **Degrees of freedom:** How many data points? How many fitted parameters?
- **Covariance matrix:** Full covariance in appendix or supplementary data
- **Residual analysis:** Do residuals scatter randomly, or is there systematic structure?
- **Sensitivity:** How much do best-fit values shift if you drop one dataset?

### ✗ Never report:
- "Qualitatively consistent" without numbers
- χ² without dof
- Best fits without error bars (or at minimum, 68% confidence regions)
- Single-dataset fits without cross-validation on held-out data

### ⚠ Marginal cases (require explicit caveat):
- χ²/dof > 1.5: State reason (intrinsic scatter? systematic errors? dataset incompatibility?)
- Small sample size (N < 5): Note "results driven by few points; await larger sample"
- Fit in publication bias range: Disclose that value was pre-selected (Bayesian posterior from prior fit)

## Example: Proper Empirical Validation Report

```python
# ============================================================================
# EMPIRICAL VALIDATION: K3×T² against DESI DR1 + Pantheon+ + DES Y3
# ============================================================================

datasets = {
    'desi_dr1_bao': {
        'file': 'data/observational/desi_dr1_bao.csv',
        'n_points': 9,
        'reference': 'Adame et al. 2024, arXiv:2404.03002',
        'dof': 9 - 2,  # 2 fitted parameters (w0, wa)
    },
    'pantheon_plus': {
        'file': 'data/observational/pantheon_plus_distance_moduli.csv',
        'n_points': 1701,
        'reference': 'Scolnic et al. 2022, ApJ 938:113',
        'dof': 1701 - 2,
    },
    'des_y3_weak_lensing': {
        'file': 'data/observational/des_y3_shear.csv',
        'n_points': 5,  # tomographic bins
        'reference': 'Hamaus et al. 2024, PRL',
        'dof': 5 - 2,
    },
}

results = {}
for name, meta in datasets.items():
    data = load_dataset(meta['file'])
    chi2 = compute_chi2(best_fit_params, data)
    dof = meta['dof']
    chi2_red = chi2 / dof
    
    results[name] = {
        'chi2': chi2,
        'chi2_reduced': chi2_red,
        'n_points': meta['n_points'],
        'dof': dof,
        'status': '✓ PASS' if chi2_red < 2.0 else '⚠ MARGINAL' if chi2_red < 3.0 else '✗ FAIL',
    }

print("\nFIT QUALITY REPORT")
print("=" * 70)
for name, res in results.items():
    print(f"{name:30s} χ²/dof = {res['chi2_red']:.2f} ({res['n_points']} points, {res['dof']} dof) {res['status']}")

print(f"\nCombined likelihood: χ²_total/dof_total = {sum(r['chi2'] for r in results.values()) / sum(r['dof'] for r in results.values()):.2f}")
print("\n[ANALYSIS] Dataset with highest χ²_red drives fit preference.")
print("[DISCLOSURE] Fit is dominated by Pantheon+ (1701 pts); DES/DESI provide weak constraints.")
print("[CROSS-VALIDATION] Refit excluding Pantheon+: w0 shifts by ±0.08 (outside 68% CL) → tension with Pantheon+")
```

## Data Retention & Archival

- **< 100 MB:** Commit directly to repo (`.gitignore` managed)
- **100 MB – 10 GB:** Archive to Zenodo with DOI; store retrieval script in repo
- **> 10 GB:** Reference with DOI + retrieval script; never commit

Example:
```bash
# scripts/fetch_observational_data.sh
wget https://zenodo.org/record/[ID]/files/desi_dr1_bao.csv -O data/observational/desi_dr1_bao.csv
echo "SHA256: [hash]" > data/observational/desi_dr1_bao.sha256
sha256sum -c data/observational/desi_dr1_bao.sha256 || exit 1
```

## Forecast vs. Constraint

Always distinguish clearly:

✓ **REAL CONSTRAINT:** "DESI DR1 BAO limits w₀ to [−1.05, −0.50] at 95% CL"
✗ **FORECAST (must label):** "Euclid is forecast to constrain w₀ to ±0.03"

When reporting forecasts, be explicit:
```latex
\textbf{Forecast [simulation-based]:} Assuming the model is correct and future 
systematics match design specifications, Euclid would constrain S_8(z) gradients 
to precision $\sigma_{S_8} < 0.01$ per bin. This forecast assumes the survey 
returns no surprises; see Appendix C for systematic error budget.
```

## Output: Data Audit Checklist

```
DATA AUDIT — Branch [name]

Dataset: DESI DR1 BAO
  ✓ Origin documented (Adame et al. 2024)
  ✓ Retrieval method in scripts/ folder
  ✓ Processing cuts logged in comments
  ✓ Cached in repo with SHA256 verification
  ✓ Error bars from data paper propagated
  ✓ Reproduces literature figures within errors

Dataset: Pantheon+ distance moduli
  ✓ All items above
  ✗ Cross-validation report missing → ADD before merge

Dataset: Synthetic forecast (Euclid)
  ✓ Labeled "forecast"
  ✓ Separate from real data in analysis
  ✓ Assumptions stated (systematic budget, fiducial cosmology)
  ⚠ Sensitivity to assumption (e.g., σ_sys) not shown → recommend for appendix

BLOCKING: None (forecasts correctly labeled)
RECOMMENDED: Cross-validation report for Pantheon+
```
