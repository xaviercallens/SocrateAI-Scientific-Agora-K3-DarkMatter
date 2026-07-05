# ⚠️ Scientific Caveats & Known Limitations

> **Epistemic Stance**: This repository houses a *theoretical mathematical exploration*, not a claimed observational discovery. The results below are computational and conjectural. We explicitly document the known limitations to ensure intellectual honesty.
> 
> **Version**: Updated 2026-06-25 (Phase 12 Peer Review Remediation). Prior version contradicted the implementation state. See `LESSONS_LEARNT.md §26`.

---

## 1. Mass Calibration Is Parameterized, Not Uniquely Predicted

The axion mass predictions ($m_a = 3.18 \times 10^{-21}$ eV for $S_{1,2}$ and $1.83 \times 10^{-21}$ eV for $S_{2,1}$) are derived using the Svrcek-Witten (2006) instanton formula:

$$m_a = \frac{M_{\text{Pl}}}{\sqrt{\mathcal{V}}} \sqrt{\sum_d d^2 \, q_d \, e^{-2\pi d\tau}}$$

However, **the Kähler modulus $\tau$ and volume $\mathcal{V}$ are not uniquely fixed by the K3 topology.** A full derivation would require a moduli stabilization mechanism (KKLT, Large Volume Scenario). Without this, the formula simply shows that FDM-range masses are *achievable* for $\mathcal{V} \sim 10^4$, $\tau \sim 30$–35 — it does not *predict* specific values.

**Status**: The mass predictions should be treated as *achievability demonstrations* within a two-parameter ($\tau$, $\mathcal{V}$) family. The parameter sweep in `scripts/mass_from_first_principles.py` shows the achievable contour.

---

## 2. K3 Surface Identification Is Conjectural

The classification of $S_{1,2}$ and $S_{2,1}$ as "K3 surfaces" is based on detecting Order-3 Picard-Fuchs recurrences via exact nullspace extraction. However:

- The mapping **"Order-3 Picard-Fuchs ↔ K3 Surface"** relies on the Stienstra-Beukers correspondence, which is **not formally verified in Lean 4** and requires additional checks (monodromy computation, modularity of Fourier coefficients).
- The monodromy matrix computation in `scripts/k3_monodromy_verification.py` extracts the **PF ODE singular points** (now genuine). Full connection matrix computation via `mpmath` analytic continuation is in progress (Phase 12-P2).
- The Weil bound check (`|a_p mod p| ≤ p`) is computed; this is a necessary but not sufficient condition for K3 identification.

**Status**: The K3 identification is a **computationally supported conjecture** pending complete monodromy and modularity verification.

---

## 3. Chameleon Mechanism Parameters Are Free

The Chameleon mass scaling:

$$m_{\text{eff}}(\rho) = m_a \left(1 + \frac{\rho}{\rho_{\text{crit}}}\right)^{\gamma}$$

uses $\gamma$ and $\rho/\rho_{\text{crit}}$ as **free phenomenological parameters fitted via MCMC** (see `scripts/candelas_chameleon_solver.py`). In standard Khoury-Weltman chameleon field theory, the exponent is $\gamma = n/(n+2)$ for an inverse power-law $V(\phi) \propto \phi^{-n}$. The value $\gamma = 0.25$ would require $n = -3$, which is unphysical.

**Status**: The superradiance evasion relies on a density-dependent mechanism with **tunable parameters not derived from the K3 compactification geometry**. The MCMC posterior on $\gamma$ is the honest representation of our knowledge.

---

## 4. Superradiance Growth Rate (Updated Phase 12)

The code now uses the correct **Detweiler (1980) / Dolan (2007) growth rate** for the dominant $l=m=1$, $n=2$ mode:

$$\Gamma_{211} \approx \frac{1}{24} a_* \alpha^8 \mu_{\text{eff}}$$

(Previously incorrectly used $\alpha^5$; corrected in Phase 12, see `scripts/superradiance_growth_rate.py`.)

**Remaining caveat**: This formula is valid in the small-$\alpha$ limit. For $\alpha_{\text{eff}} \gg 1$ (deep in the Chameleon-boosted regime), the Detweiler approximation breaks down and the full Teukolsky equation solution (Dolan 2007) is required. The current code uses the small-$\alpha$ formula even outside its regime of validity.

---

## 5. Datasets: Partially Archival, Partially Simplified (Updated Phase 12)

The CSV files in `scientific_protocol/datasets/` have been improved from fully synthetic placeholders:

- `SPARC_IC2574.csv`: **Real SPARC rotmod observational data** (Lelli et al. 2016). Full dataset with ~40 radial bins downloaded from astroweb.cwru.edu/SPARC/. Columns: `Radius_kpc, Vobs_km_s, errV_km_s, Vgas_km_s, Vdisk_km_s`. ✅
- `GD1_constraints.csv`: **Simplified from** Bonaca et al. 2019 Table 1. Not a direct machine-readable extraction; column definitions may differ from the published table. Use the primary paper for any quantitative analysis. ⚠️
- `M87_spin_bounds.csv`: **Archival spin bounds** from EHT 2019 and Cui et al. 2023. Note that EHT 2019 constrains mass, not spin directly; the spin value $a_* \approx 0.9$ is from the jet-precession analysis of Cui et al. 2023, which itself carries modeling uncertainties. ⚠️

**For quantitative scientific analysis**: Use the SPARC database directly (http://astroweb.cwru.edu/SPARC/), Bonaca et al. 2019 ApJ 880, 38, and EHT Collaboration 2019 ApJL 875, L1.

---

## 6. Lean 4 Proofs: What Is vs. What Is Not Formally Verified

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
