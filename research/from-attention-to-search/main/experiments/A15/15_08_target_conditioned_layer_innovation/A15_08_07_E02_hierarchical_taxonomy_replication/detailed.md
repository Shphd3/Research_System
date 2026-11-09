# Detailed: A15_08_07_E02_hierarchical_taxonomy_replication

Primary Anchor: `main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_07_semantic_conditioned_functional_subspace_anchor_cn.md`  
Frozen Protocol and registered revision: [protocol_cn.md](protocol_cn.md), `a15_08_06_e02-r1`, SHA256 `3ba0788cd6e8a24b60f9cf2842260f6d8e329c90621f243261df70012f019269`  
Summary: [summary.md](summary.md)  
Result eligibility: `ELIGIBLE`; scientific verdict is `INSUFFICIENT`, and knowledge wording remains `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

## 0. Quick Recap

**Purpose:** 把两次会议中的争论缩成两个可判定问题：宽谱是否主要由多个粗类内局部子空间叠加；\(R_U\) 能否在不借助标签选方向时压到低维仍保留未见数据功能。  
**Hypothesis:** H-GEO 要求局部谱更窄、局部方向更稳定且不同、八个局部子空间并集增秩三项同时成立；H-FUNC 只有在 full-\(R_U\) 先超过 duplicate/mismatch null 后才允许读取 80%/90% 交点。  
**Experiment logic:** 先残余化得到 \(R_U\)；再做同粗类/跨粗类匹配几何；最后用一次性新确认集比较 full、null 和多种低维投影。  
**Direct result:** 两层只有 union growth 通过；full-\(R_U\) 对只用 \(X\) 有正增益，但 full-minus-null 的同时 LCB 分别为 \(-0.0108\)、\(-0.0196\)。  
**Eligibility:** 新确认集新鲜、冻结后一次打开、8×5090 正常完成；一个 float32 数值守卫偏差经同数组 float64 复算全部通过。  
**Verdict:** block 24/28 均为 `GEOMETRY_INSUFFICIENT` 与 `INSUFFICIENT_NO_FULL_GAIN`；正式功能维数为 `NA`。  
**Claim boundary:** 可以说本轮没有确认局部窄谱并集解释，也没有确认低维功能秩；不能把描述性 RRR 8 维或 PCA 256/512 维写成表征秩。

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| \(X_\ell\) | 进入目标 MLP 前、未加入本层 attention 写入的状态 | \(N_\ell(h_\ell)\) | 4096 维向量 | 功能比较的基线输入 | 完整模型此前没有语义信息 |
| \(U_\ell\) | 本层 attention 写入后相对 \(X\) 的变化 | \(N_\ell(h_\ell+a_\ell)-X_\ell\) | 4096 维向量 | 候选“本层新增更新” | 纯新知识；它也含旧特征重混合和缩放 |
| \(R_{U,\ell}\) | 从 \(U\) 中去掉可由 \(X\) 线性预测的部分 | \(U-\widehat{\mathbb E}_{lin}[U\mid X]\) | 4096 维向量 | 避免把 \(X\) 的线性重复当新增功能 | 与 \(X\) 完全独立；也不排除非线性重编码 |
| 粗类 | 大学科 | 数学、物理、化学、生物、计算机、经济、医学、语言学 | 8 类 | 用作已知条件和 bootstrap 一级单位 | Router 的专家 ID |
| 细类 | 粗类内的子领域 | 每个粗类 8 个，如数学下代数、分析、组合等 | 每任务 8-way | 功能任务标签 | 自然语言所有语义类别 |
| 几何方差秩 | 覆盖 90% 协方差方差需多少方向 | \(r_{90}^{var}\)，任务内最大可识别 79 | directions/79 | 判断谱是否宽 | 任务功能所需维数 |
| 功能增益 \(G\) | 加入 correction 后交叉熵减少多少 | \(CE(X\text{-only})-CE(X+\text{correction})\) | nats/样本；越大越好 | H-ADMIT/H-FUNC 主指标 | 模型原生使用该方向 |
| PCA 头部 | 不看标签，按 \(R_U\) 方差从大到小取方向 | TRAIN PCA 的前 \(r\) 个方向 | \(r\in\{1,2,\ldots,512\}\) | 主表征压缩读数 | 最大方差就是最大路由价值 |
| Haar 随机子空间 | 不看标签随机取同样维数的方向 | 64 条嵌套随机正交基 | 与 PCA 同维数 | 判断 PCA 是否超过“只给维数” | 所有随机路由器的表现 |
| 监督降秩岭 | 用 TRAIN 标签共同学低秩输入映射与修正头 | reduced-rank ridge regression | 输入秩 \(r\)；8-way centered 输出秩最多 7 | 监督任务子空间 oracle | \(R_U\) 表征只有 7/8 维 |
| 准入门 | 先确认正确 \(R_U\) 真有样本配对功能 | full gain 超过 duplicate-\(X\) 与 64 个 mismatch gain 的 q95，且同时 LCB \(>0\) | nats/样本 | 防止对无资格信号讨论“保留率” | full gain 为 0 才会关闭；不确定也关闭 |

## 2. Anchor Link And Decision Point

会议先提出“整体高秩可能只是很多局部低秩语义子空间的并集”，随后又提出“即使表征宽，某个细分类任务也可能只需低维判别坐标”。本实验没有把这两句话混成一条：实验一检查几何并集，实验二检查未见数据上的功能保留，并用 full-\(R_U\) 准入门防止把任意 probe 可读性升级成新增功能。

本轮真正的决策点不是“维数是 8、256 还是 512”，而是：**是否已经有资格读取这个维数。** 结果是没有；因此维数只保留为描述性诊断。

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Protocol / scope | r1；实现、smoke、8×5090、一次性 confirmation、报告 | 与批准范围一致；未 commit/push/root sync | PASS | [protocol](protocol_cn.md) | 无 |
| 数据 | 8×8×10/每 split；确认集新模板、新文本、新 ID | TRAIN/DEV/TEST 各 640；确认集 2 条线索 320、4 条线索 320；重复/泄漏均 0 | PASS | raw `data_v2/data_receipt.json` | 无 |
| TEST 冻结 | 所有选择完成后才打开 | r2 freeze 显示 `test_metrics_absent=true`；确认 run 后打开 640 行 | PASS | raw `pre_test_freeze.json`; extraction manifest | 无 |
| 代码身份 | 冻结 snapshot | source manifest SHA256 `bc773de2...fad3f` | PASS | raw source snapshot | 无 |
| 资源 | 单节点 8×RTX 5090 SPOT | 8 张 RTX 5090、31.36 GiB/卡、sm120、CUDA 12.9 | PASS | raw `gpu_preflight.json` | 无 |
| 单元测试 | snapshot 全套通过 | 73 passed；renderer 新增 2 tests 通过 | PASS | raw `unit_tests.log`; local test log | 无 |
| 几何任务 | 每层 8 within +64 cross | 每层 72，共 144 | PASS | [geometry table](tables/geometry_task_summary.csv) | 无 |
| Trace 分解守卫 | 相对误差 \(\le10^{-6}\) | 原 GPU float32：111/144 超阈值，max \(6.58\times10^{-6}\)；同一冻结数组 float64 复算 0/144 超阈值，max \(8.34\times10^{-16}\) | DEVIATION, AUDITED PASS | [numerical audit](evidence/numerical_trace_audit.json) | 数值精度与守卫落盘偏差；不改输入、任务、科学指标或 verdict，证据仍 ELIGIBLE |
| 主功能任务 | 每层 8 个粗类内 8-way 任务 | 16 个任务完整 | PASS | raw functional result | 无 |
| 次功能任务 | 每层 8 个跨粗类兼容性任务 | 16 个任务完整 | PASS | [cross table](tables/cross_parent_compatibility.csv) | 仅 secondary，不救回主结果 |
| 不确定性 | 2,000 层级 bootstrap + 同时区间 | 2,000 draws；decision critical value 5.1004，curve critical value 4.6810 | PASS | raw functional result | 无 |
| 重试 / 排除 | 无科学结果后修改 | preconfirmation r1 因缺少已注册 cross-functional stage，在 TEST 未打开前被 r2 取代；最终 r2 无排除 | RECORDED | run roots r1/r2 | r1 不进入结果；r2/confirmation 可用 |

Frozen Protocol revision: `a15_08_06_e02-r1`  
Execution scope approved: implementation, smoke, full 8×5090 run, one-shot CONFIRMATION-v2, reporting  
Amendments: 执行前第 18 节明确确认集使用 5 个 k=2 与 5 个互补 k=4 表达；这是结果前冻结，不是结果后修改。  
Retries and exclusions: preconfirmation r1 superseded；正式 confirmation 只有一次，job `pt-8iy1thd6`，状态 `SUCCEEDED`。  
Missing conditions or artifacts: none for registered primary/secondary analysis.  
Post-hoc analyses: float64 trace 恒等式复核与读者用图表渲染；均未重算科学效应或更改阈值。

## 4. Actual Setup

### 4.1 数据是什么

数据共 1,920 条英文合成学科描述，结构固定为 **8 个粗类 × 每类 8 个细类 × 每个 split 每细类 10 条**。TRAIN、DEVELOPMENT、CONFIRMATION-v2 各 640 条。确认集每个细类有 5 条由 2 个事实线索构成、5 条由 4 个事实线索构成；模板、事实子集、规范化文本和 ID 均不与 TRAIN/DEVELOPMENT 重叠。

两条直观例子（中文转述，模型实际看到英文）：

1. “抽象运算满足封闭与逆元性质；研究由公理定义的群、环和域。判断宽学科与具体子领域。”标签是“数学—代数”。
2. “相变与自发有序；大量相互作用组分涌现宏观性质。判断宽学科与具体子领域。”标签是“物理—凝聚态物理”。

它适合本实验，因为粗类、细类、类别数和样本数都能严格对齐；因此“跨粗类更宽”不能由多了类别或样本解释。它比此前真实用户请求的粗细粒度数据更适合做**机制控制**，但后者语言更自然、更接近 Router 输入，更适合做**外部有效性确认**。两者不是互相取代：本数据回答“控制住规模后几何关系还在不在”，真实数据回答“现实请求里能否复现”。

### 4.2 学习与评价

- 模型：冻结 Qwen3-8B；block 24/28；decision token 为 `Classification:` 末位置。
- Residualizer：TRAIN 5-fold OOF ridge；DEVELOPMENT 选正则；只拟合 \(X\to U\)，不使用确认标签。
- 几何：TRAIN 内按粗类减均值；同粗类和跨粗类任务都为 8 类×每类 10 行；rank-7 局部判别基。
- 主功能任务：粗类已知，在每个粗类内做 8-way 细分类；8 个粗类等权聚合。
- 次功能任务：固定 8 个互不重叠跨粗类集合；只作数据兼容性描述。
- 读出器：所有分支复用同一 base logits、岭回归网格和评价路径。
- 候选维数：1、2、4、8、16、32、64、128、256、512。
- 独立统计单位：粗类为一级 bootstrap 单位，在每个细类内部重采样文本/模板；64 个 cross/mismatch 不被当成独立重复。
- 主 seed：`819060250`；bootstrap 2,000 次；max-t simultaneous intervals。

Code / config / data identities: data manifest SHA256 `61056fc1...8887`; pre-test freeze SHA256 `55ce2bef...e0c6`; functional result SHA256 `7b94948a...c9a`; cross result SHA256 `2bf24b35...e99c`.  
Known setup limitations: 合成模板、两个层、线性读出器；确认集相对旧 split 同时改变表达模板和事实数（2/4 vs 平均 3），所以结论限定为这种表达 shift 下的确认。

## 5. Metrics And Registered Decision Rules

### H-GEO

只有以下三项同时通过才是 `LOCAL_UNION_SUPPORTED`：

1. cross-minus-within 的归一化 \(r_{90}\)：同时 LCB \(>0\) 且点估计 \(\ge0.05\)；
2. within 重复方向相似度减 cross 粗类方向相似度：同时 LCB \(>0\) 且点估计 \(\ge0.10\)；
3. 八个局部子空间 union effective rank \(>\) same-parent bootstrap q95。

### H-ADMIT 与 H-FUNC

每层先计算：

\[
G_{full}-\max(G_{duplicate-X},q_{.95}G_{mismatch}).
\]

同时 95% LCB 必须大于 0，才允许读取

\[
r_{func}^{(m)}(\eta)=\min\{r:G_{m,r}\ge \eta G_{full}\},\quad \eta\in\{0.8,0.9\}.
\]

点估计过线但同时区间不过线记 `UNCERTAIN`；grid 内未达到记 `>512`；full 未准入统一记 `NA`。PCA 还需报告相对 64 条同维随机曲线；RRR 单独类型化，不承担表征秩结论。

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B24 局部并集 | 三项合取 | selection residual + 72 tasks | parent-center、r90、200 half splits、1000 union null | 2,000 bootstrap；同时 LCB | rank gap .0127/- .0253 LCB；orientation .0639/.0346 LCB；union 48.84 vs 22.36 | ELIGIBLE | GEOMETRY_INSUFFICIENT | union 单项通过不能替代合取 |
| B28 局部并集 | 同上 | 同上 | 同上 | 同上 | rank gap .0443/-.0063；orientation .0933/.0480；union 48.68 vs 25.01 | ELIGIBLE | GEOMETRY_INSUFFICIENT | 两个点估计接近阈值，但阈值是冻结的 |
| B24 full 准入 | full-minus-null simultaneous LCB >0 | 8 task npz + result JSON | 8 粗类等权 CE gain | 2,000 hierarchy bootstrap，跨层校正 | full .1541；null .1191；diff .0350；LCB -.0108 | ELIGIBLE | INSUFFICIENT_NO_FULL_GAIN | 不能把正点估计写成已确认优势 |
| B28 full 准入 | 同上 | 同上 | 同上 | 同上 | full .0682；null .0554；diff .0128；LCB -.0196 | ELIGIBLE | INSUFFICIENT_NO_FULL_GAIN | 同上 |
| PCA 功能维数 | H-ADMIT 后读取且超过随机 | curve statistics | first simultaneous crossing | 全曲线 simultaneous intervals | formal NA；描述性 B24 256/512，B28 512/512；random guard 均 false | ELIGIBLE, GATE CLOSED | NA | 描述性数不能晋升为功能秩 |
| RRR 任务子空间 | H-ADMIT 后类型化 | curve statistics + permuted/random controls | supervised reduced-rank ridge | 全曲线 simultaneous intervals | formal NA；描述性两层 8/8，随机与标签置乱 guard true | ELIGIBLE, GATE CLOSED | DIAGNOSTIC_ONLY | 输出秩最多 7；不能证明表征低秩 |
| 跨粗类兼容性 | secondary only | cross functional result | 8 cross tasks 等权 | simultaneous intervals | full B24 .1051 [.0643,.1459]；B28 .0478 [.0227,.0729] | BOUNDED | DESCRIPTIVE_ONLY | 跨粗类含粗类差异，无主准入门，不能救回 H-FUNC |

## 7. Main Results

### 7.1 实验一：有“并集增长”，但没有确认“窄局部子空间并集”

两层八个粗类的 rank-7 判别基拼在一起，有效秩约 48.7--48.8，而把同一个粗类反复重采样八次的 q95 只有 22.4--25.0。这说明不同粗类的监督判别方向并不完全相同。

但假设还要求局部谱显著更窄、同粗类方向重复稳定性差达到预注册幅度。B24 的 cross-minus-within 只有 0.013，B28 为 0.044，均没有达到 0.05 且同时下界小于 0；方向差 0.064/0.093，也没有达到 0.10。故三项合取不成立。

白话：**不同学科确实带来一些不同方向，但每个学科自己的更新云也很宽；不能说整体宽主要只是很多窄小空间拼起来。**

### 7.2 实验二：完整 \(R_U\) 有正增益，但“正确配对优势”未确认

相对只用 \(X\)，B24 full-\(R_U\) 增益为 0.1541 nats/样本，B28 为 0.0682；它们相对 0 的同时下界也为正。这说明完整 correction branch 在新表达上能够改善分类。

真正的准入比较更严格：正确 \(R_U\) 必须超过 duplicate-\(X\) 与不同细类错配 \(R_U\)。B24 优势点估计 0.0350，但同时下界 -0.0108；B28 优势 0.0128，下界 -0.0196。区间跨 0，所以不能确认改善来自当前样本正确配对的 \(R_U\)，正式维数必须停止读取。

### 7.3 PCA 与监督降秩岭告诉了什么、没告诉什么

若只看曲线形状，PCA 头部达到 80%/90% 的同时交点是 B24 256/512、B28 512/512；但同维随机子空间的同时超额守卫不通过。监督降秩岭在两层均为描述性 8/8，并超过随机和标签置乱对照。

正确读法是：**标签监督能迅速找到少量判别坐标，而方差最大的无标签方向需要数百维且没有稳健超过同维随机方向。** 这解释了为什么 gating 容易对齐 PCA 主方向却未必最优：主方向最显眼、能量最大，但目标函数不是“解释最多方差”，而是“区分哪个选择会带来相对功能收益”。不过 full gate 已关闭，加上 RRR 的 8-way 输出秩上限，本轮仍不能宣布 \(R_U\) 是低秩表征。

### 7.4 跨粗类兼容性只作旁证

跨粗类 8-way 任务的 full gain 为 B24 0.1051、B28 0.0478；点估计上 PCA 80%/90% 交点分别约 64/128 与 32/64，RRR 为 8/8。跨粗类任务含显著粗类差异，本来就更容易被宽语义坐标区分，而且没有主实验的 mismatch admission。它只能说明实现和数据可以运行这种任务，不能用来替代粗类内细分类结论。

## 8. Visualization Results

### 8.1 三个几何条件

![Experiment 1 geometry](figures/figure_1_geometry.png)

**横轴：**左图为 block 24/28 各自的同粗类与跨粗类任务；中、右图为两个 block。  
**纵轴：**左图是覆盖 90% 方差所需方向占 79 的比例；中图是同粗类重复 overlap 减跨粗类 overlap；右图是八个 rank-7 子空间拼接后的有效秩。  
**怎样看：**左、中的注册点阈值分别是 0.05 和 0.10；右图蓝柱要超过灰色 q95。右图通过，左、中未过，所以不是“差不多三个都过了”，而是合取假设未确认。  
**不能证明：**union growth 本身不说明每个局部空间低秩，也不说明 Router 应按粗类路由。

### 8.2 增益—维数曲线

![Experiment 2 functional curves](figures/figure_2_functional_rank_curves.png)

**横轴：**投影维数 1--512，按 log2 排列。  
**纵轴：**相对只用 \(X\) 的交叉熵增益，nats/样本；越高越好。  
**线：**黑色为完整 \(R_U\)；黄/橙虚线为其 80%/90%；酒红点线为准入 null；蓝色 PCA 头、青色 PCA 尾、橙色监督降秩岭；64 条灰线与灰带为同维随机子空间。淡色带是同时区间。  
**怎样看：**先看黑线是否可靠高于酒红 null，而不是先找蓝/橙线过 80% 的位置。两层 full-minus-null 下界都小于 0，所以后面的所有交点只可描述，不是正式功能秩。  
**不能证明：**橙线 8 维饱和不等于 4096 维 \(R_U\) 只有 8 维；蓝线贴近主方差也不等于它最适合路由。

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| data/freshness | 640 confirmation rows；overlap/leak=0 | passed | — | 旧文本重复造成结果 | 新表达 shift 本身增加方差 |
| extraction/identity | 640 rows；2 layers；hash-bound freeze | passed | — | 测试前调参、错层/错 hook | 只测两个 block |
| residualizer | finite；B24 test standardized \(R^2=.0866\)，B28 \(.5539\) | passed, diagnostic | B24 线性可预测部分迁移弱 | 数值失败 | 非线性 \(X\to U\) 仍可能存在 |
| geometry concentration | 两层 LCB<0，点估计<.05 | unclear / insufficient | 效应小于注册幅度且不确定 | “明显窄局部谱” | 更弱的局部差异 |
| geometry orientation | LCB>0，但点估计<.10 | insufficient by rule | 有方向差但幅度不足 | 强稳定局部方向 | 中等幅度方向差 |
| union growth | actual≫null q95 | passed | — | 所有粗类方向完全相同 | 不同方向并存 |
| full admission | 两层 diff LCB<0 | insufficient | correct-pair advantage 未稳定超过 null | 直接读取功能秩 | 更大真实确认集或更精准配对对照 |
| PCA compression | formal NA；random guard false | gate closed | full 未准入且无随机超额 | PCA=已确认低维功能方向 | 描述性高维增长趋势 |
| RRR | formal NA；描述性 8/8 | gate closed | full 未准入；输出秩上限 | RRR=表征低秩 | 少量监督判别坐标可拟合训练任务 |

Falsified physical prior: 未证伪“局部方向存在”，但削弱“每个局部空间明显很窄且共同解释整体宽谱”。  
Falsified mathematical model: 三项合取的强版本未获支持。  
Falsified operationalization / proxy: PCA 方差方向不能单独作为 Router 效用代理。  
Falsified implementation: no；数值 trace 偏差已定位为 float32 精度并复核。  
Falsified metric: no；H-ADMIT 正确阻止了无资格维数结论。  
Remaining rival explanations: \(R_U\) correction 的部分收益可能是类别级公共方向、容量或非样本特定信号；真实用户请求可能有不同信噪比。

## 10. Full Experiment Record

- preconfirmation r1: job `pt-1r7wv6ld`; `SUCCEEDED`; TEST unopened；因漏掉注册 secondary cross-functional stage 被明确 supersede，不用于最终 freeze。
- canonical preconfirmation r2: job `pt-vfvxiive`; `SUCCEEDED`; 73 tests；2 residualizers；144 geometry tasks；16 primary +16 secondary +16 nonlinear selection tasks；freeze passed；TEST metrics absent。
- formal confirmation r1: job `pt-8iy1thd6`; `SUCCEEDED`; 640 test rows；8 GPU extraction；2-layer residual apply；16 primary +16 secondary confirmation tasks。
- resource: `share-space` / `computing-cluster-5090-01g` / `n12lp.nn.i10a.8` / NORMAL SPOT / 8×RTX 5090。
- no result-dependent code, threshold, rank grid, exclusion, or rerun after TEST opening.

## 11. Interpretation

两次会议的核心困惑现在可以分开回答。

第一，“表征空间高秩”只描述整个 \(R_U\) 云的宽度，不等于每个任务都需要这么多维，也不等于信息本质高秩。本实验试图用“局部窄子空间并集”解释宽谱，结果只看到并集增长，没看到足够强的局部收窄和稳定性。因此这条解释目前只能保留弱版本：不同粗类确有不同判别方向，但它们并不足以说明整体宽谱主要由窄局部空间拼成。

第二，“gating 容易对齐 PCA 主方向”不推出最优分发。PCA 优化的是输入方差；Router 真正需要优化的是选择某专家后相对其他专家能减少多少损失。一个方向可以方差很大却在所有专家间共同出现，对分发没有区分力；一个方差较小的方向反而可能精确决定哪个专家更有用。本轮描述性曲线正体现这个错位：监督方向很快饱和，PCA 需要数百维且没有同时超过随机，但由于 full gate 未过，这只能作为方法直觉，不是 Router 实证结论。

所以主旨没有变成“低秩假设被证错”。更准确的更新是：**我们尚未确认可由 PCA 找到、又能保留正确样本 \(R_U\) 增益的低维表征子空间；监督任务坐标看起来较低维，但其证据类型更弱且受输出秩限制。**

## 12. Claim Boundary

**Can claim:**

- 受控学科数据上，不同粗类的 rank-7 判别子空间并集显著增长；
- 强版局部窄谱并集假设在 block 24/28 均为 Insufficient；
- full-\(R_U\) 相对 \(X\) 有正增益，但正确配对相对 matched null 的同时优势未确认；
- 因而正式 PCA/RRR 80%/90% 功能维数均为 NA；
- PCA 方差目标与监督判别目标在描述性曲线上明显不同。

**Cannot claim:**

- 语义或 \(R_U\) 内禀高秩/低秩；
- RRR 8 维是表征秩，或 PCA 256/512 是功能秩；
- 模型原生按这些方向计算；
- PCA/RRR 方向就是 Router 输入；
- 任一真实专家的相对效用、负载、专门化、持续学习或遗忘得到改善；
- 合成模板结果可直接外推到真实用户请求。

## 13. Next Decision

**Decision:** 是否在真实用户请求的新确认集上，先把“正确配对 full-\(R_U\) 稳定超过 duplicate/mismatch null”单独做实。  
**Completion criterion:** 至少一个预注册 block 的 full-minus-null simultaneous 95% LCB \(>0\)；若不过，所有功能维数继续为 NA，Router 支线停止。  
**Resume action:** 只审核 `A15_08_07_E01_clinc150_semantic_conditioned_functional_subspace` 的 confirmation freshness、样本配对 null 与 H-ADMIT 计算，不先运行完整维数曲线。

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [protocol_cn.md](protocol_cn.md) | frozen contract | human-approved r1 | meetings + anchor | `3ba0788c...19269` | yes | yes | result后未改阈值 |
| raw `data_v2/data_manifest.json` | data identity | builder v2 | registered taxonomy | `61056fc1...8887` | yes | yes | 1,920 rows |
| raw `pre_test_freeze.json` | TEST gate | r2 snapshot | all selection states | `55ce2bef...e0c6` | yes | yes | test absent |
| raw `geometry_result.json` | H-GEO verdict | snapshot r2 | 144 tasks | `e2d0415f...3fef` | yes | yes | trace deviation separately audited |
| raw `functional_test_result.json` | H-ADMIT/H-FUNC | formal confirmation | 16 primary tasks | `7b94948a...c9a` | yes | yes | 640 confirmation rows |
| raw `cross_functional_result.json` | secondary compatibility | formal confirmation | 16 cross tasks | `2bf24b35...e99c` | yes | bounded | descriptive only |
| [numerical trace audit](evidence/numerical_trace_audit.json) | deviation resolution | post-hoc audit v1 | frozen residual arrays/tasks | in [artifact manifest](evidence/artifact_manifest.json) | yes | guard only | no scientific metric changed |
| [functional curves table](tables/functional_curves.csv) | curated plot source | renderer v1 | raw functional result | manifest | yes | yes | rows typed by evidence role |
| [typed decisions](tables/typed_decisions.csv) | compact verdict source | renderer v1 | geometry + functional | manifest | yes | yes | formal vs descriptive separated |
| [figures](figures) | reader explanation | renderer v1 | curated tables/raw results | manifest | yes | yes | axes and boundaries explained above |

## 15. Links

- anchor: `main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_07_semantic_conditioned_functional_subspace_anchor_cn.md`
- protocol: [protocol_cn.md](protocol_cn.md)
- summary: [summary.md](summary.md)
- code workspace: `XingyuD/MoE_Routing_Experiments/active/a15_08_06_e02_hierarchical_taxonomy_replication`
- data / manifest: `/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e02_hierarchical_taxonomy_replication/data_v2/`
- result dir: `/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e02_hierarchical_taxonomy_replication/runs/confirmation-20260819T_formal_confirm_r1/`
- figure dir: [figures](figures)
- logs / receipts: raw preconfirmation r2 and confirmation r1 run roots
- repro renderer: `python render_results.py --data-root ... --geometry-root ... --functional-result ... --cross-functional-result ... --output ...`
- job ids: pre r1 `pt-1r7wv6ld` (superseded), pre r2 `pt-vfvxiive`, confirmation `pt-8iy1thd6`
