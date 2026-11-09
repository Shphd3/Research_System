# Detailed：A17_04_E01 条件映射变化与跨任务学习

主 Anchor：[A17_04](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor_cn.md)。
冻结 Protocol：[Protocol](protocol_cn.md)，版本 `A17_04_E01_r1`；冻结时间 `2026-10-11T09:53:00.623986+00:00`。
结果入口：[Summary](summary_cn.md)。
证据：测量合格，但不足以判断已学旧映射的保持假设。描述裁决：`INSUFFICIENT_OLD_MAPPING_NOT_ACQUIRED`。科学机制接受／问题关闭：`Unknown`。

## 0. 简要结果

Full 完成三个 seed、每 seed 四阶段，共 2,880 次更新、57,600 个有效答案目标。Smoke、四次独立精确恢复、源冻结和 Full worker 检查通过。全部 120 个保存矩阵／训练状态已核验并登记。

旧映射未通过学习前提：DEV 每口令／分项 33%–54%，预设门槛 80%。合并 TEST 中，反向比同向少改善旧答案优势 0.005165 nat，但两个分支都改善旧 CE 与平均优势。旧 CE 收益主要由三词列表总概率提高解释，三词内部选择略变差。新映射资格与联合可行性也未达标。因此，本轮给出有限的概率更新事实，不能证明已学规则的干扰机制或参数分开收益。

## 1. 术语与定义

| 术语 | 白话与计算 | 单位／用途 | 不能证明 |
|---|---|---|---|
| 旧／新模式 | 前文可见的模式一／二 | 条件输入 | 内部路由 |
| 同向／反向 | 保留／交换甲首乙末映射 | 任务关系干预 | 本质矛盾 |
| 答案优势 | 正确端点 log 概率减另一端 | nat；主读数 | 全词表准确率 |
| 列表访问／选择 | 三词总概率／正确词在三词内部份额 | CE，nat | 两个内部功能 |
| 模式—口令响应 | 两口令的末项相对首项 log 优势之差 | 精确输出坐标 | 参数模块 |
| 联合可行性 | 继续教两模式及旧标签 | 成功才提供可行实例 | 等监督胜出；容量不可能 |
| 未见顺序／组合 | 已训练三词集合的新排列／新三词集合 | 独立留出分项 | 未见词汇迁移 |

## 2. Anchor 与决定点

用户激活同级任务关系问题，没有给 A17_03 增加第四项实验。合并是一项同向／反向映射干预及诊断读数。此前成分／轨迹实验保持任务固定，本轮改变任务关系。旧模式同时教两个口令，因此不测试缺失位置补足。唯一未来研究者决定是：条件映射证据是否值得比较共享／分开参数。这个证据不足结果不能决定架构效用。

## 3. 冻结、符合性与偏离

| 注册项目 | 预期 | 实际 | 状态／资格影响 |
|---|---|---|---|
| 范围 | 实现／Smoke／Full，不用中途批准 | 用户明确接受合并并要求完成 | 已授权；科学裁决 Unknown |
| 科学正文／源冻结 | 双语契约、配置／数据／代码快照 |Smoke 和 Full 前后查 21 文件 |PASS，无科学变更|
| 数据 |每世界训练2,400、DEV／TEST800 |跨三个世界物理训练7,200／DEV2,400／TEST2,400 |schema／划分／均衡 PASS|
| 任务／模型／目标 |可见模式中性口令、答案 CE、只末层 o_proj |冻结配置与各 worker 冻结检查 |工程 PASS|
| 条件／预算 |3 seed×4阶段×240更新 |2,880更新、57,600目标；阶段独立计数 |完成|
| 检查点 |0／1／16／50／120／240；共同旧分支起点 |Full72、Smoke48；9次分支0点字节检查 |PASS|
| 恢复／telemetry |四独立精确恢复、必需标签 |四恢复 exit0 与阶段检查 |PASS|
| 旧能力 |DEV 每口令／分项≥80% |33%–54%，三个 seed 都失败 |已学规则解释证据不足，事实保留|
| 主效应 |固定240新更新合并 TEST 配对优势 |−0.005165nat，三 seed 负，幅度<0.01 |小的描述相对差，不是支持裁决|
| 可比能力／联合 |预设 DEV 达标读数 |六条轨迹 NOT_REACHED、联合 FEASIBILITY_UNKNOWN |不可比，不证明容量|
| 资产门槛／顺序 |strict 保存产物检查后分析 |首次 enum 错误 exit2，分析误提前；修后通过并重算 |偏离保留，只用修后事实分析|

