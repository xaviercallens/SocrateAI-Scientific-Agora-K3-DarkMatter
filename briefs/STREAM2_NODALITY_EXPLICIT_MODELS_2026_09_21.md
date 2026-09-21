# Stream 2 brief: singular members of explicit models of the cooper_s7 / cooper_s10 pencils, against the lattice side (2026-09-21)

**Status: RECORD, NOT A GATE.** Tier **B**. Nothing is scored or ranked; `K3_CRITERIA.md` is unchanged; the rho = 20 cut and T3 are not adopted. All cooper_s10 output is **ADVISORY** (flags ['LATTICE_CERT_DRAFT']: its lattice certificate is DRAFT). This is algebraic geometry of explicit surfaces; it carries no physical reading. No Kodaira reading is made (ledger item 3): the singular objects below are points of **surfaces** (members of a pencil), named each time.

Rendered from `data/certificates/NODALITY_EXPLICIT_MODELS.json` by `python3 checkers/check_nodality_explicit_models.py --brief`; code identity `v0.3.7-c1-mirror-integrality-14-gb636f08`; certificate verdict **PASS(10)** (integrity gates only: 8/8 hold). The hand estimate is scored in section 6 and is not part of that verdict.

## 1. Question

The lattice side (`CM_POINTS_RHO20.json`, Tier B) places the finite singular points of L3 at these vectors of T_n:

| family | z | -v^2 | div v | reflective | D |
|---|---|---|---|---|---|
| cooper_s7 | -1 | 2 | 2 | True | -7 |
| cooper_s7 | 1/27 | 2 | 1 | True | -28 |
| cooper_s7 | infinity | 42 | 14 | False | -3 |
| cooper_s10 (ADVISORY) | -1/4 | 4 | 2 | True | -20 |
| cooper_s10 (ADVISORY) | 1/16 | 2 | 1 | True | -40 |
| cooper_s10 (ADVISORY) | infinity | 20 | 10 | True | -4 |

The orchestrator's hand estimate (UNVERIFIED when issued): at a (-2)-vector the polarized model acquires one ordinary double point (an A1 point of the surface); at the other points no such statement is made. The test asked for: an explicit model, no lattice, no monodromy.

## 2. Models, and the constant-term gate

A Laurent polynomial P with CT(P^n) = s(n) gives the pencil {P = lambda}, z = 1/lambda. No P is used before the identity is checked exactly. Almkvist-van Straten (arXiv:2103.08651, pinned; read) describe the surfaces as six hyperplane sections of G(2,6) and four (1,1) sections of P^3 x P^3 and refer to Gorodetsky for Laurent polynomials; they print no equations, so their models are **not explicit enough to use** and are not used.

| model | family | P = N / (xyz), N = | provenance | CT identity |
|---|---|---|---|---|
| s10_a | cooper_s10 | `x**2*y**2*z**2 + x**2*y**2*z + x**2*y*z**2 + x**2*y*z + x*y**2*z**2 + x*y**2*z + x*y*z**2 + 2*x*y*z + x*y + x*z + x + y*z + y + z + 1` | derived here: C(n,k)^4 = [x^k y^k z^k (xyz)^-k] of ((1+x)(1+y)(1+z)(1+1/(xyz)))^n | PASS(10) |
| s7_a | cooper_s7 | `x**2*y*z + 2*x*y**2*z + 3*x*y*z**2 + 4*x*y*z + x*y + x*z**3 + 3*x*z**2 + 3*x*z + x + y**3*z + 3*y**2*z**2 + 4*y**2*z + y**2 + 3*y*z**3 + 8*y*z**2 + 7*y*z + 2*y + z**4 + 4*z**3 + 6*z**2 + 4*z + 1` | written from recollection of the literature on Landau-Ginzburg models of the Fano threefold of degree 14 (NOT fetched, NOT pinned in docs/literature/MANIFEST.md); admitted ONLY because leg CT passes | PASS(10) |
| s7_b | cooper_s7 | `x**2*y**2*z**2 + 2*x**2*y**2*z + x**2*y**2 + 2*x**2*y*z**2 + 4*x**2*y*z + 2*x**2*y + x**2*z**2 + 2*x**2*z + x**2 + x*y**2*z**2 + 2*x*y**2*z + x*y**2 + 2*x*y*z**2 + 4*x*y*z + 3*x*y + x*z**2 + 2*x*z + 2*x + y + 1` | derived here from the closed form: C(n,j)^2 from (1 + x(1+y)(1+z)^2)^n (1+1/x)^n at x^j x^-j, then [y^n](1+y)^(n+j) = C(n+j,n), [z^n](1+z)^(2j) = C(2j,n) | PASS(10) |

