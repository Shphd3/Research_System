# 0518 汇报报告：Router Specialization 与 KV Retrieval 的假设闭环

## 1. 30 秒结论

我这轮想验证的是：MoE router 能不能先形成 `one feature -> one expert`，再把这个 expert bucket 当成 KV retrieval index。现在最稳的结论是两层否定：第一，feature 虽然已经能从 hidden state 读出，但 natural NTP 不会自动把它转成 clean expert assignment；第二，即使我用监督强制得到 perfect feature routing，它也不能有效召回 block2 attention 真正需要的 high-mass KV。也就是说，`feature separability != router specialization`，并且 `router specialization != KV index`。所以下一步不是继续堆 MoE 变体，而是直接诊断 dense attention 的 high-mass KV 到底由 locality、token identity、hidden similarity、value similarity 还是 feature identity 决定。

## 2. 这份报告要闭环的假设

这份报告不是要证明“MoE 有用或没用”，而是闭环三个更小的假设。

| ID | Hypothesis | 当前裁决 |
|---|---|---|
| H1 | 如果 feature 在 hidden/router representation 中可分，natural router 会自然形成 `one feature -> one expert`。 | 不支持 |
| H2 | 如果把 router 改成 trainable prototype/center，NTP 会把 centers 推到不同 feature cluster 上。 | 不支持 |
| H3 | 如果强制得到 perfect feature routing，feature-aligned buckets 就能成为好的 KV retrieval index。 | 不支持 |

主线更新：

```text
feature representation separability 不等于 router specialization；
router specialization 也不等于 KV retrieval index。
```

## 3. 实验世界：这份报告的边界

本报告只讨论一个受控 synthetic setting，不直接外推到真实 LLM。

| Item | Setting |
|---|---|
| Data | all-trigram synthetic corpus |
| Features | `ABC`, `DEF`, `GHI`, `JKL` 四个 context relation |
| Model | tiny causal Transformer + 4-expert top-1 MoE |
| Training | next-token prediction, plus optional router supervision |
| Retrieval target | block2 full attention 的 high-mass KV |

原本想验证的链条是：

```text
controlled features
-> learned feature representation
-> feature-aligned expert routing
-> feature-aligned buckets retrieve attention-relevant KV
```

0518 的结果说明这条链条断在两处：

1. feature representation 可分，不代表 router 会按 feature 分 expert；
2. router 按 feature 分 expert，也不代表 bucket 能召回 attention 需要的 KV。

## 4. H1/H2：为什么 natural router 不形成 one-feature-one-expert？

### 4.1 实验目的

我们先问：natural router 不 clean，到底是因为 feature 没学到，还是因为 router objective 没有要求它按 feature 切？

### 4.2 关键实验

| Experiment | Question | Result |
|---|---|---|
| E2-B3 prototype center | 可训练 expert center 是否自然对齐 feature？ | centers 有梯度并移动，但不自然 clean |
| E2-C contrastive representation | 让 router representation 更可分是否足够？ | feature 可读出，但 routing 仍不 clean |
| E3 predictor diagnostic | natural router 的 expert choice 更像由什么决定？ | 更像 hidden geometry / router projection，而不是 feature label |

### 4.3 关键证据 1：prototype center 有梯度，但不自然 clean

E2-B3 修正了 hard top-1 的梯度问题，让被选 expert output 乘上 gate value：

$$
\begin{aligned}
e^* &= \arg\max_e p_{t,e}, \\
y_t &= p_{t,e^*}\,\mathrm{Expert}_{e^*}(h_t).
\end{aligned}
$$

这保证 NTP loss 可以影响 prototype centers。

| Variant | first prototype grad | readback | NMI | best-perm acc |
|---|---:|---:|---:|---:|
| natural NTP | 0.0050 | 0.9957 | 0.5772 | 0.5000 |
| center separation | 0.0706 | 0.9955 | 0.1924 | 0.3333 |
| supervised CE | 4.1205 | 0.9969 | 1.0000 | 1.0000 |

解释：

- natural NTP 下，centers 确实收到梯度；
- 但它们没有自然变成四个 feature centers；
- center separation 只能把 centers 撑开，不能告诉哪个 feature 应该进哪个 center；
- supervised CE 可以稳定达到 `NMI=1`，说明模型和路由结构本身能 clean，失败来自 objective pressure 不够。

![E2-B3 prototype gradient](figures/e2b3_prototype_grad_norm_over_steps.png)

![E2-B3 routing matrix](figures/e2b3_routing_matrix_by_variant.png)

### 4.4 关键证据 2：feature 可读出，但 router 不按 feature label 切

E3 中，feature 可以从 hidden state 线性读出：

```text
feature-linear-probe = 1.0
```

但 feature label 对 expert choice 的解释力不高，而 router projection / PCA geometry 解释力更高：

| Dataset / no-LB | feature-linear-probe | feature-only -> expert | router-projection -> expert | PCA-only -> expert |
|---|---:|---:|---:|---:|
| unique | 1.000 | 0.539 | 0.973 | 0.941 |
| shared-B | 1.000 | 0.510 | 0.984 | 0.968 |
| shared-target | 1.000 | 0.435 | 0.963 | 0.908 |
| crossed-factorial | 1.000 | 0.457 | 0.978 | 0.957 |

这说明：

