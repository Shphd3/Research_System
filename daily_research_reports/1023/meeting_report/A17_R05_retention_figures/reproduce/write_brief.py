from pathlib import Path
import csv,json
F=Path(__file__).resolve().parent;S=Path('/data/250010109/Research_System');M=S/'daily_research_reports/1023/meeting_report';D=M/'A17_R05_retention_figures';C=S/'Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023'
def rows(p):return list(csv.DictReader(open(p)))
def table(head,body):return '| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in body)
a=rows(D/'tables/table1_main_experiment_21.csv');b=rows(D/'tables/table2_residual_interventions_9.csv')
t1=table(['顺序','方法','旧准确率（%）','新准确率（%）','新学习达标','较U的旧准确率变化（百分点）'],[[r['training_order'],r['method'],f"{float(r['old_accuracy_pct']):.3f}",f"{float(r['new_accuracy_pct']):.3f}",'是' if r['new_learning_qualified']=='True' else '否',f"{float(r['old_minus_U_pp']):+.3f}"] for r in a])
def v(r,k,u,signed=False):
 m,lo,hi=[float(r[f'{k}_{z}_{u}']) for z in ['mean','min','max']];fmt=lambda x:f'{x:+.3f}' if signed else f'{x:.3f}';return fmt(m)+(f' ［{fmt(lo)}, {fmt(hi)}］' if r['condition']=='random' and lo!=hi else '')
