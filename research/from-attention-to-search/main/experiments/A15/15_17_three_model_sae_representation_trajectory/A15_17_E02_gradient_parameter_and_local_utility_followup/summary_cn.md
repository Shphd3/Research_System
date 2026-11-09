# 总结：A15_17_E02 梯度、参数与局部效用补测

主 Anchor：[A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
冻结 Protocol：[protocol.md](protocol.md)  
完整证据记录：[detailed.md](detailed.md)  
执行凭据：[execution_receipt.md](execution_receipt.md)  
结果状态/资格：Smoke、full、S6 汇总均 `PASS`，证据 `ELIGIBLE`；科学裁决为 `AI_DRAFT_NOT_SUPPORTED_AWAITING_HUMAN_CONFIRMATION`。

> 4×H100 Reserved 作业 `pt-d6swd6xd` 已到达 `SUCCEEDED`。以下数值是合格观察；研究者尚未确认最终科学判断，因此没有把裁决写回 Anchor 或 Focus。

## 1. 目的（Purpose）

检验 M2 的重构梯度在确实到达主干并改变一步更新方向后，是否比同状态、同批次的 LM-only 更新更能改善冻结 P-report 领域读出；同时补齐 15B、Fisher 分子/分母、参数位移、字典方向和冻结 N-report 损失。

## 2. 假设（Hypothesis）

若重构到主干的局部方向有可检测效用，主指标 \(\mathrm{CE}(U0)-\mathrm{CE}(U1)\) 的 95% 配对区间应位于 0 以上。最强竞争解释是：梯度路径真实存在、也改变参数增量，但在当前 2,048 有效词元的一步局部条件下并不改善 held-out 可读性。

## 3. 分析方法（Analysis Method）

- 在 M2 10B 主检验和 15B 独立敏感性上，对四个固定 N-fit 批分别从相同 checkpoint、AdamW、scheduler 和 RNG 状态执行 U0（仅 LM）与 U1（LM + \(\lambda=1\) 重构）各一步；SAE 参数和活动缓冲冻结。
- 用未更新 checkpoint 上 fit/tune 固定的读出器评估 P-report；主指标按四个批方向平均后，对 family/class 做 5,000 次分层配对 bootstrap。正值支持 U1，15B 不能挽救 10B。
- 只读补测 B/W/F、0B→10B/15B 参数与 30,000 个 decoder 列方向，以及 M0/M1/M2 的同一 N-report 冻结 NLL；这些是边界证据，不能替代主指标。

## 4. 结论（Conclusion）

裁决：`AI_DRAFT_NOT_SUPPORTED_AWAITING_HUMAN_CONFIRMATION`。

1. **一步局部试验不支持重构梯度优于 LM-only 更新。**10B 主指标为 `−0.000622 nats`，95% CI `[−0.001691, 0.000400]`，四个批方向中 2 个为正；15B 敏感性为 `−0.000571`，95% CI `[−0.001664, 0.000564]`，1/4 为正。两个区间都跨 0，且点估计略偏向 U0，因此不能宣称 U1 改善；也不能据此宣称 U1 有害或与 U0 等价。[主表](tables/primary_local_utility.csv)

2. **梯度路径和参数作用真实存在，但“存在”没有转化为本次局部效用。**重构梯度在 10B 的 \(h\) 节点范数为 LM 的 `8.27%--10.06%`，15B 为 `3.45%--5.57%`；与 LM 的余弦分别为 `−0.0021--0.0402` 和 `−0.0250--0.1146`。所有 8 个 G0 批在未选位置的最大绝对梯度均精确为 `0`，全部 16 次 G1 更新后 SAE 状态不变。[G0 表](tables/g0_h_gradient.csv)、[G1 表](tables/g1_trial_summary.csv)

3. **原 E01 的 Fisher 上升不能解释为“同类更紧”。**P actual-input 在 10B 的 M1−M0 raw 差为：B `+83.18 [72.78, 98.87]`、W `+120.59 [70.99, 152.69]`、F `+0.2777 [0.1309, 0.3722]`；15B 分别为 B `+138.03 [128.65, 162.75]`、W `+214.18 [150.83, 245.85]`、F `+0.2745 [0.0923, 0.3684]`。即类间和类内能量都增加，只是比例净上升；B3 后结论相同。[分量表](tables/fisher_decomposition_key.csv)、[配对差表](tables/fisher_decomposition_key_differences.csv)

4. **补测描述了历史变化，但没有把它变成单一 loss 的因果证据。**M2−M1 共有主干距离/共同初值范数从 10B 的 `1.4503` 增至 15B 的 `1.6332`；同模型固定-ID decoder 列相对 0B 的中位夹角在 M1/M2 分别由 `84.73°/85.37°` 增至 `86.13°/86.53°`。冻结 N-report 上，10B M2−M1 NLL 为 `−0.00263 [−0.00920, 0.00536]`，15B 为 `+0.00625 [0.000079, 0.01384]` nats/有效词元；后者只说明该开发复制面板上的局部代价，不是一般能力结论。[参数表](tables/parameter_change_summary.csv)、[字典表](tables/dictionary_direction_summary.csv)、[NLL 表](tables/n_report_nll_differences.csv)

| 预注册规则 | 观察值 | 守卫/资格 | 裁决 | 证据来源 |
|---|---|---|---|---|
| 10B 主指标 \(>0\) 且区间不跨 0 | `−0.000622 [−0.001691, 0.000400]` | 4/4 成对批；5,000 draws | `NOT_SUPPORTED` | [primary_local_utility.csv](tables/primary_local_utility.csv) |
| 15B 独立敏感性 | `−0.000571 [−0.001664, 0.000564]` | 不与 10B 合并、不作挽救 | `NOT_SUPPORTED` | [primary_local_utility.csv](tables/primary_local_utility.csv) |
| G0 支持与有限值 | 8/8 批未选位置精确 0；全部有限 | checkpoint dead mask；target/denominator detach | `PASS` | [g0_h_gradient.csv](tables/g0_h_gradient.csv) |
| G1 完整性 | 16/16 隔离更新；SAE 16/16 不变 | 每个 trial 重置 checkpoint/optimizer/scheduler | `PASS` | [g1_trial_summary.csv](tables/g1_trial_summary.csv) |
| 4×H100 Reserved full | `pt-d6swd6xd`，`SUCCEEDED` | 4 卡可见；fresh v2 root | `PASS` | [execution_receipt.md](execution_receipt.md) |

### 重要图

![10B主检验与15B敏感性的局部效用](figures/primary_local_utility.png)

读法：纵轴为 P-report 的 \(\mathrm{CE}(U0)-\mathrm{CE}(U1)\)，高于 0 才偏向带重构梯度的 U1；两个 95% 区间均穿过 0，15B 没有改变 10B 的不支持结论。

### 结论边界

可以说：在两个 checkpoint、四个固定批、一次真实 AdamW 更新的局部条件下，重构梯度到达主干并改变更新，但没有产生可检测的 P-report 读出收益；Fisher 的 M1 增幅同时伴随 B 和 W 增大；15B 参数、字典方向与 NLL 已补齐。

不能说：重构梯度长期无效或有害、U0/U1 等价、历史 M2−M1 差异由重构 loss 单独造成、SAE feature ID 跨期语义稳定、一般语言能力无损，或“从零更容易形成”已经得到验证。

### 下一步分析

**AI 建议的唯一决策：**不要再用历史权重差或单步局部梯度支持“从零更容易形成”；若该机制问题仍是优先级，下一步只考虑一张匹配从零 C/T 训练设计卡，并在提交任何训练前由研究者确认预算、种子、功能主指标和停止规则。

完成标准：研究者确认或修正本次 `NOT_SUPPORTED` 边界，并决定是否值得为匹配从零训练付出成本。停止/转向条件：若不能冻结等 token、数据顺序、全局 batch、优化器、SAE 容量和多种子，或没有 held-out 功能指标，则停止把该因果问题升级为训练实验。
