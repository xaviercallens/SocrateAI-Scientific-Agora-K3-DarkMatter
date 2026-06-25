import sympy as sp
import math

def get_u(A, B, n_max=30):
    u = []
    for n in range(n_max+1):
        u_val = 0
        for k in range(n+1):
            binom_A = math.comb(n, k)**A
            binom_B = math.comb(n+k, k)**B
            u_val += binom_A * binom_B
        u.append(u_val)
    return u

def detect_recurrence_exact(u, num_terms, degree):
    num_unknowns = num_terms * (degree + 1)
    if len(u) < num_unknowns + num_terms:
        return False
        
    matrix = []
    num_eqs = min(len(u) - num_terms, num_unknowns + 3)
    if num_eqs < num_unknowns:
        return False
        
    for n in range(num_eqs):
        row = []
        for i in range(num_terms):
            for j in range(degree + 1):
                row.append( (n**j) * u[n+i] )
        matrix.append(row)
        
    M = sp.Matrix(matrix)
    null_space = M.nullspace()
    return len(null_space) > 0

def find_minimal_order(u):
    for degree in range(1, 4):
        for num_terms in range(2, 6):
            if detect_recurrence_exact(u, num_terms, degree):
                return degree + 1, num_terms
    return -1, -1

results = []
print(f"{'A':<3} | {'B':<3} | {'Order':<5} | {'Terms':<5}")
print("-" * 30)

for A in range(1, 11):
    for B in range(A, 11):  # Symmetry A,B is NOT true in general, because comb(n,k)^A comb(n+k,k)^B. Wait, is it symmetric? No!
        # Actually I should do all A, B.
        pass

for A in range(1, 11):
    for B in range(1, 11):
        u = get_u(A, B, n_max=35)
        order, terms = find_minimal_order(u)
        if order != -1:
            print(f"{A:<3} | {B:<3} | {order:<5} | {terms:<5}")
            results.append((A, B, order))

for A, B, order in results:
    if order == 3:
        print(f"K3 Candidate: A={A}, B={B}")
