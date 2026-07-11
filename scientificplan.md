# scientificplan.md — Referee Review & Executable Validation Plan
## For the conjectured 4D K3 (S₁,₂ / S₂,₁) × T² dark-sector theory (w₀, wₐ quintessence)

**Document type:** Scientific referee review + machine-executable implementation plan
**Review persona:** Senior string phenomenologist / Swampland-programme referee
**Executor profile:** Tasks are scoped so a lightweight LLM (Haiku-class) can execute them mechanically. Each task has explicit inputs, steps, acceptance criteria, and a verification command. Tasks that genuinely require heavier reasoning or a human expert are flagged `[TIER: SONNET+]` or `[TIER: HUMAN]`. Everything else is `[TIER: HAIKU]`.
**Governing rules:** All tasks are executed under `AGENTS.md` Rules 1–8 and the skills in `.agents/skills/` (especially `strict-math-verification`, `axiom-gap-disclosure`, `empirical-data-validation`, `cross-consistency-gate`).
**Last updated:** 2026-07-11

---

# PART A — REFEREE REVIEW (the scientific assessment)

## A.0 Summary verdict

The work is an honest, well-disclosed *string-inspired phenomenology* with one genuinely novel methodological contribution (exact-rational algebraic sieving + targeted kernel verification) and one clean physics result (quantitative instantiation of the Agrawal–Obied–Steinhardt–Vafa quintessence-Swampland tension in a concrete K3×T² setting). It is **not yet** a validated theory. The distance between "interesting phenomenology" and "candidate physics" is spanned by exactly **six load-bearing gaps**, ranked below by how much of the edifice rests on each.

## A.1 Ranked load-bearing gaps

### GAP-1 (critical): The K3 identification of S₁,₂ / S₂,₁ is conjectural
The entire "K3" label rests on: order-3 Picard–Fuchs operator ⇒ K3 Hodge structure, via the Stienstra–Beukers correspondence. This is a *necessary-condition* argument. Without (a) the monodromy/connection matrices, (b) modularity of the associated Fourier coefficients (weight-3 form for a rigid K3 family), and (c) integrality checks on the mirror map, the objects S₁,₂ and S₂,₁ are — from a referee's standpoint — *binomial sums with order-3 recurrences*, not surfaces. If GAP-1 fails, every downstream physics claim loses its geometric anchor. **This is the highest-value validation target and much of it is mechanically computable.**

### GAP-2 (critical): "Topological stiffness" V″(0) lacks a published derivation
The numbers 1014 and 336 drive the mass ratio √(1014/336) ≈ 1.74 — the *only* dimensionless prediction of Part I. But the manuscripts assert rather than derive the map:
`PF recurrence coefficients → axion potential curvature V″(0)`.
A referee will ask: which potential V? At which point in moduli space? In what normalization? The chain "instanton sum → potential → second derivative at the origin → these specific integers" must be written down step by step, or the ratio 1.74 is numerology attached to a true algebraic fact. **This is a derivation-writing task, partially mechanizable.**

### GAP-3 (serious): Superradiance analysis uses the Detweiler small-α formula outside its validity
CAVEATS.md §4 already admits this: Γ₂₁₁ ∝ α⁸ is a small-α approximation, applied at α_eff ≈ 0.89–1.55 where it is invalid. The correct treatment at α ≳ 0.4 is Dolan (2007) continued-fraction / Leaver-method solution of the Teukolsky equation. Additionally, only the m=1 mode is treated; m=2,3 modes are superradiant at larger α and are unaddressed. **Until this is fixed, the "M87* escape" claim is unsupported in the regime where it is invoked.** Note the honest fallback already identified in Part I §Limitations: S₂,₁ (bare α ≈ 0.089) may be natively borderline-safe *without* chameleon rescue — quantifying that is high value.

