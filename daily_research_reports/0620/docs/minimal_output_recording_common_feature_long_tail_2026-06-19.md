# Minimal Output Recording — Common Feature vs Long-Tail Suppression

Date: 2026-06-19

Source document: `common_feature_long_tail_theory_and_results_polished_final.md`

---

## 0. Today’s Core Takeaway

导师真正要解决的问题不是泛泛地说“长尾学得慢”，而是区分：

```text
rare learning delay = sample scarcity?
还是
rare learning delay = destructive interference from common-feature updates?
```

当前最安全结论：

```text
common features suppress long-tail features only when:
1. frequency imbalance,
2. target conflict,
3. persistent prediction-relevant effective overlap
occur together.
```

表面措辞相似、语义类别相同、或者稀有样本少，本身都不足以推出“压制”。

---

## 1. 导师想解决什么问题？

### Decision Question

```text
高频共同特征是否会主动压制低频长尾特征？
如果会，压制发生的必要机制条件是什么？
```

更精确地说，导师想把两个现象分开：

| 现象 | 含义 | 是否等于 suppression? |
|---|---|---|
| Sample scarcity | 稀有特征出现少，直接梯度更新少，所以学得慢 | 否 |
| Destructive interference | 高频共同样本的更新会增加稀有 loss、降低稀有概率、把稀有 logit 推向错误目标 | 是 |

### 最重要的纠偏

不要把问题写成：

```text
common feature 会不会压制 rare feature？
```

应写成：

```text
在什么条件下，common-feature updates 会对 rare-feature predictor 产生负的一阶影响？
```

---

## 2. 物理先验、假设、boundary，以及如何区分

### 2.1 物理先验是什么？

物理先验是对机制方向的直觉，不是已经被证明的 hypothesis。

本文中的物理先验可以写成：

```text
如果一个高频 common feature 和一个低频 rare feature 在模型的预测相关方向上纠缠，
那么 cross-entropy training 会先把 common direction 学强。
如果 rare target 与 common target 冲突，
这个共同方向可能会泄漏进 rare logit 或 rare attention，
从而把 rare prediction 推向错误目标。
```

最小数学直觉：

$$
s_r \approx \theta_r + \rho_{\mathrm{out}}\theta_c
$$

如果

$$
y_r\rho_{\mathrm{out}}\theta_c < 0
\quad\text{and}\quad
|\rho_{\mathrm{out}}\theta_c| > |\theta_r|,
$$

则 common term 会压过 rare signal。

### 2.2 假设是什么？

假设必须是可检验、可证伪的版本：

```text
当 frequency imbalance、target conflict、persistent prediction-relevant effective overlap 同时存在时，
common-feature updates 会 destructively interfere with rare-feature learning。
```

可观测预测：

```text
1. rare threshold crossing 延迟；
2. gradient cosine < 0；
3. common component removal 在 conflict case 中改善 rare prediction；
4. aligned target control 不应出现同样伤害；
5. balanced frequency control 应减弱延迟。
```

### 2.3 Hypothesis boundary 是什么？

这个假设不能推出：

```text
1. 只要 rare feature 少，就一定被 suppression；
2. 只要两个样本共享词语，就一定有效重叠；
3. 只要两个事实属于同一语义类别，就一定共享预测方向；
4. controlled vector experiment 的机制会自动推广到 flexible Transformer；
5. delayed learning 本身就是 destructive interference。
```

可以 claim：

```text
在持久有效重叠 + 目标冲突 + 频率不均衡同时出现时，
common updates 可以主动伤害 rare learning。
```

### 2.4 如何区分 physical prior 和 hypothesis？

| 概念 | 作用 | 形式 | 例子 |
|---|---|---|---|
| Physical prior | 给出“为什么可能发生”的机制直觉 | 机制方向、力学类比、数学直觉 | 高频 common direction 先变强，若与 rare target 冲突，会泄漏进 rare logit |
| Hypothesis | 给出“什么条件下会发生”的可检验命题 | 条件 + 预测 + falsifier | 三条件同时成立时，gradient cosine 应为负，rare learning 应延迟，移除 common component 应改善 rare prediction |
| Boundary | 防止 claim 过强 | 不能推出什么 | 表面重叠/语义相同/稀有性本身不等于 suppression |

最短区分：

```text
physical prior = 我为什么相信这个机制可能存在；
hypothesis = 我准备怎样让它被支持或被证伪；
boundary = 即使实验成功，我仍然不能 claim 什么。
```

---

## 3. 导师针对假设提出的 minimal verification experiment 是什么？

### Minimal Verification Experiment

最小实验是受控输出头模型，因为它直接控制 overlap、target relation 和 frequency。

