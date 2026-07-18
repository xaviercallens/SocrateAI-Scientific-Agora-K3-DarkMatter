#!/usr/bin/env python3
"""
compare_battery_results.py

Once both batteries complete, compare results for:
1. Identical decision (PASS/FAIL)
2. Separation metrics within floating-point precision
3. Test values (means, stds, z-scores) match

Usage:
  python3 compare_battery_results.py

Output: Comparison report to stdout + saved to COMPARISON_REPORT.md
"""

import json
import sys
from pathlib import Path
import numpy as np


def load_results(filename):
    """Load JSON results from battery output."""
    path = Path(filename)
    if not path.exists():
        return None

    with open(path, 'r') as f:
        return json.load(f)


def compare_decisions(orig, vect):
    """Compare gate decisions."""
    orig_status = orig["gate_d1v2_decision"]["status"]
    vect_status = vect["gate_d1v2_decision"]["status"]

    return orig_status == vect_status, orig_status, vect_status


def compare_separations(orig, vect):
    """Compare separation metrics (should be identical within epsilon)."""
    sep_s7_orig = orig["gate_d1v2_decision"]["s7_separation_sigma"]
    sep_s7_vect = vect["gate_d1v2_decision"]["s7_separation_sigma"]

    sep_s10_orig = orig["gate_d1v2_decision"]["s10_separation_sigma"]
    sep_s10_vect = vect["gate_d1v2_decision"]["s10_separation_sigma"]

    eps = 1e-10

    match_s7 = abs(sep_s7_orig - sep_s7_vect) < eps
    match_s10 = abs(sep_s10_orig - sep_s10_vect) < eps

    return (match_s7, match_s10), (sep_s7_orig, sep_s7_vect), (sep_s10_orig, sep_s10_vect)


def compare_test_values(orig, vect):
    """Compare individual test metrics (means, stds, z-scores)."""
    eps = 1e-10
    mismatches = []

    for test_name in orig["tests"]:
        if test_name not in vect["tests"]:
            mismatches.append((test_name, "missing in vectorized"))
            continue

        orig_test = orig["tests"][test_name]
        vect_test = vect["tests"][test_name]

        for metric in ["mean", "std", "z_score_vs_mock"]:
            if metric not in orig_test or metric not in vect_test:
                continue

            orig_val = orig_test[metric]
            vect_val = vect_test[metric]
            diff = abs(orig_val - vect_val)

            if diff > eps:
                mismatches.append({
                    "test": test_name,
                    "metric": metric,
                    "original": orig_val,
                    "vectorized": vect_val,
                    "difference": diff,
                })

    return mismatches


def main():
    print("=" * 80)
    print("BATTERY RESULTS COMPARISON")
    print("=" * 80)

    # Paths
    data_dir = Path(__file__).parent.parent / "data" / "k3t2"
    orig_file = data_dir / "d1_3b_kernel_swap_v2.json"
    vect_file = data_dir / "d1_3b_kernel_swap_v2_vectorized.json"

    # Load results
    print(f"\nLoading: {orig_file}")
    orig = load_results(orig_file)

    print(f"Loading: {vect_file}")
    vect = load_results(vect_file)

    if orig is None:
        print("✗ Original results not found")
        return 1

    if vect is None:
        print("✗ Vectorized results not found")
        return 1

    print("✓ Both results loaded")

    # Comparisons
    print("\n" + "=" * 80)
    print("COMPARISON RESULTS")
    print("=" * 80)

    # Decision comparison
    print("\n1. Gate Decision")
    print("-" * 80)
    match_decision, orig_status, vect_status = compare_decisions(orig, vect)
    print(f"   Original: {orig_status}")
    print(f"   Vectorized: {vect_status}")
    if match_decision:
        print("   ✓ DECISIONS MATCH")
    else:
        print("   ✗ DECISIONS DIFFER (critical!)")

    # Separation metrics
    print("\n2. Separation Metrics (σ)")
    print("-" * 80)
    (match_s7, match_s10), (sep_s7_orig, sep_s7_vect), (sep_s10_orig, sep_s10_vect) = compare_separations(orig, vect)

    print(f"   S7 Separation:")
    print(f"     Original: {sep_s7_orig:.12f}σ")
    print(f"     Vectorized: {sep_s7_vect:.12f}σ")
    print(f"     Difference: {abs(sep_s7_orig - sep_s7_vect):.2e}")
    print(f"     {'✓ MATCH' if match_s7 else '✗ DIFFER'}")

    print(f"\n   S10 Separation:")
    print(f"     Original: {sep_s10_orig:.12f}σ")
    print(f"     Vectorized: {sep_s10_vect:.12f}σ")
    print(f"     Difference: {abs(sep_s10_orig - sep_s10_vect):.2e}")
    print(f"     {'✓ MATCH' if match_s10 else '✗ DIFFER'}")

    # Test values
    print("\n3. Individual Test Values")
    print("-" * 80)
    mismatches = compare_test_values(orig, vect)

    if not mismatches:
        print("   ✓ ALL TEST VALUES MATCH")
    else:
        print(f"   ✗ {len(mismatches)} MISMATCHES FOUND:")
        for i, mismatch in enumerate(mismatches[:10]):  # Show first 10
            print(f"      {i+1}. {mismatch}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    all_match = match_decision and match_s7 and match_s10 and not mismatches

    if all_match:
        print("\n✓✓✓ RESULTS IDENTICAL ✓✓✓")
        print("\nVectorized version validated! Ready for deployment:")
        print("  • Use for D-3 empirical rerun (250x faster)")
        print("  • Deploy to GPU infrastructure (CuPy compatible)")
        print("  • Archive original for reference")
        status = "VALIDATED"
    else:
        print("\n✗✗✗ RESULTS DIFFER ✗✗✗")
        print("\nDebug required before deployment:")
        print("  • Check floating-point accumulation order")
        print("  • Verify broadcasting shape logic")
        print("  • Review edge cases (NaN, infinity, zero)")
        status = "MISMATCH"

    # Write report
    report_file = data_dir / "COMPARISON_REPORT.md"

    report = f"""# Battery Results Comparison Report

**Timestamp:** {Path('/tmp').resolve()}
**Status:** {status}

## Decision Comparison
- **Original:** {orig_status}
- **Vectorized:** {vect_status}
- **Match:** {"✓ YES" if match_decision else "✗ NO"}

## Separation Metrics
- **S7 Separation:**
  - Original: {sep_s7_orig:.12f}σ
  - Vectorized: {sep_s7_vect:.12f}σ
  - Difference: {abs(sep_s7_orig - sep_s7_vect):.2e}
  - Match: {"✓ YES" if match_s7 else "✗ NO"}

- **S10 Separation:**
  - Original: {sep_s10_orig:.12f}σ
  - Vectorized: {sep_s10_vect:.12f}σ
  - Difference: {abs(sep_s10_orig - sep_s10_vect):.2e}
  - Match: {"✓ YES" if match_s10 else "✗ NO"}

## Test Value Discrepancies
Found: {len(mismatches)} mismatches
{f"First 10: {mismatches[:10]}" if mismatches else "None"}

## Conclusion
{"Results identical—vectorized version validated." if all_match else "Results differ—further investigation required."}

---
Generated by: compare_battery_results.py
"""

    report_file.write_text(report)
    print(f"\n✓ Report saved to {report_file}")

    return 0 if all_match else 1


if __name__ == "__main__":
    sys.exit(main())
