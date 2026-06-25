---
parent_node: ordinary_top1_moe_route_consistency_and_specialization
anchor_id: 05_03_collapse_root_cause_and_antilockin
status: draft_for_next_iteration
created_from: research_handoff_0605 + 0605 mentor transcript + meeting_brief_cn
---

# 05_03 Collapse Root-Cause And Anti-Lockin Anchor

## Thinking Card

父问题：

```text
ordinary top-1 MoE router 在 NTP 训练下形成的 route consistency，
到底是不是有意义的 feature-level routing / expert specialization？
```

当前子问题：

```text
在原始 uniform feature setting 中，为什么 top-1 MoE router 仍然频繁 route collapse？
根因更接近：
1. 数据 / 代码并非真正 uniform 或随机；
2. random initialization / finite random geometry 的自然不均衡；
3. hidden-state common component 被 linear router 捕获；
4. top-1 / selected-expert training 把 early bias 放大成 lock-in；
5. 以上因素的组合。
```

为什么要问这个问题：

```text
之前 inhibition 在 non-collapsed seeds 中提高 same-feature consistency，
但多数 seeds 出现 collapse，且 inhibition 有放大 collapse 的趋势。
这使 P1/P3/P2 的 feature-assumption relaxation 结果无法解释为可靠 feature-level specialization。
导师追问的核心是：如果 data uniform，feature/router/expert vectors 都随机初始化，为什么仍然不均匀分发？
```

决策问题：

```text
在 verified uniform data + correct initialization 下，
collapse 是否主要来自 hidden-state common component 被 router 放大？
如果是，去除或控制 common component 是否能减少 collapse，同时保持 target learning？
如果不是，collapse 是否更应归因于 random geometry finite-sample imbalance、router/expert initialization、或 top-1 utility lock-in？
```

任务构造：

```text
只回到原始 uniform feature data、原始 seeds、原始 checkpoints。
先做 code/data/init sanity audit，再做 random geometry baseline，
然后做 common-direction residual routing intervention。
anti-lockin variants 只作为下一步候选，不先扩展成大 sweep。
```

当前结果 / 预期结果：

```text
已有 audit 表明：final collapse expert 在 early routing geometry 中可见；
step-0 margin 不大但训练后显著增大；
collapse expert 最终高度对齐 global common hidden direction。
但 common direction 尚未被因果干预证明，也未排除数据/初始化实现问题。
```

结论边界：

```text
能声称：collapse 是当前主线 boundary；early geometry 和 training amplification 都重要；common direction 是强机制候选。
不能声称：collapse 已解决；common direction 是唯一原因；inhibition 一定有害；router 选择与 utility-best expert 错配；结论可推广到 compositional / Zipf / real data。
```

下一步：

```text
1. 用 code/data/init audit prompt 审计源代码和实验配置；
2. 建立 random geometry finite-sample baseline；
3. 做 common-direction residual routing：router 看 h - proj_c(h)，expert 仍看 full h；
4. 若 residual routing 不足，转向 top-1 warmup / load balance / better initialization / forced utility matrix。
```

---

## 1. Problem Definition

### 1.1 Broader Question

```text
ordinary top-1 MoE router 在 NTP 训练下形成的 same-feature route consistency，
是否代表有意义的 feature-level routing / expert specialization？
```

### 1.2 Current Sharper Question

```text
在未放松 assumptions 的原始 uniform feature setting 中，
为什么 top-1 routing 仍然发生 collapse？
```

### 1.3 Decision Question

```text
collapse 是 primarily:
A. code/data construction artifact;
B. random initialization / finite random geometry;
C. hidden common direction shortcut;
D. training-amplified top-1 lock-in / expert utility feedback;
E. insufficient evidence?
```

### 1.4 What We Do Not Need To Do Now

```text
不继续扩大 P1/P3/P2 feature-assumption relaxation。
不做 compositional token generalization。
不做 Zipf frequency claim。
不做 real data claim。
不证明 expert utility specialization。
不先设计 hierarchy / H-MoE 大方案。
```

### 1.5 Operational Definitions

