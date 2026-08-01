# 🔬 K3×T² Deep Scientific Improvement Plan — Haiku/Sonnet Execution Tiers

> **2026-07-16:** This plan is now the **Stream-2 gate machinery** of the three-stream
> **Dual-Scale Topological Universe Model** master plan — see `DUAL_SCALE_THREE_STREAM_PLAN.md`
> (Stream 1: F-theory Lean certification in `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal`;
> Stream 2: this repo; Stream 3: DarkMatter@Home GPU validation in `DarkMatterK3-Home.github.io`).
> The gate sequence below remains binding; D-2.3 (T² Lean) migrates to Stream 1 (task S1-3),
> and Phase 8.E DarkMatter@Home tasks migrate to Stream 3.

**Date:** 2026-07-14 · **Status:** ACTIVE · **Authority:** Plan drafted by Fable session; execution split Haiku/Sonnet; all gates HUMAN-decided
**Scope:** Harden the K3×T² compactification hypothesis (Cooper s₇ primary, **cooper_s10 challenger**) from its current phenomenological state to a preregistered, mock-calibrated, Lean-anchored research program.

---

## 0. Why this plan exists (honest state assessment)

The project has a genuinely rigorous kernel and a softer empirical shell. This plan closes the gap.

### What is solid (do not redo)

| Asset | Evidence |
|---|---|
| Cooper s₇/s₁₀/t103 exact recurrences | `Structures/{CooperS7,CooperS10,T103}Recurrence.lean`, `decide`-proved n∈[0,20], zero `sorry`, verified to n≈197 in Python (commit 9796080) |
| GATE battery G1-1…G2-4 on frozen 13-pool | `data/autoresearch_v2/*.json`, pool frozen 2026-07-14 |
| S₁₂/S₂₁ formal rejection (elliptic, order-2) | Phase 8.B exact-rational nullspace; GATE-B record |
| GATE-C finalist selection (t103, cooper_s7, cooper_s10) | `data/autoresearch_v2/GATE_C_DECISION.md`, HUMAN-decided |
| CI: 28/28 cross-consistency incl. real `lake build` of 3 finalists | `scripts/cross_consistency_check.sh` |

### What is broken or unproven (audited 2026-07-14, this session)

| # | Defect | Evidence | Severity |
|---|---|---|---|
| A1 | `Structures/CooperS7_K3Geometry.lean` **does not compile** (noncomputable-instance errors at :36/:41/:46, unsolved goal at :51) **and contains `sorry` at :129** — yet commit c704833, `V5_COOPER_S7_OBSERVATORY.md`, and `PHASE_1_CHECKLIST.md` all claim "compiles cleanly, zero sorry" | `lake env lean` output, this session | **CRITICAL — Rule 4 violation** |
| A2 | "DISCOVERY: Δ_s7 = 663.4" is an **uncalibrated raw statistic**: no null distribution, no mocks, threshold 1.0 chosen arbitrarily. Δ_s7 = \|FFT(f(ρ)) − FFT(ρ)\| is *guaranteed* nonzero for any nonlinear monotone f — a large max proves the transform is nonlinear, not that K3 physics is present | `cooper_s7_euclid_worker.py` sector-1 run | **CRITICAL** |
| A3 | K3_volume spans **~25 decades** ([4.5e2, 4.8e27]); after z-scoring, the FFT difference is dominated by a handful of densest voxels — the metric mostly re-detects the density maximum | Phase 1 test log | HIGH |
| A4 | SDSS fallback **injects synthetic clusters** into 1-in-4 sectors and the discovery logger cannot distinguish real from fallback data | `cooper_s7_euclid_worker.py::fetch_real_sdss_data` | HIGH |
| A5 | Two **inconsistent** m_eff(Δ) laws coexist: `m_eff = m₀·exp(kΔ), k≈0.048` (Part VI memory) vs `m_eff ≈ m₀(1+κΔ)^{1/4}` (AGORA_K3_T2_BRIDGE_PLAN.md) | doc grep | HIGH |
| A6 | ρ_b → z sigmoid mapping is ad-hoc (acknowledged), un-parameterized, un-marginalized | `cooper_s7_periods.py::density_to_modulus` | MEDIUM |
| A7 | Historical headline numbers (S₁,₂ ≤ 1.177, Δ=47.0, 327,918-galaxy run) are **external, non-reproducible from committed artifacts** (prior Fable provenance audit) | memory `project_resonance_observatory.md` | MEDIUM (already qualified in manuscripts) |

