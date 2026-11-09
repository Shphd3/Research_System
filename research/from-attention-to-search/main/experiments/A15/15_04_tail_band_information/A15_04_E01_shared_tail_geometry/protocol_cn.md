---
experiment_id: A15_04_E01_shared_tail_geometry
anchor_id: 15_04_tail_band_information
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN
canonical_language: en
companion_language: zh
created: 2026-08-09
revised: 2026-08-09
---

# Protocol 审核稿：晚层语义方差是否进入共享 F9--F16 参数 tail？

英文主协议：[protocol.md](protocol.md)。问题来源：[A15_04 中文 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_04_tail_band_information/15_04_tail_band_information_anchor_cn.md)。

## 0. 审批快照

- **文件状态：**`APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN`。
- **冻结版本：**`A15_04_E01_r1`，于 `2026-08-09T14:05:43Z`、实现和结果访问前冻结。
- **研究者已确认的频谱划分：**16 个连续等宽频谱段，每段 256 个参数方向；F1=head，F2--F8=middle，F9--F16=tail。必须给出每个 band 和 H/M/T 三个广义区域的数据。
- **研究者已确认的范围：**只在 A15_02_06 的冻结样本上做几何检验；不删除 activation、不测任务 loss、不跑下游任务、不做 Router、不声称功能。
- **研究者确认的唯一主语义对象：**只用 conditional-fine 协方差；coarse 或复杂减简单统计不能进入或挽救 verdict。
- **唯一问题：**实际 attention 引起的 MLP 输入增量中，条件细类方差从早层到晚层是否更富集于全局跨层共享的广义 F9--F16 tail，并超过同维随机几何、F1 head 与 F2--F8 middle？
- **主处理：**只用另一奇偶互斥层组构造的全局广义共享 tail。
- **对照：**匹配的随机 16-band 正交分区、广义共享 head/middle、每个共享 F1--F16 band，以及每层本地频谱。
- **强制分层诊断：**每个 band 与 H/M/T 都测早层内部、晚层内部、早建空间到晚层、晚建空间到早层。它们只解释全局稳定、晚层形成或阶段重定向，不能替代全局主裁定。
- **固定不变：**Qwen3-8B、512 条样本、\(\Delta n\)、条件细类协方差、1--35 层裁定、第 36 层只描述、两组封存表达。
- **主统计量：**\(D_T=T_T-\max(T_H,T_M)\)；\(T_G\) 是全局共享广义区域的“捕获除以同维随机期望”从早层到晚层的变化。
- **Pass：**本地后移保留；广义 tail 富集为正、超过同维随机，且以 95% 下界超过 head/middle；层组和表达半集不反号。
- **Fail：**本地后移保留，但广义 tail 可由同维随机解释、不大于 head/middle，或只有本地参数秩变化。
- **Insufficient：** 原始 \(\Delta n\) 回放、本地现象、共享 tail 估计或分组可靠性不稳定。
- **关键来源修复：**旧文件只有 \(\Delta n\) 的本层特征坐标；已批准对相同 512 条样本回放一次，只补存原始 4096 维 \(\Delta n\)。
- **协议块：**A--G 全部 `CONFIRMED`；依据研究者 2026-08-09 对唯一主语义对象、四类共享几何、全局主裁定及直接完成实验的明确指令。
- **跨块状态：**`PASS`。
- **当前执行权限：**实现、确定性回放、工程 smoke、一次 full run、本地结果记录、Anchor 结果更新和今日 focus 更新；不授权发布、同步、commit 或 push。

## 1. 对象与术语

