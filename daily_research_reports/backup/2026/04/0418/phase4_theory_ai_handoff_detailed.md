# Phase4 完整结果交接稿（供理论 AI 分析）

## 0. 这份文档的用途

这是一份面向理论分析的 `Phase4` 完整实验交接稿。目标是把本轮实验的：

- 研究目标
- 实现方式
- 每个实验的具体步骤
- 每个实验实际运行命令
- 每个实验的结果
- 每个实验的判读
- 当前主线推进到什么位置

全部放进一个单独文档中，尽量做到“只上传这一份文件，理论 AI 就能完整理解本轮 Phase4 的输入、过程、输出和结论”。

如果理论 AI 还需要原始结果表，可以额外上传这些文件名：

- `phase4_small_models_gate.json`
- `small_models_key_summary.md`
- `prep_scan_results.csv`
- `c1_frozen_summary.csv`

但只从理论分析角度看，这份文档已经尽量自洽。

---

## 1. 先给结论摘要

本轮 `Phase4` 的实验已经全部完成。

需要先给出最重要的五条结论：

1. `A1` 支持：`split-first` 优于 `flat raw route`。
2. 但 `A1` 同时表明：当前小模型中主要收益来自 `split`，不是 routing 本身。
3. `A2` 不支持“mild load balance regularizer 是必要条件”。
4. `B1` 没有通过 gate：estimated projector 没能稳定优于 matched-dim `random_projected` 控制组。
5. `C1` 在真实 `Qwen3-0.6B` 上给出明确正信号：`hier_moe_tail_uniform` 在两个 seed 上都优于 `baseline_ffn` 和 `flat_moe_raw_uniform`。

因此，这轮最关键的推进不是“所有子命题都成立”，而是：

$$
\text{Hierarchical tail-conditioned block} > \text{flat raw MoE block}
$$

已经在真实模型里开始成立。

但是：

- projector 主线这轮没有成立
- `WD-only` 的额外收益这轮没有成立
- router 的 `purity / NMI` 仍然很低，因此当前 gain 更像来自 factorized residual structure，而不是强离散 specialization

---

## 2. 本轮实验到底做了哪些事

本轮 `Phase4` 总共做了 5 个实验块：

- `A0`：infra sanity
- `A1`：oracle split 的真实 block 主实验
- `A2`：LB ablation
- `B1`：estimated split 替代 oracle split
- `C1`：回到真实 `Qwen3-0.6B` 的单层 block replacement

### 2.1 `A* / B* / C*` 这套命名分别代表什么

这轮 `Phase4` 里，`A* / B* / C*` 不是随意命名，而是按“主线中的功能位置”来分组。

- `A*`：small-model 上的结构本体验证组
- `B*`：projector 替代 oracle split 的验证组
- `C*`：回到真实 pretrained LLM 的 block-level 最小闭环组

更具体地说：

- `A0`
  - 表示 `A` 组里的第 `0` 个实验
  - 作用是 infra sanity，不负责给科学结论
  - 它验证的是：数据生成、block 实现、指标统计、参数预算对齐、结果落盘是否都正常
- `A1`
  - 表示 `A` 组里的主实验
  - 作用是直接比较 `Dense FFN / Flat MoE / Split Dense / Hierarchical MoE`
  - 它回答的是：在 oracle split 已知时，真实 block 本体是否支持“先 split 再 route”
- `A2`
  - 表示 `A` 组里的 load-balance ablation
  - 作用是检查 mild LB 是否必要
  - 它回答的是：在 tail router 输入已经相对净化后，`with_lb` 和 `no_lb` 的差异是什么

- `B1`
  - 表示 `B` 组里的第 `1` 个实验
  - `B` 组专门负责 projector 问题
  - 它回答的是：把 oracle split 换成估计得到的 $$P_t(x-\mu)$$ 之后，Hierarchical block 的收益是否还成立
  - 这组里还专门保留了两种 `projector_source`：
    - `dense`
    - `flat`

- `C1`
  - 表示 `C` 组里的第 `1` 个实验
  - `C` 组专门负责“回到真实大模型”
  - 它回答的是：在真实 pretrained `Qwen3-0.6B` 上，做单层 block replacement 时，Hierarchical tail-conditioned block 是否优于 `baseline_ffn` 和 `flat_moe_raw_uniform`

所以，这套命名的逻辑可以压缩成一句话：

$$
A^\ast = \text{小模型结构验证}, \quad
B^\ast = \text{projector 验证}, \quad
C^\ast = \text{真实模型闭环}
$$

### 2.2 执行顺序

实际执行顺序是：

