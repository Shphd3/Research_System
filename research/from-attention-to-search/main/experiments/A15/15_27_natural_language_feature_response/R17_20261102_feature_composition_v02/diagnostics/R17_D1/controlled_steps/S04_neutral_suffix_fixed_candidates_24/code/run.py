"""S04 only: 24 neutral-suffix captures and fixed complete-candidate native scores."""
from common import *
import sys,importlib.util,time,math
import numpy as np
import torch
import torch.nn.functional as F
import transformers.utils as hfu,transformers.utils.import_utils as hfi
for m in [hfu,hfi]:
 for n in ['is_flash_attn_2_available','is_flash_attn_3_available','is_torchvision_available','is_librosa_available']:setattr(m,n,lambda:False)
from transformers import AutoModelForCausalLM
assert not (R/'cache/new.npz').exists() and not (R/'results/behavior_raw.jsonl').exists(),'No overwrite/repeat'
plan=json.load(open(R/'frozen_plan.json'));plan_sha=sha(R/'frozen_plan.json')
for n,h in plan['data_SHA256'].items():assert sha(R/'data'/n)==h
for p,h in plan['input_SHA256'].items():assert sha(p)==h
assert sha(OLD/'results/selection.json')==plan['selection_SHA256']
start=time.time();torch.set_num_threads(2);torch.set_num_interop_threads(1);torch.manual_seed(20261103)
model=AutoModelForCausalLM.from_pretrained(plan['model'],torch_dtype=torch.float32,local_files_only=True,attn_implementation='sdpa').cpu().eval().requires_grad_(False);model.config.use_cache=False
assert not any(m._forward_hooks or m._forward_pre_hooks for m in model.modules())
saes={};norms={};identities={}
for site,ss in plan['sites'].items():
 assert sha(ss['path'])==ss['sha256'] and sha(ss['loader'])==ss['loader_sha256']
 spec=importlib.util.spec_from_file_location('s04_native_'+site,ss['loader']);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
 sae=mod.TopKSAE.from_pretrained(ss['path'],map_location='cpu').eval().requires_grad_(False);assert (sae.d_model,sae.n_latents,sae.k)==(1024,30000,32)
 assert not any(p.requires_grad for p in sae.parameters());saes[site]=sae;norms[site]=sae.decoder.weight.detach().norm(dim=0).numpy()
 identities[site]=dict(**ss,native_loader_used=True,decoder_norm_min=float(norms[site].min()),decoder_norm_max=float(norms[site].max()))
assert not any(p.requires_grad for p in model.parameters())
panel=rows(R/'data/panel.jsonl');store={s:{k:[] for k in ['h','z','pre','topk_indices','cutoff32','cutoff33','reconstruction_relative_L2']} for s in SITES};checks=[]
dump(R/'evidence/started.json',dict(UTC=now(),plan_sha256=plan_sha,selection_sha256=plan['selection_SHA256'],run_code_sha256=sha(__file__),device='cpu',capture_rows=24,behavior_rows=24))
@torch.inference_mode()
def capture(batch,hooks_enabled=True):
 xx=torch.zeros((4,192),dtype=torch.long);mask=torch.zeros_like(xx);ii=torch.arange(4);pp=torch.tensor([len(p['token_ids'])-1 for p in batch]);caps={};hooks=[]
 for j,p in enumerate(batch):xx[j,:len(p['token_ids'])]=torch.tensor(p['token_ids']);mask[j,:len(p['token_ids'])]=1
 def grab(k,v):caps[k]=v[ii,pp].detach().clone()
 if hooks_enabled:
  hooks.append(model.model.layers[27].self_attn.o_proj.register_forward_hook(lambda m,a,y:grab('ATTN_SAE',y)))
  hooks.append(model.model.layers[27].mlp.register_forward_pre_hook(lambda m,a:grab('MLPIN_SAE',a[0])))
 try:out=model.model(input_ids=xx,attention_mask=mask,use_cache=False,return_dict=True).last_hidden_state[ii,pp]
 finally:
  for hook in hooks:hook.remove()
 return caps,out