labels={'endpoint':'原终点','target':'靶向削弱','random':'随机对照'}
t2=table(['顺序','条件','旧准确率（%）','新准确率（%）','旧变化（百分点）','新变化（百分点）'],[[r['training_order'],labels[r['condition']],v(r,'old_accuracy','pct'),v(r,'new_accuracy','pct'),v(r,'old_change','pp',True),v(r,'new_change','pp',True)] for r in b])
(D/'tables/table1_main_experiment_cn.md').write_text('''# 表1：七种更新方法的1200步主终点

'''+t1+'''

每行旧、新任务各800题，按全词表预测计算准确率。新学习达标要求“口令×评价面板”的四格各200题均≥95%；它只表示新任务学会，不表示旧能力保持成功。最后一列为该方法减同顺序U，单位百分点。

U统一更新；UL整体更新乘0.1；US整体更新按0.1→0.01调度衰减；TC固定衰减原前16方向；TS对原前16方向调度衰减；RS对随机16方向采用同一调度；LS对最小16奇异方向采用同一调度。TC的固定系数为0.1。这里的衰减作用于优化器提出的参数位移。

**如何向导师解释：** TS三种顺序均学会新任务，但相对U的旧准确率变化为0、0、−0.375个百分点，没有得到预期保持收益。保留其他五个对照，是为了核对整体减速、随机方向和小奇异方向是否产生不同权衡。例如US71的旧准确率为4.5%，但新学习未达标，不能把它作为兼顾新旧的成功例子。

来源：[A阶段终点原表]('''+str(C/'a_stage_audit_tables/endpoint_21.csv')+''')。三个顺序共用一个旧模型，不是三个独立旧模型。
''')
(D/'tables/table2_residual_interventions_cn.md').write_text('''# 表2：保护组TS的冻结残差干预

'''+t2+'''

“变化”均相对同顺序原终点。随机对照行显示五次固定方向干预的均值，方括号为五次最小值和最大值；五次相同则只列一个值。范围不是置信区间。每个条件旧、新任务各800题。

**如何向导师解释：** 靶向削弱使旧准确率提高22.75—45.5个百分点，但新准确率同时降低22.25—40.625个百分点；匹配随机对照基本留在原终点附近。这个结果表明残差更新含有影响两项任务的特定结构，恢复旧表现并不等于同时保住新表现。

干预对象是新增ΔR，而非全部R。先从ΔR选16个奇异分量，再减回其C投影，实际构造秩为32；随机对照匹配同秩和每张矩阵的实际改动长度。R1—R5对应方向种子2701—2705，不是训练顺序。完整单次值见[主图2数据](../plot_data/figure2_TS_21.csv)。

来源：[66条件原表]('''+str(C/'A_residual_spectral_20261023/tables/intervention_behavior_66.csv')+''')及[实际秩/范数核验]('''+str(C/'A_residual_spectral_20261023/tables/actual_norm_rank_matches_120.csv')+''')。同类U结果保留在原记录，本表聚焦TS保护失败的解释。
''')
(M/'meeting_brief_A17_R05_retention_cn.md').write_text('''# 参数方向保护与旧能力保持：结论配图稿

## 目的与本轮检验

我们希望在进一步学习差异时，保留已经掌握、仍有用的计算。本轮先用两条可由可见模式区分的相反规则，检验参数方向保护是否能在学会新规则时保持旧能力。旧模式中甲选首词、乙选末词，新模式反过来。

模型为Qwen3-0.6B Base。本轮从学完旧任务的同一检查点出发，只继续学习新任务，更新末层注意力的查询、键、值、输出四张矩阵，共1200步。把每张完整旧权重的前16个奇异秩一系数记作候选C，其余记作R；本轮实际干预是衰减优化器提出的C方向参数更新。C目前仍是候选分量，跨输入复用价值尚未确认。

正文只讲下面两条结论。表1完整保留七种方法作为对照核对；表2提供残差干预数值；谱变化留作备用。

## 结论1：保护选定参数方向，未实现旧能力保持

![主图1](A17_R05_retention_figures/figures/figure1_protection_and_retention.png)

**怎么看。** U是不保护组，TS是衰减原前16方向更新的保护组。第一栏显示C的终点净位移；接下来两栏用全范围和局部放大显示同一组旧准确率，最后一栏显示新准确率。横轴29、43、71是新任务训练顺序，三者共用同一个旧模型。旧、新评价各800题，按全词表预测计算准确率。

**关键差别。** TS的C净位移为初始C长度的0.0171%—0.0366%，U为0.1792%—0.4996%，约相差一个数量级。新学习均达标；TS旧准确率为0%、0%、0.5%，U为0%、0%、0.875%。局部放大用于看清接近零的数值，不代表获得了较大的保持效果。

**为什么重要。** 所选系数的变化确实被压低，但旧行为没有改善。本轮“大奇异方向选择＋更新衰减”的方式没有实现预期功能保持，结果边界止于这一具体配置。

图注：净位移为终点减起点的参数长度，不是逐步累计更新量；归一化分母是四张矩阵初始C的联合Frobenius长度22.6734065。Frobenius长度是全部元素平方和开根号。详细对照见[文字表1](A17_R05_retention_figures/tables/table1_main_experiment_cn.md)；[SVG](A17_R05_retention_figures/figures/figure1_protection_and_retention.svg) · [PDF](A17_R05_retention_figures/figures/figure1_protection_and_retention.pdf) · [CSV](A17_R05_retention_figures/plot_data/figure1_6.csv)。

## 结论2：残差更新也改变旧任务输出

![主图2](A17_R05_retention_figures/figures/figure2_residual_tradeoff.png)

**怎么看。** 这张图聚焦保护组TS。横轴是新准确率，纵轴是旧准确率，右上方代表两项同时较好。每栏保留原终点、靶向削弱和五个匹配随机对照。局部图放大原终点附近的随机结果；R1—R5重合时合并标注，不挪动数据点。它们是冻结模型后的干预结果，不是训练轨迹。

**关键差别。** 靶向削弱使旧准确率从0%、0%、0.5%提高到45.5%、37.375%、23.25%；新准确率同时从100%、99.875%、98.625%降到59.375%、67.125%、76.375%。随机干预的结果仍接近原终点。表2保留随机均值与五次范围，见[文字表2](A17_R05_retention_figures/tables/table2_residual_interventions_cn.md)。

**为什么重要。** 剩余更新没有只服务新任务；其中的特定分量也会影响旧任务输出。削弱这些分量比等量随机扰动更能恢复旧表现，但代价是损失新表现，因此还没有得到兼顾新旧的保护方法。

另一个直接支持来自固定旧输入的局部测量：第16步，ΔR导致的投影输出变化为原输出长度的9.53%—22.04%，ΔC为0.0040%—0.0436%，范围覆盖三个顺序和四张矩阵。这是局部输出向量长度变化，不是准确率或损失的百分比。完整模型干预提供最终行为证据；无需为这一补充量再堆一张主图。

图注：ΔR是相对旧模型新增的剩余参数更新，R0始终保留。靶向干预先按权重选ΔR前16个奇异分量，削弱50%，并减回其C投影；实际构造秩为32。随机对照匹配同秩和每矩阵实际参数改动长度，R1—R5为五次固定方向抽样。三种顺序共用同一个旧模型，不能作为三个独立旧模型解释。[SVG](A17_R05_retention_figures/figures/figure2_residual_tradeoff.svg) · [PDF](A17_R05_retention_figures/figures/figure2_residual_tradeoff.pdf) · [所有21点CSV](A17_R05_retention_figures/plot_data/figure2_TS_21.csv)。

## 可直接讲的两句话

1. 减缓初始前16个奇异秩一方向的更新，确实降低了选定系数的变化，但在学会新规则的同时，没有改善旧任务表现。这说明本轮参数保护方式不足以保持旧行为，尚不能据此判断所有共同计算保护方案。
2. 剩余部分的更新也会改变旧任务输出。针对性削弱其中的主要分量，比同秩、同改动长度的随机干预更能恢复部分旧表现，同时明显降低新表现；后续需要明确要保持的旧输入输出功能。

## 备用：行为变化与谱变化的时间对齐

![备用图](A17_R05_retention_figures/figures/figure3_backup_spectral_timing.png)

上排旧准确率，中排完整权重谱范数的最大相对变化，下排前16子空间重合的最大下降。三个纵轴各自独立，同一行在三个顺序中使用相同尺度；橙线标出第16步。连线仅辅助阅读已保存点。

谱范数是矩阵最强的输入放大倍数，中排取四矩阵的相对变化绝对值的最大值。子空间表示16个方向合起来覆盖的范围；下排分别计算输入/输出空间的平均主夹角余弦平方，再在四矩阵和两侧中取最大重合损失。不同矩阵的奇异值没有相加。

第16步TS旧准确率已降到48.375%—50.5%，最大的谱范数相对变化为0.083%—0.092%，前16子空间重合下降1.09%—1.41%。后期子空间确实继续变化。这张图支持“早期行为转向先于较大的整体谱变化”，保留为问答材料，不承担正文两条结论的叙述。

[SVG](A17_R05_retention_figures/figures/figure3_backup_spectral_timing.svg) · [PDF](A17_R05_retention_figures/figures/figure3_backup_spectral_timing.pdf) · [CSV](A17_R05_retention_figures/plot_data/figure3_TS_27.csv)。

## 问答与证据

**为什么还保留表1的其他对照？** 因为需要看清整体减速、随机方向与小奇异方向是否给出另一种权衡。新学习达标只说明B学会，不能代替旧能力保持的效用判断。正文先讲U/TS这一最关键比较，完整21行按需核对。

**为什么靶向恢复旧表现还不能直接推出分专家有用？** 因为本轮只改变一个冻结终点的参数，且新表现随之下降。按上下文选择残差、限制特定更新或保持旧输入输出，仍是待比较的方案。

[原A阶段审计]('''+str(C/'a_stage_audit_cn.md')+''') · [候选定位]('''+str(C/'A_localization_20261023/summary_cn.md')+''') · [残差诊断]('''+str(C/'A_residual_spectral_20261023/summary_cn.md')+''') · [图表来源与核验](A17_R05_retention_figures/manifest.json)。只重排既有证据，原1200步效用判断不变。
''')
(M/'meeting_brief_A17_R05_retention.md').write_text('''# Parameter-direction protection and old-task retention: meeting figures

The [Chinese speaking brief](meeting_brief_A17_R05_retention_cn.md) is the primary requested reading. This is a derived meeting artifact, not a new scientific owner. All values come from the frozen A endpoint audit, candidate-localization record, and residual diagnostic. No training, intervention, forward evaluation, or best-checkpoint selection was added.

## Purpose and operational setup

The broader aim is to preserve useful acquired computation while learning finer differences. This round uses two opposite visible-mode list rules as a minimal retention test. It continues from one acquired-old Qwen3-0.6B Base state and updates only the four last-attention projection matrices for 1200 new-task steps. Candidate C consists of 16 paired singular rank-one coefficients per complete acquired matrix; cross-input reuse remains unconfirmed. The actual intervention attenuates the optimizer's proposed candidate displacement rather than using separate C/R optimizers.

## Figure 1: smaller selected-coordinate movement without old-task retention

![Figure1](A17_R05_retention_figures/figures/figure1_protection_and_retention.png)

U is ordinary continuation and TS attenuates the initial selected directions. Columns show endpoint C net displacement, full-range old accuracy, the same old accuracy enlarged, and full-range new accuracy. Each point/order is shown separately. C displacement is divided by the initial joint C Frobenius norm,22.6734065,not accumulated path length. TS normalized displacement is0.0171%–0.0366%,versus0.1792%–0.4996%for U. TS old accuracies are0%,0%,0.5%,versus0%,0%,0.875%for U. All U/TS cases qualify on new learning. The intervention reduces selected-coordinate movement but does not deliver the intended old/new utility.

## Figure 2: targeted residual weakening restores some old accuracy at a new-task cost

![Figure2](A17_R05_retention_figures/figures/figure2_residual_tradeoff.png)

This figure focuses on TS, retaining all three orders. The x/y axes are new/old accuracy. Each panel shows the original endpoint, targeted weakening,and all five matched random directions. Insets show overlapping near-endpoint controls without jitter. These are frozen interventions,not training trajectories. Original old/new values are0/100,0/99.875,and0.5/98.625 percent;targeted values are45.5/59.375,37.375/67.125,and23.25/76.375. Random controls remain near the original endpoints. Thus the residual update affects old as well as new outputs,with a directional effect beyond matched random changes,but old recovery trades away new learning.

Delta_R is the added residual update,not the complete preexisting residual R. The target weakens50%of the leading16delta_Rsingular components after subtracting their C projection. This construction has rank32;random controls match that rank and per-matrix actual perturbation norm. At update16,fixed-old-input local delta_R output changes are9.53%–22.04%of initial output length,versus0.0040%–0.0436%for delta_C across four matrices andthree orders. Local output length is not a loss attribution.

## Two text tables

[Table1](A17_R05_retention_figures/tables/table1_main_experiment_cn.md) retains all seven methods andthree orders,old/newaccuracy,new-learning qualification,andold accuracy relative to U. Qualification requires each of four new command/panel cells,200answers each,to reach95%;new mean accuracy alone is insufficient. It is not an old-retention success label.

[Table2](A17_R05_retention_figures/tables/table2_residual_interventions_cn.md) lists original,target,andrandom results for each TS order,with changes relative to the original endpoint. Random rows retain mean andmin/max across five fixed draws;identical draws show one value. These ranges are not confidence intervals. Tables are Markdown andCSV,not images.

## Backup: separate spectral and behavioral scales

![Backup](A17_R05_retention_figures/figures/figure3_backup_spectral_timing.png)

Rows show old accuracy,maximal per-matrix absolute relative spectral-norm change,andmaximal top16input/output subspace-overlap loss. Orange marks update16. Within each row,the scale is shared across orders;different measurements have independent axes. Lines connect saved points only. Spectral norm is maximum input amplification. Overlap loss is one minus mean squared principal cosine,maximized over four matrices andinput/output sides. Singular values are never summed across matrices. Early behavioral turnover precedes larger later subspace changes;this is a temporal description,not causal mediation.

The three orders share one acquired-old model;every old/new evaluation has800answers anduses full-vocabulary predictions. Candidate localization does not yet establish cross-task shared computation. Original utility conclusions remain in the canonical source records. Provenance andverification are in the [manifest](A17_R05_retention_figures/manifest.json).
''')
# Small English table companions retain data through the same CSVs, with definitions.
(D/'tables/table1_main_experiment.md').write_text('# Table 1: all seven methods at update 1200\n\n'+t1.replace('顺序','Order').replace('方法','Method').replace('旧准确率（%）','Old accuracy (%)').replace('新准确率（%）','New accuracy (%)').replace('新学习达标','New learning qualified').replace('较U的旧准确率变化（百分点）','Old accuracy minus U (pp)').replace('| 是 |','| Yes |').replace('| 否 |','| No |')+'\n\nEach mode has800answers. Qualification requires all four new-task command/panel cells of200answers to reach95%. It does not imply old-task retention. Orders share one old model. The difference column is in percentage points. See the Chinese companion for method definitions.\n')
(D/'tables/table2_residual_interventions.md').write_text('# Table 2: TS frozen residual interventions\n\n'+t2.replace('顺序','Order').replace('条件','Condition').replace('旧准确率（%）','Old accuracy (%)').replace('新准确率（%）','New accuracy (%)').replace('旧变化（百分点）','Old change (pp)').replace('新变化（百分点）','New change (pp)').replace('原终点','Endpoint').replace('靶向削弱','Targeted').replace('随机对照','Random')+'\n\nChanges are relative to the same-order original endpoint. Random values are means with[min,max]over five fixed directions;identical draws show a single value. Ranges are not confidence intervals. Each mode has800answers. The intervention changes delta_R,not all R;actual construction rank32 andper-matrix perturbation norms are matched.\n')
(D/'README_cn.md').write_text('# A阶段结论图表\n\n[唯一汇报入口](../meeting_brief_A17_R05_retention_cn.md)。正文两张主图，谱图备用；所有解释放在图后。表格以文字和CSV交付，不提供表格图片。\n\n- [主图1](figures/figure1_protection_and_retention.svg)：选定系数变化减少，旧能力保持没有收益。\n- [主图2](figures/figure2_residual_tradeoff.svg)：残差靶向削弱恢复旧表现，同时降低新表现。\n- [文字表1](tables/table1_main_experiment_cn.md) / [CSV](tables/table1_main_experiment_21.csv)。\n- [文字表2](tables/table2_residual_interventions_cn.md) / [CSV](tables/table2_residual_interventions_9.csv)。\n- [备用图](figures/figure3_backup_spectral_timing.svg)。\n\n每张图均有同名PDF与320dpi PNG。SVG保留可编辑文字；PDF嵌入字体以便分享。无新训练或前向计算。[来源与核验](manifest.json)。\n')
(D/'README.md').write_text('# A-stage conclusion figures and text tables\n\n[Single speaking entry](../meeting_brief_A17_R05_retention.md). Two main figures,one spectral backup,andtwo Markdown/CSV tables. Explanations follow figures. Tables are not rendered as pictures. Each plot includes editable-text SVG,embedded-font PDF,and320dpi PNG. No new training or forward evaluation. [Manifest](manifest.json).\n')
for lang in ['','_cn']:
 p=S/'daily_research_reports/1023'/f'README{lang}.md'
 text=('# 10月23日会议材料\n\n[参数方向保护与旧能力保持：两张主图和两张文字表](meeting_report/meeting_brief_A17_R05_retention_cn.md)\n\n既有A阶段数据的汇报整理；研究问题和科学状态仍由原项目记录持有。\n' if lang else '# October23 meeting materials\n\n[Parameter protection and retention: two main figures andtwo text tables](meeting_report/meeting_brief_A17_R05_retention.md)\n\nPresentation of existing A-stage evidence;scientific ownership remains in the project records.\n')
 if not p.exists():p.write_text(text)
 p=S/'daily_research_reports'/f'README{lang}.md';s=p.read_text()
 if '1023/README' not in s:
  lines=s.splitlines();i=next(i for i,x in enumerate(lines) if x.startswith('|---') or x.startswith('| ---'))
  lines.insert(i+1,'| 10-23 | 参数方向保护与残差诊断：结论图表 | [进入](1023/README_cn.md) |' if lang else '| 10-23 | Parameter protection and residual diagnosis: conclusion figures | [Open](1023/README.md) |');p.write_text('\n'.join(lines)+'\n')
print('Bilingual brief and two text tables saved; one day-index speaking entry.')
