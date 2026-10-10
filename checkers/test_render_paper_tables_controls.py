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
shutil.copy(orig_certs / "C6_SELECTOR_COMPARISON.json", tmp / "C6_SELECTOR_COMPARISON.json")

# N4 (2026-10-08): the fibration orders are read, not typed -- a tampered locus order must change the table
base4 = rpt.render_fibration_orders()
fb = json.loads((tmp / "INOSE_FIBRATION_MULTIPLICITIES.json").read_text())
fb["result"]["T5_s7_loci"]["-1"]["orders"]["s=0"] = 7
(tmp / "INOSE_FIBRATION_MULTIPLICITIES.json").write_text(json.dumps(fb))
t4 = rpt.render_fibration_orders()
check("N4 tampered locus order changes the fibration_orders fragment", t4 != base4 and "7" in t4.split("z=-1")[1].split("\\\\")[0])
fb["result"]["T3_generic_orders"]["roots_of_d_of_s2"] = "6 simple iff ..."
(tmp / "INOSE_FIBRATION_MULTIPLICITIES.json").write_text(json.dumps(fb))
check("N4b tampered generic root count changes the generic row", rpt.render_fibration_orders().count(",1") > t4.count(",1"))
shutil.copy(orig_certs / "INOSE_FIBRATION_MULTIPLICITIES.json", tmp / "INOSE_FIBRATION_MULTIPLICITIES.json")

# N5 (2026-10-08): the ADVISORY tag follows the certificate flag, not the family name
tr = json.loads((tmp / "CM_POINTS_RHO20_LATTICE_TIER.json").read_text())
check("N5a no ADVISORY tag while every advisory_family flag is false", "ADVISORY" not in rpt.render_rankjump_rows())
for r in tr["rows"]:
    if r["candidate"] == "cooper_s7":
        r["advisory_family"] = True
(tmp / "CM_POINTS_RHO20_LATTICE_TIER.json").write_text(json.dumps(tr))
t5 = rpt.render_rankjump_rows()
check("N5b setting the s7 flag tags exactly the s7 rows", t5.count("ADVISORY") == 3 and all("cooper\\_s7}\\,(ADVISORY)" in l for l in t5.splitlines() if "cooper\\_s7}" in l))
shutil.copy(orig_certs / "CM_POINTS_RHO20_LATTICE_TIER.json", tmp / "CM_POINTS_RHO20_LATTICE_TIER.json")

# N6 (2026-10-08): new-paper tables follow their certificates
base6 = rpt.render_tw2_loci()
lo = json.loads((tmp / "TW2_RHO20_LOCI.json").read_text())
lo["result"]["loci"]["infinity"]["resolution"]["mordell_weil_rank"] = 1
lo["result"]["loci"]["infinity"]["resolution"]["height"] = "3"
lo["result"]["loci"]["infinity"]["resolution"]["P_dot_O_solutions"] = [{"P_dot_O": 9}]
(tmp / "TW2_RHO20_LOCI.json").write_text(json.dumps(lo))
t6 = rpt.render_tw2_loci()
check("N6 a tampered MW rank at z=infinity removes 'no section'", "no section" in base6 and "no section" not in t6)
idn = json.loads((tmp / "SELECTED_K3_IDENTIFICATION.json").read_text())
base7 = rpt.render_identification()
idn["points"][0]["determined_by_discriminant_alone"] = False
(tmp / "SELECTED_K3_IDENTIFICATION.json").write_text(json.dumps(idn))
check("N7 identification name is withheld when the certificate says det does not determine it", rpt.render_identification().count("not named") == base7.count("not named") + 1)

# N8 (2026-10-08): the Reading S table follows K3xT2_READING_S.json
rs = json.loads((tmp / "K3xT2_READING_S.json").read_text())
base8 = rpt.render_reading_s()
rs["result"]["generic"]["cooper_s7"]["verdict"] = "FAIL_NO_ISOMETRY_TO_CERTIFIED_GRAM"
rs["result"]["rho20_cooper_s7"]["-1"]["agree"] = False
(tmp / "K3xT2_READING_S.json").write_text(json.dumps(rs))
t8 = rpt.render_reading_s()
check("N8 a failed isometry and a disagreement both show as NO", t8 != base8 and t8.count("NO") == base8.count("NO") + 2)

# N9 (2026-10-10): the section-descent table follows TW2_SECTION_DESCENT.json
sd = json.loads((tmp / "TW2_SECTION_DESCENT.json").read_text())
base9 = rpt.render_section_descent()
sd["result"]["P_dot_O"] = 6
sd["result"]["height"] = "16"
sd["cross_check_against_earlier_steps"]["agree"] = False
(tmp / "TW2_SECTION_DESCENT.json").write_text(json.dumps(sd))
t9 = rpt.render_section_descent()
check("N9 a tampered P.O/height/cross-check changes the descent table and shows NO", t9 != base9 and "NO" in t9 and "$16$" in t9)

# N10: the simulator-ledger table follows the mirrored counts
orig_repo = rpt.REPO
mirror = json.loads((orig_repo / "refs" / "simulator_k3t2_ledger_counts_v3.json").read_text())
base10 = rpt.render_sim_ledger()
mirror["counts"]["comparison"]["final_status_counts"]["AGREE"] = 999
fake_repo = tmp / "fake_repo"
(fake_repo / "refs").mkdir(parents=True)
(fake_repo / "refs" / "simulator_k3t2_ledger_counts_v3.json").write_text(json.dumps(mirror))
rpt.REPO = fake_repo
t10 = rpt.render_sim_ledger()
rpt.REPO = orig_repo
check("N10 a tampered mirrored count changes the simulator-ledger table", t10 != base10 and "999" in t10)

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
