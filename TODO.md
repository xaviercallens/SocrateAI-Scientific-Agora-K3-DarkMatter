# ✅ TODO — restart here

**Last updated:** 2026-09-21 (s10 lattice cert kept DRAFT by T0; orientation block below dates from 2026-07-26) · **Release:** `v0.3.11-criteria-canonical` · **Previous TODO:** commit history

> ## 30-second orientation
>
> **The mathematics is done. The physics branch closed honestly. Nothing is on fire.**
>
> - **ρ = 19, T = 3 — DERIVED** [tier B], E-011; derivation independently verified by Stream 1.
>   (**Value ≠ gate scoring**: Gate E criterion 1 stays UNRESOLVED per T0 D1 — a derived prior
>   is not a measurement. Both statements hold; do not conflate them — that conflation cost
>   Stream 3 an escalation.)
> - **F5b — no prediction extractable.** Adopted into `PREDICTION.md` **v1.1-PINNED §6**.
>   Pre-registered outcome, **not** a refutation, and **reversible**.
> - **Gate E criteria 1–2 UNSCOREABLE** (no valid empirical run exists). *Not failing.*
> - **Stream 1 parked clean. Stream 2: Phase 4 running (lattice refinement — one residual, U1).
>   Stream 3: WP-E5 COMPLETE — 2D transverse route closed (floors 1.6 Mpc / 10⁴ objects);
>   directives E2.18–E2.23 adopted.**
>
> Full history: `ESCALATIONS.md` E-007 … E-013. Governing docs: `VISION.md`, `EXECUTION_PLAN.md`
> (both restored 2026-07-26 — they had been deleted since 07-18).

---

## 🔴 Open — needs a human

- [x] **T0: v0.4.0 — ANSWERED (2026-07-27, D4′):** it still means "Gate E PASS", original
      meaning retained; stays parked until a valid empirical route exists (D1/E-012
      unchanged). Record: `briefs/T0_DECISIONS_2026_07_27_STREAM2.md`.
- [x] **T0: `EXECUTION_PLAN.md` §S3-00 step 2(b) — RE-SCOPED (2026-07-27, D2′/AL-1):**
      re-posed on the certified M₇-polarized lattice data (C2 v4), posable only given an
      exhibited X₄/B₃; Kodaira wording retracted-retained for audit; amendment AL-1
      propagated to all three mirrored copies. F5b stands.
- [x] **Stream 3 asks — ALL ANSWERED** (2026-07-26 night, their
      `STREAM3_TO_STREAM2_DIRECTIVE_RESPONSE_2026_07_26.md` + WP-E5 findings, Dark Home repo
      `~/SocrateAI-Scientific-Agora-Home`): **(a)** no D-3 run, no 3D data anywhere — 50
      spectroscopic objects is the largest field; **(b)** no Gate E verdicts exist (verified by
      search; runner never produced output, G1-L closed); **(c)** pre-flight σ(0) = **NO-GO**,
      worse than predicted — β₂ *degenerate* (zero variance at 2/3 thresholds), not offset;
      **(d)** t103 inadmissible-without-certificate (convergent with E-014). **WP-E5 CLOSED
      the 2D transverse route**: floors ~1.6 Mpc / ~10⁴ objects per slice; real data 50× short;
      no (r_s, α) bounding box deliverable, by design. Directives **E2.18–E2.23 adopted** into
      Stream 2 standing practice. Response:
      `briefs/STREAM2_TO_STREAM3_WPE5_RESPONSE_2026_07_26.md` (also dissolves their R-1 — no
      M2 exists to reject — and resolves the ρ/T "contradiction" as value-vs-gate-scoring).

## 🟡 Open — mechanical, any agent can pick up

- [x] **Correct `stream3_mirror/NO_PREDICTION_BRANCH.md` §2/§5 at source — DONE (2026-07-27).**
      Dated correction notes added at source (Dark Home repo: §2 certificate table + §8
      obstruction basis; also `PREDICTION_APPENDIX_A.md` §A.1.4/§A.3.4, whose Type II veto
      cited the retracted certificates); mirror refreshed from corrected source. F5b
      unaffected, as expected. See
      `briefs/EXTERNAL_UNBLOCK_PLAN_RECONCILIATION_2026_07_27.md`.
