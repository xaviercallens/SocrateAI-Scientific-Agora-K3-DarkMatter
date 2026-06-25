import numpy as np
import emcee
import scipy.integrate as integrate
from scipy.optimize import minimize
import json
import os
import time
import warnings
warnings.filterwarnings('ignore')

def compute_observables(h, omega_c, log10_zc, f_EDE, theta_i):
    omega_b = 0.02236
    omega_m = omega_b + omega_c
    omega_r = 4.183e-5
    omega_gamma = 2.469e-5
    
    zc = 10**log10_zc
    xc = -np.log(1 + zc)
    x_star = -np.log(1 + 1090.0)
    
    Hc2 = omega_r * np.exp(-4*xc) + omega_m * np.exp(-3*xc)
    rho_tot_c = Hc2 / (1.0 - f_EDE)
    
    qs = [1, 9, 165]
    V_i = sum(q * (1 - np.cos(n * theta_i)) for n, q in enumerate(qs, 1))
    
    if V_i < 1e-6:
        return -np.inf, -np.inf
        
    Lambda4 = f_EDE * rho_tot_c / V_i
    f2 = Lambda4 * 1522.0 / (9.0 * rho_tot_c)
    f = np.sqrt(f2)
    
    def V_dV(phi):
        theta = phi / f
        v = Lambda4 * sum(q * (1 - np.cos(n * theta)) for n, q in enumerate(qs, 1))
        dv = (Lambda4 / f) * sum(q * n * np.sin(n * theta) for n, q in enumerate(qs, 1))
        return v, dv
        
    omega_Lambda = h**2 - omega_r - omega_m
    
    def derivs(x, state):
        phi, y = state
        v, dv = V_dV(phi)
        rho_bg = omega_r * np.exp(-4*x) + omega_m * np.exp(-3*x) + omega_Lambda
        y_sq = min(y**2, 5.999)
        H2 = (rho_bg + v) / (1.0 - y_sq / 6.0)
        if H2 < 0: return [0, 0]
        p_tot = omega_r * np.exp(-4*x)/3.0 - omega_Lambda - v + H2 * y_sq / 6.0
        H_prime_over_H = -1.5 * (1.0 + p_tot / H2)
        dy_dx = - (3.0 + H_prime_over_H) * y - dv / H2
        return [y, dy_dx]

    x_start = -14.0
    state0 = [theta_i * f, 0.0]
    
    res = integrate.solve_ivp(derivs, (x_start, x_star), state0, method='Radau', 
                              dense_output=True, rtol=1e-4, atol=1e-5)
                              
    if not res.success:
        return -np.inf, -np.inf
        
    phi_star, y_star = res.sol(x_star)
    v_star, _ = V_dV(phi_star)
    rho_bg_star = omega_r * np.exp(-4*x_star) + omega_m * np.exp(-3*x_star) + omega_Lambda
    y_sq_star = min(y_star**2, 5.999)
    H2_star = (rho_bg_star + v_star) / (1.0 - y_sq_star / 6.0)
    rho_phi_star = v_star + H2_star * y_sq_star / 6.0
    
    def H_func(x):
        if x <= x_star:
            state = res.sol(x)
            phi, y = state
            v, _ = V_dV(phi)
            rho_bg = omega_r * np.exp(-4*x) + omega_m * np.exp(-3*x) + omega_Lambda
            y_sq = min(y**2, 5.999)
            H2 = max((rho_bg + v) / (1.0 - y_sq / 6.0), 1e-10)
            return np.sqrt(H2)
        else:
            rho_phi = rho_phi_star * np.exp(-3 * (x - x_star))
            rho_bg = omega_r * np.exp(-4*x) + omega_m * np.exp(-3*x) + omega_Lambda
            return np.sqrt(max(rho_bg + rho_phi, 1e-10))
            
    chi_star, _ = integrate.quad(lambda x: np.exp(-x) / H_func(x), x_star, 0.0, epsrel=1e-4)
    R = np.sqrt(omega_m) * chi_star
    
    def integrand_rs(x):
        Rb = 3.0 * omega_b / (4.0 * omega_gamma) * np.exp(x)
        cs = 1.0 / np.sqrt(3.0 * (1.0 + Rb))
        return cs * np.exp(-x) / H_func(x)
        
    rs_star, _ = integrate.quad(integrand_rs, -12.0, x_star, epsrel=1e-4)
    theta_star = rs_star / chi_star
    
    return R, theta_star

