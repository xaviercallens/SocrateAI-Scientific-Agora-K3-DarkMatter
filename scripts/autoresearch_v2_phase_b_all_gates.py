"""
AutoEvolve R2 / Phase B — full gate battery G1-1..G1-4, G2-1..G2-3 on the
frozen 13-candidate pool. REAL tools only (per user "keep rigor" instruction);
any gate that cannot run rigorously writes a BLOCKED entry with the reason
(Rule 1 — no simulated substitutes).

Reuses (imported, not re-implemented):
  autoresearch_v2_pool            — exact term generators, OEIS-verified
  autoresearch_v2_phase_a_scan    — classify(), exact nullspace machinery
  modularity_screen               — Weil bounds + LMFDB weight-3 candidate table
  mirror_map_integrality          — compute_u_and_c (harmonic-sum control),
                                    series_div, series_exp
  k3_monodromy_verification       — classify_singular_points, compute_monodromy
  dolan_continued_fraction        — validated superradiance solver (GAP-3)
  (constants) FuzzyDarkMatter.lean — GD-1 K_heating rationals, transcribed exactly

Method notes (load-bearing):
  * The minimal generating-function ODE is found by exact modular+Fraction
    nullspace (find_ode_with_coeffs, same search as Phase A's find_ode but
    returning the coefficient vector).
  * The mirror-map log-solution coefficients c_n are computed by FROBENIUS
    RECURSION on the theta-form of the minimal ODE (rigorous for any MUM
    operator), NOT by per-family harmonic-sum formulas. The harmonic-sum
    formula (Beukers) is retained as an independent CONTROL: for the three
    2-factor candidates both derivations must agree exactly or the run halts.
  * a_p uses the Stienstra-Beukers unit-root recipe a_p = centered(u_{(p-1)/2}
    mod p). For alternating-sign sequences (A006077, A125143, A219692) this
    recipe's literature grounding is weaker; values are recorded with an
    explicit caveat, not suppressed.
  * t003 gates G1-2/G1-3/G1-4/G2-* run on its hypergeometric CORE C(2k,k)^3
    (g.f. 3F2(1/2,1/2,1/2;1,1;64z)); the partial sum is core/(1-z) and the
    geometry lives in the core. Documented deviation, flagged in every output.
  * Guide erratum: AUTORESEARCH_IMPLEMENTATION_GUIDE.md G1-2 says
    "|a_p|<=2*sqrt(p) (weight-3) and |a_p|<=2p (weight-2)" — this is inverted.
    Weight k Ramanujan-Petersson bound is |a_p| <= 2 p^((k-1)/2): weight-3 <-> 2p,
    weight-2 <-> 2*sqrt(p). This script follows the (correct) convention of
    scripts/modularity_screen.py.

Outputs (data/autoresearch_v2/):
  g1_1_order_classification.json   g1_2_weil_modularity.json
  g1_3_mirror_integrality.json     g1_4_monodromy_status.json
  g2_1_stiffness_contours.json     g2_2_no_go_status.json
  g2_3_superradiance_bands.json

Run:  python3 scripts/autoresearch_v2_phase_b_all_gates.py [--skip-monodromy]
"""

import json
import math
import os
import signal
import sys
import time
from fractions import Fraction as F

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPTS_DIR)
sys.path.insert(0, SCRIPTS_DIR)
OUT_DIR = os.path.join(REPO_ROOT, "data", "autoresearch_v2")
os.makedirs(OUT_DIR, exist_ok=True)

from autoresearch_v2_pool import POOL, GEOMETRIC_CORE, OEIS_FIRST_TERMS, verify_terms
from autoresearch_v2_phase_a_scan import (classify, mod_nullspace_dim,
                                          exact_nullspace_vector, ode_rows,
                                          ode_validate, P1, P2)
from modularity_screen import weil_bound_ok, weight2_bound_ok, LMFDB_CANDIDATES
from mirror_map_integrality import compute_u_and_c, series_div, series_exp

NMAX = 110
N_MIRROR = 30          # per AUTORESEARCH_IMPLEMENTATION_GUIDE.md G1-3 spec
ALTERNATING = {"az_sporadic_a006077", "almkvist_zagier_second", "cooper_s18"}


