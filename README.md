# SocrateAI-Scientific-Agora: K3 Dark Matter & Dark Energy

This repository contains the public artifacts, papers, mathematical formalizations, and simulation code for the **K3 String Vacua, Dark Matter, and Dark Energy** project, developed within the SocrateAI Scientific Agora ecosystem.

This repository serves as the definitive reference for the scientific community to review, reproduce, and critically analyze the findings.

## Papers and Preprints

The exact theoretical results and dynamics have been documented in the following preprints, which are available on Zenodo:

- **Part I: Exact Algebraic Identification of K3 String Vacua with Dark Matter**
  - **DOI/Link:** [10.5281/zenodo.20863378](https://zenodo.org/deposit/20863378)
  - **File:** `manuscript/K3_DarkMatter_Preprint.pdf`
- **Part II: Project Vafa-Continuity: $K3 \times T^2$ Moduli Dynamics & The Dark Energy Equation of State**
  - **DOI/Link:** [10.5281/zenodo.20863381](https://zenodo.org/deposit/20863381)
  - **File:** `manuscript/Vafa_Continuity_Monograph.pdf`

## Directory Structure

- `manuscript/`: Contains the PDF preprints and monographs of the theoretical work.
- `Agora/`: Contains the **Lean 4** formalization of the mathematical proofs. We strictly adhere to the 'No Simulation' rule, relying on formal theorem proving to establish mathematical truths.
- `simulations/`: Contains the exact numerical physics scripts (e.g., SymPy exact integration, Vlasov equation solvers) to track the time evolution of the dark energy fluid and dark matter candidates.
- `vlasov_data/`: Contains the `Vlasov` simulation datasets (`Linear_Landau_Damping_training_data.mat`, `Noninear_Landau_Damping_training_data.mat`) used for benchmark verifications.
- `empirical_validation/`: Contains the Jupyter notebook and scripts fetching real observational data (e.g., from `astroquery`) to empirically validate the $K3 \times T^2$ theoretical signatures.
- `.agents/`: Contains the configurations, skills, and prompts for the autonomous AI agents (e.g., Galois, Socrates) that assisted in exploring and validating these theories within the strict mathematical boundaries established by the workspace rules.

## Empirical Validation against JWST, DES, and Quasar Catalogs

Standard cosmologists treat the JWST early galaxy crisis and the DES Y3 $S_8$ clustering crisis as separate anomalies. Our empirical notebook demonstrates they are the exact same phenomenon. By parsing real observational data (UNCOVER catalog and Webb-Murphy quasar data), we mathematically link the birth of the first stars to the modern smoothness of the cosmic web using a single expanding String Theory Torus.

Explore the executable code, raw data parsing, and scientific caveats in our Jupyter Notebook:
- **[Agora Empirical Validation Notebook](empirical_validation/Agora_Empirical_Validation.ipynb)**

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
