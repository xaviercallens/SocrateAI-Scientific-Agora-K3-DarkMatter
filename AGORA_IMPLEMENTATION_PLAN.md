# 💻 Agora Code Guidelines & Implementation Plan

This document outlines the strict software engineering practices, architectural patterns, and step-by-step implementation plan required to encode the **Topological Phase Cosmology** theory into the SocrateAI Scientific Agora codebase.

Our objective is to computationally prove that the $S_{1,2}$ and $S_{2,1}$ K3 asymmetry is the fundamental mechanism for **Spontaneous Geometric Symmetry Breaking**, bridging String Phenomenology, the Swampland Distance Conjecture (SDC), and the Trace Anomaly using verifiable Lean 4 proofs and massive LSS (Large Scale Structure) data analysis.

---

## Part 1: Code Architecture & Engineering Standards

Because this codebase spans formal mathematics (Lean 4), high-performance tensor computing (PyTorch/JAX), and Big Data astrophysics, strict architectural discipline—derived from our historical logs (`LL.md`, `JOURNAL.md`)—is mandatory.

### 1.1 Language & Framework Segregation

* **Lean 4 (`/lean4_formal_proofs/`):** Strictly reserved for formal, kernel-verified mathematical proofs. No empirical approximations. All rational numbers must be exact (`ℚ`). Operations on real numbers must use the `noncomputable def` specifier.
* **Python/PyTorch (`/empirical_crucible/`):** Reserved for GPU-accelerated tensor networks, PAC generalization bounds, and deep learning mappings. Must run locally without simulation (Rule 1: "Zero Simulation Flottante").
* **Python/JAX & NumPyRo (`/cosmology_solvers/`):** Reserved for differentiable MCMC cosmological inference against observational datasets.
* **Python/CuPy & Dask (`/lss_tensor_analytics/`):** Reserved for Out-Of-Core, GPU-accelerated Big Data processing of SDSS DR17/DESI catalogs to compute the macroscopic $\Delta$ topological asymmetry.

### 1.2 The "Axiomatic Firewall" (Lean 4)

* **Zero `sorry` tolerance in core proofs.** All logic must compile flawlessly under `lake build`.
* **Explicit `axiom` Declarations:** Any unproven physical input (e.g., the specific top-down Type IIB orientifold data from collaborators, or integer flux quanta) must be encapsulated in a clearly labeled `axiom` and logged in `OPEN_PROBLEMS.md`.
* **Mathematical Traceability:** If Lean 4 code proves that $\lambda > \sqrt{2}$, the docstring must explicitly cite the "Quintessence-Swampland Tension".

### 1.3 Big Data Safeguards (LSS Analytics)

* **No OOM (Out of Memory) Crashes:** Processing millions of galaxies via 3D FFTs will crash 16GB GPUs. You must use **Voxel Chunking** (e.g., $10^\circ \times 10^\circ \times \Delta z$ sectors) and explicitly clear cache (`torch.cuda.empty_cache()`).
* **No FFT Ringing:** You must implement exact survey masks or **3D Hamming/Hanning Window Functions** to smoothly taper the edges of galaxy catalogs to zero before applying the topological tensor transform to prevent Gibbs phenomenon artifacts.

---

## Part 2: Step-by-Step Implementation Roadmap

This is the concrete roadmap to encode the Global Theory into code.

### Pillar I: Formalizing the Global Theory (Lean 4)

**Goal:** Machine-certify the Swampland Distance Conjecture, the Trace Anomaly, and position the $S_{1,2}$ vs $S_{2,1}$ mass gap as Spontaneous Geometric Symmetry Breaking.

1. **Formalize Spontaneous Geometric Symmetry Breaking:**
   * *Path:* `lean4_formal_proofs/Agora/Phenomenology/SymmetryBreaking.lean`
   * *Action:* Define the Picard-Fuchs operators for $S_{1,2}$ and $S_{2,1}$ over $\mathbb{Q}$. Define the asymmetry parameter $\Delta = |S_{1,2} - S_{2,1}|$. Prove the theorem that if the local baryonic density breaks the topological mirror symmetry, then $\Delta > 0$, implying a mass ratio strictly greater than 1 (using the verified ratio 1014/336).

2. **Formalize the LVS Hessian Stability & SDC Bounds:**
   * *Path:* `lean4_formal_proofs/Agora/Swampland/LVS_Stability.lean`
   * *Action:* Define the F-term scalar potential $V_F$ using `Mathlib.Analysis.Calculus.Deriv`. Compute the mixed partial derivatives $\partial_i \partial_j V$. Prove Sylvester's criterion ($\det \mathbf{H} > 0$) to formally guarantee the vacuum is tachyon-free. Define the tower mass scale $M(\Delta S) = M_0 e^{-\alpha \Delta S}$ to verify Swampland bounds.

3. **Formalize the Atiyah-Singer Trace Anomaly:**
   * *Path:* `lean4_formal_proofs/Agora/Topology/AtiyahSinger.lean`
   * *Action:* Define the K3 Hirzebruch signature $\tau = b_2^+ - b_2^- = -16$. State the index theorem mapping this to the chiral fermion asymmetry $n_+ - n_- = -16$. Create an audited `axiom` linking this non-zero chiral trace to the macroscopic expectation value of the stress-energy trace $\langle \tensor{T}{^\mu_\mu} \rangle \neq 0$ (Dark Energy).

