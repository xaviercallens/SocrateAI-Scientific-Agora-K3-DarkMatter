# Stream 2 → Stream 3: D-3 was NOT run, and here is why. Do not run it either.

**Date:** 2026-07-26 · **Ticket:** `ESCALATIONS.md` **E-012** · **Status:** 🔴 blocker, T0 decision needed

I was asked to conduct the D-3 empirical run. **I did not.** Running the pipeline as it stands
would have produced a Gate E result out of a random number generator. Four independent blockers,
any one of which is sufficient:

## 1. There is no selected observable yet — by design

`PREDICTION.md` v1.0-PINNED §6 is **empty on purpose**; §1 states `m_φ, α_D, Λ_D` are
**TO-BE-DERIVED** by WP S3-00 and that writing them early *"would be numbers-from-memory —
forbidden."* But §3 branches on m_φ: **P1** (PTA) if m_φ ∈ [10⁻²³,10⁻²²] eV, else **P2** (lensing).
**S3-00 has not run ⇒ no m_φ ⇒ no branch ⇒ no observable.** Anything run now and called "the
pre-registered test" destroys the pre-registration, which is the whole evidential point of the pin.

## 2. The official runner fabricates — and it is the one the pin names

`pipelines/D3_batch_runner_phase2.py`, verbatim:

```python
error = np.random.normal(0, 1e-8, n_objects)   # tested against precision=1e-6 -> CANNOT FAIL
chi2  = np.random.chi2(df=1, size=1)[0]        # "synthetic, mean=1, pass if <3"
def compute_lattice_estimate(sector_data, c2_prior_rho=4, c2_prior_t=18):
    rho_est = c2_prior_rho + np.random.normal(0, 0.3)
```

It reads `sector_data` only for `n_objects` — **your redshift columns are never touched**. Its
"pass rate" is a property of the RNG (~91.7%), not of any data, and its ρ defaults are the
**E-007-retracted** 4/18. **I have disabled it**: it now raises with a pointer to E-012. It was
disabled rather than deleted because the pinned PREDICTION.md names it, so it must fail loudly.

## 3. The pin's own prerequisites are now false

PREDICTION.md lists as met: *"✅ C1 Kodaira classification complete (ρ=4, T=18 confirmed)"* and
*"✅ C2 Picard/lattice computation complete"*. **Both retracted (E-007)**; ρ/T are now 19/3 (E-011).
A pinned document cannot simply be edited — that is what pinning means — so this needs a **T0
decision**: re-pin at v1.1 recording the correction, or annotate under the open countermand window
in `ASSUMPTIONS.md` §2.

## 4. The data cannot support the observable

`empirical_crucible/s2_1_singular_locus_observable.py` **is real** — and it consumes a **3D baryon
density field**. What the mirror actually holds:

| | |
|---|---|
| `sdss_z/` | Coma cluster, **50 galaxies**, spectroscopic |
| `euclid_z/` | 3 EDF fields × **2000 objects**, **photometric** z |
| `wp_r5_3d_field/` | **JSON results only — no field** |

50 galaxies cannot constrain the observable's grid; Euclid photo-z (σ_z ≈ 0.05(1+z)) smears radial
position by ~10² Mpc, far beyond the scales a singular-locus proximity metric probes. And 4 sectors
against the protocol's 100–150.

## What I need from you

1. **Do you have a real D-3 run, or real 3D field data, that is not in this repo?** If yes, that
   changes blocker 4 entirely and I want it. If no, say so plainly — it is the single biggest gap
   in the project and it should be visible as such.
2. **Confirm you have not run `D3_batch_runner_phase2.py`** and produced verdicts from it. If you
   have, those verdicts are not measurements and must be withdrawn.

## Gate E position, unchanged and honest

Criteria 1–2 are **UNSCOREABLE for want of a valid run** — *not failing*. Criterion 1's **prior** is
now available (E-011: ρ=19, T=3, tier B) but **a prior is not a measurement**. The other criteria
(operator numerics, mirror-map, physics-washing) stand on their own Stream 2 evidence.

**Generated-by:** Opus 5 (Stream 2) | **Verified-by:** `ESCALATIONS.md` E-012 | **Reviewed-by:** Xavier (T0) — pending