#### Setup

```text
model: z = Wx
common direction: u_c = e_1
rare direction: u_r = rho e_1 + sqrt(1-rho^2)e_2
common target: class 0
rare target:
  conflict condition: class 1
  aligned condition: class 0
frequency:
  imbalanced: 90/10
  balanced control: 50/50
```

#### Primary Metric

```text
T_0.9 = first step where rare probability >= 0.9
```

#### Mechanism Diagnostic

```text
gradient cosine cos(g_c, g_r)
```

#### Minimal Controls

| Control | 问什么 | 预期 |
|---|---|---|
| Orthogonal conflict, 90/10 | 只有频率不均衡和目标冲突，但无 overlap，是否压制？ | 不应有一阶 destructive interference |
| Strong overlap conflict, 90/10 | 三条件同时成立，是否延迟 rare learning？ | 应强烈延迟，gradient cosine < 0 |
| Strong overlap aligned, 90/10 | overlap + imbalance 但 target 不冲突，是否仍有害？ | 不应有害，甚至可能帮助 |
| Strong overlap conflict, 50/50 | overlap + conflict 但频率均衡，是否减弱？ | 延迟应减弱 |

#### Key Result

```text
orthogonal conflict, 90/10: T_0.9 = 140, gradient cosine = 0
strong overlap conflict, 90/10: T_0.9 = 420, gradient cosine = -0.6
strong overlap aligned, 90/10: T_0.9 = 40, gradient cosine = +0.6
strong overlap conflict, 50/50: T_0.9 = 80
```

因此最小验证支持：

```text
persistent overlap + target conflict + frequency imbalance
=> destructive rare-learning delay
```

---

## 4. 导师如何一步一步走到结论？

### Step 1 — 从粗猜想开始

初始猜想：

```text
common features suppress long-tail features.
```

问题：这个说法过宽，把 sample scarcity 和 destructive interference 混在一起。

---

### Step 2 — 定义概念差异

导师先区分三种 overlap：

```text
1. statistical co-occurrence: 两个 feature 是否一起出现；
2. raw geometric overlap: 原始 feature vector 是否重叠；
3. effective prediction-relevant overlap: 模型预测相关子空间中是否重叠。
```

关键纠偏：

```text
surface overlap 不推出 effective overlap；
same semantic category 不推出 same prediction-relevant direction。
```

---

### Step 3 — 建立 no-interference baseline

先证明一个反例基线：

```text
如果 common 和 rare raw directions 正交，
且模型参数 block-decoupled，
那么 common-only example 不直接更新 rare-feature parameter。
```

这一步的科研作用：

```text
建立 falsifier：frequency imbalance alone is not enough。
```

---

### Step 4 — 写出最小数学机制

当 raw overlap 存在时：

$$
s_r = \theta_r + \rho_{\mathrm{raw}}\theta_c
$$

如果 common leakage 指向错误 rare target 且压过 rare signal，则产生 destructive logit interference。

科研作用：

```text
把 vague intuition 变成可测机制变量：rho、theta_c、theta_r、target sign。
```

---

### Step 5 — 设计直接诊断

用一阶 Taylor 展开得到：

$$
L_r(\theta-\eta g_c)
\approx
L_r(\theta)-\eta\langle g_r,g_c\rangle
$$

因此：

```text
cos(g_c, g_r) < 0
```

是 destructive interference 的直接证据。

科研作用：

```text
避免只看 delayed learning，因为 delay 可能只是 sample scarcity。
```

---

### Step 6 — 做 controlled output-head experiment

在最简单模型中控制：

```text
overlap: rho = 0 vs rho = 0.6
target: conflict vs aligned
frequency: 90/10 vs 50/50
```

结论：三条件同时成立时 rare learning 最慢，并且 gradient cosine 为负。

---

### Step 7 — 加入 tiny attention 验证机制是否保留

加入 attention 后，机制仍出现，但延迟变小。

科研解释：

```text
attention 增加了模型分离 common/rare context 的能力，
所以 suppression mechanism survives but weakens。
```

---

### Step 8 — 做 causal intervention 和 robustness sweep

干预：移除 shared common component。

结果：

```text
conflict case: removal improves rare prediction
aligned case: removal hurts rare prediction
```

这说明 shared component 不是本质有害，而是当它指向错误目标时有害。

---

### Step 9 — 用 Transformer 实验修正 broad claim

半真实文本实验：共享措辞没有额外延迟。

语义事实实验：共同首都事实没有选择性压制稀有首都事实。

科研作用：

```text
falsify broad surface/semantic overlap claim。
```

---

### Step 10 — 得到 refined conclusion

最终结论从宽泛版本：

