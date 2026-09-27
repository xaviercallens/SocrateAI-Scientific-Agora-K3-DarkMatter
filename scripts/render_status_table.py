#!/usr/bin/env python3
"""
render_status_table.py -- regenerate K3_CRITERIA.md sec. 5 (Live Status Table)
from certificates only.

Written 2026-09-27 to close the open item K3_CRITERIA.md sec. 5 left in band on
2026-09-21: that section cited this script, which had never existed (phantom
artifact, standing rule 4), and its hand-kept table contradicted every
certificate on `main`, so the table was removed rather than edited.

What this script reads, and nothing else:
  * the sec. 1 Candidate Register of K3_CRITERIA.md (row ids, Cooper params, tier flags);
  * refs/recurrences_v1.json (to DERIVE which refs entry each register row is:
    the row's Cooper params (a,b,c,d) must reproduce the entry's recurrence
    coefficients exactly -- no register-id -> refs-key mapping is typed here);
  * data/certificates/*.json named in SOURCES below.

SOURCES is configuration, not data: for each (criterion, candidate) it names
WHICH certificate is the source of record and which field holds the verdict,
citing the record that makes that certificate the source. Every cell's text is
copied from, or computed from, a certificate field at run time. No verdict,
order, or lattice value appears in this file.

Fail-closed rules (each has a negative control in
checkers/test_render_status_table_controls.py):
  * a named source certificate that is missing           -> RenderError
  * a source carrying an in-band retraction               -> RenderError
    (top-level "RETRACTED" block, or a verdict/status starting "RETRACTED")
  * a source whose candidate field names another family   -> RenderError
  * an expected field missing from a source               -> RenderError
  * a C1 verdict PASS(N) whose N differs from order_checked -> RenderError
  * a register row matching zero or several refs entries  -> RenderError
  * a checker named by a source that is absent from checkers/ -> RenderError
A DRAFT lattice certificate renders as DRAFT (ADVISORY) -- neither a pass nor a
failure (K3_CRITERIA.md sec. 4).

Output is byte-stable: no dates, git stamps, checker versions or hashes reach
the table (the regression run refreshes certificate stamps, and K3_CRITERIA.md
is hash-pinned by its Stream 1 / Stream 3 mirrors).

Usage:
  python3 scripts/render_status_table.py            # rewrite sec. 5 between the markers
  python3 scripts/render_status_table.py --check    # exit 1 if sec. 5 is stale or hand-edited
  python3 scripts/render_status_table.py --stdout   # print the table only
Options --criteria-file / --certs-dir / --refs-file / --checkers-dir exist for
the controls (run against temp copies, never the real files).

Generated-by: Claude (Opus 5.5), Stream 2 | Verified-by: checkers/test_render_status_table_controls.py | Reviewed-by: N
"""
import argparse
import json
import re
import sys
from pathlib import Path

import sympy

REPO = Path(__file__).resolve().parent.parent

BEGIN = "<!-- BEGIN GENERATED STATUS TABLE: scripts/render_status_table.py -- do not edit by hand -->"
END = "<!-- END GENERATED STATUS TABLE -->"


class RenderError(Exception):
    pass


