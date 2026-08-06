# 05-06-07 Research Chain: From Initialization Collapse To Interference Value

## 0. 一句话结论

当前 05-06-07 的完整研究问题不是单纯“让负载均匀”，而是：

如何避免普通 top-1 MoE 在初始化和早期训练中被共同成分锁进路由塌缩，使均匀分布的 features 能进入非塌缩、可解释、可保持的 expert partition；并进一步验证这个 partition 是否真的降低 feature interference、产生 expert utility。

这里的几个词需要先固定：

- 路由塌缩：大部分 token 或 feature 被分到少数 expert，导致“均匀 feature 分布”没有变成“均匀 expert 使用”。
- feature-level expert specialization：专家分工不仅负载均匀，还要和可操作 feature 对齐，训练后保持，并最终证明被选 expert 对该 feature 有因果价值。
- 共同成分 common component：不同 feature 共享的 hidden direction，例如 $c$；它会通过 $w_e^T c$ 给某些 expert 形成有效偏置。
- proxy：真实数据没有人工 feature label 时，用稳定 hidden-state cluster 作为可评估的替代 feature。
- utility binding：路由到某个 expert 不只是标签上对齐，而是该 expert 对对应 group 的 loss 或 ablation 有因果贡献。

## 1. 父问题与边界

父问题：
如何让 MoE gating 形成稳定、可解释、可复用的 feature-level expert specialization？

当前收束后的子问题：
在进入 utility binding 之前，先解决入口条件：普通 top-1 router 为什么即使 feature 均匀也会初始化或早期训练塌缩？怎样构造或发现一个非塌缩、feature-aligned 的初始分区，并判断它能否被训练保持？

你的表述“如何避免初始化 collapse，将均匀分布的 features 均匀分到专家上去”是正确的，但它是必要条件，不是最终 claim。原因是：

- 均匀分到专家可以排除单 expert collapse；
- 但均匀负载不等于 feature 对齐；
- feature 对齐也不等于 expert function 有用；
- 所以 07 必须进入故事线，回答“这个分区是否降低干扰、有功能价值”。

总 claim boundary：
05-06 目前能支持“collapse 机制和可达/可保持边界”的故事，不能直接支持“真实语言模型已有语义专家”或“方法已经解决 MoE specialization”。07 已经在 controlled synthetic D07 上支持“metric surface 合法 -> common-control 减少 rare interference -> route-function binding 存在”这条链，但还不能外推到真实语料、真实 checkpoint 或可部署 MoE。

## 2. 链条总览

1. 05 failure mechanism：解释为什么普通 top-1 会失败。核心更新是 common-offset / common-logit 和 early lock-in。
2. 06 geometry proxy preservation：把机制变成阶段合同：feature/proxy 是否存在、能否转成 router init、训练是否保持。
3. 07 features overlap：在“不塌缩并能形成分区”之后，检查这个分区是否真的减少 common/rare feature interference，并最终检查 expert utility。

主链条：

`05_03 common offset`
-> `05_04_02 common-logit causality`
-> `05_04_03 real-text early-training amplification`
-> `06_10 real proxy`
-> `06_11 proxy-center router init`
-> `06_12 preservation failure`
-> `06_13 failure localization`
-> `06_16 controlled bridge boundary`
-> `06_17 route-relevant state selector boundary`
-> `07_01 metric/data audit`
-> `07_02 method effect`
-> `07_03 route-function binding`

## 3. Anchor Chain

### Anchor: 05_01 Inhibition And Early Lock-In

解决了什么问题：
先排除一个诱人的错误路径：仅用 center separation 或 token-conditioned inhibition 是否能直接解决 routing collapse。

和父问题的关系：
它说明“让同 feature 稳定走同一路由”不足以证明 specialization，因为 inhibition 可能让早期 top-1 选择更硬，反而放大 collapse。

conclusion：
center separation 不稳定；当前 token-conditioned inhibition 可能提高一致性，但容易硬化 early lock-in。它不是当前主解决方案。

boundary：
不能 claim inhibition 永远无效，也不能 claim expert utility 错误；这里只说明当前 inhibition formulation 不是可靠 anti-collapse path。

链接下去：
[05_03 common-offset anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_03_uniform_collapse_common_offset_anchor.md)

