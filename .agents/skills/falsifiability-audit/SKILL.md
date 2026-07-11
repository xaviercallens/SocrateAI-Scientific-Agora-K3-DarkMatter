---
name: falsifiability-audit
description: Verifies that all [PREDICTED] claims include concrete falsification criteria with measurable precision thresholds, preventing vague or unfalsifiable predictions.
---

# Falsifiability Audit & Rigor Framework

Use this skill when evaluating or proposing predictions, ensuring each one can actually be ruled out by data.

## The Falsifiability Standard

A prediction is **falsifiable** if and only if:

1. **Observable quantity identified:** A physical measurement that can be made by existing or funded instruments
2. **Theoretical prediction stated:** The precise functional form or numerical range the model predicts
3. **Precision threshold given:** The measurement precision at which disagreement counts as falsification (e.g., "Euclid precision σ_{S₈} < 0.01")
4. **Timeline attached:** When will data be available to test this? (e.g., "Euclid DR1 forecast 2026")
5. **Refutability gate:** A clear statement of the form: "If measurement X shows Y to precision Z, the model is falsified"

## Audit Checklist for Each Prediction

**Form:**
```
PREDICTION:     [State the consequence]
OBSERVABLE:     [What quantity will observers measure?]
THEORY VALUE:   [What does the model predict for that quantity?]
PRECISION:      [Measurement uncertainty required for falsification]
TIMELINE:       [When will data be available?]
FALSIFY IF:     [Measurement shows this result at stated precision]
RESOLUTION:     [If falsified, what was wrong? Single field? Initial conditions? Geometry?]
```

**Example (good):**
```
PREDICTION:     S₈ exhibits temporal gradient tracking axion mass decay
OBSERVABLE:     Weak-lensing power C_ℓ(z) in Euclid tomographic bins
THEORY VALUE:   S₈(z) declines as ε·ΔD(z), ε=0.0251; quantitatively ΔS₈/Δz ≈ -0.015
PRECISION:      σ_{S₈} < 0.01 per bin (Euclid design specification)
TIMELINE:       Euclid Tier 1 + 2 releases 2026–2028
FALSIFY IF:     S₈(z) consistent with redshift-independent value at stated precision
RESOLUTION:     If flat: mass-varying mechanism is not realized; alternatives: 
                (a) FDM has constant mass, (b) geometry is not K3×T², (c) initial conditions differ
```

**Example (bad — too vague):**
```
❌ "The model predicts JWST early galaxies are less of a problem"
❌ "We expect future surveys to confirm the prediction"
❌ "The thawing trajectory qualitatively matches DESI hints"
```

## Common Failure Modes

### 1. **Reverse-Engineering Precision**
❌ "The model is compatible with data to 1σ" (only after fitting 5 parameters)
✅ "If S₈ from 10 independent weak-lensing surveys agree to σ < 0.005, the mass-decay model is falsified"

### 2. **Unfalsifiable Hedging**
❌ "The model might predict X or alternatively might predict Y depending on unknown physics"
✅ "The model predicts X [show why]; if future data favors Y and Y is incompatible with X at >2σ, the model is ruled out"

### 3. **Vague Timeline**
❌ "Future telescopes will test this"
✅ "Euclid sensitivity to S₈(z) gradients is ~0.01; DESI BAO improvements targeting σ(w₀,wₐ) = (0.03, 0.07) by 2025"

### 4. **Circular Fit + Prediction**
❌ Fit λ to DESI, then claim DESI "confirms" the prediction
✅ Fit λ to DESI (2024), **separate** DESI 2026 data held back for validation; report post-hoc validation accuracy

## Predictions That Are NOT Falsifiable

- "The model is consistent with dark energy" — every EFT is consistent with *some* dark-energy value
- "Future data might show..." — all futures are possible
- "The theory is motivated by string theory" — motivation ≠ testability
- "We expect the Swampland to constrain our model" — abstract principle, not measurement

## For This Project: The Curated Prediction Manifest

Candidates for inclusion in `PREDICTIONS.md` should pass this rubric:

| # | Prediction | Observable | Precision | Falsification | Status |
|:--:|:---|:---|:---|:---|:---|
| 1 | S₈(z) gradient | Euclid C_ℓ(z) | σ < 0.01/bin | Flat S₈ within errors | ✓ Ready |
| 2 | ELT Sandage-Loeb drift | Lyα forest $\dot{z}$ | cm s⁻¹ yr⁻¹ | Slope matches Λ CDM | ✓ Ready |
| 3 | LISA GW-leakage ratio | d_L^GW / d_L^EM | Δ < 0.05 | Ratio = 1 at 2σ | ✓ Ready |
| 4 | PTA monochromatic lines | NANOGrav/EPTA power | SNR > 3 | No excess at 7.52 d, 13.08 d | ✓ Ready |
| ? | Quasar α-drift slope | Keck/VLT/ESPRESSO Δα/α vs z | Δ(slope) < 10⁻⁶ | ESPRESSO null result ±2σ | ⚠ In development |

## Handling "Soft" Predictions

Some physical claims are intrinsically harder to falsify quantitatively (e.g., "Does chameleon screening work?"). For these:

1. **State the foundational assumption clearly:** "We assume chameleon screening lifts the superradiant coupling by factor ~10 [Mechanism: density-dependent mass, supported by lab experiments but not proven in astrophysical context]"
2. **Identify what would falsify the assumption:** "Direct detection of axion-induced GW strain from M87*, or measurement of spin-evolution incompatible with absorption, would falsify the chameleon hypothesis"
3. **Link to [AXIOM] in formal code:** If unproven, it belongs in the Lean file as an explicit `axiom`

## Output Template

```
AUDIT: [PREDICTION name]

✓ PASS / ⚠ MARGINAL / ✗ FAIL

If PASS:
  - Observable: [measurement type]
  - Threshold: [precision requirement]
  - Falsification gate: [clear statement]
  - Status for publication: READY

If MARGINAL:
  - Missing: [timeline? precision? refutability gate?]
  - Remediation: [add precision forecast, specify falsification threshold, obtain instrument commitment]

If FAIL:
  - Reason: [vagueness, circularity, unfalsifiability]
  - Recommendation: Reframe as [FITTED] claim instead, or reformulate prediction with explicit precision
```
