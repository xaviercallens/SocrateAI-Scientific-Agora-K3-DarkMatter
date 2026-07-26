# Stream 2 — AutoEvolve K3 Selection: Haiku Implementation Plan (v1.0)

**Date:** 2026-07-26
**Branch:** `feat/stream2-autoevolve`
**Status:** PLAN ONLY — no implementation in this PR. Implementation authorized only after T0 sign-off on this document.
**Owner:** Stream 2 (K3 Selection & Lattice) · **Executor tier:** HAIKU (~90%), SONNET escalation points marked, 2 HUMAN gates.
**Tracker linkage:** `PROJECT_STATUS_TRACKER.md` task **S2-5 (AutoEvolve extended)**; `DUAL_SCALE_THREE_STREAM_PLAN.md` §5 row S2-5.
**Replaces:** `scripts/auto_evolve_k3_selection_stub_tobeupdate.py` (stub) when implemented.

> Epistemic tags: **[A]** established/certified math · **[B]** checkable but unproven ·
> **[C]** physical interpretation (in-sentence conjecture marker mandatory).
> All numbers emitted by this pipeline must trace to a checker certificate (Rule 1 / No-Simulation).

---

## 0. Objectives (user-directed Stream 2 scope)

1. **"Train" AutoEvolve on Cooper s₇ / s₁₀ / S₂₂** — build an exact-arithmetic *anchor
   fingerprint library* from the three certified K3-type sequences (A183204, A005260,
   A005259). "Training" here is **not** ML fitting: per the No-Simulation rule, it is the
   deterministic extraction of exact discriminating invariants (ODE order/degree,
   mirror-map integrality, singular loci, Sym²-root existence) that the evaluator uses
   as the fitness answer key.
2. **Run AutoEvolve to rank K3 candidates** — evolutionary generator + ruthless gate
   evaluator over the binomial-sum landscape, producing a scored, certificate-backed
   ranking per `K3_CRITERIA_INTERFACE.md` (60/30/10 weights).
3. **Align K3 with Elliptic EFTs** — for every ranked K3 survivor, attempt the C3b
   symmetric-square decomposition L₃ = Sym²(L₂) and emit the order-2 elliptic partner
   certificate `PASS(N)`. **[C]** *We conjecture* the Sym² relation corresponds to a
   Shioda–Inose structure; no physical bulk↔brane coupling is claimed absent a worked
   EFT matching (binding constraint, `briefs/PHASE_10_K3_SELECTION.md` §4).

## 0.1 Design inspiration (what we copy, what we refuse)

**From AlphaEvolve (Google DeepMind):**
- Cheap generator + rigorous automated evaluator loop; the evaluator is the science.
- Archive of elites: keep the best candidate *per niche* (family type × ODE order),
  not just a single global best — preserves diversity across generations.
- Mutation operators applied to a structured genome (here: exponent tuples and
  binomial-factor templates), never free-form code mutation.
- Hard gates as fitness cliffs: a candidate failing a certificate gate scores 0, no
  partial credit (C3b failure ⇒ F1 removal, no score — per S2-5 spec).

**From Karpathy-style auto-research (nanoGPT ethos):**
- One small, single-file, dependency-light driver per stage; no framework.
- Fully deterministic: fixed integer seeds, exact rational arithmetic, no floats in
  any gate decision; two runs must be byte-identical.
- Log everything to plain JSON/CSV artifacts; every claim greppable to a file+line.
- Small iterations: each generation is independently resumable and inspectable.

**What we explicitly refuse:**
- No neural nets, no gradient training, no stochastic scoring (No-Simulation rule).
- No empirical-fit scoring from the A4/A7-defective V4C/SDSS pipeline: the 30%
  "Empirical Fit" weight is emitted as `null` until Stream 3 DM-3 quorum data exists.
- No ρ / T / Kodaira-label emission anywhere in this pipeline while **E-009** is open
  (`briefs/STREAM2_ACTION_PLAN_2026_07_26.md`): lattice fields are hard-`null`.

---

## 1. Architecture

