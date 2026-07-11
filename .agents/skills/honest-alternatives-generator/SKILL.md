---
name: honest-alternatives-generator
description: When a proposed claim, fit, or mechanism cannot be proven or contradicts data, generates a structured set of rigorous alternatives grounded in theory or observation, preventing the tendency to simply assert one story.
---

# Honest Alternatives: A Structured Approach to Uncertainty

Use this skill whenever:
- A [PREDICTED] claim is falsified by new data
- A [FITTED] parameter produces tension with another dataset
- An [AXIOM] cannot be discharged or fails empirical validation
- A proposed mechanism (e.g., chameleon screening) has theoretical gaps

## The Alternatives Framework

Instead of defending a single story, propose a **disjunctive research programme**: "Either A holds, or B holds, or C holds — and here is how to tell them apart."

### Form: The Three-Tier Alternative

For any falsified claim, propose three categories of alternative:

**Tier 1: Conservative Alternative**
- Minimal changes to the framework; mostly adjusting parameters or initial conditions
- Example: If λ-fit is too high for dark energy, reduce the field excursion (ϕ_0) or change initial condition

**Tier 2: Moderate Alternative**
- Changes core assumption within same theoretical framework
- Example: Instead of single-exponential potential, use multi-field or hilltop/plateau potential

**Tier 3: Radical Alternative**
- Replaces core assumptions; may require new physics
- Example: Dark energy is transient and embedding in early-universe cosmology; no current accelerating epoch

### Rigor Requirement

Each alternative must:
1. **Be internally consistent** (state the equations, no hand-waving)
2. **Have testable consequences** (what measurement falsifies this alternative?)
3. **Cite supporting precedent** (Has this been tried before? What were the results?)
4. **State explicit parameter values** or functional forms (not "some coupling")
5. **Include a cost/benefit analysis** (What does it explain? What new problems does it create?)

## Example: Swampland Tension Alternatives

**Observed tension:** λ_fit = 1.67 > √2, so single-exponential cannot produce sustained dark energy.

### Alternative 1: Conservative (parameter adjustment)
```
NAME:        Transient Dark Energy (no new physics)
CHANGE:      Initial field value ϕ₀ set to hilltop instead of tracking attractor
MECHANISM:   Potential V(ϕ) = Λ₄(1 - cos(ϕ/f))ⁿ with n ≥ 2; fine-tuned initial 
             condition places universe at potential maximum (ϕ₀ ≈ π), where slope ≪ H
PREDICTION:  w₀ ≈ −0.99 → −1.00 today, future evolution w(z) → −0.5 as field rolls
FALSIFY:     Spectral index running α_s from Planck or future CMB: if α_s differs by > 1σ
             from hilltop prediction, this alternative is ruled out
COST:        Requires artificial initial condition; not derived from theory
BENEFIT:     Avoids Swampland tension; single potential; phenomenologically similar to ΛCDM

REFERENCE:   Lindenmann & Barrow 2015 (hilltop inflation models); Planck 2018 CMB constraints
             on running spectral index rule out some hilltop scenarios
VERDICT:     [PLAUSIBLE] Not yet ruled out; awaits CMB-S4 precision
```

### Alternative 2: Moderate (mechanism change)
```
NAME:        Multi-Field Tracker (K3 axion + rolling modulus + third field)
CHANGE:      Add a second scalar field χ coupled to the K3 axion through cross term:
             V(ϕ,χ) = Λ₄[exp(λϕ) + β χ·exp(λϕ/2) + α χ²]
MECHANISM:   The coupling β allows χ to "steepen" the effective potential as ϕ rolls,
             converting w from −0.55 to −0.9 smoothly in late universe without
             requiring Λ (Steinhardt et al. 2003)
PREDICTION:  w₀ ≈ −0.98, w_a ≈ 0.1; w(z) shows smooth evolution, not abrupt
FALSIFY:     DESI BAO + Pantheon+ combined fit: does (w₀, w_a) prefer multi-field
             structure? If 1D exponential fit has χ² < multi-field by > 5 units, 
             single-field is favored
COST:        Adds 2–3 new parameters (β, α, coupling strength); requires explaining
             why χ is light and why coupling has this form
BENEFIT:     Swampland-compatible slope; can produce actual dark energy attractor

REFERENCE:   Steinhardt, Wang, Zlatev (PRL 1999); extends to mixed dark matter/energy
VERDICT:     [TESTABLE] Fits DESI; distinguishable from single-field in future surveys
```

