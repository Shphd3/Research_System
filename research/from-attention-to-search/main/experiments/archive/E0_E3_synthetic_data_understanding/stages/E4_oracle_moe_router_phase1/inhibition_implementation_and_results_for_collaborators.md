# Inhibition Implementation And Results Note

## TL;DR

本说明整理当前实验中 `inhibition` 的实现和证据边界，方便和合作者讨论。我们现在主要有两类 inhibition：一种是我们实现的 **clean expert-only CE inhibition**，用于 C5/C6 和 R0/R1 中的 P2；另一种是 Dingyi-style **prototype score inhibition**，用于 C7d 这类 prototype router。两者机制不同，不能混在一起解释。

当前最安全结论是：clean inhibition 可以增强 expert functional exclusivity，让 router 选中的 expert 更稳定地成为 forced-routing 下最有用的 expert；但它本身不证明 relation-level one-feature-one-expert。R0/R1 结果进一步显示，clean inhibition 的 bucket 在 uniform two-forward RI 中几乎无 CE 损失，但这应解释为“候选质量好、接近 full attention”，不能说 restricted attention 真正优于 full attention。

## 1. What Is Being Tested

我们关心的问题不是“inhibition 这个词是否合理”，而是：

能不能通过一个额外正则项，让不同 expert 不要学成完全一样，从而形成更有功能差异的 expert bucket。

这里的 functional specialization 指：

router 选中的 expert，在 forced-routing 诊断下确实比其他 expert 更适合当前样本。

它不同于 feature-aligned specialization：

例如 `ABC -> expert 0`、`DEF -> expert 1`、`GHI -> expert 2`、`JKL -> expert 3`。

当前证据更支持前者，而不是后者。

## 2. Our Clean Expert-Only CE Inhibition

### 2.1 Main Idea

对一个样本，router 先选出 winning expert：

$$
e_{\mathrm{sel}} = \arg\max_e \operatorname{logit}_e
$$

主路径仍然正常训练 next-token prediction：

$$
L_{\text{NTP}} = \operatorname{CE}(y, f(x; e_{\mathrm{sel}}))
$$

clean inhibition 额外做一件事：让其他 experts 在这个样本上不要和 selected expert 一样好。

直观说：

selected expert 正常学当前样本；other experts 如果也能很好预测当前样本，就被惩罚。

### 2.2 Loss Definition

我们先固定 shared representation：

$$
h_{\text{detach}} = \operatorname{stopgrad}(h)
$$

然后对每个非选中 expert 计算 forced-routing CE：

$$
\operatorname{CE}_e = \operatorname{CE}(y, f(h_{\text{detach}}; e))
$$

selected expert 的 CE 只作为 reference：

$$
\operatorname{CE}_{e_{\mathrm{sel}}}^{\text{ref}}
=
\operatorname{stopgrad}(\operatorname{CE}_{e_{\mathrm{sel}}})
$$

clean inhibition loss 是：

$$
L_{\text{clean-inh}}
=
\frac{1}{E-1}
\sum_{e\neq e_{\mathrm{sel}}}
\max\left(
0,\ 
m-\left(\operatorname{CE}_e-\operatorname{CE}_{e_{\mathrm{sel}}}^{\text{ref}}\right)
\right)
$$

含义是：

如果 other expert 的 $\operatorname{CE}_e$ 没有比 selected expert 差至少 margin $m$，就惩罚这个 other expert。

### 2.3 Gradient Path

这是最容易误解的地方。

我们的 clean inhibition 不是：

先算 selected expert 的梯度 $g$，再用 $-g$ 更新 other experts。

而是：

每个 other expert 自己 forward，自己得到 $\operatorname{CE}_e$，再由 inhibition loss 反向更新自己。

因此它不是 explicit gradient reversal。它是 CE-margin based expert-only penalty。

梯度路径：

