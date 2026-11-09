import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,shutil,textwrap
import numpy as np,pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager,FontProperties
E=Path(__file__).resolve().parents[1];cfg=json.load(open(E/'manifest.json'));P=Path(cfg['project_dir']);S=pd.read_csv(E/'analysis/summary_metrics.csv');D=pd.read_csv(E/'analysis/position_metrics.csv');R=[json.loads(l) for l in (E/'data/positions.jsonl').read_text().splitlines()]
font='/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030/presentation_variants/near_single_domain_20261030/fonts/NotoSansCJKsc-Regular.otf';fontManager.addfont(font);plt.rcParams.update({'font.family':FontProperties(fname=font).get_name(),'axes.unicode_minus':False,'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':160})
coverage=pd.read_csv(E/'analysis/group_coverage.csv')
gnames={'format':'空白／标点','nonformat_common':'参考常见ID，排除格式','nonformat_other':'其余ID，排除格式'};snames={'all_prefix':'全前缀有效位置投影','target_only':'仅当前目标位置投影'};colors=['#b77a1c','#267bac','#925ea2']
def save(fig,name):
 for ext in ['png','pdf']:
  fig.savefig(E/'figures'/f'{name}.{ext}',bbox_inches='tight');shutil.copy2(E/'figures'/f'{name}.{ext}',P/'figures'/f'{name}.{ext}')
 plt.close(fig)
def get(scope,group,metric,cond='head64',readout='continuation'):
 return S[(S.panel=='natural')&(S.scope==scope)&(S.group==group)&(S.metric==metric)&(S.condition==cond)&(S.readout==readout)].sort_values('layer')
# Main: one question, same original-top1 classes, two intervention scopes.
fig,ax=plt.subplots(1,2,figsize=(14,5.5),sharey=True)
for a,scope in zip(ax,['all_prefix','target_only']):
 for color,(g,label) in zip(colors,gnames.items()):
  z=get(scope,g,'top1_agreement');a.plot(z.layer,z['mean']*100,c=color,label=label+f"（{int(coverage[(coverage.panel=='natural')&(coverage.group==g)].iloc[0].positions)}位置）",lw=2);a.fill_between(z.layer,z.ci_low*100,z.ci_high*100,color=color,alpha=.13)
 a.axhline(100,c='#333333',ls=':',lw=1);a.set_ylim(-2,103);a.set_xlim(1,28);a.set_xticks([1,4,8,12,16,20,24,28]);a.set_title(snames[scope]);a.set_xlabel('单独干预第几层（1—28）');a.grid(alpha=.15)
ax[0].set_ylabel('最终首选与完整模型相同的比例（%）');ax[0].legend(fontsize=9,loc='best');fig.suptitle('只保留该层前64主成分，继续后续原网络',fontsize=16);fig.text(.5,.005,'175篇／700位置；先在文档内按组平均，再对文档等权。阴影：按文档重采样的逐点95%区间；首选一致不是预测正确。',ha='center',fontsize=9);fig.tight_layout(rect=[0,.04,1,.94]);save(fig,'01_layerwise_top1_preservation')
# Native task loss and intervention magnitude are separate panels, not combined units.
fig,ax=plt.subplots(2,2,figsize=(14,9),sharex=True)
for col,scope in enumerate(['all_prefix','target_only']):
 for cond,c,ls,label in [('head64','#277aab','-','头64维'),('mean_only','#b05b4a','--','仅参考均值')]:
  z=get(scope,'ALL','NLL',cond);ax[0,col].plot(z.layer,z['mean'],c=c,ls=ls,label=label);ax[0,col].fill_between(z.layer,z.ci_low,z.ci_high,color=c,alpha=.12)
 zs=[get(scope,'ALL','NLL',f'random{s}') for s in cfg['random_seeds']];v=np.stack([z['mean'].to_numpy() for z in zs]);ax[0,col].plot(range(1,29),v.mean(0),c='#777777',label='随机64维：3种子均值');ax[0,col].fill_between(range(1,29),v.min(0),v.max(0),color='#777777',alpha=.15)
 base=S[(S.panel=='natural')&(S.condition=='identity')&(S.group=='ALL')&(S.metric=='NLL')]['mean'].iloc[0];ax[0,col].axhline(base,c='#222222',ls=':',label='完整模型');ax[0,col].set_title(snames[scope]);ax[0,col].set_ylabel('真实后继负对数概率（nat；越低越好）');ax[0,col].legend(fontsize=9);ax[0,col].grid(alpha=.15)
 z=get(scope,'ALL','target_retained_energy');ax[1,col].plot(z.layer,z['mean']*100,c='#277aab',label='头64：当前目标位置');ax[1,col].fill_between(z.layer,z.ci_low*100,z.ci_high*100,color='#277aab',alpha=.12)
 zs=[get(scope,'ALL','target_retained_energy',f'random{s}') for s in cfg['random_seeds']];v=np.stack([z['mean'].to_numpy() for z in zs]);ax[1,col].plot(range(1,29),v.mean(0)*100,c='#777777',label='随机64维：3种子均值');ax[1,col].fill_between(range(1,29),v.min(0)*100,v.max(0)*100,color='#777777',alpha=.15);ax[1,col].set_ylabel('目标位置保留的中心化平方范数（%）');ax[1,col].set_xlabel('单独干预第几层');ax[1,col].set_xticks([1,4,8,12,16,20,24,28]);ax[1,col].legend(fontsize=9);ax[1,col].grid(alpha=.15)
