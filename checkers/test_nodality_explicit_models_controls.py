#!/usr/bin/env python3
"""
test_nodality_explicit_models_controls.py -- negative controls for
check_nodality_explicit_models.py.

Standing rule 1: a test that cannot fail is not a test.  R = REAL known-bads / known answers
on untampered objects, S = synthetic tamper.  Every refusal control checks WHICH clause
fired, so that a control cannot pass because the checker refused for an unrelated reason.

  R1  real wrong Laurent polynomials (a forgotten square in the derivation of s7_b; s7_a
      with a square dropped; the s10 polynomial for s7; the Franel polynomial for s10, which
      AGREES at n = 0, 1 and first fails at n = 2) -> `ct_mismatch`, and NO geometry is
      computed for a refused P.
  R2  cross-family: the torus critical values of the s7 models against the s10 loci, and
      conversely -> `critical_value_not_a_certified_locus` (and the missing-locus clause).
  R3  degenerate critical point, P = (x-1)^3 + (y-1)^2 + (z-1)^2 + 5: one critical point,
      Hessian rank 2 -> NOT Morse, clause `hessian_degenerate`.
  R4  REAL known-bad for the inference "signature changes => operator singular":
      s7_b at lambda = 2.  The member's signature differs from the generic one, z = 1/2 is
      NOT a singular point of L3 (C1 certificate), and the checker must say
      `model_special_but_operator_regular` -- and must not list it as a locus.  The lattice
      certificate's row for z = 1/2 is read to record that it is a non-reflective CM point.
  R5  non-vacuity: P = x + y + z + 1/(xyz) has exactly 4 critical points on the torus,
      values 4*(fourth roots of unity), all Morse.
  R6  non-isolated critical points with P != 0: P = (xy-1)^2 + z + 1/z + 5
      -> `critical_locus_not_zero_dimensional`.
  R7  s7_a is not a (2,2,2) surface -> leg K says `not_a_222_surface` (no closure claimed).
  R8  the member lambda = 0 (z = infinity) of s7_b and s10_a -> `singular_locus_not_isolated`:
      the reason z = infinity is NOT EXAMINED is itself machine-checked.
  R9  the headline observations (each could have come out otherwise):
      s7: no torus critical point over z = -1 in either model; one Morse point over 1/27;
      s7_b at lambda = -1: 5 singular points against 7 generic, one of Hessian rank 1;
      s10: one Morse point over 1/16, two over -1/4, conjugate over Q(i).
  R10 completeness (second CAS): a scan list that omits lambda = -1 and 2 of s7_b is caught by
      leg C -> `complete_special_set_differs_from_scan`, naming the omitted members; on the
      pencil shifted by 100 leg C returns {99, 102, 127}, all outside the scanned window, so
      it does not read the scan list.  With the full list the comparison is clean.
  S1  s10 polynomial + x -> `ct_mismatch`.
  S2  s10 polynomial + x^3: agrees with the sequence for n <= 3 and fails at n = 4 -- a CT
      check of too low an order ACCEPTS a wrong P (order 3 passes, order 10 refuses).
  S3  tampered loci (1/27 -> 1/28) -> both comparison clauses.
  S4  probes that include the special member lambda = 2 -> `probes_disagree_on_generic_signature`.
  S5  Singular absent (simulated) -> `singular_leg_not_run`, legs CT/T/Z/K unaffected.
  S6  arnold_label: a (corank, Milnor number) outside the cases met -> `unlabelled`.
  S7  root-system arithmetic of the remark: exactly two roots (+-) of D4 orthogonal to three
      mutually orthogonal roots, index 2; none of A2 orthogonal to a root; the norm of the
      sum of two orthogonal roots is COMPUTED from the Gram matrix (and the two are orthogonal).
  S8  exactness: P = x+1/x+y+1/y+z+1/z+21 has the critical value 27 (z = 1/27 matched);
      with 21 + 10^-20 the value is 27 + 10^-20 and must NOT be matched with the locus 1/27
      -> both comparison clauses.  (sp.nsimplify, used before review, maps it to 27.)
      Floats are refused in an exact comparison.
  S9  refs cross-check: one tampered refs term -> `refs_mismatch` with its index.
  S10 the brief refuses to render from a certificate that no longer supports its prose
      -> BriefStale `brief_prose_not_supported_by_certificate` (E-015 guard).

Run:  python3 checkers/test_nodality_explicit_models_controls.py   (or pytest)
"""
import json
import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_nodality_explicit_models as C  # noqa: E402

