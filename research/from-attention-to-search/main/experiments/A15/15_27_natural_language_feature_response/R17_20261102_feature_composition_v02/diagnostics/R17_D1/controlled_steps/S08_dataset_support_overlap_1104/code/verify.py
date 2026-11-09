from common import *
import numpy as np,pandas as pd,itertools
pp=rows(R/'data/panel.jsonl');ids=[p['id'] for p in pp];ac=np.load(R/'cache/activations.npz');ker=np.load(R/'cache/document_kernels.npz');graphs=np.load(R/'data/pair_graphs.npz');df=pd.read_csv(R/'tables/overlap_summary.csv');rr=np.random.default_rng(20261105);errors=[]
for path,h in json.load(open(R/'evidence/protocol_freeze.json'))['hashes'].items():assert sha(path)==h
assert len(pp)==771 and len({p['normalized_sha256'] for p in pp})==771;assert all(len(p['positions'])==len(set(p['positions']))==8 for p in pp)
for s in SITES:
 ii=ac[s+'__indices'];vv=ac[s+'__values'];counts=(vv>0).sum(-1);assert np.array_equal(counts,ac[s+'__active_count']);assert ii.shape==(771,10,32);assert all(len(set(row))==32 for row in ii.reshape(-1,32))
 for _ in range(100):
  a,b=rr.choice(771,2,False);jj=[]
  for t in range(8):
   x={int(i) for i,v in zip(ii[a,t],vv[a,t]) if v>0};y={int(i) for i,v in zip(ii[b,t],vv[b,t]) if v>0};jj.append(len(x&y)/len(x|y))
  errors.append(abs(np.mean(jj)-ker[s+'__main'][a,b]))
assert max(errors)<1e-12
pairchecks=[]
for _,r in df.iterrows():
 key=r.A+'__'+r.B+'__'+r['mode'];a=graphs[key+'__A'];b=graphs[key+'__B'];w=graphs[key+'__within_ij'];c=graphs[key+'__cross_ij'];n=len(a);assert len(w)==len(c)==n*(n-1)//2;assert np.all(w[:,0]<w[:,1]);assert len(set(map(tuple,c)))==len(c);assert set(a).isdisjoint(set(b));assert np.all(np.bincount(c[:,0],minlength=n)==(n-1)//2);assert np.all(np.bincount(c[:,1],minlength=n)==(n-1)//2)
 mode=r['mode'];kk=r.site+'__'+('main' if mode=='length_matched' else mode)
 if mode=='same_token':kk+='__'+r.A+'__'+r.B
 k=ker[kk]
 for col,aa,bb,edges in [('within_A',a,a,w),('within_B',b,b,w),('cross',a,b,c)]:
  vals=k[aa[edges[:,0]],bb[edges[:,1]]];point=np.nanmean(vals);assert abs(point-r[col])<1e-12;assert int(np.isfinite(vals).sum())==r[col+'_actual_pairs']
  assert r[col+'_lo']<=r[col+'_hi']
 pairchecks.append(key)
primary=df[df['mode']=='main'];assert len(primary)==6
p=primary.p_pooled_one_sided.to_numpy();oo=np.argsort(p);ad=np.minimum(1,np.maximum.accumulate([(6-j)*p[i] for j,i in enumerate(oo)]));assert np.allclose(primary.holm_primary.to_numpy()[oo],ad)
# Independent multiplicity arithmetic on a toy document graph, including repeated document incidences.
x=np.array([[0.,.2,.3],[.2,0,.7],[.3,.7,0]]);cnt=np.array([2,0,1]);edges=[(0,1),(0,2),(1,2)];explicit=[x[i,j] for i,j in edges for _ in range(cnt[i]*cnt[j])];weighted=sum(x[i,j]*cnt[i]*cnt[j] for i,j in edges)/sum(cnt[i]*cnt[j] for i,j in edges);assert abs(np.mean(explicit)-weighted)<1e-15
# A binary overlap must be invariant to any strictly positive rescaling of nonzero magnitudes.
a,b=ii[0,0],ii[1,0];va,vb=vv[0,0],vv[1,0];before=set(a[va>0])&set(b[vb>0]);after=set(a[(va*17)>0])&set(b[(vb*.02)>0]);assert before==after
perdoc=pd.read_csv(R/'tables/per_document_neighbors.csv')
for _,r in primary.iterrows():
 for ds,col in [(r.A,'A_minus_cross'),(r.B,'B_minus_cross')]:
  q=perdoc[(perdoc.site==r.site)&(perdoc.pair==r.A+'/'+r.B)&(perdoc.dataset==ds)];assert len(q)==257;assert abs(q.within_minus_cross.mean()-r[col])<1e-12
out=dict(UTC=now(),status='PASS',documents=771,unique_text_hashes=771,numerical_set_checks=200,max_Jaccard_error=max(errors),point_mean_replays=len(df)*3,pair_graph_checks=len(pairchecks),protocol_and_panel_freeze='unchanged',unit='whole document, all sampled positions and pair incidences kept together',Holm_checks=6,code_sha256=sha(__file__))
dump(R/'evidence/independent_verification.json',out);print(json.dumps(out))
