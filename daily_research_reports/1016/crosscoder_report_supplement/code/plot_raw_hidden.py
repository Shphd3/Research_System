#!/usr/bin/env python3
"""Plot cached raw-input covariance spectra from saved small analysis arrays."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

ROOT = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/report_spectrum/20261016_raw_hidden')
FONT = Path('/data/250010109/Research_System/daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf')

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--out', type=Path)
    ap.add_argument('--font', type=Path, default=FONT)
    a = ap.parse_args()
    out = a.out or a.root / 'figures'; out.mkdir(parents=True, exist_ok=True)
    font_manager.fontManager.addfont(str(a.font))
    fp = font_manager.FontProperties(fname=str(a.font))
    plt.rcParams.update({'font.family': fp.get_name(), 'font.size': 18,
                         'axes.titlesize': 24, 'axes.labelsize': 21,
                         'xtick.labelsize': 16, 'ytick.labelsize': 16,
                         'legend.fontsize': 18, 'figure.facecolor': 'white',
                         'axes.facecolor': 'white', 'pdf.fonttype': 42,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.titlepad': 18, 'savefig.facecolor': 'white'})
    rules = ['same_frequency', 'mixed_frequency']
    labels = ['同频组', '混频组']; colors = ['#3572B0', '#D98928']
    values = []
    curves = []
    output = []
    fig, ax = plt.subplots(figsize=(8.8, 6.6), layout='constrained')
    for rule, label, color in zip(rules, labels, colors):
        z = np.load(a.root / (rule + '_raw_hidden_spectra.npz'))
        norm = z['normalized']; valid = np.isfinite(norm[:, 0])
        v = norm[valid]; values.append(v[:, 0])
        mean = v.mean(0)
        # The theoretical centered sample rank is127. Full1024 spectra are retained
        # in NPZ/CSV; plot shows all127 estimable directions, excluding numerical
        # zero remainder from the finite-sample Gram representation.
        ax.plot(np.arange(1, 128), mean[:127], lw=3., color=color, label=label)
        for j, x in enumerate(mean):
            curves.append(dict(rule=rule, direction_index=j+1,
                               equal_group_mean_variance_share=float(x),
                               estimable_groups=int(valid.sum()),
                               displayed_in_figure=int(j<127)))
    ax.set_title('原始hidden归一化谱')
    ax.set_xlabel('方向序号'); ax.set_ylabel('方差占比')
    ax.set_xlim(1, 127); ax.set_ylim(bottom=0)
    ax.set_xticks([1, 16, 32, 64, 96, 127])
    ax.grid(axis='y', alpha=.15); ax.legend(frameon=False)
    base = out / 'figure5_raw_hidden_normalized_spectrum'
    for ext in ('png', 'pdf'):
        p = base.with_suffix('.'+ext); fig.savefig(p, dpi=240); output.append(p)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8.8, 6.6), layout='constrained')
    rng = np.random.default_rng(2026101606)
    for i, (v, color) in enumerate(zip(values, colors), 1):
        ax.scatter(i+rng.uniform(-.19, .19, len(v)), v, s=14, alpha=.2,
                   color=color, edgecolors='none')
    bp = ax.boxplot(values, positions=[1, 2], widths=.44, showfliers=False,
                    patch_artist=True, medianprops={'color':'#202020', 'lw':2.},
                    boxprops={'lw':1.8}, whiskerprops={'lw':1.5}, capprops={'lw':1.5})
    for p, color in zip(bp['boxes'], colors):
        p.set_facecolor('white'); p.set_edgecolor(color); p.set_alpha(.85)
    ax.scatter([1, 2], [v.mean() for v in values], marker='D', s=75,
               color=colors, edgecolors='white', linewidths=.8, zorder=4)
    ax.set_title('原始hidden第一方向占比')
    ax.set_xlabel('分组规则'); ax.set_ylabel('第一方向占比')
    ax.set_xticks([1, 2], labels); ax.set_xlim(.5, 2.5); ax.set_ylim(0, .7)
    ax.grid(axis='y', alpha=.15)
    base = out / 'figure6_raw_hidden_first_direction_share'
    for ext in ('png', 'pdf'):
        p = base.with_suffix('.'+ext); fig.savefig(p, dpi=240); output.append(p)
    plt.close(fig)
    with open(out / 'raw_hidden_normalized_spectrum_plot_data.csv', 'w') as f:
        w = csv.DictWriter(f, fieldnames=list(curves[0])); w.writeheader(); w.writerows(curves)
    provenance = dict(plot_script=str(Path(__file__).resolve()), plot_script_sha256=sha(__file__),
                      font_path=str(a.font), font_sha256=sha(a.font), colors=dict(zip(labels, colors)),
                      matrix='Original cached raw layer28 hidden at group-hit positions, not reconstructed contribution',
                      plot_directions=127, full_stored_directions=1024,
                      rank_note='N128 position-centered sample rank<=127. Remaining897 directions are theoretically zero; direction128 in row-Gram may contain floating-point residual.',
                      first_direction_plot='All1119 group points per rule shown; boxes median/IQR,1.5IQR whiskers; diamonds equal-group means, no inferential error bars.',
                      source_config_sha256=sha(a.root/'frozen_config.json'),
                      source_summary_sha256=sha(a.root/'raw_hidden_summary.json'),
                      outputs=[dict(path=str(p), bytes=p.stat().st_size, sha256=sha(p)) for p in output])
    (out/'plot_provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(status='COMPLETE', figures=len(output), output=str(out)), ensure_ascii=False))

if __name__ == '__main__':
    main()
