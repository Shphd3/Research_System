# C-D Oracle-MoE 执行报告：给理论 AI 复核

## 1. 当前目标

本轮不是 Reverse Index 实验，而是先完成 Oracle-MoE 的 C-series 训练和 D-series 行为诊断。

核心问题：

```text
router 分区、synthetic feature 分配、expert 功能差异、NTP loss 是否一致？
```

必须区分三件事：

1. router 把样本分给哪个 expert；
2. planted feature 是否刚好对应这种分区；
3. 被选中的 expert 是否真的比其他 expert 更擅长该样本。

## 2. 模型定义

使用 1-layer Transformer + 1 Oracle-MoE block：

```text
token + position embedding
-> causal self-attention
-> Oracle-MoE
-> LM head
```

Oracle-MoE 的关键定义：

```text
gate_input   = attention_output
expert_input = original hidden / residual entering MoE
```

代码中对应：

```text
z_t = attention_output_t
h_t = x0_t + attention_output_t
router = router(z_t)
expert = Expert(h_t)
```

这意味着：

- router 只看 attention output；
- expert 仍处理 residual hidden；
- 行为诊断中的 `gate_input` 必须解释为 attention-output 表征空间。

## 3. 数据

当前 Phase 1 只使用 `unique_uniform`：

| feature | relation | count |
|---|---|---:|
| ABC | `[1,2] -> 22` | 3900 |
| DEF | `[3,4] -> 23` | 3900 |
| GHI | `[6,7] -> 20` | 3900 |
| JKL | `[8,9] -> 21` | 3900 |

暂不使用 shared-target / crossed-factorial，因为本轮先验证 C-series router design 与 boundary/utility 是否一致。

## 4. C-Series 训练条件

五个 variants：

| ID | 名称 | router | loss |
|---|---|---|---|
| C0 | `standard_oracle_linear` | linear router | `$L_{\text{NTP}} + 0.01L_{\text{balance}}$` |
| C1 | `fixed_parameter_center` | fixed expert parameter center | `$L_{\text{NTP}} + 0.01L_{\text{balance}}$` |
| C2 | `trainable_center_repulsion` | trainable center router | `$L_{\text{NTP}} + 0.01L_{\text{balance}} + 1.0L_{\text{repulsion}}$` |
| C3 | `inhibition_margin` | linear router + inhibition | `$L_{\text{NTP}} + 0.01L_{\text{balance}} + 0.5L_{\text{inhibit}}$` |
| C4 | `center_inhibition` | trainable center + inhibition | `$L_{\text{NTP}} + 0.01L_{\text{balance}} + 1.0L_{\text{repulsion}} + 0.5L_{\text{inhibit}}$` |

参数：

```text
seq_len = 32
vocab_size = 1000
d_model = 64
n_heads = 4
num_experts = 4
expert_ffn_dim = 128
batch_size = 128
steps = 10000
lr = 0.0006
seeds = 20260513-20260517
```

## 5. Router 形式

C0/C3：

```text
logits_e = W_e LN(z_t) + b_e
route = argmax_e logits_e
```

C1：

```text
c_e = normalize(first PCA direction of Expert_e.W_in)
logits_e = tau * cosine(normalize(LN(z_t)), c_e)
```

C2/C4：

```text
logits_e = tau * cosine(normalize(LN(z_t)), normalize(c_e))
```

center repulsion：

```text
L_repulsion =
mean_{e != e'} max(0, cosine(c_e, c_e') - 0.0)^2
```

inhibition：

```text
L_inhibit =
mean_{e != e*} max(0, 0.1 - (CE_other_e - CE_selected))
```

这里的 `CE_other_e` 通过 all-expert forward 得到，所以 inhibition 诊断的是 selected expert 是否被训练成功能上优于其他 experts。

## 6. 关键实现细节，建议 AI 重点复核

### 6.1 Hard top-1 routing 的梯度问题

当前 route 使用：

```text
expert_id = argmax(router_probs)
```

这意味着 NTP loss 对 router 的离散选择没有直接可微梯度；router 主要通过 load-balance、center/inhibition 的间接项改变。

需要复核的问题：

```text
如果目标是测试 natural router training dynamics，是否需要 straight-through / soft mixture / Gumbel routing 对照？
```

当前实验仍然有意义，因为它诊断的是这个 top-1 Oracle-MoE 设置下的 router 行为，但不能过度解释为所有 MoE router 的自然梯度机制。

### 6.2 Inhibition 会更新 non-selected experts

`L_inhibit` 在 violation 时会推动：

```text
CE_selected 下降
CE_other 上升
```

这符合“让 selected expert 排他”的设计，但也可能人为损害 non-selected experts 的通用能力。

需要复核的问题：

```text
inhibition 是 functional exclusivity diagnostic，还是过强的人为反机制？
```

因此报告中必须看 NTP/readback 是否变差。

### 6.3 C1 fixed center 的定义

C1 使用 expert 第一层输入矩阵 `W_in` 的第一 PCA direction 作为 fixed center。

需要复核的问题：

```text
fixed center 是否应该使用 W_in 行均值、第一主成分，还是初始化时随机正交中心？
```

