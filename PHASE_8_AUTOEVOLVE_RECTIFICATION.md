# 🔬 Phase 8: AutoEvolve Rectification and the True K3 Discriminant

**Date:** 2026-07-14  
**Engine:** AutoEvolve / AlphaEvolve evolutionary sieve + Phase 8.A/B exact-rational gates  
**Subject:** Formal reclassification of $S_{1,2}$ and the elevation of Cooper $s_7$ / GATE-C candidates  
**Status:** Resolved — theory re-anchored to verified K3-type candidates

---

## 1. The Category Error in the V1 Classifier

Earlier Agora phases classified $S_{1,2}$ (OEIS A112019) as a K3 surface because it satisfies a minimal **order-3 shift recurrence**.

The Phase 8 exact-rational gate suite (G1-1 through G1-3) corrected this:

| Discriminator | V1 | V2 / Phase 8 |
|---|---|---|
| Geometry proxy | shift-recurrence order | **generating-function Picard–Fuchs ODE order** |
| Order-2 | elliptic / modular curve | **not a K3** |
| Order-3 | K3 surface | **canonical K3 Picard–Fuchs signature** |

The same exact-rational nullspace extraction over $\mathbb{Q}$ used for the $A,B$ sieve and for the AlphaEvolve neighbourhood search is the source of the corrected classification.

---

## 2. Independent Rejections of $S_{1,2}$ (A112019)

The G1-1 / G1-3 gates applied two independent K3-period tests to $S_{1,2}$ using the **minimal** Picard–Fuchs operator (order 2, degree 5).

| Diagnostic Test | $S_{1,2}$ Result | Strict K3 Requirement | Verdict |
| :--- | :--- | :--- | :--- |
| **Minimal Picard–Fuchs ODE order** | **2** (degree 5) | **3** | ❌ **FAILS** — elliptic curve |
| **Mirror-map $q_2$ coefficient** | **$81/8$** | **integral** ($\in \mathbb{Z}$) | ❌ **FAILS** — non-integral |

**Data source:** `data/autoresearch_v2/g1_3_mirror_integrality.json`, entry `s12_v1_primary`.  
**V1 false positive:** `scripts/mirror_map_integrality.py` computed the log solution from the **non-minimal order-3 shift operator** and reported all 30 coefficients as integral; the G1-3 gate recomputes on the minimal operator and exposes the fractional $q_2$.

Because the minimal ODE is order 2 and the mirror map has a non-integral second coefficient, $S_{1,2}$ does **not** pass the standard arithmetic K3-period criteria. It remains a well-defined order-2 elliptic-type period sequence, but it is not a K3 surface candidate under the Stienstra–Beukers–Zagier K3-period correspondence.

---

## 3. Convergence with the Empirical Pipeline

The V4C macroscopic tensor pipeline had already strongly preferred Cooper $s_7$ over $S_{1,2}$. The Phase 8 gates now formally explain why:

| Candidate | ODE order | Mirror map $q_2$ | Geometry | Gate status |
|---|---|---|---|---|
| $S_{1,2}$ (A112019) | 2 | $81/8$ (non-integral) | elliptic | **REJECTED** |
| Cooper $s_7$ (A183204) | 3 | $9$ (integral) | **K3-type** | **PASSES** |
| Cooper $s_{10}$ (A005260) | 3 | $4$ (integral) | **K3-type** | **PASSES** |
| T103 (A276536) | 3 | $25$ (integral) | **K3-type** | **PASSES** |
| Apery $\zeta(3)$ / $S_{2,2}$ (A005259) | 3 | $12$ (integral) | **K3-type** | **PASSES** |
| Domb (A002895) | 3 | $6$ (integral) | **K3-type** | **PASSES** |