### Anchor: 05_02 Feature Assumption Relaxation

解决了什么问题：
检查 ordinary top-1 在更复杂 feature 假设下是否仍能产生可解释路由，而不是只在弱 toy 上看起来一致。

和父问题的关系：
它把“target 学会了”和“router 形成专家分工”拆开。target accuracy 高但 route structure 坍缩或随机，不能作为 specialization 证据。

conclusion：
compositional token 和 many-feature grouping 下，普通 top-1 的 route structure 不可靠；same-feature consistency 是弱证据。

boundary：
不能 claim 没有任何 router 可以学到 compositional/family grouping；只能 claim 当前 ordinary top-1 不能作为正证据。

链接下去：
[05_04_02 common-logit causality anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md)

### Anchor: 05_03 Uniform Collapse Common-Offset

解决了什么问题：
回答为什么 feature frequency 已经均匀，bias-free linear router 仍然在 step 0 或早期形成 dominant expert。

和父问题的关系：
它把“均匀 feature 分布应该自然产生均匀 expert 使用”这个直觉打破。均匀数据不保证 hidden state 零均值；共同 hidden component 会造成 expert-specific effective bias。

conclusion：
在 uniform toy setting 中，$h_f=c+r_f$ 里的 $c$ 会通过 $w_e^Tc$ 造成共同偏置；common-score 能预测 step-0 dominant expert，common-logit cancellation 能降低早期 concentration。

boundary：
不能 claim collapse 已解决；position/common source 不是唯一机制；toy 结论不能直接外推真实 LM。

链接下去：
[05_04_02 common-logit causality anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md)

### Anchor: 05_04_01 Uniform Feature Specialization After Position Removal

解决了什么问题：
检查去掉显式 positional common source 后，slot signal 是否能支撑 route specialization，还是训练仍会 collapse。

和父问题的关系：
它把“position shortcut”从主要机制里拆出来，保护 05_03 的 common-offset 解释不过度泛化。

conclusion：
slot signal 可以存在，positive controls 有用；但普通 routing 仍需要机制分解，不能因为去掉 position 后有改善就 claim solved。

boundary：
这是 synthetic uniform slot setting，不证明真实 LM、multi-B feature 或 expert computation causality。

链接下去：
[05_04_02 common-logit causality anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md)

### Anchor: 05_04_02 Dot-Product Common-Logit Causality

解决了什么问题：
把 common-offset 从相关性推进到时序和干预证据：common logit 是否早于 collapse、预测 collapse，并且取消它能否改善 slot routing。

和父问题的关系：
这是 05 线的关键机制裁决。它说明初始化 collapse 不是 feature 不存在，而是 common logit 在 slot margin 稳定前把 top-1 router 推入 common-dominated basin。

conclusion：
在 no-position uniform slot dot-product toy 中，common-logit dominance 是 early、predictive、intervention-relevant 的 collapse mechanism；slot-init 成功更像进入另一个 basin。

boundary：
common cancellation 不是 deployable solution；不能 claim expert computation 已因果专门化；不能直接外推 real LM、cosine router 或长上下文。

链接下去：
[05_04_03 real-text common-logit anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_03_real_text_common_logit_initialization_anchor.md)

### Anchor: 05_04_03 Real-Text Common-Logit Initialization

解决了什么问题：
检查 toy 里的 step-0 common-logit dominance 是否也解释真实 DCLM packed text 上的 early route concentration。

和父问题的关系：
它防止把 synthetic common-logit 机制过度外推到真实数据。真实数据上机制有变形：step 0 不一定由 common margin 主导，但早期训练会快速放大 common/load concentration。

conclusion：
step-0 common dominance 在真实 DCLM 中被削弱；centering 仍降低 max load；step 10 common channel 快速放大，主机制从 pure initialization geometry 转向 early-training feedback。

boundary：
只裁定小型 Qwen-style top-1 MoE、DCLM packed text、随机初始化、300-step early training；不证明 final specialization 或 deployable anti-common init。

链接下去：
[06_02 early-training common-logit amplification anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_02_early_training_common_logit_amplification_anchor.md)

### Anchor: 06_01 Common-Filtered Expert-Spectrum Router Initialization