```text
uniform data:
  s, i, r, target Y, operational feature key (s,i), batch/order 层面的 empirical distribution
  与 intended uniform distribution 一致；没有 target leakage 或 deterministic block ordering。

collapse:
  final routing load highly concentrated in one expert，例如 max_load_fraction 超过预设 hard-collapse threshold；
  同时 load entropy 低，且多数 features/tokens route to same expert。

step-0 early geometry:
  optimizer update 前，router input hidden states h_f 与 router vectors w_e 形成的 score/order structure。
  必须确认 checkpoint step 0 是否真为训练前。

common direction:
  routing hidden centroids 的 shared component：
  c = mean_f h_f 或 top principal direction；
  它对多个 features 提供 shared logit offset w_e^T c + b_e。

random geometry baseline:
  在 F features、E experts、d dimensions、matched init distribution 下，
  random h_f 和 random w_e 的 top-1 load / margin 分布。

training-amplified lock-in:
  step-0/early load advantage 不大，但 top-1 margin、dominant expert load、router alignment 在训练中持续增大。

anti-lockin:
  能减少 final hard collapse、打散 step 0-50 dominant expert lock-in、保持 target accuracy，
  并不破坏 non-collapsed seeds 的 slot-level expert composition 的最小机制。
```

---

## 2. Physical Priors

### Prior 1: Uniform Frequency Removes One Explanation, Not All Explanations

```text
如果 s/i/r/counts 是 uniform，只能排除 feature frequency imbalance。
它不能保证 hidden states zero-mean，也不能保证 router scores uniform。
```

可被削弱：

```text
如果 code audit 发现数据/顺序不是 uniform，则当前 mechanism audit 必须退回 code/data bug。
```

### Prior 2: Random Top-1 Geometry Does Not Guarantee Perfect Partition

```text
即使 h_f 与 w_e 都是随机 isotropic，top-1 assignment 也是 finite-sample multinomial。
F 小时 natural imbalance 并不罕见。
```

可被削弱：

```text
如果 observed step-0 concentration 显著超过 matched random baseline，
纯 random finite-sample explanation 不够。
```

### Prior 3: Common Hidden Component Can Create Feature-Independent Expert Advantage

```text
如果 h_f = c + u_f，router score 为 z_{f,e}=w_e^T c + w_e^T u_f + b_e。
其中 w_e^T c + b_e 是所有 features 共享的 expert-specific offset。
某个 expert 在这个 offset 上占优时，会吸收多个 features。
```

可被削弱：

```text
如果 ||c|| 很小，或 residual-only routing 仍同样 collapse，
则 global common direction 不是主要解释。
```

### Prior 4: Gate Learns Expert Responsibility, Not Feature Identity By Default

```text
NTP gate 的直接训练信号不是“feature identity should split”，
而是哪个 expert 对正确 token 更有 posterior responsibility / utility。
如果同一个 expert 对多个 features 都更好或更早学会，gate 有理由把它们合并。
```

可被削弱：

```text
如果 forced-routing utility matrix 显示 collapsed expert 并没有 higher responsibility，
则需要解释 router 为什么偏离 utility；否则不能声称 router 选错。
```

### Prior 5: Hard Top-1 Can Create Hysteresis

```text
被 early geometry 选中的 expert 获得更多 token 和 gradient；
非选中 expert 缺少相同训练机会；
small advantage 可以被训练放大为 high-margin lock-in。
```

可被削弱：

```text
如果 early load spike 经常自动 recovery，或 soft/warmup 不改变 collapse rate，
则 lock-in 不是充分解释。
```

---

## 3. Mechanistic Motivation

### 3.1 Why The Mentor's Question Matters

导师追问不是“common direction 这个词对不对”，而是：

```text
在 data uniform、features random、router/expert vectors random 的最基础设定下，
为什么不能自然分茅列土？
```

这个问题必须拆成三个可判定层次：

```text
Layer 1: data/code 层面是否真 uniform / random？
Layer 2: 即使真 uniform，random top-1 geometry 的 finite-sample baseline 是否本来就可能不均匀？
Layer 3: hidden-state geometry 是否有 common component，使某 expert 获得 feature-independent offset？
Layer 4: training 是否把 Layer 2/3 的 small advantage 放大？
```

### 3.2 Rival Explanations

| Rival explanation | What it predicts | How to test |
|---|---|---|
| Data not truly uniform | count/order/target leakage abnormal | source-code + count audit |
| Step-0 checkpoint not truly pre-training | early geometry already includes training | checkpoint semantics audit |
| Router bias/init mismatch | same expert wins via bias/norm | router W/b stats and score decomposition |
| Finite random geometry | step-0 load within random baseline | Monte Carlo matched baseline |
| Common hidden direction | full routing concentrated; residual-only balanced | h = c + residual score decomposition |
| Top-1 training amplification | small step-0 margin grows over steps | load/margin dynamics |
| Expert utility shared dominance | same expert has higher responsibility across features | forced-routing utility matrix |
| Inhibition-specific artifact | collapse only under inhibition | matched with/without inhibition seeds |
| No causal common component | residual routing does not reduce collapse | common-direction residual routing |

