import sympy as sp
import numpy as np

def compute_k3_periods(z_val, eps=0.01):
    """
    Computes the 22-dimensional K3 moduli space period vector.
    Using SymPy's hypergeometric solver to evaluate:
    Pi(z) = 3F2(1/4, 1/2, 3/4; 1, 1; z)
    
    Generates 22 features:
    1. K3 Volume: V = 1 / (1 + |z|^2)
    2. Picard Rank (simulated algebraic cycle count, e.g., 20)
    3. 20 branch periods evaluated at perturbed points z_k = z * (1 + eps * k) for k = 1 to 20
    """
    z = sp.Symbol('z')
    # Define the 3F2 hypergeometric function
    pi_expr = sp.hyper([sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4)], [sp.Integer(1), sp.Integer(1)], z)
    
    # 1. Volume
    try:
        z_float = float(z_val)
    except TypeError:
        z_float = float(z_val.evalf()) if hasattr(z_val, 'evalf') else 0.1
    volume = 1.0 / (1.0 + z_float**2)
    
    # 2. Picard Rank (For a 1-parameter family, generic Picard rank is 19 or 20)
    picard_rank = 20.0
    
    # 3. 20 branch periods
    periods = []
    for k in range(1, 21):
        z_k = z_val * (1 + eps * k)
        # Evaluate hypergeometric function at z_k
        val = pi_expr.subs(z, z_k).evalf()
        periods.append(float(val))
        
    # Combine into a 22-dimensional feature vector
    features = [volume, picard_rank] + periods
    return np.array(features, dtype=np.float32)

if __name__ == "__main__":
    # Test generation with a sample rational coordinate z = 1/10
    z_test = sp.Rational(1, 10)
    features = compute_k3_periods(z_test)
    print("Generated 22 K3 features:")
    print(features)
    print(f"Feature vector shape: {features.shape}")
    assert features.shape[0] == 22, "Feature vector must have exactly 22 elements."
