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

### Phase 1: Provenance gate (1–2 h)
- [ ] `mkdir docs/literature/`; create `refs/literature_provenance.txt`
- [ ] **O'Brien (2016) MSc thesis, Massey Univ.** — Thm 6.1, the c₇/A279619 recurrence *(new, from E-007)*
- [ ] **Chan, Cooper & Sica (2010)** "Congruences satisfied by Apéry-like numbers" — Conj 5.4 *(new)*
- [ ] Fetch Gorodetsky (arXiv:2102.11839) — *also unblocks the corrupt s18 recurrence*
- [ ] Fetch Almkvist–van Straten (arXiv:2103.08651); Zagier 2009; Cooper 2012 (Ramanujan J. 29)
- [ ] SHA256 + pin hashes; cross-check (a,b,c,d) vs PDFs and OEIS
- [ ] Write `checkers/check_provenance_hygiene.py` — scope honestly in the docstring
      (hashes + document identity + Cooper parameter sets; **not** 15 sequences, no OEIS lookup)

### Phase 2: ⚠️ REVISED — do NOT run Tate's algorithm on raw L₂ (8–14 h)
> The earlier "Weierstrass + Tate on L₂" plan is **retracted** — it repeated the same
> category error one level up. Tate's algorithm needs a genuine unipotent PF operator.

Pick **one** route, do not mix:
- **Route α (recommended) — derive geometry from L₃** (fully unipotent, {0,0,0})
  - [ ] Confirm L₃ unipotency at each singular locus (log solutions)
  - [ ] Derive invariants from L₃'s monodromy representation
- **Route β — untwist L₂ by gauge transformation**
  - [ ] Clear the ½-exponents (e.g. `y ↦ P₂^{1/4}·y`) to reach {0,0}
  - [ ] Verify the untwisted Wronskian is rational (currently `C/(z√P₂)`, irrational)
  - [ ] Only then is fibre classification meaningful
- [ ] Emit `C1_cooper_s{7,10}_v3.json` **naming which operator the geometry came from**
- [ ] Reframe s7's target as **X₀(7)**; re-examine whether ρ is even the right invariant

### Phase 3: C2 v3 (2–3 h) — only after Phase 2 yields a genuine PF operator
- [ ] Shioda–Tate with **derived** mᵥ: ρ = 2 + Σ(mᵥ−1) + rank MW
- [ ] **Compute** rank MW (v2 assumed 0 with no derivation)
- [ ] τ = 22 − ρ; intersection form; discriminant — derived, not pre-declared
- [ ] Emit `C2_cooper_s{7,10}_v3.json`
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