# ---------------------------------------------------------------------------
# Source map (configuration). Keys are refs-register names; the register row
# -> refs name link is derived at run time by derive_refs_key().
# ---------------------------------------------------------------------------
SOURCES = {
    # C1: K3_CRITERIA sec. 2 C1 names check_C1_mirror_integrality.py.
    "C1": {
        "kind": "c1",
        "checker": "check_C1_mirror_integrality.py",
        "certs": {
            "cooper_s7": "C1_mirror_integrality_cooper_s7.json",
            "cooper_s10": "C1_mirror_integrality_cooper_s10.json",
            "avs_sporadic3_s18": "C1_mirror_integrality_avs_sporadic3_s18.json",
        },
    },
    # C2 (AM-3): sec. 2 names the live/draft files explicitly. C2_cooper_s7_v4.json
    # still self-reports "LIVE v4" but was superseded by v5 (T0 D5'), and v5 by v6
    # (T0 D10', 2026-09-27; provenance only, identical values), hence v6 here.
    "C2": {
        "kind": "c2",
        "checker": "check_U1_lattice.py",
        "certs": {
            "cooper_s7": "C2_cooper_s7_v6.json",
            "cooper_s10": "C2_cooper_s10_v4_DRAFT.json",
        },
    },
    # C3: sec. 2 names checkers/check_C3_sym2.py, which does not exist in this repo.
    # The operator identity L3 = Sym^2(L2) with L2 exhibited is certified by
    # check_C3b_symsqrt.py; AM-2 (adopted, T0 D8') cites exactly these files as C3's
    # pass evidence (briefs/K3_CRITERIA_AMENDMENT_PROPOSAL_2026_09_21.md, AM-2).
    "C3": {
        "kind": "c3",
        "checker": "check_C3b_symsqrt.py",
        "certs": {
            "cooper_s7": "C3b_symsqrt_cooper_s7.json",
            "cooper_s10": "C3b_symsqrt_cooper_s10.json",
        },
    },
    # C3b (explicit Shioda-Inose map F, check_C3b_moduli_map.py): no certificate is
    # designated for any register candidate. The *__apery_zeta2 files are the
    # ruled-out partner test and must never render as a candidate's C3b status.
    "C3b": {"kind": "none", "certs": {}},
    # C4 / C5: definitions TBD-AT-FREEZE; no checker exists (criteria-checkers contract).
    "C4": {"kind": "tbd", "certs": {}},
    "C5": {"kind": "tbd", "certs": {}},
    # C6 (AM-1, T0 D7'): the CM-point table; rendered as a record, never a count.
    "C6": {
        "kind": "c6",
        "checker": "check_CM_points_rho20.py",
        "certs": {"cooper_s7": "CM_POINTS_RHO20.json", "cooper_s10": "CM_POINTS_RHO20.json"},
    },
    # T1 (AM-4): one Hauptmodul certificate per family, checker named in sec. 2 T1.
    "T1": {
        "kind": "t1",
        "certs": {
            "cooper_s7": ("HAUPTMODUL_S7_GAMMA07PLUS.json", "check_s7_hauptmodul_gamma07plus.py"),
            "cooper_s10": ("HAUPTMODUL_S10_GAMMA010STAR.json", "check_s10_hauptmodul_gamma010star.py"),
        },
    },
    # T3 (AM-4): per-candidate results block of the one T3 certificate.
    "T3": {
        "kind": "t3",
        "checker": "check_T3_level_consistency.py",
        "certs": {"cooper_s7": "T3_LEVEL_CONSISTENCY.json", "cooper_s10": "T3_LEVEL_CONSISTENCY.json"},
    },
}

SCORED_COLUMNS = ["C1", "C2", "C3", "C3b", "C4", "C5"]
UNSCORED_COLUMNS = ["C6", "T1", "T3"]


# ---------------------------------------------------------------------------
# Register + identity
# ---------------------------------------------------------------------------
def _int(s):
    return int(s.replace("−", "-"))


