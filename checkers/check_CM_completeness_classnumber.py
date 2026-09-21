#!/usr/bin/env python3
"""
check_CM_completeness_classnumber.py (A6) -- a completeness CONTROL for the P2 table
(data/certificates/CM_POINTS_RHO20.json), by exact enumeration of Heegner forms.

STATUS: RECORD, NOT A GATE.  Lattice / modular arithmetic, Tier B at best, no physical
reading.  The rho = 20 cut is adopted (T0 D7', 2026-09-21), read narrowly; T3 is not adopted; nothing is scored.
cooper_s10 output is ADVISORY (lattice certificate DRAFT).  P2 claims no completeness;
an INCOMPLETE row below is a finding about P2's window, not a failure of this checker
and not a defect of P2.

DERIVATION OF THE NORMALISATION (from v.omega = 0; every step is asserted at run time)
-------------------------------------------------------------------------------------
B(v, omega) = y - n x tau^2 + 2 n z tau, so tau is a root of  n x t^2 - 2 n z t - y.
With d = div(v) = gcd(x, y, 2 n z) put  F_v = [A, B, C] = [n x, -2 n z, -y] / d.  Then
  (i)   F_v is integral, n | A, and gcd(A/n, B, C) = 1          (v primitive)
  (ii)  disc F_v = B^2 - 4AC = 2 n v^2 / d^2 = D,  the discriminant of T_X = v^perp
        recorded in the table (asserted against every row's D),
  (iii) v -> F_v is a bijection {primitive v, x > 0, v^2 < 0} -> {positive definite [A,B,C]:
        n | A, gcd(A/n, B, C) = 1}; the inverse is d = 2n / gcd(2n, B), v = (dA/n, -dC, -dB/2n)
        (asserted as a round trip on every vector used).
These are the Heegner forms of level n (gcd(A, B, C) need not be 1: forms whose content
divides n occur, e.g. [7, 0, 7]).

EXPECTED NUMBER OF POINTS, BY ENUMERATION (no class-number formula is typed in)
-------------------------------------------------------------------------------
For each D: all SL_2(Z)-reduced forms Q of discriminant D (any content) are listed.  For
each Q and each point c of P^1(Z/n) (= the cosets SL_2(Z)/Gamma_0(n), via the first column)
a lift M_c in SL_2(Z) is built and Q o M_c is tested for the Heegner condition.  Q o (S M)
= Q o M for S in Aut(Q) (found by exhaustion over entries in {-1,0,1}, which contains
every automorph of a reduced form), so the Gamma_0(n)-classes are the Aut(Q)-orbits of
admissible c.  The Atkin-Lehner operators (one matrix W_Q per exact divisor Q of n, found
by search) act on forms by F -> (F o W_Q)/Q; the image is reduced again, with the
transformation tracked, to read off its class.  Complex conjugation tau -> -conj(tau) is
[A, B, C] -> [A, -B, C].  Orbits under <Atkin-Lehner> give the points of X_0(n)*; orbits
under <Atkin-Lehner, conjugation> give the quantity comparable with the table, which
identifies z with conj(z).

CROSS-CHECKS (each can fail, each has a control)
  X1  class-number cross-check of the enumeration (the formula is used ONLY here): for
      gcd(D, n) = 1, #Gamma_0(n)-classes = h(D) * #{beta mod 2n : beta^2 = D mod 4n}, with
      h(D) counted here from the primitive reduced forms.  This is the standard Heegner-form
      count (Gross-Kohnen-Zagier); it has NOT been fetched or pinned in docs/literature, which
      is why it serves as a cross-check and not as the method.  Applied to every D of the table and every D in -400 < D < 0 that
      is coprime to n.  COVERAGE, stated because it is small: nearly every discriminant of the
      table shares a factor with n, so X1 reaches only a few table rows (the certificate lists
      which: `table_discriminants_covered`).  X1 validates the enumeration code in general; it
      does NOT validate the per-D expected counts of the table.  Those rest on X2 and X3.
  X2  every one of P2's window vectors maps to one of the enumerated classes, and P2's
      NUMERIC grouping by z (40 digits) coincides with the EXACT orbit partition under
      <Gamma_0(n), Atkin-Lehner, conjugation>.  This is two independent code paths (modular
      function values vs. integer group theory) and it tests that z is invariant under
      exactly that group.
  X3  brute force: every Heegner form with A <= n * 12, |B| <= A falls in an enumerated
      class (tested for the D of the table).

ABSENT D.  The table's window is cut on -v^2, not on D, so discriminants with
-v^2 = |D| div(v)^2/(2n) above the bound never enter it.  Every D up to the largest |D| of
the table that carries at least one Heegner class and is not in the table is listed as
ABSENT(missing all k), with the (-v^2, div v) it would need; an absent D whose required norm
lies INSIDE the bound would be a contradiction and gates the exit code.

OUTPUT per D: expected, found (distinct z of that D in the table), COMPLETE /
INCOMPLETE(missing k).  `found > expected` would be a contradiction and gates the exit code.
"""
import hashlib
import json
import pathlib
import sys
from math import gcd, isqrt

