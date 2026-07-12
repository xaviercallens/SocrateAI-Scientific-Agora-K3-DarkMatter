# GAP-2 Stiffness Pipeline: How 1014 and 336 Are Actually Computed (Task T2.1)

This document traces, with zero unexplained steps, exactly how the two integers
`V''(0) = 1014` (for $S_{1,2}$) and `V''(0) = 336` (for $S_{2,1}$) — asserted in
`PARAMETER_LEDGER.yaml` and kernel-verified (as a *ratio*, not a derivation) in
`lean4_formal_proofs/Agora/GaugeCoupling.lean` — are computed from the underlying
Picard-Fuchs recurrence data. It does **not** address whether this quantity is
correctly identified with the physical curvature of an axion potential — that
question is the subject of the companion memo
`docs/derivations/stiffness_to_potential.md` (Task T2.2).

**Regression test:** `tests/test_stiffness_values.py` recomputes both integers
from scratch with exact rational arithmetic (Python `fractions.Fraction`, no
floats) and asserts they equal 1014 / 336. Run: `pytest tests/test_stiffness_values.py -v`.

---

## The chain, step by step

### Step 0 — Input: the sequence itself

$$u(n) = S_{A,B}(n) = \sum_{k=0}^{n} \binom{n}{k}^A \binom{n+k}{k}^B$$

with $(A,B)=(1,2)$ for $S_{1,2}$ and $(A,B)=(2,1)$ for $S_{2,1}$. This is the
same sequence whose order-3 Picard-Fuchs recurrence identifies it as a K3
period (GAP-1; note $S_{2,1}$ is now known to be order-2/elliptic instead —
see `docs/gap1/ORDER_VERIFICATION_FINDINGS.md` — a fact this stiffness
pipeline does not itself depend on, since it only uses $u(n)$ directly, not
the recurrence order).

Computed at: `scripts/mirror_map_integrality.py::compute_u_and_c` (exact
integers, `math.comb`), or equivalently `scripts/k3_sieve_analysis.py::get_u_v`
(floating point, used only for the sieve table — see the cross-check below).

### Step 1 — The logarithmic second solution's coefficients $c(n)$

The Frobenius/mirror-map recipe (standard for a MUM point at $z=0$; see e.g.
Zagier "Arithmetic and topology of..."; Almkvist-Zudilin) needs the
coefficients of the log solution $y_1(z) = y_0(z)\log z + \tilde y(z)$, where
$y_0(z) = \sum u(n) z^n$. These are obtained by differentiating each binomial
factor at $n \to n+\epsilon$ and setting $\epsilon=0$:

$$c(n) = \sum_{k=0}^n T(n,k)\Big[A\big(H_n - H_{n-k}\big) + B\big(H_{n+k}-H_n\big)\Big],
\qquad T(n,k) = \binom{n}{k}^A\binom{n+k}{k}^B$$

where $H_m$ is the $m$-th harmonic number ($H_0 := 0$). This is an **exact
rational** number for every $n$ (a finite sum of rationals).

Computed at: `scripts/mirror_map_integrality.py::compute_u_and_c`, lines
computing `dlog = A*(Hn-Hnk) + B*(Hnpk-Hn)` and `csum += term*dlog`.

### Step 2 — The mirror map $q(z)$

Standard construction: $q(z) = z\exp(\tilde y(z)/y_0(z))$ (the $\log z$ terms
cancel by construction). Implemented as two formal power-series operations
over exact rationals:

1. `ratio(z) = ỹ(z)/y0(z)` via power-series division (`series_div`).
2. `q(z)/z = exp(ratio(z))` via the power-series exponential recurrence
   `n·g_n = Σ_{k=1}^n k·f_k·g_{n-k}` (`series_exp`).

Computed at: `scripts/mirror_map_integrality.py::mirror_map_coefficients`.
Output: `q_over_z_coefficients[d-1]` $= q_d$ for $d=1,2,\dots$ — i.e. index 0
of that array is $q_1$, index 1 is $q_2$, etc.

**Integrality** of these $q_d$ (a necessary signature of genuine K3/CY
periods, Lian-Yau integrality) was independently checked for the first 30
coefficients under Task T1.3 (`data/mirror_map/S12_qcoeffs.json`,
`S21_qcoeffs.json`) — both sequences pass. This document only needs $q_1,q_2,q_3$.

**Values** (exact, reproduced by `tests/test_stiffness_values.py`):

