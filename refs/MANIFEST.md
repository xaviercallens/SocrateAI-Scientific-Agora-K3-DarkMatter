# refs/ MANIFEST — data provenance register

Every file in `refs/` must be listed here with SHA256 and source citation before any checker
reads it (criteria-checkers contract §2). To add a literature value: add the file + this entry
first, then read it from the checker. Never transcribe numbers from memory.

| file | sha256 | source / citation | added |
|---|---|---|---|
| recurrences_v1.json | (tracked by per-checker `refs_sha256` fields in certificates; current: run `sha256sum refs/recurrences_v1.json`) | Frozen recurrence register: Cooper 2012 (Ramanujan J. 29), OEIS A183204/A005260/A005258/A002893, Gorodetsky arXiv:2102.11839 (s18 BLOCKED — corrupt), + DERIVED partners (check_C3b_symsqrt.py) | ≤2026-07-24 |
| oeis_A112019_bfile.txt | fbaed47a4d1c892ab7c8b9811ed6be95dc328a57e685aa6ed44955370d51517a | OEIS A112019 b-file, https://oeis.org/A112019/b112019.txt — a(n)=Σ C(n,k)·C(n+k,k)²; fetched 2026-07-24 | 2026-07-24 |

## Pending additions (Route-A prerequisite — no numbers about these may be cited until landed)

- AZ sporadic order-3 sequences γ, α, δ, η + their Zagier order-2 partners (F, C, A, D)
- A005259 (Apéry ζ(3)) — Beukers–Peters K3 candidate
- s18 clean re-transcription from arXiv:2102.11839 (replaces BLOCKED entry; F6-track)

Generated-by: Stream 2 (Fable 5) | Verified-by: sha256sum | Reviewed-by: T0 pending
