# ⚠️ Scientific Caveats & Known Limitations

> **Epistemic Stance**: This repository houses a *theoretical mathematical exploration*, not a claimed observational discovery. The results below are computational and conjectural. We explicitly document the known limitations to ensure intellectual honesty.
> 
> **Version**: Updated 2026-06-25 (Phase 12 Peer Review Remediation). Prior version contradicted the implementation state. See `LESSONS_LEARNT.md §26`.

---

## 1. Mass Calibration Is Parameterized, Not Uniquely Predicted (GAP-2)

The axion mass predictions ($m_a = 3.18 \times 10^{-21}$ eV for $S_{1,2}$ and $1.83 \times 10^{-21}$ eV for $S_{2,1}$) are derived using the Svrcek-Witten (2006) instanton formula:

$$m_a = \frac{M_{\text{Pl}}}{\sqrt{\mathcal{V}}} \sqrt{\sum_d d^2 \, q_d \, e^{-2\pi d\tau}}$$

However, **the Kähler modulus $\tau$ and volume $\mathcal{V}$ are not uniquely fixed by the K3 topology.** A full derivation would require a moduli stabilization mechanism (KKLT, Large Volume Scenario). Without this, the formula simply shows that FDM-range masses are *achievable* for $\mathcal{V} \sim 10^4$, $\tau \sim 30$–35 — it does not *predict* specific values.

**Status**: The mass predictions should be treated as *achievability demonstrations* within a two-parameter ($\tau$, $\mathcal{V}$) family. The parameter sweep in `scripts/mass_from_first_principles.py` shows the achievable contour.

> **2026-07-11 update (Task T2.2):** Full derivation memo `docs/derivations/stiffness_to_potential.md`. Two further findings, not previously documented:
> 1. The "stiffness" integers $V''(0)=1014/336$ (used in `GaugeCoupling.lean` and `PTAFrequencyRatio.lean` as *the* mass/coupling ratio) are computed with **no** $e^{-2\pi d\tau}$ instanton suppression, whereas the actual cited masses above are computed by `scripts/k3_sieve_analysis.py` **with** that suppression at $\tau\approx33.6$–$33.8$. At those $\tau$ values the sum is single-instanton ($d=1$) dominated to ~90 decimal places — since $q_1=1$ for both sequences, $d=2,3$ (i.e. 1014 vs. 336) are numerically irrelevant to the masses actually reported. The mass ratio $m_a(S_{1,2})/m_a(S_{2,1})=1.7378$ agrees with $\sqrt{1014/336}=1.7372$ to $\sim0.03\%$ for a reason unrelated to the stiffness integers: it follows almost entirely from the specific, hardcoded $(\tau_{12},\tau_{21})=(33.6255,33.8014)$ pair.
> 2. Those two $\tau$ values have **no derivation, citation, or documented fitting procedure** anywhere in `k3_sieve_analysis.py` or its history, and reproduce the pre-assumed target masses (3.18e-21, 1.83e-21 eV) to 3 significant figures — the exact practice `scripts/mass_from_first_principles.py`'s own header explicitly disavows as "logically circular" ("using them to back-calibrate (tau, V) and then claiming the model 'predicts' the masses is logically circular"). Whether `k3_sieve_analysis.py`'s $\tau$ values were obtained the same way is an **open provenance question**, not confirmed here.
>
> **Consequence:** the claim in `PTAFrequencyRatio.lean` that the PTA frequency-ratio test is "independent of every uncertain modelling choice upstream" is not established by this model's own numbers — see the memo for the full argument and the recommended (not yet applied) docstring downgrade.

---

## 2. K3 Surface Identification Is Conjectural (GAP-1)

