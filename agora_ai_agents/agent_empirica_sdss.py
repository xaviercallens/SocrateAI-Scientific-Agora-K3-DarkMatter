#!/usr/bin/env python3
"""
Agora Swarm - Agent Empirica: SDSS Cosmic Web Extractor
Downloads real 3D galaxy coordinates to build the WebGL Universe Point Cloud.
Target: Project Rosetta (Phase 3 - Topological Visualization)
"""

import os
import json
import numpy as np
from astroquery.sdss import SDSS
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

# 1. Define our Cosmology 
# We use the H0 = 71.92 km/s/Mpc derived from your Vafa-Continuity K3xT2 model!
cosmo = FlatLambdaCDM(H0=71.92, Om0=0.315)

def fetch_sdss_wedge(limit=20000):
    print(f"[*] Agent Empirica: Connecting to SDSS DR17 Database... Requesting {limit} galaxies.")
    
    # SQL Query: Fetch an "Equatorial Wedge" of the universe.
    # We select galaxies that trace the cosmic web filaments.
    # RA: 130 to 230 degrees, Dec: -5 to 5 degrees, Redshift (z): 0.02 to 0.2
    query = f"""
    SELECT TOP {limit} 
        ra, dec, z
    FROM SpecObj
    WHERE class = 'GALAXY' 
      AND z BETWEEN 0.02 AND 0.2
      AND ra BETWEEN 130 AND 230
      AND dec BETWEEN -5 AND 5
      AND zWarning = 0
    ORDER BY z ASC
    """
    
    print("[*] Executing SQL Query... Downloading Universe Slice...")
    try:
        result = SDSS.query_sql(query)
    except Exception as e:
        print(f"[!] SDSS Query failed with exception: {e}")
        return None
    
    if result is None:
        print("[!] Error: SDSS Query returned None. Check network or SDSS server status.")
        return None
        
    print(f"[+] Downloaded {len(result)} galaxies.")
    return result

def spherical_to_cartesian_json(data, filename="/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-K3-DarkMatter/grand_public/cosmic_web_sdss.json"):
    print("[*] Converting (RA, Dec, Redshift) to 3D Cartesian Coordinates (Mpc)...")
    
    # Extract arrays
    ra = data['ra'].data
    dec = data['dec'].data
    z = data['z'].data
    
    # Convert Redshift to Comoving Distance in Megaparsecs (Mpc)
    print("[*] Applying K3xT2 Cosmology to calculate comoving distances...")
    comoving_dist = cosmo.comoving_distance(z).value 
    
    # Convert degrees to radians
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)
    
    # Spherical to Cartesian transform
    X = comoving_dist * np.cos(dec_rad) * np.cos(ra_rad)
    Y = comoving_dist * np.cos(dec_rad) * np.sin(ra_rad)
    Z = comoving_dist * np.sin(dec_rad)
    
    # Center the point cloud around [0,0,0] for easy camera rotation in WebGL
    X = X - np.mean(X)
    Y = Y - np.mean(Y)
    Z = Z - np.mean(Z)
    
    print("[*] Packaging into WebGL-optimized JSON format...")
    
    # We flatten the array to [x1, y1, z1, x2, y2, z2, ...] 
    # This is 10x faster for WebGL GPU BufferGeometry than a list of dictionaries.
    points_array = []
    for i in range(len(data)):
        points_array.extend([
            round(float(X[i]), 3),
            round(float(Y[i]), 3),
            round(float(Z[i]), 3)
        ])
        
    payload = {
        "metadata": {
            "dataset": "SDSS_DR17_Equatorial_Wedge",
            "cosmology": "FlatLambdaCDM (H0=71.92)",
            "point_count": len(data),
            "format": "Flat Float32Array (X,Y,Z)"
        },
        "positions": points_array
    }
    
    # Ensure parent directories exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save the file
    with open(filename, "w") as f:
        json.dump(payload, f)
        
    file_size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"[+] Success! Point cloud saved to {filename} ({file_size_mb:.2f} MB)")

if __name__ == "__main__":
    sdss_data = fetch_sdss_wedge()
    if sdss_data:
        spherical_to_cartesian_json(sdss_data)
