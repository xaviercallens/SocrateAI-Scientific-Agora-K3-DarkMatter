# SocrateAI Lessons Learned & Linked Lemmas (LL.md)

This file compiles key insights, mathematical structures, Lean 4 kernel idiosyncrasies, and technical lessons discovered during the development of our neuro-symbolic framework.

## 1. Lean 4 Kernel & Compiler Insights
### The 'Noncomputable' Specifier for Real-Number Operations
- **Discovery:** In Lean 4, mathematical comparisons and operations on the real numbers `Real` (e.g. `if k3.volume > 0 then ...` or division `1.0 / k3.volume`) are mathematically nonconstructive. Because Lean's default definitions require computability, attempting to declare these standard real operations results in `failed to compile definition, consider marking it as 'noncomputable'`.
- **Resolution:** All physical mappings, loss functions, and density metrics that use real analysis or division must be marked as `noncomputable def` (e.g., `dark_energy_density`, `dark_sector_loss` in `K3GitnBlueprint.lean`).
- **Guidance:** Do not use compute-forcing structures for nonconstructive real geometry; embrace `noncomputable` early to maintain strict type safety without compiler blockages.

### Pre-compiling Mathlib via Cache
- **Discovery:** Compiling high-dimensional algebra and analytical tactics (like `field_simp` and `ring`) inside Mathlib 4 from source is highly resource-intensive and will exceed time or memory limits on standard virtual environments.
- **Resolution:** Always execute `/home/callensxavier_gmail_com/.elan/bin/lake exe cache get` as a precursor to any major compilation run. This retrieves pre-compiled Mathlib binaries, resolving dependency deadlocks and speeding up builds.

### Typeclass Synthesis Limits on Massive Polynomials
- **Discovery:** The Lean 4 typeclass synthesizer can reach maximum recursion depth limits (e.g., `error: failed to synthesize HPow ℚ`) when compiling extremely large rational polynomials (such as creative-telescoping WZ certificates `cert_poly` in `S20RecurrenceProof.lean`).
- **Guidance:** To prevent recursive depth failure, split massive polynomials into smaller sub-polynomials or scale coefficients to avoid fraction-clearing overhead during tactic execution.

## 2. Statistical Learning Theory Reference
- **Repository Reference:** `YuanheZ/lean-stat-learning-theory` (ICML 2026) located locally at `/home/callensxavier_gmail_com/lean-stat-learning-theory`.
- **Key Formalized Tools:**
  - `CoveringNumber.lean`: Computes metric entropy and covering bounds.
  - `Dudley.lean`: Dudley's entropy integral theorem for sub-Gaussian processes.
  - `GaussianLipConcen.lean`: Lipschitz concentration under Gaussian measures.
  - `MetricEntropy.lean`: Metric entropy bounding for generic metric spaces.
- **Integration Mapping:** In our K3-GITN blueprint, the neural hypothesis class `NeuralHypothesisClass` has its generalization bound structured symmetrically to the master error bounds formalized in the SLT library. This provides a direct path to completely eliminating `sorry` stubs in future phases by linking our K3-GITN map to their formalized Rademacher complexities.

## 3. GPU Acceleration & On-Device Operations
- **PSD Density Matrices:** To enforce a valid quantum state on-GPU, the network must output a square matrix $A$, and then compute $\rho = A A^T / \text{Tr}(A A^T)$. Directly predicting the 16 elements of a density matrix without this structure will violate positive semi-definiteness or trace conservation.
- **Stable Entanglement Entropy:** When computing the eigenvalues of $\rho$ via `torch.linalg.eigh`, some eigenvalues can become extremely small or negative due to float32 numerical precision. To prevent $\text{NaN}$ outputs, eigenvalues must be clamped using `torch.clamp(eigenvalues, min=1e-9)` before calculating $\log_2(\lambda)$.
