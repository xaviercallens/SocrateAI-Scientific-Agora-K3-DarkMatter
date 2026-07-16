# VISION.md — Project Vafa-Continuity: Masterwork Goals & The Long Forward View

**Maintained by:** Xavier Callens, Socrate AI Lab
**Scientific advisor (in absentia):** Cumrun Vafa review framework
**Honest framing:** String-inspired algebraic-geometry phenomenology with exact-rational formal verification
**Target publication:** *Physical Review D* or *Journal of Cosmology and Astroparticle Physics (JCAP)*

---

## Contents

**Part 0 — The Governing Vision: Dual-Scale Topological Universe Model (2026-07-16)**
- §0.1 The unification statement
- §0.2 Three parallel streams
- §0.3 What "reaching the vision" means (north-star success criteria)
- §0.4 How the legacy Masterwork Goals map into the streams

**Part I — The Three Masterwork Goals (path to publication)**
- Goal I — Discharge `s20_recurrence` (mechanical, highest priority)
- Goal II — Pick a compactification (physics depth)
- Goal III — Treat the quintessence-Swampland tension as the result *(done)*
- Publication target and submission checklist

**Part II — The Long Forward View (2025–2035 and beyond)**
- §4 The Grand Interpretation — the "Cosmic See-Saw" hypothesis
- §5 Experimentation history — the 30-year observational arc
- §6 The Falsifiable Predictions Manifest (Euclid, ELT, LISA, PTA)
- §7 Execution roadmap — predictions into deliverables

**Appendix — Current formal-methods status**

---

# PART 0 — THE GOVERNING VISION: DUAL-SCALE TOPOLOGICAL UNIVERSE MODEL (2026-07-16)

> **Operational plan:** `DUAL_SCALE_THREE_STREAM_PLAN.md` (task-level) · `ROADMAP.md` Phase 9 (milestones).
> This section defines *where the whole program is going*; Parts I–III below remain valid as the
> in-repo legacy goals now nested inside Stream 2.

## §0.1 The unification statement

The **Dual-Scale Topological Universe Model** proposes that the dark sector is the geometry of an
**F-theory compactification**: an elliptically fibered Calabi–Yau fourfold whose **base is
B₃ = K3 × T²** and whose **elliptic fiber degenerates along the discriminant locus**.

| Physical phenomenon | F-theory geometry | Generating sequence | Evidence status (2026-07-16) |
|---|---|---|---|
| Dark energy / global cosmic web | K3 base (rigid, order-3 Picard–Fuchs) | Cooper s₇ (A183204) / s₁₀ (A005260) | **[PARTIAL]** — order-3, Weil weight-3, integrality, exact singular loci done; newform identification open |
| Dark matter subhalos | Elliptic fiber (flexible, order-2 Picard–Fuchs) | S₁₂ (A112019) / S₂₁ (A005258) | **[ESTABLISHED]** at ODE/arithmetic level (GATE-B formal rejection as K3) |
| Baryonic matter / halo centers | Discriminant locus Δ_F = 4f³ + 27g² (7-branes) | Δ_obs peaks | **[NOT SUPPORTED]** — prior observable proved kernel-blind (GATE D-1.3); reframed via exact singular-locus observable |

The three-tier honesty vocabulary of Part II (**[VERIFIED] / [FITTED] / [PREDICTED]**) governs
every claim above; the third row is the program's open front, not an achievement.

## §0.2 Three parallel streams

| Stream | Repository | Focus | Goal |
|---|---|---|---|
| **1. Theory** | `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal` | F-theory formalization in Lean 4 | Mathematically certify the Dual-Scale Model |
| **2. K3 Selection** | `SocrateAI-Scientific-Agora-K3-DarkMatter` (this repo) | AutoEvolve for K3 sequence selection | Confirm Cooper s₇/s₁₀ as true K3 surfaces |
| **3. Experimentation** | `DarkMatterK3-Home.github.io` (+ `SocrateAI-Scientific-Agora-Home` infra) | GPU validation vs SDSS/Euclid/PTA | Empirically validate (or falsify) the model |

Streams run in parallel; they exchange only **committed, hash-referenced artifacts** (certified
sequences, exact discriminants, preregistered observables, quorum-replicated verdicts) — never
prose claims. See `DUAL_SCALE_THREE_STREAM_PLAN.md` §7.

## §0.3 What "reaching the vision" means (north-star success criteria)

The vision is **reached** when all three hold simultaneously — and it is **honestly killed** if
any of the falsification branches fires:

- **V1 (Theory certified):** the Lean dual-scale theorem chain compiles with zero `sorry` and an
  axiom inventory in which every axiom is either discharged, or tagged `empirical_` with a
  reproducible artifact hash, or tagged `hypothesis_`. *No axiom encodes a non-reproducible
  number.* (Gate: **GATE-T**.)
- **V2 (Selection decided):** cooper s₇ and s₁₀ are identified with specific K3 families
  (weight-3 newform / literature match), and the preregistered singular-locus discriminant
  (z_crit = 1/27 vs 1/16) either selects one or declares degeneracy publishably.
  *Falsification branch: neither matches a K3 family → H1 dies and the base must be re-selected
  from the AutoEvolve pool.* (Gate: **GATE D-1v2** + AutoEvolve battery.)
- **V3 (Experiment adjudicated):** a kernel-swap-passing observable, run under quorum replication
  on the volunteer GPU network against real SDSS/Euclid data, returns calibrated p-values for the
  F1–F5 scoreboard. *Falsification branch: the discriminant-locus signature is absent at
  preregistered sensitivity → H3 dies; the model survives only as mathematics.* (Gates:
  **GATE-X** → **GATE-E**.)

