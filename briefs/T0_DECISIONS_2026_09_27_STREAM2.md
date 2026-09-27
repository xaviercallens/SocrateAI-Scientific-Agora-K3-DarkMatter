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
| D9′-5 | Start WP-S2-CERT: certified (ball-arithmetic) monodromy replacing the numeric recognition gate | **STEP 1 LANDED the same day**: `checkers/check_certified_monodromy_L2.py` certifies, for **both** families, that every Sym² monodromy entry recognised by `check_U1_lattice.py` stage 2 is the unique rational of denominator ≤ 10⁴ inside a rigorous enclosure (Arb balls, majorant tail bounds, exact rational centres). s7: diameters 1.5e−96 / 1.0e−115; s10: 4.2e−102 / 2.2e−115; cusp loop encloses [[1,1],[0,1]] to 1e−116. Certificates `CERTIFIED_MONODROMY_L2_cooper_s7.json`, `_s10.json`. **Step 2 landed too**: the certified matrices are fed into the exact stage 3 and the derived lattice equals the lattice certificate field by field — 9/9 vs `C2_cooper_s7_v5.json` (LIVE) and 9/9 vs `C2_cooper_s10_v4_DRAFT.json` (ADVISORY); a tampered certified matrix is refused by stage 3 (control N8). **Does not promote s10** (lattice cert stays DRAFT, D6′) and does not change the Tier B identification of the invariant lattice with T | `checkers/check_certified_monodromy_L2.py`, `checkers/test_certified_monodromy_L2_controls.py`, two certificates |
| — | The review's laboratory programme for Stream 3 (asks item 4) | **No recommendation was made, so nothing is ruled.** It stays *offered* in the Stream 3 delivery note, entering only under the pin protocol | — |
| — | The review's spec-edit list (asks item 3) | Moot: the spec was REJECTED 2026-09-16 | — |

**Follow-ups offered to T0 after D9′ (not ruled, same day).** (i) `C2_cooper_s7_v6_DRAFT.json` — v5
content with one change of provenance (stage-2 matrices certified instead of recognised at 1e−35;
`derived_identical_to_v5: true` asserted at emission). v5 stays LIVE until T0 accepts v6, as with
v4→v5 (D5′). (ii) The §5 status table now carries, in the C2 cell, "stage-2 monodromy CERTIFIED, chain to
this lattice closed" for both families, read from the `CERTIFIED_MONODROMY_L2_*` certificates (renderer
control N16: an open chain renders loudly; a reference mismatch refuses). Neither item promotes s10.

## D10′ — same day, later: v6 accepted, PR merged, streams informed

**Form of the ruling, verbatim:**

> accept v6 draft and merge the PR and inform Stream 1 and stream 3

| # | Ruling | Applied |
|---|---|---|
| D10′-1 | **`C2_cooper_s7_v6_DRAFT.json` ACCEPTED** → promoted to `C2_cooper_s7_v6.json`, LIVE, lattice authority for cooper_s7 | derived block asserted identical to v5 at promotion; `t0_acceptance` block carries the verbatim words; v5/v5_DRAFT/v4/v4_DRAFT/v3 retained unchanged; certificates whose inputs pin v5's hash stay valid (identical values); v3 remains the rank source. `K3_CRITERIA.md` C2 status line, renderer source map, certified checker's stage-3 reference and the witness checker's `--all` list updated to v6; s7 certified-monodromy certificate re-emitted against v6 |
| D10′-2 | **Merge PR #55** | merged by Stream 2 on this instruction (merge commit, branch `stream2/status-table-renderer-2026-09-27`) |
| D10′-3 | **Inform Stream 1 and Stream 3** | notices placed untracked in their repos with the post-merge `K3_CRITERIA.md` sha256 |

Not ruled by D10′: cooper_s10 (still ADVISORY, D6′); the lab programme for Stream 3; any selector (AM-6).

## D11′ — same day, later: decisions taken by Stream 2 under T0's explicit delegation

**Form of the delegation, verbatim:** "help me take decision on my behalf" (with the workflow-scoped
GitHub token supplied in `~/.gh_workflow_token`). Each decision below is the conservative reading of
the standing rules, is **reversible by one T0 sentence**, and is marked as taken *on T0's behalf*, not
by T0. Anything that needs new evidence (a fetched source, a lab partner, an EFT draft) is **not**
decided here.

