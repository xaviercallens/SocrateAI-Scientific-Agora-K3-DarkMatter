#!/usr/bin/env bash
# =============================================================================
# agora_restart.sh — Session Context Loader for the SocrateAI K3xT2 Project
# =============================================================================
# Purpose: re-orient a fresh Claude Code (or human) session FAST. Prints the
#          skills, project context, and the tier-routed implementation plan,
#          then runs read-only health checks. Safe & non-destructive by design
#          (no writes, no network) so it runs without permission prompts.
#
# Usage:
#   bash scripts/agora_restart.sh            # full briefing + health checks
#   bash scripts/agora_restart.sh --brief    # briefing only, skip health checks
#   bash scripts/agora_restart.sh --health   # health checks only
#
# Author: Xavier Callens / Socrate AI Lab
# =============================================================================

set -uo pipefail

WORKSPACE_DIR="/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-K3-DarkMatter"
cd "${WORKSPACE_DIR}" 2>/dev/null || { echo "Workspace not found: ${WORKSPACE_DIR}"; exit 1; }

MODE="${1:-full}"

hr() { printf '=%.0s' {1..77}; echo; }
sec() { echo; hr; echo "  $1"; hr; }

briefing() {
  sec "🌌 AGORA SESSION RESTART — K3 (S1,2/S2,1) x T2 DARK-SECTOR PROJECT"
  echo "  Time (UTC):   $(date -u '+%Y-%m-%d %H:%M:%S')"
  echo "  Workspace:    ${WORKSPACE_DIR}"
  echo "  Git branch:   $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
  echo "  Latest tag:   $(git describe --tags --abbrev=0 2>/dev/null || echo 'none')"
  echo "  Last commit:  $(git log -1 --format='%h %s' 2>/dev/null || echo '?')"

  sec "📜 THE 8 NON-NEGOTIABLE RULES  (source: .agents/AGENTS.md)"
  cat <<'EOF'
  1. No Simulation        — no metric without hard execution data
  2. Strict Formalization — proven only if `lake build` passes, zero `sorry`
  3. No LLM Math Arbiter  — Lean 4 kernel / exact symbolic is truth, not LLMs
  4. Adversarial          — assume bugs & hallucinations until proven; no hype
  5. Exact Sequences      — physical sequences from executed code only
  6. Atomic Caveats       — every CAVEATS.md caveat appears in every manuscript
  7. No Circular Deriv.   — a fit to a target is a fit, NOT a derivation
  8. Cross-Consistency    — one number identical across code/JSON/paper/Lean
EOF

  sec "🛠  RIGOR SKILLS  (.agents/skills/ — index: .agents/SKILLS_INDEX.md)"
  cat <<'EOF'
  claim-classification-audit   label every claim [VERIFIED]/[FITTED]/[PREDICTED]
  falsifiability-audit         every [PREDICTED] needs a falsification gate
  axiom-gap-disclosure         axiom -> comment -> CAVEATS -> OPEN_PROBLEMS -> paper
  empirical-data-validation    real data only; report chi2/dof; log lineage
  honest-alternatives-generator on tension: Tier1/2/3 alternatives w/ equations
  cross-consistency-gate       Rule 8 checker + PARAMETER_LEDGER.yaml
  strict-math-verification     no-sorry / lake-build / physical-derivative checks
EOF

  sec "🎯 SIX LOAD-BEARING GAPS  (full review: scientificplan.md)"
  cat <<'EOF'
  GAP-1 [critical]  K3 identification conjectural (monodromy/modularity)   -> WS1
  GAP-2 [critical]  stiffness V''(0)=1014/336 has no PF->potential deriv.   -> WS2
  GAP-3 [serious]   superradiance uses small-alpha formula out of range     -> WS3
  GAP-4 [serious]   chameleon gamma=0.25 -> unphysical KW index n=-3        -> WS3
  GAP-5 [moderate]  cosmology pre-Boltzmann, rest-IC, reverse-eng. epsilon  -> WS5
  GAP-6 [mechanical] general-n S20 recurrence still a Lean `axiom`          -> WS4

  Sharpest parameter-free test: if BOTH PTA lines detected, their frequency
  ratio must be in (1.73,1.75)=sqrt(1014/336); moduli tau,V cancel.
EOF

  sec "🧭 IMPLEMENTATION PLAN — TASKS BY EXECUTOR TIER  (TODO.md §0)"
  cat <<'EOF'
  [HAIKU] mechanical, fully specified — run on Haiku:
    T8.1 cross_consistency_check.sh + PARAMETER_LEDGER.yaml   (do first)
    T8.2 CI gate (lake build / pytest / no-sorry / consistency)
    T4.2 finite-range decide proofs for S1,2 / S2,1
    T2.1 document V''(0) pipeline + regression test
    T2.3 kernel-verify PTA frequency-ratio lemma
    T1.1 monodromy matrices   T1.2 Weil/modularity   T1.3 mirror-map integrality
    T1.4 propagate WS1 outcomes to caveats/manuscripts
    T5.1 tracker-IC lambda sweep    T3.2 S2,1-bare superradiance survival
    T6.2 galactic-frame PTA spec    T7.1 compactification §1.5 scaffold
    T5.4 DESI DR2 refit (when public)

  [SONNET+] multi-step derivation / non-trivial debugging:
    T2.2 PF->potential-curvature derivation memo
    T3.1 Dolan (2007) continued-fraction growth rates
    T4.1 compile WZ certificate into Lean (chunkable to Haiku)
    T5.2 CLASS-fork mass-varying-axion ingestion
    T5.3 joint epsilon likelihood (JWST x S8 see-saw test)
    T6.1 PTA injection-recovery forecast (enterprise)

  [HUMAN] domain judgement / external collaborator (OPEN_PROBLEMS.md 1-2):
    T3.3 screening-alternatives sign-off
    T7.2 tadpole feasibility (seeking string phenomenologists)

  Recommended solo-Haiku order:
    T8.1 -> T8.2 -> T4.2 -> T2.1 -> T2.3 -> T1.1 -> T1.2 -> T1.3 -> T1.4
       -> T5.1 -> T3.2 -> T6.2 -> T7.1 -> T5.4
  Skip & report if an upstream SONNET+/data dependency is unmet.
EOF

  sec "📁 KEY FILES"
  cat <<'EOF'
  scientificplan.md            referee review + full task specs (inputs/verify)
  ROADMAP.md §2 Phase 6        workstreams + milestones M1..M6
  TODO.md §0                   active task tracker (this plan)
  OPEN_PROBLEMS.md             disclosed gaps + collaboration asks
  CAVEATS.md                   detailed limitation disclosures
  PREDICTIONS.md               falsifiable forecasts (Euclid/ELT/LISA/PTA)
  .agents/AGENTS.md            the 8 rules   .agents/SKILLS_INDEX.md   skills
  lean4_formal_proofs/         `lake build Agora` to verify
EOF

  sec "🚦 STANDING INSTRUCTIONS FOR EVERY TIER"
  cat <<'EOF'
  - Never invent numbers; report tracebacks verbatim (Rule 1).
  - Never upgrade a claim's tier: computational => [VERIFIED-computational];
    only `lake build` => [VERIFIED-kernel] (claim-classification-audit).
  - Negative results (failed Weil bound, excluded S2,1, dead see-saw) go to
    the TOP of the report and into the manuscripts (Rule 4).
  - Any task touching a ledger number (lambda,w0,wa,H0,eps,masses,stiffness,
    alpha_eff,PTA periods) triggers the full cross-consistency-gate (Rule 8).
  - Stop on ambiguity/missing data/Lean timeout: write BLOCKED, do not improvise.
EOF
}

