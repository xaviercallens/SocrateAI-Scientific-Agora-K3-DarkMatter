# 🔍 Deep Think — Adversarial Concurrence Brief: C3b resolution (s7 / s10)

**To:** Deep Think (T0s adversarial concurrence · Two-Model Rule)
**From:** Stream 2 (K3 Selection)
**Subject:** Independently attack the claim "C3b RESOLVED for cooper_s7 / cooper_s10" before it is accepted.
**Under review:** commit `3b6064b` — `checkers/check_C3b_symsqrt.py`, certs `data/certificates/C3b_symsqrt_*.json`,
refs `cooper_s7_partner` / `cooper_s10_partner`, `data/k3t2/C3B_FINAL_STATUS.md`.

Your job is not to confirm. It is to **find the failure mode**. Re-derive independently (do not read the
extracted operator first and then "check" it — derive L₂ yourself, then compare). Concur only if every
attack below is neutralised.

## The claims being asserted

1. **[B, PASS(58)]** √g is order-2 holonomic for s7 and s10, with the stated partner recurrences.
2. **[B]** z(L₂)(q) = z(L₃)(q) exactly to q¹⁴ (moduli map = identity).
3. **[B, negative]** None of Zagier's six sporadic order-2 sequences is the partner (moduli-map checker,
   ≤ bidegree 5, 8 power-hypotheses, to q³²).
4. **[F6]** A002893 is Zagier's *valid order-2* sporadic C (10,9,3), not "order-3 / wrong type."

## Attack surface (each must be independently killed)

**A1 — Is the order-2 holonomy real or a finite-order fit artifact?**
The partner recurrence was obtained by nullspace fit on n≤26 and revalidated to n=58. A degree-2, 3-poly
ansatz has 9 unknowns; 24 fit rows. Push it: regenerate f to n≥200 and re-test the *same* recurrence. Does it
hold? Independently, fit at a *different* degree bound (D=3,4) and window — do you recover the same order-2
operator (content-normalised), or a spurious higher-order one? Confirm the **discrimination control**: a
generic order-3 MUM sequence (e.g. s7 with a₁-coefficient 90→91) must give NO order-2 fit. If it does, the
test is vacuous.

**A2 — Is z(L₂)=z(L₃) a tautology of the construction?**
The mirror map is built from the same series. Argue whether the equality is forced by g = f² *definitionally*
(in which case it proves nothing) or is a genuine constraint that a non-Sym² operator would violate. Test it:
take a bulk that is NOT a symmetric square and confirm the constructed z's do **not** match. (Apéry ζ(3) is
instructive — its √g is order-2 holonomic but with C(n) = −4(n+1)², a *non-MUM* operator; verify the checker
rejects it with `FAIL_PARTNER_VALIDATION`, not a false accept.)

**A3 — The MUM constant.** s7/s10 give C(n) = −(n+1)² exactly (constant 1); ζ(3) gives −4(n+1)². Is the
"constant = 1" gate the mathematically correct selector for the elliptic (mirror-map-bearing) partner, or an
accident of normalisation that could reject a genuine partner? Justify or break it.

**A4 — s10's rational partner.** f for s10 is non-integral (2-power denominators). Is L₂ still a legitimate
order-2 operator over ℚ(z), or does the non-integrality signal a branch/scaling defect that invalidates the
Sym² claim? Independently reconstruct s10's L₂ and decide.

**A5 — The F6 correction (A002893).** Verify from Gorodetsky arXiv:2102.11839 (fetch, do not trust this brief)
that A002893 = ∑C(n,k)²C(2k,k) is the second-order sporadic C (A,B,λ)=(10,9,3). Confirm it is MUM + integral +
order-2 under the checker. If instead it is genuinely order-3, the F6 correction is wrong and must be reverted.

**A6 — Provenance hygiene (Rule 1 / guardrails Rule 5).** Trace **every** number in the certificates and refs
to (a) a checker computation on committed data, or (b) a fetched literature artifact with citation. Flag any
value that originates from model memory. Special attention: the six Zagier triples and OEIS ids — confirm each
against the fetched source, not recollection (this is the exact failure that corrupted the 2026-07-20 refs).

## Two-Model Rule checkpoint

The downstream Stream-1 proof (`briefs/STREAM1_C3B_SYM2_PROOF_TASK.md`) will produce L₂, L₃, and Sym²(L₂) as
explicit operators. **Do not let Opus 4.8 encode the `ring` identity until you have independently produced
Sym²(L₂) and confirmed it matches Fable's output.** Concurrence on the operator forms is the gate.

## Concurrence output

Return one of: **CONCUR** (all attacks neutralised; list what you independently re-derived) · **CONCUR-WITH-
CAVEATS** (state each) · **BLOCK** (name the surviving failure mode + the artifact that proves it). Verdicts
are Human-decided; your role is adversarial evidence, not the final gate.

---
Generated-by: Opus 4.8 (Stream-2) | Verified-by: pending Deep Think independent re-derivation | Reviewed-by: pending T0