**Data source:** `data/autoresearch_v2/g1_1_order_classification.json` (ODE orders) and `data/autoresearch_v2/g1_3_mirror_integrality.json` (mirror-map coefficients).  
The Cooper $s_7$ and T103 candidates are also Lean kernel-verified through `lean4_formal_proofs/Structures/CooperS7Recurrence.lean` and `T103Recurrence.lean` (order-4 shift recurrences and structural cubic-leading-coefficient facts, with the ODE order as the basis of K3-type classification).

---

## 4. The New K3 Candidate Pool

The exact-rational landscape now contains the following verified K3-type candidates, with $S_{1,2}$ formally retained as a negative control and $S_{2,1}$ remaining the elliptic-type companion:

| Candidate | Source | ODE order | Mirror map | Notes |
|---|---|---|---|---|
| Apery $\zeta(3)$ / $S_{2,2}$ (A005259) | 2-factor family, literature anchor | 3 | integral | classical K3 |
| Domb (A002895) | 2-factor family, literature anchor | 3 | integral | classical K3 |
| Cooper $s_7$ (A183204) | Cooper sporadic | 3 | integral | GATE-C finalist |
| Cooper $s_{10}$ (A005260) | Cooper sporadic | 3 | integral | GATE-C finalist |
| T103 (A276536) | 3-factor sieve discovery | 3 | integral | GATE-C finalist |
| t011 | 3-factor family | 3 | — | blocked at G1-3 (non-MUM, z=0 not MUM) |
| t112 | 3-factor family | 3 | integral | GATE-C finalist |
| AlphaEvolve `gen_3f_A1B1C2` | evolutionary neighbourhood search | 3 | — | queued for Phase C gates |

**Data sources:** `data/autoresearch_v2/g1_1_order_classification.json`, `data/autoresearch_v2/g1_3_mirror_integrality.json`, `data/autoresearch_v2/alphaevolve_gen_survivors.json`.

---

## 5. Reproducibility

The classifications above are obtained from exact-rational code, not manual calculation:

```bash
# G1-1: ODE order classification
python scripts/autoresearch_v2_phase_a_scan.py anchors
# output: data/autoresearch_v2/phase_a_anchors.json
#         data/autoresearch_v2/g1_1_order_classification.json

# G1-3: mirror-map integrality on the minimal operator
# (run as part of the Phase 8.B gate suite)
python scripts/autoresearch_v2_phase_b_all_gates.py
# output: data/autoresearch_v2/g1_3_mirror_integrality.json

# AlphaEvolve K3 neighbourhood search
python scripts/autoresearch_v2_alphaevolve.py
# output: data/autoresearch_v2/alphaevolve_gen_survivors.json
```

---

## 6. Conclusion

The $S_{1,2}$ / $S_{2,1}$ pair is now classified as **elliptic-type** (ODE order 2). The K3-type candidate pool is re-anchored to the GATE-C finalists and the Apery/Domb literature anchors, all of which satisfy order-3 Picard–Fuchs ODEs and integral mirror-map coefficients.

This is a self-correction driven by exact-rational algebra. The arithmetic facts (mass ratio bounds, GD-1 No-Go, chameleon stability) remain kernel-verified; their geometric interpretation now attaches to the GATE-C K3 candidates, not to $S_{1,2}$.

---

## 7. Impact on Manuscripts

The preprint `manuscripts_and_proofs/K3_DarkMatter_Preprint.tex` and the older `OPEN_PROBLEMS.md` / `CAVEATS.md` `GAP-1` resolutions should be updated to:

1. State that $S_{1,2}$ is elliptic (ODE order 2, $q_2=81/8$), not K3.
2. Remove or downgrade the phrase "$S_{1,2}$ is the sole surviving K3 candidate."
3. Identify the K3 candidate pool as the GATE-C finalists (Cooper $s_7$, $s_{10}$, T103, etc.).

The `docs/autoresearch_v2/S12_S21_DEFINITION_ALIGNMENT.md` and `lean4_formal_proofs/Structures/S12S21Recurrence.lean` docstrings have already been aligned with this rectification.
