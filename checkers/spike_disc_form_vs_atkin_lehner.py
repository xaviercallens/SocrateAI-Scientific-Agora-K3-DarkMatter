#!/usr/bin/env python3
"""
spike_disc_form_vs_atkin_lehner.py -- exact count, for T = U + <2n>, of
  |O(q_T)|  : automorphisms of the discriminant form (Z/2n, q(x) = x^2/(2n) mod 2Z)
  |W(n)|    : size of the Atkin-Lehner group of Gamma_0(n) = number of exact divisors
              d || n (d | n, gcd(d, n/d) = 1)
and reports whether they agree.

WHY: the Deep Think s10 brief (briefs/DEEPTHINK_ALIGNMENT_BRIEF_S10_COMPOSITE_LEVEL_2026_08_01.md)
asks whether a Gamma_0(10)* (full Atkin-Lehner) mirror-map group contradicts T = U+<20>.
If |O(q_T)| = |W(n)| for every n, the extra Atkin-Lehner involutions at composite n have
the right count to come from lattice isometries of T acting on its discriminant group.
That would make Gamma_0(n)* the expected group rather than an anomaly. This script checks
ONLY that the counts agree. It does NOT show the two groups are isomorphic or that they
act compatibly (a hypothesis for review, SPIKE, not a certificate).

The U summand is unimodular, so the discriminant form of U+<2n> is that of <2n>.
An automorphism of the cyclic group Z/2n is x -> a x with gcd(a, 2n) = 1; it preserves
q iff a^2 x^2 / 2n = x^2 / 2n mod 2Z for all x, i.e. (a^2 - 1)/2n is an even integer,
i.e. a^2 = 1 mod 4n.

Negative control: the check must be able to FAIL. It is run on a lattice where the two
counts are known to differ by construction (a scrambled q: x^2/(2n) replaced by
x^2/n on Z/2n, which is not even the discriminant form of an even lattice). If that
comparison also "agrees" for all n, the script is vacuous and exits nonzero.

Exact integer arithmetic only. No inputs from refs/ (pure arithmetic).

Generated-by: Claude (Opus 5) | Verified-by: negative control below | Reviewed-by: N
"""
import sys
from math import gcd


def orth_disc_form(n, modulus_factor=4):
    """|{a in (Z/2n)^x : a^2 = 1 mod modulus_factor*n}|"""
    m = 2 * n
    return sum(1 for a in range(m) if gcd(a, m) == 1 and (a * a - 1) % (modulus_factor * n) == 0)


def atkin_lehner_size(n):
    return sum(1 for d in range(1, n + 1) if n % d == 0 and gcd(d, n // d) == 1)


def main():
    N_MAX = 60
    rows = [(n, orth_disc_form(n), atkin_lehner_size(n)) for n in range(1, N_MAX + 1)]
    for n in (7, 10):
        _, o, w = rows[n - 1]
        print(f"n={n:3d}  T=U+<{2*n}>  |O(q_T)|={o}  |W(n)|={w}  agree={o == w}")
    mismatches = [r for r in rows if r[1] != r[2]]
    print(f"n=1..{N_MAX}: {N_MAX - len(mismatches)} agree, {len(mismatches)} disagree"
          + (f": {mismatches}" if mismatches else ""))

    # negative control: wrong form (a^2 = 1 mod 2n instead of mod 4n)
    control_mismatch = [n for n in range(1, N_MAX + 1)
                        if orth_disc_form(n, modulus_factor=2) != atkin_lehner_size(n)]
    if not control_mismatch:
        print("NEGATIVE CONTROL FAILED: scrambled form also agrees everywhere -- check is vacuous")
        return 1
    print(f"negative control OK: scrambled form disagrees at {len(control_mismatch)} of {N_MAX} n "
          f"(first: n={control_mismatch[0]})")
    return 0 if not mismatches else 2


if __name__ == "__main__":
    sys.exit(main())
