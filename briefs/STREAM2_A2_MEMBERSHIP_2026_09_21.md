# Stream 2 brief: A2 membership in the cooper_s7 / cooper_s10 M_n-polarized families (2026-09-21)

**Status: RECORD, NOT A GATE.** The rho = 20 cut is not adopted by the program; adopting it is an open T0 decision. `K3_CRITERIA.md` is unchanged, nothing is scored, no candidate or family member is ranked or preferred. This is lattice / modular arithmetic, Tier B at best, with no physical reading.

This file is rendered from `data/certificates/A2_MEMBERSHIP.json` by `python3 checkers/check_A2_membership.py --brief` (function `render_brief`); numbers are looked up in the certificate, not typed. Code identity: f091e43. The checker imports `checkers/check_CM_points_rho20.py` and does not duplicate it; the sha256 of every code and data file used is in the certificate under `inputs.sha256` (16 files).

## Question

LeanMaster's theorem `smallest_black_hole` (`DualScaleDyons/AttractorCharges.lean`, read as source at commit `4109a51`, citation status VERIFIED, no Lean build run; the theorem name is LeanMaster's and is quoted as an identifier only) states `reducedForms 3 = [(1, 1, 1)]`: the one reduced form of discriminant -3 is A2, Gram [[2,1],[1,2]]. The checker recomputes that list and re-verifies the citation at run time. Does A2 occur as v^perp for a primitive v of negative norm in T_n = U + <2n>, for n = 7 (cooper_s7) and n = 10 (cooper_s10)? Within the cited framework (Dolgachev 1996 sec 7, read and hash-pinned; Lefschetz (1,1), standard and not among the pinned statements) that is the condition for the M_n-polarized family to contain a point whose transcendental lattice is A2. The checker computes the lattice side only.

## Result

| family | n | A2 | clause that fired | scope |
|---|---|---|---|---|
| cooper_s7 | 7 | **PRESENT** | `explicit_vector_with_target_form` | existence (one explicit exact vector suffices) |
| cooper_s10 (ADVISORY, lattice cert DRAFT) | 10 | **ABSENT** | `D_not_square_mod_4n` | ALL primitive v of negative norm (exact congruence, leg A) |

Cautious wording, Tier B: **the M_7-polarized family (Dolgachev moduli space X_0(7)+; cooper_s7 is its period operator) contains a point whose transcendental lattice is A2, and in the s7 coordinate that point is z = infinity** - a singular point of L3, where the explicit projective model is not examined (see Not claimed). The lattice statement is exact: T_7 contains the primitive vector v = (14, -14, -5) with -v^2 = 42, div(v) = 14, v^perp with Z-basis [[1, 1, 0], [0, 5, 1]] and Gram [[2, 5], [5, 14]], which Gauss-reduces to (1, 1, 1).
**T_10 = U + <20> contains no such vector**: -3 mod 40 = 37 is not among the squares mod 40, [0, 1, 4, 9, 16, 20, 24, 25, 36]. The s10 statement is arithmetic of the lattice recorded in the DRAFT certificate `C2_cooper_s10_v4_DRAFT.json` and is advisory.

### Why the n = 10 negative is not "not found within a bound"

Leg (A) of the checker covers all primitive v. With G = Gram(T_n), d = div(v), K = v^perp with basis u1, u2 and c = u1 x u2: (i) det(U^T G U) = c^T adj(G) c and (ii) (Gv)^T adj(G) (Gv) = det(G) v^T G v are checked symbolically (sympy, generic G); (iii) c = +-Gv/d because both are primitive and Euclidean-orthogonal to u1, u2 - this step is a three-line argument in the checker docstring, not a machine proof; (iv) with x = d x', y = d y', beta = 2nz/d, sympy gives D = beta^2 + 4n x'y'. So D is a square mod 4n for every v (the Heegner condition at level n). The squares mod 4n are found by exhaustion. The converse is constructive: each beta with beta^2 = D mod 4n gives a vector, and every such vector in the table is verified exactly. Stage-0 identities: i_det_UtGU_equals_ct_adjG_c = True, ii_Gv_adjG_Gv_equals_detG_vGv = True, detTn_is_minus_2n = True, iv_D_equals_beta2_plus_4n_xp_yp = True.

Leg (B), bounded and stated as such: all primitive negative-norm v with |x|, |y|, |z| <= 80 (145465 vectors at n = 7, 121667 at n = 10). The determinant identity held on 145465 and 121667 of them; the congruence D = (2nz/d)^2 mod 4n is checked on each; violations counted over both families, all clauses: 0. no vector with D = -3 among 121667 in the box |coords| <= 80.

## The n = 7 point

