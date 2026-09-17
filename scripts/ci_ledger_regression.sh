#!/usr/bin/env bash
# ci_ledger_regression.sh -- the TODO.md "Regression" block plus every checkers/test_*.py
# control suite, as one fail-closed command. Runnable locally now. Intended to become Gate B
# of agora-ci-gate.yml, replacing scripts/cross_consistency_check.sh (T0 decision 2026-09-17;
# that script asserts retracted pre-ledger values). The workflow change is committed on local
# branch ci/fix-gates-2026-09-17 and waits for a GitHub token with `workflow` scope.
#
# Standing rule 1: this runner must be able to fail. `--self-test` asserts an all-passing
# list exits 0 AND a list with one failing command exits nonzero. CI runs it first.
#
# Exit: 0 all green; 1 at least one command failed; 3 self-test did not detect failure.
#
# Generated-by: Claude (Opus 5), Stream 2 | Verified-by: --self-test + clean-clone run |
# Reviewed-by: N
set -u
cd "$(dirname "$0")/.."
LOG=$(mktemp)

COMMANDS=(
  "checkers/check_L3_irreducible_minimal.py"
  "checkers/check_C2_transcendental_rank.py"
  "checkers/check_s7_partner_integrality_modular.py"
  "checkers/check_neron_severi_ambient.py"
  "checkers/check_s7_hauptmodul_gamma07plus.py"
  "scripts/check_tier_language.py"
  "checkers/check_U1_lattice.py"
  "checkers/check_U1_witness_serialization.py --all"
  "checkers/independent_rederivation_C2_s10_v4.py"
  "checkers/independent_rederivation_C2_s10_v4_controls.py"
  "checkers/spike_disc_form_vs_atkin_lehner.py"
  "checkers/check_C1_mirror_integrality.py --order 30"
)
for t in checkers/test_*.py; do
  COMMANDS+=("$t")
done

run_all() {
  local failed=0
  for c in "$@"; do
    local start=$SECONDS
    # shellcheck disable=SC2086
    if python3 $c > "$LOG" 2>&1; then
      printf 'PASS  %4ss  %s\n' "$((SECONDS - start))" "$c"
    else
      printf 'FAIL  %4ss  %s\n' "$((SECONDS - start))" "$c"
      tail -20 "$LOG" | sed 's/^/      | /'
      failed=$((failed + 1))
    fi
  done
  echo "----"
  echo "$(( $# - failed )) passed, ${failed} failed, $# total"
  [ "$failed" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  tmp=$(mktemp -d)
  printf 'import sys\nsys.exit(0)\n' > "$tmp/ok.py"
  printf 'import sys\nsys.exit(1)\n' > "$tmp/bad.py"
  if ! run_all "$tmp/ok.py" "$tmp/ok.py"; then
    echo "SELF-TEST FAILED: runner reported failure for all-passing commands"
    exit 3
  fi
  if run_all "$tmp/ok.py" "$tmp/bad.py"; then
    echo "SELF-TEST FAILED: runner reported success with a failing command"
    exit 3
  fi
  rm -rf "$tmp"
  echo "SELF-TEST OK: all-pass -> 0, one failure -> nonzero"
  exit 0
fi

run_all "${COMMANDS[@]}" || exit 1
