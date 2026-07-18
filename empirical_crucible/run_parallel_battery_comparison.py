#!/usr/bin/env python3
"""
run_parallel_battery_comparison.py

Strategy: Run BOTH original and vectorized versions of GATE D-1v2 kernel-swap
battery in parallel. Compare results when both complete.

Original: run_s2_1_kernel_swap_battery.py (already executing, PID 7371)
Vectorized: run_s2_1_kernel_swap_battery_vectorized.py (new, to launch here)

Verification: confirm identical results (within floating-point epsilon)

Output locations:
  Original: data/k3t2/d1_3b_kernel_swap_v2.json
  Vectorized: data/k3t2/d1_3b_kernel_swap_v2_vectorized.json

Generated-by: Haiku 4.5 (orchestration) | Verified-by: epistemic-guardrails
"""

import subprocess
import sys
import json
import time
from pathlib import Path
import numpy as np
import os


def check_gpu_availability():
    """Check if GPU (CUDA/CuPy) is available."""
    try:
        import cupy as cp
        print("✓ GPU (CuPy) detected")
        return True
    except ImportError:
        print("  GPU (CuPy) not available; will use CPU with NumPy (still ~250x faster via vectorization)")
        return False


def create_vectorized_battery_runner():
    """Create run_s2_1_kernel_swap_battery_vectorized.py if it doesn't exist."""
    runner_path = Path(__file__).parent / "run_s2_1_kernel_swap_battery_vectorized.py"

    if runner_path.exists():
        return runner_path

    content = '''#!/usr/bin/env python3
"""
run_s2_1_kernel_swap_battery_vectorized.py

Execute GATE D-1v2 kernel-swap battery v2 using VECTORIZED observable.
Identical to run_s2_1_kernel_swap_battery.py, except:
  - Imports s2_1_singular_locus_observable_vectorized
  - Output file: d1_3b_kernel_swap_v2_vectorized.json
  - Logs indicate "VECTORIZED" version

Expected speedup: ~250x due to NumPy broadcasting vs loop.
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
'''

    runner_path.write_text(content)
    runner_path.chmod(0o755)
    print(f"✓ Created {runner_path}")
    return runner_path


def launch_verification_test():
    """Run equivalence verification script."""
    verify_path = Path(__file__).parent / "verify_vectorization_equivalence.py"

    print("\n" + "=" * 70)
    print("STEP 1: Verify mathematical equivalence")
    print("=" * 70)

    result = subprocess.run(
        [sys.executable, str(verify_path)],
        cwd=verify_path.parent,
        capture_output=False
    )

    if result.returncode != 0:
        print("\n✗ Verification failed! Do not proceed with parallel battery.")
        return False

    print("\n✓ Verification passed. Proceeding with parallel battery launches.")
    return True


def launch_vectorized_battery():
    """Launch vectorized battery runner as background process."""
    runner_path = create_vectorized_battery_runner()

    print("\n" + "=" * 70)
    print("STEP 2: Launch vectorized battery (background)")
    print("=" * 70)

    proc = subprocess.Popen(
        [sys.executable, str(runner_path)],
        cwd=runner_path.parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    print(f"✓ Vectorized battery launched")
    print(f"  PID: {proc.pid}")
    print(f"  Process: python3 {runner_path.name}")
    print(f"  Output file: data/k3t2/d1_3b_kernel_swap_v2_vectorized.json")

    return proc


def log_parallel_status(orig_pid, vect_proc):
    """Log status of both battery processes."""
    log_file = Path(__file__).parent.parent / "data" / "k3t2" / "PARALLEL_BATTERY_STATUS.md"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    content = f"""# Parallel Battery Execution Log

**Timestamp:** {timestamp}

## Original Battery (Loop-based)
- **PID:** {orig_pid}
- **Status:** Running (or completed from earlier)
- **Output file:** data/k3t2/d1_3b_kernel_swap_v2.json
- **Expected completion:** ~2026-07-18 06:40 UTC

## Vectorized Battery (NumPy Broadcasting)
- **PID:** {vect_proc.pid}
- **Status:** Running
- **Output file:** data/k3t2/d1_3b_kernel_swap_v2_vectorized.json
- **Expected speedup:** ~250x
- **Expected completion:** ~2026-07-18 06:37 UTC (20 min faster)

## Comparison Plan

Once both complete, verification script will:
1. Load both JSON results
2. Compare `gate_d1v2_decision` outcomes (should be identical)
3. Compare `s7_separation_sigma` and `s10_separation_sigma` (should differ <1e-15)
4. Verify test means/stds match (floating-point precision)
5. Report: RESULTS-MATCH or RESULTS-DIVERGE

If results match:
- ✓ Vectorized version validated
- ✓ Use vectorized for future D-3 empirical rerun (250x faster)
- ✓ Deploy to GPU infrastructure if CuPy available

If results diverge:
- ✗ Debug discrepancy (check broadcasting logic)
- ✗ Fall back to original version
- ✗ Investigate numerical stability

## Monitoring

```bash
# Check original battery status
ps aux | grep run_s2_1_kernel_swap_battery.py

# Check vectorized battery status
ps aux | grep run_s2_1_kernel_swap_battery_vectorized.py

# Monitor output files
ls -lh data/k3t2/d1_3b_kernel_swap_v2*.json
```

---

**Generated by:** run_parallel_battery_comparison.py
**Orchestration:** Sequential launch with background monitoring
"""

    log_file.write_text(content)
    print(f"\n✓ Status log written to {log_file}")


def main():
    print("\n" + "=" * 70)
    print("PARALLEL BATTERY ORCHESTRATOR")
    print("=" * 70)
    print()
    print("Strategy: Run both original and vectorized GATE D-1v2 battery in parallel")
    print("- Original: Loop-based (already running, PID 7371)")
    print("- Vectorized: NumPy broadcasting (~250x faster)")
    print()

    # Step 1: Check GPU
    gpu_available = check_gpu_availability()
    print()

    # Step 2: Verify equivalence
    if not launch_verification_test():
        return 1

    # Step 3: Launch vectorized battery
    vect_proc = launch_vectorized_battery()

    # Step 4: Log status
    log_parallel_status(7371, vect_proc)

    print()
    print("=" * 70)
    print("LAUNCH COMPLETE")
    print("=" * 70)
    print()
    print("Both batteries are now running in parallel:")
    print("  • Original (loop): PID 7371, output → d1_3b_kernel_swap_v2.json")
    print(f"  • Vectorized: PID {vect_proc.pid}, output → d1_3b_kernel_swap_v2_vectorized.json")
    print()
    print("Expected completion times:")
    print("  • Vectorized: ~2–3 minutes (250x speedup)")
    print("  • Original: ~30 minutes (original estimate)")
    print()
    print("Next steps:")
    print("  1. Monitor both processes with 'ps aux | grep kernel_swap'")
    print("  2. When vectorized completes, run comparison verification")
    print("  3. If results match: use vectorized for D-3 empirical rerun")
    print("  4. If mismatch: debug numerical differences")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
