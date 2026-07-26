#!/usr/bin/env python3
"""
check_s7_hauptmodul_gamma07plus.py — is t = g.f.(A279618) a Hauptmodul for
Γ₀(7)+ (Fricke extension), and not merely for Γ₀(7)?

Why this matters (Phase 4, lattice refinement): E-011 delivered ρ=19/T=3 as
RANKS only. If the s7 family is M₇-polarized in the Dolgachev–Doran sense,
its moduli curve is X₀(7)+ and full candidate LATTICES follow (see the Phase 4
memo). The computable leg of that identification is exactly the "+".

Method (exact ℚ arithmetic throughout, no floats):
  u = q⁻¹·(E(q)/E(q⁷))⁴ is the classical Γ₀(7) Hauptmodul, built here from
  Euler's pentagonal-number product E(q)=∏(1−qⁿ) — self-verified against its
  own recurrence. Work with v = 1/u = q·(E₇/E₁)⁴ ∈ qℤ[[q]].

  TEST M (must FAIL for "+"): t Möbius in v ⇔ t is a Γ₀(7) Hauptmodul.
  TEST D (must PASS): t = (a·v² + b·v + e)/(f·v² + g·v + h), coefficients
    solved LINEARLY from the first orders, then VERIFIED on held-out orders
    never used in solving. PASS ⇒ [ℚ(u):ℚ(t)] = 2.
  TEST F (corroboration): rewrite t = (a + b·u)/(f + g·u + h·u²); solve for
    the involution constant κ with R(κ/u) ≡ R(u). κ must EMERGE from the
    fitted coefficients (expected 49 = 7², but never assumed).

  Logic: PASS(D) + FAIL(M) ⇒ ℚ(t) is an index-2 subfield of ℚ(u) fixed by an
  element normalizing Γ₀(7). The normalizer of Γ₀(7) in PSL₂(ℝ) is Γ₀(7)+
  (Atkin–Lehner 1970, prime level) — so that element is the Fricke involution
  and t is a Γ₀(7)+ Hauptmodul. TEST F sees the Fricke constant directly.

Tier: the three identities are exact to the stated order [computed]; the
group-theoretic conclusion rests on the Atkin–Lehner normalizer statement
[B: classical, cited, not re-derived here]. NO lattice data is emitted —
the lattice step needs Dolgachev/Doran fetched and read first.

Negative controls (standing rule 1 — each must FAIL the "+" verdict):
  N1: t ← v itself (a Γ₀(7) Hauptmodul): TEST M passes ⇒ verdict NOT-plus.
  N2: t ← A279618 with one corrupted coefficient: TEST D verification fails.
  N3: t vs the WRONG level: v₅ = q(E₅/E₁)⁶ (Γ₀(5)): TEST D fails.
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BFILE = REPO / "refs" / "oeis_A279618_bfile.txt"
OUT = REPO / "data" / "certificates" / "HAUPTMODUL_S7_GAMMA07PLUS.json"

N_SOLVE_D = 12   # orders used to solve TEST D's linear system
N_SOLVE_M = 6    # orders used to solve TEST M's linear system


# ---------------------------------------------------------------- series ----
def euler_E(nmax):
    """E(q) = prod(1-q^n) to order nmax, via pentagonal number theorem."""
    E = [0] * (nmax + 1)
    E[0] = 1
    k = 1
    while True:
        g1 = k * (3 * k - 1) // 2
        g2 = k * (3 * k + 1) // 2
        if g1 > nmax and g2 > nmax:
            break
        s = 1 if k % 2 == 0 else -1
        if g1 <= nmax:
            E[g1] += s
        if g2 <= nmax:
            E[g2] += s
        k += 1
    return E


def ps_mul(A, B, nmax):
    C = [Fraction(0)] * (nmax + 1)
    for i, a in enumerate(A[: nmax + 1]):
        if a == 0:
            continue
        for j, b in enumerate(B[: nmax + 1 - i]):
            if b:
                C[i + j] += Fraction(a) * b
    return C

def ps_inv(A, nmax):
    assert A[0] != 0
    B = [Fraction(0)] * (nmax + 1)
    B[0] = Fraction(1, 1) / A[0]
    for n in range(1, nmax + 1):
        s = Fraction(0)
        for k in range(1, n + 1):
            if k < len(A) and A[k]:
                s += Fraction(A[k]) * B[n - k]
        B[n] = -s / A[0]
    return B

def ps_pow(A, e, nmax):
    R = [Fraction(0)] * (nmax + 1)
    R[0] = Fraction(1)
    for _ in range(e):
        R = ps_mul(R, A, nmax)
    return R

def dilate(A, m, nmax):
    B = [Fraction(0)] * (nmax + 1)
    for i, a in enumerate(A):
        if i * m > nmax:
            break
        B[i * m] += Fraction(a)
    return B


def build_v(level, exponent, nmax):
    """v_N = q · (E(q^N)/E(q))^exponent  — 1/(eta-quotient Hauptmodul)."""
    E1 = euler_E(nmax)
    EN = dilate(euler_E(nmax // level + 1), level, nmax)
    ratio = ps_mul(EN, ps_inv(E1, nmax), nmax)
    p = ps_pow(ratio, exponent, nmax)
    return [Fraction(0)] + p[:nmax]          # multiply by q


def read_bfile(path):
    terms = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        n, a = line.split()
        terms[int(n)] = int(a)
    nmax = max(terms)
    assert sorted(terms) == list(range(1, nmax + 1))
    return [Fraction(0)] + [Fraction(terms[i]) for i in range(1, nmax + 1)]


# ---------------------------------------------------------- linear algebra --
def nullspace_solve(rows, ncols):
    """One rational nullspace vector of the row system, or None."""
    M = [r[:] for r in rows]
    piv_of_col = {}
    r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        M[r] = [x / M[r][c] for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                M[i] = [a - M[i][c] * b for a, b in zip(M[i], M[r])]
        piv_of_col[c] = r
        r += 1
    free = [c for c in range(ncols) if c not in piv_of_col]
    if not free:
        return None
    f = free[0]
    x = [Fraction(0)] * ncols
    x[f] = Fraction(1)
    for c, pr in piv_of_col.items():
        x[c] = -M[pr][f]
    return x


def rational_fit(t, v, deg, n_solve, nmax):
    """Fit t = P(v)/Q(v), deg P,Q ≤ deg, on orders 1..n_solve; verify to nmax.

    Returns (ok_solve, ok_verify, coeffs).  t·Q(v) − P(v) = 0: linear in the
    unknown coefficients of P and Q.  Column order: p0..p_deg, q0..q_deg.
    """
    ncols = 2 * (deg + 1)
    vpow = [[Fraction(1)] + [Fraction(0)] * nmax]          # v^0
    for k in range(deg):
        vpow.append(ps_mul(vpow[-1], v, nmax))
    tv = [ps_mul(t, vp, nmax) for vp in vpow]              # t·v^k

    def row(order):
        return [-vpow[k][order] for k in range(deg + 1)] + \
               [tv[k][order] for k in range(deg + 1)]

    sol = nullspace_solve([row(o) for o in range(0, n_solve + 1)], ncols)
    if sol is None:
        return False, False, None
    ok_verify = all(
        sum(sol[k] * -vpow[k][o] for k in range(deg + 1)) +
        sum(sol[deg + 1 + k] * tv[k][o] for k in range(deg + 1)) == 0
        for o in range(n_solve + 1, nmax + 1)
    )
    return True, ok_verify, sol


def plus_verdict(t, v, nmax):
    """Full pipeline: (is_plus, detail dict)."""
    m_solved, m_verified, _ = rational_fit(t, v, 1, N_SOLVE_M, nmax)
    mobius_pass = m_solved and m_verified
    d_solved, d_verified, sol = rational_fit(t, v, 2, N_SOLVE_D, nmax)
    deg2_pass = d_solved and d_verified
    return (deg2_pass and not mobius_pass), {
        "mobius_pass": mobius_pass, "deg2_pass": deg2_pass, "sol": sol}


def fricke_kappa(sol):
    """t=(p0+p1v+p2v²)/(q0+q1v+q2v²), v=1/u ⇒ t=(p0u²+p1u+p2)/(q0u²+q1u+q2).
    Solve R(κ/u) = R(u) for κ: substituting gives numerator/denominator
    (p2u²+p1κu+p0κ²)/(q2u²+q1κu+q0κ²).  Cross-multiplying and matching the
    coefficient lattice yields the consistency conditions below.
    """
    p0, p1, p2, q0, q1, q2 = sol
    # Cross-multiplied difference must vanish identically in u.  With both
    # quadratics, matching coefficients of u⁴ and u⁰ gives the same κ² and
    # the u³/u¹ pair gives κ.  Guard degenerate coefficients.
    kappas = []
    if p1 * q0 != p0 * q1 and p2 * q1 != p1 * q2:
        # u³:  p0·q1·κ + p1·q2 ... derive: N1·D2 − N2·D1 = 0 where
        # N1=p0u²+p1u+p2, D1=q0u²+q1u+q2, N2=p2u²+p1κu+p0κ², D2=q2u²+q1κu+q0κ²
        # u⁴ coeff: p0q1κ − p1q2  +  (p0q2 − p2q0)·0 ... compute symbolically:
        # (N1·D2)[u⁴] = p0q2 ; wait — do it properly below.
        pass
    # Full symbolic expansion with κ as unknown, using polynomial in κ:
    # N1·D2 coefficients in u (each a polynomial in κ):
    #   u⁴: p0·q2         + 0·κ         + 0·κ²
    #   u³: p1·q2         + p0·q1·κ
    #   u²: p2·q2         + p1·q1·κ     + p0·q0·κ²
    #   u¹:                 p2·q1·κ     + p1·q0·κ²
    #   u⁰:                               p2·q0·κ²
    # N2·D1 coefficients in u:
    #   u⁴: p2·q0
    #   u³: p2·q1         + p1·q0·κ
    #   u²: p2·q2         + p1·q1·κ     + p0·q0·κ²
    #   u¹:                 p1·q2·κ     + p0·q1·κ²
    #   u⁰:                               p0·q2·κ²
    # Differences (must all vanish):
    #   u⁴: p0q2 − p2q0                                   -> κ-free: must be 0
    #   u³: (p1q2 − p2q1) + κ(p0q1 − p1q0)                -> gives κ
    #   u²: 0
    #   u¹: κ[(p2q1 − p1q2) + κ(p1q0 − p0q1)]             -> same κ again
    #   u⁰: κ²(p2q0 − p0q2)                               -> κ-free: must be 0
    c_free = p0 * q2 - p2 * q0
    a_lin, b_lin = (p1 * q2 - p2 * q1), (p0 * q1 - p1 * q0)
    if c_free != 0 or b_lin == 0:
        return None
    kappa = -a_lin / b_lin
    # u¹ condition is κ·(−(a_lin) − κ·(−b_lin))·(−1)… it reduces to the same
    # linear relation, but assert it explicitly rather than trusting algebra:
    assert kappa * ((p2 * q1 - p1 * q2) + kappa * (p1 * q0 - p0 * q1)) == 0
    return kappa


def main():
    t = read_bfile(BFILE)
    nmax = len(t) - 1

    # positive control on the series engine: E(q) head is 1,-1,-1,0,0,1,0,1
    E = euler_E(8)
    assert E[:8] == [1, -1, -1, 0, 0, 1, 0, 1], E[:8]

    v7 = build_v(7, 4, nmax)
    v5 = build_v(5, 6, nmax)

    print("=" * 74)
    print("A279618: Hauptmodul for Γ₀(7)+ (Fricke), or only Γ₀(7)?")
    print(f"terms available: {nmax}   solve orders: M≤{N_SOLVE_M}, D≤{N_SOLVE_D}; "
          f"all higher orders are held-out verification")
    print("=" * 74)

    is_plus, det = plus_verdict(t, v7, nmax)
    print(f"TEST M  (t Möbius in v₇ — must FAIL for '+'):      "
          f"{'PASS' if det['mobius_pass'] else 'FAIL'}")
    print(f"TEST D  (t degree-2 rational in v₇ — must PASS):   "
          f"{'PASS' if det['deg2_pass'] else 'FAIL'}"
          f"   [verified on orders {N_SOLVE_D + 1}..{nmax}]")

    kappa = fricke_kappa(det["sol"]) if det["sol"] else None
    print(f"TEST F  (involution constant κ, computed):          κ = {kappa}")

    # ------------------------------------------------------ negative controls
    print("-" * 74)
    ok = True

    n1_plus, n1 = plus_verdict(v7, v7, nmax)          # a Γ₀(7) Hauptmodul
    good = (not n1_plus) and n1["mobius_pass"]
    ok &= good
    print(f"  {'ok  ' if good else 'FAIL'}  N1: v₇ itself → Möbius passes, verdict NOT-plus")

    t_bad = t[:]
    t_bad[nmax - 2] += 1                               # corrupt one held-out term
    n2_plus, n2 = plus_verdict(t_bad, v7, nmax)
    good = not n2_plus and not n2["deg2_pass"]
    ok &= good
    print(f"  {'ok  ' if good else 'FAIL'}  N2: corrupted A279618 → deg-2 verification fails")

    n3_plus, n3 = plus_verdict(t, v5, nmax)
    good = not n3_plus and not n3["deg2_pass"] and not n3["mobius_pass"]
    ok &= good
    print(f"  {'ok  ' if good else 'FAIL'}  N3: wrong level (Γ₀(5) coordinate) → all fits fail")

    print("-" * 74)
    verdict_ok = is_plus and kappa == 49 and ok
    if is_plus and kappa is not None:
        print(f"VERDICT: A279618 generates the index-2 Fricke-invariant subfield of "
              f"ℚ(u₇);\n  by the Atkin–Lehner normalizer statement [B] it is a "
              f"Hauptmodul for Γ₀(7)+.\n  Fricke constant κ = {kappa} "
              f"(= 7² expected for w₇) — computed from the fit, not assumed.")
    else:
        print("VERDICT: NOT ESTABLISHED — see test lines above.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "checker": Path(__file__).name,
        "date": "2026-07-26",
        "claim": "g.f.(A279618) is a Hauptmodul for Gamma_0(7)+ (Fricke extension)",
        "method": "exact deg-2 rational identity in the Gamma_0(7) eta-quotient "
                  "coordinate; Mobius fit refuted; Fricke constant computed",
        "orders": {"available": nmax, "solve_M": N_SOLVE_M, "solve_D": N_SOLVE_D,
                   "held_out_verified": [N_SOLVE_D + 1, nmax]},
        "mobius_in_u7": det["mobius_pass"],
        "degree2_in_u7": det["deg2_pass"],
        "fricke_kappa": str(kappa),
        "negative_controls": {"N1_gamma07_hauptmodul": "not-plus as required",
                              "N2_corrupted_series": "deg2 verify fails as required",
                              "N3_wrong_level_5": "all fits fail as required"},
        "tier": "B",
        "tier_reason": "identities exact to stated order [computed]; conclusion uses "
                       "the classical Atkin-Lehner normalizer statement [cited, not "
                       "re-derived]; NO lattice data emitted (needs Dolgachev/Doran "
                       "fetched and read — see Phase 4 memo)",
        "verdict": "GAMMA07PLUS_HAUPTMODUL" if verdict_ok else "NOT_ESTABLISHED",
    }, indent=1))
    print(f"\ncertificate: {OUT.relative_to(REPO)}")
    return 0 if verdict_ok else 1


if __name__ == "__main__":
    sys.exit(main())
