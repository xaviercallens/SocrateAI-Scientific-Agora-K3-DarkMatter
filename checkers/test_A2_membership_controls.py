#!/usr/bin/env python3
"""
test_A2_membership_controls.py -- negative controls for check_A2_membership.py.

Standing rule 1: a test that cannot fail is not a test.  House style of
test_T3_level_consistency_controls.py: R = REAL known-bads / known answers on untampered
data, S = synthetic tamper.  Every control that expects a refusal or a negative verdict
also checks WHICH clause fired.

  R-controls
    R1  REAL known-negative: A2 at n = 10 -> ABSENT, fired `D_not_square_mod_4n`, and the
        box holds no vector of discriminant -3.
    R2  REAL known-negative in the other direction: the square lattice (1,0,1), D = -4, at
        n = 7 -> ABSENT on the same clause; so the checker is not an n = 10 detector.
    R3  non-vacuity: A2 at n = 7 -> PRESENT, and (1,0,1) at n = 10 -> PRESENT (the n = 10
        machinery can say yes), each fired `explicit_vector_with_target_form`.
    R4  known answers from sources other than this checker: Stream 1's g3-fixed vector
        (14,-14,5) (ModularAction.lean, read as source) has v^perp = A2 with div 14; the
        P2 certificate has an A2 row for s7 and none for s10.
    R5  the Gamma_0(7) stabilizer search is not constant: order 3 at the A2 point, order 1
        (nothing found within the bound) at a D = -19 point.
  S-controls
    S1a WRONG LATTICE: the Gauss discriminant lattice G0N = Gram(b^2 - 4Nac) of Stream 1's
        no_isometry_G0N_TN, fed in place of T_n -> refused, clause `lattice_not_even`
        (the determinant path is NOT exercised by this one; S1b does that).
    S1b an EVEN lattice carrying the Gauss determinant -4n^2 (= U + <4n^2>) -> refused,
        clause `lattice_level_mismatch`.  Also computed: had it been silently accepted,
        the s7 headline would flip (criterion at n' = 2n^2 = 98 says ABSENT), which is
        why the refusal matters.
    S1p the same two wrong lattices through the PRODUCTION call path: the registry entry
        T3.CANDIDATES[key]["lattice_cert"] is swapped (and restored) and run_family's own
        first two calls are made, family_level(key) then level_relation(key, n).  G0N ->
        `lattice_leg_refused` (T3's evenness refusal, now carrying a clause); the even
        lattice of Gauss determinant passes the lattice leg with n' = 2n^2 and is stopped
        by `no_level_coordinate`.  A lattice of ANOTHER family's level (s7's registry entry
        pointed at the s10 certificate) -> `relation_not_certified`.
    S2  tampered criterion (squares modulo 4(n+1) instead of 4n, i.e. the wrong level) ->
        leg (C) refuses, clause `enumeration_outside_criterion` or
        `criterion_not_reached_in_box`; which one fired is reported.  [A first draft
        tampered 4n -> 2n.  At n = 7 that is NOT a tamper: for D = 0, 1 mod 4 and n odd,
        'square mod 2n' and 'square mod 4n' coincide, and leg (C) rightly did not fire.
        Kept below as S2x, asserted for what it is.]
    S3  box too small (|coords| <= 3) -> `criterion_not_reached_in_box`: the bounded
        inclusion of leg (C) can fail.
    S4  witness with y + 1 -> `witness_fails`.
    S5  PRESENT is not awarded on the discriminant alone: target (1,0,5), D = -20, at
        n = 7 (D admitted, only the class (2,2,3) is seen) -> verdict
        D_OCCURS_FORM_NOT_FOUND, fired `form_class_not_matched`.
    S6  per-vector congruence against the wrong modulus: a v^perp computed at n = 7,
        checked at n = 10 -> `divisibility_structure` or `congruence_violated`.
    S6b the same at box scale: box_enumeration(n = 7, check_n = 10) COUNTS violations (the
        production count is a computed number, and it can be non-zero); untampered, 0.
    S7  tampered relation (beta + 1): 1/z is no longer 0 at the A2 point -> the z = infinity
        gate refuses on `w_not_zero`, and point_data no longer reports z = infinity.
    S8  non-reduced target -> `target_not_reduced`.
    S9  citation of a name that is not in the cited Lean file -> PHANTOM.
    S10 the exit-code gate: checks_ok({.. False ..}) is False (Python has False == 0; a
        first version of the gate tested `v == 0` and would have passed a failed boolean),
        and a non-zero violation count is not ok either.
    S11 the brief is rendered from the certificate: a tampered certificate dict (headline
        verdicts swapped, order changed) changes the rendered text accordingly, and the
        brief on disk equals render_brief(certificate on disk).

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: python3 + pytest, this file
Reviewed-by: N
"""
import copy
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_A2_membership as A2  # noqa: E402

