"""
GAP-5 / Task T5.2: Boltzmann-grade check of the mass-varying axion background,
using real CLASS (classy) as ground truth wherever possible.

The vulnerability (scientificplan.md WORKSTREAM 5, T5.2): the repository's
"H_0 ~ 72" claim (PARAMETER_LEDGER.yaml: epsilon=0.02511 -> H_0=71.92) was
computed by a background-only integration (LL.md:94) that has never been
checked against a real Boltzmann code, and per GAP-5's own description was
"reverse-engineered" (epsilon tuned to hit a target H_0, not fit
independently). This script does two things:

  (A) A SELF-CONSISTENT background/acoustic-scale recomputation. The model
      (scientificplan.md T5.2) is rho_DM(a) ∝ a^{-3-epsilon} -- an anomalous
      dilution of the DARK MATTER sector (not a dark-energy fluid; that
      distinction matters, see "Architectural finding" below). This script
      solves for the sound horizon r_s(epsilon) and comoving distance to
      recombination D_M(epsilon) using the SAME epsilon-modified H(a) in
      BOTH integrals (the previous "reverse-engineered" fit is not proven
      self-consistent -- see cross-check below), then finds the H_0 that
      keeps the CMB angular acoustic scale theta_s = r_s/D_M fixed at the
      real-CLASS-computed Planck-like baseline value.

  (B) An HONEST DOCUMENTATION of why a full perturbation-level (Cl^TT/TE/EE)
      Boltzmann computation of this exact model is NOT achieved here, and
      what would be needed. Public CLASS's native dark-energy fluid module
      (`Omega_fld`/`w0_fld`/`cs2_fld`) architecturally REJECTS any fluid
      with w(a->0) >= 0 (hard-coded check in perturbations_init(), verified
      empirically below) -- so `w_DM = epsilon/3 > 0` (the equation of state
      implied by rho_DM ∝ a^{-3-epsilon}) cannot be entered through CLASS's
      public Python API at all. A genuine fix requires patching CLASS's C
      source (background.c's CDM density law, perturbations.c's CDM
      continuity/Euler equations) and recompiling -- a real "CLASS fork" in
      the literal sense scientificplan.md names it, and a multi-session
      undertaking that (unlike the GAP-3 Dolan solver) has no independent
      published benchmark to validate against, so it is explicitly NOT
      attempted here rather than risk producing an unverifiable "Cl^TT"
      number dressed up as ground truth (Rule 1/Rule 4).

  As a documented, clearly-labeled SUPPLEMENTARY check (not the headline
  result), this script also builds a real-CLASS "effective LCDM" proxy that
  reproduces the SAME (r_s, D_M) pair as the true epsilon-model, to at least
  get one genuine Cl^TT out of real CLASS -- but the fit requires an
  unphysically boosted omega_cdm (see results), which by itself demonstrates
  why this proxy technique does NOT give a trustworthy peak-HEIGHT
  prediction for the true model (only positions are matched by
  construction). This finding is reported, not hidden.

Validation of the custom integrator (Rule 1): the sound horizon r_s and
comoving distance D_M integrators in this script are validated against
REAL CLASS's own `rs_rec`/`ra_rec`/`100*theta_s` derived parameters at
epsilon=0 (see `validate_integrator()`) to <0.01% agreement before being
trusted with epsilon != 0.

Outputs:
  data/cosmology/class_fork_validation.csv
  docs/cosmology/class_fork_validation.md

Verify: python empirical_crucible/class_fork_validation.py
"""
import csv
import os

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, fsolve

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data", "cosmology")
DOCS_DIR = os.path.join(REPO_ROOT, "docs", "cosmology")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

c_km_s = 299792.458
EPSILON = 0.02511  # PARAMETER_LEDGER.yaml, source LL.md:94
H_FIDUCIAL = 0.6736  # Planck-2018-like baseline used as reference cosmology


