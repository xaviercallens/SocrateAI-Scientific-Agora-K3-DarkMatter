#!/usr/bin/env python3
"""
test_gate_e_verdict_controls.py — negative controls for scripts/gate_e_verdict.py

Standing rule 1: a test that cannot fail is not a test. Criterion 5 was a
hardcoded `True` until 2026-07-26 and the expected Picard rank was the
E-007-retracted 4.0. These controls assert the repaired script actually
refuses / fails in every situation where the old one silently passed:

  C1  read_aggregate_verdict raises (E-012 guard) — no verdict from the
      fabricating runner's output.
  C2  physics_washing_audit FAILS on a file containing a known tier
      violation (negative control — the audit can fail).
  C3  physics_washing_audit PASSES on a clean file (positive control —
      the audit is not fail-everything).
  C4  physics_washing_audit FAILS-CLOSED when a target file is missing
      (halt, don't skip — WP-E review item D).
  C5  physics_washing_audit FAILS-CLOSED on an empty file list.
  C6  read_expected_rho returns the live certificate value (currently 19,
      but the test reads the certificate itself — never hardcodes).
  C7  read_expected_rho RAISES on a certificate with picard_rank null
      (in-band retraction must halt the criterion, not default it).
"""
import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import gate_e_verdict as gev  # noqa: E402

failures = []


def check(name, cond, detail=""):
    tag = "ok   " if cond else "FAIL "
    print(f"  {tag} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


# C1 — the E-012 guard
try:
    gev.read_aggregate_verdict("anything.json")
    check("C1 aggregate read refuses (E-012)", False, "did not raise")
except SystemExit as e:
    check("C1 aggregate read refuses (E-012)", "E-012" in str(e))

with tempfile.TemporaryDirectory() as td:
    td = Path(td)

    # C2 — negative control: a genuine tier violation must FAIL the audit
    bad = td / "bad_report.md"
    bad.write_text(
        "The lattice rigidly locks the dark sector coupling.\n\n# Body\nrest\n"
    )
    passed, detail = gev.physics_washing_audit([bad])
    check("C2 audit FAILS on tier violation", passed is False, detail)

    # C3 — positive control: clean file passes
    good = td / "good_report.md"
    good.write_text(
        "Engineering summary: variance characterized; no model claim is made.\n"
        "\n# Body\nrho = 19 [tier B], reported as a lattice rank only.\n"
    )
    passed, detail = gev.physics_washing_audit([good])
    check("C3 audit PASSES on clean file", passed is True, detail)

    # C4 — missing target file fails closed
    passed, detail = gev.physics_washing_audit([td / "does_not_exist.md"])
    check("C4 audit FAILS-CLOSED on missing file", passed is False
          and "missing" in detail.lower(), detail)

    # C5 — empty list fails closed
    passed, detail = gev.physics_washing_audit([])
    check("C5 audit FAILS-CLOSED on empty file list", passed is False, detail)

    # C6 — expected rho comes from the live certificate, not a literal
    live = gev.read_expected_rho()
    with open(gev.C2_V3_CERT) as f:
        cert_value = json.load(f)["picard_rank"]
    check("C6 expected rho == live certificate value", live == float(cert_value),
          f"got {live}, cert says {cert_value}")

    # C7 — a null (retracted) certificate value must raise, not default
    null_cert = td / "C2_null.json"
    null_cert.write_text(json.dumps({"picard_rank": None, "note": "RETRACTED"}))
    try:
        gev.read_expected_rho(null_cert)
        check("C7 null certificate raises", False, "did not raise")
    except ValueError:
        check("C7 null certificate raises", True)

print()
if failures:
    print(f"CONTROLS FAILED: {failures}")
    sys.exit(1)
print("all gate_e_verdict controls behaved as required")
