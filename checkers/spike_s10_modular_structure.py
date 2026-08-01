#!/usr/bin/env python3
"""Modular structure of the s10/s7 mirror-map coordinates: Ligozat cusp
divisors + Atkin-Lehner action. Companion to spike_s10_mirror_map_level.py.
Establishes WHICH modular group each coordinate belongs to."""
from fractions import Fraction as F
from math import gcd
from itertools import product
def divisors(N): return [d for d in range(1,N+1) if N%d==0]

def ligozat_orders(N, r):
    """ord of prod eta(d tau)^{r_d} at each cusp 1/c, c|N (Ligozat)."""
    out={}
    for c in divisors(N):
        s=sum(F(gcd(c,d)**2 * r.get(d,0), d) for d in divisors(N))
        out[c]=F(N,24*gcd(c*c,N))*s
    return out

def report(N, exps, label):
    ds=divisors(N); r=dict(zip(ds,exps))
    o=ligozat_orders(N,r)
    tot_z=sum(v for v in o.values() if v>0); tot_p=-sum(v for v in o.values() if v<0)
    wt=F(sum(exps),2)
    print(f"  {label}  exps={exps}")
    print(f"     weight={wt}  orders at cusps 1/c: { {c:str(v) for c,v in o.items()} }")
    print(f"     sum={sum(o.values())}  degree(zeros)={tot_z} degree(poles)={tot_p}"
          f"   -> {'HAUPTMODUL (degree 1)' if tot_z==1 and tot_p==1 else f'degree {tot_z} map, NOT a Hauptmodul'}")

print("s7, level 7:")
report(7, (-4,4), "t7")
print("\ns10, level 10 (the three hits):")
for e in [(-4,4,-4,4),(-2,-2,2,2),(6,-6,-6,6)]:
    report(10, e, "t")
print("\nSearch: is ANY level-10 weight-0 eta quotient a genuine Hauptmodul?")
from itertools import product
found=[]
for e in product(range(-12,13),repeat=4):
    if sum(e)!=0: continue
    ds=divisors(10); r=dict(zip(ds,e))
    o=ligozat_orders(10,r)
    tz=sum(v for v in o.values() if v>0); tp=-sum(v for v in o.values() if v<0)
    if tz==1 and tp==1 and all(v.denominator==1 for v in o.values()):
        found.append((e,{c:str(v) for c,v in o.items()}))
print(f"  {len(found)} degree-1 (Hauptmodul) eta quotients found; first few:")
for e,o in found[:6]: print("   ",e,o)

N=10; ds=divisors(N)
# Atkin-Lehner w_Q permutes cusps 1/c by  c -> c' with  c' = Q/gcd(c,Q) * gcd(c,N/Q)... use the
# standard action on the set of divisors: w_Q sends the cusp class c to  (Q/g)*(c/g') pattern.
# For N=10 squarefree, w_Q acts on c|N by  c -> Q*c / gcd(c,Q)^2.
def wQ(c,Q,N):
    g=gcd(c,Q); return (Q*c)//(g*g)

print("Cusp permutations for N=10 (cusps indexed by c | 10):")
for Q in (2,5,10):
    print(f"  w_{Q}: " + ", ".join(f"{c}->{wQ(c,Q,N)}" for c in ds))

print("\nFor each fitted coordinate: which AL involutions fix its divisor?")
for e in [(-4,4,-4,4),(-2,-2,2,2),(6,-6,-6,6)]:
    r=dict(zip(ds,e)); o=ligozat_orders(N,r)
    div={c:o[c] for c in ds}
    line=f"  exps={e} div={ {c:str(v) for c,v in div.items()} }"
    inv=[];anti=[]
    for Q in (2,5,10):
        pushed={wQ(c,Q,N):div[c] for c in ds}
        if all(pushed[c]==div[c] for c in ds): inv.append(Q)
        elif all(pushed[c]==-div[c] for c in ds): anti.append(Q)
    print(line)
    print(f"     invariant under w_{inv}   anti-invariant (t -> const/t) under w_{anti}")
