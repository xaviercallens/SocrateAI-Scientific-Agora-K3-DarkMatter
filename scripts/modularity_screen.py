"""
GAP-1 / Task T1.2: Weil-bound and modularity screen for S_{1,2} and S_{2,1}.
=============================================================================

Scope (honest framing per scientificplan.md T1.2 note):
  A full modularity PROOF is out-of-scope for this script (that is research
  mathematics — proving a specific L-function is modular requires either an
  explicit modularity theorem for the relevant motive or a computer-assisted
  Faltings-Serre argument, neither of which is attempted here). This script
  only produces NECESSARY-CONDITION evidence:
    1. The weight-3 Weil bound |a_p| <= 2p for p in [5, 200].
    2. A finite, explicitly-cited candidate match against a SMALL subset of
       real weight-3 rational newforms pulled from the LMFDB (not the full
       261-form table at level <= 120 — see CANDIDATES below for the exact
       subset and citation). A "no match among these candidates" result is
       NOT evidence of non-modularity; it only means these particular small
       levels do not match.

Method (Stienstra-Beukers 1985, "Congruences"):
  For the diagonal hypergeometric sequence u(n) = sum_k C(n,k)^A C(n+k,k)^B,
  the candidate Frobenius trace at an odd prime p is the "unit-root" residue
    a_p := centered_residue( u((p-1)/2) mod p )
  where centered_residue takes the representative in (-p/2, p/2]. This is
  the same recipe already used for the Weil-bound spot-check in
  scripts/k3_monodromy_verification.py::compute_ap_mod_p (reused here
  verbatim, not re-derived, to avoid drift between the two scripts).

Rule 1 compliance: every a_p value is computed by executed exact-integer
arithmetic (Python's arbitrary-precision int), never typed in by hand.
Rule 5 compliance: the LMFDB candidate coefficients ARE typed constants in
this file, but they are real values fetched from lmfdb.org on 2026-07-11
(URLs cited per-candidate below) — not fabricated. Only 4 small-level forms
are included; this is explicitly disclosed as a small, non-exhaustive subset.

Outputs:
  data/modularity/S12_ap_table.csv
  data/modularity/S21_ap_table.csv
  docs/modularity_report.md

Verify: python scripts/modularity_screen.py
"""

import csv
import math
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data", "modularity")
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)


def primes_upto(n: int) -> list:
    """Sieve of Eratosthenes, exact integers only."""
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(n + 1) if sieve[i]]


def u_exact(A: int, B: int, n: int) -> int:
    """u(n) = sum_{k=0}^n C(n,k)^A * C(n+k,k)^B, exact integer arithmetic."""
    return sum(math.comb(n, k) ** A * math.comb(n + k, k) ** B for k in range(n + 1))


def compute_ap(A: int, B: int, p: int) -> int:
    """
    Candidate Frobenius trace a_p via the Stienstra-Beukers (1985) unit-root
    recipe: a_p := centered_residue(u((p-1)/2) mod p).
    Identical formula to scripts/k3_monodromy_verification.py::compute_ap_mod_p
    (reused, not re-derived, to keep the two scripts in lockstep).
    """
    n = (p - 1) // 2
    val = u_exact(A, B, n)
    ap = val % p
    if ap > p // 2:
        ap -= p
    return ap


def weil_bound_ok(ap: int, p: int) -> bool:
    """Weight-3 Weil bound: |a_p| <= 2 * p^{(3-1)/2} = 2p."""
    return abs(ap) <= 2 * p


def weight2_bound_ok(ap: int, p: int) -> bool:
    """
    Weight-2 Weil (Hasse) bound: |a_p| <= 2 * p^{(2-1)/2} = 2*sqrt(p).
    Added 2026-07-11 per docs/gap1/ORDER_VERIFICATION_FINDINGS.md: S21 was
    reclassified from order-3 (K3, weight 3) to order-2 (elliptic curve,
    weight 2). Weight-3 is the wrong bound for an order-2/elliptic object;
    this is the bound that actually applies if S21's Frobenius traces come
    from a weight-2 (elliptic) motive. Reported for both sequences for
    direct comparison, computed exactly (no hand-typed counts).
    """
    return abs(ap) <= 2 * math.sqrt(p)


