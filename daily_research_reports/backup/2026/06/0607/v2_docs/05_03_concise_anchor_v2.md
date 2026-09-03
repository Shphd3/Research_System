---
parent_node: ordinary_top1_moe_route_consistency
anchor_id: 05_03_uniform_collapse_common_offset
status: draft_for_anchor_audit
---

# 05_03 Uniform MoE Collapse: Common Offset vs Random Initialization

## researcher judgment record

**父问题：** ordinary top-1 MoE router 在 NTP 训练中形成的 route consistency，是否代表 feature-level routing / expert specialization？

**当前子问题：** 在最简 uniform feature setting 下，为什么 bias-free linear gate 仍然发生 route collapse？

**为什么现在问：** 之前的 feature-assumption relaxation 被 collapse 强干扰。代码审计已经初步排除 slot 频率不均、训练顺序错误、router 随机初始化错误作为主因；更强的候选是 hidden representation 中存在 shared/common component。

**决策问题：** 在 verified uniform data 和 verified random router init 下，collapse 是否主要来自 hidden common component 通过 linear gate 产生的 expert-specific common offset？如果是，去除或控制这个 offset 是否能减少 collapse，同时保持 target learning？

**当前最短判断：** 随机初始化本身可能是正确的，但当 `h = c + r_f` 且 `c` 很大时，随机 router row 的 `w_e^T c` 会变成 expert-specific effective bias；top-1 训练再把这个早期 bias 放大成 lock-in。

**下一步：** 只做 anchor-linked minimal tests：common-source perturbation、multi-seed common-score audit、common-offset cancellation / residual routing、common-aware initialization。

## 1. Problem Definition

### Broader question

```text
ordinary top-1 MoE router 学到的是 feature-level specialization，还是 collapse / shortcut / early lock-in？
```

### Sharper question

```text
在原始 uniform feature setting 下，linear top-1 router 为什么不能自然均匀分发？
```

### Decision question

```text
hidden common component 是否通过 w_e^T c 形成 expert-specific common offset，并成为 collapse 的主要 early driver？
```

### Boundary of this anchor

This anchor only studies:

```text
uniform feature data
linear router / top-1 routing
step-0 to early training geometry
common component intervention before routing
```

This anchor does **not** answer:

```text
compositional feature routing
Zipfian feature frequency
real data
full LM behavior
whether selected expert is utility-optimal
whether anti-lockin is solved in general
```

## 2. Operational Definitions

**Uniform data**

```text
slot / intended operational feature is uniform in train and eval.
Exact (slot, B) may be finite-sample noisy in fixed train set but should be exactly uniform in diagnostic grid.
```

**Common component**

```text
c = E_f[h_f]
```

A direction is decision-relevant common component only if:

```text
1. it explains a large fraction of hidden centroid norm / variance;
2. router load decreases after removing or equalizing its contribution;
3. its source can be tied to data/model construction, not just post-hoc SVD.
```

**Collapse**

```text
One expert receives a large majority of feature centroids / tokens across early or final checkpoints.
Operational metrics: max_load, load_entropy, dominant_expert_persistence, top1_margin.
```

**Common-offset score**

```text
a_e = w_e^T c
```

If `argmax_e a_e` predicts the dominant expert across seeds and conditions, the common-offset hypothesis is supported.

## 3. Physical Priors

### Prior P1: Uniform frequency does not imply zero-mean representation

Uniform slot frequency removes frequency imbalance, but does not remove fixed position embeddings, fixed template tokens, residual-stream offsets, or attention-induced shared components.

### Prior P2: Linear routing is sensitive to shared offsets

For a linear router,

```text
z_e(h_f) = w_e^T h_f = w_e^T c + w_e^T r_f.
```

If `|w_e^T c - w_j^T c|` is comparable to or larger than feature residual differences, top-1 routing will prefer the same expert for many features.

### Prior P3: Top-1 routing can amplify early bias

Hard selection gives more gradient and utility updates to already-selected experts. A small initial load advantage can become high-margin lock-in unless the training dynamics or objective provides a correction pressure.

## 4. Mechanistic Hypothesis

### Main hypothesis

```text
H_common_offset:
Uniform data still produces h_f = c + r_f, where c mainly comes from fixed routed-position/template structure.
Random bias-free router rows produce unequal common scores a_e = w_e^T c.
The expert with largest a_e receives many features at step 0.
Top-1 training then amplifies this into collapse.
```

### Rival explanations

```text
R1. Hidden common component exists but is not causal; collapse is mainly from expert utility dynamics.
R2. Collapse is caused by a remaining data / order / target leakage artifact not captured by the first audit.
R3. Random finite-sample geometry alone can explain load imbalance.
R4. Initialization scale or row geometry is the main driver even after controlling common offset.
R5. Common subtraction balances routing but destroys task learning, meaning c also carries necessary task signal.
```

### What would change my mind

```text
1. argmax_e w_e^T c does not predict step-0 or final dominant expert across seeds.
2. Removing / equalizing common offset does not reduce early max_load or final collapse.
3. Data variants that weaken the measured common source do not weaken collapse.
4. Forced-routing utility shows the dominant expert is consistently utility-best for all features.
```

## 5. Mathematical Modeling

Let feature centroid hidden state be:

```text
h_f = c + r_f + epsilon_f
```

where:

```text
c: feature-shared component
r_f: feature-specific residual
epsilon_f: nuisance / sampling noise
W = [w_1, ..., w_E]^T: router matrix
z_e(f) = w_e^T h_f
```

Decompose routing logit:

```text
z_e(f) = a_e + b_e(f)
a_e = w_e^T c
b_e(f) = w_e^T r_f
```

Common-offset-driven collapse occurs when:

