#!/usr/bin/env python3
"""
test_partner_global_boundedness_controls.py -- negative controls for
check_partner_global_boundedness.py (A4).  R = real known-bads / known answers,
S = synthetic tamper.  Every refusal / negative verdict checks WHICH clause fired.

  R1  REAL known-bad: exp(z), a_n = 1/n!  (order 160) -> NO_C_FOUND, clause
      `prime_above_C_MAX_in_denominator`.  Not globally bounded (every prime occurs).
  R2  REAL known-bad: log(1+z)/z, a_n = (-1)^n/(n+1) -> NO_C_FOUND, same clause.
  R3  REAL known-bad on the OTHER clause: exp(z) cut at order 60 has only primes < 64 in
      its denominators, and still no c <= 64 works -> `no_c_in_box`.
  R4  REAL known-bad of square-root shape: sqrt(exp(z)) = exp(z/2) (input not integral, so
      the lemma does not apply) -> NO_C_FOUND, clause `prime_above_C_MAX_in_denominator`
      (asserted, as for every other negative verdict).
  R5  known answers, all three values of the lemma: sqrt(1+4z) -> c = 1, sqrt(1+2z) -> c = 2,
      sqrt(1+z) -> c = 4; and (1-4z)^(-1/2) (central binomials) -> c = 1.  The checker is
      therefore not a constant.
  R6  the s10 row is not vacuous: c = 1 fails at n = 2 exactly (17/2), c = 2 passes.
  S1  tampered register (s10 partner a_2 = 17/3 stored) -> refused,
      `recurrence_does_not_regenerate_stored_terms`.
  S2  tampered series (1/3 added to one coefficient of the s10 partner)
      -> least c changes from 2 to 6, prime 3 reported.
  S3  the closed-form test can fail: e(n) = n - 1 (the BOUND, read as an equality) is
      refuted at n = 3.
  S4  formal_sqrt refuses a_0 != 1 -> `constant_term_not_one`.
  S5  a_n = 2^(-n^2): only the prime 2, yet NO_C_FOUND on `no_c_in_box`.
  S6  exit-code gate: checks_ok is False on a False, on 0, and on a missing-True value.
  S7  the two code paths are compared: a forged per-prime result raises `two_paths_disagree`
      (exercised by monkeypatching factor_small to hide the prime 2).
  R7  REAL known-bad for the anti-phantom citation check: the real Stream 1 file FormalSqrt.lean
      mentions `sqrtSeq_dyadic` in its header comment long before the theorem.  A citation keyed
      on the bare name (the defect found in review) must NOT be located at that comment line:
      the bare name starts no line -> PHANTOM; `theorem sqrtSeq_dyadic` -> the statement line,
      which is later than the first mention.
  S8  a source that only MENTIONS a theorem in a comment -> PHANTOM.
  S9  register-vs-template gate can fail: one coefficient of the registered s10 partner
      recurrence changed (15 -> 16) -> `order2_recurrence_is_template` False, the other three
      s10 clauses and all s7 clauses unchanged.
"""
import json
import pathlib
import sys
import tempfile
from fractions import Fraction
from math import comb, factorial

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_partner_global_boundedness as G

results = []


def record(name, ok, detail):
    results.append({"control": name, "behaved": bool(ok), "detail": detail})
    print(("ok   " if ok else "FAIL ") + name + " :: " + detail)


def binom_half_series(scale, N):
    b, out = Fraction(1), [Fraction(1)]
    for k in range(1, N + 1):
        b = b * (Fraction(1, 2) - (k - 1)) / k
        out.append(b * scale ** k)
    return out


N = G.N_ORDER
expz = [Fraction(1, factorial(n)) for n in range(N + 1)]
r = G.boundedness(expz)
record("R1", r["verdict"] == "NO_C_FOUND" and r["clause"] == "prime_above_C_MAX_in_denominator",
       f"exp(z): {r['verdict']} / {r['clause']}; first primes above C_MAX {r['primes_above_C_MAX'][:3]}")
r = G.boundedness([Fraction((-1) ** n, n + 1) for n in range(N + 1)])
record("R2", r["verdict"] == "NO_C_FOUND" and r["clause"] == "prime_above_C_MAX_in_denominator",
       f"log(1+z)/z: {r['verdict']} / {r['clause']}")
r = G.boundedness(expz[:61])
record("R3", r["verdict"] == "NO_C_FOUND" and r["clause"] == "no_c_in_box" and max(r["denominator_primes"]) < 64,
       f"exp(z) to order 60: {r['verdict']} / {r['clause']}; largest prime {max(r['denominator_primes'])}; "
       f"unbounded formula c has {len(str(r['c_formula_unbounded']))} digits")
sq = G.formal_sqrt(expz)
r = G.boundedness(sq)
record("R4", sq == [Fraction(1, factorial(n) * 2 ** n) for n in range(N + 1)] and r["verdict"] == "NO_C_FOUND"
       and r["clause"] == "prime_above_C_MAX_in_denominator",
       f"sqrt(exp z) equals exp(z/2) exactly to order {N}; {r['verdict']} / {r['clause']}")
got = [G.boundedness(binom_half_series(s, N)).get("c") for s in (4, 2, 1)]
cb = G.boundedness([Fraction(comb(2 * n, n)) for n in range(N + 1)]).get("c")
sq_ok = G.formal_sqrt([Fraction(1), Fraction(4)] + [Fraction(0)] * (N - 1)) == binom_half_series(4, N)
record("R5", got == [1, 2, 4] and cb == 1 and sq_ok, f"sqrt(1+4z), sqrt(1+2z), sqrt(1+z) -> c = {got}; central binomials c = {cb}; "
       f"formal_sqrt(1+4z) equals the binomial series: {sq_ok}")
