import math
import torch
import torch.nn as nn
from transformers.activations import ACT2FN
from .qwen3config import Qwen3Config

class Qwen3RMSNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-6):
        """
        Qwen3RMSNorm is equivalent to T5LayerNorm
        """
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def forward(self, hidden_states):
        input_dtype = hidden_states.dtype
        hidden_states = hidden_states.to(torch.float32)
        variance = hidden_states.pow(2).mean(-1, keepdim=True)
        hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)
        return self.weight * hidden_states.to(input_dtype)

    def extra_repr(self):
        return f"{tuple(self.weight.shape)}, eps={self.variance_epsilon}"


class LoRALinear(nn.Module):
    def __init__(self, in_features, out_features, rank, alpha, dropout=0.0, bias=False):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.scaling = alpha / rank if rank > 0 else 1.0

        self.lora_A = nn.Parameter(torch.zeros(rank, in_features))
        self.lora_B = nn.Parameter(torch.zeros(out_features, rank))
        self.dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()

        self.reset_parameters()

    def reset_parameters(self):
        # 科学初始化方案：
        # A 矩阵标准差：1/sqrt(in_features)，类似于 Kaiming 初始化
        # B 矩阵标准差：1/sqrt(rank)，用于抵消求和时的方差增长
        nn.init.normal_(self.lora_A, mean=0.0, std=1.0 / math.sqrt(self.in_features))
        nn.init.normal_(self.lora_B, mean=0.0, std=1.0 / math.sqrt(self.rank))

    def forward(self, x):
        result = self.dropout(x) @ self.lora_A.T @ self.lora_B.T
        return result * self.scaling


class MyQwen3MLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.hidden_size = config.hidden_size
        self.intermediate_size = config.intermediate_size
        self.gate_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.up_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.down_proj = nn.Linear(self.intermediate_size, self.hidden_size, bias=False)
        self.act_fn = ACT2FN[config.hidden_act]

    def forward(self, x):
        down_proj = self.down_proj(self.act_fn(self.gate_proj(x)) * self.up_proj(x))
        return down_proj


class MyQwen3ExpertMLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.hidden_size = config.hidden_size
        if config.moe_type == "multihead":
            self.intermediate_size = int(config.moe_intermediate_size * 3 / (2 * config.moe_head_num + 1)) + 1
            # print(f"multihead moe intermediate size: {self.intermediate_size}")
        else:
            self.intermediate_size = config.moe_intermediate_size
            
        self.act_fn = ACT2FN[config.hidden_act]
        
        # Check if using LoRA for experts
        self.use_lora = getattr(config, "use_lora", False)
        
        if self.use_lora:
            self.gate_lora = LoRALinear(
                self.hidden_size, self.intermediate_size, 
                config.lora_rank, config.lora_alpha, config.lora_dropout
            )
            self.up_lora = LoRALinear(
                self.hidden_size, self.intermediate_size, 
                config.lora_rank, config.lora_alpha, config.lora_dropout
            )
            
            out_dim = self.hidden_size // config.moe_head_num if config.moe_type == "multihead" else self.hidden_size
            self.down_lora = LoRALinear(
                self.intermediate_size, out_dim, 
                config.lora_rank, config.lora_alpha, config.lora_dropout
            )

            if config.lora_mode == "lora_bias":
                self.gate_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
                self.up_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
                self.down_proj = nn.Linear(self.intermediate_size, out_dim, bias=False)
                
                # Freeze base weights
                self.gate_proj.weight.requires_grad = False
                self.up_proj.weight.requires_grad = False
                self.down_proj.weight.requires_grad = False
            else:
                self.gate_proj = None
                self.up_proj = None
                self.down_proj = None
        else:
            self.gate_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
            self.up_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
            if config.moe_type == "multihead":
                self.down_proj = nn.Linear(self.intermediate_size, self.hidden_size // config.moe_head_num, bias=False)
            else:
                self.down_proj = nn.Linear(self.intermediate_size, self.hidden_size, bias=False)

    def forward(self, x):
        if self.use_lora:
            gate_out = self.gate_lora(x)
            up_out = self.up_lora(x)
            
            if self.gate_proj is not None:
                gate_out = gate_out + self.gate_proj(x)
                up_out = up_out + self.up_proj(x)
                
            activated = self.act_fn(gate_out) * up_out
            
            down_out = self.down_lora(activated)
            
            if self.down_proj is not None:
                down_out = down_out + self.down_proj(activated)
                
            return down_out
        else:
            down_proj = self.down_proj(self.act_fn(self.gate_proj(x)) * self.up_proj(x))
            return down_proj
