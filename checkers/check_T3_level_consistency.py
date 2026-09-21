#!/usr/bin/env python3
"""
check_T3_level_consistency.py -- gate T3 of
briefs/STREAM2_K3xT2_SELECTION_CRITERIA_PROPOSAL_2026_09_16.md, as a runnable test.

T3 asks: does the n read from the LATTICE leg equal the n read from the MODULAR leg?

  leg L (lattice).  From the candidate's C2 lattice certificate, RE-DERIVE (never read)
      the Gram determinant of `derived.gram_primitive_even`, check the diagonal is even,
      re-apply the serialized base-change witness P and check P^T G P = U + <d>, check
      d = |det| and d = 2n with n a positive integer.  n_L = d / 2.
      Signature (2,1) is re-checked by Stream 1's diagonalising basis (below).
  leg M (modular).  Recompute z(q), the inverse mirror map, from the refs RECURRENCE via
      check_C1_mirror_integrality (round trip enforced), and fit it against the
      eta-quotient Hauptmodul coordinate of level n_L: a Mobius (deg-1) fit must FAIL and
      a deg-2 fit must solve on low orders and VERIFY on held-out orders.
      The level tested is the one the LATTICE names -- that is what makes this a gate and
      not a lookup.  The T1 certificate's own verdict is read alongside, for corroboration
      only; the fit is redone here.

WHAT "TWO LINEAGES" DOES AND DOES NOT MEAN  (corrects the proposal's wording)
  The proposal says the two legs "name the same isogeny degree by independent
  computations".  Traced to source, that is too strong: both legs start from the SAME
  object -- leg L from the monodromy representation of L2/L3, leg M from the q-series of
  the same family's recurrence, and the operator and the recurrence are the same data.
  What is true, and what this checker certifies, is weaker and still worth having: the
  two legs reach n by DISJOINT COMPUTATIONAL ROUTES (integral monodromy arithmetic and a
  (T_cusp - 1)^2 divisibility, versus an exact q-series identity against an independently
  constructed eta quotient), and the level in leg M is a free INPUT that a wrong value of
  n_L would send to a failing fit.  Certificates must say "internal consistency between
  two disjoint computations on the same operator", never "independent measurements".

DISCRIMINATING POWER (standing rule 1, at the bar set by C1's A112019 control)
  The controls file ships REAL known-bads, not only tampering: the other four order-3
  entries in refs (apery_zeta3, domb, almkvist_zagier_second, avs_sporadic3_s18) are real
  candidates with real integral mirror maps, and each FAILS the deg-2 fit at level 7 and
  at level 10 -- so a passing leg M is candidate-specific, not a property of any order-3
  mirror map.  Real cross-family bads (s7's z at level 10, s10's z at level 7) fail too.
  Not established: a real candidate that has BOTH legs and disagrees.  Only s7 and s10
  have a lattice certificate at all, and both agree; the gate's power against a real
  disagreeing candidate is therefore UNTESTED, and the certificate says so.  Note also
  that the teeth are DIRECTIONAL: leg M is only ever run at n_L, so a wrong n_L is sent
  to a failing fit (controls R2, S7), but nothing here tests whether a correct lattice
  could be paired with a modular certification at some OTHER level.

IMPORTED FROM STREAM 1 (Tier A-external; no Lean build was run from this repo)
  SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal, commit e801d6e,
  Agora/Geometry/MnLattice.lean and Agora/Geometry/SymSquareForms.lean, 0 sorry:
    TN_det          : det(U + <2N>) = -2N
    TN_diagonalises : diagBasis^T (U+<2N>) diagBasis = diag(2, 2N, -2), det diagBasis = 2
                      (so the signature is (2,1) by Sylvester, their Tier L caveat)
    no_isometry_G0N_TN : the Gauss discriminant lattice of Gamma_0(N)-forms (b^2 - 4Nac,
                      Gram det -4N^2) is NOT isometric to U + <2N> (Gram det -2N), for
                      every N >= 1.  That conflation is control C3 below.
  DERIVED HERE, not by Stream 1: U+<14> and U+<20> are not isometric.  It is one line
  from TN_det plus the invariance of the Gram determinant under unimodular base change
  (-14 != -20), and it is what makes n_L an isometry invariant of the lattice leg.

SCOPE.  This does NOT adopt T3.  Adopting it as a gate is T0 decision 2 of the proposal's
sec 6, still open; K3_CRITERIA.md is untouched.  This is a proposal-stage consistency test
with its own certificate.  cooper_s10 carries two separate open items, reported as two
separate flags and never collapsed into one: its lattice certificate is DRAFT (T0, D6',
2026-09-16), and its modular group is Gamma_0(10)*, not Gamma_0(10)+, whose Atkin-Lehner
action on the discriminant form has only had COUNTS matched (spike_disc_form_vs_atkin_lehner.py,
4 = 4); that the actions agree is unshown and referred to Deep Think, unanswered.

Generated-by: Claude (Opus 5), Stream 2 | Verified-by: test_T3_level_consistency_controls.py
Reviewed-by: N
"""
import argparse
import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_C1_mirror_integrality as C1  # noqa: E402
import check_s7_hauptmodul_gamma07plus as H7  # noqa: E402
import check_s10_hauptmodul_gamma010star as H10  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
CERTS = REPO / "data" / "certificates"
OUT = CERTS / "T3_LEVEL_CONSISTENCY.json"

