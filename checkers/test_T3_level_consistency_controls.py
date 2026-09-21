#!/usr/bin/env python3
"""
test_T3_level_consistency_controls.py -- negative controls for check_T3_level_consistency.py.

Standing rule 1: a test that cannot fail is not a test.  The bar set by the immediately
preceding C1 work (commit 297425e) is a REAL known-bad, not only synthetic tampering, so
the controls here are in two groups:

  R-controls (REAL candidates, real data, no tampering)
    R1  The other four order-3 entries in refs -- apery_zeta3, domb,
        almkvist_zagier_second, avs_sporadic3_s18 -- are real candidates whose mirror maps
        are integral (all six PASS(60) in C1).  Each must FAIL leg M at level 7 and at
        level 10.  8 real fits; if leg M passed for an arbitrary order-3 mirror map it
        would be measuring nothing.
    R2  Real cross-family: cooper_s7's z at level 10, and cooper_s10's z at level 7, must
        both FAIL.  (These are the T1 checkers' own N1/N3 controls, re-run through leg M.)
    R3  Non-vacuity: the two real pairs must PASS, so R1/R2 are not failing for a dumb
        reason (e.g. the fitter is broken).

  S-controls (synthetic tampering of leg L; each must make the checker REFUSE)
    S1  The CONFLATION control.  Feed the Gauss discriminant lattice of Gamma_0(n)-forms,
        Gram(b^2 - 4nac) = [[0,0,-2n],[0,1,0],[-2n,0,0]], in place of U + <2n>.  Stream 1
        proved these are not isometric for any n >= 1 (no_isometry_G0N_TN, commit e801d6e);
        a checker that read n off it would report 2n^2 instead of n.  Must refuse.
    S2  Tampered witness P (one entry changed) -> P^T G P is no longer U + <d>.
    S3  Tampered Gram entry -> |det| no longer equals the splitting's d.
    S4  Witness with det(P) = 2 -> not a lattice isometry.
    S5  Odd d (U + <15>, so the +-summand is not <2n>) -> refuse.
    S6  Missing witness -> refuse (a certificate without a serialized P cannot be checked;
        this is why the 2026-07-27 serialization ruling exists).
    S7  A lattice at the wrong level: s10's Gram fed through the s7 row must make leg M
        test level 10, not 7 -- i.e. leg L really drives the level tested.

Generated-by: Claude (Opus 5), Stream 2 | Verified-by: python3 + pytest, this file
Reviewed-by: N
"""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_T3_level_consistency as T3  # noqa: E402

ORDER = 40
REAL_KNOWN_BADS = ["apery_zeta3", "domb", "almkvist_zagier_second", "avs_sporadic3_s18"]
results = []


def record(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"  {'ok  ' if ok else 'FAIL'}  {name}" + (f"  -- {detail}" if detail else ""))


def leg_M(key, level, z_override=None):
    try:
        return T3.modular_leg(key, level, ORDER, z_override=z_override)
    except T3.Refused as e:
        return {"uniformizes_at_level": False, "failing_clauses": [f"REFUSED: {e}"]}


def leg_M_passes(key, level):
    return leg_M(key, level)["uniformizes_at_level"]


def refuses(fn):
    try:
        fn()
    except T3.Refused as e:
        return True, str(e)[:70]
    return False, "no refusal"


def gram_with_d(d):
    """A certificate-shaped dict for U + <d> in the repo's primitive-even basis."""
    return {"derived": {
        "gram_primitive_even": [[0, 0, -1], [0, d, 0], [-1, 0, 0]],
        "u_splitting": {"basis_change_matrix": [[1, 0, 0], [0, 0, 1], [0, -1, 0]]}}}


def as_cert_file(tmp, obj):
    tmp.write_text(json.dumps(obj))
    return tmp