### GAP-4 (serious): The chameleon rescue is internally inconsistent as stated
γ ≈ 0.25 maps to Khoury–Weltman index n = −3 (unphysical). So the mechanism that rescues S₁,₂ from superradiance is not, as written, a consistent field theory. Three honest exits exist: (i) find a screening model whose exponent is physical (symmetron, dilaton-type, or environment-dependent f(ρ) derived from the T² coupling itself), (ii) demote S₁,₂ and promote S₂,₁ as the preferred vacuum (its bare α may survive without screening — see GAP-3), (iii) keep chameleon as explicitly phenomenological and accept the reduced claim. The manuscripts currently do (iii); the plan below makes (i) and (ii) computable.

### GAP-5 (moderate): Cosmology pipeline is pre-Boltzmann
The H₀ ~ 72 estimate uses background-only integration, rest initial conditions (not tracker), and a reverse-engineered ε = 0.042/λ. All three are disclosed. To be publishable as more than "indicative," the mass-varying axion fluid must go through a Boltzmann code (CLASS/axionCAMB fork), the initial conditions must be attractor-consistent, and ε must be fit jointly (JWST stellar-mass function × S₈ × CMB acoustic scale), not tuned to H₀.

### GAP-6 (moderate, mechanical): The general-n S₂₀ recurrence is an axiom
The WZ certificate is already SymPy-verified (diff = 0 exactly). Compiling it into Lean (`field_simp; ring` on the certificate identity + `Finset.sum_telescope`) upgrades the axiom to a theorem. This is the single cheapest credibility purchase available: it converts "computer-algebra-assisted" into "kernel-verified" for the 6D No-Go backbone. Note (correctly disclosed in Part I §2): S₂₀ is in the *excluded* symmetric family, so this does not gate the K3 results — but referees weigh hygiene.

## A.2 What is already solid (do not re-litigate)

- The exact-rational sieve and the S₁,₁ falsification (floating-point SVD bug) — genuinely good computational mathematics.
- `cy_axion_no_go`, mass-ratio interval (1.73, 1.75), `lambda_fit_exceeds_sqrt2`, `attractor_not_dark_energy` — kernel-verified, correctly scoped.
- The Swampland-tension reframing (Part II §7) — this is the right way to present a negative result and is the paper's strongest claim to relevance.
- The disclosure culture (CAVEATS.md, OPEN_PROBLEMS.md, explicit axioms) — above community standard.

## A.3 Referee's decision-tree for the theory

```
Is S₁,₂ (resp. S₂,₁) genuinely a K3 family?          ← GAP-1 (compute monodromy + modularity)
  ├─ NO  → reframe as "arithmetic sequences with FDM-compatible scalings"; physics survives as EFT-only
  └─ YES → Is V″(0)=1014/336 a derived potential curvature?   ← GAP-2 (write the derivation)
        ├─ NO  → ratio 1.74 is heuristic; keep as conjecture
        └─ YES → Does S₂,₁ survive superradiance *without* chameleon?   ← GAP-3 (Dolan rates)
              ├─ YES → S₂,₁ is the clean candidate; chameleon becomes optional for S₁,₂
              └─ NO  → chameleon must be made physical (GAP-4) or superradiance kills both
Independent track: does the ε that fits JWST also fit S₈?     ← GAP-5 (joint likelihood; falsifiable)
Independent track: PTA lines at 7.52 d / 13.08 d              ← observational endgame (ratio test!)
```

**Key falsification insight the manuscripts under-use:** if *both* PTA lines were ever detected, their frequency ratio must equal √(1014/336) ≈ 1.7386 (kernel-verified interval (1.73, 1.75)) *independently of τ and 𝒱*, because the free moduli cancel in the ratio. This is the single sharpest, parameter-free test the theory owns. Elevate it.

---

# PART B — IMPLEMENTATION PLAN (machine-executable)

## How to use this plan

