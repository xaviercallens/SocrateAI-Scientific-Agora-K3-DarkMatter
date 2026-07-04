import Lake
open Lake DSL

package socrate-ai {
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
