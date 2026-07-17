#!/usr/bin/env python3
"""
check_C3b_moduli_map.py — C3b criterion checker (K3_CRITERIA.md, EXECUTION_PLAN.md S2-01b).

For a (bulk = order-3, brane = order-2) candidate pair, this checker:

  1. Loads the pair's holonomic recurrences from refs/ (literature transcriptions only —
     no value in this file or its output originates from model memory).
  2. Extracts the shift-recurrence polynomials C(k) a_{k+1} = A(k) a_k + B(k) a_{k-1}
     symbolically from the frozen recurrence string (done once; the generation loop uses
     only the extracted polynomials, evaluated in exact rational arithmetic).
  3. VALIDATES the MUM hypothesis: C(k) must equal (k+1)^order exactly (maximally
     unipotent monodromy at z=0 — required for the mirror map to exist in the form used).
  4. Generates N terms exactly and checks integrality (a mistranscribed Apéry-like
     recurrence generically fails integrality within a few terms).
  5. Builds the Frobenius solutions at the MUM point: y0 = Σ a_n z^n and
     y1 = y0·log z + Σ a'_n z^n, where a'_n comes from the ρ-differentiated recurrence
     (a_n(ρ) with k → k+ρ; a'_n = ∂ρ a_n |_{ρ=0}).
  6. Computes each mirror map q = z·exp((y1/y0) − log z) and inverts it to z(q)
     (exact series reversion).
  7. Searches for a polynomial relation P(z_bulk(q^{m_b}), z_brane(q^{m_e})) = 0 over ℚ
     by exact nullspace computation, over a declared hypothesis grid, and re-validates
     any found relation at higher truncation order (falsifiability of the fit itself).
  8. Emits a certificate JSON embedding the ref SHA256, all parameters, and the relation.

Checker contract (K3_CRITERIA.md §3): exact arithmetic, no network, no LLM calls,
deterministic — identical inputs give bit-identical certificates.
"""

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp

CHECKER_VERSION = "1.0.0"
REPO_ROOT = Path(__file__).resolve().parent.parent


# ----------------------------------------------------------------------------
# Recurrence extraction (symbolic, once per sequence)
# ----------------------------------------------------------------------------

class _SpShim:
    """Namespace shim so the frozen recurrence strings (which call sp.Rational on a
    polynomial in k) can be evaluated with a *symbolic* k for polynomial extraction."""
    @staticmethod
    def Rational(x):
        return sp.sympify(x)


def extract_recurrence_polys(recurrence_python, order):
    """Return (A, B, C) as sympy Polys in k, where C(k) a_{k+1} = A(k) a_k + B(k) a_{k-1}."""
    k = sp.Symbol("k")
    s_prev1, s_prev2 = sp.Symbol("S_k"), sp.Symbol("S_km1")
    expr = eval(recurrence_python, {"__builtins__": {}},
                {"sp": _SpShim, "k": k, "s": [s_prev2, s_prev1]})
    expr = sp.together(sp.expand(sp.sympify(expr)))
    numer, denom = sp.fraction(expr)
    numer = sp.expand(numer)
    A = sp.expand(numer.coeff(s_prev1))
    B = sp.expand(numer.coeff(s_prev2))
    if sp.expand(numer - A * s_prev1 - B * s_prev2) != 0:
        raise ValueError("recurrence string is not linear in (s[-1], s[-2])")
    C = sp.expand(denom)
    mum_ok = sp.expand(C - (k + 1) ** order) == 0
    return sp.Poly(A, k), sp.Poly(B, k), sp.Poly(C, k), mum_ok


def poly_at(poly, kval):
    """Evaluate a sympy Poly at an integer, returning Fraction."""
    v = poly.eval(sp.Integer(kval))
    return Fraction(int(sp.numer(v)), int(sp.denom(v)))


# ----------------------------------------------------------------------------
# Exact sequence + Frobenius derivative generation
# ----------------------------------------------------------------------------

def generate_sequence(A, B, C, initial_terms, n_terms):
    """Generate a_0..a_{n_terms-1} exactly. Returns (list[Fraction], integral: bool)."""
    a = [Fraction(t) for t in initial_terms]
    while len(a) < n_terms:
        k = len(a) - 1
        nxt = (poly_at(A, k) * a[-1] + poly_at(B, k) * a[-2]) / poly_at(C, k)
        a.append(nxt)
    integral = all(x.denominator == 1 for x in a)
    return a, integral


