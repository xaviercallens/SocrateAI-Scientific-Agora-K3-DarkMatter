#!/usr/bin/env python3
"""
Negative / discriminating controls for the independent s10 re-derivation.

A verifier that has never failed on purpose is untested (criteria-checkers
skill). These controls establish that the PART-3 algorithm actually reads d
out of the lattice rather than being hardwired or insensitive to the input,
and that the cert's witness P is specific to s10 rather than generic.
"""
from sympy import Matrix, Rational, gcd
from itertools import product

U20 = Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 20]])
U14 = Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 14]])

P_s10_cert = Matrix([[1, -360, 120], [0, -6, 1], [0, -1, 0]])

G_s10 = Matrix([[0, 0, -1], [0, 20, 0], [-1, 0, 0]])
G_s7  = Matrix([[0, 0, -1], [0, 14, 0], [-1, 0, 0]])   # the LIVE s7 lattice


def split_off_U(G):
    """Same from-scratch algorithm as PART 3, factored so it can be re-aimed
    at other lattices. Returns (d, P) or (None, None) if it cannot split."""
    def pair(u, v):
        return (u.T * G * v)[0, 0]

    e = None
    for coeffs in product(range(-8, 9), repeat=3):
        if all(c == 0 for c in coeffs):
            continue
        if gcd(gcd(coeffs[0], coeffs[1]), coeffs[2]) != 1:
            continue
        v = Matrix(3, 1, list(coeffs))
        if pair(v, v) != 0:
            continue
        ps = [pair(v, Matrix(3, 1, [1 if i == j else 0 for i in range(3)]))
              for j in range(3)]
        if gcd(gcd(ps[0], ps[1]), ps[2]) == 1:
            e = v
            break
    if e is None:
        return None, None

    w = None
    for coeffs in product(range(-8, 9), repeat=3):
        v = Matrix(3, 1, list(coeffs))
        if pair(e, v) == 1:
            w = v
            break
    if w is None:
        return None, None
    w2 = pair(w, w)
    if w2 % 2 != 0:
        return None, None
    f = w - Rational(w2, 2) * e
    if any(f[i].q != 1 for i in range(3)):
        return None, None

    ker = Matrix.vstack((G * e).T, (G * f).T).nullspace()
    if len(ker) != 1:
        return None, None
    kv = ker[0]
    den = 1
    for i in range(3):
        den = den * kv[i].q // gcd(den, kv[i].q)
    kv = kv * den
    cont = gcd(gcd(int(kv[0]), int(kv[1])), int(kv[2]))
    k = Matrix(3, 1, [int(kv[i]) // int(cont) for i in range(3)])
    return int(pair(k, k)), Matrix.hstack(e, f, k)


fails = 0
def expect(name, cond, detail=""):
    global fails
    ok = bool(cond)
    if not ok:
        fails += 1
    print(f"[{'PASS' if ok else '*** FAIL ***'}] {name} {detail}")


print("=" * 74)
print("CONTROL 1 -- same algorithm aimed at the LIVE s7 lattice must give 14")
print("=" * 74)
d7, P7 = split_off_U(G_s7)
print(f"  d(s7) re-derived = {d7}")
expect("s7 yields d=14, not 20 (algorithm reads d from the lattice)", d7 == 14)
expect("s7 splitting really is U + <14>",
       P7 is not None and P7.T * G_s7 * P7 == U14)

print()
print("=" * 74)
print("CONTROL 2 -- tampered s10 Gram must NOT still yield 20")
print("=" * 74)
for bad_d in (18, 22, 20 + 40):
    G_bad = Matrix([[0, 0, -1], [0, bad_d, 0], [-1, 0, 0]])
    d_bad, _ = split_off_U(G_bad)
    print(f"  tampered <{bad_d}>: re-derived d = {d_bad}")
    expect(f"tampered d={bad_d} does not masquerade as 20", d_bad != 20)

print()
print("=" * 74)
print("CONTROL 3 -- the cert's s10 witness must NOT split the s7 lattice")
print("=" * 74)
cross = P_s10_cert.T * G_s7 * P_s10_cert
print(f"  P_s10^T G_s7 P_s10 =\n{cross}")
expect("s10 witness does NOT produce U + <14>", cross != U14)
expect("s10 witness does NOT produce U + <20> on s7 either", cross != U20)
expect("cross-family application is visibly non-split (off-block junk)",
       not (cross[0, 2] == 0 and cross[1, 2] == 0))

print()
print("=" * 74)
print("CONTROL 4 -- a non-unimodular 'witness' must be rejected")
print("=" * 74)
P_scaled = P_s10_cert * 2          # det = 8, not a lattice automorphism
print(f"  det(2*P) = {int(P_scaled.det())}")
expect("scaled witness is correctly not unimodular", abs(int(P_scaled.det())) != 1)
expect("scaled witness does not give U + <20>",
       P_scaled.T * G_s10 * P_scaled != U20)

print()
print("=" * 74)
print(f"CONTROLS SUMMARY: {fails} failure(s)")
print("=" * 74)
raise SystemExit(1 if fails else 0)