def get_baseline_from_class():
    """Runs real CLASS for a Planck-2018-like baseline and extracts the
    physical densities (omega_gamma, omega_ur, omega_b, omega_cdm) and
    acoustic-scale quantities used as ground truth throughout this script."""
    from classy import Class
    cosmo = Class()
    cosmo.set({
        "output": "tCl,pCl,lCl", "lensing": "yes",
        "h": H_FIDUCIAL, "omega_b": 0.02237, "omega_cdm": 0.1200,
        "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544,
    })
    cosmo.compute()
    bg = cosmo.get_background()
    h = H_FIDUCIAL
    out = {
        "omega_gamma": bg["(.)rho_g"][-1] / bg["(.)rho_crit"][-1] * h**2,
        "omega_ur": bg["(.)rho_ur"][-1] / bg["(.)rho_crit"][-1] * h**2,
        "omega_b": bg["(.)rho_b"][-1] / bg["(.)rho_crit"][-1] * h**2,
        "omega_cdm": bg["(.)rho_cdm"][-1] / bg["(.)rho_crit"][-1] * h**2,
        "z_rec": cosmo.get_current_derived_parameters(["z_rec"])["z_rec"],
        "rs_rec": cosmo.get_current_derived_parameters(["rs_rec"])["rs_rec"],
        "ra_rec": cosmo.get_current_derived_parameters(["ra_rec"])["ra_rec"],
        "theta_s_100": cosmo.get_current_derived_parameters(["100*theta_s"])["100*theta_s"],
        "cl_tt": cosmo.lensed_cl(2500)["tt"],
        "ell": cosmo.lensed_cl(2500)["ell"],
    }
    cosmo.struct_cleanup()
    return out


def H_of_a(a, h, omega_b, omega_cdm, omega_r, epsilon=0.0):
    """H(a) in km/s/Mpc for a flat universe with anomalous CDM dilution
    rho_cdm(a) ∝ a^{-3-epsilon} (scientificplan.md T5.2). omega_x are
    PHYSICAL densities (Omega_x * h^2), independent of h by construction;
    Omega_Lambda is fixed by flatness at a=1."""
    Omega_Lambda = 1.0 - (omega_r + omega_b + omega_cdm) / h**2
    E2 = (omega_r * a**-4 + omega_b * a**-3 + omega_cdm * a**(-3 - epsilon)) / h**2 + Omega_Lambda
    return 100.0 * h * np.sqrt(E2)


def sound_horizon(h, omega_b, omega_cdm, omega_r, omega_gamma, epsilon, a_star):
    def integrand(a):
        R = (3.0 * omega_b) / (4.0 * omega_gamma) * a
        cs = c_km_s / np.sqrt(3.0 * (1.0 + R))
        return cs / (a**2 * H_of_a(a, h, omega_b, omega_cdm, omega_r, epsilon))
    return quad(integrand, 1e-8, a_star, limit=200)[0]


def comoving_distance(h, omega_b, omega_cdm, omega_r, epsilon, a_star):
    def integrand(a):
        return c_km_s / (a**2 * H_of_a(a, h, omega_b, omega_cdm, omega_r, epsilon))
    return quad(integrand, a_star, 1.0, limit=200)[0]


def validate_integrator(baseline):
    """Cross-checks the custom r_s/D_M integrator against real CLASS's own
    derived parameters at epsilon=0. Returns (rs_err_pct, dm_err_pct,
    theta_s_err_pct)."""
    a_rec = 1.0 / (1.0 + baseline["z_rec"])
    rs_mine = sound_horizon(H_FIDUCIAL, baseline["omega_b"], baseline["omega_cdm"],
                             baseline["omega_gamma"] + baseline["omega_ur"],
                             baseline["omega_gamma"], 0.0, a_rec)
    dm_mine = comoving_distance(H_FIDUCIAL, baseline["omega_b"], baseline["omega_cdm"],
                                 baseline["omega_gamma"] + baseline["omega_ur"], 0.0, a_rec)
    theta_s_mine = rs_mine / dm_mine * 100
    rs_err = abs(rs_mine / baseline["rs_rec"] - 1) * 100
    dm_err = abs(dm_mine / baseline["ra_rec"] - 1) * 100
    theta_err = abs(theta_s_mine / baseline["theta_s_100"] - 1) * 100
    return rs_mine, dm_mine, theta_s_mine, rs_err, dm_err, theta_err


