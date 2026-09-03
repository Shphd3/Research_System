# Protocol：A15_08_06_E03 粗类—细类学科数据复现

## 0. 审批快照

- **文档状态：**`APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN`。
- **审批状态：**用户于 2026-08-19 明确要求按 0817 统计口径重跑两个实验，并在随后上传的实验一步骤图中确认 H-GEO 构造；A–G 全部为 `CONFIRMED`，跨块一致性为 `PASS`。
- **已批准执行范围：**实现、TRAIN/DEVELOPMENT smoke、单节点 `8×5090` SPOT 正式运行、一次性打开新 CONFIRMATION-v3、结果分析与项目内报告。未批准 commit、push、root sync 或外部发布。
- **冻结时间与注册版本：**`2026-08-19T12:00:00Z`；`a15_08_06_e03-r1`。
- **目的：**在此前 8 个粗类 × 每粗类 8 个细类的平衡学科数据上，复现 A15_08_06 的两个问题：局部细类子空间是否共同造成宽几何，以及 $R_U$ 的分类增益能否由低维投影保留。
- **主 Anchor：**`15_08_06_semantic_conditioned_functional_subspace`。
- **实验角色：**数据集稳健性复现；不取代 CLINC150 主实验，也不把合成数据结果外推到真实用户请求。
- **主对象：**冻结 Qwen3-8B block 24、28 的 $X$、$U$ 与重新拟合的线性残余 $R_U$。
- **最小设置：**8 个已知粗类条件下的 8-way 细类任务；与其规模完全相同的跨粗类 8-way 任务；TRAIN/DEVELOPMENT 各 640 行；新建、一次性打开的 CONFIRMATION-v3 为 640 行。
- **处理与对照：**同粗类与跨粗类几何；full-$R_U$、duplicate-$X$、错配-$R_U$、非线性 $X$ 对照；PCA 头/尾、64 条嵌套 Haar 随机子空间、监督降秩岭回归和 full-$R_U$。
- **改变变量：**类别是否来自同一粗类，以及 $R_U$ 投影方法与维数。
- **保持不变：**模型、prompt、decision token、block、每任务类别数、每类样本数、数据 split、读出器族、正则网格和评价代码。
- **主几何指标：**同粗类/跨粗类的归一化 $r_{90}^{var}$ 差、局部方向稳定性差、8 个局部子空间的并集有效秩相对同粗类零假设。
- **主功能指标：**粗类等权的未见数据交叉熵增益；只有 full-$R_U$ 先通过准入，才读取 $0.8G_{full}$ 和 $0.9G_{full}$ 的首次确认交点。
- **Pass：**几何三项合取通过；功能上 full-$R_U$ 超过匹配 null，且冻结投影曲线在同时区间下达到相应保留阈值。
- **Fail：**效应方向相反或同时上界不超过注册边界。
- **Insufficient：**新确认集不新鲜、full gain 未准入、区间跨阈值、样本/身份/拟合守卫失败。
- **不能 claim：**语义内禀秩、非线性新信息、模型原生使用、expert utility、Router 改进、专家专门化或遗忘减少。
- **本轮审批决策：**实验一严格按用户图片的三项合取执行；实验二恢复 0817 的样本级标签独立 mismatch，并把 H-ADMIT 与探索性曲线分成两个统计族。已确认新建 CONFIRMATION-v3，RRR 只承担监督任务子空间读数，不能单独承担表征低秩结论；采用 `5090-8-spot` 资源档位完成正式运行。

## 1. 术语与对象

对 block $\ell$：

$$
X_\ell=N_\ell(h_\ell),\qquad
Z_\ell=N_\ell(h_\ell+a_\ell),\qquad
U_\ell=Z_\ell-X_\ell,
$$

$$
R_{U,\ell}=U_\ell-\widehat{\mathbb E}_{lin}[U_\ell\mid X_\ell].
$$

- **粗类：**mathematics、physics、biology、chemistry、computer science、economics、linguistics、medicine。
- **细类：**每个粗类下 8 个子领域；例如 mathematics 下的 algebra、analysis、combinatorics、geometry、number theory、probability、statistics、topology。
- **几何方差秩：**达到 90% covariance 方差所需的最小方向数 $r_{90}^{var}$。
- **功能保留维数：**投影后的未见数据增益达到完整 $R_U$ 增益的 80% 或 90% 所需的最小输入维数。
- **监督降秩岭回归（RRR）：**用 TRAIN 标签联合学习输入投影 $P_r$ 和修正头 $A_r$ 的线性低秩模块。
- **重要边界：**8-way centered target 的代数秩最多为 7。因此 RRR 在 7 维后饱和是方法/输出上界，不能单独证明 $R_U$ 表征只有 7 维。

