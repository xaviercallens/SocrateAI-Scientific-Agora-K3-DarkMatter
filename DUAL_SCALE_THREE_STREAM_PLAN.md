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

## 5. Stream 2 — K3 Selection (this repo: AutoEvolve + gate machinery + MVM matching)

**Tier routing:** Haiku = mechanical/binary-checkable; Sonnet = derivations + non-decide Lean; **T0 = C3b criterion definition + MVM observable design**; HUMAN = gates.

**Architecture update:** Phase 0 introduces A-SEQ, A-VOL, A-ONT, A-REL as load-bearing assumptions; S2-01 now includes **C3b (Shioda-Inose moduli map)** as a new hard criterion; S3-00 (MVM matching) becomes the true "observable design" — it must derive the P1/P2 predictions from geometric data under assumptions, not from phenomenological guessing. **The existing gate sequence (R-0 → D-1 → D-2 → D-3 → GATE-E) now feeds into the MVM calculation, not to independent empirical tests.**

**Achieved:** GATE R-0 ✅ (c3a1b37) · fabricated-array fix + self-verifying kernel engine ✅ (40f2151) · GATE D-1.3 kernel-swap verdict ✅ (F1_FAILS_KERNEL_BLIND) · GATE D-2.4 exact singular loci ✅ · CI 28/28 incl. real `lake build` of the 3 finalists.

**Backlog (revised priority, critical path first):**

