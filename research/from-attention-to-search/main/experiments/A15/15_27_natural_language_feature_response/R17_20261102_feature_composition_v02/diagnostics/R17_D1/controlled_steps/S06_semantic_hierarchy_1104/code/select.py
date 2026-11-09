from common import *
import numpy as np
assert (R/'evidence/discovery_complete.json').exists() and not (R/'cache/remaining.npz').exists()
src=np.load(R/'cache/discovery.npz');ps={p['id']:p for p in rows(R/'data/panel.jsonl')};pp=[ps[x] for x in src['ids']];ix={(p['family'],p['label']):i for i,p in enumerate(pp)}
result={};summary=[]
for s in SITES:
 z=src[s+'__z'].astype(float);b=z>0;result[s]={}
 for d,labels in DOMAINS.items():
  trip=np.array([[ix[(f'F{i:02d}',c)] for c in labels] for i in range(1,9)]);x=z[trip];ab=x>0;freq=ab.all(1).sum(0);avg=x.mean((0,1))
  common=sorted(np.flatnonzero(freq>=6),key=lambda a:(-freq[a],-avg[a],a))[:8]
  h2=sorted(np.flatnonzero(freq==8),key=lambda a:(-avg[a],a))[:8]
  events={}
  for j,c in enumerate(labels[1:],1):
   for event,mask in [('recruit',(x[:,0]==0)&(x[:,j]>0)),('loss',(x[:,0]>0)&(x[:,j]==0))]:
    nf=mask.sum(0);delta=abs(x[:,j]-x[:,0]).mean(0);events[c+'_'+event]=[int(a) for a in sorted(np.flatnonzero(nf>=4),key=lambda a:(-nf[a],-delta[a],a))[:6]]
  xx=x[:,:,h2];norm=np.linalg.norm(xx,axis=-1,keepdims=True);q=np.divide(xx,norm,out=np.zeros_like(xx),where=norm>0)
  dirs={}
  for a,c in [(0,1),(0,2),(1,2)]:
   dd=(q[:,c]-q[:,a]).mean(0);n=float(np.linalg.norm(dd));dirs[labels[a]+'->'+labels[c]]=dict(mean=dd.tolist(),unit=(dd/n).tolist() if n>1e-12 else [0.]*len(dd),norm=n)
  delta=q[:,2]-q[:,1];mean=delta.mean(0);pairs=[]
  for a in range(len(h2)):
   for c in range(a+1,len(h2)):
    effect=float(((q[:,2,c]-q[:,2,a])-(q[:,1,c]-q[:,1,a])).mean());pairs.append(dict(a=int(h2[a]),b=int(h2[c]),effect=effect))
  pairs=sorted(pairs,key=lambda p:-abs(p['effect']))[:4]
  result[s][d]=dict(common=[int(a) for a in common],H2=[int(a) for a in h2],events=events,directions=dirs,rank_pairs=pairs,common_triple_discovery_count={str(a):int(freq[a]) for a in common},discovery_frequency_counts=b.sum(0).tolist())
  summary.append(dict(site=s,domain=d,H1_common=[int(a) for a in common],H2=[int(a) for a in h2],events=events,H2_direction_norm=dirs[labels[1]+'->'+labels[2]]['norm']))
dump(R/'results/selection.json',dict(UTC=now(),rule_sha256=sha(R/'frozen_plan.json'),sites=result))
dump(R/'evidence/candidates_frozen.json',dict(UTC=now(),selection_sha256=sha(R/'results/selection.json'),discovery_cache_sha256=sha(R/'cache/discovery.npz'),heldout_cache_exists=False,selection_rows=64,remaining_responses_seen=0,code_sha256=sha(__file__)))
print(json.dumps(summary),flush=True)
