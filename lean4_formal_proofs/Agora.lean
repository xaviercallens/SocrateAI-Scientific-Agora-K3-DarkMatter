-- Agora: K3 Dark Matter Formal Verification Library
-- Root module importing all proof components

-- Core K3 topology and stability proofs
import Agora.K3_Topology
import Agora.BimodalStability
import Agora.GaugeCoupling
import Agora.FeynmanSieveEquivalence

-- New submodules from Agora Implementation Plan
import Agora.Phenomenology.SymmetryBreaking
import Agora.Phenomenology.PTAFrequencyRatio
import Agora.Swampland.LVS_Stability
import Agora.Topology.AtiyahSinger


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
import Agora.BlackHole.InformationConservation