> **🔴 2026-07-11 finding — S₂,₁ is CONFIRMED NOT a K3 surface.** Full write-up: `docs/gap1/ORDER_VERIFICATION_FINDINGS.md`. Summary: independently re-deriving the minimal Picard-Fuchs recurrence for $S_{2,1}(n)=\sum_k\binom{n}{k}^2\binom{n+k}{k}$ and validating against 149 held-out values (exact integer arithmetic) shows it satisfies a genuine **order-2** recurrence, not order-3 — the signature of an **elliptic curve period**, not a K3 surface. $S_{1,2}$ was checked against the same order-2 ansatz and has none — it remains genuinely order-3. The original "$S_{2,1}$: K3 Surface (Order-3)" classification traced to a bug in `scripts/k3_sieve_analysis.py::find_minimal_order` (conflated polynomial-coefficient degree with recurrence shift-order; no held-out validation). **This bug has been fixed and the full $A,B\in[1,5]$ sieve re-run in this session**: with the corrected classifier, only $(A,B)=(1,2)=S_{1,2}$ survives as K3; $(2,1)=S_{2,1}$ and $(2,2)$ both come back **Elliptic Curve (Order-2)**. This is a confirmed result, not a suspicion — **do not cite "$S_{2,1}$ is a K3 surface" going forward.** How to proceed (drop $S_{2,1}$, search for a genuine replacement, or keep it as a non-K3 "recurrence invariant") is a physics-judgement call, `[TIER: HUMAN]`, not resolved here.
>
> Separately, the monodromy computation in `scripts/k3_monodromy_verification.py` had its own bug: the Fuchs-criterion regularity classifier was missing the leading-coefficient's own vanishing-order offset, which systematically misclassified every tested singular point (including the presumed MUM point at z=0) as irregular. **This bug is now fixed (2026-07-11)** — see the findings doc for the concrete before/after check and the performance rewrite (factor-based exact divisibility, not per-root symbolic simplify) that made the corrected version actually finish. The fix changes the diagnosis, not the practical outcome: $z=0$ now correctly classifies as REGULAR for both sequences (as expected), but every *other* finite singular point of *both* extracted operators classifies as genuinely IRREGULAR — so **no numeric RK4 monodromy matrix has been computed for either sequence**, this time because the corrected classifier finds no regular point away from $z=0$ to integrate around, not because of the bug. Whether this reflects a non-minimal ("apparent singularity"-bearing) extracted recurrence or a genuine anomaly is unresolved and flagged as a new SONNET+ follow-up (Ore-algebra minimality check) — see `docs/gap1/ORDER_VERIFICATION_FINDINGS.md` "Step 1 completed" for the full argument, including why a shared pattern across both sequences (one K3, one elliptic) makes a pipeline artifact more likely than K3-specific evidence.

The classification of $S_{1,2}$ as a "K3 surface" is based on detecting an Order-3 Picard-Fuchs recurrence via exact nullspace extraction, now confirmed as the *only* survivor of the $A,B\in[1,5]$ sieve (see update above). $S_{2,1}$ is no longer classified as K3.

- The mapping **"Order-3 Picard-Fuchs ↔ K3 Surface"** relies on the Stienstra-Beukers correspondence, which is **not formally verified in Lean 4** and requires additional checks (monodromy computation, modularity of Fourier coefficients).
- The monodromy matrix computation in `scripts/k3_monodromy_verification.py` extracts the **PF ODE singular points**, but (per the 2026-07-11 update above) the regularity classifier itself is buggy, so no genuine numeric monodromy has yet been computed even for the surviving $S_{1,2}$ candidate.
- The Weil bound check (`|a_p| ≤ 2p`, weight-3) is computed for both sequences over 44 primes (p∈[5,200]) and **passes for both** (`scripts/modularity_screen.py`, `docs/modularity_report.md`) — a necessary but not sufficient condition. **Correction (2026-07-11, self-audit):** an earlier draft of this note claimed the weight-2 bound $|a_p|\le2\sqrt p$ "fails at 6/23 checked primes" for $S_{2,1}$ — that figure was never actually computed by any script and did not match the data on disk. The weight-2 check has now been added to `scripts/modularity_screen.py` and run for real: it fails at **11/44** primes for $S_{2,1}$ (p = 29, 41, 53, 61, 73, 97, 109, 113, 137, 149, 181) and, notably, **also fails at 9/44** primes for $S_{1,2}$ (p = 43, 59, 89, 107, 131, 137, 139, 179, 193) — the sequence independently confirmed to be genuinely order-3/K3. Because both sequences fail the weight-2 bound at broadly similar rates, **this check does not actually discriminate between the two sequences** and should not be cited as evidence for the order-2 reclassification; the order-2 finding rests entirely on the held-out recurrence-order re-derivation in `docs/gap1/ORDER_VERIFICATION_FINDINGS.md`, not on this Weil-bound comparison.
- The mirror-map integrality check (`scripts/mirror_map_integrality.py`, task T1.3) passes for both sequences: all 30 checked coefficients of $q(z)/z$ are exact integers for both $S_{1,2}$ and $S_{2,1}$ (`data/mirror_map/S12_qcoeffs.json`, `S21_qcoeffs.json`). Integrality is a necessary condition for many arithmetic period sequences (not exclusively K3), so this pass does not contradict $S_{2,1}$'s reclassification as elliptic.

