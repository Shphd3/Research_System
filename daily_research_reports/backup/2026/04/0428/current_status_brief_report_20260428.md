# Synthetic Natural Zipfian Hierarchical MoE 当前 Brief Report

更新时间：2026-04-28  
实验目录：`spectral_router/exp_hierarchical/synthetic_natural_zipfian_hier_moe`

## 0. 背景和阅读说明

本 brief 记录的是 **Synthetic Natural Zipfian Hierarchical MoE** 这条实验线的最新状态。它不是在真实语料上直接证明语言模型天然有层级 MoE 结构，而是在一个生成机制已知的 synthetic natural text 数据集中做机制验证：

> 如果数据确实由 `common / coarse / fine` 三层因素生成，并且词、短语、token 的出现频率满足 Zipfian 长尾分布，那么冻结 Qwen3-0.6B backbone 后，只训练 layer-8 replacement block，模型能不能学出有用的层级路由和专家分工？

这里需要区分三个概念：

1. **Soft hierarchical mixture**：所有专家都会被计算，只是按 router probability 加权求和；训练稳定，但不是严格 sparse MoE。
2. **Top-1 sparse hierarchical MoE**：每个 token 走 top-1 coarse/source/fine path；这是更接近真正 MoE 的函数形式，但当前工程实现仍是 one-hot/ST 权重组合，不是高效 sparse dispatch kernel。
3. **Oracle diagnostic**：直接使用数据生成时的真实 `coarse_label / fine_label / token_source` 走路由；它不是可部署模型，而是用来判断专家结构本身是否有上界潜力。

因此，当前报告里的实验不能只看 group 代号。关键判断必须同时看：模型做了什么、训练了多久、是否参数量匹配、是否使用真实标签、是否是 soft mixture 或 top-1 path、以及 route 指标是否允许 expert id 置换。

## 1. 当前项目定位

本 series 的目标是构造一个真相可控的 synthetic natural Zipfian hierarchy dataset，并在 frozen Qwen3-0.6B 的 layer-8 replacement/adaptation block 上测试不同 MoE 结构是否能学出有用的层级专家分工。

这条线目前已经从“soft hierarchical mixture”推进到“top-1 sparse hierarchical MoE”补充实验。当前结果支持两个事实：

1. 长训显著降低 NTP loss，说明 1500-step formal run 明显训练不足。
2. top-1 sparse oracle diagnostic 明显强于 learned top-1 router；learned M-band top-1 在当前 loss 指标上没有超过 random top-1。这说明 **M-band learned routing 的因果优势尚未建立**。同时，这也不能被简单解读为“模型完全没有学到任何层级”，因为旧式 router recovery gate 带有固定 label-to-expert 对齐假设，只能作为诊断信号。

## 2. 数据构建

数据不是外部真实语料，而是 synthetic natural text。每条 document 先均匀采样 `coarse_label`，再在该 coarse 下均匀采样 `fine_label`。Zipfian 控制的是 word / phrase / token 的出现频率，不是类别采样频率。

| 项 | 设置 |
|---|---:|
| train docs | 20,000 |
| valid docs | 1,000 |
| test docs | 1,000 |
| seq_len | 128 |
| coarse classes | 4 |
| fine classes | 16 |
| fine per coarse | 4 |
| common phrase pool | 512 |
| coarse phrase pool | 4 x 256 |
| fine phrase pool | 16 x 128 |

coarse labels:

| id | coarse label |
|---:|---|
| 0 | biomedicine |
| 1 | computing |
| 2 | materials |
| 3 | climate |

fine labels:

| coarse | fine labels |
|---|---|
| biomedicine | cell_signaling, clinical_trial, genomics, immunology |
| computing | optimization, language_modeling, network_security, robotics |
| materials | alloy_design, crystal_growth, polymer_film, battery_interface |
| climate | carbon_cycle, hydrology, urban_heat, biodiversity |

