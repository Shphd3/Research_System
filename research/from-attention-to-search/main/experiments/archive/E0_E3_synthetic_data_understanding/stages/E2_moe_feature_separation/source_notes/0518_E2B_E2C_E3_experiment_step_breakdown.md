# 实验步骤详细解析：E2-B / E2-C / E3

## 1. 三个实验的共同背景

共同问题：

```text
synthetic feature 已经能被模型读回，
但 natural MoE router 没有把 ABC/DEF/GHI/JKL 干净分给不同 expert。
```

共同数据基础：

```text
vocab_size = 1000
feature type = trigram relation
task = next-token prediction
model = 1-layer causal Transformer + 4-expert top-1 MoE FFN
```

核心指标：

| metric | 含义 | 用来判断什么 |
|---|---|---|
| readback probability | feature prefix 下预测 target token 的概率 | 模型是否学会任务 |
| NMI / ARI | feature label 与 expert id 的一致性 | routing 是否按 feature 分 |
| best-perm acc | 允许重排 expert 编号后的 feature-expert 匹配率 | 是否形成任意编号的一对一分工 |
| fixed-label acc | 固定 ABC->0, DEF->1 等编号后的准确率 | 是否形成指定 expert 映射 |
| ablation drop | 删除 dominant expert 后 target probability 下降 | expert 对 feature 是否有因果贡献 |
| feature-linear-probe | 从 hidden state 线性预测 feature label | 表示是否可分 |

## 2. E2-B Prototype / Center Gating

### 2.1 要问的问题

普通 linear router 没有 clean 分工，可能是 router 形式不够像聚类。E2-B 问：

```text
如果每个 expert 有一个可学习中心 c_e，
router 按 hidden 与中心的 cosine similarity 选 expert，
是否会更自然地形成 feature cluster -> expert 的映射？
```

### 2.2 模型改动

原始 linear router：

$$
\text{logits}_e = w_e^\top h_t + b_e
$$

E2-B prototype router：

$$
s_{t,e} = \tau \cdot \frac{z_t^\top c_e}{\|z_t\|\|c_e\|}
$$

其中：

- $h_t$ 是 prefix-end position 的 hidden state；
- $z_t$ 是 router 使用的投影表示；
- $c_e$ 是 expert $e$ 的 prototype center；
- $\tau$ 是温度/缩放因子；
- top-1 expert 是 $\arg\max_e s_{t,e}$。

### 2.3 实验步骤

1. 使用均匀 all-trigram 数据：ABC/DEF/GHI/JKL 频率相同。
2. 固定人工期望映射：ABC->expert 0，DEF->expert 1，GHI->expert 2，JKL->expert 3。
3. 训练 5 个 variants：
   - `prototype_no_aux_no_lb`
   - `prototype_no_aux_lb`
   - `prototype_aux_0_1_no_lb`
   - `prototype_aux_1_0_no_lb`
   - `prototype_aux_1_0_lb`
4. 每个 variant 跑 5 个 seeds，每个 seed 10000 steps。
5. 统计 readback、routing matrix、NMI、best-perm acc、fixed-label acc、expert load、ablation drop。
6. 额外统计 prototype-specific 几何量：prototype cosine、feature centroid 到 prototype 的 cosine。

### 2.4 结果如何读

如果 no-aux prototype 自然 clean，说明聚类式 router inductive bias 足够。  
如果只有 aux prototype clean，说明架构能承载 clean 分工，但 natural NTP 没给足 feature-to-expert assignment pressure。  
实际结果属于第二种。

## 3. E2-C Contrastive Router Loss

### 3.1 要问的问题

E2-B 的 prototype CE 太直接绑定 feature->expert。E2-C 问一个更弱的问题：

```text
不指定 feature 应该进哪个 expert，
只让同一 feature 的 router representation 更近、不同 feature 更远，
能否自然诱导 expert 分工？
```

### 3.2 模型改动

Router representation：

$$
r_t = \mathrm{normalize}(W_p h_t)
$$

Supervised contrastive loss：

$$
L_{\text{supcon}}
=
-\frac{1}{N}
\sum_i
\frac{1}{|P(i)|}
\sum_{p\in P(i)}
\log
\frac{\exp(r_i^\top r_p/T)}
{\sum_{a\neq i}\exp(r_i^\top r_a/T)}
$$

其中：

- $P(i)$ 是与样本 $i$ 属于同一 feature 的样本集合；
- $T$ 是 temperature；
- loss 只要求同类靠近、异类远离；
- 它不规定 ABC 必须进入哪个 expert。

### 3.3 实验步骤

1. 使用同一均匀 all-trigram 数据。
2. 训练 5 个 variants：
   - `contrastive_no_aux_no_lb`
   - `contrastive_no_aux_lb`
   - `contrastive_aux_0_1_no_lb`
   - `contrastive_aux_1_0_no_lb`
   - `contrastive_aux_1_0_lb`
3. 每个 variant 跑 5 个 seeds，每个 seed 10000 steps。
4. 评估 readback、routing NMI、best-perm acc、fixed-label acc、load entropy、ablation drop。
5. 对 $r_t$ 做 linear probe，检查 feature label 是否可读出。
6. 画 router representation PCA，检查可视化聚类是否与 expert assignment 一致。

### 3.4 结果如何读

