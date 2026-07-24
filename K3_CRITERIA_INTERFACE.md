# K3 Criteria Interface

## Overview

This document defines the minimal K3 properties and interface requirements for the AutoEvolve integration.

## Minimal K3 Properties

### Mathematical Properties
1. **Order-3 ODE**: Must satisfy a third-order ordinary differential equation
2. **Holonomic Sequence**: Must be annihilated by its Picard-Fuchs ODE
3. **Symmetric-Square Structure**: ODE must have symmetric-square structure

### Physical Properties
1. **Swampland Compliance**: Must satisfy all Swampland conjectures
2. **String Vacua Compatibility**: Must be compatible with string theory vacuum solutions
3. **F-theory Alignment**: Must align with F-theory compactifications

## AutoEvolve Integration

### Training Data
- Cooper s7, s10, S22 sequences
- SDSS/Euclid survey data
- K3 topology metrics

### Ranking Criteria
- Mathematical Rigor: 60% weight
  - Order-3 ODE satisfaction
  - Holonomic sequence properties
  - Symmetric-square structure
- Empirical Fit: 30% weight
  - Match with survey data
  - Δ asymmetry alignment
  - Weak Lensing correlation
- Theoretical Consistency: 10% weight
  - Swampland compliance
  - F-theory alignment

## Validation

### Cross-Validation with Stream 1 (Theory)
- Verify Lean 4 proofs match AutoEvolve selection criteria
- Ensure mathematical properties are correctly implemented

### Cross-Validation with Stream 3 (Experimentation)
- Confirm AutoEvolve ranking aligns with V5 pipeline results
- Validate Δ scores against V5 pipeline measurements

## Implementation

See [auto_evolve_k3_selection.py](scripts/auto_evolve_k3_selection.py) for the implementation.

## Selection Handoff

Since W ≡ 0 is non-discriminating between s₇ and s₁₀ (structural for the whole Cooper ansatz),
active candidate discrimination now runs through the non-structural discriminators (C3b Sym²
partner map, C1/C2 Kodaira/lattice). See [briefs/PHASE_8_K3_SELECTION.md](briefs/PHASE_8_K3_SELECTION.md)
for the tiered task definitions and priority target (s₇, A183204).

## References

- [briefs/PHASE_8_K3_SELECTION.md](briefs/PHASE_8_K3_SELECTION.md)
- [DUAL_SCALE_HYPOTHESIS.md](DUAL_SCALE_HYPOTHESIS.md)
- [V3 Cosmic Topology Dashboard](dashboards/dual_scale_v3_cosmic_topology_dashboard.pdf)
- [V5 Dual-Scale Pipeline Dashboard](dashboards/v5_dual_scale_pipeline_dashboard.pdf)