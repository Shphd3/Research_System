"""Requested descriptive proportions/support, without additional hypothesis tests."""
from common import *
from stats import *
import pandas as pd
out=[];summ=[]
for stage in ['baseline','controls']:
 path=R/f'tables/{stage}_frequency_pairs.csv'
 if not path.exists():continue
 f=pd.read_csv(path);m=pd.read_csv(R/f'tables/{stage}_member_values.csv')
 for (site,frame,split,fam,gold,lo,hi),q in f.groupby(['site','frame','split','family','gold','distance_left','distance_right']):
  raw=m[(m.site==site)&(m.frame==frame)&(m.family==fam)&(m.gold==gold)&(m.distance_left==lo)&(m.distance_right==hi)]
  for _,r in q.iterrows():
   rm=raw[raw.group==r.group];o=dict(site=site,frame=frame,split=split,family=fam,template=r.template,gold=gold,distance_left=int(lo),distance_right=int(hi),group=r.group,common_share=float(r.shared/q.shared.sum()) if q.shared.sum() else None,entry_share=float(r.entered/q.entered.sum()) if q.entered.sum() else None,exit_share=float(r.exited/q.exited.sum()) if q.exited.sum() else None,entries_per_dictionary_opportunity=float(r.entered/r.dictionary_entry_opportunities) if r.dictionary_entry_opportunities else None,mean_active_z_left=float(r.sum_z_left/r.left_at_risk) if r.left_at_risk else None,mean_active_z_right=float(r.sum_z_right/r.right_active) if r.right_active else None,sum_unit_abs_delta=float(np.sum(abs(rm.unit_right-rm.unit_left))),positions_left=int(r.left_at_risk),positions_right=int(r.right_active),positive_change_members=int(sum(rm.delta>0)),negative_change_members=int(sum(rm.delta<0)))
   out.append(o)
table(R/'tables/frequency_roles.csv',out);df=pd.DataFrame(out)
for (site,frame,split,lo,hi,group),q in df.groupby(['site','frame','split','distance_left','distance_right','group']):
 for field in ['common_share','entry_share','exit_share','mean_active_z_left','mean_active_z_right','sum_unit_abs_delta']:
  if q[field].notna().any():summ.append(dict(site=site,frame=frame,split=split,distance_left=int(lo),distance_right=int(hi),group=group,metric=field,**summarize(q,field)))
table(R/'tables/frequency_role_summaries.csv',summ);print('ROLE_PROPORTIONS',len(out),len(summ))
