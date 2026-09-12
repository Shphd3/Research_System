"""Top-k nonnegative sparse autoencoder with forward-normalized decoder columns.
This is a deliberately small baseline, not a reproduction of Gao et al.'s AuxK recipe.
"""
from dataclasses import dataclass
import torch
from torch import nn
from torch.nn import functional as F

@dataclass
class SAEOutput:
    reconstruction: torch.Tensor
    indices: torch.Tensor
    values: torch.Tensor
    loss_sum: torch.Tensor
    token_count: torch.Tensor

class TopKSAE(nn.Module):
    def __init__(self, hidden_size: int, width: int, k: int):
        super().__init__()
        if not 0 < k <= width or hidden_size <= 0:
            raise ValueError("Require 0 < k <= width and hidden_size > 0")
        self.hidden_size, self.width, self.k = hidden_size, width, k
        self.decoder = nn.Parameter(torch.randn(hidden_size, width))
        self.encoder = nn.Linear(hidden_size, width)
        self.bias = nn.Parameter(torch.zeros(hidden_size))
        self.register_buffer("firing_counts", torch.zeros(width, dtype=torch.long))
        self.register_buffer("tokens_observed", torch.zeros((), dtype=torch.long))
        with torch.no_grad():
            self.decoder.copy_(F.normalize(self.decoder, dim=0))
            self.encoder.weight.copy_(self.decoder.T)
            self.encoder.bias.zero_()

    def dictionary(self):
        return F.normalize(self.decoder, dim=0, eps=1e-8)

    def encode(self, x):
        scores = F.relu(self.encoder(x - self.bias))
        values, indices = scores.topk(self.k, dim=-1, sorted=True)
        return indices, values

    def decode(self, indices, values):
        # Dense scatter/GEMM is the reference path. No claim of a fused sparse kernel.
        z = values.new_zeros(*values.shape[:-1], self.width)
        z.scatter_(-1, indices, values)
        return F.linear(z, self.dictionary(), self.bias)

    def forward(self, x):
        if x.ndim != 2 or x.shape[1] != self.hidden_size:
            raise ValueError("SAE input must be [sampled_tokens, hidden_size]")
        indices, values = self.encode(x)
        reconstruction = self.decode(indices, values)
        # Target and scale are detached. In auxiliary mode gradient enters h ONLY
        # through the encoder/reconstruction path, NOT through the target branch.
        target = x.detach().float()
        per_token = (reconstruction.float() - target).square().mean(-1)
        per_token = per_token / target.square().mean(-1).clamp_min(1e-4)
        return SAEOutput(reconstruction, indices, values, per_token.sum(),
                         torch.tensor(x.shape[0], device=x.device, dtype=torch.long))

    @torch.no_grad()
    def record_activity(self, out: SAEOutput):
        """Call explicitly in TRAINING only; evaluation never changes counters.
        DDP trainer must aggregate counts across ranks before interpreting deadness.
        """
        ids = out.indices[out.values > 0]
        self.firing_counts.add_(torch.bincount(ids, minlength=self.width))
        self.tokens_observed.add_(out.token_count)
