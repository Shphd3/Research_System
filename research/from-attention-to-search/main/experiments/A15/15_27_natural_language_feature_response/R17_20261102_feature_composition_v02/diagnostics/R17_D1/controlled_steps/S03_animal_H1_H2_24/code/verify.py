"""Independent replay of frozen-token provenance, native sparsity and delivered arithmetic."""
from common import *
import numpy as np
from tokenizers import Tokenizer
plan=json.load(open(R/'frozen_plan.json'));selection=json.load(open(R/'results/selection.json'));freeze=json.load(open(R/'evidence/candidates_frozen_before_heldout.json'))
assert sha(R/'results/selection.json')==freeze['selection_SHA256']
for n,d in freeze['code_SHA256'].items(): assert sha(R/'code'/n)==d
for n,d in json.load(open(R/'evidence/protocol_freeze.json'))['protocol_SHA256'].items():assert sha(R/n)==d
PANEL=rows(R/'data/panel.jsonl');T=Tokenizer.from_file(str(Path(plan['model'])/'tokenizer.json'));old={p['id']:p for p in rows(OLD/'data/panel.jsonl')}
for p in PANEL:
 assert T.encode(p['prefix'],add_special_tokens=False).ids==p['token_ids']
 assert p['target_index_zero_based']==len(p['token_ids'])-1 and p['target_token_id']==264 and p['target_token_text']==' a'
 if p['source_S02_id']:
  o=old[p['source_S02_id']];assert p['text']==o['text'] and p['prefix']==o['prefix']
 if p['condition']=='P':assert p['cat'] is None and p['dog'] is None and p['labels']==['animal']
for f in range(6): assert len({p['target_index_zero_based'] for p in PANEL[f*4:f*4+4]})==1
for p,d in json.load(open(R/'evidence/old_steps_immutable_before.json')).items():assert sha(p)==d
audits={};replayed_transitions=0;replayed_H2=0;replayed_candidates=0
for site in SITES:
 parts=[np.load(R/f'cache/{sp}.npz') for sp in ['exploration','heldout_check']]
 z=np.concatenate([p[site+'__z'] for p in parts]).astype(float);pre=np.concatenate([p[site+'__pre'] for p in parts]).astype(float);dn=parts[0][site+'__decoder_norm'].astype(float);u=z*dn
 assert z.shape==(24,30000) and pre.shape==z.shape
 for j in range(24):
  active=np.flatnonzero(z[j]>0);assert len(active)==32
  assert np.array_equal(z[j,active],pre[j,active]) and bool((pre[j,active]>0).all())
  inactive=np.ones(30000,bool);inactive[active]=False;assert pre[j,inactive].max()<=z[j,active].min()
 tt=list(csv.DictReader(open(R/f'results/{site}/transitions.csv')))
 for t in tt:
  f=int(t['family'][1:])-1;pa=f*4+CONDS.index(t['source']);pb=f*4+CONDS.index(t['destination']);a=set(np.flatnonzero(z[pa]>0));b=set(np.flatnonzero(z[pb]>0))
  assert int(t['retained'])==len(a&b) and int(t['zero_to_positive'])==len(b-a) and int(t['positive_to_zero'])==len(a-b)
  assert len(a&b)+len(b-a)==len(b) and len(a&b)+len(a-b)==len(a);replayed_transitions+=1
 ids=selection['sites'][site]['H2'];w=u[:,ids];norm=np.sqrt(np.einsum('ij,ij->i',w,w));q=np.divide(w,norm[:,None],out=np.full_like(w,np.nan),where=norm[:,None]>0)
 for t in csv.DictReader(open(R/f'results/{site}/H2_directions.csv')):
  f=int(t['family'][1:])-1;i=ids.index(int(t['atom']));a=f*4+1;b=f*4+2
  assert abs(float(t['weighted_q_difference'])-(q[a,i]-q[b,i]))<1e-12
  assert abs(float(t['cat_z'])-z[a,ids[i]])<1e-12;replayed_H2+=1
 for t in csv.DictReader(open(R/f'results/{site}/candidate_values.csv')):
  j=next(j for j,p in enumerate(PANEL) if p['id']==t['id']);i=int(t['atom']);assert abs(float(t['u'])-z[j,i]*dn[i])<1e-12;replayed_candidates+=1
 c32=np.concatenate([p[site+'__cutoff32'] for p in parts]);c33=np.concatenate([p[site+'__cutoff33'] for p in parts]);assert bool((c32>=c33).all())
 capture=[json.load(open(R/f'evidence/capture_{sp}.json')) for sp in ['exploration','heldout_check']]
 assert all(c['native_encoding_equivalence'] and c['hook_noop_checks'][0]['noop_native_state_max_difference']==0 for c in capture)
 assert capture[0]['UTC']<freeze['UTC']<capture[1]['UTC'];assert capture[1]['selection_sha256']==freeze['selection_SHA256']
 audits[site]=dict(rows=24,atoms=30000,all_active_counts=32,min_Top32_positive_margin=float((c32-c33).min()),Top32_boundary_ties=int((c32==c33).sum()),full_support_equal_pairs=int(sum(np.array_equal(z[f*4+1]>0,z[f*4+2]>0) for f in range(6))),candidate_support_equal_pairs=int(sum(np.array_equal(z[f*4+1,ids]>0,z[f*4+2,ids]>0) for f in range(6))),min_decoder_norm=float(dn.min()),max_decoder_norm=float(dn.max()),h_min_norm=float(np.linalg.norm(np.concatenate([p[site+'__h'] for p in parts]),axis=1).min()))
dump(R/'evidence/verification.json',dict(UTC=now(),status='PASS',old_files_unchanged=len(json.load(open(R/'evidence/old_steps_immutable_before.json'))),original_cat_dog_rows_identical=12,all_target_token_ids=264,within_family_absolute_target_positions_matched=True,replayed_transition_rows=replayed_transitions,replayed_H2_differences=replayed_H2,replayed_candidate_values=replayed_candidates,candidate_gate_verified=True,protocol_and_selection_unchanged=True,sites=audits,scientific_acceptance='Unknown',next_step='NOT_RUN_WAIT_FOR_JOINT_REVIEW'))
print('VERIFICATION_PASS',replayed_transitions,replayed_H2,replayed_candidates,flush=True)
