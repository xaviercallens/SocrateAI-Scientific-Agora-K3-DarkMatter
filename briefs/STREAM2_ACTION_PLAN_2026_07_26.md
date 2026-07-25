# Stream 2 Action Plan — Reconciled (2026-07-26)

**Status:** 🔴 **PHASE 0 FINDING BLOCKS ACTIONS 4–6 OF THE PROPOSED PLAN**
**Author:** Opus 5, executing the Stream 2 plan proposed 2026-07-26
**Authority:** Xavier (T0) — sign-off required on the reconciliation below

---

## Why this plan differs from the one proposed

The proposed plan was written against repo state that has since moved, and two of
its steps would have produced a false confirmation. Before executing anything I
verified the referenced files and re-derived the geometry independently. Results:

### A. Most referenced files do not exist

| Proposed reference | Reality |
|---|---|
| `briefs/STREAM1_TO_STREAM2_HANDOFF_C3B.md` | ✗ — actual file is `briefs/STREAM1_TO_STREAM2_C1C2_HANDOFF.md` |
| `briefs/REVIEW_2026-07-24_STREAM1_HANDOFF_APPROVED.md` | ✗ — actual file is `briefs/APPROVAL_STREAM1_2_T0_SIGNOFF_2026_07_24.md` |
| `STATUS_2026-07-24_PHASE_SETUP_COMPLETE.md` | ✗ does not exist |
| `checkers/adversarial_A5_A6_provenance_hygiene.py` | ✗ does not exist |
| `checkers/check_C1_kodaira_fibers.py` / `check_C2_picard_lattice.py` | ✗ — actual: `check_C1.py` / `check_C2.py`, both **deprecated** by the F6 rectification |
| `scripts/k3_t2_singular_loci.py` | ✗ does not exist |
| `refs/literature_provenance.txt`, `docs/literature/` | ✗ do not exist |
| `ESCALATIONS.md` (E-007) | ✗ does not exist |

### B. Actions 4 and 5 are already done — and were already corrected once

`data/certificates/C1_cooper_s{7,10}_partner_v2.json` and
`C2_cooper_s{7,10}_partner_v2.json` were produced 2026-07-25 by the **F6
rectification** (commit `1dd17cd`), which fixed a dimensional category error
(singular loci had been read off `B(k)` in discrete *index* space instead of
`P₂(z)` in continuous *moduli* space).

The proposed plan's exact singular points **match** the F6-corrected values —
good, that part is right:

| | proposed | v2 certificate | independently recomputed |
|---|---|---|---|
| s7 | z = 1/27, −1 | 1/27, −1 | ✅ 1/27, −1 |
| s10 | z = 1/16, −1/4 | 1/16, −1/4 | ✅ 1/16, −1/4 |

### C. 🔴 The expected outputs are not achievable — they are mutually inconsistent

New checker `checkers/check_C1_kodaira_consistency.py` re-derives the local
exponents from the L₂ operators directly (reading nothing from any certificate).
Result at **all four** singular loci, both partners:

```
exponents = [0, 1/2]      Δ = 1/2      det(monodromy) = −1      in SL₂(ℤ): False
```

Four findings follow:

- **[F1] The fibres are not I₁ and not II.** Kodaira I₁ has *unipotent* monodromy
  (Δ = 0, log case) — we have Δ = 1/2, so **not I₁**. Kodaira II has monodromy of
  order 6 (Δ = 1/6) — so **not II** either.

- **[F2] No Kodaira type can be read off these exponents at all.** Exponents
  [0, 1/2] give monodromy eigenvalues {+1, −1}, determinant **−1**. Every Kodaira
  fibre monodromy lies in SL₂(ℤ) and so has determinant **+1**. This is not an
  elliptic-fibration monodromy.

- **[F3] The proposed plan is internally inconsistent.** It expects
  `Σ = [I₁, I₁]` *and* `ρ = 4`. Shioda–Tate gives
  ρ = 2 + Σ(mᵥ − 1) + rank MW. Kodaira I₁ has mᵥ = 1, so [I₁, I₁] with rank MW = 0
  yields **ρ = 2, not 4**. The same contradiction sits inside the existing v2
  certificates, which label the fibres "II (tentative)" (m = 1) while using m = 2
  to reach ρ = 4.

- **[F4] Probable root cause.** Half-integer exponents are the expected signature
  of a symmetric-square **root**. L₂ was extracted as the Sym² root of L₃, and
  that extraction introduces √ branch points. So L₂'s singular points are likely
  **not** the elliptic fibration's singular fibres, and reading Kodaira types off
  L₂'s exponents is methodologically unsound regardless of which label you pick.

**Executing Actions 4–5 as proposed would have "confirmed" pre-declared values
that cannot be simultaneously true.** Given this project's documented history
(`c3b_refs_integrity_2026_07_20`, `ws11_1177_synthetic_finding_2026_07_20`), a plan
that states *"Expected output (no surprises)"* and then computes toward it is the
exact failure mode already encountered twice. Flagging rather than executing.

### D. 🔴 Downstream consequence — time-sensitive

**Stream 3's running D-3 batch uses ρ = 4, T = 18 as a lattice prior**
(`--lattice-prior data/certificates/C2_cooper_s7_partner.json`), and Gate E is
scheduled for **2026-07-27 EOD**. If ρ = 4 is unsupported, so is that prior, and
Gate E criterion 1 ("lattice structure validated") cannot be scored as PASS on
current evidence. **This needs a T0 decision before Gate E, not after.**

Note the discriminant = −3 figure in the proposed plan appears only in the
**superseded v1** certificates, which the v2 files explicitly mark
*"F6 retracted: fabricated from incorrect C1."* It should not be carried forward.

---

## Reconciled Plan

