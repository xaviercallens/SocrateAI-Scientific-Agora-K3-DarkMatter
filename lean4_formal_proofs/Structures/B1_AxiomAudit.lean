-- Structures/B1_AxiomAudit.lean
-- WP-B1 trust-base audit. Building this file prints the complete axiom
-- dependency of every B1 theorem, so the trust base is auditable in CI logs
-- rather than asserted in prose.
--
-- Expected output for every theorem below: the three standard Lean kernel
-- axioms [propext, Classical.choice, Quot.sound], plus ONLY those B1_Screening
-- physical-constant axioms the theorem genuinely needs. Any other name
-- appearing here (especially `sorryAx`) is a regression.

import Structures.B1_Chameleon
import Structures.B1_Sym2Bridge

-- Core screening lemmas (WP-B1 DoD 1–3)
#print axioms B1_Chameleon.screening_always_triggers
#print axioms B1_Chameleon.force_range_bounded
#print axioms B1_Chameleon.dense_env_short_range

-- Supporting monotonicity
#print axioms B1_Chameleon.screening_radius_strict_anti
#print axioms B1_Screening.m_eff_monotone
#print axioms B1_Screening.screening_radius_bounded

-- WP-B1 DoD 4 (corrected statement) + the recorded spec defect
#print axioms B1_Chameleon.no_unscreened_lmp
#print axioms B1_Chameleon.brief_literal_statement_is_refutable

-- B3 / SYM2_PARTNER bridge
#print axioms B1_Sym2Bridge.s7_site
#print axioms B1_Sym2Bridge.s10_site
#print axioms B1_Sym2Bridge.site_force_range_bounded
#print axioms B1_Sym2Bridge.site_screening_triggers
#print axioms B1_Sym2Bridge.site_denser_is_shorter
