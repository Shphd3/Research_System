# 粗类判别空间对细类判别空间的复用如何随层深变化？

```text
type: meeting_cycle_core_task
workstream: A15_coarse_fine_direction_alignment
status: EVIDENCE_COMPLETE_AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
synthetic_calibration: COMPLETED_METHOD_GATE_ONLY
real_execution_authorization: COMPLETED
cycle_start: 2026-08-26
target_meeting: Unknown
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_09_layerwise_coarse_fine_reuse_geometry/15_09_layerwise_coarse_fine_reuse_geometry_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_09_layerwise_coarse_fine_reuse_geometry/A15_09_E01_qwen3_30b_cross_depth_coarse_fine_reuse/protocol.md
source_meeting: daily_research_reports/0826/docs/0826会议记录.md
research_reset: 2026-08-27 human-upgraded cross-depth question
core_experiment_count: 1
```

## 1. 核心问题

> 在冻结 Qwen3-30B-A3B 的原生完整 Router/Expert 输入中，mathematics 和
> physics 的父类条件细类 Fisher 判别空间，在每个预选层分别复用了多少八父类
> 共同粗类判别空间；这种粗—细关系如何随网络深度变化？

“复用”只指两个稳定七维判别空间的方向重合，不等于 Router 原生使用、expert
utility 或因果收益。

## 2. 实验目的

在 Block 4/12/20/28/36/44 上，先逐层测量 mathematics、physics 的粗—细重合，
再比较六层原始轨迹、单调趋势和浅/中/深阶段或非单调结构。C4 是主分析面板，C5
用完全相同的方法独立复现。

完成标准：两父类、六层、两面板均原样报告秩门、A/B 复现度、raw/corrected
overlap、标签置换与 Haar 随机基线、复现参照和七个 principal-angle
$\cos^2$；产出三张预注册核心图。无效层保留并标记，不得替换。

**本轮不回答：**Router 训练收益、方向的原生使用、expert utility、跨父类细类
空间共享、PCA 谱位置或任意自然语料上的普遍性。

## 3. 分析方法

1. 冻结 Qwen3-30B-A3B，在 C4/C5 固定文本和固定模板家族 A/B 切分上，一次性
   提取六个预选 Block 真正送入 MoE Gate/Experts 的完整输入；目标父类始终只有
   mathematics 和 physics。
2. 每层完全复用共同 Ledoit–Wolf 正则化 Fisher、七维秩门、A/B 交叉重合、标签
   置换 null、Haar baseline 和经验稳定性校正；任何中间结果都不得改变层、类别、
   阈值、数据或方法。
3. 先报告六层原始轨迹，再把 Spearman 作为单调辅助指标，并按冻结的浅/中/深
   两层均值、阶段排序和中段极值规则检查可复现的阶段性或非单调结构；C4/C5 分开
   分析后才判断复现。0.25/0.75 只作描述区间。

## 4. 结论

### 执行前：两种预期结果

- **若存在可复现的跨层变化：**C4 与 C5 在相同层或阶段呈现一致的粗—细复用
  轨迹，可说明该冻结表征中的判别几何具有层依赖；主角热图进一步区分整体变化
  与少数方向复用，但仍不能推出 Router 架构收益。
- **若不复现或证据不足：**若 C4/C5 轨迹、阶段结构或方向不一致，只能报告逐层
  事实而不能声称稳定的深度规律；若预选层秩不足或不稳定，该层保持原位并标记
  `Insufficient`，不得换层补救。

### 执行后：由研究者完成

以下是 AI 根据冻结证据写出的待确认版本，不替代研究者自己的结果表述：

- **直接结果：**24/24 个注册单元通过秩与 A/B 稳定性门；corrected overlap 为
  0.0596--0.1445。24/24 个 raw overlap 均低于相应标签置换 null 中位数。physics
  在 C4/C5 都呈 shallow > middle > deep；mathematics 的完整阶段排序和单调符号
  不复现；没有可复现的中段极值。
- **AI 待确认结论：**稳定的父类条件细类判别空间主要不沿用共同粗类判别空间；
  fine residual 是当前更符合几何证据的后续假设，但尚未获得因果或功能验证。
- **仍不能说：**不能说 native Router 使用这些空间、粗类补空间对细类功能充分、
  fine-residual Router 会改善 loss，或存在普遍单调的深度规律。
- **唯一下一决策：**固定父类后，细类功能是否保留在粗类空间的补空间中，并且
  是否会在删除 fine-specific residual directions 后特异性下降？下一步仍先做冻结
  表征干预，不启动 Router 训练。

## 路径

- **组会记录：**[0826会议记录](docs/0826会议记录.md)
- **Anchor：**[15_09 Anchor](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_09_layerwise_coarse_fine_reuse_geometry/15_09_layerwise_coarse_fine_reuse_geometry_anchor.md)
- **Protocol：**[A15_09_E01 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_09_layerwise_coarse_fine_reuse_geometry/A15_09_E01_qwen3_30b_cross_depth_coarse_fine_reuse/protocol.md)
- **Summary：**[A15_09_E01 Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_09_layerwise_coarse_fine_reuse_geometry/A15_09_E01_qwen3_30b_cross_depth_coarse_fine_reuse/summary.md)
- **Detailed：**[A15_09_E01 Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_09_layerwise_coarse_fine_reuse_geometry/A15_09_E01_qwen3_30b_cross_depth_coarse_fine_reuse/detailed.md)
- **Parking Lot：**[README.md](../../Projects/from-attention-to-search/main/parking_lot/README.md)
