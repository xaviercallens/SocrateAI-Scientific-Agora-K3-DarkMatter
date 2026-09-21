#!/usr/bin/env python3
"""
check_partner_global_boundedness.py (A4) -- integrality of an order-2 partner series is
coordinate-dependent; report the least rescaling that makes it integral.

STATUS: an ATTRIBUTE TO REPORT.  Whether criterion C3 requires integrality of the partner is
an open T0 question; this checker does not answer it, scores nothing and ranks nothing.
No physical reading of any kind.

WHAT IS COMPUTED (all exact, fractions.Fraction / int; no float anywhere)
-------------------------------------------------------------------------
For a power series f = sum a_n z^n with rational a_n:

  * least c in {1, ..., C_MAX = 64} with c^n a_n in Z for every n <= N  -> "c_found", PASS(N),
    or NO_C_FOUND with the clause that fired:
        `prime_above_C_MAX_in_denominator`   a prime p > C_MAX divides some denominator
                                             (then no c <= C_MAX can work: exact for the box)
        `no_c_in_box`                        every c <= C_MAX fails at some n <= N
    Two code paths: brute force over c, and the per-prime formula
        c_formula = prod_p p^{max_n ceil(v_p(den a_n)/n)};  they must agree.
  * the p-adic denominator exponents e_p(n) = v_p(den a_n).

Series examined: every `order-2` entry of refs/recurrences_v1.json (terms regenerated from
`recurrence_python`, seeds = the first two stored terms, stored terms re-checked), and the
formal square root of every `order-3` entry.  For cooper_s7 / cooper_s10 the square root is
compared term by term with the registered partner (exact, PASS(N)).

WHAT IS PROVED, AND HOW MUCH OF THE PROOF IS MACHINE-CHECKED
-----------------------------------------------------------
Lemma (binomial).  b_k := binom(1/2, k) = (-1)^(k-1) * 2 * Cat(k-1) / 4^k  for k >= 1,
Cat(m) = binom(2m, m)/(m+1) the Catalan number (an integer).
  Machine-checked here: base case k = 1, and the ratio identity
  b_{k+1}/b_k = (1/2 - k)/(k + 1) = RHS_{k+1}/RHS_k as rational functions of k (sympy).
  That is an induction whose two steps are each verified; it is not a Lean proof.
  The lemma is also checked numerically-exactly for k <= N (PASS(N)).

Consequence, for F = 1 + u, u in z Z[[z]], f = sqrt(F) = sum_k b_k u^k:
  (L4)  always:            v_2(den a_n) <= 2n - 1   and no odd prime: c = 4 always suffices.
  (L2)  if 2 | u:          v_2(den a_n) <= n - 1                     : c = 2 suffices.
  (L1)  if 4 | u:          a_n in Z                                  : c = 1.
  because b_k 2^{jk} = +-2 Cat(k-1) 2^{(j-2)k}, j = 0, 1, 2, and the z^n coefficient of u^k
  vanishes for k > n.  (L1) is Stream 1's `sqrtSeq_integral_of_four_dvd` and the dyadic
  statement is its `sqrtSeq_dyadic` (read as source, no Lean build run; see CITATIONS).
  So NO_C_FOUND can never occur for a square-root partner of an integral series with
  constant term 1: the attribute worth reporting is WHICH of 1, 2, 4.  The real known-bads
  therefore have to come from elsewhere (controls file: exp, log(1+z), exp(z/2)).

For cooper_s10 the hypothesis of (L2) holds for ALL n, given the register's closed form
s10(n) = sum_k C(n,k)^4:   x^4 = x mod 2, so s10(n) = sum_k C(n,k) = 2^n = 0 mod 2 (n >= 1).
  Machine-checked here: x^4 = x mod 2 on residues; closed form == recurrence to N (PASS(N));
  sum_k C(n,k) = 2^n to N.  The identity "closed form = recurrence for all n" is the
  register's (OEIS A005260 / Stream 1), not re-proved here.
  The argument above yields e_2(n) <= n - 1 for all n >= 1 for the series sqrt(g.f. of sum_k C(n,k)^4).
  The REGISTERED order-2 entry cooper_s10_partner is defined by its own recurrence, so the
  all-n statement about THAT entry rests on TWO all-n identities, neither re-proved here:
    (H1) s10(n) = sum_k C(n,k)^4 satisfies the registered order-3 recurrence for all n;
    (H2) the registered order-2 partner recurrence generates the formal square root of the
         s10 generating function for all n.
  In this checker both are finite-order only (PASS(N): gates `closed_form_equals_recurrence`
  and `sqrt(cooper_s10)_equals_cooper_s10_partner`).  Stream 1 states both as theorems,
  `WZ.s10_satisfies` (H1) and `partner_eq_sqrt` / `partner_eq_sqrt_s10` (H2) -- read as
  source at the pinned commit, no Lean build run (CITATIONS).  Those theorems are about the
  Cooper template with `s10_params`; that the register's two recurrence strings ARE that
  template at those parameters is checked here symbolically (`template_transcription`, the
  parameters parsed from the Lean source, not typed).
  So: e_2(n) <= n - 1 and, with a_2 = 17/2, least c = 2 for the registered entry for all n,
  MODULO (H1) and (H2); unconditionally only PASS(N).
The closed form e_2(n) = v_2((2 floor(n/2))!) of the hand estimate is only tested: PASS(N).

Exit code 0 iff every gate in `checks` holds.  NO_C_FOUND or c > 1 for a series is a
REPORTED ATTRIBUTE, never a failure of the checker.
"""
import hashlib
import json
import pathlib
import subprocess
import sys
from fractions import Fraction
from math import comb

