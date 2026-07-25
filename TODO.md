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

### Phase 2: ⚠️ REVISED TWICE — Routes α and β both REFUTED (E-008)
> Neither Deep Think's Route A (use L₃) nor any gauge transform works. Both tested and closed.

- [x] Test Route A premise → **REFUTED**: L₃ exponents are **{0, ½, 1}**, not unipotent
      (`scripts/compute_L3_monodromy.py`; Sym² of {0,½} = {0,½,1} — cross term keeps ½)
- [x] Route β (gauge transform) → **REFUTED**: exponent *differences* are gauge-invariant,
      so a difference of ½ cannot be gauged away (incl. fractional twists like P₂^{1/4})
- [x] Emit `C1_L3_cooper_s{7,10}.json` with `picard_rank: null` (deliberate — no fabrication)

**Route γ — ramified Hauptmodul pullback (only surviving path):**
- [ ] Fetch level-7 Hauptmodul **A279618** (A279619 = expansion of **A002652** in its powers)
- [ ] Construct pullback `z ↦ t(z)`; push the operator through it
- [ ] **Verify** integral exponents + rational Wronskian — *test, do not assume*
- [ ] Only then classify fibres; emit `C1_cooper_s{7,10}_v3.json` naming operator + coordinate


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
- [x] **M1 mechanism memo delivered** → `briefs/STREAM2_M1_MECHANISM_MEMO_2026_07_26.md`
      **Verdict: conditional negative.** Walls 1–2 are posed in retracted quantities
      (ρ=4/T=18, Type II — E-007) so no route is currently nameable; Wall 3 routed by
      renunciation (no dark-energy claims). Unblock = Route γ delivering C1v3/C2v3.
- [ ] ⛔ **STOP-POINT: T0 review of M1** — M2 (two-model derivation) must NOT start before this
- [ ] Request Stream 3 mirror WP-R6/R7 + `check_tier_language.py` + `pipeline/siblings.py`
      into this repo (14/16 directive-referenced artifacts absent here)
- [ ] M2–M4: blocked on M1 acceptance AND Route γ

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
