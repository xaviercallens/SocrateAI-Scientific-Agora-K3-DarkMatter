# Stream 3 → Stream 2 — activation report, 2026-09-29 (W5 of `STREAM3_ACTIVATION_2026_09_29.md`)

**From:** Stream 3 (Home), executed in session on T0's instruction ("continue and execute stream 3 dark
matter home on the K3 selected", 2026-09-29). **Repo:** `DarkMatterK3-Home.github.io` (the Home checkout),
branch `stream3/activation-2026-09-29`, PR to its `main` open; commits below are on that branch.

## Commit hashes (W1, W2, W4)

| item | Home commit | content |
|---|---|---|
| W1 | `1822c18` | four Stream 2 briefs filed untouched; TODO inbox section |
| W2 | `18cd0b7` | `K3_CRITERIA.md` re-pinned; 12 certificates mirrored; manifest generated from files |
| W4 | `75257f0` | E1 checker + certificate + tests; E2 pre-registration DRAFT |

**Recomputed `K3_CRITERIA.md` hash at the re-pin:**
`bcafe8025d6752d11624d72d0e548ab6f1dc7924bfd5b3b4dbae61fdfd829643` — equals `git show 2894e78:K3_CRITERIA.md`
on K3-DarkMatter `main` (PR #72 merged). All 13 artifacts in the activation table were verified to exist at
that commit with the listed hashes before anything was executed (standing rule 4).

## E1 — result line and negative-control line, side by side

```
PASS(N) for N in 13,89,233            (tol 1e-9; J = 1; lam in {0.5, 1, 3}; self-dual point lam = 2J)
  PASS(N=13)  max spectral gap 9.0e-15, intertwiner 2.9e-14, IPR gap 1.1e-14, min level gap 1.62e-02
  PASS(N=89)  max spectral gap 3.9e-14, intertwiner 1.0e-12, IPR gap 7.1e-13, min level gap 6.49e-05
  PASS(N=233) max spectral gap 2.3e-13, intertwiner 7.8e-12, IPR gap 1.7e-11, min level gap 7.15e-06
controls (run first, required to fail):  N1 random matched-rms potential breaks the spectral duality — True at every N
                                         N2 same potential at lam = 2J breaks IPR_x = IPR_k        — True at every N
                                         N3 gcd(p, N) != 1 is refused (transform not unitary)       — True at every N
```

What is checked: on an N-site ring with gcd(p,N)=1, `U† H(J,λ) U = H(λ/2, 2J)` with
`U[n,k] = e^{2πi p n k/N}/√N` (explicit intertwiner), hence equal spectra and the scaled form
`spec H(J, 4J²/λ) = (2J/λ)·spec H(J,λ)`; at λ = 2J the map is an automorphism, so every non-degenerate
eigenvector has IPR_x = IPR_k. Verified in floating point at the stated tolerance: `PASS(N)`, not a proof,
not a measurement. The checker refuses if the spectrum is degenerate at tol. Certificate:
`checkers/certificates/E1_aubry_andre_selfduality.json` (not_claimed block included).

## E2 — drafted, not pinned

`briefs/PREDICTION_V2_AMENDMENT_E2_SIT_NOISE_DUALITY_DRAFT_2026_09_29.md`: statement, inputs (`RESERVED`),
arms V/P/0, decision rule with kill rule, prior-knowledge disclosure (2016 reflection, 2022 dual Shapiro
steps — known by description only, not fetched), freeze procedure. No dataset named from memory, none
fetched; `PREDICTION.md` untouched; nothing in `pipeline/` or `data/` changed (Home rule 1).

## Guardrail, restated

The K3 surface is the mathematical shadow of the duality, not the target. Nothing above is evidence for
cooper_s7, cooper_s10, or any Tier A/B certificate. No sentence here links σ = i or σ = (1+i)/2 to
⟨2⟩⊕⟨2⟩; any future one is Tier C and carries its marker.

## Needs a ruling (T0), as briefs not questions

1. **Merge the Home PR** (`stream3/activation-2026-09-29` → `main`); Stream 3 did not push to `main`.
2. **Pin E2:** fill the seven `RESERVED` fields, fetch and hash-pin the two prior-knowledge items, tag
   `prereg/E2-sit-noise-duality-<date>`. Only then may `scripts/fetch_data.py` touch an E2 dataset.
3. E3/E4 stay designed appendices until E2 is pinned (E1 exists).

Nothing else is asked of Stream 2.

*Generated-by: Claude (Fable 5.1), Stream 3 activation | Verified-by: the E1 controls and tests, the mirror
drift test (7/7), `refresh_stream2_mirror_manifest.py --check`, `check_tier_language.py` (0 violations) —
all on the Home branch | Reviewed-by: N*
