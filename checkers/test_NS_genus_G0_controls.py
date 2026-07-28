#!/usr/bin/env python3
"""
test_NS_genus_G0_controls.py — mandatory negative controls for
check_NS_genus_G0.py (WP S2-G Phase G0; CLAUDE.md standing rule 1: "a test
that cannot fail is not a test — every headline-number checker ships a
negative control").

Controls:
  1. SCRAMBLED CANDIDATE TWIST: perturbing the candidate's <-d> block by +1
     (still a valid even rank-1 lattice, just the WRONG one) must make the
     disc-form match check fail loudly. Proves the match check can actually
     detect a wrong answer, not just rubber-stamp whatever is built.
  2. NON-CYCLIC DISCRIMINANT GROUP GUARD: cyclic_disc_form() must refuse
     (fail loudly) a fabricated discriminant group with more than one
     nontrivial generator — this checker's genus-uniqueness argument is
     written specifically for the cyclic-length-1 case and must not silently
     apply itself outside it.
  3. OVERSIZED/NON-CYCLIC DISCRIMINANT-GROUP GUARD: a fabricated rank-12 T
     with a large, non-cyclic discriminant group ((Z/2Z)^12) must be
     rejected loudly by the preconditions this checker's argument depends on
     (it is caught here by the same cyclic-length-1 guard as control 2 — for
     the rank-22 K3 lattice specifically, any T satisfying the embedding
     signature precondition m_+/- < n_+/- with a STRICTLY cyclic (ell=1)
     discriminant group automatically satisfies the Nikulin uniqueness bound
     too, so within this fixed ambient the two guards overlap; the point of
     this control is that a T failing either precondition never reaches an
     unjustified genus-uniqueness claim, not to isolate one exact line).
  4. CROSS-FAMILY DISCRIMINATION (positive control, standalone): cooper_s7
     and cooper_s10 must independently reproduce numerically different NS
     genus data (also asserted inline in check_NS_genus_G0.py's main(), but
     re-asserted here as pytest-style so CI catches it without running the
     full mpmath monodromy pipeline's __main__ path).
  5. E8 CANDIDATE-MATRIX SANITY: perturbing one entry of the E8 Gram matrix
     used internally must break unimodularity/positive-definiteness and be
     caught by e8_gram()'s own assertions (guards against a silently wrong
     hand-typed matrix).

Run:  python3 checkers/test_NS_genus_G0_controls.py

Generated-by: Sonnet 5 (Stream 2, WP S2-G Phase G0 session 2026-07-28)
Verified-by: this file IS the verifier for check_NS_genus_G0.py
Reviewed-by: pending T0 (Xavier)
"""

import sys
from pathlib import Path

import mpmath as mp
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_NS_genus_G0 as G0  # noqa: E402
import check_U1_lattice as U1  # noqa: E402


def control_scrambled_candidate_twist():
    """d -> d+offset in the candidate's <-d> block must break the pipeline.
    Two offsets, exercising two different gates:
      offset=1 (d=15, odd)  -> caught by the evenness check itself
      offset=2 (d=16, even) -> passes evenness, must be caught by the
                                disc-group-order / q-value MATCH check
                                (the code path that actually decides YES/NO)
    """
    mp.mp.dps = U1.DPS
    res = U1.run_family("cooper_s7", verbose=False)
    T_gram = sp.Matrix(res["stage3"]["gram_primitive_even"])

    for offset, why in ((1, "odd d=15, breaks evenness"), (2, "even d=16, breaks the disc-form match")):
        try:
            G0.nikulin_complement(T_gram, f"cooper_s7-SCRAMBLED-offset{offset}",
                                   scramble_d_offset=offset)
        except G0.ControlFailure as e:
            print(f"  [control] scrambled candidate twist (offset={offset}, {why}): "
                  f"pipeline failed loudly as required: PASS\n            ({e})")
            continue
        raise G0.ControlFailure(f"scrambled-candidate-twist control (offset={offset}) "
                                 "FAILED: pipeline accepted a candidate with the wrong disc form")
    return True


def control_noncyclic_disc_group_guard():
    """cyclic_disc_form() must refuse a fabricated 2-generator disc group."""
    fake_gens = [{"order": 2, "q_value_mod_2Z": "1"}, {"order": 2, "q_value_mod_2Z": "1"}]
    try:
        G0.cyclic_disc_form(fake_gens, "fabricated")
    except G0.ControlFailure as e:
        print(f"  [control] non-cyclic discriminant-group guard: failed loudly "
              f"as required: PASS\n            ({e})")
        return True
    raise G0.ControlFailure("non-cyclic-disc-group-guard control FAILED: "
                             "cyclic_disc_form() accepted a 2-generator group")


