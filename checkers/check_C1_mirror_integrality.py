#!/usr/bin/env python3
"""
check_C1_mirror_integrality.py -- mirror-map integrality for every order-3 entry of
refs/recurrences_v1.json (criterion C1 of K3_CRITERIA.md; gate K3 of
briefs/STREAM2_K3xT2_SELECTION_CRITERIA_PROPOSAL_2026_09_16.md).

NOT the retracted C1_*_partner.json Kodaira certificates. Output files are named
C1_mirror_integrality_<key>.json to keep the two apart.

METHOD (exact Fraction arithmetic, no floats)
  1. Frobenius at z = 0. The register convention is C(k) a_{k+1} = A(k) a_k + B(k) a_{k-1},
     stored as the string `recurrence_python` in k and s. Every order-3 entry has
     C(k) = (k+1)^3, i.e. indicial polynomial theta^3 (maximally unipotent at 0).
     Evaluating that same string with k replaced by the dual number k + eps gives
     a_n(eps); f0 = sum a_n(0) z^n, g = sum a_n'(0) z^n.
     Checked directly: f0 must reproduce the stored initial_terms, or the checker
     refuses. The deformation (the g part) is checked indirectly: s7's z(q) must equal
     the pinned A279618 b-file (control 1), which fails if the deformation is wrong.
  2. q(z) = z * exp(g / f0);  z(q) = series reversion.
  3. Verdict: PASS(N) if every coefficient of q(z) and z(q) up to z^N / q^N is an
     integer; otherwise FAIL with the first non-integral index. The normalization is
     the register's own (no rescaling of z); integrality in another normalization is
     not tested.
  4. OBSERVATION ONLY (unexplained, not a criterion): the largest k <= 24 such that
     (q/z)^(1/k) = exp(g/(k f0)) has integral coefficients to order N. It differs
     between families. No interpretation is claimed.

CONTROLS (run by test_C1_mirror_integrality_controls.py; they must be able to fail)
  1. s7 z(q) equals refs/oeis_A279618_bfile.txt on every b-file term  -> must MATCH.
  2. Same comparison against a copy of the b-file with one term changed -> must MISMATCH.
  3. Wrong Frobenius derivative (s7's g with two coefficients swapped) -> must FAIL
     integrality.
  4. Corrupted recurrence (one coefficient changed) -> f0 must fail to reproduce the
     stored terms, and the checker must refuse to emit a verdict.

Finite-order integrality is evidence, not proof: always report PASS(N), never PASS.

Usage:
  python3 checkers/check_C1_mirror_integrality.py            # all order-3 entries, N=60
  python3 checkers/check_C1_mirror_integrality.py --order 80 --only cooper_s7
  python3 checkers/check_C1_mirror_integrality.py --emit     # also write certificates

Generated-by: Claude (Opus 5), Stream 2 | Verified-by: test_C1_mirror_integrality_controls.py
| Reviewed-by: N
"""
import argparse
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REFS = REPO / "refs" / "recurrences_v1.json"
BFILE_A279618 = REPO / "refs" / "oeis_A279618_bfile.txt"
CERTS = REPO / "data" / "certificates"
CHECKER_VERSION = "1.0.0"


class Refused(Exception):
    """Input failed a precondition; no verdict may be emitted."""


