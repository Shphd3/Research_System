# A11_02_01_E01 K=2 语义切向核传递实验 Protocol（中文审核稿）

## 0. 审核摘要

**批准状态：** 用户已于 2026-07-10 授权后续正式 Anchor 直接执行；当前进入实现与运行阶段。  
**目的：** 判断 K=2 隐藏状态语义信号是否能按切向核预测传到 Transformer 参数空间。  
**主 Anchor：** `../../../../problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/subanchors/11_02_01_reachability_and_background_sign_anchor.md`。
**唯一问题：** 原生共享编码器雅可比是否具有正的语义传递系数，且 K=2 直接项在扣除共享目标干扰后仍产生正参数空间语义速度？  
**实验角色：** 根因审计，不是方法比较。  
**主指标：** \(G_{\theta,total}=G_{\theta,direct}+G_{\theta,background}\)，以及核预测 \(v^\top\Theta v/m^2\)。  
**最小设置：** K=2 clean decision-only、一层 Transformer、固定输出头、5 个种子、语义雅可比缩放 \(\alpha\in\{0,0.5,1\}\)。  
**通过：** 核测量满足零点/二次缩放，原生雅可比 \(\alpha=1\) 的共享编码器净语义速度在至少 4/5 种子为正，真实一步 margin 变化与线性预测一致。  
**失败：** 隐藏状态直接速度为正，但共享编码器的原生核传递或净参数速度非正；或背景项稳定反转直接项。  
**证据不足：** 前向不一致、核恒等式失败、梯度数值退化，或非线性余项大到一步符号不可判定。  
**不能声称：** 自然语言收益、LLM scaling、全位置样本效率、一般 K 或 MoE 收益。  
**执行决策：** 英文 canonical `protocol.md` 固化后，完成两轮 smoke，再提交远程一机四卡 full run。

## 1. 术语解释

| 术语 | 直白含义 | 计算式 | 本实验作用 | 不能证明什么 |
|---|---|---|---|---|
| 参数语义速度 | 一次 SGD 参数更新在一阶上让语义 margin 增长多少 | \(G_{\theta}=-\langle\nabla_\theta M,\nabla_\theta L\rangle\) | 主判据 | 多步收敛 |
| 核信号 | 共享编码器参数沿语义方向的局部可达强度 | \(S_\Theta=v^\top\Theta v/m^2=\|\nabla_\theta M\|^2\) | 判断参数瓶颈 | 含背景时的净速度 |
| 直接项 | 第二词 \(S_Z\) 的交叉熵梯度 | \(G_{\theta,direct}\) | MTP 目标信号 | 总训练结果 |
| 背景项 | 共享下一词 \(A\) 的梯度投影 | \(G_{\theta,background}\) | 判断抵消或帮助 | all-position 背景 |
| 净保留率 | 加入共享目标后，直接语义速度保留了多少且是否反号 | 直接项超过数值地板时，\(\rho_{\theta,net}=G_{\theta,total}/G_{\theta,direct}\) | 无量纲判断背景抵消 | 绝对学习速度 |
| 核余弦 | 语义方向和共享目标方向分别通过共享编码器后的对齐程度 | \(\chi_\Theta=\cos(J^\top v,J^\top c)\) | 判断背景项为何为正或负 | 有限步真实损害 |
| 核范数比 | 共享目标参数梯度相对语义参数梯度的强度 | \(r_\Theta=\|J^\top c\|/\|J^\top v\|\) | 判断背景抵消幅度 | 长期收敛 |
| 雅可比缩放 \(\alpha\) | 折叠参考状态相同，之后共享编码器真实雅可比按语义方向缩放 | \(H_\alpha(\theta)=\bar H_0+D_\alpha(H^{raw}(\theta)-H_0^{raw})\) | 因果校准核传递 | 自然架构差异 |
| 一步余项 | 真实一步变化减去线性预测 | \(R=(\Delta M-\eta G_\theta)/\eta^2\) | 判断有限步可信度 | 长期曲率界 |

## 2. Anchor 对齐

**决策问题：** 隐藏状态上的 K=2 直接语义速度是否被共享编码器参数化吸收，而不是只更新分支 token 的独立 embedding 行？  
**物理先验：** 参数学习只能沿 \(J^\top v\) 发生；核强度随语义雅可比缩放的平方变化。  
**核心模型项：** \(v^\top\Theta v\)、背景投影和一步非线性余项。  
**主反例：** \(G_{hidden}>0\)，但共享编码器 \(\kappa_2\approx0\) 或 \(G_{\theta,total}\le0\)。  
**结论边界：** 仅限受控 K=2、固定头、decision-only、SGD 局部动力学。