```text
模型内部能区分 feature；
router 也不是随机切；
但 router 学到的是 hidden space 中另一个低损失 partition，
不是人工定义的 ABC/DEF/GHI/JKL one-to-one partition。
```

![E3 predictor crossed](figures/e3_predictor_accuracy_crossed.png)

### 4.5 H1/H2 裁决

现在可以排除四个解释：

- 不是 feature 没学到；
- 不是模型或代码不能 clean route；
- 不是 prototype centers 没梯度；
- 不是 representation 可分就足够。

当前更稳的解释是：

```text
NTP 只要求预测下一个 token。
只要某种 hidden-geometry partition 或多个 experts 的冗余能力足够降低 loss，
router 就没有必要形成 one-feature-one-expert。
```

这个解释还不是完全闭环，因为我们还需要证明 natural router 选择的 partition 为什么是低损失解，以及什么压力会让 feature-aligned routing 变成必要解。

## 5. H3：如果强制 one-feature-one-expert，能否做 KV retrieval？

### 5.1 实验目的

R3 是 upper-bound test：不再等 natural router 自然 specialize，而是直接用 `RouterFeatureCE` 强制得到 perfect one-feature-one-expert。

Mapping:

```text
ABC -> expert 0
DEF -> expert 1
GHI -> expert 2
JKL -> expert 3
```

然后测试这些 feature-aligned buckets 是否能召回 block2 full attention 的 high-mass KV。

### 5.2 关键结果

强制路由成功：

| Dataset | NMI | ARI | fixed-label routing | feature readback acc |
|---|---:|---:|---:|---:|
| uniform | 1.000 | 1.000 | 1.000 | 1.000 |
| longtail | 1.000 | 1.000 | 1.000 | 1.000 |

但 retrieval 不成功：

| Dataset | K | Router recall | Random recall | Local recall | Router mass | Local mass |
|---|---:|---:|---:|---:|---:|---:|
| uniform | 1 | 0.310 | 0.279 | 0.404 | 0.346 | 0.681 |
| uniform | 2 | 0.536 | 0.530 | 0.680 | 0.528 | 0.838 |
| longtail | 1 | 0.328 | 0.298 | 0.433 | 0.378 | 0.735 |
| longtail | 2 | 0.582 | 0.580 | 0.746 | 0.614 | 0.887 |

结论：

```text
perfect feature routing 只略好于 random，
并且明显弱于 same-count local baseline。
```

![R3 uniform retrieval](figures/r3_uniform_perfect_router_topk_recall_mass_l2_baselines.png)

![R3 longtail retrieval](figures/r3_longtail_perfect_router_topk_recall_mass_l2_baselines.png)

### 5.3 H3 裁决

H3 不支持。

在当前 synthetic all-trigram setup 中，one-feature-one-expert 不是 KV retrieval 成立的充分条件。这说明 R1/R2 的失败不只是 natural router 没有 specialize；即使人为得到 perfect feature specialization，attention 需要的 high-mass KV 也没有主要按 feature label 聚集。

更可能的解释变量是：

- locality；
- token identity；
- hidden similarity；
- value/output similarity；
- head-specific attention pattern。

## 6. Claim 边界

可以说：

- 在 controlled synthetic trigram setting 中，natural top-1 router 不会自动形成 clean one-feature-one-expert；
- feature 在 hidden state 中可读出，不足以推出 router 会按 feature 切；
- supervised feature routing 可以达到 `NMI=1`；
- 但即使 perfect feature routing 成立，也不足以在当前设置下成为高效 KV index；
- 下一步应诊断 attention high-mass KV 到底由什么变量决定。

不能说：

- 真实 LLM MoE 不会形成语义 expert；
- MoE router 永远不能做 retrieval index；
- feature specialization 在所有任务中都没有检索价值；
- 当前实验已经证明没有长上下文加速可能。

## 7. 下一步

优先做 attention source decomposition：

```text
locality / token identity / hidden similarity / value similarity / feature identity
```

目标是测量每个变量解释了多少 attention mass。

同时做 utility gap test：

```text
learned router vs feature-oracle router vs best-utility router
```

如果 feature-oracle router 仍不优于 learned router，就说明 one-feature-one-expert 更像人类希望的解释性 partition，而不是当前 NTP / attention 机制的必要解。

## 8. 汇报时不要说什么

- 不要说“MoE router 没有语义”。
- 不要说“feature routing 没用”。
- 不要说“实验已经证明 retrieval 不可能”。
- 不要把 `NMI=1` 说成 retrieval 成功；R3 正好说明 routing clean 和 retrieval useful 是两件事。

## 9. 1 分钟汇报稿

我这轮把问题拆成两个假设闭环。第一个是假设 feature 可分以后，natural MoE router 会自然形成 one-feature-one-expert；这个不成立。E2/E3 显示 feature 可以从 hidden state 线性读出，supervised router 也能做到 `NMI=1`，但 natural NTP 下 expert assignment 仍然不 clean，更像按 hidden geometry 或 router projection 切。第二个是假设如果我强制 perfect feature routing，它就能作为 KV retrieval index；这个也不成立。R3 里 router 已经达到 `NMI=1`，但 router bucket 对 high-mass KV 的召回只略高于 random，明显弱于 local baseline。所以现在最稳的结论是：feature separability 不等于 router specialization，router specialization 也不等于 KV index。下一步我要直接分解 dense attention 的 high-mass KV 到底由 locality、token identity、hidden similarity、value similarity 还是 feature identity 决定。
