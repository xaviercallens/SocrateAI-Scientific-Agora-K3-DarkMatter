#!/usr/bin/env python3
"""
PROJECT ALPHA-TOPOLOGY  —  exact-algebra test of three geometric origins for the
bare string-scale gauge coupling alpha_GUT^{-1} in [24, 26], from the S_{1,2} K3.

Governing rule ("Zero Simulation Flottante"): every number printed is either
  (a) an EXACT integer/rational computed over Q with sympy, or
  (b) an explicitly-labelled representative value used only to demonstrate the
      *structure* of a formula, never presented as the verified S_{1,2} value.

What is genuinely S_{1,2}-derivable from the data we hold (the sequence ->
Picard-Fuchs recurrence, and chi(K3)=24) is computed exactly. What requires the
S_{1,2} transcendental-lattice Gram matrix / monodromy (NOT computed in this
repo, see CAVEATS.md) is flagged as a null result, exactly as the directive asks.
"""
import sympy as sp


# ======================================================================
# 0.  Exact sequences and their Picard-Fuchs recurrences  (REAL S_{1,2} data)
# ======================================================================
def S(a, b, n):
    k = sp.symbols('k', integer=True)
    return sp.summation(sp.binomial(n, k)**a * sp.binomial(n + k, k)**b, (k, 0, n))


def _normalize(polys, n):
    """Clear denominators and common integer content for a clean recurrence."""
    dens = [sp.fraction(sp.together(p))[1] for p in polys if p != 0]
    L = sp.lcm([sp.Integer(1)] + dens) if dens else sp.Integer(1)
    polys = [sp.expand(p * L) for p in polys]
    contents = [sp.Poly(p, n).content() for p in polys if p != 0]
    g = sp.gcd(contents) if contents else sp.Integer(1)
    if g and g != 0:
        polys = [sp.cancel(p / g) for p in polys]
    return polys


def find_recurrence(seq, max_order=4, max_deg=4):
    """Find minimal poly-coefficient recurrence sum_j p_j(n) a(n+j)=0 over Q
    via exact nullspace. Returns (order, [p_j(n)]) or None. Verified on all terms."""
    n = sp.symbols('n')
    N = len(seq)
    for order in range(1, max_order + 1):
        for deg in range(0, max_deg + 1):
            ncols = (order + 1) * (deg + 1)
            rows = list(range(0, N - order))
            if len(rows) < ncols:
                continue
            # build coefficient matrix: each row n0 -> entries seq[n0+j]*n0^d
            M = sp.zeros(len(rows), ncols)
            for r, n0 in enumerate(rows):
                col = 0
                for j in range(order + 1):
                    for d in range(deg + 1):
                        M[r, col] = seq[n0 + j] * sp.Integer(n0)**d
                        col += 1
            for vec in M.nullspace():
                # unpack vector into polynomials p_j(n)
                polys = []
                col = 0
                for j in range(order + 1):
                    pj = sum(vec[col + d] * n**d for d in range(deg + 1))
                    polys.append(sp.expand(pj)); col += deg + 1
                if polys[-1] == 0:          # require genuine 'order' (leading nonzero)
                    continue
                polys = _normalize(polys, n)
                ok = all(sp.simplify(sum(polys[j].subs(n, n0) * seq[n0 + j]
                                         for j in range(order + 1))) == 0
                         for n0 in rows)
                if ok:
                    return order, polys
    return None


print("=" * 70)
print("EXACT PICARD-FUCHS RECURRENCES  (genuine S_{1,2} / S_{2,1} topology)")
print("=" * 70)
NTERMS = 26
seq12 = [S(1, 2, n) for n in range(NTERMS)]
seq21 = [S(2, 1, n) for n in range(NTERMS)]
print("S_{1,2}(n):", seq12)
print("S_{2,1}(n):", seq21)
n = sp.symbols('n')
for name, seq in (("S_{2,1}", seq21), ("S_{1,2}", seq12)):
    res = find_recurrence(seq)
    if res:
        order, polys = res
        terms = " + ".join(f"({sp.factor(polys[j])})*a(n+{j})" for j in range(order + 1))
        print(f"\n{name}: order-{order} P-recurrence (verified on {NTERMS} terms):")
        print("   " + terms + " = 0")
    else:
        print(f"\n{name}: no recurrence found within search bounds.")
print("\nNote: S_{2,1}(n) = sum C(n,k)^2 C(n+k,k) are the Apery numbers for zeta(2)")
print("      (Beukers 1987) -> a pencil of K3 surfaces, Picard number 19.")

CHI = 24
print(f"\nEuler characteristic of any K3 surface: chi = {CHI}  (exact, topological)")


