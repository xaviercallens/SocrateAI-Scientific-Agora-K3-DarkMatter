# ✅ TODO — 2026-07-26

**Critical path:** T0 decisions (blocking Gate E) → Stream 2 geometry redo → Stream 3 Gate E

> Previous TODO (2026-07-24: C1/C2 for s10, Lean Sym² encoding) is **complete or superseded**.
> The C1/C2 items it listed were done, then corrected by F6, and their Kodaira labels are now
> under the open finding below.

---

## 🔴 BLOCKING — T0 decisions (Xavier)

- [ ] **Gate E criterion 1.** Stream 3's D-3 batch runs with ρ=4, T=18 as its lattice prior.
      That prior is unsupported (see finding below). Decide:
      **(a) score criterion 1 UNRESOLVED and proceed on the other five** *(recommended)*,
      (b) delay Gate E pending Stream 2 Phase 2–3, or
      (c) proceed and annotate the prior as Tier B-provisional.
      **Needed before 2026-07-27 EOD.**
- [ ] **v2 certificates:** annotate with `known_inconsistency` *(recommended)* or retract?
- [ ] **WP-B1 sign-off** on two documented deviations → `briefs/STREAM1_WP_B1_RESULTS.md`
      (incl. the fact that the brief's `no_unscreened_lmp` was specified as a false theorem)
- [ ] **Amend the proposed Stream 2 plan's expected outputs** — `[I₁,I₁]` and `ρ=4` cannot both hold

---

## 🔴 OPEN FINDING — C1 Kodaira labels unsupported (2026-07-26)

`checkers/check_C1_kodaira_consistency.py` re-derives the L₂ exponents independently:
**[0, 1/2], Δ = 1/2, det(monodromy) = −1** at all four loci, both partners.

- Not I₁ (unipotent, Δ=0). Not II (order 6, Δ=1/6).
- det = −1 ∉ SL₂(ℤ) ⇒ **no Kodaira type derivable from these exponents**.
- ρ=4 needs mᵥ=2; "II" has m=1 ⇒ would give ρ=2. **v2 certs self-contradict.**
- Likely cause: half-integer exponents are the Sym²-root signature, so L₂'s singular
  points are probably not the fibration's singular fibres.

Artifacts: `data/certificates/C1_KODAIRA_CONSISTENCY.json`,
`briefs/STREAM2_ACTION_PLAN_2026_07_26.md`

**Unaffected:** L₃=Sym²(L₂) (Tier A); exact singular loci; all WP-B1 results.

---

## Stream 2 — Geometry redo

### Phase 1: Provenance gate (1–2 h) — unblocks literature-derived claims
- [ ] `mkdir docs/literature/`; create `refs/literature_provenance.txt`
- [ ] Fetch Almkvist–van Straten (arXiv:2103.08651)
- [ ] Fetch Gorodetsky (arXiv:2102.11839) — *also unblocks the corrupt s18 recurrence*
- [ ] Fetch Zagier 2009; Cooper 2012 (Ramanujan J. 29)
- [ ] SHA256 + pin hashes; manually cross-check (a,b,c,d) vs PDFs and OEIS
- [ ] Write `checkers/check_provenance_hygiene.py` — scope honestly in the docstring
      (hashes + document identity + Cooper parameter sets; **not** 15 sequences, no OEIS lookup)

### Phase 2: C1 v3 via Weierstrass model (8–14 h) — replaces the old exponent→Kodaira route
- [ ] Construct Weierstrass model for s7 and s10
- [ ] Compute discriminant Δ(z) and j-invariant
- [ ] Classify fibres by **Tate's algorithm** (ord Δ, ord c₄, ord c₆)
- [ ] Derive mᵥ from fibre types (do not assume)
- [ ] Emit `C1_cooper_s{7,10}_partner_v3.json`; mark v2 superseded
- [ ] Cross-check v3 loci still = {1/27, −1} / {1/16, −1/4}

### Phase 3: C2 v3 (2–3 h)
- [ ] Shioda–Tate with v3 mᵥ: ρ = 2 + Σ(mᵥ−1) + rank MW
- [ ] **Compute** rank MW (v2 assumed 0 with no derivation)
- [ ] τ = 22 − ρ; intersection form; discriminant — derived, not pre-declared
- [ ] Emit `C2_cooper_s{7,10}_partner_v3.json`
- [ ] **If ρ ≠ 4 → notify Stream 3 immediately** (D-3 prior changes)

### Phase 4: Physics interpretation (4–6 h) — ⛔ BLOCKED on Phase 3
- [ ] Map Picard lattice → D-brane gauge groups
- [ ] Every physics claim carries an inline `[C] CONJECTURE` marker **in the same sentence**
- [ ] Deliverable: `briefs/STREAM2_PHYSICS_INTERPRETATION.md`
- [ ] Guardrail holds: "load-bearing physical vacuum" framing **not adopted**

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
- [ ] ⚠️ Note criterion 1 lattice prior is unsupported pending T0 decision

---

## Housekeeping

- [ ] **Rotate the GitHub token embedded in `.git/config`.** `git remote -v` prints a
      plaintext `ghp_…` PAT. Revoke it and switch to SSH or a credential helper.
