# AutoEvolve R2 Implementation Guide
## Executing the Hypothesis Foundry at Low Cost

**Document status:** IMPLEMENTATION READY (not yet started)
**Audience:** HAIKU-tier LLM executors, SONNET+ for derivations, HUMAN gates for selection
**Reference:** `AUTORESEARCH_RELEASE_V2_PLAN.md` (detailed spec), `ROADMAP.md` §3 (architecture), `TODO.md` §0 (task checklist)

---

## 1. Pre-Execution Setup (checklist before ANY task)

- [ ] Clone/sync `https://github.com/xaviercallens/DarkMatterK3-Home.github.io` as `data/citizen_science/dmk3_home/` for volunteer integration
- [ ] Verify `scripts/k3_sieve_analysis.py` has GAP-1 fixes (corrected order classifier with held-out validation at n≤110)
- [ ] Verify `scripts/dolan_continued_fraction.py` compiles and validates against published reference points (≤5% error)
- [ ] Verify `scripts/cross_consistency_check.sh` is executable and CI-integrated
- [ ] Create `data/autoresearch_v2/` directory structure: `{sieve_scan, weil_analysis, monodromy_status, g2_*.json, qt*_*.json, selection_*.md}`
- [ ] Create `docs/autoresearch_v2/` directory: `{s12_s21_oeis_match.md, lee_tsai_bridge.md}`
- [ ] Create `docs/reference/` if absent; add `lee_tsai_2026.md`, `el_naschie_2013.md`

---

## 2. Phase A Task Execution (weeks 1–2)

### LR-1: OEIS Cross-Match (HAIKU)

**Input:** Binomial forms $S_{1,2}(n)=\sum_k\binom{n}{k}\binom{n+k}{k}$ and $S_{2,1}(n)=\sum_k\binom{n}{k}^2\binom{n+k}{k}$; OEIS search API

**Steps:**
1. Query OEIS for binomial sums matching $S_{1,2}$ and $S_{2,1}$ term-by-term (first 10 terms exact match)
2. Cross-reference results against Zagier 2009 "Integral solutions of Apéry-like recurrences" and Cooper 2012 sporadic sequences
3. For each match, record: OEIS ID, weight (if classified), modularity status, Beukers attestation

**Key finding to document:**
- $S_{2,1}$ should match **A005258 (Apéry ζ(2) sequence)**, which is classically **elliptic/weight-2**
- If confirmed, this *independently validates* the GAP-1 reclassification

**Output:** `docs/autoresearch_v2/s12_s21_oeis_match.md` with table:
```
| Sequence | OEIS ID | First-10-term match | Weight | Modularity | Beukers? | Literature geometry |
|----------|---------|---------------------|--------|------------|----------|---------------------|
| S_{1,2}  | ?       | ?                   | ?      | ?          | ?        | K3 (conjectural)    |
| S_{2,1}  | A005258 | ✓                   | 2      | proven     | ✓        | Elliptic (Apéry ζ2) |
```

**Acceptance:** Exact OEIS IDs + geometry assignments recorded without hedging. If $S_{2,1}$ ≠ A005258 → note discrepancy and re-escalate.

---

### LR-2: Enumerate Classified Sporadics (HAIKU)

**Input:** Zagier 2009 §4 (6 sporadic order-2 sequences), Cooper 2012 order-3 table, AESZ Calabi-Yau operators database

**Steps:**
1. Tabulate Zagier's 6 order-2 sequences + their first-10 terms
2. Tabulate Cooper's order-3 sporadics (s₇, s₁₀, s₁₈, relatives)
3. Add Domb numbers (A002895, order-3, hypergeometric family)
4. Add Almkvist–Zagier order-3 entries from AESZ database (≥5)
5. Verify exact binomial-sum forms for each

