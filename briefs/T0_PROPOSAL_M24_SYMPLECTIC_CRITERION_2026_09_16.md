# T0 PROPOSAL — M24/Mukai symplectic-automorphism criterion for K3 selection

**Date:** 2026-09-16 | **Status:** PROPOSAL — not authorized, not implemented, no checker exists yet
**Branch:** `sandbox/m24-moonshine-criterion-2026-09-16` (this file only; nothing on `main`)
**Requested by:** Xavier Callens ("continue stream 3 with experimentation of K3 selection
based on K3 M24 Mathieu moonshine inspired from other science domain")
**Author:** Claude (Sonnet 5), this session | **Reviewed-by:** T0 pending

---

## 0. Reading the request, and where it actually routes

K3 selection is Stream 2's function (`K3_SELECTION_REPORT.md`, PREDICTION.md §2); Stream 3
consumes a certified pair, it doesn't select one. So "continue Stream 3 with M24-inspired
selection" is, mechanically, a **proposed new Stream-2 criterion** that would only reach
Stream 3 after a candidate is certified against it. This brief stays in S2 for that reason;
Stream 3 does nothing until S2 produces a result.

**Housekeeping done this session, reported for the record:** the local Stream 3 checkout
(`~/SocrateAI-Scientific-Agora-Home`) had been lost — the symlink pointed at a gitignored
data-offload directory (`raw/` only, no repo). Re-cloned from
`github.com/xaviercallens/DarkMatterK3-Home.github.io` to
`/mnt/disks/disk-socrateai-local-1/callensxavier_home_data/DarkMatterK3-Home.github.io`
(HEAD `21cbb3d`, matches `origin/main`), re-linked `data/raw` to the recovered raw-data
directory, and re-pointed the home symlink at the real repo. No repo content was lost;
this was a mount-path problem, not a data-loss problem.

---

## 1. Two different "K3 + M24" connections exist — this proposal picks one, explicitly

"Mathieu moonshine" most commonly means the **Eguchi–Ooguri–Tachikawa (2010) observation**
that the K3 elliptic genus, expanded in N=4 superconformal characters, has non-negative
integer coefficients that match dimensions of M24 representations.

**That is not usable as a selection criterion.** The K3 elliptic genus is a
**deformation invariant** — every K3 surface (and every candidate in this project's pool:
cooper_s7, cooper_s10, Domb, …) has the *same* one. A criterion built on it would return
an identical verdict for every candidate and could not discriminate cooper_s7 from
cooper_s10, which is the whole point of Stream 2's pipeline. [Tier A — standard fact about
elliptic genera, stated here as textbook mathematics, not sourced to a project checker.]

**What does discriminate between candidates is Mukai's theorem**, already present as a
hash-pinned reference in this repo (`docs/literature/huybrechts_K3Global.txt`, "3. Finite
groups of symplectic automorphisms," Thm 3.1, cited verbatim below). It connects M23 (a
maximal subgroup of M24, and the group actually relevant to K3 surfaces per that same
section: *"Only M23 and M24 are (so far) relevant for K3 surfaces"*) to a K3's own lattice
data — data Stream 2 already certifies per candidate. This is the connection this proposal
develops. [Tier A — theorem statement, quoted from the pinned reference below.]

> **Theorem 3.1 (Mukai).** For a finite group G the following conditions are equivalent:
> (i) There exists a complex (projective) K3 surface X such that G is isomorphic to a
> subgroup of Auts(X) [the symplectic automorphism group].
> (ii) There exists an injection G ↪ M23 into the Mathieu group M23 such that the induced
> action of G on Ω := {1,…,24} has at least five orbits.
>
> There are exactly 11 maximal subgroups of finite groups acting faithfully and
> symplectically on a complex (projective) K3 surface. […] The orders of these maximal
> groups are |G| = 48, 72, 120, 168, 192, 288, 360, 384, 960 (some appearing twice).
>
> — Huybrechts, *Lectures on K3 Surfaces*, Ch. 15 §3 (`docs/literature/huybrechts_K3Global.txt`,
> lines 14538–14561, this repo, hash-pinned in `refs/MANIFEST.md` — verify hash before citing
> further; this brief did not re-verify it).

**Why Ω has 24 elements at all, and why that's the actual "M24 connection":** M23 and M24
arise here via the **Niemeier lattice with root system A1⊕24** and its Golay-code
construction — the *same* combinatorial object (24 points, Golay code, Mathieu group) that
generates Mathieu moonshine's characters, but arriving through **lattice/automorphism
theory (Nikulin, Mukai)**, not through the elliptic genus. Both routes touch M24 because
both ultimately trace to the Leech lattice / Niemeier lattice combinatorics; they are not
the same theorem and should not be conflated in any writeup. [Tier A, same reference,
§4 "Niemeier lattices," lines 13880–13910.]

---

## 2. What a criterion would actually check, concretely

**Not yet a checker — this is the proposal for what one would compute.**