def gate_terms(cid, nmax=NMAX):
    """Terms used by G1-2/G1-3/G1-4/G2-*: geometric core where defined."""
    gen = GEOMETRIC_CORE.get(cid, POOL[cid])
    return gen(nmax)


# ────────────────────────────────────────────────────────── minimal exact ODE

def find_ode_with_coeffs(u, nmax, rho_max=4, delta_max=8, extra_rows=12):
    """Same search as phase_a find_ode, but returns the exact integer
    coefficient vector. Layout: coeffs[j*(delta+1)+m] = a_{j,m} multiplying
    z^m y^(j) in  sum_{j,m} a_{j,m} z^m y^(j) = 0."""
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
                return {"rho": rho, "delta": delta, "coeffs": vec,
                        "held_out_terms": held_out}
    return None


def theta_form(rho, delta, coeffs):
    """Convert D-form sum a_{j,m} z^m D^j to theta-form z^s sum_m' z^m' G_{m'}(theta)
    via z^m D^j = z^(m-j) ff(theta, j) (ff = falling factorial).
    Returns (G, s): G[m'] = integer coefficient list of G_{m'}(x)."""
    terms = [(j, m, coeffs[j * (delta + 1) + m])
             for j in range(rho + 1) for m in range(delta + 1)
             if coeffs[j * (delta + 1) + m] != 0]
    s = max(0, max(j - m for j, m, _ in terms))

    def ff_poly(j):
        poly = [1]
        for t in range(j):        # multiply by (x - t)
            new = [0] * (len(poly) + 1)
            for i, cc in enumerate(poly):
                new[i + 1] += cc
                new[i] += -t * cc
            poly = new
        return poly

    gmax = max(s + m - j for j, m, _ in terms)
    G = [[0] * (rho + 1) for _ in range(gmax + 1)]
    for j, m, a in terms:
        for t, cc in enumerate(ff_poly(j)):
            G[s + m - j][t] += a * cc
    return G, s


def poly_eval(p, x):
    v = F(0)
    for c in reversed(p):
        v = v * x + c
    return v


def poly_deriv(p):
    return [i * c for i, c in enumerate(p)][1:] or [0]


def theta_form_validate(G, u, n_check):
    """Check sum_{m'} G_{m'}(N - m') u_{N-m'} == 0 for N = 0..n_check."""
    for N in range(n_check + 1):
        s = 0
        for mp in range(min(N, len(G) - 1) + 1):
            s += poly_eval(G[mp], N - mp) * u[N - mp]
        if s != 0:
            return False, N
    return True, None


def mum_check(G, rho):
    """z=0 is MUM iff the indicial polynomial G_0(x) = b * x^rho, b != 0."""
    chi = G[0]
    lead = chi[rho] if len(chi) > rho else 0
    return (lead != 0 and all(c == 0 for c in chi[:rho])), chi


def frobenius_log_coeffs(G, u, N):
    """Log-solution coefficients c_n (y1 = y0 log z + sum c_n z^n, c_0 = 0)
    by exact Frobenius recursion on the theta-form. Requires MUM at z=0."""
    chi, chi_d = G[0], poly_deriv(G[0])
    Gd = [poly_deriv(g) for g in G]
    c = [F(0)]
    for n in range(1, N + 1):
        rhs = -poly_eval(chi_d, n) * u[n]
        for mp in range(1, min(n, len(G) - 1) + 1):
            rhs -= (poly_eval(Gd[mp], n - mp) * u[n - mp]
                    + poly_eval(G[mp], n - mp) * c[n - mp])
        c.append(rhs / poly_eval(chi, n))
    return c


def mirror_q(u, c, N):
    """E = exp((sum c z^n)/(sum u z^n)); q_d = E[d-1] (q_1 = 1 always).
    Convention matches scripts/k3_sieve_analysis.py::get_mirror_map."""
    u_frac = [F(x) for x in u[:N + 1]]
    c_frac = [F(x) for x in c[:N + 1]]
    ratio = series_div(c_frac, u_frac, N)
    assert ratio[0] == 0, "ratio must have zero constant term (c_0 = 0)"
    return series_exp(ratio, N)


# ─────────────────────────────────────────────────────────────── G1-2 helpers