1. 先实现 `Phase4` 专用脚本
2. 做最小 smoke 验证
3. 删除所有 smoke / `_tmp` 目录
4. 正式运行 `A0`
5. 正式运行 `A1`
6. 从 `A1` 里选出 `best_rho` 与 `best_gamma_ratio`
7. 正式运行 `A2`
8. 正式运行 `B1`
9. 正式运行 `Qwen3-0.6B` 的 prep scan
10. 正式运行 `C1(frozen)`
11. 汇总结果并写正式报告

### 2.3 关于 smoke

为了保证 `Phase4` 脚本本身可运行，开发过程中确实做过最小 smoke：

- small-model smoke
- real-model `C1` smoke

但这些 smoke 结果都已经删除，不纳入任何正式结论。

也就是说，本轮最终保留的结果目录中：

- 没有 `_tmp`
- 没有 `smoke`

保留下来的只有正式结果。

---

## 3. 脚本、目录、结果文件

### 3.1 主要脚本文件

本轮使用的核心脚本有 3 个：

1. `run_phase4_small_models.py`
   - 负责 `A0 / A1 / A2 / B1`
2. `run_phase4_qwen_block.py`
   - 负责 `prep scan / C1`
3. `merge_phase4_small_shards.py`
   - 负责把 small-model 的分片结果合并

### 3.2 主要结果目录

正式结果都在：

- `phase4_full_20260418/`

其中主要子目录是：

- `small_base/`
- `small_shard_a/`
- `small_shard_b/`
- `small_merged/`
- `real_model/`

### 3.3 为什么有 shard

因为 `A1 / A2 / B1` 使用了多个 seed，而且可以并行运行，所以实际把 small-model 正式实验分成了两个 shard：

- `small_shard_a`：跑 `seed = 20260418, 20260419`
- `small_shard_b`：跑 `seed = 20260420`

最后再合并成：

- `small_merged`

---

## 4. small-model 共有设定

### 4.1 synthetic causal LM 的生成方式

small-model 使用 synthetic causal LM，不是分类，不是 regression。

词表写为：

$$
\mathcal V = \mathcal V_{\mathrm{common}} \cup \bigcup_{m=1}^{M}\mathcal V_m
$$

其中：

- $\mathcal V_{\mathrm{common}}$：shared common token 词表
- $\mathcal V_m$：第 $m$ 个 latent domain 的 tail token 词表
- $M = 4$：latent domain 数量

本轮固定：

- `common_vocab_size = 256`
- 每个 domain 的 `tail_vocab_size = 64`
- `num_domains = 4`

因此总词表大小为：

$$
|\mathcal V| = 256 + 4 \times 64 = 512
$$

### 4.2 序列生成过程

每条序列先采样 latent domain：

$$
z \sim \mathrm{Unif}\{1,2,3,4\}
$$

然后按长度 `seq_len = 128` 生成 token。

对每个位置，next-token 分布写成：

$$
p(x_{t+1}\mid x_t,z)
=
(1-\rho)\,T_{\mathrm{common}}(\cdot \mid x_t)
+
\rho\,T_z(\cdot \mid x_t)
$$

其中：

- $x_t$：当前位置 token
- $x_{t+1}$：下一个 token
- $T_{\mathrm{common}}$：shared common 转移机制
- $T_z$：第 $z$ 个 domain 的 tail 转移机制
- $\rho$：tail 触发概率

本轮扫描：

$$
\rho \in \{0.05, 0.1, 0.2\}
$$

### 4.3 rare-tail 的定义

每个 domain 的 tail 词表内部按 Zipf 频率排序。

定义该 domain 的：

- 频率最低的末 `25%` token 集合

为 `rare-tail`。

### 4.4 small-model 共享训练设定

small-model 统一用：

- `d_model = 128`
- `d_common = 96`
- `d_tail = 32`
- `num_heads = 4`
- `num_experts = 4`
- `top_k = 1`
- `train_sequences = 4096`
- `val_sequences = 1024`
- `batch_size = 128`
- `train_steps = 500`
- `eval_every = 100`
- `learning_rate = 3e-4`
- `beta_lb = 0.01`
- `gamma_common = 0.1`
- `gamma_ratios = {1.0, 0.3, 0.1}`
- seeds：`20260418, 20260419, 20260420`

### 4.5 参数预算对齐

脚本里用 deterministic width search 对齐 block 内参数预算。

最终预算计划是：

- `Dense FFN`
  - `dense_width = 256`
  - `dense_params = 65536`
- `Flat MoE`
  - `flat_expert_width = 63`
  - `flat_params = 65024`
- `Split Dense`
  - `split_common_width = 96`
  - `split_tail_width = 256`
  - `split_params = 65536`
- `Hierarchical MoE`
  - `hier_common_width = 16`
  - `hier_expert_width = 96`
  - `hier_params = 65664`

这些都在 `2%` 预算容忍度内。

