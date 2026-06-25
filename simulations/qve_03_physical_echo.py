import sympy as sp
import json
import os
import sys
import time
from typing import List, Tuple, Dict, Optional

class EPoly:
    def __init__(self, d=None):
        self.d = d if d is not None else {}
        
    def __add__(self, other):
        res = dict(self.d)
        for k, v in other.d.items():
            res[k] = res.get(k, 0) + v
            if res[k] == 0:
                del res[k]
        return EPoly(res)
        
    def __sub__(self, other):
        res = dict(self.d)
        for k, v in other.d.items():
            res[k] = res.get(k, 0) - v
            if res[k] == 0:
                del res[k]
        return EPoly(res)
        
    def __neg__(self):
        return EPoly({k: -v for k, v in self.d.items()})
        
    def __mul__(self, other):
        if isinstance(other, EPoly):
            res = {}
            for k1, v1 in self.d.items():
                for k2, v2 in other.d.items():
                    k = (k1[0]+k2[0], k1[1]+k2[1])
                    if k[0] + k[1] <= 2: # truncate at O(e^2)
                        res[k] = res.get(k, 0) + v1 * v2
            return EPoly({k: v for k, v in res.items() if v != 0})
        else:
            return EPoly({k: v * other for k, v in self.d.items() if v * other != 0})

class FourierPoly:
    def __init__(self, coeffs=None):
        self.coeffs = coeffs if coeffs is not None else {}
        
    def __add__(self, other):
        res = dict(self.coeffs)
        for k, v in other.coeffs.items():
            if k not in res:
                res[k] = v
            else:
                res[k] = res[k] + v
        return FourierPoly(res)
        
    def __neg__(self):
        return FourierPoly({k: -v for k, v in self.coeffs.items()})

    def __sub__(self, other):
        return self + (-other)
        
    def __mul__(self, other):
        if isinstance(other, (int, float, sp.Expr)):
            return FourierPoly({k: v * other for k, v in self.coeffs.items()})
        res = {}
        for k1, v1 in self.coeffs.items():
            for k2, v2 in other.coeffs.items():
                k = k1 + k2
                if k not in res:
                    res[k] = v1 * v2
                else:
                    res[k] = res[k] + v1 * v2
        return FourierPoly(res)
        
    def dx(self):
        res = {}
        for k, v in self.coeffs.items():
            if k != 0:
                res[k] = v * (k * sp.I)
        return FourierPoly(res)
        
    def inv_dx(self):
        res = {}
        for k, v in self.coeffs.items():
            if k == 0:
                continue
            res[k] = v * (1 / (k * sp.I))
        return FourierPoly(res)

    def get(self, k):
        return self.coeffs.get(k, EPoly())

def extract_physical_waterbag_echo_sequence(max_order: int = 50, A=None, V0=None) -> List[sp.Rational]:
    """
    Simulates the true 1D convective double-pulse waterbag boundaries.
    Initializes a perturbation at k1 = 1 (amplitude e1) and k2 = 2 (amplitude e2)
    and solves the non-linear coupling convective equations to extract the
    O(e^2) echo sequence at mode k_e = -1.
    """
    if A is None:
        A = [sp.Rational(1), sp.Rational(-1), sp.Rational(1), sp.Rational(-1)]
    if V0 is None:
        V0 = [sp.Rational(2), sp.Rational(1), sp.Rational(-1), sp.Rational(-2)]
        
    num_bags = len(V0)
    V = []
    for i in range(num_bags):
        poly = FourierPoly({
            0: EPoly({(0,0): V0[i]}),
            1: EPoly({(1,0): sp.Rational(1,2)}),
            -1: EPoly({(1,0): sp.Rational(1,2)}),
            2: EPoly({(0,1): sp.Rational(1,2)}),
            -2: EPoly({(0,1): sp.Rational(1,2)})
        })
        V.append([poly])

    E = []
    rho_0 = FourierPoly()
    for j in range(num_bags):
        poly_pert = FourierPoly(dict(V[j][0].coeffs))
        if 0 in poly_pert.coeffs:
            poly_pert.coeffs[0] = poly_pert.coeffs[0] - EPoly({(0,0): V0[j]})
        rho_0 = rho_0 + poly_pert * A[j]
    E.append( (-rho_0).inv_dx() )
    
    sequence = []
    for n in range(max_order):
        E_n = E[n]
        for j in range(num_bags):
            nl_term = FourierPoly()
            for m in range(n + 1):
                term = V[j][m] * V[j][n - m].dx()
                nl_term = nl_term + term * sp.binomial(n, m)
            
            V_next = -nl_term - E_n
            V[j].append(V_next)
            
        rho_next = FourierPoly()
        for j in range(num_bags):
            rho_next = rho_next + V[j][n+1] * A[j]
        E_next = (-rho_next).inv_dx()
        E.append(E_next)
        
        rho_k_minus_1 = rho_next.get(-1)
        echo_coeff = rho_k_minus_1.d.get((1,1), sp.Rational(0))
        sequence.append(echo_coeff)
        
    return sequence

