# 🗺️ ROADMAP: Dual-Scale Topological Universe Model (K3×T² + D-brane Dynamics)

**Last updated:** 2026-07-26 (evening) | **Release:** `v0.3.4`

> ## ⬛ READ THIS FIRST — current state supersedes everything below
>
> | | |
> |---|---|
> | **Stream 1** | ✅ **PARKED CLEAN.** Sym² + WP-B1 signed off; 2 goals `blocked-on-mathlib`. |
> | **Stream 2** | ✅ **MATHEMATICS COMPLETE.** ρ = 19, T = 3 **DERIVED** [tier B] (E-011). |
> | **Stream 3** | 🟡 **D-3 NOT RUNNABLE** (E-012). WP-E transverse study live on Dark Home. |
> | **Physics** | 🔴 **F5b — no prediction extractable.** Adopted into `PREDICTION.md` **v1.1-PINNED** §6. |
> | **Gate E** | criteria 1–2 **UNSCOREABLE** (no valid run). *Not failing.* |
>
> **The programme has contracted to its Tier A mathematical content, per `VISION.md` §5.**
> That content is substantial and publishable on its own merits. This is a **pre-registered,
> reportable outcome — not a failure, and not a refutation.** F5b means no prediction could be
> *extracted*; none was tested and failed. It is **reversible**: exhibit a flux stabilization
> plus a non-fibration route to the dark gauge sector and S3-00 reopens.
>
> **Tickets:** `ESCALATIONS.md` E-007 … E-013. **Restart here:** `TODO.md`.

---

## 🟢 E-007, E-008, E-009 ALL RESOLVED (2026-07-26) — C1/C2 retracted; Route γ succeeded; **the K3 exists**

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
- **Real geometric substrate for s7:** a **level-7 modular** parametrization — O'Brien 2016
  Thm 6.1 gives `z7 = Σ c7(n) X7ⁿ` with `X7 = η₁³η₇³/z7³`. ⚠️ **Rescoped 2026-07-26** (commit
  `c7ba6fb`): that thesis does **not** state "X₀(7)" or "CM by ℚ(√−7)" — zero hits. Those rest
  on the separate disc-(−7) fact about A002652, not on this source. Cite it only for the
  generating-function/level-7 identity.

**Retracted permanently:** C1/C2 certificates (v1 **and** v2), **ρ = 4**, **T = 18**,
**discriminant = −3**. Cause: `exponents_to_kodaira_type()` in
`scripts/compute_C1_monodromy.py` had a wrong lookup table *and* a hardcoded
`components = 2`, which mechanically produced ρ = 2+2+0 = 4. That function is now
**hard-disabled (raises)**; the script is marked RETRACTED.

**Downstream — ✅ T0 DECIDED (D1, 2026-07-26):** criterion 1 scored **UNRESOLVED**;
other five proceed; date kept; criterion-1 outputs retained as re-scorable data.
Best achievable Gate E outcome = **CONDITIONAL**. → `briefs/T0_DECISIONS_2026_07_26.md`

**Untouched:** L₃ = Sym²(L₂) (Tier A — this resolution *confirms* it); the exact
singular loci; all WP-B1 chameleon results.

**🔴 E-008 (2026-07-26, OPEN) — the proposed replacement path is ALSO refuted.**
Deep Think's course-correction mandated "Route A: run C1/C2 on L₃ instead," premised on
L₃ being unipotent. **Tested and false:** `scripts/compute_L3_monodromy.py` gives L₃
exponents **{0, ½, 1}** at every finite locus. Sym² of {0,½} is {0, ½, 1} — only y₂²
doubles to 1, the **cross term y₁y₂ keeps ½**. Kodaira is blocked at the L₃ level too.
The gauge-transform escape is also closed: **exponent differences are gauge-invariant**.
**Route γ SUCCEEDED (2026-07-26) — E-008 RESOLVED.** Step 0: `g.f.(A002652)=F(t(q))` exact
to order 29. Step 1: both singular loci are **simple critical values** of the Hauptmodul
(m = 2 exactly) ⇒ exponents {0,½} ↦ **{0,1}, integral — the branch cut clears** (1/27 to
17 digits; −1 to ~3 digits, flagged).

**But the reason it cleared is the real finding, now 🔴 E-009:** ½ + ramification 2 is the
signature of an **order-2 elliptic point** of a Fuchsian group — finite-order monodromy by
construction, **not** a Kodaira degeneration. All three retractions (F6, E-007, E-008) were
downstream of forcing a fibration reading onto a modular object. Leads (both [B], untested):
the group is likely **Γ₀(7)+**; and L₃'s order 3 suggests **T=3, ρ=19**.

