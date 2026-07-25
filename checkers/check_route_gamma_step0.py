#!/usr/bin/env python3
"""
check_route_gamma_step0.py — the first checkable step of Route γ (E-008).

Route γ (ramified Hauptmodul pullback) is the only unrefuted path to genuine
K3 geometry from the s7 partner. Its foundational claim (Deep Think T0s, OEIS
A279619) is:

    g.f.(A002652) = F( t(q) )

where t(q) = g.f.(A279618) is the level-7 Hauptmodul, and F(z) = Σ c(k) z^k is
the generating function of A279619 (the s7 order-2 partner). If this holds, the
Hauptmodul t is the correct uniformizing coordinate in which to attempt the
untwisting — i.e. Route γ has a real starting point rather than a hoped-for one.

This script tests that composition to the order the OEIS b-files allow. It reads
only committed b-files under refs/; it fabricates nothing.

IMPORTANT SCOPE. A PASS here does NOT establish ρ, T, any Kodaira type, or that
the pulled-back operator is unipotent. It establishes exactly one thing: that the
Hauptmodul composition the whole route rests on is real. The unipotency of the
pulled-back operator is a SEPARATE, still-open test (Route γ step 1).

Usage:
  python3 checkers/check_route_gamma_step0.py
  python3 checkers/check_route_gamma_step0.py --json data/certificates/ROUTE_GAMMA_STEP0.json
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

BFILES = {
    "A279618": REPO / "refs" / "oeis_A279618_bfile.txt",  # level-7 Hauptmodul t(q)
    "A002652": REPO / "refs" / "oeis_A002652_bfile.txt",  # weight-1 theta series, disc -7
    "A279619": REPO / "refs" / "oeis_A279619_bfile.txt",  # s7 order-2 partner c(k)
}


def read_bfile(path):
    d = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2:
            d[int(parts[0])] = int(parts[1])
    return d


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    for name, p in BFILES.items():
        if not p.exists():
            print(f"ERROR: missing b-file {p}")
            return 2

    H = read_bfile(BFILES["A279618"])
    A = read_bfile(BFILES["A002652"])
    C = read_bfile(BFILES["A279619"])

    N = max(H) + 1  # available Hauptmodul order bounds everything
    t = [H.get(n, 0) for n in range(N)]          # t(0) must be 0 (cusp)
    a = [A.get(n, 0) for n in range(N)]          # A(0) = 1
    c = [C.get(k + 1, 0) for k in range(N)]      # A279619 b-file offset 1

    if t[0] != 0:
        print(f"ERROR: Hauptmodul t(0) = {t[0]} != 0; composition ill-posed")
        return 2

    def mul(p, q):
        r = [0] * N
        for i, pi in enumerate(p):
            if pi:
                for j, qj in enumerate(q):
                    if i + j < N and qj:
                        r[i + j] += pi * qj
        return r

    acc = [0] * N
    tk = [0] * N
    tk[0] = 1
    for k in range(N):
        if c[k]:
            for i in range(N):
                acc[i] += c[k] * tk[i]
        tk = mul(tk, t)

    mism = [n for n in range(N) if acc[n] != a[n]]
    ok = not mism

    print("=" * 70)
    print("ROUTE γ — STEP 0:  g.f.(A002652) =?= F(t(q)),  t = A279618, F = A279619")
    print("=" * 70)
    print(f"order tested: {N - 1}  (bounded by A279618 b-file length)")
    for n in range(min(N, 12)):
        flag = "OK" if acc[n] == a[n] else "MISMATCH"
        print(f"  n={n:2d}  F(t(q))={acc[n]:>10d}   A002652={a[n]:>6d}   {flag}")
    if N > 12:
        print(f"  … through n={N-1}")
    print()
    if ok:
        print(f"VERDICT: CONFIRMED to order {N-1}. The Hauptmodul composition is real;")
        print("         Route γ has a genuine starting coordinate t.")
        print("SCOPE:   this does NOT give ρ/T/Kodaira/unipotency. Route γ step 1")
        print("         (unipotency of the pulled-back operator) remains OPEN.")
    else:
        print(f"VERDICT: REFUTED at orders {mism[:10]}. Route γ's premise fails;")
        print("         no unrefuted path to s7 geometry would remain.")

    out = {
        "checker": "check_route_gamma_step0.py",
        "checker_version": "1.0.0",
        "date": "2026-07-26",
        "claim": "g.f.(A002652) = F(t(q)), t=A279618 (level-7 Hauptmodul), F=g.f.(A279619)",
        "order_tested": N - 1,
        "verdict": "CONFIRMED" if ok else "REFUTED",
        "mismatch_orders": mism,
        "scope": (
            "Establishes only that the Hauptmodul composition underlying Route γ is real. "
            "Does NOT establish ρ, T, Kodaira type, or unipotency of the pulled-back "
            "operator (Route γ step 1, still open). Emits no ρ/T."
        ),
        "refs_sha256": {name: sha256(p) for name, p in BFILES.items()},
    }
    if args.json:
        Path(args.json).write_text(json.dumps(out, indent=2))
        print(f"\nWrote {args.json}")

    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
