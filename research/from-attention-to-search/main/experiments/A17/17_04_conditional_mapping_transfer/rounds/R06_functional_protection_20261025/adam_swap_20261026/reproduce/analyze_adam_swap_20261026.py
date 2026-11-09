"""CPU-only analysis of frozen moment-swap readouts. No model/data loading."""
from pathlib import Path
import csv,json,statistics as st,hashlib,collections,math,shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
E=Path(__file__).resolve().parents[1];O=E/'analysis/adam_swap_20261026';V=O/'provenance';T=O/'tables'
own=json.load(open(V/'ownership.json'));R=Path(own['round']);A=Path(own['anchor'])
def read(n):return list(csv.DictReader((T/n).open()))
def write(n,rows):
 with (T/n).open('w',newline='') as f:
  w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
def out(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
r=read('candidate_DEV_effects_72.csv');geo=read('candidate_geometry_36.csv');items=read('per_item_DEV_effects_4608.csv');noise=read('baseline_noop_noise_12.csv');replay=read('native_firstbatch_replay.csv')
assert len(r)==72 and len(geo)==36 and len(items)==4608
key=lambda x:(int(x['seed']),int(x['batch']),x['group'],x['cell'])
d={key(x):x for x in r};assert len(d)==72
num=lambda z,b,g,c:float(d[z,b,g,c]['CE_change'])
contrasts=[];matrix=[]
for z in [29,43,71]:
 for b in [1,2,3]:
  row={'seed':z,'batch':b,'original_order_index':119+b}
  for g in ['old_DEV','new_DEV']:
   vals={c:num(z,b,g,c) for c in ['UU','UF','FU','FF']};tau=max(float(d[z,b,g,c]['noise_tau']) for c in vals)
   for c,v in vals.items():row[f'{g}_{c}_delta_CE']=v
   cs={'moments_F_minus_U_at_Utheta':vals['UF']-vals['UU'],'moments_F_minus_U_at_Ftheta':vals['FF']-vals['FU'],'theta_F_minus_U_at_Umoments':vals['FU']-vals['UU'],'theta_F_minus_U_at_Fmoments':vals['FF']-vals['UF'],'interaction_DiD':vals['FF']-vals['FU']-vals['UF']+vals['UU']}
   for label,val in cs.items():
    threshold=tau*(4 if label=='interaction_DiD' else 2)
    contrasts.append({'seed':z,'batch':b,'group':g,'contrast':label,'delta_of_delta_CE':val,'precision_threshold':threshold,'resolved':abs(val)>threshold,'sign':1 if val>threshold else (-1 if val< -threshold else 0)})
  matrix.append(row)
write('four_cells_by_seed_batch_9.csv',matrix);write('paired_effects_and_interactions_90.csv',contrasts)
summary=[];seedmeans=[]
for g in ['old_DEV','new_DEV']:
 for c in ['UU','UF','FU','FF']:
  vals=[num(z,b,g,c) for z in [29,43,71] for b in [1,2,3]]
  summary.append({'group':g,'cell':c,'n_seed_batch_contexts':9,'mean_delta_CE':st.mean(vals),'min_delta_CE':min(vals),'max_delta_CE':max(vals),'negative':sum(v<0 for v in vals),'positive':sum(v>0 for v in vals)})
  for z in [29,43,71]:
   v=[num(z,b,g,c) for b in [1,2,3]]
   seedmeans.append({'seed':z,'group':g,'cell':c,'n_batches':3,'mean_delta_CE':st.mean(v),'min_delta_CE':min(v),'max_delta_CE':max(v)})
write('four_cell_means_8.csv',summary);write('seed_cell_means_24.csv',seedmeans)
stability=[]
for g in ['old_DEV','new_DEV']:
 for label in dict.fromkeys(x['contrast'] for x in contrasts):
  rows=[x for x in contrasts if x['group']==g and x['contrast']==label];v=[x['delta_of_delta_CE'] for x in rows]
  stability.append({'group':g,'contrast':label,'mean_delta_of_delta_CE':st.mean(v),'min':min(v),'max':max(v),'positive':sum(x['sign']==1 for x in rows),'negative':sum(x['sign']==-1 for x in rows),'unresolved':sum(x['sign']==0 for x in rows),'all9_same_resolved_direction':len(set(x['sign'] for x in rows))==1 and rows[0]['sign']!=0})
write('contrast_stability_10.csv',stability)
# Independent per-item and context audits. No model reloads.
errs=[]
for k,row in d.items():
 rr=[x for x in items if key(x)==k];assert len(rr)==64 and len({x['record_id'] for x in rr})==64
 for field in ['before_CE','after_CE','CE_change']:
  err=abs(st.mean(float(x[field]) for x in rr)-float(row[field]));errs.append(err);assert err<1e-12
 for phase in ['before','after']:
  acc=100*sum(int(x[phase+'_correct']) for x in rr)/64
  assert acc==float(row[phase+'_accuracy_pct'])
for z in [29,43,71]:
 for b in [1,2,3]:
  for theta in ['U','F']:
   gg=[x for x in geo if x['seed']==str(z) and x['batch']==str(b) and x['theta_origin']==theta]
   assert len(gg)==2 and len(set(x['gradient_hash_by_name'] for x in gg))==1
   assert len(set(x['raw_gradient_norm'] for x in gg))==1 and len(set(x['gradient_clip_coefficient'] for x in gg))==1
   assert all(x['optimizer_step_before']=='120' and x['optimizer_step_after']=='121' and x['F_projection_applied']=='False' for x in gg)
assert all(x['PASS']=='True' for x in replay)
assert sum(x['sequences'] for x in json.load(open(O/'sequence_calls.json')))==10320
noopmax=max(float(x['noop_span']) for x in noise);taumax=max(float(x['noise_tau']) for x in noise)
audit={'status':'PASS','aggregate_rows':72,'per_item_rows':4608,'candidates':36,'contexts':9,'independent_continuation_seeds':3,'shared_old_checkpoint':True,'max_per_item_aggregation_error':max(errs),'all_correctness_denominators':64,'same_theta_batch_gradient_hash_equal_across_moment_donors':True,'all_native_replay_checks':24,'native_replay_max_CE_error':json.load(open(V/'native_replay_gate.json'))['max_CE_error'],'max_noop_CE_span':noopmax,'max_noise_tau':taumax,'all90_contrasts_resolved_above_precision':all(x['resolved'] for x in contrasts),'precision_is_not_statistical_uncertainty':True,'sequence_forwards_count_independent_sum':10320,'no_extra_forward_in_analysis':True,'raw_gradient_norm_range':[min(float(x['raw_gradient_norm']) for x in geo),max(float(x['raw_gradient_norm']) for x in geo)],'clip_coefficient_range':[min(float(x['gradient_clip_coefficient']) for x in geo),max(float(x['gradient_clip_coefficient']) for x in geo)],'actual_displacement_norm_range':[min(float(x['final_actual_displacement_norm']) for x in geo),max(float(x['final_actual_displacement_norm']) for x in geo)]}
out(V/'independent_analysis_audit.json',audit)
# One figure with four panels: rows parameter source, columns moment source.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42})
fig,axes=plt.subplots(2,2,figsize=(11,7.2),sharex=True,sharey=True)
contexts=[(z,b) for z in [29,43,71] for b in [1,2,3]];x=list(range(9))
for i,theta in enumerate(['U','F']):
 for j,mom in enumerate(['U','F']):
  ax=axes[i,j];c=theta+mom
  for g,color,marker,off,label in [('old_DEV','#0072B2','o',-.12,'Old DEV'),('new_DEV','#D55E00','s',.12,'New DEV')]:
   vals=[num(z,b,g,c) for z,b in contexts];xx=[k+off for k in x]
   ax.vlines(xx,0,vals,color=color,alpha=.42,lw=1.5);ax.scatter(xx,vals,c=color,marker=marker,s=30,label=label,zorder=3)
  ax.axhline(0,c='#555555',lw=.8);ax.axvline(2.5,c='#cccccc',ls=':',lw=.8);ax.axvline(5.5,c='#cccccc',ls=':',lw=.8)
  ax.set_title(f'Parameters: {theta}   |   Adam moments: {mom}',fontsize=11,pad=9)
  ax.set_xticks(x,[f'{z}\n{b}' for z,b in contexts]);ax.grid(axis='y',alpha=.18);ax.set_ylim(-.235,.215)
  ax.spines[['top','right']].set_visible(False)
  if j==0:ax.set_ylabel('CE change after one step (nats / answer)')
  if i==1:ax.set_xlabel('Continuation seed / batch')
handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',ncol=2,frameon=False,bbox_to_anchor=(.5,1.0))
fig.tight_layout(rect=[0,0,1,.95],h_pad=2)
for suffix in ['svg','pdf','png']:fig.savefig(O/'figures'/f'four_cell_CE_change.{suffix}',dpi=320,bbox_inches='tight')
plt.close(fig)
# Concise Chinese narrative with the full three-seed by three-batch effects in appendix.
mdtable='| 参数来源 | Adam 累积状态来源 | 旧任务单步 CE 变化 | 新任务单步 CE 变化 |\n|---|---|---:|---:|\n'
for c in ['UU','UF','FU','FF']:
 vals={g:st.mean(num(z,b,g,c) for z,b in contexts) for g in ['old_DEV','new_DEV']}
 mdtable+=f"| {c[0]} | {c[1]} | {vals['old_DEV']:+.6f} | {vals['new_DEV']:+.6f} |\n"
main='''# 第120步诊断：Adam 累积状态参与差异，作用取决于当前参数

**判断：当前证据更支持 Adam 累积状态确实参与旧任务的不利更新，同时存在参数与 Adam 状态的交互；不足以把长期劣势归结为某一个因素。** 固定 F 参数，换用 U 的 Adam 状态，三个种子、每种子三批的旧损失变化全部更有利。固定同一 Adam 状态，更换参数的影响则不稳定。

## 问题与对照

A17 是带模式标记的两套可兼容列表规则。本轮只检查旧∶新监督为1∶9的第120步：普通更新为何从 U、F 两条历史轨迹出发产生不同效果？U 指历史上普通更新；F 指历史上按旧探针梯度投影。**本轮四格全部只执行一次普通 Adam 更新，不应用 F。**

每个种子交换两份参数与两份 Adam 累积状态。后者包括梯度的一阶矩（近期梯度的加权平均）与二阶矩（近期梯度平方的加权平均）。三个种子各锁定三批，每批36条新题＋4条有监督旧题，仍占72槽位、损失分母72。每一批均独立从120步出发，更新到121步后恢复。评价固定独立旧、新 DEV 各64题；DEV 是未参与这次更新的开发评价集。

## 关键结果

交叉熵 CE 衡量模型给正确答案的概率，单位为自然对数单位／答案。这里报告“更新后减更新前”，**负值更有利，正值更不利**。下表对三个种子各三批等权平均，只作概览，不是九个独立模型，也不是置信区间。

'''+mdtable+'''
- **Adam 状态具有稳定的局部作用。** 固定 F 参数，把 F 状态换为 U 状态，旧 CE 变化在9/9个种子×批次中更有利，平均少上升0.130592；其中7次实际下降、2次仍上升。因此“更有利”不等于全部保旧成功。新 CE 在其中6次更不利、3次更有利，平均更不利0.005384，存在取舍。这一平均新任务成本并非三种子一致：29号平均更不利，43、71号平均更有利。
- **作用依赖参数。** 固定 U 参数，把 U 状态换为 F 状态，旧 CE 在8/9次更不利，但71号种子的第三批方向反转；新 CE 则9/9次更有利。相同更换在 F 参数下的旧 CE 效应更大，并且交互差值在29、71号种子为正、43号为负（三批各自同号）。不能当成统一、可加的历史贡献。
- **参数单独解释不足。** 固定 U 状态，换成 F 参数，旧 CE 变化为5次更有利、4次更不利；固定 F 状态则为2次更有利、7次更不利。“F 的参数本身总让普通更新更伤旧任务”受到削弱。

## 已排除什么，尚未区分什么

六个原生 U＋U、F＋F 的第一批均复放通过：与上一轮普通 d4 的旧 DEV、旧 TRAIN 探针、新 TRAIN 批次损失变化完全一致。相同参数与批次下，交换 Adam 前的原梯度哈希和裁剪系数一致；比较的是最终写回的真实位移。故该局部差异不能只由当批样本或原梯度不同解释。无操作重复 CE 差为0，效应超过事前精度界；这不是统计显著性检验。

**当前支持：Adam 累积状态参与，并受参数状态调节。削弱：只有参数位置重要、或 Adam 状态在任何参数下有固定单向作用。仍未知：一阶矩与二阶矩各自的作用，以及这些单步效应对240步终点差距贡献多少。** 交换产生训练中未经历的组合；这测量当前敏感性，不是训练历史的完整因果分解，不能称为长期兼容学习改进。基线损失在不同参数间本就不同，CE变化比较也不抹去这一点。

## 执行与唯一下一步建议

完成36个独立单步候选，前向10320／12000条；未读 TEST、未完整续训、未应用 F、未新增资源、未保存候选终点，六份原检查点哈希未变。**AI建议（未执行）：** 在相同六状态和三批上分别交换一阶矩、二阶矩，辨别累积方向与自适应缩放各自参与了什么。不要据此预言长期训练收益。

[四格图与图注](figures_cn.md) · [逐种子逐批、复放及数值附录](appendix_cn.md) · [冻结协议](protocol_cn.md) · [证据清单](artifact_manifest.md)
'''
# Verify factual count embedded above.
assert sum(num(z,b,'old_DEV','FU')<0 for z,b in contexts)==7
(R/'one_page_cn.md').write_text(main)
(R/'summary_cn.md').write_text(main)
cncap='''# 四格对照图

![第120步四格对照](figures/four_cell_CE_change.png)

**问题：** 同一当前参数下，换一份 Adam 累积状态是否改变普通更新对旧／新任务的影响？

**观察：** 每行固定参数来源，每列固定 Adam 来源；蓝圆为旧 DEV、橙方为新 DEV，纵轴是单步交叉熵变化，负数更有利。横轴上行29／43／71是续训顺序种子，下行1／2／3是固定训练批次；所有面板同尺度，点各自独立，竖线仅连接零线与点，没有训练轨迹连线。

**更新判断：** F 参数这一行中，U Adam 比 F Adam 的旧 CE 变化9/9次更有利；U 参数这一行中，反向更换的旧效应8/9同向、1次反转，且交互大小和符号依种子而变。Adam 累积状态参与，不能忽略参数交互。

**不能推出：** 新损失常出现反向取舍；九个种子×批次不是九个独立模型，三种子共用旧模型，图中没有跨模型置信区间。只读出64旧＋64新固定 DEV，不代表完整800题面板或TEST；交换不是完整历史因果分解，也未评价长期续训。

来源：执行侧 `tables/candidate_DEV_effects_72.csv`，同名文件随交付；图只用原始逐批变化，不平滑、不挑选检查点、不合并旧新得分。数值精度见 `reproduce/independent_analysis_audit.json`。另交SVG与PDF矢量图和320 dpi PNG。
'''
(R/'figures_cn.md').write_text(cncap)
# Detailed readable appendix, including every seed-batch primary value and every contrast.
appendix='''# 逐种子逐批与核验附录

## 对象、分母与成本

仅使用三个续训顺序种子的 U1∶9、F1∶9 第120步完整状态。三种子共用同一旧任务模型，不是独立预训练重复。四个6,291,456参数的完整矩阵为最后一层（索引27）Q/K/V/O；Q是查询、K是键、V是值、O是注意力输出投影。本轮无低秩训练约束，也无 F 投影。AdamW 学习率0.0001，一阶／二阶衰减率0.9／0.999，数值稳定项1e−8，权重衰减0，最大梯度范数1，FP32实际写回；步数120→121，偏差修正一致。

每批72输入槽位：36新＋36旧，其中4旧非零监督，其余旧损失乘0；损失为40个有效答案loss之和除72，而非除40。三批来自原记录索引120、121、122，不连做三步。36个候选对应4格×3种子×3批；批次不是独立训练种子。复用上一轮旧DEV64不变；本轮新DEV64是在当前结果前锁定的同列表同口令模式二配对题。上一轮的“新题”36条来自TRAIN，只用于原生复放，未冒充独立DEV。

训练旧4题（参与普通更新）、原保护旧TRAIN探针64题（本轮只在复放中评分）、独立旧DEV64题（只测量）是三种不同对象。独立旧DEV梯度仅用于内积测量，不参与更新方向或样本选择。新DEV同样不参与更新。答案为原缓存单词单token，CE以完整词表计算正确token的负对数概率；准确率以完整词表最大logit是否为目标计算，非三词内限选。

## 逐种子逐批主要结果

CE为自然对数单位／答案，表中均是更新后−更新前。UU＝U参数＋U Adam，UF＝U参数＋F Adam，FU＝F参数＋U Adam，FF＝F参数＋F Adam。未报告的精度位保留在CSV。

| 种子 | 批次 | UU旧 | UF旧 | FU旧 | FF旧 | UU新 | UF新 | FU新 | FF新 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
'''
for z,b in contexts:
 appendix+=f'| {z} | {b} | '+' | '.join(f'{num(z,b,g,c):+.6f}' for g in ['old_DEV','new_DEV'] for c in ['UU','UF','FU','FF'])+' |\n'
appendix+='''
## 固定另一因素后的差值

定义每格的Δ为该格单步CE变化。固定U参数的矩状态效应＝ΔUF−ΔUU；固定F参数＝ΔFF−ΔFU。固定U Adam的参数效应＝ΔFU−ΔUU；固定F Adam＝ΔFF−ΔUF。所有差值均为“F来源减U来源”，正数表示更不利。交互差值＝ΔFF−ΔFU−ΔUF＋ΔUU；它比较同一矩状态交换在两份参数下是否有相同作用，不是长期因果归因比例。

| 种子 | 批次 | 旧：矩效应@U参数 | 旧：矩效应@F参数 | 旧：参数效应@U矩 | 旧：参数效应@F矩 | 旧：交互 | 新：交互 |
|---|---|---:|---:|---:|---:|---:|---:|
'''
for z,b in contexts:
 vals=[x['delta_of_delta_CE'] for x in contrasts if x['seed']==z and x['batch']==b and x['group']=='old_DEV']
 newi=next(x['delta_of_delta_CE'] for x in contrasts if x['seed']==z and x['batch']==b and x['group']=='new_DEV' and x['contrast']=='interaction_DiD')
 appendix+=f'| {z} | {b} | '+' | '.join(f'{v:+.6f}' for v in vals+[newi])+' |\n'
appendix+='''
全部新任务简单效应见 `tables/paired_effects_and_interactions_90.csv`，包括每项事前精度阈值；每格的更新前后CE、准确率与旧正确答案相对新规则答案的logit差见 `candidate_DEV_effects_72.csv`。参数跨来源前后基线不同；这里没有将不同起点说成同一位置的能力变化。

## 原生第一批复放

先完成全部六个原生UU／FF第一批，再运行混合状态。对照上一轮**未经过F投影的普通d4**，不对照过滤后的F4。旧DEV、原保护旧TRAIN探针64、新TRAIN36的更新前／后／变化全部一致（最大CE差0），位移范数检查也通过。共24项通过；复放逐项原数、容差见 `native_firstbatch_replay.csv`，门槛回执见 `reproduce/native_replay_gate.json`。因此没有因当前新DEV扩展而改变原生旧DEV复放对象。

## 名称映射与恢复

原检查点未保存显式参数名列表。核对原生产代码冻结哈希后，用原代码构造优化器，并以当前参数对象身份解析保存ID对应的Q/K/V/O名称；四矩阵、形状、类型、分组、全部步数120、超参数逐项核验。K和V同形状，不能靠形状互认。本轮按该已核验名称映射复制一阶矩exp_avg、二阶矩exp_avg_sq，逐张量哈希确认供体；接收方step和组设置保持。映射和每份矩哈希见 `reproduce/named_mapping_and_inputs.json`，36候选供体身份见 `tables/moment_source_identity_36.csv`。

每个候选恢复同一来源参数、完整Adam状态和随机状态；在该批上联合计算36新＋4旧的梯度，裁剪后执行一次Adam；未把两份Adam位移相加。测量最后写回后的位移，再恢复起点和Adam哈希。相同参数／批次、不同矩来源的更新前梯度逐名哈希完全相同。原始梯度范数、裁剪系数、最终位移范数、实际位移与固定旧DEV梯度内积均在 `candidate_geometry_36.csv`；内积的一阶预测不代替实际CE测量。

## 数值、覆盖和不确定性

'''
appendix+=f"两次无操作重复最大CE差 {noopmax:g}；最大事前数值容差τ为{taumax:.10g}。τ取无操作跨度、1e−8×(1+基线CE)、旧DEV有梯度／无梯度前向差的最大值；配对差阈值2τ，交互4τ。90个简单／交互差值均超过对应精度界，**不等于跨种子的统计显著性**。逐题重新聚合与主表最大误差{max(errs):.3g}，每格每任务分母64，没有按正确率选题。\n\n"
appendix+=f"原始梯度范数范围{audit['raw_gradient_norm_range']}，裁剪系数范围{audit['clip_coefficient_range']}，实际位移范数范围{audit['actual_displacement_norm_range']}。不同矩来源可能同时改变方向和长度；本轮未把Adam作用进一步分解为二者。\n\n"
appendix+='''10320条额外序列前向＝1536条重复DEV基线＋384条固定旧DEV梯度＋2592条候选训练槽位＋4608条候选后DEV＋1200条原生复放额外TRAIN读出。预算上限12000，余1680未使用。已完成全部36候选和六原生复放；无缺失分支，不扩展检查点。只使用原有H100 MIG资源，无新作业、无完整续训、无TEST，无候选终点保存。六份原检查点执行前后SHA256相同，冻结代码／配置／顺序／协议未变，非更新模型参数字节校验通过。见 `reproduce/original_assets_immutable.json` 与 `receipt.json`。

## 假设更新与唯一建议

A（Adam参与）得到局部支持：F参数下9/9同向，U参数下8/9，存在一批反向，不能声称全域单调。B（仅参数主导）受到削弱：固定U Adam的参数效应5负4正。C（交互）得到局部支持：旧交互在29／71号为正，43号为负，幅度不能用一个统一系数代表。D（采样依赖）必须保留：U参数下矩效应有71号第三批反转，部分参数效应也换批反转。E（旧新取舍）存在：F参数由F矩换U矩时旧9/9改善，但新6/9更不利、3/9更有利；不能称为稳定兼容收益。

观测：上述CE和配对差值。解释：Adam的累积状态改变了当前普通更新的局部效用，参数状态调节其效果。待验证：一阶矩还是二阶矩更重要，以及长期终点差异中各部分贡献。下一步仅建议拆开交换两类矩（未执行）；不增加训练或把本轮写成解决方案。
'''
(R/'appendix_cn.md').write_text(appendix)
english='''# R06 step120 parameter × Adam-moment exchange

**Bounded result:** accumulated Adam state contributes to the local old-task disadvantage, with parameter-dependent effects. This is not a causal decomposition of the full training history.

A17 contains two compatible, mode-conditioned list rules. At the saved step120 of U/F 1:9 continuations (seeds29/43/71), we crossed U/F parameters with U/F named Adam first/second moments. Every cell used three prespecified TRAIN batches independently from step120:36new+4activeold,72slots,denominator72; one ordinary Adam update, no F projection. We evaluated64fixed old DEV and64paired new DEV items before/after. Three continuation orders share one old model.

'''+mdtable+'''
Table: equal mean of9seed-batch contexts; CE change is after−before in nats/answer, negative is favorable. No confidence intervals implied.

At fixed F parameters, replacing F moments with U moments improves old CE change in9/9contexts (mean0.130592), although2updates still increase old CE. New CE change worsens in6/9 (mean0.005384 cost), improves in3/9. At U parameters, F rather than U moments worsens old CE change8/9 but improves new CE9/9. At fixed U moments, the F−U parameter effect has5favorable/4unfavorable old outcomes; at F moments,2/7. Old interaction differences are positive for all batches of seeds29/71 and negative for all batches of43. A universal additive attribution is unsupported.

All6native first batches exactly reproduced the previous unprojected d4 CE readouts before hybrids. Full name mapping is reconstructed from verified frozen producer code and actual parameter object identities because original optimizer metadata lacks explicit parameter names. We exchanged only exp_avg/exp_avg_sq, retainingstep120/settings, verifying shape/name/group/moment hashes. Same-parameter/batch raw gradients and clipping coefficients match across moment donors. No-op CE span0; all contrasts exceed prespecified numerical precision bounds, which are not statistical significance.

Completed36independent temporary steps,10320/12000sequence forwards, all6original checkpoint hashes unchanged. No TEST, F projection, full continuation, new allocation or candidate checkpoint save. Main new DEV64 is a locked extension using old DEV pairs; previous new TRAIN36 remains replay-only. Parameter/moment hybrid states may not occur naturally in training; one-step effects do not establish long-term cause or benefit. First versus second moments and direction versus scale contributions remain unresolved. AI suggestion only: separate first/second-moment exchange at the same states/batches; not executed.

[Chinese one-page](one_page_cn.md), [all-seed/all-batch appendix](appendix_cn.md), [frozen protocol](protocol.md), [figure](figures_cn.md).
'''
# English artifact must not silently contain a Chinese table header.
english=english.replace('参数来源','Parameter source').replace('Adam 累积状态来源','Adam moment source').replace('旧任务单步 CE 变化','Old one-step CE change').replace('新任务单步 CE 变化','New one-step CE change')
(R/'summary.md').write_text(english)
for sub in ['tables','figures','reproduce']:(R/sub).mkdir(exist_ok=True)
for f in T.glob('*.csv'):
 if not f.name.startswith('per_item_'):shutil.copy2(f,R/'tables'/f.name)
for f in (O/'figures').iterdir():shutil.copy2(f,R/'figures'/f.name)
for f in V.glob('*.json'):shutil.copy2(f,R/'reproduce'/f.name)
shutil.copy2(O/'receipt.json',R/'reproduce/receipt.json');shutil.copy2(O/'sequence_calls.json',R/'reproduce/sequence_calls.json')
for f in [Path(__file__),E/'ops/adam_swap_20261026.py',E/'ops/local_dynamics_20261026.py',E/'source/engine.py',E/'source/retention_r05_v1.py',E/'source/entry.py',E/'config/frozen.json']:
 shutil.copy2(f,R/'reproduce'/f.name)
(R/'reproduce/run.sh').write_text('''#!/usr/bin/env bash
set -euo pipefail
# Model runtime reproduces a separate, explicitly bounded rerun only; completed worker refuses overwrite.
# This delivery does NOT rerun GPU work. CPU-only figure/table reconstruction:
python /data/250010109/MoE_Router/experiments/20261025_a17_functional_protection/ops/analyze_adam_swap_20261026.py
''')
print(json.dumps(audit,indent=2));print('Delivered narratives, tables and one four-cell figure:',R)
