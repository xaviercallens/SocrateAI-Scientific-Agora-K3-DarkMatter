-- Structures.lean
-- Root module for Stream 1 formalization
-- Imports all K3 topology, symmetric-square proofs, and chameleon screening

-- Chameleon screening formalization (WP-B1)
import Structures.Axioms.B1_Screening
import Structures.B1_Chameleon
import Structures.Tests.B1_screening_golden

-- Existing Stream 1 proof (Sym²)
import Structures.CooperSym2Proof

-- Cooper sequence infrastructure
import Structures.CooperS7Recurrence
import Structures.CooperS10Recurrence
import Structures.CooperS7_Topology

-- K3 foundational proofs
import Structures.K3GitnBlueprint
import Structures.S20Recurrence
import Structures.S20RecurrenceProof
import Structures.S20Decomposition

-- Additional recurrences and proofs
import Structures.TelescopingBinomial
import Structures.S12S21Recurrence
import Structures.T103Recurrence