| 名称 | 直白含义 | 确切计算 | 不能证明 |
| --- | --- | --- | --- |
| 固定集合 \(S_0\) | 看结果前冻结，之后不能替换的文本 | A15_02_06 的 512 条平衡样本 | 整体语言分布 |
| \(\Delta n_\ell\) | 本层 attention 写入对本层 MLP 实际输入造成的变化 | \(RMSNorm_\ell(x_\ell+a_\ell)-RMSNorm_\ell(x_\ell)\) | 信息论意义的纯新增信息 |
| 条件细类协方差 \(B_{\ell,F}\) | 去掉每个大类均值后，小类中心之间的方差 | 八个大类、每类八个小类等权 | 粗细任务难度或非线性可读性 |
| F1--F16 | 本层 MLP 输入参数方向按增益由大到小排序后连续分成16段 | 每段256维 | 跨层同一向量身份 |
| head/middle/tail | 研究者固定的广义参数区域 | F1 / F2--F8 / F9--F16 | 功能模块 |
| 本地频谱 | 同一层内把方差投到相互正交的 F1--F16 | 每方向绝对方差与归一化份额，份额和为1 | 跨层共享方向 |
| 共享 band/区域 | 在其他层同一参数秩中最稳定的方向 | 另一层组本地投影平均后取指定秩 | MLP 使用 |
| 原始捕获 \(c\) | 总条件细类方差有多少比例落入某空间 | \(\operatorname{tr}(QB)/\operatorname{tr}(B)\) | 准确率或因果作用 |
| 维度归一化富集 \(e\) | 捕获相对同维随机空间平均值有多大 | \(e=c/(r/4096)\)，随机期望为1 | 总体统计显著性 |
| 随机频谱分区 | 一个随机正交基切成16段，再按相同规则合并 H/M/T | 一次抽样中的同一分区用于所有层 | 模型内部存在随机模块 |
| 互斥层组 | 一组只构造空间，另一组只测量，然后交换 | 1--35 层奇数/偶数分组 | 独立模型重复 |
| 全局共享几何 | 在1--35层拟合、且不使用待测层的一个跨层方向 | 另一奇偶层组 | 阶段形成历史 |
| 早层/晚层内部几何 | 分别在1--12层或25--35层内部估计稳定方向 | 同阶段另一奇偶层组 | 全局可复用方向 |
| 双向阶段迁移 | 早建空间只测晚层，晚建空间只测早层 | \(E\rightarrow L\) 与 \(L\rightarrow E\) | 功能或因果传递 |

“middle”是参数 F2--F8；“中间深度”是第13--24层，两者不是同一对象。

## 2. 与 Anchor 的对应关系

- **待消除的不确定性：**本地参数秩后移是否对齐一个真正跨层共享的广义低增益几何。
- **表征：**实际 raw \(\Delta n\)，不是 raw `o_proj` 写入。
- **语义：**研究者确认只用条件细类协方差；coarse 和复杂减简单对象不进入 verdict 或阶段标签。
- **完整频谱证据：**每层 F1--F16 的本地绝对方差、本地归一化份额、共享-band 捕获与随机归一化富集。
- **裁定证据：**广义 H/M/T 的 raw capture 与维度归一化富集。
- **提议主指标：**\(D_T\)；另用 \(T_T\) 相对匹配随机分区作为强制随机保护门。
- **主反例：**维度校正后 tail 不再占优，或没有超随机/超 head/middle 的方向特异性。
- **边界：**只判断冻结集合上的静态几何。

## 3. 假设

### G0：本地完整频谱现象门

\(\Delta n\) 的条件细类本地 F1--F16 频谱仍呈现正的早层到晚层秩重心后移，并在 design/confirmation 中同向。

### G1：广义共享 tail 几何

将广义区域捕获除以同维随机比例后，F9--F16 tail 从早层到晚层的富集增长大于 F1 head、F2--F8 middle，也大于匹配随机分区。

### 最强竞争解释

tail 的表面优势仅来自 2048 维的大空间、一般共享几何，或只有本地频谱重分配而没有共同方向。它预言维度校正后不存在 tail 特异增长。

F1--F16 负责定位变化发生在哪些 band，不是16个独立主假设；不能看结果后挑一个 band 挽救 G1。

## 4. 需要区分的解释

1. tail 因维度占一半而天然捕获更多；
2. 同维随机空间也能保留相同有限样本结构；
3. 只有本地 F1--F16 质量后移，没有共享方向；
4. head 或 middle 也产生相同的共享增长；
5. 错把旧本地坐标与另一套基底结合；
6. 只有第36层异常；
7. 少数 parent 或 template 决定符号。

