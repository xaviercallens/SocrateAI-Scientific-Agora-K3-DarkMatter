# SocrateAI Task List (TODO.md)

This file contains the near-term task list for implementing the K3-GITN Neuro-Symbolic integration blueprint and maintaining strict scientific rigor.

## 0. AutoEvolve R2 — The Hypothesis Foundry (Phase 8) — PROPOSED

**Status:** PLANNING (not yet implemented; ready for low-cost LLM execution per AUTORESEARCH_RELEASE_V2_PLAN.md)

A gate-driven evolutionary hypothesis search. Reuses validation infrastructure as fitness function. AlphaEvolve-style: cheap generator + ruthless evaluator. Answer-key classifier controls: Apéry ζ(2) (A005258, elliptic, 40-year literature) and Apéry ζ(3) (A005259, Beukers–Peters K3).

**Executor budget:** ~85% HAIKU tier, 3 HUMAN gates, <50 CPU-h, ~1,100 LLM calls, 12 weeks.

### Phase 8.A — Literature Review (weeks 1–2): 13 candidates
- [ ] `[HAIKU]` **LR-1** Cross-match $S_{1,2}$/$S_{2,1}$ OEIS + Zagier/Cooper/AESZ → confirm $S_{2,1}$ ≡ A005258 (elliptic)
- [ ] `[HAIKU]` **LR-2** Enumerate classified sporadics (Zagier 6×order-2, Cooper order-3 pool, Domb, Almkvist–Zagier, Verrill) → ≥15 with geometry assignments
- [ ] `[HAIKU]` **LR-3** Extended sieve: $(A,B)\in[1,8]^2$ + 3-factor $S_{A,B,C}$ with held-out validation (≥70 terms, n≤110)
- [ ] `[HAIKU]` **LR-4** Archive Lee & Tsai 2026 PRD + El Naschie 2013 in `docs/reference/` with epistemic classification (El Naschie = numerology-class, boundary-marker only)
- [ ] `[SONNET+]` **LR-5** Lee–Tsai bridge memo: $(R, m_B)$ resonance → $m_{\mathrm{eff}}(\Delta)$ mapping + "where the analogy breaks" section ≥alignment section
- [ ] `[HAIKU+HUMAN]` **LR-6** Freeze pool at 13 candidates (include Apéry ζ(3) positive control + one Zagier negative control); HUMAN approves ranking

### Phase 8.B — G1/G2 Exact-Arithmetic + Physics Gates (weeks 3–4): 13 → 5
- [ ] `[HAIKU batch]` **G1-1** Classify order per candidate (corrected classifier on 13); **control fail → halt**
- [ ] `[HAIKU batch]` **G1-2** Weil bounds (44 primes) + weight-2/3 status (recorded, not eliminatory)
- [ ] `[HAIKU batch]` **G1-3** Mirror-map integrality (30 coefficients per candidate)
- [ ] `[HAIKU batch]` **G1-4** Fuchs criterion + monodromy attempt; computable monodromy → auto-elevate
- [ ] `[HAIKU batch]` **G2-1** Stiffness contours $(\tau,\mathcal{V})$ per candidate (never point masses)
- [ ] `[HAIKU batch]` **G2-2** GD-1 No-Go check (pinned to $10^{-23}$ eV → eliminate)
- [ ] `[HAIKU batch]` **G2-3** Dolan superradiance solver (achievable windows, bare-survival asymmetry)
- [ ] `[HUMAN]` **GATE-B-SELECT** Score composite (G1/G2 completeness + monodromy + No-Go + superradiance + control sanity) → pick top 5