A killed hypothesis with this machinery is a publishable result; an unfalsifiable one is not.

## §0.4 How the legacy Masterwork Goals map into the streams

- **Goal I** (discharge `s20_recurrence`) → Stream 2 formal-verification backlog (WS4/T4.1); unchanged.
- **Goal II** (pick a compactification) → **superseded and upgraded by Stream 1**: the schematic
  Type IIA orientifold sketch below is replaced by the concrete F-theory choice (elliptically
  fibered CY₄ over K3×T²), already formalized at v0.1 (0 sorry) in the LeanProposal repo. The
  tadpole/flux feasibility questions (T7.2) migrate to Stream 1 task S1-4/S1-5.
- **Goal III** (Swampland tension as the result) → unchanged, feeds the Stream 1 manuscript.
- **Part III AutoEvolve R2** → is Stream 2's engine; its next iteration adds the singular-locus
  fingerprint gate (task S2-5).

---

# PART I — THE THREE MASTERWORK GOALS

## Thesis statement (the correct framing)

> "A string-inspired algebraic-geometry sieve for fuzzy dark matter candidates, with exact-rational formal verification of the GD-1 exclusion."

This is what the work *actually is* and what it should be presented as. The ambition of the current title ("unification of the dark sector") outruns the content. The content itself — exact arithmetic, Lean kernel results, honest limitations — is genuine and novel in this phenomenological context. The three goals below are the specific steps that would elevate it from respectable phenomenology to a genuine contribution to both string phenomenology and the Swampland literature.

---

## Goal I — Discharge `s20_recurrence` (mechanical, highest priority)

### What it is

The order-5 Picard–Fuchs recurrence for the $S_{20}$ sequence:

$$P_0(n)\,S_{20}(n) + P_1(n)\,S_{20}(n+1) + \cdots + P_5(n)\,S_{20}(n+5) = 0$$

is stated in `lean4_formal_proofs/Structures/S20Recurrence.lean` with a `sorry` placeholder.
This recurrence is the algebraic backbone of the 6D No-Go argument — if it is not kernel-verified, the No-Go claim rests on a computer-algebra assertion, not a proof.

### Why it matters

- The GD-1 No-Go (`cy_axion_no_go`) is already fully kernel-verified.
- The upstream 6D stiffness claim ($V''(0) \approx 1024$ for symmetric geometries) depends on the $S_{20}$ recurrence being correct.
- Discharging the `sorry` would make the complete exclusion chain — from geometry to mass to stellar stream — entirely kernel-verified, which is publishable as a standalone formal-methods result.

### How to achieve it (step by step)

1. **Extract the Zeilberger certificate from SageMath.**
   The coefficients $P_0 \ldots P_5$ are already in the Lean file. What is missing is the telescoping
   rational certificate $G(n, k)$ such that:
   $$P_k(n) = \Delta_k[G(n,k) \cdot \text{summand}(n,k)]$$
   Run in SageMath:
   ```python
   from sage.combinat.e_one_s import *
   # or use the built-in Zeilberger implementation:
   var('n k')
   f = binomial(n,k)^4 * binomial(n+k,k)
   # ZeilbergerRecurrence(f, n, k, 5)  # order-5
   ```
   The output is a list of rational polynomials in $n$ — the certificate $G(n,k)$.

2. **Encode the certificate as a Lean `Finset.sum` identity over $\mathbb{Q}$.**
   Template (skeleton):
   ```lean
   theorem s20_certificate (n k : ℕ) :
       G n k * summand n k - G n (k-1) * summand n (k-1) =
       P0 n * summand n k + ... := by
     ring
   ```
   Then the global recurrence follows by `Finset.sum_telescope`.

3. **Close with `norm_num` or `decide` on the rational polynomial coefficients.**
   Since all coefficients are rational numbers with bounded denominators, `norm_num` can verify
   each polynomial identity in finite time.

4. **Remove the `sorry` and the `⚠️ DISCLAIMER` header.**
   Update the module docstring to reflect clean status.

5. **Update manuscript §2 open-obligations bullet** and **Reviewer_Response.md table**.

### Effort estimate

2–4 days of focused Lean/SageMath work. The mathematics is done; this is purely mechanical encoding.

### Files to modify

- `lean4_formal_proofs/Structures/S20Recurrence.lean` — discharge sorry
- `manuscripts_and_proofs/K3_DarkMatter_Preprint.tex` — update §2 open obligations
- `agora_ai_agents/Reviewer_Response.md` — mark obligation closed
- `agora_ai_agents/Physic review.md` — update inventory table

---

## Goal II — Pick a compactification (physics depth, medium priority)

### What it is

The paper currently identifies $S_{1,2}$ and $S_{2,1}$ as "K3 string vacua" based on their
Picard–Fuchs operators having order 3. An order-3 PF operator is evidence that a *family of
K3 Hodge structures* exists — it is not a vacuum. A string vacuum requires:

- A choice of string theory (Type IIA, Type IIB, M-theory, F-theory)
- A compactification geometry with specified orientifold or fibration data
- A flux superpotential $W = \int G \wedge \Omega$ with tadpole cancellation
- Stabilization of *all* moduli (dilaton, $T^2$ complex structure and volume, K3 moduli — up to 20)

None of this is currently present. The goal is to introduce at least a **schematic compactification
scaffold** sufficient to justify the vocabulary "string vacuum" in a qualified sense.

### The proposed compactification

