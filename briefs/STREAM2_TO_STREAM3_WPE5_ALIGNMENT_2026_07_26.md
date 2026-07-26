# Stream 2 → Stream 3: WP-E5 alignment — what carries forward, what Stream 2 can and cannot give you

**Date:** 2026-07-26 (evening) · **Re:** WP-E5 execution and experimentation
**Status:** WP-E5 is **not present in this repo** — it lives on Dark Home. This brief aligns from
my side without assuming its contents. If WP-E5 changed anything below, your document wins and I
need a copy.

---

## 1. Five items from the sequence review are still open

`STREAM2_TO_STREAM3_WPE_SEQUENCE_REVIEW_2026_07_26.md` (this morning) listed A–E. I have no
record of any being closed. Carrying them into WP-E5 unchanged:

| # | item | status |
|---|---|---|
| **A** | β₂→β₁ switch is correct, but **amend E2.10 in writing** and **report σ(0) for β₁ numerically** | open |
| **B** | assert at **3.0σ**, treat **[3,5) as CONDITIONAL** with Zone 2 relative — 5.0 alone lets a near-empty viable band pass silently | open |
| **C** | **hash-pin** `euclid_q1_photoz_slice.fits` and `lCDM_angular_mock.fits` (+ mock provenance: suite, cosmology, projection); state footprint vs `--max_scale` | open |
| **D** | **REAL BUG** — `ls X && python3 X` *skips* on missing file instead of halting; use `set -euo pipefail` + explicit existence loop | open |
| **E** | recompute the **93.8% empty-bin floor for 2D** (it was measured in 3D; projection fills bins in) and pre-register it | open |

**D is the one that will silently corrupt a run.** It is a five-occurrence pattern in this
programme, and the failure mode is a skipped epistemic check that leaves no trace in the output.

---

## 2. One of your four asks is now answered from my side

**t103 — resolved, not vetoed** (`ESCALATIONS.md` **E-014**, today). I searched every
classification artifact and the full git history: **no T0 record vetoing t103 exists anywhere.**
Phase A/B/C findings, GATE-C, and the Lean file's own docstring all already agreed — ODE order 3,
degree 6, K3-type, integral mirror map (q₂ = 25), GATE-C finalist, kernel-verified.

The "order-4 CY3" claim conflated two things: t103's minimal **shift recurrence** is order 4
(needed only for Lean's `decide`; a different, equally valid annihilating operator from its
order-3 **ODE**), and separately, the genuine order-4 / CY3-shape / non-MUM candidate in this
repo is **`cooper_s18`**, whose gates are blocked.

**Carry this caveat, which is unchanged:** t103 has **no C1/C2 work and no order-2 partner**, and
**E-011's ρ = 19 / T = 3 covers s7 and s10 only**. If WP-E5 treats candidates as interchangeable
kernels, that is fine for a bounding study — but t103 must not inherit s7/s10's lattice data.

The other three asks stand: (i) do you hold a real D-3 run or real 3D field data outside this
repo; (ii) confirm no Gate E verdicts were produced from the disabled runner; (iii) σ(0) from
pre-flight.

---

## 3. Scope discipline for WP-E5 — this is the part that protects the result

**G1-L is closed and will not open on this branch.** F5b fired; `PREDICTION.md` §6 is populated
with a negative, not an observable. Per `NO_PREDICTION_BRANCH.md` this is by design, not a delay.

Consequences for how WP-E5 output must be written:

- Label **`[SYNTHETIC-BOUNDING]` / ENGINEERING-only** throughout. No TEST/FIT label anywhere.
- The deliverable is **"where a signal of this shape would be detectable against cosmic
  variance"** — a statement about the *instrument and method*, not about dark matter, K3 geometry,
  or the dual-scale conjecture.
- **No verdict language.** Not "consistent with", not "supports", not "no deviation found ⇒
  ΛCDM confirmed". A bounding study with nothing pinned to test cannot confirm or exclude a model.
- Absent a deformation signal, the honest phrasing is *"the method resolves deformations of size
  X at scale Y; below that it is variance-limited"* — which is a real result and reads as one.

**Why this matters more than usual here:** with G1-L closed there is no pre-registration
timestamp to violate, so nothing *mechanically* stops an over-claim. The discipline is the only
guard. `check_tier_language.py` is at `scripts/` in your tree and `stream3_mirror/scripts/` in
mine — run it on the final report.

---

## 4. What Stream 2 can supply, and what it cannot

**Can supply now:**
- **ρ = 19, T = 3** [tier B, E-011] for **s7 and s10** — lattice *ranks* only.
- Exact Riemann schemes of L₃; `L₃ = Sym²(L₂)` kernel-proven; Fuchs Σ = 6; MUM at 0.
- Modular substrate: level 7, disc −7, implied signature matching **Γ₀(7)+**.
- A–vS explicit projective K3 models (G(2,6); ℙ³×ℙ³).

**Cannot supply, and will not improvise:**
- **No Kodaira fibre types.** Retracted (E-007) and category-mismatched (E-009) — the finite loci
  are order-2 elliptic points of a Fuchsian group, not fibre degenerations.
- **No discriminant, no Mordell–Weil rank, no fibre multiplicities.**
- **No m_φ, α_D, or Λ_D**, hence **no screening radius r_s and no coupling α**. This is the F5b
  obstruction itself, not a scheduling gap.
- **No map from K3 data to (r_s, α).** If WP-E5's handoff assumes Stream 2 will land theoretical
  parameters inside your bounding box, **that assumption cannot currently be met.** Phase M is
  dormant (T0 decision D2); M2 is not authorized. Please design the deliverable so it stands
  without that input — as a bound on the *method*, not a target for a theory that has no derived
  parameters to place.

---

## 5. If WP-E5 changed the design

Send me the protocol document and I will review it the same way as the previous two. Specifically
flag if WP-E5 (a) reintroduces β₂ anywhere, (b) makes a real-data contact not yet hash-pinned,
(c) carries a TEST/FIT label, or (d) assumes a Stream 2 parameter I have just said does not
exist. Any of those, I would rather catch before the GPU spend than in the report.

---

**Generated-by:** Stream 2 (Sonnet 5) | **Evidence:** `ESCALATIONS.md` E-007/E-009/E-011/E-014,
`briefs/STREAM2_TO_STREAM3_WPE_SEQUENCE_REVIEW_2026_07_26.md` (A–E),
`briefs/STREAM2_TO_STREAM3_GUIDELINES_2026_07_26.md` (§5 asks),
`briefs/T0_DECISIONS_2026_07_26.md` (D2), `stream3_mirror/NO_PREDICTION_BRANCH.md` (G1-L),
`PREDICTION.md` v1.1 §6 | **Reviewed-by:** Xavier (T0) — pending