x, y, z = C.VARS
ONE = sp.Integer(1)


def test_R1_wrong_polynomials_refused():
    for name, m in C.KNOWN_BAD_MODELS.items():
        r = C.analyse_model(name, m, C.load_loci(m["family"]), quick=True, with_singular=False)
        assert r["verdict"] == "REFUSED" and r["clause"] == "ct_mismatch", (name, r["clause"])
        assert r["ct"]["first_mismatch_index"] is not None
        assert "torus" not in r and "closure" not in r, "geometry computed for a refused P"
    late = C.check_ct(C.KNOWN_BAD_MODELS["franel_polynomial_for_s10"])
    assert late["first_mismatch_index"] == 2, late      # survives n = 0, 1
    assert C.check_ct(C.KNOWN_BAD_MODELS["franel_polynomial_for_s10"], order=1)["clause"] is None
    for name, m in C.MODELS.items():            # non-vacuity: the admitted ones pass
        assert C.check_ct(m)["clause"] is None, name


def test_R2_cross_family():
    s7 = C.torus_critical_points(C.MODELS["s7_b"]["N"], C.MODELS["s7_b"]["D"])["points"]
    s10 = C.torus_critical_points(C.MODELS["s10_a"]["N"], C.MODELS["s10_a"]["D"])["points"]
    a = C.compare_with_loci(s7, C.load_loci("cooper_s10"))
    b = C.compare_with_loci(s10, C.load_loci("cooper_s7"))
    for r in (a, b):
        assert "critical_value_not_a_certified_locus" in r["clauses"], r
        assert "certified_locus_without_torus_critical_point" in r["clauses"], r
    ok = C.compare_with_loci(s10, C.load_loci("cooper_s10"))
    assert ok["clauses"] == [], ok            # right family: clean


def test_R3_degenerate_critical_point():
    P = (x - 1) ** 3 + (y - 1) ** 2 + (z - 1) ** 2 + 5
    r = C.torus_critical_points(sp.expand(P), ONE)
    assert r["verdict"] == "OK" and len(r["points"]) == 1, r
    p = r["points"][0]
    assert p["point"] == ["1", "1", "1"] and p["hessian_rank"] == 2
    assert p["morse"] is False and p["clause"] == "hessian_degenerate"


def test_R4_signature_change_without_operator_singularity():
    N = C.MODELS["s7_b"]["N"]
    loci = C.load_loci("cooper_s7")
    assert "1/2" not in loci
    k = C.scan_222(N, [sp.Integer(l) for l in C.PROBES] + [sp.Integer(2)], loci)
    assert k["verdict"] == "OK" and list(k["special"]) == ["2"], k.get("special")
    sp2 = k["special"]["2"]
    assert sp2["clause"] == "model_special_but_operator_regular"
    assert sp2["z_is_certified_locus"] is False
    assert sp2["kinds"] == ["boundary_point_hessian_rank_drops"]
    row = C.load_lattice_side("cooper_s7")["rational_z"]["1/2"]
    assert row["reflective"] is False and row["minus_v2"] != 2


def test_R5_morse_toy_non_vacuity():
    r = C.torus_critical_points(sp.expand(x * y * z * (x + y + z) + 1), x * y * z)
    assert r["verdict"] == "OK" and len(r["points"]) == 4
    assert all(p["morse"] for p in r["points"])
    assert sorted(p["critical_value"] for p in r["points"]) == sorted(["4", "-4", "4*I", "-4*I"])


def test_R6_non_isolated_critical_points():
    P = (x * y - 1) ** 2 + z + 1 / z + 5
    r = C.torus_critical_points(sp.expand(P * z), z)
    assert r["verdict"] == "REFUSED" and r["clause"] == "critical_locus_not_zero_dimensional"


def test_R7_not_222():
    m = C.MODELS["s7_a"]
    assert C.is_222(m["N"], m["D"]) is False
    assert C.is_222(C.MODELS["s7_b"]["N"], C.MODELS["s7_b"]["D"]) is True


def test_R8_z_infinity_member_not_isolated():
    for name in ("s7_b", "s10_a"):
        r = C.singular_points_222(C.MODELS[name]["N"], sp.Integer(0))
        assert r["verdict"] == "REFUSED" and r["clause"] == "singular_locus_not_isolated", name
        assert C.value_zero_locus(C.MODELS[name]["N"], C.MODELS[name]["D"])["positive_dimensional"]


