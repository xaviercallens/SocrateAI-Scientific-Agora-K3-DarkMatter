---
name: claim-classification-audit
description: Ensures all scientific claims are correctly labeled as [VERIFIED], [FITTED], or [PREDICTED] with explicit justification, preventing confusion between proven facts, fitted parameters, and speculative predictions.
---

# Claim Classification & Disclosure Audit

Use this skill whenever writing or reviewing manuscripts, documentation, or code that makes scientific claims.

## The Three-Tier Classification System

**[VERIFIED]** — Kernel-checked (Lean 4) or exact-rational computed
- Can only be contradicted by finding an error in the formal proof or computation
- Example: "The mass ratio √(1014/336) ∈ (1.73, 1.75) [VERIFIED, `Agora.GaugeCoupling`]"

**[FITTED]** — Phenomenological parameter calibrated to data
- Defensible but NOT derived from first principles
- Must state the loss function and data source explicitly
- Example: "λ = 1.6724 [FITTED to DESI 2024 BAO via χ² minimization]"

**[PREDICTED]** — Falsifiable consequence testable by future instruments
- Must include: (1) the prediction, (2) the measurement method, (3) the falsification criterion
- Example: "S₈(z) exhibits temporal gradient [PREDICTED, Euclid precision ~0.01 falsifies]"

## Audit Checklist

**Before any claim is published:**

- [ ] **Identify category:** Is this [VERIFIED], [FITTED], or [PREDICTED]?
- [ ] **Add justification:** Link to proof module, fit procedure, or prediction paper
- [ ] **Disclose origin:** State data source or theoretical foundation explicitly
- [ ] **State uncertainty:** What would prove this claim wrong?
- [ ] **Cross-check labels:** Search the entire manuscript for the same claim; all instances must use the same label
- [ ] **Avoid label creep:** Never upgrade [FITTED] to [VERIFIED] without kernel proof; never call [PREDICTED] "expected" or "likely" (these suggest higher confidence than falsifiability warrants)

## Common Pitfalls to Avoid

❌ **"The model satisfies the Swampland bound"** (ambiguous: FITTED? VERIFIED? Both?)
✅ **"The model produces λ = 1.6724 [FITTED], which exceeds √2 [VERIFIED], violating single-exponential dark energy [PREDICTED]"**

❌ **"Early JWST galaxies are explained by mass-varying axions"** (causal claim, not tested)
✅ **"A mass-varying axion with ε = 0.0251 [FITTED to JWST stellar-mass function] would reduce early-universe growth barriers by ΔV/V ≈ 19% [VERIFIED calculation]"**

❌ **"The theory predicts PTA monochromatic lines"** (prediction without falsification criterion)
✅ **"The theory predicts PTA lines at T ≈ 7.52 d [PREDICTED]; absence of excess power at >3σ after foreground subtraction falsifies this channel [FALSIFICATION CRITERION]"**

## Manuscript Integration

1. **Abstract/Introduction:** Lead with [VERIFIED] results; place [PREDICTED] results in forward-looking context
2. **Methods:** Clearly label each [FITTED] parameter with loss function and data range
3. **Results:** Use labels consistently throughout; repeat them in figure captions
4. **Discussion:** Explicitly separate "what we know" (VERIFIED), "what we've calibrated" (FITTED), and "what testable consequences follow" (PREDICTED)
5. **Caveats:** For each [FITTED] parameter, state: "This parameter is phenomenological; its value depends on the observed dataset X. Future measurements of Y could change this fit."

## For Code and Configuration

Every numerical constant in the codebase must have a comment indicating its classification:

```python
# [FITTED] λ = 1.6724 from DESI 2024 BAO fit (χ²_min at this value)
lambda_fit = 1.6724

# [VERIFIED] mass ratio √(1014/336) from exact rational arithmetic (Agora.GaugeCoupling)
mass_ratio_lower = 1.73
mass_ratio_upper = 1.75

# [PREDICTED] Expected S₈ gradient at Euclid precision based on thawing quintessence trajectory
predicted_dS8_per_dz = -0.015  # per unit redshift
```

## When Uncertainty Grows

If a [FITTED] parameter's best fit moves as new data arrives, **document this explicitly:**
- Old fit (Dataset X): λ = 1.67, χ² = 2.33
- New fit (Dataset X + Dataset Y): λ = 1.62, χ² = 1.89
- **Interpretation:** The addition of Y data shifts the preferred region; refit should be re-published

## Output Template

After auditing a claim, produce a short report:

```
CLAIM: "The model satisfies the Swampland bound."
ORIGINAL LABEL: [ambiguous]
AUDIT RESULT: 
  ✓ Reformulated as: "The fit value λ=1.6724 [FITTED] exceeds √2 [VERIFIED], producing 
    an attractor w≈-0.07 [VERIFIED] incompatible with dark energy, quantifying the 
    Agrawal–Obied–Steinhardt–Vafa quintessence-Swampland tension."
  ✓ Added falsification criterion: DESI/future BAO data tightening bounds on w₀, wₐ
  ✓ Caveats added: Single-exponential potential; multi-field/plateau scenarios may resolve this.
```
