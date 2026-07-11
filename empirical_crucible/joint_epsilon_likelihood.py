"""
GAP-5 / Task T5.3: the "Cosmic See-Saw" test (VISION.md §4A) -- does a single
epsilon/axion-mass simultaneously fit the JWST early-galaxy excess AND the
late-time S8 deficit?

Falsification criterion (VISION.md §4A, scientificplan.md T5.3): build
L(epsilon) = L_JWST(epsilon) * L_S8(epsilon); if the JWST-preferred epsilon
and the S8-preferred epsilon are mutually exclusive at >3 sigma, the see-saw
hypothesis is dead.

WHAT THIS SCRIPT ACTUALLY DOES, honestly scoped (Rule 1/Rule 4):

  S8 side (fully executed, two independent real calculations):
    (a) The standard fuzzy-dark-matter (FDM) quantum-pressure suppression
        mechanism (Hu, Barkana & Gruzinov 2000, PRL 85, 1158 -- the actual
        physical mechanism VISION.md §4A cites for "a longer de Broglie
        wavelength...suppresses small-scale power"), applied to this
        model's own established axion masses (m_a(S12)=3.18e-21 eV,
        m_a(S21)=1.83e-21 eV, PARAMETER_LEDGER.yaml), using the real CLASS
        linear P(k) as the baseline (validated: this script's own sigma8
        integral reproduces CLASS's cosmo.sigma8() to 5 significant
        figures before trusting it with FDM suppression applied).
    (b) A separate calculation of the linear growth factor D(a) under the
        epsilon-modified background from T5.2 (rho_DM ∝ a^{-3-epsilon},
        cs2=0 -- i.e. treating epsilon as a Generalized Dark Matter
        background modification, NOT the FDM quantum-pressure channel).

  JWST side (NOT quantitatively executed -- honestly flagged, not
  fabricated): building a rigorous L_JWST(epsilon) requires either
  reproducing a full halo-mass-function / stellar-mass-function calculation
  (Press-Schechter or better, with a stellar-to-halo-mass relation) or
  finding a published paper that already fits an axion-mass-vs-JWST
  posterior directly comparable to this model's parametrization. Neither is
  attempted here: a from-scratch halo-modeling calculation would have no
  independent benchmark to validate against (the same concern that ruled
  out a hand-patched CLASS perturbation fork in T5.2), and fabricating a
  precise-looking posterior would repeat exactly the kind of unverified
  claim this session already caught and corrected twice. Instead, this
  script reports a real, independently-published QUALITATIVE consistency
  check: Cox, Jaeckel & Nurmi (or similar), "Enhanced Early Galaxy Formation
  in JWST from Axion Dark Matter?" (arXiv:2307.10302) find a *viable ALP
  mass window* of 1e-22 eV < m_a < 1e-19 eV for addressing the JWST excess
  via a DIFFERENT mechanism (delayed oscillation onset, not this model's
  mass-varying/chameleon mechanism) -- both of this model's masses fall
  within that window, which is necessary-condition-only evidence, not a
  quantitative fit.

  CONSEQUENCE: the full ">3 sigma mutual exclusion" falsification test from
  VISION.md §4A cannot be completed as specified without the missing
  JWST-side likelihood. What CAN be reported: the S8 side, evaluated
  quantitatively for the first time against this model's own real
  parameters, does NOT show the claimed suppression mechanism working --
  a real, negative, falsification-relevant finding in its own right,
  reported per Rule 4 rather than buried.

Real cited external data (fetched live via WebSearch, not from memory):
  - Planck 2018 (TT,TE,EE+lowE): S8 = 0.834 +/- 0.016
  - KiDS-1000 (2023, cosmic shear): S8 = 0.776 (+0.029/-0.027 stat, small sys)
  - DES Y3 + KiDS-1000 joint: S8 = 0.790 (+0.018/-0.014)

Outputs:
  data/cosmology/joint_epsilon_likelihood.csv
  docs/cosmology/joint_epsilon_likelihood.md

Verify: python empirical_crucible/joint_epsilon_likelihood.py
"""
import csv
import os

import numpy as np
from scipy.integrate import quad, solve_ivp

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data", "cosmology")
DOCS_DIR = os.path.join(REPO_ROOT, "docs", "cosmology")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

EPSILON = 0.02511
M_A_S12_EV = 3.18e-21
M_A_S21_EV = 1.83e-21
H_FIDUCIAL = 0.6736

