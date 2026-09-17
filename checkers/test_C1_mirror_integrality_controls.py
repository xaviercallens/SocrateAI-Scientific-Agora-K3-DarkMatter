#!/usr/bin/env python3
"""
test_C1_mirror_integrality_controls.py -- controls for check_C1_mirror_integrality.py.
"A test that cannot fail is not a test" (TODO.md standing rule 1).

  1. MATCH: s7 z(q) from the register recurrence equals refs/oeis_A279618_bfile.txt on
     every b-file term. This is what validates the eps-deformation (the g series).
  2. MISMATCH: the same comparison against the b-file with one term changed must
     report a mismatch at that index.
  3. WRONG DERIVATIVE: s7's g series with two coefficients swapped (g3 <-> g4) must FAIL
     integrality. (A first version used g/3; it did NOT fail, because q/z for s7 has an
     integral cube root to the tested order -- see the checker's root-index field.)
  4. CORRUPTED RECURRENCE: s7's recurrence with one constant changed must be REFUSED
     (f0 no longer reproduces the stored terms), never given a verdict.
  5. POSITIVE: unmodified s7 passes at the test order.

Run: python3 checkers/test_C1_mirror_integrality_controls.py   (or pytest)

Generated-by: Claude (Opus 5), Stream 2 | Verified-by: this file | Reviewed-by: N
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_C1_mirror_integrality as C  # noqa: E402

ORDER = 30
SEQS = json.loads(C.REFS.read_text())["sequences"]
S7 = SEQS["cooper_s7"]


def _s7_Z():
    _, _, Z = C.mirror_map(S7["recurrence_python"], ORDER)
    return Z


def test_bfile_match():
    rows = C.read_bfile(C.BFILE_A279618)
    n_cmp, mism = C.compare_to_bfile(_s7_Z(), rows)
    assert n_cmp >= 20, f"too few b-file terms compared ({n_cmp})"
    assert mism is None, f"s7 z(q) disagrees with A279618 at q^{mism}"
    return f"s7 z(q) == A279618 on {n_cmp} terms"


def test_bfile_tamper_mismatch():
    rows = C.read_bfile(C.BFILE_A279618)
    idx, val = rows[7]
    rows[7] = (idx, val + 1)
    _, mism = C.compare_to_bfile(_s7_Z(), rows)
    assert mism == idx, f"tampered b-file not detected (mismatch reported at {mism}, expected {idx})"
    return f"tampered term q^{idx} detected"


def test_wrong_derivative_fails():
    f0, g = C.frobenius(S7["recurrence_python"], ORDER + 1)
    g = list(g)
    g[3], g[4] = g[4], g[3]
    Q = [F(0)] + C.ps_exp(C.ps_mul(g, C.ps_inv(f0, ORDER), ORDER), ORDER)[:ORDER]
    bad = C.first_nonintegral(Q)
    assert bad is not None, "swapped-g mirror map came out integral -- control is vacuous"
    return f"swapped-g mirror map non-integral at index {bad}"


def test_corrupted_recurrence_refused():
    entry = dict(S7)
    rec = entry["recurrence_python"]
    assert rec.startswith("((90+"), "control anchor moved; update this control"
    entry["recurrence_python"] = "((91+" + rec[len("((90+"):]
    try:
        C.check_entry("cooper_s7_corrupted", entry, ORDER)
    except C.Refused as e:
        return f"refused: {e}"
    raise AssertionError("corrupted recurrence was given a verdict instead of being refused")


def test_s7_passes():
    r = C.check_entry("cooper_s7", S7, ORDER)
    assert r["verdict"] == f"PASS({ORDER})", r
    return r["verdict"]


CONTROLS = [
    ("s7 z(q) matches A279618 b-file (must MATCH)", test_bfile_match),
    ("tampered b-file (must MISMATCH)", test_bfile_tamper_mismatch),
    ("swapped g3<->g4 (must FAIL integrality)", test_wrong_derivative_fails),
    ("corrupted recurrence (must be REFUSED)", test_corrupted_recurrence_refused),
    ("unmodified s7 (must PASS)", test_s7_passes),
]


def main():
    ok_all = True
    for name, fn in CONTROLS:
        try:
            detail, ok = fn(), True
        except AssertionError as e:
            detail, ok = str(e), False
        ok_all &= ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name}\n        {detail}")
    print(f"VERDICT: {'ALL CONTROLS PASS' if ok_all else 'CONTROL SUITE FAILED'}")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
