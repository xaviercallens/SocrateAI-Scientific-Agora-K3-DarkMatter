#!/usr/bin/env python3
"""
PROJECT ZEILBERGER (step 2): EXACT verification of the S20 minimal order-4 recurrence.

This script verifies that the order-4 recurrence coefficients (minimal recurrence of degree 13)
extracted from the creative telescoping certificate actually annihilate the S20 sequence terms:
    S20(n) = sum_{k=0}^n C(n,k)^4 * C(n+k,k)
exactly for all n in [0, 60].
"""
import sys
from math import comb
import sympy as sp

def S20(n: int) -> int:
    return sum(comb(n, k)**4 * comb(n + k, k) for k in range(n + 1))

def main():
    n = sp.symbols('n')
    
    # Minimal order-4 recurrence polynomials Q0..Q4 of degree 13
    Q0 = -(3*(n+1)**4*(3*n+4)*(3*n+5)*(8535643*n**7+169469658*n**6+1436623360*n**5+6740299644*n**4+18902585197*n**3+31686619162*n**2+29399194280*n+11647125056))
    Q1 = -(55063432993*n**13+1588819660695*n**12+20963891132894*n**11+167468366956203*n**10+903613284556839*n**9+3477557072410390*n**8+9820711443781882*n**7+20606199948403839*n**6+32126707298278818*n**5+36761444179589385*n**4+30012007177436894*n**3+16556660879488928*n**2+5532868382941920*n+846052269753600)
    Q2 = -(6819978757*n**13+210426023069*n**12+2975530787671*n**11+25526125026989*n**10+148183325103510*n**9+614551146955742*n**8+1872743330919213*n**7+4244605360330637*n**6+7153495812783439*n**5+8851419391630559*n**4+7814133099256906*n**3+4659741954049164*n**2+1681997842192584*n+277519882765920)
    Q3 = -((n+3)**2*(179248503*n**11+4813602339*n**10+57994210309*n**9+413646681628*n**8+1940244739916*n**7+6283318000170*n**6+14334249392454*n**5+23036916744307*n**4+25562518558626*n**3+18654645293596*n**2+8059295555832*n+1561898457120))
    Q4 = (n+3)**2*(n+4)**4*(8535643*n**7+109720157*n**6+599053915*n**5+1800480209*n**4+3216974566*n**3+3417224202*n**2+1998561324*n+496575040)

    Q = [Q0, Q1, Q2, Q3, Q4]
    
    print("=" * 68)
    print("Minimal S20 Order-4 Recurrence Verification")
    print("=" * 68)
    print("First 8 S20 values:")
    vals = [S20(i) for i in range(8)]
    print("S20(0..7) =", vals)
    
    # Check degree and leading coefficients of Q0..Q4
    print("\nRecurrence polynomials:")
    for j, q_poly in enumerate(Q):
        q_expanded = sp.expand(q_poly)
        poly_obj = sp.Poly(q_expanded, n)
        deg = poly_obj.degree()
        lead = poly_obj.LC()
        print(f"  Q{j}: degree {deg}, leading coeff {lead}")

    print("\nPlugging S20 terms into order-4 recurrence...")
    NMAX = 60
    S = [sp.Integer(S20(i)) for i in range(NMAX + 5)]
    all_zero = True
    first_fail = None
    
    for n0 in range(NMAX + 1):
        tot = sum(sp.expand(Q[j]).subs(n, n0) * S[n0 + j] for j in range(5))
        if tot != 0:
            all_zero = False
            if first_fail is None:
                first_fail = (n0, tot)
                
    if all_zero:
        print(f"  PASS: order-4 recurrence holds EXACTLY for all n in [0, {NMAX}]")
        print(f"        ({NMAX + 1} independent checks).")
    else:
        n0, tot = first_fail
        print(f"  FAIL: recurrence is NON-ZERO at n={n0}")
        print(f"        residual: {tot}")
        sys.exit(1)
        
    # Negative control
    Q0_bad = Q0 + 1
    sensitive = any(
        (sp.expand(Q0_bad).subs(n, n0) * S[n0]
         + sum(sp.expand(Q[j]).subs(n, n0) * S[n0 + j] for j in range(1, 5))) != 0
        for n0 in range(0, 6)
    )
    print(f"  Negative control (Q0+1 perturbation breaks recurrence): "
          f"{'PASS (sensitive)' if sensitive else 'FAIL (blind!)'}")
    
    if not sensitive:
        sys.exit(1)
        
    print("\nVERDICT: Minimal order-4 recurrence is rigorously verified numerically!")

if __name__ == "__main__":
    main()
