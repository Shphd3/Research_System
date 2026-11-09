"""Independent real-h/direct covariance checks; no new forwards or fits."""
from pathlib import Path
import json,hashlib,csv
import numpy as np
O=Path(__file__).resolve().parent;S=O.parent;R=S.parent;A=O/'analysis'

def main():
    C=json.loads((O/'amendment.json').read_text());J=json.loads((A/'spectral_results.json').read_text());checks={};done=json.loads((O/'completed.json').read_text());ledger=[json.loads(x) for x in (O/'forward_ledger.jsonl').read_text().splitlines()]
    checks['exact124prechargedforwards']=len(ledger)==124==done['charged_forwards'];checks['all124charged_before_attempt']=all(x['charged_before_attempt'] for x in ledger);checks['all120docs_latents_exact']=done['max_original_z_relative_error']==0 and done['min_original_z_support_jaccard']==1
    checks['all_repeat_and_causal_true_h_exact']=all(x['relative_h_error']==0 and x['z']['relative_z_error']==0 for x in done['checks']);checks['buffers_and_parameters_unchanged']=done['buffers_unchanged'] and done['parameters_updated']==0
    checks['selection_freeze_unchanged']=hashlib.sha256((S/'analysis/candidate_freeze.json').read_bytes()).hexdigest()==C['candidate_freeze_sha256']
    docs=[json.loads(x) for x in (R/'data/documents.jsonl').read_text().splitlines()];labels=np.array([x['label'] for x in docs]);split=np.array([x['split'] for x in docs]);train=np.flatnonzero(split=='discovery');held=np.flatnonzero(split=='heldout');bm=np.load(A/'spectral_bootstrap_multiplicities.npz')
    checks['same120source_ids']=set(p.stem for p in (O/'raw_documents').glob('*.npz'))==set(x['seq_id'] for x in docs)
    for name in ['SAE','CC']:
        b=np.load(A/f'{name}_common_basis.npz');V=b['PC_columns'];mu=b['mean'];H=np.stack([np.load(O/'raw_documents'/f"{r['seq_id']}.npz")[name+'_h'][32:192] for r in docs]).astype(float)
        checks[name+'_pooled_discovery_mean_exact']=np.allclose(mu,H[train].mean((0,1)),atol=1e-12)
        checks[name+'_full1024orthogonal']=V.shape==(1024,1024) and np.max(abs(V.T@V-np.eye(1024)))<1e-10
        flat=H[held].reshape(-1,1024);cov=np.cov(flat,rowvar=False);vdiag=np.einsum('ij,ij->j',V,cov@V);frac=vdiag.reshape(16,64).sum(1)/np.trace(cov)
        checks[name+'_held_variance_direct_raw_covariance']=np.allclose(frac,J['dictionaries'][name]['splits']['heldout']['variance_fraction_by_band'],atol=1e-11)
        means=H.mean(1);im=held[labels[held]==1];ib=held[labels[held]==0];delta=means[im].mean(0)-means[ib].mean(0);dsq=(delta@V)**2;dfrac=dsq.reshape(16,64).sum(1)/np.dot(delta,delta)
        checks[name+'_domain_delta_direct_raw_means']=np.allclose(dfrac,J['dictionaries'][name]['splits']['heldout']['mean_difference_fraction_by_band'],atol=1e-11)
        checks[name+'_mean_centering_cancels_delta']=np.allclose((means[im]-mu).mean(0)-(means[ib]-mu).mean(0),delta,atol=1e-10)
        checks[name+'_bootstrap_stratified_doc_sizes']=all((bm[f'{s}_math'].sum(1)==n).all() and (bm[f'{s}_bio'].sum(1)==n).all() for s,n in [('discovery',30),('development',10),('heldout',20)])
        dec=np.load(A/f'{name}_decoder_common_spectrum.npz');sums=dec['squared_projection_per_PC'].sum(1);checks[name+'_full_projection_sum1']=np.max(abs(sums-1))<1e-9;checks[name+'_cumulative_monotone']=bool((np.diff(dec['cumulative_projection'],axis=1)>=-1e-14).all())
        old=np.load(S/f'analysis/{name}_selected_native_decoder.npz');loc={int(f):i for i,f in enumerate(dec['feature_ids'])};take=np.array([loc[int(f)] for f in old['feature_ids']]);direct=(old['unit_native_decoder']@V)**2
        checks[name+'_saved_native_directions_independent_projection']=np.allclose(direct,dec['squared_projection_per_PC'][take],atol=1e-12)
        checks[name+'_rank_bands_all64']=np.allclose(direct.reshape(len(direct),16,64).sum(2),dec['band_squared_projection'][take],atol=1e-12)
        # Direct bootstrap mean-vector resampling from raw document means, not projected moment code.
        arr=[]
        for wm,wb in zip(bm['heldout_math'][:12],bm['heldout_bio'][:12]):
            dm=np.repeat(means[im],wm.astype(int),axis=0).mean(0)-np.repeat(means[ib],wb.astype(int),axis=0).mean(0);pp=(dm@V)**2;arr.append(pp.reshape(16,64).sum(1)/pp.sum())
        checks[name+'_bootstrap_direct_raw_shapes']=np.array(arr).shape==(12,16) and np.allclose(np.sum(arr,axis=1),1,atol=1e-10)
        checks[name+'_rank_record_matches_eigenvalues']=int(b['effective_rank'])==int((b['eigenvalues']>float(b['rank_tolerance'])).sum())
        del H,flat,cov
    rows=list(csv.DictReader((A/'activation_weighted_auxiliary.csv').open(encoding='utf-8-sig')));checks['aux_not_total_variance_or_percent']=all(r['includes_cross_terms']=='False' and r['is_total_representation_variance']=='False' and r['normalized_to_100_percent']=='False' for r in rows)
    # Independently verify the32-test adjustment through the defining minimum over later ordered ranks.
    ts=list(csv.DictReader((A/'primary_matched_background_tests.csv').open(encoding='utf-8-sig')));p=np.array([float(r['p']) for r in ts]);order=np.argsort(p);expected=np.empty(32)
    for i,f in enumerate(order):expected[f]=min(1,min(32*p[j]/(k+1) for k,j in enumerate(order) if k>=i))
    checks['BH32_independent_definition']=np.allclose(expected,[float(r['BH_q_32_main_comparisons']) for r in ts],atol=1e-12)
    # Keep immutable v1 and original R04 assets untouched.
    src=json.loads((S/'source_manifest.json').read_text());checks['original_input_hashes_unchanged']=all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==v['sha256'] for p,v in src.items())
    result={'status':'PASS' if all(checks.values()) else 'FAIL','check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'new_audit_forwards':0,'new_statistical_fits':0,'raw_h_acquisition':124,'PCA_fit':'only60originaldiscoverydocsperhook','mean_difference_bootstrap_warning':'percentile bands summarize conditional resampling dispersion; high-dimensional nonlinear squared-ratio bootstrap is biased and can exclude plug-in point. Not a guaranteed population confidence interval; preserve observed values, no tuning','scientific_acceptance':'Unknown'}
    (O/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');assert all(checks.values()),[k for k,v in checks.items() if not v];print('SPECTRUM_AUDIT_PASS',len(checks))

if __name__=='__main__':main()