---

## 5. `A0`：infra sanity

### 5.1 `A0` 的目的

`A0` 不是为了最终科学结论，而是为了确认：

1. synthetic data 生成正确
2. block 接口跑得通
3. token 分桶指标能算
4. router 指标能算
5. 参数预算对齐逻辑正常

### 5.2 `A0` 实际运行步骤

`A0` 的具体步骤如下：

1. 调用 `search_budget_plan(...)`
2. 在结果目录里写出 `budget_plan.json`
3. 固定 `rho = 0.1`
4. 用 `seed = 20260418` 生成 train / val synthetic 数据
5. 依次训练 5 个 config：
   - `G0_dense`
   - `G1_flat`
   - `G2_split_dense`
   - `G3_hier_uniform`
   - `G4_hier_wdonly`
6. 每个 config 训练 `500` steps
7. 每 `100` steps 评估一次
8. 保存：
   - `best_model.pt`
   - `history.csv`
   - `rare_tail_ppl.png`
9. 聚合成 `a0_results.csv`

### 5.3 `A0` 实际命令

```bash
python run_phase4_small_models.py \
  --stage a0 \
  --output-dir phase4_full_20260418/small_base \
  --device cuda:0
```

### 5.4 `A0` 结果

`A0` 单次正式结果如下：

- `G0_dense`
  - `overall_ppl = 295.41`
  - `tail_ppl = 350.90`
  - `rare_tail_ppl = 32884.02`
- `G1_flat`
  - `overall_ppl = 293.01`
  - `tail_ppl = 316.50`
  - `rare_tail_ppl = 30924.29`
  - `router_purity = 0.3486`
  - `router_nmi = 0.0446`
- `G2_split_dense`
  - `overall_ppl = 286.22`
  - `tail_ppl = 239.58`
  - `rare_tail_ppl = 25977.12`
- `G3_hier_uniform`
  - `overall_ppl = 294.24`
  - `tail_ppl = 341.89`
  - `rare_tail_ppl = 32578.86`
  - `router_purity = 0.3247`
  - `router_nmi = 0.0732`
- `G4_hier_wdonly`
  - `overall_ppl = 293.49`
  - `tail_ppl = 321.91`
  - `rare_tail_ppl = 31180.66`
  - `router_purity = 0.3900`
  - `router_nmi = 0.0729`

### 5.5 `A0` 判读

`A0` 已经出现一个很清楚的方向：

- `split_dense` 最好
- flat routing 没有自动赢

因此，即使在 infra sanity 阶段，也已经能看到：

$$
\text{split} \text{ 可能是首要收益来源}
$$

---

## 6. `A1`：oracle split 的真实 block 主实验

### 6.1 `A1` 的目的

`A1` 直接测试：

1. oracle split 的真实 block 本体是否优于 flat raw route
2. `WD-only` 是否在 oracle hierarchical block 下带来额外收益

### 6.2 `A1` 的 5 类 block

`A1` 比较的 block 为：

- `G0_dense`
- `G1_flat`
- `G2_split_dense`
- `G3_hier_uniform`
- `G4_hier_wdonly`

其中 oracle split 写为：

$$
x = [x_c; x_t]
$$

### 6.3 `A1` 每个 seed 的具体步骤

对每个 seed，脚本做下面这些事：

1. 对每个 $\rho \in \{0.05, 0.1, 0.2\}$：
2. 生成该 `rho` 下的 train / val synthetic 数据
3. 训练一次：
   - `G0_dense`
   - `G1_flat`
   - `G2_split_dense`
   - `G3_hier_uniform`
4. 对 `G4_hier_wdonly` 再分别训练三次：
   - `gamma_ratio = 1.0`
   - `gamma_ratio = 0.3`
   - `gamma_ratio = 0.1`
5. 每个 run：
   - 训练 `500` steps
   - 每 `100` steps 评估一次
   - 保存 checkpoint/history/plot
6. 最后把所有行写成 `a1_results_all.csv`

### 6.4 `A1` 实际并行方式

`A1` 正式并行成两个 shard：

- shard A：
  - seeds = `20260418, 20260419`
- shard B：
  - seeds = `20260420`

因此：

- shard A 实际训练 `42` 个 run
- shard B 实际训练 `21` 个 run

### 6.5 `A1` 实际命令

```bash
python run_phase4_small_models.py \
  --stage a1 \
  --output-dir phase4_full_20260418/small_shard_a \
  --device cuda:0 \
  --seeds 20260418,20260419 \
  --train-steps 500 \
  --eval-every 100 \
  --batch-size 128
```

```bash
python run_phase4_small_models.py \
  --stage a1 \
  --output-dir phase4_full_20260418/small_shard_b \
  --device cuda:1 \
  --seeds 20260420 \
  --train-steps 500 \
  --eval-every 100 \
  --batch-size 128
```

