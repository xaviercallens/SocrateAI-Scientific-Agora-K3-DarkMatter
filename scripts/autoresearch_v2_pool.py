"""
AutoEvolve R2 / Phase B: exact term generators for the frozen 13-candidate pool.
================================================================================

Source of truth for candidate membership: data/autoresearch_v2/candidate_pool.yaml
(GATE-A approved by HUMAN 2026-07-14). This module supplies exact-integer term
generators for every candidate plus first-term cross-checks against OEIS data
fetched 2026-07-14 (curl, oeis.org/search?fmt=json — WebFetch is 403'd by OEIS).

Rule 1: every OEIS_FIRST_TERMS entry below is pasted verbatim from the OEIS
"data" field of the JSON response on the fetch date — real external data with
provenance, never invented. verify_terms() must pass before any gate runs.

Phase B OEIS resolutions performed 2026-07-14 (LR-2 closure):
  t011  -> NO OEIS MATCH for 1,5,43,469,5701,73583,986763 (searched 2026-07-14);
           recorded as not-in-OEIS, candidate remains defined by its binomial form.
  t103  -> A276536 (binomial sums of cubes of central binomial coefficients)
  t112  -> A274789 (diagonal of a rational function)
  cooper_s7  -> A183204 ("This sequence is s_7 in Cooper's paper" — J. Kimberley,
                OEIS comment). Closed form (Zudilin, via Kimberley):
                a(n) = Sum_j C(n,j)^2 C(2j,n) C(j+n,j).
  cooper_s10 -> A005260 ("s_10 in Cooper's paper"), a(n) = Sum_k C(n,k)^4.
  cooper_s18 -> A219692 ("s_18 in Cooper's paper"),
                a(n) = Sum_{j<=n/3} (-1)^j C(n,j) C(2j,j) C(2n-2j,n-j)
                       * (C(2n-3j-1,n) + C(2n-3j,n)),  a(0)=2 (C(-1,0):=1).
  az_sporadic_a006077 -> A006077, a(n) = Sum_k (-1)^k 3^(n-3k) C(n,3k) C(2k,k) C(3k,k).
                NOTE: A006077's recurrence has (n+1)^2 leading coefficient
                (Zagier zeta(2)/elliptic class shape) — the pool's provisional
                "K3-class per literature" tag is under test in G1-1.
  almkvist_zagier_second -> A125143 (Almkvist-Zudilin numbers),
                a(n) = Sum_k (-1)^(n-k) 3^(n-3k) ((3k)!/k!^3) C(n,3k) C(n+k,k),
                where (3k)!/k!^3 = C(3k,k)*C(2k,k).
"""

import math

# guarded binomial: C(m,0)=1 for ALL m (incl. m=-1, needed by A219692's a(0)=2);
# 0 outside the ordinary range otherwise.
def C(m: int, k: int) -> int:
    if k == 0:
        return 1
    if k < 0 or m < 0 or k > m:
        return 0
    return math.comb(m, k)


def terms_apery_zeta3(nmax):
    return [sum(C(n, k) ** 2 * C(n + k, k) ** 2 for k in range(n + 1))
            for n in range(nmax + 1)]

def terms_apery_zeta2_s21(nmax):
    return [sum(C(n, k) ** 2 * C(n + k, k) for k in range(n + 1))
            for n in range(nmax + 1)]

def terms_s12(nmax):
    return [sum(C(n, k) * C(n + k, k) ** 2 for k in range(n + 1))
            for n in range(nmax + 1)]

def terms_domb(nmax):
    return [sum(C(n, k) ** 2 * C(2 * k, k) * C(2 * n - 2 * k, n - k)
                for k in range(n + 1)) for n in range(nmax + 1)]

def terms_t003(nmax):
    """Partial sums of central-binomial cubes: sum_{k<=n} C(2k,k)^3 (A079727)."""
    out, s = [], 0
    for n in range(nmax + 1):
        s += C(2 * n, n) ** 3
        out.append(s)
    return out

def terms_t003_core(nmax):
    """Hypergeometric core of t003: u_k = C(2k,k)^3 (A002897),
    g.f. 3F2(1/2,1/2,1/2;1,1;64z). The K3-type geometry of t003 lives in this
    core; the partial sum is core/(1-z)."""
    return [C(2 * k, k) ** 3 for k in range(nmax + 1)]

def terms_t011(nmax):
    return [sum(C(n + k, k) * C(2 * k, k) for k in range(n + 1))
            for n in range(nmax + 1)]

def terms_t103(nmax):
    return [sum(C(n, k) * C(2 * k, k) ** 3 for k in range(n + 1))
            for n in range(nmax + 1)]

def terms_t112(nmax):
    return [sum(C(n, k) * C(n + k, k) * C(2 * k, k) ** 2 for k in range(n + 1))
            for n in range(nmax + 1)]

