from common import *
from stats import *
import pandas as pd
rows_out=[];atlas=[];summary=[]
for stage in ['baseline','controls']:
 path=R/f'tables/{stage}_member_values.csv'
 if not path.exists():continue
 m=pd.read_csv(path)
 for (site,frame,split,fam,lo,hi),q in m.groupby(['site','frame','split','family','distance_left','distance_right']):
  changed=q[q.status!='common'];entry=changed[changed.status=='entered'];exit=changed[changed.status=='exited'];rows_out.append(dict(site=site,frame=frame,split=split,family=fam,template=q.template.iloc[0],distance_left=int(lo),distance_right=int(hi),turnover_instances=len(changed),near_cutoff_fraction=float(changed.near_cutoff.mean()) if len(changed) else None,entry_prepositive_fraction=float(entry.was_subthreshold_positive.mean()) if len(entry) else None,exit_prepositive_fraction=float(exit.still_subthreshold_positive.mean()) if len(exit) else None,mean_prechange_over_cutoff=float(changed.prechange_over_cutoff.mean()) if len(changed) else None))
 for (site,frame,split,lo,hi,group,atom),q in m.groupby(['site','frame','split','distance_left','distance_right','group','atom']):
  en=q[q.status=='entered'];ex=q[q.status=='exited'];co=q[q.status=='common'];atlas.append(dict(site=site,frame=frame,split=split,distance_left=int(lo),distance_right=int(hi),group=group,atom=int(atom),entered_positions=len(en),entered_families=len(set(en.family)),exited_positions=len(ex),exited_families=len(set(ex.family)),common_positions=len(co),common_families=len(set(co.family)),families=len(set(q.family)),entered_mean_z=float(en.z_right.mean()) if len(en) else None,exited_mean_z=float(ex.z_left.mean()) if len(ex) else None,mean_delta=float(q.delta.mean()),families_entered=sorted(set(en.family)),families_exited=sorted(set(ex.family))))
table(R/'tables/threshold_family.csv',rows_out);table(R/'tables/feature_turnover_atlas.csv',atlas);df=pd.DataFrame(rows_out)
for (site,frame,split,lo,hi),q in df.groupby(['site','frame','split','distance_left','distance_right']):
 for field in ['near_cutoff_fraction','entry_prepositive_fraction','exit_prepositive_fraction','mean_prechange_over_cutoff']:summary.append(dict(site=site,frame=frame,split=split,distance_left=int(lo),distance_right=int(hi),metric=field,**summarize(q,field)))
table(R/'tables/threshold_summaries.csv',summary)
print('DESCRIPTIVE',len(atlas),len(summary))