### Phase 8.C — Quick Data Tests (weeks 5–7): 5 → 3
- [ ] `[HAIKU]` **EU-1** Euclid Q1 acquisition (ESA archive); if blocked → BLOCKED note (Rule 1)
- [ ] `[HAIKU]` **JW-1** JWST UNCOVER acquisition ($z≥8.5$, same $\tilde\rho$ formula as WS9)
- [ ] `[HAIKU]` **QT-1** KK projection per 5 candidates on SDSS DR17 + Euclid Q1 (KS test vs. $S_{1,2}$); indistinguishable at $p>0.9$ → demoted
- [ ] `[HAIKU]` **QT-2** Replace WS11 synthetic $\Delta_{\rm early}$ with JW-1 empirical; re-run see-saw t-test
- [ ] `[HAIKU]` **QT-3** PTA window occupancy per candidate (NANOGrav 15-yr sensitivity); flag PTA-reachable ratio bands
- [ ] `[SONNET+]` **QT-4** Lee–Tsai overlap (self-interaction SIDM band); structural analogy ≠ Lagrangian prediction disclaimer
- [ ] `[HAIKU batch]` **QT-5** Null-hypothesis battery (Poisson mocks); stats failing separation → barred
- [ ] `[HUMAN]` **GATE-C-SELECT** Observational leverage ranking: (# tests distinguishable) × (falsifiability); pick top 3

### Phase 8.D — Top-3 Implementation + Lean (weeks 8–12)
- [ ] `[HAIKU chunks]` **D-1** Lean kernel verification for 3 finalists (n≤20 decidable recurrence; zero `sorry`)
- [ ] `[HAIKU]` **D-2** Ledger + CI integration for finalists; `cross_consistency_check.sh` extended
- [ ] `[SONNET+]` **D-3** Part VII manuscript: Hypothesis Foundry (3 sections, one per finalist, negative-results-first, provenance ledger pattern)
- [ ] `[HUMAN]` **D-4** External verification invitations (GitHub issues to arithmetic-geometry/PTA communities; reproduction scripts)
- [ ] `[SONNET+]` **D-5** Observatory targeting dossier (PTA ratio-test bands, lensing cross-match targets)

### Phase 8.E — DarkMatterK3-Home Integration
- [ ] `[HAIKU]` **DM-1** Job spec schema (survey_tile, statistic_hash, candidate_id, seed, client_version)
- [ ] `[HAIKU]` **DM-2** Quorum replication protocol (≥2 independent clients per tile; disagreement → quarantine)
- [ ] `[HAIKU]` **DM-3** Re-run v1 headline numbers (1.177, Δ=47.0) under quorum; archive before re-citation
- [ ] `[HAIKU]` **DM-4** Dispatch Phase C TDA jobs to volunteer network; quorum replication active

### Phase 8.F — Anti-Circularity Enforcement (standing gate all phases)
- [ ] Parameter fit-to-target declared in `PARAMETER_LEDGER.yaml` per task; CI check for circularity → task void
- [ ] Audit log: `data/autoresearch_v2/anti_circularity_audit.json`

---

## 0. Scientific Validation Program (v2.0.0) — COMPLETE

Full referee review and task specs: **[`scientificplan.md`](scientificplan.md)**. Roadmap/milestones: **[`ROADMAP.md`](ROADMAP.md) §2 Phase 6**. Every task below is tagged by executor tier — `[HAIKU]` tasks are fully specified and mechanical; `[SONNET+]` tasks need multi-step derivation; `[HUMAN]` tasks need domain judgement or an external collaborator. Task IDs (T1.1, T2.3, ...) cross-reference the full spec in `scientificplan.md` §B.

### 0.1 Do first — cheap, protects everything downstream
- [x] `[HAIKU]` **T8.1** Implement `scripts/cross_consistency_check.sh` for real; create `PARAMETER_LEDGER.yaml` at repo root with λ, w₀, wₐ, H₀, ε, both axion masses, both stiffness integers, both α_eff, both PTA periods, each with source-line references.
- [x] `[HAIKU]` **T8.2** Add CI workflow: `lake build Agora`, `pytest tests/`, `cross_consistency_check.sh`, grep for zero `sorry` in `lean4_formal_proofs/`. Block merge on failure.
- [x] `[HAIKU]` **T4.2** Kernel-verify $S_{1,2}$/$S_{2,1}$ order-3 recurrences for $n\le20$ via `decide` (new `Structures/S12S21Recurrence.lean`, mirroring `S20Recurrence.lean`).

### 0.2 WS1 — K3 Identification (GAP-1, critical)
- [x] `[HAIKU]` **T1.1** Compute monodromy/connection matrices for $S_{1,2}$, $S_{2,1}$ (`mpmath`, 50-digit precision); verify product-of-monodromies ≈ identity; check MUM structure at $z=0$. Output `data/monodromy/S12_monodromy.json`, `S21_monodromy.json`.
- [x] `[HAIKU]` **T1.2** Weil-bound + modularity screen: compute $a_p$ for $p<200$, check $|a_p|\le2p$, compare against known weight-3 rational newforms (LMFDB). Output `data/modularity/*_ap_table.csv` + `modularity_report.md`. State match/no-match without hedging.
- [x] `[HAIKU]` **T1.3** Mirror-map integrality check: 30 exact-ℚ coefficients per sequence; report integrality verdict plainly, including if it fails.
- [x] `[HAIKU]` **T1.4** Propagate WS1 outcomes into `CAVEATS.md §2`, `OPEN_PROBLEMS.md`, `Part I §2/§Limitations` (Rule 6 — grep-verified in all three).

### 0.3 WS2 — Stiffness Derivation (GAP-2, critical)
- [x] `[HAIKU]` **T2.1** Document the $V''(0)=1014/336$ pipeline end-to-end in `docs/derivations/stiffness_pipeline.md`; add regression test `tests/test_stiffness_values.py`.
- [x] `[SONNET+]` **T2.2** Write `docs/derivations/stiffness_to_potential.md`: derive (or honestly fail to derive) PF-recurrence → potential-curvature; every non-derivable step becomes a named Lean-axiom candidate.
- [x] `[HAIKU]` **T2.3** Kernel-verify `pta_frequency_ratio_in_interval` (parameter-free ratio test, reuses `mass_ratio_in_interval`); add the "ratio test" falsification paragraph to Part I §Observational Predictions and `PREDICTIONS.md` (Prediction 4b).

### 0.4 WS3 — Superradiance & Screening (GAP-3/4, serious)
- [x] `[SONNET+]` **T3.1** Implement Dolan (2007) continued-fraction growth rates; validate against published reference points (≤5% error); evaluate at bare α = 0.155 (S₁,₂) / 0.089 (S₂,₁), modes $l=m=1,2$.
- [x] `[x]` **T3.2** (after T3.1) S₂,₁-bare survival table across M87* + 5 highest-spin SMBHs; propagate conclusion to Part I §Limitations.
- [x] `[HUMAN]` + `[SONNET+ draft]` **T3.3** Screening-alternatives memo (chameleon $n>0$, symmetron, native $T^2$-coupling density-dependence); human sign-off required before manuscript change.

### 0.5 WS4 — Formal Verification Closure (GAP-6, mechanical; non-blocking as of 2026-07-12 — see VALIDATION_GUIDE.md)
- [ ] `[SONNET+]` (chunked `[HAIKU]`) **T4.1** Compile WZ certificate into Lean; discharge `axiom s20_recurrence`; update all 5 disclosure locations (OPEN_PROBLEMS.md, CAVEATS.md §6, README.md, both manuscript §2/AI-Methodology blocks). **Confirmed non-blocking for the physics paper:** `cy_axion_no_go` (the GD-1 No-Go theorem, S20's only load-bearing role here) is self-contained and does not depend on this axiom. Still genuinely open as a formal-verification goal in its own right — `scripts/gen_wz_lean.py`/`verify_wz_certificate.py` referenced elsewhere do not exist yet; a same-day attempt in the companion Mirror-Map-Sieve repo to discharge this via "Horner reduction" produced a vacuous `True` theorem, not a real proof (corrected there 2026-07-12).

### 0.6 WS5 — Cosmology to Boltzmann Grade (GAP-5, moderate)
- [x] `[HAIKU]` **T5.1** Replace rest ICs with tracker/scaling ICs (Copeland–Liddle–Wands 1998); re-run λ sweep; write `docs/cosmology/ic_sensitivity.md`; trigger `cross-consistency-gate` if (w₀,wₐ) moves >0.01.
- [x] `[SONNET+]` **T5.2** CLASS-fork ingestion of mass-varying axion fluid; recompute H₀ shift with full perturbations against Planck 2018 plik-lite.
- [x] `[HAIKU]` data prep + `[SONNET+]` **T5.3** Joint $\epsilon$ likelihood (JWST × S₈): execute the see-saw falsification test from `VISION.md §4A`; report plainly if posteriors are mutually exclusive at >3σ.
- [ ] `[HAIKU]` **T5.4** DESI DR2 refit when public; full `cross-consistency-gate` checklist in the same commit.

### 0.7 WS6 — PTA Endgame Preparation
- [ ] `[SONNET+]` **T6.1** Injection-recovery forecast for both PTA lines (`enterprise`/`enterprise_extensions`, NANOGrav 15-yr-like synthetic residuals, clearly labeled forecast).
- [x] `[HAIKU]` **T6.2** Write `docs/pta/galactic_frame_test.md`: explicit phase-residual formula + likelihood-ratio test, precise enough for an external PTA collaborator to implement unassisted.

### 0.8 WS7 — Compactification Scaffold (Goal II)
- [x] `[HAIKU]` **T7.1** Insert manuscript §1.5 "Compactification data" per `VISION.md` Goal II template; add Becker–Becker/Vafa–Witten bib entries; add schematic-input Lean axiom via the four-ledger `axiom-gap-disclosure` routine.
- [ ] `[HUMAN]` **T7.2** Tadpole feasibility check for a concrete orientifold matching $S_{1,2}$/$S_{2,1}$ Hodge data — requires a string-phenomenology collaborator (see `OPEN_PROBLEMS.md` items 1–2, templates in `data/theory_inputs/`).

### 0.9 Phase 7 — Part VI (The Resonance Observatory)
- [x] `[HAIKU]` **T9.1** Reprocess SDSS DR17 spectroscopic catalog through the density-dependent mass ansatz to export the macroscopic Kaluza-Klein resonance map (`ws9_observational_telescope.py`).
- [x] `[HAIKU]` **T10.1** Compute Chameleon-type geometric pinching at M87* to validate superradiance evasion bounds (`ws10_m87_chameleon_validation.py`).
- [x] `[HAIKU]` **T11.1** Perform Welch's t-test on synthetic local/early-universe mass distributions to establish the Cosmic See-Saw p-value (`ws11_cosmic_seesaw_verification.py`).
- [x] `[HAIKU]` **T12.1** Consolidate all sensitivity analyses and attributions into the Part VI LaTeX manuscript and compile the preprint PDF.

### 0.10 Phase 7 — Part VII (Supercluster Anomaly & DarkMatter@Home)
- [x] `[HAIKU]` **T13.1** Ingest DarkMatter@Home pilot run results (327,918 galaxies, asymmetry 69.7, warp parameter 1.45) and the 22-node cosmic web junction at K3-DISC-0003, write the Part VII LaTeX manuscript, and compile to PDF.

---

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

### 4. Operation Lambda-Falsification
- [x] Ingest DESI DR1 BAO data and compute $\Delta \chi^2$ for the $T^2$ rolling Torus versus flat $\Lambda$CDM.
- [x] Ingest Pantheon+ Supernova dataset and overlay theoretical $T^2$ distance modulus $\mu_{\text{th}}(z)$ on the high-redshift scatter plot.
- [x] Calculate the Late-Time ISW temperature depression ($\Delta T$) for the $T^2$ trajectory to cross-reference with the CMB Cold Spot.
- [x] Compute the Sandage-Loeb real-time redshift drift ($\Delta z / \Delta t$) for $z=2$ to $z=5$.
- [x] Generate `Agora_Lambda_Falsification.ipynb` with final plots, BIC evaluation, and formal penalization calculations.
