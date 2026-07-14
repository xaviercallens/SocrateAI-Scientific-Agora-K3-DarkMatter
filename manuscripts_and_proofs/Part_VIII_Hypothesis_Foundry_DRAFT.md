# Part VIII: The Hypothesis Foundry — A Gate-Driven Search for K3-Type Dark-Sector Candidates

**Status:** DRAFT (markdown; LaTeX/PDF conversion pending) · **Date:** 2026-07-14
**Naming note:** "Part VII" is already assigned to `Part_VII_TDA_30Arcmin_Supercluster_Analysis.tex` (merged from a concurrent session, commit 4eeff24). This manuscript is Part VIII.

## Abstract (draft)

We report the results of AutoEvolve R2, a gate-driven evolutionary search over binomial-sum sequences for K3-surface-type Picard–Fuchs geometry, applied to the dark-sector axion framework of this programme. Starting from a corrected exact-arithmetic classifier (Phase 8.A) that reclassifies the v1 flagship candidate S₁,₂ as elliptic-type rather than K3-type, we screened 13 candidates through a seven-gate battery (Phase 8.B) covering exact recurrence order, Weil bounds, mirror-map integrality, Fuchs/monodromy structure, and three physics viability checks (GD-1 stream heating, M87* superradiance, PTA/Lyman-α consistency). Six candidates survive as literature-grounded or in-session-verified K3-type geometries; S₁,₂ is formally rejected on two independent grounds. Of these, three finalists — two Cooper (2012) sporadic sequences and one novel in-session discovery — receive Lean 4 kernel-verified formal proofs of their governing recurrences. We report negative and corrective findings first, per this programme's standing methodology.

## 1. Negative and corrective findings (reported first)

1. **v1's shift-recurrence-order classifier was inverted** relative to the correct discriminant (Phase 8.A): the minimal generating-function ODE order (2 = elliptic, 3 = K3), not the shift-recurrence order, distinguishes the geometry. Verified against literature answer keys (A005258 elliptic, A005259 K3).
2. **S₁,₂ (A112019), v1's flagship candidate, is formally rejected** (this document, §3): its minimal Picard–Fuchs operator has ODE order 2 (elliptic), and its mirror map on that minimal operator is non-integral (q₂ = 81/8). v1's contrary "K3, integral" result used the log solution of a non-minimal, higher-order operator.
3. **A006077's literature "K3-class" tag is falsified** by exact classification: ODE order 2 (elliptic), consistent with its (n+1)²-type recurrence leading coefficient (Zagier ζ(2) class).
4. **A monodromy-verification sign bug** (found and fixed 2026-07-14) had misclassified every tested singular point as irregular since 2026-07-11, silently skipping all monodromy integration; the fix was verified against the classical Apéry ζ(3) operator before being trusted on the pool.
5. **The physics-viability gates (G2) are non-discriminating** across the pool at any common (τ, 𝒱) normalization: single-instanton domination of the mirror-map series makes the achievable axion mass identical for all 13 candidates. Candidate selection for Phase 8.D therefore rests on the mathematical gates (G1), not the physics gates.
6. **An S₁₂-inspired empirical hybrid** (Σₖ C(n,k)C(n+k,k)²C(2k,k), proposed as a 7th trial candidate) **failed the first gate**: no minimal ODE was found within the standard search window, and its term growth is incompatible with a Picard–Fuchs structure. Reported as a negative result, not silently dropped.

## 2. Method summary

