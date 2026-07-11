# Open Problems & Call for Collaboration

**Project:** Agora Dark Sector — a *string-inspired* $K3\times T^2$ phenomenological model
**Status:** string-inspired EFT with an exact-rational algebraic sieve and targeted Lean 4 verification
**Posture:** This document is an explicit, honest map of what the model does **not** yet establish. We are **not** asking for a review — we are offering a **partnership**. Several gaps below require top-down string-theory expertise and topological databases (e.g. Kreuzer–Skarke) that an automated symbolic/formal pipeline cannot honestly supply. Fabricating those values would violate our *Zero Simulation Flottante* rule, so we leave them open and labelled.

---

## 🔴 GAP-1 update (2026-07-11): S₂,₁ is CONFIRMED not a K3 surface

**Full findings:** `docs/gap1/ORDER_VERIFICATION_FINDINGS.md`. This is placed first because it is a negative result bearing directly on the model's central premise (Rule 4 — negative results go at the top, not buried).

Re-deriving the minimal Picard-Fuchs recurrence for $S_{2,1}(n)=\sum_k\binom{n}{k}^2\binom{n+k}{k}$ from scratch, and validating the candidate against 149 held-out exact-integer values, shows it satisfies a genuine **order-2** recurrence — the signature of an **elliptic curve period**, not a K3 surface (which needs order-3). $S_{1,2}$ was checked against the same order-2 ansatz and has none; it remains genuinely order-3. This directly contradicted the "$S_{2,1}$: K3 Surface (Order-3)" label previously asserted in `K3_DISCOVERY_REPORT.md` and used as a load-bearing premise throughout the manuscripts.

**Root cause traced to two independent bugs**, both pre-existing (not introduced by this finding):
1. `scripts/k3_sieve_analysis.py::find_minimal_order` returned a polynomial-coefficient-degree quantity mislabeled as "order" (conflated with the true recurrence shift-order that actually determines the geometry class), and its existence check validated candidates against only 3 equations beyond the bare minimum — no held-out validation. This script also could not execute at all prior to this session due to a Python-version-incompatible f-string.
2. `scripts/k3_monodromy_verification.py::classify_singular_points` (the Fuchs-criterion regularity check) is missing the leading-coefficient's own vanishing-order offset in its threshold, which **systematically misclassifies every singular point it has ever tested as irregular** — including the presumed MUM point at z=0 for both sequences. Consequence: **no numeric monodromy matrix has ever actually been computed** by this script, despite being the cited implementation for Task T1.1. (This second bug is documented but **not yet fixed** — flagged as SONNET+ follow-up.)

**Bug #1 has been fixed and the full $A,B\in[1,5]$ sieve re-run in this session** (70 held-out checks, $n_{\max}=110$): with the corrected classifier, **only $(A,B)=(1,2)=S_{1,2}$ survives as a K3 candidate**; $(2,1)=S_{2,1}$ and $(2,2)$ both come back **Elliptic Curve (Order-2)**. No replacement K3 candidate appears elsewhere in the searched range.

**What is NOT yet settled** (a physics-judgement call, `[TIER: HUMAN]`, not resolved by this fix): whether to (a) drop $S_{2,1}$ and search for a genuine second K3 candidate outside $A,B\in[1,5]$, (b) keep $S_{2,1}$ as a non-K3 "recurrence invariant" (the downgrade-in-language escalation clause scientificplan.md already anticipates for GAP-2), or (c) rebuild the two-vacuum narrative entirely around a different second object. The mass-ratio prediction $\sqrt{1014/336}$ and the GAP-2 PTA ratio test remain arithmetically true as rational-number statements, but their interpretation as "two K3 vacua" no longer holds for the $S_{2,1}$ side.

**Status:** confirmed, not a suspicion. Do not cite "$S_{2,1}$ is a verified K3 surface candidate" going forward — see the findings doc for full detail and the open physics-judgement question.

---

## 🟢 GAP-3/GAP-4 update (2026-07-11): $S_{2,1}$ bare survives M87* without Chameleon screening

