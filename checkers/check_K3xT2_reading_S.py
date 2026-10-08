#!/usr/bin/env python3
"""check_K3xT2_reading_S.py -- the lattice side of Reading S of "K3 x T^2" (ruling D29', 2026-10-08), computed.

Reading S: for selection criteria, "K3 x T^2" denotes the Shioda-Inose pairing of a family member X with a product E x E' of
elliptic curves related by a cyclic isogeny of degree n. Two facts carry it:
  (i)  T(X) ~= T(E x E') for an Inose surface X = Ino(E, E')  -- Shioda-Inose structure; pinned source: Kumar-Kuwata
       arXiv:1409.2931 Remark 2.2 (txt l.245-248). Tier L. Not recomputed here.
  (ii) for E, E' WITHOUT complex multiplication related by a cyclic n-isogeny, T(E x E') ~= U + <2n>. Usually cited to
       Morrison, Invent. Math. 75 (1984) 105-121 (doi:10.1007/BF01403093), which is paywalled and was NOT fetched.
       THIS SCRIPT COMPUTES (ii) instead of citing it.

How (ii) is computed, exactly, from first principles. E x E' = C^2 / Lambda with Lambda = Z^4 (e1, e2 from E; e3, e4 from E').
H^2(E x E', Z) = wedge^2 Hom(Lambda, Z), unimodular of signature (3,3); identify it with wedge^2 Lambda by the volume form, so
the class of a 2-dimensional subtorus spanned by v1, v2 in Lambda is the bivector v1 ^ v2, and the intersection pairing is
<u, w> = coefficient of e1^e2^e3^e4 in u ^ w. The classes:
   B = e1^e2 (E x pt),   A = e3^e4 (pt x E'),   Gamma_M = (e1 + M e1) ^ (e2 + M e2)  (graph of the isogeny with matrix M),
where M is the integer matrix of the isogeny on lattices, det M = deg = n > 0 (holomorphic maps preserve orientation).
ASSUMPTION, NOT COMPUTED: E, E' have no complex multiplication, so Hom(E, E') ~= Z and NS(E x E') = <A, B, Gamma_M> has rank 3.
Checks: NS has signature (1,2); NS is saturated (gcd of maximal minors = 1; a non-cyclic M fails this); T = NS^perp is
computed as an integral basis; T has signature (2,1) and is isometric to the CERTIFIED Gram of the family's C2 certificate,
by an explicit unimodular basis change stored as a witness. n and the target Gram are READ from the certificates.

Part R (cooper_s7 only, the three rho = 20 points): the explicit model gives E1 ~= E2 there, with j read from
TW2_RHO20_LOCI.json (and j = 0 at z = infinity, INOSE_MODEL_M7 S6). The CM order of each j is identified by COMPUTATION:
class number one discriminants are enumerated by counting reduced forms, j(tau_D) is evaluated numerically and matched to
the exact model j. Then T(E x E) is computed from NS = <A, B, Gamma_1, Gamma_tau> and compared with the CM_POINTS_RHO20
row. Ledger item 8: this agreement is FORCED (elliptic point => CM, Shioda-Inose) -- consistency, never corroboration.
cooper_s10 rho = 20 points are NOT covered (no explicit s10 Inose model; the D = -20 row would need E x E' with E !~= E').

Usage: python3 checkers/check_K3xT2_reading_S.py [--emit]
Generated-by: Claude (Opus 5.5), Stream 2, 2026-10-08 | Verified-by: checkers/test_K3xT2_reading_S_controls.py | Reviewed-by: N
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

import mpmath
import sympy as sp

REPO = Path(__file__).resolve().parent.parent
CERTS = REPO / "data" / "certificates"
OUT = CERTS / "K3xT2_READING_S.json"
C2 = {"cooper_s7": "C2_cooper_s7_v6.json", "cooper_s10": "C2_cooper_s10_v5.json"}
PAIRS = list(itertools.combinations(range(4), 2))          # basis of wedge^2 Z^4: e_ij, i<j


class Refuse(RuntimeError):
    pass


# ---------- exterior algebra on Z^4 ----------
def wedge(v1, v2):
    return [v1[i] * v2[j] - v1[j] * v2[i] for i, j in PAIRS]


def _sign(perm):
    s, p = 1, list(perm)
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                s = -s
    return s


PAIRING = [[(_sign(a + b) if len(set(a + b)) == 4 else 0) for b in PAIRS] for a in PAIRS]


def pair(u, w):
    return sum(u[a] * PAIRING[a][b] * w[b] for a in range(6) for b in range(6))


def gram(vs):
    return [[pair(u, w) for w in vs] for u in vs]


def _sign_changes(coeffs):
    s = [c for c in coeffs if c != 0]
    return sum(1 for a, b in zip(s, s[1:]) if (a > 0) != (b > 0))


def signature(G):
    """exact inertia: a symmetric matrix has a real-rooted characteristic polynomial, so Descartes' rule is exact."""
    x = sp.Symbol("x")
    p = sp.Poly(sp.Matrix(G).charpoly(x).as_expr(), x)
    if p.eval(0) == 0:
        raise Refuse(f"degenerate form {G}")
    pos = _sign_changes(p.all_coeffs())
    neg = _sign_changes(sp.Poly(p.as_expr().subs(x, -x), x).all_coeffs())
    return [pos, neg]


