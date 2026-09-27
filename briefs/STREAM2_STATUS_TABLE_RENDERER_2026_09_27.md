# Stream 2 — K3_CRITERIA §5 status table restored by a renderer; two findings; mirror re-pin

**Date:** 2026-09-27 · **From:** Stream 2 · **To:** T0 (Xavier); Stream 1 and Stream 3 (mirror
holders) · **Nature:** mechanical-item closure + two flagged findings. **No criterion, threshold,
verdict or certificate was changed.**

## 1. What was done

`K3_CRITERIA.md` §5 carried an in-band open item (2026-09-21): write
`scripts/render_status_table.py` (reading certificates only), then restore a generated table. It is
now written, and §5 holds its output between explicit BEGIN/END markers.

- **Inputs, and nothing else:** the §1 register, `refs/recurrences_v1.json`, and the certificates
  named in the script's `SOURCES` map. Each map entry cites the record that makes that certificate
  the source of record (e.g. C2 s7 → `C2_cooper_s7_v5.json` per T0 D5′, not v4, which still
  self-reports "LIVE v4").
- **Row identity is derived, not typed.** Each register row's Cooper params (a,b,c,d) must reproduce
  exactly one refs entry's recurrence coefficients (exact, sympy). All three live rows match
  uniquely. In particular, `K-s18` (register params from Gorodetsky) is the refs entry
  `avs_sporadic3_s18` (read from Almkvist–van Straten), which confirms the two transcriptions agree
  on the recurrence.
- **Fail-closed:** a missing, retracted (in-band `RETRACTED` block or verdict), wrong-candidate,
  wrong-producer or field-missing source makes the render **refuse**. A `PASS(N)` whose N differs
  from `order_checked` also refuses, as does a checker named in `SOURCES` that is absent from
  `checkers/`. A DRAFT lattice certificate renders `DRAFT (ADVISORY)`, which is neither a pass nor a
  failure (§4).
- **Byte-stable:** no dates, git stamps, checker versions or hashes reach the table, so the
  regression run's stamp refresh cannot change `K3_CRITERIA.md`.
- **Controls:** `checkers/test_render_status_table_controls.py`, 20 checks, all run on temp copies:
  one positive round-trip plus N1–N15 (flipped verdict changes the cell; each refusal case refuses;
  hand-edited §5 makes `--check` exit 1; stamp changes leave the table identical). All pass.
- **Regression:** `render_status_table.py --check` and the controls are added to `TODO.md`
  §Regression.

**What the table does not do:** it scores nothing and ranks nothing, adds no reading to any
criterion, and does not adjudicate the frozen §1 rows. Struck rows `K-S22` and `K-t103` are listed
as §1 states them, and the t103 question stays with T0. C6 is rendered without counts, because CM
points are dense and a certificate lists a window.

## 2. Findings (flagged, not fixed)

**F-a — §2 C3 names a checker that is not in the repository of record.** The C3 symbolic route
cites `checkers/check_C3_sym2.py`. That file is not in this repo. It exists in Stream 3's Home repo
and, per `briefs/STREAM2_TO_STREAM3_C3_BRANCH_REPLY_2026_09_21.md`, covers the `d = 0` case only, so
it cannot run on either register primary. The operator identity that C3 asks for is certified here
by `check_C3b_symsqrt.py`, and AM-2 (adopted, D8′) cites exactly `C3b_symsqrt_cooper_s7/s10.json` as
C3's evidence. The renderer therefore reads C3 from those certificates and states that in a footnote
under the table. Correcting §2's checker path is an amendment to the canonical file, so it goes
through the §6 protocol. **Ask (T0):** authorize a §6 amendment replacing the C3 route-1 checker path
with `checkers/check_C3b_symsqrt.py`, or rule otherwise.

**F-b — `T3_LEVEL_CONSISTENCY.json` self-reports a superseded status.** Its top-level `status` says
"PROPOSAL STAGE — T3 is not an adopted gate". T3 was adopted as an unscored consistency gate by
D8′/AM-4 on the same day. The string is hardcoded at `checkers/check_T3_level_consistency.py:346`
(and in the console banner at :307). The renderer does not read this field, only the per-candidate
`results` block, so the table is unaffected. **Proposed fix (Stream 2, not done here):** edit the
string and re-emit the certificate wording-only, with a value diff of zero. This follows the D7′
re-emission precedent and belongs in a separate commit.

**Related, no action needed:** the C3b column (explicit Shioda–Inose map F) reads `no certificate`
for every row. The only `check_C3b_moduli_map.py` certificates for s7/s10 are the `*__apery_zeta2`
pairings, which are a ruled-out partner test, and the renderer never reads them as a row's C3b
status. Whether some existing certificate should be designated as C3b's source is a question for
T0, not something the renderer infers.

## 3. Mirror holders — re-pin needed

`K3_CRITERIA.md` changed in §5 (history note + generated table) and in header item (b). Nothing else
changed.

| | SHA-256 |
|---|---|
| before (`main` @ `749a3e6`) | `7e18fa07eecc6864a746c52834c637bfe501ad30407eb7585e8850d1d65633e6` |
| after (this branch) | `993350cf9f04a750f2d282b1daa7caef7b63d117a7e399632e13c46c59a5e1ae` |

**Stream 1 / Stream 3:** refresh your mirror from `main` after merge and re-pin the hash. The file
will not change again from certificate stamp refreshes, only when a verdict or the register changes.

---
*Generated-by: Claude (Opus 5.5), Stream 2 | Verified-by: `checkers/test_render_status_table_controls.py`
(20/20), `scripts/render_status_table.py --check`, `scripts/check_tier_language.py` | Reviewed-by: N*
