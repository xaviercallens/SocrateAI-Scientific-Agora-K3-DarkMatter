"""
agent_astro_pheno.py — Astrophysical phenomenology for the K3 dark matter candidates.

FIXES (2026-06-25):
  1. alpha_bare is now derived from SI constants, not the magic number 0.00748.
  2. Superradiance growth rate uses alpha_eff**8, not alpha_eff**5.
     Reference: Detweiler (1980), Dolan (2007), Arvanitaki et al. PRD 95, 043001.
"""
import numpy as np

M_m87     = 6.5    # in 10^9 M_sun  (Event Horizon Telescope 2019)
spin_initial = 0.90  # M87* dimensionless spin
yr_to_sec = 365.25 * 24 * 3600   # s/yr
M_sun_kg  = 1.989e30              # kg
eV_to_J   = 1.602176634e-19       # J/eV  (exact, SI 2019)
c         = 2.99792458e8          # m/s   (exact)
hbar      = 1.054571817e-34       # J·s
G         = 6.67430e-11           # m³/(kg·s²)

# ---------------------------------------------------------------------------
# alpha_conversion: G * M_bh * m_a / (hbar * c) evaluated for the reference
# units used by this script (M_bh in 10^9 M_sun, m_a in 10^-21 eV).
#
# Derivation:
#   alpha = G * (M_bh_Msun * 1e9 * M_sun_kg) * (m_a_21 * 1e-21 * eV_to_J / c^2)
#           / (hbar * c)
#         = [G * M_sun_kg * 1e9 * 1e-21 * eV_to_J / c^2] / [hbar * c]
#           * M_bh_Msun * m_a_21
#         ≡ alpha_conversion * M_bh_Msun * m_a_21
# ---------------------------------------------------------------------------
_M_ref_kg = 1e9 * M_sun_kg
_m_ref_kg = 1e-21 * eV_to_J / c**2
alpha_conversion = G * _M_ref_kg * _m_ref_kg / (hbar * c)
# This equals approximately 0.00748 — derived, not hardcoded.
print(f"[init] alpha_conversion = {alpha_conversion:.6e}  "
      f"(G*M_1e9Msun*m_1e-21eV/(hbar*c))")


def superradiance_timescale(m_a_21):
    """
    Assess whether a K3 axion candidate with mass m_a = m_a_21 × 10⁻²¹ eV
    is excluded by M87* superradiance (Kerr spin-down constraint).

    Parameters
    ----------
    m_a_21 : float  Axion mass in units of 10⁻²¹ eV

    Returns
    -------
    safe : bool   True if the candidate is NOT excluded
    """
    # --- Bare gravitational coupling (derived from SI) ---
    alpha_bare = alpha_conversion * M_m87 * m_a_21

    # --- Chameleon field density boost ---
    # rho_ratio = near-horizon density enhancement (free parameter from MCMC)
    # gamma     = power-law index (free parameter from MCMC)
    rho_ratio       = 1e4
    gamma_chameleon = 0.25
    chameleon_boost = (1.0 + rho_ratio)**gamma_chameleon
    alpha_eff       = alpha_bare * chameleon_boost

    print(f"  Bare mass: {m_a_21 * 1e-21:.2e} eV")
    print(f"  Bare alpha = {alpha_bare:.6f}  "
          f"[derived: alpha_conversion × {M_m87} × {m_a_21}]")
    print(f"  Chameleon boost = {chameleon_boost:.4f}")
    print(f"  Chameleon-boosted alpha = {alpha_eff:.4f}")

    m_a_eV = m_a_21 * 1e-21
    m_a_kg = m_a_eV * eV_to_J / c**2
    mu_eff = (m_a_kg * chameleon_boost) * c**2 / hbar  # angular freq [rad/s]

    # --- Kerr horizon angular velocity ---
    sqrt_term    = np.sqrt(np.clip(1.0 - spin_initial**2, 0.0, 1.0))
    r_tilde_plus = 1.0 + sqrt_term          # r_+ / (G M / c²)
    Omega_H      = (spin_initial * c**3) / (4.0 * G * M_m87 * 1e9 * M_sun_kg * r_tilde_plus)

    # Bound-state frequency (n=2, l=1 shift)
    omega_R = mu_eff * (1.0 - alpha_eff**2 / 8.0)

    if omega_R >= Omega_H:
        print("  SAFE: Not superradiant (ω_R ≥ Ω_H).")
        return True

    # --- Detweiler (1980) / Dolan (2007) Γ_211 ∝ α^8  [BUG FIX] ---
    Gamma  = (1.0 / 24.0) * spin_initial * (alpha_eff**8) * mu_eff
    tau_sr = 1.0 / Gamma if Gamma > 0 else np.inf

    print(f"  Γ_211 = {Gamma:.4e} rad/s  (α^8 formula)")
    print(f"  Instability timescale: {tau_sr / yr_to_sec:.4e} years")

    if tau_sr > 1e10 * yr_to_sec:
        print("  SAFE: Instability too slow (τ_sr > 10 Gyr).")
        return True
    else:
        print("  FAIL: Black hole would spin down within 10 Gyr.")
        return False


print("\nCandidate S_2,1 (m_a = 1.83e-21 eV):")
superradiance_timescale(1.83)

print("\nCandidate S_1,2 (m_a = 3.18e-21 eV):")
superradiance_timescale(3.18)