| $d$ | $q_d(S_{1,2})$ | $q_d(S_{2,1})$ |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 8 | 5 |
| 3 | 109 | 35 |

### Step 3 — The instanton-sum axion potential ansatz

The mirror-map coefficients $q_d$ are re-interpreted as instanton weights in
a cosine-sum axion potential (the standard Svrcek-Witten form):

$$V(x) = \Lambda^4 \sum_{d=1}^{D} q_d\big(1-\cos(dx)\big), \qquad x=\phi/f_a$$

(implemented for $S_{20}$ specifically in `scripts/extract_axion_potential.py`,
which builds this exact sum and Taylor-expands it in `sympy`; the physical
$S_{1,2}/S_{2,1}$ pipeline computes the needed derivative directly — see
Step 4 — without building the full symbolic $V(x)$).

**This re-interpretation — that the abstract mirror-map coefficients of a
Picard-Fuchs period are the same numbers as the instanton weights of a
physical D-brane axion potential — is an assumption, not a derivation from
first principles. It is the central subject of `stiffness_to_potential.md`
(T2.2), not re-litigated here.**

### Step 4 — $V''(0)$, the "stiffness"

$$V''(0) = \Lambda^4 \sum_{d=1}^{D} q_d\, d^2$$

(differentiate the cosine sum twice at $x=0$: $\frac{d^2}{dx^2}[1-\cos(dx)]_{x=0} = d^2$).
Setting $\Lambda^4=1$ (the value normalizes out of any *ratio*, which is the
only kernel-verified quantity — see `GaugeCoupling.lean`'s own scope
disclosure), and **truncating at $D=3$** (not the $D=5$ that `q` was computed
to — this specific truncation choice is not otherwise justified in the code
and is flagged here, not smoothed over):

$$V''(0) = \sum_{d=1}^{3} q_d\, d^2 = q_1\cdot 1 + q_2\cdot 4 + q_3\cdot 9$$

Computed at: `scripts/k3_sieve_analysis.py:191`,
`V_double_prime = sum(q_int[d] * (d**2) for d in range(1, 4))`.

**Arithmetic (reproduced exactly by the regression test):**

| | $q_1\cdot1$ | $q_2\cdot4$ | $q_3\cdot9$ | **Sum** |
|---|---|---|---|---|
| $S_{1,2}$ | $1$ | $32$ | $981$ | **1014** |
| $S_{2,1}$ | $1$ | $20$ | $315$ | **336** |

Both match `PARAMETER_LEDGER.yaml`'s `stiffness_S12`/`stiffness_S21` and
`GaugeCoupling.lean`'s `stiffness_S12`/`stiffness_S21` definitions exactly.

### Cross-check: the float pipeline vs. the exact pipeline

`k3_sieve_analysis.py` computes $q_d$ in **floating point**
(`get_u_v`/`get_mirror_map`, using `numpy` floats) and rounds to the nearest
integer for the sieve table's `V''(0)` column — a different code path from
the exact-rational one in `mirror_map_integrality.py` (Step 1–2 above).
`tests/test_stiffness_values.py::test_float_pipeline_agrees_with_exact_pipeline`
verifies these two independent implementations agree after rounding, for
both sequences, up to $d=3$. They do.

### Why only up to $D=3$?

No first-principles justification for truncating the instanton sum at $D=3$
(rather than $D=5$, which is how far $q$ was already computed, or any other
value) appears anywhere in the codebase, commit history, or manuscripts as
of this writing. This is exactly the kind of unexplained step T2.1 was
scoped to surface, not silently accept — flagged here and carried into
`stiffness_to_potential.md`'s "Assumed" list as an explicit, named gap.

---

## Summary: the full chain with zero unexplained steps (modulo the $D=3$ flag above)

$$
S_{A,B}(n) \;\xrightarrow{\text{Step 1}}\; c(n) \;\xrightarrow{\text{Step 2 (series div + exp)}}\; q_d
\;\xrightarrow{\text{Step 3 (instanton ansatz, ASSUMED)}}\; V(x)
\;\xrightarrow{\text{Step 4}}\; V''(0) = \textstyle\sum_{d=1}^{3} q_d d^2
$$

giving $1014$ for $S_{1,2}$ and $336$ for $S_{2,1}$, both reproduced exactly
by `tests/test_stiffness_values.py` from Step 0 with no reliance on any
previously-computed/cached value.
