from common import *
import pandas as pd
p=pd.read_csv(R/'tables/baseline_pair_metrics.csv');f=pd.read_csv(R/'tables/baseline_fact_contrasts.csv');q=p[(p.split=='heldout')&(p.distance_left==16)&(p.distance_right==128)];ret=q.groupby('family').retention.mean();z=f[(f.split=='heldout')&(f.view=='native')&(f.distance_left==16)&(f.distance_right==128)].pivot(index='family',columns='site',values='log_relative_ratio');score=z.mean(1);selected=[]
def take(values,ascending,role,reason):
 candidates=[(float(v),str(fam)) for fam,v in values.items() if fam not in [x['family'] for x in selected]];candidates.sort(key=lambda x:((x[0] if ascending else -x[0]),x[1]));value,fam=candidates[0];selected.append(dict(role=role,family=fam,selection_value=value,reason=reason));return fam
take(ret,False,'relatively_stable','Largest mean16→128retained fraction across sites/facts; ties family ID')
take(ret,True,'larger_turnover','Smallest retained fraction among unselected families')
take(score,True,'smaller_fact_contrast_change','Smallest mean log normalized fact-separation ratio among unselected families; may still be positive')
median=float(score.median());opposite=score[score*median<0];available=[fam for fam in opposite.index if fam not in [x['family'] for x in selected]]
if available:take(opposite.loc[available].abs(),False,'counter_to_pooled_trend','Largest absolute opposite-sign family log ratio')
else:take((z[SITES[0]]-z[SITES[1]]).abs(),False,'site_disagreement_fallback','No remaining family opposite to pooled median; largest between-site log-ratio disagreement')
dump(R/'results/case_selection.json',dict(UTC=now(),source='R19reanalysis only; not supplemental outcomes',frozen_rule_source=str(C/'protocol.md'),median_pooled_log_ratio=median,no_remaining_opposite=not bool(available),families=selected,all_family_selection_inputs=[dict(family=fam,retention=float(ret[fam]),mean_log_ratio=float(score[fam]),ATTN_log_ratio=float(z.loc[fam,SITES[0]]),MLPIN_log_ratio=float(z.loc[fam,SITES[1]])) for fam in ret.index]))
print('CASES',selected)
