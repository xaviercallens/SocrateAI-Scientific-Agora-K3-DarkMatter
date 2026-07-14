#!/bin/bash
# cross_consistency_check.sh
# Task T8.1: Cross-consistency verification of critical parameters across codebase
# Ensures atomic parameter synchronization per Rule 8 (AGORA_GUIDELINES.md)
# Verifies: w_0, w_a, H_0, ε, axion masses, stiffness ratios, α_eff, PTA periods

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEDGER="${REPO_ROOT}/PARAMETER_LEDGER.yaml"
RESULTS_LOG="${REPO_ROOT}/.consistency_check_results.log"

# Initialize
> "$RESULTS_LOG"
PASS=0 FAIL=0 WARN=0

log() {
    echo "$@" >> "$RESULTS_LOG"
    echo "$@"
}

check() {
    local desc=$1 file=$2 value=$3
    if grep -q "$value" "$file" 2>/dev/null; then
        ((PASS++)) && log "✓ $desc"
    else
        ((FAIL++)) && log "✗ $desc"
    fi
}

log "========================================"; log "Cross-Consistency Check (T8.1)"; log "Repository: $REPO_ROOT"; log "Timestamp: $(date)"; log "========================================"

log ""; log "--- Cosmological Parameters ---"
check "w_0 in ROADMAP.md" "$REPO_ROOT/ROADMAP.md" "0.5485"
check "w_0 in LL.md" "$REPO_ROOT/LL.md" "0.5485"
check "w_a in ROADMAP.md" "$REPO_ROOT/ROADMAP.md" "0.3968"
check "w_a in LL.md" "$REPO_ROOT/LL.md" "0.3968"
check "H_0 in ROADMAP.md" "$REPO_ROOT/ROADMAP.md" "71.92"
check "H_0 in LL.md" "$REPO_ROOT/LL.md" "71.92"

log ""; log "--- Topological Stiffness ---"
check "stiffness_S12=1014 in GaugeCoupling.lean" "$REPO_ROOT/lean4_formal_proofs/Agora/GaugeCoupling.lean" "1014"
check "stiffness_S12=1014 in K3_DISCOVERY_REPORT.md" "$REPO_ROOT/K3_DISCOVERY_REPORT.md" "1014"
check "stiffness_S21=336 in GaugeCoupling.lean" "$REPO_ROOT/lean4_formal_proofs/Agora/GaugeCoupling.lean" "336"
check "stiffness_S21=336 in K3_DISCOVERY_REPORT.md" "$REPO_ROOT/K3_DISCOVERY_REPORT.md" "336"

log ""; log "--- Axion Masses ---"
check "m_a(S₁,₂)=3.18e-21 in K3_DISCOVERY_REPORT.md" "$REPO_ROOT/K3_DISCOVERY_REPORT.md" "3.18"
check "m_a(S₂,₁)=1.83e-21 in K3_DISCOVERY_REPORT.md" "$REPO_ROOT/K3_DISCOVERY_REPORT.md" "1.83"

log ""; log "--- Superradiance Parameters ---"
check "α_eff(S₁,₂)=1.55 in K3_DISCOVERY_REPORT.md" "$REPO_ROOT/K3_DISCOVERY_REPORT.md" "1.55"
check "α_eff(S₂,₁)=0.89 in K3_DISCOVERY_REPORT.md" "$REPO_ROOT/K3_DISCOVERY_REPORT.md" "0.89"

log ""; log "--- PTA Parameters ---"
check "PTA period S₁,₂=7.52d in VISION.md" "$REPO_ROOT/VISION.md" "7.52"
check "PTA period S₂,₁=13.08d in VISION.md" "$REPO_ROOT/VISION.md" "13.08"
check "PTA ratio bounds in GaugeCoupling.lean" "$REPO_ROOT/lean4_formal_proofs/Agora/GaugeCoupling.lean" "1.73"

log ""; log "--- Caveats (Rule 6) ---"
for gap in GAP-1 GAP-2 GAP-3 GAP-4 GAP-5 GAP-6; do
    if grep -q "$gap" "$REPO_ROOT/CAVEATS.md"; then
        ((PASS++)); log "✓ $gap in CAVEATS.md"
    else
        ((FAIL++)); log "✗ $gap not in CAVEATS.md"
    fi
done

log ""; log "--- Phase 8.D: GATE-C Finalist Lean Kernel Verification ---"
LEAN_DIR="$REPO_ROOT/lean4_formal_proofs"
for pair in "CooperS7Recurrence:CooperS7.cooper_s7_recurrence_checked" \
            "CooperS10Recurrence:CooperS10.cooper_s10_recurrence_checked" \
            "T103Recurrence:T103.t103_recurrence_checked"; do
    modname="${pair%%:*}"
    thm="${pair##*:}"
    file="$LEAN_DIR/Structures/${modname}.lean"
    if [ ! -f "$file" ]; then
        ((FAIL++)); log "✗ $modname.lean missing"
        continue
    fi
    if (cd "$LEAN_DIR" && timeout 300 lake build "Structures.${modname}" >/tmp/leanbuild_${modname}.log 2>&1); then
        ((PASS++)); log "✓ $modname.lean builds (kernel-checked, $thm)"
    else
        ((FAIL++)); log "✗ $modname.lean FAILED to build — see /tmp/leanbuild_${modname}.log"
    fi
done
check "GATE-B/C 6-candidate pool frozen" "$REPO_ROOT/data/autoresearch_v2/candidate_pool.yaml" "frozen: true"
check "t103 in candidate pool" "$REPO_ROOT/data/autoresearch_v2/candidate_pool.yaml" "t103"

log ""; log "========================================"; log "Summary: PASS=$PASS FAIL=$FAIL WARN=$WARN"; log "========================================"

if [ "$FAIL" -gt 0 ]; then exit 1; fi
exit 0
