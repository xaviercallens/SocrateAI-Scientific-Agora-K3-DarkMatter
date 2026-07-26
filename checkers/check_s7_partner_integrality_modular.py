#!/usr/bin/env python3
"""
check_s7_partner_integrality_modular.py — WHY the s7 partner is integral, from the source.

Reconstructs O'Brien 2016's modular parametrization from the thesis's OWN definitions and
verifies that it reproduces A279619 (= cooper_s7_partner), then exhibits the property that
actually forces integrality.

BACKGROUND
----------
Stream 1 kernel-proved (`sqrtSeq_dyadic`) that the order-2 partner of any Cooper-template
sequence lands in Z[1/2]: the square-root recursion g_n = (a_n - sum g_k g_{n-k})/2 divides
by 2 at every step. So 2-power denominators are the FORCED baseline, and s10 (17/2, 147/2,
6363/8, ...) and s18 (45/2, 429/2, 18387/8, ...) merely exhibit it. **s7 is the anomaly.**

The open question was why. T0 ruled the "Level 7 absorbs the 1/2's, Levels 10/18 do not"
explanation a [C] heuristic, correctly — it is not what makes the difference.

WHAT ACTUALLY FORCES IT
-----------------------
From the thesis, verified here in exact arithmetic:

    z7 = sum_{m,n} q^(m^2+mn+2n^2)              (3.13)  weight-1 theta series, disc -7
    Z7 = (7 P(q^7) - P(q)) / 6                  (3.14)  P = Ramanujan Eisenstein (2.14)
    X7 = eta_1^3 eta_7^3 / z7^3                 (3.15)
    z7 = sum_n c7(n) X7^n                       Theorem 6.1

The load-bearing fact is not "eta quotients have integer coefficients". It is that

    X7 = q - 9q^2 + 30q^3 - 15q^4 - ...   is a NORMALIZED integral uniformizer,

i.e. X7 is in q*Z[[q]] with leading coefficient EXACTLY 1. Expanding an integral q-series in
powers of such a uniformizer is integral, because inverting a monic integral series never
introduces a denominator. Integer coefficients alone would NOT suffice — a leading
coefficient of 2, say, would reintroduce exactly the 2-adic denominators we are trying to
explain. Normalization is the whole content.

So: c7(n) integral is a genuine corollary of the modular parametrization — but of
(3.13)+(3.15)+Thm 6.1 taken together, not of Theorem 6.1 alone, and not of "eta quotients
are integral".

A NOTE ON (3.15)
----------------
The pinned OCR of (3.15) renders the denominator ambiguously between z7 and Z7 and drops the
exponent. Three readings were tested; only eta_1^3 eta_7^3 / z7^3 reproduces A279619, and it
is the only weight-consistent one (eta_1^3 eta_7^3 has weight 3, z7 has weight 1, so z7^3
gives a weight-0 function as a uniformizer must be). Z7^3 and Z7^2 both fail. This checker
records the resolution so the ambiguity is not re-litigated. Note also z7^2 = Z7 exactly,
verified below — the two symbols denote genuinely different objects and OCR conflates them.

WHAT THIS DOES *NOT* ESTABLISH
------------------------------
Nothing about s10 or s18. Their partners are non-integral (Tier A, Stream 1), and no modular
parametrization by a normalized integral uniformizer is known for them. **Absence of a known
parametrization is not a proof that none exists**, so this checker asserts no negative result
about s10/s18 beyond the kernel-proved non-integrality of their partner sequences themselves.
It also assigns s18 no level, and makes no claim linking s18 to "Level 18".

Usage:
  python3 checkers/check_s7_partner_integrality_modular.py
  python3 checkers/check_s7_partner_integrality_modular.py --json data/certificates/S7_PARTNER_MODULAR.json
"""

import argparse
import json
import sys
from fractions import Fraction

N = 12
A279619 = ["1", "2", "22", "336", "6006", "117348", "2428272"]


def mul(a, b):
    r = [Fraction(0)] * N
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if i + j < N and y:
                    r[i + j] += x * y
    return r


def inv(a):
    r = [Fraction(0)] * N
    r[0] = 1 / a[0]
    for n in range(1, N):
        r[n] = -sum(a[k] * r[n - k] for k in range(1, n + 1)) / a[0]
    return r


def sigma(n):
    return sum(d for d in range(1, n + 1) if n % d == 0)