- [x] **`t103` status — RESOLVED (E-014, 2026-07-26): not vetoed.** No T0 record vetoing it exists
      anywhere in the repo; every classification artifact (Phase A/B/C findings, GATE-C, the Lean
      file itself) already agreed it is K3-type, order-3 ODE, GATE-C finalist. The "order-4 CY3"
      claim conflated it with `cooper_s18` (the actual order-4, CY3-*shape*, non-MUM candidate).
      t103 stays in the pool, with the pre-existing caveat that it has no C1/C2 work and is not
      covered by E-011's ρ=19/T=3.
- [x] **`scripts/v5_dual_scale_pipeline.py` — DELETED** (2026-07-26, plus its twin
      `_stub_tobeupdate.py`). It advertised the retracted legacy program (Δ-spikes, weak
      lensing, NANOGrav). README link removed.
- [x] **`scripts/gate_e_verdict.py` criterion 5 — REAL and fail-closed** (2026-07-26). Audits
      via the tier-language wrapper; missing checker/files/empty list all FAIL. Also fixed while
      there: expected ρ was the **retracted 4.0 hardcoded** — now read at runtime from
      `C2_cooper_s7_v3.json` (null ⇒ raise); and the script refuses D-3 aggregates entirely
      (E-012: their only producer fabricates). Controls:
      `checkers/test_gate_e_verdict_controls.py` (7, incl. negatives).
- [x] **Dolgachev 1996 / Doran 1998 — FETCHED AND READ** (Phase 4 step 2, 2026-07-26 night,
      hash-pinned in `docs/literature/MANIFEST.md`). The framework verifies **verbatim**:
      Dolgachev Thm 7.1 (K_{Mₙ} ≅ H/Γ₀(n)+), §7 p.20 ((Mₙ)⊥ = U⊕⟨2n⟩), Thm 7.3 (ample locus
      minus countable S = our very-general caveat at source), Doran Thm 5.13 (PF of
      Mₙ-polarized = Sym² of 2nd-order Fuchsian). Record:
      `briefs/STREAM2_PHASE4_STEP2_SOURCES_READ_2026_07_26.md`.
- [x] **U1 — EXECUTED fresh-context 2026-07-27, U1a PASS with all controls; U1 CLOSED [B]
      pending T0.** Full record: `briefs/STREAM2_U1_EXECUTION_2026_07_27.md`; pipeline
      `checkers/check_U1_lattice.py`; controls `checkers/test_U1_controls.py` (different-level
      s10 → det −20/2n = 20, scrambled-matrix ×3, Yukawa-scramble — all fail loudly as
      required). **Derived (never typed): Gram [[0,0,−1],[0,14,0],[−1,0,0]], det = −14,
      signature (2,1), disc form ℤ/14 (q = 1/14), 2n = 14 from (T_cusp−1)² divisibility, and
      an EXPLICIT integral base change realizing U⊕⟨14⟩** (constructive isometry ⇒ the Eichler/
      Cassels genus route became unnecessary — Cassels NOT fetched, no 2-adic claim made).
      Honest findings: (i) the Yukawa VALUE is not extractable independently of the integral
      lattice — constancy (exact to q³¹) is the checkable part, value 14 comes from stage 3, as
      the route design anticipated; (ii) residual Tier-B links: numerical recognition of
      monodromy entries (~1e−59 residuals vs 1e−35 gate) and the framework identification of
      the monodromy lattice with T (Dolgachev/Doran, read; overlattices enumerated: none).
      `C2_cooper_s7_v4_DRAFT.json` emitted → **ACCEPTED by T0 2026-07-27 (D1′): live as
      `C2_cooper_s7_v4.json`** (draft retained for audit; v3 remains runtime source for
      ranks). **H-M7 upgrade is PARTIAL: T-half [B], NS-half stays [C]** (Nikulin step
      unexecuted). Phase M: Option B — dormant, re-gated on an exhibited X₄/B₃ (D3′).
      **Superseded as of D5′ (below): `C2_cooper_s7_v5.json` is now the LIVE lattice
      certificate** (v4/v4_DRAFT retained unchanged for audit; v3 still the rank
      source). Record: `briefs/T0_DECISIONS_2026_07_27_STREAM2.md`.
- [x] **E-016 → Stream 3: told**, with the one-line self-check, in
      `briefs/STREAM2_TO_STREAM3_WPE5_RESPONSE_2026_07_26.md` §5.
