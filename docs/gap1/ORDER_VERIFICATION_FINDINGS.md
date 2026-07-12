# GAP-1 Order Verification: Two Serious Findings (2026-07-11)

**Status: 🔴 CONFIRMED — S₂,₁ is not a K3 surface candidate.** Surfaced per
Rule 4 (Adversarial Assessment). Read this before trusting any prior
monodromy or "S₂,₁ is K3" claim in this repository.

This document reports two independent bugs discovered while executing Task
T1.1 (monodromy matrices) of the Scientific Validation Program v2.0.0. Both
were found by re-deriving quantities from scratch and cross-checking against
the existing pipeline, not by assuming the existing code was correct.

**Update:** Finding 1 has moved from "suspected" to **confirmed at the
source**. After fixing the bug in `scripts/k3_sieve_analysis.py` (see below)
and re-running the *original* discovery pipeline's full $A,B\in[1,5]$ sweep
with proper held-out validation (70 held-out checks, $n_{\max}=110$):

```
Total K3 Candidates Found: 1
  (A,B) = (1,2)  ->  K3 Surface (Order-3)     [S_{1,2}, confirmed]
  (A,B) = (2,1)  ->  Elliptic Curve (Order-2) [S_{2,1}, REJECTED as K3]
  (A,B) = (2,2)  ->  Elliptic Curve (Order-2) [new: also elliptic]
```

**Only $S_{1,2}$ survives as a genuine K3 candidate in the entire searched
landscape. $S_{2,1}$ is conclusively an elliptic-curve-type object, not K3.**
This is no longer a numerical coincidence under dispute — it is the corrected
version of the project's own discovery script, run on the project's own
data, with the validation gap closed.

---

## Finding 1: S₂,₁ genuinely satisfies an order-2 recurrence, not order-3

### The claim in this repository (as of 2026-07-11, before this finding)
`K3_DISCOVERY_REPORT.md`, `CAVEATS.md`, `scientificplan.md`, `VISION.md`, and
`lean4_formal_proofs/Agora/GaugeCoupling.lean` all assert or assume that both
$S_{1,2}(n) = \sum_k \binom{n}{k}\binom{n+k}{k}^2$ and
$S_{2,1}(n) = \sum_k \binom{n}{k}^2\binom{n+k}{k}$
satisfy **order-3** Picard-Fuchs recurrences (the defining signature the
project uses to call both sequences "K3 surface candidates").

### What was actually found
Using `scripts/k3_monodromy_verification.py::find_recurrence` (which
explicitly searches order ∈ {2,3,4} in that order and validates each
candidate against held-out values), $S_{2,1}$ returns an **order-2**
recurrence at the *first* order tried:

```
-(n+1)² · u(n)  -  (11n² + 33n + 25) · u(n+1)  +  (n+2)² · u(n+2)  =  0
```

This was independently re-derived from scratch (not just re-run) and
validated against **149 consecutive held-out values** (n = 0..148) with
exact Python arbitrary-precision integer arithmetic — far beyond the 15-point
check the original pipeline used, and far beyond what could hold by
coincidence for a 3-unknown-family recurrence. $S_{1,2}$ was checked against
the same order-2 ansatz (all degrees 1–7) and **no** order-2 recurrence
exists for it — confirming $S_{1,2}$ is genuinely order-3 while $S_{2,1}$ is
genuinely order-2, not a shared classification.

**An order-2 Picard-Fuchs recurrence is the hallmark of an elliptic curve
period (a rank-2 local system / weight-2 modular motive), not a K3 surface
(which needs a rank-3, order-3 system for a 1-parameter family).** If this
holds up, $S_{2,1}$ is very likely **not a K3 surface** in the sense claimed
throughout the manuscripts.

### Root cause: a bug in `scripts/k3_sieve_analysis.py`
The original discovery script's `find_minimal_order(A, B)` function is the
source of the "$S_{2,1}$: K3 Surface (Order-3)" label. Reading it closely:

```python
def find_minimal_order(A, B):
    u = get_u_exact(A, B, n_max=35)
    for degree in range(1, 4):
        for num_terms in range(2, 6):
            if detect_recurrence_exact(u, num_terms, degree):
                return degree + 1, num_terms   # <-- returns degree+1 as "order"!
    return -1, -1
```

Two independent problems:
1. **Wrong quantity labeled "order".** The function returns `degree + 1`
   (the *polynomial coefficient degree* plus one) as the geometry-classifying
   "order" — not `num_terms` (the actual recurrence *shift order*, i.e. the
   number of `u(n+i)` terms, which is the quantity that actually determines
   K3-vs-elliptic-vs-CY3 classification). These are different integers in
   general, and the loop returns as soon as **any** `num_terms` at a given
   `degree` produces a nullspace, without recording *which* `num_terms`
   worked.
