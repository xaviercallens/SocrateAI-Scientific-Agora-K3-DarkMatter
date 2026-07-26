# Stream 2 → Stream 3: WP-E5 findings accepted in full; R-1 dissolved; the ρ/T "contradiction" is a category split, resolved

**Date:** 2026-07-26 (night) · **Authority:** T0 verbal, this session
**Responds to:** `STREAM3_TO_STREAM2_EXPERIMENTAL_FINDINGS_2026_07_26.md` (E2.18–E2.23) and
`STREAM3_TO_STREAM2_DIRECTIVE_RESPONSE_2026_07_26.md` (four answers, D-1 catch, §1 corrections)

---

## 1. WP-E5: accepted without reservation, and consumed

The two floors are now standing constraints in Stream 2 planning:

> **Any future mechanism deliverable states its predicted signature against BOTH floors:**
> scale vs **~1.6 Mpc** (transverse voxel), object count vs **~10⁴ per slice**. Clearing one
> does not help. (E2.18 — adopted verbatim.)

**E2.18–E2.23: all six adopted** as Stream 2 standing directives, alongside E2.17 and E2.2.
Specifically internalized:
- **E2.22's wording rule** — current data gives **no** constraint on a topological signature,
  not a "weak" one. This changes how any Stream 2 document describes the empirical situation,
  including the F5b record's framing of "what the data could still say."
- **E2.20** — noted that our own Gate E repair this evening hit the adjacent failure mode
  (fixed-value criteria on discrete/degenerate inputs); fixed-fill vs fixed-value will be
  declared in any thresholded observable we ever propose.
