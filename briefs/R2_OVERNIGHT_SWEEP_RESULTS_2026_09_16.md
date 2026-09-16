# R2 Widened Sieve — Results (2026-09-16)

**EXPLORATORY SANDBOX artifact** — AutoEvolve R2 Hypothesis Foundry track (S3 `CLAUDE.md`
rule 7). Not citable in Streams 1–3 or for any Tier A/B/C claim. Nothing promoted to
`candidate_pool.yaml`; no HUMAN/T0 gate has reviewed this.

## What ran
`scripts/r2_overnight_sweep_2026_09_16.py` (commit `c2e34f4`), importing the unmodified
`autoresearch_v2_phase_a_scan.py` classifier. Wall time about 11 min on CPU (6 workers). A T4
was requested, but this computation is exact integer arithmetic and does not use a GPU.

- **Controls** (`controls.json`): A005259 and T103 give order 3, and S(1,2) gives order 2, in
  both windows. All 6 PASS; a failure would have aborted the sweep.
- **Stage 1** (ODE ρ≤4, δ≤8, n≤110): 114 new cases — 3-factor (A,B,C) ∈ [0,4]³ outside LR-3's
  grid, plus 4-factor Σ C(n,k)^A C(n+k,k)^B C(2k,k)^C C(2n−2k,n−k)^D, (A,B,C) ∈ [0,2]³, D ∈ {1,2}.
- **Stage 2** (ODE ρ≤6, δ≤16, n≤200): all 187 cases with no ODE in a smaller window, including
  LR-3's own. **160 still have no ODE in the window** ("not found", not a negative); 27 have
  order 4–6; **0 have order 3**.

## Order-3 survivors (OEIS identified by live `oeis.org` JSON query, not from memory)

| case | ODE (order, degree), held-out | OEIS | already in this program? |
|---|---|---|---|
| 4f (2,0,1,1) | (3,4), 72 | **A002895** Domb numbers | yes — known anchor (positive re-derivation) |
| 3f (4,0,0) = Σ C(n,k)⁴ | (3,4), 72 | **A005260** | yes — cooper_s10 |
| 4f (0,0,2,2) = Σ C(2k,k)² C(2n−2k,n−k)² | (3,4), 72 | **A036917**, OEIS: "g.f. (4/π²)·EllipticK(4x^{1/2})²" | **not referenced in S2** |
| 3f (0,2,0) = Σ C(n+k,k)² | (3,5), 67 | **A112029** | **not referenced in S2** |

Observations (engineering, not geometry):
- **No sequence missing from OEIS** turned up; every order-3 survivor is a known sequence.
- A036917's own OEIS title writes its generating function as the **square of an elliptic
  integral**, so order 3 is expected by construction (a symmetric square of an order-2
  object). That makes it a check on the classifier, not a new K3 candidate, unless a review
  shows otherwise.
- A112029 is the only survivor with no known reason for order 3 in this program's records. It
  is the natural next item for the same analytic check T0 set for A079727 (partial sum /
  twist of a known family?) before any G1-2/G1-3/G1-4 run.

## Not done
Weil-bound screen (G1-2), mirror integrality (G1-3), monodromy (G1-4), and physics gates — none
were run. No ranking: "best" here means "not already in the program", not "better K3".

---
*Generated-by: Claude (Opus 5), sandboxed | Verified-by: exact held-out validation; 6/6
known-answer controls; OEIS by live query | Reviewed-by: T0 pending*