**Full findings:** `docs/superradiance/s21_bare_survival.md`, solver validation: `docs/superradiance/dolan_validation.md`. This is a positive result, but reported with the same rigor as a negative one (Rule 4): the number is real, script-computed, and corrects a previously-circulated figure that was not.

Task T3.1 replaced the small-$\alpha$ Detweiler (1980) superradiance growth-rate formula — used throughout this repository at couplings ($\alpha=0.089$–$1.55$) well outside its stated validity range (0.01–0.1) — with an exact continued-fraction solver following Dolan (2007), `scripts/dolan_continued_fraction.py`. The solver is validated against all 6 points of Dolan's published Table I (maximum $l=1,m=1$ growth rates vs. spin), transcribed directly from the arXiv PDF, to **<0.4% error** (5% was the task's required tolerance).

Task T3.2 (`scripts/s21_bare_analysis.py`) then used this exact solver to re-examine whether Chameleon screening (GAP-4's unphysical $n=-3$ mechanism) is actually *needed*, evaluating the bare (unscreened) couplings at M87* (EHT 2019 mass; $a_*=0.90$ is an illustrative literature value, not an EHT measurement):

- **$S_{2,1}$ bare** ($\alpha=0.089$): instability timescale $\approx380$ Myr — **longer** than the Salpeter accretion spin-up time ($\approx50$ Myr, Salpeter 1964) by $\approx7.6\times$. **Survives without any Chameleon screening.**
- **$S_{1,2}$ bare** ($\alpha=0.155$): instability timescale $\approx4.6$ Myr — **shorter** than the Salpeter time by $\approx11\times$. Does **not** survive unscreened; GAP-4's screening problem remains open, but now only for $S_{1,2}$.
- 5 additional real high-spin SMBHs (X-ray reflection-spectroscopy sample from Reynolds 2013: NGC 4051, IRAS 13224-3809, MCG-6-30-15, 1H0707-495, Ark 564), all far less massive than M87*, are stable under both sequences by a huge margin (cross-checked against the small-$\alpha$ formula: $\tau_\text{instability}\sim10^{33}$–$10^{38}$ yr).

**Correction on the record:** a previously-circulated narrative quoted $\tau_\text{instability}\approx86.6$ Myr for this same ($S_{2,1}$, M87*) case. That number does not appear in the output of any script in this repository — it was never actually computed. The real, reproducible value is $\approx380$ Myr; the qualitative conclusion (survives) is unchanged, but future citations should point to `docs/superradiance/s21_bare_survival.md`, not to that earlier figure.

**What is NOT resolved:** the survival argument compares instantaneous timescales, not a full spin-evolution/GRMHD history; M87*'s spin is assumed, not measured; GAP-4 (unphysical chameleon index) is still open for $S_{1,2}$ specifically (task T3.3, screening alternatives, remains `[TIER: HUMAN]`).

---

## 🟡 GAP-5 update (2026-07-11): real-CLASS check finds H₀≈75.8, not the claimed 71.92

**Full findings:** `docs/cosmology/class_fork_validation.md` (T5.2), `docs/cosmology/ic_sensitivity.md` (T5.1). Reported as a real, unfavorable discrepancy (Rule 4), not reconciled with the previous claim.

The "$H_0\sim72$" claim (`epsilon=0.02511 \to H_0=71.92$ km/s/Mpc, `LL.md:94`) was a **background-only** integration, described by `scientificplan.md` itself as using a "reverse-engineered" $\epsilon$ (tuned to a target $H_0$). Two checks were run against real CLASS (`classy`, actually installed and executed, not simulated):

1. **T5.1 — tracker ICs** (`empirical_crucible/tracker_ics.py`): replacing rest ICs ($\dot\phi=0$) with the Copeland-Liddle-Wands (1998) attractor solution shifts $w_0$ by only $\approx0.0002$ for this potential — a real result, but a small one.

2. **T5.2 — Boltzmann-grade background check** (`empirical_crucible/class_fork_validation.py`): a custom sound-horizon/comoving-distance integrator, validated against real CLASS's own derived parameters to $<0.002\%$ at $\epsilon=0$, was used to recompute the acoustic scale self-consistently at $\epsilon=0.02511$ (the model's own formula, $\rho_{DM}(a)\propto a^{-3-\epsilon}$, applied to BOTH the sound horizon and comoving-distance integrals — the previous calculation's internal consistency was not verifiable from what's documented). Result: **$H_0\approx75.8$ km/s/Mpc**, not 71.92 — and this **overshoots** the SH0ES local value ($\approx73$) rather than bridging Planck and SH0ES as the model intends. A diagnosed "inconsistent-shortcut" variant gives $H_0\approx61.0$ instead — neither reproduces 71.92, and the exact original derivation is not fully reproducible from the repository as documented.

3. **Architectural finding:** $\rho_{DM}(a)\propto a^{-3-\epsilon}$ implies $w_{DM}=\epsilon/3\approx+0.0084$ (positive). CLASS's public dark-energy-fluid API hard-rejects any fluid with $w(a\to0)\ge0$ — confirmed by an actual `classy` call raising `CosmoComputationError` (not asserted from documentation). A true perturbation-level $C_\ell^{TT}$ computation of this model requires patching CLASS's C source and recompiling — a genuine fork in the literal sense `scientificplan.md` T5.2 names it — and was **not attempted**: unlike the GAP-3 Dolan solver (validated against 6 independent published data points), a hand-written perturbation-equation patch would have no independent benchmark to validate against, and shipping one un-validated risks exactly the kind of unverified-claim failure already caught twice this session (GAP-1's fabricated weight-2 statistic, GAP-3's fabricated 86.6 Myr figure).

**What is NOT resolved:** whether $H_0\approx71.92$ or $\approx75.8$ (or neither) is the "correct" prediction of this model depends on resolving the internal-consistency question above, which requires either finding the original derivation or deciding which self-consistent treatment is authoritative — a judgement call, not something this finding auto-resolves. `PARAMETER_LEDGER.yaml`'s $H_0=71.92$ value is **not changed** pending that decision (changing it would require synchronized edits across `empirical_crucible/jax_inference.py`, `.benchmarks/*.json`, and the LaTeX manuscripts per the ledger's own consistency constraints) — the discrepancy is flagged in the ledger's `caveat` field instead.

**T5.3 update (same session): the S₈ side of the "cosmic see-saw" test is also negative.** `empirical_crucible/joint_epsilon_likelihood.py` executes the S₈ half of VISION.md §4A's falsification test quantitatively for the first time, using this model's own real axion masses against real CLASS $P(k)$ (own $\sigma_8$ integral validated to 5 significant figures against `cosmo.sigma8()`). Two independent channels, both real calculations:
- **FDM quantum-pressure suppression** (Hu, Barkana & Gruzinov 2000 — the mechanism VISION.md §4A itself cites): **negligible** ($<0.001\%$) at this model's masses ($1.8$–$3.2\times10^{-21}$ eV), which are $\sim20$–$30\times$ heavier than the FDM "sweet spot" ($\sim10^{-22}$ eV) where this effect matters for $S_8$.
- **Background-growth channel** (treating $\epsilon$ as a $c_s^2=0$ modification, T5.2's own model): gives $D_\epsilon(a{=}1)/D_{\rm std}(a{=}1)=1.040$ — a **+4% increase**, the **wrong sign** for lowering $S_8$.

The **JWST side was not quantitatively executed** — a rigorous $\mathcal{L}_{\rm JWST}(\epsilon)$ needs halo-mass-function modeling with no independent benchmark available (same reasoning that ruled out a hand-patched CLASS perturbation fork in T5.2); a real, independently-published qualitative check (Cox et al., arXiv:2307.10302: viable ALP window $10^{-22}$–$10^{-19}$ eV via a *different* mechanism) shows this model's masses fall inside that broad window, but that is not a fit of this model's own $\epsilon$ to JWST data. **Consequence: the full ">3σ mutual exclusion" falsification test cannot be completed as specified** — but the S₈ side alone is a real, negative, falsification-relevant finding: two independent real calculations, using this model's own real parameters, both fail to reproduce the S₈-lowering mechanism the see-saw narrative requires. Full details: `docs/cosmology/joint_epsilon_likelihood.md`. T5.4 (DESI DR2 refit) remains to be executed.

---

## The 5 Missing Pieces (referee "deeper programme", Round 2)

These are the items a second-round referee (string-theory / Swampland) identified as separating the present *string-inspired phenomenology* from a genuine top-down construction.

| # | Missing piece | What it requires | Label |
|:-:|:---|:---|:---|
| 1 | **Compactification / vacuum data** | A concrete Type IIB/IIA orientifold of $K3\times T^2$: D-brane content, integer flux quanta $(F_3,H_3)$, and explicit tadpole/anomaly cancellation. Needs Kreuzer–Skarke-scale topological databases and string-phenomenology judgement. | **Seeking Theoretical Collaborators** |
| 2 | **Genuine instanton action** | Derivation of the axion mass from a true Euclidean (E3/ED3) brane-instanton action wrapping a definite cycle — replacing the current phenomenological fit of $\tau$ and $\mathcal V$. | **Seeking Theoretical Collaborators** |
| 3 | **$S_{20}$ Picard–Fuchs recurrence (all $n$)** | A general-$n$ kernel proof of the order-4 minimal recurrence via a Wilf–Zeilberger certificate $G(n,k)$ compiled into Lean. (Now algebraically verified for all $n$ via SymPy symbolic certificate checking, numerically verified for $n \in [0,60]$, kernel-verified $n\le 8$ via `decide`, general law is an explicit `axiom`.) | **Agora Phase 4 Roadmap (WZ Lean Compilation)** |
| 4 | **Moduli stabilisation** | A mechanism (GVW flux superpotential / $\mathcal N=2$ attractor) that fixes the dilaton and complex-structure moduli. Our exact analysis (`scripts/alpha_topology.py`) shows the stabilised values are functions of free integer fluxes/charges — i.e. not yet determined. | **Seeking Theoretical Collaborators** |
| 5 | **Quintessence–Swampland tension resolution** | An explicit accelerating-epoch mechanism (multi-field, hilltop/plateau, or transient-DE embedding) consistent with $\lambda_\mathrm{fit}=1.6724>\sqrt2$. Currently reported honestly as a *tension/obstruction*, not resolved. | **Agora + Collaboration** |

---

## Detail per item

### 1 & 2 — Seeking Theoretical Collaborators (top-down string data)
The Agora pipeline **cannot** and **will not** hallucinate orientifold/flux/tadpole data or an instanton action. These are precisely the inputs that turn a *string-inspired EFT* into a *string vacuum*. We are looking to partner with string phenomenologists (e.g. groups at **OCA Nice**, **LUPM Montpellier**, or internationally) who can:
- propose a concrete $K3\times T^2$ orientifold whose K3 fibre is in the $S_{1,2}$/$S_{2,1}$ algebraic family (see structural template: [`orientifold_dbranes_template.json`](file:///home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-K3-DarkMatter/data/theory_inputs/orientifold_dbranes_template.json));
- specify integer flux quanta and verify tadpole cancellation;
- write down the Euclidean brane-instanton action that would *derive* (not fit) the axion mass scale (see submission template: [`euclidean_instantons_template.json`](file:///home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-K3-DarkMatter/data/theory_inputs/euclidean_instantons_template.json)).

In exchange, the Agora contributes: an exact-rational algebraic sieve, a reproducible Lean 4 verification harness, and an empirical-validation notebook against JWST/DES/quasar archives.


### 3 — Agora Phase 4 Roadmap (WZ Lean Compilation)
This is the one open item the Agora can close on its own.
- **Done:**
  - **Numerical Verification:** Both the order-5 and minimal order-4 recurrences have been verified exactly for all $n\in[0,60]$ using arbitrary-precision integers with negative control checks (`verify_s20_recurrence.py` and `verify_s20_order_4.py`).
  - **Lean 4 Formalization:** Both recurrences, their polynomials, their left-hand sides, and kernel-verified checks for $n \le 8$ via `decide` are fully formalized in `Structures/S20Recurrence.lean` (sorry-free and admit-free). The general laws are declared as explicit, auditable `axiom`s.
  - **WZ Certificate Verification:** The bivariate rational creative-telescoping certificate $R(n,k)$ from Maxima/SageMath has been algebraically verified for all $n$ and $k$ via exact SymPy symbolic evaluation (`verify_wz_certificate.py`), simplifying the WZ relation difference to exactly `0` (`diff = 0`).
- **Phase 4 (WZ Lean Compilation):** Map the algebraically verified bivariate polynomial identity into a formal Lean 4 algebraic proof (using `field_simp; ring`) to prove the telescoping relation and replace the general-n `axiom s20_recurrence_order_4` with a fully compiled `theorem`. This would establish the first kernel-certified order-4 minimal Picard-Fuchs recurrence on the entire range.

### 4 — Moduli stabilisation (exact null result on record)
`scripts/alpha_topology.py` tests three geometric origins (GVW flux / dilaton, $\mathcal N=2$ attractor, D7-volume + $\chi=24$ threshold) for the bare gauge coupling. **Verdict: topologically unconstrained** — every candidate value depends on free integer fluxes/charges or on the (uncomputed) $S_{1,2}$ transcendental-lattice Gram matrix. Deriving an absolute coupling needs the item-1 vacuum data. The only defensible geometric output is the *relative* ratio $\sqrt{1014/336}\approx1.74$ (kernel-verified in `Agora.GaugeCoupling`).

### 5 — Quintessence–Swampland tension (reported as result, not resolved)
With $\lambda_\mathrm{fit}=1.6724>\sqrt2$ the scaling attractor gives $w_\phi\approx-0.07$ (not acceleration), kernel-certified in `Agora.SwamplandK3T2`. We present this as the model's central falsifiable physics statement: stable dark energy is obstructed here, consistent with the Swampland conjectures. An accelerating-epoch resolution remains open.

---

## What IS established (so collaborators know the starting point)

- **Exact algebraic sieve** over $\mathbb Q$ isolating $S_{1,2}$, $S_{2,1}$ as candidates in $A,B\in[1,5]$. **⚠️ 2026-07-11: $S_{1,2}$ is confirmed order-3; $S_{2,1}$ is now shown to be order-2 (elliptic signature), disputing its K3 label — see the GAP-1 update above and `docs/gap1/ORDER_VERIFICATION_FINDINGS.md`.**
- **GD-1 No-Go** (`cy_axion_no_go`): kernel-verified exact-rational exclusion of the symmetric-geometry masses.
- **Mass ratio** $\sqrt{1014/336}\in(1.73,1.75)$ and **relative inverse-coupling ratio** (same interval): kernel-verified over $\mathbb Q$.
- **Swampland tension lemmas** (`lambda_fit_exceeds_sqrt2`, `attractor_not_dark_energy`): kernel-verified.
- **$S_{20}$ recurrence**: exact for $n\in[0,60]$, kernel-verified for $n\le8$ (general law an `axiom`).
- Repository is **`sorry`-free**; remaining unproven items are explicit, disclosed `axiom`s.

## Disclosed axioms (full list)

| Axiom | Module | Justification |
|:---|:---|:---|
| `s20_recurrence` (general $n$) | `Structures.S20Recurrence` | Exact-verified $n\in[0,60]$; WZ certificate not yet compiled |
| Hodge / Euler data | `Agora.Conjectures.MirrorSymmetry` | CCGK classification data, not derived here |
| 13 Fano supercongruences | `Agora.Discovery.FanoSupercongruences` | Computationally verified conjectures |
| `atiyah_singer_trace_anomaly_coupling` | `Agora.Topology.AtiyahSinger` | Audited coupling of chiral trace anomaly to macroscopic stress-energy |


---

## How to engage

Open a GitHub issue or PR (formal Lean 4 counter-proofs and corrections welcome), or contact the author. Suggested venues for the joint result: **Physical Review D** or **JCAP**. We are explicitly seeking co-authors for items 1, 2, and 4.
