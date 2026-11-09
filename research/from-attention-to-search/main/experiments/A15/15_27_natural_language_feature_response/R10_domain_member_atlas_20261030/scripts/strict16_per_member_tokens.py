"""Native-positive actual-token inventory for every unchanged all-cached-strict16 member."""
from pathlib import Path
import csv,json,hashlib,collections,datetime,shutil
import numpy as np
from scipy import sparse
S=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030');A=S/'presentation_variants/pooled_simple_20261030';T=S/'presentation_variants/token_context_audit_20261030';O=S/'presentation_variants/strict16_per_member_tokens_20261030';O.mkdir(exist_ok=True);W=Path(__file__).resolve().parents[1];D=W/'figure_variants/strict16_per_member_tokens_20261030';D.mkdir(exist_ok=True)
def read(p):return list(csv.DictReader(p.open()))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(n,rr):
    rr=list(rr)
    with (O/n).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
def dump(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
freeze=json.loads((A/'freeze.json').read_text());groups={g:freeze['sets']['all_cached_strict_'+g] for g in ['math','biology']};ids=groups['math']+groups['biology'];byid={int(r['feature_id']):r for r in read(A/'strict16_members.csv')};docs=[json.loads(x) for x in (S.parent/'R04_domain_usage_20261027/data/documents.jsonl').read_text().splitlines()];pk=np.load(S/'analysis/position_keys.npz');di=pk['document_index'];tk=pk['token_id'];held=np.flatnonzero(np.array([docs[int(i)]['split']=='heldout' for i in di]));tcats={int(r['token_id']):r for r in read(A/'token_ID_details.csv') if r['mode']=='native_all'};spell={int(r['global_row']):r['posthoc_word_spelling'] for r in read(T/'heldout_token_spelling_positions.csv')};X=sparse.load_npz(S/'analysis/native_positions_csr.npz')[held][:,ids].toarray();P=X>0
cfg={'revision':'strict16-per-member-native-token-v1','member_freeze_sha256':sha(A/'freeze.json'),'member_ids':ids,'members_fixed':16,'readout':'native shared z>0; no p90 threshold, no intensity weighting','positions':'unchanged oldheldout40documents(20math/20biology)*160positions,tokenindices32..191;6400positions','categories':'unchanged pooled-simple full120-document coverage: shared>=5docs EACH domain;observed single-domain>=5docs one and0other;remaining other/insufficient','denominators':'within each feature: native-positive positions; documents count distinct source documents containing that feature/token positive event; exact token IDs deduplicated for types','ranking':'descending native-positive position count,ascending tokenID for ties;top3chat,top10appendix,alltokenscsv;no manual substitution','posthoc_spellings':'full observed word aid only, may include future subword characters; never causal activation explanation','exploratory':'member subset and token coverage inspect allcached data;oldheldout is not independent generalization','new_model_forwards':0,'new_training':0}
if (O/'config.json').exists():assert json.loads((O/'config.json').read_text())==cfg
else:dump('config.json',cfg)
summ=[];allrows=[];top=[];catnames=['shared','observed_single_domain','other_or_insufficient'];inputtoken=collections.Counter(tk.tolist())
for j,fid in enumerate(ids):
    g=byid[fid]['domain_bias'];rr=np.flatnonzero(P[:,j]);N=len(rr);assert N==int(byid[fid]['heldout_preferred_events']);assert all(docs[int(di[held[r]])]['domain']==g for r in rr);counts=collections.Counter(tk[held[rr]].tolist());ordered=sorted(counts,key=lambda t:(-counts[t],t));categories=collections.Counter();cattypes=collections.Counter()
    for rank,t in enumerate(ordered,1):
        tr=rr[tk[held[rr]]==t];gr=held[tr];tag=tcats[t];cls=tag['category'];categories[cls]+=len(tr);cattypes[cls]+=1;sp=collections.Counter(spell[int(r)] for r in gr);available=(tk[held]==t)&np.array([docs[int(di[r])]['domain']==g for r in held]);n_available=int(available.sum());row=dict(feature_id=fid,domain_bias=g,rank=rank,token_id=t,token_string=tag['token_string'],native_positive_positions=len(tr),active_documents=len(set(di[gr].tolist())),position_share=len(tr)/N,total_feature_positive_positions=N,total_feature_active_documents=len(set(di[held[rr]].tolist())),token_category=cls,math_input_documents_all60=int(tag['math_documents_all60']),biology_input_documents_all60=int(tag['biology_documents_all60']),input_corpus_count=inputtoken[t],input_corpus_positions=19200,preferred_domain_available_token_positions=n_available,preferred_domain_available_token_documents=len(set(di[held[available]].tolist())),conditional_activation_fraction=len(tr)/n_available,observed_full_word_spellings=' | '.join(f'{w} ({n})' for w,n in sp.most_common(3)),spelling_status='posthoc_readability_not_activation_cause');allrows.append(row)
        if rank<=10:top.append(row)
    row=dict(feature_id=fid,domain_bias=g,positive_positions=N,active_documents=len(set(di[held[rr]].tolist())),available_domain_documents=20,opposite_active_documents=0,distinct_token_IDs=len(counts),**{c+'_positions':categories[c] for c in catnames},**{c+'_share':categories[c]/N for c in catnames},**{c+'_token_types':cattypes[c] for c in catnames},top3_position_share=sum(counts[t] for t in ordered[:3])/N,top10_position_share=sum(counts[t] for t in ordered[:10])/N);summ.append(row)
table('member_summary.csv',summ);table('member_token_all.csv',allrows);table('member_token_top10.csv',top)
old={int(r['feature_id']):r for r in read(A/'per_member_token_composition.csv') if r['mode']=='native_all'}
for r in summ:
    assert r['positive_positions']==int(old[r['feature_id']]['response_positions']) and r['active_documents']==int(old[r['feature_id']]['response_documents'])
    for new,prior in [('shared','shared_share'),('observed_single_domain','single_domain_share'),('other_or_insufficient','other_share')]:assert np.isclose(r[new+'_share'],float(old[r['feature_id']][prior]))
assert sum(r['positive_positions'] for r in summ)==4675;assert len({r['token_id'] for r in allrows})==1182;assert len(summ)==16 and len(top)==160
sources=[Path(__file__).resolve(),A/'freeze.json',A/'strict16_members.csv',A/'token_ID_details.csv',A/'per_member_token_composition.csv',S/'analysis/position_keys.npz',S/'analysis/native_positions_csr.npz',S.parent/'R04_domain_usage_20261027/data/documents.jsonl',T/'heldout_token_spelling_positions.csv']
dump('provenance.json',{'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent_asset_ids':['analysis_a15_27_04_r10_domain_member_atlas_20261030','analysis_a15_27_r10_near_domain_token_context_20261030'],'sources':[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sources],'new_model_forwards':0})
dump('audit.json',{'status':'PASS','all16retained':True,'position_and_document_counts_match_existing_native_summary':True,'per_member_category_shares_match_existing_native_summary':True,'native_member_position_events':4675,'unique_token_IDs':1182,'top10_rows':160,'new_model_forwards':0})
for n in ['config.json','member_summary.csv','member_token_all.csv','member_token_top10.csv','provenance.json','audit.json']:shutil.copy2(O/n,D/n)
print('SUMMARY')
for r in summ:print(json.dumps(r,ensure_ascii=False))
print('TOP5')
for fid in ids:
    tt=[r for r in allrows if r['feature_id']==fid][:5];print(fid,json.dumps([{k:r[k] for k in ['token_string','token_id','native_positive_positions','active_documents','position_share','token_category','observed_full_word_spellings']} for r in tt],ensure_ascii=False))
print('OUTPUT',str(D))
