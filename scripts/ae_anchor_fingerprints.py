#!/usr/bin/env python3
"""
AE-1 — Anchor fingerprint library for Stream 2 AutoEvolve.

"Training" on Cooper s7, s10, S22 (Apery zeta(3)) and controls (S21/A005258, S12).
Extracts exact-rational invariants that serve as the fitness answer key:
  * minimal generating-function ODE order/degree and coefficients,
  * mirror-map q coefficients (Frobenius log on minimal operator),
  * singular loci from the leading ODE polynomial,
  * C3b symmetric-square root verdict via checkers/check_C3b_symsqrt.py.

All arithmetic is exact (Fraction / SymPy Rational). No floats in gate paths.
"""

import hashlib
import json
import math
import os
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(REPO_ROOT))

from autoresearch_v2_pool import POOL, OEIS_FIRST_TERMS, verify_terms
from autoresearch_v2_phase_a_scan import classify
from autoresearch_v2_phase_b_all_gates import (
    find_ode_with_coeffs, theta_form, mum_check, frobenius_log_coeffs, mirror_q
)
from checkers import check_C3b_symsqrt

OUT_DIR = REPO_ROOT / "data" / "autoresearch_v2"
OUT_DIR.mkdir(parents=True, exist_ok=True)
CERT_DIR = REPO_ROOT / "data" / "certificates" / "ae"
CERT_DIR.mkdir(parents=True, exist_ok=True)

NMAX = 110
N_MIRROR = 31  # plan requires 31 coefficients
ANCHOR_IDS = ["cooper_s7", "cooper_s10", "apery_zeta3"]
CONTROL_IDS = ["apery_zeta2_s21", "s12_v1_primary"]  # expected elliptic and false-positive controls


def leading_coefficient_roots(rho, delta, coeffs):
    """
    The ODE is sum_{j=0}^{rho} sum_{m=0}^{delta} a_{j,m} z^m D^j y = 0.
    Leading D^rho coefficient is sum_m a_{rho,m} z^m.
    Return rational roots and the factorization string.
    """
    z = sp.Symbol("z")
    lead = sum(int(coeffs[rho * (delta + 1) + m]) * z ** m for m in range(delta + 1))
    lead_poly = sp.Poly(lead, z)
    fac = sp.factor(lead_poly.as_expr())
    # sp.roots returns multiplicities; we want unique rational roots
    roots = sorted(sp.roots(lead_poly, z, filter="Q").keys(), key=lambda r: (sp.denom(r), sp.numer(r)))
    return [str(r) for r in roots], str(fac)


def q_coeffs_are_integral(q):
    return all(Fraction(str(x)).denominator == 1 for x in q)


def mirror_fingerprint(cid, u):
    """Return q2, integrality, and full q-coeffs from the minimal ODE."""
    ode = find_ode_with_coeffs(u, NMAX)
    if ode is None:
        return None
    rho, delta = ode["rho"], ode["delta"]
    G, s = theta_form(rho, delta, ode["coeffs"])
    is_mum, chi = mum_check(G, rho)
    if not is_mum:
        return {
            "ode_order": rho,
            "ode_degree": delta,
            "mum": False,
            "q_coeffs": None,
            "q2": None,
            "integral": False,
        }
    # Frobenius log solution needs series with u[0]=1 for MUM normal form.
    # The theta_form validation implicitly uses u starting at n=1 scaled by z^s;
    # for mirror map at MUM, use the standard y0 = sum u_n z^n with u_0 = 1.
    # If s > 0, shift the sequence: effective series is z^s * sum u_n z^n, so
    # the holomorphic solution starts with u[s] as the new constant term. We
    # scale by u[s] to enforce MUM normalisation g_0 = 1.
    if s > 1:
        # This path should not hit for the anchors, but document it honestly.
        scale = u[s]
        g = [Fraction(x, scale) for x in u[s:]]
    else:
        g = [Fraction(x) for x in u]
    c = frobenius_log_coeffs(G, g, N_MIRROR)
    q = mirror_q(g, c, N_MIRROR)
    return {
        "ode_order": rho,
        "ode_degree": delta,
        "mum": True,
        "q_coeffs": [str(x) for x in q[:N_MIRROR]],
        "q2": str(q[1]) if len(q) > 1 else None,
        "integral": q_coeffs_are_integral(q[:N_MIRROR]),
    }


def run_c3b(cid):
    """Run the constructive C3b checker and return the relevant fields."""
    refs_path = REPO_ROOT / "refs" / "recurrences_v1.json"
    result, code = check_C3b_symsqrt.run_check(refs_path, cid, n_fit=26, n_val=60, deg=2)
    # Write the certificate for audit trail.
    cert_path = CERT_DIR / f"C3b_symsqrt_{cid}.json"
    result["provenance"] = (
        "Generated-by: scripts/ae_anchor_fingerprints.py | "
        "Verified-by: checkers/check_C3b_symsqrt.py | Reviewed-by: pending T0"
    )
    with open(cert_path, "w") as f:
        json.dump(result, f, indent=2, sort_keys=True, default=str)
    return {
        "verdict": result.get("verdict"),
        "partner_recurrence": result.get("partner_L2", {}).get("recurrence"),
        "partner_first_terms": result.get("partner_L2", {}).get("first_terms"),
        "operator_identity": result.get("validation", {}).get("sym2_operator_identity_L3_eq_Sym2L2"),
        "certificate": str(cert_path.relative_to(REPO_ROOT)),
    }


def fingerprint(cid):
    """Build the full fingerprint record for one candidate/control."""
    terms = POOL[cid](NMAX)
    cls = classify(cid, terms, NMAX)
    rec = {
        "id": cid,
        "oeis": OEIS_FIRST_TERMS.get(cid, (None, []))[0],
        "first_terms": terms[:8],
        "shift": cls.get("shift"),
        "ode": cls.get("ode"),
        "geometry_by_ode": cls.get("geometry_by_ode"),
    }

    # Minimal ODE + mirror map
    mirror = mirror_fingerprint(cid, terms)
    if mirror:
        rec["mirror"] = mirror
        if cls.get("ode"):
            roots, fac = leading_coefficient_roots(
                cls["ode"]["ode_order"], cls["ode"]["ode_degree"], find_ode_with_coeffs(terms, NMAX)["coeffs"]
            )
            rec["singular_loci"] = {
                "rational_roots": roots,
                "leading_polynomial_factored": fac,
            }
    else:
        rec["mirror"] = None
        rec["singular_loci"] = None

    # C3b only for order-3 sequences (the checker refuses otherwise)
    if cls.get("ode") and cls["ode"].get("ode_order") == 3:
        rec["c3b"] = run_c3b(cid)
    else:
        rec["c3b"] = {"verdict": "SKIPPED_NOT_ORDER3"}

    return rec


def main():
    fails = verify_terms()
    if fails:
        print("FATAL: pool term generators disagree with OEIS reference:", fails)
        sys.exit(1)

    out = {
        "nmax": NMAX,
        "n_mirror": N_MIRROR,
        "anchors": ANCHOR_IDS,
        "controls": CONTROL_IDS,
        "fingerprints": {},
    }

    for cid in ANCHOR_IDS + CONTROL_IDS:
        print(f"[AE-1] fingerprinting {cid} ...")
        out["fingerprints"][cid] = fingerprint(cid)

    out_path = OUT_DIR / "ae_anchor_fingerprints.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str, sort_keys=True)

    print(f"\n[AE-1] wrote {out_path}")
    print("[AE-1] certificates under", CERT_DIR.relative_to(REPO_ROOT))
    return out


if __name__ == "__main__":
    main()
