# Detailed: A15_08_06_E01 Qwen3-8B CAR / ZX / \(R_U\) 对齐复现

Primary Anchor: [A15_08_06](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_06_qwen8b_geometric_rank_replication_anchor_cn.md)  
Frozen Protocol: [protocol.md](protocol.md), frozen before first8B forward on2026-08-18  
Summary: [summary.md](summary.md)  
Result eligibility: `ELIGIBLE_AI_DRAFT_AWAITING_HUMAN_JUDGMENT`

## 0. Quick Recap

- **Purpose：**只替换模型为 Qwen3-8B，检验0.6B上的 CAR/ZX/\(R_U\)几何秩叙述是否保持。
- **Hypothesis：**三种对象的8B层中位 \(r_{90}/d\) 都与0.6B相差小于0.03。
- **Direct result：**CAR+0.02588，ZX+0.05600，\(R_U\)−0.11096；全部百万-token收敛。
- **Verdict：**`MODEL_SCALE_SHIFT`，由 \(R_U\) 的比例下降触发。
- **Boundary：**CAR/ZX宽谱复现；不能据此推断语义或功能秩。

## 1. Terminology / Definitions

| 术语 | 白话含义 | 计算 | 决策作用 | 不能证明 |
| --- | --- | --- | --- | --- |
| CAR | 相邻完整block之间所有计算运动 | \(H_{l+1}-H_l\) | 看完整层间差谱宽 | 新增语义 |
| ZX | 相邻Attention write在同一500维末层参考空间的差 | \((a_{l+1}-a_l)Q_{500}\) | 对齐会议中的公共参考空间分析 | 参考方向跨层同义 |
| \(R_U\) | 本层归一化更新减去旧状态可仿射线性预测部分 | \(U_l-(X_lB_l+b_l)\) | 看“线性去旧”后的候选剩余 | 非线性新信息 |
| \(r_{90}\) | 解释90%中心化token方差所需最少方向数 | covariance特征值累计到0.9 | 几何谱宽 | 功能必要性 |
| \(r_{90}/d\) | \(r_{90}\)除以对象维数 | 无量纲比例 | 跨4096维和500维比较 | 绝对方向数相同 |

## 2. Anchor Link And Decision Point

A15_08_05 已在 Qwen3-0.6B 对齐模型内证明 CAR/ZX 比 \(R_U\)宽约14--15个百分点。本实验只检验“模型规模是否解释该谱形”这一 rival，不重新定义新增信息。

## 3. Protocol Freeze, Conformance, And Deviations

| 注册项目 | 预期 | 实际 | 状态 | 资格影响 |
| --- | --- | --- | --- | --- |
| 执行范围 |实现、smoke、full、分析|全部完成|PASS|无|
| 模型 |Qwen3-8B，36×4096|一致|PASS|无|
| 分区 |131,072 / 131,072 / 1,048,576|一致且hash互异|PASS|无|
| 对象 |CAR/ZX-500/\(R_U\)|一致|PASS|无|
| 主指标 |层中位 \(r_{90}/d\) 与0.6B差|一致|PASS|无|
| 收敛 |half→full不超过0.02|三者最大0.00903|PASS|无|
| 身份guard |MLP输入误差≤\(10^{-5}\)|0|PASS|无|
| ZX guard |正交/能量误差≤\(5\times10^{-4}\)|\(1.10\times10^{-4}\) / \(1.17\times10^{-4}\)|PASS|无|
| 资源实现 |float32充分统计，可CPU暂存|按层无损暂存|PASS|无|

**Retries：**第一次smoke使用错误Python环境，在模型加载前停止；第二次smoke在写回执时访问已释放的计数对象，保存整数计数后从头重跑。两次均未改变科学配置，完整smoke随后通过。  
**Post-hoc：**CAR边界诊断由注册guard触发，不删除主总体中的token，不改变裁定。  
**Missing：**无主条件或主产物缺失。

## 4. Actual Setup

- 模型：`/data/share/Qwen3-8B`，36层，hidden4096，intermediate12288，bfloat16 forward，SDPA。
- 数据：同 A15_08_05 的 DCLM `uint32` token源；sequence length2048。
- 分区：TRAIN和DEVELOPMENT各64段，EVALUATION 512段；固定连续且不重叠。
- TRAIN：构造末层状态 PCA-500，并拟合36个 \(X\to U\) 仿射岭回归。
- DEVELOPMENT：从 \(10^{-6}\) 到 \(10^{-1}\) 六个无量纲乘子中选择每层MSE最小者。34/36层选择0.1，2/36层选择0.01。
- EVALUATION：仅计算三类中心化 covariance 及六个嵌套token快照。
- 设备：单个40GB H100 MIG，batch1；充分统计float32，阶段间无损移至CPU。
- Seed：8180601。语言模型无训练、无梯度、无checkpoint选择。
- 完整运行耗时约376秒，产生636行谱指标。

