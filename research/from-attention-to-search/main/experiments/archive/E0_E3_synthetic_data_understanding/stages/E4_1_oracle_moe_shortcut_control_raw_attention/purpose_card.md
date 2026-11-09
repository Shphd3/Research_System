# Experiment Card: E4.1 Oracle-MoE Shortcut Control With Raw Attention Router

## 1. Purpose / Main Reason

本实验要把 E4 的两个不确定点拆开：

```text
1. router 是否真的按 relation-level feature 分 expert；
2. E4 中 router 使用 LN(attention_output) 是否改变了 boundary geometry。
```

E4 已经说明 router selection 可以有 task utility，但不能证明 clean one-feature-one-expert。E4.1 的目的不是继续堆新的 router trick，而是用更干净的数据控制和 raw attention-output routing，判断 router 到底依赖 feature relation，还是依赖 token/target/common geometry。

## 2. Mainline Position

本实验接在 E4 Oracle-MoE Phase 1 之后。

E4 的当前结论是：

```text
task-useful expert selection != feature-aligned functional specialization
```

E4.1 是进入 Reverse Index 前的必要门控实验。只有 shortcut controls 下仍满足四联判据，才考虑进入 Reverse Index。

## 3. Known Narrative / Premise

已知前提：

- synthetic trigram feature 可以被模型 read back；
- feature representation 可以在 hidden / attention-output 空间中出现；
- C0/C2/C3/C4 的 router-selected expert 通常有 functional utility；
- 但 E4 的 `unique_uniform` 同时绑定了 feature、prefix-end token、target token 和 attention source token；
- E4 的 router logits 使用 `router_ln(attention_output)`，还不是 raw attention-output routing。

## 4. Experiment Purpose

本实验要判断：

```text
当 token shortcut 和 target shortcut 被拆开，并且 router 直接使用 raw attention_output 时，
Oracle-MoE 是否仍能形成 relation-level feature-aligned functional specialization？
```

## 5. Hypothesis And Sub-Hypotheses

H4.1: 如果 Oracle-MoE 真的学到 relation-level feature routing，那么在 shared prefix-end、shared target、crossed-factorial 数据上，router 仍应同时满足 feature assignment、boundary alignment、expert utility 和 readback。

H4.1a: 如果原先 routing 主要依赖 prefix-end token，则 shared prefix-end 后 feature-expert alignment 和 boundary alignment 会明显下降。

H4.1b: 如果原先 routing 主要依赖 target token，则 shared target 后同 target features 会更容易进入同一 expert，relation-level feature alignment 会变弱。

H4.1c: 如果原先 routing 主要依赖完整 relation，则 crossed-factorial 中即使 first token、prefix-end token、target token 被打散，routing 仍能按 relation feature 保持清晰。

H4.1d: 如果 raw attention-output routing 与 `LN(attention_output)` routing 差异很大，则 E4 的 boundary 结论应被限定为 LN-router-space 结论，不能直接外推到 raw attention geometry。

## 6. Experiment Object

对象是 1-layer Transformer + Oracle-MoE。

本轮关键改动：

```text
gate_input = raw attention_output
router logits use raw attention_output directly, without router LayerNorm
expert_input = original hidden / residual
```

数据控制至少包含：

```text
unique_uniform
shared_prefix_end
shared_target
crossed_factorial
```

## 7. Experiment Paradigm

对每个 dataset 训练或评估 C-series 的最小必要 router 组：

```text
C0 standard linear
C2 trainable center + repulsion
C3 inhibition margin
```

如资源允许再补 C1/C4。训练后重复 D-series 行为诊断和 boundary direction audit。

核心不看单一 NMI，而看四联判据：

```text
feature assignment
boundary alignment
expert utility
readback
```

## 8. Expected Outcomes And Hypothesis Update Logic

如果四联判据在 shortcut controls 下都成立：

```text
支持 relation-level feature-aligned functional specialization；
可以讨论进入 Reverse Index。
```

如果 readback 和 utility 成立，但 feature assignment / boundary alignment 不成立：

```text
说明 router 找到 task-useful partition，但不是 human-defined feature partition；
不进入 Reverse Index。
```

如果 shared prefix-end 或 shared target 后 routing 明显崩：

```text
说明 E4 的 routing 很可能依赖 token / target shortcut。
```

如果 raw attention routing 明显不同于 LN routing：

```text
说明 LayerNorm 改变了 router boundary geometry；
E4 结论必须限定为 LN-router-space。
```

## 9. What This Can Prove

它能在 synthetic setting 中判断当前 Oracle-MoE routing 是否经得起 token/target shortcut 控制，并判断 raw attention-output router 与 LN-router-space router 是否一致。

## 10. What This Cannot Prove

它不能证明真实语言 MoE expert 语义分工，不能证明 Reverse Index 有用，也不能把 high NMI 单独当作 functional specialization 证据。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

如果 purpose card 被确认，再写 execution plan。执行前先最终确认 inhibition loss 是否保留、修改或作为 ablation。
