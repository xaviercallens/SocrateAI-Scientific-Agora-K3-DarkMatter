# "K3×T² / M24 Mathieu Moonshine" document — Claims Register (guardrail-compliant form)

**Date:** 2026-09-16 | **Purpose:** Xavier supplied an externally-authored document ("SPÉCIFICATION
GÉOMÉTRIQUE DE LA VARIÉTÉ K3×T² ET VALIDATION EXPÉRIMENTALE" + a follow-on "RÉPERTOIRE CRITIQUE
DES SÉQUENCES OEIS" + extended physics derivation) as a candidate basis for K3 selection. Same
situation as `docs/OEIS_FTHEORY_CLAIMS_REGISTER.md` (2026-07-24): an external "AI-swarm"-style
submission cannot enter this repo's selection criteria as written. This register applies that
same discipline — every extractable claim checked individually, nothing accepted on the
document's own authority. **A claim graduates out of this register only via a fetched primary
source or a computed check, both shown inline.**

**House rules applied (epistemic-guardrails):** no numbers from memory (every check below was
actually run — via WebFetch to oeis.org, Python computation, or grep against this repo's own
pinned `docs/literature/huybrechts_K3Global.txt`); PASS always carries its order; Tier C requires
an in-sentence conjecture marker.

**Headline finding:** of 12 OEIS IDs checked, **7 are fabricated or misattributed to the wrong
mathematical object**, 5 are genuinely correct. The failure pattern is not random: every generic,
famous sequence cited (Ramanujan tau, partition function, sum-of-divisors, Leech theta, η³) is
correct; every sequence specifically claimed to encode "the M24 connection" (the McKay-Thompson
twisted series, the M24 irrep dimensions, the Golay weight enumerator) is wrong. This is
consistent with a generator that got the boilerplate right and invented the citations that would
have required an actual literature/database lookup — the same signature as this project's three
prior fabrication incidents (Domb×A002893 false relation; 0/24-supported Discovery PDF; vacuous
"0 sorry" Lean oracle claim; see `session_log_2026_07_31.md`).

---

## 1. OEIS claims (checked against oeis.org directly, this session)

| # | OEIS ID | Claimed to be | Actually is (fetched) | Verdict |
|---|---|---|---|---|
| O1 | A000594 | Ramanujan tau, Δ=η²⁴ | Ramanujan's tau function, confirmed | ✅ **CORRECT** |
| O2 | A010816 | η(q)³ coefficients (Ramanujan "shadow") | Expansion of ∏(1−x^k)³: `1,-3,0,5,0,0,-7,...` — matches the claimed Jacobi identity η³=Σ(−1)ⁿ(2n+1)q^(n(n+1)/2) exactly | ✅ **CORRECT** |
| O3 | A000041 | Partition function p(n) | Partition function, confirmed | ✅ **CORRECT** |
| O4 | A000203 | σ₁(n), sum of divisors | σ₁(n), confirmed | ✅ **CORRECT** |
| O5 | A008408 | Theta series of Leech lattice | Theta series of Leech lattice, confirmed | ✅ **CORRECT** |
| O6 | A182111 | K3 elliptic-genus mock-theta H⁽²⁾(τ), M24 class "1A" McKay-Thompson: claimed terms `-1,90,462,1540,4554,11592` | "Number of iterations of n → sum of cubes of its decimal digits": actual terms `1,7,3,6,6,10,6,6,4,1` | ❌ **FABRICATED** — unrelated sequence |
| O7 | A182112 | M24 class "2A" McKay-Thompson series | "Ordered triples (w,x,y)… (w+n)²=x+y+w" — combinatorics, unrelated | ❌ **FABRICATED** |
| O8 | A182113 | M24 class "3A" McKay-Thompson series | Lexicographically-earliest parity-constrained permutation — unrelated | ❌ **FABRICATED** |
| O9 | A182118 | M24 class "23A" McKay-Thompson series | "Table of triangular arguments," unrelated recursive construction | ❌ **FABRICATED** |
| O10 | A007267 | Dimensions of M24 irreps: `1,23,45,45,231,252,253,...` | McKay-Thompson series class **2A for the Monster group** (not M24): `1,104,4372,96256,...` | ❌ **FABRICATED / wrong group** — real moonshine sequence, but Monstrous moonshine, not Mathieu moonshine |
| O11 | A003300 | Binary Golay code G24 weight enumerator (759 octads, 2576 dodecads) | "Denominators of coefficients of Green function for cubic lattice": `1,1,18,24,27216,...` | ❌ **FABRICATED** — coding theory claim attached to an unrelated lattice-physics sequence |
| O12 | A004006 | "E8 Theta" | `C(n,1)+C(n,2)+C(n,3)` — unrelated combinatorial polynomial. (The document *separately* and correctly cites A004009 = "theta series of E8 lattice" elsewhere — so the document contradicts itself between its two E8 citations.) | ❌ **FABRICATED / self-contradictory** |

**Additional check:** searched oeis.org directly for "Mathieu moonshine McKay-Thompson K3 elliptic
genus" — **zero results**. No OEIS sequence for the Mathieu-moonshine McKay-Thompson series
appears to exist in the database under any search term tried this session. This means every
citation in the O6–O10 row group was necessarily either invented or misattributed — there was no
correct ID available to cite in the first place, under this search.

**Not checked (not independently used elsewhere in the document with a specific numeric claim
riding on them; flag as unverified, not fabricated):** A182114–A182117, A182119, A182120,
A004009 (secondary use only), A000001 (used as a bare placeholder label "Draft RAMA" next to the
real, unrelated sequence "number of groups of order n" — confusing, not a substantive claim).

---

## 2. Geometric/structural claims (checked against this repo's own pinned reference or computed)

| # | Claim | Check | Verdict |
|---|---|---|---|
| G1 | χ(K3)=24, b₂=22, signature=−16, Γ³'¹⁹≅E8(−1)²⊕U³ | Standard textbook K3 facts, consistent with `docs/literature/huybrechts_K3Global.txt` throughout | ✅ **CORRECT** — Tier A |
| G2 | "24 singularités nodales A₁ (Kummer)" | `huybrechts_K3Global.txt` lines 219, 730 (already hash-pinned in this repo): a Kummer K3 has the **16** two-torsion fixed points of the involution on the abelian surface, resolved to **16** A₁ nodes — quoted directly: *"the 16 two-torsion points as fixed points"* and *"a quartic … with the maximal number of **16** singular points is also called a Kummer surface"* | ❌ **WRONG** — conflates χ(K3)=24 with the (different, and incorrect as stated) Kummer node count, which is 16 |
| G3 | "Quotient Modulaire M₂₄ → A₄" (used to derive 3 flavor generations, δCP=282.4°) | M24 is a **simple group** (order 244,823,040) — already established Tier A in this repo's own pinned reference, `huybrechts_K3Global.txt` line 13885 area: *"It is a simple sporadic group"* | ❌ **STRUCTURALLY IMPOSSIBLE AS STATED** — a simple group's only normal subgroups are {1} and itself, hence it has no nontrivial quotient group at all, let alone one isomorphic to A₄ (order 12). Whatever the document intends (a subgroup, a branching, a stabilizer) it is not a quotient, and no derivation of δCP=282.4° is shown regardless of terminology |

---

## 3. Numerical claims (computed directly, this session — see prompt log for the Python)

| # | Claim | Computed | Verdict |
|---|---|---|---|
| N1 | ρ_Λ = M_Pl⁴·e^(−2π√23) ≈ **10⁻¹²²** M_Pl⁴ (headline "resolves the cosmological constant" claim) | `e^(-2*pi*sqrt(23))` = **8.19×10⁻¹⁴** | ❌ **WRONG by ~108 orders of magnitude.** Not a rounding issue — the claimed exponent and the computed exponent disagree by more than a hundred decades. This is the document's central physics claim and it does not survive direct computation of its own stated formula |
| N2 | r = 12/N_e² = 0.00396 (N_e=55) | `12/55**2` = 0.0039669… | ✅ Arithmetically consistent with the stated formula (note: `12/N_e²` is a generic large-field-inflation plateau-model formula, not something the document derives from M24/K3 structure specifically — the arithmetic checks out, the physical derivation connecting it to this geometry does not appear in the document) |
| N3 | R_NL = A₂/(4A₁) = 462/360 = 1.28333 | `462/360` = 1.28333…, and the document's own Lean `decide` step (462×60 = 360×77 → 27720=27720) | ✅ Arithmetically consistent **as a fraction reduction**, but built on the A₁=90, A₂=462 values — which are real, independently-published EOT-2010 mock-theta coefficients (not verifiable against OEIS per §1, since no such OEIS entry exists) attached to a **fabricated OEIS citation** (O6, A182111). The arithmetic is fine; the sourcing for the inputs is not |
| N4 | Eta-quotient weight k=−91.5 from exponent vector e=(24,23,−14,−24×9) | `0.5*(24+23-14+(-24)*9)` = −91.5 | ✅ Self-consistent given the standard eta-quotient weight formula k=½Σe_d — this only confirms internal arithmetic consistency of an unverified, self-supplied exponent vector, not that the vector means anything geometrically |

---

## 4. The Lean 4 "formal specification" block

**Verdict: proves nothing about K3 geometry or physics.** Every theorem in the supplied block
(`k3_euler_char_eq_24`, `k3_signature_difference`, `k3_parity_modulo_8`, `mathieu_rigidity_ratio`,
`discriminant_is_23`, `kummer_matches_euler`) is `rfl` or `decide` closing over `def`s that are
**hand-typed integer/nat literals** (`def k3_betti_2 : Nat := 22`, `def mathieu_A1 : Int := 90`,
`def kummer_singularities_count : Nat := 24`), not derivations from any geometric construction or
external library (no `Mathlib` K3/lattice/group import, no connection to this repo's actual Lean
work in `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal`). `kummer_matches_euler` in
particular formalizes the **wrong number** identified in G2 above (24 instead of 16) as if it were
a proven fact, by definitional fiat. This is the same "0 sorry, vacuous" pattern already logged
against a prior fabricated Lean oracle claim in `session_log_2026_07_31.md` — it compiles, and it
demonstrates nothing beyond the arithmetic of numbers the author already chose.

---

## 5. Physics/phenomenology correspondence table (Tier C — conjecture markers mandatory)

The document's central "geometry ⟺ observation" table asserts **Validé / Confirmé / Conforme**
for ~11 rows spanning Planck low-ℓ anomalies, ARCADE 2, EDGES 21-cm, Fermi-LAT, CRESST/CDMS, and
DUNE/HERA/LiteBIRD/CMB-S4 forecasts. **None of these rows has a shown derivation connecting the
geometry column to the physics column** — each is an assertion. Per this project's own
`epistemic-guardrails` skill, every one of these is a Tier C physical-interpretation claim and
none may be stated as fact ("Validé", "Confirmé", "Conforme" are exactly the forbidden pattern
without an in-sentence conjecture marker and a constructed EFT matching, which VISION §1.3
requires and which is absent here). Given §1–§4 above, the specific numbers feeding several of
these rows (the M24 representation data in particular) are independently unreliable.

**Compliant restatement, if any version of this table is to be used going forward:** each row
would need to read as **"[C] we conjecture ⟨geometric mechanism⟩ produces ⟨observable⟩, pending
a worked EFT matching"** — not as a validated result.

---

## 6. Disposition

**None of this document's specific predictive content (η-quotient level-12 sequence, McKay-
Thompson coefficient tables, the physics correspondence table, the numerical predictions) may be
cited in this repo, `K3_SELECTION_REPORT.md`, or any Stream 3 experimentation plan.** It does not
graduate out of this register.

