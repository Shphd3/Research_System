"""Strict, serializable configuration for the pretraining-only research model.
Architecture follows the inspected Qwen3 implementation; this is not an HF checkpoint loader.
"""
from dataclasses import asdict, dataclass, fields
import json
from pathlib import Path

@dataclass
class Qwen3SAEConfig:
    vocab_size: int = 151936
    hidden_size: int = 1024
    intermediate_size: int = 3072
    num_hidden_layers: int = 10
    num_attention_heads: int = 16
    num_key_value_heads: int = 8
    head_dim: int = 128  # Deliberately NOT hidden_size // num_attention_heads.
    max_position_embeddings: int = 2048
    rope_theta: float = 1_000_000.0
    rms_norm_eps: float = 1e-6
    initializer_range: float = 0.02
    tie_word_embeddings: bool = True
    sae_mode: str = "observer"  # none | observer | auxiliary | bottleneck
    sae_width: int = 8192
    sae_k: int = 32
    sae_loss_weight: float = 1.0
    bottleneck_alpha: float = 0.0
    ce_chunk_tokens: int = 128
    checkpoint_ce: bool = True
    gradient_checkpointing: bool = False

    def __post_init__(self):
        ints = ("vocab_size", "hidden_size", "intermediate_size", "num_hidden_layers",
                "num_attention_heads", "num_key_value_heads", "head_dim", "max_position_embeddings",
                "sae_width", "sae_k", "ce_chunk_tokens")
        for name in ints:
            v = getattr(self, name)
            if not isinstance(v, int) or isinstance(v, bool) or v <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if self.num_attention_heads % self.num_key_value_heads:
            raise ValueError("Query heads must be divisible by KV heads")
        if self.head_dim % 2:
            raise ValueError("RoPE requires even head_dim")
        if self.sae_k > self.sae_width:
            raise ValueError("sae_k exceeds dictionary width")
        if self.sae_mode not in {"none", "observer", "auxiliary", "bottleneck"}:
            raise ValueError("Unknown SAE mode")
        if not 0.0 <= self.bottleneck_alpha <= 1.0 or self.sae_loss_weight < 0:
            raise ValueError("Invalid SAE weight / interpolation coefficient")
        if self.sae_mode != "bottleneck" and self.bottleneck_alpha != 0:
            raise ValueError("alpha is meaningful only for bottleneck mode")
        if self.rope_theta <= 0 or self.rms_norm_eps <= 0:
            raise ValueError("Invalid normalization / rotary parameters")

    def to_dict(self):
        return asdict(self)

    def save(self, path):
        Path(path).write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def from_dict(cls, obj):
        unknown = set(obj) - {f.name for f in fields(cls)}
        if unknown:
            raise ValueError(f"Unknown configuration keys: {sorted(unknown)}")
        return cls(**obj)

    @classmethod
    def load(cls, path):
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
