from common import *
import numpy as np,math
from tokenizers import Tokenizer
plan=json.load(open(R/'frozen_plan.json'));freeze=json.load(open(R/'evidence/protocol_freeze.json'));run=json.load(open(R/'evidence/run_complete.json'));panel=rows(R/'data/panel.jsonl');oldpanel=rows(R/'data/S03_original_panel.jsonl');T=Tokenizer.from_file(str(Path(plan['model'])/'tokenizer.json'))
for n,h in freeze['protocol_SHA256'].items():assert sha(R/n)==h
for n,h in freeze['code_SHA256'].items():assert sha(R/'code'/n)==h
for n,h in plan['data_SHA256'].items():assert sha(R/'data'/n)==h
assert sha(OLD/'results/selection.json')==plan['selection_SHA256']==sha(R/'data/S03_frozen_selection.json')
protected=json.load(open(R/'evidence/old_immutable_before.json'))
for p,h in protected.items():assert sha(p)==h
for p,o in zip(panel,oldpanel):
 assert p['text']==o['text'] and p['labels']==o['labels'] and p['family']==o['family'] and p['split']==o['split']
 assert p['prefix']==p['text']+'\nDescription:' and T.encode(p['prefix'],add_special_tokens=False).ids==p['token_ids']
 assert p['target_token_id']==25 and p['target_token_text']==':' and p['target_index_zero_based']==len(p['token_ids'])-1
 for c in p['candidates']:assert T.encode(p['prefix']+c['text'],add_special_tokens=False).ids==c['full_input_token_ids']==p['token_ids']+c['token_ids']
for f in range(6):assert len(set(p['target_index_zero_based'] for p in panel[f*4:f*4+4]))==1
raw=rows(R/'results/behavior_raw.jsonl');assert len(raw)==24
for p,b in zip(panel,raw):
 assert p['prefix']==b['prefix'] and p['token_ids']==b['prefix_token_ids']
 assert b['gold']==(p['condition'] if p['condition'] in ['cat','dog'] else None)
 for x in b['candidates']:assert abs(math.fsum(x['token_logprobs'])-x['total_logprob'])<1e-12 and x['token_count']==2
 d=b['candidates'][0]['total_logprob']-b['candidates'][1]['total_logprob'];assert d==b['delta_cat_minus_dog'];choice='cat' if d>=0 else 'dog';assert choice==b['choice']
 assert b['correct']==(None if b['gold'] is None else choice==b['gold'])
