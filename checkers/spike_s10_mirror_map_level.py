#!/usr/bin/env python3
"""
Bounded feasibility spike: can we get an independent handle on d=20 for
cooper_s10 via the Dolgachev route (family is M_n-polarized  =>  T = U+<2n>)?

Method: build the mirror map from the Picard-Fuchs data by exact Frobenius,
FIRST validating the machinery reproduces the known s7 coordinate (A279618),
THEN applying the identical construction to s10 and testing integrality.

All arithmetic exact (Fraction). No floating point anywhere.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path

REPO = Path.home() / "SocrateAI-Scientific-Agora-K3-DarkMatter"
NMAX = 26

# Cooper parameters (a,b,c,d), hash-pinned refs/cooper_sequences.md (S1),
# Gorodetsky p.3 table. NOTE: this 'd' is a recurrence coefficient, NOT the
# lattice determinant.
PARAMS = {"s7": (13, 4, -27, 3), "s10": (6, 2, -64, 4)}

# Recurrence (same file):
#   (n+1)^3 u_{n+1} = (2n+1)(a n^2 + a n + b) u_n - n(c n^2 + d) u_{n-1}


# ---- dual numbers  x = a + b*eps  (for the Frobenius eps-derivative) ------
class D:
    __slots__ = ("a", "b")
    def __init__(self, a, b=0): self.a, self.b = F(a), F(b)
    def __add__(s, o): return D(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return D(s.a - o.a, s.b - o.b)
    def __mul__(s, o): return D(s.a * o.a, s.a * o.b + s.b * o.a)
    def __truediv__(s, o):
        return D(s.a / o.a, (s.b * o.a - s.a * o.b) / (o.a * o.a))
    def __repr__(s): return f"({s.a}+{s.b}eps)"


def frobenius(params, nmax):
    """Return (f0, g): f0 = sum u_n z^n (holomorphic solution),
    g = sum u_n'(0) z^n (the non-log part of the second solution)."""
    a, b, c, d = params
    u = [D(1, 0)]                      # u_0 = 1, independent of eps
    prev = D(0, 0)                     # u_{-1} = 0
    for n in range(0, nmax):
        lead = D((n + 1) ** 3, 3 * (n + 1) ** 2)          # (n+eps+1)^3
        t1 = D(2 * n + 1, 2) * D(a * n * n + a * n + b, a * (2 * n + 1))
        t2 = D(n, 1) * D(c * n * n + d, 2 * c * n)
        nxt = (t1 * u[n] - t2 * prev) / lead
        prev = u[n]
        u.append(nxt)
    return [x.a for x in u], [x.b for x in u]


# ---- exact power-series helpers (lists of Fractions, index = power) -------
def ps_mul(A, B, n):
    out = [F(0)] * (n + 1)
    for i, ai in enumerate(A[:n + 1]):
        if ai:
            for j, bj in enumerate(B[:n + 1 - i]):
                if bj:
                    out[i + j] += ai * bj
    return out


def ps_inv(A, n):
    assert A[0] != 0
    out = [F(0)] * (n + 1)
    out[0] = 1 / A[0]
    for k in range(1, n + 1):
        s = F(0)
        for i in range(1, k + 1):
            s += A[i] * out[k - i]
        out[k] = -s / A[0]
    return out


def ps_exp(A, n):
    """exp of a series with A[0] == 0, via  E' = A' E."""
    assert A[0] == 0
    E = [F(0)] * (n + 1)
    E[0] = F(1)
    for k in range(1, n + 1):
        s = F(0)
        for i in range(1, k + 1):
            s += i * A[i] * E[k - i]
        E[k] = s / k
    return E


def series_reverse(Q, n):
    """Given q = z + c2 z^2 + ... (as coefficient list Q with Q[0]=0, Q[1]=1),
    return z as a series in q, by iterative substitution."""
    Z = [F(0)] * (n + 1)
    Z[1] = F(1)
    for k in range(2, n + 1):
        # compose Q(Z) up to order k and force it to equal q
        comp = [F(0)] * (n + 1)
        power = [F(0)] * (n + 1); power[0] = F(1)     # Z^0
        for j in range(1, k + 1):
            power = ps_mul(power, Z, n)               # Z^j
            if Q[j]:
                for i in range(n + 1):
                    comp[i] += Q[j] * power[i]
        Z[k] -= comp[k]
    return Z


def mirror_map(params, nmax):
    f0, g = frobenius(params, nmax)
    ratio = ps_mul(g, ps_inv(f0, nmax), nmax)     # g/f0, constant term 0
    E = ps_exp(ratio, nmax)                        # exp(g/f0)
    # q = z * E  ->  as a series in z with q[1] = 1
    Q = [F(0)] * (nmax + 1)
    for i in range(nmax):
        Q[i + 1] = E[i]
    Z = series_reverse(Q, nmax)                    # z as a series in q
    return f0, Q, Z