fig.suptitle('最终预测损失与投影保留能量：两个不同指标',fontsize=16);fig.text(.5,.006,'自然面板175篇／700位置，文档等权；随机灰带为3种子的范围，非独立文档区间。等64维不代表相同能量／干预幅度。',ha='center',fontsize=9);fig.tight_layout(rect=[0,.04,1,.95]);save(fig,'02_layerwise_loss_and_energy')
fig,ax=plt.subplots(3,2,figsize=(14,11),sharex=True,sharey=True)
for row,(g,label) in enumerate(gnames.items()):
 for col,scope in enumerate(['all_prefix','target_only']):
  a=ax[row,col]
  for cond,c,ls,lab in [('head64',colors[row],'-','头64维'),('mean_only','#af6559','--','仅均值')]:
   z=get(scope,g,'top1_agreement',cond);a.plot(z.layer,z['mean']*100,c=c,ls=ls,label=lab)
  zs=[get(scope,g,'top1_agreement',f'random{s}') for s in cfg['random_seeds']];v=np.stack([z['mean'].to_numpy() for z in zs]);a.plot(range(1,29),v.mean(0)*100,c='#777777',label='随机64维');a.fill_between(range(1,29),v.min(0)*100,v.max(0)*100,color='#777777',alpha=.14);a.set_title(label+'｜'+snames[scope]);a.set_ylim(-2,103);a.grid(alpha=.15);a.set_ylabel('首选一致（%）')
  if row==0:a.legend(fontsize=9)