- **Classification (G1-1):** exact modular+Fraction nullspace search for the minimal shift recurrence and the minimal generating-function ODE, held-out validated to n=110, controlled against literature answer keys embedded in the same scan.
- **Modularity (G1-2):** Stienstra–Beukers unit-root a_p recipe, Weil bound checks at 44 primes, comparison against a small cited LMFDB weight-3 newform subset (non-exhaustive by design).
- **Integrality (G1-3):** Frobenius log-solution recursion on the *minimal* operator's theta-form, validated by exact agreement with the classical Beukers harmonic-sum formula on both literature controls before being trusted on novel candidates.
- **Fuchs/monodromy (G1-4):** exact polynomial divisibility test for the Fuchs regularity criterion (corrected sign bug, see §1.4), RK4 numerical monodromy integration at 50-digit precision for regular singular points.
- **Physics (G2-1..4):** achievable-mass contour over a (τ, 𝒱) grid (never a fitted point), GD-1 stream-heating no-go using the exact rational constants of the `cy_axion_no_go` Lean theorem, Dolan continued-fraction M87* superradiance solver (revalidated against its own published benchmark before use), and PTA/Lyman-α literature-bound comparison.

## 3. S₁,₂ formal rejection

See `data/autoresearch_v2/s12_formal_validation_rejection.md` for the full gate-by-gate record. Summary: ODE order 2 (not 3), mirror map non-integral at q₂ = 81/8 on the minimal operator. Both grounds independent and exact-arithmetic verified; retained in the pool only as the geometry-negative comparison point alongside the literature-confirmed elliptic control S₂,₁ (A005258).

## 4. GATE-C finalists (Phase 8.D)

Selection: **Novel-heavy** (user directive, 2026-07-14) — prioritizes the strongest in-session discovery alongside independently literature-anchored objects, rather than the most conservative literature-only set.

### 4.1 t103 (OEIS A276536)

Term: T103(n) = Σₖ C(n,k) C(2k,k)³. In-session sieve discovery (Phase 8.A, 3-factor family scan). G1-1: minimal generating-function ODE order 3, degree 6 (K3-type), held-out to 62 terms. Its minimal *shift* recurrence — needed for Lean's `decide`-based finite verification — required widening the search window beyond the Phase 8.B default (order 4, degree 3, found at ρ≤4/δ≤8); this is a different, larger annihilating operator than the order-3 ODE used for the K3 classification, and both are valid. Verified exactly for n ∈ [0, 195] (196 checks) before Lean formalization; `decide`-proved for n ∈ [0, 20] with zero `sorry` in `T103Recurrence.lean`.

### 4.2 Cooper s₇ (OEIS A183204)

Term: Σⱼ C(n,j)² C(2j,n) C(j+n,j) (Wadim Zudilin form, per OEIS). Cooper (2012), level-7 sporadic, weight-3 class. Minimal shift recurrence: order 2, degree 3, with leading coefficient P₂(n) = (n+2)³ exactly. Verified to n=197; `decide`-proved n ∈ [0,20], zero `sorry`.

### 4.3 Cooper s₁₀ (OEIS A005260)

Term: Σₖ C(n,k)⁴. Cooper (2012), level-10 sporadic. Minimal shift recurrence: order 2, degree 3, leading coefficient again P₂(n) = (n+2)³ — an observation, not a claimed physical significance, shared with s₇'s recurrence structure. Verified to n=197; `decide`-proved n ∈ [0,20], zero `sorry`.

### 4.4 A note on monodromy determinants

For all three finalists, some regular singular points have monodromy determinant −1, not +1 (§1.4 fix notwithstanding — this is expected, not an artifact of the earlier sign bug). By Abel's/Liouville's formula this reflects a half-integer residue of the sub-leading/leading coefficient ratio at that point and is a normal feature of order-3 (and higher) Fuchsian operators; it does not indicate irregularity or an unreliable computation, and the corrected `k3_monodromy_verification.py` docstring (2026-07-14) now states this explicitly rather than labeling the check "symplecticity."

## 5. Outstanding items for the next drafting pass

- LaTeX/PDF conversion in house style (see `Part_VII_TDA_30Arcmin_Supercluster_Analysis.tex` for the template).
- Observatory targeting dossier (D-5): per-finalist PTA frequency bands and superradiance timescales, formatted for an observational audience.
- Full introduction/discussion sections connecting to the Lee–Tsai bridge memo and the provenance-ledger discipline established in Parts I–VII.
- External verification invitations (D-4) are explicitly NOT part of this draft — that is an outward-facing action requiring separate user sign-off.