Work in the **Type IIA orientifold of $K3 \times T^2 / \mathbb{Z}_2$** with D6-branes, following
the Becker–Becker framework. This is the simplest $\mathcal{N}=2 \to \mathcal{N}=1$ reduction
that:
- Gives a 4D EFT with K3 moduli and a $T^2$ volume modulus
- Allows flux stabilization via RR and NS-NS 3-form fluxes
- Has a known tadpole condition $N_\mathrm{D6} + N_\mathrm{flux} = 24$ (K3 Euler characteristic)
- Has axions from the RR sector whose masses are set by instanton actions on K3 cycles

### Minimum viable addition to the manuscript

Add a new §1.5 "Compactification data" with the following:

```
We work schematically in the Type IIA orientifold of K3 × T²/ℤ₂.
The K3 is identified with the S_{1,2} or S_{2,1} family via its
Picard–Fuchs Hodge structure. The T²/ℤ₂ orientifold introduces
O6-planes whose tadpole condition fixes:
  N_flux = χ(K3) - N_D6 = 24 - N_D6

The axion is the RR 1-form reduced on the K3 fundamental class [Σ].
Its mass is m_a² ~ M_pl² exp(-S_inst) where S_inst = 2π Vol(Σ)/ℓ_s².
The topological stiffness V''(0) ∈ {1014, 336} encodes the relative
instanton action ratio between the two K3 vacua; the absolute scale
requires fixing Vol(Σ) via a moduli stabilization mechanism (KKLT or LVS),
which is explicitly left as an open problem.
```

This paragraph would:
- Justify calling the objects "string vacua" in a qualified sense
- Correctly attribute the mass scale to the instanton action
- Honestly state that absolute mass values require full moduli stabilization

### How to achieve it (step by step)

1. **Read:** Becker–Becker (hep-th/9506023), Vafa–Witten (hep-th/9409188), Svrcek–Witten
   (hep-th/0605206) §2 on axion masses from branes. These are the three foundational references.

2. **Identify the correct cycle $\Sigma$.** For $S_{1,2}$, the Picard group has rank $\rho = h^{1,1}$.
   The instanton wraps the generator of $\mathrm{Pic}(K3)$ at the MUM point. This is the data
   currently encoded as "topological stiffness" — the connection needs to be made explicit.

3. **Write the tadpole equation** for the specific orientifold and verify $N_\mathrm{flux} \ge 0$.
   If this fails for $S_{1,2}$ or $S_{2,1}$, say so — it is a genuine constraint.

4. **Add one Lean `axiom` or `def`** for the compactification choice, clearly labelled as
   schematic input data, not a derived theorem. This keeps the formal-methods layer honest.

5. **Add the three new bibliography entries:**
   - Becker–Becker `becker1995` (hep-th/9506023)
   - Vafa–Witten `vafa1995` (hep-th/9409188)
   - Svrcek–Witten `svrcek2006axions` (already in bib — just cite in this new section)

### Effort estimate

1–2 weeks of physics writing. No new computation required; this is a theoretical framing addition.

### Files to modify

- `manuscripts_and_proofs/K3_DarkMatter_Preprint.tex` — add §1.5 with compactification data
- `manuscripts_and_proofs/k3_axion_bibliography.bib` — add Becker–Becker, Vafa–Witten
- `lean4_formal_proofs/Agora/Conjectures/MirrorSymmetry.lean` — add compactification axiom
- `agora_ai_agents/Physic review.md` — mark A.1 ("period sequence is not a vacuum") as addressed

---

## Goal III — Treat the quintessence-Swampland tension as the *result* (reframing, high impact)

### What it is

The current framing claims the model *satisfies* the Swampland bound. It does not — and that
is the interesting result. The tension is:

$$\lambda_\mathrm{needed\,for\,dark\,energy} < \sqrt{2} \approx 1.414$$
$$\lambda_\mathrm{Swampland\,bound} \gtrsim \mathcal{O}(1) \approx 1$$
$$\lambda_\mathrm{best\,fit} = 1.6724 > \sqrt{2}$$

A single exponential potential with $\lambda > \sqrt{2}$ has its scaling attractor at
$w_\phi = -1 + \lambda^2/3 \approx -0.07$ — not dark energy. The $w_0 = -0.55$ is a
transient thawing value, not an attractor. So the model simultaneously:

- Has $\lambda > 1$ (satisfies the Swampland inequality as input)
- Has $\lambda > \sqrt{2}$ (fails to produce accelerated expansion on the attractor)
- Has $w_0 = -0.55$ outside the DESI 1σ contour

This is not a failure — it is a **quantitative demonstration of the quintessence-Swampland
tension** first analyzed by Agrawal, Obied, Steinhardt, and Vafa (arXiv:1806.09718). The
model's value is that it *instantiates* that tension in a concrete $K3 \times T^2$ geometry.

### The reframed contribution

Instead of: *"We satisfy the Swampland bound"*

Write: *"We demonstrate that a $K3 \times T^2$ quintessence model with $\lambda = 1.67$
satisfies $|\nabla V|/V = \lambda \ge 1$ (Swampland input) but produces an attractor
$w_\phi \approx -0.07$ incompatible with dark energy, quantitatively recovering the
Agrawal–Obied–Steinhardt–Vafa tension in a concrete geometric context. Resolving this
tension requires either: (a) a multi-field potential that steepens while tracking
$w < -1/3$; (b) a hilltop/plateau potential with a Swampland-compatible slope at large
field values; or (c) accepting that the dark energy is a transient and embedding the
model in a cosmology that predicts its future evolution."*

