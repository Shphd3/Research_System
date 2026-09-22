"""Render the requested meeting figures from verified completed evidence.

No probe fitting, resampling, model inference, or statistical tests. Rank
quantiles are descriptive re-aggregation of existing, identity-matched caches.
"""
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
import numpy as np

DAY=Path(__file__).resolve().parents[2]
OUT=DAY/'figures/domain_meeting_final'
OUT.mkdir(parents=True,exist_ok=True)
FONT=Path('/tmp/0921-sae-meeting-font/NotoSansSC.ttf')
if not FONT.exists():
    from urllib.request import urlretrieve
    FONT.parent.mkdir(parents=True,exist_ok=True)
    urlretrieve('https://raw.githubusercontent.com/google/fonts/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf',FONT)
# The upstream variable font defaults to weight 100. Instantiate readable weights.
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
for weight in (400,700):
    static=FONT.with_name(f'NotoSansSC-{weight}.ttf')
    if not static.exists():
        instantiateVariableFont(TTFont(FONT),{'wght':weight},inplace=True).save(static)
    font_manager.fontManager.addfont(str(static))
plt.rcParams.update({'font.family':'Noto Sans SC','font.size':11,'axes.titlesize':13,
                     'axes.labelsize':11,'axes.unicode_minus':False,'pdf.fonttype':42,
                     'svg.fonttype':'path','axes.spines.top':False,'axes.spines.right':False})
BASE=Path('/data/250010109/MoE_Router/experiments')
R21=BASE/'20260920_sae_representation_21b_audit/runs/full_4x5090_retry2_20260921T0200Z'
RS=BASE/'20260921_sae_domain_supplementary_analysis/runs/full_local_cpu_20260921T0645Z'
R15=BASE/'20260920_sae_representation_15b_early_audit/runs/full_15b_4x5090_20260920_wave1'
R08=BASE/'20260920_sae_representation_15b_early_audit/runs/full_early_4x5090_20260920_wave1'
C={'21b_dense':'#27272a','21b_sall_original':'#00856a','21b_s7_reweighted':'#1676b8'}
N={'21b_dense':'Dense','21b_sall_original':'SALL原版','21b_s7_reweighted':'S7重加权'}
MARK={'21b_dense':'o','21b_sall_original':'s','21b_s7_reweighted':'^'}
GRAY='#64748b';PURPLE='#8556a6';INK='#172b3a'
sources={};figures=[];data={}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
    sources[str(p)]=sha(p)
    v=json.loads(Path(p).read_text())
    assert v.get('status','PASS')=='PASS',p
    return v
for root in (R21,RS,R15,R08):
    read(root/'terminal_receipt.json');read(root/'stages/ANALYSIS_PASS.json')
am=read(RS/'artifact_manifest.json')
for entry in am['artifacts']:
    assert sha(entry['path'])==entry['sha256'],entry['path']
p=read(R21/'analysis/primary/primary_metrics.json')
g=read(R21/'analysis/geometry/geometry_cka.json')
o=read(R21/'analysis/observer/observer_metrics.json')
cost=read(R21/'analysis/cost/n8_test_nll.json')
a=read(RS/'readout/domain_readout_metrics.json')
b=read(RS/'observer/observer_and_layer_metrics.json')

def pick(rows,case,layer=8,pool='mean'):
    return next(r for r in rows if r['case']==case and r['layer']==layer and r['pooling']==pool)
def pair(case,layer=8,pool='mean'):
    return next(r for r in a['paired_readout'] if r['contrast']==case+'_minus_21b_dense' and r['layer']==layer and r['pooling']==pool)
def geo(layer=8,pool='mean'):
    return next(r for r in a['geometry_bootstrap'] if r['layer']==layer and r['pooling']==pool)
