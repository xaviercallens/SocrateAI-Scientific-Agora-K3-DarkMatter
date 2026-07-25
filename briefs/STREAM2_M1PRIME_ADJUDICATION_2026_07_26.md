# T0 Adjudication — Deep Think M1 Proposal "Topological EFT via Chameleon Screening"

**Date:** 2026-07-26 · **Adjudicator:** Fable 5 (T0-delegated, decision authority per D2) ·
**Proposal:** `briefs/DEEPTHINK_M1_PROPOSAL_AS_RECEIVED_2026_07_26.md`
**Xagainst:** the accepted M1 (`STREAM2_M1_MECHANISM_MEMO_2026_07_26.md`) + ESCALATIONS E-007/E-008 + T0 decisions D1–D4

## Verdict: **RETURNED — not adopted as filed. Two components salvaged with conditions.**

The proposal is a genuinely better piece of physics thinking than the directive's own
framing anticipated — it correctly abandons [A-DD], honestly drops Wall 3, and lands its
observable inside the WP-R6/R7 envelope. But it is **written against a geometry that no
longer exists**, and two of its three wall-routes are premised on that retracted geometry.
I cannot pin it as M1. I adjudicate it component by component so the salvage is explicit.

---

## A. Premise audit (mandatory, per the standing rule)

The proposal self-dates 2026-07-25 and its §1 anchors on *"cooper_s7: ρ=4, T=18, 2× Type
II fibres."* **All three are retracted** (E-007) and the L₃ fallback refuted (E-008). This
is not the proposal's fault — it predates both findings — but it is disqualifying for the
parts that lean on them.

| Proposal element | Depends on retracted geometry? | Disposition |
|---|---|---|
| Wall 1 route (Argyres–Douglas from "Type II cusps") | **YES** — there are no certified Type II fibres; no certified fibre of any type | ❌ **Struck** |
| Wall 2 route ("T=18 ⇒ 15 moduli", Kulikov/SDC decoupling to a rank-3 chameleon) | **YES** — T is unknown; "15" is uncomputable | ⚠️ **Struck as stated; salvageable structure** |
| Wall 3 route (honest drop of dark energy) | NO | ✅ **Adopted** — coincides with D4 / A-DE |
| §3 envelope (r_s ≥ 0.27 Mpc; β₁/β₂; absolute thresholds; no shear) | NO | ✅ **Adopted as the standing envelope spec** |
| §4 sibling list; §5 kill condition | NO | ✅ **Adopted** |

## B. Component rulings

**B1 — Wall 1 (Argyres–Douglas dark sector): STRUCK.**
The route reads a strongly-coupled non-Lagrangian sector off "Type II cusps." No Type II
cusp is certified — E-007 retracted the label, and E-008 shows no Kodaira type is derivable
from L₂ *or* L₃. An AD sector conjured from a fibre type we do not have is assumption-stacking
on a withdrawn premise (Rule 7). *Its falsifiable consequence (β₂ void suppression vs ΛCDM)
is well-formed and worth keeping — but it must attach to a gauge-sector origin that survives
Route γ, not to Type II.*

**B2 — Wall 2 (chameleon from a surviving rank-3 subspace): STRUCK AS STATED, STRUCTURE SALVAGED.**
"T=18 leaves 15 moduli, of which a rank-3 chameleon survives" is unstatable today (T unknown).
**But the proposal independently arrives at exactly the mechanism WP-B1 already formalizes**
— a chameleon scalar that screens in dense regions and mediates only in voids. That is not a
coincidence to discard: it means the two independent lines (Deep Think's EFT reasoning, and
the kernel-verified `Structures/B1_Chameleon.lean`) agree on the *form* of the mechanism.
What neither can supply yet is the *derivation of its constants* from certified geometry —
which is precisely the WP-B1 → S3-00 gap and the E-008 blocker. **Salvage:** the chameleon
mechanism is retained as the program's working mechanism hypothesis (it already was, via
WP-B1); the Kulikov/SDC *justification story for why rank-3 survives* is deferred until Route
γ yields a real transcendental lattice to count against.

**B3 — Wall 3 (drop dark energy): ADOPTED.** Identical to D4; already standing policy A-DE.

**B4 — §3 envelope: ADOPTED as the binding observable spec** for any future M1′, subject to
one correction from the D3 mirror re-verification: the proposal says "exclude β₀… β₁/β₂";
the mirrored data shows **β₁ *alone* is 29/30, not 30/30** (one zero-variance cell:
fornax·50%·angular_csr). So the spec must read **"β₂, or the β₁/β₂ pair, or β₁ at threshold
> 50% / scheme ≠ angular_csr"** — not "β₁ or β₂" unconditionally. With that edit the envelope
is sound and I adopt it.

## C. The one thing that could be tested today — and was

The proposal's real value is that it forces the question: *does the surviving path (Route γ)
even have a starting point?* I tested Route γ's foundational step now rather than waiting.

**Route γ step 0 — CONFIRMED** (`checkers/check_route_gamma_step0.py`,
`data/certificates/ROUTE_GAMMA_STEP0.json`):

```
g.f.(A002652) = F(t(q))   where t = A279618 (level-7 Hauptmodul), F = g.f.(A279619)
CONFIRMED exactly to order 29.
```

This matters two ways: (1) the Hauptmodul `t` **is** the correct uniformizing coordinate for
the pullback — Route γ has a genuine starting point, not a hoped-for one; (2) the composition
**self-validates** the (OEIS-synthesized) A279618 b-file — wrong Hauptmodul coefficients could
not reproduce the independently-fetched A002652 (genuine 5008-term b-file) at every order.

**Scope guard, stated in the certificate:** this establishes *only* that the composition is
real. It yields **no ρ, no T, no Kodaira type, and does not show the pulled-back operator is
unipotent** — that is Route γ **step 1**, still open. No number was emitted.

## D. Decision and instruction

1. **The accepted M1 stands** as the file of record (conditional negative, D2). This proposal
   is recorded alongside it as `DEEPTHINK_M1_PROPOSAL_AS_RECEIVED_2026_07_26.md`, **adjudicated
   RETURNED**, with B1/B2 struck and B3/B4/§4/§5 folded forward.
2. **Phase M stays dormant.** Nothing here reopens M2. The proposal's own §5 kill condition
   (no r_s ≥ 0.27 Mpc without an unconstructed scenario ⇒ halt) is adopted verbatim and will
   bind M2 if it ever opens.
3. **Route γ is now a two-step ladder with step 0 cleared.** A revised **M1′** may be drafted
   *only after* Route γ step 1 (unipotency of the pulled-back operator) is tested and passes —
   at which point Walls 1 and 2 become posable in real quantities and this proposal's struck
   routes can be re-attempted honestly. If step 1 fails, the geometric leg closes and the
   program files its clean third negative.
4. **Two-model rule engaged for whenever M2 opens:** this proposal is Deep Think's derivation
   sketch; the blind re-derivation partner is Fable 5. Neither has produced a physical
   derivation yet (both blocked at Route γ step 1), so there is nothing to adjudicate into
   DERIVATION_DISPUTES.md today — only the shared mechanism *form* (chameleon), which both
   independently favor.

---

**Generated-by:** Fable 5 (T0-delegated adjudication) | **Verified-by:** premise table → E-007/E-008; Route γ step 0 → `checkers/check_route_gamma_step0.py` (CONFIRMED order 29); β₁ correction → `stream3_mirror/README.md` | **Reviewed-by:** Xavier (T0) — countermand window open