def test_R9_headline_observations():
    for name in ("s7_a", "s7_b"):
        pts = C.torus_critical_points(C.MODELS[name]["N"], C.MODELS[name]["D"])["points"]
        assert [(p["z"], p["morse"]) for p in pts] == [("1/27", True)], (name, pts)
    N = C.MODELS["s7_b"]["N"]
    gen = C.signature(C.singular_points_222(N, sp.Integer(3))["points"])
    m1 = C.signature(C.singular_points_222(N, sp.Integer(-1))["points"])
    assert gen == [7, [2, 3, 3, 3, 3, 3, 3]] and m1 == [5, [1, 2, 3, 3, 3]], (gen, m1)
    pts = C.torus_critical_points(C.MODELS["s10_a"]["N"], C.MODELS["s10_a"]["D"])["points"]
    per = {}
    for p in pts:
        per.setdefault(p["z"], []).append(p)
    assert {k: len(v) for k, v in per.items()} == {"1/16": 1, "-1/4": 2}
    assert all(p["morse"] for p in pts)
    assert sorted(p["point"][0] for p in per["-1/4"]) == ["-I", "I"]
    assert all(not p["rational"] for p in per["-1/4"])


def test_S1_tampered_polynomial():
    m = dict(C.MODELS["s10_a"], N=C.MODELS["s10_a"]["N"] + x)
    r = C.check_ct(m)
    assert r["clause"] == "ct_mismatch"


def test_S2_low_order_ct_accepts_a_wrong_P():
    m = dict(C.MODELS["s10_a"], N=sp.expand(C.MODELS["s10_a"]["N"] + x ** 4 * y * z))  # P + x^3
    assert C.check_ct(m, order=3)["clause"] is None
    r = C.check_ct(m, order=C.CT_ORDER)
    assert r["clause"] == "ct_mismatch" and r["first_mismatch_index"] == 4, r


def test_S3_tampered_loci():
    pts = C.torus_critical_points(C.MODELS["s7_b"]["N"], C.MODELS["s7_b"]["D"])["points"]
    r = C.compare_with_loci(pts, ["-1", "1/28"])
    assert r["extra"] == ["1/27"] and "1/28" in r["missing"]
    assert set(r["clauses"]) == {"critical_value_not_a_certified_locus",
                                 "certified_locus_without_torus_critical_point"}


def test_S4_probes_disagree():
    old = C.PROBES
    try:
        C.PROBES = [3, 2, 5]
        k = C.scan_222(C.MODELS["s7_b"]["N"], [sp.Integer(l) for l in C.PROBES],
                       C.load_loci("cooper_s7"))
    finally:
        C.PROBES = old
    assert k["verdict"] == "REFUSED" and k["clause"] == "probes_disagree_on_generic_signature"


def test_S5_second_cas_absent():
    old = C.shutil.which
    try:
        C.shutil.which = lambda _: None
        r = C.singular_leg(C.MODELS["s10_a"]["N"], [sp.Integer(3)], [])
    finally:
        C.shutil.which = old
    assert r == {"verdict": "NOT_RUN", "clause": "singular_leg_not_run"}


def test_S6_label_outside_cases():
    assert C.arnold_label(2, 6) == "unlabelled" and C.arnold_label(3, 8) == "unlabelled"
    assert C.arnold_label(0, 1) == "A1" and C.arnold_label(1, 4) == "A4" and C.arnold_label(2, 4) == "D4"


def test_S7_root_arithmetic():
    r = C.root_system_remark()
    assert r["D4_number_of_roots"] == 24 and r["A2_number_of_roots"] == 6
    assert r["e_i_gram"] == [[-2, 0, 0], [0, -2, 0], [0, 0, -2]]
    assert len(r["roots_of_D4_orthogonal_to_all_e_i"]) == 2
    assert r["index_of_A1^3_plus_that_root_in_D4"] == 2
    assert r["roots_of_A2_orthogonal_to_a_root"] == []
    assert r["their_pairing"] == 0
    a, b = r["two_orthogonal_roots_used"]
    D4 = [[-2, 1, 1, 1], [1, -2, 0, 0], [1, 0, -2, 0], [1, 0, 0, -2]]
    q = lambda u, v: sum(u[i] * D4[i][j] * v[j] for i in range(4) for j in range(4))
    assert q(a, a) == q(b, b) == -2 and q(a, b) == 0
    assert r["sum_of_two_orthogonal_roots_has_norm"] == q(a, a) + q(b, b) + 2 * q(a, b) == -4


