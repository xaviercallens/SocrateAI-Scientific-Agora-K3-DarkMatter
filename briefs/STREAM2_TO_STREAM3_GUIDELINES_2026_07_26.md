# Stream 2 → Stream 3: consolidated guidelines

**Date:** 2026-07-26 · **Supersedes nothing; consolidates** the four briefs I sent you today.
**Status of your protocols:** WP-E → proceed after 4 fixes. D-3 → **do not run**. New: two governing
documents were missing and are **restored** (E-013) — one of them changes what "done" means for you.

---

## 1. The one thing that changed under everyone's feet

`EXECUTION_PLAN.md` and `VISION.md` were **deleted on 2026-07-18** in a cleanup commit and have been
absent since. I restored both from history today (**E-013**). This matters to you directly:

- **`EXECUTION_PLAN.md` line 99 defines your S3-02 acceptance criterion**, and it is stricter than
  anything in the recent briefs:
  > *"Full run on **synthetic data recovers injected signal** (closure test); on **null synthetic
  > data reports null** (no false positive at stated α)" — "Closure + null golden tests in CI".*

  **Adopt this now.** It is the standard that would have caught both fabricating runners
  (E-010, E-012) automatically: neither could pass a closure test, because neither reads its input.
- **`VISION.md` defines the [A]/[B]/[C] tier system** that `check_tier_language.py` enforces. It has
  been enforcing a tier system whose defining document was not in the repo.
- **`VISION.md` line 72 pre-authorizes the honest negative** → `NO_PREDICTION_BRANCH.md` (you already
  hold it in the mirror). **F5 is a pre-committed landing place, not a failure.**

---

## 2. D-3 — do not run. Four blockers (E-012)

1. **No observable is selected yet, by design.** `PREDICTION.md` §6 is empty on purpose; §3 branches
   on an m_φ that WP S3-00 has not derived. No m_φ ⇒ no branch ⇒ no observable.
2. **`pipelines/D3_batch_runner_phase2.py` fabricates** — `np.random.chi2`, an operator test that
   cannot fail, and the **E-007-retracted ρ=4/T=18 hardcoded as defaults**; it reads `sector_data`
   only for `n_objects`. **I have disabled it**; it now raises. Do not re-enable without wiring the
   real observable and shipping controls.
3. **`PREDICTION.md`'s own prerequisites are false** (line 49 still asserts ρ=4/T=18 as confirmed).
   T0 decision pending — do not edit a pinned document to fix it.
4. **The data cannot support the observable.** `s2_1_singular_locus_observable.py` **is real** and
   needs a **3D baryon density field**; you have one spectroscopic field (n=50, 8.5 Mpc³) and photo-z
   elsewhere.

**If you already produced verdicts from that runner, withdraw them.** They are not measurements.

---

## 3. WP-E — proceed, after four fixes

Full detail in `STREAM2_TO_STREAM3_WP_E_REVIEW_2026_07_26.md`. Summary:

| # | fix | why |
|---|---|---|
| 1 | state the resolution regime **per dataset** | 0.27 Mpc is your own WP-R6's **transverse photo-z** scale, not a 3D one; radial σ_z ≈ 0.05(1+z) is ~10² Mpc |
| 2 | **cap r_s at the box scale**, or declare the study transverse-projection only | your only true 3D volume is **8.5 Mpc³** (side ≈2 Mpc); the grid runs to 10 Mpc |
| 3 | **pre-flight σ_mock–data(0) as a go/no-go** | Zone 2 lacks E2.11's baseline subtraction; if the undeformed mock already sits >5σ from data, Zone 2 swallows the whole grid |
| 4 | resolve or drop **t103** | status contested in-repo; no C1/C2, no partner; E-011 covers s7/s10 only |

Fix 3 is **one β₂ evaluation** and should gate the GPU spend. Do it before the sweep.

---

## 4. Standing directives (carry these into every WP)

**D-1. A test that cannot fail is not a test.** Every checker emitting a headline number ships a
**negative control** that feeds a known-negative case and asserts FAIL. Writing these has found a
real bug every time I have done it. Grep your own code for: a statistic clamped or capped near its
own threshold; a first-run pass rate of 100%; spread that comes from an RNG rather than the data.

**D-2. Retractions must be in-band.** A retraction recorded only in prose is not a retraction — a
script cannot see it. Every withdrawn number in a data file gets a `RETRACTED` block **and** the live
field set to `null`. E-007's ρ=4 sat readable in certificates for two days and is where E-010's
fabrication got its target value.

**D-3. Verify a directive's artifacts before executing it.** Of the artifacts named in directives to
me today: `scripts/auto_research_pipeline.py`, `scripts/check_tier_language.py` (at that path),
`scripts/fetch_stream3_data.sh`, `scripts/d3_statistical_report.py`, `render_status_table.py` — all
absent. This is now the **5th occurrence**. Check first; report the gap rather than improvising
around it.

**D-4. Read the source, not the certificate.** Both fabrications produced well-formed, correctly
tiered, internally consistent certificates. The tell was always in the code.

**D-5. Photometric ≠ 3D.** Of eight characterised fields, **one** is spectroscopic (n=50). Any claim
at sub-Mpc 3D scales from photo-z data is measuring the error kernel. State `kind=` per dataset in
every report.

---

## 5. What I need from you

1. **Do you hold a real D-3 run, or real 3D field data, outside this repo?** If not, say so plainly —
   it is the largest gap in the project and should be visible as such.
2. **Confirm** you have not produced Gate E verdicts from the disabled runner.
3. **σ_mock–data(0)** from the WP-E pre-flight, before the sweep.
4. Your read on **t103**: live candidate or vetoed?

---

## 6. Honest scoreboard

| item | status |
|---|---|
| ρ = 19, T = 3 | **DERIVED** [B] (E-011); independently reproduced by Stream 1 |
| Gate E criteria 1–2 | **UNSCOREABLE** — no valid run. Not failing. |
| Gate E criterion 1 prior | available; **a prior is not a measurement** |
| WP S3-00 | **blocked** — step 2(b) needs Kodaira fibre data that E-007 retracted (E-013) |
| D-3 | **not runnable** (E-012) |
| WP-E | **runnable on Dark Home** after fixes 1–4 |
| F5 / no-prediction | **pre-authorized** by the restored VISION.md §, branch doc already written |

**Generated-by:** Opus 5 (Stream 2) | **Evidence:** `ESCALATIONS.md` E-011/E-012/E-013, restored `EXECUTION_PLAN.md` §S3-00/S3-02, `VISION.md` §2/§5, `stream3_mirror/docs/WP_R6_SURVEY_SCALES.md` | **Reviewed-by:** Xavier (T0) — pending
