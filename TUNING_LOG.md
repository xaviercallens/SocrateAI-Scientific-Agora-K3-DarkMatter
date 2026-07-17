# TUNING_LOG — Assumption-List Change Audit

**Purpose:** Track every change to assumption lists after phase pin. A tuning event is when a quantity's assumption dependencies grow or shift after M1 (GATE M1 commits the baseline assumption set).

**Entry structure:**
```
## [YYYY-MM-DD] Commit HASH
- **Quantity:** (e.g., `m_φ`, `r_c(M_halo)`, `σ(v)/m`)
- **Old assumptions:** [list at pin]
- **New assumptions:** [list after change]
- **Justification:** (why the dependency grew or shifted)
- **Status:** (approved, escalated, rolled back)
```

---

## Initialization (Phase 0)

*No entries yet — log opens after GATE M1 (MVM pin).* Baseline assumption set at M1:
- A-SEQ (Moduli Sequestering)
- A-VOL (Volume & Coupling Stabilization)
- A-ONT (Dark Sector Ontology)
- A-REL (Relic Abundance)

Every quantity in PREDICTION.md at M1 carries one of these four tags. Any subsequent growth is a tuning event and must be logged here with explicit justification.

---

## CI Rule

**CI audit:** Every commit touching PREDICTION.md assumption tags must include a TUNING_LOG entry. Failure → CI red.

```bash
# Pseudocode for CI hook
if git diff HEAD~1 HEAD -- PREDICTION.md | grep -E '\[A-(SEQ|VOL|ONT|REL)' > /dev/null; then
  # Assumption tag change detected
  if ! git diff HEAD~1 HEAD -- TUNING_LOG.md | grep "Commit $(git rev-parse --short HEAD)" > /dev/null; then
    echo "ERROR: PREDICTION.md assumption tags changed, but no TUNING_LOG entry. Add entry for commit $(git rev-parse --short HEAD)"
    exit 1
  fi
fi
```

---

## Historical Reference

*Once data contact occurs and results are collected:*
- Every reinterpretation or re-derivation of a result with changed assumptions is logged.
- Tuning events are reportable results — they show where the model gained flexibility post-pin.
- Zero tuning events is the goal; documenting them is the accountability mechanism.