ROOT = pathlib.Path(__file__).resolve().parents[1]
CERTS = ROOT / "data" / "certificates"
P2 = CERTS / "CM_POINTS_RHO20.json"
OUT = CERTS / "CM_COMPLETENESS.json"
X1_RANGE = 400


class Refusal(Exception):
    def __init__(self, clause, msg=""):
        super().__init__(f"{clause}: {msg}")
        self.clause = clause


# ------------------------------------------------------------------ forms and matrices
def disc(f):
    return f[1] * f[1] - 4 * f[0] * f[2]


def act(f, M):
    """f o M, M = (p, q, r, s): (x, y) -> (p x + q y, r x + s y)."""
    A, B, C = f
    p, q, r, s = M
    return (A * p * p + B * p * r + C * r * r,
            2 * A * p * q + B * (p * s + q * r) + 2 * C * r * s,
            A * q * q + B * q * s + C * s * s)


def mmul(X, Y):
    return (X[0] * Y[0] + X[1] * Y[2], X[0] * Y[1] + X[1] * Y[3],
            X[2] * Y[0] + X[3] * Y[2], X[2] * Y[1] + X[3] * Y[3])


def minv(M):
    p, q, r, s = M
    if p * s - q * r != 1:
        raise Refusal("not_unimodular")
    return (s, -q, -r, p)


def reduce_form(f):
    """(Q, T) with f o T = Q reduced (|b| <= a <= c, b >= 0 if |b| = a or a = c), T in SL_2(Z)."""
    A, B, C = f
    if A <= 0 or disc(f) >= 0:
        raise Refusal("form_not_positive_definite", str(f))
    T = (1, 0, 0, 1)
    while True:
        A, B, C = f
        if A > C or (A == C and B < 0):
            S = (0, -1, 1, 0)
            f, T = act(f, S), mmul(T, S)
            continue
        if not (-A < B <= A):
            k = (A - B) // (2 * A)            # B + 2Ak in (-A, A]
            S = (1, k, 0, 1)
            f, T = act(f, S), mmul(T, S)
            continue
        return f, T


