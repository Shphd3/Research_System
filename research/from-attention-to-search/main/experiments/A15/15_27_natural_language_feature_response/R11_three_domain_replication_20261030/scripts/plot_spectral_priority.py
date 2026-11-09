"""Presentation-only derivative; no membership, basis, or statistics changes."""
from pathlib import Path
import json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import PercentFormatter
from matplotlib.lines import Line2D

B=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response')
C=B/'R11_three_domain_replication_20261030/cached_spectral_baseline'
font=B/'R10_domain_member_atlas_20261030/presentation_variants/near_single_domain_20261030/fonts/NotoSansCJKsc-Regular.otf'
font_manager.fontManager.addfont(str(font))
plt.rcParams.update({'font.family':font_manager.FontProperties(fname=str(font)).get_name(),'font.size':13,'axes.titlesize':16,'axes.labelsize':14,'axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False,'pdf.fonttype':42})
rows=list(csv.DictReader((C/'band_profiles.csv').open()))
over=list(csv.DictReader((C/'overlap_comparison.csv').open()))
sens=json.loads((C/'support_matching_audit/summary.json').read_text())
def save(fig,name):
    for ext in ['png','pdf']:fig.savefig(C/'figures'/f'{name}.{ext}',dpi=190,bbox_inches='tight')
    plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(12.8,4.8))
fig.subplots_adjust(wspace=.28,bottom=.20,top=.80)
for ax,cohort,title,top in zip(axes,['discriminative','strict16'],['领域区分：数学433名／生物527名','本批严格单域：数学7名／生物9名'],[.15,.40]):
    for group,label,color in [('math','数学','#2879af'),('biology','生物','#c65b36')]:
        rr=[r for r in rows if r['cohort']==cohort and r['group']==group]
        yy=np.array([float(r['mean']) for r in rr]);ax.plot(np.arange(16),yy,'-o',color=color,label=label,ms=4,lw=2.3)
        ax.annotate(f'{yy[0]:.1%}',(0,yy[0]),xytext=(7,8),textcoords='offset points',color=color,fontsize=14)
    ax.axhline(64/1024,color='#888888',ls=':',lw=1.3)
    ax.set_xticks([0,3,7,11,15],['1–64','193–256','449–512','705–768','961–1024'])
    ax.set_ylim(0,top);ax.set_yticks(np.linspace(0,top,6 if cohort=='discriminative' else 5));ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0));ax.grid(axis='y',alpha=.16)
    ax.set_xlabel('共同PC谱段（每段64维）');ax.set_title(title,pad=15);ax.set_ylabel('成员平均平方投影份额');ax.legend(frameon=False,loc='upper right')
fig.text(.5,.02,'两图纵轴范围不同；虚线6.25%仅为维数占比参照。旧两域缓存，无物理数据。',ha='center',fontsize=11,color='#555555')
save(fig,'figure3_domain_spectra_clear')
fig,axes=plt.subplots(1,2,figsize=(12.8,4.8),sharey=True)
fig.subplots_adjust(left=.16,wspace=.16,bottom=.25,top=.81)
for ax,res,title in zip(axes,['per_PC','64PC_bands'],['逐PC重合（主读数）','每64PC合并（较粗读数）']):
    for cohort,y,color in [('discriminative',1,'#2879af'),('strict16',0,'#9b4d9b')]:
        r=next(r for r in over if r['cohort']==cohort and r['resolution']==res)
        ax.plot([float(r['matched_low']),float(r['matched_high'])],[y+.055]*2,color='#b6bec5',lw=8,solid_capstyle='round')
        obs=float(r['observed']);ax.plot(obs,y,'o',ms=9,color=color,zorder=4);ax.text(obs,y+.23,f'{obs:.3f}',ha='center',color=color,fontsize=15)
        if cohort=='strict16':
            key='overlap_per_PC' if res=='per_PC' else 'overlap_64PC';lo,hi=sens[key]['matched95']
            ax.plot([lo,hi],[y-.11]*2,color='#d69d46',lw=6,solid_capstyle='round')
    ax.set_yticks([1,0],['领域区分\n433／527名','本批严格单域\n7／9名']);ax.set_ylim(-.45,1.5);ax.set_xlim(.50,1.005)
    ax.set_xticks([.5,.6,.7,.8,.9,1]);ax.set_xlabel('数学／生物谱分布重合系数');ax.set_title(title,pad=13);ax.grid(axis='x',alpha=.16)
fig.legend(handles=[Line2D([],[],marker='o',ls='',color='#444444',label='观察值'),Line2D([],[],lw=7,color='#b6bec5',label='发现集支持匹配：95%参照'),Line2D([],[],lw=6,color='#d69d46',label='全120篇支持匹配：95%参照')],loc='lower center',ncol=3,frameon=False,fontsize=11)
save(fig,'figure4_overlap_with_support_audit')
print('Saved two presentation figures; unchanged cached statistics.')