- Tasks are atomic: one task = one commit (or one PR).
- Every task states: **Inputs → Steps → Acceptance → Verify command**.
- `[TIER: HAIKU]` = mechanical, fully specified; a light model executes it without design decisions.
- `[TIER: SONNET+]` = requires multi-step derivation or non-trivial debugging.
- `[TIER: HUMAN]` = requires domain judgement or external collaborator (per OPEN_PROBLEMS.md).
- On any ambiguity: **stop and report**, per Rule 4 (Adversarial Assessment). Never fill gaps with plausible-sounding output.
- After any task that changes a number: run the `cross-consistency-gate` skill checklist.

---

## WORKSTREAM 1 — K3 Identification (attacks GAP-1)

**Goal:** upgrade "computationally supported conjecture" to "verified necessary conditions + documented monodromy," or falsify the K3 label honestly.

### T1.1 — Compute connection/monodromy matrices for S₁,₂ and S₂,₁ `[TIER: HAIKU]`
- **Inputs:** `scripts/k3_monodromy_verification.py` (existing, extracts singular points); PF operators from `scripts/k3_sieve_analysis.py`.
- **Steps:**
  1. Extend the existing script: for each PF operator, find all singular points of the ODE (already done) and, for each pair of adjacent singular points, numerically integrate the ODE around a closed loop using `mpmath` with `mp.dps = 50` (analytic continuation along a polygonal path with ≥ 200 segments, radius 1/2 of distance to nearest other singularity).
  2. Record the 3×3 monodromy matrix at each singular point in exact-looking rational/algebraic form where entries round to integers or simple rationals within 10⁻³⁰; otherwise store the 50-digit floats.
  3. Compute: (a) eigenvalues of each local monodromy, (b) the product of all monodromies (must be identity to numerical precision — this is a *hard consistency check*), (c) whether the monodromy at the MUM point (z=0) is maximally unipotent (single Jordan block, eigenvalue 1).
  4. Write results to `data/monodromy/S12_monodromy.json` and `S21_monodromy.json` with the full precision settings, path definitions, and residuals logged (Rule 1: execution data or nothing).
- **Acceptance:** product-of-monodromies deviates from identity by < 10⁻³⁰ per entry; MUM structure confirmed or explicitly refuted; JSON files committed with input hashes.
- **Verify:** `python scripts/k3_monodromy_verification.py --check && jq '.product_identity_residual' data/monodromy/S12_monodromy.json`

### T1.2 — Weil-bound and modularity screen for the associated L-data `[TIER: HAIKU]`
- **Inputs:** integer sequences S₁,₂(n), S₂,₁(n) for n ≤ 200 (exact, from `sympy` — Rule 5: generated by executed code, never typed in).
- **Steps:**
  1. For each prime p in [5, 200], compute the candidate Frobenius trace aₚ via the standard Beukers–Stienstra recipe for the associated double covers (unit-root method: aₚ ≡ S(p−1)/2 mod p, following Stienstra–Beukers 1985 §"Congruences"; encode the exact congruence used in a comment with citation).
  2. Check the weight-3 Weil bound |aₚ| ≤ 2p^{(3−1)/2} = 2p for every p; log every pass/fail.
  3. Attempt matching against known weight-3 newforms with rational coefficients (finite list: CM forms of weight 3; levels from the LMFDB table of weight-3 rational newforms — hardcode the candidate list with LMFDB labels in the script header, cite each). Report best match and number of matching aₚ.
  4. Output `data/modularity/S12_ap_table.csv`, `S21_ap_table.csv` and a `modularity_report.md` stating: matched form (if any), number of primes checked, mismatches.
- **Acceptance:** ≥ 40 primes checked per sequence; every aₚ satisfies the Weil bound (else report as *falsification signal* prominently, per Rule 4); match/no-match stated without hedging.
- **Verify:** `python scripts/modularity_screen.py --primes 200 --report`
- **Note for executor:** a full modularity *proof* is out of scope (that is research mathematics). This task only produces the necessary-condition evidence table. Do not claim "modularity verified" — claim "consistent with / inconsistent with modularity at N primes."

