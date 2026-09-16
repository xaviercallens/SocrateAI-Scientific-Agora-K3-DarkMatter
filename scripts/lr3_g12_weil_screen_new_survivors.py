#!/usr/bin/env python3
"""
G1-2-style Weil-bound screen for the 3 NEW order-3 survivors found by the
LR-3 extended sieve (scripts/autoresearch_v2_phase_a_scan.py scan3 mode),
run 2026-09-16. EXPLORATORY SANDBOX, non-citable (CLAUDE.md rule 7).

Candidates (A,B,C) in T(A,B,C)(n) = sum_k C(n,k)^A C(n+k,k)^B C(2k,k)^C:
  (0,0,3) = A079727
  (0,1,1) = OEIS-unlisted
  (1,1,2) = A274789
(1,0,3)=A276536=T103 excluded: already a known GATE-C finalist, not new.

Method (Stienstra-Beukers 1985 unit-root recipe, reused verbatim from
scripts/modularity_screen.py's documented convention -- NOT re-derived):
  a_p := centered_residue( u((p-1)/2) mod p ),  p odd prime, u(n) defined
  only when (p-1)/2 is a valid index, i.e. p <= 2*n_max+1.
Weight-3 Ramanujan-Petersson bound under test: |a_p| <= 2p.
(The bound exponent for a weight-k eigenform is (k-1)/2; weight 3 -> 2p^1.)
"""
import math
import json

def seq_3factor(A, B, C, nmax):
    return [sum(math.comb(n, k) ** A * math.comb(n + k, k) ** B
                * math.comb(2 * k, k) ** C
                for k in range(n + 1)) for n in range(nmax + 1)]

def primes_upto(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(n + 1) if sieve[i]]

def centered_residue(x, p):
    r = x % p
    return r - p if r > p // 2 else r

CANDIDATES = {
    "T(0,0,3)_A079727": (0, 0, 3),
    "T(0,1,1)_OEIS_UNLISTED": (0, 1, 1),
    "T(1,1,2)_A274789": (1, 1, 2),
}

def main():
    p_max = 199
    primes = [p for p in primes_upto(p_max) if p >= 5]
    n_max = (p_max - 1) // 2  # need u up to this index
    results = {}
    for name, (A, B, C) in CANDIDATES.items():
        u = seq_3factor(A, B, C, n_max)
        rows = []
        n_fail = 0
        for p in primes:
            idx = (p - 1) // 2
            if idx > n_max:
                continue
            ap = centered_residue(u[idx], p)
            bound = 2 * p
            ok = abs(ap) <= bound
            if not ok:
                n_fail += 1
            rows.append({"p": p, "a_p": ap, "bound_2p": bound, "pass": ok})
        results[name] = {
            "n_primes_checked": len(rows),
            "n_fail": n_fail,
            "weil_weight3_pass": n_fail == 0,
            "table": rows,
        }
        print(f"{name}: {len(rows)} primes checked, {n_fail} failures, "
              f"weil_weight3_pass={n_fail == 0}")

    with open("data/autoresearch_v2/g1_2_weil_new_survivors.json", "w") as f:
        json.dump(results, f, indent=1)
    print("\nwritten: data/autoresearch_v2/g1_2_weil_new_survivors.json")

if __name__ == "__main__":
    main()