### 3.3 Mainline Impact

```text
affects hypothesis? yes
  It decides whether same-feature consistency can be interpreted beyond collapse.

affects claim boundary? yes
  Without root-cause audit, we cannot claim feature-level specialization.

affects next decision? yes
  It determines whether next intervention should be residual routing, init change, load balance, or data fix.

recommendation: pursue now
  This is the current bottleneck before any feature-assumption relaxation.
```

---

## 4. Mathematical Model
### 4.1 Objects

```text
F: number of operational features, e.g. f=(s,i)
E: number of experts
d: router input dimension
h_f(t): routing hidden centroid for feature f at checkpoint t
w_e(t): router vector for expert e at checkpoint t
b_e(t): router bias for expert e, if any
z_{f,e}(t): router logit
c(t): common hidden direction / mean centroid
u_f(t): feature residual
```

### 4.2 Linear Router

\[
z_{f,e}(t)=w_e(t)^\top h_f(t)+b_e(t)
\]

\[
e^*(f,t)=\arg\max_e z_{f,e}(t)
\]

### 4.3 Common / Residual Decomposition

\[
c(t)=\frac{1}{F}\sum_f h_f(t)
\]

\[
u_f(t)=h_f(t)-c(t)
\]

\[
z_{f,e}(t)=\underbrace{w_e(t)^\top c(t)+b_e(t)}_{\text{common expert offset}}+
\underbrace{w_e(t)^\top u_f(t)}_{\text{feature-specific residual score}}
\]

Core test:

```text
If full score routes to one expert but residual score routes more evenly,
common direction is sufficient to explain early concentration.
```

### 4.4 Random Geometry Baseline

Assume:

\[
h_f \sim \mathcal{N}(0,I_d), \quad w_e \sim \mathcal{N}(0,\sigma^2 I_d)
\]

Then by symmetry:

\[
P(e^*(f)=e)=\frac{1}{E}
\]

and load vector:

\[
(n_1,\dots,n_E)\sim \mathrm{Multinomial}\left(F; \frac{1}{E},\dots,\frac{1}{E}\right)
\]

Metrics:

```text
P_random(max_load >= observed max_load)
P_random(step0_margin >= observed margin)
P_random(final_dominant_step0_load >= observed)
```

Interpretation:

```text
If observed step-0 imbalance is within baseline, random geometry may explain early identity but not necessarily final training amplification.
If observed imbalance is far beyond baseline, hidden anisotropy / bias / init mismatch must be investigated.
```

### 4.5 Gate Responsibility Theory

For soft mixture, let:

\[
R_{i,e}=P_e(y_i|x_i)
\]

\[
L_i=-\log\sum_e g_e(x_i)R_{i,e}
\]

Define posterior responsibility:

\[
\rho_{i,e}=\frac{g_e(x_i)R_{i,e}}{\sum_k g_k(x_i)R_{i,k}}
\]

Then:

\[
\frac{\partial L_i}{\partial z_e}=g_e(x_i)-\rho_{i,e}
\]

Thus gradient descent pushes gate probability toward expert responsibility.

Boundary:

```text
This explains why feature identity alone does not force split.
To claim utility mismatch, we need forced-routing utility matrix.
```

### 4.6 Top-1 Lock-In Dynamics

Let \(l_e(t)\) be expert load and \(m(t)\) be mean top-1 margin.

A lock-in pattern is:

\[
l_j(0)>\frac{1}{E}, \quad m(0) \text{ small}
\]

but later:

\[
l_j(t)\rightarrow 1, \quad m(t)\uparrow, \quad \cos(w_j(t),c(t))\uparrow
\]

This is not pure initialization; it is early geometry plus training amplification.

---

## 5. Computational Realization

### 5.1 Workflow Interface

Input:

```text
original uniform synthetic data
x_{s,i,r} = [r_start, C_s, B_i, Y_{s,i}, r_end]
original model / top-1 MoE router
original seeds and checkpoints
```

Computation:

```text
1. source-code audit of data generation, randomization, model and router init;
2. step-0 hidden decomposition h_f = c + u_f;
3. router score decomposition z = common offset + residual score;
4. matched random geometry Monte Carlo baseline;
5. residual routing intervention;
6. optional anti-lockin variant if needed.
```

Output:

```text
collapse root-cause decision:
- code/data/init issue;
- random finite-sample + training amplification;
- common-direction shortcut;
- top-1/utility lock-in;
- insufficient evidence.
```

### 5.2 Minimal Computational Test

#### Test 0: Code / Data / Init Sanity Audit

Use the audit prompt in:

```text
05_03_code_data_init_audit_prompt.md
```