```
                       ┌─────────────────────────────┐
                       │ AE-1 Anchor Fingerprints     │
                       │ (s7, s10, S22 + controls)    │
                       └──────────────┬──────────────┘
                                      │ answer key (JSON)
┌──────────────┐   genomes   ┌────────▼─────────┐   certificates   ┌───────────────┐
│ AE-2         │────────────▶│ AE-3 Gate Battery │────────────────▶│ AE-4 Ranker    │
│ Generator    │◀────────────│ (G1-1, G1-3, C3b) │                 │ (60/30/10)     │
│ (mutate/     │  survivors  └────────┬─────────┘                  └───────┬───────┘
│  archive)    │  feed next gen       │ K3 survivors                       │ ranked list
└──────────────┘                      ▼                                    ▼
                          ┌───────────────────────┐            ┌───────────────────────┐
                          │ AE-5 Elliptic-EFT      │            │ AE-6 Reports           │
                          │ alignment (Sym² root,  │            │ (K3_SELECTION_REPORT,  │
                          │ PASS(N) certificates)  │            │  JSON artifacts)       │
                          └───────────────────────┘            └───────────────────────┘
```

**Reused existing code (do not rewrite):**
- `scripts/autoresearch_v2_phase_a_scan.py::classify` — exact ODE-order classifier (G1-1).
- `scripts/autoresearch_v2_phase_b_all_gates.py` — minimal-operator mirror-map integrality (G1-3).
- `checkers/check_C3b_symsqrt.py` — constructive Sym²-root extraction + verification.
- `scripts/autoresearch_v2_pool.py::POOL` — frozen candidate pool (read-only).
- `scripts/autoresearch_v2_alphaevolve.py` — v1 neighborhood sweep (superseded by AE-2 but kept as regression baseline).

**New files (implementation phase, not this PR):**
| File | Stage |
|---|---|
| `scripts/auto_evolve_k3_selection.py` | AE-2/3/4 driver (replaces the `_stub_tobeupdate` file) |
| `scripts/ae_anchor_fingerprints.py` | AE-1 |
| `scripts/ae_elliptic_alignment.py` | AE-5 |
| `tests/test_autoevolve_stream2.py` | AE-7 golden tests |
| `data/autoresearch_v2/autoevolve_stream2_config.yaml` | frozen config (in this PR) |

---

## 2. Task breakdown (Haiku work orders)

Every task below is written to be executable by a low-tier model in a single session
with **no design decisions required**. If a step forces a design decision, that is an
escalation trigger (see §4).

### AE-0 — Preflight `[HAIKU]`

- **Inputs:** repo at `feat/stream2-autoevolve`; `requirements.txt`.
- **Steps:** verify `python -c "from scripts.autoresearch_v2_phase_a_scan import classify"`;
  verify `data/autoresearch_v2/candidate_pool.yaml` has `frozen: true`; verify
  `checkers/check_C3b_symsqrt.py` runs its self-test.
- **Definition of Done (DoD):** a `data/autoresearch_v2/ae_preflight.json` with each
  check `PASS`/`FAIL` and exact commands used.
- **Test case:** re-running preflight twice produces identical JSON (determinism smoke).
- **Validation:** `python scripts/ae_preflight.py && git diff --exit-code data/autoresearch_v2/ae_preflight.json` (second run).

### AE-1 — Anchor fingerprint library ("training") `[HAIKU]`

- **Inputs:** exact term generators for the 3 anchors + 2 controls:
  - Anchors (positive): `cooper_s7` (A183204), `cooper_s10` (A005260), `S22` (A005259).
  - Controls: `A005258` (S₂₁, elliptic — **negative** control), `A005259` doubles as
    the literature-certified **positive** control (Beukers–Peters 1984).
- **Steps:** for each sequence compute, in exact ℚ arithmetic, nmax ≥ 110:
  1. minimal generating-function ODE (order, degree) via `classify`;
  2. mirror-map coefficients q₁..q₃₁ + integrality verdict (minimal operator only);
  3. singular loci of the ODE symbol polynomial (exact rationals);
  4. Sym²-root existence via `check_C3b_symsqrt.py` → `PASS(N)`/`FAIL`;
  5. held-out recurrence check (≥ 70 held-out terms, residual exactly 0).
- **Output:** `data/autoresearch_v2/ae_anchor_fingerprints.json` — one record per
  sequence with all five invariants + provenance (script, commit, date).
- **DoD:** controls reproduce the literature answer key exactly:
  A005259 → ODE order 3, q₂ = 12, integral; A005258 → ODE order 2 (elliptic);
  s7 loci = {1/27, −1}; s10 loci = {1/16, −1/4} (confirmed values,
  `briefs/STREAM2_ACTION_PLAN_2026_07_26.md` §B). Any mismatch ⇒ HALT + negative-first report.