def terms_cooper_s7(nmax):
    return [sum(C(n, j) ** 2 * C(2 * j, n) * C(j + n, j) for j in range(n + 1))
            for n in range(nmax + 1)]

def terms_cooper_s10(nmax):
    return [sum(C(n, k) ** 4 for k in range(n + 1)) for n in range(nmax + 1)]

def terms_cooper_s18(nmax):
    out = []
    for n in range(nmax + 1):
        s = 0
        for j in range(n // 3 + 1):
            s += ((-1) ** j * C(n, j) * C(2 * j, j) * C(2 * n - 2 * j, n - j)
                  * (C(2 * n - 3 * j - 1, n) + C(2 * n - 3 * j, n)))
        out.append(s)
    return out

def terms_a006077(nmax):
    out = []
    for n in range(nmax + 1):
        s = 0
        for k in range(n // 3 + 1):
            s += (-1) ** k * 3 ** (n - 3 * k) * C(n, 3 * k) * C(2 * k, k) * C(3 * k, k)
        out.append(s)
    return out

def terms_a125143(nmax):
    out = []
    for n in range(nmax + 1):
        s = 0
        for k in range(n // 3 + 1):
            s += ((-1) ** (n - k) * 3 ** (n - 3 * k)
                  * C(3 * k, k) * C(2 * k, k)      # = (3k)!/k!^3
                  * C(n, 3 * k) * C(n + k, k))
        out.append(s)
    return out


# OEIS "data" fields, fetched 2026-07-14 (first entries; verbatim provenance).
OEIS_FIRST_TERMS = {
    "apery_zeta3":            ("A005259", [1, 5, 73, 1445, 33001, 819005]),
    "apery_zeta2_s21":        ("A005258", [1, 3, 19, 147, 1251, 11253]),
    "s12_v1_primary":         ("A112019", [1, 5, 55, 749, 11251, 178835]),
    "domb":                   ("A002895", [1, 4, 28, 256, 2716, 31504]),
    "t003_csum_central_cubes":("A079727", [1, 9, 225, 8225, 351225, 16354233]),
    "t011":                   (None,      [1, 5, 43, 469, 5701, 73583]),   # no OEIS match 2026-07-14
    "t103":                   ("A276536", [1, 9, 233, 8673, 376329, 17800209]),
    "t112":                   ("A274789", [1, 9, 241, 9129, 402321, 19321689]),
    "cooper_s7":              ("A183204", [1, 4, 48, 760, 13840, 273504]),
    "cooper_s10":             ("A005260", [1, 2, 18, 164, 1810, 21252]),
    "cooper_s18":             ("A219692", [2, 6, 54, 564, 6390, 76356]),
    "az_sporadic_a006077":    ("A006077", [1, 3, 9, 21, 9, -297]),
    "almkvist_zagier_second": ("A125143", [1, -3, 9, -3, -279, 2997]),
}

# t003 core cross-check: A002897 = C(2n,n)^3 = 1, 8, 216, 8000, ...
A002897_FIRST = [1, 8, 216, 8000, 343000, 16003008]

POOL = {
    "apery_zeta3":             terms_apery_zeta3,
    "apery_zeta2_s21":         terms_apery_zeta2_s21,
    "s12_v1_primary":          terms_s12,
    "domb":                    terms_domb,
    "t003_csum_central_cubes": terms_t003,
    "t011":                    terms_t011,
    "t103":                    terms_t103,
    "t112":                    terms_t112,
    "cooper_s7":               terms_cooper_s7,
    "cooper_s10":              terms_cooper_s10,
    "cooper_s18":              terms_cooper_s18,
    "az_sporadic_a006077":     terms_a006077,
    "almkvist_zagier_second":  terms_a125143,
}

# For gates that need the geometric (hypergeometric) core rather than the
# partial sum, map candidate id -> core generator (documented deviation).
GEOMETRIC_CORE = {
    "t003_csum_central_cubes": terms_t003_core,
}

CONTROLS = {
    "positive_k3": "apery_zeta3",       # must classify K3-type (ODE order 3)
    "negative_elliptic": "apery_zeta2_s21",  # must classify elliptic (ODE order 2)
}


def verify_terms() -> list:
    """Cross-check every generator against its OEIS first terms.
    Returns list of failures (empty = all pass)."""
    failures = []
    for cid, (oeis_id, expected) in OEIS_FIRST_TERMS.items():
        got = POOL[cid](len(expected) - 1)
        if got != expected:
            failures.append((cid, oeis_id, expected, got))
    core = terms_t003_core(len(A002897_FIRST) - 1)
    if core != A002897_FIRST:
        failures.append(("t003_core", "A002897", A002897_FIRST, core))
    return failures


if __name__ == "__main__":
    fails = verify_terms()
    if fails:
        for f in fails:
            print("MISMATCH:", f)
        raise SystemExit(1)
    print(f"All {len(OEIS_FIRST_TERMS)} candidate generators + t003 core match "
          f"OEIS reference terms (fetched 2026-07-14).")