ROOT = pathlib.Path(__file__).resolve().parents[1]
REFS = ROOT / "refs" / "recurrences_v1.json"
CERT = ROOT / "data" / "certificates" / "PARTNER_GLOBAL_BOUNDEDNESS.json"
N_ORDER = 160
C_MAX = 64

STREAM1 = ROOT.parent / "SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal"
CITATIONS = [
    # (path, text with which a LINE OF THE FILE MUST START -- a declaration, never a mention in a
    #  comment -- , commit at which it is read).  The reported line is the line of the statement.
    ("Agora/Sequences/SqrtIntegrality.lean", "theorem sqrtSeq_integral_of_four_dvd", "5cabc83"),
    ("Agora/Sequences/FormalSqrt.lean", "theorem sqrtSeq_dyadic", "5cabc83"),
    ("Agora/Sequences/SqrtBridgeGeneric.lean", "theorem partner_eq_sqrt (", "5cabc83"),
    ("Agora/Sequences/SqrtBridgeGeneric.lean", "theorem partner_eq_sqrt_s10", "5cabc83"),
    ("Agora/Sequences/WZCertificates.lean", "theorem s10_satisfies", "5cabc83"),
    ("Agora/Sequences/CooperRecurrences.lean", "def s10_params", "5cabc83"),
    ("Agora/Sequences/CooperRecurrences.lean", "def s7_params", "5cabc83"),
    ("Agora/Sequences/PartnerIntegrality.lean", "theorem s18_partner_not_integral", "5cabc83"),
    ("Agora/Sequences/PartnerIntegrality.lean", "theorem s10_partner_not_integral", "5cabc83"),
]


class Refusal(Exception):
    def __init__(self, clause, msg=""):
        super().__init__(f"{clause}: {msg}")
        self.clause = clause


# ----------------------------------------------------------------------------- series
def regenerate(rec, seed, n_terms):
    s = [Fraction(str(t)) for t in seed]
    while len(s) < n_terms:
        k = len(s) - 1
        s.append(Fraction(eval(rec, {"__builtins__": {}}, {"k": Fraction(k), "s": s})))
    return s


def register_terms(entry, n_terms):
    stored = entry.get("initial_terms", entry.get("initial_terms_rational"))
    if stored is None:
        raise Refusal("no_stored_terms")
    stored = [Fraction(str(t)) for t in stored]
    s = regenerate(entry["recurrence_python"], stored[:2], n_terms)
    if s[:len(stored)] != stored:
        raise Refusal("recurrence_does_not_regenerate_stored_terms")
    return s


def formal_sqrt(a):
    """f with f^2 = a, f_0 = 1; requires a_0 = 1.  Exact."""
    if a[0] != 1:
        raise Refusal("constant_term_not_one")
    f = [Fraction(1)]
    for n in range(1, len(a)):
        conv = sum(f[i] * f[n - i] for i in range(1, n))
        f.append((a[n] - conv) / 2)
    return f


# ----------------------------------------------------------------------------- arithmetic
def vp(m, p):
    if m == 0:
        raise ValueError("v_p(0)")
    e = 0
    while m % p == 0:
        m //= p
        e += 1
    return e