- [x] **U1 witness serialization — DONE (2026-07-27, T0-ruled); v5 PROMOTED TO LIVE
      (2026-07-27, D5′).** Motivated by Stream 1's independent-verification finding
      (their `briefs/STREAM1_U1_INDEPENDENT_VERIFICATION_2026_07_27.md`): the
      base-change matrix P was computed but not serialized. `derived.u_splitting
      .basis_change_matrix` added to `check_U1_lattice.py`'s output (additive
      only); `C2_cooper_s7_v5_DRAFT.json` emitted via `--emit-cert-v5`, then
      **accepted by T0 and promoted to `C2_cooper_s7_v5.json` (now LIVE, supersedes
      v4 in that role)**; v3/v4/v4_DRAFT untouched (SHA256-verified before and after
      promotion). Checker `checkers/check_U1_witness_serialization.py`
      (`--all` now checks v3, v4, v5, v5_DRAFT) + `checkers/test_U1_witness_
      serialization_controls.py` (7 controls, python3 + pytest green;
      missing-witness on v3/v4 reports WITNESS_ABSENT, not FAIL; v5 and v5_DRAFT
      both PASS). Records: `briefs/STREAM2_P_WITNESS_SERIALIZATION_2026_07_27.md`,
      `briefs/T0_DECISIONS_2026_07_27_STREAM2.md` (D5′).

- [x] **cooper_s10 lattice certificate — T0 ruling 2026-09-16: stays DRAFT.** Asked
      explicitly; answer: keep `C2_cooper_s10_v4_DRAFT.json` as DRAFT. T(s10) ≅ U⊕⟨20⟩ stays
      formally uncertified, and G0-s10's gap statement stands. The independent re-derivation
      (23/23 + 10/10) remains on record as a recommendation only. Record:
      `briefs/T0_DECISIONS_2026_09_16_STREAM2.md`. (A promotion commit made earlier the same
      day on a menu selection was reverted.)