## 5. 数据构造与来源

### 5.1 固定语义集合

- 8 个 parent × 每个 8 个 child × 4 个无标签模板 × 每模板 2 组事实 = 512 条；
- design：模板1--2；confirmation：模板3--4；
- 数据标识：`cb440b98d81bac3f9813344f85e6efdbd994b7b988d8009ba64e207e64a11859`；
- 数据文件 SHA-256：`60236fcd675c307a38f1b1ae7b8b7712fa325f437937b6f8febebdaca3ee6bb1`。

不得修改 prompt、label、tokenizer、读出位置、样本顺序或划分。

### 5.2 冻结来源

- 参数 run `a15-01-09-e01-p-20260807T061000Z`，manifest SHA-256 为 `2fd84effc280e7090fe33a99e44446df083f2556de592c3fa8ee4faa0b99bf59`，36/36 层；
- response run `a15-01-09-e01-r-20260807T061000Z`，manifest SHA-256 为 `f7c74a1e495f6fed13d852b403693abde15b2ba9dce63b5f264c2d645bb5a72a`，36/36 层、512/512 条；
- A15_02 冻结的 post-`o_proj` 写入缓存，用于回放身份检查。

旧 response 只保存了一套单独重算的本地参数基坐标，参数基向量未保存。它可检查本地频谱，但不能直接构造跨层投影。

### 5.3 提议的一次确定性 raw-\(\Delta n\) 回放

用冻结模型和 \(S_0\) 回放一次，保存全部36层的原始 bfloat16 \(\Delta n_\ell\in\mathbb R^{512\times4096}\)。必须满足：

1. 数据 hash 与样本顺序完全一致；
2. 36/36 层、512/512 条完整且有限；
3. 回放 \(a_\ell\) 与冻结缓存最大绝对误差为0；
4. 完整基投影能量相对误差不超过 \(10^{-4}\)；
5. 16 个本地 band 的 raw fine 统计复现旧结果：秩重心绝对差不超过 \(5\times10^{-4}\)，类别间总方差相对差不超过 \(10^{-3}\)。

任一失败记为 `INSUFFICIENT_INPUT_REPLAY` 并停止。

### 5.4 条件细类协方差

令 \(z_{pcet}^{(\ell)}\) 对应 parent、child、template、fact bundle：

\[
\mu_{pc}^{(\ell)}=\frac{1}{8}\sum_{e,t}z_{pcet}^{(\ell)},\qquad
\mu_p^{(\ell)}=\frac{1}{8}\sum_c\mu_{pc}^{(\ell)},
\]

\[
B_{\ell,F}=\frac{1}{64}\sum_{p,c}
(\mu_{pc}^{(\ell)}-\mu_p^{(\ell)})(\mu_{pc}^{(\ell)}-\mu_p^{(\ell)})^{\top}.
\]

parent 和 child 等权。实际用中心化类均值矩阵计算 trace，不显式构造高维噪声协方差。

## 6. 诊断任务

本实验不训练 probe、不优化模型。它只：

1. 重建完整本地 F1--F16 语义频谱；
2. 仅用参数构造每个共享 F1--F16 和广义共享 H/M/T；
3. 对所有真实与随机空间测同一个 \(B_{\ell,F}\)；
4. 区分广义 tail 特异富集与维度、随机、一般共享、本地后移解释。

标签只用于构造平衡类中心；绝对可读性、非线性读出和任务行为都不在范围内。

## 7. 模型、频谱段与共享空间

### 7.1 冻结坐标

- 模型 `/data/share/Qwen3-8B`，冻结；
- 36 层，隐维 \(d=4096\)；
- native MLP 输入参数算子 \(K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}\)；
- 不纳入 `down_proj`；
- 不用 RMSNorm-folded，因为 \(\Delta n\) 已处于 native MLP 输入坐标。

### 7.2 固定频谱划分

\(P_{\ell,k}\) 投影到排序秩 \(256(k-1)+1\) 至 \(256k\)。

