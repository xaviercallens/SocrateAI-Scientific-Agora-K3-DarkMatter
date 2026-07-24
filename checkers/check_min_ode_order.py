#!/usr/bin/env python3
"""
check_min_ode_order.py — minimal Picard-Fuchs ODE order of a sequence's generating function.

THE geometric discriminator per the Stream-3 Fable brief (2026-07-24): the minimal
generating-function ODE order — NOT the shift-recurrence order — decides elliptic
(order 2) vs K3 (order 3). This checker computes it by exact rational linear algebra.

Method (exact arithmetic, no floats):
  For f(z) = sum a_n z^n and a candidate (order r, degree d) box, solve
      sum_{i=0..r} p_i(z) f^{(i)}(z) = 0,   deg p_i <= d,
  as an exact integer nullspace problem over ALL available series coefficients.
  A nonzero nullspace vector is an annihilating ODE verified to the full depth
  of the input series -> finite-order evidence PASS(N), never bare PASS.
  Minimality is RELATIVE TO THE SEARCH BOX: "no ODE of order < r with deg <= dmax"
  is exhaustively checked inside the box and reported as such.

Also fits the minimal shift-recurrence order (same nullspace method on
  sum_{i=0..R} q_i(n) a_{n+i} = 0, deg q_i <= D) so that recurrence-order vs
ODE-order mismatches (the misclassification mode the brief warns about) are
visible in one certificate.

Inputs: refs/ files only (b-file or a frozen recurrence in recurrences_v1.json),
listed in refs/MANIFEST.md. No network. Deterministic. Certificate JSON output.
"""

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp

CHECKER_VERSION = "1.0.0"
REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "checkers"))
import check_C3b_moduli_map as base  # noqa: E402  (refs recurrence machinery)


def load_bfile_terms(path, max_terms):
    """Parse an OEIS b-file (lines 'n a(n)') into a list of ints, index-aligned from 0."""
    terms = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 2:
            continue
        terms[int(parts[0])] = int(parts[1])
    n0 = min(terms)
    out = []
    k = n0
    while k in terms and len(out) < max_terms:
        out.append(terms[k])
        k += 1
    return out


def load_refs_terms(refs_path, seq_id, max_terms):
    """Generate terms of a refs-frozen recurrence (exact rational arithmetic)."""
    refs = json.loads(Path(refs_path).read_bytes())
    entry = refs["sequences"][seq_id]
    order = 3 if entry["type"] == "order-3" else 2
    A, B, C, _ = base.extract_recurrence_polys(entry["recurrence_python"], order)
    init = [Fraction(int(x)) for x in entry["initial_terms"]]
    seq, _ = base.generate_sequence(A, B, C, init, max_terms)
    assert all(x.denominator == 1 for x in seq), "non-integral refs sequence"
    return [int(x) for x in seq[:max_terms]]


def falling(m, i):
    """Falling factorial m(m-1)...(m-i+1); =1 for i=0."""
    out = 1
    for t in range(i):
        out *= (m - t)
    return out


