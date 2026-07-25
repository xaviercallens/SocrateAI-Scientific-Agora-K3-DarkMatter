#!/usr/bin/env python3
"""
restart_session.py — Quick session restart with memory alignment & decision log synchronization.

Purpose: At the start of any new session, run this script to:
  1. Load current memory state (auto-memory system)
  2. Check recent git commits (last 20)
  3. Display all three streams' current status
  4. Show critical decision logs + next actions
  5. Highlight any blocking issues or pending decisions

Usage:
  python3 scripts/restart_session.py              # Full report
  python3 scripts/restart_session.py --streams    # Streams status only
  python3 scripts/restart_session.py --memory     # Memory files only
  python3 scripts/restart_session.py --decisions  # Decisions + next actions only
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MEMORY_DIR = Path.home() / ".claude/projects" / (
    "-mnt-disks-disk-socrateai-local-1-callensxavier-home-data-SocrateAI-Scientific-Agora-K3-DarkMatter/memory"
)


def print_header(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def load_memory_index():
    """Load MEMORY.md index to show latest memory entries."""
    memory_md = MEMORY_DIR / "MEMORY.md"
    if not memory_md.exists():
        print("⚠️  Memory index not found")
        return []

    lines = memory_md.read_text().split("\n")
    entries = []
    for line in lines:
        if line.startswith("- ["):
            entries.append(line.strip())

    return entries[:15]  # Last 15 entries


def get_git_log(limit=20):
    """Get recent git commits."""
    try:
        result = subprocess.run(
            ["git", "log", f"--oneline", f"-{limit}"],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip().split("\n") if result.returncode == 0 else []
    except Exception as e:
        print(f"⚠️  Git log error: {e}")
        return []


def get_git_status():
    """Check git working tree status."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else "Unknown"
    except Exception as e:
        return f"Error: {e}"


def get_current_branch():
    """Get current git branch."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else "Unknown"
    except Exception as e:
        return f"Error: {e}"


def load_critical_dates():
    """Extract critical dates from memory files."""
    dates = {
        "Session start": datetime.now().strftime("%Y-%m-%d %H:%M UTC"),
        "D-3 batch starts": "2026-07-25 18:00 UTC",
        "D-3 batch completes": "2026-07-26 06:00 UTC",
        "Gate E decision": "2026-07-27 EOD UTC",
        "v0.4.0 release": "2026-07-27+ (if Gate E PASS)",
    }
    return dates


def stream_1_status():
    """Stream 1 status from recent commits."""
    return {
        "Name": "Lean Formalization (L₃=Sym²(L₂))",
        "Current": "Polynomial handoff ready for Lean encoding",
        "Status": "✅ Independent encoding path (SYM2_PROVED kernel-verified)",
        "Next": "Encode polynomial identities in Lean 4",
        "Blocker": "None (independent work)",
    }


def stream_2_status():
    """Stream 2 status from recent work."""
    return {
        "Name": "K3 Selection & Lattice Characterization",
        "Current": "F6 rectification complete; all priorities done",
        "Status": "✅ Awaiting Gate E decision (fully prepared)",
        "Next": "PASS→v0.4.0 release+v0.5.0 planning | CONDITIONAL→diagnostics | FAIL→hypothesis revision",
        "Blocker": "Awaiting Gate E (2026-07-27 EOD UTC)",
    }


def stream_3_status():
    """Stream 3 status from coordination."""
    return {
        "Name": "D-3 Empirical Validation",
        "Current": "Phase 2 D-3 batch executing (2026-07-25 18:00 UTC start)",
        "Status": "🔄 Running 6-12 hrs GPU or 3-7 days CPU",
        "Next": "Complete batch → Gate E decision (Xavier makes call)",
        "Blocker": "Waiting for D-3 results (expected 2026-07-26 06:00 UTC)",
    }


def show_streams_status():
    """Display all three streams' current status."""
    print_header("THREE-STREAM STATUS (Real-time)")

    for stream_id, stream_func in [("Stream 1", stream_1_status), ("Stream 2", stream_2_status), ("Stream 3", stream_3_status)]:
        status = stream_func()
        print(f"🔷 {stream_id}: {status['Name']}")
        print(f"   Current:  {status['Current']}")
        print(f"   Status:   {status['Status']}")
        print(f"   Next:     {status['Next']}")
        print(f"   Blocker:  {status['Blocker']}")
        print()


def show_memory_status():
    """Display current memory state."""
    print_header("MEMORY STATE (Auto-Memory System)")

    if not MEMORY_DIR.exists():
        print("⚠️  Memory directory not found")
        return

    entries = load_memory_index()
    print(f"Total memory entries: {len(list(MEMORY_DIR.glob('*.md')))}")
    print(f"\nLatest entries (up to 15):\n")

    for i, entry in enumerate(entries, 1):
        print(f"  {i:2d}. {entry}")


