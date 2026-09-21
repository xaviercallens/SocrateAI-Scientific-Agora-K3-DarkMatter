#!/usr/bin/env python3
"""
check_elliptic_points_are_CM.py (A1) -- the singular loci of the s7 / s10 operators are
elliptic points of the modular curve, and an elliptic point is FORCED to be a CM point.

STATUS: RECORD, NOT A GATE.  Lattice / modular arithmetic, Tier B at best, no physical
reading.  The rho = 20 cut is adopted (T0 D7', 2026-09-21), read narrowly; nothing is scored.  cooper_s10 output is
ADVISORY (its lattice certificate is DRAFT).

THE ARGUMENT (elementary; the checker exhibits each ingredient exactly)
-----------------------------------------------------------------------
If a real 2x2 integer matrix M = [[a, b], [c, d]], not a scalar, fixes tau in the upper half
plane, then  c tau^2 + (d - a) tau - b = 0  is an integer quadratic satisfied by tau: tau is
imaginary quadratic.  In the lattice picture of CM_POINTS_RHO20.json (T_n = U + <2n>,
omega = (1, -n tau^2, tau)), B(v, omega) = y - n x tau^2 + 2 n z tau, so the integer vector
proportional to (x, y, z) = (c/n, b, (a - d)/(2n)) is orthogonal to the period.
Hence "the singular loci are rho = 20 points" (P2's finding) is NOT an independent
observation once the loci are known to be elliptic points of X_0(n)+ / X_0(n)*:
THE AGREEMENT IS FORCED, NOT CORROBORATION.  What is not forced, and is checked here:
  (1) that each locus in P2's table really has a non-trivial stabilizer in the group,
  (3) that the stabilizer order equals the lcm of the denominators of the L3 local
      exponents at that locus (data/certificates/L3_RIEMANN_SCHEME.json),
  (4) that NO other row of the table has a non-trivial stabilizer.
And one INPUT-CONSISTENCY check, which is NOT in that list because it is close to
tautological by construction (review finding, 2026-09-21):
  (2) that the stabilizer's quadratic is proportional to the lattice vector's quadratic.
      Path 1 builds each stabilizer element from P2's tau, and P2's tau is computed from v,
      so (2) can fire only if the P2 record is internally inconsistent (tau field versus v
      field; control S1 tampers exactly that).  It guards the input; it is no evidence.

OBJECTS.  "Singular" here refers to a singular point of the differential operator L3 on
the z-line, and to a point of the upper half plane with non-trivial stabilizer in the
group.  Nothing is said about fibres of any fibration (CLAUDE.md ledger item 3), and
nothing about singularities of a surface.

GROUP.  Gamma_0(n)* = all Atkin-Lehner normalizers: integer matrices [[Q a, b], [n c, Q d]]
of determinant Q, Q an exact divisor of n (Q | n, gcd(Q, n/Q) = 1).  For n = 7 this is
Gamma_0(7)+.  The exact divisors are computed from n; n comes from the P2 certificate.

SEARCH (exact, stated box).  tau = re + i sqrt(im2) with re, im2 rational gives the primitive
integer quadratic (P, R, S) of tau.  A matrix fixes tau iff (c, d - a, -b) = k (P, R, S) for an
integer k != 0 (P, R, S primitive and tau of degree 2).  Path 1 enumerates (k, a) with all
four entries in [-BOX, BOX], BOX = 40 -- this IS the full 4-dimensional box, cut down by an
exact linear condition.  Path 2 is an independent brute force over all four entries in
[-BOX2, BOX2], BOX2 = 9, testing "M tau = tau" in exact Q(sqrt(-im2)) arithmetic; both
paths must agree on their common box.  Order in PSL_2(R): least m with M^m scalar (exact
integer matrix powers).

EXACT COMPLETE DETERMINATION (unbounded; path 3).  A non-scalar M in the group fixing tau in
H has t^2 < 4 det (t = a + d), and Q | a, Q | d make t^2/det an integer, so t^2 = m Q with m in {0,1,2,3}, and disc(fixed quadratic) = t^2 - 4 det = -(4-m) Q
= k^2 D0, D0 the discriminant of tau's primitive quadratic.  For each exact divisor Q and each
m this leaves at most the candidates k = +-sqrt((4-m) Q / -D0), t = +-sqrt(m Q),
a = (t - k R)/2, d = t - a, c = k P, b = -k S, each tested for membership.  That is a finite
exact list of ALL stabilizer elements, with no box.  The checker requires path 3 to agree
with path 1 (and path 1 with path 2 on the small box); "trivial stabilizer" is therefore an
exact statement for every row, not a bounded one.
"""
import hashlib
import json
import pathlib
import sys
from fractions import Fraction as F
from math import gcd, isqrt

