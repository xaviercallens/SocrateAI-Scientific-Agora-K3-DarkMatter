# Phase 8.A Findings — Deep First Scan (LR-1…LR-3)

**Date:** 2026-07-14 · **Executor:** Fable (deep-intelligence pass) · **Status:** Complete; GATE-A pending
**Method:** `scripts/autoresearch_v2_phase_a_scan.py` — dual exact detection (minimal shift recurrence AND minimal generating-function ODE), modular pre-screen (two 62-bit primes) routing exact ℚ nullspace solves, every reported relation validated exactly on ≥70 held-out terms to n=110. Raw outputs: `data/autoresearch_v2/phase_a_{anchors,scan2,scan3}.json`.

---

## NEGATIVE / CORRECTIVE RESULTS FIRST (Rule 4)

### Finding 1 — The v1 classification rule was inverted, and the answer-key controls caught it

v1 (GAP-1) classified by **minimal shift-recurrence order**: order 3 ⇒ "K3", order 2 ⇒ "elliptic".
The literature-certified K3 control breaks this rule:

| Sequence | OEIS | Shift (order, deg) | **ODE (order, deg)** | Literature geometry | v1 rule says | Truth |
|---|---|---|---|---|---|---|
| Apéry ζ(3) = S(2,2) | A005259 | **(2, 3)** | **(3, 4)** | **K3** (Beukers–Peters 1984) | elliptic ✗ | K3 ✓ |
| Apéry ζ(2) = S₂,₁ | A005258 | (2, 2) | (2, 3) | Elliptic (Beauville; Cooper t₅) | elliptic ✓ | elliptic ✓ |
| Domb | A002895 | (2, 3) | (3, 4) | K3-class (Almkvist–Zagier sporadic) | elliptic ✗ | K3 ✓ |
| **S₁,₂** | **A112019** | **(3, 3)** | **(2, 5)** | none assigned in OEIS | "K3" ✗ | **elliptic-type** |

The geometry-discriminating datum is the **ODE order of the generating function** (2 = elliptic/weight-2, 3 = K3-type/weight-3, 4 = CY3-type), equivalently the (order, coefficient-degree) class of the 3-term recurrence (Zagier (2,2) ↔ weight 2; Almkvist–Zagier (2,3) ↔ weight 3). Shift-recurrence order alone anti-correlates with geometry in exactly the cases that matter.

### Finding 2 — S₁,₂, the v1 primary "K3" candidate, is elliptic-type

S₁,₂ = OEIS **A112019** (a known rational-function diagonal; no K3/modularity attribution in the literature). Its generating function satisfies an **order-2 ODE** (degree 5), fit on 30 exact coefficients and validated exactly on **74 held-out terms**. Its order-3 *shift* recurrence — the entire basis of v1's "K3 signature" — is an artifact of the shift/ODE order distinction. **Under the control-validated classifier, neither S₁,₂ nor S₂,₁ is K3-type. The v1 K3 identification fails entirely at the arithmetic level.** This supersedes and sharpens the GAP-1 resolution: GAP-1 correctly demoted S₂,₁ but for an under-specified reason, and left S₁,₂ standing on the same under-specified rule.

### Finding 3 — v1's sieve excluded the only genuine K3 in its own search box

The full corrected scan of (A,B) ∈ [1,8]² finds **exactly one** K3-type sequence: **S(2,2) = Apéry ζ(3) = A005259** — the Beukers–Peters K3 (Picard rank 19), one of the most-studied objects in arithmetic geometry. It lies inside v1's original [1,5]² window; the shift-order rule excluded it (shift order 2) while promoting two elliptic-type sequences. Every other (A,B) with max(A,B) ≥ 3 has no ODE of order ≤ 4 / degree ≤ 8 (higher-weight objects, outside the elliptic/K3/CY3-simple window).

---

## POSITIVE RESULTS

### Corrected landscape, (A,B) ∈ [1,8]² (scan2)

| Class | Members |
|---|---|
| Rational (ODE order 1) | S(1,1) (central Delannoy) |
| Elliptic (ODE order 2) | S(1,2)=A112019, S(2,1)=A005258 |
| **K3-type (ODE order 3)** | **S(2,2)=A005259 only** |
| Higher / none found | all with max(A,B) ≥ 3 |

