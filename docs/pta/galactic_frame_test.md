# T6.2 — Galactic-Frame Discriminant Specification

**Status:** `[TIER: HAIKU]`, documentation of already-stated intent
(`K3_DarkMatter_Preprint.tex` §Systematics and Proposed PTA Searches, Item 1;
`PREDICTIONS.md` Prediction 4a), made precise enough for an external PTA
collaborator to implement without contacting the authors. This is a **test
specification**, not an executed analysis — no PTA data is fit here.

## 1. The problem this test solves

The predicted signal periods, $T\approx7.52$ d ($S_{1,2}$) and $T\approx13.08$
d ($S_{2,1}$), sit uncomfortably close to common terrestrial/instrumental
cadences (routine observatory maintenance windows, lunar-month subharmonics
$\approx29.5/2=14.75$ d, etc.). A bare periodogram peak at either period is
therefore not, by itself, strong evidence for the model: an unrelated
systematic locked to Earth–Sun–Moon geometry could produce a similar peak.
This document specifies a **phase-based** test that distinguishes the two
origins using physics the systematic does not share.

## 2. Signal model (galactic-frame hypothesis, $H_1$)

Following the standard ultralight-scalar-DM PTA formalism (Khmelnitsky &
Rubakov 2014, JCAP 1402, 019), a coherently oscillating background scalar
field sources an oscillating term in the pulsar timing residual via its
contribution to the local gravitational potential (Earth term):

$$\delta t(t) = A \cos\!\big(\omega_a(t)\, t + \phi_0\big), \qquad \omega_a(t) = \frac{m_a c^2}{\hbar}\Big[1 + \frac{\vec v_\oplus(t)\cdot\hat v_{\rm DM}}{c}\Big]$$

The bracketed term is the special-relativistic Doppler correction from
Earth's velocity relative to the frame in which the DM field's phase is
comoving — to excellent approximation the **galactic rest frame** (halo DM
velocity dispersion $\sim200$ km/s $\ll c$, so higher-order corrections are
$O(v^2/c^2)\sim10^{-6}$ and neglected here).

$\vec v_\oplus(t) = \vec v_{\rm LSR} + \vec v_{\odot,\rm pec} + \vec v_{\rm orbit}(t)$
has **three** pieces:
- $\vec v_{\rm LSR}$: Local Standard of Rest circular velocity, $\approx220$–235 km/s, fixed direction (galactic rotation).
- $\vec v_{\odot,\rm pec}$: Solar peculiar motion relative to the LSR, $\approx(11.1, 12.2, 7.3)$ km/s in $(U,V,W)$ galactic Cartesian coordinates (Schönrich, Binney & Dehnen 2010, MNRAS 403, 1829) — fixed direction, the "solar apex."
- $\vec v_{\rm orbit}(t)$: Earth's orbital velocity around the Sun, $\approx29.8$ km/s, **time-dependent with a known, exact 1-year period and phase** (perihelion $\approx$ Jan 3; direction from standard JPL ephemerides, e.g. `astropy.coordinates.get_body_barycentric_posvel`).

Only $\vec v_{\rm orbit}(t)$ varies on observationally useful timescales. Its
projection onto the *fixed* direction $\hat v_{\rm DM}$ (solar apex direction,
$\approx(\alpha,\delta)\approx(18^{\rm h}04^{\rm m}, +30^\circ)$ J2000,
consistent with $\vec v_{\rm LSR}+\vec v_{\odot,\rm pec}$ combined) produces an
**annual modulation of $\omega_a(t)$ with a fixed, parameter-free phase**:
the modulation peaks when Earth's orbital velocity vector aligns with
$\hat v_{\rm DM}$, at a calendar date fixed by the (known) solar apex
right ascension — **no free phase parameter**, unlike a generic annual
systematic.

## 3. Null model (terrestrial/instrumental hypothesis, $H_0$)

$$\delta t(t) = A \cos\!\Big(\frac{2\pi t}{T} + \phi_0\Big), \qquad T \in \{7.52\ \text{d},\, 13.08\ \text{d}\}\ \text{fixed}, \quad \phi_0\ \text{free}$$

A terrestrial systematic (maintenance cadence, tidal clock error, RFI
periodicity) has **no physical reason** to carry the specific,
Doppler-derived annual sideband structure of $H_1$ — its phase $\phi_0$ is
either constant or locked to a *different*, independently known ephemeris
angle (e.g. lunar phase, solar conjunction avoidance schedule), not to the
solar-apex-direction projection above.

