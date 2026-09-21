#!/usr/bin/env python3
"""
check_A2_membership.py -- does the rank-2 lattice A2 (Gram [[2,1],[1,2]], reduced form
(1,1,1), D = -3) occur as v^perp for a primitive v of negative norm in T_n = U + <2n>,
for the n of cooper_s7 (n = 7) and of cooper_s10 (n = 10)?  Lattice / modular
arithmetic.  Tier B at best.  No physical reading.  Builds on check_CM_points_rho20.py
(imported as CM; its lattice, tau, reduction and recognition code is reused, not copied).

THE QUESTION, AS LATTICE ARITHMETIC
  Within the cited framework (see TIERS), a member of the M_n-polarized family has
  transcendental lattice isometric to a rank-2 lattice K iff there is a primitive
  v in T_n with v^2 < 0 and v^perp isometric to K.  This checker computes the right-hand
  side only.  The target K = A2 is the lattice of LeanMaster's theorem
  `smallest_black_hole` (DualScaleDyons/AttractorCharges.lean; the theorem name is
  LeanMaster's, quoted as an identifier -- nothing of its Tier C reading is imported):
  its statement contains `reducedForms 3 = [(1, 1, 1)]`, re-verified at run time by
  CM.verify_citation and RE-COMPUTED here by reduced_forms(-3).

THREE LEGS
  (A) exact congruence, covering ALL primitive v (not a bounded search).
      Let G = Gram(T_n), det G = -2n, v primitive, d = div(v) = gcd of the entries of Gv,
      K = v^perp with Z-basis u1, u2 and c = u1 x u2 (the vector of 2x2 minors).
        (i)   det(U^T G U) = c^T adj(G) c                  [stage 0, sympy, generic U, G]
        (ii)  (Gv)^T adj(G) (Gv) = det(G) * v^T G v        [stage 0, sympy]
        (iii) c is primitive (K is saturated) and Euclidean-orthogonal to u1, u2; so is
              Gv/d (because u_i^T G v = 0); the Euclidean complement of a rank-2
              sublattice of Z^3 has rank 1, hence c = +-Gv/d.
      So det K = det(G) v^2 / d^2 = 2n * (-v^2) / d^2, i.e. D := -det K = 2n v^2 / d^2.
      Writing x = d x', y = d y' (d | x, d | y, and gcd(d, z) = 1 by primitivity, so
      d | 2n) and beta = 2n z / d:
        (iv)  D = beta^2 + 4n x' y'                        [stage 0, sympy]
      Hence for EVERY primitive v of negative norm, D is a square modulo 4n (the
      Heegner condition at level n).  Conversely if beta^2 = D mod 4n, put
      e = gcd(beta, 2n), d = 2n/e, z = beta/e, v = (d, d (D - beta^2)/(4n), z): it is
      primitive with div d and v^perp of discriminant D -- constructed and VERIFIED
      exactly by CM.transcendental_lattice for every (n, D, beta) in the table.
      The squares modulo 4n are computed by exhausting beta in range(4n).
      Step (iii) is a three-line argument in this docstring, not a machine proof; legs
      (B) and the per-vector assertion below are its computational cross-check.
  (B) exhaustive exact enumeration over a STATED box: all primitive v = (x, y, z),
      |x|, |y|, |z| <= BOX, one of +-v, v^2 < 0.  For each, v^perp is computed by
      CM.transcendental_lattice (which itself asserts det K * d^2 = -v^2 * 2n), and the
      congruence D = (2nz/d)^2 mod 4n is asserted per vector.
  (C) agreement, |D| <= D_MAX, all D = 0, 1 mod 4 (fundamental ones are flagged):
      {D found in the box} must equal {D square mod 4n}; both inclusions gate the exit
      code (clauses `enumeration_outside_criterion`, `criterion_not_reached_in_box`).
      The second inclusion is a bounded statement (it holds at BOX; a smaller box fails
      it -- control S3); the unbounded version of it is the witness construction of (A).

  The discriminant criterion decides D, not the form class.  For the target (1,1,1)
  that is enough: reduced_forms(-3) has one element.  For a general target the verdict
  PRESENT is only awarded on an explicit vector whose reduced form IS the target
  (control S5); the per-D form lists in the table are what the box and the witnesses
  contain and are NOT claimed complete.

IF PRESENT: tau (exact), and z = 1/w at tau through CM.point_record (Tier B numeric
  recognition, LLL at CM.DPS_FIT digits re-checked at CM.DPS_VERIFY digits).  Every z
  statement rests on TWO things and both are recorded in the point record: (a) the
  relation 1/z = alpha t + beta + gamma/t, which T3.modular_leg certifies to q-order
  CM.ORDER only -- PASS(ORDER), a finite order, not a proof; (b) the numeric evaluation
  of the eta quotient t at tau.  For a
  point with w = 0 (z = infinity) the recognition is "|w| below 10^-(dps-20) at both
  precisions", plus the exact statement that alpha t^2 + beta t + gamma is proportional
  to the recognised minimal polynomial of t.  The Gamma_0(n)-stabilizer of tau is found
  by exact integer search and its order compared with the exponent denominators at the
  matching point of data/certificates/L3_RIEMANN_SCHEME.json.

BRIEF
  --brief renders briefs/STREAM2_A2_MEMBERSHIP_2026_09_21.md from the certificate file
  (render_brief); the brief's numbers are read from the JSON, none is typed.  --emit
  --brief does both in order.

TIERS
  finite order, PASS(ORDER): the relation 1/z = alpha t + beta + gamma/t (T3.modular_leg).
  exact: legs (A)(i),(ii),(iv), the residues, every witness, leg (B), leg (C), tau, the
      stabilizer.  framework, cited not proved (Tier B): as in check_CM_points_rho20.py
      (Dolgachev 1996 sec 7, read and hash-pinned; Lefschetz (1,1), standard, not among
      the pinned statements) -- the link from "v.omega = 0" to "rho = 20, T_X = v^perp".
  numeric recognition (Tier B): every value of t, w, z.
  cooper_s10: the lattice certificate is DRAFT by T0 ruling; every s10 statement is
      advisory and is arithmetic of U + <20> as that draft records it.

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: test_A2_membership_controls.py
Reviewed-by: N
"""
import argparse
import json
import sys
import time
from fractions import Fraction as F
from math import gcd
from pathlib import Path

import mpmath as mp
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_CM_points_rho20 as CM  # noqa: E402

T3 = CM.T3
REPO = CM.REPO
CERTS = CM.CERTS
OUT = CERTS / "A2_MEMBERSHIP.json"
BRIEF = REPO / "briefs" / "STREAM2_A2_MEMBERSHIP_2026_09_21.md"
Refused = CM.Refused
log = CM.log

TARGET_FORM = (1, 1, 1)     # the QUESTION's input (A2); cross-checked against reduced_forms(-3)
BOX = 80                    # leg (B): |x|, |y|, |z| <= BOX
D_MAX = 100                 # leg (C): -D_MAX <= D < 0
WINDOW_BOUND = 42           # CM.enumerate_vectors window used for the "all A2 points share one z" check
STAB_BOUND = 30             # |entries| of the stabilizer search
RIEMANN_CERT = "L3_RIEMANN_SCHEME.json"
P2_CERT = "CM_POINTS_RHO20.json"

EXTERNAL_CITATIONS = {
    "leanmaster_target": {
        "repo_dir_name": "SocrateAI-Scientific-Agora-LeanMaster", "commit": "4109a51",
        "paths": {"DualScaleDyons/AttractorCharges.lean": "reducedForms 3 = [(1, 1, 1)]",
                  "docs/STREAM8_WHICH_K3.md": "the same computation in two languages"}},
    "stream1_G0N": {
        "repo_dir_name": "SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal",
        "commit": "3a96018",
        "paths": {"Agora/Geometry/SymSquareForms.lean": "no_isometry_G0N_TN",
                  "Agora/Geometry/ModularAction.lean": "g3_fixes"}},
    # the docstring of g3_fixes already identifies (14,-14,5) with an order-3 elliptic point:
    "stream1_elliptic_point_already_on_record": {
        "repo_dir_name": "SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal",
        "commit": "3a96018",
        "paths": {"Agora/Geometry/ModularAction.lean": "is the order-3 elliptic point of"}},
}

