#!/usr/bin/env python3
"""Renders briefs/STREAM2_A1_A4_A6_2026_09_21.md from the three certificates and the three
controls files.  Every number in the brief is looked up here, none is typed."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
C = ROOT / "data" / "certificates"
j = lambda n: json.loads((C / n).read_text())
a1, a4, a6 = j("ELLIPTIC_POINTS_ARE_CM.json"), j("PARTNER_GLOBAL_BOUNDEDNESS.json"), j("CM_COMPLETENESS.json")
k1, k4, k6 = j("ELLIPTIC_POINTS_ARE_CM_controls.json"), j("PARTNER_GLOBAL_BOUNDEDNESS_controls.json"), j("CM_COMPLETENESS_controls.json")
L = []
w = L.append


def controls(k):
    for r in k["results"]:
        w(f"- **{r['control']}** ({'behaved' if r['behaved'] else 'DID NOT BEHAVE'}): {r['detail']}")


def hand(cert):
    w("| clause | outcome |")
    w("|---|---|")
    for c, o in cert["hand_estimate"]["clauses"].items():
        w(f"| {c} | {'**REFUTED**' if o == 'REFUTED' else o} |")


w("# Stream 2 brief: A1 / A4 / A6 -- three small checkers on the CM-point table and the order-2 partners (2026-09-21)")
w("")
w("**Status: RECORD, NOT A GATE.** The rho = 20 cut is not adopted, T3 is not adopted, `K3_CRITERIA.md` is unchanged, "
  "nothing is scored or ranked. Lattice, modular and power-series arithmetic only; Tier B at best; no physical reading. "
  "Every cooper_s10 statement is **ADVISORY** (lattice certificate `C2_cooper_s10_v4_DRAFT.json` is DRAFT by T0 ruling).")
w("")
w("Rendered by `scripts/render_brief_A1_A4_A6_2026_09_21.py` from the three certificates and three controls files; "
  "numbers are looked up, not typed. The orchestrator's hand estimates were issued UNVERIFIED and are scored clause by clause.")
w("")
w("| item | checker | certificate | controls |")
w("|---|---|---|---|")
for cert, k in ((a1, k1), (a4, k4), (a6, k6)):
    w(f"| {cert['certificate']} | `{cert['checker']}` | `data/certificates/{cert['certificate']}.json` | `{cert['controls']}`: {k['behaved']}/{k['total']} behaved |")
w("")

# ---------------------------------------------------------------- A1
w("## A1. The singular loci are elliptic points, and elliptic points are forced to be CM points")
w("")
w(f"> {a1['forced_not_corroboration']}")
w("")
w("The argument is one line: a non-scalar integer matrix [[a, b], [c, d]] fixing tau gives the integer quadratic "
  "c tau^2 + (d - a) tau - b = 0, and in the basis of `CM_POINTS_RHO20.json` that quadratic *is* the pairing of an integer "
  "vector with the period. So P2's observation that the singular loci of L3 are rows of its CM table could not have come out otherwise, "
  "once the loci are elliptic points. What could have failed, and was checked exactly:")
w("")
for t in a1["what_is_not_forced_and_was_checked"]:
    w(f"- {t}")
w("")
w("Input-consistency only (listed apart after independent review: it is close to tautological by construction and is no evidence):")
w("")
for t in a1["input_consistency_checks_near_tautological"]:
    w(f"- {t}")
w("")
w("'Singular' below refers to a singular point of the operator L3 on the z-line and to a point of the upper half plane with "
  "non-trivial stabilizer in the group. No statement is made about fibres (ledger item 3) or about singularities of a surface.")
w("")
for key, f in a1["families"].items():
    w(f"**{key}**, n = {f['n']}, group {f['group']}{' -- **ADVISORY**' if f['advisory'] else ''}")
    w("")
    w("| locus z | v | tau quadratic (P, R, S) | stabilizer order | generator | det | trace | L3 exponents | lcm of denominators | clauses fired |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for l in f["loci"]:
        g = l["generator"]
        w(f"| {l['locus_z']} | {tuple(l['v'])} | {tuple(l['primitive_quadratic_of_tau'])} | {l['stabilizer_order_exact']} | "
          f"`{g['matrix']}` | {g['det']} | {g['trace']} | {', '.join(l['exponents_L3'])} | {l['exponent_denominator_lcm']} | "
          f"{', '.join(l['clauses_fired']) or 'none'} |")
    nl = f["non_locus_rows"]
    w("")
    w(f"Other rows of the table: {nl['count']}; with trivial stabilizer by the exact determination (no box): "
      f"{nl['trivial_stabilizer_exact_no_box']}; with a non-trivial stabilizer: {len(nl['rows_with_nontrivial_stabilizer'])}. "
      f"Orders found {f['orders_found']}, orders from the exponent denominators {f['orders_from_exponent_denominators']}.")
    w("")
b1, b2 = a1["search_boxes"]["path1_full_box_all_entries"], a1["search_boxes"]["path2_bruteforce_all_entries"]
w(f"Search: path 1 is the full box (all four entries in [-{b1}, {b1}], cut down by the exact linear condition), path 2 an independent "
  f"brute force on [-{b2}, {b2}]^4 with the fixed-point test done in exact quadratic-field arithmetic, path 3 an exact determination "
  "with no box (t^2 = m det, m in {0,1,2,3}, leaves finitely many candidates). The three must agree, and did. Path 3's argument is "
  "three lines in the docstring; it is not a machine proof.")
w("")
w("Hand estimate, scored:")
w("")
hand(a1)
w("")
dets = {k: sorted(l["generator"]["det"] for l in f["loci"]) for k, f in a1["families"].items()}
d10, d7 = dets["cooper_s10"], dets["cooper_s7"]
w(f"Observation recorded without interpretation: at n = 10 the generators have determinants {d10} -- {len(set(d10))} different "
  "Atkin-Lehner classes -- so the s10 coordinate needs the full group Gamma_0(10)*; in the Fricke-only group the order-4 point "
  "drops to order 2 and z = -1/4 loses its stabilizer (control R3). This is consistent with the s10 Hauptmodul certificate and "
  f"is advisory. At n = 7 the generator determinants are {d7}, listed per locus in the table above (det 7: Fricke element; det 1: in Gamma_0(7); control R5).")
w("")
w("Controls:")
w("")
controls(k1)
w("")

# ---------------------------------------------------------------- A4
w("## A4. Integrality of the order-2 partner is coordinate-dependent")
w("")
w("An attribute to **report**. Whether criterion C3 requires an integral partner is an open T0 question and is not answered here.")
w("")
N = a4["order_checked"]
w(f"For each series f: the least c <= {a4['C_MAX']} with f(c z) integral to order N = {N} (brute force over c, cross-checked against "
  "the per-prime formula), and the primes in the denominators. All arithmetic exact.")
w("")
w("| series | kind | result | primes in denominators | min v_2 of order-3 terms (n >= 1) | flag |")
w("|---|---|---|---|---|---|")
for r in a4["rows"]:
    w(f"| `{r['series']}` | {r['kind']} | {r['render']} | {r['denominator_primes'] or 'none'} | "
      f"{r.get('min_v2_of_order3_terms_n_ge_1', '')} | {'ADVISORY' if r.get('flags') else ''} |")
w("")
d = a4["cooper_s10_partner_detail"]
w(f"**cooper_s10_partner (ADVISORY flag by house rule; the series arithmetic does not use the lattice certificate).** Least c = {d['least_c']} "
  f"({d['render']}). 2-adic denominator exponents e(n), n = 0..39: `{d['e2_first_40']}`. Closed form tested, {d['closed_form_tested']}: "
  f"**{d['closed_form_verdict']}**, mismatches {d['closed_form_mismatches']}. Since an odd n contributes no factor 2, this is the same as "
  "e(n) = v_2(n!) = n - (number of binary digits 1 of n).")
w("")
w(f"Bound e(n) <= n - 1: observed {d['bound_e_le_n_minus_1_observed']}; status: {d['bound_status']}")
w("")
w("The two all-n hypotheses (added after independent review; the first version named only H1):")
w("")
for h in d["all_n_hypotheses"]:
    ss = h["stream1_statement"] if isinstance(h["stream1_statement"], list) else [h["stream1_statement"]]
    where = "; ".join(f"`{c['path']}:{c['line']}` `{c['name']}` at `{c['commit']}` ({c['status']})" for c in ss)
    w(f"- **{h['id']}**: {h['statement']}. In this checker: {h['status_in_this_checker']}. Stream 1 statement: {where}.")
w("")
w(d["all_n_hypotheses_note"])
w("")
tr = a4["register_vs_stream1_template"]
w("Register versus Stream 1 template (symbolic; parameters parsed from the Lean source): "
  + "; ".join(f"{k}: (a, b, c, d) = {tuple(v['params_abcd_parsed_from_lean'])}, all clauses hold = {v['ok']}" for k, v in tr.items()) + ".")
w("")
w(f"Least c = 2 for all n: {d['least_c_is_2_for_all_n']}. Closed form: {d['closed_form_status']}.")
w("")
g = a4["general_lemma"]
w(f"**General lemma (argument in the checker docstring, algebraic steps machine-checked, not a Lean proof).** {g['statement']} "
  f"Machine-checked pieces: `{g['machine_checked_pieces']}`; s10 parity pieces: `{g['s10_parity']}`. {g['consequence']} "
  "The column 'min v_2' above is the hypothesis of the lemma read off to order N: 0 -> c | 4, 1 -> c | 2, >= 2 -> c = 1; it is consistent on every row. "
  "For cooper_s7 and domb the hypothesis '4 divides every higher term' is PASS(N) only; for cooper_s10 the hypothesis '2 divides every higher term' "
  "is proved from the closed form sum_k C(n,k)^4 (x^4 = x mod 2, so the sum is 2^n mod 2).")
w("")
w("Stream 1 statements used (each read as source, no Lean build run; path, name and line re-verified at run time):")
w("")
for c in a4["external_citations_verified_at_run_time"]:
    w(f"- `{c['repo']}/{c['path']}:{c['line']}` at commit `{c['commit']}`: `{c['name']}` -- {c['status']}")
w("")
s18 = next(r for r in a4["rows"] if r["series"] == "sqrt(avs_sporadic3_s18)")
w(f"s18: Stream 1's `s18_partner_not_integral` is matched (first terms {s18['first_terms'][:4]}); the answer to 'what c?' is {s18['render']}, "
  f"denominators {s18['denominator_primes']}.")
w("")
w("Hand estimate, scored:")
w("")
hand(a4)
w("")
w("Controls:")
w("")
controls(k4)
w("")

# ---------------------------------------------------------------- A6
w("## A6. Completeness control on the P2 table, by enumeration of Heegner forms")
w("")
w("P2 claims no completeness. This control measures its window; an INCOMPLETE or ABSENT row is a finding about the window, not a defect.")
w("")
w(f"Normalisation, derived from v.omega = 0 and asserted on every vector used: {a6['normalisation']}.")
w("")
w("Expected counts come from exact enumeration (reduced forms x P^1(Z/n), modulo the automorphs of the reduced form, then modulo the "
  "Atkin-Lehner operators and complex conjugation, because the table identifies z with conj z). No class-number formula enters the method; "
  "one is used as cross-check X1 only.")
w("")
for key, f in a6["families"].items():
    s, a, x2 = f["summary"], f["absent_D"], f["x2_numeric_grouping_vs_exact_orbits"]
    x1 = a6["x1_class_number_cross_check"][key]
    w(f"**{key}**, n = {f['n']}{' -- **ADVISORY**' if f['advisory'] else ''}")
    w("")
    w(f"- Discriminants in the table: {s['D_values']}; COMPLETE: {s['complete']}; INCOMPLETE: {s['incomplete']}; "
      f"points expected {s['expected_total']}, found {s['found_total']}.")
    w(f"- Discriminants NOT in the table that carry points, {a['range']}: {a['count']} discriminants, {a['points_missing']} points; "
      f"least |D| absent: {a['least_abs_D_absent']}. {a['reason']}.")
    w(f"- X2: P2's numeric grouping by z of its {x2['vectors']} window vectors ({x2['numeric_groups']} groups) against the exact orbit "
      f"partition ({x2['exact_orbits']} orbits): identical = {x2['partitions_identical']}.")
    w(f"- X1: class-number formula against enumeration on {x1['discriminants_checked']} discriminants coprime to n "
      f"({x1['nonzero_cases']} with at least one class): {len(x1['disagreements'])} disagreements. "
      f"**Coverage of the table: {x1['table_discriminants_covered_count']} of {x1['table_discriminants_total']} table discriminants** "
      f"({x1['table_discriminants_covered']}). {x1['coverage_note']}")
    mp = f["discriminants_with_more_than_one_norm_div_pair"]
    w(f"- Discriminants whose classes need more than one pair (-v^2, div v): listed {mp['listed'] or 'none'}, absent {mp['absent'] or 'none'}.")
    w(f"- Contradictions (gate the exit code): {f['contradictions'] or 'none'}.")
    w("")
    w("| D | Gamma_0(n)-classes | points on X_0(n)* | expected (up to conj) | found | verdict |")
    w("|---|---|---|---|---|---|")
    for p in f["per_D"]:
        w(f"| {p['D']} | {p['gamma0_classes']} | {p['points_on_X0n_star']} | {p['expected']} | {p['found']} | {p['verdict']} |")
    w("")
    w("First absent discriminants: " + "; ".join(
        f"D = {r['D']} ({r['verdict']}, needs (-v^2, div v) = {[tuple(t) for t in r['minus_v2_and_div_required']]})" for r in a["rows"][:6]) + ".")
    w("")
n_inc = sum(f["summary"]["incomplete"] for f in a6["families"].values())
x2_all = all(f["x2_numeric_grouping_vs_exact_orbits"]["partitions_identical"] is True for f in a6["families"].values())
w("Reading, Tier B: " + ("within its logged window the P2 table is complete at every discriminant it lists" if n_inc == 0 else
                         f"the P2 table is INCOMPLETE at {n_inc} of the discriminants it lists (rows above)")
  + (", and its numeric grouping by z is the exact orbit partition. " if x2_all else
     "; its numeric grouping by z DIFFERS from the exact orbit partition (X2 above). ") + "It is not complete as a list of discriminants: the window is cut on -v^2, and a discriminant whose Heegner "
  "classes all need a larger norm never enters. " + ("For every discriminant seen, one pair (-v^2, div v) serves all its classes (computed: the per-family lines above), which is "
       "consistent with no listed D being partially covered. " if not any(
           f["discriminants_with_more_than_one_norm_div_pair"][s] for f in a6["families"].values() for s in ("listed", "absent"))
       else "Some discriminants need more than one pair (-v^2, div v) (per-family lines above), so partial coverage of a D is possible. ") + "That the window contains a representative of every point at the listed D is an outcome of the "
  "enumeration, not a theorem about the window.")
w("")
for t in a6["tier_notes"]:
    w(f"- {t}")
w("")
w("Controls:")
w("")
controls(k6)
w("")

w("## Not claimed")
w("")
for cert in (a1, a4, a6):
    for t in cert["not_claimed"]:
        w(f"- ({cert['certificate']}) {t}")
w("")
w("## Open items for T0 (flagged, not decided here)")
w("")
w("- Whether criterion C3 requires integrality of the order-2 partner, and if so in which coordinate (A4 reports c per series; it does not rule).")
w("- Whether the P2 window should be re-cut on |D| instead of -v^2 if a complete list of discriminants is ever wanted (A6 lists what is absent).")
w("")
w("Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: the three controls files named above "
  f"({k1['behaved']}/{k1['total']}, {k4['behaved']}/{k4['total']}, {k6['behaved']}/{k6['total']}) | Reviewed-by: N")
(ROOT / "briefs" / "STREAM2_A1_A4_A6_2026_09_21.md").write_text("\n".join(L) + "\n")
print("written", len(L), "lines")
