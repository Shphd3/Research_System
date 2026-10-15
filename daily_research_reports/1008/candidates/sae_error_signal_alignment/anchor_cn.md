# 候选 Anchor：SAE 相似性与原生损失梯度方向

## 1. 问题定义

**问题：在固定的 S7fresh 和 Qwen3-0.6B-Base 中，SAE 激活模式相似的 token 位置，其真实下一词损失的误差信号 δ，是否比匹配随机位置更同向？**

研究者明确提出 H2“SAE 原子相似的 token，其误差信号 δ 也相似”，并授权先在当天 candidate 中构建设计、直接进行四卡 H100 reserved 诊断，无需额外审计通过。本文件不新建 Focus、不取代 canonical Anchor、不确认科学结论。问题为 `USER_ACTIVATED`；AI 补充的指标、对照和阈值为 `AI_PROPOSAL_UNDER_AUTHORIZED_CANDIDATE_SCOPE`；科学结论为 `Unknown`。

这里的 token 指带上下文的预测位置，不是词表中的一个词类。“SAE 原子相似”落实为两个位置的完整稀疏激活码相似，不是两根 decoder 列向量相似。δ 指真实下一词交叉熵对 SAE 所观测原生表征的梯度。

这是判断 SAE 分组能否连接到共享学习的局部前提。支持结果保留这一候选性质；非支持结果削弱这套 SAE 相似性定义；区间未分辨则保留未知。本次不训练 Router 或 Expert。

## 2. 物理先验

候选先验：相似的 SAE 激活模式可能聚集需要相似局部修正的位置。竞争解释：SAE 主要编码输入或词汇相似性，真实下一词目标和下游计算仍要求不同方向的修正。

两套 SAE 的观测接口不同。S7fresh 观测末块 Attention 输出投影、残差相加之前；Qwen 观测末层归一化后的 MLP 输入。分别在各模型、各接口内检验，不能因维度相同就认为误差信号相同。

## 3. 可证伪假设

H2 的可测预测：对 readout 位置，从 fit 中只凭 SAE 码选出的五个近邻，其平均 δ 方向余弦为正，而且高于同领域、同位置区间的二十次随机参考抽样。

主要竞争解释是领域、位置或当前 token 身份造成了表面相关。主近邻和随机对照使用同领域、同位置区间候选池；原生表征近邻和严格相同当前 token 子群检查这些解释。真实下一词只用于计算 δ 和事后分层，不参与选近邻。

本次检验的是冻结模型中的预测关联，不直接识别语义因果机制，也不检验路由收益。

## 4. 数学模型

对位置 i，a_i 是 SAE 观测的 1024 维原生张量，z_i 是 30000 维非负 Top-32 激活码，y_i 是文本中真实的下一 token。模型下游计算固定，定义：

\[
\ell_i=-\log p_m(y_i\mid\text{prefix}_i),\qquad
\delta_i=\nabla_{a_i}\ell_i.
\]

ℓ_i 是该位置的下一词交叉熵，δ_i 是降低这项损失所需修正方向的反向信号；下降方向是 −δ_i。δ 由原模型计算，不含 SAE 重构损失梯度。

计算 SAE 相似性时，激活码各坐标乘对应 decoder 列范数，再计算余弦。对 readout 位置 i，从 fit 候选池选五个 SAE 近邻 N_i；随机对照 R_i 抽二十次，允许重复，但排除 N_i。选位置时不使用 δ 或 y。

主指标是近邻相对随机参考的梯度同向优势：

\[
s_i=\frac{1}{5}\sum_{j\in N_i}\cos(\delta_i,\delta_j)
-\frac{1}{20}\sum_{j\in R_i}\cos(\delta_i,\delta_j),\qquad
S=\frac14\sum_{d=1}^{4}\operatorname{mean}_{\text{领域 }d\text{ 的记录}}
\operatorname{mean}_{i\text{ 属于该记录}}s_i.
\]

余弦和 S 均无量纲。先记录内平均，再各领域内平均，最后四领域等权，防止有效位置较多的领域占更大权重。S 为正也可能只是“较少反向”，因此支持 H2 还要求近邻的绝对平均余弦为正。

与参数兼容性的关系有条件。对输入为 u_i、输出误差梯度为 κ_i 的线性投影：

