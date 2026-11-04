"""Five numbered meeting figure groups; further panels live in appendix/."""
from pathlib import Path
import json,csv,textwrap,os
os.environ['OPENBLAS_NUM_THREADS']='2'
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
O=Path(__file__).resolve().parent
def js(p):return json.loads(Path(p).read_text())
def rows(name):return list(csv.DictReader((O/'tables'/name).open(encoding='utf-8-sig')))
def save(fig,name,appendix=False):
    fig.savefig(O/('appendix' if appendix else 'figures')/(name+'.png'),dpi=180,bbox_inches='tight');plt.close(fig)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':120})
C={'math':'#267fb0','biology':'#cc6b3d','low':'#77b9d0','middle':'#f1bc57','high':'#9b6ca8','low_support':'#b5b5b5'}
fr=js(O/'freeze.json');res=js(O/'analysis/results.json');ids=fr['ordered_union'];geom=np.load(O/'analysis/unit_decoder_geometry.npz');bands=geom['per_band'];G=fr['groups']
fc=rows('frequency_counts.csv');spec=rows('spectrum_summary.csv');effects=rows('context_effects.csv');token=rows('token_member_summary.csv');examples=rows('real_token_examples.csv')

# 1: Actual member counts, with pool composition and clearly separate sensitivity.
fig,axs=plt.subplots(2,2,figsize=(12,7),gridspec_kw={'width_ratios':[1.2,1]})
for row,scheme in enumerate(['original_equal_count','R09_log_equal_width']):
    ax=axs[row,0];bottom=np.zeros(2)
    for group in ['low','middle','high','low_support']:
        vals=[int(next(r['n'] for r in fc if r['scheme']==scheme and r['population']==d and r['group']==group)) for d in G]
        ax.bar([0,1],vals,bottom=bottom,color=C[group],label=group)
        for i,v in enumerate(vals):
            if v:ax.text(i,bottom[i]+v/2,str(v),ha='center',va='center',fontsize=12)
        bottom+=vals
    ax.set_xticks([0,1],['Math bias (n=16)','Biology bias (n=16)']);ax.set_ylim(0,18);ax.set_yticks([0,4,8,12,16]);ax.set_ylabel('Number of frozen members')
    ax.set_title('Primary: original equal-count groups' if row==0 else 'Sensitivity: R09 log-width groups')
    ax=axs[row,1];left=0
    for group in ['low','middle','high','low_support']:
        r=next(r for r in fc if r['scheme']==scheme and r['population']=='eligible_pool' and r['group']==group);v=float(r['fraction'])*100
        ax.barh([0],v,left=left,color=C[group],label=group)
        if v>4:ax.text(left+v/2,0,f'{int(r["n"]):,}\n({v:.1f}%)',ha='center',va='center')
        left+=v
    ax.set_xlim(0,100);ax.set_yticks([0],['Eligible pool\nn=8,113']);ax.set_xlabel('Pool composition (%)');ax.set_title('Same document-support eligibility')
axs[0,0].legend(ncol=4,fontsize=8,loc='upper center',bbox_to_anchor=(.5,1.31))
fig.suptitle('1. Which activation-frequency groups?  Same 16+16 members throughout',y=1.02,fontsize=14)
fig.text(.02,-.015,'Primary cuts: 0.259399% / 1.344299%. Log-width cuts: 0.451726% / 6.686506%.\nNative shared z>0 / 65,536 independent DCLM positions; <20 hits = low support (pool n=8).',fontsize=10)
fig.tight_layout(rect=(0,.08,1,.97));save(fig,'figure1_frequency')

# 2: Every member + mean + median, full dictionary and available exact matching.
x=np.arange(16);labels=[f'{k*64+1}\n{(k+1)*64}' for k in x]
fig,axs=plt.subplots(1,2,figsize=(14,5),sharey=True)
for j,(d,g) in enumerate(G.items()):
    ax=axs[j];v=bands[j*16:(j+1)*16]
    for a in v:ax.plot(x,a,color=C[d],alpha=.22,lw=1)
    ax.plot(x,v.mean(0),'o-',color=C[d],lw=2,label='16-member mean')
    ax.plot(x,np.median(v,axis=0),'s--',color='#252525',lw=1.5,label='16-member median')
    bg=[r for r in spec if r['population']=='full_dictionary'];ax.plot(x,[float(r['mean']) for r in bg],':',color='#69747c',lw=2,label='Full dictionary mean (16,384)')
    mp=O/'analysis'/f'{d}_matched_background.npz'
    if mp.exists():
        vbg=np.load(mp)['band_mean'];lo,hi=np.quantile(vbg,[.025,.975],axis=0);ax.fill_between(x,lo,hi,color='#999999',alpha=.3,label='Exact matched-set 95% range')
    else:ax.text(.98,.92,'Exact matching: NA\nf9491 joint bin has no replacement',transform=ax.transAxes,ha='right',va='top',fontsize=9,color='#a44834')
    ax.axhline(1/16,color='#999',lw=.8,ls=':');ax.set_xticks(x,labels,fontsize=8);ax.yaxis.set_major_formatter(PercentFormatter(1));ax.set_xlabel('R07 fixed natural-text PCA rank band (start / end)');ax.set_title(f'{d.capitalize()} bias: n=16');ax.legend(fontsize=8)
