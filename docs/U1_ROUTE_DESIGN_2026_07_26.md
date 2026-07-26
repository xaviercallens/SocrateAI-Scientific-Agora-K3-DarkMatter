# U1 route design — how to close "T ≅ U ⊕ ⟨14⟩" without guessing

**Date:** 2026-07-26 (night) · **Status:** DESIGN ONLY — nothing here is certified; no number
below may be cited until the computations run with negative controls. Written so the next
session executes instead of re-deriving.

**U1 (the residual from Phase 4 step 2):** the framework (Dolgachev Thm 7.1, Doran Thm 5.13,
both read) gives Mₙ-polarized ⇒ {moduli X₀(n)+, T = U⊕⟨2n⟩, PF = Sym²}. Our family has all
three fingerprints at n = 7. U1 is the converse gap: showing OUR T is U⊕⟨14⟩, not another
even (2,1) lattice with the same visible behavior.

## Decomposition: U1 = U1a + U1b

**U1a — derive disc form of T from the family itself** (the real content):

The period vector of an Mₙ-polarized family in a lattice basis (f, g isotropic, ⟨f,g⟩=1;
⟨e,e⟩=2n) is **ϖ ∝ g + τe − nτ²f** — this is verbatim Dolgachev §7 p.20 ("µ = −nt²f+g+te",
his t ∈ H). Consequences derived this session (re-derive before use; do not cite this note
as authority):

1. **The cusp monodromy alone does NOT see n.** τ→τ+1 acts integrally on the Frobenius flag
   (y₀, y₀τ, y₀τ²) for every n. Do not try to read n off T_MUM — it is not there.
2. **n sits in the elliptic-point/Fricke monodromies.** ϖ(−1/(nτ)) ∝ n²τ²g-side mixing — the
   w₇-type matrices in the integral basis carry n. **Route:** compute the monodromy of L₂
   around BOTH finite singular loci in the Frobenius basis (numerical analytic continuation —
   Route γ step 1 already did ~17-digit continuation on this operator, reuse that machinery),
   Sym² them, find the ℤ-lattice Λ preserved by cusp + both elliptic matrices jointly, restrict
   the Sym² quadric (y₀y₂ − y₁² in Frobenius coordinates) to Λ, rescale to a primitive even
   integral form, read off the Gram matrix ⇒ disc form of T. Expectation: det = −14; **if the
   computation says otherwise, THAT is the result.**
3. **Independent cross-check — the Yukawa constant.** Q(∂τϖ, ∂τϖ) = ⟨e,e⟩ = 2n exactly,
   τ-independent (one-line computation from ϖ above; K3 ⇒ no instanton corrections — this is
   Dolgachev's MS3′ "constant quantum intersection form", read). So the mirror-normalized
   two-point Yukawa of L₃ must equal the CONSTANT 2n = 14. Computable as an exact q-series
   from L₂/L₃ data; it must be constant to full order (that constancy is itself a control).
   Getting 14 here corroborates U1a; it does not by itself fix the integral lattice.

**Controls for U1a:** run the identical pipeline on a DIFFERENT level (s10's operator once its
coordinate lands, or the level-1 E-series family where the answer U⊕⟨2⟩ is classical) and
assert it does NOT give −14; scramble one elliptic matrix and assert the invariant-lattice
step fails; the Yukawa series must be constant — any q-dependence is a pipeline bug.

**U1b — class number of the genus** (the finishing step):

If U1a lands det = −14 with the disc form of U⊕⟨14⟩, then T ≅ U⊕⟨14⟩ follows if the genus
contains one class. Route: **Eichler's theorem** (indefinite, rank ≥ 3 ⇒ spinor genus = class)
plus spinor-norm coverage at p = 2, 7 (at 7: Jordan splitting is unimodular-rank-2 ⊥ scale-7,
and a unimodular component of rank ≥ 2 at an odd prime forces unit coverage; at 2 the rules
are fussier — **do not hand-wave the 2-adic case**). Source to fetch and read: Cassels,
*Rational Quadratic Forms*, Ch. 11 (or O'Meara §102/104). Not in `docs/literature/` yet —
same discipline as Zarhin/Dolgachev: fetch, pin, read, THEN cite with page numbers.

## Why this was not executed tonight

End-of-session, authority freshly granted, expectation of the answer in context — the exact
conditions under which this project has previously manufactured results (E-010). U1a is a
numerically delicate basis-convention computation; done eagerly it produces a well-formed
wrong certificate. The design is recorded; the execution is next session's first task, fresh.

## Order of work next session

1. U1a-3 (Yukawa constant): smallest, exact q-series arithmetic, self-controlling. Do first.
2. U1a-2 (elliptic monodromy → integral lattice → Gram): the main computation.
3. Fetch Cassels; U1b as a checker citing read pages.
4. On U1 PASS: `C2_cooper_s7_v4.json` (lattices [B]); Phase 4 memo re-issue; S3-00 2(b)
   re-scope option to T0. On any FAIL: that is a finding, not a setback — report it as-is.

**Generated-by:** Fable 5 (Stream 2) | **Verified-by:** nothing — this is a design note, and
it says so | **Reviewed-by:** Xavier (T0) — pending
