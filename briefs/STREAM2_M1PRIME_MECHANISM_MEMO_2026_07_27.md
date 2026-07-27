# M1′ — Revised Mechanism Memo (Phase M) — DRAFT for T0

**Date:** 2026-07-27 · **Owner:** Stream 2 (T1 drafting) · **Status:** **DRAFT — pending T0
(Xavier).** Nothing here reopens Phase M; M2 remains unauthorized (T0 D2).
**Revises:** `briefs/STREAM2_M1_MECHANISM_MEMO_2026_07_26.md` (accepted 2026-07-26 as a
conditional negative, T0 D2). M1′ is that memo's revision against a changed geometric
substrate — not a fresh start, and not a re-litigation of M1's accepted findings.
**Binding constraints on this document:** `CLAUDE.md` epistemic ledger; VISION §1.3
(geometric relation ≠ physical coupling absent a worked EFT matching); T0 D4 / A-DE (no
dark-energy or vacuum-energy claim while B₃ is unspecified); F5b (no exact observables or
coefficient values). No numeric physical value appears anywhere below.

---

## §1. What changed since M1

M1 was written on 2026-07-26, one day after E-007/E-008, at the moment when its own
geometric premises had just been withdrawn. Three things have changed since.

| Item | Status at M1 (2026-07-26) | Status now (2026-07-27) |
|---|---|---|
| L₃ = Sym²(L₂) | [A] kernel-proven | [A] unchanged |
| ρ, T | Retracted (E-007); no replacement | **ρ = 19, T = 3 [B, derived]** (E-011; independently verified by Stream 1) |
| Exponent structure of L₂ | {0, ½}, det(monodromy) = −1; no Kodaira reading; Route γ untested | Route γ **step 0 CONFIRMED** (order 29) and **step 1 PASS_BRANCH_CUT_CLEARS** (`data/certificates/ROUTE_GAMMA_STEP1.json`, 2026-07-26): under the level-7 Hauptmodul pullback the ramification index is 2 at both finite loci, so the pulled-back exponents are integral. The ½ was a coordinate artifact of an order-2 elliptic point, not a defect |
| Transcendental lattice | Unknown | **T ≅ U ⊕ ⟨14⟩ [B, derived]** — computed Gram `[[0,0,−1],[0,14,0],[−1,0,0]]`, det −14, signature (2,1), disc form ℤ/14 (q = 1/14), derived 2n = 14, with an **explicit det-1 integral base change** realizing the splitting; zero proper even invariant overlattices. All controls pass (`checkers/test_U1_controls.py`), including the cooper_s10 level control deriving det −20 / U ⊕ ⟨20⟩ (`briefs/STREAM2_U1_EXECUTION_2026_07_27.md`) |
| Framework | Cited, unread | **Read and hash-pinned**: Dolgachev Thm 7.1 (moduli of M_n-polarized K3s ≅ X₀(n)+), §7 p.20 ((M_n)⊥ = U ⊥ ⟨2n⟩), Thm 7.3 (ample locus minus a countable set), Doran Thm 5.13 (PF operator = symmetric square) — `briefs/STREAM2_PHASE4_STEP2_SOURCES_READ_2026_07_26.md`, re-derived symbolically in U1 stage 0 where computable |
| Kodaira picture M1 argued against | Retracted | Still retracted, and now **explained**: the finite loci are order-2 elliptic points of X₀(7)+ (E-008/E-009). No Kodaira reading is used or implied anywhere below |

**Consequence for D2 clause 1.** D2 gated M2 on "Route γ yields an integral-exponent
operator and derived C1v3/C2v3 lattice data." Route γ step 1 returned an integral-exponent
verdict on 2026-07-26, and derived lattice data now exists (v3 ranks, live; v4-DRAFT
lattice, pending). Stream 2's reading is that **clause 1 is satisfied on its letter**,
with two caveats T0 should weigh: the lattice data arrived by the U1 monodromy-invariant
route rather than by re-running C1/C2 through the pulled-back operator, and the −1 locus in
the step-1 certificate agrees to 3 significant digits against its series tail bound (the
1/27 locus agrees to 17). **Clause 2 — T0 reopening Phase M against a revised M1′ — is
therefore the only remaining gate, and this document exists to inform it.**