def frame(title,subtitle):
    fig,axs=plt.subplots(1,2,figsize=(13.8,7.2))
    fig.subplots_adjust(left=.09,right=.97,top=.77,bottom=.25,wspace=.34)
    fig.text(.055,.94,title,fontsize=19,weight='bold',color=INK)
    fig.text(.055,.878,subtitle,fontsize=11,color=GRAY)
    for ax in axs:ax.grid(alpha=.18);ax.set_axisbelow(True)
    return fig,axs
def footer(fig,s):fig.text(.055,.13,s,fontsize=10,color=GRAY,va='top',linespacing=1.7)
def save(fig,stem,selectors,interpretation):
    paths=[]
    for ext in ('png','pdf','svg'):
        target=OUT/(stem+'.'+ext);fig.savefig(target,dpi=200,facecolor='white')
        paths.append({'path':str(target),'sha256':sha(target)})
    plt.close(fig)
    figures.append({'id':stem,'selection':selectors,'interpretation':interpretation,'outputs':paths})

# G0: labelled hypotheses and exact sidecar consumption path.
fig=plt.figure(figsize=(13.8,7.6));ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,14);ax.set_ylim(0,8);ax.axis('off')
ax.text(.55,7.55,'G0  我们希望改变的是领域组织，而不只是向量或得分',fontsize=18,weight='bold',color=INK)
ax.text(.55,7.06,'假设示意，非实测投影。颜色表示来源领域；允许共享方向和部分重叠。',color=GRAY,fontsize=11)
rng=np.random.default_rng(21);domain_colors=['#00856a','#1676b8','#b77637']
for x,title,centers,sd in [(0.6,'希望：简单规则更容易辨认领域',[(1.7,4.8),(3.6,5.55),(5.05,4.6)],(.53,.34)),
                           (7.25,'竞争解释：缩放、拉伸或共同方向改变',[(9,5),(10.2,5.1),(10.6,5.3)],(.96,.23))]:
    ax.add_patch(FancyBboxPatch((x,3.7),6.1,2.95,boxstyle='round,pad=.08',fc='#f6f8fa',ec='#cbd5df'))
    ax.text(x+.15,6.23,title,fontsize=12,weight='bold',color=INK)
    for center,col in zip(centers,domain_colors):
        pts=rng.normal(center,sd,(26,2));pts[:,0]=np.clip(pts[:,0],x+.18,x+5.9);pts[:,1]=np.clip(pts[:,1],4.3,6.0)
        ax.scatter(*pts.T,s=16,color=col,alpha=.72)
    ax.text(x+.15,3.98,'若“领域团分离”机制成立：中心差异相对内部散布增大' if x<1 else '空间或原子得分变化，领域仍可能混杂',fontsize=10,color=GRAY)
def box(x,y,w,label,fc='#edf2f6'):
    ax.add_patch(FancyBboxPatch((x,y),w,.58,boxstyle='round,pad=.04',fc=fc,ec='#8193a3'))
    ax.text(x+w/2,y+.29,label,ha='center',va='center',fontsize=11,color=INK)
def arrow(a0,a1,color=INK,ls='-',rad=0):
    ax.add_patch(FancyArrowPatch(a0,a1,arrowstyle='->',mutation_scale=12,color=color,lw=1.5,ls=ls,connectionstyle=f'arc3,rad={rad}'))
box(.8,2.5,2,'注意力原生写入 a');box(4,2.5,2,'与残差相加');box(7.2,2.5,2,'前馈网络');box(10.4,2.5,2.3,'后续预测')
for l,r in [(2.8,4),(6,7.2),(9.2,10.4)]:arrow((l,2.79),(r,2.79))
box(4,1.25,2,'SAE编码 z','#e9f5ef');box(7.2,1.25,2,'重构 â','#e9f5ef');box(10.4,1.25,2.3,'重构损失','#e9f5ef')
arrow((1.8,2.48),(4,1.53),C['21b_sall_original']);arrow((6,1.54),(7.2,1.54),C['21b_sall_original']);arrow((9.2,1.54),(10.4,1.54),C['21b_sall_original'])
arrow((11.55,1.2),(1.75,2.43),'#a85940','--',-.26)
ax.text(6.9,.22,'虚线：训练时重构损失的梯度可影响上游主干；正常推理仍使用 a',ha='center',fontsize=10,color='#a85940')
ax.text(.75,3.25,'a 取于输出投影后、残差相加前；重构 â 不替换正常主路径。',fontsize=10,color=GRAY)
save(fig,'G0_hypothesis_and_path','Conceptual only; no empirical embeddings. Sidecar path verified in E06 protocol.','Hypothesis and rival, not result or causal proof.')

