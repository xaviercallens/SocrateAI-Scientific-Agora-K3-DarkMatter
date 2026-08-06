#!/usr/bin/env python3
"""
auto_evolve_k3_selection.py — Stream 2 AutoEvolve K3 candidate generator,
gate battery, ranking, and elliptic-EFT alignment driver.

Git history: replaces scripts/auto_evolve_k3_selection_stub_tobeupdate.py

Stages (per briefs/STREAM2_AUTOEVOLVE_HAIKU_PLAN.md):
  AE-2: deterministic evolutionary generator over binomial-sum families
  AE-3: gate battery (G1-1 ODE order, G1-3 mirror-map integrality, C3b hard gate)
  AE-4: ranking per K3_CRITERIA_INTERFACE.md (math 0.60, empirical null, theory 0.10)
  AE-5: C3b symmetric-square-root extraction for ranked K3 survivors

Execution is exact-arithmetic and deterministic; the evaluator, not a neural
network, is the source of truth.
"""

import hashlib
import json
import math
import os
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

import sympy as sp

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(REPO_ROOT))

from ae_anchor_fingerprints import (
    mirror_fingerprint as _mirror_fingerprint,
    run_c3b as _run_c3b,
    run_c3b_generated as _run_c3b_generated,
    q_coeffs_are_integral,
)
from autoresearch_v2_phase_a_scan import classify
from autoresearch_v2_pool import POOL, OEIS_FIRST_TERMS, verify_terms

OUT_DIR = REPO_ROOT / "data" / "autoresearch_v2"
OUT_DIR.mkdir(parents=True, exist_ok=True)
CERT_DIR = REPO_ROOT / "data" / "certificates" / "ae"
CERT_DIR.mkdir(parents=True, exist_ok=True)

NMAX = 110
N_MIRROR = 31


# ─────────────────────────────────────────────────────────── term generators

def gen_2factor(A, B, nmax):
    return [sum(math.comb(n, k) ** A * math.comb(n + k, k) ** B
                for k in range(n + 1)) for n in range(nmax + 1)]


def gen_3factor(A, B, C, nmax):
    return [sum(math.comb(n, k) ** A * math.comb(n + k, k) ** B
                * math.comb(2 * k, k) ** C for k in range(n + 1))
            for n in range(nmax + 1)]


def genome_id(family, exponents):
    exp_str = "".join(str(e) for e in exponents)
    return f"{family}_{exp_str}"


def generate_search_space():
    """Deterministic, bounded search space for v1.

    2-factor (A,B) in [1,5]^2 and 3-factor (A,B,C) in [1,3]^3.
    Budget: 52 genome evaluations + anchors; well under the 400 cap.
    """
    genomes = []
    for A, B in product(range(1, 6), repeat=2):
        genomes.append(("2factor", (A, B)))
    for A, B, C in product(range(1, 4), repeat=3):
        genomes.append(("3factor", (A, B, C)))
    return genomes


# ───────────────────────────────────────────────────────────── gate battery

def gate_battery(cid, family, exponents, u, anchors):
    """Run G1-1, G1-3, and C3b on a candidate. Return certificate dict."""
    result = {
        "id": cid,
        "family": family,
        "exponents": exponents,
        "first_terms": u[:8],
    }

    cls = classify(cid, u, NMAX)
    result["classify"] = cls
    ode = cls.get("ode") or {}
    result["g1_1"] = {
        "ode_order": ode.get("ode_order"),
        "ode_degree": ode.get("ode_degree"),
        "held_out_terms": ode.get("held_out_terms"),
        "held_out_pass": ode.get("held_out_pass"),
    }

    if ode.get("ode_order") != 3:
        result["g1_3"] = {"verdict": "SKIPPED_NOT_ORDER3"}
        result["c3b"] = {"verdict": "SKIPPED_NOT_ORDER3"}
        result["status"] = "REJECTED_G1_1"
        result["score_math_only"] = 0
        return result

    mirror = _mirror_fingerprint(cid, u)
    if mirror is None:
        result["g1_3"] = {"verdict": "ERROR_MUM"}
        result["c3b"] = {"verdict": "SKIPPED_MIRROR_ERROR"}
        result["status"] = "REJECTED_G1_3_ERROR"
        result["score_math_only"] = 0
        return result

    result["g1_3"] = {
        "q2": mirror["q2"],
        "integral": mirror["integral"],
        "q_coeffs": mirror["q_coeffs"],
        "verdict": "PASS_INTEGRAL" if mirror["integral"] else "FAIL_NON_INTEGRAL",
    }

    if not mirror["integral"]:
        result["c3b"] = {"verdict": "SKIPPED_G1_3_FAIL"}
        result["status"] = "REJECTED_G1_3"
        result["score_math_only"] = 0
        return result

    # C3b hard gate (anchors use refs; generated genomes use derived shift recurrence)
    shift_rec = cls.get("shift")
    if cid in ("cooper_s7", "cooper_s10", "apery_zeta3"):
        c3b = _run_c3b(cid)
    else:
        c3b = _run_c3b_generated(cid, u, shift_rec, initial_terms=[str(t) for t in u[:10]])
    result["c3b"] = c3b
    if "SYM2" in (c3b.get("verdict") or ""):
        result["status"] = "SURVIVOR"
        result["score_math_only"] = 0.60
    else:
        result["status"] = "REJECTED_C3B"
        result["score_math_only"] = 0.0

    return result


