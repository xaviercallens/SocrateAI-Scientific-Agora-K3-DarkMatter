#!/usr/bin/env python3
"""
check_s10_hauptmodul_gamma010star.py -- modular group of the cooper_s10 mirror-map
coordinate z(q). Gate T1 of briefs/STREAM2_K3xT2_SELECTION_CRITERIA_PROPOSAL_2026_09_16.md.
Turns the 2026-08-01 spikes (spike_s10_mirror_map_level.py, spike_s10_modular_structure.py)
into a certificate with negative controls.

What is computed
  S1 (exact). z(q) = inverse mirror map of the refs recurrence for cooper_s10
     (check_C1_mirror_integrality machinery, round trip enforced).
  S2 (exact). t = q * (E(q^2) E(q^10) / (E(q) E(q^5)))^4, i.e. eta exponents
     r = {1:-4, 2:4, 5:-4, 10:4}. Newman/Ligozat conditions for a modular function on
     Gamma_0(10) are evaluated exactly [theorem cited, not re-derived].
  S3 (exact to order N). z = P(t)/Q(t) with deg <= 2 solved on low orders and verified on
     held-out orders; a Mobius (deg 1) fit must FAIL. The relation is reported in the form
     1/z = alpha*t + beta + gamma/t when it has that shape.
  S4 (exact). Ligozat cusp orders of t -> degree of t on X_0(10); degree of z on X_0(10).
  S5 (exact). Fricke w_10: tau -> -1/(10 tau) sends prod eta(d tau)^r_d to
     prod_d (10/d)^(r_d/2) * prod eta((10/d) tau)^r_d (weight 0); the constant K_10 in
     t o w_10 = K_10 / t is computed, and the relation from S3 is checked to be invariant
     under t -> K_10/t exactly.
  S6 (numerical, 50 digits). w_2, w_5 as explicit integer matrices [[Q a, b],[10 c, Q d]]
     of determinant Q. At several points tau, compute t(W tau) and determine the constant
     c_Q in t o w_Q = c_Q * t or t o w_Q = c_Q / t, recognized as a rational with small
     denominator. Invariance of 1/z = alpha t + beta + gamma/t under w_2 and w_5 then follows
     algebraically from those constants (c = 1 for 'inv'; alpha c = gamma for 'anti').

Verdict GAMMA010STAR_HAUPTMODUL requires: S3 deg-2 PASS and Mobius FAIL; z has degree 4 on
X_0(10); invariance under w_10 (exact) and w_2, w_5 (numerical). Degree 4 on X_0(10) and
invariance under the order-4 Atkin-Lehner group give degree 1 on X_0(10)* = Hauptmodul.

Tier B: S6 is numerical recognition; the Newman/Ligozat and Atkin-Lehner statements are
cited. NOT claimed: that the family's moduli space IS X_0(10)* (the open Deep Think
question, briefs/DEEPTHINK_ALIGNMENT_BRIEF_S10_COMPOSITE_LEVEL_2026_08_01.md sec 2.1), or
anything about T(s10).

Negative controls (each must fail as stated):
  N1 wrong level: cooper_s7's z(q) against the same level-10 t -> deg-2 fit fails.
  N2 corrupted: s10 z(q) with one held-out coefficient changed -> verification fails.
  N3 not Atkin-Lehner: tau -> (tau+1)/5 (det 5, not normalizing) -> no small-denominator
     constant relates t(W tau) to t(tau).
  N4 numerics engine: the level-7 coordinate t7 = q (E(q^7)/E(q))^4 under Fricke w_7
     numerically gives the exact constant from the S5 formula (1/49).

Generated-by: Claude (Opus 5), Stream 2 | Verified-by: controls N1-N4 | Reviewed-by: N
"""
import json
import sys
from fractions import Fraction as F
from math import gcd
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_C1_mirror_integrality as C1  # noqa: E402
import check_s7_hauptmodul_gamma07plus as H7  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "certificates" / "HAUPTMODUL_S10_GAMMA010STAR.json"
ORDER = 40
N_SOLVE = 12
LEVEL = 10
R_T = {1: -4, 2: 4, 5: -4, 10: 4}
R_T7 = {1: -4, 7: 4}
mp.mp.dps = 50


