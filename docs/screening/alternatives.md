# GAP-4: Physical Screening Alternatives Memo (Task T3.3)

**Status: `[TIER: SONNET+ DRAFT]` — HUMAN SIGN-OFF REQUIRED.** This memo is a literature-grounded
draft only. No manuscript, CAVEATS.md, or PARAMETER_LEDGER.yaml language should change on the
basis of this document alone (per `scientificplan.md` T3.3's acceptance criterion).

## What actually needs screening, after T3.2

Task T3.2 (`docs/superradiance/s21_bare_survival.md`) found $S_{2,1}$ survives M87*-type
superradiance spin-down at its **bare** coupling ($\alpha=0.089$) with no screening at all.
GAP-4 therefore now applies **only to $S_{1,2}$**, whose bare coupling ($\alpha=0.155$) does
*not* survive unscreened (instability timescale $\approx4.6$ Myr vs. Salpeter's $\approx50$ Myr).
`PARAMETER_LEDGER.yaml` records the boost this vacuum needs: `alpha_bare_S12=0.155` →
`alpha_eff_S12=1.55` — a factor of **exactly 10** (the same ×10 factor is also recorded for
$S_{2,1}$, `alpha_bare_S21=0.089`→`alpha_eff_S21=0.89`, even though T3.2 shows $S_{2,1}$ no
longer needs it — the ×10 target predates T3.2 and has not been revisited since).

## The currently-implemented mechanism, and a provenance problem

`scripts/superradiance_growth_rate.py:71` hardcodes:

```python
gamma_chameln = 0.25  # power-law index from MCMC  (free param)
```

This is a **bare literal**, not a value actually read from any MCMC output file for this
scenario. `scripts/candelas_chameleon_solver.py` does run a real MCMC, but fits $(\rho_{\rm
crit},\gamma)$ against **Milky Way / IC 2574 galactic rotation curve targets** (`m0=1.71\times
10^{-23}$ eV — an $S_{20}$-era mass, not $S_{1,2}$'s $3.18\times10^{-21}$ eV), an entirely
different physical scenario from M87*-horizon superradiance survival. **No MCMC run in this
repository actually fits $\gamma$ against the $S_{1,2}$/M87* target this comment claims to
justify.** This is flagged here as a second, independent provenance gap (of the same kind T2.2
found for the $\tau$ values) — not fixed in this memo, since fixing it requires re-running an
MCMC against the corrected T3.2 scope, which is future work, not drafted here.

## Comparison of three physical mechanisms

### 1. Chameleon, physical branch ($n>0$)

Standard Khoury–Weltman (2004) chameleon: $V(\phi)=\Lambda^{4+n}\phi^{-n}$, linearly coupled to
matter density via $\beta\rho\phi/M_{\rm Pl}$. Minimizing $V_{\rm eff}=V(\phi)+\beta\rho\phi/M_{\rm
Pl}$ gives $\phi_{\rm min}\propto\rho^{-1/(n+1)}$, and the effective mass at the minimum,

$$m_{\rm eff}^2 = V''_{\rm eff}(\phi_{\rm min}) \propto \phi_{\rm min}^{-(n+2)} \propto \rho^{(n+2)/(n+1)}
\quad\Longrightarrow\quad m_{\rm eff}\propto\rho^{\gamma},\ \ \gamma=\frac{n+2}{2(n+1)}.$$

**Correction to `CAVEATS.md §3`:** that section currently prints $\gamma=n/(n+2)$, which is
*inconsistent with its own stated conclusion* — solving $\gamma=n/(n+2)=0.25$ gives $n=2/3$
(physical!), not $n=-3$. Only the correct relation above, $\gamma=(n+2)/(2(n+1))$, reproduces
$n=-3$ from $\gamma=0.25$ ($n+2=0.5(n+1)\Rightarrow n=-3$). The numeric conclusion in
`CAVEATS.md` ("$n=-3$, unphysical") is right; the printed formula used to justify it is a typo.
This should be corrected independent of any other decision in this memo.

**Range for physical $n>0$:** $\gamma$ is strictly decreasing in $n$ (checked: $d\gamma/dn=
-2/(2n+2)^2<0$), running from $\gamma\to1$ as $n\to0^+$ down to $\gamma\to1/2$ as $n\to\infty$.
**$\gamma=0.25$ is outside this range for every physical $n$ — this branch is structurally
excluded, not merely disfavoured**, confirming and sharpening the existing CAVEATS.md verdict.

**Falsifiable lab consequence:** chameleon models with order-unity matter coupling $\beta$ are
tightly constrained by Eöt-Wash torsion-balance tests (Kapner et al. 2007, PRL 98, 021101;
Upadhye 2012, PRD 86, 102003, gives explicit chameleon exclusion contours in $(\beta,n)$ space).
A concrete, testable prediction of this branch (were it viable) would be an $n$-dependent
Eöt-Wash exclusion region; moot here since no physical $n$ reaches $\gamma=0.25$.

### 2. Symmetron

Hinterbichler & Khoury (2010, PRL 104, 231301): $V(\phi)=-\tfrac12\mu^2\phi^2+\tfrac14\lambda\phi^4$,
coupling $A(\phi)\rho\approx(1+\phi^2/2M^2)\rho$. Below a critical density
$\rho_{\rm SSB}=\mu^2M^2$ the $\mathbb Z_2$ symmetry is spontaneously broken and $\phi$ acquires a
nonzero VEV (unscreened, long-range fifth force); above $\rho_{\rm SSB}$ the symmetric phase is
restored, $\phi_{\rm min}=0$, and

$$m_{\rm eff}^2(\rho) = \frac{\rho}{M^2}-\mu^2 \;\xrightarrow{\rho\gg\rho_{\rm SSB}}\; \frac{\rho}{M^2}
\quad\Longrightarrow\quad m_{\rm eff}\propto\rho^{1/2}\quad(\gamma=1/2\ \text{exactly}).$$

This is a **sharp, parameter-independent prediction** in the deep-screened phase (unlike the
chameleon, $\gamma$ is not tunable here — it is fixed by the quartic potential's structure).
**$\gamma=1/2$ also cannot reach 0.25** — it sits exactly at the chameleon's own asymptotic floor.

**Falsifiable lab consequence:** symmetron force experiments (Burrage & Sakstein 2018, Living
Rev. Relativity 21:1, §5, review the constraints) probe $M$ and $\mu$ directly via the
screening/unscreening transition itself — a qualitatively distinct signature (a density
*threshold*, not a smooth power law) that Eöt-Wash-style experiments can in principle
distinguish from chameleon screening.

### 3. Native $T^2$-modulus coupling (no new field)

The model already has a modulus, the $T^2$ volume $\mathcal V_{T^2}$, coupled to the axion mass
via $m_a\propto\mathcal V_{T^2}^{-1/2}$ (the same volume-suppression structure used throughout
this repository's mass formulas). **If** $\mathcal V_{T^2}$ itself responds to the local
matter/curvature density — e.g. $\mathcal V_{T^2}(\rho)\propto\rho^{-p}$ for some $p$ set by the
radion's own coupling to the stress-energy tensor — this would give
$m_a(\rho)\propto\rho^{p/2}$, i.e. $\gamma_{\rm native}=p/2$, achievable at $\gamma=0.25$ for
$p=0.5$ with **no new field content** beyond what the model already has.

**This is not derived anywhere in this repository.** $p$ is set by the radion-matter coupling in
the moduli-stabilisation potential — exactly the mechanism OPEN_PROBLEMS.md item 4 (moduli
stabilisation) already flags as open, and `scripts/alpha_topology.py`'s own verdict
("topologically unconstrained... depends on free integer fluxes/charges") applies here with equal
force. **This branch is not excluded by any known physics constraint, but it is also not derived
— any specific $\gamma_{\rm native}$ (including 0.25) would currently have to be *assumed*, not
computed**, which reproduces exactly the free-parameter problem GAP-4 was trying to escape.

**Falsifiable lab consequence:** none identifiable without first deriving $p$ — a radion with a
density-dependent VEV would generically also produce a fifth force and (if $\mathcal V_{T^2}$
couples to Standard Model gauge kinetic terms, as volume moduli generically do) a
density-dependent variation of gauge couplings, in principle constrained by atomic-clock/quasar
fine-structure-constant drift bounds — but quantifying this requires the same undelivered $p$.

## Ranked recommendation (draft — human sign-off required)

1. **Re-derive the *needed* $\gamma$ for the corrected, $S_{1,2}$-only target before ranking
   mechanisms further.** A boost of exactly ×10 in $\alpha$ (0.155→1.55) can be supplied by
   $(1+\rho/\rho_{\rm crit})^\gamma=10$. At $\gamma=1/2$ (the physical floor shared by both
   standard mechanisms above) this needs only $\rho/\rho_{\rm crit}\approx100$ — a modest,
   plausible density contrast between the M87* horizon environment and the reference density.
   **The currently-hardcoded $\gamma=0.25$ appears unnecessary**: nothing in the repository
   demonstrates that $\gamma=1/2$ with a modest density ratio fails to supply the same ×10 boost.
   This is a testable, constructive alternative to fabricating a new mechanism.
2. **If confirmed, prefer the symmetron ($\gamma=1/2$ exactly, parameter-independent, distinct
   falsifiable lab signature)** over a native-$T^2$ mechanism that currently has no derived
   exponent at all, and over the chameleon (whose $n>0$ branch tops out at the same $\gamma=1/2$
   floor with less predictive sharpness, since $\gamma$ is tunable via $n$ rather than fixed).
3. **Do not adopt the native $T^2$-coupling mechanism as a manuscript claim** until $p$ is
   derived from an actual moduli-stabilisation potential (OPEN_PROBLEMS.md item 4) — using it
   now would only relabel the free-parameter problem, not solve it.
4. **Independent of the above, fix `CAVEATS.md §3`'s printed chameleon formula** ($\gamma=n/(n+2)
   \to\gamma=(n+2)/(2(n+1))$) — a typo, not a physics decision, safe to correct without human
   sign-off.

**What this memo does NOT do:** rerun the MCMC against the corrected T3.2-only target, or verify
that $\gamma=1/2$ actually reproduces the ×10 boost end-to-end through the exact Dolan-solver
survival calculation (only the schematic $(1+\rho/\rho_{\rm crit})^\gamma$ scaling relation is
checked above). Both are natural follow-on `[TIER: SONNET+]` tasks, not attempted here to avoid
overstating what has actually been computed (Rule 1).
