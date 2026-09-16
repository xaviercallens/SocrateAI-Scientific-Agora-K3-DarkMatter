# Order-3 sieve survivors — analytic check (MUM exponents + symmetric square), 2026-09-16

**EXPLORATORY SANDBOX artifact** (S3 `CLAUDE.md` rule 7). Not citable in Streams 1–3. No
G1-2/G1-3/G1-4 gate was run; nothing promoted to `candidate_pool.yaml`.

**Why:** the sieve labels a sequence "K3-type" from ODE order 3 alone
(`autoresearch_v2_phase_a_scan.classify`). That is necessary, not sufficient. This check adds
two mechanical conditions, both exact over ℚ(z) (sympy):
1. **MUM at z = 0**: local exponents 0, 0, 0 (maximal unipotent monodromy).
2. **Symmetric square**: for L₃ = ∂³ + p∂² + q∂ + r, set a = p/3, b = (q − 2a² − a′)/4 and
   test r = 4ab + 2b′ exactly (this is Sym²(∂² + a∂ + b) expanded).

Script `scripts/r2_a112029_analytic_check_2026_09_16.py` → `data/autoresearch_v2/a112029_analytic_check_2026_09_16.json`
(persisted before print). The operator is the minimal-order ODE found by the unmodified
classifier routines, re-validated exactly on held-out terms (n ≤ 160). The minimal
annihilating operator is unique up to a left factor in ℚ(z), so its exponents do not depend
on the search.

**Controls:** A005259 (Apéry ζ(3)) and A005260 (cooper_s10) give MUM and exactly Sym² (residual
0). The two failures below show the test can also fail, so it discriminates in both directions.

## Results

| sequence | ODE | exponents at 0 | Sym² | verdict |
|---|---|---|---|---|
| A005259 (control) | 3,4 | 0,0,0 | yes | control PASS |
| A005260 (control) | 3,4 | 0,0,0 | yes | control PASS |
| **A112029** Σ C(n+k,k)² | 3,5 | **−1/2, 0, 0** | **no** | **order-3 false positive: not MUM, not Sym²** |
| **T(0,1,1)** Σ C(n+k,k)C(2k,k) (not in OEIS; LR-3 "new") | 3,6 | **0, 0, 1** | **no** | **order-3 false positive: not MUM, not Sym²** |
| A079727 Σ C(2k,k)³ (T0 HOLD) | 3,4 | 0,0,0 | yes | **partial sum of a hypergeometric family** (below) |
| A036917 Σ C(2k,k)²C(2n−2k,n−k)² | 3,4 | 0,0,0 | yes | MUM + Sym²; OEIS g.f. is (4/π²)K(4√x)², so expected |
| **A274789** T(1,1,2) | 3,8 | 0,0,0 | yes | **passes both; the only survivor still unexplained** |

Other facts from the JSON:
- A112029: the OEIS recurrence (Kotesovec 2012, live fetch) holds for n = 2…160. Singular
  point z = 16/25 has integer exponents 0, 1, 3 (consistent with an apparent singularity from
  the recurrence's (21n−13) factor).
- A274789: singular points 0, ±1, 33 ± 8√17. z = 1 also has exponents 0,0,0; z = −1 has 0,2,4.

## Answer to the T0 HOLD question on A079727 (2026-09-16)

**Yes, it is a partial sum of a known hypergeometric family.** From first principles:
C(2k+2,k+1)/C(2k,k) = 4(k+½)/(k+1), so c_k = C(2k,k)³ has term ratio 64((k+½)/(k+1))³,
i.e. Σ c_k z^k = ₃F₂(½,½,½; 1,1; 64z). A079727(n) = Σ_{k≤n} c_k (checked exactly, n < 120), so its
g.f. is ₃F₂(½,½,½; 1,1; 64z)/(1−z). The extra singular point z = 1 (exponents −1, 0, 1) is that
1/(1−z) factor. On T0's own criterion this is not new geometry; the ruling stays T0's.

## Corrections to earlier sandbox records
- `LR3_EXTENDED_SIEVE_RESULTS_2026_09_16.md` lists T(0,1,1) as a new order-3/K3-type survivor with a
  Weil-bound pass. Under this check **it is not MUM and not a symmetric square**. A weight-3
  Weil-bound pass does not rescue that.
- `R2_OVERNIGHT_SWEEP_RESULTS_2026_09_16.md` names A112029 as the lead. **It is an order-3 false
  positive.** The remaining unexplained survivor across both sieves is **A274789**.

## Engineering recommendation (not implemented)
Add the MUM + Sym² check to the sieve's classification step, so ODE order 3 is no longer labeled
"K3-type" on its own.

---
*Generated-by: Claude (Opus 5), sandboxed | Verified-by: exact ℚ(z) arithmetic; 2 positive controls,
2 discriminating failures; OEIS recurrence re-checked to n = 160 | Reviewed-by: T0 pending*
