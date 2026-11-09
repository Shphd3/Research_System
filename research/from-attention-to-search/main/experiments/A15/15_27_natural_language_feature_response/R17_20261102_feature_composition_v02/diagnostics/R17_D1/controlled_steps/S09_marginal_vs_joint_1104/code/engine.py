from common import *
import numpy as np,ctypes as ct,subprocess,itertools
from scipy.sparse import csr_matrix
S08=R.parent/'S08_dataset_support_overlap_1104'
if not S08.is_dir():S08=R/'inputs'
PLAN=json.load(open(R/'frozen_plan.json'));INDEX=json.load(open(R/'data/split_indices.json'));PANEL=rows(S08/'data/panel.jsonl');SEL=json.load(open(R/'data/feature_universe.json'));TOK=json.load(open(R/'data/token_classes.json'))['token_ids'];PAIRS=list(itertools.combinations(range(24),2));FI=np.array([p[0] for p in PAIRS]);FJ=np.array([p[1] for p in PAIRS]);DP=list(itertools.combinations(range(3),2))
# Adapt the original sparse Jaccard implementation; row counts are measured, not assumed in Bernoulli.
def binary(ids,nfeat=30000):
 n,k=ids.shape;use=ids>=0;rr=np.broadcast_to(np.arange(n)[:,None],ids.shape)[use];return csr_matrix((np.ones(use.sum()),(rr,ids[use])),shape=(n,nfeat))
def kernels(support):
 # shape3,n,8,k padded-1or exact32; return J and I averaged8quantiles.
 n=support.shape[1];jj=np.zeros((3*n,3*n));ii=jj.copy()
 for t in range(8):
  b=binary(support[:,:,t].reshape(3*n,-1));inter=(b@b.T).toarray();c=np.array(b.sum(1)).ravel();u=c[:,None]+c[None,:]-inter;jj+=np.divide(inter,u,out=np.zeros_like(inter),where=u>0)/8;ii+=inter/8
 return jj,ii

def pair_stats(j,i):
 n=len(j)//3;within=np.triu_indices(n,1);rr=np.repeat(np.arange(n),(n-1)//2);cc=(np.repeat(np.arange(n),(n-1)//2)+np.tile(np.arange(1,(n-1)//2+1),n))%n
 # Discovery n128 uses diagnostic full cross rather than pretend balanced odd pairing.
 if n%2==0:rr,cc=np.indices((n,n)).reshape(2,-1)
 vals=[];ivs=[];cur=[];full=[]
 for d in range(3):
  a=within[0]+d*n;b=within[1]+d*n;vals.append(float(j[a,b].mean()));ivs.append(float(i[a,b].mean()));cur.append(vals[-1]-ivs[-1]/64)
 for d,e in DP:
  a=rr+d*n;b=cc+e*n;vals.append(float(j[a,b].mean()));ivs.append(float(i[a,b].mean()));cur.append(vals[-1]-ivs[-1]/64);full.append(float(j[d*n:(d+1)*n,e*n:(e+1)*n].mean()))
 return np.array(vals),np.array(ivs),np.array(cur),np.array(full)

def candidate_rows(support,features):
 a=np.zeros(support.shape[:-1]+(24,),dtype=bool)
 for f,idx in enumerate(features):a[...,f]=(support==idx).any(-1)
 return a

def joint(support,features,patterns=None):
 a=candidate_rows(support,features);q=(a[...,FI]&a[...,FJ]).mean(2);cnt=a.sum(-1);hist=np.stack([(cnt==k).mean((1,2)) for k in range(25)],axis=1);codes=np.sum(a.astype(np.uint32)*(1<<np.arange(24,dtype=np.uint32)),axis=-1)
 pat=None
 if patterns is not None:pat=np.stack([(codes==p).mean((1,2)) for p in patterns]+[(~np.isin(codes,patterns)).mean((1,2))],axis=1)
 return q,hist,codes,pat

libfile=R/'cache/curveball.so'
if not libfile.exists():
 p=subprocess.run(['g++','-O3','-std=c++17','-shared','-fPIC',str(R/'code/curveball.cpp'),'-o',str(libfile)],capture_output=True,text=True);assert p.returncode==0,p.stderr