### T1.3 — Mirror-map integrality check `[TIER: HAIKU]`
- **Inputs:** PF operators; standard mirror-map expansion q(z) = z·exp(y₁(z)/y₀(z)).
- **Steps:** compute the first 30 coefficients of the mirror map for S₁,₂ and S₂,₁ in exact ℚ via sympy series manipulation; test integrality (a hallmark of genuine K3/CY mirror maps) of the canonical coordinate coefficients after the standard rescaling; write `data/mirror_map/S12_qcoeffs.json` (exact rationals as strings).
- **Acceptance:** 30 exact coefficients each; integrality verdict stated per sequence; any non-integral coefficient reported as evidence *against* the K3 identification (do not rationalize it away).
- **Verify:** `python scripts/mirror_map_integrality.py && jq '.all_integral' data/mirror_map/S12_qcoeffs.json`

### T1.4 — Update manuscripts and caveats with WS1 outcomes `[TIER: HAIKU]`
- **Steps:** whatever T1.1–T1.3 produce, propagate verbatim into: `CAVEATS.md §2` (status upgrade or downgrade), Part I §2 and §Limitations, `OPEN_PROBLEMS.md`. Apply the `claim-classification-audit` skill: monodromy/Weil/integrality results are [VERIFIED-computational] (exact or high-precision execution), never [VERIFIED-kernel].
- **Acceptance:** Rule 6 (Atomic Caveat Propagation) — grep confirms the same status string appears in all three documents.
- **Verify:** `grep -l "monodromy" CAVEATS.md OPEN_PROBLEMS.md manuscripts_and_proofs/K3_DarkMatter_Preprint.tex | wc -l` → must be 3.

---

## WORKSTREAM 2 — The V″(0) derivation (attacks GAP-2)

### T2.1 — Reconstruct and document the stiffness pipeline `[TIER: HAIKU]`
- **Inputs:** `scripts/extract_axion_potential.py`, `scripts/k3_sieve_analysis.py`.
- **Steps:**
  1. Trace, in code, exactly how 1014 and 336 are computed from the recurrences (which coefficients, which normalization, which expansion point). Produce `docs/derivations/stiffness_pipeline.md` documenting every intermediate object with its formula and the script line that computes it.
  2. Add a regression test `tests/test_stiffness_values.py` that recomputes both integers from scratch (exact arithmetic) and asserts equality.
- **Acceptance:** a reader can follow the chain `recurrence → [named intermediate objects] → V″(0)` with zero unexplained steps; test passes.
- **Verify:** `python -m pytest tests/test_stiffness_values.py -v`

### T2.2 — Write the physics derivation memo: PF data → potential curvature `[TIER: SONNET+]`
- **Steps:** write `docs/derivations/stiffness_to_potential.md` deriving (or honestly failing to derive) the identification of the recurrence-extracted quantity with the curvature of the axion potential from the instanton sum m_a² ~ Σ d² q_d e^{−2πdτ}. Every non-derivable step becomes an explicit named assumption (feeding the `axiom-gap-disclosure` skill: Lean `axiom` + CAVEATS entry + manuscript caveat).
- **Acceptance:** the memo ends with a boxed list: "Derived: […] / Assumed: […]"; each assumption has a Lean axiom stub name assigned.
- **Escalation:** if the derivation cannot be completed, this becomes OPEN_PROBLEMS.md item and the manuscripts' language downgrades from "topological stiffness" to "recurrence invariant" — a wording task for T2.3 `[TIER: HAIKU]`.