def read_bfile(p):
    vals = []
    for line in Path(p).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        vals.append(int(line.split()[1]))
    return vals



# ---- level machinery (eta quotients, deg-2 rational fit, controls) --------
def euler(nmax, d=1):
    A=[F(0)]*(nmax+1); A[0]=F(1)
    for n in range(1, nmax//d+1):
        for i in range(nmax, d*n-1, -1): A[i]-=A[i-d*n]
    return A

def ps_pow(A,e,n):
    if e==0:
        r=[F(0)]*(n+1); r[0]=F(1); return r
    if e<0: return ps_pow(ps_inv(A,n),-e,n)
    r=[F(0)]*(n+1); r[0]=F(1)
    for _ in range(e): r=ps_mul(r,A,n)
    return r

def eta_quotient(divs,exps,nmax):
    """t = q * prod_d E(q^d)^{r_d}; weight 0 and leading q^1 are imposed by
    the caller via sum r_d = 0 and sum d*r_d = 24 (that pair forces the
    level-7 coordinate q(E(q^7)/E(q))^4, which is how it was validated)."""
    t=[F(0)]*(nmax+1); t[0]=F(1)
    for d,r in zip(divs,exps): t=ps_mul(t,ps_pow(euler(nmax,d),r,nmax),nmax)
    return [F(0)]+t[:nmax]

def nullspace(rows,ncols):
    M=[r[:] for r in rows]; piv=[]; r=0
    for c in range(ncols):
        p=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; pv=M[r][c]; M[r]=[x/pv for x in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]!=0:
                f=M[i][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        piv.append(c); r+=1
        if r==len(M): break
    free=[c for c in range(ncols) if c not in piv]
    if not free: return []
    fc=free[0]; sol=[F(0)]*ncols; sol[fc]=F(1)
    for i,c in enumerate(piv): sol[c]=-M[i][fc]
    return sol

def deg2_fit(z,t,nmax,n_solve,verify_at):
    t2=ps_mul(t,t,nmax); zt=ps_mul(z,t,nmax); zt2=ps_mul(z,t2,nmax)
    one=[F(0)]*(nmax+1); one[0]=F(1)
    cols=[z,zt,zt2,[-x for x in one],[-x for x in t],[-x for x in t2]]
    rows=[[c[k] for c in cols] for k in range(n_solve)]
    sol=nullspace(rows,6)
    if not sol or all(x==0 for x in sol): return False,None
    for k in verify_at:
        if sum(sol[j]*cols[j][k] for j in range(6))!=0: return False,sol
    return True,sol

def divisors(N): return [d for d in range(1,N+1) if N%d==0]

def enum_exps(ds,bound):
    k=len(ds); d1,d2=ds[0],ds[1]
    if k==2:
        r2,rem=divmod(24,(d2-d1))
        if rem==0 and abs(r2)<=bound: yield (-r2,r2)
        return
    for rest in product(range(-bound,bound+1),repeat=k-2):
        S=sum(rest); T=sum(d*r for d,r in zip(ds[2:],rest))
        num=24-T+d2*S; den=d1-d2
        if den==0 or num%den: continue
        r1=num//den; r2=-S-r1
        if abs(r1)<=bound and abs(r2)<=bound: yield (r1,r2)+rest

def hits_for(z,N,nmax,bound=10):
    out=[]
    for e in enum_exps(divisors(N),bound):
        t=eta_quotient(divisors(N),list(e),nmax)
        ok,sol=deg2_fit(z,t,nmax,14,[24,32,40])
        if ok: out.append((e,sol))
    return out

def main():
    NM=44
    f7,Q7,Z7=mirror_map(PARAMS["s7"],NM)
    f10,Q10,Z10=mirror_map(PARAMS["s10"],NM)
    print("VALIDATION  s7 u_n :",[int(x) for x in f7[:6]],"(A183204)")
    print("VALIDATION  s10 u_n:",[int(x) for x in f10[:6]],"(A005260)")
    a=[int(x) for x in Z7[1:12]]
    ref=[1,-9,30,-15,-240,978,-1463,-2361,18201,-42800,15624]
    print("VALIDATION  s7 z(q) == A279618 :",a==ref)
    print("RESULT      s10 z(q) first terms:",[int(x) for x in Z10[1:9]])
    print("RESULT      s10 z(q) integral   :",all(x.denominator==1 for x in Z10[1:]))
    print()
    for label,z,N in (("s7",Z7,7),("s10",Z10,10)):
        print(f"{label}: level-{N} hits =",[e for e,_ in hits_for(z,N,NM)])
    print()
    print("CROSS-LEVEL CONTROLS (s10 must hit ONLY 10):")
    for N in [2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
        h=hits_for(Z10,N,NM)
        print(f"   level {N:>3}: {len(h)} hit(s)",flush=True)

if __name__=="__main__":
    main()
