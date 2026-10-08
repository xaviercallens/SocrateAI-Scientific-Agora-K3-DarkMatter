#!/usr/bin/env python3
"""check_selected_k3_identification.py -- WHICH K3 surface is the selected point? (T0: "identify the K3", 2026-10-08)

The AM-8 pick is a CM point of the cooper_s7 (resp. cooper_s10) moduli curve whose transcendental lattice is a
rank-2 positive-definite even lattice T = [[2a,b],[b,2c]]. By the Shioda-Inose bijection a singular K3 surface
(Picard number 20) is determined up to isomorphism by T up to SL2(Z)-equivalence, so the surface is identified by
the *class of T*. This checker does that identification mechanically, with everything read or computed:

  1. T for each point is READ from SELECTED_K3_DOSSIER.json (the two AM-8 picks) and CM_POINTS_RHO20.json (the other
     s7 loci);
  2. the SL2(Z)-classes of positive-definite even forms of the same determinant are ENUMERATED (reduced forms,
     non-primitive included) -- the count says whether the determinant alone fixes the surface;
  3. the literature table and statements are PARSED from the pinned, read text docs/literature/takatsu_1903.03054.txt
     (Takatsu, arXiv:1903.03054): the table of [a,b,c] with their names (No.1 [2,1,2] and No.2 [2,0,2] attributed to
     Vinberg, No.3 [2,1,4] to Ujikawa), and the sentences "unique up to isomorphisms for d = 3, 4, 7 ... X_d" and the
     E_omega / E_i constructions; nothing from the table is typed in this file;
  4. consistency with the explicit model: at z = infinity the model has sigma = pi = 0 (E_omega x E_omega), which is the
     Shioda-Inose partner Takatsu's section 5.1 uses for X_3 -- a CONSISTENCY statement (forced by Shioda-Inose, not
     corroboration; ledger item 8).

Tiers: that T_X = v-perp is the Tier B framework (Dolgachev 1996 sec. 7, pinned); the bijection and the table are Tier L
(sources read, lines recorded in the certificate). NOT identified: a smooth fibre of a specific projective model --
A2_MEMBERSHIP records that what is established is a point of the period domain.

Usage: python3 checkers/check_selected_k3_identification.py [--emit]
Controls: checkers/test_selected_k3_identification_controls.py
Generated-by: Claude (Sonnet 5.5), Stream 2, 2026-10-08 | Verified-by: controls | Reviewed-by: N
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CERTS = REPO / "data" / "certificates"
SRC = REPO / "docs" / "literature" / "takatsu_1903.03054.txt"
CERT = CERTS / "SELECTED_K3_IDENTIFICATION.json"
SRC_SHA256 = "ffb3e5b452e30fe2c98f48518dedf1e8f7e916a7b8b299fd784a1d789c280cbe"   # of the .pdf recorded in MANIFEST.md


class Refuse(RuntimeError):
    pass


def reduced_classes(d):
    """SL2(Z)-classes of positive-definite integral forms a x^2 + b xy + c y^2 with 4ac - b^2 = d (all contents),
    as reduced triples: |b| <= a <= c, and b >= 0 when |b| == a or a == c."""
    if d <= 0:
        raise Refuse(f"determinant must be positive, got {d}")
    out = []
    for a in range(1, int(math.isqrt(d // 3)) + 2):
        for b in range(-a, a + 1):
            if (d + b * b) % (4 * a):
                continue
            c = (d + b * b) // (4 * a)
            if c < a or (abs(b) == a and b < 0) or (a == c and b < 0):
                continue
            out.append((a, b, c))
    return out


def is_ambiguous(a, b, c):
    """class equal to its complex-conjugate (b -> -b): complex conjugation does not change the surface's isomorphism class."""
    return b == 0 or abs(b) == a or a == c


