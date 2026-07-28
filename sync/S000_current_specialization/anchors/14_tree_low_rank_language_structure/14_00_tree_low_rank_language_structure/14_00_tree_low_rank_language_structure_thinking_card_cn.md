# 语言树低秩传播 Thinking Card

来源：研究者在所引用的 2026-07-17 讨论中给出的判断，以及 2026-07-18
“按照这个建模，开始设计实验然后完成，不用审核，所有直接执行”的明确授权。

## Human Draft

**Phenomenon / 现象：**

语言可以先近似为由短 sequence 递归组合成长 sequence 的层次结构。叶子短句的表示被认为具有低有效秩；希望判断这种低秩是否能逐层传播到父节点和根节点，以及真实语料和真实模型是否近似满足该模型。

**Mechanism guess / 机制猜想：**

不同叶子表示共享一个低维空间；父节点的组合主要复用这个共享空间，并且不会在每一层持续引入或放大大量新的独立方向。因此低秩信号可以从叶子传播到高层。

**Strongest rival explanation / 最强替代解释：**

研究者明确提出两项替代可能：真实语言包含复用、重入或环状关系，不是严格树；使用 Transformer 观察低秩可能只说明该 Transformer 的表示性质，而不是语言结构本身的性质。

**Most uncertain point / 最不确定之处：**

真实语料是否足够接近树状组合，以及真实模型的父节点表示是否能由共享、稳定的子节点组合算子解释。

**Evidence that would change my mind / 改变判断的证据：**

如果叶子不共享可泛化的低维空间、真实父子关系不比长度匹配的随机关系更容易由共享算子解释，或破坏树结构不改变表示秩，则应修正或放弃“树状组合解释真实低秩”的机制判断。

**Current next decision / 当前唯一决策：**

直接执行从理论/合成校验到真实语法树、预训练模型和因果训练的分阶段实验，并依据预注册的 pass/fail/insufficient 规则给出结论。

## Optional Formalization

**Key variables / 关键变量：**

$H_\ell$（同一树层跨样本节点表示矩阵）、$k$（叶子共享秩预算）、$A_\ell$（树聚合算子）、$W_\ell$（共享特征变换）、$E_{\ell+1}$（组合创新残差）、$B_\ell$（理论误差上界）。

**Causal relation / 因果方向：**

共享低维叶子状态与稳定组合算子决定高层尾部能量；改变潜在维度或破坏树关系应改变模型中的低秩结构。

**Primary observable metric / 主要观测指标：**

固定 $k$ 下的尾部能量比例

$$
\tau_k(H)=\frac{\sum_{i>k}\sigma_i(H)^2}{\sum_i\sigma_i(H)^2},
$$

及其 95% 能量秩 $r_{0.05}(H)$。真实语料和模型阶段使用 held-out 投影误差、真实树相对伪树的压缩差和父子组合残差差。

**Pass / fail / insufficient evidence：**

- Pass：定理界通过数值校验；真实叶子子空间可泛化；真实树优于长度匹配伪树；父子共享算子有测试集优势；树结构干预改变秩。
- Fail：有效实现和样本量充分时，关键真实树差异为零或反向。
- Insufficient：样本数造成形状低秩、低秩只来自未中心化均值/位置/pooling、模型未学会任务，或理论界在真实模型中始终为空泛上界。

## AI Audit Record

**Judgments to preserve / 必须保留的人的判断：**

先证明条件定理，再分别验证真实语言和真实模型是否满足前提；Transformer 是观测对象而不是理论前提；树只是第一版近似。

**Unclear definitions / 未定义对象：**

原讨论未唯一确定节点表示、有效秩阈值、真实树类型和组合算子的估计方式。

**Hidden assumptions / 隐含假设：**

“每个叶子低秩”必须加强为跨样本共享低维空间；父节点必须使用共享或子空间保持算子；单个根向量不能谈低秩；树层与 Transformer 层必须分开。

**Metric mismatch / 指标错配：**

短 sequence 的 token-by-d 矩阵天然秩不超过长度；mean pooling 会随 span 长度机械压缩；未中心化 PCA 可能只测到公共均值或 rogue dimensions。

**Candidate correction proposed by AI / AI 候选修正：**

以跨树节点矩阵的 held-out 95% 能量秩为主指标；预训练模型主表示使用共同单 token readout；真实树必须与长度/数量匹配的非成分或随机树比较；加入初始化 checkpoint 和因果训练对照。

**Human decision on the proposal / 人的最终确认：**

研究者在 2026-07-18 明确要求按该建模直接设计、执行、分析并给出结论。该授权允许上述防伪修正进入执行合同；运行后的最终机制判断仍由测量结果约束。

## Boundary

本文件只保存研究者的初始判断与 AI 审计记录，不是 Protocol 或结果报告。
