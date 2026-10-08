#!/usr/bin/env python3
"""Controls for checkers/check_selected_k3_identification.py (standing rule 1)."""
import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from checkers import check_selected_k3_identification as k  # noqa: E402


def test_P1_real_data_identifies_the_four_points():
    d = k.build()
    by = {p["point"]: p for p in d["points"]}
    s7 = by["cooper_s7, z = infinity (AM-8 pick)"]
    assert s7["determinant"] == 3 and s7["identification"].startswith("X_3") and s7["table_entry"]["No"] == 1
    s10 = by["cooper_s10, z = infinity (AM-8 pick)"]
    assert s10["determinant"] == 4 and s10["identification"].startswith("X_4") and s10["table_entry"]["No"] == 2
    z1 = by["cooper_s7, z = -1"]
    assert z1["determinant"] == 7 and z1["identification"].startswith("X_7") and z1["table_entry"]["No"] == 3
    z27 = by["cooper_s7, z = 1/27"]
    assert z27["determinant"] == 28 and z27["number_of_classes"] == 2 and not z27["determined_by_discriminant_alone"] and z27["table_entry"] is None


def test_P2_class_counts_are_computed_and_match_known_values():
    assert [len(k.reduced_classes(d)) for d in (3, 4, 7, 28)] == [1, 1, 1, 2]
    assert sorted(k.reduced_classes(28)) == [(1, 0, 7), (2, 2, 4)]            # the primitive form and 2 x [2,1,4]
    assert sorted(k.reduced_classes(12)) == [(1, 0, 3), (2, 2, 2)]            # x^2+3y^2 and the non-primitive 2(x^2+xy+y^2)


def test_P3_the_picks_sit_at_the_two_smallest_attainable_determinants_computed():
    d = k.build()
    floor = d["global_floor"]["smallest_determinants_attained_by_any_positive_definite_even_binary_lattice"]
    assert floor[:2] == [3, 4] and d["global_floor"]["picks_determinants"] == [3, 4]
    assert all(k.reduced_classes(x) == [] for x in (1, 2))               # nothing below 3 exists: the floor is computed, not assumed


def test_N1_positive_definiteness_enforced():
    with pytest.raises(k.Refuse):
        k.reduced_classes(0)
    with pytest.raises(k.Refuse):
        k.reduced_classes(-4)


def test_N2_unreduced_or_wrong_form_refused():
    src = k.parse_source()
    with pytest.raises(k.Refuse):
        k.identify("x", (3, 1, 1), src)                                      # a > c: not a reduced representative
    with pytest.raises(k.Refuse):
        k.identify("x", (2, 0, 1), src)                                      # a > c again, determinant 8


def test_N3_tampered_source_missing_uniqueness_sentence_refused(tmp_path):
    bad = tmp_path / "t.txt"
    bad.write_text(k.SRC.read_text().replace("unique up to isomorphisms for d = 3, 4, 7", "UNIQUE for d = 3, 4"))
    with pytest.raises(k.Refuse, match="required statement"):
        k.parse_source(bad)


def test_N4_tampered_table_changes_the_identification(tmp_path):
    bad = tmp_path / "t.txt"
    bad.write_text(k.SRC.read_text().replace("1   [2,1,2]            Vinberg [8]", "1   [2,1,3]            Vinberg [8]"))
    src = k.parse_source(bad)
    assert (2, 1, 3) in src["table"] and (2, 1, 2) not in src["table"]
    r = k.identify("s7", (1, 1, 1), src)
    assert r["table_entry"] is None                                          # the pick no longer matches a table row


def test_N5_missing_source_refused(tmp_path):
    with pytest.raises(k.Refuse, match="missing"):
        k.parse_source(tmp_path / "absent.txt")


def test_N6_dossier_tamper_changes_the_result(tmp_path):
    for n in ("SELECTED_K3_DOSSIER.json", "CM_POINTS_RHO20.json", "INOSE_MODEL_M7.json"):
        shutil.copy(k.CERTS / n, tmp_path / n)
    p = tmp_path / "SELECTED_K3_DOSSIER.json"
    d = json.loads(p.read_text())
    d["families"]["cooper_s7"]["T_reduced_form_abc"] = [1, 0, 1]             # claim the s7 pick has T = <2>+<2>
    p.write_text(json.dumps(d))
    with pytest.raises(k.Refuse, match="s7 pick is not table No.1"):
        k.build(tmp_path)


def test_N7_model_without_E_omega_squared_refused(tmp_path):
    for n in ("SELECTED_K3_DOSSIER.json", "CM_POINTS_RHO20.json", "INOSE_MODEL_M7.json"):
        shutil.copy(k.CERTS / n, tmp_path / n)
    p = tmp_path / "INOSE_MODEL_M7.json"
    d = json.loads(p.read_text())
    d["result"]["S6"]["both_zero_E_omega_x_E_omega"] = False
    p.write_text(json.dumps(d))
    with pytest.raises(k.Refuse, match="E_omega"):
        k.build(tmp_path)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
