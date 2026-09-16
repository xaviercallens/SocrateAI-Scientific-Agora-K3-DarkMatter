#!/usr/bin/env python3
"""A112029 = sum_k C(n+k,k)^2 (and the other order-3 sieve survivors) — analytic check (EXPLORATORY SANDBOX, CLAUDE.md rule 7; non-citable).

Same kind of check T0 set for A079727 (2026-09-16): is this new K3-type geometry, or
explained by a known structure? No G1-2/G1-3/G1-4 gate is run.
  1. exact minimal ODE (reuses the unmodified phase_a_scan classifier routines)
  2. cross-check OEIS recurrence (Kotesovec 2012, live oeis.org fetch 2026-09-16)
  3. singular points + local exponents (Frobenius indicial roots) at each one, incl. z=0 (MUM?)
  4. symmetric-square test: L3 = Sym^2(L2) for some order-2 L2 over Q(z)
  5. negative/positive controls for test 4: Apery zeta(3) A005259 (known Sym^2) and cooper_s10 A005260
Writes data/autoresearch_v2/a112029_analytic_check_2026_09_16.json before printing.
"""
import json, math, os, sys
import sympy as sp
SCRIPTS = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, SCRIPTS)
from autoresearch_v2_phase_a_scan import ode_rows, exact_nullspace_vector, ode_validate, find_ode
from r2_overnight_sweep_2026_09_16 import seq_2factor
OUT = os.path.join(os.path.dirname(SCRIPTS), "data", "autoresearch_v2", "a112029_analytic_check_2026_09_16.json")
z = sp.symbols("z"); NMAX = 160

def seqs():
    return {
        "A112029": [sum(math.comb(n + k, k) ** 2 for k in range(n + 1)) for n in range(NMAX + 1)],
        "A005259_control": seq_2factor(2, 2, NMAX),
        "A005260_control": [sum(math.comb(n, k) ** 4 for k in range(n + 1)) for n in range(NMAX + 1)],
        # the other order-3 sieve survivors (LR-3 2026-09-16 + overnight sweep), same check
        "A036917": [sum(math.comb(2*k, k) ** 2 * math.comb(2*n - 2*k, n - k) ** 2 for k in range(n + 1)) for n in range(NMAX + 1)],
        "A079727_T003": [sum(math.comb(2*k, k) ** 3 for k in range(n + 1)) for n in range(NMAX + 1)],
        "unlisted_T011": [sum(math.comb(n + k, k) * math.comb(2*k, k) for k in range(n + 1)) for n in range(NMAX + 1)],
        "A274789_T112": [sum(math.comb(n, k) * math.comb(n + k, k) * math.comb(2*k, k) ** 2 for k in range(n + 1)) for n in range(NMAX + 1)],
    }

def operator(u):
    o = find_ode(u, NMAX)
    rho, delta = o["ode_order"], o["ode_degree"]
    nrows = (rho + 1) * (delta + 1) + 12
    vec = exact_nullspace_vector(ode_rows(u, rho, delta, nrows), (rho + 1) * (delta + 1))
    assert ode_validate(u, rho, delta, vec, nrows, NMAX - rho - delta)
    q = [sp.expand(sum(sp.Rational(vec[j * (delta + 1) + m]) * z ** m for m in range(delta + 1)))
         for j in range(rho + 1)]
    g = sp.gcd_list(q)
    return o, [sp.factor(sp.cancel(x / g)) for x in q]

def local_exponents(q, pt):
    # indicial polynomial at z=pt for sum_j q_j(z) d^j (regular singular assumed; recorded if not)
    rho = len(q) - 1; t = sp.symbols("t"); s = sp.symbols("s")
    qq = [sp.expand(x.subs(z, t + pt)) for x in q]
    # order of vanishing shift: valuation of q_j minus (rho - j) ... Fuchs: min_j (ord q_j - j)
    ords = [sp.Poly(x, t).monoms()[-1][0] if x != 0 else 10**6 for x in qq]
    m = min(ords[j] - j for j in range(rho + 1))
    ind = 0
    for j in range(rho + 1):
        if ords[j] - j == m:
            lc = sp.Poly(qq[j], t).coeff_monomial(t ** ords[j])
            ind += lc * sp.ff(s, j)
    regular = ords[rho] - rho == m
    return {"regular_singular_top": bool(regular),
            "exponents": [str(r) for r in sp.roots(sp.Poly(sp.expand(ind), s), multiple=True)]}

def sym2_test(q):
    p3, p2, p1, p0 = [sp.cancel(x / q[3]) for x in (q[3], q[2], q[1], q[0])]
    a = p2 / 3
    b = sp.cancel((p1 - 2 * a ** 2 - sp.diff(a, z)) / 4)
    resid = sp.cancel(p0 - (4 * a * b + 2 * sp.diff(b, z)))
    return {"is_sym2": resid == 0, "residual": str(sp.factor(resid))[:300],
            "L2": {"a": str(sp.factor(a)), "b": str(sp.factor(b))}}

def main():
    out = {"label": "EXPLORATORY SANDBOX — not citable in Streams 1-3", "nmax": NMAX}
    S = seqs(); u = S["A112029"]
    # (2) OEIS recurrence cross-check, n = 2..NMAX
    ok = all(2*(2*n+1)*(21*n-13)*n**2*u[n] == (1365*n**4-1517*n**3+240*n**2+216*n-64)*u[n-1]
             - 4*(n-1)*(2*n-1)**2*(21*n+8)*u[n-2] for n in range(2, NMAX + 1))
    out["oeis_recurrence_holds_n2_to_nmax"] = ok
    for name, seq in S.items():
        o, q = operator(seq)
        lead = sp.Poly(q[-1], z)
        rts = sp.roots(lead, multiple=True)
        sing = sorted(set(rts), key=lambda r: sp.N(abs(r)))
        if len(rts) < lead.degree():
            print(f"   [{name}] note: only {len(rts)}/{lead.degree()} leading-coefficient roots solved in radicals")
        rec = {"ode": o, "q": [str(x) for x in q], "leading": str(sp.factor(q[-1])),
               "singular_points": [str(r) for r in sing],
               "exponents": {str(r): local_exponents(q, r) for r in sing},
               "sym2": sym2_test(q) if len(q) == 4 else None}
        out[name] = rec
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=str)
    print("OEIS recurrence holds:", ok)
    for name in S:
        r = out[name]
        print(f"\n== {name}: ODE {r['ode']['ode_order']},{r['ode']['ode_degree']}  leading {r['leading']}")
        for pt, e in r["exponents"].items():
            print(f"   z={pt}: exponents {e['exponents']} regular={e['regular_singular_top']}")
        print("   Sym^2:", r["sym2"]["is_sym2"], "| residual:", r["sym2"]["residual"][:120])

if __name__ == "__main__":
    main()
