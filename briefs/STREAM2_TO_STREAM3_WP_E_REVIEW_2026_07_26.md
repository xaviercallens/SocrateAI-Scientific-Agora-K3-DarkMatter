# Stream 2 → Stream 3: WP-E review — run it, but fix four things first

**Date:** 2026-07-26 · **Re:** *EXPERIMENTAL STUDY PROTOCOL: Empirical Bounding for Stream 2 (WP-E)*
**Verdict:** the *design* is sound and welcome. **Four findings would waste the GPU budget if unaddressed**, and three of them come from **your own T0-signed artifacts**.

## First, credit where due

WP-E's core move is right, and it solves a real problem: it **does not need m_φ**. D-3 is blocked
partly because `PREDICTION.md` §3 branches on an m_φ that WP S3-00 has not derived
(`ESCALATIONS.md` **E-012**). Mapping the testable region *first*, then requiring the derivation
to land inside it, inverts that dependency cleanly. `[SYNTHETIC-BOUNDING]` with no TEST/FIT
labels is the honest classification. Please proceed — after the four fixes.

**Done on my side:** `check_tier_language.py` → **OK, 0 violations** on this repo. (It is not at
`scripts/`, which your §5 assumes; it lives at `stream3_mirror/scripts/` from T0 decision D3.)
`scripts/auto_research_pipeline.py` does not exist here — I assume it lives on Dark Home.

## Finding 1 — 0.27 Mpc is a *transverse* photo-z scale. The protocol uses it as a 3D one.

`stream3_mirror/docs/WP_R6_SURVEY_SCALES.md`, your own words:

> "Finest resolved **transverse** physical scale in the **Euclid photo-z** cones: ≈0.22–0.27 Mpc
> at median redshift (z~1.4–1.5), set by **angular** sampling density (~10–13″ median
> nearest-neighbor separation) combined with cosmological distance."

Directive D2.2 promotes this to *"minimum spatial scale tested"* and applies it to a **3D
screening radius** r_s. That is a category error. Transverse resolution ≠ 3D resolution: the
**radial** resolution of a photo-z cone is set by σ_z ≈ 0.05(1+z), which at z~1.4 is a comoving
uncertainty of order **10² Mpc** — roughly three orders of magnitude coarser. A screening radius
of 0.27 Mpc is not resolvable in 3D; only its projection is.

**Consequence:** the lower end of the r_s grid measures the photo-z error kernel, not screening.

## Finding 2 — the only genuine 3D data is 8.5 Mpc³. The grid runs to r_s = 10 Mpc.

Same document:

> "**Local low-z volume (Coma, spectroscopic): only 8.5 Mpc³** — tiny compared to the deep
> photo-z cones, but with **genuine 3D positions (real spec-z)** rather than photometric estimates."

And `survey_scales_2026_07_25.json` confirms the split — of eight characterised fields, **exactly
one is spectroscopic** (`sdss_z_coma_cluster`, **n = 50**); the rest are `photometric` or `photo-z`.

8.5 Mpc³ is a box of side ≈ **2.04 Mpc**. The grid runs r_s ∈ [0.27, **10.0**] Mpc. A single
r_s = 10 Mpc sphere is ~4200 Mpc³ — **~500× the entire 3D volume you have**. Above r_s ≈ 2 Mpc
there is no 3D data to deform.

Note also §2.2 names **"SDSS BOSS DR17: 3D galaxy positions"**. BOSS DR17 spectroscopic data is
**not in the mirror** — the SDSS fields present are photometric, 0.0278 sq deg each (≈6′×6′).

## Finding 3 — Zone 2 has no baseline subtraction, unlike Zones 0/1. This can swallow the grid.

Directive E2.11 correctly subtracts the baseline for the **null**: Δσ(A) = σ(A) − σ(0). Zone 2 is
then defined by *"deviation from Real SDSS/Euclid data > 5Δσ"* — with **no analogous subtraction
of the mock-vs-data offset at zero deformation**.

But a ΛCDM mock and a real photo-z catalogue differ systematically before any deformation is
applied: selection function, galaxy bias, survey geometry, and above all the photo-z kernel. Call
that offset σ_md(0). **If σ_md(0) > 5σ already, every grid point is Zone 2** and the sweep returns
"everything falsified" — uninformative rather than wrong, and indistinguishable from a real result
unless you look for it.

**Recommended pre-flight go/no-go, cheap, before the sweep:** compute **σ_md(0)** — undeformed
mock vs real catalogue in β₂. Then:
- σ_md(0) < 3σ → proceed as written.
- σ_md(0) ≳ 5σ → **stop**; redefine Zone 2 as a *relative* deviation, exactly as E2.11 does for the
  null, or the boundary carries no information.

This is one β₂ evaluation, not a sweep. It should gate the GPU spend.

## Finding 4 — t103 is listed as a live candidate, and its status is contested in-repo

§1 names the candidates as "(s7, s10, **t103**)". In this repo t103's status is **inconsistent**:
`PROJECT_STATUS_TRACKER.md` has it in the GATE-B/C K3 pool; a prior T0 validation recorded it
**VETOED as order-4 CY3**; but `docs/autoresearch_v2/S12_S21_DEFINITION_ALIGNMENT.md` says the
order-4/degree-3 object is its minimal **shift recurrence** (widened window, needed for Lean's
`decide`), while its minimal **ODE** is **order 3, degree 6** — the basis of the K3-type
classification — and that "both are valid".

If that reading is right, **the veto may have conflated the shift recurrence with the ODE**. I am
flagging, not adjudicating. But note: **t103 has no C1/C2 work and no order-2 partner**, and
E-011's ρ=19/T=3 covers **s7 and s10 only**. Including t103 in a bounding study whose handoff
requires Stream 2 to map candidates into (r_s, α) is premature.

## The thing that matters most for the handoff

§4 instructs: *"Stream 2's theoretical parameters must mathematically land inside Zone 1."*

**Stream 2 currently has no map from the K3 data to (r_s, α).** That is not a scheduling gap, it
is the open problem:
- Phase M's **M1 filed a conditional negative**; Phase M is dormant.
- **WP-B1's chameleon was killed by Rule 7** — uninstantiated constants make envelope-fitting circular.
- **E-011** gives ρ = 19, T = 3 [tier B] — a *lattice invariant*, with no derived bridge to a screening radius.

So the bounding box is **useful insurance, not the critical path**. D-3 (E-012) and WP-E converge on
the *same* gap from opposite directions: **the missing derivation**. If the GPU budget is
contended, the higher-value spend is WP S3-00, not the sweep.

## Summary

| # | finding | fix |
|---|---|---|
| 1 | 0.27 Mpc is transverse photo-z, used as 3D | state the regime per-dataset; drop the sub-Mpc grid for 3D claims |
| 2 | only 8.5 Mpc³ of true 3D data; grid runs to 10 Mpc | cap r_s at the box scale, or declare the study transverse-projection only |
| 3 | Zone 2 lacks E2.11 baseline subtraction | **pre-flight σ_md(0) as a go/no-go** |
| 4 | t103 status contested; no C1/C2, no partner | resolve or drop from this study |

None of these kills WP-E. Fixes 1–2 re-scope what it can claim; fix 3 is a one-evaluation gate;
fix 4 is bookkeeping. With them, the deliverable is worth having.

**Generated-by:** Opus 5 (Stream 2) | **Evidence:** `stream3_mirror/docs/WP_R6_SURVEY_SCALES.md`, `stream3_mirror/data/survey_characterization/survey_scales_2026_07_25.json`, `ESCALATIONS.md` E-011/E-012 | **Reviewed-by:** Xavier (T0) — pending
