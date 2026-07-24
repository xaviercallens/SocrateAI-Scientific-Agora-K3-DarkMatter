# K3_SELECTION_REPORT — v0.1-DRAFT (Stream 2 → Stream 3 unblock)

**Date:** 2026-07-24 | **Status:** DRAFT — criterion tables final (machine-generated); **selection rationale T0-PENDING**
**Requested by:** Stream 3 Fable brief "Execution Expectations to Unblock Stream 3" (2026-07-24)
**Regenerate tables:** `python3 scripts/render_k3_selection_report.py`

---

## 0. Critical reconciliation — read before the tables

Stream 3's v0.7.0-checker-suite (their repo, DarkMatterK3-Home) reports **s7/s10 FAIL C3/C3b**.
This repo's v0.3.0 reports **SYM2_PROVED** for s7/s10 (Lean kernel, axiom-clean, re-reproduced live 2026-07-24).

**There is no mathematical contradiction.** The two criteria are different questions:

| Label (proposed canonical) | Question asked | s7/s10 answer | Where verified |
|---|---|---|---|
| **C3b-CAT** (catalogue search — what v0.7.0 tested) | Is the bulk Sym²-of / Shioda–Inose-mapped-to a **Zagier-catalogued** order-2 operator? | **FAIL** — corroborated independently in THIS repo: moduli-map search vs apery_zeta2 = A005258 (a Zagier sporadic) → `C3B_NOT_FOUND` (Table T3); prior session tested all six Zagier sporadics → none matched | both repos, independently |
| **C3b-SYM** (constructive — what v0.3.0 proved) | Does there **exist** an order-2 L₂ with L₃ = Sym²(L₂)? | **PROVEN** (all-n operator identity over ℚ(z); Lean kernel-verified; s7 partner integral = OEIS A279619, s10 partner non-integral) | this repo: `C3b_symsqrt_*` certs + `Structures/CooperSym2Proof.lean` |

**Consequence for the Fable brief's §7:** the sentence *"s7/s10 are not symmetric squares of … **any** elliptic order-2 operator"* is **overbroad and refuted as stated** (kernel-verified counterexample exists). The correct, defensible statement is: *"…of any **Zagier-catalogued** order-2 operator."* The Cooper family sits **outside the Almkvist–Zudilin catalogue bijection** — which is precisely why its partners had to be *extracted* rather than *looked up*. Both v0.7.0's FAIL and v0.3.0's SYM2_PROVED stand, unmodified, under their own definitions. No checker was re-run or altered after seeing results (their Option-C concern does not arise: SYM2_PROVED predates the brief, commit 27b2c3f, tag v0.3.0).

**Criterion-naming hazard (flagged):** Stream 3's "C1" = mirror-map integrality; this repo's "C1" = Kodaira classification. This report uses **C1-INT** / **C1-KOD** and **C3b-CAT** / **C3b-SYM** throughout. Cross-repo reports must adopt one canonical naming before Gate E.

**s18 divergence (flagged):** v0.7.0 reports s18 `C1-INT PASS(40)`. This repo's s18 refs entry is **BLOCKED** (recurrence corrupt, does not reproduce its own terms — integrity finding 2026-07-20). We cannot corroborate their s18 row until a clean re-transcription lands in `refs/`; the two repos are running on different s18 data. F6-track: do not use s18 anywhere until resolved.

---

## 1. Criterion tables (machine-generated — do not hand-edit)

### T1. Candidate register (refs/recurrences_v1.json, frozen)

