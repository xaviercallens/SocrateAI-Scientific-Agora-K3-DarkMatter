# GATE-B-SELECT: 13 → 5 Composite Scoring and Recommendation

**Date:** 2026-07-14 · **Status:** AWAITING HUMAN DECISION (this document is the machine recommendation; GATE-B is a HUMAN gate per AUTORESEARCH_RELEASE_V2_PLAN.md)
**Inputs:** all G1-1..G2-4 outputs (see `docs/autoresearch_v2/PHASE_B_FINDINGS.md`).

## Scoring context (read first)

- **G2 gates are non-discriminating** (Finding N3: all candidates yield the identical mass at any common (τ,𝒱); GD-1, superradiance, PTA, Lyman-α verdicts are therefore pool-uniform). Selection rests on the **G1 mathematical gates** plus literature anchoring.
- Both controls behaved (A005259 → K3, A005258 → elliptic), so verdicts below are trusted.
- Monodromy is computable for **all 13** (post-N1 fix), so the guide's monodromy bonus does not separate candidates either.

## Score table

Criteria: K3-type geometry (G1-1, exact) · mirror-map integrality on the **minimal** operator (G1-3) · MUM at z=0 · Weil weight-3 pass (G1-2) · literature anchor (external, citable) · liabilities.

| # | Candidate | K3 | Integral | MUM | Weil | Anchor | Liabilities | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | **apery_zeta3** (A005259) | ✓ | ✓ | ✓ | ✓ | Beukers–Peters 1984 (proven K3, ρ=19) | none | **PROMOTE** |
| 2 | **domb** (A002895) | ✓ | ✓ | ✓ | ✓ | Almkvist–Zagier sporadic | none | **PROMOTE** |
| 3 | **cooper_s7** (A183204) | ✓ | ✓ | ✓ | ✓ | Cooper 2012 (level 7) | none | **PROMOTE** |
| 4 | **cooper_s10** (A005260) | ✓ | ✓ | ✓ | ✓ | Cooper 2012 (level 10) | none | **PROMOTE** |
| 5 | **almkvist_zagier_second** (A125143) | ✓ | ✓ | ✓ | ✓ | Almkvist–Zudilin ζ(3)-class | alternating signs (a_p caveat) | **PROMOTE** |
| 6 | t103 (A276536) | ✓ | ✓ | ✓ | ✓ | OEIS only, no geometry literature | novel, unanchored | ALTERNATE |
| 7 | t112 (A274789) | ✓ | ✓ | ✓ | ✓ | OEIS diagonal, no geometry literature | novel, unanchored | ALTERNATE |
| 8 | t003 core (A002897) | ✓ | ✓ | ✓ | ✓ | classical ₃F₂ hypergeometric | core is textbook object; partial-sum wrapper adds nothing new | ALTERNATE |
| 9 | t011 | ✓ | BLOCKED | ✗ (roots 0,0,1) | ✓ | none (not in OEIS) | non-MUM, unanchored | KILL |
| 10 | cooper_s18 (A219692) | ✗ (order 4 in window) | BLOCKED | ✗ | ✓ | Cooper 2012 (level 18) | not weight-3 in window | KILL (flag: CY3-shape curiosity) |
| 11 | az_sporadic_a006077 | ✗ elliptic | ✓ (weight-2) | ✓ | ✓ | Zagier ζ(2) class | literature tag was wrong (N4) | KILL |
| 12 | apery_zeta2_s21 (A005258) | ✗ elliptic | ✓ (weight-2) | ✓ | ✓ | Beukers/Beauville | is the negative control | RETAIN AS CONTROL (not promoted) |
| 13 | s12_v1_primary (A112019) | ✗ elliptic | **✗ (q₂=81/8)** | ✓ | ✓ | none for K3 | v1 integrality was wrong-operator artifact (N2) | **KILL — v1 closure complete** |

## Recommended top 5

**apery_zeta3, domb, cooper_s7, cooper_s10, almkvist_zagier_second** — the five candidates that pass every mathematical gate AND carry independent literature anchoring (each is a known sporadic/weight-3 object, so Phase C/D work builds on citable ground rather than in-house-only claims).

**Decision point for the human:** if novelty is valued over anchoring, swap cooper_s10 (or almkvist_zagier_second) for **t103** — the strongest in-session discovery (full gate pass, OEIS-listed, but no geometry literature). The recommendation errs toward anchored candidates because Phase D (Lean formalization) needs literature statements to formalize against.

## On S₁,₂ and S₂,₁ (explicit, per the user's Phase B directive)

Both ran through every gate identically to all candidates ("validate the pipeline WITH S12 and S21"). Outcomes:
- **S₂,₁** = A005258: elliptic (confirms GAP-1 and the literature answer key); it did its job as the negative control — every K3 gate correctly rejected it.
- **S₁,₂** = A112019: elliptic AND its minimal-operator mirror map is non-integral (q₂ = 81/8); v1's contrary result traced to the non-minimal operator (Finding N2). This completes the honest v1 closure: **neither v1 flagship survives as a K3 candidate**, and the pipeline that once promoted them now demonstrably self-corrects.
- The pasted "Lean 4 reversal" claiming S12/S21 are proven K3 was separately adjudicated and rejected (`docs/autoresearch_v2/S12_S21_ADJUDICATION.md`).

## Pool-uniform physics caveats carried to Phase C

At the common (GAP-2 reverse-engineered) normalization all promoted candidates share: m ≈ 3.4×10⁻²¹ eV, GD-1 survival, **no** bare M87* superradiance survival (l=m=1 timescale ≈ 2.5 Myr), outside the NANOGrav band, and Lyman-α tension if all-DM. Phase C data tests must either exploit the PTA-visible part of the (τ,𝒱) window or work in the sub-dominant-fraction regime — and any per-candidate mass claim requires solving the moduli problem first (N3).