axs[0].set_ylabel('Squared projection of unit decoder');fig.suptitle('2. Decoder orientation across all 1,024 PCs (16 bands of 64)',fontsize=14);fig.tight_layout();save(fig,'figure2_decoder_spectrum')

# 3: Shading is the minimum group mean, not confidence or a decoder direction.
fig,(ax,info)=plt.subplots(1,2,figsize=(12,4.6),gridspec_kw={'width_ratios':[3,1.3]})
means={d:bands[j*16:(j+1)*16].mean(0) for j,d in enumerate(G)}
for d,v in means.items():ax.plot(x,v,'o-',label=f'{d.capitalize()} mean (n=16)',color=C[d],lw=2)
ax.fill_between(x,0,np.minimum(*means.values()),color='#8aa6a6',alpha=.38,label='Common share: minimum of group means')
ax.set_xticks(x,labels,fontsize=8);ax.set_xlabel('Same R07 PCA rank bands (start / end)');ax.set_ylabel('Group mean squared unit-decoder projection');ax.yaxis.set_major_formatter(PercentFormatter(1));ax.set_ylim(bottom=0);ax.legend(fontsize=9)
g=res['geometry'];info.axis('off');info.text(0,.95,f"Per-PC overlap\n{g['overlap_per_PC']:.4f}\n\n64-PC band overlap\n{g['overlap_per_band']:.4f}\n\nMatched pair background: NA\nOne required bin is empty.\n\nUnmatched dictionary pairs\nper-PC 95% range:\n{g['uniform_unmatched_per_PC_quantiles'][0]:.3f} - {g['uniform_unmatched_per_PC_quantiles'][2]:.3f}\n(not frequency/support matched)",va='top',fontsize=12)
fig.suptitle('3. Spectral-distribution overlap depends on resolution',fontsize=14);fig.tight_layout();save(fig,'figure3_spectral_overlap')

# 4a+4b share a single numbered figure group. Representatives were first-ranked
# in each frozen discovery group; no activation/spectrum-dependent replacement.
fig=plt.figure(figsize=(13,10));gs=fig.add_gridspec(2,1,height_ratios=[1.15,1],hspace=.35);ax=fig.add_subplot(gs[0]);ax.axis('off')
display=[]
for f in [G['math'][0],G['biology'][0]]:
    er=[r for r in examples if int(r['feature'])==f]
    for kind in ['high','ordinary','same_token_low_or_inactive']:
        r=next((r for r in er if r['example_type']==kind),None)
        if r is None:continue
        prefix=r['read_prefix'][-100:].replace('\n',' ')
        display.append([f'f{f}\n{kind.replace("_or_inactive","")}',f"{r['token_id']} {r['token_string']!r}\np={r['position_zero_based']}; z={float(r['z']):.4g}",textwrap.fill(prefix,48),f"{r['document']}\n{r['domain']} / {r['split']}"])
table=ax.table(cellText=display,colLabels=['Member / input case','Token ID / string / position','Already-read prefix (last 100 chars only)','Document'],cellLoc='left',colWidths=[.16,.22,.41,.21],bbox=[0,0,1,.93]);table.auto_set_font_size(False);table.set_fontsize(9)
ax.set_title('4a. Real observed input tokens; first-ranked member per domain (full prefixes in appendix)',loc='left',fontsize=12,pad=10)
ax=fig.add_subplot(gs[1])
for d in G:
    rr=[r for r in token if r['group']==d];xx=np.array([float(r['feature_reference_rate']) for r in rr]);yy=np.array([float(r['token_rate_median']) for r in rr]);lo=np.array([float(r['token_rate_p10']) for r in rr]);hi=np.array([float(r['token_rate_p90']) for r in rr]);ax.errorbar(xx,yy,yerr=[yy-lo,hi-yy],fmt='o',color=C[d],alpha=.7,label=f'{d} (n=16)',capsize=2)
    for f in [G[d][0]]:
        r=next(r for r in rr if int(r['feature'])==f);ax.annotate(f'f{f}',(float(r['feature_reference_rate']),float(r['token_rate_median'])),xytext=(5,6),textcoords='offset points')
