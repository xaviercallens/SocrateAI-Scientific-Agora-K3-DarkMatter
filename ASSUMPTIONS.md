# ASSUMPTIONS — Dual-Scale Topological Universe Model (v0.2)

*(Dependencies for the MVM and PREDICTION.md. Every downstream result is conditional on the
assumptions below and must cite them by ID. Each assumption carries a discharge path — how it
could eventually be verified, replaced by a computation, or falsified — and a tier ledger entry.)*

**Status:** v0.2 — authoritative register from the T0 review session. **Reviewed-by: pending Xavier sign-off.**
**Repo of record:** `SocrateAI-Scientific-Agora-K3-DarkMatter`; mirrored (hash-pinned at freeze) in the other two repos.

> Supersedes the v0.1 draft, which was a best-inference reconstruction made before this text
> was available in-repo. Note the v0.1 reconstruction's "A-REL" was a different assumption
> (global–local sector relation) — that content is *not* lost: it is the kill condition already
> pre-committed in `EXECUTION_PLAN.md` WP S3-00 step (4), where it belongs as a checkable
> outcome rather than an assumption.

---

**A-SEQ (Moduli Sequestering).**
We assume the Calabi-Yau fourfold Y₄ admits a flux stabilization scheme in which all moduli
outside the explicitly tracked sequence pair (z_bulk, z_brane) — including all remaining
complex-structure moduli of Y₄, the Kähler moduli of B₃ other than the overall volume,
**the open-string sector on the brane divisor D (brane position moduli and Wilson lines)**,
and any additional axionic partners — are stabilized strictly above the dark-sector EFT
cutoff, decouple from the 4D dark-sector EFT, and mediate no long-range forces.
*(Tier C. Discharge path: exhibit an explicit flux choice realizing the hierarchy for the
selected candidate, or find an obstruction — either outcome is reportable. Failure mode:
if a forgotten light field is identified that couples to the dark sector, every MVM result
is void and must be recomputed.)*

**A-VOL (Volume and Coupling Stabilization).** *(v0.2 — split out of A-SEQ to remove a
dangerous ambiguity.)*
The overall volume 𝒱 and the string coupling g_s are **stabilized** — with masses safe from
fifth-force, equivalence-principle, and post-BBN cosmological constraints in the *visible*
sector — but at values not computed within the MVM. They therefore enter the EFT as the two
declared CONTINUOUS-FREE constants of the Free-Parameter Ledger: unknown numbers, **not light
dynamical fields**. No MVM observable may rely on 𝒱 or g_s rolling.
*(Tier C. Rationale: a light volume modulus couples gravitationally to all sectors and is
excluded by visible-sector fifth-force tests long before any dark-sector observable is
reached; exempting 𝒱 from stabilization would falsify the model in the wrong sector.
Discharge path: a concrete stabilization mechanism for (𝒱, g_s) with computed values would
convert both from FREE to GEOMETRIC in the ledger and strengthen every prediction; this is
desirable but not required for M1.)*

**A-ONT (Dark Sector Ontology).**
Dark matter consists of confined SU(N) dark-sector states (e.g., dark glueballs) localized on
the 7-branes wrapping D. The local elliptic modulus fluctuation φ is the light scalar
mediator, with mass m_φ computed from the flux potential at the vacuum point selected by the
C3b map F. The solitonic-halo picture is relegated to a clearly-marked speculative appendix,
outside the prediction chain.
*(Tier C. Discharge path: the MVM steps 1–2 replace the qualitative statement with computed
(m_φ, α_D, Λ_D) as functions of (𝒱, g_s). Failure mode: if the Kodaira data of the selected
candidate provides no non-Abelian locus (criterion C2, HYPOTHESIS-DERIVED list), A-ONT has no
carrier and triggers F1 for the dual-scale role.)*

**A-REL (Relic Abundance).** *(v0.2 — new.)*
The observed dark matter abundance Ω_DM h² ≈ 0.12 is achieved by some production mechanism
(e.g., dark-sector freeze-out/freeze-in or misalignment of a heavier partner) **without
modifying the low-velocity self-interaction physics** that the MVM predicts: the σ(v)/m curve
and the mediator sector are treated as independent of the production history. The DM particle
mass is set by the confinement scale, m_DM ~ Λ_D(𝒱, g_s).
*(Tier C. Rationale: without this assumption, the lensing prediction silently depends on an
uncomputed cosmological history. Declaring it makes the dependency auditable. Discharge path:
a worked production calculation for the selected candidate; if the required history conflicts
with the (𝒱, g_s) region singled out by other observables, that tension is a reportable
result, not a tuning opportunity.)*

---

## Consistency notes

1. **Ledger alignment:** A-VOL is the assumption-form of the ledger's CONTINUOUS-FREE row;
   A-SEQ is the assumption-form of the ASSUMED row. The ledger and this file must never
   disagree; CI greps both for the assumption IDs.
2. **Labeling rule:** any PREDICTION.md quantity derived under these assumptions carries the
   suffix list it depends on, e.g. r_c(M_halo) [A-SEQ, A-VOL, A-ONT, A-REL]. A result whose
   assumption list grows after the pin is a tuning event (TUNING_LOG.md).
3. **Adversarial standing item:** the Deep Think adversarial pass on each phase explicitly
   attempts to break A-SEQ (find the light field we forgot) and A-REL (find the production
   history that back-reacts on σ(v)). Unanswered breaks block the pin.

**Changelog**
- v0.1: Desk draft (A-SEQ, A-ONT); in-repo v0.1 was a session reconstruction, now superseded.
- v0.2 (this version): A-VOL split out — 𝒱 and g_s are stabilized-at-unknown-values, not
  light fields; g_s added (absent from v0.1); open-string moduli and Wilson lines added to
  A-SEQ's scope; A-REL added; discharge paths, failure modes, labeling rule, and adversarial
  standing items added.

*Generated-by: T0 review session | Verified-by: n/a (assumption register) | Reviewed-by:
pending Xavier sign-off*
