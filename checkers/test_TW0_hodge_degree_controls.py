#!/usr/bin/env python3
"""Controls for the RETRACTED checkers/check_TW0_hodge_degree.py (2026-10-07).

The checker's degree formula was shown to be a Fuchs-relation tautology (see
briefs/WP_TW0_HODGE_DEGREE_REEXAMINATION_2026_10_07.md); the only behaviour left to test is that it
refuses to run by default and that its old certificate carries the in-band retraction flag.
Its former tests ("cooper_s7 passes", "perturbed operators fail") tested a non-discriminating
quantity and were removed rather than kept green.
"""
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from checkers import check_TW0_hodge_degree as old  # noqa: E402


def test_refuses_by_default(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["check_TW0_hodge_degree.py"])
    assert old.main() == 2
    assert "REFUSED (2026-10-07)" in capsys.readouterr().out


def test_old_certificate_carries_retraction_flag():
    cert = REPO / "data" / "certificates" / "TW0_hodge_degree_cooper_s7.json"
    if not cert.exists():
        pytest.skip("old certificate absent")
    d = json.loads(cert.read_text())
    assert "RETRACTED_AS_FAMILY_LEVEL_STATEMENT_2026_10_07" in d
    assert d["RETRACTED_AS_FAMILY_LEVEL_STATEMENT_2026_10_07"]["superseded_by"].endswith("TW0_HODGE_DEGREE_ORBIFOLD.json")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
