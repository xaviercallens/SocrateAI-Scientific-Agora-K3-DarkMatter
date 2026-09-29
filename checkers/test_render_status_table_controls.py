#!/usr/bin/env python3
"""
test_render_status_table_controls.py -- controls for scripts/render_status_table.py

Standing rule 1: a test that cannot fail is not a test. The sec. 5 table was
once hand-kept and contradicted every certificate; these controls assert the
renderer follows the certificates, and refuses where it should, instead of
emitting stale or wrong text. Every case runs on TEMP COPIES of the criteria
file, certificates, refs and checker names -- never on the real files.

  P0  positive: real inputs render; splice + --check round-trips (exit 0)
  N1  flipped C1 verdict in a certificate -> the rendered cell changes
  N2  source certificate deleted          -> refuse
  N3  in-band RETRACTED block added       -> refuse
  N3b verdict string "RETRACTED ..."      -> refuse
  N4  s10 C1 certificate placed in the s7 slot (candidate mismatch) -> refuse
  N5  DRAFT lattice cert renders DRAFT (ADVISORY), never LIVE/PASS;
      an s7 status flipped to DRAFT renders DRAFT too
  N6  hand-edited sec. 5 -> --check exits 1
  N7  expected field missing (order_checked) -> refuse
  N8  PASS(N) disagreeing with order_checked -> refuse
  N9  register params altered so no refs entry matches -> refuse
  N10 named checker absent from checkers/ (phantom) -> refuse
  N11 C2 status neither LIVE nor DRAFT -> refuse
  N12 byte stability: changed git stamp / timestamp / checker_version -> identical table
  N13 C6 violation injected -> cell reports CHECK FAILURES
  N14 BEGIN/END markers missing -> refuse
  N15 certificate produced by a different checker than the source map names -> refuse
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import render_status_table as rst  # noqa: E402

failures = []


def check(name, cond, detail=""):
    tag = "ok   " if cond else "FAIL "
    print(f"  {tag} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


def all_source_files():
    names, checkers = set(), set()
    for spec in rst.SOURCES.values():
        for entry in spec.get("certs", {}).values():
            if isinstance(entry, tuple):
                names.add(entry[0]); checkers.add(entry[1])
            else:
                names.add(entry); checkers.add(spec["checker"])
    return names, checkers


class Sandbox:
    def __init__(self, root):
        self.root = Path(root)
        self.certs = self.root / "certs"
        self.checkers = self.root / "checkers"
        self.refs = self.root / "recurrences_v1.json"
        self.criteria = self.root / "K3_CRITERIA.md"
        self.certs.mkdir()
        self.checkers.mkdir()
        names, checkers = all_source_files()
        for n in names:
            shutil.copy(REPO_ROOT / "data" / "certificates" / n, self.certs / n)
        for c in checkers:
            (self.checkers / c).write_text("# placeholder name for the phantom guard\n")
        shutil.copy(REPO_ROOT / "refs" / "recurrences_v1.json", self.refs)
        shutil.copy(REPO_ROOT / "K3_CRITERIA.md", self.criteria)

    def edit(self, name, fn):
        f = self.certs / name
        d = json.loads(f.read_text())
        fn(d)
        f.write_text(json.dumps(d, indent=2))

    def render(self):
        return rst.render_table(self.criteria.read_text(), self.certs, self.refs, self.checkers)

    def main(self, *extra):
        return rst.main(["--criteria-file", str(self.criteria), "--certs-dir", str(self.certs),
                         "--refs-file", str(self.refs), "--checkers-dir", str(self.checkers), *extra])


def refuses(sb, needle=""):
    try:
        sb.render()
        return False, "rendered without error"
    except rst.RenderError as e:
        return (needle.lower() in str(e).lower()), str(e)


def fresh():
    return Sandbox(tempfile.mkdtemp(prefix="rst_ctl_"))


# P0
sb = fresh()
base = sb.render()
check("P0 real inputs render", "PASS(" in base and "K-s7" in base)
rc = sb.main()
rc2 = sb.main("--check")
check("P0 splice then --check round-trips", rc == 0 and rc2 == 0, f"write rc={rc}, check rc={rc2}")

# N1
sb = fresh()
sb.edit("C1_mirror_integrality_cooper_s7.json", lambda d: d.update(verdict="FAIL_AT(17)"))
out = sb.render()
check("N1 flipped verdict changes the cell", out != base and "FAIL_AT(17)" in out)

# N2
sb = fresh()
(sb.certs / "C2_cooper_s7_v6.json").unlink()
ok, e = refuses(sb, "missing")
check("N2 deleted source refuses", ok, e)

# N3 / N3b
sb = fresh()
sb.edit("C3b_symsqrt_cooper_s7.json", lambda d: d.update(RETRACTED={"ticket": "CTL"}))
ok, e = refuses(sb, "RETRACTED")
check("N3 RETRACTED block refuses", ok, e)
sb = fresh()
sb.edit("C1_mirror_integrality_cooper_s10.json", lambda d: d.update(verdict="RETRACTED (control)"))
ok, e = refuses(sb, "RETRACTED")
check("N3b RETRACTED verdict refuses", ok, e)

# N4
sb = fresh()
shutil.copy(sb.certs / "C1_mirror_integrality_cooper_s10.json", sb.certs / "C1_mirror_integrality_cooper_s7.json")
ok, e = refuses(sb, "row is")
check("N4 candidate mismatch refuses", ok, e)

# N5 (s10 v5 LIVE since D15' 2026-09-29: the DRAFT rendering is exercised by flipping it back)
s10_line = [l for l in base.splitlines() if l.startswith("| K-s10") and "C2_cooper_s10" in l]
check("N5 s10 lattice (v5 LIVE) renders LIVE, not DRAFT", len(s10_line) == 1
      and "LIVE:" in s10_line[0] and "DRAFT (ADVISORY)" not in s10_line[0])
sb = fresh()
sb.edit("C2_cooper_s10_v5.json", lambda d: d.update(status="DRAFT - control"))
s10_line = [l for l in sb.render().splitlines() if l.startswith("| K-s10") and "C2_cooper_s10" in l]
check("N5 s10 flipped to DRAFT renders DRAFT (ADVISORY), not LIVE", len(s10_line) == 1
      and "DRAFT (ADVISORY)" in s10_line[0] and "LIVE:" not in s10_line[0])
sb = fresh()
sb.edit("C2_cooper_s7_v6.json", lambda d: d.update(status="DRAFT - control"))
s7_line = [l for l in sb.render().splitlines() if l.startswith("| K-s7") and "C2_cooper_s7" in l]
check("N5 s7 flipped to DRAFT renders DRAFT", len(s7_line) == 1 and "DRAFT (ADVISORY)" in s7_line[0]
      and "LIVE:" not in s7_line[0])

# N6
sb = fresh()
sb.main()
t = sb.criteria.read_text()
sb.criteria.write_text(t.replace("`PASS(60)`", "`PASS(200)`", 1))
check("N6 hand-edited sec. 5 -> --check exit 1", sb.main("--check") == 1)

# N7
sb = fresh()
sb.edit("C1_mirror_integrality_cooper_s7.json", lambda d: d.pop("order_checked"))
ok, e = refuses(sb, "order_checked")
check("N7 missing field refuses", ok, e)

# N8
sb = fresh()
sb.edit("C1_mirror_integrality_cooper_s7.json", lambda d: d.update(order_checked=d["order_checked"] + 1))
ok, e = refuses(sb, "disagrees")
check("N8 PASS(N) vs order_checked mismatch refuses", ok, e)

# N9
sb = fresh()
t = sb.criteria.read_text()
check("N9 setup: s7 params present", "params (13,4,−27,3)" in t)
sb.criteria.write_text(t.replace("params (13,4,−27,3)", "params (13,5,−27,3)", 1))
ok, e = refuses(sb, "match 0 refs")
check("N9 unmatched register params refuse", ok, e)

# N10
sb = fresh()
(sb.checkers / "check_T3_level_consistency.py").unlink()
ok, e = refuses(sb, "phantom")
check("N10 absent checker refuses", ok, e)

# N11
sb = fresh()
sb.edit("C2_cooper_s7_v6.json", lambda d: d.update(status="SUPERSEDED v5"))
ok, e = refuses(sb, "neither LIVE nor DRAFT")
check("N11 unknown C2 status refuses", ok, e)

# N12
sb = fresh()
def stamp(d):
    d["git_describe_HEAD"] = "v9.9.9-control"
    d["timestamp_utc"] = "2099-01-01T00:00:00Z"
    d["checker_version"] = "9.9.9"
    d["date"] = "2099-01-01"
for n in all_source_files()[0]:
    sb.edit(n, stamp)
check("N12 stamps do not reach the table", sb.render() == base)

# N13
sb = fresh()
sb.edit("CM_POINTS_RHO20.json",
        lambda d: d["families"]["cooper_s7"]["fricke_consistency_violations"].append({"control": 1}))
check("N13 C6 violation surfaces", "CHECK FAILURES" in sb.render())

# N14
sb = fresh()
sb.criteria.write_text(sb.criteria.read_text().replace(rst.BEGIN, ""))
check("N14 missing marker refuses (exit 2)", sb.main("--check") == 2)

# N15
sb = fresh()
sb.edit("C1_mirror_integrality_cooper_s7.json", lambda d: d.update(checker="check_something_else.py"))
ok, e = refuses(sb, "produced by")
check("N15 wrong producing checker refuses", ok, e)

# N16 -- the optional certified-monodromy note: present and closed -> rendered;
# chain open -> rendered LOUDLY; reference mismatch -> refuse; absent -> no note.
CM7 = "CERTIFIED_MONODROMY_L2_cooper_s7.json"
if (REPO_ROOT / "data" / "certificates" / CM7).exists():
    sb = fresh()
    shutil.copy(REPO_ROOT / "data" / "certificates" / CM7, sb.certs / CM7)
    line = [l for l in sb.render().splitlines() if l.startswith("| K-s7") and "C2_cooper_s7" in l][0]
    check("N16 certified note rendered when chain closed", "monodromy CERTIFIED" in line)
    sb.edit(CM7, lambda d: d["result"].update(chain_closed=False))
    line = [l for l in sb.render().splitlines() if l.startswith("| K-s7") and "C2_cooper_s7" in l][0]
    check("N16 open chain rendered loudly", "certification OPEN" in line and "monodromy CERTIFIED" not in line)
    sb.edit(CM7, lambda d: d["result"]["stage3_from_certified_matrices"].update(reference_certificate="C2_cooper_s7_v3.json"))
    ok, e = refuses(sb, "stage-3 reference")
    check("N16 reference mismatch refuses", ok, e)
    check("N16 absent certificate -> no note", "monodromy" not in base)
else:
    check("N16 skipped: certified-monodromy certificate absent", True)

print()
if failures:
    print(f"FAILED: {len(failures)} control(s): {failures}")
    sys.exit(1)
print("all render_status_table controls passed")
