# Stream 2 — CM points (ρ = 20 locus) of the cooper_s7 and cooper_s10 families

Date: 2026-09-21 · Branch: `stream2/cm-points-rho20-2026-09-21` · Tier: **B at best** · Status: record, not a gate.

Every number below is copied by script from `data/certificates/CM_POINTS_RHO20.json`
(checker `checkers/check_CM_points_rho20.py`, controls `checkers/test_CM_points_rho20_controls.py`).
This is lattice and modular arithmetic. It carries no physical reading of any kind.

## 1. What was computed

For T_n = U ⊕ ⟨2n⟩ (n re-derived from the C2 lattice certificate, never typed), basis (e, f, w),
norm v² = 2xy + 2n z², period ω(τ) = (1, −nτ², τ): an integer vector v = (x, y, z) pairs with the
period as B(v, ω) = y − n x τ² + 2 n z τ, a quadratic in τ of discriminant 2n·v². It has a root in the
upper half plane exactly when v² < 0, namely τ = z/x + i·√(−v²/(2n))/|x|. Stage 0 of the checker
re-derives these identities symbolically (sympy); all hold.

For each primitive v in the logged window (0 < −v² ≤ 44, Im τ ≥ 1/20,
−1/2 < Re τ ≤ 1/2, |τ|² ≥ 1/n, x > 0) the checker computes: τ exactly; T_X := v^⊥ ⊂ T_n as an exact
saturated integer kernel (orthogonality, rank, saturation, evenness, positive definiteness all
checked, and det T_X = (−v²)·2n/div(v)² asserted per row); its Gauss-reduced form (a, b, c) and
D = b² − 4ac; a round trip (from the numerical τ alone the integer vector is recovered); and
z(τ) through the level-n eta quotient t and the relation 1/z = αt + β + γ/t re-fitted exactly to
q^40 (s7: α, β, γ = 49, 13, 1; s10: 16, 8, 1). z is then recognised as
an algebraic number by LLL at 120 digits and accepted only if the polynomial still vanishes
at 200 digits (second tier 320/420 digits, degree ≤ 12, for rows the first tier leaves open).
A value of modulus > 1 is recognised through its inverse, so that the integer LLL matrix never
asks for more digits than the evaluation carries (review fix, see §7).

- cooper_s7: 180 primitive vectors in the window, 71 distinct z (up to complex conjugation), 0 unrecognised; degree histogram {'1': 7, '2': 18, '3': 4, '4': 23, '5': 6, '6': 8, '8': 5}; rows needing the second precision tier: 5; rows of degree > 1 whose minimal polynomial has all its roots in the table: 64/64.
- cooper_s10 (**advisory**, flag `LATTICE_CERT_DRAFT`): 182 primitive vectors in the window, 69 distinct z (up to complex conjugation), 0 unrecognised; degree histogram {'1': 13, '2': 13, '3': 8, '4': 23, '6': 4, '12': 8}; rows needing the second precision tier: 8, all at (D, form) = (−800, (10, 0, 20)), one degree-12 polynomial; rows of degree > 1 whose minimal polynomial has all its roots in the table: 56/56.
- Family-level consistency gates (each gates the exit code, each has a control that makes it fire — §5):
  Fricke consistency z(τ_v) = z(τ_{−swap v}): 0 violations on 180 (s7) and 182 (s10) vectors;
  same z ⇒ same T_X up to the sign of b: 0 violations; same z ⇒ same (−v², div v): 0 violations.
- Grouping by z is numeric clustering at 40 digits, tolerance 10⁻²⁸ relative to 1 + |1/z|.
- Inputs are hash-pinned in the certificate (`inputs.sha256`: the two C2 lattice certificates, the two
  C1 certificates, `refs/recurrences_v1.json`, `docs/literature/MANIFEST.md`).

The window is **not** shown to be a fundamental domain and the table is **not** claimed complete
at any D. The all-roots-present count above is a diagnostic of coverage, not a proof of it.

## 2. Table (first 15 rows per family, sorted by |D|; full table in the certificate)

**cooper_s7** — n = 7, lattice certificate C2_cooper_s7_v5.json (LIVE).

