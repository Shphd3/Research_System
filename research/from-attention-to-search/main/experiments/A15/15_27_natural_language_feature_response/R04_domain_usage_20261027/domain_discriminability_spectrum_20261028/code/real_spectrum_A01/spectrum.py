"""True-h pooled PCA and frozen-coordinate spectra; statistical fitting, no LM/SAE training."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','4')
from pathlib import Path
import json,csv,time,hashlib
import numpy as np
O=Path(__file__).resolve().parent;S=O.parent;R=S.parent;A=O/'analysis'
C=json.loads((O/'amendment.json').read_text());G=json.loads((S/'analysis/candidate_freeze.json').read_text())['dictionaries']

def dump(p,x):
    def clean(v):
        if isinstance(v,dict):return {k:clean(w) for k,w in v.items()}
        if isinstance(v,(list,tuple)):return [clean(w) for w in v]
        if isinstance(v,np.ndarray):return clean(v.tolist())
        if isinstance(v,np.generic):return clean(v.item())
        if isinstance(v,float) and not np.isfinite(v):return None
        return v
    Path(p).write_text(json.dumps(clean(x),ensure_ascii=False,indent=2,allow_nan=False)+'\n')

def csvwrite(p,rows):
    with Path(p).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def bh(ps):
    ps=np.array(ps);ix=np.argsort(ps);q=np.empty(len(ps));q[ix]=np.minimum(1,np.minimum.accumulate((ps[ix]*len(ps)/np.arange(1,len(ps)+1))[::-1])[::-1]);return q

def bands(x):return x.reshape(*x.shape[:-1],16,64).sum(-1)

def bootstrap_weights(n,rng,B):
    return np.array([np.bincount(rng.integers(0,n,n),minlength=n) for _ in range(B)],dtype=float)

def mean_direction(bootstrap_m,bootstrap_b):
    return bootstrap_m-bootstrap_b

def main():
    t=time.time();done=json.loads((O/'completed.json').read_text());assert done['all_checks_pass'] and done['charged_forwards']==124
    assert hashlib.sha256((S/'analysis/candidate_freeze.json').read_bytes()).hexdigest()==C['candidate_freeze_sha256']
    docs=[json.loads(x) for x in (R/'data/documents.jsonl').read_text().splitlines()];labels=np.array([x['label'] for x in docs]);splits=np.array([x['split'] for x in docs]);ix={s:np.flatnonzero(splits==s) for s in ['discovery','development','heldout']}
    rng=np.random.default_rng(C['reproduction']['bootstrap_seed']);B=C['reproduction']['bootstrap_draws'];W={}
    for split,idx in ix.items():
        mi=idx[labels[idx]==1];bi=idx[labels[idx]==0];W[split]=(mi,bi,bootstrap_weights(len(mi),rng,B),bootstrap_weights(len(bi),rng,B))
    np.savez_compressed(A/'spectral_bootstrap_multiplicities.npz',**{f'{s}_{k}':v for s,(mi,bi,wm,wb) in W.items() for k,v in [('math_indices',mi),('bio_indices',bi),('math',wm),('bio',wb)]})
    summary={}; checks={}; primary=[]; row_features=[]; row_splits=[]; row_groups=[]; row_aux=[]
    import torch
    torch.set_num_threads(2)
    ckpaths={'SAE':Path('/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt'),'CC':Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt')}
    for name in ['SAE','CC']:
        H=np.stack([np.load(O/'raw_documents'/f"{r['seq_id']}.npz")[name+'_h'][32:192] for r in docs]).astype(np.float64)
        tr=H[ix['discovery']].reshape(-1,1024);mu=tr.mean(0);X=tr-mu;cov=X.T@X/(len(X)-1)
        lam,V=np.linalg.eigh(cov);order=np.argsort(lam)[::-1];lam=lam[order];V=V[:,order]
        negative=float(lam.min());assert negative>=-max(float(lam[0])*1e-10,1e-12);lam=np.maximum(lam,0)
        for j in range(1024):
            if V[np.argmax(abs(V[:,j])),j]<0:V[:,j]*=-1
        ranktol=float(lam[0]*max(X.shape)*np.finfo(float).eps);rank=int((lam>ranktol).sum());ev=lam/lam.sum()
        checkorth=float(np.max(abs(V.T@V-np.eye(1024))));checks[name+'_full_orthonormal_basis']=checkorth<1e-10
        checks[name+'_pooled_cov_trace']=bool(np.isclose(np.trace(cov),lam.sum(),rtol=1e-10))
        eigres=float(np.linalg.norm(cov@V-V*lam[None,:])/max(np.linalg.norm(cov),1e-12));checks[name+'_eigen_residual']=eigres<1e-10
        np.savez_compressed(A/f'{name}_common_basis.npz',mean=mu,PC_columns=V,eigenvalues=lam,explained_variance_fraction=ev,effective_rank=rank,rank_tolerance=ranktol,fit_seq_ids=np.array([docs[i]['seq_id'] for i in ix['discovery']]),fit_rows=9600,dimension=1024)
        coeff=((H-mu)@V);doc_mean=coeff.mean(1);doc_sum=coeff.sum(1);doc_sq=(coeff**2).sum(1)
        delta_train=doc_mean[ix['discovery'][labels[ix['discovery']]==1]].mean(0)-doc_mean[ix['discovery'][labels[ix['discovery']]==0]].mean(0)
        splitout={}
        for split,idx in ix.items():
            mi,bi,wm,wb=W[split];n=len(idx)*160;p=coeff[idx].reshape(-1,1024);var=p.var(0,ddof=1);varfrac=bands(var)/var.sum();second=bands((p*p).mean(0));delta=doc_mean[mi].mean(0)-doc_mean[bi].mean(0);d2=delta*delta;dfrac=bands(d2)/d2.sum()
            bs=wm@doc_sum[mi]+wb@doc_sum[bi];bss=wm@doc_sq[mi]+wb@doc_sq[bi];bvar=np.maximum((bss-bs*bs/n)/(n-1),0);bvfrac=bands(bvar)/bvar.sum(1)[:,None]
            bd=wm@doc_mean[mi]/len(mi)-wb@doc_mean[bi]/len(bi);bd2=bands(bd*bd);bdfrac=bd2/(bd*bd).sum(1)[:,None]
            cos=float(delta@delta_train/(np.linalg.norm(delta)*np.linalg.norm(delta_train)));bcos=bd@delta_train/(np.linalg.norm(bd,axis=1)*np.linalg.norm(delta_train))
            vc=np.quantile(bvfrac,[.025,.975],axis=0);dc=np.quantile(bdfrac,[.025,.975],axis=0)
            so={'documents':len(idx),'positions':n,'variance_fraction_by_band':varfrac,'variance_CI95':vc,'secondmoment_around_discovery_mean_by_band':second,'mean_difference_squared_by_band':bands(d2),'mean_difference_norm2':float(d2.sum()),'mean_difference_fraction_by_band':dfrac,'mean_difference_fraction_CI95':dc,'mean_difference_alignment_with_discovery':cos,'alignment_CI95':np.quantile(bcos,[.025,.975]),'variance_spectrum_cosine_with_discovery':float(varfrac@bands(ev)/(np.linalg.norm(varfrac)*np.linalg.norm(bands(ev))))}
            splitout[split]=so
            for b in range(16):row_splits.append({'dictionary':name,'split':split,'band':b+1,'PC_start':64*b+1,'PC_end':64*(b+1),'real_variance_fraction':float(varfrac[b]),'real_variance_CI_low':float(vc[0,b]),'real_variance_CI_high':float(vc[1,b]),'real_secondmoment_traincenter':float(second[b]),'domain_mean_difference_squared':float(bands(d2)[b]),'domain_mean_difference_fraction':float(dfrac[b]),'domain_difference_CI_low':float(dc[0,b]),'domain_difference_CI_high':float(dc[1,b])})
        checks[name+'_discovery_var_equals_eigenvalues']=bool(np.allclose(splitout['discovery']['variance_fraction_by_band'],bands(ev),atol=1e-10))
        # Same dictionary universe used in the original matching. This includes all newly eligible coordinates.
        frozen=np.load(S/f'analysis/{name}_discovery_freeze.npz');orig=G[name]['groups'];ids=np.unique(np.concatenate([np.flatnonzero(frozen['eligible'])]+[np.array(v) for v in orig.values()])).astype(int)
        payload=torch.load(ckpaths[name],map_location='cpu',mmap=True,weights_only=False)
        if name=='SAE':native=payload['state_dict']['decoder.weight'][:,ids].T.detach().numpy().astype(float)
        else:native=payload['crosscoder']['decoder'][-1,ids].detach().numpy().astype(float)*float(payload['normalization']['rms'][-1])
        norm=np.linalg.norm(native,axis=1);unit=native/norm[:,None];proj=(unit@V)**2;cum=np.cumsum(proj,axis=1);band=bands(proj);loc={int(f):i for i,f in enumerate(ids)}
        sums=proj.sum(1);err=float(np.max(abs(sums-1)));checks[name+'_complete_unit_projection_sums1']=err<1e-9
        checks[name+'_native_norm_matches_original']=bool(np.allclose(norm,np.load(R/f'forward/documents_{name}.npz')['decoder_norm'][ids],rtol=2e-6,atol=1e-5))
        np.savez_compressed(A/f'{name}_decoder_common_spectrum.npz',feature_ids=ids,squared_projection_per_PC=proj,cumulative_projection=cum,band_squared_projection=band,unit_direction_norm=np.linalg.norm(unit,axis=1),native_norm=norm,uncovered_fraction=1-sums)
        ref=np.load(R/f'forward/reference_{name}.npz')['counts'].sum(0)/65536
        for fi,f in enumerate(ids):
            for b in range(16):row_features.append({'dictionary':name,'feature':int(f),'band':b+1,'PC_start':64*b+1,'PC_end':64*(b+1),'unit_decoder_squared_projection':float(band[fi,b]),'DCLM_rate':float(ref[f]),'groups':'|'.join(g for g,v in orig.items() if f in v)})
        rids=np.load(S/f'analysis/{name}_matched_random_ids.npz');rsummary=json.loads((S/f'analysis/{name}_matched_random_summary.json').read_text());groupout={};nullarrays={}
        ag=np.load(R/f'forward/documents_{name}.npz');secondmom=ag['sum_z2'].astype(float)*ag['decoder_norm'][None,:]**2/160
        for g,flist in orig.items():
            ii=np.array([loc[f] for f in flist]);obs=band[ii].mean(0);nullinfo=rsummary[g]
            out={'feature_count':len(flist),'unit_mean_band_projection':obs,'matching_status':nullinfo['status'],'matched_spectral_status':'NA_INSUFFICIENT_MATCH_POOL'}
            if g in rids.files:
                ri=np.array([[loc[int(f)] for f in rr] for rr in rids[g]]);random=band[ri].mean(1);quant=np.quantile(random,[.025,.5,.975],axis=0);pvals=np.minimum(1,2*np.minimum((1+(random>=obs[None,:]).sum(0))/1001,(1+(random<=obs[None,:]).sum(0))/1001))
                out.update(matched_spectral_status='DONE_EXPLORATORY',random_band_quantiles=quant,band_two_sided_background_p=pvals)
                nullarrays[g]=random
                if g=='new_top16':primary.extend([{'dictionary':name,'band':b+1,'p':float(pvals[b])} for b in range(16)])
            groupout[g]=out
            for b in range(16):
                row={'dictionary':name,'group':g,'band':b+1,'unit_mean_projection':float(obs[b]),'matching_status':out['matched_spectral_status'],'random_low':None,'random_median':None,'random_high':None,'background_p':None}
                if g in rids.files:row.update(random_low=float(quant[0,b]),random_median=float(quant[1,b]),random_high=float(quant[2,b]),background_p=float(pvals[b]))
                row_groups.append(row)
            # Auxiliary uses actual squared activation weights and never normalizes to100%.
            eachdoc=secondmom[:,flist]@band[ii]
            for split,idx in ix.items():
                mi,bi,wm,wb=W[split];avg=eachdoc[idx].mean(0);boots=(wm@eachdoc[mi]+wb@eachdoc[bi])/len(idx);ci=np.quantile(boots,[.025,.975],axis=0)
                for b in range(16):row_aux.append({'dictionary':name,'group':g,'split':split,'band':b+1,'sum_of_individual_feature_squared_contributions':float(avg[b]),'CI_low':float(ci[0,b]),'CI_high':float(ci[1,b]),'includes_cross_terms':False,'is_total_representation_variance':False,'normalized_to_100_percent':False})
        np.savez_compressed(A/f'{name}_matched_random_spectral_bands.npz',**nullarrays)
        np.savez_compressed(A/f'{name}_document_projected_moments.npz',seq_id=np.array([r['seq_id'] for r in docs]),mean=doc_mean,sum=doc_sum,sum_squared=doc_sq,labels=labels,split=splits)
        summary[name]={'hook':C['spaces'][name],'fit_matrix_shape':[9600,1024],'full_eigenbasis_shape':[1024,1024],'rank':rank,'rank_tolerance':ranktol,'minimum_eigenvalue_before_clip':negative,'orthogonality_max_error':checkorth,'eigen_residual_relative':eigres,'projection_sum_max_error':err,'unit_projection_universe':len(ids),'top16_feature_ids':orig['new_top16'],'groups':groupout,'splits':splitout,'native_LayerNorm':'native model post_attention RMSNorm already in MLP input' if name=='SAE' else 'none applied beyond original block computation, before final global norm','additional_standardization':False}
        print('PCA_COMPLETE',name,'rank',rank,'train/head var',float(splitout['discovery']['variance_fraction_by_band'][0]),'held/head mean diff',float(splitout['heldout']['mean_difference_fraction_by_band'][0]),'seconds',round(time.time()-t,1),flush=True)
        del payload,H,coeff,tr,X,cov,native,unit,proj,cum
    assert len(primary)==32
    for z,q in zip(primary,bh([x['p'] for x in primary])):z['BH_q_32_main_comparisons']=float(q)
    for name in ['SAE','CC']:summary[name]['groups']['new_top16']['BH_q_32_main_comparisons']=[x['BH_q_32_main_comparisons'] for x in primary if x['dictionary']==name]
    csvwrite(A/'per_feature_band_projections.csv',row_features);csvwrite(A/'real_variance_and_domain_mean_difference.csv',row_splits);csvwrite(A/'cohort_matched_background.csv',row_groups);csvwrite(A/'activation_weighted_auxiliary.csv',row_aux);csvwrite(A/'primary_matched_background_tests.csv',primary)
    dump(A/'spectral_results.json',{'status':'DONE_TRUE_H_EXPLORATORY','raw_acquisition_forwards':124,'training':0,'classifier_fits':0,'new_clustering':0,'source_amendment':C,'dictionaries':summary,'primary_background_test_family':32,'checks':checks,'checks_pass':all(checks.values()),'elapsed_seconds':time.time()-t,'numpy':np.__version__,'torch':torch.__version__})
    assert all(checks.values()),checks

if __name__=='__main__':main()
