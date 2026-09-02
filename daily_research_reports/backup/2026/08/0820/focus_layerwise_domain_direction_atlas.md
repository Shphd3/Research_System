# 不同领域的细类知识在每层的哪种谱、哪些方向和多大子空间中稳定出现？

```text
type: meeting_cycle_core_task
status: RESULTS_READY_AWAITING_HUMAN_ACCOUNT
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
plain_language_design_last_human_confirmation: 2026-08-20
cycle_start: 2026-08-19
target_meeting: 2026-08-21
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/subanchors/15_07_01_layerwise_domain_direction_atlas_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E02_fixed_axis_and_learned_subspace_atlas/protocol.md
source_meeting: daily_research_reports/backup/2026/08/0819/meeting/0819_频谱意义会议原文_清晰转述版.md
core_experiment_count: 1
```

> 研究者已确认本轮直接写 Protocol、实现、冒烟并执行完整实验。上一轮已经打开的
> 确认数据只作为先验证据；本轮最终判断必须使用新密封表达。正式文稿不依赖人物
> 名称，而直接定义分析方法。

## 1. 核心问题

为了以后构造逐层路由，我们现在只回答一个更基础的问题：在第 24、28 层中，
每个领域内部用于区分细类的知识，稳定出现在**哪一种谱坐标、哪些方向和多大
子空间**里；这些方向在不同领域间是复用的，还是只对一个领域有效？

这里比较三把固定“尺子”：本层参数对输入的响应方向、跨层平均得到的公共参数
方向、以及用百万 token 完整表征得到的数据方向。同时保留一种不受固定尺子限制、
直接从分类目标学习低秩空间的方法，判断固定谱轴是否遗漏了可旋转的判别空间。

## 2. 实验目的

在全新表达上为八个领域分别产出一张可核查的方向图谱：固定谱轴方法给出具体
方向及谱段，学习低秩空间的方法给出最少判别维数；两者共同给出每个方向主要拉开
哪些细类、领域间重合多少，以及哪些共享/特有候选仍有留出分类作用。

**完成标准：**第 24、28 层、八个领域、三套固定谱基和一个学习低秩空间都必须
给出新表达上的完整分类曲线、方向位置、领域重合和细类响应；无论结果支持、
基底敏感或失败，都形成明确分类，不用一张正向图替代缺失条件。

## 3. 分析方法

**一句话方法：**在三套冻结谱基上按“细类之间差得大、同类换表达波动小”挑方向，
再与直接学习的低秩分类空间在同一批新表达上比较分类作用、谱段位置和跨领域重合。

1. 只用旧训练/开发表达挑方向、选维数和训练分类头，随后一次性打开新密封表达。
2. 固定谱轴逐个打分并与谱头部、同维随机轴、标签打乱比较；学习低秩空间作为
   可自由旋转的功能上界，二者使用相同旧状态基线和分类增益。
3. 对通过留出功能门的方向画谱段分布、领域重合和细类响应图；未通过的方向不贴
   “共享”或“特有”标签。

## 4. 结论

### 执行前：两种预期结果

- **若支持：**至少一种固定谱基能在多数领域用少量方向保留新表达上的分类增益，
  且与学习低秩空间指向相容；据此更新为“这些层存在可定位、可复现的领域判别
  方向”，并把通过功能门的方向作为后续逐层路由的候选输入，而不是直接宣称路由
  或专家专门化已经有效。
- **若不支持或基底敏感：**若只有自由旋转的低秩空间有效，更新为“低维功能存在，
  但不能固定到当前谱轴”；若两类方法都失败，则更新为“现有方向是表达/噪声依赖”，
  停止据此修改 Router。任何一种结果都必须逐领域说明，而不是只给平均值。

### 执行后：由研究者完成

- **AI 核验的直接结果：**完整更新在 15/16 个“层×领域”通过入口；所有领域的
  自由学习空间都选到完整的 7 个独立类别对比维度；三套固定谱没有任何条件通过
  完整稳健门。七维空间稳定集中于参数响应谱尾段和激活 PCA 前 500 维之外，且
  跨领域几何重合显著高于随机。详见 canonical `summary.md` / `detailed.md`。
- **我的结论：**等待研究者看完三张主图后确认或纠正；AI 不代填研究者判断。
- **仍不能说：**本实验不测试 Router 决策、专家相对效用或专家专门化。
- **唯一下一决策：**研究者确认或纠正“本次只建立谱段认识、尚未找到 Router
  可用的紧凑固定方向，因此暂不修改 Router 代理任务”这一结果边界。

## 路径

- **研究锚点：**[逐层领域方向图谱 Anchor](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/subanchors/15_07_01_layerwise_domain_direction_atlas_anchor_cn.md)
- **实验协议：**[A15_07 E02 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E02_fixed_axis_and_learned_subspace_atlas/protocol.md)
- **结果摘要：**[A15_07 E02 Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E02_fixed_axis_and_learned_subspace_atlas/summary.md)
- **完整证据：**[A15_07 E02 Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E02_fixed_axis_and_learned_subspace_atlas/detailed.md)
- **中文自洽报告：**[实验细节与结论解析](../../Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E02_fixed_axis_and_learned_subspace_atlas/detailed_cn.md)
- **简短组会同步：**[白话同步稿](../../Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E02_fixed_axis_and_learned_subspace_atlas/meeting_sync_cn.md)
- **上一轮证据：**[A15_07 E01 Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E01_stable_domain_discriminant_subspaces/summary.md)
