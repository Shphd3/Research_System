"""Independent cache/denominator/matching checks for the near-domain supplement."""
from pathlib import Path
import csv,json,collections,hashlib,re
import numpy as np
from scipy import sparse
S=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030');O=S/'presentation_variants/near_single_domain_20261030';T=S/'presentation_variants/token_context_audit_20261030'
def rows(p):return list(csv.DictReader(p.open()))
checks=[]
def check(name,condition):
    if not condition:raise AssertionError(name)
    checks.append(name)
docs=[json.loads(x) for x in (S.parent/'R04_domain_usage_20261027/data/documents.jsonl').read_text().splitlines()];di=np.load(S/'analysis/position_keys.npz')['document_index'];pk=np.load(S/'analysis/position_keys.npz');pos=pk['position'];tokens=pk['token_id'];Z=sparse.load_npz(S/'analysis/native_positions_csr.npz');freeze=json.loads((O/'freeze.json').read_text());parent=json.loads((S/'freeze.json').read_text());sets=freeze['sets'];ids=np.r_[sets['near95_math'],sets['near95_biology']];held=np.flatnonzero(np.array([docs[int(d)]['split']=='heldout' for d in di]));X=Z[:,ids].toarray();tau=np.load(S/'analysis/token_thresholds.npz')['positive_z_p90'][ids];H=X>tau
check('55 fixed unique IDs, all in original960',len(ids)==55 and len(set(ids))==55 and all(set(sets['near95_'+g])<=set(parent['sets']['main_'+g]) for g in ['math','biology']))
for g in ['math','biology']:
    pp=np.array([docs[int(d)]['split']=='discovery' and docs[int(d)]['domain']==g for d in di]);oo=np.array([docs[int(d)]['split']=='discovery' and docs[int(d)]['domain']!=g for d in di]);allids=np.array(parent['sets']['main_'+g]);zz=Z[:,allids];a=zz[pp]>0;b=zz[oo]>0;pd=np.array([int(a[k*160:(k+1)*160].getnnz(axis=0).astype(bool).sum()) for k in []])
    prefdocs=np.sum(np.vstack([Z[np.flatnonzero(di==d)][:,allids].getnnz(axis=0)>0 for d,doc in enumerate(docs) if doc['split']=='discovery' and doc['domain']==g]),axis=0);oppdocs=np.sum(np.vstack([Z[np.flatnonzero(di==d)][:,allids].getnnz(axis=0)>0 for d,doc in enumerate(docs) if doc['split']=='discovery' and doc['domain']!=g]),axis=0);pt=np.asarray(a.sum(0)).ravel();ot=np.asarray(b.sum(0)).ravel();share=np.divide(pt,pt+ot,out=np.zeros_like(pt,dtype=float),where=pt+ot>0)
    check(g+' near freeze from direct position cache',allids[(prefdocs>=5)&(oppdocs<=1)&(share>=.95)].tolist()==sets['near95_'+g])
    check(g+' strict freeze from direct position cache',allids[(prefdocs>=5)&(oppdocs==0)].tolist()==sets['strict_'+g])
    tt=[r for r in rows(O/'near95_activated_tokens.csv') if r['domain_bias']==g];check(g+' token and matched baseline masses sum1',np.isclose(sum(float(r['high_share']) for r in tt),1) and np.isclose(sum(float(r['document_matched_background']) for r in tt),1))
top=rows(O/'per_member_token_top10.csv');check('per-member top-token table retains all55 including no-high',set(int(r['feature_id']) for r in top)==set(ids))
alltokens=rows(O/'per_member_tokens_all.csv');cm=collections.defaultdict(float)
for r in alltokens:cm[int(r['feature_id'])]+=float(r['share'])
check('each nonempty member token distribution sums1',all(np.isclose(v,1) for v in cm.values()))
for r in alltokens:
    j=list(ids).index(int(r['feature_id']));mask=H[held,j]&(tokens[held]==int(r['token_id']));check0=int(mask.sum())==int(r['high_events']);check0&=len(set(di[held[mask]]))==int(r['high_response_documents'])
    if not check0:raise AssertionError('per-member actual token coverage')
checks.append('all per-member high counts and document coverage independently agree')
pairs=rows(O/'matched_token_position_pairs.csv');by=collections.defaultdict(list)
for r in pairs:
    m,b=int(r['math_global_row']),int(r['biology_global_row']);dm,db=docs[int(di[m])],docs[int(di[b])];p,q=int(pos[m]),int(pos[b]);t=int(r['token_id'])
    assert tokens[m]==tokens[b]==t and dm['split']==db['split']=='heldout' and dm['genre']==db['genre'] and dm['token_ids'][p-1]==db['token_ids'][q-1] and (p-32)//40==(q-32)//40
    if r['level']=='source_local':assert dm['host']==db['host']
    by[t,r['level']].append(r)
checks.append('every matched target/previousID, genre, position-bin and source restriction holds')
for key,rr in by.items():
    pairmap={int(r['document_pair']):(r['math_doc'],r['biology_doc']) for r in rr};assert len(set(m for m,b in pairmap.values()))==len(pairmap)==len(set(b for m,b in pairmap.values()));assert len(set(r['math_global_row'] for r in rr))==len(rr)==len(set(r['biology_global_row'] for r in rr))
checks.append('matching never reuses a document across pairs or a position within token/level')
gs=rows(O/'matched_same_token_group_summary.csv')
for r in gs:
    if not int(r['matched_document_pairs']):assert r['interval_status']=='NO_MATCHED_OPPORTUNITY';continue
    rr=by[int(r['target_token_id']),r['level']];group=sets['near95_'+r['feature_group']];jj=[list(ids).index(f) for f in group];diff=[]
    for d in sorted(set(x['document_pair'] for x in rr)):
        a=[x for x in rr if x['document_pair']==d];mr=[int(x['math_global_row']) for x in a];br=[int(x['biology_global_row']) for x in a];diff.append(H[mr][:,jj].mean()-H[br][:,jj].mean())
    sign=1 if r['feature_group']=='math' else -1;assert np.isclose(sign*np.mean(diff),float(r['preferred_minus_other_high_fraction']))
checks.append('group responses recomputed from fixed thresholds, zeros and equal document-pair means')
blind=rows(O/'prefix_annotation_blinded_inputs.csv');check('6400 annotation inputs contain only random caseID and prior text',len(blind)==6400 and set(blind[0])=={'case_id','already_read_window'})
review=rows(O/'prefix_annotation_v2_AI_proposals.csv');check('all human annotation fields remain unverified',all(not r['human_verified_category'] for r in review))
check('example members remain fixed first discovery ranks', [int(r['feature_id']) for r in rows(O/'predetermined_member_matched_examples.csv')]==[sets['near95_math'][0],sets['near95_biology'][0]])
check('no-high counterexample remains visible',rows(O/'predetermined_member_matched_examples.csv')[1]['status']=='NO_MATCHED_HIGH_RESPONSE_SUPPORT')
check('all289thepositions times55members retained',len(rows(O/'near_the_all_occurrences.csv'))==289*55)
result={'status':'PASS','checks':checks,'checked_categories':len(checks),'frozen_members':55,'heldout_positions':6400,'new_model_forwards':0,'human_review':'PENDING','statistical_claims':'Exploratory observational comparisons, not causal/semantic confirmation.'}
(O/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