**Two named residual links carry forward** into everything below (U1 brief §4): monodromy
entries enter by rational recognition of 60-digit numerics before exact structural
verification (Link 1), and the identification of the computed lattice with the
transcendental lattice T rests on the read framework's T = U ⊕ ⟨2n⟩ shape rather than on
computation (Link 2). Both keep the substrate at Tier B, not Tier A.

---

## §2. Does the certified substrate change the mechanism landscape?

The question M1′ has to answer is narrow and specific: **does the derived
M₇-polarized/modular geometry supply any route to a worked EFT matching — dark-sector
coupling structure or mediator identification — that M1 lacked?** Six candidate routes are
enumerated below. Each is stated with what it would take, the tier of each step, and the
assumption tags that apply.

A note on how to read this section: M1 could not answer its walls because the quantities
they were posed in had been withdrawn. That is no longer the situation. The walls are now
**posable in derived quantities**, and two of them are answerable in their stated form.
Answering them is what §2 does.

### R1 — Gauge algebra from the Néron–Severi root sublattice

**The route.** The framework's complementary shape for an M₇-polarized K3 is
NS ≅ U ⊕ E₈ ⊕ E₈ ⊕ ⟨−14⟩ (rank 19, matching ρ = 19 [B]). An E₈ ⊕ E₈ root sublattice is
lattice-level structure of exactly the kind A.1.4 found missing: in the standard
M-theory-on-K3 / F-theory dictionary, ADE root systems in NS are associated with gauge
enhancement at loci where the corresponding −2 classes become effective and contract.
This is the strongest-looking candidate and deserves the most careful accounting.

**What it would take, step by step:**

1. **Promote NS to [B].** U1 derived **T**, not NS. NS is currently obtained from T by the
   framework's complementary shape, which is an additional primitive-embedding/uniqueness
   step in Λ_K3 (Nikulin-type) that **has not been executed in this repo**. H-M7's NS half
   accordingly stays where `STREAM2_PHASE4_LATTICE_REFINEMENT_2026_07_26.md` §3 left it,
   pending that step. *Tier: [B]-pending, and a bounded, well-posed computation.*
2. **Select an elliptic fibration.** A gauge algebra is read from a frame lattice, which
   requires a primitive U ⊂ NS (fibre + section). A K3 with this NS admits many such
   embeddings, generally inequivalent, each with its own root content. **This program has
   no selection principle among them,** and the choice is discrete, so it cannot be fixed
   by continuous data. *Tier: unconstrained discrete choice — not a computation with a
   unique answer.*
3. **Pass from roots to contracted curves.** Roots in NS are not curves on any actual
   member; which −2 classes are effective and contractible is a question about the specific
   member, and Dolgachev Thm 7.3's countable-exceptional-set caveat applies to exactly this
   kind of jump. *Tier: C.*
4. **Obtain a coupling.** Even granting 1–3, what steps 1–3 would supply is a *label* — an
   algebra type and rank. A.1.4's ansatz needs Re(f) ∼ 𝒱^{2/3}/g_s, i.e. the volume of a
   wrapped divisor in the Calabi–Yau fourfold X₄. **No K3 lattice invariant carries a
   volume.** *Tier: C, and blocked — X₄ and its threefold base B₃ are unspecified.*

**Assessment.** R1 genuinely improves A.1.4's obstruction — from "no gauge-algebra reading
exists at these loci at all" to "an algebra type could be *posed*, conditional on steps 1
and 2." That is a real change and Stream 2 records it as such. But a₁ and Λ_D stay exactly
as blocked as before, because their blocker was never the fibre reading: it is Vol(D) in an
unspecified fourfold. R1 therefore moves the obstruction's *reason* without moving its
*status*. We conjecture [C] that a dark gauge sector *would* be associated with such a root
system if a fourfold containing this K3 were exhibited and a fibration selected; no such
fourfold has been exhibited, so nothing follows today. **Tags: [A-ONT], [A-REL], [A-VOL].**

### R2 — The flat-direction wall (A.2.5), re-examined

**The route.** A.2.5's obstruction is stated as: the PF operator controls a rank-3
sub-VHS, the C2 certificate gives T = 18, so flux along that subspace leaves 18 − 3 = 15
moduli unstabilized, and those flat directions would be massless scalars that fifth-force
bounds do not permit.