# ------------------------------------------------------------ exact series ----
def eta_quotient_series(r, nmax):
    """q^(sum d r_d / 24) * prod E(q^d)^r_d, returned as coefficients of q^0..q^nmax
    after removing the leading power (which must be q^1)."""
    lead = F(sum(d * e for d, e in r.items()), 24)
    assert lead == 1, f"leading power q^{lead}, expected q^1"
    S = [F(1)] + [F(0)] * nmax
    for d, e in r.items():
        Ed = H7.dilate(H7.euler_E(nmax // d + 1), d, nmax)
        base = Ed if e > 0 else H7.ps_inv(Ed, nmax)
        S = H7.ps_mul(S, H7.ps_pow(base, abs(e), nmax), nmax)
    return [F(0)] + S[:nmax]


def newman_conditions(r, N):
    s_r = sum(r.values())
    s_d = sum(d * e for d, e in r.items())
    s_nd = sum((N // d) * e for d, e in r.items())
    prod = F(1)
    for d, e in r.items():
        prod *= F(d) ** e
    num, den = prod.numerator, prod.denominator
    is_square = all(int(round(x ** 0.5)) ** 2 == x for x in (num, den))
    return {"sum_r_zero": s_r == 0, "sum_d_r_mod24": s_d % 24 == 0,
            "sum_Nd_r_mod24": s_nd % 24 == 0, "prod_d_r_is_square": is_square}


def ligozat_orders(r, N):
    divs = [d for d in range(1, N + 1) if N % d == 0]
    return {c: F(N, 24 * gcd(c * c, N)) * sum(F(gcd(c, d) ** 2 * r.get(d, 0), d) for d in divs)
            for c in divs}


def fricke_constant(r, N):
    """t o w_N = K * prod eta((N/d) tau)^r_d with K = prod (N/d)^(r_d/2); returns (K, r')."""
    K = F(1)
    for d, e in r.items():
        assert e % 2 == 0
        K *= F(N, d) ** (e // 2)
    r_new = {N // d: e for d, e in r.items()}
    return K, r_new


# ---------------------------------------------------------------- numerics ----
def eta_num(tau):
    q = mp.e ** (2j * mp.pi * tau)
    s, k = mp.mpf(1), 1
    while True:
        g1, g2 = k * (3 * k - 1) // 2, k * (3 * k + 1) // 2
        t1, t2 = q ** g1, q ** g2
        s += (-1) ** k * (t1 + t2)
        if abs(t1) < mp.mpf(10) ** (-mp.mp.dps - 5):
            break
        k += 1
    return mp.e ** (2j * mp.pi * tau / 24) * s


def eta_quotient_num(r, tau):
    v = mp.mpc(1)
    for d, e in r.items():
        v *= eta_num(d * tau) ** e
    return v


def moebius(M, tau):
    (a, b), (c, d) = M
    return (a * tau + b) / (c * tau + d)


def al_matrix(Q, N):
    """[[Q x, y],[N z, Q w]] with det Q, i.e. Q x w - (N/Q) y z = 1."""
    for x in range(1, 6):
        for w in range(1, 6):
            for y in range(-6, 7):
                for z in range(1, 6):
                    if Q * x * w - (N // Q) * y * z == 1:
                        return ((Q * x, y), (N * z, Q * w))
    raise RuntimeError("no Atkin-Lehner matrix found")


def recognize(x, max_den=100, tol=mp.mpf(10) ** -30):
    """x (complex) -> Fraction if |imag| and |real - p/q| < tol with q <= max_den."""
    if abs(mp.im(x)) > tol:
        return None
    re = mp.re(x)
    for den in range(1, max_den + 1):
        num = int(mp.nint(re * den))
        if abs(re - mp.mpf(num) / den) < tol:
            return F(num, den)
    return None


def al_constant(r, M, taus):
    """Return ('inv', c) if t(W tau) = c t(tau) at all points, ('anti', c) if t(W tau) t(tau) = c,
    else (None, None)."""
    for kind in ("inv", "anti"):
        vals = []
        for tau in taus:
            tw, t0 = eta_quotient_num(r, moebius(M, tau)), eta_quotient_num(r, tau)
            vals.append(tw / t0 if kind == "inv" else tw * t0)
        cs = [recognize(v) for v in vals]
        if cs[0] is not None and all(c == cs[0] for c in cs):
            return kind, cs[0]
    return None, None


TAUS = [mp.mpc("0.13", "0.21"), mp.mpc("-0.31", "0.19"), mp.mpc("0.42", "0.23")]


# ----------------------------------------------------------------- pipeline ---
def z_series(key, order):
    seqs = json.loads(C1.REFS.read_text())["sequences"]
    r = C1.check_entry(key, seqs[key], order)          # refuses on round-trip failure
    assert r["verdict"] == f"PASS({order})"
    _, _, Z = C1.mirror_map(seqs[key]["recurrence_python"], order)
    return Z


def relation_shape(sol):
    """sol = (p0,p1,p2,q0,q1,q2) with z = (p0+p1 t+p2 t^2)/(q0+q1 t+q2 t^2).
    If p0 = p2 = 0: 1/z = (q0 + q1 t + q2 t^2)/(p1 t) = gamma/t + beta + alpha t."""
    p0, p1, p2, q0, q1, q2 = sol
    if p0 == 0 and p2 == 0 and p1 != 0:
        return {"alpha": q2 / p1, "beta": q1 / p1, "gamma": q0 / p1}
    return None


def main():
    report = {}
    z10 = z_series("cooper_s10", ORDER)
    z7 = z_series("cooper_s7", ORDER)
    t = eta_quotient_series(R_T, ORDER)

    newman = newman_conditions(R_T, LEVEL)
    orders = ligozat_orders(R_T, LEVEL)
    deg_t = sum(v for v in orders.values() if v > 0)

    m_s, m_v, _ = H7.rational_fit(z10, t, 1, 6, ORDER)
    d_s, d_v, sol = H7.rational_fit(z10, t, 2, N_SOLVE, ORDER)
    shape = relation_shape(sol) if sol else None
    deg_z = 2 * deg_t if shape else None               # z = t/(alpha t^2 + beta t + gamma)

    K10, r_after = fricke_constant(R_T, LEVEL)
    fricke_anti = r_after == {d: -e for d, e in R_T.items()}
    # 1/z = alpha t + beta + gamma/t invariant under t -> K/t  <=>  alpha K = gamma
    fricke_invariant = bool(shape and fricke_anti and shape["alpha"] * K10 == shape["gamma"])

    al = {}
    for Q in (2, 5):
        M = al_matrix(Q, LEVEL)
        kind, c = al_constant(R_T, M, TAUS)
        al[Q] = {"matrix": M, "kind": kind, "constant": c}
    # 1/z invariant under t -> c t ('inv') needs c = 1 (alpha, gamma both nonzero);
    # under t -> c/t ('anti') needs alpha c = gamma.
    def z_invariant(entry):
        if not shape or entry["constant"] is None:
            return False
        if entry["kind"] == "inv":
            return entry["constant"] == 1
        return shape["alpha"] * entry["constant"] == shape["gamma"]
    al_invariant = {Q: z_invariant(al[Q]) for Q in (2, 5)}

    # ---- controls
    c_ok = {}
    _, n1_v, _ = H7.rational_fit(z7, t, 2, N_SOLVE, ORDER)
    c_ok["N1_wrong_level_s7_fit_fails"] = not n1_v
    z_bad = list(z10); z_bad[ORDER - 3] += 1
    _, n2_v, _ = H7.rational_fit(z_bad, t, 2, N_SOLVE, ORDER)
    c_ok["N2_corrupted_z_verify_fails"] = not n2_v
    n3_kind, _ = al_constant(R_T, ((1, 1), (0, 5)), TAUS)
    c_ok["N3_non_AL_map_no_constant"] = n3_kind is None
    K7, _ = fricke_constant(R_T7, 7)
    n4_kind, n4_c = al_constant(R_T7, ((0, -1), (7, 0)), TAUS)
    c_ok["N4_numerics_reproduce_exact_fricke_7"] = (n4_kind == "anti" and n4_c == K7)

    passed = (all(newman.values()) and d_s and d_v and not (m_s and m_v) and shape is not None
              and deg_z == 4 and fricke_invariant and all(al_invariant.values())
              and all(c_ok.values()))

    print("=" * 76)
    print("cooper_s10 mirror-map coordinate: Hauptmodul for Gamma_0(10)* ?")
    print("=" * 76)
    print(f"S2 Newman/Ligozat conditions for t on Gamma_0(10): {newman}")
    print(f"S3 Mobius fit (must FAIL): {'PASS' if m_s and m_v else 'FAIL'}; "
          f"deg-2 fit: {'PASS' if d_s and d_v else 'FAIL'} (held-out orders {N_SOLVE + 1}..{ORDER})")
    if shape:
        print(f"   1/z = {shape['alpha']}*t + {shape['beta']} + {shape['gamma']}/t")
    print(f"S4 cusp orders of t: { {c: str(v) for c, v in orders.items()} }  deg t = {deg_t}, deg z = {deg_z}")
    print(f"S5 Fricke w_10: t o w_10 = {K10}/t (exact); 1/z invariant: {fricke_invariant}")
    for Q in (2, 5):
        e = al[Q]
        print(f"S6 w_{Q} matrix {e['matrix']}: t -> {e['kind']} with constant {e['constant']}; "
              f"1/z invariant: {al_invariant[Q]}")
    print("-" * 76)
    for k, v in c_ok.items():
        print(f"  {'ok  ' if v else 'FAIL'}  {k}")
    print("-" * 76)
    verdict = "GAMMA010STAR_HAUPTMODUL" if passed else "NOT_ESTABLISHED"
    print(f"VERDICT: {verdict}")

    cert = {
        "certificate": "HAUPTMODUL_S10_GAMMA010STAR",
        "checker": Path(__file__).name,
        "date": "2026-09-17",
        "claim": "the cooper_s10 inverse mirror map z(q) is a Hauptmodul for Gamma_0(10)* "
                 "(Gamma_0(10) extended by all Atkin-Lehner involutions w_2, w_5, w_10)",
        "coordinate_t": {"eta_exponents": {str(d): e for d, e in R_T.items()},
                         "newman_conditions": newman,
                         "cusp_orders": {str(c): str(v) for c, v in orders.items()},
                         "degree_on_X0_10": str(deg_t)},
        "relation": ({k: str(v) for k, v in shape.items()} | {"form": "1/z = alpha*t + beta + gamma/t"})
                    if shape else None,
        "orders": {"z_series_order": ORDER, "solved_on": [0, N_SOLVE], "held_out_verified": [N_SOLVE + 1, ORDER],
                   "mobius_fit_passes": bool(m_s and m_v), "degree2_fit_passes": bool(d_s and d_v)},
        "degree_of_z_on_X0_10": str(deg_z),
        "fricke_w10": {"constant_K": str(K10), "t_anti_invariant": fricke_anti,
                       "one_over_z_invariant": fricke_invariant, "method": "exact eta transformation"},
        "atkin_lehner_numerical": {f"w{Q}": {"matrix": al[Q]["matrix"], "t_transform": al[Q]["kind"],
                                            "constant": str(al[Q]["constant"]),
                                            "one_over_z_invariant": al_invariant[Q]} for Q in (2, 5)},
        "numerics": {"dps": mp.mp.dps, "recognition_tolerance": "1e-30", "max_denominator": 100,
                     "sample_points": [str(x) for x in TAUS]},
        "negative_controls": c_ok,
        "verdict": verdict,
        "tier": "B",
        "tier_reason": "q-series identity and Fricke constant exact; w_2/w_5 constants by 50-digit "
                       "numerical recognition at 3 points; Newman/Ligozat modularity criterion and "
                       "Atkin-Lehner theory cited, not re-derived",
        "not_claimed": [
            "that the moduli space of the cooper_s10 family IS X_0(10)* (open, Deep Think brief sec 2.1)",
            "anything about T(s10) or the value 20 (C2_cooper_s10_v4_DRAFT stays DRAFT, D6')",
            "identities beyond the stated order",
        ],
        "provenance": "Generated-by: Claude (Opus 5), Stream 2 | Verified-by: negative controls N1-N4 in this "
                      "checker | Reviewed-by: N",
    }
    if "--emit" in sys.argv:
        OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"certificate: {OUT.relative_to(REPO)}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