### 6.6 `A1` 聚合结果

按 `config` 聚合，`rare_tail_ppl` 的平均排序为：

- `G2_split_dense = 30552.31 ± 23197.90`
- `G3_hier_uniform = 31358.65 ± 23652.04`
- `G4_hier_wdonly = 31365.80 ± 22757.64`
- `G0_dense = 31475.71 ± 22931.53`
- `G1_flat = 31995.61 ± 24317.11`

同时，按 `G4_hier_wdonly` 的脚本协议选出的 gate 是：

- `best_rho = 0.2`
- `best_gamma_ratio = 0.1`

### 6.7 一个实现细节：`best_rho` 与 `best_gamma_ratio` 的选法

这里有一个非常重要的实现细节，理论 AI 需要知道：

脚本并不是直接选“全局最优的 joint pair $(\rho, \gamma)$”，而是分两步边际选择：

1. 先按 `G4_hier_wdonly` 在不同 `rho` 上聚合 `rare_tail_ppl`，选 `best_rho`
2. 再按 `G4_hier_wdonly` 在不同 `gamma_ratio` 上聚合 `rare_tail_ppl`，选 `best_gamma_ratio`

所以：

- 脚本最终选出的是 `(best_rho = 0.2, best_gamma_ratio = 0.1)`
- 但从单个 cell 看，最优的 joint `G4` 其实是：

$$
(\rho = 0.2,\ \gamma = 1.0)
$$

对应：

$$
\text{rare_tail_ppl} = 6973.68
$$

而不是 `(0.2, 0.1)`。

这点需要单独记下来，因为它会影响后续 `A2/B1` 的解释。

### 6.8 `A1` 判读

`A1` 的判读非常清楚：

1. `G3 > G1` 成立
2. `G4 > G1` 也成立
3. 但 `G2 >= G3/G4` 也成立

因此：

- “先 split 再 route”优于 `flat raw route`
- 但当前收益主要来自 split，而不是 routing 本身
- `WD-only` 在 oracle hierarchical block 下没有形成额外增益

---

## 7. `A2`：LB ablation

### 7.1 `A2` 的目的

`A2` 测试：

在当前最优 `rho / gamma` 设定附近，mild load balance regularizer 是否仍然必要。

### 7.2 `A2` 的输入

`A2` 固定使用：

- `best_rho = 0.2`
- `best_gamma_ratio = 0.1`

并只比较：

- `G3_hier_uniform + with_lb`
- `G3_hier_uniform + no_lb`
- `G4_hier_wdonly + with_lb`
- `G4_hier_wdonly + no_lb`

其中：

- `with_lb`：`beta_lb = 0.01`
- `no_lb`：`beta_lb = 0`

### 7.3 `A2` 具体步骤

对每个 seed：

1. 用 `rho = 0.2` 重新生成 synthetic 数据
2. 对 `beta_lb = 0.01 / 0.0` 两种条件分别训练
3. 对 `G3 / G4` 两种 block 分别训练
4. 每个 run：
   - 训练 `500` steps
   - 每 `100` steps 评估
   - 保存 history
5. 最后写出 `a2_results_all.csv`

### 7.4 `A2` 实际命令

```bash
python run_phase4_small_models.py \
  --stage a2 \
  --output-dir phase4_full_20260418/small_shard_a \
  --device cuda:0 \
  --seeds 20260418,20260419 \
  --train-steps 500 \
  --eval-every 100 \
  --batch-size 128 \
  --best-rho 0.2 \
  --best-gamma-ratio 0.1
```

```bash
python run_phase4_small_models.py \
  --stage a2 \
  --output-dir phase4_full_20260418/small_shard_b \
  --device cuda:1 \
  --seeds 20260420 \
  --train-steps 500 \
  --eval-every 100 \
  --batch-size 128 \
  --best-rho 0.2 \
  --best-gamma-ratio 0.1
```

### 7.5 `A2` 结果

- `G3_hier_uniform + no_lb`
  - `rare_tail_ppl = 6803.53 ± 148.75`
  - `router_purity = 0.4639 ± 0.1830`
  - `router_nmi = 0.3009 ± 0.2331`
- `G3_hier_uniform + with_lb`
  - `rare_tail_ppl = 6965.59 ± 418.43`
  - `router_purity = 0.5381 ± 0.0211`
  - `router_nmi = 0.2764 ± 0.0898`
- `G4_hier_wdonly + no_lb`
  - `rare_tail_ppl = 6989.33 ± 92.77`
  - `router_purity = 0.5029 ± 0.0910`
  - `router_nmi = 0.3688 ± 0.0365`