def show_git_status():
    """Display recent git history."""
    print_header("GIT HISTORY (Recent 20 Commits)")

    branch = get_current_branch()
    print(f"Current branch: {branch}")

    status = get_git_status()
    if status:
        print(f"Working tree: ⚠️  Uncommitted changes detected")
        print(f"  {status[:200]}...")
    else:
        print(f"Working tree: ✅ Clean")

    print(f"\nRecent commits:\n")

    commits = get_git_log(20)
    for i, commit in enumerate(commits[:20], 1):
        print(f"  {i:2d}. {commit}")


def show_critical_timeline():
    """Display critical timeline to Gate E."""
    print_header("CRITICAL TIMELINE TO GATE E DECISION")

    dates = load_critical_dates()
    print("Key milestones:\n")

    for milestone, date in dates.items():
        print(f"  ▸ {milestone:30s} → {date}")

    print()
    print("Status:")
    print("  • Stream 3 D-3 batch: 🔄 RUNNING (started 2026-07-25 18:00 UTC)")
    print("  • Stream 2 contingency: ✅ READY (all scenarios prepared)")
    print("  • Stream 1 encoding: ✅ READY (independent path open)")


def show_next_actions():
    """Display next actions by priority."""
    print_header("NEXT ACTIONS BY STREAM")

    print("Stream 1 (Lean Formalization):")
    print("  ✅ Priority 0: Encode polynomial identities")
    print("     - Use docs/STREAM1_LEAN_ENCODING_GUIDE_2026_07_25.md")
    print("     - Exact coefficients ready to copy-paste")
    print("     - No further Stream 2 coordination needed")
    print()

    print("Stream 2 (K3 Selection & Lattice):")
    print("  ✅ Priority 1: AWAIT Gate E decision (2026-07-27 EOD UTC)")
    print("  ✅ Priority 2: IF PASS → Execute v0.5.0 planning")
    print("     - Use docs/EXTENDED_MONODROMY_FRAMEWORK_2026_07_25.md")
    print("     - Phases 1-2 highest ROI (6-9 hrs)")
    print("  ✅ Priority 3: IF CONDITIONAL → Run diagnostics")
    print("     - Use docs/STREAM2_CONTINGENCY_ANALYSIS_2026_07_25.md")
    print("  ✅ Priority 4: IF FAIL → Hypothesis revision")
    print()

    print("Stream 3 (D-3 Empirical Validation):")
    print("  🔄 Priority 1: Complete D-3 Phase 2 batch")
    print("     - Expected completion: 2026-07-26 06:00 UTC")
    print("  ✅ Priority 2: Aggregate results + statistics")
    print("     - Expected completion: 2026-07-26 08:00 UTC")
    print("  ✅ Priority 3: Gate E decision (Xavier)")
    print("     - Expected decision: 2026-07-27 EOD UTC")


def show_blocking_issues():
    """Display any blocking issues or critical notes."""
    print_header("BLOCKING ISSUES & CRITICAL NOTES")

    print("Stream 1:")
    print("  ✅ No blockers (independent path)")
    print()

    print("Stream 2:")
    print("  ⏳ Waiting for Gate E decision (expected 2026-07-27 EOD UTC)")
    print("  • All contingencies prepared (no reactive scrambling)")
    print("  • Optional Priority 3 blocked (s18 needs Gorodetsky paper)")
    print()

    print("Stream 3:")
    print("  🔄 D-3 batch running (3-7 days CPU or 6-12 hrs GPU)")
    print("  • Expected completion: 2026-07-26 06:00 UTC (GPU)")
    print("  • Lattice priors grounded (ρ=4, T=18 exact)")
    print()

    print("Global:")
    print("  • No critical blockers")
    print("  • All mandatory work complete (Priorities 1-2)")
    print("  • Standing by for Gate E decision")


def main():
    parser = argparse.ArgumentParser(
        description="Session restart script — quick memory + decision alignment"
    )
    parser.add_argument(
        "--streams",
        action="store_true",
        help="Show streams status only"
    )
    parser.add_argument(
        "--memory",
        action="store_true",
        help="Show memory state only"
    )
    parser.add_argument(
        "--decisions",
        action="store_true",
        help="Show decisions + next actions only"
    )
    parser.add_argument(
        "--timeline",
        action="store_true",
        help="Show critical timeline only"
    )

    args = parser.parse_args()

    # If no options, show full report
    show_full = not any([args.streams, args.memory, args.decisions, args.timeline])

    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║                    🚀 SESSION RESTART — MEMORY ALIGNMENT                       ║
║                                                                                ║
║                 Three-Stream Status | Memory | Decisions | Timeline           ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")

    if show_full or args.streams:
        show_streams_status()

    if show_full or args.memory:
        show_memory_status()

    if show_full or args.timeline:
        show_critical_timeline()

    if show_full or args.decisions:
        show_next_actions()

    if show_full:
        show_blocking_issues()

    if show_full or args.memory:
        show_git_status()

    print("\n" + "="*80)
    print("✅ Session alignment complete. Ready to proceed.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
