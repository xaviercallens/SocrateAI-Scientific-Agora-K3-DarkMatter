#!/usr/bin/env bash
# restart_session.sh — Quick-context reload for resuming K3xT2 work tomorrow.
#
# Run this at the start of a new session (Haiku, Sonnet, or Fable) to get an
# immediate, accurate picture of where things stand: last commits, open GATE
# items, the last journal epoch, and live verification of the kernel engine
# so you know the ground truth hasn't drifted since last session.
#
# Usage: bash scripts/restart_session.sh

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BOLD}=========================================================${NC}"
echo -e "${BOLD}  K3xT2 SESSION RESTART — $(date '+%Y-%m-%d %H:%M %Z')${NC}"
echo -e "${BOLD}=========================================================${NC}"

echo -e "\n${BOLD}--- Git: last 8 commits ---${NC}"
git log --oneline -8

echo -e "\n${BOLD}--- Git: working tree status ---${NC}"
git status --short || echo "(clean)"

echo -e "\n${BOLD}--- Live re-verification (ground truth, not narrative) ---${NC}"

echo -e "\n${YELLOW}[1/3] Kernel engine self-test (sequences vs Lean recurrences vs OEIS)...${NC}"
if python3 lss_tensor_analytics/k3_kernel_engine.py > /tmp/k3_kernel_check.log 2>&1; then
    echo -e "${GREEN}  PASS${NC} — all kernels verified. See /tmp/k3_kernel_check.log for detail."
else
    echo -e "${RED}  FAIL${NC} — kernel engine self-test broke since last session! Check /tmp/k3_kernel_check.log immediately."
    tail -20 /tmp/k3_kernel_check.log
fi

echo -e "\n${YELLOW}[2/3] Lean: CooperS7_Topology.lean (math-only, replaces quarantined K3Geometry file)...${NC}"
if command -v lake >/dev/null 2>&1 || [ -x "$HOME/.elan/bin/lake" ]; then
    LAKE_BIN="${HOME}/.elan/bin/lake"
    ( cd lean4_formal_proofs && timeout 180 "$LAKE_BIN" env lean Structures/CooperS7_Topology.lean > /tmp/lean_check.log 2>&1 )
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}  PASS${NC} (exit 0)"
    else
        echo -e "${RED}  FAIL${NC} — see /tmp/lean_check.log"
    fi
else
    echo -e "${YELLOW}  SKIPPED${NC} — lake not found at \$HOME/.elan/bin/lake"
fi

echo -e "\n${YELLOW}[3/3] GATE D-1 kernel-swap verdict (cached result, not rerun — rerun costs ~10s if you want fresh):${NC}"
if [ -f data/k3t2/d1_3_kernel_swap.json ]; then
    python3 -c "
import json
with open('data/k3t2/d1_3_kernel_swap.json') as f:
    d = json.load(f)
print(f\"  Verdict: {d['preregistered_verdict']}\")
print(f\"  (from {d['timestamp']})\")
"
else
    echo "  No cached result — run: python3 scripts/k3t2_kernel_swap_battery.py"
fi

echo -e "\n${BOLD}--- Where things stand (TODO.md, Phase 8.D-ext) ---${NC}"
awk '/### Phase 8.D-ext/,/### Phase 8.E/' TODO.md | head -n -1

echo -e "\n${BOLD}--- Last journal epoch (JOURNAL.md) ---${NC}"
awk '/^### Epoch/{e=$0} END{print e}' JOURNAL.md
echo "  (full entry: see JOURNAL.md, search for the epoch title above)"

echo -e "\n${BOLD}--- Immediate next steps ---${NC}"
cat <<'EOF'
  GATE D-1 verdict is F1_FAILS_KERNEL_BLIND: the FFT-contrast observable
  cannot distinguish real K3 kernels from unstructured noise. Before any
  further empirical work (D-3: tomography/TDA/lensing), the observable
  itself needs redesigning. Candidate directions already logged in
  TODO.md / data/k3t2/GATE_D1_DECISION.md:
    - use phase structure of Pi_0(z), not just |Pi_0(z)|
    - compare local z to the D-2.4 singular loci (1/27 for s7, 1/16 for s10)
      rather than a generic FFT contrast against raw density

  Remaining GATE D-2 theory tasks (Sonnet tier), not yet started:
    - D-2.1: resolve m_eff(Delta) contradiction (exp(k*Delta) vs (1+k*Delta)^0.25)
    - D-2.2: derive or parameterize rho_b -> z density-to-modulus map
    - D-2.3: T^2 KK-lattice module (Python + Lean math-only)

  Full plan: K3xT2_DEEP_IMPROVEMENT_PLAN.md
  Sonnet handoff doc: GATE_D2_SONNET_HANDOFF.md
EOF

echo -e "\n${BOLD}--- Memory files relevant to this project ---${NC}"
MEMDIR="/home/callensxavier_gmail_com/.claude/projects/-home-callensxavier-gmail-com-SocrateAI-Scientific-Agora-K3-DarkMatter/memory"
if [ -f "$MEMDIR/MEMORY.md" ]; then
    cat "$MEMDIR/MEMORY.md"
else
    echo "  (memory index not found at $MEMDIR)"
fi

echo -e "\n${BOLD}=========================================================${NC}"
echo -e "${BOLD}  Restart context loaded. Ready to continue.${NC}"
echo -e "${BOLD}=========================================================${NC}"