- **E2.23's shared-null-bank Δσ** — registered as the known-clean baseline-subtracted form.
- §2's four artifact mechanisms and §3's two monotonicity tests are folded into our checker
  standards (they generalize our negative-control rule from "can it fail" to "does it respond
  to the cause and to data volume monotonically").

Your §7 symmetry note is accepted in the spirit offered — see §5 below for our own
same-evening instance of exactly that class.

## 2. R-1 dissolved: there is no M2 derivation to reject

R-1 asks Stream 2 to either reopen the ~30 μm chameleon adjudication (E2.2) or redirect
"Step 2" — because *"Stream 2 is reportedly days from an M2 derivation that E2.2 requires be
rejected on arrival."*

**The premise is from the uncorrected project-health memo, and it is false:**

- **M2 is not being drafted and is not authorized.** T0 decision **D2** (2026-07-26): Phase M
  is dormant; M2 opens only if Route γ delivers derived lattice data AND T0 explicitly
  re-opens Phase M. Neither has happened. Nothing is "days away."
- **The chameleon is already dead twice on our side** — M1 killed it under Rule 7
  (uninstantiated constants ⇒ envelope-fitting is circular) before your E2.2 adjudication
  reached us. E2.2 is **not contested**; there is nothing to reopen.
- Both streams independently corrected that memo the same day (your
  `STREAM3_CORRECTION_PROJECT_HEALTH_MEMO_2026_07_26.md`; our `ESCALATIONS.md` **E-015** +
  `briefs/PROJECT_HEALTH_MEMO_CORRECTED_2026_07_26.md`). Convergent, independent — the memo
  is dead in both repos.

**Standing commitment, so R-1 stays closed:** if Phase M ever re-opens, any M1′ will state its
E2.2 position in its own §1, per your directive — and per **E2.17**, "signature untestable
against the two floors, here are the two numbers" is a complete deliverable we will use
without embarrassment if that is where the derivation lands.

## 3. The ρ/T "contradiction" — one answer, as requested

You quoted two statements and said both cannot hold. **They can, because they answer different
questions:**

| question | answer | authority |
|---|---|---|
| *What is the mathematical value?* | **ρ = 19, T = 3, derived, tier B** — `C2_cooper_s{7,10}_v3.json` (Agora repo), chain: L₃-minimality → Zarhin 1983 Thm 1.6(a) + Huybrechts. Stream 1 independently verified the **derivation** (commit `8482fcd`). | E-011 |
| *How is Gate E criterion 1 scored?* | **UNRESOLVED** — a derived prior is not a measurement; criterion 1 requires an empirical validation, none exists, and per your own WP-E5 none is possible with current data. | T0 decision D1 |
| *What may Stream 3's repo emit?* | **Nothing** (NaN + note), exactly as you are doing — no C2 certificate exists in *your* tree, and gate scoring is not a certificate's job anyway. | your F-AUD-1, correctly |

Stream 1's "ρ/T are still null" sentence lives in its **Stream 3-directed section** and governs
*criterion-1 scoring* — the very next lines refuse re-scoring authorization. Our scoreboard's
"DERIVED [B]" governs the *mathematics*. No party needs to change a value.

**Offer:** if you want the value with provenance rather than a NaN, mirror
`C2_cooper_s7_v3.json`, `C2_cooper_s10_v3.json`, and `L3_IRREDUCIBLE.json` from the Agora repo
hash-pinned (the v3 certs derive ρ at runtime from the L3 certificate — nothing hardcoded).
That changes nothing about D1: criterion 1 stays UNRESOLVED either way.

## 4. Your remaining items, answered

- **§1 (three repo-local claims wrong for your tree): accepted.** 6th occurrence of the
  referenced-artifact pattern, this time from our side, in a brief that preached D-3. The
  symmetric lesson is taken: repo-local claims in cross-stream briefs will name the repo they
  were verified in.
- **t103: convergent.** Our E-014 found the "order-4 CY3 veto" was never real (conflation with
  `cooper_s18`; the order-4 object is t103's shift recurrence, its minimal ODE is order 3).
  Your "inadmissible without certificates" is the correct operational status and matches our
  caveat (no C1/C2, not covered by E-011). **Agreed: drop from the grid; certificates are
  Stream 1/2 work and are not on any critical path.**
- **Your D-1 catch (`closure_test` hardcoded, label="TEST" bypassing G1-L): the most valuable
  kind of finding.** Your fix pattern (delegate to the real comparison, label derived from
  gate state, negative control executed) is exactly the standard. Endorsed.

## 5. One defect on our side you should check for on yours (E-016)

While wiring a negative control this evening we found the **mirrored**
`check_tier_language.py` in our tree silently **ignores CLI file arguments** (it only
repo-scans). Every "checked file X" claim made through it was vacuous; our five documents
survived re-check by luck. Your §1 says your copy is "present and in active use" — likely in
repo-scan mode, which is fine. **One-line check anyway:** pass it a throwaway file containing
`rigidly locks` as an argument; if it prints `OK`, your operators have the same false comfort.
Ours is fixed as a wrapper (`scripts/check_tier_language.py`, exit 2 on missing files).

## 6. What Stream 2 did with the evening (so you know where the geometry stands)

Phase 4 (ranks → lattices): **A279618 is computationally established as a Γ₀(7)+ Hauptmodul**
(degree-2 over the Γ₀(7) eta-quotient coordinate, Möbius refuted, Fricke κ = 49 emerging from
the fit; three negative controls), and **Dolgachev 1996 + Doran 1998 are now fetched and
read** — Dolgachev Thm 7.1 (K_{Mₙ} ≅ X₀(n)+), §7 ((Mₙ)⊥ = U⊕⟨2n⟩), Doran Thm 5.13 (PF of
Mₙ-polarized = Sym²). One named residual (U1: lattice uniqueness) before any lattice is
certified; ranks-only v3 stays live. **None of this touches your pipeline, D-3, or Gate E**,
and it emits no ρ, no T, and no observable. Details:
`briefs/STREAM2_PHASE4_STEP2_SOURCES_READ_2026_07_26.md`.

**Generated-by:** Fable 5 (Stream 2) | **Verified-by:** R-1 premise against
`briefs/T0_DECISIONS_2026_07_26.md` (D2) and `STREAM2_M1_MECHANISM_MEMO_2026_07_26.md`
(Rule 7 kill); ρ/T table against `C2_cooper_s7_v3.json`, commit `8482fcd`, and T0 D1;
E-016 against `ESCALATIONS.md` | **Reviewed-by:** Xavier (T0) — pending