This reframing:
- Makes the tension a *result*, not a deficiency
- Cites Agrawal et al. 2018 properly (already in the bib)
- Opens a genuine research programme (options a, b, c above)
- Is directly relevant to the ongoing Swampland/cosmology literature

### How to achieve it (step by step)

1. **Add a dedicated subsection** in Part II §"Swampland Formal Verification":
   *"§5.3 — The quintessence-Swampland tension as a quantitative result"*

2. **Compute and state the attractor equation of state explicitly:**
   $$w_\mathrm{attractor} = -1 + \frac{\lambda^2}{3} = -1 + \frac{(1.6724)^2}{3} \approx -0.07$$
   and note that this is $\mathcal{O}(1)$ away from $w = -1$, confirming no acceleration.

3. **State the resolution window:**
   For a single exponential, dark energy requires $\lambda < \sqrt{2}$.
   The Swampland bound requires $\lambda \gtrsim 1$.
   The allowed window is $1 \lesssim \lambda < \sqrt{2}$, which is narrow ($1 < \lambda < 1.414$).
   The best-fit $\lambda = 1.67$ falls outside this window, which is the tension.

4. **Propose the three resolution paths** (a), (b), (c) as a Research Programme box.

5. **Update the abstract** of Part II to reflect this reframing. Replace:
   > *"...qualitative thawing trajectory in the correct direction..."*
   with:
   > *"...we recover the Agrawal–Obied–Steinhardt–Vafa quintessence-Swampland tension
   > in a concrete $K3\times T^2$ geometry, and quantify the resolution window
   > $1 \lesssim \lambda < \sqrt{2}$..."*

6. **Add one sentence to the Lean verification section** noting that the formal result
   `swampland_bound` establishes $|\nabla V|/V = \lambda$, and that the *tension* is the
   statement $\lambda_\mathrm{fit} > \sqrt{2}$, which is a simple real-number inequality
   that could itself be kernel-verified as a one-line `norm_num` lemma:
   ```lean
   theorem lambda_exceeds_sqrt2 : (16724 : ℚ) / 10000 > Real.sqrt 2 := by norm_num
   ```
   *(Note: this requires `Mathlib.Analysis.SpecialFunctions.Pow.Real` and a rational bound
   on $\sqrt{2}$; use `(16724:ℚ)/10000 > 14143/10000` and `(14143/10000)^2 > 2`.)*

### Effort estimate

3–5 days of writing. One new `norm_num` lemma. High impact-to-effort ratio.

### Files to modify

- `manuscripts_and_proofs/Part_II_Vafa_DarkEnergy.tex` — reframe abstract, add §5.3, update conclusion
- `lean4_formal_proofs/Agora/SwamplandK3T2.lean` — add `lambda_exceeds_sqrt2` lemma
- `agora_ai_agents/Physic review.md` — mark B.1 ("tension unaddressed") as resolved
- `agora_ai_agents/Reviewer_Response.md` — add Goal III as a new positive result

---

## Publication target and submission checklist

### Primary target: *Journal of Cosmology and Astroparticle Physics* (JCAP)

JCAP is the correct venue because:
- It accepts string-inspired phenomenology without requiring a complete compactification
- It has a formal-methods-friendly editorial board (increasingly so since 2022)
- The GD-1 exclusion and mass-ratio prediction are exactly the kind of quantitative,
  observationally-grounded results JCAP values
- The Swampland tension framing (Goal III) is directly in scope for current JCAP topical issues

**Fallback:** *Physical Review D* (Letters or Regular Articles), Section on Cosmology and
Astroparticle Physics. PRD requires slightly more complete physics but has higher visibility.

### Submission checklist

#### Before submission (blocking)

- [x] **Goal I (partial):** `s20_recurrence` `sorry` **discharged** — kernel-verified for $n\le8$ (`s20_recurrence_checked`), exact-verified $n\in[0,60]$ (`scripts/verify_s20_recurrence.py`), general law now an explicit `axiom`. Remaining: compile the WZ certificate to upgrade the axiom to a theorem (Phase 4, see `OPEN_PROBLEMS.md`).
- [x] **Goal III:** Reframe Swampland tension as result ✓ Done
  - New §5.3 "The Quintessence-Swampland Tension as a Quantitative Result" added
  - Abstract rewritten to lead with the tension as the positive finding
  - Attractor $w\approx-0.07$ computed and displayed
  - Resolution window $1\lesssim\lambda<\sqrt{2}$ quantified
- [x] **Mirror symmetry label:** Fixed (`K3_DarkMatter_Preprint.tex:65`) ✓ Done
- [x] **Distance Conjecture $\Delta\phi$ estimate:** Added (`Part_II_Vafa_DarkEnergy.tex`) ✓ Done
- [x] **$\epsilon = 0.042/\lambda$ origin:** Disclosed (`Part_II_Vafa_DarkEnergy.tex`) ✓ Done
- [ ] **Title revision:** Change to "A string-inspired algebraic-geometry sieve for fuzzy dark
  matter candidates, with exact-rational formal verification of the GD-1 exclusion"
- [ ] **Author affiliation:** Verify "Independent Researcher / Socrate AI Lab" is acceptable;
  JCAP requires an institutional email for correspondence. Zenodo DOI is acceptable as a
  preprint anchor.

#### Before submission (strongly recommended)

