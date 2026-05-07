import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.distributed as dist
from .modules import MyQwen3ExpertMLP

# 尝试导入 deepspeed，如果环境没有安装则忽略（但在训练脚本中是必须的）
try:
    import deepspeed
except Exception:
    deepspeed = None

class SpikeProjector(nn.Module):
    def __init__(self, hidden_dim, rank, ortho_interval=10, ortho_mode="qr", oja_lr=1e-3):
        super().__init__()
        self.step_counter = 0
        self.ortho_interval = ortho_interval
        self.ortho_mode = ortho_mode
        self.oja_lr = oja_lr
        self.hidden_dim = hidden_dim
        self.rank_dim = rank
        
        if self.ortho_mode == "geoopt":
            import geoopt
            manifold = geoopt.manifolds.Stiefel()
            self.U_s = geoopt.ManifoldParameter(torch.empty(hidden_dim, rank), manifold=manifold)
        else:
            self.U_s = nn.Parameter(torch.empty(hidden_dim, rank))
        
        # 初始化为正交矩阵
        nn.init.orthogonal_(self.U_s)
        
        # Oja 模式下，U_s 不参与梯度下降，而是手动更新
        if self.ortho_mode == "oja":
            self.U_s.requires_grad = False
        
    def reorthogonalize(self):
        """
        执行 QR 分解进行重正交化。
        关键修复：
        1. 仅在 Rank 0 上计算 QR，避免不同 GPU 产生符号翻转 (v vs -v)。
        2. 使用 Broadcast 强制所有 Rank 同步。
        3. 兼容 DeepSpeed ZeRO-3。
        """
        # 如果没有初始化分布式，退回单机模式
        if not dist.is_initialized():
            with torch.no_grad():
                U_matrix = self.U_s.data.float()
                Q, _ = torch.linalg.qr(U_matrix)
                self.U_s.data.copy_(Q.to(self.U_s.dtype))
            return

        # ZeRO-3 兼容上下文：确保参数在当前 GPU 完整可用
        # 如果 deepspeed 未导入，假设不是 ZeRO 环境
        ctx = deepspeed.zero.GatheredParameters(self.U_s, modifier_rank=None) if deepspeed else torch.no_grad()
        
        with ctx:
            with torch.no_grad():
                rank = dist.get_rank()
                
                # 容器准备
                if rank == 0:
                    U_matrix = self.U_s.data.float()
                    Q, _ = torch.linalg.qr(U_matrix)
                    Q_broadcast = Q.to(self.U_s.device).contiguous()
                else:
                    # 占位符，shape 必须正确
                    Q_broadcast = torch.empty(
                        (self.hidden_dim, self.rank_dim), 
                        device=self.U_s.device, 
                        dtype=torch.float32
                    ).contiguous()

                # 广播：所有人都听 Rank 0 的
                dist.broadcast(Q_broadcast, src=0)
                
                # 写入
                self.U_s.data.copy_(Q_broadcast.to(self.U_s.dtype))

    def _oja_update(self, x):
        """
        分布式安全的 Subspace Oja's Rule 更新。
        解决 Micro-batch 噪声和多卡不同步问题。
        """
        # 0. Safety Check: Never update in eval mode
        if not self.training:
            return

        # 1. 基础准备
        x_detached = x.detach()
        # Oja 必须使用 FP32 以避免数值下溢
        x_f32 = x_detached.float()
        U_f32 = self.U_s.data.float() # 使用 .data 避免计算图追踪
        
        batch_size_local = x_f32.shape[0]
        
        # 2. 计算本地统计量
        # y = x @ U  [B, K]
        y = torch.matmul(x_f32, U_f32)
        
        # term1 = x.T @ y  [D, K] (Hebbian Term)
        term1 = torch.matmul(x_f32.T, y)
        
        # term2_inner = y.T @ y [K, K]
        term2_inner = torch.matmul(y.T, y)
        
        # 3. 分布式同步 (CRITICAL FIX)
        # 将所有 GPU 的 term1 和 term2_inner 累加，模拟 Global Batch
        if dist.is_initialized():
            # 确保张量连续，避免 NCCL 报错
            term1 = term1.contiguous()
            term2_inner = term2_inner.contiguous()
            
            # 异步 reduce 提高效率
            handles = []
            handles.append(dist.all_reduce(term1, op=dist.ReduceOp.SUM, async_op=True))
            handles.append(dist.all_reduce(term2_inner, op=dist.ReduceOp.SUM, async_op=True))
            
            # 统计全局 batch size
            total_batch_tensor = torch.tensor([batch_size_local], device=x.device, dtype=torch.float32)
            handles.append(dist.all_reduce(total_batch_tensor, op=dist.ReduceOp.SUM, async_op=True))
            
            for h in handles:
                h.wait()
                
            global_batch_size = total_batch_tensor.item()
        else:
            global_batch_size = batch_size_local

        # 4. 计算最终 Delta
        # term2 = U @ (Sum(y.T @ y)) [D, K]
        # 注意：这里是用同步后的 term2_inner
        term2 = torch.matmul(U_f32, term2_inner)
        
        # Oja Rule: delta = lr * (term1 - term2) / N
        # 除以 global_batch_size 是为了让 lr 对 Batch Size 不敏感
        delta = self.oja_lr * (term1 - term2) / max(1.0, global_batch_size)
        
        # 5. 更新参数
        self.U_s.data.add_(delta.to(self.U_s.dtype))

    def forward(self, x):
        # x: (batch * seq_len, hidden_dim)
        
        ortho_loss = torch.tensor(0.0, device=x.device, dtype=x.dtype)
        rec_loss = torch.tensor(0.0, device=x.device, dtype=x.dtype)

        # === 训练阶段更新逻辑 ===
        if self.training:
            self.step_counter += 1
            
            # 模式 A: Oja Rule
            if self.ortho_mode == "oja":
                # 执行手动更新（不产生梯度）
                self._oja_update(x)
                # Oja 模式下，定期做一次硬性 QR 修正防止数值漂移
                if self.ortho_interval > 0 and self.step_counter % self.ortho_interval == 0:
                    self.reorthogonalize()
                
                # 计算 Ortho Loss 用于日志 (不参与梯度)
                with torch.no_grad():
                    gram = torch.matmul(self.U_s.T, self.U_s) 
                    identity = torch.eye(gram.shape[0], device=gram.device, dtype=gram.dtype)
                    ortho_loss = F.mse_loss(gram, identity)
            
            # 模式 B: QR / Loss (基于梯度的更新)
            elif self.ortho_mode in ["qr", "loss"]:
                # QR 模式：定期硬性投影
                if self.ortho_mode == "qr" and self.ortho_interval > 0 and self.step_counter % self.ortho_interval == 0:
                    self.reorthogonalize()
                
                # Loss 模式：计算软约束损失
                if self.ortho_mode == "loss":
                     # L_ortho = || U^T U - I ||^2
                     # 这里的 U_s 需要梯度
                     gram = torch.matmul(self.U_s.T, self.U_s) 
                     identity = torch.eye(gram.shape[0], device=gram.device, dtype=gram.dtype)
                     ortho_loss = F.mse_loss(gram, identity)

        # === 前向计算 (Track 1: Main Path) ===
        # 准备 U_s
        # 关键修复：在计算用于下游任务的 x_spike 时，必须切断对 U_s 的梯度追踪。
        # 这样 LM Loss 反向传播时，梯度只会传给 x (Backbone)，不会传给 U_s。
        # 符合图中 "在更新LM_loss的时候冻结 V_s" 的要求。
        U_s_detached = self.U_s.detach()

        # 1. 计算投影系数 z = x @ U_detached
        z_main = torch.matmul(x, U_s_detached)
        
        # 2. 计算重建 x_spike = z @ U_detached.T
        # 这个 x_spike 用于后续的 Router 和 Shared Expert，保持与 x 的梯度联系，但切断与 U_s 的联系
        x_spike = torch.matmul(z_main, U_s_detached.T)
        
        # === 损失计算 (Track 2: Loss Path) ===
        if self.training:
            if self.ortho_mode == "oja":
                with torch.no_grad():
                    x_detached = x.detach()
                    z_reco = torch.matmul(x_detached, self.U_s)
                    x_spike_reco = torch.matmul(z_reco, self.U_s.T)
                    rec_loss = F.mse_loss(x_detached, x_spike_reco)
            else:
                x_detached = x.detach()
                z_reco = torch.matmul(x_detached, self.U_s)
                x_spike_reco = torch.matmul(z_reco, self.U_s.T)
                rec_loss = F.mse_loss(x_detached, x_spike_reco)

        if self.ortho_mode == "oja":
            rec_loss = rec_loss.detach()
            ortho_loss = ortho_loss.detach()

        return x_spike, rec_loss, ortho_loss


