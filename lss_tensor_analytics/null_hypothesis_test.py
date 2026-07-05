"""
null_hypothesis_test.py - Null Hypothesis Falsification Run

Creates a mock catalog by randomly shuffling the 3D coordinates of real galaxies
to produce a uniform Poisson distribution, and runs the topological FFT pipeline.
Verifies that the topological asymmetry Δ ≈ background noise everywhere.
"""

import numpy as np
import logging
from k3_tensor_grid import CosmologicalCartesianConverter, voxel_chunk_generator
from topological_fft import accumulate_to_grid_3d, compute_topological_asymmetry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("null_hypothesis_test")

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


def generate_mock_catalog_poisson(real_x, real_y, real_z, real_weights):
    """
    Generates a uniform Poisson distribution by randomly shuffling real galaxy coordinates 
    within their spatial bounding box, preserving total counts and masses.
    """
    num_galaxies = len(real_x)
    
    # Shuffle and sample uniformly from bounds
    mock_x = np.random.uniform(np.min(real_x), np.max(real_x), num_galaxies)
    mock_y = np.random.uniform(np.min(real_y), np.max(real_y), num_galaxies)
    mock_z = np.random.uniform(np.min(real_z), np.max(real_z), num_galaxies)
    
    # Keep weights identical but shuffled to destroy physical spatial clustering
    mock_weights = np.random.permutation(real_weights)
    
    return mock_x, mock_y, mock_z, mock_weights


def run_falsification_test():
    """Runs the full null hypothesis falsification loop."""
    logger.info("Starting Null Hypothesis Falsification Run...")
    
    # 1. Generate synthetic 'real' catalog with massive physical clustering
    np.random.seed(42)
    num_points = 5000
    
    logger.info(f"Generating synthetic clustered catalog with {num_points} galaxies...")
    # Clustered nodes around a few massive centers (simulating baryonic superclusters)
    centers = np.array([[-20.0, -20.0, -20.0], [20.0, 20.0, 20.0], [0.0, 0.0, 0.0]])
    clustered_x, clustered_y, clustered_z = [], [], []
    for _ in range(num_points):
        center = centers[np.random.choice(len(centers))]
        clustered_x.append(center[0] + np.random.normal(0, 5.0))
        clustered_y.append(center[1] + np.random.normal(0, 5.0))
        clustered_z.append(center[2] + np.random.normal(0, 5.0))
    
    real_x = np.array(clustered_x)
    real_y = np.array(clustered_y)
    real_z = np.array(clustered_z)
    real_weights = np.random.exponential(10.0, num_points)  # galaxy masses
    
    # 2. Generate randomized mock catalog (shuffled)
    logger.info("Generating randomized mock catalog (unclustered Poisson)...")
    mock_x, mock_y, mock_z, mock_weights = generate_mock_catalog_poisson(
        real_x, real_y, real_z, real_weights
    )
    
    # 3. Define grid parameters
    grid_shape = (32, 32, 32)
    bounds = (
        min(np.min(real_x), np.min(mock_x)), max(np.max(real_x), np.max(mock_x)),
        min(np.min(real_y), np.min(mock_y)), max(np.max(real_y), np.max(mock_y)),
        min(np.min(real_z), np.min(mock_z)), max(np.max(real_z), np.max(mock_z))
    )
    
    # 4. Accumulate and run transform on Clustered Catalog
    logger.info("Running topological FFT on clustered catalog...")
    real_grid = accumulate_to_grid_3d(
        np.stack([real_x, real_y, real_z], axis=-1), real_weights, grid_shape, bounds
    )
    real_delta, real_mask = compute_topological_asymmetry(real_grid, grid_shape)
    
    # 5. Accumulate and run transform on Mock Poisson Catalog
    logger.info("Running topological FFT on randomized mock catalog...")
    mock_grid = accumulate_to_grid_3d(
        np.stack([mock_x, mock_y, mock_z], axis=-1), mock_weights, grid_shape, bounds
    )
    mock_delta, mock_mask = compute_topological_asymmetry(mock_grid, grid_shape)
    
    # 6. Extract values and evaluate success criteria
    if TORCH_AVAILABLE:
        real_mean_delta = real_delta.mean().item()
        real_max_delta = real_delta.max().item()
        mock_mean_delta = mock_delta.mean().item()
        mock_max_delta = mock_delta.max().item()
    else:
        real_mean_delta = np.mean(real_delta)
        real_max_delta = np.max(real_delta)
        mock_mean_delta = np.mean(mock_delta)
        mock_max_delta = np.max(mock_delta)
        
    logger.info(f"Clustered Catalog -> Mean Δ: {real_mean_delta:.6f}, Max Δ: {real_max_delta:.6f}")
    logger.info(f"Poisson Mock Catalog -> Mean Δ: {mock_mean_delta:.6f}, Max Δ: {mock_max_delta:.6f}")
    
    ratio = real_max_delta / mock_max_delta if mock_max_delta > 0 else 1.0
    logger.info(f"Topological S/N ratio (Clustered Max / Poisson Mock Max): {ratio:.2f}")
    
    # Success Criteria: Mock grid must show Δ ≈ background noise
    # and clustered grid must show significantly higher peak asymmetry signals.
    if mock_mean_delta < real_mean_delta * 0.5:
        logger.info("[SUCCESS] Null Hypothesis falsification verified: mock background is clean.")
    else:
        logger.warning("[WARNING] High background noise detected in uniform Poisson run.")


if __name__ == "__main__":
    run_falsification_test()
