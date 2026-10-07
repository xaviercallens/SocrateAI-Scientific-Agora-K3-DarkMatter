#!/usr/bin/env python3
"""check_TW2_sqrt_m7_endomorphism.py -- WP-TW2 step 2b-i: the degree-7 endomorphism sqrt(-7) of the
elliptic curve at the cooper_s7 locus z = 1/27, exhibited exactly over Q and verified.

Step 2a (TW2_RHO20_LOCI.json) found that at z = 1/27 (D = -28, T = <2>+<14>) the Shioda-Inose partner
is E x E with End(E) = Z[sqrt(-7)] and the rank-1 Mordell-Weil generator has height 14 = 2 * deg,
i.e. it is the section attached to the degree-7 endomorphism sqrt(-7). This checker exhibits that
endomorphism's x-coordinate map explicitly:

  1. j is READ from INOSE_FIBRATION_MULTIPLICITIES.json (locus 1/27), never typed; a Q-model
     y^2 = x^3 + A x + B with that j is built (A = 3j(1728-j), B = 2j(1728-j)^2) and twisted down.
  2. The 7-division polynomial psi_7 (degree 24) is factored over Q: exactly one cubic factor h(x)
     appears -- the kernel polynomial of the unique Galois-stable subgroup of order 7, ker(sqrt(-7)).
  3. Velu's formulas (symmetric-function form, exact power sums of the roots of h -- no numerics):
     phi_x(x) = x + sum_Q [ t_Q/(x - x_Q) + u_Q/(x - x_Q)^2 ],  t_Q = 2(3x_Q^2 + A),  u_Q = 4(x_Q^3 + A x_Q + B),
     codomain (A', B') = (A - 5t, B - 7w) (Velu/Kohel).
  4. Verifications: deg phi_x = 7 (num 7, den 6 = h^2); j(A', B') = j (the codomain is E up to
     isomorphism); the isomorphism constant c^2 is the unique root with (c^2)^2 = A/A' and
     (c^2)^3 = B/B' (it is -1/7: the endomorphism is defined over Q(sqrt(-7)), its x-map over Q);
     and the decisive identity  psi(psi(x)) = x([7]P)  with psi = c^2 phi_x, checked EXACTLY at
     N random rational points -- two rational functions of degree <= 49 that agree at more than 49
     points are equal, so this is a proof of phi o phi = [-7] on x-coordinates, hence of
     phi = +/- sqrt(-7).

NOT CLAIMED: the section on the K3 (that is step 2b-ii: Kumar-Kuwata (3.1)-(3.3) descent); anything
about the surface's fibres beyond step 2a; anything physical. The curve is the elliptic factor of the
Shioda-Inose partner, not the K3; nothing here is a Kodaira label (ledger items 3, 10).

Usage: python3 checkers/check_TW2_sqrt_m7_endomorphism.py [--emit] [--points N]
Controls: checkers/test_TW2_sqrt_m7_endomorphism_controls.py

Generated-by: Claude (Fable 5.1), Stream 2, 2026-10-07 | Verified-by: controls; the exact composition identity |
Reviewed-by: N
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parent.parent
CERTS = REPO / "data" / "certificates"
CERT = CERTS / "TW2_SQRT_M7_ENDOMORPHISM.json"
x, y, z = sp.symbols("x y z")


class Refuse(RuntimeError):
    pass


def read_j(locus="1/27"):
    fib = json.loads((CERTS / "INOSE_FIBRATION_MULTIPLICITIES.json").read_text())["result"]
    return sp.Integer(fib["T5_s7_loci"][locus]["j"])


def model_from_j(j):
    if j in (0, 1728):
        raise Refuse("j in {0, 1728}: the generic model A = 3j(1728-j), B = 2j(1728-j)^2 degenerates")
    A0, B0 = 3 * j * (1728 - j), 2 * j * (1728 - j) ** 2
    u = sp.Integer(1)
    fB = sp.factorint(B0)
    for p_, e in sp.factorint(A0).items():
        u *= p_ ** min(e // 4, fB.get(p_, 0) // 6)
    A, B = A0 // u ** 4, B0 // u ** 6
    assert sp.Rational(1728 * 4 * A ** 3, 4 * A ** 3 + 27 * B ** 2) == j
    return A, B


def division_polys(n_max, A, B):
    psi = {0: sp.Integer(0), 1: sp.Integer(1), 2: 2 * y, 3: 3 * x ** 4 + 6 * A * x ** 2 + 12 * B * x - A ** 2,
           4: 4 * y * (x ** 6 + 5 * A * x ** 4 + 20 * B * x ** 3 - 5 * A ** 2 * x ** 2 - 4 * A * B * x - 8 * B ** 2 - A ** 3)}
    for n in range(5, n_max + 1):
        m = n // 2
        psi[n] = (psi[m + 2] * psi[m] ** 3 - psi[m - 1] * psi[m + 1] ** 3) if n % 2 else \
            sp.cancel((psi[m] / (2 * y)) * (psi[m + 2] * psi[m - 1] ** 2 - psi[m - 2] * psi[m + 1] ** 2))
        psi[n] = sp.expand(sp.expand(psi[n]).subs(y ** 2, x ** 3 + A * x + B))
    return psi


def kernel_cubic(psi7):
    cubics = [sp.Poly(f, x).monic() for f, m in sp.factor_list(psi7)[1] if sp.degree(f, x) == 3]
    if len(cubics) != 1:
        raise Refuse(f"psi_7 has {len(cubics)} rational cubic factors; need exactly one (a unique Galois-stable 7-subgroup)")
    return cubics[0]


def power_sums(hp, kmax):
    n = hp.degree()
    c = hp.all_coeffs()
    e = [sp.Integer(1)] + [(-1) ** i * c[i] for i in range(1, n + 1)]
    p = [sp.Integer(n)]
    for k in range(1, kmax + 1):
        s = (sum((-1) ** (i - 1) * e[i] * p[k - i] for i in range(1, k)) + (-1) ** (k - 1) * k * e[k]) if k <= n \
            else sum((-1) ** (i - 1) * e[i] * p[k - i] for i in range(1, n + 1))
        p.append(sp.expand(s))
    return p


def root_sum(Tpoly, hp):
    """exact sum_Q T(x_Q)/(x - x_Q) over the roots x_Q of hp."""
    T = sp.Poly(Tpoly, x)
    D = sp.Poly(sp.cancel((T.as_expr() - T.as_expr().subs(x, z)) / (x - z)), x, z)
    p = power_sums(hp, D.degree(z))
    S = sum(coeff * x ** i * p[k] for (i, k), coeff in D.terms())
    return sp.cancel(T.as_expr() * sp.diff(hp.as_expr(), x) / hp.as_expr() - S)


def velu(A, B, h):
    S_T = root_sum(2 * (3 * x ** 2 + A), h)
    S_U = root_sum(4 * (x ** 3 + A * x + B), h)
    phi_x = sp.cancel(x + S_T - sp.diff(S_U, x))
    p = power_sums(h, 3)
    t = sp.expand(2 * (3 * p[2] + A * p[0]))
    w = sp.expand(4 * (p[3] + A * p[1] + B * p[0]) + 2 * (3 * p[3] + A * p[1]))
    return phi_x, (A - 5 * t, B - 7 * w)


def iso_constant(A, B, A2, B2):
    for s in (1, -1):
        c2 = s * sp.sqrt(sp.Rational(A, A2))
        if sp.simplify(c2 ** 3 - sp.Rational(B, B2)) == 0 and sp.simplify(c2 ** 2 - sp.Rational(A, A2)) == 0:
            return sp.nsimplify(c2)
    raise Refuse("no isomorphism constant c^2 with (c^2)^2 = A/A' and (c^2)^3 = B/B': the codomain is not isomorphic to E")


def run(j=None, n_points=60):
    j = read_j() if j is None else j
    A, B = model_from_j(j)
    psi = division_polys(8, A, B)
    # x([7]P) = x - psi_6 psi_8 / psi_7^2 ; psi_6 psi_8 contains y^2, eliminated by the curve equation
    pe6_8 = sp.expand(sp.expand(psi[6] * psi[8]).subs(y ** 2, x ** 3 + A * x + B))
    h = kernel_cubic(psi[7])
    phi_x, (A2, B2) = velu(A, B, h)
    num, den = sp.fraction(phi_x)
    degs = (int(sp.degree(num, x)), int(sp.degree(den, x)))
    if degs != (7, 6):
        raise Refuse(f"phi_x has degrees {degs}, expected (7, 6)")
    den_is_h2 = sp.simplify(sp.Poly(den, x).monic().as_expr() - h.as_expr() ** 2) == 0
    j2 = sp.Rational(1728 * 4 * A2 ** 3, 4 * A2 ** 3 + 27 * B2 ** 2)
    if j2 != j:
        raise Refuse(f"codomain j = {j2} != j: not an endomorphism")
    c2 = iso_constant(A, B, A2, B2)
    # composition: use psi6*psi8 reduced (y eliminated) and psi7
    rng = random.Random(7)
    ok = tried = 0
    for _ in range(n_points):
        x0 = sp.Rational(rng.randint(-10 ** 6, 10 ** 6), rng.randint(1, 10 ** 3))
        try:
            v1 = c2 * num.subs(x, x0) / den.subs(x, x0)
            v2 = c2 * num.subs(x, v1) / den.subs(x, v1)
            rhs = x0 - pe6_8.subs(x, x0) / psi[7].subs(x, x0) ** 2
            tried += 1
            ok += int(sp.simplify(v2 - rhs) == 0)
        except ZeroDivisionError:
            continue
    return {"j": str(j), "model": {"A": str(A), "B": str(B)}, "kernel_cubic": str(h.as_expr()),
            "phi_x": {"num": str(num), "den": str(den), "degrees": list(degs), "den_is_kernel_cubic_squared": den_is_h2},
            "codomain": {"A2": str(A2), "B2": str(B2), "j_equal": True, "c2": str(c2)},
            "composition_phi_phi_equals_minus7": {"agreements": ok, "points": tried, "degree_bound": 49,
                                                   "is_identity": ok == tried and tried > 49}}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--points", type=int, default=60)
    a = ap.parse_args(argv)
    res = run(n_points=a.points)
    print(f"j = {res['j']} (read from INOSE_FIBRATION_MULTIPLICITIES.json, locus 1/27); model A = {res['model']['A']}, B = {res['model']['B']}")
    print(f"kernel cubic of sqrt(-7): {res['kernel_cubic']}")
    print(f"phi_x degrees {res['phi_x']['degrees']}, denominator = h^2: {res['phi_x']['den_is_kernel_cubic_squared']}; codomain isomorphic to E with c^2 = {res['codomain']['c2']}")
    cc = res["composition_phi_phi_equals_minus7"]
    print(f"phi o phi = [-7] on x-coordinates: {cc['agreements']}/{cc['points']} exact agreements (identity: {cc['is_identity']})")
    ok = cc["is_identity"] and res["phi_x"]["den_is_kernel_cubic_squared"]
    print("PASS: sqrt(-7) exhibited" if ok else "FAIL")
    if a.emit and ok:
        cert = {"checker": "checkers/check_TW2_sqrt_m7_endomorphism.py", "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "work_package": "WP-TW2 step 2b-i (D23', 2026-10-07)",
                "tier": "A-style exact computation (Velu's formulas over Q, identity verified at > degree-bound many rational points); the link to the K3 section is Tier B via step 2a",
                "result": res,
                "not_claimed": ["the section on the K3 itself (step 2b-ii, Kumar-Kuwata (3.1)-(3.3) descent, not done)",
                                "anything about fibres of the K3 beyond step 2a; no Kodaira label anywhere",
                                "the sign of the endomorphism (phi = +/- sqrt(-7); x-coordinates do not see it)",
                                "any physical statement (ledger item 4)"],
                "generated_by": "Claude (Fable 5.1), Stream 2, 2026-10-07", "verified_by": "checkers/test_TW2_sqrt_m7_endomorphism_controls.py", "reviewed_by": "N"}
        CERT.write_text(json.dumps(cert, indent=2) + "\n")
        print("wrote", CERT)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
