import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 4.3009e-3  # (pc/M_sun) (km/s)^2
rho_local = 0.0105  # M_sun / pc^3  (0.4 GeV/cm^3) for MW at solar circle / GD-1 radius
v_rel = 200.0  # km/s
t_age_years = 3e9  # 3 Gyr stream age
sigma_obs = 2.0  # km/s (GD-1 observed limit)

m_a_dwarf = 1.71e-23  # eV (mass needed for dwarf galaxies)

def compute_heating(m_a):
    """Calculate the velocity dispersion increase squared (km/s)^2 over 3 Gyr."""
    lambda_dB = 1.9e3 * (1e-22 / m_a) * (200.0 / v_rel)  # in pc
    M_g = rho_local * lambda_dB**3
    ln_lambda = 3.0
    heating_rate_astrounits = 8 * np.pi * G**2 * rho_local * M_g * ln_lambda / v_rel
    t_astro = t_age_years / 9.778e5
    return np.sqrt(heating_rate_astrounits * t_astro), M_g

# Sweep across axion masses
m_a_range = np.logspace(-24, -19, 500)
sigma_v_vals = []
M_g_vals = []

for ma in m_a_range:
    sig, Mg = compute_heating(ma)
    sigma_v_vals.append(sig)
    M_g_vals.append(Mg)

sigma_v_vals = np.array(sigma_v_vals)
M_g_vals = np.array(M_g_vals)

# Find minimum mass required to keep sigma_v < sigma_obs
valid_indices = np.where(sigma_v_vals < sigma_obs)[0]
if len(valid_indices) > 0:
    required_m_a = m_a_range[valid_indices[0]]
    required_Mg = M_g_vals[valid_indices[0]]
else:
    required_m_a = np.nan
    required_Mg = np.nan

print(f"To satisfy GD-1 stream limit (\u0394\u03c3_v < {sigma_obs} km/s):")
print(f"Required Milky Way local mass: m_a >= {required_m_a:.2e} eV")
print(f"Maximum allowable granule mass: M_g <= {required_Mg:.2e} M_sun")

# Compute the Potential Scaling Index alpha
# Phi ~ V_rot^2
phi_mw = 220.0**2
phi_dwarf = 30.0**2

# m_a_mw = m_a_dwarf * (phi_mw / phi_dwarf)^alpha
# ln(m_a_mw / m_a_dwarf) = alpha * ln(phi_mw / phi_dwarf)
if not np.isnan(required_m_a):
    alpha = np.log(required_m_a / m_a_dwarf) / np.log(phi_mw / phi_dwarf)
    print(f"\nChameleon Potential Scaling:")
    print(f"If m_a \u221d |\u03a6|^\u03b1, the required index is \u03b1 \u2248 {alpha:.2f}")

# Plotting
plt.figure(figsize=(9, 6))

plt.plot(m_a_range, sigma_v_vals, 'b-', lw=2, label='Predicted GD-1 Thickening (3 Gyr)')
plt.axhline(sigma_obs, color='r', linestyle='--', lw=2, label='GD-1 Observational Limit (2 km/s)')

plt.axvline(m_a_dwarf, color='gray', linestyle=':', lw=2, label=f'Rigid Dwarf Mass ($1.71 \\times 10^{{-23}}$ eV)')
plt.axvline(required_m_a, color='green', linestyle='--', lw=2, label=f'Required MW Mass (>{required_m_a:.1e} eV)')

# Highlight the excluded region
plt.fill_betweenx([0, 100], 1e-24, required_m_a, color='red', alpha=0.1, label='Excluded (Stream Disruption)')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Local Axion Mass $m_{a, local}$ (eV)', fontsize=14)
plt.ylabel('Velocity Dispersion $\\Delta \\sigma_v$ (km/s)', fontsize=14)
plt.title('Chameleon Axion: Escaping Stellar Stream Destruction', fontsize=16)
plt.legend(fontsize=11)
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.ylim(0.1, 100)
plt.xlim(1e-24, 1e-19)

# Add text box for alpha
plt.text(1e-21, 20, f'Chameleon Scaling:\n$m_a \\propto |\\Phi|^{{{alpha:.2f}}}$\n$\\Phi_{{MW}}/\\Phi_{{dwarf}} \\approx 54$', 
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))

plt.savefig('/Users/xcallens/xdev/SocrateAI-Scientific-Agora/scripts/chameleon_mass_threshold.png', dpi=150, bbox_inches='tight')
print("\nSaved plot to scripts/chameleon_mass_threshold.png")