- `G4_hier_wdonly + with_lb`
  - `rare_tail_ppl = 7036.46 ± 117.45`
  - `router_purity = 0.4595 ± 0.0790`
  - `router_nmi = 0.2173 ± 0.0912`

### 7.6 `A2` 判读

`A2` 不支持“LB 是必要的”。

在这版 synthetic causal LM 上：

- `no_lb` 并没有更差
- 有时甚至更好

因此，本轮最多只能说：

- `Switch-style LB` 是一个可选默认正则
- 不能说当前 hierarchical block 没有 `LB` 就不工作

---

## 8. `B1`：estimated split 替代 oracle split

### 8.1 `B1` 的目的

`B1` 测试：

$$
x_t = (I - V_kV_k^\top)(x - \mu)
$$

得到的 projector，是否足够替代 oracle split。

### 8.2 `B1` 保留的 projector source

这轮 `B1` 明确保留了两种 projector 来源：

- `projector_source = dense`
- `projector_source = flat`

具体含义是：

- `dense`：从 `G0_dense` 的 block hidden 估计 projector
- `flat`：从 `G1_flat` 的 block hidden 估计 projector

### 8.3 `B1` 每个 seed 的具体步骤

对每个 seed：

1. 先固定使用 `best_rho = 0.2`
2. 分别载入：
   - `G0_dense` 的 `best_model.pt`
   - `G1_flat` 的 `best_model.pt`
3. 对每个 `projector_source`：
   1. 在 train set 上收集 block inputs
   2. 估计 hidden 均值：

      $$
      \mu = \mathbb E[x]
      $$

   3. 估计协方差：

      $$
      \Sigma = \mathbb E[(x-\mu)(x-\mu)^\top]
      $$

   4. 取 top-$k$ 主方向，$k \in \{8,16,32\}$
   5. 构造：

      $$
      P_t = I - V_kV_k^\top
      $$

4. 对每个 `k`：
   - 训练 `pca_hier_uniform`
   - 训练 `pca_hier_wdonly`
   - 训练 matched-dim `random_projected_hier`
5. 额外把 `A1` 中同 seed、同 `best_rho`、同 `best_gamma_ratio` 的：
   - `G3_hier_uniform`
   - `G4_hier_wdonly`

   作为 oracle 行写入 `B1` 汇总表

### 8.4 `B1` 每个 seed 的训练数

对每个 seed，`B1` 实际训练：

- `2` 个 source
- `3` 个 `k`
- 每个 `k` 下：
  - `pca_hier_uniform`
  - `pca_hier_wdonly`
  - `random_projected_hier`

所以每个 seed 是：

$$
2 \times 3 \times 3 = 18
$$

个真实训练 run。

此外，再从 `A1` 附加 `2` 条 oracle 行，但 oracle 行不重新训练。

### 8.5 `B1` 实际命令

```bash
python run_phase4_small_models.py \
  --stage b1 \
  --output-dir phase4_full_20260418/small_shard_a \
  --device cuda:0 \
  --seeds 20260418,20260419 \
  --train-steps 500 \
  --eval-every 100 \
  --batch-size 128 \
  --best-rho 0.2 \
  --best-gamma-ratio 0.1
```

```bash
python run_phase4_small_models.py \
  --stage b1 \
  --output-dir phase4_full_20260418/small_shard_b \
  --device cuda:1 \
  --seeds 20260420 \
  --train-steps 500 \
  --eval-every 100 \
  --batch-size 128 \
  --best-rho 0.2 \
  --best-gamma-ratio 0.1
```

### 8.6 `B1` 的 gate 定义

脚本里 `b1_pass` 的判定是：

$$
\text{b1\_pass}
=

\big[
\text{best\_pca} \le 1.10 \times \text{best\_oracle}
\big]
\land
\big[
\text{best\_pca} < 0.98 \times \text{best\_random}
\big]
$$

即：

1. 最优 `pca` 至少要接近 `oracle`
2. 最优 `pca` 还必须显著优于最优 `random`

### 8.7 `B1` 结果

`B1` 的最终 gate 为：

- `b1_pass = false`
- `best_oracle_rare_tail_ppl = 6981.46`
- `best_pca_rare_tail_ppl = 6595.14`
- `best_random_rare_tail_ppl = 6547.90`
- `best_pca_config = (pca_hier_uniform, flat-source, k = 8)`

按 `config` 聚合后：

- `pca_hier_uniform = 6735.66 ± 194.54`
- `random_projected_hier = 6769.99 ± 157.02`
- `pca_hier_wdonly = 6854.13 ± 188.77`
- `oracle_hier_wdonly = 6981.46 ± 323.43`

按更细粒度 `(config, source, k, wd)` 看，最优几项是：

