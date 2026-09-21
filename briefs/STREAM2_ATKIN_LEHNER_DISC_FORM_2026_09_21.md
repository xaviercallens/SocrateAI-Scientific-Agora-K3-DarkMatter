# Stream 2 brief: Atkin-Lehner group versus the discriminant form of T_n = U + <2n> (2026-09-21)

**Status: RECORD, proposal stage.** Gate T3 is not adopted; `check_T3_level_consistency.py` is not edited; the rho = 20 cut is not adopted; nothing is scored or ranked. Every cooper_s10 statement is **ADVISORY** (flag `LATTICE_CERT_DRAFT`: `C2_cooper_s10_v4_DRAFT.json` is DRAFT by T0 ruling). This is lattice and modular arithmetic, Tier B at best, with no physical reading of any kind.

Rendered from `data/certificates/ATKIN_LEHNER_DISC_FORM.json` by `python3 checkers/check_atkin_lehner_vs_disc_form.py --emit --brief`; numbers are looked up in the certificate, not typed. Code identity: da84a90 (HEAD at emit; this checker is uncommitted and is identified by its self-hash in `inputs.sha256`). Verdict: `AL_ACTION_ON_DISC_FORM_EXPLICIT - PASS(30) over n for legs O and W; PASS(40) inherited for every z-locus identification`.

**Orders of the finite checks.** Legs O and W: PASS(30) - finite sweep over n = 1..30; the rule m = -1 mod 2Q, +1 mod 2n/Q itself is symbolic in n (stage 0). Leg F: PASS(40) inherited - z is identified through the relation 1/z = alpha t + beta + gamma/t, fitted upstream to q-order 40 (check_CM_points_rho20); t and 1/z are Tier B numeric at 60 and 120 digits.

## 1. The flag, and what was missing

`ATKIN_LEHNER_ACTION_UNVERIFIED` (cooper_s10, `check_T3_level_consistency.py`) exists because the only evidence that the extra Atkin-Lehner involutions of Gamma_0(10)* are compatible with T = U + <20> was a COUNT, |O(q_A)| = |W(n)| (`spike_disc_form_vs_atkin_lehner.py`). Two groups of the same order need not be related at all. This task builds the map and tests it.

## 2. The map, through the action on periods (derived, not cited)

With omega(tau) = (1, -n tau^2, tau), B(v, omega(tau)) = y - n x tau^2 + 2 n z tau is a quadratic polynomial in tau. For g = [[A,B],[C,D]] of determinant Delta > 0 the pullback P -> (C tau + D)^2 P(g tau) / Delta is a linear map phi_g of T_n (x) Q. Stage 0 (sympy, symbolic n):

- `AL_shape_phi_entries_are_integer_polynomials`: True
- `fixed_vector_norm_is_minus_2det_over_n`: True
- `image_of_dual_generator_integral_off_w`: True
- `m_equals_1_plus_2nprime_bc_on_shape`: True
- `m_equals_2Qad_minus_1_on_shape`: True
- `multiplier_is_Qad_plus_nprime_bc`: True
- `phi_formula_is_the_pullback`: True
- `phi_gh_equals_phi_h_phi_g`: True
- `pullback_scales_norm_by_det_squared`: True
- `trace0_phi_equals_minus_reflection`: True

Consequences, all exact. (a) phi_g preserves v^2 and phi_{gh} = phi_h phi_g. (b) For the Atkin-Lehner shape [[Q a, b],[n c, Q d]], det Q, phi_g is an INTEGRAL isometry and acts on A = Z/2n by the multiplier m = Q a d + (n/Q) b c = 2 Q a d - 1 = 1 + 2 (n/Q) b c: **m = -1 mod 2Q and m = +1 mod 2n/Q**. That is the rule "-1 on the Q-part, +1 on the rest", with the 2-adic part made exact; it depends on Q only. (c) When the coset w_Q Gamma_0(n) contains a trace-0 element g, with fixed point tau_g and primitive fixed vector v, then **phi_g = - r_v**: the reflection r_v is integral and has multiplier -m_Q.

