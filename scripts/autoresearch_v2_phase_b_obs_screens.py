"""
AutoEvolve R2 / Phase B — G2-4 observational screens: PTA (NANOGrav) and
Lyman-alpha forest. Literature-bound comparison ONLY (Rule 1: no invented or
simulated data; every number below carries its citation).

PTA screen
----------
A coherently oscillating ultralight scalar produces a monochromatic pressure
oscillation at f = m_a c^2 / h (standard phenomenology; formalized conditionally
in lean4_formal_proofs/Agora/Phenomenology/PTAFrequencyRatio.lean).
  f[Hz] = 2.4180e14 * m_a[eV]        (c^2/h in Hz/eV)
NANOGrav 15-yr sensitive band taken as [2e-9, 6e-8] Hz (NANOGrav 15-yr data set,
Agazie et al. 2023, ApJL 951 L8: T ~ 16 yr -> f_min ~ 1/T ~ 2 nHz; sensitivity
degrades above tens of nHz). Corresponding mass band:
  m in [8.3e-24, 2.5e-22] eV.
GAP-2 caveat carried over verbatim: candidate masses at the common reference
point (tau=33.6, V=1e4) use the REVERSE-ENGINEERED v1 normalization; PTA-band
membership at that point is a normalization-dependent statement, not a
parameter-free prediction. Cross-candidate frequency RATIOS at a common (tau,V)
are normalization-independent up to the shared instanton factor and are
reported for that reason.

Lyman-alpha screen
------------------
Published lower bounds on the mass of fuzzy dark matter constituting ALL of DM:
  m_a > 3.8e-21 eV   (Irsic et al. 2017, PRL 119, 031302, XQ-100+HIRES/MIKE)
  m_a > 2e-20  eV    (Rogers & Peiris 2021, PRL 126, 071302, emulator-based)
A candidate whose reference-point mass falls below these bounds is IN TENSION
with Lyman-alpha if the axion is all of DM; this is reported honestly even
where it disfavors the flagship ~1e-21 eV regime (Rule 4).

Input : data/autoresearch_v2/g2_1_stiffness_contours.json
Output: data/autoresearch_v2/g2_4_obs_screens.json
"""

import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "data", "autoresearch_v2")

HZ_PER_EV = 2.4180e14          # c^2/h
NANOGRAV_BAND_HZ = (2e-9, 6e-8)   # Agazie et al. 2023 (15-yr), see docstring
PTA_MASS_BAND_EV = (NANOGRAV_BAND_HZ[0] / HZ_PER_EV, NANOGRAV_BAND_HZ[1] / HZ_PER_EV)
LYA_BOUNDS = {
    "irsic_2017_prl119_031302": 3.8e-21,
    "rogers_peiris_2021_prl126_071302": 2.0e-20,
}


def main():
    with open(os.path.join(OUT_DIR, "g2_1_stiffness_contours.json")) as f:
        g2_1 = json.load(f)

    out = {"_method": {"hz_per_ev": HZ_PER_EV,
                       "nanograv_band_hz": NANOGRAV_BAND_HZ,
                       "pta_mass_band_ev": PTA_MASS_BAND_EV,
                       "lyman_alpha_bounds_ev": LYA_BOUNDS,
                       "caveat": "reference-point masses use the GAP-2 "
                                 "reverse-engineered normalization (tau=33.6, "
                                 "V=1e4); see g2_1 provenance note"}}
    refs = {}
    for cid, entry in g2_1.items():
        if cid.startswith("_"):
            continue          # metadata keys (e.g. _structural_finding)
        if entry.get("status") != "OK":
            out[cid] = {"status": "BLOCKED",
                        "reason": entry.get("reason", "no G2-1 window")}
            continue
        m_ref = entry["reference_point"]["m_a_eV"]
        lo, hi = entry["mass_window_eV"]
        refs[cid] = m_ref
        f_ref = m_ref * HZ_PER_EV
        pta_at_ref = NANOGRAV_BAND_HZ[0] <= f_ref <= NANOGRAV_BAND_HZ[1]
        window_hits_pta = not (hi < PTA_MASS_BAND_EV[0] or lo > PTA_MASS_BAND_EV[1])
        lya = {name: {"bound_eV": b,
                      "ref_mass_in_tension_if_all_DM": bool(m_ref < b)}
               for name, b in LYA_BOUNDS.items()}
        out[cid] = {"status": "OK",
                    "reference_m_a_eV": m_ref,
                    "pta": {"f_ref_hz": f_ref,
                            "in_nanograv_band_at_reference": bool(pta_at_ref),
                            "window_intersects_pta_band": bool(window_hits_pta)},
                    "lyman_alpha": lya}

    # normalization-independent cross-candidate frequency ratios at common (tau,V)
    if "apery_zeta3" in refs:
        base = refs["apery_zeta3"]
        out["_frequency_ratios_vs_apery_zeta3"] = {
            cid: (m / base) for cid, m in sorted(refs.items())}

    with open(os.path.join(OUT_DIR, "g2_4_obs_screens.json"), "w") as f:
        json.dump(out, f, indent=1)

    print(f"PTA mass band: [{PTA_MASS_BAND_EV[0]:.2e}, {PTA_MASS_BAND_EV[1]:.2e}] eV")
    for cid in sorted(refs):
        e = out[cid]
        tension = any(v["ref_mass_in_tension_if_all_DM"]
                      for v in e["lyman_alpha"].values())
        print(f"  {cid:26} m_ref={e['reference_m_a_eV']:.2e} eV "
              f"PTA@ref={e['pta']['in_nanograv_band_at_reference']} "
              f"LyA-tension(all-DM)={tension}")


if __name__ == "__main__":
    main()
