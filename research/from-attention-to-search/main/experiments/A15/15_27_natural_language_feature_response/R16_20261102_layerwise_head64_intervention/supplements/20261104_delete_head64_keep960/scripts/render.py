import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,shutil,textwrap,re
import numpy as np,pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager,FontProperties
E=Path(__file__).resolve().parents[1];c=json.load(open(E/'manifest.json'));P=Path(c['project_dir']);S=pd.read_csv(E/'analysis/summary_metrics.csv');J=pd.read_csv(E/'analysis/joint_patterns.csv');A=pd.read_csv(E/'analysis/position_metrics.csv');RR=[json.loads(l) for l in (E/'data/positions.jsonl').read_text().splitlines()]
font='/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030/presentation_variants/near_single_domain_20261030/fonts/NotoSansCJKsc-Regular.otf';fontManager.addfont(font);plt.rcParams.update({'font.family':FontProperties(fname=font).get_name(),'axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'font.size':10,'savefig.dpi':155})
scopes=['target_only','all_prefix'];sn={'target_only':'仅当前位置','all_prefix':'整个有效前缀'};cn={'keep_head64':'保留头64（旧结果）','delete_head64':'删除头64，保留后960'};colors={'keep_head64':'#307da7','delete_head64':'#bf702e'}
def q(scope,metric,cond,group='ALL',panel='natural'):return S[(S.panel==panel)&(S.scope==scope)&(S.metric==metric)&(S.condition==cond)&(S.group==group)].sort_values('layer')
def save(fig,name):
 for ext in ['png','pdf']:
  fig.savefig(E/'figures'/f'{name}.{ext}',bbox_inches='tight');shutil.copy2(E/'figures'/f'{name}.{ext}',P/'figures'/f'{name}.{ext}')
 plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(14,5.6),sharey=True)
for ax,scope in zip(axes,scopes):
 for cond in ['keep_head64','delete_head64']:
  z=q(scope,'top1_agreement',cond);ax.plot(z.layer,z['mean']*100,c=colors[cond],label=cn[cond],lw=2);ax.fill_between(z.layer,z.ci_low*100,z.ci_high*100,color=colors[cond],alpha=.12)
 vv=np.stack([q(scope,'top1_agreement',f'delete_random{s}')['mean'] for s in c['seeds']['random']]);ax.plot(range(1,29),vv.mean(0)*100,c='#777777',ls='--',label='删除随机64：3种子均值');ax.fill_between(range(1,29),vv.min(0)*100,vv.max(0)*100,color='#777777',alpha=.1);ax.axhline(100,c='#222222',ls=':',lw=1);ax.set_title(sn[scope]);ax.set_xticks([1,4,8,12,16,20,24,28]);ax.set_xlim(1,28);ax.set_ylim(-2,103);ax.set_xlabel('单独干预第几层（1—28）');ax.grid(alpha=.15)
axes[0].set_ylabel('最终原首选保持比例（%）');axes[0].legend(fontsize=9);fig.suptitle('相反谱操作：保留头64 vs 删除头64',fontsize=16);fig.text(.5,.005,'同一175篇／700位置；每篇4位置，文档等权。彩色阴影为文档95%逐点区间；随机灰带为种子范围。保留维数不同，能量未匹配。',ha='center',fontsize=9);fig.tight_layout(rect=[0,.04,1,.94]);save(fig,'01_keep_delete_layerwise')
fig,axes=plt.subplots(2,3,figsize=(17,9))
for row,scope in enumerate(scopes):
 for col,(metric,label,scale) in enumerate([('NLL','真实后继负对数概率（nat；低为好）',1),('KL_full','与完整输出分布的KL（nat；低为接近）',1),('target_retained_energy','当前位置中心化能量保留（%）',100)]):
  ax=axes[row,col]
  for cond in ['keep_head64','delete_head64']:
   z=q(scope,metric,cond);ax.plot(z.layer,z['mean']*scale,c=colors[cond],label=cn[cond],lw=2);ax.fill_between(z.layer,z.ci_low*scale,z.ci_high*scale,color=colors[cond],alpha=.12)
  vv=np.stack([q(scope,metric,f'delete_random{s}')['mean'] for s in c['seeds']['random']]);ax.plot(range(1,29),vv.mean(0)*scale,c='#777777',ls='--',label='删除随机64');ax.fill_between(range(1,29),vv.min(0)*scale,vv.max(0)*scale,color='#777777',alpha=.1)
  if metric in ['NLL','KL_full']:
   base=S[(S.panel=='natural')&(S.condition=='identity')&(S.group=='ALL')&(S.metric==metric)]['mean'].iloc[0];ax.axhline(base,c='#222222',ls=':',label='完整模型')
  ax.set_title(sn[scope]+'｜'+label);ax.set_xlabel('干预层');ax.set_xticks([1,4,8,12,16,20,24,28]);ax.grid(alpha=.15)
  if col==0:ax.legend(fontsize=8)
fig.suptitle('预测质量、分布变化与保留能量：分别测量',fontsize=16);fig.text(.5,.005,'不能把原首选一致当成正确；NLL与KL分别衡量原文目标和接近原模型。删除随机64仅匹配维数，未匹配能量。',ha='center',fontsize=10);fig.tight_layout(rect=[0,.035,1,.94]);save(fig,'02_loss_KL_energy')
fig,axes=plt.subplots(3,2,figsize=(14,10.5),sharex=True,sharey=True)
for row,(group,label,nn,nd) in enumerate([('format','空白／标点',108,81),('nonformat_common','参考常见ID，排除格式',386,163),('nonformat_other','其余ID，排除格式',206,125)]):
 for col,scope in enumerate(scopes):
  ax=axes[row,col]
  for cond in ['keep_head64','delete_head64']:
   z=q(scope,'top1_agreement',cond,group);ax.plot(z.layer,z['mean']*100,c=colors[cond],label=cn[cond]);ax.fill_between(z.layer,z.ci_low*100,z.ci_high*100,color=colors[cond],alpha=.12)
  ax.set_title(f'{label}：{nd}篇／{nn}位置｜{sn[scope]}');ax.set_ylim(-2,103);ax.set_ylabel('原首选保持（%）');ax.grid(alpha=.15);ax.set_xticks([1,4,8,12,16,20,24,28])
  if row==0:ax.legend(fontsize=8)
for ax in axes[-1]:ax.set_xlabel('干预层')
fig.suptitle('哪些原预测更容易保持？类别来自完整模型原首选',fontsize=16);fig.text(.5,.005,'组内文档等权，文档可跨组；“其余ID”不是“细语义／上下文token”。颜色仍为相反干预操作。',ha='center',fontsize=9);fig.tight_layout(rect=[0,.035,1,.95]);save(fig,'03_recovery_by_original_type')
fig,axes=plt.subplots(1,2,figsize=(14,5.5),sharey=True)
patterns=['both','keep_only','delete_only','neither'];pn={'both':'两者均保持','keep_only':'仅保留头64时保持','delete_only':'仅删除头64时保持','neither':'两者均改变'};pcolors=['#91b89d','#4386ad','#d49558','#c8c8c8']
for ax,scope in zip(axes,scopes):
 vals=[J[(J.panel=='natural')&(J.scope==scope)&(J.group=='ALL')&(J.pattern==p)].sort_values('layer')['mean'].to_numpy()*100 for p in patterns];assert np.max(abs(np.sum(vals,0)-100))<1e-9;ax.stackplot(range(1,29),*vals,labels=[pn[p] for p in patterns],colors=pcolors,alpha=.95);ax.set_ylim(0,100);ax.set_xlim(1,28);ax.set_title(sn[scope]);ax.set_xlabel('干预层');ax.set_xticks([1,4,8,12,16,20,24,28])
axes[0].set_ylabel('配对位置的文档等权比例（%）');axes[0].legend(fontsize=8,loc='lower left');fig.suptitle('同一位置的保留／删除结果如何组合？',fontsize=16);fig.text(.5,.005,'两种操作共享训练均值、其他位置及剩余网络；“都保持”不证明独立冗余，“都改变”不证明功能交互。',ha='center',fontsize=9);fig.tight_layout(rect=[0,.04,1,.94]);save(fig,'04_joint_recovery_patterns')
# Casebook: exact input and all28layer top3; rawJSON has top10.
need=set(c['fixed_cases']);jp=pd.read_csv(E/'analysis/joint_position_results.csv');chosen=[]
for pattern in patterns:
 z=jp[(jp.panel=='natural')&(jp.layer==28)&(jp.scope=='target_only')&(jp.pattern==pattern)].sort_values('position_uid')
 if len(z):chosen.append({'pattern':pattern,'index':int(z.iloc[0]['index']),'position_uid':z.iloc[0].position_uid});need.add(int(z.iloc[0]['index']))
(E/'analysis/outcome_selected_cases.json').write_text(json.dumps(chosen,ensure_ascii=False,indent=2)+'\n')
lookup={}
for line in (E/'analysis/raw_outputs.jsonl').open():
 r=json.loads(line)
 if r['index'] in need and r['condition'] in ['identity','keep_head64','delete_head64']:lookup[(r['index'],r['layer'],r['scope'],r['condition'])]=r
def tokens(r,n=3):return '; '.join(f"ID{t['id']} {t['fragment']!r} {t['probability']*100:.5g}%" for t in r['top10'][:n])
book=['# 相反谱操作的完整真实输入与逐层输出\n\n9例沿用输出前固定规则。另列末层四格结果后选首例（按UID排序），未作为确认数据。所有概率为native下一token，子词不当完整词。\n']
for i in list(dict.fromkeys(c['fixed_cases']+[x['index'] for x in chosen])):
 m=RR[i];base=lookup[(i,0,'none','identity')];typ='原固定' if i in c['fixed_cases'] else '结果后选';book.append(f"\n## {m['position_uid']}（{typ}）\n\n当前第{m['position']+1}个token，0基{m['position']}，ID{m['input_id']} {m['input_fragment']!r}；原文后继ID{m['target_id']} {m['target_fragment']!r}。\n\n完整可见输入：\n\n```text\n{m['visible_prefix']}\n```\n\n完整模型：{tokens(base,10)}。真实目标P={base['target_probability']:.9g}，排名{base['target_rank']}。\n")
 for scope in scopes:
  book.append(f'\n### {sn[scope]}，继续后续网络\n\n|层|保留头64：前3候选|删除头64：前3候选|保留：目标P／排名|删除：目标P／排名|\n|---|---|---|---|---|')
  for l in range(1,29):
   k=lookup[(i,l,scope,'keep_head64')];d=lookup[(i,l,scope,'delete_head64')];book.append(f"|{l}|{tokens(k)}|{tokens(d)}|{k['target_probability']:.9g} / {k['target_rank']}|{d['target_probability']:.9g} / {d['target_rank']}|")
 if i in [211,284,676] or i in [x['index'] for x in chosen]:
  excerpt=[x for x in m['visible_prefix'].split('\n\n') if x.strip()][-1]
  if len(excerpt)>600:
   start=excerpt.find(' ',len(excerpt)-600);excerpt=excerpt[start+1:]
  fig,ax=plt.subplots(figsize=(17,8.8));ax.axis('off');fig.text(.025,.98,f"{m['seq_id']}｜当前第{m['position']+1}个token（0基{m['position']}），ID{m['input_id']} {m['input_fragment']!r}\n真实后继ID{m['target_id']} {m['target_fragment']!r}｜完整模型：{tokens(base)}",va='top',fontsize=11)
  fig.text(.025,.90,'可见输入末段（完整输入见配套casebook）：\n'+'\n'.join(textwrap.wrap(excerpt,width=150,replace_whitespace=False)),va='top',fontsize=10)
  rows=[]
  for scope in scopes:
   for l in [1,7,14,21,28]:
    for cond in ['keep_head64','delete_head64']:
     r=lookup[(i,l,scope,cond)];rows.append([f"{sn[scope]} L{l}", '保留头64' if cond=='keep_head64' else '删除头64',tokens(r,2),f"{r['target_probability']*100:.5g}% / {r['target_rank']}"])
  table=ax.table(cellText=rows,colLabels=['干预位置／层','谱操作','实际前2候选：ID、片段、概率','原文后继概率／排名'],cellLoc='left',colWidths=[.15,.1,.58,.17],bbox=[0,0,1,.78]);table.auto_set_font_size(False);table.set_fontsize(9)
  for (r,cl),cell in table.get_celld().items():
   if r==0:cell.set_facecolor('#e2e9ed')
   elif r%2==0:cell.set_facecolor('#f5ecdf')
  fig.text(.025,.012,'同一前文和同一PCA；每次只干预一层。所有行均经过原剩余网络、最终norm与输出头。相反操作保留维数不同。',fontsize=9);save(fig,f'05_case_{i:03d}')
text='\n'.join(book)+'\n';text=re.sub(r'<\|[^>]*\|>',lambda m:m.group(0).replace('|',r'\|'),text)
for b in [P,E]:(b/'casebook_cn.md').write_text(text)
print('fixed',c['fixed_cases'],'postselected',chosen)
