#!/usr/bin/env python3
"""Controls for scripts/extract_simulator_ledger_counts.py. The mirror file in refs/ is checked against the pinned source when
the source is present on this machine; the recount controls run on a synthetic ledger and need no external file.

  P1  a consistent synthetic ledger is recounted and accepted
  N1  a hand-edited AGREE count (stated != rows tally) is refused
  N2  a hand-edited per-track count is refused
  N3  n_from_memory != len(from_memory) is refused
  N4  an extra disputed row not in the stated count is refused
  N5  the committed mirror in refs/ carries the pinned source hash and (if the source is present) matches a fresh extraction
"""
import copy
import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import extract_simulator_ledger_counts as ex  # noqa: E402

fails = []


def check(name, cond, detail=""):
    print(f"  {'ok  ' if cond else 'FAIL'} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        fails.append(name)


def refused(fn):
    try:
        fn()
        return False
    except ex.Refuse:
        return True


rows = [{"final_status": "AGREE", "sealed_track": "A"}, {"final_status": "AGREE", "sealed_track": "A"},
        {"final_status": "NOT_COMPUTED", "sealed_track": "B"}]
good = {
    "header": "synthetic", "sealed": {"leanmaster_tag": "v0", "n_sealed_targets": 3},
    "comparison": {"counts": {"total_rows": 3, "final_status_counts": {"AGREE": 2, "NOT_COMPUTED": 1},
                              "by_sealed_track": {"A": {"AGREE": 2}, "B": {"NOT_COMPUTED": 1}},
                              "rows_with_2plus_routes": 0, "rows_with_2plus_routes_if_R2_rejected": 0}, "rows": rows},
    "declared_inputs": {"counts": {"A": 2, "B": 1}, "total": 3, "from_memory": ["x"], "n_from_memory": 1},
    "rigidity": {"counts": {"total_entries": 2, "self_claimed_rigid_family": 1, "reviewed_by_at_least_one_skeptic": 1,
                            "disputed": 1, "genuinely_rigid_confirmed": 0, "self_reported_unreviewed": 1},
                 "rows": [{"final_label": "RIGID"}, {"final_label": "DISPUTED: blind vs math"}]},
    "could_not_do": {"counts": {"A": 1}, "total": 1},
    "reverse": {"counts": {"total": 1, "holds_true": 1}, "rows": [{}]},
    "chain": {"counts": {"n_links": 1, "all_consistent": True, "n_independent_corroborations": 0,
                         "n_independent_corroborations_if_R2_rejected": 0}},
}
check("P1 consistent synthetic ledger accepted", not refused(lambda: ex.recount(good)))

bad = copy.deepcopy(good)
bad["comparison"]["counts"]["final_status_counts"]["AGREE"] = 3
check("N1 edited AGREE count refused", refused(lambda: ex.recount(bad)))
bad = copy.deepcopy(good)
bad["comparison"]["counts"]["by_sealed_track"]["A"]["AGREE"] = 1
check("N2 edited per-track count refused", refused(lambda: ex.recount(bad)))
bad = copy.deepcopy(good)
bad["declared_inputs"]["n_from_memory"] = 5
check("N3 from_memory mismatch refused", refused(lambda: ex.recount(bad)))
bad = copy.deepcopy(good)
bad["rigidity"]["rows"].append({"final_label": "DISPUTED: another"})
bad["rigidity"]["counts"]["total_entries"] = 3
check("N4 undeclared disputed row refused", refused(lambda: ex.recount(bad)))

mirror = ex.DEFAULT_OUT
m = json.loads(mirror.read_text()) if mirror.exists() else None
check("N5a mirror present with a pinned sha256", m is not None and len(m["source"]["sha256"]) == 64)
src = Path(os.environ.get("SIM_LEDGER_JSON", os.path.expanduser(
    "~/SocrateAI-Scientific-DualScaleSimulator/audit/k3t2_rigidity_v3/agreement_ledger_v3.json")))
if m is not None and src.exists():
    check("N5b the source file on this machine hashes to the pinned value", hashlib.sha256(src.read_bytes()).hexdigest() == m["source"]["sha256"])
    check("N5c a fresh extraction equals the committed counts", ex.build(src)["counts"] == m["counts"])
else:
    print("  skip N5b/N5c: source ledger not present on this machine")

print()
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all ledger-extraction controls behaved as required")
