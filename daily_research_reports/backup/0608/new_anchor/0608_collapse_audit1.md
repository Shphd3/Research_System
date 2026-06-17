# 0608 Conversation Summary

## 0. One-Line State

当前研究已从“feature assumption relaxation”暂时回到 **uniform feature baseline 的 collapse root-cause audit**。目前最安全的主结论是：

```text
uniform feature frequency 不保证 hidden representation zero-mean；
transformer hidden state 中的 common component c 会通过 linear gate 的 w_e^T c 形成 expert-specific effective bias，
从而解释 step-0 dominant expert；
但 final collapse 还需要 top-1 training amplification / anti-lockin dynamics 来解释。
```

当前 iteration 已经能较强解释 **step-0 load imbalance**，但还不能 claim 已解决 **final collapse** 或已经得到可推广的架构方法。

---

## 1. Main Research Question

### Parent Problem

```text
ordinary top-1 MoE router 在 NTP 训练下形成的 route consistency，
是否代表 feature-level routing / expert specialization？
```

### Current Subproblem

```text
在构造的 feature 均匀分布、Gating 矩阵 random uniform 初始化
w_ij ~ U(-1/sqrt(d_model), 1/sqrt(d_model)) 的情形下，
为什么 MoE 仍然发生路由坍缩？
```

### Current Decision Question

```text
collapse 是否主要来自：
1. data / code / init bug；
2. finite random initialization geometry；
3. hidden-state common component 诱导的 common offset；
4. top-1 training amplification；
5. evidence insufficient？
```

本轮已经基本关闭 `1` 的一阶怀疑，并把主机制推进到 `3 + 4`。

---

## 2. Code / Data / Initialization Audit

### Audit Verdict

code audit 给出的核心判断：

```text
data_uniformity: PASS with boundary
sequence_randomization: PASS
model_initialization: PASS
router_gating_initialization: PASS with distinction
hidden_common_direction_sources: PASS
conclusion: no first-order bug found
```

### Audit 说明了什么

1. 当前 collapse 不优先解释为数据构造不均衡。
2. router random initialization 实现本身没有明显 bug。
3. R* router 是 bias-free random linear router；S* 是 slot-centroid overwrite，不能被当作 random-init evidence。
4. 训练前 hidden states 已经存在强 common component。
5. residual-only / logit-cancel routing 能把 step-0 load 拉回接近 random/balanced range。

### Audit 的边界

不能 claim：

```text
common direction 是唯一 root cause；
final collapse 已经被解释完全；
position embedding 已经被 causal 证明；
anti-lockin 方法已经有效泛化。
```

Audit 的作用是 **validity gate**：它允许我们从 bug hunting 进入 mechanism experiment。

---

## 3. Revised Anchor Core

### Core Mechanism

将 routed hidden centroid 写成：

```math
h_f = c + r_f
```

其中：

```text
h_f: feature f 的 routed-position hidden centroid
c: across-feature common component
r_f: feature-specific residual
w_e: router row for expert e
```

linear router logit：

```math
z_{f,e} = w_e^T h_f
        = w_e^T c + w_e^T r_f
```

定义：

```math
a_e = w_e^T c
```

则 `a_e` 对所有 feature 共享，相当于：

```text
expert e 的 effective common bias
```

因此，即使：

```text
data frequency uniform
router bias=False
router random initialized
```

也仍然会因为不同 router rows 对 `c` 的随机投影不同，产生 step-0 dominant expert。

### Correct Framing

不要写成：

```text
collapse 是 common 导致，还是 init 导致？
```

应写成：

```text
common component 如何在 random init 下变成 effective router bias，
并被 top-1 training 放大成 final collapse？
```

---

## 4. 0608 Experiments: Purpose / Result / Boundary

### Protocol Summary

| Protocol | 它问的问题 | 结果说明 | 边界 |
|---|---|---|---|
| P0 | data / init / code 是否存在一阶错误？ | 没有发现一阶错误，可以进入机制解释 | P0 不证明 common 是原因 |
| P1 | step-0 hidden states 是否存在 common component？ | 有；full hidden step-0 load 明显偏 | diagnostic，不是 causal ablation |
| P2 | common score `w_e^T c` 能否预测 step-0 dominant expert？ | 能，agreement 接近 1.0，强于 random baseline 0.25 | 解释 step-0，不解释 final collapse |
| P3 | 训练时取消 common offset，collapse 会不会下降？ | hard collapse 下降，accuracy 保持，但 final max-load 仍偏高 | common 是 early driver，但不是全部 |
| P4 | common-aware initialization 能否修复 step-0 bias？ | 能显著降低 step-0 load；final mixed | init alone 不够 |
| P5 | 哪种 common-control 更稳定？ | logit-level cancellation 最稳；SVD / low-rank residual 不稳定 | 不能 claim common subtraction 是最终算法 |
| P6 | anti-lockin warmup 能否控制 final collapse？ | P6A load-balance warmup 最强，final load 下降且 accuracy 基本保持 | load balance 不等于 feature specialization |
| P7 | final router 是不是选错 expert？ | post-training route-utility match 很高 | 不能说 router 错选；应说 route 和 expert utility co-adapt |

