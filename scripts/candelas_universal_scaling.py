import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, brentq
from scipy.integrate import quad
from scipy.interpolate import interp1d
import os
import zipfile
import io
import urllib.request
import ssl

# Constants
G = 4.3009e-6  # kpc M_sun^-1 (km/s)^2
rho_crit = 137.0  # M_sun / kpc^3 at z=0

# SPARC Galaxies to fit
galaxies = [
    "DDO154", "DDO168", "F563-1", "F568-3", "IC2574",
    "NGC2403", "NGC2903", "NGC3198", "NGC3741", "NGC3992",
    "NGC5055", "NGC6503", "NGC7331", "UGC00731", "UGC02259"
]

zip_path = "/tmp/Rotmod_LTG.zip"
if not os.path.exists(zip_path):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = "https://zenodo.org/api/records/16284118/files/Rotmod_LTG.zip/content"
    print(f"Downloading SPARC dataset from {url}...")
    with urllib.request.urlopen(url, context=ctx) as response, open(zip_path, 'wb') as out_file:
        out_file.write(response.read())

print("Precomputing soliton dimensionless integral...")
u_int, _ = quad(lambda u: u**2 / (1 + 0.091 * u**2)**8, 0, 1)

def get_m200(rho_s, r_s):
    """Calculate NFW halo virial mass M_200."""
    def f(x):
        val = 4 * np.pi * rho_s * r_s**3 * (np.log(1 + x/r_s) - (x/r_s)/(1 + x/r_s))
        return val - (4.0/3.0) * np.pi * 200.0 * rho_crit * x**3
    try:
        r200 = brentq(f, 1.0, 5000.0)
        return 4.0/3.0 * np.pi * 200.0 * rho_crit * r200**3
    except ValueError:
        return 4.0/3.0 * np.pi * 200.0 * rho_crit * (10.0 * r_s)**3

# Fit containers
results = {}

