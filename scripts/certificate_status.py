#!/usr/bin/env python3
"""
certificate_status.py — mechanical status table over data/certificates/*.json.

Does NOT read or require K3_CRITERIA.md (which VISION.md/EXECUTION_PLAN.md cite as
"frozen" but which does not exist in this repo as of 2026-08-01 — see
briefs/LOW_TIER_QUEUE_2026_08_01.md item A-S2-1). This script only lists what
certificates exist and their self-reported fields; it applies no criteria, no
weighting, and makes no selection or ranking judgment. Regenerating the actual
frozen criteria table is a T0/T1 design task, not this script's job.

Every field printed is read directly from the certificate JSON at run time —
nothing is hardcoded or recalled from memory (CLAUDE.md standing rule 5,
"numbers are computed, never typed").

Usage:
  python3 scripts/certificate_status.py              # table to stdout
  python3 scripts/certificate_status.py --json out.json   # also write machine-readable form
"""

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CERT_DIR = REPO / "data" / "certificates"


def load_all():
    rows = []
    for f in sorted(CERT_DIR.glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            rows.append({
                "file": f.name, "certificate": "PARSE_ERROR", "operator": "",
                "tier": "", "status": str(e), "date": "",
            })
            continue
        rows.append({
            "file": f.name,
            "certificate": d.get("certificate", d.get("criterion", "")),
            "operator": d.get("operator", d.get("candidate", "")),
            "tier": d.get("tier", ""),
            "status": _short_status(d.get("status", d.get("verdict", ""))),
            "date": d.get("date", ""),
        })
    return rows


def _short_status(s):
    """Certificates carry long prose status blocks; keep only the leading
    classification word(s) for table display, not the full paragraph."""
    if not isinstance(s, str):
        return str(s)
    for sep in (" - ", ". ", ", "):
        if sep in s:
            return s.split(sep, 1)[0]
    return s[:60]


def render_table(rows):
    cols = ["file", "certificate", "operator", "tier", "status", "date"]
    widths = {c: max(len(c), max((len(str(r[c])) for r in rows), default=0)) for c in cols}
    lines = []
    header = "  ".join(c.ljust(widths[c]) for c in cols)
    lines.append(header)
    lines.append("  ".join("-" * widths[c] for c in cols))
    for r in rows:
        lines.append("  ".join(str(r[c]).ljust(widths[c]) for c in cols))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None, help="also write machine-readable JSON to this path")
    args = ap.parse_args()

    rows = load_all()
    print(f"{len(rows)} certificates in {CERT_DIR.relative_to(REPO)}\n")
    print(render_table(rows))

    n_draft = sum(1 for r in rows if "DRAFT" in r["status"].upper())
    n_live = sum(1 for r in rows if r["status"].upper() in ("LIVE", "") and "DRAFT" not in r["status"].upper())
    n_error = sum(1 for r in rows if r["certificate"] == "PARSE_ERROR")
    print(f"\n{n_draft} DRAFT, {n_error} PARSE_ERROR, {len(rows) - n_draft - n_error} other "
          f"(status string not classified as DRAFT — check status column, this script does "
          f"not assume LIVE from absence of 'DRAFT')")

    if args.json:
        out = Path(args.json)
        out.write_text(json.dumps(rows, indent=2))
        print(f"\nWrote {out}")

    return 1 if n_error else 0


if __name__ == "__main__":
    sys.exit(main())