Real known-bads (refused before any geometry, clause named):

- `franel_polynomial_for_s10`: REFUSED, clause `ct_mismatch`, first mismatch at n = 2 (CT [1, 2, 10, 56] against [1, 2, 18, 164]) - exponent confusion: ((1+x)(1+y)(1+1/(xy)))^n has constant term sum C(n,k)^3, not sum C(n,k)^4; the two sequences share n = 0 and n = 1, so a CT check of order 1 would ACCEPT this P
- `s10_polynomial_for_s7`: REFUSED, clause `ct_mismatch`, first mismatch at n = 1 (CT [1, 2, 18, 164] against [1, 4, 48, 760]) - cross-family: the s10 polynomial offered for the s7 sequence
- `s7_a_misremembered`: REFUSED, clause `ct_mismatch`, first mismatch at n = 1 (CT [1, 3, 31, 399] against [1, 4, 48, 760]) - s7_a with the square on (z+1) dropped: the kind of slip a formula written from recollection invites; this is why s7_a is admitted on leg CT alone
- `s7_missing_square`: REFUSED, clause `ct_mismatch`, first mismatch at n = 1 (CT [1, 2, 6, 20] against [1, 4, 48, 760]) - the s7_b derivation with the square on (1+z) forgotten: gives sum C(n,j)^2 C(n+j,n) C(j,n), a different sequence

PASS(10) is a finite order: what the machine checked is n <= 10, which is evidence and not a proof. For the models whose provenance reads 'derived here' the provenance column is a hand derivation valid for every n (a hand argument, not machine-checked); the model 'written from recollection' rests on the finite order alone. Known-bads that survive n = 1 and are refused later: {'franel_polynomial_for_s10': 2}; control S2 shows a wrong P that passes at order 3 and is refused at order 4. The closed forms are cross-checked against `refs/recurrences_v1.json` for n <= {'cooper_s10': 9, 'cooper_s7': 9} only (that is all the register holds); beyond that the sequence is the closed form itself. Control S9 tampers a refs term (`refs_mismatch`).

## 3. Torus critical points (exact; complete for the torus with P != 0)

Groebner basis with a Rabinowitsch variable; the ideal is zero-dimensional in every model, so the list is complete for (C*)^3 with P != 0. Hessian rank 3 means a nondegenerate critical point: the member {P = value} has an A1 point there and the total space of the pencil is smooth there.

| model | critical point | value | z | Hessian rank | Morse | coordinates rational |
|---|---|---|---|---|---|---|
| s10_a | (-I, -I, -I) | -4 | -1/4 | 3 | True | False |
| s10_a | (I, I, I) | -4 | -1/4 | 3 | True | False |
| s10_a | (1, 1, 1) | 16 | 1/16 | 3 | True | True |
| s7_a | (6, 3/2, 1/2) | 27 | 1/27 | 3 | True | True |
| s7_b | (1/4, 5/4, 5/3) | 27 | 1/27 | 3 | True | True |