## 3. 被检验假设

### H1：核校准与二次缩放守卫

在参考检查点状态和 logits 完全相同的条件下：

\[
\frac{S_\Theta(0)}{S_\Theta(1)}\le10^{-6},
\qquad
0.225\le\frac{S_\Theta(0.5)}{S_\Theta(1)}\le0.275.
\]

同时，在参考检查点，direct-only 条件满足：

\[
\frac{|G_{\theta,direct}-S_\Theta|}{|S_\Theta|+10^{-12}}\le10^{-4}.
\]

这些等式由干预和规则单纯形构造保证。通过只说明实现有效，不构成“共享编码器能吸收语义”的科研证据；若失败，整次运行判为实现无效。

共享 H1 目标在折叠参考点产生分支公共隐藏下降方向 \(c=(b,\ldots,b)\)，满足 \(v^\top c=0\)。因此还必须验证：当背景项超过数值地板 \(|\eta G_{\theta,background}(1)|\ge10^{-10}\) 时，

\[
0.45
\le
\frac{G_{\theta,background}(0.5)}
{G_{\theta,background}(1)}
\le
0.55.
\]

并逐种子验证总速度重构：

\[
G_{\theta,total}(\alpha)
=\alpha^2G_{\theta,direct}(1)
+\alpha G_{\theta,background}(1),
\]

以原生参考尺度 \(|G_{\theta,direct}(1)|+|G_{\theta,background}(1)|\) 归一化后的残差不超过 \(10^{-4}\)。之所以不用预测值作分母，是因为 \(\alpha=0\) 的理论预测严格为零。直接项二次缩放和背景项线性缩放都是实现校准，不作为 MTP 优势证据。

### H2：直接信号能否压过共享目标干扰

原生共享编码器雅可比 \(\alpha=1\) 必须有：

\[
G_{\theta,direct}>0.
\]

标准 K=2 总损失至少在 4/5 种子满足：

\[
G_{\theta,total}=G_{\theta,direct}+G_{\theta,background}>0.
\]

等价地，至少 4/5 种子满足 \(\rho_{\theta,net}>0\)。\(G_{\theta,direct}>0\) 的“明确为正”只在 \(|\eta G_{\theta,direct}|\ge10^{-10}\) 时判定；低于该数值地板记为不可分辨，不把浮点噪声写成传递证据。

在 \(\alpha=1\) 上还应满足精确诊断关系：

\[
\rho_{\theta,net}=1+\chi_\Theta r_\Theta.
\]

它把“是否反转”分成方向因素 \(\chi_\Theta\) 与强度因素 \(r_\Theta\)，但二者仍是局部参数几何，不能单独代表真实训练损害。

### H3：一步与早期有限步保真

主学习率下，对 \(\alpha\in\{0.5,1\}\) 且 \(|\eta G_{\theta,total}|\ge10^{-10}\) 的条件，至少 4/5 种子满足：

\[
\operatorname{sign}(\Delta M)=\operatorname{sign}(G_{\theta,total}),
\]

\[
\frac{|\Delta M-\eta G_{\theta,total}|}
{\eta|G_{\theta,total}|+10^{-12}}\le0.25.
\]

前 200 步中，`direct_only_k2` 的 margin 早期面积和 native H2 恢复应满足 \(\alpha=1>0.5>0\)。`full_k2` 只有在参考点净速度为正时才要求相同排序；若一步通过但排序迅速消失，则结论收缩为局部核传递。

本地 Y1 守卫只适用于训练了 \(L_1\) 的 `shared_only_k1` 和 `full_k2`：`full_k2, alpha=1` 的最终 Y1 accuracy 不低于 `shared_only_k1` 超过 `0.05`，且自身不低于 `0.90`。\(L_1\) AUC 差异完整报告，但不以一个任意很小阈值否决参数传递机制。

## 4. 竞争解释

