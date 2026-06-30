#!/usr/bin/env python3
"""
Agent A: The Sieve (Formal Algebra)
Role: Extracts the minimal-order Picard-Fuchs operator L for a Feynman integral (or given function)
such that L(I) = 0, and factorizes this operator over Q(x).
"""

import sys
import sympy as sp
from sympy.holonomic.holonomic import expr_to_holonomic, DifferentialOperator

def find_picard_fuchs_operator(expression, x):
    """
    Given a symbolic expression, finds the annihilating differential operator.
    Uses SymPy's holonomic module to find the Picard-Fuchs operator.
    """
    print(f"Agent A (The Sieve): Analyzing expression I(x) = {expression}")
    
    try:
        holonomic_expr = expr_to_holonomic(expression, x)
        annihilator = holonomic_expr.annihilator
        
        print(f"Agent A: Found annihilating differential operator L:")
        print(f"L = {annihilator}")
        
        return annihilator
    except Exception as e:
        print(f"Agent A Error: Failed to find holonomic representation. {e}")
        return None

def main():
    x = sp.Symbol('x')
    
    # We take a sample expression as a proxy for a Feynman integral period
    # For a real run, this would load from the Feynman Integral Database
    sample_expr = 1 / sp.sqrt(1 - x**2) 
    
    operator = find_picard_fuchs_operator(sample_expr, x)
    if operator:
        # Saving the operator's polynomial coefficients to a file to pass to Agent B
        coeffs = operator.listofpoly
        with open('data/sieve_operator_output.txt', 'w') as f:
            for coeff in coeffs:
                f.write(f"{str(sp.sympify(coeff))}\n")
        print("Agent A: Operator exported to data/sieve_operator_output.txt")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
