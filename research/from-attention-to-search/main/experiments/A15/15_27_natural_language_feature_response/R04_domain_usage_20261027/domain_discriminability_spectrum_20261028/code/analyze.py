"""Cache-only R04 exploratory discriminability. No torch, model, PCA or fitting."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '4')
os.environ.setdefault('OMP_NUM_THREADS', '4')
from pathlib import Path
import json, csv, hashlib, time, platform
import numpy as np
from scipy.stats import rankdata

O = Path(__file__).resolve().parent
C = json.loads((O/'config.json').read_text())
R = Path(os.environ.get('R04_SOURCE_ROOT',C['source_root']))
A = O/'analysis'; A.mkdir(exist_ok=True)

def dump(p, x):
    def clean(v):
        if isinstance(v, dict): return {str(k):clean(w) for k,w in v.items()}
        if isinstance(v, (list,tuple)): return [clean(w) for w in v]
        if isinstance(v, np.ndarray): return clean(v.tolist())
        if isinstance(v, np.generic): return clean(v.item())
        if isinstance(v,float) and not np.isfinite(v): return None
        return v
    Path(p).write_text(json.dumps(clean(x),ensure_ascii=False,indent=2,allow_nan=False)+'\n')

def writecsv(p, rows):
    with Path(p).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader()
        for row in rows:
            w.writerow({k:('' if v is None or isinstance(v,float) and not np.isfinite(v) else v) for k,v in row.items()})

def auc(x, y):
    """One column per feature; raw probability math score > bio score."""
    nm=int(y.sum()); nb=len(y)-nm
    return (rankdata(x,axis=0,method='average')[y==1].sum(0)-nm*(nm+1)/2)/(nm*nb)

def orient(v, direction):
    return np.where(direction>0,v,np.where(direction<0,1-v,np.nan))

def quantile_ci(v):
    # Avoid warnings for endpoints whose bootstrap samples have no active document.
    lo=np.full(v.shape[1],np.nan); hi=lo.copy()
    valid=np.isfinite(v).any(0)
    lo[valid],hi[valid]=np.nanquantile(v[:,valid],[.025,.975],axis=0)
    return lo,hi

def main():
    t=time.time()
    docs=[json.loads(s) for s in (R/'data/documents.jsonl').read_text().splitlines()]
    y=np.array([x['label'] for x in docs]); splits=np.array([x['split'] for x in docs])
    idx={s:np.flatnonzero(splits==s) for s in ['discovery','development','heldout']}
    rng=np.random.default_rng(C['bootstrap']['seed']); B=C['bootstrap']['draws']
    wm=np.array([np.bincount(rng.integers(0,20,20),minlength=20) for _ in range(B)],dtype=float)
    wb=np.array([np.bincount(rng.integers(0,20,20),minlength=20) for _ in range(B)],dtype=float)
    wp=(wm[:,:,None]*wb[:,None,:]).reshape(B,400)/400
    np.savez_compressed(A/'bootstrap_document_multiplicities.npz',math=wm,bio=wb)
    checks={'constant_auc':bool(auc(np.ones((4,1)),np.array([1,1,0,0]))[0]==.5),
            'separated_auc':bool(auc(np.array([[2],[3],[0],[1]]),np.array([1,1,0,0]))[0]==1),
            'reversed_auc':bool(auc(np.array([[0],[1],[2],[3]]),np.array([1,1,0,0]))[0]==0)}
    summaries={}; freeze={}; data={}
    # Selection reads only discovery slices. Freeze before computing new heldout statistics.
    for name in ['SAE','CC']:
        a=np.load(R/f'forward/documents_{name}.npz'); counts=a['counts'].astype(float)
        native=a['sum_z'].astype(float)*a['decoder_norm'][None,:]
        x=native/160; tr=idx['discovery']; f=np.arange(counts.shape[1])
        sm=(counts[tr[y[tr]==1]]>0).sum(0); sb=(counts[tr[y[tr]==0]]>0).sum(0)
        eligible=(sm>=5)&(sb>=5); disc=auc(x[tr],y[tr]); direction=np.sign(disc-.5).astype(int)
        order=np.flatnonzero(eligible & (direction!=0)); order=order[np.lexsort((order,-abs(disc[order]-.5)))]
        old=json.loads((R/f'analysis/{name}_candidate_freeze.json').read_text())
        groups={'new_top16':order[:16].tolist(),
                'expanded_math64':order[direction[order]>0][:64].tolist(),
                'expanded_bio64':order[direction[order]<0][:64].tolist(),
                'old_shared32':old['shared'],'old_math16':old['math'],'old_bio16':old['bio']}
        rms=np.sqrt(a['sum_z2'][tr].astype(float).sum(0)/(len(tr)*160))*a['decoder_norm']
        freeze[name]={'eligible_count':int(eligible.sum()),'discovery_direction_ties':int((eligible&(direction==0)).sum()),'groups':groups,
                      'top16_discovery_auc':[float(disc[i]) for i in groups['new_top16']],
                      'top16_direction':[int(direction[i]) for i in groups['new_top16']],
                      'top16_discovery_token_RMS':[float(rms[i]) for i in groups['new_top16']]}
        data[name]=(a,counts,native,x,sm,sb,eligible,disc,direction,groups,rms)
        np.savez_compressed(A/f'{name}_discovery_freeze.npz',direction=direction,raw_auc=disc,eligible=eligible,order=order,RMS=rms,support_math=sm,support_bio=sb)
    freeze_path=A/'candidate_freeze.json'
    if freeze_path.exists():
        assert json.loads(freeze_path.read_text())['dictionaries']==freeze
    else:
        dump(freeze_path,{'frozen_at':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
                         'selection':'new discovery-only ranking; old heldout already examined historically',
                         'config_sha256':hashlib.sha256((O/'config.json').read_bytes()).hexdigest(),'dictionaries':freeze})
    print('CANDIDATES_FROZEN',json.dumps({k:{'eligible':v['eligible_count'],'top16':v['groups']['new_top16'],'math':len(v['groups']['expanded_math64']),'bio':len(v['groups']['expanded_bio64'])} for k,v in freeze.items()}),flush=True)
    for name in ['SAE','CC']:
        a,counts,native,x,sm,sb,eligible,disc,direction,groups,rms=data[name]
        F=counts.shape[1]; te=idx['heldout']; im=te[y[te]==1]; ib=te[y[te]==0]
        hit=counts/160; cond=np.divide(native,counts,out=np.full_like(native,np.nan),where=counts>0)
        checks[name+'_zero_conditional_is_NA']=bool(np.isnan(cond[counts==0]).all())
        checks[name+'_positive_document_identity']=bool(np.allclose((hit*cond)[counts>0],x[counts>0],rtol=1e-12,atol=1e-12))
        checks[name+'_seq_ids_match']=bool(a['seq_id'].tolist()==[z['seq_id'] for z in docs])
        hold_raw=auc(x[te],y[te]); dev_raw=auc(x[idx['development']],y[idx['development']])
        hold=orient(hold_raw,direction); dev=orient(dev_raw,direction); dauc=orient(disc,direction)
        ref=np.load(R/f'forward/reference_{name}.npz'); refhits=ref['counts'].sum(0).astype(int)
        assert int(ref['n_positions'].sum())==65536
        freq=refhits/65536
        pool=np.unique(np.concatenate([np.flatnonzero(eligible)]+[np.array(v,dtype=int) for v in groups.values()]))
        ci_low=np.full(F,np.nan);ci_high=ci_low.copy()
        # Each feature's exact20x20 pair comparison; bootstrap weights resample documents, not pairs.
        for start in range(0,len(pool),256):
            fs=pool[start:start+256]
            v=x[im[:,None],fs[None,:]][:,None,:]-x[ib[:,None],fs[None,:]][None,:,:]
            pair=(v>0).astype(float)+.5*(v==0); boot=np.clip(wp@pair.reshape(400,len(fs)),0,1)
            boot=orient(boot,direction[fs][None,:]);ci_low[fs],ci_high[fs]=quantile_ci(boot)
        selected=np.unique(np.concatenate([np.array(v,dtype=int) for v in groups.values()]))
        umean={}; uci={}; statrows=[]
        for metric,mat in [('hit',hit),('conditional',cond),('mean',x)]:
            vals=[]
            for label,jx,w in [('math',im,wm),('bio',ib,wb)]:
                valid=np.isfinite(mat[jx]); vv=np.nan_to_num(mat[jx]);den=valid.sum(0)
                mu=np.divide(vv.sum(0),den,out=np.full(F,np.nan),where=den>0);umean[metric+'_'+label]=mu
                bootden=w@valid[:,selected].astype(float)
                z=np.divide(w@vv[:,selected],bootden,out=np.full((B,len(selected)),np.nan),where=bootden>0)
                vals.append(z);lo,hi=quantile_ci(z);uci[metric+'_'+label]=(lo,hi)
            uci[metric+'_diff']=quantile_ci(vals[0]-vals[1])
        byselected={int(f):i for i,f in enumerate(selected)}
        for f in range(F):
            row={'dictionary':name,'feature':f,'eligible':bool(eligible[f]),'discovery_direction':int(direction[f]),'discovery_raw_auc_math':float(disc[f]),
                 'discovery_direction_fixed_auc':float(dauc[f]),'development_direction_fixed_auc':float(dev[f]),'heldout_direction_fixed_auc':float(hold[f]),
                 'heldout_auc_CI_low':float(ci_low[f]),'heldout_auc_CI_high':float(ci_high[f]),'heldout_auc_minus_chance':float(hold[f]-.5),
                 'heldout_auc_minus_chance_CI_low':float(ci_low[f]-.5),'heldout_auc_minus_chance_CI_high':float(ci_high[f]-.5),
                 'heldout_minus_discovery_auc':float(hold[f]-dauc[f]),'heldout_minus_discovery_auc_CI_low':float(ci_low[f]-dauc[f]),'heldout_minus_discovery_auc_CI_high':float(ci_high[f]-dauc[f]),
                 'discovery_support_math':int(sm[f]),'discovery_support_bio':int(sb[f]),'heldout_support_math':int((counts[im,f]>0).sum()),'heldout_support_bio':int((counts[ib,f]>0).sum()),
                 'DCLM_hits':int(refhits[f]),'DCLM_rate':float(freq[f]),'DCLM_low_support':bool(refhits[f]<20),'discovery_token_RMS':float(rms[f]),
                 'groups':'|'.join(k for k,v in groups.items() if f in v)}
            for metric in ['hit','conditional','mean']:
                for label in ['math','bio']:row[metric+'_'+label]=float(umean[metric+'_'+label][f])
                row[metric+'_math_minus_bio']=float(umean[metric+'_math'][f]-umean[metric+'_bio'][f])
                if f in byselected:
                    j=byselected[f]
                    for label in ['math','bio','diff']:
                        row[metric+'_'+label+'_CI_low']=float(uci[metric+'_'+label][0][j]);row[metric+'_'+label+'_CI_high']=float(uci[metric+'_'+label][1][j])
                else:
                    for label in ['math','bio','diff']:
                        row[metric+'_'+label+'_CI_low']=float('nan');row[metric+'_'+label+'_CI_high']=float('nan')
            for label,jx in [('math',im),('bio',ib)]:
                den=counts[jx,f].sum()
                row['position_weighted_conditional_'+label]=float(native[jx,f].sum()/den) if den else float('nan')
            statrows.append(row)
        writecsv(A/f'{name}_all_feature_metrics.csv',statrows)
        writecsv(A/f'{name}_selected_feature_metrics.csv',[statrows[i] for i in selected])
        writecsv(A/f'{name}_display16_metrics.csv',[statrows[i] for i in groups['new_top16']])
        for group,ids in groups.items():
            writecsv(A/f'{name}_{group}_metrics.csv',[statrows[i] for i in ids])
        np.savez_compressed(A/f'{name}_per_document_metrics.npz',feature_ids=selected,seq_id=a['seq_id'],counts=counts[:,selected],hit_fraction=hit[:,selected],conditional_native_contribution=cond[:,selected],mean_native_contribution=x[:,selected],RMS=rms[selected],labels=y,split=splits)
        np.savez_compressed(A/f'{name}_all_feature_results.npz',eligible=eligible,discovery_auc=disc,direction=direction,development_auc=dev,heldout_auc=hold,heldout_auc_ci_low=ci_low,heldout_auc_ci_high=ci_high,reference_hits=refhits,reference_frequency=freq)
        # Exact joint-bin matching; no forced retention, fallback, or heldout-dependent matches.
        rfbin=np.floor(np.log2(refhits+.5)).astype(int);suppbin=np.floor((sm+sb)/5).astype(int)
        rrng=np.random.default_rng(C['random']['seed']+(name=='CC')); rand={}; rids={}
        for group,ids0 in groups.items():
            ids=np.array(ids0);bins=[(int(rfbin[f]),int(suppbin[f])) for f in ids];need={b:bins.count(b) for b in sorted(set(bins))};pools={b:np.flatnonzero(eligible & ~np.isin(np.arange(F),ids)&(rfbin==b[0])&(suppbin==b[1])) for b in need}
            shortages=[{'bin':list(b),'needed':n,'available':len(pools[b])} for b,n in need.items() if len(pools[b])<n]
            record={'group_size':len(ids),'bin_counts':[{'bin':list(b),'count':n,'pool':len(pools[b])} for b,n in need.items()],'shortages':shortages,'forced_retained_members':0}
            if shortages:record['status']='NA_INSUFFICIENT_MATCH_POOL';rand[group]=record;continue
            sets=np.array([np.concatenate([rrng.choice(pools[b],n,replace=False) for b,n in need.items()]) for _ in range(C['random']['draws'])])
            assert not np.isin(sets,ids).any()
            scores=np.nanmean(hold[sets],axis=1);record.update(status='DONE_DESCRIPTIVE',draws=len(sets),observed_mean_auc=float(np.nanmean(hold[ids])),random_mean_auc_quantiles=np.quantile(scores,[.025,.5,.975]).tolist(),random_valid_direction_counts=np.isfinite(hold[sets]).sum(1).tolist(),matched_reference_frequency_median_quantiles=np.quantile(np.median(freq[sets],axis=1),[.025,.5,.975]).tolist(),spectral_comparison='NOT_RUN_REAL_H_MISSING')
            rand[group]=record;rids[group]=sets
        np.savez_compressed(A/f'{name}_matched_random_ids.npz',**rids);dump(A/f'{name}_matched_random_summary.json',rand)
        gs={}
        for group,ids0 in groups.items():
            ids=np.array(ids0); h=hold[ids];rh=refhits[ids]; ranks=np.array([100*((refhits<v).sum()+.5*(refhits==v).sum())/F for v in rh]);ff=freq[ids]
            s_freq=direction[ids]*(umean['hit_math'][ids]-umean['hit_bio'][ids]);s_int=direction[ids]*(umean['conditional_math'][ids]-umean['conditional_bio'][ids])
            gs[group]={'n':len(ids),'discovery_math_direction':int((direction[ids]>0).sum()),'discovery_bio_direction':int((direction[ids]<0).sum()),'eligible_new_gate':int(eligible[ids].sum()),'heldout_auc_quantiles':np.nanquantile(h,[0,.25,.5,.75,1]).tolist(),'heldout_auc_ge_0p8':int((h>=.8).sum()),'heldout_auc_le_0p5':int((h<=.5).sum()),'DCLM_rate_quantiles':np.quantile(ff,[0,.25,.5,.75,1]).tolist(),'DCLM_rank_percentile_median':float(np.median(ranks)),'reference_low_support':int((rh<20).sum()),'all40docs_present':int((counts[te][:,ids]>0).all(0).sum()),'observed_usage_signs_not_confirmatory':{'more_frequent_and_stronger':int(((s_freq>0)&(s_int>0)).sum()),'more_frequent_not_stronger':int(((s_freq>0)&(s_int<=0)).sum()),'stronger_not_more_frequent':int(((s_freq<=0)&(s_int>0)).sum()),'neither_positive':int(((s_freq<=0)&(s_int<=0)).sum()),'conditional_NA':int((~np.isfinite(s_int)).sum())},'random_status':rand[group]['status']}
        summaries[name]={'eligible_count':int(eligible.sum()),'direction_ties':int((eligible&(direction==0)).sum()),'all_feature_count':F,'frequency_median_all':float(np.median(freq)),'groups':gs,'display_ids':groups['new_top16'],'display_native_examples':[{k:statrows[f][k] for k in ['feature','discovery_direction','heldout_direction_fixed_auc','heldout_auc_CI_low','heldout_auc_CI_high','DCLM_rate','hit_math','hit_bio','conditional_math','conditional_bio','mean_math','mean_bio']} for f in groups['new_top16']]}
        # Full source stats are enough to check original probe inputs without refitting them.
        olduse=np.load(R/f'analysis/{name}_candidate_document_usage.npz'); oo=olduse['feature_ids']
        checks[name+'_old_probe_input_exact']=bool(np.allclose(olduse['mean_native_contribution'],x[:,oo],rtol=2e-6,atol=2e-6))
        # Replay one fixed discovery and one fixed heldout document from saved sparse values.
        for di in [idx['discovery'][0],idx['heldout'][0]]:
            row=docs[di]; z=np.load(R/'forward/documents'/f"{row['seq_id']}.npz");ptr=z[name+'_ptr'];fids=z[name+'_ids'];zs=z[name+'_z'];lo,hi=int(ptr[32]),int(ptr[192]);cf=np.bincount(fids[lo:hi],minlength=F);sf=np.bincount(fids[lo:hi],weights=zs[lo:hi],minlength=F)
            checks[f'{name}_{row["seq_id"]}_count_replay']=bool(np.array_equal(cf,counts[di]));checks[f'{name}_{row["seq_id"]}_sum_replay']=bool(np.allclose(sf,a['sum_z'][di],rtol=2e-6,atol=2e-5))
        print('DONE',name,'seconds',round(time.time()-t,1),'groups',json.dumps({g:{'n':z['n'],'AUCmedian':z['heldout_auc_quantiles'][2],'freqmedian':z['DCLM_rate_quantiles'][2]} for g,z in gs.items()}),flush=True)
    # Independently compare small selected actual scores to sklearn's scalar implementation.
    from sklearn.metrics import roc_auc_score
    for name in ['SAE','CC']:
        _,_,_,x,_,_,_,_,direction,groups,_=data[name]
        for f in groups['new_top16'][:3]:
            scalar=roc_auc_score(y[idx['heldout']],direction[f]*x[idx['heldout'],f]);vec=orient(auc(x[idx['heldout'],f:f+1],y[idx['heldout']]),np.array([direction[f]]))[0]
            checks[f'{name}_f{f}_sklearn_scalar_auc']=bool(abs(scalar-vec)<1e-12)
    dump(A/'numerical_checks.json',{'checks':checks,'passed':all(checks.values()),'count':len(checks)})
    dump(A/'results.json',{'scope':'existing-data exploratory reuse; not new unbiased holdout','dictionaries':summaries,'PCA':'NOT_RUN_REAL_H_MISSING','new_forwards':0,'model_or_dictionary_training':0,'classifier_fits':0,'clustering':0,'runtime_seconds':time.time()-t,'python':platform.python_version(),'numpy':np.__version__,'checks_passed':all(checks.values())})
    assert all(checks.values()),checks

if __name__=='__main__':main()
