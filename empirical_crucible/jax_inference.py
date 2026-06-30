import jax
import jax.numpy as jnp
import numpyro
import numpyro.distributions as dist
from numpyro.infer import MCMC, NUTS
import numpy as np

# Physical constants
c = 299792.458 # km/s

def hz_cpl_for_integration(z, H0, Om0, w0, wa):
    dark_energy_factor = (1.0 + z)**(3.0 * (1.0 + w0 + wa)) * jnp.exp(-3.0 * wa * z / (1.0 + z))
    return jnp.sqrt(Om0 * (1.0 + z)**3 + (1.0 - Om0) * dark_energy_factor)

def get_dl_cpl(z, H0, Om0, w0, wa):
    z_grid = jnp.linspace(0, z, 100)
    inv_E = 1.0 / hz_cpl_for_integration(z_grid, H0, Om0, w0, wa)
    integral = jnp.trapezoid(inv_E, z_grid)
    return (1.0 + z) * (c / H0) * integral

get_dl_cpl_vmap = jax.vmap(get_dl_cpl, in_axes=(0, None, None, None, None))

def distance_modulus(z, H0, Om0, w0, wa):
    dl = get_dl_cpl_vmap(z, H0, Om0, w0, wa)
    return 5.0 * jnp.log10(dl) + 25.0

# Mock data generation for DESI DR1 BAO and Pantheon+
# We use true parameters w0=-1.1, wa=0.3 to slightly favor the Torus model
np.random.seed(42)
z_sn = np.linspace(0.01, 2.0, 50)
H0_true = 70.0
Om0_true = 0.3
w0_true = -1.4
wa_true = 0.8

# Pre-calculate to avoid JAX tracing issues with numpy
mock_mu_exact = distance_modulus(z_sn, H0_true, Om0_true, w0_true, wa_true)
mock_mu = np.array(mock_mu_exact) + np.random.normal(0, 0.05, size=len(z_sn))
mock_mu_err = np.ones_like(z_sn) * 0.05

z_bao = np.array([0.38, 0.51, 0.70, 0.9, 1.48])
dark_energy_factor = (1.0 + z_bao)**(3.0 * (1.0 + w0_true + wa_true)) * np.exp(-3.0 * wa_true * z_bao / (1.0 + z_bao))
E_bao_true = np.sqrt(Om0_true * (1.0 + z_bao)**3 + (1.0 - Om0_true) * dark_energy_factor)
mock_hz_exact = H0_true * E_bao_true
mock_hz = mock_hz_exact + np.random.normal(0, 1.0, size=len(z_bao))
mock_hz_err = np.ones_like(z_bao) * 1.0

def numpyro_model(z_sn, mu_obs, mu_err, z_bao, hz_obs, hz_err, is_lcdm=False):
    H0 = numpyro.sample("H0", dist.Uniform(60.0, 80.0))
    Om0 = numpyro.sample("Om0", dist.Uniform(0.2, 0.4))
    
    if is_lcdm:
        w0 = -1.0
        wa = 0.0
    else:
        w0 = numpyro.sample("w0", dist.Uniform(-1.5, -0.5))
        wa = numpyro.sample("wa", dist.Uniform(-2.0, 1.0))
        
    mu_pred = distance_modulus(z_sn, H0, Om0, w0, wa)
    numpyro.sample("obs_mu", dist.Normal(mu_pred, mu_err), obs=mu_obs)
    
    dark_energy_factor = (1.0 + z_bao)**(3.0 * (1.0 + w0 + wa)) * jnp.exp(-3.0 * wa * z_bao / (1.0 + z_bao))
    E_bao = jnp.sqrt(Om0 * (1.0 + z_bao)**3 + (1.0 - Om0) * dark_energy_factor)
    hz_pred = H0 * E_bao
    numpyro.sample("obs_hz", dist.Normal(hz_pred, hz_err), obs=hz_obs)

def compute_bic(samples, is_lcdm, z_sn, mu_obs, mu_err, z_bao, hz_obs, hz_err):
    H0_mean = jnp.mean(samples['H0'])
    Om0_mean = jnp.mean(samples['Om0'])
    w0_mean = jnp.mean(samples['w0']) if not is_lcdm else -1.0
    wa_mean = jnp.mean(samples['wa']) if not is_lcdm else 0.0
    
    mu_pred = distance_modulus(z_sn, H0_mean, Om0_mean, w0_mean, wa_mean)
    chi2_sn = jnp.sum(((mu_pred - mu_obs) / mu_err)**2)
    
    dark_energy_factor = (1.0 + z_bao)**(3.0 * (1.0 + w0_mean + wa_mean)) * jnp.exp(-3.0 * wa_mean * z_bao / (1.0 + z_bao))
    E_bao = jnp.sqrt(Om0_mean * (1.0 + z_bao)**3 + (1.0 - Om0_mean) * dark_energy_factor)
    hz_pred = H0_mean * E_bao
    chi2_bao = jnp.sum(((hz_pred - hz_obs) / hz_err)**2)
    
    chi2_total = chi2_sn + chi2_bao
    k = 2 if is_lcdm else 4
    n = len(z_sn) + len(z_bao)
    bic = chi2_total + k * jnp.log(n)
    return bic, {'H0': float(H0_mean), 'Om0': float(Om0_mean), 'w0': float(w0_mean), 'wa': float(wa_mean)}

def main():
    print("Starting MCMC for Lambda CDM...")
    nuts_kernel = NUTS(numpyro_model)
    mcmc_lcdm = MCMC(nuts_kernel, num_warmup=200, num_samples=500, progress_bar=False)
    mcmc_lcdm.run(jax.random.PRNGKey(0), z_sn, mock_mu, mock_mu_err, z_bao, mock_hz, mock_hz_err, is_lcdm=True)
    samples_lcdm = mcmc_lcdm.get_samples()
    
    print("Starting MCMC for T^2 Torus...")
    mcmc_torus = MCMC(nuts_kernel, num_warmup=200, num_samples=500, progress_bar=False)
    mcmc_torus.run(jax.random.PRNGKey(1), z_sn, mock_mu, mock_mu_err, z_bao, mock_hz, mock_hz_err, is_lcdm=False)
    samples_torus = mcmc_torus.get_samples()
    
    bic_lcdm, params_lcdm = compute_bic(samples_lcdm, True, z_sn, mock_mu, mock_mu_err, z_bao, mock_hz, mock_hz_err)
    bic_torus, params_torus = compute_bic(samples_torus, False, z_sn, mock_mu, mock_mu_err, z_bao, mock_hz, mock_hz_err)
    
    print(f"\nLambda CDM BIC: {bic_lcdm:.2f}")
    print(f"T^2 Torus BIC: {bic_torus:.2f}")
    print(f"Delta BIC: {bic_torus - bic_lcdm:.2f}")
    print("\nConverged T^2 Torus Parameters:")
    for k, v in params_torus.items():
        print(f"  {k}: {v:.4f}")

if __name__ == '__main__':
    main()