解决了什么问题：
测试一种从 expert spectrum 构造 router init 的早期方案是否能绕过 common collapse。

和父问题的关系：
它把“是否已有一个可行初始化方法”提前否定，迫使主线转向 stage-wise mechanism，而不是继续堆方法。

conclusion：
V4 common-filtered spectrum linear init 不足以作为成功方法；需要先拆 computation-vs-implementation bridge。

boundary：
不能否定所有 spectrum/parameter-space feature idea；这里只说明当前 linear row-mean bridge 不够。

链接下去：
[06_10 real-DCLM proxy anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_10_real_dclm_proxy_feature_operationalization_anchor.md)

### Anchor: 06_02 Early-Training Common-Logit Amplification

解决了什么问题：
延续 05_04_03，定位真实 DCLM 中 route concentration 是不是早期训练反馈，而不是纯 step-0 初始化偏置。

和父问题的关系：
它把 anti-collapse 问题从“初始化时去 common”推进到“训练过程中防止 common/load amplification”。

conclusion：
真实 DCLM early training 的 common/load amplification 是主要风险；后续 preservation 必须观察 step 5/10 window。

boundary：
仍是早期训练机制，不是最终 specialization；不能单独证明 proxy routing 或 utility。

链接下去：
[06_12 preservation anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_12_real_dclm_proxy_init_training_preservation_anchor.md)

### Anchor: 06_03 High-Dimensional Gaussian Gate Norm Variation

解决了什么问题：
建立 gate-only baseline，确认 row-norm variation 本身能制造负载不均，避免把几何假象误读成 specialization 或 collapse mechanism。

和父问题的关系：
它是指标护栏：在判断“features 是否均匀进 experts”前，先排除 router row norm 导致的假不均匀。

conclusion：
Gaussian-scaled gate 的额外 fixed floor 主要来自 row-norm variation；equal-norm guard 是必要诊断。

boundary：
只解释随机初始化、纯 gate-only、高维均匀输入；不能直接解释 trained MoE collapse。

链接下去：
[06_04 synthetic hidden-state geometry anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_hidden_state_gate_geometry_decomposition_anchor.md)

### Anchor: 06_04 Synthetic Hidden-State Gate Geometry Decomposition

解决了什么问题：
把 step-0 load imbalance 拆成 row norm、hidden common component、二者交互，定位 synthetic hidden-state 中哪个因素主导。

和父问题的关系：
它把 05 的 common-offset 机制转成可量化 hidden geometry decomposition，为后续 common-centered residual discovery 铺路。

conclusion：
hidden common component 是 tested source 中的主导因素；row norm 不是主因。

boundary：
只能 claim initialized synthetic hidden-state step-0 geometry；不能 claim training collapse、real text 或 final method。

链接下去：
[06_05 residual geometry anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_05_common_centered_residual_geometry_diagnostic_anchor.md)

### Anchor: 06_05 Common-Centered Residual Geometry Diagnostic

解决了什么问题：
在 common-centering 后，解释 residual load 为什么仍然存在：是有限样本噪声，还是 residual covariance / structured residual geometry。

和父问题的关系：
它说明去 common 只解决一层问题；剩余 residual geometry 中仍可能有 feature-like structure，可作为 discovery 目标。

conclusion：
residual covariance / structured residual geometry 是 common-centered residual load 的主要来源；finite-sample noise 不是主解释。

boundary：
whitening 是诊断控制，不是最终 router 方法；仍是 initialized synthetic replay。

链接下去：
[06_06 oracle initialization anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_06_feature_level_initialization_positive_control_anchor.md)

### Anchor: 06_06 Feature-Level Initialization Positive Control

解决了什么问题：
验证如果已知 feature identity / feature centroid，是否存在一个 router initialization 能把均匀 features 完美、均匀地分到 experts。

和父问题的关系：
这是“均匀 features 均匀分到 expert”是否可达的 positive control。它证明目标 partition 几何上可达，不是任务本身不可能。

conclusion：
oracle feature-centroid initialization 在 synthetic hidden states 中达到 `feature_NMI=1.0`、load imbalance `L=0`；feature-level routing 可达。

boundary：
这是 oracle，有标签；不能 claim label-free method，也不能 claim training preservation 或 real-data transfer。

