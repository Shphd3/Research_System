from load_data import *
from stats import *
import pandas as pd,sys
stage=sys.argv[1] if len(sys.argv)>1 else 'baseline';members=pd.read_csv(R/f'tables/{stage}_member_values.csv');pairs=pd.read_csv(R/f'tables/{stage}_pair_metrics.csv');out=[];coverage=[]
def conditional_counts(weights,left,m,gi,seed):
 w=weights.copy();w[left]=0;total=w.sum()
 if total<=0 or np.count_nonzero(w)<m:return None
 if m==0:return np.zeros(5),np.zeros(5)
 cdf=np.cumsum(w/total);cdf[-1]=1.;rng=np.random.default_rng(seed);sample=np.searchsorted(cdf,rng.random((512,m)),side='right');counts=np.zeros((512,5))
 for row in range(512):
  seen=set()
  for j in range(m):
   f=int(sample[row,j])
   while f in seen:f=int(np.searchsorted(cdf,rng.random(),side='right'))
   seen.add(f);counts[row,gi[f]]+=1
 return counts.mean(0),counts.std(0,ddof=1)/np.sqrt(512)
for si,site in enumerate(SITES):
 data,dn=load_site(site,stage=='controls');reference=pd.read_csv(R/f'data/{site}_reference_frequency.csv');labels=reference['group'].to_numpy();gi=np.array([GROUPS.index(g) for g in labels]);refweights=reference.frequency.to_numpy();taskcount=np.zeros(30000)
 for pid,a in data.items():
  if META[pid]['provenance']=='R19_REUSE' and META[pid]['split']=='discovery':taskcount[a['indices']]+=1
 taskweights=taskcount+32*refweights
 if stage=='baseline':np.savez_compressed(R/f'cache/{site}_opportunity_weights.npz',reference=refweights,discovery_counts=taskcount,task_weights=taskweights,groups=gi)
 for split in ['discovery','heldout']:
  for frame in sorted(set(members.frame)):
   selected=[pid for fam,dd in MAP[frame].items() for d in DISTS for pid in dd[str(d)].values() if pid in data and META[pid]['split']==split]
   for group in GROUPS:
    ii=np.where(labels==group)[0];observed=[]
    for pid in selected:
     active=[f for f in data[pid]['indices'] if labels[f]==group]
     if active:observed.append((pid,active))
    coverage.append(dict(site=site,frame=frame,split=split,group=group,dictionary_members=len(ii),reference_positive_mass=float(refweights[ii].sum()),discovery_task_positive_mass=float(taskweights[ii].sum()),observed_members=len({int(f) for pid,v in observed for f in v}),positions=len(observed),position_denominator=len(selected),families=len({META[pid]['family'] for pid,v in observed}),active_instances=sum(len(v) for pid,v in observed)))
 for k,r in pairs[pairs.site==site].reset_index(drop=True).iterrows():
  l=data[r.left_id];left=l['indices'];leftgroup=labels[left];m=int(r.entered);seed=SEED+si*1000000+k*30+(0 if stage=='baseline' else 10000000);ref=conditional_counts(refweights,left,m,gi,seed);task=conditional_counts(taskweights,left,m,gi,seed+1);q=members[(members.site==site)&(members.left_id==r.left_id)&(members.right_id==r.right_id)&(members.frame==r.frame)];totalabs=q.abs_decoder_weighted_change.sum();poolcounts=np.bincount(gi,minlength=5)-np.bincount(gi[left],minlength=5)
  for g,group in enumerate(GROUPS):
   a=q[q.group==group];entered=a[a.status=='entered'];exited=a[a.status=='exited'];common=a[a.status=='common'];at_risk=sum(leftgroup==group);rank_expected=0.
   for low,high in [(1,8),(9,16),(17,24),(25,32)]:
    binrows=q[(q.rank_left>=low)&(q.rank_left<=high)];exits=sum(binrows.status=='exited');rank_expected+=exits*sum(binrows.group==group)/8
   re=None if ref is None else float(ref[0][g]);te=None if task is None else float(task[0][g]);row=dict(site=site,frame=r.frame,split=r.split,family=r.family,template=r.template,gold=r.gold,distance_left=int(r.distance_left),distance_right=int(r.distance_right),group=group,shared=len(common),entered=len(entered),exited=len(exited),left_at_risk=int(at_risk),left_active_share=float(at_risk/32),exit_rate=float(len(exited)/at_risk) if at_risk else None,right_active=int(len(common)+len(entered)),dictionary_entry_opportunities=int(poolcounts[g]),dictionary_expected_entries=float(m*poolcounts[g]/(30000-32)),reference_expected_entries=re,reference_MCSE=None if ref is None else float(ref[1][g]),task_expected_entries=te,task_MCSE=None if task is None else float(task[1][g]),reference_entry_excess=None if re is None else float(len(entered)-re),task_entry_excess=None if te is None else float(len(entered)-te),reference_OE=float(len(entered)/re) if re and re>0 else None,task_OE=float(len(entered)/te) if te and te>0 else None,reference_zero_expectation=bool(re==0),task_zero_expectation=bool(te==0),uniform_expected_exits=float(m*at_risk/32),rank_matched_expected_exits=float(rank_expected),rank_matched_exit_excess=float(len(exited)-rank_expected),sum_z_left=float(a.z_left.sum()),sum_z_right=float(a.z_right.sum()),sum_delta=float(a.delta.sum()),common_mean_left=float(common.z_left.mean()) if len(common) else None,common_mean_right=float(common.z_right.mean()) if len(common) else None,common_mean_delta=float(common.delta.mean()) if len(common) else None,entered_mean_z=float(entered.z_right.mean()) if len(entered) else None,exited_mean_z=float(exited.z_left.mean()) if len(exited) else None,abs_raw_change=float(a.abs_raw_change.sum()),abs_decoder_weighted_change=float(a.abs_decoder_weighted_change.sum()),absolute_change_share=float(a.abs_decoder_weighted_change.sum()/totalabs) if totalabs>0 else None,entered_prepositive=int(entered.was_subthreshold_positive.sum()),exited_prepositive=int(exited.still_subthreshold_positive.sum()),near_cutoff_turnover=int(q[(q.group==group)&(q.status!='common')].near_cutoff.sum()),turnover=len(entered)+len(exited))
   out.append(row)
table(R/f'tables/{stage}_frequency_pairs.csv',out);table(R/f'tables/{stage}_frequency_coverage.csv',coverage)
df=pd.DataFrame(out);summary=[]
for (site,frame,split,lo,hi,group),q in df.groupby(['site','frame','split','distance_left','distance_right','group']):
 for metric in ['shared','entered','exited','exit_rate','reference_expected_entries','task_expected_entries','reference_entry_excess','task_entry_excess','rank_matched_exit_excess','common_mean_delta','entered_mean_z','exited_mean_z','absolute_change_share']:
  if q[metric].notna().any():summary.append(dict(site=site,frame=frame,split=split,distance_left=int(lo),distance_right=int(hi),group=group,metric=metric,**summarize(q,metric)))
table(R/f'tables/{stage}_frequency_summaries.csv',summary)
print('FREQUENCY',stage,len(out),len(summary),flush=True)
