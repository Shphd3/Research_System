import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,shutil
import numpy as np,pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager,FontProperties
from matplotlib.colors import LogNorm
E=Path(__file__).resolve().parents[1];c=json.load(open(E/'manifest.json'));P=Path(c['project_dir']);S=pd.read_csv(E/'analysis/summary_metrics.csv');F=S[(S.panel=='natural')&(S.group=='ALL')]
font='/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030/presentation_variants/near_single_domain_20261030/fonts/NotoSansCJKsc-Regular.otf';fontManager.addfont(font);plt.rcParams.update({'font.family':FontProperties(fname=font).get_name(),'axes.unicode_minus':False,'font.size':10,'savefig.dpi':155})
scopes=['target_only','all_prefix'];sn={'target_only':'只改当前位置','all_prefix':'改整个前缀'};bands=[f'{64*i+1}—{64*i+64}' for i in range(16)]
def save(fig,name):
 for ext in ['png','pdf']:
  fig.savefig(E/'figures'/f'{name}.{ext}',bbox_inches='tight');shutil.copy2(E/'figures'/f'{name}.{ext}',P/'figures'/f'{name}.{ext}')
 plt.close(fig)
def matrix(scope,mode,metric):
 a=F[(F.scope==scope)&F.condition.str.startswith(mode+'_b')].copy();a['band']=a.condition.str[-2:].astype(int);return a.pivot(index='band',columns='layer',values=metric).reindex(index=range(16),columns=range(1,29)).to_numpy()
def axes_ticks(ax):
 ax.set_xticks([0,3,7,11,15,19,23,27],[1,4,8,12,16,20,24,28]);ax.set_yticks(range(16),bands);ax.set_xlabel('单独干预层（1—28）');ax.set_ylabel('保留的主成分编号：每段64维')
fig,axs=plt.subplots(2,3,figsize=(18,11),layout='constrained')
for row,scope in enumerate(scopes):
 a=matrix(scope,'add','top1_agreement')*100;b=matrix(scope,'no','top1_agreement')*100
 for col,(v,title) in enumerate([(a,'加回均值'),(b,'不加均值'),(a-b,'加均值 − 不加均值')]):
  ax=axs[row,col];im=ax.imshow(v,aspect='auto',cmap='viridis' if col<2 else 'RdBu_r',vmin=0 if col<2 else -100,vmax=100);axes_ticks(ax);ax.set_title(sn[scope]+'｜'+title);fig.colorbar(im,ax=ax,label='原首选保持率（%）' if col<2 else '配对差（百分点）',shrink=.75)
fig.suptitle('等维谱段：同一层只保留64个方向，最终首选能否保持？\n175篇／700位置；文档等权。前两列共用0—100%色标；差值共用±100个百分点。',fontsize=15);save(fig,'01_equal64_mean_heatmaps')
fig,axs=plt.subplots(2,2,figsize=(14,9),sharex=True,sharey=True,layout='constrained');colors=['#126e94','#e68a22','#459f66','#bd5295','#786bc1'];chosen=[0,1,3,7,15]
for row,scope in enumerate(scopes):
 for col,mode in enumerate(['add','no']):
  ax=axs[row,col]
  for b,colr in zip(chosen,colors):
   d=F[(F.scope==scope)&(F.condition==f'{mode}_b{b:02d}')].sort_values('layer');ax.plot(d.layer,d.top1_agreement*100,c=colr,label=bands[b]);ax.fill_between(d.layer,d.top1_agreement_ci_low*100,d.top1_agreement_ci_high*100,color=colr,alpha=.10)
  mean=F[(F.scope==scope)&(F.condition=='mean_only')].sort_values('layer');ax.plot(mean.layer,mean.top1_agreement*100,c='gray',ls='--',label='仅均值（旧参照）');ax.set_title(sn[scope]+'｜'+('加回均值' if mode=='add' else '不加均值'));ax.set_ylim(-2,101);ax.set_xticks([1,4,8,12,16,20,24,28]);ax.set_xlabel('干预层');ax.set_ylabel('原首选保持率（%）');ax.grid(alpha=.15)
