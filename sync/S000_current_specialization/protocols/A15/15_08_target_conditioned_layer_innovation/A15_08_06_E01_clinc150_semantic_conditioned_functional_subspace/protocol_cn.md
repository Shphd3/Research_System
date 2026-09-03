# Protocol：A15_08_06_E01 CLINC150 语义条件几何与低维功能子空间

## 0. 审批快照

- **文档状态：**`APPROVED_AND_FROZEN_FOR_EXECUTION`。
- **覆盖的人工请求：**审计 0818 Routing exp 对话和截图，列出全部条件、数据和分析，并先形成一个完整 Anchor 与一个 Protocol 供审核。
- **执行授权：**用户于 2026-08-18 明确批准全部设计并要求开始执行；正式任务冻结使用单节点 `8×5090`（资源档位 `5090-8-spot`）。TEST 仍须等 freeze receipt 通过后一次性打开。
- **主 Anchor：**[A15_08_06](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_06_semantic_conditioned_functional_subspace_anchor_cn.md)。
- **实验角色：**真实任务迁移与语义条件化检验；不取代 A15_08_05。
- **主对象：**冻结 Qwen3-8B block 24、28 的 $X$、$U$ 与仿射线性残余 $R_U$。
- **主数据：**CLINC150 英文 in-scope utterances；官方 TRAIN/validation/test；排除 OOS。
- **几何主判据：**匹配的 within/cross 归一化 $r_{90}^{var}$，加局部子空间方向和并集检验。
- **功能主判据：**domain 等权的未见数据交叉熵增益。
- **功能秩：**不使用类别数 $C$ 判定；直接报告 $R_U$ 投影达到 $0.8G_{full}$ 与 $0.9G_{full}$ 的最小维数。
- **监督方法：**固定为 reduced-rank ridge regression（监督降秩岭回归，RRR）。
- **不能 claim：**语义内禀秩、非线性新信息、模型原生使用、expert utility、Router 改进、专门化或遗忘减少。

### 待人工确认块

| 块 | 待确认决策 | 状态 |
| --- | --- | --- |
| A | 两子问题与 claim boundary | `CONFIRMED` |
| B | CLINC150、仅 in-scope、完整 10×15 映射 | `CONFIRMED` |
| C | Qwen3-8B、prompt/token、block 24/28、$R_U$ 定义 | `CONFIRMED` |
| D | matched within/cross 构造及 Global-150 仅描述 | `CONFIRMED` |
| E | 先准入 full $R_U$，再解释功能秩 | `CONFIRMED` |
| F | 监督降秩岭回归；80%/90% 功能保留曲线 | `CONFIRMED` |
| G | 阈值、null 数、bootstrap、资源和输出 | `CONFIRMED` |

七块均已由用户确认并冻结。实现必须记录本文 SHA-256；任何会改变数据、对象、阈值、比较族或 TEST 使用方式的修改都必须形成新 amendment，不能静默覆盖本次批准。

## 1. 决策问题与类型化结论

### Q1：几何混合

类别数和样本数一致时，within-domain 更新云是否比 cross-domain 更集中；局部子空间是否稳定且方向不同；它们的并集维数是否超过同 domain 重采样零假设？

结论类型：

- `LOCAL_UNION_SUPPORTED`：集中、方向稳定差异、并集增长全部通过；
- `LOCAL_CONCENTRATION_ONLY`：秩收窄，但方向或并集证据不通过；
- `NO_LOCAL_CONCENTRATION`：匹配秩比较在有充分区分力时为无效或相反；
- `GEOMETRY_INSUFFICIENT`：谱、稳定性、映射或样本 guard 失败。

### Q2：低维功能保留

在新任务上准入 full $R_U$ 后，把 $R_U$ 投影到多少维，能够在未见数据上分别保留 full $R_U$ 的 80% 与 90% 新增可访问性，并超过同秩随机对照？

每层结论类型：

- `FUNCTION_RANK_80_90_ESTIMATED`；
- `FULL_GAIN_BUT_THRESHOLD_NOT_REACHED`；
- `INSUFFICIENT_NO_FULL_GAIN`；
- `FUNCTION_INSUFFICIENT_GUARD`。

### Q3：方差排序

同秩下，PCA 头部是否保留与监督降秩岭回归方向相同的功能？这是方法比较，不单独承担科学 promotion。

## 2. 数据、来源与具体例子

### 2.1 规范来源