health() {
  sec "🩺 READ-ONLY HEALTH CHECKS"

  echo "• git status (short):"
  git status --short 2>/dev/null | sed 's/^/    /' || echo "    (git unavailable)"
  echo

  echo "• real sorry stubs in Agora Lean sources (tactic position only, excludes .lake/ & prose):"
  local sorry_re='(^\s*sorry\b|:=\s*sorry\b|\bby\s+sorry\b)'
  local n
  n=$(grep -rlnE "${sorry_re}" --include='*.lean' --exclude-dir=.lake lean4_formal_proofs/ 2>/dev/null | wc -l | tr -d ' ')
  if [ "${n}" = "0" ]; then echo "    ✓ zero project files contain a real 'sorry' stub"; else
    echo "    ⚠ ${n} project file(s) contain real 'sorry' stub(s):"
    grep -rlnE "${sorry_re}" --include='*.lean' --exclude-dir=.lake lean4_formal_proofs/ 2>/dev/null | while read -r f; do
      local imported cnt; cnt=$(grep -cE "${sorry_re}" "$f")
      if grep -rqE "import .*$(basename "$f" .lean)\b" --include='*.lean' --exclude-dir=.lake lean4_formal_proofs/ 2>/dev/null; then imported="IN BUILD GRAPH"; else imported="orphaned, not imported"; fi
      echo "      ${f}  (${cnt} stub(s); ${imported})"
    done
    echo "    note: orphaned files do not affect 'lake build Agora'; still qualify any 'repo is sorry-free' claim."
  fi
  echo

  echo "• explicit axioms on record in Agora sources (expected; must be disclosed in OPEN_PROBLEMS.md):"
  grep -rnE '^\s*axiom ' --include='*.lean' --exclude-dir=.lake lean4_formal_proofs/ 2>/dev/null | wc -l | sed 's/^/    /'
  echo

  echo "• cross-consistency gate (Rule 8):"
  if [ -x scripts/cross_consistency_check.sh ] || [ -f scripts/cross_consistency_check.sh ]; then
    bash scripts/cross_consistency_check.sh 2>&1 | tail -5 | sed 's/^/    /'
  else
    echo "    ⧗ scripts/cross_consistency_check.sh not yet implemented (task T8.1)"
  fi
  echo

  echo "• lake toolchain:"
  if command -v lake >/dev/null 2>&1; then echo "    ✓ lake present — run: (cd lean4_formal_proofs && lake build Agora)";
  else echo "    ⚠ lake not on PATH — Lean checks will be skipped"; fi
  echo

  echo "• PARAMETER_LEDGER.yaml:"
  if [ -f PARAMETER_LEDGER.yaml ]; then echo "    ✓ present"; else echo "    ⧗ not yet created (task T8.1)"; fi
}

case "${MODE}" in
  --brief|-b)   briefing ;;
  --health|-h)  health ;;
  full|*)       briefing; health ;;
esac

sec "✅ CONTEXT LOADED"
echo "  Read scientificplan.md for full task specs. Pick the first unchecked"
echo "  [HAIKU] task in TODO.md §0 and follow its Steps/Acceptance/Verify block."
echo
