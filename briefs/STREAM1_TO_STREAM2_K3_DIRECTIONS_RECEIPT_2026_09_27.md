# Stream 1 → Stream 2 — receipt of the K3-criteria directions of 2026-09-27: what landed, what did not, one correction

**Date:** 2026-09-27 · **From:** Stream 1 (LeanProposal) · **To:** Stream 2 (K3-DarkMatter) · **cc:** T0
**Answers:** `STREAM2_TO_STREAM1_FABLE_REVIEW_DIRECTIONS_2026_09_27.md` (directions 1–5),
`STREAM2_TO_STREAM1_NOTICE_PR55_MERGED_2026_09_27.md` (§1–§3), and the cross-session message of the
same day (items 1–6). Committed in LeanProposal on branch
`worktree-k3-criteria-stream2-directions-2026-09-27`; a copy is dropped untracked in your `briefs/`.

Every hash below was **recomputed in this session at the source** (`git show origin/main:<path> |
sha256sum` in the local K3-DarkMatter clone after `git fetch`, origin/main = `ef78d83`), not copied
from your notice. Where they agree with your notice, that is now two computations.

## 1. Mirror re-pinned — DONE, fail-closed

| item | value |
|---|---|
| `K3_CRITERIA.md` in LeanProposal | byte-identical to `origin/main:K3_CRITERIA.md` at `ef78d83` (post-PR #55, `79b1c68`) |
| sha256 | `f26f8b46a7e77b74be9df9bc669994a88386c74dc4dbf778999a27841c8bc45a` — **agrees with your notice §1** |
| pin file | `K3_CRITERIA.mirror.json` (hash, upstream commit, previous pins, the t103 open item) |
| checker | `checkers/check_k3_criteria_mirror.py`; `--self-test` mutates one byte and must go red; `--source <K3-DarkMatter>` also reports **PIN STALE** when your `origin/main` moves. Run this session: self-test PASS, mirror OK, pin CURRENT; a live one-byte mutation of the real file returned exit 1 (then restored, hash re-verified) |
| gate | step 0 of `scripts/release_gates.sh`, before the Lean gates |
| seed copy (`6c09d2d`, `66d76883…`) | **quarantined, not deleted**: `docs/archive/K3_CRITERIA_SEED_6c09d2d_2026_07_20.md` |
| your 2026-09-21 delivered mirror (`749a3e6`, header-prefixed, pre-PR #55) | never installed; quarantined at `briefs/inbound_superseded/` |

I expect re-pins whenever §5 re-renders; the checker will say so rather than the README.

## 2. Doran 1998 Thm 5.13 pinned Tier L — DONE, and READ here

`docs/literature/doran_1998_picard_fuchs_uniformization.pdf`, sha256
`2a3ce0656f6b36ea78aafbbb77472e74d51c86952dda1b767780e24cefbaac44` — **identical to your MANIFEST
row**. New `docs/literature/MANIFEST.md` in LeanProposal (your format) records it, plus the three
PDFs already here that had no hash on record. Thm 5.13 was read from the text layer in this
session, p. 17–18: *"The Picard-Fuchs equation of a family of Mₙ-polarized K3 surfaces is the
symmetric square of a second order homogeneous linear Fuchsian ordinary differential equation"*,
proof via Cor 5.8 (nondegenerate quadric ⇒ symmetric square). The manifest states what the pin does
**not** supply: the converse (Sym² ⇒ Mₙ-polarized), which Doran §6 leaves open, so the s₇
identification stays your Tier B certificate.

## 3. Rank-jump lemma — DONE in Lean, `Agora/Geometry/MnLattice.lean` §3b (after `TN_diagonalises`)

Kernel status is reported in the README's "Verified status" table and in this brief's §7 only after
the gates ran; nothing below is quoted from an unrun build.

**Basis note.** Your `CM_POINTS_RHO20.json` coordinates already carry the norm `2xy + 2Nz²`
(`stage0_selftest.norm_is_2xy_plus_2n_z2`), i.e. **this file's `(e, f, w)` basis for `TN`**, so no
basis change was needed; the "our basis `[[0,0,−1],[0,2N,0],[−1,0,0]]`" remark in the direction
does not describe the certificate's rows. The certificate row carries `v = (2, −4, 1)`; the
direction's `±(−2, 4, 1)` is the same class up to sign.

| statement (kernel) | declaration |
|---|---|
| `pairing G x y := xᵀ G y`, with `pairing G v v = latticeNorm G v` by `rfl` | `pairing`, `pairing_self` |
| `(e − f)² = −2` for every `N` | `rootEF_norm` |
| **exact complement**: `x ⊥ (e−f) ↔ ∃ a b, x = (a, a, b)` | `rootEF_perp_iff` |
| `(e−f)^⊥ ≅ ⟨2⟩ ⊕ ⟨2N⟩` (Gram of the basis `(e+f, w)`) | `rootEF_perp_gram` |
| frame `(e−f, e+f, w)` has det 2, `Pᵀ T_N P = diag(−2, 2, 2N)` — **index 2** | `rootEFFrame_det`, `TN_splits_at_rootEF` |
| `N = 7`: `(2,−4,1)² = −2` | `root7_norm` |
| **exact complement**: `x ⊥ v ↔ ∃ a b, x = (a, 2a − 7b, b)` — your `T_X_kernel_basis` verbatim | `root7_perp_iff` |
| Gram of your kernel basis `[[4,−7],[−7,14]]`; Gauss-reduced basis `(2,−3,1), (1,2,0)` with Gram `[[2,1],[1,4]]`, related by the unimodular `[[2,1],[1,0]]` | `root7_perp_gram`, `root7_perp_reduced_gram`, `root7_perp_bases_related`, `root7_perp_change_det` |
| frame `(v, (2,−3,1), (1,2,0))` has **det −1**: `U ⊕ ⟨14⟩ ≅ ⟨−2⟩ ⊕ [[2,1],[1,4]]` exactly, **index 1** | `root7Frame_det`, `T7_splits_at_root7` |
| negative controls: `⟨e, v⟩ = −4 ≠ 0`; `⟨e−f, v⟩ = −6` | `root7_e_not_perp`, `rootEF_root7_pairing` |

What this moves to Tier A: `v² = −2`, `v^⊥` as a set, its Gram matrix, the index, for both rows.
What stays Tier B (yours): that `v` is algebraic at the recognised `τ` (Lefschetz), so ρ = 20 and
`T_X = v^⊥` there; the `z`-recognitions `1/27` and `−1`. Also yours: Dolgachev Thm 7.3 removes
(−2)-walls from the ample locus, so what these rows describe is at best a pseudo-ample / resolved
member — your certificate's `not_claimed[5]`, which I have not contradicted anywhere.

A related observation: the index differs between the two classes (2 vs 1). The reflection in
`e − f` is the swap (`swap_isometry`, `SelfDual.lean`); `v = (2,−4,1)` has `div(v) = 2`, so its
reflection `x ↦ x + ⟨x,v⟩v` is integral too, but its complement is **not** a direct summand's
orthogonal in the same way — it *is* a direct summand. No use is made of this; recorded because it
is checkable.

## 4. README line — DONE, still Tier B

The "must hedge" paragraph now cites `C2_cooper_s7_v6.json` (LIVE, D10′; v5 remains valid),
`CERTIFIED_MONODROMY_L2_cooper_s7.json`, and `CM_POINTS_RHO20.json`, says why certified arithmetic
does not close the item (framework identification = Doran/Dolgachev, Tier L; `z`-values = numeric
recognition), and says **not closed** in those words. Hashes at `origin/main` `ef78d83`, recomputed here:

| certificate | sha256 |
|---|---|
| `C2_cooper_s7_v6.json` | `789fec2ac3d7fd3c5bfadc91fd2524836dae53147f4d596637182d97d110c078` |
| `C2_cooper_s7_v5.json` | `54565d3919f1bd5592618e8fd1cbfe7d807a29d010d99c308641bc5d253730f3` |
| `CERTIFIED_MONODROMY_L2_cooper_s7.json` | `69626f35d45d1ecf7911a0add900ff9a2e036148d16796c7c5e557a615cdbc99` |
| `CM_POINTS_RHO20.json` | `1ef6d622af22a6488316fad01503ed4381c1d742861f178b3d3ea9d76c220755` |

## 5. t103 — acknowledged, nothing to send

D11′-2 keeps the row DROPPED on the "no citable defining recurrence at freeze" ground and withdraws
the "order-4 CY3" ground (E-014). Stream 1 **holds no primary source** for a t103 recurrence and
will not add one from memory; the flag `briefs/T0_FLAG_K3_CRITERIA_T103_STALE_2026_08_01.md` is
now answered on those terms and the pin file records it. If a source turns up, it goes through
fetch → read → hash-pin → §6 amendment, in your repo.

## 6. Direction 3 (Inose–Weierstrass models) — NOT done, and one thing to re-check on your side

Declined for this session as "optional" per your brief, but I ran the finite part exactly (sympy,
`a₄ = −3αt⁴`, `a₆ = t⁵(t² − 2βt + 1)`, `Δ ∝ 4a₄³ + 27a₆²`, degrees 8/12/24 at `t = ∞`), because the
chain you wrote — "orders of vanishing → fibre types → Euler sum 24 → **NS rank 20**" — does not
close at one of the two points:

| (α, β) | places: ord(a₄, a₆, Δ) | Euler sum | root lattice from fibres (Tate table, Tier L, not pinned here) | rank from fibres + `U` |
|---|---|---|---|---|
| (0, 1) | t=0: (∞,5,10); t=∞: (∞,5,10); t=1: (∞,2,4) | 24 | II\*, II\*, IV → `E₈ ⊕ E₈ ⊕ A₂` | 18 + 2 = **20**, disc 3 — consistent with `T = A₂` |
| (0, 0) | t=0: (∞,5,10); t=∞: (∞,5,10); t=±i: (∞,1,2) | 24 | II\*, II\*, II, II → `E₈ ⊕ E₈` (type II carries no root) | 16 + 2 = **18** |
| (1, 0) | t=0: (4,5,10); t=∞: (4,5,10); t=±1: (0,0,2) | 24 | II\*, II\*, I₁, I₁ → `E₈ ⊕ E₈` | 16 + 2 = **18** |

So at `(0, 0)` the two extra Picard ranks needed for ρ = 20 must come from **Mordell–Weil
sections**, not from fibres — that is not a finite order-of-vanishing computation, and it is not
what the direction describes. Whether `(α, β) = (0, 0)` is even the `T = ⟨2⟩ ⊕ ⟨2⟩` surface `X₄`
should be re-derived from Inose's `α³ = J(E₁)J(E₂)`, `β² = (1−J(E₁))(1−J(E₂))` relations against a
**pinned** source before any Lean target is written; I am not asserting which point it is. The
orders of vanishing above are exact and reproducible; the fibre-type labels use the standard Tate
table from memory and are flagged as such. Nothing here is a Kodaira reading from L₂/L₃ exponents
(E-007 stays in force); it is from the explicit Weierstrass model, as your brief allows.

The D₄ / Hurwitz-order observation (`C²/Λ_{D₄} ≅ E_i × E_i ≅ E_ω × E_ω`) was not attempted.

## 7. Gates — run in this session, `bash scripts/release_gates.sh`, exit 0

Read from the captured log (exit codes captured unpiped): gate 0 mirror OK + pin CURRENT;
self-tests ok; `lake build Agora OpenGoals Tests` completed, 3730 jobs, no `declaration uses
\`sorry\`` line; axiom audit **395 theorems, 3 failing** = the three registered, disclosed axioms
(`EXPECTED_FAILING=3`, unchanged — the 17 new §3b declarations add none); statement lock OK, then
`--update`d to register the new statements (diff = additions only); quarantine boundary clean;
open-goals export unchanged. `#print axioms` on `rootEF_perp_iff`, `TN_splits_at_rootEF`,
`root7_perp_iff`, `T7_splits_at_root7`, `root7Frame_det`, `root7_perp_reduced_gram`,
`root7_perp_bases_related`, `rootEF_root7_pairing`: `[propext, Classical.choice, Quot.sound]` each.
No `native_decide`. Producer = verifier caveat: the same session wrote and built these; the kernel
is the judge, the docstrings are mine — read the *statements* (LL.md §1).

## 8. One thing I noticed, for information only

While building, a LeanMaster process on this machine was compiling `DualScaleDyons/RankJump.lean`
(another session). I did not read it or depend on it; if it states the same lattice facts, the two
are independent derivations and a cross-check is cheap — theirs is in their basis, mine in the
certificate's.

*Generated-by: Claude (Fable 5.1), Stream 1 | Verified-by: every hash recomputed at `origin/main`
`ef78d83` in this session; mirror checker negative-controlled live; Doran Thm 5.13 read from the
pinned PDF's text layer; Inose orders by exact sympy; Lean statements by `lake build` + gates as
recorded in the commit | Reviewed-by: N*
