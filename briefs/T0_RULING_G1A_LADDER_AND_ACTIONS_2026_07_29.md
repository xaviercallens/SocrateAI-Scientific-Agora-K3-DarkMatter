# T0 Ruling & Action Brief — G1 Ladder Revision, Xavier Actions, Program Scoreboard (2026-07-29)

**Status:** T0 RULING (issued by Fable 5 running as T0 per `EXECUTION_PLAN.md` §1.1 roster) on
`briefs/T0_DECISION_REQUEST_G1a_LADDER_2026_07_28.md`, plus the standing action list for Xavier
and the program scoreboard. Countermand window on §1.R2 closes **2026-07-30 EOD** (D1-grid
precedent); absent countermand, execution proceeds as ruled.

---

## §1 — T0 Rulings

### R1. G1-a certificate promoted DRAFT → LIVE [Tier B]

The G1-a result (`briefs/G1a_CY_CONDITION_RESULT_2026_07_28.md`, commit `d6146c4`: naive
fiber-product pullback of the certified cooper_s7 family cannot be Calabi-Yau over P² or any
F_n incl. P¹×P¹, exactly and for every value of the uncomputed Hodge-bundle degree ℓ) is
promoted to LIVE.

**Basis (producer ≠ verifier satisfied twice over):**
1. Coordinator's independent verification — all 5 negative/positive controls re-run fresh
   (PASS), and K_{F_n} = −2s−(n+2)f re-derived from scratch via adjunction without reading the
   checker, exact match.
2. External cross-model convergence — Deep Think's independent zero-shot "Trap 1"
   (`briefs/DEEPTHINK_DEBRIEF_AUDIT_2026_07_28.md` §C2, S3, hand-audited) reaches the same
   conclusion via the K² necessary condition; the G1-a agent was deliberately never shown it.

**Tier: B**, inherited from the family's own certification tier (the argument is exact symbolic
mathematics, but the object it constrains — the cooper_s7 family with T ≅ U⊕⟨14⟩ — is itself
Tier B, E-011/U1). Scope guard carried forward verbatim: this does NOT claim no CY exists over
these bases by any construction — only that the naive-pullback route is closed; the twisted
alternative is untested by both routes.

### R2. Ladder ruling: Option 1 (K²=0 revision, dP9 first), hard-gated on O1, plus a bounded scoping pass on Option 2

Of the four options in the decision request, T0 rules: **revise the B₂ ladder to K²=0 bases
with dP9 (degree-9 del Pezzo / rational elliptic surface) as the first rung — but no rung is
attempted until O1 (deg ℒ_curve for cooper_s7 itself) is computed.** In parallel, a bounded
desk-scoping memo (no code, no proof attempts) on the twisted-Weierstrass construction is
authorized so Option 2 is warm if O1 kills dP9. G1-b remains held pending Deep Think's
adversarial read (sequencing unchanged).

**Justification, point by point:**

1. **O1 is load-bearing, cheap, and decision-resolving.** Both routes agree: if
   deg ℒ_curve = 1, dP9 is admissible and the rung proceeds; if ≥ 2, dP9 is obstructed by the
   same arithmetic that killed F_n, and the twisted construction becomes the primary route.
   Computing O1 first converts the Option-1-vs-Option-2 strategic bet into a computed fact —
   this is why the ruling can be issued now rather than deferring: the ruling's own branch
   point is mechanical once O1 lands. **O1 is authorized to launch immediately** (it is
   decision input, not a new rung commitment).
2. **Convergent independent endorsement of dP9.** Deep Think proposed it as the fix (audit
   §C3, conditional); the in-house checker's own positive control independently landed on dP9
   and solved its Hodge-bundle degree exactly (ℓ = 1, matching the classical rational-
   elliptic-surface fact). Caveat kept explicit: that control solved dP9's *own* generic
   fibration — it does not transfer to cooper_s7, which is exactly why O1 gates.
3. **dP9 avoids reopening G0.** The decision request's open scoping question — G0's U-summand
   argument is certified fiberwise and might need re-derivation on a non-simply-connected base
   — does not fire for dP9 (rational, simply connected). Of all K²=0 candidates (dP9, other
   rational elliptic surfaces, K3, abelian, bielliptic), dP9 is the only first rung that
   requires no G0 rework. Cheapest admissible step first.
4. **Option 4 (pause) rejected.** The structural negative is already documented per house
   style (decision log §8 + result brief + this ruling); pausing adds no information while a
   cheap decisive computation (O1) is on the table. A documented dead end is a result — and it
   has been documented; that discharge is complete.