def parse_register(text):
    """Rows of the sec. 1 table. Returns list of dicts; struck rows are marked dropped."""
    m = re.search(r"^## 1\. Candidate Register\s*$(.*?)^## 2\.", text, re.S | re.M)
    if not m:
        raise RenderError("sec. 1 Candidate Register not found in criteria file")
    rows = []
    for line in m.group(1).splitlines():
        if not line.startswith("| K-") and not line.startswith("| ~~K-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rid = cells[0].replace("~~", "").strip()
        dropped = cells[0].startswith("~~") or "DROPPED" in cells[-1]
        pm = re.search(r"params \((\S+?),(\S+?),(\S+?),(\S+?)\)", cells[2])
        flags = re.findall(r"`([A-Z0-9_]+)`", cells[-1])
        rows.append({
            "id": rid,
            "dropped": dropped,
            "params": tuple(_int(x) for x in pm.groups()) if pm else None,
            "flags": flags,
        })
    if not rows:
        raise RenderError("sec. 1 Candidate Register has no rows")
    return rows


def _cooper_coefficients(a, b, c, d):
    """Refs-format coefficient lists [m^0..m^3] implied by the Cooper ansatz
    (n+1)^3 u(n+1) = (2n+1)(a n^2 + a n + b) u(n) - n(c n^2 + d) u(n-1),
    written as P0 u(m) + P1 u(m+1) + P2 u(m+2) = 0 with n = m + 1."""
    m = sympy.Symbol("m")
    N = m + 1
    p1 = sympy.Poly(sympy.expand(-(2 * N + 1) * (a * N**2 + a * N + b)), m)
    p0 = sympy.Poly(sympy.expand(c * N**3 + d * N), m)
    p2 = sympy.Poly(sympy.expand((m + 2) ** 3), m)
    return {k: [int(p.coeff_monomial(m**i)) for i in range(4)] for k, p in (("P0", p0), ("P1", p1), ("P2", p2))}


def derive_refs_key(params, refs):
    target = _cooper_coefficients(*params)
    hits = [k for k, e in refs.items() if e.get("recurrence_coefficients") == target]
    if len(hits) != 1:
        raise RenderError(f"register params {params} match {len(hits)} refs entries ({hits}); need exactly 1")
    return hits[0]


# ---------------------------------------------------------------------------
# Certificate access
# ---------------------------------------------------------------------------
def _field(d, path, src):
    cur = d
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            raise RenderError(f"{src}: expected field '{path}' missing")
        cur = cur[p]
    return cur


def load_cert(certs_dir, name):
    f = certs_dir / name
    if not f.exists():
        raise RenderError(f"source certificate {name} missing from {certs_dir}")
    d = json.loads(f.read_text())
    if "RETRACTED" in d:
        raise RenderError(f"{name}: carries an in-band RETRACTED block; never a source of record")
    for k in ("verdict", "status"):
        v = d.get(k)
        if isinstance(v, str) and v.strip().upper().startswith("RETRACTED"):
            raise RenderError(f"{name}: {k} is RETRACTED; never a source of record")
    return d


def _require_candidate(d, field, expected, src):
    got = _field(d, field, src)
    if got != expected:
        raise RenderError(f"{src}: {field} = {got!r}, but the row is {expected!r}")


def _require_checker(checkers_dir, name):
    if not (checkers_dir / name).exists():
        raise RenderError(f"checker {name} named as a source does not exist in {checkers_dir} (phantom)")


# ---------------------------------------------------------------------------
# Cell renderers -- text comes from certificate fields only
# ---------------------------------------------------------------------------
def cell_c1(d, key, src):
    _require_candidate(d, "candidate", key, src)
    verdict = _field(d, "verdict", src)
    order = _field(d, "order_checked", src)
    m = re.fullmatch(r"PASS\((\d+)\)", verdict)
    if m and int(m.group(1)) != order:
        raise RenderError(f"{src}: verdict {verdict} disagrees with order_checked {order}")
    return f"`{verdict}`"


def certified_monodromy_note(key, src, certs_dir):
    """Optional suffix for the C2 cell: WP-S2-CERT certificate, if present. It must
    name the same lattice certificate as its stage-3 reference; a present-but-open
    chain is rendered loudly, never hidden."""
    name = f"CERTIFIED_MONODROMY_L2_{key}.json"
    f = certs_dir / name
    if not f.exists():
        return ""
    d = load_cert(certs_dir, name)
    _require_candidate(d, "result.family", key, name)
    ref = _field(d, "result.stage3_from_certified_matrices.reference_certificate", name)
    if ref != src:
        raise RenderError(f"{name}: stage-3 reference is {ref!r}, but the C2 source is {src!r}")
    closed = _field(d, "result.chain_closed", name)
    if closed is not True:
        return f"; stage-2 monodromy certification OPEN (`{name}`)"
    return f"; stage-2 monodromy CERTIFIED, chain to this lattice closed (`{name}`)"


def cell_c2(d, key, src, certs_dir=None):
    _require_candidate(d, "operator", key, src)
    status = _field(d, "status", src)
    dval = _field(d, "derived.u_splitting.d", src)
    lattice = f"U⊕⟨{dval}⟩"
    head = status.split(" - ")[0].split(" ")[0].upper()
    note = certified_monodromy_note(key, src, certs_dir) if certs_dir is not None else ""
    if head == "LIVE":
        rec = _field(d, "t0_acceptance.record", src)
        return f"LIVE: T ≅ {lattice} (`{src}`; T0 acceptance `{rec}`){note}"
    if head == "DRAFT":
        return f"DRAFT (ADVISORY): {lattice} not certified; neither pass nor failure (`{src}`){note}"
    raise RenderError(f"{src}: status head {head!r} is neither LIVE nor DRAFT")


def cell_c3(d, key, src):
    _require_candidate(d, "bulk", key, src)
    verdict = _field(d, "verdict", src)
    _field(d, "validation.sym2_operator_identity_L3_eq_Sym2L2", src)
    return f"`{verdict}`"


def cell_c6(d, key, src):
    fam = _field(d, f"families.{key}", src)
    _require_candidate(fam, "candidate", key, src)
    viol = sum(len(_field(fam, k, src)) for k in (
        "same_z_different_form_violations", "same_z_different_norm_or_div_violations",
        "fricke_consistency_violations"))
    unrec = _field(fam, "unrecognised_rows", src)
    lat = _field(fam, "lattice_cert_status", src)
    flags = _field(fam, "flags", src)
    if viol or unrec:
        return f"CHECK FAILURES in `{src}` (violations {viol}, unrecognised rows {unrec})"
    tail = f"; flags {', '.join('`'+f+'`' for f in flags)} (ADVISORY)" if flags else ""
    return f"record in `{src}` (lattice source {lat}){tail}"


def cell_t1(d, key, src):
    verdict = _field(d, "verdict", src)
    held = _field(d, "orders.held_out_verified", src)
    return f"`{verdict}` (held-out to q^{max(held)})"


def cell_t3(d, key, src):
    r = _field(d, f"results.{key}", src)
    _require_candidate(r, "candidate", key, src)
    verdict = _field(r, "verdict", src)
    status = _field(r, "status", src)
    flags = _field(r, "open_flags", src)
    tail = f"; open flags {', '.join('`'+f+'`' for f in flags)}" if flags else ""
    return f"`{verdict}`, {status}{tail}"


CELL = {"c1": cell_c1, "c2": cell_c2, "c3": cell_c3, "c6": cell_c6, "t1": cell_t1, "t3": cell_t3}


def render_cell(col, key, certs_dir, checkers_dir):
    spec = SOURCES[col]
    kind = spec["kind"]
    if kind == "tbd":
        return "TBD-AT-FREEZE (no checker)"
    entry = spec["certs"].get(key)
    if entry is None:
        return "no certificate"
    name, checker = entry if isinstance(entry, tuple) else (entry, spec["checker"])
    _require_checker(checkers_dir, checker)
    d = load_cert(certs_dir, name)
    cert_checker = d.get("checker")
    if cert_checker is not None and Path(cert_checker).name != checker:
        raise RenderError(f"{name}: produced by {cert_checker}, source map expects {checker}")
    if kind == "c2":
        return cell_c2(d, key, name, certs_dir)
    return CELL[kind](d, key, name)


# ---------------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------------
def render_table(criteria_text, certs_dir, refs_file, checkers_dir):
    refs = json.loads(Path(refs_file).read_text())["sequences"]
    rows = parse_register(criteria_text)
    live = [r for r in rows if not r["dropped"]]
    keys = {}
    for r in live:
        if r["params"] is None:
            raise RenderError(f"register row {r['id']} has no Cooper params to derive its refs entry")
        keys[r["id"]] = derive_refs_key(r["params"], refs)

    def table(cols):
        out = ["| Register row (refs entry) | §1 pool flag | " + " | ".join(cols) + " |",
               "|---|---|" + "---|" * len(cols)]
        for r in live:
            tier = ", ".join(f"`{f}`" for f in r["flags"] if f.startswith("TIER_")) or "—"
            cells = [render_cell(c, keys[r["id"]], certs_dir, checkers_dir) for c in cols]
            out.append(f"| {r['id']} (`{keys[r['id']]}`) | {tier} | " + " | ".join(cells) + " |")
        return out

    lines = ["**Scored criteria** (proposed hard set per §4, TBD-AT-FREEZE: C1, C2, C3 · soft: C4, C5, "
             "weights TBD-AT-FREEZE · C3b gates S3-00 input). `no certificate` is neither a pass nor a "
             "failure. The §1 pool flag is the register's pool assignment in the narrow sense §1 states, "
             "not an epistemic tier.", ""]
    lines += table(SCORED_COLUMNS)
    lines += ["", "**Unscored — record and consistency gates** (C6, T1, T3; never scored, §4). "
              "C6 is rendered without counts: CM points are dense and a certificate lists a window, "
              "not a complete or ordered set.", ""]
    lines += table(UNSCORED_COLUMNS)
    dropped = [r["id"] for r in rows if r["dropped"]]
    if dropped:
        lines += ["", "Rows struck in the frozen §1 register (rendered as §1 states them, not adjudicated "
                  "here): " + ", ".join(f"`{x}`" for x in dropped) + "."]
    lines += ["", "Sources: **C3** is read from the `check_C3b_symsqrt.py` certificates, the checker §2 names "
              "since AM-7 (2026-09-27; AM-2 already cited them as C3's evidence). "
              "**C3b** has no certificate designated for any register row; the `*__apery_zeta2` "
              "certificates are a ruled-out partner test and are never read as a row's C3b status."]
    lines += ["", "Identity: each row's refs entry is the unique `refs/recurrences_v1.json` entry whose "
              "recurrence coefficients equal those implied by the row's Cooper params (exact, sympy)."]
    return "\n".join(lines) + "\n"


def splice(criteria_text, table):
    if criteria_text.count(BEGIN) != 1 or criteria_text.count(END) != 1:
        raise RenderError("criteria file must contain exactly one BEGIN and one END marker in sec. 5")
    pre, rest = criteria_text.split(BEGIN)
    _, post = rest.split(END)
    return pre + BEGIN + "\n" + table + END + post


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--criteria-file", default=REPO / "K3_CRITERIA.md", type=Path)
    ap.add_argument("--certs-dir", default=REPO / "data" / "certificates", type=Path)
    ap.add_argument("--refs-file", default=REPO / "refs" / "recurrences_v1.json", type=Path)
    ap.add_argument("--checkers-dir", default=REPO / "checkers", type=Path)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true")
    g.add_argument("--stdout", action="store_true")
    a = ap.parse_args(argv)
    text = a.criteria_file.read_text()
    try:
        table = render_table(text, a.certs_dir, a.refs_file, a.checkers_dir)
        if a.stdout:
            sys.stdout.write(table)
            return 0
        new = splice(text, table)
    except RenderError as e:
        print(f"RENDER REFUSED: {e}", file=sys.stderr)
        return 2
    if a.check:
        if new != text:
            print("STALE: K3_CRITERIA.md sec. 5 differs from the certificates "
                  "(hand edit or un-rendered change). Re-run without --check.", file=sys.stderr)
            return 1
        print("OK: sec. 5 matches the certificates")
        return 0
    if new != text:
        a.criteria_file.write_text(new)
        print(f"wrote sec. 5 of {a.criteria_file}")
    else:
        print("sec. 5 already current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
