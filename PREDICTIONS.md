# The Future Manifest: K3 × T² Falsifiable Predictions

A model is only as useful as its falsifiable predictions. Below we state the specific, testable signatures of the $K3\times T^2$ moduli-dynamics model for observatories operating 2025--2035, **together with the conditions under which each prediction would falsify the model**.

> **Honest framing.** These are *model-dependent forecasts*, contingent on the open theoretical problems listed in `OPEN_PROBLEMS.md` (no derived compactification, instanton action still phenomenological). The current best-fit trajectory already lies **outside** the DESI 2024 1$\sigma$ contour, so the model is in tension with present data; the forecasts below are the sharp targets by which it should be confirmed or ruled out, not claims of established fact.

## 1. Euclid's redshift-dependent $S_8$
**Prediction.** Euclid weak-lensing tomography should measure a *redshift-dependent* $S_8(z)$ rather than a single static value, evolving along the mass-varying-dark-matter decay curve set by $\epsilon\approx0.0251$ (the best-fit value from Part II). In this picture the early/late $S_8$ tension reflects physical smearing of the axion de Broglie scale, not measurement error.

**Falsification.** If Euclid finds an $S_8(z)$ consistent with a single, redshift-independent $\Lambda$CDM value across its tomographic bins (within errors), this prediction fails.

## 2. ELT Sandage--Loeb redshift drift
**Prediction.** Over a $\sim$decade baseline the Extremely Large Telescope (ELT) Sandage--Loeb test probes the expansion history directly. The model's best-fit thawing trajectory ($w_0\approx-0.55$, $w_a\approx-0.40$) predicts a redshift-drift signal measurably distinct from a cosmological constant ($w=-1$).

**Falsification.** A measured drift consistent with $w=-1$ (static $\Lambda$) at the achieved precision would exclude this trajectory. Note the model's best-fit is already in tension with DESI 2024, so this is a stringent test, not a safe bet.

## 3. LISA standard sirens (most speculative)
**Prediction (speculative).** If the $T^2$ volume modulus evolves cosmologically, gravitational-wave propagation over cosmological distances could acquire a small modification relative to General Relativity (a GW-vs-EM luminosity-distance offset for standard sirens detected by LISA).

**Caveat.** This is the **least developed** prediction: it requires a derived modified GW propagation equation for the specific $K3\times T^2$ geometry, which is *not yet computed* (see `OPEN_PROBLEMS.md`). The magnitude and even the sign of any effect are presently undetermined, so this should be read as a research direction, not a quantitative forecast.

## 4a. Dual PTA scalar-monopole lines
**Prediction.** Pulsar Timing Arrays (NANOGrav, EPTA, SKA) should detect two scalar-monopole signal lines at periods $T\approx7.52$ days ($S_{1,2}$) and $T\approx13.08$ days ($S_{2,1}$), per `K3_DarkMatter_Preprint.tex` §Observational Predictions and §Systematics and Proposed PTA Searches. Because these periods fall near common terrestrial/instrumental cadences, the key discriminant is galactic-frame phase coherence rather than raw periodogram detection (see `docs/pta/galactic_frame_test.md`, Task T6.2).

**Falsification.** Absence of both lines at the predicted periods (with adequate sensitivity and galactic-frame discrimination) after a full PTA observing campaign would falsify the corresponding vacuum's axion-mass prediction.

## 4b. The PTA ratio test (conditionally parameter-free — corrected 2026-07-11, Task T2.2)
**Prediction.** *If* the mass ratio $m(S_{1,2})/m(S_{2,1})$ equals the topological stiffness ratio $\sqrt{1014/336}$ exactly, the free Kähler modulus $\tau$ and volume $\mathcal{V}$ cancel and $f(S_{1,2})/f(S_{2,1}) = \sqrt{1014/336}$, kernel-verified (`lean4_formal_proofs/Agora/Phenomenology/PTAFrequencyRatio.lean`, theorem `pta_frequency_ratio_in_interval`) to lie in the exact-rational interval $(1.73, 1.75)$.

**Status of the antecedent (not previously stated here):** `docs/derivations/stiffness_to_potential.md` (Task T2.2) finds this equality is **not established** by the model's own current mass values. The masses actually cited elsewhere in this repository ($3.18\times10^{-21}$, $1.83\times10^{-21}$ eV) are computed WITH $e^{-2\pi d\tau}$ instanton suppression at hardcoded, undocumented $\tau$ values ($\tau_{S_{1,2}}=33.6255$, $\tau_{S_{2,1}}=33.8014$), under which the sum is single-instanton-dominated to ~90 decimal places — making 1014 vs. 336 numerically irrelevant to those masses. The observed $\approx0.03\%$ agreement between $\sqrt{1014/336}$ and the real mass ratio traces almost entirely to the specific, unexplained $\tau$ pair, not to the stiffness integers, and nothing currently derives that $\tau$ difference from geometry.

**The ratio test (falsification, revised scope).** A jointly detected frequency ratio outside $(1.73, 1.75)$ still falsifies the arithmetic-plus-antecedent package (both the kernel-verified interval AND the assumed mass-ratio equality). A ratio landing *inside* the interval, however, is **not** by itself confirmation that the test is parameter-free — that additionally requires the still-open moduli-stabilization derivation of $\tau$ (`OPEN_PROBLEMS.md` item 4). See Task T2.2/T2.3, `scientificplan.md` §WORKSTREAM 2.

---

*All forecasts above are conditional on resolving the open problems in `OPEN_PROBLEMS.md`. The model is presented as a falsifiable, string-inspired phenomenology, not an established description of nature.*
