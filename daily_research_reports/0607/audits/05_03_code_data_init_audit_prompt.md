# 05_03 Code / Data / Initialization Audit Prompt

> 用途：把本 prompt 交给本地 AI / Codex / repo-side assistant，让它在代码仓库内审计：数据是否真 uniform、随机顺序是否正确、训练初始化是否可复现、Gating/router 初始化的数学形式是否与我们以为的一致。  
> 输出目标不是“猜测原因”，而是给出带文件路径、行号、代码片段和最小验证结果的 PASS / FAIL / UNCLEAR audit report。

---

## 0. Role And Scope

你是 repo-side 代码审计助手。请只围绕以下问题审计当前仓库，不要扩展到 unrelated refactor：

```text
在原始 uniform feature setting 下，top-1 MoE router 仍发生 collapse。
我们需要确认：
1. 数据生成是否真的 uniform；
2. 数据出现顺序 / batch 顺序是否真的随机；
3. 训练和 checkpoint 的 seed / 初始化是否正确；
4. 模型，特别是 Gating/router network 的初始化数学形式，是否与实验假设一致；
5. 是否存在 hidden common direction 的代码来源，例如 shared tokens、position embedding、bias、LayerNorm、template tokens、target position、embedding mean、router bias 等。
```

请先阅读：

```text
AGENTS.md
PROJECTS.md
当前 active project / worker surface 的 README 或 experiment protocol
当前 uniform MoE collapse 相关脚本、config、dataset、model、training loop、analysis scripts
```

不要改代码，除非我明确要求。可以新建临时 audit script，但必须说明路径和用途。

---

## 1. Expected Output Format

请输出一个 markdown audit report，结构如下：

```markdown
# Uniform MoE Collapse Audit Report

## Executive Verdict
- data_uniformity: PASS / FAIL / UNCLEAR
- sequence_randomization: PASS / FAIL / UNCLEAR
- seed_reproducibility: PASS / FAIL / UNCLEAR
- model_initialization: PASS / FAIL / UNCLEAR
- router_gating_initialization: PASS / FAIL / UNCLEAR
- hidden_common_direction_sources: PASS / FAIL / UNCLEAR
- conclusion: bug / no bug found / insufficient evidence

## Evidence Table
| Item | Verdict | File:Line | Evidence | Why It Matters |
|---|---|---|---|---|

## Minimal Reproduction Commands
...

## Quantitative Checks
...

## Risks / Ambiguities
...

## Recommended Minimal Fix Or Next Audit
...
```

每个判断必须有：

```text
file path + line number + relevant code snippet + actual value / printed statistic
```

不要只写“看起来没问题”。

---

## 2. Data Generation Audit

### 2.1 Identify The Exact Dataset Builder

找到原始 uniform feature setting 的 dataset / dataloader / generator。给出：

```text
- dataset class / function name
- config name
- command or script used by original experiment
- train / validation / analysis split 的生成方式
- 是否每个 epoch 动态采样，还是预先生成固定数据集
```

### 2.2 Verify The Intended Data Form

确认原始 setting 是否真的是：

```text
x_{s,i,r} = [r_start, C_s, B_i, Y_{s,i}, r_end]

s: slot / context feature, intended uniform
B_i: identity token, intended uniform
r: nuisance variant, should not determine target
Y_{s,i}: target determined by (C_s, B_i)
operational feature key: (s, i)
```

请检查：

```text
- C_s 的数量 F_s 是多少？
- B_i 的数量 F_i 是多少？
- operational feature key (s, i) 的总数是多少？
- nuisance r 的数量是多少？
- r_start / r_end 是否固定 token？是否所有样本都有？
- target Y 是否完全由 (s, i) 决定？
- 是否存在某些 token / position 永远共享，可能引入 common component？
```

### 2.3 Uniformity Counts

写一个 audit script 或使用现有 script，生成足够多样本，例如：

```text
N = max(100000, 1000 * num_features)
```

输出以下计数和偏差：

```text
count(s)
count(i)
count(r)
count(Y)
count(s, i)
count(s, i, r)
count(batch_id, s)
count(batch_id, i)
count(epoch, s)
count(epoch, i)
```

报告：

```text
- max_abs_deviation_from_uniform
- max_relative_deviation_from_uniform
- chi-square statistic / p-value, if straightforward
- KL(empirical || uniform)
- min_count / max_count ratio
```

判定：

```text
PASS: sampling distribution 与 uniform 符合，偏差只在 finite sample noise 内。
FAIL: 某些 feature / pair / nuisance 明显系统性偏高或偏低。
UNCLEAR: 代码路径无法确认，或 sample size 不足。
```

### 2.4 Random Order / Batch Order

确认不是只在 global counts uniform，而是在训练顺序中也足够随机。

检查：

```text
- dataset 是否 shuffle
- dataloader shuffle=True/False
- sampler 是否固定顺序
- distributed sampler 是否 set_epoch
- batch 内是否存在排序 pattern
- epoch-to-epoch order 是否复用
- train/analysis checkpoint 取样是否固定 subset
```