链接下去：
[06_07 label-free common/residual control anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_07_label_free_common_residual_control_router_anchor.md)

### Anchor: 06_07 Label-Free Common / Residual-Control Router

解决了什么问题：
测试不用 feature labels，仅用 common centering / projection / whitening 等 label-free controls，能否接近 oracle feature partition。

和父问题的关系：
它区分“改善负载”与“形成 feature specialization”。这一步防止把 anti-collapse 当成 specialization。

conclusion：
simple label-free controls 主要改善 load，不恢复 feature NMI；0/336 label-free rows 通过。

boundary：
不能排除 learned feature discovery、anti-lockin training 或真实 DCLM 机制；只能否定 simple global controls 作为 standalone method。

链接下去：
[06_08 label-free discovery anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_08_label_free_feature_discovery_initialization_anchor.md)

### Anchor: 06_08 Label-Free Feature Discovery Initialization

解决了什么问题：
从“简单 common control 不够”转向“能否无标签发现 feature centers”，测试 route-position residual clustering。

和父问题的关系：
它给“如何从 random/init collapse 进入 feature-aligned basin”提供第一个 label-free discovery route。

conclusion：
route-position residual k-means / spherical k-means 在 synthetic setting 中能恢复 pseudo-feature centers，full-grid cells 达到 `feature_NMI=1.0, L=0`。

boundary：
这是 step-0 discovery 成功，不是训练成功；pair_id 只用于 evaluation；spectral/dictionary 不稳定。

链接下去：
[06_09 training basin preservation anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_09_training_basin_preservation_anchor.md)

### Anchor: 06_09 Training Basin Preservation

解决了什么问题：
测试一旦有 feature-aligned pseudo init，普通训练是否会保持这个 partition。

和父问题的关系：
它把“初始化不塌缩”推进到“训练后不塌缩”。没有 preservation，就不能说进入了 specialization basin。

conclusion：
在 synthetic route-position target training 中，oracle init 和 A06_08 pseudo init 都能保持 `feature_NMI=1.0`、accuracy `1.0`、load `L=0`。

boundary：
训练目标仍是 synthetic route-position target prediction，不是完整 real-text next-token training；不能推出 real DCLM 或 semantic expert。

链接下去：
[06_10 real-DCLM proxy anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_10_real_dclm_proxy_feature_operationalization_anchor.md)

### Anchor: 06_10 Real-DCLM Proxy Feature Operationalization

解决了什么问题：
真实数据没有人工 feature label，因此先定义可评估 proxy：真实 DCLM hidden states 是否存在稳定、非纯 frequency/position 的 clusters。

和父问题的关系：
它把 synthetic feature identity 桥到 real data 的可测 feature axis。没有 proxy，就无法判断 real router 是否 feature-aligned。

conclusion：
真实 DCLM hidden geometry 存在稳定 label-free proxy clusters；step10 late layer 最强，residual step10 mean stability NMI = 0.5211，random 约 0.0002。

boundary：
不能 claim semantic feature discovery、expert specialization、training preservation，且 common-centering 不是 k-means proxy discovery 的关键。

链接下去：
[06_11 real-DCLM proxy-center router initialization anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_11_real_dclm_proxy_center_router_initialization_anchor.md)

### Anchor: 06_11 Real-DCLM Proxy-Center Router Initialization

解决了什么问题：
测试 A06_10 proxy centers 能否转成线性 top-1 router rows，在 step 0 实现 proxy routing。

和父问题的关系：
它证明真实 proxy 不只是 clustering artifact，而是可以成为 actual router initialization。

conclusion：
proxy centers 可线性路由；raw-center raw-input 是当前最强 actual bridge，step0 proxy_route_NMI = 0.7449，random = 0.0343。

boundary：
不能 claim training stability、semantic meaning、expert utility；residual-center 在 centered-input 诊断强，但 raw-input 会受 common bias 压制。

链接下去：
[06_12 training preservation anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_12_real_dclm_proxy_init_training_preservation_anchor.md)

### Anchor: 06_12 Real-DCLM Proxy-Init Training Preservation

解决了什么问题：
测试强 step-0 proxy routing 是否能穿过真实 DCLM next-token training 的早期 step 5/10 collapse window。

