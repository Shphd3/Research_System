"""Reading figures from completed metrics; no model load, refit, or resampling."""
import csv
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

DAY=Path(__file__).resolve().parents[2]
OUT=DAY/'figures/domain_structure_complete';OUT.mkdir(exist_ok=True)
ASSET=Path(__file__).parent
FONT=Path('/tmp/0921-sae-meeting-font/NotoSansSC.ttf')
if not FONT.exists():
    from urllib.request import urlretrieve
    FONT.parent.mkdir(parents=True,exist_ok=True)
    urlretrieve('https://raw.githubusercontent.com/google/fonts/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf',FONT)
for weight in (400,700):
    static=FONT.with_name(f'NotoSansSC-{weight}.ttf')
    if not static.exists():
        from fontTools.ttLib import TTFont
        from fontTools.varLib.instancer import instantiateVariableFont
        instantiateVariableFont(TTFont(FONT),{'wght':weight},inplace=True).save(static)
    font_manager.fontManager.addfont(str(static))
plt.rcParams.update({'font.family':'Noto Sans SC','font.size':11,'axes.titlesize':13,
    'axes.unicode_minus':False,'pdf.fonttype':42,'svg.fonttype':'path',
    'axes.spines.top':False,'axes.spines.right':False})
BASE=Path('/data/250010109/MoE_Router/experiments')
R21=BASE/'20260920_sae_representation_21b_audit/runs/full_4x5090_retry2_20260921T0200Z'
R15=BASE/'20260920_sae_representation_15b_early_audit/runs/full_15b_4x5090_20260920_wave1'
R08=BASE/'20260920_sae_representation_15b_early_audit/runs/full_early_4x5090_20260920_wave1'
COL={'dense':'#27272a','sall_original':'#00856a','s7_reweighted':'#1676b8'}
NAME={'dense':'Dense','sall_original':'SALL原版','s7_reweighted':'S7重加权'}
MARK={'dense':'o','sall_original':'s','s7_reweighted':'^'}
sources={};figures=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
    sources[str(p)]=sha(p);j=json.loads(Path(p).read_text())
    assert j.get('status','PASS') in ['PASS','VALIDATED'],p
    return j
def frame(title,sub,n=2):
    fig,axs=plt.subplots(1,n,figsize=(14,7.4))
    fig.subplots_adjust(left=.085,right=.96,top=.76,bottom=.26,wspace=.33)
    fig.text(.045,.94,title,fontsize=18,weight='bold',color='#172b3a')
    fig.text(.045,.875,sub,fontsize=10.5,color='#64748b')
    for ax in np.ravel(axs):ax.grid(alpha=.17);ax.set_axisbelow(True)
    return fig,np.ravel(axs)
def save(fig,name,note,selection):
    fig.text(.045,.125,note,va='top',fontsize=10,color='#52677b',linespacing=1.7)
    files=[]
    for ext in ['png','pdf','svg']:
        p=OUT/f'{name}.{ext}';fig.savefig(p,dpi=180,facecolor='white');files.append({'path':str(p),'sha256':sha(p)})
    plt.close(fig);figures.append({'id':name,'selection':selection,'files':files})
def export(name,rows):
    p=ASSET/(name+'.csv')
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
def geom(j,m,layer=8,pool='mean'):
    return next(r for r in j['geometry'] if r['panel']=='N8_v1' and r['case'].endswith('_'+m) and r['layer']==layer and r['pooling']==pool)
def spec(j,m,layer=8,pool='mean'):
    return next(r for r in j['fit_spectrum'] if r['panel']=='N8_v1' and r['case'].endswith('_'+m) and r['layer']==layer and r['pooling']==pool)
def cka(j,m='sall_original',layer=8,pool='mean',n=800):
    return next(r for r in j['n8_cka_first_pc_and_nested_sizes'] if r['right'].endswith('_'+m) and r['layer']==layer and r['pooling']==pool and r['n']==n)