class SpectralRouter(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.num_experts = config.num_experts
        self.top_k = config.num_experts_per_tok
        self.hidden_dim = config.hidden_size
        self.norm_topk_prob = config.norm_topk_prob
        self.residual_mode = getattr(config, 'residual_mode', 'clean')
        self.gate_norm = getattr(config, 'gate_norm', False)
        
        # 噪声门控线性层
        self.noise_gate_linear = nn.Linear(self.hidden_dim, self.hidden_dim)
        if self.gate_norm or self.residual_mode in ['clean', 'norm']:
            self.gate_layernorm = nn.LayerNorm(self.hidden_dim, eps=getattr(config, 'rms_norm_eps', 1e-6))
        
        # 路由线性层
        self.router_linear = nn.Linear(self.hidden_dim, self.num_experts, bias=False)
        
    def forward(self, x, x_spike):
        # x, x_spike: (batch * seq_len, hidden_dim)
        
        # 1. 带阻滤波器：获取语义残差
        # x_spike 允许梯度回传（如果需要反向优化 shared block），但在 Router 计算中作为输入
        x_residual = x - x_spike
        
        # 2. 噪声门控 (Noise Gating)
        # g = sigmoid(Linear(x_residual))
        gate_val = torch.sigmoid(self.noise_gate_linear(x_residual))
        
        # 3. 准备专家输入与路由输入
        if self.gate_norm:
            x_for_routing = self.gate_layernorm(x_residual) * gate_val
        else:
            x_for_routing = x_residual * gate_val
            
        # 专家输入控制
        if self.residual_mode == 'clean':
            # clean：LayerNorm(x_residual) * Gate
            expert_input = self.gate_layernorm(x_residual) * gate_val
            
        elif self.residual_mode == 'norm':
            # norm：LayerNorm(x_residual)
            expert_input = self.gate_layernorm(x_residual)
            
        elif self.residual_mode == 'raw':
            expert_input = x_residual
            
        elif self.residual_mode == 'full':
            expert_input = x
            
        else:
            # default to raw
            expert_input = x_residual

        # 4. 路由决策 (Routing)
        router_logits = self.router_linear(x_for_routing)
        
        routing_weights = F.softmax(router_logits, dim=1)
        topk_weights, selected_experts = torch.topk(routing_weights, self.top_k, dim=-1)
        
        if self.norm_topk_prob:
            topk_weights /= topk_weights.sum(dim=-1, keepdim=True)
            
        topk_weights = topk_weights.to(x.dtype)
        
        return topk_weights, selected_experts, expert_input, router_logits


class SpectralMoELayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.hidden_dim = config.hidden_size
        self.num_experts = config.num_experts
        self.top_k = config.num_experts_per_tok
        
        # 配置：公共专家的输入选择
        self.common_spike = getattr(config, 'common_spike', True)
        
        # 组件 A：SpikeProjector
        self.projector = SpikeProjector(
            self.hidden_dim, 
            config.spectral_rank,
            ortho_interval=getattr(config, 'ortho_interval', 10),
            ortho_mode=getattr(config, 'ortho_mode', 'qr'),
            oja_lr=getattr(config, 'oja_lr', 1e-3)
        )
        
        # 组件 B：SpectralRouter
        self.router = SpectralRouter(config)
        
        # 组件 C：专家
        # 共享专家（Shared Expert / Spike Expert）
        self.shared_expert = MyQwen3ExpertMLP(config)
        
        # 稀疏专家 (Sparse Experts)
        self.experts = nn.ModuleList([
            MyQwen3ExpertMLP(config) for _ in range(self.num_experts)
        ])
        
    def forward(self, hidden_states, gating_reference=None):
        batch_size, sequence_length, hidden_dim = hidden_states.shape
        hidden_states_flat = hidden_states.reshape(-1, hidden_dim)
        
        # 1. 投影器：提取 x_spike
        x_spike, rec_loss, ortho_loss = self.projector(hidden_states_flat)
        
        # 2. 共享路径：处理通用/高频信息
        if self.common_spike:
            # 仅将 Spike 部分送入 Shared Expert
            shared_input = x_spike.reshape(batch_size, sequence_length, hidden_dim)
            shared_output = self.shared_expert(shared_input)
        else:
            # 将原始输入送入 Shared Expert
            shared_output = self.shared_expert(hidden_states)
        
        # 3. 路由器：基于残差进行决策
        routing_weights, selected_experts, expert_input_flat, router_logits = self.router(hidden_states_flat, x_spike)
        
        # 4. 稀疏专家路径
        final_hidden_states = torch.zeros(
            (batch_size * sequence_length, hidden_dim), 
            dtype=hidden_states.dtype, 
            device=hidden_states.device
        )
        
        expert_mask = F.one_hot(selected_experts, num_classes=self.num_experts).permute(2, 1, 0)
        expert_counts = expert_mask.sum(dim=(1, 2)) # 用于日志
        
        for expert_idx in range(self.num_experts):
            expert_layer = self.experts[expert_idx]
            idx, top_x = torch.where(expert_mask[expert_idx])
            
            if top_x.shape[0] == 0:
                continue

            # 专家输入已经由 Router 准备好（可能是 clean/norm/residual）
            current_state = expert_input_flat[top_x]
            
            # 计算输出并加权
            current_hidden_states = expert_layer(current_state) * routing_weights[top_x, idx, None]
            
            # 累加到最终结果
            final_hidden_states.index_add_(0, top_x, current_hidden_states.to(hidden_states.dtype))
            
        final_hidden_states = final_hidden_states.reshape(batch_size, sequence_length, hidden_dim)
        
        # 5. 最终求和
        total_output = final_hidden_states + shared_output
        
        # 辅助信息打包
        aux_info = {
            'rec_loss': rec_loss,
            'ortho_loss': ortho_loss,
            'expert_counts': expert_counts,
            'router_logits': router_logits
        }
                
        return total_output, aux_info