- [x] **Deep Think referrals — RETIRED as unanswered (D11′, 2026-09-27, on T0's behalf):** TW2A
      Reading 1/2 (`briefs/DEEPTHINK_ALIGNMENT_BRIEF_TW2A_Q1_2026_07_31.md`) and s10 composite level
      (`briefs/DEEPTHINK_ALIGNMENT_BRIEF_S10_COMPOSITE_LEVEL_2026_08_01.md`): no reply on record in any
      repo after ~2 months. Closed, not resolved — the questions stay open in the ledger; a reply,
      audited before citation, reopens either.
- [ ] **T0: review the K3×T² criteria proposal** —
      `briefs/STREAM2_K3xT2_SELECTION_CRITERIA_PROPOSAL_2026_09_16.md` (Reading S vs P, new
      two-lineage gate T3, replace Kodaira C2 with the lattice gate, no scoring yet). Not a
      freeze; `K3_CRITERIA.md` unchanged.
      **2026-09-21: T3 is now runnable** — `checkers/check_T3_level_consistency.py`
      (+ 25 controls incl. four REAL order-3 known-bads, a Mobius-clause known-bad, and the
      Stream-1-sourced Gauss-determinant control). s7 → AGREE(n=7) CONSISTENT; s10 → AGREE(n=10)
      with two *separate* open flags (`LATTICE_CERT_DRAFT` process, `ATKIN_LEHNER_ACTION_
      UNVERIFIED` mathematics). Proposal's "independent computations" corrected to "two
      disjoint computations on the same operator". Record + asks:
      `briefs/STREAM2_T3_LEVEL_CONSISTENCY_2026_09_21.md`. T3 still NOT adopted.
- [x] **T0: the ρ = 20 fork — RULED 2026-09-21 (D7′): ADOPTED, read narrowly.** Record:
      `briefs/T0_DECISIONS_2026_09_21_STREAM2.md`; ledger item 8 in `CLAUDE.md`. Adopted: ρ = 20 as a
      selection criterion. NOT adopted (each needs its own T0 text): ranking s7 over s10, any
      minimum-|D| rule, promotion of s10 (still ADVISORY), any physical reading, any edit of
      `K3_CRITERIA.md`, gate T3. Certificates re-emitted with the new status wording; no computed
      value changed. Content of the cut: `CM_POINTS_RHO20.json`, `A2_MEMBERSHIP.json`.
- [x] **T0 D8′ (2026-09-21): `K3_CRITERIA.md` is now CANONICAL HERE**, seeded byte-identical from
      Stream 1 @ `6c09d2d` (`f62f2c8`) then amended (`ea2b181`). **C6** = the ρ = 20 cut (narrow,
      unscored); **C3** literal — integrality is NOT part of it, the constant c is reported only, so
      both primaries clear C3 and Stream 3's D-2 is closed; **C2** → transcendental lattice (T2),
      Kodaira text struck with E-007; **T1/T3** adopted as unscored consistency gates; the
      Atkin–Lehner flag is retired (verified, PASS(30)) leaving `LATTICE_CERT_DRAFT` alone on s10.
      §4 now says a DRAFT certificate is neither a pass nor a failure. Record:
      `briefs/T0_DECISIONS_2026_09_21_STREAM2.md` (questions + selected options verbatim).
      **Not a freeze** — thresholds stay SKELETON, §7 still blocks v1.0.
- [x] **`scripts/render_status_table.py` — WRITTEN 2026-09-27; §5 table restored, generated.**
      Reads only the §1 register, `refs/recurrences_v1.json` and the certificates named in its
      `SOURCES` map. Each row's refs entry is **derived**: its Cooper params must reproduce exactly
      one refs recurrence, which confirms K-s18 = `avs_sporadic3_s18`. The renderer refuses a
      missing, retracted, wrong-candidate or field-missing source. DRAFT renders as DRAFT
      (ADVISORY). The output is byte-stable because no stamps are rendered. 20 controls in
      `checkers/test_render_status_table_controls.py`. It also surfaced two findings, flagged and
      not fixed, in `briefs/STREAM2_STATUS_TABLE_RENDERER_2026_09_27.md`: §2 C3 names a checker
      that does not exist here, and `T3_LEVEL_CONSISTENCY.json` still self-reports "not an
      adopted gate". K3_CRITERIA.md's hash changed, so the S1/S3 mirrors need re-pinning (same brief).
- [x] **The `K-t103` row of §1 — ANSWERED on T0's behalf (D11′, 2026-09-27):** row stays DROPPED;
      the "order-4 CY3" ground is withdrawn (E-014), the standing ground is §1's own rule (no citable
      defining recurrence at freeze). Reinstatement = §6 amendment carrying a fetched, pinned primary
      source. Stream 1 informed (`STREAM2_TO_STREAM1_NOTICE_PR55_MERGED_2026_09_27.md`, their repo).
- [ ] **T0: C4 and C5 still carry `TBD-AT-FREEZE`** — implementing their checkers is blocked until
      the freeze resolves them (`criteria-checkers` contract).

- [x] **Flux bound on D — PARKED on T0's behalf (D11′, 2026-09-27)** per the brief's own
      recommendation (`briefs/T0_DECISION_REQUEST_FLUX_BOUND_ON_D_2026_09_21.md`: Q1 no, Q2 option A).
      S3-00b stays BLOCKED (F5b). Reopens with a specified B₃.
- [x] **`ATKIN_LEHNER_ACTION_UNVERIFIED` — already retired by D8′/AM-4** (PASS(30),
      `ATKIN_LEHNER_DISC_FORM.json`); item closed as superseded (D11′-6). s10 still advisory.
- [ ] **Open thread GE-10 (hypothesis, still zero tests — but the model now EXISTS, 2026-09-27):**
      `checkers/check_inose_model_M7.py` → `INOSE_MODEL_M7.json`: the explicit M₇-polarized model of
      the s7 family in the Clingher–Doran–Lewis–Whitcher normal form, W₁ = π(z), W₂ = π(z) − σ(z) + 1
      with σ, π exact Laurent polynomials in z (PASS(128)); σ² − 4π has simple zeros exactly at z = −1,
      1/27 (D −7, −28) and double zeros at the other self-7-isogenous CM points (D −12, −19, −27, −24,
      each h(D) times; three of them outside the CM table's window, explained). Brief:
      `briefs/WP_GE10_INOSE_MODEL_M7_2026_09_27.md`. **Step 2 done up to the Kodaira boundary
      (same day):** from Kuwata–Shioda's sourced J₉ equation (transcription verified against their
      printed discriminant), the Inose fibration's discriminant orders are {10,10,1,1,1,1} generically
      and **{10,10,2,1,1} at every J₁ = J₂ ∉ {0,1} — both loci z = −1 and z = 1/27 alike** (d(0) ≡ 0
      when the curves are isomorphic: one order-2 fibre at the branch point). **GE-10 answered at the
      fibre level: no div-2/div-1 difference, no A₁ merging; the second extra class is a Mordell–Weil
      section, not a fibre.** J = 0 → {10,10,4}; J = 1 → {10,10,2,2} (the review's X₃/X₄ rows, at the
      level of orders). `INOSE_FIBRATION_MULTIPLICITIES.json`. Still gated on T0 (ledger item 3
      reading): attaching Kodaira *labels* to these orders.
