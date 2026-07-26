# Stream 2 Phase 4, step 2 — Dolgachev and Doran fetched and READ: the framework verifies verbatim; one named residual (U1) before lattice promotion

**Date:** 2026-07-26 (night) · **Authority:** T0 verbal, this session ("I give you authority to
progress to unblock the situation") · **Companion:** `STREAM2_PHASE4_LATTICE_REFINEMENT_2026_07_26.md`
(step 1: the Γ₀(7)+ computation) · **Sources:** `docs/literature/MANIFEST.md` (both hash-pinned)

---

## 1. What the sources actually say — read, with locations

**Dolgachev, arXiv:alg-geom/9502005 (J. Math. Sci. 81, 1996):**

- **§7 (p.20).** For M = ⟨2n⟩ (degree-2n polarized K3s): M⊥ ≅ U ⊥ U ⊥ E₈ ⊥ E₈ ⊥ ⟨−2n⟩, and
  the mirror lattice is **M_N := (ℤf)⊥/ℤf ≅ U ⊥ E₈ ⊥ E₈ ⊥ ⟨−2N⟩**. Then, verbatim:
  *"The mirror family K_M̌ is one-dimensional … We have **(Mₙ)⊥ = U ⊥ ⟨2n⟩**."*
- **Theorem 7.1.** The stabilizer Γ′_{Mₙ} of the connected period component satisfies
  **Γ′_{Mₙ} = Γ₀(n)+** (up to PSL₂(ℝ)-conjugation), and *"in particular **K_{Mₙ} ≅ H/Γ₀(n)+**"* —
  the moduli space of Mₙ-polarized K3 surfaces IS the Fricke modular curve X₀(n)+.
- **Theorem 7.3.** The **ample** locus is H/Γ₀(n)+ minus an explicit countable set S of special
  orbits — the source-level form of our standing "very general member; ρ jumps on a countable
  dense subset" caveat.
- **Theorem 7.5.** When X₀(n)+ is rational there is a canonical Hauptmodul with **integer**
  Fourier coefficients and a simple point at the cusp, generating the function field.

**Doran, arXiv:math/9812162 (Comm. Math. Phys. 212 (2000) 625–647):**

- **Theorem 5.13.** *"The Picard–Fuchs equation of a family of Mₙ-polarized K3 surfaces is the
  **symmetric square** of a second order homogeneous linear Fuchsian ODE."* Proof route: order
  = rank T = 22 − 19 = 3; the period domain lies on a nondegenerate quadric in ℙ²
  (Dolgachev's Torelli); Corollary 5.8 (a fundamental system satisfying a nondegenerate
  quadric ⇒ symmetric square, via Singer's Lemma 5.7).
- **§6.** The Sym² structure *"immediately extends to the general rank 19 lattice polarized
  case"* — and, load-bearing for honesty: *"What is **lacking** in the general setting is a
  complete classification of the rank 19 lattices."*

## 2. Where H-M7 stands now

Fingerprint match, all legs now verified at source or computed in-repo:

| leg | statement | status |
|---|---|---|
| 1 | our PF operator L₃ = Sym²(L₂) | **[A]** kernel-proven (Stream 1) |
| 2 | ρ = 19, T = 3 (very general member) | **[B]** E-011 |
| 3 | the family's moduli coordinate is a Γ₀(7)+ Hauptmodul | **[B]** computed (step 1, κ=49) |
| 4 | Mₙ-polarized ⇒ moduli = X₀(n)+, T = U⊕⟨2n⟩, PF = Sym² | **READ** — Dolgachev Thm 7.1/§7, Doran Thm 5.13 |

**The one residual before promoting the lattices themselves — U1 (uniqueness):**
legs 1–4 show our family *looks exactly like* the M₇-polarized family in every invariant we
can compute, and the framework says M₇-polarized families have exactly these invariants. What
is not yet shown is the **converse**: that Γ₀(7)+ as uniformizing group *characterizes*
T ≅ U ⊕ ⟨14⟩ among even rank-3 lattices of signature (2,1) — Doran's own §6 flags precisely
this classification as open in general. U1 is a bounded, well-posed question (one-class-genus
of U⊕⟨14⟩ / the rank-3-lattice ↔ Eichler-order correspondence at level 7), answerable by a
genus computation or a further citation — **not** by tonight's assertion.

**Therefore: no C2 v4 certificate is emitted.** `C2_cooper_s7_v3.json` (ranks only) remains
live. H-M7 (NS = U⊕E₈²⊕⟨−14⟩, T = U⊕⟨14⟩) stays **[C]**, now with its promotion condition
narrowed from "fetch and read two papers" (done) to "discharge U1" (one question).

## 3. Consequence for the S3-00 2(b) T0 decision

Unchanged in direction, sharpened in content: the replacement-input route is **real and one
step from citable**. If U1 discharges, S3-00 2(b)'s dead "Kodaira fibre data" input is
replaced by an explicit lattice with an E₈⊕E₈ root system — and the T0 choice becomes
"re-scope 2(b) at lattice level" vs "strike", instead of "strike" by default. Recommend the
decision continue to hold until U1 is resolved (fast) — and note WP-E5's E2.17 means even a
re-scoped 2(b) mechanism may honestly land as "signature untestable + the two numbers"
(see the Stream 3 findings response, same date).

## 4. Next Stream 2 work items, in order

1. **U1**: compute the genus of U ⊕ ⟨14⟩ (class number 1?) or locate the classification
   citation; negative-controlled checker if computational.
2. On U1-PASS: emit `C2_cooper_s7_v4.json` (lattices [B], citations per-statement), update
   Phase 4 memo, put the S3-00 2(b) re-scope option to T0.
3. s10 analogue (level 10, (ℤ/2)² Atkin–Lehner): needs its Hauptmodul coordinate landed in
   `refs/` first; **still deliberately deferred**.

**Generated-by:** Fable 5 (Stream 2) | **Verified-by:** direct read of both PDFs (text layers
extracted in-repo; quotes located by line in the .txt extractions); hashes in
`docs/literature/MANIFEST.md` | **Reviewed-by:** Xavier (T0) — pending
