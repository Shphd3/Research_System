"""Frozen v1+supplement contract. No transformer or dictionary training."""
import os
os.environ.setdefault('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION','python')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
import json,math,random,time,hashlib,csv,struct,resource
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from scipy import sparse
ROOT=Path(__file__).resolve().parents[1]
CFG=json.load(open(ROOT/'config/frozen.json'))
OLD=Path(CFG['paths']['old_run']); PREV=Path(CFG['paths']['previous_run'])
BASE=Path('/data/share/Qwen3-0.6B-Base')
K,D,FCOUNT=8,1024,16384

def write_json(path,obj):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 def clean(x):
  if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
  if isinstance(x,(list,tuple)):return [clean(v) for v in x]
  if isinstance(x,np.ndarray):return clean(x.tolist())
  if isinstance(x,np.generic):return clean(x.item())
  if isinstance(x,float) and not math.isfinite(x):return None
  return x
 temp=p.with_suffix(p.suffix+'.tmp');temp.write_text(json.dumps(clean(obj),ensure_ascii=False,indent=2)+'\n');temp.replace(p)
def save(path,obj):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix('.tmp');torch.save(obj,tmp);tmp.replace(p)
def csvwrite(path,rows):
 if not rows:return
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
def append(path,obj):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('a') as f:f.write(json.dumps(obj,allow_nan=False)+'\n');f.flush()
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(8<<20),b''):h.update(b)
 return h.hexdigest()
def tensorhash(state):
 h=hashlib.sha256()
 for k,v in sorted(state.items()):h.update(k.encode());h.update(v.detach().cpu().contiguous().reshape(-1).view(torch.uint8).numpy().tobytes())
 return h.hexdigest()
def configure(device,seed=11):
 torch.set_num_threads(2);random.seed(seed);np.random.seed(seed);torch.manual_seed(seed)
 torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 torch.use_deterministic_algorithms(True)
 if str(device).startswith('cuda'):
  torch.cuda.set_device(device);torch.cuda.set_per_process_memory_fraction(min(1.,32*(1<<30)/torch.cuda.get_device_properties(device).total_memory),device)
  torch.cuda.reset_peak_memory_stats(device)
def rng():return dict(python=random.getstate(),numpy=np.random.get_state(),torch=torch.get_rng_state(),cuda=torch.cuda.get_rng_state_all())
def setrng(r):
 random.setstate(r['python']);np.random.set_state(r['numpy']);torch.set_rng_state(r['torch']);torch.cuda.set_rng_state_all(r['cuda'])
def cpu_tree(x):
 if torch.is_tensor(x):return x.detach().cpu().clone()
 if isinstance(x,dict):return {k:cpu_tree(v) for k,v in x.items()}
 if isinstance(x,list):return [cpu_tree(v) for v in x]
 if isinstance(x,tuple):return tuple(cpu_tree(v) for v in x)
 return x
def loadcache(split):return torch.load(OLD/'cache'/f'{split}.pt',map_location='cpu',mmap=True,weights_only=False)
def csr(c,binary=False):
 v=np.ones(len(c['feature_ids']),dtype=np.float32) if binary else c['feature_z'].numpy()
 return sparse.csr_matrix((v,c['feature_ids'].numpy(),c['feature_ptr'].numpy()),shape=(len(c['target']),FCOUNT))
def condition(name):return next(c for c in CFG['conditions'] if c['id']==name)
def routes(split,name):return np.load(ROOT/'routes'/f'{split}_{name}.npz')['route']
def stats():return np.load(ROOT/'cache/train_stats.npz')
def sync(device):torch.cuda.synchronize(device)
def memory(device):
 return dict(rss_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,gpu_peak_allocated_bytes=torch.cuda.max_memory_allocated(device),gpu_allocated_bytes=torch.cuda.memory_allocated(device))
def safetensor_read(key):
 p=BASE/'model.safetensors'
 with p.open('rb') as f:
  length=struct.unpack('<Q',f.read(8))[0];meta=json.loads(f.read(length));a,b=meta[key]['data_offsets'];f.seek(8+length+a);raw=f.read(b-a)
 m=meta[key];dtype={'BF16':torch.bfloat16,'F32':torch.float32,'F16':torch.float16}[m['dtype']]
 return torch.frombuffer(bytearray(raw),dtype=torch.uint8).view(dtype).reshape(m['shape']).clone()
class FrozenHead(nn.Module):
 def __init__(self,device):
  super().__init__();self.register_buffer('norm',safetensor_read('model.norm.weight').to(device));self.register_buffer('weight',safetensor_read('model.embed_tokens.weight').to(device));self.eps=json.load(open(BASE/'config.json'))['rms_norm_eps']
 def forward(self,h):
  h=h.to(torch.bfloat16).float();h=h*torch.rsqrt(h.square().mean(-1,keepdim=True)+self.eps)
  return F.linear(h.to(torch.bfloat16)*self.norm,self.weight)
class Expert(nn.Module):
 def __init__(self):
  super().__init__();self.gate=nn.Linear(D,D,bias=False);self.up=nn.Linear(D,D,bias=False);self.down=nn.Linear(D,D,bias=False)
 def forward(self,u):return self.down(F.silu(self.gate(u))*self.up(u))