**2026-07-14 Phase 3 resolution:** $S_{2,₁}$ is kept in the model as a **non-K3 recurrence-invariant** with identical topological stiffness to $S_{1,2}$. The mass-ratio prediction $\sqrt{1014/336}$ remains arithmetically valid; its interpretation shifts from "two K3 surfaces" to "two objects with shared stiffness topology, one confirmed K3, one elliptic." See OPEN_PROBLEMS.md "GAP-1 RESOLUTION (2026-07-14)" for rationale and manuscript updates.

**Status**: $S_{1,2}$ remains a **computationally supported conjecture** (order-3 confirmed as the unique K3 survivor of the corrected sieve, Weil bound + integrality both pass, no strong modularity match yet found; monodromy computation still pending due to the separate classifier bug). $S_{2,₁}$ is **confirmed non-K3** (elliptic, order-2) and **reframed as recurrence-invariant** — see `docs/gap1/ORDER_VERIFICATION_FINDINGS.md` for technical details and OPEN_PROBLEMS.md for the Phase 3 resolution.

---

## 3. Chameleon Mechanism Parameters Are Free (GAP-4)

The Chameleon mass scaling:

$$m_{\text{eff}}(\rho) = m_a \left(1 + \frac{\rho}{\rho_{\text{crit}}}\right)^{\gamma}$$

