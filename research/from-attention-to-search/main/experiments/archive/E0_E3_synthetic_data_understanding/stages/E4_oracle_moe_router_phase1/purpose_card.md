# Experiment Card: E4 Oracle-MoE Router Phase 1

## 1. Purpose / Main Reason

本实验要回答一个比 “feature 是否可分” 更直接的问题：

```text
在 Oracle-MoE 中，router 实际按什么标准把 token representation 分给 experts？
```

我们关心的是 router 分区、synthetic feature 分配、expert 功能差异和 NTP loss 是否一致。

## 2. Mainline Position

E2/E3 已经削弱了一个直觉：representation separability 不会自动导致 one-feature-one-expert routing。

E4 接在这个结论之后，只做 Phase 1：先诊断 Oracle-MoE router 机制，不进入 Reverse Index。

## 3. Known Narrative / Premise

已知前提：

- synthetic trigram feature 可以被 dense/MoE read back；
- feature label 可以作为 audit label，但不能直接等同于 router 机制；
- clean routing assignment 不等于 expert 功能 specialization；
- Reverse Index 是否有用必须等 router mechanism 先被说明。

## 4. Experiment Purpose

比较 C0-C4 五种 router 设计，并在训练后做行为诊断，判断：

1. router 是否按 planted feature 分；
2. router 是否按 token、target、attention source、common direction 或 difficulty 分；
3. router 选中的 expert 是否真的是当前样本功能上最好的 expert；
4. center separation / inhibition 是否产生了 functional specialization，还是只制造了人工排他性。

## 5. Hypothesis And Sub-Hypotheses

H4: 如果 Oracle-MoE 形成了真正有用的 feature specialization，那么 feature-to-expert assignment、expert utility matrix 和 NTP readback 应该同时一致。

H4a: 如果 router 主要按 planted feature 分，则 `P(expert | feature)` 应清楚，且反事实 feature 改动会导致 route flip。

H4b: 如果 router 主要按 shortcut/common geometry 分，则 expert assignment 会更好地被 token、target、attention source、norm/loss bin 或 top-PC removal 解释。

H4c: 如果 experts 功能冗余，则 utility matrix 不会 diagonal，即使 routing 看起来 clean，也不能 claim expert specialization。

H4d: 如果 inhibition 有效，它应提升 selected expert win rate，同时不显著破坏 NTP loss/readback。

## 6. Experiment Object

对象是 1-layer Transformer + Oracle-MoE：

```text
gate_input   = attention_output
expert_input = original hidden / residual entering MoE
```

数据是 uniform synthetic trigram：

```text
ABC: [1,2] -> 22
DEF: [3,4] -> 23
GHI: [6,7] -> 20
JKL: [8,9] -> 21
```

## 7. Experiment Paradigm

先训练 C0-C4，再只读 checkpoint 做 D0-D7 行为诊断。

训练阶段测试 router 设计是否能保持 NTP/readback。  
诊断阶段测试 router cell 的实际组成和 expert utility，而不是用 feature probe 代替机制解释。

## 8. Expected Outcomes And Hypothesis Update Logic

如果 feature assignment、utility matrix、NTP readback 都一致，则支持 synthetic feature-aligned functional specialization。

如果 feature assignment clean 但 utility 不 diagonal，则说明 routing clean 不等于 expert 功能分化。

如果 NTP/readback 好但 routing 不按 feature 分，则说明当前任务不要求 feature-aligned specialization。

如果 center 分开但 feature alignment 低，则说明几何中心分离不足以得到 feature specialization。

如果 inhibition 提高排他性但损害 NTP，则说明它是人工 exclusivity，不是有用机制。

## 9. What This Can Prove

它能证明在当前 synthetic Oracle-MoE 设置下，某种 router 设计是否同时产生 feature-aligned routing 和 functional expert utility。

## 10. What This Cannot Prove

它不能证明 Reverse Index 有用，不能证明真实语言 expert 语义，也不能把 NMI 或 feature probe 当作 specialization 机制证据。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

只有在 routing assignment、expert utility 和 NTP/readback 同时支持 functional feature specialization 时，才进入 Reverse Index stage。
