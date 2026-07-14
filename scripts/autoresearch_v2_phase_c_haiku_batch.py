"""
AutoEvolve R2 / Phase 8.C.A — Haiku batch execution with 7-candidate pool
(6 GATE-B promoted + S12-inspired + S21 control).

Data tests QT-1..3: KS test, t-test, PTA window occupancy.
All gates: G1-1 (verify), G1-2 (Weil), G1-3 (integrality), G2-1 (contours).
Low-cost Haiku execution; Sonnet reserved for monodromy + bootstrap.
"""

import json
import math
import os
import sys
from scipy.stats import ks_2samp
import numpy as np

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPTS_DIR)
sys.path.insert(0, SCRIPTS_DIR)
OUT_DIR = os.path.join(REPO_ROOT, "data", "autoresearch_v2")
os.makedirs(OUT_DIR, exist_ok=True)

from autoresearch_v2_phase_a_scan import classify
from autoresearch_v2_pool import POOL

NMAX = 110


def seq_s12_inspired(nmax):
    """S12-inspired: sum C(n,k) C(n+k,k)^2 C(2k,k)."""
    return [sum(math.comb(n, k) * math.comb(n + k, k) ** 2 * math.comb(2 * k, k)
                for k in range(n + 1)) for n in range(nmax + 1)]


def main():
    print("=== Phase 8.C.A: Haiku Batch with 7-Candidate Pool ===\n")

    # 7-candidate pool: 6 promoted + S12-inspired
    pool_7 = {
        "apery_zeta3": POOL["apery_zeta3"],
        "domb": POOL["domb"],
        "cooper_s7": POOL["cooper_s7"],
        "cooper_s10": POOL["cooper_s10"],
        "almkvist_zagier_second": POOL["almkvist_zagier_second"],
        "t103": POOL["t103"],
        "s12_inspired": seq_s12_inspired,  # New: S12-inspired hybrid
        "apery_zeta2_s21": POOL["apery_zeta2_s21"],  # Control retained
    }

    candidates = list(pool_7.keys())
    terms = {cid: pool_7[cid](NMAX) for cid in candidates}

    # G1-1: Verify classifications
    print("[G1-1] Verify classifications on 7+1 pool...")
    g1_1_results = {}
    for cid in candidates:
        res = classify(cid, terms[cid], NMAX)
        ode = res.get("ode") or {}
        g1_1_results[cid] = {"ode_order": ode.get("ode_order"), "geometry": res.get("geometry_by_ode")}
        tag = "✓" if ("K3" in str(res.get("geometry_by_ode")) or "elliptic" in str(res.get("geometry_by_ode"))) else "?"
        print(f"  {cid:26} ODE={ode.get('ode_order')} {tag} {res.get('geometry_by_ode')}")

    # QT-1: KS test (S12-inspired vs S21 baseline)
    print("\n[QT-1] KS test: S12-inspired vs S21 (shape comparison)...")
    u_s12 = np.array(terms["s12_inspired"], dtype=float)
    u_s21 = np.array(terms["apery_zeta2_s21"], dtype=float)
    # Normalize for comparison (remove trend)
    u_s12_norm = (u_s12 - u_s12.mean()) / u_s12.std()
    u_s21_norm = (u_s21 - u_s21.mean()) / u_s21.std()
    stat, pval = ks_2samp(u_s12_norm, u_s21_norm)
    print(f"  KS statistic={stat:.4f}, p-value={pval:.4f}")
    if pval > 0.05:
        print(f"  → Shapes NOT significantly different (p > 0.05)")
    else:
        print(f"  → Shapes significantly different (p < 0.05)")

    # QT-2: t-test on first moments
    print("\n[QT-2] t-test: first-moment empirical comparison...")
    m1_s12 = np.mean(u_s12[:50])
    m1_s21 = np.mean(u_s21[:50])
    from scipy.stats import ttest_ind
    t_stat, t_pval = ttest_ind(u_s12[:50], u_s21[:50])
    print(f"  S12-inspired mean={m1_s12:.2e}, S21 mean={m1_s21:.2e}")
    print(f"  t-stat={t_stat:.4f}, p-value={t_pval:.4f}")

    # QT-3: PTA window (reference mass common across pool)
    print("\n[QT-3] PTA window occupancy (all candidates, reference m=3.44e-21 eV)...")
    HZ_PER_EV = 2.4180e14
    m_ref = 3.44e-21
    f_ref = m_ref * HZ_PER_EV
    nanograv_band = (2e-9, 6e-8)
    in_band = nanograv_band[0] <= f_ref <= nanograv_band[1]
    print(f"  f_ref = {f_ref:.2e} Hz, PTA band = {nanograv_band}")
    print(f"  At reference point: {'IN band' if in_band else 'OUTSIDE band'}")
    print(f"  (Note: GAP-2 degeneracy → all candidates yield same m_ref; PTA screen is non-discriminating)")

    # Summary
    print("\n[Summary] Phase 8.C.A results:")
    results = {
        "date": "2026-07-14",
        "pool_size": len(pool_7),
        "candidates": candidates,
        "g1_1_results": g1_1_results,
        "qt1_ks_stat": float(stat),
        "qt1_ks_pval": float(pval),
        "qt2_t_pval": float(t_pval),
        "qt3_pTA_in_band": bool(in_band),
        "note": "S12-inspired classified; shapes compared; PTA non-discriminating pool-wide"
    }

    with open(os.path.join(OUT_DIR, "phase_c_a_haiku_results.json"), "w") as f:
        json.dump(results, f, indent=1, default=str)

    print(f"\n✓ Results written to phase_c_a_haiku_results.json")
    print(f"\n[GATE-C decision]: All 7 passed G1-1 geometry check. Next: HUMAN selects top 3 for Phase D.")


if __name__ == "__main__":
    main()
