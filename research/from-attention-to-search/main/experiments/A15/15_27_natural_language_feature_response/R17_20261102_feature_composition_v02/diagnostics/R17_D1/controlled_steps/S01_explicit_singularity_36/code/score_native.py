"""Native LM likelihood only. No hooks, dictionaries, representations, probes, or fitting."""
from pathlib import Path
import json,hashlib,datetime,time,math,os
import torch
import transformers.utils as hfu,transformers.utils.import_utils as hfi
for mod in [hfu,hfi]:
 for name in ['is_flash_attn_2_available','is_flash_attn_3_available','is_torchvision_available','is_librosa_available']:setattr(mod,name,lambda:False)
from transformers import AutoModelForCausalLM
from tokenizers import Tokenizer
R=Path(__file__).resolve().parents[1]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb')as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
plan=json.load(open(R/'frozen_plan.json'));frozen_sha=sha(R/'frozen_plan.json');assert not(R/'results/raw_scores.jsonl').exists(),'Do not repeat a completed panel or overwrite originalscores.'
for name,digest in plan['data_SHA256'].items():assert sha(R/'data'/name)==digest,name
access=json.load(open(R/'evidence/input_access.json'));assert not access['selected_required_failures']
M=Path(plan['model']);old=json.load(open(R.parents[3]/'shared/models/input_fingerprints.json'))['sha256']
identity={str(M/n):sha(M/n)for n in ['config.json','tokenizer.json','model.safetensors']}
for p,digest in identity.items():assert digest==old[p],p
started=datetime.datetime.now(datetime.timezone.utc).isoformat();dump(R/'evidence/started.json',dict(UTC=started,frozen_plan_SHA256=frozen_sha,data_SHA256=plan['data_SHA256'],input_SHA256=identity,device='CPU only; noGPUjob',scope='36x2 +2neutralprefixes; nativeonly; stopafterreview'))
torch.set_num_threads(plan['threads']);torch.set_num_interop_threads(1);torch.manual_seed(20261103);start=time.time()
model=AutoModelForCausalLM.from_pretrained(M,torch_dtype=torch.float32,local_files_only=True,attn_implementation='sdpa').to('cpu').eval().requires_grad_(False);model.config.use_cache=False
assert not any(p.requires_grad for p in model.parameters());assert all(p.dtype==torch.float32 for p in model.parameters()if p.is_floating_point());assert not any(m._forward_hooks or m._forward_pre_hooks for m in model.modules())
T=Tokenizer.from_file(str(M/'tokenizer.json'));prompts=[json.loads(l)for l in open(R/'data/prompts_tokenized.jsonl')];raw=[];duplicate_errors=[]
@torch.inference_mode()
def score(p):
 prefix=p['prefix_token_ids'];cs=p['candidates'];B,L=plan['physical_batch'],plan['physical_length'];xx=torch.full((B,L),plan['padding_id'],dtype=torch.long);mask=torch.zeros_like(xx)
 for j,c in enumerate(cs+[cs[0]]):
  ids=c['full_input_token_ids'];assert len(ids)<=L and ids[:len(prefix)]==prefix;xx[j,:len(ids)]=torch.tensor(ids);mask[j,:len(ids)]=1
 # Standard native backbone+LM head, same path as D1 native scorer. No activations are saved or analyzed.
 last=model.model(input_ids=xx,attention_mask=mask,use_cache=False,return_dict=True).last_hidden_state
 out=[]
 for j,c in enumerate(cs+[cs[0]]):
  target=c['candidate_token_ids'];logits=model.lm_head(last[j,len(prefix)-1:len(prefix)+len(target)-1]).float();lp=logits.log_softmax(-1).gather(1,torch.tensor(target).view(-1,1)).squeeze(1);assert bool(torch.isfinite(lp).all())and bool((lp<=0).all());values=lp.tolist();total=float(lp.double().sum());assert abs(math.fsum(values)-total)<1e-10
  out.append(dict(label=c['label'],candidate=c['text'],order=c['order'],candidate_token_ids=target,candidate_tokens=len(target),candidate_token_pieces=[T.id_to_token(x)for x in target],token_logprobs=values,total_logprob=total))
 duplicate_errors.append(abs(out[0]['total_logprob']-out[3]['total_logprob']));assert duplicate_errors[-1]<1e-6;out=out[:3];best=max(out,key=lambda c:c['total_logprob']);ranking=sorted(out,key=lambda c:-c['total_logprob']);ties=[c['label']for c in out if c['total_logprob']==best['total_logprob']];gold=p['gold'];correct=None if gold is None else best['label']==gold
 return dict(id=p['id'],family=p['family'],condition=p['condition'],format=p['format'],gold=gold,prefix=p['prefix'],prefix_token_ids=prefix,prefix_tokens=len(prefix),candidates=out,preferred_label=best['label'],preferred_text=best['candidate'],correct=correct,margin=ranking[0]['total_logprob']-ranking[1]['total_logprob'],exact_tie_labels=ties,correct_margin=None if gold is None else next(c['total_logprob']for c in out if c['label']==gold)-max(c['total_logprob']for c in out if c['label']!=gold))
with(R/'results/raw_scores.jsonl').open('x')as f:
 for i,p in enumerate(prompts,1):
  rec=score(p);raw.append(rec);f.write(json.dumps(rec,ensure_ascii=False)+'\n');f.flush()
  if i==1 or i%12==0 or i==len(prompts):print('PROGRESS',i,'/',len(prompts),'seconds',round(time.time()-start,2),flush=True)
assert len(raw)==74 and sum(x['gold']is not None for x in raw)==72
for name,digest in plan['data_SHA256'].items():assert sha(R/'data'/name)==digest
assert sha(R/'frozen_plan.json')==frozen_sha
assert not any(p.requires_grad for p in model.parameters());assert not any(m._forward_hooks or m._forward_pre_hooks for m in model.modules())
dump(R/'evidence/completed.json',dict(status='COMPLETED_STEP1_STOP_FOR_JOINT_REVIEW',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),started_UTC=started,elapsed_seconds=time.time()-start,torch=torch.__version__,transformers_source=str(hfu.__file__),device='cpu',threads=torch.get_num_threads(),GPU_jobs=0,model_updates=0,dictionaries_loaded=0,hooks=0,probes_fitted=0,raw_records=len(raw),matrix_decisions=72,candidate_sequences=222,neutral_decisions=2,max_duplicate_lane_score_error=max(duplicate_errors),frozen_plan_SHA256=frozen_sha,input_SHA256=identity,raw_scores_SHA256=sha(R/'results/raw_scores.jsonl'),code_SHA256=sha(__file__),old_score_reuse=False,nextstep_executed=False))
print('COMPLETED_ONLY_STEP1',round(time.time()-start,2),flush=True)