---

## 5. What The Results Mean

### 5.1 Step-0 Load Imbalance

Step-0 load 是训练前 routing geometry diagnostic。

如果 feature centroids 和 router rows 接近各向同性随机分布，top-1 assignment 不会完全均匀，但 max-load 应该接近 matched random baseline，而不是出现极端 dominant expert。

本轮结果支持：

```text
common-score w_e^T c predicts step-0 dominant expert；
logit common-offset cancellation 将 step-0 max-load 从高集中状态拉回接近 random/balanced range。
```

因此，step-0 偏向更像：

```text
hidden common component c 通过 w_e^T c 形成 effective expert bias。
```

而不是：

```text
普通 random split，或者 bad router initialization。
```

### 5.2 Training Dynamics

common-offset control 修复的是 early geometry；但 final collapse 仍可能发生。

解释：

```text
hard top-1 routing 让 early winner 获得更多 traffic / gradient；
expert utility 与 router assignment 发生 co-adaptation；
因此 final routing 可能重新集中。
```

本轮最安全表述：

```text
final collapse = common-offset seeded + top-1 training amplified。
```

不能说：

```text
final collapse 完全由 common 决定。
```

### 5.3 Common Subtraction / Offset Cancellation

推荐用更清楚的说法：

```math
z'_{f,e} = z_{f,e} - w_e^T c
```

含义：

```text
expert 仍然看到完整 hidden state；
router 不再使用 common component 诱导出来的 feature-independent offset。
```

这比 batch mean 或 SVD 更稳定，因为：

```text
batch mean 会随 batch composition 抖动；
SVD 可能去掉 task-relevant direction；
logit-level cancellation 只去掉数学模型中明确的 common-offset 项。
```

边界：

```text
它证明 common-offset 是 early mechanism，
但不是 final collapse 的完整解决方案。
```

---

## 6. Position Embedding / Template Source Issue

### Current Status

目前没有看到严格的 causal position ablation：

```text
1. 去除 position embedding 后训练 / step-0 audit；
2. 改变 feature 在 sequence 中的位置，看 common shift 和 collapse 是否仍出现。
```

因此 brief 中不能写：

```text
position embedding 是确定原因。
```

只能写：

```text
现有结果提示 common component 与 fixed routed position / template 有关，
但 position/template source 还需要 causal ablation。
```

### Prompt For System AI

```markdown
# Task: Position / Template Source Ablation For Common-Offset Collapse

## Goal

Test whether the hidden common component `c` in the uniform MoE toy setting is caused by fixed routed position / positional embedding / fixed sequence template.

Current known result:
- In baseline uniform data, step-0 hidden centroids have common component `c`.
- Common score `w_e^T c` predicts step-0 dominant expert.
- Logit-level common-offset cancellation reduces step-0 max-load close to random baseline.
- But we have not causally ablated position embedding or feature position.

Do not change the target rule or feature distribution unless explicitly stated.

---

## Experiment A: Step-0 Position Embedding Ablation

### Question

Does removing positional embedding reduce common ratio and step-0 load concentration before training?

### Variants

1. `baseline_pos`: original model, original position embedding.
2. `zero_all_pos_step0`: set all positional embeddings to zero before extracting step-0 hidden states.
3. `zero_routed_pos_step0`: only zero the positional embedding at the routed position.
4. `shuffle_pos_vectors_step0`: permute positional embedding vectors across sequence positions.

### Metrics

For each seed and slot pattern:

```text
common_ratio = ||mean_f h_f||^2 / mean_f ||h_f||^2
cos(c, pos_embedding_at_routed_position)
common_score_rank_of_dominant_expert
step0_max_load_full_hidden
step0_max_load_after_logit_cancel
```

### Interpretation

- If zeroing routed-position embedding strongly lowers common_ratio and step0_max_load, position embedding is a causal source.
- If common remains large, common also comes from template tokens / attention / residual stream.

---

## Experiment B: Train Without Positional Embedding

### Question

If position embedding is removed throughout training, does final collapse reduce?

### Variants

1. baseline full model.
2. no positional embedding from initialization and training.
3. optional: frozen zero position embedding but same architecture.

### Metrics

```text
step0_max_load
final_max_load
collapse_rate
target_accuracy
common_ratio over checkpoints
dominant_expert_persistence
```

### Boundary

If accuracy drops strongly, this does not cleanly prove collapse mechanism; it means position information was task-relevant.

---

## Experiment C: Randomize Feature Position In Sequence

### Question

If the same logical feature appears at variable sequence positions, does the common component tied to fixed routed position disappear?

### Construction

Keep feature distribution uniform and target rule unchanged.

Create variants:

1. `fixed_position_baseline`: original sequence order.
2. `random_feature_position_train_eval`: feature-bearing token / slot appears at random valid positions; model routes at the logical feature token, not a fixed absolute index.
3. `random_feature_position_eval_only`: train baseline, evaluate step-0 hidden geometry with randomized feature position, if implementation permits.

### Metrics

```text
count(feature_key) uniformity
count(position | feature_key)
common_ratio
cos(c, position_embedding)
step0_max_load
common_score agreement
final_max_load
target_accuracy
```

### Interpretation

- If randomizing feature position lowers common_ratio and step0 concentration while preserving accuracy, fixed position/template is a causal source.
- If common persists, inspect fixed template tokens, layernorm/residual mean, and attention aggregation.
```

