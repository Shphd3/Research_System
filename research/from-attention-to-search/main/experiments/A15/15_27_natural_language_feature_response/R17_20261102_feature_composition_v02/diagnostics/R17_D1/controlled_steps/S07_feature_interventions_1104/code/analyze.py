from common import *
import numpy as np,itertools,math,collections
assert (R/'evidence/run_complete.json').exists()
rr=rows(R/'results/conditions.jsonl');bykey={(r['text_id'],r['site'],r['intervention_domain'],r['arm'],r['group'],r['alpha'],r['destination']):r for r in rr};rng=np.random.default_rng(20261104)
def ci(v):
 if not v:return [None,None]
 v=np.array(v,float);bt=v[rng.integers(len(v),size=(4096,len(v)))].mean(1);return [float(a) for a in np.quantile(bt,[.025,.975])]
def pval(v):
 if not v:return 1.
 x=np.array(v);sg=np.array(list(itertools.product([-1,1],repeat=len(x))));return float(np.mean(sg@x/len(x)>=x.mean()-1e-12))
def find(r,arm):return bykey[(r['text_id'],r['site'],r['intervention_domain'],arm,r['group'],r['alpha'] if arm.startswith('strength') else None,r['destination'] if arm.startswith('strength') else None)]
primary=[];families=[];pertext=[]
for s,d,kind in itertools.product(SITES,DOMAINS,['delete','strength']):
 candidates=[r for r in rr if r['site']==s and r['intervention_domain']==d and r['wording']=='explicit' and r['label'] in DOMAINS[d][1:] and r['arm']==kind and r['group']=='common' and (kind=='delete' or r['alpha']==.5 and r['destination']!=r['label'])]
 vals=[];rawvals=[];ctrlvals=[]
 for f in [f'F{i:02d}' for i in range(9,17)]:
  rowsf=[r for r in candidates if r['family']==f];eligible=[];obs=[];control=[]
  for r in rowsf:
   c=find(r,'delete_matched' if kind=='delete' else 'strength_shuffle');loss=-r['correct_margin_change'];closs=-c['correct_margin_change']
   ok=bool(c['discovery_matched'] and r['active_before']==c['active_before'] and r['delta_hidden_L2']>0) if kind=='delete' else bool(r['support_preserved'] and c['support_preserved'] and r['active_before']>=2 and c['norm_ratio'] is not None and .9<=c['norm_ratio']<=1.1)
   pertext.append(dict(site=s,domain=d,kind=kind,family=f,text_id=r['text_id'],label=r['label'],eligible=ok,margin_loss=loss,control_margin_loss=closs,specificity_difference=loss-closs,candidate_delta_norm=r['delta_hidden_L2'],control_delta_norm=c['delta_hidden_L2'],candidate_active=r['active_before'],control_active=c['active_before'],candidate_correct=r['sibling_correct'],control_correct=c['sibling_correct'],candidate_id=r['condition_id'],control_id=c['condition_id']))
   obs.append(loss);control.append(closs);eligible.append(ok)
  ok=len(rowsf)==2 and all(eligible);raw=float(np.mean(obs));con=float(np.mean(control));effect=raw-con
  families.append(dict(site=s,domain=d,kind=kind,family=f,eligible=ok,margin_loss=raw,control_margin_loss=con,specificity_difference=effect))
  rawvals.append(raw);ctrlvals.append(con)
  if ok:vals.append(effect)
 lo,hi=ci(vals);rlo,rhi=ci(rawvals);primary.append(dict(site=s,domain=d,kind=kind,eligible_families=len(vals),N=8,specificity_mean=float(np.mean(vals)) if vals else None,specificity_ci_low=lo,specificity_ci_high=hi,p=pval(vals),p_holm=None,raw_margin_loss_mean=float(np.mean(rawvals)),raw_ci_low=rlo,raw_ci_high=rhi,control_margin_loss_mean=float(np.mean(ctrlvals)),raw_p=pval(rawvals),raw_positive_families=int(np.sum(np.array(rawvals)>0))))
primary.sort(key=lambda r:r['p']);v=0
for i,r in enumerate(primary):v=max(v,min(1.,r['p']*(8-i)));r['p_holm']=v;r['specificity_status']='INSUFFICIENT_MATCH_OR_SUPPORT' if r['eligible_families']<6 else 'LOCAL_DIRECTION_SPECIFIC_EFFECT' if r['specificity_mean']>0 and r['specificity_ci_low']>0 and v<=.05 else 'NOT_SUPPORTED_BY_PRIMARY'
table(R/'results/primary.csv',primary);dump(R/'results/primary.json',primary);table(R/'results/family_primary.csv',families);table(R/'results/per_text_primary.csv',pertext)

# Class, off-domain and dose summaries; every condition remains present.
groups=collections.defaultdict(list)
for r in rr:
 if r['arm']=='identity':continue
 if r['arm'].startswith('strength') and r['gold'] and r['label'] in DOMAINS[r['intervention_domain']][1:] and r['destination']==r['label']:direction='own_destination'
 elif r['arm'].startswith('strength') and r['gold'] and r['label'] in DOMAINS[r['intervention_domain']][1:]:direction='opposite_destination'
 else:direction='both_destinations_or_deletion'
 cohort='target_children' if r['label'] in DOMAINS[r['intervention_domain']][1:] else 'other_children' if r['gold'] else 'parent_or_negative'
 key=(r['site'],r['intervention_domain'],r['arm'],r['group'],r['alpha'],r['wording'],r['label'],cohort,direction);groups[key].append(r)
