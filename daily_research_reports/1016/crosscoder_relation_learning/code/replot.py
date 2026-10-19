#!/usr/bin/env python3
"""Replot this frozen evidence package with NumPy + Matplotlib only.

No model, cache, PyTorch or GPU is needed. Default output is ../figures.
The main figure functions are AST-extracted from analysis_learning.py; response
uses its plotting block only. Centering metrics use the equivalent saved-CSV
plot from plot_centering_control.py. No statistical inference is rerun here.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLORS={'R':'#3264a0','F':'#d88335','N':'#438968'}
MASTER_PLOT_SOURCE_SHA256='06a3d1c3e7952f91078d3270046818a8a3f3442adf29bbeb97a756b086d3f414'
CENTERING_PLOT_SOURCE_SHA256='109c33b197dcbc9cc8f11b57cf149b3daf087dc43e5518b695615fdb92635044'
EXTRACTED_FUNCTION_SOURCE_SHA256={'save': '267c0325877d6506b001207d6fba72763e13170655fede73a41113d95727402b', 'unavailable': 'ae2668fea7b0b6780bfe6e22fca4e9f4fa6ed24bb621856bdc9d2e86de7d465e', 'structure_figure': '018ee3ceceb4877d8ea184fae241efa1077d16ccb158fbc89090e626f35c6c1c', 'direction_figure': '40fb742df0a1c5de1d4bd54e651e9970eaa7ad01e72735c9b51211555f514c5d', 'learning_figures': 'cf1bf4db3c049fa736f774d0782aaf9b158fb39f1bd08269cc7cd1b50193a03c', 'intervention_figure': '40999605bfab3998faa1f357b692147843e6f3b676c97ea97236c24b94d75aec', 'response_figure': '74a1724f72d7101c791fdc699ef0b8bb70c67c1c5dae2effa9a1cd6c0859e451'}

def read_json(path):
    return json.loads(Path(path).read_text())

def read_csv(path):
    with open(path,newline='') as handle:
        return list(csv.DictReader(handle))

def typed_rows(path):
    result=[]
    for row in read_csv(path):
        converted={}
        for key,value in row.items():
            if value=='':converted[key]=None;continue
            try:converted[key]=int(value);continue
            except ValueError:pass
            try:converted[key]=float(value);continue
            except ValueError:converted[key]=value
        result.append(converted)
    return result

def file_sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as handle:
        for chunk in iter(lambda:handle.read(8<<20),b''):h.update(chunk)
    return h.hexdigest()
def save(fig, root, name, manifest, metadata):
    root.mkdir(parents=True, exist_ok=True)
    for ext in ('png', 'pdf', 'svg'):
        fig.savefig(root / f'{name}.{ext}', dpi=180, bbox_inches='tight')
    plt.close(fig)
    manifest[name] = metadata

def unavailable(ax, label):
    ax.text(0.5, 0.5, label, ha='center', va='center', transform=ax.transAxes, wrap=True, color='#666666')
    ax.set_xticks([])
    ax.set_yticks([])

def structure_figure(root, figdir, manifest):
    s = root / 'structure'
    (fig, ax) = plt.subplots(2, 2, figsize=(11, 8.5))
    meta = {}
    controls = s / 'full_group_controls.csv'
    summary = s / 'full_repair_summary.json'
    if controls.exists() and summary.exists():
        rows = read_csv(controls)
        sizes = np.array([int(r['size']) for r in rows])
        real = np.array([float(r['observed_strict_SD']) for r in rows])
        ctrl = np.array([float(r['meanmatched_strict_SD']) for r in rows])
        weights = [np.ones(len(rows)) / len(rows), sizes / sizes.sum()]
        for (j, w) in enumerate(weights):
            ax[0, 0].bar([j * 3, j * 3 + 1], [w @ real, w @ ctrl], color=['#3264a0', '#888888'], width=0.8)
            for (x, y) in [(j * 3, w @ real), (j * 3 + 1, w @ ctrl)]:
                ax[0, 0].text(x, y + 0.012, f'{y:.3f}', ha='center', fontsize=9)
        ax[0, 0].set_xticks([0.5, 3.5], ['Group equal', 'Member weighted'])
        ax[0, 0].set_ylabel('Within-group SD of log10 frequency (dex)')
        ax[0, 0].set_title('Full cache: actual / mean-matched control\n186/186 groups qualified')
        from matplotlib.patches import Patch
        ax[0, 0].legend(handles=[Patch(color='#3264a0', label='Actual'), Patch(color='#888888', label='Mean-matched control')], fontsize=8)
        sm = read_json(summary)
        keys = ['small_size2_3', 'medium_size4_19', 'large_size20plus']
        x = np.arange(3)
        ax[0, 1].bar(x - 0.18, [sm[k]['delta_groupweighted'] for k in keys], 0.36, label='Group equal', color='#3264a0')
        ax[0, 1].bar(x + 0.18, [sm[k]['delta_memberweighted'] for k in keys], 0.36, label='Member weighted', color='#7daccb')
        ax[0, 1].axhline(0, color='#333333', lw=0.8)
        ax[0, 1].set_xticks(x, ['2-3 members', '4-19 members', '20+ members'])
        ax[0, 1].set_ylabel('Actual minus matched SD (dex)')
        ax[0, 1].set_title('Effect by group size; lower = more similar')
        ax[0, 1].legend(fontsize=8)
        meta['full_cache_summary'] = str(summary)
    else:
        unavailable(ax[0, 0], 'Full-cache controls NOT COMPLETED')
        unavailable(ax[0, 1], 'Size strata NOT COMPLETED')
    repaired = s / 'triple_counting_repair' / 'null_results.json'
    nullfile = repaired if repaired.exists() else s / 'null_results.json'
    if nullfile.exists():
        null = read_json(nullfile)
        draws = null.get('draws', [])
        obs = null.get('observed', {})
        status = null.get('status', 'UNKNOWN')
        for (axis, key, label) in [(ax[1, 0], 'T_a', 'Matched-community member Jaccard\n(group-equal mean)'), (ax[1, 1], 'T_b_smoothed', 'SD difference (Jeffreys-smoothed dex)')]:
            values = [r[key] for r in draws if isinstance(r, dict) and r.get(key) is not None]
            missing = len(draws) - len(values)
            if missing:
                unavailable(axis, f'{key}: NA in {missing}/{len(draws)} null draws\nNo valid-only reference distribution')
            elif values and obs.get(key) is not None:
                axis.hist(values, bins=min(15, len(values)), color='#999999', alpha=0.8, label=f'Null B={len(values)}')
                axis.axvline(obs[key], color='#3264a0', lw=2, label=f'Actual {obs[key]:.3f}')
                axis.set_xlabel(label)
                axis.set_ylabel('Randomization draws')
                axis.legend(fontsize=8)
                complete = null.get('B_completed', len(draws)) == null.get('B_requested', 99)
                axis.set_title('4096 positions/side: bounded pipeline null' + ('' if complete else '\nPARTIAL snapshot'))
            else:
                unavailable(axis, f'Bounded null: {status}\nNo eligible reference distribution')
        meta['bounded_null_summary'] = str(nullfile)
        meta['bounded_scope'] = '4096 positions/side; cannot calibrate full-cache score'
    else:
        unavailable(ax[1, 0], 'Bounded null NOT COMPLETED')
        unavailable(ax[1, 1], 'Bounded null NOT COMPLETED')
    fig.tight_layout()
    save(fig, figdir, 'figure1_structure', manifest, meta)

def direction_figure(root, figdir, manifest):
    auxroot = root / 'data' / 'first_direction'
    if not (auxroot / 'heatmap_data.npz').exists():
        auxroot = root / 'first_direction'
    path = auxroot / 'heatmap_data.npz'
    if not path.exists():
        return {'status': 'NOT_COMPLETED', 'expected': str(path)}
    d = np.load(path)
    summary = read_json(auxroot / 'summary.json')
    provenance_file = auxroot / 'figures/provenance.json'
    provenance = read_json(provenance_file) if provenance_file.exists() else {}
    (fig, axes) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    maximum = max(d['z_original'].max(), d['z_removed'].max())
    diff = max(abs(d['z_difference'].min()), abs(d['z_difference'].max()))
    for (ax, key, title) in zip(axes, ['z_original', 'z_removed', 'z_difference'], ['Original gated shared latent', 'After removing per-layer first direction', 'Removed minus original']):
        im = ax.imshow(d[key], aspect='auto', interpolation='nearest', cmap='RdBu_r' if key == 'z_difference' else 'viridis', vmin=-diff if key == 'z_difference' else 0, vmax=diff if key == 'z_difference' else maximum)
        ticks = np.arange(len(d['feature_ids']))
        ax.set_yticks(ticks, [str(i) for i in d['feature_ids'][ticks]], fontsize=6)
        ax.set_ylabel('Fixed feature ID')
        ax.set_title(title)
        fig.colorbar(im, ax=ax, label='Gated activation z')
    axes[-1].set_xlabel('Same ordered text prediction position t (first 256 measured positions)')
    fig.suptitle(f"Fixed 32 shared-latent features, 256 plotted positions; full measurement N={summary['measurement_positions']:,}", fontsize=11)
    fig.tight_layout()
    save(fig, figdir, 'figure2_direction_sensitivity', manifest, {'heatmap_source': str(path), 'summary': str(auxroot / 'summary.json'), 'feature_selection': provenance.get('feature_selection', 'see source aux_direction.py'), 'feature_selection_provenance': str(provenance_file), 'fixed_feature_ids': d['feature_ids'].tolist(), 'measurement_positions': summary['measurement_positions'], 'plotted_positions': d['z_original'].shape[1], 'no_random_direction_control': True})
    return {'status': 'COMPLETE'}

def learning_figures(root, figdir, manifest, rows, endpoints, loads, cfg):
    if not rows:
        return
    (fig, axes) = plt.subplots(1, 2, figsize=(12, 4.6))
    for (ax, key, title) in zip(axes, ['low_loss', 'overall'], ['Fixed low-feature conditional loss', 'Overall next-token loss']):
        initial = next((r[key] for r in rows if r['step'] == 0))
        ax.axhline(initial, color='#666666', ls='--', lw=1.3, label='Frozen base (zero adapter)')
        for arm in ('R', 'F', 'N'):
            rr = [r for r in rows if r['arm'] == arm]
            steps = sorted({int(r['tokens_seen']) for r in rr})
            for seed in cfg['paired_seeds']:
                per = sorted([r for r in rr if r['seed'] == seed], key=lambda r: r['tokens_seen'])
                ax.plot([r['tokens_seen'] for r in per], [r[key] for r in per], color=COLORS[arm], lw=0.8, alpha=0.35)
            means = [np.mean([r[key] for r in rr if r['tokens_seen'] == s]) for s in steps]
            ax.plot(steps, means, color=COLORS[arm], lw=2.3, label=arm)
        ax.set_title(title)
        ax.set_xlabel('Cumulative valid training prediction tokens')
        ax.set_ylabel('NTP loss (nat)')
        ax.legend()
        ax.grid(alpha=0.15)
    fig.tight_layout()
    save(fig, figdir, 'figure3_learning_curves', manifest, {'source': str(root / 'analysis_outputs/learning_metrics.csv'), 'thin_lines': 'individual trained seeds', 'thick_lines': 'arithmetic seed mean', 'frozen_baseline': 'initial zero-adapter loss, identical all routes/seeds', 'evaluation_set': 'fixed across checkpoints and conditions'})
    changes = read_csv(root / 'analysis_outputs/zero_reference_changes.csv')
    (fig, axes) = plt.subplots(1, 3, figsize=(13, 4.5))
    for (ax, metric, title) in zip(axes, ['low', 'overall', 'high'], ['Low-feature conditional', 'Overall NTP', 'High-feature conditional']):
        for (j, arm) in enumerate(('R', 'F', 'N')):
            rr = [r for r in changes if r['metric'] == metric and r['arm'] == arm]
            values = [float(r['final_minus_initial_nat']) for r in rr]
            if values:
                ax.bar(j, np.mean(values), color=COLORS[arm], alpha=0.3, width=0.65)
                ax.scatter(j + np.linspace(-0.12, 0.12, len(values)), values, color=COLORS[arm], s=30)
        ax.axhline(0, color='#333333', lw=0.9)
        ax.set_xticks(range(3), ['R', 'F', 'N'])
        ax.set_xlabel('Route condition')
        ax.set_title(title)
        ax.grid(axis='y', alpha=0.15)
    axes[0].set_ylabel('Final minus frozen-base loss (nat)\nPositive = damage relative to zero adapter')
    fig.tight_layout()
    save(fig, figdir, 'supplement_zero_reference', manifest, {'source': str(root / 'analysis_outputs/zero_reference_changes.csv'), 'quantity': 'final_minus_initial_nat; positive is worse than frozen base', 'points': 'individual paired seeds', 'bars': 'seed means'})
    if endpoints:
        (fig, axes) = plt.subplots(1, 2, figsize=(11, 4.7), sharey=True)
        for (ax, metric) in zip(axes, ['low', 'overall']):
            for (j, seed) in enumerate(cfg['paired_seeds']):
                for (c, offset, color) in [('R-F', -0.13, COLORS['F']), ('R-N', 0.13, COLORS['N'])]:
                    r = next((r for r in endpoints if r['metric'] == metric and r['contrast'] == c and (r['seed'] == seed)), None)
                    if r:
                        ax.errorbar(r['difference_nat'], j + offset, xerr=[[max(0, r['difference_nat'] - r['ci025'])], [max(0, r['ci975'] - r['difference_nat'])]], fmt='o', color=color, label=c if j == 0 else None, capsize=3)
            ax.axvline(0, color='#333333', lw=0.9)
            ax.set_xlabel('Endpoint loss difference (nat); negative favors R')
            ax.set_title('Low-feature conditional' if metric == 'low' else 'Overall NTP')
            ax.grid(axis='x', alpha=0.15)
            ax.legend()
        axes[0].set_yticks(range(len(cfg['paired_seeds'])), [str(x) for x in cfg['paired_seeds']])
        axes[0].set_ylabel('Paired training seed')
        fig.tight_layout()
        save(fig, figdir, 'figure4_paired_endpoints', manifest, {'source': str(root / 'analysis_outputs/paired_endpoints.csv'), 'interval': 'approximate 95% paired 4-consecutive-context block bootstrap, linearized fixed-feature mean; conditional on each seed; not document independent', 'no_seed_mean_ci': True})
    if loads:
        (fig, axes) = plt.subplots(1, 2, figsize=(11, 4.5))
        for (j, arm) in enumerate(('R', 'F', 'N')):
            for e in range(4):
                rr = [r for r in loads if r['arm'] == arm and r['expert'] == e]
                axes[0].bar(e + (j - 1) * 0.24, np.mean([r['fraction'] for r in rr]), 0.24, color=COLORS[arm], label=arm if e == 0 else None)
                axes[1].bar(e + (j - 1) * 0.24, np.mean([r['nonzero_gradient_updates'] for r in rr]), 0.24, color=COLORS[arm], label=arm if e == 0 else None)
        axes[0].axhline(0.25, color='#333333', ls='--', lw=0.8)
        axes[0].set_ylabel('Fraction of training tokens')
        axes[1].set_ylabel('Updates with nonzero expert gradient')
        for ax in axes:
            ax.set_xlabel('Expert ID')
            ax.set_xticks(range(4))
            ax.legend()
            ax.grid(axis='y', alpha=0.15)
        fig.tight_layout()
        save(fig, figdir, 'supplement_expert_load', manifest, {'source': str(root / 'analysis_outputs/expert_exposure.csv'), 'averaging': 'mean over paired seeds; raw per-seed values retained'})

def intervention_figure(root, figdir, manifest, effects, cfg):
    if not effects:
        return
    (fig, axes) = plt.subplots(2, 2, figsize=(11, 8), sharex=True, sharey='row')
    for (column, version) in enumerate(['raw', 'expert_norm_matched']):
        top = axes[0, column]
        ax = axes[1, column]
        for (j, arm) in enumerate(('R', 'F', 'N')):
            rr = [r for r in effects if r['arm'] == arm and r['version'] == version]
            for (k, r) in enumerate(rr):
                x = j + (k - (len(rr) - 1) / 2) * 0.16
                y = r['actual_minus_exchanged_low_decrease']
                top.scatter(x - 0.025, r['actual_mean_low_decrease'], marker='o', color=COLORS[arm], s=35)
                top.scatter(x + 0.025, r['exchanged_mean_low_decrease'], marker='x', color=COLORS[arm], s=40)
                ax.errorbar(x, y, yerr=[[max(0, y - r['ci025'])], [max(0, r['ci975'] - y)]], fmt='o', color=COLORS[arm], capsize=3)
        for axis in [top, ax]:
            axis.axhline(0, color='#333333', lw=0.9)
            axis.set_xticks(range(3), ['R', 'F', 'N'])
            axis.grid(axis='y', alpha=0.15)
        ax.set_xlabel('Training route condition')
        top.set_title('Same SGD step size' if version == 'raw' else 'Per-expert update norms matched')
        from matplotlib.lines import Line2D
        top.legend(handles=[Line2D([0], [0], marker='o', color='black', ls='', label='Actual donor route'), Line2D([0], [0], marker='x', color='black', ls='', label='Frequency-matched exchange')], fontsize=8)
    axes[0, 0].set_ylabel('One-step low-feature probe loss decrease (nat)\nPositive = improvement; each point a seed mean')
    axes[1, 0].set_ylabel('Actual minus exchanged loss decrease (nat)\nPositive = actual causes greater decrease')
    fig.suptitle('Three paired seeds left to right: ' + ', '.join((str(s) for s in cfg['paired_seeds'])), fontsize=10)
    fig.tight_layout()
    save(fig, figdir, 'figure5_local_update', manifest, {'source': str(root / 'analysis_outputs/intervention_paired_effects.csv'), 'interval': '95% paired donor/probe batch bootstrap, conditional on each trained seed', 'donor': 'frequency-bin route-label exchange preserves each expert token count', 'probe': 'original routing always fixed'})

def response_plot(root, figdir, manifest):
    source = root / 'response_decomposition'
    output = root / 'analysis_outputs'
    rows = read_csv(output / 'response_decomposition_effects.csv')
    (fig, axes) = plt.subplots(1, 2, figsize=(13, 5))
    fields = ['full_damage_nat', 'constant_only_damage_nat', 'centered_only_damage_nat', 'loss_interaction_nat']
    labels = ['Full response', 'Constant only', 'Centered only', 'Loss interaction']
    for (ax, metric, title) in zip(axes, ['overall', 'low'], ['Overall next-token loss', 'Fixed low-feature conditional loss']):
        for (j, arm) in enumerate(['R', 'F', 'N']):
            rr = [r for r in rows if r['arm'] == arm and r['metric'] == metric]
            for (k, field) in enumerate(fields):
                values = [float(r[field]) for r in rr]
                x = k + (j - 1) * 0.24
                if not values:
                    continue
                ax.bar(x, np.mean(values), width=0.22, color=COLORS[arm], alpha=0.35, label=arm if k == 0 else None)
                ax.scatter(x + np.linspace(-0.045, 0.045, len(values)), values, color=COLORS[arm], s=22)
        ax.axhline(0, color='#333333', lw=0.9)
        ax.set_xticks(range(4), labels, rotation=15, ha='right')
        ax.set_title(title)
        ax.legend()
        ax.grid(axis='y', alpha=0.15)
    axes[0].set_ylabel('Loss damage or interaction (nat)\nPositive = damage or super-additive damage')
    fig.suptitle('Frozen final adapter: TRAIN-only expert mean response decomposition; individual seed points', fontsize=11)
    fig.tight_layout()
    save(fig, figdir, 'supplement_response_decomposition', manifest, {'source': str(output / 'response_decomposition_effects.csv'), 'prediction': str(source / 'prediction.json'), 'states': 'original complete h plus full / constant-only / centered-only adapter response', 'means': 'TRAIN original-route expert means; no targets or EVAL fitting', 'interaction': 'Lfull-Lconstant-Lcentered+Lzero; effects are not assumed additive', 'boundary': 'functional response components at this fixed checkpoint; not common semantics or complete training root cause'})
    return None
def centering_metrics_figure(root,figdir,manifest):
    folder=root/'data/first_direction/centering_control'
    summary=read_json(folder/'summary.json')
    rows=typed_rows(folder/'figures/control_metrics.csv')
    labels=['Original','Raw removal','Mean preserved']
    colors=['#657786','#d97928','#218477']
    fig,axes=plt.subplots(1,3,figsize=(12,3.8),constrained_layout=True)
    for ax,key,title,ylabel in zip(axes,['mean_l0','mean_phi_same_common_edges','event_jaccard_with_original'],
          ['Activation count','Fixed-edge relation','Overlap with original code'],
          ['Active features / position','Mean phi, same estimable edges','Binary-event Jaccard']):
        values=[float(row[key]) for row in rows]
        ax.bar(np.arange(3),values,color=colors,width=.65)
        ax.set_xticks(np.arange(3),labels,rotation=20,ha='right')
        ax.set_ylabel(ylabel);ax.set_title(title,loc='left',fontweight='bold')
        ax.set_ylim(0,max(values)*1.15)
        for i,value in enumerate(values):ax.text(i,value,f'{value:.3f}',ha='center',va='bottom',fontsize=9)
    fig.suptitle(f"Posthoc centering control | same {summary['measurement_positions']:,} positions, {summary['fixed_edges_common_estimable']:,} common estimable edges",fontsize=12)
    save(fig,figdir,'supplement_centering_control',manifest,{
        'source':str(folder/'figures/control_metrics.csv'),
        'summary':str(folder/'summary.json'),
        'original_plot_source_sha256':CENTERING_PLOT_SOURCE_SHA256,
        'boundary':'preprocessing sensitivity at fixed measured positions; not common semantics or learned utility'})

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,help='Default: the figures folder beside this evidence package.')
    args=parser.parse_args()
    report=Path(__file__).resolve().parents[1]
    evidence=report/'evidence'
    output=args.output_dir.resolve() if args.output_dir else report/'figures'
    output.mkdir(parents=True,exist_ok=True)
    cfg=read_json(evidence/'config/formal_R1_8.json')
    rows=typed_rows(evidence/'analysis_outputs/learning_metrics.csv')
    endpoints=typed_rows(evidence/'analysis_outputs/paired_endpoints.csv')
    loads=typed_rows(evidence/'analysis_outputs/expert_exposure.csv')
    effects=typed_rows(evidence/'analysis_outputs/intervention_paired_effects.csv')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                         'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
    manifest={}
    structure_figure(evidence,output,manifest)
    direction_figure(evidence,output,manifest)
    learning_figures(evidence,output,manifest,rows,endpoints,loads,cfg)
    intervention_figure(evidence,output,manifest,effects,cfg)
    response_plot(evidence,output,manifest)
    centering_metrics_figure(evidence,output,manifest)
    main_names=['figure1_structure','figure2_direction_sensitivity','figure3_learning_curves',
                'figure4_paired_endpoints','figure5_local_update']
    for name in main_names:
        for ext in ['png','pdf','svg']:
            path=output/f'{name}.{ext}'
            if not path.is_file() or path.stat().st_size==0:raise RuntimeError('Missing main figure '+str(path))
    verification={'mode':'static replot from curated small evidence only','numpy':np.__version__,
                  'matplotlib':matplotlib.__version__,'no_PyTorch_or_GPU_needed':True,
                  'master_plot_source_sha256':MASTER_PLOT_SOURCE_SHA256,
                  'centering_plot_source_sha256':CENTERING_PLOT_SOURCE_SHA256,
                  'extracted_function_source_sha256':EXTRACTED_FUNCTION_SOURCE_SHA256,
                  'figures':manifest,'outputs':{p.name:{'sha256':file_sha(p),'bytes':p.stat().st_size}
                  for p in sorted(output.iterdir()) if p.suffix in ['.png','.pdf','.svg']}}
    (output/'replot_manifest.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','main_figures':len(main_names),'figure_types':len(manifest),
                      'output_dir':str(output),'numpy':np.__version__,'matplotlib':matplotlib.__version__}),flush=True)

if __name__=='__main__':main()
