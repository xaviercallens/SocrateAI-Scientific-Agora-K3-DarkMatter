#!/usr/bin/env python3
"""
aggregate_d3_verdicts.py — Merge individual sector verdicts into summary statistics.

Reads all D3_VERDICT_*.json files from output directory, computes pass rates,
lattice statistics, and generates D3_AGGREGATE_VERDICT.json for Gate E.

Usage:
  python3 scripts/aggregate_d3_verdicts.py \
    --input-dir data/d3_runs/ \
    --output data/d3_summary/D3_AGGREGATE_VERDICT.json
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


def aggregate_verdicts(input_dir):
    """
    Load all D3_VERDICT_*.json files and aggregate statistics.
    Returns: dict with summary metrics.
    """
    input_dir = Path(input_dir)
    verdict_files = sorted(input_dir.glob("D3_VERDICT_*.json"))

    if not verdict_files:
        print(f"ERROR: No verdict files found in {input_dir}")
        return None

    # Collections
    all_verdicts = []
    operator_stats = defaultdict(lambda: {"pass": 0, "fail": 0, "chi2": [], "rho": [], "t": []})

    for verdict_file in verdict_files:
        with open(verdict_file) as f:
            verdict = json.load(f)

        all_verdicts.append(verdict)

        sector_id = verdict.get("sector_id")
        operators = verdict.get("operators", {})

        for op_id, op_verdict in operators.items():
            if op_verdict.get("pass", False):
                operator_stats[op_id]["pass"] += 1
            else:
                operator_stats[op_id]["fail"] += 1

            operator_stats[op_id]["chi2"].append(op_verdict.get("chi2_lattice", np.nan))
            operator_stats[op_id]["rho"].append(op_verdict.get("picard_estimate", np.nan))
            operator_stats[op_id]["t"].append(op_verdict.get("transcendental_estimate", np.nan))

    # Compute summary statistics
    summary = {
        "timestamp": all_verdicts[0].get("timestamp") if all_verdicts else None,
        "total_sectors": len(verdict_files),
        "operators": {}
    }

    for op_id, stats in operator_stats.items():
        total = stats["pass"] + stats["fail"]
        pass_rate = stats["pass"] / total if total > 0 else 0

        chi2_vals = [x for x in stats["chi2"] if not np.isnan(x)]
        rho_vals = [x for x in stats["rho"] if not np.isnan(x)]
        t_vals = [x for x in stats["t"] if not np.isnan(x)]

        summary["operators"][op_id] = {
            "pass_count": stats["pass"],
            "fail_count": stats["fail"],
            "pass_rate": float(pass_rate),
            "pass_rate_pct": f"{pass_rate*100:.1f}%",
            "lattice_chi2": {
                "mean": float(np.mean(chi2_vals)) if chi2_vals else np.nan,
                "std": float(np.std(chi2_vals)) if chi2_vals else np.nan,
                "median": float(np.median(chi2_vals)) if chi2_vals else np.nan,
                "max": float(np.max(chi2_vals)) if chi2_vals else np.nan,
            },
            "picard_number": {
                "mean": float(np.mean(rho_vals)) if rho_vals else np.nan,
                "std": float(np.std(rho_vals)) if rho_vals else np.nan,
                "expected": 4.0,
                "deviation": float(np.mean(rho_vals) - 4.0) if rho_vals else np.nan,
            },
            "transcendental_rank": {
                "mean": float(np.mean(t_vals)) if t_vals else np.nan,
                "std": float(np.std(t_vals)) if t_vals else np.nan,
                "expected": 18.0,
                "deviation": float(np.mean(t_vals) - 18.0) if t_vals else np.nan,
            }
        }

    # Gate E decision logic (preliminary)
    gate_e_criteria = {
        "s7_pass_rate_ge_95": summary["operators"].get("L3_cooper_s7", {}).get("pass_rate", 0) >= 0.95,
        "s10_pass_rate_ge_95": summary["operators"].get("L3_cooper_s10", {}).get("pass_rate", 0) >= 0.95,
        "chi2_s7_lt_3sigma": summary["operators"].get("L3_cooper_s7", {}).get("lattice_chi2", {}).get("mean", 999) < 3.0,
    }
    summary["gate_e_preliminary"] = gate_e_criteria
    summary["gate_e_ready"] = all(gate_e_criteria.values())

    return summary


def main():
    ap = argparse.ArgumentParser(description="Aggregate D-3 sector verdicts")
    ap.add_argument("--input-dir", required=True, help="Input directory with D3_VERDICT_*.json files")
    ap.add_argument("--output", required=True, help="Output JSON file")
    args = ap.parse_args()

    summary = aggregate_verdicts(args.input_dir)
    if summary is None:
        sys.exit(1)

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"Aggregate verdict written: {output_path}")
    print(f"Total sectors: {summary['total_sectors']}")
    for op_id, op_stats in summary["operators"].items():
        print(f"  {op_id}: {op_stats['pass_rate_pct']} pass rate")

    sys.exit(0 if summary.get("gate_e_ready", False) else 1)


if __name__ == "__main__":
    main()