登记最初对 28 个 adapter family 使用了不合法的 enum `CHECKPOINT_STATE_PRESENT`，后来修为 `MODEL_STATE_PRESENT`。只改 metadata，实际 payload／哈希、数据／配置／代码和 GPU 训练不变。初次 strict check 返回 2，分析却已启动，临时结果保留在 `analysis/attempts/pre_access_enum_fix`。修正后 30 产物 strict 检查通过，再确定性重跑分析。`results.json`、`paired_table.csv`、`descriptive_sample_table.csv` 与临时版本逐字节相同。事实交付因此修复，但执行顺序偏离不能抹去。[修正记录](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/registration/schema_correction.json)与[重分析回执](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/registration/reanalysis_after_strict_access.json)保存全过程。

没有 GPU 重试、适应性延长、排除 seed、科学正文修订或结果驱动指标变更。Full `pt-qs6ndgat` 平台状态 SUCCEEDED，终点更新时间 `2026-10-11T10:06:57.95841Z`。worker 完成、科学资格与平台状态分开。

## 4. 实际设置

Run：`/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z`。
输入 ID：`model_qwen3_0p6b_base_official_a5`、`tokenizer_qwen3_0p6b_base_official_a5`、`data_a17_conditional_mapping_v1`。
父模型：`/data/250010109/model_cache/Qwen3-0.6B-Base-official`。
只训练末层 attention `model.layers.27.self_attn.o_proj.weight`，1,024×2,048。上下游权重冻结。FP32、SDPA、确定性、无 dropout／TF32、原生前向。固定输入的上游投影输入不变，投影位移精确等于矩阵增量乘该输入；下游预测／损失仍是非线性。
目标：平均单答案 CE；普通 SGD LR0.01、clip1，无 momentum／decay／辅助损失。micro5×累积4，每步20个有效答案。四 worker 执行独立 case，不是数据并行复制。

Full 的训练顺序 seed 为29／43／71，全部使用相同预训练起点，不是不同随机权重初始化。每个旧、同向、反向、联合阶段240步。旧和主新阶段各4,800答案、两个确定遍历。联合旧2,400＋新2,400，一遍底层列表：每步五列表，各模式两口令。其旧监督额外、新曝光只有主分支一半。全部保存／评估0／1／16／50／120／240存在。状态包含矩阵、优化／scheduler 描述、RNG、cursor／order、step／targets、parent／config／stage。没有再导出完整 Base，每个 adapter 必须依赖精确父模型。Smoke 四 case 含一个 seed29 重复，各阶段3步，共48更新／960答案。四独立恢复下一步另外处理80答案。六个同范数诊断各用20源答案，不计为累计训练轨迹。

20答案词：红、黄、蓝、黑、绿、白、紫、灰、金、银、猫、狗、鸟、鱼、牛、马、羊、虎、龙、花。data manifest 有精确 ID。生成 seed20261011 将57循环三词轨道分训练30、DEV组合10、TEST组合10、unused7。训练1,200列表配两口令；每 DEV／TEST 分项200列表配两口令／世界。每世界训练2,400、DEV／TEST800，物理文件各保存三世界。有意模式间共享底层内容，主新训练无旧完整前文。两个新世界的前文／顺序／答案直方图相同，仅映射标签不同。

DEV／TEST 都用熟悉词。顺序分项复用训练无序三词集合的新排列；组合分项用训练未出现的三词集合。DEV 仅选预设可比点。Full 机械记录预注册里程碑 TEST，它不选择 stop／预算／标签／参数／检查点。全部有限训练完成后才解释。单模板、预训练父模型、末层单矩阵学习限定范围。

## 5. 指标与冻结决定规则