class PRecurrenceSolver:
    """
    Mines linear recurrence relations with polynomial coefficients:
    Sum_{j=0}^d P_j(n) a_{n-j} = 0, where P_j(n) = Sum_{r=0}^p c_{j,r} n^r
    """
    @staticmethod
    def find_recurrence(seq: List[sp.Rational], max_order: int, max_degree: int) -> Optional[Tuple[int, int, Dict[Tuple[int, int], sp.Rational]]]:
        N = len(seq)
        for d in range(1, max_order + 1):
            for p in range(0, max_degree + 1):
                num_vars = (d + 1) * (p + 1)
                num_eqs = N - d
                if num_eqs < num_vars + 2: # Keep system overdetermined for statistical uniqueness
                    continue
                
                matrix_rows = []
                var_indices = []
                for j in range(d + 1):
                    for r in range(p + 1):
                        var_indices.append((j, r))
                        
                for n in range(d, N):
                    row = []
                    for j, r in var_indices:
                        val = (n**r) * seq[n - j]
                        row.append(val)
                    matrix_rows.append(row)
                    
                M = sp.Matrix(matrix_rows)
                ns = M.nullspace()
                
                if len(ns) > 0:
                    for sol in ns:
                        lcm = 1
                        for val in sol:
                            if val != 0:
                                lcm = sp.lcm(lcm, val.q)
                        sol = sol * lcm
                        
                        coeffs = {}
                        for idx, (j, r) in enumerate(var_indices):
                            val = sol[idx]
                            if val != 0:
                                coeffs[(j, r)] = val
                                
                        has_d = any(c != 0 for (j, r), c in coeffs.items() if j == d)
                        has_0 = any(c != 0 for (j, r), c in coeffs.items() if j == 0)
                        if has_d and has_0:
                            return d, p, coeffs
        return None

    @staticmethod
    def format_recurrence(order: int, degree: int, coeffs: Dict[Tuple[int, int], sp.Rational]) -> str:
        P_j = {}
        for j in range(order + 1):
            poly_terms = []
            for r in range(degree + 1):
                c = coeffs.get((j, r), 0)
                if c != 0:
                    if r == 0:
                        poly_terms.append(f"{c}")
                    elif r == 1:
                        poly_terms.append(f"{c}*n")
                    else:
                        poly_terms.append(f"{c}*n^{r}")
            if poly_terms:
                poly_str = " + ".join(poly_terms).replace("+ -", "- ")
                if len(poly_terms) > 1:
                    P_j[j] = f"({poly_str})"
                else:
                    P_j[j] = poly_str
            else:
                P_j[j] = "0"
                
        terms = []
        for j in range(order + 1):
            if P_j[j] != "0":
                terms.append(f"{P_j[j]} * a_{{n-{j}}}")
        return " + ".join(terms).replace("+ -", "- ") + " = 0"

