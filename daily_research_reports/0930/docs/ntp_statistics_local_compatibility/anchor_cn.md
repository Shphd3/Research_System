# Anchor：自然语言统计与局部更新结构

执行更新2026-09-30：严格 Smoke 与完整 Full 已记录于 [Summary](summary_cn.md)和 [Detailed](detailed_cn.md)；主裁决 INSUFFICIENT，研究者科学判断 Unknown。下方登记科学正文（含运行前证据／下一决定快照）保持原值，未提升科学结论状态。


2026-09-30，Asia/Shanghai。`CANDIDATE_FOR_REVIEW`；结果 `NOT RUN`；候选标识 `ntp_statistics_local_compatibility`。研究者确认有符号相容性、自然目标混合，以及将已有 SAE 用作领域/方向敏感性分析工具；具体假设、估计器、取样和阈值仍为 **AI_PROPOSAL**。[英文](anchor.md)；[实验方案](protocol_cn.md)。不重置 Focus。研究者现已授权初始实现、Smoke 与资格通过后的 Full，不确认科学结果或解释。

## 1. Problem Definition

**固定语言模型状态与共享注意力块，自然文本是否呈现可重复的局部更新结构，并能分清有符号平均需求与预测敏感方向？**领域和真实目标是第一组条件变量，不是全部语言结构的定义。上位目的仍是理解哪些学习关系可能指导后续数据共享；现有读出尚未建立这条桥。

一项有界实验使用选出的学术片段。一阶主检验看目标可比较时领域均值差是否复现，配套有符号跨作用与自然目标混合。另设必做功能分析，看 native 输出哪些方向改变预测，已有冻结 SAE 字典提供 feature 坐标。不预设 SAE 优越、语义命名、事前预测或长期分配成立。均值不支持仍可有功能结构答案，两类证据不替代彼此。

## 2. Physical Priors

**候选先验：**上下文—续写结构与模型偏差可能产生重复的平均需求；即使没有偏差，模型预测也可能对一组有结构的输出方向敏感。表征与下游敏感性共同决定梯度。Fisher/KL 关系是数学推导，不是领域功能差异的经验证据。

边际 Zipf 型频率、激活各向异性、中心化梯度波动、有符号均值作用各有含义，均不证明冲突。总体梯度小可能掩盖群体抵消，但不预设驻点。共同敏感方向不等于已测容量竞争或分 Expert 理由。

## 3. Falsifiable Hypotheses

**主 H1：**目标匹配、子领域均衡后，领域均值对比跨批一致性超过历史梯度平方尺度的候选 1%。竞争解释：组成、有限样本均值误差或一般平均效应，没有复现的条件差异。

**功能 H2：**领域条件的模型 Fisher profile 存在可复现差别，包括 H1 不支持的情形。竞争解释：共同敏感性、目标/上下文组成、尺度或探针噪声造成表面差别。**工具 H3：**冻结 SAE 坐标能展示可复现的出现/敏感性模式；用同秩 PCA/随机对照区分一般方向结构与字典特有描述，不要求 SAE 胜出。有符号相容性、混合和经验协方差诊断继续必做。H2/H3 各有描述性结果，尚未提出确认性门槛，不救回 H1。

## 4. Mathematical Model

上下文 \(x\)、真实目标 \(y\)、领域 \(s\)，固定全部参数 \(\theta_0\)。\(c\) 为共享矩阵输入，\(a=W_0c\) 为 native 输出，\(r\) 为残差，logits \(z=g_{\theta_0}(a,r)\)、概率 \(p=\operatorname{softmax}(z)\)、one-hot \(u_y\)、损失 \(\ell=-\log p(y)\)，\(J=\partial z/\partial a\)。于是

\[
e=J^\top(p-u_y),\qquad G=ec^\top,\qquad
K_{ij}=\langle G_i,G_j\rangle_F=(c_i^\top c_j)(e_i^\top e_j),\qquad
\Delta\ell_j=-\eta K_{ij}+O(\eta^2).
\]

末式要求仅 W 做足够小的普通 SGD 步。未知真实续写 \(q_x=P_{\rm data}(Y\mid X=x)\) 给出 \(\mathbb E[G\mid x]=J_x^\top(p_x-q_x)c_x^\top\)。p=q_x 时选出目标均值仍可非零；单续写/上下文不能辨识校准。

定义**模型 Fisher**，对模型 p 下的目标求期望，无须预设校准：

\[
F_a(x)=J_x^\top[\operatorname{Diag}(p_x)-p_xp_x^\top]J_x,\qquad
D_{\rm KL}(p_a\Vert p_{a+\delta a})=\tfrac12\delta a^\top F_a(x)\delta a+o(\|\delta a\|^2).
\]

这项局部 native 输出变化固定 x/r/其他参数。p_x=q_x 时条件平均梯度零且 Cov(e|x)=F_a(x)；按列向量化有

\[
\operatorname{Cov}(\operatorname{vec}G\mid x)=(c_xc_x^\top)\otimes F_a(x)\qquad(p_x=q_x).
\]

