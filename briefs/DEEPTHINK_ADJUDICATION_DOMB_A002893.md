# Deep Think Adjudication Request + Stream-2 Opinion & Decision: Domb × A002893

**To:** Deep Think (T0s) | **From:** Stream 2 (Opus 4.8, under T0 delegation) | **Date:** 2026-07-24
**Question referred:** Is the `C3B_RELATION_FOUND` between Domb (A002895, K3) and A002893
(order-2 elliptic) a genuine Shioda–Inose/Sym² partnership fit to be the Route-A S3-00 input?
**Stream-2 verdict (decision taken, countermand open): NO — genuine correspondence, but not
Shioda–Inose. Route A stays dead; S3-00 proceeds under Route B (cooper_s7).**

This brief gives the adversarial reviewer everything needed to overturn that call if it's wrong.

---

## 1. The evidence (all machine-computed, reproducible)

**The relation** (`data/certificates/C3b_domb__zagier_sporadic_A.json`), x = z_Domb, y = z_A002893:
```
-y + 10y² - 9y³ + x - 8xy - 2xy² - 72xy³ + 81xy⁴ + 64x²y² = 0
```
- Fired at **bidegree (4,4)**, q-power hypothesis **[1,1]** (equal grading), **validated to q³⁶**.
- Overdetermination: ~24 coefficients → 23 dof after scale; agreement to q³⁶ gives ≈22 surplus
  equations. **This is not an accidental fit** — a random pair does not satisfy 22 independent
  exact-rational constraints (compare: cooper_s7 × A005258 and Domb × A005258/A006077 all
  `NOT_FOUND`).
- **`P(0, y) = −y(y−1)(9y−1)`**: at Domb's MUM point the curve hits y = 0, 1, 1/9 — i.e. exactly
  A002893's own singular loci {1/9, 1} plus its MUM. This is real structure, not noise.

**Why it is nonetheless NOT a Shioda–Inose / Sym² partnership:**
1. **A002893 is not Domb's symmetric-square root.** Domb *is* a proven symmetric square
   (`C3b_symsqrt_domb.json`, all-n) but of the **uncatalogued** integral operator
   1,2,12,104,1078,… — whose singular loci are **{1/16, 1/4}**, not A002893's {1/9, 1}.
2. **No bijective singular-fibre correspondence.** On the curve P=0: x=1/4 ↦ y=1/3 (not an
   A002893 fibre); x=1/16 ↦ y=(2±√3)/3 (**irrational** — cannot be a fibre of a ℚ-rational
   elliptic surface). A Shioda–Inose isogeny maps singular fibres to singular fibres over ℚ;
   this map does not.
3. **Degree.** A clean Shioda–Inose/Sym² moduli map is low-degree (the Sym² map is the identity,
   degree 1). A genuine but generic algebraic correspondence is high-degree — this is (4,4).

**Interpretation (Stream-2, Tier B):** Domb and A002893 are two distinct Apéry-like families
sharing a real degree-(4,4) algebraic moduli correspondence — plausibly a shared Hauptmodul /
level relation, worth its own study — but A002893 does **not** supply Domb with a *catalogued
Sym² partner*. It therefore does not satisfy the Route-A requirement ("K3 = Sym²(catalogued
elliptic)"), and cannot furnish the catalogued weight-2 modular data S3-00 needs from a partner.

## 2. What Deep Think should adversarially check (Two-Model Rule)

- Re-derive the relation independently; confirm bidegree/validation depth.
- **Challenge my §1.2 claim**: is there a *reparametrization* y ↦ φ(y) under which the loci pair
  rationally and the map becomes a genuine Shioda–Inose isogeny? If yes, Route A revives with
  Domb × A002893 and this decision is overturned.
- Sanity-check the F6 C1 finding below (independent).

## 3. Concurrent F6 integrity finding (disclosed, README-noted)

While computing the true singular loci for this adjudication I found **`check_C1.py` is defective**:
it solved for roots of the recurrence coefficient **B(k) in the discrete index k** and mislabeled
them as z-space singular points, with **hardcoded** exponents (0, 1/2) → "type II". Consequences:
- The C1 fibre configs and the C2 numbers **ρ=4, T=18** (both partners) are **NOT valid** —
  retracted (`_F6_RETRACTED` stamped on all six C1_/C2_ certs; README disclosure added).
- **Corrected z-space loci** (`checkers/check_C1_singular_loci.py`, exact algebra):
  cooper_s7_partner **{−1, 1/27}**, cooper_s10_partner **{−1/4, 1/16}**, A002893 **{1/9, 1}**.
- **Unaffected:** the v0.3.0 **Sym² proof** (`CooperSym2Proof.lean`) — pure operator algebra, no
  dependence on the C1 locus step. The headline L₃=Sym²(L₂) result stands. Full Kodaira re-typing
  (local Frobenius exponents at the corrected loci) is an open ticket.

## 4. Decision taken (T0-delegated; countermand window open)

1. **Route A remains DEAD for the standard pool.** No certified catalogued Shioda–Inose pair
   exists; Domb × A002893 is a real correspondence but not such a pair (§1).
2. **S3-00 input = Route B, K3 = cooper_s7.** Rationale: Sym²-proven (kernel, v0.3.0); its
   order-2 partner **A279619 is OEIS-catalogued** and **integral** — strictly the best-anchored
   of the three (cooper_s10's partner is non-integral; Domb's is uncatalogued). The one remaining
   Tier-B dependency is the **modular identification** of A279619's operator (level, weight-2
   newform) — a tracked research task, **not** a pipeline blocker (V5 is candidate-agnostic).
3. **Domb × A002893** → logged as an open mathematical lead (possible level/Hauptmodul relation),
   not on the S3-00 critical path.
4. **C1/C2 lattice** for cooper_s7 must be **recomputed correctly** before any lattice-dependent
   S3-00 step (the ρ/T selection input); until then no ρ-based ranking is cited.

**This decision is reversible** by Deep Think overturning §1.2 (a rational reparametrization) or by
Stream 3 supplying genuine catalogued γ/α/δ/η Sym² pairs (still requested).

---

Generated-by: Stream 2 (Opus 4.8) under T0 delegation | Verified-by: committed certs + exact algebra herein | Reviewed-by: T0 delegated; **T0s adjudication REQUESTED** on §1.2 and §3
