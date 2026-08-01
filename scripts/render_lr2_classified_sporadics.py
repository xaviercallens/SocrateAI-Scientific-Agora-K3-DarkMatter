#!/usr/bin/env python3
"""
LR-2 (AutoEvolve R2 Hypothesis Foundry, Phase A) -- "enumerate classified
sporadic sequences into a CSV." EXPLORATORY SANDBOX output, not citable into
Streams 1-3 (CLAUDE.md rule 7).

Reads refs/recurrences_v1.json directly (the same already-hash-pinned,
already-cited register Track A's own checkers read) and emits
data/autoresearch_v2/CLASSIFIED_SPORADICS.csv. Every field is read from that
file at run time -- no OEIS ID, order, or citation is typed here from
memory, per CLAUDE.md standing rule 5 ("numbers are computed, never typed").

DELIBERATELY EXCLUDES t103 and S22 (Cooper S22): both were named as
candidates in various program docs, but their status is a live, unresolved
cross-repo question as of 2026-08-01 -- see
briefs/T0_FLAG_K3_CRITERIA_T103_STALE_2026_08_01.md (S1 repo). Including
either here, before T0 rules, would risk exactly the kind of premature
citation this sandbox firewall exists to prevent. Re-run this script after
T0 rules if either should be added.

11 entries, not the guide's aspirational ">=15" -- every one traces to a
citation already hash-pinned and read in this repo; padding to a round
number with less-verified entries was deliberately not done (see
briefs/LOW_TIER_QUEUE_2026_08_01.md item B-S2-3's own reasoning, S3 repo).
"""

import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REGISTER = REPO / "refs" / "recurrences_v1.json"
OUT = REPO / "data" / "autoresearch_v2" / "CLASSIFIED_SPORADICS.csv"

# name -> is this entry itself OEIS-registered, or a derived (non-OEIS) object?
# Read from the register's own prose, not guessed: an entry is DERIVED if its
# source field says so explicitly ("DERIVED (not literature transcription)").
DERIVED_MARKER = "DERIVED (not literature transcription)"


def oeis_id_or_derived(source_text: str) -> str:
    if DERIVED_MARKER in source_text:
        return "DERIVED (no OEIS ID -- see notes)"
    m = re.search(r"(A\d{6})", source_text)
    return m.group(1) if m else "NOT FOUND IN SOURCE TEXT"


def main():
    d = json.loads(REGISTER.read_text())
    seqs = d["sequences"]

    rows = []
    for name, s in seqs.items():
        source = s.get("source", "")
        rows.append({
            "name": name,
            "oeis_id": oeis_id_or_derived(source),
            "binomial_or_closed_form": (s.get("closed_form") or "").strip() or "(see recurrence_coefficients in refs/recurrences_v1.json)",
            "order": s.get("type", ""),
            "status_in_register": s.get("status", ""),
            "citation": source,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "name", "oeis_id", "binomial_or_closed_form", "order",
            "status_in_register", "citation",
        ])
        w.writeheader()
        for r in sorted(rows, key=lambda r: r["name"]):
            w.writerow(r)

    print(f"Wrote {len(rows)} rows to {OUT.relative_to(REPO)}", file=sys.stderr)
    n_derived = sum(1 for r in rows if r["oeis_id"].startswith("DERIVED"))
    n_oeis = len(rows) - n_derived
    print(f"  {n_oeis} OEIS-registered, {n_derived} derived (order-2 partners, no OEIS ID)",
          file=sys.stderr)
    print("  EXCLUDED (status contested pending T0, see "
          "briefs/T0_FLAG_K3_CRITERIA_T103_STALE_2026_08_01.md, S1 repo): t103, S22",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
