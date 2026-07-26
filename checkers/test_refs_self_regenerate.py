#!/usr/bin/env python3
"""
test_refs_self_regenerate.py — every refs recurrence must reproduce its own stored terms.

This guard exists because the register has now been silently corrupt twice:
  2026-07-20  two of five sequences (s18, zagier_A) had recurrences that did not
              reproduce their own terms. Never caught, because never run.
  2026-07-26  avs_sporadic3_s18 again — the entry was folded in that morning with the
              claim "independently re-verified ... integral to n=22", but the check had
              only compared the STORED initial_terms against A-vS's printed phi(x). The
              stored terms are seeded, not generated, so the recurrence itself was never
              exercised. Under this register's documented convention it produced
              1, 6, 44, 1419/4, ... from its own seeds, and non-integers from n=10.

Both are the E-010 failure mode: a verification that could not fail, because it never
touched the thing it claimed to verify.

The test: seed each entry with the minimum number of terms its order requires, then
regenerate the remaining stored terms and demand exact equality.

Convention (checkers/check_C3b_moduli_map.py:56):  C(k)·a_{k+1} = A(k)·a_k + B(k)·a_{k-1}
so when computing s[n], k = len(s) - 1.

Run:  python3 checkers/test_refs_self_regenerate.py
"""

import json
import pathlib
import sys

import sympy as sp

REFS = pathlib.Path(__file__).resolve().parents[1] / "refs" / "recurrences_v1.json"


def regenerate(recurrence, seed, n_terms):
    s = [sp.Rational(str(t)) for t in seed]
    while len(s) < n_terms:
        k = len(s) - 1
        s.append(sp.Rational(eval(recurrence, {"__builtins__": {}}, {"k": k, "s": s, "sp": sp})))
    return [str(x) for x in s]


def main():
    sequences = json.load(open(REFS))["sequences"]
    failures = []

    for key, entry in sorted(sequences.items()):
        terms = entry.get("initial_terms") or entry.get("initial_terms_rational")
        rec = entry.get("recurrence_python")
        if not terms or not rec:
            print(f"  skip  {key:24} (no recurrence or no stored terms)")
            continue
        terms = [str(t) for t in terms]

        seeded = None
        for n_seed in (1, 2, 3):
            if n_seed >= len(terms):
                break
            try:
                if regenerate(rec, terms[:n_seed], len(terms)) == terms:
                    seeded = n_seed
                    break
            except Exception:
                continue

        if seeded is not None:
            print(f"  PASS  {key:24} self-regenerates from {seeded} seed term(s)")
        else:
            try:
                got = regenerate(rec, terms[:2], len(terms))
            except Exception as exc:
                got = [f"<error: {exc}>"]
            print(f"  FAIL  {key:24}")
            print(f"        stored : {terms[:6]}")
            print(f"        regen  : {got[:6]}")
            failures.append(key)

    print()
    if failures:
        print(f"{len(failures)} entr{'y' if len(failures) == 1 else 'ies'} do not reproduce "
              f"their own terms: {', '.join(failures)}")
        print("A recurrence that cannot regenerate its own stored terms is corrupt. Do not")
        print("consume it, and do not trust any certificate computed from it.")
        return 1
    print("all entries reproduce their own stored terms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
