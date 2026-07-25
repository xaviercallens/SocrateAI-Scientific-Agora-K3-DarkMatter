# ESCALATIONS

Formal escalation register. One entry per ticket. Entries are append-only; status
changes are edited in place with a dated note.

> **Note (2026-07-26):** this file did not previously exist in the repo, despite being
> referenced by earlier briefs. It is created here to formally close **E-007** per the
> Deep Think (T0s) mandate of 2026-07-25. Earlier tickets E-001…E-006 were never
> recorded in a central register; if they exist in stream-local briefs they should be
> back-filled here.

---

## E-008 — Route A refuted: L₃ is also not unipotent at the finite singular loci

| | |
|---|---|
| **Status** | 🔴 **OPEN** — Route A closed; only Route B (ramified pullback) remains |
| **Opened** | 2026-07-26 |
| **Raised by** | Opus 5 (Stream 2), testing the Deep Think course-correction mandate |
| **Severity** | High — invalidates the proposed replacement path for the retracted C1/C2 layer |

### Finding

Deep Think's course-correction (2026-07-25) mandated **Route A**: run C1/C2 on L₃
instead of L₂, on the stated premise that

> *"Because L₃ = Sym²(L₂), the ½ exponents of L₂ double to 1 in L₃, effectively
> clearing the branch cut and rendering L₃ unipotent at the finite singular points."*

**That premise was tested and is FALSE.** `scripts/compute_L3_monodromy.py`:

```
L2 exponents at every finite locus:  {0, 1/2}
L3 exponents at every finite locus:  {0, 1/2, 1}   <- NOT unipotent
```

Confirmed two independent ways that agree exactly:
1. **Direct order-3 indicial computation** at each locus (s7: z = −1, 1/27;
   s10: z = −1/4, 1/16).
2. **Sym² structure.** Sym² of a rank-2 system with exponents {a, b} has solution
   space {y₁², y₁y₂, y₂²} and hence exponents {2a, a+b, 2b}. With {0, ½} that is
   **{0, ½, 1}** — only y₂² doubles to 1; the **cross term y₁y₂ retains ½**.

So the branch cut is *not* cleared and **Kodaira classification remains blocked at
the L₃ level too.** Running Tate/Kodaira on L₃ would repeat the E-007 fabrication
one level up.

### Also refuted: the "gauge transformation" escape

Both Deep Think's Route B-as-gauge and my own earlier Phase 2 Route β proposed
"untwisting L₂ by gauge transformation to clear the ½-exponents." **This cannot
work.** A gauge transformation `y ↦ f·y` shifts *all* exponents at a point by
`ord(f)`, so **exponent differences are gauge-invariant**. A difference of ½ cannot
be gauged away — including by fractional twists like `P₂^{1/4}`, which shift
uniformly too.

### What remains viable

**Only a ramified pullback.** Passing to a double cover branched at the singular
loci genuinely converts exponent ½ into an integer. Concretely this is the
**Hauptmodul route**: A279619 is the expansion of A002652 (weight-1 form, disc −7)
in powers of **A279618** (the level-7 Hauptmodul). The natural coordinate is the
Hauptmodul `t`, not `z`, and the ramification lives in the map `z ↦ t`.

### Deliverables produced

- `scripts/compute_L3_monodromy.py` — tests the premise, does not assume it
- `data/certificates/C1_L3_cooper_s7.json`, `C1_L3_cooper_s10.json` —
  verdict `L3_NOT_UNIPOTENT_AT_FINITE_LOCI`, `route_A_premise: REFUTED`.
  **`picard_rank` and `transcendental_rank` are `null` by design** — emitting them
  would repeat the E-007 fabrication.

### Next

Route B (Hauptmodul pullback) is now the only proposed path not yet refuted. It
must be *tested*, not assumed, before any ρ/T is emitted. See
`briefs/STREAM2_ACTION_PLAN_2026_07_26.md` Phase 2.

---

## E-007 — K3 geometry cannot be extracted from L₂ as-is

| | |
|---|---|
| **Status** | 🟢 **CLOSED (2026-07-26)** — resolved by literature identification + independent verification |
| **Opened** | ~2026-07-24 (Stream 2 C1/C2 layer) |
| **Closed** | 2026-07-26 |
| **Raised by** | Stream 2 |
| **Resolved by** | Deep Think (T0s) literature review 2026-07-25 + Opus 5 independent verification 2026-07-26 |
| **Severity** | High — invalidated the C1/C2 certificate layer and a live Stream 3 prior |

### Resolution

