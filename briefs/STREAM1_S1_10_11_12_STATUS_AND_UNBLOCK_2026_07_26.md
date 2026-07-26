# Stream 1 → Streams 2 & 3 (+ T0): S1-10/11/12 landed — status, consumed-artifact changes, unblock directions

**Date:** 2026-07-26 · **From:** Stream 1 (Lean) · **Authority:** T0-directed ("inform stream 2
and stream 3 and deep think and provide directions to unblock")
**Companion:** `briefs/DEEPTHINK_REVIEW_REQUEST_S1_10_12_2026_07_26.md` (the Deep Think ask)
**Commits:** `2891638` (S1-10) · `7fde974` (S1-11) · `ffa1361` (S1-12), all on `main`, pushed.

---

## 1. What landed today, one line each

| WP | Result | Tier |
|---|---|---|
| S1-10 | The Cooper-template Sym² partner is **generic**: the four θ-form identities *determine* `L₂` from `(a,b,c,d)` and the leftover constraint holds identically — s7/s10/s18 are corollaries. s18's partner is explicit: `P₂=(1−12z)(1−16z)`, `P₁=−14z+192z²`, `P₀=−3z+45z²`. | A |
| S1-10 | `s18_params (14,6,192,−12)` **vindicated** against Almkvist–van Straten — the 2026-07-20 corruption was Stream 2's register *encoding*, not the values. | A |
| S1-11 | s10/s18 partner series **NOT integral** — complete proofs, witnesses `17/2`, `45/2` at n=2. s7 partner integrality: **PASS(7) only**, general case = named open goal. Two vacuous S1-03 "integrality" theorems disclosed (F6, README). | A / PASS(7) |
| S1-12 | **Dyadic baseline kernel-proved** (`sqrtSeq_dyadic`): the formal √ of *any* integer series has only 2-power denominators. Deep Think's Q6 mechanism, recomputed then formalised. s7's integrality question **reduces to purely 2-adic**, modulo the bridge open goal. | A (generic) |

The candidate-separation picture, stated with its honest asymmetry: **s10/s18 partners are
non-integral [A, complete]; that behaviour is the generic baseline [A, via `sqrtSeq_dyadic`];
s7 avoiding it is the anomaly and is verified PASS(7)/PASS(81-CAS), not proved.**

## 2. FOR STREAM 2 — three actions, one flag

**2a. (pending from S1-10 brief) Two register corrections** — see
`briefs/STREAM1_TO_STREAM2_S18_PARTNER_AND_PARAMS_2026_07_26.md` in your repo:
`avs_sporadic3_s18._meta_note` ("transcription was simply wrong" → it was your schema, values
were right) and the E-009 status brief's "nothing to state as a Sym² claim" (the Sym² claim is
kernel-proved; what's absent is a *modular* companion). Suggested wording is in the brief.

**2b. `open_goals.json` semantics changed** (you are its consumer per CLAUDE.md):
- Now **4 goals** (was 2): `open_goal_partner_integral_s7` (open), `open_goal_partner_eq_sqrt_s7`
  (open), the two recurrence goals (closed).
- `status` is now derived from the **proof body** (bare `sorry` token, comments stripped), not
  from docstring prose — a docstring can no longer misreport a goal as closed. Two prior
  misclassification bugs were found and fixed on the way; treat any cached copy as stale.
- `context` is now a per-file WP map (`S1-02/S1-03` vs `S1-11/S1-12`), no longer hardcoded.

**Flag:** your `criteria-checkers` skill tells operators to run
`python scripts/render_status_table.py` to merge our `open_goals.json` — **that script does not
exist in your repo** (verified by search, 2026-07-26). This is the referenced-but-absent-artifact
pattern of T0 D3 (4th instance). Per the D3 standing rule, either write it or remove the
reference before anyone executes that skill.

**2c. Cheap, high-value check you can do with what you already fetched:** grep O'Brien 2016
(`docs/literature/obrien_2016_massey_thesis.txt`, hash-pinned) for whether Theorem 6.1 (or its
surrounding text) **proves integrality** of the `c_n` (A279619), or only the g.f. identity. If
the thesis proves it, the mathematical (not Lean) side of the s7 anomaly is sourced and
`open_goal_partner_integral_s7`'s route note upgrades from [B] to sourced. 15 minutes.

**Also closed for you:** stop hunting geometric realisations of the s10/s18 order-2 partners —
Deep Think's Q1/Q4 answer is NO SOURCE FOUND and the non-integrality theorems explain why the
literature ignores them. They are formal Sym² factors over `ℚ[z]`; the geometry lives at L₃.

## 3. FOR STREAM 3 — no action; one explicit warning

**Nothing in S1-10/11/12 touches your pipeline, your D-3 batch, or Gate E.**

- **ρ/T are still `null`. Criterion 1 is still UNRESOLVED per T0 D1.** Unchanged.
- Deep Think's response contains the sentence "the identification of ρ=19/T=3 is theoretically
  sound". **That is not an authorization to re-score criterion 1** — Deep Think itself
  concludes UNRESOLVED is the only safe scoring, S-B 1985 remains unfetched, and the operative
  instruction remains `briefs/STREAM2_TO_STREAM3_GATE_E_CRITERION1_2026_07_26.md`. After E-010,
  any brief that *could* be misread as a re-score authorization gets this explicit disclaimer.
- This brief emits no ρ and no T.

## 4. FOR T0 (Xavier) — the unblock queue, in priority order

| # | Decision | Blocks | Recommendation |
|---|---|---|---|
| 1 | **WP-B1 sign-off** (two documented deviations, `STREAM1_WP_B1_RESULTS.md`) | closing Stream 1's last gate | Unchanged since 2026-07-25; still the only item wholly on you. |
| 2 | **Classify the 2 open goals** `blocked-on-mathlib` or `active` | whether Stream 1 grinds or parks | **Recommend `blocked-on-mathlib` for both.** The bridge needs operator→solution transport (no holonomic/`PowerSeries.sqrt` API at the pin); s7 2-adic integrality needs modular-forms machinery. Both informal arguments are standard; the gap is machinery, and the pin is frozen (rule 1). Deep Think's review (companion brief) is the cheap second opinion before you rule. |
| 3 | **Authorize the Deep Think review request** (companion brief) | two-model bar on S1-10/11/12 | Same bar as D2/WZ closure. Recommend yes — S1-10/12 are now load-bearing for candidate ordering. |
| 4 | Stream 2 register corrections (2a) | s18 record accuracy | Endorse; Stream 2 applies. |

**What is NOT blocked:** Stream 1 has no active proof work left that isn't gated on #2/#3.
If both goals are classified blocked-on-mathlib, Stream 1 is **parked clean**: 0 `sorry`
outside `OpenGoals/`, all builds green (3117 jobs), every remaining question either external
(literature), machinery (Mathlib pin), or yours (#1).

## 5. Unblock map (who unblocks whom)

```
Xavier #1 (WP-B1 sign-off)     → closes Stream 1's last open gate
Xavier #2 (goal classification)→ parks or re-activates Stream 1 grinding
Xavier #3 + Deep Think review  → two-model bar on S1-10/11/12 (candidate-ordering evidence)
Stream 2 (2c O'Brien grep)     → sources the s7-anomaly mechanism ([B] → sourced)
Stream 2 (Stienstra–Beukers or Cooper 2012 access, if ever) → ρ/T citation path (dormant)
Nobody                         → Stream 3's D-3/Gate E path (already unblocked; runs per D1)
```

---

**Generated-by:** Fable 5 (Stream 1, T1, executing T0 direction) | **Verified-by:** Lean kernel
(`lake build Agora Tests OpenGoals`, 3117 jobs, 0 `sorry` outside `OpenGoals/`); CAS sweeps with
live negative controls (`verify_sym2_partner_identities.py` CLAIMs 5–6, `q6_check.py`);
`render_status_table.py` absence verified by repo search 2026-07-26 | **Reviewed-by:** Xavier
(T0) — direction given in-session; contents pending his countermand as always
