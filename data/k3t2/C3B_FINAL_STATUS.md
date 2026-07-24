# C3b Extraction — Final Status Report

**Date:** 2026-07-18 (corrections 2026-07-20; **RESOLVED 2026-07-24**)  
**Status:** ✅ **RESOLVED for cooper_s7 and cooper_s10** — order-2 elliptic partners extracted and certified  
**Authority:** Peer review (2026-07-18); user directive to hold Stream 3 handoff until C3b complete

---

> ## ✅ RESOLUTION 2026-07-24 — the partner is computed, not catalogued
>
> **The C3b partner search was looking for the wrong kind of object.** It sought a *catalogued*
> order-2 Apéry-like sequence whose mirror map has a low-degree algebraic relation to the bulk's.
> Every catalogued candidate failed — because the partner is not in any catalogue.
>
> **What was done (all exact arithmetic, from committed data):**
> 1. Fetched Zagier's six sporadic order-2 sequences (Gorodetsky arXiv:2102.11839, Table) and ran
>    the moduli-map checker for s7 and s10 against **all six** (incl. apery_zeta2=D and A002893=C).
>    Result: **no validated mirror-map relation** up to bidegree 5, 8 power-hypotheses, to q³².
>    The known sporadic order-2 class is exhausted — none is the partner.
> 2. Tested symmetric-square-ness directly: the series square root f = √(Σaₙzⁿ) of s7 and s10 is
>    **order-2 holonomic** (exact nullspace fit, re-validated to n=58). A generic order-3 sequence's
>    √g is NOT (control), so this is a non-trivial property. This *extracts the partner operator L₂*.
> 3. Confirmed **z(L₂)(q) = z(L₃)(q) exactly** to q¹⁴ — Sym² preserves the mirror map, so the C3b
>    moduli map is the **identity** (the tightest possible Shioda–Inose relation, z_bulk = z_brane).
>
> **Partners (checker `check_C3b_symsqrt.py`; certificates `data/certificates/C3b_symsqrt_*.json`):**
> - **s7** → `(n+1)²fₙ₊₁ = (26n²+13n+2)fₙ + 3(3n−1)(3n−2)fₙ₋₁`, integer sequence **OEIS A279619**
>   (1, 2, 22, 336, 6006, 117348, …). Certified `SYM2_PARTNER_EXTRACTED`, PASS(58).
> - **s10** → `(n+1)²fₙ₊₁ = (12n²+6n+1)fₙ + (8n−5)(8n−3)fₙ₋₁`, partner series **rational** (2-power
>   denominators) — an operator-level partner, not a catalogued integer sequence. PASS(58).
>
> Both partners are *extended-form* order-2 operators (full-quadratic on fₙ₋₁, "d≠0") — which is
> exactly why none of Zagier's six *pure* sporadics matched.
>
> **Epistemic scope:** verdicts are finite-order machine checks — report as **PASS(58)**, not
> "proved for all n". The all-n operator identity L₃ = Sym²(L₂) is a **Stream-1 symbolic follow-up**.
> Naming L₂ "the elliptic/brane partner" and any bulk↔brane physical coupling remains **Tier C**
> (conjecture); the geometric Sym² relation implies no EFT coupling absent a worked matching.
>
> **F6 correction:** the 2026-07-20 note calling A002893 "weight-3 K3-type / genuinely order-3 ODE,
> invalid as an order-2 brane" was itself wrong — A002893 is Zagier's second-order sporadic C
> (10,9,3), a valid order-2 sequence; it is simply *not s7/s10's partner* (now empirically ruled
> out). The refs entry is corrected to `OK_NOT_A_PARTNER`.

---

> **CORRECTION 2026-07-20 — refs data-integrity sweep.**
> The "all 5 sequences pass validation" claim below was verified only for the **3 executed**
> sequences (cooper_s7, cooper_s10, apery_zeta2). A mechanical sweep (regenerate each sequence
> from its own recurrence, compare to stated terms) found the **2 reserve partners were corrupt**:
> - `gorodetsky_s18` — recurrence predicts a₂≈0.544 (not 672); no clean order-3 fit exists
>   (consistent with the G1-1 "s18 is order-4" finding). Now `BLOCKED_CORRUPT_RECURRENCE`;
>   needs re-transcription from arXiv:2102.11839.
> - `zagier_sporadic_A` — recurrence predicts a₂=−6 (not 15); tail terms fabricated. The true
>   sequence is **OEIS A002893** (verified via OEIS fetch). But A002893 is weight-3 **K3-type**
>   (Beukers–Stienstra), **not** a weight-2 elliptic curve → invalid as an order-2 brane. Now
>   `BLOCKED_WRONG_TYPE`.
>
> Both now return `REFUSED_NO_DATA`. **Consequence:** no valid untested pairing remains
> (only s7+apery, s10+apery are type-valid, both already ruled out). The blocker is unchanged
> and mathematical: a correct **weight-2 elliptic** partner for s7/s10 from modular-forms theory.

