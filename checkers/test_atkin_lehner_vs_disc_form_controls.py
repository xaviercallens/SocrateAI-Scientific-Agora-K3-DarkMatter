#!/usr/bin/env python3
"""
test_atkin_lehner_vs_disc_form_controls.py -- negative controls for
check_atkin_lehner_vs_disc_form.py.  Standing rule 1: a test that cannot fail is not a test.
House style of test_CM_points_rho20_controls.py: R = REAL known-bads / real hypotheses on
untampered data, S = synthetic tamper.  Every refusal control checks WHICH clause fired.

  R1  REAL known-bad, not Atkin-Lehner: tau -> (tau+1)/5 (det 5, the same map as control N3 of
      check_s10_hauptmodul_gamma010star.py) at n = 10 and n = 7  -> `phi_not_integral`;
      al_type() does not recognise it.
  R2  REAL known-bad, wrong level: the level-10 matrices w_2, w_5 (H10.al_matrix) and the
      level-10 Fricke matrix against T_7                      -> `phi_not_integral`;
      and conversely the level-7 Fricke matrix against T_10   -> `phi_not_integral`.
      Monodromy twin: cooper_s7's monodromy run with n = 10   -> `monodromy_lattice_det_not_2n`.
  R3  REAL non-reflective vectors from the CM table: (14,-14,-5) in T_7 (v^2 = -42, div 14) and
      (4,-4,-1) in T_10 (v^2 = -12, div 4)                    -> `reflection_not_integral`.
  R4  REAL: the hyperbolic representative H10.al_matrix(2, 10) has no fixed point in H
                                                              -> `no_fixed_point_in_H`.
  R5  the sign of the rule is detected: the sign-swapped rule (+1 on the Q-part, -1 on the rest)
      disagrees with the phi-multiplier at EVERY n > 1 and Q; it equals the REFLECTION multiplier
      wherever a reflection exists (so the two lifts differ by exactly the global sign).
  R6  the reflection lift is NOT a homomorphism into O(q_A): at every n in the sweep where three
      reflections r(Q1), r(Q2), r(Q1 Q2) exist, m_r(Q1) m_r(Q2) != m_r(Q1 Q2); the count of such
      n must be > 0 (non-vacuity), and the products must agree modulo +-1.
  R7  REAL hypothesis with two outcomes: "the family's monodromy acts on A through {+-1}" --
      TRUE for cooper_s7, FALSE for cooper_s10 (advisory).  The monodromy leg therefore
      discriminates between the two families on untampered data.
  R8  Q | n but not Q || n: al_rep(2, 12) -> `Q_not_exact_divisor`; al_type([[2,1],[12,7]], 12) is None.
  R9  injectivity modulo +-1 is REFUTED, not assumed: kernel {1, n} at every n > 1 of the sweep,
      while into O(q_A) the map is bijective.
  S1  phi with one entry changed                              -> `phi_not_isometry`
  S2  monodromy generator with one entry changed              -> `monodromy_invariant_form_not_unique`
  S3  leg-F rows with the reflection multiplier changed       -> `monodromy_reflection_disagrees_with_fixed_point`
  S4  O(q_A) with 4n replaced by 2n: disagrees with the brute-force derivation at some n, and
      then W(n) -> O no longer onto.
  S5  P2 cross-check: t moved by 1e-40 -> False; (v2) changed -> False; untouched -> True.
  S6  WORKING PRECISION (a defect found while writing the checker): at 15 working digits (forced
      here with mp.workdps(15)) the same 1e-40 perturbation is ACCEPTED; family() therefore runs
      every comparison at DPS_HI + 30 digits.  Honest scope (review 2026-09-21): in the real
      process the ambient mp.dps after the imports is NOT 15, and without the wrapper the
      t-consistency gate goes False (fails safe) rather than passing vacuously.  What S6 guards
      is the wrapper itself, through comparison_working_dps and the restored ambient precision.
  S7  multiplier(): a rational isometry that is not integral (phi of R1) is refused upstream;
      a matrix that does not preserve T_n^* modulo T_n       -> `dual_generator_leaves_coset`.
Clauses with no control, stated: `phi_det_not_plus_one`, `multiplier_depends_on_representative`,
`multiplier_not_in_O_qA`, `phi_not_antimultiplicative`, `not_a_homomorphism`,
`product_not_AL_of_expected_type` are consequences of stage 0 for every Atkin-Lehner shape and
stand as assertions over the sweep; `rule_mismatch` is exercised through R5.

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: self (each control names its clause)
Reviewed-by: N
"""
import copy
import sys
from fractions import Fraction as F
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_atkin_lehner_vs_disc_form as AL  # noqa: E402

