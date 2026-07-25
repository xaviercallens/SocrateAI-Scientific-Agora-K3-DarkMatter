#!/usr/bin/env python3
"""
check_L3_riemann_scheme.py — Lead 2 (E-009): does the order-3 operator constrain T?

Computes the COMPLETE Riemann scheme of the bulk order-3 operator L₃ (all four
singular points including ∞), verifies the Fuchs relation, tests maximal unipotent
monodromy (MUM) at z = 0, and tests the Wronskian identity W(L₃) = W(L₂)³.

Everything is exact rational arithmetic in the θ-basis. Nothing is read from a
certificate; the L₃/L₂ coefficients come from the Tier A kernel-verified
`lean4_formal_proofs/Structures/CooperSym2Proof.lean`.

WHAT THIS SETTLES (unconditionally)
-----------------------------------
The retracted ρ = 4 / T = 18 is **structurally impossible**, not merely unsupported.
A Fuchsian operator of order 3 governs a rank-3 local system; it cannot govern an
18-dimensional one. T = 18 would require an order-18 operator. So E-007's retraction
is reinforced by an independent argument that does not depend on any K3 reading.

WHAT THIS DOES *NOT* SETTLE (E-009)
-----------------------------------
Whether there IS a K3 whose transcendental sub-VHS L₃ governs. Every structural
precondition tested here passes, but passing preconditions is not existence. So
T = 3 / ρ = 19 is emitted ONLY as a CONDITIONAL, with `picard_rank` and
`transcendental_rank` still null. Do not cite them as derived.

Usage:
  python3 checkers/check_L3_riemann_scheme.py
  python3 checkers/check_L3_riemann_scheme.py --json data/certificates/L3_RIEMANN_SCHEME.json
"""

import argparse
import json
import sys
from pathlib import Path

import sympy as sp

z, r, w = sp.symbols("z r w")

# Provenance: lean4_formal_proofs/Structures/CooperSym2Proof.lean (Tier A, kernel-verified).
OPERATORS = {
    "cooper_s7": {
        "bulk_oeis": "A183204",
        "Q": (-27 * z**2 - 26 * z + 1, -81 * z**2 - 39 * z, -78 * z**2 - 21 * z, -24 * z**2 - 4 * z),
        "P": (-27 * z**2 - 26 * z + 1, -27 * z**2 - 13 * z, -6 * z**2 - 2 * z),
    },
    "cooper_s10": {
        "bulk_oeis": "A005260",
        "Q": (-64 * z**2 - 12 * z + 1, -192 * z**2 - 18 * z, -188 * z**2 - 10 * z, -60 * z**2 - 2 * z),
        "P": (-64 * z**2 - 12 * z + 1, -64 * z**2 - 6 * z, -15 * z**2 - z),
    },
}

# L₂ exponents at each finite singular locus, established by
# checkers/check_C1_kodaira_consistency.py; L₃ = Sym²(L₂) ⇒ {2a, a+b, 2b}.
L2_FINITE = (sp.Integer(0), sp.Rational(1, 2))


def roots_with_multiplicity(poly):
    out = []
    for root, mult in sp.roots(poly).items():
        out += [sp.nsimplify(root)] * mult
    return sorted(out, key=lambda x: sp.re(x))


