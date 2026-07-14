# LR-5 — Lee–Tsai (5D orbifold) ↔ Agora K3×T² Bridge Memo

**Date:** 2026-07-14 · **Status:** complete · **Companion:** `docs/reference/lee_tsai_2026.md`, `docs/reference/dmk3_home/AGORA_K3_T2_BRIDGE_PLAN.md`

## 1. Structural alignment

| Structure | Lee–Tsai 5D | Agora 6D (this programme) |
|---|---|---|
| Compact geometry | S¹/(Z₂×Z₂′) orbifold, radius R | K3-fibered CY (candidate fiber now S(2,2)=A005259 per Phase A) × T² |
| Mass generation | KK quantization: level spacing set by 1/R | D3-instanton action on fiber cycles; KK tower on effective radius |
| Resonance condition | KK-level crossing enhances annihilation & self-interaction | density-coupled effective-radius "pinching": m_eff(Δ) |
| Density dependence | warped/brane setup | conformal (chameleon-type) coupling to baryonic T^μ_μ |
| Early-active / late-inert | resonance active in dense early universe, frozen today | Cosmic See-Saw; local bound S₁,₂ ≤ 1.177 (32 SDSS BOSS DR17 sectors, companion pipeline) *consistent with* freeze-out |
| Observable channel | direct detection + accelerator | PTA lines, weak-lensing cross-match of high-Δ nodes, TDA survey statistics |

The genuinely shared physics is one sentence: **compact-dimension geometry sets a resonance structure, and local environment can move the system on and off resonance.** Both programmes instantiate that sentence; everything else differs.

## 2. Where the analogy breaks (equal weight, per plan requirement)

1. **Particle content.** Lee–Tsai: fermionic DM + massive dark photon with an axial-vector coupling. Agora: ultralight pseudo-scalar (axion) from RR-form reduction. Different spin, different statistics, different Lagrangian — there is no field-level map between the two models.
2. **Mass scale.** Their phenomenology lives where direct-detection and accelerator searches operate; ours at ~10⁻²¹ eV where the de Broglie wavelength is kiloparsecs. No experiment tests both.
3. **What "resonance" does.** Theirs is an *s-channel/KK-level* resonance enhancing annihilation and self-interaction cross-sections (relic abundance and SIDM phenomenology). Ours is a *mass-shift* response m_eff(Δ) with no annihilation channel at all — the axion relic is misalignment-produced. QT-4's "SIDM overlap" test is therefore a **structural analogy check, not a shared prediction**: axion self-coupling at 10⁻²¹ eV cannot produce their σ/m band.
4. **Derivation status.** Their R and brane masses are model inputs with a worked 5D field theory. Our Δ-coupling k (or κ) is a phenomenological parameter with **no top-down derivation** (v1 open problem, unchanged), and the two Agora repositories currently disagree on the functional form — exp(kΔ) here vs. (1+κΔ_obs)^{1/4} in the companion bridge plan (**open item OI-1**; must be reconciled before any joint fit).
5. **Evidential grade.** Lee–Tsai is a peer-reviewed PRD Letter with a self-contained model. The Agora freeze-out consistency rests on companion-pipeline outputs whose converged runs are not yet archived reproducibly (provenance ledger). The bridge is conceptual until OI-1 is resolved and DM-3 (quorum re-run) completes.
6. **The K3 side just changed under us.** Phase A reclassified v1's S₁,₂ as elliptic-type; the K3 anchor of the 6D story is now S(2,2)=A005259 (Beukers–Peters). Any bridge statement written against the v1 fiber is void until the Phase B stiffness pipeline is rebuilt on the new pool.

## 3. What the bridge licenses (and what it does not)

Licensed: using Lee–Tsai as the *microscopic motivation* for density-coupled resonance language; citing their freeze-out requirement as the qualitative hypothesis our 1.177 bound is *consistent with*; division of labor (no orbifold simulation needed browser-side — 5D physics enters only through m_eff(Δ)).
Not licensed: claiming shared predictions, shared parameter space, or that SDSS/TDA results "confirm" the 5D model; claiming Euclid results (none exist — SDSS BOSS DR17 only, per the companion Phase III report).