axs[0,0].legend(ncol=3,fontsize=9);fig.suptitle('预先固定5个代表谱段的逐层曲线\n阴影：文档重采样95%逐点区间；完整16段见热图与原始表。',fontsize=14);save(fig,'02_selected_band_curves')
fig,axs=plt.subplots(1,3,figsize=(18,6.5),layout='constrained');en=matrix('target_only','add','target_band_energy')*100
im=axs[0].imshow(en,aspect='auto',norm=LogNorm(vmin=max(en.min(),1e-5),vmax=en.max()),cmap='magma');axes_ticks(axs[0]);axs[0].set_title('保留的中心化能量（对数色标）');fig.colorbar(im,ax=axs[0],label='中心化平方范数保留（%）',shrink=.7)
for col,mode in enumerate(['add','no'],1):
 v=matrix('target_only',mode,'target_norm_ratio');im=axs[col].imshow(v,aspect='auto',vmin=0,vmax=max(1.,v.max()),cmap='cividis');axes_ticks(axs[col]);axs[col].set_title(('加均值' if mode=='add' else '不加均值')+'：实际表征范数／原范数');fig.colorbar(im,ax=axs[col],label='范数比（倍）',shrink=.7)
fig.suptitle('等维数仍不等能量；均值恢复还会改变向量的范数和方向\n能量仅指中心化的谱段投影，同一谱段两种均值条件的该能量相同。',fontsize=14);save(fig,'03_energy_norm')
fig,axs=plt.subplots(2,2,figsize=(14,9),layout='constrained')
for row,scope in enumerate(scopes):
 for col,(metric,label) in enumerate([('top1_agreement','原首选保持率（%）'),('NLL','真实后继负对数概率（nat；低为好）')]):
  ax=axs[row,col];scale=100 if metric=='top1_agreement' else 1
  for name,title,color in [('add_b00','头64＋均值','#126e94'),('no_b00','头64，不加均值','#e68a22'),('full_centered','全1024维减均值','#459f66'),('mean_only','仅均值（旧）','#777777'),('zero','零向量','#bd5295')]:
   d=F[(F.scope==scope)&(F.condition==name)].sort_values('layer');ax.plot(d.layer,d[metric]*scale,c=color,label=title)
  base=F[F.condition=='identity'][metric].iloc[0];ax.axhline(base*scale,c='black',ls=':',label='完整模型');ax.set_title(sn[scope]+'｜'+label);ax.set_xlabel('干预层');ax.set_xticks([1,4,8,12,16,20,24,28]);ax.set_ylabel(label);ax.grid(alpha=.15)
axs[0,0].legend(fontsize=8,ncol=2);fig.suptitle('均值控制：全维减均值并不是完整恒等重建',fontsize=15);save(fig,'04_mean_controls')
# Fixed examples, no selection by observed success.
cases=[json.loads(s) for s in (E/'analysis/fixed_case_outputs.jsonl').read_text().splitlines()];RR=[json.loads(s) for s in (E/'data/positions.jsonl').read_text().splitlines()]
for idx in [58,211,676]:
 z=[r for r in cases if r['index']==idx and r['scope']=='target_only'];fig,axs=plt.subplots(1,2,figsize=(16,16),layout='constrained')
 for ax,mode in zip(axs,['add','no']):
  ax.set_xlim(-.5,3.5);ax.set_ylim(15.5,-.5);ax.set_xticks(range(4),['第1层','第14层','第25层','第28层']);ax.xaxis.tick_top();ax.set_yticks(range(16),bands);ax.set_title('加回均值' if mode=='add' else '不加均值',pad=24)
  for b in range(16):
   for col,l in enumerate([1,14,25,28]):
    r=next(a for a in z if a['layer']==l and a['condition']==f'{mode}_b{b:02d}');t=r['top10'][0];frag=repr(t['fragment']).replace(chr(65533),chr(92)+'ufffd');frag=frag if len(frag)<18 else frag[:15]+'…';ax.text(col,b,f"{frag}\nID {r['top1_id']} · {100*t['probability']:.1f}%",ha='center',va='center',fontsize=8.5,color='#126e94' if r['top1_agreement'] else '#6b463a')
  for y in np.arange(-.5,16,1):ax.axhline(y,c='#dddddd',lw=.5)
 r=RR[idx];base=next(a for a in cases if a['index']==idx and a['condition']=='identity');bt=base['top10'][0];ending=r['visible_prefix'][-110:].replace('\n',' ')
 title=f"固定案例 {idx}｜输入末段：…{ending}\n当前位置：第{r['position']+1}个／0基{r['position']}，ID{r['input_id']} {repr(r['input_fragment'])}；真实后继：ID{r['target_id']} {repr(r['target_fragment'])}\n完整模型首选：ID{bt['id']} {repr(bt['fragment'])} {100*bt['probability']:.2f}%；只改当前位置，再经过剩余网络\n每格：首选片段、ID和概率。蓝字保持原首选；转义ufffd表示单token解码替代字符，完整前文与前10候选见案例表。"
 fig.suptitle(title,fontsize=12);save(fig,f'05_case_{idx:03d}')
print('FIGURES_DONE',flush=True)