1. `random_projected_hier(flat, k=8)`：`6547.90`
2. `pca_hier_uniform(flat, k=8)`：`6595.14`
3. `pca_hier_uniform(dense, k=8)`：`6644.89`

### 8.8 `B1` 判读

`B1` 不能判为成功。

原因不是 `pca` 完全没用，而是：

1. `pca_hier_uniform` 只是在平均上略优于 `random_projected_hier`
2. 但最优 `pca` 并没有稳定压过最优 `random`
3. 更关键的是，`oracle` 本身也没有给出强上界

因此，这轮不能说：

$$
\text{estimated split} \approx \text{oracle split}
$$

更准确的说法是：

- projector 对几何可能有帮助
- 但 projector 还没有以足够稳定的方式转成 LM 收益

---

## 9. 真实模型 prep scan

### 9.1 prep scan 的目的

在正式替换 `Qwen3-0.6B` 的 FFN 之前，先选层位和 `k`。

### 9.2 prep scan 的输入

真实模型是：

- `Qwen3-0.6B`

扫描候选层：

- `8, 14, 20, 24`

扫描 `k`：

- `16, 32`

### 9.3 prep scan 的具体步骤

1. 从 WoS train/test 中读取文本
2. 实际数据字段是：
   - text 列：`abstract`
   - label 列：`domain`
3. 按 domain 平衡采样：
   - `wos_cov_per_domain = 64`
   - `wos_train_per_domain = 128`
   - `wos_test_per_domain = 128`
4. 从 DCLM 采样：
   - `dclm_cov_sequences = 512`
5. 对每个候选层、每个 `k`：
   1. 估计 projector
   2. 提取 `raw / centered / tail_residual` 表征
   3. 在 `tail_residual` 上训练 logistic probe
   4. 再做 KMeans 聚类
   5. 记录：
      - `tail_probe_acc`
      - `tail_purity`
      - `tail_nmi`
      - `tail_sep_trace`
6. 选择规则是：
   1. 先看 `tail_probe_acc`
   2. 再用 `purity / nmi` 打破平局

### 9.4 prep scan 实际命令

```bash
python run_phase4_qwen_block.py \
  --stage prep_scan \
  --output-dir phase4_full_20260418/real_model \
  --device cuda:1 \
  --scan-batch-size 2 \
  --wos-cov-per-domain 64 \
  --wos-train-per-domain 128 \
  --wos-test-per-domain 128 \
  --dclm-cov-sequences 512
```

### 9.5 prep scan 结果

最优结果是：

- `layer = 8`
- `k = 16`
- `tail_probe_acc = 0.7154`
- `tail_purity = 0.5301`
- `tail_nmi = 0.3449`

前几名大致是：

1. `(layer 8, k 16)`
2. `(layer 8, k 32)`
3. `(layer 24, k 16)`
4. `(layer 20, k 16)`

### 9.6 prep scan 判读

这一步说明：

- 在 `Qwen3-0.6B` 上，`layer 8` 的 tail residual 几何最好
- 因此真实 block replacement 就固定在 `layer 8`

---

## 10. `C1`：真实 `Qwen3-0.6B` 单层 block replacement

### 10.1 `C1` 的目的

这是本轮最关键的真实模型实验。目的不是继续做 proxy，而是直接问：

在真实模型里，把单层 FFN 替换成 hierarchical tail-conditioned block，能不能赢过：

- 原始 FFN
- flat raw MoE block

### 10.2 `C1` 只运行 `frozen`

本轮没有触发 `half-frozen`。

原因不是忘了跑，而是按计划：

- 只有 `frozen` 没有信号时，才进入 `half-frozen`
- 实际上 `frozen` 已经给出了清晰正信号

因此没有进入 fallback 分支。

### 10.3 `C1` 使用的数据

`C1` 使用真实数据：

- WoS
- DCLM

数据准备细节如下：

1. 从 WoS 中按 domain 平衡采样
2. 从 DCLM 中随机采样固定条数
3. 对每个 seed 分别重新采样
4. `rare-token` 定义为：
   - 在 `wos_train` 的 labels 中统计 token 频率
   - 选频率最低的末 `25%` token

### 10.4 `C1` 真实模型 block 的 4 类 config

本轮比较：

- `baseline_ffn`
- `flat_moe_raw_uniform`
- `hier_moe_tail_uniform`
- `hier_moe_tail_wdonly`

其中：

- `baseline_ffn`
  - 保留预训练 FFN
  - 只训练这一层 FFN
- `flat_moe_raw_uniform`
  - common branch 从原始 MLP warm-start
  - router / experts 随机初始化
  - router 与 experts 看 full hidden
- `hier_moe_tail_uniform`
  - common branch 从原始 MLP warm-start
  - router / experts 随机初始化
  - router 与 experts 只看：

    $$
    P_t(x-\mu)
    $$
