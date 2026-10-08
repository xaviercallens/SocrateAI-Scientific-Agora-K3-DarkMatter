#!/usr/bin/env python3
"""
check_paper_tier_language.py -- tier-language lint for LaTeX papers.

Why: scripts/check_tier_language.py (and the hash-pinned mirror it wraps) reads markdown
"## Abstract"/"Summary"/"Overview" sections and the text before the first markdown heading. A .tex
file has no markdown heading, so the wrapper treats the whole file as that preamble and does check it
(tested 2026-10-08 with a planted 'proves': exit 1). This script applies the same check_block() --
the same forbidden phrases and verbs, the same conjecture markers -- to the body of each paper
(\\begin{document}..\\end{document}), with LaTeX comments and the bibliography removed so that a cited
title cannot trip it. Its own addition is one rule from ledger item 10 (D14'): no Kodaira fibre-type
token (I_n, I_n^*, II, III, IV and their starred forms) anywhere in the body, with a narrow, self-tested
allowlist for proper names.

Usage: python3 scripts/check_paper_tier_language.py paper.tex [more.tex ...]
       python3 scripts/check_paper_tier_language.py --selftest
Exit: 0 clean, 1 violations, 2 usage / missing file.
Generated-by: Claude (Opus 5.5), Stream 2, 2026-10-08 | Verified-by: --selftest (planted bad text must fail) | Reviewed-by: N
"""
import importlib.util
import re
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MIRROR = REPO_ROOT / "stream3_mirror" / "scripts" / "check_tier_language.py"
FIBRE_TYPE_RE = re.compile(r"(?<![A-Za-z\\])(I_\{?[0-9n]|I_0\^|II\^?\*|III\^?\*?|IV\^?\*?|\\mathrm\{(II|III|IV)\}|\bII\b)(?![A-Za-z])")


def load_mirror():
    if not MIRROR.exists():
        print(f"FATAL: mirrored checker missing at {MIRROR}")
        sys.exit(2)
    spec = importlib.util.spec_from_file_location("tier_mirror", MIRROR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def body_of(tex):
    m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", tex, re.S)
    if not m:
        raise ValueError("no \\begin{document}..\\end{document}")
    body = re.sub(r"(?<!\\)%.*", "", m.group(1))
    body = re.sub(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", "", body, flags=re.S)
    return body


# proper names that contain a roman numeral and are not fibre types (each one is a self-test case)
NAME_ALLOWLIST = re.compile(r"Eridanus(~|\s+)II")


def check_file(mod, path):
    body = body_of(path.read_text(encoding="utf-8"))
    v = list(mod.check_block(str(path.name), body))
    for m in FIBRE_TYPE_RE.finditer(NAME_ALLOWLIST.sub("Eridanus-two", body)):
        ctx = " ".join(body[max(0, m.start() - 40): m.end() + 40].split())
        v.append(f"[{path.name}] fibre-type token '{m.group(0)}' (ledger item 10): ...{ctx}...")
    return v


def selftest(mod):
    doc = "\\documentclass{article}\\begin{document}%s\\end{document}"
    cases = {"verb": ("The selected point proves the dark sector.", True),
             "fibre": ("The fibre at z=-1 has type $I_2$.", True),
             "fibre2": ("A fibre of type $\\mathrm{IV}^*$ appears.", True),
             "clean": ("We report the transcendental lattice; no fibre type is attached.", False),
             "comment_ignored": ("Clean text. % this line proves nothing\n", False),
             "name_allowlisted": ("The Eridanus~II star cluster is recorded.", False),
             "name_does_not_mask": ("Eridanus~II is recorded; the fibre has type II here.", True)}
    ok = True
    with tempfile.TemporaryDirectory() as td:
        for name, (txt, bad) in cases.items():
            p = Path(td) / f"{name}.tex"
            p.write_text(doc % txt)
            got = bool(check_file(mod, p))
            ok &= got == bad
            print(f"  {'ok  ' if got == bad else 'FAIL'} {name}: flagged={got} expected={bad}")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv):
    mod = load_mirror()
    if "--selftest" in argv:
        return selftest(mod)
    if not argv:
        print(__doc__)
        return 2
    paths = [Path(a) for a in argv]
    missing = [p for p in paths if not p.exists()]
    if missing:
        print("FATAL: missing", missing)
        return 2
    allv = [x for p in paths for x in check_file(mod, p)]
    for x in allv:
        print("  " + x)
    print(f"check_paper_tier_language.py: {'OK' if not allv else 'BLOCKED'} ({len(allv)} violation(s) in {len(paths)} file(s))")
    return 1 if allv else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
