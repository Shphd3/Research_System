"""Only protocol-declared descriptive sensitivities; no member selection or tests added."""
from engine import *
from stats_utils import cosine,boot_interval,corr_audit
spec=json.load(open(R/'data/candidates.json'))['sites'];out=[];swap=[];single=[]
for site in SITES:
 for stage in ['discovery','heldout']:
  p,z,a=load_stage(stage,site);by={x['id']:i for i,x in enumerate(p)};fs=sorted({x['family'] for x in p})
  for co,rr in per_condition(p).items():
   for atom in spec[site]['U']:
    v=z[rr,atom];positive=v[v>0];single.append(dict(site=site,split=stage,condition=co,atom=atom,rows=len(rr),positions=int(sum(v>0)),families=len({p[r]['family'] for r in rr if z[r,atom]>0}),mean_z=float(v.mean()),mean_positive_z=float(positive.mean()) if len(positive) else None,RMS=float(np.sqrt(np.mean(v*v))),positive_values=list(map(float,positive))))
  for fam in fs:
   for size in [3,6]:
    ids=spec[site]['C'][:size]
    for form in ['raw','relative']:
     v={co:{g:z[by[f'{fam}_{co}_{g}'],ids].astype(float) for g in 'AB'} for co in CONDS}
     if form=='relative':v={co:{g:x/np.linalg.norm(x) if np.linalg.norm(x)>0 else np.zeros_like(x) for g,x in dd.items()} for co,dd in v.items()}
     d0=v['nearN']['A']-v['nearN']['B'];ta=v['nearA']['A']-v['nearA']['B'];tb=v['nearB']['A']-v['nearB']['B'];T=(ta+tb)/2;N=(v['nearA']['A']-v['nearB']['A']+v['nearA']['B']-v['nearB']['B'])/2;d16=v['main16']['A']-v['main16']['B'];d128=v['main128']['A']-v['main128']['B'];den=float(d0@d0);ca=cosine(ta,d0);cb=cosine(tb,d0)
     out.append(dict(site=site,split=stage,family=fam,size=size,form=form,all4main_positive=all(np.all(z[by[f'{fam}_{co}_{g}'],ids]>0) for co in ['main16','main128'] for g in 'AB'),all6far_positive=all(np.all(z[by[f'{fam}_{co}_{g}'],ids]>0) for co in ['nearN','nearA','nearB'] for g in 'AB'),target_alignment=(ca+cb)/2 if ca is not None and cb is not None else None,near_far_cosine=cosine(d16,d128),near_far_projection=float(d128@d16/(d16@d16)) if d16@d16>1e-12 else None,target_projection=float(T@d0/den) if den>1e-12 else None,near_projection=float(N@d0/den) if den>1e-12 else None,pattern_loss=1-float((T-N)@d0/den) if den>1e-12 else None))
   def jac(x,y):
    s=set(np.flatnonzero(x));t=set(np.flatnonzero(y));return len(s&t)/len(s|t)
   for lo,hi in [(16,64),(16,128),(64,128)]:
    same=np.mean([jac(z[by[f'{fam}_main{lo}_{g}']],z[by[f'{fam}_main{hi}_{g}']]) for g in 'AB']);wrong=np.mean([jac(z[by[f'{fam}_main{lo}_{g}']],z[by[f'{fam}_main{hi}_{h}']]) for g,h in [('A','B'),('B','A')]])
    swap.append(dict(site=site,split=stage,family=fam,role=f'{lo}_to_{hi}',same_fact_Jaccard=float(same),swapped_fact_Jaccard=float(wrong),difference=float(same-wrong)))
table(R/'tables/declared_sensitivities.csv',out);table(R/'tables/fact_aligned_vs_swapped.csv',swap);table(R/'tables/single_member_marginals.csv',single)
summ=[]
for site in SITES:
 for role in ['16_to_64','16_to_128','64_to_128']:
  q=[x for x in swap if x['site']==site and x['split']=='heldout' and x['role']==role];v=[x['difference'] for x in q];summ.append(dict(site=site,role=role,families=len(q),same_mean=float(np.mean([x['same_fact_Jaccard'] for x in q])),swapped_mean=float(np.mean([x['swapped_fact_Jaccard'] for x in q])),difference=float(np.mean(v)),CI=boot_interval(v)))
dump(R/'results/declared_sensitivities.json',dict(scope='Descriptive only; predeclared C3 and fixed-list-with-zeros, fact-swapped membership control. No new fitting or hypothesis family.',membership=summ))
print('SUPPLEMENT',len(out),len(swap),len(single))
