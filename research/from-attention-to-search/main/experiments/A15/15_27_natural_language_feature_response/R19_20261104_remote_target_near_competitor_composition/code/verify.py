from engine import *
from tokenizers import Tokenizer
import re,math
tokenizer=Tokenizer.from_file(str(MODEL/'tokenizer.json'));panel=rows(R/'data/panel.jsonl');portable=rows(R/'data/panel_portable.jsonl');lookup={p['id']:p for p in panel};checks=0
for p,q in zip(panel,portable):
 assert p['id']==q['id'] and p['text']==q['text'] and p['token_ids']==q['token_ids'];enc=tokenizer.encode(p['text'],add_special_tokens=False);assert enc.ids==p['token_ids'] and len(enc.ids)==320;assert p['target_position']==319 and enc.ids[319]==p['target_token_id'];assert 319-p['evidence_last_position']-1==p['actual_distance'];start,end=p['evidence_char_span'];pos=[i for i,(a,b) in enumerate(enc.offsets) if b>start and a<end];assert pos==p['evidence_token_positions'];assert [enc.ids[i] for i in pos]==p['evidence_token_ids'];assert max(pos)==p['evidence_last_position']
 for c in p['candidates']:
  full=tokenizer.encode(p['text']+c['text'],add_special_tokens=False).ids;assert full==c['full_ids'] and full[320:]==c['token_ids'];assert p['token_ids']==full[:320]
 assert len(p['candidates'][0]['token_ids'])==len(p['candidates'][1]['token_ids']);checks+=1
 if p['frame']=='matched_far' and p['split']!='smoke':
  assert p['actual_distance']==128 and p['evidence_last_position']==190
  assert [enc.ids[i] for i in p['near_token_positions']]==p['near_token_ids']
  if p['near_token_positions']:assert p['near_actual_gap']==319-max(p['near_token_positions'])-1
beh={x['id']:x for stage in ['smoke','discovery','heldout'] for x in rows(R/f'results/behavior_{stage}.jsonl')};old=rows(R/'data/R18_scores.jsonl');maxerr=0
for b in old:
 x=beh[b['R19_id']]
 for c,d in zip(x['candidates'],b['candidates']):maxerr=max(maxerr,abs(c['total_logprob']-d['total_logprob']))
assert maxerr<2e-5
for stage in ['smoke','discovery','heldout']:
 a=np.load(R/f'cache/{stage}.npz');assert list(a['ids'])==[p['id'] for p in panel if p['split']==stage]
 for site in SITES:
  ids=a[site+'__indices'];v=a[site+'__values'];assert np.all(v>0) and all(len(set(row))==32 for row in ids);assert np.all(np.isfinite(a[site+'__h']));assert np.all(a[site+'__cutoff32']>=a[site+'__cutoff33'])
for m in rows(R/'results/membership_pairs.jsonl'):
 assert m['intersection']+len(m['entered_ids'])==32 and m['intersection']+len(m['exited_ids'])==32 and len(m['entered_ids'])==len(m['exited_ids']);assert m['union']==64-m['intersection']
for site in SITES:
 for split in ['discovery','heldout']:
  p,z,a=load_stage(split,site);null=np.load(R/f'cache/{site}_{split}_null.npz');ix=per_condition(p)
  for key in null.files:
   if key.startswith('condition') and '_draw' in key:
    k=int(key.split('_')[0].replace('condition',''));orig=a[site+'__indices'][list(ix.values())[k]];snap=null[key];assert all(len(set(row))==32 for row in snap);assert np.array_equal(np.bincount(orig.ravel(),minlength=30000),np.bincount(snap.ravel(),minlength=30000))
  audit=rows(R/f'evidence/{site}_{split}_degree_constraints.jsonl');assert len(audit)==24 and all(x['checks']==64 and x['row32'] and x['column_counts_exact'] for x in audit)
# Small independent set validation of the compiled unchanged reference sampler.
rng=np.random.default_rng(41019);toy=np.stack([rng.choice(96,32,replace=False) for _ in range(8)]);sam=Sampler(toy,41019);sam.advance(100);state=sam.snapshot();sam.close();assert np.array_equal(np.bincount(toy.ravel(),minlength=30000),np.bincount(state.ravel(),minlength=30000));assert all(len(set(r))==32 for r in state)
for path,h in json.load(open(R/'evidence/R18_protected_snapshot.json'))['files'].items():assert sha(path)==h,path
gate=json.load(open(R/'evidence/candidates_and_joint_frozen.json'));start=json.load(open(R/'evidence/heldout_started.json'));assert gate['UTC']<start['UTC']
for path,h in gate['hashes'].items():assert sha(path)==h,path
for path,h in json.load(open(R/'evidence/analysis_code_frozen_before_heldout.json'))['hashes'].items():assert sha(path)==h,path
dump(R/'evidence/verification.json',dict(UTC=now(),status='PASS',retokenized_prefixes=checks,legacy_replayed_prefixes=len(old),max_R18_total_score_error=maxerr,protected_R18_files=len(json.load(open(R/'evidence/R18_protected_snapshot.json'))['files']),sparse_positives_per_row=32,null_degree_checks=2*2*24*64,independent_toy='Python set/column-count checks on saved C++ snapshot PASS',all_legacy_bytes_unchanged=True,selection_precedes_heldout=True,analysis_hashes_unchanged=True,portable_panel_identity=True,model_updates=0,activation_interventions=0))
print('VERIFICATION PASS',checks,maxerr)