def fit_ode(terms, r, d):
    """Exact nullspace fit of sum_i p_i(z) f^(i) = 0, deg p_i <= d, over ALL terms.
    Row m (coefficient of z^m), unknowns c[i][j] for p_i = sum_j c[i][j] z^j:
        [z^m] p_i f^(i) = sum_j c[i][j] * falling(m-j+i, i) * a_{m-j+i}
    Returns (ode_coeffs or None, n_rows_used)."""
    N = len(terms)
    n_unknowns = (r + 1) * (d + 1)
    rows = []
    for m in range(0, N - r):
        row = []
        for i in range(r + 1):
            for j in range(d + 1):
                k = m - j          # power index in f^(i) expansion
                idx = k + i        # a-index
                if k < 0 or idx >= N:
                    row.append(0)
                else:
                    row.append(falling(k + i, i) * terms[idx])
        rows.append(row)
    if len(rows) < n_unknowns + 5:   # demand overdetermination margin
        return None, len(rows)
    M = sp.Matrix(rows)
    ns = M.nullspace()
    if not ns:
        return None, len(rows)
    v = ns[0]
    # normalise to integer vector
    dens = [sp.Rational(x).q for x in v]
    lcm = 1
    for q in dens:
        lcm = sp.ilcm(lcm, q)
    vi = [int(x * lcm) for x in v]
    g = 0
    for x in vi:
        g = sp.igcd(g, x)
    if g > 1:
        vi = [x // g for x in vi]
    coeffs = {}
    t = 0
    for i in range(r + 1):
        coeffs[i] = vi[t:t + d + 1]
        t += d + 1
    return coeffs, len(rows)


def fit_recurrence(terms, R, D):
    """Exact nullspace fit of sum_i q_i(n) a_{n+i} = 0, deg q_i <= D, over all terms."""
    N = len(terms)
    n_unknowns = (R + 1) * (D + 1)
    rows = []
    for n in range(0, N - R):
        row = []
        for i in range(R + 1):
            for j in range(D + 1):
                row.append((n ** j) * terms[n + i])
        rows.append(row)
    if len(rows) < n_unknowns + 5:
        return None, len(rows)
    M = sp.Matrix(rows)
    ns = M.nullspace()
    return (ns[0] if ns else None), len(rows)


def min_order_scan(terms, fit_fn, r_max, d_max):
    """Ascending scan: smallest order r (any deg <= d_max) admitting an annihilator."""
    for r in range(1, r_max + 1):
        for d in range(1, d_max + 1):
            sol, n_rows = fit_fn(terms, r, d)
            if sol is not None:
                return r, d, sol, n_rows
    return None, None, None, 0


def run_check(source_kind, source_path, seq_id, n_terms=60, r_max=4, d_max=8):
    raw = Path(source_path).read_bytes()
    sha = hashlib.sha256(raw).hexdigest()

    if source_kind == "bfile":
        terms = load_bfile_terms(source_path, n_terms)
    else:
        terms = load_refs_terms(source_path, seq_id, n_terms)

    result = {
        "checker": "check_min_ode_order.py",
        "checker_version": CHECKER_VERSION,
        "criterion": "min-ODE-order (generating-function Picard-Fuchs order; the geometric discriminator)",
        "sequence": seq_id,
        "source_kind": source_kind,
        "source_file": str(source_path),
        "source_sha256": sha,
        "n_terms_used": len(terms),
        "search_box": {"r_max": r_max, "d_max": d_max},
        "first_terms": [str(t) for t in terms[:6]],
    }

    # minimal ODE order (ascending exhaustive scan inside the box)
    r_ode, d_ode, ode, n_rows = min_order_scan(terms, fit_ode, r_max, d_max)
    if r_ode is None:
        result["verdict"] = f"NO_ODE_FOUND_IN_BOX(r<={r_max}, d<={d_max})"
        return result, 2
    result["min_ode"] = {
        "order": r_ode,
        "poly_degree": d_ode,
        "rows_validated": n_rows,
        "orders_below_excluded_to_deg": d_max,
        "ode_coefficients_p_i_ascending_z": {str(i): [str(c) for c in ode[i]]
                                             for i in sorted(ode)},
    }

    # minimal shift-recurrence order (for the mismatch diagnostic)
    r_rec, d_rec, _, rec_rows = min_order_scan(terms, fit_recurrence, r_max + 1, d_max)
    result["min_recurrence"] = ({"order": r_rec, "poly_degree": d_rec,
                                 "rows_validated": rec_rows}
                                if r_rec is not None else "NOT_FOUND_IN_BOX")

    geom = {1: "rational/log (order 1)", 2: "ELLIPTIC-curve type (order 2)",
            3: "K3-type (order 3)", 4: "CY3-type (order 4)"}.get(r_ode, f"order {r_ode}")
    result["geometric_type_if_MUM"] = geom + "  [Tier B: finite-order evidence, box-relative minimality]"
    result["verdict"] = (f"MIN_ODE_ORDER={r_ode} PASS({n_rows}) "
                        f"[deg={d_ode}; orders<{r_ode} excluded to deg {d_max}; "
                        f"min recurrence order={r_rec}]")
    result["provenance"] = ("Generated-by: checkers/check_min_ode_order.py v1.0.0 (Tier B) | "
                            "Verified-by: exact integer nullspace over full series depth | "
                            "Reviewed-by: pending T0")
    return result, 0


def main():
    ap = argparse.ArgumentParser(description="Minimal generating-function ODE order checker")
    ap.add_argument("--bfile", help="Path to an OEIS b-file in refs/")
    ap.add_argument("--refs-seq", help="Sequence id in refs/recurrences_v1.json")
    ap.add_argument("--refs", default=str(REPO_ROOT / "refs" / "recurrences_v1.json"))
    ap.add_argument("--seq-id", required=True, help="Label for the certificate")
    ap.add_argument("--n-terms", type=int, default=60)
    ap.add_argument("--r-max", type=int, default=4)
    ap.add_argument("--d-max", type=int, default=8)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.bfile:
        result, code = run_check("bfile", args.bfile, args.seq_id,
                                 args.n_terms, args.r_max, args.d_max)
    elif args.refs_seq:
        result, code = run_check("refs", args.refs, args.refs_seq,
                                 args.n_terms, args.r_max, args.d_max)
    else:
        ap.error("need --bfile or --refs-seq")

    payload = json.dumps(result, indent=2, sort_keys=True)
    out = args.out or str(REPO_ROOT / "data" / "certificates" / f"MINODE_{args.seq_id}.json")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(payload + "\n")
    print(payload)
    print(f"\ncertificate written: {out}", file=sys.stderr)
    sys.exit(code)


if __name__ == "__main__":
    main()
