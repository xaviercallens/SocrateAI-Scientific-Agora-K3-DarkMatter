#!/usr/bin/env python3
"""
check_NS_genus_G0.py — WP S2-G Phase G0
(briefs/WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md sec.5, G0 row; opened by T0
2026-07-28, decision log at the bottom of that file, commit 1dd660a).

WHAT THIS COMPUTES
-------------------
The Neron-Severi genus of the generic K3 fiber in the certified cooper_s7
family, as the Nikulin orthogonal complement of the certified transcendental
lattice T inside the K3 lattice Lambda = U^3 (+) E8(-1)^2, and answers the
plan's G1-c load-bearing question EXACTLY, in NS terms:

    MATCH CRITERION: does NS contain a primitive isotropic vector of
    divisor 1 — equivalently, does U embed as an ORTHOGONAL DIRECT SUMMAND
    of NS?  This is necessary and sufficient (Huybrechts *Lectures on K3
    Surfaces*, Ch.14 Example 0.3, and the classical Piatetski-Shapiro -
    Shafarevich / Nikulin correspondence between primitively-isotropic NS
    classes and genus-one fibrations) for the generic fiber to carry an
    elliptic fibration WITH SECTION over P^1 — the fact Route A's G1-c step
    needs.  If NO: the plan's own documented stop condition fires
    (G0 row, "Stop condition": "NS genus lacks U summand -> G1-c expectation
    dies -> HALT, report").

METHOD (exact lattice arithmetic; Nikulin's theory of primitive embeddings
of even lattices into the K3 lattice, as read in Huybrechts *Lectures on K3
Surfaces* Ch.14 -- docs/literature/huybrechts_K3Global.pdf/.txt, hash-pinned
in docs/literature/MANIFEST.md; theorem numbers below are Huybrechts's,
attributed there to Nikulin [448] and Eichler; this is the SAME textbook
already cited (E-011) and the same primitive-embedding style of argument
check_U1_lattice.py used for T's own U-splitting)
-------------------------------------------------------------------------
1. T is re-derived FRESH from source (checkers/check_U1_lattice.py's own
   run_family()), NOT parsed out of the certificate JSON — "read the source,
   not the certificate" (CLAUDE.md standing rule 2). Its Gram/det/signature/
   disc-form are then cross-checked bit-for-bit against the accepted LIVE
   certificate data/certificates/C2_cooper_s7_v5.json as an integrity gate.

2. The K3 lattice Lambda = U^3 (+) E8(-1)^2 is built explicitly (rank 22
   Gram matrix) and its defining properties — even, unimodular (det = -1),
   signature (3,19) — are VERIFIED computationally (exact Sylvester-criterion
   determinant test for E8 positive-definiteness, exact charpoly real-root
   count for signature), not merely asserted from memory. This is the unique
   even unimodular lattice of signature (3,19) (Huybrechts Thm 1.1: n+,n->0
   => unique) and is identified with H^2(K3,Z) as an abstract lattice
   (Huybrechts Ch.14 sec 0.3.vi / Example 1.4.i) — a classical fact of K3
   Hodge theory, cited not re-derived.

3. Existence + UNIQUENESS of a primitive embedding T -> Lambda: Huybrechts
   Thm 1.12 (= Nikulin [448] Thm 1.14.4). Conditions checked exactly:
   m+ < n+, m- < n-, and ell(A_T) + 2 <= rk(Lambda) - rk(T), where ell(A_T)
   is the minimal number of generators of T's discriminant group (computed
   via exact Smith normal form of T's Gram, not assumed). Because the
   embedding is unique up to Aut(Lambda), NS := T^perp is well-defined up to
   isometry — the question "does NS contain U" has one right answer, not one
   per choice of embedding.

4. NS's GENUS (signature + discriminant form) is pinned down exactly:
   - signature(NS) = (n+ - m+, n- - m-)   [additivity of signature under the
     finite-index orthogonal splitting Lambda_Q = T_Q (+) NS_Q]
   - (A_NS, q_NS) ~= (A_T, -q_T)          [Huybrechts Prop 0.2(i), since
     Lambda is unimodular and T, NS are its mutual orthogonal complements]
   both computed by the SAME generic exact dual-lattice routine used on T.

5. UNIQUENESS OF NS IN ITS GENUS: Huybrechts Thm 1.5 ("If ell(A)+2 <=
   n+ + n- and n_+/- > 0 [the p=2 edge case does not bite here: it only
   applies when ell((A)_2) = rk exactly, and ell=1 << rk], then Lambda is
   the UNIQUE even lattice of that signature and discriminant form").
   ell(A_NS) = ell(A_T) = 1 (T's discriminant group is cyclic — checked
   from SNF, |det T| squarefree-or-not is irrelevant, only ell matters), and
   1+2=3 <= rk(NS)=19, both n_+/-(NS) > 0: the bound holds, so NS is unique
   in its genus.

6. An EXPLICIT representative of that genus is exhibited: the block sum
   U (+) E8(-1) (+) E8(-1) (+) <-d> where d = |det T|. Its rank, signature,
   and discriminant form are computed by the identical generic routine and
   checked EQUAL (not merely "isomorphic in principle") to NS's required
   genus data. By step 5's uniqueness, NS IS isometric to this candidate.
   The candidate manifestly contains U as an orthogonal direct summand (it
   is block-diagonal with U as the first block) — QED the match criterion.

TIER: the *lattice arithmetic* in this file (steps 2-6) is exact throughout
(sympy Integer/Rational, no floats, no numerical tolerance anywhere) and
would be Tier A/E in isolation. The certificate's overall claim inherits
Tier B from its INPUT: T's identification with the actual transcendental
lattice of the cooper_s7 family is Tier B (C2_cooper_s7_v5.json; monodromy
entries recognized numerically with a loud tolerance gate, framework
theorem citations not kernel-proofs). This script does not upgrade that —
see the certificate's "tier" / "tier_reason" fields.

REGRESSION CONTROL: the identical pipeline is also run on cooper_s10 (T =
U + <20>, det -20 vs s7's det -14 — already certified as a discriminating
control in C2_cooper_s7_v5.json's own controls block). The two families
MUST produce numerically DIFFERENT NS genus data (different d => different
discriminant form/det), proving this checker is not a constant-return stub.
See checkers/test_NS_genus_G0_controls.py for negative (must-fail) controls.

Usage:
  python3 checkers/check_NS_genus_G0.py                  # s7 (+ s10 control), print only
  python3 checkers/check_NS_genus_G0.py --emit-cert       # also write the certificate JSON

Exit codes: 0 all structural assertions passed. 3 a structural assertion
failed (this would BE the plan's stop condition if it were the U-summand
check itself that failed).

Generated-by: Sonnet 5 (Stream 2, WP S2-G Phase G0 session 2026-07-28)
Verified-by: this script's own structural assertions + checkers/test_NS_genus_G0_controls.py
Reviewed-by: pending T0 (Xavier) — coordinator reviews and commits per plan sec.5 footer
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import mpmath as mp
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_U1_lattice as U1  # noqa: E402  (re-derive T from source, not the certificate)

REPO = Path(__file__).resolve().parent.parent
CERT_S7_LIVE = REPO / "data" / "certificates" / "C2_cooper_s7_v5.json"
HUYBRECHTS_PDF = REPO / "docs" / "literature" / "huybrechts_K3Global.pdf"

MATCH_CRITERION = (
    "NS contains a primitive isotropic vector of divisor 1, equivalently U "
    "embeds as an orthogonal DIRECT SUMMAND of NS (not merely a sublattice) "
    "-- necessary and sufficient for the generic K3 fiber to carry an "
    "elliptic fibration WITH SECTION over P^1 (Huybrechts Ch.14 Ex 0.3; "
    "Piatetski-Shapiro-Shafarevich / Nikulin genus-one-fibration correspondence)."
)


class ControlFailure(Exception):
    """A structural assertion failed — the loud path."""


def chk(cond, msg):
    if not cond:
        raise ControlFailure(msg)


# ----------------------------------------------------------------------------
# generic exact lattice-arithmetic primitives (integer/rational sympy only)
# ----------------------------------------------------------------------------

def signature(G):
    """Exact signature (n+, n-) of a nondegenerate symmetric integer Gram
    matrix via exact real roots of its characteristic polynomial (no floats,
    no eigenvalue numerics — same style as check_U1_lattice.py stage3)."""
    n = G.shape[0]
    lam = sp.Symbol("lam")
    cp = sp.Poly(G.charpoly(lam).as_expr(), lam)
    rts = cp.real_roots()
    chk(len(rts) == n and all(r != 0 for r in rts), "degenerate Gram matrix")
    pos = sum(1 for r in rts if r > 0)
    neg = sum(1 for r in rts if r < 0)
    return (pos, neg)


def discriminant_data(G):
    """Exact discriminant-group data of an even nondegenerate integer Gram
    matrix G (rank n): det, minimal-generator count ell(A_G) via Smith
    normal form of G itself, and an explicit generating set of (A_G, q_G)
    from the columns of G^{-1} restricted to the standard basis (same
    construction check_U1_lattice.py's stage3_lattice uses for T)."""
    n = G.shape[0]
    det = G.det()
    chk(det != 0, "degenerate Gram matrix")
    chk(all(G[i, i] % 2 == 0 for i in range(n)), "Gram matrix is not even")
    S = smith_normal_form(G)
    diag = [int(S[i, i]) for i in range(n)]
    ell = sum(1 for d in diag if abs(d) not in (0, 1))
    Ginv = G.inv()
    gens = []
    for i in range(n):
        v = Ginv[:, i]
        order = sp.lcm([x.q for x in v])
        if order == 1:
            continue
        qval = sp.nsimplify((v.T * G * v)[0, 0]) % 2
        gens.append({"order": int(order), "q_value_mod_2Z": str(qval)})
    return {"rank": n, "det": int(det), "ell": ell, "disc_form_generators": gens}


def cyclic_disc_form(gens, label):
    """Extract the (order, q) of the single nontrivial cyclic generator from
    a discriminant_data() generator list; fail loudly if the group is not
    cyclic-of-length-1 (this checker's argument is specific to that case)."""
    chk(len(gens) == 1, f"{label}: discriminant group is not length-1 cyclic "
        f"(got {len(gens)} nontrivial generators) — the block-sum-candidate "
        "argument in this file does not apply as written")
    return gens[0]["order"], sp.Rational(gens[0]["q_value_mod_2Z"])


# ----------------------------------------------------------------------------
# the K3 lattice Lambda = U^3 (+) E8(-1)^2, built + verified, not assumed
# ----------------------------------------------------------------------------

def e8_gram():
    """Standard E8 Cartan-type Gram matrix (Huybrechts Ch.14 sec 0.3.iii).
    Verified below (not assumed) to be even, unimodular, positive definite
    of rank 8 -- by Milnor's classical uniqueness of the even unimodular
    positive-definite rank-8 lattice, ANY matrix passing those three checks
    IS (isometric to) E8, so the specific basis chosen here is immaterial."""
    E8 = sp.Matrix([
        [2, -1, 0, 0, 0, 0, 0, 0],
        [-1, 2, -1, 0, 0, 0, 0, 0],
        [0, -1, 2, -1, 0, 0, 0, 0],
        [0, 0, -1, 2, -1, 0, 0, 0],
        [0, 0, 0, -1, 2, -1, 0, -1],
        [0, 0, 0, 0, -1, 2, -1, 0],
        [0, 0, 0, 0, 0, -1, 2, 0],
        [0, 0, 0, 0, -1, 0, 0, 2],
    ])
    chk(E8 == E8.T, "E8 candidate matrix not symmetric")
    chk(all(E8[i, i] == 2 for i in range(8)), "E8 candidate matrix not even/norm-2 diagonal")
    # exact positive-definiteness via Sylvester's criterion (leading principal
    # minors all > 0) -- no eigenvalue numerics
    minors = [E8[:k, :k].det() for k in range(1, 9)]
    chk(all(m > 0 for m in minors), f"E8 candidate matrix not positive definite: minors={minors}")
    chk(E8.det() == 1, f"E8 candidate matrix not unimodular: det={E8.det()}")
    return E8


def k3_lattice_gram():
    """Lambda = U^3 (+) E8(-1)^2, rank 22. Verified: even, unimodular
    (det=-1), signature (3,19) — matching Huybrechts Ch.14 sec 0.3.vi /
    Example 1.4.i (H^2(K3,Z) as an abstract lattice)."""
    U = sp.Matrix([[0, 1], [1, 0]])
    E8m = -e8_gram()
    Lam = sp.diag(U, U, U, E8m, E8m)
    chk(Lam.shape == (22, 22), "Lambda not rank 22")
    chk(all(Lam[i, i] % 2 == 0 for i in range(22)), "Lambda not even")
    chk(Lam.det() == -1, f"Lambda not unimodular: det={Lam.det()}")
    sig = signature(Lam)
    chk(sig == (3, 19), f"Lambda signature {sig} != (3,19)")
    return Lam


# ----------------------------------------------------------------------------
# Nikulin complement: T -> Lambda primitive embedding, NS := T^perp genus
# ----------------------------------------------------------------------------

def nikulin_complement(T_gram, family_label, scramble_d_offset=0):
    """Given T's exact Gram matrix, compute + certify NS = T^perp's genus
    inside the K3 lattice, and the explicit U-summand candidate. Returns a
    result dict. Raises ControlFailure if any precondition or the match
    check fails (the latter would BE the plan's own stop condition).

    Lambda = K3 lattice is built and its defining properties VERIFIED here
    via k3_lattice_gram() on every call — Lam_sig/Lam_rank are read off that
    verified matrix, never hardcoded independently of it (a prior draft of
    this function accepted them as separate default arguments, which could
    silently drift out of sync with the actual matrix; fixed before the
    certificate was emitted)."""
    Lam = k3_lattice_gram()
    Lam_rank = Lam.shape[0]
    Lam_sig = signature(Lam)
    m_sig = signature(T_gram)
    Tdata = discriminant_data(T_gram)
    order_T, q_T = cyclic_disc_form(Tdata["disc_form_generators"], f"{family_label}: T")

    # --- step 3: existence + uniqueness of the primitive embedding T -> Lambda
    # (Huybrechts Thm 1.12 / Nikulin [448] Thm 1.14.4)
    chk(m_sig[0] < Lam_sig[0] and m_sig[1] < Lam_sig[1],
        f"{family_label}: embedding-uniqueness precondition m+ < n+, m- < n- "
        f"fails: m={m_sig}, n={Lam_sig}")
    bound = Lam_rank - T_gram.shape[0]
    chk(Tdata["ell"] + 2 <= bound,
        f"{family_label}: embedding existence/uniqueness bound ell(A_T)+2 <= "
        f"rk(Lambda)-rk(T) fails: {Tdata['ell']}+2 > {bound}")

    # --- step 4: NS's genus
    ns_sig = (Lam_sig[0] - m_sig[0], Lam_sig[1] - m_sig[1])
    ns_rank = Lam_rank - T_gram.shape[0]
    chk(ns_rank == ns_sig[0] + ns_sig[1], "internal inconsistency: NS rank vs signature")
    order_ns_required = order_T
    q_ns_required = sp.Rational(-q_T) % 2   # Prop 0.2(i): (A_NS,q_NS) ~= (A_T,-q_T)

    # --- step 5: uniqueness of NS in its genus (Huybrechts Thm 1.5 / Rmk 1.6)
    ell_ns = Tdata["ell"]  # |A_NS| = |A_T| as abstract groups (Prop 0.2(i)); both cyclic length 1
    chk(ell_ns + 2 <= ns_rank and ns_sig[0] > 0 and ns_sig[1] > 0,
        f"{family_label}: NS genus-uniqueness bound fails "
        f"(ell={ell_ns}, rank={ns_rank}, sig={ns_sig}) — genus does NOT pin "
        "down a unique isometry class; this checker's method is inconclusive "
        "(NOT the same as a NO on the U-summand question — would need escalation)")

    # --- step 6: explicit candidate U (+) E8(-1)^2 (+) <-d>, d = |det T|
    d = abs(Tdata["det"]) + scramble_d_offset  # scramble hook: negative controls only
    U_ = sp.Matrix([[0, 1], [1, 0]])
    E8m = -e8_gram()
    twist = sp.Matrix([[-d]])
    cand = sp.diag(U_, E8m, E8m, twist)
    cand_rank = cand.shape[0]
    cand_sig = signature(cand)
    cand_data = discriminant_data(cand)

    chk(cand_rank == ns_rank, f"{family_label}: candidate rank {cand_rank} != NS rank {ns_rank}")
    chk(cand_sig == ns_sig, f"{family_label}: candidate signature {cand_sig} != NS signature {ns_sig}")
    order_cand, q_cand = cyclic_disc_form(cand_data["disc_form_generators"], f"{family_label}: candidate")
    chk(order_cand == order_ns_required,
        f"{family_label}: candidate disc-group order {order_cand} != required {order_ns_required}")
    chk(sp.Rational(q_cand) % 2 == q_ns_required,
        f"{family_label}: candidate q-value {q_cand} != required -q_T = {q_ns_required} (mod 2Z)")

    # candidate is block-diagonal starting with U by construction: manifest
    # orthogonal direct summand. By step 5's genus-uniqueness, NS ~= candidate.
    u_summand = True

    return {
        "family": family_label,
        "T": {"gram": [[int(x) for x in row] for row in T_gram.tolist()],
              "det": Tdata["det"], "signature": list(m_sig),
              "disc_group_order": order_T, "disc_form_q_mod_2Z": str(q_T)},
        "embedding_conditions": {
            "m_lt_n": True, "ell_T_plus_2_le_rk_complement": Tdata["ell"] + 2 <= bound,
            "ell_T": Tdata["ell"], "bound_rk_Lambda_minus_rk_T": bound,
        },
        "NS": {
            "rank": ns_rank, "signature": list(ns_sig),
            "disc_group_order_required": order_ns_required,
            "disc_form_q_mod_2Z_required": str(q_ns_required),
            "genus_unique": True,
        },
        "candidate": {
            "construction": f"U (+) E8(-1) (+) E8(-1) (+) <{-d}>",
            "gram": [[int(x) for x in row] for row in cand.tolist()],
            "rank": cand_rank, "signature": list(cand_sig),
            "det": cand_data["det"], "disc_group_order": order_cand,
            "disc_form_q_mod_2Z": str(sp.Rational(q_cand) % 2),
        },
        "u_summand_determination": "YES" if u_summand else "NO",
        "u_summand_reasoning": (
            f"NS is unique in its genus (rank {ns_rank}, signature {ns_sig}, "
            f"cyclic discriminant group of order {order_ns_required}, "
            f"Huybrechts Thm 1.5 bound ell+2={ell_ns+2}<=rk={ns_rank} holds). "
            f"The explicit candidate U(+)E8(-1)^2(+)<{-d}> has identical exact "
            "genus data (rank, signature, discriminant form all checked equal, "
            "not merely isomorphic-in-principle) and is block-diagonal with U "
            "as its first summand by construction. By genus uniqueness, "
            f"NS = T^perp is isometric to this candidate, hence NS contains U "
            "as an orthogonal direct summand."
        ),
    }


# ----------------------------------------------------------------------------
# CONSTRUCTIVE witness (Huybrechts Ch.14 Example 1.11(i)): exhibit T -> Lambda
# and NS = T^perp by an EXPLICIT integral basis, not just genus uniqueness.
#
# This is the primary evidence in the certificate; nikulin_complement()'s
# genus-uniqueness argument above is retained as an INDEPENDENT cross-check
# (two different proof methods agreeing on the identical Gram matrix), not
# as the sole justification. Rationale: this repo's own C2_cooper_s7_v5.json
# u1b_status field explicitly prefers an exhibited integral base change over
# a genus/one-class argument ("stronger... Cassels Ch.11 therefore not
# fetched"), and T0 separately ruled (2026-07-27, motivating v5) that a
# splitting witness must be SERIALIZED, not left implicit. A genus-only G0
# certificate would not meet the bar this repo already set for the identical
# style of claim on T itself.
#
# Construction: T's own certified splitting T ~= U + <d> (gram_after from
# check_U1_lattice.py's u_splitting, d = 2n even by the family's own
# construction — see stage0_framework's G = U + <2n>) embeds into
# Lambda = U_1 (+) U_2 (+) U_3 (+) E8(-1)^2 by
#   f -> e_{U1},  e -> f_{U1},  w -> ell := e_{U2} + n f_{U2}   (ell^2 = 2n = d)
# Since f,e span ALL of U_1 and ell lies entirely inside U_2, block-diagonality
# of Lambda gives immediately (Huybrechts Ch.14 Example 0.3, applied twice):
#   T^perp = U_1^perp cap ell^perp = (U_2 (+) U_3 (+) E8(-1)^2) cap ell^perp
#          = (U_2 cap ell^perp) (+) U_3 (+) E8(-1)^2
#          = Z*(e_{U2} - n f_{U2})  (+)  U_3  (+)  E8(-1)^2
# with (e_{U2}-n f_{U2})^2 = -2n = -d exactly (Huybrechts Ex 1.11(i)
# specialized to the K3-lattice case, d = 2n even). No genus/uniqueness
# argument is used in this derivation — every step is checked equality of
# explicit integer vectors and matrices.
# ----------------------------------------------------------------------------

def exhibit_constructive_witness(gram_after, family_label):
    """Returns a dict with the explicit embedding matrix B (T -> Lambda, in
    T's certified (f,e,w) splitting basis), the explicit NS basis matrix, and
    the resulting NS Gram — all exact integers, all independently checked."""
    ga = [[int(x) for x in row] for row in gram_after]
    chk(ga[0] == [0, 1, 0] and ga[1] == [1, 0, 0] and ga[2][0] == 0 and ga[2][1] == 0,
        f"{family_label}: gram_after {ga} is not block form U (+) <d> in "
        "(f,e,w) order — the e_U1/f_U1/ell construction below assumes it is")
    d = ga[2][2]
    chk(d % 2 == 0, f"{family_label}: d={d} is odd; the ell=e+nf construction needs d=2n even")
    n = d // 2

    Lam = k3_lattice_gram()

    # embedding matrix B: columns are f,e,w expressed in Lambda's standard
    # basis (indices 0,1 = U1; 2,3 = U2; 4,5 = U3; 6..13 = E8(-1)_a; 14..21 = E8(-1)_b)
    B = sp.zeros(22, 3)
    B[0, 0] = 1   # f -> e_{U1}  (index 0)
    B[1, 1] = 1   # e -> f_{U1}  (index 1)
    B[2, 2] = 1   # w -> ell = e_{U2} + n f_{U2}
    B[3, 2] = n

    reproduced = B.T * Lam * B
    chk(reproduced == sp.Matrix(ga),
        f"{family_label}: embedding B does not reproduce gram_after: "
        f"got {reproduced.tolist()}, expected {ga}")

    # primitivity of the embedding: gcd of all 3x3 maximal minors of B must be 1
    # (only the nonzero rows {0,1,2,3} can contribute a nonzero 3x3 minor here,
    # so it suffices to check those C(4,3)=4 minors exactly)
    from itertools import combinations
    nz_rows = [0, 1, 2, 3]
    g = sp.Integer(0)
    for r in combinations(nz_rows, 3):
        g = sp.gcd(g, B[list(r), :].det())
    chk(g == 1, f"{family_label}: embedding B is not primitive: gcd of maximal minors = {g}")

    # NS basis: e_{U2}-n f_{U2}, then all of U3 and both E8(-1) blocks verbatim
    # -- ordered to match nikulin_complement()'s candidate block order
    # U (+) E8(-1) (+) E8(-1) (+) <-d> for a literal (not just isometric) cross-check
    ns_cols = []
    for i in (4, 5):        # U3
        v = sp.zeros(22, 1); v[i, 0] = 1; ns_cols.append(v)
    for i in range(6, 14):  # E8(-1)_a
        v = sp.zeros(22, 1); v[i, 0] = 1; ns_cols.append(v)
    for i in range(14, 22):  # E8(-1)_b
        v = sp.zeros(22, 1); v[i, 0] = 1; ns_cols.append(v)
    v = sp.zeros(22, 1); v[2, 0] = 1; v[3, 0] = -n; ns_cols.append(v)  # <-d>
    NSB = sp.Matrix.hstack(*ns_cols)
    chk(NSB.shape == (22, 19), f"{family_label}: NS basis wrong shape {NSB.shape}")

    orth = B.T * Lam * NSB
    chk(orth == sp.zeros(3, 19), f"{family_label}: NS basis not orthogonal to embedded T")

    Gram_NS = NSB.T * Lam * NSB
    return {
        "d": d, "n": n,
        "embedding_matrix_B": [[int(x) for x in row] for row in B.tolist()],
        "embedding_primitive": True,
        "NS_basis_matrix": [[int(x) for x in row] for row in NSB.tolist()],
        "NS_gram_exhibited": [[int(x) for x in row] for row in Gram_NS.tolist()],
    }


# ----------------------------------------------------------------------------
# driver
# ----------------------------------------------------------------------------

def run_family_G0(family, verbose=True):
    mp.mp.dps = U1.DPS  # match check_U1_lattice.py's own precision setting
    L2, L3 = U1.load_operators(family)
    U1.cross_check_lean_provenance(family, L3)
    res = U1.run_family(family, verbose=False)
    T_gram = sp.Matrix(res["stage3"]["gram_primitive_even"])
    result = nikulin_complement(T_gram, family)

    u_splitting = res["stage3"]["u_splitting"]
    chk(u_splitting is not None, f"{family}: stage3 produced no u_splitting witness")
    witness = exhibit_constructive_witness(u_splitting["gram_after"], family)
    chk(witness["NS_gram_exhibited"] == result["candidate"]["gram"],
        f"{family}: CROSS-CHECK FAILED — the exhibited NS Gram (explicit "
        "basis, Huybrechts Ex 1.11(i) construction) does not match the "
        "genus-uniqueness candidate Gram from nikulin_complement(); the two "
        "independent methods disagree")
    result["constructive_witness"] = witness
    result["u_summand_reasoning_primary"] = (
        f"EXHIBITED (primary evidence): T's certified splitting T ~= U + <{witness['d']}> "
        f"embeds into Lambda via f->e_U1, e->f_U1, w->e_U2+{witness['n']}*f_U2 "
        "(checked primitive: gcd of maximal minors = 1); NS = T^perp is then "
        f"read off directly from Lambda's block structure as Z*(e_U2-{witness['n']}*f_U2) "
        "(+) U3 (+) E8(-1)^2, an explicit integral basis with Gram computed "
        "and checked orthogonal to the embedded T generators. This matches "
        "(literal Gram-matrix equality, not just isomorphism-in-principle) "
        "the independent genus-uniqueness argument below."
    )
    if verbose:
        print(f"=== G0 NS-genus pipeline: {family} ===")
        print(f"  T (fresh from source): det={result['T']['det']}, "
              f"signature={result['T']['signature']}, "
              f"disc group order={result['T']['disc_group_order']}")
        print(f"  embedding T->Lambda: existence+uniqueness bound "
              f"{result['embedding_conditions']['ell_T']}+2 <= "
              f"{result['embedding_conditions']['bound_rk_Lambda_minus_rk_T']}: "
              f"{result['embedding_conditions']['ell_T_plus_2_le_rk_complement']}")
        print(f"  NS = T^perp: rank={result['NS']['rank']}, "
              f"signature={result['NS']['signature']}, "
              f"required disc group order={result['NS']['disc_group_order_required']}, "
              f"required q={result['NS']['disc_form_q_mod_2Z_required']}")
        print(f"  candidate {result['candidate']['construction']}: "
              f"rank={result['candidate']['rank']}, signature={result['candidate']['signature']}, "
              f"disc order={result['candidate']['disc_group_order']}, "
              f"q={result['candidate']['disc_form_q_mod_2Z']}")
        print(f"  [cross-check] exhibited NS Gram (Ex 1.11(i) construction, "
              f"d={witness['d']}, n={witness['n']}) == genus-uniqueness candidate Gram: "
              f"{witness['NS_gram_exhibited'] == result['candidate']['gram']}")
        print(f"  MATCH: {result['u_summand_determination']}")
    return result, res


def verify_against_live_cert(res_s7, verbose=True):
    """Cross-check the freshly re-derived s7 T against the accepted LIVE
    certificate (integrity gate; does not trust the JSON as input)."""
    cert = json.loads(CERT_S7_LIVE.read_text())
    d = cert["derived"]
    lat = res_s7["stage3"]
    chk(lat["gram_primitive_even"] == d["gram_primitive_even"],
        "fresh T Gram != C2_cooper_s7_v5.json derived.gram_primitive_even")
    chk(lat["det"] == d["det"], "fresh T det != certificate det")
    chk(lat["signature"] == d["signature"], "fresh T signature != certificate signature")
    chk(lat["disc_group_elementary_divisors"] == d["disc_group_elementary_divisors"],
        "fresh T disc group != certificate disc group")
    if verbose:
        print("  [integrity] fresh re-derivation of T matches C2_cooper_s7_v5.json exactly: PASS")


def emit_certificate(result_s7, result_s10, res_s7_raw, out_path):
    cert = {
        "certificate": "G0_NS_genus_cooper_s7",
        "status": "DRAFT - pending T0 (Xavier) review. WP S2-G Phase G0 "
                  "(briefs/WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md sec.5); "
                  "phase opened by T0 2026-07-28 (decision log in that file, "
                  "commit 1dd660a).",
        "checker": "check_NS_genus_G0.py",
        "checker_version": "1.0.0",
        "date": "2026-07-28",
        "operator": "cooper_s7",
        "claim": (
            "The Neron-Severi lattice NS of the generic K3 fiber of the "
            "certified cooper_s7 family, computed as the Nikulin orthogonal "
            "complement NS = T^perp of the certified transcendental lattice "
            "T (T ~= U + <14>, C2_cooper_s7_v5.json) inside the K3 lattice "
            "Lambda = U^3 (+) E8(-1)^2, is isometric to "
            f"{result_s7['candidate']['construction']}. This is EXHIBITED, "
            "not just genus-argued: an explicit integral embedding matrix "
            "T -> Lambda and an explicit integral basis for NS = T^perp are "
            "constructed (Huybrechts Ch.14 Example 1.11(i)) and checked to "
            "reproduce this exact Gram matrix. An independent genus-"
            "uniqueness argument (existence+uniqueness of the primitive "
            "embedding, Huybrechts Thm 1.12; additivity of signature; Prop "
            "0.2(i) for the complement's discriminant form; uniqueness in "
            "genus, Thm 1.5) is carried alongside as a second, independent "
            "derivation, and the two are checked to agree on the identical "
            "Gram matrix (not merely isomorphic-in-principle)."
        ),
        "match_criterion": MATCH_CRITERION,
        "match_determination": result_s7["u_summand_determination"],
        "match_reasoning": result_s7["u_summand_reasoning_primary"],
        "match_reasoning_secondary_crosscheck": result_s7["u_summand_reasoning"],
        "caveats": [
            "WEAK DISCRIMINATING POWER OF G0, reported per plan sec.5's own "
            "framing that G0's stop condition 'can kill the plan cheaply': "
            "both cooper_s7 (d=14) and cooper_s10 (d=20) pass with a U "
            "summand. For NS of rank 19, signature (1,18), with cyclic "
            "discriminant group (ell=1) — which is what any of this family's "
            "members produce, by the family's own construction, T ~= U+<2n> "
            "-- the genus-representative construction essentially ALWAYS "
            "places a U in front (any n works in the ell=e+nf construction "
            "above). A NO here would have required an unusual disc-form "
            "obstruction that this family's T does not have. Clearing G0 is "
            "therefore weak evidence that G1 (actual fibration/resolution "
            "construction) will succeed — it rules out one specific failure "
            "mode, not the main risk the plan already flags for G1-b "
            "(crepant resolvability).",
            "FIBERWISE, NOT YET RELATIVE: this certifies that the GENERIC "
            "K3 FIBER (each member of the family, abstractly) admits an "
            "elliptic fibration with section. G1-c's actual requirement is "
            "relative — X4 elliptic over a B3 that is a P1-fibration over "
            "B2 — which needs the isotropic NS class exhibited here to be "
            "monodromy-invariant ALONG the family (plausible for an "
            "M-polarized family with constant NS, and the monodromy "
            "generators are already available from check_U1_lattice.py "
            "stage2/stage3, but NOT checked by this G0 certificate). This "
            "is the first prerequisite for G1-c, not authorized or "
            "attempted in this phase.",
        ],
        "derived": {
            "T_input": result_s7["T"],
            "K3_lattice": {"construction": "U^3 (+) E8(-1)^2", "rank": 22,
                            "signature": [3, 19], "det": -1, "even": True,
                            "unimodular": True,
                            "note": "verified computationally in this checker, "
                                    "not assumed (see e8_gram()/k3_lattice_gram())"},
            "constructive_witness": result_s7["constructive_witness"],
            "embedding_conditions": result_s7["embedding_conditions"],
            "NS_genus": result_s7["NS"],
            "candidate": result_s7["candidate"],
            "consistency_check_rho": {
                "NS_rank": result_s7["NS"]["rank"],
                "rho_E011": 19,
                "match": result_s7["NS"]["rank"] == 19,
                "note": "NS rank (from this G0 Nikulin-complement computation, "
                        "route: U1 monodromy pipeline -> T -> T^perp) equals "
                        "rho=19 (from Zarhin 1983 Thm 1.6(a), E-011, an "
                        "entirely independent derivation route) — an "
                        "unforced cross-check, not a tautology.",
            },
        },
        "how": {
            "T_source": "re-derived fresh via checkers/check_U1_lattice.py "
                        "run_family('cooper_s7') (NOT parsed from the "
                        "certificate JSON), then cross-checked bit-for-bit "
                        "against data/certificates/C2_cooper_s7_v5.json "
                        "(see verify_against_live_cert)",
            "lattice_theory": "Nikulin's theory of primitive embeddings of "
                              "even lattices into the K3 lattice, as read in "
                              "Huybrechts *Lectures on K3 Surfaces* Ch.14 "
                              "(docs/literature/huybrechts_K3Global.pdf, "
                              "hash-pinned MANIFEST.md); PRIMARY: Example "
                              "1.11(i) (explicit isotropic vector "
                              "ell=e+nf in a U summand, explicit orthogonal "
                              "complement Z(e-nf)); SECONDARY cross-check: "
                              "Thm 1.12 (embedding existence+uniqueness), "
                              "Prop 0.2 (orthogonal-complement discriminant "
                              "form), Thm 1.5 (genus uniqueness)",
            "arithmetic": "exact sympy Integer/Rational throughout; Smith "
                          "normal form for discriminant groups; exact "
                          "real-root-count characteristic-polynomial "
                          "signature; Sylvester-criterion positive-"
                          "definiteness for E8 — no floating point, no "
                          "numerical tolerance anywhere in this file",
        },
        "controls": {
            "different_level_cooper_s10": {
                "T_det": result_s10["T"]["det"],
                "NS_disc_group_order": result_s10["NS"]["disc_group_order_required"],
                "candidate": result_s10["candidate"]["construction"],
                "u_summand_determination": result_s10["u_summand_determination"],
                "discriminates": (result_s10["T"]["det"] != result_s7["T"]["det"]
                                    and result_s10["NS"]["disc_group_order_required"]
                                    != result_s7["NS"]["disc_group_order_required"]),
                "note": "identical pipeline on cooper_s10 (T ~= U+<20>) must "
                        "produce a numerically DIFFERENT NS genus than s7's "
                        "(T~=U+<14>); both currently answer YES on the "
                        "U-summand question but for numerically distinct "
                        "reasons (d=20 vs d=14) — this is the G0-row "
                        "regression control, NOT a claim that the two "
                        "answers must differ",
            },
            "negative_controls": "checkers/test_NS_genus_G0_controls.py: "
                                 "(a) perturbed candidate twist <-d+1> must "
                                 "fail the disc-form match loudly; "
                                 "(b) non-cyclic-disc-group guard "
                                 "(cyclic_disc_form) must fail loudly on a "
                                 "fabricated rank-2 discriminant group; "
                                 "(c) cross-family discrimination re-asserted "
                                 "standalone",
        },
        "tier": "B",
        "tier_reason": (
            "DEVIATION FROM THE REQUESTING BRIEF, stated explicitly: the "
            "task brief allowed 'Tier (E), exact lattice arithmetic, if the "
            "derivation is airtight' for this deliverable. The derivation "
            "IS airtight and exact (steps 3-6 of the module docstring, plus "
            "the constructive witness above: no floats, no numerical "
            "tolerance, every step a cited theorem or explicit checked "
            "matrix identity) — but the certificate's OVERALL claim still "
            "inherits Tier B, not E/A, because it is a claim about T, and T "
            "itself is Tier B at its source: the identification of T with "
            "the actual transcendental lattice of the cooper_s7 family "
            "(C2_cooper_s7_v5.json) rests on monodromy entries recognized "
            "numerically with a loud 1e-35 tolerance gate, and cites read "
            "framework theorems rather than a kernel proof. A claim cannot "
            "be more certain than its input; this certificate does not "
            "upgrade T's tier, it only adds an exact derivation on top of "
            "it. If T's own tier is ever upgraded, this certificate's "
            "lattice-arithmetic content is already exact and would inherit "
            "the upgrade without rework."
        ),
        "not_claimed": [
            "no Kodaira fibre types (E-007/E-008/E-009 stand)",
            "no physical coupling of any kind (VISION sec 1.3)",
            "no CY condition, resolution analysis, or elliptic-fibration "
            "CONSTRUCTION for X4 (that is G1, not authorized by this phase)",
            "no observable of any kind (m_phi, alpha_D, Lambda_D) — F5b stands",
            "no claim that NS(X) is projective-ample-generated or that the "
            "resulting genus-one fibration is actually realized on the "
            "family's K3 surfaces beyond the abstract-lattice statement "
            "(surjectivity of the period map / very-ampleness questions are "
            "out of scope for G0)",
        ],
        "refs_sha256": {
            "recurrences_v1.json": hashlib.sha256((REPO / "refs" / "recurrences_v1.json").read_bytes()).hexdigest(),
            "huybrechts_K3Global.pdf": hashlib.sha256(HUYBRECHTS_PDF.read_bytes()).hexdigest()
            if HUYBRECHTS_PDF.exists() else "FILE_NOT_FOUND_AT_CHECK_TIME",
        },
        "provenance": "Generated-by: Sonnet 5 (Stream 2, WP S2-G Phase G0 "
                      "session 2026-07-28) | Verified-by: check_NS_genus_G0.py "
                      "structural assertions + checkers/test_NS_genus_G0_controls.py "
                      "| Reviewed-by: pending T0 (Xavier) — per plan sec.5 "
                      "footer, coordinator reviews and commits, no agent commits",
    }
    out_path.write_text(json.dumps(cert, indent=2))
    print(f"\nWrote {out_path.relative_to(REPO)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-cert", action="store_true")
    ap.add_argument("--out", default=str(REPO / "data" / "certificates" / "G0_NS_genus_cooper_s7.json"))
    args = ap.parse_args()

    try:
        result_s7, res_s7_raw = run_family_G0("cooper_s7")
        verify_against_live_cert(res_s7_raw)
        result_s10, _ = run_family_G0("cooper_s10")

        chk(result_s7["T"]["det"] != result_s10["T"]["det"],
            "cross-family control FAILED: s7 and s10 T dets coincide")
        chk(result_s7["NS"]["disc_group_order_required"] != result_s10["NS"]["disc_group_order_required"],
            "cross-family control FAILED: s7 and s10 NS disc-group orders coincide")
        print("\n[control] different-level cross-family check: s7 and s10 "
              "produce numerically distinct NS genus data: PASS")

        print(f"\n=== G0 DETERMINATION (cooper_s7): {result_s7['u_summand_determination']} ===")
        print(result_s7["u_summand_reasoning_primary"])
        print(f"\n[secondary cross-check, genus-uniqueness]\n{result_s7['u_summand_reasoning']}")

        if args.emit_cert:
            emit_certificate(result_s7, result_s10, res_s7_raw, Path(args.out))

        print("\ncheck_NS_genus_G0.py: all structural assertions passed")
        return 0
    except ControlFailure as e:
        print(f"\nFAIL / STOP CONDITION: {e}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
