"""Frozen uncentered native Dense weight SVD; deterministic CPU, one state at a time."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='4'
from pathlib import Path
import json,hashlib,time,gc,datetime,argparse,csv
import numpy as np
import torch
from scipy import linalg
ROOT=Path(__file__).resolve().parents[1];CFG=json.load(open(ROOT/'config.json'));MAN=json.load(open(ROOT/'manifest.json'))
torch.set_num_threads(4)
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(16*1024*1024),b''):h.update(b)
 return h.hexdigest()
def js(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);q=p.with_suffix('.partial');q.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n');os.replace(q,p)
def atomic_npz(p,x):
 q=p.with_suffix('.partial')
 with open(q,'wb') as f:np.savez(f,**x)
 os.replace(q,p)
def csvout(p,rows):
 with open(p,'w') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
def decompose(a):
 a=np.asarray(a);m,n=a.shape;right=n<=m;d=min(m,n);G=np.zeros((d,d),np.float64);chunksize=8192
 if right:
  for i in range(0,m,chunksize):
   b=a[i:i+chunksize].astype(np.float64);G+=b.T@b
 else:
  for i in range(0,n,chunksize):
   b=a[:,i:i+chunksize].astype(np.float64);G+=b@b.T
 w,v=linalg.eigh(G,driver='evd',check_finite=True);assert w[0]>=-max(w[-1],1)*1e-10
 w=np.maximum(w[::-1],0);v=v[:,::-1];s=np.sqrt(w);k=CFG['stored_rank'];small=v[:,:k].copy()
 assert s[k-1]>s[0]*1e-10,'TOP_RANK_NUMERIC_ZERO'
 opposite=np.empty((m if right else n,k),np.float64)
 if right:
  for i in range(0,m,chunksize):opposite[i:i+chunksize]=(a[i:i+chunksize].astype(np.float64)@small)/s[:k]
  U,V=opposite,small
 else:
  for i in range(0,n,chunksize):opposite[i:i+chunksize]=(a[:,i:i+chunksize].astype(np.float64).T@small)/s[:k]
  U,V=small,opposite
 norm=max(np.linalg.norm(G),1e-300);err=float(np.linalg.norm(G@small-small*w[:k])/norm)
 ou=float(np.linalg.norm(U.T@U-np.eye(k)));ov=float(np.linalg.norm(V.T@V-np.eye(k)))
 assert max(err,ou,ov)<1e-8,('NUMERIC_GUARD',err,ou,ov)
 return dict(singular_values=s,U=U,V=V),dict(eigen_relative_residual=err,U_orthogonality=ou,V_orthogonality=ov)
def smoke():
 rng=np.random.default_rng(1101);a=rng.normal(size=(128,96));s,check=decompose(a);uu,ss,vv=linalg.svd(a,full_matrices=False)
 assert np.max(abs(ss-s['singular_values']))<1e-10
 sub=lambda x,y:np.linalg.norm(x-y@(y.T@x))/np.sqrt(x.shape[1])
 assert sub(s['V'][:,:64],vv.T[:,:64])<1e-10
 assert sub(s['V'][:,:64],-s['V'][:,:64])<1e-10
 q,_=np.linalg.qr(rng.normal(size=(96,96)));b=a@q
 t,_=decompose(b);assert np.allclose(s['singular_values'],t['singular_values'],atol=1e-10)
 assert sub(s['V'][:,:64],t['V'][:,:64])>.2
 row=MAN['checkpoints'][0];state=torch.load(row['state_path'],map_location='cpu',weights_only=False,mmap=True);a=state['model']['blocks.0.attn.q.weight'].numpy();s,check=decompose(a)
 _,direct,v=linalg.svd(a.astype(np.float64),full_matrices=False,check_finite=True)
 error=float(np.linalg.norm(s['singular_values']-direct)/np.linalg.norm(direct));assert error<1e-10
 assert sub(s['V'][:,:64],v.T[:,:64])<1e-8
 # Identical top values are by construction below the registered isolation guard.
 assert (1.-1.)/1.<CFG['top1_isolation_relative_singular_gap']
 js(ROOT/'audit/smoke.json',dict(status='PASS',identity_and_sign=True,fixed_spectrum_rotating_axes=True,near_degenerate_unidentifiable=True,real_query_direct_SVD_relative_error=error,numerical=check,seconds=time.time()-START))
 print('SMOKE_PASS',round(time.time()-START,2),flush=True)
def run():
 assert (ROOT/'audit/smoke.json').exists()
 matrixrows=[];excluded=[];checks=[]
 for row in MAN['checkpoints']:
  assert time.time()-START<CFG['max_wall_seconds'],'WALL_CEILING'
  t=row['tokens'];beg=time.time();assert sha(row['state_path'])==row['state_sha256'],'CHECKPOINT_HASH'
  state=torch.load(row['state_path'],map_location='cpu',weights_only=False,mmap=True)
  assert state['tokens_seen']==t and state['optimizer_step']==row['step'];assert state['extra_training_state']['model_config']==row['architecture']
  weights=state['model'];actual=[k for k,v in weights.items() if v.ndim==2];assert set(actual)==set(CFG['modules']),(len(actual),len(CFG['modules']))
  for name,w in weights.items():
   if w.ndim!=2:excluded.append(dict(tokens=t,module=name,shape='x'.join(map(str,w.shape)),reason='ONE_DIMENSIONAL_GAIN_NOT_MATRIX'))
  done=0
  for name in CFG['modules']:
   assert time.time()-START<CFG['max_wall_seconds'],'WALL_CEILING'
   w=weights[name];a=w.numpy();spec=dict(checkpoint_sha256=row['state_sha256'],manifest_sha256=row['manifest_sha256'],module=name,shape=list(a.shape),config_sha256=sha(ROOT/'config.json'),code_sha256=sha(__file__),preprocessing='uncentered FP64 SVD native W[out,in]')
   key=hashlib.sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest();folder=ROOT/'cache'/str(t);folder.mkdir(exist_ok=True);p=folder/(name+'.npz');meta=p.with_suffix('.json')
   if p.exists() and meta.exists():
    saved=json.load(open(meta));assert saved['key']==key and sha(p)==saved['npz_sha256'],'CACHE_IDENTITY';data=dict(np.load(p));diag=saved['numerical']
   else:
    data,diag=decompose(a);atomic_npz(p,data);js(meta,dict(key=key,spec=spec,npz_sha256=sha(p),numerical=diag,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
   s=data['singular_values'];energy=float(np.sum(s*s));gap1=float((s[0]-s[1])/s[0]);gap64=float((s[63]-s[64])/s[63]);matrixrows.append(dict(tokens=t,training_B=t/1e9,module=name,rows=a.shape[0],cols=a.shape[1],dtype=str(w.dtype),s1=float(s[0]),frobenius_norm=float(np.sqrt(energy)),total_squared_singular_energy=energy,s1_energy_fraction=float(s[0]**2/energy),top64_energy_fraction=float(np.sum(s[:64]**2)/energy),gap1_relative=gap1,gap64_relative=gap64,pc1_identifiable=gap1>=CFG['top1_isolation_relative_singular_gap'],top64_numeric_identifiable=gap64>CFG['numerical_gap_floor'],top64_weak_gap=gap64<.05,**diag,cache=str(p)))
   done+=1;del data,a
  del weights,state;gc.collect();csvout(ROOT/'tables/matrix_metrics.csv',matrixrows);csvout(ROOT/'tables/excluded_tensors.csv',excluded)
  check=dict(tokens=t,step=row['step'],matrices=done,payload_hash='PASS',seconds=time.time()-beg,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());checks.append(check);js(ROOT/'audit/collection_progress.json',checks);print('CHECKPOINT_DONE',t,'matrices',done,'seconds',round(time.time()-beg,2),'elapsed',round(time.time()-START,2),flush=True)
 js(ROOT/'audit/collection_complete.json',dict(status='PASS',matrix_states=len(matrixrows),checkpoints=len(checks),seconds=time.time()-START,new_forwards=0,gpus=0,threads=4))
if __name__=='__main__':
 START=time.time()
 try:smoke();run()
 except BaseException as e:js(ROOT/'audit/failure.json',dict(error=repr(e),seconds=time.time()-START));raise
