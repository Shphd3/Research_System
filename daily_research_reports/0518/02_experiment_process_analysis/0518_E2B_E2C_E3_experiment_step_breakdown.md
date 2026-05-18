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

## 5. 四个诊断合起来的逻辑链

1. E2-B：prototype router 不是自然解；但加 feature CE 后能 clean。
2. E2-B2：center separation 可以撑开 expert centers，但不自动产生 feature-to-expert assignment。
3. E2-C：contrastive representation 可分不是充分条件；cluster 不自动变 assignment。
4. E3：同一模型在 supervised router 下全部 clean；natural router 不 clean；hidden feature 可分但 router 不按 feature label 切。

最终闭环：

```text
当前 failure 的核心不是表示学不到，也不是 expert 容量不够；
而是 natural NTP objective 没有把可分 feature representation 转成 clean expert assignment 的必要压力。
```

## 6. 补充实验：E2-B2 Center Separation Prototype Router

Correction: E2-B2 使用 hard top-1 prototype routing，expert output 没有乘以 selected gate probability，因此自然 $L_{\text{NTP}}$ 不能可靠训练 prototype centers。E2-B3 已经修正这一点，后续关于 prototype center dynamics 的结论以 E2-B3 为准。

### 6.1 要问的问题

如果不使用 feature label supervision，只让每个 expert 的 prototype center 彼此远离，是否能自然形成 clean one-feature-one-expert？

这比 E2-B 的 feature CE 更接近实际可用形式，因为它不需要知道 ABC/DEF/GHI/JKL 的真实标签。

### 6.2 损失函数

对 expert centers $c_e$ 做归一化后，惩罚不同 centers 的正余弦相似度：

$$
L_{\text{center-sep}}
=
\frac{1}{E(E-1)}
\sum_{e \neq e'}
\max(0,\cos(c_e,c_{e'}) - m)^2
$$

本轮使用 $m=0$，总损失为：

$$
L
=
L_{\text{NTP}}
+ \lambda_{\text{sep}} L_{\text{center-sep}}
+ \lambda_{\text{LB}} L_{\text{LB}}
$$

其中 center separation 只让 centers 分开，不告诉 router 哪个 feature 应该进入哪个 center。

### 6.3 运行设置

本轮只跑 3 seeds：`20260513/20260514/20260515`。  
数据仍是 uniform all-trigram synthetic corpus。

| variant | center-sep coef | LB |
|---|---:|---:|
| `prototype_center_sep_0_1_no_lb` | 0.1 | no |
| `prototype_center_sep_1_0_no_lb` | 1.0 | no |
| `prototype_center_sep_1_0_lb` | 1.0 | yes |

### 6.4 结果

| variant | readback | NMI | best-perm acc | load entropy | ablation drop |
|---|---:|---:|---:|---:|---:|
| `prototype_center_sep_0_1_no_lb` | 0.9952 | 0.4843 | 0.5077 | 1.1363 | 0.3629 |
| `prototype_center_sep_1_0_no_lb` | 0.9948 | 0.4875 | 0.5238 | 1.1414 | 0.3980 |
| `prototype_center_sep_1_0_lb` | 0.9949 | 0.5783 | 0.5284 | 1.3862 | 0.4060 |

Prototype centers 的 off-diagonal cosine 已经被压到非正，final `center_sep_loss = 0.0`。也就是说，center separation 目标本身是成功的。

### 6.5 结论

E2-B2 说明：

```text
把 expert centers 撑开，可以避免 center collapse；
但不能自动把 feature clusters 分配到不同 experts。
```

因此，缺失的不是 center geometry pressure，而是 assignment-level pressure：目标函数需要推动“不同 feature-like clusters 使用不同 experts”，而不只是让 expert centers 彼此远离。

## 7. 修正实验：E2-B3 Trainable Prototype Dynamics

### 7.1 修正了什么

旧 prototype top-1：

$$
e^*=\arg\max_e p_{t,e},
\quad
y_t=\mathrm{Expert}_{e^*}(h_t)
$$

这里 `argmax` 不可导，而且 $y_t$ 不含 $p_{t,e^*}$，所以自然 $L_{\text{NTP}}$ 不会反传到 router/prototype。

E2-B3 改成：

$$
y_t=p_{t,e^*}\mathrm{Expert}_{e^*}(h_t)
$$

这样 NTP loss 可以通过 $p_{t,e^*}$ 更新 prototype centers。

### 7.2 实验设置

本轮 3 seeds：`20260513/20260514/20260515`。

| variant | loss | 目的 |
|---|---|---|
| `trainable_center_natural_no_lb` | $L_{\text{NTP}}$ | 看 centers 是否自然对齐 feature |
| `trainable_center_sep_1_0_no_lb` | $L_{\text{NTP}} + L_{\text{center-sep}}$ | 看撑开 centers 是否足够 |
| `trainable_center_supervised_ce_1_0_no_lb` | $L_{\text{NTP}} + L_{\text{router-feature}}$ | supervised upper bound |

### 7.3 结果

| variant | first prototype grad | readback | NMI | best-perm acc | fixed-label acc |
|---|---:|---:|---:|---:|---:|
| natural NTP | 0.0050 | 0.9957 | 0.5772 | 0.5000 | 0.3333 |
| center separation | 0.0706 | 0.9955 | 0.1924 | 0.3333 | 0.2500 |
| supervised CE | 4.1205 | 0.9969 | 1.0000 | 1.0000 | 1.0000 |

### 7.4 结论

E2-B3 说明：

```text
prototype centers 在 NTP 下确实收到梯度并移动；
但 natural NTP 仍不会把 centers 自然演化成四个 feature centers。
```

Center separation 能把 centers 撑开，但不能把 feature clusters 分配给不同 centers。Supervised CE 能 clean，说明模型和代码链路能做这件事；失败仍然来自 assignment-level pressure 不足。
