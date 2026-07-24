#!/usr/bin/env python3
"""Derive a refs/recurrences_v1.json entry from a hash-pinned OEIS b-file.

Fetches nothing (b-file must already be in refs/, listed in refs/MANIFEST.md). Derives the
minimal 3-term Picard-Fuchs shift recurrence  C(k) a_{k+1} = A(k) a_k + B(k) a_{k-1}  by exact
integer nullspace over ALL terms — NEVER transcribes coefficients from memory — verifies it
reproduces every term, and prints a refs-compatible JSON fragment + the min-ODE order.

Usage:
  python3 scripts/derive_refs_entry.py --bfile refs/oeis_A005259_bfile.txt \
      --id apery_zeta3 --oeis A005259 --closed-form "..." --note "..."
"""
import argparse
import json
import sys
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "checkers"))
import check_min_ode_order as mo  # noqa: E402 (reuse b-file loader + ODE-order scan)


def derive_3term(terms, dmax=4):
    """Smallest degree d with a 1-dim nullspace for C(k)a_{k+1}=A(k)a_k+B(k)a_{k-1}.
    Row k (k>=1): [ -a_{k+1}*k^j (C) | a_k*k^j (A) | a_{k-1}*k^j (B) ]  == 0.
    Returns (C_coeffs, A_coeffs, B_coeffs) ascending in k, or None."""
    N = len(terms)
    for d in range(1, dmax + 1):
        rows = []
        for k in range(1, N - 1):
            row = []
            for j in range(d + 1):          # C on a_{k+1}
                row.append(-(k ** j) * terms[k + 1])
            for j in range(d + 1):          # A on a_k
                row.append((k ** j) * terms[k])
            for j in range(d + 1):          # B on a_{k-1}
                row.append((k ** j) * terms[k - 1])
            rows.append(row)
        need = 3 * (d + 1)
        if len(rows) < need + 5:
            continue
        ns = sp.Matrix(rows).nullspace()
        if len(ns) == 1:
            v = ns[0]
            dens = [sp.Rational(x).q for x in v]
            L = 1
            for q in dens:
                L = sp.ilcm(L, q)
            vi = [int(x * L) for x in v]
            g = 0
            for x in vi:
                g = sp.igcd(g, x)
            if g:
                vi = [x // g for x in vi]
            C = vi[0:d + 1]
            A = vi[d + 1:2 * (d + 1)]
            B = vi[2 * (d + 1):3 * (d + 1)]
            # MUM normalisation: the recurrence a_{k+1}=(A s_{-1}+B s_{-2})/C is invariant
            # under negating (C,A,B) together. Fix the sign so C's leading coeff is positive
            # (checkers require C(k) == +(k+1)^order exactly).
            lead = next((c for c in reversed(C) if c != 0), 0)
            if lead < 0:
                C = [-c for c in C]; A = [-c for c in A]; B = [-c for c in B]
            return C, A, B, d
    return None


def poly_str(coeffs, var="k"):
    parts = []
    for j, c in enumerate(coeffs):
        if c == 0:
            continue
        if j == 0:
            parts.append(f"({c})")
        elif j == 1:
            parts.append(f"({c})*{var}")
        else:
            parts.append(f"({c})*{var}**{j}")
    return " + ".join(parts) if parts else "0"


def verify(C, A, B, terms):
    """Check C(k)a_{k+1} - A(k)a_k - B(k)a_{k-1} == 0 for all k>=1 (exact ints)."""
    def ev(coeffs, k):
        return sum(c * k ** j for j, c in enumerate(coeffs))
    for k in range(1, len(terms) - 1):
        if ev(C, k) * terms[k + 1] - ev(A, k) * terms[k] - ev(B, k) * terms[k - 1] != 0:
            return False, k
    return True, len(terms) - 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bfile", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--oeis", required=True)
    ap.add_argument("--closed-form", default="")
    ap.add_argument("--note", default="")
    ap.add_argument("--dmax", type=int, default=4)
    ap.add_argument("--n-terms", type=int, default=80)
    args = ap.parse_args()

    terms = mo.load_bfile_terms(args.bfile, args.n_terms)
    res = derive_3term(terms, args.dmax)
    if res is None:
        print(f"NO 3-term recurrence found up to degree {args.dmax}", file=sys.stderr)
        sys.exit(2)
    C, A, B, d = res
    ok, depth = verify(C, A, B, terms)
    if not ok:
        print(f"DERIVED RECURRENCE FAILED at k={depth}", file=sys.stderr)
        sys.exit(2)

    # min-ODE order for the type label (reuse committed checker)
    r_ode, d_ode, _, n_rows = mo.min_order_scan(terms, mo.fit_ode, 4, 8)
    seq_type = "order-3" if r_ode == 3 else ("order-2" if r_ode == 2 else f"order-{r_ode}")

    rec_py = f"(({poly_str(A)})*s[-1] + ({poly_str(B)})*s[-2]) / ({poly_str(C)})"
    entry = {
        "type": seq_type,
        "status": "OK",
        "source": f"OEIS {args.oeis} (http://oeis.org/{args.oeis}); {args.note}",
        "closed_form": args.closed_form,
        "initial_terms": terms[:10],
        "recurrence_python": rec_py,
        "_derivation": (f"recurrence DERIVED by exact nullspace from hash-pinned b-file "
                        f"(refs/oeis_{args.oeis}_bfile.txt) — NOT transcribed; verified to "
                        f"reproduce {depth} terms; min-ODE order {r_ode} PASS({n_rows})"),
    }
    print(json.dumps({args.id: entry}, indent=2))
    print(f"\n# {args.id}: {args.oeis} | rec deg {d} verified {depth} terms | "
          f"min-ODE order {r_ode} PASS({n_rows}) [{seq_type}]", file=sys.stderr)


if __name__ == "__main__":
    main()
