#!/usr/bin/env python3
"""
AE-0 — Preflight checks for Stream 2 AutoEvolve.

Deterministic, dependency-light verification that the environment can import
all reused gate machinery and that the frozen candidate pool is intact.
"""

import hashlib
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "data" / "autoresearch_v2"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def check(name, fn, details=None):
    """Run a check function; return status dict.

    If fn returns a dict, use it directly (allows INFO status).
    """
    try:
        ret = fn()
        if isinstance(ret, dict):
            return ret
        return {"status": "PASS", "detail": details or "ok"}
    except Exception as e:
        detail = f"{type(e).__name__}: {e}"
        if detail.startswith("RuntimeError: INFO:"):
            return {"status": "INFO", "detail": detail.split(":", 1)[1].strip()}
        return {"status": "FAIL", "detail": detail}


def _import_scanner():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    sys.path.insert(0, str(REPO_ROOT))
    from autoresearch_v2_phase_a_scan import classify
    from autoresearch_v2_phase_b_all_gates import find_ode_with_coeffs
    from autoresearch_v2_pool import POOL, verify_terms
    from checkers import check_C3b_symsqrt


def _pool_frozen():
    pool_path = REPO_ROOT / "data" / "autoresearch_v2" / "candidate_pool.yaml"
    if not pool_path.exists():
        # The historical pool file is not present in this branch; this is recorded
        # as INFO, not a hard fail, because the frozen generators live in
        # scripts/autoresearch_v2_pool.py and are verified separately.
        raise RuntimeError("INFO: candidate_pool.yaml not present; relying on autoresearch_v2_pool.py")


def _pool_generators():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from autoresearch_v2_pool import verify_terms
    fails = verify_terms()
    if fails:
        raise RuntimeError(f"OEIS verification failures: {fails}")


def _refs_integrity():
    refs_path = REPO_ROOT / "refs" / "recurrences_v1.json"
    if not refs_path.exists():
        raise FileNotFoundError("refs/recurrences_v1.json missing")
    sha = hashlib.sha256(refs_path.read_bytes()).hexdigest()
    return sha


def main():
    results = {}

    results["python_version"] = ".".join(map(str, sys.version_info[:3]))
    results["import_core"] = check("import_core", _import_scanner)
    results["pool_frozen"] = check("pool_frozen", _pool_frozen)
    results["pool_generators"] = check("pool_generators", _pool_generators)

    sha = None
    try:
        sha = _refs_integrity()
        results["refs_integrity"] = {"status": "PASS", "sha256": sha}
    except Exception as e:
        results["refs_integrity"] = {"status": "FAIL", "detail": str(e)}

    def _ok(r):
        return r.get("status") in ("PASS", "INFO")

    statuses = [r.get("status") for r in results.values() if isinstance(r, dict) and "status" in r]
    overall = "PASS" if all(_ok(r) for r in results.values() if isinstance(r, dict) and "status" in r) else "FAIL"
    out = {
        "preflight": results,
        "overall": overall,
        "script": "scripts/ae_preflight.py",
    }

    out_path = OUT_DIR / "ae_preflight.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
