import numpy as np
import matplotlib.pyplot as plt

# Constants
m0 = 1.71e-23  # eV
rho_mw_solar = 0.08  # M_sun / pc^3
rho_ic_core = 0.001  # M_sun / pc^3
target_mw_mass = 1.0e-21  # eV
target_ic_mass = 1.71e-23  # eV

def m_eff(rho_b, rho_crit, gamma):
    return m0 * (1.0 + rho_b / rho_crit)**gamma

def log_likelihood(theta):
    log_rho_crit, gamma = theta
    rho_crit = 10**log_rho_crit
    
    if gamma <= 0 or rho_crit <= 0 or log_rho_crit > 2 or log_rho_crit < -5:
        return -np.inf
        
    m_mw = m_eff(rho_mw_solar, rho_crit, gamma)
    m_ic = m_eff(rho_ic_core, rho_crit, gamma)
    
    # Penalize Milky Way (must be >= 1e-21 to save streams)
    mw_penalty = 0.0
    if m_mw < target_mw_mass:
        mw_penalty = -0.5 * ((m_mw - target_mw_mass) / 1e-22)**2
        
    # Penalize IC 2574 (must be close to 1.71e-23 to maintain cores)
    # We use a 5% tolerance on m0
    ic_penalty = -0.5 * ((m_ic - m0) / (0.05 * m0))**2
    
    # Add a small regularizer to gamma to prefer smaller, more natural couplings
    reg_penalty = -0.5 * (gamma / 5.0)**2
    
    return mw_penalty + ic_penalty + reg_penalty

# Simple MCMC (Metropolis-Hastings)
n_steps = 20000
theta_current = np.array([-2.0, 1.5])  # initial guess: rho_crit=0.01, gamma=1.5
logL_current = log_likelihood(theta_current)

samples = []

for i in range(n_steps):
    theta_prop = theta_current + np.random.normal(0, [0.1, 0.1])
    logL_prop = log_likelihood(theta_prop)
    
    if logL_prop > logL_current or np.log(np.random.rand()) < (logL_prop - logL_current):
        theta_current = theta_prop
        logL_current = logL_prop
        
    samples.append(theta_current)

samples = np.array(samples[5000:])  # discard burn-in
best_log_rho_crit, best_gamma = np.mean(samples, axis=0)
best_rho_crit = 10**best_log_rho_crit

print("=== MCMC Optimization Complete ===")
print(f"Best fit rho_crit: {best_rho_crit:.4f} M_sun/pc^3")
print(f"Best fit gamma: {best_gamma:.4f}")
print(f"Milky Way Mass (R=8 kpc): {m_eff(rho_mw_solar, best_rho_crit, best_gamma):.2e} eV")
print(f"IC 2574 Mass (R=0 kpc): {m_eff(rho_ic_core, best_rho_crit, best_gamma):.2e} eV")

# Generate Spatial Mass Mapping
R_mw = np.linspace(0, 20, 100)  # kpc
rho_b_mw = 1.15 * np.exp(-R_mw / 3.0)  # Exponential disk approx
m_mw_spatial = m_eff(rho_b_mw, best_rho_crit, best_gamma)

R_ic = np.linspace(0, 10, 100)  # kpc
rho_b_ic = 0.005 * np.exp(-R_ic / 2.0)
m_ic_spatial = m_eff(rho_b_ic, best_rho_crit, best_gamma)

fig, ax1 = plt.subplots(figsize=(10, 6))

color1 = 'tab:blue'
ax1.set_xlabel('Galactocentric Radius R (kpc)', fontsize=14)
ax1.set_ylabel('Milky Way Axion Mass $m_{eff}$ (eV)', color=color1, fontsize=14)
ax1.plot(R_mw, m_mw_spatial, color=color1, lw=2, label='Milky Way (GD-1 Shielding)')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.axhline(1e-21, color=color1, linestyle='--', alpha=0.5, label='Stream Survival Limit ($10^{-21}$ eV)')
ax1.set_yscale('log')
ax1.set_ylim(1e-23, 1e-19)

ax2 = ax1.twinx()  
color2 = 'tab:red'
ax2.set_ylabel('IC 2574 Axion Mass $m_{eff}$ (eV)', color=color2, fontsize=14)
ax2.plot(R_ic, m_ic_spatial, color=color2, lw=2, label='IC 2574 (Dwarf Core)')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.axhline(1.71e-23, color=color2, linestyle=':', alpha=0.5, label='Rigid $S_{20}$ Topological Mass')
ax2.set_yscale('log')
ax2.set_ylim(1e-23, 1e-19)

fig.suptitle(f'Chameleon Modulus Spatial Mapping\n$\\rho_{{crit}} = {best_rho_crit:.4f} \\, M_\\odot/\\text{{pc}}^3$, $\\gamma = {best_gamma:.2f}$', fontsize=16)

# Combine legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', fontsize=10)

plt.grid(True, which="both", ls="--", alpha=0.3)
plt.savefig('/Users/xcallens/xdev/SocrateAI-Scientific-Agora/scripts/chameleon_spatial_mapping.png', dpi=150, bbox_inches='tight')
print("Saved spatial mapping to scripts/chameleon_spatial_mapping.png")