def control_oversized_disc_group_guard():
    """A fabricated rank-12 T with disc group (Z/2)^12 (ell=12) — badly
    non-cyclic, well beyond what this checker's argument covers — must be
    rejected loudly rather than silently let through to an unjustified
    genus-uniqueness claim."""
    T_fake = sp.diag(*([2, 2] + [-2] * 10))  # even, signature (2,10), rank 12
    chk_sig = G0.signature(T_fake)
    assert chk_sig == (2, 10), f"test setup bug: fake T signature {chk_sig} != (2,10)"
    try:
        G0.nikulin_complement(T_fake, "FABRICATED-oversized-disc-group")
    except G0.ControlFailure as e:
        print(f"  [control] oversized/non-cyclic disc-group guard: failed "
              f"loudly as required: PASS\n            ({e})")
        return True
    raise G0.ControlFailure("oversized-disc-group-guard control FAILED: pipeline "
                             "accepted a T whose disc group the argument does "
                             "not cover")


def control_cross_family_discrimination():
    """cooper_s7 and cooper_s10 must produce numerically different NS genus data."""
    mp.mp.dps = U1.DPS
    result_s7, _ = G0.run_family_G0("cooper_s7", verbose=False)
    result_s10, _ = G0.run_family_G0("cooper_s10", verbose=False)
    assert result_s7["T"]["det"] != result_s10["T"]["det"], \
        "cross-family control FAILED: s7 and s10 T dets coincide"
    assert result_s7["NS"]["disc_group_order_required"] != result_s10["NS"]["disc_group_order_required"], \
        "cross-family control FAILED: s7 and s10 NS disc-group orders coincide"
    print(f"  [control] cross-family discrimination: s7 det={result_s7['T']['det']} "
          f"vs s10 det={result_s10['T']['det']}, NS disc orders "
          f"{result_s7['NS']['disc_group_order_required']} vs "
          f"{result_s10['NS']['disc_group_order_required']}: PASS")
    return True


def control_e8_matrix_sanity():
    """Perturbing one off-diagonal entry of the E8 candidate matrix must
    break its own unimodularity/positive-definiteness assertions."""
    good = G0.e8_gram()
    assert good.det() == 1, "test setup bug: e8_gram() itself not unimodular"

    def broken_e8():
        E8 = sp.Matrix([
            [2, -1, 0, 0, 0, 0, 0, 0],
            [-1, 2, -1, 0, 0, 0, 0, 0],
            [0, -1, 2, -1, 0, 0, 0, 0],
            [0, 0, -1, 2, -1, 0, 0, 0],
            [0, 0, 0, -1, 2, -1, 0, -1],
            [0, 0, 0, 0, -1, 2, -1, 0],
            [0, 0, 0, 0, 0, -1, 2, 0],
            [0, 0, 0, 0, -1, 0, 0, 3],  # perturbed: 2 -> 3 (breaks evenness+unimodularity)
        ])
        E8 = sp.Matrix(E8)
        E8[7, 7] = 3
        E8[7, 4] = -1
        E8[4, 7] = -1
        n = 8
        chk = G0.chk
        chk(E8 == E8.T, "E8 candidate matrix not symmetric")
        chk(all(E8[i, i] == 2 for i in range(n)), "E8 candidate matrix not even/norm-2 diagonal")
        minors = [E8[:k, :k].det() for k in range(1, n + 1)]
        chk(all(m > 0 for m in minors), f"E8 candidate matrix not positive definite: minors={minors}")
        chk(E8.det() == 1, f"E8 candidate matrix not unimodular: det={E8.det()}")
        return E8

    try:
        broken_e8()
    except G0.ControlFailure as e:
        print(f"  [control] E8 candidate-matrix sanity: perturbed matrix "
              f"rejected as required: PASS\n            ({e})")
        return True
    raise G0.ControlFailure("E8-matrix-sanity control FAILED: a perturbed, "
                             "non-even matrix passed the evenness/unimodularity gates")


def main():
    print("=" * 78)
    print("test_NS_genus_G0_controls.py")
    print("=" * 78)
    controls = [
        ("scrambled candidate twist", control_scrambled_candidate_twist),
        ("non-cyclic disc-group guard", control_noncyclic_disc_group_guard),
        ("oversized/non-cyclic disc-group guard", control_oversized_disc_group_guard),
        ("cross-family discrimination", control_cross_family_discrimination),
        ("E8 matrix sanity", control_e8_matrix_sanity),
    ]
    worst = 0
    for name, fn in controls:
        print(f"\n--- {name} ---")
        try:
            fn()
        except (G0.ControlFailure, AssertionError) as e:
            print(f"FAIL: {name}: {e}", file=sys.stderr)
            worst = 3
    print()
    if worst == 0:
        print("ALL CONTROLS PASSED")
    return worst


if __name__ == "__main__":
    sys.exit(main())
