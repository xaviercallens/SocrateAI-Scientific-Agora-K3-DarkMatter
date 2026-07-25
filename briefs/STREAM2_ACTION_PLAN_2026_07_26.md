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

### Phase 2 — ⚠️ **REVISED 2026-07-26 after Deep Think (T0s) literature review**

> **My original Phase 2 ("redo C1 via Weierstrass model + Tate's algorithm on L₂")
> was itself wrong** and is retracted. It repeated the same category error one level
> up: Tate's algorithm requires a genuine unipotent Picard–Fuchs operator, and L₂ is
> not one. See Deep Think's mandate in §E below. **Do not run Tate's algorithm on
> raw L₂ under any normalization.**

**Phase 2A — ⚠️ REVISED AGAIN 2026-07-26: Routes α and β are BOTH REFUTED (E-008)**

> Both previously-proposed routes were **tested and closed**. Neither Deep Think's
> Route A (use L₃) nor the gauge-transform route (my Route β, also Deep Think's
> untwisting suggestion) works. See `ESCALATIONS.md` **E-008**.

- ~~**Route α: derive geometry from L₃.**~~ **REFUTED.** Deep Think's premise was that
  "L₃ = Sym²(L₂) makes the ½ exponents double to 1, rendering L₃ unipotent." Tested by
  `scripts/compute_L3_monodromy.py`: **L₃ exponents are {0, ½, 1} — not unipotent.**
  Sym² of a rank-2 system with exponents {a,b} gives {2a, a+b, 2b}; with {0,½} that is
  {0,½,1}. Only y₂² doubles to 1 — the **cross term y₁y₂ keeps ½**. Confirmed two
  independent ways (direct order-3 indicial computation + Sym² structure), which agree
  exactly. **Kodaira classification is blocked at the L₃ level too.**
- ~~**Route β: untwist by gauge transformation.**~~ **REFUTED.** A gauge transform
  `y ↦ f·y` shifts *all* exponents at a point by `ord(f)`, so **exponent differences are
  gauge-invariant**. A difference of ½ cannot be gauged away — fractional twists like
  `P₂^{1/4}` shift uniformly too. (This closes my own earlier Route β as well.)

**Route γ (the only surviving path): ramified Hauptmodul pullback**

Only a **ramified covering** genuinely converts exponent ½ into an integer.
- [ ] Fetch the level-7 Hauptmodul **A279618**; A279619 is the expansion of **A002652**
      (weight-1 form, disc −7) in powers of it
- [ ] Construct the pullback `z ↦ t(z)` and push L₂ (or L₃) through it
- [ ] **Verify** the pulled-back operator has integral exponents and a rational
      Wronskian — *test this, do not assume it*
- [ ] Only if that verification passes is fibre classification meaningful
- [ ] Emit `C1_cooper_s{7,10}_v3.json` **naming the operator and coordinate used**
- [ ] Cross-check: singular loci must still map to {1/27, −1} / {1/16, −1/4}

**Standing rule for this phase:** emit **no ρ and no T** until an operator with
integral exponents is in hand. `data/certificates/C1_L3_cooper_s{7,10}.json` set both
to `null` deliberately — emitting numbers here is exactly the E-007 failure.

**Phase 2B — Reframe the geometric target for s7**

Deep Think identifies the actual substrate: **modular curve X₀(7), CM by ℚ(√−7)** —
*not* a generic Beauville rational elliptic surface with 4 singular fibres. Treating it
as the latter is a false parallel.
- [ ] Restate the s7 geometric target as X₀(7) / level-7 modular
- [ ] Re-examine whether "Picard rank ρ" is even the right invariant for this substrate

### Phase 3 — C2 recompute (2–3 h) — *replaces proposed Action 5*

**Only meaningful once Phase 2 yields a genuine PF operator.**

- [ ] Shioda–Tate with **derived** mᵥ: ρ = 2 + Σ(mᵥ − 1) + rank MW
- [ ] Compute rank MW rather than assuming 0 (v2 assumed 0 without derivation)
- [ ] τ = 22 − ρ; intersection form; discriminant — **derived, not pre-declared**
- [ ] Emit `C2_cooper_s{7,10}_v3.json`
- [ ] **If ρ ≠ 4:** notify Stream 3 immediately — the D-3 prior changes

---

## §E — Deep Think (T0s) literature review, 2026-07-25 — CONCUR + root cause

Deep Think independently reached the same verdict and supplied the literature that
explains it. **Its central algebraic claim was re-verified here from repo data**
(`refs/recurrences_v1.json`), not taken on trust:

```
g.f.(A279619)² == g.f.(A183204)   →  CONFIRMED exactly on all 8 available terms
1,2,22,336,6006,…  squared  →  1,4,48,760,13840,273504,5703096,123519792
```