当前实现选择第一 PCA direction，因为它更像 expert 参数中最强的输入方向。

### 6.4 Router boundary 空间

Boundary audit 中，feature centroid 和 boundary 都在 router 真正使用的空间里比较：

- C0/C3: `LN(z_t)`；
- C1/C2/C4: `normalize(LN(z_t))`。

需要复核的问题：

```text
是否应同时报告 raw attention_output 空间和 router-normalized 空间？
```

当前主报告用 router-normalized 空间，因为它最接近 router 实际 logits。

## 7. D-Series 行为诊断

行为诊断只加载 checkpoint，不训练。

### D0 Sanity

检查：

```text
gate_input = attention_output
expert_input = original_hidden / residual
gate_input != expert_input
```

### D1 Router Cell Exemplar

每个 expert 取 routing margin 最大的样本，记录 token、feature、target、attention source、loss、target probability。

目的：看 expert cell 的高置信样本共享什么。

### D2 Expert Cell Composition

比较以下变量和 expert id 的互信息：

```text
feature
target_token
prefix_end_token
position
attention_source_token
hidden_norm_bin
loss_bin
router_entropy_bin
```

目的：判断哪个变量最解释 expert assignment。

### D3 Counterfactual Route Flip

构造 matched pairs，看 route 是否翻转。

目的：判断 router 对 feature、surface token、target、attention source 哪个变量敏感。

### D4 Boundary Walk

在两个 gate_input 向量之间插值：

```text
h(alpha) = normalize((1-alpha) h_a + alpha h_b)
```

目的：看 router 边界是否和 feature 边界一致。

### D5 Common Direction Removal

去掉 mean/top-PC 等 common direction，再看 route 是否变化。

目的：判断 router 是否依赖 common/high-variance geometry。

### D6 Expert Utility Alignment

强制同一 feature 走每个 expert：

```text
CE(feature, expert)
P(target | feature, expert)
```

目的：判断 router 选的 expert 是否真的是功能上最好的 expert。

### D7 Inhibition Diagnostic

只对 C3/C4 看：

```text
CE_other - CE_selected
selected expert win rate
margin violation rate
```

目的：判断 inhibition 是功能有效，还是只制造 routing exclusivity。

## 8. C-Series Boundary Direction Audit

新增补充诊断，只读 C0-C4 checkpoints。

### D1 Boundary vs Feature Direction

feature centroid：

```text
c_f = mean(z_t | feature=f)
```

feature direction：

```text
d_{f,f'} = normalize(c_f - c_f')
```

router boundary：

```text
b_{e,e'} = normalize(p_e - p_e')
```

其中：

- C0/C3: `p_e = W_e`；
- C1: `p_e = fixed parameter center`；
- C2/C4: `p_e = learned center`。

指标：

```text
cos(d_{f,f'}, b_{e,e'})
```

### D2 Router Boundary SVD Energy

对 `gate_input = attention_output` 做 SVD：

```text
Z_centered = U S V^T
energy_i = (b^T v_i)^2
```

band：

```text
top_shared = PC 0-25%
middle = PC 25-75%
tail = PC 75-100%
```

### D3 Feature Direction SVD Energy

同样计算 feature direction 在 SVD basis 上的能量。

判断：

- feature 在 tail，而 boundary 在 top：router 忽略 feature-specific direction；
- 同 band 且 cosine 高：支持 feature-aligned boundary；
- 同 band 但 cosine 低：router 使用同类方差区间，但不是 feature direction。

### D4 Variant Effect

比较 C0-C4：

```text
feature_alignment_mean
top_shared_energy
middle_energy
tail_energy
feature_expert_NMI
router_selects_best_expert_rate
selected_minus_best_CE
```

### D5 Position Effect

位置：

```text
prefix_first
prefix_end
target_pos
background
```

注意：`target_pos` 只作为 shortcut/leakage diagnostic，不能作为正常 NTP routing 证据。

### D6 Boundary Alignment vs Utility

合并：

```text
boundary feature alignment
router_selects_best_expert_rate
selected_minus_best_CE
forced routing utility matrix
```

目的：判断 feature-aligned boundary 是否真的对应 task utility。

## 9. 输出目录

训练：

```text
outputs/oracle_moe_router_phase1_20260519/
figures/oracle_moe_router_phase1_20260519/
```

行为诊断：

```text
outputs/router_behavior_diagnostic_20260519/
figures/router_behavior_diagnostic_20260519/
```

boundary audit：

```text
outputs/router_behavior_diagnostic_20260519/c_boundary_direction_audit/
figures/router_behavior_diagnostic_20260519/c_boundary_direction_audit/
```

## 10. 实际执行状态

已完成：

- 本地 C0/C2/C3 training smoke；
- 本地 D0-D7 behavior diagnostic smoke；
- 本地 C-series boundary direction audit smoke；
- C0-C4 full run；
- D0-D7 behavior diagnostic；
- C-series boundary direction audit。

最终成功 ACP jobs：

