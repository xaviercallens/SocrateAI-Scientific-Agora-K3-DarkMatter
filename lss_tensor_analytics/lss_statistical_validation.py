"""
lss_statistical_validation.py - 3D 2-Point Cross-Correlation Validation

Computes the 3D 2-point cross-correlation function xi_{Δ, cluster}(r) between
the highest Δ topological nodes and known baryonic superclusters.
"""

import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lss_statistical_validation")

# Try to import scipy for spatial tree search, fall back to simple numpy search if unavailable
try:
    from scipy.spatial import KDTree
    SCIPY_SPATIAL_AVAILABLE = True
except ImportError:
    SCIPY_SPATIAL_AVAILABLE = False
    logger.warning("scipy.spatial not available. Cross-correlation will use vectorized numpy fallback.")


def compute_cross_correlation_3d(delta_coords, cluster_coords, r_bins):
    """
    Computes the 3D 2-point cross-correlation function xi(r).
    Using the Landy-Szalay or standard Peebles-Hauser estimator:
    xi(r) = (D1_D2(r) / R1_R2(r)) - 1
    For validation, we calculate the number of pairs as a function of distance r.
    """
    num_delta = len(delta_coords)
    num_clusters = len(cluster_coords)
    
    logger.info(f"Computing cross-correlation between {num_delta} topological nodes and {num_clusters} baryonic clusters...")
    
    num_bins = len(r_bins) - 1
    pair_counts = np.zeros(num_bins, dtype=np.int64)
    
    if SCIPY_SPATIAL_AVAILABLE:
        # High-performance KDTree spatial query
        delta_tree = KDTree(delta_coords)
        cluster_tree = KDTree(cluster_coords)
        
        # Count pairs in cumulative bins
        for idx in range(num_bins):
            r_outer = r_bins[idx + 1]
            r_inner = r_bins[idx]
            
            # Find all pairs within r_outer
            pairs_outer = delta_tree.count_neighbors(cluster_tree, r_outer)
            pairs_inner = delta_tree.count_neighbors(cluster_tree, r_inner)
            
            pair_counts[idx] = pairs_outer - pairs_inner
    else:
        # Vectorized / looped numpy fallback
        for idx in range(num_bins):
            r_inner = r_bins[idx]
            r_outer = r_bins[idx+1]
            bin_count = 0
            # For each delta node, calculate distances to all clusters
            for dc in delta_coords:
                dists = np.sqrt(np.sum((cluster_coords - dc)**2, axis=1))
                bin_count += np.sum((dists >= r_inner) & (dists < r_outer))
            pair_counts[idx] = bin_count
            
    # Normalize by random pair counts (analytical Poisson expectation)
    # Vol of bin = 4/3 * pi * (r_out^3 - r_in^3)
    # Expected density = num_delta * num_clusters / Total_Volume
    # For a box of 100 Mpc^3, total volume is 1e6 Mpc^3.
    total_volume = 100.0**3
    expected_pairs = []
    for idx in range(num_bins):
        r_inner = r_bins[idx]
        r_outer = r_bins[idx + 1]
        bin_vol = (4.0 / 3.0) * np.pi * (r_outer**3 - r_inner**3)
        expected = (num_delta * num_clusters / total_volume) * bin_vol
        expected_pairs.append(expected)
        
    expected_pairs = np.array(expected_pairs)
    
    # xi(r) = (Observed Pairs / Expected Pairs) - 1
    xi = np.zeros(num_bins)
    for idx in range(num_bins):
        if expected_pairs[idx] > 0:
            xi[idx] = (pair_counts[idx] / expected_pairs[idx]) - 1.0
        else:
            xi[idx] = 0.0
            
    return xi, pair_counts


if __name__ == "__main__":
    # Dry-run validation test
    np.random.seed(42)
    
    # Generate 100 delta nodes clustered around center
    delta_coords = np.random.normal(0, 5.0, (100, 3))
    # Generate 50 baryonic clusters clustered around same center (physical alignment)
    cluster_coords = np.random.normal(0, 6.0, (50, 3))
    
    r_bins = np.linspace(0.1, 20.0, 10)
    
    xi, counts = compute_cross_correlation_3d(delta_coords, cluster_coords, r_bins)
    
    logger.info("Validation complete.")
    for idx in range(len(r_bins) - 1):
        logger.info(f"Bin [{r_bins[idx]:.1f} - {r_bins[idx+1]:.1f}] Mpc -> Observed Pairs: {counts[idx]}, xi(r): {xi[idx]:.4f}")