CLINC150 是英文任务型对话用户意图分类数据，包含 10 个业务领域、150 个用户意图，每个领域 15 类。  
每类提供 100/20/30 条训练/验证/测试样本；本实验排除越界样本，只使用 22,500 条域内样本。

- 官方仓库：`https://github.com/clinc/oos-eval`；
- 原始文件：`data/data_full.json`；
- 预期域内结构：150 个用户意图类别、10 个领域；每类为 100 TRAIN、20 validation、30 test；
- 预期 in-scope 总数：15,000/3,000/4,500，共 22,500；
- 主实验排除全部 OOS。

原始文件没有一个可直接信任的完整领域字段。实现前必须根据论文/补充材料的用户意图类别列表生成冻结的 10-domain×15-class 映射，独立核对每个原始类别恰好出现一次，并记录来源与 SHA-256。缺失、重复、领域非 15 类或 split 数量不符均硬停止。

预期 domain 名包括 banking、credit cards、work、meta、auto and commute、travel、home、utility、kitchen and dining、small talk；真正执行时以规范化并带 hash 的 manifest 为准。

### 2.2 任务例子

下表是帮助理解的意译，不替代原始数据：

| 任务 | 用户意图例子 | 实验作用 |
| --- | --- | --- |
| 银行业务 15 类 | 账户间转账、冻结账户、查询余额 | 共享金融词汇但动作不同，检验固定粗主题后的细区分 |
| 旅行业务 15 类 | 订机票、查询航班状态、报告行李丢失 | 共享旅行/航班词汇，不能只依靠粗主题 |
| 跨领域 15 类 | 账户间转账、安排会议、订机票、查询积分余额，加 11 个冻结类别 | 保持 15 类和每类样本不变，同时暴露粗领域轴 |

### 2.3 split 与统计行

- 一行是一条完整 utterance 在一个冻结 prompt token 的表征；
- TRAIN 学所有 residualizer、standardizer、PCA/监督/null 子空间和读出器；
- validation 为每个冻结维数选择正则；
- TEST 只在 freeze receipt 通过后打开一次；
- 主 bootstrap 在用户意图类别内重采样语句，再对 domain 等权汇总；冻结 2,000 次；
- 保留官方 split。可报告 TEST 到最近 TRAIN 的词面相似度分层，但不得删除样本或改变主裁定。

## 3. 数据条件构造

### 3.1 `global_150`

全部 150 个域内用户意图类别。计算总体 covariance 和功能曲线作上下文。因类别数和行数不同，不能制造 Q1 Pass。

### 3.2 `within_domain_15`

10 个任务。每个 domain 含 15 个用户意图类别及全部官方样本，因此每个任务有 1,500/300/450 条 TRAIN/validation/TEST。

### 3.3 `matched_cross_domain_15`

对每个目标 domain $d$，使用基础 seed `8180601`，从其余 9 个 domain 冻结 64 个几何集合。每个集合含 15 个用户意图类别；在 seed 冻结的 domain 顺序下，来源计数为 $(2,2,2,2,2,2,1,1,1)$，任何源 domain 最多 2 类。每类仍使用 100/20/30 条样本。

约束：

- 排除目标 domain 的用户意图类别；
- 不允许集合内类别重复；
- 64 次中各类别的暴露次数尽量组合平衡并审计；
- 选择集合时禁止使用 activation、标签难度、TEST 指标或 spectrum；
- 每个目标 domain 预先冻结的前 16 个集合做次要功能曲线；64 个集合全部做几何分析。

## 4. 模型、prompt、token、层与 shape

- 模型：冻结 `/data/share/Qwen3-8B`；
- 预期 36 blocks、hidden width $d=4096$，实现必须验证；
- forward：eval/inference、`use_cache=False`、记录确定性 attention backend、bfloat16 前向、分析数组转 float32；
- prompt：

```text
Utterance: <utterance>
Category:
```

- 不把 gold domain 或用户意图类别写进 prompt；
- token：字面后缀 `Category:` 的最后一个非 padding token；记录 token IDs，并要求冻结 tokenizer 下只有一个无歧义出现；
- 层：人类编号为 1-based block 24、28；实现收据必须写出精确 module index。

对含 $n$ 条数据的 split：

| 对象 | shape |
| --- | ---: |
| $h,a,X,Z,U,R_U$ | $n\times4096$ |
| domain 内 15-way centered target | $n\times15$ |
| 低维投影 $P_r$ | $4096\times r$ |
| $R_UP_r$ | $n\times r$ |
| domain-specific logits | $n\times15$ |