```text
common features suppress long-tail features
```

修正为条件机制：

```text
common features suppress long-tail features only when
frequency imbalance, target conflict, and persistent prediction-relevant effective overlap occur together.
```

---

## 5. 科研流程中必须经历的环节

这篇 note 展示的标准科研流程是：

```text
1. Broad conjecture
   -> common features suppress long-tail features

2. Concept separation
   -> sample scarcity vs destructive interference
   -> statistical co-occurrence / raw overlap / effective overlap

3. Null baseline
   -> no-interference baseline shows rarity alone is insufficient

4. Minimal mathematical model
   -> s_r = theta_r + rho theta_c
   -> harmful only if wrong sign and dominates rare signal

5. Mechanism diagnostic
   -> gradient cosine and rare-loss increase after common update

6. Controlled verification
   -> output-head model with overlap/conflict/frequency controls

7. Robustness and causal tests
   -> sweep rho/frequency; remove common component

8. More realistic model test
   -> tiny attention and Transformer experiments

9. Falsify overbroad claim
   -> surface overlap and semantic category are not enough

10. Refined claim and next decision
   -> measure/manipulate persistent effective overlap
```

---

## 6. Five Core Questions For You To Answer

请先只回答下面五个问题，不看后面的答案区。

### Q1

导师为什么不接受“rare feature 学得慢，所以 common feature suppress rare feature”这个推理？

### Q2

这篇 note 中，physical prior 和 hypothesis 分别是什么？请用一句话区分。

### Q3

为什么 aligned strong-overlap control 是关键 sanity check？它排除了什么错误解释？

### Q4

为什么 Transformer 中“shared wording”或“same semantic category”不能直接当作 suppression evidence？

### Q5

如果下一步要继续研究，最应该测量/操纵的变量是什么？为什么不是 surface overlap？

---

## 7. Answer Key / Thinking Correction

### A1

因为 rare learning delay 可能只是 sample scarcity。稀有特征出现少，因此直接更新少，学得慢并不说明 common updates 主动伤害了 rare predictor。要 claim suppression，需要看到 common update 对 rare loss/probability/logit/attention 的负面影响，例如 negative gradient cosine 或移除 common component 后 rare prediction 改善。

### A2

Physical prior 是机制直觉：高频 common direction 会先变强，若与 rare target 冲突并在预测相关方向上重叠，就可能压过 rare signal。Hypothesis 是可证伪命题：只有 frequency imbalance、target conflict、persistent prediction-relevant effective overlap 同时存在时，common updates 才会 destructively interfere with rare learning。

一句话区分：

```text
physical prior 解释为什么机制可能发生；hypothesis 规定什么观测会支持或推翻它。
```

### A3

aligned strong-overlap control 保持 overlap 和 frequency imbalance 不变，只把 target conflict 去掉。如果这个条件下学习变快、gradient cosine 为正，就说明 overlap 本身不是坏的；真正有害的是 overlap 指向冲突目标。它排除了“只要重叠就会压制”的错误解释。

### A4

因为 Transformer 的预测不是直接基于表面词或人类语义类别，而是基于学到的隐藏表征。两个样本可以共享很多词或同一语义关系，但模型仍可能把它们映射到不同预测相关方向。因此 shared wording / same semantic category 只能提出怀疑，不能证明 effective overlap 或 destructive interference。

### A5

下一步最应该测量和操纵的是模型预测相关子空间中的 persistent effective overlap，例如 output-head overlap、attention-subspace overlap、高增益奇异方向 overlap、gradient cosine，或 common-subspace causal intervention。不是 surface overlap，因为实验已经显示 surface overlap 不必然转化为 prediction-relevant overlap。

---

## 8. Minimal Self-Check Rubric

你的回答如果出现下面错误，需要修正：

| 错误说法 | 修正 |
|---|---|
| rare 学得慢 = suppression | rare 学得慢可能是 sample scarcity；suppression 需要 common update 主动伤害 rare evidence |
| overlap 一定有害 | 只有 target conflict 时 overlap 才可能有害；aligned overlap 可能有益 |
| shared wording = effective overlap | shared wording 不推出 hidden prediction direction overlap |
| semantic category = mechanism | semantic category 不是模型内部 causal variable |
| Transformer 结果否定 controlled result | 不否定；controlled result 测 persistent overlap，Transformer result 说明 overlap may not persist |

---

## 9. One-Sentence Recording

```text
Today I learned that the mentor’s refined claim is not “common features always suppress rare features,” but a conditional mechanism: destructive suppression requires frequency imbalance, target conflict, and persistent prediction-relevant effective overlap; otherwise delayed rare learning may be sample scarcity or may disappear if the model separates the representations.
```
