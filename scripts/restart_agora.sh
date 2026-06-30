#!/bin/bash
# SocrateAI Agora Restart & Environment Control Script
# Save as scripts/restart_agora.sh

set -e

# Setup colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

BASE_DIR="/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-K3-DarkMatter"
VENV_DIR="$BASE_DIR/empirical_crucible/venv"

echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}             SocrateAI Scientific Agora Management System            ${NC}"
echo -e "${BLUE}======================================================================${NC}"

# Check for virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}Error: Virtual environment not found at $VENV_DIR${NC}"
    exit 1
fi

activate_env() {
    echo -e "${BLUE}[+] Activating virtual environment...${NC}"
    source "$VENV_DIR/bin/activate"
}

start_dashboard() {
    activate_env
    echo -e "${GREEN}[+] Starting Interactive Cosmological Fitter Dashboard (Dash)...${NC}"
    echo -e "${YELLOW}Dashboard will run in the background. Access it locally on http://127.0.0.1:8050${NC}"
    python3 "$BASE_DIR/empirical_crucible/app.py" &
    DASH_PID=$!
    echo $DASH_PID > "$BASE_DIR/empirical_crucible/dashboard.pid"
    echo -e "${GREEN}[+] Dashboard launched with PID: $DASH_PID${NC}"
}

run_mcmc() {
    activate_env
    echo -e "${GREEN}[+] Starting JAX/NumPyRo MCMC Cosmological Optimizer...${NC}"
    python3 "$BASE_DIR/empirical_crucible/jax_inference.py"
}

compile_manuscripts() {
    echo -e "${GREEN}[+] Compiling Part III Feynman-K3 Mapping Preprint to PDF...${NC}"
    cd "$BASE_DIR/manuscripts_and_proofs"
    pdflatex -interaction=nonstopmode Part_III_Feynman_K3_Mapping.tex
    bibtex Part_III_Feynman_K3_Mapping
    pdflatex -interaction=nonstopmode Part_III_Feynman_K3_Mapping.tex
    pdflatex -interaction=nonstopmode Part_III_Feynman_K3_Mapping.tex
    echo -e "${GREEN}[+] Part_III_Feynman_K3_Mapping.pdf compiled successfully!${NC}"
    cd "$BASE_DIR"
}

run_peer_review() {
    echo -e "${GREEN}[+] Running 3-Persona Peer Review Audit...${NC}"
    python3 "$BASE_DIR/scripts/conduct_peer_review.py"
}

verify_all() {
    activate_env
    echo -e "${BLUE}[+] Checking system health and GPU status...${NC}"
    if command -v nvidia-smi &> /dev/null; then
        echo -e "${GREEN}[+] GPU detected:${NC}"
        nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv
    else
        echo -e "${YELLOW}[!] CUDA GPU not detected, utilizing high-performance CPU cores.${NC}"
    fi

    echo -e "${BLUE}[+] Checking Lean 4 compiler version...${NC}"
    if command -v lean &> /dev/null; then
        lean --version
    else
        echo -e "${YELLOW}[!] Lean 4 compiler not found in standard PATH.${NC}"
    fi
}

# Main menu
echo -e "Choose an option to execute:"
echo -e "  ${YELLOW}1)${NC} Launch Interactive Dashboard (Dash)"
echo -e "  ${YELLOW}2)${NC} Run JAX MCMC Cosmological Fitting"
echo -e "  ${YELLOW}3)${NC} Recompile LaTeX Manuscripts"
echo -e "  ${YELLOW}4)${NC} Execute 3-Persona Peer Reviews"
echo -e "  ${YELLOW}5)${NC} Verify System & Environment Status"
echo -e "  ${YELLOW}6)${NC} Stop Running Dashboard"
echo -ne "Select [1-6]: "

read -r opt

case $opt in
    1)
        start_dashboard
        ;;
    2)
        run_mcmc
        ;;
    3)
        compile_manuscripts
        ;;
    4)
        run_peer_review
        ;;
    5)
        verify_all
        ;;
    6)
        if [ -f "$BASE_DIR/empirical_crucible/dashboard.pid" ]; then
            PID=$(cat "$BASE_DIR/empirical_crucible/dashboard.pid")
            echo -e "${BLUE}[+] Stopping dashboard PID: $PID${NC}"
            kill $PID || true
            rm -f "$BASE_DIR/empirical_crucible/dashboard.pid"
            echo -e "${GREEN}[+] Dashboard stopped.${NC}"
        else
            echo -e "${RED}No dashboard PID file found.${NC}"
        fi
        ;;
    *)
        echo -e "${RED}Invalid option.${NC}"
        exit 1
        ;;
esac
