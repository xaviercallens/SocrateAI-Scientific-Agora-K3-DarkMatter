"""
GAP-1 / Task T1.3: Mirror-map integrality check for S_{1,2} and S_{2,1}.
=========================================================================

Method (standard Frobenius/mirror-map recipe, e.g. Zagier "Arithmetic and
topology of ..."; Almkvist-Zudilin; Lian-Yau integrality conjecture):

Given the holomorphic Frobenius solution at the MUM point z=0,
    y0(z) = sum_n u(n) z^n,          u(n) = sum_k C(n,k)^A C(n+k,k)^B,
the logarithmic second solution is y1(z) = y0(z) log(z) + ytilde(z), where
ytilde(z) = sum_n c_n z^n is obtained by the standard derivative-at-epsilon
trick: continue n -> n+epsilon in each binomial factor via the Gamma
function, differentiate the term-by-term product at epsilon=0, and sum over
k. For integer n, k this reduces to an EXACT rational expression in harmonic
numbers:
    d/deps [C(n+eps,k)]|_0     = C(n,k)   * (H_n     - H_(n-k))
    d/deps [C(n+eps+k,k)]|_0   = C(n+k,k) * (H_(n+k) - H_n)
so, for T(n,k) = C(n,k)^A * C(n+k,k)^B,
    c_n = sum_k T(n,k) * [ A*(H_n - H_(n-k)) + B*(H_(n+k) - H_n) ]
(product rule on ln T, since d/deps ln(x^A y^B) = A dx/x + B dy/y).

The mirror map is q(z) = z * exp(ytilde(z)/y0(z)) (the log(z) terms cancel
between y1 and the exp/log structure — this is the textbook construction).
Integrality of q(z)/z's power-series coefficients (after this standard
normalization, no further rescaling) is a well-known necessary signature of
genuine Calabi-Yau/K3 periods (Lian-Yau integrality; verified, not proven in
general). A non-integral coefficient is evidence AGAINST the K3 identification
and must be reported as such (scientificplan.md T1.3, Rule 4).

Implementation note: series division and exponentiation are done via direct
power-series recurrences over Python's exact `Fraction` type (NOT sympy
`.series()`, which was empirically too slow at this order — see git history).
This is mathematically equivalent, just faster; Rule 1 (exact execution,
no floats) is preserved throughout.

Outputs:
  data/mirror_map/S12_qcoeffs.json
  data/mirror_map/S21_qcoeffs.json

Verify: python scripts/mirror_map_integrality.py && \
        python3 -c "import json; print(json.load(open('data/mirror_map/S12_qcoeffs.json'))['all_integral'])"
"""

import json
import math
import os
import sys
from fractions import Fraction as F

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data", "mirror_map")
os.makedirs(DATA_DIR, exist_ok=True)

N_COEFFS = 30  # "first 30 coefficients" per task T1.3 spec


def compute_u_and_c(A: int, B: int, N: int):
    """
    u[n] = sum_k C(n,k)^A * C(n+k,k)^B                       (exact integers)
    c[n] = sum_k T(n,k) * [A*(H_n - H_{n-k}) + B*(H_{n+k} - H_n)]  (exact rationals)
    where T(n,k) = C(n,k)^A * C(n+k,k)^B and H_m is the m-th harmonic number
    (H_0 := 0). Both computed by direct execution, no floats (Rule 1).
    """
    H = [F(0)]
    for i in range(1, 2 * N + 2):
        H.append(H[-1] + F(1, i))

    u, c = [], []
    for n in range(N + 1):
        usum = 0
        csum = F(0)
        for k in range(n + 1):
            Cnk = math.comb(n, k)
            Cnpk = math.comb(n + k, k)
            term = Cnk ** A * Cnpk ** B
            usum += term
            Hn, Hnk, Hnpk = H[n], H[n - k], H[n + k]
            dlog = A * (Hn - Hnk) + B * (Hnpk - Hn)
            csum += term * dlog
        u.append(usum)
        c.append(csum)
    return u, c


def series_div(b: list, a: list, N: int) -> list:
    """Formal power series division: returns r with b = r * a, a[0] != 0."""
    r = [F(0)] * (N + 1)
    for n in range(N + 1):
        s = F(b[n])
        for k in range(n):
            s -= r[k] * a[n - k]
        r[n] = s / a[0]
    return r


def series_exp(f: list, N: int) -> list:
    """Formal power series exponential exp(f), requires f[0] == 0.
    Uses the derivative-matching recurrence g' = f' g:
        n * g_n = sum_{k=1}^{n} k * f_k * g_{n-k}."""
    assert f[0] == 0, "series_exp requires zero constant term"
    g = [F(0)] * (N + 1)
    g[0] = F(1)
    for n in range(1, N + 1):
        s = F(0)
        for k in range(1, n + 1):
            s += k * f[k] * g[n - k]
        g[n] = s / n
    return g


def mirror_map_coefficients(A: int, B: int, N: int) -> dict:
    u, c = compute_u_and_c(A, B, N)
    u_frac = [F(x) for x in u]
    ratio = series_div(c, u_frac, N)          # ytilde(z) / y0(z)
    qz_over_z = series_exp(ratio, N)          # exp(ratio) = q(z)/z

    coeffs = [str(x) for x in qz_over_z]      # exact rationals as strings (Rule 5)
    all_integral = all(x.denominator == 1 for x in qz_over_z)
    first_non_integral = next(
        (i for i, x in enumerate(qz_over_z) if x.denominator != 1), None
    )

    return {
        "u_values": [str(x) for x in u],
        "q_over_z_coefficients": coeffs,   # index 0..N, q(z)/z = sum coeffs[n] z^n
        "n_coefficients_checked": N,
        "all_integral": all_integral,
        "first_non_integral_index": first_non_integral,
    }


def main():
    results = {}
    for name, A, B in [("S12", 1, 2), ("S21", 2, 1)]:
        print(f"Computing mirror map for {name} (A={A}, B={B}), {N_COEFFS} coefficients ...")
        res = mirror_map_coefficients(A, B, N_COEFFS)
        results[name] = res

        out_path = os.path.join(DATA_DIR, f"{name}_qcoeffs.json")
        with open(out_path, "w") as f:
            json.dump(res, f, indent=2)
        print(f"  Wrote {out_path}")

        verdict = "✅ ALL INTEGRAL" if res["all_integral"] else f"❌ NON-INTEGRAL at n={res['first_non_integral_index']}"
        print(f"  Verdict: {verdict}")
        print(f"  q(z)/z coefficients (n=0..10): {res['q_over_z_coefficients'][:11]}")
        print()

    print("=" * 72)
    print("SUMMARY (Task T1.3 — Mirror-map integrality)")
    print("=" * 72)
    any_failed = False
    for name, res in results.items():
        status = "✅ INTEGRAL (necessary condition for K3 PASSES)" if res["all_integral"] else "❌ NON-INTEGRAL (evidence AGAINST K3 identification)"
        if not res["all_integral"]:
            any_failed = True
        print(f"  {name}: {status}  ({res['n_coefficients_checked']} coefficients checked)")

    return 1 if any_failed else 0


if __name__ == "__main__":
    sys.exit(main())