**Output:** `data/autoresearch_v2/CLASSIFIED_SPORADICS.csv` with ≥15 sequences:
```
name, oeis_id, binomial_form, order, weight, modularity_status, literature_geometry, citation
Apéry_ζ3, A005259, ∑_k (C(n,k))³ C(n+k,k), 3, 3, proven, K3, Beukers-Peters 1984
Domb, A002895, ..., 3, 2, ?, ?, ...
```

**Acceptance:** ≥15 named sequences with exact forms and citations present.

---

### LR-3: Extended Sieve (HAIKU batch)

**Input:** Corrected `k3_sieve_analysis.py` (GAP-1 fixes), domain $(A,B)\in[1,8]^2$ + 3-factor $S_{A,B,C}(n)=\sum_k\binom{n}{k}^A\binom{n+k}{k}^B\binom{2k}{k}^C$

**Steps:**
1. Run sieve over $(A,B)\in[1,8]^2$, 2-factor: order-3 candidates only
2. Run sieve over $(A,B,C)\in[0,3]^3$, 3-factor: order-3 candidates only
3. For each order-3 survivor, validate against held-out set: ≥70 held-out terms, $n_{\max}\ge110$, residuals exactly 0.0
4. Log all order-3 survivors with residual data

**Output:** `data/autoresearch_v2/sieve_scan_extended.json`:
```json
{
  "2-factor": [
    {"A": 2, "B": 1, "order": 3, "held_out_n": 85, "residuals_exact": true},
    ...
  ],
  "3-factor": [
    {"A": 1, "B": 1, "C": 1, "order": 3, "held_out_n": 70, "residuals_exact": true},
    ...
  ]
}
```

**Acceptance:** Every order-3 survivor has held-out residuals = 0.0 exactly. Any non-zero residual → halt and debug classifier.

---

### LR-4: Archive Reference Documents (HAIKU)

**Input:** Lee & Tsai 2026 (Phys. Rev. D 114, L011701); El Naschie 2013 (JQIS 3, 23–26)

