"""Descriptive post-output stratification with the pre-output frequency/format masks; no new forward or fit."""
from pathlib import Path
import json,shutil
import numpy as np,pandas as pd
P=Path(__file__).resolve().parents[1];E=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response')/P.name
r=[json.loads(l) for l in (E/'data/positions.jsonl').read_text().splitlines()];outputs=[json.loads(l) for l in (E/'analysis/raw_outputs.jsonl').read_text().splitlines()];df=pd.read_csv(E/'analysis/position_metrics.csv');doc=pd.read_csv(E/'analysis/document_metrics.csv');freq=np.load(E/'data/frequency.npz');base={x['index']:x for x in outputs if x['condition']=='identity'}
meta=[]
for i,x in enumerate(r):
 y=base[i]['top20'][0];ii=y['id'];g='nonlexical' if not freq['valid'][ii] else 'format' if freq['format_mask'][ii] else 'nonformat_common' if freq['group'][ii]==0 else 'nonformat_other'
 meta.append({'index':i,'panel':x['panel'],'seq_id':x['seq_id'],'recovery_group':g,'full_top1_id':ii,'full_top1_fragment':y['fragment'],'full_top1_probability':y['probability'],'full_entropy':base[i]['entropy'],'reference_count':int(freq['counts'][ii])})
md=pd.DataFrame(meta);md.to_csv(E/'analysis/recovery_group_members.csv',index=False);merged=df.merge(md[['index','recovery_group']],on='index');summary=[];coverage=[];rng=np.random.default_rng(20261102)
for panel in ['the','natural']:
 for group in ['format','nonformat_common','nonformat_other','nonlexical']:
  a=md[(md.panel==panel)&(md.recovery_group==group)];coverage.append({'panel':panel,'group':group,'positions':len(a),'documents':a.seq_id.nunique(),'full_top1_probability_mean_position_weighted':float(a.full_top1_probability.mean()) if len(a) else None,'full_entropy_mean_position_weighted':float(a.full_entropy.mean()) if len(a) else None})
  if a.empty:continue
  for cond,z in merged[(merged.panel==panel)&(merged.recovery_group==group)].groupby('condition'):
   d=z.groupby('seq_id')[['top1_agreement','NLL','KL_full']].mean();n=len(d);bs=rng.integers(0,n,(2000,n))
   for metric in ['top1_agreement','NLL','KL_full']:
    v=d[metric].to_numpy();lo,hi=np.quantile(v[bs].mean(1),[.025,.975]);summary.append({'panel':panel,'group':group,'condition':cond,'metric':metric,'mean':float(v.mean()),'ci_low':float(lo),'ci_high':float(hi),'documents':n,'positions':len(z)})
pd.DataFrame(summary).to_csv(E/'analysis/recovery_by_full_top1_type.csv',index=False);pd.DataFrame(coverage).to_csv(E/'analysis/recovery_type_coverage.csv',index=False)
contrasts=[]
for panel in ['the','natural']:
 d=doc[doc.panel==panel];ids=sorted(d.seq_id.unique());bs=rng.integers(0,len(ids),(2000,len(ids)))
 for a,b in [('head_middle','k128'),('head_middle','head_random1034'),('head_middle','head_random1035'),('head_middle','head_random1036'),('head_tail','k128'),('head_tail','head_random1034'),('head_tail','head_random1035'),('head_tail','head_random1036')]:
  for metric in ['NLL','KL_full','centered_energy_fraction']:
   v=(d[d.condition==a].set_index('seq_id').loc[ids,metric]-d[d.condition==b].set_index('seq_id').loc[ids,metric]).to_numpy();lo,hi=np.quantile(v[bs].mean(1),[.025,.975]);contrasts.append({'panel':panel,'condition':a,'control':b,'metric':metric,'difference_condition_minus_control':float(v.mean()),'ci_low':float(lo),'ci_high':float(hi),'documents':len(ids)})
pd.DataFrame(contrasts).to_csv(E/'analysis/addition_control_contrasts.csv',index=False)
for name in ['recovery_group_members.csv','recovery_by_full_top1_type.csv','recovery_type_coverage.csv','addition_control_contrasts.csv']:shutil.copy2(E/'analysis'/name,P/'evidence'/name)
print(pd.DataFrame(coverage).to_string(index=False));print(pd.DataFrame(contrasts).query("metric=='NLL'").round(4).to_string(index=False))