def parse_source(path=SRC):
    if not path.exists():
        raise Refuse(f"pinned source missing: {path}")
    text = path.read_text()
    flat = re.sub(r"(\w)-\s+(\w)", r"\1\2", re.sub(r"\s+", " ", text))   # join words hyphenated across line breaks ("dis- criminant")
    rows = {}
    for m in re.finditer(r"^\s*(\d+)\s+\[(\d+),\s*(\d+),\s*(\d+)\]\s+(.+?)\s*$", text, re.M):
        rows[(int(m.group(2)), int(m.group(3)), int(m.group(4)))] = {"No": int(m.group(1)), "attribution": m.group(5).strip(),
                                                                    "line": text[:m.start()].count("\n") + 1}
    if len(rows) < 3:
        raise Refuse(f"parsed only {len(rows)} table rows from {path.name}; the table moved or the file is wrong")
    uniq = re.search(r"unique up to isomorphisms for d = 3, 4, 7, so we denoted by X ?d these K3 surfaces", flat)
    same_disc = re.search(r"there exist singular K3 surfaces which have the same discriminant, but is not isomorphic", flat)
    e3 = re.search(r"Let E3 be an elliptic curve C/Z \+ Z", flat)
    e4 = re.search(r"Let E4 be an elliptic curve C/Z \+ Z", flat)
    if not (uniq and same_disc and e3 and e4):
        raise Refuse("a required statement (uniqueness for d = 3, 4, 7 / Remark 1 / E3, E4 constructions) was not found in the pinned text")
    return {"table": rows, "uniqueness_sentence_found": True, "remark_same_discriminant_found": True, "constructions_E3_E4_found": True}


def identify(label, abc, src):
    a, b, c = abc
    d = 4 * a * c - b * b
    classes = reduced_classes(d)
    gram = (2 * a, b, 2 * c)
    row = src["table"].get(gram)
    res = {"point": label, "T_reduced_form_abc": [a, b, c], "T_gram": [[2 * a, b], [b, 2 * c]], "determinant": d,
           "this_class_is_in_enumeration": (a, b, c) in classes, "classes_of_this_determinant": [list(t) for t in classes],
           "number_of_classes": len(classes), "ambiguous_class": is_ambiguous(a, b, c),
           "table_entry": ({"No": row["No"], "attribution": row["attribution"], "source_line": row["line"]} if row else None)}
    if (a, b, c) not in classes:
        raise Refuse(f"{label}: the form {abc} is not a reduced representative of a class of determinant {d}")
    if d in (3, 4, 7) and len(classes) == 1:
        res["identification"] = f"X_{d} (Takatsu Sec. 5: the unique singular K3 surface of discriminant {d})"
        res["determined_by_discriminant_alone"] = True
    else:
        res["identification"] = (f"the singular K3 surface with T = [{gram[0]},{gram[1]},{gram[2]}] (Shioda-Inose); "
                                 f"{len(classes)} class(es) share determinant {d}, so the determinant alone does not name it")
        res["determined_by_discriminant_alone"] = len(classes) == 1
    return res


