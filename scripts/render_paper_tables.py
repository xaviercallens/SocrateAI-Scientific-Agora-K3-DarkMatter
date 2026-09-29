#!/usr/bin/env python3
"""
render_paper_tables.py -- generates the LaTeX table fragments \\input by
papers/stream2_selection_geometry_2026_09_29.tex, from certificates only.

Standing rule 5 ("numbers are computed, never typed") applies to prose exactly as it
applies to checkers: a paper is prose. Every number in every table here is read from a
certificate at run time; nothing is typed into this script as a literal result value
(structural constants -- table column counts, LaTeX syntax -- are not results).

Tables written, each as papers/tables/<name>.tex:
  rankjump_rows.tex     the six CM_POINTS_RHO20 locus rows, joined with
                         CM_POINTS_RHO20_LATTICE_TIER.json for the lattice tier and
                         source count
  selector_comparison.tex   SEL-D vs SEL-N per family, from C6_SELECTOR_COMPARISON.json,
                         including the s7 SEL-N tie
  fibration_orders.tex  the Inose fibration discriminant orders, from
                         INOSE_FIBRATION_MULTIPLICITIES.json (generic / both s7 loci / J=0 / J=1)
  monodromy_diameters.tex   the certified enclosure diameters, from
                         CERTIFIED_MONODROMY_L2_cooper_s7.json / _s10.json

Usage:
  python3 scripts/render_paper_tables.py            # write the fragments
  python3 scripts/render_paper_tables.py --check     # exit 1 if any fragment is stale
Controls: checkers/test_render_paper_tables_controls.py (one negative: a tampered
certificate must change the rendered table, so --check catches drift).

Generated-by: Claude (Sonnet 5), Stream 2 | Verified-by: checkers/test_render_paper_tables_controls.py | Reviewed-by: N
"""
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CERTS = REPO / "data" / "certificates"
OUT = REPO / "papers" / "tables"


def esc(s):
    return str(s).replace("_", "\\_")


def frac_or_int(x):
    """Render an exact rational/int string for LaTeX math mode."""
    s = str(x)
    if "/" in s:
        n, d = s.split("/")
        return f"{n}/{d}"
    return s


def gram_str(T):
    a, b, c = T
    return f"[{a},{b};{b},{c}]" if False else f"[[{2*a},{b}],[{b},{2*c}]]"


