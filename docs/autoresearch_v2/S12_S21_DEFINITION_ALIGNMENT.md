# S₁₂ / S₂₁ Definition Alignment — Rigorous Reference

**Date:** 2026-07-14  
**Author:** Cascade (in-session verification)  
**Scope:** settle the S₁₂/S₂₁ definition/geometry conflict by collecting every authoritative definition in this repository, re-running the exact-rational ODE classifier and the G1-3 minimal-operator mirror-map integrality gate, and stating the rigorous alignment.

---

## 1. One unambiguous definition is used everywhere in this repo

All scripts, Lean files, JSON/CSV gate outputs, and adjudication documents define S₁₂ and S₂₁ as the two asymmetric members of the two-parameter family

```
S_{A,B}(n) = Σ_{k=0}^{n} C(n,k)^A · C(n+k,k)^B
```

| name | (A,B) | formula | OEIS | first terms |
|---|---|---|---|---|
| **S₁₂** | (1,2) | `Σ C(n,k)^1 · C(n+k,k)^2` | [A112019](https://oeis.org/A112019) | 1, 5, 55, 749, 11251, 178835, 2949115, 49906925 |
| **S₂₁** | (2,1) | `Σ C(n,k)^2 · C(n+k,k)^1` | [A005258](https://oeis.org/A005258) (Apéry ζ(2) / Domb-like) | 1, 3, 19, 147, 1251, 11253, 104959, 1004307 |
| **S₂₂** | (2,2) | `Σ C(n,k)^2 · C(n+k,k)^2` | [A005259](https://oeis.org/A005259) (Apéry ζ(3), Beukers–Peters K3) | 1, 5, 73, 1445, 33001, 819005, 21460825, 584307365 |
| S(1,1) | (1,1) | `Σ C(n,k)^1 · C(n+k,k)^1` | central Delannoy | 1, 3, 13, 63, 321, 1683 |

**Sources:**
- `lean4_formal_proofs/Structures/S12S21Recurrence.lean:49-52`
- `scripts/autoresearch_v2_phase_a_scan.py:32-34`
- `scripts/k3_sieve_analysis.py:10-66`
- `scripts/modularity_screen.py:205`
- `docs/autoresearch_v2/PHASE_A_FINDINGS.md:15-26`
- `docs/autoresearch_v2/S12_S21_ADJUDICATION.md:29-35`

There is **no** place in this repository that defines S₁₂ or S₂₁ as the symmetric `Σ C(n,k)^1 · C(n+k,k)^1`. That sequence is S(1,1) / central Delannoy, a different object.

---

## 2. Geometry is determined by the generating-function ODE order, not the shift-recurrence order

The v1 classifier (and the outdated `S12S21Recurrence.lean` docstring) used **shift-recurrence order** as a proxy for geometry. Phase 8.A found that proxy is inverted for these sequences: the literature-certified K3 control `S₂₂` has shift order 2, which under the v1 rule would be called "elliptic". The correct discriminator is the **ODE order of the generating function** `y(z) = Σ S(n) z^n`.

| sequence | shift recurrence (order, degree) | generating-function ODE (order, degree) | geometry by ODE | held-out pass |
|---|---|---|---|---|
| S(1,1) | (2, ?) in repo scan not tracked | (1, 2) | rational | — |
| **S₁₂ = S(1,2)** | (3, 3) | **(2, 5)** | **elliptic (weight 2)** | 74 terms |
| **S₂₁ = S(2,1)** | (2, 2) | **(2, 3)** | **elliptic (weight 2)** | 82 terms |
| **S₂₂ = S(2,2) = A005259** | (2, 3) | **(3, 4)** | **K3-type (weight 3)** | 72 terms |
| Domb A002895 | (2, 3) | (3, 4) | K3-type (weight 3) | 72 terms |
| Cooper s₇ (A183204) | (2, 3) | (3, 4) | K3-type (weight 3) | 72 terms |
| Cooper s₁₀ (A005260) | (2, 3) | (3, 4) | K3-type (weight 3) | 72 terms |
| T103 (A276536) | (4, 3)* | (3, 6) | K3-type (weight 3) | 62 terms |
| Almkvist–Zagier 2nd (A125143) | (2, 3) | (3, 4) | K3-type (weight 3) | 72 terms |
| A006077 | (2, 2) | (2, 3) | elliptic | 82 terms |
| Cooper s₁₈ (A219692) | (2, 4) | (4, 5) | CY3-type (weight 4) | 60 terms |

*The repo's `T103Recurrence.lean` formalizes a wider-window **shift** recurrence of order 4, degree 3, because the default (order ≤ 3) window did not contain T103's minimal shift recurrence. Its minimal **ODE** (order 3, degree 6) was found in the default window and is the basis of its K3-type classification.

**Sources:**
- `data/autoresearch_v2/g1_1_order_classification.json`
- `data/autoresearch_v2/phase_a_anchors.json` (reproduced by re-running `python scripts/autoresearch_v2_phase_a_scan.py anchors`)
- `docs/autoresearch_v2/PHASE_A_FINDINGS.md`
- `lean4_formal_proofs/Structures/CooperS7Recurrence.lean:4-16` (docstring explicitly distinguishes shift recurrence from ODE)
- `lean4_formal_proofs/Structures/T103Recurrence.lean:4-15`

---

## 3. Mirror-map integrality on the *minimal* operator (Phase 8.B G1-3)

A second, independent K3-period test is the integrality of the mirror-map `q(z)/z` coefficients. The v1 `scripts/mirror_map_integrality.py` used the **non-minimal** order-3 shift operator and reported S₁₂ as integral (false positive). The Phase 8.B G1-3 gate recomputes the Frobenius log solution from the **minimal** generating-function ODE and finds the second coefficient is fractional for S₁₂.

| sequence | ODE order | `q(z)/z` first coefficients | `q₂` | integrality verdict |
|---|---|---|---|---|
| **S₁₂ = S(1,2)** | 2 | `1, 81/8, 16717/128, ...` | **81/8** | **❌ FAILS** (non-integral) |
| **S₂₁ = S(2,1)** | 2 | `1, 5, 35, 280, ...` | 5 | ✅ passes |
| **Apery ζ(3) = S₂₂** | 3 | `1, 12, 222, 4900, ...` | 12 | ✅ passes |
| **Domb** | 3 | `1, 6, 51, 518, ...` | 6 | ✅ passes |
| **Cooper s₇** | 3 | `1, 9, 132, 2310, ...` | 9 | ✅ passes |
| **Cooper s₁₀** | 3 | `1, 4, 38, 384, ...` | 4 | ✅ passes |
| **T103** | 3 | `1, 25, 901, 38373, ...` | 25 | ✅ passes |

**Source:** `data/autoresearch_v2/g1_3_mirror_integrality.json` (31 coefficients checked for each candidate).

---

## 4. Independent re-run (this session)

I re-ran `scripts/autoresearch_v2_phase_a_scan.py anchors` unchanged and also wrote a separate exact-`Fraction` ODE solver. Both give the same result for the asymmetric definitions used by every script in this repo:

```
S(1,1): [1, 3, 13, 63, 321, 1683]   ODE order 1 (rational)
S12    : [1, 5, 55, 749, 11251, 178835]  ODE order 2 (elliptic)
S21    : [1, 3, 19, 147, 1251, 11253]    ODE order 2 (elliptic)
S22    : [1, 5, 73, 1445, 33001, 819005] ODE order 3 (K3)
```

The controls behave exactly as the literature says:
- `A005258 = S₂₁` is weight-2 modular (elliptic) — Beukers 1983 / Beauville.
- `A005259 = S₂₂` is K3 — Beukers–Peters 1984.

Because the classifier recovers both answer keys correctly, its S₁₂ classification (ODE order 2) is licensed by the same calculation.

---

## 5. What actually exists in Lean 4

| claimed theorem | actually in repo | truth |
|---|---|---|
| `S12_is_K3` | **does not exist** in any `*.lean` or `*.md` file | ❌ never existed as a compiling theorem |
| `S21_is_K3` | **does not exist** | ❌ never existed as a compiling theorem |
| `S11_is_EllipticCurve` | **does not exist** | ❌ never existed |
| `chameleon_mechanism_stable` | **does not exist** as a theorem name | ❌ the actual theorems in `lean4_formal_proofs/Agora/Discovery/ChameleonStability.lean` are `m_eff_pos`, `m_eff_mono`, `m_eff_has_deriv_at` |
| `mass_ratio_lower_bound` / `mass_ratio_upper_bound` | ✅ exist in `lean4_formal_proofs/Agora/K3_Topology.lean:38-44` | ✅ they are distinct `>` / `<` rational inequalities, not identical statements |
| `cy_axion_no_go` | ✅ exists in `lean4_formal_proofs/Agora/Discovery/FuzzyDarkMatter.lean:77` | ✅ says four rigid axion masses fail GD-1 heating bounds; says nothing about S₁₂/S₂₁ geometry |

**Search method:** `grep -R "S12_is_K3\|S21_is_K3\|chameleon_mechanism_stable"` over `lean4_formal_proofs/` and all `*.md` returns zero matches. `git log -S S12_is_K3 --all` only finds `docs/autoresearch_v2/S12_S21_ADJUDICATION.md`, the document explaining why the claim is rejected.

---

## 6. Why the conflict arose

1. **Shift order vs ODE order confusion.** S₁₂ has shift recurrence order 3, which v1 called "K3". S₂₁ has shift recurrence order 2. Phase 8.A showed the geometry discriminator is **ODE order**, and S₁₂'s ODE is order 2 (elliptic).
2. **Stale docstring in `S12S21Recurrence.lean`.** The file was written after `2b486a7` (2026-07-11), which correctly demoted S₂₁ to elliptic but still left S₁₂ as "order-3/K3". The later commit `f73d2e4` (2026-07-14) corrected this and showed S₁₂ is also ODE order 2/elliptic, but `S12S21Recurrence.lean` was not updated. This stale comment is the *realignment target*.
3. **External "review" text conflated symmetric S(1,1) with asymmetric S₁₂/S₂₁.** The symmetric `Σ C(n,k)^1 C(n+k,k)^1` is S(1,1), which is rational (ODE order 1), not S₁₂ or S₂₁.
4. **External "review" misread Cooper/T103 files.** It appears to have looked at the *shift* recurrence order (2 for Cooper s₇/s₁₀, 4 for T103) and ignored the file docstrings that explicitly say the **ODE** order is 3 (K3-type).

---

## 7. Real alignment statement

| object | definition | ODE order | mirror-map q₂ | geometry | status |
|---|---|---|---|---|---|
| S₁₂ | `Σ C(n,k)^1 · C(n+k,k)^2` | 2 | **81/8** (non-integral) | elliptic (weight 2) | **not** a K3 surface; negative control |
| S₂₁ | `Σ C(n,k)^2 · C(n+k,k)^1` | 2 | 5 (integral) | elliptic (weight 2) | **not** a K3 surface; negative control |
| S₂₂ / A005259 | `Σ C(n,k)^2 · C(n+k,k)^2` | 3 | 12 (integral) | K3-type | literature K3 anchor of the programme |
| Domb | — | 3 | 6 (integral) | K3-type | literature K3 anchor |
| Cooper s₇ / A183204 | `Σ C(n,j)^2 · C(2j,n) · C(j+n,j)` | **ODE** 3 | 9 (integral) | K3-type | GATE-C finalist, Lean kernel-verified |
| Cooper s₁₀ / A005260 | Cooper 10th sporadic | **ODE** 3 | 4 (integral) | K3-type | GATE-C finalist, Lean kernel-verified |
| T103 / A276536 | `Σ C(n,k) · C(2k,k)^3` | **ODE** 3 | 25 (integral) | K3-type | GATE-C finalist, Lean kernel-verified |

The mass/stiffness integers `1014` and `336` are treated in `lean4_formal_proofs/Agora/K3_Topology.lean` as an exact rational ratio `1014/336 = 169/56` giving a PTA frequency ratio in `(1.73, 1.75)`. The repo explicitly notes that these integers are **not** derived from a Picard–Fuchs potential curvature (GAP-2 unresolved) and that the K3 geometric interpretation no longer attaches to S₁₂/S₂₁, which are elliptic-type.

---

## 8. Recommended PR changes

1. **Update `lean4_formal_proofs/Structures/S12S21Recurrence.lean` docstring** (lines 13-26) to align with Phase 8.A / `f73d2e4`: both S₁₂ and S₂₁ have generating-function ODE order 2 (elliptic-type); the file still does not prove recurrence order in Lean, but it must no longer claim S₁₂ "remains genuinely order-3".
2. **Add this alignment document** to `docs/autoresearch_v2/` so future sessions have a single source of truth.
3. **Add `PHASE_8_AUTOEVOLVE_RECTIFICATION.md`** at the repository root to document the S₁₂ rejection and the re-anchoring to GATE-C K3 candidates.
4. Optionally update `PARAMETER_LEDGER.yaml`, `OPEN_PROBLEMS.md`, `CAVEATS.md` and the LaTeX preprint to remove stale "S₁₂ remains sole surviving K3" language.

---

## 9. Reproducibility

Re-run the ODE classification independently:

```bash
python scripts/autoresearch_v2_phase_a_scan.py anchors
# output: data/autoresearch_v2/phase_a_anchors.json
```

Verify the JSON shows:
- `S12 (A=1,B=2)`: `"ode_order": 2`, `"geometry_by_ode": "elliptic (weight 2)"`
- `S21 (A=2,B=1)`: `"ode_order": 2`, `"geometry_by_ode": "elliptic (weight 2)"`
- `Apery zeta(3) A005259 [K3 control]`: `"ode_order": 3`, `"geometry_by_ode": "K3-type (weight 3)"`

For the mirror-map integrality gate:

```bash
python scripts/autoresearch_v2_phase_b_all_gates.py
# output: data/autoresearch_v2/g1_3_mirror_integrality.json
```

Check `s12_v1_primary` for the non-integral `q₂ = 81/8` and `cooper_s7` for the integral `q₂ = 9`.

Run `lake build Agora` to confirm `S12S21Recurrence.lean` still compiles after the docstring-only change.