uses $\gamma$ and $\rho/\rho_{\text{crit}}$ as **free phenomenological parameters fitted via MCMC** (see `scripts/candelas_chameleon_solver.py`). In standard Khoury-Weltman chameleon field theory, the exponent is $\gamma = \frac{n+2}{2(n+1)}$ for an inverse power-law $V(\phi) \propto \phi^{-n}$ (corrected 2026-07-11, Task T3.3 — the previous printed formula $\gamma=n/(n+2)$ was a typo inconsistent with this section's own numeric conclusion; only the corrected formula reproduces it). The value $\gamma = 0.25$ would require $n = -3$, which is unphysical; moreover $\gamma$ is strictly decreasing in $n$ and bounded to $(1/2, 1)$ for every physical $n>0$, so **no** physical chameleon $n$ reaches $\gamma=0.25$ — see `docs/screening/alternatives.md` (T3.3) for the full comparison against symmetron and native-modulus alternatives, including a constructive suggestion that $\gamma=1/2$ (physically attainable) may suffice via a modest density-ratio boost, obviating the need for $\gamma=0.25$ at all.

**Status**: The superradiance evasion relies on a density-dependent mechanism with **tunable parameters not derived from the K3 compactification geometry**. The MCMC posterior on $\gamma$ is the honest representation of our knowledge.

> **2026-07-11 update (Task T3.2):** the unphysical-$n=-3$ problem is now moot **for $S_{2,1}$ specifically** — see §4 below. $S_{2,1}$'s bare coupling survives M87*-type spin-down without any Chameleon screening at all, so this GAP-4 caveat now applies only if $S_{1,2}$'s bare coupling is the one that needs to be screened (its bare $\alpha=0.155$ does NOT survive unscreened at M87*, per §4).

---

## 4. Superradiance Growth Rate (GAP-3) (Updated 2026-07-11, Task T3.1/T3.2)

**The small-$\alpha$ approximation has been replaced with an exact method, validated against real published data.** `scripts/dolan_continued_fraction.py` implements Dolan's (2007) Leaver-type continued-fraction solver for the exact complex bound-state frequency $\omega$ of the $l=m=1$ mode on Kerr, valid at any coupling (not just $\alpha\ll1$). It is validated against all 6 published maximum-growth-rate points in Dolan (2007) Table I (transcribed via `pdftotext` from the arXiv PDF, not typed from memory) to **<0.4% error**, comfortably inside the 5% tolerance required by task T3.1 — see `docs/superradiance/dolan_validation.md`.

The previous small-$\alpha$ (Detweiler 1980) formula, $\Gamma_{211}\approx\frac{1}{24}a_*\alpha^8\mu_{\text{eff}}$, remains in `scripts/superradiance_growth_rate.py` for the low-$\alpha$ regime where it is accurate and cheap, but is **no longer used for the physically relevant bare/effective couplings** ($\alpha=0.089$–$1.55$), which are now evaluated exactly.

**Task T3.2 result (`scripts/s21_bare_analysis.py`, `docs/superradiance/s21_bare_survival.md`):** evaluating the exact growth rate at M87* (EHT 2019 mass $6.5\times10^9\,M_\odot$; spin $a_*=0.90$ is an illustrative literature value, **not** an EHT measurement):
- **$S_{2,1}$ bare** ($\alpha=0.089$): $\tau_{\text{instability}}\approx 380$ Myr, **longer** than the Salpeter accretion-spinup time ($\approx50$ Myr, Salpeter 1964) by a factor $\approx7.6$ → **SURVIVES without any Chameleon screening.**
- **$S_{1,2}$ bare** ($\alpha=0.155$): $\tau_{\text{instability}}\approx4.6$ Myr, **shorter** than the Salpeter time by a factor $\approx11$ → **does NOT survive unscreened**; still needs Chameleon (or an alternative) screening, i.e. GAP-4 remains open for $S_{1,2}$.
- 5 additional real high-spin SMBHs (Reynolds 2013 X-ray reflection sample: NGC 4051, IRAS 13224-3809, MCG-6-30-15, 1H0707-495, Ark 564) are all $\approx$1000–6000$\times$ less massive than M87*, giving bare $\alpha\sim10^{-5}$–$10^{-4}$ for both sequences — both sequences are essentially perfectly stable there (cross-checked against the small-$\alpha$ Detweiler formula, which gives $\tau_{\text{instability}}\sim10^{33}$–$10^{38}$ yr, vastly longer than the age of the universe).

**Correction relative to an earlier draft narrative:** a previously-circulated description of this result quoted $\tau_{\text{instability}}\approx86.6$ Myr for $S_{2,1}$/M87* — that number was never produced by any script in this repository. The actual computed value (above) is $\approx380$ Myr. The qualitative conclusion ($S_{2,1}$ survives unscreened) is unchanged, but the number itself should be cited from `docs/superradiance/s21_bare_survival.md`, not from memory.

**Remaining caveats:** (1) the survival argument compares instantaneous instability/accretion timescales, not a full GRMHD spin-evolution history; (2) M87*'s spin is not directly measured; (3) the angular eigenvalue $\Lambda_{lm}$ uses $\mathrm{Re}(\omega)$ only (an excellent approximation given $\mathrm{Im}(\omega)/\mathrm{Re}(\omega)\sim10^{-7}$–$10^{-9}$ here, but not exact).

---

## 5. Cosmology Pipeline Is Pre-Boltzmann (GAP-5) (Updated 2026-07-11, Task T5.1/T5.2)

**Note on numbering:** an earlier version of this document also used the "(GAP-5)" tag for a
*different* topic (dataset provenance); that content has been retitled "Datasets: Partially
Archival, Partially Simplified" below (no GAP tag) to avoid collision with `scientificplan.md`'s
canonical GAP-5 ("cosmology pipeline is pre-Boltzmann"), which is what this section now covers.

The original "H₀ ~ 72" claim (`PARAMETER_LEDGER.yaml`: ε=0.02511 → H₀=71.92 km/s/Mpc) was
computed by a **background-only integration** (`LL.md:94`) with **rest initial conditions**
(field at potential minimum) and an ε value described in `scientificplan.md` itself as
"reverse-engineered" (tuned to hit a target H₀, not independently fit). Two of the three fixes
scientificplan.md's WS5 calls for have now been attempted:

- **T5.1 (tracker ICs):** `empirical_crucible/tracker_ics.py` replaces rest ICs with the
  Copeland-Liddle-Wands (1998) attractor solution. Result: for this potential (V(φ)∝φ², n=2),
  the tracker and rest ICs converge to nearly the same late-time w (Δw₀≈0.0002) — a genuine,
  if modest, finding. See `docs/cosmology/ic_sensitivity.md`.

- **T5.2 (Boltzmann-grade check):** `empirical_crucible/class_fork_validation.py` uses real
  CLASS (`classy`) as ground truth. Two real findings:
  1. **Architectural blocker (confirmed live, not asserted):** the model's own formula,
     $\rho_{DM}(a)\propto a^{-3-\epsilon}$, implies $w_{DM}=\epsilon/3\approx+0.0084$ (positive).
     CLASS's public dark-energy fluid API (`Omega_fld`/`w0_fld`/`cs2_fld`) **hard-rejects any
     fluid with $w(a\to0)\ge0$** — confirmed by an actual `classy` call raising
     `CosmoComputationError`, not asserted from documentation. A literal implementation of this
     model in CLASS requires patching the C source (`background.c`, `perturbations.c`) and
     recompiling — a genuine fork, not a parameter choice — and is **not attempted** here: unlike
     the GAP-3 Dolan solver (validated against 6 independent published points), a hand-written
     perturbation-equation patch would have no independent benchmark to validate against.
  2. **Self-consistent background recomputation finds a materially different H₀.** A custom
     sound-horizon/comoving-distance integrator (validated to <0.002% against CLASS's own
     `rs_rec`/`ra_rec`/`100*theta_s` at ε=0) applied the SAME ε-modified $H(a)$ consistently to
     both integrals and solved for the $H_0$ that preserves the CMB acoustic scale. Result:
     **$H_0\approx75.8$ km/s/Mpc**, not 71.92. This is a real discrepancy (~+3.9 km/s/Mpc) and
     notably **overshoots** the SH0ES local value (~73) rather than bridging Planck and SH0ES as
     intended. Neither this self-consistent calculation nor a diagnosed "inconsistent shortcut"
     variant (H₀≈60.95) reproduces the ledger's 71.92; the exact original method is not fully
     reproducible from what's documented in the repository (`LL.md:94` gives the result but not
     the full derivation). Per Rule 1, this is reported rather than silently reconciled.
  3. A supplementary "effective-ΛCDM" proxy (matching only $r_s,D_M$, run through real CLASS to
     get an actual $C_\ell^{TT}$) requires boosting $\omega_{cdm}$ by 22% above the true model's
     own value to match — demonstrating that this shortcut conflates a redshift-*scaling* change
     with a density-*normalization* change and should **not** be read as a genuine peak-height
     prediction. Its 17% max $C_\ell^{TT}$ deviation is reported only as an illustration of why
     the shortcut is untrustworthy, not as the model's real Boltzmann-level prediction.

