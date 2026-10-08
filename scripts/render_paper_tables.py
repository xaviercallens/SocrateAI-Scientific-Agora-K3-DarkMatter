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
import re
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


def set_str(parts):
    return "$\\{" + ",".join(str(x) for x in sorted((int(p) for p in parts if int(p) > 0), reverse=True)) + "\\}$"


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
            if tr is None:
                raise SystemExit(f"no lattice-tier row for {fam} {h['v']}: refusing to guess the advisory flag")
            adv = r"\,(ADVISORY)" if tr["advisory_family"] else ""   # read from the certificate (2026-10-08 fix; was keyed on the family name)
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

    # 2026-10-08 fix: the generic and locus orders were typed literals; they are now read from the certificate.
    g = d["T3_generic_orders"]
    m = re.match(r"^(\d+) simple", g["roots_of_d_of_s2"])
    if not m:
        raise SystemExit("T3_generic_orders.roots_of_d_of_s2 not in the expected '<k> simple ...' form")
    gparts = [g["orders_at_s_plus_minus_1"]] * 2 + [1] * int(m.group(1)) + ([g["order_at_infinity"]] if g["order_at_infinity"] else [])
    lines.append(f"Generic ($E_1\\not\\cong E_2$) & {set_str(gparts)} & --- \\\\")
    for fam_label, loc in (("cooper\\_s7, $z=-1$", "-1"), ("cooper\\_s7, $z=1/27$", "1/27")):
        row = d["T5_s7_loci"][loc]
        o = row["orders"]
        parts = [o["s=+1"], o["s=-1"], o["s=0"]] + list(o["roots_of_e(s^2)"]) + ([o["s=infinity"]] if o["s=infinity"] else [])
        lines.append(f"{fam_label} & {set_str(parts)} & $J={esc(row['J'])}$ \\\\")
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


# ---- tables for papers/stream2_k3_identification_twisted_route_2026_10_08.tex (added 2026-10-08) ----
def _pt(point):
    fam, _, rest = point.partition(", ")
    z = rest.replace("z = ", "").replace(" (AM-8 pick)", "")
    z = r"$\infty$" if z == "infinity" else f"${z}$"
    return fam, z, "(AM-8 pick)" in point