**The -1 ambiguity, stated.** -1 acts trivially on the period domain, so the action on the upper half plane only sees O(T_n)/{+-1}. Two lifts exist: the lift g -> phi_g (determinant +1) lands in O(q_A) and is a homomorphism; the reflection lift w_Q -> r_v is a homomorphism only modulo +-1 (controls R5, R6). O(q_A) itself = {m mod 2n : m^2 = 1 mod 4n} is derived from q(m g) = m^2/(2n) mod 2Z and re-derived by brute force over all multipliers for n = 1..30 (agreement everywhere: True; the variant "mod 2n" disagrees at n = [4, 8, 12, 16, 20, 24, 28]).

## 3. Lattice-level sweep, every n = 1..30, every Q || n (exact)

- `W_fricke_maps_to_minus_one_for_every_n`: True
- `W_image_equals_O_qA_for_every_n`: True
- `W_injective_into_O_qA_for_every_n`: True
- `W_kernel_modulo_pm1_is_1_and_fricke`: True

So w_Q -> m_Q is a group **isomorphism W(n) -> O(q_A)** at every n of the sweep, PASS(30) as a statement over n (set equality, not a count; multiplicativity checked on actual matrix products for every pair, independence of the representative checked on 9 representatives per class), with **Fricke w_n -> -1**. Modulo +-1 the kernel is {1, w_n}. This matches the source that is read and pinned (Dolgachev 1996 Thm 7.1, `docs/literature/MANIFEST.md`): the group in that theorem is Gamma_0(n)+, read in this repo as the extension by the Fricke involution only, and here Fricke is the one class whose reflection r_v acts on A by +1. Corroboration, read as source in the pinned text (`docs/literature/dolgachev_1996_mirror_lattice_polarized_k3.txt`, section 7, around lines 1078-1130; located by the reviewer, re-read for this revision): Gamma_0(n)+ is introduced there as the Fricke modular group, the proof of Thm 7.1 identifies the group with O(U + <2n>)^*, and it uses the same representation on binary forms as phi_g here. The derivation in section 2 stands on its own; the passage is corroboration, not the source of any number.

Not every w_Q has a reflection. (n, Q) with no trace-0 representative, decided by a complete residue search: [(10, 2), (12, 4), (14, 2), (15, 3), (20, 5), (21, 7), (24, 3), (26, 2), (28, 4), (30, 2), (30, 3), (30, 10)]. Among them, no fixed point in the upper half plane at all: [(12, 4), (14, 2), (15, 3), (20, 5), (21, 7), (24, 3), (28, 4), (30, 2), (30, 3), (30, 10)]. The map phi is defined for all of them; the fixed-point route is a cross-check where it exists.

## 4. The two families

**cooper_s7** - n = 7 (from `C2_cooper_s7_v5.json`, LIVE), group Gamma_0(7)+.

W(n) -> O(q_A): {'1': 1, '7': 13}; O(q_A) = [1, 13].

| v | v^2 | div v | D | fixed by (order of the element) | r_v multiplier | phi multiplier | z | exponent-denominator lcm (L3_RIEMANN_SCHEME) |
|---|---|---|---|---|---|---|---|---|
| (1, -1, 0) | -2 | 1 | -28 | w7 (2) | 1 | [13] | 1/27 | 2 |
| (2, -4, -1) | -2 | 2 | -7 | w7 (2) | 1 | [13] | -1 | 2 |
| (2, -4, 1) | -2 | 2 | -7 | w7 (2) | 1 | [13] | -1 | 2 |
| (4, -2, -1) | -2 | 2 | -7 | w7 (2) | 1 | [13] | -1 | 2 |
| (4, -2, 1) | -2 | 2 | -7 | w7 (2) | 1 | [13] | -1 | 2 |

