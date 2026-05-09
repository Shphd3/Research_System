from functools import partial
from typing import Callable, Optional, Tuple, Union

import torch
import torch.nn.functional as F
import torch.distributed as dist
from torch import nn

from transformers.activations import ACT2FN
from transformers.cache_utils import Cache, DynamicCache, SlidingWindowCache, StaticCache
from transformers.generation import GenerationMixin
from transformers.modeling_attn_mask_utils import AttentionMaskConverter
from transformers.modeling_flash_attention_utils import FlashAttentionKwargs
from transformers.modeling_outputs import (
    BaseModelOutputWithPast,
    CausalLMOutputWithPast,
    QuestionAnsweringModelOutput,
    SequenceClassifierOutputWithPast,
    TokenClassifierOutput,
)
from transformers.modeling_rope_utils import ROPE_INIT_FUNCTIONS
from transformers.modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel
from transformers.processing_utils import Unpack
from transformers.utils import (
    add_code_sample_docstrings,
    add_start_docstrings,
    add_start_docstrings_to_model_forward,
    logging,
    replace_return_docstrings,
)
from transformers.utils.deprecation import deprecate_kwarg
from .qwen3config import Qwen3Config
from .spectral_moe import SpectralMoELayer
from .modules import Qwen3RMSNorm, LoRALinear, MyQwen3MLP, MyQwen3ExpertMLP


