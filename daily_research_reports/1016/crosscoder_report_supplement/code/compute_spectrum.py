#!/usr/bin/env python3
"""Frozen cached-z contribution covariance spectra. CPU only, no model forward."""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ.setdefault(_k, '4')
import argparse
import csv
import hashlib
import json
import time
from pathlib import Path
from datetime import datetime, timezone
import numpy as np

E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
P=E/'analysis/feature_relation_phase1/20261013T173130Z'
F=E/'analysis/feature_frequency/20261015T143300Z'
R=E/'analysis/report_spectrum/20261016_spectrum'
CK=E/'runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt'

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(8<<20),b''): h.update(b)
    return h.hexdigest()
def dump(p,d):
    Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def log(event,**kw):
    print(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'event':event,**kw}),flush=True)
def writecsv(p,rows):
    with Path(p).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def freeze():
    R.mkdir(parents=True,exist_ok=True)
    if (R/'frozen_config.json').exists(): raise RuntimeError('Already frozen: do not overwrite a pre-outcome receipt')
    rows=list(csv.DictReader((F/'frequency.csv').open()))
    ids=np.array([int(x['feature_id']) for x in rows],np.int64)
    nd=np.array([int(x['n_D']) for x in rows],np.int64)
    pd=np.array([float(x['p_D']) for x in rows],np.float64)
    coverage=np.array([int(x['blocks_D']) for x in rows],np.int64)
    eligible=(nd>=100)&(coverage>=10)&(pd>0)&(pd<1)
    assert np.array_equal(eligible,np.load(F/'candidate_mask.npy'))
    ordered=ids[eligible][np.lexsort((ids[eligible],np.log10(pd[eligible])))]
    assert len(ordered)==15666
    same=ordered.reshape(1119,14).copy();mixed=ordered.reshape(14,1119).T.copy()
    for a in (same,mixed): assert np.array_equal(np.sort(a.ravel()),np.sort(ordered))
    split=json.loads((P/'split_manifest.json').read_text()); vb=[b for b in split['blocks'] if b['side']=='V']
    n=131072;nv=sum(b['N'] for b in vb); assert nv==5247663
    vindex=((2*np.arange(n,dtype=np.int64)+1)*nv)//(2*n)
    ends=np.cumsum([b['N'] for b in vb]);which=np.searchsorted(ends,vindex,side='right')
    start=np.r_[0,ends[:-1]]
    pos=np.array([vb[k]['position_begin'] for k in which],np.int64)+(vindex-start[which])
    assert len(np.unique(pos))==n and len(np.unique(which))==41
    np.save(R/'feature_pool_ordered.npy',ordered)
    np.save(R/'same_frequency_members.npy',same);np.save(R/'mixed_frequency_members.npy',mixed)
    np.save(R/'V_global_position_ids.npy',pos);np.save(R/'V_stream_position_ids.npy',vindex)
    means=[];members=[]
    for label,a in [('same_frequency',same),('mixed_frequency',mixed)]:
        for g,ii in enumerate(a):
            lp=np.log10(pd[ii]);means.append({'rule':label,'group_id':g,'m':14,'mean_p_D':float(pd[ii].mean()),'mean_log10_p_D':float(lp.mean()),'std_log10_p_D_ddof0':float(lp.std()),'sum_D_column_hits':int(nd[ii].sum()),'min_D_column_hits':int(nd[ii].min())})
            for k,i in enumerate(ii):members.append({'rule':label,'group_id':g,'member_slot':k,'feature_id':int(i),'n_D':int(nd[i]),'p_D':float(pd[i]),'D_blocks':int(coverage[i])})
    writecsv(R/'grouping_members.csv',members);writecsv(R/'grouping_D_frequency.csv',means)
    files=['feature_pool_ordered.npy','same_frequency_members.npy','mixed_frequency_members.npy','V_global_position_ids.npy','V_stream_position_ids.npy','grouping_members.csv','grouping_D_frequency.csv']
    config={'schema':'fixed_group_contribution_representation_spectrum_v1','frozen_utc':datetime.now(timezone.utc).isoformat(),'processing_agent':'Codex /root/spectrum_data','pre_outcome_statement':'No representation covariance spectrum or first-direction endpoint has been computed or inspected before this freeze. Only D frequency/support, cache schemas and checkpoint decoder/normalization metadata were inspected.','root_authorization':'Root user-authorized bounded descriptive analysis; root froze definitions in collaboration message before this receipt.','m':14,'groups_per_rule':1119,'pool_size':15666,'pool_rule':'Existing D hits>=100, D-block coverage>=10, 0<p_D<1; every feature exactly once per rule.','m_rationale':'Largest divisor of15666 not exceeding16; all candidate features retained. D summed column hits per group>=1400; neither unique position count nor independent signal guarantee; no optimality claim.','same_rule':'Ascending(log10p_D,feature_id).reshape(1119,14)','mixed_rule':'Same ordered feature IDs reshape(14,1119).T; one member from each of14 equal-count D-frequency bands.','sample_N':n,'full_N_V':nv,'V_blocks':41,'positions_rule':'floor((j+0.5)*N_V/N) in concatenated V eligible positions; map to original global eligible IDs; no activation-dependent selection','layer_model_one_based':28,'layer_model_zero_based':27,'source_index_zero_based':13,'layer_object':'residual-post before final RMSNorm','model_coordinate_direction':'d_i = saved TRAIN_centered_vector_L2_RMS[13] * saved decoder[13,i,:]; never unit-normalize.','h_G':'sum_i cached_z_i(t) d_i; no per-group decoder bias or TRAIN mean','center':'Position mean over exactly the same fixed N V rows including zeros, ddof1 covariance','statistic':'Nonzero eigenvalues of group-contribution representation covariance, not parameter spectrum or capacity','shuffle_replicates':1,'shuffle_seed':20261016,'shuffle_rule':'Independent uniform permutation of all N positions for every feature column; exact original value multiset including zeros; one shared randomized matrix for both rules.','zero_variance_rule':'NA first-direction share; count and report, never recode0; no post-outcome support deletion','inference_boundary':'Fixed model/rules/V-position set descriptive comparison, composite grouping rules not frequency-only causation. One statistical permutation no p values. Not model-input intervention or evidence of learning benefit.','files':{x:{'sha256':sha(R/x),'bytes':(R/x).stat().st_size} for x in files},'input_files':{str(p):sha(p) for p in [F/'frequency.csv',F/'candidate_mask.npy',P/'split_manifest.json',P/'feature_cache/manifest.json']},'checkpoint_sha256':'09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628','proposal_seed_note':'Proposal seed2026101603 superseded before outcomes by explicit root freeze seed20261016.'}
    dump(R/'frozen_config.json',config)
    log('freeze_complete',config_sha256=sha(R/'frozen_config.json'),sample_N=n,pool=len(ordered),groups=1119)

