#!/usr/bin/env python3
"""
check_external_review_fable_2026_09_21.py -- clause-by-clause audit of the external
"K3 Selection Review" (Fable 5.1, dated 2026-09-21), recorded verbatim at
docs/literature/external_reviews/FABLE51_K3_SELECTION_REVIEW_2026_09_21.md.

Standing practice (feedback_workflow_pattern_build_verify_fix): an externally supplied
review is passed in as UNVERIFIED and scored clause by clause against certificates and
exact recomputation. Nothing in the review becomes evidence by being recorded; only the
clauses this checker CONFIRMS may be cited, and only with this certificate as the source.

What is scored (Stream 2 scope only -- the review's Lambda, M24, A4, Kummer, quartic, r,
n_s, delta_CP, Papers 10-12 conflict claims, X3/X4 Weierstrass fibre tables, Hurwitz-order
observation, laboratory experiments and TDA sections have no artifact in this repository
and are NOT scored; they are listed in the certificate as out of scope):

  F1  s7 singular loci {0, 1/27, -1, oo}         leading symbol 1 - 2a z + c z^2 from the
  F2  s10 singular loci {0, -1/4, 1/16, oo}      register's Cooper params (exact, sympy)
  F3  L3 Riemann scheme: interior {0,1/2,1}, oo {2/3,1,4/3} (s7) / {3/4,1,5/4} (s10)
                                                 L3_RIEMANN_SCHEME.json
  F4  L2 exponents at oo {1/3,2/3} (s7), {3/8,5/8} (s10) via {2a, a+b, 2b} -- exact
  F5  stabiliser orders [2,2,3] (s7), [2,2,4] (s10)   ELLIPTIC_POINTS_ARE_CM.json
  F6  Gauss-Bonnet: (2,2,3) matches Gamma_0(7)+ (index 8, /2, 1 cusp); (2,2,4) matches
      Gamma_0(10)* (index 18, /4, 1 cusp) and NOT Gamma_0(10)+10 -- exact Fractions,
      index N prod(1+1/p), cusps sum_{d|N} phi(gcd(d,N/d))
  F7  W_7 fixed points: tau = i/sqrt7 -> v=(1,-1,0), v^2=-2, T=<2>+<14>, D=-28, h=1;
      second point -> v = +-(-2,4,1), v^2=-2, T=[[2,1],[1,4]], D=-7, h=1
                                                 CM_POINTS_RHO20.json + exact class numbers
  F8  count of W_7 fixed points = h(-28) + h(-7) = number of order-2 loci of s7
  F9  W_10 Fricke point tau = i/sqrt10 -> T=<2>+<20>, D=-40, h=2   CM_POINTS_RHO20.json
  F10 class numbers h(-3)=h(-4)=h(-7)=h(-8)=h(-28)=1, h(-40)=2, h(-23)=3 with the
      -23 forms (1,1,6),(2,1,3),(2,-1,3) -- exact reduced-form enumeration
  F11 lattice convergence: the review's X3 lattice A2=(1,1,1), D=-3, is the z=oo member
      of cooper_s7; its X4 lattice <2>+<2>=(1,0,1), D=-4, is the z=oo member of cooper_s10
                                                 CM_POINTS_RHO20.json
  F12 L3 = Sym^2(L2) with L2 exhibited, s7 and s10   C3b_symsqrt_*.json (identity proven)

Findings recorded in band (not failures of the review's own tables):
  N1  the review repeats the reviewed spec's labels "1/27 (conifold), -1 (Fricke)"; per
      the certificate the W_7 fixed point tau = i/sqrt7 sits at z = 1/27 and the D=-7
      point at z = -1. Also "conifold" is a Kodaira-type reading, which ledger item 3
      forbids for this family (order-2 elliptic point, E-008/E-009).
  N2  the review's "h(-4N) + h(-N) fixed points" rule is scored at N=7 only; for s10 the
      review itself names the full Atkin-Lehner group, where W_10 is one of three.

Exit 0 when every scored clause is CONFIRMED, 1 otherwise. Controls:
checkers/test_external_review_fable_controls.py.

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: checkers/test_external_review_fable_controls.py | Reviewed-by: N
"""
import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import sympy

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from render_status_table import parse_register, derive_refs_key  # noqa: E402

