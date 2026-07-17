# CLAUDE.md — Stream 2: K3 Selection

Candidate ranking repo. Governing docs: `VISION.md`, `K3_CRITERIA.md` (the frozen interface),
`EXECUTION_PLAN.md` §3. Read the **criteria-checkers** skill before touching checkers/certificates
and **autoevolve-harness** before any ranking run; **epistemic-guardrails** for all prose.

## Commands
- Checker tests: `pytest checkers/tests/`
- Run a checker: `python checkers/check_C<k>.py --candidate K-<id>`
- Status table: `python scripts/render_status_table.py` (only way to update it)
- Ranking: see autoevolve-harness skill (seeded, reproduced, diffed before reporting)

## Non-negotiable rules
1. Every number about a candidate comes from a checker certificate. No exceptions, no memory.
2. Exact arithmetic; no network/LLM calls inside checkers; literature inputs only via `refs/` + manifest SHA256.
3. `K3_CRITERIA.md` frozen ⇒ amendment protocol only (hook-enforced). Unresolved TBD-AT-FREEZE ⇒ implementation blocked; escalate.
4. Hard-criterion failure ⇒ F1 removal logged in the same PR. No renormalization retries.
5. Status table and certificates are machine-written (hook-enforced).
