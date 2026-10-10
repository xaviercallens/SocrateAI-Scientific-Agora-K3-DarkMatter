#!/usr/bin/env python3
"""check_K3xT2_reading_S_level_sweep.py -- the Reading S pipeline re-run across levels: how it discriminates, computed.

check_K3xT2_reading_S.py computes, for ONE level n, the transcendental lattice of E x E' (cyclic n-isogeny, no CM) in
wedge^2 Z^4 and compares it with a target Gram. This script runs the same function for every n in 1..N and compares each
computed lattice with EVERY target U + <2m>, m in 1..N, by an explicit unimodular basis change. The expected (and checked)
picture: the isometry exists exactly on the diagonal m = n. Any off-diagonal isometry, or a missing diagonal one, is a defect.

Why this is in the repository: it is the approach, exercised. A candidate at a new level is adapted to the pipeline by
changing one integer; a wrong level is rejected by the same code that accepted the right one, and the matrix below is the
evidence that the rejection is not an accident of the two levels (7, 10) the programme happens to carry.

Scope: the no-CM assumption of the base checker is unchanged and stated; this is pure lattice arithmetic over Z; nothing physical.

Usage: python3 checkers/check_K3xT2_reading_S_level_sweep.py [--n-max 24] [--emit]
Controls: checkers/test_K3xT2_reading_S_level_sweep_controls.py
Generated-by: Claude (Fable 5.1), Stream 2, 2026-10-10 | Verified-by: the controls | Reviewed-by: N
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_K3xT2_reading_S as base  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "certificates" / "K3xT2_READING_S_LEVEL_SWEEP.json"


def target(n):
    return [[0, 0, -1], [0, 2 * n, 0], [-1, 0, 0]]


def sweep(n_max):
    computed = {}
    for n in range(1, n_max + 1):
        r = base.generic_check(n, target(n), [2, 1])
        computed[n] = r
    matrix = {}
    for n in range(1, n_max + 1):
        T = computed[n]["T_basis_in_wedge2"]
        for m in range(1, n_max + 1):
            matrix[(n, m)] = base.find_isometry(T, target(m)) is not None
    diag_ok = all(matrix[(n, n)] for n in range(1, n_max + 1))
    off_ok = not any(matrix[(n, m)] for n in range(1, n_max + 1) for m in range(1, n_max + 1) if n != m)
    return computed, matrix, diag_ok, off_ok


def build(n_max):
    computed, matrix, diag_ok, off_ok = sweep(n_max)
    per_n = {str(n): {"NS_signature": computed[n]["NS_signature"], "NS_saturated": computed[n]["NS_saturated"],
                      "T_det": computed[n]["T_det"], "T_signature": computed[n]["T_signature"],
                      "verdict": computed[n]["verdict"]} for n in computed}
    return {"certificate": "K3xT2_READING_S_LEVEL_SWEEP", "checker": "checkers/check_K3xT2_reading_S_level_sweep.py",
            "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "date": "2026-10-10",
            "tier": "B (exact lattice arithmetic over Z; the no-CM assumption of K3xT2_READING_S is unchanged)",
            "result": {"n_max": n_max, "pairs_tested": n_max * n_max,
                       "diagonal_isometric": sum(matrix[(n, n)] for n in range(1, n_max + 1)),
                       "off_diagonal_isometric": sum(v for (n, m), v in matrix.items() if n != m),
                       "off_diagonal_total": n_max * n_max - n_max,
                       "diagonal_all": diag_ok, "off_diagonal_none": off_ok, "per_level": per_n,
                       "signature_all_1_2": all(c["NS_signature"] == [1, 2] for c in computed.values()),
                       "saturated_all": all(c["NS_saturated"] for c in computed.values())},
            "not_claimed": ["any physical reading", "that every n is realized by a family the programme carries (only 7 and 10 are)",
                            "the no-CM hypothesis: assumed, not computed"],
            "generated_by": "Claude (Fable 5.1), Stream 2, 2026-10-10",
            "verified_by": "checkers/test_K3xT2_reading_S_level_sweep_controls.py", "reviewed_by": "N"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-max", type=int, default=24)
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    cert = build(a.n_max)
    r = cert["result"]
    print(f"levels 1..{r['n_max']}: diagonal isometric {r['diagonal_isometric']}/{r['n_max']}, "
          f"off-diagonal isometric {r['off_diagonal_isometric']}/{r['off_diagonal_total']}, "
          f"NS signature (1,2) at all levels: {r['signature_all_1_2']}, saturated at all levels: {r['saturated_all']}")
    ok = r["diagonal_all"] and r["off_diagonal_none"] and r["signature_all_1_2"] and r["saturated_all"]
    if a.emit:
        OUT.write_text(json.dumps(cert, indent=2) + "\n")
        print("wrote", OUT)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
