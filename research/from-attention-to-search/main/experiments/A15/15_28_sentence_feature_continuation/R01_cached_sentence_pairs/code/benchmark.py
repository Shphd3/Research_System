from core import *
from datetime import datetime,timezone
synthetic();rng=np.random.default_rng(4);N=7000;F=16384;B=np.zeros((N,F),bool)
for r in range(N):B[r,rng.choice(F,300,replace=False)]=1
rows,ids=np.nonzero(B);ids=ids.astype(np.int32);ptr=np.r_[0,np.cumsum(B.sum(1))];g=rng.integers(0,4,F,dtype=np.int32);p=rng.integers(0,N,(75000,3),dtype=np.int32)
a,b=graph();adj=adjacency(a,b)
# First calls compile; time representative domain-sized steady state separately.
fw,rv=coverage(B,ptr,ids,np.arange(N),*adj);out,_=measure(B,ptr,ids,g,p[:10],fw,rv,True);incidence_switch(B,rows,ids,10)
t=time.time();fw,rv=coverage(B,ptr,ids,np.arange(N),*adj);cov=time.time()-t
t=time.time();out,_=measure(B,ptr,ids,g,p,fw,rv,True);secs=time.time()-t
t=time.time();incidence_switch(B,rows,ids,int(np.ceil(len(ids)/10)));swap=time.time()-t
estimated=(secs+cov+swap+0.6)*1592+600
rec=dict(time=datetime.now(timezone.utc).isoformat(),synthetic=True,N=N,F=F,pairs=len(p),coverage_seconds=cov,measurement_seconds=secs,spacing_switch_seconds=swap,estimated_full_null_seconds=estimated,ceiling_seconds=14400,peak_engineering_ram_estimate_gib=5,reason='Representative domain-sized warmed benchmark replaces small cold-JIT extrapolation; no draw count, threshold or resource ceiling changed. Conservative 1592 CC-sized evaluations plus SAE/bootstrap/storage allowance.')
dump(R/'provenance/runtime_smoke.json',rec);print(rec);assert estimated<14400
