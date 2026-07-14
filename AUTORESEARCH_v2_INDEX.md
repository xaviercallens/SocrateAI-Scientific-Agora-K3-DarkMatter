# AutoEvolve R2 — Complete Planning & Execution Index

**Status:** STAGED FOR EXECUTION (not yet implemented)  
**Release date:** 2026-07-14  
**Git origin:** All committed and pushed; ready for low-cost LLM implementation

---

## ✅ Documentation Complete — Five Entry Points

### 1. **START HERE** → [`AUTORESEARCH_R2_RELEASE_NOTES.md`](AUTORESEARCH_R2_RELEASE_NOTES.md)
**Executive summary (3 pages):** What v2 does, why, timeline, success metrics, key innovation (answer-key controls).  
**For:** Stakeholders, oversight, quick understanding.

### 2. **ARCHITECTURE** → [`AUTORESEARCH_RELEASE_V2_PLAN.md`](AUTORESEARCH_RELEASE_V2_PLAN.md)
**Detailed specification (120 pages):** All phases A–E, design thesis, gate structure, anti-circularity enforcement.  
**For:** Scientific design review, task specification, edge-case handling.

### 3. **ROADMAP** → [`ROADMAP.md` § Phase 8](ROADMAP.md)
**Phase breakdown with task IDs:** 8 subsections (A–F), executor tiers, task counts per phase.  
**For:** Project management, milestone tracking, gate coordination.

### 4. **CHECKLIST** → [`TODO.md` § Phase 8](TODO.md)
**64 checklistified tasks:** All tasks (LR-1…LR-6, G1-1…G1-4, G2-1…G2-3, QT-1…QT-5, D-1…D-5, DM-1…DM-4).  
**For:** Day-to-day execution, progress tracking, checkbox verification.

### 5. **STEP-BY-STEP** → [`AUTORESEARCH_IMPLEMENTATION_GUIDE.md`](AUTORESEARCH_IMPLEMENTATION_GUIDE.md)
**1000-line walkthrough:** Pre-execution checklist, every task with explicit steps, inputs, outputs, acceptance criteria, debugging.  
**For:** HAIKU/SONNET+ executors, task-level detail, fallback procedures.

### 6. **STRATEGY** → [`VISION.md` § Part III](VISION.md)
**Long-term AutoEvolve trajectory:** Success metrics (3 publishable outcomes), classifier philosophy, citizen-science integration.  
**For:** Strategic alignment, understanding why success is multi-modal.

---

## 📊 Task & Resource Summary

| Metric | Value | Reference |
|--------|-------|-----------|
| **Total tasks** | 64 | TODO.md § Phase 8 |
| **HAIKU tier** | ~54 (85%) | Fully specified, 0 design |
| **SONNET+ tier** | ~4 (6%) | Multi-step derivation |
| **HUMAN gates** | 3 (9%) | Selection decisions only |
| **LLM calls** | ~1,100 | AUTORESEARCH_IMPLEMENTATION_GUIDE.md § 7 |
| **Compute time** | <50 CPU-h | Owned, batched |
| **Timeline** | 12 weeks | AUTORESEARCH_R2_RELEASE_NOTES.md § Timeline |

---

## 🎯 Five Phases at a Glance

| Phase | Goal | Duration | Deliverable | Kill criteria |
|-------|------|----------|-------------|---|
| **A** | Literature review → pool of 13 | weeks 1–2 | `candidate_pool.yaml` (frozen) | LR-1 finds $S_{1,2}$ ≠ K3 in literature |
| **B** | G1/G2 gates: 13 → 5 | weeks 3–4 | `selection_13to5_rationale.md` | Control misclassification halts; classifier fixed |
| **C** | Data tests: 5 → 3 | weeks 5–7 | `selection_5to3_rationale.md` | All blocked or indistinguishable-everywhere |
| **D** | Implementation: 3 → 1 | weeks 8–12 | Part VII + Lean + dossiers | — (all strategies pursued) |
| **E** | Citizen science | ongoing | v1 re-run + Phase C jobs | Quorum disagreement flagged |

---

## 🔑 Key Innovation: Answer-Key Classifier Controls

The classifier will be tested against *literature-known* ground truth embedded in the 13-candidate pool:

| Control | Status | Literature | Role | Expected result |
|---------|--------|-----------|------|---|
| **Apéry ζ(2)** | A005258 | Elliptic, weight-2 (40 years) | Negative control | Classifier must call order-2 |
| **Apéry ζ(3)** | A005259 | K3-type (Beukers–Peters 1984) | Positive control | Classifier must call order-3/K3 |

**Gate rule:** If either control misclassifies → **Phase B halts**, classifier is debugged in-place, Phase B re-runs.  
**Outcome:** This makes classifier validation a visible, public, citable result.

---

## 🛡️ Standing Rules (All Phases)

### Anti-Circularity Enforcement (hard CI gate)

Every parameter must declare `fit_to_target` in `PARAMETER_LEDGER.yaml`. CI check: if fit_target ∈ same task's acceptance criteria → task output void.

```bash
# Before committing each phase output:
./scripts/cross_consistency_check.sh  # includes anti-circularity gate
```

### Rule 1 (Data Integrity)

Never invent data. If a dataset (Euclid Q1, JWST UNCOVER, NANOGrav) requires credentials we lack or terms incompatible with open science → BLOCKED note with clear rationale. No simulated substitutes.

---

## 📁 Directory Structure (create on startup)

