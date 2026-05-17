# Daily Record / Checkpoint

## 0. 本次对话梳理

1. 今日核心问题：我们要构建一个符合Zipfian的数据集，将Hierarchicial的MoE在数据集上训练，看是否训得出来，训的效果怎么样。
2. 当前判断：我们目前已经完成了1 数据集构造及确认 2 softversion的验证（比同参数的dense的loss下降得稍微快一点点）
3. 卡点：1 训练的步数不够；2 没有真正拿MoE进行训练
4. 希望得到的产物：

---

## 1. Project Snapshot

### 1.1 愿景

做一个更适合 continual learning 的 MoE 架构，使模型能够快速适配新任务，同时减少旧任务遗忘。

### 1.2 背景叙述

这个课题的出发点是 continual learning 中的灾难性遗忘问题：当 dense 模型或 dense adapter 在新任务上更新时，更新会同时扰动大量共享参数和共享表征方向。即使新任务学习得更快，也可能把旧任务依赖的 common structure、tail-sensitive features 或 rare-token 相关方向一并改坏。因此，真正需要解释的不是“模型容量是否更大”，而是“新旧任务干扰是否能被定位到某些表征子空间，并通过结构隔离减少干扰”。

MoE / modular architecture 的动机来自参数隔离和功能分工。如果不同 expert 接收的不是同一份混合表征，而是经过某种 operator 分离后的 feature / subspace，那么 expert 可能形成更强的 functional specialization：一部分专家处理通用高频结构，一部分专家处理 domain / topic 差异，一部分专家处理低频或长尾 token 的局部特征。这样，continual learning 中的新任务更新就有机会集中在更相关的模块里，而不是无差别地污染所有共享表示。

这个想法进一步受到 Zipfian token distribution 的启发。语料中的 token 和 feature 使用频率高度不均衡：高频 token / common feature 反复出现、更新稳定；中低频 token / rare feature 激活稀疏、更新机会少，却可能对任务迁移和遗忘更敏感。因此，一个合理的研究假设是：pretrained LM 的 hidden representation 里可能存在与频率、方差或功能相关的子空间结构；如果这些结构可以被 PCA/SVD band、projection operator 或 learned router 暴露出来，就可能成为 MoE expert 切分的依据。

当前假设还依赖三个更底层的前提：第一，语义或功能特征可以看作高维表征空间中的低维组合；第二，不同 feature 具有不同的激活频率、能量或梯度更新频率；第三，这些 feature 在某种表示或变换下具有可分性。现在最需要被严格定义和验证的，是所谓“表征拆得更干净”到底意味着什么：是 token loss contribution 更集中、branch ablation 更有差异、expert 被路由后 NTP loss 更优，还是 continual learning 中 old-task forgetting 更低。

已有证据只能作为动机，不能直接作为结论。早期实验中，去均值和移除中心化后的高方差方向可以让分发更开，但在下游任务和 toy CL 上没有稳定提升；two-branch 形式

$$
h_{out}=h_{in}+F_c(x)+F_t(x_t)
$$

曾经在把 common / tail 或不同方差 band 分开学习时出现过 toy CL 和专一化信号；其中 `u50_ext`：

$$
x_{u50\_ext}=P_{u50}(x-\mu)+0.25P_{ext}(x-\mu)
$$

曾被认为是较有希望的 plastic input。然而最新 matched-budget H3 causal audit 显示，真实 variance-band split 尚未打过 matched dense、raw two-branch 和 random split。因此，背景叙述应该从“MoE / hierarchy 很有希望”降级为“频率/方差表征切分是一个待证伪的机制假设”，后续必须先验证 branch isolation 是否真的带来 CL 价值。

### 1.3 当前主线



## 2. Core Hypotheses

### H-main1（Hierarchical）

真实 pretrained LM 的 hidden representation 中存在多层级 functional components。顶层 component 主要承载跨 domain / 跨 token 的 shared common structure；中层 component 可能承载 domain / topic / subdomain 差异；底层 component 可能承载 token-signature、rare feature 或局部语义差异。
如果某个 operator 能把这些 components 显式暴露出来，那么 router / experts 可以利用这些 components 形成更细粒度的 functional specialization。

### H-main2（Two Branch，Secondary）

在 pretrained LM 的某一层中，不同 representation subspace 对 continual learning 干扰的贡献可能不同。  
如果能把 plastic / tail-sensitive update 与 common update 隔离，可能减少 forgetting。

#### H1: representation band 与 token-frequency function 相关

middle / tail variance band 可能对 middle / rare tokens 更关键。  
状态：未证实。

#### H2: forgetting 来自 non-uniform gradient interference

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

#### H3: frequency / variance-aware two-branch 有 CL 价值

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

## 4. Evidence