def extract():
    cfg=json.loads((R/'frozen_config.json').read_text());n=cfg['sample_N'];pool=np.load(R/'feature_pool_ordered.npy');pos=np.load(R/'V_global_position_ids.npy')
    lookup=np.full(16384,-1,np.int32);lookup[pool]=np.arange(len(pool))
    z=np.lib.format.open_memmap(R/'sample_z_feature_major.npy',mode='w+',dtype=np.float32,shape=(len(pool),n));z[:]=0
    chunks=[]
    for rank in range(4):chunks+=json.loads((P/f'feature_cache/rank{rank}/manifest.json').read_text())['chunks']
    chunks.sort(key=lambda x:x['start']);trace=[];count=0;tick=time.monotonic()
    for ci,m in enumerate(chunks):
        lo,hi=np.searchsorted(pos,[m['start'],m['end']])
        if lo==hi:continue
        path=Path(m['file']);assert path.stat().st_size==m['bytes'];h=sha(path);assert h==m['sha256']
        with np.load(path) as cache:
            ptr=cache['ptr'];ids=cache['ids'];values=cache['z']
            assert len(ptr)==m['end']-m['start']+1 and int(ptr[-1])==len(ids)==len(values)
            local=pos[lo:hi]-m['start']
            for j,row in enumerate(local,start=lo):
                a,b=int(ptr[row]),int(ptr[row+1]);features=lookup[ids[a:b]];keep=features>=0
                z[features[keep],j]=values[a:b][keep]
            count+=hi-lo
        trace.append({'path':str(path),'sha256':h,'selected_rows':int(hi-lo)})
        if len(trace)%40==0:log('cache_extract_progress',chunks=len(trace),rows=int(count),seconds=time.monotonic()-tick)
    assert count==n
    z.flush();del z
    dump(R/'sample_cache_receipt.json',{'status':'COMPLETE','sample_N':n,'pool_size':len(pool),'source_chunks':trace,'source_chunk_hashes_verified':True,'sample_z_path':str(R/'sample_z_feature_major.npy'),'sample_z_sha256':sha(R/'sample_z_feature_major.npy'),'seconds':time.monotonic()-tick,'new_model_forwards':0,'training_updates':0})
    log('cache_extract_complete',rows=int(count),seconds=time.monotonic()-tick)

