"""Explain cached R10 spectral location, overlap, and actual-use energy separately."""
import os
for key in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[key] = '2'
from pathlib import Path
import argparse
import csv
import hashlib
import json
import shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, default=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030'))
parser.add_argument('--output', type=Path)
args = parser.parse_args()
source = args.source
out = args.output or source/'presentation_variants/spectral_explanation_20261030'
out.mkdir(parents=True, exist_ok=True)
inputs = [source/'freeze.json', source/'analysis/all_decoder_projection.npz',
          source/'tables/group_reconstruction_energy.csv']
freeze = json.loads(inputs[0].read_text())
with np.load(inputs[1]) as data:
    per_pc = data['per_pc']
    per_band = data['per_band']
ids = {g: np.array(freeze['sets']['main_'+g], int) for g in ('math', 'biology')}
assert tuple(len(ids[g]) for g in ids) == (433, 527)
assert np.allclose(per_pc.sum(1), 1, atol=1e-12)
assert np.allclose(per_pc.reshape(-1, 16, 64).sum(2), per_band, atol=1e-12)
q = {g: per_pc[v].mean(0) for g, v in ids.items()}
band_mean = {g: q[g].reshape(16, 64).sum(1) for g in ids}
summary = {'new_model_forwards': 0, 'training_updates': 0, 'new_PCA': False,
           'new_selection': False, 'groups': {}, 'within_group_unit': 'member-equal',
           'added_descriptions': ['share in first256 PCs vs256/1024 dimensional baseline',
                                  'per-member peak64-PC band',
                                  'actual group-energy overlap at64-PC-band resolution']}
member_rows = []
for g, fids in ids.items():
    b = per_band[fids]
    front = b[:, :4].sum(1)
    peak = b.argmax(1)
    quarter_peak = b.reshape(-1,4,4).sum(2).argmax(1)
    first64_peak = int((peak == 0).sum())
    enriched = int((front > .25).sum())
    summary['groups'][g] = {'members': len(fids), 'PC1_64_mean': float(b[:, 0].mean()),
                           'PC1_64_median': float(np.median(b[:, 0])),
                           'PC1_256_mean': float(front.mean()),
                           'PC1_256_median': float(np.median(front)),
                           'PC1_256_above_dimensional_share_count': enriched,
                           'PC1_256_above_dimensional_share_fraction': enriched/len(fids),
                           'peak_PC1_64_count': first64_peak,
                           'peak_PC1_64_fraction': first64_peak/len(fids),
                           'peak_in_first256_count': int((peak < 4).sum()),
                           'largest_quarter_is_first_count':int((quarter_peak == 0).sum()),
                           'largest_quarter_is_first_fraction':float((quarter_peak == 0).mean()),
                           'peak_band_counts': np.bincount(peak, minlength=16).tolist()}
    for i, f in enumerate(fids):
        member_rows.append(dict(feature_id=int(f), domain_bias=g,
                                PC1_64_fraction=float(b[i, 0]),
                                PC1_256_fraction=float(front[i]),
                                PC1_256_exceeds_dimension_share=bool(front[i] > .25),
                                largest_quarter=int(quarter_peak[i]+1),
                                peak_band=int(peak[i]+1)))

bg = {}
for g in ids:
    path = source/f'analysis/{g}_fine_matched_background.npz'
    inputs.append(path)
    with np.load(path) as data:
        bg[g] = data['mean_per_pc']
observed_pc = float(np.minimum(q['math'], q['biology']).sum())
observed_band = float(np.minimum(band_mean['math'], band_mean['biology']).sum())
bg_pc = np.minimum(bg['math'], bg['biology']).sum(1)
bg_band = np.minimum(bg['math'].reshape(1000, 16, 64).sum(2),
                     bg['biology'].reshape(1000, 16, 64).sum(2)).sum(1)
assert observed_band >= observed_pc
assert np.isclose(observed_pc, 1-.5*np.abs(q['math']-q['biology']).sum())
summary['geometry_overlap'] = dict(per_PC=observed_pc, per_64PC_band=observed_band,
                                 per_PC_matched95=np.quantile(bg_pc, [.025,.975]).tolist(),
                                 per_band_matched95=np.quantile(bg_band, [.025,.975]).tolist(),
                                 reference='A01 frequency/support matched dictionary; pool includes selected')

with inputs[2].open() as stream:
    energy_rows = list(csv.DictReader(stream))