# Freeze exact coordinate identity using extraction and checkpoint manifests.
coordinates=[]
for root in [R08,R15,R21]:
    read(root/'terminal_receipt.json');read(root/'stages/ANALYSIS_PASS.json')
    seen=set()
    for f in sorted(root.glob('workers/*/extraction_manifest.json')):
        e=read(f)
        if 'N8_v1' not in e['panels'] or e['case'] in seen:continue
        seen.add(e['case']);cp=Path(e['checkpoint']);m=read(cp/'manifest.json')
        assert m['complete'] and m['tokens_seen']==m['milestone_target_tokens']
        state=next(x for x in m['files'] if x['path']=='state.pt')
        assert state['sha256']==e['checkpoint_state_sha256_manifest_claim']
        coordinates.append({'case':e['case'],'tokens_seen':m['tokens_seen'],'optimizer_step':m['optimizer_step'],
            'world_size':m['parallel']['world_size'],'checkpoint':str(cp),'manifest_sha256':sha(cp/'manifest.json'),
            'state_sha256_manifest_claim':state['sha256'],'state_hash_recomputed_this_turn':False,
            'extraction_manifest':str(f),'extraction_loader_validated':e['checkpoint_loader_validated_manifest']})
coordinates.sort(key=lambda r:(r['tokens_seen'],r['case']))
assert len(coordinates)==17
for m in ['dense','sall_original']:
    assert [r['tokens_seen'] for r in coordinates if r['case'].endswith('_'+m)]==[0,500000000,1000000000,3000000000,5000000000,10000000000,15000000000,21000000000]
export('checkpoint_coordinates',coordinates)
lineage={}
for m in ['sall_original','s7_reweighted']:
    cp=Path(next(r['checkpoint'] for r in coordinates if r['case']=='21b_'+m))
    lineage[m]=read(cp.parents[1]/'fork_lineage.json')
times=[0,.5,1,3,5,10,15,21];geo_by_time={};trajectory=[]
for t in times:
    p=(R08/f'analysis/time_{int(t*1e9)}' if t<=10 else R15/'analysis/15b' if t==15 else R21/'analysis')
    j=read(p/'geometry/geometry_cka.json');geo_by_time[t]=j
    pri=read(p/'primary/primary_metrics.json')
    for m in ['dense','sall_original']:
        g=geom(j,m);s=spec(j,m);k=cka(j)
        acc=next(x['test_accuracy'] for x in pri['N8_v1'] if x['case'].endswith('_'+m) and x['layer']==8 and x['pooling']=='mean')
        trajectory.append({'tokens_seen':int(t*1e9),'model':m,'accuracy':acc,'rms_norm':np.sqrt(g['mean_squared_norm']),
            'mean_vector_norm':g['mean_vector_norm'],'centered_rms':np.sqrt(g['T_class_balanced']),
            'B_over_W':g['B_over_W'],'first_pc_fraction':s['first_pc_fraction'],'top16_fraction':s['top16_fraction'],
            'effective_variance_dimension':s['effective_variance_dimension'],
            'dense_sall_cka':k['raw']['u_corrected'],'dense_sall_cka_remove_pc1':k['fit_first_pc_removed']['u_corrected']})
export('training_trajectory',trajectory)
j=geo_by_time[21]
norms=[]
for r in j['geometry']:
    if r['panel']!='N8_v1':continue
    assert np.isclose(r['mean_squared_norm'],r['T_class_balanced']+r['mean_vector_norm']**2,rtol=1e-9)
    norms.append({**r,'rms_norm':np.sqrt(r['mean_squared_norm']),'centered_rms':np.sqrt(r['T_class_balanced']),
                  'mean_energy_fraction':r['mean_vector_norm']**2/r['mean_squared_norm']})
export('norm_and_dispersion_21b_all_layers',norms)
spectra=[r for r in j['fit_spectrum'] if r['panel']=='N8_v1'];export('spectrum_summary_21b',spectra)
export('cka_pc_sensitivity_21b',[{k:v for k,v in r.items() if k not in ['raw','fit_first_pc_removed']}|
    {'raw_u':r['raw']['u_corrected'],'removed_u':r['fit_first_pc_removed']['u_corrected'],
     'raw_biased':r['raw']['biased'],'removed_biased':r['fit_first_pc_removed']['biased']}
    for r in j['n8_cka_first_pc_and_nested_sizes']])
matrices=[r for r in j['n8_cka_dev_matrices'] if r['estimator']=='u_corrected']
export('cka_all_layer_pairs',[{'left':r['left'],'right':r['right'],'pooling':r['pooling'],'left_layer':l+1,'right_layer':k+1,'cka':v}
    for r in matrices for l,row in enumerate(r['matrix_human_layers_1_to_8']) for k,v in enumerate(row)])

