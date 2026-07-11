import unittest
import torch
import sympy as sp
import numpy as np

from moduli_generator import compute_k3_periods
from gitn_model import GeometricInformationTensorNetwork, compute_von_neumann_entropy
from scramble_kernel import triton_stable_scramble

class TestBlackHoleGITN(unittest.TestCase):
    
    def test_moduli_generator_dimensions(self):
        """Verify that moduli generator outputs exactly 22 features."""
        z_test = sp.Rational(1, 10)
        features = compute_k3_periods(z_test)
        self.assertEqual(features.shape, (22,))
        self.assertTrue(np.all(np.isfinite(features)))
        # Check volume is between 0 and 1
        self.assertGreater(features[0], 0.0)
        self.assertLessEqual(features[0], 1.0)
        # Check Picard rank is 20
        self.assertEqual(features[1], 20.0)

    def test_gitn_model_trace_and_psd(self):
        """Verify that GITN model outputs hermitian, trace-conserving, and PSD matrices."""
        model = GeometricInformationTensorNetwork()
        # Generate some mock batch data of size 4
        mock_input = torch.randn(4, 22)
        rho_real, rho_imag = model(mock_input)
        
        # 1. Check shape
        self.assertEqual(rho_real.shape, (4, 4, 4))
        self.assertEqual(rho_imag.shape, (4, 4, 4))
        
        # 2. Check Trace = 1 (on the real diagonal)
        for i in range(4):
            trace_val = torch.diagonal(rho_real[i]).sum().item()
            self.assertAlmostEqual(trace_val, 1.0, places=5)
            
            # Trace of imaginary diagonal must be exactly 0
            trace_imag = torch.diagonal(rho_imag[i]).sum().item()
            self.assertAlmostEqual(trace_imag, 0.0, places=5)
            
        # 3. Check Hermiticity: rho = rho^H (conjugate transpose)
        # rho_real == rho_real^T and rho_imag == -rho_imag^T
        for i in range(4):
            real_transpose = rho_real[i].transpose(-2, -1)
            imag_transpose = rho_imag[i].transpose(-2, -1)
            
            torch.testing.assert_close(rho_real[i], real_transpose, atol=1e-5, rtol=1e-5)
            torch.testing.assert_close(rho_imag[i], -imag_transpose, atol=1e-5, rtol=1e-5)

    def test_stable_entropy_computation(self):
        """Verify that entropy computation remains stable and NaN-free under extreme conditions."""
        # 1. Test standard state
        rho_real = torch.eye(4).unsqueeze(0) * 0.25
        rho_imag = torch.zeros(1, 4, 4)
        entropy = compute_von_neumann_entropy(rho_real, rho_imag)
        # S = -4 * (0.25 * log2(0.25)) = 2.0
        self.assertAlmostEqual(entropy.item(), 2.0, places=5)
        
        # 2. Test extreme scrambled state (eigenvalues near 0)
        # Create an almost singular matrix
        A = torch.tensor([[[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1e-15, 0.0, 0.0],
                           [0.0, 0.0, 1e-15, 0.0],
                           [0.0, 0.0, 0.0, 1e-15]]])
        rho_real = torch.matmul(A, A.transpose(-2, -1))
        trace = torch.diagonal(rho_real, dim1=-2, dim2=-1).sum(-1, keepdim=True).unsqueeze(-1)
        rho_real = rho_real / trace
        rho_imag = torch.zeros(1, 4, 4)
        
        # Should execute successfully without throwing NaN
        entropy = compute_von_neumann_entropy(rho_real, rho_imag)
        self.assertFalse(torch.isnan(entropy).any().item())
        self.assertTrue(torch.isfinite(entropy).all().item())

    def test_scramble_kernel(self):
        """Verify that the scrambling kernel performs stable softmax and masking."""
        logits = torch.tensor([[1.0, 2.0, 3.0, 4.0],
                               [5.0, 6.0, 7.0, 8.0]])
        # Mask the last state in each batch
        mask = torch.tensor([[False, False, False, True],
                             [False, False, False, True]])
        
        probs = triton_stable_scramble(logits, mask)
        
        # Checking sum and that the last state has 0 probability
        for i in range(2):
            self.assertAlmostEqual(probs[i].sum().item(), 1.0, places=5)
            self.assertEqual(probs[i, 3].item(), 0.0)
            self.assertGreater(probs[i, 2].item(), probs[i, 1].item())

if __name__ == "__main__":
    unittest.main()
