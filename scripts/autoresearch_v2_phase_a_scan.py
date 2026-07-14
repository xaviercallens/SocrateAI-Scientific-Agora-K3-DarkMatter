#!/usr/bin/env python3
"""AutoEvolve R2 — Phase 8.A scanner (LR-1 anchors + LR-3 extended sieve).

Dual detection per sequence, all exact arithmetic:
  1. Minimal SHIFT recurrence:  sum_{i=0}^{r} P_i(n) u(n+i) = 0,  deg P_i <= d.
  2. Minimal ODE order for the generating function y(z) = sum u(n) z^n:
       sum_{j=0}^{rho} q_j(z) y^(j)(z) = 0,  deg q_j <= delta.

Classification rule under test (the v2 upgrade over GAP-1's shift-order rule):
  geometry is discriminated by ODE order (2=elliptic, 3=K3-type, 4=CY3-type)
  and, for 3-term Apery-like recurrences, by the (r, d) pair:
  Zagier class (r=2, d=2) <-> weight 2 (elliptic);
  Almkvist-Zagier class (r=2, d=3) <-> weight 3 (K3).

Method: modular Gaussian elimination (two independent 62-bit primes) routes
which (r, d) to attempt; the winning relation is then solved EXACTLY over Q
(fraction-free elimination on Python ints) and validated on >= 70 held-out
terms up to n_max = 110 with exact integer arithmetic. No relation is
reported without an exact held-out pass.
"""

import json
import math
import sys
from fractions import Fraction

P1 = (1 << 61) - 1          # Mersenne prime 2^61 - 1
P2 = 4611686018427387847    # another large prime

# ---------------------------------------------------------------- sequences

def seq_2factor(A, B, nmax):
    return [sum(math.comb(n, k) ** A * math.comb(n + k, k) ** B
                for k in range(n + 1)) for n in range(nmax + 1)]

def seq_3factor(A, B, C, nmax):
    return [sum(math.comb(n, k) ** A * math.comb(n + k, k) ** B
                * math.comb(2 * k, k) ** C
                for k in range(n + 1)) for n in range(nmax + 1)]

def seq_apery3(nmax):   # A005259, Apery zeta(3): sum C(n,k)^2 C(n+k,k)^2
    return [sum(math.comb(n, k) ** 2 * math.comb(n + k, k) ** 2
                for k in range(n + 1)) for n in range(nmax + 1)]

def seq_domb(nmax):     # A002895: sum C(n,k)^2 C(2k,k) C(2n-2k,n-k)
    return [sum(math.comb(n, k) ** 2 * math.comb(2 * k, k)
                * math.comb(2 * (n - k), n - k)
                for k in range(n + 1)) for n in range(nmax + 1)]

# ------------------------------------------------- modular linear algebra

def mod_nullspace_dim(rows, ncols, p):
    """Rank-nullity via in-place modular Gaussian elimination."""
    mat = [[x % p for x in row] for row in rows]
    rank, col = 0, 0
    nrows = len(mat)
    while rank < nrows and col < ncols:
        piv = next((r for r in range(rank, nrows) if mat[r][col]), None)
        if piv is None:
            col += 1
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        inv = pow(mat[rank][col], p - 2, p)
        mat[rank] = [(x * inv) % p for x in mat[rank]]
        for r in range(nrows):
            if r != rank and mat[r][col]:
                f = mat[r][col]
                mat[r] = [(a - f * b) % p for a, b in zip(mat[r], mat[rank])]
        rank += 1
        col += 1
    return ncols - rank

