# Stream 2 — Selection: AutoEvolve K3 Candidate Ranking

**K3 Candidate Selection via AutoEvolve: Exact-Algebraic Sieving & Swampland Screening**

This is **Stream 2** of the Dual-Scale Topological Universe Model project. Its role is to **rank K3 candidates** against a frozen criteria list using systematic automated search (AutoEvolve).

**See [VISION.md](VISION.md) for the full project scope, roadmap, and epistemic framework.**

---

## What This Repository Does

- **Consumes the frozen criteria** from [K3_CRITERIA.md](K3_CRITERIA.md) (defined by Stream 1).
- **Scores candidates** (Cooper s7, s10, S22, t103, etc.) against Tier A properties (arithmetic, Picard-Fuchs structure) via automated search.
- **Evaluates Tier B claims** (Hodge data, Kodaira fiber types, Swampland constraints) via symbolic computation and expert review.
- **Produces** [K3_SELECTION_REPORT.md](K3_SELECTION_REPORT.md) with final ranking and justification.

This repository is **not** responsible for:
- Formalizing mathematics (→ Stream 1, `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal`)
- Testing predictions against data (→ Stream 3, `SocrateAI-Scientific-Agora-Home`)

---

## Key Documents

1. **[VISION.md](VISION.md)** — The master vision document. Read this first.
2. **[K3_CRITERIA.md](K3_CRITERIA.md)** — Frozen criteria list (Tier A/B). This repo uses these to score candidates.
3. **[PREDICTION.md](PREDICTION.md)** — Draft falsifiable predictions. Your ranking determines which candidates get tested in Stream 3.
4. **[K3_SELECTION_REPORT.md](K3_SELECTION_REPORT.md)** (to be generated) — Your final output.

---

## Repository Structure

```
.
├── agora_ai_agents/         # AutoEvolve orchestrator and scoring agents
│   ├── orchestrator.py      # Main ranking loop
│   ├── agent_math_sympy.py  # Symbolic computation (Tier A criteria)
│   ├── agent_swampland.py   # Swampland screening (Tier B criteria)
│   └── agent_vafa.py        # Vafa distance conjecture checks
├── empirical_crucible/      # Data validation notebooks
├── lean4_formal_proofs/     # Links to Stream 1 Lean proofs (read-only)
├── manuscripts_and_proofs/  # Published papers (for context)
├── simulations/             # Numerical checks for candidate properties
├── scripts/                 # Verification scripts
└── docs/                    # Documentation
```

---

## Workflow (Phase 2)

1. **Lock the criteria** in [K3_CRITERIA.md](K3_CRITERIA.md) (frozen at week 1).
2. **Run AutoEvolve ranking** against Tier A (arithmetic properties).
3. **Evaluate Tier B claims** (geometry, Swampland) via symbolic computation + expert review.
4. **Document verdicts** in [K3_SELECTION_REPORT.md](K3_SELECTION_REPORT.md).
5. **Pass results to Stream 3** so they can test the surviving candidates' predictions.

**Important:** The criteria list is frozen *before* ranking runs. Do not re-weight criteria post hoc to match your preferred outcome.

---

## Running the Candidate Ranking

```bash
# Install dependencies
pip install -r requirements.txt

# Run AutoEvolve ranking against K3_CRITERIA.md
python agora_ai_agents/orchestrator.py --mode ranking --output K3_SELECTION_REPORT.md

# Verify Tier B properties
python simulations/verify_kodaira_fibers.py --candidates s7,s10,S22,t103
python scripts/swampland_check.py --candidates s7,s10,S22,t103
```

---

## Key Rules

- **Criteria freezing:** [K3_CRITERIA.md](K3_CRITERIA.md) is locked before any ranking. Changes require an amendment with rationale.
- **Transparency:** Every score must be traceable to a checkable property (Lean proof, SymPy computation, or expert statement).
- **"The model preferred it" is never sufficient:** AutoEvolve is a tool for systematic search, not an oracle.
- **Parameter-tuning transparency:** If you adjust a score after seeing the results, log it in `TUNING_LOG.md` (VISION.md §4).

---

## Roadmap

| Phase | Dates | Deliverable |
|-------|-------|-------------|
| **Phase 0** | Weeks 1–2 | VISION.md, K3_CRITERIA.md (frozen), draft PREDICTION.md |
| **Phase 1** | Months 1–2 | Finalize prediction with Stream 3 |
| **Phase 2** | Months 2–8 | AutoEvolve ranking → K3_SELECTION_REPORT.md (this repo) |
| **Phase 3** | Months 8–14 | Stream 3 tests survivors against data |

**This repo's focus:** Phase 2 (months 2–8).

---

## Contact & Collaboration

- **Author:** Xavier Callens (callensxavier@gmail.com)
- **Feedback:** Open issues or PRs. Major verdicts should be reviewed by experts in mirror symmetry / modular forms before finalization.
- **Data sources:** See `CAVEATS.md` and `OPEN_PROBLEMS.md` for known limitations.
