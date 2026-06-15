# 12-Minute Speech Script

Topic: **Why Sparse MoE Routers Collapse Before They Specialize**  
Subtitle: **A mechanism audit of common-logit bias and early top-1 amplification**  
Version: updated with 0614 freeze-split results and 0615 common-filtered expert-spectrum stress test.

## Delivery Rule

Use this as the main speaking script. The slide text should stay short; this document carries the explanation.

When saying technical terms:

- Sparse Mixture-of-Experts, or sparse MoE: a model where each token activates only a few experts.
- Router or gate: the module that decides which expert receives each token.
- Common component: the shared mean direction in router-input hidden states.
- Common-logit: the expert-specific score $w_e^T c$ produced by projecting the common component onto expert $e$'s router row.
- Route concentration: most tokens go to a small number of experts.

---

## Slide 01. Title

Time: 0:00-0:35

English script:

Today I will present my current research progress on sparse Mixture-of-Experts routing. The title is "Why Sparse MoE Routers Collapse Before They Specialize." The main point is not that I already have a complete new gating method. Instead, this is a mechanism audit. I want to understand why a sparse top-1 router can concentrate tokens on a few experts before useful expert specialization has a chance to form.

Chinese intent:
开场先定边界：这是机制解释和研究进展，不是完整方法论文。

---

## Slide 02. MoE scaling depends on routing, not only expert count

Time: 0:35-1:30

English script:

Sparse MoE is attractive because it increases the number of parameters while keeping per-token computation relatively small. But the router becomes a central bottleneck. It decides which experts receive data, gradient, and early training signal. Traditional MoE work already studies load balancing, such as auxiliary load losses and expert-choice routing. But recent geometry-focused work suggests an important caution: expert usage patterns do not necessarily mean human-interpretable domain expertise. They may mainly reflect the geometry of hidden states. So my question is more specific: when top-1 routing fails, is it failing because the feature is missing, or because the router amplifies the wrong geometry?

Chinese intent:
把背景从“负载均衡”推进到“routing geometry”。引用两篇新 paper 的观点：routing pattern 不等于 domain expertise。

Optional cut:
Remove the sentence about expert-choice routing if time is tight.

---

## Slide 03. Research question: missing features or bad early routing?

Time: 1:30-2:20

English script:

This slide shows the storyline of the past week. I started from a simple question: if the model can represent a feature, will the sparse router naturally route by that feature? The answer became more subtle. First, route consistency can be misleading, because a collapsed router is also very consistent. Second, specialization is reachable under favorable initialization, so it is not impossible. Third, the common-logit model gave a concrete mechanism: a shared hidden direction can become an expert-specific bias. Finally, real-text experiments revised the claim. In real DCLM text, the common component is not the dominant step-0 margin source, but it is a load-bias source and is rapidly amplified during early training.

Chinese intent:
一页完成从 0601 到 0615 的主线，不按时间流水账讲，而按问题递进讲。

---

## Slide 04. High route consistency can hide collapse

Time: 2:20-3:10

English script:

The first lesson is that high route consistency is not enough. In early toy audits, the same feature key often went to the same expert with very high consistency. At first this looked like specialization. But the heatmaps show the problem: many slots can be captured by the same expert. A collapsed router can look perfectly consistent because it always makes the same wrong assignment. Therefore, I stopped treating route consistency or task accuracy as sufficient evidence. The more important metrics became slot-to-expert NMI, expert load, heatmap structure, and intervention results.

Chinese intent:
解释为什么我们的研究需要机制审计：弱指标会产生 false positive。

---

## Slide 05. Specialization is reachable, but random top-1 often misses the basin

Time: 3:10-4:05

English script:

The second lesson is that specialization is reachable. With slot-aware initialization, the final heatmaps show a clean slot-to-expert structure. In oracle-to-trainable release experiments, once the router is placed into a good routing basin, training can preserve that structure. This rules out a simple explanation that the task is impossible or that the hidden states do not contain the relevant information. The bottleneck is more likely basin entry: random top-1 routing often enters a bad early route basin before useful specialization forms.

Chinese intent:
排除 rival explanation：不是 feature 不存在，也不是 specialization 不可达，而是 random top-1 的 early basin 问题。

---

## Slide 06. Common-logit bias is an expert-specific effective bias

Time: 4:05-5:00

English script:

The mechanism I tested is common-logit bias. Suppose the router input hidden state can be decomposed as $h_i = c + r_i$, where $c$ is a common component shared by many tokens and $r_i$ is a residual or feature-specific component. For a linear dot-product router, the expert score is $z_{i,e}=w_e^T h_i = w_e^T c + w_e^T r_i$. The term $w_e^T c$ is independent of the token feature, but it differs across experts. In top-1 routing, even a feature-independent term can decide the argmax for many tokens. So the common component acts like an expert-specific effective bias.

Chinese intent:
讲清楚核心数学对象：$w_e^T c$。这是后面所有实验的共同语言。

---

## Slide 07. Controlled evidence: common-logit is early and intervention-relevant

Time: 5:00-6:15

English script:

In the controlled toy setting, this mechanism is not just descriptive. The timing plot shows that the common margin rises early and becomes larger than the slot margin before the final routing structure is decided. More importantly, when I cancel the common-logit contribution during routing, slot NMI improves sharply while accuracy remains at one. In the baseline, slot NMI is about 0.08 with almost complete load collapse. With common cancellation, slot NMI rises to around 0.90 or higher, while accuracy is preserved. This supports common-logit as a causal contributor in the controlled dot-product setting.