class QuadraticTopKRouter(nn.Module):
    def __init__(
        self,
        input_dim: int,
        num_experts: int,
        top_k: int,
        eps: float = 1e-6,
    ):
        super().__init__()
        self.input_dim = input_dim
        self.num_experts = num_experts
        self.top_k = top_k
        self.eps = eps
        self.linear_router = nn.Linear(input_dim, num_experts, bias=False)
        self.quadratic_router = nn.Linear(input_dim, num_experts, bias=False)
        self.register_buffer("running_second_moment", torch.zeros(input_dim))

    @torch.no_grad()
    def _compute_global_feature_mean(self, values: torch.Tensor) -> torch.Tensor:
        x_f = values.detach().reshape(-1, values.shape[-1]).float()
        local_count = torch.tensor([x_f.size(0)], device=x_f.device, dtype=torch.float32)
        local_sum = x_f.sum(dim=0)
        if dist.is_initialized():
            dist.all_reduce(local_sum, op=dist.ReduceOp.SUM)
            dist.all_reduce(local_count, op=dist.ReduceOp.SUM)
        return local_sum / local_count.clamp_min(1.0)

    def _feature_like_input(self, feature_vec: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
        feature_vec = feature_vec.to(device=x.device, dtype=x.dtype)
        if x.dim() == 3:
            return feature_vec.view(1, 1, -1)
        return feature_vec.view(1, -1)

    def forward(self, x: torch.Tensor, running_beta: Optional[Union[float, torch.Tensor]] = None):
        quadratic_feature = x * x
        if self.training:
            if running_beta is None:
                raise ValueError("running_beta is required for quadratic router during training")
            if isinstance(running_beta, torch.Tensor):
                if running_beta.numel() == 0:
                    beta_val = 0.0
                else:
                    beta_val = float(running_beta.detach().to(dtype=torch.float32).max().item())
            else:
                beta_val = float(running_beta)
            beta_val = min(max(beta_val, 0.0), 1.0)
            second_moment = self._compute_global_feature_mean(quadratic_feature)
            self.running_second_moment.mul_(1.0 - beta_val).add_(second_moment, alpha=beta_val)
        quadratic_feature = quadratic_feature - self._feature_like_input(self.running_second_moment, x)
        logits = self.linear_router(x) + self.quadratic_router(quadratic_feature)
        probs = F.softmax(logits, dim=-1, dtype=torch.float)
        topk_probs, topk_indices = torch.topk(probs, self.top_k, dim=-1)
        return topk_probs, topk_indices, probs, logits


class SubspaceEnergyRouter(nn.Module):
    def __init__(
        self,
        input_dim: int,
        num_experts: int,
        top_k: int,
        rank: int,
        init_scale: float = 0.1,
        use_bias: bool = False,
    ):
        super().__init__()
        if rank <= 0:
            raise ValueError(f"low_rank_rank must be > 0, got {rank}")
        if rank > input_dim:
            raise ValueError(f"low_rank_rank ({rank}) must be <= input_dim ({input_dim})")
        self.input_dim = input_dim
        self.num_experts = num_experts
        self.top_k = top_k
        self.rank = rank
        self.init_scale = init_scale
        self.use_bias = use_bias
        self.V = nn.Parameter(torch.empty(num_experts, rank, input_dim))
        if use_bias:
            self.bias = nn.Parameter(torch.zeros(num_experts))
        else:
            self.register_parameter("bias", None)
        self.reset_parameters()

    def reset_parameters(self):
        with torch.no_grad():
            for expert_idx in range(self.num_experts):
                nn.init.orthogonal_(self.V[expert_idx])
            self.V.mul_(self.init_scale)
            if self.bias is not None:
                nn.init.zeros_(self.bias)

    def _mean_like_input(self, running_mean: torch.Tensor, hidden_states: torch.Tensor) -> torch.Tensor:
        running_mean = running_mean.to(device=hidden_states.device, dtype=hidden_states.dtype)
        if hidden_states.dim() == 3:
            return running_mean.view(1, 1, -1)
        if hidden_states.dim() == 2:
            return running_mean.view(1, -1)
        raise ValueError(f"SubspaceEnergyRouter expects 2D or 3D input, got shape {tuple(hidden_states.shape)}")

    def center_inputs(self, hidden_states: torch.Tensor, running_mean: torch.Tensor) -> torch.Tensor:
        return hidden_states - self._mean_like_input(running_mean, hidden_states)

    def compute_logits_from_centered(self, centered_hidden_states: torch.Tensor) -> torch.Tensor:
        squeeze_batch = False
        if centered_hidden_states.dim() == 2:
            centered_hidden_states = centered_hidden_states.unsqueeze(0)
            squeeze_batch = True
        projected = torch.einsum("bsd,krd->bskr", centered_hidden_states, self.V)
        logits = projected.square().sum(dim=-1)
        if self.bias is not None:
            logits = logits + self.bias.view(1, 1, -1)
        if squeeze_batch:
            logits = logits.squeeze(0)
        return logits

    def compute_routing(self, centered_hidden_states: torch.Tensor):
        logits = self.compute_logits_from_centered(centered_hidden_states)
        probs = F.softmax(logits, dim=-1, dtype=torch.float)
        topk_probs, topk_indices = torch.topk(probs, self.top_k, dim=-1)
        return topk_probs, topk_indices, probs, logits

    def compute_regularization_losses(self) -> Tuple[torch.Tensor, torch.Tensor]:
        V = self.V.float()
        vv_t = torch.matmul(V, V.transpose(-1, -2))
        eye = torch.eye(self.rank, device=V.device, dtype=V.dtype).unsqueeze(0)
        internal_loss = (vv_t - eye).square().sum()

        cross_matrix = torch.einsum("ird,jqd->ijrq", V, V)
        cross_pair_loss = cross_matrix.square().sum(dim=(-1, -2))
        cross_loss = cross_pair_loss.sum() - torch.diagonal(cross_pair_loss).sum()
        return internal_loss, cross_loss

    def forward(self, hidden_states: torch.Tensor, running_mean: torch.Tensor):
        centered_hidden_states = self.center_inputs(hidden_states, running_mean)
        return self.compute_routing(centered_hidden_states)


class CenteredLowRankRouter(nn.Module):
    def __init__(self, input_dim: int, num_experts: int, top_k: int, rank: int):
        super().__init__()
        if rank <= 0:
            raise ValueError(f"low_rank_rank must be > 0, got {rank}")
        if rank > input_dim:
            raise ValueError(f"low_rank_rank ({rank}) must be <= input_dim ({input_dim})")
        self.top_k = top_k
        self.down_proj = nn.Linear(input_dim, rank, bias=False)
        self.up_proj = nn.Linear(rank, num_experts, bias=True)

    def forward(self, x: torch.Tensor):
        logits = self.up_proj(self.down_proj(x))
        probs = F.softmax(logits, dim=-1, dtype=torch.float)
        topk_probs, topk_indices = torch.topk(probs, self.top_k, dim=-1)
        return topk_probs, topk_indices, probs, logits


class MyQwen3SparseMoeBlock(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.num_experts = config.num_experts
        self.top_k = config.num_experts_per_tok
        self.norm_topk_prob = config.norm_topk_prob
        self.router_center_input = getattr(config, 'router_center_input', False)
        self.router_center_mode = getattr(config, "router_center_mode", "batch")
        self.router_center_grad_mode = getattr(config, "router_center_grad_mode", "none")
        self.router_center_decay_base = getattr(config, "router_center_decay_base", 0.99)
        self.router_center_decay_scale = getattr(config, "router_center_decay_scale", 1.0)
        self.router_aux_gate = getattr(config, 'router_aux_gate', False)
        self.router_acp_transform = getattr(config, "router_acp_transform", False)
        self.router_acp_eps = getattr(config, "router_acp_eps", 1e-6)
        self.router_acp_mode = getattr(config, "router_acp_mode", "parallel")
        self.router_type = getattr(config, "router_type", "linear")
        self.low_rank_rank = getattr(config, "low_rank_rank", 0)
        self.quadratic_low_rank_bias = getattr(config, "quadratic_low_rank_bias", False)
        self.quadratic_low_rank_linear = getattr(config, "quadratic_low_rank_linear", False)
        self.lambda_quadratic_low_rank_internal = getattr(config, "lambda_quadratic_low_rank_internal", 0.0)
        self.lambda_quadratic_low_rank_cross = getattr(config, "lambda_quadratic_low_rank_cross", 0.0)
        if self.router_type in {"low_rank", "quadratic", "quadratic_low_rank"}:
            self.router_center_input = True
            self.router_center_mode = "running"
        if self.router_center_mode not in ("batch", "running"):
            raise ValueError(f"Unsupported router_center_mode: {self.router_center_mode}")
        if self.router_center_grad_mode not in ("none", "batch_only"):
            raise ValueError(f"Unsupported router_center_grad_mode: {self.router_center_grad_mode}")
        if self.router_acp_mode not in ("parallel", "orthogonal"):
            raise ValueError(f"Unsupported router_acp_mode: {self.router_acp_mode}")
        if not (0.0 < self.router_center_decay_base <= 1.0):
            raise ValueError(
                f"router_center_decay_base must be in (0, 1], got {self.router_center_decay_base}"
            )
        if self.router_center_decay_scale <= 0:
            raise ValueError(
                f"router_center_decay_scale must be > 0, got {self.router_center_decay_scale}"
            )

        # gating
        if self.router_aux_gate:
            self.aux_gate_linear = nn.Linear(config.hidden_size, config.hidden_size)

        if config.moe_type == "multihead":
            self.routing_input_dim = config.hidden_size // config.moe_head_num
        else:
            self.routing_input_dim = config.hidden_size
        if (
            (self.router_center_input and self.router_center_mode == "running")
            or (self.router_acp_transform and self.router_center_mode == "running")
        ):
            self.register_buffer("router_running_mean", torch.zeros(self.routing_input_dim))
        if self.router_acp_transform:
            self.acp_gate_center = nn.Linear(self.routing_input_dim, config.num_experts, bias=False)
            self.acp_gate_residual = nn.Linear(self.routing_input_dim, config.num_experts, bias=False)

        if self.router_type == "quadratic":
            self.quadratic_router = QuadraticTopKRouter(
                input_dim=self.routing_input_dim,
                num_experts=config.num_experts,
                top_k=self.top_k,
                eps=getattr(config, "quadratic_eps", 1e-6),
            )
        elif self.router_type == "low_rank":
            self.low_rank_router = CenteredLowRankRouter(
                input_dim=self.routing_input_dim,
                num_experts=config.num_experts,
                top_k=self.top_k,
                rank=self.low_rank_rank,
            )
        elif self.router_type == "quadratic_low_rank":
            self.quadratic_low_rank_router = SubspaceEnergyRouter(
                input_dim=self.routing_input_dim,
                num_experts=config.num_experts,
                top_k=self.top_k,
                rank=self.low_rank_rank,
                use_bias=self.quadratic_low_rank_bias,
            )
            if self.quadratic_low_rank_linear:
                self.quadratic_low_rank_linear_gate = nn.Linear(
                    self.routing_input_dim,
                    config.num_experts,
                    bias=False,
                )
        else:
            self.gate = nn.Linear(self.routing_input_dim, config.num_experts, bias=False)
        self.shared_expert = MyQwen3ExpertMLP(config)
        self.experts = nn.ModuleList(
            [MyQwen3ExpertMLP(config) for _ in range(self.num_experts)]
        )

    def _update_running_center(self, gating_reference: torch.Tensor, global_step: Optional[Union[int, torch.Tensor]] = None):
        if not self.training:
            return 0.0
        if self.router_center_mode == "running" and global_step is None:
            raise ValueError("global_step is required when router_center_mode='running'")
        with torch.no_grad():
            x_f = gating_reference.detach().reshape(-1, gating_reference.shape[-1]).float()
            local_count = torch.tensor([x_f.size(0)], device=x_f.device, dtype=torch.float32)
            local_sum = x_f.sum(dim=0)
            if dist.is_initialized() and self.training:
                dist.all_reduce(local_sum, op=dist.ReduceOp.SUM)
                dist.all_reduce(local_count, op=dist.ReduceOp.SUM)
            mean_val = local_sum / local_count.clamp_min(1.0)
        if isinstance(global_step, torch.Tensor):
            if global_step.numel() == 0:
                step_val = 0.0
            else:
                step_val = float(global_step.detach().to(dtype=torch.float32).max().item())
        elif global_step is None:
            step_val = 0.0
        else:
            step_val = float(global_step)
        step_val = max(step_val, 0.0)
        decay_base = min(max(float(self.router_center_decay_base), 0.0), 1.0)
        decay_scale = max(float(self.router_center_decay_scale), 1e-12)
        beta_t = decay_base ** (step_val / decay_scale)
        beta_t = min(max(float(beta_t), 0.0), 1.0)
        with torch.no_grad():
            self.router_running_mean.mul_(1.0 - beta_t).add_(mean_val, alpha=beta_t)
        return beta_t

    def _compute_batch_center(self, gating_reference: torch.Tensor) -> torch.Tensor:
        if gating_reference.dim() == 3:
            return gating_reference.mean(dim=(0, 1), keepdim=True)
        return gating_reference.mean(dim=0, keepdim=True)

    def _center_like_input(self, center_vec: torch.Tensor, gating_reference: torch.Tensor) -> torch.Tensor:
        center_vec = center_vec.to(device=gating_reference.device, dtype=gating_reference.dtype)
        if gating_reference.dim() == 3:
            return center_vec.view(1, 1, -1)
        return center_vec.view(1, -1)

    def _compute_acp_parallel_component(self, gating_reference: torch.Tensor, center_vec: torch.Tensor) -> torch.Tensor:
        center = self._center_like_input(center_vec, gating_reference)
        denom = torch.linalg.vector_norm(center, ord=2, dim=-1, keepdim=True).clamp_min(self.router_acp_eps)
        center_unit = center / denom
        return (gating_reference * center_unit).sum(dim=-1, keepdim=True) * center_unit

    def _compute_acp_input_component(self, gating_reference: torch.Tensor, center_vec: torch.Tensor) -> torch.Tensor:
        x_parallel = self._compute_acp_parallel_component(gating_reference, center_vec)
        if self.router_acp_mode == "parallel":
            return x_parallel
        if self.router_acp_mode == "orthogonal":
            return gating_reference - x_parallel
        raise ValueError(f"Unsupported router_acp_mode: {self.router_acp_mode}")

    def forward(self, hidden_states, gating_reference = None, global_step: Optional[Union[int, torch.Tensor]] = None) -> torch.Tensor:
        if gating_reference is None:
            gating_reference = hidden_states

        running_beta = None
        running_center_vec = getattr(self, "router_running_mean", None)
        center_for_forward_vec = running_center_vec
        if self.router_center_mode == "running" and (
            self.router_center_input or self.router_acp_transform
        ):
            running_beta = self._update_running_center(gating_reference, global_step=global_step)
            running_center_vec = self.router_running_mean
            center_for_forward_vec = running_center_vec
            if self.training and self.router_center_grad_mode == "batch_only":
                batch_center_vec = self._compute_batch_center(gating_reference).reshape(-1)
                center_for_forward_vec = (1.0 - float(running_beta)) * running_center_vec.detach() + float(running_beta) * batch_center_vec

        acp_center_vec = None
        if self.router_acp_transform and self.router_center_mode == "running":
            acp_center_vec = center_for_forward_vec
        elif self.router_acp_transform:
            acp_center_vec = self._compute_batch_center(gating_reference).reshape(-1)

        if self.router_center_input:
            if self.router_center_mode == "running":
                mean_val = self._center_like_input(center_for_forward_vec, gating_reference)
            else:
                mean_val = self._compute_batch_center(gating_reference)
            gating_reference = gating_reference - mean_val

        if self.router_aux_gate:
            gate_val = torch.sigmoid(self.aux_gate_linear(gating_reference))
            gating_reference = gating_reference * gate_val

        shared_expert_output = self.shared_expert(hidden_states)
        
        batch_size, sequence_length, hidden_dim = hidden_states.shape
        batch_size, sequence_length, gating_dim = gating_reference.shape

        hidden_states = hidden_states.view(-1, hidden_dim)
        gating_reference = gating_reference.view(-1, gating_dim)
        if self.router_acp_transform and acp_center_vec is not None and self.router_type != "quadratic_low_rank":
            center_component = self._compute_acp_input_component(gating_reference, acp_center_vec)
            router_logits = self.acp_gate_center(center_component) + self.acp_gate_residual(gating_reference)
            router_logits = router_logits.view(-1, self.num_experts)
            full_routing_probs = F.softmax(router_logits, dim=1, dtype=torch.float)
            routing_probs, selected_experts = torch.topk(full_routing_probs, self.top_k, dim=-1)
        elif self.router_type == "quadratic":
            quadratic_outputs = self.quadratic_router(
                gating_reference.view(batch_size, sequence_length, gating_dim),
                running_beta=running_beta,
            )
            routing_probs, selected_experts, full_routing_probs = quadratic_outputs[:3]
            routing_probs = routing_probs.view(-1, self.top_k)
            selected_experts = selected_experts.view(-1, self.top_k)
            full_routing_probs = full_routing_probs.view(-1, self.num_experts)
        elif self.router_type == "low_rank":
            low_rank_outputs = self.low_rank_router(
                gating_reference.view(batch_size, sequence_length, gating_dim)
            )
            routing_probs, selected_experts, full_routing_probs = low_rank_outputs[:3]
            routing_probs = routing_probs.view(-1, self.top_k)
            selected_experts = selected_experts.view(-1, self.top_k)
            full_routing_probs = full_routing_probs.view(-1, self.num_experts)
        elif self.router_type == "quadratic_low_rank":
            router_logits = self.quadratic_low_rank_router.compute_logits_from_centered(
                gating_reference.view(batch_size, sequence_length, gating_dim)
            )
            if self.quadratic_low_rank_linear:
                router_logits = router_logits + self.quadratic_low_rank_linear_gate(
                    gating_reference.view(batch_size, sequence_length, gating_dim)
                )
            if self.router_acp_transform and acp_center_vec is not None:
                center_component = self._compute_acp_input_component(gating_reference, acp_center_vec)
                acp_logits = self.acp_gate_center(center_component) + self.acp_gate_residual(gating_reference)
                router_logits = router_logits.view(-1, self.num_experts) + acp_logits.view(-1, self.num_experts)
            else:
                router_logits = router_logits.view(-1, self.num_experts)
            full_routing_probs = F.softmax(router_logits, dim=1, dtype=torch.float)
            routing_probs, selected_experts = torch.topk(full_routing_probs, self.top_k, dim=-1)
            routing_probs = routing_probs.view(-1, self.top_k)
            selected_experts = selected_experts.view(-1, self.top_k)
            full_routing_probs = full_routing_probs.view(-1, self.num_experts)
        else:
            router_logits = self.gate(gating_reference)
            full_routing_probs = F.softmax(router_logits, dim=1, dtype=torch.float)
            routing_probs, selected_experts = torch.topk(full_routing_probs, self.top_k, dim=-1)

        if self.norm_topk_prob:  # only diff with mixtral sparse moe block!
            routing_probs /= routing_probs.sum(dim=-1, keepdim=True).clamp_min(1e-9)
        # we cast back to the input dtype
        routing_weights = routing_probs.to(hidden_states.dtype)

        final_hidden_states = torch.zeros(
            (batch_size * sequence_length, gating_dim), dtype=hidden_states.dtype, device=hidden_states.device
        )

        # One hot encode the selected experts to create an expert mask
        # this will be used to easily index which expert is going to be sollicitated
        expert_mask = torch.nn.functional.one_hot(selected_experts, num_classes=self.num_experts).permute(2, 1, 0)

        # Loop over all available experts in the model and perform the computation on each expert
        for expert_idx in range(self.num_experts):
            expert_layer = self.experts[expert_idx]
            idx, top_x = torch.where(expert_mask[expert_idx])

            # Index the correct hidden states and compute the expert hidden state for
            # the current expert. We need to make sure to multiply the output hidden
            # states by `routing_weights` on the corresponding tokens (top-1 and top-2)
            current_state = hidden_states[None, top_x].reshape(-1, hidden_dim)
            current_hidden_states = expert_layer(current_state) * routing_weights[top_x, idx, None]

            # However `index_add_` only support torch tensors for indexing so we'll use
            # the `top_x` tensor here.
            final_hidden_states.index_add_(0, top_x, current_hidden_states.to(hidden_states.dtype))

        final_hidden_states = final_hidden_states.reshape(batch_size, sequence_length, gating_dim) + shared_expert_output

        # Load balancing loss (Switch Transformer style)
        # router_logits: (batch * sequence_length, n_experts)
        # routing_weights: (batch * sequence_length, n_experts) - softmaxed
        # expert_mask: (n_experts, batch * sequence_length) - one-hot selected

        # 1. Expert importance: sum of routing weights for each expert
        # shape: (n_experts,)
        expert_importance = full_routing_probs.sum(dim=0)
        
        # 2. Expert load: count of tokens assigned to each expert
        # shape: (n_experts,)
        # We need to compute this from expert_mask. 
        # expert_mask is (n_experts, batch*seq_len) but with boolean/indices logic in code.
        # Re-computing simple mask for load calculation
        # selected_experts: (batch * sequence_length, top_k)
        
        # Create a full mask for load counting
        # (batch * seq_len, num_experts)
        expert_load_mask = torch.zeros((batch_size * sequence_length, self.num_experts), device=hidden_states.device)
        expert_load_mask.scatter_(1, selected_experts, 1.0)
        expert_load = expert_load_mask.sum(dim=0)

        # 3. Aux Loss = alpha * N * sum(importance * load)
        # N = num_experts
        # Normalize by batch size to keep loss scale independent of batch size?
        # Standard Switch Transformer implementation normalizes by (num_tokens * num_experts) inside, 
        # or just N * sum(P * f) where P and f are probabilities.
        # Let's use the probability formulation:
        
        # P_i = sum(routing_weights_i) / T
        # f_i = sum(expert_load_mask_i) / T
        # loss = N * sum(P_i * f_i)
        
        T = batch_size * sequence_length
        T_load = T * self.top_k
        P = expert_importance / T
        f = expert_load / T_load
        
        lb_loss = self.num_experts * torch.sum(P * f)
        qlr_internal_loss = lb_loss.new_zeros(())
        qlr_cross_loss = lb_loss.new_zeros(())
        if self.router_type == "quadratic_low_rank":
            qlr_internal_loss, qlr_cross_loss = self.quadratic_low_rank_router.compute_regularization_losses()
            qlr_internal_loss = qlr_internal_loss.to(lb_loss.dtype)
            qlr_cross_loss = qlr_cross_loss.to(lb_loss.dtype)

        return final_hidden_states, (selected_experts, lb_loss, qlr_internal_loss, qlr_cross_loss)


class MyQwen3MultiheadMoeBlock(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.num_experts = config.num_experts
        self.top_k = config.num_experts_per_tok
        self.norm_topk_prob = config.norm_topk_prob
        self.head_num = config.moe_head_num
        self.head_size = config.hidden_size // config.moe_head_num

        self.head_moes = nn.ModuleList(
            [MyQwen3SparseMoeBlock(config) for _ in range(self.head_num)]
        )

    def forward(self, hidden_states, gating_reference = None, global_step: Optional[Union[int, torch.Tensor]] = None) -> torch.Tensor:
        if gating_reference is None:
            gating_reference = hidden_states
        
        bs, sequence_length, hidden_dim = hidden_states.shape
        gating_reference = gating_reference.reshape(bs, sequence_length, self.head_num, self.head_size)
        gating_reference = gating_reference.permute(2, 0, 1, 3) # (head_num, bs, seq_len, head_size)
        
        final_output = []
        total_lb_loss = 0
        total_qlr_internal_loss = 0
        total_qlr_cross_loss = 0
        all_selected_experts = []

        for i in range(self.head_num):
            head_output, (selected_experts, lb_loss, qlr_internal_loss, qlr_cross_loss) = self.head_moes[i](
                hidden_states,
                gating_reference=gating_reference[i],
                global_step=global_step,
            )
            final_output.append(head_output)
            total_lb_loss += lb_loss
            total_qlr_internal_loss += qlr_internal_loss
            total_qlr_cross_loss += qlr_cross_loss
            all_selected_experts.append(selected_experts)
        
        final_output = torch.cat(final_output, dim=-1)
        
        # Stack selected experts for return consistency if needed, or just return list
        # Returning stacked tensor might be better if downstream expects tensor
        # But selected_experts shape in sparse block is (batch*seq, top_k)
        # Here we have head_num of them.
        # Let's stack them: (head_num, batch*seq, top_k)
        stacked_experts = torch.stack(all_selected_experts, dim=0)
        
        return final_output, (stacked_experts, total_lb_loss, total_qlr_internal_loss, total_qlr_cross_loss)



def rotate_half(x):
    """Rotates half the hidden dims of the input."""
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_pos_emb(q, k, cos, sin, position_ids=None, unsqueeze_dim=1):
    cos = cos.unsqueeze(unsqueeze_dim)
    sin = sin.unsqueeze(unsqueeze_dim)
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed


def repeat_kv(hidden_states: torch.Tensor, n_rep: int) -> torch.Tensor:
    batch, num_key_value_heads, slen, head_dim = hidden_states.shape
    if n_rep == 1:
        return hidden_states
    hidden_states = hidden_states[:, :, None, :, :].expand(batch, num_key_value_heads, n_rep, slen, head_dim)
    return hidden_states.reshape(batch, num_key_value_heads * n_rep, slen, head_dim)


def eager_attention_forward(
    module: nn.Module,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attention_mask: Optional[torch.Tensor],
    scaling: float,
    dropout: float = 0.0,
    **kwargs,
):
    key_states = repeat_kv(key, module.num_key_value_groups)
    value_states = repeat_kv(value, module.num_key_value_groups)

    attn_weights = torch.matmul(query, key_states.transpose(2, 3)) * scaling
    if attention_mask is not None:
        causal_mask = attention_mask[:, :, :, : key_states.shape[-2]]
        attn_weights = attn_weights + causal_mask

    attn_weights = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query.dtype)
    attn_weights = nn.functional.dropout(attn_weights, p=dropout, training=module.training)
    attn_output = torch.matmul(attn_weights, value_states)
    attn_output = attn_output.transpose(1, 2).contiguous()

    return attn_output, attn_weights


class MyQwen3Attention(nn.Module):
    def __init__(self, config: Qwen3Config, layer_idx: int):
        super().__init__()
        self.config = config
        self.layer_idx = layer_idx
        self.head_dim = getattr(config, "head_dim", config.hidden_size // config.num_attention_heads)
        self.num_key_value_groups = config.num_attention_heads // config.num_key_value_heads
        self.scaling = self.head_dim**-0.5
        self.attention_dropout = config.attention_dropout
        self.is_causal = True

        self.q_proj = nn.Linear(
            config.hidden_size, config.num_attention_heads * self.head_dim, bias=config.attention_bias
        )
        self.k_proj = nn.Linear(
            config.hidden_size, config.num_key_value_heads * self.head_dim, bias=config.attention_bias
        )
        self.v_proj = nn.Linear(
            config.hidden_size, config.num_key_value_heads * self.head_dim, bias=config.attention_bias
        )
        self.o_proj = nn.Linear(
            config.num_attention_heads * self.head_dim, config.hidden_size, bias=config.attention_bias
        )
        self.q_norm = Qwen3RMSNorm(self.head_dim, eps=config.rms_norm_eps)  # unlike olmo, only on the head dim!
        self.k_norm = Qwen3RMSNorm(self.head_dim, eps=config.rms_norm_eps)  # thus post q_norm does not need reshape
        self.sliding_window = config.sliding_window
        if not (
            self.config.use_sliding_window
            and getattr(self.config, "sliding_window", None) is not None
            and self.layer_idx >= self.config.max_window_layers
        ):
            self.sliding_window = None

    def forward(
        self,
        hidden_states: torch.Tensor,
        position_embeddings: Tuple[torch.Tensor, torch.Tensor],
        attention_mask: Optional[torch.Tensor],
        past_key_value: Optional[Cache] = None,
        cache_position: Optional[torch.LongTensor] = None,
        **kwargs: Unpack[FlashAttentionKwargs],
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple[torch.Tensor]]]:
        # print(hidden_states.shape)
        input_shape = hidden_states.shape[:-1]
        hidden_shape = (*input_shape, -1, self.head_dim)
        query_states = self.q_norm(self.q_proj(hidden_states).view(hidden_shape)).transpose(1, 2)
        key_states = self.k_norm(self.k_proj(hidden_states).view(hidden_shape)).transpose(1, 2)
        value_states = self.v_proj(hidden_states).view(hidden_shape).transpose(1, 2)

        cos, sin = position_embeddings
        query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin)

        if past_key_value is not None:
            # sin and cos are specific to RoPE models; cache_position needed for the static cache
            cache_kwargs = {"sin": sin, "cos": cos, "cache_position": cache_position}
            key_states, value_states = past_key_value.update(key_states, value_states, self.layer_idx, cache_kwargs)

        attention_interface: Callable = eager_attention_forward
        if self.config._attn_implementation != "eager":
            if self.config._attn_implementation == "sdpa" and kwargs.get("output_attentions", False):
                pass 
            else:
                attention_interface = ALL_ATTENTION_FUNCTIONS[self.config._attn_implementation]

        attn_output, attn_weights = attention_interface(
            self,
            query_states,
            key_states,
            value_states,
            attention_mask,
            dropout=0.0 if not self.training else self.attention_dropout,
            scaling=self.scaling,
            sliding_window=self.sliding_window,  # diff with Llama
            **kwargs,
        )

        attn_output = attn_output.reshape(*input_shape, -1).contiguous()
        oracle_output = attn_output
        attn_output = self.o_proj(attn_output)
        return attn_output, oracle_output


class MyQwen3DecoderLayer(nn.Module):
    def __init__(self, config: Qwen3Config, layer_idx: int):
        super().__init__()
        print(f"init layer {layer_idx}", end="\r")
        self.layer_idx = layer_idx
        self.hidden_size = config.hidden_size
        self.self_attn = MyQwen3Attention(config=config, layer_idx=layer_idx)
        print(f"init mlp {layer_idx}, moe_type {config.moe_type}")
        if config.moe_type == "moe": # [none, moe, multihead]
            self.mlp = MyQwen3SparseMoeBlock(config)
            self.gating_reference = config.gating_reference
        elif config.moe_type == "multihead":
            self.gating_reference = config.gating_reference
            self.mlp = MyQwen3MultiheadMoeBlock(config)
        elif config.moe_type == "spectral":
            self.mlp = SpectralMoELayer(config)
            self.gating_reference = config.gating_reference
        elif config.moe_type == "none":
            self.mlp = MyQwen3MLP(config)
        else:
            print("moe_type error")
            sys.exit()
        self.moe_type = config.moe_type

        self.input_layernorm = Qwen3RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.post_attention_layernorm = Qwen3RMSNorm(config.hidden_size, eps=config.rms_norm_eps)

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[Cache] = None,
        output_attentions: Optional[bool] = False,
        output_expert_labels: Optional[bool] = False,
        use_cache: Optional[bool] = False,
        cache_position: Optional[torch.LongTensor] = None,
        position_embeddings: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,  # necessary, but kept here for BC
        **kwargs: Unpack[FlashAttentionKwargs],
    ) -> Tuple[torch.FloatTensor, Optional[Tuple[torch.FloatTensor, torch.FloatTensor]]]:
        global_step = kwargs.pop("global_step", None)
        residual = hidden_states

        hidden_states = self.input_layernorm(hidden_states)

        # Self Attention
        attn_output_wo_res, self_attn_weights = self.self_attn(
            hidden_states=hidden_states,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_value=past_key_value,
            output_attentions=output_attentions,
            use_cache=use_cache,
            cache_position=cache_position,
            position_embeddings=position_embeddings,
            **kwargs,
        )
        hidden_states = residual + attn_output_wo_res

        # Fully Connected
        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)
        if self.moe_type in ("moe", "multihead"):
            if self.gating_reference == "oracle":
                hidden_states = self.mlp(hidden_states, attn_output_wo_res, global_step=global_step)
            else:
                hidden_states = self.mlp(hidden_states, global_step=global_step)
        elif self.moe_type != "none" and self.gating_reference == "oracle":
            hidden_states = self.mlp(hidden_states, attn_output_wo_res)
        else: # switch
            hidden_states = self.mlp(hidden_states)

        if isinstance(hidden_states, tuple):
            if self.moe_type == "spectral":
                hidden_states, aux_info = hidden_states
                aux_losses = aux_info
            else:
                hidden_states, moe_aux = hidden_states
                expert_labels = moe_aux[0]
                lb_loss = moe_aux[1]
                qlr_internal_loss = moe_aux[2] if len(moe_aux) > 2 else lb_loss.new_zeros(())
                qlr_cross_loss = moe_aux[3] if len(moe_aux) > 3 else lb_loss.new_zeros(())
                aux_losses = {
                    "lb_loss": lb_loss,
                    "qlr_internal_loss": qlr_internal_loss,
                    "qlr_cross_loss": qlr_cross_loss,
                }
        else:
            aux_losses = None

        hidden_states = residual + hidden_states

        outputs = (hidden_states,)
        if output_attentions:
            outputs += (self_attn_weights,)

        if output_expert_labels:
            if self.moe_type == "spectral":
                # Spectral MoE doesn't output discrete labels in same way, but let's handle if needed
                outputs += (None, ) 
            else:
                outputs += (expert_labels, )
            
        if aux_losses is not None:
            outputs += (aux_losses, )

        return outputs


