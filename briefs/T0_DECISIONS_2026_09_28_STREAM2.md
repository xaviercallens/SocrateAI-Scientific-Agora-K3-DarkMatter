# T0 decisions — 2026-09-28 (Stream 2) — D13′: the C6 selector

**Ruled by:** T0 (Xavier Callens), via `AskUserQuestion`, 2026-09-28. **Recorded by:** Claude
(Sonnet 5), Stream 2. **Question asked and the exact selection:**

> Which ρ=20 selector should Stream 2 adopt as AM-8 in `K3_CRITERIA.md`?
> Options: SEL-D (minimal `|disc T|`) · SEL-N (minimal `|v²|`, tiebreak) · decline for v1.0 · other.
> **Selected: "SEL-D: minimal `|disc T|`"**, with the preview text shown (both families' picks,
> the "unique on curve" fact, the D7′-conflict flag, and the Paper 12 attractor-mechanism note) —
> all confirmed correct by recomputation before and after the choice.

This is the "named extremised quantity … adopted by its own T0 text" AM-6 required, and satisfies
D7′'s "widening [item 8's clauses] needs its own T0 text" for the "no minimum-|D| rule" clause
specifically.

## What was applied

| # | Item | Applied |
|---|---|---|
| D13′-1 | **AM-8 adopted**: C6 selector = minimal `\|disc T\|` per family | `K3_CRITERIA.md` C6 clause, §6 version row `v0.1e`, §7 checklist ticked |
| D13′-2 | Narrow D7′'s "no minimum-\|D\| rule" to cross-family comparison only | `K3_CRITERIA.md` C6 AM-8 text; `CLAUDE.md` ledger item 9 (new) |
| D13′-3 | Verify the adopted prose against fresh recomputation, not trust | `checkers/check_C6_selector_adopted.py` (5 controls) → `data/certificates/C6_SELECTED_CANDIDATE.json` |
| D13′-4 | Inform Stream 1, Stream 3, LeanMaster with the concrete per-family answer | this session, cross-session messages + repo notice files |

**The two selected candidates, verified unique on the modular curve (`CM_COMPLETENESS.json`
`points_on_X0n_star = 1`, a point count, not `h(D)=1`, a form count):**

- **cooper_s7 → `T = A₂` (reduced form `(1,1,1)`), `D = −3`, at `z = ∞`.**
- **cooper_s10 (ADVISORY, D6′ untouched) → `T = ⟨2⟩⊕⟨2⟩` (reduced form `(1,0,1)`), `D = −4`, at
  `z = ∞`.**

## What this ruling does not do

No ranking of cooper_s7 over cooper_s10 (each family's answer stands on its own); no promotion of
cooper_s10's lattice certificate (still DRAFT, D6′); no physical reading — the selected point maps
to no observable (ledger item 4, untouched); not presented as corroboration of anything; gate T3
still not adopted; the rejected alternative (SEL-N, minimal `|v²|`) is not erased — it stays on
record in `C6_SELECTOR_COMPARISON.json` as the comparison AM-6 requires, including the fact that it
is **not unique for cooper_s7** (two rows tie at the `−2` floor, `D=−7` and `D=−28`), which is why it
was not chosen. Reversible by one T0 sentence, as every ruling this session has been.

*Recorded by Claude (Sonnet 5), Stream 2, 2026-09-28. Reviewed-by: T0 Y (the ruling itself), record N.*