Primary outputs:

```text
data_uniformity: PASS / FAIL / UNCLEAR
sequence_randomization: PASS / FAIL / UNCLEAR
step0_checkpoint_semantics: pre-training / post-update / unclear
router_init_math: W, b, init distribution, temperature, top-k, bias, aux loss
hidden_common_sources: listed and quantified
```

#### Test 1: Representation Decomposition

For each checkpoint \(t\in\{0,10,20,50,100,final\}\):

```text
h_f(t) = feature centroid at router input
c(t) = mean_f h_f(t)
u_f(t) = h_f(t) - c(t)
```

Metrics:

```text
common_ratio(t) = ||c(t)|| / mean_f ||h_f(t)||
variance_explained_by_c(t)
pairwise_cosine(h_f)
pairwise_cosine(u_f)
```

#### Test 2: Router Score Decomposition

Compute:

```text
common_score_e(t) = w_e(t)^T c(t) + b_e(t)
residual_score_{f,e}(t) = w_e(t)^T u_f(t)
full_load(t) = argmax_e common_score_e + residual_score_{f,e}
residual_load(t) = argmax_e residual_score_{f,e}
```

Decision:

```text
full concentrated + residual balanced -> common shortcut candidate
full concentrated + residual concentrated -> residual geometry / init candidate
full balanced + final collapsed -> training amplification candidate
```

#### Test 3: Random Geometry Baseline

Monte Carlo:

```text
sample F random feature centroids
sample E random router vectors with matched init distribution
compute top-1 loads and margins
repeat >= 100000
```

Compare observed step-0:

```text
observed max_load
observed dominant expert identity
observed top-1 margin
observed full-vs-residual load
```

#### Test 4: Common-Direction Residual Routing

Intervention:

```text
h_full = transformer hidden state
c = mean hidden direction, estimated on train batch / feature centroids
h_route = h_full - proj_c(h_full)
router logits = W h_route + b
expert input = h_full
```

Why this is clean:

```text
Only router input changes. Expert still receives full hidden state.
If target accuracy remains high and collapse decreases, this supports common-direction routing shortcut.
```

#### Test 5: Anti-Lockin Variant, Only If Needed

Candidates in priority order after Tests 0-4:

```text
1. zero-bias / row-centered / orthogonal router init;
2. early load balancing / router warmup;
3. delayed hard top-1 or high-temperature soft routing early;
4. forced-routing utility matrix;
5. counterfactual negative correction.
```

---

## 6. Minimal Falsifiable Test

| Mathematical object | Implementation object | Metric | Decision |
|---|---|---|---|
| data uniformity | dataset generator + dataloader | counts, chi-square/KL, batch entropy, order hash | pass/fail code sanity |
| router init | router class and checkpoint step 0 | W/b distribution, row norms, bias, cosine | pass/fail init assumption |
| common component c | feature hidden centroids | common_ratio, variance explained, c alignment | whether common exists |
| random geometry | Monte Carlo matched baseline | p-value for observed step-0 max_load/margin | random enough or anomalous |
| common score offset | w_e^T c + b_e | full load vs residual-only load | common shortcut candidate |
| training amplification | checkpoints | load entropy, top-1 margin, final-expert agreement | lock-in dynamics |
| causal common test | residual routing intervention | final collapse rate, target accuracy, slot composition | support/weaken common-cause |
| anti-lockin | warmup/load-balance/init variants | collapse rate, accuracy, early lock-in | choose next mechanism |

---

## 7. Falsifiable Outcomes

### Supported: Common-Direction Collapse Mechanism

Supported if:

```text
1. data and init audit pass;
2. c(t) is nontrivial at step 0 or early steps;
3. full router scores concentrate on collapse expert while residual-only scores are more balanced;
4. collapse expert has high common_score_e = w_e^T c + b_e;
5. common-direction residual routing reduces final hard collapse;
6. target accuracy remains close to baseline.
```

Then claim:

```text
In this uniform setting, route collapse is at least partly driven by a shared hidden component used as a routing shortcut.
```

Still cannot claim:

```text
common direction is the only cause or sufficient in all settings.
```

### Supported: Random Geometry + Training Amplification

Supported if:

```text
1. step-0 load imbalance is within random geometry baseline;
2. step-0 margin is small;
3. final collapse rate is high because margins grow during training;
4. residual routing does not substantially reduce collapse;
5. warmup/load-balance/delayed top-1 reduces collapse.
```

Then claim:

```text
Random early asymmetry is not pathological by itself, but hard top-1 training lacks enough self-correction and amplifies early advantage.
```

