"""Redraw only R10 Figure2A with a shared, explicitly clipped0--15% axis."""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[name] = '2'
import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import PercentFormatter
import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, default=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030'))
parser.add_argument('--output', type=Path)
args = parser.parse_args()
source = args.source
output = args.output or source / 'presentation_variants/figure2A_zoom_20261030'
output.mkdir(parents=True, exist_ok=True)

freeze_path = source / 'freeze.json'
freeze = json.loads(freeze_path.read_text())
projection_path = source / 'analysis/all_decoder_projection.npz'
with np.load(projection_path) as data:
    band = data['per_band']
assert band.shape == (16384, 16)
assert np.allclose(band.sum(axis=1), 1, atol=1e-12)

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                     'axes.spines.top': False, 'axes.spines.right': False})
fig, axes = plt.subplots(1, 2, figsize=(14, 5.8), sharey=True)
fig.subplots_adjust(left=.065, right=.99, bottom=.255, top=.76, wspace=.10)
fig.suptitle('Unit decoder projections across the common spectrum', fontsize=16, y=.985)
colors = {'math': '#2874A6', 'biology': '#C05B38'}
rng = np.random.default_rng(10)
limit = .15
x = np.arange(16)
dictionary_mean = band.mean(axis=0)
rows = []
clipped = {}
inputs = [freeze_path, projection_path]

for ax, group in zip(axes, ('math', 'biology')):
    ids = np.array(freeze['sets']['main_' + group], dtype=int)
    values = band[ids]
    background_path = source / f'analysis/{group}_fine_matched_background.npz'
    inputs.append(background_path)
    with np.load(background_path) as data:
        background = data['mean_per_pc'].reshape(1000, 16, 64).sum(axis=2)
    low, high = np.quantile(background, [.025, .975], axis=0)
    mean = values.mean(axis=0)
    median = np.median(values, axis=0)
    assert max(mean.max(), median.max(), high.max(), dictionary_mean.max()) < limit
    clipped_counts = (values > limit).sum(axis=0)
    clipped[group] = {'members': len(ids), 'band_values_above_limit': int(clipped_counts.sum()),
                      'distinct_members_above_limit': int((values > limit).any(axis=1).sum()),
                      'counts_by_band': clipped_counts.tolist(),
                      'largest_value': float(values.max())}

    for k in x:
        jitter = rng.uniform(-.12, .12, len(ids))
        visible = values[:, k] <= limit
        ax.scatter(k + jitter[visible], values[visible, k], s=4, color=colors[group],
                   alpha=.14, edgecolors='none', rasterized=True, zorder=2)
        if clipped_counts[k]:
            ax.scatter(k, .147, marker='^', s=30, color=colors[group], zorder=6)
            ax.annotate(str(clipped_counts[k]), (k, .147), xytext=(0, -14),
                        textcoords='offset points', ha='center', va='top',
                        fontsize=8, color=colors[group])
        rows.append({'group': group, 'members': len(ids), 'PC_start': int(64*k+1),
                     'PC_end': int(64*(k+1)), 'mean_all_members': float(mean[k]),
                     'median_all_members': float(median[k]),
                     'matched_reference_low': float(low[k]),
                     'matched_reference_high': float(high[k]),
                     'whole_dictionary_mean': float(dictionary_mean[k]),
                     'above_display_limit': int(clipped_counts[k])})

    ax.fill_between(x, low, high, color='#A0A0A0', alpha=.35, zorder=3)
    ax.plot(x, mean, 'o-', color=colors[group], lw=2.2, ms=4.5, zorder=5)
    ax.plot(x, median, '--', color=colors[group], lw=2, zorder=5)
    ax.plot(x, dictionary_mean, ':', color='black', lw=1.9, zorder=5)
    ax.set_title(f'{group.title()} ({len(ids)} members)', fontsize=13, pad=12)
    ax.set_xlim(-.45, 15.45)
    ax.set_ylim(0, limit)
    ax.set_yticks(np.arange(0, .1501, .025))
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=1))
    ax.tick_params(axis='y', labelleft=True)
    ax.set_xticks(x, [f'{64*k+1}-{64*(k+1)}' for k in x], rotation=50, ha='right', fontsize=8)
    ax.set_xlabel('PC range (64 directions per band)', labelpad=8)
    ax.grid(axis='y', color='#D8D8D8', lw=.6, alpha=.65, zorder=0)
axes[0].set_ylabel('Squared projection share of complete unit decoder')

handles = [Line2D([], [], marker='o', linestyle='none', color='#607D8B', ms=4, alpha=.6,
                  label='Individual members'),
           Line2D([], [], marker='o', color='#465566', lw=2, ms=4, label='Mean (all members)'),
           Line2D([], [], linestyle='--', color='#465566', lw=2, label='Median (all members)'),
           Patch(facecolor='#A0A0A0', alpha=.35, label='Matched background 95% range'),
           Line2D([], [], linestyle=':', color='black', lw=2, label='Whole dictionary mean'),
           Line2D([], [], marker='^', linestyle='none', color='#465566', label='Count above 15%')]
fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(.5, .925), ncol=3,
           fontsize=9, frameon=False, columnspacing=2)
fig.text(.015, .055,
         'Shared y-axis: 0-15%. Triangles and numbers mark band-values above the display limit; all values remain in mean/median calculations.\n'
         f'Above-limit band-values: math {clipped["math"]["band_values_above_limit"]}, biology {clipped["biology"]["band_values_above_limit"]}. '
         'Same frozen433/527 members;60 discovery documents x160 positions; same1024-PC common basis and A01 fine-matched reference.',
         fontsize=8, va='bottom', linespacing=1.6)

for suffix in ('png', 'pdf'):
    fig.savefig(output / f'figure2A_decoder_spectrum_zoom.{suffix}', dpi=200)
plt.close(fig)
with (output / 'plot_data.csv').open('w', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
metadata = {'kind': 'presentation_only_redraw', 'y_limits': [0, limit],
            'new_model_forwards': 0, 'statistics_changed': False, 'clipped': clipped,
            'inputs': [{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs]}
(output / 'provenance.json').write_text(json.dumps(metadata, indent=2)+'\n')
print(json.dumps({'output': str(output), 'clipped': clipped}, indent=2))