ROOT = pathlib.Path(__file__).resolve().parents[1]
CERTS = ROOT / "data" / "certificates"
P2 = CERTS / "CM_POINTS_RHO20.json"
SCHEME = CERTS / "L3_RIEMANN_SCHEME.json"
OUT = CERTS / "ELLIPTIC_POINTS_ARE_CM.json"
BOX, BOX2 = 40, 9
FORCED = ("The agreement between 'singular locus of L3' and 'rho = 20 (CM) point' is FORCED, not "
          "corroboration: a point fixed by a non-scalar integer matrix satisfies an integer quadratic, "
          "so every elliptic point of X_0(n)+ / X_0(n)* is a CM point. It adds no independent support "
          "to either statement.")


class Refusal(Exception):
    def __init__(self, clause, msg=""):
        super().__init__(f"{clause}: {msg}")
        self.clause = clause


def exact_divisors(n):
    return [q for q in range(1, n + 1) if n % q == 0 and gcd(q, n // q) == 1]


def primitive_quadratic(re, im2):
    """(P, R, S), P > 0, gcd 1, with P tau^2 + R tau + S = 0 for tau = re + i sqrt(im2)."""
    if im2 <= 0:
        raise Refusal("tau_not_in_upper_half_plane")
    co = [F(1), -2 * re, re * re + im2]
    L = 1
    for c in co:
        L = L * c.denominator // gcd(L, c.denominator)
    ints = [int(c * L) for c in co]
    g = gcd(gcd(ints[0], ints[1]), ints[2])
    return tuple(i // g for i in ints)


def lattice_quadratic(n, v):
    x, y, z = v
    return (n * x, -2 * n * z, -y)


def proportional(u, w):
    return all(u[i] * w[j] == u[j] * w[i] for i in range(3) for j in range(3)) and any(u) and any(w)


def in_group(M, n, divisors):
    a, b, c, d = M
    det = a * d - b * c
    return det in divisors and c % n == 0 and a % det == 0 and d % det == 0


def mat_mul(X, Y):
    return (X[0] * Y[0] + X[1] * Y[2], X[0] * Y[1] + X[1] * Y[3],
            X[2] * Y[0] + X[3] * Y[2], X[2] * Y[1] + X[3] * Y[3])


def psl_order(M, cap=24):
    X = M
    for m in range(1, cap + 1):
        if X[1] == 0 and X[2] == 0 and X[0] == X[3]:
            return m
        X = mat_mul(X, M)
    return None


def fixes_exact(M, re, im2):
    """M tau = tau in Q(sqrt(-im2)): numbers are (u, w) = u + w*I, I^2 = -im2, tau = (re, 1)."""
    a, b, c, d = M
    num = (a * re + b, F(a))                       # a tau + b
    den = (c * re + d, F(c))                       # c tau + d
    rhs = (re * den[0] - im2 * den[1], re * den[1] + den[0])   # tau * (c tau + d)
    return num == rhs


def canon(M):
    return max(M, tuple(-x for x in M))


def stabilizer_path1(re, im2, n, divisors, box=BOX):
    P, R, S = primitive_quadratic(re, im2)
    found = set()
    for k in range(-box, box + 1):
        if k == 0:
            continue
        c, b = k * P, -k * S
        if abs(c) > box or abs(b) > box:
            continue
        for a in range(-box, box + 1):
            d = a + k * R
            if abs(d) > box:
                continue
            M = (a, b, c, d)
            if in_group(M, n, divisors):
                if not fixes_exact(M, re, im2):
                    raise Refusal("path1_matrix_does_not_fix_tau", str(M))
                found.add(canon(M))
    return found


def stabilizer_path2(re, im2, n, divisors, box=BOX2):
    found = set()
    rng = range(-box, box + 1)
    for c in rng:
        if c % n:
            continue
        for a in rng:
            for d in rng:
                for b in rng:
                    M = (a, b, c, d)
                    if (b or c or a != d) and in_group(M, n, divisors) and fixes_exact(M, re, im2):
                        found.add(canon(M))
    return found


def stabilizer_exact(re, im2, n, divisors):
    """Path 3: ALL non-scalar group elements fixing tau, up to sign; no box."""
    P, R, S = primitive_quadratic(re, im2)
    D0 = R * R - 4 * P * S
    found = set()
    for Q in divisors:
        for m in range(4):
            num = (4 - m) * Q
            if num % (-D0):
                continue
            k0, t0 = isqrt(num // (-D0)), isqrt(m * Q)
            if k0 * k0 != num // (-D0) or t0 * t0 != m * Q:
                continue
            for k in (k0, -k0):
                for t in {t0, -t0}:
                    if (t - k * R) % 2:
                        continue
                    a = (t - k * R) // 2
                    M = (a, -k * S, k * P, t - a)
                    if in_group(M, n, divisors) and M[0] * M[3] - M[1] * M[2] == Q:
                        if not fixes_exact(M, re, im2):
                            raise Refusal("path3_matrix_does_not_fix_tau", str(M))
                        found.add(canon(M))
    return found


def stabilizer(re, im2, n, divisors, box=BOX, cross_check=True):
    P, R, S = primitive_quadratic(re, im2)
    D0 = R * R - 4 * P * S
    s1 = stabilizer_path1(re, im2, n, divisors, box)
    if cross_check:
        b2 = min(BOX2, box)
        s2 = stabilizer_path2(re, im2, n, divisors, b2)
        small = {M for M in s1 if max(abs(x) for x in M) <= b2}
        if s2 != small:
            raise Refusal("two_search_paths_disagree", f"{sorted(s2)} vs {sorted(small)}")
    els = []
    for M in sorted(s1, key=lambda M: (max(abs(x) for x in M), M)):
        a, b, c, d = M
        els.append({"matrix": [[a, b], [c, d]], "det": a * d - b * c, "trace": a + d,
                    "order_in_PSL2": psl_order(M),
                    "fixed_quadratic_c_dminusa_minusb": [c, d - a, -b]})
    order = len(els) + 1
    if els and max(e["order_in_PSL2"] or 0 for e in els) != order:
        # a finite stabilizer in PSL2(R) is cyclic; if the box holds all of it, some element has full order
        raise Refusal("stabilizer_not_cyclic_of_the_counted_order", f"{order} elements, orders {[e['order_in_PSL2'] for e in els]}")
    s3 = stabilizer_exact(re, im2, n, divisors)
    if {M for M in s3 if max(abs(x) for x in M) <= box} != s1:
        raise Refusal("box_search_and_exact_determination_disagree", f"{sorted(s1)} vs {sorted(s3)}")
    return {"primitive_quadratic_of_tau": [P, R, S], "D0": D0, "stabilizer_order_in_box": order,
            "stabilizer_order_exact": len(s3) + 1,
            "elements_up_to_sign": els,
            "scope": f"box: all four entries in [-{box}, {box}]; exact determination (path 3): no box"}


def quadratic_of_algebraic_tau(expr):
    """For a tau given as a sympy algebraic number: refuse unless it is imaginary quadratic.
    If 1, tau, tau^2 are linearly independent over Q, c tau^2 + (d-a) tau - b = 0 forces a
    scalar matrix: NO non-scalar integer matrix fixes tau (exact, no box)."""
    import sympy as sp
    x = sp.symbols("x")
    mpoly = sp.Poly(sp.minimal_polynomial(expr, x), x)
    if mpoly.degree() != 2:
        raise Refusal("tau_not_imaginary_quadratic", f"minimal polynomial degree {mpoly.degree()}: {mpoly.as_expr()}")
    return [int(c) for c in mpoly.all_coeffs()]


def scheme_denominators(operator):
    res = json.loads(SCHEME.read_text())["results"]
    sch = next(r for r in res if r["operator"] == operator)["riemann_scheme"]
    out = {}
    for locus, exps in sch.items():
        L = 1
        for e in exps:
            den = F(e).denominator
            L = L * den // gcd(L, den)
        out["infinity" if locus == "oo" else locus] = {"exponents": exps, "denominator_lcm": L}
    return out


def family(key, fam, divisors=None, box=BOX):
    n = fam["n"]
    divisors = divisors or exact_divisors(n)
    dens = scheme_denominators(key)
    loci, violations = [], []
    for locus, hits in fam["locus_hits"].items():
        for h in hits:
            re, im2 = F(h["tau"]["re"]), F(h["tau"]["im_squared"])
            st = stabilizer(re, im2, n, divisors, box)
            lq = lattice_quadratic(n, h["v"])
            rec = {"locus_z": locus, "v": h["v"], "tau": h["tau"], **st,
                   "lattice_quadratic_nx_m2nz_my": list(lq),
                   "exponents_L3": dens.get(locus, {}).get("exponents"),
                   "exponent_denominator_lcm": dens.get(locus, {}).get("denominator_lcm")}
            clauses = []
            if locus not in dens:
                clauses.append("locus_absent_from_riemann_scheme")
            if not proportional(lq, st["primitive_quadratic_of_tau"]):
                clauses.append("lattice_quadratic_not_proportional_to_tau_quadratic")
            if st["stabilizer_order_in_box"] == 1:
                clauses.append("locus_has_trivial_stabilizer_in_box")
            for e in st["elements_up_to_sign"]:
                if not proportional(tuple(e["fixed_quadratic_c_dminusa_minusb"]), lq):
                    clauses.append("stabilizer_quadratic_not_proportional_to_lattice_quadratic")
            if st["stabilizer_order_exact"] != st["stabilizer_order_in_box"]:
                clauses.append("stabilizer_not_contained_in_box")
            if st["stabilizer_order_in_box"] != rec["exponent_denominator_lcm"]:
                clauses.append("order_neq_exponent_denominator")
            rec["clauses_fired"] = sorted(set(clauses))
            rec["generator"] = next((e for e in st["elements_up_to_sign"]
                                     if e["order_in_PSL2"] == st["stabilizer_order_in_box"]), None)
            loci.append(rec)
            violations += [f"{locus}:{c}" for c in rec["clauses_fired"]]
    # every other row of the table
    locus_vs = {tuple(h["v"]) for hits in fam["locus_hits"].values() for h in hits}
    others, unexpected = [], []
    for row in fam["rows"]:
        if tuple(row["v"]) in locus_vs:
            continue
        st = stabilizer(F(row["tau"]["re"]), F(row["tau"]["im_squared"]), n, divisors, box, cross_check=False)
        others.append({"v": row["v"], "D": row["D"], "D0": st["D0"], "order": st["stabilizer_order_in_box"],
                       "order_exact": st["stabilizer_order_exact"]})
        if st["stabilizer_order_in_box"] != 1 or st["stabilizer_order_exact"] != 1:
            unexpected.append(row["v"])
            violations.append(f"row {row['v']}:non_locus_row_has_nontrivial_stabilizer")
    return {"candidate": key, "n": n, "advisory": fam["advisory"], "flags": fam["flags"],
            "group": f"Gamma_0({n})* : Atkin-Lehner determinants {divisors}",
            "box": box, "loci": loci,
            "non_locus_rows": {"count": len(others),
                               "trivial_stabilizer_in_box": sum(o["order"] == 1 for o in others),
                               "trivial_stabilizer_exact_no_box": sum(o["order_exact"] == 1 for o in others),
                               "rows_with_nontrivial_stabilizer": unexpected},
            "orders_found": sorted(l["stabilizer_order_in_box"] for l in loci),
            "orders_from_exponent_denominators": sorted(d["denominator_lcm"] for k, d in dens.items() if k != "0"),
            "violations": violations}


def run(p2_path=P2):
    p2 = json.loads(pathlib.Path(p2_path).read_text())
    fams = {k: family(k, f) for k, f in p2["families"].items()}
    checks = {}
    for k, f in fams.items():
        checks[f"{k}: no clause fired"] = not f["violations"]
        checks[f"{k}: orders equal exponent denominators (as multisets)"] = \
            f["orders_found"] == f["orders_from_exponent_denominators"]
    hand = {}
    for k, f in fams.items():
        tag = " [ADVISORY]" if f["advisory"] else ""
        hand[f"{k}: every singular locus has a non-trivial stabilizer in the group{tag}"] = \
            all(l["stabilizer_order_in_box"] > 1 for l in f["loci"])
        hand[f"{k}: the stabilizer's quadratic is proportional to the lattice vector's "
             f"(input-consistency only, near-tautological by construction){tag}"] = \
            not any("proportional" in c for l in f["loci"] for c in l["clauses_fired"])
        hand[f"{k}: stabilizer order = lcm of L3 exponent denominators at each locus{tag}"] = \
            not any("order_neq" in c for l in f["loci"] for c in l["clauses_fired"])
    return {
        "certificate": "ELLIPTIC_POINTS_ARE_CM", "checker": "checkers/check_elliptic_points_are_CM.py",
        "date": "2026-09-21", "tier": "B", "checker_version": checker_version(),
        "status": "RECORD, NOT A GATE. The rho = 20 cut was ADOPTED by T0 on 2026-09-21 (D7', briefs/T0_DECISIONS_2026_09_21_STREAM2.md), read narrowly: no ranking of candidates, no minimum-|D| rule, no physical reading; T3 is not adopted; "
                  "nothing is scored. cooper_s10 is ADVISORY (lattice certificate DRAFT).",
        "forced_not_corroboration": FORCED,
        "input_consistency_checks_near_tautological": [
            "the stabilizer's fixed-point quadratic is proportional to the lattice vector's quadratic: the stabilizer "
            "is built from the tau of the P2 record and that tau is computed from v, so this can fire only on an "
            "internally inconsistent P2 record (tau field versus v field); it guards the input and is no evidence"],
        "search_boxes": {"path1_full_box_all_entries": BOX, "path2_bruteforce_all_entries": BOX2},
        "what_is_not_forced_and_was_checked": [
            "each locus of the P2 table has a non-trivial stabilizer in Gamma_0(n)* (exact search, box stated)",
            "stabilizer order = lcm of the denominators of the L3 local exponents at the locus",
            "no other row of the P2 table has a non-trivial stabilizer"],
        "inputs": {"sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (P2, SCHEME)}},
        "families": fams, "checks": checks,
        "hand_estimate": {"provenance": "orchestrator hand estimate, issued UNVERIFIED; scored here",
                          "clauses": {k: ("confirmed" if v else "REFUTED") for k, v in hand.items()}},
        "controls": "checkers/test_elliptic_points_are_CM_controls.py",
        "not_claimed": [
            "any independent support for 'rho = 20 at the singular loci': the agreement is forced",
            "that rho = 20 is a selection criterion, or that any point or family is preferred",
            "a machine proof of the exact determination (path 3): its three-line argument is in the docstring; it is cross-checked against the box search on every row",
            "that z is a Hauptmodul of Gamma_0(n)* : that is the statement of the s7 / s10 Hauptmodul certificates "
            "(Tier B), used here only to name the group",
            "the step from 'v orthogonal to the period' to 'rho = 20': cited framework of CM_POINTS_RHO20.json, Tier B",
            "any fibre type at any locus (ledger item 3); 'singular' refers to the operator L3 and to the "
            "stabilizer in the group, never to a fibre or to the surface",
            "anything certified about cooper_s10: advisory throughout",
            "any physical reading whatsoever"],
        "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: "
                      "checkers/test_elliptic_points_are_CM_controls.py | Reviewed-by: N",
    }


def checker_version():
    """git describe of the repo HEAD the checker ran on (the checker file itself may be uncommitted:
    `checker_sha256` pins its bytes)."""
    import subprocess
    try:
        d = subprocess.run(["git", "-C", str(ROOT), "describe", "--always", "--tags"],
                           capture_output=True, text=True, timeout=30).stdout.strip() or "unknown"
    except Exception:
        d = "unknown"
    return {"git_describe_HEAD": d, "checker_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}


def checks_ok(checks):
    return all(v is True for v in checks.values())


def main():
    cert = run()
    OUT.write_text(json.dumps(cert, indent=1) + "\n")
    for k, f in cert["families"].items():
        print(f"== {k} (n = {f['n']}){' ADVISORY' if f['advisory'] else ''}: {f['group']}")
        for l in f["loci"]:
            g = l["generator"]
            print(f"  z = {l['locus_z']:9s} v = {l['v']}  order {l['stabilizer_order_in_box']}  "
                  f"exponent-denominator lcm {l['exponent_denominator_lcm']}  generator {g['matrix'] if g else None} "
                  f"det {g['det'] if g else None}  clauses {l['clauses_fired']}")
        nl = f["non_locus_rows"]
        print(f"  other rows: {nl['count']}, trivial in box {nl['trivial_stabilizer_in_box']}, "
              f"trivial by the exact determination (no box) {nl['trivial_stabilizer_exact_no_box']}")
    print("hand estimate:", json.dumps(cert["hand_estimate"]["clauses"], indent=1))
    print("checks:", cert["checks"])
    return 0 if checks_ok(cert["checks"]) else 1


if __name__ == "__main__":
    sys.exit(main())