## 2. Anchor 对齐

本实验不改变 Anchor 的问题，只更换为结构更严格但规模更小的粗类—细类数据，检验结论是否依赖 CLINC150。

测试的不确定性：

1. 宽 $R_U$ 几何是否可由多个稳定、彼此不同的粗类内细分类子空间的并集部分解释；
2. 在 full-$R_U$ 增益先通过准入后，固定低维输入投影能否在未见表达模板上保留该增益；
3. PCA 头部与监督任务方向是否一致。

最强替代解释：

- 跨粗类谱更宽只是粗类均值差，而非局部细分类方向不同；
- full-$R_U$ 提升只是额外参数容量、样本错配或 $X$ 的非线性重编码；
- RRR 的低维结果只是 8-way 输出秩上限，而非 $R_U$ 低维。

## 3. 可证伪假设

### H-GEO：局部子空间并集

先从所有 $R_U$ 中减去各粗类的 TRAIN 均值，但不减细类均值。只有以下三项同时通过，才记为 `LOCAL_UNION_SUPPORTED`：

1. 跨粗类 8-way 任务的归一化 $r_{90}^{var}$ 高于同粗类 8-way；
2. 同一粗类的监督判别子空间在重复 TRAIN 半切之间更相似，并且高于不同粗类子空间之间的相似度；
3. 8 个粗类子空间的并集有效秩超过“同一粗类反复重采样 8 次”的 q95。

### H-ADMIT：完整 $R_U$ 的功能准入

至少一个预注册 block 的正确配对 full-$R_U$，在新 CONFIRMATION-v3 上必须超过 duplicate-$X$ 和 64 个粗类内、样本级标签独立错配 $R_U$ 的 null envelope。错配只保持 split、粗类、样本数和边际细类频数，不强制来源细类不同；对任一目标细类，八种来源细类的次数差不超过 1，从而不能由来源细类反推目标标签。

### H-FUNC：低维功能保留

对 $\eta\in\{0.8,0.9\}$：

$$
r_{func}^{(m)}(\eta)=\min\{r:G_{m,r}\ge \eta G_{full}\},
$$

其中 $m$ 是 PCA 头、PCA 尾、Haar 或 RRR。每种方法单独报告交点；不使用类别数 8 直接判秩。

- **主表征压缩读数：**PCA 头部的交点及其随机对照超额，因为 PCA 不使用细类标签学习输入方向。
- **监督任务子空间读数：**RRR 交点，类型化为 `SUPERVISED_TASK_SUBSPACE`；即使很小，也不能单独写成表征低秩。

## 4. 替代解释与对应控制

| 替代解释 | 控制 | 若控制关闭差距时的结论 |
| --- | --- | --- |
| 跨粗类更宽只是粗类均值 | 几何主分析先减 TRAIN 粗类均值；未减均值只作诊断 | 不能写局部细分类子空间并集 |
| 类别数或样本数造成谱差 | 同粗类和跨粗类都固定 8 类 × 每类 10 行 | 构造失败则 H-GEO 不合格 |
| 方向差来自小样本噪声 | 200 次细类分层半切；同粗类重采样并集 null | 稳定性不过则不能 claim 稳定局部方向 |
| full gain 是额外容量 | duplicate-$X$ 修正分支，复用完全相同 base logits | H-ADMIT 失败 |
| full gain 不依赖正确样本配对 | 64 个粗类内、样本级标签独立且来源细类平衡的错配 $R_U$ | H-ADMIT 失败 |
| $R_U$ 只是 $X$ 的非线性重编码 | 参数预算不大于 full correction 的两层 $X$-only MLP | 结论限定为线性可访问性 |
| RRR 低维只是输出秩上界 | PCA/Haar/full 同图；RRR 单独类型化 | 不得用 RRR 单独宣布 $R_U$ 表征低秩 |

## 5. 数据构造与来源

### 5.1 已有数据