energy = {}
for domain in ids:
    energy[domain] = {}
    for group in ids:
        rr = [r for r in energy_rows if r['input_domain']==domain and r['member_group']==group]
        assert len(rr)==16 and [int(r['band']) for r in rr]==list(range(1,17))
        values = np.array([float(r['fraction']) for r in rr])
        assert np.isclose(values.sum(),1)
        energy[domain][group]=values
    summary.setdefault('actual_group_energy', {})[domain] = {
        'heldout_documents':20, 'positions_per_document':160,
        'first64_fraction':{g:float(v[0]) for g,v in energy[domain].items()},
        'first256_fraction':{g:float(v[:4].sum()) for g,v in energy[domain].items()},
        'overlap_64PC_bands':float(np.minimum(energy[domain]['math'],energy[domain]['biology']).sum()),
        'operation':'sum z times model-scale decoder first, then project, square, doc-average, normalize'}

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,
                     'axes.spines.top':False,'axes.spines.right':False})
color = {'math':'#2874A6','biology':'#C05B38'}
x=np.arange(16)
labels=[f'{64*k+1}-{64*(k+1)}' for k in x]
def band_axis(ax, ylabel, upper=.14):
    ax.set(xlim=(-.45,15.45),ylim=(0,upper),ylabel=ylabel,
           xlabel='PC range (64 directions per band)')
    ax.set_xticks(x,labels,rotation=50,ha='right',fontsize=8)
    ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
    ax.grid(axis='y',color='#DBDBDB',alpha=.6,lw=.7,zorder=0)
def finish(fig,name,foot):
    fig.text(.015,.025,foot,fontsize=8,va='bottom',linespacing=1.6)
    fig.subplots_adjust(left=.07,right=.985,top=.78,bottom=.27,wspace=.40)
    for ext in ['png','pdf']:
        fig.savefig(out/f'{name}.{ext}',dpi=200)
    plt.close(fig)

#1: the average profile and a direct count supporting the word "most".
fig,axes=plt.subplots(1,2,figsize=(14,5.5),gridspec_kw={'width_ratios':[1.45,1]})
fig.suptitle('1 | Front-of-spectrum emphasis: average shape and member coverage',fontsize=15,y=.985)
ax=axes[0]
ax.axvspan(-.45,3.45,color='#F0E4BD',alpha=.35,zorder=0)
for g in ids:
    ax.plot(x,band_mean[g],'o-',color=color[g],lw=2.3,ms=5,label=f'{g.title()} mean (n={len(ids[g])})')
ax.axhline(1/16,color='#6C6C6C',linestyle='--',lw=1.3,label='Equal-dimensional allocation:6.25%')
band_axis(ax,'Mean normalized squared projection',upper=.14)
ax.set_title('A | Same-sized bands: highest group mean at PC1-64',fontsize=11,pad=12)
ax.legend(fontsize=8.5,loc='upper right',frameon=False)
ax.text(.02,.07,'Shaded x-region: PC1-256 (25% of directions)',transform=ax.transAxes,fontsize=8,color='#7C663A')
ax=axes[1]
metrics=[('PC1_256_above_dimensional_share_fraction','PC1-256 share\nabove25%'),
         ('largest_quarter_is_first_fraction','PC1-256 largest\nof four256-PC blocks'),
         ('peak_PC1_64_fraction','PC1-64 largest\nof sixteen64-PC blocks')]
for row,(key,label) in enumerate(metrics):
    y=2-row
    for k,g in enumerate(ids):
        fraction=summary['groups'][g][key];dy=.14 if k==0 else -.14
        ax.barh(y+dy,fraction,color=color[g],height=.25)
        ax.text(fraction/2,y+dy,f'{fraction:.1%}',ha='center',va='center',color='white',fontsize=10,fontweight='bold')
ax.set(xlim=(0,1),ylim=(-.55,2.6),yticks=[2,1,0],yticklabels=[m[1] for m in metrics],
       xlabel='Fraction of members',title='B | How widespread is the front emphasis?')
ax.tick_params(axis='y',labelsize=8.5)
ax.set_xticks([0,.25,.5,.75,1]);ax.xaxis.set_major_formatter(PercentFormatter(1));ax.grid(axis='x',alpha=.2,lw=.6)
finish(fig,'evidence1_front_location',
       'Same frozen433math /527biology members;60 discovery documents x160 positions define one common1024-PC basis. No activation/norm weighting.\n'
       'First64 group means:10.03% /11.52%; first256 means:32.34% /35.07%. Bars distinguish above-dimensional share from having the largest spectral block.\n'
       'The25% reference is dimensional share, not a matched-dictionary null; unique front enrichment over the fine-matched dictionary is not established for the main set.')

#2: visualize common mass but retain the full1024-PC coefficient as the primary overlap.
fig,axes=plt.subplots(1,2,figsize=(13.2,5.4),gridspec_kw={'width_ratios':[1.65,1]})
fig.suptitle('2 | Different domain preferences, strongly overlapping spectral distributions',fontsize=15,y=.985)
ax=axes[0]
common=np.minimum(band_mean['math'],band_mean['biology'])
ax.fill_between(x,0,common,color='#9EAA9B',alpha=.6,label='Common minimum at each band')
for g in ids:
    ax.plot(x,band_mean[g],'o-',color=color[g],lw=2.2,ms=4.5,label=g.title())