```
data/autoresearch_v2/
  sieve_scan_extended.json          (LR-3 output)
  CLASSIFIED_SPORADICS.csv           (LR-2 output)
  g1_order_classification.json       (G1-1 output × 13)
  g1_weil_analysis.csv               (G1-2 output × 13)
  g1_monodromy_status.json           (G1-4 output × 13)
  g2_stiffness_contours.json         (G2-1 output × 13)
  g2_superradiance_bands.json        (G2-3 output × 13)
  selection_13to5_rationale.md       (GATE-B decision)
  qt1_kk_projections.json            (QT-1 output × 5)
  qt2_seesaw_empirical_ttest.json    (QT-2 output × 5)
  qt3_pta_window_analysis.json       (QT-3 output × 5)
  qt5_null_hypothesis_battery.json   (QT-5 output × 5)
  selection_5to3_rationale.md        (GATE-C decision)
  anti_circularity_audit.json        (FE enforcement log)

docs/autoresearch_v2/
  s12_s21_oeis_match.md              (LR-1 output)
  lee_tsai_bridge.md                 (LR-5 output)
  pool_selection_rationale.md        (LR-6 HUMAN decision)

docs/reference/
  lee_tsai_2026.md                   (LR-4 archive)
  el_naschie_2013.md                 (LR-4 archive)

docs/observatories/
  pta_ratio_test_target_dossier.md   (D-5 output)
  lensing_cross_match_targets.csv    (D-5 output)

data/euclid_q1/
  euclid_q1_validation_slice.csv     (EU-1 acquisition)

data/jwst_uncover/
  uncover_z85plus_density_proxies.csv (JW-1 acquisition)

data/citizen_science/
  dmk3_home/                         (DarkMatterK3-Home integration)

manuscripts_and_proofs/
  Part_VII_Hypothesis_Foundry.tex    (D-3 output)
  Part_VII_Hypothesis_Foundry.pdf    (compiled D-3)

lean4_formal_proofs/Structures/
  S1X_Candidate_*.lean               (D-1 modules × 3)
```

---

## 🔄 Git Workflow

### Phase Checkpoints (for resumption)

After each phase completes:
```bash
git tag autoresearch_v2/phase_X_complete
git push origin --tags
```

### Atomic Commits

Each phase is a single, well-documented commit:
- Phase A → one commit with all LR-1…LR-6 outputs + frozen pool
- Phase B → one commit with all G1/G2 results + selection rationale
- Phase C → one commit with all QT results + selection rationale
- Phase D → one commit with Lean + Part VII + dossiers
- Phase E → one commit with citizen-science jobs archived

---

## 📋 Executor Onboarding

### For HAIKU executors
1. Read **AUTORESEARCH_IMPLEMENTATION_GUIDE.md** (your phase)
2. Check **TODO.md** for task checklist
3. Execute task step-by-step; outputs must match acceptance criteria exactly
4. If ERROR: log full trace, escalate to SONNET+/HUMAN
5. Commit on phase completion with full output artifacts

### For SONNET+ executors
1. Read **AUTORESEARCH_RELEASE_V2_PLAN.md** (your task section)
2. Review **AUTORESEARCH_IMPLEMENTATION_GUIDE.md** (multi-step workflow)
3. Execute derivation; outputs must include rationale + caveats
4. Run `cross_consistency_check.sh` before committing
5. Link outputs in git commit message

### For HUMAN gates
1. GATE-A (LR-6): Review ranking rationale in `pool_selection_rationale.md`; approve or request rebuild
2. GATE-B (post G1/G2): Review scored sheet; pick top 5 with rationale
3. GATE-C (post QT): Review observational leverage ranking; pick top 3 with rationale

---

## 🎓 Success Metrics (Three Publishable Outcomes)

| Outcome | Evidence | Citable? | Next step |
|---------|----------|----------|-----------|
| **Outcome A:** Monodromy settlement | ≥1 finalist with computable monodromy solving its geometry class | **Yes** — methodological | → Part VII solo paper |
| **Outcome B:** Falsifiable pair | Data-distinguishable pair with PTA-reachable ratio band (non-circular antecedent) | **Yes** — falsifiable prediction | → Observatory invitations (NANOGrav, lensing) |
| **Outcome C:** Honest closure | All 13 candidates eliminated with classifier passing controls | **Yes** — negative result | → Methodological paper ("The $S_{A,B}$ route is closed") |
| **Classifier win:** Control validation | Classifier passes A005258 (elliptic) and A005259 (K3) tests | **Yes** — classifier validation | → Methods contribution (independent reproducible classification) |

---

## 🚀 Next Action

This release is **READY FOR EXECUTION**. All specifications are complete, all dependencies are committed, all infrastructure is in place.

**To start Phase 8.A (Literature Review):**

1. Create directories in §5 above
2. Invoke **task LR-1** per AUTORESEARCH_IMPLEMENTATION_GUIDE.md § 2 (LR-1)
3. Follow step-by-step; outputs to `docs/autoresearch_v2/s12_s21_oeis_match.md`
4. Commit on completion; push to origin

---

## 📞 Reference Quick Links

| Need | Reference |
|------|-----------|
| Executive summary | AUTORESEARCH_R2_RELEASE_NOTES.md |
| Full architecture | AUTORESEARCH_RELEASE_V2_PLAN.md |
| Task checklist | TODO.md § Phase 8 |
| Step-by-step help | AUTORESEARCH_IMPLEMENTATION_GUIDE.md |
| Roadmap timeline | ROADMAP.md § Phase 8 |
| Long-term vision | VISION.md § Part III |
| Directory structure | This file § 5 |
| Executor guides | This file § 5 (Onboarding) |
| Success metrics | This file § 7 |

---

**Document version:** INDEX RC  
**Last updated:** 2026-07-14  
**Git commits:** `9cd5088`, `450c9af`, `4eeff24`, `ebcba45`  
**Status:** All staged and committed to origin; ready for low-cost LLM execution.
