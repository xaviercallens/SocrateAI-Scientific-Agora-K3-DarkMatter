# Agora AutoEvolve R2 Release Notes
## The Hypothesis Foundry — A Gate-Driven Evolutionary Re-Evaluation Engine

**Release date:** 2026-07-14  
**Status:** PROPOSED & STAGED — NOT YET IMPLEMENTED  
**Git commits:** `9cd5088` (v2 plan), `450c9af` (structured documentation), `4eeff24` (pushed to origin)

---

## Executive Summary

The **AutoEvolve R2 release** transforms the validation infrastructure that dismantled v1's overclaims into a hypothesis-generation and filtering engine. Using AlphaEvolve-inspired gate-driven evolution (cheap generator + ruthless evaluator) and answer-key classifier controls from the literature, it replicates and extends the K3-dark-sector search over a pool of exactly 13 candidates.

**Key innovation:** The literature already contains ground-truth classifications:
- **Apéry ζ(2) (A005258)** — classically elliptic/weight-2
- **Apéry ζ(3) (A005259)** — classically K3-type (Beukers–Peters 1984)

If the classifier misidentifies these, everything halts. This converts classifier debugging from hidden problems into a visible, public, citable gate.

**Timeline:** 12 weeks, ~85% low-cost HAIKU LLM, 3 HUMAN selection gates, 3 SONNET+ derivations, <50 CPU-hours owned compute, ~1,100 LLM calls total.

---

## What This Release Contains

### 1. Complete Specification Documents (ready for execution)

| Document | Purpose | Audience |
|----------|---------|----------|
| **AUTORESEARCH_RELEASE_V2_PLAN.md** | Detailed architectural spec (9 sections, all phases A–E) | Scientific design + oversight |
| **ROADMAP.md § Phase 8** | 12-week phase breakdown with task IDs | Project management |
| **TODO.md § Phase 8** | Checklistified task list (64 tasks, ~85% HAIKU) | Day-to-day execution |
| **AUTORESEARCH_IMPLEMENTATION_GUIDE.md** | 1000-line step-by-step walkthrough per phase | HAIKU/SONNET+ executors |
| **VISION.md § Part III** | Long-term AutoEvolve trajectory + success metrics | Strategic planning |

### 2. Integrated Infrastructure (already in repo)

| Component | Status | Role in v2 |
|-----------|--------|-----------|
| `scripts/k3_sieve_analysis.py` (GAP-1 fixes) | ✓ Debugged | G1 classifier + held-out validation |
| `scripts/dolan_continued_fraction.py` | ✓ Validated | G2-3: superradiance screening |
| `scripts/cross_consistency_check.sh` | ✓ CI-gated | Anti-circularity enforcement |
| `PARAMETER_LEDGER.yaml` | ✓ Committed | Parameter provenance + fit-target tracking |
| Lean formalization templates | ✓ Compiled clean | D-1: kernel verification per finalist |
| `lss_tensor_analytics/null_hypothesis_test.py` | ✓ In-repo | QT-5: null-hypothesis battery |
| DarkMatterK3-Home.github.io integration | ⏳ Ready | Phase E: citizen-science quorum jobs |

### 3. Structured Execution Tiers

**HAIKU-tier tasks** (fully specified, zero design decisions): 54 tasks  
- LR-1, LR-2, LR-3 (extended sieve)
- G1-1…G1-4, G2-1…G2-3 (exact-arithmetic + physics gates × 13 candidates)
- QT-1…QT-3, QT-5 (observational tests × 5 candidates)
- D-1, D-2, DM-1…DM-4 (Lean + ledger + citizen jobs)

**SONNET+-tier tasks** (multi-step derivation): 4 tasks  
- LR-5: Lee–Tsai bridge memo
- QT-4: structural analogy test
- D-3: Part VII manuscript
- D-5: observatory targeting dossier