fig,axs=frame('S1  S7的跨模型关系差异集中在末层；均值与末词都要看','21B｜N8开发集800条｜原生注意力输出｜有限样本修正版线性CKA')
for ax,pool,title in zip(axs,['mean','last'],['正文均值','最后正文词元']):
    for r in matrices:
        if r['pooling']!=pool:continue
        pair=(r['left'].removeprefix('21b_'),r['right'].removeprefix('21b_'))
        color=COL[pair[1]] if pair[0]=='dense' else '#8556a6'
        vals=np.diag(r['matrix_human_layers_1_to_8'])
        marker=MARK[pair[1]] if pair[0]=='dense' else 'D'
        ax.plot(range(1,9),vals,marker=marker,color=color,label=f'{NAME[pair[0]]}—{NAME[pair[1]]}',lw=1.8)
    ax.set(title=title,xlabel='同层比较：人类层号',ylabel='CKA',xticks=range(1,9),ylim=(0,1.05));ax.legend(fontsize=8.5,frameon=False)
save(fig,'S1_cka_layers','每个点比较同一层、同一批输入；连线只表示层序。低CKA不是语义丢失比例。\n完整跨层矩阵另见S9；同模型跨层关系已在上一版A2汇报。','21B n8_cka_dev_matrices u_corrected diagonal, mean/last, all3 pairs')

fig,axs=frame('S2  S7末层写入幅度很小；SALL更大的总幅度主要对应均值项','21B｜N8测试1,600条｜正文均值向量｜纵轴为对数刻度，不能把小幅度直接叫信息塌缩')
for m in COL:
    rr=[geom(j,m,l) for l in range(1,9)]
    for ax,key in zip(axs,['mean_squared_norm','T_class_balanced']):
        v=np.sqrt([r[key] for r in rr]);ax.plot(range(1,9),v,marker=MARK[m],color=COL[m],label=NAME[m]);ax.set_yscale('log')
        ax.annotate(f'{v[-1]:.3f}',(8,v[-1]),xytext=(-3,-18 if m=='dense' else 9),textcoords='offset points',ha='right',color=COL[m])
axs[0].set_title('相对原点的RMS范数');axs[1].set_title('减去该模型均值后的RMS半径')
for ax in axs:ax.set(xlabel='人类层号',ylabel='向量长度（log刻度）',xticks=range(1,9));ax.legend(frameon=False,fontsize=9)
save(fig,'S2_norm_decomposition','RMS² = 平均向量长度² + 中心化RMS²（本面板各类等量，中心化总量=B+W）。\n第8层Dense/SALL中心化半径为48.63/48.67；总RMS为95.02/108.95。不同坐标的均值不代表同一方向。','geometry N8_v1 test mean layers1-8; algebraic square roots and identity checked')

fig,axs=frame('S3  SALL均值表示的方差更分散；S7更多方差落在少数方向','21B｜N8拟合集2,400条｜各条件独立中心化协方差｜已有谱摘要，不是完整逐秩方差谱',3)
conditions=[(4,'mean'),(8,'mean'),(4,'last'),(8,'last')]
for ax,key,title,scale in zip(axs,['first_pc_fraction','top16_fraction','effective_variance_dimension'],['第一主成分占比','前16方向累计占比','有效方差维度'],[100,100,1]):
    for i,m in enumerate(COL):
        v=[spec(j,m,l,p)[key]*scale for l,p in conditions]
        ax.scatter(np.arange(4)+(i-1)*.15,v,marker=MARK[m],color=COL[m],s=45,label=NAME[m])
    ax.set_title(title);ax.set_xticks(range(4),['L4均值','L8均值','L4末词','L8末词'],rotation=25);ax.set_ylabel('%' if scale==100 else '参与率维度');ax.legend(fontsize=8,frameon=False)
save(fig,'S3_spectrum_summaries','有效维度 = (Σλ)² / Σλ²；不是矩阵秩、语义维数或SAE激活数。\n没有保存完整特征值向量，因此不从PC1与Top16两个摘要伪造方差谱曲线。','fit_spectrum N8_v1 all12 rows; original covariance n-1 denominator, nonnegative eigenvalues')

fig,axs=frame('S4  去掉各模型首主成分后，S7的差异仍在；不能仅归因于一个共同方向','21B｜N8开发集嵌套256/512/800条｜首方向仅在fit估计｜有限样本修正版CKA')
for ax,pool in zip(axs,['mean','last']):
    for m in ['sall_original','s7_reweighted']:
        for key,ls,suffix in [('raw','-','原始'),('fit_first_pc_removed','--','去首PC')]:
            v=[cka(j,m,pool=pool,n=n)[key]['u_corrected'] for n in [256,512,800]]
            ax.plot([256,512,800],v,ls=ls,marker=MARK[m],color=COL[m],label=f'Dense—{NAME[m]} {suffix}')
    ax.set(title='第8层正文均值' if pool=='mean' else '第8层最后词元',xlabel='开发集记录数',ylabel='CKA',xticks=[256,512,800],ylim=(.1,1.02));ax.legend(fontsize=8,frameon=False)