| \|D\| | −v² | div v | reflective | v | T_X (a,b,c) | deg z | z or minimal polynomial | note |
|---|---|---|---|---|---|---|---|---|
| 3 | 42 | 14 | no | (14, -14, -5) | (1, 1, 1) | 1 | `infinity` | z = ∞ |
| 7 | 2 | 2 | yes | (2, -4, 1) | (1, 1, 2) | 1 | `-1` | C1 singular locus |
| 12 | 42 | 7 | no | (7, -7, -2) | (1, 0, 3) | 1 | `1/2` |  |
| 28 | 2 | 1 | yes | (1, -1, 0) | (1, 0, 7) | 1 | `1/27` | C1 singular locus |
| 35 | 10 | 2 | no | (2, -6, 1) | (3, 1, 3) | 1 | `-1/8` |  |
| 56 | 4 | 1 | no | (1, -2, 0) | (2, 0, 7) | 2 | `8*z**2 - 40*z + 1` |  |
| 56 | 4 | 1 | no | (3, -3, -1) | (1, 0, 14) | 2 | `8*z**2 - 40*z + 1` |  |
| 63 | 18 | 2 | no | (2, -8, 1) | (4, 1, 4) | 2 | `125*z**2 - 23*z - 1` |  |
| 63 | 18 | 2 | no | (4, -4, -1) | (1, 1, 16) | 2 | `125*z**2 - 23*z - 1` |  |
| 84 | 6 | 1 | no | (1, -3, 0) | (3, 0, 7) | 2 | `216*z**2 + 68*z - 1` |  |
| 84 | 6 | 1 | no | (2, -5, 1) | (3, 0, 7) | 2 | `216*z**2 + 68*z - 1` |  |
| 91 | 26 | 2 | no | (2, -10, 1) | (5, 3, 5) | 1 | `-1/64` |  |
| 112 | 8 | 1 | no | (1, -4, 0) | (4, 0, 7) | 1 | `1/125` |  |
| 119 | 34 | 2 | no | (2, -12, 1) | (6, 5, 6) | 5 | `1331*z**5 + 670*z**4 + 14262*z**3 - 1775*z**2 + 110*z + 1` |  |
| 119 | 34 | 2 | no | (4, -6, -1) | (5, -1, 6) | 5 | `1331*z**5 + 670*z**4 + 14262*z**3 - 1775*z**2 + 110*z + 1` |  |

**cooper_s10** — n = 10, lattice certificate C2_cooper_s10_v4_DRAFT.json (DRAFT).
**ADVISORY — flag LATTICE_CERT_DRAFT on every row.**

| \|D\| | −v² | div v | reflective | v | T_X (a,b,c) | deg z | z or minimal polynomial | note |
|---|---|---|---|---|---|---|---|---|
| 4 | 20 | 10 | yes | (10, -10, -3) | (1, 0, 1) | 1 | `infinity` | z = ∞ |
| 15 | 12 | 4 | no | (4, -4, -1) | (1, 1, 4) | 1 | `1` |  |
| 16 | 20 | 5 | no | (5, -10, -2) | (2, 0, 2) | 1 | `-1/2` |  |
| 20 | 4 | 2 | yes | (2, -6, 1) | (2, 2, 3) | 1 | `-1/4` | C1 singular locus |
| 24 | 30 | 5 | no | (5, -5, -1) | (1, 0, 6) | 1 | `1/4` |  |
| 40 | 2 | 1 | yes | (1, -1, 0) | (1, 0, 10) | 1 | `1/16` | C1 singular locus |
| 55 | 44 | 4 | no | (4, -8, -1) | (2, 1, 7) | 2 | `81*z**2 - 7*z + 1` |  |
| 60 | 12 | 2 | no | (2, -8, 1) | (4, 2, 4) | 1 | `-1/9` |  |
| 80 | 4 | 1 | no | (1, -2, 0) | (2, 0, 10) | 2 | `4*z**2 + 22*z - 1` |  |
| 80 | 4 | 1 | no | (3, -4, -1) | (2, 0, 10) | 2 | `4*z**2 + 22*z - 1` |  |
| 100 | 20 | 2 | no | (2, -10, 1) | (5, 0, 5) | 1 | `-1/20` |  |
| 120 | 6 | 1 | no | (1, -3, 0) | (3, 0, 10) | 1 | `1/36` |  |
| 140 | 28 | 2 | no | (2, -12, 1) | (6, 2, 6) | 3 | `784*z**3 - 192*z**2 + 32*z + 1` |  |
| 140 | 28 | 2 | no | (4, -6, -1) | (6, 2, 6) | 3 | `784*z**3 - 192*z**2 + 32*z + 1` |  |
| 160 | 8 | 1 | no | (1, -4, 0) | (4, 0, 10) | 2 | `324*z**2 + 52*z - 1` |  |