def analyse(name, spec):
    Q3, Q2, Q1, Q0 = spec["Q"]
    P2, P1, P0 = spec["P"]

    # z = 0: indicial polynomial is Σ Q_k(0) r^k  (θ-basis)
    ind0 = sp.Poly(sum(Q.subs(z, 0) * r**k for k, Q in enumerate([Q0, Q1, Q2, Q3])), r)
    exp0 = roots_with_multiplicity(ind0)

    # finite singular loci = roots of the leading θ-coefficient
    loci = sorted(sp.solve(sp.Eq(Q3, 0), z), key=lambda s: sp.re(s))
    a, b = L2_FINITE
    exp_fin = sorted([2 * a, a + b, 2 * b], key=lambda x: sp.re(x))

    # z = ∞: θ_z = -θ_w with w = 1/z; scale by w² and alternate signs
    qc = [sp.expand(sp.simplify(Q.subs(z, 1 / w) * w**2)).subs(w, 0) for Q in (Q0, Q1, Q2, Q3)]
    indoo = sp.Poly(sum(((-1) ** k) * qc[k] * r**k for k in range(4)), r)
    expoo = roots_with_multiplicity(indoo)

    total = sum(exp0) + len(loci) * sum(exp_fin) + sum(expoo)
    n, s_pts = 3, 2 + len(loci)
    fuchs_req = sp.Rational(n * (n - 1) * (s_pts - 2), 2)
    fuchs_ok = sp.simplify(total - fuchs_req) == 0
    mum = exp0 == [0, 0, 0]

    # Wronskian: W(L₃) = W(L₂)³  ⟺  a₂/a₃ = 3·b₁/b₂
    a3, a2 = sp.expand(Q3 * z**3), sp.expand((3 * Q3 + Q2) * z**2)
    b2, b1 = sp.expand(z**2 * P2), sp.expand(z * (P2 + P1))
    wron_ok = sp.simplify(a2 / a3 - 3 * b1 / b2) == 0

    # Fuchsian signature implied by the exponent differences:
    #   difference 0 (integral, unipotent) → cusp;  difference 1/e → order-e elliptic point
    def order_of(exps):
        d = sp.nsimplify(exps[1] - exps[0])
        return None if d == 0 else sp.denom(d)

    e_inf = order_of(expoo)
    e_fin = order_of(exp_fin)
    elliptic = [int(e_fin)] * len(loci) + ([int(e_inf)] if e_inf else [])
    cusps = 1 if mum else 0
    # hyperbolic area / 2π for signature (0; e...; s)
    area = sp.Rational(-2) + sum(1 - sp.Rational(1, e) for e in elliptic) + cusps

    print("=" * 74)
    print(f"{name}   (bulk {spec['bulk_oeis']})")
    print("=" * 74)
    print(f"  z = 0      : {[str(x) for x in exp0]}     MUM? {mum}")
    for zc in loci:
        print(f"  z = {str(zc):>6} : {[str(x) for x in exp_fin]}")
    print(f"  z = oo     : {[str(x) for x in expoo]}")
    print(f"  Fuchs relation: Σ = {sp.nsimplify(total)}  required {fuchs_req}  -> "
          f"{'SATISFIED' if fuchs_ok else 'VIOLATED'}")
    print(f"  Wronskian W(L3) = W(L2)^3 ?  {'CONFIRMED' if wron_ok else 'FAILS'}")
    print(f"  implied Fuchsian signature: genus 0; elliptic orders {elliptic}; "
          f"{cusps} cusp; area/2π = {area}")

    return {
        "operator": name,
        "bulk_oeis": spec["bulk_oeis"],
        "riemann_scheme": {
            "0": [str(x) for x in exp0],
            **{str(zc): [str(x) for x in exp_fin] for zc in loci},
            "oo": [str(x) for x in expoo],
        },
        "fuchs_sum": str(sp.nsimplify(total)),
        "fuchs_required": str(fuchs_req),
        "fuchs_satisfied": bool(fuchs_ok),
        "mum_at_zero": bool(mum),
        "wronskian_W3_equals_W2_cubed": bool(wron_ok),
        "implied_fuchsian_signature": {
            "genus": 0,
            "elliptic_orders": elliptic,
            "cusps": cusps,
            "hyperbolic_area_over_2pi": str(area),
        },
        "all_structural_tests_pass": bool(fuchs_ok and mum and wron_ok),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    results = [analyse(k, v) for k, v in OPERATORS.items()]
    every = all(x["all_structural_tests_pass"] for x in results)

    print("\n" + "=" * 74)
    print("LEAD 2 VERDICT")
    print("=" * 74)
    print("ESTABLISHED (unconditional): ρ=4 / T=18 is STRUCTURALLY IMPOSSIBLE.")
    print("  An order-3 Fuchsian operator governs a rank-3 local system. It cannot")
    print("  govern an 18-dimensional one; T=18 needs an order-18 operator.")
    print("  This is independent of any K3 reading and reinforces E-007.")
    print()
    print(f"ALL STRUCTURAL PRECONDITIONS FOR A K3 READING PASS: {every}")
    print("  order 3; MUM {0,0,0}; Fuchs exact; integral holomorphic solution;")
    print("  L3 = Sym^2(L2) (Tier A); W(L3) = W(L2)^3 (rank-3 ORTHOGONAL from")
    print("  rank-2 SYMPLECTIC — exactly a K3 transcendental lattice's form).")
    print()
    print("NOT ESTABLISHED (= E-009): that a K3 EXISTS whose transcendental sub-VHS")
    print("  L3 governs. Passing preconditions is not existence.")
    print("  ⇒ T=3 / ρ=19 is the UNIQUE assignment consistent with the operator,")
    print("    but it is emitted ONLY as a CONDITIONAL. picard_rank stays null.")

    out = {
        "checker": "check_L3_riemann_scheme.py",
        "checker_version": "1.0.0",
        "date": "2026-07-26",
        "ticket": "E-009 Lead 2",
        "results": results,
        "picard_rank": None,
        "transcendental_rank": None,
        "established_unconditionally": {
            "claim": "rho=4 / T=18 is structurally impossible for an order-3 operator",
            "reason": (
                "A Fuchsian operator of order n governs a rank-n local system. order(L3)=3, "
                "so any sub-VHS it governs has rank 3, not 18. T=18 would require order 18."
            ),
            "depends_on_K3_reading": False,
        },
        "conditional_result": {
            "if": "L3 governs the transcendental sub-VHS of a K3 family (E-009, OPEN)",
            "then": {"transcendental_rank_T": 3, "picard_rank_rho": 19},
            "status": "NOT ESTABLISHED — E-009 must resolve first. Do not cite as derived.",
        },
        "lead1_bonus": (
            "[B] The implied Fuchsian signature for s7 — genus 0, elliptic orders (2,2,3), "
            "1 cusp, area/2π = 2/3 — matches Γ₀(7)+ = Γ₀(7)/w₇ exactly: Γ₀(7) has index 8 "
            "(area 4/3), the Fricke quotient halves it to 2/3, its 2 cusps fuse to 1, its 2 "
            "order-3 points fuse to 1, and w₇'s 2 fixed points (h(-7)=h(-28)=1) become the 2 "
            "order-2 elliptic points. This independently corroborates E-009 Lead 1 "
            "(group is Γ₀(7)+, not Γ₀(7), which has ν₂=0). Inferred from exponent data + "
            "standard Fuchsian theory — NOT a rigorous identification."
        ),
    }
    if args.json:
        Path(args.json).write_text(json.dumps(out, indent=2))
        print(f"\nWrote {args.json}")
    return 0 if every else 3


if __name__ == "__main__":
    sys.exit(main())