\[
P_{\ell,H}=P_{\ell,1},\qquad
P_{\ell,M}=\sum_{k=2}^{8}P_{\ell,k},\qquad
P_{\ell,T}=\sum_{k=9}^{16}P_{\ell,k}.
\]

三者维度为 \(r_H=256\)、\(r_M=1792\)、\(r_T=2048\)。

### 7.3 跨层互斥

第36层不参与空间构造或裁定。在1--35层中：A组为奇数层，B组为偶数层。测量组 \(f\) 时只用另一组 \(-f\)：

\[
Q_k^{(-f)}=\operatorname{TopEig}_{256}\left(\frac{1}{|-f|}\sum_{j\in-f}P_{j,k}\right),
\]

\[
Q_G^{(-f)}=\operatorname{TopEig}_{r_G}\left(\frac{1}{|-f|}\sum_{j\in-f}P_{j,G}\right).
\]

广义 \(Q_G\) 必须直接构造。独立构造的 \(Q_k\) 可能彼此重叠，不能直接相加得到广义 capture。

### 7.4 分阶段共享几何

令 \(E=\{1,\ldots,12\}\)、\(L=\{25,\ldots,35\}\)，强制完成四类诊断：

1. **早层内部：**在 \(E\) 内用另一奇偶子组构造，测被排除的早层；
2. **晚层内部：**在 \(L\) 内用另一奇偶子组构造，测被排除的晚层；
3. **早到晚：**用全部早层参数投影构造 \(Q_{G,E}\)，只测晚层 conditional-fine 协方差；
4. **晚到早：**用全部晚层构造 \(Q_{G,L}\)，只测早层 conditional-fine 协方差。

全部 F1--F16 与直接广义 H/M/T 都执行相同构造，并报告参数侧跨阶段重合

\[
O_{EL,G}=\frac{\operatorname{tr}(Q_{G,E}Q_{G,L})}{r_G}.
\]

全局奇偶 \(Q_G^{(-f)}\) 是唯一主构造。分层空间不进入 \(T_G\)、\(D_T\)、Pass、Fail 或 Insufficient；只有数值构造失败导致必需证据缺失时，才影响资格。

### 7.5 投影可靠性

每个投影的归一化正交误差与求解残差不超过 \(10^{-5}\)。两套广义 tail 共识空间的重合度必须超过512对随机 rank-2048 空间重合度的 q95。F1--F16 与 H/M/T 都报告相同稳定性；非 tail 共享度低可以是结果，数值错误必须停止。

## 8. 精度、随机性与次数

- 无训练目标、优化器、checkpoint 选择或结果调参；
- 模型按冻结 bfloat16 路径回放；
- 投影构造和矩阵乘法用 FP32；类均值、trace、汇总和区间用 FP64；
- 投影重合度随机种子 `151100`；
- 语义随机分区种子 `151101`；
- 分组重采样种子 `151102`；
- 提议随机规模：512 个 Haar 正交 16-band 分区；
- 提议不确定性规模：2,000 次配对分组重采样。

每次 Haar 抽样生成一个4096维随机正交基，连续切成16个256维随机 band；再按 F1、F2--F8、F9--F16 合并成同维 H/M/T 随机对照。同一分区用于所有层和两个表达半集。

## 9. 冻结条件与证据

| 项目 | 冻结值 |
| --- | --- |
| 表征 | raw 实际 \(\Delta n_\ell\) |
| 语义 | 条件细类 \(B_{\ell,F}\) |
| 本地频谱 | F1--F16，每段256维 |
| 广义区域 | H=F1；M=F2--F8；T=F9--F16 |
| 早层/晚层 | 1--12 / 25--35 |
| 中间深度展示 | 13--24 |
| 终端边界 | 第36层只描述 |
| 构造/测量 | 1--35层奇偶互斥 |
| 分层构造 | 早/晚层内部奇偶互斥；全早只测晚；全晚只测早 |
| 随机对照 | 每次一个跨层共享的随机16-band分区 |
| 表达可靠性 | 模板1--2与3--4 |