with zipfile.ZipFile(zip_path) as z:
    for gal in galaxies:
        print(f"Fitting {gal}...")
        with z.open(f"{gal}_rotmod.dat") as f:
            content = f.read().decode('utf-8')
        
        # Load columns
        data = np.loadtxt(io.StringIO(content), comments='#')
        r = data[:, 0]
        v = data[:, 1]
        v_err = data[:, 2]
        v_gas = data[:, 3]
        v_disk = data[:, 4]
        
        # Baryonic contribution
        v_bar = np.sqrt(np.clip(v_gas**2 + 0.5 * v_disk**2, 0, None))
        
        # Define model fit functions closed over v_bar
        def v_nfw_fit(r_arr, rho_s, r_s):
            M_dm = 4 * np.pi * rho_s * r_s**3 * (np.log(1 + r_arr/r_s) - (r_arr/r_s)/(1 + r_arr/r_s))
            v_dm2 = G * M_dm / r_arr
            return np.sqrt(np.clip(v_bar**2 + v_dm2, 0, None))

        def make_v_fdm_fit(m_a_val):
            m_a_22 = m_a_val * 1e22
            def v_fdm_fit(r_arr, rho_c):
                r_c = (1.9e7 / (rho_c * m_a_22**2))**0.25
                v_out = np.zeros_like(r_arr)
                for idx, rad in enumerate(r_arr):
                    integral, _ = quad(lambda x: x**2 / (1 + 0.091 * (x / r_c)**2)**8, 0, rad)
                    M_dm = 4 * np.pi * rho_c * integral
                    v_dm2 = G * M_dm / rad
                    v_out[idx] = np.sqrt(np.clip(v_bar[idx]**2 + v_dm2, 0, None))
                return v_out
            return v_fdm_fit

        # Fit standard NFW
        try:
            popt_nfw, _ = curve_fit(v_nfw_fit, r, v, sigma=v_err, p0=[1e6, 5.0], bounds=([1e3, 0.1], [1e10, 100.0]))
            v_nfw_pred = v_nfw_fit(r, *popt_nfw)
            chi2_nfw = np.sum(((v - v_nfw_pred) / v_err)**2)
            m_h = get_m200(popt_nfw[0], popt_nfw[1])
        except Exception as e:
            print(f"  NFW fit failed for {gal}: {e}")
            continue

        # Fit FDM Case A (m_a = 1.71e-23 eV)
        v_fdm_a = make_v_fdm_fit(1.71e-23)
        try:
            popt_fdm_a, _ = curve_fit(v_fdm_a, r, v, sigma=v_err, p0=[1e6], bounds=(1e3, 1e11))
            v_fdm_a_pred = v_fdm_a(r, *popt_fdm_a)
            chi2_fdm_a = np.sum(((v - v_fdm_a_pred) / v_err)**2)
            
            # Soliton Mass Case A
            rho_c_a = popt_fdm_a[0]
            r_c_a = (1.9e7 / (rho_c_a * (1.71e-23 * 1e22)**2))**0.25
            m_c_a = 4 * np.pi * rho_c_a * r_c_a**3 * u_int
        except Exception as e:
            print(f"  FDM A fit failed for {gal}: {e}")
            continue

        # Fit FDM Case B (m_a = 4.43e-24 eV)
        v_fdm_b = make_v_fdm_fit(4.43e-24)
        try:
            popt_fdm_b, _ = curve_fit(v_fdm_b, r, v, sigma=v_err, p0=[1e6], bounds=(1e3, 1e11))
            v_fdm_b_pred = v_fdm_b(r, *popt_fdm_b)
            chi2_fdm_b = np.sum(((v - v_fdm_b_pred) / v_err)**2)
            
            # Soliton Mass Case B
            rho_c_b = popt_fdm_b[0]
            r_c_b = (1.9e7 / (rho_c_b * (4.43e-24 * 1e22)**2))**0.25
            m_c_b = 4 * np.pi * rho_c_b * r_c_b**3 * u_int
        except Exception as e:
            print(f"  FDM B fit failed for {gal}: {e}")
            continue

        results[gal] = {
            "r": r, "v": v, "v_err": v_err, "v_bar": v_bar,
            "popt_nfw": popt_nfw, "chi2_nfw": chi2_nfw, "m_h": m_h,
            "popt_fdm_a": popt_fdm_a, "chi2_fdm_a": chi2_fdm_a, "m_c_a": m_c_a,
            "popt_fdm_b": popt_fdm_b, "chi2_fdm_b": chi2_fdm_b, "m_c_b": m_c_b
        }

# Global statistics
print("\n=== Global Fit Statistics ===")
total_chi2_nfw = sum(res["chi2_nfw"] for res in results.values())
total_chi2_a = sum(res["chi2_fdm_a"] for res in results.values())
total_chi2_b = sum(res["chi2_fdm_b"] for res in results.values())

print(f"Total NFW chi^2: {total_chi2_nfw:.2f}")
print(f"Total FDM Case A (1.71e-23 eV) chi^2: {total_chi2_a:.2f} (Delta chi^2 = {total_chi2_nfw - total_chi2_a:.2f})")
print(f"Total FDM Case B (4.43e-24 eV) chi^2: {total_chi2_b:.2f} (Delta chi^2 = {total_chi2_nfw - total_chi2_b:.2f})")

# Fit Scaling Laws
m_h_vals = np.array([res["m_h"] for res in results.values()])
m_c_a_vals = np.array([res["m_c_a"] for res in results.values()])
m_c_b_vals = np.array([res["m_c_b"] for res in results.values()])

# Fit Log(Mc) = A*Log(Mh) + B
p_a = np.polyfit(np.log10(m_h_vals), np.log10(m_c_a_vals), 1)
p_b = np.polyfit(np.log10(m_h_vals), np.log10(m_c_b_vals), 1)