### Supported: Initialization Problem

Supported if:

```text
1. router bias / row norm / custom init / checkpoint semantics differs from assumed math;
2. row-centered / zero-bias / orthogonal init reduces early load concentration and final collapse;
3. data and representation common component do not explain the effect alone.
```

Then claim:

```text
The basic initialization does not provide the desired uniform partition property in this setting.
A new initialization or warmup constraint is justified.
```

### Supported: Data / Code Artifact

Supported if:

```text
1. counts are not uniform;
2. order is block structured;
3. nuisance or position leaks target;
4. step 0 is not actually pre-training;
5. wrong config / wrong dataset path is used.
```

Then claim:

```text
The collapse observation cannot yet be interpreted as a model mechanism.
Fix and rerun baseline before mechanism claims.
```

### Weakened / Redirected

Redirect if:

```text
- common component exists but residual routing does not help;
- random geometry baseline already predicts most observed early imbalance;
- forced-routing utility shows collapsed expert is genuinely best for all features;
- recovery seeds show early spike is reversible under certain dynamics.
```

Next target:

```text
expert utility landscape, capacity constraint, load-balance pressure, or recovery mechanism.
```

### Insufficient Evidence

Insufficient if:

```text
- no source-code audit;
- no step-0 checkpoint semantics;
- no matched random baseline;
- only correlational common alignment without intervention;
- only final load plots without early margin / hidden decomposition.
```

---

## 8. Current Evidence

### 8.1 What We Have

```text
1. 原始 uniform setting 中 collapse 频繁出现；因此 P1/P3/P2 暂停。
2. final collapsed runs: 9/24。
3. 所有 final collapsed runs 中，final dominant expert 在 step 0 已是 dominant expert: 9/9。
4. collapsed runs mean top-1 margin 从 step 0 的小 margin 增长到 final 的大 margin：
   step 0 ~0.078, step 100 ~0.462, final ~0.797。
5. S1-cos/20260522 是 hard collapse seed：step 0 偏向最终 expert，step 10 跨过 collapse threshold。
6. S1-cos/20260523 是 recovery contrast：early spike 后 step 50 恢复平衡，说明 early spike 非充分条件。
7. 同一 bad seed 在多个 matched conditions 有 early load concentration，说明 collapse 不是 inhibition-only artifact。
8. collapse expert 最终高度对齐 global common hidden direction。
```

### 8.2 Current Interpretation

```text
collapse 不是 late-stage accident。
final collapse expert 在 early routing geometry 中已经可见。
但 step-0 margin 不大，所以 initialization 不是完整解释；训练会放大 early bias。
common-direction alignment 是强机制候选，但尚未被 causal intervention 证明。
```

### 8.3 What Is Missing

```text
1. source code data generation audit;
2. exact router/gating initialization math;
3. step-0 checkpoint semantics;
4. matched random geometry baseline;
5. h = c + residual decomposition at step 0;
6. common-direction residual routing intervention;
7. forced-routing utility matrix, if we want to discuss router utility mismatch.
```

---

## 9. Claim Boundary And Next Decision

### Can Claim Now

```text
- 在原始 uniform feature setting 中，collapse 是主要解释边界。
- final collapse expert 在 early geometry 中已经可见。
- 训练会放大 early small bias，形成 high-margin / high-load lock-in。
- common-direction alignment 是当前最强机制候选。
- 在解释 collapse 前，不应继续扩大 feature-assumption relaxation 的 claim。
```

### Cannot Claim Yet

```text
- collapse 的完整因果机制已经解决。
- common direction 是唯一或充分原因。
- inhibition 一定有害。
- router-chosen expert 与 utility-best expert 错配。
- anti-lockin 机制已经验证。
- 结论可推广到 compositional token、Zipfian frequency、full LM、attention setting 或 real data。
```

### Next Decision

```text
本轮最小 decision：
在 verified uniform data 和 verified router initialization 下，
common-direction residual routing 是否显著减少 final collapse，且保持 target accuracy？
```

Decision tree:

```text
If code/data/init audit fails:
  fix baseline; do not make mechanism claim.

If audit passes and residual routing reduces collapse:
  update anchor: common-direction shortcut supported; next test anti-lockin robustness.

If audit passes and residual routing does not reduce collapse:
  update anchor: common direction insufficient; next test random geometry + top-1 warmup/load-balance/init.

If random baseline predicts step-0 imbalance but training causes final collapse:
  update anchor: random early geometry is normal, lock-in mechanism is target.

If zero-bias/orthogonal/row-centered init reduces collapse:
  update anchor: initialization property is a root-cause component; propose better initialization method.
```