class Qwen3RotaryEmbedding(nn.Module):
    def __init__(self, config: Qwen3Config, device=None):
        super().__init__()
        # BC: "rope_type" was originally "type"
        if hasattr(config, "rope_scaling") and config.rope_scaling is not None:
            self.rope_type = config.rope_scaling.get("rope_type", config.rope_scaling.get("type"))
        else:
            self.rope_type = "default"
        self.max_seq_len_cached = config.max_position_embeddings
        self.original_max_seq_len = config.max_position_embeddings

        self.config = config
        self.rope_init_fn = ROPE_INIT_FUNCTIONS[self.rope_type]

        inv_freq, self.attention_scaling = self.rope_init_fn(self.config, device)
        self.register_buffer("inv_freq", inv_freq, persistent=False)
        self.original_inv_freq = self.inv_freq

    @torch.no_grad()
    def forward(self, x, position_ids):
        inv_freq_expanded = self.inv_freq[None, :, None].float().expand(position_ids.shape[0], -1, 1).to(x.device)
        position_ids_expanded = position_ids[:, None, :].float()

        device_type = x.device.type if isinstance(x.device.type, str) and x.device.type != "mps" else "cpu"
        with torch.autocast(device_type=device_type, enabled=False):  # Force float32
            freqs = (inv_freq_expanded.float() @ position_ids_expanded.float()).transpose(1, 2)
            emb = torch.cat((freqs, freqs), dim=-1)
            cos = emb.cos() * self.attention_scaling
            sin = emb.sin() * self.attention_scaling

        return cos.to(dtype=x.dtype), sin.to(dtype=x.dtype)


