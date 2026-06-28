#!/usr/bin/env python3
"""
PROJECT ALPHA-ORIGIN: an honest assessment of "deriving 1/137 from K3 geometry".

This script does NOT derive the fine-structure constant from geometry. It performs
two well-defined, defensible calculations and reports them with their caveats:

  (1) The standard one-loop MSSM gauge-coupling running from a unified coupling
      1/alpha_GUT ~= 1/25 at M_GUT ~ 2e16 GeV down to M_Z, to show what the RGE
      *actually* produces and why landing near 1/137 is MSSM physics, not geometry.

  (2) A magnitude check on the "chiral twin" quasar-dipole hypothesis: if alpha
      differed between an S_{1,2}-dominated and an S_{2,1}-dominated hemisphere by
      the geometric stiffness ratio, how large would the dipole be?

Run:  python3 scripts/alpha_origin_rge.py
"""
import math

# ------------------------------------------------------------------
# Inputs. IMPORTANT: none of these are fixed by the K3 topology.
# ------------------------------------------------------------------
M_Z      = 91.1876     # GeV
M_GUT    = 2.0e16      # GeV (canonical MSSM unification scale)
aGUT_inv = 24.3        # 1/alpha_GUT (~1/25): an INPUT, not a geometric output

# MSSM one-loop beta coefficients (alpha_1 in SU(5) / GUT normalization)
b1, b2, b3 = 33.0/5.0, 1.0, -3.0

t       = math.log(M_GUT / M_Z)
two_pi  = 2.0 * math.pi


def run_down(aGUT_inv: float):
    """One-loop run of the three couplings from M_GUT to M_Z."""
    a1_inv = aGUT_inv + (b1 / two_pi) * t
    a2_inv = aGUT_inv + (b2 / two_pi) * t
    a3_inv = aGUT_inv + (b3 / two_pi) * t
    # 1/alpha_em = 1/alpha_2 + 1/alpha_Y, with 1/alpha_Y = (5/3) * 1/alpha_1
    aem_inv = a2_inv + (5.0 / 3.0) * a1_inv
    return a1_inv, a2_inv, a3_inv, aem_inv


def main() -> None:
    a1_inv, a2_inv, a3_inv, aem_inv_MZ = run_down(aGUT_inv)

    print("=" * 64)
    print("(1) One-loop MSSM running  (1/alpha_GUT = %.1f at M_GUT = %.1e)" %
          (aGUT_inv, M_GUT))
    print("=" * 64)
    print("  1/alpha_1(M_Z) = %7.2f" % a1_inv)
    print("  1/alpha_2(M_Z) = %7.2f" % a2_inv)
    print("  1/alpha_3(M_Z) = %7.2f   -> alpha_s(M_Z) = %.4f" %
          (a3_inv, 1.0 / a3_inv))
    print("  ----------------------------------------")
    print("  DERIVED  1/alpha_em(M_Z) = %7.2f" % aem_inv_MZ)
    print()
    print("  MEASURED 1/alpha_em(M_Z) = 127.95")
    print("  MEASURED alpha_s(M_Z)    = 0.1179")
    print("  MEASURED 1/alpha_em(0)   = 137.036   (Thomson / q^2 -> 0 limit)")
    print()
    print("  The ~9.1 gap between 1/alpha_em(M_Z)=127.95 and 1/alpha_em(0)=137.036")
    print("  is QED + HADRONIC vacuum polarization. The hadronic part is")
    print("  non-perturbative and is taken from e+e- -> hadrons data; it CANNOT")
    print("  be derived from a compactification volume.")
    print()

    # Reverse-fit: which aGUT_inv reproduces the measured 1/alpha_em(M_Z)?
    coef      = 1.0 + 5.0 / 3.0
    beta_comb = b2 + (5.0 / 3.0) * b1
    aGUT_needed = (127.95 - (t / two_pi) * beta_comb) / coef
    print("  Reverse-fit: the 1/alpha_GUT that lands exactly on the measured")
    print("  1/alpha_em(M_Z)=127.95 is %.2f." % aGUT_needed)
    print("  => 'Landing on 137' is achieved by CHOOSING 1/alpha_GUT, i.e. it is")
    print("     a tuned input, not a prediction of the K3 geometry.")
    print()

    # ------------------------------------------------------------------
    print("=" * 64)
    print("(2) Quasar-dipole magnitude falsification ('chiral twins')")
    print("=" * 64)
    ratio = math.sqrt(1014.0 / 336.0)   # geometric inverse-coupling ratio S12/S21
    dalpha = ratio - 1.0                # implied Delta(alpha)/alpha between hemispheres
    observed = 1e-5                     # Webb-King claimed |Delta alpha/alpha|
    print("  Geometric ratio sqrt(1014/336)            = %.4f" % ratio)
    print("  Implied |Delta alpha/alpha| (S12 vs S21)   = %.3f  (= %.0f%%)" %
          (dalpha, 100 * dalpha))
    print("  Webb-King claimed dipole                  = %.0e" % observed)
    print("  OVERPREDICTION FACTOR                     = %.1e" % (dalpha / observed))
    print()
    print("  The chiral-twin hypothesis overpredicts the claimed dipole by ~5")
    print("  orders of magnitude. Even granting a domain-wall hemisphere split,")
    print("  a 74%% variation in alpha is excluded by BBN, the CMB, and atomic")
    print("  clocks at the |Delta alpha/alpha| < 1e-6 level. Moreover, the")
    print("  Webb-King dipole itself is contested: ESPRESSO/VLT (Murphy et al.")
    print("  2022) finds no confirmation and tightens the bound. The hypothesis")
    print("  is therefore FALSIFIED on magnitude alone.")


if __name__ == "__main__":
    main()