def main():
    tmpdir = Path(__file__).resolve().parent / "__pycache__"
    tmpdir.mkdir(exist_ok=True)
    tmp = tmpdir / "_t3_control_cert.json"

    print("=" * 78)
    print("T3 controls")
    print("=" * 78)
    print("\nR -- REAL known-bads (real refs candidates, untampered data)")
    for key in REAL_KNOWN_BADS:
        for level in (7, 10):
            m = leg_M(key, level)
            record(f"R1 {key} does NOT uniformize at level {level}",
                   not m["uniformizes_at_level"], "fails: " + ", ".join(m["failing_clauses"]))
    for key, level in (("cooper_s7", 10), ("cooper_s10", 7)):
        m = leg_M(key, level)
        record(f"R2 {key} z does NOT uniformize at level {level}",
               not m["uniformizes_at_level"], "fails: " + ", ".join(m["failing_clauses"]))
    record("R3 cooper_s7 DOES uniformize at level 7 (non-vacuity)",
           leg_M_passes("cooper_s7", 7))
    record("R3 cooper_s10 DOES uniformize at level 10 (non-vacuity)",
           leg_M_passes("cooper_s10", 10))
    # R4: the Mobius clause is load-bearing and has its own REAL known-bad.  The level-7
    # coordinate t is itself a Gamma_0(7) Hauptmodul (H7's N1 control).  Fed to leg M at
    # level 7 it must fail, and must fail ON THE MOBIUS CLAUSE -- not on deg-2 solvability.
    # Without this, leg M would only be shown to test deg-2 solvability at the level.
    t7 = T3.H10.eta_quotient_series(T3.LEVEL_COORD[7], ORDER)
    m = leg_M("(Gamma_0(7) Hauptmodul t7)", 7, z_override=t7)
    record("R4 a Gamma_0(7) Hauptmodul fails leg M at level 7",
           not m["uniformizes_at_level"], "fails: " + ", ".join(m["failing_clauses"]))
    record("R4 ... and it fails ON THE MOBIUS CLAUSE (deg-2 solvability alone would not "
           "have rejected it)",
           m["failing_clauses"] == ["mobius_fit_fails"],
           f"clauses {m.get('clauses')}")

    print("\nS -- synthetic tampering of leg L (each must REFUSE)")
    # S1a: the Gauss discriminant lattice b^2 - 4nac is ODD (a 1 on the diagonal), so leg L
    # refuses on parity -- the determinant never enters.  Recorded for what it is.
    for n in (7, 10):
        g0n = {"derived": {
            "gram_primitive_even": [[0, 0, -2 * n], [0, 1, 0], [-2 * n, 0, 0]],
            "u_splitting": {"basis_change_matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}}}
        ok, why = refuses(lambda: T3.lattice_leg(as_cert_file(tmp, g0n)))
        record(f"S1a Gauss discriminant lattice b^2-4*{n}ac refused ON PARITY "
               "(odd diagonal; the determinant path is NOT exercised here)", ok, why)
    # S1b: the determinant path, which is what no_isometry_G0N_TN is actually about.
    # An even lattice carrying the Gauss determinant -4n^2 splits as U + <4n^2>, so leg L
    # reads n' = 2n^2, not n -- and leg M then has no coordinate at that level.  This is
    # the machine-visible consequence of the two lattices not being isometric: substituting
    # one for the other moves the number T3 compares.
    for n in (7, 10):
        d = 4 * n * n
        got = T3.lattice_leg(as_cert_file(tmp, gram_with_d(d)))["n_lattice"]
        ok_n = got == 2 * n * n != n
        ok_m, why_m = refuses(lambda: T3.modular_leg("x", got, ORDER))
        record(f"S1b even lattice of Gauss determinant {-d} reads n = {2*n*n}, not {n}, "
               "and leg M has no coordinate there (Stream 1 no_isometry_G0N_TN, det leg)",
               ok_n and ok_m, f"n={got}; {why_m}")

    live = json.loads((T3.CERTS / "C2_cooper_s7_v5.json").read_text())

    bad = copy.deepcopy(live)
    bad["derived"]["u_splitting"]["basis_change_matrix"][0][1] += 1
    ok, why = refuses(lambda: T3.lattice_leg(as_cert_file(tmp, bad)))
    record("S2 tampered witness P refused", ok, why)

    bad = copy.deepcopy(live)
    bad["derived"]["gram_primitive_even"][1][1] = 16
    ok, why = refuses(lambda: T3.lattice_leg(as_cert_file(tmp, bad)))
    record("S3 tampered Gram entry refused", ok, why)

    bad = copy.deepcopy(live)
    bad["derived"]["u_splitting"]["basis_change_matrix"] = [[2, 0, 0], [0, 0, 1], [0, -1, 0]]
    ok, why = refuses(lambda: T3.lattice_leg(as_cert_file(tmp, bad)))
    record("S4 witness with det P = 2 refused", ok, why)

    ok, why = refuses(lambda: T3.lattice_leg(as_cert_file(tmp, gram_with_d(15))))
    record("S5 odd U-complement <15> refused", ok, why)

    bad = copy.deepcopy(live)
    del bad["derived"]["u_splitting"]["basis_change_matrix"]
    ok, why = refuses(lambda: T3.lattice_leg(as_cert_file(tmp, bad)))
    record("S6 missing serialized witness refused", ok, why)

    # S7: leg L drives the level tested -- a d = 20 lattice must send leg M to level 10.
    n20 = T3.lattice_leg(as_cert_file(tmp, gram_with_d(20)))["n_lattice"]
    n14 = T3.lattice_leg(as_cert_file(tmp, gram_with_d(14)))["n_lattice"]
    record("S7 leg L drives the level: <20> -> n 10, <14> -> n 7",
           n20 == 10 and n14 == 7, f"got {n20}, {n14}")

    # positive sanity on the real, untampered certificate
    record("S0 untampered C2_cooper_s7_v5.json gives n = 7",
           T3.lattice_leg(T3.CERTS / "C2_cooper_s7_v5.json")["n_lattice"] == 7)

    tmp.unlink(missing_ok=True)
    bad_n = [n for n, ok, _ in results if not ok]
    print("-" * 78)
    print(f"{len(results) - len(bad_n)}/{len(results)} controls behaved as required")
    if bad_n:
        for n in bad_n:
            print(f"  FAILED: {n}")
        return 1
    return 0


def test_t3_controls():
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())
