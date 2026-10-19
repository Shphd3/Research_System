#!/usr/bin/env python3
"""Independently qualify production maths on synthetic data and frozen inputs.

The script does not read any measured covariance spectra or endpoint results.
"""
import csv
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

E = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
R = E / 'analysis/report_spectrum/20261016_spectrum'
SCRIPT = E / 'analysis_tools/report_spectrum/compute_spectrum.py'
OUT = Path(__file__).parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    spec = importlib.util.spec_from_file_location('spectrum_impl_audit', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rng = np.random.default_rng(20261016)
    a = rng.lognormal(size=(113, 14)) * (rng.random((113, 14)) < .2)
    d = rng.normal(size=(14, 37))
    before = a.copy()
    w, s, diag, c = module.one_spectrum(a, d)
    assert np.array_equal(before, a), 'Do not mutate the caller activation array'
    h = (a - a.mean(axis=0)) @ d
    actual = np.linalg.eigvalsh(h.T @ h / (len(h) - 1))[::-1]
    err = float(np.max(np.abs(w - actual[:14])))
    assert np.allclose(w, actual[:14], rtol=1e-11, atol=1e-10)
    assert np.allclose(s.sum(), 1)
    ws, ss, _, _ = module.one_spectrum(a, 374.3495121024576 * d)
    assert np.allclose(ws, 374.3495121024576**2 * w, rtol=1e-11)
    assert np.allclose(ss, s, rtol=1e-12)
    constant_checks = []
    for n in (113, 131072):
        const = np.tile(np.float32(1.2345678).astype(np.float64), (n, 14))
        wz, sz, dz, _ = module.one_spectrum(const, d)
        assert dz['total_variance'] == 0 and np.isnan(sz).all()
        constant_checks.append({'N': n, 'total_variance': 0.0, 'first_share_NA': True})
    x = rng.normal(size=(113, 1))
    same = np.repeat(x, 2, axis=1)
    oppose = np.array([[1., 0.], [-1., 0.]])
    wz, sz, dz, _ = module.one_spectrum(same, oppose)
    assert dz['total_variance'] == 0 and np.isnan(sz).all()
    config = json.loads((R / 'frozen_config.json').read_text())
    assert config['shuffle_seed'] == 20261016 and config['shuffle_replicates'] == 1
    assert config['sample_N'] == 131072 and config['m'] == 14
    pool = np.load(R / 'feature_pool_ordered.npy')
    group_same = np.load(R / 'same_frequency_members.npy')
    group_mixed = np.load(R / 'mixed_frequency_members.npy')
    assert len(pool) == len(np.unique(pool)) == 15666
    assert np.array_equal(group_same, pool.reshape(1119, 14))
    assert np.array_equal(group_mixed, pool.reshape(14, 1119).T)
    for groups in (group_same, group_mixed):
        assert np.array_equal(np.sort(groups.ravel()), np.sort(pool))
    rows = list(csv.DictReader((E / 'analysis/feature_frequency/20261015T143300Z/frequency.csv').open()))
    assert np.array_equal([int(x['feature_id']) for x in rows], np.arange(16384))
    positions = np.load(R / 'V_stream_position_ids.npy')
    n, nv = 131072, 5247663
    expected = ((2 * np.arange(n, dtype=np.int64) + 1) * nv) // (2*n)
    assert np.array_equal(positions, expected)
    assert len(np.unique(np.load(R / 'V_global_position_ids.npy'))) == n
    receipt = {
        'status': 'PASS_DEFINITIONS_AND_SYNTHETIC_IMPLEMENTATION',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'processing_agent': 'Codex /root/spectrum_audit',
        'production_source': str(SCRIPT), 'source_sha256': sha(SCRIPT),
        'frozen_config': str(R / 'frozen_config.json'), 'frozen_config_sha256': sha(R / 'frozen_config.json'),
        'no_empirical_spectrum_results_read': True,
        'synthetic_full_covariance_vs_small_matrix_max_abs': err,
        'synthetic_constant_checks': constant_checks,
        'synthetic_exact_decoder_cancellation': 'zero variance -> NA',
        'input_immutability': True, 'model_scale_and_normalized_share_qualification': True,
        'frozen_assignments_every_feature_exactly_once': True,
        'frozen_systematic_positions_exact': True,
        'source_review': {
            'last_decoder': 'source index13 / model block28 residual-post before final RMSNorm',
            'inverse_scale': 'saved centered TRAIN vector RMS times saved decoder; no unit normalization',
            'coefficients': 'cached gated raw ReLU z, not norm-weighted gate score',
            'no_repeated_bias_or_mean': True,
            'covariance_centering': 'explicit position centering, all fixed V rows including zero rows, ddof1',
            'exact_low_rank_identity': 'Gram^(1/2) Cz Gram^(1/2), same nonzero representation covariance eigenvalues',
            'per_group_normalization_then_group_equal_average': True,
            'support_postselection_absent': True,
            'shared_independent_feature_position_permutations': True,
            'same_versus_mixed_mean_frequency_distribution_exported': ['mean p_D', 'mean log10 p_D'],
            'no_p_values_from_one_permutation': True
        },
        'seed_history': 'Unexecuted proposal2026101603 replaced pre-outcome by formal frozen seed20261016.',
        'repairs': ['raw second moment subtraction -> explicit centered Gram for constant-column numerical safety',
                    'exact trace0 contribution covariance -> zero eigenvalues and NA ratios before tiny roundoff PSD error'],
        'boundary': 'This receipt qualifies definitions, fixed assignment/position inputs and synthetic implementation. It does not verify the empirical endpoint or turn the descriptive comparison into frequency-only causation, capacity or learning benefit.'
    }
    (OUT / 'implementation_qualification.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == '__main__':
    main()
