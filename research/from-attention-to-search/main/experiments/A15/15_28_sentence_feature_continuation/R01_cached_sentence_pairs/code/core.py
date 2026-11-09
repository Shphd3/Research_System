import os
for key in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMBA_NUM_THREADS']:os.environ[key]='4'
import json,hashlib,time,sys
from pathlib import Path
import numpy as np
from scipy import sparse
from numba import njit,prange
R=Path(__file__).resolve().parents[1]
SRC=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027')
GRAPH=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/graphs/raw_edges.npz')
DOCS=json.loads((R/'data/documents.json').read_text())
SENTS=[json.loads(x) for x in (R/'data/sentence_manifest.jsonl').read_text().splitlines()]
GROUPS=['low','middle','high','low_support','all'];METRICS=['identity','forward','reverse','all_forward','all_reverse','common_forward','common_reverse'];DIST=['1','2-3','4-7','8-15','16-31','32-63','64+']
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=True)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load_data(k):
 F=30000 if k=='SAE' else 16384
 tok=np.load(R/'data/tokens.npz');N=len(tok['doc']);B=np.zeros((N,F),np.bool_);zlist=[]
 for di,d in enumerate(DOCS):
  rr=np.flatnonzero(tok['doc']==di)
  if not len(rr):continue
  x=np.load(SRC/'forward/documents'/f"{d['seq_id']}.npz")
  assert np.array_equal(x['token_ids'],d['token_ids'])
  ptr=x[k+'_ptr'];ids=x[k+'_ids'];zs=x[k+'_z']
  for r in rr:
   p=tok['pos'][r];ii=ids[ptr[p]:ptr[p+1]];zz=zs[ptr[p]:ptr[p+1]]
   assert np.all(zz>0) and np.all(np.isfinite(zz)) and np.all(np.diff(ii)>0)
   B[r,ii]=True
 ref=np.load(SRC/f'forward/reference_{k}.npz');h=ref['counts'].sum(0);freq=h/ref['n_positions'].sum();cut=np.quantile(freq[h>=20],[1/3,2/3]);g=np.where(h<20,3,(freq>cut[0]).astype(int)+(freq>cut[1]).astype(int)).astype(np.int32)
 rows,features=np.nonzero(B);ptr=np.r_[0,np.cumsum(B.sum(1))].astype(np.int64)
 return B,ptr,features.astype(np.int32),g

def graph():
 x=np.load(GRAPH);a=x['A'][x['passV']].astype(np.int32);b=x['u'][x['passV']].astype(np.int32)
 assert len(a)==206136 and np.all(a!=b)
 return a,b

def adjacency(a,b,F=16384):
 G=sparse.csr_matrix((np.ones(len(a),np.int8),(a,b)),shape=(F,F));G.sort_indices();H=G.T.tocsr();return G.indptr,G.indices,H.indptr,H.indices

@njit(cache=True,parallel=True)
def coverage(B,ptr,ids,targets,gp,gi,hp,hi):
 N,F=B.shape;fw=np.zeros((N,F),np.bool_);rv=np.zeros((N,F),np.bool_)
 for v in prange(len(targets)):
  r=targets[v]
  for it in range(ptr[r],ptr[r+1]):
   g=ids[it]
   for j in range(hp[g],hp[g+1]):fw[r,hi[j]]=True
   for j in range(gp[g],gp[g+1]):rv[r,gi[j]]=True
 return fw,rv

