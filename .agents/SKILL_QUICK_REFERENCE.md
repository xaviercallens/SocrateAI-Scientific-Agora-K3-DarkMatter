# Skills Quick Reference — Copy to Your Editor

**Print this or keep it as a scratch file while working.**

---

## Claim Classification Cheat Sheet

```
[VERIFIED]   = Kernel-proved (Lean ✓) or exact-computed (SymPy ✓)
[FITTED]     = Parameter fit to data; include error bar
[PREDICTED]  = Falsifiable future consequence; include falsification criterion
```

### Template
```
Claim: [Your statement]
Label: [VERIFIED|FITTED|PREDICTED]
Justification: [Link to proof module, fit dataset, or prediction paper]
```

### Quick Test
❌ "The model satisfies the Swampland bound"
✅ "λ=1.6724 [FITTED to DESI BAO] exceeds √2 [VERIFIED], violating single-field attractor [PREDICTED, falsifiable by DESI precision]"

---

## Falsifiability Checklist

Every [PREDICTED] must have:
```
[ ] Observable: What quantity will be measured?
[ ] Theory value: What does the model predict?
[ ] Precision: At what σ is disagreement "falsification"?
[ ] Timeline: When will data arrive? (5-year target)
[ ] Falsify if: "Measurement shows X at stated precision"
```

---

## Axiom Disclosure Checklist

If adding an `axiom` to Lean:
```
[ ] Axiom declared with comment in .lean file
[ ] Justification in comment (why it's unproven)
[ ] Entry added to OPEN_PROBLEMS.md with discharge path
[ ] Caveat added to CAVEATS.md with physics implications
[ ] Manuscript caveat written (search all papers for dependent claims)
```

Manuscript caveat template:
```latex
\textbf{Caveat [ID]:} This result depends on [axiom name]. 
[What goes wrong if assumption is false?] 
See OPEN_PROBLEMS.md (item X).
```

---

## Data Validation Checklist

Every empirical result needs:
```
[ ] Dataset origin & DOI documented
[ ] Retrieval script in scripts/ (bash or Python)
[ ] Processing cuts logged in code comment
[ ] Error bars from data paper propagated (not replaced)
[ ] χ²/dof reported (never just "fits well")
[ ] Reproduces published figures? (✓ verified)
```

Quick template:
```python
# DATASET: [Name]
# Origin: [Author(s) YYYY, DOI/arXiv]
# Fetch: bash scripts/fetch_[name].sh
# Cuts: [z range, systematics, masking applied]
# χ²/dof: [value] (✓ reproduces Fig X in paper)

data = load_dataset('path/to/data.csv')
```

---

## Consistency Gate (Rule 8)

Before every commit with parameter changes:
```bash
# Search for parameter across all files
grep -r "lambda_fit\|w0\|w_a\|H0" \
  simulations/ empirical_crucible/ manuscripts_and_proofs/ data/

# Visual check: do all instances have same value ± rounding?
# Update PARAMETER_LEDGER.yaml
# Run: scripts/cross_consistency_check.sh  (should exit 0)
```

---

## Alternatives Framework (Tier 1–3)

When a result is falsified or produces tension:

### Tier 1: Conservative (tune parameters, same structure)
```
Mechanism: [What parameter changes?]
Prediction: [New observable consequence]
Falsify if: [What measurement rules this out?]
Cost: [Why might we not want this?]
```

### Tier 2: Moderate (add/change assumption within framework)
```
Mechanism: [New coupling, new field, etc. — write equation]
Prediction: [Observable consequence]
Falsify if: [Measurement falsification criterion]
Cost: [New free parameters, naturalness concerns, etc.]
```

### Tier 3: Radical (different fundamental picture)
```
Mechanism: [Conceptual shift — e.g., transient DE]
Prediction: [Unique observable]
Falsify if: [Measurement that rules it out]
Cost: [Loses predictive power for? Requires new physics?]
```

---

## Before Release: Blocking Checklist

```bash
# 1. Consistency
scripts/cross_consistency_check.sh  # Exit code 0?

# 2. Math
lake build Agora  # Zero errors? No sorry?

# 3. Data
jupyter nbconvert --execute empirical_crucible/Agora_Empirical_Validation.ipynb
# Outputs match cached version?

# 4. Caveats
grep -r "AXIOM\|OPEN_PROBLEMS\|CAVEATS.md" manuscripts_and_proofs/*.tex
# Every axiom dependency has caveat? ✓

# 5. Predictions
grep "\[PREDICTED\]" manuscripts_and_proofs/*.tex
# Each [PREDICTED] has falsification criterion? ✓

# 6. Claims
# Run claim-classification-audit on all new sections
# All labels consistent? No creep? ✓

echo "✓ Ready to release if all above pass"
```

---

## When Stuck: Which Skill to Use?

| You're writing... | Use skill... |
|---|---|
| Paper section | claim-classification-audit |
| Predictions table | falsifiability-audit |
| Methods/assumptions | axiom-gap-disclosure |
| Data fitting | empirical-data-validation |
| Discussing tension | honest-alternatives-generator |
| Code parameters | cross-consistency-gate |
| Lean proof | strict-math-verification |

---

## Emergency Checklist: "Did I Just Hallucinate This?"

Ask yourself:

1. **Is this [VERIFIED]?**
   - ❌ "No, I read it in a paper" → Cite paper, call it [FITTED] or [PREDICTED]
   - ❌ "No, I computed it in my head" → Run code to verify
   - ✅ "Yes, Lean kernel proved it" → [VERIFIED] ✓

2. **Is this [FITTED]?**
   - ❌ "No, I guessed χ²/dof" → Recompute from real data
   - ❌ "No, I used synthetic data" → Redo with real data or label "Forecast"
   - ✅ "Yes, here's the loss function and dataset" → [FITTED] ✓

3. **Is this [PREDICTED]?**
   - ❌ "No, I'm not sure how to test it" → It's not falsifiable; don't publish
   - ❌ "No, I said 'might' or 'could'" → Remove hedging; be specific
   - ✅ "Yes, if measurement shows X with precision Y, we're ruled out" → [PREDICTED] ✓

---

## One-Liner Reminders

> Every number in code must appear in paper; every number in paper must be in code.

> [VERIFIED] claims need Lean. [FITTED] claims need error bars. [PREDICTED] claims need falsification criteria.

> Axiom in code → comment in code → entry in CAVEATS.md → caveat in manuscripts.

> Never fit synthetic data. Never report χ² without dof. Never say "consistent" instead of "fits with χ²/dof=X".

> If you can't test it, don't claim it. If you can't falsify it, it's not a prediction.

