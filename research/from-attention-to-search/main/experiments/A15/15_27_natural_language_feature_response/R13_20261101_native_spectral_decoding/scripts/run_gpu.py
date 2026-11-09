"""Frozen native decoder; cached vectors only after full-model smoke. No optimizer/training."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,time,hashlib,sys,traceback,datetime,argparse
import numpy as np
import torch
import transformers.utils as hfutils
import transformers.utils.import_utils as hfimports
# SDPA only; do not import the base image optional FlashAttention extension.
for mod in [hfutils,hfimports]:
 mod.is_flash_attn_2_available=lambda:False
 mod.is_flash_attn_3_available=lambda:False
 mod.is_torchvision_available=lambda:False
 mod.is_librosa_available=lambda:False
from transformers import AutoModelForCausalLM
from tokenizers import Tokenizer
E=Path(__file__).resolve().parents[1];M=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official');R=E.parent/'R11_three_domain_replication_20261030/qualified_three_domain_A02'
def dump(p,x):
 p=Path(p);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n');tmp.replace(p)
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for a in iter(lambda:f.read(8<<20),b''):h.update(a)
 return h.hexdigest()
def rows(p):return [json.loads(l) for l in Path(p).read_text().splitlines() if l]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
@torch.inference_mode()
def main():
 start=time.time();torch.set_num_threads(2);torch.manual_seed(20261101);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 assert torch.cuda.is_available() and '5090' in torch.cuda.get_device_name(0),'RTX5090 required; no H100 fallback'
 assert 'sm_120' in torch.cuda.get_arch_list();assert os.environ.get('RESOURCE_PROFILE')=='5090-2-spot'
 freeze=json.load(open(E/'freeze.json'))
 for p,h in freeze['sha256'].items():assert sha(p)==h,('changed after freeze',p)
 manifest=json.load(open(E/'manifest.json'));assert sha(M/'model.safetensors')==manifest['input_sha256'][str(M/'model.safetensors')]
 model=AutoModelForCausalLM.from_pretrained(str(M),local_files_only=True,trust_remote_code=False,torch_dtype=torch.bfloat16,attn_implementation='sdpa').cuda().eval().requires_grad_(False);model.config.use_cache=False
 assert model.lm_head.weight.data_ptr()==model.model.embed_tokens.weight.data_ptr(),'expected tied official head'
 tok=Tokenizer.from_file(str(M/'tokenizer.json'));A=np.load(E/'data/h.npy');B=np.load(E/'data/bases.npz');mu=B['mean'];V=B['V'];rr=rows(E/'data/positions.jsonl');doc={x['seq_id']:x for x in rows(R/'data/documents.jsonl')}
 def decode(h):return model.lm_head(model.model.norm(h)).float()
 # Legacy cache failed the unchanged native replay gate. Refresh SAME model/hook/input on current5090 runtime.
 freshdir=E/'data/native_h27_fresh';freshdir.mkdir(exist_ok=True);fresh_calls=0
 for ordinal,sid in enumerate(sorted({r['seq_id'] for r in rr})):
  path=freshdir/(sid+'.npz')
  if path.exists():continue
  x=torch.zeros((1,256),dtype=torch.long,device='cuda');x[0,:192]=torch.tensor(doc[sid]['token_ids'],device='cuda');mask=torch.zeros_like(x);mask[:,:192]=1;cap={}
  def capture(m,a,y):cap['h']=(y[0] if isinstance(y,tuple) else y).detach()
  handle=model.model.layers[27].register_forward_hook(capture)
  model.model(input_ids=x,attention_mask=mask,position_ids=torch.arange(256,device='cuda')[None],use_cache=False,return_dict=True)
  hh=cap['h'][0,:192].float().cpu().numpy();handle.remove();tmp=path.with_suffix('.tmp')
  with tmp.open('wb') as stream:np.savez_compressed(stream,h27=hh,token_ids=np.array(doc[sid]['token_ids'],np.int32))
  tmp.replace(path);fresh_calls+=1
  if ordinal%30==0:print(json.dumps({'fresh_cache_documents':ordinal+1,'total':180,'elapsed_seconds':time.time()-start}),flush=True)
 A=np.stack([np.load(freshdir/(r['seq_id']+'.npz'))['h27'][r['position']].astype(np.float64) for r in rr]);np.save(E/'data/fresh_h.npy',A)
 dump(E/'data/fresh_cache_manifest.json',{'source':'same official checkpoint, block27 residual-post, BF16 SDPA fixed1x256/mask192, currentRTX5090','documents':180,'positions_selected':len(rr),'new_transformer_forwards_this_attempt':fresh_calls,'model_sha256':manifest['input_sha256'][str(M/'model.safetensors')],'producer_sha256':sha(__file__),'selected_h_sha256':sha(E/'data/fresh_h.npy'),'old_cache_status':'INELIGIBLE_NATIVE_REPLAY; preserved, not primary decoder input','PCA':'original fixed TRAIN mean/basis unchanged; no new fit'})
 fullpc=mu+(A-mu)@V@V.T;assert np.max(abs(fullpc-A))<1e-8
 cast_equal=torch.equal(torch.tensor(fullpc).bfloat16(),torch.tensor(A).bfloat16())
 allpc_logit_error=0.;allpc_nll_error=0.
 for lo in range(0,len(A),16):
  hi=min(lo+16,len(A));orig=decode(torch.tensor(A[lo:hi],device='cuda',dtype=torch.bfloat16));reco=decode(torch.tensor(fullpc[lo:hi],device='cuda',dtype=torch.bfloat16));allpc_logit_error=max(allpc_logit_error,float(abs(orig-reco).max()));yy=torch.tensor([x['target_id'] for x in rr[lo:hi]],device='cuda');ii=torch.arange(hi-lo,device='cuda');allpc_nll_error=max(allpc_nll_error,float(abs(torch.log_softmax(orig,1)[ii,yy]-torch.log_softmax(reco,1)[ii,yy]).max()))
 assert allpc_logit_error<=1e-4 and allpc_nll_error<=1e-6,('all-PC decoder error',allpc_logit_error,allpc_nll_error)
 smoke=[]
 # Same-input shape and causal-prefix forward, target IDs manually audited on CPU.
 for sid in ['R11_A02_090','R11_A02_292',manifest['fixed_examples'][-2]]:
  r=next(x for x in rr if x['seq_id']==sid and x['panel']=='the');t=r['position'];ids=doc[sid]['token_ids'];x=torch.zeros((1,256),dtype=torch.long,device='cuda');x[0,:192]=torch.tensor(ids,device='cuda');mask=torch.zeros_like(x);mask[:,:192]=1;cap={}
  def hook(m,a,y):cap['h']=(y[0] if isinstance(y,tuple) else y).detach()
  hh=model.model.layers[27].register_forward_hook(hook)
  out=model(input_ids=x,attention_mask=mask,position_ids=torch.arange(256,device='cuda')[None],use_cache=False,return_dict=True);native=out.logits[0,t].float().clone();fresh=cap['h'][0,t].clone();direct=decode(fresh[None])[0];saved=torch.tensor(np.load(freshdir/(sid+'.npz'))['h27'][t],device='cuda',dtype=torch.bfloat16);cached=decode(saved[None])[0]
  # model lm_head GEMM matrix shape versus single-row decode can differ in BF16.
  e={'seq_id':sid,'position':t,'target_id':r['target_id'],'native_vs_hook_head_max_logits':float(abs(native-direct).max()),'cache_h_relative_L2':float(torch.linalg.vector_norm(fresh.float()-saved.float())/torch.linalg.vector_norm(saved.float())),'cache_h_max_abs':float(abs(fresh.float()-saved.float()).max()),'cache_head_max_logits':float(abs(cached-direct).max()),'cache_NLL_abs':float(abs(torch.log_softmax(cached,0)[r['target_id']]-torch.log_softmax(direct,0)[r['target_id']]))}
  xp=x.clone();xp[:,t+1:]=0;mp=torch.zeros_like(mask);mp[:,:t+1]=1;prefix=model(input_ids=xp,attention_mask=mp,position_ids=torch.arange(256,device='cuda')[None],use_cache=False,return_dict=True);prefixlog=prefix.logits[0,t].float();e['causal_prefix_max_logits']=float(abs(prefixlog-native).max());e['causal_prefix_NLL_abs']=float(abs(torch.log_softmax(prefixlog,0)[r['target_id']]-torch.log_softmax(native,0)[r['target_id']]))
  h=saved[None];id1=decode(h);id2=decode(h.clone());e['identity_logits_max_abs']=float(abs(id1-id2).max());e['identity_NLL_abs']=float(abs(torch.log_softmax(id1,1)[0,r['target_id']]-torch.log_softmax(id2,1)[0,r['target_id']]))
  e['pass']=e['cache_h_relative_L2']<=.02 and e['cache_head_max_logits']<=.5 and e['cache_NLL_abs']<=.05 and e['causal_prefix_max_logits']<=.5 and e['causal_prefix_NLL_abs']<=.05 and e['native_vs_hook_head_max_logits']<=.5 and e['identity_logits_max_abs']==0 and e['identity_NLL_abs']==0
  smoke.append(e);hh.remove();del out,prefix
 dump(E/'audit/03_implementation_numerics.json',{'timestamp':now(),'pass':all(x['pass'] for x in smoke),'smoke':smoke,'all_PC_FP64_max_abs':float(np.max(abs(fullpc-A))),'all_PC_cast_exact':cast_equal,'all_PC_logit_max_abs':allpc_logit_error,'all_PC_NLL_max_abs':allpc_nll_error,'training_updates':0,'trainable_parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),'optimizer':None,'precision':'native BF16, FP64 projection, float32 softmax metrics','device':torch.cuda.get_device_name(0),'visible_device_count':torch.cuda.device_count(),'torch':torch.__version__,'transformers':__import__('transformers').__version__,'source_freeze_verified':True})
 print('SMOKE',json.dumps(smoke),flush=True)
 assert all(x['pass'] for x in smoke),'smoke failed; main decoding stopped'
 # Only cache-derived h beyond this point. Never store N*condition*vocabulary distributions.
 f=np.load(E/'data/frequency.npz');valid=torch.tensor(f['valid'],device='cuda');lf=torch.tensor(f['logfreq'],device='cuda',dtype=torch.float32);group=torch.tensor(f['group'],device='cuda');fmt=torch.tensor(f['format_mask'],device='cuda');conditions=[x['condition'] for x in manifest['conditions']]
 target=torch.tensor([r['target_id'] for r in rr],device='cuda');chunks=E/'analysis/chunks';chunks.mkdir(exist_ok=True);batch=16
 for lo in range(0,len(rr),batch):
  hi=min(lo+batch,len(rr));path=chunks/f'{lo:06d}_{hi:06d}.json'
  if path.exists():continue
  hh=torch.tensor(A[lo:hi],device='cuda',dtype=torch.bfloat16);full=decode(hh);flp=torch.log_softmax(full,dim=1);fp=flp.exp();ftop=full.topk(10,1).indices;yy=target[lo:hi];idx=torch.arange(hi-lo,device='cuda');records=[]
  for name in conditions:
   Q=B[name] if name!='identity' else None
   if Q is not None:assert np.max(abs(Q.T@Q-np.eye(Q.shape[1])) ,initial=0)<1e-10
   projected=A[lo:hi] if name=='identity' else mu+(A[lo:hi]-mu)@Q@Q.T
   h=torch.tensor(projected,device='cuda',dtype=torch.bfloat16);logits=decode(h);lp=torch.log_softmax(logits,1);prob=lp.exp();val,ind=prob.topk(20,1);nll=-lp[idx,yy];kl=(fp*(flp-lp)).sum(1);entropy=-(prob*lp).sum(1);lexmass=prob[:,valid].sum(1);expected=(prob*lf).sum(1)/lexmass.clamp_min(1e-12)
   gm=torch.stack([prob[:,group==j].sum(1) for j in range(4)],dim=1);top10=((ind[:,:10,:,None] if False else ind[:,:10,None])==ftop[:,None,:]).any(2).float().mean(1);ranks=(logits>logits[idx,yy,None]).sum(1)+1
   # normalize from the actual BF16 intervention entering native norm/head.
   actual=h.float();original=hh.float();centered=actual-torch.tensor(mu,device='cuda',dtype=torch.float32)
   norm=torch.linalg.vector_norm(actual,dim=1);energy=centered.square().sum(1)/(original-torch.tensor(mu,device='cuda',dtype=torch.float32)).square().sum(1)
   for j in range(hi-lo):
    row={'index':lo+j,'position_uid':rr[lo+j]['position_uid'],'condition':name,'NLL':float(nll[j]),'KL_full':float(kl[j]),'entropy':float(entropy[j]),'top1_agreement':bool(ind[j,0]==ftop[j,0]),'top10_recovery':float(top10[j]),'target_probability':float(prob[j,yy[j]]),'target_rank':int(ranks[j]),'top1_correct':bool(ind[j,0]==yy[j]),'lexical_mass':float(lexmass[j]),'format_mass':float(prob[j,fmt].sum()),'format_mass':float(prob[j,fmt].sum()),'expected_log_frequency':float(expected[j]),'h_norm':float(norm[j]),'centered_energy_fraction':float(energy[j]),'frequency_mass':[float(x) for x in gm[j]],'top20':[{'id':int(ii),'fragment':tok.decode([int(ii)],skip_special_tokens=False),'probability':float(pp)} for ii,pp in zip(ind[j],val[j])]}
    records.append(row)
  dump(path,{'lo':lo,'hi':hi,'records':records})
  if lo%80==0:print(json.dumps({'positions_completed':hi,'total':len(rr),'elapsed_seconds':time.time()-start,'peak_GPU_bytes':torch.cuda.max_memory_allocated()}),flush=True)
 assert all(not p.requires_grad and p.grad is None for p in model.parameters())
 dump(E/'terminal_receipt.json',{'status':'NUMERIC_FORWARD_COMPLETE','time_utc':now(),'positions':len(rr),'documents':len(set(r['seq_id'] for r in rr)),'conditions':len(conditions),'elapsed_seconds':time.time()-start,'peak_GPU_bytes':torch.cuda.max_memory_allocated(),'reserved_GPU_bytes':torch.cuda.max_memory_reserved(),'device_used':[0],'profile':'5090-2-spot','training_updates':0,'model_forward_calls_smoke':6,'fresh_cache_forward_calls_this_attempt':fresh_calls,'fresh_cache_documents':180,'cache_input':'data/fresh_h.npy','new_training':False})
 print('COMPLETE',json.dumps(json.load(open(E/'terminal_receipt.json'))),flush=True)
if __name__=='__main__':
 try:main()
 except Exception as exc:
  dump(E/'audit'/('failure_'+datetime.datetime.now().strftime('%Y%m%dT%H%M%S')+'.json'),{'time_utc':now(),'error':repr(exc),'traceback':traceback.format_exc()});raise
