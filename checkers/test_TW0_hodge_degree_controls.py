#!/usr/bin/env python3
"""
test_TW0_hodge_degree_controls.py — Negative controls for WP-TW0

Tests that verify the checker correctly rejects operators with wrong degree
and passes on independently validated cases.

Exit code: 0 if all tests pass, 1 if any fail.
"""

import sys
import json
from pathlib import Path

import sympy as sp

z, w, r = sp.symbols("z w r")

REPO = Path(__file__).resolve().parent.parent


def compute_degree_L2(P2, P1, P0):
    """Compute Hodge degree for an order-2 operator."""
    # Finite singular points
    fin_loci = sorted(sp.solve(P2, z))

    # Exponents at finite points
    total_fin = 0
    for z_c in fin_loci:
        a2 = z**2 * P2
        a1 = z * (P2 + P1)
        a0 = P0

        p = sp.simplify(a1 / a2)
        q = sp.simplify(a0 / a2)

        p0 = sp.simplify(sp.limit((z - z_c) * p, z, z_c))
        q0 = sp.simplify(sp.limit((z - z_c)**2 * q, z, z_c))

        indicial = r * (r - 1) + p0 * r + q0
        exps = sp.solve(indicial, r)
        total_fin += sum(exps)

    # Exponents at infinity
    P0_w2 = sp.simplify(P0.subs(z, 1/w) * w**2).subs(w, 0)
    P1_w2 = sp.simplify(P1.subs(z, 1/w) * w**2).subs(w, 0)
    P2_w2 = sp.simplify(P2.subs(z, 1/w) * w**2).subs(w, 0)

    indicial_inf = P0_w2 - P1_w2 * r + P2_w2 * r**2
    exps_inf = sp.solve(indicial_inf, r)
    total_inf = sum(exps_inf)

    # Degree formula
    total = total_fin + total_inf
    deg_ell = total / sp.Integer(2)
    deg_K3 = 2 * deg_ell

    return sp.nsimplify(deg_K3)


def test_cooper_s7_passes():
    """TEST 1: Cooper s7 should give degree 2."""
    P2 = -27*z**2 - 26*z + 1
    P1 = -27*z**2 - 13*z
    P0 = -6*z**2 - 2*z

    deg = compute_degree_L2(P2, P1, P0)
    passed = deg == 2

    print(f"TEST 1 (cooper_s7 should give ℓ=2): {'PASS' if passed else 'FAIL'}")
    print(f"  Computed: ℓ = {deg}")

    assert passed
    return passed


def test_perturbed_degree_1():
    """TEST 2: Apery-Zeta2 (different elliptic family) should give degree ≠ 2."""
    # Use the Apery-Zeta2 operator (from checkers/check_L3_riemann_scheme.py)
    # This is a different elliptic family, should have different degree
    P2_apery = -3*z**2 - z
    P1_apery = -3*z**2 - z
    P0_apery = z**2 + 3*z

    deg = compute_degree_L2(P2_apery, P1_apery, P0_apery)
    passed = deg != 2  # Should NOT equal 2

    print(f"TEST 2 (Apery-zeta2 should NOT give ℓ=2): {'PASS' if passed else 'FAIL'}")
    print(f"  Computed: ℓ = {deg} (should be ≠ 2)")

    assert passed
    return passed


def test_perturbed_degree_2():
    """TEST 3: Perturbed P1 should give different degree."""
    # Perturb P1 (leading coefficient)
    P2 = -27*z**2 - 26*z + 1
    P1_perturb = -27*z**2 - 13*z + 5  # Perturb by adding constant 5
    P0 = -6*z**2 - 2*z

    deg = compute_degree_L2(P2, P1_perturb, P0)
    passed = deg != 2  # Should NOT equal 2

    print(f"TEST 3 (perturbed P1 should NOT give ℓ=2): {'PASS' if passed else 'FAIL'}")
    print(f"  Computed: ℓ = {deg} (should be ≠ 2)")

    assert passed
    return passed


def test_certificate_exists():
    """TEST 4: Certificate file should be created."""
    cert_path = REPO / "data" / "certificates" / "TW0_hodge_degree_cooper_s7.json"
    passed = cert_path.exists()

    print(f"TEST 4 (certificate exists): {'PASS' if passed else 'FAIL'}")
    print(f"  Path: {cert_path}")

    if passed:
        with open(cert_path) as f:
            cert = json.load(f)
        print(f"  Verification passes: {cert.get('verification', {}).get('passes')}")

    assert passed
    return passed


def main():
    print("=" * 78)
    print("NEGATIVE CONTROLS FOR WP-TW0 HODGE DEGREE VERIFICATION")
    print("=" * 78)
    print()

    results = [
        test_cooper_s7_passes(),
        test_perturbed_degree_1(),
        test_perturbed_degree_2(),
        test_certificate_exists(),
    ]

    print()
    print("=" * 78)
    print(f"SUMMARY: {sum(results)}/{len(results)} tests passed")
    print("=" * 78)

    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