class Qwen3PreTrainedModel(PreTrainedModel):
    config_class = Qwen3Config
    base_model_prefix = "model"
    supports_gradient_checkpointing = True
    _no_split_modules = ["MyQwen3DecoderLayer"]
    _skip_keys_device_placement = ["past_key_values"]
    _supports_flash_attn_2 = True
    _supports_sdpa = True
    _supports_flex_attn = True
    _supports_cache_class = True
    _supports_quantized_cache = True
    _supports_static_cache = True
    _supports_attention_backend = True

    def _init_weights(self, module):
        std = self.config.initializer_range
        if isinstance(module, nn.Linear):
            module.weight.data.normal_(mean=0.0, std=std)
            if module.bias is not None:
                module.bias.data.zero_()
        elif isinstance(module, nn.Embedding):
            module.weight.data.normal_(mean=0.0, std=std)
            if module.padding_idx is not None:
                module.weight.data[module.padding_idx].zero_()


class Qwen3Model(Qwen3PreTrainedModel):
    def __init__(self, config: Qwen3Config):
        super().__init__(config)
        self.padding_idx = config.pad_token_id
        self.vocab_size = config.vocab_size

        self.embed_tokens = nn.Embedding(config.vocab_size, config.hidden_size, self.padding_idx)
        self.layers = nn.ModuleList(
            [MyQwen3DecoderLayer(config, layer_idx) for layer_idx in range(config.num_hidden_layers)]
        )
        self.norm = Qwen3RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.rotary_emb = Qwen3RotaryEmbedding(config=config)
        self.gradient_checkpointing = False

        # Initialize weights and apply final processing
        # self.post_init()

    def get_input_embeddings(self):
        return self.embed_tokens

    def set_input_embeddings(self, value):
        self.embed_tokens = value

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Cache] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_expert_labels:Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        cache_position: Optional[torch.LongTensor] = None,
        **flash_attn_kwargs: Unpack[FlashAttentionKwargs],
    ) -> BaseModelOutputWithPast:
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_expert_labels = output_expert_labels if output_expert_labels is not None else False
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        use_cache = use_cache if use_cache is not None else self.config.use_cache

        if (input_ids is None) ^ (inputs_embeds is not None):
            raise ValueError("You must specify exactly one of input_ids or inputs_embeds")

        if self.gradient_checkpointing and self.training and use_cache:
            # logger.warning_once(
            #     "`use_cache=True` is incompatible with gradient checkpointing. Setting `use_cache=False`."
            # )
            use_cache = False

        # TODO (joao): remove this exception in v4.56 -- it exists for users that try to pass a legacy cache
        if not isinstance(past_key_values, (type(None), Cache)):
            raise ValueError("The `past_key_values` should be either a `Cache` object or `None`.")

        if inputs_embeds is None:
            inputs_embeds = self.embed_tokens(input_ids)

        if use_cache and past_key_values is None:
            past_key_values = DynamicCache()

        if cache_position is None:
            past_seen_tokens = past_key_values.get_seq_length() if past_key_values is not None else 0
            cache_position = torch.arange(
                past_seen_tokens, past_seen_tokens + inputs_embeds.shape[1], device=inputs_embeds.device
            )

        if position_ids is None:
            position_ids = cache_position.unsqueeze(0)

        causal_mask = self._update_causal_mask(
            attention_mask, inputs_embeds, cache_position, past_key_values, output_attentions
        )

        hidden_states = inputs_embeds

        # create position embeddings to be shared across the decoder layers
        position_embeddings = self.rotary_emb(hidden_states, position_ids)

        # decoder layers
        all_hidden_states = () if output_hidden_states else None
        all_self_attns = () if output_attentions else None
        all_expert_labels = () if output_expert_labels else None
        
        # Spectral MoE Aux Loss
        accum_rec_loss = torch.tensor(0.0, device=hidden_states.device, dtype=hidden_states.dtype)
        accum_ortho_loss = torch.tensor(0.0, device=hidden_states.device, dtype=hidden_states.dtype)
        accum_lb_loss = torch.tensor(0.0, device=hidden_states.device, dtype=hidden_states.dtype)
        accum_qlr_internal_loss = torch.tensor(0.0, device=hidden_states.device, dtype=hidden_states.dtype)
        accum_qlr_cross_loss = torch.tensor(0.0, device=hidden_states.device, dtype=hidden_states.dtype)
        accum_expert_counts = None

        for decoder_layer in self.layers[: self.config.num_hidden_layers]:
            if output_hidden_states:
                all_hidden_states += (hidden_states,)

            if self.gradient_checkpointing and self.training:
                layer_outputs = self._gradient_checkpointing_func(
                    partial(decoder_layer.__call__, **flash_attn_kwargs),
                    hidden_states,
                    causal_mask,
                    position_ids,
                    past_key_values,
                    output_attentions,
                    use_cache,
                    cache_position,
                    position_embeddings,
                )
            else:
                layer_outputs = decoder_layer(
                    hidden_states,
                    attention_mask=causal_mask,
                    position_ids=position_ids,
                    past_key_value=past_key_values,
                    output_attentions=output_attentions,
                    output_expert_labels = output_expert_labels,
                    use_cache=use_cache,
                    cache_position=cache_position,
                    position_embeddings=position_embeddings,
                    **flash_attn_kwargs,
                )

            hidden_states = layer_outputs[0]

            if output_attentions:
                all_self_attns += (layer_outputs[1],)
            
            if output_expert_labels:
                # Assuming expert labels are before aux_loss if both present
                idx = 1 + int(output_attentions)
                all_expert_labels += (layer_outputs[idx],)
                
            # Aggregate Aux Loss for all MoE types
            if len(layer_outputs) > 0 and (isinstance(layer_outputs[-1], dict) or isinstance(layer_outputs[-1], torch.Tensor)):
                aux = layer_outputs[-1]
                # Check if it's really aux loss (not attention weights or labels)
                # layer_outputs structure: (hidden_states, [attentions], [expert_labels], [aux_loss])
                # We need to be careful about indexing.
                # Logic in DecoderLayer:
                # returns outputs = (hidden_states,)
                # if output_attentions: outputs += (self_attn_weights,)
                # if output_expert_labels: outputs += (expert_labels,) (or None for spectral)
                # if aux_losses is not None: outputs += (aux_losses,)
                
                # So aux_losses is always the last element IF it exists.
                # But how do we know if it exists?
                # We can check if the last element is a dict or tensor, AND it's not one of the others.
                # Expert labels is tuple or None. Attentions is Tensor (weights).
                # Aux loss is dict or Tensor.
                
                # Safer way: Count expected returns
                expected_len = 1 + int(output_attentions) + int(output_expert_labels)
                if len(layer_outputs) > expected_len:
                    aux = layer_outputs[-1]
                    
                    if isinstance(aux, dict):
                        if 'rec_loss' in aux:
                            accum_rec_loss += aux['rec_loss']
                        if 'ortho_loss' in aux:
                            accum_ortho_loss += aux['ortho_loss']
                        if 'lb_loss' in aux:
                            accum_lb_loss += aux['lb_loss']
                        if 'qlr_internal_loss' in aux:
                            accum_qlr_internal_loss += aux['qlr_internal_loss']
                        if 'qlr_cross_loss' in aux:
                            accum_qlr_cross_loss += aux['qlr_cross_loss']
                        if 'expert_counts' in aux and aux['expert_counts'] is not None:
                            if accum_expert_counts is None:
                                accum_expert_counts = aux['expert_counts']
                            else:
                                accum_expert_counts += aux['expert_counts']
                    elif isinstance(aux, torch.Tensor):
                         # Fallback for old spectral implementation returning single tensor
                        accum_rec_loss += aux

        hidden_states = self.norm(hidden_states)

        # add hidden states from the last decoder layer
        if output_hidden_states:
            all_hidden_states += (hidden_states,)

        output =  BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=past_key_values if use_cache else None,
            hidden_states=all_hidden_states,
            attentions=all_self_attns,
        )
        
        if self.config.moe_type != "none":
            output.aux_loss = {
                'rec_loss': accum_rec_loss,
                'ortho_loss': accum_ortho_loss,
                'lb_loss': accum_lb_loss,
                'qlr_internal_loss': accum_qlr_internal_loss,
                'qlr_cross_loss': accum_qlr_cross_loss,
                'expert_counts': accum_expert_counts
            }


        
        if output_expert_labels:
            output.expert_labels = all_expert_labels

        return output

    def _update_causal_mask(
        self,
        attention_mask: torch.Tensor,
        input_tensor: torch.Tensor,
        cache_position: torch.Tensor,
        past_key_values: Cache,
        output_attentions: bool = False,
    ):
        if self.config._attn_implementation == "flash_attention_2":
            if attention_mask is not None and past_key_values is not None:
                is_padding_right = attention_mask[:, -1].sum().item() != input_tensor.size()[0]
                if is_padding_right:
                    raise ValueError(
                        "You are attempting to perform batched generation with padding_side='right'"
                        " this may lead to unexpected behaviour for Flash Attention version of Qwen3. Make sure to "
                        " call `tokenizer.padding_side  = 'left'` before tokenizing the input. "
                    )
            if attention_mask is not None and 0.0 in attention_mask:
                return attention_mask
            return None

        # For SDPA, when possible, we will rely on its `is_causal` argument instead of its `attn_mask` argument, in
        # order to dispatch on Flash Attention 2. This feature is not compatible with static cache, as SDPA will fail
        # to infer the attention mask.
        past_seen_tokens = past_key_values.get_seq_length() if past_key_values is not None else 0
        using_static_cache = isinstance(past_key_values, StaticCache)
        using_sliding_window_cache = isinstance(past_key_values, SlidingWindowCache)

        # When output attentions is True, sdpa implementation's forward method calls the eager implementation's forward
        if (
            self.config._attn_implementation == "sdpa"
            and not (using_static_cache or using_sliding_window_cache)
            and not output_attentions
        ):
            if AttentionMaskConverter._ignore_causal_mask_sdpa(
                attention_mask,
                inputs_embeds=input_tensor,
                past_key_values_length=past_seen_tokens,
                sliding_window=self.config.sliding_window,
                is_training=self.training,
            ):
                return None

        dtype, device = input_tensor.dtype, input_tensor.device
        min_dtype = torch.finfo(dtype).min
        sequence_length = input_tensor.shape[1]
        # SlidingWindowCache or StaticCache
        if using_sliding_window_cache or using_static_cache:
            target_length = past_key_values.get_max_cache_shape()
        # DynamicCache or no cache
        else:
            target_length = (
                attention_mask.shape[-1]
                if isinstance(attention_mask, torch.Tensor)
                else past_seen_tokens + sequence_length + 1
            )

        # In case the provided `attention` mask is 2D, we generate a causal mask here (4D).
        causal_mask = self._prepare_4d_causal_attention_mask_with_cache_position(
            attention_mask,
            sequence_length=sequence_length,
            target_length=target_length,
            dtype=dtype,
            device=device,
            cache_position=cache_position,
            batch_size=input_tensor.shape[0],
            config=self.config,
            past_key_values=past_key_values,
        )

        if (
            self.config._attn_implementation == "sdpa"
            and attention_mask is not None
            and attention_mask.device.type in ["cuda", "xpu"]
            and not output_attentions
        ):
            # Attend to all tokens in fully masked rows in the causal_mask, for example the relevant first rows when
            # using left padding. This is required by F.scaled_dot_product_attention memory-efficient attention path.
            # Details: https://github.com/pytorch/pytorch/issues/110213
            causal_mask = AttentionMaskConverter._unmask_unattended(causal_mask, min_dtype)

        return causal_mask

    @staticmethod
    def _prepare_4d_causal_attention_mask_with_cache_position(
        attention_mask: torch.Tensor,
        sequence_length: int,
        target_length: int,
        dtype: torch.dtype,
        device: torch.device,
        cache_position: torch.Tensor,
        batch_size: int,
        config: Qwen3Config,
        past_key_values: Cache,
    ):
        """
        Creates a causal 4D mask of shape `(batch_size, 1, query_length, key_value_length)` from a 2D mask of shape
        `(batch_size, key_value_length)`, or if the input `attention_mask` is already 4D, do nothing.

        Args:
            attention_mask (`torch.Tensor`):
                A 2D attention mask of shape `(batch_size, key_value_length)` or a 4D attention mask of shape `(batch_size, 1, query_length, key_value_length)`.
            sequence_length (`int`):
                The sequence length being processed.
            target_length (`int`):
                The target length: when generating with static cache, the mask should be as long as the static cache, to account for the 0 padding, the part of the cache that is not filled yet.
            dtype (`torch.dtype`):
                The dtype to use for the 4D attention mask.
            device (`torch.device`):
                The device to place the 4D attention mask on.
            cache_position (`torch.Tensor`):
                Indices depicting the position of the input sequence tokens in the sequence.
            batch_size (`torch.Tensor`):
                Batch size.
            config (`Qwen3Config`):
                The model's configuration class
            past_key_values (`Cache`):
                The cache class that is being used currently to generate
        """
        if attention_mask is not None and attention_mask.dim() == 4:
            # In this case we assume that the mask comes already in inverted form and requires no inversion or slicing.
            causal_mask = attention_mask
        else:
            min_dtype = torch.finfo(dtype).min
            causal_mask = torch.full(
                (sequence_length, target_length), fill_value=min_dtype, dtype=dtype, device=device
            )
            diagonal_attend_mask = torch.arange(target_length, device=device) > cache_position.reshape(-1, 1)
            if config.sliding_window is not None:
                # if we have sliding window, we should not attend to tokens beyond sliding window length, so we mask them out also
                # the check is needed to verify is current checkpoint was trained with sliding window or not
                if not isinstance(past_key_values, SlidingWindowCache) or sequence_length > target_length:
                    sliding_attend_mask = torch.arange(target_length, device=device) <= (
                        cache_position.reshape(-1, 1) - config.sliding_window
                    )
                    diagonal_attend_mask.bitwise_or_(sliding_attend_mask)
            causal_mask *= diagonal_attend_mask
            causal_mask = causal_mask[None, None, :, :].expand(batch_size, 1, -1, -1)
            if attention_mask is not None:
                causal_mask = causal_mask.clone()  # copy to contiguous memory for in-place edit
                if attention_mask.shape[-1] > target_length:
                    attention_mask = attention_mask[:, :target_length]
                mask_length = attention_mask.shape[-1]
                padding_mask = causal_mask[:, :, :, :mask_length] + attention_mask[:, None, None, :].to(
                    causal_mask.device
                )
                padding_mask = padding_mask == 0
                causal_mask[:, :, :, :mask_length] = causal_mask[:, :, :, :mask_length].masked_fill(
                    padding_mask, min_dtype
                )
        return causal_mask


