# ✅ TODO — restart here

**Last updated:** 2026-07-26 (evening) · **Release:** `v0.3.4` · **Previous TODO:** commit history

> ## 30-second orientation
>
> **The mathematics is done. The physics branch closed honestly. Nothing is on fire.**
>
> - **ρ = 19, T = 3 — DERIVED** [tier B], E-011. Independently reproduced by Stream 1.
> - **F5b — no prediction extractable.** Adopted into `PREDICTION.md` **v1.1-PINNED §6**.
>   Pre-registered outcome, **not** a refutation, and **reversible**.
> - **Gate E criteria 1–2 UNSCOREABLE** (no valid empirical run exists). *Not failing.*
> - **Stream 1 parked clean. Stream 2 mathematics complete. Stream 3 running WP-E on Dark Home.**
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
- [ ] **Stream 3: answer the three remaining asks** in
      `briefs/STREAM2_TO_STREAM3_GUIDELINES_2026_07_26.md` — do they hold a real D-3 run or 3D
      field data outside this repo; have they produced Gate E verdicts from the disabled runner;
      the WP-E pre-flight σ(0). (Fourth ask, t103's status, resolved in-repo — see E-014.)

## 🟡 Open — mechanical, any agent can pick up

- [ ] **Correct `stream3_mirror/NO_PREDICTION_BRANCH.md` §2/§5 at source.** It lists ρ=4/T=18 and
      "2× Type II" Kodaira as certified and "not in question" — both retracted by E-007 the day
      after it was written. Corrected *downstream* in `PREDICTION.md` §6, but the mirror copy is
      still stale. **The F5b conclusion is unaffected**; only its supporting table is wrong.
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
- [ ] **Fetch and read Dolgachev 1996 / Doran** (Phase 4 step 2 — see
      `briefs/STREAM2_PHASE4_LATTICE_REFINEMENT_2026_07_26.md`). Promotes H-M7 lattices
      (NS = U⊕E₈²⊕⟨−14⟩, T = U⊕⟨14⟩) from [C] to [B] and changes which S3-00 2(b) decision
      is on the T0 table. The computational leg is done:
      **A279618 is a Γ₀(7)+ Hauptmodul [B]** — deg-2 over the Γ₀(7) coordinate, Möbius refuted,
      Fricke κ=49 computed from the fit (`check_s7_hauptmodul_gamma07plus.py`).
- [ ] **Tell Stream 3 about E-016**: their mirrored `check_tier_language.py` silently ignores
      CLI file arguments on Dark Home too — repo-scan is its only real mode. Fold into the next
      Stream 3 brief.

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
