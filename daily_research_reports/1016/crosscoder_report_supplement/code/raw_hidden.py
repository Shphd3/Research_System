#!/usr/bin/env python3
"""Descriptive spectra of cached raw hidden at fixed group-hit positions.

Support subcommand only reads binary feature CSR; it never reads hidden values.
Compute is only enabled after a separately written frozen_config.json.
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import torch
from numba import njit

E = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
OUT = E / 'analysis/report_spectrum/20261016_raw_hidden'
GROUPS = E / 'analysis/report_spectrum/20261016_spectrum'
CACHE = E / 'analysis/relation_learning/20261015T164000Z/data_eval512/eval.pt'

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for x in iter(lambda: f.read(1 << 20), b''):
            h.update(x)
    return h.hexdigest()

def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

@njit(cache=False)
def event_counts(ptr, ids, group_of, groups):
    counts = np.zeros((len(ptr) - 1, groups), dtype=np.uint8)
    for r in range(len(ptr) - 1):
        for j in range(ptr[r], ptr[r + 1]):
            g = group_of[ids[j]]
            if g >= 0:
                counts[r, g] += 1
    return counts

def load_members(rule):
    a = np.load(GROUPS / (rule + '_members.npy'))
    assert a.shape == (1119, 14)
    assert len(np.unique(a)) == a.size == 15666
    return a

def mapped_counts(cache, members):
    group_of = np.full(16384, -1, dtype=np.int32)
    group_of[members.ravel()] = np.repeat(np.arange(len(members)), members.shape[1])
    return event_counts(cache['feature_ptr'].numpy(), cache['feature_ids'].numpy(),
                        group_of, len(members))

def support():
    OUT.mkdir(parents=True, exist_ok=True)
    cache = torch.load(CACHE, map_location='cpu', mmap=True, weights_only=False)
    summary = dict(status='SUPPORT_ONLY_NO_HIDDEN_VALUES_READ', created_utc=now(),
                   processing_agent='Codex /root/raw_hidden_spectrum', cache=str(CACHE),
                   positions=len(cache['target']), hidden_schema=dict(
                       shape=list(cache['hidden'].shape), dtype=str(cache['hidden'].dtype)),
                   event_definition='Positive gated CrossCoder shared latent coordinates; full cached CSR, no feature truncation',
                   group_size=14, groups_per_rule=1119, rules={})
    rows = []
    for rule in ('same_frequency', 'mixed_frequency'):
        counts = mapped_counts(cache, load_members(rule))
        rule_stats = {}
        for min_hits in (1, 2):
            n = np.count_nonzero(counts >= min_hits, axis=0)
            for g, ng in enumerate(n):
                rows.append(dict(rule=rule, group_id=g, min_active_members=min_hits,
                                 available_positions=int(ng), group_size=14))
            rule_stats[str(min_hits)] = dict(
                quantiles={str(q): float(np.quantile(n, q)) for q in (0, .01, .05, .1, .25, .5, .75, .9, .95, 1)},
                sufficient={str(N): int(np.count_nonzero(n >= N)) for N in (32, 64, 128, 256, 512)},
                zero_support=int(np.count_nonzero(n == 0)))
        summary['rules'][rule] = rule_stats
        del counts
    with open(OUT / 'per_group_position_support.csv', 'w') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary['files'] = {'per_group_position_support.csv': sha(OUT / 'per_group_position_support.csv')}
    write_json(OUT / 'support_only_summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

def freeze():
    """Persist the root's explicit freeze, after binary support and before spectra."""
    p = OUT / 'frozen_config.json'
    if p.exists():
        raise FileExistsError('Never overwrite a frozen analysis definition')
    spec = dict(
        schema='group_hit_raw_hidden_covariance_spectrum_v1', frozen_utc=now(),
        processing_agent='Codex /root/raw_hidden_spectrum',
        authority='Root explicit collaboration instruction: anyhit>=1, N128, original m14 same/mixed all1119, seed20261016; no hidden spectra seen before this freeze',
        source_cache=str(CACHE), source_cache_sha256='d37dbcd979067b83bc5088b25c1fbb251fac8e1b98cef8c97bc35d4f58d98e83',
        source_manifest=str(CACHE.parent / 'cache_manifest.json'),
        source_scope='Existing adapter EVAL cache, original CrossCoder TRAIN source bin local-shard_2_of_10_shard_00000247_processed.bin. Not original structure V or the contribution-spectrum sampled V positions.',
        original_document_independence='UNKNOWN',
        layer_model_one_based=28, layer_model_zero_based=27,
        matrix_object='Raw cached Qwen3 block28 residual-post before final RMSNorm, shape N128 x hidden1024; no CrossCoder reconstruction, decoder, coefficients or parameter matrices',
        hidden_storage_dtype='BF16', arithmetic_dtype='FP64',
        group_size=14, groups_per_rule=1119, pool_size=15666,
        rules=dict(same_frequency='Original D-log-frequency adjacent groups, not original phi relationship groups',
                   mixed_frequency='Original one-from-each-of14 equal-count D-frequency band groups'),
        hit_rule='Any member of the group occurs in the positive gated cached CrossCoder latent event CSR at that exact position; at least1 member; no alternative thresholds in the spectrum comparison',
        source_positions=523136, sample_N_per_group=128, sampling_seed=20261016,
        sampling='No replacement. SHA256(sorted group members bytes + seed) gives group key; SplitMix64(key XOR absolute cached position_id) gives fixed pseudorandom priorities; smallest128 priorities with absolute-position tie break. Priority selection uses no hidden values.',
        center='Subtract the position mean from each original hidden coordinate separately in each sampled group matrix',
        covariance='H_centered.T @ H_centered/(128-1), represented equivalently by its 128x128 row Gram eigenvalues. Total dimension1024, centered sample rank<=127; remaining>=897 zero directions are a sampling rank limit, not model capacity.',
        normalized='Per group lambda_j/sum(lambda), then equal-weight average within each rule. First share per group retained, never replace zero total variance by0 share.',
        insufficient='If available<128 retain row in support/metrics but no spectrum; do not change grouping or pool. Current pre-spectrum support all1119 per rule sufficient.',
        inference='Descriptive selection-associated input representation distribution. Input sets differ across groups/rules; positions overlap and share contexts. No independent-group CI/p-value or frequency/learning/capacity causal claim.',
        forbidden_operations=['new model forward', 'training', 'checkpoint load', 'decoder load', 'CrossCoder reconstruction', 'outcome-based grouping or sampling'],
        files={str(GROUPS / (r + '_members.npy')): sha(GROUPS / (r + '_members.npy')) for r in ('same_frequency', 'mixed_frequency')},
        support_only_summary_sha256=sha(OUT / 'support_only_summary.json'),
        script_sha256=sha(__file__))
    write_json(p, spec)
    print('FROZEN', p)

