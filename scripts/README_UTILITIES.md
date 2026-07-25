# Stream Utility Scripts — Quick Reference

This directory contains utility scripts for stream coordination, session restart, and memory alignment.

---

## Quick Start

### At Session Start: Restore Context
```bash
python3 scripts/restart_session.py
```

Displays:
- ✅ All three streams' current status
- 🔄 Recent git commits (last 20)
- 📋 Memory state (latest entries)
- ⏱️ Critical timeline to Gate E
- 📌 Next actions by stream
- ⚠️ Blocking issues

**Options:**
```bash
python3 scripts/restart_session.py --streams      # Streams status only
python3 scripts/restart_session.py --memory       # Memory state only
python3 scripts/restart_session.py --decisions    # Next actions only
python3 scripts/restart_session.py --timeline     # Timeline only
```

---

## Available Scripts

### 1. `restart_session.py` — Session Restart & Memory Alignment
**Purpose:** Quick context recovery at session start

**Usage:**
```bash
python3 scripts/restart_session.py              # Full report
python3 scripts/restart_session.py --streams    # Streams status only
```

**Shows:**
- Three-stream status (current, status, next, blocker)
- Memory system state (latest entries)
- Git history (recent 20 commits)
- Critical timeline (milestones to Gate E)
- Next actions by stream (prioritized)
- Blocking issues (if any)

**When to run:** Start of every new session

---

### 2. `compute_C1_monodromy.py` — Picard-Fuchs Exponent → Kodaira Mapping
**Purpose:** Convert PF exponents to Kodaira fibre types

**Usage:**
```bash
python3 scripts/compute_C1_monodromy.py \
  --c1-loci data/certificates/C1loci_cooper_s7_partner.json \
  --partner cooper_s7_partner \
  --out data/certificates/C1_monodromy_cooper_s7_partner_v2.json
```

**Input:** C1-loci JSON (from `checkers/check_C1_singular_loci.py`)  
**Output:** Monodromy + Kodaira type JSON (v2 certificate intermediate)

**Rigor:** Tier B (exponent-based, heuristic but grounded in algebra)

---

### 3. `generate_C1C2_v2_certificates.py` — Unified v2 Certificate Generation
**Purpose:** Merge C1-loci + monodromy → unified C1 + C2 v2 certificates

**Usage:**
```bash
python3 scripts/generate_C1C2_v2_certificates.py
```

**Inputs:**
- `data/certificates/C1loci_*.json` (corrected loci)
- `data/certificates/C1_monodromy_*_v2.json` (monodromy data)

**Outputs:**
- `data/certificates/C1_*_partner_v2.json` (exact Kodaira types)
- `data/certificates/C2_*_partner_v2.json` (lattice ranks)

**Status:** F6 rectification complete (commit 1dd17cd)

---

### 4. `k3_monodromy_verification.py` — Monodromy Consistency Check
**Purpose:** Verify monodromy matrices satisfy symplectic constraints

**Usage:**
```bash
python3 scripts/k3_monodromy_verification.py --cert data/certificates/C1_cooper_s7_partner_v2.json
```

**Checks:**
- ✅ Fuchs relation (sum of exponents = #singularities - 2)
- ✅ Shioda-Tate formula (ρ = 2 + Σ(m_i - 1) + rank(MW))
- ✅ K3 constraint (T = 22 - ρ)

---

## Stream Coordination

### Before D-3 Batch Starts
```bash
python3 scripts/restart_session.py --streams
```
Verify all three streams ready (Stream 1 handoff, Stream 2 contingency, Stream 3 launch).

### During D-3 Execution
```bash
python3 scripts/restart_session.py --timeline
```
Track progress to Gate E decision (batch completion → aggregation → decision).

### After D-3 Batch
```bash
python3 scripts/restart_session.py --decisions
```
Review next actions (PASS/CONDITIONAL/FAIL paths).

---

## Memory System Integration

The restart script reads from:
- **Memory files:** `~/.claude/projects/.../memory/*.md`
- **Git history:** `git log --oneline`
- **Status:** `git status --porcelain`

**Update memory after major milestones:**
```bash
# After Gate E decision
# After v0.4.0 release
# After Stream 1 Lean completion
```

Use the auto-memory system to record:
- 🔷 Stream status updates
- 📋 Decision logs (PASS/CONDITIONAL/FAIL outcomes)
- 🎯 Next actions (prioritized by stream)
- ⚠️ Blocking issues (if any)

---

## Quick Reference: Critical Dates

| Milestone | Date | Status |
|-----------|------|--------|
| D-3 batch START | 2026-07-25 18:00 UTC | 🔄 Running |
| D-3 batch COMPLETE | 2026-07-26 06:00 UTC | Pending |
| Aggregation COMPLETE | 2026-07-26 08:00 UTC | Pending |
| Gate E DECISION | 2026-07-27 EOD UTC | Pending |
| v0.4.0 RELEASE | 2026-07-27+ | Conditional (if Gate E PASS) |

---

## Troubleshooting

**Script not running?**
```bash
chmod +x scripts/restart_session.py
python3 scripts/restart_session.py --help
```

**Memory files not found?**
```bash
# Check memory system
ls -la ~/.claude/projects/.../ memory/MEMORY.md
```

**Git status error?**
```bash
cd /path/to/repo
git status  # Verify git is working
python3 scripts/restart_session.py
```

---

## For v0.5.0 Development

When ready to start v0.5.0 sprint:

```bash
# 1. Check current status
python3 scripts/restart_session.py

# 2. Review v0.5.0 roadmap
cat docs/EXTENDED_MONODROMY_FRAMEWORK_2026_07_25.md

# 3. Start Phase 1 (monodromy computation)
# → Follow roadmap in docs/EXTENDED_MONODROMY_FRAMEWORK_2026_07_25.md
```

---

**Last updated:** 2026-07-25  
**Maintained by:** Stream 2 (K3 Selection & Lattice)  
**For:** Three-stream coordination (Streams 1-3)