ORDER = 40
N_SOLVE_DEG2 = 12
N_SOLVE_MOB = 6

# Eta exponents of the level-n Hauptmodul coordinate, exactly as used by the two T1
# certificates.  Each is re-validated in-checker (leading power q^1 + Newman conditions);
# nothing here is trusted because it is written down.
LEVEL_COORD = {
    7: {1: -4, 7: 4},                    # HAUPTMODUL_S7_GAMMA07PLUS.json
    10: {1: -4, 2: 4, 5: -4, 10: 4},     # HAUPTMODUL_S10_GAMMA010STAR.json
}

CANDIDATES = {
    "cooper_s7": {
        "lattice_cert": "C2_cooper_s7_v5.json",
        "lattice_cert_status": "LIVE",
        "t1_cert": "HAUPTMODUL_S7_GAMMA07PLUS.json",
        "t1_verdict_expected": "GAMMA07PLUS_HAUPTMODUL",
        "group": "Gamma_0(7)+",
        # Atkin-Lehner action on the discriminant form: verified at lattice level, PASS(30)
        # over n (ATKIN_LEHNER_DISC_FORM.json, 2026-09-21). Prime level: normalizer = Fricke.
        "al_action": {"verified": True, "evidence": "ATKIN_LEHNER_DISC_FORM.json", "pass_order_n": 30},
    },
    "cooper_s10": {
        "lattice_cert": "C2_cooper_s10_v4_DRAFT.json",
        "lattice_cert_status": "DRAFT",
        "t1_cert": "HAUPTMODUL_S10_GAMMA010STAR.json",
        "t1_verdict_expected": "GAMMA010STAR_HAUPTMODUL",
        "group": "Gamma_0(10)*",
        # Was ATKIN_LEHNER_ACTION_UNVERIFIED (counts matched only, 4 = 4). RETIRED 2026-09-21:
        # W(n) -> O(q_A) is an explicit isomorphism, PASS(30) over n, built from the action on
        # periods rather than counted (ATKIN_LEHNER_DISC_FORM.json; T0 D8', AM-4). The one open
        # flag left on cooper_s10 is LATTICE_CERT_DRAFT, a PROCESS item -- the two are reported
        # separately and must never be merged into one flag.
        "al_action": {"verified": True, "evidence": "ATKIN_LEHNER_DISC_FORM.json", "pass_order_n": 30},
    },
}

# Stream 1 MnLattice.diagBasis, columns (e+f, w, e-f); det 2.
DIAG_BASIS = [[1, 0, 1], [1, 0, -1], [0, 1, 0]]


class Refused(Exception):
    """The checker refuses to emit a number rather than emit a wrong one."""


# --------------------------------------------------------------- linear algebra ----
def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def matmul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def transpose(A):
    return [list(r) for r in zip(*A)]


