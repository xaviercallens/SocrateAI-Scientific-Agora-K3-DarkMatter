# Agora Dark Sector: A String-Inspired $K3 \times T^2$ Phenomenological Model
**String-inspired effective field theories (EFTs) for Fuzzy Dark Matter ($K3$) and thawing quintessence ($T^2$), built via exact algebraic sieving, targeted Lean 4 formal verification, and empirical validation.**

**Scope note:** This is a *string-inspired phenomenological model*, not a top-down string compactification. We identify K3-surface EFT candidates by an exact-rational algebraic sieve; we do **not** claim a complete vacuum (orientifold/flux/tadpole) construction. See `OPEN_PROBLEMS.md` for the precise list of what is and is not established.

**Update (June 28, 2026):** The framework spans Part I (Dark Matter) and Part II (Dark Energy). Coupling the rigid K3 axion to an expanding $T^2$ modulus gives a mass-varying dark-matter model that is *suggestive* for the Hubble, JWST early-galaxy, and $S_8$ tensions. For the DESI 2024 quintessence data the best-fit trajectory is thawing but lies **outside** the 1$\sigma$ contour — and, more importantly, the model exhibits a genuine **Swampland tension with stable dark energy** (quintessence here is necessarily transient). See `empirical_crucible` for real-data Jupyter validations and `scripts/` for the exact-arithmetic checks.

This repository contains the public artifacts, papers, mathematical formalizations, and simulation code for the unified Dark Sector project developed within the SocrateAI Scientific Agora ecosystem.

This repository serves as the definitive reference for the scientific community to review, reproduce, and critically analyze the findings.

## Official Publication & Citation

The consolidated core theory has been officially published on Zenodo (July 14, 2026). Please use the following citation for the unified framework:

> Callens, X. (2026). Topological Phase Cosmology (Parts I & II): Exact-Rational Sieve for K3 Fuzzy Dark Matter and Swampland Quintessence Bounds (Version 1.0.0-Core-Theory) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.21350629

**DOI:** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21350629.svg)](https://doi.org/10.5281/zenodo.21350629)

## Papers and Preprints

The exact theoretical results and dynamics are split into two major parts:

- **Part I: String-Inspired Effective Field Theories from K3 Surfaces: Resolving Fuzzy Dark Matter Tensions via Exact Algebraic Sieving**
  - **File:** `manuscripts_and_proofs/Part_I_K3_DarkMatter.pdf`
- **Part II: Project Vafa-Continuity: A String-Inspired $K3 \times T^2$ Quintessence Model and the Swampland Obstruction to Stable Dark Energy**
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
All theorems are kernel-verified and the repository is free of `sorry` stubs. A small number of clearly-labelled results remain as explicit `axiom` declarations (the general-$n$ $S_{20}$ Picard–Fuchs recurrence, the CCGK Hodge data, and the Fano supercongruences); these are disclosed in `CAVEATS.md` and `OPEN_PROBLEMS.md`. The $S_{20}$ recurrence is additionally kernel-verified for $n\le 8$ and exact-checked for $n\in[0,60]$ (`scripts/verify_s20_recurrence.py`).
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
