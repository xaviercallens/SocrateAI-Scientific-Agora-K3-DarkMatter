# GATE D-1 Decision Record

**Date:** 2026-07-15 · **Tier:** Sonnet (executed directly; deviates from the
plan's Haiku-executes/Sonnet-reviews split per explicit user instruction) ·
**Authority:** Preregistered decision rule (K3xT2_DEEP_IMPROVEMENT_PLAN.md §3, D-1.3)

## Critical prerequisite finding (discovered during D-1 setup)

The `COOPER_S7_EXACT` array hardcoded in `lss_tensor_analytics/cooper_s7_periods.py`
(committed in the prior "Phase 1" session, commit c704833) was **fabricated**:
it satisfies neither the Lean-verified Cooper s₇ Picard-Fuchs recurrence nor
OEIS A183204 (confirmed by direct b-file fetch: `1,4,48,760,13840,...`, not
`1,13,271,6721,184561,...`). This is a Rule-1 violation (hand-typed/unverified
numbers) that invalidated every "Δ_s7" statistic computed in that session,
including the reported "discovery" of Δ_s7 = 663.4.

**Fixed:** `cooper_s7_periods.py` now computes terms directly from the exact
combinatorial definition (`Σ_j C(n,j)²C(2j,n)C(j+n,j)`), self-verifies against
the recurrence at import time, and matches the OEIS b-file exactly. A new
generalized, multi-kernel module `lss_tensor_analytics/k3_kernel_engine.py`
was built specifically to prevent this class of bug recurring (no kernel's
sequence is ever hardcoded as a literal array — all are computed and
self-verified against their Lean recurrences and cross-checked against OEIS
b-files at every run).

cooper_s10 (A005260) and t103 (A276536) were checked at the same time and are
clean — both match their OEIS b-files exactly.

## D-1.3: Kernel-swap falsification battery — PREREGISTERED VERDICT

**Script:** `scripts/k3t2_kernel_swap_battery.py`
**Result file:** `data/k3t2/d1_3_kernel_swap.json`

Ran all four kernels (cooper_s7, cooper_s10, t103, random_control) through the
identical bounded-observable pipeline on a 64³ lognormal mock density field.

| Pair | Pearson r |
|---|---|
| cooper_s7 – cooper_s10 | 0.9999 |
| cooper_s7 – t103 | 1.0000 |
| **cooper_s7 – random_control** | **1.0000** |
| cooper_s10 – t103 | 0.9998 |
| cooper_s10 – random_control | 0.9999 |
| t103 – random_control | 1.0000 |

**Preregistered rule:** if r(s7, random) > 0.95 → F1 FAILS.

**r(s7, random) = 1.0000 → F1 FAILS.**

### Verdict: `F1_FAILS_KERNEL_BLIND`

The Δ-map observable (|FFT(bounded_period) − FFT(raw_density)|) cannot
distinguish ANY of the four kernels, including a growth-matched random
control carrying no Picard-Fuchs/modular structure whatsoever. This confirms
the audit suspicion (A2, from the prior GATE R-0 review): the statistic is
dominated by the shape of the monotone density→observable map itself, not by
which K3 kernel is used. The "Δ_s7 = 663.4" figure — even after the Rule-1
data fix — carries **no evidential weight** for K3 geometry specifically.

## Consequences

1. **GATE D-3 (empirical validation) is FROZEN.** Per the preregistered plan,
   no further empirical claims (redshift tomography, TDA alignment, lensing
   overlay) should be run against real data using this observable until it is
   redesigned to be kernel-sensitive.
2. **GATE D-2.4 (s7/s10 discriminant) proceeds anyway** — it is a pure exact
   computation independent of the broken empirical observable, and produces a
   mathematically genuine discriminant regardless of F1's outcome. See
   `data/k3t2/d2_4_singular_loci.json` and `GATE_D2_SONNET_HANDOFF.md` update.
3. **Observable redesign is now a precondition for GATE D-3**, not an
   optional refinement. Candidate directions (not yet executed): use the
   *phase* structure of Π₀(z) rather than |Π₀(z)|; use higher-order period
   derivatives; or compare against the specific singular-point structure
   found in D-2.4 (e.g., proximity of local z to 1/27 vs 1/16) rather than a
   generic FFT contrast.

## Sign-off

This is a negative result, delivered honestly per the project's standing
Rule 4. It is a direct product of preregistration working as intended: the
decision rule was committed before the run, and the run falsified the
observable rather than confirming a "discovery."
