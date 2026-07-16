# 🌌 Dual-Scale Topological Universe Model — Three-Stream Master Plan

**Date:** 2026-07-16 · **Status:** ACTIVE (supersedes single-repo framing; absorbs `K3xT2_DEEP_IMPROVEMENT_PLAN.md` as the Stream-2 gate machinery)
**Authority:** Vision set by HUMAN (Xavier); plan drafted by Fable session after full codebase + achievements audit; all gates remain HUMAN-decided.

---

## 1. The Vision

The **Dual-Scale Topological Universe Model** unifies three lines of work under one F-theory picture:

- **Theory:** F-theory compactification on an elliptically fibered Calabi–Yau fourfold with **base B₃ = K3 × T²** and **elliptic fiber**.
- **K3 Selection:** AutoEvolve gate battery classifying **Cooper s₇/s₁₀ (order-3 Picard–Fuchs → K3 surfaces)** vs **S₁₂/S₂₁ (order-2 Picard–Fuchs → elliptic curves)**.
- **Experimentation:** DarkMatter@Home volunteer-GPU network validating (or killing) the empirical signatures against SDSS, Euclid, and PTA data.

### The F-theory duality mapping (hypothesis, not established fact)

| Physical phenomenon | F-theory geometry | Generating sequence | Mathematical order |
|---|---|---|---|
| Dark energy / global cosmic web | Base manifold (rigid) | Cooper s₇ / s₁₀ | Order-3 ODE (K3 surface) |
| Dark matter subhalos / tidal stress | Elliptic fiber (flexible) | S₁₂ / S₂₁ | Order-2 ODE (elliptic curve) |
| Baryonic matter / halo centers | Discriminant locus Δ_F = 4f³ + 27g² | Δ_obs peaks | Singularities (7-brane loci) |

---

## 2. Three Parallel Streams

