# 实验设计文档：训练过程与训练目标

## 0. 实验目标

本实验的第一目标不是在真实数据上证明 hierarchy，而是在一个真相已知的 synthetic Zipfian hierarchy dataset 上验证：

> 如果数据真的由 common / coarse / fine 三层机制生成，模型能不能学出这种层级结构？

因此，“学得出来”必须同时包含：

1. next-token prediction loss 下降；
2. router 能恢复真实 coarse label、group 内 conditional common/tail source、fine latent labels；
3. selected expert 在 token-level NTP loss 上优于 alternative experts。

---

## 1. 固定模型设置

第一版使用：

```yaml
base_model: Qwen3-0.6B
backbone: frozen
trainable_part: layer-8 replacement block / adapter block
hook_point: post_attention_layernorm
task: next-token prediction
sequence_length: 128
```

不建议第一版 full fine-tune 0.6B。

原因：

1. 训练成本太高；
2. 很难判断 hierarchy 是否来自模型结构；
3. 冻结 backbone + 单层 replacement block 更适合做结构审计。

---

## 2. 输入与标签

每条样本包含：

```json
{
  "text": "...",
  "input_ids": [...],
  "labels": [...],
  "coarse_label": c,
  "fine_label": f,
  "span_source": [...],
  "token_source": [...],
  "token_frequency_bucket": [...]
}
```

其中：

- `labels` 用于 next-token prediction；
- `coarse_label` 和 `fine_label` 只用于评估 router 是否学出真实 hierarchy；
- `token_source` 用于评估 global common / conditional-common / conditional-tail 是否被正确分化；
- 第一版主训练不使用 label supervision；
- oracle / teacher-aided ablation 可以使用 label。

---

## 3. 主训练目标

### 3.1 Next-token prediction loss

主目标是标准语言模型损失：

$$
L_{\text{LM}}
=
-\frac{1}{T}
\sum_{t=1}^{T}
\log p_\theta(y_t \mid y_{<t})
$$

所有模型都必须使用同一个 $L_{\text{LM}}$。

---

## 4. Router 相关 loss

### 4.1 主实验：不加 router supervision

主实验只用：

$$
L = L_{\text{LM}}
$$

这样可以检验 hierarchy 是否能从 NTP objective 中自然学出来。

---

### 4.2 Load-balance loss 消融

普通 MoE 通常使用 load-balance loss，记为：

$$
L_{\text{LB}}
$$

带 LB 的训练目标为：

$$
L
=
L_{\text{LM}}
+
\lambda_{\text{LB}}L_{\text{LB}}
$$

需要比较：

```text
no-LB
flat MoE + LB
hierarchical MoE + coarse LB
hierarchical MoE + coarse + source LB
hierarchical MoE + coarse + source + fine LB
```

第一版建议：

```yaml
lambda_LB: [0, 0.01]
```

LB 不能被当作成功本身。

如果 expert usage 更均匀，但 NTP loss 或 expert advantage 没提升，不能说 hierarchy 成立。

---

### 4.3 Teacher-aided router loss 只做诊断

为了区分“结构没用”和“router 学不出来”，可以加入 teacher-aided loss：

$$
L_{\text{route}}
=
\operatorname{CE}(g_c(x), c)
+
\operatorname{CE}(g_s(x,c), s)
+
\operatorname{CE}(g_f(x,c), f)
$$

对应总 loss：

$$
L
=
L_{\text{LM}}
+
\lambda_{\text{route}}L_{\text{route}}
$$

但这不是主实验，只是诊断。

第一版建议：

```yaml
lambda_route: [0, 0.1]
```

解释：

- 如果 teacher-aided 明显提升，说明结构可能有用，但 router 自己学不出来；
- 如果 teacher-aided 也不提升，说明当前 hierarchy 结构或数据任务本身可能不需要 hierarchy。

---

## 5. 训练流程

### Step 1: Dataset sanity check

先确认 synthetic dataset 满足：

1. Zipfian slope 合格；
2. coarse / fine item-token concentration 合格；
3. coarse / fine labels 可由 item-token statistics 初步恢复；
4. prefix-level coarse / fine 可识别性合格；
5. template-only classifier 没有形成明显 shortcut。

如果数据不合格，不进入训练。

---

### Step 2: Hidden-state calibration

用 frozen Qwen3-0.6B 在 synthetic train subset 上收集 layer 8 hidden states：

$$
x \in \mathbb{R}^{d}
$$

计算均值：

$$
\mu=\mathbb{E}[x]
$$

做 PCA/SVD：

$$
V=[v_1,\dots,v_r]
$$

定义 middle band：

$$
x_{\text{mid}}
=
P_M(x-\mu)
$$

第一版沿用此前定义：

$$
M=[17,207]
$$

如果 hidden rank 或维度不同，则使用同等比例区间并在报告里说明。

同时在 $M$ 内部定义 group 内 conditional routing 使用的子 band：

```text
M_cc: 用于 conditional common/tail source router
M_tail: 用于 fine/tail router 或 tail expert input
```

第一版可以按 $M$ 内部方差排序切分，必须在日志和报告中保存实际 index。

---

### Step 3: Train model groups

每个模型组使用相同：

- train split；
- valid split；
- test split；
- optimizer；
- total steps；
- batch size；
- trainable parameter budget；
- random seeds。

第一版建议：

```yaml
optimizer: AdamW
learning_rate: 5e-5
weight_decay: 0.01
batch_size_tokens: fixed across groups
train_steps: 5000
eval_every: 500
seeds: [0, 1, 2]
```

### Step 4: Training budget

第一版数据规模：