AUDIT_DATE = "2026-09-27"
REVIEW = "docs/literature/external_reviews/FABLE51_K3_SELECTION_REVIEW_2026_09_21.md"


# ---------------------------------------------------------------------------
# exact helpers
# ---------------------------------------------------------------------------
def reduced_primitive_forms(D):
    """All reduced primitive positive-definite binary forms (a,b,c) of discriminant D<0."""
    assert D < 0
    out = []
    a = 1
    while 3 * a * a <= -D:
        for b in range(-a + 1, a + 1):
            num = b * b - D
            if num % (4 * a):
                continue
            c = num // (4 * a)
            if c < a:
                continue
            if a == c and b < 0:
                continue
            if math.gcd(math.gcd(a, abs(b)), c) != 1:
                continue
            out.append((a, b, c))
        a += 1
    return sorted(out)


def class_number(D):
    return len(reduced_primitive_forms(D))


def gamma0_index(N):
    idx = Fraction(N)
    for p in sympy.primefactors(N):
        idx *= Fraction(p + 1, p)
    return idx


def gamma0_cusps(N):
    return sum(sympy.totient(math.gcd(d, N // d)) for d in sympy.divisors(N))


def gauss_bonnet_matches(N, quotient_order, elliptic_orders):
    """Exact orbifold Gauss-Bonnet for a genus-0 quotient of Gamma_0(N) by an
    Atkin-Lehner subgroup of the given order, acting freely on cusps."""
    area = gamma0_index(N) / 6 / quotient_order            # area / 2pi
    cusps = Fraction(int(gamma0_cusps(N)), quotient_order)
    if cusps.denominator != 1:
        return False, {"reason": "cusp count not divisible by quotient order"}
    rhs = Fraction(-2) + sum(1 - Fraction(1, e) for e in elliptic_orders) + cusps
    return area == rhs, {"area_over_2pi": str(area), "orbifold_euler_rhs": str(rhs),
                         "cusps_after_quotient": str(cusps)}


def cooper_loci(params):
    a, b, c, d = params
    z = sympy.Symbol("z")
    lead = 1 - 2 * a * z + c * z**2
    roots = sorted(sympy.roots(sympy.Poly(lead, z)).keys(), key=lambda r: float(r))
    return ["0"] + [str(r) for r in roots] + ["oo"], str(sympy.factor(lead))


def reduce_form(a, b, c):
    """Gauss reduction of a positive-definite form (a,b,c)."""
    while True:
        if c < a:
            a, b, c = c, -b, a
            continue
        if not (-a < b <= a):
            k = (a - b) // (2 * a)
            b2 = b + 2 * a * k
            c = a * k * k + b * k + c
            b = b2
            continue
        if a == c and b < 0:
            b = -b
            continue
        return (a, b, c)


# ---------------------------------------------------------------------------
# clauses
# ---------------------------------------------------------------------------
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(criteria_file, refs_file, certs_dir, review_file):
    certs_dir = Path(certs_dir)
    text = Path(criteria_file).read_text()
    refs = json.loads(Path(refs_file).read_text())["sequences"]
    rows = {r["id"]: r for r in parse_register(text) if not r["dropped"]}
    keys = {rid: derive_refs_key(r["params"], refs) for rid, r in rows.items()}
    params = {keys[rid]: r["params"] for rid, r in rows.items()}

    cm = json.loads((certs_dir / "CM_POINTS_RHO20.json").read_text())
    ell = json.loads((certs_dir / "ELLIPTIC_POINTS_ARE_CM.json").read_text())
    rs = json.loads((certs_dir / "L3_RIEMANN_SCHEME.json").read_text())
    scheme = {r["operator"]: r["riemann_scheme"] for r in rs["results"]}
    c3 = {k: json.loads((certs_dir / f"C3b_symsqrt_{k}.json").read_text())
          for k in ("cooper_s7", "cooper_s10")}

    clauses = []

    def clause(cid, statement, confirmed, evidence, source):
        clauses.append({"id": cid, "review_claim": statement,
                        "verdict": "CONFIRMED" if confirmed else "NOT_CONFIRMED",
                        "evidence": evidence, "source": source})
        return confirmed

    # F1 / F2
    for cid, key, expect in (("F1", "cooper_s7", ["0", "-1", "1/27", "oo"]),
                             ("F2", "cooper_s10", ["0", "-1/4", "1/16", "oo"])):
        loci, lead = cooper_loci(params[key])
        clause(cid, f"{key} singular loci are {expect}", loci == expect,
               {"cooper_params": list(params[key]), "leading_symbol": lead, "loci": loci},
               "register params (K3_CRITERIA sec. 1, matched to refs) -> exact sympy")

    # F3
    exp_scheme = {"cooper_s7": {"0": ["0", "0", "0"], "-1": ["0", "1/2", "1"],
                                "1/27": ["0", "1/2", "1"], "oo": ["2/3", "1", "4/3"]},
                  "cooper_s10": {"0": ["0", "0", "0"], "-1/4": ["0", "1/2", "1"],
                                 "1/16": ["0", "1/2", "1"], "oo": ["3/4", "1", "5/4"]}}
    clause("F3", "L3 Riemann schemes as tabulated (MUM at 0; {0,1/2,1} interior; oo as stated)",
           all(scheme[k] == exp_scheme[k] for k in exp_scheme),
           {k: scheme[k] for k in exp_scheme}, "L3_RIEMANN_SCHEME.json")

    # F4
    l2 = {}
    ok4 = True
    for k, expect in (("cooper_s7", ("1/3", "2/3")), ("cooper_s10", ("3/8", "5/8"))):
        e = sorted(Fraction(x) for x in scheme[k]["oo"])
        alpha, beta = e[0] / 2, e[2] / 2
        good = (alpha + beta == e[1]) and (str(alpha), str(beta)) == expect
        l2[k] = {"L3_oo": [str(x) for x in e], "alpha": str(alpha), "beta": str(beta),
                 "middle_equals_alpha_plus_beta": alpha + beta == e[1],
                 "difference": str(beta - alpha)}
        ok4 &= good
    clause("F4", "L2 exponents at oo are {1/3,2/3} (s7) and {3/8,5/8} (s10), read through {2a, a+b, 2b}",
           ok4, l2, "F3 + exact arithmetic")

    # F5
    orders = {k: sorted(l["stabilizer_order_exact"] for l in ell["families"][k]["loci"])
              for k in ("cooper_s7", "cooper_s10")}
    clause("F5", "stabiliser orders [2,2,3] (s7) and [2,2,4] (s10)",
           orders == {"cooper_s7": [2, 2, 3], "cooper_s10": [2, 2, 4]}, orders,
           "ELLIPTIC_POINTS_ARE_CM.json")

    # F6
    m7, e7 = gauss_bonnet_matches(7, 2, orders["cooper_s7"])
    m10, e10 = gauss_bonnet_matches(10, 4, orders["cooper_s10"])
    m10w, e10w = gauss_bonnet_matches(10, 2, orders["cooper_s10"])
    clause("F6", "Gauss-Bonnet: (2,2,3) <-> Gamma_0(7)+ (index 8, halved); (2,2,4) <-> Gamma_0(10)* "
                 "(index 18, quartered), and NOT Gamma_0(10)+10 (halved)",
           m7 and m10 and not m10w,
           {"Gamma_0(7)+": e7, "Gamma_0(10)*": e10, "Gamma_0(10)+10_must_fail": e10w,
            "index_7": str(gamma0_index(7)), "index_10": str(gamma0_index(10)),
            "cusps_7": int(gamma0_cusps(7)), "cusps_10": int(gamma0_cusps(10))},
           "exact Fractions; orders from F5")

    # F7
    hits7 = {loc: h[0] for loc, h in cm["families"]["cooper_s7"]["locus_hits"].items()}
    fr = hits7.get("1/27", {})
    other = hits7.get("-1", {})
    fricke_ok = (fr.get("tau", {}).get("re") == "0" and fr.get("tau", {}).get("im_squared") == "1/7"
                 and fr.get("v") == [1, -1, 0] and fr.get("minus_v2") == 2
                 and fr.get("T_X_reduced_form_abc") == [1, 0, 7] and fr.get("D") == -28
                 and class_number(-28) == 1)
    v_other = other.get("v")
    other_ok = (v_other in ([-2, 4, 1], [2, -4, 1]) and other.get("minus_v2") == 2
                and other.get("T_X_reduced_form_abc") == [1, 1, 2] and other.get("D") == -7
                and class_number(-7) == 1)
    clause("F7", "W_7 fixed points: tau=i/sqrt7 -> v=(1,-1,0), v^2=-2, T=<2>+<14>, D=-28, h=1; "
                 "the other -> v=+-(-2,4,1), v^2=-2, T=[[2,1],[1,4]], D=-7, h=1",
           fricke_ok and other_ok,
           {"z=1/27": {k: fr.get(k) for k in ("v", "minus_v2", "T_X_reduced_form_abc", "D", "tau")},
            "z=-1": {k: other.get(k) for k in ("v", "minus_v2", "T_X_reduced_form_abc", "D", "tau")},
            "h(-28)": class_number(-28), "h(-7)": class_number(-7)},
           "CM_POINTS_RHO20.json locus_hits + exact class numbers")

    # F8
    n_order2 = sum(1 for l in ell["families"]["cooper_s7"]["loci"] if l["stabilizer_order_exact"] == 2)
    d_order2 = sorted(l["D0"] for l in ell["families"]["cooper_s7"]["loci"] if l["stabilizer_order_exact"] == 2)
    clause("F8", "number of W_7 fixed points = h(-28) + h(-7) = 2 = the order-2 loci of s7, with D in {-28, -7}",
           class_number(-28) + class_number(-7) == n_order2 == 2 and d_order2 == [-28, -7],
           {"h(-28)+h(-7)": class_number(-28) + class_number(-7), "order2_loci": n_order2,
            "their_D0": d_order2}, "ELLIPTIC_POINTS_ARE_CM.json + exact class numbers")

    # F9
    hits10 = {loc: h[0] for loc, h in cm["families"]["cooper_s10"]["locus_hits"].items()}
    f10 = hits10.get("1/16", {})
    clause("F9", "W_10 Fricke point tau=i/sqrt10 -> v=(1,-1,0), T=<2>+<20>, D=-40, h=2",
           (f10.get("tau", {}).get("re") == "0" and f10.get("tau", {}).get("im_squared") == "1/10"
            and f10.get("v") == [1, -1, 0] and f10.get("T_X_reduced_form_abc") == [1, 0, 10]
            and f10.get("D") == -40 and class_number(-40) == 2),
           {"z=1/16": {k: f10.get(k) for k in ("v", "minus_v2", "T_X_reduced_form_abc", "D", "tau")},
            "h(-40)": class_number(-40),
            "advisory": cm["families"]["cooper_s10"]["advisory"]},
           "CM_POINTS_RHO20.json (s10 ADVISORY: lattice cert DRAFT) + exact class number")

    # F10
    expect_h = {-3: 1, -4: 1, -7: 1, -8: 1, -28: 1, -40: 2, -23: 3}
    got_h = {D: class_number(D) for D in expect_h}
    forms23 = reduced_primitive_forms(-23)
    clause("F10", "class numbers h(-3)=h(-4)=h(-7)=h(-8)=h(-28)=1, h(-40)=2, h(-23)=3; "
                  "the -23 forms are (1,1,6), (2,1,3), (2,-1,3)",
           got_h == expect_h and forms23 == [(1, 1, 6), (2, -1, 3), (2, 1, 3)],
           {"h": {str(k): v for k, v in got_h.items()}, "forms_-23": forms23},
           "exact reduced-form enumeration (this checker)")

    # F11
    inf7 = hits7.get("infinity", {})
    inf10 = hits10.get("infinity", {})
    clause("F11", "the review's X3 lattice A2 (D=-3) is a member of the s7 family (z=oo) and its X4 "
                  "lattice <2>+<2> (D=-4) a member of the s10 family (z=oo) -- lattice statement only",
           (inf7.get("D") == -3 and inf7.get("T_X_reduced_form_abc") == [1, 1, 1]
            and inf10.get("D") == -4 and inf10.get("T_X_reduced_form_abc") == [1, 0, 1]),
           {"s7_z=oo": {k: inf7.get(k) for k in ("D", "T_X_reduced_form_abc", "v")},
            "s10_z=oo": {k: inf10.get(k) for k in ("D", "T_X_reduced_form_abc", "v")},
            "identification_with_named_surfaces": "Shioda-Inose (singular K3 <-> T), Tier L, cited by "
                                                  "the review, NOT pinned in this repo"},
           "CM_POINTS_RHO20.json locus_hits")

    # F12
    clause("F12", "L3 = Sym^2(L2) for an exhibited L2, s7 and s10, with no condition on (a,b,c,d)",
           all(c3[k]["validation"]["sym2_operator_identity_L3_eq_Sym2L2"] is True for k in c3),
           {k: c3[k]["verdict"] for k in c3}, "C3b_symsqrt_cooper_s7/s10.json")

    all_ok = all(c["verdict"] == "CONFIRMED" for c in clauses)
    return {
        "certificate": "EXTERNAL_REVIEW_FABLE_2026_09_21_AUDIT",
        "checker": "checkers/check_external_review_fable_2026_09_21.py",
        "checker_version": "1.0.0",
        "date": AUDIT_DATE,
        "status": "RECORD -- audit of an EXTERNAL review; nothing is adopted, scored or ranked by this "
                  "certificate. CONFIRMED means: the clause agrees with a certificate on main or with an exact "
                  "recomputation here. The rho = 20 cut stays read narrowly (T0 D7'): no selector between CM "
                  "points is adopted; cooper_s10 is ADVISORY (lattice certificate DRAFT).",
        "review": {"file": REVIEW, "sha256": sha(review_file),
                   "source": "https://claude.ai/artifact/SFDSuPbfKD8SB4mVQhAErg (Claude Docs id "
                             "cc708cbe-058d-4c7e-9903-02b9af1e1d5d, rev 21)", "author": "Fable 5.1",
                   "dated": "2026-09-21"},
        "tier": "B",
        "tier_reason": "F1, F2, F4, F6, F10 exact here; F3, F5, F7, F8, F9, F11, F12 rest on Tier B certificates "
                       "(numeric recognition of z, Dolgachev/Doran framework identification).",
        "clauses": clauses,
        "all_scored_clauses_confirmed": all_ok,
        "findings_in_band": {
            "N1": "The review keeps the reviewed spec's labels '1/27 (conifold), -1 (Fricke)'. Per "
                  "CM_POINTS_RHO20.json the W_7 fixed point tau = i/sqrt7 is at z = 1/27 and the D = -7 "
                  "point at z = -1; and 'conifold' is a Kodaira-type reading that ledger item 3 forbids for "
                  "this family (both are order-2 elliptic points, E-008/E-009).",
            "N2": "The 'h(-4N)+h(-N) fixed points' rule is scored at N = 7 only (F8). For s10 the review "
                  "itself names Gamma_0(10)* where W_10 is one of three involutions.",
            "N3": "The review's 'name the selector' point is the content of D7' read narrowly: C6 lists "
                  "members; no quantity to extremise among them has been adopted. A selection principle "
                  "(discriminant, height, Fricke point) needs its own T0 text.",
        },
        "out_of_scope_not_scored": [
            "Lambda / dark-energy arithmetic (A-DE renunciation; ledger item 4)",
            "M24 branching, Mukai, GHV/GTVW symmetry-group statements",
            "Kummer node count, quartic homogeneity, spec's r / n_s / delta_CP / 21-cm / TDA rows",
            "conflicts with Papers 10-12 (LeanMaster theorems exist by name: smallest_black_hole, "
            "tau_minimal, discriminant_gap, smallest_black_hole_index, immortal_m1, "
            "literal_lock_fails_at_2A -- their statements were read via the LeanMaster index, not re-proved here)",
            "X3 / X4 Inose-Weierstrass fibre tables and NS lattices (no model in this repo; a Kodaira "
            "reading of an explicit Weierstrass model is not the E-007 category error, but nothing here "
            "checks it -> Stream 1 Lean target)",
            "Hurwitz-order / D4 torus observation", "laboratory experiments E1-E4", "TDA proposals",
            "'neither s7 nor s10 is Sym^2 of a Zagier-sporadic operator' (consistent with "
            "briefs/STREAM2_TO_STREAM3_C3_BRANCH_REPLY_2026_09_21.md; not recomputed here)",
        ],
        "inputs": {"sha256": {
            "refs/recurrences_v1.json": sha(refs_file),
            "data/certificates/CM_POINTS_RHO20.json": sha(certs_dir / "CM_POINTS_RHO20.json"),
            "data/certificates/ELLIPTIC_POINTS_ARE_CM.json": sha(certs_dir / "ELLIPTIC_POINTS_ARE_CM.json"),
            "data/certificates/L3_RIEMANN_SCHEME.json": sha(certs_dir / "L3_RIEMANN_SCHEME.json"),
            "data/certificates/C3b_symsqrt_cooper_s7.json": sha(certs_dir / "C3b_symsqrt_cooper_s7.json"),
            "data/certificates/C3b_symsqrt_cooper_s10.json": sha(certs_dir / "C3b_symsqrt_cooper_s10.json"),
        }},
        "not_claimed": [
            "that any CM point, surface or family is preferred (D7' narrow reading)",
            "that X3 or X4 as named surfaces are certified here: only their transcendental lattices are matched",
            "any physical reading of any clause (VISION sec. 1.3; ledger item 4)",
            "that the unscored sections of the review are true or false",
        ],
        "controls": "checkers/test_external_review_fable_controls.py",
        "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: "
                      "checkers/test_external_review_fable_controls.py | Reviewed-by: N",
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--criteria-file", default=REPO / "K3_CRITERIA.md", type=Path)
    ap.add_argument("--refs-file", default=REPO / "refs" / "recurrences_v1.json", type=Path)
    ap.add_argument("--certs-dir", default=REPO / "data" / "certificates", type=Path)
    ap.add_argument("--review-file", default=REPO / REVIEW, type=Path)
    ap.add_argument("--out", default=None, type=Path,
                    help="certificate path (default data/certificates/EXTERNAL_REVIEW_FABLE_2026_09_21_AUDIT.json)")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args(argv)
    cert = run(a.criteria_file, a.refs_file, a.certs_dir, a.review_file)
    for c in cert["clauses"]:
        print(f"  {c['verdict']:14s} {c['id']:4s} {c['review_claim'][:100]}")
    print("findings:", ", ".join(cert["findings_in_band"]))
    print("all scored clauses confirmed:", cert["all_scored_clauses_confirmed"])
    if not a.no_write:
        out = a.out or (a.certs_dir / "EXTERNAL_REVIEW_FABLE_2026_09_21_AUDIT.json")
        out.write_text(json.dumps(cert, indent=2) + "\n")
        print("wrote", out)
    return 0 if cert["all_scored_clauses_confirmed"] else 1


if __name__ == "__main__":
    sys.exit(main())
