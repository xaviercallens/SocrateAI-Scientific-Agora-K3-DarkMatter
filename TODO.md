# ✅ TODO — restart here

**Last updated:** 2026-09-29 (D14′–D18′ taken on T0's behalf under explicit delegation — `briefs/T0_DECISIONS_2026_09_29_STREAM2_DELEGATED.md`: no Kodaira labels for the explicit model; `C2_cooper_s10_v5.json` LIVE; CI red-run diagnosis + fixes + standing rule 6; Stream 3 restarted by notice §9; LeanMaster closed for this project, MCP server kept. Paper: PR #70. Orientation block below dates from 2026-07-26) · **Release:** `v0.3.16-tw2-steps-0-2bi` (D23′; WP-TW2 steps 0, 1, 2a, 2b-i: P̄·Ō = n − 2 generically; ρ = 20 loci resolved — the AM-8 K3 has an A₂ root fibre and no section; √−7 at z = 1/27 exhibited over Q; tagged only on a green post-merge run, rule 6) · **Previous TODO:** commit history

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
      **SUPERSEDED 2026-09-29 (D15′, on T0's behalf under explicit delegation):**
      `C2_cooper_s10_v5.json` is LIVE, value-identical to v4_DRAFT; re-derivation 23/23 and witness
      check re-run before promotion. Record: `briefs/T0_DECISIONS_2026_09_29_STREAM2_DELEGATED.md`.
- [x] **D19′–D22′ taken on T0's behalf (2026-10-07, delegation "take decision on my behalf and continue";
      `briefs/T0_DECISIONS_2026_10_07_STREAM2_DELEGATED.md`).** D19′ WP-TW0 R-a: ledger item 6 amended (ℓ := χ(O_K3)
      = 2 for the Weierstrass model; family-level degree 2/3), WP-TW0 CLOSED. D20′ WP-TW1 verified (re-run +
      line-by-line read; ALL CONTROLS PASSED) and LIVE as a necessary-condition screen — P³ FAILS, P¹×P² and the
      scroll family PASS; certificate `status` fields still say DRAFT (classifier refused the edit; brief note is
      the in-band record). **WP-TW2 opened, step 0 done:** `checkers/check_TW2_height_condition.py` (+9 controls,
      `TW2_HEIGHT_CONDITION.json`): with two E8-root fibres and ρ = 19, Shioda–Tate forces MW rank 1 and
      NS = M_n forces h(P) = 2n, so the generator meets the zero section with **P̄·Ō = n − 2 (= 5 for s7)**;
      Schütt–Shioda fetched, read, pinned. D21′ E2 HELD unpinned (Home PRs #5/#6 merged). D22′ phantom Lean
      workflows RETIRED on record; deletion is T0's (classifier). **WP-TW2 step 1 DONE (same day):** Kumar–Kuwata arXiv:1409.2931 Prop. 3.1 (Shioda) and
      Shioda MPIM 2007-137, fetched and read, give MWL(F(1)) ≅ Hom(E1,E2)⟨2⟩ — height 2·deg φ — so a 7-isogeny
      yields h = 14, P̄·Ō = 5: the step-0 number from an independent route. KK Prop. 3.2 is the explicit
      isogeny→section recipe (step 2 design, not executed; Prop. 3.1 excludes E1 ≅ E2, so use the class-number-1
      loci z = −1, 1/27, not the A₂ point). Brief: `briefs/WP_TW2_HEIGHT_CONDITION_STEPS_0_1_2026_10_07.md`.
      **WP-TW2 step 2a DONE (D23′, same day):** `checkers/check_TW2_rho20_loci.py` (+7 controls, `TW2_RHO20_LOCI.json`) —
      exact bookkeeping at the three ρ = 20 loci (E1 ≅ E2 at all three, so Prop. 3.1 is off): z = 1/27 (D −28): A₁
      root, MW rank 1, h = 14, P̄·Ō = 5; z = −1 (D −7): A₁ root, MW rank 1, h = 7/2, P̄·Ō = 0 via the non-identity
      component; **z = ∞ (AM-8 selected, D −3): A₂ root, MW rank 0 — no section at all.** The TW2 constraint for the
      selected K3 is an order-4 discriminant root with A₂ root lattice, not a height-14 section.
      **WP-TW2 step 2b-i DONE (same day):** `checkers/check_TW2_sqrt_m7_endomorphism.py` (+7 controls,
      `TW2_SQRT_M7_ENDOMORPHISM.json`) — the degree-7 endomorphism √−7 of the z = 1/27 curve (j read from the
      fibration certificate; model y² = x³ − 1551893875x + 23529814932750) exhibited over Q by Vélu from the unique
      rational cubic factor of ψ₇; codomain ≅ E via c² = −1/7; **φ∘φ = [−7] proved exactly** (60/60 rational points,
      degree bound 49). Sign-slip in c² caught live → negative control.
      **D26′ (2026-10-08): `SELECTED_K3_DOSSIER.json`** (`check_selected_k3_dossier.py`, +7 controls) — one citable record of both
      AM-8 picks, assembled only by cross-checking seven certificates (selector, CM row, lattice tier, A₂ membership,
      completeness, explicit model, TW2 NS structure); refuses on any disagreement; ranks nothing. Observation: the CM
      certificate's s7 lattice pointer is still `C2_cooper_s7_v5.json` (v6 is value-identical, provenance-only).
      **Regression-block repair (same day):** the TW2 step-2a, step-2b-i and dossier checkers had never been added to the
      block (earlier guarded inserts silently skipped); now present, so Gate B covers them.
      **2026-10-08:** step 2b-i completed as a morphism of curves — exact y-identity, deg φ_y(x₁)=t³ equation = 9 = (3d−3)/2
      (KK Prop 3.2(i)), and a dated precision correction: the x-identity proves φ∘φ=±[7]; the sign −7 is fixed by D=−28 < 0
      (Tier B). Brief §7.
      **K3 IDENTIFIED (2026-10-08, T0: "identify the K3"):** `SELECTED_K3_IDENTIFICATION.json`, brief `SELECTED_K3_IDENTIFICATION_2026_10_08.md`.
      s7 pick (z=∞, T=[[2,1],[1,2]]) = **X₃, Vinberg's most algebraic K3**; s10 pick (T=⟨2⟩⊕⟨2⟩) = **X₄**; s7 z=−1 = X₇; z=1/27 = the
      T=⟨2⟩⊕⟨14⟩ surface (2 classes at det 28). Source: Takatsu arXiv:1903.03054 (table + uniqueness parsed from the pinned text; author
      mis-attributed by a search snippet, corrected from the header). Determinants 3,4 = the two smallest attainable (computed). Tier B.
      **D22′ EXECUTED (2026-10-08): phantom Lean workflows removed from `main` by T0, commit `684e382`.**
      **D27′ (2026-10-08): numeric evaluation with Dark Home** — guidance brief `STREAM2_TO_STREAM3_NUMERIC_EVALUATION_GUIDANCE_2026_10_08.md`;
      Home PR #9: E1b filed (2 in-band revisions), mirror 17 files, invariants 604 passed (`iminuit` missing on host). WP-E6 v2 Phase 0
      needs one T0 sentence — NOT signed off by Stream 2.
      **D28′ (2026-10-08): T0 sign-off, read as WP-E6 v2 Phase 0 ONLY — executed in Home** (decisive-and-open 221 → 182 text-only / 152 with
      figure reads; P0 does not fire; DESI DR1 secondary trigger NO). Phases 1–4, pin, §8(a)/Q1–Q5 NOT authorized. WP-TW3 stays unopened
      (no T0 text specifies twist data over the threefold base). Record: `briefs/T0_DECISIONS_2026_10_07_STREAM2_DELEGATED.md` D28′.
      **PAPERS (2026-10-08, T0: "publish the different papers"):** new `papers/stream2_k3_identification_twisted_route_2026_10_08.pdf`
      (X₃/X₄, K3×T² Shioda–Inose reading + T3, TW0/TW1/TW2; all tables from certificates); 09-29 paper rebuilt with dated item 7
      (its 10-07 build still printed 3 ADVISORY tags; renderer now reads `advisory_family`, fibration orders read not typed).
      Stream 3 note in Home `papers/stream3_status_note_2026_10_08.pdf`. Other streams' papers NOT edited; FYI brief
      `briefs/STREAM2_TO_ALL_STREAMS_PAPERS_2026_10_08.md`. Nothing submitted externally.
      **D29′ (2026-10-08): K3×T² = Reading S (Shioda–Inose pairing), ledger item 12.** `checkers/check_K3xT2_reading_S.py` →
      `K3xT2_READING_S.json`: T(E×E′) for a cyclic n-isogeny computed in ∧²Z⁴ is isometric to the certified T for n = 7 and n = 10,
      with NS saturated and of signature (1,2), so Morrison 1984 is no longer needed. At the three s7 ρ=20 points, T(E×E) for
      the computed CM order equals the certified row (forced; ledger 8). 9 controls. Paper section added (dated item 8). Open:
      proposal decisions 2–4 (T3 hard gate, K3_CRITERIA edit, scoring).
      **ALL THREE STREAMS PUBLISHED (2026-10-08, T0: "publish the stream 1, stream 2 and stream 3 results as tex and pdf"):**
      Stream 1 paper revision (dated addendum §12, v4 text unchanged; mirror re-pinned; release gates re-run by Stream 2, red
      at gate 0 before the re-pin) → S1 PR #4 @ 8dbf438, tag `v0.27-paper-addendum-2026-10-08` only on a green gate run;
      Stream 2 v0.3.19; Stream 3 note (Home v5.13.0). No Zenodo deposit (T0's step).
      **WP-TW3 OPENED (D32′, 2026-10-10, on T0's "implement on my behalf … WP-TW3's twist data"):** B₃ = P¹×P², E8 divisors
      {0}×P², {∞}×P²; f = s⁴t⁴f′, g = s⁵t⁵g′, f′ ∈ O(0,12), g′ ∈ O(2,18); `checkers/check_TW3_twist_data_degrees.py` →
      `TW3_TWIST_DATA_DEGREES.json`. Next gate **TW3-G2** = a rational map z: P² ⇢ P¹ with α³ = π(z), β² = π−σ+1: necessary
      condition e ≤ 3 (12e ≤ deg ac = 36), explicit exact constructions for e = 1, 2, 3. Smoothness/minimality (G3) NOT done;
      no tadpole/χ (F5b). Brief `WP_TW3_OPENING_2026_10_10.md`.
      **WP-TW2 step 2b-ii DONE (2026-10-10):** `checkers/check_TW2_section_descent.py` → `TW2_SECTION_DESCENT.json`, 14 controls.
      Kumar–Kuwata Prop. 3.2 executed exactly at 52 specializations; X′(t) = N/D², deg N = 14, D = (t+1)·(irreducible quartic),
      unique 26-unknown fit (44 points) agreeing at 8 held-out points; **P̄·Ō = 5, contr = 0 (P meets O inside the A₁ fibre),
      h = 14**, equal to step 0, step 2a, KK's 2d and the fibration orders {10,10,2,1,1}, all read from their certificates; section
      defined over Q on its branch. Scoping brief `STREAM2_K3xT2_DUAL_SCALE_SCOPING_2026_10_10.md`: the physical K3×T² dual-scale
      theory is Tier C and cannot be validated; no tr G + tr G⁻¹ on CM tori (not GL(2,Z)-invariant, needs a typed Kähler modulus,
      D29′/D31′ bar it). Stream 1 request addended (kernel check of the Reading S lattice; statement must carry set equality).
      **Released** `v0.3.20-am9-t3-hard-gate` (run 37844601329). **Next:** WP-TW2 at z = −1 (P̄·Ō = 0; 2-isogeny, own Vélu
      step); WP-TW3 needs T0 text (unopened).
- [x] **WP-TW0 RE-EXAMINED (2026-10-07) — F6 disclosure filed, T0 escalation, ledger NOT edited.**
      `checkers/check_TW0_hodge_degree_orbifold.py` (+9 controls) recomputes the Hodge-bundle degree in
      exponent language from the Tier-A operator tuple: L₂ has FOUR singular points (the 07-29 brief listed
      three — z = 0, MUM, was omitted); the Γ₀(7)+ signature (0; 2,2,3; 1) is derived two independent ways
      (exponents; group theory with class numbers counted) and they agree; orbifold degrees deg ω = 1/3,
      deg ω² = 2/3; Deligne-extension integer degrees 0 / 1 by residue convention — **never 2 at family
      level**. ℓ = 2 is reproduced only as χ(O_K3) = 2 (Noether, deg Δ = 24): a fact about any elliptic K3
      with section, not about the family. The 07-29 formula "(Σ exponents)/order" is a Fuchs-relation
      tautology (returns 1 for every 4-point order-2 operator; control N4). Record:
      `briefs/WP_TW0_HODGE_DEGREE_REEXAMINATION_2026_10_07.md`; certificate `TW0_HODGE_DEGREE_ORBIFOLD.json`.
      **T0 to rule:** which reading WP-TW1 (deg Δ = 48 on P³) needs; ledger item 6's wording.
- [x] **v5 chain RE-EMITTED (2026-10-07).** `T3.CANDIDATES['cooper_s10']` → `C2_cooper_s10_v5.json` (LIVE);
      re-emitted in dependency order: `CM_POINTS_RHO20` → `A2_MEMBERSHIP` (+ brief) → `CM_POINTS_RHO20_LATTICE_TIER`
      → `C6_SELECTOR_COMPARISON` → `C6_SELECTED_CANDIDATE`; independently `ATKIN_LEHNER_DISC_FORM` (+ brief),
      `HAUPTMODUL_S10_GAMMA010STAR`, `T3_LEVEL_CONSISTENCY`. Values unchanged (6/6 rows Tier A; AM-8 text still
      verifies; 46/46, 25/25, 33/33 controls). Three checkers had `advisory` **hardcoded** as `fam == "cooper_s10"`
      (C6 comparison, C6 adopted) or read from the static attestation record (lean attestations) — now read from
      the CM certificate's family flag; one control that encoded the pre-D15′ state replaced by a mirror check +
      a tamper control. §5 regenerated: K-s10 C6 cell no longer shows `LATTICE_CERT_DRAFT`. **Stream 3 must
      re-mirror** these 8 certificates and re-pin `K3_CRITERIA.md` (their drift test asserts "every s10 row is
      advisory" and will need the same update).
- [x] **🟡 Re-emit the v5 chain (mechanical, any agent) — DONE above.** Original text: certificates emitted while v4_DRAFT was
      the lattice source still carry `LATTICE_CERT_DRAFT`/"ADVISORY" provenance wording (values
      unaffected). Order and list in the D15′ brief; also the four checkers that print the wording.
      Until done, §5's K-s10 C6 cell shows the flag next to a LIVE C2 cell — dated, not hidden.
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
      level of orders). `INOSE_FIBRATION_MULTIPLICITIES.json`. **RULED 2026-09-29 (D14′, on T0's
      behalf): no Kodaira labels for the explicit model either — ledger item 10. GE-10 CLOSED at the
      level of orders.** Record: `briefs/T0_DECISIONS_2026_09_29_STREAM2_DELEGATED.md`.
- [x] **CI Gate — GREEN 2026-09-29** after the D16′ fixes: PR run `36523846615`, post-merge run
      `36524218006` on `main` `2894e78`, Gates A–D + Merge Gate all success (first green runs since #65).
      Recorded in the D16′ brief addendum. Diagnosis of the red runs (Gate A `packagesDir`; Gate B missing
      `python-flint`/`pytest`, sympy pure-Python LLL assertion, Stream 1 repo absent) and the fixes: same brief.
- [ ] **🔴 T0: retire (or repair) three legacy Lean workflows that cannot pass** — `lean4-compile.yml`,
      `lean4-ci.yml`, `part4-proofs.yml` build nonexistent `Agora.PartIV.*` modules, `grep "error"` matches
      Lake's own warning text, and every `sorry` string in the tree counts as a defect; not merge gates, but
      red on every trigger (runs `36523846606`, `36523846604`). Evidence and proposal: D16′ brief addendum.
      Stream 2 did not remove them (workflow removal reserved to T0).
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
- [x] **AM-8 (T0 D13′, 2026-09-28): C6 selector ADOPTED — minimal `|disc T|` per family, chosen by T0
      via `AskUserQuestion` from two computed alternatives.** Narrows D7′'s "no minimum-|D| rule" to
      cross-family comparison only (the sentence right after it — "A₂ ∈ s7, A₂ ∉ s10, is a lattice
      fact, not a preference" — is unchanged). Selected: **cooper_s7 → T = A₂ (D=−3), z=∞**;
      **cooper_s10 (ADVISORY) → T = ⟨2⟩⊕⟨2⟩ (D=−4), z=∞** — both verified unique on the modular curve
      (`CM_COMPLETENESS.json` point count, not class number). Rejected alternative (minimal `|v²|`) is
      not unique for s7 (ties at the −2 floor between D=−7 and D=−28) and stays on record.
      `checkers/check_C6_selector_comparison.py` (13 controls, comparison) +
      `checkers/check_C6_selector_adopted.py` (5 controls, verifies the criteria prose against
      recomputation) → `C6_SELECTOR_COMPARISON.json`, `C6_SELECTED_CANDIDATE.json`. Record:
      `briefs/T0_DECISIONS_2026_09_28_STREAM2.md`, `briefs/STREAM2_AM8_SELECTOR_COMPARISON_2026_09_28.md`.
      Does not rank the families, does not promote s10, does not read physically (ledger item 4).
- [x] **The two AM-8-selected rows (both z=∞) lattice-half kernel-checked, DOUBLE-SOURCED —
      DONE 2026-09-28.** Stream 1 added `Agora/Geometry/MnLattice.lean` §3c (`2f665dd`, sha
      `b4d0adcb…`; merged `--no-ff` into their `main` as `4bab4b6`, `v0.24-am8-rows-lattice-half`) for
      exactly the two rows AM-8 selected — same pattern as §3b, independently derived from
      LeanMaster's own `s7_z_infinity`/`s10_z_infinity` (statement-level match confirmed both ways).
      Re-gated by Stream 2 in Stream 1's worktree: G1 exit 0 (3723 jobs), G2 exit 0, G3 exit 1 = 421
      audited / 3 failing (same three registered axioms as §3b, none new), G4 exit 0, `#print axioms`
      standard on all sixteen declarations — matches Stream 1's own report exactly. Independently
      recomputed the lattice arithmetic before trusting either report (norm, orthogonality, Gram,
      reduction, frame det, determinant identity — all matched).
      **Bug found and fixed while extending the attestation file:** `check_lean_attestations_rankjump.py`
      resolved one worktree path per repo, so a second gate record on a *different* worktree for the
      same repo always failed its file-hash check (A7) silently under `--verify-source-files` — fixed
      to resolve the worktree from each gate record's own `branch` field (`source_root()`). A second,
      unrelated bug in `test_lean_attestations_rankjump_controls.py`'s N8 control (matched a row by
      vector coordinates alone, which collide across candidates — `(1,-1,0)` is a row of *both*
      families) was also caught and fixed. `refs/lean_attestations_rankjump_2026_09_27.json` now has
      3 gate records / 10 attestations; overlay `CM_POINTS_RHO20_LATTICE_TIER.json` re-emitted: **3 of
      the 6 rows are now double-sourced** (both s7 (−2)-walls, and now both z=∞ points too). 16
      controls (was 14; N8 fixed + N8b added). Not proved by either file: the index step, `v^⊥ = T_X`
      (Tier L), `z` (Tier B). No promotion of s10; no ranking; no physical reading.
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

**CI record (rule 6):** post-merge runs on main — `2cab124` run 37673233682 GREEN; `bd576c1` run 37674696716 RED (Gate B: paper table fragment stale after the v5-chain re-emission — fixed by regenerating `papers/tables/`, paper correction item 6); `413220d` run 37679794858 RED for the same cause. Fix `0adb074` run 37681111136 GREEN.

## Regression — all green as of `v0.3.14-delegated-rulings-ci-green` (2026-09-29; all 40
`checkers/test_*.py` suites green locally with `STREAM1_ROOT` set, and Gate B green in CI run `36524218006`;
the former worktree-only false failures are fixed — see note below the block)

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
python3 checkers/test_lean_attestations_rankjump_controls.py # 16 controls (tampered Gram/basis/vector/axioms/det/sha/kernel-basis/det_T_X -> tier B; double-sourcing checked)
python3 checkers/check_C6_selector_comparison.py              # C6 selector comparison record (SEL-D vs SEL-N), not a gate
python3 checkers/test_C6_selector_comparison_controls.py      # 13 controls
python3 checkers/check_C6_selector_adopted.py                 # verifies AM-8's K3_CRITERIA.md prose against recomputation
python3 checkers/test_C6_selector_adopted_controls.py         # 5 controls
python3 scripts/render_paper_tables.py --check                # papers/tables/*.tex match the certificates (papers 2026-09-29 and 2026-10-08)
python3 checkers/test_render_paper_tables_controls.py         # 18 checks (P0 x9; tampered cert changes each table incl. fibration orders + advisory flag; stale fails --check)
python3 scripts/check_tier_language.py papers/stream2_selection_geometry_2026_09_29.tex  # paper prose: 0 violations
python3 scripts/check_tier_language.py papers/stream2_k3_identification_twisted_route_2026_10_08.tex  # paper prose: 0 violations
python3 scripts/check_paper_tier_language.py --selftest       # 7 planted cases (verbs, fibre-type tokens, comments, name allowlist)
python3 scripts/check_paper_tier_language.py papers/stream2_selection_geometry_2026_09_29.tex papers/stream2_k3_identification_twisted_route_2026_10_08.tex  # + no fibre-type token (item 10)
python3 checkers/check_K3xT2_reading_S.py                     # D29': T(ExE') = certified U+<2n> (n=7,10) by witness; s7 rho=20 forced consistency
python3 checkers/test_K3xT2_reading_S_controls.py             # 9 controls (wrong n, non-cyclic, orientation, tampered Gram, wrong order, ...)
python3 checkers/check_TW2_section_descent.py                 # WP-TW2 2b-ii: KK Prop 3.2 section at z=1/27, P.O=5, contr=0, h=14 (exact, over-determined)
python3 checkers/test_TW2_section_descent_controls.py          # 14 controls (tampered Velu, wrong normalization, too few points, 2P, twist, extra pole, ...)
python3 checkers/check_TW3_twist_data_degrees.py                # WP-TW3 opening (D32'): twist data on P^1 x P^2, gate G2 necessary condition, e=1..3 exact
python3 checkers/test_TW3_twist_data_degrees_controls.py        # 19 controls (wrong class, non-disjoint, Tate (5,5), wrong K, tampered a/b/pi, e=4)
python3 checkers/check_TW0_hodge_degree_orbifold.py          # WP-TW0 re-examination: signatures agree; family-level degree != 2 (finding)
python3 checkers/test_TW0_hodge_degree_orbifold_controls.py  # 9 controls (wrong level/operator disagree; irregular point refused; 07-29 formula non-discriminating)
python3 checkers/check_TW1_two_e8_feasibility.py             # WP-TW1 LIVE (D20'): P3 FAIL, P1xP2 / scroll PASS (necessary-condition screen)
python3 checkers/test_TW1_two_e8_feasibility_controls.py      # 5 controls
python3 checkers/check_TW2_height_condition.py               # WP-TW2 step 0: P.O = n - 2 (5 for s7); two order-10 roots per locus cross-checked
python3 checkers/test_TW2_height_condition_controls.py        # 9 controls
python3 checkers/check_TW2_rho20_loci.py                    # WP-TW2 step 2a: rho=20 loci resolve uniquely (A1/A1/A2; MW 1/1/0), model-confirmed mod m_J
python3 checkers/test_TW2_rho20_loci_controls.py             # 9 controls
python3 checkers/check_TW2_sqrt_m7_endomorphism.py          # ~20 s: sqrt(-7) at z=1/27 exhibited over Q; phi o phi = [-7] exact
python3 checkers/test_TW2_sqrt_m7_endomorphism_controls.py   # 12 controls (incl. exact y-identity, degree-9 count, wrong-constant refusals)
python3 checkers/check_selected_k3_dossier.py               # D26: seven certificates agree on the AM-8 picks (fails closed otherwise)
python3 checkers/test_selected_k3_dossier_controls.py        # 7 controls
python3 checkers/check_selected_k3_identification.py         # identifies the AM-8 picks: s7 -> X_3, s10 -> X_4 (table parsed from pinned Takatsu text)
python3 checkers/test_selected_k3_identification_controls.py  # 10 controls
# slow (~70 s): python3 checkers/check_nodality_explicit_models.py   (Singular optional second CAS)
# slow (~2.5 min), run before release: python3 checkers/check_CM_points_rho20.py
```

**Former worktree-only false failure — FIXED 2026-09-29 (D16′):** `check_partner_global_boundedness.py`
and its controls now honour `STREAM1_ROOT`; from a `.claude/worktrees/…` checkout run them as
`STREAM1_ROOT=<repos root>/SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal python3 …`
(16/16 controls verified that way on 2026-09-29). CI checks the public LeanProposal repo out under
`stream1_ro/` and sets the same variable. Without the variable the sibling-directory default still applies.

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

## 📄 K3×T² numerics paper PREPARED 2026-10-10 (T0: "prepare a publication on the numeric results of the K3*T2 theory and simulation")

`papers/stream2_k3t2_numerics_2026_10_10.{tex,pdf}` (7 pp.): the Reading S lattice, T3, the z=1/27 section (exact, over-determined),
and the simulator stream's cross-check ledger **as that stream's own counts** (mirrored in `refs/simulator_k3t2_ledger_counts_v3.json`,
recounted from its rows, pinned to source sha256 and commit 3adda92; NOT re-verified here). Tables from certificates via
`render_paper_tables.py --check` (10 table controls). The physical K3×T² dual-scale theory is stated as NOT validated (Tier C).
**Restructured around the method** on T0's instruction (factual results; the approach reusable to falsify and readapt): six-part
method, a falsification table, and `check_K3xT2_reading_S_level_sweep.py` (levels 1..24: 24/24 diagonal, 0/552 off-diagonal;
6 checks; the runner uses `--n-max 8`). **Merged and released on T0's word** ("merge and release after"). New:
`scripts/extract_simulator_ledger_counts.py` (+8 controls). The paper lint lines in `ci_ledger_regression.sh` include this paper.
