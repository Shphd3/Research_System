import os
os.environ['MPLBACKEND']='Agg'
from pathlib import Path
import json,shutil
import pandas as pd,numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager,FontProperties
P=Path(__file__).resolve().parents[1];E=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_20261101_native_spectral_decoding/supplements')/P.name
font='/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030/presentation_variants/near_single_domain_20261030/fonts/NotoSansCJKsc-Regular.otf';fontManager.addfont(font);plt.rcParams.update({'font.family':FontProperties(fname=font).get_name(),'axes.unicode_minus':False,'font.size':11,'axes.spines.right':False,'axes.spines.top':False,'savefig.dpi':160})
r=pd.read_csv(E/'analysis/group_recovery.csv');s=pd.read_csv(E/'analysis/summary_metrics.csv');o=pd.read_csv(E/'analysis/output_top1_ID_counts.csv');conditions=['k1','pc2','k8','k16'];labels=['仅第1主成分','仅第2主成分','前8主成分','前16主成分'];groups=['format','nonformat_common','nonformat_other'];names=['空白／标点','参考常见ID（排除格式）','其他ID（排除格式）'];colors=['#bc812a','#2f7b9c','#925f9b']
def save(fig,name):
 for ext in ['png','pdf']:fig.savefig(E/'figures'/(name+'.'+ext),bbox_inches='tight');shutil.copy2(E/'figures'/(name+'.'+ext),P/'figures'/(name+'.'+ext))
 plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(14,5.7),sharey=True)
for col,panel in enumerate(['the','natural']):
 ax=axs[col]
 for gi,g in enumerate(groups):
  d=r[(r.panel==panel)&(r.group==g)].set_index('condition');n=int(d.iloc[0].documents);positions=int(d.iloc[0].positions)
  if n<5:
   ax.text(.01,.96,'空白／标点仅1篇：不作组间推断',transform=ax.transAxes,va='top',fontsize=10,color='#666666');continue
  z=d.loc[conditions];y=z['mean'].to_numpy()*100;lo=z.ci_low.to_numpy()*100;hi=z.ci_high.to_numpy()*100;x=np.arange(4)+(gi-1)*.24
  ax.bar(x,y,.23,color=colors[gi],label=f'{names[gi]}：{n}篇/{positions}位置');ax.errorbar(x,y,yerr=[y-lo,hi-y],fmt='none',c='#444444',capsize=3,lw=1);ax.bar_label(ax.containers[-2] if False else ax.containers[-2] if False else ax.containers[0],labels=[] ) if False else None
  for xx,yy in zip(x,y):ax.text(xx,yy+.8,f'{yy:.1f}',ha='center',va='bottom',fontsize=9,color=colors[gi])
 ax.set_xticks(range(4),labels);ax.set_ylim(0,max(40,100*r[r.condition.isin(conditions)]['ci_high'].max()+6));ax.set_title('固定the：37篇／37位置' if panel=='the' else '自然面板：175篇／700位置');ax.set_ylabel('与原模型首选ID相同的组内文档均值（%）');ax.legend(loc='upper left',bbox_to_anchor=(0,.90),fontsize=9);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
fig.suptitle('只留一个方向，或累计8／16维：哪些原有预测被保留？',fontsize=16);fig.text(.5,.015,'全部条件加回同一训练均值，再接原生RMSNorm与冻结输出头；误差线为组内文档bootstrap2000次的95%区间。',ha='center',fontsize=10);fig.tight_layout(rect=[0,.05,1,.94]);save(fig,'01_four_conditions_recovery')
fig,axs=plt.subplots(2,3,figsize=(15,8))
for row,panel in enumerate(['the','natural']):
 for col,(metric,title,unit) in enumerate([('NLL','真实后继NLL：越低越好','nat'),('format_mass','输出到空白／标点的概率质量','%'),('freq_top1pct','输出到参考最高频1% ID的质量','%')]):
  ax=axs[row,col];d=s[(s.panel==panel)&(s.metric==metric)].set_index('condition');z=d.loc[conditions];scale=1 if metric=='NLL' else 100;y=z['mean'].to_numpy()*scale;lo=z.ci_low.to_numpy()*scale;hi=z.ci_high.to_numpy()*scale
  ax.bar(range(4),y,color=['#477fa4','#c38d42','#789f94','#816b9c']);ax.errorbar(range(4),y,yerr=[y-lo,hi-y],fmt='none',c='black',capsize=3)
  for xx,yy in enumerate(y):ax.text(xx,hi[xx]+(.2 if metric=='NLL' else .4),f'{yy:.2f}',ha='center',va='bottom',fontsize=10)
  ax.axhline(d.loc['mean_only','mean']*scale,c='#777777',ls=':',label='仅训练均值');ax.axhline(d.loc['identity','mean']*scale,c='#222222',ls='--',label='原模型');ax.set_xticks(range(4),['第1单独','第2单独','前8','前16']);ax.set_title(title);ax.set_ylabel(('the面板' if row==0 else '自然面板')+' · '+unit);ax.set_ylim(0,max(1,1.22*max(hi.max(),d.loc['mean_only','mean']*scale)));ax.set_ylim(0,105) if metric=='freq_top1pct' else None;ax.legend(fontsize=8,loc='lower left');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
fig.suptitle('保留原有预测 ≠ 输出偏常见／符号：同时看真实后继与概率质量',fontsize=16);fig.text(.5,.01,'“常见最高1%质量”含其中的格式ID；恢复图中的常见组排除了格式。两个定义有意分别展示，不能把柱高当正确率。',ha='center',fontsize=10);fig.tight_layout(rect=[0,.04,1,.94]);save(fig,'02_accuracy_and_output_bias')
# Actual selected output IDs, rather than assigning a semantic name from a scalar metric.
fig,axs=plt.subplots(1,4,figsize=(16,4.5))
for ax,co,title in zip(axs,conditions,labels):
 a=o[(o.panel=='natural')&(o.condition==co)].sort_values(['positions','token_id'],ascending=[False,True]).head(6);ax.barh(range(len(a)),a.positions,color='#5a829e');lab=[repr(x.fragment).replace('\\n','[换行]')+f' [{x.token_id}]' for x in a.itertuples()];ax.set_yticks(range(len(a)),lab,fontsize=9);ax.invert_yaxis();ax.set_title(title);ax.set_xlabel('成为首选的原始位置数（共700）');ax.bar_label(ax.containers[0],padding=2,fontsize=9);ax.set_xlim(0,max(a.positions.max()*1.2,1))
fig.suptitle('自然面板实际输出什么：每个条件最常成为首选的6个ID',fontsize=15);fig.tight_layout(rect=[0,0,1,.91]);save(fig,'03_actual_top1_IDs')
print('3figure groups rendered')
