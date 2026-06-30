# Open Problems & Call for Collaboration

**Project:** Agora Dark Sector — a *string-inspired* $K3\times T^2$ phenomenological model
**Status:** string-inspired EFT with an exact-rational algebraic sieve and targeted Lean 4 verification
**Posture:** This document is an explicit, honest map of what the model does **not** yet establish. We are **not** asking for a review — we are offering a **partnership**. Several gaps below require top-down string-theory expertise and topological databases (e.g. Kreuzer–Skarke) that an automated symbolic/formal pipeline cannot honestly supply. Fabricating those values would violate our *Zero Simulation Flottante* rule, so we leave them open and labelled.

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
- propose a concrete $K3\times T^2$ orientifold whose K3 fibre is in the $S_{1,2}$/$S_{2,1}$ algebraic family;
- specify integer flux quanta and verify tadpole cancellation;
- write down the Euclidean brane-instanton action that would *derive* (not fit) the axion mass scale.

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

- **Exact algebraic sieve** over $\mathbb Q$ isolating $S_{1,2}$, $S_{2,1}$ as the order-3 survivors in $A,B\in[1,5]$.
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

---

## How to engage

Open a GitHub issue or PR (formal Lean 4 counter-proofs and corrections welcome), or contact the author. Suggested venues for the joint result: **Physical Review D** or **JCAP**. We are explicitly seeking co-authors for items 1, 2, and 4.
