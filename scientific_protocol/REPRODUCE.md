# Reproducibility Protocol

This document outlines the step-by-step procedure to independently reproduce the exact algebraic sieving, phenomenological validation, and formal verification of the 4D K3 String Vacua models proposed in our manuscript.

**Epistemic Stance**: This repository houses a theoretical mathematical derivation, not a claimed observational discovery. We utilize automated exact algebra and formal verification to propose that the $S_{1,2}$ and $S_{2,1}$ K3 surfaces are mathematically viable String Dark Matter vacua. We present the exact macroscopic oscillation frequencies ($\sim 10^{-7}$ Hz) as testable predictions awaiting observational verification.

---

### 1. Algebraic Sieve Verification (Python/Sympy)
**Command**: 
```bash
python3 agora_ai_agents/agent_math_sympy.py
```
**Explanation**: Reproduces the exact rational `sympy.Matrix.nullspace()` extraction. Demonstrates the falsification of 6D symmetric Calabi-Yau and isolates the Order-3 Picard-Fuchs 4D K3 operators ($S_{1,2}$ and $S_{2,1}$).

### 2. Formal Kernel Verification (Lean 4)
**Command**: 
```bash
cd lean4_formal_proofs && lake build Agora
```
**Explanation**: The Lean 4 kernel compiles the exact topological coefficients, mathematically guaranteeing a strictly positive effective mass squared ($m_a^2 > 0$)—proving the vacua are free of tachyonic ghosts.

### 3. Phenomenological Crucible (Astrophysics)
**Command**: 
```bash
python3 agora_ai_agents/agent_astro_pheno.py --evaluate superradiance
```
**Explanation**: Verifies the Chameleon mass-scaling mechanism ($\gamma = 0.25$). Proves the K3 axion is shielded from the M87* superradiance spin-down constraint ($\alpha_{eff} > 0.88$).

---

## Dataset Provenance
- **IC2574 Rotation Curve:** Real SPARC observational data (Lelli et al. 2016).
- **GD-1 Stream Constraints:** Actual gap and spur constraints from Bonaca et al. 2019.
- **M87 Spin Bounds:** Archival spin bounds retrieved from Event Horizon Telescope (EHT 2019) and Cui et al. 2023.
