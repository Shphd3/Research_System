#!/usr/bin/env python3
"""Frozen final-layer learning data and D-only R/F/N routing.

No trainable model or learning-loss-driven choice is present here. R uses the
previous 186 nonsingleton communities; all conditions use the same 13,807 IDs.
The full sparse CrossCoder event set is retained for fixed feature metrics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time

import numpy as np
from scipy import sparse

E = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
OLD = E / 'analysis/feature_frequency/20261015T143300Z'
PHASE = E / 'analysis/feature_relation_phase1/20261013T173130Z'
ROOT = E / 'analysis/relation_learning/20261015T164000Z/data'
DATA = E / 'data/direct_dclm_bins_a15'
CKPT = E / 'runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt'
BASE = '/data/share/Qwen3-0.6B-Base'
F = 16384
SEED = 20261016
sys.path.insert(0, str(E))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    os.replace(tmp, path)


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(16 << 20), b''):
            h.update(b)
    return h.hexdigest()


def log(stage, **kw):
    print(json.dumps({'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                      'stage': stage, **kw}, ensure_ascii=False), flush=True)


def stable_hash(values, salt=0):
    """Label-independent integer hash, also identical across conditions."""
    x = np.asarray(values, dtype=np.uint64) + np.uint64(salt)
    with np.errstate(over='ignore'):
        x = (x ^ (x >> np.uint64(30))) * np.uint64(0xbf58476d1ce4e5b9)
        x = (x ^ (x >> np.uint64(27))) * np.uint64(0x94d049bb133111eb)
    return x ^ (x >> np.uint64(31))


def labels_from_groups(groups):
    labels = np.full(F, -1, np.int32)
    for i, members in enumerate(groups):
        if np.any(labels[members] >= 0):
            raise AssertionError('overlapping community membership')
        labels[members] = i
    return labels


def member_hash_order(labels, G):
    """Hash the sorted feature IDs in each group, never learning labels."""
    digests=[]
    for g in range(G):
        members=np.flatnonzero(labels==g).astype('<i4')
        digests.append(hashlib.sha256(members.tobytes()).digest())
    return np.asarray(sorted(range(G),key=lambda g:(digests[g],g)),np.int32)


def scores_and_winner(ptr, ids, labels, sizes, means=None, stds=None, tie_order=None):
    """D-standardized binary mean; unhit groups never compete."""
    rows = len(ptr) - 1
    row = np.repeat(np.arange(rows, dtype=np.int32), np.diff(ptr))
    group_ids = labels[ids]
    keep = group_ids >= 0
    m = sparse.csr_matrix((np.ones(int(keep.sum()), np.int32),
                           (row[keep], group_ids[keep])), shape=(rows, len(sizes)))
    counts = m.toarray()
    binary_score = counts / sizes[None, :]
    score=binary_score.copy()
    if means is not None:
        score=np.divide(score-means[None,:],stds[None,:],out=np.zeros_like(score),where=stds[None,:]>0)
    score[counts==0]=-np.inf
    if tie_order is None:
        tie_order=member_hash_order(labels,len(sizes))
    win = tie_order[np.argmax(score[:, tie_order], axis=1)].astype(np.int32)
    maximum = score[np.arange(rows), win]
    nohit=~np.isfinite(maximum)
    win[nohit] = -1
    tie_count = ((score == maximum[:, None]) & (score > 0)).sum(1)
    mass = binary_score.sum(1)
    binary_maximum=binary_score.max(1)
    selected_binary=binary_score[np.arange(rows),np.maximum(win,0)]
    selected_binary[nohit]=0
    dropped_fraction = np.divide(mass - selected_binary, mass,
                                 out=np.zeros(rows), where=mass > 0)
    return win, {'no_hit_fraction': float(nohit.mean()),
                 'tied_positive_fraction': float((tie_count > 1).mean()),
                 'mean_discarded_score_fraction': float(dropped_fraction.mean()),
                 'mean_winning_group_size': float(sizes[win[win >= 0]].mean())}, counts


def fit_balanced_map(winner, K=4):
    """Largest D-only winner masses first; common uniform load objective."""
    G = int(winner.max()) + 1
    weights = np.bincount(winner[winner >= 0], minlength=G)
    order = np.lexsort((stable_hash(np.arange(G), SEED + 19), -weights))
    load = np.zeros(K, np.int64)
    mapping = np.zeros(G, np.int32)
    for g in order:
        least = np.flatnonzero(load == load.min())
        k = int(least[np.argmin(stable_hash(least, SEED + int(g)))])
        mapping[g] = k
        load[k] += weights[g]
    return mapping, weights


def apply_routes(winner, mapping, position_ids):
    out = (stable_hash(position_ids, SEED + 23) % np.uint64(4)).astype(np.int64)
    hit = winner >= 0
    out[hit] = mapping[winner[hit]]
    return out


def collect_discovery_sample(max_rows=32768):
    """First source-ordered D rows of the frozen sparse cache; no V usage."""
    split = json.loads((PHASE / 'split_manifest.json').read_text())
    blocks = split['blocks']
    ends = np.array([b['position_end'] for b in blocks], np.int64)
    is_d = np.array([b['side'] == 'D' for b in blocks])
    records = np.load(DATA / 'index_val/records.npy', mmap_mode='r')
    prefix = np.load(DATA / 'index_val/prefix.npy', mmap_mode='r')
    index = json.loads((DATA / 'index_val/manifest.json').read_text())
    source = np.memmap(index['sources'][0]['path'], mode='r', dtype='<u4')
    chunks = []
    for rank in range(4):
        chunks.extend(json.loads((PHASE / f'feature_cache/rank{rank}/manifest.json').read_text())['chunks'])
    all_ptr = [0]
    all_ids, all_pos = [], []
    taken = 0
    for meta in sorted(chunks, key=lambda x: x['start']):
        positions = np.arange(meta['start'], meta['end'], dtype=np.int64)
        keep = np.flatnonzero(is_d[np.searchsorted(ends, positions, side='right')])
        if not len(keep):
            continue
        keep = keep[:max_rows - taken]
        cache = np.load(meta['file'])
        ptr, ids = cache['ptr'].astype(np.int64), cache['ids'].astype(np.int32)
        for r in keep:
            all_ids.append(ids[ptr[r]:ptr[r+1]])
            all_ptr.append(all_ptr[-1] + int(ptr[r+1]-ptr[r]))
        global_ids = positions[keep]
        contexts = np.searchsorted(prefix, global_ids, side='right') - 1
        absolute = np.empty(len(keep), np.int64)
        for ci in np.unique(contexts):
            _, start, n, limit = map(int, records[ci])
            valid = np.flatnonzero(~np.isin(source[start:start+n], index['excluded_ids']))[:limit]
            ss = contexts == ci
            absolute[ss] = start + valid[global_ids[ss] - int(prefix[ci])]
        all_pos.append(absolute)
        taken += len(keep)
        if taken == max_rows:
            break
    if taken != max_rows:
        raise ValueError('not enough discovery rows')
    return np.array(all_ptr, np.int64), np.concatenate(all_ids), np.concatenate(all_pos)


def build_routes(out=ROOT, d_rows=32768, bins=10):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    old = json.loads((OLD / 'main/groups_D.json').read_text())
    groups = [np.asarray(x['members'], np.int32) for x in old if x['size'] > 1]
    sizes = np.asarray([len(x) for x in groups], np.int32)
    labels_R = labels_from_groups(groups)
    pool = np.flatnonzero(labels_R >= 0)
    nD = np.load(PHASE / 'feature_frequency.npz')['n'][0]
    ND = int(json.loads((PHASE / 'split_manifest.json').read_text())['N_D'])
    ranked = pool[np.lexsort((pool, nD[pool]))]
    labels_F = np.full(F, -1, np.int32)
    begin = 0
    for g, size in enumerate(sizes):
        labels_F[ranked[begin:begin+size]] = g
        begin += size
    # In each discovery-frequency decile, preserve the exact multiset of group
    # labels and randomly exchange feature identities. Group size and per-bin
    # composition remain exact; original edges must actually be destroyed.
    labels_N = np.full(F, -1, np.int32)
    rng = np.random.default_rng(SEED + 29)
    for part in np.array_split(ranked, bins):
        labels_N[part] = labels_R[rng.permutation(part)]
    assert np.array_equal(np.bincount(labels_F[pool]), sizes)
    assert np.array_equal(np.bincount(labels_N[pool]), sizes)
    ptr, ids, positions = collect_discovery_sample(d_rows)
    artifact = {'pool': pool, 'sizes': sizes, 'nD': nD, 'ND': np.array(ND)}
    summaries, route_all = {}, {}
    for condition, labels in [('R', labels_R), ('F', labels_F), ('N', labels_N)]:
        _, _, counts = scores_and_winner(ptr, ids, labels, sizes)
        binary_score=counts/sizes[None,:]
        means=binary_score.mean(0)
        stds=binary_score.std(0,ddof=0)
        tie_order=member_hash_order(labels,len(sizes))
        win, summary, _ = scores_and_winner(ptr, ids, labels, sizes, means,stds,tie_order)
        mapping, weights = fit_balanced_map(win)
        if len(mapping) < len(sizes):
            mapping = np.pad(mapping, (0, len(sizes)-len(mapping)), constant_values=0)
            weights = np.pad(weights, (0, len(sizes)-len(weights)), constant_values=0)
        routes = apply_routes(win, mapping, positions)
        artifact[f'labels_{condition}'] = labels
        artifact[f'means_{condition}'] = means
        artifact[f'stds_{condition}'] = stds
        artifact[f'tie_order_{condition}'] = tie_order
        artifact[f'mapping_{condition}'] = mapping
        artifact[f'discovery_winner_counts_{condition}'] = weights
        route_all[condition] = routes
        summary.update({'D_route_load': np.bincount(routes, minlength=4).tolist(),
                        'winner_group_counts': weights.tolist(),
                        'winner_groups_never_used': int((weights == 0).sum()),
                        'D_load_fraction': (np.bincount(routes, minlength=4) / d_rows).tolist()})
        summaries[condition] = summary
        log('route_fit', condition=condition, **{k:v for k,v in summary.items() if k != 'winner_group_counts'})
    # Fixed primary feature lists independent of route pool and evaluation hits.
    candidate = np.load(OLD / 'candidate_mask.npy')
    eligible = np.flatnonzero(candidate & (nD >= 100) & (nD < ND))
    order = eligible[np.lexsort((eligible, nD[eligible]))]
    q = len(order) // 4
    artifact['low_ids'], artifact['high_ids'] = order[:q], order[-q:]
    event_rows=np.repeat(np.arange(d_rows,dtype=np.int32),np.diff(ptr))
    logp=np.log10(np.maximum(nD/ND,1/ND))
    row_logfreq=np.bincount(event_rows,weights=logp[ids],minlength=d_rows)/np.diff(ptr)
    artifact['frequency_cuts']=np.quantile(row_logfreq,np.arange(1,10)/10)
    np.savez(out / 'route_maps.npz', **artifact)
    import csv
    with open(OLD / 'main/edges_D.csv') as f:
        edges = list(csv.DictReader(f))
    uv = np.array([(int(e['u']), int(e['v'])) for e in edges], np.int32)
    within = labels_R[uv[:,0]] == labels_R[uv[:,1]]
    within &= labels_R[uv[:,0]] >= 0
    retained = {}
    for c, lab in [('R',labels_R),('F',labels_F),('N',labels_N)]:
        retained[c] = float((lab[uv[within,0]] == lab[uv[within,1]]).mean())
    disagreement = {f'{a}_{b}': float((route_all[a] != route_all[b]).mean())
                    for a,b in [('R','F'),('R','N'),('F','N')]}
    receipt = {'status':'COMPLETE', 'R_groups':len(groups), 'feature_pool':len(pool),
               'D_fit_positions':d_rows, 'frequency_bins':bins, 'seed':SEED,
               'score':'hit-only ((binary active member count / full group size)-Dmean)/Dstd; Dstd0 score0; no-hit groups excluded',
               'tie':'ascending SHA256 of sorted original feature IDs in group; learning-label independent',
               'fallback':'splitmix64(absolute source token offset+20261039) modulo 4',
               'mapping':'D winner mass largest first, each to least-loaded expert; fixed hash ties; same uniform objective',
               'N':'permute group labels within D-frequency equal-count bins; exact per-group per-bin counts',
               'R_original_within_edge_retention':retained,
               'D_route_disagreement':disagreement, 'conditions':summaries,
               'low_high_definition':{'candidate_count':len(eligible),'count_each':q,'minimum_D_hits':100,
                                      'range':'bottom/top25% ranked D frequency; ties original feature ID'},
               'row_frequency_definition':'mean log10 discovery frequency over the complete gated feature event set; D-only decile cuts',
               'frequency_cuts':artifact['frequency_cuts'].tolist(),
               'source_hashes':{'groups_D':sha(OLD/'main/groups_D.json'),
                                'frequency':sha(PHASE/'feature_frequency.npz')},
               'scientific_boundary':'operationalized deterministic allocation; no learning utility result; D sample is within one source bin'}
    receipt['amendment_before_learning']={'original':'unstandardized meanbinary with fixed group-ID hash',
        'reason':'D-only initial F scoring tied on99.896% of positions and151/186 groups never won; only one pre-loss repair allowed',
        'new':'apply identical per-condition D mean/std standardization, hit-only eligibility, member-content hash ties',
        'original_preserved':'meanbinary_initial/route_definition.json and route_maps.npz',
        'no_learning_loss_observed':True}
    write_json(out/'route_definition.json',receipt)
    return receipt


def load_models(device):
    import gc
    import torch
    from recovery_20261015.a23.runner import isolate_optional_flash_attention
    policy=isolate_optional_flash_attention()
    log('runtime_optional_plugins',policy=policy)
    from crosscoder.model import CrossCoderConfig
    from crosscoder.fast_batchtopk_a21 import FastBatchTopKCrossCoder
    from crosscoder.batchtopk_a18 import CenteredRMSStats
    from crosscoder.extraction_a16 import FrozenQwenExtractor
    from transformers import AutoModelForCausalLM
    payload = torch.load(CKPT, map_location='cpu', mmap=True, weights_only=False)
    coder = FastBatchTopKCrossCoder(CrossCoderConfig(n_layers=14,hidden_size=1024,
                        dict_size=F,init_encoder_norm=1/np.sqrt(14)), device='meta',compute_dtype='bfloat16')
    coder.load_state_dict(payload['crosscoder'],strict=True,assign=True)
    coder = coder.to(device).eval().requires_grad_(False)
    stats = CenteredRMSStats.from_state_dict(payload['normalization'])
    model = AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,
                        trust_remote_code=False,torch_dtype=torch.bfloat16,attn_implementation='sdpa').to(device)
    model.eval().requires_grad_(False)
    ex = FrozenQwenExtractor.from_model(model,selected_block_indices=list(range(1,28,2)))
    ex.model.config._attn_implementation='sdpa'
    ex.backbone.config._attn_implementation='sdpa'
    del payload
    gc.collect()
    return model, ex, coder, stats


def encode(raw, coder, stats):
    """Frozen TRAIN threshold, no BatchTopK over sequence positions."""
    import torch
    norm = coder.decoder_norm_weights().detach().float()
    result=[]
    for part in raw.split(1024):
        relu = coder._post_relu(stats.normalize(part))
        scores = relu.float() * norm
        result.append(relu * (scores > float(coder.threshold)))
    return torch.cat(result)


def prefix_causality_check(ex,coder,stats,maps,device):
    import torch
    from crosscoder.bin_data_a15 import BinEvents
    event=BinEvents(DATA,'TRAIN')[4096]
    original=torch.tensor(event['input_ids'][:128],device=device,dtype=torch.long)[None]
    cases=[]
    for t in [7,31,63]:
        changed=original.clone()
        changed[:,t+1:]=(changed[:,t+1:]+12345)%151643
        rr=[]
        for tokens in [original,changed,original[:,:t+1]]:
            valid=torch.zeros_like(tokens,dtype=torch.bool);valid[:,t]=True
            rr.append(ex.extract(tokens,torch.ones_like(tokens),valid).activations)
        zz=[encode(x,coder,stats) for x in rr]
        routes=[]
        for z in zz:
            ids=torch.nonzero(z[0]>0,as_tuple=True)[0].cpu().numpy().astype(np.int32)
            ptr=np.array([0,len(ids)],np.int64)
            row=[]
            for c in ['R','F','N']:
                win,_,_=scores_and_winner(ptr,ids,maps[f'labels_{c}'],maps['sizes'],maps[f'means_{c}'],maps[f'stds_{c}'],maps[f'tie_order_{c}'])
                row.append(int(apply_routes(win,maps[f'mapping_{c}'],np.array([int(event['position_ids'][t])]))[0]))
            routes.append(row)
        change_mask=int(((zz[0]>0)!=(zz[1]>0)).sum())
        trunc_mask=int(((zz[0]>0)!=(zz[2]>0)).sum())
        item={'position_in_context':t,'future_change_raw_max_abs':float((rr[0]-rr[1]).abs().max()),
              'prefix_truncation_raw_max_abs':float((rr[0]-rr[2]).abs().max()),
              'future_change_z_max_abs':float((zz[0]-zz[1]).abs().max()),
              'prefix_truncation_z_max_abs':float((zz[0]-zz[2]).abs().max()),
              'future_change_event_differences':change_mask,
              'prefix_truncation_event_differences':trunc_mask,'routes_original_changed_truncated':routes}
        item['PASS']=change_mask==0 and item['future_change_raw_max_abs']==0 and item['future_change_z_max_abs']==0 and routes[0]==routes[1]==routes[2]
        cases.append(item)
    result={'status':'PASS' if all(x['PASS'] for x in cases) else 'FAIL','cases':cases,
            'future_tokens':'all positions after t changed; same shape',
            'truncated_prefix':'separate forward ending at t; fixed per-position TRAIN normalization and gate',
            'no_online_early_layer_router':True,
            'causal_gate':'fixed-shape arbitrary future change: exact raw,z,events,routes; truncated-prefix selected routes unchanged',
            'BF16_cross_shape_gate_sensitivity':'full thresholded events diagnosed separately, not bitwise causal requirement',
            'original_failure_preserved':'prefix_causality_attempt0_BF16_truncation_strict.json',
            'amendment':'R1.6 before any learning loss; independent FP32/padded-future diagnostic in prefix_precision.json'}
    return result


def native_zero_guard(model,tokens,positions,raw):
    """Actual full-model logits vs independently normalized cached raw h.

    Both output-head matrix shapes match to avoid attributing GEMM tiling
    rounding to extraction. Adapter zero-output follows the cached path.
    """
    import torch
    import torch.nn.functional as functional
    cached_h=raw[:,-1,:].detach().cpu().to(raw.device)
    native_logits=model(input_ids=tokens,attention_mask=torch.ones_like(tokens),
                        use_cache=False,return_dict=True).logits
    # Match the actual Qwen3RMSNorm operation order: FP32 normalization,
    # cast back to BF16, then multiply by the BF16 norm weight.
    normalized=cached_h.float()
    normalized=normalized*torch.rsqrt(normalized.pow(2).mean(-1,keepdim=True)+model.model.norm.variance_epsilon)
    normalized=normalized.to(cached_h.dtype)*model.model.norm.weight
    native_norm=model.model.norm(cached_h)
    assert torch.equal(normalized,native_norm),'cached RMSNorm differs from native operation order'
    all_normalized=torch.zeros((*tokens.shape,cached_h.shape[-1]),device=tokens.device,dtype=cached_h.dtype)
    all_normalized[positions[:,0],positions[:,1]]=normalized
    cached_logits=model.lm_head(all_normalized)
    pick=torch.linspace(0,len(positions)-1,32,device=tokens.device).long()
    pp=positions[pick]
    native=native_logits[pp[:,0],pp[:,1]].float()
    cached=cached_logits[pp[:,0],pp[:,1]].float()
    target=tokens[pp[:,0],pp[:,1]+1]
    loss_native=functional.cross_entropy(native,target,reduction='none')
    loss_cached=functional.cross_entropy(cached,target,reduction='none')
    result={'status':'PASS' if torch.equal(native,cached) else 'FAIL',
            'positions':len(pick),'native_full_model_forward':True,
            'cached_hidden_CPU_roundtrip':True,'output_head_matrix_shapes_matched':True,
            'native_RMSNorm_exact':True,'logits_exact':bool(torch.equal(native,cached)),
            'max_absolute_logit_error':float((native-cached).abs().max()),
            'mean_absolute_logit_error':float((native-cached).abs().mean()),
            'mean_native_NTP_loss':float(loss_native.mean()),
            'mean_cached_NTP_loss':float(loss_cached.mean()),
            'max_absolute_NTP_loss_error':float((loss_native-loss_cached).abs().max()),
            'zero_adapter_reference':'unchanged raw h plus zero expert residual, followed by original final norm and head'}
    return result


def make_cache(out=ROOT,device='cuda:0',train_contexts=128,eval_contexts=64,
               train_start=8192,eval_start_in_file=8192,batch_contexts=8):
    import torch
    from crosscoder.bin_data_a15 import BinEvents
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    torch.set_num_threads(2)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False
    maps=np.load(out/'route_maps.npz')
    model,ex,coder,stats=load_models(device)
    with torch.inference_mode():
        causal=prefix_causality_check(ex,coder,stats,maps,device)
    write_json(out/'prefix_causality.json',causal)
    if causal['status']!='PASS':
        raise RuntimeError('prefix causality failed; preserve evidence and stop cache')
    events=BinEvents(DATA,'TRAIN')
    fi=events.records[:,0]
    file0=np.flatnonzero(fi==0)
    file1=np.flatnonzero(fi==1)
    selections={'train':file0[train_start:train_start+train_contexts],
                'eval':file1[eval_start_in_file:eval_start_in_file+eval_contexts]}
    assert len(selections['train'])==train_contexts and len(selections['eval'])==eval_contexts
    coder_buffers={k:v.detach().clone() for k,v in coder.named_buffers()}
    receipts={}
    for split,contexts in selections.items():
        if (out/f'{split}.pt').exists():
            log('cache_existing',split=split)
            receipts[split]=json.loads((out/f'{split}_manifest.json').read_text())
            continue
        started=time.monotonic()
        hidden=[];targets=[];feature_ids=[];feature_ptr=[0];block=[];position=[];all_routes={c:[] for c in ['R','F','N']}
        for begin in range(0,len(contexts),batch_contexts):
            chosen=contexts[begin:begin+batch_contexts]
            ee=[events[int(i)] for i in chosen]
            tokens=torch.tensor([e['input_ids'] for e in ee],device=device,dtype=torch.long)
            valid=torch.tensor([e['valid_mask'] for e in ee],device=device,dtype=torch.bool)
            valid[:,-1]=False
            target_valid=~torch.isin(tokens[:,1:],torch.tensor(events.manifest['excluded_ids'],device=device))
            valid[:,:-1]&=target_valid
            with torch.inference_mode():
                result=ex.extract(tokens,torch.ones_like(tokens),valid)
                raw=result.activations
                z=encode(raw,coder,stats)
                if split=='train' and begin==0:
                    guard=native_zero_guard(model,tokens,result.position_indices,raw)
                    write_json(out/'native_zero_guard.json',guard)
                    log('native_zero_guard',**guard)
                    if guard['status']!='PASS':
                        raise RuntimeError('full native model vs cached zero adapter logits failed')
            rr,ff=torch.nonzero(z>0,as_tuple=True)
            counts=torch.bincount(rr,minlength=len(z)).cpu().numpy()
            ptr=np.r_[0,np.cumsum(counts)].astype(np.int64)
            ids=ff.cpu().numpy().astype(np.int32)
            pos=result.position_indices
            target=tokens[pos[:,0],pos[:,1]+1].cpu()
            absolute=np.array([ee[int(b)]['position_ids'][int(t)] for b,t in pos.cpu().tolist()],np.int64)
            context_ids=np.array([int(chosen[int(b)]) for b,_ in pos.cpu().tolist()],np.int32)
            hidden.append(raw[:,-1,:].detach().cpu())
            targets.append(target)
            feature_ids.append(torch.from_numpy(ids))
            feature_ptr.extend((ptr[1:]+feature_ptr[-1]).tolist())
            block.append(torch.from_numpy(context_ids))
            position.append(torch.from_numpy(absolute))
            for c in ['R','F','N']:
                winner,_,_=scores_and_winner(ptr,ids,maps[f'labels_{c}'],maps['sizes'],maps[f'means_{c}'],maps[f'stds_{c}'],maps[f'tie_order_{c}'])
                routes=apply_routes(winner,maps[f'mapping_{c}'],absolute)
                all_routes[c].append(torch.from_numpy(routes))
            log('cache_progress',split=split,contexts=min(begin+batch_contexts,len(contexts)),
                positions=sum(len(x) for x in hidden),seconds=time.monotonic()-started)
        payload={'hidden':torch.cat(hidden),'target':torch.cat(targets),
                 'routes':{c:torch.cat(v) for c,v in all_routes.items()},
                 'feature_ptr':torch.tensor(feature_ptr,dtype=torch.long),'feature_ids':torch.cat(feature_ids),
                 'block_id':torch.cat(block),'position_id':torch.cat(position),
                 'low_ids':torch.from_numpy(maps['low_ids'].copy()).long(),
                 'high_ids':torch.from_numpy(maps['high_ids'].copy()).long()}
        payload['discovery_frequency']=torch.from_numpy(maps['nD']/maps['ND']).double()
        payload['frequency_cuts']=torch.from_numpy(maps['frequency_cuts'].copy()).double()
        tmp=out/f'{split}.pt.tmp';torch.save(payload,tmp);os.replace(tmp,out/f'{split}.pt')
        sources={events.manifest['sources'][int(events.records[int(i),0])]['path'] for i in contexts}
        manifest={'status':'COMPLETE','positions':len(payload['target']), 'contexts':contexts.tolist(),
                  'source_paths':sorted(sources),'source_split':'original CrossCoder TRAIN bins; source files disjoint from structure VAL',
                  'source_identities':[x for x in events.manifest['sources'] if x['path'] in sources],
                  'original_document_independence':'UNKNOWN',
                  'feature_representation':'full positive gated shared latent CSR, no feature truncation',
                  'hidden':'raw final Qwen3 block residual-post before final norm, BF16',
                  'target':'real next token at t+1, both current and target special IDs excluded; context last position excluded',
                  'file':str(out/f'{split}.pt'),'sha256':sha(out/f'{split}.pt'),
                  'route_load':{c:torch.bincount(v,minlength=4).tolist() for c,v in payload['routes'].items()},
                  'mean_l0':len(payload['feature_ids'])/len(payload['target']),
                  'low_feature_routing_pool_coverage':float(np.isin(maps['low_ids'],maps['pool']).mean()),
                  'elapsed_seconds':time.monotonic()-started,'threshold':float(coder.threshold),
                  'coder_batch':1024,'base_batch_contexts':batch_contexts}
        write_json(out/f'{split}_manifest.json',manifest)
        receipts[split]=manifest
        del payload
    for k,v in coder.named_buffers():
        assert torch.equal(v,coder_buffers[k]),f'CrossCoder buffer changed: {k}'
    ex.assert_frozen()
    write_json(out/'cache_manifest.json',{'status':'COMPLETE','splits':receipts,
        'no_train_eval_file_overlap':not set(receipts['train']['source_paths'])&set(receipts['eval']['source_paths']),
        'CrossCoder_saw_learning_text_during_dictionary_training':True,
        'no_loss_based_selection':True,'data_independence_boundary':'source-file disjoint for adapter training/evaluation and structure discovery; original document/near duplicate independence UNKNOWN',
        'coder_buffers_unchanged':True,'base_frozen':True,'prefix_causality':causal['status']})


def main():
    p=argparse.ArgumentParser()
    p.add_argument('action',choices=['routes','prefix','cache'])
    p.add_argument('--out',type=Path,default=ROOT)
    p.add_argument('--device',default='cuda:0')
    p.add_argument('--d-rows',type=int,default=32768)
    p.add_argument('--bins',type=int,default=10)
    p.add_argument('--train-contexts',type=int,default=128)
    p.add_argument('--eval-contexts',type=int,default=64)
    p.add_argument('--train-start',type=int,default=8192)
    p.add_argument('--eval-start-in-file',type=int,default=8192)
    p.add_argument('--batch-contexts',type=int,default=8)
    a=p.parse_args()
    if a.action=='routes':
        build_routes(a.out,a.d_rows,a.bins)
    elif a.action=='prefix':
        import torch
        torch.set_num_threads(2)
        torch.backends.cuda.matmul.allow_tf32=False
        torch.backends.cudnn.allow_tf32=False
        started=time.monotonic()
        _,ex,coder,stats=load_models(a.device)
        with torch.inference_mode():
            result=prefix_causality_check(ex,coder,stats,np.load(a.out/'route_maps.npz'),a.device)
        result['elapsed_seconds']=time.monotonic()-started
        write_json(a.out/'prefix_causality.json',result)
        log('prefix_causality_complete',**result)
        if result['status']!='PASS':
            raise RuntimeError('prefix causality failed')
    else:
        make_cache(a.out,a.device,a.train_contexts,a.eval_contexts,a.train_start,a.eval_start_in_file,a.batch_contexts)


if __name__=='__main__':
    main()