如果 contrastive aux 后 NMI 接近 1，说明“表示聚类压力”足以变成 expert 分工。  
如果 representation probe 已经 1.0，但 NMI 仍不高，说明“可分表示”和“expert assignment”之间还有断裂。  
实际结果是后者：$r_t$ 中 feature 可读出，但 top-1 routing 不 clean。

## 4. E3 Gating Failure Mode Diagnostic

### 4.1 要问的问题

E2-B 和 E2-C 说明：换 router 形式或让表示更可分，都不足以解释 natural router failure。E3 系统诊断：

```text
natural router 到底按什么变量切分？
如果给真实 feature supervision，同一个模型是否能 clean specialize？
```

### 4.2 数据控制

E3 使用 4 组 uniform synthetic trigram datasets：

| dataset | relations | 目的 |
|---|---|---|
| `unique_uniform` | `[1,2]->22`, `[3,4]->23`, `[6,7]->20`, `[8,9]->21` | 标准基线 |
| `shared_b_uniform` | `[1,2]->22`, `[3,2]->23`, `[6,7]->20`, `[8,7]->21` | 检查 prefix-end token shortcut |
| `shared_target_uniform` | `[1,2]->22`, `[3,4]->22`, `[6,7]->20`, `[8,9]->20` | 检查 target-token shortcut |
| `crossed_factorial_uniform` | `[1,2]->22`, `[1,4]->23`, `[3,2]->23`, `[3,4]->22` | 打散 first token / end token / target token 的一一对应 |

### 4.3 训练变体

每个 dataset 跑：

| variant | loss | 用途 |
|---|---|---|
| `moe_top1_no_lb` | $L_{\text{NTP}}$ | natural baseline |
| `moe_top1_lb` | $L_{\text{NTP}} + 0.01L_{\text{LB}}$ | 检查 LB 是否解决 routing |
| `router_aux_lam_1_0` | $L_{\text{NTP}} + L_{\text{router-feature}}$ | supervised upper bound |

其中：

$$
L_{\text{router-feature}}
=
\mathrm{CE}(\text{router logits at prefix-end position}, \text{feature id})
$$

### 4.4 E3 的执行流程

1. 先 smoke：只跑 crossed-factorial 的 `moe_top1_no_lb` 和 `router_aux_lam_1_0`，500 steps。
2. smoke 通过后 full run：4 datasets × 3 variants × 5 seeds，共 60 runs。
3. 每个 run 训练 10000 steps。
4. 对 `unique_uniform` 和 `crossed_factorial_uniform` 保存 dynamics checkpoints：0、10、50、100、200、500、1000、2000、5000、10000。
5. 对最终 checkpoint 做 predictor decomposition。
6. 对最终 checkpoint 做 component ablation / forced-routing utility。
7. 聚合表格和图片，写 `summary.md` / `detailed.md`。

### 4.5 Predictor Decomposition 怎么读

E3 把每个 prefix event 记录成表：

```text
feature_id
first_token
prefix_end_token
target_token
hidden_norm
router_logits
router_margin
router_entropy
target_probability
CE_loss
PCA coordinates
router projection coordinates
top1_expert
```

然后用 multinomial logistic regression 预测 `top1_expert`。

| predictor group | 含义 |
|---|---|
| `feature-only` | expert 是否按人工 feature label 分 |
| `B-token-only` | expert 是否按 prefix-end token 分 |
| `target-token-only` | expert 是否按目标 token 分 |
| `difficulty-only` | expert 是否按 CE / margin / confidence 分 |
| `norm-only` | expert 是否按 hidden scale 分 |
| `PCA-only` | expert 是否按 hidden geometry 主方向分 |
| `router-projection` | expert 是否按 router 权重敏感方向分 |
| `full-hidden` | hidden 是否足够预测 expert id |
| `feature-linear-probe` | hidden 是否足够预测 feature id |

关键读法：

```text
如果 feature-linear-probe = 1.0，
但 feature-only -> expert 很低，
说明 feature 信息在 hidden 里存在，但 router 没按 feature label 用。
```

实际结果正是这样。

### 4.6 Component Ablation 怎么读

E3 比较：

| mode | 含义 |
|---|---|
| `learned` | 使用模型学到的 route |
| `force_random_expert_expectation` | 平均强制使用每个 expert 的结果 |
| `mean_expert_output` | 平均多个 expert 输出 |
| `zero_moe_output` | 删除 MoE 输出 |
| `force_feature_oracle_expert` | 强制用人工 feature 对应 expert |
| `force_best_utility_expert` | 强制用对当前 feature 预测最强的 expert |

如果 random/mean expert 仍然高，说明多个 experts 都能做同一 feature。  
如果 zero MoE 很低，说明 MoE path 仍然重要。  
两者合起来说明：

```text
MoE 对任务有贡献，但 natural routing 不是 clean 独占分工。
```

## 5. 三个实验合起来的逻辑链

1. E2-B：prototype router 不是自然解；但加 feature CE 后能 clean。
2. E2-C：contrastive representation 可分不是充分条件；cluster 不自动变 assignment。
3. E3：同一模型在 supervised router 下全部 clean；natural router 不 clean；hidden feature 可分但 router 不按 feature label 切。

最终闭环：

```text
当前 failure 的核心不是表示学不到，也不是 expert 容量不够；
而是 natural NTP objective 没有把可分 feature representation 转成 clean expert assignment 的必要压力。
```
