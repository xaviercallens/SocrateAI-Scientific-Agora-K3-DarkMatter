# ✅ TODO — 2026-07-26

**Critical path:** T0 decisions (blocking Gate E) → Stream 2 geometry redo → Stream 3 Gate E

> Previous TODO (2026-07-24: C1/C2 for s10, Lean Sym² encoding) is **complete or superseded**.
> The C1/C2 items it listed were done, then corrected by F6, and their Kodaira labels are now
> under the open finding below.

---

## T0 decisions — ✅ DECIDED 2026-07-26 (`briefs/T0_DECISIONS_2026_07_26.md`)

- [x] **D1 — Gate E criterion 1: UNRESOLVED**; other five proceed; date kept. Best
      achievable verdict = CONDITIONAL. Handoff sent →
      `briefs/STREAM2_TO_STREAM3_GATE_E_CRITERION1_2026_07_26.md`
- [x] **D2 — M1 accepted** (conditional negative); Phase M dormant, gated on Route γ; M2 unauthorized
- [x] **D3 — Stream 3 mirroring DELIVERED 2026-07-26** → `stream3_mirror/` (25 files, hash-pinned,
      source commit `3d18add`; claims re-verified at mirror time — see `stream3_mirror/README.md`,
      incl. β₁=29/30 precision note). Standing returned-for-provenance rule in force.
- [x] **D4 — Wall-3 renunciation = standing policy** → ASSUMPTIONS.md addendum **A-DE**
- [x] Expected-outputs amendment — overtaken by E-007 closure (retraction is permanent)

