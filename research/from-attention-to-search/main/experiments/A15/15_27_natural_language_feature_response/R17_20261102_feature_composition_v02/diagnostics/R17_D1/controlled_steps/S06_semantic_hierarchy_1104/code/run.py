"""CPU native behavior and prefix-position capture, with a hard discovery freeze gate."""
from common import *
import sys,importlib.util,time,math,os
import numpy as np
import torch
import torch.nn.functional as F
import transformers.utils as hfu,transformers.utils.import_utils as hfi
for m in [hfu,hfi]:
 for n in ['is_flash_attn_2_available','is_flash_attn_3_available','is_torchvision_available','is_librosa_available']:setattr(m,n,lambda:False)
from transformers import AutoModelForCausalLM
stage=sys.argv[1];assert stage in ['discovery','remaining']
dest=R/f'cache/{stage}.npz';assert not dest.exists()
plan=json.load(open(R/'frozen_plan.json'));allp=rows(R/'data/panel.jsonl')
if stage=='remaining':assert (R/'evidence/candidates_frozen.json').exists()
pp=[p for p in allp if (p['split']=='discovery' and p['wording']=='explicit')==(stage=='discovery')]
for f,h in json.load(open(R/'evidence/protocol_freeze.json'))['hashes'].items():assert sha(f)==h
for f,h in plan['input_SHA256'].items():assert sha(f)==h
torch.set_num_threads(2);torch.set_num_interop_threads(1);torch.manual_seed(plan['seed']);start=time.time()
model=AutoModelForCausalLM.from_pretrained(plan['model'],torch_dtype=torch.float32,local_files_only=True,attn_implementation='sdpa').cpu().eval().requires_grad_(False);model.config.use_cache=False
saes={};dn={}
for site,ss in plan['sites'].items():
 assert sha(ss['path'])==ss['sha256'] and sha(ss['loader'])==ss['loader_sha256']
 spec=importlib.util.spec_from_file_location('s06_native_'+site,ss['loader']);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
 sae=mod.TopKSAE.from_pretrained(ss['path'],map_location='cpu').eval().requires_grad_(False)
 assert (sae.d_model,sae.n_latents,sae.k)==(1024,30000,32);saes[site]=sae;dn[site]=sae.decoder.weight.detach().norm(dim=0).numpy()
assert not any(p.requires_grad for p in model.parameters())
out={s:{k:[] for k in ['h','z','pre','topk_indices','cutoff32','cutoff33','reconstruction_relative_L2']} for s in SITES}
checks=[];lane_max=0
dump(R/f'evidence/{stage}_started.json',dict(UTC=now(),rows=len(pp),device='CPU',shape=plan['shape'],code_sha256=sha(__file__),plan_sha256=sha(R/'frozen_plan.json'),pid=os.getpid()))
@torch.inference_mode()
def forward(p,capture=True,prefixonly=False):
 xx=torch.zeros(4,128,dtype=torch.long);mask=torch.zeros_like(xx);n=len(p['token_ids']);cap={};hooks=[]
 for j,c in enumerate(p['candidates']):
  ids=p['token_ids'] if prefixonly else c['full_ids'];xx[j,:len(ids)]=torch.tensor(ids);mask[j,:len(ids)]=1
 def grab(s,y):cap[s]=y[:,n-1].detach().clone()
 if capture:
  hooks=[model.model.layers[27].self_attn.o_proj.register_forward_hook(lambda m,a,y:grab('ATTN_SAE',y)),model.model.layers[27].mlp.register_forward_pre_hook(lambda m,a:grab('MLPIN_SAE',a[0]))]
 try:hh=model.model(input_ids=xx,attention_mask=mask,use_cache=False,return_dict=True).last_hidden_state
 finally:
  for h in hooks:h.remove()
 return cap,hh
