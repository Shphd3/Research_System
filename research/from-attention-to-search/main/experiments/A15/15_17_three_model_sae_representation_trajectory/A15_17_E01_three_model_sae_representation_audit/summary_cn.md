# 总结：A15_17_E01 三模型 SAE 表征审计

主 Anchor：[A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
冻结 Protocol：[protocol.md](protocol.md)  
完整证据记录：[detailed.md](detailed.md)  
结果状态/资格：S2--S6 `PASS`，证据 `ELIGIBLE`；科学裁决为 `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`。

> 作业 `pt-we1cni15` 已完成全量矩阵和产物审计。下面的数值是合格观察；“有界支持”的研究判断仍需研究者确认，尚未写回 Anchor 或作为 Focus 的人类结论。

## 1. 目的（Purpose）

判断 Dense 模型 M0、重建输入对主干断梯度的 SAE 模型 M1、以及重建输入对主干保持梯度并带 SAE-only AuxK 的 M2，在相同 0--10B checkpoint 上是否形成不同的领域可读性与粗细层级表征轨迹，以及这些差异在用 fit 数据去除第一共同方向后是否仍然存在。

## 2. 假设（Hypothesis）

若 SAE 介入确实改变了剩余可访问结构，至少一组预注册配对差 M1−M0、M2−M1 或 M2−M0 会在 raw \(h\) 或实际末层 MLP 输入中形成连贯轨迹，并在 B2 或 B3 去除第一奇异方向后保留差异。

最强竞争解释是：raw 差异来自词面组成、重建误差、probe 波动、全局均值或单一主导共同方向；另一竞争解释是局部梯度不同，但 held-out 表征没有对应变化。

## 3. 分析方法（Analysis Method）

- 在相同 P/N report 样本上，跨 0、0.5、1、3、5、10B 比较 M1−M0、M2−M1、M2−M0；主读数是实际 MLP 输入和 raw \(h\) 的全局细类 balanced accuracy、父类条件细类 Fisher trace 与余弦关系间隔，区间来自 5,000 次分层配对 bootstrap。
- 独立执行 fit-only B1 中心化、B2 从未中心化 fit 矩阵移除第一右奇异方向、B3 先中心化再移除第一方向；投影后沿用 raw 选出的 \(C\) 并重新拟合 probe，以判断轨迹是否只依赖均值或共同主轴。
- 审计 M1/M2 稀疏贡献重合、FVU/effective-L0/覆盖率、每 checkpoint 四个固定局部梯度批，以及包含 0B 的原子激活和 PCA/UMAP/t-SNE 演化图；这些只诊断 SAE 健康与局部目标作用。

## 4. 结论（Conclusion）

裁决：`AI_DRAFT_SUPPORTING_BOUNDED_AWAITING_HUMAN_CONFIRMATION`。

1. **存在一条合格、跨 checkpoint 且去共同方向后保留的 M1 几何差异。**在 P 的实际 MLP 输入上，M1−M0 的父类条件细类 Fisher 差从 1B 到 10B 连续为正：raw 为 `+0.0709 / +0.1045 / +0.0995 / +0.2777`，对应四个 95% 点区间都不跨 0；B3 后为 `+0.0757 / +0.1098 / +0.1141 / +0.2661`，区间也都不跨 0。N 的 B3 实际输入上，M1−M0 从 0.5B 到 10B 同样连续为正。这满足“同一对象和指标形成有界轨迹并通过 B2/B3”的预注册支持分支，但只支持剩余几何不同。

2. **线性可读性没有形成“三模型统一排序”。**P 的实际输入在 3B 出现 M1−M0 `+0.0778 [0.0333, 0.1222]`，同时 M2−M1 为 `−0.0667 [−0.1111, −0.0222]`；B3 后仍分别为 `+0.0611 [0.0167, 0.1111]` 与 `−0.0611 [−0.1056, −0.0167]`。但其他 checkpoint 多数区间未分离，N 的 raw-\(h\) 全局细类 probe 在全部 checkpoint/比较上都未分离。因此可把 **M1 3B** 视作最小候选点，不能说 M1/M2 普遍优于 M0，更不能说 live-gradient 的 M2 优于 detached 的 M1。

3. **第一共同方向不是上述 M1 Fisher 轨迹的充分解释。**P 实际输入的 B2 在 3B 移除了各模型 `73.0%--94.5%` 的 fit 能量、在 10B 移除了 `75.4%--99.4%`；B3 相应移除 `21.2%--24.9%` 与 `23.3%--82.9%`。尽管投影很强，M1−M0 的 Fisher 差与 raw 接近且保持同号。它排除了“只靠第一方向”的简单竞争解释，但没有证明被模型因果使用。

4. **稀疏与梯度诊断符合实现拓扑，却不能解释成机制因果。**M1 的重建损失对主干组梯度为 0；M2 的重建损失在 10B 对主干组有非零局部梯度，全部记录的 reconstruction/LM 加权范数比中位数为 `0.0406`。M2 的 AuxK 只作用于 SAE，10B 最大加权比为 `0.0005707`；0B 的四个批次均为 0 个 AuxK 有效样本和精确零梯度。该诊断证明收集到的局部目标路径与设计一致，不证明这些梯度造成了观察到的 Fisher 差异。

所有区间都是预注册的逐点描述性区间，没有 family-wise 多重比较校正；checkpoint 不是独立重复实验。

| 预注册规则 | 观察值 | 守卫/资格 | 裁决 | 证据来源 |
|---|---|---|---|---|
| S2 runtime、hook、有限值、state 不变 | 6/6 资格任务通过；17 个远程测试通过；optimizer/buffer 更新均为 0 | 四张 H100 可见；前后 state hash 一致 | `PASS` | [execution_receipt.md](execution_receipt.md) |
| 18 个 checkpoint 全覆盖 | 18 cache、18 gradient、18 completion；每项内容哈希吻合 | 每个梯度文件 4 个固定批次 | `PASS` | [detailed.md](detailed.md#3-protocol-freeze-conformance-and-deviations) |
| raw 配对轨迹连贯 | P actual Fisher 的 M1−M0 在 1/3/5/10B 连续为正 | 相同 report 单元；5,000 配对 draws | `SUPPORTING_BOUNDED` | [paired_fisher_differences.csv](tables/paired_fisher_differences.csv) |
| B2 或 B3 后仍有剩余差异 | 同一 P actual Fisher 轨迹在 B2/B3 后保留；N B3 也形成 M1−M0 正轨迹 | 216 个 fit-only transforms 完整 | `SUPPORTING_BOUNDED` | [paired_fisher_differences_B.csv](tables/paired_fisher_differences_B.csv) |
| probe 给出一致模型排序 | 只有 checkpoint/面板特定分离；N raw-\(h\) 全部未分离 | 2,100 个 probe metric 单元全部 eligible | `NOT_SUPPORTED_AS_GLOBAL_RANKING` | [paired_probe_differences.csv](tables/paired_probe_differences.csv)、[paired_probe_differences_B.csv](tables/paired_probe_differences_B.csv) |
| 必需可视证据 | 16/16 图齐全可解码；A06 与三张 A09 均含 0B | UMAP 谱初始化回退到固定种子随机初始化，仅描述使用 | `PASS_WITH_DESCRIPTIVE_LIMIT` | [detailed.md](detailed.md#8-visualization-results) |

### 重要图

![实际 MLP 输入的全局细类可读性](figures/A03_actual_input_readability.png)

读法：横轴是训练 token，纵轴是 report balanced accuracy；P 的 3B 蓝线（M1）高于红线（M0）和绿线（M2），但其余点没有形成统一排序，精确配对区间见源表。

![去除第一共同方向后的 raw-h 可读性](figures/B02_probe_after_direction_removal.png)

读法：同色不同线型是 B1/B2/B3；去掉第一方向后，P 的若干差异仍存在，而 N 曲线仍高度接近。该图展示敏感性，裁决依据是配对源表而不是线条外观。

用户要求的描述图均已补齐并含 0B：[原子激活演化 A06](figures/A06_sae_health_and_features.png)、[PCA A09](figures/A09_representation_evolution_pca.png)、[UMAP A09](figures/A09_representation_evolution_umap.png)、[t-SNE A09](figures/A09_representation_evolution_tsne.png)。它们不用于挑选模型或 checkpoint。

### 结论边界

可以说：合格证据支持 M1 在冻结 checkpoint 的实际 MLP 输入上具有不同于 M0 的父类条件细类剩余几何；该差异跨多个 checkpoint，并在 fit-only B2/B3 后保留。可以报告 checkpoint 特定的 probe 差异、SAE 使用和局部梯度。

不能说：原生 Gate 或 MLP 因果使用该几何、M1/M2 具有专家专门化、下游语言模型性能更好、M2 普遍优于 M1，或不同模型/不同 checkpoint 的 SAE atom ID 对应同一语义。

### 下一步分析

**AI 建议的唯一决策：**研究者确认上述有界裁决后，决定是否把 M1 3B 作为一个独立因果功能干预的候选点；本轮没有授权该后继实验。

为什么：M1 3B 同时具有 actual-input probe 差 `+0.0778` 和 Fisher 差 `+0.1045`，两者在 B2/B3 后都保留，是最小且不依赖单一指标的候选。

仍未解决：标准模型计算是否真正使用这一可读几何，以及干预后是否改变 held-out 功能。

完成标准：研究者确认或修正直接结果、结论边界，以及是否进入这个唯一后继决策。

停止/转向条件：若研究者不接受“点区间 + 开发复制”作为足够提名证据，或后续匹配成本的因果干预没有稳定功能效应，则停止把当前 SAE 配置当作已建立的机制证据。

续接动作：先读 [detailed.md](detailed.md) 的证据链和失败/资格记录，再由研究者确认裁决；在此之前不更新 Anchor 的科学结论。
