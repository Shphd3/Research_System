#!/usr/bin/env python3
"""Post-outcome descriptive context sensitivity; never changes primary samples."""
from pathlib import Path
import argparse
import csv
import datetime
import json
import numpy as np
from scipy.stats import spearmanr

DEFAULT = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/report_spectrum/20261016_phi_input_spectrum')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=DEFAULT)
    args = ap.parse_args()
    p = args.root
    main_ids = json.loads((p/'plot_selection.json').read_text())['group_ids']
    rows = list(csv.DictReader((p/'per_group_input_hidden_metrics.csv').open()))
    indexed = {(x['condition'], int(x['group_id'])): x for x in rows}
    spec = {
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'stage': 'POSTHOC_DESCRIPTIVE_CONTEXT_DIAGNOSTIC_NOT_PRIMARY',
        'primary_group_ids_unchanged': main_ids,
        'max_single_context_fraction_cut': 0.1,
        'selection': 'retain group ID only if all three sampled input sets have largest context share <=0.1; no new positions or spectrum computation',
        'reason': 'check whether observed average ordering is limited to groups dominated by one context; does not establish document independence',
    }
    # This specification is saved before reading the restricted endpoint means.
    (p/'context_diagnostic_spec.json').write_text(json.dumps(spec, indent=2)+'\n')
    kept = [g for g in main_ids if all(float(indexed[c,g]['largest_context_position_fraction']) <= 0.1 for c in 'RFN')]
    result = {
        'spec': 'context_diagnostic_spec.json', 'retained_groups': len(kept),
        'excluded_group_ids': [g for g in main_ids if g not in kept],
        'population': 'same group IDs in all conditions; unchanged original frozen samples',
        'rules': {},
    }
    for c in 'RFN':
        full = [indexed[c,g] for g in main_ids]
        restricted = [indexed[c,g] for g in kept]
        metrics = ('first_share_original', 'first_share_residual')
        current = {k: float(np.mean([float(r[k]) for r in restricted])) for k in metrics}
        current['main_group_spearman'] = {
            metric: {
                covariate: float(spearmanr([float(r[metric]) for r in full], [float(r[covariate]) for r in full]).statistic)
                for covariate in ('largest_context_position_fraction', 'group_size')
            } for metric in metrics
        }
        result['rules'][c] = current
    (p/'context_diagnostic_result.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps({'retained_groups': len(kept), 'rules': result['rules']}, indent=2))

if __name__ == '__main__':
    main()