# Real, cited S8 measurements (fetched live, 2026-07-11; see module docstring for sources).
S8_MEASUREMENTS = {
    "Planck 2018 (TT,TE,EE+lowE)": (0.834, 0.016),
    "KiDS-1000 (2023 cosmic shear)": (0.776, 0.028),  # symmetrized (+0.029/-0.027, sys~0.003 negligible here)
    "DES Y3 + KiDS-1000 joint": (0.790, 0.016),  # symmetrized (+0.018/-0.014)
}


def get_baseline_and_pk():
    from classy import Class
    cosmo = Class()
    cosmo.set({
        "output": "mPk", "P_k_max_1/Mpc": 50.0,
        "h": H_FIDUCIAL, "omega_b": 0.02237, "omega_cdm": 0.1200,
        "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544,
    })
    cosmo.compute()
    return cosmo


def W_tophat(x):
    return 3.0 * (np.sin(x) - x * np.cos(x)) / x**3


def sigma8_with_transfer(cosmo, h, transfer_sq=None, R_hmpc=8.0):
    def integrand(lnk):
        k_hmpc = np.exp(lnk)
        pk = cosmo.pk(k_hmpc * h, 0.0) * h**3
        tsq = transfer_sq(k_hmpc) if transfer_sq else 1.0
        return k_hmpc**3 * pk * tsq * W_tophat(k_hmpc * R_hmpc)**2 / (2 * np.pi**2)
    val, _ = quad(integrand, np.log(1e-4), np.log(40.0), limit=400)
    return np.sqrt(val)


def T_fdm_sq(k_hmpc, m_a_eV, h):
    """Hu, Barkana & Gruzinov (2000) FDM transfer function squared, T^2(k).
    k_Jeq is defined in 1/Mpc (not h/Mpc); k_hmpc*h converts to 1/Mpc."""
    m22 = m_a_eV / 1e-22
    k_Jeq = 9.0 * np.sqrt(m22)  # 1/Mpc
    x = 1.61 * m22**(1.0 / 18.0) * (k_hmpc * h / k_Jeq)
    return (np.cos(x**3) / (1 + x**8))**2


def compute_growth_factor(epsilon, omega_b, omega_cdm, omega_r, h):
    """Linear growth factor D(a) under rho_DM(a) ∝ a^{-3-epsilon}, treated
    as a cs2=0 Generalized Dark Matter background modification (as opposed
    to the FDM quantum-pressure channel computed separately above)."""
    def E2(a):
        Omega_Lambda = 1.0 - (omega_r + omega_b + omega_cdm) / h**2
        return (omega_r * a**-4 + omega_b * a**-3 + omega_cdm * a**(-3 - epsilon)) / h**2 + Omega_Lambda

    def Omega_m_of_a(a):
        return (omega_b * a**-3 + omega_cdm * a**(-3 - epsilon)) / h**2 / E2(a)

    def dlnE2_da(a, da=1e-6):
        return (np.log(E2(a + da)) - np.log(E2(a - da))) / (2 * da)

    def growth_ode(a, y):
        D, Dp = y
        coeff1 = 3.0 / a + 0.5 * dlnE2_da(a)
        coeff2 = 1.5 * Omega_m_of_a(a) / a**2
        return [Dp, -coeff1 * Dp + coeff2 * D]

    a_start = 1e-3
    sol = solve_ivp(growth_ode, (a_start, 1.0), [a_start, 1.0], method="Radau",
                     rtol=1e-10, atol=1e-12)
    return sol.y[0][-1]