| id | type | status | source (truncated) |
|---|---|---|---|
| cooper_s7 | order-3 | OK | OEIS A183204 (http://oeis.org/A183204); Cooper 2012 sporadic sequence |
| cooper_s10 | order-3 | OK | OEIS A005260 (http://oeis.org/A005260); Cooper 2012 sporadic sequence |
| gorodetsky_s18 | order-3 | BLOCKED | Gorodetsky arXiv:2102.11839 (https://arxiv.org/abs/2102.11839); recurr |
| apery_zeta2 | order-2 | OK | OEIS A005258 (http://oeis.org/A005258); Apéry ζ(2) sequence; weight-2 |
| zagier_sporadic_A | order-2 | OK_NOT_A_PARTNER | OEIS A002893 (http://oeis.org/A002893); a(n)=Sum_{k=0..n} C(n,k)^2 C(2 |
| cooper_s7_partner | order-2 | OK | DERIVED (not literature transcription): symmetric-square root of coope |
| cooper_s10_partner | order-2 | OK | DERIVED (not literature transcription): symmetric-square root of coope |

### T2. C3b-SYM — symmetric-square structure (constructive, this repo)

| bulk | verdict | operator identity (all-n) | mirror z(L2)=z(L3) | partner integral |
|---|---|---|---|---|
| cooper_s7 | SYM2_OPERATOR_IDENTITY_PROVEN(all-n symbolic; partner revali… | True | True (q^14) | True |
| cooper_s10 | SYM2_OPERATOR_IDENTITY_PROVEN(all-n symbolic; partner revali… | True | True (q^14) | False |

### T3. C3b-CAT — catalogued-partner search (moduli-map, this repo)

| bulk | tested partner | verdict |
|---|---|---|
| cooper_s7 | apery_zeta2 (A005258) | C3B_NOT_FOUND(n_terms=24, max_bidegree=6, hypotheses=[[1, 1], [1, 2], [2, 1]]) |
| cooper_s10 | apery_zeta2 (A005258) | C3B_NOT_FOUND(n_terms=20, max_bidegree=4, hypotheses=[[1, 1], [1, 2], [2, 1]]) |

### T4. C1-KOD — Kodaira fibre classification (order-2 partners)

| partner | fibres | types | singular points z | exponents |
|---|---|---|---|---|
| cooper_s7_partner | 2 | II+II | 2/3, 1/3 | (0,1/2); (0,1/2) |
| cooper_s10_partner | 2 | II+II | 5/8, 3/8 | (0,1/2); (0,1/2) |

### T5. C2 — Picard / transcendental lattice (Shioda–Tate)

| partner | ρ | T=22−ρ | fibre contrib | MW rank (assumed) | disc (placeholder) |
|---|---|---|---|---|---|
| cooper_s7_partner | 4 | 18 | 2 | 0 | 4 |
| cooper_s10_partner | 4 | 18 | 2 | 0 | 4 |

### T6. Min-ODE-order discriminator (new checker `check_min_ode_order.py`, 2026-07-24)

| sequence | min ODE order | min recurrence order | verdict |
|---|---|---|---|
| A112019 | 2 | 3 | MIN_ODE_ORDER=2 PASS(58) [deg=5; orders<2 excluded to deg 8; min recurrence order=3] |

*(machine-generated by scripts/render_k3_selection_report.py — do not hand-edit)*

---

## 2. New verified result: A112019 (the "S₁,₂" claim)

The externally supplied "AI-swarm" matrix claims A112019 (a(n)=Σ C(n,k)·C(n+k,k)²) was
misclassified via its order-3 shift recurrence but is elliptic by minimal g.f. ODE order 2.

**Checker result (Tier B, finite-order):** CONFIRMED at `PASS(58)` — an order-2, degree-5
annihilating ODE holds across all 60 fetched terms; no order-1 ODE exists to degree 8;
minimal shift-recurrence order is 3 (degree 3). Certificate: `data/certificates/MINODE_A112019.json`;
b-file hash-pinned in `refs/MANIFEST.md`. Golden tests: apery_zeta2 → order 2 ✓ (known-good);
cooper_s7 → order 3, order-2 refused ✓ (known-bad control). 2/2 green.

**NOT verified (no checker run — do not cite):** the fractional mirror-map values (81/8 for
A112019, 27/4 for A005258), any Picard-rank claim for A002893, and every physical-role
sentence in the swarm matrix. See `docs/OEIS_FTHEORY_CLAIMS_REGISTER.md`.

---

## 3. Selection rationale — **T0-PENDING** (decision matrix)

Two mathematically honest routes exist. **Stream 2 recommends Route A for the S3-00 input**,
with Route B retained as the novel-mathematics track. Xavier (T0) decides.

**Route A — sporadic AZ pair with catalogued Zagier partner (Fable brief Options A/B).**
Fully literature-anchored: partner's modular data (level, weight-2 form) is catalogued, which
is what the S3-00 MVM derivation consumes. Prerequisite in THIS repo (est. 4–8 h, matching the
brief's estimate): add the chosen AZ sporadic + its Zagier partner to `refs/` (fetch + hash),
reproduce v0.7.0's C1-INT/C3b-CAT verdicts here (a genuine cross-repo two-model check), then
run C1-KOD + C2 on the partner to produce the fibre/lattice tables S3-00 needs.

**Route B — s7/s10 with extracted partner (C3b-SYM).**
Sym² structure is Tier A (kernel-proven); C1-KOD/C2 data already exists (T4/T5). Honest caveat:
the partner's modular identification (conjectured level-7/level-10 weight-2 realisation) is
**not literature-anchored** — Tier B at the operator level, Tier C as geometry. If S3-00 needs
catalogued modular data, Route B adds an open research dependency to the critical path.

**Transparent Cooper statement (corrects the brief's Option B wording):** the Cooper family is
excluded from the S3-00 input **not** because it lacks Sym² structure (it provably has it) but
because its partners are non-catalogued, so their modular/geometric data is not yet at the
evidence tier S3-00's pre-registration requires.

**Assumption tags:** every criterion result above carries **[A-ONT]** (contingent on
compactification realisation); T4/T5 additionally carry the stated MW-rank-0 assumption.

---

## 4. Gaps blocking report v1.0 (explicit)

1. **AZ sporadics (γ, α, δ, η) + Zagier partners are not in `refs/`** — no numbers about them
   may appear here until fetch+hash lands (anti-hallucination rule). This is the Route-A prerequisite.
2. **C2 on the selected pair's catalogued partner** — pending Route decision.
3. **T0 selection sign-off** — §3 decision.
4. **s18 re-transcription** — F6-track, blocks any s18 row.
5. **Canonical criterion naming** — adopt C1-INT/C1-KOD/C3b-CAT/C3b-SYM across both repos.

---

Generated-by: Stream 2 (Fable 5) — tables by scripts/render_k3_selection_report.py from committed certificates | Verified-by: checkers cited per table; Lean kernel for C3b-SYM | Reviewed-by: T0 pending
