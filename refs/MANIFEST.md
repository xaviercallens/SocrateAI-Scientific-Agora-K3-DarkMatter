# refs/ MANIFEST — data provenance register

Every file in `refs/` must be listed here with SHA256 and source citation before any checker
reads it (criteria-checkers contract §2). To add a literature value: add the file + this entry
first, then read it from the checker. Never transcribe numbers from memory.

| file | sha256 | source / citation | added |
|---|---|---|---|
| recurrences_v1.json | (tracked by per-checker `refs_sha256` fields in certificates; current: run `sha256sum refs/recurrences_v1.json`) | Frozen recurrence register: Cooper 2012 (Ramanujan J. 29), OEIS A183204/A005260/A005258/A002893, Gorodetsky arXiv:2102.11839 (s18 BLOCKED — corrupt), + DERIVED partners (check_C3b_symsqrt.py) | ≤2026-07-24 |
| oeis_A112019_bfile.txt | fbaed47a4d1c892ab7c8b9811ed6be95dc328a57e685aa6ed44955370d51517a | OEIS A112019 b-file, https://oeis.org/A112019/b112019.txt — a(n)=Σ C(n,k)·C(n+k,k)²; fetched 2026-07-24 | 2026-07-24 |
| oeis_A005259_bfile.txt | ba139ad41908a1bf6201d5d7c366a182fdd93e00d57ad65a700850f284dbee20 | OEIS A005259 b-file — Apéry ζ(3), Beukers–Peters K3; fetched 2026-07-24 | 2026-07-24 |
| oeis_A002895_bfile.txt | b2e750030034aa64ae02daf6a89a46c5503c4a0bf4cdb95949187c4d94b283a0 | OEIS A002895 b-file — Domb numbers, K3-class; fetched 2026-07-24 | 2026-07-24 |
| oeis_A125143_bfile.txt | 977daaeb90c900465d5963d424249a8d3745f5e42c3230a9f67947b862e312f7 | OEIS A125143 b-file — Almkvist–Zudilin 2nd K3-class; fetched 2026-07-24 | 2026-07-24 |
| oeis_A006077_bfile.txt | 0084a70705396f0f5bc1b2b053f310b0e5799c233065a5da8fb111828436184a | OEIS A006077 b-file — Zagier order-2 sporadic (elliptic); fetched 2026-07-24 | 2026-07-24 |

**Recurrences for the 4 sequences above were DERIVED by exact nullspace from these b-files
(`scripts/derive_refs_entry.py`), never transcribed. A005259 and A006077 derived recurrences
were cross-checked to reproduce their textbook forms exactly.**

## Pending additions (no numbers about these may be cited until landed)

- **Stream 3's exact γ/F, α/C, δ/A, η/D pairs** — OEIS IDs REQUESTED from Stream 3 (their brief
  named them but this repo's pool does not identify them; see ROUTE_A_EXECUTION_FINDINGS_2026_07_24.md)
- s18 clean re-transcription from arXiv:2102.11839 (replaces BLOCKED entry; F6-track)

Generated-by: Stream 2 (Fable 5) | Verified-by: sha256sum | Reviewed-by: T0 pending