### Alternative 3: Radical (new physics)
```
NAME:        Transient Dark Energy + Early-Universe Reheating
CHANGE:      Dark energy is a temporary phenomenon of the late universe (z < 3),
             caused by the decay of a long-lived field. Prior to z ~ 10, the universe
             was radiation-dominated or had a different dark-energy equation of state.
MECHANISM:   Quintessence field ϕ is extremely light (mass ~ 10⁻³² eV) for much of
             cosmic history; it only recently began rolling due to Hubble-parameter-dependent
             friction term in EOM: ϕ̈ + 3Hϕ̇ + V'(ϕ) = 0
             At z ~ 1000, H was large, friction dominated, ϕ ≈ const. As H → 0, ϕ rolls.
PREDICTION:  w(a) = constant for a ≪ a_eq, then decays. CMB would show no evidence of
             early-time acceleration. PTA would show no monochromatic lines (K3 axion
             not sourcing GWs in early universe, only late-time).
FALSIFY:     
             - CMB: If Planck temperature anisotropies deviate from standard ΛCDM/Λ physics,
               transient DE is ruled out
             - PTA: If detected lines at 7.52 d, 13.08 d exist and trace to z > 10 events,
               axion source was active early → rules out "late-time transient" picture
COST:        Requires explaining why acceleration happens *now* (coincidence problem
             in new guise); loses predictive power for early universe; many more parameters
BENEFIT:     Fully Swampland-compatible; no fine-tuning required; connects to multiverse
             / inflationary predictions

REFERENCE:   Quintessence reviews (Wetterich, Zlatev, Wetterich 1998–2002); early vs.
             late dark energy literature (Dvali et al. 2015 "Gravity Wave Cosmology")
VERDICT:     [SPECULATIVE] Consistent with current data; unique predictions (e.g., no early
             CMB anomalies from dark energy) can be tested by CMB-S4
```

## Algorithm: Generating Alternatives

**Step 1: Identify the Tension**
- What is the mismatch? (e.g., "λ = 1.67 > √2")
- What does it contradict? (e.g., "single-field dark energy attractor")
- What is the severity? (e.g., "2σ tension, not fatal but concerning")

**Step 2: Conservative Alternative**
- Change **parameters only**, keeping structure fixed
- Ask: "What initial condition or parameter choice makes this work?"
- Example: Instead of tracking attractor, start at hilltop

**Step 3: Moderate Alternative**
- Change **one structural assumption** (e.g., add field, change coupling)
- Ask: "What minimal new ingredient resolves the tension?"
- Example: Multi-field model, or different potential family

**Step 4: Radical Alternative**
- Change **foundational picture** (e.g., transient DE, modified gravity, extra dimensions)
- Ask: "If this framework is fundamentally wrong, what replaces it?"
- Example: Quintessence is rare event; dark energy is cosmological constant or gravitational modification

**Step 5: Falsification Gates**
- For each alternative, identify one measurement that would rule it in or out
- Prioritize by feasibility (5-year timeline preferred)
- Example: "DESI BAO precision ±0.02 on w₀ decides between alternatives 1 and 2"

## Writing the Alternatives Section

Manuscript template (e.g., Discussion or Appendix):

```latex
\section{Alternatives and Robustness}

The best-fit K3×T² model produces w₀ = −0.548, which sits outside 
the DESI 1σ contour for thawing dark energy. This section explores 
three classes of alternative scenario, each internally consistent 
and each testable by near-term observations.

\subsection{Conservative: Tuned Initial Conditions (Hilltop)}
[~200 words: equation, prediction, falsification criterion, reference]

\subsection{Moderate: Multi-Field Tracking}
[~200 words: mechanism, parameter count, DESI prediction, testability]

\subsection{Radical: Transient Dark Energy + Early Radiation}
[~300 words: conceptual shift, CMB/PTA predictions, role in cosmology]

\subsection{Discriminant Analysis}
\begin{table}
\begin{tabular}{|c|c|c|c|}
\hline
Alternative & w₀ Prediction & Testable by & Preferred if \\
\hline
Single-field (current) & −0.55 & DESI+Pantheon & χ²_red < 1.2 \\
Hilltop (Tier 1) & −0.99 & CMB running index α_s & α_s consistent with hilltop \\
Multi-field (Tier 2) & −0.98 & DESI w_a constraint & w_a < 0.05 preferred \\
Transient (Tier 3) & const. → decays & CMB/PTA line absence & No monochromatic PTA lines \\
\hline
\end{tabular}
\end{table}

The next generation of surveys (Euclid, CMB-S4, SKA) will decisively 
test these scenarios within 5 years.
```

