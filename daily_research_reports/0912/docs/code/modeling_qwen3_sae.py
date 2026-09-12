"""Native PyTorch Qwen3-style dense causal LM + final-normalized-state SAE.

Inspected upstream: transformers v4.57.1, models/qwen3/modeling_qwen3.py.
Research implementation, random initialization only. No upstream numerical-parity
claim; no generation cache, tensor parallelism, FlashAttention package, or trainer.
"""
from dataclasses import dataclass
from pathlib import Path
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.checkpoint import checkpoint
from .configuration_qwen3_sae import Qwen3SAEConfig
from .sae import TopKSAE, SAEOutput

class RMSNorm(nn.Module):
    def __init__(self, dim, eps):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dim))
        self.eps = eps
    def forward(self, x):
        y = x.float()
        y = y * torch.rsqrt(y.square().mean(-1, keepdim=True) + self.eps)
        return y.to(x.dtype) * self.weight.to(x.dtype)

def rotary(x, position_ids, theta):
    dim = x.shape[-1]
    inv = 1.0 / (theta ** (torch.arange(0, dim, 2, device=x.device).float() / dim))
    phase = position_ids.float().unsqueeze(-1) * inv
    phase = torch.cat((phase, phase), dim=-1).unsqueeze(1)
    cos, sin = phase.cos().to(x.dtype), phase.sin().to(x.dtype)
    a, b = x.chunk(2, dim=-1)
    return x * cos + torch.cat((-b, a), dim=-1) * sin

class Attention(nn.Module):
    def __init__(self, c):
        super().__init__()
        self.c = c
        qdim, kdim = c.num_attention_heads*c.head_dim, c.num_key_value_heads*c.head_dim
        self.q = nn.Linear(c.hidden_size, qdim, bias=False)
        self.k = nn.Linear(c.hidden_size, kdim, bias=False)
        self.v = nn.Linear(c.hidden_size, kdim, bias=False)
        self.o = nn.Linear(qdim, c.hidden_size, bias=False)
        self.qnorm = RMSNorm(c.head_dim, c.rms_norm_eps)
        self.knorm = RMSNorm(c.head_dim, c.rms_norm_eps)
    def forward(self, x, positions, allowed):
        b, s, _ = x.shape
        c = self.c
        q = self.qnorm(self.q(x).view(b,s,c.num_attention_heads,c.head_dim)).transpose(1,2)
        k = self.knorm(self.k(x).view(b,s,c.num_key_value_heads,c.head_dim)).transpose(1,2)
        v = self.v(x).view(b,s,c.num_key_value_heads,c.head_dim).transpose(1,2)
        q, k = rotary(q,positions,c.rope_theta), rotary(k,positions,c.rope_theta)
        repeat = c.num_attention_heads // c.num_key_value_heads
        k, v = k.repeat_interleave(repeat,1), v.repeat_interleave(repeat,1)
        y = F.scaled_dot_product_attention(q,k,v,attn_mask=allowed,
                                         is_causal=allowed is None,dropout_p=0.0)
        return self.o(y.transpose(1,2).contiguous().view(b,s,-1))

class Block(nn.Module):
    def __init__(self,c):
        super().__init__()
        self.norm1, self.norm2 = RMSNorm(c.hidden_size,c.rms_norm_eps), RMSNorm(c.hidden_size,c.rms_norm_eps)
        self.attn = Attention(c)
        self.gate = nn.Linear(c.hidden_size,c.intermediate_size,bias=False)
        self.up = nn.Linear(c.hidden_size,c.intermediate_size,bias=False)
        self.down = nn.Linear(c.intermediate_size,c.hidden_size,bias=False)
    def forward(self,x,positions,allowed):
        x = x + self.attn(self.norm1(x),positions,allowed)
        y = self.norm2(x)
        return x + self.down(F.silu(self.gate(y))*self.up(y))

@dataclass
class ModelOutput:
    lm_loss_sum: torch.Tensor | None
    lm_tokens: torch.Tensor
    sae_loss_sum: torch.Tensor | None
    sae_tokens: torch.Tensor
    logits: torch.Tensor | None
    sae: SAEOutput | None
    sampled_flat_indices: torch.Tensor | None

