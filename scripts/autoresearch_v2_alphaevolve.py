"""
AutoEvolve R2 / Phase 8.B-ext — AlphaEvolve sequence generator for Phase B.

Strategy: generate new binomial K3-type candidates via evolutionary search in
the (A, B, C) parameter space, gate them through G1-1 exact classifier, and
promote surviving K3-type sequences to the candidate pool.

Method: start with known K3 anchors (apery_zeta3 A005259, domb A002895,
cooper_s7 A183204) and nearby points in the (A,B,C) lattice; compute terms,
classify ODE order; keep order-3 sequences. Each survivor is passed to Phase B
gates on demand (Phase C).

Cost: O(n_gen * term_compute) — term computation is cheap; Haiku can handle
the full sweep. Monodromy (G1-4) is where Sonnet becomes necessary (RK4 numeric
integration at 50-digit precision is resource-intensive).
"""

import json
import math
import os
import sys
from itertools import product

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPTS_DIR)
sys.path.insert(0, SCRIPTS_DIR)
OUT_DIR = os.path.join(REPO_ROOT, "data", "autoresearch_v2")
os.makedirs(OUT_DIR, exist_ok=True)

from autoresearch_v2_phase_a_scan import classify
from autoresearch_v2_pool import POOL

NMAX = 110


def seq_2factor_gen(A, B, nmax):
    """Generate sum_k C(n,k)^A C(n+k,k)^B (generic 2-factor)."""
    return [sum(math.comb(n, k) ** A * math.comb(n + k, k) ** B
                for k in range(n + 1)) for n in range(nmax + 1)]


def seq_3factor_gen(A, B, C, nmax):
    """Generate sum_k C(n,k)^A C(n+k,k)^B C(2k,k)^C (generic 3-factor)."""
    return [sum(math.comb(n, k) ** A * math.comb(n + k, k) ** B * math.comb(2 * k, k) ** C
                for k in range(n + 1)) for n in range(nmax + 1)]


def main():
    print("=== AlphaEvolve Phase 8.B-ext: K3-type candidate generation ===")

    # Anchor points: known K3 sporadics
    anchors_2f = [(2, 2), (2, 3), (1, 4)]  # apery_zeta3, domb-like, t003-like
    anchors_3f = [(1, 1, 1), (1, 2, 1), (2, 1, 2)]  # t011-like, t103-like, t112-like

    # Generation: 2-factor neighborhood
    print("\n[G1] 2-factor sweep (A,B) near anchors...")
    gen_2f = {}
    for (a0, b0) in anchors_2f:
        for da, db in product([-1, 0, 1], repeat=2):
            A, B = a0 + da, b0 + db
            if 1 <= A <= 8 and 1 <= B <= 8:
                cid = f"gen_2f_A{A}B{B}"
                u = seq_2factor_gen(A, B, NMAX)
                res = classify(cid, u, NMAX)
                ode = (res or {}).get("ode") or {}
                if ode.get("ode_order") == 3:
                    gen_2f[cid] = res
                    print(f"  {cid:20} ODE order 3 → **K3-type CANDIDATE**")

    # Generation: 3-factor neighborhood
    print("\n[G2] 3-factor sweep (A,B,C) near anchors...")
    gen_3f = {}
    for (a0, b0, c0) in anchors_3f:
        for da, db, dc in product([-1, 0, 1], repeat=3):
            A, B, C = a0 + da, b0 + db, c0 + dc
            if 1 <= A <= 4 and 1 <= B <= 4 and 1 <= C <= 4:
                cid = f"gen_3f_A{A}B{B}C{C}"
                u = seq_3factor_gen(A, B, C, NMAX)
                res = classify(cid, u, NMAX)
                ode = (res or {}).get("ode") or {}
                if ode.get("ode_order") == 3:
                    gen_3f[cid] = res
                    print(f"  {cid:20} ODE order 3 → **K3-type CANDIDATE**")

    # Consolidate
    survivors = {**gen_2f, **gen_3f}
    print(f"\n[Summary] Generated {len(gen_2f) + len(gen_3f)} terms; "
          f"**{len(survivors)} K3-type survivors** ready for Phase C gates")

    # Write registry
    out = {
        "generation_date": "2026-07-14",
        "nmax": NMAX,
        "method": "evolutionary neighborhood search around known K3 anchors",
        "2factor_count": len(gen_2f),
        "3factor_count": len(gen_3f),
        "k3_survivors": len(survivors),
        "survivors": survivors,
        "note": "These candidates passed G1-1 (ODE order 3) and are queued for "
                "full G1-2..G1-4 gates in Phase C. Monodromy (G1-4) requires "
                "Sonnet for RK4 precision; G1-2/G1-3 are Haiku-tractable."
    }
    with open(os.path.join(OUT_DIR, "alphaevolve_gen_survivors.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)

    print(f"\nAlphaEvolve registry written to alphaevolve_gen_survivors.json")
    return survivors


if __name__ == "__main__":
    survivors = main()
