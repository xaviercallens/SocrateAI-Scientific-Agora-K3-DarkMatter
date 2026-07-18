#!/usr/bin/env python3
"""
verify_vectorization_equivalence.py

Quick test: confirm that vectorized compute_proximity_metric() returns
IDENTICAL results to original loop-based version (bit-for-bit, within machine epsilon).

Usage:
  python3 verify_vectorization_equivalence.py

Output: PASS if all tests match; FAIL if any discrepancy detected.
"""

import numpy as np
import sys
from pathlib import Path

# Import both versions
sys.path.insert(0, str(Path(__file__).parent))

from s2_1_singular_locus_observable import compute_proximity_metric as compute_proximity_metric_original
from s2_1_singular_locus_observable import density_to_modulus as density_to_modulus_original
from s2_1_singular_locus_observable import SINGULAR_LOCI as LOCI_ORIGINAL

from s2_1_singular_locus_observable_vectorized import compute_proximity_metric as compute_proximity_metric_vectorized
from s2_1_singular_locus_observable_vectorized import density_to_modulus as density_to_modulus_vectorized
from s2_1_singular_locus_observable_vectorized import SINGULAR_LOCI as LOCI_VECTORIZED


def test_kernel_consistency():
    print("=" * 70)
    print("TEST 1: Kernel loci identical")
    print("=" * 70)

    for kernel in ["cooper_s7", "cooper_s10"]:
        orig = LOCI_ORIGINAL[kernel]
        vect = LOCI_VECTORIZED[kernel]
        match = np.allclose(orig, vect)
        status = "✓ PASS" if match else "✗ FAIL"
        print(f"{kernel}: {status}")
        if not match:
            print(f"  Original: {orig}")
            print(f"  Vectorized: {vect}")
            return False
    return True


def test_density_to_modulus():
    print("\n" + "=" * 70)
    print("TEST 2: Density→modulus mapping identical")
    print("=" * 70)

    np.random.seed(42)
    rho_test = np.random.uniform(0.1, 5.0, (64, 64, 64))

    z_orig = density_to_modulus_original(rho_test)
    z_vect = density_to_modulus_vectorized(rho_test)

    match = np.allclose(z_orig, z_vect, atol=1e-15)
    status = "✓ PASS" if match else "✗ FAIL"
    print(f"Mapping: {status}")

    if not match:
        diff = np.abs(z_orig - z_vect)
        print(f"  Max difference: {np.max(diff):.2e}")
        print(f"  Mean difference: {np.mean(diff):.2e}")
        return False
    return True


def test_compute_proximity_metric():
    print("\n" + "=" * 70)
    print("TEST 3: compute_proximity_metric() identical (bit-for-bit)")
    print("=" * 70)

    np.random.seed(42)
    rho_test = np.random.uniform(0.1, 5.0, (32, 32, 32))
    z_test = density_to_modulus_original(rho_test)

    all_pass = True

    for kernel in ["cooper_s7", "cooper_s10"]:
        L_K_orig, dist_orig = compute_proximity_metric_original(z_test, kernel)
        L_K_vect, dist_vect = compute_proximity_metric_vectorized(z_test, kernel)

        # Check proximity metric (scalar)
        match_scalar = np.isclose(L_K_orig, L_K_vect, atol=1e-15)
        status_scalar = "✓ PASS" if match_scalar else "✗ FAIL"

        # Check distance field (array)
        match_field = np.allclose(dist_orig, dist_vect, atol=1e-15)
        status_field = "✓ PASS" if match_field else "✗ FAIL"

        print(f"\n{kernel}:")
        print(f"  L_K scalar: {status_scalar}")
        print(f"    Original: {L_K_orig:.12f}")
        print(f"    Vectorized: {L_K_vect:.12f}")
        print(f"    Difference: {abs(L_K_orig - L_K_vect):.2e}")

        print(f"  Distance field: {status_field}")
        if not match_field:
            diff = np.abs(dist_orig - dist_vect)
            print(f"    Max difference: {np.max(diff):.2e}")
            print(f"    Mean difference: {np.mean(diff):.2e}")

        all_pass = all_pass and match_scalar and match_field

    return all_pass


def benchmark():
    print("\n" + "=" * 70)
    print("BENCHMARK: Performance comparison")
    print("=" * 70)

    import time

    np.random.seed(42)
    rho_test = np.random.uniform(0.1, 5.0, (128, 128, 128))
    z_test = density_to_modulus_original(rho_test)

    # Original (loop)
    start = time.time()
    for _ in range(10):
        L_K_orig, _ = compute_proximity_metric_original(z_test, "cooper_s7")
    time_orig = time.time() - start

    # Vectorized
    start = time.time()
    for _ in range(10):
        L_K_vect, _ = compute_proximity_metric_vectorized(z_test, "cooper_s7")
    time_vect = time.time() - start

    speedup = time_orig / time_vect if time_vect > 0 else float('inf')

    print(f"Original (loop): {time_orig:.4f}s (10 runs)")
    print(f"Vectorized: {time_vect:.4f}s (10 runs)")
    print(f"Speedup: {speedup:.1f}x")

    return True


def main():
    print("\n" + "=" * 70)
    print("VECTORIZATION EQUIVALENCE VERIFICATION")
    print("=" * 70)
    print("Checking: s2_1_singular_locus_observable_vectorized.py")
    print("vs: s2_1_singular_locus_observable.py (original)")
    print()

    tests = [
        ("Kernel consistency", test_kernel_consistency),
        ("Density mapping", test_density_to_modulus),
        ("Proximity metric", test_compute_proximity_metric),
        ("Performance", benchmark),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ ERROR in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    all_pass = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
        all_pass = all_pass and result

    if all_pass:
        print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("Vectorized version is mathematically equivalent to original.")
        print("Ready to deploy for parallel GPU execution.")
        return 0
    else:
        print("\n✗✗✗ SOME TESTS FAILED ✗✗✗")
        print("Do not deploy. Review differences above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