### 🔶 Remaining open T0 item (explicitly NOT covered by the 2026-07-26 authorization)
- [ ] **WP-B1 sign-off** on two documented deviations → `briefs/STREAM1_WP_B1_RESULTS.md`
      (incl. the fact that the brief's `no_unscreened_lmp` was specified as a false theorem)

---

## 🟢 E-007 RESOLVED (2026-07-26) — root cause established, C1/C2 layer retracted

**L₂ is a twisted PF operator, not a PF operator.** Two independent confirmations:
- `checkers/check_C1_kodaira_consistency.py`: exponents [0, 1/2], det(monodromy) = −1
  ∉ SL₂(ℤ) ⇒ **no Kodaira type derivable** (not I₁, not II).
- Deep Think (T0s) + verification here: **g.f.(A279619)² = g.f.(A183204)** exactly on
  all 8 terms. The square root halves {0,0} → {0,½} and flips det to −1.
- s7's real substrate is **X₀(7)**, CM by ℚ(√−7) — not a Beauville elliptic surface.

**Permanently retracted:** C1/C2 certs (v1 + v2), ρ=4, T=18, discriminant=−3.
Cause: hardcoded `components = 2` in a wrong lookup (`exponents_to_kodaira_type`),
now **hard-disabled (raises)**.

Artifacts: `ESCALATIONS.md` E-007 · `data/certificates/C1_KODAIRA_CONSISTENCY.json` ·
`briefs/STREAM2_ACTION_PLAN_2026_07_26.md`

**Unaffected:** L₃=Sym²(L₂) (Tier A — this *confirms* it); exact singular loci; WP-B1.

---

## Stream 2 — Geometry redo

- [x] Phase 0 reconciliation + root cause (E-007 closed)
- [x] Hard-disable `exponents_to_kodaira_type()`; mark `compute_C1_monodromy.py` RETRACTED

### Phase 1: Provenance gate — ✅ SUBSTANTIALLY DONE (2026-07-26); 2 sources outstanding
- [x] `docs/literature/` + `refs/literature_provenance.txt` created
- [x] Fetched + hash-pinned **Almkvist–van Straten arXiv:2103.08651** and
      **Gorodetsky arXiv:2102.11839**; identity verified from front matter
- [x] `checkers/check_literature_provenance.py` (honest scope in docstring) — **PASS**
- [x] **Cross-validation:** A–vS's printed operator coefficients match the repo's exactly;
      their printed Riemann symbols match our independently computed schemes exactly
- [ ] Still unfetched: Cooper 2012 (Ramanujan J. 29, paywalled); O'Brien 2016 MSc thesis;
      Chan–Cooper–Sica 2010; **Stienstra–Beukers 1985 Math. Ann. 271** ← would close the ρ/T step

### 🟢 E-009 RESOLVED (2026-07-26) — the K3 EXISTS
A–vS §"three sporadic third order operators" *is* our s7/s10/s18, and gives explicit constructions:
- **s7** = their Sporadic 2 → K3 = **intersection of six hyperplane sections of the Grassmannian G(2,6)** (Plücker)
- **s10** = their Sporadic 1 → K3 = **intersection of four hyperplane sections of type (1,1) in P³×P³**

The category worry is answered: there IS a K3. Order-2 elliptic points (E-008) are features
of the modular parametrization, not evidence against it — both coexist, as in classical Apéry.
**Residual:** A–vS state no Picard number, so ρ=19/T=3 now rests on the standard
order-3-sub-VHS ↔ transcendental-lattice identification — **[B] awaiting citation**, no longer
conditional on an unproven existence claim. `Stienstra–Beukers 1985` would close it.

### 🎁 s18 UNBLOCKED (corrupt since 2026-07-20)
A–vS Sporadic 3 gives `Q₃=192z²−28z+1, Q₂=576z²−42z, Q₁=564z²−26z, Q₀=180z²−6z`;
regenerates 1, 6, 54, 564, 6390, 76356, 948276 exactly.
- [ ] Fold the recovered s18 operator into `refs/recurrences_v1.json` (currently BLOCKED there)

### Phase 2: ⚠️ REVISED TWICE — Routes α and β both REFUTED (E-008)
> Neither Deep Think's Route A (use L₃) nor any gauge transform works. Both tested and closed.

- [x] Test Route A premise → **REFUTED**: L₃ exponents are **{0, ½, 1}**, not unipotent
      (`scripts/compute_L3_monodromy.py`; Sym² of {0,½} = {0,½,1} — cross term keeps ½)
- [x] Route β (gauge transform) → **REFUTED**: exponent *differences* are gauge-invariant,
      so a difference of ½ cannot be gauged away (incl. fractional twists like P₂^{1/4})
- [x] Emit `C1_L3_cooper_s{7,10}.json` with `picard_rank: null` (deliberate — no fabrication)

**Route γ — ramified Hauptmodul pullback (only surviving path):**
- [x] **Step 0: composition CONFIRMED** — `g.f.(A002652) = F(t(q))` exact to order 29
      (`checkers/check_route_gamma_step0.py`, `data/certificates/ROUTE_GAMMA_STEP0.json`).
      Hauptmodul t = A279618 is the correct uniformizing coordinate. **No ρ/T emitted.**
- [x] **Step 1: PASS** — `checkers/check_route_gamma_step1.py`. Both singular loci are
      **simple critical values** of t (t′=0, t″≠0 ⇒ ramification index **m = 2 exactly**),
      so exponents {0, ½} ↦ **{0, 1}, integral — the branch cut clears.**
      z = 1/27 to **17 significant digits**; z = −1 to ~3 digits (nearer the convergence
      radius — weaker, flagged). Certificate `ROUTE_GAMMA_STEP1.json`. **No ρ/T emitted.**
      → **E-008 RESOLVED.**

### 🔴 E-009 (NEW, OPEN) — is a Kodaira/Picard reading category-correct at all?
> The ½ cleared *because* these look like **order-2 elliptic points** of a Fuchsian group —
> which have finite-order monodromy by construction and are **not** Kodaira degenerations.
> Three retractions (F6, E-007, E-008) were all downstream of forcing a fibration reading
> onto a modular object. This ticket names that assumption.

- [x] **Lead 2 WORKED** (`checkers/check_L3_riemann_scheme.py`, `L3_RIEMANN_SCHEME.json`):
      complete Riemann scheme computed exactly — s7 {0,0,0} MUM / {0,½,1} / {2/3,1,4/3},
      **Fuchs Σ = 6 exact**; **W(L₃)=W(L₂)³ confirmed** (rank-3 orthogonal from rank-2
      symplectic = a K3 transcendental form).
      → **ESTABLISHED UNCONDITIONALLY: ρ=4/T=18 is structurally IMPOSSIBLE** — an order-3
      operator governs a rank-3 system, not rank-18. Independent second argument for E-007.
      → **T=3 / ρ=19 is the unique consistent assignment, but CONDITIONAL on E-009.**
      Recorded as conditional; ρ/T still `null`. Do not cite as derived.
- [x] **Lead 1 CORROBORATED [B]:** implied signature genus 0, elliptic (2,2,3), 1 cusp,
      area 2/3 = **Γ₀(7)+ exactly** (Fricke halves Γ₀(7)'s 4/3; 2 cusps→1; 2 order-3→1;
      w₇'s 2 fixed points → the 2 order-2 points). Predicted from a count, met by an
      independent exponent computation. Still [B], not a rigorous identification.
- [ ] **E-009 core question remains OPEN:** does a K3 EXIST whose transcendental sub-VHS
      L₃ governs? Passing preconditions is not existence. This is now the single blocker.
- [ ] Only if that resolves: emit C1/C2 v3, notify Stream 3, then a revised M1′ is draftable


### Phase 3: C2 v3 (2–3 h) — only after Phase 2 yields a genuine PF operator
- [ ] Shioda–Tate with **derived** mᵥ: ρ = 2 + Σ(mᵥ−1) + rank MW
- [ ] **Compute** rank MW (v2 assumed 0 with no derivation)
- [ ] τ = 22 − ρ; intersection form; discriminant — derived, not pre-declared
- [ ] Emit `C2_cooper_s{7,10}_v3.json`
- [ ] **If ρ ≠ 4 → notify Stream 3 immediately** (D-3 prior changes)

### Phase 4: Physics interpretation — ⛔ BLOCKED on Phase 2/3
- [x] **GUT-claim audit (Deep Think "Fallacy B")** — repo scanned for `SU(5)|SO(10)|GUT`:
      4 hits, **all already correctly hedged** (`CAVEATS.md` "Not attempted";
      `PHASE_10_K3_SELECTION.md` carries **[C]** + "not a result"; handoff brief mandates
      the marker; `alpha_origin_rge.py` is a normalization comment). **No scrub needed —
      the guardrails held.** The SU(5)/SO(10) language came from the proposed plan, not the repo.
- [ ] Restrict claims to what real C1/C2 data supports (dark-sector coupling structure),
      **not** GUT embeddings
- [ ] Every phenomenological leap carries an inline `[C] CONJECTURE` marker **in the same sentence**
- [ ] Deliverable: physics brief — retitle to match whichever operator/coordinate actually
      yields the geometry (Deep Think's `PHYSICS_INTERPRETATION_L3.md` presumes L₃, now blocked)
- [ ] Guardrail holds: "load-bearing physical vacuum" framing **not adopted**

### Phase M: Astrophysical model construction (Fable 5 T0 directive, 2026-07-25)
- [x] **M1 mechanism memo delivered & T0-ACCEPTED** (decision D2) →
      `briefs/STREAM2_M1_MECHANISM_MEMO_2026_07_26.md` — conditional negative;
      Wall 3 routed by renunciation (now ASSUMPTIONS.md **A-DE**)
- [x] Stop-point cleared (T0 acceptance 2026-07-26)
- [x] Mirroring delivered (D3) → `stream3_mirror/` — M2's artifact precondition is now met (Route γ still required)
- [ ] Phase M **DORMANT**: M2–M4 open only after Route γ delivers C1v3/C2v3 AND T0 re-opens against a revised M1′

---

## Stream 1 — Complete (maintenance only)

- [x] `L₃ = Sym²(L₂)` kernel-verified, axiom-clean
- [x] WP-B1: 4/4 DoD lemmas, zero `sorry`, 10/10 golden tests
- [x] `B1_Sym2Bridge.lean` (B3 interface), `B1_AxiomAudit.lean`, CI gate
- [ ] Awaiting T0 sign-off (see Blocking above)
- [ ] Optional: tighten `h_scale` in `no_unscreened_lmp` once C1 v3 lands (Stream 2 request)
- [ ] Optional: s18 recurrence recovery — unblocked by the Phase 1 Gorodetsky fetch

---

## Stream 3 — D-3 running

- [x] Phase 2 infrastructure deployed; batch launched
- [ ] Batch completion → aggregation → statistical report
- [ ] Gate E verdict **2026-07-27 EOD UTC** (Xavier)
- [x] Criterion 1 decision taken (D1): score **UNRESOLVED**, retain outputs as re-scorable data
- [ ] Apply D1 at aggregation/verdict → `briefs/STREAM2_TO_STREAM3_GATE_E_CRITERION1_2026_07_26.md`
- [x] D3 mirroring delivered (done by Stream 2, 2026-07-26) → `stream3_mirror/`

---

## Housekeeping

- [ ] **Rotate the GitHub token embedded in `.git/config`.** `git remote -v` prints a
      plaintext `ghp_…` PAT. Revoke it and switch to SSH or a credential helper.
