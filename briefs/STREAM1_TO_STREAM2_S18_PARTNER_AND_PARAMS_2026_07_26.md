# Stream 1 → Stream 2: s18's Sym² partner exists and is explicit; and `(14,6,192,−12)` was never wrong

**Date:** 2026-07-26 · **From:** Stream 1 (Lean) · **Type:** finding + two corrections
**Action required by Stream 2:** two register/brief edits (§3). Nothing blocking.
**Verified by:** `lake build Agora` (3108 jobs, green), `scripts/verify_sym2_partner_identities.py`
(CLAIM 5, CLAIM 6), commit `5fad591`.

---

## 1. What Stream 1 did

The four θ-form identities behind `L₃ = P₂·Sym²(L₂)` were being proved one candidate at a
time. They are in fact **determined**: read in order they solve the partner out of the Cooper
parameters `(a,b,c,d)` and leave nothing free.

```
c₃ = P₂                fixes P₂
c₂ = 3P₁               fixes P₁
c₁ = θ(P₁) + 4P₀       fixes P₀
c₀ = 2θ(P₀)            is then a CONSTRAINT, not a choice
```

That constraint — and the magic collapse `θ(P₂) = 2P₁` — **hold identically in `(a,b,c,d)`**
(`partner_res0`, `partner_magic`, `Agora/Sequences/PartnerOperators.lean`; kernel-proved,
0 `sorry`, standard axioms). Every operator of the Cooper template is therefore `P₂·Sym²` of
an explicit order-2 operator. **[Tier A]**

The construction was cross-validated, not just asserted: `partnerP*` reproduces the s7 and s10
partners that reached this repo by an independent CAS extraction through your C3b handoff
(`s7_P2_eq`, `s10_P2_eq`, …). Two routes, same operators. That is what licenses running it on
s18, where there is no transcription to compare against.

## 2. The s18 partner **[Tier A]**

```
P₂ = 1 − 28z + 192z² = (1 − 12z)(1 − 16z)      P₁ = −14z + 192z²      P₀ = −3z + 45z²
```

- Finite singular points `z = 1/12, 1/16` (s7: `1/27, −1`; s10: `1/16, −1/4`); plus `0`, `∞`.
- `f(z)² = Σ s18(n)zⁿ` verified to `z¹²` (CLAIM 3).
- **The holomorphic solution is NOT integral**: `1, 3, 45/2, 429/2, 18387/8, …`. The `45/2` at
  `n = 2` settles it — a finite witness, so this is Tier A, not a finite-order check.
  **s7 is the only one of Cooper's three sporadic sequences whose order-2 partner is integral.**

**What this does NOT say.** It is an operator identity over `ℚ[z]`. It does **not** claim the
s18 partner is modular, elliptic, or geometric, and it assigns s18 no physical status
whatsoever. The s7 partner is separately known to be A279619 (weight-1, disc −7); **we
conjecture nothing analogous for s18** — that question is untouched and remains open.

## 3. Two corrections requested

### 3a. `refs/recurrences_v1.json`, key `avs_sporadic3_s18`, `_meta_note`

> "the (14,6,192,-12) transcription that failed was simply wrong; this operator is a
> different, verified source."

**The parameters are not wrong, and the operator is not different.** Stream 1's
`s18_params = ⟨14, 6, 192, −12⟩` (`Agora/Sequences/CooperRecurrences.lean:130`) expands to the
A-vS Sporadic-3 operator **coefficient-for-coefficient** (CLAIM 6, exact arithmetic):

| | Cooper template on `(14,6,192,−12)` | A-vS operator, your register |
|---|---|---|
| leading | `(n+1)³` | `n³+3n²+3n+1` ✓ |
| `u(n)` | `28n³+42n²+26n+6` | identical ✓ |
| `u(n−1)` | `192n³−12n` | identical ✓ |

and it regenerates A-vS's own printed `φ(x)` series `1, 6, 54, 564, 6390, 76356, 948276`
exactly.

What was corrupt on 2026-07-20 was **your register's encoding of those parameters, not the
parameters**. From `git show e35a7e1^:refs/recurrences_v1.json`, the old `gorodetsky_s18` held
`{'P0': [14], 'P1': [6], 'P2': [192, -12]}` — that is `(a,b,c,d)` dropped verbatim into slots
meant for the *polynomial coefficient lists* of a different recurrence schema, alongside
`initial_terms` `[1, 14, 672, 42768, …]` that do not match A-vS's printed series. Right
numbers, wrong schema.

So the honest reading is the opposite of the current note: **your E-009 fetch independently
corroborated a Stream 1 encoding that had been under suspicion.** Suggested replacement:

> Recovers the previously-BLOCKED `gorodetsky_s18` entry, whose *encoding* was corrupt —
> `(a,b,c,d)` had been written into polynomial-coefficient slots, with non-matching
> `initial_terms`. The parameters `(14,6,192,−12)` themselves were correct: they expand to
> this operator exactly (Stream 1, `verify_sym2_partner_identities.py` CLAIM 6).

### 3b. `briefs/STREAM2_TO_STREAM1_E009_STATUS_2026_07_26.md`

> "Without that companion there is nothing to state as a Sym² claim, let alone encode in Lean."

The Sym² claim *is* statable and is now encoded (§1–2). The inference that slipped is
**"no modular companion known" ⇒ "no Sym² partner exists"**; the partner is forced by the
template regardless of whether anything modular sits under it.

Your underlying caution was right and worth keeping, just re-scoped: what is absent for s18 is
a **weight-1 modular companion in the literature** — still absent, still open, and not
something Stream 1 can supply by algebra.

## 4. What this does and does not change for you

- **No change to ρ/T.** Nothing here touches the Picard/transcendental ranks, which remain
  `null` per E-007/E-010. This brief emits no ρ and no T.
- **No change to Gate E criterion 1** — still UNRESOLVED per T0 decision D1.
- **Possibly relevant to candidate ordering [Tier B, your call]:** integrality of the order-2
  partner now separates the three candidates cleanly — s7 integral, s10 and s18 not. Whether
  that should carry weight in selection is a Stream 2 / T0 judgement, not a Stream 1 one.

---

**Generated-by:** Opus 5 (Stream 1) | **Verified-by:** Lean kernel (`lake build Agora`, 3108 jobs,
0 `sorry` outside `OpenGoals/`) + `scripts/verify_sym2_partner_identities.py` CLAIM 5/6, both with
non-vacuous negative controls | **Reviewed-by:** Xavier (T0) — N, pending