强制 identity 包括：native post-Attention MLP input 与 $Z$、$U=Z-X$、hook 覆盖、重复 batch 确定性、sample order、prompt token、有限值。系统性失败使该层失格。

## 5. 残余化与标准化

$$
X=N(h),\qquad Z=N(h+a),\qquad U=Z-X.
$$

只用 TRAIN 拟合 feature 均值/尺度。使用 5 个按用户意图类别分组的 TRAIN folds，从 $X$ 到 $U$ 拟合仿射多输出 ridge。每个 TRAIN 行必须得到 out-of-fold 预测。validation 从下列无量纲 grid 选 residualizer：

$$
\alpha\in\{10^{-6},10^{-5},10^{-4},10^{-3},10^{-2},10^{-1},1,10\},
$$

$$
\lambda=\alpha\,\operatorname{tr}(C_{XX})/d.
$$

用完整 TRAIN 重拟合后，原样应用到 validation 与 TEST：

$$
R_U=U-(XB+b).
$$

残余化不得使用 domain 或用户意图标签。报告 TRAIN out-of-fold 与 validation/TEST reconstruction $R^2$。无论拟合多好，结论都只限定在线性族内。

## 6. 几何分析

### 6.1 Spectrum

每个 block/condition 只用 TRAIN 均值中心化，计算无偏 covariance。令 $m=\min(n_{train}-1,4096)$，非负特征值降序为 $\lambda_j$：

$$
r_q^{var}=\min\left\{r:\frac{\sum_{j\le r}\lambda_j}{\sum_{j\le m}\lambda_j}\ge q\right\},
\quad q\in\{0.8,0.9\}.
$$

报告 $r_{90}^{var}/m$、熵有效秩、头部占比、trace 和累计曲线。只裁掉数值误差导致的负特征值，并报告裁剪质量。

PCA 尾部 $r$ 维指 TRAIN 可识别的正谱内最后 $r$ 个方向，不得偷用任意零空间方向。

### 6.2 用户意图类别内/间分解

对每个 15 类任务：

$$
\Sigma_{total}=\Sigma_{类别内}+\Sigma_{类别间}.
$$

分别报告两部分的谱和 trace。若 matched effect 完全由用户意图类别内 nuisance covariance 改变解释，Q1 不得写成语义子空间并集证据。

### 6.3 局部方向稳定性

主方向预算冻结为 $r_0=8$，$r_0\in\{4,14\}$ 只作次要。把 TRAIN 按用户意图类别分层拆成两半，每半每类 50 行；独立学习局部监督广义特征子空间。对正交基 $P,Q$：

$$
O(P,Q)=\frac1{r_0}\|P^\top Q\|_F^2.
$$

主方向 gap：

$$
\Delta_{orient}=
\operatorname{median}_d O(P_d^A,P_d^B)-
\operatorname{median}_{d\ne d'}O(P_d,P_{d'}).
$$

### 6.4 并集增长

对十个稳定局部 $r_0$ projectors，按冻结 domain 顺序构造：

$$
M_k=\sum_{d\in S_k}P_dP_d^\top,
$$

计算 $M_k$ 的熵有效秩。将 $k=10$ 的实际并集与 1,000 个“对同一 domain 做十次独立 split/bootstrap 估计”的并集比较，以区分方向差异与估计噪声。

### 6.5 Q1 阈值

$$
\Delta_{rank}=\operatorname{median}_{d,s}
\left[
\widetilde r_{90}^{cross(d,s)}-
\widetilde r_{90}^{within(d)}
\right],\qquad \widetilde r=r/m.
$$

`LOCAL_UNION_SUPPORTED` 必须同时满足：

1. $\Delta_{rank}$ 的同时 95% LCB 大于 0，点估计至少 0.05；
2. $\Delta_{orient}$ 的同时 95% LCB 大于 0，点估计至少 0.10；
3. $k=10$ union effective rank 超过 same-domain union null 的 q95；
4. 对明确合格层，projector/test capture、covariance trace 与两层多重比较 guard 通过。

秩集中通过但方向/并集失败，记 `LOCAL_CONCENTRATION_ONLY`；$\Delta_{rank}$ 的 95% UCB 不大于 0，记 `NO_LOCAL_CONCENTRATION`；区间居中未决，记 `GEOMETRY_INSUFFICIENT`。

## 7. 功能准入与秩曲线