| # | Item | Decision on T0's behalf | Reversal path |
|---|---|---|---|
| D11′-1 | CI Gates A/B red since 2026-09-17; fix on local branch, push blocked (token lacked `workflow` scope) | Branch `ci/fix-gates-2026-09-17` **pushed** with the new token. Opening and merging its PR was left to T0 (the automated permission layer refused the PR-creation command). Recommendation: open, merge, then close PR #44 as superseded (it is the non-workflow half of the same fix) | close the PR without merging |
| D11′-2 | t103 (§1 frozen row `DROPPED`; Stream 1 flag unanswered since 2026-08-01; E-014: never vetoed) | **Row stays DROPPED**, ground narrowed: the "order-4 CY3" ground is **withdrawn** (E-014, category error corrected); the ground that stands is §1's own rule — *no citable defining recurrence at freeze time* — until a primary source for t103's recurrence is fetched, read and pinned. Reinstatement = §6 amendment carrying that citation; nobody may add C1/C2 work on t103 before it | fetch + pin a source, then a §6 PR |
| D11′-3 | The Fable review's laboratory programme (E1–E4) for Stream 3 | **PARKED** (declined for now): no observational element by the review's own statement; laboratory physics is outside Stream 3's scope and outside anything this program can execute; nothing in it touches a K3 claim. Stays in the record as an offered appendix | T0 text naming a laboratory partner opens it under the pin protocol (rule 5) |
| D11′-4 | Two Deep Think referrals with no reply on record since 2026-07-31 / 2026-08-01 (TW2A Reading 1/2; s10 composite level) | **RETIRED as unanswered** (closed, not resolved). Their questions remain open in the ledger; no text may cite them as answered | a reply, audited before citation, reopens either |
| D11′-5 | Flux bound on D (`T0_DECISION_REQUEST_FLUX_BOUND_ON_D_2026_09_21.md`, own recommendation: park) | **PARKED** per the brief's Q1 = no (K3×P¹ is not a specified B₃), Q2 = option A. S3-00b stays BLOCKED (F5b) | a specified B₃ |
| D11′-6 | TODO item "narrow ATKIN_LEHNER_ACTION_UNVERIFIED" | **Already done by D8′/AM-4** (flag retired, PASS(30)); item closed as superseded | — |
| D11′-7 | TODO item "does C3 require an integral partner?" | **Already ruled by D8′/AM-2** (integrality not part of C3; constant reported, never gated); item closed as superseded | — |
| — | cooper_s10 promotion; criteria v1.0 freeze; C4/C5 `TBD-AT-FREEZE`; any selector (AM-6) | **Not decided** — each needs evidence or a freeze, not a reading of the rules | — |

*Recorded by Claude (Fable 5.1), Stream 2, 2026-09-27. Reviewed-by: T0 — delegation Y, individual
decisions N (taken on T0's behalf; T0 may strike any row).*

**What this ruling does not do.** It adopts no selector (AM-6 requires one to be *named* by its own T0
text before any member is preferred); it changes no certificate value; it does not promote `cooper_s10`
(still ADVISORY, D6′); it does not freeze the criteria (§7 still open, and now one item longer); it does
not adopt any physical reading.

**Impact statement (§6):** no ranking run exists, so none is invalidated. `K3_CRITERIA.md` sha256
right after this ruling was `e7d420af…`; after the same-day §5 re-render with the certified-monodromy
note it is `8e6c5d17e84360bb70ae4f298f33df25a1106efe51dd0052e6865e904b337531`. Stream 1 and Stream 3
mirrors re-pin to the value **at merge** (`git show main:K3_CRITERIA.md | sha256sum`); the §5 table is
generated and moves with certificate changes, so no quoted value here is authoritative past merge.

**Reading rule applied:** "follow your recommendation" was read as covering exactly the items on which
a recommendation had been stated and nothing wider (cf. `feedback_menu_choice_is_not_a_ruling`).

*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: T3 key-diff, `render_status_table.py --check`,
renderer + audit controls, tier lint, all run after the edits | Reviewed-by: T0 Y (ruling), record N*