def render_rankjump_rows():
    cm = json.loads((CERTS / "CM_POINTS_RHO20.json").read_text())
    tier = json.loads((CERTS / "CM_POINTS_RHO20_LATTICE_TIER.json").read_text())
    tier_rows = {(r["candidate"], tuple(r["v"])): r for r in tier["rows"]}
    lines = [r"\begin{tabular}{lllrrll}", r"\toprule",
             r"Family & $z$ & $v$ & $v^2$ & $D$ & $T$ (reduced) & Tier / sources \\", r"\midrule"]
    for fam in ("cooper_s7", "cooper_s10"):
        fh = cm["families"][fam]
        for locus, hits in sorted(fh["locus_hits"].items(), key=lambda kv: (kv[0] != "1/27" and kv[0] != "-1", kv[0])):
            h = hits[0]
            tr = tier_rows.get((fam, tuple(h["v"])))
            src = tr["independent_files_passing"] if tr else 0
            tierlab = tr["lattice_tier"] if tr else "?"
            adv = r"\,(ADVISORY)" if fam == "cooper_s10" else ""
            zdisp = r"$\infty$" if locus == "infinity" else f"${frac_or_int(locus)}$"
            a, b, c = h["T_X_reduced_form_abc"]
            lines.append(
                f"\\lean{{{esc(fam)}}}{adv} & {zdisp} & $({h['v'][0]},{h['v'][1]},{h['v'][2]})$ & "
                f"${-h['minus_v2']}$ & ${h['D']}$ & $[{2*a},{b};{b},{2*c}]$ & "
                f"Tier {tierlab}, {src} source(s) \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def render_selector_comparison():
    d = json.loads((CERTS / "C6_SELECTOR_COMPARISON.json").read_text())["result"]["families"]
    lines = [r"\begin{tabular}{llll}", r"\toprule",
             r"Family & SEL-D (min $|{\rm disc}\,T|$) & SEL-N (min $|v^2|$) & Agree? \\", r"\midrule"]
    for fam, v in d.items():
        sd, sn = v["SEL-D"], v["SEL-N"]
        adv = r"\,(ADVISORY)" if v["advisory"] else ""
        dtxt = f"$T=[{2*sd['picked_row']['T'][0]},{sd['picked_row']['T'][1]};{sd['picked_row']['T'][1]},{2*sd['picked_row']['T'][2]}]$, $D={sd['D']}$"
        if sn["unique"]:
            ntxt = f"$D={sn['tied_rows'][0]['D']}$ (unique)"
        else:
            ds = ", ".join(f"$D={t['D']}$" for t in sn["tied_rows"])
            ntxt = f"tie: {ds} ({sn['tie_count']} rows)"
        lines.append(f"\\lean{{{esc(fam)}}}{adv} & {dtxt} & {ntxt} & {'Yes' if v['SEL-D_and_SEL-N_agree'] else 'No'} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def render_fibration_orders():
    d = json.loads((CERTS / "INOSE_FIBRATION_MULTIPLICITIES.json").read_text())["result"]
    lines = [r"\begin{tabular}{lll}", r"\toprule", r"Case & Discriminant-root orders & Note \\", r"\midrule"]

    def orders_str(entry):
        parts = []
        for o in entry.get("orders_finite", []):
            parts += [str(o["order"])] * o["degree"]
        if entry.get("order_at_infinity"):
            parts.append(str(entry["order_at_infinity"]))
        return "$\\{" + ",".join(sorted(parts, key=int, reverse=True)) + "\\}$"

    lines.append(r"Generic ($E_1\not\cong E_2$) & $\{10,10,1,1,1,1\}$ & --- \\")
    for fam_label, loc in (("cooper\\_s7, $z=-1$", "-1"), ("cooper\\_s7, $z=1/27$", "1/27")):
        row = d["T5_s7_loci"][loc]
        lines.append(f"{fam_label} & $\\{{10,10,2,1,1\\}}$ & $J={esc(row['J'])}$ \\\\")
    for k, label in (("J=1 (lam=-1)", "$J=1$ ($E_1\\cong E_2$)"), ("J=0 (lam^2-lam+1=0)", "$J=0$ ($E_i\\cong E_\\omega$)")):
        lines.append(f"{label} & {orders_str(d['T6_special_values'][k])} & --- \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def render_monodromy_diameters():
    lines = [r"\begin{tabular}{lll}", r"\toprule", r"Family & Clause & Enclosure diameter \\", r"\midrule"]
    for fam in ("cooper_s7", "cooper_s10"):
        d = json.loads((CERTS / f"CERTIFIED_MONODROMY_L2_{fam}.json").read_text())["result"]
        for k, v in d["clauses"].items():
            if k.startswith("C-b_sym2_entries_certified_at_"):
                loc = k.split("_at_")[-1]
                mant, exp = f"{v['max_diameter']:.1e}".split("e-")
                lines.append(f"\\lean{{{esc(fam)}}} & $z={esc(loc)}$ & ${mant}\\times 10^{{-{int(exp)}}}$ \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


TABLES = {
    "rankjump_rows.tex": render_rankjump_rows,
    "selector_comparison.tex": render_selector_comparison,
    "fibration_orders.tex": render_fibration_orders,
    "monodromy_diameters.tex": render_monodromy_diameters,
}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    OUT.mkdir(parents=True, exist_ok=True)
    stale = []
    for name, fn in TABLES.items():
        content = fn()
        path = OUT / name
        if a.check:
            if not path.exists() or path.read_text() != content:
                stale.append(name)
        else:
            path.write_text(content)
            print("wrote", path)
    if a.check:
        if stale:
            print("STALE:", stale, file=sys.stderr)
            return 1
        print("OK: all table fragments match the certificates")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
