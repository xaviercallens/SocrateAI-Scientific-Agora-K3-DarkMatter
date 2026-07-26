#!/usr/bin/env python3
"""
check_tier_language.py (Agora-repo wrapper) — tier-language lint that HONORS
its file arguments.

Why this exists (ESCALATIONS.md E-016): the mirrored checker at
stream3_mirror/scripts/check_tier_language.py silently IGNORES CLI file
arguments — `run_check()` only globs its own repo-root *.md (which in this
tree is stream3_mirror/). Every "checked file X" claim made by passing paths
to it was vacuous. The mirror copy is hash-pinned (T0 D3) and must not be
edited; this wrapper reuses its check_text() verbatim and adds honest CLI
semantics:

  with file args     : check exactly those files; a MISSING file is exit 2
                       (halt, don't skip — WP-E review item D)
  without args       : scan this repo's root *.md and briefs/*.md
  --selftest         : mirror's selftest PLUS a control asserting file-args
                       mode actually reads the named file (the control whose
                       absence let E-016 survive)

Exit codes: 0 clean · 1 violations · 2 usage/missing-file.
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MIRROR = REPO_ROOT / "stream3_mirror" / "scripts" / "check_tier_language.py"


def load_mirror():
    if not MIRROR.exists():
        print(f"FATAL: mirrored checker missing at {MIRROR} — halting (not skipping).")
        sys.exit(2)
    spec = importlib.util.spec_from_file_location("tier_mirror", MIRROR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_paths(mod, paths):
    missing = [p for p in paths if not p.exists()]
    if missing:
        print("FATAL: file(s) not found — halting (not skipping):")
        for p in missing:
            print(f"  {p}")
        sys.exit(2)
    total = []
    for p in paths:
        for v in mod.check_text(p.read_text(encoding="utf-8")):
            try:
                shown = p.relative_to(REPO_ROOT)
            except ValueError:
                shown = p
            total.append(f"{shown}: {v}")
    if total:
        print("BLOCKED by check_tier_language (epistemic-guardrails Finding F-A):")
        for v in total:
            print(f"  {v}")
        return 1
    print(f"check_tier_language.py: OK (0 violations in {len(paths)} file(s))")
    return 0


def run_selftest(mod):
    # 1) the mirror's own three control cases
    assert mod.run_selftest() == 0
    # 2) THE E-016 CONTROL: file-args mode must actually read the named file.
    with tempfile.TemporaryDirectory() as td:
        bad = Path(td) / "bad.md"
        bad.write_text("This rigidly locks the dark sector.\n\n# Body\nrest\n")
        rc = check_paths(mod, [bad])
        assert rc == 1, "file-args mode did not flag a known-bad file (E-016 regression)"
    print("wrapper self-test: PASS (mirror 3/3 + E-016 file-args control)")
    return 0


def main():
    mod = load_mirror()
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    if "--selftest" in sys.argv[1:]:
        return run_selftest(mod)
    if args:
        return check_paths(mod, [Path(a) for a in args])
    paths = sorted(REPO_ROOT.glob("*.md")) + sorted((REPO_ROOT / "briefs").glob("*.md"))
    return check_paths(mod, paths)


if __name__ == "__main__":
    sys.exit(main())
