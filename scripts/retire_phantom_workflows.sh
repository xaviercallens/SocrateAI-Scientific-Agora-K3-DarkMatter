#!/usr/bin/env bash
# retire_phantom_workflows.sh -- remove the three phantom Lean workflows (T0 decision D22', 2026-10-07).
#
# Why a script: agent sessions are blocked from editing .github/workflows/ by the permission classifier,
# so T0 runs this once from an ordinary shell. It touches ONLY the three files named below, refuses to run
# in a Claude worktree or on a dirty tree, and never force-pushes.
#
# The three files build nonexistent Agora.PartIV.* Lake targets and grep "error" in Lake's own warning
# text, so they are red on every trigger; part4-proofs.yml additionally #checks names of retracted
# "theorems". None is a merge gate -- the Agora CI Gate (agora-ci-gate.yml) is (standing rule 6).
#
# Usage:
#   scripts/retire_phantom_workflows.sh --dry-run    # show what would happen
#   scripts/retire_phantom_workflows.sh              # git rm + commit on main + push origin main
#   scripts/retire_phantom_workflows.sh --no-push    # commit only
set -euo pipefail

FILES=(
  .github/workflows/part4-proofs.yml
  .github/workflows/lean4-compile.yml
  .github/workflows/lean4-ci.yml
)
DRY=0; PUSH=1
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --no-push) PUSH=0 ;;
    *) echo "unknown option: $a" >&2; exit 2 ;;
  esac
done

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "not inside a git repository" >&2; exit 1; }
cd "$ROOT"
case "$ROOT" in
  */.claude/worktrees/*) echo "refusing: run this from the main checkout, not a Claude worktree ($ROOT)" >&2; exit 1 ;;
esac
if [ -n "$(git status --porcelain)" ]; then
  echo "refusing: working tree is not clean; commit or stash first" >&2; git status --short; exit 1
fi
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [ "$BRANCH" != "main" ]; then
  echo "refusing: on branch '$BRANCH'; run 'git switch main' first" >&2; exit 1
fi

echo "fetching origin/main ..."
git fetch origin main
git merge --ff-only origin/main

PRESENT=()
for f in "${FILES[@]}"; do
  if [ -f "$f" ]; then PRESENT+=("$f"); else echo "already absent: $f"; fi
done
if [ "${#PRESENT[@]}" -eq 0 ]; then
  echo "nothing to do: all three phantom workflows are already gone"; exit 0
fi

echo "will remove:"; printf '  %s\n' "${PRESENT[@]}"
echo "will keep: $(ls .github/workflows | grep -v -e part4-proofs.yml -e lean4-compile.yml -e lean4-ci.yml | tr '\n' ' ')"
if [ "$DRY" -eq 1 ]; then echo "(dry run; no changes made)"; exit 0; fi

git rm -q -- "${PRESENT[@]}"
git commit -q -m "Retire three phantom Lean workflows (D22', 2026-10-07)

part4-proofs.yml, lean4-compile.yml, lean4-ci.yml built nonexistent Agora.PartIV.* targets and
grepped 'error' in Lake's own warning text, so they were red on every trigger; part4-proofs.yml also
#checked names of retracted theorems. Not merge gates: the Agora CI Gate (agora-ci-gate.yml) is
(standing rule 6). Record: briefs/T0_DECISIONS_2026_10_07_STREAM2_DELEGATED.md (D22')."
echo "committed $(git rev-parse --short HEAD) on main"

if [ "$PUSH" -eq 1 ]; then
  echo "pushing to origin main ..."
  if ! git push origin main; then
    echo "push refused. If the error mentions the 'workflow' scope, push with SSH or a token that has it:" >&2
    echo "  git push git@github.com:xaviercallens/SocrateAI-Scientific-Agora-K3-DarkMatter.git main" >&2
    exit 1
  fi
  echo "done. Optional: in GitHub -> Actions, disable the three stale workflow entries so their last red runs stop showing."
else
  echo "not pushed (--no-push). Push later with: git push origin main"
fi
