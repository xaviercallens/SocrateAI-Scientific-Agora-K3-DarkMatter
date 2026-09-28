# AM-8 candidate: naming the C6 selector — comparison, computed exactly; decision needed

**Date:** 2026-09-28 · **From:** Stream 2 · **To:** T0 (Xavier) · **Status:** comparison record only
(`data/certificates/C6_SELECTOR_COMPARISON.json`, `checkers/check_C6_selector_comparison.py`, 13
controls). **Nothing in `K3_CRITERIA.md` has been touched.** This is the brief AM-6 requires before any
selector is adopted: "a named extremised quantity … adopted by its own T0 text, with the outputs of the
other known selectors listed beside it."

## Why this brief exists

You asked, directly, to name a ρ=20 selector and inform the other streams so they could leverage it.
Before I could write that instruction into `K3_CRITERIA.md`, two problems surfaced in my own first pass
that I want you to see rather than have me quietly resolve:

1. **D7′ (ledger item 8) already says "no minimum-|D| rule."** My first draft argued that clause was
   about cross-family ranking only, not within-family selection. Read plainly, it isn't scoped that way.
   If you want the discriminant-floor selector, it needs its own text overriding or narrowing D7′ — not
   an inference from context.
2. **My first pick was wrong on its own terms.** I initially favoured "minimal |v²|" as uniform and
   unique across families. It is uniform (proven for every N by `wall_general`/`TN_splits_at_rootEF`,
   both kernel-checked), but it is **not unique for cooper_s7**: two rows tie at the −2 floor, `D = −7`
   and `D = −28` — exactly the two W₇ fixed points the external review's clause F8 already names
   (`h(−28) + h(−7) = 2`). I broke the tie with a coordinate-dependent quantity the first time; caught
   before it went anywhere.

## The two candidates, computed exactly

`checkers/check_C6_selector_comparison.py` (13 controls) computes both from lattice-intrinsic data only
— never from `z`, never from a physical reading — and cross-checks uniqueness **on the modular curve
itself** (`CM_COMPLETENESS.json`'s `points_on_X0n_star`, a point count, not a form count) rather than
trusting `h(D)=1` alone.

| | **SEL-D — minimal `|disc T|`** | **SEL-N — minimal `|v²|`** |
|---|---|---|
| s7 pick | `v=(14,−14,−5)`, `D=−3`, `T=A₂`, at `z=∞` | **not unique** — two rows tie at `|v²|=2`: `D=−7` (`div=2`) and `D=−28` (`div=1`) |
| s7 uniqueness | global minimum over **all** levels (occurrence criterion, exact search), realized in the window, `points_on_X0n_star=1`, curve-complete | tie count 2; a stated but **not adopted** tiebreak (minimal `div(v)`) would give `D=−28` |
| s10 pick (ADVISORY) | `v=(10,−10,−3)`, `D=−4`, `T=⟨2⟩⊕⟨2⟩`, at `z=∞` | `v=(1,−1,0)`, `D=−40`, `T=⟨2⟩⊕⟨20⟩` — unique, `div=1` |
| s10 uniqueness | global minimum, curve-complete, `points_on_X0n_star=1` | unique, no tie |
| kernel status of the pick | s7 pick Tier A (`s7_z_infinity`); s10 pick Tier A (`s10_z_infinity`) — both already lifted this session | s10 pick Tier A (`s7_z_1_27`/`s10_z_1_16` cover the D=−28/−40 rows); the s7 tie's other member (`D=−7`) is also Tier A (`s7_z_minus_1`) |
| existing machinery built on this point | Moore's attractor mechanism (Paper 12, `DualScaleDyons/AttractorCharges.lean`, `discriminant_gap`/`smallest_black_hole`, already Tier A/L, pre-existing and independent of C6) singles out exactly this quantity for black-hole charge quantization | `wall_general` is the one N-uniform theorem in both Lean files; WP-GE10's explicit Inose model and Kuwata–Shioda fibration were built around the s7 `D=−28` point specifically |
| conflicts with existing text | **D7′: "no minimum-|D| rule."** Adopting SEL-D needs text resolving that, not silence. | AM-6 itself, read literally, asks for "an extremised quantity" — a selector that returns two answers for one family does not extremize uniquely without a further, separately-justified tiebreak |

Both selectors disagree with each other in both families. The third selector the external review names
(the Fricke-fixed-point count) is already established non-unique at `N ≠ 1` (audit clause F8) and isn't
recomputed here.

## What adopting either one would and would not do

Whichever is chosen: no ranking of cooper_s7 over cooper_s10 follows (each family gets its own answer);
cooper_s10 stays ADVISORY (D6′ untouched — a selected point in an advisory family's lattice does not
promote the certificate); no CM point maps to any observable (ledger item 4, untouched); and the choice
is reversible by one T0 sentence, same as every other ruling this session.

## Draft AM-8 text, one paragraph per option — none applied

**Option 1 — adopt SEL-D** (append to C6, after the selector clause AM-6 already added):
> **AM-8 (2026-09-28).** The C6 selector is minimal `|disc T|` within a register family, computed by
> the occurrence criterion and verified unique on the modular curve (`points_on_X0n_star = 1`). This
> narrows D7′'s "no minimum-|D| rule" to cross-family comparison only; within-family selection by
> discriminant is now adopted. Per family: cooper_s7 → `T = A₂` (`D=−3`, `z=∞`); cooper_s10 (ADVISORY)
> → `T = ⟨2⟩⊕⟨2⟩` (`D=−4`, `z=∞`).

**Option 2 — adopt SEL-N with the stated tiebreak** (minimal `div(v)`, i.e. the most primitive class):
> **AM-8 (2026-09-28).** The C6 selector is minimal `|v²|` within a register family, ties broken by
> minimal `div(v)`. Per family: cooper_s7 → `T = ⟨2⟩⊕⟨14⟩` (`D=−28`, `z=1/27`, `div=1`, over the tied
> `D=−7` at `div=2`); cooper_s10 (ADVISORY) → `T = ⟨2⟩⊕⟨20⟩` (`D=−40`, `z=1/16`, `div=1`, no tie).

**Option 3 — decline for v1.0.** `K3_CRITERIA.md` §7's pre-freeze checklist already allows "selector
named **or explicitly declined**." C6 stays exactly as D7′ left it: a record of candidates, no selector,
nothing to inform the streams beyond the comparison table itself.

## What the streams can already leverage regardless of which you pick

Two facts hold under **either** choice and need no further ruling:
- The **global minimality of `|D|` per level**, exact, via the occurrence criterion (SEL-D's
  machinery) — usable by any stream wanting the smallest-discriminant CM point of a family, whatever
  it ends up being called.
- The **`|v²| ≥ −2` floor and its unique-at-`N=10`/tied-at-`N=7` structure** — usable by anyone building
  on the W_N-fixed-point class specifically (as WP-GE10 already does for the `D=−28` point).

Both are already Tier A/exact and sent to the streams below, without naming either one "the" selector.

*Generated-by: Claude (Sonnet 5), Stream 2 | Verified-by: `checkers/check_C6_selector_comparison.py`,
`checkers/test_C6_selector_comparison_controls.py` (13/13) | Reviewed-by: N*
