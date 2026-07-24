#!/usr/bin/env python3
"""
export_pipeline_bound_artifact.py — Stream-2 → Stream-1 cross-stream data interface (D-3).

Emits a *deterministic, hash-stamped, exact-rational* static artifact for the freeze-out
pipeline upper bound S_{1,2} <= 1.177, so Stream 1 can `import` it natively into the Lean
proof kernel.

IMPORTANT — epistemic typing (VISION.md §2, DUAL_SCALE_THREE_STREAM_PLAN.md S1-1):

  The number 1.177 is an *external DarkMatter@Home v1 headline output*. It is NOT reproducible
  from committed artifacts (A7 provenance defect, plan line 69). The committed script
  scripts/ws11_cosmic_seesaw_verification.py does NOT compute it — 1.177 appears there only as a
  code comment while the script runs a Welch t-test on np.random.normal synthetic data (seed=42).

  Therefore this artifact declares `lean_import_kind = "hypothesis"`. Stream 1 must import it as
  `hypothesis_pipeline_upper_bound` (a labeled assumption in the hypothesis set), NEVER as a
  verified `axiom`. A SHA-256 hash makes the file *deterministic*; it does not make the number
  *reproducible*. Promotion to a verified bound is gated on DM-3 (Stream-3 quorum re-run).

This script is self-contained: identical inputs -> byte-identical artifact + hash.
"""

import hashlib
import json
from fractions import Fraction
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_JSON = REPO_ROOT / "data" / "interfaces" / "pipeline_bound_v1.json"
OUT_HASH = REPO_ROOT / "data" / "interfaces" / "pipeline_bound_v1.sha256"

ARTIFACT_SCHEMA_VERSION = "1.0.0"

# --- The frozen quantity ---------------------------------------------------
# Exact rational representation of the v1 headline decimal 1.177.
VALUE = Fraction(1177, 1000)


def build_artifact() -> dict:
    """Assemble the artifact body (without the self-hash field)."""
    return {
        "schema_version": ARTIFACT_SCHEMA_VERSION,
        "artifact_id": "pipeline_upper_bound_v1",
        "quantity": {
            "symbol": "S_{1,2}",
            "description": "Local-universe (z~0) freeze-out upper bound on the seesaw ratio S_{1,2}.",
            "relation": "S_{1,2} <= value",
        },
        "value": {
            "rational": f"{VALUE.numerator}/{VALUE.denominator}",
            "numerator": VALUE.numerator,
            "denominator": VALUE.denominator,
            "decimal_display": "1.177",
        },
        # --- Epistemic typing (the load-bearing part) ---
        "epistemic": {
            "tier": "C_hypothesis",
            "lean_import_kind": "hypothesis",
            "lean_symbol": "hypothesis_pipeline_upper_bound",
            "must_not_be_imported_as": "axiom",
            "rationale": (
                "Number is an external DarkMatter@Home v1 headline output, not reproducible "
                "from committed artifacts (A7 provenance defect)."
            ),
        },
        "provenance": {
            "origin": "External DarkMatter@Home volunteer run (v1 headline number).",
            "reproducible_from_committed_artifacts": False,
            "source_defect_ref": "DUAL_SCALE_THREE_STREAM_PLAN.md:69 (A7 provenance defect)",
            "governing_rule": (
                "S1-1: no axiom may encode a non-reproducible number without a provenance tag "
                "in its docstring; demote to hypothesis_ prefix or re-source via DM-3."
            ),
            "ws11_note": (
                "scripts/ws11_cosmic_seesaw_verification.py does NOT compute 1.177; it appears "
                "only as a code comment while the script runs a Welch t-test on np.random.normal "
                "synthetic data (seed=42). This artifact does not inherit any statistical claim "
                "from that script."
            ),
            "promotion_blocker": (
                "DM-3 — re-run the v1 headline number under a Stream-3 quorum and archive the "
                "reproducible artifact before promoting this hypothesis to a verified bound."
            ),
        },
        "generator": {
            "script": "scripts/export_pipeline_bound_artifact.py",
            "determinism": "Byte-identical output for identical inputs; no network, no RNG, no LLM.",
        },
        "provenance_footer": (
            "Generated-by: scripts/export_pipeline_bound_artifact.py (Tier C hypothesis) | "
            "Verified-by: exact rational, deterministic serialization | Reviewed-by: pending T0"
        ),
    }


def canonical_bytes(obj: dict) -> bytes:
    """Deterministic canonical JSON: sorted keys, no whitespace ambiguity, trailing newline."""
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def main() -> None:
    body = build_artifact()
    digest = hashlib.sha256(canonical_bytes(body)).hexdigest()

    # The written JSON embeds the digest for convenience but the digest is computed over the
    # body WITHOUT the digest field, so it is self-consistent and re-verifiable.
    out = dict(body)
    out["sha256"] = {
        "algorithm": "sha256",
        "over": "canonical JSON of this object with the 'sha256' key removed (sorted keys, compact separators, trailing newline)",
        "digest": digest,
    }

    OUT_JSON.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    OUT_HASH.write_text(f"{digest}  pipeline_bound_v1.json\n")

    print(f"value            : {VALUE.numerator}/{VALUE.denominator}  (= {float(VALUE)})")
    print(f"lean_import_kind : {body['epistemic']['lean_import_kind']}  (symbol: {body['epistemic']['lean_symbol']})")
    print(f"sha256           : {digest}")
    print(f"wrote            : {OUT_JSON.relative_to(REPO_ROOT)}")
    print(f"wrote            : {OUT_HASH.relative_to(REPO_ROOT)}")


def verify() -> bool:
    """Re-derive the digest from the committed file; return True if self-consistent."""
    obj = json.loads(OUT_JSON.read_text())
    stated = obj.pop("sha256")["digest"]
    return hashlib.sha256(canonical_bytes(obj)).hexdigest() == stated


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        ok = verify()
        print("VERIFY:", "OK — digest matches" if ok else "FAIL — digest mismatch")
        sys.exit(0 if ok else 1)
    main()