---

## 7. Meeting Brief Guidance

### Recommended 6-Minute Structure

#### 0:00-0:40 Problem

```text
这轮没有继续扩展 feature assumption，而是回到 uniform baseline。
问题是：feature frequency 均匀、router random uniform 初始化、bias-free linear gate 下，为什么仍然 collapse？
```

#### 0:40-1:40 Mechanistic Model

```text
核心模型是 h_f = c + r_f。
虽然数据没有 common feature frequency bias，但 hidden state 有 across-feature common component c。
因此 bias-free gate 仍然有 effective expert bias: w_e^T c。
```

#### 1:40-3:00 Step-0 Evidence

```text
P1/P2: common-score w_e^T c predicts step-0 dominant expert，agreement 接近 1.0。
random baseline 是 0.25。
logit cancellation 后 step-0 max-load 接近 random/balanced range。
```

Conclusion:

```text
step-0 collapse seed 来自 common-offset，不是普通 random split。
```

#### 3:00-4:10 Training Dynamics

```text
P3/P5: cancellation 降低 hard collapse，accuracy 保持，但 final max-load 仍偏高。
P4: common-aware init 修复 step-0，但 final mixed。
所以 offset control 不等于 solve final collapse。
```

#### 4:10-5:00 Anti-Lockin + Utility Boundary

```text
P6A load-balance warmup 是当前最强 final-load control。
P7 显示 post-training route-utility match 高，所以不能说 router 最终选错 expert。
更合理说法是 early route assignment 和 expert utility co-adapt。
```

#### 5:00-6:00 Boundary + Next Decision

```text
Can claim:
common-offset 是 step-0 dominant expert 的强机制解释；
final collapse 需要 training-time amplification / anti-lockin 解释。

Cannot claim:
collapse 已解决；
load balance 等于 feature specialization；
position embedding 已被证明是 common 来源；
结果能直接推广到真实数据。

Next:
做 position/template causal ablation，
并 full 4-card verification: baseline / P5B / P4-I4 / P6A。
```

---

## 8. Suggested Meeting Brief Fill-In

```markdown
**Question:**
在 uniform feature frequency 和 bias-free random linear gate 下，为什么 step-0 routing 已经偏向某个 expert，并最终形成 collapse？

**Why this matters?**
如果 uniform baseline 的 route consistency 本身来自 common-offset seeded collapse，那么后续 feature specialization / route consistency 的解释都会被污染。

**Hypothesis:**
routed hidden state 可分解为 \(h_f=c+r_f\)。common component \(c\) 通过 \(w_e^\top c\) 产生 expert-specific effective bias，决定 step-0 dominant expert；final collapse 还需要 top-1 training amplification。

**Evidence:**
1. P1/P2: \(w_e^\top c\) predicts step-0 dominant expert; cancellation lowers step-0 max-load to near random/balanced range.
2. P3/P5/P4: offset control improves early geometry and hard collapse but final max-load remains high.
3. P6/P7: anti-lockin warmup gives strongest final-load control; final route utility is co-adapted, not simply utility-wrong.

**Cannot claim yet:**
common source has been causally identified;
collapse is solved;
load balancing implies feature specialization;
position embedding is the only source;
result transfers beyond this toy setting.

**Next Decision:**
position/template causal ablation + full 4-card verification of baseline, P5B, P4-I4, P6A.
```