**Both leads worked (2026-07-26).** L₃'s complete Riemann scheme (exact): s7 has
{0,0,0} **MUM** at 0, {0,½,1} at ±loci, {2/3,1,4/3} at ∞, **Fuchs Σ=6 exact**, and
**W(L₃)=W(L₂)³** (rank-3 orthogonal from rank-2 symplectic — a K3 transcendental form).
→ **ESTABLISHED UNCONDITIONALLY: ρ=4/T=18 is structurally IMPOSSIBLE** (order-3 operator
⇒ rank-3 system, never rank-18) — an independent second argument for E-007.
→ **T=3/ρ=19 is the unique consistent assignment — but CONDITIONAL on E-009.**
→ **Lead 1 corroborated [B]:** implied signature (genus 0; 2,2,3; 1 cusp; area 2/3)
matches **Γ₀(7)+** exactly. All certificates still emit ρ/T as `null` by design.

**🟢 E-009 RESOLVED — the K3 EXISTS.** Phase 1 provenance gate fetched Almkvist–van Straten
(arXiv:2103.08651, hash-pinned). Its "three sporadic third order operators" are *ours*, stated
verbatim: *"also found by S. Cooper … called s10, s7 and s18"*. Explicit K3 constructions:
**s7** → intersection of six hyperplane sections of the Grassmannian **G(2,6)** (Plücker);
**s10** → intersection of four hyperplane sections of type (1,1) in **P³×P³**.
Their *printed* Riemann symbols and operator coefficients match our independent computations
**exactly** — external validation of the whole Stream 2 computation chain.
**🎁 s18 recovered** (corrupt since 2026-07-20). **Residual:** A–vS state no Picard number, so
ρ=19/T=3 is now **[B] awaiting citation** (Stienstra–Beukers 1985), not conditional on existence.

→ `ESCALATIONS.md` E-007, E-008, E-009 (all resolved) · `briefs/STREAM2_ACTION_PLAN_2026_07_26.md`

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
- **ρ = 4, T = 18** — withdrawn. Cannot be recomputed from L₂ *or* L₃ (both carry a ½ exponent);
  requires the Route γ ramified Hauptmodul pullback first (E-008).
- **discriminant = −3** — appears only in the **superseded v1** certs, which are marked
  *"F6 retracted: fabricated from incorrect C1."* Do not carry forward.

### Critical Path
```
Stream 2:  Phase 1 provenance gate ──→ Route γ Hauptmodul pullback ──→ C1/C2 v3 (ρ, τ derived)
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
| **C1 Kodaira types (s7, s10)** | 🟡 UNBLOCKED | — | K3 exists (E-009); classify fibres from the A–vS explicit models, not from L₂/L₃ exponents |
| **C2 Lattice ρ, τ (s7, s10)** | 🔴 UNSUPPORTED | — | Blocked on C1 v3 |
| **Provenance gate (literature)** | 🟢 SUBSTANTIALLY DONE | 2026-07-26 | A–vS + Gorodetsky pinned & cross-validated; 2 sources outstanding |
| **Physics interpretation** | ⛔ BLOCKED | — | Gauge groups need fibre types |

**Deliverable (Stream 2):** C1 v3 / C2 v3 certificates with fibre types derived from an
operator with **integral** exponents (Route γ), then the physics brief.
→ `briefs/STREAM2_ACTION_PLAN_2026_07_26.md`

**Standing rule:** emit no ρ and no T until such an operator is in hand.
`C1_L3_cooper_s{7,10}.json` set them to `null` deliberately.

**Note on tooling:** `checkers/check_C1.py` and `check_C2.py` are **deprecated** (F6).
`checkers/check_C1_kodaira_fibers.py` / `check_C2_picard_lattice.py` do **not** exist.
Live checkers: `checkers/check_C1_kodaira_consistency.py` (L₂, E-007) and
`scripts/compute_L3_monodromy.py` (L₃, E-008).

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

### ✅ T0 decisions D1–D4 taken 2026-07-26 → `briefs/T0_DECISIONS_2026_07_26.md`
1. ✅ D1: Gate E criterion 1 = UNRESOLVED (best outcome now CONDITIONAL); handoff sent to Stream 3
2. ✅ v2 certificates: permanently retracted (E-007 closure)
3. 🔶 **Still open (not covered by the authorization):** WP-B1 deviation sign-off → `briefs/STREAM1_WP_B1_RESULTS.md`

### Immediate (Stream 2)
1. ✅ Phase 0 reconciliation → `check_C1_kodaira_consistency.py` (DONE 2026-07-26)
2. ⏳ Phase 1 provenance gate — fetch 4 PDFs, hash-pin, honest checker (1–2 h)
3. ✅ Phase 2 **Route γ steps 0+1 PASS** — branch cut clears (E-008 resolved); next: **E-009** (is a Kodaira/Picard reading category-correct?)
4. ⏳ Phase 3 C2 v3 — Shioda–Tate from v3 fibre data, derive rank MW (2–3 h)
5. ✅ **Phase M / M1 memo (T0 directive)** — conditional negative filed; Phase M gated on
   Route γ + T0 review → `briefs/STREAM2_M1_MECHANISM_MEMO_2026_07_26.md`
6. ✅ **D3 mirror delivered** — Stream 3 WP-R artifacts + data outcomes hash-pinned into
   `stream3_mirror/` (claims re-verified; β₁=29/30 precision note in its README)

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
