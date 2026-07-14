# AutoResearch Release v2 — The Hypothesis Foundry
## An evolutionary, gate-driven re-evaluation of the K3 dark-sector hypothesis

**Status:** PROPOSED — NOT YET IMPLEMENTED
**Date:** 2026-07-14
**Executor target:** low-cost LLM (HAIKU-tier) for ~80% of tasks; SONNET+ for derivations; HUMAN at selection gates only
**Inspiration:** AlphaEvolve-style evolutionary program search; karpathy/autoresearch lightweight agentic loops; the agentic-research methodology of arXiv:2506.13131
**Prime directive:** this project's greatest validated strength is not the K3 hypothesis — it is the **validation infrastructure that dismantled most of it** (parameter ledger, CI gates, Rule 1/Rule 4, held-out classifiers, provenance ledger). v2 turns that infrastructure from a shield into an **engine**: a hypothesis foundry where candidates are bred, gated, and either promoted or honestly killed.

---

## 0. Design Thesis: Selection Pressure as Science

AlphaEvolve works because it couples a cheap generator to a ruthless evaluator. We already own the ruthless evaluator. The v2 loop is:

```
                    ┌─────────────────────────────────────────────┐
                    │  GENERATOR (literature + sieve mutation)     │
                    │  → pool of 13 candidate sequences/geometries │
                    └──────────────────┬──────────────────────────┘
                                       ▼
   G0 literature cross-match ──► kill/annotate (known classification wins)
                                       ▼
   G1 exact-arithmetic screen ──► 13 → 5   (corrected order classifier,
                                             held-out validation, Weil, integrality)
                                       ▼
   G2 physics viability      ──► annotate  (mass window WITHOUT circular fit,
                                             GD-1 No-Go, Dolan bare survival)
                                       ▼
   G3 quick data tests       ──► 5 → 3    (SDSS DR17 live, Euclid Q1, PTA window,
                                             Lee–Tsai overlap)
                                       ▼
   G4 deep implementation    ──► top 3    (Lean kernel verification, manuscripts,
                                             external verification invitations)
                                       ▼
   G5 publication + observatory targeting
```

**Anti-circularity is a hard gate, not a guideline** (the GAP-2 lesson): *any parameter fit to its own validation target invalidates the task output automatically.* This is enforceable by a HAIKU-tier check: every fitted parameter must declare its fit target in `PARAMETER_LEDGER.yaml`, and the CI gate fails if a fit target appears in the same task's acceptance criteria.

**Calibration controls with known answers (the answer key insight).** The literature already contains ground truth for our classifier:
- $S_{2,1}(n)=\sum_k\binom{n}{k}^2\binom{n+k}{k}$ is (to be verified in LR-1) the classical **Apéry ζ(2) sequence** (OEIS A005258), whose weight-2 / elliptic-modular association is classical (Beukers). If confirmed, this *independently validates* the GAP-1 reclassification — our pipeline rediscovered a known classification blind.
- The **Apéry ζ(3) sequence** (OEIS A005259) carries a literature-certified K3 association (Beukers–Peters 1984, "A family of K3 surfaces and ζ(3)"). It enters the pool as a **positive control**: if our corrected classifier does not classify it order-3/K3-type, the classifier is broken and everything downstream halts.
- Zagier's six sporadic order-2 sequences serve as **negative controls** (expected elliptic).

A classifier that passes both controls earns the right to classify novel candidates. This is the single highest-value scientific upgrade over v1, and it costs almost nothing.

---

## 1. Phase A — Deep Literature Review → Candidate Pool of 13

All LR tasks are HAIKU-executable: they are retrieval + tabulation with explicit acceptance criteria. Output artifact for the phase: `docs/autoresearch_v2/CANDIDATE_POOL.md` + `data/autoresearch_v2/candidate_pool.yaml` (machine-readable: name, OEIS id, binomial form, literature-assigned geometry + citation, prior status).

