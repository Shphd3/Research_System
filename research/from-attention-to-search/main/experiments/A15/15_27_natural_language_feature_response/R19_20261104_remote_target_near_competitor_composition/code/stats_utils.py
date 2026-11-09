import numpy as np,itertools
from scipy.stats import rankdata
def cosine(a,b,eps=1e-6):
 na=float(np.linalg.norm(a));nb=float(np.linalg.norm(b))
 return float(np.dot(a,b)/(na*nb)) if na>eps and nb>eps else None
def boot_interval(v,seed=2026110419,n=4096):
 v=np.asarray(v,float);v=v[np.isfinite(v)]
 if not len(v):return [None,None]
 rng=np.random.default_rng(seed);b=v[rng.integers(0,len(v),(n,len(v)))].mean(1);return np.quantile(b,[.025,.975]).tolist()
def sign_p(v):
 v=np.asarray(v,float);v=v[np.isfinite(v)];n=len(v)
 if not n:return 1.
 bits=np.array(list(itertools.product([-1.,1.],repeat=n)));return float(np.mean((bits@v/n)>=np.mean(v)-1e-14))
def corr(x,y):
 x=np.asarray(x,float);y=np.asarray(y,float)
 if len(x)<3 or np.std(x)==0 or np.std(y)==0:return None
 return float(np.corrcoef(rankdata(x),rankdata(y))[0,1])
def corr_audit(x,y,templates,seed=2026110419):
 x=np.asarray(x,float);y=np.asarray(y,float);templates=np.asarray(templates);rho=corr(x,y)
 if rho is None:return dict(rho=None,lo=None,hi=None,p=1.,template_p=1.,bootstrap_valid=0)
 rng=np.random.default_rng(seed);null=[corr(x,rng.permutation(y)) for _ in range(9999)];p=(1+sum(z is not None and z>=rho-1e-14 for z in null))/10000;bb=[]
 for j in range(4096):
  ix=rng.integers(0,len(x),len(x));v=corr(x[ix],y[ix])
  if v is not None:bb.append(v)
 groups=[np.where(templates==g)[0] for g in sorted(set(templates))];perms=[]
 # Whole observed two-family template strata; singleton strata stay fixed.
 for flags in itertools.product([False,True],repeat=len(groups)):
  yy=y.copy()
  for ii,swap in zip(groups,flags):
   if swap:yy[ii]=yy[ii[::-1]]
  v=corr(x,yy)
  if v is not None:perms.append(v)
 lo,hi=np.quantile(bb,[.025,.975]) if bb else [None,None]
 return dict(rho=rho,lo=None if lo is None else float(lo),hi=None if hi is None else float(hi),p=float(p),template_p=float(np.mean(np.array(perms)>=rho-1e-14)) if perms else 1.,bootstrap_valid=len(bb))
def holm(p):
 p=np.asarray(p,float);order=np.argsort(p);out=np.zeros(len(p));prev=0.
 for i,j in enumerate(order):prev=max(prev,(len(p)-i)*p[j]);out[j]=min(prev,1.)
 return out.tolist()
def cluster_interval(v,labels,seed=2026110419):
 groups=sorted(set(labels));a=np.array([np.mean([x for x,g in zip(v,labels) if g==k]) for k in groups]);return boot_interval(a,seed)