- [ ] **Goal II:** Add schematic compactification scaffold — justifies "string vacua" vocabulary
- [x] **`lambda_fit_exceeds_sqrt2` lemma:** `norm_num` over ℚ, kernel-verifies $\lambda>√2$ ✓ Done
- [x] **`attractor_not_dark_energy` lemma:** `norm_num`, certifies $w_\mathrm{att}+1>0$ ✓ Done
- [x] **Figure 1 revision:** Attractor point $(-0.07, 0)$ added with future trajectory arrow ✓ Done
- [ ] **Lyman-$\alpha$ compatibility check:** The Discussion acknowledges a potential tension
  with Lyman-$\alpha$ from mass-varying dark matter; a quantitative estimate is needed

#### At submission

- [ ] arXiv preprint posted (hep-th or astro-ph.CO cross-listed)
- [ ] Zenodo DOI updated to point to the submitted version
- [ ] GitHub repository tagged `v1.0-submission` with all Lean proofs compiling cleanly
- [ ] Supplementary material: Python notebooks for parameter sweep + SciPy integration
- [ ] Cover letter explicitly scoping the Lean verification claims and acknowledging open
  obligations (`s20_recurrence` if not yet discharged)

---

# PART II — THE LONG FORWARD VIEW (2025–2035 and beyond)

> **Honesty protocol for this entire section.** Everything below is *forward-looking
> interpretation and prediction*, not proven physics. We use a strict three-tier vocabulary
> and never blur the tiers:
>
> - **[VERIFIED]** — kernel-checked in Lean or exact-rational computation. Cannot be wrong
>   given the definitions.
> - **[FITTED]** — a phenomenological parameter calibrated to data ($\lambda=1.6724$,
>   $\epsilon=0.0251$, $f_b=0.05$). Defensible but not derived from first principles.
> - **[PREDICTED]** — a falsifiable consequence that future instruments can confirm or rule
>   out. The value of the theory rests entirely on these surviving contact with data.
>
> No claim in this section "proves" that $\Lambda$CDM is wrong or that string theory is
> realised in nature. The honest standard is: *the $K3\times T^2$ mass-varying framework
> makes a small set of sharp, falsifiable predictions; if the next decade of data matches
> them, the model graduates from phenomenology to candidate physics; if not, it is falsified
> cleanly.* That falsifiability is the asset.

---

## 4. The Grand Interpretation — the "Cosmic See-Saw" hypothesis

The central physical idea unifying the empirical section is a single mechanism: a mass-varying
axion whose mass was **~19% heavier** at recombination ($m_a(z{=}1100)/m_a(0)\approx1.19$,
**[FITTED]** via $\epsilon=0.0251$) and decays as the $T^2$ volume expands. One rolling modulus
drives two opposite-sign effects at the two ends of cosmic time — hence "see-saw."

### A. The Cosmic See-Saw: do JWST and DES $S_8$ share one cause?

**The hypothesis (not yet a proof).** Standard analyses treat the JWST early-galaxy
over-abundance and the DES Y3 / KiDS low-$S_8$ clustering deficit as two unrelated tensions.
The $K3\times T^2$ model proposes they are *the same parameter seen at two redshifts*:

- **Early universe (anchor):** a 19% heavier axion deepens early potential wells, accelerating
  halo collapse and easing the "impossible" massive $z>8$ galaxies (Labbé et al. 2023;
  Boylan-Kolchin 2023).
- **Late universe (smear):** the now-lighter axion has a longer de Broglie wavelength, which
  suppresses small-scale power and lowers $S_8$ toward the observed $\approx0.776$ (DES Y3,
  KiDS-1000).

**Expected result [PREDICTED].** A *single* value of $\epsilon$ should simultaneously fit
the early-galaxy stellar-mass function at $z\in[8,12]$ **and** the late-time $S_8$ deficit.
The model is correct only if the $\epsilon$ that fixes one fixes the other within error bars.

**How to achieve / test it.**
1. Build a joint likelihood $\mathcal{L}(\epsilon) = \mathcal{L}_\mathrm{JWST}(\epsilon)\cdot
   \mathcal{L}_{S_8}(\epsilon)$ over the UNCOVER $z>8$ catalogue and the DES Y3 + KiDS-1000
   $S_8$ posterior.
2. Verify the two single-probe posteriors on $\epsilon$ overlap. **Falsification criterion:**
   if the JWST-preferred $\epsilon$ and the $S_8$-preferred $\epsilon$ are mutually exclusive
   at $>3\sigma$, the see-saw hypothesis is dead.
3. Replace the linear-theory smearing estimate with a proper transfer-function calculation
   (axionCAMB / AxiCLASS with a time-dependent mass).

**Honest status.** Current notebook overlays are *consistency illustrations* at the linear
level with a toy baryon fraction, not a joint fit. Calling them "the same phenomenon proven"
is premature; calling them "a testable unification hypothesis with a single shared parameter"
is exactly right and is what the manuscript should say.

### B. The Quasar $\alpha$-drift and the $\chi^2/\mathrm{dof}\approx2.33$

**What it is.** Keck/HIRES and VLT/UVES quasar absorption spectra show statistical evidence
for fine-structure-constant variation $\Delta\alpha/\alpha\sim-0.57\times10^{-5}$ (Webb,
Murphy, King et al.). The model maps this to EM gauge fields on D-branes wrapping the
expanding $T^2$, giving a drift set by $\lambda\approx1.67$ **[FITTED]**.

**On the $\chi^2$.** A reduced $\chi^2\approx2.33$ on *raw* quasar data is **not a weakness and
not a badge of honor** — it is simply what one expects when the intrinsic astrophysical scatter
(turbulent gas, magnetic fields, wavelength calibration) is large and not folded into the error
model. The honest statement is: *the model captures a consistent monotonic trend through noisy
data without overfitting; a $\chi^2\approx1$ would in fact be suspicious given the known scatter.*
We must not present $2.33$ as evidence of correctness — only as evidence of non-overfitting.

