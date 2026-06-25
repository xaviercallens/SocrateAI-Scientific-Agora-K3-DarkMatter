import classy
import numpy as np

cosmo = classy.Class()
# Try a fluid with w0 > 0 to simulate decaying DM
params = {
    'output': 'tCl, pCl, lCl, mPk',
    'l_max_scalars': 2000,
    'P_k_max_1/Mpc': 3.0,
    'Omega_b': 0.05,
    'Omega_cdm': 0.0,
    'Omega_fld': 0.26, # use fluid for DM
    'w0_fld': 0.041,   # mimics a^-3.123 scaling
    'wa_fld': 0.0,
    'h': 0.73          # forcing H0=73 to see if it's stable, or just leave it out to get the implied H0 given theta_s?
}
try:
    cosmo.set(params)
    cosmo.compute()
    print("H0 computed:", cosmo.h() * 100)
except Exception as e:
    print("Class error:", e)