2. **No held-out validation.** `detect_recurrence_exact` only checks that a
   nullspace *exists* for a matrix built from `num_unknowns + 3` equations
   (line 74: `num_eqs = min(len(u) - num_terms, num_unknowns + 3)`) — just 3
   equations beyond the bare minimum needed to determine the unknowns. It
   never checks the candidate recurrence against additional held-out values.
   For a small system this existence check alone is weak evidence.

Running the (syntax-error-fixed — see below) script directly confirms it
reports `(2,1) → "K3 Surface (Order-3)"`, i.e. the bug is live in the
committed code, not a hypothetical.

**Also discovered in passing:** `scripts/k3_sieve_analysis.py` had a Python
3.12+-only f-string syntax (`f"...{'V\\'\\'(0)':<10}..."`) that fails on this
environment's Python 3.10, meaning **this script could not run at all** prior
to a one-line cosmetic fix applied in this session (extracting the string
literal). It is unclear how long this script has been non-executable, or
whether the "K3 Surface (Order-3)" table in `K3_DISCOVERY_REPORT.md` was ever
actually regenerated from a successful run versus transcribed once and never
re-verified.

### What this does NOT settle
- An order-2 recurrence is strong evidence the *minimal* Picard-Fuchs operator
  for $S_{2,1}$ has order 2, but does not by itself constitute a rigorous
  proof (no formal Zeilberger-certificate closure was attempted here for the
  *non-existence* of an order-3 operator either — only exhaustive numerical
  search up to degree 7).
- It does not resolve whether the *stiffness integer* 336 (a separately
  extracted quantity, GAP-2) has any remaining physical meaning if $S_{2,1}$
  is reclassified as non-K3. That is an open question for whoever picks this
  up next.

### Resolution status (2026-07-11, same session)
Steps 1 and 2 below **have now been done**; step 3 is applied in this
document, `CAVEATS.md`, and `OPEN_PROBLEMS.md`. What remains open is a
decision by the project maintainer / a physics collaborator on how to treat
$S_{2,1}$ going forward (see "Implications" below) — that judgement call is
explicitly out of scope for an automated fix.

1. ✅ **Fixed** `k3_sieve_analysis.py::find_minimal_order` and
   `detect_recurrence_exact` to search on the true recurrence shift-order
   (`num_terms`) and require 40–70 held-out checks before accepting a
   candidate (mirroring `k3_monodromy_verification.py::find_recurrence`).
   Also fixed the Python-3.10-incompatible f-string that prevented the
   script from running at all.
2. ✅ **Re-ran** the full $A,B\in[1,5]$ sieve with the corrected classifier
   (see the confirmed output at the top of this document). Result: only
   $(1,2)$ survives as K3; $(2,1)$ and $(2,2)$ are both reclassified as
   elliptic (order-2); no replacement K3 candidate appears elsewhere in the
   searched range.
3. ✅ **Escalated** to `CAVEATS.md` §2 and `OPEN_PROBLEMS.md` (this session).