数据 sanity 已通过：phrase-level Zipfian slope 约 1.05，token-id-level Zipfian slope 约 1.01；template-only shortcut 接近随机水平；prefix 16/32/64/128 上 coarse/fine predictability 足够高，说明文本中确实存在可恢复层级信号。

## 3. 共同训练流程

所有模型共享以下流程：

1. 加载 pretrained Qwen3-0.6B。
2. 冻结 backbone、embedding、attention、layer norm、LM head 和原始 MLP 权重。
3. 在 layer 8 替换 MLP 为：冻结原始 MLP copy + trainable adapter / router / expert delta。
4. 训练目标为 next-token prediction cross entropy。
5. 只训练 replacement block 中的 adapter/router/expert 参数。
6. 使用 AdamW，learning rate `5e-5`，weight decay `0.01`，dtype `bfloat16`。
7. 使用 4-GPU shard 并行，每张卡跑不同 group；不是 DDP。
8. 每个 group 使用 seeds `0,1,2`。
9. 输出 `summary.csv`、`all_metrics.csv`、`param_budget.csv`、`gate.json`、中文 report 和 shard logs。

主要 projection bands：

| band | 定义 |
|---|---|
| `x_head` | `P_1:16(h - mu)` |
| `x_M` | `P_17:207(h - mu)` |
| `x_Mcc` | `P_17:80(h - mu)` |
| `x_Mtail` | `P_81:207(h - mu)` |
| `x_R` | same-dim random projection |

## 4. 模型架构总览

所有模型输出形式均为：

`M(h) = M_0(h) + Delta(h)`

其中 `M_0` 是冻结的原始 layer-8 MLP，`Delta` 是 trainable adaptation delta。

下面的 group 名称是实验代码中的简称；每个重要 group 的含义在对应小节中展开说明。

### 4.1 Dense Baseline

| group | 架构 | 参数 |
|---|---|---:|
| `G0_dense_matched` | 单个 AdapterMLP，输入 raw hidden | 3,670,016 |

`Delta(h) = F_dense(h)`。

做的要点：冻结 backbone，只在 layer-8 replacement block 中训练一个单独 dense adapter，参数量尽量匹配 MoE 主模型。  
作用：排除“MoE 好只是因为参数更多”的解释。

### 4.2 Flat MoE

| group | router input | expert input | experts | LB | 参数 |
|---|---|---|---:|---|---:|
| `G1_flat_raw_lb` | raw hidden | raw hidden | 16 | yes | 3,686,400 |
| `G2_flat_middle_lb` | `x_M` | raw hidden | 16 | yes | 3,686,400 |
| `G2_flat_middle` | `x_M` | raw hidden | 16 | no | 3,686,400 |

形式：

`Delta(h) = sum_i softmax(W z)_i E_i(h)`。

做的要点：使用同一组 flat experts，没有树状 coarse/source/fine 层级；区别只在 router 输入是 raw hidden 还是 middle-band projection。  
注意：flat MoE 当前是 soft mixture，所有 experts 都参与加权求和，不是 sparse dispatch。

### 4.3 Middle-Band Hierarchical Soft MoE

| group | router input | expert input | experts | 参数 |
|---|---|---|---:|---:|
| `G3_h_mid_soft` | `x_M` | raw hidden | 16 leaf experts | 3,678,208 |

形式：

`Delta(h) = sum_c sum_f p(c | x_M) p(f | x_M) E_{c,f}(h)`。

做的要点：把 router factorize 成 coarse 和 fine 两层，但 coarse group 内没有继续拆 conditional-common / conditional-tail。  
作用：作为“浅层 hierarchy”对照，检查真正 CondCT 结构是否必要。

### 4.4 Conditional Common/Tail Soft Hierarchical MoE

| group | router input | expert input | LB | oracle | 参数 |
|---|---|---|---|---|---:|
| `G4_h_condct_soft` | `x_M` | raw hidden | no | no | 3,698,688 |
| `G5_h_condct_soft_lb` | `x_M` | raw hidden | yes | no | 3,698,688 |
| `G6_h_condct_level_input` | `x_M/x_Mcc/x_Mtail` | level-specific bands | no | no | 3,698,688 |
| `G7_h_oracle_condct` | label/source path | raw hidden | no | yes | 3,698,688 |
| `G8_h_rand_condct` | `x_R` | raw hidden | no | no | 3,698,688 |