\[
G_i=\kappa_i u_i^\top,\qquad
\cos_F(G_i,G_j)=\cos(\kappa_i,\kappa_j)\cos(u_i,u_j).
\]

S7 的输入是 c_i，输出误差梯度 κ_i 就是该 SAE 接口上的 δ_i。Qwen 的 down projection 输入是门控中间激活，κ_i 是 down projection 输出梯度；SAE 观测的 MLP 输入梯度 δ_i 通常不等于 κ_i。因此参数梯度只使用真实投影输入和输出梯度作次级测量，不能把 S7 公式中的 δ 直接搬到 Qwen。即使 δ 同向，也不能无条件推出完整参数更新兼容、有限步降损或长期路由收益。

## 5. 计算实现

1. **测量 H2。** 固定抽取 1024 条自然文本，记录不重叠地分为 fit 和 readout。在每条十六个固定位置采集 a、δ、SAE 稀疏码及真实下一词。主干和 SAE 全部冻结，只计算自然下一词损失，保证 δ 来自真实任务。
2. **隔开选邻居和答案信息。** 只用 fit 输入表征选 SAE 近邻、原生 a 近邻，在同领域和位置区间内与随机参考比较；增加严格相同当前 token 子群和 δ 打乱负对照。它们检查词汇或匹配条件能否解释关联，而不是凭结果挑有利配对。
3. **报告有界证据。** 按记录、领域聚合并 bootstrap readout 记录，fit 参考固定。输出优势区间、近邻绝对余弦、负余弦比例、有效覆盖和真正参数梯度方向。回答局部关联，不把未运行的共享更新写成结论。

[Protocol](protocol_cn.md) 冻结抽样、有效掩码、计算和执行范围。

## 6. 最小证伪检验

每个模型独立判断。测量资格要求至少 256 条有效 readout 记录、至少 90% 计划 readout 位置有效。按领域分层抽样记录 2000 次，得到双侧 95% percentile 区间。

- `SUPPORT`：S 的区间下界大于零，且近邻绝对平均 δ 余弦的区间下界大于零。
- `NON_SUPPORT`：S 的区间上界不大于零。
- `INSUFFICIENT`：其余情况，或测量资格未达到。

零阈值是 AI 提议的关联阈值，不是 Router 实用收益门槛。分别报告两个模型，不把两个局部检验自动推广为总体规律。原生 a、当前 token、中心化 SAE 码和打乱 δ 的次级结果不能挽救主指标失败。严格当前 token 子群不足 64 条 readout 记录时，只作描述。

## 7. 当前证据

**H2 结果：NOT RUN。** 目前确认的是资产身份，不是 H2。

S7fresh 的 exact 33B-token checkpoint 为八层模型、1024 维 Attention 输出、30000-feature Top-32 SAE、重构权重 0.1。旧缓存已有 a、δ 和对齐的 SAE 码；本轮重新选记录并采集。[现有 local-update 完整报告](../../local_update/full_report_cn.md) 记录相关一步更新证据与边界。

Qwen3-0.6B-Base 的最后层 MLP-input SAE 在冻结主干上训练了 1,000,001,536 DCLM tokens。本轮已读取 checkpoint，核对 config hash 和张量形状；[原 Summary](../../../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E16_dclm_final_layer_topk_sae_teacher/summary.md) 证明字典训练技术合格，未证明语义和路由有效。

已准备的新样本与 20260925 旧 1024-record 面板精确重叠为零，但与 20260930 的旧 2048-record NTP-statistics 面板重叠 768 条。来源语料之前已经审计，缺少 paper ID。本轮 readout 不称为未接触 confirmation。

## 8. 结论边界与下一决策

能回答的是：指定模型状态、指定 SAE 接口中，仅凭输入 SAE 相似性是否能预测真实下一词梯度方向，并报告对照和不确定性。词汇或目标混淆、固定参考池依赖、记录近似独立和跨状态迁移仍有边界。

不能声称 SAE 原子导致误差相似、δ 同向必然让完整更新兼容、Router 改善训练、哪些 Expert 必须共享，或两模型的误差张量相同。科学确认仍由研究者作出。

**唯一下一决策：** 两个冻结检验及对照完整报告后，由研究者判断是否保留 SAE 相似性作为候选分组信号。完成标准是两模型均有测量、资格和各自结果分支；恢复工作从分析表和执行收据开始，不自动启动 Router 训练。