# ─────────────────────────────────────────────────────────────── ranking

def rank_candidates(certs, anchors):
    """Pure ranking from certificate data.

    Mathematical rigor 0.60 is broken into:
      order-3 ODE      0.25
      held-out pass    0.15
      C3b PASS(N>=24)  0.20
    Empirical fit 0.30 is always null (blocked on DM-3 quorum).
    Theoretical consistency 0.10 is null in v1 (no Stream-3 artifact yet).
    """
    for c in certs:
        if c["status"] != "SURVIVOR":
            c["empirical_fit"] = None
            c["theory"] = None
            c["score_total"] = None
            c["score_math_only"] = 0.0
            continue

        score = 0.0
        g1_1 = c.get("g1_1", {})
        g1_3 = c.get("g1_3", {})
        c3b = c.get("c3b", {})

        if g1_1.get("ode_order") == 3:
            score += 0.25
        if g1_1.get("held_out_pass"):
            score += 0.15
        verdict = c3b.get("verdict") or ""
        n_verified = 0
        if "SYM2" in verdict:
            import re
            m = re.search(r"n=(\d+)", verdict)
            if m:
                n_verified = int(m.group(1))
            if n_verified >= 24 or "all-n" in verdict:
                score += 0.20

        c["score_components"] = {
            "math_order3": 0.25 if g1_1.get("ode_order") == 3 else 0,
            "math_heldout": 0.15 if g1_1.get("held_out_pass") else 0,
            "math_c3b": 0.20 if ("SYM2" in (c3b.get("verdict") or "") and (n_verified >= 24 or "all-n" in (c3b.get("verdict") or ""))) else 0,
        }
        c["empirical_fit"] = None
        c["empirical_fit_reason"] = "BLOCKED_ON_DM3_QUORUM"
        c["theory"] = None
        c["theory_reason"] = "BLOCKED_ON_STREAM3_ARTIFACT"
        c["score_math_only"] = score
        c["score_total"] = None

    # Sort by math score desc, then by q2 asc as a deterministic tie-breaker.
    def sort_key(c):
        q2 = Fraction(0)
        if c.get("g1_3", {}).get("q2"):
            q2 = Fraction(str(c["g1_3"]["q2"]))
        return (-c.get("score_math_only", 0), -float(q2))

    ranked = sorted(certs, key=sort_key)
    for i, c in enumerate(ranked):
        c["rank"] = i + 1 if c.get("status") == "SURVIVOR" else None
    return ranked


# ───────────────────────────────────────────────────── elliptic-EFT alignment

def align_survivors(ranked):
    """AE-5: C3b alignment already produced during gate battery. This stage
    aggregates per-survivor partner certificates and emits the alignment summary.
    """
    alignment = []
    for c in ranked:
        if c.get("status") != "SURVIVOR":
            continue
        c3b = c.get("c3b", {})
        alignment.append({
            "id": c["id"],
            "rank": c["rank"],
            "partner_recurrence": c3b.get("partner_recurrence"),
            "partner_first_terms": c3b.get("partner_first_terms"),
            "operator_identity": c3b.get("operator_identity"),
            "verdict": c3b.get("verdict"),
            "certificate": c3b.get("certificate"),
            "epistemic_tag": "[C] we conjecture Sym^2(L2)=L3 corresponds to a Shioda-Inose structure; "
                             "no bulk-to-brane EFT matching is claimed",
        })
    return alignment


