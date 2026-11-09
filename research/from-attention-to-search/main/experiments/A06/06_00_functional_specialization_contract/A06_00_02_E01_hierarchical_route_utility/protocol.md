# Protocol: A06_00_02_E01 Hierarchical Route Utility

Anchor:

```text
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md
```

## 1. Run Goal

这次实验只问一个问题：

```text
如果给 MoE 一个 always-on common path，再把剩下的 leaf route 做成层级结构，
它能不能把“按 slot 路由”和“这个 expert/path 对该 slot 真的有用”绑起来？
```

上一轮 multi-B 实验已经说明：slot 信息在 hidden state 里是可见的，oracle routing 也能工作；问题不是“模型看不见 slot”，而是普通 flat top-1 router 学到的 assignment 不稳定，未必选中对该 slot 最有用的 expert。这里测试 hierarchy/common path 是否能把共享成分和 slot-specific 成分拆开。

## 2. Data Construction

使用受控 synthetic NTP 数据，先不引入 Zipf，避免把 frequency shortcut 和 hierarchy 机制混在一起。

```text
seq_len = 32
slots = 4
B identities = 64
positions 10-14: slot/context prefix
position 15: B_i
position 16: Y_{slot,i}
```

目标规则：

\[
Y_{s,i}=target\_start+s \times 64+i.
\]

同一个 \(B_i\) 在不同 slot 下对应不同 target；因此如果 router 真按 slot/function 分，它应该在同一 slot 下对不同 \(B_i\) 给出一致 leaf/path，而不是被 \(B_i\) identity 拉走。

数据规模：

```text
train_samples_per_slot = 5000  -> 20,000 train rows / condition / seed
eval_samples_per_slot = 1600   -> 6,400 eval rows / condition / seed
calibration_samples_per_slot = 512
```

第一批条件：

```text
A_long_repeated_slot_init
B_long_distributed_slot_init
```

## 3. Model / Training / Evaluation Setup

训练设置：

```text
loss = full NTP CE over all positions
steps = 3000
batch_size = 384
load balance = off
seeds = 20260521, 20260522, 20260523, 20260524
```

`target_ce` 只作为 B-position diagnostic，不参与优化。

### A. `flat_top1`

普通 flat top-1 Switch-style MoE：

```text
4 experts
expert ffn_dim = 256
active ffn_dim/token = 256
output = p_e f_e(h)
```

### B. `common_flat`

加入 global common expert，但 leaf router 仍是一层：

```text
global common ffn_dim = 64
4 leaf experts, leaf ffn_dim = 192
active ffn_dim/token = 64 + 192 = 256
output = f_common(h) + p_j f_leaf,j(h)
```

这个模型判断：只给共享计算一条常驻路径，是否已经足够。

### C. `hierarchical_common`

真正的两层级 route：

```text
global common ffn_dim = 32
root router: 2 groups
selected group common ffn_dim = 48
inner router: 2 leaf choices inside each group
selected leaf ffn_dim = 176
active ffn_dim/token = 32 + 48 + 176 = 256
```

计算形式：

\[
y=f_{\mathrm{global}}(h)+p_g f_{\mathrm{group},g}(h)+p_g p_{\ell|g} f_{\mathrm{leaf},g,\ell}(h).
\]

三种模型优先对齐 active FFN width / active compute；total parameters 会记录，但不是第一公平性标准。

## 4. Configs And Commands

Code workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
```

Runner:

```text
scripts/run_hierarchical_route_utility_binding.py
```

Config:

```text
configs/hierarchical_route_utility_binding.json
```

Submit:

```text
scripts/submit_hierarchical_route_utility_binding_4gpu_acp.sh
```

## 5. Metrics And Artifacts

Primary metric:

```text
assignment_utility_agreement
```

它回答：模型实际选择的 expert/path，是不是 ablation 后对这个 slot 最有用的 expert/path。

Supporting metrics:

```text
route-slot NMI
route-B NMI
conditional route-B NMI within each slot
slot-B route consistency
forced path target CE heatmap
ablation utility heatmap
global/common/group common ablation delta
full_ntp_ce / target_ce / target_accuracy
path load entropy
```

关键图：

```text
slot x B route map
route-slot heatmap
ablation utility heatmap
assignment-utility trajectory
```

## 6. Pass / Fail Criteria

支持 hierarchy/common path：

```text
hierarchical_common 相比 flat_top1：
1. assignment_utility_agreement 更高；
2. leaf/path ablation utility 更接近 slot diagonal；
3. 同一 slot 下跨 B_i route 更一致；
4. route-B NMI 或 conditional route-B NMI 不成为主解释；
5. full_ntp_ce / target_accuracy 不明显恶化。
```

如果 `common_flat` 已经接近或超过 `hierarchical_common`，说明 common path 可能是主要机制，两层 group structure 不是必要条件。

如果 B/C 只降低 loss、不改善 utility binding，则不能算解决 specialization。

## 7. Failure Modes To Check

```text
1. 把 loss 下降误读成 specialization；
2. 只看 route NMI，不看 ablation utility；
3. 忽略同一 slot 下不同 B_i 的路由一致性；
4. 把 64-B moderate stress 过度外推到 256-B 或真实语料；
5. 忽略 active compute 与 total parameters 的区别。
```

## 8. Result Location

Result dir:

```text
active/synthetic_data_understanding/results/hierarchical_route_utility_binding/<run_name>
```

Figure dir:

```text
active/synthetic_data_understanding/figures/hierarchical_route_utility_binding/<run_name>
```

Curated docs:

```text
Projects/from-attention-to-search/main/experiments/hierarchical_route_utility_binding/summary.md
Projects/from-attention-to-search/main/experiments/hierarchical_route_utility_binding/detailed.md
```