class D:
    """Dual number a + b*eps, eps^2 = 0."""
    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a, self.b = F(a), F(b)

    @staticmethod
    def _c(o):
        return o if isinstance(o, D) else D(o)

    def __add__(s, o):
        o = D._c(o); return D(s.a + o.a, s.b + o.b)
    __radd__ = __add__

    def __sub__(s, o):
        o = D._c(o); return D(s.a - o.a, s.b - o.b)

    def __rsub__(s, o):
        return D._c(o) - s

    def __neg__(s):
        return D(-s.a, -s.b)

    def __mul__(s, o):
        o = D._c(o); return D(s.a * o.a, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__

    def __truediv__(s, o):
        o = D._c(o)
        if o.a == 0:
            raise ZeroDivisionError("dual division by zero real part")
        return D(s.a / o.a, (s.b * o.a - s.a * o.b) / (o.a * o.a))

    def __rtruediv__(s, o):
        return D._c(o) / s

    def __pow__(s, e):
        assert isinstance(e, int) and e >= 0
        r = D(1)
        for _ in range(e):
            r = r * s
        return r


def frobenius(recurrence, n_terms):
    """a_n(eps) for n < n_terms from the register recurrence string, with a_0 = 1 and
    a_{-1} = 0 imposed by the Frobenius ansatz (not read from the stored seeds)."""
    s = [D(0), D(1)]  # a_{-1}, a_0 ; the string reads s[-1] (= a_k) and s[-2] (= a_{k-1})
    while len(s) - 1 < n_terms:
        k = len(s) - 2  # index of s[-1] in the a_n numbering
        k_eps = D(k, 1)
        val = eval(recurrence, {"__builtins__": {}}, {"k": k_eps, "s": s})
        s.append(D._c(val))
    a = s[1:]
    return [x.a for x in a], [x.b for x in a]


def ps_mul(A, B, n):
    out = [F(0)] * (n + 1)
    for i in range(min(len(A), n + 1)):
        ai = A[i]
        if ai:
            for j in range(min(len(B), n + 1 - i)):
                if B[j]:
                    out[i + j] += ai * B[j]
    return out


def ps_inv(A, n):
    out = [F(0)] * (n + 1)
    out[0] = 1 / A[0]
    for k in range(1, n + 1):
        out[k] = -sum(A[i] * out[k - i] for i in range(1, min(k, len(A) - 1) + 1)) / A[0]
    return out


def ps_exp(A, n):
    assert A[0] == 0
    E = [F(0)] * (n + 1)
    E[0] = F(1)
    for k in range(1, n + 1):
        E[k] = sum(i * A[i] * E[k - i] for i in range(1, k + 1)) / k
    return E


def reversion(Q, n):
    """Q = [0, 1, q2, ...] (q as series in z) -> Z (z as series in q), by exact
    order-by-order coefficient matching."""
    Z = [F(0)] * (n + 1)
    Z[1] = F(1)
    for k in range(2, n + 1):
        comp = [F(0)] * (n + 1)
        P = [F(0)] * (n + 1); P[0] = F(1)
        for j in range(1, k + 1):
            P = ps_mul(P, Z, k)
            if Q[j]:
                comp[k] += Q[j] * P[k]
        Z[k] = -comp[k]
    return Z


def q_of_z(f0, g, order, g_scale=F(1)):
    ratio = ps_mul([x * g_scale for x in g], ps_inv(f0, order), order)
    E = ps_exp(ratio, order)
    return [F(0)] + E[:order]       # q = z * E, coefficients of z^0..z^order


def mirror_map(recurrence, order, g_scale=F(1)):
    f0, g = frobenius(recurrence, order + 1)
    Q = q_of_z(f0, g, order, g_scale)
    Z = reversion(Q, order)
    return f0, Q, Z


def first_nonintegral(series, start=1):
    for i in range(start, len(series)):
        if series[i].denominator != 1:
            return i
    return None


def read_bfile(path):
    out = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            idx, val = line.split()[:2]
            out.append((int(idx), int(val)))
    return out


def compare_to_bfile(Z, bfile_rows):
    """b-file index n <-> coefficient of q^n in z(q). Returns (n_compared, first_mismatch)."""
    n_cmp = 0
    for idx, val in bfile_rows:
        if idx >= len(Z):
            break
        n_cmp += 1
        if Z[idx] != val:
            return n_cmp, idx
    return n_cmp, None


def order3_entries(seqs):
    return [k for k, v in seqs.items() if v.get("type") == "order-3" and "recurrence_python" in v]


def check_entry(key, entry, order):
    stored = entry.get("initial_terms")
    if isinstance(stored, str):
        stored = json.loads(stored)
    f0, Q, Z = mirror_map(entry["recurrence_python"], order)
    n_stored = min(len(stored), len(f0))
    if [F(x) for x in stored[:n_stored]] != f0[:n_stored]:
        raise Refused(f"{key}: Frobenius f0 does not reproduce stored initial_terms "
                      f"(first {n_stored}); recurrence or convention mismatch")
    f0_raw, g_raw = frobenius(entry["recurrence_python"], order + 1)
    root_k = max(k for k in range(1, 25)
                 if first_nonintegral(q_of_z(f0_raw, g_raw, order, g_scale=F(1, k))) is None)
    bad_q = first_nonintegral(Q)
    bad_z = first_nonintegral(Z)
    verdict = f"PASS({order})" if bad_q is None and bad_z is None else "FAIL"
    return {
        "key": key, "order_checked": order, "verdict": verdict,
        "first_nonintegral_q_of_z": bad_q, "first_nonintegral_z_of_q": bad_z,
        "f0_reproduces_stored_terms": n_stored,
        "observation_largest_k_le_24_integral_kth_root_of_q_over_z": root_k,
        "z_of_q_first_terms": [str(x) for x in Z[1:13]],
        "q_of_z_first_terms": [str(x) for x in Q[1:13]],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--order", type=int, default=60)
    ap.add_argument("--only", action="append")
    ap.add_argument("--emit", action="store_true")
    args = ap.parse_args()

    raw = REFS.read_bytes()
    refs_sha = hashlib.sha256(raw).hexdigest()
    seqs = json.loads(raw)["sequences"]
    keys = args.only or order3_entries(seqs)
    worst = 0
    for key in keys:
        try:
            r = check_entry(key, seqs[key], args.order)
        except Refused as e:
            print(f"REFUSED  {e}", file=sys.stderr)
            worst = max(worst, 2)
            continue
        print(f"{key:28s} {r['verdict']:10s} q(z) first non-integral: {r['first_nonintegral_q_of_z']}, "
              f"z(q): {r['first_nonintegral_z_of_q']}  | largest k<=24 with integral (q/z)^(1/k): "
              f"{r['observation_largest_k_le_24_integral_kth_root_of_q_over_z']}")
        if r["verdict"] == "FAIL":
            worst = max(worst, 1)
        if args.emit:
            cert = {
                "certificate": f"C1_mirror_integrality_{key}",
                "criterion": "C1 mirror-map integrality (K3_CRITERIA.md C1; proposal gate K3)",
                "candidate": key,
                "verdict": r["verdict"],
                "order_checked": r["order_checked"],
                "evidence": {k: r[k] for k in ("first_nonintegral_q_of_z", "first_nonintegral_z_of_q",
                                               "f0_reproduces_stored_terms", "z_of_q_first_terms",
                                               "observation_largest_k_le_24_integral_kth_root_of_q_over_z",
                                               "q_of_z_first_terms")},
                "normalization": "register's own z (no rescaling); q = z*exp(g/f0), g = d/d(eps) of the Frobenius coefficients",
                "tier": "B",
                "tier_reason": "finite-order integrality is evidence, not proof",
                "not_claimed": [
                    "integrality beyond order_checked",
                    "integrality under any other normalization of z",
                    "that N = order_checked is the frozen C1 threshold (N1 is TBD-AT-FREEZE)",
                    "anything about Kodaira fibres (E-007) or physics (VISION sec 1.3)",
                    "any meaning for the observation_largest_k field (computed, unexplained)",
                ],
                "inputs": {"refs": {"recurrences_v1.json": refs_sha}},
                "checker": "check_C1_mirror_integrality.py",
                "checker_version": CHECKER_VERSION,
                "controls": "checkers/test_C1_mirror_integrality_controls.py",
                "provenance": "Generated-by: Claude (Opus 5), Stream 2 | Verified-by: test_C1_mirror_integrality_controls.py | Reviewed-by: N",
            }
            out = CERTS / f"C1_mirror_integrality_{key}.json"
            out.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    return worst


if __name__ == "__main__":
    sys.exit(main())