new=np.load(R/'cache/new.npz');selection=json.load(open(R/'data/S03_frozen_selection.json'))['sites'];counts=list(csv.DictReader(open(R/'results/H2_direction_counts.csv')));summaries={};nvalues=0;nh2=0;ntrans=0
def sg(v):return None if not np.isfinite(v) else 0 if abs(v)<=1e-8 else int(np.sign(v))
for site in SITES:
 z=new[site+'__z'].astype(float);pre=new[site+'__pre'].astype(float);ids=new[site+'__topk_indices'];norm=new[site+'__decoder_norm'].astype(float)
 assert z.shape==(24,30000) and len(new['ids'])==24
 for j in range(24):
  assert len(set(ids[j]))==32 and bool((z[j]>=0).all())
  assert np.array_equal(z[j,ids[j]],np.maximum(pre[j,ids[j]],0))
  mask=np.ones(30000,bool);mask[ids[j]]=False;assert not z[j,mask].any();assert np.maximum(pre[j,mask],0).max()<=z[j,ids[j]].min()
 old=np.concatenate([np.load(OLD/f'cache/{sp}.npz')[site+'__z'] for sp in ['exploration','heldout_check']]).astype(float);H2=selection[site]['H2'];ow=old[:,H2]*norm[H2];nw=z[:,H2]*norm[H2]
 on=np.linalg.norm(ow,axis=1);nn=np.linalg.norm(nw,axis=1);oq=np.divide(ow,on[:,None],out=np.full_like(ow,np.nan),where=on[:,None]>0);nq=np.divide(nw,nn[:,None],out=np.full_like(nw,np.nan),where=nn[:,None]>0)
 oldcsv=list(csv.DictReader(open(OLD/f'results/{site}/H2_directions.csv')));hh=list(csv.DictReader(open(R/f'results/{site}/H2_old_new_pairs.csv')))
 for h in hh:
  fi=int(h['family'][1:])-1;j=H2.index(int(h['atom']));a=fi*4+1;b=fi*4+2
  assert abs(float(h['old_raw_delta'])-(old[a,H2[j]]-old[b,H2[j]]))<1e-12 and abs(float(h['new_raw_delta'])-(z[a,H2[j]]-z[b,H2[j]]))<1e-12
  for key,v in [('old_q_delta',oq[a,j]-oq[b,j]),('new_q_delta',nq[a,j]-nq[b,j])]:
   if np.isfinite(v):assert abs(float(h[key])-v)<1e-12
   else:assert h[key]==''
  oo=next(x for x in oldcsv if x['atom']==h['atom'] and x['family']==h['family']);assert abs(float(oo['weighted_q_difference'])-float(h['old_q_delta']))<1e-12
  nh2+=1
 for ct in [x for x in counts if x['site']==site]:
  hh0=[x for x in hh if x['atom']==ct['atom'] and x['split']==ct['split']];expected={s:0 for s in ['same','opposite','member_inactive','zero_norm','no_reference','zero_difference']}
  for h in hh0:
   normalized=ct['metric']=='q_weighted';ctx=ct['reference'];i=int(h['atom']);fi=int(h['family'][1:])-1;a=fi*4+1;b=fi*4+2;j=H2.index(i)
   od=(oq[a,j]-oq[b,j]) if normalized else old[a,i]-old[b,i];nd=(nq[a,j]-nq[b,j]) if normalized else z[a,i]-z[b,i]
   reference=sg(od) if ctx=='old_pair' else selection[site]['H2_discovery_direction'][str(i)] if normalized else sg(plan['old_raw_discovery_mean_difference'][site][str(i)])
   zero=normalized and (nn[a]==0 or nn[b]==0 or (ctx=='old_pair' and (on[a]==0 or on[b]==0)))
   inactive=not(z[a,i]>0 and z[b,i]>0) or (ctx=='old_pair' and not(old[a,i]>0 and old[b,i]>0))
   status='zero_norm' if zero else 'member_inactive' if inactive else 'no_reference' if reference in [None,0] else 'zero_difference' if sg(nd)==0 else 'same' if sg(nd)==reference else 'opposite'
   expected[status]+=1
  assert sum(expected.values())==3 and all(int(ct[k])==v for k,v in expected.items())
 for v in csv.DictReader(open(R/f'results/{site}/candidate_values.csv')):
  row=next(j for j,p in enumerate(panel) if p['id']==v['id']);atom=int(v['atom']);zz=z if v['context']=='new' else old
  assert abs(float(v['z'])-zz[row,atom])<1e-12 and abs(float(v['u'])-zz[row,atom]*norm[atom])<1e-12;nvalues+=1
 for tr in csv.DictReader(open(R/f'results/{site}/support_transitions.csv')):
  fi=int(tr['family'][1:])-1;a=fi*4+CONDS.index(tr['source']);b=fi*4+CONDS.index(tr['destination']);az=old[a] if tr['kind'] in ['old','old_to_new'] else z[a];bz=old[b] if tr['kind']=='old' else z[b];A=set(np.flatnonzero(az));B=set(np.flatnonzero(bz));assert int(tr['retained'])==len(A&B) and int(tr['zero_to_positive'])==len(B-A) and int(tr['positive_to_zero'])==len(A-B);ntrans+=1
 sums={}
 for group,ii in [('H1_common',selection[site]['H1_common']),('H1_added_cat',selection[site]['H1_added']['cat']),('H1_added_dog',selection[site]['H1_added']['dog']),('H2',H2)]:sums[group]=int((np.linalg.norm(z[:,ii]*norm[ii],axis=1)==0).sum())
 summaries[site]=dict(rows=24,all_positive_counts=(z>0).sum(1).tolist(),zero_norm_by_list=sums,min_Top32_margin=float((new[site+'__cutoff32']-new[site+'__cutoff33']).min()),exact_Top32_boundary_ties=int((new[site+'__cutoff32']==new[site+'__cutoff33']).sum()))
assert run['hook_noop_checks'][0]['noop_native_state_max_difference']==0 and run['max_duplicate_lane_difference']<1e-6
dump(R/'evidence/verification.json',dict(UTC=now(),status='PASS',body_changes=0,old_files_unchanged=len(protected),candidate_reselection=0,selection_unchanged=True,tokenization_rows=24,candidate_token_sums=48,H2_pair_replays=nh2,direction_count_rows=len(counts),candidate_value_replays=nvalues,support_transition_replays=ntrans,S03_H2_old_q_exact=True,sites=summaries,scientific_acceptance='Unknown',next_experiment='NOT_RUN_WAIT_FOR_JOINT_REVIEW'))
print('S04_VERIFIED',len(protected),nvalues,nh2,ntrans,flush=True)