def log_likelihood(theta):
    h, omega_c, log10_zc, f_EDE, theta_i = theta
    if not (0.6 < h < 0.8 and 0.05 < omega_c < 0.2 and 3.0 < log10_zc < 4.5 
            and 0.0 <= f_EDE < 0.2 and 0.1 < theta_i < 3.14):
        return -np.inf
        
    if f_EDE == 0.0:
        omega_b = 0.02236
        omega_m = omega_b + omega_c
        omega_r = 4.183e-5
        omega_gamma = 2.469e-5
        omega_Lambda = h**2 - omega_r - omega_m
        x_star = -np.log(1 + 1090.0)
        
        def H_lcdm(x):
            return np.sqrt(max(omega_r*np.exp(-4*x) + omega_m*np.exp(-3*x) + omega_Lambda, 1e-10))
            
        chi_star, _ = integrate.quad(lambda x: np.exp(-x)/H_lcdm(x), x_star, 0.0)
        R = np.sqrt(omega_m) * chi_star
        
        def integrand_rs(x):
            Rb = 3.0 * omega_b / (4.0 * omega_gamma) * np.exp(x)
            cs = 1.0 / np.sqrt(3.0 * (1.0 + Rb))
            return cs * np.exp(-x) / H_lcdm(x)
        rs_star, _ = integrate.quad(integrand_rs, -12.0, x_star)
        theta_star = rs_star / chi_star
    else:
        try:
            R, theta_star = compute_observables(h, omega_c, log10_zc, f_EDE, theta_i)
        except Exception:
            return -np.inf
            
    if R == -np.inf:
        return -np.inf
        
    chi2_R = ((R - 1.74963) / 0.0040)**2
    chi2_theta = ((100*theta_star - 1.0411) / 0.0003)**2
    chi2_H0 = ((h*100 - 73.04) / 1.04)**2
    
    return -0.5 * (chi2_R + chi2_theta + chi2_H0)

def run():
    print("Optimizing LCDM baseline...")
    def nll_lcdm(theta):
        h, omega_c = theta
        ll = log_likelihood([h, omega_c, 3.5, 0.0, 1.0])
        return -ll if ll != -np.inf else 1e10
        
    res_lcdm = minimize(nll_lcdm, [0.67, 0.12], method='Nelder-Mead')
    chi2_lcdm = 2.0 * res_lcdm.fun
    h_lcdm, omegac_lcdm = res_lcdm.x
    print(f"LCDM Best Fit: H0 = {h_lcdm*100:.2f}, omega_c = {omegac_lcdm:.4f}")
    print(f"LCDM chi2 = {chi2_lcdm:.2f}")

    print("\nOptimizing AEDE model (q1=1, q2=9, q3=165)...")
    def nll_aede(theta):
        ll = log_likelihood(theta)
        return -ll if ll != -np.inf else 1e10
        
    guess = [0.72, 0.13, 3.5, 0.1, 2.0]
    res_aede = minimize(nll_aede, guess, method='Nelder-Mead', options={'maxiter': 200})
    chi2_aede = 2.0 * res_aede.fun
    print(f"AEDE Best Fit: H0 = {res_aede.x[0]*100:.2f}, f_EDE = {res_aede.x[3]:.4f}, zc = {10**res_aede.x[2]:.0f}")
    print(f"AEDE chi2 = {chi2_aede:.2f}")
    print(f"Delta chi2 = {chi2_aede - chi2_lcdm:.2f}")

    print("\nRunning emcee MCMC...")
    ndim = 5
    nwalkers = 12
    nsteps = 25
    
    pos = res_aede.x + 1e-4 * np.random.randn(nwalkers, ndim)
    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_likelihood)
    t0 = time.time()
    sampler.run_mcmc(pos, nsteps, progress=False)
    t1 = time.time()
    print(f"MCMC finished in {t1-t0:.1f} seconds")
    
    samples = sampler.get_chain(discard=5, flat=True)
    best_idx = np.argmax(sampler.get_log_prob(discard=5, flat=True))
    best_theta = samples[best_idx]
    best_chi2 = -2.0 * log_likelihood(best_theta)
    
    results = {
        "lcdm_chi2": chi2_lcdm,
        "lcdm_H0": h_lcdm * 100,
        "aede_best_chi2": best_chi2,
        "aede_best_H0": best_theta[0] * 100,
        "delta_chi2": best_chi2 - chi2_lcdm,
        "best_params": {
            "h": best_theta[0],
            "omega_c": best_theta[1],
            "log10_zc": best_theta[2],
            "f_EDE": best_theta[3],
            "theta_i": best_theta[4]
        }
    }
    
    with open("scripts/mcmc_results.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Results saved to scripts/mcmc_results.json")

if __name__ == '__main__':
    run()
