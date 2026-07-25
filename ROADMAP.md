# 🗺️ ROADMAP: Dual-Scale Topological Universe Model (K3×T² + D-brane Dynamics)

**Last updated:** 2026-07-26 | **Status:** Stream 1 ✅ COMPLETE (Sym² + WP-B1); Stream 2 🔴 C1 KODAIRA LABELS UNSUPPORTED; Stream 3 🔄 D-3 running, Gate E 2026-07-27 EOD

---

## 🟢 E-007 RESOLVED (2026-07-26) — C1/C2 layer permanently retracted; root cause established

**L₂ is a *twisted* Picard–Fuchs operator, not a PF operator. K3 geometry cannot be
extracted from it as-is.** Independently established two ways:

- `checkers/check_C1_kodaira_consistency.py` (Opus 5): L₂ local exponents are
  **[0, 1/2], Δ = 1/2, det(monodromy) = −1** at all four loci. det = −1 ∉ SL₂(ℤ),
  and every Kodaira monodromy has det +1 ⇒ **no Kodaira type is derivable at all**
  (not I₁, not II).
- Deep Think (T0s) literature review + verification here: **A279619's g.f. is exactly
  the square root of A183204's g.f.** — re-verified from `refs/recurrences_v1.json`,
  exact on all 8 terms. Squaring a unipotent {0,0} operator's solution halves the
  exponents to {0, ½} and flips the monodromy determinant. The irrational Wronskian
  `W = C/(z√P₂)` is that twist's analytic signature.
- **Real geometric substrate for s7:** modular curve **X₀(7)**, CM by ℚ(√−7) — *not*
  a Beauville rational elliptic surface. (O'Brien 2016 MSc thesis Thm 6.1;
  Chan–Cooper–Sica 2010 Conj 5.4.)

**Retracted permanently:** C1/C2 certificates (v1 **and** v2), **ρ = 4**, **T = 18**,
**discriminant = −3**. Cause: `exponents_to_kodaira_type()` in
`scripts/compute_C1_monodromy.py` had a wrong lookup table *and* a hardcoded
`components = 2`, which mechanically produced ρ = 2+2+0 = 4. That function is now
**hard-disabled (raises)**; the script is marked RETRACTED.

**Downstream — T0 action needed:** Stream 3's D-3 batch runs with ρ=4, T=18 as its
lattice prior. Withdrawn ⇒ **Gate E criterion 1 cannot be scored PASS**.
Recommend: score it UNRESOLVED, proceed on the other five, keep 2026-07-27.

**Untouched:** L₃ = Sym²(L₂) (Tier A — this resolution *confirms* it); the exact
singular loci; all WP-B1 chameleon results.

→ `ESCALATIONS.md` E-007 · `briefs/STREAM2_ACTION_PLAN_2026_07_26.md`

---

## Executive Summary

### 🎯 T0 SIGN-OFF (2026-07-24 EOD)
**Xavier Callens (T0 Owner) officially approves Streams 1 & 2 and authorizes Stream 3 go-ahead.**

→ See: `briefs/APPROVAL_STREAM1_2_T0_SIGNOFF_2026_07_24.md` (official T0 sign-off)  
→ See: `briefs/STREAM3_GO_AHEAD_2026_07_24.md` (explicit Stream 3 authorization + 5-phase roadmap)

**Implications:**
- ✅ v0.3.0 is **LIVE** (approved for deployment)
- 🚀 Stream 3 **BEGIN PHASE 1** (local checks → GPU deployment)
- 📅 Gate E verdict expected 2026-07-27 EOD → v0.4.0 release decision

---

### What's Done ✅
- **C3b Resolution (2026-07-24):** s7/s10 order-2 Shioda–Inose partners extracted; all-n L₃=Sym²(L₂) proven at CAS level (Deep Think CONCUR verified independently)
- **Stream 1 Sym² (2026-07-24):** `L₃ = Sym²(L₂)` kernel-verified in Lean 4, axiom-clean
- **Stream 1 WP-B1 Chameleon (2026-07-25/26):** 4/4 DoD lemmas kernel-verified, zero `sorry`;
  B3/SYM2_PARTNER bridge compiles; CI gate live. ⚠️ Found the brief's `no_unscreened_lmp`
  was **false as specified** — recorded in-kernel and restated. Two deviations await T0 sign-off.
  → `briefs/STREAM1_WP_B1_RESULTS.md`