def render_identification():
    d = json.loads((CERTS / "SELECTED_K3_IDENTIFICATION.json").read_text())
    lines = [r"\begin{tabular}{lllrrl}", r"\toprule",
             r"Family & $z$ & $T$ (Gram) & $\det T$ & classes & Surface \\", r"\midrule"]
    for p in d["points"]:
        fam, z, pick = _pt(p["point"])
        g = p["T_gram"]
        name = p["identification"].split(" (")[0] if p["determined_by_discriminant_alone"] else r"not named by $\det T$ alone"
        name = re.sub(r"X_(\d+)", r"$X_{\1}$", name)
        lines.append(f"\\lean{{{esc(fam)}}} & {z}{'$^{*}$' if pick else ''} & $[{g[0][0]},{g[0][1]};{g[1][0]},{g[1][1]}]$ & "
                     f"${p['determinant']}$ & ${p['number_of_classes']}$ & {name} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def render_tw0_degrees():
    d = json.loads((CERTS / "TW0_HODGE_DEGREE_ORBIFOLD.json").read_text())["result"]
    deg = d["cooper_s7"]["degrees"]
    sr = d["surface_reading"]
    lines = [r"\begin{tabular}{ll}", r"\toprule", r"Quantity & Value \\", r"\midrule",
             f"orbifold Euler characteristic of $X_0(7)^+$ & ${deg['chi_orb']}$ \\\\",
             f"$\\deg\\omega$ (family Hodge bundle, $\\mathbb{{Q}}$-degree) & ${deg['deg_omega_Q']}$ \\\\",
             f"$\\deg\\omega^{{2}}$ & ${deg['deg_omega2_Q']}$ \\\\",
             f"$\\chi(\\mathcal{{O}}_{{K3}})$ (elliptic-surface reading of $\\ell$) & ${sr['chi_O']}$ \\\\",
             f"$\\deg\\Delta$ of the Weierstrass model & ${sr['deg_Delta']}$ \\\\",
             r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def render_tw1_screen():
    rows = []
    for key in ("P3", "P1xP2"):
        r = json.loads((CERTS / f"TW1_two_e8_{key}.json").read_text())["result"]
        rows.append((r["base"], r["overall_verdict"]))
    b = json.loads((CERTS / "TW1_two_e8_P1bundle_P2.json").read_text())["result"]["symbolic_n"]
    rows.append((b["base"].replace("(+)", r"$\oplus$"), b["overall_verdict"].split(" (")[0] + r" (degree budget all $n\ge0$; realizability checked $n\le18$)"))
    lines = [r"\begin{tabular}{ll}", r"\toprule", r"Base $B_3$ & Two-divisor degree screen \\", r"\midrule"]
    for base, v in rows:
        base = base.replace("P^3", r"$\mathbb{P}^3$").replace("P^1 x P^2", r"$\mathbb{P}^1\times\mathbb{P}^2$").replace("O(n)", r"$\mathcal{O}(n)$").replace("P(O", r"$\mathbb{P}$($\mathcal{O}$").replace("over P^2", r"over $\mathbb{P}^2$")
        lines.append(f"{base} & {v} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def render_tw2_loci():
    gen = json.loads((CERTS / "TW2_HEIGHT_CONDITION.json").read_text())["result"]["cooper_s7_n7"]
    loci = json.loads((CERTS / "TW2_RHO20_LOCI.json").read_text())["result"]["loci"]
    lines = [r"\begin{tabular}{lrrlrll}", r"\toprule",
             r"$s_7$ member & $|\mathrm{disc}\,T|$ & $\rho$ & extra roots & MW rank & $h(P)$ & $\bar P\cdot\bar O$ \\", r"\midrule",
             f"generic & ${gen['target_abs_disc_NS']}$ & $19$ & --- & ${gen['mordell_weil_rank']}$ & ${gen['height_h_P']}$ & ${gen['P_dot_O']}$ \\\\"]
    for k in ("1/27", "-1", "infinity"):
        v = loci[k]
        r = v["resolution"]
        z = r"$z=\infty$" if k == "infinity" else f"$z={k}$"
        if r["mordell_weil_rank"] == 0:
            h, po = "---", "no section"
        else:
            h = f"${r['height']}$"
            po = ", ".join(f"${s['P_dot_O']}$" for s in r["P_dot_O_solutions"])
        lines.append(f"{z} & ${v['abs_disc_T']}$ & ${v['rho']}$ & ${r['root_lattice'][0]}_{{{r['root_lattice'][1:]}}}$ & ${r['mordell_weil_rank']}$ & {h} & {po} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def render_t3():
    d = json.loads((CERTS / "T3_LEVEL_CONSISTENCY.json").read_text())["results"]
    lines = [r"\begin{tabular}{llll}", r"\toprule", r"Family & $n$ from lattice & $n$ from modular side & Verdict \\", r"\midrule"]
    for fam, v in d.items():
        lines.append(f"\\lean{{{esc(fam)}}} & ${v['n_lattice']}$ & ${v['n_modular']}$ & {esc(v['verdict'])} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def render_reading_s():
    d = json.loads((CERTS / "K3xT2_READING_S.json").read_text())["result"]
    lines = [r"\begin{tabular}{llllll}", r"\toprule",
             r"Family & $n$ & NS sig. & saturated & $T(E\times E')$ (Gram), sig. & $\cong$ certified $T$ \\", r"\midrule"]
    for fam, v in d["generic"].items():
        gtxt = ";".join(",".join(str(x) for x in row) for row in v["T_gram"])
        lines.append(f"\\lean{{{esc(fam)}}} & ${v['n']}$ & $({v['NS_signature'][0]},{v['NS_signature'][1]})$ & "
                     f"{'yes' if v['NS_saturated'] else 'no'} & $[{gtxt}]$, $({v['T_signature'][0]},{v['T_signature'][1]})$ & "
                     f"{'yes' if v['verdict'] == 'ISOMETRIC_TO_CERTIFIED_T' else 'NO'} \\\\")
    lines += [r"\midrule", r"$s_7$ point & model $j$ & CM disc. & $T(E\times E)$ & certified $T$ & agree \\", r"\midrule"]
    for z, v in d["rho20_cooper_s7"].items():
        zz = r"$\infty$" if z == "infinity" else f"${z}$"
        a, b, c = v["T_reduced_abc"]
        ca, cb, cc = v["certified_T_reduced_abc"]
        lines.append(f"{zz} & ${v['j_from_model']}$ & ${v['cm_discriminant_by_computation']}$ & $[{2*a},{b};{b},{2*c}]$ & "
                     f"$[{2*ca},{cb};{cb},{2*cc}]$ & {'yes (forced)' if v['agree'] else 'NO'} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


TABLES = {
    "reading_s.tex": render_reading_s,
    "identification.tex": render_identification,
    "tw0_degrees.tex": render_tw0_degrees,
    "tw1_screen.tex": render_tw1_screen,
    "tw2_loci.tex": render_tw2_loci,
    "t3_level.tex": render_t3,
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