| Task | Executor | Content | Acceptance criteria |
|---|---|---|---|
| **LR-1** | HAIKU | Cross-match $S_{1,2}$, $S_{2,1}$ against OEIS + classified Apéry-like literature (Zagier 2009 "Integral solutions of Apéry-like recurrences"; Cooper 2012 sporadic sequences; Almkvist–van Straten–Zagier CY operator tables / AESZ database). Confirm or refute the A005258 ≡ S₂,₁ identification and its weight-2 status. | Table with OEIS ids, first-10-term exact matches, literature citations. Discrepancies reported at top per Rule 4. |
| **LR-2** | HAIKU | Enumerate the classified sporadic pools: Zagier's 6 order-2 sequences; Cooper's order-3 sporadics (s₇, s₁₀, s₁₈ and relatives); Domb numbers (A002895); Almkvist–Zagier order-3 entries; Apéry ζ(3) (A005259); Verrill-type sequences. | ≥15 named sequences with exact binomial-sum forms and literature-assigned geometry. |
| **LR-3** | HAIKU | Extended sieve generation: run the **corrected** `k3_sieve_analysis.py` classifier over $S_{A,B}$, $(A,B)\in[1,8]^2$ (beyond v1's $[1,5]^2$), and the 3-factor family $S_{A,B,C}(n)=\sum_k\binom{n}{k}^A\binom{n+k}{k}^B\binom{2k}{k}^C$, $(A,B,C)\in[0,3]^3$, with held-out validation (≥70 held-out terms, $n_{\max}\ge110$) per the GAP-1-fixed protocol. | Every order-3 survivor logged with held-out residuals = 0 exactly. No survivor claimed without held-out pass. |
| **LR-4** | HAIKU | Archive reference documents: create `docs/reference/`; deposit BibTeX + summary sheets for (i) Lee & Tsai 2026, *Naturally resonant dark matter from extra dimensions*, PRD 114 L011701 — noting honestly that their model is **fermionic DM + dark photon** on $S^1/(Z_2\times Z_2')$ (resonance-enhanced annihilation & self-interaction, axial-vector coupling, direct-detection/accelerator predictions), i.e. a *different particle content* from our axion — the shared structure is the KK resonance geometry, not the particle physics; (ii) El Naschie 2013 (JQIS 3, 23–26) — archived **as a cautionary boundary-marker only**: its transfinite/golden-ratio derivation of $\Omega_\Lambda$ is classified in mainstream literature as non-dynamical numerology, the exact failure mode Paper V explicitly brands itself against. It takes **no load-bearing role**; its function in v2 is to sharpen the falsifiability criterion that separates our programme from that class. | `docs/reference/` populated; each entry has: full citation, 5-line honest summary, epistemic classification (mainstream / speculative / numerology-class), and role-in-v2 statement. |
| **LR-5** | SONNET+ | Lee–Tsai bridge memo: extract their $(R, m_B)$ resonance-mass structure (their Eq. for $m_E^{(n)}$) and their self-interaction/annihilation resonance conditions; map onto our $m_{\mathrm{eff}}(\Delta)$ ansatz; identify which of their direct-detection/accelerator predictions have any overlap with an axionic (rather than fermionic) realization; state where the analogy **breaks** (spin, couplings, relic mechanism). | `docs/reference/lee_tsai_bridge.md` with an explicit "where the analogy breaks" section ≥ as long as the alignment section. |
| **LR-6** | HAIKU + HUMAN sign-off | Score and fix the pool at exactly **13 candidates**: rank by (a) literature-assigned or sieve-confirmed order-3/K3-type status, (b) not previously falsified, (c) known modularity data available, (d) distinctness (no two members related by trivial transformation). Include A005259 (positive control) and one Zagier order-2 (negative control) *inside* the 13. | `candidate_pool.yaml` frozen; HUMAN approves ranking rationale; controls present. |

**Phase A kill criterion:** if LR-1 finds that the $S_{1,2}$ operator itself is a known, already-classified object whose literature classification contradicts K3 (as happened to $S_{2,1}$), that finding goes to the top of every artifact and the pool is rebuilt around the literature's actual K3-class sequences. This would be a *success* of the method, not a failure of the programme.

---

## 2. Phase B — Gate G1/G2: 13 → 5

Reuses existing, already-debugged in-repo tooling. All tasks HAIKU unless noted.

**G1 — exact-arithmetic screen** (per candidate, fully mechanical):
1. Minimal recurrence order via corrected classifier + held-out validation (`k3_sieve_analysis.py` protocol).
2. Weight-3 and weight-2 Weil bounds over ≥44 primes (`modularity_screen.py`) — recalling the v1 lesson that weight-2 failures alone do **not** discriminate; both bounds are recorded, neither is over-interpreted.
3. Mirror-map integrality, 30 coefficients (`mirror_map_integrality.py`).
4. Fuchs-criterion singular-point classification (`k3_monodromy_verification.py`, post-fix); if a candidate yields regular non-MUM points where $S_{1,2}$ did not, attempt the RK4 monodromy loop that GAP-1 could never run — any candidate where monodromy is actually computable is automatically elevated (it can settle its geometry class properly).

**G2 — physics viability** (annotation, not elimination, except No-Go):
5. Stiffness $V''(0)$ extraction and mass-achievability contour over the $(\tau,\mathcal{V})$ family — **published as a contour, never a point**; fitting $\tau$ to a target mass is prohibited by the anti-circularity gate.
6. GD-1 No-Go check (kernel-verified exclusion applies to any candidate whose achievable window is pinned to $\sim10^{-23}$ eV).
7. Bare superradiance survival at M87* via the validated Dolan solver (`dolan_continued_fraction.py`) across the achievable mass window — reporting survive/screened-needed/excluded bands.

**Selection 13 → 5** (HUMAN gate, scored sheet prepared by HAIKU): composite of G1 pass-completeness, monodromy computability, No-Go clearance, superradiance band favorability, and control-candidate sanity (if either control misclassifies, **the whole phase halts** — classifier bug beats all results, per the GAP-1 experience).

---

## 3. Phase C — Gate G3: Quick Data Tests, 5 → 3

Uses **existing and available data only**. Honest inventory first:

| Dataset | Status | Use |
|---|---|---|
| SDSS DR17 spectroscopic | ✅ proven live query (`ws9_observational_telescope.py`, real objIDs on disk) | TDA statistic + KK projection per candidate |
| Euclid Q1 (2025 public release, Deep Fields ~63 deg²) | ⬜ **not yet in repo** — acquisition task EU-1 below | first non-SDSS TDA tile; footprint-independent replication |
| JWST UNCOVER public catalogs | ⬜ acquisition task JW-1 | replaces the synthetic see-saw $\Delta_{\rm early}$ (Part VI open problem #6) |
| NANOGrav 15-yr public data | ⬜ acquisition task PT-1 | frequency-window occupancy check per candidate |
| Gaia DR3 / GD-1, SPARC, Pantheon+, DESI DR1 | ✅ in repo | reuse of existing crucible |
| DarkMatterK3-Home browser network | ✅ operational (external) | volunteer TDA compute; see §5 |

**Tasks:**

| Task | Executor | Content | Kill criterion |
|---|---|---|---|
| **EU-1** | HAIKU | Acquire Euclid Q1 MER catalog tiles (ESA archive / IRSA); verify license, footprint, column schema; commit a ≤500-object validation slice + full-tile fetch script (not the full data) to `data/euclid_q1/`. | If access requires credentials we lack → BLOCKED note, no simulated substitute (Rule 1). |
| **JW-1** | HAIKU | Acquire JWST UNCOVER photometric catalog; extract $z\ge8.5$ compact-source density proxies with the same $\tilde\rho$ definition as WS9, documenting every conversion. | Same Rule-1 blocking discipline. |
| **QT-1** | HAIKU | Per surviving candidate: recompute the WS9 KK projection on SDSS DR17 **and** the Euclid Q1 slice with the candidate's stiffness-scaled base mass; record whether the projected map is structurally distinguishable between candidates (KS test on $m_{\mathrm{eff}}$ distributions). | Candidates indistinguishable from $S_{1,2}$ on both surveys at KS $p>0.9$ carry no observational leverage → demoted. |
| **QT-2** | HAIKU | Replace the WS11 synthetic $\Delta_{\rm early}$ with the JW-1 empirical distribution; re-run the see-saw detectability t-test per candidate. This converts Part VI's weakest toy into a data-anchored sensitivity statement. | — |
| **QT-3** | HAIKU | PTA window occupancy: for each candidate's achievable mass window, compute the implied $f = m c^2/h$ band and its overlap with NANOGrav 15-yr sensitivity; flag candidate *pairs* whose stiffness ratios give ratio-test bands inside PTA reach. | — |
| **QT-4** | SONNET+ | Lee–Tsai overlap test: check whether any candidate's resonance structure lands in the self-interaction band favored for small-scale structure (SIDM $\sigma/m$ ~ 0.1–1 cm²/g at dwarf scales, bounded ≲1–2 cm²/g at clusters), using the LR-5 bridge memo — reporting honestly that this is a structural analogy check, not a shared-Lagrangian prediction. | — |
| **QT-5** | HAIKU | Null-hypothesis battery: run `lss_tensor_analytics/null_hypothesis_test.py` Poisson-mock comparison for every TDA statistic used in QT-1, per survey. Any statistic that does **not** separate real data from mocks is barred from candidate scoring. | Statistic fails separation → barred. |

**Selection 5 → 3** (HUMAN gate): promote the three candidates maximizing *observational leverage* — defined as (number of independent G3 tests where the candidate is distinguishable) × (falsifiability: at least one existing-data test that could have killed it and didn't). A candidate that merely survives everything without being distinguishable anywhere is explicitly disfavored — unfalsifiable-in-practice is a defect, not a virtue.

---

## 4. Phase D — Gate G4/G5: Top-3 Real Implementation + Lean Formalization

Per promoted candidate (templates all exist from v1):

1. **Lean kernel verification** (HAIKU, chunked): finite-range recurrence theorems for $n\le20$ on the `S12S21Recurrence.lean` template; stiffness-ratio interval theorems on the `GaugeCoupling.lean` template; falsification theorems on the `PTAFrequencyRatio.lean` template *including the conditional-antecedent docstring pattern from day one* (the GAP-2 lesson, pre-installed).
2. **Ledger + CI integration** (HAIKU): every candidate parameter enters `PARAMETER_LEDGER.yaml` with source, fit-target declaration, and caveat fields; cross-consistency check extended to the new entries.
3. **Manuscript module** (SONNET+): one section per candidate in a "Part VII: The Hypothesis Foundry" manuscript, written negative-results-first, with the provenance ledger pattern from THEORY_ALIGNMENT.md.
4. **External verification invitations** (HUMAN): GitHub issues with reproduction scripts per candidate; for any candidate with computable monodromy, a targeted invitation to the arithmetic-geometry community (this is the piece professionals can verify cheapest).
5. **Observatory targeting dossier** (SONNET+): for the single best candidate pair, the PTA ratio-test band and any TDA anomaly nodes as a concrete, falsifiable target list — the v2 successor to the Δ=47.0 lensing cross-match.

---

## 5. DarkMatterK3-Home Integration (volunteer compute, auto-protected)

The browser network (DarkMatterK3-Home.github.io) becomes the G3 compute multiplier, with BOINC-grade integrity added:

- **DM-1** (HAIKU): job spec schema — each volunteer work unit = (survey tile, statistic version hash, candidate id, seed); results signed with client version.
- **DM-2** (HAIKU): **quorum replication** — every tile dispatched to ≥2 independent clients; disagreement beyond tolerance → tile quarantined, never averaged. This is the citizen-science analog of the CI gate.
- **DM-3** (HAIKU): provenance closure — converged runs auto-archived into `data/dmk3_runs/` with reproduction manifest, retiring the v1 defect where headline numbers (1.177, Δ=47.0) lived outside the repository. **The v1 numbers themselves get a re-run under this scheme before any v2 manuscript cites them again.**

---

## 6. Gates, Criteria, Kill Rules (summary table)

| Gate | Question | Pass criterion | Kill/halt criterion |
|---|---|---|---|
| G0 | Is it already classified? | Literature concordance table complete | Literature contradicts our label → adopt literature, annotate |
| G1 | Is the arithmetic real? | Held-out recurrence residuals exactly 0; screens run | Any control (A005259 / Zagier) misclassified → **halt phase, fix classifier** |
| G2 | Is the physics viable? | Mass contour + No-Go + Dolan bands published | Window pinned in GD-1-excluded regime → kill |
| G3 | Does data care? | Distinguishable on ≥1 real dataset; null battery passed | Indistinguishable everywhere → demote (unfalsifiable-in-practice) |
| G4 | Is it formalizable? | Lean n≤20 kernel theorems; ledger integration; CI green | `sorry`/axiom smuggling → CI already blocks |
| G5 | Can outsiders check it? | Reproduction script + invitation issued | — |
| **All** | Anti-circularity | No parameter fit to its own validation target (ledger-declared) | Violation → task output void, per GAP-2 precedent |

Standing rules inherited unchanged: Rule 1 (never invent numbers; BLOCKED notes over improvisation), Rule 4 (negative results at top), provenance ledger for every externally-sourced number, zero-`sorry` CI gate.

---

## 7. Cost & Executor Budget (low-cost LLM implementation)

| Phase | Tasks | Executor mix | Est. LLM calls | Est. compute |
|---|---|---|---|---|
| A (literature → 13) | LR-1…LR-6 | 5 HAIKU + 1 SONNET+ | ~150 | negligible |
| B (13 → 5) | G1/G2 × 13 | HAIKU batch | ~300 | ~20 CPU-h (sieve at n≤110, 44-prime screens) |
| C (5 → 3) | EU/JW/PT/QT × 5 | HAIKU + 1 SONNET+ | ~250 | ~10 CPU-h + volunteer network |
| D (top 3) | Lean + manuscripts | HAIKU chunks + SONNET+ | ~400 | Lean builds ~2 h/candidate |
| **Total** | | **~85% HAIKU-tier** | ~1,100 calls | < 50 CPU-h owned compute |

Every HAIKU task ships with: exact input paths, exact commands, acceptance criteria checkable by script, and a BLOCKED-note template. No HAIKU task contains a design decision; all design decisions are pre-made in this plan or deferred to the three HUMAN gates (pool freeze, 13→5, 5→3).

## 8. Timeline & Success Metrics

- **Weeks 1–2:** Phase A complete, pool frozen (HUMAN gate 1).
- **Weeks 3–4:** Phase B, 13→5 (HUMAN gate 2). Classifier controls validated — *this alone is a publishable methods result*.
- **Weeks 5–7:** Phase C incl. Euclid Q1 ingestion, 5→3 (HUMAN gate 3).
- **Weeks 8–12:** Phase D; Part VII manuscript draft; observatory dossier.

**Success is defined as any of:** (i) a candidate with computable monodromy settling its geometry class properly (v1 never achieved this); (ii) a data-distinguishable candidate pair with a PTA-reachable ratio band whose antecedent is *not* circular; (iii) the honest kill of all 13 with the answer-key-validated classifier — which would be the strongest evidence yet published that the $S_{A,B}$-to-dark-sector route is closed, itself a citable negative result.

## 9. What This Plan Does NOT Claim

It does not claim the K3 hypothesis is likely true (current evaluation: most load-bearing links broken). It does not claim Euclid results exist yet (none do). It does not adopt the El Naschie framework (numerology-class, boundary-marker only). It does not promise the Lee–Tsai particle content maps onto ours (different DM candidates; shared geometry only). It claims exactly one thing: **the infrastructure that killed v1's overclaims is strong enough to run an honest, cheap, evolutionary search over the space v1 sampled one point of — and either find something real or close the route with authority.**