Which w_Q fixes which locus: {'w7': ['-1', '1/27']}. Window: |a| <= 12, Im tau >= 1/20, |Re tau| <= 1/2; the list of fixed points is not claimed complete. Each vector is obtained exactly from the fixed-point polynomial AND recovered from the numerical tau alone by `CM.vectors_annihilating`.
t at the fixed points against the Hauptmodul certificate's transformation constants {'w7': ['anti', '1/49']}: True (5 constraints that can fail are counted; a 't -> t' transformation constrains nothing at a fixed point and is recorded, not gated; z-locus identification PASS(40) inherited; Tier B numeric, 60 and 120 digits; closure checks: {'t-set of w7 fixed points closed under t -> 1/49/t (w7)': True}). Agreement with `CM_POINTS_RHO20.json` (same (-v^2, div v, D); its minimal polynomial of t vanishes at the t found here): True. Order of the fixing element = lcm of exponent denominators in `L3_RIEMANN_SCHEME.json`: True.

**cooper_s10** - n = 10 (from `C2_cooper_s10_v4_DRAFT.json`, DRAFT), group Gamma_0(10)*. **ADVISORY - LATTICE_CERT_DRAFT on every row.**

W(n) -> O(q_A): {'1': 1, '10': 19, '2': 11, '5': 9}; O(q_A) = [1, 9, 11, 19].

| v | v^2 | div v | D | fixed by (order of the element) | r_v multiplier | phi multiplier | z | exponent-denominator lcm (L3_RIEMANN_SCHEME) |
|---|---|---|---|---|---|---|---|---|
| (1, -1, 0) | -2 | 1 | -40 | w10 (2) | 1 | [19] | 1/16 | 2 |
| (2, -6, -1) | -4 | 2 | -20 | w5 (2) | 11 | [9] | -1/4 | 2 |
| (2, -6, 1) | -4 | 2 | -20 | w5 (2) | 11 | [9] | -1/4 | 2 |
| (6, -2, -1) | -4 | 2 | -20 | w5 (2) | 11 | [9] | -1/4 | 2 |
| (6, -2, 1) | -4 | 2 | -20 | w5 (2) | 11 | [9] | -1/4 | 2 |
| (10, -10, -3) | -20 | 10 | -4 | w2 (4) | 19 | [11] | infinity | 4 |
| (10, -10, 3) | -20 | 10 | -4 | w2 (4) | 19 | [11] | infinity | 4 |

Which w_Q fixes which locus: {'w10': ['1/16'], 'w2': ['infinity'], 'w5': ['-1/4']}. Window: |a| <= 12, Im tau >= 1/20, |Re tau| <= 1/2; the list of fixed points is not claimed complete. Each vector is obtained exactly from the fixed-point polynomial AND recovered from the numerical tau alone by `CM.vectors_annihilating`.
t at the fixed points against the Hauptmodul certificate's transformation constants {'w10': ['anti', '1/16'], 'w2': ['anti', '1/16'], 'w5': ['inv', '1']}: True (3 constraints that can fail are counted; a 't -> t' transformation constrains nothing at a fixed point and is recorded, not gated; z-locus identification PASS(40) inherited; Tier B numeric, 60 and 120 digits; closure checks: {'t-set of w10 fixed points closed under t -> 1/16/t (w10)': True, 't-set of w10 fixed points closed under t -> 1/16/t (w2)': True, 't-set of w2 fixed points closed under t -> 1/16/t (w10)': True, 't-set of w2 fixed points closed under t -> 1/16/t (w2)': True, 't-set of w5 fixed points closed under t -> 1/16/t (w10)': True, 't-set of w5 fixed points closed under t -> 1/16/t (w2)': True}). Agreement with `CM_POINTS_RHO20.json` (same (-v^2, div v, D); its minimal polynomial of t vanishes at the t found here): True. Order of the fixing element = lcm of exponent denominators in `L3_RIEMANN_SCHEME.json`: True.

Reading of the s10 table (advisory). z = 1/16 is the Fricke fixed point and z = -1/4 is the w_5 fixed point; both are involutions and phi = -r_v there. **z = infinity is not the fixed point of an Atkin-Lehner involution**: v = (10, -10, -3) is fixed by elements of the w_2 coset of order 4 (for example g = [[-2, -1], [10, 4]], phi_g of order 4 on T_10, multiplier 11); g^2 lies in Gamma_0(10) up to a scalar (True) and phi_g^2 = -r_v (True). So the reflection in that vector (multiplier 19 = -1) belongs to an order-2 elliptic element of Gamma_0(10) itself, and w_2 has no reflection anywhere (section 3). t is invariant under w_5 in the Hauptmodul certificate, so the w_5 fixed points carry no constraint on t; what is checked is that their t-set is closed under t -> 1/(16 t).

