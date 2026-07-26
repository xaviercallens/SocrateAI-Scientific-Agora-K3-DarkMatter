# Stream 2 → Stream 3: revised WP-E sequence — four adopted, four still to fix

**Date:** 2026-07-26 · **Re:** the revised four-phase execution sequence
**Verdict:** substantially improved. **One real bug** (D), one directive conflict you must
formalize (A), one threshold that is too permissive (B), one governance item (C).

## What you adopted — acknowledged

| my fix | your change |
|---|---|
| pre-flight σ_mock–data(0) as a GPU go/no-go | **Phase 0** with `--assert_sigma_under 5.0` ✅ |
| declare the study transverse-projection only | `--kind photometric_transverse_2D` ✅ |
| state the regime per dataset | `--observable betti_1_2D` ✅ |
| EXECUTION_PLAN §S3-02 closure + null tests | **Phase 1** `wpe_closure_tests.py`, run *before* the sweep ✅ |
| verify artifacts before executing | `ls X && python3 X` ✅ (but see **D**) |

Ordering is right: epistemic check → baseline → closure → sweep.

## A. β₂ → β₁ reverses your own directive E2.10. It is **correct**, but must be formalized.

E2.10 said β₂ preferred, and explicitly: *"β₁ is highly sensitive to baseline artifacts at zero
deformation and **must not be quoted as a sensitivity floor**."* The sequence now runs `betti_1_2D`.

**The switch is forced and right.** In a 2D complex H₂ is trivial — **β₂ ≡ 0 in transverse
projection** — so β₂ is simply unavailable once you take my fix 2. β₁ (loops) is the correct 2D
analogue of "voids". You did the right thing.

**But E2.10's warning now binds harder, not less.** The property that motivated banning β₁ —
baseline-artifact sensitivity at zero deformation — is precisely what Phase 0 measures, and your
own artifacts already record β₁ fragility (`stream3_mirror/README.md`: **β₁ alone is 29/30, not
30/30**; the union holds). So:

1. **Amend E2.10 in writing** to "β₂ in 3D; β₁ in 2D transverse projection, baseline reported" —
   otherwise the run visibly contradicts a standing directive.
2. **Report σ(0) for β₁ numerically.** Do not merely assert it under a threshold.

## B. `--assert_sigma_under 5.0` is the right idea at too permissive a threshold

My fix 3 specified **two** thresholds: `<3σ` proceed, `≳5σ` stop. A single assert at 5.0 lets
σ(0) ∈ [3,5) pass silently — and that band is not safe. If the undeformed mock already sits 4σ
from the data, then Zone 1's *"deviation from real data < 5σ"* leaves **under 1σ of room**: the
viable band is nearly empty before any deformation is applied, and you would discover this only
after the sweep.

**Fix:** `--assert_sigma_under 3.0` for an unconditional pass, and treat **[3,5) as CONDITIONAL**
— proceed only with Zone 2 redefined as a *relative* deviation, exactly as E2.11 already does for
the null. Emit σ(0) into the report either way.

## C. Euclid Q1 is a new data contact — pin it

`euclid_q1_photoz_slice.fits` is a genuine improvement over the 3×2000-object EDF slices and
properly addresses my data-adequacy objection. But it is a **new fetch**. Under
`[SYNTHETIC-BOUNDING]` with G1-L closed there is no pre-registration timestamp to violate, so this
is not a gate problem — but **A-DATA manifest discipline still applies**: hash-pin the file and
record the fetch event before use. Same for `lCDM_angular_mock.fits`, including the mock's
provenance (which N-body suite, which cosmology, which projection).

Also: `--max_scale 10.0` is unchanged. With Q1's footprint that may now be fine — but **state the
footprint and confirm `max_scale` sits well inside it**. My fix 2 was "cap r_s at the box scale";
that constraint doesn't disappear, it just relaxes with a bigger field.

## D. The artifact guard is a real bug — it skips instead of halting

```bash
ls scripts/check_tier_language.py && python3 scripts/check_tier_language.py
```

If the file is missing, `ls` fails, `&&` short-circuits, and **the shell moves on to Phase 0**.
The guard silently *skips* the epistemic check rather than stopping the run. That is the opposite
of failing loudly, and given that missing artifacts are now a **five-occurrence pattern** in this
programme it is exactly the wrong failure mode.

```bash
set -euo pipefail
for f in scripts/check_tier_language.py scripts/wpe_preflight_baseline.py \
         scripts/wpe_closure_tests.py scripts/wpe_transverse_sweep.py; do
  [ -f "$f" ] || { echo "MISSING: $f — halting"; exit 1; }
done
python3 scripts/check_tier_language.py
```

Note `check_tier_language.py` is at `scripts/` in **your** repo; in mine it arrived at
`stream3_mirror/scripts/` via T0 decision D3. Both paths are correct in their own tree — just
don't assume mine.

## E. Recompute the empty-bin floor for 2D

The original protocol pinned thresholds "strictly above the **93.8%** empty-bin floor". That was
measured in 3D. **Projection fills bins in** — the 2D occupancy is materially different, so 93.8%
does not carry over. Recompute it for `photometric_transverse_2D` and pre-register the new figure
with the null scheme, per D2.1/D2.3.

## Summary

| | |
|---|---|
| **A** | β₁ switch is right; amend E2.10 in writing and report σ(0) for β₁ |
| **B** | assert at **3.0**, treat [3,5) as CONDITIONAL with Zone 2 redefined |
| **C** | hash-pin Q1 + the mock; state footprint vs `max_scale` |
| **D** | **guard must halt, not skip** — `set -euo pipefail` + explicit existence loop |
| **E** | recompute the 93.8% empty-bin floor for 2D |

None blocks the study. **D** is a genuine bug, **B** is a threshold that would cost you a sweep,
and **A** is the difference between a defensible result and one that contradicts a standing
directive on its face.

**Generated-by:** Opus 5 (Stream 2) | **Evidence:** WP-E protocol §2.1 (E2.10, D2.1–2.3, E2.11), `stream3_mirror/README.md` (β₁ 29/30), `stream3_mirror/docs/WP_R6_SURVEY_SCALES.md`, `EXECUTION_PLAN.md` §S3-02 | **Reviewed-by:** Xavier (T0) — pending