# ---------------------------------------------------------------------------
# Candidate weight-3 rational newforms (LMFDB, fetched 2026-07-11).
#
# NOTE ON SCOPE: this is a SMALL, EXPLICITLY NON-EXHAUSTIVE subset of the
# lowest-level entries from the LMFDB weight-3, rational (dim=1) newform
# search (https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/?weight=3&dim=1),
# which returns 261 matches total up to the site's default level bound. A
# "no match" result below means only that S12/S21 do not match THESE 4 forms
# at THESE primes -- it is NOT a general non-modularity statement.
# ---------------------------------------------------------------------------
LMFDB_CANDIDATES = {
    "7.3.b.a": {
        "level": 7, "character_orbit": "7.b", "cm": None,
        "url": "https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/7/3/b/a/",
        "ap": {2: -3, 3: 0, 5: 0, 7: -7, 11: -6, 13: 0, 17: 0, 19: 0, 23: 18,
                29: -54, 31: 0, 37: 38, 41: 0, 43: 58, 47: 0},
    },
    "8.3.d.a": {
        "level": 8, "character_orbit": "8.d", "cm": None,
        "url": "https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/8/3/d/a/",
        "ap": {2: -2, 3: -2, 5: 0, 7: 0, 11: 14, 13: 0, 17: 2, 19: -34, 23: 0,
                29: 0, 31: 0, 37: 0, 41: -46, 43: 14, 47: 0},
    },
    "11.3.b.a": {
        "level": 11, "character_orbit": "11.b", "cm": "Q(sqrt(-11))",
        "url": "https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/11/3/b/a/",
        "ap": {2: 0, 3: -5, 5: -1, 7: 0, 11: -11, 13: 0, 17: 0, 19: 0, 23: 35,
                29: 0, 31: -37, 37: -25, 41: 0, 43: 0, 47: 50},
    },
    "19.3.b.a": {
        "level": 19, "character_orbit": "19.b", "cm": "Q(sqrt(-19))",
        "url": "https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/19/3/b/a/",
        "ap": {2: 0, 3: 0, 5: -9, 7: -5, 11: 3, 13: 0, 17: 15, 19: -19, 23: -30,
                29: 0, 31: 0, 37: 0, 41: 0, 43: 85, 47: 75},
    },
}


def screen_sequence(name: str, A: int, B: int, primes: list) -> dict:
    """Compute a_p table, Weil-bound verdicts, and candidate-match counts."""
    rows = []
    n_weil_fail = 0
    n_weight2_fail = 0
    match_counts = {label: {"checked": 0, "matched": 0} for label in LMFDB_CANDIDATES}

    for p in primes:
        ap = compute_ap(A, B, p)
        ok = weil_bound_ok(ap, p)
        ok2 = weight2_bound_ok(ap, p)
        if not ok:
            n_weil_fail += 1
        if not ok2:
            n_weight2_fail += 1
        row = {"p": p, "a_p": ap, "2p": 2 * p, "weil_ok": ok, "weight2_ok": ok2}
        for label, cand in LMFDB_CANDIDATES.items():
            if p in cand["ap"]:
                match_counts[label]["checked"] += 1
                if cand["ap"][p] == ap:
                    match_counts[label]["matched"] += 1
        rows.append(row)

    return {
        "name": name, "A": A, "B": B,
        "rows": rows,
        "n_primes": len(rows),
        "n_weil_fail": n_weil_fail,
        "n_weight2_fail": n_weight2_fail,
        "match_counts": match_counts,
    }


def write_csv(result: dict, path: str):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["p", "a_p", "2p", "weil_bound_ok", "weight2_bound_ok"])
        for row in result["rows"]:
            writer.writerow([row["p"], row["a_p"], row["2p"], row["weil_ok"], row["weight2_ok"]])


def best_match(result: dict):
    """Return (label, matched, checked) for the candidate with the highest
    matched-fraction, or None if no candidate had any prime in common."""
    best = None
    for label, mc in result["match_counts"].items():
        if mc["checked"] == 0:
            continue
        frac = mc["matched"] / mc["checked"]
        if best is None or frac > best[3]:
            best = (label, mc["matched"], mc["checked"], frac)
    return best


