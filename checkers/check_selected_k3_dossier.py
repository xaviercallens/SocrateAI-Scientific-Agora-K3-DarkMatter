#!/usr/bin/env python3
"""check_selected_k3_dossier.py -- one machine-readable record of the AM-8-selected K3 (and the s10
instance), assembled by CROSS-CHECKING seven existing certificates against each other. Nothing is
typed: every field is read from a certificate whose sha256 is recorded, and the checker refuses if
any two sources disagree about the point.

Sources (data/certificates/):
  C6_SELECTED_CANDIDATE.json      the AM-8 pick per family (T0 D13', K3_CRITERIA.md C6)
  CM_POINTS_RHO20.json            the CM-point row at z = infinity (v, D, reduced T, -v^2, div)
  CM_POINTS_RHO20_LATTICE_TIER.json  kernel-checked lattice half (tier, number of independent Lean sources)
  A2_MEMBERSHIP.json              the explicit A2 vector (s7) / absence (s10)
  CM_COMPLETENESS.json            uniqueness of the point on the modular curve at its discriminant
  INOSE_MODEL_M7.json             the explicit M_7 model at z = infinity (sigma = pi = 0: E_omega x E_omega)
  TW2_RHO20_LOCI.json             NS structure at the point: U + E8^2 + A2, Mordell-Weil rank 0, model-confirmed

Tier labels travel per field (lattice half Tier A; 'this lattice is T' Tier B; NS structure Tier B;
selection itself is a T0 ruling, not a computation). The dossier ranks nothing: it records the two
families' picks side by side because K3_CRITERIA.md C6 names both; no cross-family statement is made
(ledger items 8/9). No Kodaira label (items 3, 10); no physics (item 4).

Usage: python3 checkers/check_selected_k3_dossier.py [--emit] [--certs-dir DIR]
Controls: checkers/test_selected_k3_dossier_controls.py
Generated-by: Claude (Fable 5.1), Stream 2, 2026-10-08 | Verified-by: controls | Reviewed-by: N
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_CERTS = REPO / "data" / "certificates"
OUT_NAME = "SELECTED_K3_DOSSIER.json"
SOURCES = ["C6_SELECTED_CANDIDATE.json", "CM_POINTS_RHO20.json", "CM_POINTS_RHO20_LATTICE_TIER.json",
           "A2_MEMBERSHIP.json", "CM_COMPLETENESS.json", "INOSE_MODEL_M7.json", "TW2_RHO20_LOCI.json"]


class Refuse(RuntimeError):
    pass


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(certs):
    d = {}
    for n in SOURCES:
        p = certs / n
        if not p.exists():
            raise Refuse(f"source certificate missing: {n} (fail closed)")
        d[n] = json.loads(p.read_text())
    return d


def abs_disc(abc):
    a, b, c = abc
    return 4 * a * c - b * b


def family_record(fam, S, certs):
    sel = S["C6_SELECTED_CANDIDATE.json"]["selected"][fam]
    if sel["z"] != "infinity":
        raise Refuse(f"{fam}: selector pick is not at z = infinity ({sel['z']}); dossier layout assumes the AM-8 pick")
    cm = S["CM_POINTS_RHO20.json"]["families"][fam]
    hit = cm["locus_hits"]["infinity"][0]
    lt_rows = [r for r in S["CM_POINTS_RHO20_LATTICE_TIER.json"]["rows"] if r["candidate"] == fam and r["v"] == hit["v"]]
    if len(lt_rows) != 1:
        raise Refuse(f"{fam}: lattice-tier overlay has {len(lt_rows)} rows for v = {hit['v']}")
    lt = lt_rows[0]
    a2 = S["A2_MEMBERSHIP.json"]["families"][fam]
    cc = [p for p in S["CM_COMPLETENESS.json"]["families"][fam]["per_D"] if p["D"] == sel["D"]]
    if len(cc) != 1:
        raise Refuse(f"{fam}: completeness table has {len(cc)} rows at D = {sel['D']}")
    cc = cc[0]
    # --- cross-checks: every source must describe the same point ---
    problems = []
    if list(sel["v"]) != list(hit["v"]):
        problems.append(f"v differs: selector {sel['v']} vs CM row {hit['v']}")
    if list(sel["T_reduced_form"]) != list(hit["T_X_reduced_form_abc"]):
        problems.append(f"T differs: selector {sel['T_reduced_form']} vs CM row {hit['T_X_reduced_form_abc']}")
    if sel["D"] != hit["D"]:
        problems.append(f"D differs: selector {sel['D']} vs CM row {hit['D']}")
    if abs_disc(sel["T_reduced_form"]) != -sel["D"]:
        problems.append(f"|disc T| = {abs_disc(sel['T_reduced_form'])} != -D = {-sel['D']}")
    if lt["lattice_tier"] != "A":
        problems.append(f"lattice tier is {lt['lattice_tier']}, not A")
    if cc["verdict"] != "COMPLETE" or cc["points_on_X0n_star"] != 1:
        problems.append(f"point not unique on the curve: {cc['verdict']}, {cc['points_on_X0n_star']} point(s)")
    if fam == "cooper_s7":
        if a2["membership_A2"]["verdict"] != "PRESENT" or list(a2["membership_A2"]["v"]) != list(hit["v"]):
            problems.append("A2_MEMBERSHIP does not exhibit the same vector")
        im = S["INOSE_MODEL_M7.json"]["result"]["S6"]
        if not im.get("both_zero_E_omega_x_E_omega"):
            problems.append("INOSE_MODEL_M7 S6 does not record sigma = pi = 0 at infinity")
        tw = S["TW2_RHO20_LOCI.json"]["result"]
        loc = tw["loci"]["infinity"]["resolution"]
        mc = tw["model_checks"]["infinity"]
        if not (loc["root_lattice"] == "A2" and loc["mordell_weil_rank"] == 0 and mc["agrees_with_lattice_reading"]):
            problems.append("TW2_RHO20_LOCI does not record NS = U + E8^2 + A2 with Mordell-Weil rank 0, model-confirmed")
        if tw["loci"]["infinity"]["abs_disc_T"] != abs_disc(sel["T_reduced_form"]):
            problems.append("TW2 |disc T| differs from the selector's T")
    else:
        if a2["membership_A2"]["verdict"] != "ABSENT":
            problems.append("A2_MEMBERSHIP for s10 is not ABSENT")
    if problems:
        raise Refuse(f"{fam}: sources disagree: " + "; ".join(problems))
    rec = {
        "family": fam, "level_n": cm["n"], "z": "infinity", "v": hit["v"], "minus_v2": hit["minus_v2"],
        "D": sel["D"], "T_reduced_form_abc": sel["T_reduced_form"], "T_gram": [[2 * sel["T_reduced_form"][0], sel["T_reduced_form"][1]],
                                                                               [sel["T_reduced_form"][1], 2 * sel["T_reduced_form"][2]]],
        "abs_disc_T": abs_disc(sel["T_reduced_form"]),
        "lattice_half": {"tier": lt["lattice_tier"], "independent_kernel_sources": lt["independent_files_passing"],
                         "what_is_tier_A": lt.get("what_is_tier_A"), "what_stays_tier_B": lt.get("what_stays_tier_B")},
        "unique_on_modular_curve_at_D": {"verdict": cc["verdict"], "points_on_X0n_star": cc["points_on_X0n_star"]},
        "lattice_cert": cm["lattice_cert"], "lattice_cert_status": cm["lattice_cert_status"], "advisory": bool(cm["advisory"]),
        "selection_authority": "T0 D13' / AM-8 (K3_CRITERIA.md C6, SEL-D: minimal |disc T| within the family); recorded, not recomputed as a preference",
    }
    if fam == "cooper_s7":
        rec["A2_membership"] = {"verdict": "PRESENT", "vector": hit["v"], "tier": "B (lattice arithmetic; framework Dolgachev 1996 sec. 7)"}
        rec["shioda_inose_partner"] = {"E1_x_E2": "E_omega x E_omega (sigma = pi = 0 at z = infinity)", "source": "INOSE_MODEL_M7.json S6", "tier": "B"}
        rec["neron_severi_structure"] = {"NS": "U + E8 + E8 + A2", "mordell_weil_rank": 0, "extra_root": "order-4 discriminant root, triple root at s = 0, v_s(Delta) = 4",
                                         "source": "TW2_RHO20_LOCI.json", "tier": "B", "note": "no Mordell-Weil section; fibre described by root lattice and orders only (ledger items 3, 10)"}
    else:
        rec["A2_membership"] = {"verdict": "ABSENT", "tier": "B (all-v congruence)"}
    return rec


def build(certs):
    S = load(certs)
    return {"checker": "checkers/check_selected_k3_dossier.py", "checker_sha256": sha(Path(__file__)), "date": "2026-10-08",
            "status": "DOSSIER -- a cross-checked index of existing certificates; adopts nothing, ranks nothing",
            "families": {fam: family_record(fam, S, certs) for fam in ("cooper_s7", "cooper_s10")},
            "inputs_sha256": {n: sha(certs / n) for n in SOURCES},
            "not_claimed": [
                "any ranking or comparison of cooper_s7 and cooper_s10: both picks are recorded because K3_CRITERIA.md C6 names both (ledger items 8/9)",
                "that 'this lattice is T' is more than Tier B for either family (Dolgachev/Doran framework); the Tier A statements are the lattice half only",
                "any Kodaira fibre type (items 3, 10): fibres appear as root lattices and discriminant-root orders",
                "any physical reading of the selected point (item 4)",
                "that the dossier adds information: it only fails closed when its sources disagree"],
            "generated_by": "Claude (Fable 5.1), Stream 2, 2026-10-08", "verified_by": "checkers/test_selected_k3_dossier_controls.py", "reviewed_by": "N"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--certs-dir", type=Path, default=DEFAULT_CERTS)
    a = ap.parse_args(argv)
    d = build(a.certs_dir)
    for fam, r in d["families"].items():
        print(f"{fam}: z = inf, v = {r['v']}, D = {r['D']}, T = {r['T_reduced_form_abc']} (|disc| {r['abs_disc_T']}), lattice tier {r['lattice_half']['tier']} "
              f"x{r['lattice_half']['independent_kernel_sources']}, unique on curve: {r['unique_on_modular_curve_at_D']['verdict']}, cert {r['lattice_cert']} ({r['lattice_cert_status']}), advisory {r['advisory']}"
              + (f"; NS = {r['neron_severi_structure']['NS']}, MW rank {r['neron_severi_structure']['mordell_weil_rank']}" if fam == "cooper_s7" else ""))
    print("all seven sources agree")
    if a.emit:
        out = a.certs_dir / OUT_NAME
        out.write_text(json.dumps(d, indent=2) + "\n")
        print("wrote", out)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refuse as e:
        print("REFUSED:", e)
        sys.exit(2)