# F1: follow the requested two-panel absolute-value figure, with updated paired CIs.
fig,axs=frame('F1  SALL领域分类略高，但改善未获确认，质心式分离反而下降','21B｜N8_v1｜原生注意力写入 a｜第8层正文均值｜测试1,600条')
gn=[r for r in g['geometry'] if r['panel']=='N8_v1']
for i,case in enumerate(C):
    acc=100*pick(p['N8_v1'],case)['test_accuracy'];bw=pick(gn,case)['B_over_W']
    for ax,val,fmt in [(axs[0],acc,'.2f'),(axs[1],bw,'.3f')]:
        ax.scatter(i,val,s=100,marker=MARK[case],color=C[case],zorder=4)
        ax.annotate(format(val,fmt),(i,val),xytext=(0,13),textcoords='offset points',ha='center',color=C[case],fontsize=13)
        ax.set_xticks(range(3),N.values());ax.set_xlim(-.45,2.45)
axs[0].set_ylim(70,94);axs[0].set_ylabel('八类测试准确率（%）');axs[0].set_title('能否用简单规则认出领域？')
axs[1].set_ylim(.10,.54);axs[1].set_ylabel('类间 / 类内散度 B/W');axs[1].set_title('领域中心是否相对更分离？')
q=pair('21b_sall_original');h=geo();data['F1']={'paired_readout':q,'geometry':h}
footer(fig,f"SALL − Dense：准确率 {100*q['point']:+.2f} 个百分点，95%配对区间 [{100*q['ci95_percentile'][0]:+.2f}, {100*q['ci95_percentile'][1]:+.2f}]；尚不足以确认改善。\n"
       f"B：755.08 → 712.61；W：1610.22 → 1655.73；Δ(B/W) = {h['point']['B_over_W']:+.4f}，95%区间 [{h['ci95_percentile']['B_over_W'][0]:+.4f}, {h['ci95_percentile']['B_over_W'][1]:+.4f}]。")
save(fig,'F1_readout_and_separation','E06 primary.N8_v1 + geometry.geometry: layer8 mean; supplement paired_readout + geometry_bootstrap','Paired uncertainty is for differences, not error bars on absolute model points; post-hoc record-level intervals.')

# F2 keeps the specification's observed permutation maxima; updated q95 goes in backup.
fig,axs=frame('F2  S7变化更大却未更好；SALL预测更好，原因尚未确定','左：开发集800条的几何诊断　　右：测试1,600条、408,000个有效预测词元')
fig.subplots_adjust(left=.14,wspace=.42)
f2=[]
for y,case in enumerate(['21b_sall_original','21b_s7_reweighted']):
    r=next(z for z in g['n8_cka_dev_permutations'] if z['right']==case and z['layer']==8 and z['pooling']=='mean')['u_corrected']
    axs[0].scatter(r['observed'],y,marker=MARK[case],s=95,color=C[case],zorder=4)
    axs[0].scatter(r['permutation_max']['global'],y,marker='x',s=70,color='#8a96a3',zorder=3)
    axs[0].scatter(r['permutation_max']['within_category'],y,marker='D',s=55,facecolors='none',edgecolors=GRAY,zorder=3)
    axs[0].annotate(f"{r['observed']:.4f}",(r['observed'],y),xytext=(0,13),textcoords='offset points',ha='center',color=C[case])
    n=next(z for z in cost['paired_contrasts'] if z['contrast']==case+'_minus_21b_dense')
    v=n['mean_record_nll_difference'];lo,hi=n['paired_record_bootstrap_ci95']
    axs[1].errorbar(v,y,xerr=[[v-lo],[hi-v]],fmt=MARK[case],color=C[case],ms=8,capsize=5,lw=2)
    axs[1].annotate(f'{v:+.5f}',(v,y),xytext=(0,17),textcoords='offset points',ha='center',color=C[case])
    f2.append({'case':case,'cka':r,'nll':n})
