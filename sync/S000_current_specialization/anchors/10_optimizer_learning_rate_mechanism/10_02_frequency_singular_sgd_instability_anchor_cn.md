# 10_02 频率驱动的奇异值放大与 SGD 不稳定 Anchor

Thinking Card source: [10_02_frequency_singular_sgd_instability_thinking_card_cn.md](10_02_frequency_singular_sgd_instability_thinking_card_cn.md)

## 1. 问题定义

**父问题：** A10 研究 Adam-like 方法为什么能承受比 SGD 更大的有效学习率。

**更窄子问题：** 先在 controlled nested-prefix next-token 任务上测试 0701 design 的第一条因果链。

**决策问题：** 在一个小型 nested-prefix causal model 中，Zipfian frequency 是否产生输出头 singular concentration，并预测高 LR SGD 不稳定？

**不在范围内：** 不解释 Adam 全部优势；不证明 SGD-LL/SCALE；不证明真实文本迁移；不提出最终 optimizer；不更新 MoE routing preservation claim。

**术语解释：**

| 术语 | 具体含义 | 计算对象 | 公式/单位 | 为什么重要 | 不能证明 |
| --- | --- | --- | --- | --- | --- |
| Zipfian nested-prefix data | 短 prefix 出现远多于长 extension | 从 $A, AB,\ldots, ABCDEFG$ 的递减分布采样最大 prefix depth | target token frequency | 生成 common/rare 频率差 | 不是真实自然语言 |
| 奇异谱集中 (singular concentration) | 输出头能量集中到少数奇异方向 | 对 $W_{\mathrm{out}}$ 做 SVD | $\sum_{i\le k}\sigma_i^2/\sum_i\sigma_i^2$ | 检查 common learning 是否形成高增益方向 | 不是 Hessian 分析 |
| top 谱带梯度质量 (top spectral-band gradient mass) | 梯度能量落在当前 top right-singular subspace 的比例 | 将输出头梯度投影到 $V_{\mathrm{top}}$ | $B_{\mathrm{top}}(G)=\|G V_{\mathrm{top}}\|_F^2/(\|G\|_F^2+\epsilon)$ | 检查更新是否使用放大方向 | 单独不能证明因果 |
| extra-feature effective rank | prefix extension 使用多少独立方向 | 相邻 prefix hidden 差分矩阵的 SVD | $\operatorname{erank}(E)$ | 区分独立 extension 与塌缩复用 | 不证明语义特征 |
| 不稳定事件 (instability event) | 高 LR 下首次 loss/logit/spectrum spike | 非有限 loss 或大幅 loss/spectrum jump 的 first step | step index | 定位失败机制 | 不是最大学习率定理 |

## 2. 物理先验

**P1：频率会产生一致的 common gradient。**  
含义：$A$、$B$ 这类频繁目标在许多样本中反复出现，因此输出头梯度可能沿这些 token/feature 对齐。  
可能错在：token frequency 与 gradient row norm 没有正相关。

**P2：common gradient 会长出高增益奇异方向。**  
含义：反复一致的更新会让输出头少数 singular values 变大。  
可能错在：谱始终平坦，或 rare target 学会之后才出现谱集中。

**P3：高 LR SGD 失败可能是局部化的，而不是各方向同时失败。**  
含义：不稳定应该集中在 token columns 或 top spectral bands。  
可能错在：不稳定均匀分布，或在 top modes 形成前就出现。

## 3. 可证伪假设

**H1：frequency-gradient link。**  
如果 early training 中 output-head gradient row norm 与 target-token frequency 正相关，则支持；若接近 0 或负相关，则削弱。

**H2：common-to-spectrum temporal order。**  
如果 common-prefix accuracy 先提升，之后 top singular value / top energy 增长，则支持；若没有 common learning 或没有谱集中，则削弱。

**H3：instability localization。**  
如果高 LR SGD 的不稳定发生在谱集中之后，且 $B_{\mathrm{top}}(G)$ 或 token-gradient concentration 高于稳定基线，则支持；若不稳定发生在谱集中前或没有谱/token 局部化，则削弱。

## 4. 数学模型

输出头矩阵 $W_{\mathrm{out}}\in\mathbb{R}^{V\times d}$，输出头梯度 $G\in\mathbb{R}^{V\times d}$，奇异值分解为：

$$
W_{\mathrm{out}}=U\Sigma V^\top.
$$

读出放大关系：

$$
W_{\mathrm{out}}h=\sum_i \sigma_i \langle h,v_i\rangle u_i.
$$

top 谱带梯度质量：

$$
B_{\mathrm{top}}(G)=\frac{\|G V_{\mathrm{top}}\|_F^2}{\|G\|_F^2+\epsilon}.
$$

extra-feature effective rank：

$$
\operatorname{erank}(E)=\exp\left(-\sum_i p_i\log p_i\right),\quad
p_i=\frac{s_i^2}{\sum_j s_j^2}.
$$

