#!/usr/bin/env python3
"""
INDEPENDENT zero-shot re-derivation of T(cooper_s10) ~= U + <20> and its
witness, for T0's producer!=verifier acceptance of C2_cooper_s10_v4_DRAFT.

Deliberately does NOT import, call, or copy checkers/check_U1_lattice.py or
check_U1_witness_serialization.py. Every routine below is written from the
lattice-theory definitions directly. The ONLY thing taken from the existing
work is the *claim under test* (the Gram matrix G and the asserted witness P),
which is what an independent verifier is supposed to be handed.

Scope boundary, stated up front and not blurred:
  - IN scope (fully independent here): everything downstream of G --
    det, signature, evenness, discriminant group + form, the U-splitting
    itself (re-derived from scratch by my own algorithm, not read from the
    cert), and whether the cert's P actually does what it claims.
  - OUT of scope (cannot be re-derived without redoing 60-digit monodromy
    numerics): that G *is* the monodromy-invariant orbit lattice of the
    cooper_s10 family. Reported honestly rather than papered over.
"""

from sympy import Matrix, Rational, eye, zeros, gcd, sqrt, nsimplify
from itertools import product

# ---------------------------------------------------------------------------
# The CLAIM under test, transcribed from C2_cooper_s10_v4_DRAFT.json.
# (Transcribed by hand here on purpose: reading it via the repo's own loader
# would couple this check to the code it is supposed to be independent of.)
# ---------------------------------------------------------------------------
G = Matrix([[0, 0, -1],
            [0, 20, 0],
            [-1, 0, 0]])

P_claimed = Matrix([[1, -360, 120],
                    [0, -6, 1],
                    [0, -1, 0]])

GRAM_AFTER_claimed = Matrix([[0, 1, 0],
                             [1, 0, 0],
                             [0, 0, 20]])

CLAIMED_DET = -20
CLAIMED_SIG = (2, 1)
CLAIMED_DISC_ORDER = 20
CLAIMED_Q = Rational(1, 20)
CLAIMED_D = 20
CLAIMED_N_PROPER_EVEN_OVERLATTICES = 0

results = {}
def check(name, got, want, note=""):
    ok = (got == want)
    results[name] = ok
    flag = "PASS" if ok else "*** FAIL ***"
    print(f"[{flag}] {name}: got {got!r}, expected {want!r} {note}")
    return ok


print("=" * 74)
print("PART 1 -- basic invariants of G, computed from scratch")
print("=" * 74)

# Evenness: a lattice is even iff every diagonal entry of the Gram is even
# (diagonal even => x^2 even for all x, since x^2 = sum_i a_i^2 G_ii + 2*cross).
diag_even = all(G[i, i] % 2 == 0 for i in range(G.rows))
check("G is even", diag_even, True)

# Symmetry (a Gram matrix must be symmetric).
check("G is symmetric", G == G.T, True)

check("det(G)", int(G.det()), CLAIMED_DET)

# Signature via eigenvalue signs (Sylvester's law of inertia). Exact
# characteristic polynomial, then count sign changes numerically only for
# the *sign*, which is safe: eigenvalues are bounded away from 0 since
# det != 0.
evs = G.eigenvals()
n_pos = sum(m for val, m in evs.items() if val.evalf() > 0)
n_neg = sum(m for val, m in evs.items() if val.evalf() < 0)
n_zero = sum(m for val, m in evs.items() if val.evalf() == 0)
check("signature (n_pos, n_neg)", (n_pos, n_neg), CLAIMED_SIG)
check("no zero eigenvalues (nondegenerate)", n_zero, 0)


print()
print("=" * 74)
print("PART 2 -- discriminant group and form, from Smith normal form")
print("=" * 74)

