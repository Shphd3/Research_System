import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,time,hashlib,traceback
import numpy as np,torch
import transformers.utils as u,transformers.utils.import_utils as iu
for mod in [u,iu]:
 for f in ['is_flash_attn_2_available','is_flash_attn_3_available','is_torchvision_available','is_librosa_available']:setattr(mod,f,lambda:False)
from transformers import AutoModelForCausalLM
from tokenizers import Tokenizer
E=Path(__file__).resolve().parents[1];O=E.parents[1];M=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for v in iter(lambda:f.read(8<<20),b''):h.update(v)
 return h.hexdigest()
def dump(p,x):
 t=p.with_suffix('.tmp');t.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n');t.replace(p)
@torch.inference_mode()
def main():
 start=time.time();torch.set_num_threads(2);torch.manual_seed(20261103);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 assert '5090' in torch.cuda.get_device_name(0) and os.environ.get('RESOURCE_PROFILE')=='5090-2-spot'
 for p,h in json.load(open(E/'freeze.json'))['sha256'].items():assert sha(p)==h,p
 model=AutoModelForCausalLM.from_pretrained(str(M),local_files_only=True,trust_remote_code=False,torch_dtype=torch.bfloat16,attn_implementation='sdpa').cuda().eval().requires_grad_(False);assert model.lm_head.weight.data_ptr()==model.model.embed_tokens.weight.data_ptr()
 def decode(a):return model.lm_head(model.model.norm(torch.tensor(a,device='cuda',dtype=torch.bfloat16))).float()
 A=np.load(O/'data/fresh_h.npy');B=np.load(O/'data/bases.npz');mu=B['mean'];V=B['V'];assert abs(V.T@V-np.eye(1024)).max()<1e-10;manifest=json.load(open(E/'manifest.json'));rr=[json.loads(l) for l in (O/'data/native_positions.jsonl').read_text().splitlines()];old={(x['index'],x['condition']):x for l in (O/'analysis/raw_outputs.jsonl').read_text().splitlines() if (x:=json.loads(l))['condition'] in ['identity','k16','tail','mean_only']};F=np.load(O/'data/frequency.npz');valid=torch.tensor(F['valid'],device='cuda');fmt=torch.tensor(F['format_mask'],device='cuda');lf=torch.tensor(F['logfreq'],device='cuda',dtype=torch.float32);grp=torch.tensor(F['group'],device='cuda');pm=np.load(E/'permutation.npz');per=pm['source_index'];elig=pm['eligible'];tok=Tokenizer.from_file(str(M/'tokenizer.json'));y=torch.tensor([r['target_id'] for r in rr],device='cuda');maxerr=0.;checks=[]
 for lo in range(0,len(A),16):
  hi=min(lo+16,len(A));lp=torch.log_softmax(decode(A[lo:hi]),1);idx=torch.arange(hi-lo,device='cuda');nll=-lp[idx,y[lo:hi]];maxerr=max(maxerr,max(abs(float(nll[j])-old[lo+j,'identity']['NLL']) for j in range(hi-lo)))
  if lo==0:
   for name,Q in [('k16',V[:,:16]),('tail',V[:,960:])]:
    p=mu+(A[:16]-mu)@Q@Q.T;lp1=torch.log_softmax(decode(p),1);prob=lp1.exp();err=max(abs(float(-lp1[j,y[j]])-old[j,name]['NLL']) for j in range(16));pe=max(abs(float(prob[j,t['id']])-t['probability']) for j in range(16) for t in old[j,name]['top20']);checks.append({'condition':name,'NLL_max_abs':err,'probability_max_abs':pe});assert err<=1e-6 and pe<=1e-7,checks[-1]
 assert maxerr<=1e-6,maxerr
 dump(E/'provenance/smoke.json',{'pass':True,'identity_NLL_max_abs_all737':maxerr,'replay':checks,'torch':torch.__version__,'transformers':__import__('transformers').__version__,'GPU':torch.cuda.get_device_name(0),'trainable_parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),'new_transformer_forwards':0});print('SMOKE_PASS',maxerr,checks,flush=True)
 chunks=E/'analysis/chunks';chunks.mkdir(exist_ok=True)
 for lo in range(0,len(A),16):
  hi=min(lo+16,len(A));path=chunks/f'{lo:06d}.json'
  if path.exists():continue
  lpfull=torch.log_softmax(decode(A[lo:hi]),1);pfull=lpfull.exp();lpm=torch.log_softmax(decode(np.repeat(mu[None],hi-lo,0)),1);idx=torch.arange(hi-lo,device='cuda');yy=y[lo:hi];records=[]
  for conf in manifest['bands']:
   name=conf['condition'];left,right=conf['numpy_slice'];Q=V[:,left:right];hp=mu+(A[lo:hi]-mu)@Q@Q.T;lp=torch.log_softmax(decode(hp),1);prob=lp.exp();pv,pi=prob.topk(64,1);nll=-lp[idx,yy];kl=(pfull*(lpfull-lp)).sum(1);ent=-(prob*lp).sum(1);rank=(lp>lp[idx,yy,None]).sum(1)+1;lex=prob[:,valid].sum(1);freqmass=torch.stack([prob[:,grp==g].sum(1) for g in range(4)],1);massfmt=prob[:,fmt].sum(1);elog=(prob*lf).sum(1)/lex
   shuffled=mu+(A[per[lo:hi]]-mu)@Q@Q.T;slp=torch.log_softmax(decode(shuffled),1);snll=-slp[idx,yy]
   for j in range(hi-lo):
    i=lo+j;cand=sorted([{'id':int(t),'fragment':tok.decode([int(t)],skip_special_tokens=False),'probability':float(p),'mean_probability':float(lpm[j,t].exp()),'log_probability_lift_vs_mean':float(lp[j,t]-lpm[j,t])} for t,p in zip(pi[j],pv[j])],key=lambda x:(-x['probability'],x['id']));assert cand[9]['probability']>cand[-1]['probability'];top=cand[:20];ref=old[i,'identity']['top20'];records.append({'index':i,'position_uid':rr[i]['position_uid'],'condition':name,'NLL':float(nll[j]),'KL_full':float(kl[j]),'entropy':float(ent[j]),'target_rank':int(rank[j]),'target_probability':float(prob[j,yy[j]]),'target_NLL_improvement_vs_mean':old[i,'mean_only']['NLL']-float(nll[j]),'top1_agreement':top[0]['id']==ref[0]['id'],'top10_recovery':len({x['id'] for x in top[:10]}&{x['id'] for x in ref[:10]})/10,'top1_correct':top[0]['id']==int(yy[j]),'format_mass':float(massfmt[j]),'lexical_mass':float(lex[j]),'expected_log_frequency':float(elog[j]),'frequency_mass':[float(x) for x in freqmass[j]],'centered_energy_fraction':float(np.sum((hp[j]-mu)**2)/np.sum((A[i]-mu)**2)),'shuffle_eligible':bool(elig[i]),'shuffle_source_index':int(per[i]) if elig[i] else None,'same_token_other_document_NLL':float(snll[j]) if elig[i] else None,'real_context_NLL_gain':float(snll[j]-nll[j]) if elig[i] else None,'top20':top})
  dump(path,{'records':records})
  if lo%160==0:print('positions',hi,'elapsed',time.time()-start,flush=True)
 dump(E/'terminal_receipt.json',{'status':'COMPLETE','all_positions_including_auxiliary':737,'primary_natural_positions':700,'conditions':11,'control_eligible_positions':int(elig.sum()),'new_transformer_forwards':0,'training_updates':0,'elapsed_seconds':time.time()-start,'peak_GPU_bytes':torch.cuda.max_memory_allocated(),'device_used':[0]});print('COMPLETE',flush=True)
if __name__=='__main__':
 try:main()
 except Exception:dump(E/'provenance/failure.json',{'traceback':traceback.format_exc()});raise
