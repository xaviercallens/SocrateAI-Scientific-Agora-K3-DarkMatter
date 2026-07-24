# ✅ TODO: Immediate Actions (2026-07-24 EOD → 2026-07-25)

**Priority:** Critical path → Stream 1 (Lean) + Stream 2 (C1/C2 s10) in parallel

---

## Stream 2: Complete C1/C2 for s10 (Haiku — ~1 hour)

- [ ] **C1 s10:** `python3 checkers/check_C1.py --partner cooper_s10_partner`
  - Expected: 2-4 singular points (roots of B(k) for s10 recurrence)
  - Capture output → `data/certificates/C1_cooper_s10_partner.json`
  - Verify JSON structure, check fibre types

- [ ] **C2 s10:** `python3 checkers/check_C2.py --c1-cert data/certificates/C1_cooper_s10_partner.json`
  - Inputs: C1 certificate (fibre config)
  - Outputs: Picard number ρ, transcendental rank T
  - Capture output → `data/certificates/C2_cooper_s10_partner.json`

- [ ] **Lattice Comparison Report:** `data/reports/C1C2_LATTICE_REPORT_s7vs10.md`
  - Table: s7 vs s10 (singular points, ρ, T)
  - NO physics claims (Tier B geometry only)

- [ ] **Commit + Push** C1/C2 s10 + report

---

## Stream 1: Lean Sym² Encoding (Opus 4.8 — ~2 hours)

- [ ] **Encode L₂, L₃** in Polynomial ℚ with exact rational coefficients
- [ ] **Prove collapsed relations** via `ring`:
  - K₂ = 3P₁
  - K₁ = θ(P₁) + 4P₀
  - K₀ = 2θ(P₀)
- [ ] **Compile:** `lake env lean CooperS7Sym2Proof.lean` (0 errors, no sorry)
- [ ] **Repeat for s10**
- [ ] **Update status:** Repository state = [A] SYM2_PROVED
- [ ] **Commit + Push** Lean proofs + status update

---

## Stream 3: Monitor D-3 (Queued)

- [ ] Check if Stream 2 complete
- [ ] Queue D-3 sectors once Stream 2 → main

---

## Target: EOD 2026-07-25 (24-hour turnaround)

**Do NOT wait for Stream 2 to finish before Stream 1 starts** — they are independent. Launch both at 2026-07-24 21:00 UTC.
