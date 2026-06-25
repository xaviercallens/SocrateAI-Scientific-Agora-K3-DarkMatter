#!/usr/bin/env python3
import sys
from math import comb
from fractions import Fraction
import numpy as np
import os
import json

def harmonic_sum(n):
    return sum(Fraction(1, j) for j in range(1, n + 1))

# --- SEQUENCES ---

# S20
def S20(n):
    return sum(comb(n, k)**4 * comb(n + k, k) for k in range(n + 1))

def compute_s20_B(n):
    val = Fraction(0)
    for k in range(n + 1):
        weight = 4 * (harmonic_sum(n) - harmonic_sum(n - k)) + (harmonic_sum(n + k) - harmonic_sum(n))
        val += Fraction(comb(n, k)**4 * comb(n + k, k)) * weight
    return val

# Apery
def Apery(n):
    return sum(comb(n, k)**2 * comb(n + k, k)**2 for k in range(n + 1))

def compute_apery_B(n):
    val = Fraction(0)
    for k in range(n + 1):
        weight = 2 * harmonic_sum(n + k) - 2 * harmonic_sum(n - k)
        val += Fraction(comb(n, k)**2 * comb(n + k, k)**2) * weight
    return val

# Domb
def Domb(n):
    return sum(comb(n, k)**2 * comb(2*k, k) * comb(2*(n-k), n-k) for k in range(n + 1))

def compute_domb_B(n):
    val = Fraction(0)
    for k in range(n + 1):
        weight = 2 * harmonic_sum(n) + 2 * harmonic_sum(2*n - 2*k) - 4 * harmonic_sum(n - k)
        val += Fraction(comb(n, k)**2 * comb(2*k, k) * comb(2*(n-k), n-k)) * weight
    return val

# Franel-5
def Franel5(n):
    return sum(comb(n, k)**5 for k in range(n + 1))

def compute_franel5_B(n):
    val = Fraction(0)
    for k in range(n + 1):
        weight = 5 * harmonic_sum(n) - 5 * harmonic_sum(n - k)
        val += Fraction(comb(n, k)**5) * weight
    return val

# Almkvist-Zudilin
def AZ(n):
    return sum((-1)**k * 3**(n - 3*k) * comb(3*k, k) * comb(n, 3*k) * comb(n + k, k) * comb(2*k, k) for k in range(n // 3 + 1))

def compute_az_B(n):
    val = Fraction(0)
    for k in range(n // 3 + 1):
        weight = harmonic_sum(n + k) - harmonic_sum(n - 3*k)
        term = (-1)**k * Fraction(1, 27**k) * Fraction(comb(n + k, k) * comb(n, 3*k) * comb(3*k, k) * comb(2*k, k))
        val += term * weight
    return val * 3**n

# --- MIRROR MAP SOLVER ---

def get_mirror_map(seq_func, B_func, D):
    f = [Fraction(seq_func(n)) for n in range(D + 1)]
    B = [B_func(n) for n in range(D + 1)]
    
    r = [Fraction(0)] * (D + 1)
    for n in range(1, D + 1):
        r[n] = B[n]
        for j in range(1, n):
            r[n] -= r[j] * f[n - j]
        r[n] /= f[0]
        
    e = [Fraction(0)] * (D + 1)
    e[0] = Fraction(1)
    for n in range(1, D + 1):
        for k in range(1, n + 1):
            e[n] += Fraction(k) * r[k] * e[n - k]
        e[n] /= Fraction(n)
        
    q = [Fraction(0)] * (D + 1)
    for d in range(1, D + 1):
        q[d] = e[d - 1]
    return q

def check_convergence(q, D):
    ratios = []
    for d in range(2, D + 1):
        if q[d-1] != 0:
            ratio = float(abs(q[d] / q[d-1]))
            ratios.append(ratio)
        else:
            ratios.append(None)
            
    valid_ratios = [r for r in ratios[-10:] if r is not None]
    if len(valid_ratios) < 5:
        return False, 0.0
    
    mean_val = np.mean(valid_ratios)
    std_val = np.std(valid_ratios)
    cv = std_val / mean_val if mean_val != 0 else float('inf')
    
    print(f"    Ratios: {[f'{r:.4f}' if r is not None else 'None' for r in ratios[-10:]]}")
    print(f"    CV: {cv:.4f}")
    
    # Almkvist-Zudilin ratios might alternate or be periodic because it's a step-3 sequence.
    # If the step-3 sequence is periodic, it still has a well-defined radius of convergence
    # (lim sup^{1/d} is what defines the radius of convergence).
    # If ratios are periodic or CV is reasonably bounded, we can consider it.
    # Let's see: if CV < 0.5, or if we look at the 3-step ratio (q_d / q_{d-3})^{1/3} which should converge.
    # Let's print them first.
    is_convergent = cv < 0.4
    return bool(is_convergent), mean_val

def run_pipeline():
    D = 32
    print(f"=== RUNNING CY-BENCHMARK PIPELINE Cutoff D={D} ===")
    
    sequences = {
        "S20": (S20, compute_s20_B),
        "Apery": (Apery, compute_apery_B),
        "Domb": (Domb, compute_domb_B),
        "Franel5": (Franel5, compute_franel5_B),
        "Almkvist-Zudilin": (AZ, compute_az_B)
    }
    
    results = {}
    
    # Compute S20 baseline first
    q_s20 = get_mirror_map(S20, compute_s20_B, D)
    C1_s20 = sum(q_s20[d] * d**2 for d in range(1, D + 1))
    Omega_s20 = sum(q_s20[d] for d in range(1, D + 1))
    ratio_s20 = C1_s20 / Omega_s20
    print(f"S20 baseline: C1 = {C1_s20}, Omega = {Omega_s20}, C1/Omega = {float(ratio_s20):.4f}")
    
    for name, (seq_func, B_func) in sequences.items():
        print(f"\nProcessing {name}...")
        q = get_mirror_map(seq_func, B_func, D)
        
        # Check integrality
        all_int = all(q[d].denominator == 1 for d in range(1, D + 1))
        print(f"  Integrality: {'PASS' if all_int else 'FAIL'}")
        
        # Check convergence
        is_conv, limit = check_convergence(q, D)
        print(f"  Convergence Ratio: {limit:.4f} (Convergent: {is_conv})")
        
        # Compute V''(0) and Omega
        C1 = sum(q[d] * d**2 for d in range(1, D + 1))
        Omega = sum(q[d] for d in range(1, D + 1))
        
        results[name] = {
            "q": [str(q[d]) for d in range(1, D + 1)],
            "C1": str(C1),
            "Omega": str(Omega),
            "all_int": bool(all_int),
            "is_conv": bool(is_conv),
            "convergence_limit": float(limit)
        }
        
    os.makedirs("scripts", exist_ok=True)
    with open("scripts/benchmark_math_results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("\nMath results successfully written to scripts/benchmark_math_results.json")

if __name__ == "__main__":
    run_pipeline()