H10, CM = AL.H10, AL.CM
RESULTS = []


def record(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"  {'ok  ' if ok else 'FAIL'}  {name}  {detail}", flush=True)


def clause_of(fn):
    try:
        fn()
    except AL.Refused as e:
        return e.clause
    return None


def expect(name, fn, clause):
    got = clause_of(fn)
    ok = got == clause if isinstance(clause, str) else (got is not None and clause(got))
    record(name, ok, f"[clause fired: {got}]")


def main():
    NON_AL = ((1, 1), (0, 5))
    print("R controls")
    for n in (10, 7):
        expect(f"R1 (tau+1)/5 against T_{n}", lambda n=n: AL.integral_isometry(AL.phi(NON_AL, n), n, "phi"),
               "phi_not_integral")
    record("R1 al_type does not recognise (tau+1)/5", AL.al_type(NON_AL, 10) is None)
    for Q in (2, 5):
        g = H10.al_matrix(Q, 10)
        record(f"R2 non-vacuity: w_{Q} of level 10 IS an integral isometry of T_10",
               clause_of(lambda g=g: AL.integral_isometry(AL.phi(g, 10), 10, "phi")) is None)
        expect(f"R2 w_{Q} of level 10 against T_7", lambda g=g: AL.integral_isometry(AL.phi(g, 7), 7, "phi"),
               "phi_not_integral")
    expect("R2 Fricke of level 10 against T_7",
           lambda: AL.integral_isometry(AL.phi(((0, -1), (10, 0)), 7), 7, "phi"), "phi_not_integral")
    expect("R2 Fricke of level 7 against T_10",
           lambda: AL.integral_isometry(AL.phi(((0, -1), (7, 0)), 10), 10, "phi"), "phi_not_integral")
    expect("R2 monodromy of cooper_s7 paired with n = 10", lambda: AL.monodromy_leg("cooper_s7", 10),
           "monodromy_lattice_det_not_2n")
    for n, v in ((7, (14, -14, -5)), (10, (4, -4, -1))):
        expect(f"R3 reflection in the non-reflective {v} of T_{n}",
               lambda n=n, v=v: AL.integral_isometry(AL.reflection(n, v), n, "reflection"),
               "reflection_not_integral")
    expect("R4 hyperbolic representative of w_2, level 10",
           lambda: AL.fixed_vector(H10.al_matrix(2, 10), 10), "no_fixed_point_in_H")

    sweeps = [AL.sweep_one(n) for n in range(1, AL.N_SWEEP + 1)]
    swapped_hits = [(s["n"], Q) for s in sweeps for Q in s["exact_divisors"]
                    if s["n"] > 1 and AL.expected_rule(Q, s["n"], sign_swapped=True) == s["map_Q_to_m"][str(Q)]]
    record("R5 sign-swapped rule never matches the phi multiplier for n > 1", not swapped_hits,
           f"[matches: {swapped_hits}]")
    refl = [(s["n"], r["Q"], r["multiplier_reflection"]) for s in sweeps for r in s["rows"]
            if "multiplier_reflection" in r]
    record("R5 sign-swapped rule equals the REFLECTION multiplier wherever one exists",
           len(refl) > 0 and all(AL.expected_rule(Q, n, sign_swapped=True) == m for n, Q, m in refl),
           f"[{len(refl)} reflections]")
    tested = sum(s["reflection_lift_pairs_tested"] for s in sweeps)
    failing = sum(s["reflection_lift_pairs_failing_in_O_qA"] for s in sweeps)
    record("R6 reflection lift is not a homomorphism into O(q_A) (non-vacuous)",
           tested > 0 and failing == tested, f"[{failing}/{tested} pairs fail]")
    record("R9 kernel modulo +-1 is {1, n} for every n > 1; bijective into O(q_A)",
           all(s["kernel_modulo_pm1"] == [1, s["n"]] and not s["injective_modulo_pm1"]
               and s["image_equals_O_qA_as_sets"] and s["injective_into_O_qA"] for s in sweeps if s["n"] > 1))
    expect("R8 al_rep(2, 12): 2 is not an exact divisor of 12", lambda: AL.al_rep(2, 12), "Q_not_exact_divisor")
    record("R8 al_type([[2,1],[12,7]], 12) is None", AL.al_type(((2, 1), (12, 7)), 12) is None)

    fam7, fam10 = AL.family("cooper_s7"), AL.family("cooper_s10")
    m7, m10 = AL.monodromy_leg("cooper_s7", fam7["n"]), AL.monodromy_leg("cooper_s10", fam10["n"])
    record("R7 'monodromy acts on A through +-1': TRUE for cooper_s7", m7["acts_trivially_on_A_modulo_pm1"])
    record("R7 same hypothesis: FALSE for cooper_s10 (ADVISORY, LATTICE_CERT_DRAFT)",
           not m10["acts_trivially_on_A_modulo_pm1"], f"[multipliers {m10['multipliers_seen']}]")

    print("S controls")
    M = AL.phi(H10.al_matrix(5, 10), 10)
    M[0][0] += 1
    expect("S1 phi with one entry changed", lambda: AL.integral_isometry(M, 10, "phi"), "phi_not_isometry")
    expect("S2 monodromy generator with one entry changed",
           lambda: AL.monodromy_leg("cooper_s10", 10, tamper="entry"), "monodromy_invariant_form_not_unique")
    bad = copy.deepcopy(fam10)
    for rw in bad["fixed_points"]:
        if rw["z_locus"] == "-1/4":
            rw["multiplier_reflection"] = 1
    record("S3 non-vacuity: untampered comparison passes",
           clause_of(lambda: AL.compare_monodromy_with_fixed_points(fam10, m10)) is None)
    expect("S3 leg-F reflection multiplier changed",
           lambda: AL.compare_monodromy_with_fixed_points(bad, m10),
           "monodromy_reflection_disagrees_with_fixed_point")
    wrong = [n for n in range(1, AL.N_SWEEP + 1) if AL.O_qA_bruteforce(n) != AL.O_qA(n, mod_factor=2)]
    record("S4 'm^2 = 1 mod 2n' disagrees with the brute-force O(q_A) at some n", len(wrong) > 0,
           f"[n = {wrong}]")
    n0 = wrong[0] if wrong else 2
    record("S4 ... and W(n) -> that set is no longer onto",
           sorted(AL.sweep_one(n0)["map_Q_to_m"].values()) != AL.O_qA(n0, mod_factor=2), f"[n = {n0}]")

    row = next(rw for rw in fam10["fixed_points"] if rw["v"] == [1, -1, 0])
    with mp.workdps(AL.DPS_HI + 30):
        t_true = mp.mpf(1) / 4
        eps = mp.mpf(10) ** -40
        record("S5 P2 cross-check accepts the untouched row", AL.p2_crosscheck("cooper_s10", row, t_true) is True)
        record("S5 t moved by 1e-40 is rejected", AL.p2_crosscheck("cooper_s10", row, t_true + eps) is False)
        row2 = dict(row, v2=-4)
        record("S5 v^2 changed is rejected", AL.p2_crosscheck("cooper_s10", row2, t_true) is False)
    with mp.workdps(15):
        record("S6 at 15 working digits the 1e-40 perturbation is (wrongly) ACCEPTED -- "
               "which is why family() raises the working precision",
               AL.p2_crosscheck("cooper_s10", row, mp.mpf(1) / 4 + mp.mpf(10) ** -40) is True)
    record("S6 family() reports a comparison precision >= DPS_HI + 30, and mp.dps is restored after",
           fam10["comparison_working_dps"] >= AL.DPS_HI + 30 and fam7["comparison_working_dps"] >= AL.DPS_HI + 30
           and mp.mp.dps < AL.DPS_HI, f"[{fam10['comparison_working_dps']} digits]")
    expect("S7 a rational matrix that moves w/2n out of T* modulo T",
           lambda: AL.multiplier([[F(1), F(0), F(1, 3)], [F(0), F(1), F(0)], [F(0), F(0), F(1)]], 10),
           "dual_generator_leaves_coset")

    bad_ = [nm for nm, ok in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(bad_)}/{len(RESULTS)} controls behaved as required")
    if bad_:
        print("FAILED:", bad_)
    return 0 if not bad_ else 1


if __name__ == "__main__":
    sys.exit(main())