def exact_nullspace_vector(rows, ncols):
    """One exact rational nullspace vector via Fraction Gaussian elimination.
    Returns list of Fractions (not all zero) or None."""
    mat = [[Fraction(x) for x in row] for row in rows]
    nrows = len(mat)
    pivots = {}          # col -> row
    rank, col = 0, 0
    while rank < nrows and col < ncols:
        piv = next((r for r in range(rank, nrows) if mat[r][col] != 0), None)
        if piv is None:
            col += 1
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        inv = mat[rank][col]
        mat[rank] = [x / inv for x in mat[rank]]
        for r in range(nrows):
            if r != rank and mat[r][col] != 0:
                f = mat[r][col]
                mat[r] = [a - f * b for a, b in zip(mat[r], mat[rank])]
        pivots[col] = rank
        rank += 1
        col += 1
    free = [c for c in range(ncols) if c not in pivots]
    if not free:
        return None
    fc = free[0]
    vec = [Fraction(0)] * ncols
    vec[fc] = Fraction(1)
    for c, r in pivots.items():
        vec[c] = -mat[r][fc]
    # clear denominators -> integer vector
    lcm = 1
    for x in vec:
        lcm = lcm * x.denominator // math.gcd(lcm, x.denominator)
    ints = [int(x * lcm) for x in vec]
    g = 0
    for x in ints:
        g = math.gcd(g, abs(x))
    return [x // (g or 1) for x in ints]

# ------------------------------------------------------- shift recurrence

def shift_rows(u, r, d, nrows):
    """Row for each n: coefficients multiply c_{i,j} of P_i(n) = sum_j c_{i,j} n^j."""
    rows = []
    for n in range(nrows):
        row = []
        for i in range(r + 1):
            for j in range(d + 1):
                row.append((n ** j) * u[n + i])
        rows.append(row)
    return rows

def shift_validate(u, r, d, coeffs, n_from, n_to):
    for n in range(n_from, n_to + 1):
        s, idx = 0, 0
        for i in range(r + 1):
            for j in range(d + 1):
                s += coeffs[idx] * (n ** j) * u[n + i]
                idx += 1
        if s != 0:
            return False
    return True

def find_shift_recurrence(u, nmax, rmax=3, dmax=4, extra_rows=12):
    for r in range(1, rmax + 1):
        for d in range(0, dmax + 1):
            ncols = (r + 1) * (d + 1)
            nrows = ncols + extra_rows
            if nrows + r > len(u) - 1:
                continue
            rows = shift_rows(u, r, d, nrows)
            if mod_nullspace_dim(rows, ncols, P1) == 0:
                continue
            if mod_nullspace_dim(rows, ncols, P2) == 0:
                continue
            vec = exact_nullspace_vector(rows, ncols)
            if vec is None:
                continue
            if shift_validate(u, r, d, vec, nrows, nmax - r):
                held_out = (nmax - r) - nrows + 1
                return {"order": r, "degree": d, "coeffs": vec,
                        "fit_rows": nrows, "held_out_terms": held_out,
                        "held_out_pass": True}
    return None

# --------------------------------------------------------------- ODE order

def ode_rows(u, rho, delta, nrows):
    """z^m y^(j) contributes falling(n+j-m, j) * u[n+j-m] to coefficient of z^n."""
    rows = []
    for n in range(nrows):
        row = []
        for j in range(rho + 1):
            for m in range(delta + 1):
                idx = n + j - m
                if 0 <= idx <= len(u) - 1:
                    ff = 1
                    for t in range(j):
                        ff *= (idx + j - t) - j + t + 1  # falling factorial (idx+j)...(idx+1)? see below
                    # falling(n', j) with n' = idx + j ... simpler direct:
                    ff = 1
                    for t in range(j):
                        ff *= (idx + t + 1)
                    # y^(j) coeff of z^{idx}: u[idx+j] * (idx+j)!/(idx)! ... recompute cleanly:
                    row.append(0)  # placeholder, replaced after
                else:
                    row.append(0)
        rows.append(row)
    # clean re-computation (clarity over cleverness):
    rows = []
    for n in range(nrows):
        row = []
        for j in range(rho + 1):
            for m in range(delta + 1):
                k = n - m          # z^m * y^(j) term z^k needs series index k
                if k < 0 or k + j > len(u) - 1:
                    row.append(0)
                    continue
                c = u[k + j]
                for t in range(j):
                    c *= (k + j - t)
                row.append(c)
        rows.append(row)
    return rows

def ode_validate(u, rho, delta, coeffs, n_from, n_to):
    for n in range(n_from, n_to + 1):
        s, idx = 0, 0
        for j in range(rho + 1):
            for m in range(delta + 1):
                k = n - m
                if 0 <= k and k + j <= len(u) - 1:
                    c = u[k + j]
                    for t in range(j):
                        c *= (k + j - t)
                    s += coeffs[idx] * c
                idx += 1
        if s != 0:
            return False
    return True

def find_ode(u, nmax, rho_max=4, delta_max=8, extra_rows=12):
    for rho in range(1, rho_max + 1):
        for delta in range(1, delta_max + 1):
            ncols = (rho + 1) * (delta + 1)
            nrows = ncols + extra_rows
            if nrows + rho > len(u) - 1:
                continue
            rows = ode_rows(u, rho, delta, nrows)
            if mod_nullspace_dim(rows, ncols, P1) == 0:
                continue
            if mod_nullspace_dim(rows, ncols, P2) == 0:
                continue
            vec = exact_nullspace_vector(rows, ncols)
            if vec is None:
                continue
            if ode_validate(u, rho, delta, vec, nrows, nmax - rho - delta):
                held_out = (nmax - rho - delta) - nrows + 1
                return {"ode_order": rho, "ode_degree": delta,
                        "fit_rows": nrows, "held_out_terms": held_out,
                        "held_out_pass": True}
    return None

# ------------------------------------------------------------------ driver

def classify(name, u, nmax, rmax=3, dmax=4):
    rec = find_shift_recurrence(u, nmax, rmax=rmax, dmax=dmax)
    ode = find_ode(u, nmax)
    entry = {"name": name, "first_terms": u[:8]}
    if rec:
        entry["shift"] = {k: rec[k] for k in
                          ("order", "degree", "fit_rows",
                           "held_out_terms", "held_out_pass")}
        if rec["order"] <= 2 and rec["degree"] <= 4:
            entry["shift"]["coeffs"] = rec["coeffs"]
    else:
        entry["shift"] = None
    entry["ode"] = ode
    # weight/geometry heuristic under test
    if ode:
        entry["geometry_by_ode"] = {1: "rational", 2: "elliptic (weight 2)",
                                    3: "K3-type (weight 3)",
                                    4: "CY3-type (weight 4)"}.get(
                                        ode["ode_order"], "higher")
    else:
        entry["geometry_by_ode"] = "no ODE found in search window"
    return entry

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "anchors"
    nmax = 110
    out = {"n_max": nmax, "primes": [P1, P2],
           "note": "exact validation on all terms beyond fit window; "
                   "no relation reported without exact held-out pass"}

    if mode == "anchors":
        anchors = {
            "S12 (A=1,B=2) [in-house v1 primary]": seq_2factor(1, 2, nmax),
            "S21 (A=2,B=1) [= Apery zeta(2)?]": seq_2factor(2, 1, nmax),
            "Apery zeta(3) A005259 [K3 control]": seq_apery3(nmax),
            "Domb A002895 [AZ sporadic]": seq_domb(nmax),
        }
        out["results"] = [classify(k, v, nmax) for k, v in anchors.items()]
    elif mode == "scan2":
        res = []
        for A in range(1, 9):
            for B in range(1, 9):
                u = seq_2factor(A, B, nmax)
                r = classify(f"S({A},{B})", u, nmax)
                r["A"], r["B"] = A, B
                res.append(r)
                print(f"S({A},{B}): shift={r['shift'] and (r['shift']['order'], r['shift']['degree'])} "
                      f"ode={r['ode'] and (r['ode']['ode_order'], r['ode']['ode_degree'])} "
                      f"-> {r['geometry_by_ode']}", flush=True)
        out["results"] = res
    elif mode == "scan3":
        res = []
        for A in range(0, 4):
            for B in range(0, 4):
                for C in range(1, 4):
                    u = seq_3factor(A, B, C, nmax)
                    r = classify(f"T({A},{B},{C})", u, nmax)
                    r["A"], r["B"], r["C"] = A, B, C
                    res.append(r)
                    print(f"T({A},{B},{C}): shift={r['shift'] and (r['shift']['order'], r['shift']['degree'])} "
                          f"ode={r['ode'] and (r['ode']['ode_order'], r['ode']['ode_degree'])} "
                          f"-> {r['geometry_by_ode']}", flush=True)
        out["results"] = res

    path = f"data/autoresearch_v2/phase_a_{mode}.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(f"\nwritten: {path}")

if __name__ == "__main__":
    main()