4. **Compile the WZ Certificate (Phase 4 Roadmap):**
   * *Path:* `lean4_formal_proofs/Structures/S20Recurrence.lean`
   * *Action:* Ingest the SymPy-verified Wilf-Zeilberger certificate. Use `field_simp; ring` to prove the telescoping sum over $\mathbb{Q}$, discharging the general-$n$ axiom for the minimal Picard-Fuchs recurrence. Set `set_option maxHeartbeats 0` locally to avoid timeout limits during the massive polynomial expansion.

### Pillar II: LSS GPU Pipeline (The Macroscopic $\Delta$ Proof)

**Goal:** Prove that Spontaneous Geometric Symmetry Breaking ($\Delta \neq 0$) aligns precisely with Dark Matter clustering, using the full SDSS DR17 and DESI catalogs.

1. **Build the Voxel-Chunking Tensor Grid:**
   * *Path:* `lss_tensor_analytics/k3_tensor_grid.py`
   * *Action:* Use `astropy` to convert RA, Dec, and Redshift into comoving Cartesian coordinates. Implement a Dask/CuPy pipeline to segment the universe into discrete $100 \text{ Mpc}^3$ voxel chunks to fit VRAM limits.

2. **Implement the Baryon-Coupled Transform:**
   * *Path:* `lss_tensor_analytics/topological_fft.py`
   * *Action:* Use `torch.bincount` to accumulate exact galaxy masses/luminosities into the grid (do not use unweighted $1/0$ logic gates). Apply a 3D Hanning window. Run the 3D FFT to project the space onto the $S_{1,2}$ and $S_{2,1}$ kernels. Calculate $\Delta = |S_{1,2} - S_{2,1}|$ and extract the top 1% gravitational nodes.

3. **The Null Hypothesis Falsification Run:**
   * *Path:* `lss_tensor_analytics/null_hypothesis_test.py`
   * *Action:* Create a mock catalog by randomly shuffling the 3D coordinates of the real SDSS galaxies (creating a uniform Poisson distribution). Run the FFT pipeline. *Success criteria:* The pipeline must return $\Delta \approx \text{background noise}$ everywhere, mathematically proving the algorithm is detecting real physical gravity, not hallucinating artifacts.

4. **Cross-Correlation Verification:**
   * *Path:* `lss_tensor_analytics/lss_statistical_validation.py`
   * *Action:* Compute the 3D 2-point cross-correlation function $\xi_{\Delta, \text{cluster}}(r)$ between the highest $\Delta$ nodes and known baryonic superclusters from external catalogs (e.g., redMaPPer). Generate empirical correlation plots to prove clustering alignment.

### Pillar III: PTA Monopole Isolation (Bayesian Inference)

**Goal:** Prove the scalar nature of the FDM axion using Pulsar Timing Arrays.

1. **Define the Scalar Monopole Kernel:**
   * *Path:* `cosmology_solvers/pta_enterprise/scalar_kernel.py`
   * *Action:* Implement the rigorous General Relativity Overlap Reduction Function (ORF) for a scalar breathing mode: $\Gamma_{\text{Scalar}}(\theta) = 1.0$.

2. **Bayesian MCMC Inference:**
   * *Path:* `cosmology_solvers/pta_enterprise/bayes_factor.py`
   * *Action:* Using the `enterprise` suite, build a model combining Hellings-Downs GWB and the `FourierBasisGP` Scalar Monopole. Run a Parallel Tempering MCMC on mock/public NANOGrav data. Calculate the Savage-Dickey density ratio to extract the Bayes Factor ($\mathcal{B}$) comparing the models.

---

## Part 3: CI/CD Release Gates & Community Workflow

To effectively crowd-source the remaining string phenomenology parameters while maintaining the "Honesty Protocol", all Pull Requests (PRs) must pass these strict gates:

1. **Gate A (Lean Kernel Check):** Executing `lake build Agora` must return exactly `0 errors`. Massive polynomials (like Phase 4 WZ compilation) must be chunked properly to avoid breaking CI pipelines.
2. **Gate B (Hardware Validation):** The GPU LSS suite must run successfully on local CUDA hardware. Output logs (`.json` configurations containing the random seed, GPU specs, and grid resolution) must be committed alongside the code to prove hardware execution.
3. **The Three-Tier Vocabulary Tagging:** Every PR description modifying empirical physics must explicitly tag its outputs as **`[VERIFIED]`** (Lean 4 exact math), **`[FITTED]`** (calibrated to data), or **`[PREDICTED]`** (falsifiable consequence).
4. **"Bounty" Issues for String Theorists:** Open GitHub issues tagged `[HELP WANTED: String Pheno]` for the remaining Top-Down items (e.g., specific Type IIB orientifold D-brane content and Euclidean instanton actions). Provide clear JSON templates in `/data/theory_inputs/` so external string theorists can submit topological data without needing to write Lean 4 code.
