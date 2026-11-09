import os
os.environ['MPLBACKEND']='Agg'
from pathlib import Path
import json,shutil
import numpy as np,pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties,fontManager
P=Path(__file__).resolve().parents[1];E=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_20261101_native_spectral_decoding/supplements')/P.name
font='/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030/presentation_variants/near_single_domain_20261030/fonts/NotoSansCJKsc-Regular.otf';fontManager.addfont(font);plt.rcParams.update({'font.family':FontProperties(fname=font).get_name(),'axes.unicode_minus':False,'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':150})
M=json.load(open(E/'manifest.json'));S=pd.read_csv(E/'analysis/summary_metrics.csv');C=pd.read_csv(E/'analysis/context_controls.csv');D=pd.read_csv(E/'analysis/band_definitions.csv');counts=pd.read_csv(E/'analysis/output_top1_counts.csv',keep_default_na=False);bands=M['bands'];main=bands[:8];names={b['condition']:f"PC{b['PC_start_one_based']}–{b['PC_stop_exclusive_one_based']-1}" for b in bands}
def probstr(p):return f'{100*p:.2e}%' if p<1e-5 else f'{100*p:.4f}%'
def one(co,metric):return S[(S.condition==co)&(S.metric==metric)].iloc[0]
def save(fig,n):
 for ext in ['png','pdf']:fig.savefig(E/'figures'/(n+'.'+ext),bbox_inches='tight');shutil.copy2(E/'figures'/(n+'.'+ext),P/'figures'/(n+'.'+ext))
 plt.close(fig)
fig,axs=plt.subplots(1,3,figsize=(17,5.7));ax=axs[0];n=[b['condition'] for b in main];a=[one(c,'NLL') for c in n];v=np.array([x['mean'] for x in a]);lo=np.array([x['ci_low'] for x in a]);hi=np.array([x['ci_high'] for x in a]);ax.bar(range(8),v,color=['#477fa4']*5+['#a8735c']*3);ax.errorbar(range(8),v,yerr=[v-lo,hi-v],fmt='none',c='#444444',capsize=3);ax.axhline(one('mean_only','NLL')['mean'],c='#777777',ls=':',label='仅训练均值');ax.axhline(one('identity','NLL')['mean'],c='#222222',ls='--',label='原模型');ax.set_xticks(range(8),[f"{names[c]}\n{int(D[D.condition==c].iloc[0].dimensions)}维" for c in n],rotation=50,ha='right');ax.set_ylabel('真实后继 NLL（nat；低为好）');ax.set_title('独立区间单独解码；各段维数不同');ax.legend(fontsize=9);ax.grid(axis='y',alpha=.13);ax.set_axisbelow(True)
ax=axs[1];a=C[(C.target_group=='all')&C.condition.isin(n)].set_index('condition').loc[n];v=a.mean_NLL_gain_real_vs_same_token_other_document.to_numpy();lo=a.ci_low.to_numpy();hi=a.ci_high.to_numpy();ax.bar(range(8),v,color=['#477fa4']*5+['#a8735c']*3);ax.errorbar(range(8),v,yerr=[v-lo,hi-v],fmt='none',c='#444444',capsize=3);ax.axhline(0,c='black',lw=.8);ax.set_xticks(range(8),[names[c] for c in n],rotation=50,ha='right');ax.set_ylabel('异文档NLL − 真实上下文NLL（nat）');ax.set_title('同当前token、换文档系数后，预测变差吗？');ax.grid(axis='y',alpha=.13);ax.set_axisbelow(True)
ax=axs[2];n=['b64_128','equal64_512','equal64_768','equal64_961'];a=C[(C.target_group=='all')&C.condition.isin(n)].set_index('condition').loc[n];v=a.mean_NLL_gain_real_vs_same_token_other_document.to_numpy();lo=a.ci_low.to_numpy();hi=a.ci_high.to_numpy();ax.bar(range(4),v,color=['#477fa4']+['#a8735c']*3);ax.errorbar(range(4),v,yerr=[v-lo,hi-v],fmt='none',c='#444444',capsize=3);ax.axhline(0,c='black',lw=.8);ax.set_xticks(range(4),[names[c] for c in n],rotation=40,ha='right');ax.set_ylabel('异文档NLL − 真实上下文NLL（nat）');ax.set_title('都为64维：语境关联是否延伸至尾部？');ax.grid(axis='y',alpha=.13);ax.set_axisbelow(True)
fig.suptitle('分段输出与语境核查：正值表示真实系数更支持真实后继，不等于语义机制',fontsize=16);fig.text(.5,.005,f"NLL主面板175篇/700位置；同token异文档对照{M['permutation_eligible_documents']}篇/{M['permutation_eligible_positions']}位置。误差线为文档bootstrap95%逐点区间。全部加同一训练均值。",ha='center',fontsize=10);fig.tight_layout(rect=[0,.045,1,.93]);save(fig,'01_band_context_checks')
fig,axs=plt.subplots(2,4,figsize=(20,9));maxcount=0
for b in main:
 z=counts[counts.condition==b['condition']];maxcount=max(maxcount,int(z.positions.max()))