**Expected result [PREDICTED].** The drift should be *monotonic in look-back time* and its slope
should be tied to the **same** $\lambda$ that sets $w_0,w_a$. A consistency relation
$\dot\alpha/\alpha \propto \lambda H_0$ links the spectroscopy to the dark-energy fit.

**How to achieve / test it.**
1. Re-fit the public Keck+VLT $\Delta\alpha/\alpha$ vs $z$ data with the model's one-parameter
   drift law and report the covariance with $\lambda$.
2. Cross-check against the more recent, more stringent ESPRESSO/VLT bounds, which are tighter
   than the historical Webb dipole. **Falsification criterion:** if ESPRESSO null results
   exclude the drift slope implied by $\lambda=1.67$, the D-brane $\alpha$-drift channel is
   falsified independently of the cosmology.

### C. The Epistemic Armor: $f_b=0.05$ and the invitation to N-body teams

**What it is.** The early-galaxy estimate uses a flat baryon-to-stellar conversion fraction
$f_b=0.05$ **[FITTED, deliberately simple]** rather than a full N-body + hydrodynamic halo model.

**Why this is the right call.** Stating the simplification explicitly is honest scientific
hygiene, not a shield. It draws a clean line: *"here is the analytic, linear-theory result;
the nonlinear regime requires a supercomputer."* That is a genuine, standing invitation to the
IllustrisTNG, FIRE, and FLAMINGO collaborations to adopt the predicted mass-varying axion and
run it at scale. The manuscript should phrase it as future work, never as a completed result.

**Expected result [PREDICTED].** A cosmological N-body simulation with a time-dependent axion
mass $m_a(a)\propto a^{\epsilon/3}$ should reproduce both the $z>8$ stellar-mass function and
the $z\sim0.5$ weak-lensing $S_8$ within the same run.

**How to achieve it.** Provide a ready-to-ingest module: the $m_a(a)$ table, the modified
Poisson/quantum-pressure term, and initial transfer functions, packaged so an existing code
(e.g. a modified Gadget/AREPO or PKDGRAV branch) can adopt it without re-deriving the theory.

---

## 5. Experimentation history — the 30-year observational arc

This narrative establishes that the framework is a *culmination of existing observational
anomalies*, not an invention in a vacuum. Each era pairs a real historical observation with the
model's interpretation, clearly flagged as **[INTERPRETATION]**.

### The Past (1990s–2010s): hints of extra dimensions
- **Instruments:** Keck/HIRES, VLT/UVES.
- **Observation:** Webb, Murphy & King reported a statistical drift in the fine-structure
  constant from quasar spectra; widely attributed to instrumental systematics for lack of a
  mechanism.
- **[INTERPRETATION]:** the model reads this as the $T^2$ volume stretching the D-branes that
  carry the electromagnetic gauge field. *Honest caveat: later ESPRESSO measurements tightened
  the bounds substantially; the historical signal is contested and must be presented as such.*

### The Present (2020s): the cracks in $\Lambda$CDM
- **Instruments:** JWST, DES Y3, KiDS-1000, DESI 2024.
- **Observations:** early massive galaxies forming faster than $\Lambda$CDM comfortably allows;
  late-time clustering ($S_8$) lower than the Planck-extrapolated value; DESI BAO hints of
  evolving dark energy.
- **[INTERPRETATION]:** the mass-varying axion threads early-anchor and late-smear with one
  parameter $\epsilon$, and the $T^2$ modulus gives a thawing $w(a)$. *Honest caveat: the
  best-fit $w_0,w_a$ sits outside the DESI $1\sigma$ contour; the model is in the right
  qualitative regime, not a quantitative match.*

### The Future (2025–2035): the falsifiable manifest
See §6. The model's credibility is staked entirely on these predictions, not on retrofitting
present anomalies.

---

## 6. The Falsifiable Predictions Manifest — expected results and how to achieve them

> These mirror and extend `PREDICTIONS.md`. Each entry states the **prediction**, the
> **expected quantitative result**, the **method/instrument**, and the **falsification
> criterion** — the redshift or precision at which the prediction would be ruled out.

### Prediction 1 — Euclid's dynamic $S_8$ gradient

- **Prediction [PREDICTED]:** $S_8$ is not a single redshift-independent number; it exhibits a
  *temporal gradient* tracking the axion mass-decay curve $\epsilon\approx0.0251$.
- **Expected result:** tomographic $S_8(z)$ should *decline* with decreasing redshift at a slope
  set by $\epsilon$; quantitatively, $\Delta S_8 \sim \epsilon \times$ (growth-factor change)
  across Euclid's tomographic bins $z\in[0.2, 2.0]$.
- **Method:** fit Euclid weak-lensing tomography bin-by-bin; compare the fitted $S_8(z)$ slope
  to the model's $\epsilon$-driven prediction.
- **Falsification:** a flat $S_8(z)$ consistent with constant-mass CDM at Euclid precision
  ($\sigma_{S_8}\lesssim0.01$ per bin) falsifies the mass-decay mechanism.

### Prediction 2 — ELT Sandage–Loeb real-time drift

- **Prediction [PREDICTED]:** the redshift drift $\dot z$ measured over a decade follows a
  *thawing* expansion history with $w_0\approx-0.548$, $w_a\approx-0.396$ **[FITTED inputs]**,
  distinguishable from a cosmological constant.
