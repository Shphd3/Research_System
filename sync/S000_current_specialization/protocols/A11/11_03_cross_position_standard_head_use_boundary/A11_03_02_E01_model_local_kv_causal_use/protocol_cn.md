# Protocol 草稿：A11_03_02_E01 匹配辅助训练结构下的模型内 K/V 因果使用审计

## 0. 审批快照

**批准状态：** 研究者于 2026-07-15 批准；英文执行合同、实现和四卡 ACP 运行已授权。
**目的：** 判断信息性 K=2 MTP 是否比训练结构匹配的 shared-aux 更强地建立 `U03` 源状态到后续标准主头的因果通道。
**主要 Anchor：** [11_03_02 信息性未来目标的标准主头因果使用审计](/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/subanchors/11_03_02_standard_head_causal_use_anchor_cn.md)。
**Anchor 决策问题：** 相对于活跃头数、CE 项数和名义 loss 系数匹配的 shared-aux，信息性 MTP 是否增强后续标准主头对 `U03` 源状态的因果使用？
**检验的物理先验：** 如果标准主头使用源状态中的分支信息，在模型内部换入真实异分支供体 K/V，应使答案朝供体分支切换。
**检验的核心模型项：** $\Gamma_{info}=C_{info\text{-}MTP}-C_{shared\text{-}aux}$。
**主要证伪结果：** 能力和干预守卫均通过，但 $\Gamma_{info}$ 不高于零或只有控制量级。
**实验角色：** 根因审计；不是方法构造或性能优化。
**唯一主要指标：** informative-MTP 减 shared-aux 的受控反事实答案切换效应，单位为概率差。
**最小设置：** 四分支 A11 K=2 数据；2 层小型因果 Transformer；全位置标准交叉熵；NTP/shared-aux/informative-MTP 三个条件；5 个配对种子；只替换第二层 `U03` 的 K/V。
**基本配置：** 训练 4,096 个基础干扰配置，校准 256 个，确认 1,024 个；每个配置含四个平衡分支；最多 15,000 步，每 100 步评估。
**运行条件：** 配对 NTP、shared-aux、informative-MTP；每个模型内部包含干净、同分支供体、异分支供体和实现正控制。
**通过：** 所有守卫通过；至少 4/5 个种子的 $\Gamma_{info}\ge0.10$，且五种子均值至少为 `0.10`。
**失败：** 所有守卫通过，但五种子均值不为正，或至多 2/5 个种子达到 `0.10`。
**证据不足：** 恰好 3/5 达标、均值在 `(0,0.10)`、任务未学会、能力不匹配、同分支控制失败、双向性失败或实现/确认隔离失败。
**不能声称：** 一般 MTP 优势、K 尺度规律、长程或自然语言收益、组合算法、表征可拆分性或 MoE 价值。
**审批决定：** 已批准。英文 canonical `protocol.md` 必须与本合同保持一致；本轮只授权已注册的最小实验，不授权追加 sweep。

## 1. 术语与定义