- [x] **Does C3 require an INTEGRAL partner? — RULED by D8′/AM-2 (literal reading: no; the constant
      is reported, never gated).** Item closed as superseded (D11′-7). Record of the question:
      `briefs/STREAM2_TO_STREAM3_C3_BRANCH_REPLY_2026_09_21.md`; `PARTNER_GLOBAL_BOUNDEDNESS.json`.
- [x] **Defect FIXED 2026-09-21:** `check_C3b_symsqrt.py` tested C(n) == −(n+1)² literally, so a
      genuine MUM partner whose fit clears denominators (Apéry ζ(3): C = −4(n+1)²) was reported
      non-MUM / `FAIL_PARTNER_VALIDATION`. Now `mum_normalise` tests proportionality with a positive
      constant and reports the constant. The golden test that ASSERTED the wrong verdict is
      replaced by a regression (Apéry ζ(3) → `SYM2_OPERATOR_IDENTITY_PROVEN`, constant 4) plus
      function-level known-bads. s7/s10 verdicts unchanged; both certs re-emitted at (n_fit 30,
      deg 5) — the earlier (26, 2) vs (30, 5) parameter drift between them is gone.
      Limitation kept in the test docstring: no end-to-end real non-MUM Sym² bulk in the suite.
- [ ] **T0: external review "K3 Selection Review" (Fable 5.1, 2026-09-21) — recorded + audited
      2026-09-27**, `briefs/EXTERNAL_REVIEW_FABLE51_AUDIT_AND_DIRECTIONS_2026_09_27.md`. Verbatim record
      `docs/literature/external_reviews/…` (manifest row); 12/12 Stream-2 clauses CONFIRMED
      (`EXTERNAL_REVIEW_FABLE_2026_09_21_AUDIT.json`; its W₇ "prediction" was already in
      `CM_POINTS_RHO20.json`). Convergence [B, narrow]: Paper 12's A₂ surface = s7 at z=∞; the ⟨2⟩⊕⟨2⟩
      surface = s10 at z=∞ — no preference (D7′). The spec it reviews (`~/K3spec.md`) was REJECTED
      2026-09-16. **T0 D9′ (same day, "ok follow your recommendation",
      `briefs/T0_DECISIONS_2026_09_27_STREAM2.md`): AM-6 selector clause ADOPTED; AM-7 C3 checker path
      corrected; T3 cert wording re-emitted (values unchanged); `python-flint` 0.9.0 installed; **WP-S2-CERT
      step 1 LANDED**: `checkers/check_certified_monodromy_L2.py` certifies (Arb balls, majorant tails) that
      every Sym² monodromy entry recognised by `check_U1_lattice.py` stage 2 is the unique rational of
      denominator ≤ 10⁴ in its enclosure — s7 and s10 both (s10 stays ADVISORY; lattice cert DRAFT).**
      **Step 2 also landed:** the certified matrices run through the exact stage 3 reproduce the lattice
      certificate 9/9 fields (s7 LIVE v5; s10 DRAFT v4) — chain closed; tampered matrix refused (N8).
      **T0 D12′ (same day): Stream 3 takes the laboratory approach** — the Fable review's E1–E4 enter
      via the pin protocol (PREDICTION v2 amendment, Arm V/P/0, kill rule, tag before data; calibration
      arm E1 first); D11′-3 "parked" is struck. Nothing in it is evidence for any K3 claim. Delivery notes
      placed untracked in the S1 and S3 repos; mirrors re-pin to the post-merge `K3_CRITERIA.md` hash
      (the §5 C2 cells now carry the certified-monodromy note).
