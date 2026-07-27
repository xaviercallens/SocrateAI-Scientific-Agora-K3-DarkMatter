# STREAM2 — U1 executed: the cooper_s7 monodromy lattice is U ⊕ ⟨14⟩ [Tier B]

**Date:** 2026-07-27 · **Executor:** fresh-context Stream 2 agent (per the route design's
E-010 discipline: the route was designed 2026-07-26 and deliberately NOT executed then).
**Spec:** `docs/U1_ROUTE_DESIGN_2026_07_26.md`, executed in its stated order.
**Code:** `checkers/check_U1_lattice.py` · **Controls:** `checkers/test_U1_controls.py`
**Certificate:** `data/certificates/C2_cooper_s7_v4_DRAFT.json` (DRAFT — pending T0;
v3 stays live and is not superseded).

## 0. Headline (all values computed at runtime, none typed)

The joint monodromy-invariant lattice of the cooper_s7 family — the orbit lattice of the
cusp-invariant isotropic vector f under the computed monodromy group, in its primitive
even scaling — has

- Gram matrix `[[0,0,-1],[0,14,0],[-1,0,0]]` → **det = −14**, signature (2,1), even;
- discriminant group **ℤ/14** with discriminant form q = **1/14 mod 2ℤ** on a generator;
- derived **2n = 14** from the divisibility of (T_cusp − 1)² on the lattice;
- an **explicit integral base change (det 1) realizing U ⊕ ⟨14⟩** — verified exactly;
- **zero** proper even monodromy-invariant overlattices.

The identical pipeline on cooper_s10 (different-level negative control) derives det = −20,
2n = 20, U ⊕ ⟨20⟩ — the pipeline discriminates levels and does not manufacture −14.

Identification of this lattice with the transcendental lattice T of the family is Tier B
(derived, not kernel-proven); the derivation chain and its two non-mechanical links are
in §4. Under that identification, **T ≅ U ⊕ ⟨14⟩ [B, derived]** — the U1 residual closes.

## 1. What was computed, in the route design's order

