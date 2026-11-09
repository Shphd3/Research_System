"""Only exploration activation rows are used for means, directions, top atoms and bootstrap."""
from common import *
from geometry import *
import itertools,time
assert not (R/'evidence/bases_frozen_before_check.json').exists()
plan=json.load(open(R/'frozen_plan.json'));panel=rows(R/'data/panel.jsonl');D=np.load(R/'data/S04_frozen_activations.npz');start=time.time();manifest=[];memberrows=[];spectrum=[];comparisons=[];bootstrap=[];summaries={}
for n,h in plan['data_SHA256'].items():assert sha(R/'data'/n)==h
for site in SITES:
 # All fitting/selection operations explicitly restrict to the first12 = F01-F03 rows.
 exploration=D[site+'__z'][:12].astype(np.float64);dn=D[site+'__decoder_norm'].astype(float)
 for scale in SCALES:
  x=exploration if scale=='raw_z' else exploration*dn;tol=1e-10*max(1,float(np.linalg.norm(x,axis=1).mean()));fits={};direc={}
  for group,ci in [('AC',1),('AD',2)]:
   idx=np.array([j for f in range(3) for j in [f*4,f*4+ci]]);X=x[idx];fit=fit_svd(X);fits[group]=fit;ids=np.array([panel[j]['id'] for j in idx]);base=R/f'cache/{site}/{scale}';base.mkdir(parents=True,exist_ok=True)
   path=base/f'{group}.npz';np.savez_compressed(path,X=X,centered=fit['centered'],mean=fit['mean'],singular_values=fit['singular_values'],components=fit['components'],row_ids=ids,row_indices=idx,rank=np.array(fit['rank']),rank_tol=np.array(fit['rank_tol']),near_zero_tol=np.array(tol))
   manifest.append(dict(site=site,scale=scale,group=group,rows=6,columns=30000,row_ids=ids.tolist(),row_indices=idx.tolist(),rank=fit['rank'],rank_tol=fit['rank_tol'],near_zero_tol=tol,cache=str(path.relative_to(R)),sha256=sha(path),center='own exploration6row column mean',exploration_families=['F01','F02','F03']))
   s=fit['singular_values'];denom=float(s@s)
   for j,v in enumerate(s):
    gap=float(v-s[j+1]) if j+1<len(s) else None;rel=gap/v if gap is not None and v>0 else None
    spectrum.append(dict(site=site,scale=scale,group=group,direction=j+1,singular_value=float(v),variance_fraction=float(v*v/denom) if denom>0 else None,gap_to_next=gap,relative_gap_to_next=rel,small_gap_warning=rel is not None and rel<.1,numerically_nonzero=j<fit['rank']))
   for j in range(min(2,fit['rank'])):
    v=fit['components'][j];ii=np.lexsort((np.arange(30000),-abs(v)))[:5]
    for rank,i in enumerate(ii,1):memberrows.append(dict(site=site,scale=scale,group=group,direction=j+1,loading_rank=rank,atom=int(i),coefficient=float(v[i]),absolute_coefficient=float(abs(v[i])),coefficient_squared=float(v[i]*v[i]),source='exploration_abs_loading_ONLY'))
  mC=x[1::4].mean(0)-x[0::4].mean(0);mD=x[2::4].mean(0)-x[0::4].mean(0)
  c1=compare(fits['AC'],fits['AD'],1);c2=compare(fits['AC'],fits['AD'],2)
  cr=dict(site=site,scale=scale,PC1_absolute_cosine=c1['abs_cosine'],top2_normalized_overlap=c2['normalized_overlap'],principal_angles_degrees=c2['angles_degrees'],AC_rank=fits['AC']['rank'],AD_rank=fits['AD']['rank'],exploration_mean_delta_cosine=signed_cos(mC,mD,tol),exploration_mean_delta_cat_L2=float(np.linalg.norm(mC)),exploration_mean_delta_dog_L2=float(np.linalg.norm(mD)),near_zero_tol=tol)
  comparisons.append(cr);summaries[site+'__'+scale]=cr
  for bi,sequence in enumerate(itertools.product(range(3),repeat=3)):
   bf={}
   for g,ci in [('AC',1),('AD',2)]:
    ix=[j for f in sequence for j in [f*4,f*4+ci]];bf[g]=fit_svd(x[ix])
   c=compare(bf['AC'],bf['AD'],1);d=compare(bf['AC'],bf['AD'],2);bc=np.mean([x[f*4+1]-x[f*4] for f in sequence],axis=0);bd=np.mean([x[f*4+2]-x[f*4] for f in sequence],axis=0)
   bootstrap.append(dict(site=site,scale=scale,resample=bi,sequence=[f'F{f+1:02d}' for f in sequence],distinct_families=len(set(sequence)),AC_rank=bf['AC']['rank'],AD_rank=bf['AD']['rank'],PC1_absolute_cosine=c['abs_cosine'],top2_overlap=d['normalized_overlap'],mean_paired_delta_signed_cosine=signed_cos(bc,bd,tol),AC_PC1_vs_full=compare(bf['AC'],fits['AC'],1)['abs_cosine'],AD_PC1_vs_full=compare(bf['AD'],fits['AD'],1)['abs_cosine'],AC_top2_vs_full=compare(bf['AC'],fits['AC'],2)['normalized_overlap'],AD_top2_vs_full=compare(bf['AD'],fits['AD'],2)['normalized_overlap']))
  print('FIT_AND_BOOTSTRAP',site,scale,round(time.time()-start,2),'sec',flush=True)
table(R/'results/spectrum_and_gaps.csv',spectrum);table(R/'results/top_loading_members.csv',memberrows);jsonl(R/'results/matrix_manifest.jsonl',manifest);jsonl(R/'results/geometry_comparisons.jsonl',comparisons);jsonl(R/'results/bootstrap_raw.jsonl',bootstrap)
bootrows=[]
for site,scale in itertools.product(SITES,SCALES):
 rr=[v for v in bootstrap if v['site']==site and v['scale']==scale]
 for metric in ['PC1_absolute_cosine','top2_overlap','mean_paired_delta_signed_cosine','AC_PC1_vs_full','AD_PC1_vs_full','AC_top2_vs_full','AD_top2_vs_full']:
  vv=np.array([v[metric] for v in rr if v[metric] is not None]);q=np.quantile(vv,[0,.05,.5,.95,1]) if len(vv) else [None]*5
  bootrows.append(dict(site=site,scale=scale,metric=metric,valid=len(vv),undefined=27-len(vv),total_ordered_resamples=27,distinct_unordered_multisets=10,min=None if q[0] is None else float(q[0]),q05=None if q[1] is None else float(q[1]),median=None if q[2] is None else float(q[2]),q95=None if q[3] is None else float(q[3]),max=None if q[4] is None else float(q[4]),interpretation='empirical3-family resampling description,NOT confidence interval'))
table(R/'results/bootstrap_summary.csv',bootrows)
dump(R/'evidence/bases_frozen_before_check.json',dict(UTC=now(),scope='8full exploration SVD fits +216paired-bootstrap exploration SVD fits; no heldout rows in means/directions/topatoms',matrix_SHA256={m['cache']:m['sha256'] for m in manifest},top_loading_SHA256=sha(R/'results/top_loading_members.csv'),plan_SHA256=sha(R/'frozen_plan.json'),code_SHA256={p.name:sha(p) for p in (R/'code').glob('*.py')},elapsed_seconds=time.time()-start))
dump(R/'results/fit_summary.json',summaries);print('BASES_AND_TOP_MEMBERS_FROZEN',json.dumps(summaries,ensure_ascii=False),flush=True)