**What survives, unchanged from before this document arrived:** the textbook K3 facts in G1, and
the genuinely real, already-cited-in-this-repo connection between K3 surfaces and M24/M23 via
**Mukai's theorem** (symplectic automorphism groups, constrained by each candidate's certified
NS lattice — see `briefs/T0_PROPOSAL_M24_SYMPLECTIC_CRITERION_2026_09_16.md`,
`sandbox/m24-moonshine-criterion-2026-09-16`, still pending T0 review, unaffected by this
document's failure). That proposal does not rely on, and is not strengthened or weakened by,
anything in this document.

**Recommendation:** treat the supplied document as not usable as a K3-selection input. If Xavier
has the original source this was generated from (a paper, a specific tool, an "AI-swarm" prompt
chain), naming it would let this register be extended with a proper primary-source check instead
of closing here.

Generated-by: Claude (Sonnet 5), this session | Verified-by: 12 direct OEIS fetches (§1), grep
against pinned `docs/literature/huybrechts_K3Global.txt` (§2), direct Python computation (§3),
manual read of the supplied Lean block (§4) | Reviewed-by: T0 — REJECTED 2026-09-16 (§7)

---

## 7. T0 Ruling — 2026-09-16

**REJECTED.** The supplied document is rejected outright as a K3-selection input. Grounds, all
already checked in §1–§4 of this register: fabricated or misattributed OEIS citations; wrong
Kummer node count (16, not 24, per the pinned Huybrechts reference); and an impossible
"M24 → A4 quotient" (M24 is simple). The document was never committed to this repo, so there
is nothing to purge; this register is retained as the rejection record. The separate
Mukai-theorem proposal is on HOLD for its own reasons (S3 `briefs/T0_RULINGS_2026_09_16.md`
§B2), not because of this document. Ruled by T0 (Xavier Callens) in session; recorded by
Claude (Opus 5).

Generated-by: Claude (Opus 5) | Verified-by: n/a (ruling record) | Reviewed-by: T0 Y
