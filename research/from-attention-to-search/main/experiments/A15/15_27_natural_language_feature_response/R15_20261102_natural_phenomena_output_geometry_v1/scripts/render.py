import os
os.environ['MPLBACKEND']='Agg'
from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager,FontProperties
E=Path(__file__).resolve().parents[1];font='/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030/presentation_variants/near_single_domain_20261030/fonts/NotoSansCJKsc-Regular.otf';fontManager.addfont(font);plt.rcParams.update({'font.family':FontProperties(fname=font).get_name(),'axes.unicode_minus':False,'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':160});names=json.load(open(E/'data/phenomenon_definitions_v1p2.json'))['name'];cfg=json.load(open(E/'config.json'));P=dict(np.load(E/'analysis/pca.npz'));G=dict(np.load(E/'analysis/head_geometry.npz'));manifest=[];MAP=plt.get_cmap('RdBu_r').copy();MAP.set_bad('#e5e5e5')
def save(fig,n,q,src):
 fig.text(.5,-.015,'Qwen3-0.6B-Base｜R15｜300篇发现拟合；150篇独立分析验证｜48个固定候选feature，不代表全字典',ha='center',fontsize=8);fig.text(.5,-.035,'原表：'+src,ha='center',fontsize=7);fig.savefig(E/'figures'/f'{n}.png',bbox_inches='tight');fig.savefig(E/'figures'/f'{n}.pdf',bbox_inches='tight');plt.close(fig);manifest.append({'figure':n,'question':q,'sources':src,'model':'frozen officialQwen3-0.6B-Base;A22joint14layers','unit':'document;nottoken','label_version':'1.2','source_claim':'DCLMwebpagecohorts;mayA22trainingexposed','data':str(E/'data/documents.jsonl')})
A=pd.read_csv(E/'analysis/validation_band_map.csv');flags=list(names);bands=cfg['bands'];lab=[f'[{a},{b})\n{b-a}维' for a,b in bands];matrix=np.full((len(flags),8),np.nan);stars=np.full((len(flags),8),'',object);rowlabels=[]
for i,f in enumerate(flags):
 q=A[A.phenomenon==f]
 if len(q):
  r=q.iloc[0];rowlabels.append(names[f]+f'\n{int(r.documents)}篇/{int(r.hosts)}来源/{int(r.pairs)}对')
 else:rowlabels.append(names[f]+'\n无法同token匹配')
 for _,r in q.iterrows():
  b=int(r.response.split('_')[1]);matrix[i,b]=r.effect*100 if r.documents>=12 else np.nan;stars[i,b]='★' if bool(r.reproduced_band_association) else '·' if r.low95*r.high95>0 else ''
fig,ax=plt.subplots(figsize=(12,11));lim=max(0.1,np.nanmax(abs(matrix)));im=ax.imshow(np.ma.masked_invalid(matrix),cmap=MAP,vmin=-lim,vmax=lim,aspect='auto');ax.set_yticks(range(len(flags)),rowlabels,fontsize=9);ax.set_xticks(range(8),lab);ax.set_xlabel('归一化前 h 的固定新参考谱段（零基左闭右开区间）');ax.set_title('语言现象 × 表征谱段：同文档、同当前token的能量比例差\n正值=现象位置占比更高；不是该段“编码该现象”的证明')
for i in range(len(flags)):
 for b in range(8):
  if np.isfinite(matrix[i,b]):ax.text(b,i,f'{matrix[i,b]:+.2f}{stars[i,b]}',ha='center',va='center',fontsize=8)
