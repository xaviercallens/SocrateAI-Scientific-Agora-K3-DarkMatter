-- Agora: K3 Dark Matter Formal Verification Library
-- Root module importing all proof components

-- Core K3 topology and stability proofs
import Agora.K3_Topology
import Agora.BimodalStability
import Agora.GaugeCoupling

-- Discovery proofs from the full Agora pipeline
import Agora.Discovery.FuzzyDarkMatter
import Agora.Discovery.HubbleTension
import Agora.Discovery.ChameleonStability
import Agora.Discovery.S20Cosmology
import Agora.Discovery.CYBenchmarks
import Agora.Discovery.UniversalScaling
import Agora.Discovery.Monodromy

-- Conjectures (stated as axioms, not sorry)
import Agora.Conjectures.MirrorSymmetry
import Agora.MassFromInstanton