5. **Full-effort Option 3 rejected; bounded scoping authorized instead.** The twisted
   construction is a larger untested undertaking (needs an explicit Weierstrass-type
   presentation of the M-polarized family directly on B₂). Committing T1 effort before O1
   resolves would risk duplicating or wasting work; a T2/T1 desk memo (what would the twisted
   presentation require, what are the first obstructions, rough cost) keeps the program from
   cold-starting on the ℓ≥2 branch.
6. **O2/O3 are routed to Deep Think**, not blocked on locally: the dP9-section vs
   even-ramification conflict (O2) and the Halphen parity sketch (O3) are G1-b-shaped
   questions, and G1-b is exactly what Deep Think's outstanding adversarial read covers. See
   the companion brief (§2, action 2).

### R3. Outbound Deep Think brief approved for relay

`briefs/DEEPTHINK_ALIGNMENT_BRIEF_2026_07_29.md` (S3) is approved as the T0s work order:
O1 independent computation, O2/O3 resolution, the still-outstanding G1-b adversarial read, and
a feasibility scoping of the twisted construction — plus adversarial review of ruling R2
itself (T0s's defined role includes checking T0's decisions).

---

## §2 — Actions on Xavier's side (priority order)

1. **URGENT — GitHub token revocation sweep (browser-only, unchanged from 2026-07-28).**
   At github.com/settings/tokens: revoke (a) the OLD broad-admin-scope classic PAT formerly in
   `.bashrc` (replaced locally, still valid server-side), (b) the NEW broad-scope classic PAT
   currently in `.bashrc` (pasted in plaintext in chat — exposed-on-arrival), and audit (c)
   the earlier git-remote-URL exposure. Replace with one fine-grained, repo-scoped PAT
   (Contents: R/W on the 3 program repos only), then update `.bashrc` and re-test `git push`.
   *Rationale: two live tokens with admin scopes have each been printed in transcripts;
   classic PATs cannot be revoked via API, so no agent can do this for you. Every day open is
   exposure with full-admin blast radius.*
2. **Relay the Deep Think brief** (`DEEPTHINK_ALIGNMENT_BRIEF_2026_07_29.md`, S3) to Deep
   Think manually, as before. *Rationale: three of the five open questions gating G1-b (O1
   independently, O2, O3) are exactly T0s's defined lane — adversarial derivation work — and
   the G1-b read has been outstanding since yesterday's brief; this refreshes that ask with
   the G1-a result Deep Think hasn't seen.*
3. **Countermand window on ruling R2** — if you disagree with dP9-first-gated-on-O1 (e.g. you
   want the twisted construction primary, or a full pause), say so before **2026-07-30 EOD**;
   silence = proceed. *Rationale: the autonomy mandate batches T0-only decisions, but a ladder
   revision redirects the program's main geometric effort — you get the same countermand
   window the grid pin got (D1 precedent).*
4. **Optional but recommended — green-light S1 paper drafting kickoff.** All five PLAN.md §5
   framing questions are resolved (S1 `e621f6a`: unified paper, *Experimental Mathematics*,
   sole-author + mandated AI-acknowledgment wording, ρ=19/T=3 as conditional Tier-B
   proposition, hash-pinned internal citation). Drafting is unblocked and is the one major
   workstream needing no external input and no gate. *Rationale: it parallelizes cleanly with
   the O1/Deep Think wait; recommend starting with the certificate-backed lattice sections
   (LIVE results), leaving the G1 narrative section last since the ladder story is still
   moving.*

---

## §3 — Program scoreboard (achievements as of 2026-07-29)

Epistemic ledger in each repo's CLAUDE.md remains authoritative; tiers restated here for the
reader's convenience, not as a new source.

**Mathematical results (Streams 1–2):**
- **L₃ = Sym²(L₂) — Tier A** (Lean kernel-proven).
- **T ≅ U⊕⟨14⟩ (U1 closed) — Tier B, double-verified**; ρ=19 / T=3 — Tier B (E-011),
  independently cross-checked via the Nikulin complement route.
- **G0: NS ≅ U⊕E8(-1)⊕E8(-1)⊕⟨-14⟩, rank 19, cyclic discriminant group of order 14 — Tier B,
  LIVE, three fully independent verification lineages** (two in-house Sonnet routes agreeing
  bit-for-bit on the Gram matrix; coordinator reproduction + 5-control suite; Deep Think
  zero-shot re-derivation, hand-audited). The strongest cross-verified result in the program.
- **G1-a: structural negative, LIVE as of this ruling (R1)** — the naive-pullback ladder
  (P², all F_n) is closed, exactly and ℓ-independently, with P² additionally proven
  categorically inadmissible (no map to any curve exists — Picard-lattice isotropy + Bezout
  corroboration). Independently converged with Deep Think's Trap 1 via an uncontaminated
  route. Documented dead ends are results: this one eliminates the default construction and
  redirects the search to K²=0 bases / twisted presentations.
- **Stream 1 paper**: 33 pp, 10 sections drafted; every framing question resolved; drafting
  formally unblocked.