**Steps:**
1. Extract full BibTeX for Lee & Tsai; create `docs/reference/lee_tsai_2026.md`:
   - Citation block
   - 5-line summary (5D $S^1/(Z_2×Z_2')$ orbifold, fermionic DM + dark photon, resonance-enhanced annihilation/self-interaction, direct-detection/accelerator predictions, **different particle content from axions**)
   - Epistemic classification: "mainstream theoretical cosmology"
   - Role in v2: "bridge to 5D resonance structure; v2 goal is independent K3 geometry validation"

2. Extract full BibTeX for El Naschie; create `docs/reference/el_naschie_2013.md`:
   - Citation block
   - 5-line summary (transfinite set theory, golden-ratio derivation, numerology-class framework)
   - Epistemic classification: "non-dynamical numerology; boundary marker for failure mode"
   - Role in v2: "**explicitly NOT load-bearing**; marks what v2 avoids; Part V's honest framing depends on this distinction"

**Output:** Both markdown files in `docs/reference/`.

**Acceptance:** Epistemic classification present; el Naschie role includes "NOT load-bearing" disclaimer.

---

### LR-5: Lee–Tsai Bridge Memo (SONNET+)

**Input:** Lee & Tsai PRD paper (their Eq. for $m_E^{(n)}$ resonance masses); `THEORY_ALIGNMENT.md` v1 framework

**Steps:**
1. Extract their $(R, m_B)$ resonance-mass formula; identify the input parameters
2. Map onto v1's $m_{\mathrm{eff}}(\Delta) = m_0 e^{k\Delta}$ ansatz
   - Their $R$ (compactification radius) ↔ our $\Delta$ (baryonic asymmetry)
   - Their $(m_E^{(n)})$ resonance levels ↔ our stiffness-scaled mass windows
3. Identify any observational predictions that overlap (self-interaction cross-section bands, direct-detection scattering, accelerator signatures)
4. **Critical section:** "Where the analogy breaks"
   - They assume fermionic DM; we assume axion
   - They derive $R$ from 5D dynamics; we parameterize $\Delta$ from baryonic density
   - No shared Lagrangian; shared structure only
   - Section must be ≥ as long as the alignment section

**Output:** `docs/autoresearch_v2/lee_tsai_bridge.md` (≥2000 words)

**Acceptance:** Bridge memo complete; "breaks" section present, substantial, honest.

---

### LR-6: Pool Freeze + HUMAN Gate 1 (HAIKU + HUMAN)

**Input:** LR-2, LR-3 outputs; Apéry ζ(3) (A005259) and one Zagier order-2 sequence

**Steps:**
1. Rank all candidates by (a) literature-assigned or sieve-confirmed order-3/K3-type status, (b) not previously falsified, (c) known modularity data available, (d) distinctness
2. Select exactly 13: include A005259 as positive control, one Zagier order-2 as negative control, plus 11 novel candidates
3. Create `data/autoresearch_v2/candidate_pool.yaml`:
   ```yaml
   candidates:
     - id: "apery_zeta3"
       oeis: "A005259"
       binomial: "∑_k (C(n,k))³ C(n+k,k)"
       literature_geometry: "K3"
       literature_citation: "Beukers-Peters 1984"
       role: "positive control (classifier should assign order-3/K3)"
     - id: "zagier_order2_sample"
       oeis: "A???????"
       binomial: "..."
       literature_geometry: "Elliptic (weight-2)"
       literature_citation: "Zagier 2009"
       role: "negative control (classifier should assign order-2)"
     - id: "s12_original"
       oeis: "? (from LR-1)"
       binomial: "∑_k C(n,k) C(n+k,k)"
       literature_geometry: "K3 (conjectural)"
       prior_status: "v1 main candidate; monodromy uncomputed"
       role: "revisit in Phase B/C"
     # ... 10 more novel candidates from sieve
   ```
4. Present ranked list + rationale to HUMAN for approval

**Output:** Frozen `data/autoresearch_v2/candidate_pool.yaml` + `docs/autoresearch_v2/pool_selection_rationale.md` (HUMAN signs off)

**Acceptance:** Exactly 13 candidates; controls present; HUMAN approves ranking; file immutable for all downstream phases.

---

## 3. Phase B Task Execution (weeks 3–4)

Reuses existing scripts: `k3_sieve_analysis.py`, `modularity_screen.py`, `mirror_map_integrality.py`, `k3_monodromy_verification.py`, `dolan_continued_fraction.py`.

All tasks run in batch on the 13 candidates. Output every intermediate result; **no candidate skipped**. If a test produces `ERROR`, log it with full trace.

### G1-1 to G1-4: Exact-Arithmetic Screens

Per candidate:
1. **G1-1** — Minimal recurrence order via corrected classifier + held-out validation ($n_{\max}\ge110$, ≥70 held-out terms)
   - Output: `order_assigned`, `held_out_max_residual` (must be 0.0), classifier confidence
   - **CONTROL PASS CHECK:** If A005259 doesn't classify as order-3 or if one Zagier doesn't classify as order-2 → **halt, classifier broken, fix before continuing**

2. **G1-2** — Weil bounds + modularity
   - Compute $a_p$ for primes $p < 200$; check $|a_p|\le2\sqrt{p}$ (weight-3) and $|a_p|\le2p$ (weight-2)
   - Output: `weil_weight3_pass`, `weil_weight2_pass`, `ap_table.csv`
   - Note: both bounds may pass or fail; record, don't eliminate based on weight-2 failure alone (GAP-1 lesson)

3. **G1-3** — Mirror-map integrality
   - Extract 30 exact-rational coefficients; check denominator bounds
   - Output: `mirror_integrality_pass`, `failure_detail` if any

4. **G1-4** — Fuchs criterion + RK4 monodromy attempt
   - Identify singular points; check regularity at MUM, cusp, infinity
   - Attempt monodromy loop integration via RK4 (40+ loop steps, 50-digit precision)
   - Output: `fuchs_classification`, `monodromy_computable` (yes/no), error metrics if run
   - **Auto-elevation:** any candidate with computable monodromy is flagged for promotion (settles its geometry class decisively)

### G2-1 to G2-3: Physics Viability

Per candidate:
1. **G2-1** — Stiffness contour extraction
   - For each candidate, compute $V''(0)$ from Picard-Fuchs coefficients
   - Map achievable mass as a function of $(\tau,\mathcal{V})$ family (not a point)
   - Output: `stiffness_value`, `achievable_mass_contour.json` (grid of $(\tau,\mathcal{V})$ → $m_a$)
   - **Note:** no fitting $\tau$ to a target mass; contour is parameter-space output

2. **G2-2** — GD-1 No-Go check
   - Apply `cy_axion_no_go` theorem from `lean4_formal_proofs/Agora/Discovery/FuzzyDarkMatter.lean`
   - Check if candidate's achievable window is entirely pinned to $\sim10^{-23}$ eV
   - Output: `pinned_to_no_go_regime` (yes/no)
   - **Elimination:** if yes → candidate eliminated from further consideration

3. **G2-3** — Dolan superradiance solver
   - Apply `dolan_continued_fraction.py` across candidate's achievable mass windows
   - Evaluate M87* ($M = 6.5\times10^9 M_\odot$, $a_* = 0.90$) instability timescale for modes $l=m=1,2$
   - Compare to Salpeter timescale ($\sim50$ Myr)
   - Output: `bare_survival` (yes/no), `instability_timescale_myr`, `screening_needed_mass_band`
   - Document asymmetry: which sequences need screening and why

### GATE-B-SELECT: Composite Scoring (HUMAN)

**Input:** All G1-1 to G2-3 outputs per candidate.

**Scoring rubric:**
- **G1 pass completeness:** all 4 tests run without ERROR
- **Control validation:** A005259 ≠ order-3 OR Zagier ≠ order-2 → classifier broken, **hard stop**
- **Monodromy computability:** bonus flag (high upside: settles geometry)
- **No-Go clearance:** not pinned to $10^{-23}$ eV regime
- **Superradiance band favorability:** bare survival preferred over screening-needed
- **Overall sanity:** no contradictions between gates; consistency via cross_consistency_check.sh

**Output:** `data/autoresearch_v2/selection_13to5_rationale.md` with scored table + HUMAN-approved top-5 list.

**Acceptance:** HUMAN approves top-5 ranking; Phase C proceeds with exactly 5 candidates.

---

## 4. Phase C Task Execution (weeks 5–7)

### Data Acquisition: EU-1, JW-1, PT-1

**STRICT RULE:** Use only existing, legally accessible data. If access requires credentials we lack or terms we cannot accept → BLOCKED note per Rule 1. **No simulated substitutes.**

- **EU-1 (Euclid Q1):** Query ESA archive; download ≤500-object validation slice to `data/euclid_q1/euclid_q1_slice.csv`. Record full schema + archive access info.
  
- **JW-1 (JWST UNCOVER):** Query UNCOVER public archive; extract $z≥8.5$ galaxies with compact-source classification. Compute $\tilde\rho$ (same formula as WS9: $\tilde\rho = F_r/r_{\text{petro}}^2$ where $F_r = 10^{(22.5-m_r)/2.5}$). Output to `data/jwst_uncover/uncover_z85plus.csv`.

- **PT-1 (NANOGrav 15-yr):** NANOGrav 15-yr dataset is public; download frequency sensitivity curve to `data/pta/nanograv_15yr_sensitivity.csv`.

### QT-1 to QT-5: Observational Tests (HAIKU batch)

Per each of the 5 candidates:

1. **QT-1** — KK projection distinguishability
   - Recompute WS9 KK mass projection on SDSS DR17 using candidate's stiffness-scaled $m_0$
   - Recompute on Euclid Q1 slice (same $\Delta$ methodology)
   - Run Kolmogorov-Smirnov test: $H_0$ = distributions are the same
   - Output: `ks_statistic`, `p_value`, `indistinguishable_from_s12` (yes if $p > 0.9$)
   - **Demotion trigger:** if indistinguishable at $p>0.9$ on both surveys → candidate marked "unfalsifiable-in-practice"

2. **QT-2** — Cosmic See-Saw with real early-universe data
   - Use JW-1 empirical $\Delta$ distribution for $z≥8.5$ (replace synthetic WS11 mock)
   - Recompute $m_{\mathrm{eff}}(\Delta)$ for early and local universes
   - Run two-sided Welch's t-test on $\log_{10}(m_{\mathrm{eff}})$
   - Output: `t_statistic`, `p_value`, `mean_ratio_early_to_local`, `detectability_sigma`

3. **QT-3** — PTA window occupancy
   - Per candidate's achievable mass band, compute implied frequency $f = m_a c^2 / h$
   - Check overlap with NANOGrav 15-yr sensitivity band
   - For candidate pairs, check if their stiffness ratio $\sqrt{1014/336} \approx 1.74$ yields a PTA-reachable frequency difference
   - Output: `pta_mass_band`, `pta_overlap_yes_no`, `pairwise_ratios_reachable`

4. **QT-4** — Lee–Tsai overlap (structural analogy)
   - Per candidate's bare coupling $\alpha$ and achievable mass window, check if self-interaction cross-section $\sigma/m$ lands in the Lee–Tsai-favored SIDM band ($\sim0.1$ – $1$ cm²/g at dwarf scales)
   - Output: `lee_tsai_overlap_yes_no`, `analogy_note: "structural alignment; not a shared-Lagrangian prediction"`

5. **QT-5** — Null-hypothesis battery
   - For each TDA statistic used in QT-1, run `lss_tensor_analytics/null_hypothesis_test.py` comparing real data to Poisson mocks
   - Output: per statistic, `passes_separation` (yes if real ≠ Poisson at >2σ)
   - **Barring rule:** any statistic failing separation → excluded from QT-1 scoring

### GATE-C-SELECT: Observational Leverage Ranking (HUMAN)

**Input:** All QT outputs per candidate.

**Scoring rubric:**
- **Observational leverage:** $\sum$ (# independent G3 tests where candidate is distinguishable from $S_{1,2}$)
- **Falsifiability:** "could this have been killed?" — candidate that survived everything without being tested anywhere is unfalsifiable-in-practice → disfavored
- **Data quality:** no BLOCKED data, real access confirmed

**Output:** `data/autoresearch_v2/selection_5to3_rationale.md` with ranked table + HUMAN-approved top-3 list.

**Acceptance:** Candidates indistinguishable-everywhere are explicitly demoted in HUMAN rationale; top-3 locked.

---

## 5. Phase D Task Execution (weeks 8–12)

### D-1: Lean Kernel Verification (HAIKU chunked)

Per each of the 3 finalists:

1. Create `lean4_formal_proofs/Structures/S1X_Candidate_[ID].lean` on the template of `S12S21Recurrence.lean`
2. Define the recurrence relation for $n\le20$
3. Kernel-verify via `decide` tactic for decidable cases
4. Run `lake build Agora.[CandidateID]` → green (zero `sorry`, no heartbeat timeouts)

**Output:** 3 new Lean modules, all clean.

### D-2: Ledger + CI Integration (HAIKU)

1. Add entries to `PARAMETER_LEDGER.yaml` for each finalist (finalists' masses, stiffness integers, achievability windows)
2. Every entry includes `fit_to_target` field (if any) and disclosure caveat
3. Extend `scripts/cross_consistency_check.sh` to include 3 finalists
4. Run full CI suite: `lake build`, `pytest`, `cross_consistency_check.sh`, grep for `sorry` → all green

**Output:** Updated ledger + CI passing.

### D-3: Part VII Manuscript (SONNET+)

Title: "Part VII: The Hypothesis Foundry — A Gate-Driven Evolutionary Re-Evaluation of K3-Axion Candidates"

Structure:
- **Introduction:** AutoEvolve R2 philosophy, answer-key controls, gate structure
- **Section per finalist** (~4–6 pages each):
  - Recurrence data + Lean kernel results
  - Phase B (G1/G2) findings: monodromy status, No-Go clearance, superradiance band
  - Phase C (QT) observational tests: distinguishability on SDSS/Euclid, PTA window, etc.
  - **Negative results first:** where this candidate fails, why, what it rules out
  - Provenance ledger (every claimed number: source, fit-target, caveat)
- **Observatory Targeting:** concrete dossier for PTA + lensing cross-match
- **Conclusion:** which finalists are most promising and why; open questions

**Output:** `manuscripts_and_proofs/Part_VII_Hypothesis_Foundry.tex`, compiles cleanly.

### D-4: External Verification Invitations (HUMAN)

Post GitHub issues to:
1. **LMFDB/arithmetic-geometry community:** "monodromy verification" issues for any finalist with computable monodromy data
2. **PTA collaborations (NANOGrav, EPTA/InPTA):** "ratio-test forecast" issues with concrete target bands
3. **Weak-lensing survey teams (DES, Euclid lensing):** "K3-DISC cross-match" issues for lensing anomaly targets

Each issue includes: reproduction script, expected inputs/outputs, acceptance criteria for independent verification.

**Output:** 3–6 GitHub issues (public, linked from manuscript).

### D-5: Observatory Targeting Dossier (SONNET+)

Create `docs/observatories/pta_ratio_test_target_dossier.md`:
- Clear statement of the ratio-test falsification criterion
- Frequency bands for each finalist pair (from QT-3)
- Timing baseline required for NANOGrav/EPTA to detect phase shift
- Expected signal strength if hypothesis is true; expected null if false

Create `docs/observatories/lensing_cross_match_targets.csv`:
- Anomaly node coordinates (e.g., K3-DISC-0003: RA 205.0°, Dec +35.0°)
- Radius for weak-lensing shear ($\kappa$) map search
- Expected $\kappa$ signal if order-parameter interpretation is correct
- Decision boundary: alignment beyond statistical noise → evidence; non-alignment → falsification

**Output:** Both dossiers (concrete, actionable, published).

---

## 6. Phase E: Citizen Science Integration

### DM-1 to DM-4: DarkMatterK3-Home Workflow

**DM-1:** Standardize all v2 TDA compute jobs under a schema with (survey_tile, statistic_version_hash, candidate_id, seed, client_version).

**DM-2:** Implement quorum replication: every tile computed by ≥2 independent clients. Disagreement beyond tolerance → tile quarantined, never averaged.

**DM-3:** **Before any v2 manuscript cites the v1 headlines (1.177, Δ=47.0), re-run under DM-1/DM-2 quorum protocol and archive results in `data/dmk3_runs/v1_reproduction/`.**

**DM-4:** Dispatch Phase C TDA jobs (5 candidates × SDSS DR17 + Euclid Q1 tiles) to volunteer network under DM-1/DM-2 protocol.

---

## 7. Anti-Circularity Enforcement (All Phases)

**Standing rule:** Every parameter that is fit to a validation target must declare so in `PARAMETER_LEDGER.yaml`. CI gate: if `fit_to_target` field appears in the same task's acceptance criteria → task output void.

**Audit log:** `data/autoresearch_v2/anti_circularity_audit.json` records every parameter checked.

**Procedure:**
```bash
# Before committing each phase:
./scripts/cross_consistency_check.sh  # includes anti-circularity gate
```

---

## 8. Timeline & Rollout

| Week(s) | Phase | Deliverables | Executor | HUMAN gate |
|---------|-------|--------------|----------|-----------|
| 1–2 | A | `candidate_pool.yaml` (13 locked) | HAIKU + LR-5 SONNET+ | GATE-A: Pool freeze |
| 3–4 | B | `selection_13to5_rationale.md` (5 survivors) | HAIKU batch | GATE-B: Composite score |
| 5–7 | C | `selection_5to3_rationale.md` (3 finalists) | HAIKU + data acquisition | GATE-C: Leverage rank |
| 8–12 | D+E | Part VII + Lean modules + dossiers + citizen jobs | SONNET+ + HAIKU | Invitations open |

**Total LLM cost:** ~1,100 calls (~85% HAIKU, ~15% SONNET+)  
**Owned compute:** <50 CPU-hours  
**HUMAN effort:** ~6 hours (one person at each of 3 gates, reviewing scored sheets)

---

## 9. Success Criteria & Fallback Paths

### Outcome A: Monodromy Settlement
One or more finalists have computable monodromy → geometry class decided independently of K3 speculation → publishable alone.

### Outcome B: Falsifiable Pair
Two finalists distinguishable on real data with a PTA-reachable ratio band that is **not circular** in its antecedent (i.e., the ratio is not constructed to force a specific band) → falsifiable prediction → invitations answered.

### Outcome C: Honest Closure
All 13 candidates eliminated with the answer-key-validated classifier → publishable as "the $S_{A,B}$ route is sterile under this search" → methodological win even if no physics wins.

### Fallback: Classifier Broken
If a control (A005259 or Zagier) misclassifies in Phase B → stop Phase B, fix classifier in-place, re-run Phase B → strong validation of debugging infrastructure.

---

## 10. GitHub & Collaboration Integration

**GitHub repo structure:**
- `docs/autoresearch_v2/` — public documentation + bridge memo
- `data/autoresearch_v2/` — all intermediate results (JSON/YAML/CSV) — **committed to repo**
- `data/dmk3_runs/` — citizen-science job specs + archived runs (external links + local manifests)
- `docs/observatories/` — falsification targets (public-facing)

**DarkMatterK3-Home integration:**
- Fork/link to `https://github.com/xaviercallens/DarkMatterK3-Home.github.io` in `data/citizen_science/dmk3_home/`
- Job specs published to volunteer network automatically from Phase C onwards
- Volunteer results flow back to `data/dmk3_runs/phase_c_jobs/` with quorum enforcement

**External collaboration:**
- Invite arithmetic-geometry community (monodromy verification)
- Invite PTA teams (ratio-test forecast)
- Invite weak-lensing teams (anomaly cross-match)

All via public GitHub issues with reproduction scripts.

---

## 11. Debugging & Failure Modes

### If Phase A LR-1 finds $S_{1,2}$ ≠ K3 in literature
Immediately rebuild the pool around the literature's known K3 candidates. Amend candidate_pool.yaml and re-freeze with HUMAN gate 1. Do not proceed to Phase B until pool is settled.

### If Phase B classifier fails a control
Halt. Do not proceed to Phase C. Investigate classifier + k3_sieve_analysis.py. Fix. Re-run Phase B on all 13. Report findings (including the control failure fix) in a dedicated commit before continuing.

### If Phase C: all 5 candidates fail all tests or all data is BLOCKED
Honest finding: "The AutoEvolve R2 pipeline could not produce falsifiable finalists from the $S_{A,B}$ pool, either due to no distinguishable candidates or unavailable data." This is a publishable negative result.

### If Phase D: Lean verification fails on a finalist
That finalist is removed from the manuscript; only its failure mode is documented. Continue with remaining 2 (or 1).

---

## 12. Checkpoints for Resumption (if interrupted)

- **After Phase A:** Commit `candidate_pool.yaml` + phase-A outputs to git; continue from GATE-A checkpoint
- **After Phase B:** Commit `selection_13to5_rationale.md` + all G1/G2 results; continue from GATE-B checkpoint
- **After Phase C:** Commit `selection_5to3_rationale.md` + all QT results; continue from GATE-C checkpoint
- **After Phase D:** Commit Part VII + Lean modules; push to origin; prepare Release notes

Each checkpoint is tagged in git (e.g., `autoresearch_v2/phase_a_complete`) for easy resumption.

---

**Document maintained by:** SocrateAI Scientific Agora
**Last updated:** 2026-07-14
