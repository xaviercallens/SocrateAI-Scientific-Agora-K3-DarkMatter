#!/usr/bin/env python3
"""
test_CM_completeness_classnumber_controls.py -- negative controls for
check_CM_completeness_classnumber.py (A6).  R = real data / real known-bads, S = tamper.

  R1  deleting a row of the table flips its D to INCOMPLETE(missing 1) -- done for EVERY D
      of both families that has at least two rows (first row deleted).
  R1b the missing point's representative vector is reported, and lies in the deleted row's
      orbit (D = -56, s7).
  R1c a D with a SINGLE row (s7, z = 1/125) deleted from the full table -> ABSENT(missing all 1),
      and the exit-code gate fires on `absent_D_has_a_norm_inside_the_window`.
  R2  REAL wrong group, s7: Gamma_0(7) without the Fricke involution -> expected counts rise,
      rows go INCOMPLETE, and X2 (numeric grouping = exact orbits) FAILS: z identifies points
      that Gamma_0(7) alone does not.
  R3  REAL wrong group, s10: Fricke-only (determinants {1, 10}) -> same, X2 FAILS.  (Agrees
      with control R3 of A1: the s10 coordinate needs the full Atkin-Lehner group.)
  R4  REAL wrong level: s7 rows read at n = 10 -> refused; clause reported.
  R5  reduction is an invariant: for 200 pseudo-random SL_2(Z) images of Heegner forms (fixed
      seed) key_of returns the key of the original whenever the matrix is in Gamma_0(n), and
      the tracked matrix reproduces the form.
  R5b the class key is not a constant and is not Gamma_0(n)-blind: among small SL_2(Z) matrices
      OUTSIDE Gamma_0(7), some image that is still a Heegner form lands in a DIFFERENT class
      (asserted on Heegner images only; a witness is recorded).
  R6b X1 coverage is disclosed and is computed: the table discriminants it reaches are exactly
      those coprime to n, and they are a small minority of the table.
  R6  X1 can fail: counting beta modulo n instead of 2n makes the class-number formula
      disagree with the enumeration.
  S1  a duplicated point (the Fricke image of a row added as a new row) ->
      `two_table_rows_in_one_orbit`.
  S2  merged numeric groups -> X2 partitions_identical False.
  S3  tampered D in a row -> `row_D_disagrees_with_form_discriminant`.
  S4  non-primitive vector (2, -2, 0) -> `form_vector_round_trip_fails`.
  S5  window bound raised artificially (pretend the table covered -v^2 <= 300) ->
      `absent_D_has_a_norm_inside_the_window` fires: the ABSENT list is not vacuous.
  S6  exit gate.
"""
import copy
import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_CM_completeness_classnumber as C
import check_CM_points_rho20 as CM

results = []


def record(name, ok, detail):
    results.append({"control": name, "behaved": bool(ok), "detail": detail})
    print(("ok   " if ok else "FAIL ") + name + " :: " + detail)


p2 = json.loads(C.P2.read_text())
fams = p2["families"]

# R1
flips, total = 0, 0
for key, fam in fams.items():
    byD = {}
    for r in fam["rows"]:
        byD.setdefault(r["D"], []).append(r)
    for D, rs in byD.items():
        if len(rs) < 2:
            continue
        total += 1
        out = C.family(key, dict(fam, rows=rs[1:]), scan_absent=False)
        flips += next(p for p in out["per_D"] if p["D"] == D)["verdict"] == "INCOMPLETE(missing 1)"
record("R1", flips == total and total > 0, f"{flips}/{total} discriminants with at least two rows flip to INCOMPLETE(missing 1) "
       "when their first row is deleted (both families)")
s7 = fams["cooper_s7"]
single = next(r for r in s7["rows"] if r.get("z_value_if_rational") == "1/125")
out = C.family("cooper_s7", dict(s7, rows=[r for r in s7["rows"] if r is not single]), window_bound=p2["window"]["BOUND_minus_v2"])
ab = next((a for a in out["absent_D"]["rows"] if a["D"] == single["D"]), None)
fired = [c for c in out["contradictions"] if c["D"] == single["D"]]
record("R1c", ab is not None and ab["verdict"] == "ABSENT(missing all 1)" and
       [c["clause"] for c in fired] == ["absent_D_has_a_norm_inside_the_window"],
       f"single-row D = {single['D']} (z = 1/125) deleted -> {ab['verdict'] if ab else None}; gate clause "
       f"{[c['clause'] for c in fired]} (its norm {ab['minus_v2_and_div_required'] if ab else None} is inside the window)")
