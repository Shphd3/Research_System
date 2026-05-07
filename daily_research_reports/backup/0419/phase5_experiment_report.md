# Phase5 实验报告：从单层机制消融到递归 long-tail hierarchical MoE

## 1. 实验目的

`Phase5` 不是重复 `Phase4`，而是在 `Phase4` 已有真实正结果的基础上，把主线继续推进两步：

1. 先在真实 `Qwen3-0.6B` 上回答：

$$
\text{C1 的收益到底来自 split、本身的多 expert 容量，还是 input-dependent routing？}
$$

这对应 `Phase5-C2`。

2. 再在 oracle small-model 上回答：

$$
\text{如果 tail residual 内部仍有结构，递归拆分是否真的优于单层 tail MoE？}
$$

这对应 `Phase5-D1`。

本轮最终要判断的不是“MoE 一定成立”，而是：

$$
\text{当前最稳定的主线到底是 split factorization，还是 learned hierarchical routing。}
$$

---

## 2. 本轮实际执行了什么

本轮按照 `phase5_hierarchical_moe_execution_plan.md` 实际执行了：

- `C2`：真实 `Qwen3-0.6B` 单层机制消融
- `D1`：small-model oracle recursive hierarchy

本轮没有继续执行：

- `D2`：estimated recursive split
- `D3`：真实 Qwen recursive hierarchical block

原因不是遗漏，而是 gate 明确不满足。最终 gate 文件在：

- `results/phase5_full_20260419/phase5_gate_decisions.json`

其中最终判定是：

- `C2` 给出 `routing_value_positive = true`
- `D1` 给出 `recursive_positive = false`
- `D1` 给出 `recursive_factorization_positive = true`
- 因此：
  - `run_d2 = false`
  - `run_d3 = false`

也就是说，本轮结论是：

$$
\text{单层真实模型中 routing 有增益；但递归 learned routing 还没有被当前结果支持。}
$$

---

## 3. 运行组织与清理

### 3.1 目录

本轮正式结果保存在：

- `exp_hierarchical/phase5_recursive_hierarchical_moe/results/phase5_full_20260419/`

报告图片复制到了：

- `exp_hierarchical/phase5_recursive_hierarchical_moe/docs/figures/`

### 3.2 smoke

开发阶段做过极小 smoke，用于验证脚本可运行：

- `C2` smoke
- `D1` smoke

这些临时结果都已删除，没有纳入正式结论。

### 3.3 正式运行命令

正式运行的命令是：

```bash
python exp_hierarchical/phase5_recursive_hierarchical_moe/scripts/run_phase5_recursive_small_models.py \
  --output-dir exp_hierarchical/phase5_recursive_hierarchical_moe/results/phase5_full_20260419/d1_recursive_small \
  --device cuda:1
```

```bash
python exp_hierarchical/phase5_recursive_hierarchical_moe/scripts/run_phase5_c2_qwen.py \
  --output-dir exp_hierarchical/phase5_recursive_hierarchical_moe/results/phase5_full_20260419/c2_real_qwen \
  --device cuda:0 \
  --seeds 20260418
```

```bash
python exp_hierarchical/phase5_recursive_hierarchical_moe/scripts/run_phase5_c2_qwen.py \
  --output-dir exp_hierarchical/phase5_recursive_hierarchical_moe/results/phase5_full_20260419/c2_real_qwen \
  --device cuda:1 \
  --seeds 20260419
```

`C2` 在正式执行中一开始是串行双 seed，后来发现 wall-clock 明显过长，因此补上了“已完成 config 自动跳过”的恢复逻辑，然后拆成两个 seed shard 并行完成。这个改动只影响执行效率，不影响最终结果口径。

---

## 4. Phase5-C2：真实 Qwen 单层机制消融

## 4.1 目的

`C1` 已经证明：

$$
\text{hier\_moe\_tail\_uniform} > \text{baseline\_ffn}, \text{flat\_moe\_raw\_uniform}
$$

但 `C1` 没有回答收益到底来自哪一层机制。`C2` 的目标就是把下面三件事拆开：

1. split 本身是否足够
2. 多 expert 容量是否足够
3. input-dependent routing 是否有额外价值

## 4.2 固定设置

- 模型：`Qwen3-0.6B`
- 层位：`layer = 8`
- projector rank：`k = 16`
- freeze mode：`frozen`
- 数据：`DCLM + WoS`
- 混合比例：`DCLM : WoS = 4 : 1`
- 训练步数：`500`
- 评估间隔：`100`
- seeds：`20260418, 20260419`
- batch size：`1`
- eval batch size：`2`
- `max_length = 256`
- 优化器：`AdamW`
- 不扫 `WD-only`
- 不加 domain CE

projector 仍按 `Phase4` 的真实协议重新估计。对每个 seed：

