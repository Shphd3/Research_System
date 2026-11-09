from pathlib import Path
import numpy as np,pandas as pd,json
root=Path(__file__).resolve().parents[1];a=np.load(root/'cache/activations.npz');g=np.load(root/'data/pair_graphs.npz');df=pd.read_csv(root/'tables/overlap_summary.csv');errors=[]
for s in ['ATTN_SAE','MLPIN_SAE']:
 ii=a[s+'__indices'];vv=a[s+'__values'];support=[[{int(x) for x,v in zip(ii[d,t],vv[d,t]) if v>0} for t in range(8)] for d in range(len(ii))]
 for _,r in df[(df.site==s)&(df['mode']=='main')].iterrows():
  key=r.A+'__'+r.B+'__main';aa=g[key+'__A'];bb=g[key+'__B']
  for col,x,y,en in [('within_A',aa,aa,'within_ij'),('within_B',bb,bb,'within_ij'),('cross',aa,bb,'cross_ij')]:
   ed=g[key+'__'+en];vals=[]
   for p,q in ed:
    ss,tt=support[x[p]],support[y[q]];vals.append(sum(len(z&w)/len(z|w) for z,w in zip(ss,tt))/8)
   errors.append(abs(np.mean(vals)-r[col]))
assert max(errors)<1e-12
print(json.dumps({'status':'PASS','main_group_means':len(errors),'max_error':max(errors),'requires_model':False,'requires_large_kernel':False}))