输出：

```text
- first 100 samples 的 (s, i, r, Y)
- 每个 batch 的 feature entropy 分布
- adjacent pair autocorrelation: P(s_t = s_{t+1}), P(i_t = i_{t+1})
- run 之间同 seed / different seed 的 order hash
```

判定：

```text
PASS: 顺序随机，batch-level 不出现周期性或 deterministic block。
FAIL: 出现按 feature 排序、按 target 排序、周期性 block、或多 epoch 复用同一顺序且会影响训练。
```

### 2.5 Target Leakage / Shortcut Check

检查是否存在非 intended feature 也能预测 target：

```text
- r_start / r_end 是否编码 target family？
- nuisance r 是否与 target 或 slot 相关？
- sample index / position / batch id 是否间接决定 target？
- token id 分配是否把 C_s、B_i、Y_{s,i} 按连续区间排列，导致 embedding 初始化或 output head tying 产生 shared axis？
```

输出一个简单 baseline：

```text
Predict Y from s only
Predict Y from i only
Predict Y from r only
Predict Y from position / index only
Predict Y from (s, i)
```

如果 r 或 order 能预测 Y，标记 FAIL。

---

## 3. Seed And Reproducibility Audit

### 3.1 Seed Setting

列出所有 seed 控制点：

```text
python random
numpy
torch CPU
torch CUDA
dataloader worker_init_fn
distributed sampler seed
model init seed
dataset generation seed
analysis seed
```

检查：

```text
- seed 是否在模型初始化前设置
- seed 是否在 dataset 生成前设置
- 不同 seeds 是否真的改变 model init 和 data order
- same seed 是否能复现 step-0 router weights / first batch / final metrics
```

输出：

```text
hash(first_100_samples)
hash(router_weight_step0)
hash(expert_weight_step0)
hash(training_config)
```

### 3.2 Checkpoint Semantics

确认 step 0 是：

```text
A. model initialized, no optimizer step yet
B. after first forward/backward, before optimizer step
C. after first optimizer step
D. unclear
```

这直接影响“step 0 early geometry”的解释。

---

## 4. Model Initialization Audit

### 4.1 Embedding / Positional / Transformer Initialization

列出并解释：

```text
- token embedding init distribution
- position embedding init distribution
- output head tying or not
- LayerNorm affine init
- residual stream init conventions
- attention / FFN init distribution
- expert FFN init distribution
- router/gate init distribution
```

对每一类参数输出：

```text
shape
mean
std
min / max
norm distribution
whether bias exists
whether bias initialized nonzero
```

### 4.2 Router / Gating Network Exact Math

找到 gating/router class。确认数学形式：

```text
h: router input hidden state
W: router weight, one vector per expert
b: router bias, if any
z_e = <w_e, h> + b_e
p_e = softmax(z / temperature)_e, if soft routing is used
selected expert e* = argmax_e z_e or argmax_e p_e
```

必须确认：

```text
- router 是 nn.Linear(d_model, num_experts) 还是手写参数？
- weight shape 是 [num_experts, d_model] 还是 [d_model, num_experts]？
- bias=True/False？
- 如果用 PyTorch default nn.Linear，初始化是否为 kaiming_uniform with bound 1/sqrt(fan_in)？
- 是否有 custom init，例如 normal_(0, std)、xavier、orthogonal、zero init？
- 是否有 router temperature、noise、jitter、dropout？
- 是否有 top-k、top-1、straight-through、detach、stop-gradient？
- 是否有 load-balance loss、router z-loss、capacity factor、auxiliary loss？
- inhibition 的实现在哪里？它更新的是 expert input、router logits、expert hidden，还是 loss？
```

输出 router 初始化的实际统计：

```text
W_e norm per expert
b_e per expert
pairwise cosine(w_e, w_k)
row mean vector norm ||mean_e w_e||
max logit expert on random hidden states
max logit expert on feature centroids, if available
```

判定：

```text
PASS: router init 与实验假设一致，且无 hidden bias / unintended temperature / unintended loss。
FAIL: 存在 bias、custom init、wrong shape、temperature、detach、loss term 或 checkpoint semantics 与假设不一致。
UNCLEAR: router path 多分支，无法确认实际运行路径。
```

---

## 5. Step-0 Random Geometry Audit

在训练前，采样原始 uniform data，并 forward 到 router input hidden states。

### 5.1 Hidden State Centroids

定义 routing position 的 hidden state：

```text
h_{s,i,r} = hidden state seen by router before predicting Y_{s,i}
h_f = mean_r h_{s,i,r}, where f=(s,i) or chosen feature key
c = mean_f h_f
u_f = h_f - c
```

输出：

```text
||c||
mean_f ||h_f||
mean_f ||u_f||
common_ratio = ||c|| / mean_f ||h_f||
variance explained by c or first PC
pairwise cosine(h_f, h_g)
pairwise cosine(u_f, u_g)
```