## 5. Monodromy leg - the one place a family could have disagreed

The family's own monodromy generators (`check_U1_lattice.py` stage 2, imported; entries by numerical recognition upstream, then exact; Tier B) act on the orbit lattice, whose Gram matrix equals the one in the lattice certificate. Their multipliers on A, computed basis-independently:

| family | generator | reflection | v^2 | div v | multiplier on A | leg F at the same locus (v^2, div, r_v multiplier) |
|---|---|---|---|---|---|---|
| cooper_s7 | cusp_z=0 | False |  |  | 1 |  |
| cooper_s7 | product_of_the_three | order 3 |  |  | 1 |  |
| cooper_s7 | z=-1 | True | -2 | 2 | 1 | [[-2, 2, 1]] |
| cooper_s7 | z=1/27 | True | -2 | 1 | 1 | [[-2, 1, 1]] |
| cooper_s10 (ADVISORY) | cusp_z=0 | False |  |  | 1 |  |
| cooper_s10 (ADVISORY) | product_of_the_three | order 4 |  |  | 11 |  |
| cooper_s10 (ADVISORY) | z=-1/4 | True | -4 | 2 | 11 | [[-4, 2, 11]] |
| cooper_s10 (ADVISORY) | z=1/16 | True | -2 | 1 | 1 | [[-2, 1, 1]] |

Every monodromy reflection has the invariants of the fixed-point reflection found independently in section 4: True. cooper_s7: the monodromy acts on A through +-1: True. cooper_s10 (advisory): it does NOT: True - the loop around z = -1/4 acts by 11, and the product of the three loops has order 4 and multiplier 11 = m(w_2). Multipliers seen on the loop side: s7 [1], s10 [1, 11]. For s10 that is an index-2 subgroup of O(q_A): the loop at the w_5 fixed point acts by 11 = -m(w_5), numerically the same as m(w_2), so the loop action on A does not separate w_5 from w_2; a loop is matched to an Atkin-Lehner class only modulo +-1. The remaining values of O(q_A) are reached through the determinant +1 lift phi, not by any loop. (`implied_not_gated`: {'M_product_multiplier_is_in_image_of_W': True} - recorded, not part of the verdict, since it cannot fail once the generators are integral isometries.) Recorded as observed. What it would mean for the Neron-Severi side is not examined (section 8).

## 6. Hand estimate, scored

orchestrator's hand estimate, issued UNVERIFIED.

| clause | outcome |
|---|---|
| O(q_A) at n = 10 is {1, 9, 11, 19} | confirmed |
| n = 10: the three vectors give reflection multipliers 1, 11, 19 | confirmed |
| n = 10: with -1 they generate all of O(q_A) | confirmed |
| rule: w_Q acts by -1 on the Q-part and +1 on the rest (exactly: -1 mod 2Q, +1 mod 2n/Q), up to the global sign | confirmed |
| the map is a group homomorphism compatible with w_2 w_5 = w_10 | confirmed |
| the map is injective modulo +-1 | **REFUTED** |

The refuted clause is a finding, not a defect: modulo +-1 the map has kernel {1, w_n}; the injective statement is the one into O(q_A).

Separately - builder's own working expectation; NOT in the orchestrator's estimate, which left the locus-to-w_Q assignment to be determined:

| builder's expectation | outcome |
|---|---|
| each of the three s10 loci is the fixed point of an Atkin-Lehner INVOLUTION whose lattice image is the reflection in the listed vector | **REFUTED** |

The third s10 vector is the fixed vector of order-4 elements of the w_2 coset (and of an order-2 element of Gamma_0(10) itself), not of an Atkin-Lehner involution. Determined assignment (advisory): {'w10': ['1/16'], 'w2': ['infinity'], 'w5': ['-1/4']}.

## 7. Recommendation to T0 on the flag: **NARROW**, do not simply close