def main():
    print("=" * 90)
    print("GAP-5 / T5.3: Cosmic See-Saw test (VISION.md §4A) -- S8 side")
    print("=" * 90)

    print("\n[1/3] Real CLASS baseline P(k), validating sigma8 integral...")
    cosmo = get_baseline_and_pk()
    sigma8_class = cosmo.sigma8()
    sigma8_mine = sigma8_with_transfer(cosmo, H_FIDUCIAL)
    err_pct = abs(sigma8_mine / sigma8_class - 1) * 100
    print(f"  CLASS sigma8={sigma8_class:.6f}  mine={sigma8_mine:.6f}  err={err_pct:.4f}%")
    if err_pct > 0.1:
        print("  ABORTING: sigma8 integrator not validated.")
        return

    print("\n[2/3] FDM quantum-pressure suppression (Hu-Barkana-Gruzinov 2000) "
          "at this model's own axion masses...")
    fdm_results = {}
    for name, m_a in [("S12", M_A_S12_EV), ("S21", M_A_S21_EV)]:
        s8_fdm = sigma8_with_transfer(cosmo, H_FIDUCIAL, lambda k: T_fdm_sq(k, m_a, H_FIDUCIAL))
        ratio = s8_fdm / sigma8_mine
        fdm_results[name] = (m_a, s8_fdm, ratio)
        print(f"  {name} (m_a={m_a:.2e} eV): sigma8_FDM/sigma8_CDM = {ratio:.6f} "
              f"(suppression: {(1-ratio)*100:.4f}%)")

    print("\n[3/3] Growth-factor calculation under the epsilon-modified background "
          "(T5.2's model, cs2=0 GDM treatment)...")
    bg = cosmo.get_background()
    h = H_FIDUCIAL
    omega_gamma = bg["(.)rho_g"][-1] / bg["(.)rho_crit"][-1] * h**2
    omega_ur = bg["(.)rho_ur"][-1] / bg["(.)rho_crit"][-1] * h**2
    omega_b = bg["(.)rho_b"][-1] / bg["(.)rho_crit"][-1] * h**2
    omega_cdm = bg["(.)rho_cdm"][-1] / bg["(.)rho_crit"][-1] * h**2
    omega_r = omega_gamma + omega_ur

    D_std = compute_growth_factor(0.0, omega_b, omega_cdm, omega_r, h)
    D_eps = compute_growth_factor(EPSILON, omega_b, omega_cdm, omega_r, h)
    growth_ratio = D_eps / D_std
    print(f"  D_std(a=1)={D_std:.6f}  D_eps(a=1)={D_eps:.6f}  ratio={growth_ratio:.6f}")
    print(f"  Implied S8 shift from background channel: {(growth_ratio-1)*100:+.2f}%")
    print(f"  Sign check: {'WRONG SIGN for lowering S8 (predicts an INCREASE)' if growth_ratio > 1 else 'correct sign (predicts a decrease)'}")

    print("\n[Reference] Real S8 measurements:")
    for name, (val, err) in S8_MEASUREMENTS.items():
        print(f"  {name}: S8 = {val} +/- {err}")

    print(f"\n[Qualitative JWST check] Cox et al. (arXiv:2307.10302) viable ALP mass "
          f"window for JWST: 1e-22 eV < m_a < 1e-19 eV. "
          f"S12 (3.18e-21 eV): {'within' if 1e-22 < M_A_S12_EV < 1e-19 else 'OUTSIDE'} window. "
          f"S21 (1.83e-21 eV): {'within' if 1e-22 < M_A_S21_EV < 1e-19 else 'OUTSIDE'} window. "
          f"(NOTE: this is a different mechanism than this model's own; necessary-condition "
          f"check only, NOT a quantitative fit of this model's epsilon to JWST data.)")

    # ---- Outputs ----
    csv_path = os.path.join(DATA_DIR, "joint_epsilon_likelihood.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["quantity", "value", "note"])
        writer.writerow(["sigma8_CDM_baseline", sigma8_mine, "validated vs CLASS sigma8()"])
        for name, (m_a, s8_fdm, ratio) in fdm_results.items():
            writer.writerow([f"sigma8_FDM_{name}", s8_fdm, f"m_a={m_a:.3e} eV, ratio={ratio:.6f}"])
        writer.writerow(["growth_factor_ratio_eps_over_std", growth_ratio, f"epsilon={EPSILON}, cs2=0 GDM background channel"])
        for name, (val, err) in S8_MEASUREMENTS.items():
            writer.writerow([f"S8_{name}", val, f"+/-{err}"])
    print(f"\nWrote {csv_path}")

    md_path = os.path.join(DOCS_DIR, "joint_epsilon_likelihood.md")
    lines = [
        "# GAP-5 Cosmic See-Saw Test: S8 Side (Task T5.3)",
        "",
        "Generated by `empirical_crucible/joint_epsilon_likelihood.py`. Tests the "
        "VISION.md §4A \"cosmic see-saw\" claim that a lighter present-day axion "
        "mass suppresses small-scale power and lowers S8 toward observed values.",
        "",
        "## Scope disclosure (read before citing this result)",
        "",
        "This script executes the **S8 side** of the see-saw test quantitatively, "
        "using two independent, real calculations. It does **NOT** execute a "
        "quantitative JWST-side likelihood (see below) — building one honestly "
        "requires halo-mass-function modeling with no independent benchmark "
        "available in this session, and a fabricated-looking posterior would "
        "repeat exactly the kind of unverified claim already caught twice this "
        "session (weight-2 Weil bound, 86.6 Myr superradiance figure). The full "
        "\">3σ mutual exclusion\" falsification test from VISION.md §4A therefore "
        "**cannot be completed as specified** — only the S8 half is reported.",
        "",
        "## 1. FDM quantum-pressure suppression (the model's own claimed mechanism)",
        "",
        "Using the Hu, Barkana & Gruzinov (2000, PRL 85, 1158) analytic FDM "
        "transfer function $T(k)=\\cos(x^3)/(1+x^8)$, applied to real CLASS "
        f"linear $P(k)$ (own $\\sigma_8$ integral validated to {err_pct:.4f}% "
        "against `cosmo.sigma8()`), at this model's own established axion masses:",
        "",
        "| Sequence | m_a (eV) | σ₈ suppression |",
        "|---|---|---|",
    ]
    for name, (m_a, s8_fdm, ratio) in fdm_results.items():
        lines.append(f"| {name} | {m_a:.3e} | {(1-ratio)*100:.4f}% |")
    lines += [
        "",
        f"**Finding: negligible suppression ({(1-fdm_results['S21'][2])*100:.4f}% for S21, the "
        f"lighter mass).** This model's axion masses ($\\sim1.8$–$3.2\\times10^{{-21}}$ eV) are "
        f"$\\sim20$–$30\\times$ heavier than the canonical FDM \"sweet spot\" "
        f"($\\sim10^{{-22}}$ eV) where quantum-pressure suppression matters at the "
        f"$R=8\\,h^{{-1}}$Mpc scale relevant to $S_8$. **The standard FDM mechanism "
        f"the model's own narrative invokes does not produce an observable $S_8$ "
        f"shift at these masses.**",
        "",
        "## 2. Growth-factor channel (the epsilon-modified background from T5.2)",
        "",
        f"Treating $\\epsilon$ as a $c_s^2=0$ Generalized Dark Matter background "
        f"modification (as literally specified for the CLASS treatment), the linear "
        f"growth factor ratio is "
        f"$D_\\epsilon(a{{=}}1)/D_{{\\rm std}}(a{{=}}1) = {growth_ratio:.4f}$, implying an "
        f"$S_8$ shift of **{(growth_ratio-1)*100:+.2f}%** — "
        f"{'the WRONG SIGN (an increase, not the decrease needed to help the S8 tension)' if growth_ratio>1 else 'the correct sign'}. "
        f"This is because the anomalous CDM dilution *enhances* early matter "
        f"density (see T5.2's finding that recombination-era CDM density is "
        f"boosted), which speeds up structure growth rather than suppressing it.",
        "",
        "## 3. Real S8 measurements (for reference)",
        "",
        "| Source | S8 |",
        "|---|---|",
    ]
    for name, (val, err) in S8_MEASUREMENTS.items():
        lines.append(f"| {name} | {val} ± {err} |")
    lines += [
        "",
        "Sources: Planck 2018 VI (Cosmological Parameters); KiDS-1000 2023 cosmic "
        "shear (Wright et al./van den Busch et al., A&A); DES Y3 + KiDS-1000 joint "
        "analysis (The Open Journal of Astrophysics). Fetched live via search "
        "2026-07-11, not from memory.",
        "",
        "## 4. JWST side (qualitative only — see scope disclosure)",
        "",
        "Cox et al., \"Enhanced Early Galaxy Formation in JWST from Axion Dark "
        "Matter?\" (arXiv:2307.10302), find a viable ALP mass window "
        "$10^{-22}\\,\\text{eV} < m_a < 10^{-19}\\,\\text{eV}$ for addressing the JWST "
        "excess — via a **different mechanism** (delayed axion-field-oscillation "
        "onset, not this model's mass-varying/chameleon mechanism). Both "
        f"$m_a(S_{{1,2}})={M_A_S12_EV:.2e}$ eV and $m_a(S_{{2,1}})={M_A_S21_EV:.2e}$ eV fall "
        "within that window — a necessary-condition consistency check, **not** a "
        "quantitative fit of this model's own $\\epsilon$ to JWST data.",
        "",
        "## Conclusion",
        "",
        "The full VISION.md §4A falsification test (JWST-preferred ε vs. S₈-preferred "
        "ε, mutually exclusive at >3σ or not) **cannot be completed** without a "
        "validated JWST-side likelihood — flagged as remaining work, not fabricated "
        "here. However, the S₈ side alone, now computed quantitatively for the first "
        "time against real data and this model's own real parameters, does **not** "
        "show the claimed suppression mechanism working: both the direct FDM channel "
        "(negligible effect at these masses) and the background-growth channel "
        "(wrong-signed effect) fail to produce the S₈ decrease the \"cosmic see-saw\" "
        "narrative requires. This is a real, falsification-relevant negative result, "
        "reported per Rule 4 rather than left as an untested \"consistency "
        "illustration.\"",
        "",
    ]
    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