不得事后重分 band、挑 tail 子段、换层窗口、用 coarse/fine 差挽救或用平滑结果裁定。

## 10. 主指标与冻结分析

### 10.1 完整本地频谱

每层、每个 \(k=1,\ldots,16\) 必须报告

\[
v_{\ell,k}^{local}=\frac{\operatorname{tr}(P_{\ell,k}B_{\ell,F})}{256},
\qquad
p_{\ell,k}^{local}=\frac{\operatorname{tr}(P_{\ell,k}B_{\ell,F})}{\operatorname{tr}(B_{\ell,F})}.
\]

\(v\) 是每方向的绝对类别间方差，单位为 activation squared/direction；\(p\) 是归一化份额，F1--F16 之和为1。二者都必须给出。

### 10.2 完整共享-band 数据

每层、每个 rank-256 共享 band 必须报告

\[
c_{\ell,k}^{shared}=\frac{\operatorname{tr}(Q_kB_{\ell,F})}{\operatorname{tr}(B_{\ell,F})},
\qquad
e_{\ell,k}^{shared}=16c_{\ell,k}^{shared}.
\]

独立构造的共享 band 可能不正交，因此16个 \(c^{shared}\) 不能叫“份额”，也不要求和为1。

### 10.3 广义 H/M/T 与主统计量

对 \(G\in\{H,M,T\}\)：

\[
c_{\ell,G}=\frac{\operatorname{tr}(Q_GB_{\ell,F})}{\operatorname{tr}(B_{\ell,F})},
\qquad
e_{\ell,G}=\frac{c_{\ell,G}}{r_G/4096}.
\]

raw capture \(c\) 和 enrichment \(e\) 都要报告；只有 \(e\) 可以公平比较不同维度的 H/M/T。三个广义共享空间分别估计，所以它们的 raw capture 不要求和为1；只有本地 H/M/T 正交分区满足守恒。

\[
T_G=\operatorname{median}_{\ell=25:35}e_{\ell,G}
-\operatorname{median}_{\ell=1:12}e_{\ell,G},
\]

\[
D_T=T_T-\max(T_H,T_M).
\]

\(D_T\) 是提议主统计量，单位是“随机归一化富集差”。它判断 tail 的深度增长是否超过另外两个广义区域，不能证明功能。

对第 \(q\) 个随机分区，用其 F9--F16 并集计算 \(T_{R,T}^{(q)}\) 与晚层富集 \(L_{R,T}^{(q)}\)；真实 \(T_T\) 与 \(L_T\) 分别和随机 q95 比较。

### 10.4 G0 与本地广义 tail 桥

使用冻结的16-band秩重心

\[
C_{\ell,F}=\sum_{k=1}^{16}p_{\ell,k}^{local}\frac{k-0.5}{16}
\]

及其早晚差 \(T_{rank}\)。另报本地 H/M/T 份额，并用 \(P_{\ell,T}\) 计算本地广义 tail 富集变化 \(T_{LT}\)。

### 10.5 不确定性与多重比较

进行2,000次配对重采样：八个 parent 有放回抽取，四个 template cluster 有放回抽取；被抽中的模板保留两组事实和所有 child。相同抽样同时用于所有层和空间。不能把方向或层当独立单位。

对 \(T_T\)、\(D_T\) 和广义对照报告百分位95%区间。F1--F16 单段区间只用于定位，不作单段显著性结论，也不能多重挑选挽救主结论。

### 10.6 冻结分析顺序

输入/回放检查 → 完整本地 F1--F16 与 G0 → 共享空间检查 → 不挑选地生成完整共享 F1--F16 → 全局广义 H/M/T 的 \(c,e,T_G,D_T\) → 随机分区比较 → 奇偶层组与表达半集 → 冻结一个全局 typed verdict → 再读取早层内部、晚层内部、双向阶段迁移和跨阶段重合并给出一个非主裁定阶段标签。

## 11. 次级量与保护检查