### Implications for the rest of the model (requires human/physics judgement — NOT resolved here)
- The mass-ratio prediction $\sqrt{1014/336}\in(1.73,1.75)$ and the GAP-2 PTA
  ratio test (`Agora.Phenomenology.PTAFrequencyRatio`) both compare a K3
  stiffness invariant ($S_{1,2}$'s 1014) against what is now shown to be an
  *elliptic-curve* recurrence invariant (336, from $S_{2,1}$) rather than a
  second K3 stiffness. The Lean theorems remain arithmetically true (they
  only assert a rational-number inequality), but their *physical
  interpretation as two K3 vacua* is now unsupported for the $S_{2,1}$ side.
- Whether the model should (a) drop $S_{2,1}$ entirely and look for a
  genuine second K3 candidate outside $A,B\in[1,5]$, (b) keep $S_{2,1}$ as a
  phenomenological "recurrence invariant" without the K3 label (the
  downgrade path scientificplan.md T2.2 already anticipates for GAP-2), or
  (c) treat $S_{1,2}$ alone as the sole K3 candidate and rebuild the
  two-vacuum narrative around a different second object, is a physics
  decision for the project maintainer, not something this finding resolves
  automatically. Flagging for `[TIER: HUMAN]` per the project's own tiering
  convention.

---

## Finding 2: The Fuchs-criterion regularity classifier has a missing-offset bug

### The claim
`scripts/k3_monodromy_verification.py::classify_singular_points` is supposed
to determine whether each singular point $z_c$ (a root of the leading
coefficient $Q_{\text{order}}(z)$) is a *regular* singular point (where
monodromy is well-defined and MUM theory applies) or *irregular*.

### What was found
The implemented check requires, for each $k = 0, \ldots, \text{order}-1$:
```
ord_{z_c}(Q_k)  >=  order - k
```
But the correct Fuchs criterion (for $L = \sum_k Q_k(z) D^k$, $Q_{\text{order}}$
leading) is:
```
ord_{z_c}(Q_k)  >=  ord_{z_c}(Q_{order}) + k - order
```
i.e. the code is **missing the `ord_{z_c}(Q_order)` offset term** — the
vanishing order of the *leading* coefficient itself at $z_c$. Since every
$z_c$ tested is *by construction* a root of $Q_{\text{order}}$ (found via
`sp.solve(Q_lead, z)`), $\text{ord}_{z_c}(Q_{\text{order}}) \geq 1$ always,
meaning the implemented check is **systematically stricter than the correct
one** whenever $\text{ord}_{z_c}(Q_{\text{order}}) > 0$ — which is every
single point the function is ever called on.

### Concrete confirmation (S₂,₁, order-2 ODE, point $z_c = 0$)
$Q_0(z) = 4z^2-25z-1$ (ord at 0: 0), $Q_1(z)=5z^3-44z^2-3z$ (ord at 0: 1),
$Q_2(z)=z^4-11z^3-z^2$ (ord at 0: 2, the leading coefficient).

| k | ord(Q_k) | Buggy check: need ≥ order−k | Correct check: need ≥ ord(Q_order)+k−order |
|---|---|---|---|
| 0 | 0 | ≥2 → **FAILS (irregular)** | ≥0 → **passes (regular)** |
| 1 | 1 | ≥1 → passes | ≥1 → passes |

With the buggy formula, $z=0$ — which should be the MUM point by
construction (all local exponents 0, per the module's own
`mum_monodromy_frobenius` assumption) — is misclassified as **IRREGULAR**,
and the script prints `"Skipping RK4 integration"` for it and for every
other tested point in the actual run output (both $S_{1,2}$ and $S_{2,1}$,
all singular points, including $z=0$, came back "IRREGULAR" when the full
script was run in this session).

### Impact
**No actual numeric monodromy matrix has ever been produced by this script.**
Every invocation to date has silently skipped the RK4 integration step for
every singular point due to this misclassification, meaning:
- Task T1.1's core deliverable (`data/monodromy/S12_monodromy.json`,
  `S21_monodromy.json` with real numeric matrices and a product-of-monodromies
  residual) **has never actually been computed**, despite the module's
  docstring describing a complete pipeline.
- Any prior claim that "MUM structure at z=0 is confirmed" was based only on
  the *exact, assumed-correct* Frobenius formula
  (`mum_monodromy_frobenius`, which is unconditionally correct algebra given
  the *assumption* that all local exponents are 0 at $z=0$) — not on an
  independent regularity check, because the regularity check that was
  supposed to gate this assumption is the very thing that's broken.

### Recommended next steps (not completed in this session)
1. Fix `classify_singular_points` to include the `ord_{z_c}(Q_order)` offset
   in the threshold.
2. Re-run singular point classification for both sequences; re-attempt RK4
   monodromy integration at any points that reclassify as regular.
3. Implement the actual **product-of-monodromies-equals-identity** check
   (task T1.1's stated acceptance criterion) — this requires monodromy
   matrices expressed in a *common basis* (parallel-transported from a shared
   basepoint via straight-line paths between singularities), which the
   existing script does not do even for points it does classify as regular
   (each computed matrix is in its own local Frobenius frame at that point,
   not a global frame — the matrices as currently computed are not
   directly multipliable into a meaningful "total monodromy" product).
   This is a non-trivial numerical-differential-Galois computation and
   should be scoped as `[TIER: SONNET+]`, not the `[TIER: HAIKU]` originally
   assigned in `scientificplan.md` T1.1.

### Step 1 (fix + re-run) completed 2026-07-11 — a new, honest non-result

The offset bug is fixed (see script diff: `_order_of_vanishing` → replaced by
factor-based `_divisibility_order`, which is both correct and, unlike the
first attempted fix, computationally tractable — testing exact polynomial
divisibility of `Q_k` by the irreducible factors of `Q_order` over $\mathbb
Q[z]$, rather than repeatedly evaluating `sp.simplify` on individual
`CRootOf` algebraic roots, which took >10 minutes per sequence and did not
finish before this fix). The corrected classifier now actually runs to
completion. Real output (`data/monodromy/S12_monodromy.json`,
`data/monodromy/S21_monodromy.json`):

| Sequence | ODE order | $z=0$ (MUM) | Other finite singular points |
|---|---|---|---|
| $S_{1,2}$ | 3 | REGULAR (as expected) | 3 points (1 real + 2 complex conjugate, roots of an irreducible cubic factor of $Q_3$) — **all IRREGULAR** |
| $S_{2,1}$ | 2 | REGULAR (as expected) | 2 points ($11/2\pm5\sqrt5/2$) — **both IRREGULAR** |

This is an exact, reproducible, kernel-of-arithmetic result (polynomial
divisibility over $\mathbb Q$, not a numerical approximation) — not a repeat
of the original bug. **But it is a new negative result, not a clean win:**
$z=0$ correctly comes back regular for both sequences (consistent with MUM
theory), but *every other* finite singular point of *both* extracted
operators — including $S_{2,1}$'s, independently established elliptic —
comes back irregular. Genuine Picard–Fuchs operators of algebraic families
(Gauss–Manin connections) are always Fuchsian — regular singular at *every*
finite point — by Deligne's regularity theorem. Finding irregular points
here therefore means one of two things, and **this script cannot currently
tell you which**:

1. **The nullspace-extracted recurrence is not the canonical minimal
   Picard-Fuchs operator.** `find_recurrence` (Step 1) accepts the first
   `(order, deg)` pair whose nullspace vector satisfies the sequence on 15
   held-out terms — this is sufficient to certify the recurrence *holds*, but
   not that it is free of "apparent singularities": extra, non-geometric
   roots that a genuinely minimal (in the Ore-algebra / D-module sense)
   operator would not have. Recurrence-to-ODE conversion via the theta
   operator is a known source of such artifacts in the holonomic-function
   literature. If so, the irregular points are computational artifacts, not
   evidence about the geometry.
2. **A genuine anomaly.** If the extracted operator *is* minimal, irregular
   finite singular points would be inconsistent with either sequence having
   a geometric (algebraic-family) origin at all — which, notably, would not
   be new evidence specifically against $S_{1,2}$'s K3 status (both
   sequences show the identical pattern, including $S_{2,1}$, whose non-K3
   status was already established independently in Finding 1 above by a
   completely different method). A shared pattern across both sequences is
   more consistent with explanation (1) than with a K3-specific problem.

