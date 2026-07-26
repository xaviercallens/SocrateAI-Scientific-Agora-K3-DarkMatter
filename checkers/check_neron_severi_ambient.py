#!/usr/bin/env python3
"""
check_neron_severi_ambient.py — Phase 3 cross-check: what do the A–vS models actually give?

Independent corroboration attempt for Phase 3 step B (`check_L3_irreducible_minimal.py`),
approaching ρ from the geometry rather than from the variation of Hodge structure.

E-009 hands us explicit K3 models (Almkvist–van Straten arXiv:2103.08651):
    s7   X = G(2,6) ∩ six hyperplane sections, Plücker embedding
    s10  X = ℙ³×ℙ³ ∩ four (1,1)-type sections, Segre embedding
The hope was that counting Néron–Severi classes on these would confirm ρ = 19 from a
direction that owes nothing to the differential operator.

RESULT: IT DOES NOT, AND THE REASON IS STRUCTURAL — reported here so the route is not
retried. The ambient models pin only the classes visible in the ambient space:

    s7   NS ⊇ ⟨H⟩,        H² = deg G(2,6) = 14   ⇒  ρ ≥ 1
    s10  NS ⊇ ⟨H₁,H₂⟩,    Gram [[4,6],[6,4]]     ⇒  ρ ≥ 2

That is 18 resp. 17 classes short of 19. The shortfall is not an artefact of being lazy
about the count: **the general member of each ambient family genuinely has that small ρ.**
The dimension bookkeeping below shows it, and this checker verifies it as its main test —
the moduli space of ρ-polarized K3s has dimension 20 − ρ, and

    s7   ambient family dim = 19 = 20 − 1   (ρ = 1, the classical Mukai genus-8 model)
    s10  ambient family dim = 18 = 20 − 2   (ρ = 2)

Our family is a **1-parameter** subfamily, i.e. codimension 18 resp. 17. The missing
classes are created by the special geometry of that pencil — they are not present in, and
cannot be read off from, the ambient description. Recovering them would need the explicit
defining equations of the A–vS pencil and a resolution of its singular members: a real
piece of algebraic geometry, not a bookkeeping exercise.

WHAT THIS CHECKER DOES ESTABLISH
--------------------------------
Applying the same verified dimension formula to our own family gives a genuine bound.
The family is 1-dimensional, and it is **non-isotrivial** — the local monodromy at z = 0 is
unipotent and ≠ I (step 1 of check_L3_irreducible_minimal.py), so the period map is not
constant. A non-isotrivial 1-parameter family sits inside the moduli of ρ-polarized K3s for
its very general member, so 1 ≤ 20 − ρ, i.e.

    ρ ≤ 19        (equivalently rank T ≥ 3)

That is a real, independently-obtained bound. But note **which half it is**: it is the same
half step A already gives from V ⊆ T. The hard direction, ρ ≥ 19 (rank T ≤ 3), needs
T ⊆ V^sat — the minimality of T among primitive sub-Hodge-structures containing H^{2,0} —
and this route does not touch it.

CONCLUSION FOR PHASE 3
----------------------
The Néron–Severi route **cannot substitute for step B**. It corroborates the easy bound
from a second direction and it independently validates the dimension formula on two models
whose ρ is known, but the citation in step B remains the only thing standing between this
repo and a derived ρ = 19. ρ/T are emitted null, as everywhere else.

Usage:
  python3 checkers/check_neron_severi_ambient.py
  python3 checkers/check_neron_severi_ambient.py --json data/certificates/NS_AMBIENT_BOUND.json
"""

import argparse
import json
import sys

import sympy as sp

h1, h2 = sp.symbols("h1 h2")


def point_coeff(expr, dims=(3, 3)):
    """Coefficient of the point class h1^3 h2^3 in the Chow ring of ℙ³×ℙ³."""
    poly = sp.Poly(sp.expand(expr), h1, h2)
    return sum(c for m, c in zip(poly.monoms(), poly.coeffs()) if m == dims)


def grassmannian_degree(k, n):
    """deg G(k,n) in the Plücker embedding = (k(n-k))! · Π_{i<k} i!/(n-k+i)!."""
    d = k * (n - k)
    return sp.Integer(sp.factorial(d) * sp.prod(
        [sp.Rational(sp.factorial(i), sp.factorial(n - k + i)) for i in range(k)]))


def analyse_s10():
    X = sp.expand((h1 + h2) ** 4)  # class of the (1,1)^4 complete intersection
    g = sp.Matrix([[point_coeff(h1**2 * X), point_coeff(h1 * h2 * X)],
                   [point_coeff(h1 * h2 * X), point_coeff(h2**2 * X)]])
    eig = sorted(g.eigenvals())
    # h^0(O(1,1)) = 4·4; four of them = G(4,16); mod Aut(ℙ³×ℙ³)° = PGL4 × PGL4
    family_dim = 4 * (16 - 4) - (15 + 15)
    return {
        "model": "P3 x P3 cap four (1,1) sections (Segre)",
        "ambient_classes": ["H1 = pr1*O(1)", "H2 = pr2*O(1)"],
        "gram_matrix": [[int(x) for x in g.row(i)] for i in range(2)],
        "gram_determinant": int(g.det()),
        "gram_eigenvalue_signs": [int(sp.sign(e)) for e in eig],
        "hodge_index_signature_ok": bool([sp.sign(e) for e in eig].count(1) == 1),
        "polarisation_degree_H_squared": int(point_coeff((h1 + h2) ** 2 * X)),
        "genus": int(sp.Rational(point_coeff((h1 + h2) ** 2 * X) + 2, 2)),
        "rho_lower_bound_from_ambient": 2,
        "ambient_family_dimension": int(family_dim),
        "generic_rho_of_ambient_family": 2,
    }


