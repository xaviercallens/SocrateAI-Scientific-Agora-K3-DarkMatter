#!/usr/bin/env python3
"""Phase 8.B — G1-1 ODE-order classifier on 13 candidates."""

import json
import math
from scripts.autoresearch_v2_phase_a_scan import classify, seq_2factor, seq_3factor, seq_apery3, seq_domb

nmax = 110

# Map of (candidate_id) → (generator_fn, params_dict)
candidates = {
    # K3-type controls & verified
    "apery_zeta3": (lambda n: seq_apery3(n), {}),
    "apery_zeta2_s21": (lambda n: seq_2factor(2, 1, n), {}),
    "s12_v1_primary": (lambda n: seq_2factor(1, 2, n), {}),
    "domb": (lambda n: seq_domb(n), {}),
    "t003": (lambda n: [sum(math.comb(2*k, k)**3 for k in range(i+1)) for i in range(n+1)], {}),
    "t011": (lambda n: [sum(math.comb(n+k, k) * math.comb(2*k, k) for k in range(i+1)) for i in range(n+1)], {}),
    "t103": (lambda n: [sum(math.comb(i, k) * math.comb(2*k, k)**3 for k in range(i+1)) for i in range(n+1)], {}),
    "t112": (lambda n: [sum(math.comb(i, k) * math.comb(i+k, k) * math.comb(2*k, k)**2 for k in range(i+1)) for i in range(n+1)], {}),
}

results = {}
for cid, (gen_fn, _) in candidates.items():
    u = gen_fn(nmax)
    result = classify(cid, u, nmax)
    results[cid] = result
    ode_order = result["ode"]["ode_order"] if result["ode"] else None
    print(f"{cid:20} → ODE order {ode_order} (geometry: {result['geometry_by_ode']})")

with open("data/autoresearch_v2/g1_order_classification.json", "w") as f:
    json.dump({"date": "2026-07-14", "n_max": nmax, "results": results}, f, indent=1)
print("\n✓ output: data/autoresearch_v2/g1_order_classification.json")
