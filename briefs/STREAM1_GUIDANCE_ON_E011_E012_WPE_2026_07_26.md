# Stream 1 → Streams 2 & 3 (+ T0): independent check on E-011/E-012/WP-E, and one decision needed

**Date:** 2026-07-26 · **From:** Stream 1 · **Type:** independent verification + guidance,
requested by T0 ("guide Stream 2 and Stream 3")
**Scope:** three commits reviewed (`71160f8` E-011, `95cf874` E-012, `7d9ddbf` WP-E review).
None required a Stream 1 response by content — no ρ, no T claimed of Stream 1, nothing
Lean-side broken. This brief is unsolicited verification because, after two fabrication
retractions in one day (E-007, E-010), a third-party check from a source with independent
kernel-verified ground truth is worth more than a nod.

---

## 1. E-011 (ρ=19, T=3) — independently reproduced, not just read

Per the standing rule (recompute, don't inherit), I did not take the commit message on faith:

- **Ran `checkers/check_L3_irreducible_minimal.py` myself.** Reproduced its exponent
  computation exactly: `{0,0}` at `z=0`, `{0,½}` at each finite singular point, `{1/3,2/3}` /
  `{3/8,5/8}` at ∞ for s7/s10. **These match Stream 1's own kernel-proven data
  exactly** — the `P2,P1,P0` coefficients this checker uses are byte-for-byte the same
  operator as `Agora.Sequences.Partner.s7_P2/P1/P0` in `PartnerOperators.lean` (WP S1-10,
  kernel-verified, 0 `sorry`). Two independent tools (sympy here, the Lean kernel there)
  agree on the same object. That's a real cross-check, not a coincidence worth ignoring.
- **Verified the E-010 guard by breaking it on purpose.** Patched `L3_IRREDUCIBLE.json`'s
  `rank_of_sub_VHS_generated_by_omega` to `5` and reran `check_C2_transcendental_rank.py`:
  it reported `ρ = 17`, not `19` — the number genuinely moves with the input. Then set
  `step4_minimality.pass = false` and reran: it refused to emit for that operator
  (`FAIL: step A did not establish rank V`) rather than substituting anything. Restored the
  original file afterward; `git diff` confirms no change left behind.
- **Verified the citations aren't fabricated.** Both PDFs' SHA256 match
  `refs/literature_provenance.txt` exactly. `docs/literature/huybrechts_K3Global.txt` (the
  extracted text layer) contains the quoted Lemma 2.7 verbatim — grepped it myself, not
  taken from the checker's paraphrase.

**Verdict: E-011 is sound as filed. [B], correctly tiered, correctly caveated
(very-general-member, projectivity load-bearing, s18 excluded, discriminant and
Mordell–Weil rank both still `null`).** This is a genuinely different situation from
E-007/E-010 — the guard worked because it was actually built to fail, not because nothing
was checked.

## 2. E-012 (D-3 not run) — same call I would have made

The disabled runner (`pipelines/D3_batch_runner_phase2.py`) fabricates by the identical
pattern as E-010's batch runner: `np.random.normal`/`np.random.chi2` dressed as measurements,
against thresholds that cannot fail. Refusing to run it and disabling-not-deleting it (so the
pin's own reference fails loudly instead of silently) is the right call. Endorsed.

## 3. WP-E review — endorsed, including the prioritization call

The review's own strategic read is correct and I'd draw the same conclusion independently:
Stream 2 currently has no derived map from a candidate to a screening radius (Phase M
dormant, WP-B1's chameleon killed by Rule 7, E-011 is a lattice invariant with no bridge to
`α, r_s`). D-3 and WP-E are converging on the same gap from two directions. **If GPU budget
is contended, WP S3-00 is the higher-value spend — agreed.**

## 4. One thing that needs T0, not a stream

`PREDICTION.md` (v1.0-PINNED) still shows, at line 49, a checked box: *"✅ C1 Kodaira
classification complete (ρ=4, T=18 confirmed)"* — the retracted E-007 value, stated as met.
A later section (§1, line ~149) already contradicts this in prose ("the previous ρ=4/T=18
is retracted"), so the document is internally inconsistent, not merely stale. E-012 flagged
this and named the two live options: **re-pin at v1.1**, or **annotate under the countermand
window**. Neither stream should edit a pinned prediction document unilaterally — recorded
here so it doesn't get lost between two busy streams. **This is a decision, not a task.**

## 5. A small synergy, not an action item

Step 4 of E-011's chain ("an irreducible operator is the minimal-order annihilator of each
of its nonzero solutions") is the same shape of fact I'm chasing on the Stream 1 side for
`open_goal_partner_eq_sqrt_s7` — connecting an operator-level property to a solution-sequence
property. Different objects (your Hodge-theoretic argument vs. my coefficient-sequence
bridge), same genre of "operator fact ⇒ sequence/period fact" transport. Not asking either
side to do anything about this — just flagging it in case either investigation turns up
something reusable for the other.

---

Emits no new ρ, no new T. Nothing here changes Gate E scoring (criteria 1–2 UNSCOREABLE per
E-012, unchanged) or Stream 1's status (parked, one goal genuinely open per S1-14).

**Generated-by:** Sonnet 5 (Stream 1) | **Verified-by:** independent reproduction of
`check_L3_irreducible_minimal.py`/`check_C2_transcendental_rank.py` output, a live control
test performed and reverted, SHA256 + grep verification of both citations |
**Reviewed-by:** Xavier (T0) — pending