- [x] **`C2_cooper_s7_v6` — ACCEPTED by T0 2026-09-27 (D10′), LIVE.** v5 content, provenance only:
      stage-2 matrices CERTIFIED (`CERTIFIED_MONODROMY_L2_cooper_s7.json`) instead of recognised at
      1e−35; derived block identical to v5 (asserted at promotion). v5 retained for audit and as the
      pinned input of earlier certificates; v3 still the rank source. PR #55 merged on the same ruling;
      S1/S3 informed. Record: `briefs/T0_DECISIONS_2026_09_27_STREAM2.md` D10′.
- [x] **Two CM rows lifted to Tier A (lattice half) — DONE 2026-09-27, producer ≠ verifier honoured.**
      Stream 2 re-ran the gates itself in Stream 1's worktree (`fd76a49`, file sha `95c023ef…`): G1 exit
      0 (3723 jobs), G2 exit 0, G3 exit 1 = 395 audited / 3 failing, all three the registered-axiom
      theorems and none in §3b, G4 exit 0, `#print axioms` on the nine §3b declarations = standard
      axioms only. Then `checkers/check_lean_attestations_rankjump.py` recomputed from the certificate
      rows that each attested statement is about that row (vector, orthogonality, Gram, reduced form,
      frame det, det identity) and emitted the OVERLAY `CM_POINTS_RHO20_LATTICE_TIER.json`: s7 z=1/27
      (D −28) and z=−1 (D −7) → `lattice_tier: A`; `CM_POINTS_RHO20.json` itself unchanged. Attestation
      data: `refs/lean_attestations_rankjump_2026_09_27.json` (manifested). 9 controls. Still Tier B:
      z-recognition; Tier L: v^⊥ = T_X.
- [x] **All six locus rows at Tier A (lattice half) — DONE 2026-09-27.** LeanMaster's
      `DualScaleDyons/RankJump.lean` (`73f6fb1`, file sha `d9c3e5f3…`) re-gated by Stream 2 in their
      worktree with `LEAN_PROJECT_ROOT` set: G1 0 (8805 jobs), G2 0, **G3 0 = 184 audited / 0 failing, 18
      of them RankJump**, G4 0, `#print axioms` standard on all eleven declarations. (A first run without
      `LEAN_PROJECT_ROOT` audited the main checkout — 166 theorems, no RankJump — and was discarded; the
      trap the `lean-proof-gate` skill names.) Overlay `CM_POINTS_RHO20_LATTICE_TIER.json` v1.1.0: the two
      s7 (−2)-rows carry **two independent files** (Stream 1 + LeanMaster); s7 z=∞ (A₂) and the three s10
      rows carry LeanMaster alone (s10 ADVISORY, D6′ untouched). LeanMaster's two audit questions answered
      in the overlay per row: Q1 the unimodular change from the certificate's kernel basis to the attested
      reduced basis is computed and recorded; Q2 `det_T_X` is now certified from the kernel-checked Gram
      (4ac − b²) and compared with the certificate's formula value. 14 controls. Still not proved in either
      file: the general index step; v^⊥ = T_X stays Tier L; z stays Tier B.
- [x] **Stream 1's K3-directions receipt (2026-09-27) — received, hashes agree; one correction taken:**
      my "(0,0) [X₄]" label was wrong (X₄ = (α,β) = (1,0); (0,0) = E_ω × E_i, ρ = 18) — corrected in
      their note; their (1,0) row closes to 20 once the two order-2 places at t = ±1 are read as such.
- [x] **T0: candidate register (t103) — closed by D11′-2 and Stream 1's receipt §5** (row stays
      DROPPED on the citation ground only; Stream 1 holds no source). Original item: S1
      `K3_CRITERIA.md` listed t103 as dropped, although
      E-014 found no veto (S1 `briefs/T0_FLAG_K3_CRITERIA_T103_STALE_2026_08_01.md`, unanswered).

## ⛔ Do NOT do these

- **Do not run `pipelines/D3_batch_runner_phase2.py`.** Disabled 2026-07-26; it raises. It
  fabricates χ² via `np.random.chi2`, tests operator error against noise it cannot fail, and
  defaults to the retracted ρ=4/T=18. Re-enable only by wiring
  `empirical_crucible/s2_1_singular_locus_observable.py` **and** shipping negative controls.
