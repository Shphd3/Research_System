from common import *
import numpy as np,ctypes as ct,subprocess,itertools
PLAN=json.load(open(R/'config.json'))
def load_stage(stage,site):
 p=[x for x in rows(R/'data/panel.jsonl') if x['split']==stage];a=np.load(R/f'cache/{stage}.npz');assert list(a['ids'])==[x['id'] for x in p]
 z=np.zeros((len(p),30000),np.float32);np.put_along_axis(z,a[site+'__indices'],a[site+'__values'],axis=1)
 return p,z,a
def per_condition(p):return {co:np.array([i for i,x in enumerate(p) if x['condition']==co],int) for co in CONDS}
libfile=R/'cache/curveball.so'
def library():
 if not libfile.exists():
  x=subprocess.run(['g++','-O3','-std=c++17','-shared','-fPIC',str(R/'code/curveball.cpp'),'-o',str(libfile)],capture_output=True,text=True);assert x.returncode==0,x.stderr
 lib=ct.CDLL(str(libfile));lib.create_chain.argtypes=[ct.POINTER(ct.c_int32),ct.c_int,ct.c_int,ct.c_uint64];lib.create_chain.restype=ct.c_void_p;lib.advance_chain.argtypes=[ct.c_void_p,ct.c_int];lib.copy_rows.argtypes=[ct.c_void_p,ct.POINTER(ct.c_int32)];lib.free_chain.argtypes=[ct.c_void_p];lib.counters.argtypes=[ct.c_void_p,ct.POINTER(ct.c_uint64)];return lib
class Sampler:
 def __init__(self,ids,seed):
  self.lib=library();self.original=np.sort(np.asarray(ids,np.int32),axis=1);assert self.original.shape[1]==32 and np.all(np.diff(self.original,axis=1)>0);self.col=np.bincount(self.original.ravel(),minlength=30000);self.a=np.empty_like(self.original);self.ptr=self.lib.create_chain(self.original.ctypes.data_as(ct.POINTER(ct.c_int32)),len(ids),32,seed);self.n=len(ids);self.retention=[];self.checks=0;self.hashes=[]
 def advance(self,n):self.lib.advance_chain(self.ptr,n)
 def snapshot(self):
  self.lib.copy_rows(self.ptr,self.a.ctypes.data_as(ct.POINTER(ct.c_int32)));assert np.all(np.diff(self.a,axis=1)>0);assert np.array_equal(np.bincount(self.a.ravel(),minlength=30000),self.col);self.checks+=1;self.retention.append(float(np.mean([len(set(x)&set(y))/32 for x,y in zip(self.original,self.a)])));self.hashes.append(hashlib.sha256(self.a.tobytes()).hexdigest());return self.a.copy()
 def audit(self):
  cc=np.zeros(3,np.uint64);self.lib.counters(self.ptr,cc.ctypes.data_as(ct.POINTER(ct.c_uint64)));ex=float(np.sum(self.col.astype(float)**2)/(self.n*self.n*32));return dict(N=self.n,row32=True,column_counts_exact=True,checks=self.checks,proposals=int(cc[0]),changed_trades=int(cc[1]),changed_fraction=float(cc[1]/cc[0]) if cc[0] else 0,mean_retention=float(np.mean(self.retention)),stationary_retention_expectation=ex,retention_error=float(np.mean(self.retention)-ex),locked_feature_ids=np.where(self.col==self.n)[0].tolist(),unique_snapshots=len(set(self.hashes)))
 def close(self):self.lib.free_chain(self.ptr)
def mixing(x):
 x=np.asarray(x,float)
 if np.std(x)<1e-12:return dict(Rhat=None,ESS=None,degenerate=True,adequate=False)
 chains,n=x.shape;xx=np.concatenate([x[:,:n//2],x[:,-n//2:]]);nn=xx.shape[1];w=np.mean(np.var(xx,axis=1,ddof=1));b=nn*np.var(xx.mean(1),ddof=1);rh=float(np.sqrt(((nn-1)/nn*w+b/nn)/w)) if w>0 else 999.;cen=x-x.mean(1,keepdims=True);den=np.mean(np.sum(cen**2,axis=1));tau=1.
 for lag in range(1,n//2):
  rho=float(np.mean(np.sum(cen[:,:-lag]*cen[:,lag:],axis=1))/den)
  if rho<=0:break
  tau+=2*rho
 ess=float(min(x.size,x.size/tau));return dict(Rhat=rh,ESS=ess,degenerate=False,adequate=rh<=1.1 and ess>=100)
def allpairs(n):return np.array(list(itertools.combinations(range(n),2)),int).reshape(-1,2)
def binary_features(ids,features):return np.array([(ids==f).any(1) for f in features]).T
def moments(p,z,features,scale):
 pp=allpairs(len(features));ix=per_condition(p);b=z[:,features]>0;v=z[:,features]/scale
 br=np.array([(b[rr][:,pp[:,0]]&b[rr][:,pp[:,1]]).astype(float) for rr in ix.values()]);ar=np.array([v[rr][:,pp[:,0]]*v[rr][:,pp[:,1]] for rr in ix.values()]);return br,ar,pp,ix
def run_binary(ids,p,features,seed,burn=100,thin=10):
 ix=per_condition(p);pairs=allpairs(len(features));tr=[];audits=[];snapshots={}
 for chain in range(4):
  samplers=[Sampler(ids[rr],seed+chain*1000+k) for k,rr in enumerate(ix.values())]
  for obj in samplers:obj.advance(burn)
  trace=[]
  for draw in range(64):
   stats=[]
   for k,obj in enumerate(samplers):
    obj.advance(thin);a=obj.snapshot();b=binary_features(a,features);stats.append((b[:,pairs[:,0]]&b[:,pairs[:,1]]).mean(0))
    if chain==0 and draw in [0,63]:snapshots[f'condition{k}_draw{draw}']=a
   trace.append(stats)
  tr.append(trace)
  for k,obj in enumerate(samplers):audits.append(dict(chain=chain,condition=CONDS[k],**obj.audit()));obj.close()
 return np.array(tr),audits,snapshots
def run_amplitude(z,p,features,scale,seed):
 ix=per_condition(p);pairs=allpairs(len(features));out=[]
 for chain in range(4):
  rng=np.random.default_rng(seed+chain*1000);trace=[]
  for draw in range(64):
   stats=[]
   for rr in ix.values():
    a=z[rr][:,features].copy()
    for j in range(len(features)):
     active=np.where(a[:,j]>0)[0];values=a[active,j].copy();a[active,j]=rng.permutation(values);assert np.array_equal(np.sort(values),np.sort(a[active,j]))
    v=a/scale;stats.append((v[:,pairs[:,0]]*v[:,pairs[:,1]]).mean(0))
   trace.append(stats)
  out.append(trace)
 return np.array(out)
