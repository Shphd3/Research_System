from common import *
from stats import *
import pandas as pd
bp=pd.read_csv(R/'tables/baseline_pair_metrics.csv');bc=pd.read_csv(R/'tables/baseline_fact_contrasts.csv');cp=pd.read_csv(R/'tables/controls_pair_metrics.csv');cc=pd.read_csv(R/'tables/controls_fact_contrasts.csv');mapping=json.load(open(R/'data/condition_mapping.json'));meta={p['id']:p for p in rows(R/'data/panel.jsonl')};out=[];offset=[]
for site in SITES:
 for frame in sorted(cp.frame.unique()):
  for lo,hi in PAIRS:
   old=bp[(bp.site==site)&(bp.split=='heldout')&(bp.distance_left==lo)&(bp.distance_right==hi)].groupby('family').mean(numeric_only=True);new=cp[(cp.site==site)&(cp.frame==frame)&(cp.distance_left==lo)&(cp.distance_right==hi)].groupby('family').mean(numeric_only=True)
   for fam in new.index:
    for metric in ['shared','log_full_norm_ratio','cosine_common']:out.append(dict(site=site,frame=frame,family=fam,template=meta[cid(frame,fam,lo,'A')]['template'],distance_left=lo,distance_right=hi,metric=metric,baseline=float(old.loc[fam,metric]),control=float(new.loc[fam,metric]),difference=float(new.loc[fam,metric]-old.loc[fam,metric])))
   for view in ['native','six','pre_relu','hidden']:
    old=bc[(bc.site==site)&(bc.split=='heldout')&(bc.view==view)&(bc.distance_left==lo)&(bc.distance_right==hi)].set_index('family');new=cc[(cc.site==site)&(cc.frame==frame)&(cc.view==view)&(cc.distance_left==lo)&(cc.distance_right==hi)].set_index('family')
    for fam in new.index:
     for metric in ['log_relative_ratio','log_raw_ratio','raw_contrast_cosine']:out.append(dict(site=site,frame=frame,family=fam,template=meta[cid(frame,fam,lo,'A')]['template'],distance_left=lo,distance_right=hi,metric=view+'_'+metric,baseline=float(old.loc[fam,metric]),control=float(new.loc[fam,metric]),difference=float(new.loc[fam,metric]-old.loc[fam,metric])))
table(R/'tables/control_family_differences.csv',out);summary=[];df=pd.DataFrame(out)
for (site,frame,lo,hi,metric),q in df.groupby(['site','frame','distance_left','distance_right','metric']):summary.append(dict(site=site,frame=frame,distance_left=int(lo),distance_right=int(hi),metric=metric,**summarize(q,'difference')))
table(R/'tables/control_effect_differences.csv',summary)
# Uniform position-ID shift: compare exact same prefixes, not only distance summaries.
from load_data import load_site,behavior
b=behavior(True)
for site in SITES:
 data,dn=load_site(site,True)
 for fam,dd in mapping['pos64'].items():
  for d in DISTS:
   for gold in 'AB':
    pid=dd[str(d)][gold];oldid=cid('baseline',fam,d,gold);x=data[oldid];y=data[pid];sx=set(x['indices']);sy=set(y['indices']);offset.append(dict(site=site,family=fam,distance=d,gold=gold,id=pid,source_id=oldid,target_text_position=319,target_position_id=383,evidence_text_position=meta[pid]['evidence_last_position'],evidence_position_id=meta[pid]['position_id_evidence'],shared=len(sx&sy),max_h_error=float(np.max(abs(y['h']-x['h']))),relative_h_error=float(np.linalg.norm(y['h']-x['h'])/np.linalg.norm(x['h'])),max_z_error=float(np.max(abs(y['z']-x['z']))),correct_margin_error=float(b[pid]['correct_margin']-b[oldid]['correct_margin']),max_candidate_total_error=float(max(abs(c['total_logprob']-a['total_logprob']) for c,a in zip(b[pid]['candidates'],b[oldid]['candidates'])))))
table(R/'tables/position_id_shift_audit.csv',offset)
print('CONTROLS',len(out),len(offset))