band_axis(ax,'Group mean normalized squared projection',upper=.14)
ax.set_title('A | Common coverage (64-PC bands for display)',fontsize=11,pad=12)
ax.legend(fontsize=8.5,loc='upper right',frameon=False)
ax=axes[1]
for y,obs,ref in [(1,observed_pc,bg_pc),(0,observed_band,bg_band)]:
    low,high=np.quantile(ref,[.025,.975]);ax.plot([low,high],[y,y],color='#999999',lw=8,solid_capstyle='butt',zorder=1)
    ax.plot(obs,y,'o',color='#222222',ms=8,zorder=3)
    ax.annotate(f'{obs:.2%}',(obs,y),xytext=(0,14),textcoords='offset points',ha='center',fontweight='bold',fontsize=12)
ax.set(xlim=(.90,1),ylim=(-.5,1.65),yticks=[1,0],yticklabels=['1024 PCs\n(primary)','16 bands\n(coarsened)'],
       xlabel='Overlap coefficient (zoom:90%-100%)',title='B | Exact coefficient and matched reference')
ax.xaxis.set_major_formatter(PercentFormatter(1,decimals=0));ax.grid(axis='x',color='#DDDDDD',lw=.6)
fig.legend(handles=[Line2D([],[],marker='o',color='#222222',linestyle='none',label='Observed'),
                    Line2D([],[],color='#999999',lw=6,label='Matched dictionary95% range')],
           fontsize=8.5,loc='upper right',bbox_to_anchor=(.985,.92),ncol=2,frameon=False)
finish(fig,'evidence2_spectral_overlap',
       'Same433/527 frozen members and same common PCA; overlap=sum of pointwise minima of member-equal normalized squared projections.\n'
       'Overlap:94.93% at1024-PC resolution;96.86% after64-PC aggregation. Coarsening hides within-band differences; it does not replace the primary coefficient.\n'
       'Both coefficients fall inside the A01 matched reference. High absolute spectral overlap does not establish extra overlap vs background or identical directions/functions.')

#3: the same16 bands, actual cached activations and all four group/input conditions.
fig,axes=plt.subplots(1,2,figsize=(13.2,5.4),sharey=True)
fig.suptitle('3 | Actual activation-weighted group reconstruction energy',fontsize=15,y=.985)
for ax,domain in zip(axes,ids):
    ax.axvspan(-.45,.45,color='#F0E4BD',alpha=.4,zorder=0)
    for g in ids:
        v=energy[domain][g]
        ax.plot(x,v,'o-',color=color[g],lw=2.3,ms=4.5,label=f'{g.title()} group (n={len(ids[g])})')
        ax.annotate(f'{v[0]:.1%}',(0,v[0]),xytext=(10,6),textcoords='offset points',color=color[g],fontweight='bold',fontsize=11)
    band_axis(ax,'Fraction of summed-vector squared energy',upper=.60)
    ax.set_title(f'{domain.title()} inputs:20 exposed-heldout documents\nBand-energy overlap={summary["actual_group_energy"][domain]["overlap_64PC_bands"]:.2%}',fontsize=11,pad=12)
    ax.legend(fontsize=8.5,loc='upper right',frameon=False)
    ax.tick_params(axis='y',labelleft=True)
finish(fig,'evidence3_actual_energy',
       'Both member groups are evaluated on BOTH input domains;20 documents/domain x160 positions. Sum z x model-scale decoder FIRST, then project and square.\n'
       'PC1-64 contains the largest energy share in all four observed conditions (20.9%-51.9%). Equal document weights; normalized energy of each group vector.\n'
       'This is actual grouped reconstruction energy, not full-h explained variance or unit geometry. Its band-overlap68.95% /77.56% differs from unit-geometry96.86%.')

def save_csv(name,rr):
    with (out/name).open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rr[0]));writer.writeheader();writer.writerows(rr)
save_csv('member_front_summary.csv',member_rows)
save_csv('band_profiles.csv',[dict(group=g,band=int(k+1),PC_start=int(k*64+1),PC_end=int((k+1)*64),
                                  mean=float(band_mean[g][k]),median=float(np.median(per_band[ids[g],k])))
                             for g in ids for k in x])
shutil.copy2(inputs[2],out/'group_reconstruction_energy.csv')
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
provenance={'kind':'derived explanation and cache-only descriptive counts; frozen scientific owners unchanged',
            'parent_asset_id':'analysis_a15_27_04_r10_domain_member_atlas_20261030',
            'new_forwards':0,'new_training':0,'new_PCA':0,'new_selection':0,
            'script':str(Path(__file__).resolve()),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'inputs':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs]}
(out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps({'output':str(out),'summary':summary},indent=2))