@njit(cache=True,parallel=True)
def measure(B,ptr,ids,groups,pairs,fw,rv,hasgraph):
 # output pair,frequency,metric,real/control; separate counts source/lost real/lost control/common lost
 out=np.full((len(pairs),5,7,2),np.nan);counts=np.zeros((len(pairs),5,4),np.int32)
 for q in prange(len(pairs)):
  i,j,k=pairs[q];nums=np.zeros((5,7,2));den=np.zeros((5,4),np.int32)
  for it in range(ptr[i],ptr[i+1]):
   f=ids[it];group=groups[f];r=B[j,f];c=False if k<0 else B[k,f]
   for gg in range(2):
    g=group if gg==0 else 4
    den[g,0]+=1;den[g,1]+=not r
    if k>=0:den[g,2]+=not c;den[g,3]+=(not r and not c)
    nums[g,0,0]+=r
    if k>=0:nums[g,0,1]+=c
    if hasgraph:
     for dr in range(2):
      v=fw[j,f] if dr==0 else rv[j,f]
      w=False if k<0 else (fw[k,f] if dr==0 else rv[k,f])
      nums[g,1+dr,0]+=(not r and v);nums[g,3+dr,0]+=v
      if k>=0:
       nums[g,1+dr,1]+=(not c and w);nums[g,3+dr,1]+=w
       nums[g,5+dr,0]+=(not r and not c and v);nums[g,5+dr,1]+=(not r and not c and w)
  for g in range(5):
   for m in range(7 if hasgraph else 1):
    for cond in range(2):
     if cond==1 and k<0:continue
     dd=den[g,0] if m==0 or m in (3,4) else (den[g,3] if m>=5 else den[g,cond+1])
     if dd>0:out[q,g,m,cond]=nums[g,m,cond]/dd
   for t in range(4):counts[q,g,t]=den[g,t]
 return out,counts

@njit(cache=True)
def seed_rng(s):np.random.seed(s)
@njit(cache=True)
def incidence_switch(B,rows,ids,n):
 acc=0;E=len(ids)
 for q in range(n):
  x=np.random.randint(E);y=np.random.randint(E);r=rows[x];s=rows[y];f=ids[x];g=ids[y]
  if r!=s and f!=g and not B[r,g] and not B[s,f]:
   B[r,f]=False;B[s,g]=False;B[r,g]=True;B[s,f]=True;ids[x]=g;ids[y]=f;acc+=1
 return acc
@njit(cache=True)
def graph_switch(G,a,b,n):
 acc=0;E=len(a)
 for q in range(n):
  x=np.random.randint(E);y=np.random.randint(E);u=a[x];v=b[x];r=a[y];s=b[y]
  if u!=r and v!=s and u!=s and r!=v and not G[u,s] and not G[r,v]:
   G[u,v]=False;G[r,s]=False;G[u,s]=True;G[r,v]=True;b[x]=s;b[y]=v;acc+=1
 return acc

def synthetic():
 B=np.zeros((4,5),bool);B[0,[1,2]]=1;B[1,[2,3]]=1;B[2,[1,2]]=1
 rows,ids=np.nonzero(B);ptr=np.r_[0,np.cumsum(B.sum(1))];groups=np.zeros(5,np.int32)
 a=np.array([1]);b=np.array([3]);fw,rv=coverage(B,ptr,ids,np.arange(4),*adjacency(a,b,5));p=np.array([[0,1,2],[3,1,2],[0,2,1]])
 out,ct=measure(B,ptr,ids,groups,p,fw,rv,True)
 assert out[0,4,0,0]==.5 and out[0,4,1,0]==1 and out[0,4,2,0]==0
 assert np.isnan(out[1,4,0,0]) and np.isnan(out[2,4,1,0])
 a=np.array([1]);b=np.array([2]);fw,rv=coverage(B,ptr,ids,np.arange(4),*adjacency(a,b,5));o,_=measure(B,ptr,ids,groups,p,fw,rv,True);assert o[0,4,1,0]==1
 Bs=B.copy();ii=ids.copy();seed_rng(42);incidence_switch(Bs,rows,ii,1000);assert np.array_equal(B.sum(0),Bs.sum(0)) and np.array_equal(B.sum(1),Bs.sum(1))
 Ga=np.array([0,0,1,2],np.int32);Gb=np.array([1,2,3,4],np.int32);G=np.zeros((5,5),bool);G[Ga,Gb]=1;rs=G.sum(1);cs=G.sum(0);graph_switch(G,Ga,Gb,1000);assert np.array_equal(G.sum(0),cs) and np.array_equal(G.sum(1),rs) and not G.diagonal().any()
 dump(R/'provenance/synthetic_checks.json',dict(status='PASS',checks=['identity_half','empty_source_NA','lost_empty_NA','direction','isolated_zero','incidence_exact_margins','graph_exact_degrees_no_self'],elapsed=time.time()))
if __name__=='__main__':synthetic();print('synthetic PASS')