LIB=ct.CDLL(str(libfile));LIB.create_chain.argtypes=[ct.POINTER(ct.c_int32),ct.c_int,ct.c_int,ct.c_uint64];LIB.create_chain.restype=ct.c_void_p;LIB.advance_chain.argtypes=[ct.c_void_p,ct.c_int];LIB.copy_rows.argtypes=[ct.c_void_p,ct.POINTER(ct.c_int32)];LIB.free_chain.argtypes=[ct.c_void_p];LIB.counters.argtypes=[ct.c_void_p,ct.POINTER(ct.c_uint64)]
class Sampler:
 def __init__(self,a,seed):
  self.original=np.sort(np.asarray(a,dtype=np.int32),axis=1);self.col=np.bincount(self.original.ravel(),minlength=30000);self.a=np.empty_like(self.original);self.handle=LIB.create_chain(self.original.ctypes.data_as(ct.POINTER(ct.c_int32)),len(a),32,int(seed));self.seed=int(seed);self.checks=0;self.maxerr=0;self.retention=[];self.hashes=[]
 def advance(self,sweeps):LIB.advance_chain(self.handle,sweeps)
 def snapshot(self):
  LIB.copy_rows(self.handle,self.a.ctypes.data_as(ct.POINTER(ct.c_int32)));assert np.all(np.diff(self.a,axis=1)>0);err=int(np.max(np.abs(np.bincount(self.a.ravel(),minlength=30000)-self.col)));self.maxerr=max(err,self.maxerr);assert err==0;self.checks+=1;keep=np.mean([len(set(x)&set(y))/32 for x,y in zip(self.original,self.a)]);self.retention.append(float(keep));self.hashes.append(hashlib.sha256(self.a.tobytes()).hexdigest());return self.a.copy()
 def audit(self):
  z=np.zeros(3,dtype=np.uint64);LIB.counters(self.handle,z.ctypes.data_as(ct.POINTER(ct.c_uint64)));n=len(self.a);baseline=float(np.sum(self.col.astype(float)**2)/(n*n*32));locked=np.where(self.col==n)[0];return dict(N=n,seed=self.seed,checks=self.checks,row32=True,unique_ids=True,max_column_error=self.maxerr,proposals=int(z[0]),changed_trades=int(z[1]),moved_edges=int(z[2]),changed_fraction=float(z[1]/z[0]) if z[0] else 0.,original_edge_retention_mean=float(np.mean(self.retention)),retention_stationary_expectation=baseline,retention_difference=float(np.mean(self.retention)-baseline),unique_snapshots=len(set(self.hashes)),locked_feature_ids=[int(i) for i in locked],locked_edge_fraction=float(len(locked)/32))
 def close(self):LIB.free_chain(self.handle)

def split_support(site,tag):
 ac=np.load(S08/'cache/activations.npz');ii=ac[site+'__indices'][:,:8];return np.stack([ii[INDEX[d+'__'+tag]] for d in DATASETS])

def rhat_ess(x):
 x=np.asarray(x,float);chains,n=x.shape
 if np.std(x)<1e-14:return dict(Rhat=1.,ESS=float(x.size),degenerate=True)
 xx=np.concatenate([x[:,:n//2],x[:,-n//2:]],axis=0);nn=xx.shape[1];within=np.mean(np.var(xx,axis=1,ddof=1));between=nn*np.var(xx.mean(1),ddof=1);v=(nn-1)/nn*within+between/nn;rh=float(np.sqrt(v/within)) if within else 999.
 # Conservative initial-positive autocorrelation sum; do not count negative tails as extra samples.
 centered=x-x.mean(1,keepdims=True);den=np.mean(np.sum(centered**2,axis=1));tau=1.
 if den:
  for lag in range(1,n//2):
   rho=float(np.mean(np.sum(centered[:,:-lag]*centered[:,lag:],axis=1))/den)
   if rho<=0:break
   tau+=2*rho
 ess=float(min(x.size,x.size/tau));return dict(Rhat=rh,ESS=ess,degenerate=False)
