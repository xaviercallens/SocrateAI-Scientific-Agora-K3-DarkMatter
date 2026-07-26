#!/usr/bin/env python3
"""
Controls for check_L3_irreducible_minimal.py.

E-010's rigged observable passed because its statistic was clamped below its own
threshold: it could not fail. These controls exist so that never applies here. Two
of them feed the checker operators whose answer is known in advance and known to be
NEGATIVE; if either ever reports PASS, the checker has stopped testing anything.

The third pins the checker against a *different* checker: Sym² of the L₂ exponents
computed here must reproduce, exactly, the L₃ Riemann scheme that
check_L3_riemann_scheme.py computed independently (E-009 Lead 2).

Run:  python3 checkers/test_L3_irreducible_minimal_controls.py
"""

import importlib.util
import json
import sys

import sympy as sp

_spec = importlib.util.spec_from_file_location(
    "chk", str(__import__("pathlib").Path(__file__).with_name("check_L3_irreducible_minimal.py"))
)
chk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(chk)

failures = []


def expect(cond, msg):
    print(f"  {'ok  ' if cond else 'FAIL'}  {msg}")
    if not cond:
        failures.append(msg)


print("control 1 — reducible operator must NOT pass the irreducibility step")
# theta^2 - 2*theta + 1 annihilates y = z (theta·z = z), so u = y'/y = 1/z is rational:
# the operator has a hyperexponential solution by construction and IS reducible.
r = chk.analyse("control_reducible", {"bulk_oeis": "synthetic", "P": (sp.Integer(1), sp.Integer(-2), sp.Integer(1))})
expect(r["step2_L2_irreducible"]["pass"] is False, "step2 rejects a known-reducible operator")
expect(r["step4_minimality"]["pass"] is False, "step4 does not claim minimality for it")
expect(r["conditional_on_step5"]["picard_rank_rho"] is None, "no rho is offered for it")

print("control 2 — distinct indicial roots at 0 means no logarithm, so no unipotent")
# theta^2 - 1 has indicial roots {+1,-1} at z = 0: distinct, hence no log solution.
r = chk.analyse("control_no_log", {"bulk_oeis": "synthetic", "P": (sp.Integer(1), sp.Integer(0), sp.Integer(-1))})
expect(r["step1_not_dihedral"]["pass"] is False, "step1 rejects an operator with no logarithm at 0")

print("control 3 — Sym2 of these L2 exponents must match check_L3_riemann_scheme.py exactly")
ref = {x["operator"]: x["riemann_scheme"]
       for x in json.load(open("data/certificates/L3_RIEMANN_SCHEME.json"))["results"]}
for name, spec in chk.OPERATORS.items():
    mine = chk.analyse(name, spec)["L2_exponents"]
    for pt, exps in mine.items():
        a, b = [sp.Rational(e) for e in (exps * 2)[:2]]
        expect(sorted([2 * a, a + b, 2 * b]) == sorted(sp.Rational(e) for e in ref[name][pt]),
               f"{name} at {pt}: Sym2{{{a},{b}}} agrees with the certified L3 scheme")

print("control 4 — the real operators must still pass, and must still withhold rho")
for name, spec in chk.OPERATORS.items():
    r = chk.analyse(name, spec)
    expect(r["step4_minimality"]["pass"] is True, f"{name} minimality holds")
    expect(r["picard_rank"] is None and r["transcendental_rank"] is None,
           f"{name} emits null rho/T (standing rule)")

print(f"\n{len(failures)} failure(s)" if failures else "\nall controls behaved as required")
sys.exit(1 if failures else 0)