def build():
    P = [Fraction(0)] * N
    P[0] = Fraction(1)
    for n in range(1, N):
        P[n] = Fraction(-24 * sigma(n))
    P7 = [Fraction(0)] * N
    P7[0] = Fraction(1)
    for n in range(1, N):
        if 7 * n < N:
            P7[7 * n] = Fraction(-24 * sigma(n))
    Z7 = [(7 * P7[i] - P[i]) / 6 for i in range(N)]                       # (3.14)

    prod = [Fraction(0)] * N
    prod[0] = Fraction(1)
    for j in range(1, N):
        for _ in range(3):
            f = [Fraction(0)] * N
            f[0], f[j] = Fraction(1), Fraction(-1)
            prod = mul(prod, f)
        if 7 * j < N:
            for _ in range(3):
                f = [Fraction(0)] * N
                f[0], f[7 * j] = Fraction(1), Fraction(-1)
                prod = mul(prod, f)
    eta = [Fraction(0)] * N                                              # eta_1^3 eta_7^3
    for i in range(N - 1):
        eta[i + 1] = prod[i]

    z7 = [Fraction(0)] * N                                               # (3.13)
    for m in range(-8, 9):
        for n in range(-8, 9):
            e = m * m + m * n + 2 * n * n
            if e < N:
                z7[e] += 1
    return P, Z7, eta, z7


def expand_in(uniformizer, series, terms=7):
    c, rem = [], series[:]
    Xp = [Fraction(0)] * N
    Xp[0] = Fraction(1)
    for _ in range(terms):
        k = next((i for i, v in enumerate(Xp) if v != 0), None)
        cn = rem[k] / Xp[k]
        c.append(cn)
        rem = [rem[i] - cn * Xp[i] for i in range(N)]
        Xp = mul(Xp, uniformizer)
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    _, Z7, eta, z7 = build()
    readings = {
        "eta1^3 eta7^3 / z7^3": mul(z7, mul(z7, z7)),
        "eta1^3 eta7^3 / Z7^3": mul(Z7, mul(Z7, Z7)),
        "eta1^3 eta7^3 / Z7^2": mul(Z7, Z7),
    }

    print(f"z7^2 == Z7 (distinct objects, OCR conflates them): {mul(z7, z7) == Z7}\n")
    results, chosen = {}, None
    for name, den in readings.items():
        X = mul(eta, inv(den))
        c = expand_in(X, z7)
        normalized = X[0] == 0 and X[1] == 1
        integral_X = all(v.denominator == 1 for v in X)
        match = [str(v) for v in c] == A279619
        results[name] = {
            "X7_head": [str(v) for v in X[:5]],
            "normalized_uniformizer": bool(normalized),
            "X7_integral": bool(integral_X),
            "c7": [str(v) for v in c],
            "c7_integral": all(v.denominator == 1 for v in c),
            "reproduces_A279619": bool(match),
        }
        if match:
            chosen = name
        print(f"  X7 = {name}")
        print(f"     head {[str(v) for v in X[:5]]}   normalized: {normalized}   integral: {integral_X}")
        print(f"     c7   {[str(v) for v in c]}")
        print(f"     reproduces A279619: {match}\n")

    ok = chosen == "eta1^3 eta7^3 / z7^3" and sum(
        r["reproduces_A279619"] for r in results.values()) == 1
    print(f"unique reading that reproduces A279619: {chosen}")
    print("integrality mechanism: X7 is a NORMALIZED integral uniformizer (q + O(q^2), "
          "leading coeff exactly 1),\n  so expanding the integral theta series z7 in powers "
          "of it cannot introduce a denominator.")

    cert = {
        "checker": "check_s7_partner_integrality_modular.py",
        "checker_version": "1.0.0",
        "date": "2026-07-26",
        "source": "O'Brien 2016 (Massey), eqs (3.13),(3.14),(3.15), Thm 6.1 — "
                  "docs/literature/obrien_2016_massey_thesis.txt (hash-pinned)",
        "z7_squared_equals_Z7": bool(mul(z7, z7) == Z7),
        "readings_tested": results,
        "resolved_reading_of_eq_3_15": chosen,
        "mechanism": "X7 is a normalized integral uniformizer (leading coefficient exactly 1); "
                     "expanding an integral q-series in powers of such a uniformizer is integral. "
                     "NOT merely 'eta quotients have integer coefficients' — normalization is the "
                     "load-bearing property.",
        "scope_limits": [
            "establishes nothing about s10 or s18",
            "absence of a known modular parametrization for s10/s18 is not proof that none exists",
            "assigns s18 no level; makes no 'Level 18' claim",
        ],
        "verdict": "S7_PARTNER_INTEGRALITY_MODULAR_CONFIRMED" if ok else "INCONCLUSIVE",
        "picard_rank": None,
        "transcendental_rank": None,
    }
    if args.json:
        with open(args.json, "w") as f:
            json.dump(cert, f, indent=2)
        print(f"\nwrote {args.json}")
    print(f"\nVERDICT: {cert['verdict']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