| ID | Task | Tier | Validation | Blocking |
|---|---|---|---|---|
| **P0-A** | **Phase 0 gate:** Formalize ASSUMPTIONS.md with A-SEQ, A-VOL, A-ONT, A-REL | T0 + T1 | `ASSUMPTIONS.md` complete; assumption IDs grep-able; CI consistency check | **BLOCKS everything; must complete before S2-01 freeze** |
| **S2-01b** | **Implement C3b checker** (`check_C3b_moduli_map.py`): per-candidate Shioda-Inose relation. Construct F explicitly (q-series or algebraic), validate to order N symbolically, emit certificate JSON. Golden tests required (known-good pair; known-bad pair with no F). | Sonnet design / Haiku test | Checker passes both controls; agrees with S1-04 Sym² data on top candidates | **Blocks S2-03/S2-04 ranking; gates candidate identification for MVM** |
| **S2-1** | **Observable redesign** (now S3-00 domain, but S2's contribution is the **singular-locus fingerprint as the C3b-validated discriminant**): ensure S3-00's P1/P2 observables can distinguish s₇ from s₁₀ via the exact loci (1/27 vs 1/16). Preregister r(s7, random) < 0.5 AND r(s7, s10) < 0.95 on mocks before any real-data run. | Sonnet design / Haiku run | `data/k3t2/d1_3b_c3b_kernel_swap_v3.json`; rule committed before code | Gates S3 observable validity |
| S2-2 | D-2.1: one m_eff(Δ) law (resolve exp(kΔ) vs (1+κΔ)^{1/4}; identify n in m_eff ∝ ρ^{(n+2)/(2n+2)}). **Required for S3-00 step 1 (m_φ derivation).** | Sonnet | `docs/derivations/meff_delta_law.md` + Taylor test; used in MVM | Input to MVM |
| S2-3 | D-2.2: ρ_b → z as a 2-parameter family z(ρ; a, b), marginalized downstream. **Sensitivity grid on S2-1 verdict + S3-00 kill-condition test.** | Sonnet | API change + sensitivity table | Input to S3-00 kill-condition |
| S2-4 | **True-K3 certification** (H1 closure; R3 from recommendations): match s₇/s₁₀ a_p tables to weight-3 newforms (LMFDB); independently validate D-2.4 loci. **Double-closure task: C3b validation + H1 proof.** | Sonnet | `data/autoresearch_v2/k3_identification.json` + LMFDB a_p match + independent-loci derivation | Strengthens C3b + MVM credibility |
| S2-5 | AutoEvolve continuation: extend sweep with C3b as a hard gate (candidate fails C3b ⇒ F1 removal, no score). Survivors classified by (ODE order, integrality, C3b grade). | Haiku | survivors JSON + C3b status table | Feeds S2-04 report |
| S2-6 | D-3 empirical reruns (**FROZEN until S3-00 MVM pins P1/P2 observables**): 35-sector sweep, tomography, TDA-β₁. Now scoped as *verification* of S3-00 predictions, not discovery. | Haiku/Sonnet | per-table artifacts matching S3-00 prediction structure | **Unfrozen only after GATE M1** |

**Stream-2 gate (HUMAN): GATE D-1v2** — (1) C3b checker validated on top pair; (2) singular-locus kernel-swap battery passed; (3) S2-04 SelectionReport complete with assumption tags and C3b grades. **Only this pass unfreezes S3-00 and identifies the candidate pair for MVM.**

---

## 6. Stream 3 — Experimentation (MVM Matching + DarkMatter@Home Validation)

**Repos:** this repo (S3-00 MVM derivation), `DarkMatterK3-Home.github.io` (volunteer-facing), `SocrateAI-Scientific-Agora-Home` (server/API infra) · **Tier:** T0 (S3-00 MVM derivation), Haiku (protocol/mechanical), HUMAN (external communication)

**Architecture update:** S3-00 (MVM matching) is now the **foundational task** — it is what S3-01–S3-06 serve. The MVM calculation derives P1 (PTA ultralight) and P2 (lensing shape) observables under [A-SEQ, A-VOL, A-ONT, A-REL]; S3-01–S3-04 then **test those predictions** against public data. S3-00 output is the pre-registered prediction hash; timestamp audit ensures prediction ≤ data contact.

**Achieved:** pilot run infrastructure exists (327,918-galaxy run, K3-DISC-0003) — but per A7 its outputs are **not reproducible from committed artifacts** and per D-1.3 its statistic was kernel-blind. Stream 3's foundational job is therefore *MVM derivation + re-foundation, not expansion*.

**Backlog (revised, gates included):**

| ID | Task | Tier | Validation | Blocked By |
|---|---|---|---|---|
| **S3-00** | **(GATE M1)** Minimal Viable Matching (MVM): derive P1/P2 observables. See EXECUTION_PLAN §4 S3-00 for full spec: (1) Free-Parameter Ledger install; (2) m_φ(𝒱, g_s) from period data; (3) α_D, Λ_D(𝒱, g_s) from C2 Kodaira + RG; (4) eliminate (𝒱, g_s) or trigger kill condition; (5) tag predictions with [A-SEQ, A-VOL, A-ONT, A-REL]; (6) T0 derives, T0s blind re-derives, both agree. **This is the gate itself — no downstream work until M1 passes.** | **T0 derives + T0s blind re-derives** | Both agree within tolerance; numbers committed hash-pinned; timestamp clean; DERIVATION_DISPUTES.md empty or resolved | GATE D-1v2 (C3b + top candidate pair) |
| S3-1 | (=DM-1) Job spec schema: `{survey_tile, statistic_hash, candidate_id ∈ {cooper_s7, cooper_s10, t103, random_control}, seed, client_version}`. The `statistic_hash` pins the **P1/P2 observables** derived in S3-00 — **no job runs a generic statistic.** | Haiku | schema JSON + validator test | GATE M1 |
| S3-2 | (=DM-2) Quorum replication: ≥2 independent clients per tile; disagreement → quarantine. **Every job batch includes blinded random_control kernels** so kernel-blindness is monitored continuously in production. | Haiku | protocol doc + server test | S3-1 |
| S3-3 | (=DM-3) Re-run the v1 headline coordinates (S₁,₂, K3-DISC-0003 locus) under quorum with the S3-00 observables. Preregistered framing: these are **target coordinates to re-test, not numbers to match**. Archive the run so A7 closes. | Haiku | quorum artifacts committed; A7 struck | GATE M1 + S3-2 |
| S3-4 | (=DM-4) Dispatch the D-3 sweep (S2-6) as volunteer jobs: SDSS DR17 sectors, Euclid tiles when available, both s₇ and s₁₀ kernels + control. **Test the P1/P2 predictions from S3-00 at scale.** | Haiku | dispatch log + quorum results | GATE M1 + S3-2 |
| S3-5 | Prediction comparison: per-finalist PTA band test (P1 channel if selected), lensing profile test (P2 channel if selected). Reformat results per S3-00 observable structure. | Haiku/Sonnet | Test/FIT labels honored; assumption tags preserved; results table | GATE M1 |
| S3-6 | `OBSERVATIONAL_REPORT.md` assembly: machine tables (S3-04/S3-05 results) + T0-written interpretation. F3/F4/F5 branches triggered mechanically. **Report published even if all results are exclusions.** | T1 assembles; T0 writes interpretation | Report + branch triggers | S3-5 complete |
| S3-7 | Public site update (`DarkMatterK3-Home.github.io`): honest status page — what's established (H1 partial, H2), what failed (old FFT), what volunteers validated (S3-00 predictions). **HUMAN sign-off before publishing.** | HUMAN + Haiku draft | PR reviewed by user | S3-6 complete + GATE M3 |

**Stream-3 gate (HUMAN): GATE M1 (MVM pin)** — S3-00 complete; T0 ↔ T0s agreement; predictions hash-pinned; kill-condition evaluated.  
**Stream-3 gate (HUMAN): GATE-X (dispatch authorization)** — after GATE M1, S3-1/S3-2 protocols live; volunteer jobs dispatch; no public claims until results (S3-03/S3-04) are in quorum.

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

## 9. Sequencing & Critical Path (Revised for MVM Architecture)

**Critical path (blocks G1/M1, everything else):**
```
P0-A (ASSUMPTIONS.md) 
  ↓ [blocks S2-01]
S2-01 (K3_CRITERIA.md v1.0 + C3b definition) 
  ↓ [requires C3b checker]
S2-01b (implement check_C3b_moduli_map.py + golden tests) 
  ↓ [blocks S2-03/S2-04 ranking]
S2-03/S2-04 (AutoEvolve + ranking, identify top C3b-passing pair) 
  ↓ [blocks S3-00]
S3-00 (MVM derivation: m_φ, α_D, Λ_D, P1/P2 observables, kill-condition) 
  ↓ [T0 derives, T0s blind re-derives]
  GATE M1 (agreement + timestamp audit + assumption tags clean)
  ↓ [unfreezes empirical dispatch]
S3-1/S3-2 (volunteer protocol), S3-03/S3-04 (prediction validation)
```

**Parallel streams (do NOT block critical path):**
```
Stream 1:                          Stream 2 (non-critical):       Stream 3 (non-critical):
S1-1 axiom hygiene                 S2-2 m_eff(Δ) law              S3-5 per-candidate PTA
S1-2 import D-2.4 loci             S2-3 ρ_b → z mapping           S3-6 observational report
S1-3 base geometry Lean            S2-4 true-K3 certification     S3-7 public site (wait on GATE M3)
S1-4 Kodaira types                 S2-5 AutoEvolve w/ C3b gate
GATE-T (axiom review)              S2-6 D-3 reruns (frozen until GATE M1)
S1-5 manuscript                    
```

**Original recommendation R1 updated:** The critical path is now **P0-A → S2-01b (C3b checker) → S2-04 (ranking) → S3-00 (MVM)**. Every gate M1-blocking task is T0-tier (architecture, physics derivation, or verifier-first-dependent). S2-1 (observable redesign) is now **no longer independent**; it is consumed by S3-00's P1/P2 design.

**This plan deliberately does NOT:** assume any prior Δ statistic or PTA signature survives; assume C3b will pass for any candidate (failure → F1); assume the MVM calculation will yield a pinned observable (no relation → F5, and that is a reportable result); assume any assumption in [A-SEQ, A-VOL, A-ONT, A-REL] is unbreakable (adversarial passes explicitly attempt to break them); publish anything externally before GATE M1 + GATE-X/GATE-E; claim the Dual-Scale Model is favored — it builds machinery that can favor **or kill** it (s₁₀ challenger + random-control kernel remain the falsification scissors, now applied to P1/P2 predictions).

---

## 10. Recommendations (Updated for Phase 0 + MVM Architecture)

**R1 — Complete Phase 0 (P0-A/B/C/D) before any S2-01 freeze.** ASSUMPTIONS.md is now load-bearing: every prediction carries an assumption-list tag; every criterion definition may reference one. The Free-Parameter Ledger schema is the contract between S2 (candidate selection) and S3 (MVM derivation). The abstract-tier rule (epistemic-guardrails update) must be live in all three repos before any public prose. Start with P0-A; it unblocks everything.

**R2 — Implement C3b checker (S2-01b) as a critical-path blocker, not optional.** The Shioda-Inose moduli map F is the T0 Architecture Review's centerpiece: it is the *honest version* of the Desk's "rigid locking" claim, downgraded from asserted theorem to checkable per-candidate criterion. C3b failure → candidate removal (F1). C3b success → the pair is qualified for MVM matching. **Do not proceed to S2-04 ranking or S3-00 derivation until C3b checker is golden-test-passing and validated on at least one candidate pair.**

**R3 — Perform blind re-derivation (S3-00 step 6) as the T0/T0s gate for M1, not as optional review.** The T0 Architecture Review mandates two-model independent derivation of the MVM steps 1–4. This is not a review (where the second model reads the first's answer); it is re-derivation from geometric data + literature only. Disagreement → DERIVATION_DISPUTES.md; unresolved disputes block M1. This is your insurance that the calculation is not a story told twice.

**R4 — Tag every prediction in S3-00 with [A-SEQ, A-VOL, A-ONT, A-REL].** Do this at write time, not post-hoc. The tags are machine-auditable; CI must check that every quantity in the Free-Parameter Ledger and every observable (P1, P2) carries the correct assumption list. If an assumption's discharge path indicates it could fail (e.g., A-SEQ failure ⇒ light field found), the entire result set is void. Audit this before M1 pin.

**R5 — Preregister the kill condition (S3-00 step 4) in a commit before deriving it.** If no relation survives the (𝒱, g_s) elimination, the model is generic vdSIDM and triggers F5 (false positive). State the exact threshold, the test statistic, and the expected result of the calculation before you calculate it. This is your hedge against unwitting post-hoc tuning.

**R6 — Treat the C3b test as the new adversarial standing item (beyond A-SEQ and A-REL).** Deep Think's S2-05 adversarial pass must explicitly attempt: (1) to find a light field A-SEQ missed; (2) to find a production history that back-reacts on σ(v); (3) to find a candidate pair where C3b "passed" but F is actually disconnected or multivalued. Unanswered breaks → block GATE D-1v2.

**R7 — Keep one source of truth for sequences, and extend to assumptions.** `k3_kernel_engine.py` (compute + self-verify) plus `ASSUMPTIONS.md` (define once, reference everywhere). Stream 2 exports assumption-tagged certificates; Stream 1 receives them as-is; Stream 3 clients receive them pinned by `statistic_hash`. Never re-specify or hardcode an assumption downstream.

**R8 — Unify CI across the three repos, and add assumption-audit CI.** This repo's CI must now include: (1) assumption-tag audit (every quantity in PREDICTION.md + K3_CRITERIA carries correct tags); (2) C3b gate test (candidate fails C3b ⇒ score = null); (3) TUNING_LOG audit (every change to assumption lists is logged). LeanProposal: `lake build` + sorry-grep + axiom-inventory diff + assumption-import audit. Stream 3: schema validation + quorum-protocol tests + P1/P2 observable hash check. A vision spanning three repos is only as rigorous as its weakest audit.

**R9 — Budget realistically by tier (updated for MVM).** Plan is ~60% Haiku (schemas, sweeps, CI, checkers on golden data), ~30% Sonnet (S2-01b C3b derivation, S2-4 identification, S1-4 Kodaira, m_eff/ρ_b laws), ~5% T0 (C3b design, MVM derivation, adversarial adjudication), ~5% HUMAN (five gates + external comms). **T0 tasks non-negotiable: (1) C3b criterion definition (S2-01), (2) MVM matching derivation (S3-00), (3) adversarial adjudication (S2-05), (4) blind re-derivation agreement (S3-00 step 6), (5) all M-gate sign-offs.** No cheap model will produce confident-sounding wrong physics here; the verifier is the gate.

*Drafted 2026-07-16 (Fable session) after auditing all three repositories. Stream-2 detail remains governed by `K3xT2_DEEP_IMPROVEMENT_PLAN.md`; Phase 8.E tasks in `TODO.md` are absorbed into Stream 3.*
