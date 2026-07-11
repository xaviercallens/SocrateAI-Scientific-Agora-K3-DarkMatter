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

---

## 2. K3 Surface Identification Is Conjectural (GAP-1)

> **🔴 2026-07-11 finding — S₂,₁ is CONFIRMED NOT a K3 surface.** Full write-up: `docs/gap1/ORDER_VERIFICATION_FINDINGS.md`. Summary: independently re-deriving the minimal Picard-Fuchs recurrence for $S_{2,1}(n)=\sum_k\binom{n}{k}^2\binom{n+k}{k}$ and validating against 149 held-out values (exact integer arithmetic) shows it satisfies a genuine **order-2** recurrence, not order-3 — the signature of an **elliptic curve period**, not a K3 surface. $S_{1,2}$ was checked against the same order-2 ansatz and has none — it remains genuinely order-3. The original "$S_{2,1}$: K3 Surface (Order-3)" classification traced to a bug in `scripts/k3_sieve_analysis.py::find_minimal_order` (conflated polynomial-coefficient degree with recurrence shift-order; no held-out validation). **This bug has been fixed and the full $A,B\in[1,5]$ sieve re-run in this session**: with the corrected classifier, only $(A,B)=(1,2)=S_{1,2}$ survives as K3; $(2,1)=S_{2,1}$ and $(2,2)$ both come back **Elliptic Curve (Order-2)**. This is a confirmed result, not a suspicion — **do not cite "$S_{2,1}$ is a K3 surface" going forward.** How to proceed (drop $S_{2,1}$, search for a genuine replacement, or keep it as a non-K3 "recurrence invariant") is a physics-judgement call, `[TIER: HUMAN]`, not resolved here.
>
> Separately, the monodromy computation in `scripts/k3_monodromy_verification.py` has its own bug: the Fuchs-criterion regularity classifier is missing the leading-coefficient's own vanishing-order offset, which systematically misclassifies every tested singular point (including the presumed MUM point at z=0) as irregular. **No numeric monodromy matrix has ever actually been produced by this script to date** — every run to date has silently skipped the RK4 integration step. This bug is documented but NOT yet fixed (scoped as SONNET+ follow-up); see the findings doc for the concrete before/after check.

The classification of $S_{1,2}$ as a "K3 surface" is based on detecting an Order-3 Picard-Fuchs recurrence via exact nullspace extraction, now confirmed as the *only* survivor of the $A,B\in[1,5]$ sieve (see update above). $S_{2,1}$ is no longer classified as K3.

- The mapping **"Order-3 Picard-Fuchs ↔ K3 Surface"** relies on the Stienstra-Beukers correspondence, which is **not formally verified in Lean 4** and requires additional checks (monodromy computation, modularity of Fourier coefficients).
- The monodromy matrix computation in `scripts/k3_monodromy_verification.py` extracts the **PF ODE singular points**, but (per the 2026-07-11 update above) the regularity classifier itself is buggy, so no genuine numeric monodromy has yet been computed even for the surviving $S_{1,2}$ candidate.
- The Weil bound check (`|a_p| ≤ 2p`, weight-3) is computed for both sequences over 44 primes (p∈[5,200]) and **passes for both** (`scripts/modularity_screen.py`, `docs/modularity_report.md`) — a necessary but not sufficient condition. **Correction (2026-07-11, self-audit):** an earlier draft of this note claimed the weight-2 bound $|a_p|\le2\sqrt p$ "fails at 6/23 checked primes" for $S_{2,1}$ — that figure was never actually computed by any script and did not match the data on disk. The weight-2 check has now been added to `scripts/modularity_screen.py` and run for real: it fails at **11/44** primes for $S_{2,1}$ (p = 29, 41, 53, 61, 73, 97, 109, 113, 137, 149, 181) and, notably, **also fails at 9/44** primes for $S_{1,2}$ (p = 43, 59, 89, 107, 131, 137, 139, 179, 193) — the sequence independently confirmed to be genuinely order-3/K3. Because both sequences fail the weight-2 bound at broadly similar rates, **this check does not actually discriminate between the two sequences** and should not be cited as evidence for the order-2 reclassification; the order-2 finding rests entirely on the held-out recurrence-order re-derivation in `docs/gap1/ORDER_VERIFICATION_FINDINGS.md`, not on this Weil-bound comparison.
- The mirror-map integrality check (`scripts/mirror_map_integrality.py`, task T1.3) passes for both sequences: all 30 checked coefficients of $q(z)/z$ are exact integers for both $S_{1,2}$ and $S_{2,1}$ (`data/mirror_map/S12_qcoeffs.json`, `S21_qcoeffs.json`). Integrality is a necessary condition for many arithmetic period sequences (not exclusively K3), so this pass does not contradict $S_{2,1}$'s reclassification as elliptic.

**Status**: $S_{1,2}$ remains a **computationally supported conjecture** (order-3 confirmed as the unique K3 survivor of the corrected sieve, Weil bound + integrality both pass, no strong modularity match yet found; monodromy computation still pending due to the separate classifier bug). $S_{2,1}$ is **confirmed non-K3** (elliptic, order-2) — see `docs/gap1/ORDER_VERIFICATION_FINDINGS.md` for the full resolution path and open physics-judgement question.

---

## 3. Chameleon Mechanism Parameters Are Free (GAP-4)

The Chameleon mass scaling:

$$m_{\text{eff}}(\rho) = m_a \left(1 + \frac{\rho}{\rho_{\text{crit}}}\right)^{\gamma}$$

uses $\gamma$ and $\rho/\rho_{\text{crit}}$ as **free phenomenological parameters fitted via MCMC** (see `scripts/candelas_chameleon_solver.py`). In standard Khoury-Weltman chameleon field theory, the exponent is $\gamma = n/(n+2)$ for an inverse power-law $V(\phi) \propto \phi^{-n}$. The value $\gamma = 0.25$ would require $n = -3$, which is unphysical.

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

## 5. Datasets: Partially Archival, Partially Simplified (GAP-5) (Updated Phase 12)

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
| GD-1 No-Go for CY3 axions | ✅ Kernel-verified (exact ℚ arithmetic) |
| AEDE potential non-negativity | ✅ Kernel-verified (`cos_le_one`, `positivity`) |
| Chameleon $m_\text{eff}$ monotonicity | ✅ Kernel-verified (`rpow_lt_rpow`) |
| Axion mass positivity (Svrcek-Witten formula) | ✅ Kernel-verified (`MassFromInstanton.lean`) |
| S₁₂ sequence: 20 exact values + Weil bounds | ✅ Kernel-verified (`S12RecurrenceVerification.lean`) |
| Relative gauge-coupling ratio $\alpha^{-1}_{S_{1,2}}/\alpha^{-1}_{S_{2,1}}=\sqrt{1014/336}\in(1.73,1.75)$ | ✅ Kernel-verified (`GaugeCoupling.lean`, exact ℚ) |
| $S_{20}$ order-5 recurrence, concrete $n\le8$ | ✅ Kernel-verified (`S20Recurrence.lean`, `decide`) |
| $S_{20}$ order-4 minimal recurrence, concrete $n\le8$ | ✅ Kernel-verified (`S20Recurrence.lean`, `decide`) |
| $S_{20}$ order-4 minimal recurrence, general $n$ | ⚠️ Explicit `axiom`; algebraically verified for all $n$ via exact symbolic WZ certificate evaluation (SymPy check: `diff = 0`); numerically verified for all $n \in [0,60]$ |
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
