#!/usr/bin/env python3
"""Controls for checkers/check_selected_k3_dossier.py (standing rule 1): every disagreement between
sources must be refused; a missing source must be refused; the real certificates must agree."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from checkers import check_selected_k3_dossier as dz  # noqa: E402


@pytest.fixture()
def certs(tmp_path):
    for n in dz.SOURCES:
        shutil.copy(dz.DEFAULT_CERTS / n, tmp_path / n)
    return tmp_path


def _edit(certs, name, fn):
    p = certs / name
    d = json.loads(p.read_text())
    fn(d)
    p.write_text(json.dumps(d))


def test_P1_real_certificates_agree():
    d = dz.build(dz.DEFAULT_CERTS)
    s7, s10 = d["families"]["cooper_s7"], d["families"]["cooper_s10"]
    assert s7["D"] == -3 and s7["abs_disc_T"] == 3 and s7["lattice_half"]["tier"] == "A" and s7["neron_severi_structure"]["mordell_weil_rank"] == 0
    assert s10["D"] == -4 and s10["abs_disc_T"] == 4 and s10["A2_membership"]["verdict"] == "ABSENT"
    assert len(d["inputs_sha256"]) == 7


def test_N1_tampered_selector_vector_refused(certs):
    _edit(certs, "C6_SELECTED_CANDIDATE.json", lambda d: d["selected"]["cooper_s7"].__setitem__("v", [1, -1, 0]))
    with pytest.raises(dz.Refuse, match="v differs"):
        dz.build(certs)


def test_N2_tampered_T_form_refused(certs):
    _edit(certs, "C6_SELECTED_CANDIDATE.json", lambda d: d["selected"]["cooper_s7"].__setitem__("T_reduced_form", [1, 0, 1]))
    with pytest.raises(dz.Refuse):
        dz.build(certs)


def test_N3_missing_source_refused(certs):
    (certs / "TW2_RHO20_LOCI.json").unlink()
    with pytest.raises(dz.Refuse, match="missing"):
        dz.build(certs)


def test_N4_lattice_tier_downgrade_refused(certs):
    def f(d):
        for r in d["rows"]:
            if r["candidate"] == "cooper_s7" and r["v"] == [14, -14, -5]:
                r["lattice_tier"] = "B"
    _edit(certs, "CM_POINTS_RHO20_LATTICE_TIER.json", f)
    with pytest.raises(dz.Refuse, match="lattice tier"):
        dz.build(certs)


def test_N5_non_unique_point_refused(certs):
    def f(d):
        for p in d["families"]["cooper_s7"]["per_D"]:
            if p["D"] == -3:
                p["points_on_X0n_star"] = 2
    _edit(certs, "CM_COMPLETENESS.json", f)
    with pytest.raises(dz.Refuse, match="unique"):
        dz.build(certs)


def test_N6_tw2_structure_mismatch_refused(certs):
    _edit(certs, "TW2_RHO20_LOCI.json", lambda d: d["result"]["loci"]["infinity"]["resolution"].__setitem__("mordell_weil_rank", 1))
    with pytest.raises(dz.Refuse, match="TW2_RHO20_LOCI"):
        dz.build(certs)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