for lo in range(0,24,4):
 batch=panel[lo:lo+4];caps,native=capture(batch)
 if lo==0:
  _,plain=capture(batch,False);diff=float((plain-native).abs().max());assert diff==0;checks.append(dict(noop_native_state_max_difference=diff))
 for site,sae in saes.items():
  with torch.inference_mode():
   h=caps[site];values,ids,z,pre=sae.encode_topk(h);positive=F.linear(h,sae.encoder.weight,sae.encoder.bias).relu();v,j=positive.topk(32,dim=-1,sorted=False);ref=torch.zeros_like(positive).scatter(-1,j,v);assert torch.equal(z,ref)
   cut=positive.topk(33,dim=-1,sorted=True).values;rec=sae.decoder(z);res=h-rec;assert (rec+res-h).abs().max()<1e-4;assert torch.isfinite(z).all() and torch.isfinite(pre).all()
   dd=dict(h=h.numpy(),z=z.numpy(),pre=pre.numpy(),topk_indices=ids.numpy(),cutoff32=cut[:,31].numpy(),cutoff33=cut[:,32].numpy(),reconstruction_relative_L2=(res.norm(dim=1)/h.norm(dim=1)).numpy())
   for k,v in dd.items():store[site][k].append(v)
 print('CAPTURE',lo+4,'/24',round(time.time()-start,2),'sec',flush=True)
payload={'ids':np.array([p['id'] for p in panel])}
for site,dd in store.items():
 payload.update({site+'__'+k:np.concatenate(v) for k,v in dd.items()});payload[site+'__decoder_norm']=norms[site]
np.savez_compressed(R/'cache/new.npz',**payload)
assert not any(m._forward_hooks or m._forward_pre_hooks for m in model.modules()),'No SAE hooks during native behavior scores'
dups=[]
@torch.inference_mode()
def score(p):
 pre=p['token_ids'];cs=p['candidates'];xx=torch.zeros((4,192),dtype=torch.long);mask=torch.zeros_like(xx)
 for j,c in enumerate(cs+cs):
  ids=c['full_input_token_ids'];assert ids[:len(pre)]==pre;xx[j,:len(ids)]=torch.tensor(ids);mask[j,:len(ids)]=1
 states=model.model(input_ids=xx,attention_mask=mask,use_cache=False,return_dict=True).last_hidden_state;out=[]
 for j,c in enumerate(cs+cs):
  targets=c['token_ids'];lp=model.lm_head(states[j,len(pre)-1:len(pre)+len(targets)-1]).float().log_softmax(-1).gather(1,torch.tensor(targets).view(-1,1)).squeeze(1)
  assert torch.isfinite(lp).all() and bool((lp<=0).all());vv=lp.tolist();total=float(lp.double().sum());assert abs(math.fsum(vv)-total)<1e-10
  out.append(dict(label=c['label'],text=c['text'],candidate_token_ids=targets,candidate_token_pieces=c['token_pieces'],token_count=len(targets),token_logprobs=vv,total_logprob=total))
 for j in range(2):dups.append(abs(out[j]['total_logprob']-out[j+2]['total_logprob']));assert dups[-1]<1e-6
 out=out[:2];choice=max(out,key=lambda c:c['total_logprob'])['label'];gold=p['behavior_gold'];delta=out[0]['total_logprob']-out[1]['total_logprob']
 return dict(id=p['id'],source_id=p['source_id'],family=p['family'],split=p['split'],condition=p['condition'],text=p['text'],prefix=p['prefix'],prefix_token_ids=pre,labels=p['labels'],gold=gold,candidates=out,delta_cat_minus_dog=delta,choice=choice,correct=None if gold is None else gold==choice,exact_tie=delta==0)
with (R/'results/behavior_raw.jsonl').open('x') as f:
 for j,p in enumerate(panel,1):
  f.write(json.dumps(score(p),ensure_ascii=False)+'\n');f.flush()
  if j%4==0:print('BEHAVIOR',j,'/24',round(time.time()-start,2),'sec',flush=True)
assert sha(R/'frozen_plan.json')==plan_sha
for n,h in plan['data_SHA256'].items():assert sha(R/'data'/n)==h
for p,h in json.load(open(R/'evidence/old_immutable_before.json')).items():assert sha(p)==h
dump(R/'evidence/run_complete.json',dict(UTC=now(),status='COMPLETED_BOUNDED_S04_CAPTURE_AND_BEHAVIOR',elapsed_seconds=time.time()-start,device='cpu',threads=2,torch=torch.__version__,physical_shape=[4,192],new_prefixes=24,candidate_sequences=48,extra_hook_noop_calls=1,native_encoding_equivalence=True,hook_noop_checks=checks,max_duplicate_lane_difference=max(dups),model_trainable_parameters=0,SAE_trainable_parameters=0,CC_loaded=False,probe=0,training=0,intervention=0,selection_changed=False,old_S02_S03_unchanged=True,model_input_SHA256=plan['input_SHA256'],SAE_identity=identities,plan_sha256=plan_sha,selection_sha256=plan['selection_SHA256'],cache_sha256=sha(R/'cache/new.npz'),behavior_sha256=sha(R/'results/behavior_raw.jsonl'),next_experiment='NOT_RUN'))
print('S04_RUN_COMPLETE',round(time.time()-start,2),flush=True)