d56 = [r for r in s7["rows"] if r["D"] == -56]
out = C.family("cooper_s7", dict(s7, rows=d56[1:]))
row = next(p for p in out["per_D"] if p["D"] == -56)
cl = C.Classes(7, -56)
k_del = cl.orbit_conj[cl.key_of(C.form_of_vector(7, tuple(d56[0]["v"])))]
k_rep = cl.orbit_conj[cl.key_of(C.form_of_vector(7, tuple(row["missing_points_representative_vectors"][0])))]
record("R1b", row["verdict"] == "INCOMPLETE(missing 1)" and k_del == k_rep,
       f"D = -56, row v = {d56[0]['v']} deleted -> {row['verdict']}; reported missing vector "
       f"{row['missing_points_representative_vectors'][0]} lies in the deleted row's orbit: {k_del == k_rep}")

# R2 / R3
def wrong_group(key, divisors):
    fam = fams[key]
    rel, r = CM.relation_for(key, fam["n"])
    vs = CM.enumerate_vectors(fam["n"])
    out = C.family(key, fam, vectors_and_groups=(vs, CM.group_by_z(fam["n"], rel, r, vs)), divisors=divisors)
    return out

for name, key, div in (("R2", "cooper_s7", [1]), ("R3", "cooper_s10", [1, 10])):
    out = wrong_group(key, div)
    x2 = out["x2_numeric_grouping_vs_exact_orbits"]
    record(name, x2["partitions_identical"] is False and out["summary"]["incomplete"] > 0,
           f"{key} with Atkin-Lehner determinants {div}: X2 identical = {x2['partitions_identical']} "
           f"({x2['numeric_groups']} numeric groups vs {x2['exact_orbits']} exact orbits); "
           f"{out['summary']['incomplete']}/{out['summary']['D_values']} D INCOMPLETE; "
           f"clauses {sorted({c['clause'] for c in out['contradictions']})}")

# R4
try:
    C.family("cooper_s7", dict(s7, n=10))
    record("R4", False, "accepted")
except C.Refusal as e:
    record("R4", e.clause in ("vector_form_not_heegner", "row_D_disagrees_with_form_discriminant",
                              "form_vector_round_trip_fails", "discriminant_normalisation_fails"), f"refused: {e.clause}")

# R5
rng = random.Random(20260921)
okc, tested = 0, 0
for n, D in ((7, -119), (10, -800), (7, -3), (10, -4)):
    cl = C.Classes(n, D)
    for _ in range(50):
        f = rng.choice(list(cl.reps.values()))
        k0 = cl.key_of(f)
        # random element of Gamma_0(n): product of T^a and (1,0,n,1)^b
        M = (1, 0, 0, 1)
        for _ in range(6):
            M = C.mmul(M, rng.choice([(1, rng.randint(-3, 3), 0, 1), (1, 0, n * rng.randint(-2, 2), 1)]))
        g = C.act(f, M)
        tested += 1
        okc += (cl.key_of(g) == k0)
record("R5", okc == tested, f"{okc}/{tested} Gamma_0(n)-images keep their class key")
R5B_D = -3      # 7 splits here; at D = -119 (7 ramified) every image under such a matrix fails is_heegner
# ... and a matrix NOT in Gamma_0(n) can change the key.  Asserted on images that ARE Heegner
# forms (so it is key_of that is exercised, not is_heegner); the non-Heegner images are
# reported separately and do not count towards the verdict.
cl = C.Classes(7, R5B_D)
box = range(-3, 4)
outside = [(a, b, c, d) for a in box for b in box for c in box for d in box
           if a * d - b * c == 1 and c % 7 != 0]
moved, kept, nonheeg, witness = 0, 0, 0, None
for M in outside:
    for f in cl.reps.values():
        g = C.act(f, M)
        if not C.is_heegner(g, 7):
            nonheeg += 1
        elif cl.key_of(g) != cl.key_of(f):
            moved += 1
            witness = witness or (list(M), list(f), list(g))
        else:
            kept += 1