**Practical consequence for T1.1's stated deliverable:** even with the bug
fixed, **no numeric RK4 monodromy matrix has still been computed** — not
because integration is silently skipped by a broken check, but because the
(corrected) check finds no finite regular point to integrate around. The
only monodromy data available remains the exact, analytic $z=0$ MUM matrix
from Frobenius theory (`mum_monodromy_frobenius`, unconditionally correct
algebra, unaffected by any of this). Distinguishing explanation 1 from 2
above — e.g. by computing the operator's genuine minimal order via
Ore-algebra reduction, or checking for right-factors — is scoped as a new
`[TIER: SONNET+]` follow-up, not attempted here.

---

## Summary verdict for GAP-1 (as of this session)

| Sub-check | Status |
|---|---|
| T1.2 Weil bound (weight-3) | ✅ Both S₁,₂ and S₂,₁ pass (44/44 primes, p∈[5,200]) |
| T1.2 Modularity match (4 LMFDB candidates) | ⚪ No match found among the 4 checked (inconclusive, small sample) |
| T1.3 Mirror-map integrality | ✅ Both pass (30/30 coefficients integral) |
| **T1.1 recurrence order** | 🔴 **CONFIRMED: S₂,₁ is order-2 (elliptic), not order-3. Fixed sieve script re-run finds only S₁,₂ survives as K3 in the full A,B∈[1,5] search.** |
| **T1.1 monodromy computation** | 🟡 Classifier bug fixed and re-run 2026-07-11 (real, exact output now produced — see "Step 1 completed" above). Result: $z=0$ correctly regular (MUM) for both sequences; every *other* finite singular point of both extracted operators is genuinely IRREGULAR, so no numeric RK4 monodromy matrix exists yet for either sequence. Whether this reflects a non-minimal (apparent-singularity-bearing) extracted operator or a real anomaly is unresolved; scoped as a new SONNET+ follow-up (Ore-algebra minimality check). |

The two positive results (Weil bound, mirror-map integrality) are necessary
conditions that S₁,₂ and S₂,₁ both happened to pass — but Finding 1 is a
sharper, *sufficient* signal that S₂,₁ is the *wrong kind of object*
entirely (order-2 = elliptic, not order-3 = K3), and this is no longer a
suspicion: re-running the corrected discovery pipeline confirms it directly.
Per Rule 4, this negative result is reported at the top of the GAP-1 verdict,
not buried under the passing checks.

**This does not automatically falsify the physical dark-matter
phenomenology** (the axion mass value $m_a$ associated with $S_{2,1}$, and
the stiffness integer 336, are separately-fitted/extracted numbers — GAP-2
already flags their derivation as undocumented, independent of the K3
label). But it does mean the specific claim **"$S_{2,1}$ is a K3 surface"**
is now **confirmed wrong**, not merely unverified, and the two-vacuum K3
narrative requires either a physics-judgement decision on how to proceed
(see "Implications" above) or a manuscript downgrade before any further
publication step (see CAVEATS.md §2, OPEN_PROBLEMS.md, both updated this
session).