class KwargsForCausalLM(FlashAttentionKwargs): ...


class MyQwen3ForCausalLM(Qwen3PreTrainedModel, GenerationMixin):
    def __init__(self, config):
        super().__init__(config)
        self.model = Qwen3Model(config)
        self.vocab_size = config.vocab_size
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)

        # Initialize weights and apply final processing
        self.post_init()

    def get_input_embeddings(self):
        return self.model.embed_tokens

    def set_input_embeddings(self, value):
        self.model.embed_tokens = value

    def get_output_embeddings(self):
        return self.lm_head

    def set_output_embeddings(self, new_embeddings):
        self.lm_head = new_embeddings

    def set_decoder(self, decoder):
        self.model = decoder

    def get_decoder(self):
        return self.model

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Cache] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_expert_labels:Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        cache_position: Optional[torch.LongTensor] = None,
        logits_to_keep: Union[int, torch.Tensor] = 0,
        **kwargs: Unpack[KwargsForCausalLM],
    ) -> CausalLMOutputWithPast:
        r"""
            labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
                Labels for computing the masked language modeling loss. Indices should either be in `[0, ...,
                config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored
                (masked), the loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`.

            logits_to_keep (`int` or `torch.Tensor`, *optional*):
                If an `int`, compute logits for the last `logits_to_keep` tokens. If `0`, calculate logits for all
                `input_ids` (special case). Only last token logits are needed for generation, and calculating them only for that
                token can save memory, which becomes pretty significant for long sequences or large vocabulary size.
                If a `torch.Tensor`, must be 1D corresponding to the indices to keep in the sequence length dimension.
                This is useful when using packed tensor format (single dimension for batch and sequence length).

        Returns:

        Example:

        ```python
        >>> from transformers import AutoTokenizer, Qwen3ForCausalLM

        >>> model = Qwen3ForCausalLM.from_pretrained("Qwen/Qwen3-8B")
        >>> tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-8B")

        >>> prompt = "Hey, are you conscious? Can you talk to me?"
        >>> inputs = tokenizer(prompt, return_tensors="pt")

        >>> # Generate
        >>> generate_ids = model.generate(inputs.input_ids, max_length=30)
        >>> tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        "Hey, are you conscious? Can you talk to me?\nI'm not conscious, but I can talk to you."
        ```"""
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )

        # decoder outputs consists of (dec_features, layer_state, dec_hidden, dec_attn)
        outputs: BaseModelOutputWithPast = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_expert_labels = output_expert_labels,
            output_hidden_states=output_hidden_states,
            cache_position=cache_position,
            **kwargs,
        )

        hidden_states = outputs.last_hidden_state
        # Only compute necessary logits, and do not upcast them to float if we are not computing the loss
        slice_indices = slice(-logits_to_keep, None) if isinstance(logits_to_keep, int) else logits_to_keep
        logits = self.lm_head(hidden_states[:, slice_indices, :])

        loss = None
        if labels is not None:
            loss = self.loss_function(logits=logits, labels=labels, vocab_size=self.config.vocab_size, **kwargs)

        output =  CausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states if outputs.hidden_states is not None else outputs.last_hidden_state,
            attentions=outputs.attentions,
        )
        
        if output_expert_labels:
            output.expert_labels = outputs.expert_labels
            
        if hasattr(outputs, "aux_loss"):
            output.aux_loss = outputs.aux_loss
        
        return output