| Stream | Repository | Focus | Goal |
|---|---|---|---|
| **1. Theory** | [`SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal`](https://github.com/xaviercallens/SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal) | F-theory formalization in Lean 4 | Mathematically certify the Dual-Scale Model |
| **2. K3 Selection** | [`SocrateAI-Scientific-Agora-K3-DarkMatter`](https://github.com/xaviercallens/SocrateAI-Scientific-Agora-K3-DarkMatter) (this repo) | AutoEvolve for K3 sequence selection | Confirm Cooper s₇/s₁₀ as true K3 surfaces |
| **3. Experimentation** | [`DarkMatterK3-Home.github.io`](https://github.com/xaviercallens/DarkMatterK3-Home.github.io) (+ server infra in `SocrateAI-Scientific-Agora-Home`) | GPU-based validation with SDSS/Euclid/PTA | Empirically validate the model |

The streams run **in parallel** but exchange typed artifacts (§6): Stream 2 exports certified sequences and exact discriminants to Stream 1 (as named axioms) and to Stream 3 (as preregistered observables); Stream 3 returns quorum-replicated empirical verdicts that Stream 1 records as empirical axioms and Stream 2 uses to adjudicate F1–F5.

---

## 3. Key Hypotheses — with current evidence status (audited 2026-07-16)

### H1 — Cooper s₇/s₁₀ are order-3 Picard–Fuchs ODEs → true K3 surfaces (F-theory base)

**Status: PARTIALLY ESTABLISHED (classification done; "true K3" certification open).**

Already achieved in this repo:
- G1-1: minimal-ODE order-3 classification, controls pass (A005259→K3, A005258→elliptic). `data/autoresearch_v2/g1_1_order_classification.json`
- G1-2: weight-3 Weil bounds pass for real Stienstra–Beukers a_p, 44 primes. `g1_2_weil_modularity.json`
- G1-3: mirror-map integrality on the **minimal** operator (s₇: q₂=9, s₁₀: q₂=4). `g1_3_mirror_integrality.json`
- Lean: exact shift recurrences `decide`-proved n∈[0,20], zero sorry (`Structures/CooperS7Recurrence.lean`, `CooperS10Recurrence.lean`), self-verified at runtime against OEIS b-files by `lss_tensor_analytics/k3_kernel_engine.py`.
- GATE D-2.4: **exact singular loci** — s₇: z ∈ {−1, 1/27}; s₁₀: z ∈ {−1/4, 1/16}; ratio 16/27 ≈ 0.593. `data/k3t2/d2_4_singular_loci.json`

Still needed to say "**true** K3 surface" (Stream 2 backlog, §5.2):
- Identify each PF operator with a known K3 family / literature identification (Cooper level-7 and level-10 weight-3 forms), match a_p tables to a specific weight-3 newform in LMFDB, and record the geometric model (transcendental lattice / Picard rank where available).
- s₇-vs-s₁₀ adjudication via the preregistered singular-locus discriminant (the only currently valid discriminant — the FFT observable is dead, see H3).

### H2 — S₁₂/S₂₁ are order-2 Picard–Fuchs ODEs → elliptic curves (F-theory fiber)

**Status: ESTABLISHED at the ODE/arithmetic level (GATE-B, formally recorded).**

- S₁₂ (A112019): order-2 minimal ODE **and** non-integral mirror map q₂ = 81/8 — dual-ground formal rejection as K3. `data/autoresearch_v2/s12_formal_validation_rejection.md`
- S₂₁ (A005258, Apéry ζ(2)): order-2, retained as elliptic negative control; 40-year literature anchor.
- Remaining (Stream 2, low priority): name the actual elliptic curve / weight-2 newform behind each (LMFDB a_p match), so the "fiber" half of the mapping is as concrete as the base half.

### H3 — Δ_obs spikes (e.g. K3-DISC-0003) → 7-brane intersections (discriminant locus)

**Status: NOT SUPPORTED by any currently valid measurement. This is the load-bearing open front.**

Two audit facts constrain this hypothesis absolutely:
1. **GATE D-1.3 verdict (preregistered, executed): F1_FAILS_KERNEL_BLIND.** r(cooper_s7, random_control) = 1.0000 — the FFT-contrast Δ observable cannot distinguish any K3 kernel from unstructured noise. All prior "Δ discoveries" (incl. Δ_s7 = 663.4) carry **no evidential weight**. `data/k3t2/GATE_D1_DECISION.md`
2. **Provenance (A7):** the historical headline numbers (S₁,₂ ≤ 1.177, K3-DISC-0003 Δ = 47.0, 327,918-galaxy run) are external DarkMatter@Home outputs, **not reproducible from committed artifacts**.

Therefore H3 is *reframed, not abandoned*: the F-theory picture itself supplies the observable redesign. In F-theory, matter lives where the fiber degenerates — i.e., where the modulus hits the **discriminant locus**. The exact D-2.4 loci (z = 1/27 for s₇, z = 1/16 for s₁₀) give a **preregistrable, kernel-specific** prediction: the response of any valid observable must steepen at kernel-specific critical densities ρ_crit(s₇) ≠ ρ_crit(s₁₀). A kernel-blind statistic can never fake this. The redesigned observable (Stream 2 → Stream 3 handoff) is **proximity of the local modulus z(ρ_b) to the exact singular locus**, replacing generic FFT contrast.

---

## 4. Stream 1 — Theory (Lean 4 F-theory certification)

**Repo:** `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal` · **Tier:** Sonnet (proofs) / Haiku (CI, mechanical)

**Achieved (v0.1, commit f44f8b3):** 6 Lean modules, **0 sorry** — `FTheoryFibration.lean` (Weierstrass fibration, Kodaira classification, dual-scale proof), `Weierstrass.lean` (Δ, j-invariant, singularity classification, 0 axioms), `DiscriminantLocus.lean` (Tate's algorithm, ADE gauge algebras, 0 axioms), `DualScaleStability.lean` (LVS Hessian/Sylvester), `ChameleonRescue.lean`, `DualScaleMaster.lean`. Six named axioms with audit inventory.

**Backlog:**

| ID | Task | Tier | Validation |
|---|---|---|---|
| S1-1 | **Axiom hygiene:** `pipeline_upper_bound` (S₁₂ ≤ 1.177) inherits the A7 provenance defect — demote to `hypothesis_` prefix or re-source from a Stream-3 quorum re-run (DM-3). No axiom may encode a non-reproducible number without a provenance tag in its docstring. | Haiku | grep audit + CI |
| S1-2 | Import Stream-2 certified inputs: replace `empirical_S12_degree` / `empirical_s7_degree` axioms with references to the exact-arithmetic gate artifacts (G1-1 JSON hashes in docstrings); add the D-2.4 singular loci as *proved* rational facts (they are exact ℚ values — provable, not axiomatic). | Sonnet | `lake build` exit 0, 0 sorry; axiom count decreases |
| S1-3 | Formalize the **base geometry**: K3 Betti/χ=24 arithmetic + T² lattice quadratic form m²_{n,m} ∝ \|n+mτ\|²/τ₂ (absorbs D-2.3 `T2Lattice.lean` from the old plan — it lands in Stream 1, mirrored here). Math-only theorem names (Rule 4). | Sonnet | `lake env lean` exit 0, 0 sorry, `#print axioms` pasted |
| S1-4 | Kodaira-type classification of the s₇/s₁₀ degenerations at their exact singular points (which fiber type does each PF singular locus correspond to?) — the theoretical heart of "Δ_obs spikes = 7-branes". | Sonnet | doc + Lean where mechanizable |
| S1-5 | Manuscript: Dual-Scale Model paper skeleton pulling Parts IV–VIII lineage together, with the Provenance Ledger pattern from `THEORY_ALIGNMENT.md`. | Sonnet | LaTeX compiles |

**Stream-1 gate (HUMAN): GATE-T** — axiom inventory reviewed; every axiom either discharged, tagged `empirical_` with a reproducible artifact hash, or tagged `hypothesis_`.

---

## 5. Stream 2 — K3 Selection (this repo: AutoEvolve + gate machinery)

**Tier routing unchanged:** Haiku = mechanical/binary-checkable; Sonnet = derivations + non-decide Lean; HUMAN = gates.
**The existing gate sequence (R-0 → D-1 → D-2 → D-3 → GATE-E in `K3xT2_DEEP_IMPROVEMENT_PLAN.md`) remains binding** — this section re-scopes it under the three-stream vision.

**Achieved:** GATE R-0 ✅ (c3a1b37) · fabricated-array fix + self-verifying kernel engine ✅ (40f2151) · GATE D-1.3 kernel-swap verdict ✅ (F1_FAILS_KERNEL_BLIND) · GATE D-2.4 exact singular loci ✅ · CI 28/28 incl. real `lake build` of the 3 finalists.

**Backlog (priority order):**

| ID | Task | Tier | Validation |
|---|---|---|---|
| S2-1 | **Observable redesign** (unblocks everything empirical): implement `lss_tensor_analytics/singular_locus_observable.py` — distance of local modulus z(ρ_b) to the exact locus (1/27 vs 1/16), plus log-branch response steepening. **Must pass the same kernel-swap battery D-1.3 that killed the FFT observable:** preregistered requirement r(s7, random) < 0.5 AND r(s7, s10) < 0.95 on mocks *before* any real-data run. | Sonnet design / Haiku run | `data/k3t2/d1_3b_kernel_swap_v2.json`; preregistered rule committed first |
| S2-2 | D-2.1: one m_eff(Δ) law (resolve exp(kΔ) vs (1+κΔ)^{1/4} from the chameleon potential; identify n in m_eff ∝ ρ^{(n+2)/(2n+2)}). | Sonnet | `docs/derivations/meff_delta_law.md` + Taylor test |
| S2-3 | D-2.2: ρ_b → z as a declared 2-parameter family z(ρ; a, b), marginalized downstream; sensitivity grid on the S2-1 verdict. | Sonnet | API change + sensitivity table |
| S2-4 | **True-K3 certification** (H1 closure): match s₇/s₁₀ a_p tables to specific weight-3 newforms (LMFDB), record literature identification of the Cooper level-7/level-10 K3 families; same for S₁₂/S₂₁ as weight-2/elliptic (H2 closure). | Sonnet | `data/autoresearch_v2/k3_identification.json` + doc |
| S2-5 | AutoEvolve continuation: extend the evolutionary sweep (`autoresearch_v2_alphaevolve.py`) with the singular-locus fingerprint as a new gate — candidates now classified by (ODE order, integrality, **exact singular-locus structure**). | Haiku | survivors JSON + gate battery rerun |
| S2-6 | D-3 empirical reruns (**FROZEN until S2-1 passes its battery**): 35-sector sweep, tomography, TDA-β₁, lensing — exactly as specced in the deep plan §5, with the new observable. | Haiku/Sonnet | per-table artifacts |

**Stream-2 gate (HUMAN): GATE D-1v2** — adjudicate the redesigned observable's kernel-swap verdict; only a pass unfreezes D-3 and authorizes Stream-3 job dispatch.

---

## 6. Stream 3 — Experimentation (DarkMatter@Home GPU validation)

**Repos:** `DarkMatterK3-Home.github.io` (volunteer-facing) + `SocrateAI-Scientific-Agora-Home` (server/API infra) · **Tier:** Haiku (mechanical protocol work), HUMAN (anything volunteer-facing/external)

**Achieved:** pilot run infrastructure exists (327,918-galaxy run, K3-DISC-0003) — but per A7 its outputs are **not reproducible from committed artifacts** and per D-1.3 its statistic was kernel-blind. Stream 3's first job is therefore *re-foundation, not expansion*.

**Backlog (absorbs Phase 8.E DM-1…DM-4 from TODO.md):**

| ID | Task | Tier | Validation |
|---|---|---|---|
| S3-1 | (=DM-1) Job spec schema: `{survey_tile, statistic_hash, candidate_id ∈ {cooper_s7, cooper_s10, t103, random_control}, seed, client_version}`. The `statistic_hash` pins the **redesigned** observable code — no job runs the dead FFT statistic. | Haiku | schema JSON + validator test |
| S3-2 | (=DM-2) Quorum replication: ≥2 independent clients per tile; disagreement → quarantine. **Every job batch includes blinded random_control kernels** so kernel-blindness is monitored continuously in production, not just in mocks. | Haiku | protocol doc + server test |
| S3-3 | (=DM-3) Re-run the v1 headline numbers (S₁,₂ ≤ 1.177, Δ = 47.0, K3-DISC-0003 coordinates) under quorum with the new observable. Preregistered framing: these are **target coordinates to re-test, not numbers to match**. Archive the run so A7 closes. | Haiku | quorum artifacts committed; A7 struck from the defect table |
| S3-4 | (=DM-4) Dispatch the D-3 sweep (S2-6) as volunteer jobs: SDSS DR17 sectors, Euclid tiles when available, both s₇ and s₁₀ kernels + control. | Haiku | dispatch log + quorum results |
| S3-5 | PTA screen refresh: per-finalist NANOGrav band comparison (reformat g2_3/g2_4 per candidate — absorbs old D-5 dossier task). | Haiku | `d5_observatory_dossier.json` |
| S3-6 | Public site update (`DarkMatterK3-Home.github.io`): honest status page — what is established (H1 partial, H2), what failed (kernel-blind observable), what volunteers are now testing. **HUMAN sign-off before publishing** (external communication rule). | HUMAN + Haiku draft | PR reviewed by user |

**Stream-3 gate (HUMAN): GATE-X** — no volunteer job dispatch and no public-site claims until GATE D-1v2 (Stream 2) passes and the S3-1/S3-2 protocol is live.

---

## 7. Cross-stream interfaces (typed artifacts, one direction each)

```
Stream 2 ──(certified sequences: Lean recurrences + OEIS self-verification)──▶ Stream 1  [S1-2]
Stream 2 ──(exact singular loci 1/27, 1/16 = discriminant predictions)──────▶ Stream 1  [S1-4] & Stream 3 [S3-1]
Stream 2 ──(preregistered observable + decision rules)──────────────────────▶ Stream 3  [S3-1, S3-4]
Stream 3 ──(quorum-replicated empirical verdicts)───────────────────────────▶ Stream 1 (empirical axioms w/ artifact hashes) & Stream 2 (F1–F5 scoreboard)
Stream 1 ──(Kodaira type of each degeneration = what a "spike" should look like)─▶ Stream 2/3 observable design
```

Every interface artifact is a committed file with a hash referenced on the receiving side — never a prose claim (Rule 1/Rule 4).

---

## 8. Standing rules (inherited, binding on all three streams)

1. **Rule 1 (real arithmetic):** numbers come from executed committed code, never hand-typed. Sequence arrays are always computed + self-verified (the c704833 lesson).
2. **Rule 4 (honest reporting):** "verified/compiles/discovery" requires the verification artifact in the same commit; `lake env lean` exit-0 output pasted for every Lean claim.
3. **Reproducibility:** every headline number regenerates from one committed command; `cross_consistency_check.sh` enforces in Stream 2; Streams 1/3 get equivalent CI.
4. **No physics-washing in Lean:** theorems state mathematical facts; physics interpretations are manuscript hypotheses (Stream 1 axiom naming: `empirical_` = reproducible artifact-backed, `hypothesis_` = not yet).
5. **Preregistration:** discriminating statistic + decision threshold committed before any comparative run (Stream 3 inherits via `statistic_hash`).
6. **External communication = HUMAN-only:** volunteer-facing pages, GitHub issues to other repos, outreach.
7. **The word "discovery"** is reserved for p < 1e-3 in both mock families under a kernel-swap-passing observable, quorum-replicated.

---

## 9. Sequencing & immediate next actions

```
        Stream 1 (Theory)          Stream 2 (K3 Selection)        Stream 3 (Experimentation)
NOW:    S1-1 axiom hygiene         S2-1 observable redesign ★     S3-1 job schema
        S1-2 import D-2.4 loci     S2-2/S2-3 (D-2.1, D-2.2)       S3-2 quorum protocol
THEN:   S1-3 base geometry Lean    S2-4 true-K3 certification     (wait on GATE D-1v2)
        S1-4 Kodaira types         S2-5 AutoEvolve w/ new gate
GATE:   GATE-T (axiom review)      GATE D-1v2 (HUMAN) ────────▶   unfreezes S3-3/S3-4 dispatch
LAST:   S1-5 manuscript            S2-6 = D-3 reruns              S3-5 PTA, S3-6 public site
                                          └──────────── GATE-E (HUMAN): publication decision
```

★ **S2-1 (observable redesign) is the critical path for the entire program:** H3 and both experiment streams are blocked until an observable exists that passes the kernel-swap battery. Streams 1 and 2-theory proceed in parallel regardless.

**This plan deliberately does NOT:** assume any prior Δ statistic survives; publish anything externally before GATE-X/GATE-E; claim the Dual-Scale Model is favored — it builds machinery that can favor **or kill** it (s₁₀ challenger + random-control kernel remain the falsification scissors).

---

## 10. Recommendations (Fable session, 2026-07-16)

**R1 — Spend the next unit of effort on S2-1, and nothing empirical before it.** Every downstream deliverable (D-3, Stream-3 dispatch, H3) is gated on an observable that survives the kernel-swap battery. The singular-locus-proximity design is the only candidate with a *structural* reason to be kernel-specific: 1/27 ≠ 1/16 enters the statistic directly. Preregister the pass thresholds in a commit *before* writing the observable code.

**R2 — Fix Stream 1's axiom hygiene before any publicity of "0 sorry".** A 0-sorry Lean development is only as strong as its axioms, and `pipeline_upper_bound` (S₁,₂ ≤ 1.177) currently encodes a number the audit classified as non-reproducible (A7). Either demote it to `hypothesis_` or wait for the S3-3 quorum re-run. Conversely, the D-2.4 loci are exact rationals — *prove* them in Lean rather than axiomatizing (net axiom count goes down, which is a better headline than "0 sorry").

**R3 — Get an independent check on the D-2.4 loci as part of S2-4.** The 1/27 and 1/16 values were derived in-repo via the θ-translation (with one index-shift bug already caught). Cooper's level-7/level-10 operators exist in the literature (AESZ/Cooper 2012 tables); matching the in-repo operators against published ones both certifies "true K3" (H1) and independently validates the loci the whole observable redesign rests on. One task, two closures.

**R4 — Treat the kernel-blind negative result as a publishable asset.** GATE D-1.3 (r = 1.0000 between a K3 kernel and noise) is a clean methodological finding about FFT-contrast statistics on density fields — exactly the negative-results-first material Part VIII was designed for. Publishing it costs nothing and armors the program's credibility before any positive claim.

**R5 — Preregister *which kernel predicts what* before looking at data.** s₇'s physical locus (z = 1/27 ≈ 0.037) sits at lower modulus than s₁₀'s (z = 1/16 = 0.0625), so s₇ predicts response steepening at a *lower* critical density under any monotone z(ρ) map. Translate both loci into ρ_crit bands under the S2-3 (a,b) family and commit the two predicted signatures before any data run. If the data later prefers one, the claim is only as strong as this preregistration.

**R6 — Keep one source of truth for sequences across all three repos.** `k3_kernel_engine.py` (compute + self-verify against Lean recurrence and OEIS b-file) is the c704833 lesson made mechanical. Stream 1 should reference its artifact hashes; Stream 3 clients should vendor it pinned by `statistic_hash` — never re-implement or hardcode terms.

**R7 — Unify CI across the three repos.** This repo has `cross_consistency_check.sh` (28 checks + real `lake build`); the LeanProposal repo and the DarkMatter@Home infra have no equivalent yet. Minimum: LeanProposal CI = `lake build` + sorry-grep + axiom-inventory diff; Stream 3 CI = schema validation + quorum-protocol tests. A vision spanning three repos is only as rigorous as its weakest CI.

**R8 — Budget realistically by tier.** The plan is ~70% Haiku-executable (schemas, sweeps, CI, `decide` proofs), ~25% Sonnet (S2-1 design, S2-4 identification, S1-4 Kodaira, derivations), ~5% HUMAN (four gates + anything public). The two tasks where a cheap model *will* produce false confidence are S2-1 (statistics design) and S1-4 (Kodaira classification) — route those to Sonnet-or-better and require pasted verifier output per Rule 4.

*Drafted 2026-07-16 (Fable session) after auditing all three repositories. Stream-2 detail remains governed by `K3xT2_DEEP_IMPROVEMENT_PLAN.md`; Phase 8.E tasks in `TODO.md` are absorbed into Stream 3.*