axs[0].set_yticks([0,1],['Dense—SALL原版','Dense—S7重加权']);axs[0].set_xlim(-.035,1.03);axs[0].set_ylim(1.7,-.7)
axs[0].set_xlabel('有限样本修正版线性 CKA');axs[0].set_title('样本之间的关系保留多少一致性？')
axs[0].legend(handles=[Line2D([],[],marker='o',color='none',mfc=INK,mec=INK,label='真实对应'),Line2D([],[],marker='x',color='none',mec=GRAY,label='全局乱序最大值'),Line2D([],[],marker='D',color='none',mfc='none',mec=GRAY,label='类内乱序最大值')],fontsize=9,loc='lower center',frameon=False)
axs[1].set_yticks([0,1],['SALL原版','S7重加权']);axs[1].set_ylim(1.7,-.7);axs[1].axvline(0,color=GRAY,lw=1)
axs[1].set_xlim(-.034,.015);axs[1].set_xlabel('相对Dense的预测损失差（nat / 有效预测词元）');axs[1].set_title('正常主路径的语言预测是否获益？')
footer(fig,'左图参照为原审计100次乱序的观测最大值，不是95%置信上界；CKA不是语义保留百分比。\n右图横线为记录配对95%区间，负值表示预测损失更低；两项测量之间没有建立因果联系。')
data['F2']=f2
save(fig,'F2_geometry_and_prediction','E06 n8_cka_dev_permutations: L8 mean, u_corrected; cost.paired_contrasts','Use original maxima exactly as specification; supplementary q95 is separately documented.')

# F3 reads ranked caches with exact input/token alignment and manifests.
rank_data=[];keys_all=[]
for case,w in [('21b_sall_original',1),('21b_s7_reweighted',2)]:
    mf=read(R21/f'workers/worker_{w}/observer/observer_manifest.json');arr=[];keys=[];mass=[]
    for c in mf['chunks']:
        if c['panel']!='N8_v1' or c['human_layer']!=8:continue
        f=Path(c['npz']);assert sha(f)==c['sha256'];sources[str(f)]=c['sha256']
        with np.load(f,allow_pickle=False) as z:
            arr.append(z['rank_scores_1_to_128']);mass.append(z['top32_positive_mass_fraction'])
            keys.extend((str(z['sequence_ids'][i]),str(z['input_hashes'][i]),int(t)) for i,t in zip(z['token_local_row'],z['token_position']))
    ranks=np.concatenate(arr).astype(np.float64);assert ranks.shape==(49152,128);assert np.all(np.diff(ranks,axis=1)<=0)
    assert (ranks[:,31]>0).all();keys_all.append(keys)
    gap=float(np.median((ranks[:,31]-ranks[:,32])/ranks[:,31]));mass=float(np.median(np.concatenate(mass)))
    row=next(r for r in o['conditions'] if r['case']==case and r['panel']=='N8_v1' and r['human_layer']==8)['rank_tail_and_fidelity']
    assert np.isclose(gap,row['relative_rank32_33_gap_quantiles'][1]);assert np.isclose(mass,row['top32_positive_mass_fraction_quantiles'][1])
    rank_data.append({'case':case,'q1':np.quantile(ranks/ranks[:,0,None],[.1,.5,.9],axis=0),'q32':np.quantile(ranks/ranks[:,31,None],[.1,.5,.9],axis=0),'gap':gap,'mass':mass})