def analyse_s7():
    deg = grassmannian_degree(2, 6)
    # h^0(G(2,6), O(1)) = dim Λ²C⁶ = 15; six of them = G(6,15); mod Aut(G(2,6))° = PGL6
    family_dim = 6 * (15 - 6) - 35
    return {
        "model": "G(2,6) cap six hyperplane sections (Plucker)",
        "ambient_classes": ["H = O(1)|_X"],
        "gram_matrix": [[int(deg)]],
        "gram_determinant": int(deg),
        "gram_eigenvalue_signs": [1],
        "hodge_index_signature_ok": True,
        "polarisation_degree_H_squared": int(deg),
        "genus": int(sp.Rational(deg + 2, 2)),
        "rho_lower_bound_from_ambient": 1,
        "ambient_family_dimension": int(family_dim),
        "generic_rho_of_ambient_family": 1,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write certificate here")
    args = ap.parse_args()

    results = {"cooper_s7": analyse_s7(), "cooper_s10": analyse_s10()}

    # MAIN TEST: the moduli-dimension formula dim = 20 - rho, checked against two models
    # whose generic rho is known independently. If either fails, the formula is being
    # misapplied and the bound derived from it below is worthless.
    formula_ok = True
    for name, r in results.items():
        predicted = 20 - r["generic_rho_of_ambient_family"]
        r["dimension_formula_check"] = {
            "predicted_20_minus_rho": predicted,
            "counted_family_dimension": r["ambient_family_dimension"],
            "pass": predicted == r["ambient_family_dimension"],
        }
        formula_ok &= r["dimension_formula_check"]["pass"]

    # Applied to our own family: 1-parameter and non-isotrivial  =>  1 <= 20 - rho.
    our_bound = {
        "family_dimension": 1,
        "non_isotrivial": True,
        "non_isotriviality_source": "local monodromy at z=0 is unipotent and != I "
                                    "(check_L3_irreducible_minimal.py step 1), so the period "
                                    "map is not constant",
        "rho_upper_bound": 19,
        "equivalently": "rank T >= 3",
        "which_half": "This is the SAME half step A already gives via V subset T. The hard "
                      "direction rho >= 19 (rank T <= 3) requires T subset V^sat and is NOT "
                      "reachable from this route.",
        "valid_only_if": "the dimension formula check above passes",
        "pass": bool(formula_ok),
    }

    for name, r in results.items():
        print(f"\n{'='*72}\n{name}  —  {r['model']}\n{'='*72}")
        print(f"  ambient NS classes      : {', '.join(r['ambient_classes'])}")
        print(f"  Gram matrix             : {r['gram_matrix']}   det = {r['gram_determinant']}")
        print(f"  Hodge index signature   : {'ok (1, r-1)' if r['hodge_index_signature_ok'] else 'WRONG'}")
        print(f"  polarisation H^2        : {r['polarisation_degree_H_squared']}  (genus {r['genus']})")
        print(f"  rho lower bound         : {r['rho_lower_bound_from_ambient']}   <- vs 19 wanted")
        d = r["dimension_formula_check"]
        print(f"  dim formula 20-rho      : {d['predicted_20_minus_rho']} predicted vs "
              f"{d['counted_family_dimension']} counted   {'PASS' if d['pass'] else 'FAIL'}")

    print(f"\n{'='*72}\nAPPLIED TO OUR 1-PARAMETER FAMILY\n{'='*72}")
    print(f"  non-isotrivial (MUM)    : {our_bound['non_isotrivial']}")
    print(f"  1 <= 20 - rho           => rho <= {our_bound['rho_upper_bound']}  ({our_bound['equivalently']})")
    print(f"  {our_bound['which_half']}")
    print(f"\n  shortfall of the NS route: s7 needs 18 more classes, s10 needs 17 —")
    print(f"  they live in the specific pencil, not in the ambient description.")

    cert = {
        "checker": "check_neron_severi_ambient.py",
        "checker_version": "1.0.0",
        "date": "2026-07-26",
        "ticket": "Phase 3 cross-check of step B",
        "results": results,
        "our_family_bound": our_bound,
        "verdict": "CORROBORATES_UPPER_BOUND_ONLY" if formula_ok else "INCONCLUSIVE",
        "closes_step_B": False,
        "why_not": "the ambient models give rho >= 1 (s7) and rho >= 2 (s10); the generic member "
                   "of each ambient family really does have that rho, as the verified dimension "
                   "count shows. Our family is a codimension-18 resp. -17 subfamily and the extra "
                   "classes are not visible in the ambient space.",
        "picard_rank": None,
        "transcendental_rank": None,
    }
    if args.json:
        with open(args.json, "w") as f:
            json.dump(cert, f, indent=2)
        print(f"\nwrote {args.json}")
    print(f"\nVERDICT: {cert['verdict']}  (closes step B: {cert['closes_step_B']})")
    return 0 if formula_ok else 1


if __name__ == "__main__":
    sys.exit(main())