**机制关系：** 如果 Zipfian common gradients 创造高增益子空间，则 common accuracy 应先上升，top singular energy 随后增长，rare extension directions 应有明显 top-subspace mass，高 LR SGD 的失败也应局部化在同一 top band。

## 5. 计算实现

**输入对象：** 合成 Zipfian nested-prefix next-token 数据；一层单头 causal model；AdamW、safe SGD、high-LR SGD、output-row clipping、output-row normalization、label smoothing、spectral clipping。

**计算变量：** common/rare accuracy、common/rare loss、输出头奇异值、top energy、$B_{\mathrm{top}}(G)$、token-gradient imbalance、frequency-gradient correlation、extra-feature effective rank、extra-feature top-$k$ mass、instability step。

**算法阶段：** 生成 nested-prefix batch；用相同 seeds 跑 optimizer probes；逐步记录机制画像；聚合稳定性和谱诊断；写 summary/detailed。

## 6. 最小证伪实验

**实验：** A10_02 controlled nested-prefix frequency-singular instability diagnostic。

**问题：** 频率塑造的 singular concentration 是否能预测 controlled setup 中的高 LR SGD 不稳定？

**比较：** AdamW、safe SGD、high-LR SGD、output-row clipping、output-row normalization、label smoothing、spectral clipping。

**主指标：** instability-localization profile：不稳定条件必须在 common accuracy 和 top singular energy 已增加之后，表现出高 $B_{\mathrm{top}}(G)$ 与高 token-gradient concentration。

**通过/失败/证据不足：** H1-H3 全成立则通过；若不稳定非局部化或发生在谱形成前则失败；若没有任何 high-LR 条件不稳定，或所有条件在 common 学会前失败，则证据不足。

## 7. 当前证据

**观察：** 0701 design 提出了 Zipfian frequency -> common-feature gradient coherence -> singular-value growth -> gradient amplification -> high-learning-rate SGD instability 的因果链。

**解释：** 这是清晰的问题理解 anchor，但还不是该因果链成立的证据。

**边界：** 当前是 optimizer line diagnostic，不更新 nested learning / MoE gating preservation claim。

**观察：** A10_02 主本地边界 run (`high_lr=0.9`, seeds `0,1,2`) 没有出现合格的 late instability event，但 `sgd_high_ce` 出现 rare-prefix suppression：rare accuracy `0.4335`，common accuracy `0.8949`，top-SV growth `3.6756`，top-2 energy `0.6622`，top-band gradient mass `0.5564`，extra-feature effective rank `2.4621`，extra top-2 mass `0.4721`。

**解释：** 支持更窄机制：高 SGD 学习率会在 clean divergence 之前，把 rare prefix extensions 推入更低秩、更依赖 top subspace 的状态。

**边界：** 这是 controlled synthetic rare suppression 证据，不是 real-LM divergence 证明。

**证据链接：** `../../experiments/A10/A10_02_frequency_singular_sgd_instability/summary.md`; `../../experiments/A10/A10_02_frequency_singular_sgd_instability/detailed.md`。

**观察：** row clipping 与 row normalization 修复了主边界 run：rare accuracy 都达到 `1.0000`；row clipping 将 top-band gradient mass 降到 `0.2130`，extra top-2 mass 降到 `0.2584`；row normalization 将 extra top-2 mass 降到 `0.2436`。

**解释：** output-row scale control 是 rare-suppression regime 的有效因果 probe。

**边界：** 这不是最终 optimizer 结论。

**观察：** 远程 SCO stress run (`pt-c6a1nhsr`, `high_lr=2.0`) 成功完成，并产生早期谱爆炸：`sgd_high_ce` stable rate `0.0000`，mean instability step `12.33`，top-SV growth `3248.10`，top-2 energy `0.9955`，top-band gradient mass `0.9450`，rare accuracy `0.0000`。

**解释：** 很大的 SGD LR 可以造成 early spectral divergence，但它太激进，不能证明 common learning -> late instability 的完整时间链。

**边界：** stress-run evidence 只能作为辅助，不应替代 calibrated boundary result。

## 8. Claim Boundary And Next Decision

**现在可 claim：** 在 controlled nested-prefix task 中，高 LR SGD 会进入 rare-suppression regime，并伴随更强 output-head spectral concentration、更高 top-band gradient mass、更低 extra-feature effective rank 和更高 extra top-2 mass；row clipping、row normalization、label smoothing 能在边界 run 中修复 rare learning。

**现在不可 claim：** 不能证明 real LM 高 LR SGD divergence 的根因就是 frequency-driven singular amplification；不能解释 Adam 全部优势；不能提出最终 optimizer；不能更新 MoE routing preservation。

**下一步：** 做 LR/noise boundary map：noiseless full-batch、noisy full-batch、noisy mini-batch。目标是定位 stable learning -> rare suppression -> spectral divergence 的转变边界。