ax.set_xscale('log');ax.set_yscale('log');ax.set_xlabel('Feature reference occurrence (z>0 / 65,536), log scale');ax.set_ylabel('Median input-token reference frequency\nat active positions, reference-seen IDs only (log)');ax.legend();ax.set_title('4b. One point per frozen member; bars = 10th-90th percentiles of active-position token rates',loc='left',fontsize=11)
fig.text(.02,.015,'Unseen token IDs are missing frequency estimates, excluded from quantiles and counted separately (8.1%-56.4% of active positions).\nBoth rates use the same 65,536-position reference but count different objects. This is not the unconditional token-frequency median.',fontsize=10)
fig.suptitle('4. Actual input-token responses and two distinct frequency measures',fontsize=14,y=.98);save(fig,'figure4_tokens')

def effect_panel(ax,f):
    rr=[r for r in effects if int(r['feature'])==f];maxy=0
    for split,offset,marker,color in [('discovery',-.09,'o','#3989ad'),('heldout',.09,'s','#cf7048')]:
        v=[next(r for r in rr if r['split']==split and r['target']==t and int(r['wording'])==w) for t,w in [('example',0),('example',1),('explanation',0),('explanation',1)]]
        yy=np.array([float(r['delta_math_minus_biology']) for r in v]);lo=np.array([float(r['CI_low']) for r in v]);hi=np.array([float(r['CI_high']) for r in v]);ax.errorbar(np.arange(4)+offset,yy,yerr=[yy-lo,hi-yy],fmt=marker,color=color,capsize=2,label=f'{split}: {24 if split=="discovery" else 12} families')
    ax.axhline(0,color='#555',lw=.7);ax.set_xticks(np.arange(4),['example\nW0','example\nW1','explanation\nW0','explanation\nW1'],fontsize=8)
    n=next(r['fixed_target_active_positions'] for r in rows('context_categories.csv') if int(r['feature'])==f)
    cat=next(r['category'] for r in rows('context_categories.csv') if int(r['feature'])==f)
    ax.set_title(f'f{f}: category {cat}; active {n}/384 cached positions',fontsize=10);ax.set_ylabel('Mean z(math) - z(biology)');ax.ticklabel_format(axis='y',style='sci',scilimits=(-2,2))

fig,axs=plt.subplots(2,2,figsize=(12,7.5))
for ax,f in zip(axs.ravel(),[G['math'][0],G['math'][1],G['biology'][0],G['biology'][1]]):effect_panel(ax,f)
axs[0,0].legend(fontsize=8);fig.suptitle('5. Fixed-target context responses: first two discovery ranks per domain',fontsize=14)
fig.text(.02,.008,'All 32 retained: A=5, B=0, C=27; 19 never activate on these fixed targets (coverage insufficient).\nActive members per cell, discovery: 11/11/8/8 of 32; old heldout: 12/9/7/8 of 32.\nIntervals resample whole families; pointwise descriptive 95%, exposed old heldout. All 32 members plotted in the appendix.',fontsize=10)
fig.tight_layout(rect=(0,.12,1,.96));save(fig,'figure5_context')

# Appendix: preserve all member direction distributions and all responses.
fig,ax=plt.subplots(figsize=(12,10));im=ax.imshow(bands,aspect='auto',cmap='magma');ax.set_yticks(np.arange(32),[f'{"M" if j<16 else "B"}{j%16+1}: f{f}' for j,f in enumerate(ids)],fontsize=8);ax.set_xticks(x,labels,fontsize=8);ax.axhline(15.5,color='cyan',lw=1);ax.set_xlabel('R07 PC band');fig.colorbar(im,ax=ax,label='Unit-decoder squared projection');ax.set_title('All frozen members, same discovery order');fig.tight_layout();save(fig,'member_band_heatmap',True)
fig,axs=plt.subplots(2,1,figsize=(13,8));rr=rows('group_PC_overlap.csv')
for d in G:axs[0].plot(np.arange(1,1025),[float(r[d]) for r in rr],color=C[d],alpha=.7,lw=.7,label=d)
axs[0].set_xlabel('Individual PC rank');axs[0].set_ylabel('Mean squared unit projection');axs[0].legend();co=np.array([float(r['abs_cosine']) for r in rows('pair_absolute_cosine.csv')]).reshape(16,16);im=axs[1].imshow(co,aspect='auto',vmin=0,vmax=1,cmap='viridis');axs[1].set_xticks(np.arange(16),[str(f) for f in G['biology']],rotation=60,fontsize=8);axs[1].set_yticks(np.arange(16),[str(f) for f in G['math']],fontsize=8);axs[1].set_xlabel('Biology member ID');axs[1].set_ylabel('Math member ID');fig.colorbar(im,ax=axs[1],label='Absolute cosine');fig.tight_layout();save(fig,'per_PC_and_pair_cosine',True)
for page,d in enumerate(G):
    fig,axs=plt.subplots(4,4,figsize=(18,14))
    for ax,f in zip(axs.ravel(),G[d]):effect_panel(ax,f)
    axs[0,0].legend(fontsize=7);fig.suptitle(f'All {d} members (n=16), fixed original discovery order',fontsize=15);fig.tight_layout();save(fig,'all_context_'+d,True)
print('Rendered five main figure groups and four appendix figures.')