专家组成：

| expert type | 数量 | rank |
|---|---:|---:|
| global common expert | 1 | 256 |
| conditional-common expert | 4 | 128 |
| conditional-tail/fine expert | 16 | 64 |

soft CondCT 形式：

`Delta(h) = E_g(input_g) + sum_c p_c q_c^cc E_c^cc(input_cc) + sum_c sum_f p_c q_c^tail r_{c,f} E_{c,f}^tail(input_tail)`。

做的要点：先用 coarse router 选择大组，再在该 group 内区分 conditional-common 与 conditional-tail；tail 分支下再 fine routing。  
其中 `G6` 是当前 soft hierarchical 主模型，因为它不仅让 router 使用分层 band，也让不同层级 expert 接收不同输入：

| module | input |
|---|---|
| global expert | `x_head` |
| coarse router | `x_M` |
| source router | `x_Mcc` |
| fine router | `x_Mtail` |
| conditional-common expert | `x_Mcc` |
| conditional-tail/fine expert | `x_Mtail` |

### 4.5 Top-1 Sparse Hierarchical MoE

| group | router input | expert input | LB | oracle | 参数 |
|---|---|---|---|---|---:|
| `G9_h_condct_top1` | `x_M/x_Mcc/x_Mtail` | level-specific bands | no | no | 3,698,688 |
| `G10_h_condct_top1_lb` | `x_M/x_Mcc/x_Mtail` | level-specific bands | yes | no | 3,698,688 |
| `G11_h_condct_top1_rand` | `x_R` for coarse router | level-specific bands | no | no | 3,698,688 |
| `G12_h_condct_top1_oracle_diag` | label/source path | level-specific bands | no | yes | 3,698,688 |

数学路径：

1. coarse router 选择 `c* = argmax_c p(c | x_M)`。
2. source router 选择 `s* = argmax_s q(s | x_Mcc, c*)`，其中 `s in {cc, tail}`。
3. 如果 `s*=cc`，激活 `E_g(x_head) + E_{c*}^cc(x_Mcc)`。
4. 如果 `s*=tail`，fine router 选择 `f* = argmax_f r(f | x_Mtail, c*)`，激活 `E_g(x_head) + E_{c*,f*}^tail(x_Mtail)`。

训练中 forward 使用 hard top-1 path，router gradient 使用 straight-through estimator。工程上当前仍通过遍历 experts 并乘 one-hot/ST weights 来实现，所以它是“函数行为 top-1 sparse”，还不是高效 token dispatch sparse kernel。

做的要点：这是当前最接近“真正 Hierarchical MoE”的模型族，因为每个 token 只走一个 coarse/source/fine path；但当前实现目标是研究诊断，不是高性能 MoE kernel。

## 5. 已完成实验结果

### 5.1 `formal_ablation_v1`

配置：`1500 steps`，`eval_every=300`，3 seeds。

做的要点：短训横向比较 dense、flat MoE、浅层 hierarchy、CondCT soft hierarchy、level-specific input、random router 和 oracle soft path。这个实验主要用于快速筛选结构，不适合直接给最终结论，因为训练步数明显不足。

| group | test loss |
|---|---:|
| `G6_h_condct_level_input` | 1.6572 |
| `G0_dense_matched` | 1.6712 |
| `G8_h_rand_condct` | 1.7914 |
| `G5_h_condct_soft_lb` | 1.8108 |
| `G4_h_condct_soft` | 1.8125 |
| `G2_flat_middle_lb` | 1.9683 |
| `G1_flat_raw_lb` | 1.9770 |
| `G3_h_mid_soft` | 2.0213 |
| `G7_h_oracle_condct` | 2.1801 |

