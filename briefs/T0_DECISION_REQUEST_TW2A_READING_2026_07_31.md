# T0 Decision Request — WP-TW2-A's "Reading 1 vs Reading 2" Impasse

**Date:** 2026-07-31
**From:** Fable 5 (T1 coordinator)
**To:** T0 (Xavier Callens)
**Status:** DECISION REQUESTED — three questions (Q1–Q3), Q1 blocking
**Scope note:** Filed as a decision request, not ruled under the 2026-07-31 delegation.
That delegation covers execution-level interpretation of already-ratified decisions. This
is the specific case your own D5/R4 ruling chain pre-flagged for return: "if a sharp
impasse survives an actual n=0 construction attempt, the referral question returns to T0
with the evidence" (R4, `briefs/T1_DELEGATED_RULINGS_2026_07_31.md`). It has now occurred.
Even the question of whether *this particular item* should go to Deep Think (T0s) is
something R4 explicitly reserved for you, not something the "no Deep Think needed"
instruction pre-answers — that instruction was about today's execution batch, not a
named contingency your own prior ruling carved out in advance.

---

## Coordinator verification performed before filing

Re-ran everything independently rather than trusting the agent's transcript:
- `checkers/check_TW2A_n0_construction.py` — clean run, all 8 sections (A–H) PASS.
- `checkers/test_TW2A_n0_construction_controls.py` — 7/7 pass, including the
  task-mandated wrong-vanishing-order negative control.
- `refs/x0_7_inose_cm.json` SHA-256 independently recomputed — matches the MANIFEST pin
  (`17732a41…ce9aa0`) exactly.
- **Cross-repo independent check on the one number that matters most**: read S2's
  certified G0 result directly (`data/certificates/G0_NS_genus_cooper_s7.json`), not the
  agent's summary of it. G0's certified NS genus: det = 14, signature (1,18), via the
  Nikulin-orthogonal-complement route. TW2A's completely different derivation — an
  explicit elliptic K3 model with a computed Shioda–Tate/Mordell–Weil section — lands on
  det = 14, signature (1,18) independently. Two unrelated derivation routes agreeing is
  real corroboration, not a restated number.

**Conclusion: the mathematics is genuine, not fabricated.** TW1/TW0 regression tests
re-run clean; nothing here touches cooper_s10/U⊕⟨20⟩ or Stream-4 material.

## What was found (four pieces, all checker-verified)

1. **f, g exhibited at n=0**, exact rational model from an X₀(7) Fricke point: II*+II*
   fibers over C₀, C∞ (orders 4,5,10, matching WP-TW1's necessary condition), fiber type
   II*+II*+4I₁, Euler number 24. Transcription of the literature inputs (Shioda–Inose
   theory, Silverman's CM table) is gated by an internal fingerprint check (Fricke
   involution identity + CM-degeneration cross-check at h=±7) that the checker verifies
   before consuming any cited value — not blind transcription.
2. **⟨−14⟩ identified at the K3-fiber level**: forced to equal P̄ = P−O−7F for a
   Mordell–Weil section of height 14 — exact Shioda–Tate arithmetic, all alternative
   sources (reducible-fiber components, multisections, base pullbacks) excluded by
   computation. NS(fiber) = M₁₉ exactly, **conditional on cited Shioda–Inose theory
   (Tier B)** — this is the same conditional standing as the existing certified
   ρ=19/T=3 result for cooper_s7, not a new epistemic category.
3. **Fourfold-level ⟨−14⟩ divisor is obstructed for the isotrivial ansatz**: two
   independent obstructions (a square-twist choice creates a fatal codim-1 locus; the
   alternative twist choice has wall monodromy that kills the ⟨−14⟩ generator via
   fiberwise inversion — verified as an exact symbolic computation, not asserted).
4. **A new, sharper obstruction found by this WP, invisible to WP-TW1's original screen**:
   at every n=0 model, a codimension-2 locus with vanishing orders (4,6) exists
   *unconditionally* — proven algebraically (a, c are degree-18 forms that must vanish
   somewhere), not by genericity assumption. TW1 only checked exact orders at *generic*
   points, which is why it missed this and correctly returned PASS for its own narrower
   question.

## The impasse (Q1, blocking)

Finding 4 admits two standard readings in the F-theory/minimal-Weierstrass-model
literature, and — for the first time in this project's history — **they disagree**:

- **Reading 1** ("no minimal Weierstrass CY exists over this base as given"): the n=0
  fourfold-level M₁₉ exhibition is a **documented dead end**. TW1's PASS verdicts describe
  a screen that no actual model can survive past this next stage.
- **Reading 2** (standard practice: such codim-2 loci are cured by blowing up the base —
  the well-known E₈×E₈ "point-like instanton" phenomenon in F-theory): a cure exists, but
  the base is no longer P(O⊕O)/P² — it **leaves the currently-scoped ladder entirely**,
  and WP-TW1's verdict table would need re-derivation on blown-up bases before anyone can
  say which n (if any) still work.

**The repo currently has no F-theory/Tate-algorithm literature pinned in `refs/`** to
settle this with a citation, which is exactly why the WP stopped here instead of guessing.

## My assessment (not a ruling — offered as input)

Reading 2 is the reading the broader F-theory literature treats as standard practice (the
brief's own characterization, echoing well-known results like Morrison–Vafa on
non-Higgsable/point-like-instanton loci) — but "the literature generally does this" is not
the same as a hash-pinned citation this project can stand behind, and I am not positioned
to referee this the way an adversarial geometric review would. This reads as a genuinely
good candidate for the T0s (Deep Think) channel your R4 ruling already reserved for it:
the stakes are real (Reading 1 closes the current route to Phase M; Reading 2 keeps it
alive but changes its scope substantially), the question is technical and
literature-gated rather than execution-level, and getting it wrong in either direction
either abandons a live route or continues investing in a dead one.

## Q2 and Q3 (downstream of Q1)

- **Q2**: should "M₁₉ exhibition" be formally re-scoped to mean the K3-fiber level only
  (achieved here, Tier B) with the fourfold-divisor version tracked as a separate open
  problem — regardless of how Q1 resolves?
- **Q3** (only if Reading 2): authorize WP-TW2-B — non-isotrivial modular-pencil families
  + base blow-up bookkeeping + the still-unexhibited explicit Mordell–Weil section
  coordinates (three candidate paths mapped, none started, gated on this ruling).

---

*Verification note: every claim above was checked against the actual checker output,
test suite, certificate JSON, and G0's own certificate file this session — not restated
from the producing agent's summary.*
