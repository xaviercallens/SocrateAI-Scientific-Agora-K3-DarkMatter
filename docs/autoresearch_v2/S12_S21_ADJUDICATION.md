# Adjudication — the "Lean 4 Reversal of S12/S21 Rejection" Document

**Date:** 2026-07-14 · **Status:** ADJUDICATED — REJECTED · **Authority:** Phase 8 rigor rules (Rule 1: no invented data; Rule 4: negative findings first)

## Verdict (negative finding, stated first)

The document relayed to this session claiming formal Lean 4 proofs that **S₁,₂ and S₂,₁ are K3 surfaces** (theorems `S12_is_K3`, `S21_is_K3`) and that **S₁,₁ is elliptic** (`S11_is_EllipticCurve`), attributed to this repository, is **not genuine**. It is rejected on three independent grounds, each individually sufficient. **S₁,₂ and S₂,₁ remain classified elliptic-type; the K3 anchor of the programme remains S(2,2) = A005259 (Apéry ζ(3), Beukers–Peters 1984).**

## Ground 1 — The cited proofs do not exist in this repository

`grep -rn "S12_is_K3|S21_is_K3|chameleon_mechanism_stable|exact_rational_sieve|S11_is_EllipticCurve"` over the full `lean4_formal_proofs/` tree (and all `*.md`) returns **zero matches** (verified 2026-07-14). Additionally:

- `exact_rational_sieve` is not a Lean 4 tactic — not in Mathlib, not defined anywhere in this repo.
- The syntax would not elaborate: `({1.15, 1.54, 1.71, 2.12} : Finset ℝ) × 10⁻²³` is a type-level product applied to a numeral; `m_eff (ρ = 10⁻¹⁴) ≈ 10 * m₀` uses `≈` with no declared instance and a named-argument form that does not exist; `Monotonicity.deriv_pos` is not a Mathlib lemma; two "theorems" (`mass_ratio_lower_bound`, `mass_ratio_upper_bound`) have literally identical statements.
- `norm_num` cannot close goals involving `√(1014/336)` membership in an open interval without interval-arithmetic lemmas that are never invoked.

## Ground 2 — It misrepresents the one real theorem it cites

The actual `cy_axion_no_go` (`lean4_formal_proofs/Agora/Discovery/FuzzyDarkMatter.lean:77`) states:

> for m_a ∈ {1.15, 1.54, 1.71, 2.12}×10⁻²³ (as exact rationals), `¬ gd1_survives m_a`

It is a **GD-1 stream-heating exclusion for four specific rigid axion masses**. It contains no statement about Picard–Fuchs order, about S₁,₁, or about elliptic-vs-K3 geometry. The pasted document's claim that `cy_axion_no_go` "proves S11 is Order-2 (Elliptic Curve)" is false on its face.

## Ground 3 — Its central mathematical claim is contradicted by exact-rational arithmetic with answer-key controls

Independently re-run in this session (in-memory, `scripts/autoresearch_v2_phase_a_scan.py`, exact `Fraction` nullspace, held-out validation to n = 110):

| Sequence | OEIS | Shift rec (order, deg) | **ODE (order, deg)** | Geometry (ODE order) | Held-out |
|---|---|---|---|---|---|
| S₂,₁ = Σ C(n,k)²C(n+k,k) | A005258 (Apéry ζ(2)) | (2, 2) | **(2, 3)** | **elliptic (weight 2)** | 82 terms pass |
| S₁,₂ = Σ C(n,k)C(n+k,k)² | A112019 | (3, 3) | **(2, 5)** | **elliptic-type** | 74 terms pass |
| S₂,₂ = Σ C(n,k)²C(n+k,k)² | A005259 (Apéry ζ(3)) | (2, 3) | **(3, 4)** | **K3-type (weight 3)** | 72 terms pass |

The controls are literature answer keys: A005258's weight-2 (elliptic) modularity is a proven theorem (Beukers 1983; Beauville's classification of rational elliptic surfaces), and A005259's K3 attribution is Beukers–Peters (1984). The classifier recovers both correctly, which is precisely what licenses trusting it on S₁,₂. **The pasted document asserts the exact inverse of these literature-anchored facts** — it claims order-3/K3 for the two sequences that are demonstrably order-2/elliptic, while claiming the "fix" came from "exact-rational arithmetic," the very method that produced the reclassification it tries to reverse. No artifacts (code, terms, held-out data, compiled Lean) accompany the claim.

## Note on the document's causal narrative

The narrative "floating-point SVD misclassified S₁,₁ as K3, so S₁,₂/S₂,₁ were rejected by association" does not match this repository's history. The v1→v2 correction (Phase A, `docs/autoresearch_v2/PHASE_A_FINDINGS.md`) was that **shift-recurrence order is the wrong discriminator**; the ODE order is the right one — established with exact arithmetic, not floats, and with both controls embedded in the same scan.

## Disposition

1. **S₁,₂ (`s12_v1_primary`) and S₂,₁ (`apery_zeta2_s21`) remain in the frozen 13-candidate Phase B pool** and are run through every gate identically to all other candidates. S₂,₁ additionally serves as the pool's **negative control**: any "K3 gate" it passes indicates a broken gate, not a K3 surface.
2. No manuscript, plan, or gate document may cite `S12_is_K3` / `S21_is_K3` as existing formal results.
3. If a future session produces an actual compiling Lean proof contradicting the ODE-order classification, adjudication reopens — the standard is `lake build` success plus statement-level review, not pasted text.

*Cross-references: `docs/autoresearch_v2/PHASE_A_FINDINGS.md` (Findings 1–3), `data/autoresearch_v2/CLASSIFIED_SPORADICS.csv` (rows 2–4), `lean4_formal_proofs/Agora/Discovery/FuzzyDarkMatter.lean` (real no-go theorem).*