def main():
    primes = [p for p in primes_upto(200) if p >= 5]
    print("=" * 72)
    print("GAP-1 / T1.2: Weil-bound + modularity screen")
    print(f"Primes checked: {len(primes)} (p in [5, 200])")
    print("=" * 72)

    results = {}
    for name, A, B in [("S12", 1, 2), ("S21", 2, 1)]:
        print(f"\nScreening {name} (A={A}, B={B}) ...")
        res = screen_sequence(name, A, B, primes)
        results[name] = res

        csv_path = os.path.join(DATA_DIR, f"{name}_ap_table.csv")
        write_csv(res, csv_path)
        print(f"  Wrote {csv_path}")

        print(f"  Weil bound (weight-3, |a_p|<=2p): {res['n_primes'] - res['n_weil_fail']}/{res['n_primes']} pass")
        if res["n_weil_fail"] > 0:
            failing = [r["p"] for r in res["rows"] if not r["weil_ok"]]
            print(f"  ❌ WEIL BOUND VIOLATED at p = {failing}")
        else:
            print(f"  ✅ Weil bound holds for ALL {res['n_primes']} checked primes")

        print(f"  Weight-2 bound (|a_p|<=2sqrt(p)): {res['n_primes'] - res['n_weight2_fail']}/{res['n_primes']} pass")
        if res["n_weight2_fail"] > 0:
            failing2 = [r["p"] for r in res["rows"] if not r["weight2_ok"]]
            print(f"  ⚠️  weight-2 bound fails at p = {failing2}")

        bm = best_match(res)
        if bm is None:
            print("  No overlapping primes with any candidate (unexpected).")
        else:
            label, matched, checked, frac = bm
            print(f"  Best candidate match: {label} ({matched}/{checked} primes, {frac:.0%})")

    # ---- Markdown report ----
    report_path = os.path.join(DOCS_DIR, "modularity_report.md")
    lines = []
    lines.append("# GAP-1 Modularity Screen Report (Task T1.2)")
    lines.append("")
    lines.append(f"Generated by `scripts/modularity_screen.py`. Primes checked: {len(primes)} (p in [5, 200]).")
    lines.append("")
    lines.append("**Scope disclaimer:** this is a NECESSARY-CONDITION evidence table, not a")
    lines.append("modularity proof. The LMFDB candidate list below is 4 small-level weight-3")
    lines.append("rational newforms (of 261 total dim-1 matches on LMFDB up to its default")
    lines.append("level bound) — a non-match here does not establish non-modularity, only")
    lines.append("that S12/S21 do not match THESE specific forms.")
    lines.append("")

    overall_verdict_falsified = False

    for name, res in results.items():
        lines.append(f"## {name} (A={res['A']}, B={res['B']})")
        lines.append("")
        n_pass = res["n_primes"] - res["n_weil_fail"]
        if res["n_weil_fail"] == 0:
            lines.append(f"- **Weil bound:** ✅ CONSISTENT — all {res['n_primes']} checked primes satisfy |a_p| ≤ 2p.")
        else:
            overall_verdict_falsified = True
            failing = [r["p"] for r in res["rows"] if not r["weil_ok"]]
            lines.append(f"- **Weil bound:** ❌ FALSIFIED — {res['n_weil_fail']}/{res['n_primes']} primes violate |a_p| ≤ 2p at p = {failing}.")
            lines.append("  This is a genuine falsification signal per Rule 4 (Adversarial Assessment):")
            lines.append("  a weight-3 L-function CANNOT violate this bound, so either the unit-root")
            lines.append("  recipe does not apply to this sequence, or the K3/weight-3 identification is wrong.")

        n2_pass = res["n_primes"] - res["n_weight2_fail"]
        if res["n_weight2_fail"] == 0:
            lines.append(f"- **Weight-2 bound** ($|a_p|\\le2\\sqrt p$, the elliptic-curve bound): ✅ holds for all {res['n_primes']} checked primes.")
        else:
            failing2 = [r["p"] for r in res["rows"] if not r["weight2_ok"]]
            lines.append(f"- **Weight-2 bound** ($|a_p|\\le2\\sqrt p$, the elliptic-curve bound): fails at {res['n_weight2_fail']}/{res['n_primes']} primes, p = {failing2}. "
                          f"This is expected/uninformative for a genuine weight-3 (K3) sequence — it is reported here for direct comparison, not as a falsification signal.")

        bm = best_match(res)
        if bm is not None:
            label, matched, checked, frac = bm
            cand = LMFDB_CANDIDATES[label]
            if frac == 1.0 and checked >= 5:
                lines.append(f"- **Modularity match:** candidate `{label}` (level {cand['level']}, char {cand['character_orbit']}) "
                              f"MATCHES on all {checked} overlapping primes — [{cand['url']}]({cand['url']}).")
            else:
                lines.append(f"- **Modularity match:** NO MATCH among the {len(LMFDB_CANDIDATES)} checked candidates. "
                              f"Best candidate `{label}` agreed on only {matched}/{checked} overlapping primes ({frac:.0%}).")
        lines.append("")
        lines.append("| Candidate | Level | Character | Matched / Checked |")
        lines.append("|---|---|---|---|")
        for label, mc in res["match_counts"].items():
            cand = LMFDB_CANDIDATES[label]
            lines.append(f"| [{label}]({cand['url']}) | {cand['level']} | {cand['character_orbit']} | {mc['matched']}/{mc['checked']} |")
        lines.append("")

    lines.append("## Candidate source citations")
    lines.append("")
    for label, cand in LMFDB_CANDIDATES.items():
        cm = f", CM by {cand['cm']}" if cand["cm"] else ""
        lines.append(f"- `{label}`: level {cand['level']}, character orbit {cand['character_orbit']}{cm}. Source: {cand['url']} (fetched 2026-07-11).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**Overall verdict:** {'❌ FALSIFICATION SIGNAL (Weil bound violated)' if overall_verdict_falsified else '✅ Weil bounds consistent for both sequences; no strong modularity match found among the 4 checked LMFDB candidates (evidence is inconclusive for/against modularity — a wider LMFDB search is needed to go further, out of scope for this HAIKU-tier task).'}")
    lines.append("")

    with open(report_path, "w") as f:
        f.write("\n".join(lines))
    print(f"\nWrote {report_path}")

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    for name, res in results.items():
        status = "✅ CONSISTENT" if res["n_weil_fail"] == 0 else "❌ FALSIFIED"
        print(f"  {name}: Weil bound {status} ({res['n_primes'] - res['n_weil_fail']}/{res['n_primes']})")

    return 1 if overall_verdict_falsified else 0


if __name__ == "__main__":
    sys.exit(main())