---

## 9. Figures To Draw Next Morning

Need seed-level visual audit, not only averaged tables.

Recommended methods:

```text
baseline_full_hidden
P5B_logit_common_offset_cancel
P4_I4_residual_subspace_orthogonal
P6A_aux_load_balance_warmup
```

For each seed:

```text
step-0 route heatmap
final route heatmap
max-load trajectory
accuracy trajectory
```

Figure layout:

```text
row = seed
column = method
left panel = step 0
right panel = final
```

Each panel should annotate:

```text
max_load
entropy
dominant expert
accuracy
```

This answers:

```text
1. correction 是否修复 step-0？
2. correction 是否阻止 final re-concentration？
```

---

## 10. Next Decision And Next Iteration

### Next Scientific Decision

```text
验证 common component 的来源是否主要来自 fixed routed position / template，
并在 full 4-card setting 下确认 common-offset control 与 anti-lockin control 的作用边界。
```

### Minimal Next Experiments

```text
1. Position/template causal ablation:
   - no position embedding;
   - randomized feature position;
   - template perturbation.

2. Full 4-card verification:
   - baseline_full_hidden;
   - P5B_logit_common_offset_cancel;
   - P4_I4_residual_subspace_orthogonal;
   - P6A_aux_load_balance_warmup.

3. Seed-level route visualization:
   - step-0 corrected route map vs final route map.
```

### Decision Outcomes

```text
If P5B works nearly as well as P6A:
  common-offset control may be sufficient with better implementation.

If P6A clearly beats P5B/P4:
  final collapse is mainly training-amplified lock-in, not only initialization geometry.

If P6A balances load but destroys route structure:
  load balance is not enough; need feature-aware anti-lockin.

If all fail under full 4-card:
  shortened runs were insufficient; return to early dynamics audit.
```

---

## 11. Architecture / Algorithm Implications

Current results suggest four design directions.

### 11.1 Router Input Should Be Common-Controlled

```text
expert input = full hidden state
router input = common-controlled hidden state
```

This decouples expert computation from router decision.

### 11.2 Prefer Logit-Level Common Offset Cancellation

```math
z'_e = w_e^T h - w_e^T c
```

This is cleaner than batch mean or broad SVD removal because it directly targets the effective bias term.

### 11.3 Initialization Should Be Common-Aware

Goal:

```text
w_e^T c approximately equal across experts
```

or:

```text
w_e perpendicular to c
```

This prevents step-0 expert-specific bias from common direction.

### 11.4 Anti-Lockin Must Act During Early Training

P6A suggests final collapse is not solved only by step-0 geometry correction.

Need early training control:

```text
load-balance warmup
soft-to-hard routing schedule
dynamic expert bias
feature-aware anti-lockin regularization
```

But boundary remains:

```text
balanced load does not imply feature specialization.
```

---

## 12. Workflow Lessons

### What Improved

```text
1. 先写 minimal anchor，而不是直接接受 formal anchor。
2. 先做 code/data/init audit，再讲机制故事。
3. 开始区分 step-0 geometry 与 final training dynamics。
4. 开始把实验放进 purpose / hypothesis / metric / boundary 结构。
```

### What Still Needs Cleaning

```text
1. brief 中不要重复 Evidence / Current interpretation。
2. 不要把 position embedding 写成已证明原因。
3. P6/P7 是 training-control / utility-boundary，不要让它们抢走 root-cause 主线。
4. heatmap 只能作为 secondary evidence，primary metric 仍是 max-load / collapse rate / accuracy / common-score agreement。
5. 不要把 SVD subtraction 当作稳定 method；当前最干净的是 logit-level common-offset cancellation。
```

### Current Good Handoff Question For Mentor

```text
我现在把结果理解为：
common-offset 解释 step-0 dominant expert，
但 final collapse 还需要 training-time anti-lockin。
下一步我想先做 position/template causal ablation，
同时做 baseline/P5B/P4-I4/P6A 的 full verification。
这个 decision 是否合理？
还是应该先转向 forced-utility early dynamics？
```

---

## 13. Final Claim Boundary

### Can Claim Now

```text
In the uniform toy setting, common-score w_e^T c is a strong mechanism-level explanation for step-0 dominant expert.
Common-offset control reduces early load concentration and hard collapse while preserving task learning in shortened runs.
Final collapse still requires training-dynamics / anti-lockin explanation.
```

### Cannot Claim Yet

```text
common source is causally identified;
position embedding is the only source;
collapse is solved;
load balance equals feature specialization;
common subtraction is a deployable architecture method;
result generalizes to real data or full language models.
```