def smith_normal_form_diag(M):
    """Elementary-divisor diagonal of an integer matrix, computed here by
    straightforward SNF reduction (not via any repo helper)."""
    A = M.copy()
    rows, cols = A.rows, A.cols
    divisors = []
    r = c = 0
    while r < rows and c < cols:
        # find a pivot: smallest nonzero |entry| in the active submatrix
        piv = None
        best = None
        for i in range(r, rows):
            for j in range(c, cols):
                if A[i, j] != 0 and (best is None or abs(A[i, j]) < best):
                    best = abs(A[i, j]); piv = (i, j)
        if piv is None:
            break
        pi, pj = piv
        A.row_swap(r, pi); A.col_swap(c, pj)
        # clear the row and column at the pivot, repeating until clean
        while True:
            changed = False
            for i in range(r + 1, rows):
                if A[i, c] != 0:
                    q = A[i, c] // A[r, c]
                    A[i, :] = A[i, :] - q * A[r, :]
                    if A[i, c] != 0:
                        A.row_swap(r, i); changed = True
            for j in range(c + 1, cols):
                if A[r, j] != 0:
                    q = A[r, j] // A[r, c]
                    A[:, j] = A[:, j] - q * A[:, c]
                    if A[r, j] != 0:
                        A.col_swap(c, j); changed = True
            if not changed:
                break
        divisors.append(abs(A[r, c]))
        r += 1; c += 1
    return divisors

divs = smith_normal_form_diag(G)
print(f"  elementary divisors of G: {divs}")
disc_order = 1
for d in divs:
    disc_order *= d
check("discriminant group order |det|", disc_order, CLAIMED_DISC_ORDER)

# Nontrivial elementary divisors give the group structure.
nontrivial = [d for d in divs if d != 1]
check("discriminant group is cyclic Z/20", nontrivial, [20])

# Discriminant form: q(x) = x^T G^{-1} x mod 2Z on the dual, for the
# generator of the cyclic discriminant group. Build G^{-1} exactly.
Ginv = G.inv()
print(f"  G^-1 =\n{Ginv}")

# Find a generator of L*/L. L* is spanned by rows of G^{-1} (in the basis
# dual to G's). Search small combos for an element of exact order 20.
gen = None
for coeffs in product(range(-20, 21), repeat=3):
    if all(c == 0 for c in coeffs):
        continue
    v = Matrix(3, 1, list(coeffs))
    x = Ginv * v            # element of L* in the original basis
    # order in L*/L = smallest m>0 with m*x integral
    m = 1
    while m <= 40:
        if all((m * x)[i].q == 1 for i in range(3)):
            break
        m += 1
    if m == 20:
        gen = x
        break
check("found generator of order exactly 20", gen is not None, True)

if gen is not None:
    q_val = (gen.T * G * gen)[0, 0]
    q_mod2 = q_val - 2 * (q_val / 2 - Rational(1, 2)).floor() - 1 if False else q_val % 2
    # normalise into [0,2)
    q_norm = Rational(q_val) % 2
    print(f"  q(generator) = {q_val} = {q_norm} mod 2Z")
    # The form is defined up to choice of generator: q(k*x) = k^2 q(x).
    # Collect the whole orbit so the comparison is generator-independent.
    orbit = set()
    for k in range(1, 20):
        if gcd(k, 20) == 1:
            orbit.add(Rational(k * k * q_val) % 2)
    print(f"  orbit of q under generator change: {sorted(orbit)}")
    check("claimed q=1/20 lies in the generator-change orbit",
          CLAIMED_Q % 2 in orbit, True,
          "(comparison made orbit-wise, since q depends on generator choice)")


print()
print("=" * 74)
print("PART 3 -- U-splitting RE-DERIVED FROM SCRATCH (my own algorithm)")
print("=" * 74)
print("  Not reading the cert's P. Standard construction:")
print("   (1) find primitive isotropic e with (e,L)=Z")
print("   (2) find w with (e,w)=1; set f = w - (w^2/2) e  => f^2=0, (e,f)=1")
print("   (3) K = {x : (x,e)=(x,f)=0} is rank 1, generated by k with k^2=d")
print()

def pairing(u, v):
    return (u.T * G * v)[0, 0]

# (1) search for a primitive isotropic vector whose pairing with the whole
# lattice is all of Z (that is what allows U to split off as a direct summand)
e = None
for coeffs in product(range(-6, 7), repeat=3):
    if all(c == 0 for c in coeffs):
        continue
    v = Matrix(3, 1, list(coeffs))
    if gcd(gcd(coeffs[0], coeffs[1]), coeffs[2]) != 1:
        continue                      # not primitive
    if pairing(v, v) != 0:
        continue                      # not isotropic
    pairings = [pairing(v, Matrix(3, 1, [1 if i == j else 0 for i in range(3)]))
                for j in range(3)]
    if gcd(gcd(pairings[0], pairings[1]), pairings[2]) == 1:
        e = v
        break
check("found primitive isotropic e with (e,L)=Z", e is not None, True)
print(f"  e = {list(e)}")

