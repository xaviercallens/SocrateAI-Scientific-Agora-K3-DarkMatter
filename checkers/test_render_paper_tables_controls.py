#!/usr/bin/env python3
"""
test_render_paper_tables_controls.py -- controls for scripts/render_paper_tables.py

Standing rule 1: a test that cannot fail is not a test.

  P0  the four fragments currently on disk agree with a fresh render (i.e. --check is
      not lying about being green right now)
  N1  tampering CM_POINTS_RHO20.json's s7 z=infinity D value changes the rendered
      rankjump_rows fragment
  N2  tampering C6_SELECTOR_COMPARISON.json's SEL-N tie count changes the rendered
      selector_comparison fragment
  N3  a stale on-disk fragment (one byte flipped) is caught by --check (exit 1),
      not silently accepted
"""
import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import render_paper_tables as rpt  # noqa: E402

failures = []


def check(name, cond, detail=""):
    tag = "ok   " if cond else "FAIL "
    print(f"  {tag} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


# P0
for name, fn in rpt.TABLES.items():
    fresh = fn()
    on_disk = (rpt.OUT / name).read_text() if (rpt.OUT / name).exists() else None
    check(f"P0 {name} on disk matches a fresh render", on_disk == fresh)

# N1: tamper CM_POINTS_RHO20.json in a temp copy pointed at by rpt.CERTS
orig_certs = rpt.CERTS
tmp = Path(tempfile.mkdtemp(prefix="rpt_ctl_"))
for f in orig_certs.glob("*.json"):
    shutil.copy(f, tmp / f.name)
rpt.CERTS = tmp
base = rpt.render_rankjump_rows()

d = json.loads((tmp / "CM_POINTS_RHO20.json").read_text())
d["families"]["cooper_s7"]["locus_hits"]["infinity"][0]["D"] = -999
(tmp / "CM_POINTS_RHO20.json").write_text(json.dumps(d))
tampered = rpt.render_rankjump_rows()
check("N1 tampered D changes the rankjump_rows fragment", tampered != base and "-999" in tampered)
shutil.copy(orig_certs / "CM_POINTS_RHO20.json", tmp / "CM_POINTS_RHO20.json")

# N2
base2 = rpt.render_selector_comparison()
sc = json.loads((tmp / "C6_SELECTOR_COMPARISON.json").read_text())
sc["result"]["families"]["cooper_s7"]["SEL-N"]["tie_count"] = 1
sc["result"]["families"]["cooper_s7"]["SEL-N"]["unique"] = True
sc["result"]["families"]["cooper_s7"]["SEL-N"]["tied_rows"] = sc["result"]["families"]["cooper_s7"]["SEL-N"]["tied_rows"][:1]
(tmp / "C6_SELECTOR_COMPARISON.json").write_text(json.dumps(sc))
tampered2 = rpt.render_selector_comparison()
check("N2 tampered SEL-N tie count changes the selector_comparison fragment", tampered2 != base2)

rpt.CERTS = orig_certs

# N3: a stale on-disk fragment must fail --check
orig_out = rpt.OUT
tmp_out = tmp / "tables"
tmp_out.mkdir()
for name in rpt.TABLES:
    (tmp_out / name).write_text("STALE CONTENT, NOT A REAL RENDER\n")
rpt.OUT = tmp_out
rc = rpt.main(["--check"])
check("N3 stale on-disk fragment caught by --check (exit 1)", rc == 1)
rpt.OUT = orig_out

print()
if failures:
    print(f"FAILED: {len(failures)} control(s): {failures}")
    sys.exit(1)
print("all render_paper_tables controls passed")
