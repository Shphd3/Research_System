"""Cached near-single-domain subsets of the unchanged R10 discriminator list."""
import os
for key in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[key]='2'
from pathlib import Path
import argparse,collections,csv,datetime,hashlib,json
from urllib.parse import urlsplit
import numpy as np
from scipy import sparse,stats
from tokenizers import Tokenizer

ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',type=Path,default=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030'));ap.add_argument('--output',type=Path);arg=ap.parse_args();S=arg.source;O=arg.output or S/'presentation_variants/near_single_domain_20261030';O.mkdir(parents=True,exist_ok=True);R4=S.parent/'R04_domain_usage_20261027';sources=[]
def load(p):sources.append(p);return np.load(p)
def js(p):sources.append(p);return json.loads(p.read_text())
def readrows(p):sources.append(p);return list(csv.DictReader(p.open()))
def table(name,rr):
    rr=list(rr)
    if not rr:return
    with (O/name).open('w',newline='') as fp:w=csv.DictWriter(fp,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
def dump(name,x):(O/name).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def safe(x):return float(x) if np.isfinite(x) else ''
def log(x):print(x,flush=True)
frozen=js(S/'freeze.json');main={g:np.array(frozen['sets']['main_'+g]) for g in ['math','biology']};allmain=np.r_[main['math'],main['biology']]
docpath=R4/'data/documents.jsonl';sources.append(docpath);docs=[json.loads(x) for x in docpath.read_text().splitlines()];domains=np.array([r['domain'] for r in docs]);splits=np.array([r['split'] for r in docs]);a=load(R4/'forward/documents_CC.npz');order=[list(a['seq_id']).index(r['seq_id']) for r in docs];counts=a['counts'][order];sumz=a['sum_z'][order]
idx={(s,g):np.flatnonzero((splits==s)&(domains==g)) for s in ['discovery','development','heldout'] for g in main}
def stat(ids,split,g):
    other='biology' if g=='math' else 'math';p=idx[split,g];o=idx[split,other];pc=counts[p][:,ids];oc=counts[o][:,ids];pt=pc.sum(0);ot=oc.sum(0);share=np.divide(pt,pt+ot,out=np.full(len(ids),np.nan),where=(pt+ot)>0)
    return {'prefdocs':(pc>0).sum(0),'oppdocs':(oc>0).sum(0),'prefevents':pt,'oppevents':ot,'share':share,'pref_total_positions':len(p)*160,'opp_total_positions':len(o)*160,'pref_sumz':sumz[p][:,ids].sum(0),'opp_sumz':sumz[o][:,ids].sum(0)}
disc={g:stat(ids,'discovery',g) for g,ids in main.items()};sets={};sensitivity=[]
for g,ids in main.items():
    d=disc[g];sets['strict_'+g]=ids[(d['prefdocs']>=5)&(d['oppdocs']==0)];sets['near95_'+g]=ids[(d['prefdocs']>=5)&(d['oppdocs']<=1)&(d['share']>=.95)]
    for tau in [.90,.95,.99]:
        for cap in [0,1,3,30]:
            keep=(d['prefdocs']>=5)&(d['oppdocs']<=cap)&(d['share']>=tau);sensitivity.append(dict(domain_bias=g,share_threshold=tau,opposite_document_cap=cap,members=int(keep.sum())));sets[f'share{tau:.2f}_cap{cap}_'+g]=ids[keep]
config={'revision':'R10-near-single-domain-v1','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent_main_freeze_sha256':hashlib.sha256((S/'freeze.json').read_bytes()).hexdigest(),'candidate_pool':'only frozen R10 AUC>=.75 members433math/527bio; no dictionary rescreening','activation':'native z>0,not mean strength','strict':'preferred>=5discovery documents,opposite0discovery documents','near95':'preferred>=5discovery documents,opposite<=5%documents(<=1/30),preferred>=95%of positive token positions across equal-domain panels','sensitivity':'shares90/95/99% x opposite doc caps0/1/3/unrestricted; do not change primary rule','heldout':'membership stays discovery-fixed; assess same95%event rule,opposite<=5%docs(<=1/20),preferred>=5docs; report old AUC and each failure separately','reference_frequency':'same DCLM counts/65536,original cuts and<20support exclusions; also log-rule sensitivity','reference_uncertainty':'1000canonical-reference-document bootstrap draws; all windows of a document travel together, variable denominator','token_categories':'input discovery occurrence support, independent of feature responses: shared>=5docs EACH domain;math/bio-associated>=5in that domain and<=1other;remaining insufficient/other; not semantic-exclusive','token_composition':'existing R10 high-event thresholds and>=5events/2heldoutdocs composition gate; member-equal; analytic document-exposure-matched background; all main subsets retained','geometry':'same common1024-PC basis/unit decoder; exact existing A01 finer matching rule for near95 sizes,including selected in eligible pool','new_forwards':0,'training':0,'new_PCA':0,'scientific_acceptance':'Unknown'}
if (O/'config.json').exists():old=js(O/'config.json');config['frozen_utc']=old['frozen_utc'];assert old==config
else:dump('config.json',config)
freeze={'config_sha256':hashlib.sha256((O/'config.json').read_bytes()).hexdigest(),'selection_split':'discovery only','sets':{k:v.tolist() for k,v in sets.items()},'main_parent':{g:len(v) for g,v in main.items()}}
if (O/'freeze.json').exists():assert js(O/'freeze.json')==freeze
else:dump('freeze.json',freeze)
log('FROZEN '+str({k:len(v) for k,v in sets.items() if k.startswith(('strict_','near95_'))}))
master={int(r['feature_id']):r for r in readrows(S/'tables/master_members.csv')};oldtokens={int(r['feature_id']):r for r in readrows(S/'tables/token_member_summary.csv')};allfeatures=readrows(S/'tables/all_dictionary_screen.csv')
ref=load(R4/'forward/reference_CC.npz');hits=ref['counts'].sum(0);refN=int(ref['n_positions'].sum());rate=hits/refN;freq=np.searchsorted([.002593994140625,.0134429931640625],rate,side='left');freq[hits<20]=3;logfreq=np.searchsorted([.0045172553628813825,.06686505701697326],rate,side='left');logfreq[hits<20]=3
freqrows=[]
cohorts={'dictionary':np.arange(16384),'eligible_pool':np.array([int(r['feature_id']) for r in allfeatures if r['support_qualified']=='True']),**{'parent_'+g:ids for g,ids in main.items()},**sets}
for name,ids in cohorts.items():
    for scheme,binarray in [('original',freq),('log_width',logfreq)]:
        den=int((binarray[ids]<3).sum())
        for k,label in enumerate(['low','middle','high','insufficient']):
            n=int((binarray[ids]==k).sum());freqrows.append(dict(cohort=name,scheme=scheme,frequency=label,count=n,classified_denominator=den,total_members=len(ids),proportion=n/den if den and k<3 else ''))
table('frequency_composition.csv',freqrows);table('selection_sensitivity.csv',sensitivity)

# Independent DCLM rate uncertainty resamples canonical reference documents, not tokens.
refpath=R4/'data/reference.jsonl';sources.append(refpath);refrows=[json.loads(x) for x in refpath.read_text().splitlines()];key=lambda r:(urlsplit(r['url']).hostname,urlsplit(r['url']).path.rstrip('/'));keys=sorted(set(key(r) for r in refrows));groupidx={k:i for i,k in enumerate(keys)}
windoworder=[list(ref['seq_id']).index(r['seq_id']) for r in refrows];near=np.r_[sets['near95_math'],sets['near95_biology']];groupcounts=np.zeros((len(keys),len(near)));grouppos=np.zeros(len(keys))
for i,r in enumerate(refrows):
    j=groupidx[key(r)];groupcounts[j]+=ref['counts'][windoworder[i],near];grouppos[j]+=ref['n_positions'][windoworder[i]]
rng=np.random.default_rng(2026103010);w=rng.multinomial(len(keys),np.full(len(keys),1/len(keys)),size=1000);bootrate=(w@groupcounts)/(w@grouppos)[:,None];reflo,refhi=np.quantile(bootrate,[.025,.975],axis=0);refCI={int(f):(float(l),float(h)) for f,l,h in zip(near,reflo,refhi)}
np.savez_compressed(O/'reference_frequency_bootstrap.npz',feature_ids=near,rates=bootrate,canonical_doc_counts=w,canonical_group_count=len(keys))

members=[];genrerows=[]
for g in main:
    ids=sets['near95_'+g];d=stat(ids,'discovery',g);h=stat(ids,'heldout',g);other='biology' if g=='math' else 'math'
    for k,f in enumerate(ids):
        row=dict(feature_id=int(f),domain_bias=g,strict_discovery=bool(f in sets['strict_'+g]),discovery_preferred_documents=int(d['prefdocs'][k]),discovery_opposite_documents=int(d['oppdocs'][k]),discovery_preferred_events=int(d['prefevents'][k]),discovery_opposite_events=int(d['oppevents'][k]),discovery_preferred_event_share=float(d['share'][k]),discovery_preferred_position_rate=float(d['prefevents'][k]/4800),discovery_opposite_position_rate=float(d['oppevents'][k]/4800),heldout_preferred_documents=int(h['prefdocs'][k]),heldout_opposite_documents=int(h['oppdocs'][k]),heldout_preferred_events=int(h['prefevents'][k]),heldout_opposite_events=int(h['oppevents'][k]),heldout_preferred_event_share=safe(h['share'][k]),heldout_preferred_position_rate=float(h['prefevents'][k]/3200),heldout_opposite_position_rate=float(h['oppevents'][k]/3200),heldout_near95=bool(h['prefdocs'][k]>=5 and h['oppdocs'][k]<=1 and h['share'][k]>=.95),heldout_strict=bool(h['prefdocs'][k]>=5 and h['oppdocs'][k]==0),heldout_opposite_doc_probability_upper95=float(stats.beta.ppf(.95,h['oppdocs'][k]+1,20-h['oppdocs'][k])) if h['oppdocs'][k]<20 else 1.,DCLM_hits=int(hits[f]),DCLM_positions=refN,DCLM_rate=float(rate[f]),DCLM_rate_CI_low=refCI[int(f)][0],DCLM_rate_CI_high=refCI[int(f)][1],frequency_original=['low','middle','high','insufficient'][freq[f]],frequency_log=['low','middle','high','insufficient'][logfreq[f]],discovery_oriented_auc=float(master[int(f)]['discovery_oriented_auc']),heldout_oriented_auc=float(master[int(f)]['heldout_oriented_auc']),heldout_AUC_CI_low=float(master[int(f)]['heldout_CI_low']),heldout_AUC_CI_high=float(master[int(f)]['heldout_CI_high']),composition_supported=oldtokens[int(f)]['usable']=='True',high_event_count=int(oldtokens[int(f)]['heldout_high_events']),high_token_types=int(oldtokens[int(f)]['distinct_high_token_ids']),example_token_id=oldtokens[int(f)]['example_high_token_id'],example_token=oldtokens[int(f)]['example_high_token'],example_prefix=oldtokens[int(f)]['example_prefix'],discovery_preferred_zero_inclusive_mean_z=float(d['pref_sumz'][k]/4800),discovery_opposite_zero_inclusive_mean_z=float(d['opp_sumz'][k]/4800),heldout_preferred_zero_inclusive_mean_z=float(h['pref_sumz'][k]/3200),heldout_opposite_zero_inclusive_mean_z=float(h['opp_sumz'][k]/3200))
        activepref=idx['discovery',g][counts[idx['discovery',g],f]>0];positive=counts[idx['discovery',g],f];row['preferred_discovery_distinct_hosts']=len({docs[i]['host'] for i in activepref});row['max_one_discovery_document_event_share']=float(positive.max()/max(1,positive.sum()));members.append(row)
        for splitname in ['discovery','heldout']:
            for domain in main:
                for gen in sorted(set(r['genre'] for r in docs)):
                    ix=np.array([i for i in idx[splitname,domain] if docs[i]['genre']==gen]);genrerows.append(dict(feature_id=int(f),domain_bias=g,split=splitname,input_domain=domain,genre=gen,documents=len(ix),active_documents=int((counts[ix,f]>0).sum()),positive_positions=int(counts[ix,f].sum()),positions=len(ix)*160))
table('near95_members.csv',members);table('source_genre_support.csv',genrerows)

pk=load(S/'analysis/position_keys.npz');tk=pk['token_id'];di=pk['document_index'];pp=pk['position'];vocab=np.unique(tk);tc=np.searchsorted(vocab,tk);doc_tok=np.zeros((120,len(vocab)),int);np.add.at(doc_tok,(di,tc),1)
presence={g:(doc_tok[idx['discovery',g]]>0).sum(0) for g in main};cats=[]
for j,t in enumerate(vocab):
    m,b=int(presence['math'][j]),int(presence['biology'][j]);cats.append('shared_both_domains' if min(m,b)>=5 else 'math_associated' if m>=5 and b<=1 else 'biology_associated' if b>=5 and m<=1 else 'other_or_low_support')
tokenizer_path=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json');sources.append(tokenizer_path);tok=Tokenizer.from_file(str(tokenizer_path));strings={int(t):tok.decode([int(t)],skip_special_tokens=False) for t in vocab}
table('input_token_categories.csv',(dict(token_id=int(t),token_string=strings[int(t)],discovery_math_documents=int(presence['math'][j]),discovery_biology_documents=int(presence['biology'][j]),category=cats[j]) for j,t in enumerate(vocab)))
zpath=S/'analysis/native_positions_csr.npz';sources.append(zpath);Z=sparse.load_npz(zpath);heldrow=np.flatnonzero(splits[di]=='heldout');helddoc=np.flatnonzero(splits=='heldout');hdmap={int(d):k for k,d in enumerate(helddoc)};hd=np.array([hdmap[int(d)] for d in di[heldrow]]);tau=load(S/'analysis/token_thresholds.npz')['positive_z_p90'];token_rows=[];token_summary={};position_weights={}
for g in main:
    ids=sets['near95_'+g];zz=Z[heldrow][:,ids].tocoo();ok=zz.data>tau[ids][zz.col];H=sparse.csr_matrix((np.ones(ok.sum()),(zz.row[ok],zz.col[ok])),shape=(len(heldrow),len(ids)));usable=np.array([oldtokens[int(f)]['usable']=='True' for f in ids]);sel=np.flatnonzero(usable);nt=np.asarray(H.sum(0)).ravel();natives=np.asarray((Z[heldrow][:,ids]>0).sum(0)).ravel();onehot=sparse.csr_matrix((np.ones(len(heldrow)),(np.arange(len(heldrow)),tc[heldrow])),shape=(len(heldrow),len(vocab)));T=(H.T@onehot).tocsr();docone=sparse.csr_matrix((np.ones(len(heldrow)),(np.arange(len(heldrow)),hd)),shape=(len(heldrow),40));dh=(H.T@docone).toarray()
    q=np.asarray(T[sel].multiply(1/nt[sel,None]).mean(0)).ravel() if len(sel) else np.full(len(vocab),np.nan);dw=(dh[sel]/nt[sel,None]).mean(0) if len(sel) else np.full(40,np.nan);baseline=dw@(doc_tok[helddoc]/160);posweight=np.asarray(H[:,sel]@(1/nt[sel]/len(sel))).ravel() if len(sel) else np.zeros(len(heldrow));position_weights[g]=posweight
    assert not len(sel) or np.isclose(q.sum(),1)
    rank=np.lexsort((vocab,-np.nan_to_num(q,nan=-1)));rankno=np.empty(len(vocab),int);rankno[rank]=np.arange(1,len(vocab)+1)
    totals={cat:float(np.nansum(q[np.array(cats)==cat])) for cat in sorted(set(cats))};bgcats={cat:float(np.nansum(baseline[np.array(cats)==cat])) for cat in sorted(set(cats))}
    token_summary[g]=dict(frozen_members=len(ids),composition_members=len(sel),excluded_composition_support=len(ids)-len(sel),category_shares=totals,document_matched_category_shares=bgcats,high_events=int(nt.sum()),members_with_any_high=int((nt>0).sum()),members_with_any_positive=int((natives>0).sum()),sensitivity_subsets={})
    member_flags={int(r['feature_id']):r for r in members}
    for label,test in [('strict_discovery',lambda f:member_flags[int(f)]['strict_discovery']),('near95_heldout_check',lambda f:member_flags[int(f)]['heldout_near95']),('strict_heldout_check',lambda f:member_flags[int(f)]['strict_discovery'] and member_flags[int(f)]['heldout_strict'])]:
        sub=np.array([bool(test(f)) for f in ids]);us=np.flatnonzero(sub&usable)
        subq=np.asarray(T[us].multiply(1/nt[us,None]).mean(0)).ravel() if len(us) else np.full(len(vocab),np.nan)
        token_summary[g]['sensitivity_subsets'][label]=dict(all_members=int(sub.sum()),composition_members=len(us),category_shares={c:float(np.nansum(subq[np.array(cats)==c])) for c in sorted(set(cats))})
    for j,t in enumerate(vocab):token_rows.append(dict(domain_bias=g,token_id=int(t),token_string=strings[int(t)],category=cats[j],rank=int(rankno[j]),high_share=safe(q[j]),document_matched_background=safe(baseline[j]),composition_members=len(sel),all_frozen_members=len(ids),high_response_members=int((T[sel,j]>0).sum()) if len(sel) else 0,raw_high_events=float(T[:,j].sum())))
    # Same-token group rates retain every discovery-frozen subset member, including zeros.
    theid=279;score=np.asarray(H.mean(1)).ravel();rmeans={}
    for domain in main:
        vv=[]
        for d in idx['heldout',domain]:
            rr=np.flatnonzero((di[heldrow]==d)&(tk[heldrow]==theid))
            if len(rr):vv.append(float(score[rr].mean()))
        rmeans[domain]=float(np.mean(vv)) if vv else None
    token_summary[g]['same_the_ID279_mean_fraction_high_all_members']=rmeans
table('near95_activated_tokens.csv',token_rows);np.savez_compressed(O/'heldout_position_composition_weights.npz',global_rows=heldrow,math=position_weights['math'],biology=position_weights['biology'])

# Unit geometry, and the SAME fine-matching reference rule with the new subset sizes.
P=load(S/'analysis/all_decoder_projection.npz')['per_pc'];bands=P.reshape(16384,16,64).sum(2);geometry={};q={}
for label in ['strict','near95']:
    q[label]={}
    for g in main:
        ids=sets[label+'_'+g];q[label][g]=P[ids].mean(0) if len(ids) else None;geometry.setdefault(label,{})[g]=dict(members=len(ids),head_mean=float(bands[ids,0].mean()) if len(ids) else None,head_median=float(np.median(bands[ids,0])) if len(ids) else None,first256_mean=float(bands[ids,:4].sum(1).mean()) if len(ids) else None)
    geometry[label]['overlap_pc']=float(np.minimum(q[label]['math'],q[label]['biology']).sum()) if all(v is not None for v in q[label].values()) else None
    geometry[label]['overlap_band']=float(np.minimum(q[label]['math'].reshape(16,64).sum(1),q[label]['biology'].reshape(16,64).sum(1)).sum()) if all(v is not None for v in q[label].values()) else None
pool=np.array([int(r['feature_id']) for r in allfeatures if r['support_qualified']=='True']);disc_idx=np.flatnonzero(splits=='discovery');sm=(counts[idx['discovery','math']]>0).sum(0);sb=(counts[idx['discovery','biology']]>0).sum(0);keyrows=list(zip(np.where(hits>0,np.floor(2*np.log2(np.maximum(hits,1))).astype(int),-1),(sm+sb)//5,np.maximum(sm,sb)//5));keys2={k:i for i,k in enumerate(sorted(set(keyrows)))};stratum=np.array([keys2[k] for k in keyrows]);draw={g:np.empty((1000,len(sets['near95_'+g])),int) for g in main}
for st in np.unique(stratum[near]):
    candidates=pool[stratum[pool]==st];loc={g:np.flatnonzero(stratum[sets['near95_'+g]]==st) for g in main};nm,nb=len(loc['math']),len(loc['biology']);assert len(candidates)>=nm+nb
    for b in range(1000):pick=rng.choice(candidates,nm+nb,replace=False);draw['math'][b,loc['math']]=pick[:nm];draw['biology'][b,loc['biology']]=pick[nm:]
bg={}
for g in main:
    dd=draw[g];rr=np.repeat(np.arange(1000),dd.shape[1]);weights=sparse.csr_matrix((np.full(dd.size,1/dd.shape[1]),(rr,dd.ravel())),shape=(1000,16384));bg[g]=weights@P;geometry['near95'][g]['head_background95']=np.quantile(bg[g][:,:64].sum(1),[.025,.975]).tolist();np.savez_compressed(O/f'{g}_matched_reference.npz',feature_ids=dd,mean_per_pc=bg[g])
geometry['near95']['overlap_pc_background95']=np.quantile(np.minimum(bg['math'],bg['biology']).sum(1),[.025,.975]).tolist()
table('near95_member_spectrum.csv',(dict(feature_id=int(f),domain_bias=g,**{f'band{k+1}':float(bands[f,k]) for k in range(16)}) for g in main for f in sets['near95_'+g]))

summary={'scope':'R10 main subset only; no forwards/training/newPCA','members':{},'frequency':{},'token_summary':token_summary,'geometry':geometry,'reference_documents':len(keys),'reference_positions':refN,'zero_opposite_heldout_20doc_upper95':float(1-.05**(1/20)),'definition_warning':'observed panel selectivity, not global domain-exclusive knowledge; original heldout is exposed'}
for g in main:
    rr=[r for r in members if r['domain_bias']==g];ids=sets['near95_'+g];valid=ids[freq[ids]<3]
    summary['members'][g]={'parent_main':len(main[g]),'strict_discovery':len(sets['strict_'+g]),'near95_discovery':len(ids),'near95_retains_heldout':sum(r['heldout_near95'] for r in rr),'strict_discovery_still_strict_heldout':sum(r['strict_discovery'] and r['heldout_strict'] for r in rr),'heldout_opposite_zero':sum(r['heldout_opposite_documents']==0 for r in rr),'heldout_preferred_support_under5':sum(r['heldout_preferred_documents']<5 for r in rr)}
    summary['frequency'][g]={'classified':len(valid),'insufficient':len(ids)-len(valid),'counts':[int((freq[ids]==k).sum()) for k in range(3)],'DCLM_rate_median':float(np.median(rate[ids])),'DCLM_rate_p10_p90':np.quantile(rate[ids],[.1,.9]).tolist()}
dump('summary.json',summary);dump('provenance.json',{'inputs':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in dict.fromkeys(sources)],'script':str(Path(__file__).resolve()),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'new_model_forwards':0,'new_training':0,'candidate_main_unchanged':True})
log(json.dumps(summary,ensure_ascii=False,indent=2))
