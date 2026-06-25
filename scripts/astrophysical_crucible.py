#!/usr/bin/env python3
import json
import numpy as np
import os
import zipfile
import io
import urllib.request
import ssl
from fractions import Fraction
from scipy.optimize import curve_fit
from scipy.integrate import quad

# --- CONSTANTS ---
G_kpc = 4.3009e-6  # kpc M_sun^-1 (km/s)^2
G_pc = 4.3009e-3   # pc M_sun^-1 (km/s)^2
rho_local = 0.0105  # M_sun / pc^3
v_rel = 200.0      # km/s
t_age_years = 3e9  # 3 Gyr
m_a_s20 = 1.71e-23  # eV

# --- GD-1 SURVIVAL TEST ---
def compute_gd1_heating(m_a):
    if m_a <= 0:
        return float('inf'), float('inf')
    # lambda_dB = 1.9e3 * (1e-22 / m_a) * (200.0 / v_rel)  # in pc
    # wait, from candelas_chameleon_mass.py:
    lambda_dB = 1.9e3 * (1e-22 / m_a) * (200.0 / v_rel)
    M_g = rho_local * lambda_dB**3
    ln_lambda = 3.0
    heating_rate_astrounits = 8 * np.pi * G_pc**2 * rho_local * M_g * ln_lambda / v_rel
    t_astro = t_age_years / 9.778e5
    sigma_v = np.sqrt(heating_rate_astrounits * t_astro)
    return sigma_v, M_g

# --- SPARC CORE-CUSP FIT ---
def get_sparc_data():
    zip_path = "/tmp/Rotmod_LTG.zip"
    if not os.path.exists(zip_path):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        url = "https://zenodo.org/api/records/16284118/files/Rotmod_LTG.zip/content"
        print(f"Downloading SPARC dataset from {url}...")
        try:
            with urllib.request.urlopen(url, context=ctx) as response, open(zip_path, 'wb') as out_file:
                out_file.write(response.read())
        except Exception as e:
            print(f"Error downloading SPARC data: {e}")
            return None
            
    print("Extracting IC 2574 rotation curve data...")
    try:
        with zipfile.ZipFile(zip_path) as z:
            with z.open("IC2574_rotmod.dat") as f:
                content = f.read().decode('utf-8')
        data = np.loadtxt(io.StringIO(content), comments='#')
        return data
    except Exception as e:
        print(f"Error parsing SPARC data: {e}")
        return None

def fit_sparc_chi2(m_a, data):
    if data is None or m_a <= 0:
        return float('inf')
    
    r_data = data[:, 0]
    v_data = data[:, 1]
    v_err = data[:, 2]
    v_gas = data[:, 3]
    v_disk = data[:, 4]
    
    v_bar = np.sqrt(np.clip(v_gas**2 + 0.5 * v_disk**2, 0, None))
    m_a_22 = m_a / 1e-22
    
    def v_fdm_fixed(r, rho_c):
        r_c = (1.9e7 / (rho_c * m_a_22**2))**0.25
        def integrand(x):
            return x**2 / (1 + 0.091 * (x / r_c)**2)**8
        v_out = np.zeros_like(r)
        for i, rad in enumerate(r):
            integral, _ = quad(integrand, 0, rad)
            M_dm = 4 * np.pi * rho_c * integral
            v_dm2 = G_kpc * M_dm / rad
            v_out[i] = np.sqrt(np.clip(v_bar[i]**2 + v_dm2, 0, None))
        return v_out
        
    try:
        popt, pcov = curve_fit(v_fdm_fixed, r_data, v_data, sigma=v_err, p0=[1e6], bounds=([1e3], [1e10]))
        v_fit = v_fdm_fixed(r_data, *popt)
        chi2 = np.sum(((v_data - v_fit) / v_err)**2)
        return float(chi2)
    except Exception as e:
        print(f"Fitting error for m_a={m_a:.2e}: {e}")
        return float('inf')

def run_crucible():
    # Load math results
    with open("scripts/benchmark_math_results.json", "r") as f:
        math_results = json.load(f)
        
    # Get S20 baseline
    s20_C1 = float(Fraction(math_results["S20"]["C1"]))
    s20_Omega = float(Fraction(math_results["S20"]["Omega"]))
    s20_ratio = s20_C1 / s20_Omega
    
    sparc_data = get_sparc_data()
    
    final_results = {}
    
    for name, data in math_results.items():
        print(f"\nEvaluating {name}...")
        
        is_conv = data["is_conv"]
        if not is_conv and name != "S20":
            print(f"  Sequence {name} is Geometrically Ill-Defined (fails convergence). Excluding.")
            final_results[name] = {
                "status": "Geometrically Ill-Defined",
                "m_a": None,
                "gd1_sigma": None,
                "gd1_pass": "Excluded",
                "sparc_chi2": None
            }
            continue
            
        C1 = float(Fraction(data["C1"]))
        Omega = float(Fraction(data["Omega"]))
        ratio = C1 / Omega
        
        # normalized ratio mass scaling
        # m_a_new = m_a_s20 * sqrt(ratio_new / ratio_s20)
        m_a = m_a_s20 * np.sqrt(ratio / s20_ratio)
        print(f"  Derived m_a: {m_a:.2e} eV")
        
        # Fast filter
        # check if m_a is in [1.0e-22, 1.0e-20]
        in_goldilocks = (1.0e-22 <= m_a <= 1.0e-20)
        print(f"  In Goldilocks (1e-22 to 1e-20 eV): {in_goldilocks}")
        
        # GD-1 heating test
        gd1_sigma, M_g = compute_gd1_heating(m_a)
        gd1_pass = "Pass" if gd1_sigma < 5.0 else "Fail"
        print(f"  GD-1 heating dispersion: {gd1_sigma:.2f} km/s (Survival: {gd1_pass})")
        
        # SPARC fit
        chi2 = fit_sparc_chi2(m_a, sparc_data)
        print(f"  SPARC core-cusp fit chi^2: {chi2:.2f}")
        
        final_results[name] = {
            "status": "Valid",
            "m_a": float(m_a),
            "gd1_sigma": float(gd1_sigma),
            "gd1_pass": gd1_pass,
            "sparc_chi2": float(chi2) if chi2 != float('inf') else None
        }
        
    with open("scripts/benchmark_crucible_results.json", "w") as f:
        json.dump(final_results, f, indent=4)
    print("\nCrucible results successfully written to scripts/benchmark_crucible_results.json")

if __name__ == "__main__":
    run_crucible()
