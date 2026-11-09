"""S02 fixed native continuation. No classifiers, dictionaries, hooks, or feature records."""
from pathlib import Path
import json,hashlib,datetime,time,math
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
plan=json.load(open(R/'frozen_plan.json'));plan_sha=sha(R/'frozen_plan.json');assert not(R/'results/raw_scores.jsonl').exists(),'No overwrite or repeated completed experiment.'
for name,digest in plan['data_SHA256'].items():assert sha(R/'data'/name)==digest
assert not json.load(open(R/'evidence/input_access.json'))['selected_required_failures']
prior=json.load(open(R.parent/'S01_explicit_singularity_36/evidence/completed.json'));M=Path(plan['model']);identity={str(M/n):sha(M/n)for n in ['config.json','tokenizer.json','model.safetensors']};assert identity==prior['input_SHA256']
started=datetime.datetime.now(datetime.timezone.utc).isoformat();dump(R/'evidence/started.json',dict(UTC=started,frozen_plan_sha256=plan_sha,input_SHA256=identity,device='cpu',scope='12fixedtexts+1neutral;onlyoneformat;noextraquestions'))
torch.set_num_threads(2);torch.set_num_interop_threads(1);torch.manual_seed(20261103);start=time.time();model=AutoModelForCausalLM.from_pretrained(M,torch_dtype=torch.float32,local_files_only=True,attn_implementation='sdpa').to('cpu').eval().requires_grad_(False);model.config.use_cache=False
assert not any(p.requires_grad for p in model.parameters());assert not any(m._forward_hooks or m._forward_pre_hooks for m in model.modules());assert all(p.dtype==torch.float32 for p in model.parameters()if p.is_floating_point())
T=Tokenizer.from_file(str(M/'tokenizer.json'));prompts=[json.loads(l)for l in open(R/'data/prompts_tokenized.jsonl')];dups=[]
@torch.inference_mode()
def score(p):
 pre=p['prefix_token_ids'];cs=p['candidates'];assert len(cs)==2;xx=torch.full((4,192),0,dtype=torch.long);mask=torch.zeros_like(xx)
 for j,c in enumerate(cs+cs):
  ids=c['full_input_token_ids'];assert ids[:len(pre)]==pre and len(ids)<=192;xx[j,:len(ids)]=torch.tensor(ids);mask[j,:len(ids)]=1
 # Native language-model forward/head only. Intermediate tensors are not captured, saved, or analyzed.
 state=model.model(input_ids=xx,attention_mask=mask,use_cache=False,return_dict=True).last_hidden_state;out=[]
 for j,c in enumerate(cs+cs):
  target=c['candidate_token_ids'];lp=model.lm_head(state[j,len(pre)-1:len(pre)+len(target)-1]).float().log_softmax(-1).gather(1,torch.tensor(target).view(-1,1)).squeeze(1);assert bool(torch.isfinite(lp).all())and bool((lp<=0).all());vals=lp.tolist();total=float(lp.double().sum());assert abs(math.fsum(vals)-total)<1e-10;out.append(dict(label=c['label'],candidate=c['text'],order=c['order'],candidate_token_ids=target,candidate_token_pieces=[T.id_to_token(x)for x in target],candidate_tokens=len(target),token_logprobs=vals,total_logprob=total))
 for j in range(2):dups.append(abs(out[j]['total_logprob']-out[j+2]['total_logprob']));assert dups[-1]<1e-6
 out=out[:2];best=max(out,key=lambda c:c['total_logprob']);delta=out[0]['total_logprob']-out[1]['total_logprob'];gold=p['gold']
 return dict(id=p['id'],family=p['family'],text=p['text'],prefix=p['prefix'],prefix_token_ids=pre,prefix_tokens=len(pre),labels=['animal',gold]if gold else['animal'],gold=gold,candidates=out,delta_cat_minus_dog=delta,choice=best['label'],choice_text=best['candidate'],correct=None if gold is None else best['label']==gold,exact_tie=delta==0,correct_margin=None if gold is None else delta*(1 if gold=='cat'else-1))
with(R/'results/raw_scores.jsonl').open('x')as f:
 for i,p in enumerate(prompts,1):
  f.write(json.dumps(score(p),ensure_ascii=False)+'\n');f.flush()
  if i in [1,6,12,13]:print('S02PROGRESS',i,'/13',round(time.time()-start,2),'seconds',flush=True)
for name,digest in plan['data_SHA256'].items():assert sha(R/'data'/name)==digest
assert sha(R/'frozen_plan.json')==plan_sha
for name,digest in json.load(open(R/'evidence/S01_immutable_before.json')).items():assert sha(name)==digest,('oldS01changed',name)
assert not any(m._forward_hooks or m._forward_pre_hooks for m in model.modules())
dump(R/'evidence/completed.json',dict(status='COMPLETED_S02_WAIT_FOR_JOINT_REVIEW',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),started_UTC=started,elapsed_seconds=time.time()-start,input_SHA256=identity,code_SHA256=sha(__file__),frozen_plan_SHA256=plan_sha,data_SHA256=plan['data_SHA256'],raw_scores_SHA256=sha(R/'results/raw_scores.jsonl'),device='cpu',torch=torch.__version__,threads=2,model_updates=0,dictionaries_loaded=0,feature_hooks=0,probe_fits=0,GPU_jobs=0,formats=1,test_rows=12,neutral_prefixes=1,candidate_sequences=26,max_duplicate_lane_difference=max(dups),all_S01_files_unchanged=True,next_step_executed=False))
print('S02_COMPLETE_STOP',round(time.time()-start,2),flush=True)