主量 \(E_s=\Delta M_A^{reversed}-\Delta M_A^{consistent}\) 是240新更新后的旧正确端点相对另一端 log 优势，都相对同一旧终点。口令与分项等权，分项单列及合并。重复单位是 seed。报告各效应、均值、范围、样本标准差，不作显著性／总体置信主张。描述稳定负的约定要求三个<0、均值≤−0.01nat，并且旧／新学习合格。旧 DEV 每口令／分项≥0.80；新有效学习要求合并 TEST CE 改善≥0.01nat 或准确率提高≥1百分点。后一项只检学习，不等于规则掌握。

可比能力取首个保存新 DEV 两分项≥0.80的点，本轮没有。联合成功本应要求各模式／分项 DEV≥0.80；失败则可行性 Unknown。阈值是委托报告约定，不是研究者科学置信裁决。旧能力失败，优先阻止将方向效应解释成保持证据。

列表集合 \(S\) 上，CE 精确等于访问 \(-\log\sum_{w\in S}p(w)\) 加选择 \(-\log[p(y)/\sum_{w\in S}p(w)]\)。另存20词池概率／条件 CE、全词表 argmax、最强错误词、端点／全竞争优势。定义 \(s_{m,c}=\log p(L_3)-\log p(L_1)\)、\(a_m=(s_{m,乙}-s_{m,甲})/2\)、\(q_m=(s_{m,乙}+s_{m,甲})/2\)、\(C=(a_1+a_2)/2\)、\(K=(a_2-a_1)/2\)。这些是输出坐标。旧口令均衡时，\(a_1\) 等于旧平均端点优势；恒等式不是独立机制证据。

## 6. 证据来源链

| 主张／规则 | 原始产物及计算 | 汇总／观察 | 资格／边界 |
|---|---|---|---|
|旧前提|Full `old_endpoint.json`／DEV；`launch/analyze.py` old_acquisition|每 seed／口令／分项33%–54%，都失败80%|已测，熟练旧规则保持证据不足|
|主效应|Full `eval_00240.json`；results primary／pairedCSV|三 seed 配对，分项等权；均值−0.005165nat|有限相对概率作用，前提失败|
|候选解释|同 TEST；pooled_endpoint_reader；精确 list3拆分|下表旧 ΔCE／访问／选择|输出账本，不唯一内部原因|
|新条件响应|同列表配对；mode contrasts|反向新 \(a_2=+0.005931\)，希望负|没有确立条件反转|
|可比／联合|保存 DEV 里程碑、联合终点|6 NOT_REACHED、3 FEASIBILITY_UNKNOWN|难度／容量解释未排除|
|即时效应|Full seed `one_step/` 读数／资格；equal_norm_one_step|下表同状态同范数三效应|合格局部比较，不完整轨迹中介|
|数值恒等式|102源读数；独立重算|460,920记录出现，max1.0129319e−6nat|数值 PASS，重复记录不是独立样本|
|保存状态|checkpoint manifest／checks|120状态，父起点与旧分支起点精确一致|工程／资产，不科学批准|

完整读数哈希和分析脚本版本见[analysis manifest](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/analysis_manifest.json)。Analyzer SHA256 `0148b327193c4f96aee7e732db5c7d0f02d1d1f43d913969df365236b3c84213`。全部预注册 seed／分项保留，无补值或结果排除。

## 7. 主结果

### 旧能力与等预算终点

DEV 旧终点准确率：

| Seed | 甲顺序 | 甲组合 | 乙顺序 | 乙组合 |
|---|---:|---:|---:|---:|
|29|52.5%|53.0%|33.5%|39.0%|
|43|51.0%|54.0%|34.0%|40.0%|
|71|50.0%|53.5%|33.0%|41.0%|

没有一项达80%。这不代表没有学到部分信息，而是本轮没有建立注册起点条件。

三个 seed 的旧 TEST 等权均值：

| 分项 | 旧终点 CE／准确率／优势 | 同向终点 CE／准确率／优势 | 反向终点 CE／准确率／优势 |
|---|---|---|---|
|顺序|1.106820／49.4167%／.035938|1.032439／49.1667%／.049357|1.034024／49.5833%／.047828|
|组合|1.134068／50.0833%／.055509|1.044758／50.2500%／.079203|1.049448／50.3333%／.070402|
|合并|1.120444／49.7500%／.045724|1.038598／49.7083%／.064280|1.041736／49.9583%／.059115|

