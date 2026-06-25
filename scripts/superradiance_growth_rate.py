import numpy as np
import matplotlib.pyplot as plt
import os

M_sun_kg = 1.989e30
eV_to_J = 1.602e-19
c = 3e8
hbar = 1.054e-34
G = 6.674e-11
yr_to_sec = 3.154e7

def true_growth_rate(m_a_eV, M_bh_Msun, a_star, chameleon=True):
    M_bh_kg = M_bh_Msun * M_sun_kg
    m_a_kg = m_a_eV * eV_to_J / c**2
    alpha_bare = G * M_bh_kg * m_a_kg / (hbar * c)
    
    chameleon_boost = (1.0 + 1e4)**0.25 if chameleon else 1.0
    alpha_eff = alpha_bare * chameleon_boost
    
    mu = (m_a_kg * chameleon_boost) * c**2 / hbar
    r_plus_normalized = 1.0 + np.sqrt(np.clip(1.0 - a_star**2, 0, 1.0))
    threshold_term = a_star - 2.0 * alpha_eff * r_plus_normalized
    
    if threshold_term <= 0:
        return 0.0 # Absorbed by horizon
        
    return (1.0 / 24.0) * (alpha_eff**5) * mu * threshold_term

def main():
    M_m87 = 6.5e9
    m_as = np.logspace(-22, -20, 100)
    a_stars = np.linspace(0.01, 0.99, 100)
    M, A = np.meshgrid(m_as, a_stars)
    tau_sr = np.zeros_like(M)
    
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            Gamma = true_growth_rate(M[i,j], M_m87, A[i,j], chameleon=True)
            tau_sr[i,j] = 1.0 / Gamma if Gamma > 0 else np.inf
                
    threshold_sec = 1e10 * yr_to_sec
    exclusion = tau_sr < threshold_sec
    
    plt.figure(figsize=(8, 6))
    plt.contourf(M, A, exclusion, levels=[0.5, 1.5], colors=['red'], alpha=0.3)
    plt.axhline(0.90, color='black', linestyle='--', label='M87* Spin (a* ~ 0.90)')
    plt.xscale('log')
    plt.xlabel('Bare Axion Mass $m_a$ (eV)')
    plt.ylabel('Black Hole Spin $a_*$')
    plt.title('Superradiance Exclusion Region (Chameleon Shielded)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    os.makedirs('figures', exist_ok=True)
    plt.savefig('figures/superradiance_exclusion.png', dpi=150)
    print("Saved plot to figures/superradiance_exclusion.png")

if __name__ == "__main__":
    main()