def shuffle_columns():
    cfg=json.loads((R/'frozen_config.json').read_text());a=np.load(R/'sample_z_feature_major.npy',mmap_mode='r')
    b=np.lib.format.open_memmap(R/'shuffled_z_feature_major.npy',mode='w+',dtype=np.float32,shape=a.shape)
    tick=time.monotonic();rng=np.random.default_rng(cfg['shuffle_seed']);n=a.shape[1]
    max_sum_diff=0.;checks=0
    for i in range(len(a)):
        perm=rng.permutation(n);b[i]=a[i,perm]
        # A genuine permutation vector proves exact value-multiset preservation; verify each mapping and bijection.
        assert np.all(np.bincount(perm,minlength=n)==1)
        assert np.array_equal(b[i],a[i,perm])
        checks+=1
        if i%2000==0:log('column_shuffle_progress',features=i,seconds=time.monotonic()-tick)
    b.flush();del b
    dump(R/'shuffle_receipt.json',{'status':'COMPLETE','seed':cfg['shuffle_seed'],'replicates':1,'columns':checks,'positions_per_column':n,'all_permutations_bijective':True,'all_reordered_values_exact':True,'sample_z_sha256':sha(R/'sample_z_feature_major.npy'),'shuffled_z_sha256':sha(R/'shuffled_z_feature_major.npy'),'shared_between_rules':True,'seconds':time.monotonic()-tick,'inferential_p_values':None})

def psd_eigen(a):
    a=(a+a.T)*.5;w,v=np.linalg.eigh(a);scale=max(np.max(np.abs(w)),np.finfo(float).tiny)
    if np.min(w)<-1e-9*scale:raise ArithmeticError(('PSD failure',float(np.min(w)),float(scale)))
    return np.clip(w,0,None),v,float(np.min(w))

def one_spectrum(a,d):
    n=a.shape[0];mean=a.mean(0);centered=a-mean
    c=(centered.T@centered)/(n-1);c=(c+c.T)*.5
    wc,_,cmin=psd_eigen(c)
    gram=d@d.T;wg,vg,gmin=psd_eigen(gram);root=(vg*np.sqrt(wg))@vg.T
    trace=float(np.trace(c@gram))
    if trace==0:
        # Exact zero covariance or exact decoder cancellation must not acquire
        # an artificial relative-PSD failure from a square-root roundoff residue.
        direct_sum=0.
        for start in range(0,n,8192):direct_sum+=float(np.square(centered[start:start+8192]@d).sum())
        if direct_sum!=0:raise ArithmeticError('Zero Gram trace conflicts with explicit positive representation variance')
        w=np.zeros(len(c));share=np.full(len(c),np.nan)
        return w,share,{'trace':0.,'total_variance':0.,'Cz_min_raw_eig':cmin,'Gram_min_raw_eig':gmin,'small_min_raw_eig':0.},c
    small=root@c@root;w,_,smin=psd_eigen(small);w=w[::-1]
    total=float(w.sum())
    assert np.isclose(total,trace,rtol=1e-8,atol=1e-12)
    share=w/total if total>0 else np.full(len(w),np.nan)
    return w,share,{'trace':trace,'total_variance':total,'Cz_min_raw_eig':cmin,'Gram_min_raw_eig':gmin,'small_min_raw_eig':smin},c