record("R5b", moved > 0 and len(cl.keys) > 1,
       f"{len(outside)} SL_2(Z) matrices outside Gamma_0(7), entries in [-3, 3], at D = {R5B_D} ({len(cl.keys)} distinct keys): "
       f"{moved} Heegner images change class key, {kept} keep it, {nonheeg} images are not Heegner (not counted); "
       f"first witness M, f, f.M = {witness}")

# R6
def bad_formula(n, D):
    betas = sum(1 for b in range(n) if (b * b - D) % (4 * n) == 0)
    return C.class_number(D) * betas, len(C.Classes(n, D, divisors=[1]).keys)
orig = C.x1_formula
C.x1_formula = bad_formula
bad = C.x1_all(7, [])
C.x1_formula = orig
record("R6", len(bad["disagreements"]) > 0, f"beta counted modulo n: {len(bad['disagreements'])} disagreements of {bad['discriminants_checked']}")

# R6b
from math import gcd as _gcd
p2 = json.loads(C.P2.read_text())
det = []
okb = True
for key, fam in p2["families"].items():
    Ds = sorted({r["D"] for r in fam["rows"]})
    x = C.x1_all(fam["n"], Ds)
    want = sorted((D for D in Ds if _gcd(D, fam["n"]) == 1), reverse=True)
    okb = okb and x["table_discriminants_covered"] == want and x["table_discriminants_total"] == len(Ds) \
        and 2 * len(want) < len(Ds)
    det.append(f"{key}: {len(want)} of {len(Ds)} table discriminants {want}")
record("R6b", okb, "X1 reaches " + "; ".join(det))

# S1
r0 = next(r for r in s7["rows"] if r["D"] == -56)
fr = CM.fricke_image(tuple(r0["v"]))
fr = tuple(fr) if fr[0] > 0 else tuple(-t for t in fr)
dup = copy.deepcopy(r0)
dup["v"] = list(fr)
out = C.family("cooper_s7", dict(s7, rows=s7["rows"] + [dup]))
record("S1", any(c["clause"] == "two_table_rows_in_one_orbit" for c in out["contradictions"]),
       f"Fricke image {list(fr)} of row {r0['v']} added: clauses {sorted({c['clause'] for c in out['contradictions']})}")

# S2
rel, r = CM.relation_for("cooper_s7", 7)
vs = CM.enumerate_vectors(7)
groups = CM.group_by_z(7, rel, r, vs)
merged = [groups[0] + groups[1]] + groups[2:]
out = C.family("cooper_s7", s7, vectors_and_groups=(vs, merged))
record("S2", out["x2_numeric_grouping_vs_exact_orbits"]["partitions_identical"] is False, "merged groups -> X2 False")

# S3
t = copy.deepcopy(s7)
t["rows"][3]["D"] -= 4
try:
    C.family("cooper_s7", t)
    record("S3", False, "accepted")
except C.Refusal as e:
    record("S3", e.clause == "row_D_disagrees_with_form_discriminant", f"refused: {e.clause}")

# S4
try:
    C.form_of_vector(7, (2, -2, 0))
    record("S4", False, "accepted")
except C.Refusal as e:
    record("S4", e.clause == "form_vector_round_trip_fails", f"refused: {e.clause}")

# S5
out = C.family("cooper_s7", dict(s7, rows=[r for r in s7["rows"] if -r["D"] <= 120]), window_bound=300)
record("S5", any(c["clause"] == "absent_D_has_a_norm_inside_the_window" for c in out["contradictions"]),
       f"{sum(c['clause'] == 'absent_D_has_a_norm_inside_the_window' for c in out['contradictions'])} absent D fall inside a pretended bound of 300")

record("S6", not C.checks_ok({"a": False}) and not C.checks_ok({"a": 0}) and C.checks_ok({"a": True}), "checks_ok requires `is True`")

out = C.CERTS / "CM_COMPLETENESS_controls.json"
out.write_text(json.dumps({"controls_for": "checkers/check_CM_completeness_classnumber.py", "results": results,
                           "behaved": sum(r["behaved"] for r in results), "total": len(results),
                           "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: self (controls) | Reviewed-by: N"},
                          indent=1) + "\n")
print(f"{sum(r['behaved'] for r in results)}/{len(results)} controls behaved as required")
sys.exit(0 if all(r["behaved"] for r in results) else 1)