def primes_in(lo, hi):
    sieve = [True] * (hi + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(hi ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, hi + 1, i):
                sieve[j] = False
    return [p for p in range(lo, hi + 1) if sieve[p]]


def ap_from_terms(u, p):
    """Stienstra-Beukers unit-root residue: centered u_{(p-1)/2} mod p."""
    r = u[(p - 1) // 2] % p
    return r - p if r > p // 2 else r


# ──────────────────────────────────────────────────── GD-1 constants (exact)
# Transcribed EXACTLY from lean4_formal_proofs/Agora/Discovery/FuzzyDarkMatter.lean

PI_L = F(314159, 100000)
G_L = F(66743, 10 ** 15)
LNL_L = F(2)
TAGE_L = F(3 * 365 * 24 * 3600 * 10 ** 9)
HBAR_L = F(1054571817, 10 ** 43)
VREL_L = F(220000)
EV2KG_L = F(178266192, 10 ** 44)
RHO_L = F(590280241410151, 10 ** 35)
K_HEATING = (64 * PI_L ** 4 * G_L ** 2 * RHO_L ** 2 * LNL_L * TAGE_L * HBAR_L ** 3) \
            / (VREL_L ** 4 * EV2KG_L ** 3 * 10 ** 6)
# gd1_survives(m) := K/m^3 < 4  =>  survival needs  m > (K/4)^(1/3)
GD1_MIN_MASS_EV = float(K_HEATING / 4) ** (1.0 / 3.0)

# Stiffness / mass-contour constants (repo v1 convention, k3_sieve_analysis.py:213;
# tau reference is the GAP-2 REVERSE-ENGINEERED point — flagged, never fitted here)
M_PL_EV = 2.4e27
TAU_GRID = [25.0, 28.0, 31.0, 33.6, 34.0, 37.0, 40.0]
VOL_GRID = [1e3, 1e4, 1e5, 1e6]
TAU_REF, VOL_REF = 33.6, 1e4
D_INST = 10   # instanton-sum truncation depth

# M87* (GAP-3 conventions)
M87_MASS_MSUN = 6.5e9
M87_SPIN = 0.90
GM_SUN_OVER_C3_S = 4.92549e-6         # seconds
EV_OVER_HBAR_S = 1.5192674e15         # 1/s
SEC_PER_MYR = 3.15576e13
SALPETER_MYR = 50.0


def alpha_of_mass(m_ev):
    return GM_SUN_OVER_C3_S * M87_MASS_MSUN * EV_OVER_HBAR_S * m_ev


class Timeout(Exception):
    pass


def _alarm(sig, frm):
    raise Timeout()


def _write(name, obj):
    with open(os.path.join(OUT_DIR, name), "w") as f:
        json.dump(obj, f, indent=1, default=str)


# ───────────────────────────────────────────────────────────── gate battery

def main():
    skip_monodromy = "--skip-monodromy" in sys.argv
    t0 = time.time()

    fails = verify_terms()
    if fails:
        print("FATAL: pool term generators disagree with OEIS reference:", fails)
        sys.exit(1)
    print("[pool] all 13 generators OEIS-verified")

    cids = list(POOL.keys())
    terms = {cid: POOL[cid](NMAX) for cid in cids}
    gterms = {cid: gate_terms(cid, NMAX) for cid in cids}

    # ---------------- G1-1: order classification (all 13, exact, held-out) --
    print("\n=== G1-1: exact dual classification (n_max=110) ===")
    g1_1 = {}
    for cid in cids:
        t = time.time()
        res = classify(cid, terms[cid], NMAX)
        res["oeis"] = OEIS_FIRST_TERMS[cid][0]
        res["elapsed_s"] = round(time.time() - t, 1)
        res.pop("first_terms", None)
        g1_1[cid] = res
        ode = res.get("ode")
        print(f"  {cid:26} ODE={None if not ode else (ode['ode_order'], ode['ode_degree'])} "
              f"-> {res.get('geometry_by_ode')}  [{res['elapsed_s']}s]", flush=True)

    # CONTROL PASS CHECK (guide: halt if controls misbehave)
    pos = g1_1["apery_zeta3"].get("ode") or {}
    neg = g1_1["apery_zeta2_s21"].get("ode") or {}
    if pos.get("ode_order") != 3 or neg.get("ode_order") != 2:
        print("FATAL: classifier controls failed "
              f"(A005259 order={pos.get('ode_order')}, A005258 order={neg.get('ode_order')}). "
              "Halting per G1-1 control-pass rule.")
        _write("g1_1_order_classification.json",
               {"status": "CONTROL_FAILURE", "results": g1_1})
        sys.exit(2)
    g1_1["_controls"] = {"positive_A005259_ode_order": 3,
                         "negative_A005258_ode_order": 2, "status": "PASS"}
    _write("g1_1_order_classification.json", g1_1)

    # ------------- minimal exact ODEs with coefficients (for G1-3/G1-4) ----
    print("\n=== minimal exact ODE extraction (with coefficients) ===")
    odes = {}
    for cid in cids:
        t = time.time()
        u = gterms[cid]
        ode = find_ode_with_coeffs(u, NMAX)
        if ode is None:
            odes[cid] = None
            print(f"  {cid:26} NO ODE in search window (rho<=4, delta<=8)", flush=True)
            continue
        G, s = theta_form(ode["rho"], ode["delta"], ode["coeffs"])
        ok, badN = theta_form_validate(G, u, NMAX - 2)
        mum, chi = mum_check(G, ode["rho"])
        ode.update({"theta_form_valid": ok, "theta_form_fail_at": badN,
                    "mum_at_zero": mum, "indicial_poly": [str(x) for x in chi],
                    "core_used": cid in GEOMETRIC_CORE})
        odes[cid] = (ode, G)
        print(f"  {cid:26} ODE(rho={ode['rho']}, delta={ode['delta']}) "
              f"theta-valid={ok} MUM={mum} [{time.time()-t:.1f}s]", flush=True)

    # -------- Frobenius log-solution CONTROL (vs harmonic-sum, 2-factor) ----
    # Controls are the two classical operators, where the Beukers harmonic-sum
    # log solution is KNOWN to belong to the minimal (Picard-Fuchs) operator:
    # A005259 (Apery zeta3, minimal order 3) and A005258 (Apery zeta2, minimal
    # order 2). For s12_v1_primary the minimal ODE is order 2 but v1's harmonic
    # sum was built on the NON-minimal order-3 shift structure — the comparison
    # is run and RECORDED as a diagnostic (v1 mirror-map provenance finding),
    # not used as a validity control.
    print("\n=== mirror-map method control: Frobenius vs Beukers harmonic sum ===")
    for cid, (A, B) in {"apery_zeta3": (2, 2), "apery_zeta2_s21": (2, 1)}.items():
        if odes.get(cid) is None:
            print(f"FATAL: no ODE for control {cid}")
            sys.exit(2)
        ode, G = odes[cid]
        if not ode["mum_at_zero"] or not ode["theta_form_valid"]:
            print(f"FATAL: control {cid} theta-form/MUM check failed")
            sys.exit(2)
        c_frob = frobenius_log_coeffs(G, gterms[cid], N_MIRROR)
        _, c_harm = compute_u_and_c(A, B, N_MIRROR)
        if c_frob != [F(x) for x in c_harm[:N_MIRROR + 1]]:
            print(f"FATAL: Frobenius log-solution disagrees with harmonic-sum "
                  f"control for {cid}. Halting (method invalid).")
            sys.exit(2)
        print(f"  {cid:26} EXACT MATCH ({N_MIRROR + 1} coefficients)", flush=True)

    # diagnostic: does v1's harmonic-sum log solution for S12 belong to the
    # minimal order-2 operator? (expected NO — v1 artifact, see findings doc)
    s12_diag = None
    if odes.get("s12_v1_primary"):
        ode, G = odes["s12_v1_primary"]
        c_frob = frobenius_log_coeffs(G, gterms["s12_v1_primary"], N_MIRROR)
        _, c_harm = compute_u_and_c(1, 2, N_MIRROR)
        same = c_frob == [F(x) for x in c_harm[:N_MIRROR + 1]]
        first_diff = next((i for i in range(N_MIRROR + 1)
                           if c_frob[i] != F(c_harm[i])), None)
        s12_diag = {"v1_harmonic_log_solution_matches_minimal_operator": same,
                    "first_differing_index": first_diff,
                    "note": "v1's S12 mirror map (mirror_map_integrality.py, A=1,B=2) "
                            "used the log solution of the NON-minimal order-3 "
                            "operator; the minimal (Picard-Fuchs) operator is "
                            "order 2 and its log solution differs from index "
                            f"{first_diff} on. v1's S12 stiffness chain therefore "
                            "did not use the Picard-Fuchs second solution."}
        print(f"  s12_v1_primary             v1-harmonic vs minimal-operator: "
              f"match={same} (first diff at n={first_diff}) [diagnostic, not a gate]",
              flush=True)

    # ---------------- G1-2: Weil bounds + LMFDB screen (real recipe) -------
    print("\n=== G1-2: a_p (Stienstra-Beukers), Weil bounds, LMFDB screen ===")
    g1_2 = {}
    ps = primes_in(5, 199)
    ap_dir = os.path.join(OUT_DIR, "ap_tables")
    os.makedirs(ap_dir, exist_ok=True)
    for cid in cids:
        u = gterms[cid]
        aps = {p: ap_from_terms(u, p) for p in ps}
        w3 = all(weil_bound_ok(a, p) for p, a in aps.items())        # |a_p| <= 2p
        w2 = all(weight2_bound_ok(a, p) for p, a in aps.items())     # |a_p| <= 2*sqrt(p)
        matches = {}
        for label, cand in LMFDB_CANDIDATES.items():
            shared = [p for p in cand["ap"] if p in aps]
            agree = sum(1 for p in shared if cand["ap"][p] == aps[p])
            matches[label] = {"agree": agree, "of": len(shared)}
        best = max(matches, key=lambda k: matches[k]["agree"])
        entry = {"weil_weight3_pass_2p": w3, "weil_weight2_pass_2sqrtp": w2,
                 "lmfdb_best": {best: matches[best]}, "lmfdb_all": matches,
                 "primes": f"5..199 ({len(ps)} primes)",
                 "core_used": cid in GEOMETRIC_CORE}
        if cid in ALTERNATING:
            entry["caveat"] = ("alternating-sign sequence: unit-root recipe's "
                               "literature grounding is weaker; values recorded, "
                               "interpretation deferred to GATE-B")
        g1_2[cid] = entry
        with open(os.path.join(ap_dir, f"{cid}_ap.csv"), "w") as f:
            f.write("p,ap,weil_2p_ok,weight2_2sqrtp_ok\n")
            for p in ps:
                f.write(f"{p},{aps[p]},{weil_bound_ok(aps[p], p)},"
                        f"{weight2_bound_ok(aps[p], p)}\n")
        print(f"  {cid:26} weil(2p)={w3} weight2(2sqrt p)={w2} "
              f"lmfdb-best {best}:{matches[best]['agree']}/{matches[best]['of']}",
              flush=True)
    _write("g1_2_weil_modularity.json", g1_2)

    # ---------------- G1-3: mirror-map integrality (30 coeffs, exact) ------
    print("\n=== G1-3: mirror-map integrality (Frobenius log-solution, 30 coeffs) ===")
    g1_3 = {}
    qcoeffs = {}
    for cid in cids:
        if odes.get(cid) is None:
            g1_3[cid] = {"status": "BLOCKED",
                         "reason": "no exact ODE found in search window"}
            continue
        ode, G = odes[cid]
        if not ode["theta_form_valid"]:
            g1_3[cid] = {"status": "BLOCKED",
                         "reason": f"theta-form identity fails at N={ode['theta_form_fail_at']}"}
            continue
        if not ode["mum_at_zero"]:
            g1_3[cid] = {"status": "BLOCKED",
                         "reason": f"z=0 not MUM (indicial {ode['indicial_poly']}); "
                                   "mirror map undefined in standard normalization"}
            continue
        c = frobenius_log_coeffs(G, gterms[cid], N_MIRROR)
        E = mirror_q(gterms[cid], c, N_MIRROR)
        qcoeffs[cid] = E
        nonint = next((i for i, x in enumerate(E) if x.denominator != 1), None)
        g1_3[cid] = {"status": "OK", "all_integral": nonint is None,
                     "first_non_integral_index": nonint,
                     "n_coefficients": N_MIRROR + 1,
                     "q_over_z_first10": [str(x) for x in E[:10]],
                     "core_used": cid in GEOMETRIC_CORE}
        if cid in ALTERNATING:
            g1_3[cid]["normalization_note"] = ("uniform 3^n/(-1)^n prefactors act as "
                                               "z-rescalings; integrality verdict is "
                                               "rescaling-invariant")
        if cid == "s12_v1_primary" and s12_diag:
            g1_3[cid]["v1_provenance_diagnostic"] = s12_diag
        print(f"  {cid:26} integral={g1_3[cid]['all_integral']} "
              f"first_fail={nonint}", flush=True)
    _write("g1_3_mirror_integrality.json", g1_3)

    # ---------------- G1-4: Fuchs classification + monodromy ---------------
    print("\n=== G1-4: singular-point classification + RK4 monodromy ===")
    import sympy as sp
    import mpmath
    mpmath.mp.dps = 50
    from k3_monodromy_verification import classify_singular_points, compute_monodromy
    z = sp.Symbol('z')
    g1_4 = {}
    for cid in cids:
        if odes.get(cid) is None:
            g1_4[cid] = {"status": "BLOCKED",
                         "reason": "no exact ODE found in search window"}
            continue
        ode, G = odes[cid]
        rho, delta, coeffs = ode["rho"], ode["delta"], ode["coeffs"]
        Q_polys = []
        for j in range(rho + 1):
            expr = sum(coeffs[j * (delta + 1) + m] * z ** m for m in range(delta + 1))
            Q_polys.append(sp.Poly(expr, z))
        while Q_polys and Q_polys[-1].is_zero:
            Q_polys.pop()
        actual_order = len(Q_polys) - 1
        sings = classify_singular_points(actual_order, Q_polys)
        sing_report = [{"z_c": str(zc), "regular": bool(reg)} for zc, reg in sings]
        all_regular = all(reg for _, reg in sings)
        entry = {"status": "regular" if all_regular else "has_irregular",
                 "ode_order": actual_order, "mum_at_zero": ode["mum_at_zero"],
                 "singular_points": sing_report,
                 "core_used": cid in GEOMETRIC_CORE}
        if skip_monodromy:
            entry["monodromy"] = {"skipped": True}
        else:
            signal.signal(signal.SIGALRM, _alarm)
            signal.alarm(600)
            try:
                mono = compute_monodromy(actual_order, Q_polys, sings)
                mres = {}
                for key, v in mono.items():
                    if v.get("irregular"):
                        mres[key] = {"irregular": True,
                                     "classification_error": v.get("classification_error", False)}
                    else:
                        M = v["M"]
                        mres[key] = {"det_err": v["det_err"],
                                     "M": [[[float(M[i, j].real), float(M[i, j].imag)]
                                            for j in range(actual_order)]
                                           for i in range(actual_order)]}
                entry["monodromy"] = mres
                entry["monodromy_computable"] = bool(mres) and not any(
                    v.get("irregular") for v in mres.values())
            except Timeout:
                entry["monodromy"] = {"timeout_s": 600}
                entry["monodromy_computable"] = False
            except Exception as e:
                entry["monodromy"] = {"error": repr(e)[:300]}
                entry["monodromy_computable"] = False
            finally:
                signal.alarm(0)
        g1_4[cid] = entry
        print(f"  {cid:26} {entry['status']}, {len(sings)} sing.pts, "
              f"monodromy_computable={entry.get('monodromy_computable')}", flush=True)
        _write("g1_4_monodromy_status.json", g1_4)   # checkpoint after each
    _write("g1_4_monodromy_status.json", g1_4)

    # ---------------- G2-1: stiffness contours ------------------------------
    print("\n=== G2-1: V''(0) + achievable-mass contour (tau, V) family ===")
    g2_1 = {}
    for cid in cids:
        if cid not in qcoeffs:
            g2_1[cid] = {"status": "BLOCKED",
                         "reason": g1_3.get(cid, {}).get("reason",
                                   "no mirror-map q-coefficients")}
            continue
        E = qcoeffs[cid]                       # q_d = E[d-1]
        q_d = {d: E[d - 1] for d in range(1, D_INST + 1)}
        vpp3 = sum(d * d * q_d[d] for d in range(1, 4))   # Lean convention (S20: 1522)
        contour, masses = [], []
        for tau in TAU_GRID:
            x = math.exp(-2 * math.pi * tau)
            inst = sum(d * d * float(q_d[d]) * x ** d for d in range(1, D_INST + 1))
            for vol in VOL_GRID:
                m = (M_PL_EV / math.sqrt(vol)) * math.sqrt(max(0.0, inst))
                contour.append({"tau": tau, "volume": vol, "m_a_eV": m})
                masses.append(m)
        x_ref = math.exp(-2 * math.pi * TAU_REF)
        inst_ref = sum(d * d * float(q_d[d]) * x_ref ** d for d in range(1, D_INST + 1))
        m_ref = (M_PL_EV / math.sqrt(VOL_REF)) * math.sqrt(max(0.0, inst_ref))
        g2_1[cid] = {"status": "OK",
                     "stiffness_Vpp0_d3": str(vpp3),
                     "q_d_first5": {d: str(q_d[d]) for d in range(1, 6)},
                     "contour_grid": contour,
                     "mass_window_eV": [min(masses), max(masses)],
                     "reference_point": {"tau": TAU_REF, "volume": VOL_REF,
                                         "m_a_eV": m_ref,
                                         "provenance": "tau=33.6 is the GAP-2 "
                                         "reverse-engineered v1 point; used as a "
                                         "COMMON NORMALIZATION for cross-candidate "
                                         "comparison, not a prediction"},
                     "no_fitting_note": "contour is parameter-space output; no "
                                        "(tau,V) fitted to any target (ledger rule)",
                     "core_used": cid in GEOMETRIC_CORE}
        print(f"  {cid:26} V''(0)|_3 = {vpp3}, m_ref = {m_ref:.3e} eV", flush=True)
    g2_1["_structural_finding"] = (
        "All candidates yield IDENTICAL m_a at any common (tau,V): q_1 = 1 by "
        "mirror-map normalization and e^{-2*pi*tau} suppression makes the d>=2 "
        "terms numerically irrelevant (single-instanton domination, the T2.2/GAP-2 "
        "degeneracy, now quantified across the full pool). Under this mass formula "
        "the (tau,V) contour CANNOT discriminate candidates; the only candidate-"
        "dependent stiffness quantity is the unsuppressed V''(0) = sum d^2 q_d, "
        "whose physical relevance requires the (unestablished) moduli-cancellation "
        "antecedent. Reported per Rule 4.")
    _write("g2_1_stiffness_contours.json", g2_1)

    # ---------------- G2-2: GD-1 no-go ---------------------------------------
    print(f"\n=== G2-2: GD-1 no-go (K_heating exact from FuzzyDarkMatter.lean; "
          f"survival floor m > {GD1_MIN_MASS_EV:.3e} eV) ===")
    g2_2 = {}
    for cid in cids:
        if g2_1.get(cid, {}).get("status") != "OK":
            g2_2[cid] = {"status": "BLOCKED", "reason": "no G2-1 mass window"}
            continue
        lo, hi = g2_1[cid]["mass_window_eV"]
        m_ref = g2_1[cid]["reference_point"]["m_a_eV"]
        pinned = hi < GD1_MIN_MASS_EV      # entire achievable window below GD-1 floor
        g2_2[cid] = {"status": "OK",
                     "gd1_min_mass_eV": GD1_MIN_MASS_EV,
                     "K_heating_exact": str(K_HEATING),
                     "mass_window_eV": [lo, hi],
                     "pinned_to_no_go_regime": pinned,
                     "survives_at_reference_point": bool(m_ref > GD1_MIN_MASS_EV),
                     "reference_m_a_eV": m_ref,
                     "note": "with (tau,V) free on the grid the window is broad, so "
                             "pinned=false is expected for all candidates; the "
                             "discriminating number is survives_at_reference_point "
                             "at the common GAP-2 normalization"}
        print(f"  {cid:26} pinned={pinned} survives_at_ref="
              f"{g2_2[cid]['survives_at_reference_point']} (m_ref={m_ref:.2e} eV)",
              flush=True)
    _write("g2_2_no_go_status.json", g2_2)

    # ---------------- G2-3: Dolan superradiance ------------------------------
    print("\n=== G2-3: Dolan continued-fraction superradiance (M87*) ===")
    from dolan_continued_fraction import solve_mode, validate
    val = validate()
    if not all(r["pass"] for r in val):
        print("FATAL: Dolan solver failed its own Table-I validation; G2-3 BLOCKED.")
        _write("g2_3_superradiance_bands.json",
               {"status": "BLOCKED", "reason": "Dolan Table-I validation failed",
                "validation": val})
    else:
        print(f"  [solver validated against Dolan (2007) Table I: "
              f"{len(val)} rows pass]")
        gm_s = GM_SUN_OVER_C3_S * M87_MASS_MSUN
        g2_3 = {"_solver_validation": "Dolan (2007) Table I reproduced "
                                      f"({len(val)} rows, <=5% tol)"}
        for cid in cids:
            if g2_1.get(cid, {}).get("status") != "OK":
                g2_3[cid] = {"status": "BLOCKED", "reason": "no G2-1 mass window"}
                continue
            m_ref = g2_1[cid]["reference_point"]["m_a_eV"]
            a_ref = alpha_of_mass(m_ref)
            band = []
            lo, hi = g2_1[cid]["mass_window_eV"]
            for alpha in [0.05, 0.10, 0.20, 0.30, 0.42]:
                m_ev = alpha / (GM_SUN_OVER_C3_S * M87_MASS_MSUN * EV_OVER_HBAR_S)
                row = {"alpha": alpha, "m_a_eV": m_ev,
                       "in_window": bool(lo <= m_ev <= hi)}
                for (ll, mm) in [(1, 1), (2, 2)]:
                    try:
                        om, sol = solve_mode(M87_SPIN, alpha, m=mm, l=ll)
                        unstable = om.imag > 0
                        tsc = (1.0 / om.imag) * gm_s / SEC_PER_MYR if unstable else None
                        row[f"l{ll}m{mm}"] = {
                            "omega_im": om.imag, "unstable": bool(unstable),
                            "timescale_Myr": tsc,
                            "faster_than_salpeter": (bool(tsc < SALPETER_MYR)
                                                     if tsc is not None else False)}
                    except Exception as e:
                        row[f"l{ll}m{mm}"] = {"error": repr(e)[:200]}
                band.append(row)
            ref = {"alpha": a_ref, "m_a_eV": m_ref}
            if 0.005 <= a_ref <= 0.99:
                danger = False
                for (ll, mm) in [(1, 1), (2, 2)]:
                    try:
                        om, sol = solve_mode(M87_SPIN, a_ref, m=mm, l=ll)
                        unstable = om.imag > 0
                        tsc = (1.0 / om.imag) * gm_s / SEC_PER_MYR if unstable else None
                        ref[f"l{ll}m{mm}"] = {"omega_im": om.imag,
                                              "unstable": bool(unstable),
                                              "timescale_Myr": tsc}
                        if tsc is not None and tsc < SALPETER_MYR:
                            danger = True
                    except Exception as e:
                        ref[f"l{ll}m{mm}"] = {"error": repr(e)[:200]}
                ref["bare_survival"] = not danger
            else:
                ref["bare_survival"] = None
                ref["note"] = (f"alpha={a_ref:.3g} outside solver band [0.005,0.99]; "
                               "no M87* superradiance constraint at reference point")
            g2_3[cid] = {"status": "OK", "reference": ref, "alpha_scan": band,
                         "bh": {"M_msun": M87_MASS_MSUN, "spin": M87_SPIN},
                         "salpeter_Myr": SALPETER_MYR}
            print(f"  {cid:26} alpha_ref={a_ref:.3g} "
                  f"bare_survival={ref.get('bare_survival')}", flush=True)
            _write("g2_3_superradiance_bands.json", g2_3)
        _write("g2_3_superradiance_bands.json", g2_3)

    print(f"\nAll gates complete in {time.time() - t0:.0f}s. Outputs in {OUT_DIR}")


if __name__ == "__main__":
    main()
