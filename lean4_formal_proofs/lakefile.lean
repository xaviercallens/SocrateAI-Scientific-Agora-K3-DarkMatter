import Lake
open Lake DSL

package "socrate-ai" {
  -- add package configuration options here
}

lean_lib Structures {
  -- add library configuration options here
}

lean_lib Agora {
  -- Fano supercongruences and mirror symmetry conjectures
  -- Now includes Part IV formal proofs
}

lean_lib neuro_symbolic {
  -- Neuro-symbolic integration and S20 Recurrence proofs
}

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

-- `quantumInfo`/`slt` deliberately NOT required here (reverted 2026-07-11):
-- they were added uncommitted for an unrelated, unfinished, `sorry`-containing
-- experiment (neuro_symbolic/K3_GITN_Integration.lean) whose manifest entries
-- were unresolved, which blocked `lake build Agora` entirely (mathlib cache
-- fetch for the resulting mismatched pins was not obtainable in-session).
-- Re-add only once that file is ready to be built for real.
