# T0 decisions — 2026-09-27 (Stream 2) — D9′

**Ruled by:** T0 (Xavier Callens), in session, 2026-09-27. **Recorded by:** Claude (Fable 5.1), Stream 2.
**Form of the ruling, verbatim:** after the audit report on the external review
(`briefs/EXTERNAL_REVIEW_FABLE51_AUDIT_AND_DIRECTIONS_2026_09_27.md`) and the PR #55 report, T0 wrote:

> ok follow your recommendation

The recommendations on the table at that moment, and what was done with each:

| # | Recommendation (where stated) | Ruling as applied | Artifact |
|---|---|---|---|
| D9′-1 | Adopt **AM-6**, the C6 selector clause (audit brief §4; asks item 1) | **ADOPTED**, exact text as proposed; §7 checklist item added; §6 version row v0.1d | `K3_CRITERIA.md` C6, §6, §7 |
| D9′-2 | Correct the §2 C3 route-1 checker path to `checkers/check_C3b_symsqrt.py` (PR #55 finding F-a; **AM-7**) | **ADOPTED** as a path correction with the history kept in the sentence | `K3_CRITERIA.md` C3 |
| D9′-3 | Re-emit `T3_LEVEL_CONSISTENCY.json` with the stale "not an adopted gate" wording fixed, values unchanged (PR #55 finding F-b) | **DONE**; diff against `main` shows only `status` changed (checked by key comparison, all other keys identical) | `checkers/check_T3_level_consistency.py`, certificate |
| D9′-4 | Allow the `python-flint` install for **WP-S2-CERT** (audit brief §5; asks item 2) | **ALLOWED**; installed `python-flint 0.9.0` (Arb ball arithmetic: `acb`, `arb`, `acb_mat`, `acb_series`) | environment, this machine |
| D9′-5 | Start WP-S2-CERT: certified (ball-arithmetic) monodromy replacing the numeric recognition gate | **STEP 1 LANDED the same day**: `checkers/check_certified_monodromy_L2.py` certifies, for **both** families, that every Sym² monodromy entry recognised by `check_U1_lattice.py` stage 2 is the unique rational of denominator ≤ 10⁴ inside a rigorous enclosure (Arb balls, majorant tail bounds, exact rational centres). s7: diameters 1.5e−96 / 1.0e−115; s10: 4.2e−102 / 2.2e−115; cusp loop encloses [[1,1],[0,1]] to 1e−116. Certificates `CERTIFIED_MONODROMY_L2_cooper_s7.json`, `_s10.json`. **Does not promote s10** (lattice cert stays DRAFT, D6′) and does not change the Tier B identification of the invariant lattice with T | `checkers/check_certified_monodromy_L2.py`, `checkers/test_certified_monodromy_L2_controls.py`, two certificates |
| — | The review's laboratory programme for Stream 3 (asks item 4) | **No recommendation was made, so nothing is ruled.** It stays *offered* in the Stream 3 delivery note, entering only under the pin protocol | — |
| — | The review's spec-edit list (asks item 3) | Moot: the spec was REJECTED 2026-09-16 | — |

**What this ruling does not do.** It adopts no selector (AM-6 requires one to be *named* by its own T0
text before any member is preferred); it changes no certificate value; it does not promote `cooper_s10`
(still ADVISORY, D6′); it does not freeze the criteria (§7 still open, and now one item longer); it does
not adopt any physical reading.

**Impact statement (§6):** no ranking run exists, so none is invalidated. `K3_CRITERIA.md` sha256 after
this ruling: `e7d420af01f07cd14d03468ee704e6eec3acc9f85d9fe2249688a0f74f9c2151` — Stream 1 and Stream 3
mirrors re-pin to this value (supersedes the `993350cf…` value quoted earlier in PR #55).

**Reading rule applied:** "follow your recommendation" was read as covering exactly the items on which
a recommendation had been stated and nothing wider (cf. `feedback_menu_choice_is_not_a_ruling`).

*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: T3 key-diff, `render_status_table.py --check`,
renderer + audit controls, tier lint, all run after the edits | Reviewed-by: T0 Y (ruling), record N*