### 7.1 冻结 $X$ baseline

对每个 domain/block，从标准化 $X$ 用 TRAIN 拟合 15-way centered-one-hot ridge；TRAIN logits 必须 out-of-fold。validation 选 penalty，随后冻结 validation/TEST base logits。

domain 只负责选择 readout head，不作为预测目标，也不写进 prompt。

### 7.2 full 与 null correction

所有 branch 复用 bit-identical base logits。correction target 是 centered one-hot target 减 TRAIN out-of-fold base logits。

- `true_full_ru`：正确配对的标准化 $R_U$；
- `duplicate_x`：同拟合族的第二个标准化 $X$ branch；
- `mismatch_ru`：64 个冻结 seed 的 domain 内、不同用户意图类别错配；可行时按长度 decile 匹配；每个 split 独立构造，不跨 split。

主 full gain 是 domain 等权的 TEST CE 降低。null envelope 为 duplicate-$X$ gain 与 mismatch q95 的较大者。H-ADMIT 仅在 true gain 减 envelope 的同时 95% LCB 大于 0 时通过。两层都不通过时，Q2=`INSUFFICIENT_NO_FULL_GAIN`。

### 7.3 候选子空间

冻结秩 grid：

$$
r\in\{1,2,4,8,16,32,64,128,256,512\}.
$$

每个秩比较：

1. 所有 domain 的 TRAIN $R_U$ 构成的 PCA 头部；
2. TRAIN 可识别 PCA 尾部；
3. 64 组 TRAIN 冻结的嵌套 Haar 随机空间；
4. 监督降秩岭回归空间；
5. 64 个用户意图标签置乱后重学的监督降秩岭回归空间；
6. full $R_U$。

监督方法固定为 reduced-rank ridge regression（监督降秩岭回归，RRR）。对每个功能任务，令 $T_{corr}$ 为 centered target 减去 TRAIN out-of-fold $X$ 基线 logits，拟合：

$$
\min_{P_r^\top P_r=I,\,A_r}
\|T_{corr}-R_UP_rA_r\|_F^2+\lambda\|A_r\|_F^2.
$$

$P_r\in\mathbb R^{4096\times r}$ 是可学习输入投影，$A_r$ 是可学习修正头，因此 $P_rA_r$ 是 rank 至多为 $r$ 的线性低秩模块。实现使用 TRAIN 上的闭式监督降秩岭解（ridge whitening 后对目标交叉协方差做截断 SVD），并用小矩阵直接优化核对目标值。validation 为每个 $r$ 选择：

$$
\lambda=\alpha\,\operatorname{tr}(R_U^\top R_U)/d,
\qquad
\alpha\in\{10^{-6},10^{-5},10^{-4},10^{-3},10^{-2},10^{-1},1,10\}.
$$

监督降秩岭回归对每个条件分别学习，直接回答“这个 $R_U$ 能否被低维投影保留”。跨十个 domain 共用一个 $P_r$ 另作稳健性分析，不参与功能秩定义，也不得替代主曲线。

每个随机 seed $s$ 先由高斯矩阵 QR 分解得到 $Q_s\in\mathbb R^{4096\times512}$；第 $r$ 个点固定使用 $P_{s,r}=Q_s[:,1:r]$。所以同一 seed 的各维数严格嵌套，构成一条可解释的随机曲线，而不是每个维数重抽一个无关空间。图中绘制 64 条细灰线、随机中位数虚线和 5%—95% 阴影带。

full 与所有投影 branch 必须使用相同标准化、base logits、target、正则 grid 与评价代码。类别数 $C$ 不进入 rank 定义、阈值、归一化或 Pass 条件。

### 7.4 Q2 阈值

对 $\eta\in\{0.8,0.9\}$ 定义：

$$
r_{func}(\eta)=\min\{r:G_r\ge\eta G_{full}\}.
$$

TEST 只有在以下条件满足时，才给出 `FUNCTION_RANK_80_90_ESTIMATED`：

1. 该 block/condition 的 H-ADMIT 通过；
2. 对每个阈值，报告首次满足点估计的候选秩；
3. 只有 $G_r-\eta G_{full}$ 的同时 95% LCB 大于 0，才把该秩标为“确认达到”；
4. 同时报告该秩相对 64 条随机曲线的分位数和 $G_r-q_{0.95}(G_{Haar,r})$ 区间；
5. identity、split、finite-value、headroom 与 matched-fitting guards 全通过。

