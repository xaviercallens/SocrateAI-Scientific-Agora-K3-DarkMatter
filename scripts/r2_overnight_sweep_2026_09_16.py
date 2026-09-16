#!/usr/bin/env python3
"""AutoEvolve R2 — overnight widened sieve (2026-09-16).

EXPLORATORY SANDBOX (S3 CLAUDE.md rule 7; S2 AutoEvolve R2 Hypothesis Foundry track).
Nothing produced here may be cited in Streams 1–3. No candidate is promoted to
candidate_pool.yaml; no HUMAN/T0 gate has seen any output.

Reuses the pre-existing, UNMODIFIED classifier in scripts/autoresearch_v2_phase_a_scan.py
(exact arithmetic, two-prime modular pre-screen, exact Fraction solve, exact held-out check).

Stage 1 — new grid points (not covered by LR-3 scan2/scan3) at the scanner's default window
          (ODE rho<=4, delta<=8; shift r<=3, d<=4; n_max=110):
    3-factor  sum_k C(n,k)^A C(n+k,k)^B C(2k,k)^C,             (A,B,C) in [0,4]^3
    4-factor  sum_k C(n,k)^A C(n+k,k)^B C(2k,k)^C C(2n-2k,n-k)^D, (A,B,C) in [0,2]^3, D in [1,2]
Stage 2 — every case (stage 1 AND LR-3's phase_a_scan2/scan3) that returned
          "no ODE found in search window", re-run with ODE rho<=6, delta<=16 at n_max=200
          (>= 40 held-out terms for the largest window). A stage-2 miss is still only
          "not found in window", never a negative.

Flags recorded, not filtered:
  - partial_sum_form: all n-dependent exponents are 0 (summand independent of n; the A079727 pattern under
    T0 HOLD 2026-09-16 — a partial sum of a single-index sequence, likely not new geometry)
  - reduces_to_2factor / reduces_to_3factor: a zero exponent collapses the family

Output (JSONL, one line per finished case, appended before any print; resumable):
    data/autoresearch_v2/overnight_sweep_2026_09_16/stage{1,2}.jsonl
    data/autoresearch_v2/overnight_sweep_2026_09_16/summary.json  (written at the end)
"""
import json
import math
import os
import signal
import sys
import time
from itertools import product
from multiprocessing import Pool

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPTS_DIR)
sys.path.insert(0, SCRIPTS_DIR)
from autoresearch_v2_phase_a_scan import (find_ode, find_shift_recurrence,  # noqa: E402
                                          seq_2factor, seq_3factor)

OUT_DIR = os.path.join(REPO_ROOT, "data", "autoresearch_v2", "overnight_sweep_2026_09_16")
LR3_SCAN2 = os.path.join(REPO_ROOT, "data", "autoresearch_v2", "phase_a_scan2.json")
LR3_SCAN3 = os.path.join(REPO_ROOT, "data", "autoresearch_v2", "phase_a_scan3.json")
LABEL = "EXPLORATORY SANDBOX — not citable in Streams 1-3; not a candidate-pool promotion"
CASE_TIMEOUT_S = 3 * 3600
WORKERS = int(os.environ.get("SWEEP_WORKERS", "6"))

STAGE = {
    1: {"nmax": 110, "rho_max": 4, "delta_max": 8},
    2: {"nmax": 200, "rho_max": 6, "delta_max": 16},
}
GEOM = {1: "rational", 2: "elliptic (weight 2)", 3: "K3-type (weight 3)", 4: "CY3-type (weight 4)"}


def seq_4factor(A, B, C, D, nmax):
    return [sum(math.comb(n, k) ** A * math.comb(n + k, k) ** B * math.comb(2 * k, k) ** C
                * math.comb(2 * n - 2 * k, n - k) ** D for k in range(n + 1))
            for n in range(nmax + 1)]


def terms(case, nmax):
    fam, e = case["family"], case["exps"]
    if fam == "2f":
        return seq_2factor(*e, nmax)
    if fam == "3f":
        return seq_3factor(*e, nmax)
    return seq_4factor(*e, nmax)


def case_id(fam, e):
    return f"{fam}_" + "_".join(str(x) for x in e)


def flags(fam, e):
    # summand independent of n only if every n-dependent factor has exponent 0
    # (4-factor: C(2n-2k,n-k)^D with D>=1 always depends on n)
    n_dep = list(e[:2]) + (list(e[3:4]) if fam == "4f" else [])
    f = {"partial_sum_form": all(x == 0 for x in n_dep)}
    if fam == "3f" and e[2] == 0:
        f["reduces_to_2factor"] = True
    if fam == "4f" and e[2] == 0:
        f["reduces_to_3factor_without_C2k"] = True
    return f


def _alarm(signum, frame):
    raise TimeoutError


def run_case(args):
    case, stage = args
    cfg = STAGE[stage]
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(CASE_TIMEOUT_S)
    t0 = time.time()
    rec = {"id": case["id"], "family": case["family"], "exps": case["exps"], "stage": stage,
           "window": cfg, "flags": flags(case["family"], case["exps"]), "label": LABEL}
    try:
        u = terms(case, cfg["nmax"])
        if all(x == 0 for x in u):
            rec["status"] = "zero_sequence"
        else:
            rec["first_terms"] = [str(x) for x in u[:10]]
            ode = find_ode(u, cfg["nmax"], rho_max=cfg["rho_max"], delta_max=cfg["delta_max"])
            rec["ode"] = ode
            rec["geometry_by_ode"] = (GEOM.get(ode["ode_order"], "higher") if ode
                                      else "no ODE found in search window")
            if stage == 1:
                sh = find_shift_recurrence(u, cfg["nmax"])
                rec["shift"] = ({k: sh[k] for k in ("order", "degree", "held_out_terms",
                                                    "held_out_pass")} if sh else None)
            rec["status"] = "done"
    except TimeoutError:
        rec["status"] = f"timeout_{CASE_TIMEOUT_S}s"
    except Exception as exc:  # recorded, never swallowed silently
        rec["status"] = f"error: {type(exc).__name__}: {exc}"
    finally:
        signal.alarm(0)
    rec["seconds"] = round(time.time() - t0, 2)
    return rec