summ=[]
for key,rs in groups.items():
 s,d,arm,g,a,w,label,cohort,direction=key;fam=collections.defaultdict(list)
 for r in rs:
  if r['correct_margin_change'] is not None:fam[r['family']].append(-r['correct_margin_change'])
 vv=[float(np.mean(v)) for v in fam.values()];lo,hi=ci(vv);summ.append(dict(site=s,domain=d,arm=arm,group=g,alpha=a,wording=w,label=label,cohort=cohort,direction=direction,N_text_conditions=len(rs),families=len(fam),margin_loss_mean=float(np.mean(vv)) if vv else None,ci_low=lo,ci_high=hi,correct=sum(r['sibling_correct'] is True for r in rs) if vv else None,denominator=len(rs) if vv else None,mean_delta_norm=float(np.mean([r['delta_hidden_L2'] for r in rs])),mean_active=float(np.mean([r['active_before'] for r in rs])),mean_KL=float(np.mean([r['KL_new_vs_baseline'] for r in rs])),mean_entropy=float(np.mean([r['entropy_nats'] for r in rs])),support_preserved=sum(r['support_preserved'] for r in rs),norm_matched=sum(r['norm_ratio'] is not None and .9<=r['norm_ratio']<=1.1 for r in rs),discovery_matched=sum(r['discovery_matched'] for r in rs),outside_discovery_any=sum((r['outside_discovery_coordinates'] or 0)>0 for r in rs)))
table(R/'results/class_and_dose_summary.csv',summ)
match=[]
for s,d,arm in itertools.product(SITES,DOMAINS,['delete_matched','norm_random_add','strength_shuffle','strength_own','strength_other']):
 rs=[r for r in rr if r['site']==s and r['intervention_domain']==d and r['arm']==arm and r['wording']=='explicit' and r['label'] in DOMAINS[d][1:] and (not arm.startswith('strength') or r['alpha']==.5 and r['destination']!=r['label'])]
 if not rs:continue
 match.append(dict(site=s,domain=d,arm=arm,conditions=len(rs),discovery_qualified=sum(r['discovery_matched'] for r in rs),pure_support=sum(r['support_preserved'] for r in rs),norm_ratio_matched=sum(r['norm_ratio'] is not None and .9<=r['norm_ratio']<=1.1 for r in rs),min_norm_ratio=min((r['norm_ratio'] for r in rs if r['norm_ratio'] is not None),default=None),max_norm_ratio=max((r['norm_ratio'] for r in rs if r['norm_ratio'] is not None),default=None)))
table(R/'results/control_quality.csv',match)
# Compact full-rank/distribution table for all prespecified first-token candidates.
rankrows=[]
for r in rr:
 for j,l in enumerate(r['candidate_order']):rankrows.append(dict(condition_id=r['condition_id'],text_id=r['text_id'],site=r['site'],intervention_domain=r['intervention_domain'],family=r['family'],wording=r['wording'],label=r['label'],arm=r['arm'],group=r['group'],alpha=r['alpha'],destination=r['destination'],candidate=l,vocabulary_rank=r['candidate_vocab_ranks'][j],p_full_vocab=r['candidate_vocab_prob'][j],full_sequence_logprob=r['scores'][j],p_four_sequences=r['candidate_sequence_prob4'][j]))
table(R/'results/candidate_ranks_and_probabilities.csv',rankrows)
# Fixed F09 examples plus first effect opposing expected margin loss (or explicit absence).
chosen=[]
for s,d,kind in itertools.product(SITES,DOMAINS,['delete','strength']):
 rs=[r for r in pertext if r['site']==s and r['domain']==d and r['kind']==kind];bad=next((r for r in rs if r['margin_loss']<=0),None);r=bad or min(rs,key=lambda r:r['margin_loss']);chosen.append(dict(site=s,domain=d,kind=kind,text_id=r['text_id'],family=r['family'],label=r['label'],margin_loss=r['margin_loss'],reason='first_nonpositive_margin_loss' if bad else 'none_nonpositive;least_positive',condition_id=r['candidate_id']))
dump(R/'results/counterexamples.json',chosen)
# Distributional specificity: how much do original unrelated children move under the same intervention.
off=[]
for s,d,kind in itertools.product(SITES,DOMAINS,['delete','strength']):
 rs=[r for r in rr if r['site']==s and r['intervention_domain']==d and r['arm']==kind and r['group']=='common' and r['wording']=='explicit' and (kind=='delete' or r['alpha']==.5)]
 for cohort in ['target','offdomain','parent_negative']:
  ss=[r for r in rs if (r['label'] in DOMAINS[d][1:] if cohort=='target' else r['gold'] is not None and r['label'] not in DOMAINS[d][1:] if cohort=='offdomain' else r['gold'] is None)]
  if kind=='strength' and cohort=='target':ss=[r for r in ss if r['destination']!=r['label']]
  off.append(dict(site=s,domain=d,kind=kind,cohort=cohort,N=len(ss),mean_abs_score_change=float(np.mean([np.mean(abs(np.array(r['scores'])-r['baseline_scores'])) for r in ss])),mean_KL=float(np.mean([r['KL_new_vs_baseline'] for r in ss])),mean_abs_sibling_margin_change=float(np.mean([abs(r['correct_margin_change']) for r in ss if r['correct_margin_change'] is not None])) if cohort!='parent_negative' else None))
table(R/'results/offdomain_effects.csv',off)
dump(R/'evidence/analysis_complete.json',dict(UTC=now(),conditions=len(rr),primary_tests=8,code_sha256=sha(__file__),observation_exposed_intervention_unseen=True))
print('PRIMARY',json.dumps(primary),flush=True)