print("\n=== Soliton-Halo Mass Scaling Fits ===")
print(f"Case A (1.71e-23 eV): Mc ~ Mh^{p_a[0]:.3f} (Theoretical expected: 0.333)")
print(f"Case B (4.43e-24 eV): Mc ~ Mh^{p_b[0]:.3f} (Theoretical expected: 0.333)")

# Grid Plot
fig, axes = plt.subplots(5, 3, figsize=(15, 20), sharex=False, sharey=False)
fig.suptitle("SPARC Multigalaxy Fit: Locked S_20 FDM vs NFW", fontsize=20, y=1.02)

for idx, (gal, res) in enumerate(results.items()):
    ax = axes[idx // 3, idx % 3]
    ax.errorbar(res["r"], res["v"], yerr=res["v_err"], fmt='o', color='black', alpha=0.6, ms=4)
    
    r_smooth = np.linspace(res["r"].min(), res["r"].max(), 100)
    v_bar_interp = interp1d(res["r"], res["v_bar"], kind='cubic', fill_value="extrapolate")
    
    # NFW pred
    M_dm_nfw = 4 * np.pi * res["popt_nfw"][0] * res["popt_nfw"][1]**3 * (np.log(1 + r_smooth/res["popt_nfw"][1]) - (r_smooth/res["popt_nfw"][1])/(1 + r_smooth/res["popt_nfw"][1]))
    v_nfw_smooth = np.sqrt(np.clip(v_bar_interp(r_smooth)**2 + G * M_dm_nfw / r_smooth, 0, None))
    ax.plot(r_smooth, v_nfw_smooth, '--', color='red', label=f'NFW ($\\chi^2$={res["chi2_nfw"]:.1f})')
    
    # FDM Case A pred
    m_a_22_a = 1.71e-23 * 1e22
    r_c_a = (1.9e7 / (res["popt_fdm_a"][0] * m_a_22_a**2))**0.25
    v_fdm_a_smooth = np.zeros_like(r_smooth)
    for i, rad in enumerate(r_smooth):
        integral, _ = quad(lambda x: x**2 / (1 + 0.091 * (x / r_c_a)**2)**8, 0, rad)
        v_fdm_a_smooth[i] = np.sqrt(np.clip(v_bar_interp(rad)**2 + G * 4 * np.pi * res["popt_fdm_a"][0] * integral / rad, 0, None))
    ax.plot(r_smooth, v_fdm_a_smooth, '-', color='blue', label=f'FDM A ($\\chi^2$={res["chi2_fdm_a"]:.1f})')

    # FDM Case B pred
    m_a_22_b = 4.43e-24 * 1e22
    r_c_b = (1.9e7 / (res["popt_fdm_b"][0] * m_a_22_b**2))**0.25
    v_fdm_b_smooth = np.zeros_like(r_smooth)
    for i, rad in enumerate(r_smooth):
        integral, _ = quad(lambda x: x**2 / (1 + 0.091 * (x / r_c_b)**2)**8, 0, rad)
        v_fdm_b_smooth[i] = np.sqrt(np.clip(v_bar_interp(rad)**2 + G * 4 * np.pi * res["popt_fdm_b"][0] * integral / rad, 0, None))
    ax.plot(r_smooth, v_fdm_b_smooth, '-', color='green', label=f'FDM B ($\\chi^2$={res["chi2_fdm_b"]:.1f})')
    
    ax.set_title(gal, fontsize=12)
    ax.set_xlabel("r (kpc)", fontsize=8)
    ax.set_ylabel("v (km/s)", fontsize=8)
    ax.legend(fontsize=7, loc='lower right')
    ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('/Users/xcallens/xdev/SocrateAI-Scientific-Agora/scripts/universal_scaling_curves.png', dpi=150, bbox_inches='tight')
print("\nSaved universal scaling visualization to /Users/xcallens/xdev/SocrateAI-Scientific-Agora/scripts/universal_scaling_curves.png")