### T2.3 — Kernel-verify the PTA frequency-ratio prediction `[TIER: HAIKU]`
- **Motivation:** Part A.3 — the parameter-free ratio test is under-used.
- **Steps:** add to `lean4_formal_proofs/Agora/Phenomenology/` a theorem `pta_frequency_ratio_in_interval`: given f ∝ m_a and the certified mass-ratio interval, the ratio of the two predicted PTA signal frequencies lies in (1.73, 1.75). This is exact-ℚ arithmetic reusing `mass_ratio_in_interval` — a norm_num composition, well within Haiku scope using existing lemmas as template.
- Then add one paragraph to Part I §Observational Predictions: "**The ratio test:** simultaneous detection of both lines with frequency ratio outside (1.73, 1.75) falsifies the two-vacuum K3 interpretation independently of all moduli parameters." Add the same to PREDICTIONS.md as Prediction 4b.
- **Acceptance:** `lake build Agora` clean; the paragraph appears in both files (Rule 6).
- **Verify:** `cd lean4_formal_proofs && lake build Agora && grep -c "ratio test" ../PREDICTIONS.md ../manuscripts_and_proofs/K3_DarkMatter_Preprint.tex`

---

## WORKSTREAM 3 — Superradiance done right (attacks GAP-3, GAP-4)

### T3.1 — Implement Dolan (2007) continued-fraction growth rates `[TIER: SONNET+]`
- **Inputs:** `scripts/superradiance_growth_rate.py` (current small-α version).
- **Steps:** implement Leaver's continued-fraction method for the massive scalar on Kerr (Dolan 2007 Class. Quantum Grav. 24, 4749, Eqs. for the three-term recurrence); validate against Dolan's published Table/figures at α ∈ {0.1, 0.25, 0.42} (digitized reference values hardcoded with citation); then evaluate growth/decay rates for the *bare* couplings α = 0.155 (S₁,₂) and α = 0.089 (S₂,₁), modes l=m=1 and l=m=2, spin a* ∈ {0.8, 0.9, 0.94}.
- **Acceptance (Rule 1):** validation reproduces Dolan reference points to ≤ 5%; output JSON with all rates + spin-down timescales vs. the M87* age/accretion-spin-up timescale comparison.
- **Verify:** `python scripts/dolan_growth_rates.py --validate && python scripts/dolan_growth_rates.py --evaluate`

### T3.2 — The S₂,₁-first analysis `[TIER: HAIKU]` (after T3.1)
- **Steps:** using T3.1 rates, compute the superradiance instability timescale for S₂,₁ bare (no chameleon) for M87* and for the 5 highest-spin SMBHs with published spin estimates (use archival values with citations; store in `data/observational/smbh_spins.csv` with the `empirical-data-validation` metadata block). Determine: does S₂,₁ survive with *zero* screening?
- **Acceptance:** a table `docs/superradiance/S21_bare_survival.md` with survive/excluded per BH per spin value; conclusion sentence propagated to Part I §Limitations item 2 (Rule 6).
- **Verify:** `python scripts/s21_bare_analysis.py && cat docs/superradiance/S21_bare_survival.md`