**HUMAN-tier gates** (selection decisions): 3 gates  
- GATE-A: Pool freeze (LR-6)
- GATE-B: Composite scoring, 13→5 (post G1/G2)
- GATE-C: Observational leverage, 5→3 (post QT)

---

## Phase Breakdown

### Phase 8.A — Literature Review (weeks 1–2)

**Goal:** Build a candidate pool of exactly 13 sequences with literature-assigned geometries.

**Deliverable:** `data/autoresearch_v2/candidate_pool.yaml` (frozen, immutable for downstream)

| Task | Input | Output | Acceptance |
|------|-------|--------|-----------|
| **LR-1** | OEIS + Zagier/Cooper tables | OEIS match table | $S_{2,1}$ ≡ A005258 (elliptic) confirmed |
| **LR-2** | Sporadics literature | ≥15 classified sequences | All with exact binomial forms + citations |
| **LR-3** | Extended sieve on $(A,B)∈[1,8]^2$ + 3-factor | Order-3 survivors with held-out validation | Every survivor: residuals = 0.0 exactly |
| **LR-4** | Lee & Tsai 2026 + El Naschie 2013 | Archived docs in `docs/reference/` | El Naschie = numerology-class boundary-marker |
| **LR-5** | 5D $(R, m_B)$ resonance formula | Bridge memo with "breaks" section | Breaks section ≥ alignment section length |
| **LR-6** | All LR outputs | Pool of 13 (with controls) | HUMAN approves; controls A005259 + Zagier order-2 present |

**Kill criterion:** If LR-1 reveals $S_{1,2}$ is known and misclassified → adopt literature, rebuild.

---

### Phase 8.B — Exact-Arithmetic + Physics Gates (weeks 3–4)

**Goal:** Filter 13 → 5 via G1/G2 screens using existing, debugged tools.

**Deliverable:** `data/autoresearch_v2/selection_13to5_rationale.md` + GATE-B decision

| Gate | Input per candidate | Output | Kill criterion |
|------|-------|--------|-----------|
| **G1-1** | Recurrence + held-out validation | Order assignment | **Control fails → halt, classifier broken** |
| **G1-2** | 44-prime Weil bounds | $a_p$ table + weight verdict | Recorded, not eliminatory |
| **G1-3** | 30 coefficients | Integrality verdict | Recorded |
| **G1-4** | Fuchs criterion + RK4 monodromy | Singular-point classification + monodromy status | Computable monodromy → auto-elevate |
| **G2-1** | Picard-Fuchs coefficients | Stiffness contour $(\tau, \mathcal{V}) \to m_a$ | Published as contour, never point |
| **G2-2** | Achievable mass window | No-Go regime check | Pinned to $10^{-23}$ eV → eliminate |
| **G2-3** | Achievable window + M87* profile | Dolan instability band | Bare survival vs. screening-needed asymmetry |

**GATE-B-SELECT:** Composite score (G1 completeness + monodromy + No-Go + superradiance + control sanity) → HUMAN picks top 5.

---

### Phase 8.C — Quick Data Tests (weeks 5–7)

**Goal:** Filter 5 → 3 via observational tests on SDSS, Euclid, JWST, PTA.

**Deliverable:** `data/autoresearch_v2/selection_5to3_rationale.md` + GATE-C decision

| Task | Test | Input | Output | Accept/Demote |
|------|------|-------|--------|---|
| **EU-1** | Euclid acquisition | ESA archive | ≤500 slice to `data/euclid_q1/` | If blocked → BLOCKED note (Rule 1) |
| **JW-1** | JWST UNCOVER acquisition | UNCOVER archive | $z≥8.5$ densities | If blocked → BLOCKED note |
| **QT-1** | KK projection distinguishability | 5 candidates × SDSS + Euclid | KS test vs. $S_{1,2}$ | $p < 0.1$ → survives; $p > 0.9$ → demoted (unfalsifiable) |
| **QT-2** | See-saw t-test (empirical $\Delta_{\rm early}$) | JW-1 distribution | Welch t-stat on early vs. local | Recorded |
| **QT-3** | PTA window occupancy | Achievable mass + NANOGrav 15yr | Frequency band + overlap | Ratio-test bands flagged if PTA-reachable |
| **QT-4** | Lee–Tsai overlap | SIDM σ/m band | Structural analogy check | Recorded with "≠ Lagrangian" disclaimer |
| **QT-5** | Null-hypothesis battery | Poisson mocks | Per-statistic separation verdict | Failing separation → barred from QT-1 scoring |