fig.colorbar(im,ax=ax,label='现象位置减匹配参照：中心化总能量占比差（百分点）');fig.text(.5,.01,'·：逐项文档配对95%区间不含零；★：全部现象×谱段文档同时区间不含零且三拆分同向。灰格=无法匹配或少于12篇，不表示无作用。',ha='center',fontsize=8);fig.tight_layout(rect=[0,.04,1,.98]);save(fig,'01_phenomena_band_map','哪些可见文本属性关联特定谱段，匹配后是否仍可复现？','validation_band_map.csv;validation_document_effects.csv;validation_matched_positions.csv')
# Geometry coordinates explicitly separated.
T=pd.read_csv(E/'analysis/representation_head_spectra.csv');R=json.load(open(E/'analysis/head_gain_reference.json'));O=pd.read_csv(E/'analysis/representation_head_subspace_overlap.csv');fig,axs=plt.subplots(2,2,figsize=(13,9));x=np.arange(1,1025)
for key,label in [('h_eigenvalue','归一化前h'),('y_eigenvalue','归一化后y')]:axs[0,0].loglog(x,T[key]/T[key].sum(),label=label)
axs[0,0].set_title('两套坐标分别拟合，编号不混用');axs[0,0].set_xlabel('主成分序号（从1显示）');axs[0,0].set_ylabel('该方向方差占总方差');axs[0,0].legend()
axs[0,1].loglog(x,T.head_raw_singular_value,label='原始输出矩阵');axs[0,1].loglog(x,T.head_centered_singular_value,'--',label='去词表均值输出矩阵');axs[0,1].set_title('仅输出头参数谱；共同logit平移被去除');axs[0,1].set_xlabel('输出头奇异值序号');axs[0,1].set_ylabel('奇异值');axs[0,1].legend()
scatter=axs[1,0].scatter(T.postnorm_variance,T.relative_to_isotropic_gain,c=np.arange(1024),cmap='viridis',s=8);axs[1,0].set_xscale('log');axs[1,0].axhline(1,c='#777',ls='--');axs[1,0].set_xlabel('归一化后y主成分方差');axs[1,0].set_ylabel('单位y变化的输出增益／各向同性参照');axs[1,0].set_title('大方差不自动等于高输出增益');fig.colorbar(scatter,ax=axs[1,0],label='y主成分零基序号')
for k in [16,64,256]:
 q=O[O.head_right_top_dimensions==k].drop_duplicates('representation_band');axs[1,1].plot(q.representation_band,q.overlap_per_representation_dimension,'o-',label=f'输出头前{k}右奇异方向');axs[1,1].axhline(k/1024,c='#888',alpha=.3)
axs[1,1].set_xticks(range(8),[f'段{i+1}' for i in range(8)]);axs[1,1].set_ylabel('y子空间每维重合度（0–1）');axs[1,1].set_title('只在归一化后y空间与输出头比较');axs[1,1].legend(fontsize=8);fig.tight_layout();save(fig,'02_representation_output_geometry','表征方差方向与有效输出敏感方向如何对应？','representation_head_spectra.csv;representation_head_subspace_overlap.csv;head_gain_reference.json')
# Real text paired changes; each point a document,not a token.
C=pd.read_csv(E/'analysis/validation_actual_changes.csv');fig,axs=plt.subplots(1,2,figsize=(13,5));codes=sorted(C.phenomenon.unique());colors=plt.cm.tab20(np.linspace(0,1,len(codes)));kept=[]
for i,f in enumerate(codes):
 q=C[(C.phenomenon==f)&(C.band==0)];
 if not len(q):continue
 axs[0].scatter(q.norm_delta_y,q.centered_logit_RMS,color=colors[i],s=10,alpha=.35);v=q.output_gain.to_numpy()/R['isotropic_centered_logit_RMS_per_unit_delta_y'];boot=v[np.random.default_rng(110204).integers(0,len(v),(2000,len(v)))].mean(1);lo,hi=np.quantile(boot,[.025,.975]);m=v.mean();axs[1].errorbar(i,m,yerr=[[max(0,m-lo)],[max(0,hi-m)]],fmt='o',color=colors[i],capsize=3);kept.append((i,f,len(v)));axs[1].annotate(str(len(v))+'篇',(i,m),xytext=(0,8),textcoords='offset points',ha='center',fontsize=7)
axs[0].set_xlabel('真实配对变化的 ||Δy||');axs[0].set_ylabel('||去词表均值输出矩阵×Δy|| / √词表大小');axs[0].set_title('同token不同可见前文：输入幅度与输出幅度分开');axs[1].axhline(1,c='#777',ls='--');axs[1].set_xticks([i for i,f,n in kept],[names[f] for i,f,n in kept],rotation=60,ha='right');axs[1].set_ylabel('实际方向增益／各向同性方向参照');axs[1].set_title('误差按文档重采样；关联不等于单一线索因果效应');fig.tight_layout();save(fig,'03_actual_text_change_output_gain','真实语言现象配对的变化，是幅度大还是方向更容易被读出？','validation_actual_changes.csv;validation_matched_positions.csv;head_gain_reference.json')
F=json.load(open(E/'validation_selection_frozen.json'));Vd=pd.read_csv(E/'analysis/validation_selected_verdicts.csv');fig,ax=plt.subplots(figsize=(10,5));valid=Vd[Vd.columns.intersection(['effect'])].shape[1]>0
if valid:
 for i,(_,r) in enumerate(Vd.iterrows()):
  if pd.isna(r.get('effect')):continue
  ax.errorbar(i,r.effect,yerr=[[max(0,r.effect-r.low95)],[max(0,r.high95-r.effect)]],fmt='o',capsize=4);ax.annotate(f'{int(r.documents)}篇/{int(r.hosts)}来源\nHolm p={r.holm_p:.3f}',(i,r.effect),xytext=(0,10),textcoords='offset points',ha='center',fontsize=8)
 ax.set_xticks(range(len(Vd)),[names[r.phenomenon]+'\n'+r.feature for _,r in Vd.iterrows()]);ax.axhline(0,c='#777');ax.set_ylabel('匹配后系数差／发现集系数标准差');ax.set_title('开发阶段固定的解释，在新文本上预测响应了吗？')
