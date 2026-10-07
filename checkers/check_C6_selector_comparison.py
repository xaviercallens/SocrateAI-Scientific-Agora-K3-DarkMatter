#!/usr/bin/env python3
"""
check_C6_selector_comparison.py -- AM-6's selector clause asks for the outputs of the
known selectors, computed exactly, listed side by side. This is a RECORD, not a gate:
it adopts nothing (only K3_CRITERIA.md, via the sec. 6 amendment protocol, can do that),
and every result here is candidate data for a T0 choice, never a ranking or a pick.

Two selectors, applied to the C6 candidate set (data/certificates/CM_POINTS_RHO20.json
"rows", both families), computed from lattice-intrinsic quantities only -- never from z,
never from a physical reading:

  SEL-D  minimal |disc T| (discriminant floor). Global minimality is checked two ways:
         (a) the occurrence criterion "D occurs at level n iff D is a square mod 4n"
             (check_A2_membership.py's own rule), searched exactly over |D| in [3, BOUND);
         (b) cross-checked against CM_COMPLETENESS.json's per_D table, which counts actual
             points on X_0(n)+ / X_0(n)*, not just reduced forms -- reduced_forms h(D)=1
             is a FORM count and is not by itself uniqueness on the curve; the curve count
             is what points_on_X0n_star gives.
         The certificate row (the family's own z = infinity locus) is checked to realize
         this global minimum; if it does not, that is reported, not hidden.
  SEL-N  minimal |v^2| (the smallest nonzero even negative norm on U+<2N>; -2 is the floor
         every wall_general/rootEF-type theorem already achieves). Reported WITH its exact
         tie count: if more than one row of the family shares the minimal |v^2|, that is
         stated as non-unique, and the effect of ONE stated tiebreak (minimal div(v), i.e.
         the most primitive representative) is reported separately -- never silently
         applied as if it were the selector itself.

A third selector named in the audited external review, the W_N Fricke-fixed-point count
h(-4N)+h(-N), is already established (checkers/check_external_review_fable_2026_09_21.py,
clause F8) to be non-unique at N != 1 for exactly this reason; it is reported by reference,
not recomputed here.

Neither SEL-D nor SEL-N is adopted by this checker. Where SEL-D's output coincides with a
value D7' declined to adopt ("no minimum-|D| rule"), that conflict is stated explicitly in
the output, not resolved.

Controls: checkers/test_C6_selector_comparison_controls.py.

Generated-by: Claude (Sonnet 5), Stream 2 | Verified-by: checkers/test_C6_selector_comparison_controls.py | Reviewed-by: N
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "checkers"))
from check_external_review_fable_2026_09_21 import reduced_primitive_forms, class_number  # noqa: E402

AUDIT_DATE = "2026-09-28"


def min_abs_D_at_level(n, bound=2000):
    """Occurrence criterion: D occurs at level n iff D is a square mod 4n. Exact search
    over valid discriminants D < 0, D === 0 or 1 (mod 4), |D| >= 3."""
    mod = 4 * n
    squares_mod = set((s * s) % mod for s in range(mod))
    for absD in range(3, bound):
        D = -absD
        if D % 4 not in (0, 1):
            continue
        if D % mod in squares_mod:
            return D
    raise RuntimeError(f"no valid D found for n={n} within bound {bound}")


def sel_D(rows, n):
    Dmin = min_abs_D_at_level(n)
    forms = reduced_primitive_forms(Dmin)
    cert_min = min(abs(r["D"]) for r in rows)
    cert_row = next(r for r in rows if abs(r["D"]) == cert_min)
    return {
        "definition": "minimal |disc T| over the occurrence criterion, searched exactly (not from the certificate's own window)",
        "global_min_abs_D": abs(Dmin), "D": Dmin, "reduced_forms_of_D": forms, "class_number_h_D": len(forms),
        "certificate_window_min_abs_D": cert_min,
        "window_realizes_global_min": cert_min == abs(Dmin),
        "picked_row": {"v": cert_row["v"], "D": cert_row["D"], "T": cert_row["T_X_reduced_form_abc"], "div_v": cert_row["div_v"]}
        if cert_min == abs(Dmin) else None,
    }


def sel_N(rows):
    min_norm = min(abs(r["minus_v2"]) for r in rows)
    ties = [r for r in rows if abs(r["minus_v2"]) == min_norm]
    tiebreak_div = sorted(ties, key=lambda r: (r["div_v"], abs(r["D"])))
    return {
        "definition": "minimal |v^2| over the certificate window (the -2 floor)",
        "min_abs_v2": min_norm, "tie_count": len(ties),
        "unique": len(ties) == 1,
        "tied_rows": [{"v": r["v"], "D": r["D"], "T": r["T_X_reduced_form_abc"], "div_v": r["div_v"]} for r in ties],
        "one_stated_tiebreak_minimal_div_v": {"v": tiebreak_div[0]["v"], "D": tiebreak_div[0]["D"],
                                              "T": tiebreak_div[0]["T_X_reduced_form_abc"], "div_v": tiebreak_div[0]["div_v"],
                                              "note": "NOT part of SEL-N as defined; reported only to show what one natural "
                                                      "tiebreak would give, for T0 to accept, replace or reject explicitly"}
        if len(ties) > 1 else None,
    }


def run(verbose=True):
    cm = json.loads((REPO / "data" / "certificates" / "CM_POINTS_RHO20.json").read_text())
    cc = json.loads((REPO / "data" / "certificates" / "CM_COMPLETENESS.json").read_text())
    out = {"families": {}}
    for fam, n in (("cooper_s7", 7), ("cooper_s10", 10)):
        rows = cm["families"][fam]["rows"]
        d = sel_D(rows, n)
        nn = sel_N(rows)
        per_d = {row["D"]: row for row in cc["families"][fam]["per_D"]}
        curve_row = per_d.get(d["D"])
        d["points_on_curve_at_D"] = curve_row.get("points_on_X0n_star") if curve_row else None
        d["curve_completeness_verdict"] = curve_row.get("verdict") if curve_row else "D not in CM_COMPLETENESS window"
        d["unique_on_curve"] = (curve_row is not None and curve_row.get("points_on_X0n_star") == 1
                                and curve_row.get("verdict") == "COMPLETE")
        agree = (d["picked_row"] is not None and nn["unique"] and d["picked_row"]["v"] == nn["tied_rows"][0]["v"])
        out["families"][fam] = {
            "n": n, "advisory": bool(cm["families"][fam]["advisory"]), "SEL-D": d, "SEL-N": nn,
            "SEL-D_and_SEL-N_agree": agree,
            "d7prime_conflict": "SEL-D is a minimal-|D| rule; D7' (ledger item 8) states 'no minimum-|D| rule' without "
                                "restricting that to cross-family comparison. Adopting SEL-D needs its own T0 text "
                                "resolving or narrowing that clause, not an inference from context." if not agree else None,
        }
    if verbose:
        for fam, v in out["families"].items():
            print(f"=== {fam} (n={v['n']}{', ADVISORY' if v['advisory'] else ''})")
            d, nn = v["SEL-D"], v["SEL-N"]
            print(f"  SEL-D: global min |D| = {d['global_min_abs_D']} (D={d['D']}, h={d['class_number_h_D']}); "
                  f"window realizes it: {d['window_realizes_global_min']}; unique on curve: {d['unique_on_curve']} "
                  f"(points_on_X0n_star={d['points_on_curve_at_D']}, {d['curve_completeness_verdict']})")
            if d["picked_row"]:
                print(f"    -> {d['picked_row']}")
            print(f"  SEL-N: min |v^2| = {nn['min_abs_v2']}, ties = {nn['tie_count']}, unique = {nn['unique']}")
            for t in nn["tied_rows"]:
                print(f"    tied: {t}")
            if nn["one_stated_tiebreak_minimal_div_v"]:
                print(f"    (tiebreak by min div(v), NOT adopted here): {nn['one_stated_tiebreak_minimal_div_v']}")
            print(f"  SEL-D and SEL-N agree: {v['SEL-D_and_SEL-N_agree']}")
            if v["d7prime_conflict"]:
                print(f"  FLAG: {v['d7prime_conflict']}")
    return out


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    res = run()
    if a.emit:
        rec = {
            "certificate": "C6_SELECTOR_COMPARISON", "checker": "checkers/check_C6_selector_comparison.py",
            "checker_version": "1.0.0", "date": AUDIT_DATE, "tier": "B",
            "status": "RECORD, NOT A GATE, NOT AN ADOPTION. Neither SEL-D nor SEL-N is adopted by this certificate; "
                      "AM-6 requires the selector to be named by its own T0 text before any candidate is preferred. "
                      "D7' is unchanged: no ranking of cooper_s7 over cooper_s10 (the ADVISORY label that rested on D6' "
                      "lifted with D15', 2026-09-29; the no-ranking rule did not).",
            "result": res,
            "inputs": {"sha256": {"data/certificates/CM_POINTS_RHO20.json": sha(REPO / "data" / "certificates" / "CM_POINTS_RHO20.json"),
                                  "data/certificates/CM_COMPLETENESS.json": sha(REPO / "data" / "certificates" / "CM_COMPLETENESS.json")}},
            "not_claimed": ["that either selector is adopted", "any physical reading of any point (ledger item 4)",
                            "any ranking of the two families", "any promotion of cooper_s10"],
            "controls": "checkers/test_C6_selector_comparison_controls.py",
            "provenance": "Generated-by: Claude (Sonnet 5), Stream 2 | Verified-by: checkers/test_C6_selector_comparison_controls.py | Reviewed-by: N",
        }
        out = REPO / "data" / "certificates" / "C6_SELECTOR_COMPARISON.json"
        out.write_text(json.dumps(rec, indent=2) + "\n")
        print("wrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
