from common import *
import sys,os,time,math,importlib.util
import numpy as np,torch
import torch.nn.functional as F
import transformers.utils as hfu,transformers.utils.import_utils as hfi
for m in [hfu,hfi]:
 for n in ['is_flash_attn_2_available','is_flash_attn_3_available','is_torchvision_available','is_librosa_available']:setattr(m,n,lambda:False)
from transformers import AutoModelForCausalLM
stage=sys.argv[1];assert stage in ['smoke','discovery','heldout']
cfg=json.load(open(R/'config.json'));dest=R/f'cache/{stage}.npz';assert not dest.exists()
if stage=='discovery':assert json.load(open(R/'evidence/smoke_complete.json'))['status']=='PASS'
if stage=='heldout':
 gate=json.load(open(R/'evidence/candidates_and_joint_frozen.json'))
 for path,h in gate['hashes'].items():assert sha(path)==h
for path,h in json.load(open(R/'evidence/freeze.json'))['hashes'].items():assert sha(path)==h,path
for path,h in cfg['input_hashes'].items():assert sha(path)==h
for site,s in cfg['sites'].items():assert sha(s['path'])==s['sha256'] and sha(s['loader'])==s['loader_sha256']
panel=[p for p in rows(R/'data/panel.jsonl') if p['split']==stage];old={x['R19_id']:x for x in rows(R/'data/R18_scores.jsonl')}
torch.set_num_threads(2);torch.set_num_interop_threads(1);torch.manual_seed(cfg['seed']);start=time.time()
model=AutoModelForCausalLM.from_pretrained(cfg['model'],torch_dtype=torch.float32,local_files_only=True,attn_implementation='sdpa').cpu().eval().requires_grad_(False);model.config.use_cache=False
saes={}
for site,s in cfg['sites'].items():
 spec=importlib.util.spec_from_file_location('native_'+site,s['loader']);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod);sae=mod.TopKSAE.from_pretrained(s['path'],map_location='cpu').eval().requires_grad_(False);assert (sae.d_model,sae.n_latents,sae.k)==(1024,30000,32);saes[site]=sae
assert not any(p.requires_grad for p in model.parameters()) and all(not any(p.requires_grad for p in s.parameters()) for s in saes.values())
dump(R/f'evidence/{stage}_started.json',dict(UTC=now(),rows=len(panel),pid=os.getpid(),device='CPU',torch=torch.__version__,shape=cfg['shape'],trainable=0))
col={site:{name:[] for name in ['h','indices','values','cutoff32','cutoff33','relative_reconstruction_error']} for site in SITES};maxlane=0.;maxreplay=0.;checks=[]
@torch.inference_mode()
def forward(p,capture=True):
 xx=torch.zeros(2,328,dtype=torch.long);mask=torch.zeros_like(xx);cap={};hooks=[]
 for j,c in enumerate(p['candidates']):xx[j,:len(c['full_ids'])]=torch.tensor(c['full_ids']);mask[j,:len(c['full_ids'])]=1
 if capture:
  hooks=[model.model.layers[27].self_attn.o_proj.register_forward_hook(lambda m,a,y:cap.update(ATTN_SAE=y[:,319].clone())),model.model.layers[27].mlp.register_forward_pre_hook(lambda m,a:cap.update(MLPIN_SAE=a[0][:,319].clone()))]
 try:h=model.model(input_ids=xx,attention_mask=mask,use_cache=False,return_dict=True).last_hidden_state
 finally:
  for hook in hooks:hook.remove()
 return cap,h,xx,mask
with (R/f'results/behavior_{stage}.jsonl').open('x') as out:
 for i,p in enumerate(panel):
  cap,h,xx,mask=forward(p)
  if i==0:
   _,none,_,_=forward(p,False);no_op=float((h-none).abs().max());assert no_op==0;checks.append(dict(no_op_max_error=no_op))
  for site,sae in saes.items():
   lane=float((cap[site][0]-cap[site][1]).abs().max());maxlane=max(maxlane,lane);assert lane<1e-5
   with torch.inference_mode():
    x=cap[site][:1];vals,idx,z,pre=sae.encode_topk(x);assert torch.isfinite(z).all();vv,ii=F.linear(x,sae.encoder.weight,sae.encoder.bias).relu().topk(32,sorted=False);assert torch.equal(z,torch.zeros_like(z).scatter(-1,ii,vv));cut=pre.relu().topk(33,sorted=True).values
    rec=sae.decoder(z);err=(rec-x).norm()/x.norm();values=dict(h=x.numpy(),indices=idx.numpy(),values=vals.numpy(),cutoff32=cut[:,31].numpy(),cutoff33=cut[:,32].numpy(),relative_reconstruction_error=np.array([float(err)]))
    for key,v in values.items():col[site][key].append(v)
  sc=[]
  with torch.inference_mode():
   for j,c in enumerate(p['candidates']):
    ids=c['token_ids'];lp=model.lm_head(h[j,319:319+len(ids)]).float().log_softmax(-1).gather(1,torch.tensor(ids)[:,None]).flatten().tolist();sc.append(dict(label=c['label'],text=c['text'],token_ids=ids,token_logprobs=lp,total_logprob=math.fsum(lp),item_logprob=math.fsum(lp[:-1]),period_logprob=lp[-1]))
  if p['id'] in old:
   for a,b in zip(sc,old[p['id']]['candidates']):maxreplay=max(maxreplay,abs(a['total_logprob']-b['total_logprob']))
   assert maxreplay<2e-5,(p['id'],maxreplay)
  delta=sc[0]['total_logprob']-sc[1]['total_logprob'];choice='A' if delta>0 else 'B' if delta<0 else 'TIE';g=p['gold'];margin=delta if g=='A' else -delta
  out.write(json.dumps(dict(id=p['id'],family=p['family'],split=stage,condition=p['condition'],gold=g,near_label=p['near_label'],candidates=sc,A_minus_B=delta,choice=choice,correct=choice==g,correct_margin=margin,R18_source_id=p['R18_source_id']))+'\n');out.flush()
  if (i+1)%12==0:print(stage,i+1,'/',len(panel),'seconds',round(time.time()-start,1),flush=True)
  assert time.time()-start<cfg['wall_ceiling_per_stage']
payload=dict(ids=np.array([p['id'] for p in panel]))
for site,dd in col.items():
 payload.update({site+'__'+k:np.concatenate(v) for k,v in dd.items()});payload[site+'__decoder_norm']=saes[site].decoder.weight.detach().norm(dim=0).numpy()
np.savez_compressed(dest,**payload)
for path,h in cfg['input_hashes'].items():assert sha(path)==h
for site,s in cfg['sites'].items():assert sha(s['path'])==s['sha256']
dump(R/f'evidence/{stage}_complete.json',dict(UTC=now(),status='PASS',rows=len(panel),seconds=time.time()-start,max_candidate_lane_prefix_error=maxlane,max_R18_score_replay_error=maxreplay,checks=checks,positive_counts={site:np.unique(np.count_nonzero(payload[site+'__values'],axis=1)).tolist() for site in SITES},code_sha256=sha(__file__),cache_sha256=sha(dest),behavior_sha256=sha(R/f'results/behavior_{stage}.jsonl'),model_and_SAEs_unchanged=True,training_updates=0,interventions=False))
print('COMPLETE',stage,round(time.time()-start,2),flush=True)