### 3-factor family T(A,B,C) = Σ C(n,k)^A C(n+k,k)^B C(2k,k)^C, (A,B)∈[0,3]², C∈[1,3] (scan3)

New **K3-type** (ODE order 3, exact held-out pass) candidates:

| Sequence | First terms | Shift | ODE | OEIS |
|---|---|---|---|---|
| T(0,0,3) = Σₖ C(2k,k)³ (partial sums) | 1, 9, 225, 8225, 351225 | (2,3) | (3,4) | **A079727** |
| T(0,1,1) = Σ C(n+k,k)C(2k,k) | 1, 5, 43, 469, 5701 | none ≤ caps | (3,6) | TBD (Phase B) |
| T(1,0,3) = Σ C(n,k)C(2k,k)³ | 1, 9, 233, 8673, 376329 | none ≤ caps | (3,6) | TBD (Phase B) |
| T(1,1,2) = Σ C(n,k)C(n+k,k)C(2k,k)² | 1, 9, 241, 9129, 402321 | none ≤ caps | (3,8) | TBD (Phase B) |

Elliptic (consistency checks — the classifier recovers known Zagier-class objects): T(2,0,1)=Σ C(n,k)²C(2k,k) (ODE (2,3)), T(1,1,1) (ODE (2,5)), T(0,0,2) (ODE (2,3)), T(1,0,2) (ODE (2,4)). Rational: T(0,0,1), T(1,0,1).

### Classifier validation status

Positive control (A005259 → K3-type) ✓ · Negative control (A005258 → elliptic) ✓ · Second K3 anchor (Domb → K3-type) ✓ · Known rational/elliptic objects land correctly ✓. **The upgraded ODE-order classifier passes the full answer key.**

---

## Companion-repo experimental findings (DarkMatterK3-Home, fetched 2026-07-14)

From `DarkMatterK3_Phase3_Report.tex` (archived at `docs/reference/dmk3_home/`):
- **Provenance of the 1.177 bound resolved:** 32 SDSS **BOSS DR17** sectors × ~7,200–10,000 galaxies; S₁,₂ projection min/mean/max = 1.0279 / 1.0969 / **1.1770**; Δ min/mean/max = 0.055 / 0.184 / 0.327; 100% of sectors show S₁,₂ > 1 > S₂,₁ directional asymmetry; honest **null result** vs. the 1.8 transition threshold; sector-21 TDA: χ = −33, β₁ = 47, β₀ = 14.
- **No Euclid data anywhere** — SDSS BOSS DR17 only. Euclid/DES/KiDS lensing cross-match is *planned* (bridge plan Phase 2). EU-1 remains the acquisition task.
- **Cross-repo inconsistency (flagged):** the bridge plan uses m_eff ≈ m₀(1+κΔ_obs)^{1/4}, this repository uses m_eff = m₀·exp(kΔ). These disagree beyond first order; reconciliation is a Phase B/C prerequisite before any joint fit (logged as v2 open item OI-1).
- **Naming hazard (flagged):** the macroscopic tensor statistic named "S₁,₂" in the pipeline does not mathematically depend on the sequence S₁,₂; with the sequence now reclassified elliptic-type, the statistic's "K3" branding inherits a misnomer. The statistic's empirical content (directional asymmetry, 1.177 bound) is unaffected (logged as OI-2).

## Consequences for the physics programme

1. The v1 mass-ratio invariant √(1014/336) was a ratio between two elliptic-type objects; it never was a "K3 asymmetry." Its Lean certification (exact arithmetic) stands; its geometric interpretation does not.
2. **The constructive path is better than the one it replaces:** S(2,2) = Apéry ζ(3) is a *literature-grade* K3 with explicitly known geometry (Beukers–Peters), modular structure, and 40 years of arithmetic backing — everything v1 tried and failed to establish for S₁,₂ (monodromy, modularity match) is already in print for A005259. Rebuilding the instanton/stiffness pipeline on S(2,2) + the four new K3-type T-candidates is Phase B's task.
3. Part I/II/III manuscripts require a further corrective pass once GATE-A confirms the pool (the S₁,₂ "sole K3 survivor" language is now itself falsified). Deferred until after GATE-A per plan discipline.
