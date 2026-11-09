import os
os.environ['MPLBACKEND']='Agg'
from pathlib import Path
import json,shutil,textwrap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties,fontManager
P=Path(__file__).resolve().parents[1];E=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response')/P.name
font='/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030/presentation_variants/near_single_domain_20261030/fonts/NotoSansCJKsc-Regular.otf'
fontManager.addfont(font);plt.rcParams.update({'font.family':FontProperties(fname=font).get_name(),'axes.unicode_minus':False,'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':150})
s=pd.read_csv(E/'analysis/summary_metrics.csv');c=pd.read_csv(E/'analysis/paired_contrasts.csv');m=json.load(open(E/'manifest.json'));ks=[1,4,16,64,128,256,512,768,1024];colors=['#31689e','#9b4b76'];recovery=pd.read_csv(E/'analysis/recovery_by_full_top1_type.csv');panels=[('the','固定 the 后继：37篇／37位置'),('natural','自然位置：175篇／700位置')]
def one(panel,cond,metric):return s[(s.panel==panel)&(s.condition==cond)&(s.metric==metric)].iloc[0]
def line(ax,panel,metric,col):
 a=[one(panel,'k'+str(k),metric) for k in ks];y=np.array([x['mean'] for x in a]);lo=np.array([x['ci_low'] for x in a]);hi=np.array([x['ci_high'] for x in a]);ax.plot(ks,y,'o-',color=col,label='嵌套前 k 维');ax.fill_between(ks,lo,hi,color=col,alpha=.15);ax.axhline(one(panel,'mean_only',metric)['mean'],c='#888888',ls=':',label='仅训练均值');ax.axhline(one(panel,'identity',metric)['mean'],c='#222222',ls='--',label='原模型');ax.set_xscale('log',base=2);ax.set_xticks([1,4,16,64,256,1024],[1,4,16,64,256,1024]);ax.set_xlabel('前 k 个方差方向（维）');ax.grid(alpha=.16)
def save(fig,name):
 fig.savefig(E/'figures'/f'{name}.png',bbox_inches='tight');fig.savefig(E/'figures'/f'{name}.pdf',bbox_inches='tight');plt.close(fig)
 for ext in ['png','pdf']:shutil.copy2(E/'figures'/f'{name}.{ext}',P/'figures'/f'{name}.{ext}')
fig,axs=plt.subplots(2,3,figsize=(15,8.8))
for row,(panel,label) in enumerate(panels):
 for j,(metric,title) in enumerate([('NLL','真实后继的负对数概率（nat；低为好）'),('KL_full','与原模型分布的 KL（nat；低为接近）'),('entropy','输出熵（nat；分散程度）')]):
  ax=axs[row,j];line(ax,panel,metric,colors[row]);ax.set_title(title);ax.set_ylabel(label if j==0 else '')
axs[0,0].legend(fontsize=9);fig.suptitle('累积加入方向恢复了什么：准确性、接近原模型与分布熵分开测量',fontsize=16);fig.text(.5,.005,'阴影为按文档重采样的95%区间；自然面板先在每篇4个位置内平均。固定同一前文、目标、均值、原生 RMSNorm 与输出头。',ha='center',fontsize=10);fig.tight_layout(rect=[0,.03,1,.95]);save(fig,'01_cumulative_native_metrics')
fig,axs=plt.subplots(2,3,figsize=(16.5,8.8))
for row,(panel,label) in enumerate(panels):
 ax=axs[row,0];line(ax,panel,'freq_top1pct',colors[row]);ax.set_title('独立训练参考中最高频1% ID的输出质量');ax.set_ylabel(label+'\n概率质量（0–1）');ax.legend(fontsize=8,loc='upper right');
 ax=axs[row,1]
 for group,glabel,gcol in [('format','空白／标点','#c18128'),('nonformat_common','常见ID（非格式）','#327ca0'),('nonformat_other','其余ID（非格式）','#945f9c')]:
  z=recovery[(recovery.panel==panel)&(recovery.group==group)&(recovery.metric=='top1_agreement')]
  if z.empty:continue
  n=int(z.iloc[0]['documents']);positions=int(z.iloc[0]['positions'])
  if n<5:
   ax.text(.03,.94,'格式组仅1篇：证据不足',transform=ax.transAxes,fontsize=9,color='#777777');continue
  zz=z.set_index('condition').loc[['k'+str(k) for k in ks]];yy=zz['mean'].to_numpy();ax.plot(ks,yy,'o-',c=gcol,label=f'{glabel} {n}篇/{positions}位置');ax.fill_between(ks,zz.ci_low.to_numpy(),zz.ci_high.to_numpy(),color=gcol,alpha=.1)
 ax.set_xscale('log',base=2);ax.set_xticks([1,16,64,256,1024],[1,16,64,256,1024]);ax.set_ylim(-.025,1.04);ax.set_xlabel('前 k 维');ax.set_ylabel('恢复原模型首选ID的比例');ax.set_title('按原模型首选ID的表面类型／参考频率分组');ax.legend(fontsize=8,loc='lower right');ax.grid(alpha=.15)
 ax=axs[row,2];cond=['k128','head_middle','head_tail','head_random1034','head_random1035','head_random1036'];labels=['加下64','加中64','加尾64','加随机1','加随机2','加随机3'];a=[c[(c.panel==panel)&(c.baseline=='k64')&(c.condition==x)&(c.metric=='NLL')].iloc[0] for x in cond];y=-np.array([v['difference_condition_minus_baseline'] for v in a]);lo=-np.array([v['ci_high'] for v in a]);hi=-np.array([v['ci_low'] for v in a]);ax.bar(range(6),y,color=[colors[row]]+['#999999']*2+['#b8c6d3']*3);ax.errorbar(range(6),y,yerr=[y-lo,hi-y],fmt='none',c='black',capsize=3);ax.axhline(0,c='black',lw=.8);ax.set_xticks(range(6),labels,rotation=22);ax.set_ylabel('相对头64的 NLL 改善（nat；正为好）');ax.set_title('固定头64，再增加64个正交方向');