def max_minor_gcd(rows):
    k = len(rows)
    g = 0
    for cols in itertools.combinations(range(len(rows[0])), k):
        g = gcd(g, int(sp.Matrix([[r[c] for c in cols] for r in rows]).det()))
    return abs(g)


def saturate(rows):
    """integral basis of (Q-span of rows) intersected with Z^m."""
    rows = [list(r) for r in rows]
    while True:
        d = max_minor_gcd(rows)
        if d == 0:
            raise Refuse("rows are dependent")
        if d == 1:
            return rows
        p = int(sp.factorint(d).__iter__().__next__())
        M = sp.Matrix(rows).T                                  # m x k ; find c with M c = 0 mod p
        ns = M.applyfunc(lambda x: x % p)
        sol = None
        for c in itertools.product(range(p), repeat=len(rows)):
            if any(c) and all(sum(ci * r[j] for ci, r in zip(c, rows)) % p == 0 for j in range(len(rows[0]))):
                sol = c
                break
        if sol is None:
            raise Refuse("saturation step failed")
        i = next(i for i, ci in enumerate(sol) if ci % p)
        new = [sum(ci * r[j] for ci, r in zip(sol, rows)) // p for j in range(len(rows[0]))]
        rows[i] = new


def complement(ns_rows):
    """integral basis of the orthogonal complement of ns_rows in (wedge^2 Z^4, pairing)."""
    A = sp.Matrix([[sum(r[a] * PAIRING[a][b] for a in range(6)) for b in range(6)] for r in ns_rows])
    basis = []
    for v in A.nullspace():
        den = sp.ilcm(*[sp.fraction(x)[1] for x in v])
        basis.append([int(x * den) for x in v])
    return saturate(basis)


def graph(M):
    v1 = [1, 0, M[0][0], M[1][0]]
    v2 = [0, 1, M[0][1], M[1][1]]
    return wedge(v1, v2)


A_CLS = wedge([0, 0, 1, 0], [0, 0, 0, 1])
B_CLS = wedge([1, 0, 0, 0], [0, 1, 0, 0])


def find_isometry(T_rows, target, box=4):
    """coefficient matrix C (det +-1) with C G_T C^t == target; brute force over a small box."""
    GT = sp.Matrix(gram(T_rows))
    tgt = sp.Matrix(target)
    k = len(T_rows)
    vecs = list(itertools.product(range(-box, box + 1), repeat=k))
    by_norm = {}
    for c in vecs:
        if any(c):
            v = sp.Matrix([c])
            by_norm.setdefault(int((v * GT * v.T)[0]), []).append(c)
    diag = [int(tgt[i, i]) for i in range(k)]
    cand = [by_norm.get(d, []) for d in diag]
    for c0 in cand[0]:
        for c1 in cand[1]:
            r01 = (sp.Matrix([c0]) * GT * sp.Matrix([c1]).T)[0]
            if r01 != tgt[0, 1]:
                continue
            for c2 in cand[2] if k == 3 else [()]:
                C = sp.Matrix([c0, c1, c2]) if k == 3 else sp.Matrix([c0, c1])
                if abs(C.det()) == 1 and C * GT * C.T == tgt:
                    return [list(map(int, r)) for r in C.tolist()]
    return None


def generic_check(n, target_gram, target_sig, M=None):
    M = M if M is not None else [[1, 0], [0, n]]
    detM = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    ns = [A_CLS, B_CLS, graph(M)]
    G_ns = gram(ns)
    out = {"n": n, "isogeny_matrix": M, "det_M": detM, "NS_gram": G_ns, "NS_signature": signature(G_ns),
           "NS_max_minor_gcd": max_minor_gcd(ns)}
    out["NS_saturated"] = out["NS_max_minor_gcd"] == 1
    if out["NS_signature"] != [1, 2]:
        out["verdict"] = "FAIL_NS_SIGNATURE"
        return out
    if not out["NS_saturated"]:
        out["verdict"] = "FAIL_NS_NOT_SATURATED (isogeny not cyclic of degree det M)"
        return out
    T = complement(ns)
    G_T = gram(T)
    out.update({"T_basis_in_wedge2": T, "T_gram": G_T, "T_det": int(sp.Matrix(G_T).det()), "T_signature": signature(G_T)})
    if out["T_signature"] != target_sig:
        out["verdict"] = "FAIL_T_SIGNATURE"
        return out
    W = find_isometry(T, target_gram)
    out["isometry_witness_rows"] = W
    out["target_gram"] = target_gram
    if W is None:
        out["verdict"] = "FAIL_NO_ISOMETRY_TO_CERTIFIED_GRAM"
        return out
    C = sp.Matrix(W)
    assert C * sp.Matrix(G_T) * C.T == sp.Matrix(target_gram)
    out["verdict"] = "ISOMETRIC_TO_CERTIFIED_T"
    return out


# ---------- part R: CM points of cooper_s7 ----------
def reduced_forms(D):
    out = []
    for a in range(1, int((abs(D) / 3) ** 0.5) + 2):
        for b in range(-a + 1, a + 1):
            if (b * b - D) % (4 * a):
                continue
            c = (b * b - D) // (4 * a)
            if c < a or (c == a and b < 0) or (abs(b) == a and b < 0):
                continue
            if gcd(gcd(a, abs(b)), c) != 1:                    # class number counts PRIMITIVE forms
                continue
            out.append((a, b, c))
    return out


def class_number_one(limit=200):
    return [D for D in range(-3, -limit, -1) if D % 4 in (0, 1) and len(reduced_forms(D)) == 1]


def tau_of(D):
    """principal root tau = (-b + sqrt(D))/2 with b = D mod 2, and its minimal polynomial tau^2 - t tau + s."""
    b = D % 2
    t = -b
    s = (b * b - D) // 4
    return t, s


def j_numeric(D):
    t, s = tau_of(D)
    mpmath.mp.dps = 60
    tau = (t + mpmath.sqrt(D)) / 2
    return 1728 * mpmath.kleinj(tau)


def order_for_j(j_exact):
    hits = []
    for D in class_number_one():
        jv = j_numeric(D)
        if abs(mpmath.im(jv)) < 1e-20 and abs(mpmath.re(jv) - j_exact) < mpmath.mpf(10) ** -15 * max(1, abs(j_exact)):
            hits.append(D)
    return hits


def T_of_ExE(D):
    t, s = tau_of(D)                                   # tau^2 = t tau - s
    R = [[0, -s], [1, t]]                              # multiplication by tau on basis (1, tau), columns = images
    ns = [A_CLS, B_CLS, graph([[1, 0], [0, 1]]), graph(R)]
    if max_minor_gcd(ns) != 1:
        raise Refuse(f"NS(E x E) for D={D} not saturated")
    T = complement(ns)
    G = gram(T)
    a2, b, c2 = G[0][0], G[0][1], G[1][1]
    if signature(G) != [2, 0]:
        raise Refuse(f"T(E x E) for D={D} not positive definite: {G}")
    # Gauss reduction of the even form [[2a,b],[b,2c]]
    a, c = a2 // 2, c2 // 2
    while True:
        if c < a:
            a, c, b = c, a, -b
        elif abs(b) > a:
            k = (b + a) // (2 * a) if b > 0 else -((-b + a) // (2 * a))
            c = c - k * b + k * k * a
            b = b - 2 * k * a
        else:
            break
    if b < 0 and (abs(b) == a or a == c):
        b = -b
    return {"NS_rank": 4, "NS_gram": gram(ns), "T_gram": G, "T_reduced_abc": [a, b, c], "disc": b * b - 4 * a * c}


def run():
    res = {"generic": {}, "rho20_cooper_s7": {}}
    for fam, f in C2.items():
        c2 = json.loads((CERTS / f).read_text())["derived"]
        g = c2["gram_primitive_even"]
        n = c2["derived_2n_from_cusp_unipotent"] // 2 if "derived_2n_from_cusp_unipotent" in c2 else abs(int(sp.Matrix(g).det())) // 2
        res["generic"][fam] = generic_check(n, g, c2["signature"]) | {"source_certificate": f}
    loci = json.loads((CERTS / "TW2_RHO20_LOCI.json").read_text())["result"]["model_checks"]
    cm = json.loads((CERTS / "CM_POINTS_RHO20.json").read_text())["families"]["cooper_s7"]["locus_hits"]
    for z in ("1/27", "-1", "infinity"):
        J = Fraction(loci[z]["J"])
        j = 1728 * J
        if j.denominator != 1:
            raise Refuse(f"j not integral at {z}: {j}")
        Ds = order_for_j(int(j))
        if len(Ds) != 1:
            raise Refuse(f"j = {j} at z = {z} matched {Ds} class-number-one orders")
        t = T_of_ExE(Ds[0])
        row = cm[z][0]
        res["rho20_cooper_s7"][z] = {"j_from_model": int(j), "cm_discriminant_by_computation": Ds[0], **t,
                                    "certified_T_reduced_abc": row["T_X_reduced_form_abc"], "certified_D": row["D"],
                                    "agree": t["T_reduced_abc"] == row["T_X_reduced_form_abc"] and t["disc"] == row["D"]}
    res["all_generic_isometric"] = all(v["verdict"] == "ISOMETRIC_TO_CERTIFIED_T" for v in res["generic"].values())
    res["all_rho20_agree"] = all(v["agree"] for v in res["rho20_cooper_s7"].values())
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    res = run()
    for fam, v in res["generic"].items():
        print(f"{fam}: n = {v['n']}, NS sig {v['NS_signature']}, saturated {v['NS_saturated']}, T det {v.get('T_det')}, "
              f"T sig {v.get('T_signature')} -> {v['verdict']}")
    for z, v in res["rho20_cooper_s7"].items():
        print(f"cooper_s7 z = {z}: j = {v['j_from_model']} -> D = {v['cm_discriminant_by_computation']}; T(ExE) {v['T_reduced_abc']} "
              f"vs certified {v['certified_T_reduced_abc']} -> {'AGREE (forced)' if v['agree'] else 'DISAGREE'}")
    ok = res["all_generic_isometric"] and res["all_rho20_agree"]
    if a.emit:
        cert = {"certificate": "K3xT2_READING_S", "checker": "checkers/check_K3xT2_reading_S.py",
                "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "date": "2026-10-08",
                "ruling": "D29' (2026-10-08, on T0's behalf under explicit delegation): Reading S adopted for selection criteria",
                "tier": "B (exact lattice computation from first principles; the Shioda-Inose isometry T(X) ~= T(E x E') is Tier L, "
                        "Kumar-Kuwata Remark 2.2; identification of the family member with an Inose surface is Tier B via "
                        "INOSE_MODEL_M7 for cooper_s7 only)",
                "replaces_citation": "Morrison 1984 (Invent. Math. 75, doi:10.1007/BF01403093) for T(E x E') = U + <2n>: computed here, not fetched",
                "assumption_not_computed": "E, E' without CM in the generic part, so Hom(E, E') ~= Z and rho(E x E') = 3",
                "result": res,
                "not_claimed": ["any physical reading of K3 x T^2: a compactification's T^2 is not identified with E or E' (Tier C)",
                                "corroboration: the rho = 20 agreement is forced by Shioda-Inose (ledger item 8)",
                                "cooper_s10 at rho = 20 (no explicit Inose model; D = -20 row needs E x E' with E !~= E')",
                                "T3 as a hard gate, a K3_CRITERIA.md edit, or any scoring (proposal decisions 2-4 remain open)",
                                "any ranking of cooper_s7 against cooper_s10"],
                "generated_by": "Claude (Opus 5.5), Stream 2, 2026-10-08",
                "verified_by": "checkers/test_K3xT2_reading_S_controls.py", "reviewed_by": "N"}
        OUT.write_text(json.dumps(cert, indent=2) + "\n")
        print("wrote", OUT)
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refuse as e:
        print("REFUSED:", e)
        sys.exit(2)
