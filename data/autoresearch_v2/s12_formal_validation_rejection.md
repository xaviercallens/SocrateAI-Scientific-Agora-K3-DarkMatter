# S₁,₂ (A112019) — Formal Validation & Rejection Document

**Date:** 2026-07-14 · **Status:** FORMALLY REJECTED per Phase 8.B gate battery
**Candidate ID:** s12_v1_primary · **OEIS:** A112019 · **v1 Status:** flagship K3 hypothesis

## Executive summary

S₁,₂ = Σₖ C(n,k) C(n+k,k)² was v1's primary K3-type candidate and the anchor of the entire v1 physics pipeline. Phase 8.B gate battery (all 7 gates, real tools) ran on it identically to all 12 other pool members. **Result: REJECTED on two independent grounds:**

1. **G1-1 Classification (Exact ODE):** ODE order **2**, not 3 → **elliptic-type** (literature: weight-2 form), NOT K3-type. Confirmed exact, held-out to n=110.
2. **G1-3 Mirror-Map Integrality:** The minimal-operator Picard–Fuchs mirror map is **non-integral**: q₂ = 81/8. Fails immediately. v1's "PASS" was an artifact of v1 using the non-minimal order-3 operator's log solution.

Both are mathematically rigorous, independent grounds. S₁,₂ does not survive Phase 8.B.

## Gate-by-gate record

| Gate | Criterion | Result | Evidence |
|---|---|---|---|
| **G1-1** | ODE order = 3 (K3-type) | **FAIL** | ODE(rho=2, delta=5); weight-2 characteristic; Picard-Fuchs distinguishes from weight-3 via ODE order |
| **G1-2** | Weil bounds |PASS | |a_p| ≤ 2p for all p ∈ {5..199} ✓ |
| **G1-3** | Mirror-map integral over 30 coeffs | **FAIL** | q₁=1 (normalization), **q₂=81/8 (non-integral)**, Frobenius recursion on minimal ODE exact |
| **G1-4** | Fuchs criterion + monodromy | PASS (computable) | 5 singular points, all regular; monodromy computed (|det M−1|≈1e-24) |
| **G2-1** | Achievable mass contour | PASS (non-discrim) | Mass identical to all candidates at common (τ,V); GAP-2 degeneracy |
| **G2-2** | GD-1 no-go | PASS | Survives at reference point (3.44e-21 eV > 1.59e-21 eV floor) |
| **G2-3** | M87* superradiance | PASS (non-discrim) | Pool-uniform at α=0.168; no bare survival (τ≈2.5 Myr < Salpeter) |

## Why v1's result was wrong

v1 used `mirror_map_integrality.py` which computes the log solution y₁ for a given (A,B) via the Beukers harmonic-sum formula. For A=1, B=2, v1's code applied the order-3 shift-recurrence operator's log solution — which is **not the Picard–Fuchs operator**. The minimal Picard–Fuchs operator is order 2 (confirmed in Phase 8.B), and its log solution differs starting at index 1 (q₂ onwards). v1 therefore was solving the wrong ODE. Phase 8.B uses Frobenius recursion on the exact ODE (validated against Beukers on the two classical anchors: A005259, A005258), which is the correct method.

## Consequence for v1 physics

v1's entire stiffness chain depended on S₁,₂ and S₂,₁ as a "two-vacuum" K3 pair. With S₁,₂ reclassified elliptic:
- The paired mass ratio √(1014/336) ≈ √K3 stiffness has no K3 geometry to anchor it.
- The v1 phenomenology (mass ~1.8e-21 eV, M87* screening, PTA signal) was derived from this wrong-geometry anchor.

**The v1 framework does not survive into Phase 8.C.** The new pool (13 candidates, 6 promoted) replaces it with literature-grounded K3 sporadics.

## Formal rejection authority

This rejection is based on:
- **G1-1 ODE-order classification** (exact modular-prime nullspace + Fraction arithmetic, held-out validation to n=110, literature answer keys control A005258/A005259 recovered exactly).
- **G1-3 Frobenius log-solution** (minimal operator, validated identically on controls).
- **Dual independent failure modes** (geometry AND integrality), not a single threshold dependence.

No further revocation possible without a new computation method that contradicts exact-arithmetic results.
