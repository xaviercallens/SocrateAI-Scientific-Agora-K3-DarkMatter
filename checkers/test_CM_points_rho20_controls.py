#!/usr/bin/env python3
"""
test_CM_points_rho20_controls.py -- negative controls for check_CM_points_rho20.py.

Standing rule 1: a test that cannot fail is not a test.  House style of
test_T3_level_consistency_controls.py: R = REAL known-bads / known-answers on untampered
data, S = synthetic tamper.  Every refusal control also checks WHICH clause fired, so a
control cannot pass because the checker refused for some unrelated reason.

  R-controls
    R0  non-vacuity of the inverse search: from the NUMERICAL tau of a CM point alone,
        vectors_annihilating() returns the integer vector.
    R1  non-CM tau: a cubic-irrational tau (Re 1/3, Im 2^(1/3)/2) and a tau with
        imaginary part pi/7 must yield NO primitive integer vector with x <= X_MAX, at
        either level (so the orthogonal complement of the period stays of rank 3 within
        the searched range -- a bounded statement, quoted with its bound).
    R2  wrong level, both directions, FAMILY-LEVEL: the s7 relation and level-7 coordinate
        run over the vectors of the n = 10 lattice (and conversely).  What must break is the
        checker's own gate `fricke_consistency` (z(tau_v) = z(tau_{-swap v}): swap is the
        Fricke involution of the LATTICE's n, and z is invariant under the Fricke involution
        of the MODULAR side's level only), and the fraction distinct-z / vectors must rise
        (orbits no longer collapse).  At the right level both gates are clean (non-vacuity).
        The same-z => same-form and same-z => same-(norm, div) counts at the wrong level
        are REPORTED, not asserted: independent review measured them at 3 and 0, i.e. they
        are not a reliable wrong-level detector, and this file does not pretend otherwise.
        [An earlier R2 evaluated one relation at the other lattice's Fricke point
        tau = i/sqrt(n_wrong).  Review showed that isolates nothing: i/sqrt(10) is a genuine
        CM point of the n = 7 lattice, v = (10,-7,0), -v^2 = 140 -- recomputed below as
        R2x so the reason for the replacement is itself machine-checked.]
    R3  known answers from sources other than this checker:
        - the C1 certificates' finite singular loci are all reproduced by the enumeration;
        - Stream 1's root2 = (-2,4,1) (ModularAction.lean, commit 3a96018, read as source,
          no Lean build run), taken as -root2, gives z = -1 with D = -7;
        - Stream 1's order-3 fixed vector (14,-14,5), norm -42, gives z = infinity with
          T_X = (1,1,1), D = -3, and is NOT reflective.
    R5  REAL known-bad citation: commit ede49f0 of LeanMaster, which an earlier draft of
        the checker, brief and certificate cited for sec G10 / FrickeRepair.lean, must be
        reported PHANTOM by verify_citation (clause `absent_at_commit` or name-not-found),
        while the corrected commit is VERIFIED.  If the sibling repo is not checked out
        the control says SKIPPED loudly; S10 is the always-runnable twin.
  S-controls (each must REFUSE, on the named clause)
    S1  kernel basis with one entry changed        -> kernel_not_orthogonal
    S2  v with v^2 > 0, and v with v^2 = 0          -> no_upper_half_plane_root
    S3  kernel basis with one vector doubled       -> kernel_not_saturated
    S4  non-primitive v                            -> v_not_primitive
    S5  dependent kernel basis                     -> kernel_wrong_rank
    S6  tampered relation (beta + 1)               -> the Fricke point no longer lands on a
        C1 locus (clause `locus_match`)
    S7  precision: recognition fitted at 60 digits / re-checked at 90 must AGREE with the
        production precision on the locus rows and on a degree-4 row; and a value whose
        re-check copy is perturbed at relative size 1e-50 must be REJECTED by the re-check
        (clause `recheck_at_higher_precision`) although the 60-digit fit alone accepts it.
    S8  the family-level gates can fire: two z-groups with different T_X merged into one
        -> `same_z_different_form`; two groups with different (-v^2, div) merged ->
        `same_z_different_norm_or_div`; relation with alpha + 1 -> `fricke_consistency`
        (beta + 1 is NOT used here: a constant shift of 1/z is Fricke-invariant, and the
        control says so by checking it).
    S9  the conjugates_in_table diagnostic can drop: for a row of degree d >= 2 with real z
        and d/d roots present, deleting every other row must leave fewer than d.
    S10 verify_citation on THIS repo: a path that does not exist -> PHANTOM /
        `absent_at_commit`; an existing file without the name -> PHANTOM / name-not-found;
        an existing file with the name -> VERIFIED.

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: python3 + pytest, this file
Reviewed-by: N
"""
import sys
from fractions import Fraction as F
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_CM_points_rho20 as CM  # noqa: E402