**The {0, ½} local exponents of L₂ are the correct algebraic signature of a weight-1
modular form obtained as an exact square root — not a geometric defect. K3 geometry
cannot be extracted from L₂ in its current normalization.**

Established facts:

1. **A279619's g.f. is exactly the square root of A183204's g.f.**
   Independently re-verified from `refs/recurrences_v1.json`:
   `(1,2,22,336,6006,117348,2428272,52303680)² = (1,4,48,760,13840,273504,5703096,123519792)` ✅
   exact on all 8 available terms.

2. **Therefore L₂ is a *twisted* Picard–Fuchs operator.** A unipotent PF operator has
   exponents {0,0}; its exact square root halves them to {0, ½}, introduces branch cuts,
   and flips the local monodromy determinant to **−1** (a reflection). The irrational
   Wronskian `W = C/(z√P₂)` is the analytic signature of that twist.

3. **det(monodromy) = −1 ∉ SL₂(ℤ).** Every Kodaira fibre monodromy lies in SL₂(ℤ)
   (det +1). So **no Kodaira fibre type is derivable from L₂'s exponents by any
   labelling** — neither the certificates' "II" nor the later-proposed "I₁".
   Verified independently: `checkers/check_C1_kodaira_consistency.py`.

4. **The geometric substrate for s7 is the modular curve X₀(7) with CM by ℚ(√−7)** —
   *not* a generic Beauville rational elliptic surface with 4 singular fibres.
   Literature: L. O'Brien, *"Modular forms and two new integer sequences at level 7"*
   (MSc thesis, Massey University, 2016, supervisor S. Cooper), **Theorem 6.1**;
   earlier as **Conjecture 5.4** in Chan, Cooper & Sica (2010), *"Congruences satisfied
   by Apéry-like numbers"*. A279619 = expansion of the g.f. of A002652 (x²+xy+2y²,
   disc −7) in powers of A279618 (level-7 Hauptmodul).

5. **s10 non-integrality is expected**, not an error: level 10 (Γ₀(10)) lacks the cusp
   structure that yields integral coefficients at level 7, forcing denominators scaling
   as powers of 2 (2-isogeny). s10 is correspondingly a messier F-theory candidate.

### Permanent consequences

- **The C1/C2 certificate layer is PERMANENTLY RETRACTED**, both v1 and v2:
  `C1_cooper_s{7,10}_partner{,_v2}.json`, `C2_cooper_s{7,10}_partner{,_v2}.json`,
  `C1_monodromy_cooper_s{7,10}_partner_v2.json`.
  Retained on disk for audit trail; must not be cited as evidence.
- **ρ = 4 and T = 18 are withdrawn.** They were produced mechanically by a hardcoded
  `components = 2` inside a faulty exponent→Kodaira lookup
  (`scripts/compute_C1_monodromy.py`, `exponents_to_kodaira_type`), whose own docstring
  is wrong (it claims Δ=1/2 ⇒ II/III/IV; actual: II=1/6, III=1/4, IV=1/3).
  *(Note: contrary to the Deep Think write-up, Tate's algorithm was never run — the
  mechanism was this lookup table. Same conclusion, different cause.)*
- **`exponents_to_kodaira_type()` must be deleted, not fixed.** No exponent→Kodaira
  lookup is valid for a twisted operator.
- **Discriminant = −3** (v1 certs only) is withdrawn with them.

### Downstream — ✅ T0 DECIDED 2026-07-26 (decision D1)

Xavier (T0) authorized: criterion 1 is scored **UNRESOLVED** for the 2026-07-27 verdict;
the other five criteria proceed on their own evidence; the date is kept; criterion-1
outputs are retained as re-scorable data. Best achievable Gate E outcome is therefore
**CONDITIONAL**. Record: `briefs/T0_DECISIONS_2026_07_26.md` · handoff:
`briefs/STREAM2_TO_STREAM3_GATE_E_CRITERION1_2026_07_26.md`.

### Not affected

`L₃ = Sym²(L₂)` remains **Tier A, kernel-verified** — the Sym² relation is exactly what
this resolution *confirms*. The exact singular loci ({1/27, −1}, {1/16, −1/4}) are
independently re-confirmed. All WP-B1 chameleon results are untouched.

### Follow-on work

Geometry must be re-derived either from **L₃** (fully unipotent) or from an
**untwisted L₂** (gauge transform to clear the ½-exponents and restore a rational
Wronskian). See `briefs/STREAM2_ACTION_PLAN_2026_07_26.md` Phase 2A/2B.

---
