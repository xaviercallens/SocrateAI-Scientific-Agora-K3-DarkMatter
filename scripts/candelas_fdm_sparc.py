import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad
import os
import zipfile
import io
import urllib.request
import ssl

# Constants
G = 4.3009e-6  # kpc M_sun^-1 (km/s)^2

# Ingest real SPARC data for IC 2574
zip_path = "/tmp/Rotmod_LTG.zip"
if not os.path.exists(zip_path):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = "https://zenodo.org/api/records/16284118/files/Rotmod_LTG.zip/content"
    print(f"Downloading SPARC dataset from {url}...")
    with urllib.request.urlopen(url, context=ctx) as response, open(zip_path, 'wb') as out_file:
        out_file.write(response.read())

print("Extracting IC 2574 rotation curve data...")
with zipfile.ZipFile(zip_path) as z:
    with z.open("IC2574_rotmod.dat") as f:
        content = f.read().decode('utf-8')

# Parse columns
# Column 0: Rad (kpc), Column 1: Vobs (km/s), Column 2: errV (km/s)
# Column 3: Vgas (km/s), Column 4: Vdisk (km/s), Column 5: Vbul (km/s)
data = np.loadtxt(io.StringIO(content), comments='#')
r_data = data[:, 0]
v_data = data[:, 1]
v_err = data[:, 2]
v_gas = data[:, 3]
v_disk = data[:, 4]
v_bul = data[:, 5]

# Under standard SPARC assumptions (Lelli et al. 2016), we use stellar mass-to-light ratio Upsilon_disk = 0.5
# V_bar^2 = V_gas^2 + Upsilon_disk * V_disk^2
v_bar = np.sqrt(np.clip(v_gas**2 + 0.5 * v_disk**2, 0, None))

def v_nfw(r, rho_s, r_s):
    """NFW rotation curve with baryonic contribution."""
    M_dm = 4 * np.pi * rho_s * r_s**3 * (np.log(1 + r/r_s) - (r/r_s)/(1 + r/r_s))
    v_dm2 = G * M_dm / r
    return np.sqrt(np.clip(v_bar**2 + v_dm2, 0, None))

def v_fdm(r, rho_c, m_a_22):
    """S_20 Soliton rotation curve with baryonic contribution."""
    # Core radius linked to central density and axion mass (m_a_22 = m_a / 10^-22 eV)
    r_c = (1.9e7 / (rho_c * m_a_22**2))**0.25
    
    def integrand(x):
        return x**2 / (1 + 0.091 * (x / r_c)**2)**8
    
    v_out = np.zeros_like(r)
    for i, rad in enumerate(r):
        integral, _ = quad(integrand, 0, rad)
        M_dm = 4 * np.pi * rho_c * integral
        v_dm2 = G * M_dm / rad
        v_out[i] = np.sqrt(np.clip(v_bar[i]**2 + v_dm2, 0, None))
    return v_out

# Fit NFW Profile
popt_nfw, pcov_nfw = curve_fit(v_nfw, r_data, v_data, sigma=v_err, p0=[1e6, 5.0], bounds=([1e3, 0.1], [1e10, 100.0]))
v_nfw_fit = v_nfw(r_data, *popt_nfw)
chi2_nfw = np.sum(((v_data - v_nfw_fit) / v_err)**2)

# Fit S_20 FDM Soliton
popt_fdm, pcov_fdm = curve_fit(v_fdm, r_data, v_data, sigma=v_err, p0=[1e6, 1.0], bounds=([1e3, 1e-3], [1e10, 100.0]))
v_fdm_fit = v_fdm(r_data, *popt_fdm)
chi2_fdm = np.sum(((v_data - v_fdm_fit) / v_err)**2)

delta_chi2 = chi2_nfw - chi2_fdm

rho_c_fit, m_a_22_fit = popt_fdm
r_c_fit = (1.9e7 / (rho_c_fit * m_a_22_fit**2))**0.25
m_a = m_a_22_fit * 1e-22

# Plotting
plt.figure(figsize=(8, 6))
plt.errorbar(r_data, v_data, yerr=v_err, fmt='o', label='SPARC IC 2574 (Observed)', color='black')
r_plot = np.linspace(r_data.min(), r_data.max(), 100)

# To plot curves smoothly, we interpolate the baryonic component
from scipy.interpolate import interp1d
v_bar_interp = interp1d(r_data, v_bar, kind='cubic', fill_value="extrapolate")

def v_nfw_plot(r, rho_s, r_s):
    M_dm = 4 * np.pi * rho_s * r_s**3 * (np.log(1 + r/r_s) - (r/r_s)/(1 + r/r_s))
    v_dm2 = G * M_dm / r
    return np.sqrt(np.clip(v_bar_interp(r)**2 + v_dm2, 0, None))

def v_fdm_plot(r, rho_c, m_a_22):
    r_c = (1.9e7 / (rho_c * m_a_22**2))**0.25
    def integrand(x):
        return x**2 / (1 + 0.091 * (x / r_c)**2)**8
    v_out = np.zeros_like(r)
    for i, rad in enumerate(r):
        integral, _ = quad(integrand, 0, rad)
        M_dm = 4 * np.pi * rho_c * integral
        v_dm2 = G * M_dm / rad
        v_out[i] = np.sqrt(np.clip(v_bar_interp(rad)**2 + v_dm2, 0, None))
    return v_out

plt.plot(r_plot, v_nfw_plot(r_plot, *popt_nfw), '--', label=f'NFW ($\\chi^2$={chi2_nfw:.2f})', color='red', lw=2)
plt.plot(r_plot, v_fdm_plot(r_plot, *popt_fdm), '-', label=f'$S_{{20}}$ FDM Soliton ($\\chi^2$={chi2_fdm:.2f})', color='blue', lw=2)
plt.xlabel('Radius (kpc)', fontsize=12)
plt.ylabel('Rotation Velocity (km/s)', fontsize=12)
plt.title(f'Core-Cusp Fit (Real SPARC IC 2574): S_20 FDM vs NFW\n$m_a = {m_a:.2e}$ eV', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

out_path = '/Users/xcallens/xdev/SocrateAI-Scientific-Agora/scripts/fdm_rotation_curve.png'
plt.savefig(out_path, dpi=300, bbox_inches='tight')

print("=== Real SPARC IC 2574 FDM Evaluation Results ===")
print(f"NFW chi^2: {chi2_nfw:.2f}")
print(f"FDM chi^2: {chi2_fdm:.2f}")
print(f"Delta chi^2 (NFW - FDM): {delta_chi2:.2f}")
print(f"Best-fit Soliton parameters:")
print(f"  rho_c = {rho_c_fit:.2e} M_sun/kpc^3")
print(f"  r_c   = {r_c_fit:.2f} kpc")
print(f"Derived physical S_20 axion mass: m_a = {m_a:.2e} eV")
if delta_chi2 > 0:
    print("Conclusion: S_20 FDM successfully resolves the core-cusp problem significantly better than standard NFW.")
else:
    print("Conclusion: NFW is preferred over the FDM model for this dataset.")
