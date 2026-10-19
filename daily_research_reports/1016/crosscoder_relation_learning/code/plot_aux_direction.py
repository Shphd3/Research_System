#!/usr/bin/env python3
"""Plot fixed-text/fixed-feature first-direction sensitivity from saved data."""
import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

DEFAULT=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z/data/first_direction')


def main(root):
    root=Path(root)
    d=np.load(root/'heatmap_data.npz')
    summary=json.loads((root/'summary.json').read_text())
    target=root/'figures';target.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,axes=plt.subplots(3,1,figsize=(11,10),sharex=True,sharey=True,constrained_layout=True)
    vmax=max(float(d['z_original'].max()),float(d['z_removed'].max()))
    difference=float(abs(d['z_difference']).max())
    for ax,key,title in zip(axes,['z_original','z_removed','z_difference'],
                           ['Original frozen code','All-source first directions removed','Removed minus original']):
        if key=='z_difference':
            im=ax.imshow(d[key],aspect='auto',interpolation='nearest',cmap='RdBu_r',vmin=-difference,vmax=difference)
            fig.colorbar(im,ax=ax,label='Change in gated z',pad=.015)
        else:
            im=ax.imshow(d[key],aspect='auto',interpolation='nearest',cmap='magma',vmin=0,vmax=vmax)
            fig.colorbar(im,ax=ax,label='Gated z (same scale)',pad=.015)
        ax.set_title(title,loc='left',fontweight='bold')
        ax.set_yticks(np.arange(len(d['feature_ids'])),labels=[str(i) for i in d['feature_ids']],fontsize=7)
        ax.set_ylabel('Fixed feature ID')
    axes[-1].set_xlabel('Fixed source-ordered text position (0-based within plotted sequence)')
    axes[-1].set_xticks(np.arange(0,d['z_original'].shape[1]+1,32))
    fig.suptitle(f"Joint CrossCoder latent sensitivity | {d['z_original'].shape[1]} positions, {len(d['feature_ids'])} fixed features\n"
                 f"14 uncentered raw-source directions; measurement N={summary['measurement_positions']:,}",fontsize=12)
    for suffix in ['png','pdf','svg']:
        fig.savefig(target/f'figure2_first_direction.{suffix}',dpi=180,bbox_inches='tight')
    plt.close(fig)
    origin={'data':str(root/'heatmap_data.npz'),
            'data_sha256':hashlib.sha256((root/'heatmap_data.npz').read_bytes()).hexdigest(),
            'script':str(Path(__file__).resolve()),
            'feature_selection':'D-only top16 reliable frequencies plus16 from upper boundary of fixed bottomquartile; shared order unchanged',
            'original_removed_common_vmin':0,'original_removed_common_vmax':vmax,
            'difference_symmetric_limit':difference,'no_clipping':True,
            'figure_findings':{'mean_l0_original':summary['original_mean_l0'],'mean_l0_removed':summary['removed_mean_l0'],
                               'binary_event_jaccard':summary['binary_event_jaccard']},
            'boundary':'sensitivity to first raw uncentered direction, not common semantics or learned utility'}
    (target/'provenance.json').write_text(json.dumps(origin,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=DEFAULT)
    a=p.parse_args();main(a.root)