Full details: `docs/cosmology/class_fork_validation.md`, `docs/cosmology/ic_sensitivity.md`.

**T5.3 (Cosmic See-Saw, VISION.md §4A):** `empirical_crucible/joint_epsilon_likelihood.py`
executes the **S₈ side** quantitatively (two independent, real calculations against this
model's own axion masses and real CLASS $P(k)$; own $\sigma_8$ integral validated to
5 significant figures against `cosmo.sigma8()`):
1. The standard FDM quantum-pressure suppression mechanism (Hu, Barkana & Gruzinov 2000 —
   the mechanism VISION.md §4A itself invokes) gives **negligible suppression (<0.001%)** at
   this model's masses ($1.8$–$3.2\times10^{-21}$ eV) — they are $\sim20$–$30\times$ heavier
   than the FDM "sweet spot" ($\sim10^{-22}$ eV) where this effect matters at the $S_8$-relevant
   scale.
2. Treating ε as a $c_s^2=0$ background modification (T5.2's model) instead gives $D_\epsilon(a{=}1)/D_{\rm std}(a{=}1)=1.040$,
   i.e. a **+4% increase** in growth/$S_8$ — the **wrong sign** for helping the $S_8$ tension.

Both real, validated channels fail to reproduce the "lighter axion suppresses $S_8$" mechanism
the see-saw narrative requires. The **JWST side was not quantitatively executed** (would need
halo-mass-function modeling with no independent benchmark available — flagged rather than
fabricated, per the same reasoning as T5.2's un-attempted CLASS perturbation fork); a real,
independently-published qualitative check (Cox et al., arXiv:2307.10302: viable ALP window
$10^{-22}$–$10^{-19}$ eV via a *different* mechanism) shows both masses fall inside that broad
window, but this is not a fit of this model's own ε to JWST data. **Consequence: VISION.md
§4A's full ">3σ mutual exclusion" falsification test cannot be completed as specified — but the
S₈ side alone is a real, negative result reported per Rule 4.** Full details:
`docs/cosmology/joint_epsilon_likelihood.md`.

**Status:** GAP-5 remains open. T5.1 is complete; T5.2 replaced an unverifiable background
formula with a real-CLASS-validated one and surfaced a genuine, unfavorable discrepancy
(H₀≈75.8, not 71.92) rather than confirming the original claim; T5.3's S₈ side is complete and
also unfavorable (the see-saw suppression mechanism does not work at this model's own masses).
A true perturbation-level Boltzmann computation (T5.2's full scope) and a quantitative JWST
likelihood (T5.3's remaining scope) both require substantial further work — genuine CLASS
C-source fork and halo-mass-function modeling respectively, correctly flagged by
`scientificplan.md` as `[TIER: SONNET+]` and not completed in one session. T5.4 (DESI DR2
refit) remains to be executed.

> **2026-07-14 Phase 3 resolution:** Given the H₀ discrepancy (background-only 71.92 vs. 
> self-consistent 75.8 km/s/Mpc), manuscripts will **report both values** rather than 
> suppressing the discrepancy or attempting an expensive full CLASS C-source fork (estimated 
> 40+ hours + validation risk). Rationale and manuscript-update details in OPEN_PROBLEMS.md 
> "GAP-5 RESOLUTION (2026-07-14)".

---

## 5b. Datasets: Partially Archival, Partially Simplified (Updated Phase 12)

The CSV files in `scientific_protocol/datasets/` have been improved from fully synthetic placeholders:

- `SPARC_IC2574.csv`: **Real SPARC rotmod observational data** (Lelli et al. 2016). Full dataset with ~40 radial bins downloaded from astroweb.cwru.edu/SPARC/. Columns: `Radius_kpc, Vobs_km_s, errV_km_s, Vgas_km_s, Vdisk_km_s`. ✅
- `GD1_constraints.csv`: **Simplified from** Bonaca et al. 2019 Table 1. Not a direct machine-readable extraction; column definitions may differ from the published table. Use the primary paper for any quantitative analysis. ⚠️
- `M87_spin_bounds.csv`: **Archival spin bounds** from EHT 2019 and Cui et al. 2023. Note that EHT 2019 constrains mass, not spin directly; the spin value $a_* \approx 0.9$ is from the jet-precession analysis of Cui et al. 2023, which itself carries modeling uncertainties. ⚠️

**For quantitative scientific analysis**: Use the SPARC database directly (http://astroweb.cwru.edu/SPARC/), Bonaca et al. 2019 ApJ 880, 38, and EHT Collaboration 2019 ApJL 875, L1.

---

## 6. Lean 4 Proofs: What Is vs. What Is Not Formally Verified (GAP-6)

| Claim | Lean Status |
|:---|:---|
| Topological mass coefficient arithmetic | ✅ Kernel-verified (`rfl`, `norm_num`) |
| GD-1 No-Go for CY3 axions | ✅ Kernel-verified (exact ℚ arithmetic, `cy_axion_no_go`). Self-contained: confirmed 2026-07-12 this proof does NOT import or depend on the `axiom s20_recurrence`/`s20_recurrence_order_4` rows below — the general-$n$ axiom status has no bearing on this theorem's validity. |
| AEDE potential non-negativity | ✅ Kernel-verified (`cos_le_one`, `positivity`) |
| Chameleon $m_\text{eff}$ monotonicity | ✅ Kernel-verified (`rpow_lt_rpow`) |
| Axion mass positivity (Svrcek-Witten formula) | ✅ Kernel-verified (`MassFromInstanton.lean`) |
| S₁₂ sequence: 20 exact values + Weil bounds | ✅ Kernel-verified (`S12RecurrenceVerification.lean`) |
| Relative gauge-coupling ratio $\alpha^{-1}_{S_{1,2}}/\alpha^{-1}_{S_{2,1}}=\sqrt{1014/336}\in(1.73,1.75)$ | ✅ Kernel-verified (`GaugeCoupling.lean`, exact ℚ) |
| $S_{20}$ order-5 recurrence, concrete $n\le8$ | ✅ Kernel-verified (`S20Recurrence.lean`, `decide`) |
| $S_{20}$ order-4 minimal recurrence, concrete $n\le8$ | ✅ Kernel-verified (`S20Recurrence.lean`, `decide`) |
| $S_{20}$ order-4 minimal recurrence, general $n$ | ⚠️ Explicit `axiom`; numerically verified for all $n \in [0,60]$. **The "SymPy `diff=0`" symbolic WZ-certificate check cited in earlier drafts cannot currently be reproduced: `scripts/verify_wz_certificate.py` does not exist in this repository (2026-07-11 finding, attempted Task T4.1 — see `OPEN_PROBLEMS.md` item 3).** Treat that specific claim as unverified pending relocation or re-derivation of the certificate. **Confirmed non-blocking (2026-07-12):** this axiom is not used by `cy_axion_no_go` (row above) or anything else in this repository's kernel-verified results — closing it is a genuine, worthwhile, but non-urgent formal-verification goal. A same-day companion-repo attempt to discharge it via "Horner reduction" produced a vacuous `True` theorem, not a real proof — see `OPEN_PROBLEMS.md` item 3 for detail. Do not cite that attempt as closing this row. |
| $S_{20}$ order-5 recurrence, general $n$ | ⚠️ Explicit `axiom` (was `sorry`); exact-verified $n\in[0,60]$ |
| K3 surface identification for $S_{1,2}$, $S_{2,1}$ | ❌ Not formalized |
| Monodromy connection matrix computation | ❌ Not formalized |
| Mirror map coefficient extraction | ❌ Not formalized (hardcoded) |
| **Absolute** fine-structure constant $\alpha\approx1/137.036$ from geometry | ❌ Not attempted (open problem; requires bare GUT coupling, SUSY scale, threshold corrections, SM gauge embedding) |

---

## 7. Manuscript Citations (Updated Phase 12)

The preprint `manuscript/K3_DarkMatter_Preprint.tex` now has **25 BibTeX entries** and **15+ inline `\cite{}` commands**, covering:

- String axiverse and mass calibration: Svrcek & Witten (2006), Conlon & Quevedo (2006)
- Ultralight axion reviews: Hui et al. (2017), Marsh (2016)
- Superradiance: Detweiler (1980), Dolan (2007), Arvanitaki et al. (2010, 2017)
- Chameleon mechanism: Khoury & Weltman (2004a, 2004b)
- Observational constraints: Lelli et al. (2016), Bonaca et al. (2019), EHT (2019), Cui et al. (2023)
- Lyman-α: Iršič et al. (2017), Rogers & Peiris (2021)
- FDM structure formation: Schive et al. (2014)
- Mathematical foundations: Almkvist et al. (2011), Zagier (2009), Stienstra (1992)
- Formal verification: Moura & Ullrich (2021), Mathlib Community (2020)

**Remaining gap**: The PDF requires a full `pdflatex + bibtex + pdflatex + pdflatex` recompile cycle to resolve all citation cross-references in the output PDF.

---

*This document was last updated by the SocrateAI Adversarial Assessment protocol (Rule 4) on 2026-06-25 (Phase 12 Peer Review Remediation).*