结论：短训下 `G6_h_condct_level_input` 略优于 dense，也明显优于 random/flat/soft CondCT controls。这个结果只说明 level-specific soft hierarchy 是有价值候选；是否形成有意义的层级路由，需要用 permutation-invariant recovery、route-label/source mutual information、route usage by label/source 和 counterfactual expert advantage 联合判断。

### 5.2 `top1_sparse_two_epoch_v1`

配置：`40000 steps`，约 2 epoch，`eval_every=4000`，3 seeds。该补充实验已完成并 merge。

做的要点：训练 top-1 hard path CondCT 模型，并与 random top-1 router、LB 版本和 oracle top-1 diagnostic 比较。这个实验的目的不是测试训练速度，而是检查 sparse/hard hierarchical path 是否有上界、learned M-band router 是否超过 random router。

| group | test loss | coarse Hungarian | fine Hungarian | route source MI | oracle regret |
|---|---:|---:|---:|---:|---:|
| `G12_h_condct_top1_oracle_diag` | 1.1532 | 1.0000 | 1.0000 | 0.3019 | 0.3674 |
| `G11_h_condct_top1_rand` | 1.1713 | 0.2573 | 0.1226 | 0.0687 | 0.9688 |
| `G9_h_condct_top1` | 1.1741 | 0.2987 | 0.1566 | 0.0295 | 0.8977 |
| `G10_h_condct_top1_lb` | 1.1749 | 0.2799 | 0.1520 | 0.0231 | 0.9808 |

Gate:

| gate | result |
|---|---|
| real router beats random | false |
| router recovery | false |
| route source MI | false |
| oracle stronger than learned | true |
| pass | false |

解释：上表是当前脚本的自动 gate 输出。不能把 `router recovery=false` 单独当成“模型没有达到我们想要的层级效果”，因为固定 label-to-expert recovery 会低估存在 expert id 置换或非人工标签路由的模型。当前更稳妥的结论是：top-1 sparse oracle diagnostic 很强，说明 hard path 专家结构有潜在表达能力；learned M-band top-1 在当前 loss 上没有打败 random router control，因此 M-band routing 的因果优势尚未建立。是否存在另一种有用的模型内层级，需要更严格的互信息、置换不变恢复和反事实专家收益分析。

## 6. 进行中或未完成实验

### `two_epoch_core_v1`

目标：用 2 epoch 重跑 core controls，作为 top-1 sparse 的正式横向比较。

计划 groups：

`G0_dense_matched,G1_flat_raw_lb,G2_flat_middle,G5_h_condct_soft_lb,G6_h_condct_level_input,G8_h_rand_condct`

当前状态：

| shard | groups | status |
|---|---|---|
| cuda0 | `G0_dense_matched,G1_flat_raw_lb` | incomplete；日志停在 seed 2 `G0_dense_matched` step 8000 |
| cuda1 | `G2_flat_middle,G8_h_rand_condct` | incomplete；日志停在 seed 1 `G8_h_rand_condct` step 24000 |
| cuda2 | `G5_h_condct_soft_lb` | done |
| cuda3 | `G6_h_condct_level_input` | done |

当前没有 merged `summary.csv`，本地也未看到仍在运行的 `two_epoch_core_v1` 进程。需要用 `sco` 复核 ACP job 是否退出；若已退出，需要续跑或重跑 cuda0/cuda1 shards 后再 merge。

## 7. 关键诊断指标

| metric | 含义 |
|---|---|
| `loss_mean` | test next-token prediction cross entropy |
| `loss_source_common/coarse/fine` | 按数据生成 token_source 分桶的 NTP loss |
| `loss_bucket_common/middle/rare` | 按 token frequency bucket 分桶的 NTP loss |
| `coarse_hungarian_acc` | 允许 route id 任意置换后的 coarse recovery |
| `fine_hungarian_acc` | 允许 route id 任意置换后的 fine recovery |
| `route_coarse_mi` | route 与 coarse label 的 normalized mutual information |
| `route_fine_mi` | route 与 fine label 的 normalized mutual information |
| `route_source_mi` | route 与 token_source 的 normalized mutual information |
| `adv_second_mean` | selected path 相对 second-best path 的 counterfactual loss advantage |
| `adv_random_mean` | selected path 相对平均/random path 的 counterfactual loss advantage |
| `oracle_regret_mean` | selected path loss 与 oracle-min path loss 的差距，越低越好 |

