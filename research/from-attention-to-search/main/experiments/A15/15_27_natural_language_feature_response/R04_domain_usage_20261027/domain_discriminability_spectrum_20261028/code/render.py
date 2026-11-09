"""Scientific figures from frozen cache-only results; no models or statistical refits."""
from pathlib import Path
import json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
O=Path(__file__).resolve().parent;A=O/'analysis';F=O/'figures';F.mkdir(exist_ok=True)
C=json.loads((O/'config.json').read_text());J=json.loads((A/'results.json').read_text());Z=json.loads((A/'candidate_freeze.json').read_text())['dictionaries']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white','pdf.fonttype':42})
COL={'math':'#CF692D','bio':'#147D80','shared':'#7364A9'}

def records(name):
    rows=list(csv.DictReader((A/f'{name}_all_feature_metrics.csv').open(encoding='utf-8-sig')))
    return {int(r['feature']):{k:(r[k] if k in ['dictionary','groups'] else (r[k]=='True' if k=='eligible' or k=='DCLM_low_support' else float(r[k]) if r[k] else np.nan)) for k in r} for r in rows}

def save(fig,name):
    fig.savefig(F/(name+'.png'),dpi=175);fig.savefig(F/(name+'.pdf'));plt.close(fig)

# Figure1: two dictionaries,16discovery-frozen rows each; all document points retained.
fig,axs=plt.subplots(2,4,figsize=(22,17),gridspec_kw={'width_ratios':[1.1,1.1,1.1,.9]})
fig.subplots_adjust(left=.10,right=.97,top=.89,bottom=.18,wspace=.28,hspace=.46)
for row,name in enumerate(['SAE','CC']):
    rr=records(name);ids=Z[name]['groups']['new_top16'];u=np.load(A/f'{name}_per_document_metrics.npz');cols={int(f):j for j,f in enumerate(u['feature_ids'])};lab=u['labels'];split=u['split'];rms=u['RMS']
    for col,(metric,key,title) in enumerate([('hit','hit_fraction','How often?\nActive positions in a document (%)'),('conditional','conditional_native_contribution','How strong when active?\nContribution / discovery token RMS'),('mean','mean_native_contribution','How much including zeros?\nContribution / discovery token RMS')]):
        ax=axs[row,col]
        for yi,f in enumerate(ids):
            j=cols[f];scale=100 if col==0 else 1/rms[j]
            for domain,label,off in [('math',1,-.13),('bio',0,.13)]:
                ix=np.flatnonzero((split=='heldout')&(lab==label));val=u[key][ix,j]*scale;ys=yi+off+np.linspace(-.045,.045,len(ix));ax.scatter(val,ys,s=10,alpha=.30,color=COL[domain],edgecolors='none')
                v=rr[f];mu=v[f'{metric}_{domain}']*scale;lo=v[f'{metric}_{domain}_CI_low']*scale;hi=v[f'{metric}_{domain}_CI_high']*scale
                ax.hlines(yi+off,lo,hi,color=COL[domain],lw=2);ax.scatter([mu],[yi+off],s=26,color=COL[domain],edgecolors='white',linewidths=.5,zorder=5)
        if col==0:ax.set_xlim(-2,102)
        else:
            ax.set_xscale('symlog',linthresh=1,linscale=.6);ax.set_xlim(left=-.05);ax.set_xlabel('Linear 0-1; logarithmic above 1',fontsize=8)
        ax.set_ylim(15.7,-.7);ax.set_yticks(range(16))
        if col==0:
            ax.set_yticklabels([f'f{f}  '+('M' if rr[f]['discovery_direction']>0 else 'B') for f in ids],fontsize=10)
        else:ax.set_yticklabels([])
        ax.set_title(title,fontsize=11,pad=12);ax.grid(axis='x',alpha=.15)
        for yy in np.arange(.5,16,1):ax.axhline(yy,color='#ededed',lw=.6,zorder=0)
    ax=axs[row,3]
    for yi,f in enumerate(ids):
        v=rr[f];ax.hlines(yi,v['heldout_auc_CI_low'],v['heldout_auc_CI_high'],color='#353535',lw=1.6);ax.scatter(v['heldout_direction_fixed_auc'],yi,s=32,color=COL['math' if v['discovery_direction']>0 else 'bio']);ax.text(1.025,yi,f"{v['heldout_direction_fixed_auc']:.3f}",va='center',fontsize=8)
    ax.axvline(.5,color='gray',ls='--',lw=1);ax.set_xlim(0,1.01);ax.set_ylim(15.7,-.7);ax.set_yticks(range(16),['']*16);ax.set_xticks([0,.5,1]);ax.grid(axis='x',alpha=.15);ax.set_title('Single-feature ordering probability\nDiscovery-fixed direction;95% document CI',fontsize=11,pad=12);ax.set_xlabel('0.5 = chance; 1 = all pairs ordered')
    axs[row,0].text(-.25,1.15,('A  E16 SAE | block27 MLP input' if name=='SAE' else 'B  A22 CrossCoder | shared z, block27 decoded contribution'),transform=axs[row,0].transAxes,fontsize=14,weight='bold')
