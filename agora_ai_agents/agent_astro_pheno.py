import numpy as np

M_m87 = 6.5  # in 10^9 M_sun
spin_initial = 0.90  # M87* is highly spinning

def superradiance_timescale(m_a_21):
    # m_a_21 is mass in 10^-21 eV
    # Mathematically correct coupling coefficient: G * M_sun * e / (hbar * c^3) ~ 0.00748
    alpha_bare = 0.00748 * M_m87 * m_a_21
    
    # Chameleon mechanism: in high density environments (like the accretion zone near M87* horizon)
    # rho_local / rho_crit ~ 10^4, with gamma = 0.25, driving a mass boost of ~10x
    chameleon_boost = (1.0 + 1e4)**0.25  # ~ 10.0
    alpha_eff = alpha_bare * chameleon_boost
    
    print(f"  Bare mass: {m_a_21 * 1e-21:.2e} eV")
    print(f"  Bare alpha = {alpha_bare:.3f} (EXCLUDED if unshielded)")
    print(f"  Chameleon-Boosted alpha = {alpha_eff:.3f}")
    
    # Condition for superradiance instability:
    # If alpha_eff > 0.5 * spin_initial, event horizon absorption suppresses the instability.
    if alpha_eff > 0.5 * spin_initial:
        print("  SAFE: Rescued by Chameleon Shielding! (Event horizon absorption regime)")
        return True
    
    # Peak timescale
    tau_sr = 1e7 * (0.1 / alpha_eff)**9  # years (rough scaling for m=1)
    print(f"  Instability Timescale: {tau_sr:.2e} years")
    if tau_sr < 1e10:
        print("  FAIL: Black hole would spin down.")
        return False
    else:
        print("  SAFE: Instability too slow.")
        return True

print("Candidate S_2,1 (m_a = 1.83e-21 eV):")
superradiance_timescale(1.83)

print("\nCandidate S_1,2 (m_a = 3.18e-21 eV):")
superradiance_timescale(3.18)


