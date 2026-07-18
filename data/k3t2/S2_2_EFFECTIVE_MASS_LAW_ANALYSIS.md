# S2-2: Effective Mass Law Reconciliation (Analysis Skeleton)

**Date:** 2026-07-18  
**Status:** Ready for Sonnet derivation (D-1v2 PASS gate)  
**Tier:** Sonnet (theory) + Haiku (empirical validation)

---

## Problem Statement

Two conflicting effective-mass laws appear in the codebase:

### Form A: Exponential (From Part VI memory)
```
m_eff(Δ) = m₀ · exp(k·Δ)
with k ≈ 0.048
```

**Source:** Part VI memory (citation needed from git history)  
**Domain:** Presumably small Δ approximation  
**Usage:** Historical, not currently deployed in observables

### Form B: Power-law (From AGORA_K3_T2_BRIDGE_PLAN.md)
```
m_eff(Δ) ≈ m₀ · (1 + κ·Δ)^{1/4}
```

**Source:** AGORA_K3_T2_BRIDGE_PLAN.md  
**Domain:** Power-law chameleon screening family  
**Usage:** Referenced as a standard chameleon mechanism  
**Connection:** m_eff ∝ ρ^{(n+2)/(2n+2)} with n to be determined

---

## Theoretical Framework

### Chameleon Mechanism (Standard)

The chameleon scalar field φ couples conformally to matter:

```
L = −½ ∂_μφ ∂^μφ − V(φ) − A(φ) T^μ_μ
```

where:
- V(φ) = scalar potential (e.g., V(φ) = λφ⁴)
- A(φ) = conformal coupling function
- T^μ_μ = trace of stress-energy (ρ_b for dust)

### Effective Mass (Environmental Screening)

In a region of density ρ_b, the effective mass scales as:

```
m_eff²(ρ) ∝ dV/dφ|_min(ρ) ∝ ρ^{(n+2)/(2n+2)}
```

for potential V(φ) ∝ φⁿ (Khoury–Weltman family).

**Known values:**
- n = 1 (linear): m_eff ∝ ρ^{1/2} (dilaton-like)
- n = 4 (quartic): m_eff ∝ ρ^{1/3}
- n = −3 (unphysical): gives γ ≈ 0.25 (identified in CAVEATS.md §4 as problematic)

### Power-Law from Exponential?

For small Δ:
```
m_eff(Δ) = m₀ · exp(k·Δ)
         ≈ m₀ · (1 + k·Δ) [first-order Taylor]
```

If we replace k·Δ → κ·Δ and exponent → 1/4:
```
m_eff(Δ) ≈ m₀ · (1 + κ·Δ)^{1/4}
```

This is **not** a Taylor approximation; it's a **different functional form**. The exponent 1/4 suggests:
```
m_eff ∝ ρ^{1/4}
      = ρ^{(n+2)/(2n+2)}
⟹ (n+2)/(2n+2) = 1/4
⟹ 4(n+2) = 2n+2
⟹ 4n + 8 = 2n + 2
⟹ 2n = −6
⟹ n = −3
```

**Critical finding:** The m_eff ∝ ρ^{1/4} form implies **n = −3 (unphysical)**, which is already flagged in CAVEATS.md as problematic.

---

## Questions to Resolve

1. **Which form is physically correct?**
   - Does the chameleon potential naturally give n = −3, or is there a different mechanism?
   - Can we derive either form rigorously from first principles?

2. **Regime of validity:**
   - Is Form A (exponential) valid for small Δ only?
   - Is Form B (power-law) intended for all Δ, or only Δ → 0?

3. **Parameter meanings:**
   - Form A: What is k ≈ 0.048 in dimensionful units? What is Δ?
   - Form B: What is κ? How does it relate to coupling strength A(φ)?

4. **Observational status:**
   - Does either form match empirical superradiance/screening data?
   - Which form gives better fit to M87* / SMBHs with published spins?

---

## Recommended Resolution Path (Sonnet Task)

1. **Derive Form B rigorously** from chameleon potential V(φ) ∝ φⁿ
2. **Identify physical value of n** (constrained by screening observations)
3. **Compare Form A and Form B** in valid regimes; show whether one is special case of other
4. **Choose canonical form** for S3-00 (MVM derivation) and D-3 (empirical rerun)
5. **Validate against superradiance bounds** (GAP-3 analysis already in CAVEATS.md)

---

## Success Criteria

✅ **Done if:**
- Single agreed-upon m_eff(Δ) formula with clear derivation
- Physical value of n (if chameleon) or alternative mechanism name
- Written justification: why this form is preferred
- Parameters traced to literature or first-principles derivation

✅ **Output file:** `S2_2_EFFECTIVE_MASS_RECONCILIATION_FINAL.md`
   - Chosen formula
   - Derivation (2–3 pages)
   - Regime of validity (small vs. all Δ)
   - Empirical status (M87* / SMBH constraints)

---

## References (To Compile)

- Khoury & Weltman (2004): Original chameleon paper
- Hinterbichler & Khoury (2010): Chameleon screening review
- CAVEATS.md §4: Flagged n = −3 as unphysical
- Part VI memory: m_eff = m₀·exp(kΔ) source (to locate in git)
- AGORA_K3_T2_BRIDGE_PLAN.md: (1+κΔ)^{1/4} form

---

**This task is BLOCKING S3-00 (MVM derivation step 1).** Once m_eff(Δ) is finalized, Stream-3 can proceed with mass calculations.

**Ready for Sonnet execution upon D-1v2 PASS.**

Generated-by: Haiku 4.5 (analysis skeleton) | Theory work: Sonnet tier
