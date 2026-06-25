import numpy as np

M_m87 = 6.5  # in 10^9 M_sun
spin_initial = 0.90  # M87* is highly spinning
yr_to_sec = 3.154e7
M_sun_kg = 1.989e30
eV_to_J = 1.602e-19
c = 3e8
hbar = 1.054e-34
G = 6.674e-11

def superradiance_timescale(m_a_21):
    alpha_bare = 0.00748 * M_m87 * m_a_21
    chameleon_boost = (1.0 + 1e4)**0.25
    alpha_eff = alpha_bare * chameleon_boost
    
    print(f"  Bare mass: {m_a_21 * 1e-21:.2e} eV")
    print(f"  Bare alpha = {alpha_bare:.3f} (EXCLUDED if unshielded)")
    print(f"  Chameleon-Boosted alpha = {alpha_eff:.3f}")
    
    m_a_eV = m_a_21 * 1e-21
    m_a_kg = m_a_eV * eV_to_J / c**2
    mu = (m_a_kg * chameleon_boost) * c**2 / hbar
    r_plus_normalized = 1.0 + np.sqrt(np.clip(1.0 - spin_initial**2, 0, 1.0))
    threshold_term = spin_initial - 2.0 * alpha_eff * r_plus_normalized

    if threshold_term <= 0:
        print("  SAFE: Rescued by Chameleon Shielding! (Event horizon absorption regime)")
        return True
    
    Gamma = (1.0 / 24.0) * (alpha_eff**5) * mu * threshold_term
    tau_sr = 1.0 / Gamma if Gamma > 0 else np.inf
    
    print(f"  Instability Timescale: {tau_sr / yr_to_sec:.2e} years")
    if tau_sr > 1e10 * yr_to_sec:
        print("  SAFE: Instability too slow.")
        return True
    else:
        print("  FAIL: Black hole would spin down.")
        return False

print("Candidate S_2,1 (m_a = 1.83e-21 eV):")
superradiance_timescale(1.83)

print("\nCandidate S_1,2 (m_a = 3.18e-21 eV):")
superradiance_timescale(3.18)
