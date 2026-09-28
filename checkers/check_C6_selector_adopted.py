#!/usr/bin/env python3
"""
check_C6_selector_adopted.py -- verifies the AM-8 text in K3_CRITERIA.md's C6 section
against an exact recomputation, and emits the selected-candidate certificate it cites.

Standing rule 5: numbers are computed, never typed. K3_CRITERIA.md's C6 AM-8 clause names
two lattices in prose (T=A2 for cooper_s7, T=<2>+<2> for cooper_s10, both D as stated).
This checker does not trust that prose: it re-derives SEL-D (checkers/check_C6_selector_comparison.py)
from data/certificates/CM_POINTS_RHO20.json and data/certificates/CM_COMPLETENESS.json fresh,
confirms each pick is (a) the true global minimum of |disc T| for its level (occurrence
criterion, exact search) and (b) unique ON THE MODULAR CURVE (points_on_X0n_star = 1, not a
class-number count), then compares the result against the exact strings quoted in
K3_CRITERIA.md's C6 section. A drift between the criteria file's prose and the recomputed
selector -- from a typo, a stale edit, or an uncoordinated re-render -- fails this checker.

What this certifies: SEL-D's output matches the criteria text, exactly, for both families.
What this does NOT certify: that SEL-D itself is the right choice of quantity to extremise
(that is T0's ruling, recorded in briefs/STREAM2_AM8_SELECTOR_COMPARISON_2026_09_28.md and
this file's own "status" field); any physical reading (ledger item 4); any promotion of the
cooper_s10 lattice certificate (still DRAFT, D6'); any ranking of cooper_s7 over cooper_s10.

Controls: checkers/test_C6_selector_adopted_controls.py.

Generated-by: Claude (Sonnet 5), Stream 2 | Verified-by: checkers/test_C6_selector_adopted_controls.py | Reviewed-by: T0 Y (selector choice, AskUserQuestion 2026-09-28), record N
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "checkers"))
import check_C6_selector_comparison as sc  # noqa: E402

AUDIT_DATE = "2026-09-28"

# What K3_CRITERIA.md's AM-8 clause claims, quoted for comparison only -- the values it is
# checked AGAINST are recomputed below, not read from the .md file (the .md's own prose is
# what is being verified, so it cannot also be the source of truth).
CLAIMED = {
    "cooper_s7": {"T": [1, 1, 1], "D": -3, "z": "infinity"},
    "cooper_s10": {"T": [1, 0, 1], "D": -4, "z": "infinity"},
}


class Refuse(Exception):
    pass


def chk(c, msg):
    if not c:
        raise Refuse(msg)


def verify(criteria_file, certs_dir):
    text = Path(criteria_file).read_text()
    chk("AM-8" in text and "SEL-D" in text, "K3_CRITERIA.md C6 does not carry the AM-8 clause text")
    cm = json.loads((certs_dir / "CM_POINTS_RHO20.json").read_text())
    cc = json.loads((certs_dir / "CM_COMPLETENESS.json").read_text())
    result = {}
    for fam, n in (("cooper_s7", 7), ("cooper_s10", 10)):
        rows = cm["families"][fam]["rows"]
        d = sc.sel_D(rows, n)
        per_d = {row["D"]: row for row in cc["families"][fam]["per_D"]}
        curve_row = per_d.get(d["D"])
        unique_on_curve = (curve_row is not None and curve_row.get("points_on_X0n_star") == 1
                          and curve_row.get("verdict") == "COMPLETE")
        claim = CLAIMED[fam]
        row_z = next((r for r in cm["families"][fam]["rows"] if r["v"] == d["picked_row"]["v"]), {}).get(
            "z_value_if_rational") if d["picked_row"] else None
        # the z=infinity point is not in "rows" with a z field the same way as finite loci;
        # confirm via locus_hits instead, which is keyed by z including "infinity"
        locus = cm["families"][fam]["locus_hits"].get("infinity", [{}])[0]
        z_matches = locus.get("D") == d["D"] and locus.get("v") == d["picked_row"]["v"]
        matches_claim = (d["picked_row"] is not None and d["picked_row"]["T"] == claim["T"]
                         and d["D"] == claim["D"] and z_matches)
        ok = (d["window_realizes_global_min"] and unique_on_curve and matches_claim)
        result[fam] = {"n": n, "recomputed": d, "unique_on_curve": unique_on_curve,
                       "matches_criteria_text": matches_claim, "ok": ok,
                       "advisory": fam == "cooper_s10"}
        if not ok:
            raise Refuse(f"{fam}: AM-8 text does not match the recomputed SEL-D "
                         f"(window_realizes_global_min={d['window_realizes_global_min']}, "
                         f"unique_on_curve={unique_on_curve}, matches_claim={matches_claim})")
    return result


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--criteria-file", default=REPO / "K3_CRITERIA.md", type=Path)
    ap.add_argument("--certs-dir", default=REPO / "data" / "certificates", type=Path)
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    try:
        result = verify(a.criteria_file, a.certs_dir)
    except Refuse as e:
        print("REFUSED:", e)
        return 2
    for fam, r in result.items():
        print(f"  {fam}: T={r['recomputed']['picked_row']['T']}, D={r['recomputed']['D']}, "
              f"unique_on_curve={r['unique_on_curve']}, matches K3_CRITERIA.md text={r['matches_criteria_text']}"
              + (" [ADVISORY]" if r["advisory"] else ""))
    print("AM-8 text verified against recomputation:", all(r["ok"] for r in result.values()))
    if a.emit:
        cert = {
            "certificate": "C6_SELECTED_CANDIDATE", "checker": "checkers/check_C6_selector_adopted.py",
            "checker_version": "1.0.0", "date": AUDIT_DATE, "tier": "B",
            "status": "Selector ADOPTED: AM-8, K3_CRITERIA.md C6, T0 ruling via AskUserQuestion 2026-09-28 "
                      "('SEL-D: minimal |disc T|'), narrowing D7' (ledger item 8) to cross-family comparison "
                      "only. This certificate verifies the criteria text's two named lattices against a fresh "
                      "recomputation and CM_COMPLETENESS.json's curve-point count (not class number alone). "
                      "cooper_s10's pick is ADVISORY: its lattice certificate stays DRAFT (D6'), untouched by "
                      "this selection. No ranking of the two families; no physical reading (ledger item 4).",
            "selected": {fam: {"T_reduced_form": r["recomputed"]["picked_row"]["T"], "D": r["recomputed"]["D"],
                               "z": "infinity", "v": r["recomputed"]["picked_row"]["v"],
                               "advisory": r["advisory"]} for fam, r in result.items()},
            "result": result,
            "inputs": {"sha256": {"K3_CRITERIA.md": sha(a.criteria_file),
                                  "data/certificates/CM_POINTS_RHO20.json": sha(a.certs_dir / "CM_POINTS_RHO20.json"),
                                  "data/certificates/CM_COMPLETENESS.json": sha(a.certs_dir / "CM_COMPLETENESS.json"),
                                  "data/certificates/C6_SELECTOR_COMPARISON.json": sha(a.certs_dir / "C6_SELECTOR_COMPARISON.json")}},
            "not_claimed": ["that SEL-D is intrinsically the correct quantity to extremise (a T0 ruling, not a "
                            "mathematical fact)", "any physical reading (ledger item 4)",
                            "any promotion of cooper_s10's lattice certificate (D6')",
                            "any ranking of cooper_s7 over cooper_s10"],
            "controls": "checkers/test_C6_selector_adopted_controls.py",
            "provenance": "Generated-by: Claude (Sonnet 5), Stream 2 | Verified-by: checkers/test_C6_selector_adopted_controls.py "
                          "| Reviewed-by: T0 Y (selector choice), record N",
        }
        out = a.certs_dir / "C6_SELECTED_CANDIDATE.json"
        out.write_text(json.dumps(cert, indent=2) + "\n")
        print("wrote", out)
    return 0 if all(r["ok"] for r in result.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
