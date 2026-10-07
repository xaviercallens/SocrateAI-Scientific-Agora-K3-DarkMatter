#!/usr/bin/env python3
"""check_TW2_height_condition.py -- WP-TW2 step 0: the lattice constraint an M_n-polarized
elliptic K3 with two E8-root fibres imposes on its Mordell-Weil generator.

Opened by D20' (briefs/T0_DECISIONS_2026_10_07_STREAM2_DELEGATED.md) as the first constraint any
twisted-Weierstrass construction must meet. Everything below is exact lattice arithmetic from a
fetched-and-read source (Schuett-Shioda, arXiv:0907.0298, docs/literature/MANIFEST.md addendum
2026-10-07): Shioda-Tate (Cor. 6.13), the height formula (Thm 11.5),
    h(P) = 2 chi(S) + 2 P.O - sum_v contr_v(P),
and disc(NS) = -disc(T_triv) * h(P) at Mordell-Weil rank 1 (eq. 23).

INPUTS (all computed or read, none typed as a result):
  chi(O_K3) = 1 - h^{0,1} + h^{0,2} = 2 (K3 Hodge numbers);
  E8: rank and determinant computed from its Cartan matrix (rank 8, det 1);
  U: det -1 (hyperbolic plane);
  the target M_n = U + E8 + E8 + <-2n> (Dolgachev 1996 sec. 7, pinned), |disc| = 2n;
  the number of E8-root fibres is cross-checked against INOSE_FIBRATION_MULTIPLICITIES.json
  (the two discriminant roots of order 10 in the Kuwata-Shioda fibration of the explicit M_7 model).

RESULT: with two E8-root fibres (each contributes m_v - 1 = 8 to the trivial lattice) and rho = 19,
Shioda-Tate forces rank E(K) = 1; NS = U + E8^2 + <-h(P)>, and NS = M_n forces h(P) = 2n. Fibres
of E8 root type have a unique simple component, so contr = 0 and
    P.O = (2n - 2 chi)/2 = n - chi = n - 2       (n = 7: P.O = 5;  n = 10: P.O = 8).
Any Weierstrass model realizing the M_n-polarization with two E8-root fibres must carry a section
meeting the zero section with intersection number n - 2. This is lattice / Tate-order language only;
no Kodaira label is attached to anything (ledger items 3, 10).

NOT CLAIMED: that such a section exists on any particular base (that is WP-TW2 proper); anything
physical (item 4); anything about cooper_s10's geometry beyond its use as the n = 10 instance.

Usage: python3 checkers/check_TW2_height_condition.py [--emit]
Controls: checkers/test_TW2_height_condition_controls.py

Generated-by: Claude (Fable 5.1), Stream 2, 2026-10-07 | Verified-by: controls; source lines cited
in docs/literature/MANIFEST.md | Reviewed-by: N
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parent.parent
CERT = REPO / "data" / "certificates" / "TW2_HEIGHT_CONDITION.json"
INOSE_FIB = REPO / "data" / "certificates" / "INOSE_FIBRATION_MULTIPLICITIES.json"

E8_CARTAN = sp.Matrix([
    [2, -1, 0, 0, 0, 0, 0, 0],
    [-1, 2, -1, 0, 0, 0, 0, 0],
    [0, -1, 2, -1, 0, 0, 0, -1],
    [0, 0, -1, 2, -1, 0, 0, 0],
    [0, 0, 0, -1, 2, -1, 0, 0],
    [0, 0, 0, 0, -1, 2, -1, 0],
    [0, 0, 0, 0, 0, -1, 2, 0],
    [0, 0, -1, 0, 0, 0, 0, 2],
])
U_GRAM = sp.Matrix([[0, 1], [1, 0]])

# fibre types by root lattice: (rank of root lattice = m_v - 1, number of simple components).
# A section meets a simple component; the correction term is 0 iff it meets the identity component,
# which is forced when the fibre has a unique simple component (Table 4 has no entry for it).
FIBRE_TYPES = {
    "E8": {"root_rank": int(E8_CARTAN.rank()), "root_det": int(E8_CARTAN.det()), "simple_components": 1,
           "nonidentity_contr": None},
    "E7": {"root_rank": 7, "root_det": 2, "simple_components": 2, "nonidentity_contr": Fr(3, 2)},  # Table 4, III*
    "E6": {"root_rank": 6, "root_det": 3, "simple_components": 3, "nonidentity_contr": Fr(4, 3)},  # Table 4, IV*
}


class Refuse(RuntimeError):
    pass


def chi_K3(h01=0, h02=1):
    return 1 - h01 + h02


def height_condition(n, fibres=("E8", "E8"), chi=None, rho=19, meets_nonidentity=()):
    """Return the exact constraint on P.O for NS = M_n given the fibre configuration."""
    chi = chi_K3() if chi is None else chi
    triv_rank = 2 + sum(FIBRE_TYPES[f]["root_rank"] for f in fibres)
    mw_rank = rho - triv_rank
    if mw_rank < 0:
        raise Refuse(f"rho = {rho} below the trivial-lattice rank {triv_rank}")
    disc_triv = int(U_GRAM.det()) * sp.prod([FIBRE_TYPES[f]["root_det"] for f in fibres])
    out = {"n": n, "chi": chi, "fibres": list(fibres), "trivial_lattice_rank": triv_rank, "mordell_weil_rank": mw_rank,
           "disc_trivial_lattice": int(disc_triv), "target_abs_disc_NS": 2 * n}
    if mw_rank != 1:
        out["ns_is_M_n_shape"] = False
        out["note"] = "NS = U + roots + <-h> needs Mordell-Weil rank exactly 1; this configuration does not give it"
        return out
    # eq. (23): disc NS = -disc(T_triv) * h(P); M_n has |disc| = 2n and the root part must be E8+E8 (det 1)
    if any(f != "E8" for f in fibres):
        out["ns_is_M_n_shape"] = False
        out["note"] = "root lattice of the fibres is not E8+E8, so NS cannot be U+E8^2+<-2n>"
        return out
    h = Fr(2 * n) / Fr(-disc_triv)          # |disc NS| = 2n  =>  h(P) = 2n / (-disc T_triv) = 2n
    contr = sum((FIBRE_TYPES[f]["nonidentity_contr"] or Fr(0)) for f in meets_nonidentity)
    two_PO = h - 2 * chi + contr            # from h = 2chi + 2 P.O - contr
    if two_PO.denominator != 1 or two_PO % 2 != 0:
        raise Refuse(f"2*P.O = {two_PO} is not an even integer: no section with these fibre contacts realizes h(P) = {h}")
    out.update({"ns_is_M_n_shape": True, "height_h_P": int(h), "sum_contr": str(contr), "P_dot_O": int(two_PO // 2),
                "formula": "h(P) = 2chi + 2 P.O - sum contr_v(P)  (Schuett-Shioda Thm 11.5); |disc NS| = -disc(T_triv) h(P) (eq. 23)"})
    return out


def e8_fibre_count_from_inose_certificate():
    if not INOSE_FIB.exists():
        return None
    d = json.loads(INOSE_FIB.read_text())["result"]
    counts = {}
    for loc, row in d["T5_s7_loci"].items():
        orders = row["orders"]   # {"s=+1": 10, "s=-1": 10, "s=0": 2, "roots_of_e(s^2)": [1, 1], "s=infinity": 0}
        flat = []
        for v in orders.values():
            flat.extend(v if isinstance(v, list) else [v])
        counts[loc] = sum(1 for o in flat if o == 10)
    return counts


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    res = {"cooper_s7_n7": height_condition(7), "cooper_s10_n10_as_instance": height_condition(10),
           "general": {"P_dot_O": "n - chi = n - 2", "h_P": "2n"},
           "e8_root_fibres_in_explicit_M7_model_by_locus": e8_fibre_count_from_inose_certificate(),
           "step1_literature_cross_check": {
               "statement": "MWL(F(1)) = Hom(E1, E2)<2>: the section attached to an isogeny phi has height 2 deg(phi)",
               "sources_read": ["Kumar-Kuwata arXiv:1409.2931 Prop. 3.1 (citing Shioda), hypothesis E1 not isomorphic to E2; Prop. 3.2 explicit construction, height 2d",
                                "Shioda, MPIM 2007-137 / JMSJ 60 (2008): norm 2 deg(phi) on the Inose surface, deg(phi) on the Kummer surface"],
               "consequence": "a 7-isogeny gives h(P) = 14 = 2n, hence P.O = 5 -- the same number as the lattice derivation above, from an independent route",
               "caveat": "Prop. 3.1 assumes E1 not isomorphic to E2; the A2 point (j = 0, E1 = E2) is outside its hypothesis; the class-number-1 CM loci are the natural place for an explicit construction (WP-TW2 step 2, not executed)"}}
    for k in ("cooper_s7_n7", "cooper_s10_n10_as_instance"):
        r = res[k]
        print(f"{k}: trivial rank {r['trivial_lattice_rank']}, MW rank {r['mordell_weil_rank']}, h(P) = {r.get('height_h_P')}, P.O = {r.get('P_dot_O')}")
    print("E8-root fibres (order-10 discriminant roots) in the explicit M_7 model, per locus:", res["e8_root_fibres_in_explicit_M7_model_by_locus"])
    ok = res["cooper_s7_n7"]["P_dot_O"] == 5 and all(v == 2 for v in (res["e8_root_fibres_in_explicit_M7_model_by_locus"] or {}).values())
    print("CONSISTENT" if ok else "INCONSISTENT")
    if a.emit and ok:
        cert = {"checker": "checkers/check_TW2_height_condition.py",
                "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "work_package": "WP-TW2 step 0 (opened by D20', 2026-10-07)",
                "tier": "B (exact lattice arithmetic; Shioda-Tate and height formula from Schuett-Shioda, fetched and read; M_n from Dolgachev, pinned)",
                "result": res,
                "not_claimed": [
                    "that a section with P.O = n - 2 exists on any particular base or model: this is the constraint, not its realization (WP-TW2 proper)",
                    "any Kodaira fibre type anywhere (ledger items 3, 10): fibres are named by their root lattice and discriminant order only",
                    "anything about cooper_s10 beyond its use as the n = 10 instance of the same formula",
                    "any physical statement (ledger item 4)"],
                "generated_by": "Claude (Fable 5.1), Stream 2, 2026-10-07", "verified_by": "checkers/test_TW2_height_condition_controls.py", "reviewed_by": "N"}
        CERT.write_text(json.dumps(cert, indent=2) + "\n")
        print("wrote", CERT)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
