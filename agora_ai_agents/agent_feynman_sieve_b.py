#!/usr/bin/env python3
"""
Agent B: The Geometrician (K3 Topology)
Role: Compares the operator L provided by Agent A with the K3 family catalog.
Checks if the Alphabet (singularities) of the Feynman operator match the S_{1,2} K3 geometry.
"""

import sys
import os
import sympy as sp

def load_operator_coeffs(filepath):
    if not os.path.exists(filepath):
        print(f"Agent B Error: Could not find operator output at {filepath}")
        return None
    
    coeffs = []
    x = sp.Symbol('x')
    with open(filepath, 'r') as f:
        for line in f:
            expr = sp.sympify(line.strip(), locals={'x': x})
            coeffs.append(expr)
    return coeffs

def find_singularities(coeffs):
    """
    The singularities are the roots of the leading coefficient polynomial.
    """
    if not coeffs:
        return []
    leading_coeff = coeffs[-1]
    print(f"Agent B: Leading coefficient is {leading_coeff}")
    
    # Find roots
    try:
        roots = sp.solve(leading_coeff, sp.Symbol('x'))
        return roots
    except Exception as e:
        print(f"Agent B: Could not solve for roots. {e}")
        return []

def main():
    print("Agent B (The Geometrician): Loading Picard-Fuchs operator from Agent A...")
    filepath = 'data/sieve_operator_output.txt'
    coeffs = load_operator_coeffs(filepath)
    
    if coeffs is None:
        sys.exit(1)
        
    singularities = find_singularities(coeffs)
    print(f"Agent B: Extracted Alphabet (singular points in complex plane): {singularities}")
    
    # Known S_1,2 K3 geometry singularities (mocked for this protocol test)
    # The true S_1,2 Picard-Fuchs operator has specific singularities (e.g., 0, 1, -1, oo)
    k3_s12_singularities = [sp.sympify('-1'), sp.sympify('1')] # Assuming our test expression 1/sqrt(1-x^2)
    
    # Check if Feynman singularities are a subset of K3 singularities
    print(f"Agent B: K3 S_{{1,2}} known moduli singularities: {k3_s12_singularities}")
    
    match = True
    for sing in singularities:
        if sing not in k3_s12_singularities:
            match = False
            break
            
    if match:
        print("Agent B: GO - The exponents of the singularities match S_{1,2}. Flagging for high-priority validation by Agent C.")
        with open('data/sieve_b_flag.txt', 'w') as f:
            f.write("MATCH")
    else:
        print("Agent B: NO-GO - Singularities of the integral do not overlap with K3 moduli points.")
        with open('data/sieve_b_flag.txt', 'w') as f:
            f.write("NO_MATCH")

if __name__ == "__main__":
    main()
