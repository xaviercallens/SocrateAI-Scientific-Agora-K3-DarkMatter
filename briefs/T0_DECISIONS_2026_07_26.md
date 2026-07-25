# T0 Decision Record — 2026-07-26

**Authority:** Xavier Callens (T0 Owner), verbal authorization in-session 2026-07-26
("yes I authorize you on the decisions accept them"), given in direct response to the
decision list presented with the M1 filing. Recorded by Fable 5 (T1 execution).
**Scope note:** this record covers exactly the four decisions that were on the table in
that exchange — nothing broader is inferred from a verbal authorization.

---

## D1 — Gate E criterion 1: scored UNRESOLVED ✅ DECIDED

**Decision:** Gate E criterion 1 ("lattice structure validated") is scored
**UNRESOLVED** for the 2026-07-27 EOD verdict. The other five criteria proceed and are
scored on their own evidence. **The Gate E date is kept.**

**Basis:** E-007 — the ρ=4 / T=18 lattice prior used by the running D-3 batch is
permanently withdrawn (traced to a hardcoded constant, not geometry). E-008 — no
replacement derivation exists yet (Route γ untested).

**Consequence, stated plainly:** under the pinned decision logic
("all 6 PASS → PASS; 5/6 → CONDITIONAL; else FAIL"), **a full Gate E PASS is no longer
achievable on 2026-07-27.** The best available outcome is **CONDITIONAL** (five
criteria PASS + criterion 1 UNRESOLVED → human review), which is precisely the honest
reading of the situation. The D-3 run is *not* discarded: its results on the other
five criteria stand, and its criterion-1 outputs are retained as data that can be
re-scored if/when Route γ delivers a derived prior.

**Handoff:** see `briefs/STREAM2_TO_STREAM3_GATE_E_CRITERION1_2026_07_26.md`.

## D2 — M1 accepted; Phase M gated on Route γ ✅ DECIDED

**Decision:** the M1 mechanism memo (`briefs/STREAM2_M1_MECHANISM_MEMO_2026_07_26.md`)
is **accepted as filed**: a conditional negative. Phase M is now **dormant**. M2 (the
two-model derivation step) is **not authorized** and does not open until BOTH:
1. Route γ (ramified Hauptmodul pullback) yields an integral-exponent operator and
   derived C1v3/C2v3 lattice data, and
2. T0 re-opens Phase M by explicit decision against a revised M1′.

If Route γ fails, the filing of that failure constitutes the program's clean third
negative (after F5b and Off-Ramp 3) and Phase M closes without M2.

## D3 — Stream 3 artifact mirroring: authorized ✅ DECIDED

**Decision:** Stream 3 is requested/authorized to mirror into this repository,
hash-pinned: `docs/WP_R6_SURVEY_SCALES.md`, `docs/WP_R7_BETA_VARIANCE_SCAN.md`,
`NO_PREDICTION_BRANCH.md`, `check_tier_language.py`, `pipeline/siblings.py` (and any
other artifact a future directive references). **Standing rule going forward:** a
directive whose referenced artifacts are absent from the executing repo is returned
for provenance before execution — this is the third occurrence of the pattern
(nonexistent checkers in the Stream 2 plan; false Lemma 4 in the WP-B1 brief; 14/16
absent here).

## D4 — Wall-3 renunciation: standing policy ✅ DECIDED

**Decision:** until a base B₃ is specified and the tadpole condition is posable, **no
model under this program makes any dark-energy / vacuum-energy claim.** Recorded as a
dated addendum to `ASSUMPTIONS.md` (entry **A-DE**), inside the signed A-* register's
amendment discipline.

---

## Explicitly NOT covered by this authorization

- **WP-B1 deviation sign-off** (`briefs/STREAM1_WP_B1_RESULTS.md`: the restated
  `force_range_bounded` and the corrected, formerly-false `no_unscreened_lmp`). This
  was not in the decision list the authorization responded to. It remains the **one
  open T0 item** and is left pending in `TODO.md`.

---

**Generated-by:** Fable 5 (T1 execution of T0 verbal authorization) | **Verified-by:** decision basis traced to ESCALATIONS.md E-007/E-008 + M1 memo | **Reviewed-by:** Xavier (T0) — authorization 2026-07-26, countermand window open as always
