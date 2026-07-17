#!/usr/bin/env bash
# PreToolUse guard for Edit|Write. Reads hook JSON on stdin.
set -euo pipefail
payload=$(cat)
file=$(echo "$payload" | jq -r '.tool_input.file_path // empty')
[ -z "$file" ] && exit 0
base=$(basename "$file")

if [ "$base" = "K3_CRITERIA.md" ] && [ -f "$file" ] && grep -q 'FROZEN' "$file"; then
  echo "BLOCKED by freeze_guard: K3_CRITERIA.md is FROZEN. Use the amendment protocol (K3_CRITERIA §6): amendment PR with motivation, diff, invalidated-rankings list. Do not edit the frozen file directly." >&2
  exit 2
fi

if [ "$base" = "STATUS_TABLE.md" ] || echo "$file" | grep -q 'certificates/'; then
  echo "BLOCKED by freeze_guard: '$file' is machine-generated (checker certificates / render_status_table.py). Hand edits are an integrity incident per K3_CRITERIA §5. Regenerate via the script." >&2
  exit 2
fi
exit 0