for a in ax[-1]:a.set_xlabel('干预层');a.set_xticks([1,4,8,12,16,20,24,28])
fig.suptitle('附录：头64、仅均值与等维随机参照',fontsize=16);fig.tight_layout(rect=[0,0,1,.97]);save(fig,'A01_classwise_controls')
# Cases: read exact raw probability records, keep continuation and direct-head separate.
raw=[json.loads(l) for l in (E/'analysis/raw_outputs.jsonl').read_text().splitlines()];lookup={(r['index'],r['layer'],r['condition'],r['scope'],r['readout']):r for r in raw};fixed=cfg['fixed_cases'];selected=[]
# Outcome-selected examples distinct: least/most natural all-prefix head64 agreement across layers.
a=D[(D.panel=='natural')&(D.condition=='head64')&(D.scope=='all_prefix')&(D.readout=='continuation')].groupby('index').top1_agreement.sum().sort_index();selected.extend([('结果后选：跨层保持最多',int(a.idxmax())),('结果后选：跨层保持最少',int(a.idxmin()))])
# Outcome-selected scope contrast, explicitly exploratory rather than a preselected semantic example.
zz=D[(D.panel=='natural')&(D.condition=='head64')&(D.readout=='continuation')&(D.layer==1)].pivot(index='index',columns='scope',values='top1_agreement');eligible=zz[(zz.all_prefix==False)&(zz.target_only==True)]
if len(eligible):selected.append(('结果后选：第1层全前缀改变、仅目标保持；按index首例',int(eligible.index.min())))
zz=D[(D.panel=='natural')&(D.condition=='head64')&(D.readout=='continuation')&(D.scope=='all_prefix')].pivot(index='index',columns='layer',values='top1_agreement');eligible=zz[(zz[1]==False)&(zz[28]==True)]
if len(eligible):selected.append(('结果后选：第28层保持但第1层改变；按index首例',int(eligible.index.min())))
json.dump(selected,open(E/'analysis/outcome_selected_cases.json','w'),ensure_ascii=False,indent=2)
casebook=['# 完整输入与逐层候选\n\n固定案例在新输出前选择；结果后选案例另标。每个位置t只看到截至当前token的前文。原文后继是目标，不一定是完整模型首选。\n']
def fmt(r,n=3):return '; '.join(f"ID{x['id']} {x['fragment']!r} {x['probability']*100:.4g}%" for x in r['top10'][:n])
for i in dict.fromkeys(fixed+[x[1] for x in selected]):
 m=R[i];base=lookup[(i,0,'identity','none','continuation')];designation='输出前固定' if i in fixed else '结果后按固定规则选择';casebook.append(f"\n## {m['position_uid']}（{designation}）\n\n当前0基位置{m['position']}，即第{m['position']+1}个token；ID{m['input_id']}，片段{m['input_fragment']!r}。原文后继ID{m['target_id']} {m['target_fragment']!r}。\n\n完整可见前文：\n\n```text\n{m['visible_prefix']}\n```\n\n完整模型：{fmt(base,10)}。真实后继P={base['target_probability']:.8g}，排名{base['target_rank']}。\n")
 for scope in ['all_prefix','target_only']:
  casebook.append('\n### 继续后续网络：'+snames[scope]+'\n\n|层|前3候选（ID／片段／概率）|原首选概率／排名|真实后继概率／排名|\n|---|---|---|---|')
  for l in range(1,29):
   r=lookup[(i,l,'head64',scope,'continuation')];casebook.append(f"|{l}|{fmt(r)}|{r['full_top1_probability']:.8g} / {r['full_top1_rank']}|{r['target_probability']:.8g} / {r['target_rank']}|")
 casebook.append('\n### 直接输出头诊断：不是继续后续网络\n\n|层|未投影前3|头64前3|\n|---|---|---|')
 for l in range(1,29):casebook.append(f"|{l}|{fmt(lookup[(i,l,'unprojected','target_only','direct_head')])}|{fmt(lookup[(i,l,'head64','target_only','direct_head')])}|")
 if i in fixed[:6] or i in [x[1] for x in selected] or m['seq_id'] in ['R11_A02_134','R11_A02_242','R11_A02_434']:
  fig,ax=plt.subplots(figsize=(16,9));ax.axis('off');head=f"{m['seq_id']}｜当前第{m['position']+1}个token（0基{m['position']}）ID{m['input_id']} {m['input_fragment']!r}\n真实后继ID{m['target_id']} {m['target_fragment']!r}｜完整模型：{fmt(base)}";fig.text(.03,.98,head,va='top',fontsize=12)
  # clearly label displayed tail as excerpt; entire prefix in casebook above.
  excerpt=m['visible_prefix'][-360:];fig.text(.03,.90,'可见前文末段（完整前文见配套案例记录）：\n'+ '\n'.join(textwrap.wrap(excerpt,width=132,replace_whitespace=False)),va='top',fontsize=10)
  lines=[['读出方式／层','实际前三候选（精确ID、片段、概率）','原首选排名','真实后继排名']]
  for scope in ['all_prefix','target_only']:
   for l in [1,7,14,21,28]:
    r=lookup[(i,l,'head64',scope,'continuation')];lines.append([('继续／全前缀' if scope=='all_prefix' else '继续／仅目标')+f' L{l}',fmt(r),str(r['full_top1_rank']),str(r['target_rank'])])
  for l in [7,14,28]:
   for cond,label in [('unprojected','原表征'),('head64','头64')]:
    r=lookup[(i,l,cond,'target_only','direct_head')];lines.append([f'直接头／{label} L{l}',fmt(r),str(r['full_top1_rank']),str(r['target_rank'])])
  tab=ax.table(cellText=lines[1:],colLabels=lines[0],colWidths=[.18,.62,.10,.10],cellLoc='left',loc='center',bbox=[0,0,1,.77]);tab.auto_set_font_size(False);tab.set_fontsize(9);tab.scale(1,1.4)
  for (row,col),cell in tab.get_celld().items():
   if row==0:cell.set_facecolor('#e4ebef')
   elif row>=11:cell.set_facecolor('#f3eee7')
  fig.text(.03,.012,'直接输出头经过最终norm与head，但未经过剩余block；中间层可能不匹配，不能作为生成能力排名。片段按token保留，不当成完整词。',fontsize=9);save(fig,f'03_case_{i:03d}')
import re
case_text=re.sub(r'<\|[^>]*\|>',lambda m:m.group(0).replace('|',r'\|'),'\n'.join(casebook)+'\n')
(P/'casebook_cn.md').write_text(case_text);(E/'casebook_cn.md').write_text(case_text);print('rendered fixed cases',fixed,'outcome-selected',selected)
