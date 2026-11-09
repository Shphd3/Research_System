"""Broad token response audit of frozen R10 members; cache arithmetic only."""
import os
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):
    os.environ[key]='2'
from pathlib import Path
import argparse,collections,csv,datetime,hashlib,json,re
import numpy as np
from scipy import sparse,stats
from tokenizers import Tokenizer

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source',type=Path,default=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030'))
parser.add_argument('--output',type=Path)
args=parser.parse_args();S=args.source;O=args.output or S/'presentation_variants/token_context_audit_20261030';O.mkdir(parents=True,exist_ok=True)
R4=S.parent/'R04_domain_usage_20261027';input_paths=[]
def js(p):input_paths.append(p);return json.loads(p.read_text())
def load(p):input_paths.append(p);return np.load(p)
def table(name,rows):
    rr=list(rows)
    if not rr:return
    with (O/name).open('w',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
def scalar(x):return x.item() if isinstance(x,np.generic) else x
def dump(name,x):(O/name).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def log(s):print(s,flush=True)
def safe(x):return float(x) if np.isfinite(x) else ''

freeze=js(S/'freeze.json');groups={g:np.array(freeze['sets']['main_'+g],int) for g in ['math','biology']};members=np.r_[groups['math'],groups['biology']];N=len(members);cuts={'math':slice(0,len(groups['math'])),'biology':slice(len(groups['math']),N)}
document_path=R4/'data/documents.jsonl';input_paths.append(document_path);docs=[json.loads(x) for x in document_path.read_text().splitlines()]
pk=load(S/'analysis/position_keys.npz');docindex=pk['document_index'];position=pk['position'];tokens=pk['token_id'];types=np.unique(tokens);V=len(types);column=np.searchsorted(types,tokens);D=len(docs)
domain=np.array([r['domain'] for r in docs]);split=np.array([r['split'] for r in docs]);genre=np.array([r['genre'] for r in docs]);held_docs=np.flatnonzero(split=='heldout');disc_docs=np.flatnonzero(split=='discovery');held_rows=np.flatnonzero(np.isin(docindex,held_docs));disc_rows=np.flatnonzero(np.isin(docindex,disc_docs));hdlookup={int(d):i for i,d in enumerate(held_docs)};held_localdoc=np.array([hdlookup[int(d)] for d in docindex[held_rows]])
assert len(held_docs)==40 and len(held_rows)==6400 and len(set(r['document_group'] for r in docs))==120
doccount=np.zeros((D,V),np.int32);np.add.at(doccount,(docindex,column),1)
assert np.all(doccount.sum(1)==160)
for d in range(D):assert np.array_equal(tokens[docindex==d],np.array(docs[d]['token_ids'][32:192]))
tokenizer_path=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json');input_paths.append(tokenizer_path);tokenizer=Tokenizer.from_file(str(tokenizer_path))
strings={int(t):tokenizer.decode([int(t)],skip_special_tokens=False) for t in types}
theids=[int(t) for t in types if strings[int(t)].strip().casefold()=='the']
disctotal=doccount[disc_docs].sum(0);primary_the_id=max(theids,key=lambda t:int(disctotal[np.searchsorted(types,t)]))
disc_presence={g:(doccount[disc_docs[domain[disc_docs]==g]]>0).sum(0) for g in groups};held_presence={g:(doccount[held_docs[domain[held_docs]==g]]>0).sum(0) for g in groups}
eligible_discovery=(disc_presence['math']>=5)&(disc_presence['biology']>=5)
comparable=(held_presence['math']>=5)&(held_presence['biology']>=5)
display_order=np.lexsort((types,-disctotal));display_indices=display_order[eligible_discovery[display_order]&comparable[display_order]][:12]
cfg={'revision':'R10-token-context-v1','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'scope':'same960 frozen members; existing natural z/token caches only; no model forward/training',
     'freeze_sha256':hashlib.sha256((S/'freeze.json').read_bytes()).hexdigest(),
     'positions':[32,192],'primary_events':'strictly greater than each member discovery-positive-z90th percentile, exactly R10 thresholds',
     'composition_primary':'same371/472 R10 composition-supported members; normalize high-event token counts within member, then equal-member mean',
     'composition_background':'within each member preserve high-event count per heldout document; expected token frequency from uniformly sampled positions in those same documents; then equal-member mean',
     'composition_sensitivity':'equal active documents within member, then equal members; also all members with>=1high event',
     'conditional_rates':'ALL433/527 main members incl never-high; per occurrence fraction of group members high/positive, then average within token/document, then equal documents with that exact token',
     'token_identity':'exact ID; no case/space merging; function words,punctuation,subwords retained',
     'comparison_support':'at least5heldout documents/domain containing exact token; all other token rows retained as insufficient',
     'display_tokens':'first12 by discovery occurrence count among discovery>=5docs/domain and heldout-comparable; independent of response effect',
     'display_token_ids':types[display_indices].tolist(),'focus_the_ids':theids,'primary_the_id':primary_the_id,
     'bootstrap':{'reps':1000,'seed':2026103009,'unit':'whole document;20/domain; same draws carry both feature groups','interval':'exploratory pointwise95%; no multi-token confirmatory discovery'},
     'position_genre_sensitivity':'same exact token; strata genre x four40-position bins; require3docs/domain in a stratum; average domain doc-means with fixed min(document counts) stratum weights; report retained positions; descriptive point only',
     'referent_boundary':'no gold referent labels in inputs; prefix/current token used for current-response discussion; later1-3words labeled posthoc continuations, not causal context and not asserted noun phrases',
     'posthoc_support':'continuation word discovery doc support>=3 in only one domain is labelled discovery-only with support; <=2docs remains low support; missing/unseen explicit; never called semantic-exclusive',
     'examples':'exact primary the ID; first2docs/domain in SHA256(seed,seqid) order among>=2occurrences; within-document max/min group response, never selected by domain-object wording'}
if (O/'config.json').exists():
    old=json.loads((O/'config.json').read_text());cfg['frozen_utc']=old['frozen_utc'];assert old==cfg
else:dump('config.json',cfg)
log(f'CONFIG FROZEN; exact the IDs={theids}; primary={primary_the_id}; comparable tokens={comparable.sum()}')

zpath=S/'analysis/native_positions_csr.npz';input_paths.append(zpath);Z=sparse.load_npz(zpath)[:,members].tocsr();threshold=load(S/'analysis/token_thresholds.npz')['positive_z_p90'][members];assert np.isfinite(threshold).all()
coo=Z.tocoo();hh=coo.data>threshold[coo.col];H=sparse.csr_matrix((np.ones(hh.sum(),np.float64),(coo.row[hh],coo.col[hh])),shape=Z.shape);A=Z.copy();A.data=np.ones_like(A.data,np.float64)
HH=H[held_rows];AA=A[held_rows];onehot=sparse.csr_matrix((np.ones(len(held_rows)),(np.arange(len(held_rows)),column[held_rows])),shape=(len(held_rows),V));docone=sparse.csr_matrix((np.ones(len(held_rows)),(np.arange(len(held_rows)),held_localdoc)),shape=(len(held_rows),40))
high_token=(HH.T@onehot).tocsr();active_token=(AA.T@onehot).tocsr();high_doc=(HH.T@docone).toarray();n_high=np.asarray(high_token.sum(1)).ravel();n_active=np.asarray(active_token.sum(1)).ravel();n_active_docs=(high_doc>0).sum(1)
oldsummary_path=S/'tables/token_member_summary.csv';input_paths.append(oldsummary_path)
with oldsummary_path.open() as stream:oldrows={int(r['feature_id']):r for r in csv.DictReader(stream)}
usable=np.array([oldrows[int(f)]['usable']=='True' for f in members]);assert all(n_high[i]==int(oldrows[int(f)]['heldout_high_events']) for i,f in enumerate(members))
group_pos_high=np.column_stack([np.asarray(H[:,cuts[g]].mean(1)).ravel() for g in groups]);group_pos_active=np.column_stack([np.asarray(A[:,cuts[g]].mean(1)).ravel() for g in groups])
baseline=doccount[held_docs].sum(0)/6400;docfreq=doccount[held_docs]/160
composition=[];composition_by_group={};composition_position_weights={};hc=HH.tocoo()
for gi,g in enumerate(groups):
    sl=cuts[g];loc=np.arange(N)[sl];sel=loc[usable[loc]];alt=loc[n_high[loc]>0];native=loc[n_active[loc]>0]
    q=np.asarray(high_token[sel].multiply(1/n_high[sel,None]).mean(0)).ravel()
    qalt=np.asarray(high_token[alt].multiply(1/n_high[alt,None]).mean(0)).ravel()
    qa=np.asarray(active_token[native].multiply(1/n_active[native,None]).mean(0)).ravel()
    dw=(high_doc[sel]/n_high[sel,None]).mean(0);expected=dw@docfreq
    choose=usable[hc.col]&np.isin(hc.col,loc);cc=hc.col[choose];rr=hc.row[choose];dd=held_localdoc[rr]
    weights=1/(len(sel)*n_active_docs[cc]*high_doc[cc,dd]);qdoc=np.bincount(column[held_rows[rr]],weights=weights,minlength=V)
    assert np.isclose(q.sum(),1) and np.isclose(expected.sum(),1) and np.isclose(qdoc.sum(),1)
    coverage=np.asarray((high_token[sel]>0).sum(0)).ravel();raw=np.asarray(high_token[sel].sum(0)).ravel();anypos=np.asarray(HH[:,sel].getnnz(1)>0).ravel();unique=np.bincount(column[held_rows[anypos]],minlength=V)
    rank=np.lexsort((types,-q));ranks=np.empty(V,int);ranks[rank]=np.arange(1,V+1)
    composition_by_group[g]=dict(q=q,background=expected,docbalanced=qdoc,ranks=ranks)
    composition_position_weights[g]=np.asarray(HH[:,sel]@(1/n_high[sel]/len(sel))).ravel()
    for j,t in enumerate(types):
        composition.append(dict(domain_bias=g,token_id=int(t),token_string=strings[int(t)],rank=int(ranks[j]),member_equal_high_share=float(q[j]),document_matched_background_share=float(expected[j]),lift_over_document_matched=float(q[j]/expected[j]) if expected[j]>0 else '',all_heldout_position_share=float(baseline[j]),document_balanced_high_share=float(qdoc[j]),all_high_responding_members_share=float(qalt[j]),positive_activation_share=float(qa[j]),composition_members=len(sel),all_main_members=len(loc),all_with_high_event=len(alt),members_high_on_token=int(coverage[j]),raw_member_position_high_events=int(raw[j]),distinct_high_token_positions=int(unique[j]),heldout_occurrences=int(doccount[held_docs,j].sum()),heldout_math_occurrences=int(doccount[held_docs[domain[held_docs]=='math'],j].sum()),heldout_biology_occurrences=int(doccount[held_docs[domain[held_docs]=='biology'],j].sum())))
table('all_token_composition.csv',composition)
np.savez_compressed(O/'heldout_position_composition_weights.npz',global_rows=held_rows,**composition_position_weights)
log('Broad token composition computed; document exposure-matched background retained')

# Conditional probability: never treat an absent token as zero response.
means_high=np.full((D,V,2),np.nan);means_active=np.full_like(means_high,np.nan)
for d in range(D):
    rr=np.flatnonzero(docindex==d);present=doccount[d]>0
    for gi in range(2):
        sums=np.bincount(column[rr],weights=group_pos_high[rr,gi],minlength=V);means_high[d,present,gi]=sums[present]/doccount[d,present]
        sums=np.bincount(column[rr],weights=group_pos_active[rr,gi],minlength=V);means_active[d,present,gi]=sums[present]/doccount[d,present]
rng=np.random.default_rng(cfg['bootstrap']['seed']);boot={g:rng.multinomial(20,np.full(20,1/20),size=1000).astype(float) for g in groups};domain_docs={g:held_docs[domain[held_docs]==g] for g in groups}
comp_idx=np.flatnonzero(comparable);ci_low=np.full((V,2),np.nan);ci_high=ci_low.copy();ci_valid=np.zeros((V,2),int)
for gi in range(2):
    draws={}
    for dname in groups:
        x=means_high[domain_docs[dname]][:,comp_idx,gi];den=boot[dname]@np.isfinite(x).astype(float);num=boot[dname]@np.nan_to_num(x);draws[dname]=np.divide(num,den,out=np.full_like(num,np.nan),where=den>0)
    delta=draws['math']-draws['biology'];ci_low[comp_idx,gi],ci_high[comp_idx,gi]=np.nanquantile(delta,[.025,.975],axis=0);ci_valid[comp_idx,gi]=np.isfinite(delta).sum(0)
np.savez_compressed(O/'bootstrap_document_counts.npz',math=boot['math'],biology=boot['biology'])
conditional=[];lookup_cond={}
genres=sorted(set(genre));stratum=np.array([genres.index(genre[d])*4+int((p-32)//40) for d,p in zip(docindex,position)])
for j,t in enumerate(types):
    ds={g:domain_docs[g][doccount[domain_docs[g],j]>0] for g in groups}
    for gi,g in enumerate(groups):
        rawmeans={d:float(means_high[ds[d],j,gi].mean()) if len(ds[d]) else np.nan for d in groups};positivemeans={d:float(means_active[ds[d],j,gi].mean()) if len(ds[d]) else np.nan for d in groups};diff=rawmeans['math']-rawmeans['biology'];matched_differences=[];matched_weights=[];matched_strata=[]
        if comparable[j]:
            rr_token=held_rows[tokens[held_rows]==t]
            for st in range(8):
                rr=rr_token[stratum[rr_token]==st];bydomain={d:np.unique(docindex[rr][domain[docindex[rr]]==d]) for d in groups}
                if min(len(v) for v in bydomain.values())<3:continue
                avg={}
                for dname in groups:
                    vals=[]
                    for d in bydomain[dname]:vals.append(group_pos_high[rr[docindex[rr]==d],gi].mean())
                    avg[dname]=np.mean(vals)
                matched_differences.append(avg['math']-avg['biology']);matched_weights.append(min(len(v) for v in bydomain.values()));matched_strata.append(st)
            keep=np.isin(stratum[rr_token],matched_strata);retained={d:float((keep&(domain[docindex[rr_token]]==d)).sum()/max(1,(domain[docindex[rr_token]]==d).sum())) for d in groups}
        else:retained={d:np.nan for d in groups}
        adjusted=float(np.average(matched_differences,weights=matched_weights)) if matched_weights else np.nan
        row=dict(token_id=int(t),token_string=strings[int(t)],feature_group=g,main_members=len(groups[g]),discovery_math_documents=int(disc_presence['math'][j]),discovery_biology_documents=int(disc_presence['biology'][j]),heldout_math_documents=len(ds['math']),heldout_biology_documents=len(ds['biology']),math_token_occurrences=int(doccount[domain_docs['math'],j].sum()),biology_token_occurrences=int(doccount[domain_docs['biology'],j].sum()),math_high_fraction=safe(rawmeans['math']),biology_high_fraction=safe(rawmeans['biology']),math_minus_biology=safe(diff),CI_low=safe(ci_low[j,gi]),CI_high=safe(ci_high[j,gi]),valid_bootstrap_reps=int(ci_valid[j,gi]),math_positive_fraction=safe(positivemeans['math']),biology_positive_fraction=safe(positivemeans['biology']),comparison_supported=bool(comparable[j]),discovery_display_eligible=bool(eligible_discovery[j]),position_genre_adjusted_difference=safe(adjusted),matched_strata=len(matched_weights),retained_math_token_fraction=safe(retained['math']),retained_biology_token_fraction=safe(retained['biology']),interpretation='natural-context association; no referent label; exposed heldout')
        conditional.append(row);lookup_cond[(int(t),g)]=row
table('same_token_domain_comparison.csv',conditional)
log('All-token conditional comparisons and pointwise document intervals complete')

# All occurrences of the-family, never use later words as already-visible context.
decoded={d:tokenizer.decode(docs[d]['token_ids'],skip_special_tokens=False) for d in range(D)}
the_occ=[]
for rr in np.flatnonzero(np.isin(tokens,theids)):
    d=int(docindex[rr]);pos=int(position[rr]);t=int(tokens[rr]);pre=tokenizer.decode(docs[d]['token_ids'][:pos],skip_special_tokens=False);inc=tokenizer.decode(docs[d]['token_ids'][:pos+1],skip_special_tokens=False);assert decoded[d].startswith(inc)
    tail=decoded[d][len(inc):];target=strings[t];left_ok=(target[:1].isspace() or not pre or not pre[-1].isalnum());right_ok=not tail or not tail[0].isalnum();standalone=bool(left_ok and right_ok)
    continuation=re.match(r'^\s+([A-Za-z]+(?:[-\'][A-Za-z]+)*)',tail)
    nextword=continuation.group(1).casefold() if standalone and continuation else ''
    nextwords=re.findall(r'[A-Za-z]+(?:[-\'][A-Za-z]+)*',tail)[:3] if nextword else []
    row=dict(seq_id=docs[d]['seq_id'],document_group=docs[d]['document_group'],split=docs[d]['split'],domain=docs[d]['domain'],genre=docs[d]['genre'],position=pos,token_id=t,token_string=target,standalone_the=standalone,already_read_prefix=pre,last40_read_tokens=tokenizer.decode(docs[d]['token_ids'][max(0,pos-40):pos],skip_special_tokens=False),math_high_members=int(round(group_pos_high[rr,0]*len(groups['math']))),biology_high_members=int(round(group_pos_high[rr,1]*len(groups['biology']))),math_high_fraction=float(group_pos_high[rr,0]),biology_high_fraction=float(group_pos_high[rr,1]),posthoc_next_word=nextword,posthoc_next_three_words=' '.join(nextwords),posthoc_tail_preview=tail[:100],future_text_used_for_current_activation_explanation=False,referent_annotation='MISSING',object_domain_specificity='UNKNOWN')
    the_occ.append(row)
table('all_the_family_occurrences.csv',the_occ)

# Per-member support for primary same-ID the; all960 retained.
j=np.searchsorted(types,primary_the_id);rows_by_doc={d:np.flatnonzero((docindex==d)&(tokens==primary_the_id)) for d in held_docs};feature_diffs=[]
vdoc=np.full((40,N),np.nan);adoc=np.zeros((40,N),bool)
for i,d in enumerate(held_docs):
    rr=rows_by_doc[d]
    if len(rr):vdoc[i]=np.asarray(H[rr].mean(0)).ravel();adoc[i]=np.asarray(H[rr].sum(0)).ravel()>0
for gi,g in enumerate(groups):
    for k in np.arange(N)[cuts[g]]:
        xx={dom:vdoc[np.array([domain[d]==dom for d in held_docs]),k] for dom in groups};delta=float(np.nanmean(xx['math'])-np.nanmean(xx['biology']));sgn=1 if g=='math' else -1
        active={dom:int(adoc[np.array([domain[d]==dom for d in held_docs]),k].sum()) for dom in groups}
        feature_diffs.append(dict(feature_id=int(members[k]),domain_bias=g,target_token_id=primary_the_id,target_token=strings[primary_the_id],math_high_fraction=float(np.nanmean(xx['math'])),biology_high_fraction=float(np.nanmean(xx['biology'])),preferred_domain_difference=sgn*delta,math_documents_with_high=active['math'],biology_documents_with_high=active['biology'],at_least_one_high=bool(sum(active.values())>0),at_least3_docs_one_domain=bool(max(active.values())>=3)))
table('the_per_member_support.csv',feature_diffs)

# Continuations are purely posthoc lexical descriptions, not noun-phrase or referent annotations.
disc_follow=collections.defaultdict(lambda:{g:set() for g in groups})
for r in the_occ:
    if r['token_id']==primary_the_id and r['split']=='discovery' and r['posthoc_next_word']:disc_follow[r['posthoc_next_word']][r['domain']].add(r['seq_id'])
def continuation_category(w):
    if not w:return 'unavailable_or_nonword'
    n={g:len(disc_follow[w][g]) for g in groups}
    if min(n.values())>0:return 'seen_both_domains_in_discovery'
    if max(n.values())==0:return 'unseen_in_discovery'
    if n['math']>=3:return 'math_only_discovery_ge3docs'
    if n['biology']>=3:return 'biology_only_discovery_ge3docs'
    return 'single_domain_discovery_le2docs'
held_the=[r for r in the_occ if r['split']=='heldout' and r['token_id']==primary_the_id]
continuations=[]
for w in sorted({r['posthoc_next_word'] for r in held_the}):
    rr=[r for r in held_the if r['posthoc_next_word']==w]
    continuations.append(dict(posthoc_next_word=w,heldout_occurrences=len(rr),heldout_math_occurrences=sum(r['domain']=='math' for r in rr),heldout_biology_occurrences=sum(r['domain']=='biology' for r in rr),heldout_distinct_documents=len({r['seq_id'] for r in rr}),discovery_math_documents=len(disc_follow[w]['math']),discovery_biology_documents=len(disc_follow[w]['biology']),discovery_support_category=continuation_category(w),object_or_noun_phrase_label='NOT_ANNOTATED'))
table('the_posthoc_continuation_counts.csv',continuations)
category_counts=collections.Counter(continuation_category(r['posthoc_next_word']) for r in held_the)

# Conditional high-response continuations at exactID279, with a SAME-document/the baseline.
the_global=np.flatnonzero(np.isin(docindex,held_docs)&(tokens==primary_the_id));assert len(the_global)==len(held_the)
TH=H[the_global];the_localdoc=np.array([hdlookup[int(d)] for d in docindex[the_global]]);the_doc_one=sparse.csr_matrix((np.ones(len(the_global)),(np.arange(len(the_global)),the_localdoc)),shape=(len(the_global),40));the_feature_doc=(TH.T@the_doc_one).toarray();the_feature_total=np.asarray(TH.sum(0)).ravel();the_input_doc=np.bincount(the_localdoc,minlength=40);the_wordrows=[];the_posthoc={}
for g in groups:
    local=np.arange(N)[cuts[g]];eligible=local[the_feature_total[local]>0];weights=np.asarray(TH[:,eligible]@(1/the_feature_total[eligible]/len(eligible))).ravel();docweights=(the_feature_doc[eligible]/the_feature_total[eligible,None]).mean(0);expected_position=docweights[the_localdoc]/the_input_doc[the_localdoc]
    assert np.isclose(weights.sum(),1) and np.isclose(expected_position.sum(),1)
    share_by_category=collections.defaultdict(float)
    for w in sorted({r['posthoc_next_word'] for r in held_the}):
        present=np.array([r['posthoc_next_word']==w for r in held_the]);value=float(weights[present].sum());bgvalue=float(expected_position[present].sum());cat=continuation_category(w);share_by_category[cat]+=value
        the_wordrows.append(dict(feature_group=g,posthoc_next_word=w,high_share=value,same_document_the_background=bgvalue,features_with_the_high=len(eligible),all_main_members=len(local),heldout_occurrences=int(present.sum()),heldout_documents=len({r['seq_id'] for r,p in zip(held_the,present) if p}),discovery_support_category=cat,semantic_referent_label='MISSING'))
    the_posthoc[g]=dict(features_with_the_high=len(eligible),category_high_shares=dict(share_by_category))
table('the_high_response_posthoc_continuations.csv',the_wordrows)
# Every heldout the-family occurrence is available for a future score-blind semantic audit.
blind=[];keyrows=[]
for r in the_occ:
    if r['split']!='heldout':continue
    case=hashlib.sha256(f"R10-the:{r['seq_id']}:{r['position']}".encode()).hexdigest()[:12]
    blind.append(dict(case_id=case,target_token_id=r['token_id'],target_string=r['token_string'],already_read_prefix=r['already_read_prefix'],posthoc_following_text=r['posthoc_tail_preview'],referent_recoverable_before_target='',antecedent_quote_from_prefix='',posthoc_noun_phrase_span='',object_domain_label='',label_evidence='',status='UNANNOTATED'))
    keyrows.append(dict(case_id=case,seq_id=r['seq_id'],domain=r['domain'],position=r['position'],math_high_members=r['math_high_members'],biology_high_members=r['biology_high_members']))
table('the_semantic_review_blinded.csv',sorted(blind,key=lambda r:r['case_id']));table('the_semantic_review_key.csv',keyrows)

# Examples selected by document hashes, not by a compelling semantic story.
examples=[]
for g in groups:
    candidates=[]
    for d in domain_docs[g]:
        rr=[r for r in held_the if r['seq_id']==docs[d]['seq_id']]
        if len(rr)>=2:candidates.append((hashlib.sha256(f"2026103009:{docs[d]['seq_id']}".encode()).hexdigest(),rr))
    for _,rr in sorted(candidates)[:2]:
        rank=sorted(rr,key=lambda r:(r[g+'_high_fraction'],r['position']));lo,hi=rank[0],rank[-1]
        for label,r in [('within_doc_higher',hi),('within_doc_lower',lo)]:
            examples.append(dict(display_feature_group=g,kind=label,seq_id=r['seq_id'],domain=r['domain'],position=r['position'],token_id=r['token_id'],token_string=r['token_string'],group_high_members=r[g+'_high_members'],group_members=len(groups[g]),group_high_fraction=r[g+'_high_fraction'],already_read_prefix=r['already_read_prefix'],posthoc_next_three_words=r['posthoc_next_three_words'],future_used_for_current_explanation=False))
table('the_examples_balanced_documents.csv',examples)

the_family=[]
for t in theids:
    j=np.searchsorted(types,t)
    for g in groups:
        row=lookup_cond[(t,g)].copy();row['main_composition_rank']=int(composition_by_group[g]['ranks'][j]);row['composition_high_share']=float(composition_by_group[g]['q'][j]);row['composition_docmatched_background']=float(composition_by_group[g]['background'][j]);the_family.append(row)
table('the_family_summary.csv',the_family)
summary={'scope':{'main_members':{g:len(v) for g,v in groups.items()},'composition_members':{g:int(usable[cuts[g]].sum()) for g in groups},'heldout_documents_per_domain':20,'heldout_positions':6400,'heldout_unique_token_IDs':int((doccount[held_docs].sum(0)>0).sum()),'all_panel_unique_token_IDs':V,'conditional_comparable_token_IDs':int(comparable.sum()),'display_token_IDs':types[display_indices].tolist(),'new_model_forwards':0},
         'primary_the_token_id':primary_the_id,'primary_the_string':strings[primary_the_id],
         'the_family_all_heldout_occurrences':sum(r['split']=='heldout' for r in the_occ),
         'primary_the_heldout_occurrences':len(held_the),
         'primary_the_domains':{g:sum(r['domain']==g for r in held_the) for g in groups},
         'the_same_token_comparison':{g:lookup_cond[(primary_the_id,g)] for g in groups},
         'the_member_support':{},'posthoc_continuation_discovery_support':dict(category_counts),
         'the_high_response_posthoc_summary':the_posthoc,
         'referent_status':'MISSING semantic referent labels; cannot report object domain-exclusivity proportion; later lexical continuations are descriptive only',
         'statistical_boundary':'document-level exposed-data reuse; pointwise intervals; natural contexts differ in vocabulary/style/position, no causal or semantic binding proof'}
for g in groups:
    rr=[r for r in feature_diffs if r['domain_bias']==g]
    summary['the_member_support'][g]=dict(main_members=len(rr),any_high=sum(r['at_least_one_high'] for r in rr),support_ge3docs=sum(r['at_least3_docs_one_domain'] for r in rr),preferred_domain_positive=sum(r['preferred_domain_difference']>0 for r in rr),opposite_domain_positive=sum(r['preferred_domain_difference']<0 for r in rr),zero_difference=sum(r['preferred_domain_difference']==0 for r in rr))
dump('summary.json',summary)
source_manifest={'inputs':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in dict.fromkeys(input_paths)],'script':str(Path(__file__).resolve()),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'new_model_forwards':0,'new_selection':False,'no_semantic_referent_labels_fabricated':True}
dump('provenance.json',source_manifest)
log(json.dumps(summary,ensure_ascii=False,indent=2))