assert keys_all[0]==keys_all[1] and len(set(keys_all[0]))==49152
fig,axs=frame('F3  S7头部更集中，但两模型都没有在第32名突然截断','21B｜N8固定观察器面板192条 / 49,152词元｜第8层｜截断前候选得分')
xx=np.arange(1,129)
for z in rank_data:
    case=z['case']
    for ax,key,mask in [(axs[0],'q1',xx>0),(axs[1],'q32',(xx>=24)&(xx<=40))]:
        q=z[key];ax.plot(xx[mask],q[1,mask],color=C[case],label=N[case],lw=2,ls='-' if case.endswith('original') else '--')
        ax.fill_between(xx[mask],q[0,mask],q[2,mask],color=C[case],alpha=.12)
    axs[1].text(.04,.89 if case.endswith('original') else .79,f"{N[case]}：32/33相对落差中位数 {100*z['gap']:.2f}%",transform=axs[1].transAxes,color=C[case],fontsize=10)
axs[0].set_title('整体得分形状');axs[0].set_xlabel('每个词元独立排序后的名次');axs[0].set_ylabel('得分 / 该词元第1名得分');axs[0].set_xlim(1,128);axs[0].set_ylim(0,1.03)
axs[1].set_title('第32 / 33名附近放大');axs[1].set_xlabel('截断前名次（局部放大：24—40）');axs[1].set_ylabel('得分 / 该词元第32名得分');axs[1].set_xticks([24,28,32,33,36,40]);axs[1].set_ylim(.55,1.9)
for ax in axs:ax.axvline(32,color=GRAY,ls=':',lw=1);ax.legend(frameon=False,loc='upper right' if ax==axs[0] else 'lower left',fontsize=10)
axs[1].axvline(33,color='#aeb7c0',ls=':',lw=.8)
footer(fig,f"前32项占全部正得分和：SALL原版 {100*rank_data[0]['mass']:.2f}%；S7重加权 {100*rank_data[1]['mass']:.2f}%——不是信息保留率。\n阴影为词元间10%—90%分位数，不是置信区间；归一化、32/33落差均先逐词元计算，再取分位数。")
data['F3']=[{k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in z.items()} for z in rank_data]
save(fig,'F3_pre_topk_rank','E06 manifest-hashed N8 observer L8 caches; per-token rank1/rank32 normalization; 10/50/90% quantiles','Same 49,152 token identities; descriptive distribution bands; no new inference.')

# A1 uses actual chronological checkpoints, never a S7 extrapolation.
fig,axs=frame('A1  领域可读性随训练提高，但SAE额外优势没有持续扩大','N8_v1｜原生注意力写入｜第8层正文均值｜每点独立拟合读出；检查点不是训练重复')
times=[0,.5,1,3,5,10,15,21];ys={c:[] for c in ['dense','sall_original']}
for t in times:
    root=R08/f'analysis/time_{int(t*1e9)}' if t<=10 else (R15/'analysis/15b' if t==15 else R21/'analysis')
    rows=read(root/'primary/primary_metrics.json')['N8_v1']
    for m in ys:ys[m].append(100*next(r['test_accuracy'] for r in rows if r['case'].endswith('_'+m) and r['layer']==8 and r['pooling']=='mean'))
for m,v in ys.items():axs[0].plot(times,v,marker=MARK['21b_'+m],color=C['21b_'+m],label=N['21b_'+m],lw=1.8)
delta=np.array(ys['sall_original'])-ys['dense'];axs[1].plot(times,delta,'s-',color=C['21b_sall_original']);axs[1].axhline(0,color=GRAY,lw=1)
axs[0].set_ylabel('八类测试准确率（%）');axs[1].set_ylabel('SALL − Dense（百分点）');axs[0].legend(frameon=False)
for ax in axs:ax.axvline(9.174381056,color=GRAY,ls=':',lw=1);ax.set_xlabel('累计训练词元（十亿）')
axs[0].set_title('两模型共有的成长');axs[1].set_title('扣除Dense后的额外变化')
footer(fig,'只连接0、0.5、1、3、5、10、15、21B的真实点；虚线为SALL在9.174B的续接分叉，连线仅作阅读引导。\n本轮没有S7完整早期轨迹；0B已高于12.5%机会水平，领域标签可读不自动等于抽象语义。')
data['A1']={'times_B':times,'accuracy_pct':ys,'difference_pp':delta.tolist()}
save(fig,'A1_training_trajectory','E08/E07/E06 primary.N8_v1, L8 mean','Descriptive points only; no interpolation, smoothing or independent-seed inference.')