NOT_CLAIMED = [
    "that this certificate scores, ranks or prefers a candidate or a member of a family: the rho = 20 "
    "cut was ADOPTED by T0 on 2026-09-21 (D7', briefs/T0_DECISIONS_2026_09_21_STREAM2.md) and is "
    "read narrowly - the adoption carries no ranking of s7 over s10 and no minimum-|D| rule, so "
    "'A2 is in the s7 family and not in the s10 family' stays a lattice fact, not a preference",
    "that agreement between the binary-form route and the modular route corroborates anything: "
    "LeanMaster docs/STREAM8_WHICH_K3.md sec G10 (read as source) states that the binary-form "
    "enumeration and the modular side are the same computation in two languages (Shioda-Inose), "
    "so their agreement is forced, not corroboration. The Heegner congruence and the lattice "
    "enumeration of this checker agree for the same reason",
    "that the step from 'v in T_n, v.omega = 0' to 'a member of the family has rho = 20 and "
    "T_X = v^perp' is proved here: it is the cited framework (Dolgachev 1996 sec 7, read and "
    "pinned; Lefschetz (1,1), standard, not among the pinned statements). Tier B. The checker "
    "computes the lattice side only",
    "that the explicit Almkvist-van Straten geometric family has a smooth fibre at the point "
    "found: for n = 7 the A2 point is z = infinity, which is a regular singular point of L3 "
    "(exponent denominators 3 in L3_RIEMANN_SCHEME.json) and an order-3 elliptic point of "
    "Gamma_0(7) (one of two, tau = (+-5 + i sqrt 3)/14, which the Fricke involution swaps, so "
    "THE order-3 point of X_0(7)+). What is established is a point of the period domain, not a fibre of a "
    "specific projective model",
    "that z = infinity IS the value at the A2 point: the statement rests on (a) the relation "
    "1/z = alpha t + beta + gamma/t, certified by T3.modular_leg to a finite q-order only "
    "(PASS(N), N = relation_order_checked in the point record), and (b) |1/z| below "
    "10^-(dps-20) at two precisions (Tier B numeric recognition), supported by an exact "
    "proportionality that itself rests on a numerically recognised minimal polynomial of t",
    "that the singular-point reading of the hand estimate was unanticipated program-wide: the "
    "docstring of Stream 1's g3_fixes (ModularAction.lean, read as source) already says that "
    "(14,-14,5) corresponds to the order-3 elliptic point of X_0(7)",
    "that the per-discriminant form lists are complete: they record what the stated box and the "
    "constructed witnesses contain. Only the discriminant criterion covers all v",
    "anything certified about T(cooper_s10): C2_cooper_s10_v4_DRAFT.json is DRAFT by T0 ruling; "
    "the s10 negative is arithmetic of U + <20> as that draft records it, and is advisory",
    "any Kodaira fibre type at any locus (CLAUDE.md ledger item 3); elliptic points are treated "
    "only as elliptic points of the modular curve",
    "any physical reading whatsoever (VISION sec 1.3; Tier C blocked, F5b). The LeanMaster theorem "
    "name is quoted as an identifier only",
]


# ------------------------------------------------------------------ stage 0 ----
def stage0_symbolic():
    """Leg (A) identities (i), (ii), (iv), symbolically.  All must hold."""
    g = sp.symbols("g0:6")
    G = sp.Matrix([[g[0], g[1], g[2]], [g[1], g[3], g[4]], [g[2], g[4], g[5]]])
    a = sp.symbols("a0:3")
    b = sp.symbols("b0:3")
    U = sp.Matrix([list(a), list(b)]).T
    c = sp.Matrix([a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]])
    out = {"i_det_UtGU_equals_ct_adjG_c":
           sp.expand((U.T * G * U).det() - (c.T * G.adjugate() * c)[0]) == 0}
    v = sp.Matrix(sp.symbols("v0:3"))
    out["ii_Gv_adjG_Gv_equals_detG_vGv"] = sp.expand(
        ((G * v).T * G.adjugate() * (G * v))[0] - G.det() * (v.T * G * v)[0]) == 0
    n, d, xp, yp, z = sp.symbols("n d xp yp z")
    Gn = sp.Matrix(CM.gram_T(n))
    out["detTn_is_minus_2n"] = sp.expand(Gn.det() + 2 * n) == 0
    vv = sp.Matrix([d * xp, d * yp, z])
    D = sp.simplify(-(Gn.det() * (vv.T * Gn * vv)[0]) / d ** 2)     # D = -det K
    out["iv_D_equals_beta2_plus_4n_xp_yp"] = sp.simplify(
        D - ((2 * n * z / d) ** 2 + 4 * n * xp * yp)) == 0
    if not all(out.values()):
        raise Refused("stage0_symbolic", str(out))
    return {k: bool(val) for k, val in out.items()}


# ------------------------------------------------------------ exact arithmetic ----
def squares_mod(M):
    return sorted({(b * b) % M for b in range(M)})


def default_modulus(n):
    return 4 * n


def criterion(n, D, modulus=default_modulus):
    """Leg (A): D is the discriminant of v^perp for SOME primitive v in U+<2n>, v^2 < 0,
    iff D < 0 and D is a square modulo 4n."""
    M = modulus(n)
    return D < 0 and (D % M) in set(squares_mod(M))


def is_fundamental(D):
    def squarefree(m):
        m = abs(m)
        p = 2
        while p * p <= m:
            if m % (p * p) == 0:
                return False
            p += 1
        return True
    if D % 4 == 1:
        return squarefree(D)
    if D % 4 == 0:
        q = D // 4
        return q % 4 in (2, 3) and squarefree(q)
    return False


def reduced_forms(D):
    """All reduced positive definite (a, b, c), b^2 - 4ac = D, primitive or not
    (-a < b <= a <= c, b >= 0 if a == c)."""
    if D >= 0 or D % 4 not in (0, 1):
        return []
    out = []
    a = 1
    while 3 * a * a <= -D:
        for b in range(-a + 1, a + 1):
            if (b * b - D) % (4 * a):
                continue
            c = (b * b - D) // (4 * a)
            if c < a or (a == c and b < 0):
                continue
            out.append((a, b, c))
        a += 1
    return out


def lattice_class(form):
    """Isometry class of the rank-2 lattice = GL_2(Z) class of the form: (a, |b|, c)."""
    a, b, c = form
    return (a, abs(b), c)


def check_vector_congruence(n, v, TX):
    """Per-vector assertion of leg (A): D = (2nz/d)^2 mod 4n, and d | 2n, d | x, d | y."""
    d = TX["div_v"]
    if (2 * n) % d or v[0] % d or v[1] % d or gcd(d, v[2]) != 1:
        raise Refused("divisibility_structure", f"v = {v}, d = {d}, n = {n}")
    beta = 2 * n * v[2] // d
    if (TX["D"] - beta * beta) % (4 * n):
        raise Refused("congruence_violated",
                      f"v = {v}: D = {TX['D']} != ({beta})^2 mod {4 * n}")
    return beta % (2 * n)


