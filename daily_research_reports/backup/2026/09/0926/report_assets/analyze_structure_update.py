"""Fit-only common axes, complete spectra, paired transfer summaries and figures."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','4')
from pathlib import Path
import json, hashlib, shutil, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import TwoSlopeNorm

ROOT=Path('/data/250010109/MoE_Router/experiments/20260926_structure_update_bridge')
PRIOR=Path('/data/250010109/MoE_Router/experiments/20260925_sae_domain_activation')
DEST=Path('/data/250010109/Research_System/daily_research_reports/0926/figures')
OUT=ROOT/'figures'
font_manager.fontManager.addfont('/data/250010109/Research_System/daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf')
plt.rcParams.update({'font.family':'Noto Sans CJK SC','font.size':11,'axes.unicode_minus':False,
                     'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
DOMAINS=['computer_science','mathematics','physics','biology']
LABELS=['计算机','数学','物理','生物']
COLORS=['#3075b7','#df7f28','#37966f','#a761ad']
rows=[json.loads(l) for l in (PRIOR/'selected.jsonl').open()]
fit=np.array([r['split']=='fit' for r in rows]); test=~fit
labels=np.array([DOMAINS.index(r['domain']) for r in rows])
z=np.load(ROOT/'representations.npz')
assert json.loads((ROOT/'complete.json').read_text())['status']=='COMPLETE'
assert z['sample_ids'].tolist()==[r['sample_id'] for r in rows]
OUT.mkdir(exist_ok=True); DEST.mkdir(parents=True,exist_ok=True)

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(fig,name):
    for ext in ['png','pdf']:
        p=OUT/f'{name}.{ext}';fig.savefig(p,dpi=180,bbox_inches='tight');shutil.copy2(p,DEST/p.name)
    plt.close(fig)

def pca(x):
    x=x.astype(np.float64); mu=x[fit].mean(0)
    _,s,v=np.linalg.svd(x[fit]-mu,full_matrices=False)
    var=s*s; var/=var.sum()
    raw=np.linalg.svd(x[fit],full_matrices=False,compute_uv=False)**2;raw/=raw.sum()
    proj=(x-mu)@v[:2].T
    energy=((x[test]-mu)**2).sum()
    return dict(mu=mu,v=v,s=s,var=var,raw=raw,proj=proj,
        r90=int(np.searchsorted(np.cumsum(var),.9)+1),
        r90_raw=int(np.searchsorted(np.cumsum(raw),.9)+1),
        effective_rank=float(1/np.sum(var**2)),
        fit_top2=float(var[:2].sum()), test_top2=float((proj[test]**2).sum()/energy),
        fit_mean_energy_fraction=float(np.sum(mu**2)/np.mean(np.sum(x[fit]**2,axis=1))))

structure={}; axis_cache={}
for obj,title in [('a','注意力原始输出：稀疏自编码器观察的位置'),('u','下投影实际输入：更新矩阵直接作用的位置')]:
    x=z[obj+'_mean'].astype(np.float64); result=pca(x); last=pca(z[obj+'_last'])
    normed=x/np.maximum(np.linalg.norm(x,axis=1,keepdims=True),1e-30); unit=pca(normed)
    for pool,res in [('mean',result),('last',last),('unit_mean',unit)]:
        structure[obj+'_'+pool]={k:v for k,v in res.items() if k not in ['mu','v','s','var','raw','proj']}
        axis_cache[obj+'_'+pool+'_mu']=res['mu'];axis_cache[obj+'_'+pool+'_basis']=res['v']
        axis_cache[obj+'_'+pool+'_variance']=res['var'];axis_cache[obj+'_'+pool+'_raw_energy']=res['raw']
        axis_cache[obj+'_'+pool+'_projection']=res['proj']
    structure[obj+'_mean']['test_norm_median_by_domain']={d:float(np.median(np.linalg.norm(x[test & (labels==i)],axis=1))) for i,d in enumerate(DOMAINS)}
    fig,axes=plt.subplots(2,3,figsize=(15.7,9.3),layout='constrained')
    for i,(lab,color) in enumerate(zip(LABELS,COLORS)):
        ix=test & (labels==i); p=result['proj'][ix]
        axes[0,0].scatter(p[:,0],p[:,1],s=16,alpha=.57,c=color,label=lab,edgecolors='none')
        for j in (0,1):
            val=np.sort(p[:,j]);axes[0,j+1].step(val,np.arange(1,len(val)+1)/len(val),where='post',color=color,lw=1.8,label=lab)
        un=unit['proj'][ix];axes[1,2].scatter(un[:,0],un[:,1],s=16,alpha=.57,c=color,edgecolors='none')
    axes[0,0].set(title=f'第二批的实际记录（每点一段文本）\n前两轴覆盖第二批中心化能量 {result["test_top2"]:.1%}',xlabel='共同第一主轴坐标',ylabel='共同第二主轴坐标')
    axes[0,0].legend(ncol=2,fontsize=10,frameon=False)
    for j in (0,1):
        axes[0,j+1].set(title=f'共同第{j+1}主轴上的完整记录分布',xlabel='有正负的投影坐标',ylabel='不超过该坐标的记录比例',ylim=(0,1.02))
    ax=axes[1,0];rank=np.arange(1,len(result['var'])+1)
    ax.plot(rank,np.cumsum(result['var']),label='去均值：方差累计占比',lw=2,color='#334f75')
    ax.plot(rank,np.cumsum(result['raw']),label='未去均值：原始能量累计占比',lw=2,color='#bd7534')
    ax.axhline(.9,color='#777',ls=':',lw=1);ax.axvline(result['r90'],color='#334f75',ls=':',lw=1)
    ax.set(xscale='log',ylim=(0,1.02),xlabel='方向数（对数坐标；全部样本可见谱）',ylabel='累计占比',
        title=f'第一批拟合的两种谱，不能混称\n90%：方差 {result["r90"]} 维；原始能量 {result["r90_raw"]} 维')
    ax.legend(fontsize=9,frameon=False,loc='lower right')
    vals=[np.linalg.norm(x[test & (labels==i)],axis=1) for i in range(4)]
    boxes=axes[1,1].boxplot(vals,labels=LABELS,patch_artist=True,showfliers=True)
    for b,c in zip(boxes['boxes'],COLORS):b.set_facecolor(c);b.set_alpha(.5)
    axes[1,1].set(title='正文均值向量的长度：保留尺度信息',ylabel='向量二范数（不是逐词元范数平均）')
    axes[1,2].set(title=f'敏感性：先将每段向量归一为单位长度\n另以第一批拟合共同轴；第二批覆盖 {unit["test_top2"]:.1%}',xlabel='归一化后第一共同主轴',ylabel='归一化后第二共同主轴')
    fig.suptitle(title,fontsize=18,fontweight='bold')
    fig.supxlabel('同一 21B 词元检查点、末块、正文 256 位置均值；第一批 512 条拟合，第二批 512 条展示。\n四领域共用坐标；不按类别各自降维；不依据第二批选择方向。几何差异不是更新冲突或隔离收益。',fontsize=10)
    save(fig,f'{obj}_common_axes_and_spectrum')
np.savez_compressed(ROOT/'common_axes.npz',**axis_cache)
(ROOT/'structure_results.json').write_text(json.dumps(structure,indent=2,ensure_ascii=False)+'\n')

loss=np.load(ROOT/'update_losses.npz');branches=json.loads((ROOT/'branches.json').read_text())
rr=[rows[i] for i in loss['test_indices']];help_values=loss['baseline'][None,:]-loss['after']
rng=np.random.default_rng(20260926);summary=[];means=np.zeros((2,4,4));intervals=np.zeros((2,4,4,2))
for t,d in enumerate(DOMAINS):
    ids=np.array([i for i,r in enumerate(rr) if r['domain']==d])
    cats=sorted({rr[i]['category'] for i in ids});sample=[]
    for cat in cats:
        ix=np.array([i for i in ids if rr[i]['category']==cat]);assert len(ix)==64
        sample.append(rng.choice(ix,size=(2000,len(ix)),replace=True))
    draw=np.concatenate(sample,axis=1)
    boot=help_values[:,draw].mean(2)
    for b,branch in enumerate(branches):
        k=0 if branch['rho']==1e-4 else 1;s=DOMAINS.index(branch['source'])
        mean=float(help_values[b,ids].mean());ci=np.quantile(boot[b],[.025,.975])
        means[k,s,t]=mean;intervals[k,s,t]=ci
        summary.append(dict(source=branch['source'],target=d,rho=branch['rho'],help=mean,lo=float(ci[0]),hi=float(ci[1]),baseline=float(loss['baseline'][ids].mean())))
with (ROOT/'update_summary.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=list(summary[0]));writer.writeheader();writer.writerows(summary)

profiles=np.load(PRIOR/'analysis/domain_profiles.npz');assert profiles['domains'].tolist()==DOMAINS
p=profiles['fit_frequency'];p=p/p.sum(1,keepdims=True)
tv=.5*np.abs(p[:,None]-p[None,:]).sum(2)
cos=np.load(ROOT/'gradient_geometry.npz')['cosine'];pairs=[]
for i in range(4):
    for j in range(i+1,4):pairs.append(dict(source=DOMAINS[i],target=DOMAINS[j],activation_distance=float(tv[i,j]),gradient_cosine=float(cos[i,j]),
            mean_bidirectional_help=float((means[0,i,j]+means[0,j,i])/2),half_mean_bidirectional_help=float((means[1,i,j]+means[1,j,i])/2)))
checks=dict(status='COMPLETE',all_self_point_positive=bool(np.diagonal(means,axis1=1,axis2=2).min()>0),
        all_self_marginal_lower_positive=bool(min(intervals[k,i,i,0] for k in range(2) for i in range(4))>0),
        cross_positive_points=[int(sum(means[k,i,j]>0 for i in range(4) for j in range(4) if i!=j)) for k in range(2)],
        cross_positive_marginal_lower=[int(sum(intervals[k,i,j,0]>0 for i in range(4) for j in range(4) if i!=j)) for k in range(2)],
        max_half_full_ratio_deviation=float(np.max(np.abs(means[1]/means[0]-.5))),
        pairs=pairs,boundary='All cells shown; marginal descriptive intervals conditional on fixed source gradients; not adjusted for 32 comparisons or paper clustering.')
(ROOT/'update_results.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
fig,axes=plt.subplots(2,2,figsize=(14,12.4),layout='constrained')
vmax=float(np.max(np.abs(means)))*1000
for k in range(2):
    ax=axes[0,k];im=ax.imshow(means[k]*1000,cmap='RdBu',vmin=-vmax,vmax=vmax)
    ax.set_xticks(range(4),LABELS);ax.set_yticks(range(4),LABELS)
    ax.set(xlabel='在哪组第二批文本上测后果',ylabel='只用哪组第一批文本计算更新',title=['一步更新：相对权重长度 0.0001','半步检查：相对权重长度 0.00005'][k])
    for i in range(4):
        for j in range(4):
            m=means[k,i,j]*1000;lo,hi=intervals[k,i,j]*1000
            ax.text(j,i,f'{m:+.3f}\n[{lo:+.3f}, {hi:+.3f}]',ha='center',va='center',fontsize=9,color='white' if abs(m)>.63*vmax else '#202020')
    fig.colorbar(im,ax=ax,shrink=.72,label='损失下降 × 1000；正值帮助，负值伤害')
axes[1,0].imshow(cos,cmap='RdBu',vmin=-1,vmax=1)
axes[1,0].set_xticks(range(4),LABELS);axes[1,0].set_yticks(range(4),LABELS)
axes[1,0].set_title('第一批完整矩阵梯度的方向相似度')
for i in range(4):
    for j in range(4):axes[1,0].text(j,i,f'{cos[i,j]:.3f}',ha='center',va='center',color='white' if abs(cos[i,j])>.6 else '#222')
ax=axes[1,1]
for pair in pairs:
    i=DOMAINS.index(pair['source']);j=DOMAINS.index(pair['target'])
    ax.scatter(pair['activation_distance'],pair['mean_bidirectional_help']*1000,s=60,color='#405e80')
    ax.annotate(LABELS[i]+'—'+LABELS[j],(pair['activation_distance'],pair['mean_bidirectional_help']*1000),xytext=(4,5),textcoords='offset points',fontsize=9)
ax.axhline(0,color='#888',ls=':');ax.set(xlabel='第一批全字典激活频率总变差距离',ylabel='双向平均帮助 × 1000',title='同一四组的六个组对：完整列出，不拟合规律')
fig.suptitle('表征有差异之后：一步更新到底帮助还是伤害？',fontsize=18,fontweight='bold')
fig.supxlabel('固定基座末层下投影的全矩阵虚拟梯度步；每组 128 条更新、另 128 条读出；每条固定 16 个预测位置。\n每格为均值及 95% 记录分层配对区间；条件于固定更新方向，未作多重比较或论文聚类校正。无连续训练、无隔离比较。',fontsize=10)
save(fig,'same_panel_update_consequences')
inputs=[ROOT/'analysis_contract.json',ROOT/'representations.npz',ROOT/'update_losses.npz',ROOT/'branches.json',ROOT/'gradient_geometry.npz',PRIOR/'analysis/domain_profiles.npz',PRIOR/'selected.jsonl']
manifest=dict(generator=str(Path(__file__)),generator_sha256=sha(__file__),inputs={str(p):sha(p) for p in inputs},
    files=[dict(evidence_copy=str(p),reading_copy=str(DEST/p.name),sha256=sha(p)) for p in sorted(OUT.iterdir())],
    numeric_artifacts={str(ROOT/n):sha(ROOT/n) for n in ['structure_results.json','update_summary.csv','update_results.json','common_axes.npz']})
(ROOT/'figure_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
(DEST/'structure_update_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(structure=structure,update=checks),indent=2,ensure_ascii=False))