1. **输出头共同适配：** 固定 H1/H2 头，且记录 drift 必须为零。
2. **参考点前向状态未真正折叠或被 \(\alpha\) 改变：** step 0 每个精确分支状态以及不同 \(\alpha\) 的 hidden/logit/loss 最大绝对差必须不超过 \(10^{-7}\)。训练后的轨迹本来就应随分支与 \(\alpha\) 不同。
3. **自动微分实现错误：** 用 \(\|\nabla_\theta M\|^2\) 与向量-雅可比积的核值双重校验。
4. **共享目标伪装成直接语义信号：** 分别计算 direct-only、shared-only 和 full loss。
5. **一步正确但非线性立即破坏：** 同时记录 \(\eta\) 与 \(\eta/2\) 的虚拟一步余项，并跑 200 步短曲线。
6. **独立 embedding 查表解释：** 分支 token embedding 保持不同但完全冻结；主核和主速度只对 attention、MLP、LayerNorm 与位置参数组成的共享编码器计算，并记录 embedding 梯度必须为零。
7. **原始编码器没有看到分支差异：** 折叠前的分支状态或其共享编码器雅可比必须存在非零分支差异；折叠后的参考状态分离必须为零。否则无法区分“共享编码器零空间”和“输入实现没有分支信号”。
8. **参数组遗漏：** attention、MLP、LayerNorm 与位置参数的 \(\|\nabla M\|^2\) 之和必须重构共享编码器总核信号，防止只记录部分参数得到假结论。

固定 H1/H2 头的交叉正交误差及共同状态上的类别 logit 极差必须不超过 \(10^{-6}\)；这是输出头构造守卫，与不同条件之间 \(10^{-7}\) 的前向一致性守卫分开。

## 5. 数据、模型与目标

### 数据

\[
Z\sim\operatorname{Unif}\{1,2,3,4\},
\]

\[
X_{\le T}=(\operatorname{BR}_Z,F_1,\ldots,F_{16},U_1,\ldots,U_4),
\]

\[
Y_1=A,
\qquad
Y_2=S_Z.
\]

每个分支只保留一个确定性前缀，完整训练 batch 为四个分支各一个样本；不加入分支内随机 filler、噪声后缀或数据增强。五个种子只改变模型、固定头和固定 embedding 的初始化。这样 \(H^{raw}\) 是四个精确状态的堆叠，理论中的参考点前向相等和核恒等式不依赖未控制的分支内残差。

分支 token embedding 使用不同的固定初值，并在整个实验中冻结。原始共享编码器由这些不同输入产生 \(H^{raw}(\theta)\)。令 \(H_0^{raw}=H^{raw}(\theta_0)\)，并把各分支参考状态的均值重复堆叠成 \(\bar H_0\)。诊断用 H2 softmax 只包含四个语义类别；四个输出行固定成规则单纯形，并构造在与共同折叠状态 \(\bar h_0\) 正交的子空间，使参考点 logits 均匀、softmax 公共项严格消失。定义：

\[
v=(v_1,\ldots,v_m),
\qquad
v_z=u_{S_z}-\bar u_2,
\qquad
\bar u_2=\frac1m\sum_z u_{S_z}.
\]

H1 预测头同样固定：目标 \(A\) 与三个未出现的干扰类别组成规则单纯形，其输出行张成空间同时正交于 H2 行空间和 \(\bar h_0\)。因此参考点 H1 logits 也均匀，且 \(L_1\) 在隐藏状态上的梯度对四个分支完全相同；若 \(G_{\theta,background}\ne0\)，只能由不同分支输入诱导的共享编码器雅可比产生，而不是隐藏空间中预先放入的语义重叠。

令 \(c=(b,\ldots,b)\) 表示该分支公共 H1 隐藏下降方向，令：

\[
a=J_{raw}^\top v,
\qquad
d=J_{raw}^\top c.
\]

参考点必须满足：

\[
G_{\theta,direct}(\alpha)=\frac{\alpha^2}{m^2}\|a\|^2,
\]

\[
G_{\theta,background}(\alpha)
=\frac{\alpha}{m^2}\langle a,d\rangle,
\]

\[
G_{\theta,total}(\alpha)
=\frac1{m^2}
\left(\alpha^2\|a\|^2+\alpha\langle a,d\rangle\right).
\]

参考点中心化干预定义为：

\[
H_\alpha(\theta)
=\bar H_0+D_\alpha\left(H^{raw}(\theta)-H_0^{raw}\right),
\qquad
D_\alpha=P_\perp+\alpha P_v,
\]