- 已验证来源：旧实验 `registered_taxonomy.json`，共 1,920 行；TRAIN、DEVELOPMENT、旧 CONFIRMATION 各 640 行。
- 每个 split 都是 8 个粗类 × 每粗类 8 个细类 × 每细类 10 行。
- 每行是由 3 条主题事实组成的英文“学科简介”，末尾统一询问粗类和细类，decision token 位于 `Classification:` 末端。
- 旧审计：标签词泄漏 0、归一化重复 0；旧 CONFIRMATION 使用 10 个新模板族和 5 个新事实子集。

示例：

1. “符号表达式、未知量方程、多项式和代数结构”对应 mathematics → algebra。
2. “叠加、非对易算符、离散能级和测量概率”对应 physics → quantum physics。

### 5.2 split 使用

- **TRAIN（640）：**拟合 residualizer、标准化、PCA/RRR/Haar/null、base 与 correction heads。
- **DEVELOPMENT（640）：**选择正则和冻结所有候选；不得改变假设或秩网格。
- **旧 CONFIRMATION（640）：**已经被 A15_08_02_E01 打开并用于裁定，本实验只允许作为带明确标签的回放诊断，不得再次叫“未见正式测试”。
- **CONFIRMATION-v3（640）：**8×8×10；使用相对既有 1,920 行和已经打开的 CONFIRMATION-v2 都未出现的模板族与事实子集；全局归一化重复、标签泄漏、record-ID overlap 必须为 0。

若无法构造同时满足“新模板族 + 新事实子集 + 无重复 + 无标签泄漏”的 640 行 CONFIRMATION-v3，正式功能实验硬停止；不得静默改用旧 CONFIRMATION。

### 5.3 同粗类与跨粗类条件

1. **Within-parent-8：**8 个任务；每个粗类内部 8 个细类，每任务每 split 80 行。
2. **Matched-cross-parent-8：**基础 seed `819060201`。对 batch $b=0,\ldots,7$，为每个粗类 $p$ 生成一个细类索引排列 $\pi_{b,p}$；第 $k$ 个集合为

$$
C_{b,k}=\{(p,\pi_{b,p}(k)):p=0,\ldots,7\}.
$$

共 64 个跨粗类任务；每个任务恰有 8 类、每类 10 行；每个粗类—细类单元跨 64 个任务恰出现 8 次。

- H-GEO 使用全部 64 个跨粗类任务。
- 次要功能比较只使用 $b=0$ 的 8 个互不重叠跨粗类任务，保证 64 个细类单元恰好各出现一次。
- 64 个任务不是 64 个独立样本；统计重采样基于原始粗类/细类/文本行，不把任务数当独立样本量。

## 6. 学习任务与允许的监督

### 6.1 实验一

- 输入：TRAIN 的 parent-centered $R_U$。
- 标签：细类标签，仅用于学习局部监督判别方向；不用于 covariance spectrum。
- 输出：谱指标、局部方向重合、并集有效秩。
- 局部方向方法：与 CLINC 实现一致的 diagonal-within-covariance LDA-style basis。对各细类均值差按 pooled within-class feature variance 白化，取前 7 个右奇异方向并 QR 正交化。
- 7 维只因 8 个中心化类均值最多有 7 个独立对比；它不是 $R_U$ 功能秩的判定。

### 6.2 实验二

- 主任务：粗类已知时预测该粗类内部的 8 个细类；粗类只选择 head，不作为预测目标，也不写入额外 prompt。
- 次要任务：8 个互不重叠的跨粗类 8-way 任务，每个任务独立拟合 readout。
- base 输入：标准化 $X$；correction 输入：标准化 $R_U$ 或其冻结投影。
- 目标：centered 8-way one-hot；主损失为每样本交叉熵。
- TEST/CONFIRMATION-v3 标签不得用于 residualizer、正则、子空间、rank、图范围或结论选择。

## 7. 模型、对象与冻结变体

- 模型：冻结 `/data/share/Qwen3-8B`，eval/inference，`use_cache=False`。
- 层：1-based block 24、28；必须记录精确 module index。
- hidden width：4,096；实现前再次验证。
- prompt：复用已有学科数据全文，并以 `Classification:` 结尾；不得换成 CLINC 的 `Utterance: ... Category:` prompt。
- decision token：冻结 tokenizer 下 `Classification:` 的最后一个非 padding token；已有抽取记录 token id 25，复用前必须以 hash 和 token receipt 核验。
- 已有 TRAIN/DEVELOPMENT 的 $X,U,Z$ 可在模型、数据、prompt、token、hook 和数组 hash 全部一致时复用。
- 旧 `R_U` 不直接复用：必须按本协议重新拟合 residualizer，以保证与当前 full/null/rank 曲线使用同一代码路径。
- 几何分析减粗类 TRAIN 均值；功能分支保留原始标准化 $R_U$，由 task head/intercept 处理常数项。

