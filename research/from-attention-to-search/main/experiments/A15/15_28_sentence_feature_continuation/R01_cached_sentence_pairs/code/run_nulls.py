from core import *
from datetime import datetime,timezone
import resource
OUT=R/'results/nulls';OUT.mkdir(exist_ok=True)
class State:
 def __init__(self,k,dom):
  self.k=k;self.dom=dom
  B,ptr,ids,g=load_data(k);tok=np.load(R/'data/tokens.npz');rr=np.flatnonzero(tok['domain']==dom);remap=np.full(len(B),-1,np.int32);remap[rr]=np.arange(len(rr));self.B=B[rr].copy();del B
  self.rows,self.ids=np.nonzero(self.B);self.ids=self.ids.astype(np.int32);self.ptr=np.r_[0,np.cumsum(self.B.sum(1))].astype(np.int64);self.g=g
  self.row0=self.B.sum(1);self.col0=self.B.sum(0);self.origids=self.ids.copy()
  pack=np.load(R/f'results/matched_{k}.npz');base=np.load(R/'data/base_pairs.npz')['pairs'];qq=np.flatnonzero(base[pack['base_indices'],5]==dom);self.pairs=remap[pack['pairs'][qq]];assert self.pairs.min()>=0
  self.targets=np.unique(self.pairs[:,1:].reshape(-1));cs=json.loads((R/f'results/cells_{k}.json').read_text());self.cidx=np.array([c['cell'] for c in cs if c['domain_id']==dom]);self.cells=[cs[i] for i in self.cidx]
  cols=(qq[:,None]*35+np.arange(35)).reshape(-1);W=sparse.load_npz(R/f'results/weights_{k}.npz');self.W=W[self.cidx][:,cols].tocsr();self.Wcount=self.W.copy();self.Wcount.data[:]=1
  self.probes=np.array([i for i,c in enumerate(self.cells) if c['tier']==1 and c['class_id']==0 and c['same_id']==0 and c['group']==4 and c['metric_id']<(3 if k=='CC' else 1)])
 def evaluate(self,a,b):
  fw,rv=coverage(self.B,self.ptr,self.ids,self.targets,*adjacency(a,b)) if self.k=='CC' else (np.zeros((1,1),bool),np.zeros((1,1),bool))
  y,_=measure(self.B,self.ptr,self.ids,self.g,self.pairs,fw,rv,self.k=='CC');v=y[:,:,:,0]-y[:,:,:,1];flat=v.reshape(-1);invalid=self.Wcount@(~np.isfinite(flat)).astype(float)
  res=np.stack([self.W@np.nan_to_num(y[:,:,:,q].reshape(-1)) for q in range(2)],1);res=np.c_[res,self.W@np.nan_to_num(flat)];res[invalid>0]=np.nan
  probes=[]
  for m in range(3 if self.k=='CC' else 1):
   idx=[i for i in self.probes if self.cells[i]['metric_id']==m];vv=res[idx,2];probes.append(float(np.nanmean(vv)) if np.isfinite(vv).any() else np.nan)
  return res,invalid,np.array(probes)

def acorr(v):
 v=np.array(v);v=v[np.isfinite(v)]
 return float(np.corrcoef(v[1:],v[:-1])[0,1]) if len(v)>2 and np.std(v)>0 else None

def check_budget():
 freeze=json.loads((R/'provenance/outcome_freeze.json').read_text());start=datetime.fromisoformat(freeze['time']).timestamp()
 if time.time()-start>4*3600:raise RuntimeError('WALL_CAP_4H')
 if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>16*1024*1024:raise RuntimeError('RAM_CAP_16GIB')

