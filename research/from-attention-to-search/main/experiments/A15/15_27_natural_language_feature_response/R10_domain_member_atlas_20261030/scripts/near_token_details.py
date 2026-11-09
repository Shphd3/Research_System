"""Per-member token IDs, observed spellings, coverage and frequency for all55near members."""
from pathlib import Path
import csv,json,collections
import numpy as np
from scipy import sparse
from tokenizers import Tokenizer
S=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030');O=S/'presentation_variants/near_single_domain_20261030';T=S/'presentation_variants/token_context_audit_20261030'
tok=Tokenizer.from_file('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json')
def table(name,rr):
    rr=list(rr)
    if not rr:return
    with (O/name).open('w',newline='') as fp:w=csv.DictWriter(fp,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
f=json.loads((O/'freeze.json').read_text());near={g:np.array(f['sets']['near95_'+g]) for g in ['math','biology']};ids=np.r_[near['math'],near['biology']];m={int(r['feature_id']):r for r in csv.DictReader((O/'near95_members.csv').open())};categories={int(r['token_id']):r for r in csv.DictReader((O/'input_token_categories.csv').open())};old={int(r['feature_id']):r for r in csv.DictReader((S/'tables/token_member_summary.csv').open())}
docs=[json.loads(x) for x in (S.parent/'R04_domain_usage_20261027/data/documents.jsonl').read_text().splitlines()];pk=np.load(S/'analysis/position_keys.npz');di=pk['document_index'];pos=pk['position'];tokens=pk['token_id'];held=np.flatnonzero(np.array([docs[d]['split']=='heldout' for d in di]));x=sparse.load_npz(S/'analysis/native_positions_csr.npz')[held][:,ids].toarray();tau=np.load(S/'analysis/token_thresholds.npz')['positive_z_p90'][ids];H=x>tau;words={int(r['global_row']):r for r in csv.DictReader((T/'heldout_token_spelling_positions.csv').open())};allcount=collections.Counter(tokens.tolist());heldcount=collections.Counter(tokens[held].tolist());all_docs={t:set(di[tokens==t].tolist()) for t in allcount};native_input_bg=np.bincount(np.searchsorted(np.unique(tokens),tokens[held]),minlength=len(np.unique(tokens)))/6400
rows=[];top=[];member_composition=[];opposite=[]
for j,fid in enumerate(ids):
    g=m[int(fid)]['domain_bias'];rr=np.flatnonzero(H[:,j]);N=len(rr);cnt=collections.Counter(tokens[held[rr]].tolist());ordered=sorted(cnt,key=lambda t:(-cnt[t],t))
    if not N:
        top.append(dict(feature_id=int(fid),domain_bias=g,rank=0,token_id='',token_string='',posthoc_word_spellings='',high_events=0,total_feature_high_events=0,share='',high_response_documents=0,all_panel_token_count='',all_panel_positions=19200,all_panel_token_occurrence_rate='',all_panel_documents='',heldout_token_count='',heldout_positions=6400,token_category='',token_frequency_bin='',composition_supported=False,mean_high_z='',max_high_z='',threshold=float(tau[j]),status='NO_HELDOUT_HIGH_EVENTS'));continue
    classshare=collections.Counter();freqshare=collections.Counter()
    for rank,t in enumerate(ordered,1):
        tr=rr[tokens[held[rr]]==t];gr=held[tr];sp=collections.Counter(words[int(r)]['posthoc_word_spelling'] for r in gr);readable=' | '.join(f'{w}({n})' for w,n in sp.most_common(3));cls=categories[t]['category'];freqbin='low_count1' if allcount[t]==1 else 'middle_count2' if allcount[t]==2 else 'high_count_ge3';classshare[cls]+=len(tr)/N;freqshare[freqbin]+=len(tr)/N
        row=dict(feature_id=int(fid),domain_bias=g,rank=rank,token_id=t,token_string=categories[t]['token_string'],posthoc_word_spellings=readable,high_events=len(tr),total_feature_high_events=N,share=len(tr)/N,high_response_documents=len(set(di[gr].tolist())),all_panel_token_count=allcount[t],all_panel_positions=19200,all_panel_token_occurrence_rate=allcount[t]/19200,all_panel_documents=len(all_docs[t]),heldout_token_count=heldcount[t],heldout_positions=6400,token_category=cls,token_frequency_bin=freqbin,composition_supported=old[int(fid)]['usable']=='True',mean_high_z=float(x[tr,j].mean()),max_high_z=float(x[tr,j].max()),threshold=float(tau[j]),status='OK' if old[int(fid)]['usable']=='True' else 'INSUFFICIENT_HIGH_EVENT_COMPOSITION_SUPPORT');rows.append(row)
        if rank<=10:top.append(row)
    member_composition.append(dict(feature_id=int(fid),domain_bias=g,composition_supported=old[int(fid)]['usable']=='True',**{c:classshare[c] for c in ['shared_both_domains','math_associated','biology_associated','other_or_low_support']},**{c:freqshare[c] for c in ['low_count1','middle_count2','high_count_ge3']}))
    # Highest opposite-domain reading per document, even if it is below the high threshold.
    other=[i for i,r in enumerate(held) if docs[int(di[r])]['domain']!=g and x[i,j]>0]
    for d in sorted({int(di[held[i]]) for i in other}):
        candidates=[i for i in other if di[held[i]]==d];best=max(candidates,key=lambda i:float(x[i,j]));r=int(held[best]);p=int(pos[r]);opposite.append(dict(feature_id=int(fid),domain_bias=g,opposite_doc=docs[d]['seq_id'],host=docs[d]['host'],position=p,token_id=int(tokens[r]),token_string=categories[int(tokens[r])]['token_string'],z=float(x[best,j]),high_threshold=float(tau[j]),above_high_threshold=bool(H[best,j]),already_read_prefix=''.join([]),prefix_token_ids=json.dumps(docs[d]['token_ids'][:p])))
opposite=[]
for j,fid in enumerate(ids):
    g=m[int(fid)]['domain_bias']
    for d in sorted({int(di[r]) for r in held if docs[int(di[r])]['domain']!=g}):
        candidates=np.flatnonzero((di[held]==d)&(x[:,j]>0))
        if not len(candidates):continue
        best=int(candidates[np.argmax(x[candidates,j])]);r=int(held[best]);p=int(pos[r]);prefix_ids=docs[d]['token_ids'][:p]
        opposite.append(dict(feature_id=int(fid),domain_bias=g,opposite_doc=docs[d]['seq_id'],host=docs[d]['host'],position=p,token_id=int(tokens[r]),token_string=categories[int(tokens[r])]['token_string'],z=float(x[best,j]),high_threshold=float(tau[j]),above_high_threshold=bool(H[best,j]),already_read_prefix=tok.decode(prefix_ids,skip_special_tokens=False),prefix_token_ids=json.dumps(prefix_ids)))
table('per_member_tokens_all.csv',rows);table('per_member_token_top10.csv',top);table('per_member_token_class_and_frequency.csv',member_composition);table('opposite_domain_positive_examples.csv',opposite)
the_rows=[]
for i in np.flatnonzero(tokens[held]==279):
    r=int(held[i]);d=int(di[r]);p=int(pos[r]);doc=docs[d];pre=tok.decode(doc['token_ids'][:p],skip_special_tokens=False);future=tok.decode(doc['token_ids'][p+1:min(192,p+25)],skip_special_tokens=False)
    for j,fid in enumerate(ids):
        the_rows.append(dict(feature_id=int(fid),domain_bias=m[int(fid)]['domain_bias'],seq_id=doc['seq_id'],input_domain=doc['domain'],source_host=doc['host'],position=p,token_id=279,target=' the',native_z=float(x[i,j]),high_threshold=float(tau[j]),high_response=bool(H[i,j]),already_read_prefix=pre,posthoc_following_preview=future,human_posthoc_noun_phrase='',human_referent_category='',review_status='POSTHOC_DESCRIPTION_ONLY_HUMAN_LABELS_PENDING'))
table('near_the_all_occurrences.csv',the_rows)
freqrows=[];summary={};types=np.unique(tokens);input_count=np.array([allcount[int(t)] for t in types]);typebin=np.searchsorted([1,2],input_count,side='left');qrows=list(csv.DictReader((O/'near95_activated_tokens.csv').open()))
for g in near:
    supported=[r for r in member_composition if r['domain_bias']==g and r['composition_supported']];q={int(r['token_id']):r for r in qrows if r['domain_bias']==g};summary[g]={}
    for k,label in enumerate(['low_count1','middle_count2','high_count_ge3']):
        ts=types[typebin==k];value=float(np.mean([r[label] for r in supported]));raw=sum(heldcount[int(t)] for t in ts)/6400;matched=sum(float(q[int(t)]['document_matched_background']) for t in ts);freqrows.append(dict(feature_group=g,token_frequency_bin=label,member_equal_high_share=value,all_available_position_share=raw,document_matched_share=matched,composition_members=len(supported),all_main_members=len(near[g])));summary[g][label]=value
table('high_token_frequency_composition.csv',freqrows)
(O/'token_detail_summary.json').write_text(json.dumps({'per_member_rows':len(rows),'top10_rows':len(top),'members_retained':len(ids),'supported_composition_members':{g:sum(r['domain_bias']==g and r['composition_supported'] for r in member_composition) for g in near},'token_frequency_composition':summary,'new_model_forwards':0},indent=2)+'\n');print('TOKEN DETAILS DONE',len(ids),len(rows),len(top))