## 5. Metrics And Registered Decision Rules

对每个方法，在1,048,576 token时取层中位 \(r_{90}/d\)，减去0.6B冻结参考 CAR0.5625、ZX0.5940、\(R_U\)0.43505859375。

- 全部绝对差<0.03：`MODEL_SCALE_INVARIANT`；
- 任一绝对差≥0.10：`MODEL_SCALE_SHIFT`；
- 其他或不收敛：`MIXED_OR_INSUFFICIENT`。

CAR和ZX中位均≥0.40只给出辅助标签 `BROAD_TRANSITION_REPLICATED`，不能覆盖主裁定。

## 6. Evidence Lineage

| Claim / decision | 注册标准 | 原始证据 | 计算 | 观察值 | 资格 / verdict | 限制 |
| --- | --- | --- | --- | --- | --- | --- |
| 三方法已收敛 |half→full≤0.02|`spectrum_metrics.csv`|每方法跨层中位|0.00903/0.00400/0.00439|ELIGIBLE|不是跨语料重复|
| CAR跨模型近似同量级 |模型差|同上 + 0.6B冻结值|0.58838−0.56250|+0.02588|支持CAR稳定|36层与28层取各自中位|
| ZX在8B略宽 |模型差|同上|0.65000−0.59400|+0.05600|中间区间|固定500维参考空间|
| \(R_U\)发生材料变化 |任一差≥0.10|同上|0.32410−0.43506|−0.11096|`MODEL_SCALE_SHIFT`|残差化选择随模型重估|
| CAR/ZX宽谱复现 |两者≥0.40|`method_summary.csv`|层中位|0.58838 / 0.65000|`BROAD_TRANSITION_REPLICATED`|几何而非功能|
| CAR局部奇异不改变总体 |全/非边界诊断|`car_boundary_spectra.csv`|去除position0重算|中位2410→2410|BOUNDED诊断|不能定位具体机制|

## 7. Main Results

### 7.1 Eligible primary evidence

| 对象 | 维数 | 层数 | 中位 \(r_{90}\) | 范围 | 中位 \(r_{90}/d\) | 中位 effective-rank / d | 中位 top-1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CAR |4096|35|2410|1--2585|0.58838|0.49634|0.02763|
| ZX |500|35|325|243--360|0.65000|0.44075|0.11010|
| \(R_U\) |4096|36|1327.5|609--1576|0.32410|0.32612|0.00956|

CAR/ZX明显高于0.40，层间差高秩在8B上复现。\(R_U\) 相对宽度显著下降，但绝对秩从0.6B的445.5增至1327.5：它是“相对空间占比更小”，而不是“绝对只需少量方向”。

### 7.2 Within-8B object gap

目标blocks2--36中，CAR−\(R_U\)配对中位差+0.25854，31/35层为正；ZX−\(R_U\)为+0.34261，35/35层为正。线性去旧对8B谱的集中作用比0.6B更强。

### 7.3 Bounded anomaly evidence

CAR target block7 top-1占99.54%，block17占99.39%，二者 \(r_{90}=1\)。去掉每段position0后：

- block7：\(r_{90}\) 从1升至867，top-1降至73.79%，说明边界token贡献很大但非全部；
- block17：仍为1，top-1仍为99.39%，说明异常不由position0造成；
- CAR跨层中位：2410保持2410，所以整体高秩不依赖这两个局部异常。

末端blocks35/36的CAR也更集中（1191和327），显示逐层谱不单调。该现象可能来自全局尺度校正、少量大幅同向更新或其他离群结构；当前诊断不能选择其中一个机制。

## 8. Visualization Results

### 8.1 跨模型比较

![跨模型比较](figures/figure4_cross_model_median_r90.png)

- **纵轴：**每个模型内部的层中位 \(r_{90}/d\)。
- **观察：**CAR两模型相近，ZX在8B更宽，\(R_U\)在8B更集中。
- **Take-home：**宽谱复现，但对象特异的模型尺度变化存在。
- **不能证明：**下降由模型表示本身而非残差化拟合造成。

### 8.2 8B逐层结构

![8B逐层结构](figures/figure2_layerwise_r90_full.png)

- **横轴：**层间差写入的目标block；**纵轴：**该对象 \(r_{90}/d\)。
- **观察：**ZX稳定宽；CAR大多数层宽但有blocks7/17和末端跌落；\(R_U\)从浅层约0.15逐步进入约0.3--0.38区间但不严格单调。
- **不能证明：**更深层具有更多新增语义。

### 8.3 token数量收敛

![token收敛](figures/figure1_r90_token_convergence.png)

