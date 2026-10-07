#!/usr/bin/env python3
"""check_TW0_hodge_degree_orbifold.py -- WP-TW0 re-examination: what "Hodge-bundle degree ell = 2"
can and cannot mean for the cooper_s7 family, computed exactly in exponent language.

Ledger item 6 carries ell = 2 as Tier B-external "pending WP-TW0; if it lands != 2, F6 disclosure
+ T0 escalation". The 2026-07-29 draft (briefs/TW0_HODGE_DEGREE_RESULT_2026_07_29.md,
checkers/check_TW0_hodge_degree.py) reports ell = 2 from the formula deg L_ell = (sum of
exponents)/order = 1, then doubles. That formula has no cited source, and this checker shows it
is a tautology for the class of operators in play: for any order-2 Fuchsian operator with s
singular points the Fuchs relation forces sum of exponents = s - 2, so with s = 4 the formula
returns 1 for EVERY such operator (control C5) -- it cannot discriminate families, so it cannot
verify anything about this one (standing rule 1).

WHAT IS COMPUTED (all exact, sympy Rational; the operator tuple is the same Tier-A-verified
theta-form tuple used by checkers/check_L3_riemann_scheme.py, not re-typed):
  A. Riemann scheme of L2 at every singular point including z = 0 (MUM, exponents {0,0}); Fuchs
     relation with the correct count of singular points (4, not the 3 the 07-29 brief lists).
  B. Signature of the base orbifold two independent ways: (i) from the exponents (exponent
     difference 1/e <-> elliptic point of order e; repeated 0 <-> cusp); (ii) from group theory
     for Gamma_0(N)+ (index, epsilon_2/epsilon_3 by Legendre symbols, cusps, Fricke fixed points
     by class numbers counted from reduced forms). They must agree.
  C. Orbifold (Q-line-bundle) degrees: deg omega = -chi_orb/2, deg omega^2 = -chi_orb, for the
     weight-1 / weight-2 line bundles (the elliptic / K3 Hodge line bundles, Doran Thm 5.13: the
     K3 period is the square of the elliptic period).
  D. Deligne-extension integer degrees on the coarse P^1 under both residue conventions
     ([0,1) and (-1,0]): pardeg = deg + sum(alpha), alpha = exponent of the holomorphic period.
  E. The elliptic-SURFACE reading: for a K3 (h^{0,1}=0, h^{0,2}=1) Noether gives e = 12 chi(O) = 24
     = deg Delta = 12 ell, so ell = chi(O_K3) = 2 -- a fact about any elliptic K3 with section,
     not about the family over the modular curve.

FINDING, stated once: under every standard reading of "degree of the Hodge line bundle of the
family", the number is 1/3, 2/3, 0 or 1 -- never 2. The ratified ell = 2 is reproduced only by
reading E. Which reading WP-TW1 ("deg Delta = 48 on P^3") needs is a T0 question; this checker
does not edit the ledger. Exponent language only; no Kodaira label anywhere (ledger items 3, 10).

Controls: checkers/test_TW0_hodge_degree_orbifold_controls.py (wrong level, wrong operator,
Fuchs violation refused, the 07-29 formula shown non-discriminating, Noether sanity).

Generated-by: Claude (Fable 5.1), Stream 2, 2026-10-07 | Verified-by: controls above; the
signature agreement B(i) == B(ii) | Reviewed-by: N
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from math import gcd
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parent.parent
CERT = REPO / "data" / "certificates" / "TW0_HODGE_DEGREE_ORBIFOLD.json"
z, r = sp.symbols("z r")

# theta-form tuples (P2, P1, P0): identical to checkers/check_L3_riemann_scheme.py OPERATORS[*]["P"]
OPERATORS = {
    "cooper_s7": {"level": 7, "P": (-27 * z**2 - 26 * z + 1, -27 * z**2 - 13 * z, -6 * z**2 - 2 * z)},
    "cooper_s10": {"level": 10, "P": (-64 * z**2 - 12 * z + 1, -64 * z**2 - 6 * z, -15 * z**2 - z)},
}


class Refuse(RuntimeError):
    pass


# ---------------------------------------------------------------- A. Riemann scheme
def _roots_with_multiplicity(expr):
    return sorted(sum(([root] * mult for root, mult in sp.roots(sp.Poly(sp.expand(expr), r)).items()), []))


def riemann_scheme(P):
    P2, P1, P0 = P
    A2, A1, A0 = sp.expand(z**2 * P2), sp.expand(z * (P2 + P1)), sp.expand(P0)
    p, q = sp.cancel(A1 / A2), sp.cancel(A0 / A2)
    out = {}
    def finite_or_refuse(val, where):
        if val.is_finite is not True:
            raise Refuse(f"irregular singular point at {where}: local data {val} not finite; not a Fuchsian operator")
        return val

    for zc in sp.solve(A2, z):
        p0 = finite_or_refuse(sp.limit((z - zc) * p, z, zc), zc)
        q0 = finite_or_refuse(sp.limit((z - zc) ** 2 * q, z, zc), zc)
        out[str(zc)] = _roots_with_multiplicity(r * (r - 1) + p0 * r + q0)
    pinf = finite_or_refuse(sp.limit(z * p, z, sp.oo), "oo")
    qinf = finite_or_refuse(sp.limit(z**2 * q, z, sp.oo), "oo")
    out["oo"] = _roots_with_multiplicity(r * (r + 1) - pinf * r + qinf)
    s = len(out)
    total = sum(sum(v) for v in out.values())
    if total != s - 2:
        raise Refuse(f"Fuchs relation violated: sum of exponents {total} != n_sing - 2 = {s - 2}")
    return out, s, total


# ---------------------------------------------------------------- B(i). signature from exponents
def signature_from_exponents(scheme):
    sig = {"genus": 0, "elliptic_orders": [], "cusps": 0}
    for pt, ex in scheme.items():
        d = ex[1] - ex[0]
        if d == 0:
            sig["cusps"] += 1
        else:
            e = sp.Rational(1, 1) / d
            if e.q != 1:
                raise Refuse(f"exponent difference {d} at {pt} is not 1/e for an integer e")
            sig["elliptic_orders"].append(int(e))
    sig["elliptic_orders"].sort()
    return sig


# ---------------------------------------------------------------- B(ii). signature from Gamma_0(N)+
def class_number(D):
    n = 0
    a = 1
    while 3 * a * a <= abs(D) + 3:
        for b in range(-a + 1, a + 1):
            if (b * b - D) % (4 * a) == 0:
                c = (b * b - D) // (4 * a)
                if c >= a and gcd(gcd(a, abs(b)), c) == 1 and not (a == c and b < 0):
                    n += 1
        a += 1
    return n


def legendre(a, p):
    """(a/p) as used in the Gamma_0(N) elliptic-point counts (Diamond-Shurman Fig. 3.3 convention):
    Legendre for odd p; at p = 2, (-1/2) := 0 and (-3/2) := -1."""
    if p == 2:
        return {-1: 0, -3: -1}[a]
    return sp.legendre_symbol(a % p, p) if a % p else 0


def signature_gamma0_plus(N):
    primes = sp.primefactors(N)
    mu = N * sp.prod([1 + sp.Rational(1, p) for p in primes])
    e2 = sp.prod([1 + legendre(-1, p) for p in primes]) if N % 4 else 0
    e3 = sp.prod([1 + legendre(-3, p) for p in primes]) if N % 9 else 0
    cusps = sum(sp.totient(gcd(d, N // d)) for d in sp.divisors(N))
    g = 1 + sp.Rational(mu, 12) - sp.Rational(e2, 4) - sp.Rational(e3, 3) - sp.Rational(cusps, 2)
    if N <= 4:
        raise Refuse("Fricke fixed-point count used here is for N > 4")
    fixed = class_number(-4 * N) + (class_number(-N) if N % 4 == 3 else 0)
    g_plus = sp.Rational(2 * g - 2 - fixed, 4) + 1
    if g_plus.q != 1 or e2 % 2 or e3 % 2 or cusps % 2:
        raise Refuse(f"Fricke quotient data not integral for N={N}: g+={g_plus}, e2={e2}, e3={e3}, c={cusps}")
    orders = sorted([2] * (fixed + e2 // 2) + [3] * (e3 // 2))
    return {"genus": int(g_plus), "elliptic_orders": orders, "cusps": int(cusps // 2),
            "gamma0_data": {"index": int(mu), "e2": int(e2), "e3": int(e3), "cusps": int(cusps), "genus": int(g),
                            "fricke_fixed_points": int(fixed),
                            "class_numbers": {f"h({-4*N})": class_number(-4 * N), f"h({-N})": class_number(-N)}}}


# ---------------------------------------------------------------- C, D, E
def chi_orb(sig):
    return 2 - 2 * sig["genus"] - sum(1 - sp.Rational(1, e) for e in sig["elliptic_orders"]) - sig["cusps"]


def degrees(scheme, sig):
    chi = chi_orb(sig)
    hol = {pt: ex[0] for pt, ex in scheme.items()}  # exponent of the holomorphic (F^1) period
    out = {"chi_orb": chi, "deg_omega_Q": -chi / 2, "deg_omega2_Q": -chi, "holomorphic_exponents": hol}
    for k, weight in (("omega", 1), ("omega2", 2)):
        par = -chi * sp.Rational(weight, 2)
        a_lo = {pt: weight * a for pt, a in hol.items()}                      # residues in [0,1)
        a_hi = {pt: (weight * a - 1 if weight * a != 0 else 0) for pt, a in hol.items()}  # residues in (-1,0]
        out[f"deg_ext_{k}_residues_[0,1)"] = par - sum(a_lo.values())
        out[f"deg_ext_{k}_residues_(-1,0]"] = par - sum(a_hi.values())
    return out


def surface_reading(h01=0, h02=1):
    chiO = 1 - h01 + h02
    e = 12 * chiO          # Noether with K^2 = 0 (elliptic surface, K numerically a multiple of the fibre)
    return {"chi_O": chiO, "euler_number": e, "deg_Delta": e, "ell_surface": sp.Rational(e, 12)}


def formula_0729(scheme, order=2):
    """The 2026-07-29 brief's formula: (sum of all exponents)/order -- shown non-discriminating."""
    return sum(sum(v) for v in scheme.values()) / order