| 术语 | 通俗含义 | 具体对象或计算 | 单位或公式 | 为什么重要 | 不能证明 |
|---|---|---|---|---|---|
| 决策位置 | MTP 较早直接预测分支答案的位置 | `U03`，记为 $T$ | 位置索引 | 定位早期信息 | 一般规划状态 |
| 共享中间词元 | 所有分支紧邻目标相同 | `A_SHARED` | 词元 | 让 NTP 在 $T$ 处没有直接分支标签 | 长程依赖 |
| 标准主头 | 普通下一词元预测头 | $q_1(h_t)$ 预测 $x_{t+1}$ | 全词表概率 | 三个条件的共同输出接口 | 总体语言能力 |
| 第二未来词元头 | MTP 的额外预测头 | $q_2(h_t)$ 预测 $x_{t+2}$ | 全词表概率 | 在 `U03` 直接监督 $S_z$ | 标准主头使用 |
| 源 K/V | 后续位置能够读取的 `U03` 注意力记忆 | 第二层全部注意力头的 $K_{2,T},V_{2,T}$ | 张量 | 主因果干预对象 | K 与 V 各自的单独作用 |
| 接收位置 Q | `A_SHARED` 用于读取历史的查询 | $Q_{2,T+1}$ | 张量 | 与源 K 匹配 | MTP 信息形成 |
| 异分支供体 | 与接收体 $z$ 不同、但干扰配置相同的供体 | $d_{z',n}$，$z'\neq z$ | 样本 | 定向反事实替换 | 信息内容特异性 |
| 同分支供体 | 与接收体 $z$ 相同、干扰配置不同的供体 | $d_{z,n'}$ | 样本 | 测量替换本身的扰动 | 清除全部混杂 |
| 受控切换效应 | 异分支正确切换率减去同分支无关变化率 | $C_o=p_o^{diff}-p_o^{same}$ | 概率差 | 单模型因果使用 | 目标间差异 |
| shared-aux | 第二头复制主头的下一词元目标 | $q_2(h_t)$ 也预测 $x_{t+1}$ | 全词表概率 | 匹配活跃头/CE 项/名义系数 | 真实梯度相同 |
| 信息内容增量 | informative-MTP 受控效应减去 shared-aux 受控效应 | $\Gamma_{info}=C_{info\text{-}MTP}-C_{shared\text{-}aux}$ | 概率差 | 唯一主要指标 | 弱但不翻转答案的使用 |
| 能力匹配 | 主比较两个标准主头都稳定解出任务且置信难度接近 | 共同稳定检查点及 CE 差守卫 | 布尔值 | 排除“学得更多”冒充“用得更多” | 内部算法或真实梯度相同 |

### 为什么主干预不是 Q

在第二层，`A_SHARED` 读取 `U03` 的直接关系是

$$
\alpha_{T+1,T}
=
\operatorname{softmax}(Q_{2,T+1}K_{2,T}^{\top}),
\qquad
R_{T+1\leftarrow T}=\alpha_{T+1,T}V_{2,T}.
$$

- 源位置 $K_{2,T}$ 决定接收位置是否找到 `U03`；
- 源位置 $V_{2,T}$ 决定找到后读回什么；
- 源位置 $Q_{2,T}$ 只决定 `U03` 自己如何读取更早上下文，不会被后续 `A_SHARED` 直接调用；
- 接收位置 $Q_{2,T+1}$ 决定怎样检索，但替换它会改变接收端策略，而不是只替换 MTP 形成的源信息。

因此第一轮联合替换源 K/V。K-only、V-only、源 Q 和接收 Q 均停放，除非主实验先产生需要分解的稳定结果。

## 2. Anchor 对齐

**决策问题：** informative-MTP 是否在匹配辅助训练结构与标准主头能力下增强 `U03` 源 K/V 对答案的因果控制？
**物理先验：** 真实异分支源状态若被标准主头使用，应定向改变供体答案概率或答案本身。
**核心模型项：** $C_o$ 与 $\Gamma_{info}$。
**主要证伪条件：** 有效守卫下 $\Gamma_{info}\le0$ 或低于冻结的 `0.10` 最小效应。
**结论边界：** 只裁决该受控四分支 K=2 数据和第二层 K/V 接口上的强行为因果使用。

## 3. 待检验假设

### 主要假设

在标准主头能力匹配后，informative-MTP 模型从异分支 `U03` K/V 补丁得到的供体答案切换效应，比 shared-aux 模型更强：

$$
\Gamma_{info}\ge0.10.
$$

### 最强竞争解释

增加一个活跃辅助头与第二项 CE 本身已经建立相同通道，因此

$$
C_{info\text{-}MTP}\approx C_{shared\text{-}aux},
\qquad
\Gamma_{info}\approx0.
$$

### 不利替代

信息性未来目标相对 shared-aux 干扰标准头对早期通道的读取，使 $\Gamma_{info}<0$。

## 4. 竞争解释

1. **增加辅助训练结构已经足够：** 由 $\Gamma_{info}$ 而非单独 $C_{info\text{-}MTP}$ 区分。
2. **informative-MTP 只是整体学得更好：** 由 shared-aux/informative-MTP 共同稳定检查点、标准头准确率和 CE 匹配守卫区分。
3. **补丁只是大扰动：** 由真实模型内供体、自补丁复现和同分支供体区分。
4. **输出头可读但没有使用源路径：** 由源 K/V 因果替换而非线性探针区分。
5. **某一分支方向偶然容易：** 由全部 12 个有序异分支对和双向表格区分。
6. **Q 才是关键：** $Q_{T}$ 控制 `U03` 如何读取更早前缀，$Q_{T+1}$ 控制 `A_SHARED` 如何检索；当前主干预固定二者，只检验已形成的源 K/V 是否被后续主头因果使用。
7. **直接 `BR_z` 路径产生冗余：** 若 K/V 只产生小 margin 变化而不翻转答案，主指标会否定“强行为控制”，但不能否定所有弱或冗余使用；该边界必须保留。
8. **全位置目标包差异：** 为保持一般 LLM 的全位置 CE 训练形式，shared-aux 与 informative-MTP 的第二头在所有合法位置分别预测 $x_{t+1}$ 与 $x_{t+2}$。因此通过结果识别的是“信息性 K=2 目标包”相对重复下一词元辅助目标的作用，不能进一步归因于仅 `U03` 一个局部标签，也不能把 horizon 与 target content 完全拆开。

## 5. 数据、模型、算法与目标

### 5.1 数据生成

基础序列为

```text
BR_z F_{n,0} ... F_{n,15} U00 U01 U02 U03 A_SHARED S_z
```

- $z\in\{0,1,2,3\}$，`BR_z` 与 `S_z` 一一对应；
- $n$ 是与 $z$ 独立的干扰配置；
- 每个 $n$ 是 16 个中性 filler 词元的一次随机排列；
- 每个 $n$ 必须同时生成全部四个分支，保证答案和干扰严格独立；
- `U00 U01 U02 U03 A_SHARED` 在所有分支和配置中完全相同；
- 不加入距离、组合深度、自然语言改写或其他 $K$。

固定规模：

| 划分 | 基础干扰配置数 | 序列数 | 用途 |
|---|---:|---:|---|
| train | 4,096 | 16,384 | 标准 CE 训练 |
| calibration | 256 | 1,024 | 能力检查点、实现阈值和调试 |
| confirmation | 1,024 | 4,096 | 封存的主要因果判断 |

三部分的 filler 排列哈希必须为零重叠。不同目标、种子和条件共享同一数据清单与批次顺序。

供体配对：

- 异分支供体：固定同一 $n$，枚举所有 $z'\neq z$，每个 $n$ 产生 12 个有序分支对；
- 同分支供体：使用一个预先冻结的 nuisance-ID 无固定点置换 $\pi(n)$，令供体为 $(z,\pi(n))$；
- 接收体、供体和配对规则在查看任何三条件因果结果前冻结。

### 5.2 模型

- 2 层 decoder-only pre-LN 因果 Transformer；
- `d_model=64`，1 个注意力头，FFN 宽度 `256`，dropout `0`；
- 可训练词嵌入、位置嵌入、两层主干和标准主头；
- 三个条件都实例化同一个独立可训练全词表第二线性头；
- NTP 不激活第二头损失；shared-aux 与 informative-MTP 都激活第二头；
- 选择 2 层是必要的：第一层允许 `U03` 汇入更早的 `BR_z`，第二层 `U03` K/V 才能携带该信息供 `A_SHARED` 读取。1 层模型的同层 K/V 在该层注意力计算前形成，不能完成这条两阶段激活通道。

### 5.3 标准 NLP 交叉熵目标

令标准下一词元 CE 为

$$
L_1
=
\frac{1}{|\mathcal T_1|}
\sum_{t\in\mathcal T_1}
\operatorname{CE}(q_1(h_t),x_{t+1}).
$$

三个条件的目标为

$$
L_{NTP}=L_1,
$$

$$
L_{shared}
=\frac12\left[
L_1+
\frac{1}{|\mathcal T_2|}
\sum_{t\in\mathcal T_2}
\operatorname{CE}(q_2(h_t),x_{t+1})
\right],
$$

$$
L_{info\text{-}MTP}
=\frac12\left[
L_1+
\frac{1}{|\mathcal T_2|}
\sum_{t\in\mathcal T_2}
\operatorname{CE}(q_2(h_t),x_{t+2})
\right].
$$

每个活跃头都使用全词表 softmax 交叉熵；不固定输出头、不使用手工几何、不使用 decision-only loss。在 `U03`，shared-aux 第二头预测共同的 `A_SHARED`，informative-MTP 第二头预测分支答案 `S_z`。

取平均只匹配 shared-aux 与 informative-MTP 的活跃头数、CE 项数、每项系数和名义总尺度。它不保证两项 CE 的难度、共享主干的实际梯度范数/方向或优化轨迹相同；这些差异可能正是“目标信息内容”的作用路径。正式运行只记录每个 loss 分量对共享主干的梯度范数和夹角，不做动态梯度归一化或事后剂量匹配。由于 NTP 的 $L_1$ 系数为 `1` 而两个双头条件中为 `0.5`，NTP 不承担主要因果对照。

### 5.4 优化配置

- AdamW，学习率 `3e-4`，`betas=(0.9,0.95)`，权重衰减 `0.01`；
- batch size `128`；
- 最多 `15,000` optimizer steps；
- 每 `100` 步在 calibration 上评估并保存检查点；
- 无 dropout、无数据增强、无学习率扫描；
- 梯度裁剪全局范数 `1.0`；
- 所有目标共享初始化主干、标准主头、数据批次和优化器状态约定。

## 6. 条件、种子与检查点

正式种子：`971,972,973,974,975`。每个种子包含共享初始化的 NTP、shared-aux、informative-MTP 三条训练，共 15 条正式轨迹。

### 6.1 能力匹配检查点规则

对每个种子，只使用同一个训练步 $t_s$ 比较三个条件。$t_s$ 是最早同时满足以下条件的共同检查点：

1. 三个条件在 calibration 的 `A_SHARED -> S_z` 标准头准确率，连续三个检查点均为 `1.0`；
2. 当前检查点 shared-aux 与 informative-MTP 的答案位置标准头 CE 差不超过 `0.05`；
3. 在 `U03` 位置，shared-aux 第二头对其注册下一词元目标、informative-MTP 第二头对其注册第二未来词元目标的准确率，连续三个检查点均不低于 `0.95`；
4. 当前检查点不晚于 15,000 步。

若某个种子没有合格共同检查点，整体结果判为证据不足，不改用事后挑选的独立检查点。

### 6.2 条件与证据表

| 条目 | Anchor 条款 | 模型项或竞争解释 | 必要性 | 证据角色 | 通过 | 失败 | 证据不足 | 表/图 |
|---|---|---|---|---|---|---|---|---|
| NTP 干净训练 | 系统基线 | 单头普通训练 | 次要基准 | 守卫 | 连续 3 次 `1.0` | 不适用 | 未学会 | capability table |
| shared-aux 干净训练 | 匹配控制 | 活跃辅助头/损失 | 主要对照 | 守卫 | 标准头 `1.0` 且第二头 `>=0.95` | 不适用 | 未学会 | capability table |
| informative-MTP 干净训练 | 信息内容与形成 | 信息性未来监督 | 被检条件 | 守卫 | 标准头 `1.0` 且第二头 `>=0.95` | 不适用 | 未学会 | capability table |
| 自补丁复现 | 干预实现 | 缓存实现错误 | 保护主结论 | 守卫 | logits 最大差 `<=1e-6` | 不适用 | 超阈值 | patch guards |
| 同分支 K/V 补丁 | $p_o^{same}$ | 大扰动解释 | 控制补丁噪声 | 守卫 | 每条件每种子 `<=0.05` | 不适用 | 超阈值 | control table |
| 异分支 K/V 补丁 | $p_o^{diff}$ | 源状态因果控制 | 决定性干预 | 主要 | 进入 $C_o$ | 进入 $C_o$ | 配对缺失 | main table |
| 标准头输入正控制 | 输出接口有效 | 读出/补丁代码错误 | 验证已知可切换状态 | 守卫 | 供体答案切换 `>=0.95` | 不适用 | 低于阈值 | patch guards |
| informative-MTP/shared-aux 差 | $\Gamma_{info}$ | 辅助训练结构已足够 | 唯一决策 | 主要 | 4/5 且均值 `>=0.10` | 均值 `<=0` 或至多 2/5 | 其他 | central figure |
| 有序分支对分解 | 双向性 | 单方向偶然 | 检查隐藏异质性 | 次要守卫 | 所有对有覆盖，无系统反向组 | 不适用 | 缺失或稳定反向 | pair table |

## 7. 唯一主要指标

只在干净标准主头原本预测正确的接收体上计算：

$$
p_{o,s}^{diff}
=
\Pr[
\hat y_o(r_{z,n};S_o(d_{z',n}))=S_{z'}
\mid z'\neq z
],
$$

$$
p_{o,s}^{same}
=
\Pr[
\hat y_o(r_{z,n};S_o(d_{z,\pi(n)}))\neq S_z
],
$$

$$
C_{o,s}=p_{o,s}^{diff}-p_{o,s}^{same},
$$

$$
\Gamma_{info,s}=C_{info\text{-}MTP,s}-C_{shared\text{-}aux,s}.
$$

五种子均值为

$$
\bar\Gamma_{info}=\frac15\sum_s\Gamma_{info,s}.
$$

选择答案切换而不是探针或注意力权重，是因为它直接检验标准主头行为是否被供体源状态控制。假阳性的成本是把补丁扰动或增加辅助训练结构误写成信息性未来目标的特异使用；假阴性的成本是遗漏只改变 margin、但不足以翻转答案的弱或冗余使用。后者保留在次要指标和结论边界中，不改变主要判断。

## 8. 次要指标

- 供体答案相对接收体答案的 logit-margin 变化；
- `A_SHARED` 对 `U03` 的第二层注意力权重；
- `U03` 第二层 K/V 的分支内、分支间距离；
- 标准主头干净准确率、CE 和 margin 分布；
- MTP 第二头在 `U03` 的准确率与 CE；
- shared-aux 第二头在其注册目标上的准确率与 CE；
- 每个双头条件中，两个 loss 分量对共享主干的梯度范数及夹角（仅诊断，不作动态匹配）；
- $\Gamma_{system}=C_{info\text{-}MTP}-C_{NTP}$（次要系统基线）；
- 每个有序分支对的 $p^{diff}$、margin 变化和样本数；
- 线性探针只作信息形成守卫，不参与通过/失败。

不运行 K-only、V-only、源 Q、接收 Q、层扫描、K 扫描或长程变体。

## 9. 已知正确、已知错误与容易混淆的情况

### 已知正确

1. 无补丁的增量缓存前向必须复现完整序列前向，logits 最大误差不超过 `1e-6`。
2. 用异分支供体的 `A_SHARED` 最终隐藏状态直接替换标准头输入，应以至少 `0.95` 的比例输出供体答案。该正控制只验证输出接口和标签映射。

### 已知错误

1. 同分支供体不应系统改变答案，$p_o^{same}\le0.05$。
2. 随机打乱供体答案标签后，不应仍出现高“正确供体切换率”。此项只在 calibration 微测试中验证统计代码。

### 容易混淆

1. $C_{shared\text{-}aux}>0$ 且 $C_{info\text{-}MTP}>0$、但二者相同：支持两种辅助训练共同使用，否定信息内容特异增强。若二者还都强于 NTP，只能说明增加辅助训练结构这一整包条件相关。
2. 源状态探针很强但 $C_o\approx0$：支持形成，不支持强行为控制。
3. margin 有稳定变化但答案不切换：可能存在弱或冗余使用，但主要强行为假设不通过。
4. informative-MTP 与 shared-aux 的干净准确率或 CE 明显不匹配：不能直接比较因果使用，判为能力不匹配。

## 10. 分阶段证据计划

| 阶段 | 局部问题 | 输入证据 | 通过/失败/不清楚规则 | 调试产物 | 交接 |
|---|---|---|---|---|---|
| 数据生成 | 分支与干扰是否独立 | manifest、哈希、计数 | 四分支精确平衡、三划分零重叠 | `data_guard.csv` | 训练清单 |
| CE 训练 | 三个条件是否学会注册目标 | 轨迹、CE、accuracy | 满足共同检查点规则 | `learning_curves.csv` | 合格检查点 |
| 缓存提取 | K/V 是否来自正确层和位置 | 张量 shape、哈希、重放误差 | 自补丁误差 `<=1e-6` | `cache_audit.csv` | 可补状态 |
| 控制补丁 | 补丁是否造成无关扰动 | 同分支与正控制 | same `<=0.05`、positive `>=0.95` | `patch_controls.csv` | 主要评估 |
| 确认评估 | 信息性未来目标是否带来额外强行为控制 | 封存供体—接收体对 | 应用 4/5 与均值规则 | `causal_use_by_seed.csv` | 结论 |
| 方向分解 | 聚合是否隐藏分支异常 | 12 个有序分支对 | 覆盖完整、报告稳定反向组 | `causal_use_by_pair.csv` | 边界解释 |

### 中央图合同

- **问题：** informative-MTP 是否比 shared-aux 增强 `U03` K/V 对标准主头的因果控制？
- **指标：** 每种子的 $C_{NTP}$、$C_{shared\text{-}aux}$、$C_{info\text{-}MTP}$ 和 $\Gamma_{info}$，单位为概率差。
- **数据：** confirmation 全部平衡有序分支对，先在样本内聚合，再按种子汇总。
- **图形：** 左图为每种子三个条件的 $C_o$ 配对点；右图为 $\Gamma_{info}$，显示 `0` 和 `0.10` 水平线。
- **支持模式：** 至少 4/5 个点高于 `0.10` 且均值不低于 `0.10`。
- **削弱模式：** 聚集在零附近、shared-aux 与 informative-MTP 相同或 informative-MTP 更低。
- **允许结论：** 该受控接口上由信息性未来目标带来的额外强行为因果使用增量。
- **限制：** 不能排除未翻转答案的弱或冗余使用。

## 11. 算法规格

### 输入

- 冻结的数据 manifest 与供体配对表；
- 每个种子的三条件合格共同检查点；
- 第二层 `U03` K/V hook；
- confirmation 接收体与供体样本。

### 参数

| 参数 | 值 | 含义 | 过小风险 | 过大风险 |
|---|---:|---|---|---|
| `m` | 4 | 分支数 | 因果方向覆盖不足 | 评估成本增加 |
| `n_confirm` | 1,024 | 确认干扰配置 | 分支对比例噪声 | 只增加评估成本 |
| `delta_info` | 0.10 | 最小有意义信息内容增量 | 提升微小噪声 | 漏掉弱真实作用 |
| `tau_same` | 0.05 | 同分支无关变化上限 | 对数值噪声过严 | 容忍无效补丁 |
| `tau_positive` | 0.95 | 正控制切换下限 | 容忍实现缺陷 | 对少量难例过严 |
| source layer | 2 | 携带第一层汇入信息的 K/V | 第 1 层 K/V 不含上下文整合 | 扫层造成事后选择 |

### 中间变量

- 接收体干净 logits 与答案；
- 自补丁、同分支、异分支和正控制 logits；
- 每个样本的 donor-directed switch；
- 每种子 $p^{diff}$、$p^{same}$、$C_o$、$\Gamma_{info}$ 和次要 $\Gamma_{system}$；
- 每个有序分支对的样本数与效应。

### 步骤

1. 生成并冻结 train/calibration/confirmation manifests，验证哈希、平衡和独立性。
2. 对每个种子以共享初始化分别训练 NTP、shared-aux 与 informative-MTP。
3. 只用 calibration 按第 6.1 节选择共同能力检查点；不读取 confirmation 补丁结果。
4. 对每个模型进行完整前向与增量缓存重放，验证无补丁一致性。
5. 提取接收体和真实供体第二层 `U03` K/V；记录 shape、样本 ID、分支和 nuisance ID。
6. 执行自补丁、同分支补丁和标准头输入正控制；任一守卫失败即停止该种子确认评估。
7. 对 confirmation 的全部 12 个有序异分支对执行模型内联合 K/V 补丁；保持接收体其他缓存、`A_SHARED` 和 $Q_{2,T+1}$ 不变。
8. 计算样本级切换、按分支对汇总、按种子得到 $C_o$、$\Gamma_{info}$ 与次要 $\Gamma_{system}$。
9. 应用预注册的通过/失败/证据不足规则，不根据 margin 或注意力图改判。
10. 生成一张中央图、能力表、控制表、分支对表和 `hypothesis_decision.json`。

### 输出与调试产物

```text
tables/data_guard.csv
tables/capability_match.csv
tables/cache_audit.csv
tables/patch_controls.csv
tables/causal_use_by_seed.csv
tables/causal_use_by_pair.csv
tables/secondary_margin_metrics.csv
tables/gradient_diagnostics.csv
figures/kv_causal_use_main.png
hypothesis_decision.json
run_manifest.json
```

### 阶段停止原因

- `DATA_OVERLAP_OR_IMBALANCE`
- `CLEAN_CAPABILITY_FAIL`
- `CAPABILITY_MISMATCH`
- `SOURCE_FORMATION_FAIL`
- `CACHE_REPLAY_FAIL`
- `SAME_BRANCH_CONTROL_FAIL`
- `POSITIVE_CONTROL_FAIL`
- `PAIR_COVERAGE_FAIL`
- `CONFIRMATION_LEAKAGE`

## 12. 通过、失败与证据不足

### 通过

1. 五个种子全部通过数据、能力、缓存、同分支、正控制与配对守卫；
2. 至少 4/5 个种子满足 $\Gamma_{info,s}\ge0.10$；
3. $\bar\Gamma_{info}\ge0.10$；
4. 没有稳定反向的有序分支对组。

允许结论：在该 A11 K=2、2 层标准 CE 模型和第二层 `U03` K/V 接口上，信息性未来目标相对训练结构与能力匹配的 shared-aux，增强了标准主头对该源通道的强行为因果使用。

这里的“信息性未来目标”是全位置 K=2 CE 目标包，不是只在 `U03` 施加的局部标签；本实验保持一般 LLM 训练形式，因此不单独拆分 horizon 与局部 target content。

### 失败

所有守卫通过，并满足任一项：

- $\bar\Gamma_{info}\le0$；
- 至多 2/5 个种子达到 `0.10`。

若 $C_{info\text{-}MTP}$ 与 $C_{shared\text{-}aux}$ 都为正且相近，应记录“两种辅助训练都使用该通道、信息内容特异增强失败”，不能写成“主头没有使用 MTP 模型中的信息”。

### 证据不足

- 恰好 3/5 个种子达到阈值；
- $0<\bar\Gamma_{info}<0.10$；
- 任一必要守卫失败；
- 能力匹配检查点不存在；
- 结果依赖事后层选择、阈值或供体筛选。

## 13. 结论边界

即使通过，也只证明该受控任务、该模型规模和该 K/V 接口上的强反事实答案控制增量。不能推出：

- MTP 在真实 NLP、代码或长上下文中更好；
- 更大 $K$ 更好或更差；
- 标准主头使用了所有 MTP 信息；
- 效应只由 `U03` 局部 branch 标签而不是全位置 K=2 目标包造成；
- K 与 V 各自承担什么作用；
- 接收位置 Q 不重要；
- 模型形成可泛化的组合算法；
- 表征更可拆分或 MoE Router 会受益。

若只观察到稳定 margin 变化而无答案切换，应写成“存在候选弱因果影响，但强行为使用未通过”，不能用次要指标升级主要结论。

## 14. 审核记录与 Protocol 变更

### 已由研究者确认

- 主问题是信息性未来目标是否在匹配辅助训练结构之外增强标准主头使用，而非一般信息形成；
- 主干预采用源位置 K/V，不采用 Q；
- 主要比较 shared-aux/informative-MTP；NTP 只作次要系统基线；
- 唯一主要指标是 $\Gamma_{info}$；
- 每个活跃预测头使用标准全词表交叉熵。
- 双头条件采用平均 loss；这只匹配名义系数，不匹配实际梯度。

### 仍等待本次审批的具体合同

- 两层、`d_model=64`、单头模型；
- 数据量 `4096 / 256 / 1024` 个基础配置；
- AdamW `3e-4`、最多 15,000 步；
- 共同检查点与 CE 差 `0.05`；
- 主要阈值 `delta_info=0.10`；
- 同分支控制 `0.05`、正控制 `0.95`；
- 5 个种子和 4/5 一致性规则。

研究者已批准上述值及四卡远程执行。实现必须先通过完整 smoke，再提交正式任务；不得根据 smoke 或确认结果修改阈值、层、供体或主要指标。

### 已授权执行记录

- ACP job ID：`pt-pz6zjzzn`
- 提交时间：`2026-07-15T15:58:51Z`
- 资源：单节点 `n6ls.iu.i40.4`，4 张 N6LS-80GB GPU
- run name：`a11_03_02_e01_model_local_kv_causal_use_4gpu_20260715_1605`
- 最终状态：`SUCCEEDED`，完成于 `2026-07-15T15:59:58Z`
- 冻结判定：`fail`；$\bar\Gamma_{info}=0.01675$，`0/5` 种子达到 `0.10`
- 结果目录：`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_03_02_e01_model_local_kv_causal_use/a11_03_02_e01_model_local_kv_causal_use_4gpu_20260715_1605`
- 日志目录：`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a11_03_02_e01_model_local_kv_causal_use_4gpu_20260715_1605`
