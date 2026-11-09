"""Measured common-spectrum figure from true hooks, keeping frozen feature order."""
from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
O=Path(__file__).resolve().parent;A=O/'analysis';F=O/'figures';J=json.loads((A/'spectral_results.json').read_text())['dictionaries']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white','pdf.fonttype':42})
colors={'discovery':'#4774A9','development':'#A3A3A3','heldout':'#985696'}
x=np.arange(16);labels=[f'{64*b+1}-{64*(b+1)}' for b in range(16)]
fig=plt.figure(figsize=(23,21));gs=fig.add_gridspec(4,2,height_ratios=[1.2,1.2,3.6,1.5],left=.085,right=.92,top=.90,bottom=.12,wspace=.24,hspace=.62)
vmax=0
for name in ['SAE','CC']:
    a=np.load(A/f'{name}_decoder_common_spectrum.npz');loc={int(f):i for i,f in enumerate(a['feature_ids'])};ii=[loc[f] for f in J[name]['top16_feature_ids']];vmax=max(vmax,float(a['band_squared_projection'][ii].max()*100))
vmax=np.ceil(vmax)
for col,name in enumerate(['SAE','CC']):
    d=J[name]
    for row,metric,title in [(0,'variance_fraction_by_band','Real representation variance'),(1,'mean_difference_fraction_by_band','Math-bio document-mean difference')]:
        ax=fig.add_subplot(gs[row,col])
        for split in ['discovery','development','heldout']:
            so=d['splits'][split];y=np.array(so[metric])*100;ci=np.array(so['variance_CI95' if row==0 else 'mean_difference_fraction_CI95'])*100
            ax.plot(x,y,'o-',color=colors[split],ms=3.5,lw=1.3,label=split)
            if split!='development':ax.fill_between(x,np.maximum(ci[0],1e-8),np.maximum(ci[1],1e-8),color=colors[split],alpha=.12)
        ax.set_yscale('log');ax.set_xticks(x,[]);ax.set_xlim(-.5,15.5);ax.grid(axis='y',alpha=.15);ax.set_ylabel('Share (%) | log scale');ax.set_title(('E16 SAE | block27 MLP input' if name=='SAE' else 'A22 | block27 residual-post')+'\n'+title,fontsize=12,pad=8)
        if row==1:ax.text(.99,.95,f"Heldout head64: {d['splits']['heldout'][metric][0]*100:.2f}%\nMean-direction alignment: {d['splits']['heldout']['mean_difference_alignment_with_discovery']:.3f}",ha='right',va='top',transform=ax.transAxes,fontsize=9)
    ax=fig.add_subplot(gs[2,col]);a=np.load(A/f'{name}_decoder_common_spectrum.npz');loc={int(f):i for i,f in enumerate(a['feature_ids'])};ids=d['top16_feature_ids'];ii=[loc[f] for f in ids];mat=a['band_squared_projection'][ii]*100
    im=ax.imshow(mat,aspect='auto',vmin=0,vmax=vmax,cmap='YlGnBu',interpolation='nearest');ax.set_yticks(range(16),[f'f{f}' for f in ids],fontsize=10);ax.set_xticks(x,labels,rotation=60,ha='right',fontsize=8);ax.set_title('Unit decoder squared projection (%)\nEach row sums to100%; discovery-fixed feature order',fontsize=12,pad=10)
    ax=fig.add_subplot(gs[3,col]);g=d['groups']['new_top16'];obs=np.array(g['unit_mean_band_projection'])*100;qt=np.array(g['random_band_quantiles'])*100
    ax.fill_between(x,qt[0],qt[2],color='#c5c9ce',alpha=.6,label='Matched background central95%');ax.plot(x,qt[1],'--',color='#62666b',lw=1.2,label='Matched median');ax.plot(x,obs,'o-',color='#6A3D8F',lw=1.5,ms=4,label='Frozen top16 mean');q=np.array(g['BH_q_32_main_comparisons']);h=max(float(np.max(obs)),float(np.max(qt[2])))
    for b in np.flatnonzero(q<.05):ax.text(b,max(obs[b],qt[2,b])+.025*h,'*',ha='center',fontsize=13,color='#6A3D8F')
    ax.set_ylim(0,h*1.18);ax.set_xlim(-.5,15.5);ax.set_xticks(x,labels,rotation=60,ha='right',fontsize=8);ax.set_ylabel('Mean unit projection (%)');ax.set_xlabel('Same frozen PC rank bands');ax.grid(axis='y',alpha=.15);ax.set_title('1000 original frequency/support-matched sets\n* exploratory background comparison, BH across32bands',fontsize=11,pad=8)
    if col==0:ax.legend(loc='upper right',fontsize=8,frameon=False)
cbax=fig.add_axes([.94,.30,.012,.30]);cb=fig.colorbar(im,cax=cbax);cb.set_label('Unit-direction squared projection in one band (%)')
fig.legend([Line2D([0],[0],color=colors[s],marker='o',ls='-') for s in colors],['Discovery (60docs, fit basis)','Development (20docs, projection only)','Reused holdout (40docs, projection only)'],loc='upper center',bbox_to_anchor=(.5,.955),ncol=3,frameon=False,fontsize=12)
fig.suptitle('3  Where do the fixed discriminating directions lie in a shared domain spectrum?',fontsize=20,y=.985)
fig.text(.085,.028,'Each hook uses its own true1024-D representation and one pooled discovery mean; no domain-specific centering or extra dimensionwise standardization.\nTop2rows: real variance and squared document-domain mean-difference fractions; ribbons resample documents. A mean difference is not all classifiable information.\nHeatmap: one row = one frozen feature, one column =64PC directions. Bottom: mean unit geometry versus matched reference, not reconstruction variance.\nCC activations remain native14-layer shared z; final-layer decoder directions are not final-layer-independent activations. All reused-holdout analyses are exploratory.',fontsize=10.5,linespacing=1.55)
fig.savefig(F/'figure3_true_common_spectrum.png',dpi=165);fig.savefig(F/'figure3_true_common_spectrum.pdf');plt.close(fig)
(F/'figure_manifest.json').write_text(json.dumps({'status':'MEASURED_TRUE_H_EXPLORATORY','producer':'render_spectrum.py','source':'analysis/spectral_results.json and native decoder projections','rows':'same frozen top16 as prior figures1/2','columns':'16contiguous64-PCrankbands','unit':'unit-direction squared projection fraction;complete1024basis','PCA':'pooleddiscoverytrueh,separatehookbases','not':'featurefrequencybins,semanticlevel,functionalimportance,orclustering','old_gap_card':'preserved as historical cache-only state, not current result'},indent=2)+'\n')
print('TRUE_SPECTRUM_FIGURE_DONE',F)