其中 \(H^{raw}=(h_1^{raw},\ldots,h_m^{raw})\) 使用四个精确分支决策状态，\(P_v=vv^\top/\|v\|^2\) 作用于它们的堆叠空间。在 \(\theta_0\) 上，所有受控状态等于 \(\bar h_0\)，但 \(J_\alpha=D_\alpha J_{raw}\) 保留不同固定输入对共享参数的导数差异。\(\alpha=1\) 表示使用原始共享编码器雅可比，但前向状态仍经过参考点中心化；它不是未经干预的自然 Transformer 训练。该干预是机制诊断，不是候选训练方法。

### 模型

- 一层因果 Transformer；
- `d_model=64`，单注意力头；
- 参数与激活使用 float64，因为本实验判定的是 \(10^{-4}\) 量级雅可比恒等式，而不是混合精度吞吐；
- token embedding 和预测头固定，只训练共享 attention、MLP、LayerNorm 与位置参数；
- full-batch SGD，无 weight decay；
- 主学习率沿用受控设置 `0.003`；虚拟半步使用 `0.0015`；
- 训练 200 步。

### 目标

- `shared_only_k1`：仅 \(L_1=\operatorname{CE}(q_1,A)\)；
- `direct_only_k2`：仅 \(L_2=\operatorname{CE}(q_2,S_Z)\)；
- `full_k2`：\(L_1+L_2\)。

## 6. 条件、种子与检查点

种子：`971,972,973,974,975`。

| 条件 | \(\alpha\) | 检验内容 | 为什么需要 | 证据类型 | 通过 | 失败 | 证据不足 | 主表 |
|---|---:|---|---|---|---|---|---|---|
| `shared_only_k1` | 1 | 无直接目标守卫 | 排除共享目标本身制造直接项 | guard | direct=0 | 出现伪 direct | 标签/梯度错 | `transmission_decomposition.csv` |
| `direct_only_k2` | 0 | 语义零空间干预 | 证明 hidden signal 可被参数化阻断 | primary | 核与参数速度近零 | 明显非零 | 参考点前向不一致 | `kernel_scaling.csv` |
| `direct_only_k2` | 0.5 | 二次缩放 | 校准核传递 | primary | 比值约 0.25 | 偏离预设区间 | 数值退化 | `kernel_scaling.csv` |
| `direct_only_k2` | 1 | 原生雅可比传递 | 判断共享编码器能否吸收信号 | primary | direct 速度为正 | 近零/负 | 梯度消失 | `transmission_decomposition.csv` |
| `full_k2` | 0/0.5/1 | 背景抵消和有限步 | 判断标准 K=2 的净进展 | primary | 原生净速度为正 | 背景反转 | 余项过大 | `finite_step_transmission.csv` |

检查点：`0,1,2,5,10,20,50,100,200`。总训练条件为每个种子 7 条，共 35 条；一步虚拟更新不新增训练条件。

## 7. 主指标

主判定按以下顺序进行：

1. 参考检查点前向一致性和核恒等式必须先通过，否则实验无效。
2. \(S_\Theta(\alpha)\) 必须满足零点与二次缩放，证明干预真正只控制传递强度。
3. 原生雅可比 `full_k2, alpha=1` 的共享编码器 \(G_{\theta,total}\) 决定参数空间信号是否存在。
4. \(\rho_{\theta,net}=1+\chi_\Theta r_\Theta\) 区分净速度符号来自方向还是强度。
5. 一步余项和 200 步曲线决定结论能否从局部扩展到早期有限步。

## 8. 次指标

- 隐藏状态直接语义速度 \(G_{hidden}\)；
- \(\kappa_2=S_\Theta/\|v\|^2\)；
- \(G_{\theta,direct}\)、\(G_{\theta,background}\) 和干扰比；
- \(\rho_{\theta,net}\)；
- \(\chi_\Theta\)、\(r_\Theta\) 以及 \(1+\chi_\Theta r_\Theta\) 重构误差；
- 真实/线性预测的 \(\Delta M\)；
- native H2 accuracy、目标概率、\(M_2\)、分支替换一致性；
- Y1 loss/accuracy；
- 梯度范数、head drift、核漂移；
- 冻结 embedding 梯度零守卫，以及 attention / MLP / LayerNorm / position 分组速度；
- early AUC of \(M_2\) 和 native H2；
- 折叠前/后的精确分支状态分离，以及共享编码器各参数组的核贡献。

不训练 probe 作为主证据：四个确定性前缀不足以构成独立的 probe 训练/测试问题，而且 \(M_2\)、native H2 与分支替换已经直接对应本 anchor 的机制判定。

