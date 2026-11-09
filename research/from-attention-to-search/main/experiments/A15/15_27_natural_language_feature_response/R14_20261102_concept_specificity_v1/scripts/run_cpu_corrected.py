"""CPU BF16 inference adaptation; identical frozen tensors/equations, 2 threads, new smoke required."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import sys,json,time,gc,hashlib,datetime
import numpy as np
import torch
import transformers.utils as hfu, transformers.utils.import_utils as hfi
for mod in [hfu,hfi]:
 mod.is_flash_attn_2_available=lambda:False
 mod.is_flash_attn_3_available=lambda:False
 mod.is_torchvision_available=lambda:False
 mod.is_librosa_available=lambda:False
from transformers import AutoModelForCausalLM
from tokenizers import Tokenizer
E=Path(__file__).resolve().parents[1];CC=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
def rows(p):return [json.loads(x) for x in Path(p).read_text().splitlines() if x]
def dump(p,x):
 p=Path(p);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n');tmp.replace(p)
def save(p,**x):
 p=Path(p);tmp=p.with_suffix('.tmp')
 with tmp.open('wb') as f:np.savez_compressed(f,**x)
 tmp.replace(p)
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
@torch.inference_mode()
def main():
 patch=json.load(open(E/'audit/upper_name_correction_patch.json'));parent=Path(patch['parent_root']);affected=np.array(patch['affected_position_indices']);affected_set=set(affected.tolist());affected_prefix=set(patch['affected_prefixes']);first_changed=np.array([i for i,r in enumerate(rows(E/'data/prefixes.jsonl')) if r['prefix_id'] in affected_prefix]);
 t0=time.time();torch.set_num_threads(2);torch.manual_seed(1102);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 assert torch.get_num_threads()==2
 freeze=json.load(open(E/'freeze.json'))
 for p,h in freeze['sha256'].items():assert sha(p)==h,('freeze mismatch',p)
 cfg=json.load(open(E/'config.json'));M=Path(cfg['model']);assert sha(M/'model.safetensors')==freeze['model_hash_expected'];assert sha(cfg['crosscoder_checkpoint'])==freeze['crosscoder_hash_expected'];model=AutoModelForCausalLM.from_pretrained(str(M),torch_dtype=torch.bfloat16,attn_implementation='sdpa',local_files_only=True).cpu().eval().requires_grad_(False);model.config.use_cache=False
 assert model.lm_head.weight.data_ptr()==model.model.embed_tokens.weight.data_ptr()
 sys.path.insert(0,str(CC));from crosscoder.model import CrossCoderConfig
 from crosscoder.fast_batchtopk_a21 import FastBatchTopKCrossCoder
 from crosscoder.batchtopk_a18 import CenteredRMSStats
 cp=torch.load(cfg['crosscoder_checkpoint'],map_location='cpu',weights_only=False,mmap=True)
 cc=FastBatchTopKCrossCoder(CrossCoderConfig(n_layers=14,hidden_size=1024,dict_size=16384,init_encoder_norm=1/np.sqrt(14)),device='meta',compute_dtype='bfloat16');cc.load_state_dict(cp['crosscoder'],assign=True,strict=True);cc=cc.cpu().eval().requires_grad_(False)
 # The original class guards its BF16 TRAIN path to CUDA. This read-only CPU path implements the SAME autocast BF16 expression and frozen threshold, then must pass new native smoke.
 import types
 cc._gemm_context=types.MethodType(lambda self,x: torch.autocast(device_type='cpu',dtype=torch.bfloat16),cc)
 stats=CenteredRMSStats.from_state_dict(cp['normalization']);del cp;gc.collect();threshold=float(cc.threshold);assert abs(threshold-.051281172782182693)<1e-12
 buffers={k:v.clone() for k,v in cc.named_buffers()};normweights=cc.decoder_norm_weights().detach()
 rawD=cc.decoder[-1].float()*float(stats.rms[-1]);bias=cc.decoder_bias[-1].float()*float(stats.rms[-1])+stats.train_mean[-1].to('cpu',torch.float32)
 np.savez(E/'data/decoder_last_scale.npz',D=rawD.cpu().numpy(),bias=bias.cpu().numpy(),cc_mean=stats.train_mean[-1].numpy(),cc_rms=stats.rms.numpy())
 pos=rows(E/'data/positions.jsonl');prefixes=rows(E/'data/prefixes.jsonl');seq=rows(E/'data/sequences.jsonl');conds=json.load(open(E/'data/conditions.json'));groups=json.load(open(E/'data/feature_groups.json'));B=np.load(E/'data/bases.npz');mu=B['mean'];V=B['V'];N=len(pos);tok=Tokenizer.from_file(str(M/'tokenizer.json'))
 wanted=np.array([[p['target_id']]*4 for p in pos],np.int64);first=[]
 for r in prefixes:
  ix=r['candidate_map']['U']['position_indices'][0];first.append(ix);wanted[ix]=[r['candidate_map'][k]['token_ids'][0] for k in ['U','V','A','B']]
 np.save(E/'data/wanted_token_ids.npy',wanted)
 def head(x):return model.lm_head(model.model.norm(x.to(torch.bfloat16))).float()
 def head_fixed(x):
  # All actual/smoke head conditions use the same fixed row shape, including last short chunk.
  n=len(x);xx=torch.zeros((256,1024),device='cpu',dtype=torch.bfloat16);xx[:n]=x.to(torch.bfloat16);return head(xx)[:n]
 def forward(s,cut=None,native=False):
  ids=s['token_ids'];assert len(ids)<256
  x=torch.zeros((1,256),device='cpu',dtype=torch.long);x[0,:len(ids)]=torch.tensor(ids,device='cpu');mask=torch.zeros_like(x);mask[:,:len(ids)]=1
  if cut is not None:x[:,cut+1:]=0;mask[:,cut+1:]=0
  cap={};handles=[]
  for j,layer in enumerate(cfg['layers']):
   def hook(m,a,y,k=j):cap[k]=(y[0] if isinstance(y,tuple) else y)[0].detach()
   handles.append(model.model.layers[layer].register_forward_hook(hook))
  try:
   y=model(input_ids=x,attention_mask=mask,use_cache=False,return_dict=True) if native else model.model(input_ids=x,attention_mask=mask,use_cache=False,return_dict=True)
   hh=torch.stack([cap[k] for k in range(14)],1).float();return hh,(y.logits[0].float() if native else None)
  finally:
   for h in handles:h.remove()
 def encode(h):
  n=len(h);xx=torch.zeros((1024,14,1024),device='cpu',dtype=torch.float32);xx[:n]=stats.normalize(h)
  u=cc._post_relu(xx);return (u*(u.float()*normweights>cc.threshold))[:n].float()
 # New-task smoke only; inherited legacy/source checks are not rerun.
 smokefile=E/'audit/03_implementation_numerics.json'
 if not smokefile.exists():
  checks=[]
  for domain in ['biology','mathematics','physics']:
   s=next(x for x in seq if x['sequence_id'].startswith(domain+'_01_p0_A_') and x['sequence_id'].endswith('_A'))
   hh,native=forward(s,native=True);hh2,_=forward(s);pr=next(r for r in prefixes if r['prefix_id']==s['prefix_id']);firstix=pr['candidate_map']['U']['position_indices'][0];inds=[len(pr['prefix_token_ids'])-1]+[p for p,ix in s['selected']];h=hh[inds,-1];ix=[firstix]+[i for p,i in s['selected']];orig=head_fixed(h);repeat=head_fixed(h.clone());hp=mu+(h.cpu().numpy().astype(np.float64)-mu)@V@V.T;ident=head_fixed(torch.tensor(hp,device='cpu'))
   lp=torch.log_softmax(orig,1);nlp=torch.log_softmax(native[inds],1);yy=torch.tensor([wanted[ix[0],2]]+[pos[i]['target_id'] for i in ix[1:]],device='cpu');ii=torch.arange(len(ix),device='cpu')
   causal,_=forward(s,cut=inds[0]);z=encode(hh[inds]);z2=encode(hh[inds]);recon=z@rawD+bias;res=h-recon
   native_cc=stats.inverse(cc.decode(z).float())[:,-1]
   e={'domain':domain,'native_head_logit_max':float(abs(orig-native[inds]).max()),'native_target_logprob_max':float(abs(lp[ii,yy]-nlp[ii,yy]).max()),'all_pc_logit_max':float(abs(orig-ident).max()),'identity_logit_max':float(abs(orig-repeat).max()),'fresh_cache_h_max':float(abs(hh-hh2).max()),'causal_visible_h_max':float(abs(hh[inds[0]]-causal[inds[0]]).max()),'cc_replay_max':float(abs(z-z2).max()),'linear_reconstruction_residual_max':float(abs(recon+res-h).max()),'native_CC_vs_FP32_linear_reconstruction_relative':float((native_cc-recon).norm()/recon.norm()),'empty_group_h_max':float(abs(h-(h-z[:,:0]@rawD[:0])).max()),'threshold':threshold}
   e['pass']=e['identity_logit_max']==0 and e['all_pc_logit_max']==0 and e['fresh_cache_h_max']==0 and e['causal_visible_h_max']==0 and e['cc_replay_max']==0 and e['empty_group_h_max']==0 and e['native_head_logit_max']<=.5 and e['native_target_logprob_max']<=.05 and e['linear_reconstruction_residual_max']<=1e-4
   checks.append(e)
  dump(smokefile,{'pass':all(x['pass'] for x in checks),'checks':checks,'time':now(),'threshold_frozen':threshold,'device':'CPU BF16, two threads','dtype':'BF16 forward/head; FP64 spectral;FP32 probability and raw decoder contributions','training_updates':0})
  print('SMOKE',json.dumps(checks),flush=True)
 assert json.load(open(smokefile))['pass'],'New-text CPU smoke failed; do not score evaluation'
 if '--smoke-only' in sys.argv:
  print('CPU_SMOKE_ONLY_COMPLETE',time.time()-t0,flush=True);return
 # Cache only selected causal states, never an intervened transformer cache.
 if not (E/'cache/merged.npz').exists():
  for i,s in enumerate(seq):
   path=E/'cache'/(s['sequence_id']+'.npz')
   if path.exists() or not s['selected']:continue
   hh,_=forward(s);selected=[j for j,ix in s['selected']];indices=[ix for j,ix in s['selected']]
   save(path,h14=hh[selected].cpu().numpy(),indices=np.array(indices),input_ids=np.array(s['token_ids']),freeze_sha256=np.array(sha(E/'freeze.json')))
   if i%96==0:print(json.dumps({'cache_sequences':i+1,'total':len(seq),'elapsed':time.time()-t0}),flush=True)
  H=np.zeros((N,14,1024),np.float32);seen=np.zeros(N,int)
  for s in seq:
   if not s['selected']:continue
   a=np.load(E/'cache'/(s['sequence_id']+'.npz'));assert str(a['freeze_sha256']) in [sha(E/'freeze.json'),patch['parent_freeze_sha256']];assert np.array_equal(a['input_ids'],s['token_ids']);assert np.array_equal(a['indices'],[ix for j,ix in s['selected']]);H[a['indices']]=a['h14'];seen[a['indices']]+=1
  assert np.all(seen==1);zs=[]
  for lo in range(0,N,1024):zs.append(encode(torch.tensor(H[lo:lo+1024],device='cpu')).cpu().numpy())
  Z=np.concatenate(zs);oldmerged=np.load(parent/'cache/merged.npz');unchanged=np.array([i for i in range(N) if i not in affected_set]);assert np.array_equal(H[unchanged,-1],oldmerged['h'][unchanged]);assert np.array_equal(Z[unchanged],oldmerged['z'][unchanged]);dump(E/'audit/corrected_cache_reuse.json',{'unaffected_positions':len(unchanged),'affected_positions':len(affected),'unaffected_h_bit_exact':True,'unaffected_z_bit_exact':True,'legacy_cache_input_ids_and_indices_checked':True,'parent_freeze':patch['parent_freeze_sha256']});save(E/'cache/merged.npz',h=H[:,-1],z=Z)
  # last-layer raw vectors, separately kept; signs and cross terms remain recoverable.
  vectors={};support=[]
  zg=torch.tensor(Z,device='cpu')
  for name,members in groups.items():
   if name in ['zero_reference','insufficient_positive'] or name.startswith('random') or name in ['low','middle','high']:
    v=zg[:,members]@rawD[members];vectors[name]=v.cpu().numpy()
    support.append({'group':name,'members':len(members),'positive_positions':int((zg[:,members]>0).any(1).sum()),'activation_instances':int((zg[:,members]>0).sum()),'coefficient_sum':float(zg[:,members].sum())})
  save(E/'cache/vectors.npz',**vectors,reconstruction=(zg@rawD+bias).cpu().numpy())
  dump(E/'analysis/feature_support.json',support)
  H27=H[:,-1];sumv=sum(vectors[n] for n in ['low','middle','high','zero_reference','insufficient_positive'])+bias.cpu().numpy();reconstruction=(zg@rawD+bias).cpu().numpy()
  dump(E/'audit/decomposition.json',{'max_group_additivity_abs':float(abs(sumv-reconstruction).max()),'max_group_additivity_relative':float(np.linalg.norm(sumv-reconstruction)/np.linalg.norm(reconstruction)),'NMSE_mean':float(np.mean(np.sum((H27-reconstruction)**2,1)/np.sum(H27**2,1))),'residual_retained_in_group_delete':True,'dict_mean':stats.train_mean[-1].cpu().tolist(),'dict_rms':stats.rms.cpu().tolist()})
  del H,zg,Z;gc.collect()
 cache=np.load(E/'cache/merged.npz');h0=cache['h'].astype(np.float64);vv=np.load(E/'cache/vectors.npz');center=h0-mu;pc=center@V;lookup={x['condition']:x for x in conds['unique']}
 def projection(hc,Q):return hc@Q@Q.T
 def vector(c):
  kind=c['kind']
  if kind=='identity':return h0
  if kind in ['keep','delete']:
   Q=V[:,c['pc']];v=pc[:,c['pc']]@Q.T
   return mu+v if kind=='keep' else h0-v
  if kind in ['random_keep','random_delete']:
   Q=B[f'random_{c["seed"]}'][:,:c['rank']];v=projection(center,Q);return mu+v if kind=='random_keep' else h0-v
  if kind=='random_append':
   Q=B[f'orthogonal_{c["seed"]}'][:,:c['rank']];return mu+pc[:,:16]@V[:,:16].T+projection(center,Q)
  if kind=='spectral_normmatch':
   target=h0-vector(lookup[c['target']]);Q=B[f'random_{c["seed"]}'][:,:c['rank']];v=projection(center,Q)
  elif kind=='feature_delete':return h0-vv[c['group']].astype(np.float64)
  elif kind=='feature_normmatch':target=vv[c['target_group']].astype(np.float64);v=vv[c['group']].astype(np.float64)
  elif kind=='reconstruct':return vv['reconstruction'].astype(np.float64)
  else:raise ValueError(kind)
  den=np.linalg.norm(v,axis=1);num=np.linalg.norm(target,axis=1);scale=np.divide(num,den,out=np.zeros_like(num),where=den>0)
  zero_log.append({'condition':c['condition'],'zero_random':int(np.sum(den==0)),'unmatched_nonzero_target':int(np.sum((den==0)&(num>0))),'max_scale':float(scale.max()),'norm_mismatch_max':float(np.max(abs(np.linalg.norm(v*scale[:,None],axis=1)-num)))})
  return h0-v*scale[:,None]
 # First-answer reference distributions only, small enough for CPU storage and chunked GPU replay.
 freq=np.load(E.parent/'R13_20261101_native_spectral_decoding/data/frequency.npz');valid=torch.tensor(freq['valid'],device='cpu');lf=torch.tensor(freq['logfreq'],device='cpu',dtype=torch.float32);fg=torch.tensor(freq['group'],device='cpu');fmt=torch.tensor(freq['format_mask'],device='cpu');first=np.array(first);first_lookup={ix:j for j,ix in enumerate(first)}
 refpath=E/'cache/full_first_logp.npy'
 if not refpath.exists():
  arr=[]
  for lo in range(0,len(first),256):arr.append(torch.log_softmax(head_fixed(torch.tensor(h0[first[lo:lo+256]],device='cpu')),1).cpu().numpy())
  np.save(refpath,np.concatenate(arr))
 special_ids=[x['id'] for x in json.load(open(M/'tokenizer.json'))['added_tokens'] if x.get('special') and x['id']<model.config.vocab_size];special_mask=torch.zeros(model.config.vocab_size,device='cpu',dtype=torch.bool);special_mask[special_ids]=True;invalid_mask=(~valid)&(~special_mask)
 reflp=np.load(refpath,mmap_mode='r');oldref=np.load(parent/'cache/full_first_logp.npy',mmap_mode='r');unchanged_first=np.array([i for i in range(len(first)) if i not in set(first_changed)]);assert np.array_equal(reflp[unchanged_first],oldref[unchanged_first]);zero_log=[]
 for ci,c in enumerate(conds['unique']):
  name=c['condition'];dest=E/'analysis'/f'condition_{name}.npz'
  if dest.exists():continue
  hv=vector(c);assert np.isfinite(hv).all();old=np.load(parent/'analysis'/f'condition_{name}.npz');lpwanted=old['logp'].copy();diag=old['first_diagnostics'].copy();toprows={r['prefix_id']:r for r in rows(parent/'analysis'/f'top_{name}.jsonl')}
  # Candidate scores: every position, same fixed row shape for all conditions.
  for lo in range(0,len(affected),256):
   ix=affected[lo:lo+256];lp=torch.log_softmax(head_fixed(torch.tensor(hv[ix],device='cpu')),1);ii=torch.arange(len(ix),device='cpu')[:,None];wantedg=torch.tensor(wanted[ix],device='cpu');lpwanted[ix]=lp[ii,wantedg].cpu().numpy()
  # Whole vocabulary diagnostics at first-answer positions only.
  for lo in range(0,len(first_changed),256):
   selection=first_changed[lo:lo+256];ix=first[selection];lp=torch.log_softmax(head_fixed(torch.tensor(hv[ix],device='cpu')),1);prob=lp.exp();full_lp=torch.tensor(reflp[selection],device='cpu');full_p=full_lp.exp();kl=(full_p*(full_lp-lp)).sum(1);entropy=-(prob*lp).sum(1);lexmass=prob[:,valid].sum(1);logfreq=(prob*lf).sum(1)/lexmass.clamp_min(1e-12);common=prob[:,fg==0].sum(1);fmass=prob[:,fmt].sum(1)
   # Stable, complete tie handling on CPU at the cut boundary.
   lp_cpu=lp.cpu().numpy()
   for j,index in enumerate(ix):
    a=lp_cpu[j];boundary=np.partition(a,-20)[-20];cand=np.flatnonzero(a>=boundary);order=np.lexsort((cand,-a[cand]));ids=cand[order[:20]]
    tops=[{'token_number':int(k),'fragment':tok.decode([int(k)],skip_special_tokens=False),'probability':float(np.exp(a[k]))} for k in ids]
    diag[selection[j]]=[int(index),float(kl[j]),float(entropy[j]),float(logfreq[j]),float(common[j]),float(fmass[j]),float(prob[j,special_mask].sum()),float(prob[j,invalid_mask].sum())];toprows[prefixes[selection[j]]['prefix_id']]={'prefix_id':prefixes[selection[j]]['prefix_id'],'condition':name,'top20':tops}
  actual=torch.tensor(hv).bfloat16().float().numpy().astype(np.float64);delta=h0-hv;save(dest,applied_perturbation_norm=np.linalg.norm(h0-actual,axis=1),applied_h_norm=np.linalg.norm(actual,axis=1),intended_vs_applied_h_norm=np.linalg.norm(actual-hv,axis=1),logp=lpwanted,first_diagnostics=np.array(diag),perturbation_norm=np.linalg.norm(delta,axis=1),h_norm=np.linalg.norm(hv,axis=1),energy_fraction=np.sum((hv-mu)**2,1)/np.sum(center**2,1))
  (E/'analysis'/f'top_{name}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in [toprows[q['prefix_id']] for q in prefixes]))
  dump(E/'progress.json',{'time':now(),'completed_conditions':ci+1,'conditions':len(conds['unique']),'elapsed':time.time()-t0,'last':name,'peak_GPU_bytes':0});print('CONDITION',ci+1,len(conds['unique']),name,round(time.time()-t0,1),flush=True)
 dump(E/'audit/norm_matching.json',zero_log)
 assert all(torch.equal(v,buffers[k]) for k,v in cc.named_buffers())
 assert all(not p.requires_grad and p.grad is None for obj in [model,cc] for p in obj.parameters())
 dump(E/'terminal_receipt.json',{'status':'ALL_CONDITIONS_COMPLETE','time':now(),'positions':N,'prefixes':len(prefixes),'conditions':len(conds['unique']),'sequences_cached':len(list((E/'cache').glob('*_U.npz')))+len(list((E/'cache').glob('*_V.npz')))+len(list((E/'cache').glob('*_A.npz')))+len(list((E/'cache').glob('*_B.npz'))),'elapsed_seconds':time.time()-t0,'peak_GPU_bytes':0,'GPUs_actually_used':0,'allocated_profile':'EXISTING_LOCAL_CPU_2_THREADS','torch':torch.__version__,'transformers':__import__('transformers').__version__,'new_training':0,'data_version':'1.3','new_model_sequences_this_revision':len(patch['affected_sequences']),'reused_unchanged_model_sequences':1152-len(patch['affected_sequences']),'parent_version':'1.2','parent_root':str(parent),'optimizer':None,'buffers_unchanged':True})
if __name__=='__main__':main()