### T3.3 — Physical screening alternatives memo `[TIER: HUMAN + SONNET+ draft]`
- **Steps:** literature-grounded memo `docs/screening/alternatives.md` comparing chameleon (n>0 branches), symmetron, and environment-dependent mass from the T² coupling itself (m_a ∝ V_{T²}^{−1/2} with V_{T²} responding to local curvature — check whether the model's *own* modulus coupling supplies density dependence without a new field). Each alternative: exponent it predicts, whether γ_eff ≈ 0.25 is attainable physically, falsifiable lab consequence (Eöt-Wash range).
- **Acceptance:** three alternatives, each with a derived (not asserted) γ_eff and a citation; recommendation ranked. Human sign-off required before any manuscript change.

---

## WORKSTREAM 4 — Formal verification closure (attacks GAP-6)

### T4.1 — Compile the WZ certificate into Lean `[TIER: SONNET+, chunked for HAIKU]`
- **Inputs:** verified certificate R(n,k) from `scripts/verify_wz_certificate.py` (SymPy: diff = 0 exact); existing chunking machinery from ROADMAP.md Phase 4 ("polynomial splitting techniques ... compiled without heartbeat timeouts").
- **Steps:**
  1. `[HAIKU]` Export the certificate polynomials to Lean syntax via a generator script (`scripts/gen_wz_lean.py`) — mechanical translation, template provided by the existing chunk files.
  2. `[SONNET+]` Prove the per-k telescoping identity `G(n,k+1)·s(n,k+1) − G(n,k)·s(n,k) = Σᵢ Pᵢ(n)·s(n+i,k)` by `field_simp; ring` on the generated polynomial identity, split into ≤ 8 chunks if heartbeats exceed limits.
  3. `[HAIKU]` Assemble via `Finset.sum_telescope`; replace `axiom s20_recurrence_order_4` with the theorem; delete the axiom; update the disclosed-axioms tables in OPEN_PROBLEMS.md, CAVEATS.md §6, README.md §Reproduction, and both manuscript §2/§AI-Methodology blocks (Rule 6 — five locations, grep-verified).
- **Acceptance:** `lake build Agora` clean; `grep -rn "axiom s20_recurrence" lean4_formal_proofs/` returns nothing; all five prose locations updated.
- **Verify:** `cd lean4_formal_proofs && lake build Agora && ! grep -rn "axiom s20_recurrence" .`

### T4.2 — Kernel-verify S₁,₂/S₂,₁ recurrences for n ≤ 20 `[TIER: HAIKU]`
- **Steps:** mirror the existing `s20_recurrence_checked` pattern (`decide` proofs) for the two *surviving* candidates' order-3 recurrences, n ≤ 20 each. These are the sequences the physics actually rests on; currently only S₂₀ (the excluded family) has finite-range kernel checks. Template: `Structures/S20Recurrence.lean`.
- **Acceptance:** new module `Structures/S12S21Recurrence.lean` builds; CAVEATS.md §6 table gains two ✅ rows.
- **Verify:** `cd lean4_formal_proofs && lake build Agora`

---

## WORKSTREAM 5 — Cosmology pipeline to Boltzmann grade (attacks GAP-5)

### T5.1 — Tracker-consistent initial conditions `[TIER: HAIKU]`
- **Inputs:** quintessence solver in `simulations/` (Radau integrator, shooting method).
- **Steps:** replace rest ICs (φ̇=0) with the exponential-potential tracker/scaling ICs (standard closed form: during radiation domination the scaling solution has Ω_φ = 4/λ² and known φ̇; encode with citation to Copeland–Liddle–Wands 1998, Eq. 3.13). Re-run the λ sweep of Part II Table 1; regenerate (w₀, wₐ) per λ; diff against the rest-IC table and write `docs/cosmology/ic_sensitivity.md`.
- **Acceptance (Rule 1):** executed table, both IC choices, side by side; if (w₀, wₐ) at λ=1.6724 moves by > 0.01, flag for manuscript update via `cross-consistency-gate` (Rule 8 — Table 1, abstract, and PARAMETER_LEDGER must move together).
- **Verify:** `python simulations/quintessence_sweep.py --ic tracker --compare rest`

### T5.2 — CLASS fork ingestion of the mass-varying axion fluid `[TIER: SONNET+]`
- **Steps:** implement ρ_DM(a) ∝ a^{−3−ε} with ε = 0.0251 as a modified fluid in a CLASS fork (or AxiCLASS if the axion perturbation treatment is preferred); compute C_ℓ^{TT,TE,EE}; χ² against Planck 2018 plik-lite; recompute the H₀ shift with full perturbations.
- **Acceptance:** the "indicative H₀ ~ 72" claim in Part II is replaced by an executed number with χ²; if the shift shrinks or reverses, that is the result — report it plainly (Rule 4; the `honest-alternatives-generator` skill governs the rewrite).
- **Verify:** `python empirical_crucible/class_fork_validation.py --planck-lite`

### T5.3 — Joint ε likelihood: JWST × S₈ (the see-saw falsification test) `[TIER: SONNET+; data prep HAIKU]`
- **Steps:**
  1. `[HAIKU]` Data prep with `empirical-data-validation` metadata blocks: UNCOVER z>8 stellar-mass catalog; DES Y3 + KiDS-1000 S₈ posteriors (published chains or Gaussian approximations with citations).
  2. `[SONNET+]` Build L(ε) = L_JWST(ε)·L_S₈(ε); report the two single-probe posteriors and their overlap.
- **Acceptance:** the VISION.md §4A falsification criterion executed: if the two ε posteriors are mutually exclusive at >3σ, **the see-saw hypothesis is dead** — and that goes in the abstract of the next manuscript revision, not a footnote.
- **Verify:** `python empirical_crucible/joint_epsilon_likelihood.py --report`

### T5.4 — DESI DR2 refit `[TIER: HAIKU]` (when DR2 BAO tables are public)
- **Steps:** re-run the existing BAO χ² machinery on DR2 distances; update λ, w₀, wₐ posteriors; run the full `cross-consistency-gate` checklist (code, both manuscripts, JSONs, ledger).
- **Acceptance:** one commit, all sources moved in lockstep, `scripts/cross_consistency_check.sh` exits 0.

---

## WORKSTREAM 6 — PTA endgame preparation

### T6.1 — Injection-recovery forecast for the two lines `[TIER: SONNET+]`
- **Steps:** using `enterprise`/`enterprise_extensions`, inject monochromatic signals at T = 7.52 d and 13.08 d into NANOGrav 15-yr-like synthetic residuals (clearly labeled forecast, Rule 1 honored by labeling); determine the detectable amplitude threshold vs. the model's predicted δφ² amplitude for local FDM density 0.4 GeV/cm³.
- **Acceptance:** `docs/pta/forecast.md` stating detectable-or-not per line per dataset era (15-yr, SKA); PREDICTIONS.md Prediction 4 gains the quantitative sensitivity row.

### T6.2 — Galactic-frame discriminant specification `[TIER: HAIKU]`
- **Steps:** write the analysis spec `docs/pta/galactic_frame_test.md`: phase model for a galactic-rest-frame oscillation as seen from the barycenter (annual modulation formula), vs. terrestrial systematics locked to solar/lunar ephemerides; provide the explicit phase-residual formula and the statistical test (likelihood-ratio between frame hypotheses). This is documentation of already-stated intent (Part I §Systematics), made precise enough for an external PTA collaborator to run.
- **Acceptance:** an external reader could implement the test without contacting the authors.

---

## WORKSTREAM 7 — Compactification scaffold (Goal II; GAP from OPEN_PROBLEMS items 1–2)

### T7.1 — Manuscript §1.5 "Compactification data" `[TIER: HAIKU, from VISION.md template]`
- **Steps:** insert the Type IIA orientifold scaffold paragraph exactly as drafted in VISION.md Goal II (tadpole condition N_flux = 24 − N_D6, axion from RR 1-form on [Σ], absolute scale deferred to stabilization); add Becker–Becker and Vafa–Witten bib entries; add the schematic-input Lean axiom with the `axiom-gap-disclosure` four-ledger routine.
- **Acceptance:** VISION.md Goal II checklist items all check; `lake build` clean; bib compiles.
- **Verify:** `cd manuscripts_and_proofs && pdflatex -interaction=nonstopmode K3_DarkMatter_Preprint.tex && bibtex K3_DarkMatter_Preprint`

### T7.2 — Tadpole feasibility check `[TIER: HUMAN]`
- Per OPEN_PROBLEMS.md items 1–2: verify N_flux ≥ 0 for a concrete orientifold whose K3 fibre matches the S₁,₂/S₂,₁ Hodge data. **Requires a string-phenomenology collaborator.** The templates `data/theory_inputs/orientifold_dbranes_template.json` and `euclidean_instantons_template.json` already exist for this handoff. The Agora side's deliverable is only to keep those templates synchronized with WS1 outputs `[TIER: HAIKU]`.

---

## WORKSTREAM 8 — Continuous integrity (always on)

### T8.1 — Implement `scripts/cross_consistency_check.sh` for real `[TIER: HAIKU]`
- The `cross-consistency-gate` skill specifies it; implement against the actual repo layout for the ledger values (λ, w₀, wₐ, H₀, ε, both masses, both stiffness integers, both α_eff, both PTA periods). Create `PARAMETER_LEDGER.yaml` at repo root populated with current values and source line references.
- **Verify:** `bash scripts/cross_consistency_check.sh; echo $?` → 0

### T8.2 — CI gate `[TIER: HAIKU]`
- GitHub Actions workflow: on PR → `lake build Agora`, `pytest tests/`, `cross_consistency_check.sh`, and a grep asserting zero `sorry` in `lean4_formal_proofs/`. Failures block merge (Rules 2, 8).

---

## Dependency graph & sequencing

```
      T8.1 → T8.2 (do first; cheap, protects everything after)
GAP-6: T4.1 ─────────────────────────────┐
GAP-1: T1.1 → T1.2 → T1.3 → T1.4 ────────┤
GAP-2: T2.1 → T2.2 → T2.3 ───────────────┼→ Manuscript revision v2 → JCAP submission
GAP-3/4: T3.1 → T3.2 → T3.3 ─────────────┤      (VISION.md checklist)
GAP-5: T5.1 → T5.2 → T5.3 → T5.4 ────────┘
Parallel: T4.2, T6.1, T6.2, T7.1 anytime; T7.2 external
```

**Recommended execution order for a Haiku-class agent working alone:**
T8.1 → T8.2 → T4.2 → T2.1 → T2.3 → T1.1 → T1.2 → T1.3 → T1.4 → T5.1 → T3.2* → T6.2 → T7.1 → T5.4*
(* = has an upstream SONNET+/data dependency; skip and report if unmet.)

## Milestones

| Milestone | Definition of done | Gates |
|---|---|---|
| **M1 — Hygiene** | CI green, ledger live, S₁,₂/S₂,₁ finite-range kernel checks | T8.1–2, T4.2 |
| **M2 — Geometry verdict** | Monodromy + modularity + integrality evidence tables published; CAVEATS §2 upgraded or K3 label downgraded | WS1 |
| **M3 — Sorry-free *and* axiom-minimal** | S₂₀ general-n is a theorem; axiom count reduced by 1 | T4.1 |
| **M4 — Superradiance verdict** | Dolan-grade rates; S₂,₁-bare survival table; screening decision | WS3 |
| **M5 — Boltzmann-grade cosmology** | CLASS-fork χ² vs Planck; joint-ε see-saw test executed (survives or dies) | WS5 |
| **M6 — Submission** | VISION.md checklist fully checked; v2 manuscripts; JCAP | all |

## Standing instructions to the executing agent (any tier)

1. **Never invent numbers.** If a script fails, report the traceback verbatim (Rule 1, skill `strict-math-verification`).
2. **Never upgrade a claim's tier.** Computational evidence is [VERIFIED-computational], only `lake build` makes [VERIFIED-kernel] (skill `claim-classification-audit`).
3. **Negative results are results.** If T1.2's Weil bounds fail, T5.3's posteriors exclude each other, or T3.2 excludes S₂,₁ — those outcomes go to the *top* of the report and into the manuscripts (Rule 4, skill `honest-alternatives-generator` for the rewrite).
4. **One number, everywhere.** Any task touching λ, w₀, wₐ, H₀, ε, masses, stiffness, α_eff, or PTA periods triggers the full `cross-consistency-gate` checklist before commit (Rule 8).
5. **Stop conditions.** Ambiguous spec, missing data file, or heartbeat/timeout in Lean chunking → halt, write a `BLOCKED:` note in the task log, do not improvise.