## 9. 已知好例、坏例与易混淆例

- 已知好例：`direct_only_k2, alpha=1` 应有正 hidden 速度和正共享编码器核信号。
- 已知坏例：`direct_only_k2, alpha=0` 在参考检查点应与其他 \(\alpha\) 前向相同，但参数语义速度为零；训练后轨迹允许不同。
- 易混淆例：`full_k2` 的 direct 为正但 net 可能被共享目标削弱；这属于 H2 结果，不是实现失败。
- 易混淆例：背景项按 \(\alpha\) 缩放、直接项按 \(\alpha^2\) 缩放，因此较小 \(\alpha\) 下背景项的相对占比更大；`full_k2, alpha=0.5` 不保证简单位于 0 与 1 两条曲线之间。
- 易混淆例：native H2 在 200 步未达到高准确率不自动否定一步传递，必须先看 margin 与余项。

## 10. 分阶段自检

| 阶段 | 局部问题 | 通过条件 | 调试产物 |
|---|---|---|---|
| 静态审计 | 投影和损失分解是否正确 | 公式单元测试与形状检查通过 | `static_audit.json` |
| CPU smoke | 七条件是否都可计算 | 所有表非空、无 NaN 主指标 | `smoke_manifest.json` |
| 单 GPU smoke | GPU 自动微分是否一致 | 前向差、核误差通过 | `gpu_smoke.json` |
| 远程四卡 | 35 条训练是否完成 | 四分片完整、5/5 seeds | `run_manifest.json` |
| 聚合审计 | 判定能否复现 | 条件数、种子、检查点齐全 | `coverage_audit.csv` |

## 11. 实现规格

**输入：** 包含所有分支的受控 batch、\(H_0^{raw}\)、共同折叠状态 \(\bar H_0\)、固定 embedding/输出头、语义方向 \(v\)、\(\alpha\)、损失条件。  
**中间量：** \(H_\alpha\)、\(M_2\)、共享编码器 \(\nabla_\theta M_2\)、\(J^\top v\)、\(J^\top c\)、\(\chi_\Theta\)、\(r_\Theta\)、各损失梯度、核信号、一步虚拟更新。  
**输出表：** `kernel_scaling.csv`、`transmission_decomposition.csv`、`parameter_group_transmission.csv`、`finite_step_transmission.csv`、`curve_metrics.csv`、`fold_and_local_guard.csv`。  
**四卡分配：** 按 `(seed, condition)` 稳定哈希分到四个 shard；每个 shard 绑定一张 GPU；全部成功后统一聚合。  
**禁止项：** 不增加 K>2、all-position、AdamW、模型规模、自然语言数据或 MoE 条件。

## 12. 成功、失败与证据不足

**成功：** H1 全部通过，H2 原生共享编码器的直接速度超过数值地板且净速度至少 4/5 为正，H3 一步保真至少 4/5 通过，并且 embedding 零梯度与本地 Y1 守卫通过。  
**部分成功：** H1/H2 通过但 H3 失败，结论限于局部参数传递。  
**机制失败：** H1 有效但原生 \(\kappa_2\) 近零，或背景稳定反转直接项。  
**实现无效：** 前向不一致、核身份误差、头漂移或条件覆盖不完整。

## 13. 不能声称

- MTP 已在自然语言中优于 NTP；
- SGD 结果自动推广到 AdamW；
- decision-only 自动推广到 all-position；
- K=2 结论自动推广到一般 K；
- 参数局部速度已经等于训练 token 样本效率；
- MTP 已改善 MoE 路由或专家效用。
- 参考点恒等式会自动推广到 float32/bfloat16 训练。

## 14. 审核记录

当前为与英文 canonical protocol 对齐的第三版中文执行稿。相对首版已完成四项收紧：每个分支改为一个确定性前缀，消除“均值折叠但样本残差仍在”的定理/实现不一致；补齐固定 H1 头，使背景项明确来自共享编码器雅可比；加入净保留率 \(\rho_{\theta,net}\) 和数值地板，并移除四前缀场景中不可独立验证的 probe 主证据；进一步证明直接项按 \(\alpha^2\)、背景项按 \(\alpha\) 缩放，并用 \(\rho_{\theta,net}=1+\chi_\Theta r_\Theta\) 把背景抵消拆成方向与强度。当前按用户授权进入实现、两轮 smoke 和远程四卡执行。