| 参数部分 | 是否吃 inhibition 梯度 | 原因 |
|---|---:|---|
| selected expert | 否 | selected CE 只作为 detached reference |
| other experts | 是 | 它们的 $\operatorname{CE}_e$ 进入 inhibition loss |
| attention / shared path | 否 | shared representation 被 detach |
| router | 否 | selected expert id 被 detach |
| LayerNorm / LM head | 否 | inhibition path 中使用 detached readout |

本地 smoke 的梯度检查：

| variant | shared grad norm | expert grad norm |
|---|---:|---:|
| C5 | 0.0000 | 0.0170 |
| C6 | 0.0000 | 0.0134 |

这说明 inhibition 辅助项确实只更新 expert 参数。

### 2.4 Total Training Loss

在 C5/C6/P2 里，总 loss 是：

$$
L
=
L_{\text{NTP}}
+\lambda_{\text{LB}} L_{\text{LB}}
+\lambda_{\text{inh}} L_{\text{clean-inh}}
$$

P2 不使用 feature label，不使用 oracle routing。它相对普通 MoE 只多了 clean inhibition 正则项。

## 3. Difference From Dingyi-Style Prototype Inhibition

Dingyi-style inhibition 是 prototype score margin，不是 CE expert-only inhibition。

在 Dingyi 实现里，router 有 prototypes。给定输入表征 $q$，计算每个 prototype 的 score。winning prototype 是最高分 expert：

$$
e_{\mathrm{sel}} = \arg\max_e s_e
$$

Dingyi-style auxiliary losses 包括三项：

1. attraction：让 $q$ 靠近 winning prototype；
2. score inhibition：让 winning score 高于 strongest losing score；
3. homeostasis：让 expert 使用率不要 collapse。

对应核心项是：

$$
L_{\text{score-inh}}
=
\max(0,\ m+s_{\text{loser}}-s_{\text{winner}})
$$

这和我们的 clean CE inhibition 不同：

| 方法 | 惩罚对象 | 比较量 | 是否直接看 expert CE | 是否主要作用在 prototypes / router geometry |
|---|---|---|---:|---:|
| clean CE inhibition | other experts | $\operatorname{CE}_e-\operatorname{CE}_{e_{\mathrm{sel}}}$ | 是 | 否 |
| Dingyi-style score inhibition | losing prototypes / router scores | $s_{\text{winner}}-s_{\text{loser}}$ | 否 | 是 |

因此，汇报时应避免说“P2 完全按照 Dingyi inhibition”。更准确的说法是：

P2 是我们自己的 clean expert-only CE inhibition；C7d/C7e 更接近 Dingyi-style prototype / score-margin route shaping。

## 4. E4 C5/C6 Results

主实验使用 load balance。C5 是 linear router + clean inhibition；C6 是 center router + repulsion + clean inhibition。

| variant | loss | readback | NMI | selected-best | CE gap | inhibition gap | violation | boundary align | load entropy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C5 | 6.651 | 0.9999 | 0.346 | 1.000 | 0.0000 | 3.414 | 0.0000 | 0.112 | 0.416 |
| C6 | 6.652 | 0.9999 | 0.697 | 1.000 | 0.0000 | 2.648 | 0.0000 | 0.087 | 0.684 |

Interpretation:

- C5/C6 的 selected-best rate 都达到 1.0，说明 router 选中的 expert 在 forced-routing 诊断下确实是最有用的 expert。
- C5/C6 的 inhibition violation 为 0，说明 clean inhibition 成功拉开 selected expert 和 other experts 的 CE 差距。
- C5 的 NMI 低，C6 的 NMI 较高，但二者 boundary-feature alignment 都低。这说明 clean inhibition 主要改善 functional utility，不直接产生 clean relation-level feature boundary。

No-LB 消融：

| variant | loss | readback | NMI | selected-best | inhibition gap | violation | load entropy | dead experts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C5-noLB | 6.647 | 1.0000 | 0.000 | 1.000 | 2.414 | 0.0758 | 0.000 | 3.0 |
| C6-noLB | 6.647 | 1.0000 | 0.000 | 1.000 | 2.647 | 0.0000 | 0.000 | 3.0 |

