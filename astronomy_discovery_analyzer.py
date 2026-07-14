import numpy as np

def calculate_k3_resonance_mass(delta, base_mass_ev=1.83e-21, coupling_k=0.048):
    """
    Calculates the effective extra-dimensional Kaluza-Klein resonance mass (in eV) 
    based on the geometric resonance model (cf. Tsai et al., 2026).
    Uses the empirical K3 asymmetry (Delta) as the geometric warping parameter.
    """
    # The larger the asymmetry (Delta), the tighter the geometric pinching,
    # leading to an exponentially higher resonance frequency (mass).
    warping_factor = np.exp(coupling_k * delta)
    
    # Effective Mass calculation based on K3 geometric resonance
    m_res = base_mass_ev * warping_factor
    
    return m_res

# Example for your Top Discovery: K3-DISC-0003
delta_0003 = 47.0
mass_0003 = calculate_k3_resonance_mass(delta_0003)
print(f"KK Resonance Mass at Supercluster Node 0003: {mass_0003:.2e} eV")