for ax,b in zip(axs.flat,main):
 z=counts[counts.condition==b['condition']].sort_values(['positions','token_id'],ascending=[False,True]).head(5);ax.barh(range(len(z)),z.positions,color='#527d9f' if b in main[:5] else '#a8735c');labels=[('[空格]' if x.fragment==' ' else '[不换行空格]' if x.fragment=='\xa0' else repr(x.fragment).replace('\\n','[换行]'))+f' [{x.token_id}]' for x in z.itertuples()];ax.set_yticks(range(len(z)),labels,fontsize=10);ax.invert_yaxis();ax.bar_label(ax.containers[0],padding=3,fontsize=10);ax.set_xlim(0,min(740,maxcount*1.13));ax.set_title(f"{names[b['condition']]} · {b['dimensions']}维",fontsize=12);ax.set_xlabel('首选原始位置数（700个位置）')
fig.suptitle('自然面板实际解码什么：每段最常出现的5个首选ID',fontsize=17);fig.text(.5,.008,'这些是每个位置的下一token首选，不能按图中顺序拼成生成文本；单独片段/另一文字系统不自动等于混乱。',ha='center',fontsize=11);fig.tight_layout(h_pad=2.6,w_pad=2.8,rect=[0,.035,1,.94]);save(fig,'02_actual_output_IDs')
ctx={r['position_uid']:r for r in [json.loads(l) for l in (E/'analysis/contexts.jsonl').read_text().splitlines()]};raw=[json.loads(l) for l in (E/'analysis/raw_outputs.jsonl').read_text().splitlines()];lookup={(r['index'],r['condition']):r for r in raw};caseconds=[b['condition'] for b in bands]+['identity']
for key in M['main_cases']:
 c=ctx[key];i=c['index'];fig,axs=plt.subplots(4,3,figsize=(18,14),gridspec_kw={'hspace':.90,'wspace':.95});xmax=min(1.,max(max(t['probability'] for t in lookup[i,co]['top20'][:3]) for co in caseconds)*1.17)
 for ax,co in zip(axs.flat,caseconds):
  r=lookup[i,co];top=r['top20'][:3];items=[(t['id'],t['fragment'],t['probability']) for t in top]
  if c['target_id'] not in [x[0] for x in items]:items.append((c['target_id'],c['target_fragment'],r['target_probability']))
  bars=ax.barh(range(len(items)),[x[2] for x in items],color=['#b95b49' if x[0]==c['target_id'] else '#567e9d' for x in items]);labels=[repr(x[1]).replace('\\n','[换行]')+f' [{x[0]}]' for x in items];ax.set_yticks(range(len(items)),labels,fontsize=9);ax.invert_yaxis();ax.set_xlim(0,xmax);ax.bar_label(bars,labels=[f'{x[2]:.2e}' if x[2]<.001 else f'{x[2]:.3f}' for x in items],padding=2,fontsize=9);ax.set_title((names.get(co,'原模型'))+f"\n真实后继排名{r['target_rank']}；NLL {r['NLL']:.2f}",fontsize=11);ax.set_xlabel('下一token概率')
 title=f"{c['seq_id']} · 当前0基位置{c['position_zero_based']}（第{c['position_one_based']}个token） · ID{c['input_id']} {repr(c['input_fragment'])}"
 fig.suptitle(title,fontsize=16,y=.995);fig.text(.5,.958,'完整可见前文见casebook_cn.md；当前句子已见部分：'+c['current_visible_sentence_or_paragraph'].replace('\n',' / '),ha='center',fontsize=11);fig.text(.5,.006,'每格该区间前三候选；若真实后继不在前三，另列红色精确概率。所有区间单独投影、加同一训练均值；同图统一横轴尺度。',ha='center',fontsize=10);fig.subplots_adjust(top=.90,bottom=.055);save(fig,'03_case_'+c['seq_id'][-3:])