fig.suptitle('词频与等维参照：常见程度不是语义粒度；新增维数相同',fontsize=16);fig.text(.5,.006,'频率来自固定4,194,304训练token，非特殊ID加0.5平滑；特殊／填充输出质量另报。恢复曲线为组内文档95%区间；新增增益为配对文档区间。',ha='center',fontsize=10);fig.tight_layout(rect=[0,.035,1,.95]);save(fig,'02_frequency_and_equal_rank_controls')
# Show native top3 distributions, including true target even when absent from top3; no zero-filling missing probabilities.
pos=[json.loads(l) for l in (E/'data/positions.jsonl').read_text().splitlines()];oo=[json.loads(l) for l in (E/'analysis/raw_outputs.jsonl').read_text().splitlines()];lookup={(x['index'],x['condition']):x for x in oo};names=['282','292','262','297','090'];fig=plt.figure(figsize=(21,14));cc=['mean_only','k64','k256','identity'];titles=['仅训练均值','前64维','前256维','原模型（恒等）']
for row,n in enumerate(names):
 i=next(i for i,r in enumerate(pos) if r['seq_id']=='R11_A02_'+n and r['panel']=='the');r=pos[i];rowmax=min(1.,1.16*max(max(z['probability'] for z in lookup[i,c]['top20'][:3]) for c in cc))
 for col,cond in enumerate(cc):
  ax=fig.add_axes([.095+.24*col,.79-.165*row,.135,.09]);z=lookup[i,cond];top=z['top20'][:3];target=r['target_id'];items=[(x['id'],x['fragment'],x['probability']) for x in top]
  if target not in [x[0] for x in items]:items.append((target,r['target_fragment'],z['target_probability']))
  labels=[repr(x[1]).replace('\\n','[newline]')+'  ['+str(x[0])+']' for x in items];probs=[x[2] for x in items];bars=ax.barh(range(len(items)),probs,color=['#be5546' if x[0]==target else '#527d9e' for x in items]);ax.set_yticks(range(len(items)),labels,fontsize=9);ax.invert_yaxis();ax.set_xlim(0,rowmax);ax.bar_label(bars,labels=[f'{v:.1e}' if v<.001 else f'{v:.3f}' for v in probs],padding=2,fontsize=8);ax.set_xlabel('输出概率（同行同尺度）' if row==4 else '');ax.set_title(f"{titles[col]} · 真目标排名 {z['target_rank']}",fontsize=11)
  if col==0:fig.text(.025,.907-.165*row,f"{n} · {r['topic']} · 可见前文末尾：{r['visible_prefix'][-100:].replace(chr(10),' / ')}",fontsize=11,ha='left')
fig.suptitle('预先固定的真实文本：输出分布与真实后继（红色）',fontsize=17,y=.995);fig.text(.5,.005,'每格展示该条件前三候选；真实目标不在前三时补列其准确概率。[]为token ID，片段不是完整词。完整可见前文与所有条件见原始结果表。',ha='center',fontsize=10);save(fig,'03_fixed_text_output_distributions')
# Spectrum audit as appendix, not a fourth primary story.
a=np.load(E/'data/bases.npz');ev=a['eigenvalues'];fig,ax=plt.subplots(figsize=(10,4));ax.semilogy(np.arange(1,1025),ev,c='#336994');
for lo,hi,label,col in [(1,64,'头64','#afd4ea'),(481,544,'中64','#e4bdcf'),(961,1024,'尾64','#d8d7a9')]:ax.axvspan(lo,hi,color=col,alpha=.6,label=label)
ax.set_xlabel('参考协方差特征值排序（1–1024）');ax.set_ylabel('特征值（模型单位²；对数轴）');ax.set_title('R04发现侧9600位置；复用同一完整秩基底，不构成独立复现');ax.legend();fig.tight_layout();save(fig,'A01_spectrum_audit')
print('rendered three primary figures and spectrum appendix')

# Equal-rank64 controls remain available as an explicit appendix.
fig,axs=plt.subplots(1,2,figsize=(12,4.5))
for row,(panel,label) in enumerate(panels):
 ax=axs[row];cond=['k64','middle','tail','random1031','random1032','random1033'];a=[one(panel,x,'KL_full') for x in cond];y=np.array([v['mean'] for v in a]);err=np.array([[v['mean']-v['ci_low'] for v in a],[v['ci_high']-v['mean'] for v in a]]);ax.bar(range(6),y,color=[colors[row]]+['#999999']*2+['#b8c6d3']*3);ax.errorbar(range(6),y,yerr=err,fmt='none',color='black',capsize=3);ax.set_xticks(range(6),['头64','中64','尾64','随机1','随机2','随机3']);ax.set_ylabel('与原模型的 KL（nat；低为接近）');ax.set_title(label)
fig.tight_layout();save(fig,'A02_equal_rank64_controls')
