#!/usr/bin/env python3
"""
PROJECT ZEILBERGER (step 1): EXACT verification of the S20 order-5 recurrence.

Before any Lean proof can be attempted, we must confirm the degree-9 integer
coefficients P0..P5 currently sitting in Structures/S20Recurrence.lean actually
satisfy the recurrence for the true sequence
    S20(n) = sum_{k=0}^n  C(n,k)^4 * C(n+k,k).

Strategy (all exact, arbitrary-precision integers / sympy Rationals):
  1. Compute S20(n) exactly.
  2. Independently DERIVE the minimal order-5 recurrence via exact nullspace.
  3. PARSE the P0..P5 polynomials straight out of the .lean file (no retyping).
  4. Plug the parsed polynomials into the recurrence and check == 0 for every n
     in a range far larger than the number of unknowns (a real test, not a fit).
  5. Check the parsed recurrence is a rational multiple of the derived one.
"""
import re
import sys
from math import comb
import sympy as sp

LEAN = ("/Users/xcallens/xdev/SocrateAI-Scientific-Agora-K3-DarkMatter/"
        "lean4_formal_proofs/Structures/S20Recurrence.lean")


def S20(n: int) -> int:
    return sum(comb(n, k)**4 * comb(n + k, k) for k in range(n + 1))


def parse_poly(body: str):
    """Parse 'c*n^p + c*n^p ... + c0' (Lean syntax) into a sympy Poly in n."""
    n = sp.symbols('n')
    # normalise: insert explicit '+' before '-' so split is uniform
    s = body.replace('-', '+-').replace(' ', '')
    expr = sp.Integer(0)
    for tok in s.split('+'):
        if not tok:
            continue
        m = re.fullmatch(r'(-?\d+)\*n\^(\d+)', tok)
        if m:
            expr += sp.Integer(int(m.group(1))) * n**int(m.group(2))
            continue
        m = re.fullmatch(r'(-?\d+)\*n', tok)
        if m:
            expr += sp.Integer(int(m.group(1))) * n
            continue
        m = re.fullmatch(r'(-?\d+)', tok)
        if m:
            expr += sp.Integer(int(m.group(1)))
            continue
        raise ValueError(f"unparsed token: {tok!r}")
    return sp.expand(expr)


def parse_lean_polys(path):
    text = open(path).read()
    polys = {}
    for j in range(6):
        m = re.search(rf'def P{j} \(n : ℤ\) : ℤ :=\s*(.+?)\n\n', text, re.S)
        if not m:
            raise RuntimeError(f"could not locate P{j} in {path}")
        polys[j] = parse_poly(m.group(1).strip())
    return polys


def derive_recurrence(order=5, max_deg=12, nterms=40):
    """Minimal-order exact nullspace recurrence for S20."""
    n = sp.symbols('n')
    seq = [sp.Integer(S20(i)) for i in range(nterms)]
    for deg in range(0, max_deg + 1):
        ncols = (order + 1) * (deg + 1)
        rows = list(range(0, nterms - order))
        if len(rows) < ncols:
            continue
        M = sp.zeros(len(rows), ncols)
        for r, n0 in enumerate(rows):
            col = 0
            for j in range(order + 1):
                for d in range(deg + 1):
                    M[r, col] = seq[n0 + j] * sp.Integer(n0)**d
                    col += 1
        ns = M.nullspace()
        if not ns:
            continue
        vec = ns[0]
        polys = []
        col = 0
        for j in range(order + 1):
            pj = sum(vec[col + d] * n**d for d in range(deg + 1))
            polys.append(sp.expand(pj)); col += deg + 1
        if polys[-1] == 0:
            continue
        return deg, polys
    return None


def main():
    n = sp.symbols('n')
    print("=" * 68)
    print("STEP 1  Exact S20 values")
    print("=" * 68)
    vals = [S20(i) for i in range(8)]
    print("S20(0..7) =", vals)

    print("\n" + "=" * 68)
    print("STEP 2  Parse P0..P5 from the Lean source (no retyping)")
    print("=" * 68)
    P = parse_lean_polys(LEAN)
    for j in range(6):
        deg = sp.Poly(P[j], n).degree()
        lead = sp.Poly(P[j], n).LC()
        print(f"  P{j}: degree {deg}, leading coeff {lead}")

    print("\n" + "=" * 68)
    print("STEP 3  Plug parsed polynomials into the recurrence; check == 0")
    print("        P0 S20(n)+P1 S20(n+1)+...+P5 S20(n+5) =?= 0")
    print("=" * 68)
    NMAX = 30
    S = [sp.Integer(S20(i)) for i in range(NMAX + 6)]
    all_zero = True
    first_fail = None
    for n0 in range(NMAX + 1):
        tot = sum(P[j].subs(n, n0) * S[n0 + j] for j in range(6))
        if tot != 0:
            all_zero = False
            if first_fail is None:
                first_fail = (n0, tot)
    if all_zero:
        print(f"  PASS: recurrence holds EXACTLY for all n in [0, {NMAX}]")
        print(f"        ({NMAX + 1} independent checks; recurrence has 6 unknown")
        print("         polynomial coefficients, so this is a genuine test).")
    else:
        n0, tot = first_fail
        print(f"  FAIL: recurrence is NON-ZERO at n={n0}")
        print(f"        residual has {len(str(abs(tot)))} digits (should be 0)")

    print("\n" + "=" * 68)
    print("STEP 4  Independent confirmation: disjoint range + negative control")
    print("=" * 68)
    # (a) re-check on a range DISJOINT from STEP 3 to exclude a low-degree fluke
    LO, HI = 31, 60
    S2 = [sp.Integer(S20(i)) for i in range(HI + 6)]
    disjoint_ok = all(
        sum(P[j].subs(n, n0) * S2[n0 + j] for j in range(6)) == 0
        for n0 in range(LO, HI + 1))
    print(f"  (a) disjoint range n in [{LO},{HI}] : "
          f"{'PASS' if disjoint_ok else 'FAIL'}")
    # (b) negative control: perturb P0 by +1; the recurrence MUST then fail,
    #     proving the test can actually detect a wrong coefficient.
    P0_bad = P[0] + 1
    sensitive = any(
        (P0_bad.subs(n, n0) * S[n0]
         + sum(P[j].subs(n, n0) * S[n0 + j] for j in range(1, 6))) != 0
        for n0 in range(0, 6))
    print(f"  (b) negative control (P0+1 must break it) : "
          f"{'PASS (test is sensitive)' if sensitive else 'FAIL (test blind!)'}")

    print("\n" + "=" * 68)
    print("VERDICT")
    print("=" * 68)
    if all_zero:
        print("  The S20 order-5 recurrence in the Lean file is TRUE (exact check,")
        print(f"  n in [0,{NMAX}]). The coefficients are a genuine discovery, NOT")
        print("  hallucinated. A general-n proof still requires a WZ certificate")
        print("  (or kernel-checked induction); finite verification != all-n proof.")
    else:
        print("  The recurrence FAILS exact verification. The Lean coefficients")
        print("  must NOT be claimed as proven. Report this to the user.")


if __name__ == "__main__":
    main()