save(fig,'S4_cka_pc_sensitivity','n=800均值：Dense—SALL 0.9443→0.9136；Dense—S7 0.4092→0.3273。\n两模型各自去掉fit主方向，属于敏感性诊断，不是已定位的因果机制；嵌套样本不是独立重复。','n8_cka_first_pc_and_nested_sizes layer8 both pools all3 n; raw and removed u_corrected')

def series(m,key):return [r[key] for r in trajectory if r['model']==m]
def timeaxes(ax):
    ax.axvline(9.174381056,color='#8090a0',ls=':',lw=1)
    ax.set_xlabel('累计训练词元（十亿，来自检查点manifest）')
fig,axs=frame('S5  样本关系持续相似，质心分离的相对差异随训练变化','N8｜第8层正文均值｜CKA用dev800条；B/W用test1,600条｜单训练谱系')
for key,ls,label in [('dense_sall_cka','-','原始'),('dense_sall_cka_remove_pc1','--','去fit首PC')]:
    axs[0].plot(times,series('dense',key),ls=ls,marker='o',color=COL['sall_original'],label=label)
for m in ['dense','sall_original']:axs[1].plot(times,series(m,'B_over_W'),marker=MARK[m],color=COL[m],label=NAME[m])
axs[0].set(title='同一时刻Dense—SALL关系一致性',ylabel='CKA',ylim=(.87,1.02));axs[1].set(title='领域中心相对内部散布',ylabel='B/W')
for ax in axs:timeaxes(ax);ax.legend(frameon=False,fontsize=10)
save(fig,'S5_geometry_trajectory','虚线为SALL在9.174B的续接分叉。原始CKA约0.944—0.970（非零时刻），不是单调演化。\n这是跨模型、同时间的CKA；不是同模型跨时间的方向稳定性。','all8 actual checkpoints L8mean raw/removed n800 and B/W')

fig,axs=frame('S6  总幅度与样本间变化具有不同轨迹，不能只汇报一个范数','N8测试1,600条｜第8层正文均值｜RMS基于已保存二阶矩；未报告平均样本范数')
for m in ['dense','sall_original']:
    for ax,key in zip(axs,['rms_norm','centered_rms']):ax.plot(times,series(m,key),marker=MARK[m],color=COL[m],label=NAME[m])
axs[0].set(title='相对原点的总RMS',ylabel='RMS向量长度');axs[1].set(title='减去均值后的RMS',ylabel='中心化RMS半径')
for ax in axs:timeaxes(ax);ax.legend(frameon=False)
save(fig,'S6_norm_trajectory','21B时SALL的总RMS更大，但中心化RMS与Dense近似相同；尺度与中心偏移必须分开。\n点间连线是阅读引导；没有分叉附近密集检查点，不能把末期变化归因于某次操作。','all8 checkpoints geometry L8mean square roots of mean_squared_norm and T_class_balanced')

fig,axs=frame('S7  方差集中度随训练变化；有效维度没有持续单调减少','N8拟合集2,400条｜第8层正文均值｜全局谱摘要不是类别子空间证据')
for m in ['dense','sall_original']:
    axs[0].plot(times,100*np.array(series(m,'top16_fraction')),marker=MARK[m],color=COL[m],label=NAME[m])
    axs[1].plot(times,series(m,'effective_variance_dimension'),marker=MARK[m],color=COL[m],label=NAME[m])
axs[0].set(title='前16方向承载的总方差',ylabel='累计方差（%）');axs[1].set(title='有效方差维度',ylabel='参与率维度')
for ax in axs:timeaxes(ax);ax.legend(frameon=False)
save(fig,'S7_spectrum_trajectory','0B有效维度约65.45，0.5B约11；之后回升并波动。21B SALL为18.63、Dense为15.45。\n更高或更低都不是预设的好坏；全局方差方向不一定是领域判别方向。','all8 checkpoints fit_spectrum L8mean top16 and effective_variance_dimension')

