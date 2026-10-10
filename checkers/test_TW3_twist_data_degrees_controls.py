#!/usr/bin/env python3
"""Negative controls for check_TW3_twist_data_degrees.py (standing rule 1: a test that cannot fail is not a test).

Each control feeds the checker's own functions a deliberately wrong input and requires the specific refusal/failure.
Positive anchors first (the real data must pass), so a control failing to fail is distinguishable from a broken harness.
"""
import importlib.util
import json
import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("tw3", HERE / "check_TW3_twist_data_degrees.py")
tw3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tw3)

results = []


def check(name, cond):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)


# ---- positive anchors
D = (1, 0)
check("P0 canonical class of P^1 x P^2 is (-2,-3)", tw3.canonical() == (-2, -3))
check("P1 (1,0),(1,0) pass the disjointness necessary condition", tw3.disjoint_necessary(D, D))
B = tw3.budgets(D, D)
check("P2 all three budgets ok at orders (4,5,10)", all(v["ok"] for v in B.values()))
check("P3 residual classes are (0,12), (2,18), (4,36)",
      B["f"]["residual"] == (0, 12) and B["g"]["residual"] == (2, 18) and B["Delta"]["residual"] == (4, 36))
check("P4 h0 of the residuals are 91 and 570", tw3.h0((0, 12)) == 91 and tw3.h0((2, 18)) == 570)

# ---- controls from the directive
check("C1 wrong divisor class (0,1): intersection with itself is non-zero => not disjoint",
      not tw3.disjoint_necessary((0, 1), (0, 1)))
check("C2 divisor class (2,0): the f budget fails (need 16 > 8)", not tw3.budgets((2, 0), (2, 0))["f"]["ok"])
check("C3 non-disjoint pair (1,0),(0,1): product class non-zero", not tw3.disjoint_necessary((1, 0), (0, 1)))
check("C4 Tate orders (5,5,10) -> f order 5: f budget fails", not tw3.budgets(D, D, orders=(5, 5, 10))["f"]["ok"])
check("C5 Tate orders (4,7,14): g budget fails (need 14 > 12)",
      not tw3.budgets(D, D, orders=(4, 7, 14))["g"]["ok"])
K_wrong = tw3.canonical((1, 3))
check("C6 wrong canonical class (P^1 x P^3): differs from the TW1 certificate's -K",
      tuple(-k for k in K_wrong) != tuple(json.loads((HERE.parent / "data/certificates/TW1_two_e8_P1xP2.json").read_text())
                                          ["result"]["minus_K"]["value"]))

# ---- G2 controls
sig, pi = tw3.load_model()
W = sp.together(pi - sig + 1)
pi_s, w_s = tw3.structure(pi), tw3.structure(W)
X, _ = tw3.order_conditions(pi_s, w_s)
check("G0 sum of minimal vanishing orders per unit e is 12", X == 12)
refused = False
try:
    tw3.construct(4, pi_s, w_s)
except tw3.Refuse:
    refused = True
check("G1 e = 4 (12 e = 48 > 36) is refused", refused)

S = tw3.construct(1, pi_s, w_s)
ver = tw3.verify_construction(S)
check("G2 genuine e = 1 construction satisfies both identities exactly", ver["alpha3_identity"] and ver["beta2_identity"])
S_bad = dict(S)
S_bad["a"] = S["a"] + 1
ver_bad = tw3.verify_construction(S_bad)
check("G3 perturbing a by +1 breaks the alpha^3 identity", not ver_bad["alpha3_identity"])
S_bad2 = dict(S)
S_bad2["bb"] = S["bb"] + 1
check("G4 perturbing b breaks the beta^2 identity", not tw3.verify_construction(S_bad2)["beta2_identity"])
check("G5a the genuine pull-back check passes at rational points", tw3.pull_back_check(S, pi, W))
check("G5 a pi scaled by 2 is caught by the pull-back check", not tw3.pull_back_check(S, 2 * pi, W))

# ---- the sigma/pi sanity: a tampered pi is not accepted as 'c q^3 / z^8'
pi_tamper = pi + sp.Symbol("z") ** -3
raised = False
try:
    tw3.construct(1, tw3.structure(pi_tamper), w_s)
except tw3.Refuse:
    raised = True
check("G6 a tampered pi (extra z^-3 term) is refused by the structure check", raised)

bad = [n for n, ok in results if not ok]
print(f"{len(results) - len(bad)}/{len(results)} controls behave as required")
sys.exit(1 if bad else 0)