Chinese intent:
这页是 toy causality：timing + intervention。强调不是只解释，而是干预后 slot NMI 提升。

Optional cut:
If time is tight, skip the exact 0.90 number and say "substantially improves."

---

## Slide 08. The common source can be localized, but removing it is not sufficient

Time: 6:15-7:10

English script:

The next question was where the common component came from. In the synthetic setting, fixed routed position and template structure were major sources of the step-0 common offset. Zeroing the routed position embedding reduced the common ratio and reduced step-0 max load. But this did not solve the whole problem. Lower load concentration is not the same as stable slot-level specialization. This is an important boundary: common control improves early geometry, but it is not a complete gating mechanism by itself.

Chinese intent:
收紧 claim：common-offset 是重要来源，但不是完整解法。

---

## Slide 09. Real text weakens the strong step-0 dominance claim

Time: 7:10-8:15

English script:

The real-text audit forced me to revise the strongest version of the hypothesis. On DCLM text, at step 0, the common margin is about 0.124, while the residual margin is about 0.236. The dominance ratio is about 0.53, and only one out of eighteen layer-seed cases has common dominance larger than one. So I should not claim that the common component dominates every step-0 routing decision in real text. However, common centering still reduces max load from about 0.278 to 0.156. This means the common component is not the main margin source, but it is a real load-bias source.

Chinese intent:
诚实更新：真实文本削弱 strong claim，但保留 common component 的 load-bias 价值。

---

## Slide 10. Real-text route concentration is amplified during early training

Time: 8:15-9:15

English script:

The real-text problem therefore shifts from pure initialization geometry to early-training amplification. At step 0, the max load is already biased, around 0.278 instead of the uniform value 0.125 for eight experts. But by step 10, raw max load jumps to about 0.851, and the common dominance ratio becomes about 21.8. This is not simply that all other experts are dead. It is severe concentration: most tokens are routed to a very small number of experts. So the key question becomes: what training path amplifies a small early routing bias into a severe step-10 concentration?

Chinese intent:
把故事转向 0614/0615 的主问题：训练早期放大，而不是静态初始化。

---

## Slide 11. Raw concentration and common-margin amplification are related, not identical

Time: 9:15-10:35

English script:

The 0614 freeze-split result gives a sharper causal boundary. In layer 5, normal training increases common margin by about 1.276 from step 0 to step 10, and raw max load increases by about 0.733. If I freeze the gate, raw load concentration still appears almost as strongly, but the common-margin spike is smaller. If I freeze experts, raw load concentration still appears, while common-margin amplification is reduced. The strongest intervention is freezing the hidden-producing path before the layer-5 router input; this suppresses both the common-margin spike and raw load concentration. So raw concentration and common-logit amplification are related, but not identical. The full spike needs hidden-producing path and gate-hidden interaction, not gate-only updates.

Chinese intent:
0614 的边界：不要说 gate-only；固定 gate 也会 raw concentration。完整 common-margin spike 需要 hidden/gate interaction。

Optional cut:
If time is short, remove the freeze experts sentence.

---

## Slide 12. 0615 update: common-filtered spectrum init improves step 0, but fails by step 10

Time: 10:35-12:00

English script:

The latest 0615 result tests the natural next method idea: initialize the router using expert high-gain directions, and remove common directions before building the router. This is the common-filtered expert-spectrum initialization. The result is negative but informative. After removing the top one percent high-frequency token ids, random initialization has a rank-1 expert load of 19.98 percent at step 0, while the common-filtered spectrum version improves this to 13.97 percent, close to the uniform value of 12.5 percent. So it really improves the initial distribution. But by step 10, it fails: random reaches 83.16 percent on the top expert, while common-filtered spectrum reaches 93.51 percent. It also lowers the replay interaction term, but worsens the primary common-margin and load metrics. Therefore, I should not present it as a successful method. The current conclusion is that the bottleneck is early-training amplification, not just initial geometric balance. The next minimal step is a post-hoc audit: does the initially common-aligned router winner receive reinforcing updates during steps zero to ten? If yes, router self-reinforcement is part of the mechanism. If not, the focus should shift to hidden drift, residual anisotropy, or expert-output feedback.

Chinese intent:
结尾讲 0615 最新结果。重点是 negative-but-informative：第 0 步变好，第 10 步失败，所以方法 claim 不成立，但机制主线更清楚。

Closing sentence:

```text
Overall, my current contribution is a mechanism-level story: sparse top-1 failure is not just missing features or poor load balance; it is amplified routing geometry.
```

---

## If Asked: One-Sentence Summary

English:

```text
The router does not simply discover semantic experts; it amplifies hidden-state geometry, and in my current evidence a common direction can create early expert bias that training rapidly amplifies.
```

Chinese:

```text
路由器不是自然发现语义专家，而是在放大 hidden-state geometry；当前证据说明共同方向会形成早期专家偏置，并在训练早期被快速放大。
```

## If Asked: Why the 0615 result is still useful

English:

```text
It rules out a simple solution. Common-filtered spectrum initialization can fix part of the step-0 imbalance, but it cannot stop the step-10 amplification. That tells us the next target should be the amplification path, not only initialization balance.
```
