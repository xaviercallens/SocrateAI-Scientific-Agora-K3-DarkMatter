# PREDICTION.md — Pre-Registered Observable & Derivation Protocol (PINNED)

## Document Information
- **Version:** 1.0-PINNED
- **Date:** 2026-07-24
- **Pin authority:** Xavier Callens (T0 Owner) — **by explicit delegation** to Claude (Fable 5),
  instruction of 2026-07-24 ("take decision and update … prediction.md on my behalf").
  Marked **[T0-DELEGATED]** throughout; countermand window open (any countermand recorded in
  ASSUMPTIONS.md §2 ledger with date).
- **The pin:** the git commit introducing this version IS the hash-pin. Audit rule: `git log`
  timestamps must show this commit **predates any fetch of the observable's comparison dataset**
  (fetch events are themselves pinned in `data/MANIFEST_STREAM3.md` / `refs/MANIFEST.md`).
- **Supersedes:** the "DRAFT v1.0, three candidates, narrowing deferred" state referenced by
  the Stream-1→Stream-3 directive (2026-07-24).

---

## 1. What is being pinned (and what deliberately is not)

**Pinned now [T0-DELEGATED]:**
1. The **candidate-selection rule** (§2) — mechanical, evaluated on checker certificates only.
2. The **observable decision rule** (§3) — a pre-committed branch on the S3-00–derived mass;
   committed *before* the derivation runs, which is what makes the eventual choice a
   pre-registration rather than a fit.
3. The **TEST/FIT split per branch** (§4) and the **kill condition** (§5).

**Deliberately NOT pinned (no fabricated numbers):** m_φ, α_D, Λ_D and the final observable
relation. These are **TO-BE-DERIVED** by WP S3-00 (T0 derives, T0s blind re-derives; two-model
rule) from the selected candidate's period geometry + C2 Kodaira/lattice data. Writing values
here before that derivation would be numbers-from-memory — forbidden. Upon S3-00 completion,
they are appended as §6 in a new commit (v1.1-PINNED) whose timestamp must still predate data
contact for the chosen observable.

**Assumption tags on everything below:** [A-ONT, A-SEQ, A-VOL, A-REL] (ASSUMPTIONS.md v2.0,
SIGNED); §4 comparisons additionally [A-DATA, A-PIPE].

---

## 2. Candidate-selection rule (Route A — DECIDED)  [T0-DELEGATED]

Per K3_SELECTION_REPORT.md §3 (decision recorded there as DECIDED, this document is the
operative rule): the S3-00 input is a **sporadic AZ order-3 / Zagier order-2 catalogued pair**
(Route A). The Cooper family is excluded from the pre-registered input — corrected reason on
record: non-catalogued partner (C3b-CAT FAIL, both repos concur), **not** absent Sym² structure
(C3b-SYM is kernel-proven).

**Mechanical selection among qualifying pairs — rule fixed BEFORE C2 runs on them:**
1. Eligible: AZ pairs passing C1-INT, C3-CAT, C3b-CAT in *both* repos after their sequences land
   in `refs/` (fetch+hash; cross-repo two-model reproduction required).
2. Among eligible pairs, select the pair whose **C2-certified Picard rank ρ is maximal**
   (tightest moduli freezing for the [A-VOL] elimination step).
3. Tie-break 1: larger certified mirror-map integrality order (C1-INT margin).
   Tie-break 2: lower modular level of the Zagier partner.
4. The winner is whatever the certificates say. No post-hoc re-ranking; any deviation must be
   logged in TUNING_LOG.md and demotes downstream results from TEST to FIT.

## 3. Observable decision rule (the pin)  [T0-DELEGATED]

Evaluated **mechanically** on the S3-00 output m_φ (with its propagated uncertainty):

| Branch | Trigger | Observable |
|---|---|---|
| **P1 — PTA** | m_φ ∈ [10⁻²³, 10⁻²²] eV (window per EXECUTION_PLAN §4 S3-00 draft ordering, "first available") | Predicted nHz scalar signal at f = m_φ/π vs **published** NANOGrav 15-yr / EPTA DR2 free-spectrum posteriors (comparison against public products; no collaboration involvement claimed) |
| **P2 — Lensing** | m_φ outside the P1 window | r_c(M_halo) halo-profile prediction vs published stacked weak-lensing profiles (dwarf regime) |
| **Companion (both branches)** | always | **Lyman-α null test** (SDSS DR12 / DESI): model must NOT produce excess small-scale power; a detection here is evidence against, feeding §5 |

If m_φ's uncertainty band straddles the P1 boundary: run **P1**, report the straddle
explicitly, and demote the branch choice itself to FIT in the output labels.

## 4. TEST/FIT split — declared in advance  [T0-DELEGATED]

| Branch | Quantity | Label |
|---|---|---|
| P1 | spectral location f = m_φ/π and spectral shape | **TEST** |
| P1 | any amplitude scaling tuned against the same posteriors | **FIT** (report both raw and tuned) |
| P2 | radial-slope *shape* of r_c(M_halo) | **TEST** |
| P2 | profile normalization σ(v)/m | **FIT** |
| Lyman-α | presence/absence of excess power at pinned scales | **TEST** (null expected) |

Labels are assigned at output-generation time by the V5 pipeline [A-PIPE] and may never be
edited after data contact.

## 5. Kill condition — pre-committed  [T0-DELEGATED]

Per EXECUTION_PLAN §4 S3-00: **if no observable relation survives the (𝒱, g_s) elimination**
(i.e., the model's observables cannot be related independently of the unfixed moduli), the
model is generic vdSIDM and **F5 triggers**. This is a real, reportable outcome; it is recorded
in OBSERVATIONAL_REPORT.md with the same prominence as a detection. Secondary pre-committed
branches: F3/F4 threshold triggers as defined in EXECUTION_PLAN (mechanical, never post-hoc).
The kill-condition evaluation is REQUIRED output of S3-00 regardless of which way it falls.

## 6. Derived quantities — RESERVED (v1.1)

Empty by design at v1.0-PINNED. Populated only by the completed, two-model-agreed S3-00
derivation, in a new commit, with uncertainties and full assumption-tag lists.

---

Generated-by: Fable 5 under explicit T0 delegation (2026-07-24) | Verified-by: rules reference checker certificates only; no derived numbers present | Reviewed-by: T0 **SIGNED-BY-DELEGATION** (countermand window open)