- **Do not retry the Néron–Severi route to ρ.** It corroborates only the easy bound (ρ ≤ 19); the
  ambient models genuinely give ρ ≥ 1 (s7) / ρ ≥ 2 (s10). See `check_neron_severi_ambient.py`.
- **Do not chase Stienstra–Beukers 1985.** Paywalled, unfetched, and **off the critical path** —
  Zarhin 1983 Thm 1.6(a) closed the ρ/T step instead.
- **Do not edit a pinned document unilaterally.** `PREDICTION.md` v1.1 was re-pinned under its
  *own* protocol (§6 "populated only by the completed S3-00 derivation, in a new commit").

---

## Standing rules (earned the hard way — E-007, E-010, E-012)

1. **A test that cannot fail is not a test.** Every checker emitting a headline number ships a
   negative control asserting a known-negative case FAILS. This has found a real bug every time.
2. **Read the source, not the certificate.** All three fabrications produced well-formed,
   correctly tiered, internally consistent certificates. The tell was always in the code.
3. **Retractions must be in-band.** A retraction only in prose is invisible to a script — and is
   where E-010's fabrication got its target value.
4. **Verify a directive's artifacts before executing it.** Five occurrences to date of directives
   naming files that do not exist.
5. **Numbers are computed, never typed.** ρ is derived at runtime as `b₂ − rank_V` from the step-A
   certificate; break that certificate and the number moves or the checker refuses.

## Regression — all green as of `v0.3.7` (T3 lines added 2026-09-21)