### Standing rules (inherited, binding on every task below)

1. **Rule 1 (real arithmetic):** numbers must come from executed code committed to the repo, never hand-typed.
2. **Rule 4 (honest reporting):** a claim of "verified/compiles/discovery" requires the verification artifact in the same commit.
3. **Reproducibility rule (new):** every headline number must regenerate from one committed command; `cross_consistency_check.sh` is the enforcement point.
4. **No physics-washing in Lean (new):** Lean theorems may only state *mathematical* facts. Physical interpretations ("rigidity ⇒ noise filtering", "Δ probes extra dimensions") belong in manuscripts as hypotheses, never as `theorem` names.
5. **Preregistration (new):** for any comparative claim (s7 vs s10, Δ vs redshift), the discriminating statistic and decision threshold are committed *before* the run.

---

## 1. The hypothesis, stated precisely (what "K3×T²" must mean)

**H-K3T2:** The internal space is the 6-real-dimensional product **K3 × T²** (10D total). Its moduli couple to the 4D baryonic environment:

- **K3 factor** — complex-structure modulus **z**, governed by the order-3 Picard–Fuchs system whose holomorphic-period expansion coefficients are the Cooper s₇ sequence (A183204). Candidate role: **dark-matter axion sector** (mass set by K3 geometry).
- **T² factor** — Kähler/complex modulus **τ = τ₁ + iτ₂**, with KK tower m²_{n,m} ∝ |n + mτ|²/(τ₂·A). Candidate role: **dark-energy / Cosmic See-Saw sector** (slow τ evolution ⇒ freeze-out of the resonance with cosmic time).
- **Coupling ansatz:** local baryonic density ρ_b deforms z via a chameleon-type conformal coupling; the observable is a mock-calibrated asymmetry statistic on galaxy density fields.

**Falsifiable commitments (each maps to a task below):**

| ID | Prediction | Kills the hypothesis if… |
|---|---|---|
| F1 | Kernel specificity: mock-calibrated significance differs between s₇ and a growth-matched random sequence | random kernel performs identically (⇒ metric measures nonlinearity, not geometry) |
| F2 | See-Saw: mock-calibrated μ_Δ(z) rises monotonically with redshift | slope ≤ 0 or non-monotone after calibration |
| F3 | TDA alignment: top-Δ nodes over-populate high-β₁ (filament) regions vs shuffled control | enrichment consistent with random |
| F4 | Lensing: top-Δ centroids correlate with κ-map peaks beyond galaxy-count expectation | no excess over a galaxy-density-matched control |
| F5 | Next-best-candidate discrimination (s7 vs s10): preregistered statistic separates them, or degeneracy is declared | — (either outcome is publishable; hiding degeneracy is the failure) |

**The next best candidate is `cooper_s10` (OEIS A005260, Cooper level-10, weight-3 K3):** same GATE-C finalist tier, same order-2 recurrence with P₂(n)=(n+2)³, existing Lean file. `t103` is the tie-breaker if s7/s10 are degenerate.

---

## 2. GATE R-0 — Rigor repair (BLOCKING; nothing else starts first)

**Tier: Haiku.** Mechanical, checkable, no derivations.

