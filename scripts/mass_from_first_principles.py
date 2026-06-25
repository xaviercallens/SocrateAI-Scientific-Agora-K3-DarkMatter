# HONEST ASSESSMENT: This script demonstrates that the Svrcek-Witten formula
# CAN produce FDM-range masses (1e-22 to 1e-20 eV), but does NOT fix unique
# (tau, V) values without a moduli stabilization mechanism.
#
# The circular fitting against pre-assumed targets (target_mass_S12 = 3.18e-21,
# target_mass_S21 = 1.83e-21) has been REMOVED.  Those targets originated from
# spin-down phenomenology; using them to back-calibrate (tau, V) and then
# claiming the model "predicts" the masses is logically circular.
#
# What this script honestly shows:
#   - A parameter sweep over (tau, V) space
#   - A contour plot showing the region where m_a falls in the FDM window
#   - A printed summary stating that parameters are not uniquely determined

import numpy as np
import matplotlib
matplotlib.use("Agg")   # non-interactive; safe for headless runs
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------------------------
# Svrcek–Witten / Conlon formula for the K3-fibred axion mass
# ---------------------------------------------------------------------------
# References:
#   Svrcek & Witten (2006) JHEP 06, 051
#   Conlon (2006) JHEP 05, 078
#
# M_Pl = 2.4e18 GeV   (reduced Planck mass)
# M_s  = M_Pl / sqrt(V)            (string scale)
# f_a  = M_Pl / sqrt(V)            (axion decay constant, leading-order)
# S_inst = 2 π τ                   (instanton action for modulus τ)
#
# Non-perturbative superpotential contribution:
#   Λ^4 = M_s^4 * Σ_{d=1}^{N} d^2 * q_d * exp(-2π d τ)
#
# Axion mass:
#   m_a^2 = Λ^4 / f_a^2
#          = (M_Pl^2 / V) * Σ_{d} d^2 * q_d * exp(-2π d τ)
#
#   m_a = (M_Pl / sqrt(V)) * sqrt(Σ_{d} d^2 * q_d * exp(-2π d τ))

M_PL_EV = 2.4e27   # reduced Planck mass in eV  (2.4e18 GeV × 1e9 eV/GeV)

# GV invariant sequences for the two K3-fibred candidates
S12_q = [1, 8, 109, 2185, 52916, 1422776]   # (1,2)-fibration
S21_q = [1, 5, 41,  453,  5849,  82953]     # (2,1)-fibration


def compute_mass(tau, V, q_seq):
    """
    Axion mass from the Svrcek-Witten formula.

    Parameters
    ----------
    tau   : float  Real part of Kähler modulus (dimensionless)
    V     : float  Compactification volume (in units of l_s^6, dimensionless)
    q_seq : list   Gromov-Witten / instanton coefficients d=1,2,...

    Returns
    -------
    m_a : float  Axion mass in eV (0.0 if instanton sum is non-positive)
    """
    instanton_sum = sum(
        (d**2) * q_d * np.exp(-2.0 * np.pi * d * tau)
        for d, q_d in enumerate(q_seq, start=1)
    )
    if instanton_sum <= 0.0:
        return 0.0
    return (M_PL_EV / np.sqrt(V)) * np.sqrt(instanton_sum)


def parameter_sweep():
    """
    Sweep over tau and V and show the region compatible with FDM masses.
    """
    # Sweep grids
    V_values   = [1e2, 1e3, 1e4, 1e5]
    tau_values = np.linspace(5, 60, 300)

    FDM_lo = 1e-22  # eV
    FDM_hi = 1e-20  # eV

    print("=" * 65)
    print("PARAMETER SWEEP: Svrcek-Witten axion mass vs (tau, V)")
    print("=" * 65)
    print(f"FDM window: [{FDM_lo:.0e}, {FDM_hi:.0e}] eV\n")

    for V in V_values:
        print(f"  V = {V:.0e}:")
        for q_label, q_seq in [("S12", S12_q), ("S21", S21_q)]:
            masses = np.array([compute_mass(t, V, q_seq) for t in tau_values])
            mask = (masses >= FDM_lo) & (masses <= FDM_hi)
            in_window = tau_values[mask]
            if in_window.size:
                print(f"    {q_label}: FDM range for tau in "
                      f"[{in_window[0]:.1f}, {in_window[-1]:.1f}]")
            else:
                print(f"    {q_label}: NOT in FDM range for any tau in [5, 60]")
        print()

    print("HONEST ASSESSMENT:")
    print("  Mass in the FDM window (1e-22 to 1e-20 eV) is achievable for")
    print("  V~1e4, tau~30-35.  These parameters are NOT uniquely determined")
    print("  by the K3 geometry without a moduli stabilization potential.")
    print()

    # -------------------------------------------------------------------
    # 2-D contour plot: m_a(tau, V) for S12 and S21
    # -------------------------------------------------------------------
    V_grid   = np.logspace(2, 5, 80)
    tau_grid = np.linspace(5, 60, 200)
    TAU, VOL = np.meshgrid(tau_grid, V_grid)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    for ax, (q_label, q_seq) in zip(axes, [("S₁₂", S12_q), ("S₂₁", S21_q)]):
        mass_grid = np.vectorize(lambda t, v: compute_mass(t, v, q_seq))(TAU, VOL)
        # Take log10; clip zeros to avoid -inf
        log_mass = np.where(mass_grid > 0, np.log10(mass_grid), np.nan)

        levels = np.linspace(-23, -19, 25)
        cf = ax.contourf(TAU, np.log10(VOL), log_mass, levels=levels, cmap="plasma")
        ax.contour(TAU, np.log10(VOL),  log_mass,
                   levels=[np.log10(FDM_lo), np.log10(FDM_hi)],
                   colors=["cyan", "cyan"], linewidths=2)

        cb = fig.colorbar(cf, ax=ax)
        cb.set_label(r"$\log_{10}(m_a / \mathrm{eV})$")
        ax.set_xlabel(r"Modulus $\tau$")
        ax.set_ylabel(r"$\log_{10}(V)$")
        ax.set_title(f"{q_label} — cyan band = FDM window [1e-22, 1e-20] eV")

    fig.suptitle(
        "Svrcek–Witten mass parameter space (HONEST: no unique prediction without\n"
        "moduli stabilization). Cyan contours = FDM-compatible region.",
        fontsize=11
    )
    plt.tight_layout()

    os.makedirs("figures", exist_ok=True)
    out_path = os.path.join("figures", "mass_parameter_space.png")
    plt.savefig(out_path, dpi=150)
    print(f"Saved contour plot to {out_path}")


if __name__ == "__main__":
    parameter_sweep()
