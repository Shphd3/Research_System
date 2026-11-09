import os
os.environ['MPLBACKEND']='Agg'
from pathlib import Path
import json,shutil
import numpy as np,pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties,fontManager
E=Path(__file__).resolve().parents[1];P=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response')/E.name
font='/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030/presentation_variants/near_single_domain_20261030/fonts/NotoSansCJKsc-Regular.otf';fontManager.addfont(font);plt.rcParams.update({'font.family':FontProperties(fname=font).get_name(),'axes.unicode_minus':False,'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':160})
S=pd.read_csv(E/'analysis/summary.csv');F=pd.read_csv(E/'analysis/family_metrics.csv');C=pd.read_csv(E/'analysis/primary_feature_contrasts.csv');D=pd.read_csv(E/'analysis/all_paired_contrasts.csv');G=pd.read_csv(E/'analysis/group_spectral_contributions.csv.gz');domains=['biology','mathematics','physics'];names={'biology':'生物','mathematics':'数学','physics':'物理'};freqs=['low','middle','high'];freqcn={'low':'低频','middle':'中频','high':'高频'};col={'low':'#4089a6','middle':'#b075a3','high':'#b0653e'};manifest=[]
def s(domain,condition):return S[(S.domain==domain)&(S.condition==condition)].iloc[0]
def alias(x):return json.load(open(E/'data/conditions.json'))['aliases'].get(x,x)
def point(ax,x,r,m,color,label=None,offset=0):
 y=float(r[m]);ax.errorbar(x+offset,y,yerr=[[max(0,y-r[m+'_low'])],[max(0,r[m+'_high']-y)]],fmt='o',color=color,capsize=3,label=label)
def save(fig,name,question,source):
 fig.text(.5,-.015,'冻结 Qwen3-0.6B-Base｜最后第28个块输出、最终归一化前；随后仅原生归一化与输出头｜R14 数据v1.3',ha='center',fontsize=8)
 fig.text(.5,-.035,'原始表：'+source,ha='center',fontsize=7)
 fig.savefig(E/'figures'/f'{name}.png',bbox_inches='tight');fig.savefig(E/'figures'/f'{name}.pdf',bbox_inches='tight');plt.close(fig)
 for ext in ['png','pdf']:shutil.copy2(E/'figures'/f'{name}.{ext}',P/'figures'/f'{name}.{ext}')
 manifest.append({'figure':name,'question':question,'source':source,'run':E.name,'model':'official Qwen3-0.6B-Base;block27 residual-post before finalnorm;one native RMSNorm+lm_head','independent_units':'12 evaluation families/domain;36 total;two paraphrases not independent','interval':'4000 paired family bootstrap95% pointwise;not measurement noise or training-seed uncertainty'})
conds=['full','mean_only','keep_head16','feature_delete_low','feature_delete_middle','feature_delete_high','crosscoder_reconstruction'];labels=['完整模型','参考平均状态','只留头16','删低频','删中频','删高频','完整字典重建']
fig,axs=plt.subplots(2,3,figsize=(15,8))
for di,d in enumerate(domains):
 for i,c in enumerate(conds):
  r=s(d,c);point(axs[0,di],i,r,'J','#316d9c');point(axs[1,di],i,r,'upper_correct','#8b527f')
  axs[1,di].annotate(f"{int(r.upper_correct_count)}/72",(i,r.upper_correct),xytext=(0,8),textcoords='offset points',ha='center',fontsize=8)
 axs[0,di].axhline(0,color='#555',lw=.8);axs[0,di].set_title(names[d]+'：具体概念的双侧线索区分');axs[0,di].set_ylabel('对称线索区分量（自然对数单位）');axs[1,di].set_title(names[d]+'：上位概念与错误上位概念');axs[1,di].set_ylabel('上位判断正确比例；括号为原始计数');axs[1,di].set_ylim(-.05,1.15)
 for ax in axs[:,di]:ax.set_xticks(range(len(conds)),labels,rotation=24,ha='right');ax.grid(alpha=.15)
