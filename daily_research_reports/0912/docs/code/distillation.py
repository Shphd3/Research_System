"""Optional coarsened top-k + residual-tail distillation objective.
Same tokenizer, vocabulary IDs, selected causal positions, and temperature required.
Not a full-vocabulary KL; its coarse graining loses within-tail information.
"""
import torch
from torch.nn import functional as F

def coarsened_kl(student_logits,teacher_indices,teacher_top_prob,teacher_tail_prob,temperature=1.0):
    if temperature<=0:raise ValueError("Positive temperature required")
    if student_logits.shape[:-1]!=teacher_indices.shape[:-1] or teacher_indices.shape!=teacher_top_prob.shape:
        raise ValueError("Incompatible cache/logit shapes")
    if teacher_tail_prob.shape!=student_logits.shape[:-1]:raise ValueError("Invalid tail shape")
    if torch.any(teacher_top_prob<0) or torch.any(teacher_tail_prob<0):raise ValueError("Negative probability")
    if not torch.allclose(teacher_top_prob.sum(-1)+teacher_tail_prob,torch.ones_like(teacher_tail_prob),atol=1e-4):
        raise ValueError("Top-k + tail must sum to one at the SAME temperature")
    ids=teacher_indices.sort(-1).values
    if ids.shape[-1]>1 and torch.any(ids[...,1:]==ids[...,:-1]):raise ValueError("Duplicate cached top-k IDs")
    logp=F.log_softmax(student_logits.float()/temperature,dim=-1)
    logtop=logp.gather(-1,teacher_indices)
    # Float64 tail aggregation avoids subtraction catastrophe when top mass~1.
    top_mass=logtop.double().exp().sum(-1)
    logtail=torch.log1p(-top_mass.clamp(max=1-1e-15)).to(logp.dtype)
    q=torch.cat([teacher_top_prob.float(),teacher_tail_prob.float().unsqueeze(-1)],-1)
    l=torch.cat([logtop,logtail.unsqueeze(-1)],-1)
    return (torch.xlogy(q,q)-q*l).sum(-1)*temperature**2
