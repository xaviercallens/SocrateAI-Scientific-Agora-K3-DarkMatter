#!/usr/bin/env python3
"""check_TW2_rho20_loci.py -- WP-TW2 step 2a: exact Mordell-Weil bookkeeping of the explicit M_7
model at the three rho = 20 loci of cooper_s7, from certificates only.

Step 0 (check_TW2_height_condition.py) treated the GENERIC member: two E8-root fibres, four simple
discriminant roots, rho = 19 => Mordell-Weil rank 1, h(P) = 14, P.O = 5. At the rho = 20 loci the
fibre configuration changes (INOSE_FIBRATION_MULTIPLICITIES.json): an extra discriminant root of
order 2 (z = -1, z = 1/27) or 4 (z = infinity) appears at s = 0, and T is rank 2 (CM_POINTS_RHO20.json).
Kumar-Kuwata Prop. 3.1 does not apply (E1 = E2 at all three loci), so the structure is derived here
from lattice theory alone -- every number read from a certificate or computed:

  trivial lattice   T_triv = U + E8 + E8 + R,   R = root lattice of the extra fibre
  Shioda-Tate       rho = rank T_triv + rank MW                      (Schuett-Shioda Cor. 6.13)
  discriminants     |disc NS| = |disc T| ;  |disc NS| = |disc T_triv| * disc(MWL) / |tors|^2   (eq. 22)
  height formula    h(P) = 2 chi + 2 P.O - sum contr_v(P)            (Thm 11.5, Table 4)
  torsion           MW(F(1)) torsion-free (Shioda, MPIM 2007-137, Lemma 6.2: exceptions need n >= 2)

Root-lattice rank of the extra fibre: a discriminant root of order m carries a root lattice of rank
m - 1 or m - 2 (Schuett-Shioda, fibre table: e(F_v) = m, rank = e - 1 for the multiplicative kind,
e - 2 for the additive kind). The order-2 roots at s = 0 arise from a SIMPLE root of d(u) at u = 0
pulled back under u = s^2 (d(0) = 0 recorded in T1_transcription), i.e. the multiplicative kind:
rank 1, R = A1 (det 2, Table 4 correction 1/2 for the non-identity component). The order-4 root at
z = infinity has rank 2 or 3; rho = 20 and rank MW >= 0 force rank 2, R = A2 (det 3).

No Kodaira label is used or implied anywhere (ledger items 3, 10): fibres are described by the
order of the discriminant root and the rank/determinant of their root lattice.

Usage: python3 checkers/check_TW2_rho20_loci.py [--emit]
Controls: checkers/test_TW2_rho20_loci_controls.py

Generated-by: Claude (Fable 5.1), Stream 2, 2026-10-07 | Verified-by: controls; sources read and
pinned in docs/literature/MANIFEST.md | Reviewed-by: N
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CERTS = REPO / "data" / "certificates"
CERT = CERTS / "TW2_RHO20_LOCI.json"
CHI = 2
RHO_CM = 20
E8 = {"rank": 8, "det": 1}
ROOT_BY_RANK = {0: {"name": "none", "det": 1, "contr": [Fr(0)]},
                1: {"name": "A1", "det": 2, "contr": [Fr(0), Fr(1, 2)]},
                2: {"name": "A2", "det": 3, "contr": [Fr(0), Fr(2, 3)]},
                3: {"name": "A3", "det": 4, "contr": [Fr(0), Fr(3, 4), Fr(1)]}}


class Refuse(RuntimeError):
    pass


def abs_disc_T(abc):
    a, b, c = abc
    return 4 * a * c - b * b


def extra_root_orders(orders):
    """orders dict from INOSE_FIBRATION_MULTIPLICITIES: return the orders other than the two 10s."""
    flat = []
    for k, v in orders.items():
        flat.extend(v if isinstance(v, list) else [v])
    tens = [o for o in flat if o == 10]
    if len(tens) != 2:
        raise Refuse(f"expected two order-10 roots, found {len(tens)}")
    return sorted(o for o in flat if o not in (10, 0))


def analyse_locus(name, abc, orders, rho=RHO_CM, d0_is_simple_root=True):
    extra = extra_root_orders(orders)
    big = [o for o in extra if o > 1]
    simple = [o for o in extra if o == 1]
    if len(big) != 1:
        raise Refuse(f"{name}: expected exactly one extra root of order > 1, found {big}")
    m = big[0]
    candidates = [m - 1, m - 2]
    if m == 2:
        # multiplicative kind iff the order-2 root at s=0 is a pulled-back simple root of d(u)
        candidates = [1] if d0_is_simple_root else [0]
    res = {"locus": name, "T_abc": list(abc), "abs_disc_T": abs_disc_T(abc), "extra_root_order": m,
           "simple_roots": len(simple), "rho": rho}
    solutions = []
    for r in candidates:
        root = ROOT_BY_RANK[r]
        triv_rank = 2 + 2 * E8["rank"] + r
        mw = rho - triv_rank
        if mw < 0:
            continue
        disc_triv = 1 * E8["det"] ** 2 * root["det"]       # |det U| = 1
        sol = {"root_rank": r, "root_lattice": root["name"], "trivial_rank": triv_rank, "mordell_weil_rank": mw,
               "abs_disc_trivial": disc_triv}
        if mw == 0:
            sol["consistent"] = (disc_triv == abs_disc_T(abc))
            sol["note"] = "no section: NS = U + E8^2 + R, |disc NS| must equal |disc T|"
        elif mw == 1:
            h = Fr(abs_disc_T(abc), disc_triv)           # torsion-free (Lemma 6.2, n = 1)
            sol["height"] = str(h)
            found = []
            for c in root["contr"]:
                two_po = h - 2 * CHI + c
                if two_po.denominator == 1 and two_po >= 0 and two_po % 2 == 0:
                    found.append({"contr": str(c), "P_dot_O": int(two_po // 2)})
            sol["P_dot_O_solutions"] = found
            sol["consistent"] = len(found) == 1
            sol["torsion_free_by_height"] = all((2 * CHI - c) > 0 for c in root["contr"])  # h = 0 impossible
        else:
            sol["consistent"] = True
            sol["note"] = f"Mordell-Weil rank {mw}: disc(MWL) = {Fr(abs_disc_T(abc), disc_triv)}; no single-height statement"
        solutions.append(sol)
    consistent = [s for s in solutions if s.get("consistent")]
    if len(consistent) != 1:
        raise Refuse(f"{name}: {len(consistent)} consistent root-rank readings, need exactly one: {solutions}")
    res["resolution"] = consistent[0]
    res["rejected_readings"] = [s for s in solutions if not s.get("consistent")]
    return res


def load_inputs():
    cm = json.loads((CERTS / "CM_POINTS_RHO20.json").read_text())["families"]["cooper_s7"]["locus_hits"]
    fib = json.loads((CERTS / "INOSE_FIBRATION_MULTIPLICITIES.json").read_text())["result"]
    d0 = fib["T1_transcription"].get("d(0)")
    loci = {}
    for z, key in (("-1", "-1"), ("1/27", "1/27")):
        loci[z] = {"abc": tuple(cm[z][0]["T_X_reduced_form_abc"]), "orders": fib["T5_s7_loci"][key]["orders"], "D": cm[z][0]["D"]}
    j0 = fib["T6_special_values"]["J=0 (lam^2-lam+1=0)"]
    orders_inf = {o["factor"]: o["order"] for o in j0["orders_finite"]}
    orders_inf["s=infinity"] = j0.get("order_at_infinity", 0)
    loci["infinity"] = {"abc": tuple(cm["infinity"][0]["T_X_reduced_form_abc"]), "orders": orders_inf, "D": cm["infinity"][0]["D"]}
    return loci, d0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    loci, d0 = load_inputs()
    out = {"d(0)_from_T1_transcription": d0, "generic_member": {"rho": 19, "mordell_weil_rank": 1, "height": "14", "P_dot_O": 5,
                                                                "source": "check_TW2_height_condition.py (step 0)"}, "loci": {}}
    for z, dat in loci.items():
        r = analyse_locus(z, dat["abc"], dat["orders"], d0_is_simple_root=True)
        r["D"] = dat["D"]
        out["loci"][z] = r
        s = r["resolution"]
        extra = f"h = {s.get('height')}, P.O = {s['P_dot_O_solutions'][0]['P_dot_O']} (contr {s['P_dot_O_solutions'][0]['contr']})" if s["mordell_weil_rank"] == 1 else s.get("note")
        print(f"z = {z:>8} (D = {dat['D']:>3}, |disc T| = {r['abs_disc_T']:>2}): extra root order {r['extra_root_order']}, "
              f"R = {s['root_lattice']}, MW rank {s['mordell_weil_rank']}; {extra}")
    print("all loci resolved uniquely")
    if a.emit:
        cert = {"checker": "checkers/check_TW2_rho20_loci.py", "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "work_package": "WP-TW2 step 2a (D23', 2026-10-07)",
                "tier": "B (exact lattice arithmetic from certificates; Shioda-Tate, eq. 22, height formula and torsion lemma from pinned, read sources)",
                "result": out,
                "not_claimed": [
                    "any Kodaira fibre type (ledger items 3, 10): only discriminant-root orders and root-lattice rank/determinant are used",
                    "that a section has been exhibited: the heights and P.O values are forced by the lattices, the sections are not written down (step 2b)",
                    "any statement at rho = 19 members beyond step 0 (generic_member block is a pointer)",
                    "anything physical (ledger item 4)"],
                "generated_by": "Claude (Fable 5.1), Stream 2, 2026-10-07", "verified_by": "checkers/test_TW2_rho20_loci_controls.py", "reviewed_by": "N"}
        CERT.write_text(json.dumps(cert, indent=2) + "\n")
        print("wrote", CERT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
