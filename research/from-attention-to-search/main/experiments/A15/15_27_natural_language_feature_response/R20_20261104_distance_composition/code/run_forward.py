from native import *
import sys,os,time,math
import transformers.utils as hfu,transformers.utils.import_utils as hfi
for mod in [hfu,hfi]:
 for name in ['is_flash_attn_2_available','is_flash_attn_3_available','is_torchvision_available','is_librosa_available']:setattr(mod,name,lambda:False)
from transformers import AutoModelForCausalLM
stage=sys.argv[1];assert stage in ['smoke','full'];assert_freeze();cfg=json.load(open(R/'config.json'));panel={p['id']:p for p in rows(R/'data/panel.jsonl')};old={p['id']:p for p in rows(R/'results/behavior_old.jsonl')}
if stage=='full':assert json.load(open(R/'evidence/smoke_complete.json'))['status']=='PASS'
for path,h in cfg['input_hashes'].items():assert sha(path)==h,path
ids=cfg['calibration_ids']+cfg['smoke_ids'] if stage=='smoke' else [p['id'] for p in panel.values() if p['provenance']=='NEW_FORWARD'];torch.set_num_threads(2);torch.set_num_interop_threads(1);torch.manual_seed(SEED);start=time.monotonic()
model=AutoModelForCausalLM.from_pretrained(cfg['model'],torch_dtype=torch.float32,local_files_only=True,attn_implementation='sdpa').cpu().eval().requires_grad_(False);model.config.use_cache=False;saes=load_saes();assert not any(p.requires_grad for p in model.parameters())
dump(R/f'evidence/{stage}_started.json',dict(UTC=now(),local_time=local_now(),pid=os.getpid(),rows=len(ids),device='CPU',threads=2,shape=[2,328],code_sha256=sha(__file__),native_code_sha256=sha(R/'code/native.py'),trainable_parameters=0,cache_resumable=True))
@torch.inference_mode()
def forward(p,hook=True):
 xx=torch.zeros(2,328,dtype=torch.long);mask=torch.zeros_like(xx);cap={};handles=[];n=len(p['token_ids']);target=p['target_position']
 for j,c in enumerate(p['candidates']):xx[j,:len(c['full_ids'])]=torch.tensor(c['full_ids']);mask[j,:len(c['full_ids'])]=1
 if hook:handles=[model.model.layers[27].self_attn.o_proj.register_forward_hook(lambda m,a,y:cap.update(ATTN_SAE=y[:,target].clone())),model.model.layers[27].mlp.register_forward_pre_hook(lambda m,a:cap.update(MLPIN_SAE=a[0][:,target].clone()))]
 pos=(torch.arange(328)+p['position_offset']).unsqueeze(0).expand(2,-1)
 try:h=model.model(input_ids=xx,attention_mask=mask,position_ids=pos,use_cache=False,return_dict=True).last_hidden_state
 finally:
  for handle in handles:handle.remove()
 return cap,h
maxlane=0.;maxreplay=0.;no_op=None;newly_done=0;resumed=0
for k,pid in enumerate(ids):
 p=panel[pid];kind='calibration' if p['provenance']=='R19_REUSE' else 'new_rows';cachepath=R/f'cache/{kind}/{pid}.npz';scorepath=R/f'results/{kind}/{pid}.json';cachepath.parent.mkdir(exist_ok=True);scorepath.parent.mkdir(exist_ok=True)
 if cachepath.exists() and scorepath.exists():
  receipt=json.load(open(scorepath));assert receipt['cache_sha256']==sha(cachepath) and receipt['code_sha256']==sha(__file__);resumed+=1;continue
 assert not cachepath.exists() and not scorepath.exists(),'Partial row must be preserved/recovered explicitly.'
 cap,h=forward(p)
 if newly_done==0 and stage=='smoke':
  _,without=forward(p,False);no_op=float((h-without).abs().max());assert no_op==0
 payload={}
 for site,sae in saes.items():
  lane=float((cap[site][0]-cap[site][1]).abs().max());assert lane<1e-5;maxlane=max(maxlane,lane);values=encode_one(sae,cap[site][:1]);payload.update({site+'__'+key:v for key,v in values.items()});payload[site+'__decoder_norm']=sae.decoder.weight.detach().norm(dim=0).numpy()
 sc=[]
 with torch.inference_mode():
  for j,c in enumerate(p['candidates']):
   pp=p['target_position'];lp=model.lm_head(h[j,pp:pp+len(c['token_ids'])]).float().log_softmax(-1).gather(1,torch.tensor(c['token_ids'])[:,None]).flatten().tolist();sc.append(dict(label=c['label'],text=c['text'],token_ids=c['token_ids'],token_logprobs=lp,total_logprob=math.fsum(lp),item_logprob=math.fsum(lp[:-1]),period_logprob=lp[-1]))
 if pid in old:
  for c,b in zip(sc,old[pid]['candidates']):maxreplay=max(maxreplay,abs(c['total_logprob']-b['total_logprob']))
  assert maxreplay<2e-5
 delta=sc[0]['total_logprob']-sc[1]['total_logprob'];choice='A' if delta>0 else 'B' if delta<0 else 'TIE';margin=delta*(1 if p['gold']=='A' else -1)
 temp=cachepath.with_suffix('.tmp.npz');np.savez_compressed(temp,**payload);temp.replace(cachepath)
 dump(scorepath,dict(id=pid,family=p['family'],split=p['split'],condition=p['condition'],gold=p['gold'],distance=p['actual_distance'],target_position=p['target_position'],position_offset=p['position_offset'],candidates=sc,choice=choice,correct=choice==p['gold'],correct_margin=margin,A_minus_B=delta,cache_sha256=sha(cachepath),code_sha256=sha(__file__),UTC=now()))
 newly_done+=1
 if (k+1)%12==0 or k+1==len(ids):print(stage,k+1,'/',len(ids),'new',newly_done,'reused',resumed,'seconds',round(time.monotonic()-start,1),flush=True)
 assert time.monotonic()-start<cfg['wall_ceiling_per_stage']
for path,h in cfg['input_hashes'].items():assert sha(path)==h,path
for site,s in cfg['sites'].items():assert sha(s['path'])==s['sha256']
dump(R/f'evidence/{stage}_complete.json',dict(UTC=now(),local_time=local_now(),status='PASS',requested_rows=len(ids),newly_scored=newly_done,reused_rows=resumed,seconds=time.monotonic()-start,max_candidate_lane_error=maxlane,max_old_score_error=maxreplay,no_op_error=no_op,weights_unchanged=True,model_updates=0,interventions=0))
print('COMPLETE',stage,round(time.monotonic()-start,1),flush=True)