## 4. The discriminating observable

Expand $\omega_a(t)\,t$ to first order in the small annual term
($|\vec v_\oplus\cdot\hat v_{\rm DM}|/c\sim10^{-3}$, justifying linearization
over any single PTA observing baseline):

$$\delta t(t) \approx A\cos(\omega_a^{(0)} t + \phi_0) - A\,\omega_a^{(0)} t \,\frac{\vec v_{\rm orbit}(t)\cdot\hat v_{\rm DM}}{c}\sin(\omega_a^{(0)} t+\phi_0)$$

The second term is a **slow (annual-period) amplitude/phase envelope** riding
on the fast ($T\approx7$–$13$ d) carrier — a specific, computable function of
time with **zero free parameters** beyond the carrier's own $(A,\phi_0)$,
since $\vec v_{\rm orbit}(t)$ and $\hat v_{\rm DM}$ are both externally fixed.
This is the quantity to search for: a $\sim$year-period modulation of the
$7.52$-/$13.08$-day line's instantaneous phase, with a **predicted, not
fitted**, modulation phase set by the solar apex direction.

## 5. Likelihood-ratio test

For a PTA residual time series $\{r_i(t_j)\}$ (pulsar $i$, epoch $t_j$) with
known noise covariance $\Sigma_i$ (from standard PTA noise modelling —
white + red + DM-variation noise, already characterized by NANOGrav/EPTA
pipelines independent of this test):

$$\ln L(\theta \mid \{r_i\}) = -\frac12\sum_i \big(\vec r_i - \vec s_i(\theta)\big)^{\!\top}\Sigma_i^{-1}\big(\vec r_i - \vec s_i(\theta)\big) + \text{const.}$$

where $\vec s_i(\theta)$ is the predicted signal at pulsar $i$'s epochs under
either model. **Both $H_0$ and $H_1$ have exactly two free parameters**,
$\theta=(A,\phi_0)$ (common-mode across all pulsars — the Earth-term
advantage PTAs already exploit for stochastic GW backgrounds: this scalar
signal is correlated across the whole pulsar array, unlike per-pulsar red
noise). Because the models are **non-nested but parameter-count-matched**,
compare the maximized log-likelihoods directly:

$$\Delta\ln L \;=\; \ln L\big(H_1;\hat\theta_1\big) - \ln L\big(H_0;\hat\theta_0\big)$$

Since $H_0,H_1$ are not nested, Wilks' theorem does not apply; assess
significance by Monte Carlo: simulate many noise realizations under $H_0$
(using the PTA's own characterized noise model), refit both models to each,
and build the null distribution of $\Delta\ln L$. **Detection criterion:**
observed $\Delta\ln L$ exceeds the 99.7th percentile ($3\sigma$-equivalent)
of the $H_0$-simulated null distribution.

## 6. What would falsify vs. support the model

- **Line detected, $H_1$ preferred over $H_0$ at the stated significance**
  for the predicted period **and** the predicted solar-apex-locked annual
  modulation phase: strong support, independent of the GAP-2 ratio test
  (§`PREDICTIONS.md` 4b).
- **Line detected, but the annual modulation phase does not match the
  solar-apex prediction** (or is absent): evidence the line is a terrestrial
  systematic, not this model's signal — the corresponding vacuum's
  axion-mass prediction is not falsified by this alone (a real DM signal
  could simply be below the modulation's detectable amplitude at current
  sensitivity), but the periodogram detection itself should not be cited as
  supporting evidence.
- **No line at either period with adequate sensitivity:** falsifies the
  corresponding vacuum's mass prediction directly (Prediction 4a).

## 7. What this document does not do

It does not estimate the achievable $\Delta\ln L$ for any specific PTA
dataset (15-yr NANOGrav, SKA-era) — that requires injection-recovery
forecasting against real/synthetic residuals and noise models, which is
Task T6.1 (`docs/pta/forecast.md`, not yet executed — blocked in this
session on the `enterprise`/`enterprise_extensions` Python packages not
being installed in this environment). It also does not commit to a specific
numeric solar-apex right ascension/declination beyond citing Schönrich et
al. (2010); a PTA collaborator implementing this test should use their
pipeline's standard solar-system-barycenter ephemeris (already required for
ordinary PTA timing) rather than a hardcoded value here, to avoid a second,
independent source of ephemeris error.
