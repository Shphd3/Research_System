"""Bounded native hook capture. CLI gate prevents heldout access before selection freeze."""
from common import *
import sys, importlib.util, time
import numpy as np
import torch
import torch.nn.functional as F
import transformers.utils as hfu, transformers.utils.import_utils as hfi
for m in [hfu,hfi]:
 for n in ['is_flash_attn_2_available','is_flash_attn_3_available','is_torchvision_available','is_librosa_available']: setattr(m,n,lambda:False)
from transformers import AutoModelForCausalLM

stage=sys.argv[1];assert stage in ['exploration','heldout_check']
assert not (R/f'cache/{stage}.npz').exists(),'No overwrite / no completed-run repeat'
plan=json.load(open(R/'frozen_plan.json')); plan_sha=sha(R/'frozen_plan.json')
for n,d in plan['data_SHA256'].items(): assert sha(R/'data'/n)==d
if stage=='heldout_check':
 freeze=json.load(open(R/'evidence/candidates_frozen_before_heldout.json'))
 assert freeze['selection_SHA256']==sha(R/'results/selection.json')
 for n,d in freeze['code_SHA256'].items(): assert sha(R/'code'/n)==d
else: assert not (R/'evidence/candidates_frozen_before_heldout.json').exists()
for p,d in plan['input_SHA256'].items(): assert sha(p)==d
start=time.time();torch.set_num_threads(2);torch.set_num_interop_threads(1);torch.manual_seed(20261103)
model=AutoModelForCausalLM.from_pretrained(plan['model'],torch_dtype=torch.float32,local_files_only=True,attn_implementation='sdpa').cpu().eval().requires_grad_(False)
model.config.use_cache=False
assert not any(m._forward_hooks or m._forward_pre_hooks for m in model.modules())
saes={};norms={};identity={}
for site,ss in plan['sites'].items():
 assert sha(ss['path'])==ss['sha256'] and sha(ss['loader'])==ss['loader_sha256']
 spec=importlib.util.spec_from_file_location('s03_native_'+site,ss['loader']); mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
 sae=mod.TopKSAE.from_pretrained(ss['path'],map_location='cpu').eval().requires_grad_(False)
 assert (sae.d_model,sae.n_latents,sae.k)==(1024,30000,32)
 assert not any(p.requires_grad for p in sae.parameters())
 saes[site]=sae;norms[site]=sae.decoder.weight.detach().norm(dim=0).numpy()
 identity[site]=dict(**ss,decoder_norm_min=float(norms[site].min()),decoder_norm_max=float(norms[site].max()),native_loader_used=True)
assert not any(p.requires_grad for p in model.parameters())
panel=[p for p in rows(R/'data/panel.jsonl') if p['split']==stage]; acc={s:{k:[] for k in ['h','z','pre','cutoff32','cutoff33','reconstruction_relative_L2']} for s in SITES}; checks=[]

@torch.inference_mode()
def forward(batch,capture=True):
 xx=torch.zeros((4,192),dtype=torch.long);mask=torch.zeros_like(xx);pos=[]
 for j,p in enumerate(batch):
  ids=p['token_ids'];xx[j,:len(ids)]=torch.tensor(ids);mask[j,:len(ids)]=1;pos.append(len(ids)-1)
 assert len(batch)==4
 ii=torch.arange(4);pp=torch.tensor(pos);caps={};hooks=[]
 def grab(k,v): caps[k]=v[ii,pp].detach().clone()
 if capture:
  hooks.append(model.model.layers[27].self_attn.o_proj.register_forward_hook(lambda m,a,y:grab('ATTN_SAE',y)))
  hooks.append(model.model.layers[27].mlp.register_forward_pre_hook(lambda m,a:grab('MLPIN_SAE',a[0])))
 try: output=model.model(input_ids=xx,attention_mask=mask,use_cache=False,return_dict=True).last_hidden_state[ii,pp]
 finally:
  for h in hooks:h.remove()
 return caps, output

for lo in range(0,len(panel),4):
 batch=panel[lo:lo+4];caps,native=forward(batch)
 if lo==0:
  _,plain=forward(batch,capture=False)
  delta=float((plain-native).abs().max());assert delta==0,'Hooks must not mutate native forward'
  checks.append(dict(noop_native_state_max_difference=delta))
 for site,sae in saes.items():
  with torch.inference_mode():
   h=caps[site];values,ids,z,pre=sae.encode_topk(h)
   positive=F.linear(h,sae.encoder.weight,sae.encoder.bias).relu();v,j=positive.topk(32,dim=-1,sorted=False);ref=torch.zeros_like(positive).scatter(-1,j,v)
   assert torch.equal(z,ref),'Native rule equivalence'
   cut=positive.topk(33,dim=-1,sorted=True).values
   rec=sae.decoder(z);res=h-rec;assert (rec+res-h).abs().max()<1e-4
   rel=(res.norm(dim=1)/h.norm(dim=1)).numpy()
   assert torch.isfinite(z).all() and torch.isfinite(pre).all() and bool((z>=0).all())
   assert bool(((z>0).sum(-1)<=32).all())
   for key,arr in dict(h=h.numpy(),z=z.numpy(),pre=pre.numpy(),cutoff32=cut[:,31].numpy(),cutoff33=cut[:,32].numpy(),reconstruction_relative_L2=rel).items(): acc[site][key].append(arr)
 print('CAPTURE',stage,lo+4,'/12',round(time.time()-start,2),'sec',flush=True)
payload={'ids':np.array([p['id'] for p in panel])}
for site,dd in acc.items():
 payload.update({site+'__'+k:np.concatenate(v) for k,v in dd.items()});payload[site+'__decoder_norm']=norms[site]
np.savez_compressed(R/f'cache/{stage}.npz',**payload)
assert sha(R/'frozen_plan.json')==plan_sha
for p,d in json.load(open(R/'evidence/old_steps_immutable_before.json')).items():assert sha(p)==d
dump(R/f'evidence/capture_{stage}.json',dict(UTC=now(),status='COMPLETED_BOUNDED_CAPTURE',stage=stage,rows=len(panel),physical_shape=[4,192],sampling='last visible prefix token, not any answer token',device='cpu',torch=torch.__version__,threads=2,model_trainable_parameters=0,SAE_trainable_parameters=0,GPU_jobs=0,training=0,CC_loaded=False,extra_native_noop_calls=1,native_encoding_equivalence=True,hook_noop_checks=checks,elapsed_seconds=time.time()-start,cache_sha256=sha(R/f'cache/{stage}.npz'),plan_sha256=plan_sha,input_model_SHA256=plan['input_SHA256'],SAE_identity=identity,selection_sha256=sha(R/'results/selection.json') if stage=='heldout_check' else None))
