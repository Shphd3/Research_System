"""Frozen 16+16 CrossCoder member meeting analysis. CPU cache reads only.

Run --freeze before the other analyses. No model/checkpoint construction,
dictionary fitting, vocabulary decoding of decoders, or distance acquisition.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[k]='2'
from pathlib import Path
import json,csv,hashlib,datetime,argparse
import numpy as np
from scipy.stats import rankdata,spearmanr

O=Path(__file__).resolve().parent
B=O.parent
R=B/'R04_domain_usage_20261027'
S=R/'domain_discriminability_spectrum_20261028'
R7=B/'R07_fixed_target_domain_spectrum_20261029'
R8=B/'R08_within_mixed_subspaces_20261029'
R9=B/'R09_domain_difference_decomposition_20261029'
CHECKPOINT='crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013'
TOKENIZER=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json')
def js(p):return json.loads(Path(p).read_text())
def jl(p):return [json.loads(s) for s in Path(p).read_text().splitlines()]
def clean(v):
    if isinstance(v,dict):return {str(k):clean(w) for k,w in v.items()}
    if isinstance(v,(list,tuple,np.ndarray)):return [clean(w) for w in v]
    if isinstance(v,np.generic):return clean(v.item())
    if isinstance(v,float) and not np.isfinite(v):return None
    return v
def dump(p,v):Path(p).write_text(json.dumps(clean(v),ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def savecsv(p,rows):
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with Path(p).open('w',newline='',encoding='utf-8-sig') as h:
        w=csv.DictWriter(h,keys);w.writeheader();w.writerows([{k:clean(v) for k,v in r.items()} for r in rows])
def readcsv(p):return list(csv.DictReader(Path(p).open(encoding='utf-8-sig')))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for x in iter(lambda:f.read(8<<20),b''):h.update(x)
    return h.hexdigest()
def auc(x,y):
    n=int(y.sum());m=len(y)-n
    return (rankdata(x,axis=0)[y==1].sum(0)-n*(n+1)/2)/(n*m)
def timestamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def freeze():
    docs=jl(R/'data/documents.jsonl');a=np.load(R/'forward/documents_CC.npz')
    y=np.array([r['label'] for r in docs]);sp=np.array([r['split'] for r in docs]);tr=sp=='discovery'
    assert a['seq_id'].tolist()==[r['seq_id'] for r in docs]
    c=a['counts'];sm=(c[tr&(y==1)]>0).sum(0);sb=(c[tr&(y==0)]>0).sum(0)
    eligible=(sm>=5)&(sb>=5)
    # For a fixed member, positive decoder norm multiplies every document by
    # the same constant, so native-z and native-contribution AUC are identical.
    score=a['sum_z']/160
    v=auc(score[tr],y[tr]);direction=np.sign(v-.5).astype(int)
    order=np.flatnonzero(eligible&(direction!=0));order=order[np.lexsort((order,-abs(v[order]-.5)))]
    groups={d:order[direction[order]==sgn][:16].tolist() for d,sgn in [('math',1),('biology',-1)]}
    old=js(S/'analysis/candidate_freeze.json')['dictionaries']['CC']['groups']
    assert groups['math']==old['expanded_math64'][:16]
    assert groups['biology']==old['expanded_bio64'][:16]
    assert np.array_equal(eligible,np.load(S/'analysis/CC_discovery_freeze.npz')['eligible'])
    assert np.max(abs(v-np.load(S/'analysis/CC_discovery_freeze.npz')['raw_auc']))<1e-12
    core=dict(groups=groups,ordered_union=groups['math']+groups['biology'],eligible_n=int(eligible.sum()),
        ties_not_selected=int((eligible&(direction==0)).sum()),dictionary=CHECKPOINT,
        checkpoint_sha256='09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628',
        score='P(document-mean native shared z math > biology)+0.5*P(tie); 30x30 document pairs',
        eligibility='each domain >=5 positive discovery documents; fixed original R04 discriminability gate',
        rank='abs(raw AUC - 0.5) descending, member ID ascending; then retain sign-specific first16',
        window='zero-based [32,192); 160 tokens/document, zeros included',
        status='exploratory 16+16 prefix of existing frozen64 lists; exposed old heldout; no re-selection',
        basis=str(S/'real_spectrum_A01/analysis/CC_common_basis.npz'),
        basis_sha256=sha(S/'real_spectrum_A01/analysis/CC_common_basis.npz'),
        source_freeze_sha256=sha(S/'analysis/candidate_freeze.json'))
    p=O/'freeze.json'
    if p.exists():
        previous=js(p)
        assert {k:previous[k] for k in core}==core,'Frozen identity changed'
    else:dump(p,dict(frozen_utc=timestamp(),**core))
    np.savez_compressed(O/'analysis/discovery_qualification.npz',eligible=eligible,auc=v,direction=direction,
        support_math=sm,support_biology=sb,order=order)
    savecsv(O/'tables/frozen_list.csv',[dict(group=d,rank=i+1,feature=f,discovery_raw_auc=float(v[f]),
        support_math=int(sm[f]),support_biology=int(sb[f]),dictionary=CHECKPOINT) for d,ids in groups.items() for i,f in enumerate(ids)])
    print('FROZEN',json.dumps(groups),'eligible',int(eligible.sum()),flush=True)

def main():
    fr=js(O/'freeze.json');ids=np.array(fr['ordered_union']);groups={k:np.array(v) for k,v in fr['groups'].items()}
    q=np.load(O/'analysis/discovery_qualification.npz');eligible=q['eligible'];allids=np.arange(16384)
    docs=jl(R/'data/documents.jsonl');a=np.load(R/'forward/documents_CC.npz');y=np.array([r['label'] for r in docs]);sp=np.array([r['split'] for r in docs])
    score=a['sum_z']/160;counts=a['counts'];splits=['discovery','development','heldout']
    aucs={s:auc(score[sp==s],y[sp==s]) for s in splits}
    freq=np.load(R/'forward/reference_CC.npz')['counts'].sum(0)/65536
    hits=np.rint(freq*65536).astype(int)
    oldfreq=js(B/'R05_distance_attention_20261028/analysis/CC_frequency_bins.json');cuts=oldfreq['cuts']
    cfg=js(R9/'frequency_family/config.json');logedges=cfg['group_schemes']['log_equal_width']['edges']
    def bins(c):return np.where(hits<20,'low_support',np.where(freq<=c[0],'low',np.where(freq<=c[1],'middle','high')))
    fb=bins(cuts);lb=bins(logedges[1:3]);binrows=[]
    for scheme,labels in [('original_equal_count',fb),('R09_log_equal_width',lb)]:
        for pop,ix in [('eligible_pool',allids[eligible]),('full_dictionary',allids)]+list(groups.items()):
            for label in ['low','middle','high','low_support']:
                binrows.append(dict(scheme=scheme,population=pop,group=label,n=int((labels[ix]==label).sum()),denominator=len(ix),fraction=float((labels[ix]==label).mean())))
    savecsv(O/'tables/frequency_counts.csv',binrows)
    dump(O/'frequency_history.json',dict(main='original_equal_count',main_cuts=cuts,reference_N=65536,
        min_hits=20,log_equal_width_sensitivity_edges=logedges,
        history='R05 archived original equal-count bins; R09 adopted log equal width for its own contribution analysis; this report restores original as primary and shows R09 as sensitivity. No old result changed.'))
    print('FREQUENCY_DONE',flush=True)
    decoder=np.load(R9/'analysis/decoder_and_scale.npz')['decoder_model_scale']
    pc=np.load(fr['basis'])['PC_columns'];norm=np.linalg.norm(decoder,axis=1);valid=norm>0
    assert valid[ids].all() and sha(fr['basis'])==fr['basis_sha256']
    unit=decoder/norm[:,None];pr=unit@pc;energy=pr**2;bands=energy.reshape(16384,16,64).sum(2)
    assert np.max(abs(energy.sum(1)-1))<1e-9
    np.savez_compressed(O/'analysis/unit_decoder_geometry.npz',feature_ids=ids,projection=pr[ids],per_PC=energy[ids],per_band=bands[ids],unit_decoder=unit[ids],norm=norm[ids])
    savecsv(O/'tables/member_spectrum.csv',[dict(group=d,feature=int(f),band=b+1,PC_start=b*64+1,PC_end=(b+1)*64,energy=float(bands[f,b])) for d,ix in groups.items() for f in ix for b in range(16)])
    # Match counts independently for both sign groups. Noncandidate pools stay
    # disjoint within each paired random draw; exact joint bins, no relaxation.
    rfbin=np.floor(np.log2(hits+.5)).astype(int)
    suppbin=((q['support_math']+q['support_biology'])//5).astype(int)
    keys={d:[(int(rfbin[f]),int(suppbin[f])) for f in ix] for d,ix in groups.items()}
    need={k:{d:keys[d].count(k) for d in groups} for k in set(keys['math']+keys['biology'])}
    pools={k:allids[eligible&~np.isin(allids,ids)&(rfbin==k[0])&(suppbin==k[1])] for k in need}
    poolrows=[dict(log2_hits_bin=k[0],document_support_bin=k[1],need_math=n['math'],need_biology=n['biology'],available=len(pools[k]),supported=len(pools[k])>=sum(n.values())) for k,n in sorted(need.items())]
    savecsv(O/'tables/matched_pool_support.csv',poolrows)
    supported=all(r['supported'] for r in poolrows)
    rng=np.random.default_rng(2026103001);random={d:[] for d in groups}
    if supported:
        for draw in range(1000):
            sets={d:[] for d in groups}
            for k,n in sorted(need.items()):
                picked=rng.choice(pools[k],sum(n.values()),replace=False);s=0
                for d in groups:sets[d].extend(picked[s:s+n[d]]);s+=n[d]
            for d in groups:random[d].append(sets[d])
        random={d:np.array(v,int) for d,v in random.items()}
        rmean={d:energy[ix].mean(1) for d,ix in random.items()}
        rbmean={d:v.reshape(1000,16,64).sum(2) for d,v in rmean.items()}
        ropc=np.minimum(rmean['math'],rmean['biology']).sum(1)
        roband=np.minimum(rbmean['math'],rbmean['biology']).sum(1)
        np.savez_compressed(O/'analysis/matched_background.npz',**{d+'_ids':v for d,v in random.items()},
            **{d+'_band_mean':v for d,v in rbmean.items()},per_PC_overlap=ropc,band_overlap=roband)
    # Preserve all supported calculations when one group's exact match fails.
    separate={}
    for d in groups:
        dn={k:n[d] for k,n in need.items() if n[d]>0}
        if any(len(pools[k])<n for k,n in dn.items()):
            separate[d]=dict(status='NA_INSUFFICIENT_MATCHED_POOL');continue
        draws=np.array([np.concatenate([rng.choice(pools[k],n,replace=False) for k,n in sorted(dn.items())]) for _ in range(1000)])
        bm=bands[draws].mean(1)
        np.savez_compressed(O/'analysis'/f'{d}_matched_background.npz',ids=draws,band_mean=bm)
        separate[d]=dict(status='DONE',draws=1000,PC1_64_mean_quantiles=np.quantile(bm[:,0],[.025,.5,.975]))
    uniform_pool=allids[valid&~np.isin(allids,ids)]
    uniform=np.array([rng.choice(uniform_pool,32,replace=False) for _ in range(1000)])
    ump=energy[uniform[:,:16]].mean(1);ubp=energy[uniform[:,16:]].mean(1)
    uniform_PC=np.minimum(ump,ubp).sum(1)
    uniform_band=np.minimum(ump.reshape(1000,16,64).sum(2),ubp.reshape(1000,16,64).sum(2)).sum(1)
    np.savez_compressed(O/'analysis/uniform_dictionary_background.npz',ids=uniform,per_PC_overlap=uniform_PC,band_overlap=uniform_band)
    pmeans={d:energy[ix].mean(0) for d,ix in groups.items()};bmeans={d:v.reshape(16,64).sum(1) for d,v in pmeans.items()}
    overlap_PC=float(np.minimum(*pmeans.values()).sum());overlap_band=float(np.minimum(*bmeans.values()).sum())
    cos=unit[groups['math']]@unit[groups['biology']].T
    qm=np.linalg.qr(unit[groups['math']].T)[0];qb=np.linalg.qr(unit[groups['biology']].T)[0]
    singular=np.linalg.svd(qm.T@qb,compute_uv=False)
    geometry=dict(overlap_per_PC=overlap_PC,overlap_per_band=overlap_band,
        pair_abs_cosine_mean=float(abs(cos).mean()),pair_abs_cosine_max=float(abs(cos).max()),
        subspace_principal_cosines=singular,subspace_trace_overlap_fraction=float((singular**2).mean()),
        subspace_ranks=[int(np.linalg.matrix_rank(unit[v])) for v in groups.values()],
        matching_status='DONE' if supported else 'NA_INSUFFICIENT_MATCHED_POOL',
        separate_group_matching=separate,
        uniform_unmatched_per_PC_quantiles=np.quantile(uniform_PC,[.025,.5,.975]),
        uniform_unmatched_per_band_quantiles=np.quantile(uniform_band,[.025,.5,.975]),
        no_observed_CI='Fixed-list geometry. Matched ranges are random-set composition ranges, not selection uncertainty or independent generalization CIs.')
    if supported:
        geometry.update(matched_per_PC_quantiles=np.quantile(ropc,[.025,.5,.975]),matched_per_band_quantiles=np.quantile(roband,[.025,.5,.975]),
            per_PC_background_fraction_at_or_above=float((ropc>=overlap_PC).mean()),band_background_fraction_at_or_above=float((roband>=overlap_band).mean()))
    savecsv(O/'tables/pair_absolute_cosine.csv',[dict(math_feature=int(f),biology_feature=int(g),abs_cosine=float(abs(cos[i,j]))) for i,f in enumerate(groups['math']) for j,g in enumerate(groups['biology'])])
    savecsv(O/'tables/group_PC_overlap.csv',[dict(PC=k+1,math=pmeans['math'][k],biology=pmeans['biology'][k],common=min(pmeans['math'][k],pmeans['biology'][k])) for k in range(1024)])
    savecsv(O/'tables/group_band_overlap.csv',[dict(band=k+1,PC_start=k*64+1,PC_end=(k+1)*64,math=bmeans['math'][k],biology=bmeans['biology'][k],common=min(bmeans['math'][k],bmeans['biology'][k])) for k in range(16)])
    spectr={}
    spectrumrows=[]
    for d,ix in groups.items():
        head=bands[ix,0];r=dict(n=len(ix),PC1_64_mean=float(head.mean()),PC1_64_median=float(np.median(head)),members_head_over_half=int((head>.5).sum()),top2_share_of_group_head=float(np.sort(head)[-2:].sum()/head.sum()))
        if supported:r['matched_PC1_64_mean_quantiles']=np.quantile(rbmean[d][:,0],[.025,.5,.975])
        elif separate[d]['status']=='DONE':r['matched_PC1_64_mean_quantiles']=separate[d]['PC1_64_mean_quantiles']
        spectr[d]=r
        for k in range(16):
            row=dict(population=d,band=k+1,mean=float(bands[ix,k].mean()),median=float(np.median(bands[ix,k])),p25=float(np.quantile(bands[ix,k],.25)),p75=float(np.quantile(bands[ix,k],.75)))
            if supported:row.update(matched_p025=float(np.quantile(rbmean[d][:,k],.025)),matched_median=float(np.median(rbmean[d][:,k])),matched_p975=float(np.quantile(rbmean[d][:,k],.975)))
            spectrumrows.append(row)
    for d,ix in [('full_dictionary',allids[valid]),('eligible_pool',allids[eligible&valid])]:
        for k in range(16):spectrumrows.append(dict(population=d,band=k+1,mean=float(bands[ix,k].mean()),median=float(np.median(bands[ix,k])),p25=float(np.quantile(bands[ix,k],.25)),p75=float(np.quantile(bands[ix,k],.75))))
    savecsv(O/'tables/spectrum_summary.csv',spectrumrows);dump(O/'analysis/spectrum.json',dict(groups=spectr,geometry=geometry,full_dictionary_PC1_64_mean=float(bands[:,0].mean()),full_dictionary_PC1_64_median=float(np.median(bands[:,0]))))
    print('GEOMETRY_DONE',clean(geometry),flush=True)
    # Decode only observed input token IDs with the original tokenizer. No
    # decoder-to-vocabulary matrix product is performed.
    from tokenizers import Tokenizer
    assert sha(TOKENIZER)=='c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539'
    tok=Tokenizer.from_file(str(TOKENIZER))
    refs=jl(R/'data/reference.jsonl');rt=np.concatenate([r['token_ids'] for r in refs]);assert len(rt)==65536
    tc=np.bincount(rt,minlength=tok.get_vocab_size());tn=len(rt)
    n=len(ids);zlist=[];tokenlist=[];di_list=[];poslist=[];raw_files=[]
    for di,r in enumerate(docs):
        path=R/'forward/documents'/f"{r['seq_id']}.npz";v=np.load(path);raw_files.append(path)
        assert v['token_ids'].tolist()==r['token_ids']
        dense=np.zeros((160,n),np.float32);ptr=v['CC_ptr'];fi=v['CC_ids'];zz=v['CC_z']
        mapping=np.full(16384,-1,int);mapping[ids]=np.arange(n)
        for p in range(32,192):
            lo,hi=int(ptr[p]),int(ptr[p+1]);ix=mapping[fi[lo:hi]];use=ix>=0;dense[p-32,ix[use]]=zz[lo:hi][use]
        assert np.allclose(dense.sum(0,dtype=np.float64),a['sum_z'][di,ids],rtol=1e-6,atol=1e-7)
        zlist.append(dense);tokenlist.extend(r['token_ids'][32:192]);di_list.extend([di]*160);poslist.extend(range(32,192))
    Z=np.concatenate(zlist);T=np.array(tokenlist);DI=np.array(di_list);POS=np.array(poslist)
    np.savez_compressed(O/'analysis/natural_selected_positions.npz',z=Z,token_id=T,document_index=DI,position=POS,feature_ids=ids)
    mt=np.bincount(T[y[DI]==1],minlength=len(tc));bt=np.bincount(T[y[DI]==0],minlength=len(tc));tokenrows=[];tokenfeatures=[];examples=[]
    for j,f in enumerate(ids):
        active=Z[:,j]>0;ats=T[active];seen=tc[ats]>0;rates=tc[ats[seen]]/tn
        unique,cnt=np.unique(ats,return_counts=True);order=np.lexsort((unique,-cnt));ut=unique[order];uc=cnt[order]
        rec=dict(feature=int(f),group='math' if j<16 else 'biology',active_positions=int(active.sum()),active_docs=int(np.unique(DI[active]).size),distinct_token_ids=len(unique),top1_token_fraction=float(uc[0]/active.sum()),top5_token_fraction=float(uc[:5].sum()/active.sum()),
            token_reference_seen_n=int(seen.sum()),token_reference_unseen_n=int((~seen).sum()),token_reference_unseen_fraction=float((~seen).mean()),token_rate_median=float(np.median(rates)),token_rate_p10=float(np.quantile(rates,.1)),token_rate_p90=float(np.quantile(rates,.9)),feature_reference_rate=float(freq[f]),
            active_math_positions=int((active&(y[DI]==1)).sum()),active_biology_positions=int((active&(y[DI]==0)).sum()))
        rec.update(active_token_panel_math_fraction_median=float(np.median(mt[ats]/(mt[ats]+bt[ats]))),
            active_positions_token_more_math_fraction=float((mt[ats]>bt[ats]).mean()),
            active_positions_token_more_biology_fraction=float((mt[ats]<bt[ats]).mean()),
            active_positions_token_equal_fraction=float((mt[ats]==bt[ats]).mean()))
        # Token identities may occur at multiple positions; every active position
        # is one equally weighted observation. Token domain rates are a separate
        # descriptive panel quantity, never an exclusive-corpus label.
        tokenfeatures.append(rec)
        for t,c in zip(ut,uc):tokenrows.append(dict(feature=int(f),token_id=int(t),token_string=tok.decode([int(t)],skip_special_tokens=False),active_positions=int(c),reference_count=int(tc[t]),reference_N=tn,reference_rate=float(tc[t]/tn) if tc[t]>0 else None,panel_math_count=int(mt[t]),panel_biology_count=int(bt[t]),panel_positions_per_domain=9600,panel_math_fraction=float(mt[t]/(mt[t]+bt[t]))))
        # High and ordinary (nearest positive median) examples from distinct
        # documents, maximum two illustrated positions per document per member.
        highorder=np.flatnonzero(active)[np.argsort(-Z[active,j],kind='stable')]
        med=np.median(Z[active,j]);ordinary=np.flatnonzero(active)[np.argsort(abs(Z[active,j]-med),kind='stable')]
        chosen=[];docquota={}
        for typ,arr in [('high',highorder),('ordinary',ordinary)]:
            chosen_docs=set();got=0
            for ix in arr:
                di=int(DI[ix])
                if ix in chosen or di in chosen_docs or docquota.get(di,0)>=2:continue
                chosen.append(int(ix));chosen_docs.add(di);docquota[di]=docquota.get(di,0)+1;got+=1
                examples.append(example_record(tok,docs,ix,int(f),typ,Z[:,j],T,DI,POS,tc))
                if got==2:break
        # Find a same-token minimum response in another document; prefer the
        # opposite domain when a comparable occurrence exists, without claiming
        # a controlled intervention.
        for origin in chosen[:2]:
            t=T[origin];ixs=np.flatnonzero((T==t)&(DI!=DI[origin]));ixs=ixs[np.argsort(Z[ixs,j],kind='stable')]
            for ix in ixs:
                di=int(DI[ix])
                if docquota.get(di,0)>=2:continue
                docquota[di]=docquota.get(di,0)+1
                row=example_record(tok,docs,int(ix),int(f),'same_token_low_or_inactive',Z[:,j],T,DI,POS,tc);row['paired_high_document']=docs[int(DI[origin])]['seq_id'];row['paired_high_z']=float(Z[origin,j]);examples.append(row);break
    savecsv(O/'tables/token_member_summary.csv',tokenfeatures);savecsv(O/'tables/active_token_counts.csv',tokenrows);savecsv(O/'tables/real_token_examples.csv',examples)
    usedtokens=np.unique(np.r_[T,rt]);savecsv(O/'tables/reference_token_counts.csv',[dict(token_id=int(t),string=tok.decode([int(t)],skip_special_tokens=False),count=int(tc[t]),N=tn,rate=float(tc[t]/tn) if tc[t] else None,status='seen' if tc[t] else 'unseen_not_zero_probability',panel_math_count=int(mt[t]),panel_biology_count=int(bt[t])) for t in usedtokens])
    # Dependence on which natural documents were observed: resample whole
    # documents within each domain, keeping the 32-member list and reference
    # fixed. This is not a bootstrap of the member-selection process.
    medrate=np.array([r['token_rate_median'] for r in tokenfeatures]);corr={}
    for d,jx in [('all',np.arange(32)),('math',np.arange(16)),('biology',np.arange(16,32))]:corr[d]=dict(spearman=float(spearmanr(freq[ids[jx]],medrate[jx]).statistic),n=len(jx))
    rrng=np.random.default_rng(2026103002);boots=[]
    for rep in range(300):
        mult=np.zeros(120,int)
        for label in [0,1]:
            pool=np.flatnonzero(y==label);mult+=np.bincount(rrng.choice(pool,len(pool)),minlength=120)
        wm=mult[DI];meds=[]
        for j in range(32):
            use=(Z[:,j]>0)&(tc[T]>0)&(wm>0);vv=tc[T[use]]/tn;ww=wm[use];order=np.argsort(vv);cum=np.cumsum(ww[order]);meds.append(vv[order[np.searchsorted(cum,cum[-1]/2)]])
        boots.append([spearmanr(freq[ids[jx]],np.array(meds)[jx]).statistic for jx in [np.arange(32),np.arange(16),np.arange(16,32)]])
    for j,d in enumerate(['all','math','biology']):corr[d]['document_bootstrap_interval']=np.quantile(np.array(boots)[:,j],[.025,.975])
    dump(O/'analysis/token_summary.json',dict(reference_positions=tn,reference_windows=256,reference_canonical_docs=254,panel_positions=19200,correlations=corr,unseen_rule='exclude unseen IDs from frequency quantiles; report unseen count/share separately; no pseudocount and never log(0)',example_rule='two high, two median-active, up to two same-token low; maximum2 examples/document/member; only read prefix through current position'))
    print('TOKENS_DONE',clean(corr),flush=True)
    # All-member fixed-target z already exists in R08; select the frozen columns.
    panel=jl(R7/'data/panel.jsonl');cache=np.load(R8/'forward/target_readings.npz');assert cache['seq_ids'].tolist()==[r['seq_id'] for r in panel]
    tz=cache['z'][:,ids].astype(float);effects=[];familyrows=[];support=[];statuses=[]
    rng=np.random.default_rng(2026103003)
    cell={}
    for split in splits:
        fam=sorted(set(r['family'] for r in panel if r['split']==split));nf=len(fam);boots=rng.integers(0,nf,(2000,nf))
        for ending in [0,1]:
            perword=[]
            for wording in [0,1]:
                mi=[next(i for i,r in enumerate(panel) if r['family']==f and r['domain']=='math' and r['wording']==wording and r['ending']==ending) for f in fam]
                bi=[next(i for i,r in enumerate(panel) if r['family']==f and r['domain']=='biology' and r['wording']==wording and r['ending']==ending) for f in fam]
                delta=tz[mi]-tz[bi];perword.append(delta);mean=delta.mean(0);lo,hi=np.quantile(delta[boots].mean(1),[.025,.975],axis=0)
                for j,f in enumerate(ids):
                    rec=dict(feature=int(f),group='math' if j<16 else 'biology',split=split,target_token_id=panel[mi[0]]['target_token_id'],target=panel[mi[0]]['target_word'],wording=wording,n_families=nf,delta_math_minus_biology=float(mean[j]),CI_low=float(lo[j]),CI_high=float(hi[j]),active_families_math=int((tz[mi,j]>0).sum()),active_families_biology=int((tz[bi,j]>0).sum()))
                    effects.append(rec);cell[(int(f),split,ending,wording)]=rec
                    for k,ff in enumerate(fam):familyrows.append(dict(feature=int(f),family=ff,split=split,ending=ending,wording=wording,math_z=float(tz[mi[k],j]),biology_z=float(tz[bi[k],j]),delta=float(delta[k,j])))
    # A requires same fixed token, both wordings, discovery and old heldout,
    # direction as selected in natural documents, at least3 active families per
    # cell, and pointwise95% intervals in that direction. This is a transparent
    # descriptive label, not original R09 confirmation or a corrected test.
    for j,f in enumerate(ids):
        sign=1 if j<16 else -1;passing=[];nactive=int((tz[:,j]>0).sum())
        for e in [0,1]:
            rows=[cell[(int(f),s,e,w)] for s in ['discovery','heldout'] for w in [0,1]]
            passed=all(max(r['active_families_math'],r['active_families_biology'])>=3 and (r['CI_low']>0 if sign>0 else r['CI_high']<0) for r in rows)
            if passed:passing.append(e)
        natural=next(r for r in tokenfeatures if r['feature']==f)
        category='A' if passing else ('B' if nactive>0 and natural['top5_token_fraction']>=.5 else 'C')
        why='same-token context difference repeats across wordings, discovery and exposed old heldout' if passing else ('natural activation concentrated >=50% on five input token IDs; not identity-only proof' if category=='B' else ('test coverage insufficient: never active on fixed targets' if nactive==0 else 'support or cross-wording stability insufficient'))
        statuses.append(dict(feature=int(f),category=category,reason=why,A_passing_targets='|'.join(['example' if e==0 else 'explanation' for e in passing]),fixed_target_active_positions=nactive,total_fixed_target_positions=384))
    savecsv(O/'tables/context_effects.csv',effects);savecsv(O/'tables/context_family_values.csv',familyrows);savecsv(O/'tables/context_categories.csv',statuses)
    # Old and new membership mapping includes the entire old/new union, with
    # individual rankings preserved. R04 natural64 and R09 controlled64 are
    # distinct lists despite their equal size.
    old=js(S/'analysis/candidate_freeze.json')['dictionaries']['CC']['groups'];r9f=js(R9/'analysis/candidate_freeze.json')
    rep=readcsv(R9/'tables/domain_candidate_replication.csv');repids=[int(r['feature_id']) for r in rep if r['cross_condition_replication']=='True']
    lists=dict(main_math16=groups['math'].tolist(),main_biology16=groups['biology'].tolist(),**{'R04_'+k:v for k,v in old.items()},**{'R09_'+d+'64':v for d,v in r9f['domain_candidates'].items()},**{'R09_contribution32_ending'+k:v for k,v in r9f['top32_by_ending'].items()},R09_union141=r9f['all_candidates'],R09_replicated36=repids)
    screening=js(R/'CC_domain_top16_top32_20261028T140417Z/CC_四份固定名单.json')
    lists.update({'R04_same_token_'+r['domain']+str(r['top_n']):r['feature_ids'] for r in screening})
    dump(O/'analysis/old_same_token_lists.json',screening)
    union=sorted(set(sum(lists.values(),[])));maprows=[]
    for f in union:
        row=dict(feature=f)
        for name,ix in lists.items():row[name+'_rank']=ix.index(f)+1 if f in ix else None
        maprows.append(row)
    savecsv(O/'tables/list_mapping.csv',maprows);dump(O/'analysis/list_definitions.json',dict(lists=lists,main_intersections={k:len(set(v)&set(ids)) for k,v in lists.items()}))
    # Master table binds all five questions to the same member denominator.
    metrics={int(r['feature']):r for r in readcsv(S/'analysis/CC_all_feature_metrics.csv')}
    master=[]
    for j,f in enumerate(ids):
        r=dict(feature=int(f),group='math' if j<16 else 'biology',rank=j%16+1,dictionary=CHECKPOINT,decoder_interface='zero-based block27 residual-post before final norm',discovery_AUC_math=float(aucs['discovery'][f]),development_AUC_math=float(aucs['development'][f]),heldout_AUC_math=float(aucs['heldout'][f]),heldout_direction_fixed_AUC=float(aucs['heldout'][f] if j<16 else 1-aucs['heldout'][f]),heldout_direction_fixed_CI_low=float(metrics[int(f)]['heldout_auc_CI_low']),heldout_direction_fixed_CI_high=float(metrics[int(f)]['heldout_auc_CI_high']),DCLM_hits=int(hits[f]),DCLM_positions=65536,feature_reference_rate=float(freq[f]),original_frequency_group=fb[f],R09_log_frequency_group=lb[f],decoder_norm=float(norm[f]),test1_frequency='DONE',test2_geometry='DONE',test3_overlap='DONE',test4_natural_token='DONE',test5_context=next(r['category'] for r in statuses if r['feature']==f))
        for split in splits:
            for label,name in [(1,'math'),(0,'biology')]:r[f'{split}_{name}_active_documents']=int((counts[(sp==split)&(y==label),f]>0).sum())
        master.append(r)
    savecsv(O/'tables/master_members.csv',master)
    summary=dict(completed_utc=timestamp(),main_n=32,groups={d:len(v) for d,v in groups.items()},eligible_n=int(eligible.sum()),
        heldout_direction_fixed_AUC_median={d:float(np.median([r['heldout_direction_fixed_AUC'] for r in master if r['group']==d])) for d in groups},
        frequency_counts=binrows,spectrum=spectr,geometry=geometry,token_correlations=corr,
        context_category_counts={c:sum(r['category']==c for r in statuses) for c in ['A','B','C']},context_A_members=[r for r in statuses if r['category']=='A'],
        context_allzero_members=[r['feature'] for r in statuses if r['fixed_target_active_positions']==0],
        legacy_intersections={k:len(set(v)&set(ids)) for k,v in lists.items()},
        missing_new_forward_items=[],limits=['no new controlled natural-token pair edits; old caches cannot eliminate lexical/source/style rivals','no causal or routing/functional measurements','old heldout repeatedly exposed'],
        new_forwards=0,new_training=0,new_PCA=0,new_distance_inputs=0,scientific_acceptance='Unknown')
    dump(O/'analysis/results.json',summary)
    sourcepaths=[R/'data/documents.jsonl',R/'data/reference.jsonl',R/'forward/documents_CC.npz',R/'forward/reference_CC.npz',S/'analysis/candidate_freeze.json',S/'analysis/CC_all_feature_metrics.csv',Path(fr['basis']),R9/'analysis/decoder_and_scale.npz',R8/'forward/target_readings.npz',R7/'data/panel.jsonl',R9/'analysis/candidate_freeze.json',R9/'tables/domain_candidate_replication.csv',B/'R05_distance_attention_20261028/analysis/CC_frequency_bins.json',R9/'frequency_family/config.json',TOKENIZER]+raw_files
    dump(O/'source_manifest.json',dict(created_utc=timestamp(),sources={str(p):dict(bytes=p.stat().st_size,sha256=sha(p)) for p in sourcepaths},new_forwards=0,new_training=0))
    print('ALL_DONE',clean({k:summary[k] for k in ['main_n','context_category_counts','heldout_direction_fixed_AUC_median','legacy_intersections']}),flush=True)

def example_record(tok,docs,ix,f,kind,zz,T,DI,POS,tc):
    di=int(DI[ix]);p=int(POS[ix]);r=docs[di];prefix=tok.decode(r['token_ids'][:p],skip_special_tokens=False);current=tok.decode([int(T[ix])],skip_special_tokens=False)
    return dict(feature=f,example_type=kind,document=r['seq_id'],domain=r['domain'],split=r['split'],source_url=r['url'],position_zero_based=p,token_id=int(T[ix]),token_string=current,z=float(zz[ix]),reference_token_count=int(tc[T[ix]]),reference_token_N=65536,read_prefix=prefix,current_token=current,visible_through_current=tok.decode(r['token_ids'][:p+1],skip_special_tokens=False))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--freeze',action='store_true');args=ap.parse_args()
    if args.freeze:freeze()
    else:main()