这是条件恒等式，不是总体低秩结论。未校准时，真实目标二阶矩/协方差不等于模型 Fisher。直接测模型敏感性，不推断 q_x，也不以真实目标代替模型期望。[经验 Fisher 的局限](https://arxiv.org/abs/1905.12558)支持这项区分。

已有 SAE 编码 \(a\)，不编码 \(c\)：\(a\approx b_{\rm SAE}+D\alpha\)，bias 固定，\(d_k\) 是单位 decoder 列，\(\alpha\) 是稀疏系数。局部读出为

\[
I_k(x)=d_k^\top F_a(x)d_k,\qquad F_\alpha(x)=D^\top F_a(x)D,\qquad \delta a=D\delta\alpha.
\]

这个坐标图在 native a 周围固定重构残差，不以重构替换 a，也不对 TopK encoder 求导。并列激活与 I_k，区分是否出现、预测对该方向是否敏感。F_alpha 半正定但非对角可为负，该符号不是跨数据帮助/不利。非正交 atom 敏感性不可相加为独立容量或能量份额。

保留主选择均值 \(\mu^b_{s,y}=\mathbb E_b[G\mid s,y,\text{selection}]\)、两池 \(b=F,R\)、四目标 \(\mathcal Y_*\)、历史参考 \(v_0\)：

\[
T=\frac1{24v_0}\sum_{y\in\mathcal Y_*}\sum_{s<t}
\langle\mu^F_{s,y}-\mu^F_{t,y},\mu^R_{s,y}-\mu^R_{t,y}\rangle_F,\qquad
S^{\rm cond}_{st,y}=\frac{\langle\mu^F_{s,y},\mu^R_{t,y}\rangle_F+\langle\mu^F_{t,y},\mu^R_{s,y}\rangle_F}{2v_0}.
\]

每项 T 为 S_ss+S_tt-2S_st，差异为正不要求负相容性。全部自然位置另用均值 nu_s,y、边际目标权重 q_s(y)、M_s=sum_y q_s(y)nu_s,y，再把 M 代入 S。等目标混合 S 含跨目标项，不同于同目标 S 平均。功能 profile 按明确的上下文/目标取样总体条件化，不测真实目标条件 Fisher。

## 5. Computational Realization

复用冻结 S7 33B、纯 NTP、`model.blocks[7].attn.o.weight`（1024×2048）。同检查点的 TopK32 SAE 有 30,000 atoms，观察残差相加前的 native 1024 维注意力输出；核实的 encode/decode/dictionary 接口给出系数与方向。无辅助损失、新 SAE 或优化器。

逗号、空格+the、空格+of、句号的文档不共享四元组用于 T/S；每记录全部 16 位置另算自然/共同支持/等目标关系。先核对曝光与重复资格。

功能分支在预设均衡上下文面板上，将真实目标方向梯度矩与模型 Fisher 探针分开计算。并列全部 atom 的激活/条件幅值、模型 Fisher 敏感性、激活与未激活上下文；只按 F 激活选共同/富集及展示集合，不按 R 或 Fisher 分数选。固定 F native-a PCA、固定种子的随机正交方向提供同秩对照。同样探针/权重应用于各工具及正交化 decoder span；decoder 坐标与 span 汇总含义不同。面板、探针、资格及预算由 Protocol 持有。空集合或对照同样解释结构均为正常结果。

## 6. Minimal Falsification Tests

H1 保留单一主裁决：192 不共享四元组、经预先校准的候选分层 Welch 95% 区间。合格下界 >0.01 支持，上界 <0.01 不支持候选尺度，重叠/资格失败则不足。有符号 S 未有合格符号区间，保持探索。

H2/H3 独立交付：R 前冻结 F profile/集合/方向，报告共同与领域偏离、R profile 迁移、模型 Fisher 与真实目标矩、Monte Carlo 噪声及同秩对照。不以挑出的 atom、未校正 feature 检验或能量占比认定机制。单元不足、探针资格或未测资源可行性限制功能分支，不改 H1 结果。

已知例须区分：零均值/非零 Fisher、高激活/低敏感、低激活/高敏感、S 全正但差异复现、非正交 atom 重合。只报告有资格的描述性复现，不臆造新功能效应门槛或总体检验。

## 7. Current Evidence

[预测 Summary](../summary_cn.md)：Q=-0.000138（置信上界 0.002294），不支持注册 5% 改善。[领域 Summary](../domain_update_geometry/summary_cn.md)：Q_D=-0.005715、推断未校准；同目标 cosine 约 0.193、异目标约 0.00046；共同 SAE rank64 的 K 重建误差 0.803。已有研究测过全部 atom 激活和方向梯度能量，未确立模型 Fisher 敏感性或因果使用。

元数据在预筛查前满足每单元 12 端点，不是独立性证书。新 T/S、混合关系、功能 profile、对照均为 **NOT RUN**。[SAE 来源审计](sae_tool_source_audit.json)记录已读接口，不是新模型测量。

## 8. Claim Boundary And Next Decision

结论限于检查点、参数块、来源记录、测量位置。平均需求、有符号一阶关系、模型敏感方向、SAE 出现、经验协方差各自独立。敏感 decoder 方向不证明语义纯度、必要性、容量消耗、跨数据冲突、可行路由或长期收益。条件输出编辑是局部敏感性探针，不是已验证的共享参数干预。

**唯一下一决定：**审阅这项均值加功能分析，作为后续预测/路由目标选择前的有界研究。H1 失败时功能结构仍有价值；SAE 与对照持平只限制字典特有解释，不否定模型结构。研究者确认 SAE 是工具，精确功能操作化与执行资格仍为提案/阻塞。从 Protocol 资格门续接，长期互动留在本轮之外。