with (R/f'results/behavior_{stage}.jsonl').open('x') as f:
 for j,p in enumerate(pp):
  caps,hh=forward(p)
  if j==0:
   pc,ph=forward(p,prefixonly=True);_,nh=forward(p,capture=False)
   cc=dict(id=p['id'],noop=float((hh-nh).abs().max()),prefixonly={s:float((caps[s]-pc[s]).abs().max()) for s in SITES})
   assert cc['noop']==0 and max(cc['prefixonly'].values())<1e-4;checks.append(cc)
  for s,sae in saes.items():
   lane=float((caps[s]-caps[s][:1]).abs().max());lane_max=max(lane_max,lane);assert lane<1e-4
   with torch.inference_mode():
    h=caps[s][:1];vals,ids,z,pre=sae.encode_topk(h);pos=F.linear(h,sae.encoder.weight,sae.encoder.bias).relu();v,k=pos.topk(32,sorted=False);ref=torch.zeros_like(pos).scatter(-1,k,v);assert torch.equal(ref,z)
    cut=pos.topk(33,sorted=True).values;rec=sae.decoder(z);res=h-rec;assert float((rec+res-h).abs().max())<1e-4
    dd=dict(h=h.numpy(),z=z.numpy(),pre=pre.numpy(),topk_indices=ids.numpy(),cutoff32=cut[:,31].numpy(),cutoff33=cut[:,32].numpy(),reconstruction_relative_L2=(res.norm(dim=1)/h.norm(dim=1)).numpy())
    for key,a in dd.items():assert np.isfinite(a).all();out[s][key].append(a)
  scores=[]
  with torch.inference_mode():
   for ci,c in enumerate(p['candidates']):
    n=len(p['token_ids']);t=c['token_ids'];lp=model.lm_head(hh[ci,n-1:n+len(t)-1]).float().log_softmax(-1).gather(1,torch.tensor(t).view(-1,1)).flatten()
    vv=lp.tolist();sc=float(lp.double().sum());assert abs(sc-math.fsum(vv))<1e-10
    scores.append(dict(label=c['label'],text=c['text'],token_ids=t,token_logprobs=vv,total_logprob=sc,mean_logprob=sc/len(t)))
  by={a['label']:a['total_logprob'] for a in scores};sib=DOMAINS.get(p['domain'],['none','cat','dog'])[1:]
  choice=max(scores,key=lambda a:a['total_logprob'])['label'];schoice=max(sib,key=by.get);gold=p['behavior_gold']
  f.write(json.dumps(dict(id=p['id'],family=p['family'],split=p['split'],wording=p['wording'],domain=p['domain'],label=p['label'],gold=gold,candidates=scores,choice4=choice,correct4=None if gold is None else choice==gold,sibling_choice=schoice,sibling_correct=None if gold is None else schoice==gold,sibling_margin=None if gold is None else by[gold]-by[next(x for x in sib if x!=gold)],exact_tie=len(set(by.values()))<4))+'\n');f.flush()
  assert time.time()-start<plan['wall_ceiling_seconds']
  if (j+1)%16==0:print(stage,j+1,'/',len(pp),'seconds',round(time.time()-start,1),flush=True)
payload=dict(ids=np.array([p['id'] for p in pp]))
for s,dd in out.items():
 payload.update({s+'__'+k:np.concatenate(v) for k,v in dd.items()});payload[s+'__decoder_norm']=dn[s]
np.savez_compressed(dest,**payload)
dump(R/f'evidence/{stage}_complete.json',dict(UTC=now(),status='COMPLETED',rows=len(pp),seconds=time.time()-start,checks=checks,max_candidate_lane_prefix_difference=lane_max,torch=torch.__version__,device='CPU',shape=[4,128],threads=2,model_trainable=0,SAE_trainable=0,cache_sha256=sha(dest),behavior_sha256=sha(R/f'results/behavior_{stage}.jsonl'),code_sha256=sha(__file__)))
print('COMPLETE',stage,time.time()-start,flush=True)
