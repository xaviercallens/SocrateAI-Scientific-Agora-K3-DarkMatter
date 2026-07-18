#!/usr/bin/env python3
"""
run_s2_1_kernel_swap_battery_vectorized.py

Execute GATE D-1v2 kernel-swap battery v2 using VECTORIZED observable.

Identical to run_s2_1_kernel_swap_battery.py, except:
  - Imports s2_1_singular_locus_observable_vectorized
  - Output file: d1_3b_kernel_swap_v2_vectorized.json
  - Logs indicate "VECTORIZED" version

Expected speedup: ~250x due to NumPy broadcasting vs loop.

Generated-by: Haiku 4.5 | Verified-by: epistemic-guardrails
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from s2_1_singular_locus_observable_vectorized import run_kernel_swap_battery

if __name__ == "__main__":
    output_file = Path(__file__).parent.parent / "data" / "k3t2" / "d1_3b_kernel_swap_v2_vectorized.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("GATE D-1v2 Kernel-Swap Battery v2 (VECTORIZED)")
    print("=" * 70)
    print(f"Output: {output_file}")
    print()

    results = run_kernel_swap_battery(
        n_samples=100,
        output_file=str(output_file),
        verbose=True
    )

    print()
    print("=" * 70)
    print(f"COMPLETE: {results['gate_d1v2_decision']['status']}")
    print(f"  S7 separation: {results['gate_d1v2_decision']['s7_separation_sigma']:.2f}σ")
    print(f"  S10 separation: {results['gate_d1v2_decision']['s10_separation_sigma']:.2f}σ")
    print("=" * 70)