解释：

```text
如果 data counts uniform，但 c 很大，这说明 uniformity 不等于 hidden representations zero-mean。
```

### 5.2 Router Score Decomposition

对每个 expert e：

```text
z_{f,e} = w_e^T h_f + b_e
        = w_e^T c + w_e^T u_f + b_e
```

输出：

```text
common_score_e = w_e^T c + b_e
residual_score_{f,e} = w_e^T u_f
for each feature f: top1 expert using full z
for each feature f: top1 expert using residual only
expert load from full z
expert load from residual-only z
```

关键判定：

```text
If full-z load is concentrated but residual-only load is balanced:
  common component is a strong route-collapse candidate.
If both full-z and residual-only load are concentrated:
  finite random geometry / router init / feature residual anisotropy may be enough.
If neither concentrated at step 0 but final collapses:
  training amplification is dominant.
```

### 5.3 Compare To Random Geometry Baseline

构造理论 / Monte Carlo baseline：

```text
F = number of operational features
E = number of experts
d = router input dimension
Sample h_f ~ N(0, I_d), w_e ~ actual init distribution or N(0, sigma^2 I_d)
Compute argmax_e w_e^T h_f
Repeat >= 100000 trials
```

报告：

```text
expected max_load
P(max_load >= observed_step0_max_load)
P(all features assigned to one expert)
P(final-dominant step0 load >= observed)
expected top1 margin distribution
p-value for observed step0 margin
```

注意：如果 F 很小，例如 F=4, random top-1 assignment 本身不保证 perfect 1-1 split。请不要把“数据均匀”误解为“每个 expert 必然获得相同 feature 数”。

---

## 6. Training Loop / Gradient Routing Audit

### 6.1 Which Parameters Receive Gradients?

确认 top-1 routing 下：

```text
- selected expert 是否接收 expert loss gradient
- non-selected experts 是否接收任何 expert gradient
- router 是否接收 gradient；如果接收，是来自 softmax、straight-through、aux loss、inhibition，还是其他 surrogate？
- expert choice 是否 detach
- inhibition 是否只作用 selected expert
```

输出：

```text
At step 0 / 1 / 10:
  grad norm of router W by expert row
  grad norm of expert parameters by expert
  load fraction by expert
  change ||w_e(t)-w_e(0)|| by expert
```

### 6.2 Selected-Expert Self-Reinforcement Check

如果某 expert step-0 load 高，检查：

```text
- 它是否获得更大 gradient norm
- 它的 expert loss 是否更快下降
- router vector 是否更靠近 common direction
- top-1 margin 是否增加
```

输出：

```text
corr(load_e(t), grad_norm_e(t))
corr(load_e(t), ||w_e(t)-w_e(0)||)
corr(load_e(t), alignment(w_e(t), c(t)))
```

---

## 7. Anti-Lockin Candidate Audit

只做代码层面可行性确认，不要先大规模跑：

```text
A. common-direction subtraction before routing
   h_route = h_full - proj_c(h_full)
   expert input remains h_full

B. early load balancing / router warmup
   add or strengthen load-balance loss only during early steps

C. delayed hard top-1
   train with soft routing or higher temperature for first N steps, then hard top-1

D. router initialization change
   zero bias, row-centered router weights, orthogonal rows, matched norm, optional feature-centroid-aware init
```

对每个候选给出：

```text
- required code location
- minimal config switch
- risk / confound
- primary metric affected
```

---

## 8. Final Questions You Must Answer

请用 evidence 回答以下问题：

```text
Q1. 原始 uniform data 是否真 uniform？如果是，uniform 到哪个变量层级？s, i, r, target, pair, order, batch?
Q2. 数据顺序和 batch 顺序是否随机？是否存在 block ordering?
Q3. step 0 checkpoint 是否真训练前？
Q4. Gating/router 的初始化数学形式是什么？W, b, temperature, top-k, bias, init distribution 分别是什么？
Q5. router bias 是否存在？如果存在，是否可能作为 common logit offset 导致 load concentration？
Q6. token embedding / position embedding / shared template tokens 是否产生 nonzero common hidden direction？
Q7. step-0 full hidden load concentration 是否超过 random geometry baseline？
Q8. residual-only routing 是否明显更均匀？
Q9. 训练早期是否存在 selected-expert self-reinforcement？
Q10. 如果未发现 bug，最小 anti-lockin intervention 应该优先实现哪一个？
```

---

## 9. Do Not Over-Claim

不要输出这些结论，除非有直接证据：

```text
- collapse 已经被完全解释。
- common direction 是唯一因果原因。
- inhibition 一定有害。
- router 选错 expert。
- 结果可推广到 compositional / Zipf / real data。
```

可以输出：

```text
- data uniformity PASS/FAIL。
- initialization 与假设一致/不一致。
- step-0 imbalance 是否超出 random finite-sample baseline。
- common component 是否能解释 step-0 load concentration。
- 哪个最小 anti-lockin variant 最适合下一步测试。
```
