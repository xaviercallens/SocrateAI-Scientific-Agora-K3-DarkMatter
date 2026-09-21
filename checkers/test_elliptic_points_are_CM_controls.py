#!/usr/bin/env python3
"""
test_elliptic_points_are_CM_controls.py -- negative controls for check_elliptic_points_are_CM.py
(A1).  R = real data / real known-bads, S = synthetic tamper.  Each names the clause that fired.

  R1  a generic CM point of the P2 table that is NOT a locus (s7, z = 1/2, D = -12), presented
      as if it were the locus z = -1 -> `locus_has_trivial_stabilizer_in_box` and
      `order_neq_exponent_denominator`; its stabilizer is trivial by the exact determination too.
  R2  non-CM tau: tau = i * 2^(1/3) (minimal polynomial of degree 6) -> refused,
      `tau_not_imaginary_quadratic`.  Bounded numeric companion (Tier B numeric, two
      precisions, 30 and 60 digits): no integer (c, e, b) != 0 with |entries| <= 40 has
      |c tau^2 + e tau - b| < 10^-20.
  R3  REAL wrong group: cooper_s10 loci in the Fricke-only group (determinants {1, 10}) ->
      z = -1/4 loses its stabilizer and z = infinity drops below order 4; clauses reported.
  R4  REAL wrong level: the cooper_s7 loci tested in Gamma_0(10)* -> clauses fire at the loci.
  R5  Gamma_0(7) alone (determinant 1): the order-3 point keeps order 3, both order-2 points
      become trivial -- the order-2 elements are Fricke elements (det 7).  Known answer from
      L3_RIEMANN_SCHEME.json's note (Gamma_0(7) has no order-2 points).
  R6  non-vacuity of "no other row": the row count with non-trivial stabilizer is computed,
      and equals the number of loci only in the right group (cf. R3).
  S1  tampered lattice vector at a locus (y + 1) -> `lattice_quadratic_not_proportional_to_tau_quadratic`.
  S2  tampered Riemann scheme (exponents 0, 1/3, 2/3 at z = -1) -> `order_neq_exponent_denominator`.
  S3  brute-force path silenced -> `two_search_paths_disagree`.
  S4  box too small (BOX = 1) -> `stabilizer_not_contained_in_box`.
  S5  exit gate: checks_ok False on False / 0.
  S6  a matrix that does not fix tau is rejected by fixes_exact (and one that does is accepted).
"""
import copy
import json
import pathlib
import sys
import tempfile
from fractions import Fraction as F

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_elliptic_points_are_CM as E

results = []


def record(name, ok, detail):
    results.append({"control": name, "behaved": bool(ok), "detail": detail})
    print(("ok   " if ok else "FAIL ") + name + " :: " + detail)


def fired(famrec):
    return sorted({c for l in famrec["loci"] for c in l["clauses_fired"]})


p2 = json.loads(E.P2.read_text())
s7, s10 = p2["families"]["cooper_s7"], p2["families"]["cooper_s10"]

# R1
row = next(r for r in s7["rows"] if r.get("z_value_if_rational") == "1/2")
fake = copy.deepcopy(s7)
fake["locus_hits"] = {"-1": [{"v": row["v"], "tau": row["tau"]}]}
fake["rows"] = []
f = E.family("cooper_s7", fake)
st = E.stabilizer(F(row["tau"]["re"]), F(row["tau"]["im_squared"]), 7, E.exact_divisors(7))
record("R1", {"locus_has_trivial_stabilizer_in_box", "order_neq_exponent_denominator"} <= set(fired(f))
       and st["stabilizer_order_exact"] == 1,
       f"z = 1/2 (v = {row['v']}, D = {row['D']}): clauses {fired(f)}; exact order {st['stabilizer_order_exact']}")

# R2
import sympy as sp
import mpmath as mp
tau = sp.I * sp.root(2, 3)
try:
    E.quadratic_of_algebraic_tau(tau)
    record("R2", False, "accepted")
except E.Refusal as e:
    hits = {}
    for dps in (30, 60):
        mp.mp.dps = dps
        t = mp.mpc(0, mp.root(2, 3))
        t2 = t * t
        hits[dps] = sum(1 for c in range(-40, 41) for ee in range(-40, 41) for b in range(-40, 41)
                        if (c or ee or b) and abs(c * t2 + ee * t - b) < mp.mpf(10) ** -20)
    record("R2", e.clause == "tau_not_imaginary_quadratic" and hits == {30: 0, 60: 0},
           f"refused: {e.clause}; bounded numeric hits at 30/60 digits: {hits}")