NARROW the flag ATKIN_LEHNER_ACTION_UNVERIFIED: the lattice-level action is now explicit and exact (isomorphism, not a count). What stays open is stated in not_claimed (extension to the Neron-Severi side; identification of the moduli space). Not an edit of check_T3.

- What the evidence now supports: the question the flag asked - do the Atkin-Lehner involutions of composite level act on T_n compatibly with its discriminant form, or do only the counts agree - is answered at lattice level by an explicit isomorphism (exact), and for cooper_s10 that isomorphism is consistent with four artifacts produced separately: the t-transformations of `HAUPTMODUL_S10_GAMMA010STAR.json`, the loci of `CM_POINTS_RHO20.json`, the exponent denominators of `L3_RIEMANN_SCHEME.json`, and the family's own monodromy.
- What stays open, and would justify keeping a narrower flag: w_2 and w_5 act on A by 11 and 9, not by +-1, so they lie outside the group of the pinned Dolgachev theorem (Gamma_0(n)+, read as Fricke only). That Gamma_0(10)* is nevertheless the group of z is then a statement about the family that the lattice T alone does not supply. The `LATTICE_CERT_DRAFT` flag is separate and untouched.
- This is a recommendation. `check_T3_level_consistency.py` is not edited by this task.

## 8. Not claimed

- that gate T3 is adopted, or that the flag in check_T3_level_consistency.py is closed: that file is not edited; the recommendation below is addressed to T0
- anything certified about T(cooper_s10): C2_cooper_s10_v4_DRAFT.json is DRAFT by T0 ruling; every s10 row is advisory (LATTICE_CERT_DRAFT)
- that the isometries phi_g extend to the K3 lattice with a prescribed action on the Neron-Severi side: for multipliers other than +-1 that needs surjectivity of O(M_n) -> O(q), which is model-knowledge (Nikulin 1979, Thm 1.14.2), unfetched, not pinned
- that the moduli space of the cooper_s10 family IS X_0(10)*: the Deep Think question stays open
- any Kodaira fibre type at any locus (CLAUDE.md ledger item 3)
- any statement about the rho = 20 cut (not adopted) or any ranking of candidates
- any physical reading whatsoever (VISION sec 1.3; Tier C blocked, F5b)

## 9. Thought experiment (an analogy for discussion; it carries no claim)

Picture a walker who carries a clock with 2n hours - the discriminant group - around a closed path in the z-line, and compares the clock on return. For n = 7 the clock always comes back as it left, whatever the path. For n = 10 (advisory) a path around z = -1/4 brings it back with every hour h replaced by 11 h: the hours [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] are untouched, every other hour is moved by [10]. Two walkers who compare only positions on the z-line cannot tell that anything happened; two who compare clocks can. The count 4 = 4 said that the clock has as many symmetries as there are Atkin-Lehner classes. The present computation says less than 'each path produces its own symmetry': walking only ever produces the clock symmetries [1, 11], half of the 4 available, and a walker cannot tell from the clock alone whether the path went around the w_5 point or realised w_2 - the two differ by the global sign, which the clock comparison along a path does not fix. The other two symmetries belong to the algebraic lift phi, which no path realises. It is a picture of sections 4-5 and nothing more.

## 10. Controls

`test_atkin_lehner_vs_disc_form_controls.py`: 33/33 controls behaved as required (exit code 0); each control names the clause that fired. Real known-bads: tau -> (tau+1)/5 is not an integral isometry (`phi_not_integral`); level-10 matrices against T_7 and the level-7 Fricke matrix against T_10 (`phi_not_integral`); cooper_s7 monodromy paired with n = 10 (`monodromy_lattice_det_not_2n`); non-reflective vectors of the CM table (`reflection_not_integral`); the sign-swapped rule never matches; the hypothesis "monodromy acts through +-1" is true for s7 and false for s10. A defect found while writing the checker is kept as control S6: at 15 working digits the tolerances are vacuous (a 1e-40 perturbation is accepted); in the actual process the ambient precision after the imports is higher than 15, and the reviewer's mutation (wrapper removed) made the t-consistency gate go False, i.e. it fails safe; comparisons run at 150 digits.

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: test_atkin_lehner_vs_disc_form_controls.py | Reviewed-by: N