print('aggregate/context/threefixedcasefiguresrendered')
# Compact literal candidate table for reading directly below each full visible prefix.
from matplotlib.patches import Rectangle
for key in M['main_cases']:
 c=ctx[key];i=c['index'];co=[b['condition'] for b in main]+['identity'];fig,ax=plt.subplots(figsize=(16,8.2));ax.set_xlim(0,5);ax.set_ylim(0,10.6);ax.axis('off');widths=[1.1,1.,1.,1.,.9];edges=np.r_[0,np.cumsum(widths)];headers=['单独保留的谱段','候选1：片段 [ID]／概率','候选2','候选3','真实后继：概率／排名']
 for j,h in enumerate(headers):ax.text((edges[j]+edges[j+1])/2,10.05,h,ha='center',va='center',fontsize=11,weight='bold')
 for row,name in enumerate(co):
  y=9.1-row;record=lookup[i,name];label=names.get(name,'原模型（不投影）');ax.text(.55,y,label,ha='center',va='center',fontsize=12)
  for col,t in enumerate(record['top20'][:3],1):
   x0=edges[col];alpha=min(.65,.10+.9*t['probability']);ax.add_patch(Rectangle((x0+.02,y-.40),widths[col]-.04,.80,facecolor='#4c84a3',alpha=alpha,edgecolor='none'));piece=('[空格]' if t['fragment']==' ' else repr(t['fragment']).replace('\\n','[换行]'));ax.text(x0+widths[col]/2,y,f"{piece} [{t['id']}]\n{100*t['probability']:.3f}%",ha='center',va='center',fontsize=11)
  ax.add_patch(Rectangle((edges[4]+.02,y-.4),widths[4]-.04,.8,facecolor='#c66958',alpha=.13,edgecolor='none'));ax.text(edges[4]+widths[4]/2,y,f"{probstr(record['target_probability'])}\n第{record['target_rank']}名",ha='center',va='center',fontsize=11)
  ax.plot([0,5],[y-.5,y-.5],color='#dddddd',lw=.5)
 fig.suptitle(f"{c['seq_id']}：0基位置{c['position_zero_based']}／第{c['position_one_based']}个token；当前ID{c['input_id']} {repr(c['input_fragment'])}",fontsize=16,y=.99);fig.text(.5,.935,f"真实后继ID{c['target_id']} {repr(c['target_fragment'])}；各行在同一完整可见前文下预测",ha='center',fontsize=12);fig.text(.5,.012,'方框蓝色仅表示候选概率，不是语义相似度。片段不是完整词；只预测当前位置的下一token，不拼接成生成句子。',ha='center',fontsize=10);fig.subplots_adjust(top=.91,bottom=.045,left=.025,right=.995);save(fig,'04_case_'+c['seq_id'][-3:]+'_compact')