def construct_witnesses(n, D, tamper=None):
    """Leg (A) converse: one verified vector per beta in range(2n) with beta^2 = D mod 4n."""
    out = []
    for beta in range(2 * n):
        if (beta * beta - D) % (4 * n):
            continue
        e = gcd(beta, 2 * n)            # gcd(0, 2n) = 2n
        d = 2 * n // e
        v = (d, d * ((D - beta * beta) // (4 * n)), beta // e)
        if tamper:
            v = tamper(v)
        try:
            TX = CM.transcendental_lattice(n, v)
        except Refused as ex:
            raise Refused("witness_fails", f"n = {n}, D = {D}, beta = {beta}, v = {v}: {ex}")
        if TX["D"] != D or TX["div_v"] != d:
            raise Refused("witness_fails", f"n = {n}, beta = {beta}, v = {v}: D = {TX['D']}, "
                                           f"div = {TX['div_v']}, wanted D = {D}, div = {d}")
        check_vector_congruence(n, v, TX)
        out.append({"beta_mod_2n": beta, "v": list(v), "minus_v2": -CM.norm(n, v), "div_v": d,
                    "reduced_form": TX["reduced_form"]})
    return out


def box_enumeration(n, box=BOX, d_max=D_MAX, check_n=None):
    """Leg (B).  Every primitive v (one of +-v), |coords| <= box, v^2 < 0.
    Violations of the det identity (CM.verify_TX) or of the per-vector congruence are
    COUNTED by clause, not raised; main() gates the exit code on the counts.  `check_n`
    (controls only) asserts the congruence at another level."""
    by_D, count, betas = {}, 0, {}
    violations, examples, det_ok = {}, [], 0
    check_n = n if check_n is None else check_n
    for x in range(0, box + 1):
        for y in range(-box, box + 1):
            if x * y >= 0 and x != 0:
                continue                      # 2xy + 2n z^2 < 0 needs xy < 0
            if x == 0:
                continue                      # x = 0: v^2 = 2n z^2 >= 0
            for z in range(-box, box + 1):
                if 2 * x * y + 2 * n * z * z >= 0 or gcd(gcd(x, y), z) != 1:
                    continue
                v = (x, y, z)
                count += 1
                try:
                    TX = CM.transcendental_lattice(n, v)     # asserts det K d^2 = -v^2 2n
                    det_ok += 1
                    beta = check_vector_congruence(check_n, v, TX)
                except Refused as ex:
                    violations[ex.clause] = violations.get(ex.clause, 0) + 1
                    if len(examples) < 5:
                        examples.append({"v": list(v), "clause": ex.clause})
                    continue
                if TX["D"] >= -d_max:
                    rec = by_D.setdefault(TX["D"], {"forms": {}, "norm_div": set()})
                    cls = lattice_class(TX["reduced_form"])
                    if cls not in rec["forms"] or _size(v) < _size(rec["forms"][cls]):
                        rec["forms"][cls] = v
                    rec["norm_div"].add((-CM.norm(n, v), TX["div_v"]))
                    betas.setdefault(TX["D"], set()).add(min(beta, 2 * n - beta))
    return {"box": box, "vectors_checked": count, "by_D": by_D, "betas": betas,
            "det_identity_held_on": det_ok, "violations": violations,
            "violation_examples": examples}


def _size(v):
    return (max(abs(c) for c in v), v)


def discriminant_table(n, enum, d_max=D_MAX, modulus=default_modulus):
    """Leg (C).  Refuses, naming the clause, on either kind of disagreement."""
    rows, outside, unreached = [], [], []
    for D in range(-1, -d_max - 1, -1):
        if D % 4 not in (0, 1):
            continue
        crit = criterion(n, D, modulus)
        found = D in enum["by_D"]
        if found and not crit:
            outside.append(D)
        if crit and not found:
            unreached.append(D)
        wit = construct_witnesses(n, D) if crit else []
        classes = sorted({lattice_class(f) for f in reduced_forms(D)})
        seen = set(enum["by_D"][D]["forms"]) if found else set()
        seen |= {lattice_class(w["reduced_form"]) for w in wit}
        rows.append({"D": D, "fundamental": is_fundamental(D), "square_mod_4n": crit,
                     "found_in_box": found,
                     "witnesses": wit,
                     "lattice_classes_of_this_D": [list(c) for c in classes],
                     "lattice_classes_seen": [list(c) for c in sorted(seen)],
                     "minus_v2_and_div_seen_in_box":
                         sorted(list(t) for t in enum["by_D"][D]["norm_div"]) if found else []})
    if outside:
        raise Refused("enumeration_outside_criterion",
                      f"n = {n}: D in {outside} found in the box but not a square mod "
                      f"{modulus(n)} -- a bug or a finding")
    if unreached:
        raise Refused("criterion_not_reached_in_box",
                      f"n = {n}: D in {unreached} square mod {modulus(n)} but no vector in the "
                      f"box |coords| <= {enum['box']}")
    return rows


# -------------------------------------------------------------------- lattice ----
def family_level(key, lattice_cert=None):
    """n, re-derived from the family's C2 certificate (never typed).  If another lattice
    certificate is supplied it must be U + <2n> for the SAME n, or the run refuses."""
    spec = T3.CANDIDATES[key]
    try:
        n_reg = T3.lattice_leg(CERTS / spec["lattice_cert"])["n_lattice"]
    except T3.Refused as ex:
        raise Refused("lattice_leg_refused", str(ex))
    if lattice_cert is not None:
        G = (json.loads(Path(lattice_cert).read_text()).get("derived") or {}).get(
            "gram_primitive_even")
        if G and any(int(G[i][i]) % 2 for i in range(3)):
            raise Refused("lattice_not_even",
                          f"diagonal {[G[i][i] for i in range(3)]}: not an even lattice, so not "
                          "U+<2n> (the Gauss discriminant lattice b^2-4Nac has a 1 on the "
                          "diagonal; Stream 1 no_isometry_G0N_TN)")
        try:
            L = T3.lattice_leg(lattice_cert)
        except T3.Refused as ex:
            raise Refused("lattice_leg_refused", str(ex))
        if L["n_lattice"] != n_reg:
            raise Refused("lattice_level_mismatch",
                          f"supplied lattice is U+<{2 * L['n_lattice']}>, the family's certificate "
                          f"gives U+<{2 * n_reg}> (|det| {2 * L['n_lattice']} vs {2 * n_reg})")
    flags = [] if spec["lattice_cert_status"] == "LIVE" else ["LATTICE_CERT_DRAFT"]
    return n_reg, flags


def level_relation(key, n):
    """The lattice n must be the level at which the family's z uniformizes: the relation
    1/z = alpha t + beta + gamma/t, PASS(CM.ORDER).  Run for EVERY family (present or not),
    so a lattice certificate of the wrong level cannot reach a verdict."""
    try:
        rel, r = CM.relation_for(key, n)
    except T3.Refused as ex:
        raise Refused("no_level_coordinate", str(ex))
    return rel, r


def relation_record(rel):
    return {"relation_1_over_z": {k: str(val) for k, val in rel.items()},
            "relation_form": "1/z = alpha*t + beta + gamma/t, t the eta quotient of T3.LEVEL_COORD",
            "relation_order_checked": CM.ORDER,
            "relation_verdict": f"PASS({CM.ORDER})"}


# ----------------------------------------------------------------- membership ----
def membership(n, target, enum):
    """Verdict for one (n, target form).  `fired` names the clause that decided it."""
    a, b, c = target
    if tuple(CM.gauss_reduce(a, b, c)) != tuple(target):
        raise Refused("target_not_reduced", str(target))
    D = b * b - 4 * a * c
    cls = lattice_class(target)
    crit = criterion(n, D)
    in_box = D in enum["by_D"]
    if not crit:
        if in_box:
            raise Refused("enumeration_outside_criterion", f"n = {n}, D = {D}")
        return {"verdict": "ABSENT", "fired": "D_not_square_mod_4n", "D": D,
                "scope": "ALL primitive v of negative norm (exact congruence, leg A)",
                "D_mod_4n": D % (4 * n), "squares_mod_4n": squares_mod(4 * n),
                "box_cross_check": f"no vector with D = {D} among {enum['vectors_checked']} "
                                   f"in the box |coords| <= {enum['box']}"}
    wit = construct_witnesses(n, D)
    cands = [tuple(w["v"]) for w in wit if lattice_class(w["reduced_form"]) == cls]
    if in_box and cls in enum["by_D"][D]["forms"]:
        cands.append(enum["by_D"][D]["forms"][cls])
    if not cands:
        return {"verdict": "D_OCCURS_FORM_NOT_FOUND", "fired": "form_class_not_matched", "D": D,
                "scope": f"bounded: witnesses + box |coords| <= {enum['box']}",
                "lattice_classes_seen": sorted(
                    {lattice_class(w["reduced_form"]) for w in wit}
                    | (set(enum["by_D"][D]["forms"]) if in_box else set()))}
    v = min(cands, key=_size)
    TX = CM.transcendental_lattice(n, v)
    if lattice_class(TX["reduced_form"]) != cls:
        raise Refused("witness_fails", f"{v}: {TX['reduced_form']}")
    all_nd = sorted(enum["by_D"][D]["norm_div"]) if in_box else []
    return {"verdict": "PRESENT", "fired": "explicit_vector_with_target_form", "D": D,
            "scope": "existence (one explicit exact vector suffices)",
            "v": list(v), "minus_v2": -CM.norm(n, v), "div_v": TX["div_v"],
            "kernel_basis": TX["kernel_basis"], "gram": TX["gram"],
            "reduced_form": TX["reduced_form"],
            "witnesses_by_beta": wit,
            "minus_v2_and_div_of_every_such_vector_in_box": [list(t) for t in all_nd],
            "forced_minus_v2_and_div_exact": forced_norm_div(n, D)}


def forced_norm_div(n, D):
    """All (m, d) with d | 2n, m = -D d^2 / (2n) a positive even integer (m = -v^2 is even
    in an even lattice).  Exact; necessary conditions only."""
    out = []
    for d in range(1, 2 * n + 1):
        if (2 * n) % d == 0 and (-D * d * d) % (2 * n) == 0:
            m = -D * d * d // (2 * n)
            if m % 2 == 0:
                out.append([m, d])
    return out


# ------------------------------------------------------------ the point itself ----
def stabilizer(n, v, bound=STAB_BOUND):
    """Non-scalar elements [[a,b],[c,d]] of Gamma_0(n) (det 1, n | c) fixing tau_v, by exact
    integer search: c tau^2 + (d-a) tau - b = 0 must be proportional to the primitive integer
    quadratic of tau_v, n x tau^2 - 2 n z tau - y = 0."""
    x, y, z = v
    q = (n * x, -2 * n * z, -y)
    g = gcd(gcd(q[0], q[1]), q[2])
    A, B, C = (t // g for t in q)
    found = []
    for k in range(-bound, bound + 1):
        if k == 0 or (k * A) % n:
            continue
        for a in range(-bound, bound + 1):
            c, dd, b = k * A, a + k * B, -k * C
            if a * dd - b * c == 1 and max(abs(b), abs(c), abs(dd)) <= bound:
                found.append({"matrix": [[a, b], [c, dd]], "trace": a + dd})
    orders = {0: 2, 1: 3, -1: 3}
    order = max([orders.get(m["trace"], 0) for m in found], default=1)
    return {"tau_quadratic_primitive": [A, B, C], "elements": found[:6],
            "order_in_PSL2": order, "search_bound": bound}


def assert_w_zero(n, v, rel, r, mags=None):
    """The two gates behind 'z = infinity': |1/z| < 10^-(dps-20) at both precisions, and
    alpha t^2 + beta t + gamma proportional to the recognised minimal polynomial of t.
    Refuses with `w_not_zero` / `t_not_recognised` (control S7)."""
    if mags is None:
        mags = {}
        for dps in (CM.DPS_FIT, CM.DPS_VERIFY):
            mp.mp.dps = dps
            mags[dps] = CM.w_of_tau(rel, r, CM.tau_num(n, tuple(v)))[1]
    for dps, w in mags.items():
        mp.mp.dps = dps
        if not abs(w) < mp.mpf(10) ** (-(dps - 20)):
            raise Refused("w_not_zero", f"|w| = {mp.nstr(abs(w), 5)} at {dps} digits")
    mp.mp.dps = CM.DPS_FIT
    t_fit, _ = CM.w_of_tau(rel, r, CM.tau_num(n, tuple(v)))
    mp.mp.dps = CM.DPS_VERIFY
    t_ver, _ = CM.w_of_tau(rel, r, CM.tau_num(n, tuple(v)))
    rec_t = CM.recognize_algebraic(t_fit, t_ver, CM.DPS_FIT, CM.DPS_VERIFY, (1, 2))
    if rec_t is None or rec_t["degree"] != 2:
        raise Refused("t_not_recognised", str(rec_t))
    c0, c1, c2 = (F(k) for k in rec_t["coeffs"])
    if not (rel["alpha"] * c1 == rel["beta"] * c2 and rel["alpha"] * c0 == rel["gamma"] * c2):
        raise Refused("w_not_zero", "alpha t^2 + beta t + gamma is not proportional to the "
                                    f"recognised minimal polynomial {rec_t['coeffs']} of t")
    return {"t_minpoly_coeffs_ascending": rec_t["coeffs"],
            "alpha_t2_plus_beta_t_plus_gamma_proportional_to_it": True}


def point_data(key, n, v, rel=None, r=None):
    """tau exact, z numeric recognition, stabilizer, singular-point bookkeeping."""
    if rel is None:
        rel, r = CM.relation_for(key, n)
    rowd, _ = CM.point_record(n, tuple(v), rel, r)
    mags = {}
    for dps in (CM.DPS_FIT, CM.DPS_VERIFY):
        mp.mp.dps = dps
        _, w = CM.w_of_tau(rel, r, CM.tau_num(n, tuple(v)))
        mags[dps] = w
    at_infinity = rowd["z_numeric"] == "infinity"
    t_exact = assert_w_zero(n, v, rel, r, mags) if at_infinity else None
    mp.mp.dps = 15
    loci = json.loads((CERTS / CM.LOCI_CERT[key]).read_text())["finite_singular_loci"]
    scheme = next(R["riemann_scheme"] for R in
                  json.loads((CERTS / RIEMANN_CERT).read_text())["results"]
                  if R["operator"] == key)
    zname = "oo" if at_infinity else rowd["z_value_if_rational"]
    exps = scheme.get(zname) if zname else None
    stab = stabilizer(n, v)
    den = None
    if exps:
        den = 1
        for e in exps:
            den = den * F(e).denominator // gcd(den, F(e).denominator)
    return {
        **relation_record(rel),
        "v": list(v), "tau": rowd["tau"],
        "tau_readable": f"{rowd['tau']['re']} + i*sqrt({rowd['tau']['im_squared']})",
        "z": "infinity" if at_infinity else (rowd["z_value_if_rational"] or rowd["z_minpoly"]),
        "z_recognition": (f"given the relation (PASS({CM.ORDER})), Tier B numeric recognition "
                          "of 1/z = 0: |1/z| < 10^-(dps-20) at "
                          f"{CM.DPS_FIT} and at {CM.DPS_VERIFY} digits" if at_infinity
                          else rowd["recognition"]),
        "log10_abs_one_over_z": {str(dps): (float(mp.log10(abs(w))) if w != 0 else None)
                                 for dps, w in mags.items()},
        "t_numeric": rowd["t_numeric"], "t_minpoly": rowd["t_minpoly"], "t_exact_support": t_exact,
        "finite_singular_loci_from_C1_cert": loci,
        "is_a_finite_singular_locus": (not at_infinity) and rowd["z_value_if_rational"] in loci,
        "is_a_singular_point_of_L3_on_P1": exps is not None,
        "L3_exponents_there": exps, "L3_exponent_denominator_lcm": den,
        "gamma0_n_stabilizer": stab,
        "stabilizer_order_equals_exponent_denominator": (den == stab["order_in_PSL2"]
                                                         if den else None),
        "v_is_reflective": rowd["v_is_reflective"],
    }


def one_z_for_all(key, n, cls, rel, r):
    """Bounded: every vector of CM's logged window whose v^perp is in class `cls` has the same
    1/z (here compared at CM.CLUSTER_DPS digits)."""
    vs = [v for v in CM.enumerate_vectors(n, WINDOW_BOUND)
          if lattice_class(CM.transcendental_lattice(n, v)["reduced_form"]) == cls]
    mp.mp.dps = CM.CLUSTER_DPS
    ws = [CM.w_of_tau(rel, r, CM.tau_num(n, v))[1] for v in vs]
    tol = mp.mpf(10) ** -CM.CLUSTER_TOL_EXP
    same = all(abs(w - ws[0]) <= tol * (1 + abs(ws[0])) for w in ws)
    mp.mp.dps = 15
    return {"window": f"CM.enumerate_vectors(n, {WINDOW_BOUND}), Im tau >= {CM.Y_MIN}",
            "vectors": [list(v) for v in vs], "count": len(vs), "all_same_one_over_z": same}


def elliptic_pair(n, v, rel, r):
    """'An' order-3 point of Gamma_0(n) versus 'the' order-3 point of X_0(n)+.
    exact: the Fricke image v' of v, its v'^perp class, tau * tau' = -1/n is CM's stage 0;
    exact count: #{x mod n : x^2 + x + 1 = 0}, which for 9 not dividing n is the standard
      formula for the number of order-3 elliptic points of Gamma_0(n) (cited as standard,
      e.g. Diamond-Shurman Cor. 3.7.2; not among the pinned sources, not proved here);
    numeric (Tier B): t differs at tau and tau' (t is injective on X_0(n) only for the genus-0
      levels where it is a Hauptmodul -- T3's PASS(ORDER) statement), while 1/z agrees."""
    vp = CM.fricke_image(tuple(v))
    TXp = CM.transcendental_lattice(n, vp)
    mp.mp.dps = CM.CLUSTER_DPS
    t1, w1 = CM.w_of_tau(rel, r, CM.tau_num(n, tuple(v)))
    t2, w2 = CM.w_of_tau(rel, r, CM.tau_num(n, vp))
    tol = mp.mpf(10) ** -CM.CLUSTER_TOL_EXP
    out = {"fricke_image_of_v": list(vp),
           "fricke_image_vperp_reduced_form": TXp["reduced_form"],
           "count_x_mod_n_with_x2_plus_x_plus_1_zero": sum(1 for x in range(n)
                                                          if (x * x + x + 1) % n == 0),
           "count_is_the_standard_nu3_formula": n % 9 != 0,
           "t_differs_at_the_two_points_numeric": bool(abs(t1 - t2) > tol * (1 + abs(t1))),
           "one_over_z_agrees_at_the_two_points_numeric": bool(abs(w1 - w2) <= tol * (1 + abs(w1)))}
    mp.mp.dps = 15
    return out


# ------------------------------------------------------------------ prediction ----
def evaluate_prediction(res):
    """The orchestrator's hand estimate (UNVERIFIED when issued), scored clause by clause."""
    s7, s10 = res["cooper_s7"], res["cooper_s10"]
    m7, m10 = s7["membership_A2"], s10["membership_A2"]
    n7, n10 = s7["n"], s10["n"]
    hand_v = (14, -14, 5)
    try:
        hv = CM.transcendental_lattice(n7, hand_v)
        hand_ok = tuple(hv["reduced_form"]) == TARGET_FORM and hv["div_v"] == 14 \
            and -CM.norm(n7, hand_v) == 42
    except Refused:
        hand_ok = False
    pt = s7.get("point")
    clauses = {
        "det(v^perp) = |v^2| * 2n / d^2 (asserted on every box vector and witness; leg A i-iii)":
            all(R["box"]["det_identity_held_on"] == R["box"][
                "primitive_negative_norm_vectors_checked"] > 0 for R in (s7, s10)),
        "n = 7: D = -3 forces d = 14, -v^2 = 42":
            m7.get("forced_minus_v2_and_div_exact") == [[42, 14]]
            and m7.get("minus_v2_and_div_of_every_such_vector_in_box") == [[42, 14]],
        "the example v = (14,-14,5) has v^perp = A2": hand_ok,
        "A2 occurs for n = 7": m7["verdict"] == "PRESENT",
        "n = 10: z^2 = -3 mod 40 has no solution": (-3) % (4 * n10) not in squares_mod(4 * n10),
        "A2 does not occur for n = 10": m10["verdict"] == "ABSENT",
        "Heegner form of the criterion: -3 is a square mod 4n for n = 7 and not for n = 10":
            criterion(n7, -3) and not criterion(n10, -3),
        "the n = 7 A2 point is not one of the FINITE singular loci of the C1 certificate":
            bool(pt) and not pt["is_a_finite_singular_locus"],
        "the n = 7 A2 point is not a singular point of L3 at all":
            bool(pt) and not pt["is_a_singular_point_of_L3_on_P1"],
    }
    refuted = [c for c, ok in clauses.items() if not ok]
    return {"statement": ("orchestrator's hand estimate, issued UNVERIFIED; scored here. Its last "
                          "sentence ('it should not be one of the singular loci') is scored under "
                          "two readings: the finite loci of the C1 certificate, and the singular "
                          "points of L3 on P^1 including z = infinity"),
            "clauses": clauses, "refuted": refuted,
            "outcome": ("CONFIRMED on every clause" if not refuted else
                        f"CONFIRMED except {len(refuted)} clause(s): " + "; ".join(refuted))}


# ------------------------------------------------------------------------ run ----
def run_family(key, box=BOX):
    n, flags = family_level(key)
    rel, r = level_relation(key, n)
    enum = box_enumeration(n, box)
    mem = membership(n, TARGET_FORM, enum)
    table = discriminant_table(n, enum)
    out = {"candidate": key, "n": n, "flags": flags, "advisory": bool(flags),
           "lattice_cert": T3.CANDIDATES[key]["lattice_cert"],
           "box": {"abs_coords_max": box, "primitive_negative_norm_vectors_checked":
                   enum["vectors_checked"],
                   "det_identity_held_on": enum["det_identity_held_on"],
                   "violations_by_clause": enum["violations"],
                   "violation_examples": enum["violation_examples"]},
           "level_relation": relation_record(rel),
           "membership_A2": mem, "discriminant_table": table}
    if mem["verdict"] == "PRESENT":
        out["point"] = point_data(key, n, mem["v"], rel, r)
        out["elliptic_pair"] = elliptic_pair(n, mem["v"], rel, r)
        out["all_A2_vectors_in_window_share_one_z"] = one_z_for_all(
            key, n, lattice_class(TARGET_FORM), rel, r)
    return out


def p2_agreement(res):
    """The P2 certificate (if present) must not contradict this one at D = -3."""
    p = CERTS / P2_CERT
    if not p.exists():
        return {"status": "P2_CERT_ABSENT"}
    fams = json.loads(p.read_text())["families"]
    out = {}
    for key, fam in fams.items():
        rows = [R for R in fam["rows"] if tuple(R["T_X_reduced_form_abc"]) == TARGET_FORM]
        out[key] = {"A2_rows_in_P2_cert": [{"v": R["v"], "z": R["z_numeric"]} for R in rows],
                    "consistent": bool(rows) == (res[key]["membership_A2"]["verdict"] == "PRESENT")}
    out["status"] = "CONSISTENT" if all(o["consistent"] for o in out.values()) else "CONTRADICTION"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--brief", action="store_true",
                    help="render the brief from the certificate file (after --emit, if given)")
    args = ap.parse_args()
    t0 = time.time()
    log("=" * 78)
    log("A2 membership: is [[2,1],[1,2]] a v^perp in T_n = U+<2n>?  (lattice arithmetic, Tier B)")
    log("=" * 78)
    s0 = stage0_symbolic()
    log("stage 0 symbolic identities (leg A i, ii, iv):", "all hold" if all(s0.values()) else s0)
    rf = reduced_forms(-3)
    if rf != [TARGET_FORM]:
        raise Refused("target_cross_check", f"reduced_forms(-3) = {rf}")
    log(f"target: reduced_forms(-3) = {rf} (recomputed; LeanMaster states the same list)")

    res = {k: run_family(k) for k in ("cooper_s7", "cooper_s10")}
    for key, R in res.items():
        m = R["membership_A2"]
        log(f"\n[{key}] n = {R['n']}  flags: {R['flags'] or 'none'}"
            + ("  ** ADVISORY **" if R["advisory"] else ""))
        log(f"  box |coords| <= {BOX}: {R['box']['primitive_negative_norm_vectors_checked']} primitive "
            "negative-norm vectors, congruence D = (2nz/d)^2 mod 4n asserted on each; "
            f"violations by clause: {R['box']['violations_by_clause'] or 'none'}")
        log(f"  level relation: 1/z = {R['level_relation']['relation_1_over_z']} "
            f"({R['level_relation']['relation_verdict']}, finite order)")
        log(f"  A2: {m['verdict']}  [fired: {m['fired']}]  scope: {m['scope']}")
        if m["verdict"] == "PRESENT":
            P = R["point"]
            log(f"    v = {tuple(m['v'])}, -v^2 = {m['minus_v2']}, div = {m['div_v']}, "
                f"kernel {m['kernel_basis']}, Gram {m['gram']}")
            log(f"    tau = {P['tau_readable']};  z = {P['z']}  ({P['z_recognition']})")
            log(f"    log10|1/z| by precision: {P['log10_abs_one_over_z']};  t: {P['t_minpoly']}")
            log(f"    finite singular locus: {P['is_a_finite_singular_locus']};  singular point of "
                f"L3 on P^1: {P['is_a_singular_point_of_L3_on_P1']} (exponents "
                f"{P['L3_exponents_there']});  Gamma_0({R['n']}) stabilizer order "
                f"{P['gamma0_n_stabilizer']['order_in_PSL2']}")
            W = R["all_A2_vectors_in_window_share_one_z"]
            log(f"    {W['count']} A2 vectors in the P2 window, all the same 1/z: "
                f"{W['all_same_one_over_z']}")
        else:
            log(f"    D mod 4n = {m['D_mod_4n']}, squares mod 4n = {m['squares_mod_4n']}")
            log(f"    {m['box_cross_check']}")
        yes = [row["D"] for row in R["discriminant_table"] if row["square_mod_4n"]]
        log(f"  discriminants -{D_MAX} <= D < 0 admitted (criterion == box, both inclusions): {yes}")

    pred = evaluate_prediction(res)
    log("\nHAND ESTIMATE:", pred["outcome"])
    for c, ok in pred["clauses"].items():
        log(f"  {'confirmed' if ok else 'REFUTED  '}  {c}")
    p2 = p2_agreement(res)
    log("P2 certificate at D = -3:", p2["status"])
    citations = {k: CM.verify_citation(c) for k, c in EXTERNAL_CITATIONS.items()}
    for k, c in citations.items():
        log(f"citation {k} @ {c['commit']}: {c['status']} {c['paths']}")
    citations_ok = all(c["status"] != "PHANTOM" for c in citations.values())

    both = sorted(set(r["D"] for r in res["cooper_s7"]["discriminant_table"] if r["square_mod_4n"])
                  & set(r["D"] for r in res["cooper_s10"]["discriminant_table"] if r["square_mod_4n"]),
                  reverse=True)
    pts = [R["point"] for R in res.values() if "point" in R]
    checks = {
        "stage0_all_hold": all(s0.values()),
        "criterion_equals_box_both_inclusions":
            all(row["square_mod_4n"] == row["found_in_box"]
                for R in res.values() for row in R["discriminant_table"]),
        "per_vector_violations_all_clauses":
            sum(c for R in res.values() for c in R["box"]["violations_by_clause"].values()),
        "external_citations_not_phantom": citations_ok,
        "p2_certificate_not_contradicted": p2["status"] != "CONTRADICTION",
        "stabilizer_order_matches_L3_exponent_denominator":
            all(P["stabilizer_order_equals_exponent_denominator"] is not False for P in pts),
        "all_A2_vectors_in_window_share_one_z":
            all(R["all_A2_vectors_in_window_share_one_z"]["all_same_one_over_z"]
                for R in res.values() if "point" in R),
    }
    ok = checks_ok(checks)
    summary_table = [{"D": row7["D"], "fundamental": row7["fundamental"],
                      "n7": row7["square_mod_4n"], "n10": row10["square_mod_4n"]}
                     for row7, row10 in zip(res["cooper_s7"]["discriminant_table"],
                                            res["cooper_s10"]["discriminant_table"])
                     if row7["square_mod_4n"] or row10["square_mod_4n"]]
    cert = {
        "certificate": "A2_MEMBERSHIP",
        "checker": "checkers/check_A2_membership.py",
        "checker_version": commit_state()["label"],
        "checker_commit_state": commit_state(),
        "date": "2026-09-21",
        "status": ("RECORD, NOT A GATE. The rho = 20 cut was ADOPTED by T0 on 2026-09-21 (D7', briefs/T0_DECISIONS_2026_09_21_STREAM2.md), read narrowly: no ranking of candidates, no minimum-|D| rule, no physical reading. "
                   "K3_CRITERIA.md unchanged. No scoring. cooper_s10 advisory "
                   "(lattice certificate DRAFT)."),
        "claim": ("Tier B: T_7 = U+<14> contains a primitive v with v^perp isometric to A2, so -- "
                  "within the cited framework -- the M_7-polarized family (Dolgachev moduli "
                  "space X_0(7)+), of which cooper_s7 is the period operator, contains a point "
                  "whose transcendental lattice is A2; in the s7 coordinate that point is "
                  f"z = infinity (relation PASS({CM.ORDER}) + Tier B numeric recognition), a "
                  "singular point of L3, and the explicit projective model is not examined "
                  "there (see not_claimed). T_10 = U+<20> contains no such v (exact congruence "
                  "over all v), so the M_10-polarized family as the DRAFT cooper_s10 lattice "
                  "certificate records it does not."),
        "tier": "B",
        "headline": {k: {"n": R["n"], "A2": R["membership_A2"]["verdict"],
                         "fired": R["membership_A2"]["fired"], "advisory": R["advisory"]}
                     for k, R in res.items()},
        "tier_links": {
            "finite_order": [f"the relation 1/z = alpha t + beta + gamma/t per family: "
                             f"PASS({CM.ORDER}) (T3.modular_leg, q-order {CM.ORDER}); every z "
                             "statement, z = infinity included, depends on it"],
            "exact": ["stage-0 sympy identities (leg A i, ii, iv)", "squares modulo 4n by exhaustion",
                      "every witness vector and its v^perp", f"box enumeration |coords| <= {BOX}",
                      "criterion == box on both inclusions for |D| <= " + str(D_MAX),
                      "tau; the Gamma_0(n) stabilizer"],
            "argument_in_docstring_not_machine_proved": [
                "leg A (iii): c = +-Gv/div(v); cross-checked by CM.verify_TX's det identity on every "
                "vector touched"],
            "numeric_recognition_tier_B": ["every t, 1/z value; two precisions "
                                           f"({CM.DPS_FIT} and {CM.DPS_VERIFY} digits)"],
            "framework_cited_tier_B": [
                "as check_CM_points_rho20.py: Dolgachev 1996 sec 7 (read, hash-pinned); Lefschetz "
                "(1,1) (standard, not among the pinned statements)"],
            "read_as_source_no_lean_build": [
                f"LeanMaster @ {EXTERNAL_CITATIONS['leanmaster_target']['commit']}: "
                "AttractorCharges.lean `smallest_black_hole` (statement only), "
                "STREAM8_WHICH_K3.md sec G10",
                f"Stream 1 @ {EXTERNAL_CITATIONS['stream1_G0N']['commit']}: SymSquareForms.lean "
                "no_isometry_G0N_TN, ModularAction.lean g3_fixes and its docstring"]},
        "external_citations_verified_at_run_time": citations,
        "inputs": {"sha256": input_hashes()},
        "not_claimed": NOT_CLAIMED,
        "parameters": {"TARGET_FORM": list(TARGET_FORM), "BOX": BOX, "D_MAX": D_MAX,
                       "WINDOW_BOUND": WINDOW_BOUND, "STAB_BOUND": STAB_BOUND,
                       "DPS_FIT": CM.DPS_FIT, "DPS_VERIFY": CM.DPS_VERIFY},
        "stage0_symbolic": s0,
        "hand_estimate": pred,
        "p2_certificate_agreement": p2,
        "discriminants_admitted_summary": summary_table,
        "discriminants_admitted_by_both": both,
        "checks": checks,
        "controls": "checkers/test_A2_membership_controls.py",
        "families": _jsonable(res),
        "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: "
                      "test_A2_membership_controls.py | Reviewed-by: N",
    }
    log(f"\nchecks: {checks}; elapsed {time.time() - t0:.0f}s")
    if args.emit:
        OUT.write_text(json.dumps(cert, indent=1) + "\n")
        log(f"wrote {OUT.relative_to(REPO)}")
    if args.brief:
        BRIEF.write_text(render_brief(json.loads(OUT.read_text())))
        log(f"rendered {BRIEF.relative_to(REPO)} from {OUT.relative_to(REPO)}")
    return 0 if ok else 1


def checks_ok(checks):
    """Booleans must be True, counts must be the int 0.  (`False == 0` in Python: a bare
    `v == 0` test would wave a failed boolean through -- control S10.)"""
    return all((v is True) or (type(v) is int and v == 0) for v in checks.values())


def code_files():
    """Every module a number in the certificate is computed by (this file included)."""
    return [Path(__file__).resolve(), Path(CM.__file__).resolve(), Path(T3.__file__).resolve(),
            Path(T3.H7.__file__).resolve(), Path(T3.H10.__file__).resolve(),
            Path(T3.C1.__file__).resolve()]


def input_hashes():
    h = dict(CM.input_hashes())
    files = [CERTS / RIEMANN_CERT] + code_files()
    files += [CERTS / spec["t1_cert"] for spec in T3.CANDIDATES.values()]
    if (CERTS / P2_CERT).exists():
        files.append(CERTS / P2_CERT)
    for f in files:
        if Path(f).exists():
            h[str(Path(f).relative_to(REPO))] = CM.sha256_file(f)
    return dict(sorted(h.items()))


def commit_state():
    """HEAD, and which of the code files are NOT what HEAD contains (untracked or modified).
    A bare HEAD hash would misattribute an uncommitted checker to that commit."""
    import subprocess
    head = CM.git_head()
    rels = [str(f.relative_to(REPO)) for f in code_files()]
    try:
        out = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain", "--"] + rels,
                             capture_output=True, text=True, check=True).stdout
        dirty = sorted(line[3:] for line in out.splitlines() if line.strip())
    except Exception:
        dirty = None
    if dirty is None:
        label = f"{head} (git state unknown; identify the code by inputs.sha256)"
    elif dirty:
        label = (f"run on top of HEAD {head}; {len(dirty)} code file(s) uncommitted or modified "
                 "-- identify the code by inputs.sha256, not by this commit")
    else:
        label = head
    return {"head": head, "code_files_not_as_in_head": dirty, "label": label}


# ---------------------------------------------------------------------- brief ----
def render_brief(c):
    """The brief, rendered from the certificate dict `c` (as read back from the JSON file).
    Every number, vector, list and verdict below is looked up in `c`; the prose is fixed."""
    f7, f10 = c["families"]["cooper_s7"], c["families"]["cooper_s10"]
    m7, m10 = f7["membership_A2"], f10["membership_A2"]
    P = f7.get("point")
    par = c["parameters"]
    cit = c["external_citations_verified_at_run_time"]
    L = []
    w = L.append
    w("# Stream 2 brief: A2 membership in the cooper_s7 / cooper_s10 M_n-polarized families "
      f"({c['date']})")
    w("")
    w("**Status: RECORD, NOT A GATE.** The rho = 20 cut was ADOPTED by T0 on 2026-09-21 (D7', briefs/T0_DECISIONS_2026_09_21_STREAM2.md), read narrowly: no ranking of candidates, no minimum-|D| rule, no physical reading. "
      "`K3_CRITERIA.md` is unchanged, nothing is scored, no candidate "
      "or family member is ranked or preferred. This is lattice / modular arithmetic, Tier B at "
      "best, with no physical reading.")
    w("")
    w(f"This file is rendered from `data/certificates/A2_MEMBERSHIP.json` by "
      f"`python3 {c['checker']} --brief` (function `render_brief`); numbers are looked up in the "
      "certificate, not typed. Code identity: " + c["checker_version"] + ". The checker imports "
      "`checkers/check_CM_points_rho20.py` and does not duplicate it; the sha256 of every code "
      "and data file used is in the certificate under `inputs.sha256` "
      f"({len(c['inputs']['sha256'])} files).")
    w("")
    w("## Question")
    w("")
    lm = cit["leanmaster_target"]
    w("LeanMaster's theorem `smallest_black_hole` (`DualScaleDyons/AttractorCharges.lean`, read as "
      f"source at commit `{lm['commit']}`, citation status {lm['status']}, no Lean build run; the "
      "theorem name is LeanMaster's and is quoted as an identifier only) states "
      "`reducedForms 3 = [(1, 1, 1)]`: the one reduced form of discriminant -3 is A2, Gram "
      "[[2,1],[1,2]]. The checker recomputes that list and re-verifies the citation at run time. "
      "Does A2 occur as v^perp for a primitive v of negative norm in T_n = U + <2n>, for "
      f"n = {f7['n']} (cooper_s7) and n = {f10['n']} (cooper_s10)? Within the cited framework "
      "(Dolgachev 1996 sec 7, read and hash-pinned; Lefschetz (1,1), standard and not among the "
      "pinned statements) that is the condition for the M_n-polarized family to contain a point "
      "whose transcendental lattice is A2. The checker computes the lattice side only.")
    w("")
    w("## Result")
    w("")
    w("| family | n | A2 | clause that fired | scope |")
    w("|---|---|---|---|---|")
    for key, fam in c["families"].items():
        m = fam["membership_A2"]
        tag = " (ADVISORY, lattice cert DRAFT)" if fam["advisory"] else ""
        w(f"| {key}{tag} | {fam['n']} | **{m['verdict']}** | `{m['fired']}` | {m['scope']} |")
    w("")
    if m7["verdict"] == "PRESENT":
        w("Cautious wording, Tier B: **the M_7-polarized family (Dolgachev moduli space X_0(7)+; "
          "cooper_s7 is its period operator) contains a point whose transcendental lattice is A2, "
          f"and in the s7 coordinate that point is z = {P['z']}** - a singular point of L3, where "
          "the explicit projective model is not examined (see Not claimed). The lattice statement "
          f"is exact: T_{f7['n']} contains the primitive vector v = {tuple(m7['v'])} with "
          f"-v^2 = {m7['minus_v2']}, div(v) = {m7['div_v']}, v^perp with Z-basis "
          f"{m7['kernel_basis']} and Gram {m7['gram']}, which Gauss-reduces to "
          f"{tuple(m7['reduced_form'])}.")
    else:
        w(f"cooper_s7: verdict {m7['verdict']} (clause `{m7['fired']}`).")
    if m10["verdict"] == "ABSENT":
        w(f"**T_{f10['n']} = U + <{2 * f10['n']}> contains no such vector**: -3 mod "
          f"{4 * f10['n']} = {m10['D_mod_4n']} is not among the squares mod {4 * f10['n']}, "
          f"{m10['squares_mod_4n']}. The s10 statement is arithmetic of the lattice recorded in "
          f"the DRAFT certificate `{f10['lattice_cert']}` and is advisory.")
    else:
        w(f"cooper_s10: verdict {m10['verdict']} (clause `{m10['fired']}`).")
    w("")
    w('### Why the n = 10 negative is not "not found within a bound"')
    w("")
    w("Leg (A) of the checker covers all primitive v. With G = Gram(T_n), d = div(v), K = v^perp "
      "with basis u1, u2 and c = u1 x u2: (i) det(U^T G U) = c^T adj(G) c and (ii) "
      "(Gv)^T adj(G) (Gv) = det(G) v^T G v are checked symbolically (sympy, generic G); (iii) "
      "c = +-Gv/d because both are primitive and Euclidean-orthogonal to u1, u2 - this step is a "
      "three-line argument in the checker docstring, not a machine proof; (iv) with x = d x', "
      "y = d y', beta = 2nz/d, sympy gives D = beta^2 + 4n x'y'. So D is a square mod 4n for "
      "every v (the Heegner condition at level n). The squares mod 4n are found by exhaustion. "
      "The converse is constructive: each beta with beta^2 = D mod 4n gives a vector, and every "
      "such vector in the table is verified exactly. Stage-0 identities: "
      + ", ".join(f"{k} = {v}" for k, v in c["stage0_symbolic"].items()) + ".")
    w("")
    b7, b10 = f7["box"], f10["box"]
    w(f"Leg (B), bounded and stated as such: all primitive negative-norm v with |x|, |y|, |z| <= "
      f"{par['BOX']} ({b7['primitive_negative_norm_vectors_checked']} vectors at n = {f7['n']}, "
      f"{b10['primitive_negative_norm_vectors_checked']} at n = {f10['n']}). The determinant "
      f"identity held on {b7['det_identity_held_on']} and {b10['det_identity_held_on']} of them; "
      "the congruence D = (2nz/d)^2 mod 4n is checked on each; violations counted over both "
      f"families, all clauses: {c['checks']['per_vector_violations_all_clauses']}. "
      + (m10.get("box_cross_check", "") + "." if m10["verdict"] == "ABSENT" else ""))
    w("")
    if P:
        rel = P["relation_1_over_z"]
        st = P["gamma0_n_stabilizer"]
        W = f7["all_A2_vectors_in_window_share_one_z"]
        w("## The n = 7 point")
        w("")
        w(f"- tau = {P['tau_readable']} (exact). Every A2 vector in the box has (-v^2, div) in "
          f"{m7['minus_v2_and_div_of_every_such_vector_in_box']}; the exact necessary conditions "
          f"allow only {m7['forced_minus_v2_and_div_exact']}.")
        w(f"- The z statement rests on two things. (a) The relation 1/z = {rel['alpha']} t + "
          f"{rel['beta']} + {rel['gamma']}/t (t the level-{f7['n']} eta quotient), certified by "
          f"`T3.modular_leg` to q-order {P['relation_order_checked']} only: "
          f"**{P['relation_verdict']}**, a finite order, evidence and not a proof. (b) The "
          "numeric evaluation of t at tau.")
        w(f"- z = **{P['z']}**. {P['z_recognition']}; log10 |1/z| = "
          + ", ".join(f"{v:.1f} at {k} digits" for k, v in P["log10_abs_one_over_z"].items()
                      if v is not None) + ".")
        if P["t_exact_support"]:
            w(f"  Exact support: with (alpha, beta, gamma) = ({rel['alpha']}, {rel['beta']}, "
              f"{rel['gamma']}), alpha t^2 + beta t + gamma is proportional to the recognised "
              f"minimal polynomial of t, `{P['t_minpoly']}` (itself a Tier B numeric "
              "recognition): "
              f"{P['t_exact_support']['alpha_t2_plus_beta_t_plus_gamma_proportional_to_it']}.")
        w(f"- Finite singular loci of the C1 certificate: {P['finite_singular_loci_from_C1_cert']}. "
          f"The A2 point is a finite singular locus: **{P['is_a_finite_singular_locus']}**. It is "
          f"a singular point of L3 on P^1: **{P['is_a_singular_point_of_L3_on_P1']}** - exponents "
          f"{P['L3_exponents_there']} at z = infinity in `L3_RIEMANN_SCHEME.json` (denominator "
          f"lcm {P['L3_exponent_denominator_lcm']}).")
        if st["elements"]:
            e = st["elements"][0]
            w(f"- Exact integer search (entries up to {st['search_bound']}): tau is fixed by "
              f"{e['matrix']} in Gamma_0({f7['n']}) (trace {e['trace']}), so it is an elliptic "
              f"point of order {st['order_in_PSL2']}; that order equals the exponent denominator: "
              f"{P['stabilizer_order_equals_exponent_denominator']}.")
        w(f"- Bounded: the {W['count']} A2 vectors of the P2 window ({W['window']}), "
          f"{W['vectors']}, share one value of 1/z: {W['all_same_one_over_z']}.")
        E = f7["elliptic_pair"]
        w(f"- \"An\" versus \"the\": the Fricke image of v is {tuple(E['fricke_image_of_v'])} "
          f"(exact; its v^perp reduces to {tuple(E['fricke_image_vperp_reduced_form'])}). The "
          "number of x mod 7 with x^2 + x + 1 = 0 is "
          f"{E['count_x_mod_n_with_x2_plus_x_plus_1_zero']}, which is the standard count of "
          "order-3 elliptic points of Gamma_0(7) (standard formula, cited not proved, not among "
          "the pinned sources). Numerically (Tier B) t differs at the two points: "
          f"{E['t_differs_at_the_two_points_numeric']}, and 1/z agrees: "
          f"{E['one_over_z_agrees_at_the_two_points_numeric']}. So tau is AN order-3 elliptic "
          "point of Gamma_0(7) - one of a Fricke-swapped pair - and THE order-3 point of "
          "X_0(7)+, the curve z lives on.")
        s1 = cit.get("stream1_elliptic_point_already_on_record", {})
        w("")
        w('So the hand estimate\'s last sentence ("it should not be one of the singular loci") '
          "holds for the finite loci and fails for the projective line: the A2 point is the "
          "order-3 elliptic point of X_0(7)+, which is the third singular point of the operator, "
          "z = infinity. This was already on record in Stream 1: the docstring of `g3_fixes` "
          f"(`ModularAction.lean` at `{s1.get('commit')}`, citation status {s1.get('status')}) "
          "says that (14,-14,5) corresponds to the order-3 elliptic point of X_0(7). Consequence "
          "recorded in `not_claimed`: what is established is a point of the period domain; "
          "whether the explicit Almkvist-van Straten model has a smooth fibre there is not "
          "examined. No Kodaira reading is made (ledger item 3).")
        w("")
    h = c["hand_estimate"]
    w("## Hand estimate, scored")
    w("")
    w(h["statement"] + ".")
    w("")
    w("| clause | outcome |")
    w("|---|---|")
    for cl, ok in h["clauses"].items():
        w(f"| {cl.replace('|', '&#124;')} | {'confirmed' if ok else '**REFUTED**'} |")
    w("")
    w(f"Outcome: {h['outcome']}.")
    w("")
    w(f"## Discriminants admitted, -{par['D_MAX']} <= D < 0")
    w("")
    w("Criterion (D square mod 4n, all v) and box enumeration agree on both inclusions for both "
      f"n: {c['checks']['criterion_equals_box_both_inclusions']} (computed row by row; either "
      "disagreement also stops the run, clauses `enumeration_outside_criterion`, "
      "`criterion_not_reached_in_box`). The second inclusion is bounded by the box. Imprimitive "
      "forms are included. The certificate also lists, per D, the lattice classes seen in the box "
      "and among the witnesses; those lists are not claimed complete (control S5 exhibits a "
      "class of an admitted D that is not seen).")
    w("")
    w("| D | fundamental | n = 7 | n = 10 |")
    w("|---|---|---|---|")
    for row in c["discriminants_admitted_summary"]:
        w(f"| {row['D']} | {'yes' if row['fundamental'] else 'no'} | "
          f"{'yes' if row['n7'] else '-'} | {'yes' if row['n10'] else '-'} |")
    w("")
    fund = {row["D"] for row in c["discriminants_admitted_summary"] if row["fundamental"]}
    both = c["discriminants_admitted_by_both"]
    w(f"Admitted by both: {both}; of these fundamental: {[D for D in both if D in fund]}.")
    w("")
    w(f"## Controls (`{c['controls']}`, each reports the clause that fired)")
    w("")
    w("R1 real known-negative A2 at n = 10 (`D_not_square_mod_4n`); R2 (1,0,1) at n = 7, same "
      "clause; R3 non-vacuity both ways; R4 Stream 1's (14,-14,5) and the P2 certificate; R5 "
      "stabilizer order 3 vs trivial. S1a the Gauss discriminant lattice G0N of Stream 1's "
      "`no_isometry_G0N_TN` fed in place of T_n is refused on `lattice_not_even` (optional "
      "path) and, through the PRODUCTION call with the registry entry swapped, on "
      "`lattice_leg_refused`; S1b an even lattice with the Gauss determinant is refused on "
      "`lattice_level_mismatch` (optional path) and on `no_level_coordinate` (production "
      "path), and the control computes that accepting it would have flipped the s7 headline. "
      "S2 wrong-level criterion; S2x records that \"mod 2n\" is no tamper at odd n (a "
      "first-draft control that rightly did not fire); S3 small box; S4 tampered witness; S5 "
      "PRESENT is not awarded on D alone; S6 wrong-n congruence, per vector and counted over a "
      "box; S7 tampered relation (`w_not_zero`); S8 non-reduced target; S9 phantom citation; "
      "S10 the exit-code gate does not read a failed boolean as the count 0; S11 the brief "
      "renderer follows the certificate.")
    w("")
    w("## Not claimed")
    w("")
    for item in c["not_claimed"]:
        w(f"- {item}")
    w("")
    w("## For T0")
    w("")
    w("Nothing here needs a ruling. If the rho = 20 question is ever taken up, the two facts to "
      f"carry are: (1) A2 is {m7['verdict']} at n = {f7['n']} and {m10['verdict']} at "
      f"n = {f10['n']} (s10 advisory); (2) the n = 7 A2 point is z = "
      f"{P['z'] if P else 'n/a'} (relation {P['relation_verdict'] if P else 'n/a'}), the order-3 "
      "elliptic point of X_0(7)+, not a generic member.")
    w("")
    w("Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: check_A2_membership.py + "
      "test_A2_membership_controls.py | Reviewed-by: N")
    return "\n".join(L) + "\n"


def _jsonable(o):
    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [_jsonable(v) for v in (sorted(o) if isinstance(o, set) else o)]
    return o


if __name__ == "__main__":
    sys.exit(main())