# ─────────────────────────────────────────────────────────────── main driver

def main():
    fails = verify_terms()
    if fails:
        print("FATAL: pool term generators disagree with OEIS reference:", fails)
        sys.exit(1)

    # Load anchor fingerprints to seed the archive and provide answer-key context.
    anchor_path = OUT_DIR / "ae_anchor_fingerprints.json"
    anchors = {}
    if anchor_path.exists():
        anchors = json.loads(anchor_path.read_text()).get("fingerprints", {})

    print("[AE-2] generating search space ...")
    genomes = generate_search_space()

    print(f"[AE-2] evaluating {len(genomes)} genomes ...")
    certificates = []
    for family, exponents in genomes:
        cid = genome_id(family, exponents)
        if family == "2factor":
            u = gen_2factor(*exponents, NMAX)
        elif family == "3factor":
            u = gen_3factor(*exponents, NMAX)
        else:
            continue
        cert = gate_battery(cid, family, exponents, u, anchors)
        certificates.append(cert)
        if cert["status"] == "SURVIVOR":
            print(f"  [SURVIVOR] {cid}: q2={cert['g1_3']['q2']}, {cert['c3b']['verdict'][:60]}")

    # Add the certified anchors to the certificate list for ranking context.
    for cid, rec in anchors.items():
        if rec.get("ode") and rec["ode"].get("ode_order") == 3:
            anchor_cert = {
                "id": cid,
                "family": "anchor",
                "exponents": [],
                "first_terms": rec["first_terms"],
                "classify": rec,
                "g1_1": {
                    "ode_order": rec["ode"]["ode_order"],
                    "ode_degree": rec["ode"]["ode_degree"],
                    "held_out_terms": rec["ode"]["held_out_terms"],
                    "held_out_pass": rec["ode"]["held_out_pass"],
                },
                "g1_3": {
                    "q2": rec["mirror"]["q2"],
                    "integral": rec["mirror"]["integral"],
                    "q_coeffs": rec["mirror"]["q_coeffs"],
                    "verdict": "PASS_INTEGRAL" if rec["mirror"]["integral"] else "FAIL_NON_INTEGRAL",
                },
                "c3b": rec.get("c3b", {"verdict": "SKIPPED"}),
                "status": "SURVIVOR" if (rec["ode"]["ode_order"] == 3 and
                                         rec["mirror"]["integral"] and
                                         "SYM2" in rec.get("c3b", {}).get("verdict", "")) else "REJECTED_C3B",
                "score_math_only": 0.60 if (rec["ode"]["ode_order"] == 3 and
                                            rec["mirror"]["integral"] and
                                            "SYM2" in rec.get("c3b", {}).get("verdict", "")) else 0.0,
            }
            certificates.append(anchor_cert)

    print("[AE-4] ranking candidates ...")
    ranked = rank_candidates(certificates, anchors)

    print("[AE-5] elliptic-EFT alignment summary ...")
    alignment = align_survivors(ranked)

    survivors = [c for c in ranked if c.get("status") == "SURVIVOR"]

    out = {
        "nmax": NMAX,
        "n_mirror": N_MIRROR,
        "genomes_evaluated": len(genomes),
        "survivors": len(survivors),
        "ranking": ranked,
        "alignment": alignment,
        "provenance": (
            "Generated-by: scripts/auto_evolve_k3_selection.py | "
            "Verified-by: exact ODE classifier + mirror-map integrality + C3b checker | "
            "Reviewed-by: pending T0"
        ),
    }

    out_path = OUT_DIR / "ae_ranking.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)

    # Human-readable fragment
    report_lines = [
        "\n## Stream 2 AutoEvolve K3 Selection — Run Summary\n",
        f"Genomes evaluated: {len(genomes)}",
        f"Survivors: {len(survivors)}",
        "",
        "| rank | id | family | exponents | q2 | C3b |",
        "|---|---|---|---|---|---|",
    ]
    for c in ranked[:20]:
        if c.get("status") != "SURVIVOR":
            continue
        q2 = c.get("g1_3", {}).get("q2", "")
        verdict = c.get("c3b", {}).get("verdict", "")[:40]
        exps = str(c.get("exponents", ""))
        report_lines.append(f"| {c.get('rank')} | {c['id']} | {c['family']} | {exps} | {q2} | {verdict} |")

    print("\n".join(report_lines))
    print(f"\n[AutoEvolve] wrote {out_path}")
    return out


if __name__ == "__main__":
    main()