## 8. 目标函数与优化

### 8.1 Residualizer

只用 TRAIN 拟合仿射多输出 ridge $U\sim X$。5-fold 细类分层 OOF，每 fold 每个细类 2 行；DEVELOPMENT 选择：

$$
\alpha\in\{10^{-6},10^{-5},10^{-4},10^{-3},10^{-2},10^{-1},1,10\},
\qquad
\lambda=\alpha\,\operatorname{tr}(C_{XX})/4096.
$$

选定后用完整 TRAIN 重拟合并原样应用到 DEVELOPMENT 和 CONFIRMATION-v3。

### 8.2 Base 与 full correction

- 每个粗类拟合一个 8-way $X$-only ridge head；TRAIN logits 必须 OOF。
- correction target 是 centered target 减 TRAIN OOF base logits。
- `true_full_ru`、`duplicate_x`、`mismatch_ru` 和所有投影分支复用 bit-identical base logits、标准化、target 和正则网格。
- 非线性 $X$ rival：每粗类两层 MLP，hidden width 7、GELU；参数量不大于 4,096×8 full linear correction；只作诊断。

### 8.3 监督降秩岭回归

$$
\min_{P_r^\top P_r=I,A_r}
\|T_{corr}-R_UP_rA_r\|_F^2+\lambda\|A_r\|_F^2.
$$

TRAIN 使用 ridge-whitening 后的截断 SVD 闭式解；DEVELOPMENT 按与其他分支相同的 $\alpha$ 网格选择 $\lambda$。每个任务单独学习 $P_r$；跨 8 个粗类共享 $P_r$ 只作次要稳健性分析。

## 9. 条件、维数与随机性

### 9.1 冻结维数

$$
r\in\{1,2,4,8,16,32,64,128,256,512\}.
$$

全部方法使用同一 grid。由于每个主任务 TRAIN 只有 80 行，$r>79$ 的 readout 属于高维岭回归区；可以报告，但必须标注 `LOCAL_READOUT_SAMPLE_LIMITED`，并以区间而非点估计作裁定。

### 9.2 候选子空间

1. 所有 640 条 TRAIN $R_U$ 学到的 PCA 头部；
2. TRAIN 可识别正谱内的 PCA 尾部；
3. 64 个嵌套 Haar 随机空间；
4. 每任务监督 RRR；
5. 64 个细类标签置乱后重学的 RRR；
6. full $R_U$。

Haar 使用 seed `819060230 + s`，$s=0,\ldots,63$。每个 seed 先生成 $4096\times512$ 高斯矩阵并 QR；rank-$r$ 使用前 $r$ 列，因此一条随机曲线在维数上严格嵌套。

其他 seed：

- 200 次局部半切：`819060210 + t`；
- 1,000 次并集 null：`819060220 + t`；
- 64 个 mismatch：`819060240 + s`；每个 split、粗类内独立构造样本级双射，禁止 self-map，且每个目标细类接收的八种来源细类计数差不超过 1。禁止使用“每个目标细类只对应一个不同来源细类”的类别级置换。
- 2,000 次 bootstrap：root seed `819060250`。

## 10. 主指标与冻结分析

### 10.1 实验一

每个任务 $n=80$，可识别最大维数 $m=79$：

$$
\widetilde r_{90}=r_{90}^{var}/79,
$$

$$
\Delta_{rank}=\operatorname{median}_{64}\widetilde r_{90}^{cross}
-\operatorname{median}_{8}\widetilde r_{90}^{within}.
$$

局部方向固定 rank 7。对每个粗类做 200 次细类分层 5/5 半切。对正交基 $P,Q$：

$$
O(P,Q)=\frac1{7}\|P^\top Q\|_F^2,
$$

$$
\Delta_{orient}=\operatorname{median}O(P_p^A,P_p^B)
-\operatorname{median}_{p\ne q}O(P_p,P_q).
$$

8 个 full-TRAIN 局部 rank-7 bases 拼接后的奇异值平方用于计算并集熵有效秩。与 1,000 次“同一粗类独立 bootstrap 8 个 bases”的并集分布比较。

