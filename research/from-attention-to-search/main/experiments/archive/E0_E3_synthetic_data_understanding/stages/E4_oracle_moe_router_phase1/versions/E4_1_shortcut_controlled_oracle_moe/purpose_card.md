# Purpose Card: E4.1 Shortcut-Controlled Oracle-MoE

## 1. Purpose / Main Reason

E4.1 的目的不是继续证明 `unique_uniform` 上能否出现 one-feature-one-expert，而是检查这种分工是否真的来自上下文关系。

当前 `unique_uniform` 中，人工 feature、prefix-end token、target token 和 attention source 绑定在一起。即使 router 分得很干净，也可能只是按 token shortcut 或 target shortcut 分，而不是按 `[A,B] -> C` 这种关系分。

## 2. Mainline Position

E4.1 接在 E4 raw-attention C0-C7 之后。

E4 raw-attention 先判断：

```text
router 吃 raw attention_output 时，C0-C7 哪些机制能形成可读回、可分配、可解释的 expert routing。
```

E4.1 再判断：

```text
这些 routing 现象是否能在去掉 token / target 捷径后继续成立。
```

只有 E4.1 通过，才有资格进入 Reverse Index 主线。

## 3. Known Narrative / Premise

前序 E2/E3/E4 已经说明：

- feature representation 可以在 hidden / attention-output 空间中出现；
- router boundary 不一定沿 feature direction 切；
- expert utility 和 feature assignment 需要分开检查；
- high NMI 不能单独证明 expert specialization；
- `unique_uniform` 不能区分 relation-level feature 与 token shortcut。

## 4. Experiment Purpose

本实验回答：

```text
当 prefix token、prefix-end token、target token 被控制或打散后，
E4 中看起来有效的 router 机制是否仍然能形成 feature-aligned functional specialization？
```

这里的 functional specialization 必须同时满足：

```text
feature assignment 清楚
router boundary 与 feature direction 对齐
router 选中的 expert 有实际 utility
NTP readback 保持良好
```

## 5. Hypothesis And Sub-Hypotheses

主假设：

```text
H4.1: 如果 C-series / C7 的分工是真正基于上下文关系，
那么在 shared-prefix-end、shared-target、crossed-factorial controls 中，
它仍应保持 feature assignment、boundary alignment、expert utility 和 readback 的一致性。
```

细化假设：

- H4.1a: 若 router 主要依赖 prefix-end token，则 `shared_prefix_end_uniform` 会使相关 features 混到同一 expert。
- H4.1b: 若 router 主要依赖 target token，则 `shared_target_uniform` 中同 target 的 features 会 route 相似。
- H4.1c: 若 router 真的使用 relation-level feature，则 `crossed_factorial_uniform` 中单个 token 不足以解释 expert assignment。
- H4.1d: 若 C7 oracle-init 只是利用 `unique_uniform` 的 token cluster，它在 crossed-factorial 中会显著变弱。
- H4.1e: 若 C6 clean inhibition 主要增强 expert utility，而不是 relation routing，它可能 selected-best 高，但 feature-boundary alignment 仍弱。

## 6. Experiment Object

模型仍为 1-layer Transformer + Oracle-MoE：

```text
gate_input   = raw attention_output
expert_input = original hidden / residual
```

实验对象是 E4 中最关键的 router 机制：

```text
C0: standard linear router
C6: center clean expert inhibition
C7a: Dingyi random prototype
C7b: Dingyi frozen oracle centers
C7c: Dingyi trainable oracle-init centers
C7d: Dingyi oracle-init + inhibition / homeostasis
```

如果算力允许，再补 C5、C7e 和完整 C0-C7。

## 7. Experiment Paradigm

用四类 synthetic datasets 控制 shortcut：

```text
unique_uniform
shared_prefix_end_uniform
shared_target_uniform
crossed_factorial_uniform
```

每个 dataset 上训练同一组 router variants，然后做相同诊断：

- feature-to-expert assignment；
- token / target / feature 对 expert assignment 的解释力；
- boundary-feature alignment；
- forced expert utility matrix；
- readback accuracy；
- counterfactual route flip。

## 8. Expected Outcomes And Hypothesis Update Logic

如果 E4.1 成立：

```text
router 分工不是 unique_uniform 的 token/target shortcut；
relation-level feature routing 在 toy setting 中更可信；
可以进入 Reverse Index 的 R1 source decomposition。
```

如果只在 `unique_uniform` 成立：

```text
E4 的 clean routing 更可能是 shortcut routing；
不能把它接到 Reverse Index。
```

如果 readback 成功但 utility 不 diagonal：

```text
模型能做 NTP，但 experts 仍未形成可用于 index 的功能分工。
```

如果 feature assignment 清楚但 boundary / utility 不支持：

```text
不能用 NMI 宣称 functional specialization。
```

## 9. What This Can Prove

E4.1 可以证明：

```text
在 synthetic controlled setting 中，某个 router 机制是否能在去除 token/target 捷径后仍保持 relation-level feature specialization。
```

## 10. What This Cannot Prove

E4.1 不能证明：

- 真实语言中存在同样的 feature labels；
- MoE 会自然学到 relation-level routing；
- relation-level routing 一定能做 Reverse Index；
- Reverse Index 可以加速或保持真实长上下文性能。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

若 E4.1 支持 relation-level functional specialization，进入 Reverse Index R1；否则继续诊断 router shortcut 或任务设计。