1. 参数可用度 \(a_{\ell,G}=\operatorname{tr}(Q_GP_{\ell,G})/r_G\) 与 bandwise \(a_{\ell,k}\)。
2. 本地 H/M/T 的 raw share、每方向方差与富集变化。
3. design/confirmation 分别报告 \(T_{rank}\)、\(T_T\)、\(D_T\)。
4. 奇数/偶数待测层分别报告 \(T_T\)、\(D_T\)。
5. 第36层单独显示。
6. 所有原始层点必须显示；可叠加居中三层移动中位数帮助阅读，但裁定只用未平滑数据。
7. 对 \(A,B\in\{E,L\}\)，阶段 tail 捕获为 \(S_{A\rightarrow B,T}=\operatorname{median}_{\ell\in B}e_{\ell,T}(Q_{T,A})\)；\(S_{E\rightarrow E,T}\) 与 \(S_{L\rightarrow L,T}\) 使用各自内部奇偶互斥空间。
8. 全局 verdict 冻结后，只能给以下一个非主裁定解释：
   - `globally_stable_compatible`：\(O_{EL,T}\) 与两向 cross-stage capture 都超过同维 Haar q95；
   - `late_formation_compatible`：晚层内部超过 Haar q95，而早层内部、\(O_{EL,T}\) 和两向 cross-stage 都不超过；
   - `stage_redirection_compatible`：早层与晚层内部都超过 Haar q95，但 \(O_{EL,T}\) 和两向 cross-stage 都不超过；
   - `mixed_stage_geometry`：其余情形。

这些标签只表示“与某解释相容”，不是因果证明，也不能挽救或降级全局 verdict。

## 12. 已知正确、错误与易混淆情形

| 情形 | 必须如何解释 |
| --- | --- |
| 本地 F1--F16 份额和为1 | 本地分区实现正确 |
| 随机 H/M/T 平均 capture 接近 \(1/16,7/16,8/16\) | 同维随机实现正确 |
| 人工协方差位于已知投影，capture 接近1 | 投影实现正确 |
| 少样本/层、回放不一致、NaN、投影无效 | 停止，不给科学 verdict |
| raw tail 最大但 enrichment 不大 | 维度效应，不是 tail 特异 |
| 某一个 tail band 很高但广义 \(D_T\) 失败 | 只能定位，广义结论失败 |
| 本地频谱后移但共享 tail 等同随机 | local-only relocation |
| tail 超随机但 head/middle 同样增长 | 一般共享几何 |
| 只有第36层极端 | 终端异常 |
| 平滑线通过但 raw 指标失败 | 视觉假象 |

## 13. 分阶段实验合同

### Stage 0：冻结输入审计

检查数据与 run hash、样本顺序、形状、覆盖；任一不一致停止。

### Stage 1：确定性 raw-\(\Delta n\) 回放

只用冻结模型和 \(S_0\) 物化 raw \(\Delta n\)，执行 Section 5.3 全部检查；失败后 smoke/full 都不能继续。

### Stage 2：本地与共享频谱构造

构造本地 F1--F16/H/M/T、全局奇偶互斥共享空间、早层内部、晚层内部和双向阶段空间；检查秩、正交性、残差、层组排除与跨阶段重合。

### Stage 3：工程 smoke

用人工协方差和固定小子集检查完整频谱记账、随机维度期望、广义与独立 band 不可直接相加、随机种子、产物 schema。smoke 数字无研究资格。

### Stage 4：一次 full frozen analysis

一次性使用512条、1--36层、512个随机分区和2,000次重采样。看到 full 结果后不得修改科学定义。

### Stage 5：证据与图片审计

写表、图、manifest、`summary.md`、`detailed.md`；原分辨率审核标签、原始点、单位、随机基线、H/M/T维度、第36层、平滑说明与 claim 边界。

## 14. 算法、输出与来源

```text
核对冻结输入
回放 raw delta-n 并复现旧本地频谱
构造本地 F1--F16 和直接本地 H/M/T
构造全局、早层内部、晚层内部和双向阶段共享 F1--F16 与直接 H/M/T
生成跨层共享的随机16-band分区
计算全部 band 与广义区域指标
按 parent/template 配对重采样
一次性应用广义 tail verdict
只在全局 verdict 冻结后给出非主裁定阶段标签
渲染并审核完整频谱图和决策图
```

