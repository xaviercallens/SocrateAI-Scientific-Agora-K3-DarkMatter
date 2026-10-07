# WP-TW0 re-examination — the Hodge-bundle degree "ℓ = 2" is not a family-level number (F6 disclosure; T0 ruling requested)

**Date:** 2026-10-07 · **From:** Stream 2 · **Trigger:** T0, "launch numeric research on K3" (2026-10-07);
ledger item 6 names WP-TW0 as the pending in-house verification of ℓ = 2 and says "if it lands ≠ 2, F6
disclosure + T0 escalation". It lands ≠ 2 under every family-level reading. This brief is that disclosure.
**The ledger is not edited by this brief.** Checker: `checkers/check_TW0_hodge_degree_orbifold.py`
(+ `checkers/test_TW0_hodge_degree_orbifold_controls.py`, 9 controls); certificate
`data/certificates/TW0_HODGE_DEGREE_ORBIFOLD.json` (sha256 `0be0fc09756bfcfd…`). Exponent language only; no
Kodaira label anywhere (items 3, 10).

## 1. What the 2026-07-29 draft did, and why it does not verify anything

`briefs/TW0_HODGE_DEGREE_RESULT_2026_07_29.md` / `checkers/check_TW0_hodge_degree.py` (DRAFT, never promoted)
reports ℓ = 2 from "deg ℒ_ell = (Σ exponents)/order = 2/2 = 1, then ⊗2". Three defects, all machine-visible:

1. **It lists three singular points** (z = −1, 1/27, ∞). L₂ in θ-form has **four**: z = 0 is the MUM point
   with exponents {0, 0}. Its "Fuchs relation Σ = 2 with 3 singular points" is wrong as stated (for three
   points the order-2 relation would require Σ = 1); the arithmetic Σ = 2 is right only because there are
   four points. (`riemann_scheme` → `n_singular_points = 4`.)
2. **The formula has no cited source and is a tautology** for the class in play: the Fuchs relation forces
   Σ exponents = s − 2 for every order-2 Fuchsian operator with s singular points, so "(Σ exponents)/2 = 1"
   holds for **every** such operator with s = 4 — it returns 1 for cooper_s10 as well (control N4). A test
   that cannot fail is not a test (standing rule 1).
3. The "orbifold correction = 0" step is asserted, not computed.

## 2. What the number actually is, computed exactly from the Tier-A operator tuple

| quantity | value | how |
|---|---|---|
| Riemann scheme of L₂ | z=0: {0,0}; z=−1: {0,1/2}; z=1/27: {0,1/2}; z=∞: {1/3,2/3} | indicial polynomials, sympy exact |
| signature of the base, from exponents | (g; e₁,e₂,e₃; c) = (0; 2,2,3; 1) | exponent difference 1/e ↔ order e; repeated 0 ↔ cusp |
| signature of X₀(7)+, from group theory | (0; 2,2,3; 1) | index 8, ε₂ = 0, ε₃ = 2, 2 cusps, genus 0; Fricke fixed points h(−28)+h(−7) = 1+1 = 2 (class numbers counted from reduced forms); Riemann–Hurwitz |
| **agreement** | **yes** | the two derivations are independent |
| χ_orb | −2/3 | 2 − 2g − Σ(1 − 1/e) − c |
| deg ω (elliptic Hodge line bundle, weight 1) | **1/3** | −χ_orb/2 (Q-line bundle on the orbifold) |
| deg ω² (K3 Hodge line bundle, Doran Thm 5.13: K3 period = square of the elliptic period) | **2/3** | −χ_orb |
| Deligne-extension integer degree of ω² on the coarse P¹ | **0** (residues in [0,1)) or **1** (residues in (−1,0]) | par-deg = deg + Σ α, α = exponent of the holomorphic period: 0, 0, 0 at the finite points, 2/3 at ∞ |
| elliptic-**surface** reading: ℓ with deg Δ = 12ℓ | **2** | χ(O_K3) = 1 − h^{0,1} + h^{0,2} = 2; Noether 12χ(O) = K² + e ⇒ e = 24 = deg Δ |

**Finding.** No family-level reading of "degree of the Hodge line bundle" gives 2: the values are 1/3, 2/3,
0, 1. The number 2 is reproduced only as χ(O) of an elliptic K3 with section — true of every such K3, and
saying nothing specific about the cooper_s7 family or about the Sym² theorem. The countermand's phrasing
"ℓ = 2 (periods are squares of the elliptic L₂ periods, ℒ_K3 = ℒ_ell^⊗2)" mixes the two readings: the ⊗2
statement is about the family (and gives 2/3, not 2); the ℓ = 2 is about the surface.

Control outcomes: wrong level (N = 5) and wrong operator (cooper_s10 at N = 7) both make the two signatures
disagree; an irregular singular point is refused; the 07-29 formula is shown non-discriminating; Noether
distinguishes a rational elliptic surface (ℓ = 1) from a K3 (ℓ = 2). The cooper_s10 operator against
Γ₀(10)+ also disagrees — (0; 2,2,4; 1) vs (0; 2,2,2; 2) — which is consistent with the open composite-level
question (its Hauptmodul is recorded for Γ₀(10)*, `HAUPTMODUL_S10_GAMMA010STAR.json`); it is used here only as
a discriminating control and no statement about s10 is made.

## 3. What this does and does not change

- **Does not change:** Route A stays CLOSED (its closure did not rest on ℓ; countermand annotation 1 says
  so explicitly). No Tier A/B certificate cites ℓ. No physics (item 4).
- **Does change (pending T0):** ledger item 6's sentence "The Hodge-bundle degree ℓ = 2 is ratified Tier
  B-external … in-house verification WP-TW0 pending" is now **verified false as a family-level statement
  and trivially true as a surface statement**. WP-TW1 ("two-E8 degree feasibility on P³, deg Δ = 48") is
  a Weierstrass-model computation, so it almost certainly needs the **surface** reading — in which case the
  input it needs is χ(O) = 2 and WP-TW1 can proceed unchanged. That is T0's call, not Stream 2's.

## 4. Requested ruling (one of)

- **R-a:** amend ledger item 6 to read "ℓ := χ(O_K3) = 2 for the Weierstrass model (Tier A, Noether); the
  family-level Hodge-bundle degree is 2/3 (Q) / 0 or 1 (Deligne extension), Tier B, certificate
  `TW0_HODGE_DEGREE_ORBIFOLD.json`; WP-TW0 CLOSED". Then WP-TW1 may be opened as numeric research.
- **R-b:** keep item 6 as is and record this brief as a dissent; WP-TW1 waits.
- Either way: `briefs/TW0_HODGE_DEGREE_RESULT_2026_07_29.md` needs a dated correction note (standing rule 3),
  and `checkers/check_TW0_hodge_degree.py` should be disabled or made to refuse (it currently prints ℓ = 2
  from a non-discriminating formula; it is not in the regression block).

*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: the certificate above and its 9 controls; the
independent agreement of the exponent-derived and group-theoretic signatures | Reviewed-by: N (T0 rules)*