def reduced_forms(D):
    """All reduced positive definite forms of discriminant D, any content."""
    if D >= 0 or D % 4 not in (0, 1):
        return []
    out = []
    for a in range(1, isqrt(-D // 3) + 2):
        for b in range(-a + 1, a + 1):
            if (b * b - D) % (4 * a):
                continue
            c = (b * b - D) // (4 * a)
            if c < a or (a == c and b < 0):
                continue
            out.append((a, b, c))
    return out


def automorphs(Q):
    return [M for M in ((p, q, r, s) for p in (-1, 0, 1) for q in (-1, 0, 1) for r in (-1, 0, 1) for s in (-1, 0, 1))
            if M[0] * M[3] - M[1] * M[2] == 1 and act(Q, M) == Q]


# ------------------------------------------------------------------ P^1(Z/n)
def p1_canon(p, r, n):
    p, r = p % n, r % n
    if gcd(gcd(p, r), n) != 1:
        raise Refusal("not_a_point_of_P1", f"({p}:{r}) mod {n}")
    return min(((u * p) % n, (u * r) % n) for u in range(1, n + 1) if gcd(u, n) == 1)


def p1_points(n):
    return sorted({p1_canon(p, r, n) for p in range(n) for r in range(n) if gcd(gcd(p, r), n) == 1})


def ext_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x, y = ext_gcd(b, a % b)
    return (g, y, x - (a // b) * y)


def lift(c, n):
    """A matrix of SL_2(Z) whose first column is = c mod n."""
    p0, r0 = c
    for i in range(0, 4 * n + 1):
        for j in range(0, 4 * n + 1):
            p, r = p0 + i * n, r0 + j * n
            if (p or r) and gcd(p, r) == 1:
                g, u, w = ext_gcd(p, r)      # u p + w r = g = +-1
                u, w = u * g, w * g
                M = (p, -w, r, u)
                if M[0] * M[3] - M[1] * M[2] != 1:
                    raise Refusal("lift_failed")
                return M
    raise Refusal("lift_failed")


# ------------------------------------------------------------------ Heegner forms
def is_heegner(f, n):
    A, B, C = f
    return A > 0 and A % n == 0 and gcd(gcd(A // n, B), C) == 1 and disc(f) < 0


def form_of_vector(n, v):
    x, y, z = v
    d = gcd(gcd(x, y), 2 * n * z)
    f = (n * x // d, -2 * n * z // d, -y // d)
    if (n * x) % d or (2 * n * z) % d or y % d or not is_heegner(f, n):
        raise Refusal("vector_form_not_heegner", f"{v} -> {f}")
    if disc(f) * d * d != 2 * n * (2 * x * y + 2 * n * z * z):
        raise Refusal("discriminant_normalisation_fails", str(v))
    if vector_of_form(n, f) != tuple(v):
        raise Refusal("form_vector_round_trip_fails", f"{v} -> {f} -> {vector_of_form(n, f)}")
    return f


def vector_of_form(n, f):
    A, B, C = f
    d = 2 * n // gcd(2 * n, B)
    return (d * A // n, -d * C, -d * B // (2 * n))


def exact_divisors(n):
    return [q for q in range(1, n + 1) if n % q == 0 and gcd(q, n // q) == 1]


def atkin_lehner_matrix(n, Q):
    """(Q a, b, n c, Q d) with determinant Q; smallest by search."""
    if Q == 1:
        return (1, 0, 0, 1)
    for size in range(1, 4 * n):
        for a in range(-size, size + 1):
            for d in range(-size, size + 1):
                rest = Q * Q * a * d - Q            # = n b c
                if rest % n:
                    continue
                bc = rest // n
                for b in range(-size, size + 1):
                    if b and bc % b == 0 and abs(bc // b) <= size:
                        return (Q * a, b, n * (bc // b), Q * d)
    raise Refusal("no_atkin_lehner_matrix", str(Q))


def al_act(f, W, Q, n):
    g = act(f, W)
    if any(t % Q for t in g):
        raise Refusal("atkin_lehner_image_not_integral", f"{f} {W}")
    g = tuple(t // Q for t in g)
    if not is_heegner(g, n) or disc(g) != disc(f):
        raise Refusal("atkin_lehner_image_not_heegner", f"{f} -> {g}")
    return g


class Classes:
    """Gamma_0(n)-classes of Heegner forms of discriminant D, and the orbit structure."""

    def __init__(self, n, D, divisors=None):
        self.n, self.D = n, D
        self.divisors = exact_divisors(n) if divisors is None else divisors
        self.reduced = reduced_forms(D)
        self.auts = {Q: automorphs(Q) for Q in self.reduced}
        self.reps = {}                                   # key -> representative Heegner form
        pts = p1_points(n)
        for Q in self.reduced:
            for c in pts:
                f = act(Q, lift(c, n))
                if is_heegner(f, n):
                    self.reps.setdefault(self._key(Q, c), f)
        self.keys = sorted(self.reps)
        parent = {k: k for k in self.keys}
        parent_conj = {k: k for k in self.keys}

        def find(par, k):
            while par[k] != k:
                par[k] = par[par[k]]
                k = par[k]
            return k

        for k, f in self.reps.items():
            for Qd in self.divisors:
                img = self.key_of(al_act(f, atkin_lehner_matrix(n, Qd), Qd, n))
                for par in (parent, parent_conj):
                    par[find(par, k)] = find(par, img)
            img = self.key_of((f[0], -f[1], f[2]))
            parent_conj[find(parent_conj, k)] = find(parent_conj, img)
        self.orbit = {k: find(parent, k) for k in self.keys}
        self.orbit_conj = {k: find(parent_conj, k) for k in self.keys}

    def _key(self, Q, c):
        n = self.n
        return (Q, min(p1_canon(S[0] * c[0] + S[1] * c[1], S[2] * c[0] + S[3] * c[1], n) for S in self.auts[Q]))

    def key_of(self, f):
        if not is_heegner(f, self.n) or disc(f) != self.D:
            raise Refusal("not_a_heegner_form_of_this_discriminant", str(f))
        Q, T = reduce_form(f)
        M = minv(T)                                      # f = Q o M
        if act(Q, M) != f:
            raise Refusal("reduction_tracking_fails", str(f))
        k = self._key(Q, p1_canon(M[0], M[2], self.n))
        if k not in self.reps:
            raise Refusal("form_outside_enumerated_classes", f"{f} -> {k}")
        return k

    def counts(self):
        return {"reduced_forms_any_content": len(self.reduced),
                "gamma0_classes": len(self.keys),
                "points_on_X0n_star": len(set(self.orbit.values())),
                "points_up_to_conjugation": len(set(self.orbit_conj.values()))}


# ------------------------------------------------------------------ cross-checks
def class_number(D):
    return sum(1 for f in reduced_forms(D) if gcd(gcd(f[0], f[1]), f[2]) == 1)


def x1_formula(n, D):
    """Only where gcd(D, n) = 1.  Returns (formula value, enumeration value)."""
    betas = sum(1 for b in range(2 * n) if (b * b - D) % (4 * n) == 0)
    return class_number(D) * betas, len(Classes(n, D, divisors=[1]).keys)


def x3_bruteforce(n, D, cl, amax_mult=12):
    seen, bad = 0, []
    for A in range(n, n * amax_mult + 1, n):
        for B in range(-A, A + 1):
            if (B * B - D) % (4 * A):
                continue
            f = (A, B, (B * B - D) // (4 * A))
            if is_heegner(f, n):
                seen += 1
                try:
                    cl.key_of(f)
                except Refusal as e:
                    bad.append([list(f), e.clause])
    return seen, bad


def norm_div_pairs(n, cl):
    """The distinct (-v^2, div v) over the lattice vectors of all Gamma_0(n)-classes of one D."""
    return sorted({(-(2 * v[0] * v[1] + 2 * n * v[2] * v[2]), gcd(gcd(v[0], v[1]), 2 * n * v[2]))
                   for v in (vector_of_form(n, f) for f in cl.reps.values())})


def family(key, fam, rows=None, vectors_and_groups=None, divisors=None, window_bound=None, scan_absent=True):
    n = fam["n"]
    rows = fam["rows"] if rows is None else rows
    per_D, cache, contradictions = [], {}, []
    found = {}
    for r in rows:
        found.setdefault(r["D"], []).append(r)
    for D in sorted(found, reverse=True):
        cl = cache.setdefault(D, Classes(n, D, divisors))
        cnt = cl.counts()
        orbits_hit = {}
        for r in found[D]:
            f = form_of_vector(n, tuple(r["v"]))
            if disc(f) != r["D"]:
                raise Refusal("row_D_disagrees_with_form_discriminant", str(r["v"]))
            orbits_hit.setdefault(cl.orbit_conj[cl.key_of(f)], []).append(r["v"])
        dup = {str(k): v for k, v in orbits_hit.items() if len(v) > 1}
        if dup:
            contradictions.append({"D": D, "clause": "two_table_rows_in_one_orbit", "rows": list(dup.values())})
        exp, fnd = cnt["points_up_to_conjugation"], len(orbits_hit)
        missing_reps = sorted(list(cl.reps[k]) for k in
                              {o: min(kk for kk in cl.keys if cl.orbit_conj[kk] == o)
                               for o in set(cl.orbit_conj.values()) - set(orbits_hit)}.values())
        seen, bad = x3_bruteforce(n, D, cl)
        if bad:
            contradictions.append({"D": D, "clause": "bruteforce_form_outside_enumerated_classes", "forms": bad[:5]})
        if fnd > exp:
            contradictions.append({"D": D, "clause": "found_exceeds_expected"})
        per_D.append({"D": D, **cnt, "expected": exp, "found": fnd, "table_rows_of_this_D": len(found[D]),
                      "verdict": "COMPLETE" if fnd == exp else f"INCOMPLETE(missing {exp - fnd})",
                      "missing_points_representative_forms": missing_reps,
                      "missing_points_representative_vectors": [list(vector_of_form(n, tuple(f))) for f in missing_reps],
                      "x3_bruteforce_forms_checked": seen,
                      "minus_v2_and_div_of_classes": [list(t) for t in norm_div_pairs(n, cl)]})
    # discriminants that carry points but are absent from the table altogether
    absent = []
    max_abs = max(-D for D in found) if found else 0
    for D in (range(-1, -max_abs - 1, -1) if scan_absent else ()):
        if D % 4 not in (0, 1) or D in found:
            continue
        cl = Classes(n, D, divisors)
        if not cl.keys:
            continue
        need = norm_div_pairs(n, cl)
        if window_bound is not None and any(m <= window_bound for m, _ in need):
            contradictions.append({"D": D, "clause": "absent_D_has_a_norm_inside_the_window", "need": need})
        absent.append({"D": D, "expected": cl.counts()["points_up_to_conjugation"], "found": 0,
                       "verdict": f"ABSENT(missing all {cl.counts()['points_up_to_conjugation']})",
                       "minus_v2_and_div_required": [list(t) for t in need]})
    x2 = None
    if vectors_and_groups is not None:
        vs, groups = vectors_and_groups
        exact = {}
        for v in vs:
            f = form_of_vector(n, tuple(v))
            D = disc(f)
            cl = cache.setdefault(D, Classes(n, D, divisors))
            exact.setdefault((D, cl.orbit_conj[cl.key_of(f)]), set()).add(tuple(v))
        part_exact = sorted(sorted(s) for s in exact.values())
        part_num = sorted(sorted(tuple(v) for v in g) for g in groups)
        x2 = {"vectors": len(vs), "numeric_groups": len(part_num), "exact_orbits": len(part_exact),
              "partitions_identical": part_exact == part_num}
    return {"candidate": key, "n": n, "advisory": fam["advisory"], "flags": fam["flags"],
            "group": f"Gamma_0({n})* , Atkin-Lehner determinants {exact_divisors(n) if divisors is None else divisors}, "
                     "and complex conjugation (the table identifies z with conj z)",
            "per_D": per_D,
            "discriminants_with_more_than_one_norm_div_pair": {
                "listed": [p["D"] for p in per_D if len(p["minus_v2_and_div_of_classes"]) > 1],
                "absent": [a["D"] for a in absent if len(a["minus_v2_and_div_required"]) > 1]},
            "absent_D": {"range": f"-{max_abs} <= D < 0, D not in the table, at least one Heegner class",
                         "count": len(absent), "points_missing": sum(a["expected"] for a in absent),
                         "least_abs_D_absent": (-absent[0]["D"] if absent else None),
                         "reason": "each absent D needs -v^2 = |D| div(v)^2/(2n) above the table's logged bound on -v^2 "
                                   "(checked: no absent D has a required norm inside the bound)",
                         "rows": absent},
            "summary": {"D_values": len(per_D), "complete": sum(p["verdict"] == "COMPLETE" for p in per_D),
                        "incomplete": sum(p["verdict"] != "COMPLETE" for p in per_D),
                        "expected_total": sum(p["expected"] for p in per_D),
                        "found_total": sum(p["found"] for p in per_D),
                        "least_abs_D_incomplete_in_table":
                            next((-p["D"] for p in per_D if p["verdict"] != "COMPLETE"), None)},
            "x2_numeric_grouping_vs_exact_orbits": x2, "contradictions": contradictions}


def x1_all(n, table_Ds):
    rows, bad = [], []
    Ds = sorted({D for D in range(-X1_RANGE + 1, 0) if D % 4 in (0, 1)} | set(table_Ds), reverse=True)
    for D in Ds:
        if gcd(D, n) != 1:
            continue
        a, b = x1_formula(n, D)
        rows.append([D, a, b])
        if a != b:
            bad.append([D, a, b])
    tab = sorted(set(table_Ds), reverse=True)
    covered = [D for D in tab if gcd(D, n) == 1]
    return {"discriminants_checked": len(rows), "disagreements": bad, "nonzero_cases": sum(1 for r in rows if r[1]),
            "table_discriminants_total": len(tab), "table_discriminants_covered": covered,
            "table_discriminants_covered_count": len(covered),
            "coverage_note": "X1 applies only where gcd(D, n) = 1. It therefore tests the enumeration CODE on "
                             f"{len(rows)} discriminants, but only {len(covered)} of the {len(tab)} discriminants of the "
                             "table; at the others (D sharing a factor with n: forms with content, ramified primes) "
                             "the expected counts are NOT cross-checked by X1 and rest on the enumeration plus X2 "
                             "and X3 alone."}


def run(p2_path=P2, with_x2=True):
    p2 = json.loads(pathlib.Path(p2_path).read_text())
    fams, checks, x1 = {}, {}, {}
    for key, fam in p2["families"].items():
        vg = None
        if with_x2:
            sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
            import check_CM_points_rho20 as CM
            rel, r = CM.relation_for(key, fam["n"])
            vs = CM.enumerate_vectors(fam["n"])
            vg = (vs, CM.group_by_z(fam["n"], rel, r, vs))
        fams[key] = family(key, fam, vectors_and_groups=vg, window_bound=p2["window"]["BOUND_minus_v2"])
        x1[key] = x1_all(fam["n"], [r["D"] for r in fam["rows"]])
        checks[f"{key}: no contradiction (found <= expected, rows in distinct orbits, brute force inside classes)"] = \
            not fams[key]["contradictions"]
        checks[f"{key}: X1 class-number formula agrees with enumeration"] = not x1[key]["disagreements"]
        if with_x2:
            checks[f"{key}: X2 numeric z-grouping equals exact orbit partition"] = \
                fams[key]["x2_numeric_grouping_vs_exact_orbits"]["partitions_identical"] is True
    return {
        "certificate": "CM_COMPLETENESS", "checker": "checkers/check_CM_completeness_classnumber.py",
        "date": "2026-09-21", "tier": "B", "checker_version": checker_version(),
        "status": "RECORD, NOT A GATE. A completeness CONTROL on the P2 table. P2 claims no completeness; "
                  "INCOMPLETE rows are a finding about P2's window, not a failure. The rho = 20 cut was ADOPTED by T0 on 2026-09-21 (D7', briefs/T0_DECISIONS_2026_09_21_STREAM2.md), read narrowly: no ranking of candidates, no minimum-|D| rule, no physical reading; "
                  "nothing is scored. cooper_s10 is ADVISORY (lattice certificate DRAFT).",
        "normalisation": "F_v = [n x, -2 n z, -y]/div(v); disc F_v = 2 n v^2/div(v)^2 = D of the table; Heegner "
                         "condition n | A, gcd(A/n, B, C) = 1; asserted on every vector used",
        "inputs": {"sha256": {str(P2.relative_to(ROOT)): hashlib.sha256(pathlib.Path(p2_path).read_bytes()).hexdigest()}},
        "families": fams, "x1_class_number_cross_check": x1, "checks": checks,
        "tier_notes": ["expected counts: exact integer enumeration",
                       "found counts: rows of the P2 table, whose grouping by z is numeric (Tier B); X2 re-derives "
                       "that grouping exactly",
                       "the identification 'points of X_0(n)* <-> values of z' rests on the s7 / s10 Hauptmodul "
                       "certificates (Tier B); X2 is consistent with it on the window and does not prove it",
                       "X1 formula: standard (Gross-Kohnen-Zagier), not among the pinned sources; used as a cross-check only; "
                       "it covers only the table discriminants coprime to n (see coverage_note per family)"],
        "controls": "checkers/test_CM_completeness_classnumber_controls.py",
        "not_claimed": [
            "that P2 is defective: it claims no completeness, and this control measures its window",
            "that COMPLETE at a D means the z-values or minimal polynomials of that D are certified: recognition stays Tier B numeric",
            "that the table is complete as a list of discriminants: D absent from it are listed under absent_D",
            "that rho = 20 is a selection criterion or that any point is preferred",
            "anything certified about cooper_s10: advisory throughout",
            "any physical reading whatsoever"],
        "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: "
                      "checkers/test_CM_completeness_classnumber_controls.py | Reviewed-by: N",
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
        print(f"== {k} (n = {f['n']}){' ADVISORY' if f['advisory'] else ''}  {f['summary']}")
        for p in f["per_D"]:
            print(f"   D = {p['D']:5d}  classes {p['gamma0_classes']:3d}  X0* points {p['points_on_X0n_star']:3d}  "
                  f"expected(up to conj) {p['expected']:3d}  found {p['found']:3d}  {p['verdict']}")
        a = f["absent_D"]
        print(f"   ABSENT D in range: {a['count']} discriminants, {a['points_missing']} points; least |D| absent: {a['least_abs_D_absent']}; "
              f"first: {[(r['D'], r['expected'], r['minus_v2_and_div_required']) for r in a['rows'][:4]]}")
        print("   X2:", f["x2_numeric_grouping_vs_exact_orbits"], " X1:", cert["x1_class_number_cross_check"][k])
        print("   contradictions:", f["contradictions"])
    print("checks:", cert["checks"])
    return 0 if checks_ok(cert["checks"]) else 1


if __name__ == "__main__":
    sys.exit(main())