def analyse(name, spec, level=None):
    level = level or spec["level"]
    scheme, nsing, total = riemann_scheme(spec["P"])
    sig_exp = signature_from_exponents(scheme)
    sig_grp = signature_gamma0_plus(level)
    agree = {k: sig_exp[k] == sig_grp[k] for k in ("genus", "elliptic_orders", "cusps")}
    res = {"candidate": name, "level": level,
           "riemann_scheme": {k: [str(x) for x in v] for k, v in scheme.items()},
           "n_singular_points": nsing, "fuchs_sum": str(total),
           "signature_from_exponents": sig_exp, "signature_from_gamma0_plus": sig_grp,
           "signatures_agree": all(agree.values()), "agreement_detail": agree}
    if res["signatures_agree"]:
        d = degrees(scheme, sig_exp)
        res["degrees"] = {k: (str(v) if not isinstance(v, dict) else {p: str(a) for p, a in v.items()}) for k, v in d.items()}
    res["formula_2026_07_29_sum_exponents_over_order"] = str(formula_0729(scheme))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    s7 = analyse("cooper_s7", OPERATORS["cooper_s7"])
    s10 = analyse("cooper_s10", OPERATORS["cooper_s10"])
    surf = {k: str(v) for k, v in surface_reading().items()}
    print(f"cooper_s7: singular points {list(s7['riemann_scheme'])} (n={s7['n_singular_points']}), Fuchs sum {s7['fuchs_sum']}")
    print(f"  signature from exponents {s7['signature_from_exponents']}  | from Gamma_0(7)+ {{genus,orders,cusps}} = "
          f"{ {k: s7['signature_from_gamma0_plus'][k] for k in ('genus','elliptic_orders','cusps')} }  agree={s7['signatures_agree']}")
    if s7["signatures_agree"]:
        d = s7["degrees"]
        print(f"  chi_orb {d['chi_orb']}; deg omega {d['deg_omega_Q']}, deg omega^2 {d['deg_omega2_Q']} (Q-degrees); "
              f"Deligne ext omega^2: {d['deg_ext_omega2_residues_[0,1)']} ([0,1)) / {d['deg_ext_omega2_residues_(-1,0]']} ((-1,0])")
    print(f"  07-29 formula (sum exp)/2 = {s7['formula_2026_07_29_sum_exponents_over_order']} ; same formula on cooper_s10 = "
          f"{s10['formula_2026_07_29_sum_exponents_over_order']}  (non-discriminating)")
    print(f"surface reading: chi(O_K3) = {surf['chi_O']}, deg Delta = {surf['deg_Delta']}, ell_surface = {surf['ell_surface']}")
    finding = ("ell = 2 is reproduced ONLY by the elliptic-surface reading (ell = chi(O_K3)); every family-level "
               "reading gives 1/3, 2/3, 0 or 1. F6 disclosure to T0; ledger not edited.")
    print("FINDING:", finding)
    ok = s7["signatures_agree"]
    if a.emit and ok:
        cert = {"checker": "checkers/check_TW0_hodge_degree_orbifold.py",
                "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "work_package": "WP-TW0 re-examination (ledger item 6)",
                "tier": "B (exact exponent/orbifold arithmetic from the Tier-A operator tuple; framework identification of omega^2 with the K3 Hodge line bundle via Doran Thm 5.13, read and pinned)",
                "result": {"cooper_s7": s7, "cooper_s10_as_control": s10, "surface_reading": surf, "finding": finding},
                "not_claimed": [
                    "any Kodaira fibre type at any point (ledger items 3 and 10): exponent language only",
                    "that ell = 2 is wrong: it is correct as chi(O) of any elliptic K3 with section; what is not reproduced is a FAMILY-level Hodge-bundle degree of 2",
                    "which reading WP-TW1 requires: that is the T0 question raised in the brief",
                    "anything about cooper_s10's geometry beyond its use as a discriminating control here",
                    "any physical statement (ledger item 4)"],
                "generated_by": "Claude (Fable 5.1), Stream 2, 2026-10-07", "verified_by": "checkers/test_TW0_hodge_degree_orbifold_controls.py", "reviewed_by": "N"}
        CERT.write_text(json.dumps(cert, indent=2) + "\n")
        print("wrote", CERT)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
