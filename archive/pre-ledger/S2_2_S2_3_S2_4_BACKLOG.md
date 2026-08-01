# S2-2, S2-3, S2-4 Backlog Tasks (Ready for Parallel Execution)

**Status:** Ready to execute in parallel with D-1v2 adjudication  
**Tier:** Haiku (S2-2, S2-3 low-cost calibration); Sonnet (S2-4 theory)  
**Dependency:** D-1v2 PASS (if FAIL, these tasks are deprioritized)

---

## S2-2: Effective Mass Law Reconciliation

**Scope:** Resolve inconsistent m_eff(Δ) formulations  
**Issue:** Two competing forms exist in codebase:
- Form A: `m_eff = m₀·exp(kΔ)` with k ≈ 0.048 (Part VI memory)
- Form B: `m_eff ≈ m₀(1+κΔ)^{1/4}` (AGORA_K3_T2_BRIDGE_PLAN.md)

**Task breakdown:**
1. **Retrieve both forms** from codebase (search git history)
2. **Find derivation sources** (which physics model gives each?)
3. **Reconcile**: Are they approximations of the same thing? Different regimes?
4. **Decide**: Which form use in D-3 empirical rerun?
5. **Document decision** in `data/k3t2/S2_2_EFFECTIVE_MASS_RECONCILIATION.md`

**Estimated effort:** Haiku 2–3 hours (literature search + comparison)  
**Output:** Single agreed-upon m_eff(Δ) formula with justification

---

## S2-3: Density-to-Modulus Mapping Parameterization

**Scope:** Move sigmoid from ad-hoc → parameterized + validated  
**Current state:** Sigmoid is functional but parameters (ρ_min, ρ_max, curvature) are hard-coded, not justified.

**Task breakdown:**
1. **Survey literature** on chameleon-coupling density mappings
2. **Extract parameter ranges** (what do other groups use?)
3. **Parameterize observable** to allow tuning: `L_K(ρ_b; θ)` where θ = [ρ_min, ρ_max, curve]
4. **Sensitivity analysis**: How much do L_K results change with θ?
5. **Choose canonical θ** for D-3 rerun (or marginalize if small effect)
6. **Document** in `data/k3t2/S2_3_MODULUS_MAPPING_VALIDATION.md`

**Estimated effort:** Haiku 1–2 hours (literature scan + code refactor)  
**Output:** Observable parameterized; θ justification written

---

## S2-4: True K3 Certification (LMFDB a_p Matching)

**Scope:** Confirm s₇/s₁₀ are "true K3 surfaces" via LMFDB newform matching  
**Current state:** Order-3 recurrences proven, but geometric family identification still open.

**Task breakdown:**
1. **Compute a_p tables** for s₇ and s₁₀ (existing code: `lss_tensor_analytics/k3_kernel_engine.py` → restore or rebuild)
2. **Query LMFDB** (API available at lmfdb.org/api) for weight-3 newforms at level-7 and level-10
3. **Match a_p sequences** (at primes p=2,3,5,7,11,... up to ~100): does s₇ a_p match a weight-3 newform?
4. **Record newform ID** (e.g., 7.2.e.a for level-7 weight-2 form, but we need weight-3)
5. **Document match** in `data/k3t2/S2_4_K3_LMFDB_CERTIFICATION.md` with:
   - S7 matched to: [LMFDB form ID]
   - S10 matched to: [LMFDB form ID]
   - Confidence: N/N primes matched (N = number of a_p checked)

**Estimated effort:** Sonnet 2–4 hours (LMFDB API, newform lookup, comparison logic)  
**Output:** Certified identification of s₇/s₁₀ with literature references

---

## Execution Plan (If D-1v2 PASS)

### Day 1 (Parallel with D-3 prep):
- **S2-2:** Reconcile effective-mass forms (Haiku, 2–3 hrs)
- **S2-3:** Parameterize density-modulus mapping (Haiku, 1–2 hrs)
- **S2-4:** LMFDB a_p matching (Sonnet, 2–4 hrs)

### Deliverables:
- `data/k3t2/S2_2_EFFECTIVE_MASS_RECONCILIATION.md` — single authoritative formula
- `data/k3t2/S2_3_MODULUS_MAPPING_VALIDATION.md` — parameterized observable + θ justification
- `data/k3t2/S2_4_K3_LMFDB_CERTIFICATION.md` — newform identification + confidence

### Impact:
- S2-2: Refines D-3 empirical observable (physics parameter)
- S2-3: Improves L_K robustness (sensitivity analyzed)
- S2-4: Converts K3 "conjecture" → "certified via literature" (Tier A+ for Stream-1)

---

## Decision Checkpoints

- **S2-2 Form A vs B**: Which is more justified? Which gives better fit to mock data?
- **S2-3 Sensitivity**: If L_K(ρ; θ₁) ≈ L_K(ρ; θ₂) to <5% error, marginalize θ in D-3 (simpler).
- **S2-4 Confidence**: If <80% a_p match, flag as "provisional" and defer full certification to Stream-1 theory work.

---

## Ready to Start? (After D-1v2 PASS)

```bash
# S2-2: Literature search
grep -r "m_eff" data/ docs/ empirical_crucible/ | head -20

# S2-3: Check current sigmoid code
grep -A 10 "density_to_modulus" empirical_crucible/s2_1_singular_locus_observable.py

# S2-4: Test LMFDB API
python3 -c "import urllib.request; print(urllib.request.urlopen('https://lmfdb.org/api/mf_newforms?level=7&weight=3').read())"
```

---

**All three tasks are Haiku-executable with clear success criteria. Start immediately upon D-1v2 PASS.**

Generated-by: Haiku 4.5 | Tier assignment verified | Ready for parallel dispatch
