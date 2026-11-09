from engine import *
import time
assert (R/'evidence/directions_freeze.json').exists();marg=np.load(R/'data/discovery_marginals.npz');start=time.time();counts=[]
for site in SITES:
 out=R/'cache'/f'{site}__frequency_reference.npz';assert not out.exists();rr=np.random.default_rng(PLAN['seed']+8000000+SITES.index(site)*1000);nulls=[];inter=[];allc=[]
 for draw in range(256):
  support=np.full((3,129,8,96),-1,np.int32)
  for d,ds in enumerate(DATASETS):
   for t in range(8):
    p=marg[site+'__'+ds][t];ff=np.flatnonzero(p);active=rr.random((129,len(ff)))<p[ff][None,:];ctt=active.sum(1);assert ctt.max()<96;ii,jj=np.where(active);off=np.cumsum(ctt)-ctt;rank=np.arange(len(ii))-off[ii];support[d,ii,t,rank]=ff[jj];allc.append(ctt)
  jj,ii=kernels(support);st,ist,cu,fu=pair_stats(jj,ii);nulls.append(st);inter.append(ist)
  if draw%64==0:print(site,'BERNOULLI',draw,'seconds',round(time.time()-start,1),flush=True)
 c=np.concatenate(allc);np.savez_compressed(out,Jnull=np.array(nulls),Inull=np.array(inter),rowcount_hist=np.bincount(c,minlength=97));counts.append(dict(site=site,simulated_panels=256,documents_per_source=129,positions_per_doc=8,rowcount_mean=float(c.mean()),rowcount_sd=float(c.std()),rowcount_min=int(c.min()),rowcount_max=int(c.max()),expected_rowcount=32,total_simulated_rows=len(c),mean_MCSE_J=[float(v) for v in np.std(nulls,axis=0,ddof=1)/16]))
 print('FREQUENCY_COMPLETE',site,flush=True)
jsonl(R/'tables/frequency_reference_checks.jsonl',counts);dump(R/'evidence/frequency_complete.json',dict(UTC=now(),seconds=time.time()-start,conditioning='discovery plugin marginals; no fixed rowk; exactly simulated Jaccards; MC uncertainty distinct from document uncertainty'))