```bash
python3 checkers/test_refs_self_regenerate.py            # 11/11 entries, both encodings agree
python3 checkers/test_L3_irreducible_minimal_controls.py # 16 assertions incl. negative controls
python3 checkers/check_L3_irreducible_minimal.py         # L3 irreducible => rank V = 3
python3 checkers/check_C2_transcendental_rank.py         # rho = 19, T = 3  [tier B]
python3 checkers/check_s7_partner_integrality_modular.py # s7 integrality mechanism
python3 checkers/check_neron_severi_ambient.py           # rho <= 19, second route
python3 checkers/check_s7_hauptmodul_gamma07plus.py      # A279618 is Gamma_0(7)+ Hauptmodul
python3 checkers/test_gate_e_verdict_controls.py         # Gate E script fails closed (7 controls)
python3 scripts/check_tier_language.py                   # wrapper — HONORS file args (E-016);
                                                         # scans root + briefs by default
python3 checkers/check_U1_lattice.py                     # U1 lattice pipeline (s7), derived values
python3 checkers/test_U1_controls.py                     # U1 negative controls (incl. s10 level control)
python3 checkers/check_U1_witness_serialization.py --all # P witness self-check; s7 v5 + s10 v4_DRAFT PASS, v3/v4 -> WITNESS_ABSENT
python3 checkers/test_U1_witness_serialization_controls.py # 10 controls (tampered P/gram_after, s10 tamper + cross-family -> FAIL)
python3 checkers/independent_rederivation_C2_s10_v4.py   # s10 DRAFT T = U+<20>, independent code path (23 checks)
python3 checkers/independent_rederivation_C2_s10_v4_controls.py # 10 discriminating controls
python3 checkers/test_C1_mirror_integrality_controls.py  # 7 controls (A279618 match; A112019 real known-bad + tamper/swap/corrupt/round-trip must fail)
python3 checkers/check_C1_mirror_integrality.py --order 30 # all order-3 refs entries PASS(30); certs are at order 60 (--emit)
python3 checkers/check_s10_hauptmodul_gamma010star.py   # s10 z(q) Hauptmodul for Gamma_0(10)*; controls N1-N4
python3 checkers/check_T3_level_consistency.py          # T3 two-leg agreement on n; s7 AGREE(7), s10 AGREE(10)+flags
python3 checkers/test_T3_level_consistency_controls.py  # 25 controls (4 REAL order-3 known-bads; Mobius-clause R4; conflation S1a/S1b)
python3 checkers/test_CM_points_rho20_controls.py        # 46 controls: CM/rho=20 point map (s7 loci = CM points D -28,-7,-3)
python3 checkers/check_A2_membership.py                  # A2 in s7 family (z=inf), NOT in s10 (all-v congruence); ~30 s
python3 checkers/test_A2_membership_controls.py          # 35 controls
python3 checkers/test_nodality_explicit_models_controls.py   # 20 controls: explicit Laurent models, PASS(10); z=-1 literal clause FAILS on model (recorded)
python3 checkers/check_atkin_lehner_vs_disc_form.py          # W(n) -> O(q_A) isomorphism, PASS(30); s10 advisory
python3 checkers/test_atkin_lehner_vs_disc_form_controls.py  # 33 controls
python3 checkers/check_elliptic_points_are_CM.py             # stabilizer orders [2,2,3] / [2,2,4]; agreement FORCED
python3 checkers/test_elliptic_points_are_CM_controls.py     # 13 controls
python3 checkers/check_partner_global_boundedness.py         # s10/s18 partner c=2, s7 c=1, PASS(160)
python3 checkers/test_partner_global_boundedness_controls.py # 16 controls
python3 checkers/check_CM_completeness_classnumber.py        # P2 table complete where it speaks (30/30 D)
python3 checkers/test_CM_completeness_classnumber_controls.py # 16 controls
python3 checkers/test_render_status_table_controls.py        # 20 controls (retracted/missing/wrong-candidate sources refuse)
python3 scripts/render_status_table.py --check               # K3_CRITERIA sec. 5 matches the certificates
python3 checkers/check_external_review_fable_2026_09_21.py   # external review audit: 12 clauses vs certificates, exact class numbers / Gauss-Bonnet
python3 checkers/test_external_review_fable_controls.py      # 22 controls (each clause can go NOT_CONFIRMED; exact helpers reject wrong values)
python3 checkers/check_certified_monodromy_L2.py --family cooper_s7   # ~50 s: CERTIFIED stage-2 monodromy (Arb balls); needs python-flint
python3 checkers/check_certified_monodromy_L2.py --family cooper_s10  # ~30 s: same, s10 (ADVISORY family; this certifies the numerics only)
python3 checkers/test_certified_monodromy_L2_controls.py     # ~70 s: scrambled operator refused; every rigorous helper is a real bound
python3 checkers/check_inose_model_M7.py                      # ~15 s: explicit M_7 Inose/CDLW model over z; sigma^2-4pi zeros = W_7 fixed points + CM points
python3 checkers/test_inose_model_M7_controls.py              # 7 controls (scrambled z refused; level 5 does not fit; wrong pole order fails)
python3 checkers/check_inose_fibration_multiplicities.py      # ~10 s: KS J9 equation (transcription verified) -> Inose K3; orders {10,10,2,1,1} at both loci
python3 checkers/test_inose_fibration_multiplicities_controls.py # 7 controls (transcription errors refused; exceptional set discriminating)
python3 checkers/check_lean_attestations_rankjump.py --verify-source-files # overlay lattice_tier from kernel statements; A7 skipped if the producer worktree is absent
python3 checkers/test_lean_attestations_rankjump_controls.py # 9 controls (tampered Gram/basis/vector/axioms/det/sha -> tier B)
# slow (~70 s): python3 checkers/check_nodality_explicit_models.py   (Singular optional second CAS)
# slow (~2.5 min), run before release: python3 checkers/check_CM_points_rho20.py
```

## The Tier A result, for the record

Publishable on its own merits, independent of any dark-sector claim:

- `L₃ = Sym²(L₂)` — kernel-proven in Lean 4 (Stream 1)
- **L₃ irreducible ⇒ the minimal-order Picard–Fuchs operator** — exact in ℚ, both operators.
  Not dihedral (double indicial root at 0 ⇒ log ⇒ nontrivial unipotent ∉ N(T)); L₂ irreducible
  by a denominator obstruction (residues ∈ ½ℤ vs ∞-exponents {1/3,2/3} and {3/8,5/8}).
- **ρ = 19, T = 3** — via Zarhin 1983 Thm 1.6(a) + Huybrechts 3.2.7/3.3.1, both fetched and read
  (Zarhin is a scan; read as rendered page images).
- **s7-partner integrality mechanism** — `X₇ = η₁³η₇³/z₇³` is a *normalized* integral uniformizer;
  normalization is the load-bearing property, not "η-quotients are integral".
- Exact Riemann schemes, Fuchs Σ = 6, MUM at 0, W(L₃) = W(L₂)³; A–vS explicit projective K3 models.