def test_R10_completeness_leg_catches_an_incomplete_scan():
    N = C.MODELS["s7_b"]["N"]
    loci = C.load_loci("cooper_s7")
    cleg = C.completeness_leg(N)
    if cleg["verdict"] == "NOT_RUN":
        assert cleg["clause"] == "singular_leg_not_run"
        return
    short = C.scan_222(N, [sp.Integer(l) for l in C.PROBES] + [sp.Integer(27)], loci)
    r = C.compare_complete_with_scan(short, {}, cleg)
    assert r["agree"] is False and r["clause"] == "complete_special_set_differs_from_scan", r
    assert r["in_complete_set_not_in_scan_special"] == ["-1", "2"], r
    full = C.scan_222(N, [sp.Integer(l) for l in C.PROBES + [27, -1, 2]], loci)
    ok = C.compare_complete_with_scan(full, {}, cleg)
    assert ok["agree"] is True and ok["clause"] is None, ok
    shifted = C.completeness_leg(N, shift=100)
    assert shifted["lambda_where_total_tjurina_differs_from_generic"] == ["99", "102", "127"], shifted
    assert shifted["lambda_with_non_isolated_singular_points"] == ["100"]
    assert all(int(k) not in C.INT_SCAN for k in ["99", "102", "127"])


def test_S8_near_miss_is_not_matched():
    eps = sp.Rational(1, 10 ** 20)
    assert C._simp(27 + eps) != 27 and not C._is_zero(eps) and C._is_zero(sp.sqrt(2) ** 2 - 2)
    assert not C.same_number(str(1 / (27 + eps)), "1/27") and C.same_number("2/54", "1/27")
    base = x * y * z * (x + 1 / x + y + 1 / y + z + 1 / z)
    good = C.torus_critical_points(sp.expand(base + 21 * x * y * z), x * y * z)["points"]
    assert len(good) == 8 and "1/27" not in C.compare_with_loci(good, ["1/27"])["missing"]
    near = C.torus_critical_points(sp.expand(base + (21 + eps) * x * y * z), x * y * z)["points"]
    r = C.compare_with_loci(near, ["1/27"])
    assert len(near) == 8 and r["missing"] == ["1/27"] and len(r["extra"]) == 4, r
    assert set(r["clauses"]) == {"critical_value_not_a_certified_locus",
                                 "certified_locus_without_torus_critical_point"}
    try:
        C.same_number("0.037037", "1/27")
    except ValueError:
        pass
    else:
        raise AssertionError("a float was accepted in an exact comparison")


def test_S9_tampered_refs_term():
    ref = json.loads(C.REFS.read_text())["sequences"]["cooper_s7"]["initial_terms"]
    assert C.refs_crosscheck("cooper_s7", ref)["agree"] is True
    bad = list(ref)
    bad[5] = int(bad[5]) + 1
    r = C.refs_crosscheck("cooper_s7", bad)
    assert r["agree"] is False and r["clause"] == "refs_mismatch" and r["first_mismatch_index"] == 5


def test_S10_brief_refuses_stale_prose():
    import copy
    cert = json.loads(C.OUT.read_text())
    assert "post hoc" in C.brief_text(cert)                     # untampered: renders
    for tamper, needle in (
            (lambda c: c["models"]["s7_b"]["closure"]["special"]["-1"]["points"].append(
                dict(c["models"]["s7_b"]["closure"]["special"]["27"]["points"][0], on_torus=True)),
             "z = -1"),
            (lambda c: c["models"]["s10_a"]["closure"]["special"].pop("-4"), "s10_a special members"),
            (lambda c: c["controls_file"].update(number_of_controls=3), "controls named")):
        c2 = copy.deepcopy(cert)
        tamper(c2)
        try:
            C.brief_text(c2)
        except C.BriefStale as e:
            assert "brief_prose_not_supported_by_certificate" in str(e) and needle in str(e), e
        else:
            raise AssertionError(f"stale certificate rendered ({needle})")


if __name__ == "__main__":
    tests = [(k, v) for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for k, f in tests:
        try:
            f()
            print(f"ok    {k}")
        except Exception as e:  # noqa: BLE001 - an error in a control is a failure, not a crash
            failed += 1
            print(f"FAIL  {k}: {e}")
    print(json.dumps({"controls": len(tests), "failed": failed}))
    sys.exit(1 if failed else 0)