- s10_a: torus critical points per z = {'-1/4': 2, '1/16': 1}; certified loci ['-1/4', '1/16']; loci with no torus critical point: none; critical values outside the loci: none; clauses: none.
- s7_a: torus critical points per z = {'1/27': 1}; certified loci ['-1', '1/27']; loci with no torus critical point: ['-1']; critical values outside the loci: none; clauses: ['certified_locus_without_torus_critical_point'].
- s7_b: torus critical points per z = {'1/27': 1}; certified loci ['-1', '1/27']; loci with no torus critical point: ['-1']; critical values outside the loci: none; clauses: ['certified_locus_without_torus_critical_point'].

**z = infinity.** In every model the torus critical points with P = 0 form a positive-dimensional set ({'s10_a': True, 's7_a': True, 's7_b': True}), and the member lambda = 0 has non-isolated singular points (control R8). Nothing is said here about z = infinity: the order-3 statement of the lattice side is neither supported nor contradicted.

## 4. The (2,2,2) closure in P^1 x P^1 x P^1 (s7_b and s10_a)

Where N has degree at most 2 in each variable, the closure of {P = lambda} is a (2,2,2) surface. For each lambda of a logged finite list (1/z for every rational z of the lattice certificate, the probes, and an integer window) all singular points of that surface are computed in eight charts, with the Hessian rank of the local equation. Signature = [number of singular points, sorted Hessian ranks]. The optional second CAS (Singular) adds total Tjurina numbers, and Milnor / Tjurina numbers at the rational singular points.

- **s10_a**: 57 members scanned (lambda from -64 to 5776); generic signature [6, [3, 3, 3, 3, 3, 3]]; generic total Tjurina number 6; point counts of the two CAS disagree on 0 members.
  - lambda = -4 (z = -1/4): signature [8, [3, 3, 3, 3, 3, 3, 3, 3]], kinds ['new_torus_singular_points'], z is a certified locus: True; total Tjurina 8; rational singular points by (corank, Milnor number): ['A1', 'A1', 'A1', 'A1', 'A1', 'A1']; non-rational points are not sent to the second CAS.
  - lambda = 16 (z = 1/16): signature [7, [3, 3, 3, 3, 3, 3, 3]], kinds ['new_torus_singular_point'], z is a certified locus: True; total Tjurina 7; rational singular points by (corank, Milnor number): ['A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A1'].
- **s7_a**: leg not run, clause `not_a_222_surface`: the boundary of this model is not examined.
- **s7_b**: 54 members scanned (lambda from -64 to 125); generic signature [7, [2, 3, 3, 3, 3, 3, 3]]; generic total Tjurina number 10; point counts of the two CAS disagree on 0 members.
  - lambda = -1 (z = -1): signature [5, [1, 2, 3, 3, 3]], kinds ['boundary_points_merge'], z is a certified locus: True; total Tjurina 11; rational singular points by (corank, Milnor number): ['A1', 'A1', 'A1', 'A4', 'D4'].
  - lambda = 2 (z = 1/2): signature [7, [2, 2, 3, 3, 3, 3, 3]], kinds ['boundary_point_hessian_rank_drops'], z is a certified locus: False, clause `model_special_but_operator_regular`; total Tjurina 11; rational singular points by (corank, Milnor number): ['A1', 'A1', 'A1', 'A1', 'A1', 'A2', 'A4'].
  - lambda = 27 (z = 1/27): signature [8, [2, 3, 3, 3, 3, 3, 3, 3]], kinds ['new_torus_singular_point'], z is a certified locus: True; total Tjurina 11; rational singular points by (corank, Milnor number): ['A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A1', 'A4'].

**Leg C (second CAS; complete, not a scan).** Primary decomposition of the relative singular scheme over Q[lambda], chart by chart: the members whose total Tjurina number differs from the generic one are exactly the roots of the eliminants of the vertical associated primes (finite module over a PID = free + torsion; standard, used as an argument, not machine-checked).