CE／优势单位 nat／答案，准确率按全词表。两分支平均 CE／优势都改善，不能说净损害，也不能说已掌握规则被保持。

| 分项 | E seed29 | E seed43 | E seed71 | 均值／样本标准差，nat |
|---|---:|---:|---:|---:|
|顺序|−.001569147|−.001480947|−.001536922|−.001529005／.000044630|
|组合|−.008889108|−.008783555|−.008732896|−.008801853／.000079697|
|合并|−.005229127|−.005132251|−.005134909|−.005165429／.000055180|

所有效应为负，各分项均值的绝对值都小于0.01 nat报告幅度。注册描述裁决因旧映射资格失败而证据不足。方向重复原样保留，不能提升为稳定的已学规则机制。

### 候选访问、新学习与条件响应

| 旧合并相对旧终点变化 | 总 CE | 列表3访问 CE | 列表3选择 CE |
|---|---:|---:|---:|
|同向|−.081845883|−.086274679|+.004428796|
|反向|−.078708358|−.085027625|+.006319266|

三词概率总和从87.2696%升到94.9785%／94.8624%。访问改善超过全部 CE 收益，内部选择略变差。端点平均优势提升并不矛盾：中项竞争和非线性平均不同于端点平均 log 优势。精确拆分描述输出，不因果划分参数。

| 新 TEST 分项 | 同向 CE／准确率，起点→终点 | 反向 CE／准确率，起点→终点 |
|---|---|---|
|顺序|1.176080→1.069659／46.50%→47.75%|1.169551→1.063201／47.0833%→47.3333%|
|组合|1.208532→1.087370／47.00%→46.6667%|1.225542→1.113271／45.4167%→49.00%|
|合并|1.192306→1.078515／46.75%→47.2083%|1.197546→1.088236／46.25%→48.1667%|

六个新分支都满足有效 CE 学习约定，但都没有 DEV 可比80%点。反向 TEST 口令响应 \(a_2\) 为顺序−.008390、组合+.020251、合并+.005931，没有一致达到反转所需负响应。CE 收益不能证明意图中的条件规则学会。旧 \(a_1\) 两分支都提高，模式响应差异也变化，但这些输出坐标不能识别内部共享／独特处理。

联合反向的旧／新 TEST 合并准确率50.2083%／47.50%，CE1.045236／1.103891。三个可行性状态都 Unknown。联合有额外旧标签、新目标只有2,400，不是匹配新曝光的主 winner。

### 同范数即时作用与实际更新幅度

| Seed | 同向旧 ΔCE／Δ优势 | 反向旧 ΔCE／Δ优势 | 反向减同向旧 Δ优势 |
|---|---|---|---:|
|29|−.000507320／+.000075006|−.000511443／+.000058444|−.000016563|
|43|−.000949320／+.000085437|−.000937606／+.000070469|−.000014968|
|71|−.001088315／+.000039830|−.001150055／+.000026991|−.000012839|

每探针源输入／顺序／答案边际匹配，起点权重相同。实际范数相对失配≤1.86265e−7。两个探针 CE 都改善，小的相对优势差不解释完整轨迹。主训练范数累计和：同向2.397132／2.393285／2.397529，反向2.397099／2.393728／2.397261。它们是路径长度，不是净位移；普通主训练没有逐步强制同范数。完整 source metrics 保留这个竞争解释。

### 事后解释样本，不是确认

Seed71、旧模式一甲、列表 `马 花 猫`，正确答案是马。样本在看完结果后选取，用来解释答案翻转，不是独立机制检验。

| 状态 | p(马) | p(猫) | 正确 CE | 马减猫优势 | 最大概率答案 |
|---|---:|---:|---:|---:|---|
|旧终点|46.0013%|42.3474%|.776499|+.082764|马，正确|
|同向|48.0829%|46.8537%|.732243|+.025898|马，正确|
|反向|47.2847%|47.4714%|.748983|−.003941|猫，错误|

反向让正确词概率提高、CE 改善，但竞争答案超过它。这说明为什么 CE 改善不能保证正确规则选择。一个选择后的样本不能证明这种现象的频率、特异性或内部原因。来源是 `descriptive_sample_table.csv` 与 results 的 descriptive_samples。

## 8. 补充：同状态损失推导