- **Stream 2 F6 rectification (2026-07-25):** singular loci corrected from index-space to
  z-space: s7 {1/27, −1}, s10 {1/16, −1/4}. ✅ Independently re-confirmed 2026-07-26.
  *(The earlier "2 Kodaira-II fibres at z = 1/3, 2/3" entry was the pre-F6 error and is retracted.)*
- **Stream 3 D-3:** Phase 2 batch running; Gate E 2026-07-27 EOD

### ⚠️ What's NOT established
- **Kodaira fibre types** for s7/s10 — see Open Finding above. Neither "II" (v2 certs)
  nor "I₁" (proposed plan) is supported by the exponent data.
- **ρ = 4, T = 18** — does not follow from the current fibre data; needs Weierstrass-model redo.
- **discriminant = −3** — appears only in the **superseded v1** certs, which are marked
  *"F6 retracted: fabricated from incorrect C1."* Do not carry forward.

### Critical Path
```
Stream 2:  Phase 1 provenance gate ──→ C1 v3 via Weierstrass/Tate ──→ C2 v3 (ρ, τ derived)
             ↓                                                          ↓
             └──────────────────────────────→ Stream 3 lattice prior ───┘
                                                     ↓
Stream 3:  D-3 empirical rerun ──→ Gate E verdict (criterion 1 currently UNRESOLVED)
```

---

## Detailed Status by Stream

### Stream 1: Lean 4 Formalization (Opus 4.8)

| Task | Status | Blocker | Next |
|---|---|---|---|
| **L₃ = Sym²(L₂) proof (s7/s10)** | ✅ SYM2_PROVED | — | Kernel-verified, axiom-clean (2026-07-24) |
| **D1 Option B (Polynomial Identity)** | 🟢 DESIGN COMPLETE | — | Encode P_cleared(z)≡0 for generic Cooper family |
| **Frobenius Solutions (D2 WZ)** | 🟡 QUEUED | Fetch G(n,k) from arXiv:2102.11839 | Mining certificates if needed |
| **Axiom Hygiene (S1-1)** | 🟢 DISCHARGED | — | `pipeline_upper_bound` disclosure live |
| **Register Freeze (D5)** | 🟢 LIVE | s18 stays BLOCKED | Maintain: {s7, s10} Tier A; {s18} Tier B |

**✅ COMPLETED (Stream 1, 2026-07-24): `L₃ = Sym²(L₂)` kernel-verified in Lean 4.**
File `lean4_formal_proofs/Structures/CooperSym2Proof.lean` proves, for BOTH s7 and s10,
the θ-basis coefficient identities (θ = z·d/dz, exact in ℚ[z]):
- Q₃ = P₂ (θ³)
- Q₂ = 3·P₁ (θ²)
- Q₁ = θ(P₁) + 4·P₀ (θ¹)
- Q₀ = 2·θ(P₀) (θ⁰)
- collapse: θ(P₂) = 2·P₁

Discharged by `simp [Polynomial.derivative_*] + ring`. **NO `sorry`, NO `axiom`, NO
`native_decide`.** Axioms: `[propext, Classical.choice, Quot.sound]` (Mathlib foundational
only, verified via `#print axioms`). `lake build Structures.CooperSym2Proof` = 0 errors.
Repo status → **[A] SYM2_PROVED** (`PROOF_STATUS.txt`).

Scope guard (VISION §1.3): mathematical operator identity only — no bulk↔brane physical
coupling is claimed (that remains Tier C).

---

### Stream 2: K3 Selection (Theory & Checkers)

| Task | Status | Completion | Next |
|---|---|---|---|
| **C3b Partner Extraction** | ✅ RESOLVED | 2026-07-24 | — |
| **All-n L₃=Sym²(L₂) (CAS)** | ✅ PROVEN | 2026-07-24 | — |
| **Exact singular loci (s7, s10)** | ✅ CONFIRMED | 2026-07-25 (F6), re-verified 2026-07-26 | — |
| **C1 Kodaira types (s7, s10)** | 🔴 UNSUPPORTED | — | Redo via Weierstrass model + Tate's algorithm |
| **C2 Lattice ρ, τ (s7, s10)** | 🔴 UNSUPPORTED | — | Blocked on C1 v3 |
| **Provenance gate (literature)** | 🟡 NOT STARTED | — | Fetch 4 PDFs, hash-pin, write honest checker |
| **Physics interpretation** | ⛔ BLOCKED | — | Gauge groups need fibre types |

**Deliverable (Stream 2):** C1 v3 / C2 v3 certificates with fibre types derived from
Tate's algorithm, then the physics brief. → `briefs/STREAM2_ACTION_PLAN_2026_07_26.md`