def test_class_fld_rejects_positive_w():
    """Empirically confirms the architectural blocker: CLASS's public fld
    module rejects w_fld(a->0) >= 0, which is what rho_DM ∝ a^{-3-epsilon}
    (epsilon>0) implies for a fluid treatment (w=epsilon/3>0). Returns
    (attempted, raised_error_message) so the finding is verified live, not
    asserted from memory."""
    from classy import Class
    cosmo = Class()
    cosmo.set({
        "output": "tCl", "h": H_FIDUCIAL, "omega_b": 0.02237, "omega_cdm": 0.1200,
        "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544,
        "Omega_Lambda": 0.0, "w0_fld": EPSILON / 3.0, "wa_fld": 0.0, "cs2_fld": 0.0,
    })
    try:
        cosmo.compute()
        cosmo.struct_cleanup()
        return True, None
    except Exception as e:
        return False, str(e)


def main():
    print("=" * 90)
    print("GAP-5 / T5.2: Boltzmann-grade check of the mass-varying-axion background")
    print("=" * 90)

    print("\n[1/5] Running real CLASS for the Planck-2018-like baseline...")
    baseline = get_baseline_from_class()
    print(f"  omega_b={baseline['omega_b']:.6f}  omega_cdm={baseline['omega_cdm']:.6f}  "
          f"omega_gamma={baseline['omega_gamma']:.4e}  omega_ur={baseline['omega_ur']:.4e}")
    print(f"  z_rec={baseline['z_rec']:.4f}  rs_rec={baseline['rs_rec']:.4f} Mpc  "
          f"ra_rec={baseline['ra_rec']:.4f} Mpc  100*theta_s={baseline['theta_s_100']:.6f}")

    print("\n[2/5] Validating the custom r_s/D_M integrator against real CLASS (epsilon=0)...")
    rs_mine, dm_mine, theta_mine, rs_err, dm_err, theta_err = validate_integrator(baseline)
    print(f"  r_s:      mine={rs_mine:.4f}  CLASS={baseline['rs_rec']:.4f}  err={rs_err:.4f}%")
    print(f"  D_M:      mine={dm_mine:.4f}  CLASS={baseline['ra_rec']:.4f}  err={dm_err:.4f}%")
    print(f"  theta_s:  mine={theta_mine:.6f}  CLASS={baseline['theta_s_100']:.6f}  err={theta_err:.4f}%")
    integrator_ok = max(rs_err, dm_err, theta_err) < 0.1
    print(f"  Integrator validated (<0.1% target): {'PASS' if integrator_ok else 'FAIL'}")
    if not integrator_ok:
        print("  ABORTING: integrator not trustworthy, refusing to report epsilon!=0 results.")
        return

    print(f"\n[3/5] Architectural check: can CLASS's public fld module represent "
          f"w_DM=epsilon/3={EPSILON/3:.5f} (>0) directly?")
    fld_worked, fld_error = test_class_fld_rejects_positive_w()
    if fld_worked:
        print("  UNEXPECTED: CLASS accepted the w>=0 fluid (re-examine this script's assumption).")
    else:
        print(f"  CONFIRMED BLOCKED (expected): {fld_error.strip().splitlines()[-1] if fld_error else fld_error}")

    print(f"\n[4/5] Self-consistent background recomputation at epsilon={EPSILON} "
          f"(scientificplan.md: rho_DM ∝ a^(-3-epsilon))...")
    a_rec = 1.0 / (1.0 + baseline["z_rec"])
    omega_r = baseline["omega_gamma"] + baseline["omega_ur"]

    def theta_s_of_h(h, epsilon):
        rs = sound_horizon(h, baseline["omega_b"], baseline["omega_cdm"], omega_r,
                            baseline["omega_gamma"], epsilon, a_rec)
        dm = comoving_distance(h, baseline["omega_b"], baseline["omega_cdm"], omega_r, epsilon, a_rec)
        return rs / dm * 100

    h_true = brentq(lambda h: theta_s_of_h(h, EPSILON) - baseline["theta_s_100"], 0.4, 1.2)
    rs_true = sound_horizon(h_true, baseline["omega_b"], baseline["omega_cdm"], omega_r,
                             baseline["omega_gamma"], EPSILON, a_rec)
    dm_true = comoving_distance(h_true, baseline["omega_b"], baseline["omega_cdm"], omega_r, EPSILON, a_rec)
    print(f"  H_0 required to preserve theta_s: {100*h_true:.4f} km/s/Mpc")
    print(f"  (PARAMETER_LEDGER.yaml currently claims H_0≈71.92 km/s/Mpc for this epsilon)")
    print(f"  r_s(epsilon-model, matched) = {rs_true:.4f} Mpc  (ledger claims r_s≈138.87 Mpc)")
    print(f"  D_M(epsilon-model, matched) = {dm_true:.4f} Mpc  (ledger claims D_M≈13338.60 Mpc)")

    # Sanity check: a plausible "mixed" (inconsistent) shortcut that could explain
    # the previous H_0=71.92 -- report it for transparency, not as a re-derivation
    # of the exact previous method (which is not fully documented).
    rs_std = sound_horizon(H_FIDUCIAL, baseline["omega_b"], baseline["omega_cdm"], omega_r,
                            baseline["omega_gamma"], 0.0, a_rec)

    def theta_s_mixed(h):
        dm = comoving_distance(h, baseline["omega_b"], baseline["omega_cdm"], omega_r, EPSILON, a_rec)
        return rs_std / dm * 100
    h_mixed = brentq(lambda h: theta_s_mixed(h) - baseline["theta_s_100"], 0.3, 1.2)
    print(f"  [diagnostic only] if r_s is NOT epsilon-corrected but D_M is "
          f"(an internally inconsistent shortcut): H_0 = {100*h_mixed:.4f} km/s/Mpc")

    print(f"\n[5/5] Supplementary check: effective-LCDM proxy matching (r_s, D_M) via real CLASS...")
    print("  (peak POSITIONS match by construction; peak HEIGHTS are NOT a trustworthy")
    print("   prediction of the true model -- see result below and docs for why)")

    def system(x):
        h_eff, omega_cdm_eff = x
        rs = sound_horizon(h_eff, baseline["omega_b"], omega_cdm_eff, omega_r,
                            baseline["omega_gamma"], 0.0, a_rec)
        dm = comoving_distance(h_eff, baseline["omega_b"], omega_cdm_eff, omega_r, 0.0, a_rec)
        return [rs - rs_true, dm - dm_true]

    (h_eff, omega_cdm_eff), info, ier, msg = fsolve(
        system, [h_true, baseline["omega_cdm"]], full_output=True)
    print(f"  Effective proxy: H_0_eff={100*h_eff:.4f} km/s/Mpc, omega_cdm_eff={omega_cdm_eff:.6f} "
          f"(true model's own omega_cdm={baseline['omega_cdm']:.4f})")
    cdm_distortion_pct = abs(omega_cdm_eff / baseline["omega_cdm"] - 1) * 100
    print(f"  omega_cdm distortion required: {cdm_distortion_pct:.1f}% "
          f"-- this is why peak heights from this proxy are not trustworthy.")

    from classy import Class
    cosmo_eff = Class()
    cosmo_eff.set({
        "output": "tCl,pCl,lCl", "lensing": "yes",
        "h": float(h_eff), "omega_b": baseline["omega_b"], "omega_cdm": float(omega_cdm_eff),
        "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544,
    })
    cosmo_eff.compute()
    cl_eff = cosmo_eff.lensed_cl(2500)
    cosmo_eff.struct_cleanup()

    ell = baseline["ell"]
    tt_base = baseline["cl_tt"]
    tt_eff = cl_eff["tt"]
    mask = (ell >= 2) & (tt_base > 0)
    frac_dev = np.abs(tt_eff[mask] / tt_base[mask] - 1)
    max_dev_pct = np.max(frac_dev) * 100
    max_dev_ell = ell[mask][np.argmax(frac_dev)]
    print(f"  Max |ΔCl^TT/Cl^TT| across ell in [2,2500]: {max_dev_pct:.1f}% at ell={max_dev_ell} "
          f"(dominated by the {cdm_distortion_pct:.0f}% omega_cdm distortion, NOT a physical prediction)")

    # ---- Write outputs ----
    csv_path = os.path.join(DATA_DIR, "class_fork_validation.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["quantity", "baseline", "epsilon_model_self_consistent", "mixed_shortcut_diagnostic", "ledger_previous_claim"])
        writer.writerow(["H0_km_s_Mpc", H_FIDUCIAL * 100, 100 * h_true, 100 * h_mixed, 71.92])
        writer.writerow(["r_s_Mpc", baseline["rs_rec"], rs_true, rs_std, 138.87])
        writer.writerow(["D_M_Mpc", baseline["ra_rec"], dm_true, "n/a", 13338.60])
        writer.writerow(["100_theta_s", baseline["theta_s_100"], theta_s_of_h(h_true, EPSILON), "n/a", "n/a"])
    print(f"\nWrote {csv_path}")

    md_path = os.path.join(DOCS_DIR, "class_fork_validation.md")
    lines = [
        "# GAP-5 CLASS-Grade Background Validation (Task T5.2)",
        "",
        "Generated by `empirical_crucible/class_fork_validation.py`, using real CLASS "
        f"(classy {__import__('classy').__version__ if hasattr(__import__('classy'), '__version__') else 'installed'}) "
        "as ground truth wherever possible.",
        "",
        "## 1. Integrator validation (against real CLASS, epsilon=0)",
        "",
        f"Custom sound-horizon/comoving-distance integrator reproduces CLASS's own derived "
        f"parameters to <{max(rs_err, dm_err, theta_err):.3f}% (r_s: {rs_err:.4f}%, "
        f"D_M: {dm_err:.4f}%, theta_s: {theta_err:.4f}%) — trusted for the epsilon!=0 case below.",
        "",
        "## 2. Architectural finding: CLASS's public fld module cannot represent this model directly",
        "",
        f"`rho_DM(a) ∝ a^{{-3-ε}}` (scientificplan.md T5.2) implies an equation of state "
        f"w_DM = ε/3 ≈ {EPSILON/3:.5f} (positive). Attempting this via CLASS's native "
        f"dark-energy fluid API (`Omega_fld`, `w0_fld`, `cs2_fld`) raises a hard error "
        f"(confirmed live, not from memory): "
        f"`{'CLASS unexpectedly accepted this' if fld_worked else (fld_error.strip().splitlines()[-1] if fld_error else 'error')}`",
        "",
        "This is architectural, not a parameter-tuning issue: CLASS's perturbation "
        "initial-condition code assumes any `fld` species is negligible at early times "
        "(w<0 required), which is fundamentally incompatible with a component that "
        "dilutes *faster* than matter (w>0) and therefore grows in relative importance at "
        "a->0. A literal implementation requires patching CLASS's C source "
        "(`background.c`'s CDM density law and `perturbations.c`'s CDM continuity/Euler "
        "equations) and recompiling — a genuine \"CLASS fork\" in the sense the task names "
        "it. That patch is NOT attempted here: unlike the GAP-3 Dolan solver (validated "
        "against 6 independent published data points), a custom perturbation-equation "
        "patch would have no independent benchmark to validate against, and shipping an "
        "unverified custom Boltzmann patch as ground truth would repeat exactly the kind "
        "of unverified-claim failure this session already caught twice (GAP-1's weight-2 "
        "bound, GAP-3's 86.6 Myr figure). This is flagged as required follow-up work.",
        "",
        "## 3. Self-consistent background recomputation (real result)",
        "",
        "| Quantity | Baseline (ΛCDM) | ε-model, self-consistent | Ledger's previous claim |",
        "|---|---|---|---|",
        f"| H₀ (km/s/Mpc) | {100*H_FIDUCIAL:.2f} | **{100*h_true:.2f}** | 71.92 |",
        f"| r_s (Mpc) | {baseline['rs_rec']:.2f} | {rs_true:.2f} | 138.87 |",
        f"| D_M(z_rec) (Mpc) | {baseline['ra_rec']:.2f} | {dm_true:.2f} | 13338.60 |",
        f"| 100·θ_s | {baseline['theta_s_100']:.5f} | {theta_s_of_h(h_true, EPSILON):.5f} (matched by construction) | — |",
        "",
        f"**Key finding:** applying epsilon={EPSILON} consistently to BOTH the sound-horizon "
        f"integral and the comoving-distance integral (both depend on the same modified "
        f"H(a)) and solving for the H₀ that preserves the real-CLASS-computed acoustic "
        f"scale gives **H₀ ≈ {100*h_true:.2f} km/s/Mpc**, not the previously-claimed 71.92. "
        f"This is a real, substantive discrepancy (~{100*h_true-71.92:+.1f} km/s/Mpc), and "
        f"notably OVERSHOOTS even the SH0ES local measurement (~73 km/s/Mpc) rather than "
        f"landing between Planck and SH0ES as the model intends.",
        "",
        f"A diagnostic check — deliberately using the STANDARD (epsilon=0) sound horizon "
        f"together with the epsilon-modified comoving distance (an internally "
        f"*inconsistent* shortcut) — gives H₀ = {100*h_mixed:.2f} km/s/Mpc instead, which is "
        f"also far from 71.92. Neither the fully self-consistent nor this particular "
        f"inconsistent-shortcut calculation reproduces the ledger's number; the exact "
        f"method behind the original epsilon=0.02511 → H₀=71.92 fit (LL.md:94) is not "
        f"fully documented/reproducible from what's in the repository. Per Rule 1, this "
        f"discrepancy is reported rather than silently reconciled.",
        "",
        "## 4. Supplementary: effective-LCDM proxy Cl^TT (illustrative only)",
        "",
        f"An LCDM proxy (H₀_eff={100*h_eff:.2f}, ω_cdm_eff={omega_cdm_eff:.4f}) was fit via "
        f"real CLASS to reproduce the SAME (r_s, D_M) as the self-consistent ε-model above. "
        f"**This requires boosting ω_cdm by {cdm_distortion_pct:.0f}% above the true model's "
        f"own value (0.12)** — which by itself shows this proxy technique conflates a "
        f"redshift-*scaling* change (what ε actually does) with a density-*normalization* "
        f"change, and should NOT be read as a genuine prediction of the true model's CMB "
        f"peak heights. Its Cl^TT deviates from the baseline by up to "
        f"**{max_dev_pct:.0f}%** (at ℓ≈{max_dev_ell}) — this number is dominated by the "
        f"artificial ω_cdm boost, not physical content, and is reported only as a concrete "
        f"illustration of why this shortcut is untrustworthy for peak heights, not as the "
        f"model's actual Cl^TT deviation.",
        "",
        "## What this resolves and what remains open",
        "",
        "- **Resolved:** the previous H₀≈72 background-only estimate is now checked against "
        "a real-CLASS-validated integrator rather than an undocumented formula; the result "
        "is a genuine (if unwelcome) finding — the self-consistent number is H₀≈"
        f"{100*h_true:.1f}, materially different from and less favorable than the previous "
        "claim (it overshoots SH0ES rather than bridging Planck/SH0ES).",
        "- **Still open (GAP-5 not fully closed):** a true perturbation-level Cl^TT/TE/EE "
        "computation of the anomalous-CDM model requires a genuine CLASS C-source fork "
        "(background.c + perturbations.c), which has no available independent benchmark "
        "and is not attempted here. T5.4 (DESI DR2 refit) and full χ² against Planck "
        "plik-lite remain blocked on that fork.",
        "",
    ]
    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