### Phase 0 — Reconciliation ✅ **DONE (this session)**

- [x] Verify referenced files exist → most do not (§A)
- [x] Independently recompute L₂ local exponents → `checkers/check_C1_kodaira_consistency.py`
- [x] Emit finding → `data/certificates/C1_KODAIRA_CONSISTENCY.json`, verdict `C1_KODAIRA_LABELS_UNSUPPORTED`
- [ ] **T0 decision required** (see Decisions Needed below)

### Phase 1 — Provenance Gate (1–2 h) — *keep from proposed plan; genuinely missing*

Blocking for any literature-derived parameter claim.

- [ ] Create `docs/literature/` and `refs/literature_provenance.txt`
- [ ] Fetch: Almkvist–van Straten (arXiv:2103.08651), Gorodetsky (arXiv:2102.11839),
      Zagier 2009, Cooper 2012 (Ramanujan J. 29)
- [ ] SHA256 each; pin hashes; manually cross-check (a,b,c,d) against PDFs + OEIS
- [ ] Write a real `checkers/check_provenance_hygiene.py` (the A5/A6 checker named in
      the proposed plan does not exist, so its "expected ✅ PASS" is not evidence of anything)
- [ ] Scope honestly in the checker docstring: it verifies hashes, document identity,
      and the Cooper parameter sets — **not** 15 sequences, and it does not consult OEIS

*Side benefit:* Gorodetsky arXiv:2102.11839 is also what unblocks the s18 recurrence
(currently BLOCKED, corrupt transcription) — one fetch clears two items.

### Phase 2 — C1 REDO via Weierstrass model (8–14 h) — *replaces proposed Action 4*

Do **not** re-run the exponent→Kodaira mapping; [F2] shows it cannot work.

- [ ] Construct the Weierstrass model of the elliptic fibration for s7 and s10
- [ ] Compute the discriminant Δ(z) and j-invariant
- [ ] Classify fibres by Tate's algorithm (ord(Δ), ord(c₄), ord(c₆)) — the standard,
      sound route
- [ ] Determine mᵥ (component counts) **from the fibre types**, not assumed
- [ ] Emit `C1_cooper_s{7,10}_partner_v3.json`; explicitly supersede v2
- [ ] Cross-check: v3 singular loci must still be {1/27, −1} / {1/16, −1/4}

This is Phases 1–2 of the already-designed `docs/EXTENDED_MONODROMY_FRAMEWORK_2026_07_25.md`
(v0.5.0 roadmap) — pulled forward because it is now blocking, not optional.

### Phase 3 — C2 recompute (2–3 h) — *replaces proposed Action 5*

- [ ] Shioda–Tate with the **v3** mᵥ values: ρ = 2 + Σ(mᵥ − 1) + rank MW
- [ ] Compute rank MW rather than assuming 0 (v2 assumed 0 without derivation)
- [ ] τ = 22 − ρ; intersection form; discriminant — **derived, not pre-declared**
- [ ] Emit `C2_cooper_s{7,10}_partner_v3.json`
- [ ] **If ρ ≠ 4:** notify Stream 3 immediately — the D-3 prior changes

### Phase 4 — Physics interpretation (4–6 h) — **BLOCKED on Phase 3**

Gauge-group assignment depends on fibre type (I_n → SU(n), I_n* → SO(2n+8), etc.).
With fibre types unresolved, no gauge group can be assigned. Keep the proposed
plan's content and its discipline, once unblocked:

- [ ] Map Picard lattice → D-brane gauge groups
- [ ] Every physics claim carries an inline `[C] CONJECTURE` marker in the same sentence
- [ ] Deliverable: `briefs/STREAM2_PHYSICS_INTERPRETATION.md`
- [ ] Retain the standing guardrail: Deep Think's "load-bearing physical vacuum"
      framing is **not adopted** (ROADMAP §Physics-Washing Guardrails)

---

## Decisions Needed from T0 (Xavier)

1. **Gate E scoring.** Does the unsupported ρ = 4 prior change Gate E criterion 1?
   Options: (a) score criterion 1 as UNRESOLVED and let Gate E proceed on the other
   five; (b) delay Gate E pending Phase 2–3; (c) proceed and annotate the prior as
   Tier B-provisional. **Recommend (a)** — it is honest, keeps the 2026-07-27 date,
   and does not discard the D-3 run.
2. **Retract or annotate the v2 certificates?** Recommend *annotate* (add a
   `superseded_by` / `known_inconsistency` field) rather than delete, preserving the
   audit trail as was done for v1.
3. **Amend the proposed plan's expected outputs**, which cannot all hold ([F3]).

---

## Success Criteria (revised "geometry lock")

- ✅ Phase 0 reconciliation recorded and signed off
- ⬜ Phase 1 provenance gate PASS (with honestly-scoped checker)
- ⬜ C1 v3 fibre types from Tate's algorithm, not from L₂ exponents
- ⬜ C2 v3 ρ, τ **derived** from v3 fibre data
- ⬜ Physics brief drafted, all claims `[C]`-marked
- ⬜ No contradiction with L₃ = Sym²(L₂) (that Tier A result is untouched by this finding)
- ⬜ Feedback to Stream 1 (Σ fibre configs for S1-05 minimality)
- ⬜ Feedback to Stream 3 (final ρ, τ priors)

**What this finding does NOT touch:** `L₃ = Sym²(L₂)` remains Tier A,
kernel-verified. The exact singular loci {1/27, −1} / {1/16, −1/4} are confirmed
correct. WP-B1 chameleon results are unaffected. The issue is confined to the
Kodaira *labels* and the ρ/τ values derived from them.

---

**Provenance:** `Generated-by: Opus 5 | Verified-by: checkers/check_C1_kodaira_consistency.py | Reviewed-by: [pending T0]`