- s10_a: total Tjurina number differs from generic exactly at lambda in ['-4', '16']; non-isolated singular points exactly at lambda in ['0']; generic member over Q(lambda): 6 singular points, total Tjurina number 6. Against leg K: agree = True. So no other scanned member (the other rational CM values of the lattice certificate included) is special on this model in this sense.
- s7_b: total Tjurina number differs from generic exactly at lambda in ['-1', '2', '27']; non-isolated singular points exactly at lambda in ['0']; generic member over Q(lambda): 7 singular points, total Tjurina number 10. Against leg K: agree = True. So no other scanned member (the other rational CM values of the lattice certificate included) is special on this model in this sense.

Plain reading of what is observed on s7_b, the model where the boundary is examined:

- z = 1/27: 1 new A1 point (Hessian rank [3]), on the torus; the other 7 singular points keep the generic Hessian ranks. s7_a (torus only): 1 Morse critical point over z = 1/27. Total Tjurina number change +1.
- z = -1: **no new singular point.** The number of singular points goes 7 -> 5: singular points of the generic member merge, and the lowest Hessian rank on the member is 1 (second CAS: non-A1 labels of this member that the generic member does not have: ['D4']; the generic member already has ['A4']). Total Tjurina number change +1, against +1 at z = 1/27.
- z = 1/2: same number of singular points (7), Hessian ranks [2, 3, 3, 3, 3, 3, 3] -> [2, 2, 3, 3, 3, 3, 3], total Tjurina number change +1, non-A1 labels the generic member does not have: ['A2'], and **L3 is regular there**. A change of signature is therefore NOT a detector of singular points of the operator (control R4). On the lattice side z = 1/2 is a CM point of a non-reflective vector (-v^2 = 42, div 7, D = -12).

and on s10_a (ADVISORY): z = 1/16: 1 new A1 point on the torus (rational: [True]); z = -1/4: **2 new A1 points** on the torus (rational: [False, False]; coordinates in Q(i), exchanged by conjugation: see the table of section 3); the 6 singular points of the generic member keep their Hessian ranks at both values; total Tjurina number changes +1 and +2.

## 5. A reading through root systems - HYPOTHESIS, not checked

Exact integer arithmetic (in the certificate, control S7): in the D4 root lattice take three mutually orthogonal roots e_i; the roots orthogonal to all three are [[-1, -1, -1, -1], [1, 1, 1, 1]] (one root up to sign), and A1^3 plus that root has index 2 in D4. In A2 the roots orthogonal to a given root: none. The sum of two orthogonal roots has norm -4.

If - and this is the unverified step - the singular points of a member correspond to roots among the algebraic classes orthogonal to the model's polarization, the observations would read: s7 z = -1, 3 singular points merging into one (new label ['D4']), as one new root glued to the old ones with index 2, where the lattice vector has div 2; s7 z = 1/27 and s10 z = 1/16, an isolated new A1, where the lattice vectors have div 1 and 1; s10 z = -1/4, 2 A1 points exchanged by conjugation, as a vector delta_1 + delta_2 of norm -4, where the lattice vector has -v^2 = 4, div 2; s7 z = 1/2, new label ['A2'], no new root orthogonal to the old one (none in A2), and the operator is regular there.

**This reading is post hoc.** It was written in this document AFTER the observations of section 4 and was built from them; the observations it accommodates are therefore fits, not tests, and are not counted as agreement. **Independent tests passed so far: 0.** A first real test would be a second compactification of the same pencil, or a boundary analysis of s7_a, with the expected local types written down BEFORE the computation. The identification of roots with classes on the surface is not computed here.

Thought experiment, kept as an aid to discussion only. Picture the pencil as a drum whose skin is re-tensioned as lambda moves. A (-2)-wall says: somewhere one cycle is pinched to a point. The lattice tells you THAT a cycle is pinched; it does not tell you WHERE on a given drawing of the drum the pinch shows. On one drawing (the torus chart) the pinch at z = 1/27 is in full view; the pinch at z = -1 happens at the rim, where old dents already sit, and what one sees is 3 dents running together. The drawing is not the drum: that is the content of the word 'birational' in section 8.

## 6. Hand estimate, scored