ok_quadratic = E.quadratic_of_algebraic_tau(sp.Rational(1, 2) + sp.I * sp.sqrt(sp.Rational(1, 28)))
record("R2b", ok_quadratic == [7, -7, 2], f"the same function accepts the s7 locus z = -1: quadratic {ok_quadratic}")

# R3
f = E.family("cooper_s10", s10, divisors=[1, 10])
orders = {l["locus_z"]: l["stabilizer_order_in_box"] for l in f["loci"]}
record("R3", "order_neq_exponent_denominator" in fired(f) and orders["infinity"] != 4,
       f"Fricke-only group at n = 10: orders {orders}; clauses {fired(f)}")

# R4
wrong = copy.deepcopy(s7)
wrong["n"] = 10
wrong["rows"] = []
f = E.family("cooper_s7", wrong)
record("R4", "lattice_quadratic_not_proportional_to_tau_quadratic" in fired(f) or "locus_has_trivial_stabilizer_in_box" in fired(f),
       f"s7 loci at level 10: orders {[l['stabilizer_order_in_box'] for l in f['loci']]}; clauses {fired(f)}")

# R5
f = E.family("cooper_s7", s7, divisors=[1])
orders = {l["locus_z"]: l["stabilizer_order_exact"] for l in f["loci"]}
record("R5", orders == {"infinity": 3, "-1": 1, "1/27": 1}, f"Gamma_0(7) alone: exact orders {orders}")

# R6
good = E.family("cooper_s10", s10)
n_good = sum(l["stabilizer_order_exact"] > 1 for l in good["loci"]) + len(good["non_locus_rows"]["rows_with_nontrivial_stabilizer"])
f = E.family("cooper_s10", s10, divisors=[1, 10])
n_bad = sum(l["stabilizer_order_exact"] > 1 for l in f["loci"]) + len(f["non_locus_rows"]["rows_with_nontrivial_stabilizer"])
record("R6", n_good == 3 and n_bad != 3, f"rows of the s10 table with non-trivial stabilizer: {n_good} in Gamma_0(10)*, {n_bad} in the Fricke-only group")

# S1
tam = copy.deepcopy(s7)
tam["locus_hits"]["-1"][0]["v"][1] += 1
tam["rows"] = []
f = E.family("cooper_s7", tam)
record("S1", "lattice_quadratic_not_proportional_to_tau_quadratic" in fired(f), f"clauses {fired(f)}")

# S2
sch = json.loads(E.SCHEME.read_text())
sch["results"][0]["riemann_scheme"]["-1"] = ["0", "1/3", "2/3"]
orig = E.SCHEME
with tempfile.TemporaryDirectory() as d:
    E.SCHEME = pathlib.Path(d) / "s.json"
    E.SCHEME.write_text(json.dumps(sch))
    f = E.family("cooper_s7", s7)
E.SCHEME = orig
bad = [l["locus_z"] for l in f["loci"] if "order_neq_exponent_denominator" in l["clauses_fired"]]
record("S2", bad == ["-1"], f"order_neq_exponent_denominator fired at {bad}")

# S3
orig2 = E.stabilizer_path2
E.stabilizer_path2 = lambda *a, **k: set()
try:
    E.family("cooper_s7", s7)
    record("S3", False, "accepted")
except E.Refusal as e:
    record("S3", e.clause == "two_search_paths_disagree", f"refused: {e.clause}")
finally:
    E.stabilizer_path2 = orig2

# S4
f = E.family("cooper_s7", s7, box=1)
record("S4", "stabilizer_not_contained_in_box" in fired(f), f"clauses {fired(f)}")

record("S5", not E.checks_ok({"a": False}) and not E.checks_ok({"a": 0}) and E.checks_ok({"a": True}), "checks_ok requires `is True`")
record("S6", E.fixes_exact((0, 1, -7, 0), F(0), F(1, 7)) and not E.fixes_exact((0, 1, -7, 1), F(0), F(1, 7))
       and not E.fixes_exact((0, 1, -10, 0), F(0), F(1, 7)), "fixes_exact accepts the Fricke involution at i/sqrt7, rejects two others")

out = E.CERTS / "ELLIPTIC_POINTS_ARE_CM_controls.json"
out.write_text(json.dumps({"controls_for": "checkers/check_elliptic_points_are_CM.py", "results": results,
                           "behaved": sum(r["behaved"] for r in results), "total": len(results),
                           "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: self (controls) | Reviewed-by: N"},
                          indent=1) + "\n")
print(f"{sum(r['behaved'] for r in results)}/{len(results)} controls behaved as required")
sys.exit(0 if all(r["behaved"] for r in results) else 1)