```text
max_e a_e - secondmax_e a_e
```

is large enough that the same expert wins for many `f`, despite feature residual variation.

A direct correction is therefore not necessarily “subtract hidden mean from all computation”; it can be:

```text
z'_e(f) = z_e(f) - w_e^T c
```

or equivalently route on:

```text
h'_route = h - proj_U(h)
```

while experts still receive full `h`.

## 6. Computational Realization

### Baseline

```text
original uniform feature data
same seeds as previous audit
same model/training except explicit intervention variable
router input = full hidden state
expert input = full hidden state
```

### Intervention principle

Only change what the router sees or how router rows interact with `c`.

```text
router input / logits: modified
expert input: unchanged
training target: unchanged
data distribution: unchanged unless testing common source
```

This isolates routing shortcut from task computation.

## 7. Minimal Falsifiable Tests

### Test 1: Common-source perturbation

Change one construction factor that is hypothesized to create `c`, such as fixed routed position / template component. Measure whether `common_ratio`, `cos(c, source)`, and step-0 max_load decrease.

### Test 2: Multi-seed common-score audit

Across seeds, compute:

```text
c_0
w_e^T c_0
step0 dominant expert
final dominant expert
max_load trajectory
```

Primary question: does `argmax_e w_e^T c_0` predict dominant expert better than random?

### Test 3: Common-offset cancellation / residual routing

Compare baseline against:

```text
z'_e = w_e^T h - w_e^T c
```

or:

```text
h_route = h - proj_c(h)
router logits = W h_route
expert input = h
```

Primary question: does collapse decrease without target accuracy loss?

### Test 4: Common-aware initialization

Initialize router rows so:

```text
w_e^T c = constant across experts
```

preferably zero, with row norms preserved. Then compare step-0 load and final collapse against default PyTorch random init.

## 8. Falsifiable Outcomes

### Supported if

```text
1. data/init audit remains PASS;
2. common score argmax predicts dominant expert across seeds;
3. weakening common source reduces common ratio and early max_load;
4. common-offset cancellation or common-aware init reduces collapse;
5. target accuracy remains near baseline.
```

### Weakened if

```text
1. common score does not predict dominant expert;
2. common-source perturbation weakens c but collapse remains unchanged;
3. common-offset cancellation does not change max_load / entropy / persistence;
4. initialization fixes load without controlling common offset.
```

### Redirected if

```text
1. common control balances routing but hurts target accuracy;
2. forced-routing utility shows one expert is truly best for most features;
3. early load spike sometimes recovers under matched common score, implying lock-in dynamics rather than common offset is primary.
```

### Still not proven if

```text
Only heatmaps look cleaner.
Only one seed improves.
Only step-0 load improves but final collapse remains.
Only target accuracy is preserved without route structure improvement.
```

## 9. Current Evidence

Current audit supports the following limited claims:

```text
1. Slot-level data uniformity and training order look correct.
2. R* router uses random bias-free PyTorch Linear initialization.
3. A large step-0 hidden common component exists.
4. Removing the mean/common component makes step-0 load much closer to random baseline.
5. The common direction aligns mainly with fixed routed-position/template source, not feature frequency.
6. Early selected-expert load and router-row gradient can self-reinforce.
```

Current audit does not prove:

```text
1. common direction is the only cause;
2. common subtraction will fix training;
3. router-selected expert is utility-wrong;
4. results generalize beyond this toy setting.
```

## 10. Claim Boundary And Next Decision

### Safest current claim

```text
In the audited uniform toy setting, collapse is not explained by slot-frequency imbalance or a router initialization bug. The strongest current mechanism is that a shared hidden component creates expert-specific common offsets under random linear routing, and top-1 training can amplify this early imbalance.
```

### Next decision

```text
Run the minimal common-offset intervention.
If it reduces early/final collapse while preserving target accuracy, advance to anti-lockin and common-aware initialization.
If it fails, redirect to expert-utility / top-1 dynamics / load-balancing warmup.
```

## Appendix A. What We Are Not Doing In This Iteration

We are intentionally **not** doing the following, because the current mechanism is not yet aligned enough:

```text
1. Not continuing P1/P3/P2 feature-assumption relaxation.
   Reason: those results are not interpretable until baseline collapse is explained.

2. Not claiming common direction is already the root cause.
   Reason: current evidence is strong correlation plus step-0 residual diagnostic, not full causal training intervention.

3. Not using unstable per-batch mean subtraction or broad SVD removal as the main claim.
   Reason: they can change task signal and produce hard-to-interpret instability.

4. Not changing data construction and router intervention in the same experiment.
   Reason: that would confound common-source diagnosis with anti-collapse correction.

5. Not treating “better load balance” as “better specialization.”
   Reason: balanced routing can be arbitrary bucketing unless it preserves target learning and feature-specific structure.

6. Not doing a broad literature review before the minimal tests are queued.
   Reason: this iteration needs a yes/no mechanism decision, not a survey.

7. Not claiming real-data applicability.
   Reason: the current common component is tied to a controlled toy construction.
```

## Appendix B. One-Minute Alignment Check

Before running or reporting, answer these five questions:

```text
1. What is the one decision question?
   Does common-offset control reduce collapse in verified uniform data?

2. What is the physical phenomenon?
   Uniform feature frequency still yields nonzero shared hidden component; linear gate converts it into expert-specific offset.

3. What is the primary metric?
   step0-50 max_load / load_entropy / dominant persistence, plus final collapse rate and target accuracy.

4. What would falsify the claim?
   common score does not predict dominant expert, or common-offset control does not reduce collapse.

5. What is the next action after result?
   If supported: common-aware init / stable anti-lockin. If weakened: expert-utility and top-1 dynamics audit.
```