For a candidate with a Stream-2-certified Néron–Severi lattice NS(X) (rank ρ, so
transcendental lattice T = NS(X)⊥ has rank 22−ρ), a finite group G can act symplectically
on that *specific* X only if G embeds into O(T) compatibly with the Nikulin/Mukai
invariant-lattice constraints — informally, the smaller T is (the larger ρ is), the more
room there is for a nontrivial symplectic G, and Nikulin's classification bounds which G
are compatible with a given invariant-lattice rank. This is the "lattice discriminates"
mechanism the advisor flagged before this brief was drafted: it is candidate-specific in
exactly the way the elliptic genus is not.

**Currently certified inputs this criterion could consume (verified against the actual
certificate JSON in this session, not from memory):**

| candidate | NS(X), rank(NS)=19 | T = NS⊥, rank 3 | status |
|---|---|---|---|
| cooper_s7 | U ⊕ E8(−1) ⊕ E8(−1) ⊕ ⟨−14⟩ | U ⊕ ⟨14⟩ | Tier B, **DRAFT — pending T0 review** (`data/certificates/G0_NS_genus_cooper_s7.json`) |
| cooper_s10 | U ⊕ E8(−1) ⊕ E8(−1) ⊕ ⟨−20⟩ | U ⊕ ⟨20⟩ | Tier B, **DRAFT — pending T0 review** (`data/certificates/G0_NS_genus_cooper_s10.json`) |

Both candidates have ρ=19 (T rank 3) — high Picard rank, which by the informal mechanism
above is the *favorable* regime for a nontrivial symplectic G to be lattice-compatible.
That is a plausibility remark, not a result; no group-theoretic computation has been run.

**What a checker (call it a new `check_C_symp.py`, pending T0 naming approval — this repo
already has a criterion-naming collision history, see `K3_SELECTION_REPORT.md` §"Stream 3
deployment instructions" footer) would need to do, per candidate:**
1. Take the certified T (already available, both candidates).
2. Determine which of the 11 Mukai maximal groups (or their subgroups) are compatible with
   embedding into O(T) — this is Nikulin's invariant-lattice-rank machinery, not something
   this brief derives; it requires a primary or secondary source with the actual
   rank/discriminant table (Mukai 1988; Kondō 1998 extended the classification; Xiao's
   79-group list and Hashimoto's discriminant table are cited in the pinned Huybrechts
   passage but the Huybrechts excerpt currently in `docs/literature/` does not itself
   contain that table — only the theorem statement and the order list above).
3. Emit a determination (compatible group(s) found / none found) exactly as other
   checkers do, with `[A-*]` assumption tags and a `PASS(N)`-style finite-check notation
   if any part of the computation is order-truncated.

**Gap blocking step 2, stated plainly:** the Nikulin rank/discriminant table is not yet in
`refs/`. Nothing about which specific group(s) are compatible with s7's or s10's T may be
asserted until that table is fetched and hash-pinned (anti-hallucination rule, same
discipline as the AZ-sporadic gap in `K3_SELECTION_REPORT.md` §4.1). This brief does not
guess at it.

---

## 3. "Inspired from other science domain" — flagged, not answered

Xavier's phrasing asked for inspiration from another science domain. I am **not** supplying
one here. Moonshine-type phenomena (unexpected sporadic-group representation structure in
a generating function) have documented analogues outside K3/string theory — umbral
moonshine, and discussions of moonshine-adjacent structure in some condensed-matter and
CFT contexts are real published topics — but I have not fetched or hash-pinned a specific
source for any such analogy, and this project has three prior incidents (S2's Domb/A002893
false-relation episode, and two more logged in `session_log_2026_07_31.md` — a Discovery
PDF with 0/24 supported claims and a vacuous Lean "0 sorry" claim) all traced to exactly
this failure mode: cross-domain or cross-source claims asserted without a pinned citation.

**If Xavier has a specific domain or paper in mind** (the request reads as though one
exists — "inspired from other science domain" is oddly specific phrasing for an
unprompted idea), naming it turns this from a guess into a sourced lead. Otherwise the
next honest step is a literature-search task (general-purpose agent, read-only, output a
candidate list of *citations* — no claims — for T0 to pick from), not a guess written into
this brief.

---

## 4. Disposition requested

This is a **Track-B-style sandboxed proposal** (branch only, nothing on `main`), consistent
with how the last unrelated new-track discovery in these repos was handled
(`STREAM4_SANDBOX_DESIGNATION_2026_07_31.md` precedent). Asking T0 for one of:

1. **Authorize the checker** (§2) contingent on first fetching the Nikulin/Kondō
   rank-discriminant table into `refs/` — I can do the fetch+hash+checker as a normal WP.
2. **Supply or name the cross-domain source** (§3) so it can be fetched and pinned, or
   explicitly decline that part and keep this to the pure Mukai/lattice criterion.
3. **Hold** — file this as a proposal only, no further work until T0 reviews.

No number in this brief that isn't in the table in §2 or the quoted theorem in §1 has been
computed by me; nothing here should be cited elsewhere until T0 marks it reviewed.

---

Generated-by: Claude (Sonnet 5), this session | Verified-by: certificate JSONs read directly
(§2 table); Huybrechts excerpt grep'd directly, hash not re-verified this session (§1) |
Reviewed-by: T0 — **pending**