- `hier_moe_tail_wdonly`
  - 结构与 `hier_moe_tail_uniform` 相同
  - 仅优化器参数组不同

### 10.5 `C1` 的冻结方式

`frozen` 的具体含义是：

1. 全模型参数先全部冻结
2. 只把目标层 `layer 8` 的 replacement MLP 打开训练
3. attention、其他层、embedding 都保持冻结

### 10.6 `C1` 的 `WD-only` 实现

只有 `hier_moe_tail_wdonly` 会拆参数组：

- common branch：`weight_decay = gamma_common`
- router：`weight_decay = gamma_common * gamma_ratio`
- experts：`weight_decay = gamma_common * gamma_ratio`

其中：

$$
\gamma_{\mathrm{common}} = 0.1
$$

扫描：

$$
\gamma_{\mathrm{tail}} / \gamma_{\mathrm{common}}
\in \{1.0, 0.3, 0.1\}
$$

### 10.7 `C1` 每个 seed 的具体训练步骤

对每个 seed，脚本执行：

1. 加载 `Qwen3-0.6B`
2. 读取 `prep_scan_summary.json`，固定：
   - `layer = 8`
   - `k = 16`
3. 用 WoS + DCLM 的 `cov_items` 重新估计该 seed 的 projector
4. 构造 `rare_token_set`
5. 依次训练：
   - `baseline_ffn`
   - `flat_moe_raw_uniform`
   - `hier_moe_tail_uniform`
   - `hier_moe_tail_wdonly(gamma=1.0)`
   - `hier_moe_tail_wdonly(gamma=0.3)`
   - `hier_moe_tail_wdonly(gamma=0.1)`
6. 每个 run：
   - `train_steps = 500`
   - `eval_every = 100`
   - `batch_size = 1`
   - `eval_batch_size = 2`
7. 训练过程中按 `mix_ratio_dclm = 4` 混合：
   - 大致 `4` 个 DCLM batch
   - 接 `1` 个 WoS batch
8. 每次评估记录：
   - `dclm_ppl`
   - `wos_ppl`
   - `wos_rare_token_ppl`
   - `router_purity`
   - `router_nmi`
   - `router_load_entropy`
   - `common_tail_grad_ratio`
9. 保存：
   - `best_model.pt`
   - `history.csv`
   - `wos_rare_token_ppl.png`

### 10.8 `C1` 实际命令

```bash
python run_phase4_qwen_block.py \
  --stage c1 \
  --output-dir phase4_full_20260418/real_model \
  --device cuda:1 \
  --freeze-mode frozen \
  --seeds 20260418,20260419 \
  --train-steps 500 \
  --eval-every 100 \
  --forced-layer 8 \
  --forced-k 16 \
  --gamma-ratios 1.0,0.3,0.1 \
  --batch-size 1 \
  --eval-batch-size 2
```

### 10.9 一个实现细节：`C1` 中途曾中断，但已完整续跑

`C1(frozen)` 第一次正式运行时中途停过一次，停在：

- `hier_moe_tail_uniform__seed_20260418`

之后脚本补了断点续跑逻辑：

- 如果某个 `run_dir` 已经有完整 `history.csv`
- 则直接读取最终一行结果
- 不重新训练

然后把 `C1(frozen)` 重新续跑到完整结束。

所以当前的 `c1_results_all.csv` 是完整的 12 行：

- 2 个 seed
- 每个 seed 6 个 config

### 10.10 `C1` 正式结果

按两 seed 聚合后的结果：

- `baseline_ffn`
  - `DCLM PPL = 33.38 ± 1.22`
  - `WoS PPL = 17.22 ± 0.07`
  - `WoS rare-token PPL = 84.00 ± 12.75`
- `flat_moe_raw_uniform`
  - `DCLM PPL = 33.57 ± 1.26`
  - `WoS PPL = 17.35 ± 0.05`
  - `WoS rare-token PPL = 85.04 ± 12.97`
  - `router_purity = 0.1616 ± 0.0004`
  - `router_nmi = 0.0016 ± 0.0010`
- `hier_moe_tail_uniform`
  - `DCLM PPL = 32.72 ± 1.25`
  - `WoS PPL = 16.94 ± 0.07`
  - `WoS rare-token PPL = 81.53 ± 12.41`
  - `router_purity = 0.1565 ± 0.0006`
  - `router_nmi = 0.0006 ± 0.0001`
- `hier_moe_tail_wdonly`
  - `gamma = 1.0 / 0.3 / 0.1` 三组结果完全相同
  - 与 `hier_moe_tail_uniform` 完全重合

### 10.11 `C1` 单个 seed 上的方向

#### seed `20260418`

