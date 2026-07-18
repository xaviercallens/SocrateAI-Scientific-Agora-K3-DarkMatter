#!/usr/bin/env python3
"""
run_s2_1_kernel_swap_battery.py - Execute GATE D-1v2 Kernel-Swap Battery v2

Preregistered execution script for S2-1 observable validation.
- Loads preregistration from: data/k3t2/S2_1_OBSERVABLE_DESIGN_PREREGISTERED.md
- Runs mock calibration on null-hypothesis ensemble
- Executes kernel-swap battery (Tests 1-3 as defined in preregistration)
- Outputs results to: data/k3t2/d1_3b_kernel_swap_v2.json
- Decision: PASS/FAIL for GATE D-1v2

Authority: Preregistered. No changes to observable, decision rule, or threshold post-commitment.
Reproducibility: All randomness seeded; exact results reproducible.

Generated-by: Haiku 4.5 | Verified-by: epistemic-guardrails | Reviewed-by: pending
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add empirical_crucible to path
sys.path.insert(0, str(Path(__file__).parent))

from s2_1_singular_locus_observable import (
    run_kernel_swap_battery,
    calibrate_null_distribution,
)


def main():
    """Execute the full GATE D-1v2 kernel-swap battery v2."""

    repo_root = Path(__file__).parent.parent
    k3t2_dir = repo_root / "data" / "k3t2"
    k3t2_dir.mkdir(parents=True, exist_ok=True)

    calibration_file = k3t2_dir / "s2_1_mock_calibration.json"
    results_file = k3t2_dir / "d1_3b_kernel_swap_v2.json"

    print("=" * 70)
    print("  GATE D-1v2 Kernel-Swap Battery v2 (S2-1 Observable Validation)")
    print("=" * 70)
    print(f"\nTimestamp: {datetime.now().isoformat()}")
    print(f"Repository: {repo_root}")
    print(f"Output: {results_file}")
    print(f"Preregistration: {k3t2_dir}/S2_1_OBSERVABLE_DESIGN_PREREGISTERED.md")

    # Step 1: Calibrate null distribution
    print("\n" + "=" * 70)
    print("STEP 1: Mock Calibration (Null Hypothesis Ensemble)")
    print("=" * 70)

    if not calibration_file.exists():
        print(f"\nGenerating mock calibration (this will take ~5 minutes for 1000 mocks)...")

        # Calibrate both kernels
        calib_s7 = calibrate_null_distribution(n_mocks=1000, kernel="cooper_s7", verbose=True)
        calib_s10 = calibrate_null_distribution(
            n_mocks=1000, kernel="cooper_s10", verbose=True, seed=99
        )

        # Save calibration
        calibration_data = {
            "cooper_s7": calib_s7,
            "cooper_s10": calib_s10,
            "timestamp": datetime.now().isoformat(),
            "description": "Null-hypothesis ensemble calibration for GATE D-1v2 battery",
        }

        with open(calibration_file, "w") as f:
            json.dump(calibration_data, f, indent=2)

        print(f"\n✓ Calibration saved to {calibration_file}")

    else:
        print(f"Calibration already exists: {calibration_file}")
        with open(calibration_file, "r") as f:
            calibration_data = json.load(f)

    # Step 2: Run kernel-swap battery
    print("\n" + "=" * 70)
    print("STEP 2: Kernel-Swap Battery v2 (100 samples per test)")
    print("=" * 70)

    results = run_kernel_swap_battery(
        calibration_file=str(calibration_file),
        n_samples=100,
        output_file=str(results_file),
        verbose=True,
    )

    # Step 3: Report decision
    print("\n" + "=" * 70)
    print("STEP 3: GATE D-1v2 Decision Report")
    print("=" * 70)

    decision_info = results["gate_d1v2_decision"]
    print(f"\nStatus: {decision_info['status']}")
    print(f"S7 Kernel Specificity: {decision_info['s7_separation_sigma']:.2f}σ (threshold: 2.0σ)")
    print(f"S10 Kernel Specificity: {decision_info['s10_separation_sigma']:.2f}σ (threshold: 2.0σ)")
    print(f"\nRationale: {decision_info['rationale']}")

    if decision_info["status"] == "PASS":
        print("\n✓ GATE D-1v2 PASS")
        print("  Proceeding to:")
        print("    - D-3: Empirical rerun with validated observable")
        print("    - Stream 3: DarkMatter@Home volunteer dispatch")
    else:
        print("\n✗ GATE D-1v2 FAIL")
        print("  Observable requires redesign. Next iteration:")
        print("    - Review separation values for s7 and s10")
        print("    - Adjust observable definition (e.g., proximity metric weighting)")
        print("    - Return to S2-1 with revised preregistration")

    print("\n" + "=" * 70)
    print(f"Results saved to: {results_file}")
    print("Awaiting HUMAN adjudication for GATE D-1v2 final decision.")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
