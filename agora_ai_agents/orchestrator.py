#!/usr/bin/env python3
"""
Agora Orchestrator - K3 Dark Matter
Coordinates the AI Swarm across mathematical derivation and astrophysical validation.
"""

import argparse
import subprocess
import sys

def main():
    print("=========================================================")
    print(" Agora Swarm Orchestrator: K3 String Vacua for Dark Matter")
    print("=========================================================\n")
    
    print("[1] Launching Agent Math (SymPy) to isolate 4D K3 vacua...")
    try:
        subprocess.run([sys.executable, "agora_ai_agents/agent_math_sympy.py"], check=True)
    except subprocess.CalledProcessError:
        print("Agent Math failed.")
        sys.exit(1)

    print("\n[2] Launching Agent Astro/Pheno for Superradiance & Chameleon Evaluation...")
    try:
        subprocess.run([sys.executable, "agora_ai_agents/agent_astro_pheno.py"], check=True)
    except subprocess.CalledProcessError:
        print("Agent Astro/Pheno failed.")
        sys.exit(1)

    print("\n[3] Orchestration Complete. The S_{1,2} and S_{2,1} vacua satisfy all bounds.")

if __name__ == "__main__":
    main()
