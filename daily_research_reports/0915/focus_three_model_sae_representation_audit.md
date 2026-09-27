# SAE 的新增重构梯度，是否让预训练中的领域结构更容易形成？

```text
type: meeting_cycle_core_task
task_state: CLOSED
problem_key: three_model_sae_representation_audit
focus_role: SECONDARY
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: ELIGIBLE_RESULT_AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
cycle_start: 2026-09-15
target_meeting: 2026-09-18
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E05_multimodel_fisher_gradient_coefficient_audit/protocol.md
core_experiment_count: 1
```

2026-09-16 按研究者要求重写。已有审计完成；知识解释与后继建议仍由研究者裁定。本次不改变 problem_key、项目归属、已执行协议或科学状态。

阅读入口：[组会四段式报告](../0916/focus_meeting_sae_representation_update_cn.md)；[数据、方法、公平性及后继方案](../0916/sae_representation_followup/01_result_explanation_and_next_plan_cn.md)。正式结果仍由 [Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E01_three_model_sae_representation_audit/summary_cn.md) 和 [Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E01_three_model_sae_representation_audit/detailed.md) 所有。

## 核心问题与当前认识

语言模型从随机初始化预训练时，领域相关的信息能否逐渐被读出；加入 SAE 后，尤其让额外重构损失更新上游主干后，这个过程是否改变？**本轮已执行的可检验部分是三个既有模型在共同训练进度上的表征差异，不是从零配对训练的单变量因果检验。**

旧版 M1 和新版 M2 都在最后一层 MLP 前串联一个连续训练的 SAE，语言损失一直经过 SAE 反传。M1 只在额外的抽样重构分支上切断输入梯度；M2 打开这条输入梯度，并另外加入只直接训练 SAE 的防死特征损失 AuxK。不能把 M1 写成“语言梯度也断开”，不能把 M2−M1 写成纯粹的一个开关差异。

**AI 知识更新：**领域读出与稀疏使用确实随训练改变；旧版的一部分细领域几何差异在去第一方向后保留。但新版没有获得跨位置、跨面板的一致读出优势，重构更好也没有自动变成领域可读性更好。因此，“梯度接通”已核实，“促进语义形成”仍未知。命题等价不是本轮主结论，不能由领域激活图代替证明。

## 本轮唯一实验：既有三模型 0–10B 表征审计

**目的。** 分清上游原始表征、实际送入 MLP 的重构、SAE 激活和局部梯度各自改变了什么，排除仅由首个主导方向造成差异的解释。

**假设。** 如果训练配置改变了领域组织，固定文本上的配对差异应在同一表征与指标中沿训练进度持续出现，并在去第一方向后至少部分保留。最强竞争解释是词面规律、重构造成的几何重排、单一共同方向以及局部统计波动。

**分析方法。** 三模型共同快照使用同一短句面板和自然学术文本面板，分别读取 SAE 前原始状态与实际 MLP 输入；比较线性读出、父领域内部的细领域分离、稀疏贡献和损失梯度。原始分析与仅用拟合数据确定的中心化／去第一方向分析分开，模型差值共享重采样单元。具体数值与实现以既有 Protocol 为准。

**预注册结果分支。** 同一测量对象上的连续差异通过去方向检查，支持有边界的可访问结构差异；差异不分离或去方向后消失，则不支持该优势；身份、样本、抽取位置或统计资格失败则证据不足。任何分支均不自动证明语言模型使用该结构或辅助梯度带来因果收益。

## 滚动轮次摘要