这是结果后的精确代数说明，用于解释为什么反向标签不要求完整来源梯度反向，不修改冻结的主分析。在同一矩阵状态 \(W\)，对同一批模式二甲乙配对输入，分别计算同向标签平均损失 \(L_s\) 与反向标签平均损失 \(L_r\)，单位为 nat。令 \(s_c=\log p(L_3\mid c,L)-\log p(L_1\mid c,L)\)，口令响应为 \(a_2=\mathbb E_L[(s_{乙}-s_{甲})/2]\)，模式二固定。逐口令配对相减得精确关系：

\[
L_r-L_s=a_2,\qquad G=\frac{L_s+L_r}{2},\qquad
L_s=G-\frac{a_2}{2},\quad L_r=G+\frac{a_2}{2}.
\]

原始梯度因此为 \(g_s=\nabla_WG-\tfrac12\nabla_Wa_2\)、\(g_r=\nabla_WG+\tfrac12\nabla_Wa_2\)。标签干预改变其中一项的符号，仍保留一个同号项。令 \(P_2(x)=p(L_1\mid x)+p(L_3\mid x)\)，则：

\[
G=\mathbb E_x\left[-\log P_2(x)+\log\left(2\cosh\frac{s_x}{2}\right)\right].
\]

平均范围是两个口令及配对列表。\(G\) 包含首末总概率和首末偏好平衡，不是纯候选适应，更不是内部共同模块。\(a_2\) 小不代表其梯度小。若裁剪或范数匹配后实际更新为 \(d_s=-\eta_sg_s\)、\(d_r=-\eta_rg_r\)，精确有：

\[
d_r-d_s=(\eta_s-\eta_r)\nabla_WG-\frac{\eta_s+\eta_r}{2}\nabla_Wa_2.
\]

同范数不保证有效比例 \(\eta_s,\eta_r\) 相同。本轮未测成分梯度大小、夹角及有限成分干预，不能据此宣布参数机制已确定。

[同状态恒等式核验](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/paired_loss_identity.json)在72个面板格通过，最大绝对差 \(5.58794\times10^{-9}\) nat。共同旧终点的新输入 \(L_s=1.192306\)、\(L_r=1.197546\)、\(a_2=0.005240\)。不同训练状态的损失不能代入同一恒等式。这是公式实现核验，不是新的经验机制发现。

## 9. 阶段证据与失败分解

| 阶段 | 证据 | 结果 | 还剩什么 |
|---|---|---|---|
|数据 preflight|manifest／qualification|PASS|单模板合成推广范围|
|Smoke|`pt-jw3bhrzi`、gate、21文件|PASS|不裁决科学假设|
|独立恢复|四 worker|PASS精确|测下一步恢复，不科学证据|
|Full|`pt-qs6ndgat`、qualification／freeze|SUCCEEDED／PASS|旧规则前提失败|
|资产／分析门槛|schema 修正、strict 重算回执|修复，偏离保留|初次顺序错误不能抹去|
|独立重算|102文件／460,920记录出现|max1.0129319e−6，PASS|恒等式检查不证明机制|

没有验证或证伪“普遍干扰”的物理先验。CE 恒等式通过，不是经验发现。实现／训练检查通过，资产 schema／顺序失败已修复。充分学会旧映射的操作前提失败。CE 独自作为规则能力代理在此不足。难度、初始能力、冻结矩阵学习限制和优化解释仍存在。

## 10. 完整实验记录

### 2026-10-11：合并条件映射一轮

1. 问题／H：等曝光下，新反向映射是否比同向改变旧预测作用。
2. 设置／控制：官方 Base、只末层 o_proj；共同旧終点，新前文／顺序／答案边际／预算相同；三 seed、四卡 reserved H100、登记镜像。
3. 训练数据：生成可见模式／中性口令，每世界2,400记录。旧和主新两遍，联合列表一遍、两模式标签。
4. 确认：冻结 DEV／TEST 顺序与组合。DEV 仅选预设可比点，TEST 机械保存、不调参；全部有限训练后解释。
5. 结果：Smoke／外部恢复／Full完成；主E−.005165nat，旧资格失败；六个可比点缺失，联合 Unknown；候选访问拆分已测。数值、状态及 strict 输出合格。资产顺序偏离／重分析保留。
6. 认识／边界／下一项决定：没有已学旧规则前提，概率变化不能证明规则保持或迁移。未确立平均 CE／优势净损害或分开收益。科学关闭 Unknown。AI 建议先旧任务能力资格，不凭建议启动新任务。