- **Test cases:**
  - T1.1: `q2(A005259) == Fraction(12)`; T1.2: `ode_order(A005258) == 2`;
  - T1.3: `s7 loci == [Fraction(1,27), Fraction(-1)]`;
  - T1.4: fingerprint JSON contains **zero** float literals (regex `\d\.\d` scan, excluding provenance timestamps).
- **Validation:** `pytest tests/test_autoevolve_stream2.py -k anchor -q`.

### AE-2 — Evolutionary generator `[HAIKU]`

- **Genome:** `(family, exponents)` where family ∈ {2-factor `C(n,k)^A C(n+k,k)^B`,
  3-factor `… C(2k,k)^C`, 4-factor `… C(2(n−k), n−k)^D`} and exponents are small
  non-negative integers (bounds in config YAML).
- **Mutation operators (exhaustive, deterministic order):** ±1 on one exponent;
  family promotion (append factor with exponent 1); factor swap. No crossover in v1.
- **Selection:** archive-of-elites keyed by `(family, ode_order)`; a genome enters the
  archive iff it passes G1-1 with ODE order 3 AND is not equivalent to an existing
  member under the trivial-transformation dedup rule (identical first 20 terms after
  constant scaling — same rule as LR-6).
- **Budget:** ≤ 3 generations, ≤ 400 genome evaluations total (config-capped);
  term computation nmax = 110, held-out ≥ 70 terms mandatory for any survivor claim.
- **Output:** `data/autoresearch_v2/ae_gen_archive.json` (all evaluated genomes with
  verdicts), `ae_gen_survivors.json` (K3-type survivors only).
- **DoD:** (a) re-running with the same config is byte-identical; (b) the v1 sweep
  survivors in `alphaevolve_gen_survivors.json` are all rediscovered (regression);
  (c) every survivor logs a held-out residual of exactly 0.
- **Test cases:**
  - T2.1: seeding the generator with `(2,2)` alone rediscovers A005259 in gen 0;
  - T2.2: no survivor has ODE order ≠ 3;
  - T2.3: dedup — `(A,B) = (2,2)` mutated to itself is not double-archived.
- **Validation:** `python scripts/auto_evolve_k3_selection.py generate --config data/autoresearch_v2/autoevolve_stream2_config.yaml` then `pytest -k generator -q`.

### AE-3 — Gate battery integration `[HAIKU]`

- **Gates, in order (fail ⇒ stop, score 0, record reason):**
  1. **G1-1** ODE order = 3 on the *minimal* operator (reuse `classify`);
  2. **G1-3** mirror-map integrality on the *minimal* operator, 31 coefficients
     (the S₁₂ q₂ = 81/8 false-positive taught us: never the shift operator);
  3. **C3b hard gate** — Sym²-root extraction must return `PASS(N)` with N ≥ 24
     (per S2-5: "candidate fails C3b ⇒ F1 removal, no score").
- **Output:** per-candidate certificate JSON under `data/certificates/ae/`
  (schema in §3), plus a battery summary `ae_gate_battery.json`.
- **DoD:** anchors pass all three gates; A005258 control fails G1-1 (order 2) and is
  recorded as `CONTROL_EXPECTED_FAIL`, not as an error.
- **Test cases:**
  - T3.1: s7 battery result is `PASS, PASS, PASS(≥58)` (matches existing
    `data/certificates/C3b_symsqrt_*.json`);
  - T3.2: injecting S₁₂ (A112019) yields G1-1 FAIL with reason `ode_order=2`;
  - T3.3: certificate JSON validates against the schema (jsonschema check).
- **Validation:** `pytest -k gate_battery -q`.

### AE-4 — Ranking `[HAIKU]`

- **Scoring (per `K3_CRITERIA_INTERFACE.md`):**
  - Mathematical Rigor, weight 0.60 — from gate certificates only:
    order-3 (0.25) + holonomic held-out pass (0.15) + Sym² structure `PASS(N≥24)` (0.20).
  - Empirical Fit, weight 0.30 — **emitted as `null` with reason
    `BLOCKED_ON_DM3_QUORUM`** (A4/A7 defects; no V4C numbers may be consumed).
    Ranking therefore reports both `score_math_only` (renormalized to /0.70) and a
    `score_total = null` placeholder.
  - Theoretical Consistency, weight 0.10 — Swampland/F-theory flags copied verbatim
    from existing gate outputs (`g2_2_no_go_status.json` keys) where present, else `null`.