def done_ids(path):
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            out[r["id"]] = r
    return out


def run_stage(stage, cases, path):
    finished = done_ids(path)
    todo = [c for c in cases if c["id"] not in finished]
    print(f"[stage {stage}] {len(cases)} cases, {len(finished)} already done, {len(todo)} to run",
          flush=True)
    with Pool(WORKERS) as pool, open(path, "a") as f:
        for rec in pool.imap_unordered(run_case, [(c, stage) for c in todo]):
            f.write(json.dumps(rec, default=str) + "\n")
            f.flush()
            finished[rec["id"]] = rec
            o = rec.get("ode")
            print(f"[stage {stage}] {rec['id']:16} {rec['status']:8} "
                  f"ode={o and (o['ode_order'], o['ode_degree'])} {rec['seconds']}s", flush=True)
    return finished


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    # Known-answer controls at BOTH windows; abort if the classifier does not discriminate.
    # positive: Apery zeta(3) A005259 = S(2,2) and T103 = T(1,0,3) are order 3;
    # negative: S(1,2) = A112019 is order 2 (LR-1 / S12_S21_DEFINITION_ALIGNMENT.md).
    controls = [({"id": "ctl_S22", "family": "2f", "exps": [2, 2]}, 3),
                ({"id": "ctl_T103", "family": "3f", "exps": [1, 0, 3]}, 3),
                ({"id": "ctl_S12", "family": "2f", "exps": [1, 2]}, 2)]
    ctl_records = []
    for stage in (1, 2):
        for case, want in controls:
            r = run_case((case, stage))
            got = (r.get("ode") or {}).get("ode_order")
            r["control_expected_order"], r["control_pass"] = want, got == want
            ctl_records.append(r)
            print(f"[control] stage {stage} {case['id']}: order {got} (want {want}) "
                  f"{'PASS' if got == want else 'FAIL'}", flush=True)
    with open(os.path.join(OUT_DIR, "controls.json"), "w") as f:
        json.dump(ctl_records, f, indent=1, default=str)
    if not all(r["control_pass"] for r in ctl_records):
        print("[abort] control failure — sweep not run", flush=True)
        return 1
    stage1 = []
    for a, b, c in product(range(5), repeat=3):
        if (a, b, c) == (0, 0, 0):
            continue
        if a <= 3 and b <= 3 and 1 <= c <= 3:
            continue  # covered by LR-3 scan3
        if c == 0 and a >= 1 and b >= 1:
            continue  # = 2-factor S(a,b), covered by LR-3 scan2 ([1,8]^2)
        stage1.append({"id": case_id("3f", (a, b, c)), "family": "3f", "exps": [a, b, c]})
    for a, b, c in product(range(3), repeat=3):
        for d in (1, 2):
            stage1.append({"id": case_id("4f", (a, b, c, d)), "family": "4f",
                           "exps": [a, b, c, d]})

    r1 = run_stage(1, stage1, os.path.join(OUT_DIR, "stage1.jsonl"))

    stage2 = [{"id": r["id"], "family": r["family"], "exps": r["exps"]}
              for r in r1.values() if r.get("status") == "done" and not r.get("ode")]
    for path, fam, keys in ((LR3_SCAN2, "2f", ("A", "B")), (LR3_SCAN3, "3f", ("A", "B", "C"))):
        with open(path) as f:
            for r in json.load(f)["results"]:
                if not r.get("ode"):
                    e = [r[k] for k in keys]
                    stage2.append({"id": case_id(fam, e), "family": fam, "exps": e})
    # cheapest first so partial results land early
    stage2.sort(key=lambda c: sum(c["exps"]))
    r2 = run_stage(2, stage2, os.path.join(OUT_DIR, "stage2.jsonl"))

    def survivors(rs):
        return sorted((r for r in rs.values() if (r.get("ode") or {}).get("ode_order") == 3),
                      key=lambda r: (r["ode"]["ode_degree"], sum(r["exps"])))

    summary = {
        "label": LABEL,
        "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "windows": STAGE,
        "stage1_cases": len(r1), "stage2_cases": len(r2),
        "status_counts": {s: sum(1 for r in list(r1.values()) + list(r2.values())
                                 if r["status"] == s)
                          for s in {r["status"] for r in list(r1.values()) + list(r2.values())}},
        "order3_survivors": [
            {"id": r["id"], "stage": r["stage"], "exps": r["exps"], "ode": r["ode"],
             "flags": r["flags"], "first_terms": r.get("first_terms")}
            for r in survivors(r1) + survivors(r2)],
        "not_done": "OEIS identification, G1-2 Weil screen, G1-3, G1-4 — none run; "
                    "morning triage only",
    }
    with open(os.path.join(OUT_DIR, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1, default=str)
    print(f"[done] {len(summary['order3_survivors'])} order-3 survivors; summary.json written",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
