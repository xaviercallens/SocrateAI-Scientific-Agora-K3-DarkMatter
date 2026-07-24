# Route-A Prerequisite — Execution Findings & Decision (2026-07-24)

**Executed by:** Stream 2 (Opus 4.8) under T0 delegation | **Status:** COMPLETE — decision below
**One-line result:** Route A produced **one catalogued lead (Domb × A002893)** and **one new
theorem (Domb is a symmetric square)**, but **no fully-certified catalogued Shioda–Inose pair**;
S3-00 input decision revised accordingly.

---

## 1. What was executed (all from real fetched data — zero memory transcription)

Fetched 4 OEIS b-files (hash-pinned, `refs/MANIFEST.md`), derived each Picard–Fuchs recurrence
by **exact integer nullspace** (`scripts/derive_refs_entry.py`), and cross-checked: the derived
A006077 and Apéry-ζ(3) recurrences **reproduce their textbook forms exactly** (independent
validation of the derive pipeline). Then ran the committed checkers.

| Sequence | OEIS | min-ODE | C3b-SYM (is it Sym²?) | Sym² partner |
|---|---|---|---|---|
| Apéry ζ(3) | A005259 | 3 (K3) | **NO** — `FAIL_PARTNER_VALIDATION` | non-integral |
| **Domb** | **A002895** | **3 (K3)** | **YES — `SYM2_OPERATOR_IDENTITY_PROVEN` (all-n)** | **integral: 1,2,12,104,1078,12348,…** |
| Almkvist–Zudilin 2nd | A125143 | 3 (K3) | **NO** — `FAIL_PARTNER_VALIDATION` | non-integral |
| A006077 | A006077 | 2 (elliptic) | — (order-2, a partner-candidate) | — |
| *(prior)* cooper_s7 | A183204 | 3 | YES | integral = OEIS A279619 |
| *(prior)* cooper_s10 | A005260 | 3 | YES | non-integral |

**New theorem (Tier B, all-n symbolic):** the **Domb** order-3 K3 operator **is the symmetric
square** of an order-2 operator with an **integral** solution `1,2,12,104,1078,12348,150528,…`.
Certificate `data/certificates/C3b_symsqrt_domb.json`. This partner is **not in OEIS** (searched;
"No results") — non-catalogued, like cooper_s7/s10's partners.

## 2. C3b-CAT (catalogued moduli-map relation) — the Route-A criterion

| Pair (bulk × brane) | Verdict |
|---|---|
| **Domb × A002893** (`zagier_sporadic_A`) | **`C3B_RELATION_FOUND` (validated q³⁶)** — bidegree (2,4), leading `x−y` |
| Domb × A005258 (apery_zeta2) | NOT_FOUND |
| Domb × A006077 | NOT_FOUND |
| cooper_s7 × A006077 | NOT_FOUND |
| *(prior)* cooper_s7 × A005258 | NOT_FOUND |

**Domb × A002893 is the only catalogued pair in the entire tested pool with a C3b-CAT relation.**
Both are literature-anchored, in OEIS, with verified ODE orders (Domb order-3, A002893 order-2 —
the latter **refuting** the old "A002893 is K3-type" note; min-ODE checker says order-2 `PASS(43)`).

## 3. The honest caveat that blocks immediate designation

A002893 is **not** Domb's C3b-SYM square-root (that partner is `1,2,12,104…`). So the
Domb × A002893 relation is a **moduli correspondence of unverified geometric type**, not a
certified Sym²/Shioda–Inose partnership. This is exactly the bar the cooper_s7 candidates were
held to (a found algebraic relation was previously deemed insufficient without Shioda–Inose
confirmation). Additionally, the C1-KOD checker returns **degenerate** output for A002893
(0 fibres, ρ=2) — its heuristic singular-locus extraction cannot resolve A002893's complex-root
locus — so **no reliable Picard rank is available** for the PREDICTION.md §2 mechanical
ρ-selection. The pair cannot be mechanically ranked, and its Shioda–Inose status is uncertified.

## 4. Decision (T0-delegated, countermand window open)

**The pre-registered Route-A eligible set — "catalogued pairs passing C1-INT + C3-CAT + C3b-CAT
with a certified Shioda–Inose map and a rankable Picard lattice" — is currently EMPTY.**
The one C3b-CAT relation (Domb × A002893) is a promising lead but uncertified; I will not
fabricate a certified pair to unblock S3-00 (that is the precise pre-registration violation the
program forbids).

**Decision:**
1. **Do NOT designate a Route-A pair for S3-00 yet.** The mechanical selection rule fires on an
   empty eligible set → no winner.
2. **Elevate Domb × A002893 to T0s (Deep Think) for Shioda–Inose adjudication** — is the
   bidegree-(2,4), q³⁶-validated relation a genuine Shioda–Inose/Sym² correspondence or an
   accidental moduli relation? This is the single most decision-relevant open question.
3. **Record the new Domb C3b-SYM theorem** as an independent result (candidate for the Lean
   Sym² treatment already applied to s7/s10).
4. **Recommended S3-00 fallback = Route B**, K3 = **cooper_s7** (its extracted partner A279619 is
   at least OEIS-catalogued) or **Domb**, with the **partner's modular identification (level,
   weight-2 newform) as an explicit, tracked S3-00 sub-dependency** — Tier B until anchored.
5. **Escalate the Route-A premise to Stream 3:** their brief named specific pairs "γ/F, α/C,
   δ/A, η/D." Those exact sequences are **not identified in this repo's literature-anchored pool**
   and I cannot read their separate repo. **Request their OEIS IDs + refs data** so both repos
   fetch from the same cited sources; if those pairs are genuine catalogued Sym² pairs, they
   supersede this finding.

## 5. Structural takeaway (for the record)

Every Apéry-like order-3 K3 **symmetric square** found so far (cooper_s7, cooper_s10, Domb) has a
**non-catalogued** order-2 partner; the famous named K3s that are **not** symmetric squares
(Apéry ζ(3), Almkvist–Zudilin 2nd) trivially have no partner. The "catalogued Sym² pair" premise
underlying Route A does **not** hold for the standard pool as tested. This is itself a reportable
result (it sharpens the C3b-CAT/C3b-SYM distinction from the reconciliation brief).

---

## Artifacts (committed)

- `refs/oeis_A005259|A002895|A125143|A006077_bfile.txt` (hash-pinned, MANIFEST updated)
- `refs/recurrences_v1.json` — 4 new entries, recurrences DERIVED (not transcribed)
- `scripts/derive_refs_entry.py` — nullspace recurrence derivation + verification
- `data/certificates/C3b_symsqrt_{domb,apery_zeta3,almkvist_zagier_second}.json`
- `data/certificates/C3b_domb__zagier_sporadic_A.json` (the C3b-CAT relation)
- `data/certificates/C1_zagier_sporadic_A.json`, `C2_zagier_sporadic_A.json` (degenerate — see §3)
- `data/certificates/MINODE_{A112019,domb_A002895,zagier_sporadic_A_A002893}.json`

Generated-by: Stream 2 (Opus 4.8) under T0 delegation | Verified-by: committed checkers + OEIS b-file hashes | Reviewed-by: T0 delegated; T0s adjudication REQUESTED for Domb × A002893