- **Output:** `data/autoresearch_v2/ae_ranking.json` + human-readable table appended
  to `reports/K3_SELECTION_REPORT.md` (marked `Generated-by: Haiku`, tier-tagged).
- **DoD:** ranking is a pure function of certificate files — deleting all
  certificates and re-running gate battery reproduces the identical ranking;
  s7, s10, S22 appear in the ranking with `score_math_only = 0.60/0.70` each or a
  documented, negative-first explanation of any deviation.
- **Test cases:**
  - T4.1: candidate with C3b FAIL has `score_math_only = 0` and `rank = null`;
  - T4.2: `empirical_fit` is `null` for every candidate (no exceptions);
  - T4.3: ranking JSON round-trips: `rank(certs) == rank(rank(certs) inputs)`.
- **Validation:** `pytest -k ranking -q`.

### AE-5 — Elliptic-EFT alignment `[HAIKU, SONNET escalation]`

- **Inputs:** ranked K3 survivors from AE-4; `check_C3b_symsqrt.py`.
- **Steps per survivor:**
  1. extract L₂ = Sym²-root of L₃ (constructive, exact);
  2. verify z(L₂) = z(L₃) (moduli map = identity) and record `PASS(N)`;
  3. verify the operator identity L₃ = Sym²(L₂) symbolically (CAS) — if the CAS
     step exceeds Haiku capability (non-mechanical simplification), **escalate to
     SONNET**, do not approximate;
  4. record the partner recurrence coefficients exactly (the s7 → A279619 and s10 →
     rational-partner rows are the golden references).
- **Hard prohibitions (E-009, standing):** emit **no** Kodaira labels, **no** ρ, **no** T,
  **no** gauge groups. Lattice fields in the certificate are literal `null` with
  `blocked_on: "E-009"`. `exponents_to_kodaira_type()` must never be called
  (scheduled for deletion — `briefs/STREAM2_ACTION_PLAN_2026_07_26.md` §E).
- **[C]** Any prose sentence relating the partner to a Shioda–Inose structure or an
  EFT carries an in-sentence *we conjecture* marker. The deliverable is the operator
  algebra, not physics.
- **Output:** `data/certificates/ae/C3b_<candidate>_partner.json` per survivor +
  `docs/autoresearch_v2/AE_ELLIPTIC_ALIGNMENT.md` summary (tier-tagged).
- **DoD:** golden pair reproduced — s7 partner matches A279619 recurrence
  `(n+1)²fₙ₊₁ = (26n²+13n+2)fₙ + 3(3n−1)(3n−2)fₙ₋₁` exactly; s10 partner matches the
  certified rational partner; both at `PASS(≥58)`.
- **Test cases:**
  - T5.1: s7 golden partner coefficients equality (exact integers);
  - T5.2: g.f.(partner)² == g.f.(L₃ sequence) on all available terms (the Deep Think
    verification, `g.f.(A279619)² == g.f.(A183204)`);
  - T5.3: certificate lattice fields are all `null` (E-009 guard test — this test
    **must fail the build** if anyone emits ρ/T).
- **Validation:** `pytest -k alignment -q`.

### AE-6 — Reports & artifact wiring `[HAIKU]`

- Replace `scripts/auto_evolve_k3_selection_stub_tobeupdate.py` with the real driver;
  update the dangling link in `K3_CRITERIA_INTERFACE.md` §Implementation.
- Append the AutoEvolve section to `reports/K3_SELECTION_REPORT.md` (negative
  findings first, then ranking table, then alignment table).
- **DoD:** every number in the report is greppable to a JSON artifact; no orphan claims.
- **Validation:** `bash scripts/cross_consistency_check.sh` passes (extend it with the
  new artifact paths).

### AE-7 — Tests & CI `[HAIKU]`

- `tests/test_autoevolve_stream2.py` implementing T1.x–T5.x above; all tests use the
  answer-key controls, no network, no floats in assertions.
- Add the pytest file to the existing CI workflow (`.github/workflows/agora-ci-gate.yml`).
- **DoD:** CI green on the branch; test runtime < 10 min on a laptop CPU.

### Gates (HUMAN)

- **GATE AE-α (before implementation):** T0 sign-off on this plan + the frozen config YAML.
- **GATE AE-β (after AE-6):** T0 reviews ranking + alignment report; only then may
  results be cited elsewhere or handed to Stream 3.

---

## 3. Data contracts

