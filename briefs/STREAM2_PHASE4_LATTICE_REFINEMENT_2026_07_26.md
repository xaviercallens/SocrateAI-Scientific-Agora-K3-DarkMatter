# Stream 2 Phase 4 — from ranks to lattices: the M₇-polarization route

**Date:** 2026-07-26 (late evening) · **From:** Stream 2 (Fable 5)
**Status:** step 1 of 3 **computed and certified**; steps 2–3 are a fetch-and-read task and a
T0 decision, in that order. **No lattice value is emitted anywhere below tier C.**

---

## 1. Why this route exists

E-011 closed ρ = 19, T = 3 — but as **ranks only**. Everything downstream that died with the
fibre reading (S3-00 step 2(b): α_D, Λ_D "from Kodaira fibre data") needed *structure*, not
rank. E-013 left 2(b) with no input and flagged the amendment as a T0 call.

There is a classical route from exactly our situation to full lattices, and it runs through
the modular substrate we already verified — not through fibres:

> **Dolgachev–Doran picture [C until sources are read]:** a one-parameter family of
> M_n-polarized K3 surfaces, M_n = U ⊕ E₈² ⊕ ⟨−2n⟩ (rank 19), has moduli curve **X₀(n)+**,
> Picard–Fuchs operator the **symmetric square** of a weight-... order-2 operator, and generic
> transcendental lattice **T = U ⊕ ⟨2n⟩** (rank 3). Candidate sources: Dolgachev, *Mirror
> symmetry for lattice polarized K3 surfaces* (1996); Doran, *Picard–Fuchs uniformization*
> (~2000). **Neither has been fetched or read. Nothing below treats their content as fact.**

Our family's fingerprint matches this shape at every point we can compute:

| fingerprint | our status | source |
|---|---|---|
| PF operator = Sym² of order-2 | **[A]** kernel-proven | Stream 1 |
| ρ = 19, T = 3 (= ranks of M₇, U⊕⟨14⟩) | **[B]** derived | E-011 |
| moduli coordinate is a Γ₀(7)+ Hauptmodul | **[B]** — NEW, computed today | §2 |
| level n = 7 (disc −7 substrate, s7 partner at level 7) | **[B]** | Route γ, O'Brien |

## 2. What was computed today (the new leg)

`checkers/check_s7_hauptmodul_gamma07plus.py` → `data/certificates/HAUPTMODUL_S7_GAMMA07PLUS.json`

**Claim:** t = g.f.(A279618) — the coordinate Route γ proved is the correct pullback for the
s7 period — is a Hauptmodul for **Γ₀(7)+**, not merely for Γ₀(7).

**Method** (exact ℚ arithmetic, solve/verify split, three negative controls):
- u₇ = q⁻¹(E(q)/E(q⁷))⁴, the classical Γ₀(7) eta-quotient Hauptmodul, built from the
  pentagonal-number product and self-verified.
- t is **not** a Möbius function of u₇ (TEST M fails) ⇒ t is not a Γ₀(7) Hauptmodul.
- t **is** a degree-2 rational function of u₇ — coefficients solved on orders ≤ 12, then
  verified exactly on the 17 held-out orders 13–29 (TEST D) ⇒ [ℚ(u₇) : ℚ(t)] = 2.
- The involution exchanging the two sheets was solved from the fitted coefficients:
  **κ = 49 = 7², computed, not assumed** (TEST F) — this is the Fricke involution
  u ↦ 49/u appearing from the data.
- Since the normalizer of Γ₀(7) in PSL₂(ℝ) is Γ₀(7)+ (Atkin–Lehner 1970 — classical,
  cited, not re-derived: the one [B]-tier ingredient), the index-2 fixed field is Γ₀(7)+'s
  function field. **Conclusion tier B.**
- Controls: a genuine Γ₀(7) Hauptmodul yields NOT-plus; a single corrupted coefficient
  breaks held-out verification; the level-5 coordinate fails every fit.

This supersedes-in-strength (does not contradict) the earlier *indirect* evidence — the
implied-signature match (0;2,2,3;1 cusp) from Route γ — with a direct function-field
computation on 29 exact coefficients.