$$
P_t = I - V_{16}V_{16}^\top
$$

其中 `V_{16}` 来自 `layer 8` 上协方差矩阵的前 `16` 个主方向。

## 4.3 对照组

### `G0: baseline_ffn`

原始 FFN 单层训练。

### `G1: flat_moe_raw_uniform`

$$
u = \sum_i g_i(x) E_i(x)
$$

router 和 experts 都看 full hidden。

### `G2: split_dense_tail_uniform`

$$
u_c = E_c(x)
$$

$$
u_t = E_t(P_t(x-\mu))
$$

$$
h_{\text{out}} = h_{\text{in}} + u_c + u_t
$$

没有 routing。

### `G3: uniform_expert_mixture_tail`

$$
u_t = \frac{1}{N}\sum_i E_i(P_t(x-\mu))
$$

有多个 expert，但没有输入相关 routing。

### `G4: hier_moe_tail_uniform`

$$
u_t = \sum_i g_i(P_t(x-\mu)) E_i(P_t(x-\mu))
$$

这是 `Phase4 C1` 中给出正结果的结构。

## 4.4 实际训练步骤

对每个 seed，实际步骤是：

1. 加载 `Qwen3-0.6B`
2. 读取 WoS train/test 与 DCLM binary shard
3. 取 WoS 协方差样本、WoS train 样本、WoS test 样本、DCLM train/eval 样本
4. 在 `layer 8` 的 `post_attention_layernorm` 输出上估计 projector
5. 对 5 个 config 逐个替换第 8 层 FFN
6. 冻结除替换块外的所有 backbone 参数
7. 按 `DCLM:WoS = 4:1` 交替取 batch
8. 训练 `500` steps
9. 每 `100` steps 评估一次
10. 保存每个 config 的：
   - `history.csv`
   - rare-token PPL 曲线
   - 最终汇总指标

## 4.5 指标

### 主指标

- `DCLM PPL`
- `WoS PPL`
- `WoS rare-token PPL`

### 机制指标

- `router_purity`
- `router_nmi`
- `router_load_entropy`
- `effective_expert_usage`
- `common_branch_norm`
- `tail_branch_norm`
- `common_tail_grad_ratio`

这里最重要的判读指标是：

$$
\text{WoS rare-token PPL}
$$

因为这最直接对应“tail/rare token 是否被改善”。

## 4.6 C2 结果

双 seed 聚合结果如下：

| Config | DCLM PPL | WoS PPL | WoS rare-token PPL |
|---|---:|---:|---:|
| `hier_moe_tail_uniform` | `32.7218 ± 1.2499` | `16.9412 ± 0.0703` | `437.7246 ± 65.3381` |
| `split_dense_tail_uniform` | `33.2727 ± 1.2902` | `17.1691 ± 0.0409` | `455.6466 ± 71.3311` |
| `uniform_expert_mixture_tail` | `33.3204 ± 1.2368` | `17.1910 ± 0.0726` | `455.8094 ± 68.2142` |
| `baseline_ffn` | `33.3800 ± 1.2176` | `17.2250 ± 0.0730` | `457.6520 ± 67.5661` |
| `flat_moe_raw_uniform` | `33.5738 ± 1.2598` | `17.3475 ± 0.0466` | `465.3319 ± 72.1181` |

配图：

![C2 Summary](./figures/c2_rare_token_summary_merged.png)

## 4.7 C2 判读

`C2` 的结论非常清楚：

### 结论 1：flat raw routing 仍然最差

$$
\text{flat\_moe\_raw\_uniform}
>
\text{baseline\_ffn}
$$

