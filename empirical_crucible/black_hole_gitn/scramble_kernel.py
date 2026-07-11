import torch

# Try importing Triton, provide a robust PyTorch fallback if not available
try:
    import triton
    import triton.language as tl
    HAS_TRITON = True
except ImportError:
    HAS_TRITON = False

if HAS_TRITON:
    @triton.jit
    def stable_scrambling_softmax_kernel(
        logits_ptr, output_ptr, mask_ptr, num_elements, BLOCK_SIZE: tl.constexpr
    ):
        """
        Triton JIT kernel for stable scrambling softmax with NaN shielding.
        """
        pid = tl.program_id(0)
        offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
        mask = offsets < num_elements
        
        # Load logits and mask
        logits = tl.load(logits_ptr + offsets, mask=mask, other=-float('inf'))
        is_masked = tl.load(mask_ptr + offsets, mask=mask, other=True)
        
        # Apply masking - set fully evaporated/scrambled states to -inf
        logits = tl.where(is_masked, -float('inf'), logits)
        
        # Online Softmax subtraction to prevent overflow
        max_logit = tl.max(logits, axis=0)
        
        # Shield NaN: If max_logit is -inf (fully masked), set max_logit to 0.0
        # This prevents -inf - (-inf) = NaN in register subtraction
        safe_max = tl.where(max_logit == -float('inf'), 0.0, max_logit)
        
        # Compute exponentials safely
        exp_logits = tl.exp(logits - safe_max)
        exp_logits = tl.where(is_masked, 0.0, exp_logits) # Ensure zero contribution
        
        sum_exp = tl.sum(exp_logits, axis=0)
        
        # Compute final stable probabilities
        probs = exp_logits / (sum_exp + 1e-12)
        tl.store(output_ptr + offsets, probs, mask=mask)

def triton_stable_scramble(logits, mask):
    """
    Python wrapper calling the Triton stable scrambling kernel, or falling back
    to a PyTorch implementation if Triton is unavailable.
    """
    if not HAS_TRITON or not logits.is_cuda:
        # High-precision PyTorch Fallback
        # Apply mask
        logits = logits.clone()
        logits[mask] = -float('inf')
        
        # Stable softmax
        max_logit = torch.max(logits, dim=-1, keepdim=True).values
        safe_max = torch.where(max_logit == -float('inf'), torch.zeros_like(max_logit), max_logit)
        
        exp_logits = torch.exp(logits - safe_max)
        exp_logits[mask] = 0.0
        
        sum_exp = torch.sum(exp_logits, dim=-1, keepdim=True)
        probs = exp_logits / (sum_exp + 1e-12)
        return probs

    # Proceed with Triton Execution on CUDA
    orig_shape = logits.shape
    flat_logits = logits.view(-1)
    flat_mask = mask.view(-1)
    num_elements = flat_logits.numel()
    
    output = torch.empty_like(flat_logits)
    BLOCK_SIZE = 1024
    grid = (triton.cdiv(num_elements, BLOCK_SIZE),)
    
    stable_scrambling_softmax_kernel[grid](
        flat_logits, output, flat_mask, num_elements, BLOCK_SIZE=BLOCK_SIZE
    )
    
    return output.view(*orig_shape)

if __name__ == "__main__":
    # Small test on CPU (triggers the PyTorch fallback)
    test_logits = torch.tensor([1.0, 2.0, 3.0, 4.0])
    test_mask = torch.tensor([False, False, False, True]) # Fourth state is fully masked/evaporated
    
    probs = triton_stable_scramble(test_logits, test_mask)
    print("Test logits:", test_logits)
    print("Test mask (evaporated states):", test_mask)
    print("Calculated stable probabilities:", probs)
    print("Sum of probabilities:", probs.sum().item())
    assert torch.abs(probs.sum() - 1.0) < 1e-5, "Probabilities must sum to 1.0"