fig.suptitle('具体概念区分与上位判断分别测量，不比较两种量尺的绝对降幅',fontsize=15);fig.text(.5,.005,'数据v1.3；每域12家族×2措辞×2具体线索=48次具体判断；上位判断另含宽泛上下文，共72次。误差线按家族重采样。',ha='center',fontsize=9);fig.tight_layout(rect=[0,.035,1,.95]);save(fig,'01_concept_and_upper_judgements','删除组之后具体区分与上位判断各自改变多少？','analysis/summary.csv;family_metrics.csv')
# Full spectral condition matrix is secondary, held to the original requested protocol.
fig,axs=plt.subplots(3,3,figsize=(16,12));ks=[1,16,64,128,256,512,768,1024];bands=list(range(1,9));width=[1,15,48,64,128,256,256,256]
for di,d in enumerate(domains):
 ax=axs[di,0];rr=[s(d,f'keep_head{k}') for k in ks];ax.plot(ks,[r.J for r in rr],'o-',label='累计谱头');ax.fill_between(ks,[r.J_low for r in rr],[r.J_high for r in rr],alpha=.15);ax.axhline(s(d,'full').J,c='k',ls='--',label='完整模型');ax.axhline(0,c='#999',ls=':');ax.set_xscale('log',base=2);ax.set_xticks([1,16,64,256,1024],[1,16,64,256,1024]);ax.set_xlabel('保留方向数量（维）');ax.set_ylabel(names[d]+'：对称线索区分量');ax.set_title('累计保留：预测恢复不等于粗细顺序')
 ax=axs[di,1]
 for b in bands:
  rr=D[(D.domain==d)&(D.condition==f'delete_B{b}')&(D.reference=='full')&(D.metric=='J')].iloc[0];v=-rr.difference;ax.errorbar(b,v,yerr=[[max(0,v+rr.high95)],[max(0,-rr.low95-v)]],fmt='o',c='#b06a45',capsize=3)
  matches=[s(d,f'random_delete_r{width[b-1]}_s{se}').J for se in [11021,11022,11023]];ax.plot(b,s(d,'full').J-np.mean(matches),'s',c='#999',ms=5)
 ax.axhline(0,c='#555',lw=.8);ax.set_xticks(bands,[f'段{b}\n{w}维' for b,w in zip(bands,width)]);ax.set_title('删除各段：圆=谱段；灰方=同秩随机均值');ax.set_ylabel('完整模型减删除后的区分量')
 ax=axs[di,2]
 for j in range(3,9):
  target=alias(f'append_B{j}');ext=alias(f'head_extension_B{j}');r=D[(D.domain==d)&(D.condition==target)&(D.reference=='keep_head16')&(D.metric=='J')].iloc[0];ax.errorbar(j,r.difference,yerr=[[max(0,r.difference-r.low95)],[max(0,r.high95-r.difference)]],fmt='o',c='#8a567d',capsize=3);ax.plot(j,s(d,ext).J-s(d,'keep_head16').J,'x',c='#2c759a');ax.plot(j,np.mean([s(d,alias(f'random_append_B{j}_s{se}')).J for se in [11021,11022,11023]])-s(d,'keep_head16').J,'s',c='#999',ms=5)
 ax.set_xticks(range(3,9),[f'加段{b}' for b in range(3,9)]);ax.axhline(0,c='#555',lw=.8);ax.set_title('固定头16：圆=追加；叉=同总维谱头；灰方=随机');ax.set_ylabel('相对只留头16的区分量变化')
 for ax in axs[di]:ax.grid(alpha=.15)
axs[0,0].legend(fontsize=8);fig.suptitle('谱条件完整交付：三域共用旧参考基；方向顺序与成员频率独立',fontsize=15);fig.text(.5,.005,'数据v1.3；12家族/域；自然对数单位；误差为家族配对95%区间。不同段宽度不等，不能直接按圆点大小排名；范数匹配详表另交付。',ha='center',fontsize=9);fig.tight_layout(rect=[0,.03,1,.96]);save(fig,'02_spectral_conditions_secondary','保留、删除和追加谱方向的效果是否超过同维参照？','analysis/summary.csv;all_paired_contrasts.csv;conditions.json')
# Primary question with matched controls.
fig,axs=plt.subplots(2,3,figsize=(15,8.6))
for di,d in enumerate(domains):
 ax=axs[0,di]
 for gi,g in enumerate(freqs):
  t=C[(C.group==g)&(C.domain==d)];target=t.iloc[0].target_J_loss;ax.plot(gi-.20,target,'o',c=col[g],ms=7,label='真实频率组删除' if gi==0 else None)
  for off,typ,color in [(0,'same_count','#777'),(.20,'norm_matched','#dab38d')]:
   r=t[t.control_type==typ].iloc[0];ax.plot(gi+off,r.control_mean_J_loss,'s',c=color,label=('同成员数随机组' if typ=='same_count' else '范数匹配扰动') if gi==0 else None)
  # CI here is EXCESS loss above norm-matched controls, displayed in bottom panel instead of mixing with target loss.
 ax.axhline(0,c='#555',lw=.8);ax.set_xticks(range(3),[freqcn[g] for g in freqs]);ax.set_title(names[d]+'：删除损失及匹配参照');ax.set_ylabel('完整模型减干预后的区分量（自然对数单位）')
 ax=axs[1,di]
 for gi,g in enumerate(freqs):
  for off,typ,color in [(-.1,'same_count','#777'),(.1,'norm_matched',col[g])]:
   r=C[(C.group==g)&(C.domain==d)&(C.control_type==typ)].iloc[0];v=r.excess_J_loss;ax.errorbar(gi+off,v,yerr=[[max(0,v-r.low95)],[max(0,r.high95-v)]],fmt='o',c=color,capsize=3)
 ax.axhline(0,c='#333',lw=1);ax.set_xticks(range(3),[freqcn[g] for g in freqs]);ax.set_title('超过随机参照的额外损失；正值：目标删除损失更大');ax.set_ylabel('真实组损失减匹配对照损失（自然对数单位）')
 for ax in axs[:,di]:ax.grid(alpha=.15)
