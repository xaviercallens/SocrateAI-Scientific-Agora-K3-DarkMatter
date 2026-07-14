# Cooper K3 Sequence Gate Verification — Phase 8.B / 8.D

**Date:** 2026-07-14  
**Scope:** GATE-C verification record for the two Cooper sporadic sequences promoted as K3-type candidates.  
**Candidates:** `cooper_s7` (OEIS A183204) and `cooper_s10` (OEIS A005260).  

---

## 1. Candidate definitions

| name | OEIS | closed form | first terms | source |
|---|---|---|---|---|
| **Cooper s₇** | [A183204](https://oeis.org/A183204) | `CooperS7(n) = Σ_{j=0..n} C(n,j)² · C(2j,n) · C(j+n,j)` | 1, 4, 48, 760, 13840, 273504, ... | S. Cooper, *Sporadic sequences, modular forms and new series for 1/π*, Ramanujan J. 29 (2012) 163–183 — level 7 |
| **Cooper s₁₀** | [A005260](https://oeis.org/A005260) | `CooperS10(n) = Σ_{k=0..n} C(n,k)⁴` | 1, 2, 18, 164, 1810, 21252, ... | S. Cooper, *ibid.* — level 10 |

Both are independently literature-anchored weight-3 sporadic sequences. The shift recurrences are order 2, degree 3, with a clean leading coefficient `(n+2)³`.

---

## 2. Algebraic gate summary (G1-1 … G1-4)

| Gate | What it checks | `cooper_s7` | `cooper_s10` | Data source |
|---|---|---|---|---|
| **G1-1** ODE order | generating-function Picard–Fuchs ODE order | **3** (degree 4), held-out 72 terms pass | **3** (degree 4), held-out 72 terms pass | `data/autoresearch_v2/g1_1_order_classification.json` |
| **G1-2** Weil/modularity | `|a_p| ≤ 2p` weight-3 bound for 44 primes | ✅ weight-3 bound passes; LMFDB subset search not conclusive (best label `7.3.b.a` 0/13 match) | ✅ weight-3 bound passes; LMFDB subset search not conclusive | `data/autoresearch_v2/g1_2_weil_modularity.json` |
| **G1-3** mirror-map integrality | `q(z)/z` coefficients are integers | ✅ all 31 coefficients integral; `q₂ = 9` | ✅ all 31 coefficients integral; `q₂ = 4` | `data/autoresearch_v2/g1_3_mirror_integrality.json` |
| **G1-4** monodromy / Fuchsian | regular singular points, MUM at `z=0`, numeric monodromy computable | ✅ status `regular`, `mum_at_zero` true, singular points `{-1, 1/27, 0}` regular for s7; `{-1/4, 1/16, 0}` regular for s10; `det_err ≈ 2` is the expected orientation flip (see `GATE_C_DECISION.md` correction) | ✅ same for s10 | `data/autoresearch_v2/g1_4_monodromy_status.json` |

**Interpretation:** G1-1 and G1-3 are the two strongest K3-period signatures. Both Cooper sequences pass both. G1-2 is consistent with weight-3 modularity but does not produce an LMFDB match for the limited subset tried. G1-4 confirms the operators are Fuchsian with MUM point at `z=0`, which is necessary for the mirror-map construction.

---

## 3. Phenomenological gate summary (G2-1 … G2-4)

All gate computations use the **same reference mass** `m_a = 3.44481380277283 × 10⁻²¹ eV` for the GATE-C finalists (this is the GAP-2 common normalization, not an independent topological prediction; see `PHASE_8_AUTOEVOLVE_RECTIFICATION.md`).

| Gate | What it checks | `cooper_s7` | `cooper_s10` | Data source |
|---|---|---|---|---|
| **G2-1** stiffness contours | `V''(0)` (d=3 leading coefficient) and instanton sum `q_d` | `V''(0) = 1225`; `q_d` first 5: `1, 9, 132, 2310, 44574` | `V''(0) = 359`; `q_d` first 5: `1, 4, 38, 384, 4409` | `data/autoresearch_v2/g2_1_stiffness_contours.json` |
| **G2-2** GD-1 no-go | kinematic heating of GD-1 stream | ✅ `survives_at_reference_point` true; `gd1_min_mass_eV = 1.59 × 10⁻²¹` | ✅ `survives_at_reference_point` true; same `gd1_min_mass_eV` | `data/autoresearch_v2/g2_2_no_go_status.json` |
| **G2-3** superradiance bands | M87* superradiant instability (Dolan continued-fraction solver) | `bare_survival: false` at `α ≈ 0.168`; `l1m1` timescale ≈ 2.48 Myr < Salpeter 50 Myr | identical to s7 | `data/autoresearch_v2/g2_3_superradiance_bands.json` |
| **G2-4** observational screens | PTA / Lyman-α compatibility | PTA window intersects band; reference `f_ref ≈ 8.33 × 10⁻⁷ Hz` not in NANOGrav band; Lyman-α tensions if all-DM | identical to s7 | `data/autoresearch_v2/g2_4_obs_screens.json` |

**Interpretation:** G2-1 yields distinct topological stiffness invariants for the two Cooper sequences (1225 vs 359). G2-2 is satisfied at the common reference point. G2-3 reinforces that **no bare M87* survival** is expected at the reference coupling; environmental screening (e.g. Chameleon) is required. G2-4 places the reference frequency near but not inside the current NANOGrav band and flags Lyman-α tension if the axion is the totality of dark matter.

---

## 4. Lean 4 formalization

The shift recurrence and finite-range structural facts are kernel-verified in:

- `lean4_formal_proofs/Structures/CooperS7Recurrence.lean`
- `lean4_formal_proofs/Structures/CooperS10Recurrence.lean`

Each file contains:

* the exact-integer polynomial coefficients `P0`, `P1`, `P2`;
* `cooper_s7_recurrence_checked` / `cooper_s10_recurrence_checked`: `decide` proofs for `n ∈ [0, 20]`;
* the general law as an explicit `axiom` (matching `S20Recurrence.lean` pattern; full kernel proof awaits WZ certificate translation);
* `P2(n) = (n+2)³` proved by `ring`;
* `cooper_s7_pos` / `cooper_s10_pos`: all values in `Fin 20` are strictly positive (`native_decide`);
* `cooper_s7_monotone` / `cooper_s10_monotone`: strict monotonicity over adjacent pairs in `Fin 19` (`native_decide`).

CI verification is in `scripts/cross_consistency_check.sh`, "Phase 8.D: GATE-C Finalist Lean Kernel Verification".

---

## 5. Reproducibility

```bash
# Re-run the exact-rational ODE/shift classification
python scripts/autoresearch_v2_phase_a_scan.py anchors
# outputs: data/autoresearch_v2/g1_1_order_classification.json

# Re-run the full Phase 8.B gate suite
python scripts/autoresearch_v2_phase_b_all_gates.py
# outputs: data/autoresearch_v2/g1_2_weil_modularity.json
#          data/autoresearch_v2/g1_3_mirror_integrality.json
#          data/autoresearch_v2/g1_4_monodromy_status.json
#          data/autoresearch_v2/g2_1_stiffness_contours.json
#          data/autoresearch_v2/g2_2_no_go_status.json
#          data/autoresearch_v2/g2_3_superradiance_bands.json
#          data/autoresearch_v2/g2_4_obs_screens.json

# Build the Lean files
lake build Agora
```

---

## 6. Comparison with S₁₂ (negative control)

| property | `cooper_s7` / `cooper_s10` | `S₁₂` (A112019) | implication |
|---|---|---|---|
| minimal ODE order | **3** | **2** | K3-type vs elliptic |
| mirror-map `q₂` | `9` (integral) / `4` (integral) | `81/8` (non-integral) | passes / fails K3-period test |
| shift recurrence | order 2, degree 3 | order 3, degree 3 | misleading if used as geometry proxy |

This contrast is the basis of the Phase 8 rectification (`PHASE_8_AUTOEVOLVE_RECTIFICATION.md`): `S₁₂` is elliptic, while the Cooper sequences are the K3-type candidates.

---

## 7. Open items

* A full kernel proof of the **general** order-2 shift recurrence for both Cooper sequences requires translating the Wilf–Zeilberger certificate into Lean; the current files use an explicit `axiom` for the general law.
* The ODE order (3) and mirror-map integrality are currently **gate outputs** from `scripts/autoresearch_v2_phase_b_all_gates.py`, not in-kernel Lean theorems. Formalizing the Picard–Fuchs nullspace extraction and the Frobenius/mirror-map construction in Lean is a future formalization step.
* The G2-3 superradiance result says bare M87* survival is **not** obtained; the physical candidate must include an environmental-screening mechanism (e.g. Chameleon) or a different superradiance model.