三条曲线在小样本到百万token过程中都上升，说明2,048 token仍明显低估人口谱宽；最后半百万到百万的变化已满足预注册阈值。

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | 状态 | 排除 | 仍存不确定性 |
| --- | --- | --- | --- | --- |
| Preflight |36×4096模型、唯一split hashes|PASS|错模型/重叠分区|语料外推|
| Unit tests |15项测试|PASS|层数硬编码、offload数值改变|集成环境差异|
| Smoke |212行指标、全部hook|PASS after retry|显存路线、身份错误|科学效应|
| Fit |36层ridge、ZX guard|PASS|漏层、构基泄漏|正则跨模型可比性|
| Evaluation |百万token、636行|PASS|样本秩未收敛|文档相关性|
| Boundary diagnostic |全/非边界/position0|PASS BOUNDED|总体由边界造成|局部异常机制|

没有被证伪的实现或估计器guard。被证伪的是“三种对象均模型尺度不变”。仍存 rival 是 \(R_U\) 的变化来自表示几何还是残差化预测器口径。

## 10. Full Experiment Record

- Raw smoke：`/data/250010109/MoE_Router/experiments/20260818_a15_08_06_e01_qwen8b_car_zx_ru_r90_replication/runs/a15-08-06-e01-20260818-smoke`
- Raw full：`/data/250010109/MoE_Router/experiments/20260818_a15_08_06_e01_qwen8b_car_zx_ru_r90_replication/runs/a15-08-06-e01-20260818-full`
- Full manifest：metric rows636，CAR35层、ZX35层、\(R_U\)36层，全部六个快照完成。
- Failed engineering attempts保留为 `.failed_missing_transformers` 与 `.failed_fit_receipt`，不参与科学结果。

## 11. Interpretation

CAR/ZX的稳定宽谱说明：从完整block运动或固定500维Attention参考空间看，不同token的相邻层变化仍散布在大量方向，0.6B高秩并非单纯小模型产物。

\(R_U\)的下降说明：经过“旧状态可线性预测部分”这一条件化之后，8B剩余更新在总宽度中更集中。但由于绝对 \(r_{90}\) 仍有约1328，而且36层中34层选择了0.1正则，当前不能判断这是8B表示更有结构，还是残差化器在两模型上移除了不同强度/类型的运动。

谱的“奇异”也要分口径：按 \(r_{90}/d\) 的典型集中度是 \(R_U\) 最集中；按典型top-1头部是ZX最重；按单层尖峰是CAR blocks7/17最极端。这三个问题不能用一句“谁最低秩”替代。

## 12. Claim Boundary

**Can claim：**Qwen3-8B复现CAR/ZX宽谱；\(R_U\)的归一化谱相对0.6B显著收窄；对象差异在8B更大。

**Cannot claim：**8B新增语义功能低秩；模型理解或使用所有谱方向；局部CAR秩一是语义方向；谱方向可直接路由；尺度变化由宽度、深度或训练中的哪一个因素单独造成。

## 13. Next Decision

**Decision：**\(R_U\)跨模型下降是否是表示几何变化，还是残差化强度/正则选择造成。  
**Completion criterion：**两模型具有可比的 \(X\to U\)解释率，并完成固定正则下的 \(R_U\)谱敏感性表。  
**Resume action：**审计通过后再决定是否将8B \(R_U\)进入功能秩实验。

## 14. Artifact Manifest

| Artifact | Purpose | Identity | Complete | Claim-eligible |
| --- | --- | --- | --- | --- |
| `protocol.md` |冻结设计|2026-08-18|是|是|
| `evidence/preflight.json` |模型/数据/环境|full run|是|是|
| `evidence/fit_receipt.json` |构基/身份/fit guards|full run|是|是|
| `tables/spectrum_metrics.csv` |全部层/快照指标|636 rows|是|是|
| `tables/cross_model_comparison.csv` |主跨模型表|3 rows|是|是|
| `evidence/verdict.json` |注册裁定|`MODEL_SCALE_SHIFT`|是|是|
| `tables/car_boundary_spectra.csv` |异常定位|105 rows|是|仅诊断|
| `figures/figure4_cross_model_median_r90.png` |主比较图|render receipt|是|是|

## 15. Links

- code workspace: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_06_e01_qwen8b_car_zx_ru_r90_replication`
- runner: `run_alignment.py`
- data: `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_0_of_10_shard_00000000_processed.bin`
- result dir: `/data/250010109/MoE_Router/experiments/20260818_a15_08_06_e01_qwen8b_car_zx_ru_r90_replication/runs/a15-08-06-e01-20260818-full`
- repro command: `/root/anaconda3/envs/spectral-hier/bin/python run_alignment.py --mode full --batch-sequences 1 --output <new-output-dir>`