- tau = -5/14 + i*sqrt(3/196) (exact). Every A2 vector in the box has (-v^2, div) in [[42, 14]]; the exact necessary conditions allow only [[42, 14]].
- The z statement rests on two things. (a) The relation 1/z = 49 t + 13 + 1/t (t the level-7 eta quotient), certified by `T3.modular_leg` to q-order 40 only: **PASS(40)**, a finite order, evidence and not a proof. (b) The numeric evaluation of t at tau.
- z = **infinity**. given the relation (PASS(40)), Tier B numeric recognition of 1/z = 0: |1/z| < 10^-(dps-20) at 120 and at 200 digits; log10 |1/z| = -144.8 at 120 digits, -224.2 at 200 digits.
  Exact support: with (alpha, beta, gamma) = (49, 13, 1), alpha t^2 + beta t + gamma is proportional to the recognised minimal polynomial of t, `49*t**2 + 13*t + 1` (itself a Tier B numeric recognition): True.
- Finite singular loci of the C1 certificate: ['-1', '1/27']. The A2 point is a finite singular locus: **False**. It is a singular point of L3 on P^1: **True** - exponents ['2/3', '1', '4/3'] at z = infinity in `L3_RIEMANN_SCHEME.json` (denominator lcm 3).
- Exact integer search (entries up to 30): tau is fixed by [[2, 1], [-7, -3]] in Gamma_0(7) (trace -1), so it is an elliptic point of order 3; that order equals the exponent denominator: True.
- Bounded: the 2 A2 vectors of the P2 window (CM.enumerate_vectors(n, 42), Im tau >= 1/20), [[14, -14, -5], [14, -14, 5]], share one value of 1/z: True.
- "An" versus "the": the Fricke image of v is (14, -14, 5) (exact; its v^perp reduces to (1, 1, 1)). The number of x mod 7 with x^2 + x + 1 = 0 is 2, which is the standard count of order-3 elliptic points of Gamma_0(7) (standard formula, cited not proved, not among the pinned sources). Numerically (Tier B) t differs at the two points: True, and 1/z agrees: True. So tau is AN order-3 elliptic point of Gamma_0(7) - one of a Fricke-swapped pair - and THE order-3 point of X_0(7)+, the curve z lives on.

So the hand estimate's last sentence ("it should not be one of the singular loci") holds for the finite loci and fails for the projective line: the A2 point is the order-3 elliptic point of X_0(7)+, which is the third singular point of the operator, z = infinity. This was already on record in Stream 1: the docstring of `g3_fixes` (`ModularAction.lean` at `3a96018`, citation status VERIFIED) says that (14,-14,5) corresponds to the order-3 elliptic point of X_0(7). Consequence recorded in `not_claimed`: what is established is a point of the period domain; whether the explicit Almkvist-van Straten model has a smooth fibre there is not examined. No Kodaira reading is made (ledger item 3).

## Hand estimate, scored

orchestrator's hand estimate, issued UNVERIFIED; scored here. Its last sentence ('it should not be one of the singular loci') is scored under two readings: the finite loci of the C1 certificate, and the singular points of L3 on P^1 including z = infinity.

| clause | outcome |
|---|---|
| det(v^perp) = &#124;v^2&#124; * 2n / d^2 (asserted on every box vector and witness; leg A i-iii) | confirmed |
| n = 7: D = -3 forces d = 14, -v^2 = 42 | confirmed |
| the example v = (14,-14,5) has v^perp = A2 | confirmed |
| A2 occurs for n = 7 | confirmed |
| n = 10: z^2 = -3 mod 40 has no solution | confirmed |
| A2 does not occur for n = 10 | confirmed |
| Heegner form of the criterion: -3 is a square mod 4n for n = 7 and not for n = 10 | confirmed |
| the n = 7 A2 point is not one of the FINITE singular loci of the C1 certificate | confirmed |
| the n = 7 A2 point is not a singular point of L3 at all | **REFUTED** |

Outcome: CONFIRMED except 1 clause(s): the n = 7 A2 point is not a singular point of L3 at all.

## Discriminants admitted, -100 <= D < 0

Criterion (D square mod 4n, all v) and box enumeration agree on both inclusions for both n: True (computed row by row; either disagreement also stops the run, clauses `enumeration_outside_criterion`, `criterion_not_reached_in_box`). The second inclusion is bounded by the box. Imprimitive forms are included. The certificate also lists, per D, the lattice classes seen in the box and among the witnesses; those lists are not claimed complete (control S5 exhibits a class of an admitted D that is not seen).

| D | fundamental | n = 7 | n = 10 |
|---|---|---|---|
| -3 | yes | yes | - |
| -4 | yes | - | yes |
| -7 | yes | yes | - |
| -12 | no | yes | - |
| -15 | yes | - | yes |
| -16 | no | - | yes |
| -19 | yes | yes | - |
| -20 | yes | yes | yes |
| -24 | yes | yes | yes |
| -27 | no | yes | - |
| -28 | no | yes | - |
| -31 | yes | yes | yes |
| -35 | yes | yes | - |
| -36 | no | - | yes |
| -39 | yes | - | yes |
| -40 | yes | yes | yes |
| -44 | no | - | yes |
| -47 | yes | yes | - |
| -48 | no | yes | - |
| -52 | yes | yes | - |
| -55 | yes | yes | yes |
| -56 | yes | yes | yes |
| -59 | yes | yes | - |
| -60 | no | - | yes |
| -63 | no | yes | - |
| -64 | no | - | yes |
| -68 | yes | yes | - |
| -71 | yes | - | yes |
| -75 | no | yes | - |
| -76 | no | yes | yes |
| -79 | yes | - | yes |
| -80 | no | yes | yes |
| -83 | yes | yes | - |
| -84 | yes | yes | yes |
| -87 | yes | yes | - |
| -91 | yes | yes | - |
| -95 | yes | - | yes |
| -96 | no | yes | yes |
| -100 | no | - | yes |