def splitmix64(x):
    with np.errstate(over='ignore'):
        x = x + np.uint64(0x9E3779B97F4A7C15)
        x = (x ^ (x >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        x = (x ^ (x >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
        return x ^ (x >> np.uint64(31))

def select_positions(available, members, absolute_ids, N, seed):
    payload = np.sort(members).astype('<i8').tobytes() + int(seed).to_bytes(8, 'little')
    key = np.uint64(int.from_bytes(hashlib.sha256(payload).digest()[:8], 'little'))
    priority = splitmix64(absolute_ids[available].astype(np.uint64) ^ key)
    candidate = np.argpartition(priority, N - 1)[:N]
    boundary = priority[candidate].max()
    # Stable, deterministic collision handling, even if a boundary collision occurs.
    candidate = np.flatnonzero(priority <= boundary)
    order = np.lexsort((absolute_ids[available[candidate]], priority[candidate]))[:N]
    return np.sort(available[candidate[order]])

def spectrum(H):
    Hc = H - H.mean(axis=0, keepdims=True)
    gram = (Hc @ Hc.T) / (len(H) - 1)
    vals = np.linalg.eigvalsh(gram)[::-1]
    negative = float(vals.min())
    trace = float(np.square(Hc).sum() / (len(H) - 1))
    assert negative >= -max(1., trace) * 1e-10
    assert abs(vals.sum() - trace) <= max(1., trace) * 1e-10
    vals = np.maximum(vals, 0.)
    result = np.zeros(H.shape[1], dtype=np.float64)
    result[:len(vals)] = vals
    norm = result / vals.sum() if vals.sum() > 0 else np.full_like(result, np.nan)
    return result, norm, trace, negative, Hc

def compute():
    config_path = OUT / 'frozen_config.json'
    cfg = json.loads(config_path.read_text())
    assert cfg['script_sha256'] == sha(__file__), 'Script changed after freeze'
    for p, expected in cfg['files'].items():
        assert sha(p) == expected
    torch.set_num_threads(1)
    N = cfg['sample_N_per_group']
    cache = torch.load(CACHE, map_location='cpu', mmap=True, weights_only=False)
    abs_ids = cache['position_id'].numpy()
    contexts = cache['block_id'].numpy()
    assert len(np.unique(abs_ids)) == len(abs_ids)
    metric_rows = []
    summary = dict(status='COMPLETE', created_utc=now(),
                   processing_agent='Codex /root/raw_hidden_spectrum',
                   definition_sha256=sha(config_path), groups_per_rule=1119,
                   sample_N_per_group=N, hidden_dimension=1024, maximum_sample_rank=N-1,
                   source_positions=len(abs_ids), source_contexts=len(np.unique(contexts)), rules={})
    numerical = dict(gram_trace=True, significant_negative_eigenvalues=False,
                     direct_covariance_comparisons=[], synthetic_comparison={})
    rng = np.random.default_rng(519618)
    synthetic = rng.normal(size=(N, 1024)) @ np.diag(np.linspace(.1, 2., 1024))
    sv, sn, st, _, Hcs = spectrum(synthetic)
    direct_s = np.linalg.eigvalsh(Hcs.T @ Hcs/(N-1))[::-1]
    synthetic_error = float(np.max(np.abs(sv-direct_s)))
    assert synthetic_error < 1e-9
    numerical['synthetic_comparison'] = dict(shape=[N, 1024], direct_covariance_max_eigenvalue_absolute_error=synthetic_error)
    for rule in ('same_frequency', 'mixed_frequency'):
        members = load_members(rule)
        counts = mapped_counts(cache, members)
        spectra = np.full((len(members), 1024), np.nan)
        normalized = np.full_like(spectra, np.nan)
        sampled = np.full((len(members), N), -1, dtype=np.int64)
        sample_absolute = np.full_like(sampled, -1)
        context_support = []
        support = []
        for g, group in enumerate(members):
            avail = np.flatnonzero(counts[:, g] >= 1)
            support.append(len(avail))
            row = dict(rule=rule, group_id=g, group_size=len(group),
                       available_hit_positions=len(avail), requested_positions=N,
                       sampled_positions=0, sampled_contexts=0, total_variance='',
                       first_direction_share='', status='INSUFFICIENT')
            if len(avail) >= N:
                idx = select_positions(avail, group, abs_ids, N, cfg['sampling_seed'])
                assert len(np.unique(idx)) == N
                assert np.all(counts[idx, g] >= 1)
                sampled[g] = idx
                sample_absolute[g] = abs_ids[idx]
                H = cache['hidden'][torch.from_numpy(idx)].float().numpy().astype(np.float64)
                vals, norm, trace, neg, Hc = spectrum(H)
                spectra[g] = vals
                normalized[g] = norm
                nc = len(np.unique(contexts[idx])); context_support.append(nc)
                row.update(sampled_positions=N, sampled_contexts=nc,
                           total_variance=trace,
                           first_direction_share=float(norm[0]) if trace > 0 else '',
                           status='ESTIMABLE' if trace > 0 else 'ZERO_VARIANCE')
                if g == 0:
                    direct = np.linalg.eigvalsh(Hc.T @ Hc/(N-1))[::-1]
                    err = float(np.max(np.abs(vals-direct)))
                    relative = err / max(1., trace)
                    assert relative < 1e-10
                    numerical['direct_covariance_comparisons'].append(dict(
                        rule=rule, group_id=g, shape=[N, 1024], trace=trace,
                        direct_covariance_max_eigenvalue_absolute_error=err,
                        normalized_by_trace_error=relative))
            metric_rows.append(row)
            if g % 200 == 0:
                print(rule, g, row['status'], flush=True)
        np.savez_compressed(OUT / (rule + '_raw_hidden_spectra.npz'),
                            eigenvalues=spectra, normalized=normalized,
                            sampled_cache_row=sampled, sampled_absolute_position_id=sample_absolute,
                            members=members)
        valid = np.isfinite(normalized[:, 0])
        use_idx = sampled[sampled >= 0]
        occurrence = np.bincount(use_idx, minlength=len(abs_ids))
        observed = occurrence[occurrence > 0]
        summary['rules'][rule] = dict(
            groups=len(members), estimable_groups=int(valid.sum()),
            insufficient_groups=int(sum(r['rule']==rule and r['status']=='INSUFFICIENT' for r in metric_rows)),
            zero_variance_groups=int(sum(r['rule']==rule and r['status']=='ZERO_VARIANCE' for r in metric_rows)),
            source_hit_positions_quantiles={str(q):float(np.quantile(support,q)) for q in (0,.25,.5,.75,1)},
            sample_contexts_quantiles={str(q):float(np.quantile(context_support,q)) for q in (0,.25,.5,.75,1)},
            first_direction_share_mean=float(np.nanmean(normalized[:,0])),
            first_direction_share_median=float(np.nanmedian(normalized[:,0])),
            first_direction_share_quantiles={str(q):float(np.nanquantile(normalized[:,0],q)) for q in (0,.05,.25,.5,.75,.95,1)},
            total_variance_mean=float(np.nanmean(spectra.sum(1))),
            total_sampled_group_position_slots=int(len(use_idx)),
            unique_sampled_source_positions=int(len(observed)),
            source_position_reuse_maximum=int(observed.max()),
            source_position_reuse_median=float(np.median(observed)))
        del counts
    with open(OUT / 'per_group_raw_hidden_metrics.csv', 'w') as f:
        w = csv.DictWriter(f, fieldnames=list(metric_rows[0])); w.writeheader(); w.writerows(metric_rows)
    summary['descriptive_mean_first_share_same_minus_mixed'] = (
        summary['rules']['same_frequency']['first_direction_share_mean'] -
        summary['rules']['mixed_frequency']['first_direction_share_mean'])
    summary['files'] = {p.name:dict(bytes=p.stat().st_size, sha256=sha(p))
                        for p in OUT.glob('*_raw_hidden_spectra.npz')}
    summary['files']['per_group_raw_hidden_metrics.csv'] = dict(
        bytes=(OUT/'per_group_raw_hidden_metrics.csv').stat().st_size,
        sha256=sha(OUT/'per_group_raw_hidden_metrics.csv'))
    numerical['source_hidden_unchanged'] = 'Read-only mmap, no in-place hidden operation; gathered matrices cast to FP64 before centering'
    numerical['cached_BF16_values_upcast_exact'] = True
    numerical['spectra_unit_sum_max_error'] = float(max(
        np.max(np.abs(np.load(OUT / (r+'_raw_hidden_spectra.npz'))['normalized'].sum(1)-1))
        for r in ('same_frequency','mixed_frequency')))
    write_json(OUT / 'numerical_qualification.json', numerical)
    write_json(OUT / 'raw_hidden_summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=['support', 'freeze', 'compute'])
    args = ap.parse_args()
    globals()[args.command]()
