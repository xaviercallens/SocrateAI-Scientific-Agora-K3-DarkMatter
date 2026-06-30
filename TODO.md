# SocrateAI Task List (TODO.md)

This file contains the near-term task list for implementing the K3-GITN Neuro-Symbolic integration blueprint and maintaining strict scientific rigor.

## Near-Term Tasks

### 1. Lean 4 Formalization
- [x] Apply the `noncomputable` specifier to `dark_energy_density` and `dark_sector_loss` in `lean4_formal_proofs/Structures/K3GitnBlueprint.lean`.
- [x] Run compilation checks under the Lean 4 kernel to verify that `K3GitnBlueprint.lean` compiles with 0 errors and 0 warnings (except the expected linter warning for the terminal `sorry` stub).
- [x] Apply compilation options (`maxHeartbeats 0`) and generate a bivariate polynomial chunk decomposition (`Structures/S20Decomposition.lean`) to successfully resolve typeclass synthesis limits and ring timeouts in `Structures/S20RecurrenceProof.lean`.
- [ ] Connect `K3_to_GITN_Map` hypothesis class with concrete Covering Number bounds inside `lean-stat-learning-theory`.

### 2. Empirical Validation Suite
- [x] Create the GPU dry-run validation script `empirical_crucible/verify_k3_gitn.py`.
- [x] Train the K3-to-GITN mapping MLP on the local Tesla T4 GPU using Adam.
- [x] Implement on-device von Neumann entropy calculation using stable eigen-decompositions.
- [x] Estimate the empirical Rademacher complexity of the neural network class over the moduli sample space.
- [x] Calculate and output the PAC expected loss bounds under 95% confidence interval ($\delta = 0.05$).
- [x] Save all verified metrics to `empirical_crucible/k3_gitn_results.json` and logs to `empirical_crucible/k3_gitn_dry_run.log`.

### 3. Project Documentation & Management
- [x] Create and populate the long-term memory document `MEMORY.md`.
- [x] Create and populate the lessons learned registry `LL.md`.
- [x] Create and populate the development milestones journal `JOURNAL.md`.
- [x] Define a multi-phase integration roadmap in `ROADMAP.md`.
- [x] Synchronize numerical constants ($w_0, w_a, H_0$) across all code, benchmark JSONs, and manuscript text prior to the next major release (Rule 8).