- **Expected result:** $\dot z$ vs $z$ deviates from the $\Lambda$CDM curve at the
  $\sim\mathrm{cm\,s^{-1}\,yr^{-1}}$ level in the redshift range ELT/HIRES targets ($z\sim2$–5).
- **Method:** decade-baseline Lyman-$\alpha$ forest velocity-drift measurement with ELT's
  HIRES spectrograph.
- **Falsification:** a drift curve consistent with constant $w=-1$ at ELT precision rules out
  thawing quintessence with these parameters. *Honest note: do not claim this "disproves
  Einstein's $\Lambda$"; it would disfavour $\Lambda$ relative to this specific thawing model.*

### Prediction 3 — LISA standard sirens and GW leakage into $T^2$

- **Prediction [PREDICTED]:** gravitational-wave luminosity distances deviate fractionally from
  the electromagnetic/GR distance because GWs leak into the expanding $T^2$ volume.
- **Expected result:** a redshift-dependent ratio $d_L^{GW}/d_L^{EM} = 1 + \delta(z)$ with
  $\delta$ growing with distance, set by the $T^2$ expansion rate. Provide the explicit
  functional form $\delta(z;\lambda)$ as a deliverable.
- **Method:** LISA massive-black-hole-binary standard sirens with EM counterparts (or
  statistical host identification), comparing GW distance to redshift.
- **Falsification:** $\delta(z)=0$ within LISA precision rules out the higher-dimensional
  leakage channel. This is the cleanest, most model-independent test of the extra dimension.

### Prediction 4 (new) — Pulsar Timing Array monochromatic lines

- **Prediction [PREDICTED]:** the FDM field sources PTA signals at the corrected periods
  $T\approx7.52$ d ($S_{1,2}$) and $13.08$ d ($S_{2,1}$) — see Part I §"Observational
  Predictions".
- **Expected result:** narrow spectral lines at $f_\mathrm{signal}=2f_\phi$, locked to the
  galactic rest frame (distinguishing them from terrestrial/lunar systematics).
- **Method:** dedicated NANOGrav/EPTA/SKA searches with `enterprise`, using galactic-frame
  phase tracking.
- **Falsification:** absence of excess power at these periods after foreground subtraction.

---

## 7. Execution roadmap — turning predictions into deliverables

| Phase | Deliverable | Method | Status |
|---|---|---|---|
| 7.1 | Joint $\epsilon$ likelihood (JWST $\times$ $S_8$) | axionCAMB/AxiCLASS + UNCOVER + DES Y3 | Planned |
| 7.2 | $\alpha$-drift refit with ESPRESSO bounds | public Keck/VLT/ESPRESSO data | Planned |
| 7.3 | N-body ingestion module ($m_a(a)$ table + quantum-pressure term) | modified Gadget/AREPO branch | Planned |
| 7.4 | $\delta(z;\lambda)$ GW-leakage functional form | analytic + LISA forecast | Planned |
| 7.5 | PTA line-search forecast | `enterprise` injection-recovery | Planned |
| 7.6 | `empirical_crucible` notebook → reproducible pipeline | refactor `Agora_Empirical_Validation.ipynb` | In progress |

**Guiding principle for every deliverable:** publish the *method and the falsification
criterion* alongside the result. A prediction that cannot be killed by data is not science;
the strength of this programme is that all four predictions in §6 can be cleanly ruled out by
instruments already funded and under construction.

---

# PART III — AUTOEVOLVE R2: THE HYPOTHESIS FOUNDRY (2026-07-14 onwards)

## Philosophy

The v1 validation infrastructure that dismantled the overclaims is stronger than any single hypothesis it tests. AutoEvolve R2 turns that infrastructure from a **shield** (protecting against errors) into an **engine** (generating and filtering hypothesis candidates). Inspired by AlphaEvolve (cheap generator + ruthless evaluator) and arXiv:2506.13131 (agentic research), the Hypothesis Foundry couples low-cost LLM generation to the existing CI gates, Lean kernel verification, and anti-circularity ledger as a unified fitness function.

**Core design:** Answer-key classifier controls embedded in the candidate pool. The literature already contains ground truth — Apéry ζ(2) (A005258) is elliptic, Apéry ζ(3) (A005259) is K3-type per Beukers–Peters 1984. If the classifier misidentifies these, everything halts and the classifier is fixed. This converts classifier debugging from a hidden problem into a visible, public gate.

## Phase 8: AutoEvolve R2 (12 weeks, ~85% HAIKU tier, 3 HUMAN gates)

A gate-driven pipeline: **Phase A** (13 candidates via literature review) → **Phase B** (13→5 via exact arithmetic + physics screens, reusing existing tools) → **Phase C** (5→3 via real data tests) → **Phase D** (top-3 implementation + Lean + manuscripts) → **Phase E** (citizen-science integration + archive propagation).

Full task breakdown: **AUTORESEARCH_RELEASE_V2_PLAN.md** (detailed spec) and **TODO.md §0** (task checklist).

### Phase A Deliverable (weeks 1–2)

**Artifact:** `data/autoresearch_v2/candidate_pool.yaml` (13 sequences with geometry assignments, controls verified)

- LR-1: Cross-match v1's $S_{1,2}$/$S_{2,1}$ against OEIS + Apéry literature
- LR-2: Enumerate classified sporadics (Zagier 6×elliptic, Cooper order-3 pool, Domb, others) → ≥15 baseline
- LR-3: Run extended sieve $(A,B)\in[1,8]^2$ + 3-factor family with held-out validation
- LR-4: Archive Lee & Tsai 2026 (Sheffield 5D resonance) + El Naschie 2013 (numerology boundary marker)
- LR-5: Lee–Tsai bridge memo: map their 5D $(R, m_B)$ resonance to our 6D $m_{\mathrm{eff}}(\Delta)$ ansatz
- LR-6: HUMAN gate freeze at exactly 13; controls present