| 实验 / 阶段 | 关键结果 | 对主线的更新 |
|---|---|---|
| earlier single-layer block results | tail-conditioned / split-first block 曾出现真实模型正结果 | 支持继续研究 split-first，但不自动支持 CL |
| Phase8.2 formal CL | `u50_ext` 曾有弱 CL 信号 | 需要更严格 causal audit |
| latest H3-causal audit | matched dense / replay / raw two-branch 明显强于 real variance-band split；random split 也强于 `u50_ext` | H3 当前失败，不能用 real variance split 支撑 hierarchy |
| latest gradient audit | old/new hidden-gradient cosine 多为正；dense/raw 的 old loss 反而下降 | 当前 CL split 没有制造强 forgetting pressure |

---

## 5. 当前不确定点

1. 本轮 H3 失败，是因为 variance-band hypothesis 错了，还是因为 projected branch 学习信号太弱？
2. 当前 WoS old/new split 是否太相似，导致 dense baseline 没有真正 forgetting？
3. 为什么 raw two-branch 在本轮表现最强？
4. `head16` 明显强于 `u50/ext/u50_ext`，是否说明当前 CL adaptation 主要依赖 high-variance/common directions？
5. 如果要重新定义 plastic input，应使用 normalized projection、learned scaling，还是重新寻找 band？

---

## 6. Next Minimal Step

按照导师要求，完成Hierarchical的合成数据实验。

1. 首先构造数据集，数据集要符合Zipfian定律；构建训练目标
2. 设立对照组
3. 进行评估

---

## 8. 本日结束整理

### 今天推进了什么？

### 今天真正理解了什么？

### 哪个判断发生了变化？

### 明天最小下一步是什么？

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

---

## 10. 研究路线双版本整理（新增，不覆盖旧记录）

当前需要把研究路线拆成两个可并行陈述的版本：

1. **版本 A：直接探究 Hierarchical MoE**  
   按照老师要求，先构造真相已知的 synthetic natural Zipfian hierarchy dataset，再训练 hierarchical / routed MoE，检查模型是否能学出数据中的层级结构。

2. **版本 B：Two-branch + Router 探索**  
   基于 Phase8 / H3 causal audit 的结果，承认 pure two-branch split 不能直接支撑 CL claim，把研究中心转向 router：研究为什么 $P(x-\mu)$ 类 reference representation 能把表征分得更开，但不能稳定转化为下游收益，以及 learned routing 是否能把这种 separability 转化为 expert specialization。

---

## 11. 版本 A：Direct Hierarchical MoE

### 11.1 简短定位

这个版本不是证明真实语言天然有 hierarchy，而是在一个 ground-truth 已知的 synthetic world 中做 mechanism sanity check：

> 如果数据真的由 `common / coarse / fine` 三层机制生成，并且 word / phrase / token 出现频率符合 Zipfian 长尾，那么 hierarchical routed MoE 能不能从 NTP 训练中恢复这个层级结构？

当前数据集已经有 formal v1：

- `coarse_label`: 4 类，均匀；
- `fine_label`: 16 类，每个 coarse 下 4 类，均匀；
- train / valid / test: `20000 / 1000 / 1000` documents；
- sequence length: `128`；
- word/phrase Zipf: `alpha = 1.052, R2 = 0.974`；
- token-id Zipf: `alpha = 1.014, R2 = 0.933`；
- template-only shortcut 很低：coarse acc `0.254`，fine acc `0.064`。

这里的 Zipfian frequency 指的是 word / phrase / token 在语料中的出现频率，不是 PCA/SVD 谱空间中的 high / middle / low variance band。

### 11.2 Main Hypothesis

**H-A-main：** 如果 synthetic natural text 的生成机制真实包含 `common -> coarse -> fine` 的层级结构，那么一个参数量匹配的 conditional hierarchical MoE 应该能同时提升 NTP、恢复真实 coarse/source/fine route，并形成 selected expert advantage。

### 11.3 三个最重要的 Sub-hypotheses

**H-A1：Dataset hierarchy signal 可学习。**  
在 template shortcut 被控制、类别均匀、Zipfian token frequency 成立的前提下，模型应能仅从 NTP objective 中恢复 document-level `coarse/fine` 和 token-level `common/coarse/fine source`。

**H-A2：Middle-band routed hierarchy 有结构优势。**  
以 $\tilde{x}_M=P_{17:207}(h-\mu)$ 作为 coarse router input，并在 $M$ 内部继续用 `M_cc / M_tail` 做 source/fine routing，应优于 flat MoE middle、random-subspace routing 和 matched dense。

**H-A3：真正的 expert specialization 必须超过 router recovery。**  
即使 router accuracy 高，也不能直接说明 hierarchy 成立；必须看到 selected expert 的 counterfactual NTP loss 优于 alternative experts，尤其是在 coarse-source、fine-source、rare-frequency tokens 上。

### 11.4 当前风险

