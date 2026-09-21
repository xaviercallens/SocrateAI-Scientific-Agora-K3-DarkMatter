import Lake
open Lake DSL

/-!
Stream 2 root Lean project (2026-09-21, T0 directive: one toolchain for all streams, v4.34.0).

LEAN_TOOLCHAIN_ALIGNMENT: lean v4.34.0 / mathlib v4.34.0 / leanmaster TRIAL clone of v3.45.0

Capabilities: Mathlib + LeanMaster (`DualScaleStream2.Lattice`, reflections, signatures, O(d,d)).
Everything heavy lives on the SECOND DISK, never in `$HOME`:
  * packages (Mathlib etc.) are shared with the LeanMaster checkout this project requires;
  * this repository itself sits on /mnt/disks/disk-socrateai-local-1, so `.lake/build` does too.

STATUS OF THE LeanMaster DEPENDENCY — read before citing anything built here.
LeanMaster's own `main` is still on v4.34.0-rc2 (its lakefile says rc2 was chosen "for alignment
with other projects"). A consumer must use exactly LeanMaster's toolchain and Mathlib revision,
so until LeanMaster migrates this project requires a TRIAL CLONE of LeanMaster tag v3.45.0 with
only `lean-toolchain` and the Mathlib tag changed (rc2 -> v4.34.0), kept at
/mnt/disks/disk-socrateai-local-1/stream2-lean/leanmaster-v4.34.0-trial. The LeanMaster
repository and its running session were not touched. That clone has NOT been through LeanMaster's
five proof gates at the new toolchain; theorems imported from it are therefore
"LeanMaster v3.45.0 statements, rebuilt on a trial toolchain", not "LeanMaster-verified at v4.34.0".
When LeanMaster releases a v4.34.0 tag, replace the path require by the git require below and
delete this paragraph.

The legacy project `lean4_formal_proofs/` is separate and keeps its own lakefile.
-/

package «stream2-k3» where
  packagesDir := "/mnt/disks/disk-socrateai-local-1/stream2-lean/leanmaster-v4.34.0-trial/.lake/packages"
  leanOptions := #[⟨`maxHeartbeats, (1000000 : Nat)⟩]

require «SocrateAI-Scientific-Agora-LeanMaster» from
  "/mnt/disks/disk-socrateai-local-1/stream2-lean/leanmaster-v4.34.0-trial"

-- After LeanMaster's own migration, use instead:
-- require «SocrateAI-Scientific-Agora-LeanMaster» from git
--   "https://github.com/xaviercallens/SocrateAI-Scientific-Agora-LeanMaster" @ "<v4.34.0 tag>"

@[default_target]
lean_lib «Stream2Lean» where
  roots := #[`Stream2Lean]