fig.suptitle('1  Which usage differences accompany domain discrimination?',fontsize=20,y=.975)
fig.legend([Line2D([0],[0],color=COL['math'],marker='o',ls=''),Line2D([0],[0],color=COL['bio'],marker='o',ls='')],['Math documents (20)','Biology documents (20)'],ncol=2,loc='upper center',bbox_to_anchor=(.52,.945),frameon=False,fontsize=12)
fig.text(.10,.045,'One row = one feature, selected on discovery only. Small dots = documents; large dots = document means; bars = pointwise bootstrap 95% intervals.\nM/B after each ID = discovery-fixed direction. Conditional strength omits zero-hit documents (NA); document counts and native units are in the data tables.\nColumns2-3 divide by each feature\'s discovery token RMS, preserving math/bio comparisons within that row. Reused holdout: exploratory, not new confirmation.\nContribution is reconstruction magnitude, not functional importance. Terminology, source and genre remain alternatives.',fontsize=10.5,linespacing=1.6)
save(fig,'figure1_domain_usage_and_discrimination')

# Figure2: every newly eligible coordinate, old lists including exceptions, all expanded candidates and fixed top16.
fig,axs=plt.subplots(1,2,figsize=(20,10));fig.subplots_adjust(left=.065,right=.98,top=.80,bottom=.23,wspace=.18)
for ax,name in zip(axs,['SAE','CC']):
    a=np.load(A/f'{name}_all_feature_results.npz');rr=records(name);g=Z[name]['groups'];fr=a['reference_frequency']*100;auc=a['heldout_auc'];eligible=a['eligible'];valid=eligible&np.isfinite(auc);shown=np.maximum(fr,.5/65536*100)
    ax.scatter(shown[valid],auc[valid],s=9,color='#9FA8B1',alpha=.23,edgecolors='none',rasterized=True,zorder=1)
    for key,col in [('expanded_math64',COL['math']),('expanded_bio64',COL['bio'])]:
        fs=np.array(g[key]);ax.scatter(shown[fs],auc[fs],s=34,facecolors='none',edgecolors=col,linewidths=.7,zorder=3)
    for key,col,marker in [('old_shared32',COL['shared'],'s'),('old_math16',COL['math'],'^'),('old_bio16',COL['bio'],'v')]:
        fs=np.array(g[key]);ax.scatter(shown[fs],auc[fs],s=30,c=col,marker=marker,edgecolors='white',linewidths=.35,alpha=.9,zorder=4)
    fs=np.array(g['new_top16']);ax.scatter(shown[fs],auc[fs],s=95,marker='*',facecolors='#242424',edgecolors='white',linewidths=.5,zorder=6)
    noteids=([1004,11667,693,16240,5662] if name=='SAE' else [11710,8963,12266,359])
    for j,f in enumerate(noteids):
        ax.annotate(f'f{f}',(shown[f],auc[f]),xytext=(((-1)**j)*15,(-1 if j%3==0 else 1)*(15+8*(j%2))),textcoords='offset points',fontsize=9,ha='right' if j%2 else 'left',arrowprops=dict(arrowstyle='-',color='#555555',lw=.6),zorder=8)
    ax.set_xscale('log');ax.set_xlim(.5/65536*100*.7,120);ax.set_ylim(-.03,1.045);ax.axhline(.5,color='#666666',ls='--',lw=1);ax.axvline(np.median(fr),color='#888888',ls=':',lw=1);ax.set_xlabel('DCLM activation rate (%) | log scale',fontsize=12);ax.set_ylabel('Heldout ordering probability (AUROC)\nDirection fixed by discovery',fontsize=11);ax.grid(alpha=.12)
    ax.set_title(f'{name}: {int(eligible.sum()):,} eligible coordinates\n64 math-direction +64 biology-direction candidates',fontsize=13,pad=13)
    tied=int((eligible&~np.isfinite(auc)).sum());zero=int((valid&(fr==0)).sum())
    ax.text(.025,.03,f'Discovery ties: {tied} (direction NA, not plotted)\nReference zero hits: {zero} (shown at half-hit)',transform=ax.transAxes,fontsize=8,bbox=dict(facecolor='white',alpha=.85,edgecolor='none'))
