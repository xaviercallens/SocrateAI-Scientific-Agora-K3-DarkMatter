#!/usr/bin/env python3
"""
Compute binomial sequences S_{1,2} and S_{2,1} and search OEIS.
S_{1,2}(n) = ∑_k C(n,k) C(n+k,k)^2
S_{2,1}(n) = ∑_k C(n,k)^2 C(n+k,k)
"""

from math import comb
import json

def S_1_2(n):
    """Compute S_{1,2}(n) = ∑_k C(n,k) C(n+k,k)^2"""
    return sum(comb(n, k) * comb(n+k, k)**2 for k in range(n+1))

def S_2_1(n):
    """Compute S_{2,1}(n) = ∑_k C(n,k)^2 C(n+k,k)"""
    return sum(comb(n, k)**2 * comb(n+k, k) for k in range(n+1))

# Compute first 15 terms
n_max = 14
s12_terms = [S_1_2(n) for n in range(n_max + 1)]
s21_terms = [S_2_1(n) for n in range(n_max + 1)]

print("S_{1,2}(n) = ∑_k C(n,k) C(n+k,k)^2")
print(f"First {n_max + 1} terms: {s12_terms}")
print()

print("S_{2,1}(n) = ∑_k C(n,k)^2 C(n+k,k)")
print(f"First {n_max + 1} terms: {s21_terms}")
print()

# Output for OEIS search format
print("S_{1,2} for OEIS search: ", ",".join(map(str, s12_terms[:10])))
print("S_{2,1} for OEIS search: ", ",".join(map(str, s21_terms[:10])))
print()

# Save to file for later reference
data = {
    "S_1_2": {
        "formula": "∑_k C(n,k) C(n+k,k)^2",
        "terms": s12_terms,
        "oeis_search": ",".join(map(str, s12_terms[:10]))
    },
    "S_2_1": {
        "formula": "∑_k C(n,k)^2 C(n+k,k)",
        "terms": s21_terms,
        "oeis_search": ",".join(map(str, s21_terms[:10])),
        "note": "Should match A005258 (Apéry ζ(2))"
    }
}

with open("data/autoresearch_v2/binomial_sums_computed.json", "w") as f:
    json.dump(data, f, indent=2)

print("Saved to data/autoresearch_v2/binomial_sums_computed.json")