## 11. 解释

映射干预改变注册模型的有限预测，但其已学规则意义证据不足。一般候选适应与输出拆分直接相容，没有被排除。相对优势差小于预设报告幅度，不能跨过旧能力前提失败。可比／联合读数失败使难度、可实现性没有解决。此前成分实验与本轮映射实验互补，均未证明专家分开优势。

## 12. 主张边界

能说：全部预注册有限训练／读数完成且合格；实际状态已登记；中性映射未过学习门槛；反向给旧优势较少的小收益；旧合并 CE 主要由列表访问改善解释。
不能说：熟练旧规则被遗忘，成功反向规则迁移，不可避免任务冲突，唯一内部因果模块，完整模型容量不足，参数／专家分开更好，自然文本推广。科学机制裁决与关闭保持 Unknown。

## 13. 下一项决定

唯一未来研究者决定：足够的条件映射证据是否值得共享／分开参数比较。当前证据不能决定。AI 建议先做有限旧任务能力诊断，不先扩大分开或 SAE；这不是新激活任务。当前执行任务完成。恢复时读本 Summary／注册测量，再由研究者给下一科学范围。

## 14. 产物 manifest

| 产物 | producer／身份／来源 | 完成 | 资格／说明 |
|---|---|---|---|
|冻结契约／配置／代码／数据|`freeze.json`；09:53:00Z；config SHA `9d47a5c31821c1528d2de598e7a5735325a95c946d8834be4345762b3465d226`|是|21文件前后不变|
|data manifest|`a17_conditional_mapping_v1`；seed20261011|是|注册输入，不是学习证据|
|job／worker 回执|Smoke09:53:28Z／Full09:56:33Z，均SUCCEEDED，worker合格|是|平台与科学结果分开|
|检查点 payload／manifest|Full72＋Smoke48；需父模型；权重／RNG／cursor／counters|是|28adapter族，无完整Base导出|
|原生读数 manifest|Smoke／Full逐记录|是|两个 representation族，有界含义|
|strict产物 access|[30产物快照](/data/250010109/Research_System/assets/checks/2026-10-11_a17_mapping_output_access.json)|PASS30|访问／probe，不科学批准|
|注册分析|results、paired／descriptiveCSV、manifest|是|修后strict门槛确定性重算|
|schema／顺序修正|修正记录、重算回执、临时结果|是|偏离保留，无 payload／科学变更|

登记[回执](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/registration/receipt.json)给出实际28adapter／2读数族，链接[payload manifest](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/payload_manifest.json)。独立派生分析已登记为 `analysis_a17_04_mapping_20261011t095038z`，通过[当前选定访问检查](/data/250010109/Research_System/assets/checks/2026-10-11_a17_mapping_analysis_access.json)；此处30产物检查仍有其独立范围。数据 SHA256：train `3b57c72970cba2a5478caab85369bfb53804094960422ba7e2fca9ddcf14ca03`；DEV `e382ae70dea12c65aeb9178e1c32ec1eb205039181be2dbc38b38ec9379a0471`；TEST `963b4f75d6c835fffbfb79860dc1e85d687b734086103dfe53fef3b551a5f1da`。

## 15. 链接

执行根：`/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer`；run `/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z`。
Runner `source/run.py`；analyzer `launch/analyze.py`；config run `config.json`；data 根 `data/conditional_mapping_v1/manifest.json`；strict inputs 根 `provenance/input_access.json`；freeze run `freeze.json`。
决定性结果：[results](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/results.json)、[paired表](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/paired_table.csv)、[描述样本表](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/descriptive_sample_table.csv)、[分析来源](/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/runs/mapping_20261011T095038Z/analysis/analysis_manifest.json)。
Job：Smoke `pt-jw3bhrzi`、Full `pt-qs6ndgat`。状态快照、提交证书和挂载日志留 run。复现命令冻结于 run `full_launch_contract.json`；需要精确父／数据／runtime 与明确授权。
