from pathlib import Path
import csv,json,hashlib,shutil,datetime
import numpy as np
R=Path(__file__).resolve().parents[1]
C=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/weight_spectral_dynamics')
def read(n):return list(csv.DictReader(open(R/'tables'/n)))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert json.load(open(R/'audit/independent_verification.json'))['status']=='PASS_BOUNDED_AUDIT'
late=read('late_interval.csv');summary=read('onset_sensitivity_summary.csv');tol=read('tolerance_onsets.csv');matrix=read('matrix_metrics.csv');mods=json.load(open(R/'config.json'))['modules']
statistics={}
for side in ['input','output']:
 a=[x for x in late if x['side']==side];angles=[float(x['pc1_angle_deg']) for x in a if x['pc1_identifiable']=='True'];dist=[float(x['top64_projection_distance']) for x in a];fraction=[float(x['s1_relative_change_symmetric'])*100 for x in a]
 statistics[side]=dict(identifiable_pc1=len(angles),pc1_angle_median=float(np.median(angles)) if angles else None,pc1_angle_min=min(angles) if angles else None,pc1_angle_max=max(angles) if angles else None,pc1_max_module=max((x for x in a if x['pc1_identifiable']=='True'),key=lambda x:float(x['pc1_angle_deg']))['module'] if angles else None,top64_distance_min=min(dist),top64_distance_median=float(np.median(dist)),top64_distance_max=max(dist),s1_change_percent_min=min(fraction),s1_change_percent_median=float(np.median(fraction)),s1_change_percent_max=max(fraction),onset_counts={metric:{key:sum(x['interpretation']==key for x in summary if x['side']==side and x['metric']==metric) for key in ['ALL_GRID_PASS','THRESHOLD_DEPENDENT','NO_GRID_ONSET']} for metric in ['s1','pc1_angle_deg','top64_projection_distance']})
(R/'tables/reading_statistics.json').write_text(json.dumps(statistics,indent=2)+'\n')
# Every module's illustrative middle-grid onset; full nine-grid matrix remains primary sensitivity source.
onsetrows=[]
for m in mods:
 x={'module':m}
 for side in ['input','output']:
  for metric,raw,rate in [('s1',.03,.01),('pc1_angle_deg',10,3),('top64_projection_distance',.1,.01)]:
   a=next(z for z in tol if z['module']==m and z['side']==side and z['metric']==metric and float(z['raw_tolerance'])==raw and float(z['per_B_tolerance'])==rate);x[f'{side}_{metric}_conditional_onset_B']=a['onset_training_B'] or 'NOT_ESTABLISHED'
 onsetrows.append(x)