| clause | outcome | basis |
|---|---|---|
| s7_a: set of torus critical values (as z) equals the certified finite loci ['-1', '1/27'] | **REFUTED** | extra=[] missing=['-1'] |
| s7_b: set of torus critical values (as z) equals the certified finite loci ['-1', '1/27'] | **REFUTED** | extra=[] missing=['-1'] |
| s7_a: z = -1 comes from a (-2)-vector (div 2), so exactly one A1 point appears on the model | **NOT OBSERVED on the torus (boundary of this model not examined)** | torus critical points over z: 0, Morse: [] |
| s7_b: z = -1 comes from a (-2)-vector (div 2), so exactly one A1 point appears on the model | **literal clause FAILS ON THIS MODEL (no single new A1 point); NOT a refutation of the lattice side: total Tjurina number 10 -> 11 (change +1); M_n-polarized model open** | torus critical points over z: 0, Morse: []; closure signature [5, [1, 2, 3, 3, 3]] vs generic [7, [2, 3, 3, 3, 3, 3, 3]], kinds ['boundary_points_merge']; total Tjurina number generic 10, this member 11 (change +1) |
| s7_a: z = 1/27 comes from a (-2)-vector (div 1), so exactly one A1 point appears on the model | **confirmed on the torus (boundary of this model not examined)** | torus critical points over z: 1, Morse: [True] |
| s7_b: z = 1/27 comes from a (-2)-vector (div 1), so exactly one A1 point appears on the model | **confirmed ON THIS MODEL (torus and (2,2,2) closure); model-level, nothing about the M_n-polarized model** | torus critical points over z: 1, Morse: [True]; closure signature [8, [2, 3, 3, 3, 3, 3, 3, 3]] vs generic [7, [2, 3, 3, 3, 3, 3, 3]], kinds ['new_torus_singular_point']; total Tjurina number generic 10, this member 11 (change +1) |
| cooper_s7: behaviour at z = infinity | **NOT EXAMINED** | value-0 critical locus positive-dimensional in every model: {'s7_a': True, 's7_b': True} |
| s10_a: set of torus critical values (as z) equals the certified finite loci ['-1/4', '1/16'] **[ADVISORY]** | **confirmed** | extra=[] missing=[] |
| s10_a: z = -1/4 (-v^2 = 4, div 2): no prediction was made **[ADVISORY]** | **observed** | torus critical points over z: 2, Morse: [True, True]; closure signature [8, [3, 3, 3, 3, 3, 3, 3, 3]] vs generic [6, [3, 3, 3, 3, 3, 3]], kinds ['new_torus_singular_points'] |
| s10_a: z = 1/16 comes from a (-2)-vector (div 1), so exactly one A1 point appears on the model **[ADVISORY]** | **confirmed ON THIS MODEL (torus and (2,2,2) closure); model-level, nothing about the M_n-polarized model** | torus critical points over z: 1, Morse: [True]; closure signature [7, [3, 3, 3, 3, 3, 3, 3]] vs generic [6, [3, 3, 3, 3, 3, 3]], kinds ['new_torus_singular_point']; total Tjurina number generic 6, this member 7 (change +1) |
| cooper_s10: behaviour at z = infinity **[ADVISORY]** | **NOT EXAMINED** | value-0 critical locus positive-dimensional in every model: {'s10_a': True} |

Summary (model-level in every line; s10 ADVISORY). The clause '(-2)-vector => exactly one new A1 point' holds on: ['s7_a: z = 1/27 comes from a (-2)-vector (div 1)', 's7_b: z = 1/27 comes from a (-2)-vector (div 1)', 's10_a: z = 1/16 comes from a (-2)-vector (div 1)']. Its literal form fails on: ['s7_b: z = -1 comes from a (-2)-vector (div 2)']. It is not observed on the torus, boundary not examined, on: ['s7_a: z = -1 comes from a (-2)-vector (div 2)']. Where it fails, the outcome column records the change of the total Tjurina number, which is +1, the same as at the locus where the clause holds: the model shows a different local picture with the same total, and that is NOT a refutation of the lattice side. Whether the M_7-polarized model has an A1 point at z = -1 stays open, since neither model is the M_7-polarized one.