`LOCAL_UNION_SUPPORTED` 需要同时满足：

1. $\Delta_{rank}$ 同时 95% LCB > 0，且点估计 ≥ 0.05；
2. $\Delta_{orient}$ 同时 95% LCB > 0，且点估计 ≥ 0.10；
3. 实际 union effective rank > same-parent null q95；
4. 两个 block 的 identity、trace、数值和多重比较守卫通过。

### 10.2 实验二 full 准入

对每个粗类 $p$：

$$
G_{p}=CE_p(X\text{-only})-CE_p(X+\text{correction}),
$$

主增益 $G$ 是 8 个粗类等权平均，单位为 nats/样本。

null envelope 是 duplicate-$X$ gain 与 64 个 mismatch gain 的 q95 的较大者。H-ADMIT 是独立于探索性秩曲线的主准入统计族，只含 block 24、28 的以下两个预注册对比：

$$
G_{full}-\max(G_{dupX},q_{.95}G_{mismatch})
$$

两个对比用 max-$t$ 同时校正；某层的 95% LCB > 0 时该层通过。full gain 自身、所有秩、方法、随机对照和非线性 rival 的区间属于单独的探索/功能维数统计族，不得被并入 H-ADMIT 家族。未通过层的所有 80%/90% 功能秩记为 `NA`，理由写作“full-$R_U$ 未通过 matched-null 准入”，而不是“没有正收益”。

### 10.3 80%/90% 交点

每个方法、每层分别计算 $G_{m,r}-\eta G_{full}$。首次点估计交点必须再满足：

1. 同时 95% LCB > 0；
2. 相对 64 条同秩 Haar 曲线的分位数和超额区间被报告；
3. full 与投影分支的拟合代码路径、正则 grid 和 base logits 完全匹配。

若点估计达到但区间跨线，标为 `UNCERTAIN`；grid 内未达到记 `>512`；full 未准入记 `NA`。

### 10.4 统计单位

- 2,000 次层级 bootstrap；粗类等权，在每个细类内部重采样文本行/模板族。
- 64 个 cross tasks 在每次重采样中重新聚合，不当作 64 个独立观测。
- H-ADMIT 的两个 block 对比单独使用 max-$t$ simultaneous intervals。候选秩、方法、随机对照与 rival 使用另一个冻结的探索/功能维数 max-$t$ 家族；两个家族不得合并。
- 不删除 outlier；非有限值、缺行或失败分支使相应层/条件不合格。

## 11. 次要指标与守卫

- covariance total/within-class/between-class 分解；重构相对误差必须 ≤ $10^{-6}$。
- 未减粗类均值的 spectrum 仅用于判断粗类偏移量有多大，不参与 H-GEO Pass。
- macro accuracy、macro-F1、校准、$R_U$-only accuracy 只作诊断，不得救回 CE-gain Fail。
- DEVELOPMENT/CONFIRMATION-v3 的 TRAIN projector 方差 capture；低 capture 使几何方向外推记为 Insufficient。
- RRR 若在 $r\le7$ 饱和，只能写“监督线性 8-way 修正可由至多 7 个判别坐标表达”；不能写“$R_U$ 是 7 维”。
- 旧 CONFIRMATION replay 的任何数字必须标 `RETROSPECTIVE_ONLY`，不得与新确认结果合并成更窄区间。

## 12. 已知好例、坏例与易混淆例

- **已知好例：**旧 A15_08_02_E01 在 block 24/28 的 full-$R_U$ 条件细分类增益超过当时 duplicate/mismatch null；仅说明本迁移有可测 headroom，不预注册正结果。
- **已知坏例：**将同一粗类任务反复重采样后得到的多个子空间不应制造明显 union growth。
- **易混淆例：**不减粗类均值时，跨粗类谱可能变宽；这只能说明粗类偏移，不是局部细类方向并集。
- **易混淆例：**RRR rank 7 达到 90% 并不自动胜过 PCA rank 256；二者回答“监督任务充分统计量”和“标签无关坐标压缩”两个不同问题。

## 13. 科学步骤与阶段合同