若冻结 grid 内没有达到某个阈值，该阈值的功能秩记为 `>512`；若 full gain 未准入，记 `NA`；区间跨线时保留点估计但标记 `UNCERTAIN`。不能用固定 $r\le32$ 或类别数救回结论。

投影 gain 可能因正则化超过 full gain。比例大于 1 应照实报告，但不能解释为包含更多信息；必须做 matched fitting audit。

### 7.5 各数据条件的诊断曲线

为了完整覆盖截图中的所有条件，同时不改变主裁定：

- `global_150` 拟合一个 150-way $X$ baseline，以及 matched full/PCA 头/PCA 尾/Haar/监督降秩岭回归曲线，只作描述；
- 每个 `within_domain_15` 任务绘制 PCA 头/PCA 尾/64 条嵌套 Haar/full/监督降秩岭回归曲线；
- 每个目标 domain 预先冻结的前 16 个 `matched_cross_domain_15` 集合绘制相同的 15-way 曲线，每个集合使用自己的 readout，不使用 domain selector。

每张功能图必须同时呈现：绝对 $G_r$ 曲线、$0.8G_{full}$ 和 $0.9G_{full}$ 两条水平线、PCA 头/尾、监督降秩岭回归、64 条随机细线及其中位数/5%—95% 带、full $R_U$ 水平线。另附 retention 曲线 $G_r/G_{full}$，明确标记 $r_{func}(0.8)$ 与 $r_{func}(0.9)$。

对 local-versus-cross 功能比较，报告达到各自已准入 full gain 的 80% 和 90% 所需秩分布。因为两边标签任务不同，它只作次要比较；只有两边 full gain 均超过匹配 null 时才有定义。类别数和样本数必须成对一致；无 full gain 显示为 `NA`，不得用 accuracy 填补或救回。

## 8. 非线性旧状态重编码诊断

每个 domain 拟合一个由 validation 选择的两层 $X$-only MLP，其参数预算不大于 full-$R_U$ correction family。它是次要诊断。若它关闭线性 $R_U$ gain，记录 `NONLINEAR_X_RIVAL_CLOSES_GAP`，并把措辞限定为“线性可访问性”；这不取消线性 gating 测量，也不证明/否定 Shannon 新信息。

## 9. 统计与多重比较

- bootstrap：2,000 次用户意图类别内语句重采样，domain 等权；
- block 24/28：TEST 前冻结 max-$t$ simultaneous intervals 或 Holm-corrected paired intervals；
- geometry sets、ranks、random seeds 在读取表征结果前冻结；
- 所有 rank 曲线给同时区间；80%/90% 阈值的首次交点承担 Q2 裁定；
- 必须报告 effect size 和区间，不能只报 accuracy；
- macro accuracy、macro-F1、校准和 $R_U$-only accuracy 为次指标，不得覆盖 CE-gain verdict。

## 10. Guard 与停止条件

打开 TEST 前的硬停止：

1. 官方数据/hash/count 或 10×15 映射失败；
2. TRAIN/validation/TEST 重复或 sample-ID overlap；
3. prompt token 歧义或 hook identity 失败；
4. 非有限矩阵、covariance trace 可忽略或 eigensolver 不一致；
5. residualizer 泄漏或缺少 TRAIN out-of-fold prediction；
6. 使用 TEST 选择任何 subspace、rank、regularizer、layer 或 matched set；
7. correction branches 的 base logits 不一致；
8. 可构造 derangement 时 null 仍有固定行，或非法跨 split/domain；
9. full/projection 没有 matched fitting code path；
10. 调试期间已经打开 TEST。

TEST opening 需要机器可读 freeze receipt，包含 data/model/token hashes、sample lists、domain map、seeds、residualizer choices、candidate bases、rank selection、base logits、null maps 与 analysis version。

## 11. 必须产出的图表与白话读法

### 三张决策图

1. **匹配几何与并集图：**within/cross 归一化 $r_{90}$、局部稳定/跨 domain 重合、union growth；
2. **新增收益—秩图：**$X$ baseline、PCA 头/尾、64 条嵌套随机细线及其 band、监督降秩岭回归、full $R_U$，并标 $0.8G_{full}$、$0.9G_{full}$ 两条线；
3. **结论矩阵：**block 24/28 的 geometry verdict × functional verdict，包含 null excess 与边界。

### 必须表格