- `baseline_ffn`
  - `DCLM PPL = 32.52`
  - `WoS PPL = 17.28`
  - `WoS rare-token PPL = 93.02`
- `flat_moe_raw_uniform`
  - `DCLM PPL = 32.68`
  - `WoS PPL = 17.38`
  - `WoS rare-token PPL = 94.21`
- `hier_moe_tail_uniform`
  - `DCLM PPL = 31.84`
  - `WoS PPL = 16.99`
  - `WoS rare-token PPL = 90.30`

#### seed `20260419`

- `baseline_ffn`
  - `DCLM PPL = 34.24`
  - `WoS PPL = 17.17`
  - `WoS rare-token PPL = 74.98`
- `flat_moe_raw_uniform`
  - `DCLM PPL = 34.46`
  - `WoS PPL = 17.31`
  - `WoS rare-token PPL = 75.87`
- `hier_moe_tail_uniform`
  - `DCLM PPL = 33.61`
  - `WoS PPL = 16.89`
  - `WoS rare-token PPL = 72.75`

### 10.12 `C1` 判读

`C1` 的判读非常明确：

1. `hier_moe_tail_uniform > flat_moe_raw_uniform`
2. `hier_moe_tail_uniform > baseline_ffn`
3. `flat_moe_raw_uniform < baseline_ffn`

也就是说：

- flat raw MoE 这轮在真实模型里没有带来收益
- 但 hierarchical tail-conditioned block 确实带来了收益

这条结论是本轮最重要的正结果。

但同时也必须诚实写清楚：

1. `router_purity / router_nmi` 仍然极低
2. `router_load_entropy` 非常接近均匀分布的：

   $$
   \log 4 \approx 1.386
   $$

3. `WD-only` 的三种比例与 uniform 结果完全重合

因此，当前更像是：

$$
\text{factorized residual block gain}
$$

而不是：

$$
\text{strong discrete expert specialization gain}
$$

---

## 11. 这轮主线到底推进到了哪里

### 11.1 已经成立的命题

这轮已经成立的主线命题有：

1. 在 small-model 里，`split-first` 优于 `flat raw route`
2. 在真实 `Qwen3-0.6B` 里，`hier_moe_tail_uniform` 优于：
   - `baseline_ffn`
   - `flat_moe_raw_uniform`

因此，“先 split 再 route 的 block 结构”已经开始进入真实模型。

### 11.2 没有成立的命题

这轮没有成立的命题有：

1. `WD-only` 会进一步带来收益
2. `mild LB` 是必要条件
3. estimated projector 稳定替代 oracle split
4. routing 的 `purity / NMI` 会显著上升

### 11.3 最准确的总判断

这轮最准确的总判断应该写成：

1. **结构主线成立**
   - `split-first hierarchical block` 在真实模型里开始 work
2. **projector 主线未成立**
   - `B1` 没有过 gate
3. **WD-only 附加收益未成立**
   - small-model 与 real-model 两边都没看到额外增益
4. **specialization 主线未成立**
   - `purity / NMI` 几乎不动

---

## 12. 建议理论 AI 优先分析的点

如果理论 AI 只分析 4 个问题，最值得优先看的是：

### 12.1 为什么 `A1` 和 `C1` 都是 “split 有效”，但 routing 贡献很弱

也就是为什么当前看到的是：

$$
\text{split gain} \gg \text{routing gain}
$$

### 12.2 为什么 `B1` 失败

具体说：

- 为什么 `pca_hier_uniform(flat, k=8)` 接近最优 random，但没能稳定压过去
- 为什么 `oracle_hier` 本身也没有显著上界优势

### 12.3 为什么 `WD-only` 在 small-model 和 real-model 里都没有额外收益

尤其是：

- 在 `C1` 中三种 `gamma_ratio` 与 uniform 完全重合

这意味着当前脚本的 `WD-only` 可能根本没有进入真正起作用的 regime，或者当前 frozen 设置下 tail params 的 effective dynamics 不敏感。

### 12.4 为什么 `router_purity / NMI` 极低，但 PPL 已经改善

这可能意味着：

- 我们现在看到的是 continuous factorization gain
- 而不是离散 expert specialization gain

也可能意味着：

- 当前 router 指标与真正的 LM specialization 目标不对齐

---

## 13. 如果只给理论 AI 一句话

如果只能给理论 AI 一句压缩版总结，我建议写成：

> `Phase4` 已经证明：在真实 `Qwen3-0.6B` 的单层 block replacement 中，`hierarchical tail-conditioned block` 明显优于 `baseline FFN` 和 `flat raw MoE`；但本轮 gain 来自结构 factorization，而不是 projector 成功或 WD-only 成功，也不是强 expert specialization 成功。

这句话基本能准确概括本轮的真实推进与真实失败。 
