# Agora Unified Dark Sector: $K3 \times T^2$ Moduli Dynamics
**Automated Derivation of Fuzzy Dark Matter ($K3$) and Thawing Dark Energy ($T^2$) via Exact Algebraic Sieving, Formal Verification, and Empirical Validation.**

**Update (June 26, 2026):** The framework has been successfully extended from Part I (Dark Matter) to Part II (Dark Energy). By coupling the rigid K3 axion to an expanding $T^2$ Torus, we introduce a mass-varying dark matter model that simultaneously resolves the Hubble Tension, the DESI 2024 Quintessence anomaly, the JWST early-galaxy density crisis, and the $S_8$ clustering tension. See the `empirical_crucible` folder for real-data Jupyter validations.

This repository contains the public artifacts, papers, mathematical formalizations, and simulation code for the unified Dark Sector project developed within the SocrateAI Scientific Agora ecosystem.

This repository serves as the definitive reference for the scientific community to review, reproduce, and critically analyze the findings.

## Papers and Preprints

The exact theoretical results and dynamics have been documented in the following preprints, which are available on Zenodo:

- **Part I: Exact Algebraic Identification of K3 String Vacua with Dark Matter**
  - **DOI/Link:** [10.5281/zenodo.20863378](https://zenodo.org/deposit/20863378)
  - **File:** `manuscripts_and_proofs/Part_I_K3_DarkMatter.pdf`
- **Part II: Project Vafa-Continuity: $K3 \times T^2$ Moduli Dynamics & The Dark Energy Equation of State**
  - **DOI/Link:** [10.5281/zenodo.20863381](https://zenodo.org/deposit/20863381)
  - **File:** `manuscripts_and_proofs/Part_II_Vafa_DarkEnergy.pdf`

## Directory Structure

- `PREDICTIONS.md`: Falsifiable predictions for Euclid, ELT, LISA.
- `CAVEATS.md`: The Epistemic road map (Moduli stabilization, $f_b=0.05$).
- `agora_ai_agents/`: The Swarm Architecture (`orchestrator.py`, `agent_math_sympy.py`, `agent_vafa.py`, `agent_empirica.py`).
- `lean4_formal_proofs/`: All Kernel verified math (Stability + Swampland). We strictly adhere to the 'No Simulation' rule, relying on formal theorem proving to establish mathematical truths.
- `manuscripts_and_proofs/`: The Zenodo Preprints (Part I & Part II PDFs).
- `empirical_crucible/`: Real Telescope Data Validation, including the Master Notebook (`Agora_Empirical_Validation.ipynb`) and cached datasets.
- `simulations/`: Contains the exact numerical physics scripts (e.g., SymPy exact integration, Vlasov equation solvers) to track the time evolution.
- `vlasov_data/`: Contains the `Vlasov` simulation datasets.
- `.agents/`: Contains the configurations, skills, and prompts for the autonomous AI agents.

## Empirical Validation against JWST, DES, and Quasar Catalogs

Standard cosmologists treat the JWST early galaxy crisis and the DES Y3 $S_8$ clustering crisis as separate anomalies. Our empirical notebook demonstrates they are the exact same phenomenon. By parsing real observational data (UNCOVER catalog and Webb-Murphy quasar data), we mathematically link the birth of the first stars to the modern smoothness of the cosmic web using a single expanding String Theory Torus.

Explore the executable code, raw data parsing, and scientific caveats in our Jupyter Notebook:
- **[Agora Empirical Validation Notebook](empirical_crucible/Agora_Empirical_Validation.ipynb)**

For testable predictions targeting upcoming observatories (Euclid, ELT, LISA), read the **[Future Manifest (PREDICTIONS.md)](PREDICTIONS.md)**.

## Reproduction Procedure

We welcome scientific peer review, controversy analysis, and robust criticism. To reproduce the mathematical and numerical results in this repository:

### 1. Mathematical Formalization (Lean 4)
All theorems and definitions have been mechanically verified without any `sorry` stubs.
1. Install [Lean 4](https://leanprover.github.io/lean4/doc/setup.html) and `lake`.
2. Ensure the `lean-toolchain` is respected.
3. Run the following command from the repository root:
   ```bash
   lake build Agora
   ```
   A successful build with zero errors validates the proofs.

### 2. Numerical Physics (Python/SymPy)
Physical benchmarking is strictly backed by execution data.
1. Install Python 3.12 or newer.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute the simulation solvers located in the `simulations/` directory (e.g., `python simulations/vlasov_solver.py` or equivalent ODE integrators). The simulation scripts will precisely reproduce the sequence generation and physical parameters referenced in the papers.

## AI Agents and Rules

This project employed autonomous AI agents governed by strict rules, notably:
- **No Simulation Rule:** Never report benchmark or performance metrics without hard execution data.
- **Strict Formalization Rule:** Never consider a mathematical theorem 'proven' unless verified by the Lean 4 kernel.

The configurations for these agents can be explored in the `.agents/` directory.

## License and Contribution
Open for scientific scrutiny. Please open issues or submit pull requests with formal Lean 4 counter-proofs or corrections to the numerical solvers.

Copyright (C) 2026 Xavier Callens (SocrateAI Scientific Agora).
All rights reserved. No part of this work may be reproduced, distributed, or transmitted in any form or by any means without prior written permission from the author.
