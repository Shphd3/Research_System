#!/usr/bin/env python3
"""Existing R/F/N winning-group inputs: cached raw hidden spectra, no training.

Support mode imports the original scorer and reads only event/route metadata.
The186-way group winner is distinct from its downstream4-way expert mapping.
Spectrum mode requires a frozen definition written before hidden inspection.
"""
import argparse
import csv
import datetime as dt
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import torch

E = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
OUT = E / 'analysis/report_spectrum/20261016_phi_input_spectrum'
DATA = E / 'analysis/relation_learning/20261015T164000Z/data_eval512'
CACHE = DATA / 'eval.pt'
MAPS = DATA / 'route_maps.npz'
SCORER = E / 'analysis_tools/relation_learning/data_routes.py'
RULES = ('R', 'F', 'N')

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n')

def load_scorer():
    s = importlib.util.spec_from_file_location('frozen_existing_data_routes', SCORER)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m

def support():
    OUT.mkdir(parents=True, exist_ok=True)
    m = load_scorer()
    maps = np.load(MAPS)
    cache = torch.load(CACHE, map_location='cpu', mmap=True, weights_only=False)
    ptr = cache['feature_ptr'].numpy(); ids = cache['feature_ids'].numpy()
    pos = cache['position_id'].numpy(); ctx = cache['block_id'].numpy()
    positions = len(ptr)-1; G = len(maps['sizes'])
    summary = dict(status='SUPPORT_ONLY_NO_HIDDEN_VALUES_READ', created_utc=now(),
                   processing_agent='Codex /root/raw_hidden_spectrum',
                   scorer_source=str(SCORER), scorer_sha256=sha(SCORER),
                   maps=str(MAPS), maps_sha256=sha(MAPS),
                   cache=str(CACHE), cache_sha256_from_existing_manifest=json.loads((DATA/'eval_manifest.json').read_text())['sha256'],
                   cache_hidden_schema=dict(shape=list(cache['hidden'].shape), dtype=str(cache['hidden'].dtype)),
                   source_positions=positions, source_contexts=len(np.unique(ctx)),
                   group_count=G, feature_pool=len(maps['pool']),
                   score='Exactly imported original scores_and_winner(ptr,ids,labels,sizes,means,stds,tie_order); binary member fraction standardized by frozen D mean/std, std0score0; nohitgroups -inf; member-content SHA tie order; nohitgroupwinner -1',
                   group_vs_expert='groupwinner has186 possible nonnegative values; cached routes has4 experts via frozen mapping with no-hit fallback. Fallback does not identify a winning group.',
                   conditions={})
    rows = []; all_win = {}
    for c in RULES:
        labels = maps['labels_'+c]
        assert np.array_equal(np.flatnonzero(labels>=0), maps['pool'])
        assert np.array_equal(np.bincount(labels[labels>=0], minlength=G), maps['sizes'])
        winner = np.empty(positions, dtype=np.int32)
        mismatches = 0
        for begin in range(0, positions, 4096):
            end = min(begin+4096, positions)
            p = ptr[begin:end+1]-ptr[begin]
            win, _, _ = m.scores_and_winner(p, ids[ptr[begin]:ptr[end]], labels,
                    maps['sizes'], maps['means_'+c], maps['stds_'+c], maps['tie_order_'+c])
            winner[begin:end] = win
            original_experts = m.apply_routes(win, maps['mapping_'+c], pos[begin:end])
            mismatches += int(np.count_nonzero(original_experts != cache['routes'][c][begin:end].numpy()))
        assert mismatches == 0, 'Reconstructed scoring differs from actual cached learning routes'
        counts = np.bincount(winner[winner>=0], minlength=G)
        all_win[c] = winner
        summary['conditions'][c] = dict(
            nohit_positions=int(np.count_nonzero(winner<0)),
            cached_four_expert_mismatches=mismatches,
            zero_winner_groups=int(np.count_nonzero(counts==0)),
            available_winner_positions_quantiles={str(q):float(np.quantile(counts,q)) for q in (0,.05,.25,.5,.75,.95,1)},
            sufficient_groups={str(N):int(np.count_nonzero(counts>=N)) for N in (16,32,64,128,256,512)},
            winner_counts=counts.tolist())
        for g,n in enumerate(counts):
            ii=np.flatnonzero(winner==g)
            rows.append(dict(condition=c,group_id=g,group_size=int(maps['sizes'][g]),
                             available_winner_positions=int(n),available_contexts=len(np.unique(ctx[ii])),
                             frozen_D_winner_positions=int(maps['discovery_winner_counts_'+c][g]),
                             expert_id=int(maps['mapping_'+c][g]),
                             nohiddenvalue_read=True))
        print(c, summary['conditions'][c]['sufficient_groups'], flush=True)
    for N in (16,32,64,128,256,512):
        counts={c:np.array(summary['conditions'][c]['winner_counts']) for c in RULES}
        summary.setdefault('common_support',{})[str(N)] = dict(
            RN_group_ids=np.flatnonzero((counts['R']>=N)&(counts['N']>=N)).tolist(),
            RFN_group_ids=np.flatnonzero(np.logical_and.reduce([counts[c]>=N for c in RULES])).tolist())
    np.savez_compressed(OUT/'winning_group_labels.npz', **all_win,
                        absolute_position_id=pos,context_id=ctx,sizes=maps['sizes'],pool=maps['pool'])
    with open(OUT/'per_group_winner_support.csv','w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summary['outputs']={name:dict(bytes=(OUT/name).stat().st_size,sha256=sha(OUT/name))
                        for name in ('winning_group_labels.npz','per_group_winner_support.csv')}
    write_json(OUT/'support_only_summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

def independent_winner(ids, labels, sizes, means, stds, tie_order):
    """Small scalar reference, deliberately independent of scipy group counts."""
    counts = [0] * len(sizes)
    for f in ids:
        g = int(labels[int(f)])
        if g >= 0: counts[g] += 1
    winner = -1; best = -np.inf
    for g0 in tie_order:
        g = int(g0)
        if counts[g] == 0: continue
        score = (counts[g]/int(sizes[g])-float(means[g]))/float(stds[g]) if stds[g]>0 else 0.
        if score > best: winner = g; best = score
    return winner, counts, best

def qualify():
    m = load_scorer(); maps = np.load(MAPS)
    cache = torch.load(CACHE,map_location='cpu',mmap=True,weights_only=False)
    win = np.load(OUT/'winning_group_labels.npz')
    ptr=cache['feature_ptr'].numpy(); ids=cache['feature_ids'].numpy()
    rr=np.unique(np.r_[np.linspace(0,len(ptr)-2,32,dtype=np.int64),np.argmax(np.diff(ptr))])
    actual=[]
    for c in RULES:
        labels=maps['labels_'+c]
        for r0 in rr:
            r=int(r0)
            expected,counts,score=independent_winner(ids[ptr[r]:ptr[r+1]],labels,maps['sizes'],
                        maps['means_'+c],maps['stds_'+c],maps['tie_order_'+c])
            assert expected==int(win[c][r])
            actual.append(dict(condition=c,cache_row=r,expected_group_winner=expected,
                               saved_group_winner=int(win[c][r]),maximum_active_member_count=max(counts),
                               winning_score=float(score) if np.isfinite(score) else None))
    synthetic=[]
    tests=[
        ('negative_winner',np.array([0,2],np.int32),np.array([0,0,1,1,-1],np.int32),
         np.array([2,2]),np.array([.9,.8]),np.array([.1,.1]),np.array([0,1]),1),
        ('zero_std',np.array([0,2],np.int32),np.array([0,0,1,1,-1],np.int32),
         np.array([2,2]),np.array([.9,.9]),np.array([0.,1.]),np.array([0,1]),0),
        ('tie_order',np.array([0,2],np.int32),np.array([0,0,1,1,-1],np.int32),
         np.array([2,2]),np.array([0.,0.]),np.array([1.,1.]),np.array([1,0]),1),
        ('nohit',np.array([4],np.int32),np.array([0,0,1,1,-1],np.int32),
         np.array([2,2]),np.array([0.,0.]),np.array([1.,1.]),np.array([0,1]),-1),
        ('count_above255',np.r_[np.arange(300),400,401].astype(np.int32),
         np.r_[np.zeros(400,np.int32),np.ones(10,np.int32)],np.array([400,10]),
         np.array([0.,0.]),np.array([1.,1.]),np.array([0,1]),0)]
    for name, ii, ll, ss, mm, sd, tt, expected in tests:
        actual_w,_,cc=m.scores_and_winner(np.array([0,len(ii)]),ii,ll,ss,mm,sd,tt)
        reference,counts,score=independent_winner(ii,ll,ss,mm,sd,tt)
        assert expected==reference==int(actual_w[0])
        assert np.array_equal(cc[0],counts)
        synthetic.append(dict(name=name,expected=expected,actual=int(actual_w[0]),
                              counts=counts,count_dtype=str(cc.dtype),
                              score=float(score) if np.isfinite(score) else None))
    result=dict(status='PASS',created_utc=now(),actual_reference_positions_per_condition=len(rr),
                actual_reference_rows=actual,synthetic_cases=synthetic,
                original_scorer_sha256=sha(SCORER),
                source_group_winner_and_cached_expert_routes='Both independently checked; exact4expert agreement alone would not establish186groupwinner identity')
    write_json(OUT/'group_winner_qualification.json',result)
    print('WINNER_QUALIFICATION_PASS',len(actual))

def freeze():
    p=OUT/'frozen_config.json'
    if p.exists():raise FileExistsError('Never overwrite a frozen analysis definition')
    support=json.loads((OUT/'support_only_summary.json').read_text())
    assert json.loads((OUT/'group_winner_qualification.json').read_text())['status']=='PASS'
    N=128
    main=support['common_support'][str(N)]['RFN_group_ids']
    rn=support['common_support'][str(N)]['RN_group_ids']
    cfg=dict(schema='original_phi_group_winner_raw_input_covariance_spectrum_v1',
             frozen_utc=now(),processing_agent='Codex /root/raw_hidden_spectrum',
             authority='Root explicit instruction freezes N128 and commonRFN support population145 before this winning-group covariance analysis; RN161 supplementary',
             pre_outcome_boundary='No186-group-winning-input original/residual spectrum computed or inspected before this freeze. Earlier14-feature any-hit input spectra are known but do not define these group assignments or support selection.',
             cache=str(CACHE),cache_sha256=support['cache_sha256_from_existing_manifest'],
             source='Existing learning EVAL cache, original CrossCoder TRAIN bin local-shard_2_of_10_shard_00000247_processed.bin;512contexts523136positions; not original structureV',
             document_independence='UNKNOWN',layer_model_one_based=28,layer_model_zero_based=27,
             hidden_object='Original BF16 block28 residual-post before final RMSNorm; FP64 center/covariance; no reconstruction/decoder/parameter matrix',
             labels='R original186 nonsingleton phi communities; F original frequency-sorted same-pool size-matched groups; N original within10 D-frequency-bin randomized labels preservingR per-group bin composition; not earlierm14same/mixedscheme',
             feature_pool=13807,groups_per_condition=186,group_sizes='Frozen sizes[g], identical R/F/N by groupID;2–735, no regrouping',
             scorer='Reuse unmodified original data_routes.scores_and_winner with all saved means/stds/tie_order. Winner is186-way group, not4-way mapped expert. No-hit winner−1 excluded and counted, no fallbackgroup.',
             sample_N_per_group=N,sampling_seed=20261016,
             sampling='Fixed SHA256(sorted member IDs int64 little-endian+seed) content key; SplitMix64(key XOR absolutepositionID) pseudorandom priority; select lowest128 without replacement, tie by absolutepositionID; no hidden values used',
             support='Any group with fewer128 winning positions remainsNA; no replacement, no loweringN, no changed routing. Percondition allsufficient and RN common coverage supplements retain allsupport facts.',
             main_support_group_ids=main,RN_support_group_ids=rn,
             main_population='Same groupIDs supporting>=128 in allR/F/N, then common original and residual estimability; no selection by endpointdirection. If zero variance, retainNA and report removalfromestimablecurve.',
             center='Subtract pergroup sampled128-position mean for each original hidden coordinate',
             original_covariance='Hc.T@Hc/127; exactnonzero eigenvalues via128rowGram, stored paddedto1024',
             PC1_removal='Estimate eachgroup own PC1fromitscentered128rows; Hres=Hc−(Hc@v1)v1.T; newcovariance Hres.T@Hres/127. This is in-sample descriptive projection, not model input intervention, not commonPCacrossgroups.',
             residual_normalization='Normalize eachresidual eigenvalue by itsremainingtrace; record originaltrace, removedtrace, residualtrace separately. Residualfirstshare isoriginalsecond eigenvalue dividedbytrace−originalfirst eigenvalue.',
             zero_variance='Originaltrace exact0→NA; residualtrace<=1e−12*originaltrace→NA asnumericallyzero (prefrozen tolerance); neverreplaceNAby0firstshare',
             theoretical_rank_original=127,theoretical_rank_residual=126,
             strata=dict(small='size2–3',medium='size4–19',large='size>=20'),
             inference='Descriptive distribution of inputs selectedbyfixed R/F/N winning rules. Contexts/positions may differ and shared positions aredependent; grouping/composition/meanfrequency arecomposite factors; no pvalues/populationCI/frequencycausation/capacity/learning claim.',
             files={str(SCORER):sha(SCORER),str(MAPS):sha(MAPS),
                    str(OUT/'winning_group_labels.npz'):sha(OUT/'winning_group_labels.npz'),
                    str(OUT/'support_only_summary.json'):sha(OUT/'support_only_summary.json'),
                    str(OUT/'group_winner_qualification.json'):sha(OUT/'group_winner_qualification.json')},
             script_sha256=sha(__file__))
    write_json(p,cfg);print('FROZEN',p,'MAIN',len(main),'RN',len(rn))

def splitmix64(x):
    with np.errstate(over='ignore'):
        x=x+np.uint64(0x9E3779B97F4A7C15)
        x=(x^(x>>np.uint64(30)))*np.uint64(0xBF58476D1CE4E5B9)
        x=(x^(x>>np.uint64(27)))*np.uint64(0x94D049BB133111EB)
        return x^(x>>np.uint64(31))

def select_positions(available,members,absolute,N,seed):
    payload=np.sort(members).astype('<i8').tobytes()+int(seed).to_bytes(8,'little')
    key=np.uint64(int.from_bytes(hashlib.sha256(payload).digest()[:8],'little'))
    priority=splitmix64(absolute[available].astype(np.uint64)^key)
    choice=np.argpartition(priority,N-1)[:N]; boundary=priority[choice].max()
    choice=np.flatnonzero(priority<=boundary)
    order=np.lexsort((absolute[available[choice]],priority[choice]))[:N]
    return np.sort(available[choice[order]])

def get_spectrum(Hc):
    gram=Hc@Hc.T/(len(Hc)-1)
    values,vectors=np.linalg.eigh(gram)
    values=values[::-1];vectors=vectors[:,::-1]
    trace=float(np.square(Hc).sum()/(len(Hc)-1))
    assert values.min()>=-max(1.,trace)*1e-10
    assert abs(values.sum()-trace)<=max(1.,trace)*1e-10
    eigen=np.zeros(Hc.shape[1]);eigen[:len(values)]=np.maximum(values,0)
    normalized=eigen/eigen.sum() if trace>0 else np.full_like(eigen,np.nan)
    return eigen,normalized,trace,vectors[:,0]

def size_stratum(n):
    return 'small' if n<=3 else 'medium' if n<=19 else 'large'

def compute():
    cfg=json.loads((OUT/'frozen_config.json').read_text())
    assert cfg['script_sha256']==sha(__file__),'Script changed after freeze'
    for p,expected in cfg['files'].items():assert sha(p)==expected
    torch.set_num_threads(1)
    N=cfg['sample_N_per_group'];G=cfg['groups_per_condition']
    cache=torch.load(CACHE,map_location='cpu',mmap=True,weights_only=False)
    labels=np.load(OUT/'winning_group_labels.npz');maps=np.load(MAPS)
    absolute=cache['position_id'].numpy();contexts=cache['block_id'].numpy()
    assert np.array_equal(absolute,labels['absolute_position_id'])
    assert len(np.unique(absolute))==len(absolute)
    all_arrays={};metrics=[];member_rows=[];ctx_rows=[]
    qualification=dict(status='PASS',created_utc=now(),trace_identity_max_relative_error=0.,
                       residual_dropfirst_spectrum_max_relative_error=0.,
                       residual_mean_vector_max_abs=0.,direct_covariance_comparisons=[])
    for c in RULES:
        win=labels[c]
        arr=dict(group_id=np.arange(G),group_size=maps['sizes'].copy(),
                 eigenvalues_original=np.full((G,1024),np.nan),
                 eigenvalues_residual=np.full((G,1024),np.nan),
                 normalized_original=np.full((G,1024),np.nan),
                 normalized_residual=np.full((G,1024),np.nan),
                 support_qualified=np.zeros(G,bool),estimable_original=np.zeros(G,bool),
                 estimable_residual=np.zeros(G,bool),sampled_cache_row=np.full((G,N),-1,np.int64),
                 sampled_absolute_position_id=np.full((G,N),-1,np.int64),
                 original_trace=np.full(G,np.nan),residual_trace=np.full(G,np.nan),removed_trace=np.full(G,np.nan))
        for g in range(G):
            members=np.flatnonzero(maps['labels_'+c]==g)
            p=maps['nD'][members]/maps['ND']; logp=np.log10(p)
            for fid,freq in zip(members,p):
                member_rows.append(dict(condition=c,group_id=g,group_size=len(members),feature_id=int(fid),n_D=int(maps['nD'][fid]),N_D=int(maps['ND']),p_D=float(freq)))
            available=np.flatnonzero(win==g)
            row=dict(condition=c,group_id=g,group_size=len(members),stratum=size_stratum(len(members)),
                     available_winner_positions=len(available),sampled_positions=0,
                     sampled_contexts=0,largest_context_position_fraction='',
                     mean_member_log10p_D=float(logp.mean()),member_log10p_D_sd=float(logp.std(ddof=0)),
                     minimum_member_p_D=float(p.min()),maximum_member_p_D=float(p.max()),
                     original_trace='',removed_PC1_trace='',remaining_trace='',remaining_trace_fraction='',
                     first_share_original='',first_share_residual='',
                     original_status='INSUFFICIENT',residual_status='INSUFFICIENT')
            if len(available)>=N:
                arr['support_qualified'][g]=True
                selected=select_positions(available,members,absolute,N,cfg['sampling_seed'])
                assert len(np.unique(selected))==N and np.all(win[selected]==g)
                arr['sampled_cache_row'][g]=selected
                arr['sampled_absolute_position_id'][g]=absolute[selected]
                H=cache['hidden'][torch.from_numpy(selected)].float().numpy().astype(np.float64)
                Hc=H-H.mean(0,keepdims=True)
                original,normalized,trace,u1=get_spectrum(Hc)
                arr['eigenvalues_original'][g]=original
                arr['normalized_original'][g]=normalized
                arr['original_trace'][g]=trace
                context_ids,context_counts=np.unique(contexts[selected],return_counts=True)
                row.update(sampled_positions=N,sampled_contexts=len(context_ids),
                           largest_context_position_fraction=float(context_counts.max()/N),original_trace=trace,
                           original_status='ESTIMABLE' if trace>0 else 'ZERO_VARIANCE')
                for cid,n in zip(context_ids,context_counts):
                    ctx_rows.append(dict(condition=c,group_id=g,context_id=int(cid),sampled_positions=int(n),fraction=float(n/N)))
                if trace>0:
                    arr['estimable_original'][g]=True
                    v1=Hc.T@u1;v1/=np.linalg.norm(v1)
                    Hr=Hc-np.outer(Hc@v1,v1)
                    residual,resnorm,rtrace,_=get_spectrum(Hr)
                    removed=float(original[0]);arr['removed_trace'][g]=removed;arr['residual_trace'][g]=rtrace
                    arr['eigenvalues_residual'][g]=residual
                    row.update(removed_PC1_trace=removed,remaining_trace=rtrace,remaining_trace_fraction=rtrace/trace,
                               first_share_original=float(normalized[0]))
                    if rtrace>1e-12*trace:
                        arr['normalized_residual'][g]=resnorm
                        arr['estimable_residual'][g]=True
                        row.update(first_share_residual=float(resnorm[0]),residual_status='ESTIMABLE')
                    else:row['residual_status']='ZERO_VARIANCE'
                    trace_err=abs(trace-removed-rtrace)/max(1.,trace)
                    eigen_err=float(np.max(np.abs(residual[:N-1]-original[1:N])))/max(1.,trace)
                    assert trace_err<1e-10 and eigen_err<1e-10
                    qualification['trace_identity_max_relative_error']=max(qualification['trace_identity_max_relative_error'],trace_err)
                    qualification['residual_dropfirst_spectrum_max_relative_error']=max(qualification['residual_dropfirst_spectrum_max_relative_error'],eigen_err)
                    qualification['residual_mean_vector_max_abs']=max(qualification['residual_mean_vector_max_abs'],float(np.max(np.abs(Hr.mean(0)))))
                    if g==0:
                        d=np.linalg.eigvalsh(Hc.T@Hc/(N-1))[::-1]
                        rd=np.linalg.eigvalsh(Hr.T@Hr/(N-1))[::-1]
                        err=float(np.max(np.abs(d-original)))/max(1.,trace)
                        rerr=float(np.max(np.abs(rd-residual)))/max(1.,rtrace)
                        assert err<1e-10 and rerr<1e-10
                        qualification['direct_covariance_comparisons'].append(dict(condition=c,group_id=g,
                                     original_error_by_trace=err,residual_error_by_trace=rerr))
                else:row['residual_status']='ZERO_VARIANCE'
            metrics.append(row)
        all_arrays[c]=arr
        np.savez_compressed(OUT/(c+'_input_hidden_spectra.npz'),**arr)
        print(c,'COMPLETE','supported',arr['support_qualified'].sum(),flush=True)
    main_support=np.zeros(G,bool);main_support[cfg['main_support_group_ids']]=True
    rn_support=np.zeros(G,bool);rn_support[cfg['RN_support_group_ids']]=True
    both=lambda c:all_arrays[c]['estimable_original']&all_arrays[c]['estimable_residual']
    main=main_support&np.logical_and.reduce([both(c) for c in RULES])
    rn=rn_support&both('R')&both('N')
    masks=dict(RFN_support=main_support,RN_support=rn_support,RFN_estimable_original_and_residual=main,
               RN_estimable_original_and_residual=rn,
               RFN_estimable_original=main_support&np.logical_and.reduce([all_arrays[c]['estimable_original'] for c in RULES]),
               RFN_estimable_residual=main_support&np.logical_and.reduce([all_arrays[c]['estimable_residual'] for c in RULES]),
               RN_estimable_original=rn_support&all_arrays['R']['estimable_original']&all_arrays['N']['estimable_original'],
               RN_estimable_residual=rn_support&all_arrays['R']['estimable_residual']&all_arrays['N']['estimable_residual'])
    np.savez_compressed(OUT/'common_masks.npz',**masks)
    selected_ids=np.flatnonzero(main)
    selection=dict(group_ids=selected_ids.tolist(),N_positions=N,original_plot_rank=127,residual_plot_rank=126,
                   main_support_group_ids=cfg['main_support_group_ids'],RN_support_group_ids=cfg['RN_support_group_ids'],
                   RN_estimable_group_ids=np.flatnonzero(rn).tolist(),
                   analysis_population_note='Frozen RFN common winning-position support>=128, samegroupIDs/sizes acrossconditions, then commonoriginal+residualestimability only; all186support andNA retained separately. No endpointdirection selection.',
                   definition_sha256=sha(OUT/'frozen_config.json'),conditions=list(RULES))
    write_json(OUT/'plot_selection.json',selection)
    for name,rows in [('per_group_input_hidden_metrics.csv',metrics),('group_members.csv',member_rows),('sample_context_coverage.csv',ctx_rows)]:
        with open(OUT/name,'w') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summary=dict(status='COMPLETE',created_utc=now(),processing_agent='Codex /root/raw_hidden_spectrum',
                 definition_sha256=sha(OUT/'frozen_config.json'),sample_N_per_group=N,hidden_dimension=1024,
                 all_group_count=G,main_common_support_groups=int(main_support.sum()),
                 main_common_estimable_original_and_residual_groups=int(main.sum()),
                 RN_common_support_groups=int(rn_support.sum()),RN_common_estimable_groups=int(rn.sum()),conditions={})
    def coverage(mask):
        return dict(groups=int(mask.sum()),total_groups=G,
                    group_fraction=float(mask.mean()),members=int(maps['sizes'][mask].sum()),
                    total_members=int(maps['sizes'].sum()),member_fraction=float(maps['sizes'][mask].sum()/maps['sizes'].sum()))
    summary['coverage']=dict(main_RFN=coverage(main),supplement_RN=coverage(rn),
                             all_supported_per_condition={c:coverage(both(c)) for c in RULES})
    summary['missing_support_by_group_size']={}
    for c in RULES:
        summary['missing_support_by_group_size'][c]={}
        for s in ('small','medium','large'):
            stratum_mask=np.array([size_stratum(int(n))==s for n in maps['sizes']])
            absent=stratum_mask&~all_arrays[c]['support_qualified']
            summary['missing_support_by_group_size'][c][s]=dict(
                all_groups_in_stratum=int(stratum_mask.sum()),missing_groups=int(absent.sum()),
                missing_members=int(maps['sizes'][absent].sum()),group_ids=np.flatnonzero(absent).tolist())
    for c in RULES:
        a=all_arrays[c]
        summary['conditions'][c]=dict(sufficient_groups=int(a['support_qualified'].sum()),
                                      insufficient_groups=int((~a['support_qualified']).sum()),
                                      zero_variance_original_groups=int((a['support_qualified']&~a['estimable_original']).sum()),
                                      zero_variance_residual_groups=int((a['support_qualified']&~a['estimable_residual']).sum()))
    population_rows=[];paired_rows=[]
    for pop,mask,arms in [('main_RFN',main,RULES),('supplement_RN',rn,('R','N'))]:
        ids_pop=np.flatnonzero(mask)
        for stratum in ('all','small','medium','large'):
            ii=np.array([g for g in ids_pop if stratum=='all' or size_stratum(int(maps['sizes'][g]))==stratum],dtype=np.int64)
            for c in arms:
                a=all_arrays[c]
                mr=[r for r in metrics if r['condition']==c and r['group_id'] in set(ii)]
                if len(ii):
                    population_rows.append(dict(population=pop,stratum=stratum,condition=c,groups=len(ii),
                        first_share_original_mean=float(a['normalized_original'][ii,0].mean()),
                        first_share_original_median=float(np.median(a['normalized_original'][ii,0])),
                        first_share_residual_mean=float(a['normalized_residual'][ii,0].mean()),
                        first_share_residual_median=float(np.median(a['normalized_residual'][ii,0])),
                        original_trace_mean=float(a['original_trace'][ii].mean()),
                        remaining_trace_mean=float(a['residual_trace'][ii].mean()),
                        mean_remaining_trace_fraction=float((a['residual_trace'][ii]/a['original_trace'][ii]).mean()),
                        mean_group_member_log10p_D=float(np.mean([r['mean_member_log10p_D'] for r in mr])),
                        median_sampled_contexts=float(np.median([r['sampled_contexts'] for r in mr])),
                        median_largest_context_fraction=float(np.median([r['largest_context_position_fraction'] for r in mr])),
                        maximum_largest_context_fraction=float(np.max([r['largest_context_position_fraction'] for r in mr]))))
            for other in ('F','N'):
                if other not in arms or not len(ii):continue
                for state in ('original','residual'):
                    diff=all_arrays['R']['normalized_'+state][ii,0]-all_arrays[other]['normalized_'+state][ii,0]
                    paired_rows.append(dict(population=pop,stratum=stratum,contrast='R-'+other,state=state,
                                            groups=len(ii),mean_first_share_difference=float(diff.mean()),
                                            median_first_share_difference=float(np.median(diff)),
                                            R_lower_groups=int(np.count_nonzero(diff<0)),
                                            R_equal_groups=int(np.count_nonzero(diff==0)),R_higher_groups=int(np.count_nonzero(diff>0))))
    for c in RULES:
        a=all_arrays[c];ii=np.flatnonzero(both(c))
        population_rows.append(dict(population='all_supported_per_condition',stratum='all',condition=c,groups=len(ii),
                        first_share_original_mean=float(a['normalized_original'][ii,0].mean()),
                        first_share_original_median=float(np.median(a['normalized_original'][ii,0])),
                        first_share_residual_mean=float(a['normalized_residual'][ii,0].mean()),
                        first_share_residual_median=float(np.median(a['normalized_residual'][ii,0])),
                        original_trace_mean=float(a['original_trace'][ii].mean()),remaining_trace_mean=float(a['residual_trace'][ii].mean()),
                        mean_remaining_trace_fraction=float((a['residual_trace'][ii]/a['original_trace'][ii]).mean()),
                        mean_group_member_log10p_D='',median_sampled_contexts='',median_largest_context_fraction='',maximum_largest_context_fraction=''))
    for name,rows in [('population_summary.csv',population_rows),('paired_group_contrasts.csv',paired_rows)]:
        with open(OUT/name,'w') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summary['main_population']={c:next(r for r in population_rows if r['population']=='main_RFN' and r['stratum']=='all' and r['condition']==c) for c in RULES}
    summary['RN_supplement']={c:next(r for r in population_rows if r['population']=='supplement_RN' and r['stratum']=='all' and r['condition']==c) for c in ('R','N')}
    overlap={}
    for pop,mask,arms in [('main_RFN',main,RULES),('supplement_RN',rn,('R','N'))]:
        sets={c:np.unique(all_arrays[c]['sampled_cache_row'][mask]) for c in arms}
        diag={}
        for c in arms:
            flattened=all_arrays[c]['sampled_cache_row'][mask].ravel()
            _,n=np.unique(flattened,return_counts=True)
            diag[c]=dict(group_position_slots=len(flattened),unique_positions=len(n),maximum_reuse=int(n.max()))
        for other in ('F','N'):
            if other in arms:
                inter=len(np.intersect1d(sets['R'],sets[other]));union=len(np.union1d(sets['R'],sets[other]))
                diag['R_'+other]=dict(shared_unique_positions=inter,jaccard=inter/union)
        overlap[pop]=diag
    write_json(OUT/'position_overlap_diagnostics.json',overlap)
    qualification['original_theoretical_rank']=127;qualification['residual_theoretical_rank']=126
    qualification['original_direction128_share_max']=float(max(np.nanmax(all_arrays[c]['normalized_original'][:,127]) for c in RULES))
    qualification['residual_beyond126_share_max']=float(max(np.nanmax(all_arrays[c]['normalized_residual'][:,126:]) for c in RULES))
    qualification['no_hidden_inplace_write']='Read-only mmap; selectedrows copied and FP64centered/projection arrays allocated separately'
    write_json(OUT/'numerical_qualification.json',qualification)
    summary['files']={p.name:dict(bytes=p.stat().st_size,sha256=sha(p)) for p in OUT.glob('*input_hidden_spectra.npz')}
    write_json(OUT/'phi_input_hidden_summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('command',choices=['support','qualify','freeze','compute'])
    a=ap.parse_args();globals()[a.command]()