- 数据/domain/用户意图类别/split 数量与 hash；
- matched-set manifest 与平衡审计；
- residualizer 和 identity receipt；
- total/within/between covariance 指标；
- local overlap 与 union-null；
- base/full/duplicate/mismatch gains；
- 全部 rank/method gains 与 validation 选择；
- 每 domain gain、非线性 rival、typed verdict。

白话解释：

- covariance spectrum 是“这团点占了多少根轴”；
- matched within/cross 是“任务大小不变，只改类别是否来自同一 domain”；
- 主角/子空间 overlap 是“局部的轴到底是不是不同”；
- PCA 头是“动作最大”的轴，不保证是“分得最好”的轴；
- 监督降秩岭回归让 TRAIN 标签直接学习一个低秩投影和修正头；
- full $R_U$ 只有先超过 duplicate/mismatch，才有资格当功能 ceiling；
- TRAIN 学、validation 决策、TEST 一次裁定。

### 两个实验的白话版 1—2—3

**实验一：总体宽谱是不是多个局部子空间拼起来的**

1. 取 block 24、28 的 $R_U$，做两组一样大的任务：一组 15 类都来自同一领域，另一组 15 类来自多个领域。
2. 看同领域的谱是否更窄，再看各领域的低维方向能否重复、领域之间是否不同，以及多个领域合起来时维数是否增长。
3. 三件事同时成立，才支持“多个局部子空间共同造成总体宽谱”；任何一件不成立，都按预注册失败类型报告。

**实验二：把 $R_U$ 压到多少维还够用**

1. 先验证完整 $R_U$ 真能补充只用 $X$ 时缺失的分类收益，并排除重复 $X$ 或错配 $R_U$ 也能带来同样收益。
2. 在十个冻结维数上分别比较 PCA 头部、PCA 尾部、64 条嵌套随机子空间，以及监督降秩岭回归学到的低秩模块。
3. 把每条曲线和 $0.8G_{full}$、$0.9G_{full}$ 两条线相交的位置读出来；第一次达到阈值的维数就是对应经验功能秩。

## 12. 阶段合同与资源上限

| 阶段 | 目的 | gate/output |
| --- | --- | --- |
| review | 人工确认 A–G | 批准 amendment；否则停止 |
| preflight | 验证 data/model/mapping/prompt | hashes、counts、token、architecture receipt |
| unit tests | 验证公式/估计器 | hooks、covariance、RRR、null 红到绿 |
| smoke | 每 domain 2 个用户意图类别、小样本，仅 TRAIN/validation | 全 branch identity；不碰 TEST |
| extraction | 固定 block 24/28 的全部官方 rows | manifest 与 split hashes |
| fit/freeze | residualizer、conditions、各维数 bases、nulls、base logits | freeze receipt |
| TEST | 一次不可变评价 | row metrics 与 typed verdict |
| rendering | 规范证据 | summary、detailed、tables、三张图 |

冻结资源：ACP 单节点 `8×5090`，资源档位 `5090-8-spot`（`share-space` / `computing-cluster-5090-01g` / `n12lp.nn.i10a.8` / spot / normal），最多 32 CPU workers、256 GiB RAM、40 GiB 新存储、24 小时 wall time。先提交只读硬件与挂载 smoke；只有实际看到 8 张 5090、模型和数据挂载都正确才进入正式任务。batch size 可因工程原因修改，但必须重做 identity；第一次合格 extraction 后，不得改变数据、层、prompt、对象、阈值、集合或指标，也不得擅自换成其他 GPU 档位。

批准后的预期代码路径：

```text
Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/
a15_08_06_e01_clinc150_semantic_conditioned_functional_subspace/
```

批准后的预期 raw run 路径：

```text
/data/250010109/MoE_Router/experiments/
20260818_a15_08_06_e01_clinc150_semantic_conditioned_functional_subspace/runs/
```

路径本身不构成写代码或运行授权。

## 13. 结果能说明与不能说明什么

`LOCAL_UNION_SUPPORTED` 只能说明不同的稳定局部子空间对宽几何有贡献，不能证明它们是主要来源。`FUNCTION_RANK_80_90_ESTIMATED` 只能说明指定低维投影在未见数据上保留了 80%/90% 的用户意图新增可访问性，不能说明模型或 Router 原生使用它。监督优于 PCA 只证明用户意图分类目标上的 objective mismatch。若后续另行批准，真正 Router 实验必须用 expert-relative utility 或 update-compatibility 替代用户意图标签，并保持 Top-$K$、容量和预算匹配。