# A2: the two newly completed structural/observer analyses.
fig,axs=frame('A2  S7后层关系变化更大；SALL字典含可留出读出的类别线索','左：同模型、开发集800条、第8层以前的相邻层　　右：固定观察器测试64条、每组8原子')
for case in C:
    r=next(z for z in b['same_model_layer_cka']['same_model_matrices'] if z['case']==case and z['pooling']=='mean' and z['estimator']=='u_corrected')
    mat=np.array(r['matrix_human_layers_1_to_8']);v=np.diag(mat,1)
    axs[0].plot(range(1,8),v,marker=MARK[case],color=C[case],label=N[case],lw=1.8)
    axs[0].annotate(f'{v[-1]:.4f}',(7,v[-1]),xytext=(-8,10 if case=='21b_dense' else -17),textcoords='offset points',ha='right',color=C[case])
axs[0].set_xticks(range(1,8),[f'{i}→{i+1}' for i in range(1,8)]);axs[0].set_xlabel('相邻人类层号');axs[0].set_ylabel('有限样本修正版线性 CKA');axs[0].set_ylim(.30,1);axs[0].legend(frameon=False,fontsize=9);axs[0].set_title('变化集中在什么位置？')
groups=[]
for y,(case,layer) in enumerate([('21b_sall_original',4),('21b_sall_original',8),('21b_s7_reweighted',8)]):
    r=next(z for z in b['observer_conditions'] if z['case']==case and z['layer']==layer)['atom_analysis']
    v=100*r['candidate_group_probe']['test_balanced_accuracy'];hf=100*r['high_frequency_group_probe']['test_balanced_accuracy'];q=100*np.array(r['random_control']['test_balanced_accuracy_quantiles'])
    axs[1].plot(q[[0,2]],[y,y],color='#9aa5b1',lw=5,alpha=.5);axs[1].scatter(q[1],y,color=GRAY,marker='|',s=95)
    axs[1].scatter(v,y+.10,marker=MARK[case],color=C[case],s=80);axs[1].scatter(hf,y-.12,facecolor='white',edgecolor=C[case],marker=MARK[case],s=70)
    axs[1].annotate(f'{v:.2f}%',(v,y+.10),xytext=(6,5),textcoords='offset points',fontsize=10,color=C[case]);groups.append({'case':case,'layer':layer,'selected':v,'highfreq':hf,'random_q':q.tolist()})
axs[1].set_yticks([0,1,2],['SALL原版 L4','SALL原版 L8','S7重加权 L8']);axs[1].set_ylim(2.55,-.55);axs[1].set_xlim(5,70);axs[1].axvline(12.5,color=GRAY,ls=':',lw=1);axs[1].set_xlabel('八类测试准确率（%）');axs[1].set_title('fit选择的原子组合能否在test复现？')
footer(fig,'右图：实心＝fit选8原子；空心＝最高频8原子；灰段＝覆盖率匹配随机组2.5%—97.5%分位范围（不是置信区间）。\n只支持来源类别相关的组合，不证明抽象语义原子或模型使用；低CKA也不等于更好或完全随机。')
data['A2']=groups
save(fig,'A2_layers_and_atom_groups','Supplement observer.same_model_layer_cka.same_model_matrices mean/u_corrected; observer_conditions.atom_analysis','No new layer statistics or group selection; use completed supplementary outputs only.')