**Kill criterion:** If LR-1 reveals $S_{1,2}$ is a known, misclassified object → adopt literature, rebuild.

### Phase B Deliverable (weeks 3–4)

**Artifact:** `data/autoresearch_v2/selection_13to5_rationale.md` (composite scoring; 5 survivors identified)

- G1-1 to G1-4: Exact-arithmetic screens (recurrence order, Weil bounds, mirror integrality, monodromy computability) — **classifer fails control → halt**
- G2-1 to G2-3: Physics viability (stiffness contours, No-Go check, Dolan superradiance bands)
- GATE-B-SELECT: HUMAN composite score (G1 completeness + monodromy + No-Go + superradiance + control sanity) → rank top 5

### Phase C Deliverable (weeks 5–7)

**Artifact:** `data/autoresearch_v2/selection_5to3_rationale.md` (observational leverage ranking; 3 finalists picked)

- EU-1, JW-1: Acquire Euclid Q1 + JWST UNCOVER (if access blocked → Rule-1 BLOCKED note, no substitute)
- QT-1 to QT-5: Quick observational tests per candidate (KK projections, see-saw t-test with real $\Delta_{\rm early}$, PTA windows, Lee–Tsai overlap, null-hypothesis battery)
- GATE-C-SELECT: HUMAN observational leverage ranking (# tests distinguishable × falsifiability) → pick 3; candidates indistinguishable-everywhere are explicitly disfavored

### Phase D Deliverable (weeks 8–12)

**Artifacts:** (i) `lean4_formal_proofs/Structures/S1X_*.lean` (3 finalist kernel-verified modules); (ii) `manuscripts_and_proofs/Part_VII_Hypothesis_Foundry.tex` (negative-results-first essay); (iii) `docs/observatories/pta_ratio_test_target_dossier.md` (falsifiable targets)

- D-1: Lean kernel verification per finalist (n≤20 decidable recurrence, zero `sorry`)
- D-2: Ledger + CI integration; `cross_consistency_check.sh` extended to finalists
- D-3: Part VII manuscript (3 sections, one per finalist, provenance ledger pattern)
- D-4: External verification invitations (GitHub issues to arithmetic-geometry + PTA communities)
- D-5: Observatory targeting dossier (PTA ratio bands, lensing cross-match targets)

### Phase E: DarkMatterK3-Home Citizen Integration

- **DM-1, DM-2:** Job spec schema + quorum-replication protocol (≥2 independent clients per tile; disagreement → quarantine)
- **DM-3:** Re-run v1 headline numbers (1.177, Δ=47.0) under quorum before re-citation
- **DM-4:** Dispatch Phase C TDA jobs to volunteer network; auto-archive results

### Standing Rule: Anti-Circularity Enforcement

Every parameter must declare its fit target in `PARAMETER_LEDGER.yaml`. CI check: if fit_target appears in the same task's acceptance criteria → task output void. This is the GAP-2 lesson, now mechanical.

## Success Metrics

- **Outcome A:** A candidate with computable monodromy settling its geometry class decisively (v1 never achieved this)
- **Outcome B:** A data-distinguishable candidate pair with a PTA-reachable ratio band whose antecedent is not circular
- **Outcome C:** Honest kill of all 13 candidates with the answer-key-validated classifier — publishable as "closed: the S_{A,B} → dark-sector route is sterile"
- **Methodological win:** Classifier passing controls is itself a publishable validation result (independent reproducible reconstruction of known classifications)

---

# APPENDIX — Current formal-methods status (as of June 2026)

| Theorem | Module | Status |
|---|---|---|
| `cy_axion_no_go` | `Agora.Discovery.FuzzyDarkMatter` | ✓ Kernel-verified |
| `mass_ratio_in_interval` | `Agora.K3_Topology` | ✓ Kernel-verified (new) |
| `V_has_deriv_at`, `swampland_bound` | `Agora.SwamplandK3T2` | ✓ Kernel-verified |
| `lambda_fit_exceeds_sqrt2` | `Agora.SwamplandK3T2` | ✓ Kernel-verified (new) |
| `attractor_not_dark_energy` | `Agora.SwamplandK3T2` | ✓ Kernel-verified (new) |
| `m_eff_pos`, `m_eff_mono`, `m_eff_deriv` | `Agora.Discovery.ChameleonStability` | ✓ Kernel-verified |
| `binomial_sum_equality` | `Structures.TelescopingBinomial` | ✓ Kernel-verified (newly clean) |
| `inv_coupling_ratio_in_interval`, `stiffness_ratio_reduced` | `Agora.GaugeCoupling` | ✓ Kernel-verified (new) |
| `s20_recurrence_checked` ($n\le8$) | `Structures.S20Recurrence` | ✓ Kernel-verified (new, `decide`) |
| `s20_recurrence` (general $n$) | `Structures.S20Recurrence` | ✗ `axiom` (was `sorry`); exact $n\in[0,60]$; WZ = Phase 4 |
| Hodge numbers | `Agora.Conjectures.MirrorSymmetry` | ✗ `axiom` (disclosed) |

---

*This vision document is a living file. Update the checklist items as goals are achieved.*
*Last updated: 2026-07-16 — added Part 0 (Dual-Scale Topological Universe Model governing vision, three parallel streams).*