1. 目前 soft hierarchical mixture 还不等于严格 hard sparse Hierarchical MoE。
2. 如果 oracle hierarchy 不强，说明数据任务本身不需要 hierarchy。
3. 如果 H-CondCT-Soft 强但 expert advantage 不强，说明只是 label-correlated routing，不是功能专一化。

### 11.5 下一步

第一阶段必须至少比较：

```text
Dense matched
Flat MoE raw + LB
Flat MoE middle + LB
H-Mid-Soft
H-CondCT-Soft
H-CondCT-LevelInput
H-Oracle-CondCT
H-Rand-CondCT
Uniform Expert Mixture
```

主要看：

```text
NTP loss
coarse/source/fine router recovery
selected expert advantage
oracle regret
usage entropy
parameter-matched comparison
```

---

## 12. 版本 B：Two-branch + Router 研究路线

### 12.1 简短定位

这个版本承接 Phase8 / H3 causal audit。当前不能再把 two-branch split 直接作为 CL 成功证据，因为 matched dense、raw two-branch、random split、head16 等 control 已经削弱了原始 H3 claim。新的研究中心应该从“固定 split 是否直接带来 CL 收益”转向：

> 为什么 $P(x-\mu)$ 类 reference representation 可以让表征分得更开，却不能稳定转化为下游任务收益？learned router 能否把这种 separability 转化为真正的 expert specialization？

### 12.2 Main Hypothesis

**H-B-main：** $P(x-\mu)$ 及其 variance-band projection 暴露了某种 representation separability，但固定 two-branch split 缺少 task-conditional routing 和有效 expert assignment，因此 separability 不会自动转化为 downstream / CL gain；需要通过 learned router 检验这种分离是否能变成可用的 functional specialization。

### 12.3 三个最重要的 Sub-hypotheses

**H-B1：表征“分得开”不等于任务“用得上”。**  
Projection 或 variance-band split 可能提高 distribution separation / branch ablation contribution，但如果 task loss 主要依赖 raw common directions，或者 projected branch underfits，就不会带来 NTP / CL 收益。

**H-B2：当前 CL setting 没有提供足够稳定的 forgetting object。**  
Phase8-H3 bridge 中 dense baseline 没有形成清晰 positive forgetting，且 old/new hidden-gradient conflict 多数不呈明显负冲突，因此不能直接评估 anti-forgetting claim。

**H-B3：Router 是下一阶段核心变量。**  
如果 fixed split 失败但 branch contribution 在 middle/rare tokens 上仍有信号，那么下一步不是继续堆 split，而是做 routed expert：比较 learned routing、uniform mixture、oracle routing、flat raw MoE，并用 expert advantage / oracle regret 判断 routing 是否真正有用。

### 12.4 当前证据更新

来自 Phase8-H3 bridge old-stage causal audit：

1. Stage A 对齐了 old-stage CL protocol 和 H3 causal controls。
2. Dense、replay、raw two-branch、random split、head16、u50、ext、u50_ext、normalized variants、full_tail_resid 均已比较。
3. Gate decision 是 `no_valid_forgetting_object`：matched dense baseline 没有稳定 positive new-task learning / forgetting object，因此现在不能评价 anti-forgetting claim。
4. Branch ablation 显示 middle/rare contribution 可见，但这只能说明 split 有 contribution pattern，不能说明 expert specialization 或 routing advantage 成立。
5. Stage B routing diagnostics 尚未运行，因此不能声称 routing advantage 成立或失败。

### 12.5 下一步

Two-branch 路线的最小下一步不是继续声称 CL 收益，而是做 router audit：

```text
fixed two-branch
uniform expert mixture
flat raw MoE
flat projected MoE using P(x-mu)
oracle routing
learned routing
random-subspace routing
```

必须记录：

```text
selected expert advantage
oracle regret
router entropy
route-token bucket alignment
NTP by common/middle/rare tokens
matched parameter count
```

如果 learned routing 不能超过 uniform / random / raw MoE，则说明 $P(x-\mu)$ 的 separability 不是当前任务可用的 routing signal。  
如果 oracle routing 强但 learned routing 弱，则说明 expert 有潜力，但 router 学不出来。  
如果 oracle routing 也不强，则说明当前 split / task 不需要这种专家分工。

---

## 13. 两个版本的关系

版本 A 和版本 B 不冲突，但回答的问题不同：

| 版本 | 问题 | 当前最小目标 |
|---|---|---|
| Direct Hierarchical MoE | 如果数据真的有 hierarchy，MoE 能不能学出来？ | synthetic ground-truth hierarchy sanity check |
| Two-branch + Router | 固定 projection split 为什么分得开但不提升任务？ | 从 fixed split 转向 learned / oracle routing audit |

当前写作中应避免把版本 A 的 synthetic positive result 直接外推到真实 CL，也避免把版本 B 的 two-branch failure 直接解释为 hierarchy 不可能成立。
