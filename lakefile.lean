import Lake
open Lake DSL

package «socrate-ai» {
  -- add package configuration options here
}

lean_lib Structures {
  -- add library configuration options here
}

lean_lib Agora {
  -- Fano supercongruences and mirror symmetry conjectures
}

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

-- `quantumInfo`/`slt` deliberately NOT required here (reverted 2026-07-11):
-- see lean4_formal_proofs/lakefile.lean for why.