## 7. Controls

`checkers/test_nodality_explicit_models_controls.py`, 20 controls, each naming the clause that fired. Real: R1 4 wrong polynomials (`ct_mismatch`, no geometry computed; surviving n = 1: ['franel_polynomial_for_s10']); R2 cross-family both ways (`critical_value_not_a_certified_locus`); R3 (x-1)^3-type toy (`hessian_degenerate`, NOT Morse); R4 s7_b at lambda = 2 (`model_special_but_operator_regular`); R5 Morse toy with 4 critical points (non-vacuity); R6 non-isolated critical points (`critical_locus_not_zero_dimensional`); R7 `not_a_222_surface`; R8 the member at z = infinity (`singular_locus_not_isolated`); R9 the headline observations; R10 a scan list that omits special members (`complete_special_set_differs_from_scan`), and leg C on a shifted pencil finds members outside the scanned window. Tamper: S1, S2 (low-order CT accepts a wrong P), S3 tampered loci, S4 `probes_disagree_on_generic_signature`, S5 `singular_leg_not_run`, S6 `unlabelled`, S7 root arithmetic, S8 a critical value 10^-20 away from a certified locus is NOT matched (exact comparison), S9 tampered refs term (`refs_mismatch`), S10 this brief refuses to render from a certificate that no longer supports its sentences (`brief_prose_not_supported_by_certificate`).

Clauses with no control, stated: `solution_does_not_satisfy_equations` and `singular_output_unparsed` are exercised only on their passing side; a disagreement between the two CAS on point counts has not been provoked.

## 8. Not claimed

- anything about the minimal resolution of any member: an A1 point is observed on a birational model; nothing is proved about the smooth K3 surface
- that either model is the M_n-polarized model of Dolgachev 1996: the (2,2,2) closure carries one polarization class, and its singular points are not the (-2)-walls of M_n
- anything at the toric boundary of models that are not (2,2,2) (s7_a): not examined
- anything at z = infinity: the member P = 0 has non-isolated singular points in every model here; the order-3 statement of the lattice side is neither supported nor contradicted
- that a change of signature detects a singular point of the operator: s7_b at lambda = 2 is a real counterexample (control R4)
- completeness of leg K by itself: leg K examines a logged finite list of members.  Leg C (second CAS only) states which members have a total Tjurina number different from the generic one, by an argument that is standard but not machine-checked; a change of signature at constant total Tjurina number is not excluded by leg C
- the names A_k, D_4 beyond (Hessian corank, Milnor number) matched against Arnold's list (standard, cited not proved); Milnor and Tjurina numbers come from the optional Singular leg
- the reading of the s7 z = -1 and s10 z = -1/4 observations through root systems (brief section 5): the integer arithmetic is exact, the identification of those roots with classes on the surface is a hypothesis and is not checked here
- anything certified about cooper_s10: its lattice certificate is DRAFT; all s10 output is ADVISORY
- any Kodaira reading at any locus (CLAUDE.md ledger item 3): only singular points of surfaces are discussed
- that rho = 20 or T3 is a criterion of the program: neither is adopted; nothing is scored or ranked
- any physical reading whatsoever (VISION sec 1.3; Tier C blocked, F5b)

Tier statement: leg CT, leg T, leg Z, leg K are exact (integers, sympy over Q and Q(i); zero tests are structural or by minimal polynomial, no numeric recognition anywhere); they are Tier B because CT is a finite order, leg K is a finite list (leg C's completeness rests on an argument that is not machine-checked), and the link from a model's singular points to the lattice side is the cited framework, not a computation. Singular-point names rest on the optional second CAS plus Arnold's list (standard, cited not proved).

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: checkers/test_nodality_explicit_models_controls.py; optional second CAS (Singular) | Reviewed-by: N