# ------------------------------------------------------------------- leg L ----
def lattice_leg(cert_path):
    """Re-derive n from a C2 lattice certificate.  Reads only the Gram matrix and the
    serialized witness P; every number used downstream is recomputed here."""
    cert = json.loads(Path(cert_path).read_text())
    d = cert.get("derived") or {}
    G = d.get("gram_primitive_even")
    if not (isinstance(G, list) and len(G) == 3 and all(len(r) == 3 for r in G)):
        raise Refused(f"{cert_path}: no 3x3 derived.gram_primitive_even")
    G = [[int(x) for x in row] for row in G]
    if transpose(G) != G:
        raise Refused("Gram matrix is not symmetric")
    for i in range(3):
        if G[i][i] % 2 != 0:
            raise Refused(f"Gram diagonal entry {i} = {G[i][i]} is odd: lattice is not even "
                          "(a Gauss discriminant lattice b^2-4Nac has a 1 on the diagonal; "
                          "Stream 1 no_isometry_G0N_TN -- it is not U+<2n>)")
    det = det3(G)
    if det == 0:
        raise Refused("degenerate Gram matrix")

    spl = d.get("u_splitting") or {}
    P = spl.get("basis_change_matrix")
    if not (isinstance(P, list) and len(P) == 3 and all(len(r) == 3 for r in P)):
        raise Refused("no serialized u_splitting.basis_change_matrix witness")
    P = [[int(x) for x in row] for row in P]
    if det3(P) not in (1, -1):
        raise Refused(f"witness P has det {det3(P)}, not +-1: not a lattice isometry")
    after = matmul(matmul(transpose(P), G), P)
    dd = after[2][2]
    target = [[0, 1, 0], [1, 0, 0], [0, 0, dd]]
    if after != target:
        raise Refused(f"P^T G P = {after}, not U + <{dd}>")
    if dd <= 0 or dd % 2 != 0:
        raise Refused(f"U-summand complement <{dd}>: not <2n> with n a positive integer")
    if abs(det) != dd:
        raise Refused(f"|det| = {abs(det)} but the splitting gives <{dd}>")
    # Stream 1 TN_diagonalises, re-run here: diag(2, 2n, -2) => signature (2,1).
    diag = matmul(matmul(transpose(DIAG_BASIS), target), DIAG_BASIS)
    if diag != [[2, 0, 0], [0, dd, 0], [0, 0, -2]]:
        raise Refused(f"diagBasis^T (U+<{dd}>) diagBasis = {diag}, not diag(2, {dd}, -2)")
    return {
        "gram": G,
        "det_recomputed": det,
        "u_splitting_d_recomputed": dd,
        "witness_det": det3(P),
        "sylvester_diagonal": [diag[0][0], diag[1][1], diag[2][2]],
        "signature": [2, 1],
        "n_lattice": dd // 2,
    }


# ------------------------------------------------------------------- leg M ----
def modular_leg(key, level, order=ORDER, z_override=None):
    """Does the candidate's z(q) uniformize at THIS level?  deg-2 fit must solve and
    verify on held-out orders; the Mobius fit must fail.

    `uniformizes_at_level` is a conjunction of four clauses, and which one fails is part
    of the result (`failing_clauses`).  Without that, a control showing only "False" would
    not distinguish "the deg-2 fit did not solve" from "the Mobius clause fired", and the
    Mobius clause -- the one that separates a Hauptmodul for Gamma_0(n)+/* from one for
    Gamma_0(n) -- would have no negative evidence behind it anywhere in T3.

    `z_override` lets a control feed an arbitrary q-series in place of a refs candidate's
    mirror map (used for the Gamma_0(n) Hauptmodul control, which is not a refs entry).
    """
    if level not in LEVEL_COORD:
        raise Refused(f"no eta-quotient coordinate on file for level {level}; leg M cannot "
                      "be run, and no verdict is emitted")
    r = LEVEL_COORD[level]
    if F(sum(d * e for d, e in r.items()), 24) != 1:
        raise Refused(f"level-{level} coordinate has leading power != q^1")
    newman = H10.newman_conditions(r, level)
    t = H10.eta_quotient_series(r, order)
    z = list(z_override) if z_override is not None else z_of(key, order)
    m_s, m_v, _ = H7.rational_fit(z, t, 1, N_SOLVE_MOB, order)
    d_s, d_v, sol = H7.rational_fit(z, t, 2, N_SOLVE_DEG2, order)
    clauses = {
        "newman_conditions_hold": bool(all(newman.values())),
        "deg2_fit_solves": bool(d_s),
        "deg2_fit_verifies_heldout": bool(d_v),
        "mobius_fit_fails": not bool(m_s and m_v),
    }
    return {
        "level_tested": level,
        "eta_exponents": {str(k): v for k, v in r.items()},
        "newman_conditions": newman,
        "mobius_fit_passes": bool(m_s and m_v),
        "deg2_fit_solves": bool(d_s),
        "deg2_fit_verifies_heldout": bool(d_v),
        "heldout_orders": [N_SOLVE_DEG2 + 1, order],
        "clauses": clauses,
        "failing_clauses": [k for k, v in clauses.items() if not v],
        "uniformizes_at_level": all(clauses.values()),
        "relation": ({k: str(v) for k, v in H10.relation_shape(sol).items()}
                     if sol and H10.relation_shape(sol) else None),
    }


