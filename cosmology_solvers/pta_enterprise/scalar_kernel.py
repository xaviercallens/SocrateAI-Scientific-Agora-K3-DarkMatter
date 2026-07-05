"""
scalar_kernel.py - PTA Scalar Monopole Overlap Reduction Function (ORF)

Implements the General Relativity Overlap Reduction Function (ORF) for a scalar 
breathing mode (scalar monopole): Gamma_Scalar(theta) = 1.0.
"""

import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scalar_kernel")


def overlap_reduction_function_scalar_breathing(theta):
    """
    Computes the Overlap Reduction Function (ORF) for a scalar breathing mode.
    Under General Relativity and scalar-tensor theories, the breathing mode of a 
    massless scalar field produces an isotropic (monopole-like) correlations 
    between all pulsar pairs, independent of their angular separation:
    Gamma_Scalar(theta) = 1.0 (or normalized to 1.0 / sqrt(3)).
    """
    theta_arr = np.atleast_1d(theta)
    
    # Isotropic correlation
    orf = np.ones_like(theta_arr, dtype=np.float64)
    
    return orf


def hellings_downs_orf(theta):
    """
    Computes the classical Hellings-Downs ORF for transverse-traceless 
    tensor-mode gravitational wave background (for comparison).
    """
    theta_rad = np.radians(theta)
    om_cos = (1.0 - np.cos(theta_rad)) / 2.0
    
    # HD formula: 1.5 * x * ln(x) - 0.25 * x + 0.5 where x = (1 - cos(theta)) / 2
    # with special treatment at theta = 0 (same pulsar)
    hd = np.zeros_like(theta_rad)
    for i, x in enumerate(om_cos):
        if x == 0.0:
            hd[i] = 1.0
        else:
            hd[i] = 1.5 * x * np.log(x) - 0.25 * x + 0.5
            
    return hd


if __name__ == "__main__":
    # Validate ORF values across typical angles
    angles = np.array([0.0, 30.0, 60.0, 90.0, 120.0, 150.0, 180.0])
    
    orf_scalar = overlap_reduction_function_scalar_breathing(angles)
    orf_hd = hellings_downs_orf(angles)
    
    logger.info("Angles (deg) | Scalar ORF | Hellings-Downs ORF")
    logger.info("-" * 46)
    for a, s, hd in zip(angles, orf_scalar, orf_hd):
        logger.info(f"{a:12.1f} | {s:10.4f} | {hd:18.4f}")
