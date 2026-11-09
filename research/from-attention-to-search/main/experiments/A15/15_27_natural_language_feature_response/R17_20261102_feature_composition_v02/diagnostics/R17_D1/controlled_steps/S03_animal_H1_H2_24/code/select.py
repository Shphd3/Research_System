"""Reads only exploration responses. All candidates/directions frozen before heldout capture."""
from common import *
import numpy as np
assert not (R/'cache/heldout_check.npz').exists()
assert not (R/'results/selection.json').exists()
plan=json.load(open(R/'frozen_plan.json'));d=np.load(R/'cache/exploration.npz')
assert len(d['ids'])==12
def norm(a):
 v=np.linalg.norm(a,axis=-1,keepdims=True)
 return np.divide(a,v,out=np.full_like(a,np.nan),where=v>0)
out={};ranks=[]
for site in SITES:
 z=d[site+'__z'].astype(float).reshape(3,4,-1);u=z*d[site+'__decoder_norm'].astype(float);active=z>0
 triple=active[:,:3].all(axis=1);ct=triple.sum(0)
 contrast=u[:,:3].min(1)-u[:,3];strong=(triple & (contrast>0)).sum(0);score=contrast.mean(0)
 common=[int(i) for i in np.where((ct>=2)&(strong>=2))[0]];common.sort(key=lambda i:(-ct[i],-strong[i],-score[i],i))
 for rank,i in enumerate(common,1):ranks.append(dict(site=site,group='H1_common',rank=rank,atom=i,coverage=int(ct[i]),contrast_coverage=int(strong[i]),strength_score=float(score[i]),selected=rank<=6))
 added={}
 for ci,c in [(1,'cat'),(2,'dog')]:
  mask=(~active[:,0])&active[:,ci];cnt=mask.sum(0);scr=np.divide((u[:,ci]*mask).sum(0),cnt,out=np.zeros(30000),where=cnt>0)
  ii=[int(i) for i in np.where(cnt>=2)[0]];ii.sort(key=lambda i:(-cnt[i],-scr[i],i))
  for rank,i in enumerate(ii,1):ranks.append(dict(site=site,group='H1_added_'+c,rank=rank,atom=i,coverage=int(cnt[i]),contrast_coverage='',strength_score=float(scr[i]),selected=rank<=6))
  added[c]=ii[:6]
 joint=active[:,1]&active[:,2];cnt=joint.sum(0);scr=np.minimum(u[:,1],u[:,2]).mean(0)
 ii=[int(i) for i in np.where(cnt>=2)[0]];ii.sort(key=lambda i:(-cnt[i],-scr[i],i));h2=ii[:6]
 for rank,i in enumerate(ii,1):ranks.append(dict(site=site,group='H2_joint',rank=rank,atom=i,coverage=int(cnt[i]),contrast_coverage='',strength_score=float(scr[i]),selected=rank<=6))
 q=norm(u[:,:,h2]);qr=norm(z[:,:,h2]);delta=(q[:,1]-q[:,2]).mean(0)
 directions={str(i):None if not np.isfinite(v) else 0 if abs(v)<=1e-8 else int(np.sign(v)) for i,v in zip(h2,delta)}
 out[site]=dict(H1_common=common[:6],H1_added=added,H2=h2,H2_discovery_direction=directions,H2_discovery_mean_weighted_q_difference={str(i):None if not np.isfinite(v) else float(v) for i,v in zip(h2,delta)},eligible_common=len(common),eligible_H2=len(ii))
dump(R/'results/selection.json',dict(UTC=now(),source='cache/exploration.npz ONLY; no heldout response exists',exploration_cache_SHA256=sha(R/'cache/exploration.npz'),rules=plan['selection'],sites=out))
table(R/'results/exploration_candidate_ranking.csv',ranks,fields=['site','group','rank','atom','coverage','contrast_coverage','strength_score','selected'])
dump(R/'evidence/candidates_frozen_before_heldout.json',dict(UTC=now(),selection_SHA256=sha(R/'results/selection.json'),plan_SHA256=sha(R/'frozen_plan.json'),heldout_cache_exists=False,code_SHA256={p.name:sha(p) for p in (R/'code').glob('*.py')}))
print(json.dumps(out,ensure_ascii=False,indent=2))