fig,ax=plt.subplots(figsize=(14,5.8));fig.subplots_adjust(left=.14,right=.96,top=.70,bottom=.32)
fig.text(.045,.92,'S8  实测训练坐标与分叉：所有点来自真实检查点',fontsize=19,weight='bold',color='#172b3a')
fig.text(.045,.84,'横轴为manifest.tokens_seen；S7只有21B审计点，不拼接旧S7或新从头训练曲线',fontsize=11,color='#64748b')
for y,m in enumerate(['dense','sall_original','s7_reweighted']):
    rows=[r for r in coordinates if r['case'].endswith('_'+m)];xs=[r['tokens_seen']/1e9 for r in rows]
    ax.scatter(xs,[y]*len(xs),color=COL[m],marker=MARK[m],s=70,zorder=4)
    if m!='s7_reweighted':ax.plot(xs,[y]*len(xs),color=COL[m],alpha=.35)
for y,t,label in [(1,9.174381056,'SALL续接 9.174381056B'),(2,15.465567744,'S7调系数 15.465567744B')]:
    ax.scatter(t,y,marker='|',color='#a85940',s=400,zorder=5)
    ax.annotate(label,(t,y),xytext=(0,17),textcoords='offset points',ha='center',fontsize=10,color='#a85940')
ax.set(yticks=range(3),yticklabels=NAME.values(),xlabel='累计训练词元（十亿）',ylim=(2.5,-.7),xlim=(-.5,22))
ax.grid(axis='x',alpha=.2)
save(fig,'S8_checkpoint_coordinates','Dense/SALL实测0、0.5、1、3、5、10、15、21B；短竖线是分叉事件，不是新增表征测量点。\n同词元数控制训练量，不自动保证优化条件完全匹配；CSV同时列出optimizer_step、world_size与完整checkpoint路径。','17 extraction+checkpoint manifest identities; two validated fork_lineage records; state hashes are manifest claims')

fig,axs=frame('S9  完整跨层矩阵：同层差异不能由一个末层数字代替','21B｜N8开发集800条｜正文均值｜行＝Dense层，列＝对照模型层｜统一色阶')
for ax,m in zip(axs,['sall_original','s7_reweighted']):
    r=next(r for r in matrices if r['pooling']=='mean' and r['left']=='21b_dense' and r['right']=='21b_'+m)
    mat=np.array(r['matrix_human_layers_1_to_8']);im=ax.imshow(mat,vmin=0,vmax=1,cmap='viridis',origin='upper')
    for l in range(8):
        for k in range(8):ax.text(k,l,f'{mat[l,k]:.2f}',ha='center',va='center',fontsize=8,color='white' if mat[l,k]<.5 else '#172b3a')
    ax.set(title=f'Dense × {NAME[m]}',xticks=range(8),xticklabels=range(1,9),yticks=range(8),yticklabels=range(1,9),xlabel=NAME[m]+'层号',ylabel='Dense层号');ax.grid(False)
fig.colorbar(im,ax=axs.tolist(),fraction=.025,pad=.02,label='CKA')
save(fig,'S9_cka_cross_layer_matrices','对角线是同层比较，非对角线是不同层的样本关系一致性。颜色表示关系相似，不表示模型质量。\n未逐格做显著性筛选；不从矩阵挑一个亮格就宣布层间功能对应。','n8_cka_dev_matrices u_corrected mean Dense-SALL/Dense-S7 full8x8')

sourcecode=BASE/'20260920_sae_representation_21b_audit/scripts/analyze_geometry.py';sources[str(sourcecode)]=sha(sourcecode)
manifest={'status':'PASS','scope':'Existing metrics and checkpoint metadata only; algebraic norm decomposition; no new inference/statistical tests.',
 'source_files':sources,'figures':figures,'script_sha256':sha(__file__),'norm_identity':'PASS all48 N8 norm rows',
 'norm_definition':'mean_vector_norm=norm(mean(x)), NOT mean(norm(x)); RMS=sqrt(mean_squared_norm)',
 'spectrum_boundary':'Only first_pc_fraction/top16_fraction/participation dimension saved; full eigenvalue curve missing.',
 'checkpoint_count':len(coordinates),'lineage':lineage}
(OUT/'figure_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(ASSET/'all_values.json').write_text(json.dumps({'norms':norms,'spectra':spectra,'trajectory':trajectory,'coordinates':coordinates,'lineage':lineage},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','figures':len(figures),'sources':len(sources),'checkpoints':len(coordinates)}))
