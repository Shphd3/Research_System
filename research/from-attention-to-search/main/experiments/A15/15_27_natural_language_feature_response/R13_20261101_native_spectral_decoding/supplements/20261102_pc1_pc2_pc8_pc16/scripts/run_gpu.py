import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,time,hashlib,datetime,traceback
import numpy as np
import torch
import transformers.utils as u,transformers.utils.import_utils as iu
for mod in [u,iu]:
 for f in ['is_flash_attn_2_available','is_flash_attn_3_available','is_torchvision_available','is_librosa_available']:setattr(mod,f,lambda:False)
from transformers import AutoModelForCausalLM
from tokenizers import Tokenizer
E=Path(__file__).resolve().parents[1];OLD=E.parents[1];M=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for a in iter(lambda:f.read(8<<20),b''):h.update(a)
 return h.hexdigest()
def dump(p,a):
 tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');tmp.replace(p)
@torch.inference_mode()
def main():
 start=time.time();torch.set_num_threads(2);torch.manual_seed(20261102);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 assert '5090' in torch.cuda.get_device_name(0) and os.environ.get('RESOURCE_PROFILE')=='5090-2-spot'
 for p,h in json.load(open(E/'freeze.json'))['sha256'].items():assert sha(p)==h,p
 model=AutoModelForCausalLM.from_pretrained(str(M),local_files_only=True,trust_remote_code=False,torch_dtype=torch.bfloat16,attn_implementation='sdpa').cuda().eval().requires_grad_(False)
 assert model.lm_head.weight.data_ptr()==model.model.embed_tokens.weight.data_ptr()
 def decode(a):return model.lm_head(model.model.norm(torch.tensor(a,device='cuda',dtype=torch.bfloat16))).float()
 A=np.load(OLD/'data/fresh_h.npy');b=np.load(OLD/'data/bases.npz');mu=b['mean'];V=b['V'];f=np.load(OLD/'data/frequency.npz');fmt=torch.tensor(f['format_mask'],device='cuda');valid=torch.tensor(f['valid'],device='cuda');lf=torch.tensor(f['logfreq'],device='cuda',dtype=torch.float32);grp=torch.tensor(f['group'],device='cuda');rr=[json.loads(l) for l in (OLD/'data/native_positions.jsonl').read_text().splitlines()];tok=Tokenizer.from_file(str(M/'tokenizer.json'))
 old={(x['index'],x['condition']):x for l in (OLD/'analysis/raw_outputs.jsonl').read_text().splitlines() if (x:=json.loads(l))['condition'] in ['identity','k1','k16']};yy=torch.tensor([x['target_id'] for x in rr],device='cuda');maxerr=0.;replay=[]
 # Recheck old fixed conditions on matched batch shapes; new conditions only if all replays pass.
 for lo in range(0,len(A),16):
  hi=min(lo+16,len(A));logits=decode(A[lo:hi]);lp=torch.log_softmax(logits,1);idx=torch.arange(hi-lo,device='cuda');nll=-lp[idx,yy[lo:hi]]
  maxerr=max(maxerr,max(abs(float(nll[j])-old[lo+j,'identity']['NLL']) for j in range(hi-lo)))
  if lo==0:
   for k in [1,16]:
    Q=V[:,:k];hp=mu+(A[:16]-mu)@Q@Q.T;lp1=torch.log_softmax(decode(hp),1);p1=lp1.exp();err=max(abs(float(-lp1[j,yy[j]])-old[j,f'k{k}']['NLL']) for j in range(16));pe=max(abs(float(p1[j,t['id']])-t['probability']) for j in range(16) for t in old[j,f'k{k}']['top20']);replay.append({'condition':f'k{k}','NLL_max_abs':err,'saved_top20_probability_max_abs':pe});assert err<=1e-6 and pe<=1e-7,replay[-1]
 assert maxerr<=1e-6,('identity replay',maxerr)
 dump(E/'provenance/smoke.json',{'pass':True,'identity_NLL_max_abs_all737':maxerr,'replay':replay,'torch':torch.__version__,'transformers':__import__('transformers').__version__,'GPU':torch.cuda.get_device_name(0),'trainable_parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),'no_transformer_forward':True})
 print('SMOKE_PASS',maxerr,replay,flush=True)
 chunks=E/'analysis/chunks';chunks.mkdir(exist_ok=True)
 for lo in range(0,len(A),16):
  hi=min(lo+16,len(A));path=chunks/f'{lo:06d}.json'
  if path.exists():continue
  full=decode(A[lo:hi]);flp=torch.log_softmax(full,1);fp=flp.exp();idx=torch.arange(hi-lo,device='cuda');target=yy[lo:hi];records=[]
  for name,Q in [('pc2',V[:,1:2]),('k8',V[:,:8])]:
   hp=mu+(A[lo:hi]-mu)@Q@Q.T;lg=decode(hp);lp=torch.log_softmax(lg,1);prob=lp.exp();pv,pi=prob.topk(64,1);nll=-lp[idx,target];kl=(fp*(flp-lp)).sum(1);ent=-(prob*lp).sum(1);ranks=(lg>lg[idx,target,None]).sum(1)+1;mass=prob[:,valid].sum(1);fm=prob[:,fmt].sum(1);freqmass=torch.stack([prob[:,grp==g].sum(1) for g in range(4)],1);elog=(prob*lf).sum(1)/mass
   for j in range(hi-lo):
    cand=sorted([{'id':int(i),'fragment':tok.decode([int(i)],skip_special_tokens=False),'probability':float(p)} for i,p in zip(pi[j],pv[j])],key=lambda x:(-x['probability'],x['id']));assert cand[9]['probability']>cand[-1]['probability']
    ref=old[lo+j,'identity']['top20'];top=cand[:20];records.append({'index':lo+j,'position_uid':rr[lo+j]['position_uid'],'condition':name,'NLL':float(nll[j]),'KL_full':float(kl[j]),'entropy':float(ent[j]),'target_rank':int(ranks[j]),'target_probability':float(prob[j,target[j]]),'top1_correct':top[0]['id']==int(target[j]),'top1_agreement':top[0]['id']==ref[0]['id'],'top10_recovery':len({x['id'] for x in top[:10]}&{x['id'] for x in ref[:10]})/10,'format_mass':float(fm[j]),'lexical_mass':float(mass[j]),'expected_log_frequency':float(elog[j]),'frequency_mass':[float(x) for x in freqmass[j]],'top20':top})
  dump(path,{'records':records})
  if lo%160==0:print('positions',hi,'elapsed',time.time()-start,flush=True)
 dump(E/'terminal_receipt.json',{'status':'COMPLETE','positions':737,'new_conditions':['pc2','k8'],'new_transformer_forwards':0,'training_updates':0,'elapsed_seconds':time.time()-start,'peak_GPU_bytes':torch.cuda.max_memory_allocated(),'device_used':[0]});print('COMPLETE',flush=True)
if __name__=='__main__':
 try:main()
 except Exception:dump(E/'provenance/failure.json',{'traceback':traceback.format_exc()});raise