def build(certs=CERTS, src_path=SRC):
    src = parse_source(src_path)
    dossier = json.loads((certs / "SELECTED_K3_DOSSIER.json").read_text())["families"]
    cm = json.loads((certs / "CM_POINTS_RHO20.json").read_text())["families"]["cooper_s7"]["locus_hits"]
    inose = json.loads((certs / "INOSE_MODEL_M7.json").read_text())["result"]["S6"]
    pts = [("cooper_s7, z = infinity (AM-8 pick)", tuple(dossier["cooper_s7"]["T_reduced_form_abc"])),
           ("cooper_s7, z = -1", tuple(cm["-1"][0]["T_X_reduced_form_abc"])),
           ("cooper_s7, z = 1/27", tuple(cm["1/27"][0]["T_X_reduced_form_abc"])),
           ("cooper_s10, z = infinity (AM-8 pick)", tuple(dossier["cooper_s10"]["T_reduced_form_abc"]))]
    ids = [identify(lbl, abc, src) for lbl, abc in pts]
    # consistency with the explicit model at z = infinity (forced by Shioda-Inose; NOT corroboration)
    ids[0]["explicit_model_consistency"] = {
        "INOSE_MODEL_M7.S6.both_zero_E_omega_x_E_omega": bool(inose.get("both_zero_E_omega_x_E_omega")),
        "takatsu_sec_5_1_uses": "E_3 x E_3 with E_3 = C/Z + Z omega (sigma(x,y) = (omega x, omega^2 y))",
        "reading": "consistent; forced by the Shioda-Inose structure, not independent corroboration"}
    if not ids[0]["explicit_model_consistency"]["INOSE_MODEL_M7.S6.both_zero_E_omega_x_E_omega"]:
        raise Refuse("the explicit model does not record sigma = pi = 0 (E_omega x E_omega) at z = infinity")
    # table agreement: the first and last points must be the Vinberg entries, z = -1 the Ujikawa entry
    t0, t1, t3 = ids[0]["table_entry"], ids[1]["table_entry"], ids[3]["table_entry"]
    if not (t0 and t0["No"] == 1 and "Vinberg" in t0["attribution"]):
        raise Refuse("s7 pick is not table No.1 / Vinberg")
    if not (t3 and t3["No"] == 2 and "Vinberg" in t3["attribution"]):
        raise Refuse("s10 pick is not table No.2 / Vinberg")
    if not (t1 and t1["No"] == 3 and "Ujikawa" in t1["attribution"]):
        raise Refuse("s7 z = -1 point is not table No.3 / Ujikawa")
    return {"checker": "checkers/check_selected_k3_identification.py", "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "date": "2026-10-08",
            "status": "IDENTIFICATION -- names the singular K3 surface of each point from its transcendental lattice; adopts nothing, ranks nothing",
            "source": {"file": "docs/literature/takatsu_1903.03054.txt", "pdf_sha256": SRC_SHA256, "paper": "T. Takatsu, arXiv:1903.03054v1",
                       "statements_found": {k: v for k, v in src.items() if k != "table"}, "table_rows_parsed": len(src["table"])},
            "shioda_inose_bijection": {"statement": "singular K3 surfaces up to C-isomorphism <-> positive-definite even binary forms up to SL2(Z)",
                                       "sources_read": ["Shioda MPIM 2007-137 (txt l.912)", "Kumar-Kuwata arXiv:1409.2931 Thm 8.1 (txt l.1779)", "Takatsu arXiv:1903.03054 (intro Theorem)"]},
            "points": ids,
            "global_floor": {
                "smallest_determinants_attained_by_any_positive_definite_even_binary_lattice": [d for d in range(1, 40) if reduced_classes(d)][:5],
                "picks_determinants": [ids[0]["determinant"], ids[3]["determinant"]],
                "reading": ("the s7 pick sits at the absolute minimum determinant and the s10 pick at the next value; s10 cannot reach the minimum because "
                            "A2_MEMBERSHIP records A2 absent from the s10 family. A lattice fact, forced by arithmetic -- not a preference, not corroboration, no cross-family ranking (items 8/9)")},
            "tiers": {"T_X_equals_v_perp": "B (Dolgachev 1996 sec. 7; Lefschetz (1,1))", "bijection_and_table": "L (sources read, lines recorded)",
                      "naming 'Vinberg's two most algebraic K3 surfaces'": "L (Schuett-Shioda l.3293 ties the name to the d = -3, -4 surfaces; Vinberg 1983 itself NOT fetched)"},
            "not_claimed": [
                "that the member of the family at that parameter value is a smooth fibre of a specific projective model: A2_MEMBERSHIP records only a point of the period domain",
                "anything about Vinberg's 1983 paper beyond what Takatsu's table and Schuett-Shioda l.3293 state (not fetched)",
                "that our E8^2 + A2 elliptic fibration of X_3 is one of Nishiyama's six fibrations for d = -3 (Nishiyama [63] not fetched; Schuett-Shioda l.3295 gives only the count)",
                "that the explicit-model E_omega x E_omega corroborates the identification: the agreement is forced by the Shioda-Inose structure",
                "any ranking of cooper_s7 over cooper_s10, any physical reading, any Kodaira label (ledger items 3, 4, 8, 9, 10)"],
            "generated_by": "Claude (Sonnet 5.5), Stream 2, 2026-10-08", "verified_by": "checkers/test_selected_k3_identification_controls.py", "reviewed_by": "N"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    d = build()
    for p in d["points"]:
        te = p["table_entry"]
        print(f"{p['point']}: T = {p['T_gram']}, det {p['determinant']}, classes of that determinant: {p['number_of_classes']} -> {p['identification']}"
              + (f"  [table No.{te['No']}: {te['attribution']}]" if te else "  [not in the pinned table]"))
    print(f"source: {d['source']['paper']}, {d['source']['table_rows_parsed']} table rows parsed from the pinned text")
    if a.emit:
        CERT.write_text(json.dumps(d, indent=2) + "\n")
        print("wrote", CERT)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refuse as e:
        print("REFUSED:", e)
        sys.exit(2)