Admitted by both: [-20, -24, -31, -40, -55, -56, -76, -80, -84, -96]; of these fundamental: [-20, -24, -31, -40, -55, -56, -84].

## Controls (`checkers/test_A2_membership_controls.py`, each reports the clause that fired)

R1 real known-negative A2 at n = 10 (`D_not_square_mod_4n`); R2 (1,0,1) at n = 7, same clause; R3 non-vacuity both ways; R4 Stream 1's (14,-14,5) and the P2 certificate; R5 stabilizer order 3 vs trivial. S1a the Gauss discriminant lattice G0N of Stream 1's `no_isometry_G0N_TN` fed in place of T_n is refused on `lattice_not_even` (optional path) and, through the PRODUCTION call with the registry entry swapped, on `lattice_leg_refused`; S1b an even lattice with the Gauss determinant is refused on `lattice_level_mismatch` (optional path) and on `no_level_coordinate` (production path), and the control computes that accepting it would have flipped the s7 headline. S2 wrong-level criterion; S2x records that "mod 2n" is no tamper at odd n (a first-draft control that rightly did not fire); S3 small box; S4 tampered witness; S5 PRESENT is not awarded on D alone; S6 wrong-n congruence, per vector and counted over a box; S7 tampered relation (`w_not_zero`); S8 non-reduced target; S9 phantom citation; S10 the exit-code gate does not read a failed boolean as the count 0; S11 the brief renderer follows the certificate.

## Not claimed

- that rho = 20 is a selection criterion of the program: the rho = 20 cut is NOT adopted; adopting it is an open T0 decision, and nothing here scores, ranks or prefers a candidate or a member of a family
- that agreement between the binary-form route and the modular route corroborates anything: LeanMaster docs/STREAM8_WHICH_K3.md sec G10 (read as source) states that the binary-form enumeration and the modular side are the same computation in two languages (Shioda-Inose), so their agreement is forced, not corroboration. The Heegner congruence and the lattice enumeration of this checker agree for the same reason
- that the step from 'v in T_n, v.omega = 0' to 'a member of the family has rho = 20 and T_X = v^perp' is proved here: it is the cited framework (Dolgachev 1996 sec 7, read and pinned; Lefschetz (1,1), standard, not among the pinned statements). Tier B. The checker computes the lattice side only
- that the explicit Almkvist-van Straten geometric family has a smooth fibre at the point found: for n = 7 the A2 point is z = infinity, which is a regular singular point of L3 (exponent denominators 3 in L3_RIEMANN_SCHEME.json) and an order-3 elliptic point of Gamma_0(7) (one of two, tau = (+-5 + i sqrt 3)/14, which the Fricke involution swaps, so THE order-3 point of X_0(7)+). What is established is a point of the period domain, not a fibre of a specific projective model
- that z = infinity IS the value at the A2 point: the statement rests on (a) the relation 1/z = alpha t + beta + gamma/t, certified by T3.modular_leg to a finite q-order only (PASS(N), N = relation_order_checked in the point record), and (b) |1/z| below 10^-(dps-20) at two precisions (Tier B numeric recognition), supported by an exact proportionality that itself rests on a numerically recognised minimal polynomial of t
- that the singular-point reading of the hand estimate was unanticipated program-wide: the docstring of Stream 1's g3_fixes (ModularAction.lean, read as source) already says that (14,-14,5) corresponds to the order-3 elliptic point of X_0(7)
- that the per-discriminant form lists are complete: they record what the stated box and the constructed witnesses contain. Only the discriminant criterion covers all v
- anything certified about T(cooper_s10): C2_cooper_s10_v4_DRAFT.json is DRAFT by T0 ruling; the s10 negative is arithmetic of U + <20> as that draft records it, and is advisory
- any Kodaira fibre type at any locus (CLAUDE.md ledger item 3); elliptic points are treated only as elliptic points of the modular curve
- any physical reading whatsoever (VISION sec 1.3; Tier C blocked, F5b). The LeanMaster theorem name is quoted as an identifier only

## For T0

Nothing here needs a ruling. If the rho = 20 question is ever taken up, the two facts to carry are: (1) A2 is PRESENT at n = 7 and ABSENT at n = 10 (s10 advisory); (2) the n = 7 A2 point is z = infinity (relation PASS(40)), the order-3 elliptic point of X_0(7)+, not a generic member.

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: check_A2_membership.py + test_A2_membership_controls.py | Reviewed-by: N
