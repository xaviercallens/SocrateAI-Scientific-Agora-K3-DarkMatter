# Stream 2: serialize the U1 U-splitting base-change witness P

**Date:** 2026-07-27 · **From:** Stream 2 · **Type:** mechanical, T0-ruled

## Motivation

Stream 1's independent verification of the U1 U-splitting claim
(`briefs/STREAM1_U1_INDEPENDENT_VERIFICATION_2026_07_27.md`, Stream 1 repo,
checker `checkers/check_U1_splitting_independent.py`) returned **PASS** on
`C2_cooper_s7_v4.json` (LIVE), but noted a finding: the certificate records
only `det(P)` and `PᵀGP` (as `basis_change_det` and `gram_after`), not the
base-change matrix `P` itself. `check_U1_lattice.py`'s `stage3_lattice()`
computes `P` (in-code variable `T = [f | e | w]`) in memory but never
serialized it, so Stream 1 had to write its own from-scratch construction to
re-derive a witness — which worked, but the honest gap remained: this repo's
own certificate wasn't self-contained.

**T0 RULING (Xavier, 2026-07-27, verbal via coordinator): APPROVED** —
serialize `P` in future certificate versions so no re-deriving is needed.

## What was done

1. `checkers/check_U1_lattice.py`, `stage3_lattice()`: the `splitting` dict
   now includes `basis_change_matrix` (P, nested int lists, columns
   `[f | e | w]`) alongside the existing `basis_change_det`, `d`, and
   `gram_after`. Pure addition — no existing field changed.
2. New `emit_cert_v5()` writes `data/certificates/C2_cooper_s7_v5_DRAFT.json`
   via a new `--emit-cert-v5` CLI flag. Its `derived` block is
   value-identical to `C2_cooper_s7_v4.json` (LIVE) except for the one new
   `basis_change_matrix` field; `status`/`provenance` explicitly say this is
   a DRAFT that does **not** supersede v4 and goes live only by a future,
   separate T0 acceptance.
3. `C2_cooper_s7_v4.json` (LIVE) and `C2_cooper_s7_v3.json` (runtime rank
   source) were **not re-run or edited** — the new flag writes only to the
   v5 path. SHA256 verified identical before and after:
   - v3: `898f0bb6213e79495ec10a1ac54c74bd0fdaf06aa0fe529f8dffa7c09fef268b`
   - v4: `036cd895db892aee9802514ec18668535f8896cee53cf6123533af9844387c3e`
     (matches the value recorded in Stream 1's brief)
   - v5 DRAFT (new): `5c906634666bfe470dc5a40c4f5d6d68619740a5470ac5df36bac130edadd1b5`
4. New checker `checkers/check_U1_witness_serialization.py` — loads a
   certificate, and if `derived.u_splitting.basis_change_matrix` is present,
   verifies with exact integer arithmetic (sympy `Matrix`, no floats) that
   `P` has integer entries, `det(P) = ±1` (and matches the certificate's own
   `basis_change_det`), and `PᵀGP` (G = the certificate's own
   `gram_primitive_even`) equals the certificate's own `gram_after`. If the
   field is absent, it reports `WITNESS_ABSENT` — a distinct, non-failing
   outcome — rather than FAIL, so `C2_cooper_s7_v3.json` (no `derived` block
   at all) and `C2_cooper_s7_v4.json` (predates this field) don't break.
   `--all` runs it against v3/v4/v5-draft in one pass.
5. New `checkers/test_U1_witness_serialization_controls.py` (6 controls,
   runnable via `python3` and `pytest`, both green): tampered `P` FAILS,
   non-unimodular `P` (det=2) FAILS at the `GL₃(ℤ)` gate, tampered
   `gram_after` FAILS, v4 and v3 both report `WITNESS_ABSENT` (not FAIL), and
   the unmodified v5 draft PASSes.

## Regression

All 11 original `TODO.md` §Regression commands plus the 2 new ones (13
total) ran green:
`python3 checkers/check_U1_witness_serialization.py --all` and
`python3 checkers/test_U1_witness_serialization_controls.py`.
`python3 scripts/check_tier_language.py` — 0 violations, 94 files.

## What this does and does NOT change

**Upgrades:** self-containedness of the audit trail — a third party can now
verify `PᵀGP = gram_after` directly from a single certificate file, exact
integer arithmetic, no re-derivation.

**Does NOT:** touch the LIVE `C2_cooper_s7_v4.json` or the rank source
`C2_cooper_s7_v3.json`; change any existing field's value anywhere; upgrade
the Tier-B status of the lattice-to-T identification or the numerics-to-exact
monodromy recognition step (both unchanged, per the v4/v5 `tier_reason`
field); make `C2_cooper_s7_v5_DRAFT.json` live — that requires a future,
separate T0 acceptance, exactly as v4_DRAFT → v4 required one.

---
Generated-by: Sonnet 5 (Stream 2) | Verified-by: `check_U1_lattice.py`
structural assertions + `test_U1_controls.py` +
`check_U1_witness_serialization.py` +
`test_U1_witness_serialization_controls.py` (6/6, python3 and pytest) +
full 13-command regression green | Reviewed-by: pending T0 acceptance of v5