**Empirical infrastructure (Stream 3) — all validated, pre-registration intact:**
- **ANALYSIS_PROTOCOL LIVE** (covariance design, nuisance profiling, masking fix per Ravoux
  et al. 2023 window correction; taueff (0.3, 1.8) formally recorded as a prior-box, not
  trained support).
- **56-cell grid (8 masses × 7 fractions) pinned** (`27cff4a`), built-in controls PASS: f=0
  column byte-identical across masses, null-mass row max deviation 1.72% (threshold 10%),
  positive-control mass contrast 35× (`wp_e6_grid_controls_report_2026_07_28.json`).
- **Full pipeline timing GO**: N=50 mocks = 12.0 s end-to-end (99.2% in sim_spectra),
  N=200 ≈ 48 s (`WP_P2t_DESISIM_TIMING_2026_07_28.md`) — the Hartlap-corrected 16×16
  covariance run is cheap.
- **Primary galaxy sample verified**: eBOSS LRGpCMASS 377,458 rows (= published count, MATCH),
  eBOSS-only comparator 174,816 (MATCH); occupancy ratification fit-for-purpose YES, zero rows
  outside 0.6 ≤ z < 1.0, randoms ≈51× data (`WP_E7o_OCCUPANCY_RATIFICATION_2026_07_28.md`).

**Process achievements:** producer ≠ verifier held on every promotion; an uncontaminated
two-model cross-check protocol caught nothing wrong and confirmed everything twice (G0, G1-a);
one 114× timing underestimate was caught by scope-checking a subagent's deliverable against
what it literally measured — before it could mislead the covariance design.

---

## §4 — Scientific interpretation (tier-disciplined)

**What is established (Tier B, machine-checked):** the program's selected K3 surface
(cooper_s7) now has a fully identified lattice-theoretic skeleton — transcendental lattice
T ≅ U⊕⟨14⟩, Néron–Severi lattice NS ≅ U⊕E8(-1)²⊕⟨-14⟩ of rank 19 — verified through three
independent lineages, and its generic fiber admits an elliptic fibration with section
(the U summand), certified fiberwise. This is the complete "identity card" a geometer needs
before attempting to build the surface into a higher-dimensional compactification.

**What G1-a means:** the cheapest imaginable route to that compactification — pulling the
K3 family back over the textbook rational bases (P², Hirzebruch surfaces) — is now *provably*
closed, not merely unpromising. If a Calabi-Yau realization of this family exists, it must
live over a base with K²=0 (dP9 being the canonical first candidate, endorsed independently
by both review routes) or arise through a twisted Weierstrass-type construction. This is a
genuine narrowing of the search space by exact mathematics, and it is the program's second
externally cross-validated result in two days.

**Astrophysical reading (Tier C — every claim here is conjecture, marked as such):** the
program *conjectures* that this K3's topological data would, through a yet-to-be-exhibited
F-theory compactification (an explicit X₄/B₃ — Phase M gate M1′, currently dormant),
determine parameters of a dark sector. No observable prediction is claimed or permitted until
B₃ is exhibited (the F5b Tier C block stands unchanged). Independently of that conjecture,
Stream 3's pre-registered pipeline is now fully validated to test whether a mixed
ultralight-dark-matter component (mass m, fraction f, over the pinned 56-cell grid) is
consistent with the Lyman-α forest 1-D flux power spectrum — a standard, self-contained
astrophysical constraint that stands on its own regardless of the K3 conjecture's fate.
G1-a does not falsify the conjectured bridge; it proves the bridge, if it exists, cannot be
the naive one — and points, with two independent reviewers agreeing, at where to look next.

---

## Sources

- `briefs/T0_DECISION_REQUEST_G1a_LADDER_2026_07_28.md` (the request ruled on here)
- `briefs/G1a_CY_CONDITION_RESULT_2026_07_28.md` (`d6146c4`), `briefs/G0_NS_GENUS_RESULT_2026_07_28.md`
- `briefs/DEEPTHINK_DEBRIEF_AUDIT_2026_07_28.md` (S3 — canonical audit; verbatim archive not citable)
- `briefs/WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md` §8 (decision log, updated with this ruling)
- S3: `WP_P2t_DESISIM_TIMING_2026_07_28.md`, `WP_E7o_OCCUPANCY_RATIFICATION_2026_07_28.md`,
  `wp_e6_grid_controls_report_2026_07_28.json`, `T0_MF_GRID_DEFINITION_2026_07_27.md`

---
Generated-by: Fable 5 (T0) | Verified-by: every number traced inline to a named certificate,
brief, or pinned report — no new computation performed in this document | Reviewed-by: T0 Y
(this document is itself the T0 ruling; Xavier countermand window open until 2026-07-30 EOD)