results = []
X_MAX = 400


def record(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"  {'ok  ' if ok else 'FAIL'}  {name}" + (f"  -- {detail}" if detail else ""))


def refusal_clause(fn):
    try:
        fn()
    except CM.Refused as e:
        return e.clause
    return None


def z_at(rel, r, tau, dps_fit=CM.DPS_FIT, dps_verify=CM.DPS_VERIFY, perturb=None):
    """Recognise z = 1/w at a numerical tau; returns the z record (or None)."""
    mp.mp.dps = dps_fit
    _, w_fit = CM.w_of_tau(rel, r, tau())
    mp.mp.dps = dps_verify
    _, w_ver = CM.w_of_tau(rel, r, tau())
    if perturb is not None:
        w_ver = w_ver * (1 + perturb)
    return CM.z_minpoly_from_w(CM.recognize_algebraic(w_fit, w_ver, dps_fit, dps_verify))


def main():
    print("=" * 78)
    print("CM-points (rho = 20) controls")
    print("=" * 78)
    ctx = {}
    for key in ("cooper_s7", "cooper_s10"):
        n = CM.T3.lattice_leg(CM.CERTS / CM.T3.CANDIDATES[key]["lattice_cert"])["n_lattice"]
        rel, r = CM.relation_for(key, n)
        loci = CM.json.loads((CM.CERTS / CM.LOCI_CERT[key]).read_text())["finite_singular_loci"]
        ctx[key] = (n, rel, r, loci)

    print("\nR -- real data, untampered")
    for key, v in (("cooper_s7", (2, -4, 1)), ("cooper_s10", (10, -10, -3))):
        n = ctx[key][0]
        mp.mp.dps = 80
        got = CM.vectors_annihilating(n, CM.tau_num(n, v), X_MAX)
        record(f"R0 {key}: numerical tau of v={v} gives back v (non-vacuity)", got == [v], str(got))

    def tau_cubic():
        return mp.mpc(mp.mpf(1) / 3, mp.cbrt(2) / 2)

    def tau_pi():
        return mp.mpc(mp.mpf(1) / 5, mp.pi / 7)

    for key in ctx:
        n = ctx[key][0]
        for nm, tf in (("cubic 1/3 + i 2^(1/3)/2", tau_cubic), ("1/5 + i pi/7", tau_pi)):
            mp.mp.dps = 80
            got = CM.vectors_annihilating(n, tf(), X_MAX)
            record(f"R1 {key}: non-CM tau = {nm} has NO integer v with x <= {X_MAX}",
                   got == [], f"clause no_integer_vector; found {got}")

    for key, other in (("cooper_s7", "cooper_s10"), ("cooper_s10", "cooper_s7")):
        n, rel, r, loci = ctx[key]
        n_wrong = ctx[other][0]
        stats = {}
        for label, nn in (("right", n), ("wrong", n_wrong)):
            vs = CM.enumerate_vectors(nn)
            groups = CM.group_by_z(nn, rel, r, vs)
            fv, ndv = CM.same_z_checks(nn, groups)
            stats[label] = {"vectors": len(vs), "groups": len(groups),
                            "fricke": len(CM.fricke_consistency(nn, rel, r, vs)),
                            "form": len(fv), "normdiv": len(ndv)}
        R_, W_ = stats["right"], stats["wrong"]
        record(f"R2 {key} relation over the n={n_wrong} lattice: gate fricke_consistency FIRES",
               W_["fricke"] > 0,
               f"clause fricke_consistency; {W_['fricke']}/{W_['vectors']} vectors violate")
        record(f"R2 {key} relation over the n={n_wrong} lattice: distinct-z fraction rises",
               W_["groups"] * R_["vectors"] > R_["groups"] * W_["vectors"],
               f"clause orbit_collapse; wrong {W_['groups']}/{W_['vectors']} vs right "
               f"{R_['groups']}/{R_['vectors']}; REPORTED ONLY: same-z/form {W_['form']}, "
               f"same-z/(norm,div) {W_['normdiv']} at the wrong level")
        record(f"R2 ... while over its own n={n} all three gates are clean (non-vacuity)",
               R_["fricke"] == R_["form"] == R_["normdiv"] == 0, str(R_))
        rec_ok = z_at(rel, r, lambda: CM.tau_num(n, (1, -1, 0)))
        record(f"R2 ... and its own Fricke point lands on a C1 locus",
               rec_ok is not None and rec_ok["z"] in loci, f"z = {rec_ok and rec_ok['z']}")
    # R2x: why the earlier point-wise wrong-level control was withdrawn
    n7 = ctx["cooper_s7"][0]
    n10 = ctx["cooper_s10"][0]
    mp.mp.dps = 80
    got = CM.vectors_annihilating(n7, CM.tau_num(n10, (1, -1, 0)), X_MAX)
    record("R2x the n=10 Fricke point IS a CM point of the n=7 lattice (so it cannot serve as a "
           "wrong-level probe)", len(got) == 1 and CM.norm(n7, got[0]) < 0,
           f"v = {got}, -v^2 = {[-CM.norm(n7, g) for g in got]} (beyond BOUND = {CM.BOUND})")

    fams20 = {}
    for key in ctx:
        fam = fams20[key] = CM.family(key, bound=20)
        hits = CM.locus_hits(fam)
        record(f"R3 {key}: every C1 finite singular locus {ctx[key][3]} is reproduced "
               "(enumeration, bound 20)", all(l in hits for l in ctx[key][3]),
               "; ".join(f"{l} <- v={h[0]['v']}, D={h[0]['D']}" for l, h in sorted(hits.items())))
    n, rel, r, _ = ctx["cooper_s7"]
    row, _ = CM.point_record(n, (2, -4, -1), rel, r)
    record("R3 Stream 1 root2 (as -root2 = (2,-4,-1)): z = -1, D = -7, reflective",
           row["z_value_if_rational"] == "-1" and row["D"] == -7 and row["v_is_reflective"],
           f"z={row['z_value_if_rational']} D={row['D']} form={row['T_X_reduced_form_abc']}")
    row, _ = CM.point_record(n, (14, -14, 5), rel, r)
    record("R3 Stream 1 order-3 vector (14,-14,5): z = infinity, T_X = (1,1,1), D = -3, "
           "not reflective",
           row["z_value_if_rational"] == "infinity" and row["T_X_reduced_form_abc"] == [1, 1, 1]
           and row["D"] == -3 and not row["v_is_reflective"],
           f"z={row['z_value_if_rational']} form={row['T_X_reduced_form_abc']}")

    lm = CM.EXTERNAL_CITATIONS["leanmaster"]
    good_c = CM.verify_citation(lm)
    bad_c = CM.verify_citation(lm, commit="ede49f0")
    if good_c["status"] == "REPO_UNAVAILABLE":
        record("R5 LeanMaster citation control", True,
               "SKIPPED -- sibling repo not checked out here; S10 exercises the same code")
    else:
        record(f"R5 LeanMaster citation at {lm['commit']} is VERIFIED",
               good_c["status"] == "VERIFIED", str(good_c["paths"]))
        record("R5 the previously cited commit ede49f0 is reported PHANTOM (real known-bad)",
               bad_c["status"] == "PHANTOM"
               and all(not v.startswith("present_contains") for v in bad_c["paths"].values()),
               f"clauses {bad_c['paths']}")

    print("\nS -- synthetic tamper (each must REFUSE on the named clause)")
    v = (2, -4, 1)
    good = CM.integer_kernel(CM.pair_row(7, v))
    record("S0 untampered kernel accepted", CM.transcendental_lattice(7, v, good)["D"] == -7)
    bad = [tuple(good[0]), (good[1][0], good[1][1], good[1][2] + 1)]
    c = refusal_clause(lambda: CM.transcendental_lattice(7, v, bad))
    record("S1 tampered kernel vector refused", c == "kernel_not_orthogonal", f"clause {c}")
    for vv in ((1, 1, 0), (1, 1, 3), (1, 0, 0)):
        c = refusal_clause(lambda: CM.transcendental_lattice(7, vv))
        c2 = refusal_clause(lambda: CM.tau_exact(7, vv))
        record(f"S2 v = {vv}, v^2 = {CM.norm(7, vv)} >= 0 refused",
               c == c2 == "no_upper_half_plane_root", f"clauses {c}, {c2}")
    bad = [tuple(good[0]), tuple(2 * k for k in good[1])]
    c = refusal_clause(lambda: CM.transcendental_lattice(7, v, bad))
    record("S3 index-2 (non-primitive) kernel refused", c == "kernel_not_saturated", f"clause {c}")
    c = refusal_clause(lambda: CM.transcendental_lattice(7, (2, -2, 0)))
    record("S4 non-primitive v = (2,-2,0) refused", c == "v_not_primitive", f"clause {c}")
    bad = [tuple(good[0]), tuple(-k for k in good[0])]
    c = refusal_clause(lambda: CM.transcendental_lattice(7, v, bad))
    record("S5 dependent kernel basis refused", c == "kernel_wrong_rank", f"clause {c}")

    for key in ctx:
        n, rel, r, loci = ctx[key]
        rel_bad = dict(rel)
        rel_bad["beta"] = rel["beta"] + 1
        rec = z_at(rel_bad, r, lambda: CM.tau_num(n, (1, -1, 0)))
        zval = rec["z"] if rec else None
        record(f"S6 {key}: relation with beta+1 sends the Fricke point off the C1 loci",
               zval not in loci + ["infinity"], f"clause locus_match; z = {zval}")

    n, rel, r, _ = ctx["cooper_s7"]
    for v in ((1, -1, 0), (2, -4, 1), (14, -14, 5), (1, -7, 0)):
        lo = z_at(rel, r, lambda: CM.tau_num(n, v), 60, 90)
        hi = z_at(rel, r, lambda: CM.tau_num(n, v))
        record(f"S7 s7 v={v}: recognition at 60/90 digits agrees with {CM.DPS_FIT}/{CM.DPS_VERIFY}",
               lo is not None and lo == hi, f"degree {lo and lo['degree']}, z = {lo and (lo['z'] or lo['coeffs'])}")
    eps = mp.mpf(10) ** -50
    plain = z_at(rel, r, lambda: CM.tau_num(n, (1, -7, 0)), 60, 90)
    pert = z_at(rel, r, lambda: CM.tau_num(n, (1, -7, 0)), 60, 90, perturb=eps)
    record("S7 a relative 1e-50 perturbation of the 90-digit copy is REJECTED by the re-check "
           "(the 60-digit fit alone accepts)", plain is not None and pert is None,
           f"clause recheck_at_higher_precision; unperturbed degree {plain and plain['degree']}, "
           f"perturbed -> {pert}")
    c = refusal_clause(lambda: CM.recognize_algebraic(mp.mpf(1), mp.mpf(1), 90, 60))
    record("S7 verify precision <= fit precision refused", c == "precision_control", f"clause {c}")

    # S8 -- the family-level gates can fire
    n, rel, r, _ = ctx["cooper_s7"]
    vs = CM.enumerate_vectors(n, 20)
    groups = CM.group_by_z(n, rel, r, vs)
    fv, ndv = CM.same_z_checks(n, groups)
    record("S8 untampered groups: no same-z violation (non-vacuity)", fv == [] and ndv == [],
           f"{len(groups)} groups from {len(vs)} vectors")
    key_form = lambda g: tuple(abs(c) for c in CM.transcendental_lattice(n, g[0])["reduced_form"])
    key_nd = lambda g: (-CM.norm(n, g[0]), CM.transcendental_lattice(n, g[0])["div_v"])
    pair_f = next(((g, h) for g in groups for h in groups if key_form(g) != key_form(h)), None)
    pair_n = next(((g, h) for g in groups for h in groups
                   if key_nd(g) != key_nd(h) and key_form(g) == key_form(h)), None)
    fv, _ = CM.same_z_checks(n, [pair_f[0] + pair_f[1]])
    record("S8 two groups with different T_X merged -> violation list non-empty",
           len(fv) == 1, f"clause same_z_different_form; forms {fv and fv[0]['forms_up_to_sign_b']}")
    if pair_n is None:     # no two groups share a form with different (norm, div): use any pair
        pair_n = next(((g, h) for g in groups for h in groups if key_nd(g) != key_nd(h)), None)
    _, ndv = CM.same_z_checks(n, [pair_n[0] + pair_n[1]])
    record("S8 two groups with different (-v^2, div) merged -> violation list non-empty",
           len(ndv) == 1,
           f"clause same_z_different_norm_or_div; {ndv and ndv[0]['minus_v2_and_div']}")
    rel_a = dict(rel)
    rel_a["alpha"] = rel["alpha"] + 1
    fa = CM.fricke_consistency(n, rel_a, r, vs)
    record("S8 relation with alpha+1 -> gate fricke_consistency fires", len(fa) > 0,
           f"clause fricke_consistency; {len(fa)}/{len(vs)} vectors violate")
    rel_b = dict(rel)
    rel_b["beta"] = rel["beta"] + 1
    fb = CM.fricke_consistency(n, rel_b, r, vs)
    record("S8 (scope) relation with beta+1 does NOT fire fricke_consistency -- a constant shift "
           "of 1/z is Fricke-invariant; that tamper is caught by S6 instead", len(fb) == 0,
           f"{len(fb)} violations")

    # S9 -- the conjugates diagnostic can drop
    rows = fams20["cooper_s7"]["rows"]
    diag = CM.conjugates_diagnostic(rows)
    pick = next((i for i, (R, c) in enumerate(zip(rows, diag))
                 if c and R["z_degree"] >= 2 and "j" not in R["z_numeric"]
                 and c == f"{R['z_degree']}/{R['z_degree']}"), None)
    if pick is None:
        record("S9 a real-z row of degree >= 2 with all roots present exists", False)
    else:
        alone = CM.conjugates_diagnostic([rows[pick]])[0]
        record(f"S9 v={tuple(rows[pick]['v'])}: {diag[pick]} roots in the table, but with every "
               "other row deleted the count drops", int(alone.split("/")[0]) < rows[pick]["z_degree"],
               f"clause conjugates_in_table; alone -> {alone}")

    # S10 -- verify_citation on this repo
    def cit(path, needle):
        return CM.verify_citation({"repo_dir_name": CM.REPO.name, "commit": "HEAD",
                                   "paths": {path: needle}}, home=CM.REPO.parent)
    c1 = cit("checkers/__no_such_file__.py", "x")
    c2 = cit("CLAUDE.md", "__no_such_name_in_this_file__")
    c3 = cit("CLAUDE.md", "Standing rules")
    record("S10 citation of a path absent at the commit -> PHANTOM",
           c1["status"] == "PHANTOM" and list(c1["paths"].values()) == ["absent_at_commit"],
           f"clause {list(c1['paths'].values())}")
    record("S10 citation of a name absent from an existing file -> PHANTOM",
           c2["status"] == "PHANTOM" and "not_found" in list(c2["paths"].values())[0],
           f"clause {list(c2['paths'].values())}")
    record("S10 citation of an existing file and name -> VERIFIED (non-vacuity)",
           c3["status"] == "VERIFIED", str(c3["paths"]))

    bad_n = [nm for nm, ok, _ in results if not ok]
    print("-" * 78)
    print(f"{len(results) - len(bad_n)}/{len(results)} controls behaved as required")
    for nm in bad_n:
        print(f"  FAILED: {nm}")
    return 1 if bad_n else 0


def test_cm_points_controls():
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())