### R-0.1 Fix or quarantine `CooperS7_K3Geometry.lean`
- Repair path: mark polynomial defs `noncomputable`, fix `P2Poly_eq_cube` (use `Polynomial.ext` + `decide`-style coeff match or restate over `ℤ[X]` via `C`/`X` normal form), fix `K3BettiNumbers` (it's used as a type where an instance is needed), **delete or prove** `P0_P2_ratio_vanishes` (the `sorry`), import `CooperS7Recurrence` properly.
- Quarantine path (acceptable): move to `lean4_formal_proofs/drafts/`, exclude from build, and strip all "verified in Lean" language for its content from the docs.
- ✅ **Validation:** `cd lean4_formal_proofs && lake env lean Structures/CooperS7_K3Geometry.lean` exits 0 **and** `grep -c sorry` returns 0 — output pasted into commit body. Add the file to `cross_consistency_check.sh` (29th check).

### R-0.2 Correct the false claims in prose
- Amend `V5_COOPER_S7_OBSERVATORY.md` + `PHASE_1_CHECKLIST.md`: replace "compiles cleanly / zero sorry / DISCOVERY" with accurate status; re-label Δ_s7 = 663.4 as **"uncalibrated raw statistic, pending GATE D-1 mock calibration."**
- ✅ **Validation:** `grep -rn "DISCOVERY\|compiles cleanly" V5_COOPER_S7_OBSERVATORY.md PHASE_1_CHECKLIST.md` shows only corrected phrasing; correction noted in commit message (Rule 4 pattern: corrections are logged, never silently edited).

### R-0.3 Data provenance tagging
- `cooper_s7_euclid_worker.py`: every run entry gets `"data_provenance": "SDSS_ASTROQUERY" | "SYNTHETIC_FALLBACK"`; **remove the synthetic cluster injection** (it manufactures discoveries); discovery logging refuses `SYNTHETIC_FALLBACK` records.
- ✅ **Validation:** run once offline (astroquery unreachable) → log shows `SYNTHETIC_FALLBACK`, `discoveries_cooper_s7.json` unchanged.

### R-0.4 Bounded period observable
- Replace raw \|Π₀(z)\|² (25-decade dynamic range) with a bounded observable — default: **log-period contrast** `L(z) = log Π₀(z) / log Π₀(z_max)` or normalized `Π₀(z)/⟨Π₀⟩`; keep the old field behind a flag for comparison.
- ✅ **Validation:** unit test asserting output dynamic range < 3 decades on the lognormal mock; committed as `tests/test_cooper_s7_periods.py`.

**GATE R-0 exit criterion (HUMAN):** all four checkmarks green + CI 29/29.

---

## 3. GATE D-1 — Statistical foundation (the null hypothesis machine)

**Tier: Haiku executes, Sonnet reviews the design once.**

### D-1.1 Mock ensemble generator (`scripts/k3t2_mock_ensemble.py`)
- 100 Poisson mocks + 100 lognormal-clustered mocks per sector geometry, matched to (N_gal, box, selection). Seeded, reproducible.
- ✅ **Validation:** `python3 scripts/k3t2_mock_ensemble.py --selftest` prints ensemble means/variances; JSON manifest committed.

### D-1.2 Calibrated significance
- For every sector statistic X (mean Δ, max Δ, node count): report **empirical p-value and z-score against the mock ensemble**, never raw values. Discovery re-defined as p < 1e-3 in *both* mock families.
- ✅ **Validation:** rerun Sector 1 → report `Δ_s7^max = 663.4, p_Poisson = ?, p_LN = ?`. **Preregistered expectation: p will be large** (the raw 663 is likely typical for the nonlinear transform) — either outcome is progress.

### D-1.3 Kernel-swap falsification battery (**implements F1, F5**) — the core of "next best candidate"
Run identical sectors through four kernels with the **same** bounded observable and mock calibration:

| Kernel | Source | Role |
|---|---|---|
| cooper_s7 (A183204) | existing engine | primary |
| **cooper_s10 (A005260)** | new `cooper_s10_periods.py` — terms 1, 6, 66, 866, 12546, 194358, 3117876, 51033096, 848049186, 14246309586 (verify against OEIS b-file at run time, Rule 1) | **challenger (next best candidate)** |
| t103 (A276536) | existing Phase 8 tools | tie-breaker |
| growth-matched random | random log-convex integer sequence with s₇'s asymptotic ratio μ≈27+… | destructive control |

- **Preregistered statistic (commit before running):** Pearson correlation r between calibrated Δ-maps of kernel pairs, plus per-sector significance rankings.
- **Preregistered decision rule:** if r(s7, random) > 0.95 → **F1 fails, the observable is kernel-blind → Phase 2 empirical claims are frozen until the observable is redesigned.** If r(s7, s10) > 0.95 but r(s7, random) < 0.5 → declare **weight-3 degeneracy** honestly (the observable sees "K3-ness," not the modular level) and promote the s7-vs-s10 discrimination to Sonnet theory (D-2.4).
- ✅ **Validation:** `data/k3t2/d1_3_kernel_swap.json` + auto-generated table in the report; numbers regenerate via one command in CI.

**GATE D-1 exit criterion (HUMAN):** kernel-swap verdict adjudicated and recorded in `data/k3t2/GATE_D1_DECISION.md`.

---

## 4. GATE D-2 — Theory hardening (Sonnet tier)

Sonnet-only: these need derivations, not execution volume.

### D-2.1 Resolve the m_eff(Δ) contradiction (**A5**)
- Reconcile `m₀·exp(kΔ)` vs `m₀(1+κΔ)^{1/4}`. Derive the correct small-Δ law from the chameleon potential V(φ) + conformal coupling A(φ)ρ_b (ρ^{1/4} scaling suggests the standard chameleon m_eff ∝ ρ^{(n+2)/(2n+2)} family — identify n).
- ✅ **Validation:** `docs/derivations/meff_delta_law.md` with assumption ledger; both older formulas explicitly deprecated in the docs that carry them; small-Δ Taylor agreement test in Python.

### D-2.2 Derive (or honestly parameterize) ρ_b → z (**A6**)
- Either derive the transfer function from D-2.1's coupling, or declare a 2-parameter ansatz family z(ρ; a, b) and **marginalize over (a,b) in all downstream statistics**. No more single hard-coded sigmoid.
- ✅ **Validation:** derivation doc + `density_to_modulus(rho, params)` API change + sensitivity table (does the D-1.3 verdict survive across the (a,b) grid?).

### D-2.3 T² sector formalization (the "×T²" half, currently absent from code)
- Python: `lss_tensor_analytics/t2_modulus.py` — KK tower m²_{n,m}(τ), see-saw evolution τ(zₑ) ansatz, contribution to m_eff.
- Lean (math-only, per rule 4): `Structures/T2Lattice.lean` — Gaussian-integer-like lattice, KK mass-squared as positive-definite quadratic form, `decide`-proved spectrum facts for concrete τ on ℚ[i]; **no physics theorem names**.
- ✅ **Validation:** `lake env lean` exit 0, zero `sorry`, `#print axioms` pasted; Python module unit-tested against exact rational cases.

### D-2.4 s7-vs-s10 theoretical discriminant (activated if D-1.3 declares degeneracy)
- The two sequences differ in **modular level (7 vs 10)** ⇒ different singular-point locations of the PF operator ⇒ different z-values where Π₀ develops log branches ⇒ **different critical densities ρ_crit where the response steepens**. Compute both singularity structures exactly (they are algebraic numbers); the observable discriminant is the predicted ρ_crit ratio.
- ✅ **Validation:** exact singular loci in `data/k3t2/d2_4_singular_loci.json` (rational/algebraic, Rule 1: computed, not transcribed); prediction registered before any new data run.

### D-2.5 Repair the K3 topology layer in Lean (replaces the broken parts of R-0.1's file, if quarantined)
- Genuine content only: Betti vector (1,0,22,0,1) as a *definition* with χ=24 as arithmetic `decide`; P₂ positivity (already provable); **do not** state "rigidity," "mirror genus," or "monodromy structure" as theorems without proof — they were decorative in the current file.
- ✅ **Validation:** same Lean gate as D-2.3.

**GATE D-2 exit criterion (HUMAN):** one m_eff law, one documented ρ→z map, T² module live, s7/s10 discriminant registered.

---

## 5. GATE D-3 — Empirical program, re-run correctly (mixed tier)

Only after D-1 + D-2. Every test uses the bounded observable, mock calibration, provenance tags, and (a,b)-marginalization.

| Task | Tier | Test | Preregistered success metric | Validation artifact |
|---|---|---|---|---|
| D-3.1 | Haiku | Clean-slate 35-sector sweep, **both** s7 and s10, real astroquery only | ≥30/35 sectors with real data; per-sector p-values | `data/k3t2/d3_1_sweep.json` + CI regen |
| D-3.2 | Haiku | Redshift tomography (F2): bins z∈{0.1,0.2,0.3,0.4} (BOSS support; z=1.0 needs eBOSS/DESI — flag as stretch) with **per-bin mock calibration** (selection effects differ by bin!) | Spearman ρ(μ_Δ, z) > 0 at p<0.01 after calibration | `d3_2_tomography.json` + slope plot |
| D-3.3 | Sonnet design / Haiku run | TDA-β₁ alignment (F3) via existing GITN/TDA stack, with rotation-shuffled null | enrichment ratio CI excluding 1.0 | `d3_3_tda_alignment.json` |
| D-3.4 | Sonnet | Weak-lensing overlay (F4) on top calibrated node: public DES Y3 / KiDS-1000 κ-maps, **galaxy-density-matched control fields** | κ excess vs control, quoting the survey's own noise maps | `weak_lensing_overlay.py` + `d3_4_lensing.json` |
| D-3.5 | Haiku | Re-acquisition test: does the calibrated s7 pipeline recover the RA 205°/Dec 35° candidate node? (**Caveat A7: the original Δ=47 is externally sourced — treat as target coordinates only, not as a number to match**) | independent detection at p<1e-3, barycenter within 2° | `d3_5_reacquisition.json` |

**GATE D-3 exit criterion (HUMAN):** F1–F5 scoreboard filled in with calibrated verdicts; any external communication (outreach posts, GitHub issues to other repos) remains **HUMAN-signoff-only** per the standing D-4 rule from GATE-C.

---

## 6. Model routing table (who does what, and why)

| Work class | Tier | Rationale |
|---|---|---|
| File repairs, provenance tags, mock ensembles, sweeps, CI wiring, exact-integer sequence checks vs OEIS b-files | **Haiku** | mechanical, high-volume, each step has a binary pass/fail command |
| `decide`-style Lean proofs on concrete n (recurrence checks, χ=24, lattice facts) | **Haiku** | pattern-following from existing S20/CooperS7 files |
| Chameleon derivation, ρ→z transfer function, PF singular-locus analysis, s7/s10 discriminant, lensing methodology, non-`decide` Lean proofs | **Sonnet** | derivation-heavy, error-prone for a small model, low volume |
| GATE decisions R-0/D-1/D-2/D-3, external outreach, retractions | **HUMAN** | irreversible or reputation-bearing |

**Sequencing (strict):** R-0 → D-1 → D-2 (D-2 may start once R-0 closes; D-1.3 and D-2 can run in parallel) → D-3 → HUMAN GATE-E (publication/outreach decision).

---

## 7. Step-by-step validation ledger (append-only)

| Step | Command | Expected | Status |
|---|---|---|---|
| R-0.1 | `lake env lean Structures/CooperS7_K3Geometry.lean; grep -c sorry …` | exit 0; `0` | ☐ |
| R-0.2 | `grep -rn "compiles cleanly" V5_*.md PHASE_1_*.md` | no false claims | ☐ |
| R-0.3 | offline worker run | provenance tag, no synthetic discovery | ☐ |
| R-0.4 | `python3 -m pytest tests/test_cooper_s7_periods.py` | pass; range < 3 decades | ☐ |
| D-1.1 | `python3 scripts/k3t2_mock_ensemble.py --selftest` | manifest written | ☐ |
| D-1.2 | sector-1 rerun | p-values quoted, no "discovery" language unless p<1e-3 ×2 | ☐ |
| D-1.3 | kernel-swap battery | preregistered r-matrix + verdict | ☐ |
| D-2.1 | doc + Taylor test | one law survives | ☐ |
| D-2.2 | sensitivity grid | verdict stable across (a,b) | ☐ |
| D-2.3 | `lake env lean Structures/T2Lattice.lean` | exit 0, 0 sorry | ☐ |
| D-2.4 | singular-loci JSON | exact loci for s7 & s10 | ☐ |
| D-3.1–3.5 | per-table commands | calibrated artifacts | ☐ |
| GATE-E | HUMAN review of F1–F5 scoreboard | decision doc | ☐ |

---

## 8. What this plan deliberately does NOT do

- It does **not** assume the July-14 "Δ=663 discovery" survives calibration (preregistered expectation: it will not, as raw stated).
- It does **not** post anything externally — outreach text in `V5_COOPER_S7_OBSERVATORY.md` stays quarantined until GATE-E.
- It does **not** claim the K3×T² hypothesis is favored; it builds the machinery that could favor **or kill** it, with the cooper_s10 challenger and the random-kernel control as the two blades of the falsification scissors.

*Drafted 2026-07-14 (Fable session), following the audit that found defects A1–A7. First action for the next Haiku session: GATE R-0, task R-0.1.*