**Note on tooling:** `checkers/check_C1.py` and `check_C2.py` are **deprecated** (F6).
`checkers/check_C1_kodaira_fibers.py` / `check_C2_picard_lattice.py` do **not** exist.
The live adversarial checker is `checkers/check_C1_kodaira_consistency.py`.

---

### Stream 3: Experimentation (Empirical Validation)

| Task | Status | Blocker | Next |
|---|---|---|---|
| **D-3 Empirical Rerun** | 🟡 UNBLOCKED | ← Awaits C1/C2 completion | Queue sectors in DarkMatter@Home v2 |
| **GPU Validation (DM-1)** | ⏳ READY | — | Runs after D-3 sectors land |
| **Quorum Aggregation (DM-2)** | ⏳ READY | — | Consensus from 3+ independent runs |
| **Human Verdict (E)** | ⏳ DESIGN | — | Final go/no-go decision |

**Timeline:** D-3 runs in parallel with Stream-1 Lean (no dependency). E verdict in ~1 week if D-3 completes.

---

## Release Milestones

| Version | Target | Description |
|---|---|---|
| **v0.2.0** | 🟢 DONE | C3b partners extracted; all-n proof (CAS) |
| **v0.3.0** | 🟡 THIS WEEK | Stream 2 C1/C2 complete (s7/s10); Stream 1 Lean SYM2_PROVED |
| **v0.4.0** | 📅 EOW | Stream 3 D-3 complete; Gate E verdict |
| **v1.0.0** | 🎯 TBD | Final peer review + publication-ready |

---

## Physics-Washing Guardrails (ENFORCED)

✅ **Maintained in all deliverables:**
- L₂-as-brane / bulk↔brane coupling remain **Tier C** (explicit conjecture marker required)
- Deep Think's "load-bearing physical vacuum" framing **NOT adopted**
- Geometry ≠ physics — Sym² relation verified as mathematics, not as EFT proof
- All checker verdicts report **Tier B** (checkable but unproven), never physics claims

---

## Next 48 Hours: Prioritized Actions

### 🔴 Blocking (T0 — Xavier)
1. Decide Gate E scoring for criterion 1 given the unsupported ρ = 4 prior
   (recommend: score UNRESOLVED, let the other five proceed, keep 2026-07-27)
2. Decide: annotate vs. retract the v2 C1/C2 certificates (recommend annotate)
3. Sign off (or amend) the two WP-B1 deviations → `briefs/STREAM1_WP_B1_RESULTS.md`

### Immediate (Stream 2)
1. ✅ Phase 0 reconciliation → `check_C1_kodaira_consistency.py` (DONE 2026-07-26)
2. ⏳ Phase 1 provenance gate — fetch 4 PDFs, hash-pin, honest checker (1–2 h)
3. ⏳ Phase 2 C1 v3 — Weierstrass model + Tate's algorithm (8–14 h)
4. ⏳ Phase 3 C2 v3 — Shioda–Tate from v3 fibre data, derive rank MW (2–3 h)

### Stream 1 (complete — maintenance only)
1. ✅ Sym² kernel-verified; ✅ WP-B1 4/4 lemmas + bridge + CI gate
2. ⏳ Awaiting T0 sign-off on two documented WP-B1 deviations
3. ⏳ Optional: tighten `h_scale` in `no_unscreened_lmp` once Stream 2 lands C1 v3

### Parallel (Stream 3 — GPU)
1. 🔄 D-3 Phase 2 batch running
2. ⏳ Aggregation + statistics; Gate E verdict 2026-07-27 EOD
3. ⚠️ Lattice prior (ρ=4, T=18) currently unsupported — see Open Finding

---

## Known Blockers & Workarounds

| Blocker | Workaround | Status |
|---|---|---|
| s18 corrupt recurrence | BLOCKED — re-transcribe from arXiv | Flagged; no action required |
| s10 rational partner (non-integral) | Lattice claims marked provisional | Accepted; proceed with C1/C2 |
| D-3 empirical precision | Stream 3 quorum re-run | Authorized; queued |

---

## Epistemic Audit Trail

- ✅ Rule 1 (Real arithmetic): All numbers from committed checkers, no model memory
- ✅ Rule 4 (Honest reporting): Verification artifacts (certs) in same commits
- ✅ F6 correction: A002893 classification corrected; zagier_sporadic_A record updated
- ✅ Two-Model Rule: L₃=Sym²(L₂) re-derived independently (θ-basis + monic d/dz routes) before operator-form gate cleared

---

**Current Authority:** Xavier (T0 Owner) + Deep Think (T0s Concurrence) + Stream-1/2/3 execution mandates