重要解释：固定 `coarse_acc/fine_acc/source_acc` 不能作为目标判据，因为它默认“某个 category 对应某个固定 expert”。这个假设在 MoE 中通常不成立：expert index 有置换对称性，而且最优路由变量可能按 token_source、token frequency bucket、局部上下文、短语共现或表示几何来划分，不一定等于人工 `coarse_label/fine_label`。因此，旧式 fixed-index recovery 只能作为辅助诊断，不能用来声称模型“没有达到目标”。现在更应该看 Hungarian recovery、route MI、counterfactual advantage 和 oracle regret；即便这些指标较低，也只能说明“与人工标签层级对齐不足”，不能直接否定存在另一种有用的模型内层级。

## 8. 当前工程判断

当前代码是研究原型，不是生产级 MoE 实现：

1. soft MoE 会计算所有 experts，不是高效稀疏 dispatch。
2. top-1 sparse 目前是函数层面的 hard path + ST gradient，但实现上仍枚举 experts 后用 one-hot/ST weights 组合，不是 fused sparse kernel。
3. 参数预算基本匹配 expert budget，但 CondCT/router 有小额 router overhead。
4. 训练数据、模型、diagnostics 在一个 runner 内，适合快速实验，但需要进一步模块化才能长期维护。
5. 当前 evidence 还没有支持“learned router 与人工语义标签层级显式对齐”；更准确的说法是：top-1 oracle path 可学，learned route 在当前自动 gate 下尚未表现出稳定的人工标签对齐，random router control 在 loss 上略优。这个结论不等同于“没有形成有用层级”。

## 9. Daily Report 可用结论

今日可记录：

1. Synthetic natural Zipfian hierarchy 数据已稳定构造并通过 sanity check；类别采样均匀，词/短语/token 频率符合 Zipfian power-law。
2. 当前模型族已经覆盖 dense、flat MoE、soft hierarchical MoE、conditional common/tail soft hierarchy、top-1 sparse hierarchy、random control 和 oracle diagnostic。
3. 1500-step formal ablation 中，`G6_h_condct_level_input` 是最佳 soft model。旧式 router recovery 不足不能作为失败结论，因为 fixed category-to-expert recovery 本身有问题；后续需要使用 permutation-invariant recovery、mutual information 和 counterfactual expert advantage。
4. 2-epoch top-1 sparse 补充实验已完成：oracle top-1 最强，learned M-band top-1 没有超过 random top-1。当前只能说 M-band routing 的因果优势尚未建立，不能说 hierarchical MoE 没有学到任何有用层级。
5. 2-epoch core controls 尚未完整 merge；需要续跑/重跑 cuda0 和 cuda1 shards 后，再完成 soft G6、dense、flat、random 与 top-1 sparse 的正式横向比较。

## 10. 下一步建议

优先级最高：

1. 修复或续跑 `two_epoch_core_v1` 未完成 shards，拿到完整 2-epoch core controls。
2. 将 `top1_sparse_two_epoch_v1` 与完整 core controls 横向比较，判断 top-1 sparse 是否真的优于 soft G6/dense/random。
3. 重新定义 router recovery：不要使用固定 category-to-expert accuracy 作为 gate；至少加入 route-label/source mutual information、Hungarian matching、route usage by label/source、counterfactual selected-vs-oracle gap。
4. 如果 oracle top-1 仍显著强于 learned top-1，下一步应做 advantage-aware router training 或 oracle-distilled router training。
5. 如果 random router 继续接近或超过 M-band router，需要重新检验 frequency/variance band 对 routing 的因果作用。
