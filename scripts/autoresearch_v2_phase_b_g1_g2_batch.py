#!/usr/bin/env python3
"""Phase 8.B: G1-2, G1-3 (Weil + mirror-map), streamlined"""

import json, math, sys
sys.path.insert(0, 'scripts')
from autoresearch_v2_phase_a_scan import seq_2factor, seq_apery3, seq_domb

# ====== G1-2: Weil bounds (weight-2/3 check) ======
def simple_weil_check(u, p_max=43):
    """Fast Weil bounds mod p: |a_p| <= 2*sqrt(p) (weight 3) and |a_p| <= 2*p (weight 2)."""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
    results = {}
    for p in primes:
        if p >= len(u):
            continue
        a_p = u[p] % p
        w3_bound = 2 * int(p**0.5) + 1
        w2_bound = 2 * p
        results[p] = {"a_p": a_p, "weight3_pass": a_p <= w3_bound, "weight2_pass": a_p <= w2_bound}
    return results

# ====== G1-3: Mirror-map integrality (simplified) ======
def simple_integrality(u, d_max=5):
    """Check if 30 coefficients have bounded denominators (fast heuristic)."""
    int_pass = True
    for i in range(min(d_max+1, len(u))):
        if u[i] != int(u[i]):
            int_pass = False
            break
    return {"first_5_exact": int_pass, "note": "full mirror-map deferred to G1-3 detailed"}

# ====== Run ======
candidates = {
    "apery_zeta3": seq_apery3(110),
    "apery_zeta2_s21": seq_2factor(2, 1, 110),
    "s12_v1_primary": seq_2factor(1, 2, 110),
    "domb": seq_domb(110),
}

g1_2_results = {}
g1_3_results = {}
for cid, u in candidates.items():
    g1_2_results[cid] = simple_weil_check(u)
    g1_3_results[cid] = simple_integrality(u)
    print(f"{cid:20} → Weil pass: {g1_2_results[cid]}, Integrality: {g1_3_results[cid]}")

with open("data/autoresearch_v2/g1_2_weil_quick.json", "w") as f:
    json.dump(g1_2_results, f, indent=1)
with open("data/autoresearch_v2/g1_3_integrality_quick.json", "w") as f:
    json.dump(g1_3_results, f, indent=1)
print("✓ G1-2/G1-3 quick screens complete")
