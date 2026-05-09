# Daily Record / Checkpoint

## 0. 本次对话梳理

- 今日核心问题：我们需要验证，在CL的测试中，学得快 + 抗遗忘的增益是不是将common 和 tail-branch分开得到的增益。
- 当前判断：可能是？不同领域的middle tail部分应该不重合，给出的梯度方向不同。分不同branch的话，能够保住common部分，让tail部分进行特异更新。
- 卡点：two branch dense的验证效果不好，two branch中common tail分开效果打不过matched dense和Random subspace
- 希望得到的产物：可信的实验结果 + 分析

---

## 1. Project Snapshot

### 1.1 愿景

做一个更适合 continual learning 的 modular / MoE 架构，使模型能够快速适配新任务，同时减少旧任务遗忘。

### 1.2 当前主线

当前不直接推进 full hierarchical MoE。

当前主线是：

> 先验证 representation split / branch isolation 是否真的能带来 CL 价值；如果 coarse split 不成立，就不能直接推进 many-branch / hierarchy。

### 1.3 与导师 idea 的关系

two-branch 是 hierarchical MoE intuition 的最小可证伪版本。

如果 two-branch 在 matched dense、raw two-branch、random split 之外没有稳定收益，那么 many-expert / hierarchy 暂时没有地基。

---

## 2. Core Hypotheses

### H-main

在 pretrained LM 的某一层中，不同 representation subspace 对 continual learning 干扰的贡献可能不同。  
如果能把 plastic / tail-sensitive update 与 common update 隔离，可能减少 forgetting。

### H1: representation band 与 token-frequency function 相关

middle / tail variance band 可能对 middle / rare tokens 更关键。  
状态：未证实。

### H2: forgetting 来自 non-uniform gradient interference

old/new task 的梯度冲突可能集中在某些 representation bands。

hidden-gradient conflict 定义为：

$$
C_b=
\mathbb{E}
\left[
\cos
\left(
P_b\nabla_x L_{\text{old}},
P_b\nabla_x L_{\text{new}}
\right)
\right]
$$

状态：本轮没有看到明显负冲突。

### H3: frequency / variance-aware two-branch 有 CL 价值

相比 matched dense、raw two-branch、random split，真实 variance-band split 应该降低 forgetting 并保持 new-task learning。

状态：当前 H3-causal audit failed。

---

## 3. Term Mini-Dictionary

- `CL / continual learning`：新任务适配后，同时测旧任务是否遗忘。
- `F_old`：旧任务 loss 变化。
  $$
  F_{\text{old}}=L_{\text{old}}^{\text{after}}-L_{\text{old}}^{\text{before}}
  $$
- `G_new`：新任务学习收益。
  $$
  G_{\text{new}}=L_{\text{new}}^{\text{before}}-L_{\text{new}}^{\text{after}}
  $$
- `variance band`：按 hidden-state PCA/SVD 方差排序得到的方向区间。
- `u50`：第 17 到 207 个 PCA/SVD 方向。
- `ext`：第 782 到 rank 末尾的 extreme low-variance directions。
- `u50_ext`：
  $$
  P_{17:207}(x-\mu)+0.25P_{782:r}(x-\mu)
  $$
- `branch functional specialization`：无 router 的 two-branch 中，某个 branch 对某类 token loss 的贡献更大。
- `expert specialization`：仅用于 routed model，表示被选中的 expert 在 NTP loss 上优于替代 expert。

---

## 4. Evidence Ledger

| 实验 / 阶段 | 关键结果 | 对主线的更新 |
|---|---|---|
| earlier single-layer block results | tail-conditioned / split-first block 曾出现真实模型正结果 | 支持继续研究 split-first，但不自动支持 CL |
| Phase8.2 formal CL | `u50_ext` 曾有弱 CL 信号 | 需要更严格 causal audit |
| latest H3-causal audit | matched dense / replay / raw two-branch 明显强于 real variance-band split；random split 也强于 `u50_ext` | H3 当前失败，不能用 real variance split 支撑 hierarchy |
| latest gradient audit | old/new hidden-gradient cosine 多为正；dense/raw 的 old loss 反而下降 | 当前 CL split 没有制造强 forgetting pressure |

---

## 5. Current Claim Boundary

### 现在可以说

1. 我们已经完成一次 matched-budget H3 causal audit。
2. 当前 real variance-band split 没有证明优于 matched dense、raw two-branch、random split。
3. 当前 `u50_ext` 不能作为已经验证的 CL plastic input。
4. 当前不能从 H3 推进 hierarchy。
5. 下一步应先诊断 CL setting 和 projected branch underfitting。

### 现在不能说

1. hierarchy 已经被 CL 结果支持；
2. `u50_ext` 已经是最佳 CL expert input；
3. variance-band split 已经减少 forgetting；
4. branch ablation 的 rare-token contribution 就等于 specialization；
5. random split 已经被排除；
6. dense capacity explanation 已经被排除。

---

## 6. 当前不确定点

1. 本轮 H3 失败，是因为 variance-band hypothesis 错了，还是因为 projected branch 学习信号太弱？
2. 当前 WoS old/new split 是否太相似，导致 dense baseline 没有真正 forgetting？
3. 为什么 raw two-branch 在本轮表现最强？
4. `head16` 明显强于 `u50/ext/u50_ext`，是否说明当前 CL adaptation 主要依赖 high-variance/common directions？
5. 如果要重新定义 plastic input，应使用 normalized projection、learned scaling，还是重新寻找 band？

---

## 7. Next Minimal Step

下一步只做一个最小诊断：

> 构造一个 dense baseline 会出现 positive forgetting 的 CL stress setting，然后只重跑 `G0_matched_dense / G1_raw_two_branch / G2_random_split / G6_u50_ext`。

通过标准：

- 如果 `G0` 仍然没有 positive forgetting，说明当前任务不适合验证 H3。
- 如果 `G0` 有 forgetting，但 `G6` 仍然学不动，说明 projected branch underfits。
- 如果 `G6` 在 harder CL 中开始有效，再恢复完整 H3 matrix。

---

## 8. 本日结束整理

### 今天推进了什么？

今天推进了H3：相比 matched dense、raw two-branch、random split，真实 variance-band split 应该降低 forgetting 并保持 new-task learning。的验证！

### 今天真正理解了什么？

在Dense中仅仅只是将Common 和 tail分开，是没有办法增强抗遗忘性的。

### 哪个判断发生了变化？

two branch中，将common和tail分开并不存在抗遗忘性。

### 明天最小下一步是什么？

需要检查实验的进一步结果，构造能够让Dense遗忘的任务，看Two branch是否会遗忘。
在以上情况下，加入Routing模型，Routing的模型尽量多一点，然后看看多专家，能否得到的效果好一些。

---

## 9. AI Prompt

```markdown
请基于当前 checkpoint 帮我做理论纠偏。

请重点回答：

1. 当前主假设是否仍然成立？
2. 最新实验对 H1/H2/H3 分别更新了什么？
3. 哪些 claim 必须降级？
4. 当前最小下一步是什么？
5. 哪些内容应该写入 checkpoint，哪些应该移入 archive？

要求：
- 先定义关键术语；
- 不要直接推进 hierarchy；
- 区分实验失败、假设失败、benchmark 不合适、implementation underfit；
- 最后给出一段可以直接写进 Daily Record 的更新文本。
```