| 阶段 | 目的 | 输入/操作 | 通过与停止 | 输出/交接 |
| --- | --- | --- | --- | --- |
| review | 冻结迁移设计 | 本 Protocol A–G | 全部人工确认前停止 | `DESIGN_CONFIRMED_NOT_EXECUTABLE` |
| data preflight | 验证旧数据与新确认可构造 | taxonomy、模板、事实集、重复/泄漏审计 | 任一 count/hash/freshness 失败即停 | data receipt |
| activation reuse audit | 判断哪些旧数组可安全复用 | 模型/prompt/token/hook/array hashes | 不一致则不复用，需重新抽取 | reuse manifest |
| unit/smoke | 验证估计器和分支身份 | 仅 TRAIN/DEVELOPMENT 小样本 | TEST 不得出现；identity 全过 | smoke receipt |
| train/dev fit | 拟合 residualizer、bases、heads、nulls | 旧 TRAIN/DEVELOPMENT | 所有选择冻结 | freeze receipt |
| geometry | 裁定 H-GEO | TRAIN 主分析，DEV 外推 guard | 三项 typed verdict | geometry tables/figures |
| new extraction | 提取 CONFIRMATION-v3 的 block 24/28 | 已冻结新数据与模型 | 只在正式执行批准后 | test activation manifest |
| one-shot confirmation | 裁定 H-ADMIT/H-FUNC | 冻结代码、配置、曲线 | 不允许结果后改阈值 | row metrics/verdict |
| rendering | 生成可审计图表 | 冻结结果表 | 轴、图例、数值一致 | summary/detailed/figures |

## 14. 算法、产物与来源合同

