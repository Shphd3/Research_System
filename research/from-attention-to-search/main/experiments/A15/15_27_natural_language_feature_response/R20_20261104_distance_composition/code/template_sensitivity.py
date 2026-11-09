"""The six-template/64-sign sensitivity already specified in Protocol10."""
from common import *
from stats import *
import pandas as pd
p=pd.read_csv(R/'tables/baseline_pair_metrics.csv');f=pd.read_csv(R/'tables/baseline_fact_contrasts.csv');records=[]
for si,site in enumerate(SITES):
 q=p[(p.site==site)&(p.split=='heldout')&(p.distance_left==16)&(p.distance_right==128)];family=q.groupby(['family','template']).retention.mean().reset_index();v=family.groupby('template').retention.mean().to_numpy();lo,hi=interval(v,SEED+si);records.append(dict(site=site,hypothesis='H1',templates=len(v),families=12,value=float(v.mean()),lo=lo,hi=hi,p=sign_p(v-.9)))
 q=f[(f.site==site)&(f.split=='heldout')&(f.view=='native')&(f.distance_left==16)&(f.distance_right==128)];v=q.groupby('template').log_relative_ratio.mean().to_numpy();lo,hi=interval(v,SEED+si);bound=np.log(1.25)
 for hyp,pv in [('H2',max(sign_p(v+bound),sign_p(bound-v))),('H3',sign_p(-v-bound))]:records.append(dict(site=site,hypothesis=hyp,templates=len(v),families=12,value=float(np.exp(v.mean())),lo=float(np.exp(lo)),hi=float(np.exp(hi)),p=pv))
for r,pv in zip(records,holm([r['p'] for r in records])):
 r['holm_p']=pv
 if r['hypothesis']=='H1':r['verdict']='SUPPORTED' if r['lo']>=.9 and pv<=.05 else 'NOT_SUPPORTED' if r['hi']<.9 else 'INSUFFICIENT'
 elif r['hypothesis']=='H2':r['verdict']='SUPPORTED' if r['lo']>=.8 and r['hi']<=1.25 and pv<=.05 else 'NOT_SUPPORTED' if r['lo']>1.25 or r['hi']<.8 else 'INSUFFICIENT'
 else:r['verdict']='SUPPORTED' if r['hi']<.8 and pv<=.05 else 'NOT_SUPPORTED' if r['lo']>.8 else 'INSUFFICIENT'
dump(R/'results/template_sensitivity.json',dict(UTC=now(),source='Predeclared Protocol10; supporting sensitivity, never replaces family-primary verdict',records=records,exact_sign_patterns=64,smallest_possible_Holm_for_smallest_p=6/64,primary_unchanged=True));table(R/'tables/template_sensitivity.csv',records);print(json.dumps(records))