Interpretation:

clean inhibition 不能替代 load balance。

没有 LB 时，readback 仍然成功，但 expert allocation collapse 到极少数 expert，feature-expert NMI 接近 0。

## 5. R0/R1 P2 Results

R0/R1 中的 P2 使用 post-attention clean inhibition + load balance。它不使用 feature label。

| data | model | NMI | RI $\Delta CE$ | random $\Delta CE$ | RI mass | random mass |
|---|---:|---:|---:|---:|---:|---:|
| uniform | P2 | 0.459 | -0.001 | 2.553 | 0.712 | 0.417 |
| zipf | P2 | 0.409 | 0.344 | 2.682 | 0.638 | 0.424 |

Important caveat:

uniform 的 `RI ΔCE = -0.001` 不能解释成 restricted attention 真正超过 full attention。

它的量级接近 0，且在 seed 间标准差范围内。正确解释是：

P2 在 uniform 上几乎无 CE 损失。

为什么 P2 可能在 RI 上好：

- 它不追求 feature purity；
- 它让 expert 功能更分开；
- same-bucket KV 保留的 attention mass 在 uniform 中最高；
- 因此它可能形成了更适合 attention reconstruction 的 functional bucket。

但这仍是机制解释，不是最终证明。当前缺少对 P2 的精确 expert load audit 和更完整 candidate-generator tournament。

## 6. What We Can Claim

Supported:

- clean inhibition 的梯度链路是干净的：auxiliary inhibition 不更新 shared path / router / LM head；
- clean inhibition 可以增强 expert utility separation；
- 在 C5/C6 中，router-selected expert 成为 forced-routing best expert；
- 在 R0/R1 中，P2 的 same-bucket KV 明显优于 random same-count KV；
- no-LB 会 collapse，说明 clean inhibition 不能替代 load balance。

Weakened:

- clean inhibition 不足以证明 relation-level one-feature-one-expert；
- NMI 高不等于 functional specialization；
- feature-pure bucket 不一定是好的 Reverse Index bucket。

Cannot claim:

- clean inhibition 已经解决 MoE specialization；
- clean inhibition 已经解决 Reverse Index；
- P2 的 restricted attention 真正优于 full attention；
- synthetic toy setting 可直接推出真实语言模型效果。

## 7. Suggested Collaborator-Facing Wording

建议这样向合作者概括：

Our clean inhibition is an expert-only CE-margin auxiliary loss. It does not reverse the selected expert gradient. Instead, each non-selected expert is forced forward on the same detached shared representation; if it performs too similarly to the selected expert, it receives a penalty. This makes experts less functionally redundant. Empirically, it improves selected-best expert behavior and gives useful RI buckets, but it does not by itself prove relation-level one-feature-one-expert routing.

中文版本：

我们的 clean inhibition 不是把 winning expert 的梯度取反后施加给其他 expert。它是让其他 expert 各自前向，如果它们在当前样本上也预测得太好，就通过自己的 CE 被惩罚。这个辅助项只更新 expert，不更新 shared path / router。结果上，它能增强 expert 功能排他性，也能产生较好的 RI bucket；但它还不能证明 expert 已经按人工 feature 做了 clean specialization。

## 8. Source Pointers

Current project reports:

- `C5_C6_clean_inhibition_report.md`
- `R0_R1_post_attention_moe_two_pass_ri/summary.md`

Implementation references:

- clean CE inhibition: `scripts/run_post_attention_moe_two_pass_ri.py`
- Dingyi-style prototype inhibition: `dingyi/synthetic/scripts/run_prototype_inhibition_experiment.py`
- Dingyi-style oracle-init prototype inhibition: `dingyi/synthetic/scripts/run_oracle_initialized_router_experiment.py`
