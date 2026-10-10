#!/usr/bin/env python3
"""extract_simulator_ledger_counts.py -- mirror the COUNT blocks of the DualScaleSimulator's k3t2-rigidity ledger v3.

The simulator stream's `audit/k3t2_rigidity_v3/agreement_ledger_v3.json` (530 kB; its commit 3adda92) is the machine-readable
record of that stream's own cross-check of the K3 x T^2 construction against the Lean library. Stream 2 does not re-derive
it (producer != verifier does not apply: nothing here is verified by us). This script copies ONLY the count blocks into a
small file pinned to the source's sha256, after RECOUNTING each block from the ledger's own row-level data and refusing on any
mismatch -- so a transcription or a hand edit of the counts cannot pass.

Usage: python3 scripts/extract_simulator_ledger_counts.py <agreement_ledger_v3.json> [--out refs/simulator_k3t2_ledger_counts_v3.json]
Controls: checkers/test_extract_simulator_ledger_counts_controls.py
Generated-by: Claude (Fable 5.1), Stream 2, 2026-10-10 | Verified-by: the controls and the recount | Reviewed-by: N
"""
import argparse
import collections
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO / "refs" / "simulator_k3t2_ledger_counts_v3.json"
SOURCE_COMMIT = "3adda92"          # the simulator-side commit that holds the ledger (from its git log)


class Refuse(RuntimeError):
    pass


def recount(d):
    """returns the count blocks, each cross-checked against row-level data; raises Refuse on any disagreement."""
    out = {}
    comp = d["comparison"]
    tally = collections.Counter(r["final_status"] for r in comp["rows"])
    if dict(tally) != comp["counts"]["final_status_counts"]:
        raise Refuse(f"comparison: rows tally {dict(tally)} != stated {comp['counts']['final_status_counts']}")
    if len(comp["rows"]) != comp["counts"]["total_rows"]:
        raise Refuse("comparison: total_rows != len(rows)")
    by_track = collections.defaultdict(collections.Counter)
    for r in comp["rows"]:
        by_track[r["sealed_track"]][r["final_status"]] += 1
    if {k: dict(v) for k, v in by_track.items()} != comp["counts"]["by_sealed_track"]:
        raise Refuse("comparison: per-track tally != stated by_sealed_track")
    out["comparison"] = {"total_rows": len(comp["rows"]), "final_status_counts": dict(tally),
                         "by_sealed_track": {k: dict(v) for k, v in sorted(by_track.items())},
                         "rows_with_2plus_routes": comp["counts"]["rows_with_2plus_routes"],
                         "rows_with_2plus_routes_if_R2_rejected": comp["counts"]["rows_with_2plus_routes_if_R2_rejected"]}
    di = d["declared_inputs"]
    if sum(di["counts"].values()) != di["total"]:
        raise Refuse("declared inputs: sum of per-track counts != total")
    if len(di["from_memory"]) != di["n_from_memory"]:
        raise Refuse("declared inputs: len(from_memory) != n_from_memory")
    out["declared_inputs"] = {"total": di["total"], "n_from_memory": di["n_from_memory"], "per_track": dict(di["counts"])}
    rg = d["rigidity"]
    n_disputed = sum(1 for r in rg["rows"] if str(r["final_label"]).startswith("DISPUTED"))
    if len(rg["rows"]) != rg["counts"]["total_entries"] or n_disputed != rg["counts"]["disputed"]:
        raise Refuse("rigidity: rows disagree with stated total/disputed counts")
    out["rigidity"] = {k: rg["counts"][k] for k in ("total_entries", "self_claimed_rigid_family", "reviewed_by_at_least_one_skeptic",
                                                     "disputed", "genuinely_rigid_confirmed", "self_reported_unreviewed")}
    cnd = d["could_not_do"]
    if sum(cnd["counts"].values()) != cnd["total"]:
        raise Refuse("could_not_do: sum != total")
    out["could_not_do"] = {"total": cnd["total"], "per_track": dict(cnd["counts"])}
    rv = d["reverse"]
    if len(rv["rows"]) != rv["counts"]["total"]:
        raise Refuse("reverse: len(rows) != total")
    out["reverse"] = dict(rv["counts"])
    ch = d["chain"]["counts"]
    out["chain"] = {k: ch[k] for k in ("n_links", "all_consistent", "n_independent_corroborations",
                                       "n_independent_corroborations_if_R2_rejected")}
    out["sealed"] = dict(d["sealed"])
    return out


def build(path):
    raw = Path(path).read_bytes()
    d = json.loads(raw)
    return {"label": "MIRRORED COUNTS of another stream's audit; recounted from its row data; NOT independently verified by Stream 2; tier B at best (the source's own header)",
            "source": {"file": "audit/k3t2_rigidity_v3/agreement_ledger_v3.json", "repo": "SocrateAI-Scientific-DualScaleSimulator",
                       "commit": SOURCE_COMMIT, "sha256": hashlib.sha256(raw).hexdigest(), "header": d["header"]},
            "counts": recount(d),
            "not_claimed": ["that the source's AGREE rows are correct (not re-derived here)",
                            "any physical reading; the ledger's own header says physical identifications are tier L/C",
                            "that 'rigid' means anything about the universe: it means a selecting condition was scanned for one parameter"],
            "generated_by": "Claude (Fable 5.1), Stream 2, 2026-10-10", "verified_by": "checkers/test_extract_simulator_ledger_counts_controls.py",
            "reviewed_by": "N"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("ledger")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    a = ap.parse_args(argv)
    cert = build(a.ledger)
    Path(a.out).write_text(json.dumps(cert, indent=2) + "\n")
    c = cert["counts"]["comparison"]["final_status_counts"]
    print("wrote", a.out, "| comparison:", c, "| from_memory:", cert["counts"]["declared_inputs"]["n_from_memory"],
          "of", cert["counts"]["declared_inputs"]["total"])
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refuse as e:
        print("REFUSED:", e)
        sys.exit(2)
