# ✅ TODO — restart here

**Last updated:** 2026-07-26 (evening) · **Release:** `v0.3.4` · **Previous TODO:** commit history

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

- [ ] **T0: does `v0.4.0` still mean "Gate E PASS"?** Gate E in its original form may now be
      unreachable (E-012: no valid D-3 possible; F5b: empirical programme contracted). Either
      redefine v0.4.0 or retire it. **Blocking nothing**, but the reservation is currently
      pointing at an event that may never occur.
- [ ] **T0: amend `EXECUTION_PLAN.md` §S3-00 step 2(b)** — it derives α_D, Λ_D from *Kodaira
      fibre data*, which E-007 retracted and E-008/E-009 showed is category-mismatched (the
      finite loci are order-2 elliptic points, not Kodaira degenerations). Either supply a
      replacement route or formally strike the step. F5b already stands without it.
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
      `C2_cooper_s7_v4_DRAFT.json` emitted (DRAFT — **v3 stays live**; H-M7 upgrade to [B] and
      the S3-00 2(b) re-scope option are now a **T0 decision**, see brief §4).
- [x] **E-016 → Stream 3: told**, with the one-line self-check, in
      `briefs/STREAM2_TO_STREAM3_WPE5_RESPONSE_2026_07_26.md` §5.

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

## Regression — all green as of `v0.3.4`

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