reg = json.loads(G.REFS.read_text())["sequences"]
s10p = G.register_terms(reg["cooper_s10_partner"], N + 1)
r = G.boundedness(s10p)
fail1 = next(n for n, x in enumerate(s10p) if x.denominator != 1)
record("R6", r["c"] == 2 and fail1 == 2 and s10p[2] == Fraction(17, 2), f"c = 1 first fails at n = {fail1} (a_2 = {s10p[2]}); least c = {r['c']}")

tam = json.loads(G.REFS.read_text())
tam["sequences"]["cooper_s10_partner"]["initial_terms_rational"][2] = "17/3"
with tempfile.TemporaryDirectory() as d:
    p = pathlib.Path(d) / "refs.json"
    p.write_text(json.dumps(tam))
    try:
        G.run(n_order=30, refs_path=p)
        record("S1", False, "tampered register accepted")
    except G.Refusal as e:
        record("S1", e.clause == "recurrence_does_not_regenerate_stored_terms", f"refused: {e.clause}")
t = list(s10p)
t[5] = t[5] + Fraction(1, 3)      # (dividing by 3 is no tamper: the numerator 73647 is divisible by 3)
r = G.boundedness(t)
record("S2", r.get("c") == 6 and 3 in r["denominator_primes"], f"least c {r.get('c')}, primes {r['denominator_primes']}")
e2 = G.boundedness(s10p)["e_p"]["2"]
mism = [n for n in range(1, N + 1) if e2[n] != n - 1]
record("S3", bool(mism) and mism[0] == 3, f"'e(n) = n - 1' refuted first at n = {mism[0] if mism else None} "
       f"(e = {e2[3]}); {len(mism)} mismatches to order {N}")
try:
    G.formal_sqrt([Fraction(2), Fraction(1)])
    record("S4", False, "accepted")
except G.Refusal as e:
    record("S4", e.clause == "constant_term_not_one", f"refused: {e.clause}")
r = G.boundedness([Fraction(1, 2 ** (n * n)) for n in range(40)])
record("S5", r["verdict"] == "NO_C_FOUND" and r["clause"] == "no_c_in_box" and r["denominator_primes"] == [2],
       f"{r['verdict']} / {r['clause']}; primes {r['denominator_primes']}")
record("S6", not G.checks_ok({"a": True, "b": False}) and not G.checks_ok({"a": 0}) and not G.checks_ok({"a": 1})
       and G.checks_ok({"a": True}), "checks_ok requires `is True`")
orig = G.factor_small
G.factor_small = lambda m: {p: e for p, e in orig(m).items() if p != 2}
try:
    G.boundedness(s10p)
    record("S7", False, "forged path accepted")
except G.Refusal as e:
    record("S7", e.clause == "two_paths_disagree", f"refused: {e.clause}")
finally:
    G.factor_small = orig

src = G.lean_source("Agora/Sequences/FormalSqrt.lean", "5cabc83")
first_mention = next((i + 1 for i, l in enumerate(src.splitlines()) if "sqrtSeq_dyadic" in l), None)
bare = G.verify_citations([("Agora/Sequences/FormalSqrt.lean", "sqrtSeq_dyadic", "5cabc83")])[0]
full = G.verify_citations([("Agora/Sequences/FormalSqrt.lean", "theorem sqrtSeq_dyadic", "5cabc83")])[0]
record("R7", first_mention is not None and bare["status"] == "PHANTOM" and full["status"] == "VERIFIED"
       and full["line"] > first_mention,
       f"first mention of the name at line {first_mention} (a comment); bare-name citation: {bare['status']}; "
       f"declaration-keyed citation: {full['status']} at line {full['line']}")
fake = lambda path, commit: "/- see `theorem foo_bar` below; theorem foo_bar is great -/\n-- theorem foo_bar\n"
c = G.verify_citations([("X.lean", "theorem foo_bar", "0000000")], reader=fake)[0]
record("S8", c["status"] == "PHANTOM" and c["line"] is None, f"comment-only mention: {c['status']}")
tam = json.loads(G.REFS.read_text())["sequences"]
rp = tam["cooper_s10_partner"]["recurrence_python"]
assert rp.count("+15)") == 1
tam["cooper_s10_partner"]["recurrence_python"] = rp.replace("+15)", "+16)")
tr = G.template_transcription(tam)
fired = [f"{f}.{k}" for f, v in tr.items() for k, x in v.items() if x is False and k != "ok"]
record("S9", fired == ["s10.order2_recurrence_is_template"] and tr["s7"]["ok"] and not tr["s10"]["ok"],
       f"clauses fired: {fired}")

out = G.ROOT / "data" / "certificates" / "PARTNER_GLOBAL_BOUNDEDNESS_controls.json"
out.write_text(json.dumps({"controls_for": "checkers/check_partner_global_boundedness.py", "results": results,
                           "behaved": sum(r["behaved"] for r in results), "total": len(results),
                           "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: self (controls) | Reviewed-by: N"},
                          indent=1) + "\n")
print(f"{sum(r['behaved'] for r in results)}/{len(results)} controls behaved as required")
sys.exit(0 if all(r["behaved"] for r in results) else 1)