axs[1,0].plot([],[],'o',color='#777',label='超过同成员数参照');axs[1,0].plot([],[],'o',color='#4089a6',label='超过范数参照（依频率组着色）');axs[1,0].legend(fontsize=7,loc='lower left');axs[0,0].legend(fontsize=8);fig.suptitle('主要终点：哪组删除效应超过同成员数和范数匹配参照？',fontsize=15);fig.text(.5,.005,'数据v1.3；每域12独立家族；下排误差为4000次配对家族95%区间。总体六项同时区间另表；范数匹配是尺度扰动，不是实际组删除。',ha='center',fontsize=9);fig.tight_layout(rect=[0,.035,1,.95]);save(fig,'03_frequency_deletion_matched_controls','频率组贡献是否超过匹配对照？','analysis/primary_feature_contrasts.csv;individual_random_contrasts.csv')
# Actual vector spectral position, no decoder-direction surrogate.
fig,ax=plt.subplots(figsize=(10,4.5));ev=G[G.split=='evaluation'];tbl=ev.groupby(['group','band','family_id']).fraction_of_group_vector.mean().groupby(['group','band']).mean().unstack();bottom=np.zeros(3);palette=plt.cm.viridis(np.linspace(.05,.95,8))
for j in range(1,9):
 vals=[tbl.loc[g,f'B{j}'] for g in freqs];ax.bar(range(3),vals,bottom=bottom,color=palette[j-1],label=f'谱段{j}');bottom+=vals
ax.set_xticks(range(3),[freqcn[g]+'实际贡献向量' for g in freqs]);ax.set_ylabel('组向量自身平方范数的谱段比例');ax.set_title('相同参考基中的频率组实际贡献；不把三组能量相加\n仅在组向量非零位置计算比例，先按家族平均');ax.legend(ncol=4,fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.1));fig.tight_layout();save(fig,'A01_actual_group_spectral_positions','各组实际响应向量处于哪些谱位置？','analysis/group_spectral_contributions.csv.gz;group_spectral_cross_terms.csv.gz')
# Fixed six families; no attractive-case selection.
T=pd.read_csv(E/'analysis/paraphrase_metrics.csv');fixed=json.load(open(E/'config.json'))['fixed_families'];fam={r['family_id']:r for r in [json.loads(l) for l in (E/'data/families.jsonl').read_text().splitlines()]};fig,axs=plt.subplots(6,2,figsize=(13,18));cc=[('full','完整模型','#222')]+[(f'feature_delete_{g}','删除'+freqcn[g],col[g]) for g in freqs]
for i,fid in enumerate(fixed):
 f=fam[fid]
 for c,label,color in cc:
  q=T[(T.condition==c)&(T.family_id==fid)];axs[i,0].plot([0,1],q[['rA','rB']].mean().to_numpy(),'o-',c=color,label=label);axs[i,1].plot([0,1],q[['upper_A','upper_B']].mean().to_numpy(),'o-',c=color,label=label)
  for pj,(_,individual) in enumerate(q.iterrows()):
   xs=np.array([0,1])+(-.035 if pj==0 else .035);axs[i,0].scatter(xs,[individual.rA,individual.rB],s=17,marker='.',color=color,alpha=.5);axs[i,1].scatter(xs,[individual.upper_A,individual.upper_B],s=17,marker='.',color=color,alpha=.5)
 ff=T[(T.family_id==fid)&(T.condition=='full')];hh=T[(T.family_id==fid)&(T.condition=='feature_delete_high')];axs[i,0].set_title(names[f['domain']]+f'：{f["A"]} / {f["B"]}\n两侧具体都对：完整{int(ff.both_correct.sum())}/2；删高频{int(hh.both_correct.sum())}/2',fontsize=10);axs[i,1].set_title(f'上位：{f["U"]} / 错误上位：{f["V"]}\n两侧上位都对：完整{int(ff.upper_both_cues.sum())}/2；删高频{int(hh.upper_both_cues.sum())}/2',fontsize=10)
 for ax in axs[i]:ax.set_xticks([0,1],['指向第一个概念的线索','指向第二个概念的线索']);ax.axhline(0,c='#777',lw=.8);ax.grid(alpha=.15)
 axs[i,0].set_ylabel('第一个概念减第二个概念的对数概率');axs[i,1].set_ylabel('正确上位减错误上位的对数概率')
axs[0,0].legend(fontsize=8);fig.suptitle('结果前固定的六个家族：具体线索与上位判断逐例对照',fontsize=15);fig.text(.5,.005,'大点为两措辞平均，小点为各措辞；正确计数按各措辞判定，不能用均值符号替代。左图期望左正右负，右图均正。完整前文、逐片段及候选分数见真实文本材料；无跨任务量尺比较。',ha='center',fontsize=9);fig.tight_layout(rect=[0,.02,1,.97]);save(fig,'04_fixed_concept_cases','固定自然语言线索下具体概念和上位判断分别怎么变？','analysis/paraphrase_metrics.csv;data/prefixes.jsonl')
(E/'figure_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print('Rendered',len(manifest),'figures')