**Config (frozen in this PR):** `data/autoresearch_v2/autoevolve_stream2_config.yaml` —
anchors, controls, exponent bounds, budgets, weights, and the E-009 null-lattice policy.
Any change to it after GATE AE-α requires a new T0 sign-off (same rule as the Phase 8 pool freeze).

**Certificate schema (per candidate),** `data/certificates/ae/<id>.json`:

```json
{
  "id": "gen_3f_A1B2C1",
  "genome": {"family": "3factor", "exponents": [1, 2, 1]},
  "terms_sha256": "…",
  "g1_1": {"ode_order": 3, "ode_degree": 4, "held_out_terms": 72, "residual": "0"},
  "g1_3": {"q_coeffs": ["1", "9", "132"], "q2": "9", "integral": true},
  "c3b": {"verdict": "PASS", "order_verified": 58, "partner_recurrence": "…"},
  "lattice": {"rho": null, "T": null, "blocked_on": "E-009"},
  "empirical_fit": null,
  "provenance": {"script": "…", "commit": "…", "config_sha256": "…", "date": "…"}
}
```

All numeric gate values are strings encoding exact rationals (`"81/8"`), never floats.

---

## 4. Guidelines for the low-tier (Haiku) executor — BINDING

1. **Exact arithmetic only.** `int` / `fractions.Fraction` in every gate path. A float
   anywhere in a decision is an automatic task failure.
2. **Never claim bare PASS.** Always `PASS(N)` with the verified order, per
   `briefs/PHASE_10_K3_SELECTION.md` §2.
3. **Negative-first reporting.** Every session report leads with what failed,
   what is unproven, and what was assumed.
4. **Do not touch frozen artifacts:** `candidate_pool.yaml`, existing
   `data/certificates/*_v2.json` (annotate, never delete/edit), `g1_*.json`.
5. **E-009 guard:** never emit ρ, T, Kodaira types, discriminants, or gauge groups.
   If a step seems to require them, STOP and escalate.
6. **No empirical numbers** from V4C/SDSS legacy pipelines (defects A4/A7). The only
   admissible empirical channel is a future DM-3 quorum artifact.
7. **Determinism:** fixed seeds from config; rerun before commit; artifacts must be
   byte-identical (timestamps live only in `provenance`).
8. **One task per session.** Finish DoD + tests, commit with the provenance footer
   `Generated-by / Verified-by / Reviewed-by`, then stop.
9. **Escalation triggers (→ SONNET or T0):** CAS simplification beyond mechanical
   steps; any control mismatch vs the literature answer key; any gate contradiction
   between two scripts; any need to reinterpret geometry; budget overrun > 20%.
10. **Do not "compute toward expected outputs."** Pre-declared expectations are for
    *tests of controls only*; for novel candidates, report what the computation gives
    (this is the E-007/F6 failure mode — twice encountered, zero tolerance).

---

## 5. Execution order & estimates

| Order | Task | Est. | Tier |
|---|---|---|---|
| 1 | GATE AE-α (this PR review) | — | HUMAN |
| 2 | AE-0 preflight | 0.5 h | HAIKU |
| 3 | AE-1 fingerprints | 2 h | HAIKU |
| 4 | AE-7 (tests first, T1.x) | 1 h | HAIKU |
| 5 | AE-2 generator | 3 h | HAIKU |
| 6 | AE-3 gate battery | 2 h | HAIKU |
| 7 | AE-4 ranking | 1.5 h | HAIKU |
| 8 | AE-5 alignment | 3 h | HAIKU (+SONNET on CAS escalation) |
| 9 | AE-6 reports + CI | 1.5 h | HAIKU |
| 10 | GATE AE-β | — | HUMAN |

Total ≈ 14.5 h Haiku + review. CPU budget well under the ≤ 50 CPU-h Phase 8 envelope.

---

## 6. Out of scope (explicit)

- Lean 4 formalization of new survivors (S20-pattern `decide` proofs) — separate task
  after GATE AE-β, Sonnet tier.
- Any Gate E / D-3 interaction — Stream 3 owns those; this plan neither reads from nor
  writes to `data/k3t2/`.
- Resolution of E-009 (Kodaira category question) — T0/Deep Think.
- LMFDB newform matching (S2-4) — Sonnet theory task, independent.

---

**Provenance:** Generated-by: Cascade (plan only, no computation performed) | Verified-by: n/a — plan document | Reviewed-by: [pending T0]
