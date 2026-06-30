#!/usr/bin/env python3
"""
Agora Orchestrator - Project Feynman-Sieve Protocol
Coordinates the AI Swarm across formal algebra, K3 topology, and Lean 4 verification.
"""

import argparse
import subprocess
import sys
import os

def main():
    print("=========================================================")
    print(" Agora Swarm Orchestrator: Project Feynman-Sieve Protocol")
    print(" Hardware Target: T4/A100 - Parallel Sieve Mode")
    print("=========================================================\n")
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    print("[1] Launching Agent A (The Sieve) - SymPy Formal Algebra...")
    try:
        subprocess.run([sys.executable, "agora_ai_agents/agent_feynman_sieve_a.py"], check=True)
    except subprocess.CalledProcessError:
        print("Agent A failed.")
        sys.exit(1)

    print("\n[2] Launching Agent B (The Geometrician) - K3 Topology Mapping...")
    try:
        subprocess.run([sys.executable, "agora_ai_agents/agent_feynman_sieve_b.py"], check=True)
    except subprocess.CalledProcessError:
        print("Agent B failed.")
        sys.exit(1)
        
    print("\n[3] Launching Agent C (The Verifier) - Lean 4 Kernel Proof...")
    try:
        subprocess.run([sys.executable, "agora_ai_agents/agent_feynman_sieve_c.py"], check=True)
    except subprocess.CalledProcessError:
        print("Agent C failed.")
        sys.exit(1)

    print("\n[4] Orchestration Complete. Project Feynman-Sieve protocol execution finished.")

if __name__ == "__main__":
    main()