## Common Pitfalls

### ❌ Pseudo-alternatives ("it could also be X")
```
WRONG: "Alternatively, the tension might be explained by modified gravity 
       or extra spatial dimensions or new particles or..."
```
Each unspecified "or" is not an alternative; it is an evasion.

### ✅ Real alternatives (concrete equations, predictions)
```
CORRECT: "Alternatively, the tension is resolved if the effective gravitational 
         constant evolves as G(a) = G₀[1 + α_G ln(a/a₀)] with α_G ≈ 0.02. 
         This produces w_eff ≈ −0.95 today while remaining causal (see Dvali et al. 2015). 
         Falsification: Gravitational-wave speed measured by LISA must equal c to 1 part in 10¹⁵."
```

### ❌ Alternatives that require the same unknown
```
WRONG: "Alternative 1: Axion mass is m_a. Alternative 2: Axion mass is 2m_a. 
       (Both recover dark energy.)"
```
Both require determining m_a; no new insight.

### ✅ Alternatives with independent unknowns
```
CORRECT: "Alternative 1: m_a is set by instanton action (current); Alternative 2: 
         m_a is set by coupling to D-branes (distinct mechanism, different predictions 
         for PTA signals). Falsification: If PTA detects lines, computes the implied 
         m_a, and it matches instanton prediction, Alternative 1 is supported."
```

## Output: Alternatives Audit Checklist

```
ALTERNATIVES AUDIT — Swampland Tension

Identified Tension:
  ✓ Clear statement: λ_fit = 1.67 > √2 falsifies single-exponential dark-energy attractor
  ✓ Severity: 2σ tension with observational constraints, physically meaningful

Conservative Alternative:
  ✓ Hilltop initial condition specified with potential form
  ✓ Prediction: w₀ ≈ −0.99 with w_a ≈ 0
  ✓ Falsification: CMB spectral index running excludes if α_s = 0 at > 2σ
  ✓ Reference cited (Lindenmann & Barrow 2015)
  ⚠ Cost/benefit not explicitly stated → ADD

Moderate Alternative:
  ✓ Multi-field mechanism specified (coupling term added)
  ✓ Equations written in full
  ✓ Falsification: DESI (w₀, w_a) covariance favors multi-field if χ² improves by > 5
  ✓ Reference cited (Steinhardt et al. 1999)
  ✓ Cost stated (2–3 new parameters)

Radical Alternative:
  ✓ Conceptually distinct (transient DE + early radiation)
  ✓ Predictions are unique (no early w-evolution, no early PTA signals)
  ✓ Falsification: Multiple gates (CMB anomaly absence, PTA line frequency)
  ✓ Reference cited (Dvali et al. 2015)
  ⚠ Coincidence-problem cost not addressed → ADD

Cross-Alternative Discrimination:
  ✓ Table provided showing w₀ predictions and discriminants
  ✓ Timeline given (Euclid, CMB-S4 within 5 years)
  ✓ No "pick your favorite" language; all treated as open questions

BLOCKING: None
RECOMMENDED: Explicit cost-benefit for Radical alternative; add one new testable 
              discriminant (e.g., galaxy-cluster mass function at z > 10)
```

## For This Project: The Swampland Tension Alternatives (Model Answer)

This project's strength is that it acknowledges the Swampland tension honestly and proposes alternatives. Ensure every future tension follows this pattern:

1. **State the tension clearly** (e.g., "λ_fit > √2")
2. **Propose Tier 1, 2, 3 alternatives** with concrete equations
3. **Provide falsification gates** for each (near-term, not decades away)
4. **Cite relevant literature** (show this is a known problem, not a surprise)
5. **Add to PREDICTIONS.md** if testable within 5 years
6. **Update VISION.md** with "Resolution Path" for each alternative
