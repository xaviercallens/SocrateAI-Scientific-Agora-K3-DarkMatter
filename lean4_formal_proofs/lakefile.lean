import Lake
open Lake DSL

package "socrate-ai" {
  -- LEAN_TOOLCHAIN_ALIGNMENT (2026-09-21, T0): lean v4.34.0 / mathlib v4.34.0.
  -- Packages are shared with the root project on the second disk (no second 8 GB Mathlib).
  packagesDir := "/mnt/disks/disk-socrateai-local-1/stream2-lean/leanmaster-v4.34.0-trial/.lake/packages"
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
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.34.0"

-- `quantumInfo`/`slt` deliberately NOT required here (reverted 2026-07-11):
-- they were added uncommitted for an unrelated, unfinished, `sorry`-containing
-- experiment (neuro_symbolic/K3_GITN_Integration.lean) whose manifest entries
-- were unresolved, which blocked `lake build Agora` entirely (mathlib cache
-- fetch for the resulting mismatched pins was not obtainable in-session).
-- Re-add only once that file is ready to be built for real.
