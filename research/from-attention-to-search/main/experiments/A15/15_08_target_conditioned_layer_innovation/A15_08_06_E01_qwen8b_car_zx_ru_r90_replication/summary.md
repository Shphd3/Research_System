# Summary: A15_08_06_E01 Qwen3-8B 几何秩复现

Primary Anchor: [A15_08_06](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_06_qwen8b_geometric_rank_replication_anchor_cn.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status: `ELIGIBLE_AI_DRAFT_AWAITING_HUMAN_JUDGMENT`

## Result Snapshot

**Verdict：**`MODEL_SCALE_SHIFT`。

CAR 与 ZX 的层间差在 Qwen3-8B 上仍为宽谱，因而“层间表征差高秩”得到跨模型复现；但 \(R_U\) 的归一化 \(r_{90}\) 从0.4351降至0.3241，下降0.1110，达到注册的模型尺度变化阈值。因此不能说三种对象的谱都与模型规模无关。

## Decision-Bearing Setup

- **唯一改变：**Qwen3-0.6B（28层、1024维）换为 Qwen3-8B（36层、4096维）。
- **保持不变：**同一 DCLM TRAIN/DEVELOPMENT/EVALUATION分区、1,048,576个评价 token、CAR/ZX/\(R_U\)公式、ZX 500维、岭回归选择、中心化 covariance、\(r_{90}/d\)与收敛规则。
- **主指标：**8B各方法层中位 \(r_{90}/d\) 减去冻结的0.6B参考值。
- **限制：**模型宽度、深度、训练结果与残差化预测器共同随模型改变，本实验不能拆分这些内部原因。

## Verdict Basis

| 对象 | 8B中位绝对 \(r_{90}\) | 8B \(r_{90}/d\) | 0.6B \(r_{90}/d\) | 8B−0.6B | 直接判断 |
| --- | ---: | ---: | ---: | ---: | --- |
| CAR完整block相邻差 |2410 / 4096|0.58838|0.56250|+0.02588|宽谱复现，近似同量级|
| ZX公共500维Attention相邻差 |325 / 500|0.65000|0.59400|+0.05600|宽谱复现，8B略宽|
| \(R_U\)线性去旧后更新 |1327.5 / 4096|0.32410|0.43506|−0.11096|达到模型尺度变化阈值|

从524,288到1,048,576 token，CAR、ZX、\(R_U\) 的中位变化分别为0.00903、0.00400、0.00439，均通过0.02收敛门。[来源表](tables/cross_model_comparison.csv)；[注册裁定](evidence/verdict.json)。

8B内部，CAR−\(R_U\) 的配对层中位差为+0.25854，ZX−\(R_U\) 为+0.34261；说明同一模型中“完整层间运动”与“线性去旧剩余”之间的对象差异比0.6B更大。

## 谱的直观解释

“8B的 \(R_U\) 更低秩”只能按比例理解。它仍需约1328个方向解释90%方差，绝对方向数约为0.6B的三倍；只是4096维中占用的比例从43.5%降到32.4%。所以更准确的说法是：

> 8B的线性去旧剩余在更大的表示空间里相对更集中，但并没有压缩成几十维的小空间。

按典型层 \(r_{90}/d\)，\(R_U\) 最集中；按典型层第一方向份额，ZX更头重（中位top-1为11.01%）；按单层最极端异常，CAR blocks 7和17最奇异，均有 \(r_{90}=1\)。去掉每段 position 0 后，block 7恢复到867，但block 17仍为1；CAR总体中位仍为2410。因此边界效应能解释一个异常的部分，却不能解释另一个异常或总体宽谱。[边界摘要](tables/car_boundary_summary.csv)。

## Central Figures

![跨模型层中位秩比较](figures/figure4_cross_model_median_r90.png)

图中纵轴是层中位 \(r_{90}/d\)。CAR基本保持，ZX略升，\(R_U\)比例明显下降。它支持对象特异的模型尺度变化，不能证明功能更低秩。

![Qwen3-8B逐层秩](figures/figure2_layerwise_r90_full.png)

横轴为目标 block，纵轴为该层对象的 \(r_{90}/d\)。大多数 CAR/ZX层为宽谱；CAR的局部跌落是单方向异常。三条曲线都不单调，因此不支持“越深越高秩”。

## Claim Boundary

**可以声称：**在同一百万-token估计器下，Qwen3-8B复现 CAR/ZX高秩；\(R_U\) 相比0.6B在维数比例上更集中，且该变化达到注册阈值。

**不能声称：**8B新增语义功能更低秩；1328个几何方向都必要；CAR异常是语义方向；任何谱可以直接用作 Router。

## Next Decision

**决策：**先判断 \(R_U\) 的跨模型下降是表示几何变化，还是 \(X\to U\) 残差化强度/正则选择造成的口径变化。  
**完成标准：**两模型报告匹配的线性预测解释率，并在固定正则下复算 \(R_U\) 谱敏感性。  
**恢复动作：**只有该审计后，才决定是否把8B的 \(R_U\) 进入功能秩实验。