这里“>`”表示 PPL 更差。

这说明真实模型里 flat raw routing 不是正方向。

### 结论 2：split 本身有收益

$$
\text{split\_dense\_tail\_uniform}

<

\text{baseline\_ffn}
$$

说明 common/tail factorization 本身是有效的。

### 结论 3：纯容量不是全部解释

`uniform_expert_mixture_tail` 也比 baseline 略好，但它没有超过 `split_dense_tail_uniform`，也没有接近 `hier_moe_tail_uniform` 的最好值。

### 结论 4：routing 有额外价值

最关键的比较是：

$$
\text{hier\_moe\_tail\_uniform}

<

\text{split\_dense\_tail\_uniform}
$$

以及：

$$
\text{hier\_moe\_tail\_uniform}

<

\text{uniform\_expert\_mixture\_tail}
$$

在 rare-token PPL 上，两者差距分别是：

- `hier - split = -17.9220`
- `hier - uniform_mix = -18.0848`

因此 `C2` 的 gate 判断为：

$$
\text{routing\_value\_positive} = \text{true}
$$

也就是说，单层真实模型里并不是“只有 split”，input-dependent tail routing 已经开始给出额外收益。

但需要同时保留边界：

- `router_purity / router_nmi` 仍然很低
- 所以这里支持的是“routing 有 LM 价值”
- 还不支持“已经形成强离散语义 expert specialization”

---

## 5. Phase5-D1：small-model oracle recursive hierarchy

## 5.1 目的

`D1` 是本轮新增的核心实验，用来回答：

$$
\text{在 common/tail 分开后，tail 内部继续递归拆分，是否优于单层 tail MoE？}
$$

## 5.2 数据生成

这轮数据显式构造了二级 latent structure：

$$
z = (z_1, z_2)
$$

其中：

- $z_1$：coarse domain
- $z_2$：fine subdomain

固定设置：

- `num_coarse_domains = 4`
- `num_fine_per_coarse = 2`
- `common_vocab_size = 256`
- `coarse_tail_vocab_size = 64`
- `fine_tail_vocab_size = 32`
- `seq_len = 128`

next-token 分布为：

$$
p(x_{t+1}\mid x_t,z_1,z_2)
=
(1-\rho_1-\rho_2)T_{\mathrm{common}}(\cdot\mid x_t)
+
\rho_1 T_{z_1}^{\mathrm{coarse}}(\cdot\mid x_t)
+
\rho_2 T_{z_1,z_2}^{\mathrm{fine}}(\cdot\mid x_t)
$$

扫描范围：

- $\rho_1 \in \{0.1, 0.2\}$
- $\rho_2 \in \{0.02, 0.05, 0.1\}$

`rare-fine-tail` 定义为每个 fine tail 词表中最低频的末 `25%` token。

## 5.3 Oracle 表示拆分

block 输入被写成：

$$
x = [x_c; x_{t1}; x_{t2}]
$$

其中：

- $x_c$：global common
- $x_{t1}$：coarse tail
- $x_{t2}$：fine tail

本轮固定：

- `d_model = 128`
- `d_common = 64`
- `d_tail1 = 32`
- `d_tail2 = 32`

## 5.4 对照组

### `R0: dense_ffn`

普通 dense FFN。

### `R1: flat_raw_moe`

router 和 experts 都看 full hidden。

### `R2: level1_split_dense`

只做一级 split，不做 routing。

### `R3: level1_hier_moe`

一级 hierarchical MoE。

### `R4: recursive_split_dense`

递归 split，但不做 learned routing：

$$
u = E_c^{(0)}(x) + E_c^{(1)}(x_{t1}) + E_t^{(2)}(x_{t2})
$$

### `R5: recursive_hier_moe`

完整二级 learned hierarchical MoE。

### `R6: oracle_recursive_router_upper_bound`

直接使用真实 $z_1, z_2$ 做 oracle routing 的上界。

## 5.5 参数预算对齐

本轮 block 内参数预算严格控制在 `2%` 以内。最终预算清单是：

- dense target：`65536`
- `R1 flat_raw_moe`：`65024`
- `R2 level1_split_dense`：`65536`
- `R3 level1_hier_moe`：`65792`
- `R4 recursive_split_dense`：`65536`
- `R5/R6 recursive_hier`：`65408`

对应宽度搜索结果是：

- `R1 flat_expert_width = 63`
- `R2 level1_split_common_width = 64`
- `R2 level1_split_tail_width = 256`
- `R3 level1_hier_common_width = 16`
- `R3 level1_hier_expert_width = 80`
- `R4 recursive_split_global_width = 16`
- `R4 recursive_split_local_width = 128`
- `R4 recursive_split_tail_width = 256`
- `R5/R6 recursive_hier_global_width = 24`
- `R5/R6 recursive_hier_local_width = 12`
- `R5/R6 recursive_hier_expert_width = 40`

## 5.6 训练设置

- one-block causal LM
- `num_heads = 4`
- `train_sequences = 4096`
- `val_sequences = 1024`
- `batch_size = 128`
- `train_steps = 500`
- `eval_every = 100`
- `learning_rate = 3e-4`
- `beta_lb = 0.01`
- seeds：`20260418, 20260419, 20260420`

## 5.7 实际训练步骤

对每个 `seed × rho1 × rho2 × config`，实际步骤是：

1. 生成一份训练 synthetic dataset
2. 生成一份验证 synthetic dataset
3. 构建对应 block 结构
4. 按预算计划设置宽度
5. 训练 `500` steps
6. 每 `100` steps 评估：
   - overall PPL
   - common-token PPL
   - coarse-tail PPL
   - fine-tail PPL
   - rare-fine-tail PPL
   - coarse/fine/joint NMI
   - load entropy
7. 保存每个 run 的：
   - `history.csv`
   - `rare_fine_tail_ppl.png`

整轮正式 `D1` 实际跑完了：

$$
7 \text{ configs} \times 2 \text{ rho1} \times 3 \text{ rho2} \times 3 \text{ seeds}
= 126 \text{ runs}
$$

## 5.8 D1 结果

最佳区域出现在：

$$
\rho_1 = 0.2,\quad \rho_2 = 0.1
$$

在这个设置下，关键结果是：

| Config | rare-fine-tail PPL |
|---|---:|
| `R2_level1_split_dense` | `8832.04 ± 623.58` |
| `R4_recursive_split_dense` | `8941.52 ± 661.07` |
| `R3_level1_hier_moe` | `8995.21 ± 402.54` |
| `R5_recursive_hier_moe` | `9205.12 ± 732.84` |
| `R6_oracle_recursive_router_upper_bound` | `1040.39 ± 84.32` |

配图：

![D1 Summary](./figures/d1_best_per_config.png)

## 5.9 D1 判读

### 结论 1：递归 learned routing 没有通过

最终 gate 文件给出的结论是：

$$
\text{recursive\_positive} = \text{false}
$$

因为：

$$
R5_{\text{best}} = 9205.12
>
R3_{\text{best}} = 8995.21
$$

也就是说，当前 learned recursive hierarchy 没有优于一级 hierarchical MoE。

### 结论 2：递归 factorization 有弱正信号

$$
\text{recursive\_factorization\_positive} = \text{true}
$$

因为：

$$
R4_{\text{best}} = 8941.52
<
R3_{\text{best}} = 8995.21
$$

说明：

> tail 内部继续分层，在“纯 factorization”层面有一定价值。

### 结论 3：router 学习是当前瓶颈，不是结构上界

oracle 上界非常强：

$$
R6_{\text{best}} = 1040.39
\ll
R5_{\text{best}} = 9205.12
$$

这说明不是“递归结构没用”，而是：

$$
\text{oracle recursive routing 有巨大潜力，但 learned router 还没学出来。}
$$

### 结论 4：当前最稳的是 split，不是 recursive MoE

更准确地说，本轮 `D1` 支持：

- 一级 split 有效
- 递归 factorization 有一点点增益
- learned recursive MoE 目前没有压过一级 hierarchical

---

## 6. 为什么 D2 / D3 本轮没有执行

### 6.1 D2

`D2` 的前提是：

$$
\text{D1 through}
$$

也就是要先证明 oracle recursive hierarchy 自身成立。  
但本轮 `D1` 给出的结果是：

$$
\text{recursive\_positive} = \text{false}
$$

因此本轮不进入 `D2`。

### 6.2 D3

`D3` 的前提是同时满足：

1. `C2` 说明 routing 不是纯噪声
2. `D1` 或 `D2` 说明 recursive hierarchy 成立

本轮只有第一条满足：

$$
\text{C2 routing\_value\_positive} = \text{true}
$$

但第二条不满足：

$$
\text{D1 recursive\_positive} = \text{false}
$$

因此本轮不进入真实 Qwen recursive hierarchical block。

---

## 7. 本轮总结合论

`Phase5` 的核心结论可以压缩成三句：

### 结论 A

在真实 `Qwen3-0.6B` 单层 block replacement 中，机制消融已经支持：

$$
\text{hier\_moe\_tail\_uniform}
<
\text{split\_dense\_tail\_uniform}
<
\text{baseline\_ffn}
<
\text{flat\_moe\_raw\_uniform}
$$

这说明：

- split 仍然是主要收益源
- 但 routing 现在已经开始给出额外增益

### 结论 B

在 recursive small-model 中，当前最稳的结论不是“recursive learned hierarchy 已成立”，而是：

$$
\text{recursive factorization 有弱正信号，learned recursive routing 还没学稳。}
$$

### 结论 C

oracle recursive upper bound 非常强，因此下一轮最值得研究的不是“还要不要继续分层”，而是：

$$
\text{为什么 recursive router 学不出来，以及怎样让 router 学到 LM-relevant recursive partition。}
$$

---

## 8. 下一步建议

本轮之后，最合理的下一步不是直接上 `D3`，而是先做一轮新的小模型修订：

1. 保留 `C2` 的单层真实结论：
   - 单层真实模型中 routing 有价值
2. 保留 `D1` 的递归边界：
   - recursive factorization 有信号
   - recursive learned router 还不行
3. 下一轮优先做：
   - 改进 recursive router objective
   - 改进 level-2 router 的学习稳定性
   - 再决定是否上 estimated recursive split 或真实 recursive Qwen

换句话说，当前主线已经从：

> 只要多上 MoE expert 就能救 tail

修正为：

> split-first 是稳定主线；单层真实 routing 已经出现正信号；但 long-tail 继续递归拆分时，结构上界存在、learned recursive routing 还未成立。