def direct_audit(z,d,group_pool_ids):
    rows=[]
    for k,idx in enumerate(group_pool_ids):
        # Every fixed V sample position is used, independent of activation; direct h formed explicitly.
        a=np.asarray(z[idx,:512].T,dtype=np.float64);dd=d[idx];ac=a-a.mean(0);h=ac@dd
        expected=(np.linalg.svd(h,compute_uv=False)**2/511)[:14]
        w,s,diagn,c=one_spectrum(a,dd)
        scale=max(float(w.max()),1e-30);err=float(np.max(np.abs(expected-w))/scale)
        assert err<1e-8
        # Model-coordinate scale and normalized-coordinate spectra must agree after r^2 rescaling.
        r=374.3495121024576;wn,_,_,_=one_spectrum(a,dd/r)
        scaleerr=float(np.max(np.abs(wn*r*r-w))/scale);assert scaleerr<1e-8
        rows.append({'fixed_check_index':k,'positions':512,'explicit_h_shape':list(h.shape),'SVD_vs_small_Gram_max_relative_error':err,'raw_scale_r_squared_relative_error':scaleerr,'direct_centered_h_trace':float(np.square(h).sum()/511),'small_trace':diagn['total_variance']})
    # Exact simple cases: orthogonal equal coefficient variance and perfectly aligned decoder.
    a=np.array([[1.,0],[-1.,0],[0,1.],[0,-1.]])
    w,s,_,_=one_spectrum(a,np.eye(2));assert np.allclose(s,[.5,.5])
    w,s,_,_=one_spectrum(a,np.array([[1.,0],[1.,0]]));assert np.allclose(s,[1.,0])
    return {'status':'PASS','direct_explicit_h_SVD_checks':rows,'synthetic_orthogonal_shares':[.5,.5],'synthetic_collinear_shares':[1.,0],'all_eigendecompositions_FP64':True}