class Branch(nn.Module):
 def __init__(self,seed,learned=False):
  super().__init__();self.experts=nn.ModuleList([Expert() for _ in range(K)]);self.register_buffer('scale',torch.tensor(float(stats()['scale']),dtype=torch.float32))
  gen=torch.Generator().manual_seed(seed)
  with torch.no_grad():
   for e in self.experts:
    e.gate.weight.copy_(torch.randn(D,D,generator=gen)/math.sqrt(D));e.up.weight.copy_(torch.randn(D,D,generator=gen)/math.sqrt(D));e.down.weight.zero_()
  self.router=nn.Linear(D,K,bias=False) if learned else None
  if learned:
   with torch.no_grad():self.router.weight.copy_(.02*torch.randn(K,D,generator=torch.Generator().manual_seed(seed+741103)))
 def routing(self,h,fixed=None):
  if self.router is None:return fixed.long(),torch.ones(len(h),device=h.device),None
  P=torch.softmax(self.router(h.float()/self.scale),-1);r=P.argmax(-1);return r,P.gather(1,r[:,None]).flatten(),P
 def forward(self,h,fixed=None,force=None,gate_override=None):
  original=h.float();u=original/self.scale;r,g,P=self.routing(h,fixed)
  if force is not None:r=torch.full_like(r,force)
  if gate_override is not None:g=torch.ones_like(g)*gate_override
  delta=torch.zeros_like(original)
  with torch.autocast(device_type='cuda',dtype=torch.bfloat16):
   for e,expert in enumerate(self.experts):
    ix=torch.where(r==e)[0]
    if len(ix):delta[ix]=expert(u[ix]).float()*g[ix,None]
  return original+self.scale*delta,dict(route=r,gate=g,P=P)
def metrics(nll,c):
 x=csr(c,True);counts=np.asarray(x.sum(0)).ravel();sums=np.asarray(x.T@nll.astype(np.float64)).ravel();means=np.divide(sums,counts,out=np.full(FCOUNT,np.nan),where=counts>0)
 L=c['low_ids'].numpy();H=c['high_ids'].numpy();low=c['mask_low'].numpy();high=c['mask_high'].numpy()
 return dict(N=len(nll),overall=float(nll.mean(dtype=np.float64)),M_L=float(np.nanmean(means[L])),M_H=float(np.nanmean(means[H])),low_estimable=int(np.isfinite(means[L]).sum()),low_union=float(nll[low].mean(dtype=np.float64)),non_low_union=float(nll[~low].mean(dtype=np.float64)),high_union=float(nll[high].mean(dtype=np.float64))),means,counts
@torch.no_grad()
def evaluate(model,head,c,device,name=None,indices=None,force=None,gate_override=None,batch=256):
 ix=np.arange(len(c['target'])) if indices is None else np.asarray(indices);out=np.empty(len(ix),np.float32);rs=np.empty(len(ix),np.int16);gs=np.empty(len(ix),np.float32)
 fixed=routes('train' if len(c['target'])==CFG['train_N'] else 'eval',name) if model is not None and model.router is None else None
 for a in range(0,len(ix),batch):
  sub=ix[a:a+batch];h=c['hidden'][sub].to(device);y=c['target'][sub].to(device)
  if model is not None:
   h,d=model(h,torch.as_tensor(fixed[sub],device=device) if fixed is not None else None,force,gate_override);rs[a:a+len(sub)]=d['route'].cpu().numpy();gs[a:a+len(sub)]=d['gate'].cpu().numpy()
  else:rs[a:a+len(sub)]=-1;gs[a:a+len(sub)]=0
  out[a:a+len(sub)]=F.cross_entropy(head(h).float(),y,reduction='none').cpu().numpy()
 return out,rs,gs

def exposure(split,route,name,owner=None):
 c=loadcache(split);x=csr(c,True);ne=np.bincount(route,minlength=8);H=sparse.csr_matrix((np.ones(len(route)),(np.arange(len(route)),route)),shape=(len(route),8));count=(x.T@H).toarray().astype(np.int64);q=np.divide(count,ne[None,:],out=np.full_like(count,np.nan,dtype=np.float64),where=ne[None,:]>0)
 p=stats()['p'];L=c['low_ids'].numpy();T10=stats()['top10'];pool=stats()['pool'];B=np.full(len(L),np.nan);recv=np.full(len(L),np.nan);globalhits=np.bincount(c['feature_ids'].numpy(),minlength=FCOUNT)
 if owner is not None:
  for j,i in enumerate(L):
   e=owner[i];hits=int(globalhits[i])
   if e<0 or hits==0:continue
   recv[j]=count[i,e]/hits
   if ne[e]==0:continue
   if q[i,e]==0:B[j]=np.inf if np.any(q[T10,e]>0) else np.nan
   else:
    with np.errstate(divide='ignore'):B[j]=np.maximum(0,np.log10(q[T10,e]/q[i,e])).mean()
 pth=ROOT/'metrics/exposure';pth.mkdir(parents=True,exist_ok=True);np.savez_compressed(pth/f'{split}_{name}.npz',N_e=ne,counts=count,q=q,p=p,owner=owner if owner is not None else np.full(FCOUNT,-1),low=L,receive=recv,B=B)
 summ=dict(split=split,condition=name,N=len(route),load=ne.tolist(),low_receive_macro=float(np.nanmean(recv)) if np.isfinite(recv).any() else None,low_zero_receive=int((recv==0).sum()),low_NA=int(np.isnan(recv).sum()),B_le1_fixed964=float((B<=1).sum()/len(L)),B_le2_fixed964=float((B<=2).sum()/len(L)),B_finite=int(np.isfinite(B).sum()),B_infinity=int(np.isinf(B).sum()),B_NA=int(np.isnan(B).sum()),reliable_pool=len(pool),zero_exposure=[int((count[pool,e]==0).sum()) for e in range(8)])
 write_json(pth/f'{split}_{name}.json',summ);return summ