**What changed.** Both inputs to that count are retracted. T = 18 was withdrawn by E-007;
the derived value is T = 3 [B], and U1 further derives the lattice itself as U ⊕ ⟨14⟩. On
those numbers the rank-3 sub-VHS that L₃ controls **is** the transcendental lattice, and
the "15 flat directions" count does not survive as written.

> **Flagged for Stream 3 (in-band retraction hygiene, standing rule 3).**
> `PREDICTION_APPENDIX_A.md` §A.1.4 and §A.3.4 each carry a dated 2026-07-27 basis
> correction. **§A.2.5 does not**, and still reads "(ρ=4, T=18)" and "18 − 3 = 15". Stream 2
> raises this as a correction item, not as a finding to exploit: the arithmetic there rests
> on retracted numbers and needs its own dated note. Stream 2 has touched nothing in the
> Stream 3 repo.

**What did not change.** The object that A.2.5 needs stabilized was never the K3's
transcendental lattice on its own — it is 𝒱, g_s, and the fourfold's moduli. The
Gukov–Vafa–Witten superpotential W = ∫ G₄ ∧ Ω₄ requires a flux G₄ on X₄, hence B₃. So the
wall's *stated form* dissolves while its *operative content* is untouched: there is still no
flux potential to differentiate, so |∂²V_flux(F(z*))|^{1/2} remains carried symbolically and
assigned no value, exactly as A.2.5 records. The certified geometric input there (the mirror
map F) was already real before U1 and is not what was missing.

**Assessment.** R2 is where the certified substrate does the most work, and it still ends
at the same place. Correcting the count removes a *wrong* reason for the blockage without
removing the blockage. *Tier: the arithmetic correction is [B]; everything downstream of it
is [C] and blocked.* **Tags: [A-VOL], [A-ONT].**

### R3 — Arithmetic vacuum selection from X₀(7)+

