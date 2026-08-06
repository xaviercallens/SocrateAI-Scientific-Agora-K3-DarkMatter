# K3 Selection Report

## Stream 2 AutoEvolve — Implementation & Run Notes

The AutoEvolve K3 selection pipeline has been implemented in `scripts/auto_evolve_k3_selection.py` per `briefs/STREAM2_AUTOEVOLVE_HAIKU_PLAN.md`.

### Pipeline stages

- **AE-0** — `scripts/ae_preflight.py`: environment, import, frozen-pool (INFO if missing), refs-integrity checks.
- **AE-1** — `scripts/ae_anchor_fingerprints.py`: exact-rational anchor fingerprints for Cooper s7, s10, Apéry ζ(3); controls S21/S12; emits `data/autoresearch_v2/ae_anchor_fingerprints.json` and C3b certificates.
- **AE-2** — deterministic generator over 2-factor `(A,B) ∈ [1,5]²` and 3-factor `(A,B,C) ∈ [1,3]³` binomial sums (52 genomes).
- **AE-3** — gate battery: G1-1 ODE order 3, G1-3 mirror-map integrality, C3b symmetric-square-root hard gate.
- **AE-4** — ranking per `K3_CRITERIA_INTERFACE.md` weights: math rigor 0.60 (order-3 0.25, held-out 0.15, C3b 0.20); empirical 0.30 blocked on DM-3 quorum; theory 0.10 blocked on Stream 3 artifact.
- **AE-5** — elliptic-EFT alignment by aggregating C3b partner recurrences and operator-identity certificates.

### How to run

```bash
python scripts/ae_preflight.py
python scripts/ae_anchor_fingerprints.py
python scripts/auto_evolve_k3_selection.py
```

The driver writes `data/autoresearch_v2/ae_ranking.json` and C3b certificates under `data/certificates/ae/`.

### Validation commands

```bash
python -m pytest tests/test_autoevolve_stream2.py -q
```

### Runtime results

*Pending execution. Results will be inserted here after the selection run completes.*