with open(R/'tables/illustrative_grid_onsets.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(onsetrows[0]));w.writeheader();w.writerows(onsetrows)
I=statistics['input'];O=statistics['output'];decomp=json.load(open(R/'audit/collection_complete.json'));pair=json.load(open(R/'audit/comparison_complete.json'))
fmt=lambda x:f'{x:.4g}' if x is not None else 'NA'
cn=f'''# Dense权重谱动态：第一方向与前64维

本轮完成同一Dense轨迹12个可读checkpoint的全部57个独立二维权重，即684个矩阵状态。**权重幅度、第一方向、前64维子空间必须分开回答；不存在由最大奇异值变平直接推导方向收敛的关系。**以下为已核事实与有界AI解释，研究者接受和问题关闭仍为Unknown。

## 先看最后31→33B的实际变化

|指标|输入侧（右奇异空间）|输出侧（左奇异空间）|
|---|---|---|
|第一方向满足预定间隔要求的模块数|{I['identifiable_pc1']}/57|{O['identifiable_pc1']}/57|
|上述模块第一方向夹角，中位数；范围|{fmt(I['pc1_angle_median'])}°；{fmt(I['pc1_angle_min'])}–{fmt(I['pc1_angle_max'])}°|{fmt(O['pc1_angle_median'])}°；{fmt(O['pc1_angle_min'])}–{fmt(O['pc1_angle_max'])}°|
|前64维投影距离，中位数；范围|{fmt(I['top64_distance_median'])}；{fmt(I['top64_distance_min'])}–{fmt(I['top64_distance_max'])}|{fmt(O['top64_distance_median'])}；{fmt(O['top64_distance_min'])}–{fmt(O['top64_distance_max'])}|

全57模块的最大奇异值对称相对变化为{fmt(I['s1_change_percent_min'])}%–{fmt(I['s1_change_percent_max'])}%，中位{fmt(I['s1_change_percent_median'])}%。以上均是同一2B区间；其它区间必须同时看per_B列，不能按原始距离排名学习快慢。范围和中位数不替代逐模块结果，原值在[末区间表](tables/late_interval.csv)，全部相邻与距33B结果在[配对表](tables/pair_metrics.csv)。

## 两张主图

![权重幅度与第一方向](figures/figure1_weight_top1.png)

每行一个模块，所有57个矩阵均保留；每列为相邻实测区间，横轴标该区间右端训练B，间隔不相等。左图为s1对称相对变化百分比，分母sqrt(s1_a*s1_b)；中/右图为输入/输出第一方向符号不变夹角，单位度。灰色表示两端任一(s1−s2)/s1未达到预定5%单方向解读要求，不是零旋转。颜色只编码测量大小，无抽样误差条。该5%是保守的方向解释条件，不是数值上必然不可计算的证明。

![前64维输入和输出子空间](figures/figure2_weight_top64.png)

同样全部57模块和11相邻区间，左为输入、右为输出前64维归一化投影距离，范围0–1；等于sqrt(mean(sin²(64个主角度)))，不受子空间内部基向量旋转影响。它比较各点重新排序的前64空间，不追踪永久语义对象。64/65边界弱间隔在原表保留；接近数值误差时标无法分辨。没有文本样本或文档bootstrap，也没有独立训练重复区间。

## 何时趋稳：只给带容差的答案

没有科学依据选择一个唯一普适容差。批量前冻结三档原始变化阈值×三档每B变化阈值；全部九种组合都报告。条件起点是至少连续三个可测区间满足两条件、且一直保持到33B的最早实测起点；不是数学收敛时间，也不保证缺失checkpoint之间无反弹。

|对象|输入侧：九档都给起点/仅部分给起点/都不给起点|输出侧：九档都给起点/仅部分给起点/都不给起点|
|---|---|---|
'''
for metric,label in [('s1','最大奇异值幅度'),('pc1_angle_deg','可辨识第一方向'),('top64_projection_distance','前64维子空间')]:
 vals=[]
 for side in ['input','output']:
  a=statistics[side]['onset_counts'][metric];vals.append('/'.join(str(a[k]) for k in ['ALL_GRID_PASS','THRESHOLD_DEPENDENT','NO_GRID_ONSET']))
 cn+=f"|{label}|{vals[0]}|{vals[1]}|\n"
cn+='''
这些计数只是容差敏感性，不是模型收敛比例。每模块、每方向和每阈值的准确起点见[全部3078条容差结果](tables/tolerance_onsets.csv)和[敏感性汇总](tables/onset_sensitivity_summary.csv)；[中档示例表](tables/illustrative_grid_onsets.csv)仅方便定位，不能替代全部网格。对前64维，中档阈值是距离≤0.1且每B≤0.01；换阈值会改变起点，这是必须保留的认识边界。

## 对象、实际范围与限制

原生Dense约2.81亿参数，8层hidden1024；12个点为0.5/1/3/5/10/15/17/19/21/22.018691584/31/33B。全部AttentionQ/K/V/O、MLPgate/up/down及共享embedding/output权重均纳入；共享权重计一次，33个一维norm增益/点排除。每个W[输出,输入]不中心化分解W=U diag(s)Vᵀ，左右空间分开。共享矩阵按输出投影看左为词表、右为hidden，输入embedding使用转置方向。

原8个缺权重状态未恢复或插值。没有使用文本或旧表征/PCA/readout拟合，模型更新和前向均为0；本次没有使用GPU。全684缓存的哈希/维度/标量通过复核，全部末区间左右空间的114个投影距离由等价公式复核；真实早/晚Q权重与直接SVD/奇异方程交叉检查。完整独立SVD未对684个矩阵全部再跑，不能把这些检查夸为重复训练确认。

该研究只描述同一训练轨迹的原生参数坐标。坐标重参数化、头或通道的协同变化可改变权重方向而不产生相同幅度的功能变化；反之权重较稳也不证明语义或输出稳定。第一方向不隔离的模块保留不足，不能把灰色算成稳定或失稳。33B只是末端观察点。原表征实验、其protocol和数值没有被本扩展替换。

[协议](protocol_cn.md) · [实际执行与纠错](detailed_cn.md) · [资产/对象](assets_and_data_cn.md) · [数据与代码身份](artifact_manifest.json)。当前仍等研究者逐图讨论，不将这里的AI解释记成已确认机制。
'''
(C/'summary_cn.md').write_text(cn)
en=f'''# Dense native weight spectral dynamics

All57unique2Dweightmatrices were measured at12compatible saved states:684decompositions. Magnitude,first input/output directions and leading64subspaces are separate quantities. Scientific acceptance and question closure remain Unknown.

Late31-to33B:identifiable first directions {I['identifiable_pc1']}/57 modules;input median angle{fmt(I['pc1_angle_median'])}degrees(range{fmt(I['pc1_angle_min'])}–{fmt(I['pc1_angle_max'])}),output median{fmt(O['pc1_angle_median'])}(range{fmt(O['pc1_angle_min'])}–{fmt(O['pc1_angle_max'])}). Top64input projection distance median{fmt(I['top64_distance_median'])},range{fmt(I['top64_distance_min'])}–{fmt(I['top64_distance_max'])};output median{fmt(O['top64_distance_median'])},range{fmt(O['top64_distance_min'])}–{fmt(O['top64_distance_max'])}. Across57modules,s1symmetric relative change median{fmt(I['s1_change_percent_median'])}percent,range{fmt(I['s1_change_percent_min'])}–{fmt(I['s1_change_percent_max'])}. See tables/late_interval.csv,not a pooled convergence verdict.

![Magnitude and first directions](figures/figure1_weight_top1.png)

All57modules by11observed adjacent intervals;right-endpoint trainingB labels have unequal gaps. Percent s1change uses sqrt(s1_a*s1_b)denominator;angles are arccos absolute vector cosine,degrees. Gray means first vectors fail the predeclared5percent singular-gap guard,not zero motion. No sampling error bars:the object is a full saved weight matrix.

![Leading64spaces](figures/figure2_weight_top64.png)

Input/right and output/left projection distance is sqrt(mean(sin²principal_angles)),0–1. Internal basis rotations do not count as subspace drift;weak64/65boundaries and numerical identifiability are retained. Full pair distances and perB rates are in tables/pair_metrics.csv.

Convergence timing is not identified by a unique scientific tolerance. All nine predeclared raw-displacement×perB-rate combinations per metric/side/module remain in tables/tolerance_onsets.csv. A conditional onset requires at least three consecutive observed intervals satisfying both bounds through33B,with identifiable directions where applicable. This does not certify unobserved intervals or final convergence. tables/onset_sensitivity_summary.csv distinguishes all-grid-pass,threshold-dependent and no-grid onset. The illustrative middle-grid table is navigation only.

Weights are uncentered native W[out,in],not text activations. All8blocks Q/K/V/O and gate/up/down plus tied embedding/output are included;33one-dimensional norm gains per state are explicitly excluded. Tied output/input embedding is counted once and reverses mapping orientation when used as input lookup. No model forward,training,GPU,text split or old representation fit enters this new run. Eight missing-weight states remain missing. Same native281431040-parameter Dense trajectory0.5–33B;33B is not a convergence truth. Parameter movement does not establish behavior/semantic change or router utility. See detailed.md,protocol.md and artifact_manifest.json;researcher interpretation remains pending.
'''
(C/'summary.md').write_text(en)
dcn=f'''# W01实际执行记录

状态：有界权重分析完成，研究者逐图解释待讨论。原始表征protocol与冻结字节均保留；本轮新protocol记录权重对象与所有阈值。\n\n实际执行：本机CPU4线程，GPU0；684矩阵状态；权重分解耗时{decomp['seconds']:.1f}秒，跨checkpoint比较耗时{pair['seconds']:.1f}秒；57×23对×2侧={pair['paired_rows']}行配对结果；全谱{pair['spectrum_rows']}行留执行侧；容差{pair['tolerance_rows']}行。完整输入payload与内部token/step逐点核验，模型参数未更新、无forward。\n\n原计划/实际对照：全部12可读点完成；全部57唯一二维权重完成；左右第一方向和前64空间均独立测量；所有九档容差完成；8个缺权重点未执行；单方向间隔不足标UNIDENTIFIABLE而非强行追踪；没有新训练重复或功能测试。只复用已有checkpoint和模型身份，未复用表征统计或分类器。\n\n代码复用决定：沿用此前严格hash/计数及谱比较思想，适配新W的非中心化SVD；不把activation covariance当权重谱。每矩阵较小Gram为1024×1024，FP64 eigh给全部奇异值，另一侧仅恢复前65方向。测量代码与配置在正式分解前freeze；配对/绘图代码在其阶段前另存hash。一次绘图前表达修正增加不裁切的色阶上界与区分灰色含义，旧hash留在plot_freeze.previous；无数值或阈值改动。\n\n可信度：smoke含真实0.5B Q直接SVD与恒等/符号/等谱旋转/近简并例；所有684cache哈希、维度、s1/能量通过独立检查；所有114末区间左右空间距离经等价投影公式重建；33B末层Q的两个奇异方程残差通过；3078个条件起点从原pair表重新计算一致。未对684逐个重跑独立全SVD；无独立模型重复。\n\n没有文本采样，不能挪用原文档半集误差条或对权重条目bootstrap。第一方向5%间隔门槛是保守解释规则，不是数学上无法精确算出特征向量的声明。参数原坐标变化可能包含等效或协同重参数化，缺乏原生功能反事实。条件起点随容差变化而变化，不能包装成最终收敛时间。\n\n数值、具体模块和允许解释见summary_cn.md及tables；代码/来源/protocol/缓存identity由artifact_manifest与freeze拥有。没有改划分、挑正例、增补GPU或为了得到正结论选择阈值。\n'''
(C/'detailed_cn.md').write_text(dcn)
(C/'detailed.md').write_text(f'''# W01 execution record

Bounded CPU run complete;scientific acceptance Unknown. Decomposition{decomp['seconds']:.1f}seconds;pair comparison{pair['seconds']:.1f}seconds. Four threads,zero GPUs/forwards/modelupdates. 684module-states,2622left/right paired rows,700416spectrum rows retained execution-side,3078tolerance rows. All12readable states and57unique2Dmatrices completed;8missing states remain unmeasured;396one-dimensional norm tensors explicitly excluded. Left and right spaces are separate;no text panel/oldPCA/readout reused.

freeze.json owns initial code/config/protocol identity;comparison_freeze and plot_freeze own later-stage code. A pre-first-plot presentation adjustment adds non-clipping s1 colors and distinct missingness captions,with previous hash preserved;no data/metric/threshold change. Numerical smoke and audit/independent_verification.json record direct realQ SVD,all684hashes/shapes/scalars,114late paired projection checks,lateQ singular equations and all3078onset recomputations. Not all684were independently directly decomposed a second time. No independent training replicates or functional intervention exists.

Original representation protocol/results remain intact. New uncentered weight SVD adapts prior spectral-comparison ideas;activation covariance code was not substituted. Conditional tolerance onset is a descriptive terminal suffix,not final convergence;5percent PC1gap is a conservative interpretability guard,not a universal numerical theorem. Raw parameter movement may contain reparameterization with different functional meaning. See summary.md,full tables,assets_and_data.md and artifact_manifest.json. Researcher-facing Chinese detail is detailed_cn.md.
''')
for name in ['manifest.json','config.json','freeze.json','cache_index.json']:
 if name!='cache_index.json':shutil.copy2(R/name,C/name)
# Large bases and full 700416-row spectra stay execution-side.
for p in (R/'tables').iterdir():
 if p.name!='spectrum.csv':shutil.copy2(p,C/'tables'/p.name)
for p in (R/'scripts').glob('*.py'):shutil.copy2(p,C/'code'/p.name)
for p in (R/'figures').iterdir():shutil.copy2(p,C/'figures'/p.name)
for p in (R/'audit').glob('*.json'):shutil.copy2(p,C/'audit'/p.name)
artifact=dict(schema_version=1,experiment='W01_dense_weight_spectral_dynamics',task_state='COMPLETED_BOUNDED_CPU_WEIGHT_ANALYSIS',result_state='DESCRIPTIVE_MODULE_AND_TOLERANCE_SPECIFIC_DYNAMICS',scientific_acceptance='Unknown',question_closure='Unknown',execution_root=str(R),input_asset='checkpoint_family_dense_spectral_dynamics_20261101',output_asset='analysis_dense_weight_spectral_dynamics_20261101',counts=dict(checkpoints=12,unique_matrices=57,matrix_states=684,paired_rows=2622,tolerance_rows=3078,missing_payload_states=8),resources=dict(cpu_threads=4,gpus=0,new_forwards=0,LM_updates=0),reading_statistics=statistics,cache_index=dict(path=str(R/'cache_index.json'),sha256=sha(R/'cache_index.json')),canonical_files=[dict(path=str(p.relative_to(C)),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(C.rglob('*')) if p.is_file() and p.name!='artifact_manifest.json'],publication='LOCAL_ONLY_NOT_COMMITTED_OR_PUSHED',completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(C/'artifact_manifest.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n');(R/'artifact_manifest.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(statistics,indent=2))