_Z_CACHE = {}


def z_of(key, order):
    if (key, order) not in _Z_CACHE:
        seqs = json.loads(C1.REFS.read_text())["sequences"]
        if key not in seqs:
            raise Refused(f"{key} is not in the refs register")
        res = C1.check_entry(key, seqs[key], order)   # refuses on round-trip failure
        if res["verdict"] != f"PASS({order})":
            raise Refused(f"{key}: mirror map not integral to order {order} "
                          f"({res['verdict']}); leg M has no Hauptmodul candidate")
        _Z_CACHE[(key, order)] = C1.mirror_map(seqs[key]["recurrence_python"], order)[2]
    return _Z_CACHE[(key, order)]


# ------------------------------------------------------------------ verdicts ----
def evaluate(key, order=ORDER):
    spec = CANDIDATES[key]
    L = lattice_leg(CERTS / spec["lattice_cert"])
    n = L["n_lattice"]
    M = modular_leg(key, n, order)
    t1 = json.loads((CERTS / spec["t1_cert"]).read_text())
    t1_ok = t1.get("verdict") == spec["t1_verdict_expected"]

    flags = []
    if spec["lattice_cert_status"] != "LIVE":
        flags.append("LATTICE_CERT_DRAFT")
    if not spec["al_action"]["verified"]:
        flags.append("ATKIN_LEHNER_ACTION_UNVERIFIED")
    if not t1_ok:
        flags.append("T1_CERT_VERDICT_MISMATCH")

    agree = bool(M["uniformizes_at_level"])
    verdict = f"T3_AGREE(n={n})" if agree else "T3_DISAGREE"
    return {
        "candidate": key,
        "leg_L_lattice": L,
        "leg_M_modular": M,
        "t1_certificate": {"file": spec["t1_cert"], "verdict": t1.get("verdict"),
                           "group": spec["group"], "corroborates": t1_ok},
        "n_lattice": n,
        "n_modular": n if agree else None,
        "agree": agree,
        "verdict": verdict,
        "atkin_lehner_action": spec["al_action"],
        "open_flags": flags,
        "status": ("CONSISTENT" if agree and not flags
                   else "CONSISTENT_WITH_OPEN_ITEMS" if agree else "INCONSISTENT"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--order", type=int, default=ORDER)
    ap.add_argument("--only", action="append")
    ap.add_argument("--emit", action="store_true")
    args = ap.parse_args()
    keys = args.only or list(CANDIDATES)

    print("=" * 78)
    print("T3 -- two-leg agreement on n (lattice leg vs modular leg).  PROPOSAL STAGE:")
    print("adopting T3 as a gate is T0 decision 2; K3_CRITERIA.md is untouched.")
    print("=" * 78)
    results, ok = {}, True
    for key in keys:
        try:
            r = evaluate(key, args.order)
        except Refused as e:
            ok = False
            results[key] = {"candidate": key, "verdict": "REFUSED", "reason": str(e)}
            print(f"\n{key}: REFUSED -- {e}")
            continue
        results[key] = r
        L, M = r["leg_L_lattice"], r["leg_M_modular"]
        print(f"\n{key}")
        print(f"  leg L  Gram {L['gram']}  det (recomputed) {L['det_recomputed']}")
        print(f"         P^T G P = U + <{L['u_splitting_d_recomputed']}>, det P = {L['witness_det']}, "
              f"Sylvester diag {L['sylvester_diagonal']} -> signature {tuple(L['signature'])}")
        print(f"         n_lattice = {L['n_lattice']}")
        print(f"  leg M  level {M['level_tested']} coordinate eta^{M['eta_exponents']}")
        print(f"         Newman {M['newman_conditions']}")
        print(f"         Mobius fit (must FAIL): {'PASS' if M['mobius_fit_passes'] else 'FAIL'};  "
              f"deg-2 solve {M['deg2_fit_solves']}, held-out verify {M['deg2_fit_verifies_heldout']} "
              f"(orders {M['heldout_orders'][0]}..{M['heldout_orders'][1]})")
        if M["relation"]:
            print(f"         1/z = {M['relation']['alpha']}*t + {M['relation']['beta']} "
                  f"+ {M['relation']['gamma']}/t")
        print(f"  T1 cert {r['t1_certificate']['file']}: {r['t1_certificate']['verdict']} "
              f"({r['t1_certificate']['group']}), corroborates: {r['t1_certificate']['corroborates']}")
        print(f"  VERDICT: {r['verdict']}   status {r['status']}")
        for f_ in r["open_flags"]:
            print(f"     open: {f_}")
        ok = ok and r["agree"]

    cert = {
        "certificate": "T3_LEVEL_CONSISTENCY",
        "checker": Path(__file__).name,
        "checker_version": "1.0.0",
        "date": "2026-09-21",
        "status": "PROPOSAL STAGE -- T3 is not an adopted gate. Adoption is T0 decision 2 of "
                  "briefs/STREAM2_K3xT2_SELECTION_CRITERIA_PROPOSAL_2026_09_16.md sec 6, open. "
                  "K3_CRITERIA.md unchanged. No scoring.",
        "claim": "For each candidate below, the n re-derived from its C2 lattice certificate "
                 "(Gram determinant and the serialized U-splitting witness, both recomputed) "
                 "equals the level at which its inverse mirror map is verified to uniformize "
                 "by an exact q-series fit against the level-n eta-quotient coordinate.",
        "not_claimed": [
            "that the two legs are INDEPENDENT measurements -- they are two disjoint "
            "computational routes from the same operator/recurrence (see checker docstring)",
            "that T(cooper_s10) is certified: C2_cooper_s10_v4_DRAFT.json is DRAFT (T0 D6', "
            "2026-09-16), so the s10 row is advisory",
            "that the Atkin-Lehner action of Gamma_0(10)* agrees with the isometries of the "
            "discriminant form of U+<20>: only the COUNTS match (4 = 4, "
            "spike_disc_form_vs_atkin_lehner.py). Referred to Deep Think, unanswered",
            "that the family's moduli space IS X_0(n)* / X_0(n)+",
            "any physical reading: no vacuum selection, no flux, no dark-sector claim "
            "(VISION sec 1.3; Tier C blocked, F5b)",
        ],
        "discriminating_power": {
            "real_known_bads_that_fail_leg_M": "apery_zeta3, domb, almkvist_zagier_second, "
                "avs_sporadic3_s18 (all real refs order-3 entries with integral mirror maps) "
                "each fail the deg-2 fit at level 7 AND at level 10; cooper_s7 fails at level "
                "10 and cooper_s10 at level 7. See test_T3_level_consistency_controls.py.",
            "mobius_clause_control": "the Mobius clause (which separates a Hauptmodul for "
                "Gamma_0(n)+/* from one for Gamma_0(n)) has its own real known-bad: the "
                "level-7 coordinate fed to itself is a Gamma_0(7) Hauptmodul and fails leg M "
                "on exactly that clause, not on deg-2 solvability (control R4).",
            "untested": "no real candidate exists that has BOTH legs and disagrees -- only "
                        "cooper_s7 and cooper_s10 have a lattice certificate at all, and both "
                        "agree. The gate's power against a real disagreeing candidate is "
                        "UNESTABLISHED; synthetic tamper controls only for leg L. The teeth "
                        "are also DIRECTIONAL: leg M is only ever run at n_L, so nothing "
                        "tests a correct lattice paired with some other modular level.",
        },
        "imported_tier_A_external": {
            "repo": "SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal",
            "commit": "e801d6e",
            "files": ["Agora/Geometry/MnLattice.lean", "Agora/Geometry/SymSquareForms.lean"],
            "theorems_used": ["TN_det", "TN_diagonalises", "no_isometry_G0N_TN"],
            "caveat": "read as source text; no Lean build was run from this repo",
            "derived_here_not_by_stream_1": "U+<14> and U+<20> are not isometric (TN_det plus "
                                            "invariance of the Gram determinant; -14 != -20)",
        },
        "tier": "B",
        "results": results,
        "all_candidates_consistent": ok,
    }
    if args.emit:
        OUT.write_text(json.dumps(cert, indent=2) + "\n")
        print(f"\nwrote {OUT.relative_to(REPO)}")
    print("\n" + "=" * 78)
    print(f"OVERALL: {'all tested candidates consistent' if ok else 'NOT all consistent'}")
    print("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