# (2) find w with (e,w) = 1
w = None
for coeffs in product(range(-6, 7), repeat=3):
    v = Matrix(3, 1, list(coeffs))
    if pairing(e, v) == 1:
        w = v
        break
w2 = pairing(w, w)
check("w^2 is even (needed for f to be integral)", w2 % 2 == 0, True)
f = w - Rational(w2, 2) * e
check("f is integral", all(f[i].q == 1 for i in range(3)), True)
check("f^2 = 0", pairing(f, f), 0)
check("(e,f) = 1", pairing(e, f), 1)
print(f"  w = {list(w)}, w^2 = {w2}  ->  f = {list(f)}")

# (3) orthogonal complement of <e,f>, solved exactly rather than by search:
# x is in the complement iff (Ge)^T x = 0 and (Gf)^T x = 0, i.e. x lies in the
# kernel of the 2x3 integer matrix with rows (Ge)^T, (Gf)^T. Rank 2 => kernel
# is rank 1. Then clear denominators and divide by the content to make the
# generator primitive.
constraint = Matrix.vstack((G * e).T, (G * f).T)
ker = constraint.nullspace()
check("complement of <e,f> has rank exactly 1", len(ker), 1)
kv = ker[0]
denom = 1
for i in range(3):
    denom = denom * kv[i].q // gcd(denom, kv[i].q)
kv = (kv * denom)
content = gcd(gcd(int(kv[0]), int(kv[1])), int(kv[2]))
k = Matrix(3, 1, [int(kv[i]) // int(content) for i in range(3)])
check("found generator k of <e,f>^perp", k is not None, True)
d_derived = pairing(k, k)
print(f"  k = {list(k)}, k^2 = {d_derived}")
check("RE-DERIVED d (so T ~= U + <d>)", int(d_derived), CLAIMED_D)

# assemble my own witness and confirm it splits G
P_mine = Matrix.hstack(e, f, k)
check("my witness P_mine is unimodular (det = +-1)",
      abs(int(P_mine.det())), 1)
gram_mine = P_mine.T * G * P_mine
print(f"  P_mine (columns e|f|k) =\n{P_mine}")
print(f"  P_mine^T G P_mine =\n{gram_mine}")
check("my splitting gives U + <20>", gram_mine,
      Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 20]]))


print()
print("=" * 74)
print("PART 4 -- does the CERT's own witness P do what it claims?")
print("=" * 74)
check("det(P_claimed) = 1", int(P_claimed.det()), 1)
gram_after_computed = P_claimed.T * G * P_claimed
print(f"  P^T G P =\n{gram_after_computed}")
check("P^T G P equals the cert's gram_after",
      gram_after_computed, GRAM_AFTER_claimed)
check("gram_after is exactly U + <20>", GRAM_AFTER_claimed,
      Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 20]]))

# Guard against the convention being the other way round (P G P^T), which
# would silently "pass" for symmetric-ish cases; report both explicitly.
print(f"  (other convention) P G P^T =\n{P_claimed * G * P_claimed.T}")


print()
print("=" * 74)
print("PART 5 -- proper even invariant overlattices (claim: 0)")
print("=" * 74)
# An even overlattice L' > L of finite index corresponds to an isotropic
# subgroup H < L*/L with q|H = 0. Here L*/L = Z/20 cyclic, so enumerate its
# subgroups directly: generated by (20/m)*gen for each divisor m of 20.
if gen is not None:
    proper_even_overlattices = 0
    for m in [1, 2, 4, 5, 10, 20]:      # |H| = m
        if m == 1:
            continue                     # trivial subgroup = L itself
        h = (Rational(20, m)) * gen      # generator of the order-m subgroup
        # H is isotropic iff q vanishes mod 2Z on every element
        isotropic = True
        for j in range(1, m):
            x = j * h
            if (Rational((x.T * G * x)[0, 0]) % 2) != 0:
                isotropic = False
                break
        print(f"    subgroup of order {m}: isotropic = {isotropic}")
        if isotropic:
            proper_even_overlattices += 1
    check("number of proper even invariant overlattices",
          proper_even_overlattices, CLAIMED_N_PROPER_EVEN_OVERLATTICES)


print()
print("=" * 74)
n_fail = sum(1 for v in results.values() if not v)
print(f"SUMMARY: {len(results) - n_fail}/{len(results)} checks passed, {n_fail} failed")
print("=" * 74)
raise SystemExit(1 if n_fail else 0)
