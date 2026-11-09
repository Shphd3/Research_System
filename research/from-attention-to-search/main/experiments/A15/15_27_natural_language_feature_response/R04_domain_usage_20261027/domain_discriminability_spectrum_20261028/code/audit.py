"""Independent cache/provenance and bootstrap/null checks, without model calls."""
from pathlib import Path
import json,csv,hashlib
import numpy as np
from scipy.stats import mannwhitneyu
O=Path(__file__).resolve().parent;A=O/'analysis';R=O.parent

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(8<<20),b''):h.update(b)
    return h.hexdigest()

def main():
    checks={};sources=json.loads((O/'source_manifest.json').read_text())
    for p,m in sources.items():checks['source:'+p]=sha(p)==m['sha256']
    # The original delivery manifest predates this supplement; verify every registered original file.
    old=json.loads((R/'execution_manifest.json').read_text());oldchecks=[]
    for row in old['files']:
        p=R/row['path'];oldchecks.append({'path':row['path'],'pass':p.exists() and sha(p)==row['sha256']})
    checks['original_R04_manifest_all_files_unchanged']=all(x['pass'] for x in oldchecks)
    origzip=R/'delivery/R04_数学生物_原生SAE与CrossCoder_讨论包_v1.zip'
    checks['original_R04_zip_unchanged']=sha(origzip)=='32cf80b18aa742c1130a10305bff7a0ad2820fadf10d7d6dc74fe9c3a661c055'
    freeze=json.loads((A/'candidate_freeze.json').read_text())['dictionaries'];docs=[json.loads(s) for s in (R/'data/documents.jsonl').read_text().splitlines()];te=np.flatnonzero([x['split']=='heldout' for x in docs]);im=np.array([i for i in te if docs[i]['label']==1]);ib=np.array([i for i in te if docs[i]['label']==0]);b=np.load(A/'bootstrap_document_multiplicities.npz');tokenrows=list(csv.DictReader((A/'selected_token_hit_summary.csv').open(encoding='utf-8-sig')))
    for d in ['SAE','CC']:
        a=np.load(R/f'forward/documents_{d}.npz');x=a['sum_z'].astype(float)*a['decoder_norm'][None,:]/160;c=a['counts'];n=x.shape[1];g=freeze[d]['groups'];rs=np.load(A/f'{d}_all_feature_results.npz');dd=np.load(A/f'{d}_discovery_freeze.npz');mp={int(r['feature']):r for r in csv.DictReader((A/f'{d}_selected_feature_metrics.csv').open(encoding='utf-8-sig'))}
        # Recompute direct Mann-Whitney U bootstrap with repeated document values, not pair matrix multiplication.
        for f in g['new_top16'][:2]:
            raw=mannwhitneyu(x[im,f],x[ib,f],alternative='two-sided').statistic/400;val=raw if dd['direction'][f]>0 else 1-raw
            checks[f'{d}_f{f}_independent_MannWhitney']=abs(val-rs['heldout_auc'][f])<1e-12
            boots=[]
            for wm,wb in zip(b['math'],b['bio']):
                mm=np.repeat(x[im,f],wm.astype(int));bb=np.repeat(x[ib,f],wb.astype(int));raw=mannwhitneyu(mm,bb,alternative='two-sided').statistic/400;boots.append(raw if dd['direction'][f]>0 else 1-raw)
            ci=np.quantile(boots,[.025,.975]);checks[f'{d}_f{f}_bootstrap_independent']=np.allclose(ci,[rs['heldout_auc_ci_low'][f],rs['heldout_auc_ci_high'][f]],atol=1e-12)
        valid=np.isfinite(rs['heldout_auc_ci_low']);checks[d+'_CI_in_unit_interval']=bool(((rs['heldout_auc_ci_low'][valid]>=0)&(rs['heldout_auc_ci_high'][valid]<=1)).all())
        checks[d+'_old_lists_preserved']=all(g['old_'+k+('32' if k=='shared' else '16')]==json.loads((R/f'analysis/{d}_candidate_freeze.json').read_text())[k] for k in ['shared','math','bio'])
        order=np.flatnonzero(dd['eligible']&(dd['direction']!=0));order=order[np.lexsort((order,-abs(dd['raw_auc'][order]-.5)))];checks[d+'_top16_exact_discovery_rule']=order[:16].tolist()==g['new_top16']
        for key,sig in [('expanded_math64',1),('expanded_bio64',-1)]:checks[d+'_'+key+'_exact64']=len(g[key])==64 and set(g[key]).issubset(set(order[dd['direction'][order]==sig]))
        checks[d+'_direction_sets_disjoint']=not(set(g['expanded_math64'])&set(g['expanded_bio64']))
        for f,r in mp.items():
            for lab,ix in [('math',im),('bio',ib)]:
                if not (c[ix,f]>0).any():checks[f'{d}_{f}_{lab}_conditional_NA']=r['conditional_'+lab]==''
        tok={(int(r['feature'])):int(r['heldout_total_hits']) for r in tokenrows if r['dictionary']==d};checks[d+'_token_hit_counts_match_aggregate']=all(tok.get(f,0)==int(c[te,f].sum()) for f in mp)
        null=np.load(A/f'{d}_matched_random_ids.npz');summary=json.loads((A/f'{d}_matched_random_summary.json').read_text());ref=np.load(R/f'forward/reference_{d}.npz')['counts'].sum(0);fb=np.floor(np.log2(ref+.5)).astype(int);sb=np.floor((dd['support_math']+dd['support_bio'])/5).astype(int)
        for key,r in summary.items():
            if r['status'].startswith('NA'):
                checks[d+'_'+key+'_NA_not_faked']=key not in null.files and bool(r['shortages']);continue
            sets=null[key];target=np.array(g[key]);pairs=np.c_[fb[target],sb[target]];expected=sorted(map(tuple,pairs))
            checks[d+'_'+key+'_1000_valid_sets']=sets.shape==(1000,len(target)) and all(len(np.unique(row))==len(target) for row in sets)
            checks[d+'_'+key+'_excludes_candidates']=not np.isin(sets,target).any()
            checks[d+'_'+key+'_eligible_background']=bool(dd['eligible'][sets].all())
            checks[d+'_'+key+'_exact_frequency_support_matching']=all(sorted(zip(fb[row],sb[row]))==expected for row in sets)
        dec=np.load(A/f'{d}_selected_native_decoder.npz');checks[d+'_unit_directions']=np.allclose(np.linalg.norm(dec['unit_native_decoder'],axis=1),1,atol=1e-12);checks[d+'_native_norms']=np.allclose(dec['native_norm'],a['decoder_norm'][dec['feature_ids']],rtol=2e-6,atol=1e-5)
    checks['no_fabricated_spectrum_basis']=not any(p.name.startswith(('spectrum_basis','spectrum_projection')) for p in A.glob('*'))
    audit={'status':'PASS' if all(checks.values()) else 'FAIL','checks':{k:bool(v) for k,v in checks.items()},'check_count':len(checks),'original_manifest_file_count':len(oldchecks),'original_manifest_checks':oldchecks,'model_forwards':0,'fits':0,'scientific_acceptance':'Unknown'}
    (O/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n');assert all(checks.values()),[k for k,v in checks.items() if not v];print('AUDIT_PASS',len(checks),'original_manifest_files',len(oldchecks))

if __name__=='__main__':main()
