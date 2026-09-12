"""Exact parameter counts on meta device; throughput scenarios are NOT measurements."""
import json
import torch
from model import Qwen3SAEConfig,Qwen3SAEForCausalLM
with torch.device("meta"):
    m=Qwen3SAEForCausalLM(Qwen3SAEConfig())
sae=sum(p.numel() for p in m.sae.parameters());total=sum(p.numel() for p in m.parameters())
print(json.dumps({"backbone_parameters":total-sae,"sae_parameters":sae,"total_parameters":total,
                  "scenario_hours_for_20B":{str(q):20e9/q/3600 for q in [80000,150000,250000,350000]},
                  "note":"Throughputs are hypothetical aggregate valid LM tokens/sec over all four GPUs."},indent=2))