CM = A2.CM
results = []
SMALL_BOX = 60            # controls use a smaller box than production; stated in each detail


def record(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"  {'ok  ' if ok else 'FAIL'}  {name}" + (f"  -- {detail}" if detail else ""))


def refusal_clause(fn):
    try:
        fn()
    except A2.Refused as e:
        return e.clause
    return None


def main():
    print("=" * 78)
    print("A2-membership controls")
    print("=" * 78)
    n7, _ = A2.family_level("cooper_s7")
    n10, _ = A2.family_level("cooper_s10")
    enum = {n7: A2.box_enumeration(n7, SMALL_BOX), n10: A2.box_enumeration(n10, SMALL_BOX)}
    A2form, SQ = (1, 1, 1), (1, 0, 1)

    print("\nR -- real known-bads / known answers (untampered)")
    m = A2.membership(n10, A2form, enum[n10])
    record("R1 A2 at n = 10 is ABSENT, on the congruence clause",
           m["verdict"] == "ABSENT" and m["fired"] == "D_not_square_mod_4n"
           and -3 not in enum[n10]["by_D"],
           f"fired {m['fired']}; -3 mod {4 * n10} = {m['D_mod_4n']} not in {m['squares_mod_4n']}; "
           f"box {SMALL_BOX}: {enum[n10]['vectors_checked']} vectors, none with D = -3")
    m = A2.membership(n7, SQ, enum[n7])
    record("R2 (1,0,1) at n = 7 is ABSENT, on the congruence clause",
           m["verdict"] == "ABSENT" and m["fired"] == "D_not_square_mod_4n"
           and -4 not in enum[n7]["by_D"], f"fired {m['fired']}; D mod 4n = {m['D_mod_4n']}")
    for n, form in ((n7, A2form), (n10, SQ)):
        m = A2.membership(n, form, enum[n])
        record(f"R3 {form} at n = {n} is PRESENT (non-vacuity)",
               m["verdict"] == "PRESENT" and m["fired"] == "explicit_vector_with_target_form",
               f"fired {m['fired']}; v = {m.get('v')}")
    TX = CM.transcendental_lattice(n7, (14, -14, 5))
    record("R4 Stream 1's g3-fixed vector (14,-14,5): v^perp = A2, div 14",
           tuple(TX["reduced_form"]) == A2form and TX["div_v"] == 14, str(TX["reduced_form"]))
    p2 = A2.CERTS / A2.P2_CERT
    if p2.exists():
        fams = json.loads(p2.read_text())["families"]
        has = {k: any(tuple(R["T_X_reduced_form_abc"]) == A2form for R in f["rows"])
               for k, f in fams.items()}
        record("R4 P2 certificate: an A2 row for s7, none for s10",
               has == {"cooper_s7": True, "cooper_s10": False}, str(has))
    else:
        print("  SKIPPED  R4 P2 certificate absent")
    st3 = A2.stabilizer(n7, (14, -14, -5))
    v19 = enum[n7]["by_D"][-19]["forms"][(1, 1, 5)]
    st1 = A2.stabilizer(n7, v19)
    record("R5 Gamma_0(7) stabilizer: order 3 at the A2 point, trivial at a D = -19 point",
           st3["order_in_PSL2"] == 3 and st1["order_in_PSL2"] == 1 and not st1["elements"],
           f"A2: {st3['elements'][:1]}; D=-19 v = {v19}: {st1['elements']}")

    print("\nS -- synthetic tamper (each must refuse / downgrade, on the named clause)")
    _td = tempfile.TemporaryDirectory(prefix="a2_controls_")     # outside the repo tree
    tmp = Path(_td.name) / "_a2_control_cert.json"

    def production_clause(key, cert_path):
        """run_family's own first two calls, with the registry entry swapped and restored."""
        spec = A2.T3.CANDIDATES[key]
        saved = spec["lattice_cert"]
        spec["lattice_cert"] = str(cert_path)        # CERTS / <absolute path> = that path
        try:
            def go():
                n, _ = A2.family_level(key)
                A2.level_relation(key, n)
            return refusal_clause(go)
        finally:
            spec["lattice_cert"] = saved
    for key, n in (("cooper_s7", n7), ("cooper_s10", n10)):
        tmp.write_text(json.dumps({"derived": {
            "gram_primitive_even": [[0, 0, -2 * n], [0, 1, 0], [-2 * n, 0, 0]],
            "u_splitting": {"basis_change_matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}}}))
        cl = refusal_clause(lambda: A2.family_level(key, lattice_cert=tmp))
        record(f"S1a G0N (b^2 - 4*{n}ac) in place of T_{n} is refused on `lattice_not_even`",
               cl == "lattice_not_even", f"fired {cl}")
        cl = production_clause(key, tmp)
        record(f"S1p G0N through the production path ({key}) is refused on "
               "`lattice_leg_refused`", cl == "lattice_leg_refused", f"fired {cl}")
        d = 4 * n * n
        tmp.write_text(json.dumps({"derived": {
            "gram_primitive_even": [[0, 0, -1], [0, d, 0], [-1, 0, 0]],
            "u_splitting": {"basis_change_matrix": [[1, 0, 0], [0, 0, 1], [0, -1, 0]]}}}))
        cl = refusal_clause(lambda: A2.family_level(key, lattice_cert=tmp))
        record(f"S1b even lattice of Gauss determinant {-d} in place of T_{n} is refused on "
               "`lattice_level_mismatch`", cl == "lattice_level_mismatch", f"fired {cl}")
        cl = production_clause(key, tmp)
        record(f"S1p even lattice of Gauss determinant {-d} through the production path ({key}) "
               "is refused on `no_level_coordinate`", cl == "no_level_coordinate", f"fired {cl}")
    cl = production_clause("cooper_s7", A2.CERTS / A2.T3.CANDIDATES["cooper_s10"]["lattice_cert"])
    record("S1p s7's registry entry pointed at the s10 lattice certificate: "
           "`relation_not_certified`", cl == "relation_not_certified", f"fired {cl}")
    record("S1p non-vacuity: the untampered registry passes both production calls, and the "
           "registry was restored",
           all(production_clause(k, A2.CERTS / A2.T3.CANDIDATES[k]["lattice_cert"]) is None
               for k in ("cooper_s7", "cooper_s10"))
           and A2.family_level("cooper_s7")[0] == n7 and A2.family_level("cooper_s10")[0] == n10)
    flip = A2.criterion(n7, -3) and not A2.criterion(2 * n7 * n7, -3)
    record("S1b why it matters: silently accepted, the s7 headline would flip "
           "(criterion true at n = 7, false at n' = 98)", flip,
           f"-3 mod {8 * n7 * n7} = {(-3) % (8 * n7 * n7)}")

    fired = {}
    for n in (n7, n10):
        fired[n] = refusal_clause(lambda: A2.discriminant_table(n, enum[n],
                                                                modulus=lambda k: 4 * (k + 1)))
    record("S2 criterion tampered to 'square mod 4(n+1)': leg (C) refuses",
           all(c in ("enumeration_outside_criterion", "criterion_not_reached_in_box")
               for c in fired.values()), f"fired {fired}")
    fx = {n: refusal_clause(lambda: A2.discriminant_table(n, enum[n], modulus=lambda k: 2 * k))
          for n in (n7, n10)}
    record("S2x 'square mod 2n' is a real tamper at n = 10 (even) and no tamper at n = 7 (odd)",
           fx[n7] is None and fx[n10] is not None, f"fired {fx}")
    record("S2 non-vacuity: the untampered criterion passes leg (C) on the same box",
           all(refusal_clause(lambda: A2.discriminant_table(n, enum[n])) is None
               for n in (n7, n10)), f"box {SMALL_BOX}")
    tiny = A2.box_enumeration(n7, 3)
    cl = refusal_clause(lambda: A2.discriminant_table(n7, tiny))
    record("S3 box |coords| <= 3: `criterion_not_reached_in_box`",
           cl == "criterion_not_reached_in_box", f"fired {cl}")
    cl = refusal_clause(lambda: A2.construct_witnesses(n7, -3,
                                                       tamper=lambda v: (v[0], v[1] + 1, v[2])))
    record("S4 witness with y + 1: `witness_fails`", cl == "witness_fails", f"fired {cl}")

    m = A2.membership(n7, (1, 0, 5), enum[n7])
    record("S5 target (1,0,5) at n = 7: D = -20 is admitted but PRESENT is NOT awarded",
           m["verdict"] == "D_OCCURS_FORM_NOT_FOUND" and m["fired"] == "form_class_not_matched"
           and A2.criterion(n7, -20),
           f"fired {m['fired']}; classes seen {m.get('lattice_classes_seen')} "
           f"(bounded: witnesses + box {SMALL_BOX})")

    v = (14, -14, -5)
    TX7 = CM.transcendental_lattice(n7, v)
    cl = refusal_clause(lambda: A2.check_vector_congruence(n10, v, TX7))
    record("S6 n = 7 data checked against the n = 10 congruence is refused",
           cl in ("divisibility_structure", "congruence_violated"), f"fired {cl}")
    record("S6 non-vacuity: the same data passes at n = 7",
           refusal_clause(lambda: A2.check_vector_congruence(n7, v, TX7)) is None)

    wrong = A2.box_enumeration(n7, 10, check_n=n10)
    right = A2.box_enumeration(n7, 10)
    nviol = sum(wrong["violations"].values())
    record("S6b box scale: n = 7 vectors against the n = 10 congruence -> violations are COUNTED",
           nviol > 0 and not right["violations"]
           and right["det_identity_held_on"] == right["vectors_checked"] > 0,
           f"box 10: {nviol} of {wrong['vectors_checked']} by clause {wrong['violations']}; "
           f"untampered {right['violations'] or 0}")

    rel, r = CM.relation_for("cooper_s7", n7)
    bad = dict(rel)
    bad["beta"] = rel["beta"] + 1
    cl = refusal_clause(lambda: A2.assert_w_zero(n7, v, bad, r))
    record("S7 tampered relation (beta + 1): the z = infinity gate refuses on `w_not_zero`",
           cl == "w_not_zero", f"fired {cl}")
    P = A2.point_data("cooper_s7", n7, v, bad, r)
    record("S7 ... and point_data then does not report z = infinity", P["z"] != "infinity",
           f"z read as {P['z']}")
    good = A2.point_data("cooper_s7", n7, v, rel, r)
    record("S7 non-vacuity: untampered, z = infinity with the exact t-support, and the point "
           "record carries the relation and its finite order",
           good["z"] == "infinity" and good["relation_order_checked"] == CM.ORDER
           and good["relation_verdict"] == f"PASS({CM.ORDER})"
           and good["relation_1_over_z"] == {k: str(x) for k, x in rel.items()}
           and good["t_exact_support"]["alpha_t2_plus_beta_t_plus_gamma_proportional_to_it"])

    cl = refusal_clause(lambda: A2.membership(n7, (3, 1, 1), enum[n7]))
    record("S8 non-reduced target: `target_not_reduced`", cl == "target_not_reduced",
           f"fired {cl}")

    cit = dict(A2.EXTERNAL_CITATIONS["leanmaster_target"])
    cit["paths"] = {"DualScaleDyons/AttractorCharges.lean": "reducedForms 3 = [(1, 0, 1)]"}
    c = CM.verify_citation(cit)
    if c["status"] == "REPO_UNAVAILABLE":
        print("  SKIPPED  S9 LeanMaster checkout not available on this machine")
    else:
        record("S9 a statement that is NOT in the cited Lean file -> PHANTOM",
               c["status"] == "PHANTOM", str(list(c["paths"].values())))

    record("S10 exit gate: a False check is not read as the count 0",
           A2.checks_ok({"a": True, "c": 0}) and not A2.checks_ok({"a": False, "c": 0})
           and not A2.checks_ok({"a": True, "c": 3}) and not A2.checks_ok({"a": None}))

    if A2.OUT.exists():
        cert = json.loads(A2.OUT.read_text())
        base = A2.render_brief(cert)
        tam = copy.deepcopy(cert)
        f = tam["families"]["cooper_s7"]
        f["point"]["relation_order_checked"] = 7
        f["point"]["relation_verdict"] = "PASS(7)"
        f["box"]["primitive_negative_norm_vectors_checked"] = 123454321
        tb = A2.render_brief(tam)
        record("S11 the brief follows the certificate (tampered order and count show up)",
               "PASS(7)" in tb and "123454321" in tb and "PASS(7)" not in base
               and "123454321" not in base)
        if A2.BRIEF.exists():
            record("S11 the brief on disk equals render_brief(certificate on disk)",
                   A2.BRIEF.read_text() == base)
        else:
            print("  SKIPPED  S11 brief not rendered yet")
    else:
        print("  SKIPPED  S11 certificate not emitted yet")
    _td.cleanup()

    bad_n = [nm for nm, ok, _ in results if not ok]
    print("-" * 78)
    print(f"{len(results) - len(bad_n)}/{len(results)} controls behaved as required")
    for nm in bad_n:
        print(f"  FAILED: {nm}")
    return 1 if bad_n else 0


def test_a2_membership_controls():
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())