批准 worker：`Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_e01_shared_tail_geometry/`。旧 basis 与 attention-write 产物只按路径读取，不修改。raw tensor、日志和完整随机抽样留在新 worker。资源上限：一张 H100 80GB、六小时墙钟时间、20 GiB 新增存储；任一超限都在科学 verdict 前停止。

获批执行后必须产生：

- `provenance/input_manifest.json`、`numerical_guards.json`、`verdict.json`；
- `tables/local_spectrum_f1_f16.csv`：每层、每 band 的 \(v^{local}\) 与 \(p^{local}\)；
- `tables/shared_spectrum_f1_f16.csv`：每层、每 band 的 \(c^{shared}\) 与 \(e^{shared}\)；
- `tables/broad_hmt.csv`：每层本地/共享 H/M/T 的 raw 与 normalized 数据；
- `tables/stage_shared_geometry.csv`：每个 F1--F16 与 H/M/T 的早层内部、晚层内部、早到晚、晚到早测量；
- `tables/stage_overlap.csv`：真实与 Haar 的跨阶段投影重合；
- `tables/contrast_summary.csv`、`random_null_summary.csv`；
- `figures/figure0_broad_tail_decision.png`；
- `figures/figure1_full_16band_spectrum.png`；
- `summary.md`、`detailed.md`。

完整频谱图必须包含本地绝对方差、本地归一化份额、全局共享-band富集热图和 F1--F16 早晚变化；决策图必须包含全局 H/M/T 的逐层 raw capture 与 enrichment、广义对比、随机区间和层组/表达稳定性。第三张诊断图展示阶段内部、双向迁移和跨阶段重合，并显著标记“非主裁定”。所有文件记录 SHA-256。

## 15. 通过、失败与证据不足

优先检查 `Insufficient`；未触发后再检查全部 Pass 条件；只有估计明确反对假设才记 Fail。

### Pass：`BROAD_SHARED_TAIL_GEOMETRY`

必须全部满足：

1. 输入、回放、数值和广义共享 tail 稳定性检查通过；
2. G0：\(T_{rank}\) 的95%下界 \(>0\)，两组表达点估计都 \(>0\)；
3. 本地广义 tail 桥 \(T_{LT}>0\)；
4. 真实广义 tail 的 \(T_T\) 95%下界 \(>0\)；
5. 真实 \(T_T\) 与晚层富集 \(L_T\) 都超过512个匹配随机 F9--F16 并集的 q95；
6. \(D_T=T_T-\max(T_H,T_M)\) 的95%下界 \(>0\)；
7. 奇数待测层、偶数待测层、design、confirmation 中的广义 tail \(T_T\) 都 \(>0\)。

16个单 band 是强制证据，但不是额外 Pass 门。

阶段几何标签只能在全局 verdict 之后给出，且不影响全局 verdict。

### Fail：`LOCAL_RANDOM_OR_NONTAIL_RELOCATION`

G0 与有效性检查成立，但稳定出现：广义 tail 不增长、不超过同维随机、维度校正后不超过 head/middle，或只有本地频谱后移。失败关闭广义共享 tail 解释，不允许直接做 activation 删除或 Router。

### Insufficient

输入/回放/投影失败、G0 不可靠、必需广义区间跨0、表达或层组反号，都记为具体 `INSUFFICIENT_*`。只允许修复来源或估计；新的 band 分组、挑选 tail 子段、指标或阈值必须重新批准。

## 16. 不能声称

不能声称知识存储、现实语义本体、信息在 head/middle/旧状态中缺失、非线性编码、MLP 传递或压制、near-null sink、logit/loss 作用、下游效用、跨模型普遍性或 Router 价值。

## 17. 协议块确认与修改