else:ax.text(.5,.5,'没有满足开发支持规则的解释\n保留失败与不足，不补自编题',ha='center',va='center');ax.set_axis_off()
fig.tight_layout();save(fig,'04_frozen_explanations_validation','发现的feature关联能否预测独立文本响应？','validation_selected_verdicts.csv;validation_selection_frozen.json;validation_source_robustness.csv')

# Word-form properties are a separate descriptive comparison,never a substitute for same-token context tests.
D=pd.read_csv(E/'analysis/descriptive_token_category_summary.csv');fig,axs=plt.subplots(1,3,figsize=(15,4.6));cn={'number':'数字片段','punctuation':'标点片段','format':'纯空白片段'}
for ax,(cat,q) in zip(axs,D.groupby('category')):
 q=q.sort_values('band');v=q.difference.to_numpy()*100;ax.errorbar(np.arange(8),v,yerr=np.array([v-q.low95.to_numpy()*100,q.high95.to_numpy()*100-v]),fmt='o-',capsize=3);ax.axhline(0,c='#777');ax.set_xticks(range(8),['段'+str(i+1) for i in range(8)]);ax.set_title(cn[cat]+f'：{int(q.iloc[0].documents)}篇/{int(q.iloc[0].pairs)}对');ax.set_ylabel('中心化能量比例差（百分点）');ax.set_xlabel('同文档、同位置四分位；当前token身份不同')
fig.suptitle('词面类别的描述性谱分布：不能据此命名上下文语义功能');fig.tight_layout();save(fig,'A01_word_form_descriptive','发现视图的数字／标点／空白响应有多大词面成分？','descriptive_token_category_summary.csv;descriptive_token_category_document_effects.csv')
S=pd.read_csv(E/'analysis/signed_direction_validation.csv');flags=[f for f in names if f in S.phenomenon.unique()];pcs=cfg['PC_candidates'];fig,axs=plt.subplots(1,2,figsize=(16,11),sharey=True)
for ax,metric,title in zip(axs,['signed_trainSD','signed_cosine'],['有符号投影／发现集标准差','有符号投影／当前中心化向量长度']):
 mat=np.full((len(flags),len(pcs)),np.nan);stars=np.zeros_like(mat,dtype=bool);labels=[]
 for i,f in enumerate(flags):
  q=S[(S.phenomenon==f)&(S.metric==metric)];r=q.iloc[0];labels.append(names[f]+f'（{int(r.documents)}篇）')
  for _,r in q.iterrows():
   j=pcs.index(int(r.PC_index0))
   if r.documents>=12:mat[i,j]=r.effect;stars[i,j]=bool(r.exploratory_consistent_association)
 lim=np.nanmax(abs(mat));im=ax.imshow(np.ma.masked_invalid(mat),cmap=MAP,vmin=-lim,vmax=lim,aspect='auto');ax.set_xticks(range(len(pcs)),pcs,rotation=60);ax.set_xlabel('归一化前h固定主方向的零基序号');ax.set_yticks(range(len(flags)),labels,fontsize=9);ax.set_title(title);fig.colorbar(im,ax=ax,shrink=.7)
 for i,j in zip(*np.where(stars)):ax.text(j,i,'★',ha='center',va='center',color='black',fontsize=12)
fig.suptitle('A6探索性补齐：方向有符号关联与谱段能量归属不同\n指标在查看主能量表后补齐，不能追认为新确认终点',fontsize=14);fig.text(.5,.005,'星：全512方向×属性×尺度比较同时控制且三拆分同向；灰：少于12匹配文档。符号随基底约定，不是固有语义。',ha='center',fontsize=8);fig.tight_layout(rect=[0,.03,1,.93]);save(fig,'05_signed_direction_exploratory','能量表未建立集中，是否仍有正负方向的文本关联？','signed_direction_validation.csv;signed_direction_sensitivity.csv;amendmentsA6')

(E/'figure_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print('RENDERED',len(manifest),flush=True)