# ======================================================================
# 1.  HYPOTHESIS 1 — GVW flux quantization / dilaton VEV
# ======================================================================
print("\n" + "=" * 70)
print("H1  Gukov-Vafa-Witten flux stabilization of the axio-dilaton")
print("=" * 70)
print("Structure:  W = (f - tau*h) . Pi(z),   D_tau W = 0  =>  tau = (f.Pi)/(h.Pi)")
print("with f,h in H^2(K3,Z) integer flux vectors. The stabilized coupling is")
print("g_s^{-1} = Im(tau). This is a MOBIUS image of the period by integer fluxes.")
print()
# Representative period of an attractive K3 (transcendental lattice [[2,0],[0,2]]):
# period omega = i (quadratic imaginary). Scan small integer SL(2,Z) fluxes.
omega = sp.I  # representative ONLY; the true S_{1,2} period needs the monodromy (uncomputed)
hits = []
seen = set()
for a in range(-3, 4):
    for b in range(-3, 4):
        for c in range(-3, 4):
            for d in range(-3, 4):
                if a * d - b * c != 1:          # SL(2,Z) flux change of basis
                    continue
                tau = (a * omega + b) / (c * omega + d)
                im = sp.im(sp.simplify(tau))
                if im <= 0:
                    continue
                val = sp.nsimplify(im)
                key = str(val)
                if key in seen:
                    continue
                seen.add(key)
                hits.append(float(im))
hits = sorted(set(round(h, 4) for h in hits))
in_band = [h for h in hits if 24 <= h <= 26]
print(f"Distinct Im(tau) reachable with |flux|<=3 :  {hits[:12]} ...")
print(f"Maximum Im(tau) in this scan           :  {max(hits):.4f}")
print(f"Values landing in [24,26]              :  {in_band if in_band else 'NONE'}")
print("VERDICT H1: the dilaton VEV is a function of FREE integer fluxes; no")
print("            lowest-energy configuration natively selects [24,26].")
print("            => TOPOLOGICALLY UNCONSTRAINED.")


# ======================================================================
# 2.  HYPOTHESIS 2 — attractor mechanism (black-hole fixed point)
# ======================================================================
print("\n" + "=" * 70)
print("H2  N=2 attractor fixed point of the S_{1,2} complex structure")
print("=" * 70)
print("Structure:  at the horizon, moduli solve  p^I = Re(C X^I), q_I = Re(C F_I)")
print("            and  Im(f_gauge) ~ |Z(p,q)|^2  is fixed by integer charges (p,q)")
print("            AND by the transcendental-lattice Gram matrix of S_{1,2}.")
print()
print("Required input: the exact Gram matrix of the S_{1,2} transcendental lattice.")
print("Status in repo: NOT COMPUTED (monodromy connection matrix unformalized,")
print("                see CAVEATS.md sec.). Without it, |Z|^2 is undefined.")
print("Even granting a Gram matrix, |Z(p,q)|^2 is a free function of the integer")
print("charges (p,q): one tunes charges to any target, so [24,26] is not selected.")
print("VERDICT H2: missing exact input + charge-dependent => TOPOLOGICALLY UNCONSTRAINED.")


# ======================================================================
# 3.  HYPOTHESIS 3 — D7-brane cycle volume + chi=24 one-loop threshold
# ======================================================================
print("\n" + "=" * 70)
print("H3  D7-brane gauge coupling = cycle volume + chi one-loop threshold")
print("=" * 70)
print("Structure:  alpha^{-1} = Vol(Sigma)/g_s  +  kappa * chi,   chi(K3)=24.")
print(f"Genuine topological invariant available exactly:  chi = {CHI}.")
print()
# The ONLY exactly-known piece is chi=24. The map to alpha^{-1} needs kappa and
# Vol(Sigma)/g_s, neither fixed by topology. Show the band condition:
kappa, Vol_over_gs = sp.symbols('kappa Vol_over_gs', positive=True)
alpha_inv = Vol_over_gs + kappa * CHI
print("alpha^{-1} = Vol/g_s + kappa*24 .")
print("To land in [24,26] with kappa=1 (the 'natural' guess) needs Vol/g_s in [0,2]")
print("i.e. a SUB-STRING-SCALE cycle with g_s ~ O(1): not derived, just assumed.")
print("chi=24 is numerically CLOSE to alpha_GUT^{-1}~25, but this is a coincidence")
print("of order-unity integers, not a derivation (kappa and Vol/g_s are free).")
print("VERDICT H3: TOPOLOGICALLY SUGGESTIVE (chi=24) but NOT CONSTRAINED.")


# ======================================================================
# 4.  ALPHA-TOPOLOGY MATRIX
# ======================================================================
print("\n" + "=" * 70)
print("ALPHA-TOPOLOGY MATRIX  (target: alpha_GUT^{-1} in [24,26] from S_{1,2})")
print("=" * 70)
rows = [
    ("H1 GVW flux / dilaton", "Im(tau)=Mobius(period; free integer fluxes)",
     "free param", "UNCONSTRAINED"),
    ("H2 Attractor fixed pt", "needs S_{1,2} Gram matrix (uncomputed) + charges",
     "no input", "UNCONSTRAINED"),
    ("H3 D7 vol + chi=24", "chi=24 exact; kappa, Vol/g_s free",
     "chi=24 only", "SUGGESTIVE, NOT DERIVED"),
]
print(f"{'Hypothesis':24}{'Mechanism':46}{'Exact?':14}{'Verdict'}")
print("-" * 110)
for h, m, e, v in rows:
    print(f"{h:24}{m:46}{e:14}{v}")
print()
print("CONCLUSION: No hypothesis NATIVELY forces alpha_GUT^{-1} into [24,26] from")
print("the exact S_{1,2} topology. The only genuine topological invariant, chi=24,")
print("is numerically near the target but does not derive it. Reporting NULL RESULT")
print("as instructed: deriving the bare gauge coupling from K3 topology alone")
print("remains an open problem; this model does not solve it.")