## 3. The hypothesis this licenses — stated as a hypothesis

> **H-M7 [C]:** the s7 family is M₇-polarized with NS(X) ≅ U ⊕ E₈² ⊕ ⟨−14⟩ and
> T(X) ≅ U ⊕ ⟨14⟩ for the very general member.

Consistency checks that H-M7 survives (observations, **not** derivations):
- rank(U ⊕ E₈² ⊕ ⟨−14⟩) = 2+8+8+1 = **19** = ρ (E-011) ✓
- rank(U ⊕ ⟨14⟩) = **3** = T (E-011) ✓
- |disc| = **14 = 2·7** on both sides (complementary primitive sublattices of the unimodular
  Λ_K3 have equal |disc|) ✓ — and the level 7 matches the family's arithmetic everywhere else.

**Promotion path C → B, exactly two steps:**
1. **Fetch and read** Dolgachev 1996 / Doran. The load-bearing statements to verify in the
   text: (i) moduli of M_n-polarized K3s ≅ X₀(n)+; (ii) T of the generic member ≅ U ⊕ ⟨2n⟩;
   (iii) the PF operator is the Sym² of the weight-2 uniformizing operator. Per project rule,
   read the primary text — no paraphrase, no abstract-only citation (the O'Brien Thm 6.1/6.2
   incident is the template for how this goes wrong).
2. Re-issue this memo's table with per-statement page references, and emit
   `C2_cooper_s7_v4.json` carrying the lattices with `conditional_on: []` replaced by the
   citations. **Until then, v3 (ranks only) remains the live certificate.**

## 4. What H-M7 would unblock — and what it would not

**S3-00 step 2(b) gets a replacement input.** The step needed "gauge data from fibre content";
fibre content does not exist (E-007/E-009). If H-M7 is promoted, NS(X) contains an explicit
**E₈ ⊕ E₈ root sublattice** — lattice-level structure from which a dark-sector discussion can
at least be *posed* (M-theory-on-K3 language: gauge enhancement from ADE root systems in NS,
at loci where the corresponding −2-classes become effective and contract). That would convert
2(b) from "input retracted, strike the step" to "input re-derivable at lattice level,
re-scope the step" — a materially different T0 decision.

**Unchanged by any of this:**
- The physics reading stays **[C]**: roots in NS ≠ contracted curves on the actual member;
  which sublattice (if any) enhances is a geometric question about the specific family.
- **Phase M stays dormant and M2 stays unauthorized** (T0 D2). H-M7 promotion is *evidence
  toward* re-opening, never an authorization.
- **F5b stands.** No m_φ exists; obstruction 1 (no flux stabilization) is untouched.
- ρ/T in live certificates: **unchanged, ranks only, v3.**

## 5. s10, deliberately not attempted tonight

The analogue for s10 is level 10, where the Atkin–Lehner group is (ℤ/2)² (w₂, w₅, w₁₀) — the
"+" question splits into *which* extension, the eta-quotient has a different exponent
pattern, and **we hold no Hauptmodul b-file for it in refs/**. Doing it right needs: the
correct pullback coordinate from a Route-γ-style step 0 for s10, its terms ingested into
`refs/` under the register discipline, and the w-subgroup logic generalized. Guessing an OEIS
ID from memory is how s18 was corrupted twice; not doing that.

## 6. Asks

- **T0:** hold the S3-00 2(b) decision until the Dolgachev/Doran read completes (it changes
  which decision is on the table). Authorize the fetch as the next Stream 2 work item.
- **Deep Think:** adversarial check of §2's logic — in particular whether any group strictly
  between Γ₀(7) and its normalizer could evade the index-2 argument (we claim not, at prime
  level, since [Γ₀(7)+ : Γ₀(7)] = 2 leaves no room; confirm).
- **Stream 1:** none. The Sym² kernel result is load-bearing here and already parked clean.

**Generated-by:** Fable 5 (Stream 2) | **Verified-by:** `check_s7_hauptmodul_gamma07plus.py`
(3 negative controls, solve/verify split, exact ℚ); certificate hash-pinned in repo |
**Reviewed-by:** Xavier (T0) — pending