和父问题的关系：
这是 06 线的关键失败点。它回答“好的初始化是否足够”：不够，普通训练会覆盖 proxy partition。

conclusion：
raw-center proxy init 从 step0 NMI 0.7549 迅速降到 step5 0.0410、step10 0.0131；LM loss 与 random 接近。这不是 optimization crash，而是 training feedback override。

boundary：
不能 claim proxy useless、expert utility absent、或 preservation objective 不可能；只能 claim ordinary DCLM training 不自动保护 proxy partition。

链接下去：
[06_13 failure decomposition anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_13_real_dclm_proxy_init_failure_decomposition_anchor.md)

### Anchor: 06_13 Real-DCLM Proxy-Init Failure Decomposition

解决了什么问题：
把 A06_12 失败定位到 stage：proxy 不稳定、linear bridge 不够，还是 training feedback 覆盖。

和父问题的关系：
它防止直接换方法。机制发现的进步是知道第一个坏掉的合同，而不是只知道最终分数失败。

conclusion：
第一失败点是 training preservation：proxy discovery 通过，raw-center step0 bridge 通过，step10 routing 被 ordinary training 覆盖。

boundary：
不能 claim broad impossibility、final solution 或 expert utility absence；只能定位当前 pipeline 的 bottleneck。

链接下去：
[06_16 synthetic-to-realistic proxy bridge anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_16_synthetic_to_realistic_proxy_bridge_anchor.md)

### Anchor: 06_14 Real-DCLM Proxy Expert-Utility Binding

解决了什么问题：
预留 utility binding 测试：如果 proxy routing 被保持，所选 expert 是否真的对对应 proxy group 有更高 causal utility。

和父问题的关系：
它定义 specialization 的最终功能条件，但因为 A06_12 preservation 失败，目前不能执行。

conclusion：
parked。当前不能在 routing 未保持时测试 utility，否则会混淆“没有 utility”和“路由已经消失”。

boundary：
不能用当前失败否定 expert utility；只能说 utility binding 依赖 preservation。

链接下去：
[07_03 route-function binding anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_03_route_function_binding_anchor.md)

### Anchor: 06_15 Real-DCLM Utility-Aware Gating Initialization

解决了什么问题：
预留如果 A06_14 找到 utility signal，如何把 utility 合入 gating initialization。

和父问题的关系：
它属于最终方法构造，不是当前机制裁决。

conclusion：
parked。没有 preserved proxy routing 和 utility table，utility-aware init 没有合法输入。

boundary：
不能提前设计成主线方法；否则会变成“为了方法而方法”。

链接下去：
[06_14 utility binding anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_14_real_dclm_proxy_expert_utility_binding_anchor.md)

### Anchor: 06_16 Synthetic-To-Realistic Proxy Bridge

解决了什么问题：
回到 controlled setting，检查从 clean synthetic 到 more realistic input mixture 的 bridge 到底坏在 discovery 还是 preservation。

和父问题的关系：
它修正了 06 的边界：在 no-learned-absolute-position controlled bridge 中，preservation 不是断点；旧 C0 failure 是 learned absolute positional geometry artifact。

conclusion：
same-model no-pos full run 后 C0-C3 discovery 和 preservation 全通过，C4 all-position 7/8 通过但不完全稳定。

boundary：
不测试 RoPE；C4 仍有 1/8 failure；slot-end token 是 feature-specific，不能证明 whole-slot compositional semantics；不能推出 real-DCLM preservation。

链接下去：
若继续 controlled boundary，进入 [06_17 all-position route-relevant feature discovery anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_17_all_position_route_relevant_feature_discovery_anchor.md)；若回应 specialization value，进入 [07_01 common/rare conflict metric audit anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_01_common_rare_conflict_metric_audit_anchor.md)。

### Anchor: 06_17 All-Position Route-Relevant Feature Discovery

解决了什么问题：
解释 A06_16 中 C4 all-position 聚类为什么仍会把 feature 合并：是 route feature geometry 不存在，还是聚类样本池混入了太多非路由 hidden states。

和父问题的关系：
它把“能否发现 feature partition”进一步收紧到“必须先知道哪些 hidden states 是 route-relevant”。这一步防止把所有 token 位置一锅聚类误当成真实 feature discovery。

