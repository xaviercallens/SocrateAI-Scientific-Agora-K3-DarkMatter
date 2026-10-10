#!/usr/bin/env python3
"""Controls for check_K3xT2_reading_S_level_sweep.py (standing rule 1).

  P1  levels 1..5: every computed T(E x E') is isometric to U + <2n> and to no other U + <2m>
  N1  a shifted target (U + <2(n+1)> offered as the target for level n) is NOT accepted: the diagonal check fails
  N2  a target of the wrong signature (negated form) is NOT accepted at any level
  N3  the committed certificate agrees with a fresh sweep on its first 4 levels (same det, signature, verdict)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_K3xT2_reading_S as base  # noqa: E402
import check_K3xT2_reading_S_level_sweep as sw  # noqa: E402

fails = []


def check(name, cond, detail=""):
    print(f"  {'ok  ' if cond else 'FAIL'} {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        fails.append(name)


computed, matrix, diag_ok, off_ok = sw.sweep(5)
check("P1 diagonal isometric at levels 1..5", diag_ok)
check("P1b no off-diagonal isometry among the 20 pairs", off_ok)

orig = sw.target
sw.target = lambda n: orig(n + 1)
try:
    _, m2, d2, _ = sw.sweep(3)
finally:
    sw.target = orig
check("N1 a shifted target is not accepted on the diagonal (no level matches its offered target)",
      (not d2) and not any(m2[(n, n)] for n in range(1, 4)))

neg = lambda n: [[-v for v in row] for row in orig(n)]
T3 = computed[3]["T_basis_in_wedge2"]
check("N2 the negated (wrong-signature) target is not accepted", base.find_isometry(T3, neg(3)) is None)

cert = json.loads(sw.OUT.read_text())
ok = True
for n in range(1, 5):
    c = cert["result"]["per_level"][str(n)]
    f = computed[n]
    ok &= (c["T_det"] == f["T_det"] and c["T_signature"] == f["T_signature"] and c["verdict"] == f["verdict"])
check("N3 committed certificate matches a fresh sweep on levels 1..4", ok)
check("N3b committed certificate: all diagonal, no off-diagonal", cert["result"]["diagonal_all"] and cert["result"]["off_diagonal_none"])

print()
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all level-sweep controls behaved as required")