| 轮次 | 证据与认识更新 | 边界与下一决策 |
|---|---|---|
| A15_17_E01，2026-09-16 | 全矩阵及不可变性审计通过。M1 实际输入的细领域 Fisher 轨迹在去方向后保留；读出优势取决于训练点和测量对象。完整数值、工程重试与资格仅见 Detailed。 | 新版梯度有非零上游作用，但没有一致领域优势；M2 同时改变 AuxK，因果归属未知。待研究者决定是否进入下述同状态最小验证。 |
| A15_17_E03 及事后可信度审计，2026-09-17 | S7/S37/SALL 在 0/0.5/1/3B、P/N 上的表征和局部梯度测量合格。Fisher 的真实标签几何明显超过置换零假设，但重构后 Fisher 有升有降，且 44 个独立探针对比中 42 个重构读出更低。原先约 90° 的角度经 262,144 维随机方向校准后，43/44 组与随机相容，未发现“比随机更正交”的组。 | 近 90° 不能再作为特殊正交机制；Fisher 只保留为有可信度守卫的几何量。下一决策改为确认 E05 的更多 checkpoint、参数梯度与系数干预设计。 |
| A15_17_E05，2026-09-18 | 五模型精确 0/0.5/1/3/5/10B 的 30/30 采集与 672/672 probe 单元合格。10B 的 S37/SALL 在部分 Fisher 与 probe 上为正，但 P 大差值受 M0 终点下落影响；三个旁支的冻结 M2D2 NLL 均差于 M0。共享参数梯度接近 90° 但明显不符合随机正交，且总梯度比 S7/S37/SALL 为 3.54%/3.06%/1.24%。 | 当前只支持 checkpoint/数据集相关的几何重排，不支持稳定训练收益或因果机制。AI 建议下一步只做 S7/SALL 的 `lambda=1` 与 `target-rho=0.02` 匹配干预；是否采纳由研究者确认。 |

## 0918 0--10B 测量设计（研究者已确认并授权执行）

**目的。** 判断把 Attention 输出 SAE 旁支作为训练正则，是否让语言模型自身的表征更可分，并在相同训练词元下取得更低或至少不更差的语言模型损失。“增加参数 capacity”保留为动机；本轮指标不能直接证明容量上限提高。

**假设。** 如果旁支正则有益地重组主干，Fisher 几何与留出 probe 应共同改善，直接去掉未中心化表征的第一大奇异方向后仍保留，并且不伴随更差的 token 对齐语言损失。最强竞争解释是 Fisher 仅由类内压缩抬高、单一主导方向造成视觉差异、或近 90° 梯度只是高维随机现象。

**分析方法。** 第一，在 P 与 M2D2 上比较 M0、M2、S7、S37、SALL 的精确 0/0.5/1/3/5/10B，联合报告原始与直接去第一奇异方向后的 B/W/F、线性 probe 和固定两层神经网络 probe；M1 排除。五模型共同端点为精确 10B。第二，分别报告训练日志中的 token 对齐语言损失和冻结 M2D2 报告集上的语言损失，并报告仅重建 loss、loss 比例、共享主干参数上的 \(\rho=\lVert g_A\rVert/\lVert g_C\rVert\)、有可靠性保护的余弦 \(c\) 及同维随机参照；所有图以累计有效预测词元为横轴。第三，在同一模型和层内报告活跃、持续、新出现和消失 feature 的比例，不跨模型解释 feature ID。

**预注册结论分支。** Fisher 与 probe 一起改善且跨 P/N、去方向后保留，才支持有边界的表征改善；只有 Fisher 改变时只报告几何变化；只有语言损失改善时只报告训练曲线观察；均不出现则不支持；精确 checkpoint、模型身份、拟合边界或源数据缺失则证据不足。

完整结果见 [E05 中文 Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E05_multimodel_fisher_gradient_coefficient_audit/summary_cn.md)，组会读法见 [0918 汇报稿](../0918/focus_meeting_sae_sidecar_regularization_0_10b_cn.md)，精确测量合同见 [E05 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E05_multimodel_fisher_gradient_coefficient_audit/protocol.md)。最终执行使用单节点四卡 RTX 5090 Spot；H100 中断轮次与早期无效 Smoke 均不形成科学结果。

## 当前唯一下一决策

**结果状态：**E05 已完成，30/30 个注册只读单元与真实训练系数通过核验，四卡 RTX 5090 Spot Smoke 和 full 均满足无参数突变、零 optimizer update、精确 checkpoint 与完整结果要求。结果解释仍为 AI 草稿，等待研究者确认；不自动更新 Anchor 的科学判断。

**AI 建议：**不再用 `0.1/0.2/0.8` 的单旁支等权方案作为公平标准，而以共享主干总梯度比 \(\rho\) 为控制量。唯一下一实验是同初始化、同 token 顺序的 S7/SALL `lambda=1` 与 `target-rho=0.02` 对照，先测 `0/0.1/0.25/0.5/1B`，留出 NLL 不恶化且梯度配平后才继续 `3/5/10B`。若配平后差异仍在，就停止把层数差异归因于梯度范数不平衡。
