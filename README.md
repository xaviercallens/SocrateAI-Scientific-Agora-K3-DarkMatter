# Dual-Scale Topological Universe Model

> **F6 disclosure (2026-07-24): C1/C2 lattice numbers retracted.** `check_C1.py` extracted
> singular loci as roots of the recurrence coefficient B(k) in the discrete **index k** and
> mislabeled them as z-space singular points, with **hardcoded** exponents → "type II". The
> resulting fibre configs and the Picard/transcendental numbers **ρ=4, T=18** (cooper_s7/s10
> partners, in prior `C1C2_LATTICE_REPORT` and v0.3.0) are **NOT valid** and are retracted
> (`_F6_RETRACTED` on the affected certs). Corrected z-space loci via
> `checkers/check_C1_singular_loci.py`: cooper_s7_partner {−1, 1/27}, cooper_s10_partner
> {−1/4, 1/16}. **Unaffected:** the kernel-verified **L₃=Sym²(L₂) proof** (`CooperSym2Proof.lean`,
> v0.3.0) — pure operator algebra, independent of the C1 step. Full Kodaira re-typing is an open
> ticket. See `briefs/DEEPTHINK_ADJUDICATION_DOMB_A002893.md` §3.

## Project Tracking
- [GitHub Project: Dual-Scale Topological Universe Model](https://github.com/xaviercallens/SocrateAI-Scientific-Agora-K3-DarkMatter/projects)
- [Milestones](https://github.com/xaviercallens/SocrateAI-Scientific-Agora-K3-DarkMatter/milestones)

## Dashboards
- [DUAL SCALE V3 Cosmic Topology Dashboard](dashboards/dual_scale_v3_cosmic_topology_dashboard.pdf)
- [V5 Dual-Scale Pipeline Dashboard](dashboards/v5_dual_scale_pipeline_dashboard.pdf)

## Repositories
- [SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal](https://github.com/xaviercallens/SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal)
- [SocrateAI-Scientific-Agora-K3-DarkMatter](https://github.com/xaviercallens/SocrateAI-Scientific-Agora-K3-DarkMatter)
- [DarkMatterK3-Home.github.io](https://github.com/xaviercallens/DarkMatterK3-Home.github.io)

## Key Files
- [weak_lensing_overlay.py](scripts/weak_lensing_overlay.py)
- [NANOGrav_prediction.py](scripts/NANOGrav_prediction.py)

> Note (2026-07-26): `v5_dual_scale_pipeline.py` was deleted — it was an empty stub citing the
> retracted legacy program (Δ-spikes / weak lensing / NANOGrav observables). Current status
> lives in `TODO.md`; the empirical position is `PREDICTION.md` v1.1 §6 (F5b).

> Note (2026-08-01, low-tier queue A-S2-4): `DUAL_SCALE_HYPOTHESIS.md` and
> `K3_CRITERIA_INTERFACE.md` (removed from the list above, links were dead) moved to
> [archive/pre-ledger/](archive/pre-ledger/README.md) along with 23 other pre-ledger root
> docs, consistent with the retraction this file already documented above — see the
> archive's own README for the full classification and rationale. `K3_CRITERIA_INTERFACE.md`
> is very likely the never-finalized draft predecessor of the `K3_CRITERIA.md` that
> `VISION.md`/`EXECUTION_PLAN.md` cite as frozen but which does not currently exist in this
> repo — flagged there, not resolved here.

## Workflow Files
- [Dual-Scale Model Validation](.github/workflows/dual_scale_validation.yml)
- [Update Dashboards](.github/workflows/update_dashboards.yml)