def frobenius_derivative(A, B, C, a, n_terms):
    """a'_n = ∂ρ a_n(ρ)|_0 from the ρ-differentiated recurrence, a'_0 = 0, a_{-1} ≡ 0."""
    Ad, Bd, Cd = A.diff(), B.diff(), C.diff()
    ad = [Fraction(0)]
    for n in range(1, n_terms):
        k = n - 1
        am1 = a[k]                       # a_{k}
        am2 = a[k - 1] if k >= 1 else Fraction(0)
        adm1 = ad[k]
        adm2 = ad[k - 1] if k >= 1 else Fraction(0)
        rhs = (poly_at(Ad, k) * am1 + poly_at(A, k) * adm1
               + poly_at(Bd, k) * am2 + poly_at(B, k) * adm2
               - poly_at(Cd, k) * a[n])
        ad.append(rhs / poly_at(C, k))
    return ad


# ----------------------------------------------------------------------------
# Exact power-series toolkit (lists of Fraction, index = power)
# ----------------------------------------------------------------------------

def ser_mul(f, g, N):
    out = [Fraction(0)] * N
    for i, fi in enumerate(f[:N]):
        if fi == 0:
            continue
        for j, gj in enumerate(g[:N - i]):
            if gj != 0:
                out[i + j] += fi * gj
    return out


def ser_div(f, g, N):
    """f/g with g[0] != 0."""
    assert g[0] != 0
    out = [Fraction(0)] * N
    for n in range(N):
        acc = f[n] if n < len(f) else Fraction(0)
        for j in range(1, n + 1):
            gj = g[j] if j < len(g) else Fraction(0)
            acc -= gj * out[n - j]
        out[n] = acc / g[0]
    return out


def ser_exp(h, N):
    """exp(h) with h[0] == 0, via E' = h'·E."""
    assert h[0] == 0
    E = [Fraction(0)] * N
    E[0] = Fraction(1)
    for n in range(1, N):
        acc = Fraction(0)
        for j in range(1, n + 1):
            hj = h[j] if j < len(h) else Fraction(0)
            acc += j * hj * E[n - j]
        E[n] = acc / n
    return E


def ser_compose(f, g, N):
    """f(g(q)) with g[0] == 0 (Horner in series arithmetic)."""
    assert g[0] == 0
    out = [Fraction(0)] * N
    for c in reversed(f[:N]):
        out = ser_mul(out, g, N)
        out[0] += c
    return out


def ser_revert(q_of_z, N):
    """Invert q = z + c2 z² + ... to z = q + d2 q² + ... (coefficient matching)."""
    assert q_of_z[0] == 0 and q_of_z[1] == 1
    z = [Fraction(0)] * N
    z[1] = Fraction(1)
    for m in range(2, N):
        err = ser_compose(q_of_z, z, m + 1)[m]
        z[m] = -err
    return z


def ser_scale_powers(f, m, N):
    """f(q^m) truncated to N."""
    out = [Fraction(0)] * N
    for i, c in enumerate(f):
        if i * m < N:
            out[i * m] = c
    return out


# ----------------------------------------------------------------------------
# Mirror map
# ----------------------------------------------------------------------------

def mirror_map_z_of_q(a, ad, N):
    """From y0 = Σ a_n z^n, y1 = y0 log z + Σ a'_n z^n:
    q = z·exp(g/y0) with g = Σ a'_n z^n; return z(q) to order N."""
    g_over_y0 = ser_div(ad[:N], a[:N], N)
    assert g_over_y0[0] == 0
    E = ser_exp(g_over_y0, N)
    q_of_z = [Fraction(0)] * N          # z·E
    for i in range(N - 1):
        q_of_z[i + 1] = E[i]
    return ser_revert(q_of_z, N)


# ----------------------------------------------------------------------------
# Algebraic relation search (exact nullspace)
# ----------------------------------------------------------------------------