conclusion：
支持“样本池错配”。route-only 和 slot offset 3 的 held-out route `feature_NMI=1.0`，8/8 seeds 全过；all-position mean `feature_NMI=0.797`、最差 `0.637`、只有 1/8 完全通过；role-balanced all-position 也只有 1/8 完全通过。

boundary：
这不是 real-DCLM semantic feature discovery，也不是最终初始化算法；它只说明 controlled no-position bridge 里，all hidden states 不是合法的 route-initialization proxy population。

链接下去：
若继续 06 controlled bridge，下一步应构建 label-free route-relevant state selector；若转向 value story，进入 [07_01 common/rare conflict metric audit anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_01_common_rare_conflict_metric_audit_anchor.md)。

### Anchor: 07_01 Common / Rare Conflict Metric Audit

解决了什么问题：
在“不塌缩”和“可形成分区”之后，先验证 D07 数据和 `Delta_vs_best_null` 是否能合法衡量 rare-feature interference。

和父问题的关系：
它让 07 正确进入故事线：不是又发明一个 gate，而是先问 expert partition 是否有价值。只有 oracle feature gate 能在 D07 上超过 dense 和 load-only null，后续方法收益才可解释。

conclusion：
supported_controlled_synthetic。D07 是可用的 controlled synthetic audit surface：`Delta_vs_best_null=0.8601 +/- 0.0008`，dense rare loss `1.4399`，load-only rare loss `1.5300`，oracle rare loss `0.5798`；shortcut 最高 `0.5000`，hidden conflict readout `1.0000`。

boundary：
不能 claim common-control works、routing semantic、expert utility exists、真实语料迁移或 neural checkpoint 行为；只能 claim D07 是 controlled synthetic 的合法 method-test surface。

链接下去：
[07_02 common-controlled rare interference anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_02_common_controlled_rare_interference_anchor.md)

### Anchor: 07_02 Common-Controlled Rare Interference

解决了什么问题：
在 A07_01 合法后，测试 label-free common-control 是否降低 rare loss，且超过 load-matched balance-only MoE。

和父问题的关系：
它把 05/06 的 anti-common / anti-collapse 机制转成 value question：控制 common 不只是让负载好看，而是真的减少 rare-feature interference。

conclusion：
supported_controlled_synthetic。common-control 在 D07 上支持 rare-interference reduction：`RIR_cc=0.9502 +/- 0.0006`，`FoO_cc=1.1049`；load-only 和 common-control 的 max load 都是 `0.2500`，active experts 都是 `4.0000`，conflict readout 前后都是 `1.0000`。

boundary：
只能 claim controlled synthetic D07 上 common-control 比 matched balance-only 更能降低 rare loss；不能 claim expert causal specialization、semantic routing、真实语料迁移或可部署架构。

链接下去：
[07_03 route-function binding anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_03_route_function_binding_anchor.md)

### Anchor: 07_03 Route-Function Binding

解决了什么问题：
如果 A07_02 显示 rare loss 改善，再测试 routed experts 是否对 conflict group 有更高 causal utility。

和父问题的关系：
它是从“有用的路由分区”走向“真正 expert specialization”的必要最后一步。没有它，A07_02 最多证明 functional improvement，不证明 expert function 分化。

conclusion：
supported_controlled_synthetic。A07_02 的 rare-loss gain 有 route-function binding 证据：selected-best rate `1.0000` 对 chance `0.2500`，route-conditioned utility advantage 约 `0.950`，modal ablation delta `0.6800`，nonmodal ablation delta `0.0000`。

boundary：
raw expert ID 会跨 seed 置换，必须读 modal-aligned metrics；不能 claim natural-language semantic experts、真实 DCLM specialization、可部署 routing 或 one-feature-one-expert 结构。

链接下去：
若继续 controlled line，下一步是 neural D07 training；若想对接真实主线，下一步是把 route-function diagnostic 迁移到真实 trained checkpoint。

## 4. 07 如何进入故事线

07 的位置不是“06 没做完所以换方向”，而是把 05/06 的必要条件接到最终价值判断上。

05/06 已经回答：