---

## What Is Complete ✅

### Framework
- Reference database (refs/recurrences_v1.json) with 5 sequences
- C3b checker (check_C3b_moduli_map.py v1.0.0) fully functional
- Both bulk (K3) and brane (elliptic) sequences pass validation:
  - Integrality: PASS (all-integer terms to order 28+)
  - MUM: PASS (C(k) = (k+1)^order confirmed)
  - Mirror maps: PASS (computed to order 24+)

### Testing
- Tested pairings: cooper_s7 + apery_zeta2, cooper_s10 + apery_zeta2
- **Result:** High-degree relations found (degree 5-6, coeff 10^30+), NOT low-degree
- **Interpretation:** apery_zeta2 is NOT the canonical Shioda-Inose partner

---

## What Remains ⏳

**Single blocker:** Identify correct K3↔elliptic pairings

### Why Pairings Matter
- **Genuine Shioda-Inose maps** link K3 surfaces to elliptic curves via SIMPLE algebraic relations
- **Wrong pairings** produce high-degree relations (computationally valid, geometrically invalid)
- **Correct pairings** should have low-degree F(z) (bidegree ≤ 4, ideally ≤ 2)

### Partner Candidates for Testing

From Phase B findings, viable elliptic sequences (order-2, weight-2):
- **apery_zeta2** (A005258) — TESTED, ruled out (high-degree relations)
- **A006077** (Zagier sporadic) — untested
- **A112019** (S12 variant, has issues) — likely invalid

### Viable K3 Candidates (order-3, weight-3)
- **cooper_s7** (A183204, level-7) — PRIMARY ✓
- **cooper_s10** (A005260, level-10) — SECONDARY ✓
- **almkvist_zagier_second** (A125143) — TERTIARY (alternative)
- ~~cooper_s18~~ (A219692) — REJECTED (order-4, not K3)

---

## Path Forward

### Option 1: Derive Pairings from Modular Form Theory (Recommended)
Research the Shioda-Inose construction for Cooper's sporadic sequences. Expected outcome:
- Each K3 level (7, 10) paired with specific elliptic level
- Pairing documented in modular forms literature
- Implement pairings, run checker battery

**Effort:** ~3-5 hours (mathematical literature review)  
**Risk:** Low (construction is classical, deterministic)

### Option 2: Systematic Testing
- Test remaining Zagier/elliptic candidates against cooper_s7/s10
- Run at (n_terms=24, max_bidegree=2) to detect low-degree relations early
- Acceptable pairings show degree 1-2 relations

**Effort:** ~2-3 hours (computational)  
**Risk:** May not find pairings if not in current candidates list

### Option 3: Hybrid
- 30 min literature review for clues
- If clear leads → Implement
- If unclear → Fallback to systematic testing

---

## Expected Outcome

Once correct pairings identified:

```bash
# For each valid pair:
python3 checkers/check_C3b_moduli_map.py \
  --bulk cooper_s{7|10} \
  --brane <correct_elliptic_partner> \
  --n-terms 28 --max-bidegree 4
```

Expected results:
- ✅ **FOUND:** Low-degree F(z) (bidegree ≤ 2-3)
  - Decision: C3B PASS → D-3 proceeds, geometry validated
  
- ❌ **NOT_FOUND:** No low-degree relation
  - Decision: C3B FAIL (Branch F5) → geometry breaks, model falsified

---

## Why C3b Matters

After D-1v2 (observable validated), the question is: **Does the K3 geometry lock to an associated elliptic curve algebraically?**

- If YES (low-degree relation): EFT mechanism closes → D-3 empirical validation proceeds
- If NO (no low-degree relation): Geometric mechanism breaks → Branch F5, model falsified

Stream 3 handoff is held pending this answer.

---

## Commits This Session

- e9144a7: GATE D-1v2 PASS
- 16c6b53: C3b framework established
- 9fa3030: OEIS verification
- 39c194c: Blocker analysis
- d6efd25: Framework functional
- 1c79259: Stream 3 readiness memo (HOLD)

---

**Recommendation:** Proceed with Option 3 (hybrid approach). Expect C3b verdict by 2026-07-19 EOD.

**Authority:** User directive (2026-07-18): "Wait for C3b complete + peer review + formal review before Stream 3 handoff"

---

**Status:** READY FOR PARTNER IDENTIFICATION (framework proven, scaling to higher degree successful, just need correct pairings)
