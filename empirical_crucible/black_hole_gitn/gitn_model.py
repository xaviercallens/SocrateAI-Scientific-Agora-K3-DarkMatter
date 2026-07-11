import torch
import torch.nn as nn

class GeometricInformationTensorNetwork(nn.Module):
    """
    Geometric Information Tensor Network (GITN).
    Maps the 22-dimensional K3 moduli/Betti features to a valid 4x4 complex density matrix rho.
    Enforces:
    1. Hermiticity
    2. Positive semi-definiteness (via auxiliary projection A A^H)
    3. Trace conservation (Tr(rho) = 1)
    """
    def __init__(self, input_dim=22, hidden_dim=64, state_dim=4):
        super(GeometricInformationTensorNetwork, self).__init__()
        self.state_dim = state_dim
        
        # Neural network mapping 22 features to 2 * state_dim^2 elements
        # (real and imaginary parts of the auxiliary matrix A)
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, 2 * state_dim * state_dim)
        )
        
    def forward(self, x):
        # x shape: (batch_size, 22)
        batch_size = x.shape[0]
        out = self.network(x) # (batch_size, 32)
        
        # Split into real and imaginary parts of auxiliary matrix A
        A_elements = out.view(batch_size, 2, self.state_dim, self.state_dim)
        A_real = A_elements[:, 0, :, :]
        A_imag = A_elements[:, 1, :, :]
        
        # Enforce positive semi-definiteness: rho_unnormalized = A * A^H
        # rho_unrec = (A_r + i * A_i) * (A_r^T - i * A_i^T)
        #           = (A_r * A_r^T + A_i * A_i^T) + i * (A_i * A_r^T - A_r * A_i^T)
        A_r_tr = A_real.transpose(-2, -1)
        A_i_tr = A_imag.transpose(-2, -1)
        
        rho_real = torch.matmul(A_real, A_r_tr) + torch.matmul(A_imag, A_i_tr)
        rho_imag = torch.matmul(A_imag, A_r_tr) - torch.matmul(A_real, A_i_tr)
        
        # Enforce Trace = 1
        # The trace of the imaginary part must be 0 (Hermitian matrix has real diagonal).
        # We divide both real and imaginary parts by the trace of the real part.
        trace = torch.diagonal(rho_real, dim1=-2, dim2=-1).sum(-1, keepdim=True).unsqueeze(-1)
        # Add epsilon to prevent division by zero
        trace = trace + 1e-12
        
        rho_real_normalized = rho_real / trace
        rho_imag_normalized = rho_imag / trace
        
        return rho_real_normalized, rho_imag_normalized

def compute_von_neumann_entropy(rho_real, rho_imag, min_val=1e-9):
    """
    Computes von Neumann entropy stably on GPU:
    S = -Tr(rho * log2(rho))
    Clamps eigenvalues to prevent NaN under thermal scrambling.
    """
    batch_size = rho_real.shape[0]
    
    # Reconstruct complex tensor for eigenvalue decomposition
    rho_complex = torch.complex(rho_real, rho_imag)
    
    # linalg.eigvalsh works on Hermitian matrices (it expects complex input)
    eigenvalues = torch.linalg.eigvalsh(rho_complex)
    
    # Clamp eigenvalues to prevent log2(0) or log2(-eps) which yield NaN
    clamped_eigenvalues = torch.clamp(eigenvalues, min=min_val)
    
    # Compute entropy
    entropy = -torch.sum(clamped_eigenvalues * torch.log2(clamped_eigenvalues), dim=-1)
    return entropy