def compute(original_values=None,shuffled_values=None):
    import torch
    tick=time.monotonic();torch.set_num_threads(4)
    cfg=json.loads((R/'frozen_config.json').read_text());pool=np.load(R/'feature_pool_ordered.npy');lookup=np.full(16384,-1,np.int32);lookup[pool]=np.arange(len(pool))
    payload=torch.load(CK,map_location='cpu',mmap=True,weights_only=False)
    norm=payload['normalization'];assert norm['schema']=='crosscoder_train_centered_vector_rms_a18' and norm['centering'] is True and norm['rms_definition']=='vector_L2_RMS'
    r=float(norm['rms'][13]);assert r==374.3495121024576
    decoder=np.asarray(payload['crosscoder']['decoder'][13].numpy(),np.float64)[pool]*r
    np.save(R/'last_source_model_coordinate_decoder_pool.npy',decoder)
    del payload
    assignments={label:lookup[np.load(R/file)] for label,file in [('same_frequency','same_frequency_members.npy'),('mixed_frequency','mixed_frequency_members.npy')]}
    z=original_values if original_values is not None else np.load(R/'sample_z_feature_major.npy',mmap_mode='r')
    audit_groups=np.array([assignments['same_frequency'][0],assignments['same_frequency'][559],assignments['same_frequency'][1118],assignments['mixed_frequency'][0],assignments['mixed_frequency'][559],assignments['mixed_frequency'][1118]])
    dump(R/'numerical_qualification.json',direct_audit(z,decoder,audit_groups))
    freqs=list(csv.DictReader((R/'grouping_D_frequency.csv').open()));freqmap={(x['rule'],int(x['group_id'])):x for x in freqs}
    result={};metrics=[];supportrows=[];all_min=[]
    for state,file in [('original','sample_z_feature_major.npy'),('column_shuffled','shuffled_z_feature_major.npy')]:
        values=(original_values if state=='original' else shuffled_values)
        if values is None:values=np.load(R/file,mmap_mode='r')
        # No feature is removed if support is low or zero.
        hit=np.count_nonzero(values,axis=1)
        for rule,groups in assignments.items():
            spectra=[];shares=[]
            for g,idx in enumerate(groups):
                a=np.asarray(values[idx].T,dtype=np.float64)
                w,s,diag,c=one_spectrum(a,decoder[idx]);spectra.append(w);shares.append(s)
                fr=freqmap[rule,g];union=int(np.count_nonzero(np.any(a>0,axis=1)))
                metrics.append({'state':state,'rule':rule,'group_id':g,'members':14,'N_positions':cfg['sample_N'],'union_hit_positions':union,'sum_column_hits':int(hit[idx].sum()),'min_member_hits':int(hit[idx].min()),'max_member_hits':int(hit[idx].max()),'zero_hit_members':int((hit[idx]==0).sum()),'total_variance':diag['total_variance'],'first_direction_share':float(s[0]) if diag['total_variance']>0 else 'NA', 'estimable':bool(diag['total_variance']>0),'mean_p_D':fr['mean_p_D'],'mean_log10_p_D':fr['mean_log10_p_D'],'within_std_log10_p_D':fr['std_log10_p_D_ddof0']})
                for slot,i in enumerate(idx):supportrows.append({'state':state,'rule':rule,'group_id':g,'member_slot':slot,'feature_id':int(pool[i]),'V_sample_hits':int(hit[i]),'V_sample_frequency':float(hit[i]/cfg['sample_N'])})
                all_min.append(diag)
                if g%250==0:log('spectrum_progress',state=state,rule=rule,groups=g,seconds=time.monotonic()-tick)
            spectra=np.array(spectra);shares=np.array(shares);valid=np.isfinite(shares).all(1)
            np.savez(R/f'{state}_{rule}_spectra.npz',eigenvalues=spectra,variance_shares=shares,estimable=valid,member_feature_ids=pool[groups])
            first=shares[valid,0];fmean=np.array([float(freqmap[rule,g]['mean_p_D']) for g in range(len(groups))]);flog=np.array([float(freqmap[rule,g]['mean_log10_p_D']) for g in range(len(groups))]);within=np.array([float(freqmap[rule,g]['std_log10_p_D_ddof0']) for g in range(len(groups))])
            quant=lambda x:{k:float(v) for k,v in zip(['min','p10','p25','median','p75','p90','max'],np.quantile(x,[0,.1,.25,.5,.75,.9,1]))}
            result[state,rule]={'groups':len(groups),'estimable_groups':int(valid.sum()),'zero_variance_groups':int((~valid).sum()),'mean_normalized_spectrum':shares[valid].mean(0).tolist(),'first_direction_mean':float(first.mean()),'first_direction_distribution':quant(first),'mean_p_D_distribution':quant(fmean),'mean_log10_p_D_distribution':quant(flog),'within_group_log10p_D_std_distribution':quant(within),'mean_p_D_mean':float(fmean.mean()),'mean_log10_p_D_mean':float(flog.mean()),'within_group_log10p_D_std_mean':float(within.mean())}
    writecsv(R/'per_group_spectrum_metrics.csv',metrics);writecsv(R/'per_feature_sample_support.csv',supportrows)
    simple={f'{state}/{rule}':value for (state,rule),value in result.items()}
    original=result['original','same_frequency']['first_direction_mean']-result['original','mixed_frequency']['first_direction_mean']
    shuffled=result['column_shuffled','same_frequency']['first_direction_mean']-result['column_shuffled','mixed_frequency']['first_direction_mean']
    out={'status':'COMPLETE','config_sha256':sha(R/'frozen_config.json'),'processing_agent':'Codex /root/spectrum_data','N_positions':cfg['sample_N'],'m':14,'groups_per_rule':1119,'model_layer_one_based':28,'source_index_zero_based':13,'rms_model_scale':r,'rank_max':14,'remaining_hidden_eigenvalues_exact_zero':1010,'results':simple,'original_mean_first_share_same_minus_mixed':original,'shuffled_mean_first_share_same_minus_mixed':shuffled,'descriptive_shuffle_change_in_difference':shuffled-original,'no_nominal_p_values':True,'overall_seconds_compute_only':time.monotonic()-tick,'new_training_updates':0,'new_model_forwards':0,'covariance_ddof':1,'numerical_min_eigenvalues':{key:min(x[key] for x in all_min) for key in ['Cz_min_raw_eig','Gram_min_raw_eig','small_min_raw_eig']},'claim_boundary':cfg['inference_boundary']}
    dump(R/'spectrum_summary.json',out);log('complete',seconds=time.monotonic()-tick,same_minus_mixed=original,shuffle_same_minus_mixed=shuffled)