"reflective" is exact lattice arithmetic: the reflection in v is integral on T_n iff v² divides 2·div(v).

## 3. Pre-registered prediction — outcome: **CONFIRMED** (non-trivial clauses: 3/3)

PRE-REGISTERED (orchestrator hand estimate, unverified before this run): the Fricke fixed point n tau^2 = -1 is v = (1,-1,0), v^2 = -2, T_X = <2> + <2n>; for s7 it maps to one of {-1, 1/27} and the OTHER locus is another (-2)-vector CM point with t = -1/7. For s10: which of {-1/4, 1/16, infinity} come from (-2)- or other small-norm vectors (no value predicted).

- confirmed — cooper_s7: v=(1,-1,0) has v^2=-2 and T_X = <2>+<14> — *arithmetic identity*
- confirmed — cooper_s10: v=(1,-1,0) has v^2=-2 and T_X = <2>+<20> — *arithmetic identity*; **ADVISORY**: n comes from the DRAFT lattice certificate
- confirmed — cooper_s7: Fricke fixed point maps to one of the C1 loci — **non-trivial**
- confirmed — cooper_s7: the OTHER locus is a (-2)-vector CM point — **non-trivial**
- confirmed — cooper_s7: ... at t = -1/7 — **non-trivial**

The two "arithmetic identity" clauses hold for every n once n is fixed and could not have failed;
they carry no content beyond the lattice certificate's n. The content of the confirmation is the
three s7 locus clauses, which depend on the numeric evaluation of z(τ) and could have failed.

