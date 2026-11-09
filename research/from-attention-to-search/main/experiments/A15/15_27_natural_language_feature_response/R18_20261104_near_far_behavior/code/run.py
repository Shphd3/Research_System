from common import *
import os,sys,time,math
import torch
import transformers.utils as hfu, transformers.utils.import_utils as hfi
for m in [hfu,hfi]:
    for n in ['is_flash_attn_2_available','is_flash_attn_3_available','is_torchvision_available','is_librosa_available']: setattr(m,n,lambda:False)
from transformers import AutoModelForCausalLM
stage=sys.argv[1];assert stage in ['smoke','heldout']
assert not (R/f'results/{stage}.jsonl').exists()
if stage=='heldout': assert json.load(open(R/'evidence/smoke_complete.json'))['implementation_status']=='PASS'
cfg=json.load(open(R/'config.json'));freeze=json.load(open(R/'evidence/freeze.json'))
for path,h in freeze['hashes'].items(): assert sha(path)==h,(path,'freeze changed')
for path,h in cfg['input_sha256'].items(): assert sha(path)==h
pp=[p for p in rows(R/'data/panel.jsonl') if p['split']==stage]
torch.set_num_threads(cfg['threads']);torch.set_num_interop_threads(1);torch.manual_seed(cfg['seed']);start=time.time()
model=AutoModelForCausalLM.from_pretrained(cfg['model'],torch_dtype=torch.float32,local_files_only=True,attn_implementation='sdpa').cpu().eval().requires_grad_(False)
model.config.use_cache=False
assert not any(p.requires_grad for p in model.parameters())
dump(R/f'evidence/{stage}_started.json',dict(UTC=now(),pid=os.getpid(),rows=len(pp),device='cpu',torch=torch.__version__,dtype='float32',trainable_parameters=0,shape=cfg['scoring_shape']))
@torch.inference_mode()
def score(p,check=False):
    n=len(p['token_ids']);xx=torch.zeros(*cfg['scoring_shape'],dtype=torch.long);mask=torch.zeros_like(xx)
    for j,c in enumerate(p['candidates']):
        full=c['full_ids'];xx[j,:len(full)]=torch.tensor(full);mask[j,:len(full)]=1
    hh=model.model(input_ids=xx,attention_mask=mask,use_cache=False,return_dict=True).last_hidden_state
    output=[]
    for j,c in enumerate(p['candidates']):
        ids=c['token_ids'];lp=model.lm_head(hh[j,n-1:n+len(ids)-1]).float().log_softmax(-1).gather(1,torch.tensor(ids)[:,None]).flatten()
        vv=lp.tolist();total=math.fsum(vv)
        output.append(dict(label=c['label'],text=c['text'],token_ids=ids,token_count=len(ids),token_logprobs=vv,total_logprob=total,mean_logprob=total/len(ids),item_logprob=math.fsum(vv[:-1]),period_logprob=vv[-1]))
    lp0=model.lm_head(hh[0,n-1]).float().log_softmax(-1);top=lp0.topk(10)
    audit={}
    if check:
        # Independent public model forward and explicit chain rule at every answer token.
        direct=model(input_ids=xx,attention_mask=mask,use_cache=False,return_dict=True).logits
        errs=[]
        for j,c in enumerate(p['candidates']):
            for k,tid in enumerate(c['token_ids']):
                ref=float(torch.log_softmax(direct[j,n+k-1].float(),-1)[tid]);errs.append(abs(ref-output[j]['token_logprobs'][k]))
        px=xx.clone();pm=mask.clone();px[:,n:]=0;pm[:,n:]=0
        ph=model.model(input_ids=px,attention_mask=pm,use_cache=False,return_dict=True).last_hidden_state
        prefixerr=float((ph[:,n-1]-hh[:,n-1]).abs().max());laneerr=float((hh[0,n-1]-hh[1,n-1]).abs().max())
        assert max(errs)<2e-5 and prefixerr<1e-5 and laneerr<1e-5,(errs,prefixerr,laneerr)
        audit=dict(direct_forward_token_error=max(errs),prefix_only_hidden_error=prefixerr,candidate_lane_prefix_error=laneerr)
    by={z['label']:z['total_logprob'] for z in output};delta=by['A']-by['B'];choice='A' if delta>0 else 'B' if delta<0 else 'TIE';gold=p['gold']
    margin=None if gold is None else (delta if gold=='A' else -delta)
    return dict(id=p['id'],family=p['family'],split=p['split'],template=p['template'],mode=p['mode'],planned_distance=p['planned_distance'],actual_distance=p['actual_distance'],nominal_slot_distance=p['nominal_slot_distance'],candidates=output,A_minus_B=delta,choice=choice,gold=gold,correct=None if gold is None else choice==gold,correct_margin=margin,first_token_top10_ids=top.indices.tolist(),first_token_top10_logprobs=top.values.tolist(),audit=audit)
checks=[]
with (R/f'results/{stage}.jsonl').open('x') as f:
    for i,p in enumerate(pp):
        z=score(p,check=(i==0));checks.extend([z['audit']] if z['audit'] else [])
        f.write(json.dumps(z,allow_nan=False)+'\n');f.flush()
        assert time.time()-start<cfg['max_wall_seconds']
        if (i+1)%12==0:print(stage,i+1,'/',len(pp),'seconds',round(time.time()-start,1),flush=True)
if stage=='smoke':
    # A multi-token engineering fixture is not a heldout behavioral observation.
    from tokenizers import Tokenizer
    t=Tokenizer.from_file(str(MODEL/'tokenizer.json'));prefix='The chosen item is';ids=t.encode(prefix,add_special_tokens=False).ids
    cands=[]
    for label,text in [('A',' toy car.'),('B',' toy truck.')]:
        full=t.encode(prefix+text,add_special_tokens=False).ids
        assert full[:len(ids)]==ids
        cands.append(dict(label=label,text=text,token_ids=full[len(ids):],full_ids=full))
    fixture=dict(id='engineering_multitoken',family='NONE',split='smoke',template='fixture',mode='calibration',planned_distance=0,actual_distance=None,nominal_slot_distance=0,gold=None,token_ids=ids,candidates=cands)
    z=score(fixture,check=True);dump(R/'evidence/multitoken_calibration.json',z);checks.append(z['audit'])
elapsed=time.time()-start
assert all(sha(path)==h for path,h in cfg['input_sha256'].items())
dump(R/f'evidence/{stage}_complete.json',dict(UTC=now(),implementation_status='PASS',rows=len(pp),seconds=elapsed,checks=checks,output_sha256=sha(R/f'results/{stage}.jsonl'),trainable_parameters=0,training_updates=0,SAE_loaded=False,intervention=False,weights_unchanged=True,model_context_max=model.config.max_position_embeddings))
print('COMPLETE',stage,elapsed,flush=True)
