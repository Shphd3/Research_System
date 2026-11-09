"""Frozen Qwen single-layer PCA interventions; no training, native suffix continuation."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,time,hashlib,traceback,argparse
import numpy as np
import torch
import transformers.utils as hu
import transformers.utils.import_utils as hi
for m in [hu,hi]:
 m.is_flash_attn_2_available=lambda:False;m.is_flash_attn_3_available=lambda:False;m.is_torchvision_available=lambda:False;m.is_librosa_available=lambda:False
from transformers import AutoModelForCausalLM
from tokenizers import Tokenizer
E=Path(__file__).resolve().parents[1];cfg=json.loads((E/'manifest.json').read_text());O=Path(cfg['parent_round']);M=Path(cfg['model_dir'])
def dump(p,x):
 p=Path(p);p.parent.mkdir(exist_ok=True,parents=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(x,ensure_ascii=False,allow_nan=False)+'\n');t.replace(p)
def rows(p):return [json.loads(l) for l in Path(p).read_text().splitlines()]
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for x in iter(lambda:f.read(8<<20),b''):h.update(x)
 return h.hexdigest()
def init(rank):
 torch.set_num_threads(2);torch.cuda.set_device(rank);torch.backends.cuda.matmul.allow_tf32=False;torch.manual_seed(20261105)
 assert os.environ.get('RESOURCE_PROFILE')=='5090-2-spot'
 assert '5090' in torch.cuda.get_device_name(rank)
 for p,h in json.loads((E/'freeze.json').read_text())['sha256'].items():assert sha(p)==h,('source freeze',p)
 for p,h in cfg['input_sha256'].items():assert sha(p)==h,('input changed',p)
 model=AutoModelForCausalLM.from_pretrained(str(M),local_files_only=True,trust_remote_code=False,torch_dtype=torch.bfloat16,attn_implementation='sdpa').to(f'cuda:{rank}').eval()
 for p in model.parameters():p.requires_grad_(False)
 assert model.config.num_hidden_layers==28 and model.config.hidden_size==1024
 return model
class Native:
 def __init__(self,m,rank):self.m=m;self.dev=f'cuda:{rank}';self.layers=m.model.layers;self.tok=Tokenizer.from_file(str(M/'tokenizer.json'))
 def inputs(self,doc,batch=1):
  x=torch.zeros((batch,256),dtype=torch.long,device=self.dev);x[:,:192]=torch.tensor(doc['token_ids'],device=self.dev);mask=torch.zeros_like(x);mask[:,:192]=1
  return x,mask
 def body(self,x,mask,start=0,emb=None):
  self.m.model.layers=torch.nn.ModuleList(list(self.layers)[start:])
  try:return self.m.model(input_ids=x if emb is None else None,inputs_embeds=emb,attention_mask=mask,position_ids=torch.arange(256,device=self.dev)[None].expand(mask.shape[0],-1),use_cache=False,return_dict=True).last_hidden_state
  finally:self.m.model.layers=self.layers
 def decode(self,y):
  # Fixed16-row GEMM matches R13 decoder shape; accepts arbitrary number of targets.
  result=[]
  for lo in range(0,len(y),16):
   a=y[lo:lo+16];z=torch.zeros((16,1024),device=self.dev,dtype=torch.bfloat16);z[:len(a)]=a;result.append(self.m.lm_head(z)[:len(a)].float())
  return torch.cat(result)
 def capture(self,doc):
  cap={};handles=[]
  for l in range(28):
   def hk(mod,a,y,l=l):cap[l]=(y[0] if isinstance(y,tuple) else y).detach().clone()
   handles.append(self.layers[l].register_forward_hook(hk))
  x,mask=self.inputs(doc)
  try:out=self.body(x,mask)
  finally:
   for h in handles:h.remove()
  return out,cap
 def metrics(self,logits,full,targets,indices):
  lp=logits.log_softmax(-1);flp=full.log_softmax(-1);p=lp.exp();fp=flp.exp();v,ids=p.topk(10,-1);fi=full.argmax(-1);ii=torch.arange(len(targets),device=self.dev);yy=torch.tensor(targets,device=self.dev);out=[]
  for j,ind in enumerate(indices):
   out.append({'index':ind,'top1_id':int(ids[j,0]),'top1_agreement':bool(ids[j,0]==fi[j]),'full_top1_probability':float(p[j,fi[j]]),'full_top1_rank':int((logits[j]>logits[j,fi[j]]).sum()+1),'target_probability':float(p[j,yy[j]]),'target_rank':int((logits[j]>logits[j,yy[j]]).sum()+1),'NLL':float(-lp[j,yy[j]]),'KL_full':float((fp[j]*(flp[j]-lp[j])).sum()),'entropy':float(-(p[j]*lp[j]).sum()),'top10':[{'id':int(k),'fragment':self.tok.decode([int(k)],skip_special_tokens=False),'probability':float(q)} for k,q in zip(ids[j],v[j])]})
  return out
 def project(self,h,mu,q):
  a=h.float()-mu;z=mu+(a@q)@q.T if q.shape[1] else mu.expand_as(a);return z.to(h.dtype)
def basis(l,dev):
 b=np.load(E/'data/bases'/f'layer{l+1:02d}.npz');return b,torch.tensor(b['mean'],device=dev,dtype=torch.float32),torch.tensor(b['V'][:,:64],device=dev,dtype=torch.float32)
@torch.inference_mode()
def fit(model,rank):
 n=Native(model,rank);docs=rows(E/'data/reference_documents.jsonl');outdir=E/'data/reference_cache';outdir.mkdir(exist_ok=True);start=time.time()
 for i,d in enumerate(docs):
  p=outdir/(d['seq_id']+'.npy')
  if p.exists():continue
  _,cap=n.capture(d);a=np.stack([cap[l][0,32:192].float().cpu().numpy() for l in range(28)]);tmp=p.with_suffix('.tmp')
  with tmp.open('wb') as f:np.save(f,a)
  tmp.replace(p)
  if i%10==0:print(json.dumps({'stage':'reference','documents':i+1,'total':60,'seconds':time.time()-start}),flush=True)
 (E/'data/bases').mkdir(exist_ok=True)
 for l in range(28):
  p=E/'data/bases'/f'layer{l+1:02d}.npz'
  if p.exists():continue
  # Native states are exactBF16 stored asFP32. Accumulate/center/eigh inFP64.
  H=torch.cat([torch.tensor(np.load(outdir/(d['seq_id']+'.npy'),mmap_mode='r')[l],device=n.dev,dtype=torch.float64) for d in docs]);mu=H.mean(0);X=H-mu;cov=X.T@X/(len(H)-1);ev,V=torch.linalg.eigh(cov);ev=ev.flip(0);V=V.flip(1);orth=float(abs(V.T@V-torch.eye(1024,device=n.dev)).max());assert orth<1e-10
  rec=float(abs(mu+(H[:8]-mu)@V@V.T-H[:8]).max());assert rec<1e-8
  vals=ev.cpu().numpy();tmp=p.with_suffix('.tmp')
  with tmp.open('wb') as f:np.savez(f,mean=mu.cpu().numpy(),V=V.cpu().numpy(),eigenvalues=vals,n=9600,orthogonality=orth,identity_max_abs=rec)
  tmp.replace(p);print(json.dumps({'stage':'PCA','layer':l+1,'rank':int((ev>ev[0]*np.finfo(float).eps*1024).sum()),'head64_variance':float(ev[:64].sum()/ev.sum()),'seconds':time.time()-start}),flush=True)
  del H,X,cov,ev,V
 # fixed random raw-coordinate subspaces are identical across layers, different TRAIN means.
 for seed in cfg['random_seeds']:
  q=np.linalg.qr(np.random.default_rng(seed).normal(size=(1024,64)),mode='reduced')[0];np.save(E/'data'/f'random{seed}.npy',q)
 dump(E/'data/pca_complete.json',{'layers':28,'documents':60,'positions':9600,'seconds':time.time()-start,'device':rank,'mean_variance':'per-layer raw residual centered','eval_used':False,'bases_sha256':{str(p):sha(p) for p in (E/'data/bases').glob('*.npz')}})
@torch.inference_mode()
def smoke(model,rank):
 n=Native(model,rank);docs=rows(E/'data/evaluation_documents.jsonl');rr=rows(E/'data/positions.jsonl');d=next(x for x in docs if x['seq_id']=='R11_A02_134');ind=next(i for i,r in enumerate(rr) if r['seq_id']==d['seq_id'] and r['position']==144);t=144;x,mask=n.inputs(d);y,cap=n.capture(d);full=n.decode(y[0,t:t+1]);checks=[]
 for l in range(28):
  b,mu,q=basis(l,n.dev);h=cap[l];v=torch.tensor(b['V'],device=n.dev,dtype=torch.float64);mm=torch.tensor(b['mean'],device=n.dev,dtype=torch.float64);reco=mm+(h.double()-mm)@v@v.T;err=float(abs(reco-h).max());cast=torch.equal(reco.bfloat16(),h);cast_rel=float(torch.linalg.vector_norm(reco.bfloat16().float()-h.float())/torch.linalg.vector_norm(h.float()));assert err<1e-8 and cast_rel<=1e-6,('full PC',l,err,cast,cast_rel)
  yy=n.body(None,mask,start=l+1,emb=h);lg=n.decode(yy[0,t:t+1]);e=float(abs(lg-full).max());ne=float(abs(lg.log_softmax(-1)[0,rr[ind]['target_id']]-full.log_softmax(-1)[0,rr[ind]['target_id']]));assert e<=.5 and ne<=.05,('no-op suffix',l,e,ne)
  checks.append({'layer':l+1,'fullPC_max_abs':err,'fullPC_cast_exact':cast,'fullPC_cast_relative_error':cast_rel,'suffix_noop_logits_max_abs':e,'suffix_noop_NLL_abs':ne})
  if l in [0,13,27]:
   for scope in cfg['scopes']:
    hh=h.clone();proj=n.project(h,mu,q)
    if scope=='all_prefix':hh[:,:192]=proj[:,:192]
    else:hh[:,t]=proj[:,t]
    sl=n.decode(n.body(None,mask,start=l+1,emb=hh)[0,t:t+1])
    def hook(mod,a,out):
     raw=out[0] if isinstance(out,tuple) else out;z=raw.clone();pp=n.project(raw,mu,q)
     if scope=='all_prefix':z[:,:192]=pp[:,:192]
     else:z[:,t]=pp[:,t]
     return (z,*out[1:]) if isinstance(out,tuple) else z
    handle=n.layers[l].register_forward_hook(hook)
    try:fl=n.decode(n.body(x,mask)[0,t:t+1])
    finally:handle.remove()
    le=float(abs(fl-sl).max());nn=float(abs(fl.log_softmax(-1)[0,rr[ind]['target_id']]-sl.log_softmax(-1)[0,rr[ind]['target_id']]));assert le<=.5 and nn<=.05,('hook vs suffix',l,scope,le,nn)
    checks[-1][scope]={'logits_max_abs':le,'NLL_abs':nn,'top1_equal':bool(fl.argmax()==sl.argmax())};assert fl.argmax()==sl.argmax() or float(abs(sl.topk(2).values[0,0]-sl.topk(2).values[0,1]))<.5
 # Causal prefix guard: keep shape, erase suffix mask/IDs.
 xp=x.clone();mp=mask.clone();xp[:,t+1:]=0;mp[:,t+1:]=0;pl=n.decode(n.body(xp,mp)[0,t:t+1]);ce=float(abs(pl-full).max());cn=float(abs(pl.log_softmax(-1)[0,rr[ind]['target_id']]-full.log_softmax(-1)[0,rr[ind]['target_id']]));assert ce<=.5 and cn<=.05
 oldh=np.load(O/'data/fresh_h.npy');cachelog=n.decode(model.model.norm(torch.tensor(oldh[ind:ind+1],device=n.dev,dtype=torch.bfloat16)));ce2=float(abs(cachelog-full).max());cn2=float(abs(cachelog.log_softmax(-1)[0,rr[ind]['target_id']]-full.log_softmax(-1)[0,rr[ind]['target_id']]));assert ce2<=.5 and cn2<=.05
 dump(E/'audit/03_numerics_smoke.json',{'pass':True,'layers':checks,'causal_prefix_logits_error':ce,'causal_prefix_NLL_error':cn,'old_cache_logits_error':ce2,'old_cache_NLL_error':cn2,'no_optimizer':True,'trainable_parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),'torch':torch.__version__,'transformers':__import__('transformers').__version__,'device':torch.cuda.get_device_name(rank),'reference_target':rr[ind]['position_uid']})
 print('SMOKE_PASS',flush=True)
def norms(h,z,mu,positions):
 a=h.float()-mu;b=z.float()-mu;per=(b.square().sum(-1)/a.square().sum(-1).clamp_min(1e-20));pert=(z.float()-h.float()).square().sum(-1).sqrt();rel=pert/h.float().square().sum(-1).sqrt().clamp_min(1e-20);out=[]
 for t in positions:out.append({'target_retained_energy':float(per[0,t]),'prefix_retained_energy':float(per[0,:t+1].mean()),'target_intervention_norm':float(pert[0,t]),'prefix_intervention_norm':float(pert[0,:t+1].mean()),'target_relative_intervention':float(rel[0,t]),'prefix_relative_intervention':float(rel[0,:t+1].mean())})
 return out
@torch.inference_mode()
def evaluate(model,rank):
 assert json.loads((E/'audit/03_numerics_smoke.json').read_text())['pass'];n=Native(model,rank);docs=sorted(rows(E/'data/evaluation_documents.jsonl'),key=lambda x:x['seq_id']);rr=rows(E/'data/positions.jsonl');groups=json.loads((E/'data/frozen_groups.json').read_text());start=time.time();outdir=E/'analysis/chunks';outdir.mkdir(exist_ok=True);bas=[basis(l,n.dev)[1:] for l in range(28)];randoms={f'random{s}':torch.tensor(np.load(E/'data'/f'random{s}.npy'),device=n.dev,dtype=torch.float32) for s in cfg['random_seeds']};old=np.load(O/'data/bases.npz');oldmu=torch.tensor(old['mean'],device=n.dev,dtype=torch.float32);oldq=torch.tensor(old['k64'],device=n.dev,dtype=torch.float32);count=0
 for ordinal,d in enumerate(docs):
  if ordinal%2!=rank:continue
  path=outdir/(d['seq_id']+'.json')
  if path.exists():
   prior=json.loads(path.read_text());assert prior['complete'] and prior['freeze_sha256']==sha(E/'freeze.json');continue
  inds=[i for i,r in enumerate(rr) if r['seq_id']==d['seq_id']];ts=[rr[i]['position'] for i in inds];targets=[rr[i]['target_id'] for i in inds];out,cap=n.capture(d);full=n.decode(out[0,ts]);records=[];base=n.metrics(full,full,targets,inds)
  for r in base:r.update(layer=0,condition='identity',scope='none',readout='continuation')
  records+=base;diff=[{'index':i,'old':groups[i]['old_full_top1_id'],'new':r['top1_id']} for i,r in zip(inds,base) if groups[i]['old_full_top1_id']!=r['top1_id']]
  # Fixed decoder shape and native replay must keep old top1; ties explicitly recorded.
  if diff:dump(E/'audit'/('baseline_difference_'+d['seq_id']+'.json'),diff)
  for l in range(28):
   h=cap[l];mu,q=bas[l];conds={'head64':q,'mean_only':q[:,:0],**randoms}
   if l==27:conds['legacy_head64']=oldq
   # diagnostic directly read each layer, explicitly include unprojected.
   for cname,hh in [('unprojected',h),('head64',n.project(h,mu,q))]:
    logits=n.decode(model.model.norm(hh[0,ts]));r=n.metrics(logits,full,targets,inds)
    for a in r:a.update(layer=l+1,condition=cname,scope='target_only',readout='direct_head')
    records+=r
   for cname,qq in conds.items():
    mm=oldmu if cname=='legacy_head64' else mu;projected=n.project(h,mm,qq);stats=norms(h,projected,mm,ts)
    # one all-prefix sequence and one target-only sequence for EACH target, including duplicate panel positions separately.
    hh=h.expand(1+len(ts),-1,-1).clone();hh[0,:192]=projected[0,:192]
    for j,t in enumerate(ts):hh[j+1,t]=projected[0,t]
    mask=torch.zeros((len(hh),256),dtype=torch.long,device=n.dev);mask[:,:192]=1
    continued=n.body(None,mask,start=l+1,emb=hh);selected=torch.cat([continued[0,ts],continued[torch.arange(1,len(ts)+1,device=n.dev),torch.tensor(ts,device=n.dev)]],0);logits=n.decode(selected)
    for k,scope in enumerate(cfg['scopes']):
     r=n.metrics(logits[k*len(ts):(k+1)*len(ts)],full,targets,inds)
     for j,a in enumerate(r):
      a.update(layer=l+1,condition=cname,scope=scope,readout='continuation',**stats[j]);a['prefix_retained_energy']=(stats[j]['prefix_retained_energy'] if scope=='all_prefix' else (stats[j]['target_retained_energy']+ts[j])/(ts[j]+1));a['prefix_intervention_norm']=(stats[j]['prefix_intervention_norm'] if scope=='all_prefix' else stats[j]['target_intervention_norm']/(ts[j]+1));a['prefix_relative_intervention']=(stats[j]['prefix_relative_intervention'] if scope=='all_prefix' else stats[j]['target_relative_intervention']/(ts[j]+1))
     records+=r
    if l==27:
     assert torch.equal(logits[:len(ts)],logits[len(ts):]),('last layer scope disagreement',cname,d['seq_id'])
   if l in [0,13,27]:print(json.dumps({'rank':rank,'document':d['seq_id'],'layer':l+1,'documents_done':count,'seconds':time.time()-start,'peak_bytes':torch.cuda.max_memory_allocated(rank)}),flush=True)
  dump(path,{'complete':True,'seq_id':d['seq_id'],'freeze_sha256':sha(E/'freeze.json'),'positions':len(inds),'baseline_differences':diff,'records':records});count+=1
  # Capture selected states for audit/old reference and allPC target guards; fullprefix not persisted.
  p=E/'data/eval_targets';p.mkdir(exist_ok=True);a=np.stack([cap[l][0,ts].float().cpu().numpy() for l in range(28)]);np.savez_compressed(p/(d['seq_id']+'.npz'),h=a,indices=np.array(inds))
  print(json.dumps({'rank':rank,'completed_documents':count,'last':d['seq_id'],'seconds':time.time()-start}),flush=True)
 assert all(not p.requires_grad and p.grad is None for p in model.parameters())
 dump(E/f'terminal_rank{rank}.json',{'complete':True,'rank':rank,'seconds':time.time()-start,'new_documents_this_attempt':count,'peak_GPU_bytes':torch.cuda.max_memory_allocated(rank),'trainable_parameters':0,'training_updates':0})
def main():
 p=argparse.ArgumentParser();p.add_argument('--stage',choices=['fit_smoke','evaluate'],required=True);p.add_argument('--rank',type=int,default=0);a=p.parse_args();m=init(a.rank)
 if a.stage=='fit_smoke':fit(m,a.rank);smoke(m,a.rank)
 else:evaluate(m,a.rank)
if __name__=='__main__':
 try:main()
 except Exception as ex:
  dump(E/'audit'/f'failure_{int(time.time())}_{os.getpid()}.json',{'error':repr(ex),'traceback':traceback.format_exc()});raise