def run_memory():
    """Same frozen randomization, no redundant8GB shuffled temporary on network FS."""
    tick=time.monotonic();cfg=json.loads((R/'frozen_config.json').read_text())
    before={'utc':datetime.now(timezone.utc).isoformat(),'script_sha256':sha(__file__),'frozen_config_sha256':sha(R/'frozen_config.json'),'storage_only_adjustment':'Original sampled matrix is persistent. Independent column permutations generated once in RAM, shared by both rules; large randomized matrix not persisted. Seed, exact checks and raw value digest retained. All spectra/metrics/plot data persisted.','spectrum_outcomes_previously_inspected':False}
    dump(R/'pre_compute_source_receipt.json',before)
    log('load_sample_to_RAM')
    a=np.load(R/'sample_z_feature_major.npy');b=np.empty_like(a);rng=np.random.default_rng(cfg['shuffle_seed']);n=a.shape[1]
    log('sample_loaded_to_RAM',seconds=time.monotonic()-tick)
    for i in range(len(a)):
        perm=rng.permutation(n);b[i]=a[i,perm]
        assert np.all(np.bincount(perm,minlength=n)==1)
        assert np.array_equal(b[i],a[i,perm])
        if i%2000==0:log('RAM_column_shuffle_progress',features=i,seconds=time.monotonic()-tick)
    h=hashlib.sha256();h.update(memoryview(b).cast('B'))
    source=json.loads((R/'sample_cache_receipt.json').read_text())
    dump(R/'shuffle_receipt.json',{'status':'COMPLETE','seed':cfg['shuffle_seed'],'replicates':1,'columns':len(a),'positions_per_column':n,'all_permutations_bijective':True,'all_reordered_values_exact':True,'sample_z_sha256':source['sample_z_sha256'],'shuffled_raw_C_order_FP32_value_sha256':h.hexdigest(),'shared_between_rules':True,'seconds':time.monotonic()-tick,'inferential_p_values':None,'large_shuffled_matrix_retained':False,'regeneration':'Read saved sample_z_feature_major.npy in C-order; for each ordered pool feature i in sequence, rng=np.random.default_rng(seed); b[i]=a[i,rng.permutation(N)] (one shared rng stream). All definition/data hashes frozen.'})
    compute(original_values=a,shuffled_values=b)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['freeze','extract','shuffle','compute','all','run-memory']);args=ap.parse_args()
    if args.stage=='run-memory':run_memory();raise SystemExit(0)
    for stage,fn in [('freeze',freeze),('extract',extract),('shuffle',shuffle_columns),('compute',compute)]:
        if args.stage in ('all',stage):fn()