| stage | job | resource | state |
|---|---|---|---|
| C-series training | `pt-l65uzwbz` | 4-card guaranteed/default, `RESERVED` | `SUCCEEDED` |
| D-series diagnostic + boundary audit | `pt-vhg9jerf` | 4-card guaranteed/default, `RESERVED` | `SUCCEEDED` |

中间失败/停止项：

- `pt-jjia1fqr`: remote command variable export 问题，已停止；
- `pt-v40j6g6c`: 4-card spot queue 长时间 `STARTING`，已停止；
- `pt-z7v3h4tq`: 2-card retry 缺少 remote `GPU_COUNT` export，失败；
- `pt-ynr58ys8`: 2-card spot retry 后改为 4-card guaranteed，已停止。

提交规则已修正：

```text
GPU_COUNT <= 4: 不传 --quota-type=spot，使用 guaranteed/default resources
GPU_COUNT > 4: 设置 QUOTA_TYPE=spot
```

## 11. 主要结果

训练阶段：

| variant | NTP loss | readback | feature-expert NMI |
|---|---:|---:|---:|
| C0 standard linear | 6.643 | 0.9999 | 0.462 |
| C1 fixed parameter center | 6.641 | 0.9998 | 0.773 |
| C2 trainable center + repulsion | 6.642 | 1.0000 | 0.663 |
| C3 inhibition margin | 6.660 | 1.0000 | 0.685 |
| C4 center + inhibition | 6.658 | 0.9999 | 0.364 |

行为诊断中，expert assignment 与以下变量的 MI 接近：

| factor | mean MI |
|---|---:|
| attention source token | 0.5571 |
| feature | 0.5553 |
| target token | 0.5553 |
| prefix-end token | 0.5553 |
| loss bin | 0.2979 |
| hidden norm bin | 0.2589 |

这个结果的关键边界是：在 `unique_uniform` 数据里，feature、target token、prefix-end token 和 attention source token 基本一一对应，所以 MI 高不能证明 router 使用的是 relation-level feature，而可能只是 token/target shortcut。

Expert utility alignment：

| variant | router selects best expert | selected-best CE gap |
|---|---:|---:|
| C0 | 0.9992 | 0.0000 |
| C1 | 0.2949 | 2.2010 |
| C2 | 0.9996 | 0.0000 |
| C3 | 0.9949 | 0.0002 |
| C4 | 0.9956 | 0.0001 |

C1 是重要负例：它有较高 NMI，但选中 best expert 的比例很低。这说明几何分区或 NMI 本身不能证明 functional specialization。

Boundary direction audit：

| variant | feature-boundary cosine | top shared energy | middle energy | tail energy |
|---|---:|---:|---:|---:|
| C0 | 0.312 | 0.786 | 0.169 | 0.046 |
| C1 | 0.099 | 0.289 | 0.454 | 0.257 |
| C2 | 0.334 | 0.798 | 0.167 | 0.036 |
| C3 | 0.355 | 0.885 | 0.080 | 0.034 |
| C4 | 0.278 | 0.923 | 0.072 | 0.005 |

解释：

- C0/C2/C3/C4 的 router boundary 多数能量在 top shared directions；
- C1 更偏 middle/tail，但 utility 很差；
- C3 的 NMI 和 utility 较强，但 boundary 更偏 top shared direction，不足以证明 feature-direction routing。

## 12. 当前结论

当前不满足进入 Reverse Index 的 Case A。

可以说：

```text
Oracle-MoE 在 unique_uniform synthetic setting 下可以形成 task-utility compatible expert selection；
但这还不是 clean one-feature-one-expert functional specialization。
```

不能说：

```text
C-series router 已经按 relation-level feature 自然分 expert；
也不能说当前结果足以支持 Reverse Index stage。
```

## 13. 和 AI 讨论时最重要的检查问题

1. hard top-1 router 没有 straight-through，是否足以代表我们想测的 router training dynamics？
2. C1 fixed parameter center 用 `W_in` 第一 PCA direction 是否合理？
3. inhibition 是否过强，会不会人为破坏 non-selected experts？
4. boundary alignment 应该在 raw `attention_output` 空间还是 router-normalized 空间报告？
5. 当前 `unique_uniform` 是否足够，还是必须立刻加入 shared-target / crossed-factorial？
6. 如果 C4 提升 utility 但不提升 feature-boundary alignment，是否应进入 Reverse Index，还是先改 hypothesis？
7. 如果 all experts utility 接近，是否说明任务太简单，需要 redesign synthetic task？

## 14. 结果判读原则

只有以下同时成立，才进入 Reverse Index：

```text
feature assignment clean
router boundary feature-aligned
utility matrix diagonal
NTP/readback good
```

如果只是 NMI 高或 center 分开，不足以 claim functional specialization。

## 15. 下一步

下一步应优先做 shortcut-controlled Oracle-MoE：

```text
shared prefix-end token
shared target token
crossed-factorial relation
```

目的不是继续堆 router 设计，而是先排除当前 `unique_uniform` 的 token/target confound。只有在这些控制下仍同时满足 feature assignment、boundary alignment、utility diagonality 和 readback，才进入 Reverse Index。
