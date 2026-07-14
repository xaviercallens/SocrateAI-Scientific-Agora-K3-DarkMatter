# AutoEvolve R2 — Phase B Findings (full gate battery, 13 candidates)

**Date:** 2026-07-14 · **Runner:** `scripts/autoresearch_v2_phase_b_all_gates.py` + `scripts/autoresearch_v2_phase_b_obs_screens.py` · **Log:** `data/autoresearch_v2/phase_b_run.log` (78 s full battery)
**Rule 4: negative and corrective findings first.**

## Negative / corrective findings

### N1 — Fuchs-criterion sign bug in `k3_monodromy_verification.py` (GAP-1-era tool)

The 2026-07-11 "bug fix" in `classify_singular_points()` used threshold `(order−k) − nu_m`; the correct Fuchs condition is `ord(Q_k) ≥ nu_m − (order−k)` — the sign was inverted. Consequence: **every singular point of every operator tested before 2026-07-14 was classified IRREGULAR and every monodromy integration was skipped.** Verified against the classical Apéry ζ(3) Picard–Fuchs operator (singular points {0, 17±12√2}, all famously regular): the old code called all three irregular. Fixed this session (see the file's docstring); after the fix all 13 pool operators are confirmed Fuchsian and **monodromy was actually computed for all 13** (|det M| = 1 to 9–25 digits). Any monodromy-based conclusion in pre-2026-07-14 documents inherits the misclassification and must be re-derived.

### N2 — v1's S₁,₂ mirror-map integrality was an artifact of the wrong operator

S₁,₂'s **minimal** ODE (the true Picard–Fuchs operator) is order 2 (elliptic, Phase A). v1's mirror map (`mirror_map_integrality.py`, harmonic-sum log solution) belongs to the **non-minimal order-3** operator: this session's Frobenius log solution of the minimal operator differs from index 1 on. On the minimal operator, S₁,₂'s mirror map is **NOT integral** — q₂ = 81/8 fails immediately (`g1_3_mirror_integrality.json`, `v1_provenance_diagnostic`). So v1's "S₁,₂ mirror-map integrality PASS" and the stiffness chain built on it used a second solution that is not the Picard–Fuchs one. Method control: on the two classical operators (A005259, A005258) the Frobenius and Beukers harmonic-sum log solutions agree **exactly** (31 coefficients), so the method itself is validated; the discrepancy is specific to v1's use of the non-minimal S₁,₂ operator.

### N3 — G2 mass formula cannot discriminate candidates (GAP-2 degeneracy, now pool-wide)

At any common (τ, 𝒱), **all 13 candidates give the identical axion mass** (m_ref = 3.445×10⁻²¹ eV at the GAP-2 reference point): q₁ = 1 by mirror-map normalization and e^{−2πτ} suppression makes d ≥ 2 terms irrelevant (single-instanton domination — the T2.2 finding, now quantified across the whole pool). The (τ,𝒱) contour, GD-1 check, and superradiance check therefore return the **same verdicts for every candidate**; only the unsuppressed stiffness integers V″(0) differ (range 94 → 8664), and their physical relevance still rests on the unestablished moduli-cancellation antecedent. G2 as specified is honest but **non-discriminating**; GATE-B selection must rest on the G1 mathematical gates.

### N4 — A006077's "K3-class" literature tag is falsified

G1-1: A006077 → ODE order 2, **elliptic** (held-out exact). Consistent with its (n+1)² leading recurrence coefficient (Zagier ζ(2)/elliptic class). The pool's provisional "K3-class per literature" tag was wrong; the actual second Almkvist–Zudilin K3-class object is A125143, which does verify K3-type (order 3).

### N5 — cooper_s18 (A219692) is not weight-3 within the search window

G1-1: minimal ODE within (ρ≤4, δ≤8) is order 4 (CY3-type shape), degree 5; z = 0 is **not MUM** (indicial roots {0,0,0,1}). Mirror-map and stiffness gates are BLOCKED for it. Caveat recorded: an order-3 operator of z-degree > 8 is not excluded by the search window.

### N6 — t011 is not MUM at z = 0

Indicial polynomial 126x²(x−1) (roots {0,0,1}): mirror map undefined in standard normalization → G1-3/G2-* BLOCKED. Also: **no OEIS match** for its terms (searched 2026-07-14) — it remains defined only by its binomial form.

### N7 — Observational screens disfavor the flagship mass regime at the common normalization

At m_ref = 3.44×10⁻²¹ eV (all candidates, per N3): the Compton frequency 8.3×10⁻⁷ Hz is **above the NANOGrav 15-yr band** ([2, 60] nHz → masses [8.3×10⁻²⁴, 2.5×10⁻²²] eV), and the mass is **in tension with Lyman-α forest bounds if the axion is all of DM** (Iršič+ 2017: m > 3.8×10⁻²¹ eV — marginal; Rogers & Peiris 2021: m > 2×10⁻²⁰ eV — strong). Any surviving scenario needs either the PTA-visible part of the (τ,𝒱) window (which every candidate's window intersects) or a sub-dominant axion fraction. `g2_4_obs_screens.json`.

### N8 — Superradiance at the common reference mass: no bare survival

α_ref = 0.168 at M87* (a★ = 0.90): l = m = 1 instability timescale ≈ 2.5 Myr < 50 Myr Salpeter → `bare_survival = False` for all candidates at the reference point (identical by N3). This differs from GAP-3's "S₂,₁ bare survives" because GAP-3 evaluated v1's per-candidate fitted mass 1.83×10⁻²¹ eV (α = 0.089); at the common normalization the fitted-τ asymmetry disappears. The Dolan solver revalidated its Table-I benchmark (6/6 rows) before running.

## Positive results

| Candidate | OEIS | G1-1 ODE | Geometry | Weil w3 (2p) | Mirror integral | Monodromy | Fuchsian |
|---|---|---|---|---|---|---|---|
| apery_zeta3 (**+control**) | A005259 | (3,4) | **K3** | pass | **yes** | computed | yes |
| domb | A002895 | (3,4) | **K3** | pass | **yes** | computed | yes |
| t003 (core C(2k,k)³) | A079727/A002897 | (3,4) | **K3** | pass | **yes** | computed | yes |
| t011 | — (not in OEIS) | (3,6) | **K3** | pass | BLOCKED (non-MUM) | computed | yes |
| t103 | A276536 | (3,6) | **K3** | pass | **yes** | computed | yes |
| t112 | A274789 | (3,8) | **K3** | pass | **yes** | computed | yes |
| cooper_s7 | A183204 | (3,4) | **K3** | pass | **yes** | computed | yes |
| cooper_s10 | A005260 | (3,4) | **K3** | pass | **yes** | computed | yes |
| almkvist_zagier_second | A125143 | (3,4) | **K3** | pass | **yes** | computed | yes |
| apery_zeta2_s21 (**−control**) | A005258 | (2,3) | elliptic | pass | yes (weight-2 map) | computed | yes |
| s12_v1_primary | A112019 | (2,5) | elliptic | pass | **NO (q₂=81/8)** | computed | yes |
| az_sporadic_a006077 | A006077 | (2,3) | elliptic | pass | yes (weight-2 map) | computed | yes |
| cooper_s18 | A219692 | (4,5) | CY3-shape | pass | BLOCKED (non-MUM) | computed | yes |

- Both classifier controls passed (A005259 → order 3, A005258 → order 2); run would have halted otherwise.
- **Monodromy computable for all 13** — the guide's "auto-elevation" criterion is met pool-wide; the corrected G1-4 finally delivers what GAP-1 attempted.
- Phase B OEIS resolutions (LR-2 closure): s7 = A183204, s10 = A005260, s18 = A219692 (via OEIS "Cooper's paper" comments), AZ second = A125143, t103 = A276536, t112 = A274789, t011 = not in OEIS.
- LMFDB screen: no small-level weight-3 match for any candidate (4-form subset only — inconclusive by design, recorded per candidate in `g1_2_weil_modularity.json` + `ap_tables/`).

## Files

Gates: `data/autoresearch_v2/g1_1_order_classification.json`, `g1_2_weil_modularity.json` (+ `ap_tables/*.csv`), `g1_3_mirror_integrality.json`, `g1_4_monodromy_status.json`, `g2_1_stiffness_contours.json`, `g2_2_no_go_status.json`, `g2_3_superradiance_bands.json`, `g2_4_obs_screens.json`.
Selection package: `data/autoresearch_v2/selection_13to5_rationale.md` (GATE-B, HUMAN decision).
Related adjudications this session: `docs/autoresearch_v2/S12_S21_ADJUDICATION.md`, `docs/autoresearch_v2/DATA_PROVENANCE_RECONCILIATION.md`.