class Qwen3SAEForCausalLM(nn.Module):
    def __init__(self,config: Qwen3SAEConfig):
        super().__init__()
        self.config = config
        self.embed = nn.Embedding(config.vocab_size,config.hidden_size)
        self.blocks = nn.ModuleList([Block(config) for _ in range(config.num_hidden_layers)])
        self.norm = RMSNorm(config.hidden_size,config.rms_norm_eps)
        self.lm_head = None if config.tie_word_embeddings else nn.Linear(config.hidden_size,config.vocab_size,bias=False)
        self.apply(self._init)
        # Initialize the SAE AFTER the LM, so turning the observer on does not
        # change random initial backbone weights for an identical manual_seed.
        self.sae = None if config.sae_mode == "none" else TopKSAE(config.hidden_size,config.sae_width,config.sae_k)
    def _init(self,m):
        if isinstance(m,(nn.Linear,nn.Embedding)):
            nn.init.normal_(m.weight,mean=0,std=self.config.initializer_range)
            if getattr(m,"bias",None) is not None:
                nn.init.zeros_(m.bias)
    @property
    def output_weight(self):
        return self.embed.weight if self.lm_head is None else self.lm_head.weight
    def forward_features(self,input_ids,attention_mask=None,segment_ids=None):
        if input_ids.ndim != 2 or input_ids.dtype != torch.long:
            raise ValueError("input_ids must be int64 [batch, sequence]")
        b,s = input_ids.shape
        if s > self.config.max_position_embeddings:
            raise ValueError("Sequence exceeds configured context")
        valid = torch.ones_like(input_ids,dtype=torch.bool) if attention_mask is None else attention_mask.bool()
        if valid.shape != input_ids.shape:
            raise ValueError("attention_mask has wrong shape")
        positions = (valid.long().cumsum(-1)-1).clamp_min(0)
        allowed = None
        if attention_mask is not None or segment_ids is not None:
            allowed = torch.ones(s,s,device=input_ids.device,dtype=torch.bool).tril()[None,None]
            allowed = allowed & valid[:,None,None,:]
            if segment_ids is not None:
                if segment_ids.shape != input_ids.shape:
                    raise ValueError("segment_ids has wrong shape")
                allowed = allowed & (segment_ids[:,None,:,None] == segment_ids[:,None,None,:])
        x = self.embed(input_ids)
        for block in self.blocks:
            if self.config.gradient_checkpointing and self.training:
                x = checkpoint(block,x,positions,allowed,use_reentrant=False)
            else:
                x = block(x,positions,allowed)
        return x,self.norm(x)
    def _ce(self,h,labels,valid,segment_ids):
        if labels.shape != valid.shape:
            raise ValueError("labels must match input_ids shape; shifting is internal")
        x,y = h[:,:-1].reshape(-1,h.shape[-1]), labels[:,1:].reshape(-1)
        ok = (valid[:,:-1]&valid[:,1:]).reshape(-1) & (y != -100)
        if segment_ids is not None:
            ok = ok & (segment_ids[:,:-1] == segment_ids[:,1:]).reshape(-1)
        x,y = x[ok],y[ok]
        total = h.sum()*0.0
        def chunk_loss(a,w,target):
            return F.cross_entropy(F.linear(a,w).float(),target,reduction="sum")
        for start in range(0,len(y),self.config.ce_chunk_tokens):
            a,t = x[start:start+self.config.ce_chunk_tokens],y[start:start+self.config.ce_chunk_tokens]
            if self.config.checkpoint_ce and self.training and torch.is_grad_enabled():
                loss = checkpoint(chunk_loss,a,self.output_weight,t,use_reentrant=False)
            else:
                loss = chunk_loss(a,self.output_weight,t)
            total = total + loss
        return total,ok.sum()
    def forward(self,input_ids,attention_mask=None,labels=None,sae_mask=None,segment_ids=None,return_logits=False):
        _,h = self.forward_features(input_ids,attention_mask,segment_ids)
        valid = torch.ones_like(input_ids,dtype=torch.bool) if attention_mask is None else attention_mask.bool()
        sae_out,selected = None,None
        routed_h = h
        if self.sae is not None:
            if sae_mask is not None and sae_mask.shape != input_ids.shape:
                raise ValueError("sae_mask has wrong shape")
            mask = valid if sae_mask is None else (valid & sae_mask.bool())
            if self.config.sae_mode == "bottleneck":
                if sae_mask is not None:
                    raise ValueError("bottleneck uses all valid positions, not sampled SAE positions")
                mask = valid
            selected = mask.reshape(-1).nonzero(as_tuple=True)[0]
            x = h.reshape(-1,h.shape[-1])[selected]
            if self.config.sae_mode == "observer":
                x = x.detach()
            sae_out = self.sae(x)
            if self.config.sae_mode == "bottleneck" and self.config.bottleneck_alpha != 0:
                r = h.reshape(-1,h.shape[-1]).clone()
                alpha = self.config.bottleneck_alpha
                r[selected] = (1-alpha)*x + alpha*sae_out.reconstruction
                routed_h = r.view_as(h)
        zero = torch.zeros((),device=input_ids.device,dtype=torch.long)
        lm_loss,lm_tokens = (None,zero) if labels is None else self._ce(routed_h,labels,valid,segment_ids)
        logits = F.linear(routed_h,self.output_weight) if return_logits else None
        return ModelOutput(lm_loss,lm_tokens,None if sae_out is None else sae_out.loss_sum,
                           zero if sae_out is None else sae_out.token_count,logits,sae_out,selected)
    def save_checkpoint(self,path):
        """MODEL-ONLY checkpoint. The eventual trainer must additionally save optimizer,
        scheduler, sampler/cursor, RNG, scaler, tokenizer/data manifests and counters.
        """
        path=Path(path); path.mkdir(parents=True,exist_ok=True)
        self.config.save(path/"config.json")
        torch.save(self.state_dict(),path/"model.pt")
    @classmethod
    def from_checkpoint(cls,path,map_location="cpu"):
        path=Path(path)
        model=cls(Qwen3SAEConfig.load(path/"config.json"))
        model.load_state_dict(torch.load(path/"model.pt",map_location=map_location,weights_only=True))
        return model.to(map_location)

def normalized_objective(output,sae_weight=1.0,world_size=1,lm_global_count=None,sae_global_count=None):
    """For DDP's averaged gradients use world_size * local_sum / global_count.
    Global counts must be ALL-REDUCED over every rank AND accumulated microbatch
    contributing to the optimizer step. Do not average unequal per-rank means.
    """
    terms=[]
    for loss,count,global_count,weight in [
        (output.lm_loss_sum,output.lm_tokens,lm_global_count,1.0),
        (output.sae_loss_sum,output.sae_tokens,sae_global_count,sae_weight)]:
        if loss is not None:
            den=count if global_count is None else torch.as_tensor(global_count,device=count.device)
            if int(den) <= 0:
                raise ValueError("Objective has zero eligible global tokens")
            terms.append(weight*world_size*loss/den)
    if not terms:
        raise ValueError("No losses requested")
    return sum(terms)