def relation_search(zb, ze, deg_x, deg_y, n_rows):
    """Find nonzero P(x,y) = Σ p_ij x^i y^j (0≤i≤deg_x, 0≤j≤deg_y, (i,j)≠(0,0))
    with P(zb(q), ze(q)) ≡ 0 mod q^n_rows. Returns list of ((i,j), int) or None."""
    N = n_rows
    xpow = [[Fraction(1)] + [Fraction(0)] * (N - 1)]
    for _ in range(deg_x):
        xpow.append(ser_mul(xpow[-1], zb, N))
    ypow = [[Fraction(1)] + [Fraction(0)] * (N - 1)]
    for _ in range(deg_y):
        ypow.append(ser_mul(ypow[-1], ze, N))

    monomials = [(i, j) for i in range(deg_x + 1) for j in range(deg_y + 1)
                 if (i, j) != (0, 0)]
    cols = [ser_mul(xpow[i], ypow[j], N) for (i, j) in monomials]

    M = sp.Matrix(N, len(monomials),
                  lambda r, c: sp.Rational(cols[c][r].numerator, cols[c][r].denominator))
    null = M.nullspace()
    if not null:
        return None
    vec = null[0]
    denoms = [sp.denom(v) for v in vec]
    lcm = sp.ilcm(*[int(d) for d in denoms]) if len(denoms) > 1 else int(denoms[0])
    ints = [int(v * lcm) for v in vec]
    g = 0
    for v in ints:
        g = sp.igcd(g, v)
    if g > 1:
        ints = [v // g for v in ints]
    return [(monomials[idx], ints[idx]) for idx in range(len(monomials)) if ints[idx] != 0]


def relation_holds(relation, zb, ze, N):
    acc = [Fraction(0)] * N
    xpow_cache, ypow_cache = {0: [Fraction(1)] + [Fraction(0)] * (N - 1)}, \
                             {0: [Fraction(1)] + [Fraction(0)] * (N - 1)}
    def _pow(cache, base, p):
        if p not in cache:
            cache[p] = ser_mul(_pow(cache, base, p - 1), base, N)
        return cache[p]
    for (i, j), c in relation:
        term = ser_mul(_pow(xpow_cache, zb, i), _pow(ypow_cache, ze, j), N)
        for n in range(N):
            acc[n] += c * term[n]
    return all(v == 0 for v in acc)


def relation_str(relation):
    parts = []
    for (i, j), c in relation:
        mono = ("" if i == 0 else ("x" if i == 1 else f"x^{i}")) + \
               ("" if j == 0 else ("y" if j == 1 else f"y^{j}"))
        parts.append(f"{'+' if c > 0 else '-'} {abs(c)}{'*' + mono if mono else ''}")
    s = " ".join(parts).lstrip("+ ")
    return f"{s} = 0   (x = z_bulk, y = z_brane)"


# ----------------------------------------------------------------------------
# Main check
# ----------------------------------------------------------------------------

def run_check(refs_path, bulk_id, brane_id, n_terms=28, validate_extra=8,
              max_bidegree=4, power_hypotheses=((1, 1), (1, 2), (2, 1))):
    refs_raw = Path(refs_path).read_bytes()
    refs_sha = hashlib.sha256(refs_raw).hexdigest()
    refs = json.loads(refs_raw)

    result = {
        "checker": "check_C3b_moduli_map.py",
        "checker_version": CHECKER_VERSION,
        "criterion": "C3b (moduli map: algebraic relation between bulk and brane mirror maps)",
        "refs_file": str(refs_path),
        "refs_sha256": refs_sha,
        "pair": {"bulk": bulk_id, "brane": brane_id},
        "parameters": {"n_terms": n_terms, "validate_extra": validate_extra,
                       "max_bidegree": max_bidegree,
                       "power_hypotheses": [list(p) for p in power_hypotheses]},
        "sequences": {},
    }

    zq = {}
    for sid, role in ((bulk_id, "bulk"), (brane_id, "brane")):
        entry = refs["sequences"].get(sid)
        if entry is None:
            result["verdict"] = "ERROR_UNKNOWN_SEQUENCE"
            result["error"] = f"sequence '{sid}' not in refs file"
            return result, 2
        if entry.get("status", "OK") != "OK" and entry.get("_meta_status") == "BLOCKED":
            result["verdict"] = "REFUSED_NO_DATA"
            result["error"] = ("transcribe from fetched sources — no values from model memory")
            return result, 2
        order = {"order-2": 2, "order-3": 3}[entry["type"]]
        A, B, C, mum_ok = extract_recurrence_polys(entry["recurrence_python"], order)
        a, integral = generate_sequence(A, B, C, entry["initial_terms"],
                                        n_terms + validate_extra)
        seq_report = {
            "source": entry["source"],
            "order": order,
            "extracted_polynomials": {"A": str(A.as_expr()), "B": str(B.as_expr()),
                                      "C": str(C.as_expr())},
            "mum_validated": bool(mum_ok),
            "first_terms": [str(x) for x in a[:12]],
            "integrality": f"PASS({n_terms + validate_extra})" if integral else "FAIL",
        }
        result["sequences"][role] = seq_report
        if not mum_ok:
            result["verdict"] = "FAIL_MUM"
            return result, 1
        if not integral:
            result["verdict"] = "FAIL_INTEGRALITY"
            return result, 1
        ad = frobenius_derivative(A, B, C, a, n_terms + validate_extra)
        zq[role] = mirror_map_z_of_q(a, ad, n_terms + validate_extra)
        seq_report["mirror_map_z_of_q_first_terms"] = [str(x) for x in zq[role][:8]]

    # Relation search over the declared hypothesis grid.
    searches = []
    found = None
    for (mb, me) in power_hypotheses:
        zb = ser_scale_powers(zq["bulk"], mb, n_terms)
        ze = ser_scale_powers(zq["brane"], me, n_terms)
        for d in range(1, max_bidegree + 1):
            rel = relation_search(zb, ze, d, d, n_terms)
            rec = {"hypothesis_q_powers": [mb, me], "bidegree": [d, d],
                   "truncation_order": n_terms}
            if rel is not None:
                zb_v = ser_scale_powers(zq["bulk"], mb, n_terms + validate_extra)
                ze_v = ser_scale_powers(zq["brane"], me, n_terms + validate_extra)
                validated = relation_holds(rel, zb_v, ze_v, n_terms + validate_extra)
                rec["relation"] = relation_str(rel)
                rec["validated_to_order"] = (n_terms + validate_extra) if validated \
                    else f"FAILED_AT_VALIDATION({n_terms + validate_extra})"
                searches.append(rec)
                if validated:
                    found = rec
                    break
            else:
                rec["relation"] = None
                searches.append(rec)
        if found:
            break

    result["relation_search"] = searches
    if found:
        result["verdict"] = f"C3B_RELATION_FOUND(validated to q^{n_terms + validate_extra})"
        result["relation"] = found["relation"]
        code = 0
    else:
        result["verdict"] = (f"C3B_NOT_FOUND(n_terms={n_terms}, "
                             f"max_bidegree={max_bidegree}, "
                             f"hypotheses={[list(p) for p in power_hypotheses]})")
        code = 1
    return result, code


def main():
    ap = argparse.ArgumentParser(description="C3b moduli-map checker")
    ap.add_argument("--refs", default=str(REPO_ROOT / "refs" / "recurrences_v1.json"))
    ap.add_argument("--bulk", default="cooper_s10")
    ap.add_argument("--brane", default="zagier_A")
    ap.add_argument("--n-terms", type=int, default=28)
    ap.add_argument("--max-bidegree", type=int, default=4)
    ap.add_argument("--out", default=None, help="certificate output path")
    args = ap.parse_args()

    result, code = run_check(args.refs, args.bulk, args.brane,
                             n_terms=args.n_terms, max_bidegree=args.max_bidegree)
    result["provenance"] = ("Generated-by: checkers/check_C3b_moduli_map.py "
                            f"v{CHECKER_VERSION} | Verified-by: exact arithmetic, "
                            "self-validated relation | Reviewed-by: pending")
    payload = json.dumps(result, indent=2, sort_keys=True)
    out = args.out or str(REPO_ROOT / "data" / "certificates" /
                          f"C3b_{args.bulk}__{args.brane}.json")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(payload + "\n")
    print(payload)
    print(f"\ncertificate written: {out}", file=sys.stderr)
    sys.exit(code)


if __name__ == "__main__":
    main()
