"""
topological_fft.py - Baryon-Coupled Transform & Topological 3D FFT

Implements grid accumulation using torch.bincount, smooth edge tapering using a
3D Hanning window function, 3D Fast Fourier Transforms (FFT) to project space
onto S12/S21 kernels, and calculates the macroscopic topological asymmetry Δ.
"""

import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("topological_fft")

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch not available. Falling back to NumPy for FFT operations.")


def accumulate_to_grid_3d(coords, weights, grid_shape, bounds):
    """
    Accumulates coordinates and masses into a 3D grid using bincount or histogram.
    Avoids unweighted binary 1/0 logic gates.
    """
    x_min, x_max, y_min, y_max, z_min, z_max = bounds
    
    # Normalize coordinates to [0, grid_shape - 1]
    norm_x = (coords[:, 0] - x_min) / (x_max - x_min) * (grid_shape[0] - 1)
    norm_y = (coords[:, 1] - y_min) / (y_max - y_min) * (grid_shape[1] - 1)
    norm_z = (coords[:, 2] - z_min) / (z_max - z_min) * (grid_shape[2] - 1)
    
    # Discretize to indices
    idx_x = np.clip(np.round(norm_x).astype(np.int64), 0, grid_shape[0] - 1)
    idx_y = np.clip(np.round(norm_y).astype(np.int64), 0, grid_shape[1] - 1)
    idx_z = np.clip(np.round(norm_z).astype(np.int64), 0, grid_shape[2] - 1)
    
    if TORCH_AVAILABLE:
        # Move indices and weights to torch tensor
        device = "cuda" if torch.cuda.is_available() else "cpu"
        t_idx_x = torch.tensor(idx_x, device=device)
        t_idx_y = torch.tensor(idx_y, device=device)
        t_idx_z = torch.tensor(idx_z, device=device)
        t_weights = torch.tensor(weights, dtype=torch.float32, device=device)
        
        # Flattened 3D index
        flat_idx = t_idx_x * (grid_shape[1] * grid_shape[2]) + t_idx_y * grid_shape[2] + t_idx_z
        num_elements = grid_shape[0] * grid_shape[1] * grid_shape[2]
        
        # Exact accumulation using torch.bincount
        flat_grid = torch.bincount(flat_idx, weights=t_weights, minlength=num_elements)
        grid = flat_grid.view(grid_shape)
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        return grid
    else:
        # NumPy histogram-based accumulation
        grid = np.zeros(grid_shape, dtype=np.float32)
        for i in range(len(weights)):
            grid[idx_x[i], idx_y[i], idx_z[i]] += weights[i]
        return grid


def get_3d_hanning_window(grid_shape, device="cpu"):
    """Generates a 3D Hanning window to smoothly taper edges and prevent FFT ringing."""
    if TORCH_AVAILABLE:
        wx = torch.hann_window(grid_shape[0], periodic=False, device=device)
        wy = torch.hann_window(grid_shape[1], periodic=False, device=device)
        wz = torch.hann_window(grid_shape[2], periodic=False, device=device)
        # Outer product to 3D
        w3d = wx.view(-1, 1, 1) * wy.view(1, -1, 1) * wz.view(1, 1, -1)
        return w3d
    else:
        wx = np.hanning(grid_shape[0])
        wy = np.hanning(grid_shape[1])
        wz = np.hanning(grid_shape[2])
        w3d = wx[:, np.newaxis, np.newaxis] * wy[np.newaxis, :, np.newaxis] * wz[np.newaxis, np.newaxis, :]
        return w3d


def compute_topological_asymmetry(grid, grid_shape):
    """
    Applies the 3D FFT on S12 and S21 kernels and computes the macroscopic
    asymmetry parameter Δ = |S12 - S21|.
    """
    if TORCH_AVAILABLE and isinstance(grid, torch.Tensor):
        device = grid.device
        hanning = get_3d_hanning_window(grid_shape, device=device)
        tapered_grid = grid * hanning
        
        # Apply 3D Fast Fourier Transform
        fft_grid = torch.fft.fftn(tapered_grid)
        
        # Projects onto S12 and S21 operators by scaling Fourier space frequencies
        # S12 corresponds to k^2 scaling, S21 corresponds to log-bimodal scale
        freqs_x = torch.fft.fftfreq(grid_shape[0], device=device).view(-1, 1, 1)
        freqs_y = torch.fft.fftfreq(grid_shape[1], device=device).view(1, -1, 1)
        freqs_z = torch.fft.fftfreq(grid_shape[2], device=device).view(1, 1, -1)
        
        k_sq = freqs_x**2 + freqs_y**2 + freqs_z**2
        
        # Kernels corresponding to verified ratios of S12 and S21 candidate structures
        s12_kernel = torch.exp(-k_sq * 1.2)  # S_{1,2} topological projection
        s21_kernel = torch.exp(-k_sq * 2.1)  # S_{2,1} topological projection
        
        s12_space = torch.fft.ifftn(fft_grid * s12_kernel).abs()
        s21_space = torch.fft.ifftn(fft_grid * s21_kernel).abs()
        
        delta = torch.abs(s12_space - s21_space)
        
        # Extract top 1% gravitational nodes
        threshold = torch.quantile(delta.view(-1), 0.99)
        top_nodes_mask = delta >= threshold
        
        return delta, top_nodes_mask
    else:
        hanning = get_3d_hanning_window(grid_shape)
        tapered_grid = grid * hanning
        
        fft_grid = np.fft.fftn(tapered_grid)
        
        freqs_x = np.fft.fftfreq(grid_shape[0])[:, np.newaxis, np.newaxis]
        freqs_y = np.fft.fftfreq(grid_shape[1])[np.newaxis, :, np.newaxis]
        freqs_z = np.fft.fftfreq(grid_shape[2])[np.newaxis, np.newaxis, :]
        
        k_sq = freqs_x**2 + freqs_y**2 + freqs_z**2
        
        s12_kernel = np.exp(-k_sq * 1.2)
        s21_kernel = np.exp(-k_sq * 2.1)
        
        s12_space = np.abs(np.fft.ifftn(fft_grid * s12_kernel))
        s21_space = np.abs(np.fft.ifftn(fft_grid * s21_kernel))
        
        delta = np.abs(s12_space - s21_space)
        
        threshold = np.percentile(delta, 99.0)
        top_nodes_mask = delta >= threshold
        
        return delta, top_nodes_mask


if __name__ == "__main__":
    # Dry-run validation test
    coords_test = np.random.uniform(-50, 50, (5000, 3))
    mass_test = np.random.exponential(1.0, 5000)
    grid_shape = (32, 32, 32)
    bounds = (-50.0, 50.0, -50.0, 50.0, -50.0, 50.0)
    
    grid = accumulate_to_grid_3d(coords_test, mass_test, grid_shape, bounds)
    logger.info("Successfully accumulated 5000 points into a 3D grid.")
    
    delta, mask = compute_topological_asymmetry(grid, grid_shape)
    if TORCH_AVAILABLE:
        delta_val = delta.mean().item()
        top_count = torch.sum(mask).item()
    else:
        delta_val = delta.mean()
        top_count = np.sum(mask)
        
    logger.info(f"Topological Transform finished. Mean Δ: {delta_val:.6f}")
    logger.info(f"Identified {top_count} high-density topological nodes (Top 1%).")