leg=[Line2D([0],[0],marker='o',color='#9FA8B1',ls='',markersize=5),Line2D([0],[0],marker='o',markerfacecolor='none',markeredgecolor=COL['math'],ls=''),Line2D([0],[0],marker='o',markerfacecolor='none',markeredgecolor=COL['bio'],ls=''),Line2D([0],[0],marker='s',color=COL['shared'],ls=''),Line2D([0],[0],marker='^',color=COL['math'],ls=''),Line2D([0],[0],marker='v',color=COL['bio'],ls=''),Line2D([0],[0],marker='*',color='#242424',ls='',markersize=12)]
fig.legend(leg,['All eligible','New math64','New bio64','Old shared32','Old math16','Old bio16','Frozen top16'],loc='upper center',bbox_to_anchor=(.5,.91),ncol=7,frameon=False,fontsize=10)
fig.suptitle('2  Domain-discriminating coordinates occur across reference frequencies',fontsize=20,y=.975)
rands={d:json.loads((A/f'{d}_matched_random_summary.json').read_text())['new_top16'] for d in ['SAE','CC']}
for xx,d in zip([.065,.55],['SAE','CC']):
    z=rands[d];lo,med,hi=z['random_mean_auc_quantiles'];fig.text(xx,.15,f'{d} top16 mean: {z["observed_mean_auc"]:.3f}; frequency/support-matched random means:\nmedian {med:.3f}, central95% [{lo:.3f}, {hi:.3f}] (1,000 sets).',fontsize=10)
fig.text(.065,.065,'One point = one feature, not one text. Dotted vertical line = median reference frequency of the full dictionary. Grey background retains weak/reversed responses.\nOld candidate lists are kept even when they fail the new two-domain support gate. AUROC is a document ordering probability, not classification accuracy.\nRandom comparisons are descriptive and do not remove discovery selection or reused-holdout bias. Frequency association does not establish causation.',fontsize=10.5,linespacing=1.6)
save(fig,'figure2_discrimination_vs_DCLM_frequency')

# Figure3 is explicitly a dependency/status card, never a synthetic spectral heatmap.
fig,ax=plt.subplots(figsize=(15,8));ax.axis('off')
fig.suptitle('3  Common-spectrum positioning: NOT MEASURED',fontsize=23,y=.94,weight='bold')
ax.text(.04,.88,'Real R04 hook representations were not saved.',fontsize=20,color='#A54332',weight='bold',transform=ax.transAxes)
ax.text(.04,.75,'Available: original text / splits, sparse feature activations, decoder norms,\nDCLM all-coordinate frequencies, document latent moments and reconstruction errors.',fontsize=14,linespacing=1.6,transform=ax.transAxes)
ax.text(.04,.56,'Missing: real block27 MLP-input h AND real block27 residual-post h\nfor the same R04 document positions (120 documents x160 tokens x1024 dimensions per hook).',fontsize=14,linespacing=1.6,transform=ax.transAxes)
ax.text(.04,.35,'Therefore NOT RUN: pooled PCA; 16-rank-band decoder projections; real variance bands;\ndomain mean-difference projections; heldout spectral reproduction; matched spectral reference.',fontsize=14,linespacing=1.6,transform=ax.transAxes)
ax.text(.04,.14,'No reconstructed h or old-corpus PCA substituted. No new model forward was run.\nCompleting this branch needs120 document replays (+4 optional checks), pending explicit approval.\nSaving both measured hooks in FP32 requires about150 MiB, excluding metadata.',fontsize=12,linespacing=1.6,transform=ax.transAxes)
fig.text(.08,.035,'No data axes: this is a missing-data status card, not a spectral result. No conclusion about spectral concentration is available.',fontsize=11,color='#555555')
save(fig,'figure3_spectrum_NOT_MEASURED')
meta={'producer':'render.py','source':'analysis frozen candidate and metrics tables','figures':{'figure1_domain_usage_and_discrimination':'measured exploratory; native contribution/discovery RMS where labeled','figure2_discrimination_vs_DCLM_frequency':'measured exploratory; all qualified coordinates retained','figure3_spectrum_NOT_MEASURED':'MISSING-DATA STATUS CARD; NOT SPECTRAL EVIDENCE'},'unit':'feature rows/points; intervals resample documents','new_forwards':0,'PCA':'NOT_RUN','manual_labels':'illustrative fixed IDs listed in render.py, no candidate changes'}
(F/'figure_manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('FIGURES',str(F))