Where the singular loci sit (C1 certificates' finite loci, plus z = ∞), cooper_s7:

- z = -1: v = (2, -4, 1), −v² = 2, div v = 2, reflective = True, T_X = (1, 1, 2), D = -7, t satisfies `7*t + 1`
- z = 1/27: v = (1, -1, 0), −v² = 2, div v = 1, reflective = True, T_X = (1, 0, 7), D = -28, t satisfies `7*t - 1`
- z = infinity: v = (14, -14, -5), −v² = 42, div v = 14, reflective = False, T_X = (1, 1, 1), D = -3, t satisfies `49*t**2 + 13*t + 1`

cooper_s10 (advisory; no value was predicted, this is the observation):

- z = -1/4: v = (2, -6, 1), −v² = 4, div v = 2, reflective = True, T_X = (2, 2, 3), D = -20, t satisfies `16*t**2 + 12*t + 1`
- z = 1/16: v = (1, -1, 0), −v² = 2, div v = 1, reflective = True, T_X = (1, 0, 10), D = -40, t satisfies `4*t - 1`
- z = infinity: v = (10, -10, -3), −v² = 20, div v = 10, reflective = True, T_X = (1, 0, 1), D = -4, t satisfies `4*t + 1`

Plain reading of the s7 outcome: the Fricke fixed point v = (1, −1, 0) lands on z = 1/27, and the
other finite locus is the (−2)-vector (2, −4, 1) of divisibility 2 at t = −1/7, with T_X of
discriminant −7. This agrees with Stream 1's `root2 = (−2, 4, 1)` and `s7_singular_points_are_selfdual`
(read as source at commit 3a96018; no Lean build run); here the vectors were found by enumeration,
not imported. z = ∞ is, for s7, the non-reflective vector of norm −42 (Stream 1's order-3 fixed
vector up to the symmetry τ → −τ̄) with T_X = (1, 1, 1), D = −3. For s10 the three points come from
three *different* norms (−2, −4, −20), all reflective; z = ∞ there is at t = −1/4, the second root
of the Fricke-fixed equation 16t² = 1. That asymmetry between the two families was not in the
hand estimate and is recorded as observed, without interpretation.

## 4. Tier statement

- **Exact** (integer / Fraction / sympy): T_n from the certificate; v², τ, v^⊥, reduction, D; the
  determinant identity; the stage-0 identities; the relation 1/z = αt + β + γ/t as PASS(40) (a
  finite order, evidence and not proof beyond it).
- **Numeric recognition, Tier B:** every value of t and z and every minimal polynomial. Fitted at
  one precision, re-checked at a strictly higher one; control S7 shows the re-check rejects a
  relative 10⁻⁵⁰ perturbation that the fit alone accepts.
- **Framework, cited not proved, Tier B:** Dolgachev 1996 §7 (read, hash-pinned in
  `docs/literature/MANIFEST.md`): for M_n-polarized K3 surfaces the period domain is H/Γ₀(n)+ with
  T = U ⊕ ⟨2n⟩. The further step — an integral class orthogonal to the period is of type (1,1),
  hence algebraic, so at such τ the member has ρ = 20 and T_X = v^⊥ — is the Lefschetz (1,1) theorem
  plus the definition of T_X; it is standard but is **not** among the statements the MANIFEST pins
  from Dolgachev (Thm 7.1, 7.3, 7.5, (M_n)^⊥). The checker computes the lattice side only; this
  link is what turns "B(v, ω) = 0" into "ρ = 20".
- **Caveat on the (−2)-vector rows.** Dolgachev Thm 7.3 (pinned) removes the (−2)-walls from the
  ample locus. The rows s7 z = 1/27, s7 z = −1 and s10 z = 1/16 are exactly (−2)-vector points and are
  also singular points of the operator, so "ρ = 20, T_X = v^⊥" there refers at best to a
  pseudo-ample / resolved surface; those rows are recorded as lattice arithmetic only.
- **Tier L elsewhere:** LeanMaster `docs/STREAM8_WHICH_K3.md` §G10 and `DualScaleDyons/FrickeRepair.lean`
  (commit 4109a51 — the commit that introduces both files; read as source, no Lean build run): ρ = 20 ⇔ rank-2 positive definite T(X);
  the Shioda–Inose / CM-locus statement is quoted there from Huybrechts, not proved there or here.
  Both cross-repo citations (LeanMaster 4109a51, Stream 1 3a96018) are re-verified at run time: each
  cited path must exist at the cited commit and contain the cited name (certificate field
  `external_citations_verified_at_run_time`; both VERIFIED in this run).

## 5. Controls (46/46 behaved as required; each names the clause that fired)

R (real data): non-CM τ (a cubic irrational; an imaginary part π/7) yields no primitive integer
vector with x ≤ 400 at either level — a bounded statement. **Wrong level, family-level (R2):** the
s7 relation run over the n = 10 lattice fires the Fricke-consistency gate on 179/182 vectors and the
distinct-z count goes to 114/182 against 71/180 at the right level; the s10 relation over the n = 7
lattice fires it on 179/180 vectors, 118/180 against 69/182. At the wrong level the same-z ⇒
same-form count is 3 (s7 relation) and 0 (s10 relation): that check is **not** a reliable
wrong-level detector and is reported, not asserted. R2x records why the earlier point-wise
wrong-level control was withdrawn: τ = i/√10 is a genuine CM point of the n = 7 lattice,
v = (10, −7, 0), −v² = 140. The C1 loci are all reproduced; Stream 1's two vectors give z = −1
(D = −7) and z = ∞ (D = −3). **R5:** the LeanMaster commit cited in the first draft (ede49f0) is
reported PHANTOM by the citation check (one path absent, the other without §G10); 4109a51 is VERIFIED.

S (tamper): non-orthogonal kernel, v² > 0 and v² = 0, index-2 kernel, non-primitive v, dependent
basis, relation with β + 1 (locus match), precision controls (60/90 digits agrees with the
production precision; a relative 10⁻⁵⁰ perturbation is rejected; verify ≤ fit precision is
refused). **S8:** merged z-groups make both same-z gates fire; α + 1 fires the Fricke gate on 51/53
vectors, while β + 1 does not (a constant shift of 1/z is Fricke-invariant — scope stated, that tamper
is S6's). **S9:** deleting rows makes the conjugates diagnostic drop (2/2 → 1/2). **S10:** the citation
check on this repo: absent path and absent name → PHANTOM, present → VERIFIED.

Clauses with no tamper control, stated: `det_identity_fails`, `TX_not_even`,
`TX_not_positive_definite` are unreachable by construction for v² < 0 in an even lattice of
signature (2,1) and stand as assertions; `round_trip_fails` is exercised only on its passing side (R0).

## 6. Not claimed

- that rho = 20 is a selection criterion of the program: the rho = 20 cut is NOT adopted; adopting it is an open T0 decision, and nothing here scores or ranks a candidate
- that any member of either family is singled out or preferred: this is a table of lattice/modular arithmetic
- that the table is complete at any discriminant: the enumeration window is logged and is not shown to be a fundamental domain
- that any z-value IS the algebraic number recorded: every minimal polynomial is a numeric recognition, fitted at DPS_FIT digits and re-checked at DPS_VERIFY digits (Tier B)
- that the step from 'v.omega = 0' to 'rho = 20, T_X = v^perp' is proved here: it is the cited framework (Dolgachev 1996 sec 7 period domain, read and pinned, plus the Lefschetz (1,1) theorem, standard and not among the pinned statements; Tier B). The checker computes the lattice side only
- that a smooth M_n-polarized member with rho = 20 sits at the (-2)-vector rows: Dolgachev Thm 7.3 (pinned) removes the (-2)-walls from the ample locus, and those rows include C1 singular loci of the operator; 'T_X = v^perp' there refers at best to a pseudo-ample / resolved surface and is recorded as lattice arithmetic only
- anything certified about T(cooper_s10): C2_cooper_s10_v4_DRAFT.json is DRAFT by T0 ruling; every s10 row carries LATTICE_CERT_DRAFT and is advisory
- any Kodaira fibre type at any locus (CLAUDE.md ledger item 3): the loci are elliptic points of the modular curve and are treated only as such
- any physical reading whatsoever (VISION sec 1.3; Tier C blocked, F5b)

## 7. Changes after independent review (2026-09-21)

An independent reviewer reproduced the relation, the enumeration counts, all reduced forms and
discriminants, and every minimal polynomial by a separate code path, and asked for four fixes.
All four are made; none changes a row that was already in the table.

1. LeanMaster commit hash corrected (ede49f0 → 4109a51) in checker, certificate and brief; the
   wrong hash was a phantom-artifact citation (standing rule 4). It is now a real known-bad (R5),
   and citations are verified at run time.
2. The same-z headline check had no control able to fail: S8 added; a second same-z gate on
   (−v², div v) and the Fricke-consistency gate added, each with a firing control.
3. R2 did not test the level: replaced by the family-level control above (R2, R2x).
4. Input sha256 added to the certificate.

Reviewer's notes also taken: Lefschetz / Thm 7.3 caveat (§4, §6); s10 prediction clause tagged
advisory and the trivial clauses named (§3); numeric clustering instead of string keys. One
change goes beyond the review: the 8 s10 rows at D = −800 are now recognised (degree 12). Raising
the second tier to 320/420 digits recognised seven of them; the eighth (v = (1, −20, 0), |1/z| ≈ 7·10³)
exposed a defect — powers of a large value overran the digits carried into the LLL matrix — fixed
by recognising the inverse when the modulus exceeds 1. The degree-12 polynomial agrees with the one
the reviewer found independently by PSLQ at 700 digits (their coefficients for 1/z, reversed). A
diff of all 140 rows before and after that fix shows this one row as the only change.

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: checkers/test_CM_points_rho20_controls.py (46 controls) + DPS re-check; independent reviewer agent (separate code path) | Reviewed-by: N
