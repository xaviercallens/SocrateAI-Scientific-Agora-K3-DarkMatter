"""
k3_tensor_grid.py - LSS GPU Voxel-Chunking Tensor Grid

Converts RA, Dec, Redshift coordinates into comoving Cartesian coordinates and
implements out-of-core Voxel Chunking (100 Mpc^3 sectors) to fit VRAM limits on GPU/CPU.
"""

import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("k3_tensor_grid")

# Try importing specialized libraries, fall back to CPU/numpy equivalents
try:
    import astropy.units as u
    from astropy.coordinates import SkyCoord
    from astropy.cosmology import FlatLambdaCDM
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False
    logger.warning("astropy not available. Using high-precision standard cosmological integrator fallback.")

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch not available. Standard NumPy will be used for tensor grids.")

try:
    import dask.array as da
    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False
    logger.warning("Dask not available. Chunked out-of-core processing will use manual chunk generator.")


class CosmologicalCartesianConverter:
    """Handles coordinate conversion to comoving Cartesian coordinates."""
    def __init__(self, H0=71.92, Om0=0.315):
        self.H0 = H0
        self.Om0 = Om0
        if ASTROPY_AVAILABLE:
            self.cosmo = FlatLambdaCDM(H0=H0, Om0=Om0)
        else:
            self.c = 299792.458  # speed of light in km/s

    def comoving_distance(self, redshift):
        """Calculates comoving distance in Mpc using Simpson's integration rule if astropy is missing."""
        if ASTROPY_AVAILABLE:
            return self.cosmo.comoving_distance(redshift).value
        
        # High-precision numerical integrator for E(z) = sqrt(Om0*(1+z)^3 + (1-Om0))
        # Distance d_C(z) = c/H0 * \int_0^z dz'/E(z')
        redshift = np.atleast_1d(redshift)
        distances = []
        for z in redshift:
            if z <= 0.0:
                distances.append(0.0)
                continue
            # Numerical integration via Simpson's rule over 100 intervals
            n_steps = 100
            zs = np.linspace(0.0, z, n_steps + 1)
            ez = np.sqrt(self.Om0 * (1.0 + zs)**3 + (1.0 - self.Om0))
            integrand = 1.0 / ez
            # Simpson's integration
            h = z / n_steps
            integral = (integrand[0] + integrand[-1] + 
                        4.0 * np.sum(integrand[1:-1:2]) + 
                        2.0 * np.sum(integrand[2:-2:2])) * h / 3.0
            distances.append((self.c / self.H0) * integral)
        return np.array(distances)

    def convert_to_cartesian(self, ra, dec, redshift):
        """Converts RA, Dec (degrees) and Redshift into comoving X, Y, Z (Mpc)."""
        r = self.comoving_distance(redshift)
        
        if ASTROPY_AVAILABLE:
            coords = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=r*u.Mpc)
            x = coords.cartesian.x.value
            y = coords.cartesian.y.value
            z = coords.cartesian.z.value
            return x, y, z
        
        # Manual spherical-to-Cartesian coordinate transform
        ra_rad = np.radians(ra)
        dec_rad = np.radians(dec)
        
        x = r * np.cos(dec_rad) * np.cos(ra_rad)
        y = r * np.cos(dec_rad) * np.sin(ra_rad)
        z = r * np.sin(dec_rad)
        return x, y, z


def voxel_chunk_generator(x, y, z, weights, chunk_size_mpc=100.0):
    """
    Partitions the catalog coordinates into discrete voxel chunks to fit VRAM.
    Yields (chunk_coords, chunk_weights, chunk_bounds) for out-of-core operations.
    """
    min_x, max_x = np.min(x), np.max(x)
    min_y, max_y = np.min(y), np.max(y)
    min_z, max_z = np.min(z), np.max(z)
    
    logger.info(f"Catalog bounds: X:[{min_x:.1f}, {max_x:.1f}], Y:[{min_y:.1f}, {max_y:.1f}], Z:[{min_z:.1f}, {max_z:.1f}] Mpc")
    
    x_bins = np.arange(min_x, max_x + chunk_size_mpc, chunk_size_mpc)
    y_bins = np.arange(min_y, max_y + chunk_size_mpc, chunk_size_mpc)
    z_bins = np.arange(min_z, max_z + chunk_size_mpc, chunk_size_mpc)
    
    total_chunks = (len(x_bins)-1) * (len(y_bins)-1) * (len(z_bins)-1)
    logger.info(f"Total voxel chunks to process: {total_chunks}")
    
    for i in range(len(x_bins) - 1):
        for j in range(len(y_bins) - 1):
            for k in range(len(z_bins) - 1):
                mask = (
                    (x >= x_bins[i]) & (x < x_bins[i+1]) &
                    (y >= y_bins[j]) & (y < y_bins[j+1]) &
                    (z >= z_bins[k]) & (z < z_bins[k+1])
                )
                if np.any(mask):
                    yield (
                        np.stack([x[mask], y[mask], z[mask]], axis=-1),
                        weights[mask],
                        (x_bins[i], x_bins[i+1], y_bins[j], y_bins[j+1], z_bins[k], z_bins[k+1])
                    )


if __name__ == "__main__":
    # Dry-run validation test
    converter = CosmologicalCartesianConverter()
    # Generate 1000 random test galaxies
    np.random.seed(42)
    ra_test = np.random.uniform(0, 360, 1000)
    dec_test = np.random.uniform(-30, 30, 1000)
    z_test = np.random.uniform(0.01, 0.5, 1000)
    masses = np.random.exponential(1.0, 1000)
    
    x, y, z = converter.convert_to_cartesian(ra_test, dec_test, z_test)
    logger.info("Successfully converted 1000 coordinates to comoving Cartesian.")
    
    chunks = list(voxel_chunk_generator(x, y, z, masses, chunk_size_mpc=100.0))
    logger.info(f"Grid generated. Created {len(chunks)} populated chunks.")