拟议实现路径：

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/
MoE_Routing_Experiments/active/
a15_08_06_e03_aligned_hierarchical_taxonomy_replication/
```

拟议 raw run 路径：

```text
/data/250010109/MoE_Router/experiments/
20260819_a15_08_06_e03_aligned_hierarchical_taxonomy_replication/
```

必须产出：

1. 数据、split、模板、事实子集、prompt/token、模型和数组 hash 表；
2. 复用/重抽取 manifest；
3. residualizer OOF 与 DEVELOPMENT 选择表；
4. within/cross spectrum、200 次方向稳定性和 union-null 表；
5. full/duplicate/mismatch/非线性 $X$ gain 表；
6. 每层每方法每秩的增益与同时区间；
7. 三张主图：匹配几何、增益—维数、typed verdict matrix；
8. `summary.md`、`detailed.md` 和机器可读 artifact manifest。

主图合同：

- **匹配几何图：**横轴为 within/cross 或粗类数量 $k$；纵轴分别为归一化 $r_{90}$、projector overlap、union effective rank；灰色为 same-parent null。
- **增益—维数图：**横轴为投影维数（log2）；纵轴为相对 $X$ baseline 的 CE gain（nats/样本）；画 full、$0.8G_{full}$、$0.9G_{full}$、PCA 头/尾、RRR、64 条灰色 Haar 曲线及 5%–95% 带。
- **结论矩阵：**横轴为 block 24/28，纵轴为 H-GEO、H-ADMIT、PCA 功能保留、RRR 监督任务子空间；单元格显示 typed verdict 和关键区间。

## 15. Pass / Fail / Insufficient 映射

### 实验一

- `LOCAL_UNION_SUPPORTED`：集中、方向、并集三项合取通过。
- `LOCAL_CONCENTRATION_ONLY`：谱收窄通过，但方向或并集失败。
- `NO_LOCAL_CONCENTRATION`：$\Delta_{rank}$ 同时 95% UCB ≤ 0。
- `GEOMETRY_INSUFFICIENT`：区间未决或身份、trace、稳定性外推 guard 失败。

### 实验二

- `FUNCTION_RANK_80_90_ESTIMATED`：H-ADMIT 通过，PCA 的 80%/90% 首次确认交点可识别，并超过随机对照。
- `SUPERVISED_TASK_SUBSPACE_ONLY`：H-ADMIT 通过，RRR 达阈值，但 PCA 未确认；只支持监督 8-way 修正可压缩。
- `FULL_GAIN_BUT_THRESHOLD_NOT_REACHED`：full 准入，但冻结 grid 内某阈值未达到。
- `INSUFFICIENT_FULL_NOT_ADMITTED`：full-$R_U$ 可能有正收益，但未确认超过 matched null；所有正式功能秩 `NA`。
- `FUNCTION_INSUFFICIENT_GUARD`：新确认不新鲜、区间跨阈值、分支不匹配或其他硬守卫失败。

## 16. 不能声称什么

即使两个实验都通过，也只能说明：在此平衡合成学科数据、Qwen3-8B block 24/28 和指定线性分析族内，粗类条件化与 $R_U$ 的几何/细分类增益压缩之间存在注册关系。

不能声称：

- 自然语言语义本质上是低秩的；
- $R_U$ 是 Shannon 意义的新信息；
- Qwen 或其 MLP 原生使用这些低维方向；
- PCA/RRR 方向就是 Router 应使用的方向；
- expert utility、专家专门化、持续学习或永不遗忘得到改善；
- 合成模板结果等同于真实用户语句结果。

## 17. 块确认、冻结与变更台账

| 块 | 内容 | 状态 | 待审核的决定性选择 |
| --- | --- | --- | --- |
| A | 问题、假设、claim boundary | `CONFIRMED` | 作为 CLINC 的稳健性复现，不扩张到 Router |
| B | 数据构造与来源 | `CONFIRMED` | 新建未见 CONFIRMATION-v3；旧确认仅回放 |
| C | 任务与监督 | `CONFIRMED` | 主任务为已知粗类的 8-way 细分类；RRR 类型化 |
| D | 模型与对象 | `CONFIRMED` | Qwen3-8B、block 24/28、旧 X/U 可审计复用、$R_U$ 重拟合 |
| E | 目标与优化 | `CONFIRMED` | 5-fold OOF ridge、统一正则网格、RRR 闭式解 |
| F | 比较与判据 | `CONFIRMED` | H-GEO 三项合取；H-ADMIT；PCA 主压缩读数、RRR 监督 oracle |
| G | 执行与复现 | `CONFIRMED` | 单节点 `5090-8-spot`；实现、smoke、full run 与项目内报告已授权 |

跨块一致性：`PASS`。数据层级、监督边界、任务输出、模型对象、目标函数、对照、主指标、确认隔离、资源与产物可共同构成一个可裁定实验。

审批生命周期：

```text
DRAFT_NOT_EXECUTABLE
-> A–G 全部 CONFIRMED 且一致性 PASS
-> DESIGN_CONFIRMED_NOT_EXECUTABLE
-> 另行明确批准 implementation / smoke / full run
```

任何执行开始后的数据、方法、阈值、确认边界或结论规则变更，必须追加 amendment 并说明结果资格影响，不能静默覆盖本协议。

## 18. 执行前实现回执：CONFIRMATION-v3 事实数分布

- **回执 ID：**`a15_08_06_e03-r1-implementation-01`；记录于 2026-08-19，在任何 CONFIRMATION-v3 表征或结果被打开之前。
- **发现：**旧 TRAIN、DEVELOPMENT 与旧 CONFIRMATION 已共同用完 6 条事实的全部 $\binom{6}{3}=20$ 个三事实子集；已打开的 CONFIRMATION-v2 又在每个单元使用 5 个二事实子集及其 5 个四事实补集。每个单元仍剩 10 个未用二事实子集及其 10 个四事实补集，足以构造一次新的平衡确认。
- **实现：**先从每个单元排除既有 1,920 行和 CONFIRMATION-v2 的全部事实子集，再固定选择 5 个剩余二事实子集及其 5 个四事实补集。使用 10 个 v3 专属模板族，并保持每单元 10 行、全局 640 行、无标签词泄漏、无归一化文本重复、无 record-ID overlap。
- **不变项：**模型、prompt 结尾、decision token、类别/样本平衡、TRAIN/DEVELOPMENT、秩网格、控制、阈值、统计规则与一次性打开流程均不变。
- **资格影响：**该确认集比旧三事实数据多了一项“每行事实数变化”的分布移位。结果仍可裁定本协议的未见表达稳健性，但报告必须写成“在新模板和二/四事实表达移位下”；不得写成与旧 split 完全同分布的重复测量。

## 19. E02 后验发现与 E03 前置修正

- E02 的 mismatch 使用了细类级不同类置换；来源细类与目标细类一一对应，控制分支可学到反标签信息，因而不是 0817 的标签独立错配。
- E02 把 H-ADMIT 两个主对比与约 200 个秩/方法/随机/rival 对比放进同一个 max-$t$ 家族，导致准入临界值被探索性曲线数量放大。
- E03 在打开 CONFIRMATION-v3 前修正上述两点；不改 H-GEO 数据构造、阈值、秩网格、模型、block 或功能定义。E02 结果保留原样，不被覆盖。