- collapse 不是单纯数据频率问题，uniform feature 也会 collapse；
- common component 和 early top-1 feedback 是核心风险；
- synthetic feature partition 可以被 oracle 或 pseudo centers 找到；
- real DCLM proxy 可以发现并线性路由；
- ordinary real DCLM training 会覆盖 proxy routing；
- 06_17 说明 controlled bridge 中 all-position clustering 失败主要来自样本池错配，真正需要的是 route-relevant state selector；
- load balance 和 route_NMI 都可能误导。

因此 07 必须先问：

如果 gate 已经不塌缩，专家分区是否真的减少 feature interference？

这就是 A07_01 的作用。现在它已经验证 D07 和 `Delta_vs_best_null`：

- oracle feature gate 是否能降低 rare loss；
- dense 和 load-only null 是否公平；
- conflict signal 是否在 routed-token hidden state 可读；
- shortcut 是否能解释结果。

A07_01 已通过，所以 A07_02 合法地测试了 common-control 是否比 load-matched baseline 更好。A07_02 已通过，所以 A07_03 合法地测试了 routed expert 是否真的有 causal utility。当前 07 的支持范围是 controlled synthetic D07，不是 real-DCLM 或自然语义专家。

## 5. 给导师的报告梳理

开场一句：
我现在不是直接 claim MoE 已经 specialization，而是在拆 MoE 为什么连均匀 feature 都不能稳定、均匀地进 expert，并把这个入口问题推进到可验证的 functional value。

第一段，05：
普通 top-1 在 uniform feature 下也会 collapse。原因不是 feature 不存在，而是 hidden state 里有共同成分 $c$，router score 里出现 $w_e^Tc$ 的 expert-specific bias；早期 top-1 会放大这个偏置。common-logit cancellation 能改善 slot routing，但这还不是可部署方法。

第二段，06：
我把问题拆成 stage contract：feature/proxy 是否存在，能否初始化 router，训练是否保持。synthetic 中 pseudo init 可以发现并保持；真实 DCLM 中 proxy 存在且 step-0 可路由，但普通训练 step 5/10 会覆盖它。因此真实主瓶颈是 training feedback override，不是 proxy discovery 或 step-0 bridge。

第三段，06_16/06_17 boundary：
controlled no-pos bridge 修正了旧结论：没有 learned absolute position 时，C0-C3 discovery 和 preservation 都过。A06_17 进一步说明 C4 all-position 的主要问题不是 route-position feature geometry 不存在，而是聚类样本池错配；route-only 和 slot-end hidden states 能完美发现 feature，而 all-position 会把非路由状态混进来。因此 controlled bridge 的下一步应是 route-relevant state selector，而不是继续把所有 hidden states 一起聚类。

第四段，07：
即使解决 collapse 和 preservation，也还不能说 specialization 有价值。07 进入的原因是：要证明 expert partition 降低 common/rare feature interference，而不只是负载均匀。A07_01 已支持 D07 metric surface 合法，A07_02 已支持 common-control 在 matched-load 下减少 rare interference，A07_03 已支持 controlled D07 route-function binding。这个链条可以作为“controlled causal expert specialization”的证据，但不能外推真实语言模型。

## 6. 下一步决策

如果目标是延续机制主线：
优先设计 real-DCLM preservation / anti-feedback anchor，问题是能否让 raw-center proxy routing 穿过 step 5/10 collapse window，同时不伤 LM loss。

如果目标是修补 controlled bridge：
优先设计 label-free route-relevant state selector，问题是能否在不知道真实 route position 的情况下筛出 route-like hidden states，再做 feature clustering。

如果目标是给导师展示“为什么这个方向值得做”：
使用 07 的完整结果链：A07_01 证明 D07 surface 合法，A07_02 证明 common-control 的 rare-loss benefit 超过 matched load-only，A07_03 证明 route-function binding。报告中必须同时强调这是 controlled synthetic 结果，real-DCLM preservation 仍未解决。

当前推荐：
短期讨论用 07 结果链说明 specialization 的 value；下一轮实验在机制线上二选一：要么做 real-DCLM preservation / anti-feedback，要么做 06_17 后续的 route-relevant state selector。若目标是最快推进主线，优先 real-DCLM preservation，因为它仍是从 controlled result 走向真实 checkpoint 的第一瓶颈。
