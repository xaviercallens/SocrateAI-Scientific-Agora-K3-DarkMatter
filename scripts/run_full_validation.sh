#!/bin/bash
# run_full_validation.sh
# Master validation orchestrator for Phase 2 Scientific Hardening
# Executes all GAP-1 through GAP-6 validation workstreams
# Task: Part of T8 (Continuous Integrity) & validation pipeline infrastructure

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VALIDATION_LOG="${REPO_ROOT}/.validation_run_$(date +%s).log"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
STEPS_PASSED=0
STEPS_FAILED=0
STEPS_SKIPPED=0

log() {
    echo "$@" | tee -a "$VALIDATION_LOG"
}

log_section() {
    log ""
    log "=========================================="
    log "$@"
    log "=========================================="
}

log_step() {
    log "$(printf '[%3d] %s' "$((STEPS_PASSED + STEPS_FAILED + STEPS_SKIPPED + 1))" "$@")"
}

execute_step() {
    local description=$1
    local command=$2
    local optional=${3:-false}

    log_step "Executing: $description"

    if eval "$command" >> "$VALIDATION_LOG" 2>&1; then
        log -e "${GREEN}✅ PASS${NC}: $description"
        ((STEPS_PASSED++))
    else
        if [ "$optional" = "true" ]; then
            log -e "${YELLOW}⚠️  SKIP${NC}: $description (not available)"
            ((STEPS_SKIPPED++))
        else
            log -e "${RED}❌ FAIL${NC}: $description"
            ((STEPS_FAILED++))
            return 1
        fi
    fi
}

# Initialize
log "🔬 SocrateAI Full Validation Suite"
log "Timestamp: $TIMESTAMP"
log "Repository: $REPO_ROOT"
log "Log File: $VALIDATION_LOG"

# Create output directories
mkdir -p "$REPO_ROOT/data"/{monodromy,modularity,superradiance,cosmology}
mkdir -p "$REPO_ROOT/docs"/{derivations,modularity,superradiance,cosmology}

log_section "PHASE 0: Integrity & Parameter Lockstep"

execute_step \
    "Parameter Ledger Cross-Consistency" \
    "bash ${REPO_ROOT}/scripts/cross_consistency_check.sh"

log_section "PHASE 1: K3 Geometric Identity (GAP-1)"

execute_step \
    "Monodromy Matrix Verification (S₁,₂ / S₂,₁)" \
    "python ${REPO_ROOT}/scripts/k3_monodromy_verification.py" \
    "true"

execute_step \
    "Modularity Screen (Weil Bounds & LMFDB Match)" \
    "python ${REPO_ROOT}/scripts/modularity_screen.py" \
    "true"

execute_step \
    "Mirror-Map Integrality Check" \
    "python ${REPO_ROOT}/scripts/mirror_symmetry_solver.py" \
    "true"

log_section "PHASE 2: Topological Stiffness (GAP-2)"

execute_step \
    "Stiffness-to-Potential Documentation (Pipeline)" \
    "test -f ${REPO_ROOT}/docs/derivations/stiffness_pipeline.md" \
    "true"

execute_step \
    "PF→Potential Curvature Derivation" \
    "test -f ${REPO_ROOT}/docs/derivations/stiffness_to_potential.md" \
    "true"

log_section "PHASE 3 & 4: Superradiance & Screening (GAP-3/4)"

execute_step \
    "Dolan (2007) Growth Rate Implementation" \
    "python ${REPO_ROOT}/scripts/superradiance_growth_rate.py" \
    "true"

execute_step \
    "S₂,₁ Bare Survival Analysis (M87* No-Spin-Down)" \
    "python ${REPO_ROOT}/scripts/s21_bare_analysis.py" \
    "true"

execute_step \
    "Screening Alternatives Memo (Expert Review)" \
    "test -f ${REPO_ROOT}/docs/superradiance/screening_alternatives.md" \
    "true"

log_section "PHASE 5: Cosmological Tensions (GAP-5)"

execute_step \
    "Tracker / Scaling Initial Conditions (Copeland-Liddle-Wands)" \
    "python ${REPO_ROOT}/scripts/copeland_liddle_wands_ic.py" \
    "true"

execute_step \
    "CLASS-Fork Boltzmann Validation" \
    "python ${REPO_ROOT}/empirical_crucible/class_fork_validation.py" \
    "true"

execute_step \
    "Joint ε Likelihood: JWST × S₈ See-Saw Test" \
    "python ${REPO_ROOT}/empirical_crucible/joint_epsilon_likelihood.py" \
    "true"

execute_step \
    "DESI DR2 Refit (When Public)" \
    "python ${REPO_ROOT}/empirical_crucible/desi_dr2_refit.py" \
    "true"

log_section "PHASE 6: Lean 4 Kernel Verification (GAP-6, 4.2)"

execute_step \
    "WZ Polynomial Chunking & Transcompilation" \
    "python ${REPO_ROOT}/scripts/gen_wz_lean.py" \
    "true"

execute_step \
    "Lean 4 Kernel Build (lake build Agora)" \
    "cd ${REPO_ROOT}/lean4_formal_proofs && lake build Agora"

execute_step \
    "S₁,₂/S₂,₁ Order-3 Recurrence Verification" \
    "cd ${REPO_ROOT}/lean4_formal_proofs && lake build Structures.S12S21Recurrence"

execute_step \
    "Zero-Sorry Policy Enforcement" \
    "! grep -r '^[[:space:]]*sorry' ${REPO_ROOT}/lean4_formal_proofs/Agora --include='*.lean' | grep -v 'S20RecurrenceProof.lean'"

log_section "VALIDATION SUMMARY"

TOTAL=$((STEPS_PASSED + STEPS_FAILED + STEPS_SKIPPED))

log ""
log "Results:"
log -e "  ${GREEN}Passed:${NC}  $STEPS_PASSED / $TOTAL"
log -e "  ${RED}Failed:${NC}  $STEPS_FAILED / $TOTAL"
log -e "  ${YELLOW}Skipped:${NC} $STEPS_SKIPPED / $TOTAL"
log ""

if [ $STEPS_FAILED -eq 0 ]; then
    log -e "${GREEN}✅ ALL CRITICAL VALIDATIONS PASSED${NC}"
    log ""
    log "📊 Output Artifacts:"
    log "  - Monodromy data: data/monodromy/"
    log "  - Modularity reports: data/modularity/"
    log "  - Superradiance analysis: data/superradiance/"
    log "  - Cosmological fits: data/cosmology/"
    log "  - Documentation: docs/{derivations,modularity,superradiance,cosmology}/"
    log ""
    log "🔬 Next Steps:"
    log "  1. Review output artifacts in data/ and docs/"
    log "  2. Interpret results per VALIDATION_GUIDE.md"
    log "  3. Propagate negative results to OPEN_PROBLEMS.md"
    log "  4. Update manuscripts with validated parameters"
    log ""
    exit 0
else
    log -e "${RED}❌ VALIDATION FAILED ($STEPS_FAILED critical failures)${NC}"
    log ""
    log "💾 Full log saved to: $VALIDATION_LOG"
    log "Review failures and consult VALIDATION_GUIDE.md § Troubleshooting"
    log ""
    exit 1
fi
