#!/usr/bin/env python3
"""Independent fixed-population, SVD-removal and provenance audit.

No training/model forward. One saved raw-H N case supplies an independent
qualification where producer direct full covariance checks covered only R/F.
"""
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import torch

E = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
R = E / 'analysis/report_spectrum/20261016_phi_input_spectrum'
MAPS = E / 'analysis/relation_learning/20261015T164000Z/data_eval512/route_maps.npz'


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def splitmix(x):
    with np.errstate(over='ignore'):
        x = x + np.uint64(0x9E3779B97F4A7C15)
        x = (x ^ (x >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        x = (x ^ (x >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
        return x ^ (x >> np.uint64(31))


def main():
    cfg = read(R / 'frozen_config.json')
    script = E / 'analysis_tools/report_spectrum/phi_input_hidden.py'
    assert sha(script) == cfg['script_sha256']
    for path, digest in cfg['files'].items():
        assert sha(path) == digest
    maps = np.load(MAPS)
    winners = np.load(R / 'winning_group_labels.npz')
    masks = np.load(R / 'common_masks.npz')
    selection = read(R / 'plot_selection.json')
    metrics = list(csv.DictReader((R / 'per_group_input_hidden_metrics.csv').open()))
    poprows = list(csv.DictReader((R / 'population_summary.csv').open()))
    paired = list(csv.DictReader((R / 'paired_group_contrasts.csv').open()))
    summary = read(R / 'phi_input_hidden_summary.json')
    arrays = {c: np.load(R / (c + '_input_hidden_spectra.npz')) for c in ('R', 'F', 'N')}
    main_ids = np.array(cfg['main_support_group_ids'])
    rn_ids = np.array(cfg['RN_support_group_ids'])
    assert np.array_equal(main_ids, selection['group_ids'])
    assert np.array_equal(np.flatnonzero(masks['RFN_estimable_original_and_residual']), main_ids)
    assert np.array_equal(np.flatnonzero(masks['RN_estimable_original_and_residual']), rn_ids)
    assert len(main_ids) == 145 and len(rn_ids) == 161
    sizes = maps['sizes']
    abspos = winners['absolute_position_id']
    contexts = winners['context_id']
    checks = {}
    drop_error = 0.0
    for c in ('R', 'F', 'N'):
        a = arrays[c]
        supported = a['support_qualified']
        assert np.array_equal(supported, a['estimable_original'])
        assert np.array_equal(supported, a['estimable_residual'])
        assert np.array_equal(a['group_size'], sizes)
        assert np.isnan(a['eigenvalues_original'][~supported]).all()
        assert np.isnan(a['eigenvalues_residual'][~supported]).all()
        assert np.all(a['sampled_cache_row'][~supported] == -1)
        context_peak = []
        for g in np.flatnonzero(supported):
            idx = a['sampled_cache_row'][g]
            assert len(idx) == len(np.unique(idx)) == 128
            assert np.all(winners[c][idx] == g)
            assert np.array_equal(a['sampled_absolute_position_id'][g], abspos[idx])
            available = np.flatnonzero(winners[c] == g)
            members = np.flatnonzero(maps['labels_' + c] == g)
            payload = np.sort(members).astype('<i8').tobytes() + int(cfg['sampling_seed']).to_bytes(8, 'little')
            key = np.uint64(int.from_bytes(hashlib.sha256(payload).digest()[:8], 'little'))
            priority = splitmix(abspos[available].astype(np.uint64) ^ key)
            # Independent full-sort selection instead of producer argpartition.
            expected = np.sort(available[np.lexsort((abspos[available], priority))[:128]])
            assert np.array_equal(idx, expected)
            original = a['eigenvalues_original'][g]
            residual = a['eigenvalues_residual'][g]
            assert np.all(original >= 0) and np.all(residual >= 0)
            assert np.allclose(a['normalized_original'][g], original / original.sum())
            assert np.allclose(a['normalized_residual'][g], residual / residual.sum())
            err = float(np.max(np.abs(original[1:128] - residual[:127]))) / a['original_trace'][g]
            drop_error = max(drop_error, err)
            assert err < 1e-12
            assert np.isclose(a['original_trace'][g] - a['removed_trace'][g], a['residual_trace'][g], rtol=1e-12)
            row = next(x for x in metrics if x['condition'] == c and int(x['group_id']) == g)
            assert np.isclose(float(row['first_share_original']), a['normalized_original'][g, 0])
            assert np.isclose(float(row['first_share_residual']), a['normalized_residual'][g, 0])
            _, count = np.unique(contexts[idx], return_counts=True)
            assert np.isclose(float(row['largest_context_position_fraction']), count.max()/128)
            if g in set(main_ids):
                context_peak.append((int(g), float(count.max()/128), len(count)))
        for state in ('original', 'residual'):
            assert np.isclose(arrays[c]['normalized_' + state][main_ids, 0].mean(), summary['main_population'][c]['first_share_' + state + '_mean'])
        checks[c] = {'supported_groups': int(supported.sum()),
                     'missing_groups': int((~supported).sum()),
                     'main_original_mean': float(a['normalized_original'][main_ids, 0].mean()),
                     'main_residual_mean': float(a['normalized_residual'][main_ids, 0].mean()),
                     'all_supported_hash_selection_exact': True,
                     'main_maximum_single_context_fraction': max(x[1] for x in context_peak),
                     'main_groups_with_single_context_fraction_above_10pct': [x[0] for x in context_peak if x[1] > .1]}
    for row in paired:
        ids = main_ids if row['population'] == 'main_RFN' else rn_ids
        stratum = row['stratum']
        if stratum != 'all':
            ids = np.array([g for g in ids if ('small' if sizes[g] <= 3 else 'medium' if sizes[g] <= 19 else 'large') == stratum])
        c = row['contrast'][-1]
        state = row['state']
        diff = arrays['R']['normalized_' + state][ids, 0] - arrays[c]['normalized_' + state][ids, 0]
        assert np.isclose(diff.mean(), float(row['mean_first_share_difference']))
        assert int((diff < 0).sum()) == int(row['R_lower_groups'])
        assert int((diff > 0).sum()) == int(row['R_higher_groups'])
    # One independent actual N-arm full SVD/projection qualification.
    torch.set_num_threads(1)
    cache = torch.load(cfg['cache'], map_location='cpu', mmap=True, weights_only=False)
    g = int(main_ids[0])
    idx = arrays['N']['sampled_cache_row'][g]
    h = cache['hidden'][torch.from_numpy(idx)].float().numpy().astype(np.float64)
    hc = h - h.mean(axis=0)
    u, sigma, vt = np.linalg.svd(hc, full_matrices=False)
    expected_original = sigma**2/127
    hr = hc - sigma[0] * np.outer(u[:, 0], vt[0])
    expected_residual = np.linalg.svd(hr, compute_uv=False)**2/127
    scale = float(np.square(hc).sum()/127)
    err_orig = float(np.max(np.abs(expected_original - arrays['N']['eigenvalues_original'][g, :128]))/scale)
    err_res = float(np.max(np.abs(expected_residual - arrays['N']['eigenvalues_residual'][g, :128]))/scale)
    assert max(err_orig, err_res) < 1e-12
    restricted = [g for g in main_ids if all(float(next(x for x in metrics if x['condition'] == c and int(x['group_id']) == g)['largest_context_position_fraction']) <= .1 for c in ('R','F','N'))]
    assert len(restricted) == 136
    sensitive = {c: {state: float(arrays[c]['normalized_' + state][restricted, 0].mean()) for state in ('original','residual')} for c in ('R','F','N')}
    result = {
        'status': 'PASS_RESULT_IDENTITY_AND_BOUNDED_INTERPRETATION',
        'processing_agent': 'Codex /root/spectrum_audit',
        'definition_sha256': sha(R / 'frozen_config.json'), 'script_sha256': sha(script),
        'checks': checks,
        'main_population_groups': 145, 'main_population_members': int(sizes[main_ids].sum()),
        'main_member_fraction': float(sizes[main_ids].sum()/sizes.sum()),
        'RN_population_groups': 161, 'RN_population_members': int(sizes[rn_ids].sum()),
        'original_and_residual_use_identical_rows_and_population': True,
        'no_post_outcome_endpoint_selection': 'Frozen support masks match all resulting common estimable masks; zero-variance additions0',
        'maximum_residual_drop_first_lambda_relative_error': drop_error,
        'independent_actual_N_group_SVD_check': {'group_id': g, 'original_error_by_trace': err_orig, 'residual_error_by_trace': err_res},
        'posthoc_context_10pct_diagnostic': {'groups': 136, 'means': sensitive, 'boundary': 'Posthoc existing-metric sensitivity only. Does not match all text composition or establish independent documents.'},
        'mandatory_interpretation_cn': '主145共同组内R原谱与去各自PC1后的残谱第一占比平均较低，差异不只局限于首方向，但仍是固定胜组规则选择出的输入关联。R-F与R-N的大小分层方向不一致，不能概括所有组或所有大小。主集合只覆盖63.84%成员，不能写全部186关系组。',
        'stratum_caveats': ['R-F中组原与残均反向，原大组反向、残大组近0', 'R-N原中组反向、残中组接近0；大组残差更低', '逐组删除自己的PC1不是删除同一个common方向'],
        'non_claims': ['phi因果', '频率单变量因果', '模型容量', '学习相容或收益', '新的独立文档确认', '先前m14同频混频方案的同一实验']
    }
    (R / 'audit/result_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