# A3: post-hoc paired estimates, plus completed lexical/normalization checks.
fig,axs=frame('A3  小幅分类正差依赖读点；来源词汇本身已能很好分类','补充A｜固定模型与探针｜记录配对95%区间不覆盖训练随机性｜新增分析为事后探索')
for j,(layer,pool) in enumerate([(4,'mean'),(4,'last'),(8,'mean'),(8,'last')]):
    for off,case in [(-.11,'21b_sall_original'),(.11,'21b_s7_reweighted')]:
        r=pair(case,layer,pool);v=100*r['point'];lo,hi=100*np.array(r['ci95_percentile'])
        axs[0].errorbar(v,j+off,xerr=[[v-lo],[hi-v]],fmt=MARK[case],color=C[case],capsize=3,ms=6,label=N[case] if j==0 else None)
axs[0].axvline(0,color=GRAY,lw=1);axs[0].set_yticks(range(4),['L4 均值','L4 末词','L8 均值','L8 末词']);axs[0].invert_yaxis();axs[0].set_xlabel('相对Dense的准确率差（百分点）');axs[0].set_title('四个固定读点全部报告');axs[0].legend(frameon=False,fontsize=9)
for i,case in enumerate(C):
    for trans,dy,fill in [('registered_global_rms',-.12,True),('fit_centered_row_unit',.12,False)]:
        r=next(z for z in a['conditions'] if z['case']==case and z['layer']==8 and z['pooling']=='mean' and z['transform']==trans)
        val=100*r['test_balanced_accuracy'];axs[1].scatter(val,i+dy,color=C[case] if fill else 'white',edgecolor=C[case],marker=MARK[case],s=70)
tf=100*a['lexical_and_surface_baselines']['tfidf_1_2gram']['test_balanced_accuracy'];sf=100*a['lexical_and_surface_baselines']['surface_six_features']['test_balanced_accuracy']
axs[1].scatter(tf,3,marker='D',color=PURPLE,s=75);axs[1].scatter(sf,4,marker='D',color=GRAY,s=75)
for y,val in [(3,tf),(4,sf)]:axs[1].annotate(f'{val:.2f}%',(val,y),xytext=(5,-3),textcoords='offset points')
axs[1].set_yticks(range(5),[*N.values(),'词汇 TF-IDF','6项表面统计']);axs[1].set_ylim(4.6,-.6);axs[1].set_xlim(25,98);axs[1].set_xlabel('测试准确率（%）');axs[1].set_title('词面与单位范数敏感性')
footer(fig,'右图实心＝原fit中心化+整体RMS；空心＝fit中心化后逐样本单位范数。L8均值SALL−Dense由+0.75降至+0.25个百分点。\n词汇基线89.81%表明标签含强词面线索，不证明模型只使用词面；L8末词正差不能升级为新确认结论。')
save(fig,'A3_paired_and_lexical','Supplement paired_readout all 4 fixed conditions; conditions L8 mean both transforms; lexical_and_surface_baselines','Pointwise post-hoc CIs; model baselines and vocabulary are not causal or capacity-matched comparisons.')

manifest={'status':'PASS','script':str(Path(__file__).resolve()),'script_sha256':sha(__file__),
          'font':{'path':str(FONT),'sha256':sha(FONT),'source':'https://github.com/google/fonts/tree/main/ofl/notosanssc'},
          'source_files':sources,'figures':figures,'figure_count':len(figures),
          'scope':'New reading figures only. Original documents unchanged. No new fitting, resampling, inference or experiment.',
          'rank_identity':'PASS: 49,152 unique identical sample/input-hash/position tuples',
          'updates_to_template':['F1 paired interval now available','A/B completed; C remains NOT RUN','Same-model CKA and source-related atom groups added in A2','Lexical and normalization results added in A3','F2 retains original permutation maxima, not new q95']}
(OUT/'figure_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
(DAY/'meeting_domain_final/assets/figure_values.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':'PASS','figures':len(figures),'sources':len(sources),'output':str(OUT)},ensure_ascii=False))