| 协议块 | 状态 | 当前需要的决定 |
| --- | --- | --- |
| A. 问题与边界 | `CONFIRMED` | 几何问题、全局主裁定边界和 F1/F2--F8/F9--F16 已确认 |
| B. 数据与来源 | `CONFIRMED` | 复用 \(S_0\)，确定性物化 raw \(\Delta n\) |
| C. 诊断任务 | `CONFIRMED` | conditional-fine 是唯一主语义对象，完整频谱强制输出 |
| D. 模型与空间 | `CONFIRMED` | 全局、早层内部、晚层内部和双向阶段几何全部必做 |
| E. 精度与随机性 | `CONFIRMED` | 512个随机正交分区与2,000次分组重采样 |
| F. 对照与裁定 | `CONFIRMED` | 全局 \(D_T\) 严格联合规则；阶段标签非主裁定且不能挽救 |
| G. 执行与复现 | `CONFIRMED` | 已明确授权实现、回放、smoke、一次 full run 与本地证据记录 |

跨块一致性为 `PASS`。科学设计以 `A15_04_E01_r1` 于 `2026-08-09T14:05:43Z` 冻结。执行开始后，若改变 \(S_0\)、\(\Delta n\)、语义协方差、层组、阶段窗口、F1--F16、H/M/T、随机构造、主指标、阈值或全局主裁定边界，必须追加 amendment 并明确结果资格。

**Append-only amendment A1——强制逐方向图，`2026-08-09T14:18Z`。**修改前：完整频谱产物要求16-band绝对量与归一化量。修改后：额外强制输出每层4,096个本地参数方向上未平滑的 raw conditional-fine 方差与归一化方差份额，并固定展示 blocks 1、5、9、13、17、21、25、29、33、36。图上只为可读性叠加129-rank、三阶 Savitzky--Golay 曲线；表格、指标和 verdict 全部使用未平滑值。原因：保留研究者此前明确要求的必画曲线，并防止 band 平均掩盖局部形状。此时没有看到任何新实验结果，只运行了行为级单元测试。受影响块：G 的输出部分。批准来源：研究者此前对该图的明确要求与当前完成 full experiment 的授权。资格影响：无；数据、指标、阈值、比较和裁定规则均未改变。

**Append-only amendment A2——原始精确运行的坐标恢复，`2026-08-09T14:39Z`。**修改前：Section 5.3 要求在 H100 上重新回放并物化 raw \(\Delta n\)。工程 smoke 中，相同 H100 前向在36/36层都未与冻结的5090 bfloat16 attention cache 逐元素一致（浅层最大绝对误差为 `0.00390625`--`0.015625`，到第36层累积为 `1.5`），因此该回放没有证据资格，也不进入科学分析。修改后：只使用原注册 A15_01_09 response 运行；它已经记录 cache 精确回放（`max_abs_error=0`）和不超过 \(2.73059\times10^{-6}\) 的完整基重建误差。将其保存的完整 FP16 特征坐标乘以独立保存的完整参数基，恢复到 residual 原坐标的 \(\Delta n\)。只有每层同时满足以下条件才有资格：（i）response、semantic 与 parameter 保存的特征值数组逐元素相等；（ii）该参数基重建独立缓存的 raw attention write 时相对 \(L_2\) 误差不超过 \(3\times10^{-4}\)；（iii）坐标往返误差不超过 \(10^{-4}\)；（iv）原注册秩重心和总 trace 复现阈值仍满足。在读取任何几何结果前，四项观测最大值分别为 \(2.13193\times10^{-4}\)、\(2.81957\times10^{-6}\)、\(8.39460\times10^{-8}\) 和 \(2.88547\times10^{-7}\)，因此来源修复通过；最终裁定前仍必须做坐标量化扰动敏感性检查。原因：保留原5090精确语义前向，而不是为不同 GPU 架构放宽 exact-cache 门禁。受影响块：仅 B/G 的来源实现。批准来源：研究者直接完成 full experiment 的授权，以及冻结协议中“证据不足后只允许来源或估计修复”的规则。资格影响：有条件恢复；\(S_0\)、\(\Delta n\) 定义、conditional-fine 主语义对象、层、频带、指标、阈值、随机对照和全局主裁定边界均未改变。