def factor_small(m):
    out, p = {}, 2
    while p * p <= m:
        while m % p == 0:
            out[p] = out.get(p, 0) + 1
            m //= p
        p += 1
    if m > 1:
        out[m] = out.get(m, 0) + 1
    return out


def v2_factorial(m):
    return m - bin(m).count("1")          # Legendre; cross-checked against vp in selftest


def boundedness(a, c_max=C_MAX):
    """Least c <= c_max with c^n a_n integral for all n < len(a); two code paths."""
    N = len(a) - 1
    den_primes = {}
    for n, x in enumerate(a):
        for p, e in factor_small(x.denominator).items():
            den_primes.setdefault(p, {})[n] = e
    if any(x.denominator != 1 for x in a[:1]):
        return {"verdict": "NO_C_FOUND", "clause": "constant_term_not_integral", "order_checked": N}
    # path 1: brute force
    c_brute, first_fail = None, {}
    for c in range(1, c_max + 1):
        bad = next((n for n, x in enumerate(a) if (x * c ** n).denominator != 1), None)
        if bad is None:
            c_brute = c
            break
        first_fail[c] = bad
    # path 2: per-prime formula (unbounded in c)
    c_formula = 1
    for p, es in den_primes.items():
        m = max(-(-e // n) for n, e in es.items())
        c_formula *= p ** m
    res = {"order_checked": N, "c_formula_unbounded": c_formula,
           "denominator_primes": sorted(den_primes),
           "e_p": {str(p): [den_primes[p].get(n, 0) for n in range(N + 1)] for p in sorted(den_primes)}}
    if c_brute is not None:
        if c_brute != c_formula:
            raise Refusal("two_paths_disagree", f"{c_brute} vs {c_formula}")
        res.update(verdict="C_FOUND", c=c_brute, render=f"c = {c_brute}, PASS({N})")
    else:
        if c_formula <= c_max:
            raise Refusal("two_paths_disagree", f"brute none vs {c_formula}")
        big = [p for p in den_primes if p > c_max]
        res.update(verdict="NO_C_FOUND", c=None,
                   clause="prime_above_C_MAX_in_denominator" if big else "no_c_in_box",
                   primes_above_C_MAX=big[:10],
                   least_n_at_which_every_c_has_failed=max(first_fail.values()),
                   render=f"NO_C_FOUND (c <= {c_max}, order {N})")
    return res


# ----------------------------------------------------------------------------- proofs
def binomial_lemma(N):
    import sympy as sp
    k = sp.symbols("k", positive=True, integer=True)
    lhs_ratio = (sp.Rational(1, 2) - k) / (k + 1)
    cat = lambda m: sp.binomial(2 * m, m) / (m + 1)
    # Cat(k)/Cat(k-1) = 2(2k-1)/(k+1), itself checked as a gamma-function identity
    cat_ratio = sp.simplify(sp.gammasimp(sp.combsimp(cat(k) / cat(k - 1))) - 2 * (2 * k - 1) / (k + 1)) == 0
    rhs_ratio = -(2 * (2 * k - 1) / (k + 1)) / 4
    ratio_ok = sp.simplify(lhs_ratio - rhs_ratio) == 0
    base_ok = sp.binomial(sp.Rational(1, 2), 1) == sp.Rational(2 * 1, 4)
    finite_ok = True
    b = Fraction(1)
    for kk in range(1, N + 1):
        b = b * (Fraction(1, 2) - (kk - 1)) / kk
        rhs = Fraction((-1) ** (kk - 1) * 2 * (comb(2 * kk - 2, kk - 1) // kk), 4 ** kk)
        if comb(2 * kk - 2, kk - 1) % kk or b != rhs:
            finite_ok = False
    return {"catalan_ratio_identity_sympy": bool(cat_ratio), "ratio_identity_sympy": bool(ratio_ok),
            "base_case_k1": bool(base_ok), "finite_check_PASS_N": finite_ok, "N": N}


def s10_parity(a_s10, N):
    x4 = all((x ** 4 - x) % 2 == 0 for x in range(2))
    closed = all(sum(comb(n, k) ** 4 for k in range(n + 1)) == a_s10[n] for n in range(N + 1))
    rowsum = all(sum(comb(n, k) for k in range(n + 1)) == 2 ** n for n in range(N + 1))
    even = all(a_s10[n] % 2 == 0 for n in range(1, N + 1))
    return {"x4_equals_x_mod_2": x4, "closed_form_equals_recurrence_PASS_N": closed,
            "row_sum_is_2_pow_n_PASS_N": rowsum, "all_terms_even_PASS_N": even, "N": N}


def statement_line(source, name):
    """1-based line at which a DECLARATION starting with `name` stands, else None.  A mention of
    the name inside a comment or docstring does not count (the line must start with `name`)."""
    return next((i + 1 for i, l in enumerate(source.splitlines()) if l.startswith(name)), None)


def lean_source(path, commit):
    txt = subprocess.run(["git", "-C", str(STREAM1), "show", f"{commit}:{path}"],
                         capture_output=True, text=True, timeout=30)
    return txt.stdout if txt.returncode == 0 else ""


def verify_citations(citations=None, reader=lean_source):
    out = []
    for path, name, commit in (CITATIONS if citations is None else citations):
        try:
            line = statement_line(reader(path, commit), name)
        except Exception:
            line = None
        out.append({"repo": STREAM1.name, "path": path, "name": name.rstrip(" ("), "commit": commit,
                    "line": line, "status": "VERIFIED" if line else "PHANTOM",
                    "how": "read as source, no Lean build run"})
    return out


def template_transcription(reg, reader=lean_source):
    """The register's recurrence strings versus Stream 1's Cooper template (SatisfiesCooperRecurrence,
    partnerPair) at the parameters PARSED from CooperRecurrences.lean.  Symbolic, sympy."""
    import re
    import sympy as sp
    k, S1, S2 = sp.symbols("k S1 S2")
    src = reader("Agora/Sequences/CooperRecurrences.lean", "5cabc83")
    out = {}
    for fam in ("s7", "s10"):
        m = re.search(r"^def %s_params : CooperRecurrenceParams := \u27e8(-?\d+), (-?\d+), (-?\d+), (-?\d+)\u27e9" % fam,
                      src, re.M)
        if not m:
            out[fam] = {"params": None, "ok": False}
            continue
        a, b, c, d = (int(x) for x in m.groups())
        env = lambda: {"k": k, "s": [S2, S1]}
        e3 = eval(reg[f"cooper_{fam}"]["recurrence_python"], {"__builtins__": {}}, env())
        e2 = eval(reg[f"cooper_{fam}_partner"]["recurrence_python"], {"__builtins__": {}}, env())
        t3 = ((2 * k + 1) * (a * k ** 2 + a * k + b) * S1 - k * (c * k ** 2 + d) * S2) / (k + 1) ** 3
        t2 = (S1 * (2 * a * k ** 2 + a * k + sp.Rational(b, 2))
              - S2 * (c * (k - 1) ** 2 + c * (k - 1) + sp.Rational(c + d, 4))) / (k + 1) ** 2
        seeds3 = [Fraction(str(x)) for x in reg[f"cooper_{fam}"]["initial_terms"][:2]]
        pe = reg[f"cooper_{fam}_partner"]
        seeds2 = [Fraction(str(x)) for x in pe.get("initial_terms", pe.get("initial_terms_rational"))[:2]]
        r = {"params_abcd_parsed_from_lean": [a, b, c, d],
             "order3_recurrence_is_template": sp.simplify(e3 - t3) == 0,
             "order2_recurrence_is_template": sp.simplify(e2 - t2) == 0,
             "order3_seeds_are_1_b": seeds3 == [1, b],
             "order2_seeds_are_1_b_over_2": seeds2 == [1, Fraction(b, 2)]}
        r["ok"] = all(v is True for kk, v in r.items() if kk != "params_abcd_parsed_from_lean")
        out[fam] = r
    return out


# ----------------------------------------------------------------------------- run
def analyse(name, kind, a, advisory=False):
    r = boundedness(a)
    r.update(series=name, kind=kind, first_terms=[str(x) for x in a[:8]])
    if advisory:
        r["flags"] = ["ADVISORY: cooper_s10 lattice certificate is DRAFT; this row is series "
                      "arithmetic of the registered recurrence and does not depend on it, flagged "
                      "by house rule"]
    return r


def run(n_order=N_ORDER, refs_path=REFS):
    reg = json.loads(pathlib.Path(refs_path).read_text())["sequences"]
    rows, terms = [], {}
    for key, e in reg.items():
        terms[key] = register_terms(e, n_order + 1)
    for key, e in reg.items():
        adv = "s10" in key
        if e["type"] == "order-2":
            rows.append(analyse(key, "registered order-2 entry", terms[key], adv))
        elif e["type"] == "order-3":
            a = terms[key]
            if any(x.denominator != 1 for x in a):
                raise Refusal("order3_entry_not_integral", key)
            r = analyse(f"sqrt({key})", "derived square-root partner of an order-3 entry",
                        formal_sqrt(a), adv)
            m = min(vp(int(x), 2) for x in a[1:] if x != 0)
            r["min_v2_of_order3_terms_n_ge_1"] = m
            r["lemma_predicts_c_divides"] = {0: 4, 1: 2}.get(m, 1)
            r["lemma_consistent"] = (r["verdict"] == "C_FOUND" and r["lemma_predicts_c_divides"] % r["c"] == 0)
            rows.append(r)
    by = {r["series"]: r for r in rows}

    checks = {}
    for k3, p in (("cooper_s7", "cooper_s7_partner"), ("cooper_s10", "cooper_s10_partner")):
        checks[f"sqrt({k3})_equals_{p}_PASS_{n_order}"] = formal_sqrt(terms[k3]) == terms[p]
    checks["lemma_consistent_on_every_sqrt_row"] = all(r.get("lemma_consistent", True) for r in rows)
    lem = binomial_lemma(n_order)
    checks["binomial_lemma_pieces"] = all(v for k, v in lem.items() if k != "N")
    par = s10_parity([int(x) for x in terms["cooper_s10"]], n_order)
    checks["s10_parity_pieces"] = all(v for k, v in par.items() if k != "N")
    checks["v2_factorial_legendre_selftest"] = all(
        v2_factorial(m) == sum(vp(j, 2) for j in range(1, m + 1)) for m in range(0, 400))
    cites = verify_citations()
    checks["external_citations_not_phantom"] = all(c["status"] == "VERIFIED" for c in cites)
    trans = template_transcription(reg)
    checks["register_recurrences_are_the_stream1_template"] = all(v["ok"] for v in trans.values())

    # ---- hand estimate, scored
    s10 = by["cooper_s10_partner"]
    e2 = s10["e_p"].get("2", [0] * (n_order + 1))
    closed = [v2_factorial(2 * (n // 2)) for n in range(n_order + 1)]
    mism = [n for n in range(n_order + 1) if e2[n] != closed[n]]
    hand = {
        "c = 2 works for cooper_s10_partner": s10.get("c") == 2,
        "denominators are pure powers of 2": s10["denominator_primes"] in ([2], []),
        f"e(n) = v_2((2 floor(n/2))!) for n <= {n_order}": not mism,
        "cooper_s7_partner: c = 1": by["cooper_s7_partner"].get("c") == 1,
    }
    bound_ok = all(e2[n] <= n - 1 for n in range(1, n_order + 1))
    cert = {
        "certificate": "PARTNER_GLOBAL_BOUNDEDNESS", "checker": "checkers/check_partner_global_boundedness.py",
        "date": "2026-09-21", "tier": "B", "checker_version": checker_version(),
        "status": "RECORD OF AN ATTRIBUTE, NOT A GATE. Whether criterion C3 requires integrality of the "
                  "order-2 partner is an open T0 question; it is not answered here. Nothing is scored.",
        "claim": "Integrality of a partner series is a property of the series IN A COORDINATE. For each "
                 f"series: the least c <= {C_MAX} with f(c z) integral to order N, and the p-adic denominator exponents.",
        "order_checked": n_order, "C_MAX": C_MAX,
        "inputs": {"sha256": {"refs/recurrences_v1.json": hashlib.sha256(pathlib.Path(refs_path).read_bytes()).hexdigest()}},
        "rows": rows,
        "cooper_s10_partner_detail": {
            "flags": s10.get("flags", []),
            "least_c": s10.get("c"), "render": s10["render"],
            "e2_first_40": e2[:40],
            "closed_form_tested": "e(n) = v_2((2 floor(n/2))!)",
            "closed_form_mismatches": mism, "closed_form_verdict": f"PASS({n_order})" if not mism else "REFUTED",
            "bound_e_le_n_minus_1_observed": f"PASS({n_order})" if bound_ok else "FAILS",
            "bound_status": "e_2(n) <= n - 1 for all n >= 1 is proved (docstring (L2); algebraic steps "
                            "sympy-checked in `binomial_lemma`, `s10_parity`; not a Lean proof) for the series "
                            "sqrt(g.f. of sum_k C(n,k)^4). For the REGISTERED entry cooper_s10_partner it holds for "
                            "all n MODULO TWO identities, see `all_n_hypotheses`; unconditionally it is only "
                            f"PASS({n_order}).",
            "all_n_hypotheses": [
                {"id": "H1", "statement": "s10(n) = sum_k C(n,k)^4 satisfies the registered order-3 recurrence for all n",
                 "status_in_this_checker": f"PASS({n_order}) (gate s10_parity_pieces / closed_form_equals_recurrence)",
                 "stream1_statement": next(c for c in cites if c["name"] == "theorem s10_satisfies")},
                {"id": "H2", "statement": "the registered order-2 partner recurrence generates the formal square root "
                                          "of the cooper_s10 generating function for all n",
                 "status_in_this_checker": f"PASS({n_order}) (gate sqrt(cooper_s10)_equals_cooper_s10_partner)",
                 "stream1_statement": [c for c in cites if c["name"].startswith("theorem partner_eq_sqrt")]},
            ],
            "all_n_hypotheses_note": "Both Stream 1 statements were read as source at the pinned commit; no Lean "
                                     "build was run here, so neither is re-verified by this checker. They concern the "
                                     "Cooper template at s10_params; that the register's recurrence strings equal "
                                     "that template is the symbolic gate `register_recurrences_are_the_stream1_template`.",
            "least_c_is_2_for_all_n": "modulo H1 and H2: follows from the bound (c = 2 suffices) and a_2 = "
                                      + str(terms["cooper_s10_partner"][2]) + f" (c = 1 fails); otherwise PASS({n_order})",
            "closed_form_status": f"PASS({n_order}) only; no proof attempted beyond the bound",
        },
        "general_lemma": {"statement": "sqrt of an integral series with constant term 1 becomes integral under "
                                       "z -> 4z (always), z -> 2z (if all higher terms are even), z -> z (if all "
                                       "are divisible by 4); no odd prime ever occurs in a denominator.",
                          "consequence": "NO_C_FOUND cannot occur for a square-root partner; the real known-bad "
                                         "controls are series that are not such square roots.",
                          "machine_checked_pieces": lem, "s10_parity": par},
        "hand_estimate": {"provenance": "orchestrator hand estimate, issued UNVERIFIED (n < 60 only); scored here",
                          "clauses": {k: ("confirmed" if v else "REFUTED") for k, v in hand.items()}},
        "external_citations_verified_at_run_time": cites,
        "register_vs_stream1_template": trans,
        "checks": checks,
        "controls": "checkers/test_partner_global_boundedness_controls.py",
        "not_claimed": [
            "that criterion C3 requires, or does not require, an integral partner: open T0 question",
            "that a rescaled coordinate c z is preferred or canonical in any sense",
            "global boundedness of any series beyond order N, except where a proof status is stated",
            "the closed form e(n) = v_2((2 floor(n/2))!) beyond order N",
            "that s10(n) = sum_k C(n,k)^4 satisfies the registered recurrence for all n (H1; Stream 1 statement, read as source)",
            "that the registered cooper_s10_partner recurrence equals the formal square root for all n (H2; Stream 1 "
            "statement, read as source); here it is PASS(N)",
            "anything about T(cooper_s10): its lattice certificate is DRAFT; s10 rows are flagged advisory",
            "any physical reading whatsoever (VISION sec 1.3; Tier C blocked)",
        ],
        "provenance": "Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: "
                      "checkers/test_partner_global_boundedness_controls.py | Reviewed-by: N",
    }
    return cert


def checker_version():
    """git describe of the repo HEAD the checker ran on (the checker file itself may be uncommitted:
    `checker_sha256` pins its bytes)."""
    try:
        d = subprocess.run(["git", "-C", str(ROOT), "describe", "--always", "--tags"],
                           capture_output=True, text=True, timeout=30).stdout.strip() or "unknown"
    except Exception:
        d = "unknown"
    return {"git_describe_HEAD": d, "checker_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}


def checks_ok(checks):
    return all(v is True for v in checks.values())


def main():
    cert = run()
    CERT.write_text(json.dumps(cert, indent=1) + "\n")
    for r in cert["rows"]:
        print(f"{r['series']:40s} {r['render']:28s} den primes {r['denominator_primes']}"
              + ("  [ADVISORY]" if r.get("flags") else ""))
    print("hand estimate:", cert["hand_estimate"]["clauses"])
    print("checks:", cert["checks"])
    return 0 if checks_ok(cert["checks"]) else 1


if __name__ == "__main__":
    sys.exit(main())