def chains(kind,states):
 a0,b0=graph();E=len(a0) if kind=='graph' else len(states[0].ids);prefix='graph' if kind=='graph' else f'incidence_{states[0].k}_{states[0].dom}'
 allres=[[] for _ in states];allinvalid=[[] for _ in states];allprobe=[];diagnostics=[];start=time.time()
 seedbase=20261032 if kind=='graph' else 20261031
 offset=0 if kind=='graph' else (0 if states[0].k=='SAE' else 2)+states[0].dom
 seeds=np.random.SeedSequence([seedbase,offset]).generate_state(2).tolist()
 for chain in range(2):
  seed_rng(int(seeds[chain]));a=a0.copy();b=b0.copy();burnover=[];accepted=0;attempted=0;probes=[];overlaps=[]
  if kind=='graph':
   G=np.zeros((16384,16384),bool);G[a,b]=True;outdeg=np.bincount(a,minlength=16384);indeg=np.bincount(b,minlength=16384)
   def step(n):return graph_switch(G,a,b,n)
   def overlap():return float(G[a0,b0].mean())
  else:
   s=states[0];s.ids[:]=s.origids;s.B[:]=False;s.B[s.rows,s.ids]=True
   def step(n):return incidence_switch(s.B,s.rows,s.ids,n)
   def overlap():return float(s.B[s.rows,s.origids].mean())
  burnover.append(overlap())
  for z in range(5):accepted+=step(E);attempted+=E;burnover.append(overlap());check_budget()
  for draw in range(199):
   if draw>0:
    n=int(np.ceil(E/10));accepted+=step(n);attempted+=n
   if kind=='graph':
    assert np.array_equal(np.bincount(a,minlength=16384),outdeg) and np.array_equal(np.bincount(b,minlength=16384),indeg)
    assert np.all(a!=b) and np.count_nonzero(G)==E
   else:assert np.array_equal(s.B.sum(0),s.col0) and np.array_equal(s.B.sum(1),s.row0)
   pp=[]
   for si,state in enumerate(states):
    result,invalid,probe=state.evaluate(a,b);allres[si].append(result);allinvalid[si].append(invalid);pp.extend(probe.tolist())
   probes.append(pp);overlaps.append(overlap());check_budget()
   if draw%10==0 or draw==198:
    elapsed=time.time()-start;done=chain*199+draw+1
    print(prefix,'chain',chain,'draw',draw,'elapsed',round(elapsed,1),'remaining_est',round(elapsed/done*(398-done),1),flush=True)
    for si,state in enumerate(states):np.savez_compressed(OUT/f'{prefix}_{state.k}_{state.dom}_partial.npz',values=np.array(allres[si]),invalid=np.array(allinvalid[si]),cell_ids=state.cidx)
  diagnostics.append(dict(chain=chain,seed=seeds[chain],attempted=attempted,accepted=accepted,acceptance=accepted/attempted,burnin_original_overlap=burnover,original_overlap=overlaps,probe_lag1=[acorr(np.array(probes)[:,j]) for j in range(len(probes[0]))],overlap_lag1=acorr(overlaps),invariants_every_draw=True));allprobe.append(probes)
 pp=np.array(allprobe);mean=np.nanmean(pp,axis=1);sd=np.sqrt((np.nanvar(pp[0],axis=0)+np.nanvar(pp[1],axis=0))/2);diff=np.abs(mean[0]-mean[1]);between=bool(np.any(diff>2*sd));flags=[]
 if any(d['acceptance']<.001 for d in diagnostics):flags.append('LOW_ACCEPTANCE')
 if any(d['burnin_original_overlap'][-1]>=d['burnin_original_overlap'][0] for d in diagnostics):flags.append('NO_BURNIN_OVERLAP_DECREASE')
 if between:flags.append('BETWEEN_CHAIN_PROBE_DIFFERENCE')
 if not np.isfinite(mean).all():flags.append('GLOBAL_PROBE_UNAVAILABLE')
 info=dict(kind=kind,prefix=prefix,chains=diagnostics,pooled_probe_sd=sd.tolist(),between_mean_difference=diff.tolist(),qualification='MIXING_UNQUALIFIED' if flags else 'DIAGNOSTICS_PASSED_NOT_PROOF_OF_MIXING',flags=flags,draws=398,seconds=time.time()-start,peak_rss_gib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2)
 dump(OUT/f'{prefix}_diagnostics.json',info)
 for si,state in enumerate(states):
  vv=np.array(allres[si]);inv=np.array(allinvalid[si]);np.savez_compressed(OUT/f'{prefix}_{state.k}_{state.dom}.npz',values=vv,invalid=inv,cell_ids=state.cidx,probes=pp)
  (OUT/f'{prefix}_{state.k}_{state.dom}_partial.npz').unlink()
 print(prefix,'COMPLETE',info['qualification'],flush=True)

def main():
 if sys.argv[1]=='incidence':
  k=sys.argv[2];dom=int(sys.argv[3]);chains('incidence',[State(k,dom)])
 elif sys.argv[1]=='graph':chains('graph',[State('CC',0),State('CC',1)])
if __name__=='__main__':main()
