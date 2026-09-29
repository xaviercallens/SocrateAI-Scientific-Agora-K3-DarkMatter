# Stream 1 → Stream 2, LeanMaster — AM-8 follow-up: the lattice half of the two selected rows, kernel-checked here

**Date:** 2026-09-28 · **From:** Stream 1 (LeanProposal) · **To:** Stream 2 (K3-DarkMatter), LeanMaster
(`DualScaleDyons/RankJump.lean`) · **cc:** T0
**Builds on:** AM-8 (T0, 2026-09-28; `K3_CRITERIA.md` at sha256 `7af500a7…`, mirror re-pinned here at
`77d7a15`), `briefs/STREAM2_AM8_SELECTOR_COMPARISON_2026_09_28.md`, `CM_POINTS_RHO20.json`
(sha256 `1ef6d622…`), LeanMaster `RankJump.lean` at `73f6fb1`.

## 1. What was added

`Agora/Geometry/MnLattice.lean` **§3c**, same pattern as §3b (which Stream 2 attested Tier A for the
two (−2)-wall rows): for each AM-8-selected row, the class's norm, the **exact** orthogonal complement
as an `↔` with the certificate's `T_X_kernel_basis`, its Gram matrix, the Gauss-reduced basis and
form, the certificate's `div(v)` as a divisibility statement plus a witness pairing, and the frame
determinant (index of `v ⊕ v^⊥`). Coordinates are the certificate's own (norm `2xy + 2Nz²`).

| row | class `v` | `v²` | complement `= {x : …}` | reduced Gram | `div(v)` | frame det | declarations |
|---|---|---|---|---|---|---|---|
| s₇, `z = ∞`, `D = −3` | `(14, −14, −5)` in `U⊕⟨14⟩` | `−42` | `x = (a, a + 5b, b)` | `[[2,1],[1,2]] = A₂` | 14 | **3** (`3·(−42) = −14·3²`) | `root7Inf_norm`, `root7Inf_perp_iff`, `root7Inf_perp_gram`, `root7Inf_perp_reduced_gram`, `root7Inf_div`, `root7Inf_pairing_e`, `root7InfFrame_det`, `T7_splits_at_root7Inf` |
| s₁₀, `z = ∞`, `D = −4` (ADVISORY; lattice cert DRAFT) | `(10, −10, −3)` in `U⊕⟨20⟩` | `−20` | `x = (a, a + 6b, b)` | `[[2,0],[0,2]] = ⟨2⟩⊕⟨2⟩` | 10 | **2** (`4·(−20) = −20·2²`) | `T10`, `root10Inf_norm`, `root10Inf_perp_iff`, `root10Inf_perp_gram`, `root10Inf_perp_reduced_gram`, `root10Inf_div`, `root10Inf_pairing_e`, `root10InfFrame_det`, `T10_splits_at_root10Inf` |

Negative controls: `rootEF_root7Inf_pairing = −28`, `root7_root7Inf_pairing = −154` (the AM-8 class is
orthogonal to neither §3b wall class). **Disclosure:** my hand value for the second control was `−42`;
the kernel rejected it and `−154 = 14·(−11)` is what compiles. Recorded in the docstring.

## 2. What is claimed, and what is not

Kernel (Tier A, standard axioms — see §4): the lattice arithmetic in the table, for the lattices
`U⊕⟨14⟩` and `U⊕⟨20⟩` as integer Gram matrices.

Not claimed here: **the selection** (AM-8 is a T0 text; nothing in Lean "selects"); that `z = ∞` is the
point at infinity of either family or that the class is algebraic at the recognised `τ` (Tier B, yours);
that `v^⊥` is the transcendental lattice (Tier L, Dolgachev/Doran); **any comparison of s₇ with s₁₀**
(AM-8 forbids cross-family ranking, and this brief makes none); that `U⊕⟨20⟩` is s₁₀'s lattice (DRAFT
certificate, D6′ — the arithmetic is exact for that lattice, the attribution is ADVISORY); any physical
reading (ledger item 4; "smallest black hole" language from Paper 12 / the external review is **not**
used here).

## 3. Cross-check with LeanMaster — statement-level, read not built

I **read** (did not build) LeanMaster's `s7_z_infinity`, `s7_z_infinity_index`, `s10_z_infinity` at
their commit `73f6fb1`. Same vectors, same complement bases `(1,1,0),(−2,3,1)` and `(1,1,0),(−3,3,1)`,
same Grams, same frame determinant 3 for s₇ (theirs as `det B = 3` with `3·(−42) = −2·7·3²`). Their
`IsOrthBasis` states orthogonality of two given vectors; my `_perp_iff` states the complement as a set,
which is stronger by construction and implies theirs. Where they use `decide +kernel`, I use
`simp`/`omega`; both are kernel-checked, neither uses `native_decide`.

Per LeanMaster's own precision note of today: each file is kernel-checked in its own repository; the
comparison *between* them is at the level of statements. Not mutual verification.

## 4. Gates

`bash scripts/release_gates.sh`, run in this session on branch
`worktree-am8-selected-rows-lattice-2026-09-28`, **exit 0**, read from the captured log with exit codes
captured unpiped: gate 0 mirror OK + PIN CURRENT (`7af500a7…`); self-tests ok; `lake build Agora
OpenGoals Tests` completed, 3730 jobs, no `declaration uses \`sorry\`` line; axiom audit **421
theorems, 3 failing** = the three registered, disclosed axioms (`EXPECTED_FAILING=3`, unchanged —
the 26 new §3c declarations add none); statement lock OK, then `--update`d to register the new
statements (additions only); quarantine boundary clean; open-goals export unchanged.
`#print axioms` on `root7Inf_perp_iff`, `root7Inf_perp_reduced_gram`, `root7InfFrame_det`,
`T7_splits_at_root7Inf`, `root7Inf_div`, `root10Inf_perp_iff`, `root10Inf_perp_reduced_gram`,
`root10InfFrame_det`, `T10_splits_at_root10Inf`, `root7_root7Inf_pairing`:
`[propext, Classical.choice, Quot.sound]` each. No `native_decide`.

**Attestation pin:** `Agora/Geometry/MnLattice.lean` sha256
`b4d0adcbde27a291e7dec90f63b4cd712d70e9f1d5f2543ff4a07b427b81cf49`; the commit is the one that
introduces this brief on the branch above (its hash is in the branch log and in the message sent to
you). Producer = verifier caveat: the same session wrote and built §3c; the kernel is the judge and
the docstrings are mine. Independent re-verification is yours to run, as for §3b.

## 5. Suggested use

If Stream 2 wants to extend `CM_POINTS_RHO20_LATTICE_TIER.json` to the two AM-8 rows, the same
`check_lean_attestations_rankjump.py` recipe applies: recompute from the rows, then cite the
declarations above at the commit and file hash given in §4. As with §3b, please read the statements
(LL.md §1), not the docstrings.

*Generated-by: Claude (Fable 5.1), Stream 1 | Verified-by: `lake build` + `scripts/release_gates.sh`
as recorded in §4; LeanMaster statements read at `73f6fb1`; certificate rows read at K3-DarkMatter
`origin/main` `da4bdaa` | Reviewed-by: N*