def generate_si_squared_sequence(max_power: int = 120) -> List[sp.Rational]:
    """Generates the non-zero sub-sequence of 1/2 * (Si(t))^2."""
    si_coeffs = [sp.Rational(0, 1)] * (max_power + 1)
    for k in range((max_power - 1) // 2 + 1):
        power = 2 * k + 1
        si_coeffs[power] = sp.Rational((-1)**k, power * sp.factorial(power))
        
    y_coeffs = [sp.Rational(0, 1)] * (max_power + 1)
    for n in range(max_power + 1):
        term = sum(si_coeffs[j] * si_coeffs[n - j] for j in range(n + 1))
        y_coeffs[n] = term / 2
        
    sub_seq = []
    for idx in range(2, max_power + 1, 2):
        sub_seq.append(y_coeffs[idx])
    return sub_seq

def main():
    print("🌌 [Autoresearch Execution] Starting Verification of Physical Echoes and P-Recurrences\n")
    
    # ----------------------------------------------------
    # Step 1: Continuous Toy Model Sequence (Gap B Verification)
    # ----------------------------------------------------
    print("1. Generating continuous 0D toy model echo sequence: 1/2 * (Si(t))^2...")
    toy_seq = generate_si_squared_sequence(max_power=120) # 60 non-zero terms
    print(f"   Generated {len(toy_seq)} terms. First 5 terms: {[str(x) for x in toy_seq[:5]]}")
    
    print("   Searching for continuous P-recurrence (max_order=6, max_degree=6)...")
    toy_res = PRecurrenceSolver.find_recurrence(toy_seq, max_order=6, max_degree=6)
    
    if toy_res:
        d, p, coeffs = toy_res
        rec_str = PRecurrenceSolver.format_recurrence(d, p, coeffs)
        print(f"   🎉 SUCCESS: Found P-Recurrence of order {d}, degree {p}:")
        print(f"      => {rec_str}\n")
    else:
        print("   ❌ FAILED: No P-recurrence found for the toy model sequence within tested bounds.\n")
        d, p, coeffs, rec_str = None, None, None, "None"
        
    # ----------------------------------------------------
    # Step 2: Simpler 2-Waterbag Physical Model (Gap A & B Verification)
    # ----------------------------------------------------
    print("2. Generating simple 2-waterbag physical echo sequence (max_order=50)...")
    wb2_start = time.time()
    wb2_A = [sp.Rational(1), sp.Rational(-1)]
    wb2_V0 = [sp.Rational(1), sp.Rational(-1)]
    wb2_full_seq = extract_physical_waterbag_echo_sequence(max_order=50, A=wb2_A, V0=wb2_V0)
    print(f"   Generated 2-waterbag sequence in {time.time() - wb2_start:.2f} seconds.")
    
    # Extract non-zero terms (odd indices)
    wb2_non_zero_seq = []
    for idx in range(1, len(wb2_full_seq), 2):
        wb2_non_zero_seq.append(wb2_full_seq[idx])
    print(f"   Extracted {len(wb2_non_zero_seq)} terms: {[str(x) for x in wb2_non_zero_seq[:5]]} ...")
    
    print("   Searching for 2-waterbag P-recurrence (max_order=4, max_degree=3)...")
    wb2_res = PRecurrenceSolver.find_recurrence(wb2_non_zero_seq, max_order=4, max_degree=3)
    
    if wb2_res:
        w2_d, w2_p, w2_coeffs = wb2_res
        wb2_rec_str = PRecurrenceSolver.format_recurrence(w2_d, w2_p, w2_coeffs)
        print(f"   🎉 SUCCESS: Found 2-Waterbag P-Recurrence of order {w2_d}, degree {w2_p}:")
        print(f"      => {wb2_rec_str}\n")
    else:
        print("   ❌ FAILED: No exact P-recurrence found in the tested bounds for the 2-waterbag physical sequence.\n")
        w2_d, w2_p, w2_coeffs, wb2_rec_str = None, None, None, "None"

    # ----------------------------------------------------
    # Step 3: Physical 4-Waterbag Echo Sequence (Gap A Verification)
    # ----------------------------------------------------
    print("3. Generating physical 4-waterbag double-pulse convective echo sequence (max_order=50)...")
    wb4_start = time.time()
    wb4_full_seq = extract_physical_waterbag_echo_sequence(max_order=50)
    print(f"   Generated 4-waterbag sequence in {time.time() - wb4_start:.2f} seconds.")
    
    # Extract only non-zero terms (odd indices)
    wb4_non_zero_seq = []
    for idx in range(1, len(wb4_full_seq), 2):
        wb4_non_zero_seq.append(wb4_full_seq[idx])
    print(f"   Extracted {len(wb4_non_zero_seq)} non-zero terms. First 5 terms: {[str(x) for x in wb4_non_zero_seq[:5]]}")
    
    print("   Searching for 4-waterbag P-recurrence (max_order=4, max_degree=3)...")
    wb4_res = PRecurrenceSolver.find_recurrence(wb4_non_zero_seq, max_order=4, max_degree=3)
    
    if wb4_res:
        w4_d, w4_p, w4_coeffs = wb4_res
        wb4_rec_str = PRecurrenceSolver.format_recurrence(w4_d, w4_p, w4_coeffs)
        print(f"   🎉 SUCCESS: Found 4-Waterbag P-Recurrence of order {w4_d}, degree {w4_p}:")
        print(f"      => {wb4_rec_str}\n")
    else:
        print("   ❌ FAILED: No exact P-recurrence found in the tested bounds for the 4-waterbag physical sequence.\n")
        w4_d, w4_p, w4_coeffs, wb4_rec_str = None, None, None, "None"
        
    # ----------------------------------------------------
    # Step 4: Archive Results to Alexandrie
    # ----------------------------------------------------
    os.makedirs("alexandrie_data/QVE-03", exist_ok=True)
    payload = {
        "protocol": "QVE-03",
        "description": "Verification of continuous Vlasov-Poisson echoes and holonomic recurrences",
        "toy_model": {
            "function": "1/2 * (Si(t))^2",
            "sequence": [str(x) for x in toy_seq],
            "recurrence": {
                "order": d,
                "degree": p,
                "formula": rec_str
            }
        },
        "physical_2_waterbag_model": {
            "wavenumbers": "k1=1, k2=2",
            "echo_wavenumber": "k_e=1",
            "sequence": [str(x) for x in wb2_non_zero_seq],
            "recurrence": {
                "order": w2_d,
                "degree": w2_p,
                "formula": wb2_rec_str
            }
        },
        "physical_4_waterbag_model": {
            "wavenumbers": "k1=1, k2=2",
            "echo_wavenumber": "k_e=1",
            "sequence": [str(x) for x in wb4_non_zero_seq],
            "recurrence": {
                "order": w4_d,
                "degree": w4_p,
                "formula": wb4_rec_str
            }
        }
    }
    
    with open("alexandrie_data/QVE-03/physical_echo_results.json", "w") as f:
        json.dump(payload, f, indent=4)
    print("✅ Results successfully committed to Alexandrie Vault at alexandrie_data/QVE-03/physical_echo_results.json.")

if __name__ == "__main__":
    main()