**Root cause (now established, upgrading finding [F4] from "likely" to confirmed):**
A279619's g.f. *is* the square root of s7's g.f. A unipotent PF operator has exponents
{0,0}; its exact square root acquires branch cuts, halving the indicial exponents to
{0, ½} and flipping the monodromy determinant to **−1** (a reflection). The irrational
Wronskian `W = C/(z√P₂)` is the exact analytic signature of that twist. So **L₂ is a
twisted PF operator — a weight-1 modular differential equation — not the PF equation
of an elliptic fibration.** No Kodaira data can be read from it.

**Literature identified (Phase 1 provenance targets, updated):**
- **L. O'Brien (2016)**, *"Modular forms and two new integer sequences at level 7"*,
  MSc thesis, Massey University (supervisor: S. Cooper) — **Theorem 6.1** defines
  c₇(n) = A279619 with the exact three-term recurrence matching our L₂.
- **Chan, Cooper & Sica (2010)**, *"Congruences satisfied by Apéry-like numbers"* —
  **Conjecture 5.4** (the earlier conjectural form).
- A279619 = expansion of the g.f. of **A002652** (x²+xy+2y², disc −7, weight-1 modular
  form) in powers of **A279618** (level-7 Hauptmodul).

**On s10 non-integrality:** expected. Level 10 (Γ₀(10)) lacks the cusp structure that
gives level 7 integer coefficients, forcing denominators scaling as powers of 2
(2-isogeny). This makes s10 a messier F-theory candidate than s7 — consistent with the
existing `[B] provisional` caveat.

### ⚠️ One correction to Deep Think's causal account

Deep Think states Stream 2 "attempted to run Tate's Algorithm on L₂," which "forced the
algorithm to misinterpret the branch cut as a Type II fiber." **Tate's algorithm was
never run.** The actual mechanism, from `scripts/compute_C1_monodromy.py:37`
(`exponents_to_kodaira_type`), is a hand-written lookup table that is independently wrong:

- its docstring asserts *"exp_diff = 1/2 ⇒ II, III, or IV"* — but **II has Δ=1/6,
  III has Δ=1/4, IV has Δ=1/3. None of them is 1/2.**
- it returns `("II (tentative)", 1, 2)` with **`components = 2` hardcoded**, regardless
  of the type it just named (Kodaira II has m = 1).
- Shioda–Tate then mechanically produced ρ = 2 + 2 + 0 = 4.

So ρ = 4 was manufactured by a hardcoded constant in a faulty lookup, not by a
misapplied Tate algorithm. Conclusion is unchanged; recording the precise mechanism
because `exponents_to_kodaira_type()` must be **deleted, not fixed** — no exponent→Kodaira
lookup is valid for a twisted operator.

- [ ] **Delete or hard-disable** `exponents_to_kodaira_type()` in `scripts/compute_C1_monodromy.py`

### Phase 4 — Physics interpretation — **BLOCKED on Phase 2/3**

Gauge-group assignment depends on fibre type (I_n → SU(n), I_n* → SO(2n+8), …). With
fibre types unresolved at *both* the L₂ and L₃ levels, **no gauge group can be assigned.**

**Deep Think "Fallacy B" — SU(5)/SO(10) GUT claims.** Deep Think flagged the proposed
Research Summary's line *"supporting SU(5) or SO(10) GUT in s₇"* as physics-washing.
Correct — and I had carried it into this plan's Phase 4. **It is struck.**

**Audit result: the repo itself was already clean.** A full scan for
`SU(5)|SO(10)|GUT` across all tracked `.md`/`.py`/`.json` returned four hits, all
already properly hedged:

| Location | Status |
|---|---|
| `CAVEATS.md:199` | explicitly "❌ Not attempted" |
| `scripts/alpha_origin_rge.py:27` | MSSM normalization comment, not an s7 claim |
| `briefs/STREAM1_TO_STREAM2_C1C2_HANDOFF.md:59` | states the gauge reading **is [C]** and requires a marker |
| `briefs/PHASE_10_K3_SELECTION.md:52` | carries **[C]**, "*We conjecture* … not a result", "No such embedding is constructed or verified" |

**No scrub was required; the existing guardrails held.** The SU(5)/SO(10) language
entered via the proposed plan, not the codebase. Recording this rather than performing
a cosmetic "scrub" of correctly-marked text.

Once unblocked:
- [ ] Restrict claims to what the real C1/C2 data supports — e.g. dark-sector coupling
      structure (strong vs. weak), **not** GUT embeddings
- [ ] Every phenomenological leap carries an inline `[C] CONJECTURE` marker in the same sentence
- [ ] Deliverable: `docs/PHYSICS_INTERPRETATION_L3.md` (per Deep Think) — but note the
      name presumes an L₃-based geometry that E-008 has now blocked; retitle to match
      whichever operator/coordinate actually yields the geometry
- [ ] Standing guardrail retained: the "load-bearing physical vacuum" framing is
      **not adopted** (ROADMAP §Physics-Washing Guardrails)

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
- ⬜ C1 v3 fibre types from an operator with **integral** exponents (Route γ), not from L₂ or L₃
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