**GATE-C-SELECT:** Observational leverage ranking: (# tests distinguishable) × (falsifiability) → HUMAN picks top 3.

---

### Phase 8.D — Top-3 Implementation + Lean (weeks 8–12)

**Goal:** Real publication-grade finalization of 3 survivors.

**Deliverables:**
1. `lean4_formal_proofs/Structures/S1X_Candidate_*.lean` (3 modules, zero `sorry`)
2. `manuscripts_and_proofs/Part_VII_Hypothesis_Foundry.tex` (negative-results-first essay)
3. `docs/observatories/pta_ratio_test_target_dossier.md` + lensing cross-match targets
4. GitHub issues to external collaborators (monodromy verification, ratio-test forecast)

| Task | Output | Acceptance |
|------|--------|-----------|
| **D-1** | Lean kernel modules (3×) | `lake build` green; zero `sorry` |
| **D-2** | Ledger + CI integration | Extended `cross_consistency_check.sh`; CI green |
| **D-3** | Part VII manuscript | Compiles cleanly; 3 sections (one per finalist); negative results at top |
| **D-4** | External invitations | GitHub issues posted; reproduction scripts included |
| **D-5** | Observatory dossier | Concrete, falsifiable targets published |

---

### Phase 8.E — Citizen-Science Integration

**DarkMatterK3-Home workflow:**
- **DM-1:** Standardized job schema (survey_tile, statistic_hash, candidate_id, seed, client_version)
- **DM-2:** Quorum replication (≥2 independent clients per tile; disagreement → quarantine)
- **DM-3:** Re-run v1 headlines (1.177, Δ=47.0) under quorum; archive before re-citation
- **DM-4:** Dispatch Phase C TDA jobs to volunteer network

---

## Standing Rules (All Phases)

### Anti-Circularity Enforcement (hard CI gate)

Every parameter must declare its fit target in `PARAMETER_LEDGER.yaml`. If `fit_to_target` appears in the same task's acceptance criteria → task output void.

```bash
# Before committing each phase:
./scripts/cross_consistency_check.sh  # includes anti-circularity gate
```

---

## Key Innovation: Answer-Key Classifier Controls

**The Problem:** Classifiers can be wrong in hidden ways.

**The Solution:** Embed ground-truth controls in the candidate pool:
1. **Apéry ζ(2) (A005258)** — literature confirms elliptic/weight-2 (40 years established)
2. **Apéry ζ(3) (A005259)** — literature confirms K3-type (Beukers–Peters 1984)

If the classifier misidentifies either → **G1-1 halts the entire Phase B**, and the classifier is fixed.

**Outcome:** This converts a hidden risk into a visible, testable, publishable gate.

---

## Success Metrics

| Outcome | Metric | Citable? |
|---------|--------|----------|
| **Outcome A** | Computable monodromy settles geometry class decisively on ≥1 finalist | Yes — methodological |
| **Outcome B** | Data-distinguishable pair with PTA-reachable ratio band (non-circular antecedent) | Yes — falsifiable prediction |
| **Outcome C** | All 13 candidates eliminated with answer-key-validated classifier | Yes — negative result |
| **Classifier win** | Classifier passes both controls (A005259 and Zagier order-2) | Yes — independent classifier validation |

All three outcomes are publishable. Outcome C with the classifier passing controls is the strongest evidence yet that the $S_{A,B}$ → dark sector route is closed.

---

## Documentation Hierarchy

```
AUTORESEARCH_RELEASE_V2_PLAN.md (detailed spec, 9 sections, entry point)
    ↓
ROADMAP.md § Phase 8 (architecture overview, task IDs)
    ↓
TODO.md § Phase 8 (checklistified 64 tasks)
    ↓
AUTORESEARCH_IMPLEMENTATION_GUIDE.md (step-by-step walkthrough)
    ↓
VISION.md § Part III (strategic trajectory + success metrics)
```

---

## Files & Directories to Create on Startup

Before Phase A begins:

```bash
mkdir -p data/autoresearch_v2/{sieve_scan, weil_analysis, monodromy_status, qt_*, selection_*}
mkdir -p docs/autoresearch_v2/
mkdir -p docs/reference/
mkdir -p docs/observatories/
mkdir -p data/citizen_science/dmk3_home/
```

---

## Git Checkpoints (for resumption)

- After Phase A: tag `autoresearch_v2/phase_a_complete`
- After Phase B: tag `autoresearch_v2/phase_b_complete`
- After Phase C: tag `autoresearch_v2/phase_c_complete`
- After Phase D: tag `autoresearch_v2/phase_d_complete` + push + release

---

## Integration with DarkMatterK3-Home GitHub

**Citizen-science partner repo:** https://github.com/xaviercallens/DarkMatterK3-Home.github.io

- Phase C TDA jobs published to volunteer network
- Quorum-replication results auto-archived
- v1 headline numbers re-run under quorum before re-citation
- Phase D results feed back into volunteer pipeline for independent validation

---

## Backward Compatibility

All Phase 8 outputs live in `data/autoresearch_v2/` and `docs/autoresearch_v2/` (new directories). Existing repos files (Part I–VI manuscripts, PARAMETER_LEDGER, Lean modules, scripts) remain unchanged except:
- `PARAMETER_LEDGER.yaml` gains finalists' entries (2026-07-12 onwards)
- `cross_consistency_check.sh` extended for finalists
- `ROADMAP.md`, `TODO.md`, `VISION.md` updated (documented in commit)

No destructive changes.

---

## Ready to Execute

This release is **READY FOR LOW-COST LLM EXECUTION** as soon as you approve Phase A startup. All tasks are specified with explicit inputs/outputs/acceptance criteria. HAIKU-tier tasks contain zero design decisions.

**Next step:** Invoke Phase 8.A (Literature Review) with LR-1 task (OEIS cross-match).

---

## Git Commit History

| Commit | Message | Key files |
|--------|---------|-----------|
| `9cd5088` | AutoResearch v2 plan (detailed spec) | AUTORESEARCH_RELEASE_V2_PLAN.md |
| `450c9af` | Phase 8 documentation (structured, executable) | ROADMAP + TODO + VISION + GUIDE |
| `4eeff24` | Merged remote changes + pushed to origin | All staged docs + origin sync |

---

## Appendix: The Hypothesis Foundry Philosophy

The v1 validation infrastructure that dismantled the overclaims proved its worth. Rather than fixing that infrastructure away, v2 makes it the centerpiece of a hypothesis-generation engine. AlphaEvolve works because it couples a cheap generator to a ruthless evaluator. We already own the ruthless evaluator. v2 couples it to low-cost LLM generation over the $S_{A,B}$ landscape, with answer-key controls ensuring the classifier is honest.

The result is not a hypothesis that "probably works" — it's a **filtered, gate-validated, publicly transparent hypothesis funnel** that either finds something real or closes the route with authority. Either outcome is citable. That's science.

---

**Document version:** RELEASE CANDIDATE
**Status:** STAGED & COMMITTED (2026-07-14)  
**Next:** Await HUMAN approval to start Phase 8.A

