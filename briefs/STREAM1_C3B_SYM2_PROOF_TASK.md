# ⚡ Stream-1 Task: prove L₃ = Sym²(L₂) for cooper_s7 / cooper_s10 (all n)

**To:** Stream 1 (Opus 4.8 executor · Fable 5 math design)
**From:** Stream 2 (K3 Selection)
**Blocks:** upgrade of C3b from PASS(58) → Tier A. Not a critical-path blocker for D-3.
**Provenance of inputs:** commit `3b6064b`; certificates `data/certificates/C3b_symsqrt_cooper_s{7,10}.json`;
checker `checkers/check_C3b_symsqrt.py`; refs `cooper_s7_partner`, `cooper_s10_partner`.

> Tiers: **[A]** established/certified · **[B]** checkable, unproven (carries route) · **[C]** physical.

## 1. What Stream 2 established (and its exact epistemic status)

**[B, PASS(58)]** For the bulk order-3 operators of cooper_s7 (A183204) and cooper_s10 (A005260 = ∑C(n,k)⁴),
the power series f = √g (g = Σaₙzⁿ) is **order-2 holonomic**: f satisfies the order-2 recurrence

- **s7:** (n+1)² fₙ₊₁ = (26n²+13n+2) fₙ + 3(3n−1)(3n−2) fₙ₋₁,  f = 1,2,22,336,6006,117348,… (**OEIS A279619**)
- **s10:** (n+1)² fₙ₊₁ = (12n²+6n+1) fₙ + (8n−5)(8n−3) fₙ₋₁,  f rational (2-power denominators)

verified by exact nullspace fit on n≤26 and **re-validated to n=58**; and the order-2 mirror map
z(L₂)(q) equals the order-3 bulk mirror map z(L₃)(q) exactly to q¹⁴.

**The gap to close:** "validated to n=58" is a finite-order machine check, not a proof for all n. The
order-2 recurrence was *fitted*, then *revalidated*; a fit is not a derivation.

## 2. The claim to prove (Tier-A target)

> **[target A]** L₃ = Sym²(L₂) as differential operators over ℚ(z), for cooper_s7 and cooper_s10,
> where L₃ is the bulk Picard–Fuchs operator (from the frozen order-3 recurrence in `refs/`) and L₂ is
> the extracted order-2 operator (from the partner recurrence above).

If this operator identity holds, then g (the holomorphic MUM solution of L₃) is a Sym²-solution, hence
g = f² with f the holomorphic solution of L₂ — which discharges the all-n content and retro-justifies the
n=58 checks. The mirror-map equality z(L₂)=z(L₃) then follows structurally (Sym² preserves the nome).

## 3. Recommended route (reuses the D1 Option-B machinery)

1. **Recurrence → operator.** Convert each frozen order-3 recurrence and each order-2 partner recurrence to
   its differential operator via the standard θ = z d/dz ↔ shift correspondence. Keep everything in
   `Polynomial ℚ` coefficients (clear denominators). **[Fable 5 subtask:** output L₃ and L₂ as explicit
   operators with polynomial coefficients.]
2. **Symbolic Sym².** Compute Sym²(L₂): for L₂ = θ² + p(z)θ + q(z), the symmetric square is the order-3
   operator annihilating products of L₂-solutions. Emit it with cleared-denominator polynomial coefficients.
3. **Cleared-denominator identity.** Form P(z) := (denominator)·(Sym²(L₂) − L₃) coefficient-wise and prove
   **P(z) ≡ 0 in Polynomial ℚ**. This is exactly the **D1 (E-006) Option B** pattern — a pure polynomial
   identity, no RatFunc derivative API, dischargeable by `ring` (or `native_decide`, disclosed per the
   guardrails). **[Opus 4.8 subtask:** HALT kernel encoding until Deep Think clears Fable's operator output
   via the Two-Model Rule (see `briefs/DEEPTHINK_C3B_ADVERSARIAL_BRIEF.md`), then script the `ring` proof.]
4. **On success:** upgrade the two certificates' verdict language from `PASS(58)` to a Lean-backed all-n
   statement, cite the `lake env lean` output in the commit (Rule 4), and set repo state `SYM2_PROVED`
   for s7/s10.

## 4. Scope guards

- **s18 is out of scope** — `gorodetsky_s18` is BLOCKED (corrupt recurrence). Re-transcribe from
  arXiv:2102.11839 before any s18 Sym² work; do not run this task on it.
- **No physics.** Prove only the operator identity. L₂-as-brane / bulk↔brane coupling is **[C]** and belongs
  in manuscripts as a conjecture, never in a theorem name (feedback_k3_rigor: no physics-washing in Lean).
- **s10 partner is rational** (non-integral f). The operator identity is still well-posed over ℚ(z); the
  proof does not require an integral partner sequence.

---
Generated-by: Opus 4.8 (Stream-2, Tier-B handoff) | Verified-by: pending Stream-1 `ring`/Lean proof | Reviewed-by: pending T0 + Deep Think
