import numpy as np
from scipy.integrate import solve_ivp
import json
import os

def integrate_trajectory(V0, lam, Omega_m0, Omega_r0):
    """
    Integrates the trajectory for a given V0 and lambda.
    Returns:
      omega_phi_final: Omega_phi at a=1
      w0: w at a=1
      wa: wa (CPL parameter)
      phi_final, phidot_final, a_final
    """
    Omega_phi0 = 1.0 - Omega_m0 - Omega_r0
    a_init = 1e-3
    
    # Initialize from rest (frozen field due to Hubble drag in early universe)
    phi_init = 0.0
    phidot_init = 0.0

    def H_func(a, phi, phidot):
        rho_m = 3.0 * Omega_m0 * a**(-3)
        rho_r = 3.0 * Omega_r0 * a**(-4)
        V = V0 * np.exp(-lam * phi)
        rho_phi = 0.5 * phidot**2 + V
        rho_tot = rho_m + rho_r + rho_phi
        return np.sqrt(rho_tot / 3.0)

    def ivp_sys(t, y):
        phi, phidot, a = y
        H = H_func(a, phi, phidot)
        V_prime = -lam * V0 * np.exp(-lam * phi)
        
        dphi_dt = phidot
        dphidot_dt = -3 * H * phidot - V_prime
        da_dt = a * H
        
        return [dphi_dt, dphidot_dt, da_dt]

    # Event to stop integration when a = 1
    def stop_at_a_one(t, y):
        return y[2] - 1.0
    stop_at_a_one.terminal = True
    stop_at_a_one.direction = 1

    sol = solve_ivp(ivp_sys, [0, 1000], [phi_init, phidot_init, a_init], 
                    method='Radau', events=stop_at_a_one, max_step=0.1, rtol=1e-8, atol=1e-8)
    
    # Extract values at a=1
    phi_final, phidot_final, a_final = sol.y[:, -1]
    
    H_final = H_func(a_final, phi_final, phidot_final)
    V_final = V0 * np.exp(-lam * phi_final)
    rho_phi_final = 0.5 * phidot_final**2 + V_final
    p_phi_final = 0.5 * phidot_final**2 - V_final
    
    omega_phi_final = rho_phi_final / (3.0 * H_final**2)
    w0 = p_phi_final / rho_phi_final
    
    # Compute wa analytically: dw/da at a=1
    V_prime_final = -lam * V0 * np.exp(-lam * phi_final)
    phidotdot_final = -3 * H_final * phidot_final - V_prime_final
    
    dp_dt = phidot_final * phidotdot_final - V_prime_final * phidot_final
    drho_dt = phidot_final * phidotdot_final + V_prime_final * phidot_final
    dw_dt = (dp_dt * rho_phi_final - p_phi_final * drho_dt) / (rho_phi_final**2)
    
    da_dt = a_final * H_final
    dw_da = dw_dt / da_dt
    wa = -dw_da
    
    return omega_phi_final, w0, wa, phi_final, phidot_final, a_final

def shoot_V0(lam, Omega_phi0, Omega_m0, Omega_r0):
    """
    Finds the V0 that yields Omega_phi(a=1) = Omega_phi0.
    """
    V0_low = 0.001
    V0_high = 20.0
    tol = 1e-6
    max_iter = 40
    
    for _ in range(max_iter):
        V0 = 0.5 * (V0_low + V0_high)
        try:
            omega_phi_final, _, _, _, _, _ = integrate_trajectory(V0, lam, Omega_m0, Omega_r0)
        except Exception:
            # If integration fails, reduce interval
            V0_high = V0
            continue
            
        if abs(omega_phi_final - Omega_phi0) < tol:
            return V0, omega_phi_final
            
        if omega_phi_final < Omega_phi0:
            V0_low = V0
        else:
            V0_high = V0
            
    return V0, omega_phi_final

def main():
    print("Initiating Vafa: DESI Quintessence ODE integration with Shooting V0...")
    
    # Load targets from data/observational_targets.json
    targets_path = "data/observational_targets.json"
    if not os.path.exists(targets_path):
        raise FileNotFoundError(f"Missing observational targets registry: {targets_path}")
        
    with open(targets_path, "r") as f:
        targets = json.load(f)
        
    target_w0 = targets["DESI_2024"]["w0"]
    target_wa = targets["DESI_2024"]["wa"]
    print(f"Loaded DESI 2024 targets: w0 = {target_w0}, wa = {target_wa}")
    
    # Cosmological parameters
    Omega_m0 = 0.315
    Omega_r0 = 9.2e-5
    Omega_phi0 = 1.0 - Omega_m0 - Omega_r0
    
    lambdas = np.linspace(0.1, 2.5, 30)
    
    best_lam = None
    min_dist = float('inf')
    best_w0, best_wa = 0, 0
    best_V0 = 0
    
    print("Sweeping lambda...")
    for lam in lambdas:
        V0, omega_phi_final = shoot_V0(lam, Omega_phi0, Omega_m0, Omega_r0)
        # Re-integrate with the shot V0 to get final w0, wa
        _, w0, wa, _, _, _ = integrate_trajectory(V0, lam, Omega_m0, Omega_r0)
        
        dist = (w0 - target_w0)**2 + (wa - target_wa)**2
        print(f"  lambda = {lam:.3f} -> shot V0 = {V0:.4f}, Omega_phi(a=1) = {omega_phi_final:.6f}, w0 = {w0:.4f}, wa = {wa:.4f}")
        
        if dist < min_dist:
            min_dist = dist
            best_lam = lam
            best_w0 = w0
            best_wa = wa
            best_V0 = V0
            
    print("\nSweep Complete.")
    print(f"Best match: lambda = {best_lam:.4f}")
    print(f"Shot V0 = {best_V0:.4f}")
    print(f"Resulting w0: {best_w0:.4f} (target {target_w0})")
    print(f"Resulting wa: {best_wa:.4f} (target {target_wa})")
    
    os.makedirs(".benchmarks", exist_ok=True)
    with open(".benchmarks/vafa_phase1_lambda.json", "w") as f:
        json.dump({
            "solver": "scipy.integrate.solve_ivp (Radau)",
            "lambda": float(best_lam),
            "V0": float(best_V0),
            "w0": float(best_w0),
            "wa": float(best_wa),
            "Omega_phi_a1": float(Omega_phi0)
        }, f, indent=4)

if __name__ == "__main__":
    main()
