"""
k3t2_kernel_swap_battery.py — GATE D-1.3: Kernel-Swap Falsification Battery

Implements the preregistered test from K3xT2_DEEP_IMPROVEMENT_PLAN.md §3 (D-1.3):
runs identical density fields through four kernels (cooper_s7, cooper_s10, t103,
random_control) using the SAME bounded observable, and measures pairwise
correlation of the resulting Δ-maps.

PREREGISTERED DECISION RULE (committed before this script was run against
real/mock data — see plan §3, D-1.3):
  - If r(s7, random) > 0.95 → F1 FAILS: observable is kernel-blind (measures
    nonlinearity of the transform, not K3 geometry). Empirical claims freeze.
  - If r(s7, s10) > 0.95 AND r(s7, random) < 0.5 → DEGENERACY: the observable
    sees "K3-ness" (weight-3 sporadic structure) but cannot discriminate
    modular level. Promote to D-2.4 (singular-locus discriminant, Sonnet tier).
  - Otherwise → kernels are mutually discriminable; report the full matrix.

Usage: python3 scripts/k3t2_kernel_swap_battery.py
"""

import sys
import os
import json
import numpy as np
import logging
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lss_tensor_analytics'))
from k3_kernel_engine import KERNELS, construct_bounded_grid, verify_all_kernels

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kernel_swap_battery")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'k3t2')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def compute_fft_asymmetry(bounded_grid: np.ndarray, raw_density: np.ndarray) -> np.ndarray:
    """Δ = |FFT(bounded_grid) - FFT(raw_density)|, both z-normalized first."""
    b_norm = (bounded_grid - bounded_grid.mean()) / (bounded_grid.std() + 1e-10)
    r_norm = (raw_density - raw_density.mean()) / (raw_density.std() + 1e-10)
    fft_b = np.fft.fftn(b_norm)
    fft_r = np.fft.fftn(r_norm)
    return np.abs(np.fft.ifftn(np.abs(fft_b - fft_r)))


def run_kernel_swap_battery(density_grid: np.ndarray, sector_label: str = "test",
                           seed: int = 42) -> dict:
    """
    Run all 4 kernels on the same density field, compute Δ-maps, and the
    pairwise Pearson correlation matrix (preregistered discriminating statistic).
    """
    logger.info(f"=== Kernel-swap battery: sector '{sector_label}' ===")
    delta_maps = {}

    for name in KERNELS:
        if name == "random_control":
            # Ensure reproducibility for the destructive control
            from k3_kernel_engine import PeriodIntegralEngine
            engine = PeriodIntegralEngine(name)
            z = engine.density_to_modulus(density_grid.flatten())
            bounded = engine.bounded_period(z).reshape(density_grid.shape)
        else:
            _, bounded = construct_bounded_grid(name, density_grid)

        delta = compute_fft_asymmetry(bounded, density_grid)
        delta_maps[name] = delta
        logger.info(f"  {name}: mean_Δ={delta.mean():.6f}, max_Δ={delta.max():.6f}")

    # Pairwise Pearson correlations (preregistered statistic)
    names = list(KERNELS.keys())
    corr_matrix = {}
    for i, n1 in enumerate(names):
        for n2 in names[i+1:]:
            flat1 = delta_maps[n1].flatten()
            flat2 = delta_maps[n2].flatten()
            r = np.corrcoef(flat1, flat2)[0, 1]
            corr_matrix[f"{n1}__{n2}"] = float(r)
            logger.info(f"  r({n1}, {n2}) = {r:.4f}")

    # Preregistered decision rule
    r_s7_random = corr_matrix.get("cooper_s7__random_control", np.nan)
    r_s7_s10 = corr_matrix.get("cooper_s7__cooper_s10", np.nan)

    if r_s7_random > 0.95:
        verdict = "F1_FAILS_KERNEL_BLIND"
        verdict_text = ("F1 FAILS: r(s7, random) > 0.95 — the observable cannot distinguish "
                        "K3 structure from a growth-matched random sequence. It measures "
                        "transform nonlinearity, not geometry. Empirical claims (D-3) frozen "
                        "until the observable is redesigned.")
    elif r_s7_s10 > 0.95 and r_s7_random < 0.5:
        verdict = "DEGENERACY_S7_S10"
        verdict_text = ("s7/s10 degenerate under this observable (both K3, weight-3), but "
                        "clearly discriminated from random (r_random < 0.5). Promote to "
                        "D-2.4: exact singular-locus discriminant needed to separate s7 from s10.")
    elif r_s7_random < 0.5:
        verdict = "KERNELS_DISCRIMINABLE"
        verdict_text = ("Observable discriminates real K3 kernels from random control "
                        "(r_random < 0.5) and shows structure among s7/s10/t103.")
    else:
        verdict = "INCONCLUSIVE"
        verdict_text = (f"r(s7,random)={r_s7_random:.4f} falls between clean pass/fail "
                        f"thresholds (0.5, 0.95) — manual review required.")

    result = {
        "timestamp": datetime.now().isoformat(),
        "sector_label": sector_label,
        "density_grid_shape": list(density_grid.shape),
        "mean_delta": {k: float(v.mean()) for k, v in delta_maps.items()},
        "max_delta": {k: float(v.max()) for k, v in delta_maps.items()},
        "correlation_matrix": corr_matrix,
        "preregistered_verdict": verdict,
        "verdict_explanation": verdict_text,
    }

    logger.info(f"\n{'='*70}\nVERDICT: {verdict}\n{verdict_text}\n{'='*70}")
    return result


if __name__ == "__main__":
    logger.info("Verifying kernel integrity before battery run...")
    verify_all_kernels()

    # Use a reproducible mock density field (lognormal, matches Phase 1 mock)
    np.random.seed(123)
    mock_density = np.random.lognormal(mean=-1.0, sigma=1.5, size=(64, 64, 64))

    result = run_kernel_swap_battery(mock_density, sector_label="mock_lognormal_64cubed")

    output_path = os.path.join(OUTPUT_DIR, "d1_3_kernel_swap.json")
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    logger.info(f"\n✓ Results written to {output_path}")
    print(f"\nPREREGISTERED VERDICT: {result['preregistered_verdict']}")