**Stage 0 — framework re-derived before use** (route design: "re-derive its claims
before use, not cite them"). Symbolically in sympy, with n a free symbol: the Dolgachev
§7 period shape ϖ = g + τe − nτ²f satisfies Q(ϖ,ϖ) = 0, Q(ϖ,∂ϖ) = 0,
(ϖ,ϖ̄) = 4ny² > 0, and **Q(∂τϖ,∂τϖ) = 2n exactly** (the route design's Yukawa claim);
the cusp translation T is integral, carries n in the lattice basis, and its matrix in
Frobenius-flag coordinates is `[[1,0,0],[1,1,0],[1,2,1]]` — **n-free, so the cusp
monodromy cannot see n** (route-design claim 1, re-derived); the invariant bilinear form
in flag coordinates is **−2n × the polarization of y₀y₂ − y₁²** (this is the "derive the
right bilinear form" instruction — the quadric normalization is derived, not assumed);
the SL₂ → SO(1,2) representation was re-derived from scratch on binary quadratic forms
and passes Gram-preservation and equivariance. (The A(g) matrix as printed in the OCR of
Dolgachev differs from the from-scratch derivation in two denominators — 1/n vs 1/√n,
an OCR/basis-scaling artifact; nothing downstream uses the printed matrix.)

**Stage 1 — U1a-3, exact q-series Yukawa** (sympy/Fraction rationals, no floats).
Both operators are derived at runtime from `refs/recurrences_v1.json` (hash-recorded);
the L₃ theta-coefficients are cross-checked against the independent Lean-provenance
table in `scripts/compute_L3_monodromy.py`. Results:
- mirror maps computed independently from L₂ and from L₃ **agree exactly to q³⁵**;
- the s7 mirror map z(q) **equals the pinned Γ₀(7)+ Hauptmodul b-file (A279618)
  coefficient-for-coefficient** — external validation of the Frobenius normalization;
- the Yukawa exponents are derived by exact residues: Y_zz ∝ z⁻²(1+z)⁻¹(1−27z)⁻¹;
- the mirror-normalized two-point Yukawa Y_ττ(q) is **constant to q³¹** (full computed
  order; the two top orders are truncation-padding and excluded by construction).

**Finding (honesty item the task demanded):** the constancy is the checkable content of
stage 1, and even it is mathematically forced once L₃ = Sym²(L₂) holds (Tier A, kernel-
proven) — so stage 1 is a *pipeline-consistency control*, not independent evidence. The
**value** of the constant in any ODE-only normalization is a convention (it computes to
1 in the C = 1 normalization used); the value **14 is not extractable independently of
the U1a-2 integral-lattice computation**. It is fixed only in stage 3, where the derived
2n = 14 = ⟨e,e⟩ realizes Q(∂τϖ,∂τϖ) = 2n on the actual integral lattice. Recorded as
predicted by the route design's own caution; no independent check was faked.

**Stage 2 — U1a-2, elliptic monodromies.** Numerical analytic continuation of L₂ in the
MUM Frobenius basis (A, B̂), B̂ = (A log z + g)/2πi, at 60-digit working precision
(Taylor-series stepping, order 140, step ratio 0.35, tail bounds asserted < 1e−45).
The finite loci are computed at runtime as the roots of the leading theta-coefficient:
{−1, 1/27}. Machinery control: the numerically continued loop around z = 0 reproduces
the analytically known cusp matrix `[[1,1],[0,1]]` to **3e−61**. Both elliptic loops give
matrices with det = −1 and M² = I to ~1e−59 (as the {0, ½} exponents require — E-007's
twist, confirmed again). Numerically, √7 emerges uninvited: M(1/27) = (i/√7)`[[0,1],[−7,0]]`,
M(−1) = (i/√7)`[[7,4],[−14,−7]]`. Their Sym² matrices are rational; recognition uses a
loud 1e−35 gate (largest observed residual ~1e−59) and denominators come out {1, 7}.
Exact post-verification: involutions, and the three-loop product matches the infinity
monodromy predicted by the (runtime-computed) ∞-exponents {1/3, 2/3} (trace 0, order 3).

**Stage 3 — exact lattice pipeline** (sympy rationals only). The joint invariant
symmetric form exists and is **unique up to scale** (solution space dim 1; sign fixed by
the stage-0 positivity re-derivation); the orbit lattice of f stabilizes with basis
diag-related `[[1,0,0],[0,14,0],[0,0,7]]` in flag coordinates and is closed under all
generators and inverses (exact); restricting the form and rescaling primitively-even
gives the headline Gram. The explicit U-splitting: f is primitive with div(f) = 1, so
f completes to a hyperbolic pair and the orthogonal complement is ⟨14⟩ — the base change
is exhibited and `SᵀGS = U ⊕ ⟨14⟩` is checked exactly.

## 2. Controls (all mandatory, all run, all pass — `checkers/test_U1_controls.py`)

1. **Different-level:** identical pipeline on cooper_s10 → det = −20, 2n = 20,
   U ⊕ ⟨20⟩ (its own level's values; asserted ≠ the s7 results as computed-vs-computed
   inequality — no expectation is typed). The route design offered s10 as the
   discriminating control; the level-1 E-series family was not needed.
2. **Scrambled matrix**, three modes: (a) raw entry perturbation → fails loudly at the
   involution gate; (b) conjugated involution → fails loudly at the infinity-product
   gate; (c) unit control directly on the invariant-form step → the joint invariant
   form **vanishes** (dim 0) for a scrambled matrix. The invariant-lattice step can fail,
   and does, on corrupted input.
3. **Yukawa q-independence:** constant to full computed order in the real run; a
   deliberately corrupted mirror map breaks the constancy check loudly (the check can fail).

Also standing: the full v0.3.4 regression suite re-run green after these additions, and
`scripts/check_tier_language.py` reports 0 violations including this brief.

## 3. U1b — status: replaced by a stronger mechanical step, not executed as designed

The route design's U1b (one-class genus via Eichler, requiring Cassels Ch. 11 fetched
and read, 2-adic spinor norms done properly) exists to upgrade "same genus as U ⊕ ⟨14⟩"
to "isometric to U ⊕ ⟨14⟩". The computation made that upgrade unnecessary **for the
computed lattice**: an explicit integral basis realizing U ⊕ ⟨14⟩ was found and verified
exactly (§1 stage 3), which is a constructive isometry — strictly stronger than a genus
argument. Consequently **Cassels was not fetched and no 2-adic spinor-norm claim is made
anywhere**; nothing was hand-waved because nothing 2-adic is asserted. If T0 wants the
genus statement *about the abstract genus of U ⊕ ⟨14⟩* on record independently (e.g. for
the write-up), that remains open literature work — flagged, not improvised.

## 4. Honest epistemic status

- **Tier A (unchanged):** L₃ = Sym²(L₂) (Lean, Stream 1). Used, not re-proven here.
- **Tier B — established by this run, modulo the two links below:** the monodromy
  lattice of the cooper_s7 family is U ⊕ ⟨14⟩; derived 2n = 14; disc form ℤ/14, 1/14.
  - **Link 1 (numerics → exact):** the Sym² monodromy entries enter via rational
    recognition of 60-digit numerics (residuals ~1e−59 against a 1e−35 gate), followed
    by exact structural verification (involutions, infinity relation, invariant form,
    closure). A conspiracy of errors surviving all exact gates is not credible but the
    step is numerics-backed, hence Tier B, not A.
  - **Link 2 (monodromy lattice → T):** equating the computed lattice with the
    transcendental lattice T of the family uses the read framework sources (Dolgachev
    Thm 7.1/§7 p.20; Doran Thm 5.13 — fetched, read, hash-pinned; re-derived in stage 0
    where computable). Within the computation itself the identification is pinned up to
    two enumerable ambiguities: (i) even invariant overlattices of the computed lattice —
    **enumerated: none**; (ii) an overall integral rescaling of the form on the orbit
    lattice (T could a priori carry λ·G with λ > 1) — this branch is excluded by the
    framework's T = U ⊕ ⟨2n⟩ shape, not by computation, and is the honest residual gap.
    Three independently computed indicators converge on n = 7 (Hauptmodul level 7 per
    `HAUPTMODUL_S7_GAMMA07PLUS.json`; the √7 in the elliptic matrices; det −14/2n = 14).
- **Not claimed:** no Kodaira types (E-007/8/9 stand), no ρ/T rank changes (ρ = 19,
  T = 3 per v3 stands), no physical coupling of any kind (VISION §1.3), nothing about
  Gate E scoring.
- **Verdict: U1a PASS (with all controls); U1b discharged constructively for the
  computed lattice; overall U1 CLOSED at Tier B**, pending T0 review of the draft
  certificate. Per the route design's "on U1 PASS" item: the S3-00 2(b) re-scope option
  is hereby put to T0 (decision, not action — nothing in S3-00 was touched).

## 5. Files

- `checkers/check_U1_lattice.py` — pipeline (stages 0–3), standalone, exit 0/3.
- `checkers/test_U1_controls.py` — the mandatory controls, standalone.
- `data/certificates/C2_cooper_s7_v4_DRAFT.json` — DRAFT, pending T0 + does not
  supersede v3.
- `TODO.md` — U1 item updated.
- This brief.

Regression command additions (both green):
```bash
python3 checkers/check_U1_lattice.py            # U1 pipeline, s7
python3 checkers/test_U1_controls.py            # U1 negative controls
```

**Generated-by:** Fable 5 (Stream 2, fresh-context U1 execution) |
**Verified-by:** check_U1_lattice.py structural assertions + test_U1_controls.py (all
green 2026-07-27) + full v0.3.4 regression re-run + check_tier_language.py |
**Reviewed-by:** pending T0 (Xavier)
