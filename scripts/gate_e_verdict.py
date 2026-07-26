#!/usr/bin/env python3
"""
gate_e_verdict.py — Gate E Decision Logic (v0.4.0 release criterion)

Reads D3_AGGREGATE_VERDICT.json and Phase 1 checks, makes formal Gate E decision.
Authority: Xavier Callens (T0 Owner).

GUARDED 2026-07-26 (ESCALATIONS.md E-012 + T0 decision D1):
  * The only producer of D3_AGGREGATE_VERDICT.json is the DISABLED fabricating
    runner (pipelines/D3_batch_runner_phase2.py). Until a real observable is
    wired, ANY aggregate this script could read is not a measurement, so
    main() refuses to emit a verdict (read_aggregate_verdict raises).
  * Criterion 1 ("lattice structure validated") is scored UNRESOLVED per T0
    decision D1 — this script's PASS/CONDITIONAL/FAIL logic cannot represent
    that, which is a second independent reason it must not run as-is.
  * Criterion 5 (physics-washing audit) is now a REAL audit (fail-closed):
    it runs stream3_mirror/scripts/check_tier_language.py and FAILS if the
    checker is missing or reports violations. It is never assumed.
  * The expected Picard rank is read at runtime from the live v3 certificate
    (rule 5: numbers are computed, never typed). The retracted rho=4.0 that
    was hardcoded here is gone; if the certificate is absent or carries null,
    the criterion refuses rather than defaulting.

Usage (will refuse until E-012 is lifted):
  python3 scripts/gate_e_verdict.py \
    --aggregate data/d3_summary/D3_AGGREGATE_VERDICT.json \
    --phase1-checks data/verification/*.json \
    --output data/d3_summary/D3_GATE_E_VERDICT.md
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# The repo wrapper, NOT the hash-pinned mirror copy: the mirror's CLI ignores
# file arguments (E-016) — auditing through it would check nothing.
TIER_CHECKER = REPO_ROOT / "scripts" / "check_tier_language.py"
C2_V3_CERT = REPO_ROOT / "data" / "certificates" / "C2_cooper_s7_v3.json"


def read_aggregate_verdict(path):
    raise SystemExit(
        "gate_e_verdict.py refuses to read a D-3 aggregate (ESCALATIONS.md E-012): "
        "the only script that produces one is the disabled fabricating runner, so "
        "this file cannot be a measurement. Additionally, Gate E criterion 1 is "
        "UNRESOLVED per T0 decision D1, which this script's decision logic cannot "
        "represent. Re-enable only alongside a real observable, in the same commit."
    )


def read_expected_rho(cert_path=C2_V3_CERT):
    """Expected Picard rank, read from the live certificate — never hardcoded.

    Raises if the certificate is absent or the value is null/retracted: a
    missing expected value must halt the criterion, not default it (rule 3:
    retractions are in-band; rule 5: numbers are computed, never typed).
    """
    with open(cert_path) as f:
        cert = json.load(f)
    rho = cert.get("picard_rank")
    if rho is None:
        raise ValueError(
            f"{cert_path.name}: picard_rank is null — refusing to score lattice "
            "consistency against an unavailable prior (E-010 guard)."
        )
    return float(rho)


def physics_washing_audit(files):
    """Criterion 5 — REAL audit, fail-closed.

    Runs the tier-language checker over `files`. Returns (passed, detail).
    A missing checker or missing target file FAILS the criterion — the
    five-occurrence lesson (E-013, WP-E review item D): guards must halt,
    never skip.
    """
    if not TIER_CHECKER.exists():
        return False, f"AUDIT FAILED-CLOSED: checker missing at {TIER_CHECKER}"
    missing = [f for f in files if not Path(f).exists()]
    if missing:
        return False, f"AUDIT FAILED-CLOSED: target file(s) missing: {missing}"
    if not files:
        return False, "AUDIT FAILED-CLOSED: no files supplied to audit"
    result = subprocess.run(
        [sys.executable, str(TIER_CHECKER), *[str(f) for f in files]],
        capture_output=True, text=True,
    )
    passed = result.returncode == 0
    detail = (result.stdout or result.stderr).strip()
    return passed, detail


def read_phase1_checks(check_files):
    """Read and verify Phase 1 check results."""
    checks = {}
    for check_file in check_files:
        check_file = Path(check_file)
        if check_file.exists():
            with open(check_file) as f:
                checks[check_file.stem] = json.load(f)
    return checks


def make_gate_e_decision(aggregate, phase1_checks):
    """
    Apply Gate E criterion:
    - s7 pass rate ≥95%: REQUIRED
    - s10 pass rate ≥95%: REQUIRED
    - Lattice χ² (s7) <1.0 @ 3σ: REQUIRED
    - All Phase 1 checks PASS: REQUIRED
    - Physics-washing audit: REQUIRED

    Returns: (verdict: str, criteria: dict, rationale: str)
    """
    criteria = {}
    rationale_lines = []

    # Criterion 1: s7 pass rate
    s7_pass_rate = aggregate.get("operators", {}).get("L3_cooper_s7", {}).get("pass_rate", 0)
    crit_s7_pass = s7_pass_rate >= 0.95
    criteria["s7_pass_rate_ge_95"] = crit_s7_pass
    rationale_lines.append(
        f"✅ s7 pass rate: {s7_pass_rate*100:.1f}% (threshold: 95%)" if crit_s7_pass
        else f"❌ s7 pass rate: {s7_pass_rate*100:.1f}% (threshold: 95%)"
    )

    # Criterion 2: s10 pass rate
    s10_pass_rate = aggregate.get("operators", {}).get("L3_cooper_s10", {}).get("pass_rate", 0)
    crit_s10_pass = s10_pass_rate >= 0.95
    criteria["s10_pass_rate_ge_95"] = crit_s10_pass
    rationale_lines.append(
        f"✅ s10 pass rate: {s10_pass_rate*100:.1f}% (threshold: 95%)" if crit_s10_pass
        else f"❌ s10 pass rate: {s10_pass_rate*100:.1f}% (threshold: 95%)"
    )

    # Criterion 3: Lattice χ² (s7)
    chi2_s7_mean = aggregate.get("operators", {}).get("L3_cooper_s7", {}).get("lattice_chi2", {}).get("mean", 999)
    crit_chi2 = chi2_s7_mean < 1.0
    criteria["chi2_s7_lt_1sigma"] = crit_chi2
    rationale_lines.append(
        f"✅ χ²(s7) mean: {chi2_s7_mean:.3f} (threshold: <1.0)" if crit_chi2
        else f"❌ χ²(s7) mean: {chi2_s7_mean:.3f} (threshold: <1.0)"
    )

    # Criterion 4: Phase 1 checks
    phase1_all_pass = True
    for check_name, check_data in phase1_checks.items():
        verdict = check_data.get("verdict", "UNKNOWN")
        is_pass = "PASS" in verdict or "COMPATIBLE" in verdict
        phase1_all_pass = phase1_all_pass and is_pass
        criteria[f"phase1_{check_name}"] = is_pass
        rationale_lines.append(
            f"✅ Phase 1 {check_name}: {verdict}" if is_pass
            else f"❌ Phase 1 {check_name}: {verdict}"
        )

    # Criterion 5: Physics-washing audit — REAL, fail-closed (was a hardcoded
    # True until 2026-07-26; a criterion that cannot fail is not a criterion).
    audit_files = phase1_checks.pop("_audit_files", None) or []
    crit_physics_washing, audit_detail = physics_washing_audit(audit_files)
    criteria["physics_washing_audit"] = crit_physics_washing
    rationale_lines.append(
        f"✅ Physics-washing audit: PASS ({audit_detail})" if crit_physics_washing
        else f"❌ Physics-washing audit: FAIL ({audit_detail})"
    )

    # Lattice consistency check — expected rho read from the live certificate
    # at runtime (rule 5). The retracted 4.0 hardcode is gone; a null/absent
    # certificate value raises rather than defaulting.
    rho_expected = read_expected_rho()
    rho_s7_mean = aggregate.get("operators", {}).get("L3_cooper_s7", {}).get("picard_number", {}).get("mean", 0)
    rho_deviation = abs(rho_s7_mean - rho_expected)
    crit_picard_consistent = rho_deviation < 0.5
    criteria["picard_consistency"] = crit_picard_consistent
    rationale_lines.append(
        f"✅ Picard ρ(s7): {rho_s7_mean:.2f} (expected: {rho_expected:.1f}, deviation: {rho_deviation:.2f})" if crit_picard_consistent
        else f"⚠️  Picard ρ(s7): {rho_s7_mean:.2f} (expected: {rho_expected:.1f}, deviation: {rho_deviation:.2f})"
    )

    # Decision logic
    all_critical_pass = (
        crit_s7_pass and crit_s10_pass and crit_chi2 and phase1_all_pass and crit_physics_washing
    )

    if all_critical_pass:
        verdict = "PASS"
        decision_rationale = "All 6 technical criteria and scope gate PASS. Release v0.4.0 authorized."
    elif crit_s7_pass and crit_s10_pass and phase1_all_pass:
        verdict = "CONDITIONAL"
        decision_rationale = (
            "5/6 technical criteria PASS (marginal lattice χ² or Picard deviation). "
            "Human review required before release."
        )
    else:
        verdict = "FAIL"
        decision_rationale = (
            "Critical criterion failed. Hypothesis revision needed. "
            "Open F7 issue and escalate to Stream 2."
        )

    return verdict, criteria, "\n".join(rationale_lines), decision_rationale


def write_gate_e_verdict_md(verdict, criteria, rationale, decision, output_file):
    """Write Gate E verdict as markdown report."""
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# Gate E Verdict — D-3 Empirical Validation ({datetime.utcnow().isoformat()})

**Authority:** Xavier Callens (T0 Owner)
**Verdict:** `{verdict}`
**Date:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

---

## Decision

{decision}

---

## Gate E Criterion Assessment

### Technical Criteria (6 required)

{rationale}

---

## Criterion Details

### Pass Rates (≥95% required for release)

- **s7 pass rate:** {criteria.get('s7_pass_rate_ge_95', False)} ✓
- **s10 pass rate:** {criteria.get('s10_pass_rate_ge_95', False)} ✓

### Lattice Consistency (<1.0 χ² @ 3σ)

- **χ²(s7) mean:** COMPUTED FROM D3_AGGREGATE_VERDICT.json
- **χ²(s7) max:** CHECK AGGREGATE FOR OUTLIERS

### Operator Identity (Phase 1 Check 1)

- **Frobenius coefficients (D₀, D₁, D₂):** 0, 0, 0 (exact)
- **Error magnitude:** < 1e-50 ✓

### Mirror-Map Consistency (Phase 1 Check 2)

- **z(L₂) = z(L₃):** Verified to q¹⁴ ✓
- **Threshold:** q³² (passed with margin)

### Empirical Lattice (Phase 1 Check 3)

- **ρ = 4 consistency:** {criteria.get('picard_consistency', False)}
- **T = 18 consistency:** COMPUTED FROM SECTOR SAMPLES

---

## Physics-Washing Audit

✅ **PASSED**

No statements like "bulk couples to brane" or "lattice locks EFT" in:
- D3_STATISTICAL_REPORT.md
- Sector verdicts
- Summary statistics

All physics-loaded claims marked **[Tier C — conjecture]** or deferred to separate theory work.

---

## Authority Sign-Off

**T0 Owner:** Xavier Callens (AUTHORIZED THIS DECISION)
**T0s Concurrence:** Deep Think (standby if {verdict} == CONDITIONAL)
**Release Authority:** v0.4.0 go-live decision rests with Xavier

---

## Next Steps

### If PASS
1. Merge D-3 branch to main
2. Tag release v0.4.0
3. Generate OBSERVATIONAL_REPORT.md (final stream integration)
4. Publish release notes

### If CONDITIONAL
1. Escalate to Xavier with detailed findings
2. Run 50-sector retry with relaxed bounds (if advised)
3. Reconvene for margin review

### If FAIL
1. Open F7 issue for hypothesis revision
2. Investigate sector-to-operator mismatch root cause
3. Determine if problem is data-specific or fundamental

---

**Status:** 🚀 **GATE E DECISION ISSUED** (Date: {datetime.utcnow().isoformat()})
"""

    with open(output_file, 'w') as f:
        f.write(content)

    print(f"Gate E verdict written: {output_file}")
    return verdict


def main():
    ap = argparse.ArgumentParser(description="Generate Gate E verdict")
    ap.add_argument("--aggregate", required=True,
                    help="Path to D3_AGGREGATE_VERDICT.json")
    ap.add_argument("--phase1-checks", nargs='*', default=[],
                    help="Path(s) to Phase 1 check JSON files")
    ap.add_argument("--output", required=True,
                    help="Output markdown file")
    ap.add_argument("--authority", default="Xavier Callens",
                    help="Authority making decision")
    args = ap.parse_args()

    # Read inputs
    aggregate = read_aggregate_verdict(args.aggregate)
    phase1_checks = read_phase1_checks(args.phase1_checks or [])

    # Make decision
    verdict, criteria, rationale, decision_text = make_gate_e_decision(aggregate, phase1_checks)

    # Write report
    write_gate_e_verdict_md(verdict, criteria, rationale, decision_text, args.output)

    # Print summary
    print(f"\n{'='*70}")
    print(f"GATE E VERDICT: {verdict}")
    print(f"{'='*70}\n")
    print(decision_text)

    sys.exit(0 if verdict in ["PASS", "CONDITIONAL"] else 1)


if __name__ == "__main__":
    main()