```text
train_docs = 50000
sequence_length = 128
tokens_per_epoch = 6.4M
```

如果使用：

```text
batch_size_tokens = 4096
train_steps = 5000
```

则每个模型每个 seed 训练：

```text
total_train_tokens = 20.48M
equivalent_epochs = 3.2
```

报告中统一写：

> 每个模型每个 seed 训练约 20M tokens，约 3.2 epochs。

---

## 6. 评估指标

### 6.1 NTP loss

报告：

$$
L_{\text{test}}
$$

以及按 token source 分桶：

```text
common-token NLL
coarse-token NLL
fine-token NLL
conditional-common-token NLL
conditional-tail-token NLL
```

如果 hierarchy 真的有用，应该至少在 coarse / fine token 上有优势。

---

### 6.2 Router recovery

对 hierarchical model，报告 coarse router accuracy：

$$
\operatorname{Acc}_{\text{coarse}}
=
\mathbb{P}[\hat c=c]
$$

fine router accuracy：

$$
\operatorname{Acc}_{\text{fine}}
=
\mathbb{P}[\hat f=f]
$$

group 内 source router accuracy：

$$
\operatorname{Acc}_{\text{source}}
=
\mathbb{P}[\hat s=s]
$$

其中：

```text
token_source = common -> global common path
token_source = coarse -> conditional-common path
token_source = fine -> conditional-tail path
```

也报告 flat leaf expert 的 fine-label recovery。

---

### 6.3 Expert functional advantage

对每个 token，计算每个 expert 的 counterfactual NTP loss。

selected expert advantage：

$$
A(t)
=
\ell_{\text{second-best}}(t)
-
\ell_{\text{selected}}(t)
$$

如果：

$$
\mathbb{E}[A(t)]>0
$$

说明 selected expert 真的更适合当前 token。

按以下分桶报告：

```text
common tokens
coarse-specific tokens
fine-specific tokens
conditional-common tokens
conditional-tail tokens
middle-frequency tokens
rare tokens
```

---

### 6.4 Oracle regret

定义 oracle expert：

$$
e^*(t)=\arg\min_e \ell_e(t)
$$

learned router regret：

$$
\operatorname{Regret}(t)
=
\ell_{\text{selected}}(t)
-
\ell_{e^*(t)}(t)
$$

解释：

- regret 低：router 接近最优选择；
- regret 高：experts 可能有用，但 router 没学会；
- oracle 也不强：experts 没有学出功能差异。

---

### 6.5 Coarse cascade error

hard hierarchical router 可能因为 coarse router 错误导致 fine router 失效。

报告：

```text
learned hard hierarchy
soft hierarchy
oracle coarse + learned fine
learned coarse + oracle fine
oracle coarse + learned source + learned fine
learned coarse + oracle source + learned fine
oracle full hierarchy
```

如果 oracle coarse 明显好于 learned hard hierarchy，说明瓶颈在 coarse router。

---

## 7. “学得出来”的通过标准

一个 hierarchical model 只有同时满足以下条件，才叫学得出来：

### Gate 1: Prediction gate

hierarchical model 的 test NLL 低于 dense 和 flat MoE，或至少接近 oracle hierarchy。

### Gate 2: Router recovery gate

coarse router 能恢复真实 coarse label：

```text
coarse_acc >= 80%
```

fine router 能恢复真实 fine label：

```text
fine_acc >= 60%
```

group 内 source router 能区分 conditional-common / conditional-tail：

```text
source_acc >= 70%
```

第一版阈值可以根据数据难度微调，但必须提前写入报告。

### Gate 3: Expert advantage gate

selected expert advantage 为正：

$$
\mathbb{E}[A(t)]>0
$$

尤其在 coarse / fine / conditional-common / conditional-tail / rare tokens 上为正。

### Gate 4: Oracle sanity gate

oracle hierarchy 必须明显强于 dense / flat。

如果 oracle hierarchy 不强，说明数据任务不需要 hierarchy。

---

## 8. 结果解释规则

### Case A: Oracle 强，learned hierarchy 强

结论：

> 该 synthetic setting 下，hierarchical structure 能学出来。

下一步可以迁移到更真实的数据或更弱 supervision。

---

### Case B: Oracle 强，learned hierarchy 弱

结论：

> hierarchy 结构有潜力，但 router 学不出来。

下一步修 router，例如 teacher-aided routing、soft hierarchy、route stability regularization。

---

### Case C: Oracle 不强

结论：

> 当前 synthetic dataset 没有真正需要 hierarchy。

下一步应增强 fine-specific signal 或重构数据生成机制。

---

### Case D: Flat MoE 强于 hierarchy

结论：

> 当前 hard hierarchy 可能发生 cascade error，或者 coarse split 不适合作为第一层路由。

下一步比较 soft hierarchy 和 flat leaf router。

---

## 9. 最小训练矩阵

第一版只跑：

| group | 作用 |
|---|---|
| G0 Dense matched | 参数量基线 |
| G1 Flat MoE raw + LB | 普通 MoE 基线 |
| G2 Flat MoE middle + LB | 普通 MoE 但 router 看 middle band |
| G3 H-Mid-Soft | 浅层 coarse/fine hierarchy 基线 |
| G4 H-CondCT-Soft | 第一阶段主模型：coarse -> conditional common/tail -> fine |
| G5 H-CondCT-Soft + LB | 检查 LB 影响 |
| G6 H-CondCT-LevelInput | 检查不同层级 expert 是否需要不同 band input |
| G7 H-Oracle-CondCT | 上界 |
| G8 H-Rand-CondCT | 随机谱空间对照 |

不要第一版跑太多组。先确认任务和 metric 是否能工作。
