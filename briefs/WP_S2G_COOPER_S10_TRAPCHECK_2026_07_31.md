# WP S2-G: cooper_s10 Twisted-Weierstrass Trap-Check (Coordinator-Verified Brief)

**Status:** DRAFT, coordinator-verified 2026-07-31. Code was authored in the 2026-07-30
session (T0 Directive 2) but never accompanied by a brief; this record supplies it and
records the verification pass performed before landing.

**Authority:** T0 Directive 2 (2026-07-30, session log); structural template from WP-TW1
(`checkers/check_TW1_two_e8_feasibility.py`, coordinator-verified, S2 `7d41514`).

---

## What it computes

The same necessary-condition question WP-TW1 asked for cooper_s7 — can a threefold base
B₃ host two E₈ (Kodaira II*) gauge loci in Δ=4f³+27g² for the generic Weierstrass model —
asked for **cooper_s10**, whose transcendental lattice is *reported* by the AlphaEvolve
Vertex run as T ≅ U⊕⟨20⟩. That report is explicitly **not** in the S2 CLAUDE.md epistemic
ledger and is used throughout only as a labeled working hypothesis, never as fact — the
file's own docstring is careful and repeated about this distinction.

## Coordinator verification performed

1. **Re-ran the script clean.** All 3 self-tests pass (toric monomial counting vs. binomial
   closed form; n=0 product anchor P¹×P² vs. pushforward decomposition; restriction
   formulas cross-checked two independent ways). All 3 P¹-bundle cases (n=0,1,2) verdict
   PASS. All 5 controls behave correctly: 1 positive control passes as expected, 4 negative
   controls (shrunk bound, three-E8 demand, NS-side scramble, malformed input) all correctly
   fail/reject.
2. **Read the derivation chain directly** (not just the self-test pass/fail): the pushforward
   decomposition (`h0_scroll_aC0_bh`), the C₀/C∞ restriction formulas (adjunction from the
   classical scroll normal-bundle fact), and their cross-check identity were inspected line
   by line — the math is internally consistent and the cross-checks are genuine (independent
   derivation routes, not the same computation restated).
3. **Independently re-verified the file's most load-bearing empirical claim** — that this
   repo's own `checkers/check_U1_lattice.py:run_family('cooper_s10')` independently
   corroborates T≅U⊕⟨20⟩. Ran it directly (not via the trapcheck script, and not trusting
   its transcript): first attempt raised a spurious `ControlFailure` because calling
   `run_family` directly skips `main()`'s `mp.mp.dps = DPS` precision setup (machine-epsilon
   precision instead of the intended 60-digit mpmath precision). Re-ran with precision set
   correctly: **reproduces exactly** — det = −20, elementary divisors [20], explicit
   U-splitting via integral base change (det 1). This corroborates the trapcheck's claim
   and rules out fabrication of that specific number.

## Result

- cooper_s10 requires the **same structural condition** as cooper_s7 (WP-TW1): two E₈(−1)
  loci. B₃ = P(O⊕O(n))/P² for n = 0, 1, 2 all PASS the necessary-condition screen.
- **Epistemic status unchanged by this verification**: T≅U⊕⟨20⟩ remains AlphaEvolve-reported
  and uncertified in the primary ledger — the in-house corroboration strengthens confidence
  but was, per the file's own honest accounting, exercised only as a cross-family regression
  control inside `check_NS_genus_G0.py`, not promoted as a titled, reviewed certificate for
  cooper_s10 itself. This brief does not change that; it only verifies the trapcheck's
  claims about what it computed were not fabricated.

## Files

- `checkers/check_S2G_cooper_s10_trapcheck.py` (708 lines, authored 2026-07-30)
- This brief (added 2026-07-31, coordinator verification pass)

---
*Verified-by: Fable 5 (T1 coordinator), 2026-07-31 — full script re-run, derivation chain
read line-by-line, load-bearing cross-repo claim independently re-derived at correct
precision.*