**The route.** Dolgachev Thm 7.1 (read) puts the moduli space at X₀(7)+, which comes with
distinguished points: the cusp, the two order-2 elliptic points fixed by the Fricke
involution (the family's two finite singular loci), and CM points. One could conjecture that
a vacuum sits at such a point, which would name z* — the evaluation point A.2.5's ansatz
needs.

**What it would take.** A fetched-and-read source connecting arithmetic special points to a
physical attractor or vacuum condition (nothing of the kind is in
`docs/literature/MANIFEST.md` today), **plus** a potential on a specified X₄ whose critical
point the selected point is. Absent that potential, choosing a point because it is
arithmetically distinguished would be a fit presented as a derivation — the failure
`.agents/AGENTS.md` Rule 7 names.

**Assessment.** R3 could at most name *where* to evaluate; it supplies nothing to evaluate.
Recorded as a well-posed literature question, not adopted. *Tier: C, unconstructed.*
**Tags: [A-ONT], [A-VOL].**

### R4 — Fixing the WP-B1 chameleon constants from lattice data

**The route.** M1 §3 named its own re-entry condition for the one mechanism chain in this
program with Tier A structural backing: *"if Route γ-derived lattice data can fix or bound
(m_bare, α_ch, C_max) independently of the target catalogs, this candidate becomes
nameable."* U1 delivered Route γ-adjacent lattice data. So this condition is now testable,
and testing it is obligatory rather than optional.

**Test.** What U1 delivered is U ⊕ ⟨14⟩, det −14, disc form ℤ/14 on a generator, derived
2n = 14 — dimensionless lattice arithmetic and a discriminant form. What the chameleon
sector needs is a mass, a coupling, and a density threshold. Passing from lattice invariants
to dimensionful constants requires a compactification scale (M_s, 𝒱, g_s), and no lattice
invariant carries one.

**Assessment.** **M1's own named re-entry condition is not met by U1.** This is the
cleanest single test M1 left behind, and it returns negative. *Tier: C.* **Tags: [A-VOL],
[A-ONT], [A-REL].**

### R5 — Sym² / Shioda–Inose as a coupling (recorded closed, so it is not re-proposed)

VISION §1.3 is a binding ruling: the symmetric-square relation is a geometric relation
between the K3 family and the elliptic family and does not by itself supply a physical
coupling, "locking", or dynamical relation between a bulk vacuum and a brane EFT. U1
strengthens the geometric relation's certification and leaves that ruling untouched.
Enumerated here only so that a later reader does not mistake the improved substrate for an
opening. *Tier: closed by ruling.*

### R6 — Dark energy / a₃ (recorded closed by standing policy)

A.3.4's obstruction — χ(X₄) is a global invariant of the fourfold and depends on the choice
of B₃, so the D3 tadpole condition is not merely unsatisfied but not posable — carries its
2026-07-27 correction and is explicitly unaffected by the ρ/T revision. T0 D4 / A-DE is
standing policy: no model under this program makes any dark-energy or vacuum-energy claim
while B₃ is unspecified. Not a route. *Tier: closed by policy.*

### §2 net

Six routes; one (R1) improved in its reasoning without changing status; one (R2) resolved in
its stated form while its operative blockage survives; one (R4) tested against M1's own
re-entry condition and returning negative; three closed by ruling, policy, or absence of a
source. **Every route that reaches as far as a coupling terminates on the same object: an
unspecified Calabi–Yau fourfold X₄ and its threefold base B₃.** That object is not a K3
lattice fact, and no further K3 lattice work — however well certified — can supply it.

---

## §3. Verdict — the conditional negative survives, on a stronger basis

**M1′ files a conditional negative.** No mechanism route can be named today, and none is
manufactured here to justify reopening Phase M.

The negative has changed character, and the change is the substantive content of this memo:

- **M1's negative was epistemic.** The walls could not be cleared *or posed*, because the
  quantities they were written in had been withdrawn hours earlier. The honest statement was
  "we cannot tell."
- **M1′'s negative is structural.** The walls are now posable in derived quantities, two of
  them are answerable in their stated form, and the answer is still no mechanism — for a
  single named reason that is not about K3 geometry at all. The honest statement is now "we
  can tell, and it is no, because the missing object is the fourfold."

That is a genuine advance and should be read as one. It also narrows what future work can
help: M1's unblocking condition (Route γ) has discharged, and discharging it did not move
the mechanism question. Further lattice refinement on this family — the s10 analogue, the
NS promotion step, the abstract genus statement — is worthwhile mathematics and Stream 2
would defend it as such, but **none of it is on the path to a mechanism**, and M1′ recommends
it not be justified on those grounds.

**Conditions for revisiting, stated crisply.** Phase M becomes answerable in the affirmative
only if all of the following exist, in this order:

1. **A specified Calabi–Yau fourfold X₄ containing this K3, with its threefold base B₃ —
   exhibited, not assumed.** From it, χ(X₄) and Vol(D) become computable. Nothing in R1–R4
   moves without this, and this is not a Stream 2 lattice task.
2. Given (1): A.1.4 and A.3.4 become **posable** (posable, not answered) — and A.3.4 further
   requires T0 D4 / A-DE to be revisited before any statement is made.
3. Given (1): a flux vector G₄ on X₄ for which the vacuum is a genuine critical point, at
   which |∂²V_flux| acquires a value — A.2.5.
4. For R1 additionally: the NS promotion step (§2 R1 item 1) **and** a stated principle
   selecting an elliptic fibration (§2 R1 item 2). Item 1 is a bounded computation; item 2
   is currently an open question of principle, not of effort.

If T0 judges (1) outside this program's scope, then the honest reading is that the geometric
leg has no path to an astrophysical model from the s7/s10 pair, and the filing of that is the
program's clean negative — as M1 §6 anticipated, though for a different reason than M1
expected.

**Kill condition (M1 §5, carried forward verbatim in effect).** If after the two-model pass
no relation survives (𝒱, g_s)-elimination — or no mechanism clears the walls without importing
an unconstructed scenario — Stream 2 files the negative and stops. Note that A.4's elimination
algebra is machine-verified and symbols-only; it has no inputs today.

---

## §4. Decision skeleton for T0

D2 clause 1 is satisfied on its letter (§1). Clause 2 is T0's, and these are the options as
Stream 2 sees them. Stream 2 recommends **Option B**, but the recommendation is subordinate
to the accounting in §2 — T0 should weigh the options against that, not against the
recommendation.

| Option | What it means | What it commits the program to |
|---|---|---|
| **A — Reopen Phase M now** | T0 rules clause 2 satisfied; M2 opens on the certified substrate | The M2 two-model derivation runs on a chain whose first link (X₄/B₃) is absent. Both models are blocked at the same point today, so the two-model rule would compare two non-derivations. Real risk of a fit dressed as a derivation — the failure Rule 7 names and the one M1 was accepted for avoiding. Stream 2 does **not** recommend this unless T0 first authorizes a *fourfold-specification* work package, which is new scope, not M2 |
| **B — Keep Phase M dormant, re-gate it** | Phase M stays dormant; D2's gating condition is **replaced**, since Route γ has discharged without moving the mechanism question. New gate: an exhibited X₄ with base B₃ (§3 condition 1) | Records that the blocker is the fourfold, not the K3 — so future work is aimed at the real obstruction instead of at further lattice certification. M2 stays unauthorized. Stream 2 continues lattice/moduli work on its mathematical merits, explicitly **not** as mechanism work. Costs nothing already earned; keeps the option open honestly |
| **C — Close Phase M and file the negative** | Phase M closes without M2; the program files its negative on the geometric leg | The program makes no mechanism claim and no astrophysical-model claim from this family. The mathematics stands on its own and is publishable as mathematics: L₃ = Sym²(L₂) [A], ρ = 19 / T = 3 [B], T ≅ U ⊕ ⟨14⟩ with an explicit splitting [B], moduli = X₀(7)+ [B], the elliptic-point resolution of the Kodaira category error. Stream 3 proceeds on the exclusion/FIT track only, under the standing pin protocol. This is the correct option if T0 judges fourfold specification out of scope |

**Referenced, not decided here.** The `EXECUTION_PLAN.md` §S3-00 step 2(b) re-scope option
(re-scope onto the derived M₇-polarized geometry, or strike) is put to T0 by the U1 fan-out
brief and remains T0's to adopt. §2 R1 is the relevant input: a re-scoped 2(b) would gain a
*posable* lattice-level input and would still not gain a coupling. Stream 2 has touched
nothing in S3-00.

**Separate small item.** The §2 R2 flag — `PREDICTION_APPENDIX_A.md` §A.2.5 lacks the dated
basis correction that §A.1.4 and §A.3.4 carry — is a Stream 3 hygiene item, independent of
which option T0 picks.

---

## §5. Scope guards on this document

- No numeric physical value appears above (F5b). The integers that appear (14, 19, 3, −14,
  −20, 2n) are computed lattice and rank data with certificates named in §1; none is an
  observable, a coefficient, or a scale.
- No Kodaira type is claimed, cited, or implied anywhere (E-007/E-008/E-009 stand).
- No dark-energy or vacuum-energy claim is made (T0 D4, A-DE).
- No physical coupling is claimed from the Sym² relation or from any lattice fact
  (VISION §1.3).
- Every physical-interpretation sentence above carries a conjecture marker or an explicit
  [C]/blocked tier label in the same sentence.
- Nothing outside this file was modified: no certificate, no pinned document, no TODO entry,
  and nothing in the Stream 1 or Stream 3 repositories.
- `C2_cooper_s7_v4_DRAFT.json` remains DRAFT; v3 remains the live certificate; Gate E
  criterion 1 remains UNRESOLVED (T0 D1). M1′ changes none of these.

---

**Generated-by:** Opus (Stream 2 agent) | **Verified-by:** check_tier_language.py + source
list above (`CLAUDE.md` ledger; epistemic-guardrails skill; M1 memo; T0 D2/D4;
`STREAM2_U1_EXECUTION_2026_07_27.md`; `STREAM2_TO_STREAMS1_3_U1_CLOSED_2026_07_27.md`;
`STREAM2_PHASE4_STEP2_SOURCES_READ_2026_07_26.md`; `STREAM2_PHASE4_LATTICE_REFINEMENT_2026_07_26.md`;
`STREAM2_M1PRIME_ADJUDICATION_2026_07_26.md`; `EXECUTION_PLAN.md` §S3-00;
`data/certificates/ROUTE_GAMMA_STEP1.json`, `C2_cooper_s7_v4_DRAFT.json`;
Stream 3 `PREDICTION_APPENDIX_A.md` §A.1.4/A.2.5/A.3.4/A.4) | **Reviewed-by:** pending T0 (Xavier)
