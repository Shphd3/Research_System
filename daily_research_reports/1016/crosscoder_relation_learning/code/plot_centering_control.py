#!/usr/bin/env python3
"""Fixed-order supplement for the posthoc centering control."""
import argparse
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

DEFAULT=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z/data/first_direction/centering_control')


def main(root):
    root=Path(root);d=np.load(root/'control_data.npz');s=json.loads((root/'summary.json').read_text())
    folder=root/'figures';folder.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'svg.fonttype':'none'})
    names=['z_original','z_raw_removed','z_center_preserved']
    vmax=max(float(d[k].max()) for k in names)
    difference=d['z_raw_removed']-d['z_center_preserved']
    diff_limit=float(abs(difference).max())
    fig,axes=plt.subplots(4,1,figsize=(11,12),sharex=True,sharey=True,constrained_layout=True)
    titles=['Original frozen code','Raw direction removed, original mean subtracted','Centered direction removed, mean preserved']
    for ax,key,title in zip(axes[:3],names,titles):
        im=ax.imshow(d[key],aspect='auto',interpolation='nearest',cmap='magma',vmin=0,vmax=vmax)
        fig.colorbar(im,ax=ax,label='Gated z (same scale)',pad=.015)
        ax.set_title(title,loc='left',fontweight='bold')
    im=axes[3].imshow(difference,aspect='auto',interpolation='nearest',cmap='RdBu_r',vmin=-diff_limit,vmax=diff_limit)
    fig.colorbar(im,ax=axes[3],label='Change in gated z',pad=.015)
    axes[3].set_title('Raw removal minus mean-preserving removal',loc='left',fontweight='bold')
    for ax in axes:
        ax.set_yticks(np.arange(len(d['feature_ids'])),labels=[str(i) for i in d['feature_ids']],fontsize=7)
        ax.set_ylabel('Fixed feature ID')
    axes[-1].set_xlabel('Same source-ordered text position (0-based within plotted sequence)')
    axes[-1].set_xticks(np.arange(0,d['z_original'].shape[1],32))
    counts=s['mean_l0']
    fig.suptitle(f"Posthoc control | same raw directions, same {s['measurement_positions']:,} measurement positions\n"
                 f"Mean L0: original {counts['original']:.2f}, raw removal {counts['raw_removed']:.2f}, mean preserving {counts['center_preserved']:.2f}",fontsize=12)
    for suffix in ['png','pdf','svg']:fig.savefig(folder/f'centering_control.{suffix}',dpi=180,bbox_inches='tight')
    plt.close(fig)
    origin={'posthoc':True,'source_data':str(root/'control_data.npz'),
            'source_data_sha256':hashlib.sha256((root/'control_data.npz').read_bytes()).hexdigest(),
            'script':str(Path(__file__).resolve()),'feature_selection_unchanged_from_primary':True,
            'all3_common_vmin':0,'all3_common_vmax':vmax,'difference_symmetric_limit':diff_limit,
            'no_semantic_common_claim':True}
    (folder/'provenance.json').write_text(json.dumps(origin,indent=2)+'\n')
    condition_names=['original','raw_removed','center_preserved']
    labels=['Original','Raw removal','Mean preserved']
    colors=['#657786','#d97928','#218477']
    rows=[]
    for condition in condition_names:
        rows.append({'condition':condition,'mean_l0':counts[condition],
                     'mean_phi_same_common_edges':s['mean_fixed_phi_on_same_common_edges'][condition],
                     'event_jaccard_with_original':1.0 if condition=='original' else s['event_jaccard']['original_'+condition],
                     'mean_normalized_reconstruction_vector_MSE':float(np.mean(s['reconstruction'][condition]['normalized_mean_squared_vector_error_by_layer']))})
    import csv
    with (folder/'control_metrics.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    fig,axes=plt.subplots(1,3,figsize=(12,3.8),constrained_layout=True)
    for ax,key,title,ylabel in zip(axes,['mean_l0','mean_phi_same_common_edges','event_jaccard_with_original'],
                      ['Activation count','Fixed-edge relation','Overlap with original code'],
                      ['Active features / position','Mean phi, same estimable edges','Binary-event Jaccard']):
        values=[row[key] for row in rows]
        ax.bar(np.arange(3),values,color=colors,width=.65)
        ax.set_xticks(np.arange(3),labels,rotation=20,ha='right')
        ax.set_ylabel(ylabel);ax.set_title(title,loc='left',fontweight='bold')
        ax.set_ylim(0,max(values)*1.15)
        ax.spines[['top','right']].set_visible(False)
        for i,value in enumerate(values):ax.text(i,value,f'{value:.3f}',ha='center',va='bottom',fontsize=9)
    fig.suptitle(f"Posthoc centering control | same {s['measurement_positions']:,} positions, {s['fixed_edges_common_estimable']:,} common estimable edges",fontsize=12)
    for suffix in ['png','pdf','svg']:fig.savefig(folder/f'centering_control_metrics.{suffix}',dpi=180,bbox_inches='tight')
    plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=DEFAULT);a=p.parse_args();main(a.root)
